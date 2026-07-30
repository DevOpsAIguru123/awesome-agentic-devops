#!/usr/bin/env python3
"""Fail-closed release gate for Trivy image and configuration reports."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}


def confined_path(
    path: Path,
    workspace_root: Path,
    *,
    must_exist: bool,
) -> Path:
    """Resolve a CLI path and reject access outside the current workspace."""
    try:
        resolved_root = workspace_root.resolve(strict=True)
        resolved_path = path.resolve(strict=must_exist)
    except OSError as exc:
        raise ValueError(f"cannot resolve path {path}: {exc}") from exc

    if not resolved_path.is_relative_to(resolved_root):
        raise ValueError(f"path escapes workspace root: {path}")
    if must_exist and not resolved_path.is_file():
        raise ValueError(f"expected a report file: {path}")
    return resolved_path


def load_report(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid Trivy JSON from {path}: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("Results"), list):
        raise ValueError(f"invalid Trivy report structure: {path}")
    return payload


def collect(report: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [
        item
        for result in report.get("Results", [])
        if isinstance(result, dict)
        for item in result.get(key) or []
        if isinstance(item, dict)
    ]


def severity_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(str(item.get("Severity") or "UNKNOWN").upper() for item in items)
    return dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-report", type=Path, required=True)
    parser.add_argument("--config-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        workspace_root = Path.cwd()
        image_report_path = confined_path(
            args.image_report, workspace_root, must_exist=True
        )
        config_report_path = confined_path(
            args.config_report, workspace_root, must_exist=True
        )
        output_path = confined_path(args.output, workspace_root, must_exist=False)
        image_report = load_report(image_report_path)
        config_report = load_report(config_report_path)
    except ValueError as exc:
        print(f"PUSH BLOCKED: {exc}", file=sys.stderr)
        return 2

    vulnerabilities = collect(image_report, "Vulnerabilities")
    secrets = collect(image_report, "Secrets") + collect(config_report, "Secrets")
    misconfigurations = [
        item
        for item in collect(config_report, "Misconfigurations")
        if str(item.get("Status") or "FAIL").upper() != "PASS"
    ]

    blocking_vulnerabilities = [
        item
        for item in vulnerabilities
        if str(item.get("Severity") or "UNKNOWN").upper() in BLOCKING_SEVERITIES
    ]
    blocking_misconfigurations = [
        item
        for item in misconfigurations
        if str(item.get("Severity") or "UNKNOWN").upper() in BLOCKING_SEVERITIES
    ]

    reasons: list[str] = []
    if blocking_vulnerabilities:
        reasons.append(
            f"{len(blocking_vulnerabilities)} HIGH/CRITICAL vulnerability occurrences"
        )
    if blocking_misconfigurations:
        reasons.append(
            f"{len(blocking_misconfigurations)} HIGH/CRITICAL misconfigurations"
        )
    if secrets:
        reasons.append(f"{len(secrets)} secret findings")

    decision = "blocked" if reasons else "approved"
    result = {
        "schema_version": "container-release-policy/v1",
        "artifact_name": image_report.get("ArtifactName") or "unknown",
        "image_id": (image_report.get("Metadata") or {}).get("ImageID") or "unknown",
        "policy_decision": decision,
        "policy_rules": {
            "block_severities": sorted(BLOCKING_SEVERITIES),
            "block_any_secret": True,
            "fail_closed_on_invalid_report": True,
        },
        "summary": {
            "vulnerability_occurrences": len(vulnerabilities),
            "vulnerability_severity_counts": severity_counts(vulnerabilities),
            "misconfigurations": len(misconfigurations),
            "misconfiguration_severity_counts": severity_counts(misconfigurations),
            "secrets": len(secrets),
        },
        "blocking_reasons": reasons,
        "publish_allowed": decision == "approved",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if decision == "blocked":
        print("PUSH BLOCKED")
        for reason in reasons:
            print(f"- {reason}")
        print(f"Decision evidence: {output_path}")
        return 1

    print("PUSH APPROVED")
    print(f"Decision evidence: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
