# How entries are scored

Most agent lists stop at discovery. Infrastructure teams need more: whether an agent can touch production, whether it has approval gates, whether it preserves evidence, and whether it is stable enough to depend on. Every entry in [data/repos.yaml](../data/repos.yaml) records five verifiable dimensions, assessed by reading each project's documentation and exposed tool surface — not its marketing.

## The five fields

| Field | Question it answers | How it is verified |
| --- | --- | --- |
| `action_level` | Can it touch production? | Read the project's exposed tool list. Only query tools (`get`, `list`, `search`) means `read-only`. Suggesting changes for a human to execute means `proposal`. Any tool that mutates real state (`create`, `deploy`, `delete`, `sync`) means `write-capable` and the entry gets ⚠️. |
| `human_approval` | Does a human gate write actions? | Look for gates in the server (write tools disabled by default, dry-run modes, confirmation flags) or in the client (permission prompts). Server-side gates are stronger because they hold no matter which client connects. |
| `evidence_tracing` | Can you prove what it did afterward? | Check for audit logs, OpenTelemetry support, structured run records, or evaluation output. Scored `yes`, `partial`, or `none`. |
| `maturity` | Is it stable enough to depend on? | Observable signals only: vendor support status, API stability (GA versus alpha), and recent activity. The audit script checks freshness and archived status automatically. |
| `risk_notes` | What is the blast radius if it goes wrong? | Combines the above with what the tool connects to. Write-capable identity tooling is treated very differently from a read-only diagram generator. |

## How fields map to README labels

The emoji labels in the README catalog are shorthand for these fields: ⚠️ maps to `action_level: write-capable`, 🛡️ to `human_approval: true`, 📊 to tracing or eval evidence, and 🟢/🟡 to `maturity`.

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

Link reachability, archived status, and freshness are checked automatically by [scripts/audit_github_repos.py](../scripts/audit_github_repos.py) and enforced in CI. The safety scores themselves are curator judgment from reviewing each project's docs and tool surface at the time of entry. Verify against your own environment before connecting anything to real infrastructure — [templates/agent-scorecard.md](../templates/agent-scorecard.md) is the full per-project checklist used for deep review.
