# Awesome DevOps Cloud Agents

**Awesome DevOps Cloud Agents** is a curated map and build lab for DevOps, Cloud, SRE, and Platform Engineering agents across Claude Code, Gemini ADK, OpenAI Agents SDK, and MCP.

This repository evaluates which agents are safe, useful, and production-adjacent for infrastructure automation.

## Why this exists

Most agent lists stop at discovery. Infrastructure teams need more than discovery: they need to know whether an agent can touch production, whether it has approval gates, whether it preserves evidence, and whether it can be rebuilt as a safe reference workflow.

This repo is intentionally operator-grade. Each entry is scored by real infrastructure usefulness, operational risk, human approval gates, tracing/evidence, maturity, and Gemini compatibility.

## Who it is for

- DevOps and platform engineers evaluating AI automation.
- SREs designing incident-response copilots.
- Cloud engineers comparing agent frameworks.
- Security reviewers assessing infrastructure-agent risk.
- Builders creating portfolio-grade reference agents.
- Interview candidates who want a practical DevOps AI artifact.

## Safety-first disclaimer

These agents may touch infrastructure. Prefer read-only or proposal mode first. Require human approval before write actions. Never expose secrets to model context. Use least-privilege credentials, dry runs, Terraform plans before applies, and CI checks before merge.

## Evaluation labels

| Label | Meaning |
| --- | --- |
| 🟢 | production-adjacent OSS |
| 🟡 | useful prototype |
| 🔵 | MCP/server integration |
| 🛡️ | has approval/safety controls |
| 📊 | has tracing/evidence/evals |
| 💎 | Gemini-friendly workload |
| ⚠️ | write-capable; review before use |

## Categories

1. Terraform / IaC agents
2. Kubernetes troubleshooting and autopilot agents
3. CI/CD pipeline agents
4. SRE incident response agents
5. Observability and log-analysis agents
6. Cloud cost optimization agents
7. DevOps MCP servers
8. Agent skills, prompts, and runbooks
9. Safety, audit, approval, and evidence frameworks
10. Broad DevOps AI curated lists

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| Terraform generation and review | `talkops-ai/aws-orchestrator-agent`, `antonbabenko/terraform-skill` | Strong IaC workflow shape and a clear Gemini build opportunity. |
| Kubernetes triage | `talkops-ai/k8s-autopilot`, `truongnh1992/gke-sre-ai-agent` | Good candidates for read-only-first troubleshooting and approval-gated remediation. |
| CI/CD failure analysis | `talkops-ai/ci-copilot` | Useful proposal-mode workflow for pipeline repair. |
| SRE incident response | `agamm/awesome-ai-sre`, `mstrYoda/sre-ai-agent` | Good discovery and evaluation seeds for incident workflows. |
| MCP integration mapping | `rohitg00/awesome-devops-mcp-servers`, `aliyun/alibabacloud-devops-mcp-server` | Helps compare MCP tool surfaces and permission boundaries. |
| Safety and evidence | `vitas/evidra`, `BagelHole/DevOps-Security-Agent-Skills` | Useful references for traces, auditability, and refusal behavior. |

## Framework build lab

The build lab starts with one shared pattern: **Terraform Plan Reviewer Agent**.

Input: Terraform plan output.

Output: Risk summary, security findings, estimated blast radius, approval recommendation, and next safe action.

Scaffolds:

- [Claude Code Terraform Plan Reviewer](frameworks/claude-code/terraform-plan-reviewer/README.md)
- [Gemini ADK Terraform Plan Reviewer](frameworks/gemini-adk/terraform-plan-reviewer/README.md)
- [OpenAI Agents SDK Terraform Plan Reviewer](frameworks/openai-agents-sdk/terraform-plan-reviewer/README.md)
- [MCP Terraform Plan Reviewer](frameworks/mcp/terraform-plan-reviewer/README.md)

Supporting docs:

- [Framework comparison](docs/framework-comparison.md)
- [Safety model](docs/safety-model.md)
- [Curation strategy](docs/curation-strategy.md)

Templates:

- [Agent scorecard](templates/agent-scorecard.md)
- [Evaluation cases](templates/eval-cases.md)
- [Runbook agent spec](templates/runbook-agent-spec.md)

## Seed curated list

The source of truth is [data/repos.yaml](data/repos.yaml). The list below is a readable index of the seed entries.

### Terraform / IaC Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/aws-orchestrator-agent](https://github.com/talkops-ai/aws-orchestrator-agent) | 🟡 🛡️ 💎 ⚠️ | Treats IaC generation as a pipeline with validation and approval concerns. |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ 💎 | Terraform-specific skill material for plan review and module workflows. |

### Kubernetes Troubleshooting and Autopilot Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/k8s-autopilot](https://github.com/talkops-ai/k8s-autopilot) | 🟡 🛡️ 💎 ⚠️ | High-value candidate for read-only-first Kubernetes incident workflows. |

### CI/CD Pipeline Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/ci-copilot](https://github.com/talkops-ai/ci-copilot) | 🟡 🛡️ 💎 | Good bridge between developer productivity and deployment safety. |

### SRE Incident Response Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [agamm/awesome-ai-sre](https://github.com/agamm/awesome-ai-sre) | 🟡 💎 | Useful map of AI-for-SRE projects and automation patterns. |
| [truongnh1992/gke-sre-ai-agent](https://github.com/truongnh1992/gke-sre-ai-agent) | 🟡 📊 💎 | GCP-focused reference for Gemini-compatible SRE workflows. |
| [mstrYoda/sre-ai-agent](https://github.com/mstrYoda/sre-ai-agent) | 🟡 📊 💎 | Candidate for incident reasoning and hallucination-control evaluation. |

### Observability and Log-Analysis Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [alexkroman/ollychat](https://github.com/alexkroman/ollychat) | 🟡 📊 | Interesting if it preserves evidence links for operational chat and logs. |

### DevOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 💎 | Good source for MCP ecosystem mapping and candidate integrations. |
| [aliyun/alibabacloud-devops-mcp-server](https://github.com/aliyun/alibabacloud-devops-mcp-server) | 🔵 🟡 ⚠️ | Provider-specific MCP surface area that needs permission scoring. |

### Agent Skills, Prompts, and Runbooks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [agenticsorg/devops](https://github.com/agenticsorg/devops) | 🟡 💎 | Candidate source for reusable DevOps agent patterns. |
| [microsoft/azure-devops-skills](https://github.com/microsoft/azure-devops-skills) | 🟢 🛡️ 💎 | Structured skill pattern for Azure DevOps and platform tasks. |
| [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) | 🛡️ 🟡 💎 | Safety-oriented companion to IaC and Kubernetes agent entries. |

### Safety, Audit, Approval, and Evidence Frameworks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [vitas/evidra](https://github.com/vitas/evidra) | 📊 💎 | Relevant because production-adjacent agents need durable traces. |

### Broad DevOps AI Curated Lists

| Repo | Labels | Operator note |
| --- | --- | --- |
| [hammadhaqqani/awesome-devops-ai](https://github.com/hammadhaqqani/awesome-devops-ai) | 🟡 💎 | Broad entry point for DevOps AI discovery. |
| [NotHarshhaa/ai-platform-engineering-handbook](https://github.com/NotHarshhaa/ai-platform-engineering-handbook) | 🟡 💎 | Platform engineering context and learning material. |

## How to contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New entries should update [data/repos.yaml](data/repos.yaml), include a real operational use case, classify action level, and explain safety or approval behavior.

Run validation before opening a PR:

```bash
python scripts/validate_repos_yaml.py
pytest -q
```
