# Compliance Evidence for Agentic DevOps

This checklist turns an agent run into reviewable evidence for security, compliance, and production-readiness conversations. It is intentionally tool-agnostic so it can be used with MCP servers, coding-agent skills, Terraform reviewers, incident copilots, and platform agents.

## When to collect evidence

Collect evidence whenever an agent can see or influence production-like systems:

- Cloud accounts, Kubernetes clusters, CI/CD systems, source-control repositories, incidents, identity, secrets, costs, telemetry, or customer-impacting data.
- Any workflow scored as `action_level: write-capable` in `data/repos.yaml`.
- Any workflow that uses privileged tokens, organization-wide scopes, or broad read access.

## Minimum evidence packet

For each meaningful run, capture these fields in the PR, ticket, incident timeline, or runbook output:

| Field | What to capture | Why it matters |
| --- | --- | --- |
| Request | Human request, ticket, incident, or runbook step that authorized the run | Shows business context and intent |
| Agent/tool version | Agent client, MCP server, skill, plugin, image digest, or commit SHA | Makes the run reproducible |
| Identity boundary | User/service account, org/project/workspace/cluster, and permission mode | Proves least-privilege scoping |
| Data boundary | Repositories, namespaces, log indexes, cloud accounts, or datasets accessed | Shows what context was exposed |
| Commands/tools called | Tool names and important arguments with secrets redacted | Enables audit and troubleshooting |
| Evidence inputs | Plan snippets, logs, metrics, traces, policy results, docs, or links used | Separates evidence from model opinion |
| Proposed change | Diff, PR, Terraform plan, Kubernetes manifest, CI config, or runbook step | Keeps mutation reviewable before execution |
| Approval record | Approver, timestamp, and approval scope for any write action | Proves human-in-the-loop control |
| Result | What changed, what did not change, and validation output | Supports rollback and post-run review |
| Follow-ups | Risks, unresolved questions, rollback notes, and owners | Prevents silent operational debt |

## Redaction rules

Never store raw secrets in the evidence packet. Redact or omit:

- API keys, OAuth tokens, kubeconfigs, private keys, passwords, session cookies, and signing material.
- Customer data, payload samples, logs with PII, and confidential infrastructure details unless the storage location is approved for that data class.
- Full environment dumps. Prefer named variables with values removed, for example `AWS_PROFILE=<redacted>`.

Keep enough shape to review the run without exposing credentials, such as account aliases, resource IDs, PR links, policy IDs, or log query URLs with sensitive parameters removed.

## Write-action approval gate

Before an agent mutates anything, require an explicit approval record with:

1. The exact action being approved, not a broad blanket approval.
2. Blast radius: account/project/cluster/namespace/repository and affected service.
3. Expected validation: tests, policy checks, dry-run output, health checks, or monitoring signal.
4. Rollback owner and rollback path.
5. Expiry: one run, one PR, one incident, or a short time window.

If the approval cannot be recorded, keep the agent in read-only or proposal mode.

## Example evidence packet

```markdown
## Agent run evidence

- Request: INC-1042 — investigate elevated 5xx on checkout API
- Agent/tool version: grafana/mcp-grafana via Docker MCP Gateway profile `sre-readonly`, image digest `sha256:...`
- Identity boundary: Grafana service account `agent-sre-readonly`; org `prod-observability`; read-only datasource access
- Data boundary: dashboards `checkout-*`, Prometheus datasource, Loki index `checkout-prod`; no secrets requested
- Commands/tools called: `list_dashboards`, `query_prometheus`, `query_loki` with tokens redacted
- Evidence inputs: p95 latency panel link, Loki query URL, deploy SHA from dashboard annotation
- Proposed change: rollback PR link or runbook step only; no direct production mutation
- Approval record: not required; read-only investigation
- Result: suspected regression in deploy `abc123`; opened rollback recommendation in incident thread
- Follow-ups: app owner to confirm rollback; platform to add SLO alert annotation
```

## How this maps to catalog scoring

- `action_level`: determines whether an approval record is mandatory.
- `human_approval`: should cite the client, server, or workflow gate that records approval.
- `evidence_tracing`: should cite where logs, traces, eval outputs, audit logs, or run records are stored.
- `risk_notes`: should summarize the blast radius and the required evidence/approval controls.

Use this checklist when adding new catalog entries, building reference agents, and deciding whether an MCP integration is safe enough for production-adjacent use.
