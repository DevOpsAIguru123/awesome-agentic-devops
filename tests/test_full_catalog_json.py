"""Tests for data/catalog.full.json, the full machine-readable catalog."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.sync_full_catalog_json import (  # noqa: E402
    FULL_CATALOG_JSON,
    build_full_catalog,
    render,
)
from scripts.validate_repos_yaml import validate_file  # noqa: E402


def test_full_catalog_json_is_in_sync_with_repos_yaml():
    assert FULL_CATALOG_JSON.exists(), (
        "data/catalog.full.json is missing; run scripts/sync_full_catalog_json.py"
    )
    assert FULL_CATALOG_JSON.read_text(encoding="utf-8") == render(build_full_catalog()), (
        "data/catalog.full.json is stale. Run: python scripts/sync_full_catalog_json.py"
    )


def test_full_catalog_contains_every_repo_entry():
    source_entries = validate_file(Path("data/repos.yaml"))
    full_catalog = json.loads(FULL_CATALOG_JSON.read_text(encoding="utf-8"))

    assert full_catalog["schema_version"] == 1
    assert full_catalog["source"] == "data/repos.yaml"
    assert full_catalog["entry_count"] == len(source_entries)
    assert len(full_catalog["entries"]) == len(source_entries)
    assert {entry["name"] for entry in full_catalog["entries"]} == {
        entry["name"] for entry in source_entries
    }


def test_full_catalog_exposes_safety_and_search_fields():
    entries = json.loads(FULL_CATALOG_JSON.read_text(encoding="utf-8"))["entries"]
    assert entries, "catalog.full.json has no entries"

    required_public = {
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
        "safety",
    }
    required_safety = {
        "action_level",
        "human_approval",
        "evidence_tracing",
        "maturity",
        "risk_notes",
    }
    for entry in entries:
        assert required_public <= set(entry), entry
        assert required_safety == set(entry["safety"]), entry
        assert isinstance(entry["use_cases"], list), entry
        assert isinstance(entry["labels"], list), entry
        if "github.com/" in entry["url"]:
            assert entry["github_slug"].count("/") == 1, entry
