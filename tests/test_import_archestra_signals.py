"""Tests for importing Archestra external MCP evaluation signals."""

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.import_archestra_signals import (  # noqa: E402
    build_signals,
    github_slug,
    normalize_url,
)


def test_normalize_url_handles_github_variants():
    assert normalize_url("HTTP://github.com/Owner/Repo.git/") == "https://github.com/owner/repo"
    assert github_slug("https://github.com/Owner/Repo/tree/main/path") == "owner/repo"


def test_build_signals_matches_by_github_url(tmp_path):
    catalog = tmp_path / "repos.yaml"
    catalog.write_text(
        yaml.safe_dump(
            [
                {
                    "name": "example/tool",
                    "url": "https://github.com/example/tool",
                }
            ]
        ),
        encoding="utf-8",
    )
    source = tmp_path / "evals"
    source.mkdir()
    (source / "example__tool.json").write_text(
        json.dumps(
            {
                "name": "example__tool",
                "display_name": "Example Tool",
                "description": "Useful MCP server",
                "category": "Development",
                "quality_score": 77,
                "programming_language": "Python",
                "github_info": {
                    "url": "https://github.com/example/tool",
                    "stars": 42,
                    "contributors": 3,
                    "releases": True,
                    "ci_cd": True,
                    "latest_commit_hash": "abc123",
                },
                "server": {"type": "local"},
                "protocol_features": {"implementing_tools": True},
                "user_config": {
                    "token": {"sensitive": True, "required": True},
                    "url": {"sensitive": False, "required": True},
                },
                "last_scraped_at": "2026-07-22T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    result = build_signals(source, catalog)

    assert result["source_files_seen"] == 1
    assert result["matched_entry_count"] == 1
    signal = result["signals"]["example/tool"]
    assert signal["quality_score"] == 77
    assert signal["github_info"]["stars"] == 42
    assert signal["protocol_features"] == {"implementing_tools": True}
    assert signal["sensitive_config_fields"] == ["token"]
    assert signal["required_sensitive_config_fields"] == ["token"]


def test_build_signals_matches_by_remote_url(tmp_path):
    catalog = tmp_path / "repos.yaml"
    catalog.write_text(
        yaml.safe_dump([{"name": "Example Remote", "url": "https://mcp.example.com/mcp"}]),
        encoding="utf-8",
    )
    source = tmp_path / "evals"
    source.mkdir()
    (source / "remote.json").write_text(
        json.dumps(
            {
                "name": "example__remote",
                "server": {"type": "remote", "url": "https://mcp.example.com/mcp/"},
                "user_config": {},
            }
        ),
        encoding="utf-8",
    )

    result = build_signals(source, catalog)

    assert result["matched_entry_count"] == 1
    assert result["signals"]["Example Remote"]["server_type"] == "remote"
