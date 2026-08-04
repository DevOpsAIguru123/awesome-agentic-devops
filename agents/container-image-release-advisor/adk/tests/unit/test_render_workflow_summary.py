import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).parents[2]
    / "examples"
    / "agentic-devops-portfolio"
    / "scripts"
    / "render_workflow_summary.py"
)
spec = importlib.util.spec_from_file_location("render_workflow_summary", SCRIPT)
assert spec is not None
assert spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_summary_has_stable_section_and_artifact_order() -> None:
    repository = "example/project"
    run_id = "123"
    urls = {
        key: f"https://github.com/{repository}/actions/runs/{run_id}/artifacts/{index}"
        for index, (_, key, _) in enumerate(module.ARTIFACTS, 1)
    }
    consolidated = """# Unified report

## Overall release decision

**APPROVED**

## Scoped scanner decisions

- Sonar: OK

## Executive summary

13 code findings and 372 container findings.

## Sonar code findings

| Finding |
| --- |
| Example |
"""
    agent = """# Claude review

## Executive summary

Advisory only.
"""

    summary = module.render(consolidated, agent, repository, run_id, urls)

    assert summary.index("## Overall release decision") < summary.index(
        "## Reports and audit evidence"
    )
    assert "machine-readable evidence supporting the release decision" in summary
    assert summary.index("## Reports and audit evidence") < summary.index(
        "## Deterministic scanner summary"
    )
    assert summary.index("## Deterministic scanner summary") < summary.index(
        "## Claude review"
    )
    assert summary.index("## Claude review") < summary.index(
        "## Detailed deterministic scanner findings"
    )
    assert summary.index("Pre-build code and configuration report") < summary.index(
        "Container image security report"
    )
    assert summary.index("Container image security report") < summary.index(
        "Consolidated release security report"
    )
    assert "### Executive summary" in summary


def test_external_artifact_url_is_not_linked() -> None:
    summary = module.render(
        "# Report\n\n## Scoped scanner decisions\n\nDetails",
        "# Agent\n\nAdvisory",
        "example/project",
        "123",
        {"prebuild": "https://evil.example/artifact.zip"},
    )

    assert "evil.example" not in summary
    assert "Pre-build code and configuration report *(unavailable)*" in summary


def test_missing_optional_agent_report_has_clear_fallback(tmp_path: Path) -> None:
    agent = module.load_agent_text(tmp_path / "missing-agent.md")

    assert "optional advisory was unavailable" in agent
    assert "Deterministic policy remains authoritative" in agent
