#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


REQUIRED_FIELDS = (
    "name",
    "url",
    "category",
    "type",
    "framework",
    "primary_language",
    "cloud_provider",
    "use_cases",
    "action_level",
    "human_approval",
    "evidence_tracing",
    "maturity",
    "risk_notes",
    "operator_note",
    "labels",
)

ALLOWED_ACTION_LEVELS = {"read-only", "proposal", "write-capable", "unknown"}
ALLOWED_MATURITY = {
    "production-adjacent",
    "active-oss",
    "prototype",
    "curated-list",
    "skill-library",
    "unknown",
}
ALLOWED_EVIDENCE_TRACING = {"none", "partial", "yes", "unknown"}
ALLOWED_HUMAN_APPROVAL = {True, False, "unknown"}
STRING_FIELDS = (
    "name",
    "url",
    "category",
    "type",
    "framework",
    "primary_language",
    "cloud_provider",
    "risk_notes",
    "operator_note",
)
LIST_FIELDS = ("labels", "use_cases")


class ValidationError(Exception):
    """Raised when data/repos.yaml does not match the expected seed schema."""


def _entry_name(entry: dict[str, Any], index: int) -> str:
    return str(entry.get("name", f"entry #{index + 1}"))


def resolve_cli_path(path: Path, root: Path | None = None) -> Path:
    """Resolve a CLI path and require it to remain inside the working tree."""
    allowed_root = (root or Path.cwd()).resolve()
    candidate = path.expanduser()
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (allowed_root / candidate).resolve()
    )
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise ValidationError(f"path escapes the working tree: {path}") from exc
    return resolved


def _require_fields(entry: dict[str, Any], name: str) -> None:
    for field in REQUIRED_FIELDS:
        if field not in entry:
            raise ValidationError(f"{name}: missing required field: {field}")


def _validate_choice(name: str, field: str, value: Any, allowed: set[Any]) -> None:
    if value not in allowed:
        expected = ", ".join(str(item) for item in sorted(allowed, key=str))
        raise ValidationError(
            f"{name}: invalid {field} {value!r}; expected one of: {expected}"
        )


def _validate_non_empty_string(name: str, field: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name}: {field} must be a non-empty string")


def _validate_string_list(name: str, field: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValidationError(f"{name}: {field} must be a list")
    if not value:
        raise ValidationError(f"{name}: {field} must contain at least one item")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValidationError(f"{name}: {field} items must be non-empty strings")


def _validate_https_url(name: str, value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValidationError(f"{name}: url must be an absolute https URL")


def _validate_entry(entry: dict[str, Any], index: int) -> None:
    name = _entry_name(entry, index)
    _require_fields(entry, name)
    for field in STRING_FIELDS:
        _validate_non_empty_string(name, field, entry[field])
    for field in LIST_FIELDS:
        _validate_string_list(name, field, entry[field])
    _validate_https_url(name, entry["url"])
    _validate_choice(name, "action_level", entry["action_level"], ALLOWED_ACTION_LEVELS)
    _validate_choice(name, "maturity", entry["maturity"], ALLOWED_MATURITY)
    _validate_choice(
        name,
        "evidence_tracing",
        entry["evidence_tracing"],
        ALLOWED_EVIDENCE_TRACING,
    )
    if entry["human_approval"] not in ALLOWED_HUMAN_APPROVAL:
        raise ValidationError(f"{name}: human_approval must be true, false, or unknown")


def _validate_unique_field(entries: list[dict[str, Any]], field: str) -> None:
    seen: dict[Any, str] = {}
    for index, entry in enumerate(entries):
        value = entry[field]
        name = _entry_name(entry, index)
        if value in seen:
            raise ValidationError(
                f"{name}: duplicate {field} {value!r}; first used by {seen[value]}"
            )
        seen[value] = name


def _validate_write_label_consistency(entry: dict[str, Any], index: int) -> None:
    name = _entry_name(entry, index)
    labels = set(entry["labels"])
    is_write_capable = entry["action_level"] == "write-capable"
    has_write_label = "write" in labels

    if is_write_capable and not has_write_label:
        raise ValidationError(f"{name}: write-capable entries must include write label")
    if has_write_label and not is_write_capable:
        raise ValidationError(f"{name}: write label requires action_level write-capable")


def validate_entries(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        raise ValidationError("data/repos.yaml must contain a list of repo entries")

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValidationError(f"entry #{index + 1} must be a mapping")
        _validate_entry(entry, index)
        _validate_write_label_consistency(entry, index)

    _validate_unique_field(entries, "name")
    _validate_unique_field(entries, "url")

    return entries


def validate_file(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return validate_entries(data)


def main() -> int:
    supplied_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/repos.yaml")
    try:
        path = resolve_cli_path(supplied_path)
        entries = validate_file(path)
    except (OSError, yaml.YAMLError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Validation passed: {len(entries)} repo entries in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
