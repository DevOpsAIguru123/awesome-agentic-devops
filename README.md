# Awesome Agentic DevOps

**Awesome Agentic DevOps** is a curated map and build lab for DevOps, Cloud, SRE, and Platform Engineering agents across Claude Code, Gemini ADK, OpenAI Agents SDK, and MCP.

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
2. DevOps MCP servers
3. Agent skills, prompts, and runbooks

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| Terraform generation and review | `antonbabenko/terraform-skill` | Terraform-specific skill material for plan review, module authoring, and blast-radius review patterns. |
| MCP integration mapping | `rohitg00/awesome-devops-mcp-servers` | Helps compare DevOps MCP discovery sources and tool-boundary review needs. |
| Azure DevOps skills | `microsoft/azure-devops-skills` | Good source for Azure DevOps skill patterns, with write-capable behavior requiring approval review. |
| General agent skill structure | `addyosmani/agent-skills` | Production-oriented engineering skill examples that can inform DevOps-specific runbooks. |

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

The source of truth is [data/repos.yaml](data/repos.yaml). The list below is a readable index of the current four focused research-backed entries.

### Terraform / IaC Agents

| Repo | Labels | Operator note |
| --- | --- | --- |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ 💎 | Terraform-specific skill material for plan review and module workflows. |

### DevOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 💎 | Good source for MCP ecosystem mapping and candidate integrations. |

### Agent Skills, Prompts, and Runbooks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-skills](https://github.com/microsoft/azure-devops-skills) | 🟡 💎 ⚠️ | Azure DevOps skill pattern, but approval gates should be verified per skill. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 🟢 🛡️ 💎 | General engineering skill reference; useful style input for DevOps-specific scaffolds. |

## How to contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New entries should update [data/repos.yaml](data/repos.yaml), include a real operational use case, classify action level, and explain safety or approval behavior.

Run validation before opening a PR:

```bash
python scripts/validate_repos_yaml.py
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
