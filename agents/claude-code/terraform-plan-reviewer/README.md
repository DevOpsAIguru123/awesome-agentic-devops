# Terraform Plan Reviewer Agent - Claude Code

Status: scaffold only

## Goal

Review Terraform plan output and produce a practical operator summary: risk summary, security findings, estimated blast radius, approval recommendation, and next safe action.

## Why this framework

Claude Code is strong when the workflow lives in a repository: reading Terraform modules, editing policy checks, writing tests, and preparing reviewable git diffs.

## Inputs

- Terraform plan text or JSON.
- Terraform module path.
- Optional policy rules.
- Optional environment context such as dev, staging, or production.

## Outputs

- High-level risk summary.
- Resource creates, updates, replacements, and destroys.
- Security findings such as public exposure, broad IAM, or missing encryption.
- Estimated blast radius.
- Approval recommendation.
- Next safe action.

## Safety model

- Read plan output only by default.
- Do not run `terraform apply`.
- Flag destructive changes and broad IAM.
- Require human approval before any mutating command.
- Preserve evidence by citing resource addresses and plan excerpts.

## Evaluation cases

- Detects Terraform destroy.
- Detects IAM wildcard.
- Detects missing tags.
- Detects public ingress.
- Refuses apply without approval.
- Produces safe next action.

## Minimal implementation plan

1. Add sample Terraform plans under `examples/`.
2. Create a plan parser that extracts resource actions and risky policy snippets.
3. Add a Claude Code prompt or command that summarizes parsed findings.
4. Add pytest cases for parser behavior.
5. Add a PR-comment output mode.

## Future work

- Parse `terraform show -json` output.
- Add OPA or Conftest policy integration.
- Add cost and compliance scoring.
- Add inline PR comments for high-risk resources.
