#!/usr/bin/env python3
"""Create safe, deterministic triage and SARIF from Trivy JSON reports."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

BLOCKING_SEVERITIES = {"HIGH", "CRITICAL"}
NOT_APPLICABLE = "not applicable"
SARIF_SECURITY_SCORE = {
    "CRITICAL": 9.5,
    "HIGH": 8.0,
    "MEDIUM": 5.5,
    "LOW": 2.0,
    "UNKNOWN": 2.0,
}
SEVERITY_PRIORITY = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
    "UNKNOWN": 4,
}


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


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return payload


def markdown(value: Any) -> str:
    """Render scanner-controlled values as inert single-line Markdown text."""
    text = str(value or "unknown").replace("\r", " ").replace("\n", " ")
    for source, replacement in (
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("|", "&#124;"),
        ("`", "&#96;"),
    ):
        text = text.replace(source, replacement)
    return text


def safe_url(value: Any) -> str | None:
    candidate = str(value or "")
    parsed = urlparse(candidate)
    if parsed.scheme == "https" and parsed.netloc:
        return candidate
    return None


def severity(value: Any) -> str:
    normalized = str(value or "UNKNOWN").upper()
    return normalized if normalized in SEVERITY_PRIORITY else "UNKNOWN"


def findings(
    report: dict[str, Any], key: str
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[dict[str, Any], dict[str, Any]]] = []
    results = report.get("Results")
    if not isinstance(results, list):
        raise ValueError("invalid Trivy report: Results must be a list")
    for result in results:
        if not isinstance(result, dict):
            continue
        items = result.get(key) or []
        if not isinstance(items, list):
            continue
        rows.extend((result, item) for item in items if isinstance(item, dict))
    return rows


def location_for(
    kind: str,
    result: dict[str, Any],
    item: dict[str, Any],
    dockerfile: str,
) -> tuple[str, int, int]:
    if kind != "misconfiguration":
        return dockerfile, 1, 1

    target = str(result.get("Target") or dockerfile)
    target_name = Path(target).name
    if target_name == "Dockerfile":
        target = dockerfile
    elif target_name:
        target = target_name

    cause = item.get("CauseMetadata") or {}
    start = max(int(cause.get("StartLine") or 1), 1)
    end = max(int(cause.get("EndLine") or start), start)
    return target, start, end


def vulnerability_record(
    result: dict[str, Any], item: dict[str, Any], dockerfile: str
) -> dict[str, Any]:
    finding_severity = severity(item.get("Severity"))
    fixed_version = str(item.get("FixedVersion") or "")
    package = str(item.get("PkgName") or "unknown")
    installed = str(item.get("InstalledVersion") or "unknown")
    finding_id = str(item.get("VulnerabilityID") or "TRIVY-VULNERABILITY")
    action = (
        f"Upgrade {package} from {installed} to {fixed_version}."
        if fixed_version
        else f"Rebuild from an updated base image and verify whether {package} is required."
    )
    path, start, end = location_for("vulnerability", result, item, dockerfile)
    return {
        "kind": "vulnerability",
        "source_type": "cve",
        "id": finding_id,
        "title": str(item.get("Title") or f"Vulnerability in {package}"),
        "severity": finding_severity,
        "component": package,
        "installed_version": installed,
        "fixed_version": fixed_version or "not published",
        "scanner_status": str(item.get("Status") or "unknown"),
        "policy_blocking": finding_severity in BLOCKING_SEVERITIES,
        "triage_verdict": "needs_review",
        "confidence": "medium",
        "rationale": (
            "Trivy matched the installed package version to an advisory. "
            "Runtime reachability and compensating controls are not established by an image scan."
        ),
        "recommended_action": action,
        "reference": safe_url(item.get("PrimaryURL")),
        "location": {"path": path, "start_line": start, "end_line": end},
    }


def misconfiguration_record(
    result: dict[str, Any], item: dict[str, Any], dockerfile: str
) -> dict[str, Any]:
    finding_severity = severity(item.get("Severity"))
    finding_id = str(item.get("ID") or "TRIVY-MISCONFIGURATION")
    path, start, end = location_for("misconfiguration", result, item, dockerfile)
    return {
        "kind": "misconfiguration",
        "source_type": "scanner_ticket",
        "id": finding_id,
        "title": str(item.get("Title") or item.get("Message") or finding_id),
        "severity": finding_severity,
        "component": str(result.get("Target") or path),
        "installed_version": NOT_APPLICABLE,
        "fixed_version": NOT_APPLICABLE,
        "scanner_status": str(item.get("Status") or "FAIL"),
        "policy_blocking": finding_severity in BLOCKING_SEVERITIES,
        "triage_verdict": "needs_review",
        "confidence": "high",
        "rationale": (
            "Trivy identified the configuration condition at a concrete source location. "
            "Deployment context and boundary impact still require review."
        ),
        "recommended_action": str(
            item.get("Resolution") or "Apply the scanner remediation and rescan."
        ),
        "reference": safe_url(item.get("PrimaryURL")),
        "location": {"path": path, "start_line": start, "end_line": end},
    }


def secret_record(
    result: dict[str, Any], item: dict[str, Any], dockerfile: str
) -> dict[str, Any]:
    path, start, end = location_for("secret", result, item, dockerfile)
    finding_id = str(item.get("RuleID") or item.get("Category") or "TRIVY-SECRET")
    return {
        "kind": "secret",
        "source_type": "scanner_ticket",
        "id": finding_id,
        "title": "Potential secret detected",
        "severity": severity(item.get("Severity") or "CRITICAL"),
        "component": str(result.get("Target") or "container image"),
        "installed_version": NOT_APPLICABLE,
        "fixed_version": NOT_APPLICABLE,
        "scanner_status": "detected",
        "policy_blocking": True,
        "triage_verdict": "needs_review",
        "confidence": "high",
        "rationale": (
            "Trivy detected secret-like material. The match value is intentionally omitted "
            "from all generated outputs."
        ),
        "recommended_action": "Revoke or rotate the credential, remove it from image history, and rescan.",
        "reference": None,
        "location": {"path": path, "start_line": start, "end_line": end},
    }


def normalize(
    image_report: dict[str, Any],
    config_report: dict[str, Any],
    dockerfile: str,
) -> list[dict[str, Any]]:
    records = [
        vulnerability_record(result, item, dockerfile)
        for result, item in findings(image_report, "Vulnerabilities")
    ]
    records.extend(
        secret_record(result, item, dockerfile)
        for report in (image_report, config_report)
        for result, item in findings(report, "Secrets")
    )
    records.extend(
        misconfiguration_record(result, item, dockerfile)
        for result, item in findings(config_report, "Misconfigurations")
        if str(item.get("Status") or "FAIL").upper() != "PASS"
    )
    records.sort(
        key=lambda row: (
            SEVERITY_PRIORITY[row["severity"]],
            0 if row["policy_blocking"] else 1,
            0 if row["fixed_version"] not in {"not published", NOT_APPLICABLE} else 1,
            row["kind"],
            row["id"],
            row["component"],
        )
    )
    for rank, record in enumerate(records, start=1):
        record["triage_item_id"] = f"triage-{rank:04d}"
        record["exploitability_review_rank"] = rank
    return records


def triage_payload(
    records: list[dict[str, Any]],
    policy: dict[str, Any],
    image_report: dict[str, Any],
) -> dict[str, Any]:
    counts = Counter(record["severity"] for record in records)
    policy_decision = str(policy.get("policy_decision") or "not_evaluated")
    return {
        "schema_version": "container-security-triage/v1",
        "artifact_name": image_report.get("ArtifactName") or "unknown",
        "policy_decision": policy_decision,
        "policy_authoritative": False,
        "approval_notice": (
            "Automated triage is advisory. policy_decision: not_evaluated is not approval."
        ),
        "summary": {
            "total_findings": len(records),
            "policy_blocking_findings": sum(
                bool(record["policy_blocking"]) for record in records
            ),
            "severity_counts": dict(sorted(counts.items())),
        },
        "findings": records,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    counts = summary["severity_counts"]
    lines = [
        "# Container security triage",
        "",
        f"**Policy decision:** `{markdown(payload['policy_decision'])}`",
        "",
        "> Automated triage is advisory. `policy_decision: not_evaluated` is not approval. "
        "Only the deterministic release policy can authorize publishing.",
        "",
        "## Finding summary",
        "",
        f"- Total findings: **{summary['total_findings']}**",
        f"- Policy-blocking findings: **{summary['policy_blocking_findings']}**",
        "- Severity: "
        + ", ".join(
            f"{name} **{counts.get(name, 0)}**"
            for name in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN")
        ),
        "",
    ]
    records = payload["findings"]
    if not records:
        lines.extend(
            [
                "## Triage queue",
                "",
                "No Trivy vulnerability, secret, or failed configuration findings were reported.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "## Ranked triage queue",
            "",
            "Rank is a review order derived from severity, policy impact, fix availability, and stable scanner metadata. It is not proof of exploitability.",
            "",
            "| Rank | Type | ID | Severity | Component | Installed | Fixed | Policy | Verdict |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        lines.append(
            "| {rank} | {kind} | {identifier} | {severity} | {component} | "
            "{installed} | {fixed} | {policy} | {verdict} |".format(
                rank=record["exploitability_review_rank"],
                kind=markdown(record["kind"]),
                identifier=markdown(record["id"]),
                severity=markdown(record["severity"]),
                component=markdown(record["component"]),
                installed=markdown(record["installed_version"]),
                fixed=markdown(record["fixed_version"]),
                policy="BLOCK" if record["policy_blocking"] else "review",
                verdict=markdown(record["triage_verdict"]),
            )
        )

    lines.extend(["", "## Finding details", ""])
    for record in records:
        location = record["location"]
        lines.extend(
            [
                f"### {record['exploitability_review_rank']}. {markdown(record['id'])} — {markdown(record['component'])}",
                "",
                f"- Severity: **{markdown(record['severity'])}**",
                f"- Location: `{markdown(location['path'])}:{location['start_line']}`",
                f"- Confidence: `{markdown(record['confidence'])}`",
                f"- Rationale: {markdown(record['rationale'])}",
                f"- Recommended action: {markdown(record['recommended_action'])}",
                "",
            ]
        )
    return "\n".join(lines)


def sarif_level(finding_severity: str) -> str:
    if finding_severity in BLOCKING_SEVERITIES:
        return "error"
    if finding_severity == "MEDIUM":
        return "warning"
    return "note"


def _sarif_rule(record: dict[str, Any], rule_id: str) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "id": rule_id,
        "name": str(record["id"]),
        "shortDescription": {"text": str(record["title"])[:1024]},
        "properties": {
            "security-severity": str(SARIF_SECURITY_SCORE[record["severity"]]),
            "tags": ["security", "trivy", record["kind"]],
        },
    }
    if record["reference"]:
        rule["helpUri"] = record["reference"]
    return rule


def _sarif_result(record: dict[str, Any], rule_id: str) -> dict[str, Any]:
    location = record["location"]
    fingerprint_source = "|".join(
        str(record[field]) for field in ("kind", "id", "component", "installed_version")
    )
    return {
        "ruleId": rule_id,
        "level": sarif_level(record["severity"]),
        "message": {
            "text": f"{record['id']} in {record['component']}: {record['recommended_action']}"
        },
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": location["path"]},
                    "region": {
                        "startLine": location["start_line"],
                        "endLine": location["end_line"],
                    },
                }
            }
        ],
        "partialFingerprints": {
            "primaryLocationLineHash": hashlib.sha256(
                fingerprint_source.encode("utf-8")
            ).hexdigest()
        },
        "properties": {
            "severity": record["severity"],
            "policyBlocking": record["policy_blocking"],
            "triageVerdict": record["triage_verdict"],
        },
    }


def render_sarif(records: list[dict[str, Any]]) -> dict[str, Any]:
    rules: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    for record in records:
        rule_id = f"trivy/{record['kind']}/{record['id']}"
        rules.setdefault(rule_id, _sarif_rule(record, rule_id))
        results.append(_sarif_result(record, rule_id))

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Trivy container security triage",
                        "informationUri": "https://trivy.dev/",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    validated_path = confined_path(path, Path.cwd(), must_exist=False)
    validated_path.parent.mkdir(parents=True, exist_ok=True)
    validated_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    validated_path = confined_path(path, Path.cwd(), must_exist=False)
    validated_path.parent.mkdir(parents=True, exist_ok=True)
    validated_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-report", type=Path, required=True)
    parser.add_argument("--config-report", type=Path, required=True)
    parser.add_argument("--policy-report", type=Path, required=True)
    parser.add_argument("--dockerfile", required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--sarif-output", type=Path, required=True)
    args = parser.parse_args()

    try:
        workspace_root = Path.cwd()
        image_path = confined_path(args.image_report, workspace_root, must_exist=True)
        config_path = confined_path(args.config_report, workspace_root, must_exist=True)
        policy_path = confined_path(
            args.policy_report, workspace_root, must_exist=False
        )
        json_path = confined_path(args.json_output, workspace_root, must_exist=False)
        markdown_path = confined_path(
            args.markdown_output, workspace_root, must_exist=False
        )
        sarif_path = confined_path(args.sarif_output, workspace_root, must_exist=False)
        image_report = load_json(image_path)
        config_report = load_json(config_path)
        policy = load_json(policy_path) if policy_path.is_file() else {}
        records = normalize(image_report, config_report, args.dockerfile)
        payload = triage_payload(records, policy, image_report)
        write_json(json_path, payload)
        write_text(markdown_path, render_markdown(payload) + "\n")
        write_json(sarif_path, render_sarif(records))
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Triaged {len(records)} Trivy finding occurrences")
    print(f"Readable report: {markdown_path}")
    print(f"GitHub Code Scanning report: {sarif_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
