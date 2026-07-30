#!/usr/bin/env python3
"""Render sanitized pre-build or container findings as HTML and PDF."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)

CSS = """
:root { color-scheme: light; --ink:#172033; --muted:#596579; --line:#d8deea;
  --panel:#f6f8fc; --brand:#2457d6; --ok:#167447; --bad:#b42318; --warn:#a15c00; }
* { box-sizing:border-box; }
body { margin:0; font:14px/1.5 Inter,Arial,sans-serif; color:var(--ink); background:#fff; }
main { max-width:1120px; margin:0 auto; padding:40px; }
h1 { margin:0 0 8px; font-size:30px; } h2 { margin:32px 0 12px; font-size:20px; }
h3 { margin:20px 0 8px; font-size:16px; }
.subtitle,.muted { color:var(--muted); } .decision { font-weight:700; }
.cards { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin:20px 0; }
.card { border:1px solid var(--line); border-radius:10px; padding:14px; background:var(--panel); }
.card .label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
.card .value { display:block; margin-top:4px; font-size:24px; font-weight:750; }
.approved { color:var(--ok); } .blocked { color:var(--bad); } .review { color:var(--warn); }
table { width:100%; border-collapse:collapse; margin:12px 0 24px; table-layout:fixed; }
th,td { border:1px solid var(--line); padding:8px; text-align:left; vertical-align:top; overflow-wrap:anywhere; }
th { background:#edf1f8; font-size:12px; } tr { break-inside:avoid; }
.nowrap { white-space:nowrap; overflow-wrap:normal; } .table-page { break-before:page; }
.continuation { margin:8px 0; color:var(--muted); font-size:12px; font-weight:700; }
.sev-critical,.sev-high { color:var(--bad); font-weight:700; }
.sev-medium { color:var(--warn); font-weight:700; } .sev-low { color:var(--ok); font-weight:700; }
.notice { border-left:4px solid var(--brand); padding:10px 14px; background:#f3f6ff; }
.release-banner { margin:24px 0; border:2px solid var(--line); border-radius:12px; padding:18px; }
.release-banner .label { color:var(--muted); font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; }
.release-banner .value { display:block; margin:4px 0; font-size:30px; font-weight:800; }
code { font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:12px; }
ol,ul { padding-left:22px; }
@page { size:A4 landscape; margin:12mm; }
@media print {
  main { max-width:none; padding:0; } a { color:inherit; text-decoration:none; }
  thead { display:table-header-group; } .cards { grid-template-columns:repeat(4,1fr); }
  h2 { break-after:avoid; }
}
@media (max-width:760px) { main { padding:20px; } .cards { grid-template-columns:1fr 1fr; } }
"""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid report JSON from {path.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object in {path.name}")
    return payload


def text(value: Any) -> str:
    return html.escape(str(value if value not in (None, "") else "not available"))


def safe_url(value: Any) -> str | None:
    candidate = str(value or "")
    parsed = urlparse(candidate)
    return candidate if parsed.scheme == "https" and parsed.netloc else None


def severity(value: Any) -> str:
    normalized = str(value or "UNKNOWN").upper()
    return normalized if normalized in SEVERITY_ORDER else "UNKNOWN"


def metric_cards(cards: list[tuple[str, Any, str]]) -> str:
    return '<div class="cards">' + "".join(
        f'<div class="card"><span class="label">{text(label)}</span>'
        f'<span class="value {text(style)}">{text(value)}</span></div>'
        for label, value, style in cards
    ) + "</div>"


def release_banner(decision: str, detail: str) -> str:
    normalized = decision.lower()
    style = normalized if normalized in {"approved", "blocked"} else "review"
    return (
        f'<section class="release-banner"><div class="label">Overall release decision</div>'
        f'<span class="value {text(style)}">{text(normalized)}</span>'
        f"<div>{text(detail)}</div></section>"
    )


def document(title: str, subtitle: str, body: str) -> str:
    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>{text(title)}</title><style>{CSS}</style></head>
<body><main><header><h1>{text(title)}</h1><div class="subtitle">{text(subtitle)}</div>
<div class="muted">Generated {generated}</div></header>{body}</main></body></html>"""


def paged_tables(header: str, rows: list[str], columns: int, *, page_size: int = 7) -> str:
    if not rows:
        return (
            f"<table>{header}<tbody><tr><td colspan='{columns}'>"
            "No findings were reported.</td></tr></tbody></table>"
        )
    tables = []
    total = len(rows)
    for offset in range(0, total, page_size):
        end = min(offset + page_size, total)
        continuation = (
            f"<div class='continuation'>Findings {offset + 1}-{end} of {total}</div>"
        )
        tables.append(
            f"<div class='table-page'>{continuation}<table>{header}<tbody>"
            + "".join(rows[offset:end])
            + "</tbody></table></div>"
        )
    return "".join(tables)


def config_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    results = report.get("Results")
    if not isinstance(results, list):
        raise ValueError("invalid Trivy configuration report: Results must be a list")
    findings: list[dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        target = str(result.get("Target") or "unknown")
        for item in result.get("Misconfigurations") or []:
            if not isinstance(item, dict) or str(item.get("Status") or "FAIL").upper() == "PASS":
                continue
            cause = item.get("CauseMetadata") if isinstance(item.get("CauseMetadata"), dict) else {}
            findings.append(
                {
                    "severity": severity(item.get("Severity")),
                    "id": str(item.get("ID") or "TRIVY-MISCONFIGURATION"),
                    "title": str(item.get("Title") or item.get("Message") or "Misconfiguration"),
                    "target": target,
                    "line": int(cause.get("StartLine") or 1),
                    "resolution": str(item.get("Resolution") or "Apply the scanner remediation and rescan."),
                    "reference": safe_url(item.get("PrimaryURL")),
                }
            )
    findings.sort(key=lambda item: (SEVERITY_ORDER[item["severity"]], item["id"], item["target"]))
    return findings


def render_config_report(report: dict[str, Any], policy: dict[str, Any]) -> str:
    findings = config_findings(report)
    counts = Counter(item["severity"] for item in findings)
    decision = str(policy.get("policy_decision") or "not_evaluated")
    blocking = int((policy.get("summary") or {}).get("blocking_findings") or 0)
    rows = []
    for item in findings:
        identifier = text(item["id"])
        if item["reference"]:
            identifier = f'<a href="{text(item["reference"])}">{identifier}</a>'
        rows.append(
            "<tr>"
            f'<td class="nowrap sev-{text(item["severity"].lower())}">{text(item["severity"])}</td>'
            f"<td>{identifier}</td><td>{text(item['title'])}</td>"
            f"<td><code>{text(item['target'])}:{item['line']}</code></td>"
            f"<td>{text(item['resolution'])}</td></tr>"
        )
    header = (
        "<thead><tr><th style='width:8%'>Severity</th><th style='width:13%'>ID</th>"
        "<th style='width:22%'>Finding</th><th style='width:20%'>Location</th>"
        "<th>Required remediation</th></tr></thead>"
    )
    table = paged_tables(header, rows, 5)
    body = (
        release_banner(
            "not_evaluated",
            "The image scan, consolidated deterministic decision, and protected approval have not run at this stage.",
        )
        + "<section><h2>Technical summary</h2>"
        f"<p>The deterministic pre-build configuration decision is "
        f'<strong class="decision {text(decision)}">{text(decision)}</strong>. '
        "HIGH and CRITICAL failures prevent the Docker build in the production workflow.</p>"
        + metric_cards(
            [
                ("Decision", decision, decision),
                ("Failed checks", len(findings), "review" if findings else "approved"),
                ("Blocking", blocking, "blocked" if blocking else "approved"),
                ("Medium", counts.get("MEDIUM", 0), "review"),
            ]
        )
        + "</section><section><h2>Configuration findings requiring action</h2>"
        "<p>Rows are ordered by scanner severity. Locations refer to the exact release configuration supplied to Trivy.</p>"
        + table
        + "</section><section><h2>Scope and methodology</h2>"
        "<p>Trivy statically evaluated the selected Dockerfile and any selected deployment manifest before image construction. "
        "The policy blocks failed HIGH or CRITICAL findings and fails closed if the report is invalid.</p></section>"
        "<section><h2>Limitations and robustness</h2><div class='notice'>Static analysis does not prove the runtime "
        "deployment is compliant. Admission controls and post-deployment validation remain necessary. Scanner severity is "
        "preserved and no agent can override the deterministic decision.</div></section>"
        "<section><h2>Recommended next steps</h2><ol><li>Remediate blocking findings at the reported source locations.</li>"
        "<li>Re-run the pre-build scan and confirm an approved machine-readable decision.</li>"
        "<li>Validate deployed resources with admission and runtime policy.</li></ol></section>"
        "<section><h2>Further questions</h2><p>Do production Kubernetes, Helm, Terraform, or Compose assets exist outside "
        "the currently selected scan directory? If so, add them to the pre-build scope.</p></section>"
    )
    return document(
        "Pre-build Misconfiguration Security Report",
        "Trivy configuration evidence and deterministic build policy",
        body,
    )


def sonar_rows(report: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = report.get(key)
    if not isinstance(value, list):
        raise ValueError(f"invalid Sonar report: {key} must be a list")
    return [item for item in value if isinstance(item, dict)]


def sonar_severity_style(value: Any) -> str:
    normalized = str(value or "UNKNOWN").upper()
    if normalized in {"BLOCKER", "CRITICAL", "HIGH"}:
        return "blocked"
    if normalized in {"MAJOR", "MEDIUM"}:
        return "review"
    return "approved"


def render_prebuild_report(
    sonar: dict[str, Any], config: dict[str, Any], policy: dict[str, Any]
) -> str:
    """Combine code analysis and configuration evidence before image construction."""
    issues = sonar_rows(sonar, "findings")
    hotspots = sonar_rows(sonar, "hotspots")
    misconfigurations = config_findings(config)
    quality_gate = sonar.get("quality_gate")
    sonar_status = (
        str(quality_gate.get("status") or "UNKNOWN")
        if isinstance(quality_gate, dict)
        else "UNKNOWN"
    )
    config_decision = str(policy.get("policy_decision") or "not_evaluated")
    blocking = int((policy.get("summary") or {}).get("blocking_findings") or 0)

    issue_table_rows = []
    for item in issues:
        location = str(item.get("component") or "unknown")
        if item.get("line"):
            location += f":{item['line']}"
        issue_table_rows.append(
            "<tr>"
            f'<td class="nowrap {text(sonar_severity_style(item.get("severity")))}">{text(item.get("severity"))}</td>'
            f"<td>{text(item.get('kind'))}</td><td>{text(item.get('rule'))}</td>"
            f"<td><code>{text(location)}</code></td><td>{text(item.get('message'))}</td>"
            f"<td>{text(item.get('status'))}</td></tr>"
        )
    issue_header = (
        "<thead><tr><th style='width:10%'>Severity</th><th style='width:10%'>Type</th>"
        "<th style='width:15%'>Rule</th><th style='width:20%'>Location</th>"
        "<th>Finding</th><th style='width:10%'>Status</th></tr></thead>"
    )

    hotspot_table_rows = []
    for item in hotspots:
        location = str(item.get("component") or "unknown")
        if item.get("line"):
            location += f":{item['line']}"
        hotspot_table_rows.append(
            "<tr>"
            f'<td class="nowrap {text(sonar_severity_style(item.get("severity")))}">{text(item.get("severity"))}</td>'
            f"<td>{text(item.get('rule'))}</td><td><code>{text(location)}</code></td>"
            f"<td>{text(item.get('message'))}</td><td>{text(item.get('status'))}</td></tr>"
        )
    hotspot_header = (
        "<thead><tr><th style='width:12%'>Priority</th><th style='width:18%'>Category</th>"
        "<th style='width:25%'>Location</th><th>Finding</th>"
        "<th style='width:14%'>Review status</th></tr></thead>"
    )

    config_table_rows = []
    for item in misconfigurations:
        identifier = text(item["id"])
        if item["reference"]:
            identifier = f'<a href="{text(item["reference"])}">{identifier}</a>'
        config_table_rows.append(
            "<tr>"
            f'<td class="nowrap sev-{text(item["severity"].lower())}">{text(item["severity"])}</td>'
            f"<td>{identifier}</td><td>{text(item['title'])}</td>"
            f"<td><code>{text(item['target'])}:{item['line']}</code></td>"
            f"<td>{text(item['resolution'])}</td></tr>"
        )
    config_header = (
        "<thead><tr><th style='width:9%'>Severity</th><th style='width:13%'>ID</th>"
        "<th style='width:22%'>Finding</th><th style='width:21%'>Location</th>"
        "<th>Required remediation</th></tr></thead>"
    )

    dashboard = safe_url(sonar.get("dashboard_url"))
    dashboard_link = (
        f'<p><a href="{text(dashboard)}">Open the complete analysis in SonarQube Cloud</a>.</p>'
        if dashboard
        else ""
    )
    prebuild_status = (
        "approved"
        if config_decision == "approved" and sonar_status == "OK"
        else "blocked"
    )
    body = (
        release_banner(
            "not_evaluated",
            "This pre-build report cannot authorize a release; image scanning and consolidated evaluation must still complete.",
        )
        + "<section><h2>Technical summary</h2>"
        f"<p>The combined pre-build status is <strong class='decision {text(prebuild_status)}'>{text(prebuild_status)}</strong>. "
        f"SonarQube reported a quality-gate status of <strong>{text(sonar_status)}</strong>, while the Trivy configuration "
        f"policy decision is <strong>{text(config_decision)}</strong>. On a protected release branch, either failed required "
        "gate prevents the image build. Non-publishing validation does not turn a failed scanner status into approval.</p>"
        + metric_cards(
            [
                ("Pre-build status", prebuild_status, prebuild_status),
                ("Sonar issues", len(issues), "review" if issues else "approved"),
                ("Security hotspots", len(hotspots), "review" if hotspots else "approved"),
                ("Blocking config", blocking, "blocked" if blocking else "approved"),
            ]
        )
        + "</section><section><h2>Source-code findings requiring attention</h2>"
        "<p>SonarQube findings are static-analysis results for the source revision selected by this workflow. "
        "Resolve code issues and review security hotspots before treating the code gate as satisfied.</p>"
        + dashboard_link
        + paged_tables(issue_header, issue_table_rows, 6)
        + "</section><section><h2>Security hotspots requiring review</h2>"
        "<p>Hotspots require a human security review; their presence is not automatically proof of a vulnerability.</p>"
        + paged_tables(hotspot_header, hotspot_table_rows, 5)
        + "</section><section><h2>Configuration findings blocking or qualifying the build</h2>"
        "<p>Trivy evaluated the exact Dockerfile and selected deployment configuration before image construction.</p>"
        + paged_tables(config_header, config_table_rows, 5)
        + "</section><section><h2>Scope and methodology</h2>"
        "<p>SonarQube analyzes source-code quality and security rules. Trivy independently evaluates Dockerfile and IaC "
        "configuration. The deterministic configuration policy fails closed on invalid evidence and blocks failed HIGH or "
        "CRITICAL misconfigurations.</p></section>"
        "<section><h2>Limitations and robustness</h2><div class='notice'>Static analysis cannot establish runtime "
        "reachability or deployed compliance. A stopped pipeline has no built image, so container vulnerability results do "
        "not exist yet. The final release policy and protected approval remain authoritative.</div></section>"
        "<section><h2>Recommended next steps</h2><ol><li>Fix every blocking configuration finding at its reported location.</li>"
        "<li>Resolve Sonar code issues and review security hotspots.</li><li>Re-run this pre-build stage until its required "
        "gates pass.</li><li>Only then build and scan the immutable container image.</li></ol></section>"
        "<section><h2>Further questions</h2><p>Are all production Dockerfiles, Kubernetes manifests, Helm charts, "
        "Terraform modules, and Compose files included in the selected pre-build scope?</p></section>"
    )
    return document(
        "Pre-build Code and Configuration Security Report",
        "SonarQube source analysis, Trivy misconfiguration evidence, and deterministic build policy",
        body,
    )


def image_findings(triage: dict[str, Any]) -> list[dict[str, Any]]:
    findings = triage.get("findings")
    if not isinstance(findings, list):
        raise ValueError("invalid sanitized image triage report: findings must be a list")
    return [
        item
        for item in findings
        if isinstance(item, dict)
        and str(item.get("kind") or "").lower() in {"vulnerability", "secret"}
    ]


def render_image_report(triage: dict[str, Any]) -> str:
    findings = image_findings(triage)
    summary = triage.get("summary") if isinstance(triage.get("summary"), dict) else {}
    decision = str(triage.get("policy_decision") or "not_evaluated")
    counts = Counter(severity(item.get("severity")) for item in findings)
    rows = []
    for item in findings:
        location = item.get("location") if isinstance(item.get("location"), dict) else {}
        rows.append(
            "<tr>"
            f"<td class='nowrap'>{text(item.get('exploitability_review_rank'))}</td>"
            f'<td class="nowrap sev-{text(severity(item.get("severity")).lower())}">{text(severity(item.get("severity")))}</td>'
            f"<td>{text(item.get('kind'))}</td><td>{text(item.get('id'))}</td>"
            f"<td>{text(item.get('component'))}</td>"
            f"<td>{text(item.get('installed_version'))}</td><td>{text(item.get('fixed_version'))}</td>"
            f"<td class='nowrap'>{'BLOCK' if item.get('policy_blocking') else 'review'}</td>"
            f"<td><code>{text(location.get('path'))}:{text(location.get('start_line'))}</code></td>"
            f"<td>{text(item.get('recommended_action'))}</td></tr>"
        )
    header = (
        "<thead><tr><th style='width:5%'>Rank</th><th style='width:9%'>Severity</th>"
        "<th style='width:8%'>Type</th><th style='width:11%'>ID</th><th style='width:10%'>Component</th>"
        "<th style='width:8%'>Installed</th><th style='width:8%'>Fixed</th><th style='width:6%'>Policy</th>"
        "<th style='width:12%'>Location</th><th>Required remediation</th></tr></thead>"
    )
    table = paged_tables(header, rows, 10)
    body = (
        release_banner(
            "not_evaluated",
            "This scoped image decision is not overall release approval; the consolidated report evaluates every required gate.",
        )
        + "<section><h2>Container scan decision</h2>"
        f"<p>The deterministic container release decision is <strong class='decision {text(decision)}'>{text(decision)}</strong>. "
        "This report is generated only from sanitized triage data; detected secret values are intentionally excluded.</p>"
        + metric_cards(
            [
                ("Decision", decision, decision),
                ("Findings", len(findings), "review" if findings else "approved"),
                ("Blocking", summary.get("policy_blocking_findings", 0), "blocked" if summary.get("policy_blocking_findings") else "approved"),
                ("High/Critical", counts.get("HIGH", 0) + counts.get("CRITICAL", 0), "blocked"),
            ]
        )
        + "</section><section><h2>Image findings requiring action</h2>"
        "<p>Rank is a deterministic review order based on severity, policy impact, fix availability, and stable scanner metadata; "
        "it does not prove runtime exploitability.</p>"
        + table
        + "</section><section><h2>Scope and methodology</h2><p>Trivy inspected the exact locally built release candidate for "
        "operating-system and application-package vulnerabilities and secret patterns. Findings were normalized before rendering.</p></section>"
        "<section><h2>Limitations and robustness</h2><div class='notice'>Image scanning establishes package and file evidence, "
        "not application reachability or runtime exposure. Secret match content is removed from this report. The final release "
        "policy—not the agent or this document—authorizes publication.</div></section>"
        "<section><h2>Recommended next steps</h2><ol><li>Upgrade packages with fixed versions and rebuild from a current base.</li>"
        "<li>Rotate any detected credential and remove it from image history.</li><li>Re-scan the rebuilt immutable image.</li>"
        "<li>Publish only when the deterministic decision and protected approval both pass.</li></ol></section>"
        "<section><h2>Further questions</h2><p>Are runtime reachability, compensating controls, registry rescanning, "
        "SBOM attestation, and deployed-digest verification covered by separate controls?</p></section>"
    )
    return document(
        "Container Image Security Report",
        f"Sanitized Trivy findings for {triage.get('artifact_name') or 'the release candidate'}",
        body,
    )


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def html_list(items: list[str], empty_message: str) -> str:
    if not items:
        return f"<p>{text(empty_message)}</p>"
    return "<ul>" + "".join(f"<li>{text(item)}</li>" for item in items) + "</ul>"


def render_consolidated_report(unified: dict[str, Any], agent: dict[str, Any]) -> str:
    """Render authoritative scanner decisions with a bounded AI advisory."""
    authority = unified.get("authority") if isinstance(unified.get("authority"), dict) else {}
    summary = unified.get("summary") if isinstance(unified.get("summary"), dict) else {}
    sonar = unified.get("code_scan") if isinstance(unified.get("code_scan"), dict) else {}
    triage = (
        unified.get("image_and_configuration_scan")
        if isinstance(unified.get("image_and_configuration_scan"), dict)
        else {}
    )
    code_findings = sonar_rows(sonar, "findings")
    hotspots = sonar_rows(sonar, "hotspots")
    container_findings = image_findings(triage)
    sonar_status = str(authority.get("sonar_quality_gate") or "UNKNOWN")
    policy_decision = str(authority.get("container_release_policy") or "not_evaluated")
    release_ready = bool(authority.get("overall_release_ready"))
    release_status = "approved" if release_ready else "blocked"
    agent_status = str(agent.get("agent_status") or "unavailable")
    agent_label = str(agent.get("agent_display_name") or "AI agent")
    agent_review = agent.get("review") if isinstance(agent.get("review"), dict) else {}

    decision_rows = [
        ("SonarQube code quality", sonar_status, "Source-code quality and security rules"),
        ("Trivy container release policy", policy_decision, "Vulnerabilities, secrets, and configuration"),
        (f"{agent_label} advisory", agent_status, "Non-authoritative prioritization and remediation guidance"),
        ("Overall deterministic release", release_status, "Requires every authoritative gate to pass"),
    ]
    decision_table = (
        "<table><thead><tr><th style='width:28%'>Control</th><th style='width:18%'>Status</th>"
        "<th>Meaning</th></tr></thead><tbody>"
        + "".join(
            f"<tr><td>{text(control)}</td><td><strong>{text(status)}</strong></td><td>{text(meaning)}</td></tr>"
            for control, status, meaning in decision_rows
        )
        + "</tbody></table>"
    )

    prioritized_rows = []
    for item in container_findings[:20]:
        prioritized_rows.append(
            "<tr>"
            f'<td class="nowrap sev-{text(severity(item.get("severity")).lower())}">{text(severity(item.get("severity")))}</td>'
            f"<td>{text(item.get('kind'))}</td><td>{text(item.get('id'))}</td>"
            f"<td>{text(item.get('component'))}</td>"
            f"<td>{'BLOCK' if item.get('policy_blocking') else 'review'}</td>"
            f"<td>{text(item.get('recommended_action'))}</td></tr>"
        )
    prioritized_header = (
        "<thead><tr><th style='width:9%'>Severity</th><th style='width:10%'>Type</th>"
        "<th style='width:14%'>ID</th><th style='width:18%'>Component</th>"
        "<th style='width:8%'>Policy</th><th>Required remediation</th></tr></thead>"
    )

    executive_summary = str(
        agent_review.get("executive_summary")
        or "The model-backed advisory was unavailable; deterministic scanner evidence remains authoritative."
    )
    risk_assessment = str(
        agent_review.get("risk_assessment")
        or "No model-backed risk assessment was produced for this run."
    )
    actions = string_list(agent_review.get("prioritized_actions"))
    attack_paths = string_list(agent_review.get("attack_paths"))
    verification_steps = string_list(agent_review.get("verification_steps"))
    limitations = string_list(agent_review.get("limitations"))

    body = (
        release_banner(
            release_status,
            "This is the combined deterministic result from every required scanner gate; protected human approval is still required before publishing.",
        )
        + "<section><h2>Decision basis</h2>"
        f"<p>The deterministic release status is <strong class='decision {text(release_status)}'>{text(release_status)}</strong>. "
        f"SonarQube reported <strong>{text(sonar_status)}</strong> and the Trivy release policy reported "
        f"<strong>{text(policy_decision)}</strong>. The {text(agent_label)} status is <strong>{text(agent_status)}</strong>; its output "
        "is advisory and cannot approve, reject, waive, or override either scanner gate.</p>"
        + metric_cards(
            [
                ("Release status", release_status, release_status),
                ("Code issues", len(code_findings), "review" if code_findings else "approved"),
                ("Security hotspots", len(hotspots), "review" if hotspots else "approved"),
                ("Container findings", len(container_findings), "review" if container_findings else "approved"),
            ]
        )
        + "</section><section><h2>Authoritative gates and advisory status</h2>"
        "<p>This matrix separates deterministic authorization from AI-assisted interpretation. "
        "<code>policy_decision: not_evaluated</code> is not approval.</p>"
        + decision_table
        + "</section><section><h2>Findings that drive release risk</h2>"
        f"<p>The combined evidence contains {text(summary.get('total_actionable_items', 0))} actionable items. "
        "The table shows up to the first 20 deterministic container findings in policy-prioritized order; detailed "
        "code/configuration and image reports remain the audit surfaces for complete finding lists.</p>"
        + paged_tables(prioritized_header, prioritized_rows, 6)
        + f"</section><section><h2>{text(agent_label)} advisory interpretation</h2>"
        f"<div class='notice'><strong>Agent status: {text(agent_status)}.</strong> {text(executive_summary)}</div>"
        f"<h3>Risk assessment</h3><p>{text(risk_assessment)}</p>"
        + "<h3>Prioritized actions</h3>"
        + html_list(actions, "No additional agent-prioritized actions were returned.")
        + "<h3>Potential attack paths</h3>"
        + html_list(attack_paths, "No additional attack paths were returned.")
        + "</section><section><h2>Scope and methodology</h2>"
        "<p>SonarQube supplies source-code findings and its quality-gate decision. Trivy supplies configuration, package "
        "vulnerability, and secret-detection evidence for the exact candidate. Deterministic scripts normalize findings and "
        f"enforce release policy before the {text(agent_label)} receives bounded, sanitized evidence.</p></section>"
        "<section><h2>Limitations and robustness</h2>"
        + html_list(
            limitations,
            "Static scanning does not establish runtime reachability, deployment compliance, or the absence of zero-day vulnerabilities.",
        )
        + "<p>The agent may be unavailable without invalidating completed deterministic scans. Scanner databases and "
        "Sonar rules can change over time, so the immutable image digest must be rescanned continuously.</p></section>"
        "<section><h2>Recommended verification before release</h2>"
        + html_list(
            verification_steps,
            "Re-run every required scanner and verify the protected approval against the same immutable image digest.",
        )
        + "</section><section><h2>Further questions</h2><p>Are provenance attestations, SBOM publication, registry "
        "rescanning, runtime controls, and deployed-digest verification enforced outside this workflow?</p></section>"
    )
    return document(
        "Consolidated Release Security Report",
        f"SonarQube, Trivy, deterministic policy, and bounded {text(agent_label)} advisory evidence",
        body,
    )


def find_chrome() -> str:
    for command in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(command)
        if found:
            return found
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    raise ValueError("Chrome or Chromium is required to generate PDF reports")


def print_pdf(html_path: Path, pdf_path: Path, expected_title: str) -> None:
    chrome = find_chrome()
    try:
        result = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path.resolve()}",
                html_path.resolve().as_uri(),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("Chrome PDF conversion timed out") from exc
    if result.returncode != 0 or not pdf_path.is_file() or pdf_path.stat().st_size < 1000:
        raise ValueError(f"Chrome PDF conversion failed: {result.stderr[-500:]}")
    pdf_bytes = pdf_path.read_bytes()
    if pdf_bytes[:5] != b"%PDF-" or b"%%EOF" not in pdf_bytes[-1024:]:
        raise ValueError("generated output is not a valid PDF document")
    if not re.search(rb"/Type\s*/Page\b", pdf_bytes):
        raise ValueError("generated PDF contains no page objects")
    if expected_title.encode("utf-8") not in pdf_bytes:
        raise ValueError("generated PDF does not contain the expected report title")
    inspector = shutil.which("pdfinfo")
    extractor = shutil.which("pdftotext")
    if inspector:
        metadata = subprocess.run(
            [inspector, str(pdf_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if metadata.returncode != 0 or not any(
            line.startswith("Pages:") and int(line.split(":", 1)[1]) > 0
            for line in metadata.stdout.splitlines()
        ):
            raise ValueError("generated PDF did not pass page-count verification")
    if extractor:
        extracted = subprocess.run(
            [extractor, str(pdf_path), "-"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if extracted.returncode != 0 or expected_title not in extracted.stdout:
            raise ValueError("generated PDF did not pass selectable-text verification")


def write_config_report() -> None:
    report = load_json(Path("reports/ci-config-trivy.json"))
    policy = load_json(Path("reports/ci-config-policy-decision.json"))
    rendered = render_config_report(report, policy)
    with open("reports/ci-misconfiguration-report.html", "w", encoding="utf-8") as output:
        output.write(rendered)
    print_pdf(
        Path("reports/ci-misconfiguration-report.html"),
        Path("reports/ci-misconfiguration-report.pdf"),
        "Pre-build Misconfiguration Security Report",
    )


def write_prebuild_report() -> None:
    sonar = load_json(Path("reports/ci-sonar.json"))
    config = load_json(Path("reports/ci-config-trivy.json"))
    policy = load_json(Path("reports/ci-config-policy-decision.json"))
    rendered = render_prebuild_report(sonar, config, policy)
    with open("reports/ci-prebuild-security-report.html", "w", encoding="utf-8") as output:
        output.write(rendered)
    print_pdf(
        Path("reports/ci-prebuild-security-report.html"),
        Path("reports/ci-prebuild-security-report.pdf"),
        "Pre-build Code and Configuration Security Report",
    )


def write_image_report() -> None:
    triage = load_json(Path("reports/ci-triage.json"))
    rendered = render_image_report(triage)
    with open("reports/ci-image-security-report.html", "w", encoding="utf-8") as output:
        output.write(rendered)
    print_pdf(
        Path("reports/ci-image-security-report.html"),
        Path("reports/ci-image-security-report.pdf"),
        "Container Image Security Report",
    )


def write_consolidated_report() -> None:
    unified = load_json(Path("reports/ci-unified-security.json"))
    agent_path = Path("reports/ci-agent-review.json")
    agent = (
        load_json(agent_path)
        if agent_path.is_file()
        else {"agent_status": "unavailable", "failure_category": "report_missing"}
    )
    rendered = render_consolidated_report(unified, agent)
    with open("reports/ci-consolidated-security-report.html", "w", encoding="utf-8") as output:
        output.write(rendered)
    print_pdf(
        Path("reports/ci-consolidated-security-report.html"),
        Path("reports/ci-consolidated-security-report.pdf"),
        "Consolidated Release Security Report",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "report_type", choices=("configuration", "prebuild", "image", "consolidated")
    )
    args = parser.parse_args()
    try:
        if args.report_type == "configuration":
            write_config_report()
        elif args.report_type == "prebuild":
            write_prebuild_report()
        elif args.report_type == "consolidated":
            write_consolidated_report()
        else:
            write_image_report()
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Generated sanitized {args.report_type} HTML and PDF reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
