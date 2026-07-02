# Terraform Plan Reviewer Agent - Gemini ADK

Status: scaffold only

## Goal

Build a Gemini ADK agent that reviews Terraform plan output and returns risk summary, security findings, estimated blast radius, approval recommendation, and next safe action.

## Why this framework

Gemini ADK is a strong target for repeatable cloud-agent workflows, especially GCP and GKE-adjacent tasks that can use Gemini credits, structured tools, and approval-aware orchestration.

## Inputs

- Terraform plan text or JSON.
- Optional GCP project/environment metadata.
- Optional organization policy requirements.
- Optional runbook or tagging standards.

## Outputs

- Operator-readable summary.
- Structured risk findings.
- Evidence references to plan resources.
- Approval recommendation.
- Suggested next safe action.

## Safety model

- Read-only plan review by default.
- Tool allowlist limited to parsing, validation, and policy lookup.
- No direct apply capability in the first implementation.
- Escalate to human approval for destroys, replacements, IAM broadening, public network exposure, or production changes.
- Redact secrets and sensitive variables before model context.

## Evaluation cases

- Detects Terraform destroy.
- Detects IAM wildcard.
- Detects missing labels or tags.
- Detects public ingress.
- Requires approval for production replacements.
- Cites plan evidence for each finding.

## Minimal implementation plan

1. Define the agent instruction and output schema.
2. Add a local parser tool for `terraform show -json`.
3. Add policy-check tool stubs that do not call cloud APIs.
4. Create eval fixtures for safe, risky, and destructive plans.
5. Run Gemini ADK locally with fixture-only inputs.

## Future work

- Add GCP-specific policy checks.
- Add Cloud Asset Inventory read-only integration.
- Add eval scoring for evidence quality.
- Compare Gemini ADK outputs against Claude Code and OpenAI Agents SDK implementations.
