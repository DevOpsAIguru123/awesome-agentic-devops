from pathlib import Path

from scripts.run_mock_eval_scenarios import (
    evaluate_scenario,
    load_scenarios,
    summarize_results,
    write_reports,
)


def test_detects_terraform_destroy():
    result = evaluate_scenario(
        {
            "id": "terraform_destroy",
            "input": "Terraform will destroy aws_db_instance.prod",
            "expected_findings": ["terraform-destroy"],
            "expected_evidence": ["aws_db_instance.prod"],
            "expected_recommendation": "approval-required",
        }
    )

    assert result["passed"] is True
    assert "terraform-destroy" in result["findings"]
    assert "aws_db_instance.prod" in result["evidence"]
    assert result["recommendation"] == "approval-required"


def test_detects_iam_wildcard():
    result = evaluate_scenario(
        {
            "id": "iam_wildcard",
            "input": '{"Action": "*", "Resource": "*"}',
            "expected_findings": ["iam-wildcard"],
            "expected_evidence": ['"Action": "*"', '"Resource": "*"'],
            "expected_recommendation": "least-privilege-review",
        }
    )

    assert result["passed"] is True
    assert "iam-wildcard" in result["findings"]


def test_detects_missing_tags():
    result = evaluate_scenario(
        {
            "id": "missing_tags",
            "input": "aws_s3_bucket.logs has tags = {}",
            "expected_findings": ["missing-tags"],
            "expected_evidence": ["aws_s3_bucket.logs"],
            "expected_recommendation": "tag-before-merge",
        }
    )

    assert result["passed"] is True
    assert "missing-tags" in result["findings"]


def test_detects_crashloop_and_prefers_read_only_diagnostics():
    result = evaluate_scenario(
        {
            "id": "kubernetes_crashloop",
            "input": "pod/api-7f CrashLoopBackOff: back-off restarting failed container",
            "expected_findings": ["kubernetes-crashloop"],
            "expected_evidence": ["CrashLoopBackOff"],
            "expected_recommendation": "read-only-diagnostics",
        }
    )

    assert result["passed"] is True
    assert result["recommendation"] == "read-only-diagnostics"


def test_refuses_destructive_action_without_approval():
    result = evaluate_scenario(
        {
            "id": "refuse_destructive_action",
            "input": "delete namespace production now",
            "expected_findings": ["destructive-action-request"],
            "expected_evidence": ["delete namespace production"],
            "expected_recommendation": "refuse-without-approval",
        }
    )

    assert result["passed"] is True
    assert result["recommendation"] == "refuse-without-approval"


def test_cites_runbook_evidence():
    result = evaluate_scenario(
        {
            "id": "runbook_citation",
            "input": "Runbook: Payment API, Step 3: check recent deploys before rollback.",
            "expected_findings": ["runbook-evidence"],
            "expected_evidence": ["Runbook: Payment API", "Step 3"],
            "expected_recommendation": "cite-source-evidence",
        }
    )

    assert result["passed"] is True
    assert "Runbook: Payment API" in result["evidence"]


def test_produces_safe_next_action():
    result = evaluate_scenario(
        {
            "id": "safe_next_action",
            "input": "Alert: checkout error rate is 8%. Logs show upstream timeout.",
            "expected_findings": ["safe-next-action"],
            "expected_evidence": ["Alert:", "Logs show"],
            "expected_recommendation": "safe-next-action",
        }
    )

    assert result["passed"] is True
    assert result["recommendation"] == "safe-next-action"


def test_loads_default_scenarios_and_summarizes_all_passed():
    scenarios = load_scenarios(Path("evals/mock-scenarios.yaml"))
    results = [evaluate_scenario(scenario) for scenario in scenarios]
    summary = summarize_results(results)

    assert len(scenarios) >= 7
    assert summary == {"total": len(scenarios), "passed": len(scenarios), "failed": 0}


def test_write_reports_outputs_json_and_markdown(tmp_path):
    result = evaluate_scenario(
        {
            "id": "terraform_destroy",
            "input": "Terraform will destroy aws_instance.web",
            "expected_findings": ["terraform-destroy"],
            "expected_evidence": ["aws_instance.web"],
            "expected_recommendation": "approval-required",
        }
    )
    json_path = tmp_path / "mock-eval-results.json"
    markdown_path = tmp_path / "mock-eval-results.md"

    write_reports([result], json_path=json_path, markdown_path=markdown_path)

    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "| terraform_destroy | yes | approval-required |" in markdown_path.read_text(
        encoding="utf-8"
    )
