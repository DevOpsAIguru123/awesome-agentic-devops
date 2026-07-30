from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

SCRIPT = (
    Path(__file__).parents[2]
    / "examples"
    / "agentic-devops-portfolio"
    / "scripts"
    / "render_security_report.py"
)


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("render_security_report", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_configuration_html_is_escaped_and_contains_required_sections() -> None:
    module = load_script()
    rendered = module.render_config_report(
        {
            "Results": [
                {
                    "Target": "Dockerfile<script>alert(1)</script>",
                    "Misconfigurations": [
                        {
                            "ID": "DS-0002",
                            "Title": "Do not run as root",
                            "Severity": "HIGH",
                            "Status": "FAIL",
                            "Resolution": "Add USER <app>",
                            "CauseMetadata": {"StartLine": 12},
                        }
                    ],
                }
            ]
        },
        {
            "policy_decision": "blocked",
            "summary": {"blocking_findings": 1},
        },
    )

    assert "Pre-build Misconfiguration Security Report" in rendered
    assert "Technical summary" in rendered
    assert "Scope and methodology" in rendered
    assert "Recommended next steps" in rendered
    assert "<script>alert(1)</script>" not in rendered
    assert "Dockerfile&lt;script&gt;" in rendered


def test_prebuild_html_combines_sonar_and_configuration_evidence() -> None:
    module = load_script()
    rendered = module.render_prebuild_report(
        {
            "quality_gate": {"status": "ERROR"},
            "dashboard_url": "https://sonarcloud.io/dashboard?id=portfolio",
            "findings": [
                {
                    "severity": "CRITICAL",
                    "kind": "VULNERABILITY",
                    "rule": "python:S9999",
                    "component": "portfolio:app.py<script>",
                    "line": 8,
                    "message": "Fix unsafe input",
                    "status": "OPEN",
                }
            ],
            "hotspots": [
                {
                    "severity": "HIGH",
                    "rule": "auth",
                    "component": "portfolio:app.py",
                    "line": 10,
                    "message": "Review authentication",
                    "status": "TO_REVIEW",
                }
            ],
        },
        {
            "Results": [
                {
                    "Target": "Dockerfile",
                    "Misconfigurations": [
                        {
                            "ID": "DS-0002",
                            "Title": "Do not run as root",
                            "Severity": "HIGH",
                            "Status": "FAIL",
                            "Resolution": "Add USER app",
                            "CauseMetadata": {"StartLine": 12},
                        }
                    ],
                }
            ]
        },
        {"policy_decision": "blocked", "summary": {"blocking_findings": 1}},
    )

    assert "Pre-build Code and Configuration Security Report" in rendered
    assert rendered.index("Overall release decision") < rendered.index("Technical summary")
    assert "not_evaluated" in rendered
    assert "combined pre-build status is <strong class='decision blocked'>blocked</strong>" in rendered
    assert "Source-code findings requiring attention" in rendered
    assert "Security hotspots requiring review" in rendered
    assert "Configuration findings blocking or qualifying the build" in rendered
    assert "Fix unsafe input" in rendered
    assert "DS-0002" in rendered
    assert "app.py&lt;script&gt;" in rendered
    assert "app.py<script>" not in rendered


def test_image_html_uses_sanitized_triage_without_secret_match_values() -> None:
    module = load_script()
    rendered = module.render_image_report(
        {
            "artifact_name": "portfolio:test",
            "policy_decision": "blocked",
            "summary": {"policy_blocking_findings": 1},
            "findings": [
                {
                    "exploitability_review_rank": 1,
                    "severity": "CRITICAL",
                    "kind": "secret",
                    "id": "private-key",
                    "component": "app/config.py",
                    "installed_version": "not applicable",
                    "fixed_version": "not applicable",
                    "policy_blocking": True,
                    "location": {"path": "app/config.py", "start_line": 4},
                    "recommended_action": "Rotate the credential.",
                    "Match": "DO-NOT-RENDER-SECRET",
                },
                {
                    "exploitability_review_rank": 2,
                    "severity": "HIGH",
                    "kind": "misconfiguration",
                    "id": "DS-0002",
                    "component": "Dockerfile",
                    "policy_blocking": True,
                    "location": {"path": "Dockerfile", "start_line": 1},
                    "recommended_action": "This belongs only in the pre-build report.",
                },
            ],
        }
    )

    assert "Container Image Security Report" in rendered
    assert rendered.index("Overall release decision") < rendered.index("Container scan decision")
    assert "not_evaluated" in rendered
    assert "private-key" in rendered
    assert "Rotate the credential" in rendered
    assert "DO-NOT-RENDER-SECRET" not in rendered
    assert "DS-0002" not in rendered
    assert "This belongs only in the pre-build report" not in rendered
    assert "secret values are intentionally excluded" in rendered


def test_consolidated_html_separates_agent_advice_from_policy_authority() -> None:
    module = load_script()
    rendered = module.render_consolidated_report(
        {
            "authority": {
                "sonar_quality_gate": "OK",
                "container_release_policy": "blocked",
                "overall_release_ready": False,
            },
            "summary": {"total_actionable_items": 1},
            "code_scan": {"findings": [], "hotspots": []},
            "image_and_configuration_scan": {
                "findings": [
                    {
                        "severity": "CRITICAL",
                        "kind": "vulnerability",
                        "id": "CVE-2099-0001",
                        "component": "openssl",
                        "policy_blocking": True,
                        "recommended_action": "Upgrade immediately",
                    }
                ]
            },
        },
        {
            "agent_display_name": "Claude Agent SDK",
            "agent_status": "completed",
            "review": {
                "executive_summary": "Treat scanner data as evidence <script>alert(1)</script>",
                "risk_assessment": "A critical package is present.",
                "prioritized_actions": ["Upgrade openssl"],
                "attack_paths": ["Package exploitation"],
                "verification_steps": ["Rebuild and rescan"],
                "limitations": ["Static evidence only"],
            },
        },
    )

    assert "Consolidated Release Security Report" in rendered
    assert rendered.index("Overall release decision") < rendered.index("Decision basis")
    assert "deterministic release status is <strong class='decision blocked'>blocked</strong>" in rendered
    assert "policy_decision: not_evaluated" in rendered
    assert "Claude Agent SDK advisory interpretation" in rendered
    assert "ADK advisory" not in rendered
    assert "Upgrade immediately" in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
    assert "<script>alert(1)</script>" not in rendered
