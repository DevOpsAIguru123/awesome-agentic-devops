from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).parents[2]
    / "examples"
    / "agentic-devops-portfolio"
    / "scripts"
    / "aggregate_security_reports.py"
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_combines_code_hotspot_and_container_findings(tmp_path: Path) -> None:
    write_json(
        tmp_path / "sonar.json",
        {
            "quality_gate": {"status": "OK"},
            "dashboard_url": "https://sonarcloud.io/dashboard?id=portfolio",
            "findings": [
                {
                    "id": "code-1",
                    "kind": "VULNERABILITY",
                    "severity": "CRITICAL",
                    "rule": "python:S9999",
                    "component": "portfolio:app.py",
                    "line": 7,
                    "message": "Replace unsafe code | now",
                    "status": "OPEN",
                }
            ],
            "hotspots": [
                {
                    "id": "hotspot-1",
                    "severity": "HIGH",
                    "rule": "auth",
                    "component": "portfolio:app.py",
                    "line": 10,
                    "message": "Review authentication",
                    "status": "TO_REVIEW",
                }
            ],
        },
    )
    write_json(
        tmp_path / "trivy.json",
        {
            "policy_decision": "rejected",
            "findings": [
                {
                    "exploitability_review_rank": 1,
                    "severity": "HIGH",
                    "kind": "vulnerability",
                    "id": "CVE-2026-0001",
                    "component": "libexample",
                    "policy_blocking": True,
                    "recommended_action": "Upgrade libexample.",
                }
            ],
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--sonar-report",
            "sonar.json",
            "--trivy-report",
            "trivy.json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(
        (tmp_path / "reports" / "ci-unified-security.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["summary"]["total_actionable_items"] == 3
    assert report["summary"]["sonar_open_issues"] == 1
    assert report["summary"]["sonar_security_hotspots"] == 1
    assert report["summary"]["trivy_findings"] == 1
    assert report["authority"]["container_policy_authorized"] is False
    assert report["authority"]["overall_release_ready"] is False
    markdown = (tmp_path / "reports" / "ci-unified-security.md").read_text(
        encoding="utf-8"
    )
    assert "Sonar code findings" in markdown
    assert "CVE-2026-0001" in markdown
    assert "policy_decision: not_evaluated` is not approval" in markdown
    assert "Replace unsafe code &#124; now" in markdown


def test_clean_inputs_produce_explicit_zero_finding_report(tmp_path: Path) -> None:
    write_json(
        tmp_path / "sonar.json",
        {"quality_gate": {"status": "OK"}, "findings": [], "hotspots": []},
    )
    write_json(
        tmp_path / "trivy.json",
        {"policy_decision": "approved", "findings": []},
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--sonar-report",
            "sonar.json",
            "--trivy-report",
            "trivy.json",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(
        (tmp_path / "reports" / "ci-unified-security.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["summary"]["total_actionable_items"] == 0
    assert report["authority"]["container_policy_authorized"] is True
    assert report["authority"]["overall_release_ready"] is True
    markdown = (tmp_path / "reports" / "ci-unified-security.md").read_text(
        encoding="utf-8"
    )
    assert "No open Sonar code issues" in markdown
    assert "No Trivy vulnerability" in markdown
