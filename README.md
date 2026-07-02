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
7. DevOps / Cloud automation agents
8. Incident response agents
9. DevOps MCP servers
10. Agent skills, prompts, and runbooks
11. Safety, audit, approval, and evidence frameworks
12. Broad DevOps AI curated lists

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| Terraform generation and review | `talkops-ai/aws-orchestrator-agent`, `antonbabenko/terraform-skill` | Strong IaC workflow shape and a clear Gemini build opportunity. |
| Kubernetes triage | `talkops-ai/k8s-autopilot`, `truongnh1992/gke-sre-ai-agent` | Good candidates for read-only diagnostics, evidence-cited troubleshooting, and approval-gated remediation patterns. |
| CI/CD pipeline generation | `talkops-ai/ci-copilot` | Useful workflow for pipeline generation, validation, and PR-based review. |
| SRE incident response | `agamm/awesome-ai-sre`, `stevancris/sre-ai-agent` | Good discovery and evaluation seeds for incident workflows. |
| DevOps/cloud automation | `agenticsorg/devops`, `Techikrish/OpsAgents` | Good candidates for extracting broad platform-agent patterns. |
| Incident-response evals | `Venkata-Manoj/Resilience-Ops-Env`, `NikhilRaman12/Incident-Renponse-Env` | Useful for synthetic incident-response evaluation without live infrastructure. |
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

## Curated catalog

The source of truth is [data/repos.yaml](data/repos.yaml). The list below is a readable index of the current 41 research-backed entries.

### Terraform / IaC Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/aws-orchestrator-agent](https://github.com/talkops-ai/aws-orchestrator-agent) | 🟡 🛡️ 💎 ⚠️ | Treats IaC generation as a pipeline with validation and approval concerns. |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ 💎 | Terraform-specific skill material for plan review and module workflows. |
| [SrikanthBommadi/Aws-terraform-llm-agent](https://github.com/SrikanthBommadi/Aws-terraform-llm-agent) | 🟡 💎 ⚠️ | AWS Terraform generation candidate with write-capable behavior that needs strict approval gates. |
| [shan5a6/iac-ai-agent](https://github.com/shan5a6/iac-ai-agent) | 🟡 💎 | Stub-level IaC candidate; verify scope before use. |
| [lindazhang2000/iac-ai-agents](https://github.com/lindazhang2000/iac-ai-agents) | 🟡 🛡️ 📊 💎 ⚠️ | Azure IaC multi-agent pattern with ServiceNow intake, PR workflow, human merge, Terraform apply, and verification evidence. |
| [MrCaptainDartz/iac-ai-agent](https://github.com/MrCaptainDartz/iac-ai-agent) | 🟡 | Adds Proxmox/homelab IaC template coverage, not a full agent framework. |

### Kubernetes Troubleshooting and Autopilot Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/k8s-autopilot](https://github.com/talkops-ai/k8s-autopilot) | 🟡 🛡️ 📊 💎 ⚠️ | High-value candidate for read-only-first Kubernetes incident workflows. |
| [truongnh1992/gke-sre-ai-agent](https://github.com/truongnh1992/gke-sre-ai-agent) | 🟡 🛡️ 📊 💎 | Strong Gemini/MCP reference for read-only, evidence-cited GKE troubleshooting. |
| [mstrYoda/sre-ai-agent](https://github.com/mstrYoda/sre-ai-agent) | 🟡 💎 ⚠️ | Kubernetes troubleshooting/healing candidate that needs safety-gate scrutiny. |
| [siloed-project/sre-ai-agent](https://github.com/siloed-project/sre-ai-agent) | 🟡 🛡️ 📊 💎 | Read-only Kubernetes diagnosis/reporting candidate with useful evidence-quality evaluation surface. |
| [andreistefanciprian/sre-ai-agent](https://github.com/andreistefanciprian/sre-ai-agent) | 🟡 📊 💎 ⚠️ | Converts Kubernetes findings into trackable GitHub work. |

### CI/CD Pipeline Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [talkops-ai/ci-copilot](https://github.com/talkops-ai/ci-copilot) | 🟡 🛡️ 📊 💎 ⚠️ | Pipeline generation and validation agent with PR-based review concerns. |

### DevOps / Cloud Automation Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [agenticsorg/devops](https://github.com/agenticsorg/devops) | 🟡 💎 ⚠️ | Candidate source for reusable OpenAI Agents SDK DevOps automation patterns. |
| [Yash-Kavaiya/Devops-AI-Agents](https://github.com/Yash-Kavaiya/Devops-AI-Agents) | 🟡 💎 | GCP Terraform workflow automation candidate built around Strands Agents and Gemini. |
| [Techikrish/OpsAgents](https://github.com/Techikrish/OpsAgents) | 🟡 🛡️ 📊 💎 ⚠️ | Beta LangGraph suite with HITL/write-capable DevOps/cloud patterns. |
| [rathodkunj2005/Minute0](https://github.com/rathodkunj2005/Minute0) | 🟡 🛡️ 📊 💎 ⚠️ | Vercel deployment monitoring agent with Slack approval and GitHub PR/merge workflow. |

### SRE Incident Response Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [agamm/awesome-ai-sre](https://github.com/agamm/awesome-ai-sre) | 🟡 💎 | Useful map of AI-for-SRE projects and automation patterns. |
| [anilsharmay/SREnity](https://github.com/anilsharmay/SREnity) | 🟡 📊 💎 | Track for enterprise SRE agent design patterns. |
| [shahid03/SRE_AI_agent](https://github.com/shahid03/SRE_AI_agent) | 🟡 🛡️ 📊 💎 ⚠️ | Provider-agnostic SRE assistant candidate with approval-sensitive actions. |
| [stevancris/sre-ai-agent](https://github.com/stevancris/sre-ai-agent) | 🟡 📊 💎 | Interesting if incident memory becomes cited guidance. |

### Incident Response Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [Mary-Preethi/incident-response-ai-agent](https://github.com/Mary-Preethi/incident-response-ai-agent) | 🟡 🛡️ 📊 💎 | Candidate for response-plan quality evaluation with light human-in-loop evidence. |
| [redemptionwxy/Incident-Response-AI-Agent](https://github.com/redemptionwxy/Incident-Response-AI-Agent) | 🟡 📊 💎 | Relevant for security incident initial investigation. |
| [Agrawalers/incidentIQ](https://github.com/Agrawalers/incidentIQ) | 🟡 📊 💎 ⚠️ | Prototype returns auto-apply/human-review verdicts; useful for autonomy-boundary review, not verified live remediation. |
| [Venkata-Manoj/Resilience-Ops-Env](https://github.com/Venkata-Manoj/Resilience-Ops-Env) | 🟡 📊 💎 | Synthetic/simulated incident-response benchmark candidate. |
| [NikhilRaman12/Incident-Renponse-Env](https://github.com/NikhilRaman12/Incident-Renponse-Env) | 🟡 📊 💎 | Synthetic/simulated SRE incident-response test-lab candidate. |

### Observability and Log-Analysis Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [alexkroman/ollychat](https://github.com/alexkroman/ollychat) | 🟡 📊 | Observability/chatops assistant with query-oriented tooling. |

### DevOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 💎 | Good source for MCP ecosystem mapping and candidate integrations. |
| [aliyun/alibabacloud-devops-mcp-server](https://github.com/aliyun/alibabacloud-devops-mcp-server) | 🔵 🟡 ⚠️ | Provider-specific MCP surface area that needs permission scoring. |
| [stefanskiasan/azure-devops-mcp-server](https://github.com/stefanskiasan/azure-devops-mcp-server) | 🔵 🟡 ⚠️ | Candidate for comparing Azure DevOps MCP implementations. |
| [aaronsb/ado-mcp](https://github.com/aaronsb/ado-mcp) | 🔵 🟡 | Azure DevOps MCP comparison entry with currently visible read-oriented project listing surface. |
| [Jordiag/azure-devops-mcp-server](https://github.com/Jordiag/azure-devops-mcp-server) | 🔵 🟡 ⚠️ | C# Azure DevOps MCP implementation candidate. |
| [wangkanai/devops-mcp](https://github.com/wangkanai/devops-mcp) | 🔵 🟡 ⚠️ | Good for dynamic MCP tool-inventory review. |
| [mcpflow/devops-mcp-servers](https://github.com/mcpflow/devops-mcp-servers) | 🔵 🟡 💎 ⚠️ | Prototype DevOps MCP server collection for expanding the server map. |
| [talkops-ai/talkops-mcp](https://github.com/talkops-ai/talkops-mcp) | 🔵 🟡 💎 ⚠️ | Complements the TalkOps agent repos with MCP registry context. |

### Agent Skills, Prompts, and Runbooks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-skills](https://github.com/microsoft/azure-devops-skills) | 🟡 💎 ⚠️ | Azure DevOps skill pattern, but approval gates should be verified per skill. |
| [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) | 🟡 📊 💎 | Safety-oriented companion to IaC and Kubernetes agent entries. |
| [derisk-ai/awesome-devops-skills](https://github.com/derisk-ai/awesome-devops-skills) | 🔵 🟡 💎 | Bridge between DevOps skills, runbooks, and MCP discovery. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 🟢 🛡️ 💎 | General engineering skill reference; useful style input for DevOps-specific scaffolds. |

### Safety, Audit, Approval, and Evidence Frameworks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [vitas/evidra](https://github.com/vitas/evidra) | 🔵 🟡 📊 💎 ⚠️ | MCP/CLI flight recorder that combines tool execution with durable evidence capture. |

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
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
