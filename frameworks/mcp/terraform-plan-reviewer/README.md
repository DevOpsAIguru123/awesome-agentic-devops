# Terraform Plan Reviewer Agent - MCP

Status: scaffold only

## Goal

Expose Terraform plan review as an MCP server or MCP-compatible tool surface that agents can call safely.

## Why this framework

MCP is a good fit when the core need is a reusable tool boundary. A Terraform plan reviewer MCP server can accept plan artifacts, return structured findings, and keep agent clients away from direct infrastructure credentials.

## Inputs

- Terraform plan text or JSON.
- Optional policy bundle.
- Optional repository metadata.
- Optional runbook references.

## Outputs

- Structured findings resource.
- Markdown summary.
- Risk score.
- Approval recommendation.
- Evidence references.

## Safety model

- Server exposes read-only plan analysis tools.
- No `terraform apply` tool.
- Destructive findings require approval metadata in the response.
- Tool responses include evidence references.
- Secrets are rejected or redacted before analysis.

## Evaluation cases

- Detects Terraform destroy.
- Detects IAM wildcard.
- Detects missing tags.
- Detects unencrypted resource.
- Refuses apply-like tool requests.
- Produces cited safe next action.

## Minimal implementation plan

1. Define MCP tools: `analyze_plan`, `summarize_findings`, and `validate_policy`.
2. Add a parser that accepts `terraform show -json` output.
3. Return structured JSON findings plus markdown summary.
4. Add tests for tool responses.
5. Connect an agent client only after the server passes fixture tests.

## Future work

- Add a read-only Terraform state analyzer.
- Add policy bundle discovery.
- Add client examples for Claude Code, Gemini ADK, and OpenAI Agents SDK.
- Publish a tool-permission matrix.
