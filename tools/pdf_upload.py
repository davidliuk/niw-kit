#!/usr/bin/env python3
"""PDF helpers for exhibit covers and size-limited online upload files.

Every helper fails closed: it raises BuildError instead of silently producing
a degraded file.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Sequence

import pikepdf

from tools.build_support import (
    BuildError,
    merge_pdfs_structured,
    pdf_page_count,
    rasterize_pdf,
    resolve_executable,
    run_checked,
    validate_pdf,
)
from tools.package_model import Exhibit, ExhibitSeries

# Conservative per-file ceiling for USCIS online uploads. Check the current
# limit on the live upload screen and lower `upload_limit_bytes` in case.json
# if it is smaller.
USCIS_LIMIT_BYTES = 12_000_000
BUILD_LIMIT_BYTES = 11_500_000
INTERNAL_PORTAL_FILENAME_LIMIT = 100
PORTAL_FILENAME_PATTERN = re.compile(r"[A-Za-z0-9._()-]+\.pdf")

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_slug(value: str, *, maximum: int = 72) -> str:
    """Return a conservative ASCII filename component for portal preparation."""

    normalized = unicodedata.normalize(
        "NFKD",
        re.sub(r"[\u2010-\u2015\u2212]", "-", value),
    )
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9._()-]+", "_", ascii_value).strip("._-")
    slug = re.sub(r"_+", "_", slug)
    slug = slug or "document"
    if len(slug) <= maximum:
        return slug
    shortened = slug[:maximum].rstrip("._-")
    if "_" in shortened:
        word_boundary = shortened.rsplit("_", 1)[0].rstrip("._-")
        if len(word_boundary) >= maximum // 2:
            shortened = word_boundary
    return shortened


def validate_portal_filenames(filenames: Sequence[str]) -> None:
    """Fail closed on internally unsafe or ambiguous upload filenames."""

    seen: dict[str, str] = {}
    for filename in filenames:
        if len(filename) > INTERNAL_PORTAL_FILENAME_LIMIT:
            raise BuildError(
                f"online upload filename exceeds internal "
                f"{INTERNAL_PORTAL_FILENAME_LIMIT}-character safety limit: "
                f"{filename}"
            )
        if not PORTAL_FILENAME_PATTERN.fullmatch(filename):
            raise BuildError(
                "online upload filename must use only ASCII letters, digits, "
                f"periods, underscores, hyphens, and parentheses: {filename}"
            )
        folded = filename.casefold()
        if folded in seen:
            raise BuildError(
                "online upload filenames must be case-insensitively unique: "
                f"{seen[folded]} and {filename}"
            )
        seen[folded] = filename


def write_page_subset(source: Path, pages: Sequence[int], destination: Path) -> None:
    with pikepdf.Pdf.open(source) as input_pdf:
        output_pdf = pikepdf.Pdf.new()
        for page_number in pages:
            output_pdf.pages.append(input_pdf.pages[page_number])
        output_pdf.save(
            destination,
            linearize=True,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            deterministic_id=True,
        )


def widget_annotation_pages(source: Path) -> tuple[int, ...]:
    """Return one-based pages whose visible evidence may live in form widgets."""

    try:
        with pikepdf.Pdf.open(source) as pdf:
            pages: list[int] = []
            for page_number, page in enumerate(pdf.pages, start=1):
                for annotation in page.get("/Annots", ()):
                    if str(annotation.get("/Subtype", "")) == "/Widget":
                        pages.append(page_number)
                        break
            return tuple(pages)
    except (pikepdf.PdfError, pikepdf.PasswordError) as error:
        raise BuildError(
            f"cannot inspect PDF annotations in {source}: {error}"
        ) from error


def flatten_widget_pages_for_upload(
    *,
    source: Path,
    destination: Path,
    temporary: Path,
    dpi: int = 200,
    jpeg_quality: int = 94,
) -> tuple[int, ...]:
    """Rasterize only pages whose evidence would be lost with stripped forms."""

    widget_pages = widget_annotation_pages(source)
    if not widget_pages:
        shutil.copy2(source, destination)
        return ()

    page_count = pdf_page_count(source)
    rasterized = temporary / f"{source.stem}-widget-rasterized.pdf"
    rasterize_pdf(
        source,
        rasterized,
        dpi=dpi,
        jpeg_quality=jpeg_quality,
    )
    validate_pdf(rasterized, expected_pages=page_count)

    widget_page_set = set(widget_pages)
    page_files: list[Path] = []
    for page_number in range(1, page_count + 1):
        page_file = temporary / (
            f"{source.stem}-widget-safe-{page_number:04d}.pdf"
        )
        page_source = rasterized if page_number in widget_page_set else source
        write_page_subset(page_source, (page_number - 1,), page_file)
        page_files.append(page_file)

    merge_pdfs_structured(
        tuple((None, page_file) for page_file in page_files),
        destination,
    )
    validate_pdf(destination, expected_pages=page_count)
    return widget_pages


def candidate_size(
    *,
    cover: Path,
    payload: Path,
    pages: Sequence[int],
    temporary: Path,
    label: str,
) -> int:
    subset = temporary / f"{label}-subset.pdf"
    candidate = temporary / f"{label}-candidate.pdf"
    write_page_subset(payload, pages, subset)
    merge_pdfs_structured(((None, cover), (None, subset)), candidate)
    return candidate.stat().st_size


def split_page_groups(
    *,
    cover: Path,
    payload: Path,
    temporary: Path,
    maximum_bytes: int,
) -> tuple[tuple[int, ...], ...]:
    pages = tuple(range(pdf_page_count(payload)))

    def divide(group: tuple[int, ...], label: str) -> list[tuple[int, ...]]:
        size = candidate_size(
            cover=cover,
            payload=payload,
            pages=group,
            temporary=temporary,
            label=label,
        )
        if size <= maximum_bytes:
            return [group]
        if len(group) == 1:
            raise BuildError(
                f"single page in {payload} exceeds online upload safety limit"
            )
        midpoint = len(group) // 2
        return [
            *divide(group[:midpoint], f"{label}a"),
            *divide(group[midpoint:], f"{label}b"),
        ]

    return tuple(divide(pages, "split"))


def optimize_single_pages_for_upload(
    *,
    cover: Path,
    payload: Path,
    temporary: Path,
    maximum_bytes: int,
    dpi: int = 160,
    jpeg_quality: int = 90,
) -> tuple[Path, tuple[int, ...]]:
    """Rasterize only a page that cannot fit in an upload by itself."""

    if cover.stat().st_size + payload.stat().st_size <= maximum_bytes:
        return payload, ()

    page_files: list[Path] = []
    rasterized_pages: list[int] = []
    for page_index in range(pdf_page_count(payload)):
        page_number = page_index + 1
        subset = temporary / f"upload-page-{page_number:04d}.pdf"
        write_page_subset(payload, (page_index,), subset)
        candidate = temporary / f"upload-page-{page_number:04d}-with-cover.pdf"
        merge_pdfs_structured(((None, cover), (None, subset)), candidate)
        if candidate.stat().st_size > maximum_bytes:
            rasterized = temporary / f"upload-page-{page_number:04d}-raster.pdf"
            rasterize_pdf(
                subset,
                rasterized,
                dpi=dpi,
                jpeg_quality=jpeg_quality,
            )
            validate_pdf(rasterized, expected_pages=1, require_letter=True)
            merge_pdfs_structured(((None, cover), (None, rasterized)), candidate)
            if candidate.stat().st_size > maximum_bytes:
                raise BuildError(
                    f"source page {page_number} in {payload} exceeds the online "
                    f"upload safety limit even after controlled rasterization"
                )
            subset = rasterized
            rasterized_pages.append(page_number)
        page_files.append(subset)

    if not rasterized_pages:
        return payload, ()
    optimized = temporary / f"{payload.stem}-upload-optimized.pdf"
    merge_pdfs_structured(tuple((None, page) for page in page_files), optimized)
    validate_pdf(
        optimized,
        expected_pages=pdf_page_count(payload),
        require_letter=True,
    )
    return optimized, tuple(rasterized_pages)


def _typst_string(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )


def cover_typst(series: ExhibitSeries, exhibit: Exhibit) -> str:
    """Render one deterministic Typst cover source."""

    supports = exhibit.supports or "See petition and exhibit index."
    return f"""#set page(paper: "us-letter", margin: 0.8in)
#set text(font: ("Arial", "Helvetica"), size: 12pt)
#v(1.2in)
#text(size: 26pt, weight: "bold", "Exhibit {_typst_string(exhibit.id)}")
#v(0.25in)
#text(size: 18pt, weight: "bold", "{_typst_string(exhibit.title)}")
#v(0.45in)
#strong[Series:] #text("{_typst_string(series.id)} — {_typst_string(series.title)}")

#strong[Source:] #text("{_typst_string(exhibit.source)}")

#strong[Date:] #text("{_typst_string(exhibit.date_display)}")

#strong[Supports:] #text("{_typst_string(supports)}")
"""


def compile_typst(source: Path, destination: Path, *, root: Path) -> None:
    typst = resolve_executable("typst")
    run_checked(
        (typst, "compile", "--root", root, source, destination),
        cwd=root,
        quiet=True,
        environment={"SOURCE_DATE_EPOCH": "0"},
    )
