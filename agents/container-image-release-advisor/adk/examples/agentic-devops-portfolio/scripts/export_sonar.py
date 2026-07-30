#!/usr/bin/env python3
"""Export SonarQube Cloud analysis results as a normalized JSON report."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {"sonarcloud.io", "sonarqube.us"}
SEVERITY_ORDER = {"BLOCKER": 0, "CRITICAL": 1, "MAJOR": 2, "MINOR": 3, "INFO": 4}


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
        raise ValueError(f"expected an input file: {path}")
    return resolved_path


def read_properties(path: Path) -> dict[str, str]:
    properties: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            properties[key.strip()] = value.strip()
    return properties


def require_safe_server(server_url: str) -> str:
    parsed = urlparse(server_url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Sonar server must be an approved HTTPS SonarQube Cloud host")
    return server_url.rstrip("/") + "/"


class SonarClient:
    def __init__(self, server_url: str, token: str) -> None:
        self.server_url = require_safe_server(server_url)
        self.token = token

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = urljoin(self.server_url, endpoint.lstrip("/"))
        if params:
            url = f"{url}?{urlencode(params)}"
        request = Request(
            url,
            headers={"Authorization": f"Bearer {self.token}", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.load(response)
        except HTTPError as exc:
            raise ValueError(f"Sonar API {endpoint} returned HTTP {exc.code}") from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ValueError(f"Sonar API {endpoint} failed: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"Sonar API {endpoint} returned an invalid response")
        return payload


def analysis_params(pull_request: str, branch: str) -> dict[str, str]:
    if pull_request:
        return {"pullRequest": pull_request}
    if branch:
        return {"branch": branch}
    return {}


def effective_analysis_params(
    dashboard_url: str, pull_request: str, branch: str
) -> dict[str, str]:
    """Use only a branch context that Sonar actually created for the analysis."""
    query = parse_qs(urlparse(dashboard_url).query)
    if pull_request:
        return {"pullRequest": query.get("pullRequest", [pull_request])[0]}
    dashboard_branch = query.get("branch", [""])[0]
    if branch and dashboard_branch == branch:
        return {"branch": branch}
    return {}


def wait_for_analysis(client: SonarClient, ce_task_url: str, timeout: int) -> str:
    parsed_task = urlparse(ce_task_url)
    parsed_server = urlparse(client.server_url)
    if parsed_task.scheme != "https" or parsed_task.hostname != parsed_server.hostname:
        raise ValueError("compute-engine task URL does not match the Sonar server")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        request = Request(
            ce_task_url,
            headers={"Authorization": f"Bearer {client.token}", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.load(response)
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ValueError(f"could not read Sonar analysis status: {exc}") from exc
        task = payload.get("task", {}) if isinstance(payload, dict) else {}
        status = str(task.get("status", "UNKNOWN"))
        if status == "SUCCESS":
            return str(task.get("analysisId", ""))
        if status in {"FAILED", "CANCELED"}:
            raise ValueError(f"Sonar analysis ended with status {status}")
        time.sleep(2)
    raise ValueError("timed out waiting for Sonar analysis")


def fetch_pages(
    client: SonarClient,
    endpoint: str,
    params: dict[str, Any],
    result_key: str,
    *,
    maximum: int = 5000,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page = 1
    while len(rows) < maximum:
        payload = client.get(endpoint, {**params, "p": page, "ps": 500})
        batch = payload.get(result_key, [])
        if not isinstance(batch, list):
            raise ValueError(f"Sonar API {endpoint} omitted {result_key}")
        rows.extend(item for item in batch if isinstance(item, dict))
        paging = payload.get("paging", {})
        total = int(paging.get("total", len(rows))) if isinstance(paging, dict) else len(rows)
        if not batch or len(rows) >= total:
            break
        page += 1
    return rows[:maximum]


def normalize_issue(issue: dict[str, Any]) -> dict[str, Any]:
    impacts = issue.get("impacts") if isinstance(issue.get("impacts"), list) else []
    return {
        "id": str(issue.get("key", "unknown")),
        "kind": str(issue.get("type", "ISSUE")),
        "severity": str(issue.get("severity", "UNKNOWN")),
        "rule": str(issue.get("rule", "unknown")),
        "component": str(issue.get("component", "unknown")),
        "line": issue.get("line"),
        "message": str(issue.get("message", "No description supplied")),
        "status": str(issue.get("status", "UNKNOWN")),
        "clean_code_attribute": issue.get("cleanCodeAttribute"),
        "impacts": impacts,
    }


def normalize_hotspot(hotspot: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(hotspot.get("key", "unknown")),
        "kind": "SECURITY_HOTSPOT",
        "severity": str(hotspot.get("vulnerabilityProbability", "UNKNOWN")),
        "rule": str(hotspot.get("securityCategory", "security-hotspot")),
        "component": str(hotspot.get("component", "unknown")),
        "line": hotspot.get("line"),
        "message": str(hotspot.get("message", "Security hotspot requires review")),
        "status": str(hotspot.get("status", "TO_REVIEW")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-task", type=Path, required=True)
    parser.add_argument("--project-properties", type=Path, required=True)
    parser.add_argument("--pull-request", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    token = os.environ.get("SONAR_TOKEN", "")
    if not token:
        parser.error("SONAR_TOKEN is required")
    try:
        workspace_root = Path.cwd()
        report_task_path = confined_path(args.report_task, workspace_root, must_exist=True)
        properties_path = confined_path(
            args.project_properties, workspace_root, must_exist=True
        )
        task = read_properties(report_task_path)
        project = read_properties(properties_path)
        project_key = project["sonar.projectKey"]
        client = SonarClient(task["serverUrl"], token)
        analysis_id = wait_for_analysis(client, task["ceTaskUrl"], args.timeout)
        context = effective_analysis_params(
            task.get("dashboardUrl", ""), args.pull_request, args.branch
        )
        issues = fetch_pages(
            client,
            "/api/issues/search",
            {"componentKeys": project_key, "resolved": "false", **context},
            "issues",
        )
        hotspots = fetch_pages(
            client,
            "/api/hotspots/search",
            {"projectKey": project_key, **context},
            "hotspots",
        )
        quality_gate = client.get(
            "/api/qualitygates/project_status",
            {"projectKey": project_key, **context},
        ).get("projectStatus", {})
        measures_payload = client.get(
            "/api/measures/component",
            {
                "component": project_key,
                "metricKeys": (
                    "bugs,vulnerabilities,code_smells,security_hotspots,coverage,"
                    "duplicated_lines_density"
                ),
                **context,
            },
        )
        measure_rows = measures_payload.get("component", {}).get("measures", [])
        measures = {
            str(item.get("metric")): item.get("value")
            for item in measure_rows
            if isinstance(item, dict)
        }
        normalized_issues = [normalize_issue(item) for item in issues]
        normalized_issues.sort(
            key=lambda row: (SEVERITY_ORDER.get(row["severity"], 99), row["id"])
        )
        payload = {
            "schema_version": "sonar-security-export/v1",
            "source": "sonarqube-cloud",
            "project_key": project_key,
            "analysis_id": analysis_id,
            "analysis_context": context or {"default_branch": True},
            "dashboard_url": task.get("dashboardUrl"),
            "quality_gate": quality_gate,
            "measures": measures,
            "summary": {
                "open_issues": len(normalized_issues),
                "security_hotspots": len(hotspots),
            },
            "findings": normalized_issues,
            "hotspots": [normalize_hotspot(item) for item in hotspots],
        }
        Path("reports").mkdir(parents=True, exist_ok=True)
        with open("reports/ci-sonar.json", "w", encoding="utf-8") as output_file:
            json.dump(payload, output_file, indent=2)
            output_file.write("\n")
    except (KeyError, OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Exported {len(normalized_issues)} Sonar issues and {len(hotspots)} hotspots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
