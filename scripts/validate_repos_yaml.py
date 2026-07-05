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


def validate_entries(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        raise ValidationError("data/repos.yaml must contain a list of repo entries")

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValidationError(f"entry #{index + 1} must be a mapping")

        name = _entry_name(entry, index)
        for field in REQUIRED_FIELDS:
            if field not in entry:
                raise ValidationError(f"{name}: missing required field: {field}")

        if entry["action_level"] not in ALLOWED_ACTION_LEVELS:
            allowed = ", ".join(sorted(ALLOWED_ACTION_LEVELS))
            raise ValidationError(
                f"{name}: invalid action_level {entry['action_level']!r}; "
                f"expected one of: {allowed}"
            )

        if entry["maturity"] not in ALLOWED_MATURITY:
            allowed = ", ".join(sorted(ALLOWED_MATURITY))
            raise ValidationError(
                f"{name}: invalid maturity {entry['maturity']!r}; "
                f"expected one of: {allowed}"
            )

        if entry["evidence_tracing"] not in ALLOWED_EVIDENCE_TRACING:
            allowed = ", ".join(sorted(ALLOWED_EVIDENCE_TRACING))
            raise ValidationError(
                f"{name}: invalid evidence_tracing {entry['evidence_tracing']!r}; "
                f"expected one of: {allowed}"
            )

        if entry["human_approval"] not in ALLOWED_HUMAN_APPROVAL:
            raise ValidationError(
                f"{name}: human_approval must be true, false, or unknown"
            )

        if not isinstance(entry["labels"], list):
            raise ValidationError(f"{name}: labels must be a list")

        if not isinstance(entry["use_cases"], list):
            raise ValidationError(f"{name}: use_cases must be a list")

    return entries


def validate_file(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return validate_entries(data)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/repos.yaml")
    try:
        entries = validate_file(path)
    except (OSError, yaml.YAMLError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Validation passed: {len(entries)} repo entries in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
