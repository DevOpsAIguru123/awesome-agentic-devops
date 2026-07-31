#!/usr/bin/env python3
"""Combine Sonar code findings and Trivy container findings into one report."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def confined_path(path: Path, workspace_root: Path, *, must_exist: bool) -> Path:
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


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def markdown(value: Any) -> str:
    text = str(value if value is not None else "unknown").replace("\r", " ").replace("\n", " ")
    for source, replacement in (
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("|", "&#124;"),
        ("`", "&#96;"),
    ):
        text = text.replace(source, replacement)
    return text


def safe_link(value: Any) -> str | None:
    candidate = str(value or "")
    parsed = urlparse(candidate)
    return candidate if parsed.scheme == "https" and parsed.netloc else None


def rows(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def build_payload(sonar: dict[str, Any], trivy: dict[str, Any]) -> dict[str, Any]:
    code_findings = rows(sonar.get("findings"))
    hotspots = rows(sonar.get("hotspots"))
    container_findings = rows(trivy.get("findings"))
    code_severities = Counter(str(item.get("severity", "UNKNOWN")) for item in code_findings)
    container_severities = Counter(
        str(item.get("severity", "UNKNOWN")) for item in container_findings
    )
    quality_gate = sonar.get("quality_gate", {})
    quality_status = (
        str(quality_gate.get("status", "UNKNOWN"))
        if isinstance(quality_gate, dict)
        else "UNKNOWN"
    )
    policy_decision = str(trivy.get("policy_decision", "not_evaluated"))
    return {
        "schema_version": "unified-devsecops-report/v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "authority": {
            "sonar_quality_gate": quality_status,
            "container_release_policy": policy_decision,
            "container_policy_authorized": policy_decision == "approved",
            "overall_release_ready": (
                quality_status == "OK" and policy_decision == "approved"
            ),
            "notice": (
                "Sonar and Trivy decisions are independent. Only the deterministic "
                "container release policy authorizes image publishing. "
                "policy_decision: not_evaluated is not approval."
            ),
        },
        "summary": {
            "total_actionable_items": len(code_findings) + len(hotspots) + len(container_findings),
            "sonar_open_issues": len(code_findings),
            "sonar_security_hotspots": len(hotspots),
            "trivy_findings": len(container_findings),
            "trivy_policy_blocking": sum(
                bool(item.get("policy_blocking")) for item in container_findings
            ),
            "sonar_severity_counts": dict(sorted(code_severities.items())),
            "trivy_severity_counts": dict(sorted(container_severities.items())),
        },
        "code_scan": sonar,
        "image_and_configuration_scan": trivy,
    }


def render_code_findings(sonar: dict[str, Any]) -> list[str]:
    code_findings = rows(sonar.get("findings"))
    lines = ["## Sonar code findings", ""]
    dashboard = safe_link(sonar.get("dashboard_url"))
    if dashboard:
        lines.extend([f"[Open analysis in SonarQube Cloud]({dashboard})", ""])
    if code_findings:
        lines.extend(
            [
                "| Severity | Type | Rule | Location | Finding | Status |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in code_findings:
            location = str(item.get("component", "unknown"))
            if item.get("line"):
                location += f":{item['line']}"
            lines.append(
                "| {severity} | {kind} | {rule} | {location} | {message} | {status} |".format(
                    severity=markdown(item.get("severity")),
                    kind=markdown(item.get("kind")),
                    rule=markdown(item.get("rule")),
                    location=markdown(location),
                    message=markdown(item.get("message")),
                    status=markdown(item.get("status")),
                )
            )
    else:
        lines.append("No open Sonar code issues were reported.")
    return lines


def render_hotspots(sonar: dict[str, Any]) -> list[str]:
    hotspots = rows(sonar.get("hotspots"))
    lines = ["## Sonar security hotspots", ""]
    if hotspots:
        lines.extend(
            [
                "| Priority | Category | Location | Review status | Finding |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in hotspots:
            location = str(item.get("component", "unknown"))
            if item.get("line"):
                location += f":{item['line']}"
            lines.append(
                "| {severity} | {rule} | {location} | {status} | {message} |".format(
                    severity=markdown(item.get("severity")),
                    rule=markdown(item.get("rule")),
                    location=markdown(location),
                    status=markdown(item.get("status")),
                    message=markdown(item.get("message")),
                )
            )
    else:
        lines.append("No Sonar security hotspots were reported.")
    return lines


def render_container_findings(trivy: dict[str, Any]) -> list[str]:
    container_findings = rows(trivy.get("findings"))
    lines = ["## Trivy image and configuration findings", ""]
    if container_findings:
        lines.extend(
            [
                "| Rank | Severity | Type | ID | Component | Policy | Remediation |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in container_findings:
            lines.append(
                "| {rank} | {severity} | {kind} | {identifier} | {component} | {policy} | {action} |".format(
                    rank=markdown(item.get("exploitability_review_rank")),
                    severity=markdown(item.get("severity")),
                    kind=markdown(item.get("kind")),
                    identifier=markdown(item.get("id")),
                    component=markdown(item.get("component")),
                    policy="BLOCK" if item.get("policy_blocking") else "review",
                    action=markdown(item.get("recommended_action")),
                )
            )
    else:
        lines.append("No Trivy vulnerability, secret, or failed configuration findings were reported.")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    authority = report["authority"]
    summary = report["summary"]
    sonar = report["code_scan"]
    trivy = report["image_and_configuration_scan"]
    lines = [
        "# Consolidated Release Security Report",
        "",
        "Combines SonarQube source-code findings, Trivy configuration and "
        "container-image findings, deterministic release policy, and "
        "Claude advisory triage.",
        "",
        "## Overall release decision",
        "",
        f"**{'APPROVED' if authority['overall_release_ready'] else 'BLOCKED'}**",
        "",
        "This is the combined deterministic result. Protected human approval is still required before publishing.",
        "",
        "## Scoped scanner decisions",
        "",
        f"- Sonar quality gate: **{markdown(authority['sonar_quality_gate'])}**",
        f"- Deterministic container policy: **{markdown(authority['container_release_policy'])}**",
        f"- Container policy authorization: **{str(authority['container_policy_authorized']).lower()}**",
        "",
        "> Sonar and Trivy decisions are independent. Only the deterministic container "
        "release policy authorizes image publishing. `policy_decision: not_evaluated` is not approval.",
        "",
        "## Executive summary",
        "",
        "| Scanner | Scope | Findings requiring attention | Gate |",
        "| --- | --- | ---: | --- |",
        f"| SonarQube Cloud | Source code | {summary['sonar_open_issues']} issues + {summary['sonar_security_hotspots']} hotspots | {markdown(authority['sonar_quality_gate'])} |",
        f"| Trivy | Image, dependencies, secrets, configuration | {summary['trivy_findings']} | {markdown(authority['container_release_policy'])} |",
        f"| **Combined** | Full release candidate | **{summary['total_actionable_items']}** | Both gates remain authoritative in their scope |",
        "",
        *render_code_findings(sonar),
        "",
        *render_hotspots(sonar),
        "",
        *render_container_findings(trivy),
    ]

    lines.extend(
        [
            "",
            "## Team workflow",
            "",
            "1. Developers fix Sonar code issues and review each security hotspot.",
            "2. Platform or application owners remediate Trivy image/configuration findings.",
            "3. Re-run the pipeline; do not edit this generated evidence manually.",
            "4. Publishing remains blocked unless every required CI gate and protected approval succeeds.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sonar-report", type=Path, required=True)
    parser.add_argument("--trivy-report", type=Path, required=True)
    args = parser.parse_args()
    try:
        workspace_root = Path.cwd()
        sonar_path = confined_path(args.sonar_report, workspace_root, must_exist=True)
        trivy_path = confined_path(args.trivy_report, workspace_root, must_exist=True)
        report = build_payload(load_object(sonar_path), load_object(trivy_path))
        Path("reports").mkdir(parents=True, exist_ok=True)
        with open(
            "reports/ci-unified-security.json", "w", encoding="utf-8"
        ) as json_output:
            json.dump(report, json_output, indent=2)
            json_output.write("\n")
        with open(
            "reports/ci-unified-security.md", "w", encoding="utf-8"
        ) as markdown_output:
            markdown_output.write(render_markdown(report) + "\n")
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Aggregated {report['summary']['total_actionable_items']} actionable items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
