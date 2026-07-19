#!/usr/bin/env python3
"""Generate data/catalog.json, the stdlib-readable skill catalog.

The installer runs on whatever Python a user happens to have, and macOS's
/usr/bin/python3 has no PyYAML — so scripts/install_skills.py cannot parse
data/repos.yaml there. This script projects the skill entries of that catalog
into a small JSON file the installer reads with the standard library alone.

Run with no arguments to rewrite data/catalog.json, or with --check (used by
CI) to fail if it is stale.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPOS_YAML = ROOT / "data" / "repos.yaml"
CATALOG_JSON = ROOT / "data" / "catalog.json"

# Only skill categories are projected; MCP servers and the rest of the catalog
# are documentation, not installable, so they would be dead weight here.
SKILL_CATEGORIES = ("official-agent-skills", "community-agent-skills")


def build_catalog() -> dict:
    entries = yaml.safe_load(REPOS_YAML.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise SystemExit(f"{REPOS_YAML} must contain a list of entries")
    wanted = set(SKILL_CATEGORIES)
    projected = [
        {
            "name": str(entry.get("name", "")),
            "url": str(entry.get("url", "")),
            "category": str(entry.get("category", "")),
        }
        for entry in entries
        if str(entry.get("category", "")) in wanted
    ]
    # Sorted so the file is stable against reordering in the YAML.
    projected.sort(key=lambda item: (item["category"], item["name"]))
    return {
        "source": "data/repos.yaml",
        "generated_by": "scripts/sync_catalog_json.py",
        "entries": projected,
    }


def render(catalog: dict) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if data/catalog.json is stale instead of rewriting it",
    )
    args = parser.parse_args()

    expected = render(build_catalog())
    current = CATALOG_JSON.read_text(encoding="utf-8") if CATALOG_JSON.exists() else None

    if current == expected:
        count = len(json.loads(expected)["entries"])
        print(f"data/catalog.json is in sync: {count} skill sources")
        return 0
    if args.check:
        state = "missing" if current is None else "stale"
        print(
            f"data/catalog.json is {state}.\n"
            f"Run: python scripts/sync_catalog_json.py"
        )
        return 1
    CATALOG_JSON.write_text(expected, encoding="utf-8")
    count = len(json.loads(expected)["entries"])
    print(f"data/catalog.json updated: {count} skill sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
