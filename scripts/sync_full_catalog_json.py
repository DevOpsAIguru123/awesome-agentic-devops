#!/usr/bin/env python3
"""Generate data/catalog.full.json from data/repos.yaml.

Unlike data/catalog.json, which intentionally contains only installable skill
sources for the bootstrap installer, this file exposes the full safety-scored
catalog in a stable machine-readable shape for search UIs, MCP servers,
dashboards, and downstream audits.

Run with no arguments to rewrite data/catalog.full.json, or with --check to
fail if the generated file is stale.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPOS_YAML = ROOT / "data" / "repos.yaml"
FULL_CATALOG_JSON = ROOT / "data" / "catalog.full.json"

SAFETY_FIELDS = (
    "action_level",
    "human_approval",
    "evidence_tracing",
    "maturity",
    "risk_notes",
)
PUBLIC_FIELDS = (
    "name",
    "url",
    "category",
    "type",
    "framework",
    "primary_language",
    "cloud_provider",
    "use_cases",
    "operator_note",
    "labels",
)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _github_slug(url: str) -> str | None:
    marker = "github.com/"
    if marker not in url:
        return None
    slug = url.split(marker, 1)[1].strip("/")
    parts = slug.split("/")
    if len(parts) < 2:
        return None
    return "/".join(parts[:2])


def build_full_catalog() -> dict[str, Any]:
    entries = yaml.safe_load(REPOS_YAML.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise SystemExit(f"{REPOS_YAML} must contain a list of entries")

    projected: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit(f"{REPOS_YAML} contains a non-mapping entry")
        item = {field: entry.get(field) for field in PUBLIC_FIELDS}
        item["use_cases"] = _as_list(item.get("use_cases"))
        item["labels"] = _as_list(item.get("labels"))
        item["safety"] = {field: entry.get(field) for field in SAFETY_FIELDS}
        github_slug = _github_slug(str(entry.get("url", "")))
        if github_slug:
            item["github_slug"] = github_slug
        projected.append(item)

    projected.sort(key=lambda item: (str(item.get("category", "")), str(item.get("name", ""))))
    return {
        "schema_version": 1,
        "source": "data/repos.yaml",
        "generated_by": "scripts/sync_full_catalog_json.py",
        "entry_count": len(projected),
        "entries": projected,
    }


def render(catalog: dict[str, Any]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if data/catalog.full.json is stale instead of rewriting it",
    )
    args = parser.parse_args()

    expected = render(build_full_catalog())
    current = FULL_CATALOG_JSON.read_text(encoding="utf-8") if FULL_CATALOG_JSON.exists() else None

    if current == expected:
        print(f"data/catalog.full.json is in sync: {json.loads(expected)['entry_count']} entries")
        return 0
    if args.check:
        state = "missing" if current is None else "stale"
        print(
            f"data/catalog.full.json is {state}.\n"
            f"Run: python scripts/sync_full_catalog_json.py"
        )
        return 1
    FULL_CATALOG_JSON.write_text(expected, encoding="utf-8")
    print(f"data/catalog.full.json updated: {json.loads(expected)['entry_count']} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
