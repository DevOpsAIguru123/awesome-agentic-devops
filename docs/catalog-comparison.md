# Catalog comparison: awesome-agentic-devops vs. broad MCP indexes

This repository is intentionally not a generic list of every MCP server. Broad
indexes such as Archestra are useful discovery sources because they collect many
servers and machine-evaluate implementation details. `awesome-agentic-devops`
uses a narrower operator lens: DevOps, Cloud, SRE, Platform Engineering, MLOps,
Kubernetes, IaC, CI/CD, observability, security, and incident automation.

## What broad MCP indexes are good at

Broad catalogs help answer discovery questions:

- What MCP servers exist for a product or category?
- Is there a known local or remote endpoint?
- What command/env configuration does an MCP client need?
- Does a server appear to implement tools, prompts, resources, logging, OAuth,
  stdio, or Streamable HTTP?
- Are sensitive config fields required?
- What is the external quality/adoption signal?

These signals are useful inputs, but they are not enough for infrastructure
operators deciding whether to connect an agent to real systems.

## What this catalog adds

| Dimension | Broad MCP index | `awesome-agentic-devops` |
| --- | --- | --- |
| Scope | Broad, many domains | DevOps/SRE/Cloud/operator tools only |
| Entry policy | Discovery-first | Curated, official/vendor-backed first |
| Safety model | Generic quality score | `action_level`, `human_approval`, `evidence_tracing`, `risk_notes` |
| Blast radius | Usually implicit | Explicit operator notes and write-capable warnings |
| Trust posture | Mixed official/community | Official/vendor-backed preferred; community only with clear operator value |
| Useful for | Finding candidates | Deciding what is safe and useful for infra teams |

## How to use external catalogs responsibly

External evaluations should be treated as **signals**, not as acceptance criteria.
Before adding a candidate from a broad MCP index, verify:

1. **Official source or governance** — vendor org, foundation project, or clear
   maintainership.
2. **Reachability and freshness** — repo/docs reachable, not archived, recently
   maintained.
3. **Real tool surface** — actual MCP tools/resources/prompts or agent skills,
   not only marketing copy.
4. **Action level** — read-only, proposal-only, or write-capable.
5. **Credential handling** — OAuth/API key/token requirements, sensitive fields,
   and least-privilege guidance.
6. **Approval gates** — dry-run modes, write tools disabled by default, or client
   permission prompts.
7. **Evidence** — logs, audit trails, traces, run records, or eval outputs.
8. **Blast radius** — what production system could be changed if the agent is
   wrong or compromised.
9. **Fit** — whether it helps DevOps, SRE, Cloud, Platform, MLOps, Kubernetes,
   IaC, CI/CD, observability, security, or incident workflows.

## Candidate handling rules

- Do not import broad-catalog entries in bulk.
- Do not accept archived/deprecated repositories just because they have high
  historical adoption.
- Do not accept write-capable commercial tools without strong public trust
  evidence.
- Prefer official docs and first-party GitHub orgs over third-party summaries.
- Keep external quality scores separate from curator safety judgments.

## Useful external fields to consider later

If this repo ingests external evaluation signals, keep them separate from
`data/repos.yaml` curator fields. Good generated metadata includes:

```yaml
external_signals:
  quality_score: 80
  protocol_features:
    tools: true
    prompts: false
    resources: true
    logging: true
    stdio: true
    streamable_http: false
    oauth2: false
  setup:
    server_type: remote
    sensitive_config_fields: 2
    required_sensitive_config_fields: 1
```

This preserves the core rule: external indexes help with discovery; this catalog
makes the operator-grade acceptance decision.

## Example: why curator review matters

During a spot check of a broad MCP evaluation dataset, several entries needed
human review before any catalog action:

| Signal | Why curator review is needed |
| --- | --- |
| High quality score on an archived repo | Historical quality does not mean current operator suitability. |
| Official repo marked deprecated | Deprecated tools should be skipped or documented as legacy only. |
| Missing GitHub metadata | Stale scrape data can understate adoption or freshness. |
| Write-capable admin APIs | Need explicit approval gates, RBAC guidance, and audit expectations. |
| Sensitive config fields | Need no-secret-in-context guidance and least-privilege setup notes. |

## Bottom line

Use broad MCP catalogs as radar. Use `awesome-agentic-devops` as the curated
shortlist for operators who need safe, practical, trust-aware agent tooling.
