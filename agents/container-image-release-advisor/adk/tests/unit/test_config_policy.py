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
    / "evaluate_config_policy.py"
)


def run_policy(workspace: Path, report: dict[str, object]) -> subprocess.CompletedProcess[str]:
    reports = workspace / "reports"
    reports.mkdir()
    (reports / "ci-config-trivy.json").write_text(
        json.dumps(report), encoding="utf-8"
    )
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=workspace,
        check=False,
        capture_output=True,
        text=True,
    )


def test_approves_nonblocking_configuration_findings(tmp_path: Path) -> None:
    result = run_policy(
        tmp_path,
        {
            "Results": [
                {
                    "Misconfigurations": [
                        {"ID": "CFG-LOW", "Severity": "LOW", "Status": "FAIL"},
                        {"ID": "CFG-PASS", "Severity": "HIGH", "Status": "PASS"},
                    ]
                }
            ]
        },
    )

    assert result.returncode == 0
    decision = json.loads(
        (tmp_path / "reports" / "ci-config-policy-decision.json").read_text()
    )
    assert decision["policy_decision"] == "approved"
    assert decision["build_allowed"] is True
    assert decision["summary"]["failed_misconfigurations"] == 1


def test_blocks_high_or_critical_configuration_findings(tmp_path: Path) -> None:
    result = run_policy(
        tmp_path,
        {
            "Results": [
                {
                    "Misconfigurations": [
                        {"ID": "CFG-HIGH", "Severity": "HIGH", "Status": "FAIL"},
                        {
                            "ID": "CFG-CRITICAL",
                            "Severity": "CRITICAL",
                            "Status": "FAIL",
                        },
                    ]
                }
            ]
        },
    )

    assert result.returncode == 1
    decision = json.loads(
        (tmp_path / "reports" / "ci-config-policy-decision.json").read_text()
    )
    assert decision["policy_decision"] == "blocked"
    assert decision["build_allowed"] is False
    assert decision["summary"]["blocking_findings"] == 2


def test_fails_closed_on_invalid_report(tmp_path: Path) -> None:
    result = run_policy(tmp_path, {"unexpected": []})

    assert result.returncode == 2
    assert "BUILD BLOCKED" in result.stderr
    assert not (
        tmp_path / "reports" / "ci-config-policy-decision.json"
    ).exists()
