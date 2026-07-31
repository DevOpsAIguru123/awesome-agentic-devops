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


def confined_path(path: Path, workspace_root: Path) -> Path:
    """Resolve an input path and reject reads outside the current workspace."""
    try:
        resolved_root = workspace_root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
    except OSError as exc:
        raise ValueError(f"cannot resolve summary input {path}: {exc}") from exc
    if not resolved_path.is_relative_to(resolved_root) or not resolved_path.is_file():
        raise ValueError(f"summary input must be a workspace file: {path}")
    return resolved_path


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()  # NOSONAR - confined by main
    except OSError as exc:
        raise ValueError(f"cannot read summary input {path}: {exc}") from exc


def load_agent_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()  # NOSONAR - confined by main
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
) -> str:
    marker = "\n## Scoped scanner decisions"
    if marker not in consolidated:
        raise ValueError("consolidated summary is missing the scanner-decision section")
    decision, deterministic_content = consolidated.split(marker, 1)
    details_marker = "\n## Sonar code findings"
    if details_marker in deterministic_content:
        deterministic_summary, detailed_findings = deterministic_content.split(
            details_marker, 1
        )
    else:
        deterministic_summary = deterministic_content
        detailed_findings = ""

    artifact_lines = [
        "## Reports and audit evidence",
        "",
        "Downloadable human-readable reports and machine-readable evidence "
        "supporting the release decision.",
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

    sections = [
        decision.strip(),
        "\n".join(artifact_lines),
        "## Deterministic scanner summary\n\n"
        "### Scoped scanner decisions\n\n"
        + demote_agent_headings(deterministic_summary.strip()),
        demote_agent_headings(agent),
    ]
    if detailed_findings:
        sections.append(
            "## Detailed deterministic scanner findings\n\n"
            "### Sonar code findings\n\n"
            + demote_agent_headings(detailed_findings.strip())
        )
    return "\n\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consolidated-markdown", type=Path, required=True)
    parser.add_argument("--agent-markdown", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", required=True)
    for _, key, _ in ARTIFACTS:
        parser.add_argument(f"--{key}-artifact-url", default="")
    args = parser.parse_args()

    urls = {
        key: getattr(args, f"{key}_artifact_url") for _, key, _ in ARTIFACTS
    }
    try:
        workspace_root = Path.cwd()
        consolidated_path = confined_path(args.consolidated_markdown, workspace_root)
        agent_path = confined_path(args.agent_markdown, workspace_root)
        summary = render(
            load_text(consolidated_path),
            load_agent_text(agent_path),
            args.repository,
            args.run_id,
            urls,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
