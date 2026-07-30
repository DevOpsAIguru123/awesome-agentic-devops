#!/usr/bin/env python3
"""Deliver a sanitized consolidated release report through email and Discord."""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

RESEND_ENDPOINT = "https://api.resend.com/emails"
DISCORD_WEBHOOK_HOSTS = {
    "discord.com",
    "ptb.discord.com",
    "canary.discord.com",
    "discordapp.com",
}
MAX_ATTACHMENT_BYTES = 25 * 1024 * 1024


class DeliveryError(RuntimeError):
    """Safe delivery failure that never includes credentials or response bodies."""


def confined_path(path: Path, workspace_root: Path, *, must_exist: bool) -> Path:
    """Resolve a report path without allowing access outside the workspace."""
    try:
        root = workspace_root.resolve(strict=True)
        resolved = path.resolve(strict=must_exist)
    except OSError as exc:
        raise ValueError(f"cannot resolve report path {path}: {exc}") from exc
    if not resolved.is_relative_to(root):
        raise ValueError(f"report path escapes workspace: {path}")
    if must_exist and not resolved.is_file():
        raise ValueError(f"expected a report file: {path}")
    return resolved


def load_object(path: Path) -> dict[str, Any]:
    """Load one JSON object from a confined report path."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid report JSON from {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return payload


def text(value: Any, limit: int = 1_000) -> str:
    """Normalize untrusted report text and cap its delivery size."""
    normalized = " ".join(str(value or "Unavailable").split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def release_decision(report: dict[str, Any]) -> str:
    """Express deterministic readiness without claiming human approval."""
    authority = report.get("authority")
    if not isinstance(authority, dict):
        return "NOT EVALUATED"
    if authority.get("overall_release_ready") is True:
        return "HUMAN APPROVAL REQUIRED"
    if (
        authority.get("sonar_quality_gate") == "UNKNOWN"
        or authority.get("container_release_policy") == "not_evaluated"
    ):
        return "NOT EVALUATED"
    return "BLOCKED"


def advisory_summary(agent: dict[str, Any] | None) -> str:
    """Return only the bounded advisory executive summary, never raw findings."""
    if not isinstance(agent, dict) or agent.get("agent_status") != "completed":
        return "The optional agent advisory was unavailable; deterministic evidence remains authoritative."
    review = agent.get("review")
    if not isinstance(review, dict):
        return "The optional agent advisory was unavailable; deterministic evidence remains authoritative."
    return text(review.get("executive_summary"), 1_200)


def recipients(value: str) -> list[str]:
    """Parse a comma- or semicolon-separated recipient secret."""
    addresses = [item.strip() for item in re.split(r"[,;]", value) if item.strip()]
    if not 1 <= len(addresses) <= 50:
        raise DeliveryError("RESEND_TO_ADDRESS must contain between 1 and 50 recipients")
    return addresses


def validate_discord_webhook(value: str) -> str:
    """Allow only Discord's HTTPS execute-webhook endpoint."""
    parsed = urlparse(value)
    path_parts = [part for part in parsed.path.split("/") if part]
    if (
        parsed.scheme != "https"
        or parsed.hostname not in DISCORD_WEBHOOK_HOSTS
        or len(path_parts) < 4
        or path_parts[0] != "api"
        or path_parts[1] != "webhooks"
    ):
        raise DeliveryError("DISCORD_WEBHOOK_URL_DEVSECOPS is not a valid Discord webhook URL")
    return value


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """POST JSON and return a JSON object without exposing provider errors."""
    request_headers = {
        "Content-Type": "application/json",
        "User-Agent": "awesome-agentic-devops-report-delivery/1.0",
        **(headers or {}),
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(1_000_000)
    except urllib.error.HTTPError as exc:
        raise DeliveryError(f"provider returned HTTP {exc.code}") from None
    except (urllib.error.URLError, TimeoutError):
        raise DeliveryError("provider connection failed") from None
    if not body:
        return {}
    try:
        decoded = json.loads(body)
    except json.JSONDecodeError:
        return {}
    return decoded if isinstance(decoded, dict) else {}


def summary_values(report: dict[str, Any]) -> dict[str, Any]:
    """Select non-sensitive aggregate values for notifications."""
    summary = report.get("summary")
    authority = report.get("authority")
    summary = summary if isinstance(summary, dict) else {}
    authority = authority if isinstance(authority, dict) else {}
    return {
        "decision": release_decision(report),
        "sonar_gate": text(authority.get("sonar_quality_gate"), 40),
        "container_policy": text(authority.get("container_release_policy"), 40),
        "sonar_findings": int(summary.get("sonar_open_issues") or 0),
        "trivy_findings": int(summary.get("trivy_findings") or 0),
        "blocking_findings": int(summary.get("trivy_policy_blocking") or 0),
    }


def email_html(
    values: dict[str, Any],
    agent_summary: str,
    *,
    repository: str,
    ref_name: str,
    sha: str,
    run_url: str,
    artifact_url: str,
) -> str:
    """Render a compact, escaped email body."""
    color = "#b42318" if values["decision"] == "BLOCKED" else "#b54708"

    def safe(value: Any) -> str:
        return html.escape(text(value), quote=True)

    links = f'<a href="{safe(run_url)}">GitHub Actions run</a>'
    if artifact_url:
        links += f' · <a href="{safe(artifact_url)}">Consolidated report artifact</a>'
    return f"""<!doctype html>
<html><body style="font-family:Arial,sans-serif;color:#182230">
<h1>Consolidated Release Security Report</h1>
<p style="font-size:20px;color:{color}"><strong>{safe(values['decision'])}</strong></p>
<p><strong>Repository:</strong> {safe(repository)}<br>
<strong>Ref:</strong> {safe(ref_name)}<br>
<strong>Commit:</strong> {safe(sha[:12])}</p>
<table cellpadding="8" cellspacing="0" border="1" style="border-collapse:collapse">
<tr><th>Control</th><th>Result</th></tr>
<tr><td>SonarQube quality gate</td><td>{safe(values['sonar_gate'])}</td></tr>
<tr><td>Deterministic container policy</td><td>{safe(values['container_policy'])}</td></tr>
<tr><td>SonarQube findings</td><td>{values['sonar_findings']}</td></tr>
<tr><td>Trivy findings</td><td>{values['trivy_findings']}</td></tr>
<tr><td>Policy-blocking findings</td><td>{values['blocking_findings']}</td></tr>
</table>
<h2>Agent advisory summary</h2>
<p>{safe(agent_summary)}</p>
<p>{links}</p>
<p><em>Scanners produce evidence. Deterministic policy controls release. The agent is advisory and cannot override policy or human approval.</em></p>
</body></html>"""


def send_email(
    *,
    api_key: str,
    from_address: str,
    to_address: str,
    values: dict[str, Any],
    agent_summary: str,
    pdf_path: Path,
    repository: str,
    ref_name: str,
    sha: str,
    run_id: str,
    run_url: str,
    artifact_url: str,
) -> str | None:
    """Send the sanitized report and PDF through Resend."""
    attachment = pdf_path.read_bytes()
    if len(attachment) > MAX_ATTACHMENT_BYTES:
        raise DeliveryError("consolidated PDF exceeds the delivery size limit")
    payload = {
        "from": from_address,
        "to": recipients(to_address),
        "subject": f"[{values['decision']}] DevSecOps release report — {repository}",
        "html": email_html(
            values,
            agent_summary,
            repository=repository,
            ref_name=ref_name,
            sha=sha,
            run_url=run_url,
            artifact_url=artifact_url,
        ),
        "attachments": [
            {
                "content": base64.b64encode(attachment).decode("ascii"),
                "filename": "consolidated-release-security-report.pdf",
            }
        ],
        "tags": [{"name": "pipeline", "value": "container-release"}],
    }
    response = post_json(
        RESEND_ENDPOINT,
        payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Idempotency-Key": f"security-report-{run_id}",
        },
    )
    identifier = response.get("id")
    return str(identifier) if identifier else None


def send_discord(
    *,
    webhook_url: str,
    values: dict[str, Any],
    agent_summary: str,
    repository: str,
    ref_name: str,
    sha: str,
    run_url: str,
    artifact_url: str,
) -> str | None:
    """Post a mention-safe Discord embed with aggregate evidence only."""
    color = 0xD92D20 if values["decision"] == "BLOCKED" else 0xDC6803
    fields = [
        {"name": "SonarQube", "value": f"Gate: **{values['sonar_gate']}**\nFindings: **{values['sonar_findings']}**", "inline": True},
        {"name": "Trivy", "value": f"Policy: **{values['container_policy']}**\nFindings: **{values['trivy_findings']}**", "inline": True},
        {"name": "Policy blocking", "value": f"**{values['blocking_findings']}** findings", "inline": True},
        {"name": "Agent advisory", "value": text(agent_summary, 900), "inline": False},
    ]
    links = f"[Open workflow run]({run_url})"
    if artifact_url:
        links += f" · [Download consolidated report]({artifact_url})"
    payload = {
        "username": "DevSecOps Release Reporter",
        "allowed_mentions": {"parse": []},
        "embeds": [
            {
                "title": f"{values['decision']}: Consolidated Release Security Report",
                "url": run_url,
                "description": f"**{text(repository, 200)}** · `{text(ref_name, 100)}` · `{text(sha[:12], 20)}`",
                "color": color,
                "fields": fields,
                "footer": {"text": "Advisory delivery only — deterministic policy remains authoritative"},
            }
        ],
        "content": links,
    }
    validated_url = validate_discord_webhook(webhook_url)
    execute_url = validated_url + ("&" if "?" in validated_url else "?") + "wait=true"
    response = post_json(execute_url, payload)
    identifier = response.get("id")
    return str(identifier) if identifier else None


def channel_status(configured: bool) -> dict[str, Any]:
    return {"status": "pending" if configured else "not_configured"}


def render_delivery_summary(status: dict[str, Any]) -> str:
    """Render an Actions summary without addresses, webhook URLs, or API keys."""
    channels = status["channels"]
    lines = [
        "# Security report delivery",
        "",
        f"**Release decision delivered:** `{status['release_decision']}`",
        "",
        "| Channel | Provider | Status |",
        "| --- | --- | --- |",
        f"| Email | Resend | **{channels['email']['status']}** |",
        f"| Chat | Discord | **{channels['discord']['status']}** |",
        "",
        "> Report delivery is operational and non-authoritative. It cannot change "
        "scanner results, deterministic policy, human approval, or publishing.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--agent-report", type=Path)
    parser.add_argument("--pdf-report", type=Path, required=True)
    parser.add_argument("--status-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--ref-name", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--artifact-url", default="")
    args = parser.parse_args()

    root = Path.cwd()
    report_path = confined_path(args.report, root, must_exist=True)
    pdf_path = confined_path(args.pdf_report, root, must_exist=True)
    status_path = confined_path(args.status_output, root, must_exist=False)
    markdown_path = confined_path(args.markdown_output, root, must_exist=False)
    agent = None
    if args.agent_report and args.agent_report.exists():
        agent = load_object(confined_path(args.agent_report, root, must_exist=True))
    report = load_object(report_path)
    values = summary_values(report)
    agent_text = advisory_summary(agent)

    resend_api_key = os.getenv("RESEND_API_KEY", "")
    resend_from = os.getenv("RESEND_FROM_ADDRESS", "")
    resend_to = os.getenv("RESEND_TO_ADDRESS", "")
    discord_url = os.getenv("DISCORD_WEBHOOK_URL_DEVSECOPS", "")
    email_configured = bool(resend_api_key and resend_from and resend_to)
    discord_configured = bool(discord_url)
    status: dict[str, Any] = {
        "schema_version": "security-report-delivery/v1",
        "authoritative": False,
        "release_decision": values["decision"],
        "run_url": args.run_url,
        "channels": {
            "email": channel_status(email_configured),
            "discord": channel_status(discord_configured),
        },
    }

    failures = 0
    if email_configured:
        try:
            identifier = send_email(
                api_key=resend_api_key,
                from_address=resend_from,
                to_address=resend_to,
                values=values,
                agent_summary=agent_text,
                pdf_path=pdf_path,
                repository=args.repository,
                ref_name=args.ref_name,
                sha=args.sha,
                run_id=args.run_id,
                run_url=args.run_url,
                artifact_url=args.artifact_url,
            )
            status["channels"]["email"] = {"status": "delivered", "message_id": identifier}
        except (DeliveryError, OSError) as exc:
            failures += 1
            status["channels"]["email"] = {"status": "failed", "reason": text(exc, 120)}

    if discord_configured:
        try:
            identifier = send_discord(
                webhook_url=discord_url,
                values=values,
                agent_summary=agent_text,
                repository=args.repository,
                ref_name=args.ref_name,
                sha=args.sha,
                run_url=args.run_url,
                artifact_url=args.artifact_url,
            )
            status["channels"]["discord"] = {"status": "delivered", "message_id": identifier}
        except DeliveryError as exc:
            failures += 1
            status["channels"]["discord"] = {"status": "failed", "reason": text(exc, 120)}

    status_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_delivery_summary(status), encoding="utf-8")
    if failures:
        print(f"::warning::{failures} configured report delivery channel(s) failed")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
