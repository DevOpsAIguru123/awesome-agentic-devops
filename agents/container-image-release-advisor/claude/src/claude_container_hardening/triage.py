"""Bound and sanitize deterministic Trivy triage evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import AgentReview

DEFAULT_MAX_FINDINGS = 50


def confined_path(path: Path, workspace_root: Path, *, must_exist: bool) -> Path:
    """Reject input and output paths that escape the standalone project."""
    try:
        root = workspace_root.resolve(strict=True)
        resolved = path.resolve(strict=must_exist)
    except OSError as exc:
        raise ValueError(f"cannot resolve path {path}: {exc}") from exc
    if not resolved.is_relative_to(root):
        raise ValueError(f"path escapes workspace root: {path}")
    if must_exist and not resolved.is_file():
        raise ValueError(f"expected a triage report file: {path}")
    return resolved


def load_triage(path: Path) -> dict[str, Any]:
    """Load the minimum required deterministic triage structure."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid triage JSON from {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("triage report must be a JSON object")
    if not isinstance(payload.get("findings"), list):
        raise ValueError("triage report findings must be a list")
    if not isinstance(payload.get("summary"), dict):
        raise ValueError("triage report summary must be an object")
    return payload


def compact(value: Any, limit: int = 500) -> str:
    """Normalize and cap scanner-controlled strings."""
    text = " ".join(str(value or "unknown").split())
    return text if len(text) <= limit else f"{text[: limit - 3]}..."


def build_envelope(triage: dict[str, Any], max_findings: int) -> dict[str, Any]:
    """Create a bounded, allowlisted model envelope."""
    raw_findings = triage["findings"]
    selected: list[dict[str, Any]] = []
    for raw in raw_findings[:max_findings]:
        if not isinstance(raw, dict):
            continue
        location = raw.get("location") if isinstance(raw.get("location"), dict) else {}
        selected.append(
            {
                "triage_item_id": compact(raw.get("triage_item_id"), 80),
                "id": compact(raw.get("id"), 120),
                "kind": compact(raw.get("kind"), 40),
                "severity": compact(raw.get("severity"), 20),
                "component": compact(raw.get("component"), 200),
                "installed_version": compact(raw.get("installed_version"), 120),
                "fixed_version": compact(raw.get("fixed_version"), 120),
                "policy_blocking": bool(raw.get("policy_blocking")),
                "scanner_status": compact(raw.get("scanner_status"), 80),
                "location": {
                    "path": compact(location.get("path"), 300),
                    "start_line": location.get("start_line"),
                },
            }
        )
    return {
        "schema_version": "container-security-agent-input/v1",
        "policy_decision": compact(triage.get("policy_decision"), 40),
        "policy_authority": "deterministic-policy-only",
        "summary": triage["summary"],
        "input_total_findings": len(raw_findings),
        "input_returned_findings": len(selected),
        "input_truncated": len(raw_findings) > len(selected),
        "findings": selected,
    }


def validate_finding_ids(review: AgentReview, envelope: dict[str, Any]) -> AgentReview:
    """Reject citations that are absent from the bounded evidence."""
    allowed = {finding["id"] for finding in envelope["findings"]}
    cited = {
        finding_id
        for action in review.prioritized_actions
        for finding_id in action.finding_ids
    }
    if cited - allowed:
        raise ValueError("agent cited finding IDs outside the bounded input")
    return review
