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
    / "triage_trivy.py"
)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def run_triage(workspace: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    arguments = [
        sys.executable,
        str(SCRIPT),
        "--image-report",
        "image.json",
        "--config-report",
        "config.json",
        "--policy-report",
        "policy.json",
        "--dockerfile",
        "Dockerfile",
        "--json-output",
        "reports/triage.json",
        "--markdown-output",
        "reports/triage.md",
        "--sarif-output",
        "reports/trivy.sarif",
        *extra,
    ]
    return subprocess.run(
        arguments,
        cwd=workspace,
        check=False,
        capture_output=True,
        text=True,
    )


def test_triages_each_finding_without_exposing_secret_values(tmp_path: Path) -> None:
    write_json(
        tmp_path / "image.json",
        {
            "ArtifactName": "portfolio:test",
            "Results": [
                {
                    "Target": "portfolio:test (debian 13)",
                    "Vulnerabilities": [
                        {
                            "VulnerabilityID": "CVE-2026-0001",
                            "PkgName": "libexample",
                            "InstalledVersion": "1.0",
                            "FixedVersion": "1.1",
                            "Severity": "HIGH",
                            "Status": "fixed",
                            "PrimaryURL": "https://example.test/CVE-2026-0001",
                        }
                    ],
                    "Secrets": [
                        {
                            "RuleID": "private-key",
                            "Severity": "CRITICAL",
                            "Match": "DO-NOT-COPY-THIS-SECRET",
                        }
                    ],
                }
            ],
        },
    )
    write_json(
        tmp_path / "config.json",
        {
            "Results": [
                {
                    "Target": "Dockerfile",
                    "Misconfigurations": [
                        {
                            "ID": "DS-0002",
                            "Title": "Image user should not be root",
                            "Severity": "HIGH",
                            "Status": "FAIL",
                            "Resolution": "Add a non-root USER instruction.",
                            "CauseMetadata": {"StartLine": 12, "EndLine": 12},
                        }
                    ],
                }
            ]
        },
    )

    result = run_triage(tmp_path)

    assert result.returncode == 0, result.stderr
    triage_text = (tmp_path / "reports" / "triage.json").read_text()
    triage = json.loads(triage_text)
    assert triage["policy_decision"] == "not_evaluated"
    assert triage["summary"]["total_findings"] == 3
    assert [item["id"] for item in triage["findings"]] == [
        "private-key",
        "CVE-2026-0001",
        "DS-0002",
    ]
    assert "DO-NOT-COPY-THIS-SECRET" not in triage_text
    assert (
        "DO-NOT-COPY-THIS-SECRET"
        not in (tmp_path / "reports" / "triage.md").read_text()
    )
    assert (
        "not_evaluated` is not approval"
        in (tmp_path / "reports" / "triage.md").read_text()
    )

    sarif = json.loads((tmp_path / "reports" / "trivy.sarif").read_text())
    assert sarif["version"] == "2.1.0"
    assert len(sarif["runs"][0]["results"]) == 3
    assert sarif["runs"][0]["results"][0]["level"] == "error"


def test_clean_reports_produce_an_explicit_empty_report(tmp_path: Path) -> None:
    write_json(tmp_path / "image.json", {"Results": []})
    write_json(tmp_path / "config.json", {"Results": []})
    write_json(tmp_path / "policy.json", {"policy_decision": "approved"})

    result = run_triage(tmp_path)

    assert result.returncode == 0, result.stderr
    triage = json.loads((tmp_path / "reports" / "triage.json").read_text())
    assert triage["summary"]["total_findings"] == 0
    assert triage["findings"] == []
    assert "No Trivy vulnerability" in (tmp_path / "reports" / "triage.md").read_text()


def test_rejects_output_outside_workspace(tmp_path: Path) -> None:
    write_json(tmp_path / "image.json", {"Results": []})
    write_json(tmp_path / "config.json", {"Results": []})

    result = run_triage(
        tmp_path,
        "--json-output",
        "../triage.json",
    )

    assert result.returncode == 2
    assert "path escapes workspace root" in result.stderr
    assert not (tmp_path.parent / "triage.json").exists()
