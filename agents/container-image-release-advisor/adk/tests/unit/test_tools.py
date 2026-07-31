import json
import subprocess
from pathlib import Path

import pytest

from app import tools


@pytest.fixture
def scan_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("CONTAINER_HARDENING_SCAN_ROOT", str(tmp_path))
    return tmp_path


def test_rejects_path_outside_scan_root(scan_root: Path) -> None:
    result = tools.scan_with_trivy(str(scan_root.parent), "config")
    assert result["status"] == "error"
    assert "configured scan root" in result["error"]


def test_scan_uses_argument_list_and_normalizes_report(
    scan_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = scan_root / "Dockerfile"
    target.write_text("FROM scratch\n", encoding="utf-8")
    report = {
        "SchemaVersion": 2,
        "Results": [
            {
                "Target": "Dockerfile",
                "Misconfigurations": [
                    {
                        "ID": "DS-001",
                        "Severity": "HIGH",
                        "Status": "FAIL",
                        "Title": "Container runs as root",
                        "Resolution": "Add a non-root USER.",
                        "CauseMetadata": {"StartLine": 1},
                    }
                ],
            }
        ],
    }

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        assert command[:4] == ["trivy", "config", "--format", "json"]
        assert command[-2:] == ["--quiet", str(target)]
        assert kwargs["check"] is False
        assert kwargs["text"] is True
        assert "shell" not in kwargs
        assert "GOOGLE_API_KEY" not in kwargs["env"]
        output_path = Path(command[command.index("--output") + 1])
        output_path.write_text(json.dumps(report), encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setenv("GOOGLE_API_KEY", "must-not-reach-trivy")
    monkeypatch.setattr(tools.subprocess, "run", fake_run)
    result = tools.scan_with_trivy("Dockerfile", "config")

    assert result["status"] == "success"
    assert result["policy_decision"] == "not_evaluated"
    assert result["summary"]["severity_counts"]["HIGH"] == 1
    assert result["findings"][0]["id"] == "DS-001"
    assert result["findings"][0]["evidence"] == "Dockerfile, line 1"


def test_normalizer_correlates_root_and_writable_filesystem() -> None:
    report = {
        "Results": [
            {
                "Target": "deployment.yaml",
                "Misconfigurations": [
                    {
                        "ID": "KSV-001",
                        "Severity": "HIGH",
                        "Status": "FAIL",
                        "Title": "Container runs as root",
                    },
                    {
                        "ID": "KSV-002",
                        "Severity": "MEDIUM",
                        "Status": "FAIL",
                        "Title": "Root filesystem is not read-only",
                    },
                ],
            }
        ]
    }

    result = tools.normalize_trivy_report(report)

    assert result["correlations"] == [
        {
            "risk": "root-and-writable-filesystem",
            "severity": "HIGH",
            "finding_ids": ["KSV-001", "KSV-002"],
            "explanation": "Code execution could gain root privileges in a writable container, increasing persistence and tampering impact.",
        }
    ]


def test_report_loader_rejects_invalid_json(scan_root: Path) -> None:
    report_path = scan_root / "report.json"
    report_path.write_text("not json", encoding="utf-8")

    result = tools.analyze_trivy_report("report.json")

    assert result["status"] == "error"
    assert "valid JSON" in result["error"]


def test_reports_missing_trivy(scan_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = scan_root / "Dockerfile"
    target.write_text("FROM scratch\n", encoding="utf-8")

    def missing_trivy(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(tools.subprocess, "run", missing_trivy)

    result = tools.scan_with_trivy("Dockerfile", "config")

    assert result == {
        "status": "error",
        "scanner": "trivy",
        "error": "Trivy is not installed or is not on PATH.",
    }


def test_preserves_vulnerability_severity_and_fixed_version() -> None:
    report = {
        "Results": [
            {
                "Target": "requirements.txt",
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2026-0001",
                        "PkgName": "example-lib",
                        "InstalledVersion": "1.0",
                        "FixedVersion": "1.1",
                        "Severity": "CRITICAL",
                    }
                ],
            }
        ]
    }

    result = tools.normalize_trivy_report(report)
    finding = result["findings"][0]

    assert finding["severity"] == "CRITICAL"
    assert finding["fixed_version"] == "1.1"
    assert finding["resolution"] == "Upgrade example-lib from 1.0 to 1.1."
