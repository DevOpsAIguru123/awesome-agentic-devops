#!/usr/bin/env python3
"""Import Archestra MCP evaluation signals for catalog entries.

This script does not change curator scores in data/repos.yaml. It reads an
Archestra `mcp-catalog/data/mcp-evaluations` directory and writes a generated
JSON sidecar with only matching entries. The sidecar is useful for discovery,
search, and review, while keeping external quality scores separate from this
repo's operator safety model.
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
DEFAULT_OUTPUT = ROOT / "data" / "external" / "archestra-signals.json"


def normalize_url(url: str) -> str:
    value = url.strip().rstrip("/").lower()
    if value.endswith(".git"):
        value = value[: -len(".git")]
    if value.startswith("http://"):
        value = "https://" + value[len("http://") :]
    return value


def github_slug(url: str) -> str | None:
    marker = "github.com/"
    if marker not in url.lower():
        return None
    slug = normalize_url(url).split(marker, 1)[1]
    parts = slug.split("/")
    if len(parts) < 2:
        return None
    return "/".join(parts[:2])


def load_catalog_index(path: Path = REPOS_YAML) -> dict[str, dict[str, Any]]:
    entries = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise SystemExit(f"{path} must contain a list of entries")

    index: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        url = str(entry.get("url", ""))
        keys = {normalize_url(url)}
        slug = github_slug(url)
        if slug:
            keys.add(slug)
            keys.add(f"https://github.com/{slug}")
        for key in keys:
            index[key] = entry
    return index


def extract_signal(evaluation: dict[str, Any]) -> dict[str, Any]:
    github_info = evaluation.get("github_info") or {}
    protocol_features = evaluation.get("protocol_features") or {}
    user_config = evaluation.get("user_config") or {}
    oauth_config = evaluation.get("oauth_config") or None
    server = evaluation.get("server") or {}

    sensitive_fields = []
    required_sensitive_fields = []
    for name, config in user_config.items():
        if not isinstance(config, dict) or not config.get("sensitive"):
            continue
        sensitive_fields.append(name)
        if config.get("required"):
            required_sensitive_fields.append(name)

    signal: dict[str, Any] = {
        "archestra_name": evaluation.get("name"),
        "display_name": evaluation.get("display_name"),
        "description": evaluation.get("description"),
        "category": evaluation.get("category"),
        "quality_score": evaluation.get("quality_score"),
        "programming_language": evaluation.get("programming_language"),
        "server_type": server.get("type"),
        "protocol_features": protocol_features,
        "sensitive_config_fields": sorted(sensitive_fields),
        "required_sensitive_config_fields": sorted(required_sensitive_fields),
        "oauth_configured": bool(oauth_config),
        "last_scraped_at": evaluation.get("last_scraped_at"),
    }
    if github_info:
        signal["github_info"] = {
            "url": github_info.get("url"),
            "stars": github_info.get("stars"),
            "contributors": github_info.get("contributors"),
            "releases": github_info.get("releases"),
            "ci_cd": github_info.get("ci_cd"),
            "latest_commit_hash": github_info.get("latest_commit_hash"),
        }
    remote_url = server.get("url")
    if remote_url:
        signal["remote_url"] = remote_url
    docs_url = server.get("docs_url")
    if docs_url:
        signal["docs_url"] = docs_url
    return signal


def candidate_keys(evaluation: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    github_url = ((evaluation.get("github_info") or {}).get("url") or "")
    server = evaluation.get("server") or {}
    for url in [github_url, server.get("url", ""), server.get("docs_url", "")]:
        if not url:
            continue
        keys.add(normalize_url(str(url)))
        slug = github_slug(str(url))
        if slug:
            keys.add(slug)
            keys.add(f"https://github.com/{slug}")
    return keys


def build_signals(source_dir: Path, catalog_path: Path = REPOS_YAML) -> dict[str, Any]:
    if not source_dir.exists():
        raise SystemExit(f"Archestra evaluation directory not found: {source_dir}")
    catalog_index = load_catalog_index(catalog_path)
    matches: dict[str, dict[str, Any]] = {}
    files_seen = 0

    for path in sorted(source_dir.glob("*.json")):
        files_seen += 1
        evaluation = json.loads(path.read_text(encoding="utf-8"))
        for key in candidate_keys(evaluation):
            entry = catalog_index.get(key)
            if not entry:
                continue
            name = str(entry["name"])
            matches[name] = extract_signal(evaluation)
            break

    return {
        "schema_version": 1,
        "source": "archestra-ai/archestra mcp-catalog/data/mcp-evaluations",
        "generated_by": "scripts/import_archestra_signals.py",
        "source_files_seen": files_seen,
        "matched_entry_count": len(matches),
        "signals": dict(sorted(matches.items())),
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, help="Path to Archestra mcp-evaluations directory")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Generated output path")
    parser.add_argument("--check", action="store_true", help="fail if output is stale instead of writing")
    args = parser.parse_args()

    expected = render(build_signals(args.source_dir))
    current = args.output.read_text(encoding="utf-8") if args.output.exists() else None
    if current == expected:
        print(f"{args.output} is in sync: {json.loads(expected)['matched_entry_count']} matches")
        return 0
    if args.check:
        state = "missing" if current is None else "stale"
        print(f"{args.output} is {state}; rerun scripts/import_archestra_signals.py")
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    print(f"{args.output} updated: {json.loads(expected)['matched_entry_count']} matches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
