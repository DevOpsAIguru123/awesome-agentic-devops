from __future__ import annotations

import asyncio

import pytest

from app.agent import CiAgentReview, CiPriorityAction
from scripts.run_ci_agent import (
    agent_envelope,
    generate,
    render_markdown,
    validate_finding_ids,
)


def triage_payload(count: int = 3) -> dict[str, object]:
    findings = [
        {
            "triage_item_id": f"triage-{index:04d}",
            "id": f"CVE-2026-{index:04d}",
            "kind": "vulnerability",
            "severity": "HIGH",
            "component": f"package-{index}",
            "installed_version": "1.0",
            "fixed_version": "1.1",
            "policy_blocking": True,
            "scanner_status": "affected",
            "location": {"path": "Dockerfile", "start_line": 1},
            "secret_value": "must-never-reach-the-agent",
        }
        for index in range(1, count + 1)
    ]
    return {
        "policy_decision": "blocked",
        "summary": {"total_findings": count},
        "findings": findings,
    }


def test_agent_envelope_is_bounded_and_allowlisted() -> None:
    envelope = agent_envelope(triage_payload(3), max_findings=2)

    assert envelope["input_total_findings"] == 3
    assert envelope["input_returned_findings"] == 2
    assert envelope["input_truncated"] is True
    assert [finding["id"] for finding in envelope["findings"]] == [
        "CVE-2026-0001",
        "CVE-2026-0002",
    ]
    assert "secret_value" not in envelope["findings"][0]
    assert "must-never-reach-the-agent" not in str(envelope)


def test_missing_credentials_produce_non_authoritative_fallback(monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)

    result = asyncio.run(generate(triage_payload(), max_findings=2))

    assert result["agent_status"] == "unavailable"
    assert result["failure_category"] == "credentials_unavailable"
    assert result["agent_authoritative"] is False
    assert result["policy_decision"] == "blocked"
    assert result["policy_unchanged"] is True
    report = render_markdown(result)
    assert "cannot approve, reject" in report
    assert "not_evaluated` is not approval" in report


def test_rejects_agent_citations_outside_bounded_input() -> None:
    envelope = agent_envelope(triage_payload(1), max_findings=1)
    review = CiAgentReview(
        executive_summary="Review",
        risk_assessment="Risk",
        prioritized_actions=[
            CiPriorityAction(
                finding_ids=["CVE-INVENTED"],
                action="Action",
                rationale="Rationale",
                compatibility_impact="Impact",
            )
        ],
        attack_paths=[],
        verification_steps=[],
        limitations=[],
    )

    with pytest.raises(ValueError, match="outside the bounded input"):
        validate_finding_ids(review, envelope)
