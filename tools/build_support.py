#!/usr/bin/env python3
"""Shared, fail-closed helpers for petition document builds."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pikepdf
from PIL import Image

LETTER_SIZE = (612.0, 792.0)
PAGE_SIZE_TOLERANCE = 1.0

class BuildError(RuntimeError):
    """Raised when a deterministic build step cannot complete safely."""


_PAGE_NUMBER_PATTERN = re.compile(r"-(\d+)\.[^.]+$")


def _rendered_page_number(path: Path) -> int:
    match = _PAGE_NUMBER_PATTERN.search(path.name)
    if match is None:
        raise BuildError(f"cannot determine rendered page number: {path}")
    return int(match.group(1))


def resolve_executable(
    name: str,
    *,
    explicit: str | Path | None = None,
    candidates: Iterable[str | Path] = (),
) -> Path:
    """Resolve an executable or raise an actionable build error."""

    if explicit is not None:
        path = Path(explicit).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return path
        raise BuildError(f"required executable is not usable: {path}")

    discovered = shutil.which(name)
    if discovered:
        return Path(discovered)

    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return path

    raise BuildError(
        f"required executable '{name}' was not found; install it or pass an explicit path"
    )


def run_checked(
    command: Sequence[str | Path],
    *,
    cwd: str | Path | None = None,
    quiet: bool = False,
    environment: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command and surface its full failure context."""

    normalized = [str(part) for part in command]
    result = subprocess.run(
        normalized,
        cwd=cwd,
        env=(
            {**os.environ, **environment}
            if environment is not None
            else None
        ),
        text=True,
        stdout=subprocess.PIPE if quiet else None,
        stderr=subprocess.PIPE if quiet else None,
    )
    if result.returncode:
        details = []
        if result.stdout:
            details.append(result.stdout.strip())
        if result.stderr:
            details.append(result.stderr.strip())
        detail_text = "\n".join(details)
        suffix = f"\n{detail_text}" if detail_text else ""
        raise BuildError(
            f"command failed ({result.returncode}): {' '.join(normalized)}{suffix}"
        )
    return result


def atomic_replace(source: Path, destination: Path) -> None:
    """Atomically replace a generated artifact after creating its directory."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source, destination)


def pdf_page_sizes(path: Path) -> tuple[tuple[float, float], ...]:
    """Return MediaBox dimensions for every PDF page."""

    try:
        with pikepdf.Pdf.open(path) as pdf:
            return tuple(
                (
                    float(page.MediaBox[2]) - float(page.MediaBox[0]),
                    float(page.MediaBox[3]) - float(page.MediaBox[1]),
                )
                for page in pdf.pages
            )
    except (pikepdf.PdfError, pikepdf.PasswordError) as error:
        raise BuildError(f"cannot validate PDF {path}: {error}") from error


def validate_pdf(
    path: Path,
    *,
    expected_pages: int | None = None,
    require_letter: bool = False,
) -> int:
    """Validate PDF structure, page count, and optional Letter-size invariant."""

    if not path.is_file() or path.stat().st_size == 0:
        raise BuildError(f"missing or empty PDF: {path}")
    sizes = pdf_page_sizes(path)
    pages = len(sizes)
    if pages == 0:
        raise BuildError(f"PDF contains no pages: {path}")
    if expected_pages is not None and pages != expected_pages:
        raise BuildError(
            f"PDF page count mismatch for {path}: expected {expected_pages}, got {pages}"
        )
    if require_letter:
        bad = [
            (index, width, height)
            for index, (width, height) in enumerate(sizes, start=1)
            if (
                abs(width - LETTER_SIZE[0]) > PAGE_SIZE_TOLERANCE
                or abs(height - LETTER_SIZE[1]) > PAGE_SIZE_TOLERANCE
            )
        ]
        if bad:
            preview = ", ".join(
                f"p{index}={width:.1f}x{height:.1f}"
                for index, width, height in bad[:8]
            )
            raise BuildError(f"non-Letter pages in {path}: {preview}")
    return pages


def _stabilize_overlay_resource_name(page: pikepdf.Page, page_number: int) -> None:
    """Replace pikepdf's random overlay XObject name with a stable page-local name."""

    xobjects = page.Resources.XObject
    names = tuple(xobjects.keys())
    if len(names) != 1:
        raise BuildError(
            f"expected one overlay XObject on normalized page {page_number}, "
            f"found {len(names)}"
        )
    random_name = names[0]
    stable_name = pikepdf.Name(f"/NormalizedPage{page_number}")
    content = page.Contents.read_bytes()
    random_token = str(random_name).encode("ascii") + b" Do"
    stable_token = str(stable_name).encode("ascii") + b" Do"
    if content.count(random_token) != 1:
        raise BuildError(
            f"cannot locate unique overlay invocation on normalized page {page_number}"
        )
    xobjects[stable_name] = xobjects[random_name]
    del xobjects[random_name]
    page.Contents.write(content.replace(random_token, stable_token))


def normalize_pdf_pages_to_letter(source: Path, destination: Path) -> int:
    """Place every source page, vector-preserved, on a Letter-size canvas."""

    if not source.is_file():
        raise BuildError(f"cannot normalize missing PDF: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{destination.stem}-letter-", dir=destination.parent
    ) as temporary_directory:
        staged = Path(temporary_directory) / destination.name
        try:
            source_pdf = pikepdf.Pdf.open(source)
        except (pikepdf.PdfError, pikepdf.PasswordError) as error:
            raise BuildError(f"cannot normalize PDF {source}: {error}") from error
        output_pdf = pikepdf.Pdf.new()
        outlines: list[pikepdf.OutlineItem] = []
        try:
            for page_number, source_page in enumerate(source_pdf.pages, start=1):
                box = source_page.MediaBox
                width = float(box[2]) - float(box[0])
                height = float(box[3]) - float(box[1])
                scale = min(LETTER_SIZE[0] / width, LETTER_SIZE[1] / height)
                draw_width = width * scale
                draw_height = height * scale
                left = (LETTER_SIZE[0] - draw_width) / 2
                bottom = (LETTER_SIZE[1] - draw_height) / 2
                target_page = output_pdf.add_blank_page(page_size=LETTER_SIZE)
                target_page.add_overlay(
                    source_page,
                    pikepdf.Rectangle(
                        left,
                        bottom,
                        left + draw_width,
                        bottom + draw_height,
                    ),
                    shrink=True,
                    expand=False,
                )
                _stabilize_overlay_resource_name(target_page, page_number)
            output_pdf.save(
                staged,
                linearize=True,
                compress_streams=True,
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                deterministic_id=True,
            )
        finally:
            source_pdf.close()
            output_pdf.close()
        pages = validate_pdf(staged, require_letter=True)
        atomic_replace(staged, destination)
    return pages


def merge_pdfs(
    inputs: Sequence[Path],
    output: Path,
    *,
    pdfunite: str | Path | None = None,
) -> None:
    """Merge PDFs into a staged output and atomically publish it."""

    if not inputs:
        raise BuildError("cannot merge an empty PDF list")
    missing = [str(path) for path in inputs if not path.is_file()]
    if missing:
        raise BuildError(f"cannot merge missing PDFs: {', '.join(missing)}")

    executable = resolve_executable("pdfunite", explicit=pdfunite)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{output.stem}-", dir=output.parent
    ) as temporary_directory:
        staged = Path(temporary_directory) / output.name
        run_checked((executable, *inputs, staged), quiet=True)
        atomic_replace(staged, output)


def rasterize_pdf(
    source: Path,
    destination: Path,
    *,
    dpi: int = 120,
    jpeg_quality: int = 88,
    pdftoppm: str | Path | None = None,
    pdfunite: str | Path | None = None,
) -> None:
    """Create a structurally clean, image-only PDF with preserved page order."""

    if not source.is_file():
        raise BuildError(f"cannot rasterize missing PDF: {source}")
    if dpi <= 0:
        raise BuildError("raster DPI must be positive")
    if not 1 <= jpeg_quality <= 100:
        raise BuildError("JPEG quality must be between 1 and 100")

    render_tool = resolve_executable("pdftoppm", explicit=pdftoppm)
    merge_tool = resolve_executable("pdfunite", explicit=pdfunite)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix=f".{destination.stem}-", dir=destination.parent
    ) as temporary_directory:
        temporary = Path(temporary_directory)
        image_prefix = temporary / "page"
        run_checked(
            (
                render_tool,
                "-r",
                str(dpi),
                "-jpeg",
                "-jpegopt",
                f"quality={jpeg_quality},progressive=y",
                source,
                image_prefix,
            ),
            quiet=True,
        )
        images = sorted(
            temporary.glob("page-*.jpg"),
            key=_rendered_page_number,
        )
        if not images:
            raise BuildError(f"pdftoppm produced no pages for {source}")

        page_pdfs: list[Path] = []
        for index, image in enumerate(images, start=1):
            page_pdf = temporary / f"normalized-{index:04d}.pdf"
            # Pillow replaces macOS-only `sips`, so the kit also runs on Linux.
            with Image.open(image) as picture:
                picture.convert("RGB").save(page_pdf, "PDF", resolution=float(dpi))
            page_pdfs.append(page_pdf)

        staged = temporary / destination.name
        run_checked((merge_tool, *page_pdfs, staged), quiet=True)
        atomic_replace(staged, destination)


def pdf_page_count(
    path: Path,
    *,
    pdfinfo: str | Path | None = None,
) -> int:
    """Return a PDF page count using Poppler's pdfinfo."""

    executable = resolve_executable("pdfinfo", explicit=pdfinfo)
    result = run_checked((executable, path), quiet=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise BuildError(f"pdfinfo did not report a page count for {path}")


def merge_pdfs_structured(
    inputs: Sequence[tuple[str | None, Path]],
    output: Path,
    *,
    linearize: bool = True,
) -> int:
    """Merge PDFs with optional outline labels while preserving text layers."""

    if not inputs:
        raise BuildError("cannot merge an empty PDF list")
    missing = [str(path) for _, path in inputs if not path.is_file()]
    if missing:
        raise BuildError(f"cannot merge missing PDFs: {', '.join(missing)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{output.stem}-", dir=output.parent
    ) as temporary_directory:
        staged = Path(temporary_directory) / output.name
        destination = pikepdf.Pdf.new()
        outlines: list[tuple[str, int]] = []
        page_index = 0
        for label, path in inputs:
            try:
                source = pikepdf.Pdf.open(path)
            except (pikepdf.PdfError, pikepdf.PasswordError) as error:
                destination.close()
                raise BuildError(f"pikepdf cannot open {path}: {error}") from error
            with source:
                if label:
                    outlines.append((label, page_index))
                destination_start = len(destination.pages)
                try:
                    destination.add_pages_from(source, forms="strip")
                except ValueError as error:
                    if "Name must be at least one character long" not in str(error):
                        raise
                    while len(destination.pages) > destination_start:
                        del destination.pages[-1]
                    # Some browser-generated PDFs contain invalid empty named
                    # destinations. Preserve page content and searchable text,
                    # but deliberately drop those broken internal destinations.
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", pikepdf.PageCopyWarning)
                        destination.pages.extend(source.pages)
                page_index += len(source.pages)

        if outlines:
            with destination.open_outline() as outline:
                outline.root.extend(
                    pikepdf.OutlineItem(label, page)
                    for label, page in outlines
                )
        destination.save(
            staged,
            linearize=linearize,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
            deterministic_id=True,
        )
        destination.close()
        validate_pdf(staged, expected_pages=page_index)
        atomic_replace(staged, output)
    return page_index
