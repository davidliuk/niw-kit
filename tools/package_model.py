#!/usr/bin/env python3
"""Immutable models and validation for the package control files."""

from __future__ import annotations

import json
import posixpath
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Iterable


ARTIFACT_CLASSES = frozenset(
    {"FILING_FACING", "PRIVATE_CONTROL", "MACHINE_DATA"}
)
CLEAN_COPY_RULESETS = frozenset({"FILING_V2", "PRIVATE_V2", "DATA_V2"})
SERIES_ID_PATTERN = re.compile(r"^[A-Z]$")
EXHIBIT_ID_PATTERN = re.compile(r"^(?P<series>[A-Z])-(?P<number>[1-9]\d*)$")


class ModelValidationError(ValueError):
    """Raised with all structural and path errors found in a control file."""

    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(errors)
        if not self.errors:
            raise ValueError("ModelValidationError requires at least one error")
        super().__init__("\n".join(self.errors))


@dataclass(frozen=True, slots=True)
class Artifact:
    path: str
    display_title: str
    artifact_class: str
    include_in_review_packet: bool
    clean_copy_ruleset: str
    packet_order: int | None


@dataclass(frozen=True, slots=True)
class PackageManifest:
    schema_version: int
    artifacts: tuple[Artifact, ...]


@dataclass(frozen=True, slots=True)
class Exhibit:
    id: str
    title: str
    order: int
    file_path: str
    source: str
    date_display: str
    public_url: str | None = None
    retrieval_date: str | None = None
    supports: str | None = None


@dataclass(frozen=True, slots=True)
class ExhibitSeries:
    id: str
    title: str
    order: int
    exhibits: tuple[Exhibit, ...]


@dataclass(frozen=True, slots=True)
class ExhibitRegistry:
    schema_version: int
    series: tuple[ExhibitSeries, ...]


def _load_json(path: str | Path, label: str) -> Any:
    control_path = Path(path)
    try:
        return json.loads(control_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ModelValidationError(
            (f"{label}: cannot read {control_path}: {error.strerror or error}",)
        ) from error
    except json.JSONDecodeError as error:
        raise ModelValidationError(
            (f"{label}: invalid JSON at line {error.lineno}, column {error.colno}",)
        ) from error


def _is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _required_string(
    record: dict[str, Any], field: str, context: str, errors: list[str]
) -> str | None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: {field} must be a non-empty string")
        return None
    return value


def _positive_integer(
    record: dict[str, Any], field: str, context: str, errors: list[str]
) -> int | None:
    value = record.get(field)
    if not _is_integer(value) or value <= 0:
        errors.append(f"{context}: {field} must be a positive integer")
        return None
    return value


def _optional_string(
    record: dict[str, Any], field: str, context: str, errors: list[str]
) -> str | None:
    value = record.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: {field} must be null or a non-empty string")
        return None
    return value


def _repository_path(
    value: object,
    field: str,
    context: str,
    root: Path,
    errors: list[str],
    *,
    reject_private: bool,
) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: {field} must be a non-empty repository-relative path")
        return None

    if "\\" in value:
        if PureWindowsPath(value).drive or PureWindowsPath(value).is_absolute():
            errors.append(f"{context}: {field} must not be an absolute path: {value}")
        else:
            errors.append(f"{context}: {field} must use repository '/' separators: {value}")
        return None
    if PurePosixPath(value).is_absolute() or PureWindowsPath(value).drive:
        errors.append(f"{context}: {field} must not be an absolute path: {value}")
        return None

    raw_parts = value.split("/")
    if ".." in raw_parts:
        errors.append(f"{context}: {field} contains path traversal: {value}")
        return None

    normalized = posixpath.normpath(value)
    if normalized in {"", "."}:
        errors.append(f"{context}: {field} must identify a file")
        return None
    normalized_parts = PurePosixPath(normalized).parts
    if reject_private and normalized_parts[0].casefold() == "private":
        errors.append(f"{context}: {field} exposes a private path: {normalized}")

    root_resolved = root.resolve()
    candidate = (root_resolved / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        errors.append(f"{context}: {field} escapes the repository root: {value}")
        return None
    return normalized


def _root_object(payload: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        errors.append(f"{label}: root must be a JSON object")
        return {}
    return payload


def _schema_version(payload: dict[str, Any], label: str, errors: list[str]) -> int:
    version = payload.get("schema_version")
    if version != 1 or not _is_integer(version):
        errors.append(f"{label}: schema_version must be integer 1")
        return 1
    return version


def load_package_manifest(
    path: str | Path, root: str | Path, require_files: bool = True
) -> PackageManifest:
    """Load a validated package manifest with immutable artifact records."""

    errors: list[str] = []
    payload = _root_object(
        _load_json(path, "package manifest"), "package manifest", errors
    )
    schema_version = _schema_version(payload, "package manifest", errors)
    raw_artifacts = payload.get("artifacts")
    if not isinstance(raw_artifacts, list):
        errors.append("package manifest: artifacts must be an array")
        raw_artifacts = []

    repository_root = Path(root)
    artifacts: list[Artifact] = []
    paths: dict[str, int] = {}
    packet_orders: dict[int, int] = {}

    for index, raw_artifact in enumerate(raw_artifacts):
        context = f"package manifest artifact[{index}]"
        if not isinstance(raw_artifact, dict):
            errors.append(f"{context}: must be an object")
            continue

        artifact_class = _required_string(
            raw_artifact, "artifact_class", context, errors
        )
        reject_private = artifact_class == "FILING_FACING"
        artifact_path = _repository_path(
            raw_artifact.get("path"),
            "path",
            context,
            repository_root,
            errors,
            reject_private=reject_private,
        )
        display_title = _required_string(
            raw_artifact, "display_title", context, errors
        )
        clean_copy_ruleset = _required_string(
            raw_artifact, "clean_copy_ruleset", context, errors
        )
        included = raw_artifact.get("include_in_review_packet")
        if not isinstance(included, bool):
            errors.append(f"{context}: include_in_review_packet must be a boolean")
            included = False

        if artifact_class is not None and artifact_class not in ARTIFACT_CLASSES:
            errors.append(
                f"{context}: artifact_class must be one of {sorted(ARTIFACT_CLASSES)}"
            )
        if (
            clean_copy_ruleset is not None
            and clean_copy_ruleset not in CLEAN_COPY_RULESETS
        ):
            errors.append(
                f"{context}: clean_copy_ruleset must be one of "
                f"{sorted(CLEAN_COPY_RULESETS)}"
            )

        packet_order = raw_artifact.get("packet_order")
        if included:
            if not _is_integer(packet_order) or packet_order <= 0:
                errors.append(
                    f"{context}: included artifact packet_order must be a positive integer"
                )
                packet_order = None
            if artifact_class != "FILING_FACING":
                errors.append(
                    f"{context}: private or machine artifacts cannot be included in the review packet"
                )
        elif packet_order is not None:
            errors.append(f"{context}: excluded artifact packet_order must be null")
            packet_order = None

        if artifact_path is not None:
            if artifact_path in paths:
                errors.append(
                    f"{context}: duplicate path {artifact_path!r}; first used by "
                    f"artifact[{paths[artifact_path]}]"
                )
            else:
                paths[artifact_path] = index
            if require_files and not (repository_root / artifact_path).is_file():
                errors.append(f"{context}: missing file {artifact_path}")
        if packet_order is not None:
            if packet_order in packet_orders:
                errors.append(
                    f"{context}: duplicate packet_order {packet_order}; first used by "
                    f"artifact[{packet_orders[packet_order]}]"
                )
            else:
                packet_orders[packet_order] = index

        if all(
            value is not None
            for value in (
                artifact_path,
                display_title,
                artifact_class,
                clean_copy_ruleset,
            )
        ):
            artifacts.append(
                Artifact(
                    path=artifact_path,
                    display_title=display_title,
                    artifact_class=artifact_class,
                    include_in_review_packet=included,
                    clean_copy_ruleset=clean_copy_ruleset,
                    packet_order=packet_order,
                )
            )

    if errors:
        raise ModelValidationError(errors)
    return PackageManifest(schema_version=schema_version, artifacts=tuple(artifacts))


def load_exhibit_registry(
    path: str | Path, root: str | Path, require_files: bool = True
) -> ExhibitRegistry:
    """Load a validated exhibit hierarchy with immutable ordered records."""

    errors: list[str] = []
    payload = _root_object(
        _load_json(path, "exhibit registry"), "exhibit registry", errors
    )
    schema_version = _schema_version(payload, "exhibit registry", errors)
    raw_series = payload.get("series")
    if not isinstance(raw_series, list):
        errors.append("exhibit registry: series must be an array")
        raw_series = []
    elif not raw_series:
        errors.append("exhibit registry: series must not be empty")

    repository_root = Path(root)
    series_records: list[ExhibitSeries] = []
    series_ids: dict[str, int] = {}
    series_orders: dict[int, int] = {}
    exhibit_ids: dict[str, str] = {}
    file_paths: dict[str, str] = {}

    for series_index, raw_parent in enumerate(raw_series):
        context = f"exhibit registry series[{series_index}]"
        if not isinstance(raw_parent, dict):
            errors.append(f"{context}: must be an object")
            continue

        series_id = _required_string(raw_parent, "id", context, errors)
        series_title = _required_string(raw_parent, "title", context, errors)
        series_order = _positive_integer(raw_parent, "order", context, errors)
        if series_id is not None and not SERIES_ID_PATTERN.fullmatch(series_id):
            errors.append(f"{context}: id must be one uppercase letter")
        if any(
            field in raw_parent
            for field in (
                "file_path",
                "source",
                "date_display",
                "public_url",
                "retrieval_date",
                "supports",
            )
        ):
            errors.append(f"{context}: parent series must not carry exhibit payload fields")

        if series_id is not None:
            if series_id in series_ids:
                errors.append(
                    f"{context}: duplicate series id {series_id}; first used by "
                    f"series[{series_ids[series_id]}]"
                )
            else:
                series_ids[series_id] = series_index
        if series_order is not None:
            if series_order in series_orders:
                errors.append(
                    f"{context}: duplicate series order {series_order}; first used by "
                    f"series[{series_orders[series_order]}]"
                )
            else:
                series_orders[series_order] = series_index

        raw_exhibits = raw_parent.get("exhibits")
        if not isinstance(raw_exhibits, list):
            errors.append(f"{context}: exhibits must be an array")
            raw_exhibits = []
        elif not raw_exhibits:
            errors.append(f"{context}: exhibits must not be empty")

        exhibits: list[Exhibit] = []
        exhibit_orders: dict[int, int] = {}
        for exhibit_index, raw_exhibit in enumerate(raw_exhibits):
            child_context = f"{context} exhibit[{exhibit_index}]"
            if not isinstance(raw_exhibit, dict):
                errors.append(f"{child_context}: must be an object")
                continue

            exhibit_id = _required_string(raw_exhibit, "id", child_context, errors)
            title = _required_string(raw_exhibit, "title", child_context, errors)
            order = _positive_integer(raw_exhibit, "order", child_context, errors)
            file_path = _repository_path(
                raw_exhibit.get("file_path"),
                "file_path",
                child_context,
                repository_root,
                errors,
                reject_private=True,
            )
            source = _required_string(raw_exhibit, "source", child_context, errors)
            date_display = _required_string(
                raw_exhibit, "date_display", child_context, errors
            )
            public_url = _optional_string(
                raw_exhibit, "public_url", child_context, errors
            )
            retrieval_date = _optional_string(
                raw_exhibit, "retrieval_date", child_context, errors
            )
            supports = _optional_string(
                raw_exhibit, "supports", child_context, errors
            )

            id_match = (
                EXHIBIT_ID_PATTERN.fullmatch(exhibit_id)
                if exhibit_id is not None
                else None
            )
            if exhibit_id is not None and id_match is None:
                errors.append(
                    f"{child_context}: id must use <series>-<positive integer> form"
                )
            elif id_match is not None and id_match.group("series") != series_id:
                errors.append(
                    f"{child_context}: id {exhibit_id} has the wrong series prefix; "
                    f"expected {series_id}-"
                )

            if exhibit_id is not None:
                if exhibit_id in exhibit_ids:
                    errors.append(
                        f"{child_context}: duplicate exhibit id {exhibit_id}; first used by "
                        f"{exhibit_ids[exhibit_id]}"
                    )
                else:
                    exhibit_ids[exhibit_id] = child_context
            if order is not None:
                if order in exhibit_orders:
                    errors.append(
                        f"{child_context}: duplicate exhibit order {order}; first used by "
                        f"exhibit[{exhibit_orders[order]}]"
                    )
                else:
                    exhibit_orders[order] = exhibit_index
            if file_path is not None:
                if file_path in file_paths:
                    errors.append(
                        f"{child_context}: duplicate file_path {file_path!r}; first used by "
                        f"{file_paths[file_path]}"
                    )
                else:
                    file_paths[file_path] = child_context
                if require_files and not (repository_root / file_path).is_file():
                    errors.append(f"{child_context}: missing file {file_path}")

            if all(
                value is not None
                for value in (exhibit_id, title, order, file_path, source, date_display)
            ):
                exhibits.append(
                    Exhibit(
                        id=exhibit_id,
                        title=title,
                        order=order,
                        file_path=file_path,
                        source=source,
                        date_display=date_display,
                        public_url=public_url,
                        retrieval_date=retrieval_date,
                        supports=supports,
                    )
                )

        if all(
            value is not None for value in (series_id, series_title, series_order)
        ):
            series_records.append(
                ExhibitSeries(
                    id=series_id,
                    title=series_title,
                    order=series_order,
                    exhibits=tuple(sorted(exhibits, key=lambda exhibit: exhibit.order)),
                )
            )

    if errors:
        raise ModelValidationError(errors)
    return ExhibitRegistry(
        schema_version=schema_version,
        series=tuple(sorted(series_records, key=lambda parent: parent.order)),
    )


def select_review_artifacts(manifest: PackageManifest) -> tuple[Artifact, ...]:
    """Return included filing artifacts in their explicit packet order."""

    return tuple(
        sorted(
            (
                artifact
                for artifact in manifest.artifacts
                if artifact.include_in_review_packet
            ),
            key=lambda artifact: artifact.packet_order,
        )
    )
