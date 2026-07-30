import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).parents[2]
    / "examples"
    / "agentic-devops-portfolio"
    / "scripts"
    / "deliver_security_report.py"
)
spec = importlib.util.spec_from_file_location("deliver_security_report", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def report(ready: bool = False) -> dict[str, object]:
    return {
        "authority": {
            "overall_release_ready": ready,
            "sonar_quality_gate": "OK" if ready else "ERROR",
            "container_release_policy": "approved" if ready else "blocked",
        },
        "summary": {
            "sonar_open_issues": 13,
            "trivy_findings": 372,
            "trivy_policy_blocking": 74,
        },
    }


def test_blocked_report_remains_blocked() -> None:
    values = module.summary_values(report())

    assert values["decision"] == "BLOCKED"
    assert values["sonar_findings"] == 13
    assert values["trivy_findings"] == 372
    assert values["blocking_findings"] == 74


def test_ready_report_requires_human_approval() -> None:
    assert module.release_decision(report(ready=True)) == "HUMAN APPROVAL REQUIRED"


def test_discord_rejects_non_discord_destination() -> None:
    try:
        module.validate_discord_webhook("https://example.com/api/webhooks/1/token")
    except module.DeliveryError as exc:
        assert "not a valid Discord webhook" in str(exc)
    else:
        raise AssertionError("non-Discord webhook destination was accepted")


def test_discord_payload_disables_mentions(monkeypatch) -> None:
    captured = {}

    def fake_post(url, payload, *, headers=None):
        captured.update({"url": url, "payload": payload, "headers": headers})
        return {"id": "message-1"}

    monkeypatch.setattr(module, "post_json", fake_post)
    identifier = module.send_discord(
        webhook_url="https://discord.com/api/webhooks/1/token",
        values=module.summary_values(report()),
        agent_summary="Review @everyone and <script>alert(1)</script>",
        repository="example/project",
        ref_name="feature/security",
        sha="a" * 40,
        run_url="https://github.com/example/project/actions/runs/1",
        artifact_url="https://github.com/example/project/actions/runs/1/artifacts/2",
    )

    assert identifier == "message-1"
    assert captured["payload"]["allowed_mentions"] == {"parse": []}


def test_email_html_escapes_agent_summary() -> None:
    rendered = module.email_html(
        module.summary_values(report()),
        "<script>alert(1)</script>",
        repository="example/project",
        ref_name="feature/security",
        sha="a" * 40,
        run_url="https://github.com/example/project/actions/runs/1",
        artifact_url="",
    )

    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
