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
    / "evaluate_release.py"
)


def write_report(path: Path) -> None:
    path.write_text(json.dumps({"Results": []}), encoding="utf-8")


def run_policy(workspace: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=workspace,
        check=False,
        capture_output=True,
        text=True,
    )


def test_policy_accepts_reports_and_output_within_workspace(tmp_path: Path) -> None:
    write_report(tmp_path / "image.json")
    write_report(tmp_path / "config.json")

    result = run_policy(
        tmp_path,
        "--image-report",
        "image.json",
        "--config-report",
        "config.json",
        "--output",
        "reports/decision.json",
    )

    assert result.returncode == 0
    assert "PUSH APPROVED" in result.stdout
    decision = json.loads((tmp_path / "reports" / "decision.json").read_text())
    assert decision["publish_allowed"] is True


def test_policy_rejects_input_outside_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    write_report(tmp_path / "outside.json")
    write_report(workspace / "config.json")

    result = run_policy(
        workspace,
        "--image-report",
        "../outside.json",
        "--config-report",
        "config.json",
        "--output",
        "decision.json",
    )

    assert result.returncode == 2
    assert "path escapes workspace root" in result.stderr


def test_policy_rejects_output_outside_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    write_report(workspace / "image.json")
    write_report(workspace / "config.json")

    result = run_policy(
        workspace,
        "--image-report",
        "image.json",
        "--config-report",
        "config.json",
        "--output",
        "../decision.json",
    )

    assert result.returncode == 2
    assert "path escapes workspace root" in result.stderr
    assert not (tmp_path / "decision.json").exists()
