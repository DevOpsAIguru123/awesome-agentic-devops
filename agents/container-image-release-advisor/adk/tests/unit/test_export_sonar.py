from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

SCRIPT = (
    Path(__file__).parents[2]
    / "examples"
    / "agentic-devops-portfolio"
    / "scripts"
    / "export_sonar.py"
)


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("export_sonar", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_analysis_context_prefers_pull_request() -> None:
    module = load_script()
    assert module.analysis_params("42", "feature") == {"pullRequest": "42"}
    assert module.analysis_params("", "main") == {"branch": "main"}
    assert module.analysis_params("", "") == {}


def test_effective_context_uses_the_dashboard_context() -> None:
    module = load_script()
    assert module.effective_analysis_params(
        "https://sonarcloud.io/dashboard?id=portfolio&pullRequest=42", "42", ""
    ) == {"pullRequest": "42"}
    assert module.effective_analysis_params(
        "https://sonarcloud.io/dashboard?id=portfolio&branch=feature", "", "feature"
    ) == {"branch": "feature"}
    assert module.effective_analysis_params(
        "https://sonarcloud.io/dashboard?id=portfolio", "", "feature"
    ) == {}


def test_rejects_non_sonar_and_non_https_servers() -> None:
    module = load_script()
    for url in ("http://sonarcloud.io", "https://example.com", "file:///tmp/report"):
        try:
            module.require_safe_server(url)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted unsafe Sonar URL: {url}")


def test_normalized_issue_excludes_unneeded_scanner_fields() -> None:
    module = load_script()
    normalized = module.normalize_issue(
        {
            "key": "issue-1",
            "type": "VULNERABILITY",
            "severity": "CRITICAL",
            "rule": "python:S9999",
            "component": "portfolio:app.py",
            "line": 12,
            "message": "Fix this",
            "status": "OPEN",
            "flows": [{"locations": [{"msg": "unbounded scanner detail"}]}],
        }
    )
    assert normalized["id"] == "issue-1"
    assert normalized["line"] == 12
    assert "flows" not in normalized
