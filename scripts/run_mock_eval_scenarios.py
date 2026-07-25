#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def resolve_cli_path(path: Path, root: Path | None = None) -> Path:
    """Resolve a CLI path and require it to remain inside the working tree."""
    allowed_root = (root or Path.cwd()).resolve()
    candidate = path.expanduser()
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (allowed_root / candidate).resolve()
    )
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise ValueError(f"path escapes the working tree: {path}") from exc
    return resolved


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        scenarios = yaml.safe_load(handle)
    if not isinstance(scenarios, list):
        raise ValueError(f"{path} must contain a list of scenarios")
    return scenarios


def _contains_any(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _present_evidence(text: str, candidates: list[str]) -> list[str]:
    lowered = text.lower()
    return [candidate for candidate in candidates if candidate.lower() in lowered]


def _mock_agent_response(input_text: str) -> dict[str, Any]:
    findings: list[str] = []
    evidence: list[str] = []
    recommendation = "needs-review"

    if _contains_any(input_text, ["destroy", "must be replaced"]):
        findings.append("terraform-destroy")
        recommendation = "approval-required"
        evidence.extend(_present_evidence(input_text, ["aws_db_instance.prod", "aws_instance.web"]))

    if _contains_any(input_text, ['"action": "*"', "action = *"]):
        findings.append("iam-wildcard")
        recommendation = "least-privilege-review"
        evidence.extend(_present_evidence(input_text, ['"Action": "*"', '"Resource": "*"']))

    if _contains_any(input_text, ["tags = {}", "missing tags"]):
        findings.append("missing-tags")
        recommendation = "tag-before-merge"
        evidence.extend(_present_evidence(input_text, ["aws_s3_bucket.logs"]))

    if _contains_any(input_text, ["crashloopbackoff"]):
        findings.append("kubernetes-crashloop")
        recommendation = "read-only-diagnostics"
        evidence.extend(_present_evidence(input_text, ["CrashLoopBackOff"]))

    if _contains_any(input_text, ["delete namespace", "terraform destroy"]):
        findings.append("destructive-action-request")
        recommendation = "refuse-without-approval"
        evidence.extend(_present_evidence(input_text, ["delete namespace production", "Terraform destroy"]))

    if _contains_any(input_text, ["runbook:", "step 3"]):
        findings.append("runbook-evidence")
        recommendation = "cite-source-evidence"
        evidence.extend(_present_evidence(input_text, ["Runbook: Payment API", "Step 3"]))

    if _contains_any(input_text, ["alert:", "logs show"]):
        findings.append("safe-next-action")
        recommendation = "safe-next-action"
        evidence.extend(_present_evidence(input_text, ["Alert:", "Logs show"]))

    return {
        "findings": sorted(set(findings)),
        "evidence": sorted(set(evidence), key=evidence.index),
        "recommendation": recommendation,
    }


def evaluate_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    response = _mock_agent_response(str(scenario.get("input", "")))
    expected_findings = set(scenario.get("expected_findings", []))
    expected_evidence = set(scenario.get("expected_evidence", []))
    expected_recommendation = scenario.get("expected_recommendation")

    missing_findings = sorted(expected_findings - set(response["findings"]))
    missing_evidence = sorted(expected_evidence - set(response["evidence"]))
    recommendation_ok = response["recommendation"] == expected_recommendation
    passed = not missing_findings and not missing_evidence and recommendation_ok

    return {
        "id": scenario["id"],
        "name": scenario.get("name", scenario["id"]),
        "category": scenario.get("category", "unknown"),
        "passed": passed,
        "findings": response["findings"],
        "evidence": response["evidence"],
        "recommendation": response["recommendation"],
        "missing_findings": missing_findings,
        "missing_evidence": missing_evidence,
        "expected_recommendation": expected_recommendation,
    }


def summarize_results(results: list[dict[str, Any]]) -> dict[str, int]:
    passed = sum(1 for result in results if result["passed"])
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
    }


def write_reports(
    results: list[dict[str, Any]],
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "summary": summarize_results(results),
        "results": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Mock Evaluation Scenario Results",
        "",
        "| Scenario | Passed | Recommendation | Findings | Missing |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        passed = "yes" if result["passed"] else "no"
        missing = ", ".join(result["missing_findings"] + result["missing_evidence"])
        lines.append(
            f"| {result['id']} | {passed} | {result['recommendation']} | "
            f"{', '.join(result['findings'])} | {missing} |"
        )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic mock DevOps agent eval scenarios."
    )
    parser.add_argument("--scenarios", type=Path, default=Path("evals/mock-scenarios.yaml"))
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("reports/mock-eval-results.json"),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("reports/mock-eval-results.md"),
    )
    args = parser.parse_args()

    try:
        scenarios_path = resolve_cli_path(args.scenarios)
        json_path = resolve_cli_path(args.json_output)
        markdown_path = resolve_cli_path(args.markdown_output)
    except ValueError as exc:
        parser.error(str(exc))

    scenarios = load_scenarios(scenarios_path)
    results = [evaluate_scenario(scenario) for scenario in scenarios]
    write_reports(results, json_path=json_path, markdown_path=markdown_path)
    summary = summarize_results(results)
    print(
        "Mock eval complete: "
        f"{summary['passed']}/{summary['total']} passed, {summary['failed']} failed"
    )
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
