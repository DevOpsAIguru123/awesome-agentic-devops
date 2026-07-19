"""Tests for data/catalog.json, the stdlib-readable projection of the catalog.

The installer reads this file instead of data/repos.yaml so it works on a stock
interpreter with no PyYAML. It is generated, so the job here is to prove it
matches its source and has the shape the installer expects.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.sync_catalog_json import (  # noqa: E402
    CATALOG_JSON,
    SKILL_CATEGORIES,
    build_catalog,
    render,
)


def test_catalog_json_is_in_sync_with_repos_yaml():
    """CI runs sync_catalog_json.py --check; this fails the same way locally."""
    assert CATALOG_JSON.exists(), "data/catalog.json is missing; run scripts/sync_catalog_json.py"
    assert CATALOG_JSON.read_text(encoding="utf-8") == render(build_catalog()), (
        "data/catalog.json is stale. Run: python scripts/sync_catalog_json.py"
    )


def test_every_entry_has_the_fields_the_installer_reads():
    entries = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))["entries"]
    assert entries, "catalog.json has no entries"
    for entry in entries:
        assert set(entry) == {"name", "url", "category"}, entry
        assert entry["category"] in SKILL_CATEGORIES, entry
        assert entry["url"].startswith("https://github.com/"), entry
        # install_skills.py derives owner/repo by splitting on github.com/
        owner_repo = entry["url"].split("github.com/", 1)[1]
        assert owner_repo.count("/") == 1, entry


def test_catalog_holds_both_official_and_community_skills():
    entries = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))["entries"]
    categories = {entry["category"] for entry in entries}
    assert categories == set(SKILL_CATEGORIES), (
        "catalog.json should carry both official and community skill sources"
    )
