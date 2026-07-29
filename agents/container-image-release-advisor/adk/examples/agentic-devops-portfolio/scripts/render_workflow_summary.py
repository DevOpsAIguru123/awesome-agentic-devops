#!/usr/bin/env python3
"""Compose one ordered GitHub Actions summary with direct artifact links."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

ARTIFACTS = (
    ("Pre-build code and configuration report", "prebuild", "HTML and PDF"),
    ("Container image security report", "image", "HTML and PDF"),
    ("Consolidated release security report", "consolidated", "HTML, PDF, JSON, and Markdown"),
    ("SonarQube scan evidence", "sonar", "Normalized JSON"),
    ("Configuration scan evidence", "configuration", "Trivy JSON and policy decision"),
    ("Container scan evidence", "container", "Trivy JSON, SARIF, triage, and policy decision"),
    ("Claude advisory evidence", "agent", "Advisory JSON and Markdown"),
    ("Authorized image bundle", "bundle", "Scanned image archive and policy decision; retained for one day"),
)


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ValueError(f"cannot read summary input {path}: {exc}") from exc


def load_agent_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return "# Claude advisory\n\nThe optional advisory was unavailable. Deterministic policy remains authoritative."


def artifact_link(value: str, repository: str, run_id: str) -> str | None:
    parsed = urlparse(value)
    expected_prefix = f"/{repository}/actions/runs/{run_id}/artifacts/"
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or not parsed.path.startswith(expected_prefix)
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        return None
    return value


def demote_agent_headings(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            line = "### " + line[3:]
        elif line.startswith("# "):
            line = "## " + line[2:]
        lines.append(line)
    return "\n".join(lines)


def render(
    consolidated: str,
    agent: str,
    repository: str,
    run_id: str,
    artifact_urls: dict[str, str],
    diagnostic_mode: bool = False,
) -> str:
    marker = "\n## Scoped scanner decisions"
    if marker not in consolidated:
        raise ValueError("consolidated summary is missing the scanner-decision section")
    decision, findings = consolidated.split(marker, 1)

    artifact_lines = [
        "## Reports and audit evidence",
        "",
        "| Order | Artifact | Contents |",
        "| ---: | --- | --- |",
    ]
    for order, (label, key, contents) in enumerate(ARTIFACTS, 1):
        url = artifact_link(artifact_urls.get(key, ""), repository, run_id)
        artifact = f"[{label}]({url})" if url else f"{label} *(unavailable)*"
        artifact_lines.append(f"| {order} | {artifact} | {contents} |")

    run_url = f"https://github.com/{repository}/actions/runs/{run_id}#artifacts"
    artifact_lines.extend(["", f"[View all artifacts for this run]({run_url})"])

    diagnostic_notice = ""
    if diagnostic_mode:
        diagnostic_notice = (
            "> **Diagnostic evidence collection:** This pull-request demonstration "
            "continued code, configuration, image, and advisory analysis after a "
            "blocked pre-build gate. The blocked policy remained authoritative; "
            "approval, the authorized image bundle, and publishing stayed disabled."
        )

    return "\n\n".join(
        part
        for part in (
            decision.strip(),
            diagnostic_notice,
            "\n".join(artifact_lines),
            "## Deterministic scanner details\n\n" + findings.strip(),
            demote_agent_headings(agent),
        )
        if part
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consolidated-markdown", type=Path, required=True)
    parser.add_argument("--agent-markdown", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--diagnostic-mode",
        choices=("true", "false"),
        default="false",
        help="Mark a run that continued only to collect blocked-release evidence",
    )
    for _, key, _ in ARTIFACTS:
        parser.add_argument(f"--{key}-artifact-url", default="")
    args = parser.parse_args()

    urls = {
        key: getattr(args, f"{key}_artifact_url") for _, key, _ in ARTIFACTS
    }
    try:
        summary = render(
            load_text(args.consolidated_markdown),
            load_agent_text(args.agent_markdown),
            args.repository,
            args.run_id,
            urls,
            diagnostic_mode=args.diagnostic_mode == "true",
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
