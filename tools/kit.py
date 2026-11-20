#!/usr/bin/env python3
"""One command-line entry point for an EB-2 NIW self-petition case.

    uv run python tools/kit.py new <case-id> --name "Full Name"
    uv run python tools/kit.py doctor
    uv run python tools/kit.py check   --case cases/<id> [--final]
    uv run python tools/kit.py stubs   --case cases/<id>
    uv run python tools/kit.py review  --case cases/<id>
    uv run python tools/kit.py binder  --case cases/<id>
    uv run python tools/kit.py online  --case cases/<id> [--allow-draft]
    uv run python tools/kit.py all     --case cases/<id>
    uv run python tools/kit.py freeze  --case cases/<id> --label filed-YYYY-MM-DD
    uv run python tools/kit.py verify-frozen --case cases/<id>

A case is a directory created from ``case-template/``. Every path inside
``case.json``, the package manifest, and the exhibit registry is relative to
that case directory. The checks prove document integrity (every citation
resolves, nothing is left as a placeholder, uploads fit the portal limits);
they do not prove legal sufficiency.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pikepdf

from tools.build_support import (
    BuildError,
    atomic_replace,
    merge_pdfs_structured,
    normalize_pdf_pages_to_letter,
    pdf_page_count,
    pdf_page_sizes,
    rasterize_pdf,
    resolve_executable,
    run_checked,
    validate_pdf,
)
from tools.exhibit_registry import check_exhibit_usage, render_exhibit_index
from tools.package_model import (
    ModelValidationError,
    load_exhibit_registry,
    load_package_manifest,
    select_review_artifacts,
)
from tools.pandoc_typst import render_markdown_pdf
from tools.pdf_upload import (
    BUILD_LIMIT_BYTES,
    compile_typst,
    cover_typst,
    flatten_widget_pages_for_upload,
    optimize_single_pages_for_upload,
    safe_slug,
    sha256,
    split_page_groups,
    validate_portal_filenames,
    widget_annotation_pages,
    write_page_subset,
)


KIT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = KIT_ROOT / "case-template"
THEME = {
    "metadata": KIT_ROOT / "templates/legal-metadata.yaml",
    "style": KIT_ROOT / "templates/legal-document.typ",
    "notice": KIT_ROOT / "templates/draft-notice.typ",
    "pagebreak_filter": KIT_ROOT / "tools/pandoc/pagebreaks.lua",
}
PLACEHOLDER_MARK = "NIW-KIT-PLACEHOLDER"
EXHIBIT_TABLES_MARKER = "<!-- EXHIBIT_TABLES -->"
CASE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z0-9_]+\}\}")
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
DRAFT_MARKERS = ("TODO", "TBD", "XXX", "[[", "]]", "DRAFT —")
# Identifiers that never belong in tracked drafting files. Keep them in the
# ignored private/ and source_documents/ trees.
PRIVATE_PATTERNS = {
    "Social Security number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "A-number": re.compile(r"\bA[- ]?\d{3}[- ]?\d{3}[- ]?\d{3}\b"),
    "SEVIS ID": re.compile(r"\bN\d{10}\b"),
}
IGNORED_CASE_DIRS = frozenset(
    {"evidence", "source_documents", "private", "output", "archive", ".tmp"}
)


# --------------------------------------------------------------------------
# Case profile


@dataclass(frozen=True)
class LockedPhrase:
    name: str
    text: str
    files: tuple[str, ...]


@dataclass(frozen=True)
class Case:
    root: Path
    case_id: str
    applicant_name: str
    title: str
    manifest: Path
    registry: Path
    petition: Path
    exhibit_index_source: Path
    output_dir: Path
    upload_limit_bytes: int
    locked_phrases: tuple[LockedPhrase, ...]

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()


def _case_path(root: Path, value: object, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise BuildError(f"case.json {label} must be a non-empty path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise BuildError(f"case.json {label} must stay inside the case directory")
    return root / Path(*path.parts)


def load_case(case_dir: Path) -> Case:
    root = case_dir.resolve()
    config = root / "case.json"
    try:
        payload = json.loads(config.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise BuildError(f"missing {config}; create a case with `kit.py new`") from error
    except (OSError, json.JSONDecodeError) as error:
        raise BuildError(f"cannot read {config}: {error}") from error
    if payload.get("schema_version") != 1:
        raise BuildError("case.json schema_version must be 1")
    limit = payload.get("upload_limit_bytes", BUILD_LIMIT_BYTES)
    if not isinstance(limit, int) or not 1_000_000 <= limit <= BUILD_LIMIT_BYTES:
        raise BuildError(
            f"case.json upload_limit_bytes must be between 1000000 and {BUILD_LIMIT_BYTES}"
        )
    phrases = []
    for index, raw in enumerate(payload.get("locked_phrases", [])):
        if not isinstance(raw, dict) or not all(
            isinstance(raw.get(key), str) for key in ("name", "text")
        ) or not isinstance(raw.get("files"), list):
            raise BuildError(f"case.json locked_phrases[{index}] needs name, text, files")
        for item in raw["files"]:
            _case_path(root, item, f"locked_phrases[{index}].files")
        phrases.append(LockedPhrase(raw["name"], raw["text"], tuple(raw["files"])))
    applicant = payload.get("applicant_name", "")
    return Case(
        root=root,
        case_id=str(payload.get("case_id", root.name)),
        applicant_name=str(applicant),
        title=str(payload.get("packet_title") or f"{applicant} EB-2 NIW Petition"),
        manifest=_case_path(root, payload.get("manifest"), "manifest"),
        registry=_case_path(root, payload.get("registry"), "registry"),
        petition=_case_path(root, payload.get("petition"), "petition"),
        exhibit_index_source=_case_path(
            root, payload.get("exhibit_index_source"), "exhibit_index_source"
        ),
        output_dir=_case_path(root, payload.get("output_dir", "output"), "output_dir"),
        upload_limit_bytes=limit,
        locked_phrases=tuple(phrases),
    )


# --------------------------------------------------------------------------
# Checks


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def flag(self, message: str, *, blocking: bool) -> None:
        (self.errors if blocking else self.warnings).append(message)


def _visible_text(text: str) -> str:
    """Text that reaches the PDF: drafting-guide comments are stripped."""

    return HTML_COMMENT_PATTERN.sub("", text)


def is_placeholder_pdf(path: Path) -> bool:
    try:
        with pikepdf.Pdf.open(path) as pdf:
            return str(pdf.docinfo.get("/Subject", "")) == PLACEHOLDER_MARK
    except (pikepdf.PdfError, pikepdf.PasswordError):
        return False


def _normalized(text: str) -> str:
    return " ".join(text.replace("*", "").split())


def check_case(case: Case, *, final: bool) -> Report:
    report = Report()
    try:
        manifest = load_package_manifest(case.manifest, case.root, require_files=True)
    except ModelValidationError as error:
        report.errors.extend(f"manifest: {item}" for item in error.errors)
        return report
    try:
        registry = load_exhibit_registry(case.registry, case.root, require_files=False)
    except ModelValidationError as error:
        report.errors.extend(f"registry: {item}" for item in error.errors)
        return report

    filing_texts: dict[str, str] = {}
    for artifact in manifest.artifacts:
        if artifact.artifact_class != "FILING_FACING":
            continue
        raw = (case.root / artifact.path).read_text(encoding="utf-8")
        visible = _visible_text(raw)
        filing_texts[artifact.path] = visible
        placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(visible)))
        if placeholders:
            preview = ", ".join(placeholders[:6])
            more = "" if len(placeholders) <= 6 else f" (+{len(placeholders) - 6} more)"
            report.flag(
                f"{artifact.path}: {len(placeholders)} unfilled placeholders: {preview}{more}",
                blocking=final,
            )
        for marker in DRAFT_MARKERS:
            if marker in visible:
                report.flag(f"{artifact.path}: draft marker {marker!r}", blocking=final)

    report.errors.extend(check_exhibit_usage(filing_texts, registry))

    registry_text = case.registry.read_text(encoding="utf-8")
    registry_placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(registry_text)))
    if registry_placeholders:
        report.flag(
            f"{case.rel(case.registry)}: {len(registry_placeholders)} unfilled "
            f"placeholders in exhibit metadata",
            blocking=final,
        )

    for series in registry.series:
        for exhibit in series.exhibits:
            payload = case.root / exhibit.file_path
            if not payload.is_file():
                report.flag(
                    f"exhibit {exhibit.id}: missing payload {exhibit.file_path} "
                    "(run `kit.py stubs` to preview with placeholders)",
                    blocking=final,
                )
            elif payload.suffix.casefold() == ".pdf" and is_placeholder_pdf(payload):
                report.flag(
                    f"exhibit {exhibit.id}: {exhibit.file_path} is a generated placeholder",
                    blocking=final,
                )
            elif payload.suffix.casefold() == ".md" and exhibit.id.startswith("H-") and final:
                report.warnings.append(
                    f"exhibit {exhibit.id}: payload is unsigned Markdown; file the "
                    "signed scan if the statement must be signed"
                )

    for phrase in case.locked_phrases:
        if PLACEHOLDER_PATTERN.search(phrase.text):
            report.flag(f"locked phrase {phrase.name!r} is not set in case.json", blocking=final)
            continue
        wanted = _normalized(phrase.text)
        for item in phrase.files:
            path = case.root / item
            if not path.is_file():
                report.errors.append(f"locked phrase {phrase.name!r}: missing {item}")
            elif wanted not in _normalized(path.read_text(encoding="utf-8")):
                report.errors.append(
                    f"locked phrase {phrase.name!r} drifted: exact text not found in {item}"
                )

    report.errors.extend(scan_private_identifiers(case.root))
    return report


def scan_private_identifiers(root: Path) -> list[str]:
    findings = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if (
            not path.is_file()
            or relative.parts[0] in IGNORED_CASE_DIRS
            or path.suffix.casefold() not in {".md", ".json", ".txt", ".yaml", ".yml", ".csv"}
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                findings.append(
                    f"{relative.as_posix()}: looks like a {label}; keep identifiers in private/"
                )
    return findings


def print_report(report: Report, *, final: bool) -> int:
    for warning in report.warnings:
        print(f"warning: {warning}")
    for error in report.errors:
        print(f"error: {error}", file=sys.stderr)
    level = "final" if final else "draft"
    if report.errors:
        print(f"{level} check failed: {len(report.errors)} errors, {len(report.warnings)} warnings",
              file=sys.stderr)
        return 1
    print(f"{level} check passed ({len(report.warnings)} warnings)")
    return 0


# --------------------------------------------------------------------------
# Rendering


def render(case: Case, source: Path, destination: Path, *, draft: bool) -> int:
    return render_markdown_pdf(
        root=case.root,
        source=source,
        destination=destination,
        draft_notice=draft,
        metadata=THEME["metadata"],
        style=THEME["style"],
        notice=THEME["notice"],
        pagebreak_filter=THEME["pagebreak_filter"],
    )


def exhibit_index_markdown(case: Case, registry) -> str:
    source = case.exhibit_index_source.read_text(encoding="utf-8")
    tables = render_exhibit_index(registry).split("\n", 2)[2]  # drop the H1
    if EXHIBIT_TABLES_MARKER in source:
        return source.replace(EXHIBIT_TABLES_MARKER, tables.strip())
    return source.rstrip() + "\n\n" + tables


def build_review(case: Case) -> list[Path]:
    manifest = load_package_manifest(case.manifest, case.root)
    registry = load_exhibit_registry(case.registry, case.root, require_files=False)
    out = case.output_dir / "review"
    out.mkdir(parents=True, exist_ok=True)

    index_md = out / "Exhibit_Index.md"
    index_md.write_text(exhibit_index_markdown(case, registry), encoding="utf-8")

    sections = [
        f"# {case.title}\n\nReview packet generated "
        f"{dt.date.today().isoformat()} from the tracked drafting sources.\n"
    ]
    for artifact in select_review_artifacts(manifest):
        path = case.root / artifact.path
        text = (
            index_md.read_text(encoding="utf-8")
            if path == case.exhibit_index_source
            else path.read_text(encoding="utf-8")
        )
        sections.append(text.strip())
    packet_md = out / "Review_Packet.md"
    packet_md.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")

    outputs = [out / "Petition_Letter_DRAFT.pdf", out / "Review_Packet_DRAFT.pdf"]
    render(case, case.petition, outputs[0], draft=True)
    render(case, packet_md, outputs[1], draft=True)
    return outputs


def _letter_payload(case: Case, exhibit, temporary: Path) -> tuple[Path, tuple[int, ...]]:
    payload = case.root / exhibit.file_path
    if not payload.is_file():
        raise BuildError(f"exhibit {exhibit.id}: missing payload {exhibit.file_path}")
    if payload.suffix.casefold() == ".md":
        rendered = temporary / f"{exhibit.id}-payload.pdf"
        render(case, payload, rendered, draft=False)
        payload = rendered
    widget_pages = widget_annotation_pages(payload)
    if widget_pages:
        flattened = temporary / f"{exhibit.id}-widget-safe.pdf"
        flatten_widget_pages_for_upload(
            source=payload, destination=flattened, temporary=temporary
        )
        payload = flattened
    if any(abs(w - 612.0) > 1.0 or abs(h - 792.0) > 1.0 for w, h in pdf_page_sizes(payload)):
        letter = temporary / f"{exhibit.id}-letter.pdf"
        normalize_pdf_pages_to_letter(payload, letter)
        payload = letter
    return payload, widget_pages


def _ordered(registry):
    return [
        (series, exhibit)
        for series in sorted(registry.series, key=lambda item: item.order)
        for exhibit in sorted(series.exhibits, key=lambda item: item.order)
    ]


def _cover(case: Case, series, exhibit, temporary: Path) -> Path:
    source = temporary / f"{exhibit.id}-cover.typ"
    pdf = temporary / f"{exhibit.id}-cover.pdf"
    source.write_text(cover_typst(series, exhibit), encoding="utf-8")
    compile_typst(source, pdf, root=temporary)
    return pdf


def build_binder(case: Case) -> Path:
    registry = load_exhibit_registry(case.registry, case.root, require_files=True)
    output = case.output_dir / "Exhibit_Binder.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".binder-", dir=output.parent) as tmp:
        temporary = Path(tmp)
        parts: list[tuple[str | None, Path]] = []
        for series, exhibit in _ordered(registry):
            parts.append((f"Exhibit {exhibit.id} — {exhibit.title}",
                          _cover(case, series, exhibit, temporary)))
            payload, _ = _letter_payload(case, exhibit, temporary)
            parts.append((None, payload))
        staged = temporary / output.name
        merge_pdfs_structured(parts, staged)
        atomic_replace(staged, output)
    return output


def build_online(case: Case, *, draft: bool) -> Path:
    """Petition, exhibit index, then one size-limited PDF per exhibit."""

    registry = load_exhibit_registry(case.registry, case.root, require_files=True)
    out = case.output_dir / "online"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    records = []
    limit = case.upload_limit_bytes

    def record(path: Path, role: str, **extra) -> None:
        validate_pdf(path, require_letter=True)
        size = path.stat().st_size
        if size > limit:
            raise BuildError(f"{path.name} is {size} bytes, above the {limit}-byte limit")
        records.append({
            "file": path.name, "role": role, "bytes": size,
            "pages": pdf_page_count(path), "sha256": sha256(path), **extra,
        })

    petition = out / "00_Petition_Letter.pdf"
    render(case, case.petition, petition, draft=draft)
    record(petition, "petition")

    index_md = case.output_dir / "review" / "Exhibit_Index.md"
    index_md.parent.mkdir(parents=True, exist_ok=True)
    index_md.write_text(exhibit_index_markdown(case, registry), encoding="utf-8")
    index_pdf = out / "01_Exhibit_Index.pdf"
    render(case, index_md, index_pdf, draft=draft)
    record(index_pdf, "exhibit index")

    with tempfile.TemporaryDirectory(prefix=".online-", dir=case.output_dir) as tmp:
        temporary = Path(tmp)
        for number, (series, exhibit) in enumerate(_ordered(registry), start=2):
            cover = _cover(case, series, exhibit, temporary)
            payload, widget_pages = _letter_payload(case, exhibit, temporary)
            payload, raster_pages = optimize_single_pages_for_upload(
                cover=cover, payload=payload, temporary=temporary, maximum_bytes=limit
            )
            groups = split_page_groups(
                cover=cover, payload=payload, temporary=temporary, maximum_bytes=limit
            )
            stem = f"{number:02d}_Exhibit_{exhibit.id}_{safe_slug(exhibit.title, maximum=60)}"
            for part, pages in enumerate(groups, start=1):
                name = stem if len(groups) == 1 else f"{stem}_part{part}of{len(groups)}"
                subset = temporary / f"{name}-subset.pdf"
                write_page_subset(payload, pages, subset)
                target = out / f"{name}.pdf"
                merge_pdfs_structured(((None, cover), (None, subset)), target)
                record(
                    target, "exhibit", exhibit=exhibit.id,
                    source_pages=[page + 1 for page in pages],
                    widget_pages_rasterized=list(widget_pages),
                    oversize_pages_rasterized=list(raster_pages),
                    placeholder=is_placeholder_pdf(case.root / exhibit.file_path)
                    if exhibit.file_path.endswith(".pdf") else False,
                )
    validate_portal_filenames([item["file"] for item in records])
    manifest = {
        "case_id": case.case_id,
        "draft": draft,
        "upload_limit_bytes": limit,
        "generated": dt.date.today().isoformat(),
        "files": records,
    }
    (out / "upload_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return out


# --------------------------------------------------------------------------
# Placeholders, freezing, scaffolding


STUB_TYPST = """#set page(paper: "us-letter", margin: 1in)
#set text(size: 14pt)
#v(2in)
#align(center)[
  #text(size: 30pt, weight: "bold", fill: rgb("#8a1c1c"))[PLACEHOLDER]
  #v(0.3in)
  #text(size: 20pt, weight: "bold")[Exhibit {id}]
  #v(0.2in)
  #text(size: 15pt)["{title}"]
  #v(0.5in)
  Replace `{path}` with the real evidence before filing.
]
"""


def build_stubs(case: Case) -> list[str]:
    registry = load_exhibit_registry(case.registry, case.root, require_files=False)
    created = []
    with tempfile.TemporaryDirectory(prefix=".stubs-") as tmp:
        temporary = Path(tmp)
        for _, exhibit in _ordered(registry):
            target = case.root / exhibit.file_path
            if target.exists() or target.suffix.casefold() != ".pdf":
                continue
            source = temporary / f"{exhibit.id}.typ"
            escape = lambda value: value.replace("\\", "\\\\").replace('"', '\\"')
            source.write_text(STUB_TYPST.format(
                id=exhibit.id, title=escape(exhibit.title), path=escape(exhibit.file_path)
            ), encoding="utf-8")
            staged = temporary / f"{exhibit.id}.pdf"
            compile_typst(source, staged, root=temporary)
            with pikepdf.Pdf.open(staged) as pdf:
                pdf.docinfo["/Subject"] = PLACEHOLDER_MARK
                target.parent.mkdir(parents=True, exist_ok=True)
                pdf.save(target, deterministic_id=True)
            created.append(exhibit.file_path)
    return created


def _frozen_targets(case: Case) -> list[Path]:
    registry = load_exhibit_registry(case.registry, case.root, require_files=True)
    targets = sorted((case.output_dir / "online").glob("*"))
    targets += [case.root / exhibit.file_path for _, exhibit in _ordered(registry)]
    return [path for path in targets if path.is_file()]


def freeze(case: Case, label: str) -> Path:
    files = {case.rel(path): sha256(path) for path in _frozen_targets(case)}
    if not any(name.startswith(case.rel(case.output_dir / "online")) for name in files):
        raise BuildError("build the online set (`kit.py online`) before freezing")
    record = {"label": label, "frozen": dt.date.today().isoformat(), "sha256": files}
    target = case.root / "data" / "frozen_record.json"
    target.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return target


def verify_frozen(case: Case) -> list[str]:
    target = case.root / "data" / "frozen_record.json"
    record = json.loads(target.read_text(encoding="utf-8"))
    problems = []
    for name, digest in record["sha256"].items():
        path = case.root / name
        if not path.is_file():
            problems.append(f"missing {name}")
        elif sha256(path) != digest:
            problems.append(f"changed {name}")
    return problems


def new_case(case_id: str, name: str) -> Path:
    if not CASE_ID_PATTERN.fullmatch(case_id):
        raise BuildError("case id must be lowercase letters, digits, and hyphens")
    target = KIT_ROOT / "cases" / case_id
    if target.exists():
        raise BuildError(f"{target} already exists")
    shutil.copytree(TEMPLATE_DIR, target)
    config_path = target / "case.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["case_id"] = case_id
    config["applicant_name"] = name
    config["packet_title"] = f"{name} EB-2 NIW Petition"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    for folder in ("evidence", "source_documents", "private", "output"):
        (target / folder).mkdir(exist_ok=True)
    return target


def doctor() -> int:
    missing = 0
    for tool in ("pandoc", "typst", "pdfinfo", "pdftoppm", "pdfunite"):
        try:
            path = resolve_executable(tool)
            version = path
            if tool in {"pandoc", "typst"}:
                lines = run_checked((path, "--version"), quiet=True).stdout.splitlines()
                version = lines[0] if lines else path
            print(f"ok   {tool:9} {version}")
        except BuildError:
            print(f"MISS {tool:9} install with `brew bundle` (see Brewfile)")
            missing += 1
    for module in ("pikepdf", "PIL", "pypdf"):
        ok = importlib.util.find_spec(module) is not None
        print(f"{'ok  ' if ok else 'MISS'} python:{module}")
        missing += not ok
    return 1 if missing else 0


# --------------------------------------------------------------------------
# CLI


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    created = sub.add_parser("new", help="create cases/<id> from case-template/")
    created.add_argument("case_id")
    created.add_argument("--name", required=True, help="applicant full name")
    sub.add_parser("doctor", help="check system tools and Python packages")
    for name, help_text in (
        ("check", "validate citations, placeholders, payloads, locked phrases"),
        ("stubs", "write placeholder PDFs for missing exhibit payloads"),
        ("review", "draft petition and review-packet PDFs"),
        ("binder", "one bookmarked PDF of every exhibit with covers"),
        ("online", "size-limited USCIS online upload set + manifest"),
        ("all", "check, review, binder, online"),
        ("freeze", "record SHA-256 of the filed upload set and evidence"),
        ("verify-frozen", "confirm the filed record is unchanged"),
    ):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("--case", required=True, type=Path)
        if name in {"check", "all"}:
            command.add_argument("--final", action="store_true",
                                 help="treat placeholders and stubs as errors")
        if name in {"online", "all"}:
            command.add_argument("--allow-draft", action="store_true",
                                 help="build with draft banners even if the final check fails")
        if name == "freeze":
            command.add_argument("--label", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "new":
            target = new_case(args.case_id, args.name)
            print(f"Created {target.relative_to(KIT_ROOT)}; next: kit.py check --case "
                  f"{target.relative_to(KIT_ROOT)}")
            return 0
        if args.command == "doctor":
            return doctor()
        case = load_case(args.case)
        if args.command == "check":
            return print_report(check_case(case, final=args.final), final=args.final)
        if args.command == "stubs":
            created = build_stubs(case)
            print("\n".join(f"stub {path}" for path in created) or "no stubs needed")
            return 0
        if args.command == "review":
            for path in build_review(case):
                print(f"Wrote {case.rel(path)} ({pdf_page_count(path)} pages)")
            return 0
        if args.command == "binder":
            path = build_binder(case)
            print(f"Wrote {case.rel(path)} ({pdf_page_count(path)} pages)")
            return 0
        if args.command in {"online", "all"}:
            final = getattr(args, "final", False) or not args.allow_draft
            if args.command == "all" or final:
                status = print_report(check_case(case, final=final), final=final)
                if status:
                    if final and not args.allow_draft:
                        print("Fix the errors, or pass --allow-draft for a "
                              "banner-marked preview.", file=sys.stderr)
                    return status
            if args.command == "all":
                for path in build_review(case):
                    print(f"Wrote {case.rel(path)}")
                print(f"Wrote {case.rel(build_binder(case))}")
            out = build_online(case, draft=not final)
            print(f"Wrote {case.rel(out)}/ (see upload_manifest.json)")
            return 0
        if args.command == "freeze":
            print(f"Wrote {case.rel(freeze(case, args.label))}")
            return 0
        if args.command == "verify-frozen":
            problems = verify_frozen(case)
            for problem in problems:
                print(f"error: {problem}", file=sys.stderr)
            print("frozen record intact" if not problems else "frozen record CHANGED")
            return 1 if problems else 0
    except (BuildError, ModelValidationError, OSError, ValueError) as error:
        detail = "\n".join(error.errors) if isinstance(error, ModelValidationError) else error
        print(f"error: {detail}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
