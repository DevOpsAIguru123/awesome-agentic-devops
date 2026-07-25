#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

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


def _validate_entry(entry: dict[str, Any], index: int) -> None:
    name = _entry_name(entry, index)
    _require_fields(entry, name)
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
    for field in ("labels", "use_cases"):
        if not isinstance(entry[field], list):
            raise ValidationError(f"{name}: {field} must be a list")


def validate_entries(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        raise ValidationError("data/repos.yaml must contain a list of repo entries")

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValidationError(f"entry #{index + 1} must be a mapping")
        _validate_entry(entry, index)

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
