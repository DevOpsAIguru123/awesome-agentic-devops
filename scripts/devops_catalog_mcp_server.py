#!/usr/bin/env python3
"""Tiny stdio MCP server for the Awesome Agentic DevOps catalog.

This intentionally has no third-party dependency so generated client configs work
in lightweight workspaces. It implements the minimal JSON-RPC messages used by
MCP clients for initialize, tools/list, and tools/call.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_catalog(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        entries = data.get("entries", [])
    else:
        entries = data
    if not isinstance(entries, list):
        raise SystemExit(f"catalog must be a JSON list or object with entries: {path}")
    return entries


def search(entries: list[dict[str, Any]], query: str = "", category: str = "", limit: int = 10) -> list[dict[str, Any]]:
    query = query.lower().strip()
    category = category.lower().strip()
    matches: list[dict[str, Any]] = []
    for entry in entries:
        haystack = " ".join(
            str(entry.get(field, ""))
            for field in ("name", "url", "category", "type", "framework", "cloud_provider", "operator_note", "risk_notes")
        ).lower()
        haystack += " " + " ".join(str(v) for v in entry.get("use_cases", []))
        if query and query not in haystack:
            continue
        if category and category not in str(entry.get("category", "")).lower():
            continue
        matches.append(entry)
        if len(matches) >= limit:
            break
    return matches


def compact(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": entry.get("name"),
        "url": entry.get("url"),
        "category": entry.get("category"),
        "type": entry.get("type"),
        "framework": entry.get("framework"),
        "action_level": entry.get("action_level"),
        "human_approval": entry.get("human_approval"),
        "evidence_tracing": entry.get("evidence_tracing"),
        "maturity": entry.get("maturity"),
        "operator_note": entry.get("operator_note"),
        "risk_notes": entry.get("risk_notes"),
        "labels": entry.get("labels", []),
    }


def tool_result(payload: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}]}


def handle_request(request: dict[str, Any], entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")

    if method == "notifications/initialized":
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "awesome-agentic-devops-catalog", "version": "0.1.0"},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "search_devops_mcp_catalog",
                        "description": "Search official DevOps/SRE/Cloud MCP servers and agent tools by keyword or category.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Keyword such as terraform, incident, github, observability, security."},
                                "category": {"type": "string", "description": "Optional category substring."},
                                "limit": {"type": "integer", "minimum": 1, "maximum": 25, "default": 10},
                            },
                        },
                    },
                    {
                        "name": "get_devops_mcp_entry",
                        "description": "Return one catalog entry by exact or partial name.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                            "required": ["name"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name == "search_devops_mcp_catalog":
            result = [compact(e) for e in search(entries, args.get("query", ""), args.get("category", ""), int(args.get("limit", 10)))]
        elif name == "get_devops_mcp_entry":
            needle = str(args.get("name", "")).lower().strip()
            result = next((compact(e) for e in entries if needle and needle in str(e.get("name", "")).lower()), None)
            if result is None:
                result = {"error": f"No catalog entry matched: {args.get('name', '')}"}
        else:
            result = {"error": f"Unknown tool: {name}"}
        return {"jsonrpc": "2.0", "id": request_id, "result": tool_result(result)}

    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Awesome Agentic DevOps catalog over stdio MCP.")
    parser.add_argument("--catalog", default="devops-ai/official-devops-mcp-catalog.json", help="Path to generated catalog JSON.")
    args = parser.parse_args()
    entries = load_catalog(Path(args.catalog))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request, entries)
        except Exception as exc:  # pragma: no cover - defensive for client protocols
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(exc)}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
