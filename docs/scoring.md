# How entries are scored

Most agent lists stop at discovery. Infrastructure teams need more: whether a tool can perform write actions, whether it has approval gates, whether it preserves evidence, and whether it is stable enough to depend on. Every entry in [data/repos.yaml](../data/repos.yaml) records five dimensions, assessed from project documentation and exposed tool surfaces rather than marketing claims.

For the full validator-backed field list, category slugs, artifact types, maturity values, labels, and pre-submit commands, see the [catalog schema reference](catalog-schema.md).

## The five fields

| Field | Question it answers | How it is verified |
| --- | --- | --- |
| `action_level` | What kinds of actions can it perform? | Read the project's exposed tool list. Only query tools (`get`, `list`, `search`) means `read-only`. Suggesting changes for a human to execute means `proposal`. Any tool that mutates real state (`create`, `deploy`, `delete`, `sync`) means `write-capable` and the entry gets the `write` label. This classification does not prove the tool has access to a production environment. |
| `human_approval` | Does a human gate write actions? | Look for gates in the server (write tools disabled by default, dry-run modes, confirmation flags) or in the client (permission prompts). Server-side gates are stronger because they hold no matter which client connects. |
| `evidence_tracing` | Can you prove what it did afterward? | Check for audit logs, OpenTelemetry support, structured run records, or evaluation output. Scored `yes`, `partial`, or `none`. |
| `maturity` | How mature does the project appear? | Observable signals include vendor support status, API stability (GA versus alpha), and recent activity. A production-adjacent rating is curator judgment, not a production-readiness guarantee. The weekly audit automatically checks GitHub reachability and archived status. |
| `risk_notes` | What is the blast radius if it goes wrong? | Combines the above with what the tool connects to. Write-capable identity tooling is treated very differently from a read-only diagram generator. |

## How fields map to README labels

The text labels in the README catalog are shorthand for these fields: `write` maps to `action_level: write-capable`, `approval` to `human_approval: true`, `evidence` to tracing or eval evidence, and `prod`/`prototype` to `maturity`. The validator enforces the highest-risk mappings: write-capable rows must carry `write`, human-approval rows must carry `approval`, `evidence_tracing: yes` rows must carry `evidence`, `evidence` cannot be paired with `evidence_tracing: none` or `unknown`, and `maturity: prototype` rows must use `prototype` rather than `prod`. An `approval` label may represent a server-enforced gate, a client permission prompt, or another documented safety mechanism; consult the entry and upstream documentation to determine enforcement strength.

## Example: reading one entry

```yaml
- name: PagerDuty/pagerduty-mcp-server
  action_level: write-capable    # tools can create incidents and schedule overrides
  human_approval: true           # write tools ship disabled by default
  evidence_tracing: partial      # logs exist, but no structured trace guarantee
  maturity: production-adjacent  # official vendor server
  risk_notes: "Keep write tools disabled by default and require approval for changes."
```

Read as: safe to connect for incident context today, but flip on its write tools only after you have decided who approves an agent-created incident.

## What is automated and what is judgment

GitHub repository reachability and archived status are checked weekly by [scripts/audit_github_repos.py](../scripts/audit_github_repos.py). The audit records each repository's latest push timestamp but does not apply a freshness threshold, and it skips non-GitHub documentation links. Those links and all safety scores require curator review. Verify every entry against your own environment before connecting it to real infrastructure — [templates/agent-scorecard.md](../templates/agent-scorecard.md) is the full per-project checklist used for deep review.
