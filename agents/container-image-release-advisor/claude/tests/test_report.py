from claude_container_hardening.report import render_markdown


def test_human_report_omits_model_attestation_details() -> None:
    result = {
        "requested_model": "claude-sonnet-5",
        "actual_models": ["claude-sonnet-5"],
        "model_verified": True,
        "agent_status": "completed",
        "policy_decision": "approved",
        "failure_category": None,
        "input": {
            "total_findings": 0,
            "returned_findings": 0,
            "truncated": False,
        },
        "review": {
            "executive_summary": "No findings require action.",
            "risk_assessment": "Low risk based on supplied evidence.",
            "prioritized_actions": [],
            "attack_paths": [],
            "verification_steps": [],
            "limitations": [],
        },
    }

    report = render_markdown(result)

    assert "Requested model" not in report
    assert "Anthropic-reported model" not in report
    assert "Model verified" not in report
    assert "**Agent status:** `completed`" in report
    assert "**Scoped deterministic policy decision:** `approved`" in report
