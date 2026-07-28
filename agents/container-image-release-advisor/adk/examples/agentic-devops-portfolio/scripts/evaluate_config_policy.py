#!/usr/bin/env python3
"""Fail-closed pre-build policy for a Trivy configuration report."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}
REPORT_PATH = Path("reports/ci-config-trivy.json")


def load_report() -> dict[str, Any]:
    try:
        payload = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid Trivy configuration JSON: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("Results"), list):
        raise ValueError("invalid Trivy configuration report structure")
    return payload


def failed_misconfigurations(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for result in report["Results"]
        if isinstance(result, dict)
        for item in result.get("Misconfigurations") or []
        if isinstance(item, dict)
        and str(item.get("Status") or "FAIL").upper() != "PASS"
    ]


def write_outputs(decision: dict[str, Any]) -> None:
    Path("reports").mkdir(parents=True, exist_ok=True)
    with open(
        "reports/ci-config-policy-decision.json", "w", encoding="utf-8"
    ) as output_file:
        json.dump(decision, output_file, indent=2)
        output_file.write("\n")

    summary = decision["summary"]
    status = decision["policy_decision"]
    lines = [
        "# Pre-build configuration policy",
        "",
        f"**Decision:** `{status}`",
        "",
        f"- Failed misconfigurations: **{summary['failed_misconfigurations']}**",
        f"- HIGH/CRITICAL blocking findings: **{summary['blocking_findings']}**",
        "",
        "> This deterministic check runs before the Docker build. A blocked or missing "
        "decision cannot authorize building or publishing an image.",
        "",
    ]
    with open(
        "reports/ci-config-policy.md", "w", encoding="utf-8"
    ) as output_file:
        output_file.write("\n".join(lines))


def main() -> int:
    try:
        report = load_report()
    except ValueError as exc:
        print(f"BUILD BLOCKED: {exc}", file=sys.stderr)
        return 2

    findings = failed_misconfigurations(report)
    blocking = [
        item
        for item in findings
        if str(item.get("Severity") or "UNKNOWN").upper() in BLOCKING_SEVERITIES
    ]
    severity_counts = Counter(
        str(item.get("Severity") or "UNKNOWN").upper() for item in findings
    )
    policy_decision = "blocked" if blocking else "approved"
    decision = {
        "schema_version": "prebuild-config-policy/v1",
        "policy_decision": policy_decision,
        "build_allowed": policy_decision == "approved",
        "policy_rules": {
            "block_severities": sorted(BLOCKING_SEVERITIES),
            "fail_closed_on_invalid_report": True,
        },
        "summary": {
            "failed_misconfigurations": len(findings),
            "blocking_findings": len(blocking),
            "severity_counts": dict(sorted(severity_counts.items())),
        },
    }
    write_outputs(decision)

    if blocking:
        print(
            f"BUILD BLOCKED: {len(blocking)} HIGH/CRITICAL configuration findings"
        )
        return 1
    print("PRE-BUILD CONFIGURATION APPROVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
