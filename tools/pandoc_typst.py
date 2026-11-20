#!/usr/bin/env python3
"""Deterministic Markdown-to-PDF rendering through Pandoc and Typst."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_support import (
    BuildError,
    atomic_replace,
    pdf_page_count,
    resolve_executable,
    run_checked,
    validate_pdf,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = Path("templates/legal-metadata.yaml")
DEFAULT_STYLE = Path("templates/legal-document.typ")
DEFAULT_NOTICE = Path("templates/draft-notice.typ")
DEFAULT_FILTER = Path("tools/pandoc/pagebreaks.lua")


def _from_root(root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def render_markdown_pdf(
    *,
    root: Path,
    source: Path,
    destination: Path,
    draft_notice: bool = True,
    metadata: Path | None = None,
    style: Path | None = None,
    notice: Path | None = None,
    pagebreak_filter: Path | None = None,
    pandoc: str | Path | None = None,
    typst: str | Path | None = None,
    keep_typst: Path | None = None,
) -> int:
    """Render Markdown to PDF and return the generated page count."""

    if not source.is_file():
        raise BuildError(f"missing Markdown source: {source}")
    pandoc_path = resolve_executable("pandoc", explicit=pandoc)
    typst_path = resolve_executable("typst", explicit=typst)
    metadata = metadata or root / DEFAULT_METADATA
    style = style or root / DEFAULT_STYLE
    notice = notice or root / DEFAULT_NOTICE
    pagebreak_filter = pagebreak_filter or root / DEFAULT_FILTER
    required = (metadata, style, pagebreak_filter)
    if draft_notice:
        required += (notice,)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise BuildError(f"missing Pandoc/Typst build controls: {', '.join(missing)}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    build_root = root / ".tmp" / "build"
    build_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{destination.stem}-", dir=build_root
    ) as temporary_directory:
        temporary = Path(temporary_directory)
        typst_source = temporary / f"{destination.stem}.typ"
        staged_pdf = temporary / destination.name
        command: list[str | Path] = [
            pandoc_path,
            source,
            "--from=markdown+smart",
            "--to=typst",
            "--standalone",
            "--metadata-file",
            metadata,
            "--lua-filter",
            pagebreak_filter,
            "--include-before-body",
            style,
        ]
        if draft_notice:
            command.extend(("--include-before-body", notice))
        command.extend(("--output", typst_source))
        run_checked(command, cwd=root, quiet=True)
        run_checked(
            (
                typst_path,
                "compile",
                "--root",
                root,
                typst_source,
                staged_pdf,
            ),
            cwd=root,
            quiet=True,
            environment={"SOURCE_DATE_EPOCH": "0"},
        )
        if keep_typst is not None:
            keep_typst.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                prefix=f".{keep_typst.name}.",
                suffix=".tmp",
                dir=keep_typst.parent,
                delete=False,
            ) as handle:
                staged_typst = Path(handle.name)
            shutil.copy2(typst_source, staged_typst)
            atomic_replace(staged_typst, keep_typst)
        pages = validate_pdf(staged_pdf, require_letter=True)
        atomic_replace(staged_pdf, destination)

    return pages


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Markdown to PDF through Pandoc and Typst."
    )
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--filing-clean", action="store_true")
    parser.add_argument("--keep-typst")
    parser.add_argument("--metadata")
    parser.add_argument("--style")
    parser.add_argument("--notice")
    parser.add_argument("--pagebreak-filter")
    parser.add_argument("--pandoc")
    parser.add_argument("--typst")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _argument_parser().parse_args(argv)
    root = Path(args.root).resolve()
    try:
        pages = render_markdown_pdf(
            root=root,
            source=_from_root(root, args.source),
            destination=_from_root(root, args.destination),
            draft_notice=not args.filing_clean,
            metadata=(
                _from_root(root, args.metadata) if args.metadata else None
            ),
            style=_from_root(root, args.style) if args.style else None,
            notice=_from_root(root, args.notice) if args.notice else None,
            pagebreak_filter=(
                _from_root(root, args.pagebreak_filter)
                if args.pagebreak_filter
                else None
            ),
            pandoc=args.pandoc,
            typst=args.typst,
            keep_typst=(
                _from_root(root, args.keep_typst) if args.keep_typst else None
            ),
        )
    except (BuildError, OSError, UnicodeError, ValueError) as error:
        print(f"cannot render Markdown PDF: {error}", file=sys.stderr)
        return 1
    print(f"Wrote {_from_root(root, args.destination)} ({pages} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
