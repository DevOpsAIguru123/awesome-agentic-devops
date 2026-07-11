#!/usr/bin/env python3
"""Keep the README intro's catalog counts in sync with data/repos.yaml.

The intro pitch states "<N> entries organized into <M> catalog sections". N is
the number of entries in data/repos.yaml; M is the number of `###` tables in the
README's Curated catalog section. Run with no arguments to rewrite the README
in place, or with --check (used by tests/CI) to fail if the numbers are stale.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
REPOS_YAML = ROOT / "data" / "repos.yaml"

COUNTS_PATTERN = re.compile(
    r"\d+ entries organized into \d+ catalog sections"
)


def expected_counts_phrase() -> str:
    entries = yaml.safe_load(REPOS_YAML.read_text())
    readme = README.read_text()
    catalog_match = re.search(
        r"^## Curated catalog\n(.*?)^## ", readme, re.DOTALL | re.MULTILINE
    )
    if not catalog_match:
        raise SystemExit("README.md has no '## Curated catalog' section")
    sections = re.findall(r"^### ", catalog_match.group(1), re.MULTILINE)
    return f"{len(entries)} entries organized into {len(sections)} catalog sections"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if README counts are stale instead of rewriting them",
    )
    args = parser.parse_args()

    phrase = expected_counts_phrase()
    readme = README.read_text()
    if not COUNTS_PATTERN.search(readme):
        print(f"README.md is missing a counts phrase matching '{phrase}'")
        return 1
    updated = COUNTS_PATTERN.sub(phrase, readme)
    if updated == readme:
        print(f"README counts are in sync: {phrase}")
        return 0
    if args.check:
        current = COUNTS_PATTERN.search(readme).group(0)
        print(
            f"README counts are stale: found '{current}', expected '{phrase}'.\n"
            f"Run: python scripts/sync_readme_counts.py"
        )
        return 1
    README.write_text(updated)
    print(f"README counts updated: {phrase}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
