#!/usr/bin/env python3
"""Resolve exhibit citations and render registry-backed Markdown controls."""

from __future__ import annotations

import re
from collections.abc import Mapping

from tools.package_model import (
    Exhibit,
    ExhibitRegistry,
    ExhibitSeries,
    ModelValidationError,
)


_CITATION_START_PATTERN = re.compile(r"\[exhibits?", re.IGNORECASE)
_CITATION_LABEL_PATTERN = re.compile(
    r"(?P<label>exhibits?)\b(?P<body>.*)", re.IGNORECASE | re.DOTALL
)
_EXHIBIT_ID_PATTERN = re.compile(r"(?P<series>[A-Z])-(?P<number>[1-9]\d*)")
_PARENT_ID_PATTERN = re.compile(r"[A-Z]")
_RANGE_PATTERN = re.compile(
    r"(?P<first_series>[A-Z])-(?P<first_number>[1-9]\d*)"
    r"\s*(?:\u2013|\u2014|-)\s*"
    r"(?P<last_series>[A-Z])-(?P<last_number>[1-9]\d*)"
)
STABLE_EXHIBIT_ID_NOTE = (
    "Exhibit identifiers are stable controlled labels. Unused numbers or "
    "series are intentionally omitted and do not indicate missing uploads; "
    "the tables below list the complete filing exhibit set."
)


def _ordered_series(registry: ExhibitRegistry) -> tuple[ExhibitSeries, ...]:
    return tuple(sorted(registry.series, key=lambda item: item.order))


def _ordered_exhibits(series: ExhibitSeries) -> tuple[Exhibit, ...]:
    return tuple(sorted(series.exhibits, key=lambda item: item.order))


def _registry_lookups(
    registry: ExhibitRegistry,
) -> tuple[dict[str, ExhibitSeries], dict[str, Exhibit]]:
    parents: dict[str, ExhibitSeries] = {}
    children: dict[str, Exhibit] = {}
    for parent in _ordered_series(registry):
        parents[parent.id] = parent
        for child in _ordered_exhibits(parent):
            children[child.id] = child
    return parents, children


def _citation_context(citation: str, offset: int) -> str:
    return f"citation {citation!r} at offset {offset}"


def _scan_citations(text: str) -> tuple[tuple[tuple[str, int], ...], tuple[str, ...]]:
    """Return complete bracketed exhibit citations and safe scanner errors."""

    citations: list[tuple[str, int]] = []
    errors: list[str] = []
    cursor = 0
    while True:
        match = _CITATION_START_PATTERN.search(text, cursor)
        if match is None:
            break

        start = match.start()
        depth = 0
        end = start
        while end < len(text):
            character = text[end]
            if character == "[":
                depth += 1
            elif character == "]":
                depth -= 1
                if depth == 0:
                    end += 1
                    break
            end += 1

        if depth != 0:
            errors.append(f"unclosed exhibit citation at offset {start}")
            next_match = _CITATION_START_PATTERN.search(text, match.end())
            if next_match is None:
                break
            cursor = next_match.start()
            continue

        citations.append((text[start:end], start))
        cursor = end

    return tuple(citations), tuple(errors)


def _parse_exhibit_references(
    text: str, registry: ExhibitRegistry
) -> tuple[tuple[Exhibit, ...], tuple[str, ...]]:
    """Parse references while retaining valid usages beside other defects."""

    parents, children = _registry_lookups(registry)
    references: list[Exhibit] = []
    citations, scanner_errors = _scan_citations(text)
    errors = list(scanner_errors)

    for citation, offset in citations:
        context = _citation_context(citation, offset)
        inner = citation[1:-1]
        label_match = _CITATION_LABEL_PATTERN.fullmatch(inner)
        if label_match is None:
            errors.append(f"{context}: malformed exhibit citation")
            continue

        label = label_match.group("label")
        body_with_spacing = label_match.group("body")
        if label not in {"Exhibit", "Exhibits"}:
            errors.append(
                f"{context}: malformed exhibit citation label; "
                "use 'Exhibit' or 'Exhibits'"
            )
            continue
        if not body_with_spacing or not body_with_spacing[0].isspace():
            errors.append(f"{context}: malformed exhibit citation; missing reference")
            continue

        body = body_with_spacing.strip()
        if body.endswith("."):
            body = body[:-1].rstrip()
        if not body:
            errors.append(f"{context}: malformed exhibit citation; missing reference")
            continue

        for raw_item in re.split(r"[,;]", body):
            item = raw_item.strip()
            if not item:
                errors.append(
                    f"{context}: malformed exhibit reference item {item!r}"
                )
                continue

            if "__" in item or "[" in item or "]" in item:
                errors.append(
                    f"{context}: placeholder exhibit reference {item!r} is not allowed"
                )
                continue

            range_match = _RANGE_PATTERN.fullmatch(item)
            if range_match is not None:
                first_series = range_match.group("first_series")
                last_series = range_match.group("last_series")
                first_number = int(range_match.group("first_number"))
                last_number = int(range_match.group("last_number"))
                if first_series != last_series:
                    errors.append(
                        f"{context}: cross-series range {item} is not allowed"
                    )
                    continue
                if last_number < first_number:
                    errors.append(f"{context}: backward range {item} is not allowed")
                    continue

                expanded_ids = tuple(
                    f"{first_series}-{number}"
                    for number in range(first_number, last_number + 1)
                )
                missing_ids = tuple(
                    exhibit_id
                    for exhibit_id in expanded_ids
                    if exhibit_id not in children
                )
                if missing_ids:
                    errors.extend(
                        f"{context}: range {item} includes undefined exhibit {exhibit_id}"
                        for exhibit_id in missing_ids
                    )
                    continue
                references.extend(children[exhibit_id] for exhibit_id in expanded_ids)
                continue

            id_match = _EXHIBIT_ID_PATTERN.fullmatch(item)
            if id_match is not None:
                child = children.get(item)
                if child is None:
                    errors.append(f"{context}: undefined exhibit {item}")
                else:
                    references.append(child)
                continue

            if _PARENT_ID_PATTERN.fullmatch(item):
                if item in parents:
                    errors.append(
                        f"{context}: parent-only reference {item} is not allowed; "
                        "cite a child exhibit"
                    )
                else:
                    errors.append(
                        f"{context}: parent-only reference {item} is not allowed; "
                        "no such exhibit series is registered"
                    )
                continue

            errors.append(f"{context}: malformed exhibit reference item {item!r}")

    return tuple(references), tuple(errors)


def extract_exhibit_references(
    text: str, registry: ExhibitRegistry
) -> tuple[Exhibit, ...]:
    """Resolve bracketed child references in encounter and range-expansion order.

    Every malformed or undefined reference in ``text`` is reported together as a
    ``ModelValidationError``. Error context contains only the citation and its
    character offset, never surrounding narrative text.
    """

    references, errors = _parse_exhibit_references(text, registry)
    if errors:
        raise ModelValidationError(errors)
    return references


def check_exhibit_usage(
    texts: Mapping[str, str], registry: ExhibitRegistry
) -> tuple[str, ...]:
    """Return source-labeled citation defects and uncited registered children."""

    errors: list[str] = []
    cited_ids: set[str] = set()
    for source in sorted(texts):
        references, source_errors = _parse_exhibit_references(texts[source], registry)
        cited_ids.update(reference.id for reference in references)
        errors.extend(f"{source}: {error}" for error in source_errors)

    for parent in _ordered_series(registry):
        for child in _ordered_exhibits(parent):
            if child.id not in cited_ids:
                errors.append(f"uncited exhibit {child.id}")
    return tuple(errors)


def _single_line(value: str) -> str:
    return " ".join(value.splitlines())


def _table_cell(value: str | None) -> str:
    if value is None:
        return "—"
    return _single_line(value).replace("\\", "\\\\").replace("|", "\\|")


def render_exhibit_index(registry: ExhibitRegistry) -> str:
    """Render a deterministic Markdown exhibit index from canonical metadata."""

    lines = ["# Exhibit Index", "", STABLE_EXHIBIT_ID_NOTE]
    for parent in _ordered_series(registry):
        lines.extend(
            (
                "",
                f"## Series {parent.id} — {_single_line(parent.title)}",
                "",
                "| Exhibit | Title | Source | Date | Supports |",
                "| --- | --- | --- | --- | --- |",
            )
        )
        for child in _ordered_exhibits(parent):
            lines.append(
                "| "
                + " | ".join(
                    (
                        child.id,
                        _table_cell(child.title),
                        _table_cell(child.source),
                        _table_cell(child.date_display),
                        _table_cell(child.supports),
                    )
                )
                + " |"
            )
    return "\n".join(lines) + "\n"


def render_exhibit_cover(exhibit: Exhibit, series: ExhibitSeries) -> str:
    """Render one Markdown cover without exposing its repository payload path."""

    lines = [
        f"# Exhibit {exhibit.id}",
        "",
        f"## {_single_line(exhibit.title)}",
        "",
        f"**Series:** {series.id} — {_single_line(series.title)}",
        "",
        f"**Source:** {_single_line(exhibit.source)}",
        "",
        f"**Date:** {_single_line(exhibit.date_display)}",
    ]
    if exhibit.public_url is not None:
        lines.extend(("", f"**Public URL:** {_single_line(exhibit.public_url)}"))
    if exhibit.retrieval_date is not None:
        lines.extend(
            ("", f"**Retrieval date:** {_single_line(exhibit.retrieval_date)}")
        )
    if exhibit.supports is not None:
        lines.extend(("", f"**Supports:** {_single_line(exhibit.supports)}"))
    return "\n".join(lines) + "\n"


def render_all_exhibit_covers(registry: ExhibitRegistry) -> str:
    """Render every child cover in explicit registry order."""

    covers = [
        render_exhibit_cover(child, parent).rstrip()
        for parent in _ordered_series(registry)
        for child in _ordered_exhibits(parent)
    ]
    if not covers:
        return ""
    return "\n\n---\n\n".join(covers) + "\n"
