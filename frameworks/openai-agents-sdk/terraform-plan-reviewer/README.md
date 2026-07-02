# Terraform Plan Reviewer Agent - OpenAI Agents SDK

Status: scaffold only

## Goal

Create an OpenAI Agents SDK implementation that reviews Terraform plan output and returns a structured infrastructure risk assessment.

## Why this framework

OpenAI Agents SDK is a good fit for tool-using agents with tracing, guardrails, and evals. The plan reviewer can be built as a proposal-mode agent with deterministic parser tools and explicit approval policies.

## Inputs

- Terraform plan text or JSON.
- Policy configuration.
- Environment metadata.
- Optional repository standards.

## Outputs

- Risk summary.
- Security findings.
- Blast-radius estimate.
- Approval recommendation.
- Next safe action.
- Traceable evidence for each finding.

## Safety model

- Parser and policy tools only in the first version.
- No write tools.
- Explicit guardrail against `terraform apply`.
- Approval handoff for destructive or privileged changes.
- Tracing enabled for tool calls and evidence capture.

## Evaluation cases

- Detects Terraform destroy.
- Detects IAM wildcard.
- Detects missing tags.
- Detects high-risk replacement.
- Refuses destructive action without approval.
- Separates evidence from inference.

## Minimal implementation plan

1. Define a plan-review agent with a structured output type.
2. Implement local parser and policy-check tools.
3. Add sample plans and pytest fixtures.
4. Add eval cases for risky and safe plans.
5. Emit a markdown PR-comment summary.

## Future work

- Add tracing-backed scorecards.
- Add policy-as-code integrations.
- Add multi-agent split between parser, security reviewer, and operator summarizer.
- Add CI workflow for regression evals.
