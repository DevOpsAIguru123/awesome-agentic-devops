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

1. Official cloud MCP servers and agent toolkits
2. Official DevOps and source-control MCP servers
3. Official SRE and observability MCP servers
4. Official IaC MCP servers
5. Official agent skills and agent frameworks
6. Community discovery and skill references

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| AWS agentic cloud automation | `aws/agent-toolkit-for-aws` | Official AWS-supported MCP, skills, plugins, IAM-aware controls, CloudWatch metrics, and CloudTrail auditability. |
| Azure cloud automation | `microsoft/mcp` and `microsoft/azure-skills` | Official Microsoft MCP and skills/plugin sources for Azure resource workflows. |
| Google Cloud automation | `google/mcp`, `googleapis/gcloud-mcp`, and `google/skills` | Official Google MCP and skills sources for GCP, Cloud Run, GKE, observability, and storage workflows. |
| Source-control DevOps | `github/github-mcp-server`, `GitLab MCP server`, and `atlassian/atlassian-mcp-server` | Official MCP tool surfaces for repos, issues, PRs, Jira, Bitbucket, and related delivery workflows. |
| Terraform and IaC | `hashicorp/terraform-mcp-server` and `Pulumi MCP Server` | Official IaC MCP sources for Terraform Registry/HCP Terraform and Pulumi Cloud automation. |
| SRE incident response | `grafana/mcp-grafana`, `datadog-labs/mcp-server`, and `PagerDuty/pagerduty-mcp-server` | Official observability and incident-management MCPs for metrics, logs, traces, alerts, incidents, and on-call context. |
| Agent build scaffolds | `google/adk-python` and `GoogleCloudPlatform/agent-starter-pack` | Official Google agent framework and production templates with CI/CD, evaluation, and observability. |

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

The source of truth is [data/repos.yaml](data/repos.yaml). The list below is a readable index of the current official and community research-backed entries.

### Official Cloud MCP Servers and Agent Toolkits

| Repo | Labels | Operator note |
| --- | --- | --- |
| [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official AWS-supported toolkit that bundles MCP server configuration, skills, plugins, and DevSecOps agent workflows. |
| [awslabs/mcp](https://github.com/awslabs/mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official AWS Labs MCP server collection; useful legacy/source reference while AWS transitions capabilities into Agent Toolkit. |
| [microsoft/mcp](https://github.com/microsoft/mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Microsoft MCP catalog, including Azure cloud and infrastructure MCP references. |
| [google/mcp](https://github.com/google/mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Google MCP repository listing managed and open-source MCP servers for Google and Google Cloud. |
| [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Google API repository for gcloud, observability, storage, and backup/disaster-recovery MCP servers. |
| [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Google Cloud Platform MCP server for deploying apps to Cloud Run. |

### Official DevOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Azure DevOps MCP server with remote-first onboarding and local server option. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 🟢 🔵 🛡️ 💎 ⚠️ | Official GitHub MCP server for repository, issue, pull request, code, and workflow automation. |
| [GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/) | 🟢 🔵 🛡️ 💎 ⚠️ | Official GitLab MCP server is documented as a GitLab-hosted endpoint rather than a standalone GitHub repo. |
| [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Atlassian Rovo MCP server for Jira, Confluence, Jira Service Management, Bitbucket, and Compass. |
| [docker/mcp-registry](https://github.com/docker/mcp-registry) | 🟢 🔵 🛡️ 📊 💎 | Official Docker MCP registry and catalog source for verified containerized MCP servers. |
| [kubernetes-sigs/mcp-lifecycle-operator](https://github.com/kubernetes-sigs/mcp-lifecycle-operator) | 🟡 🔵 🛡️ 💎 ⚠️ | Official Kubernetes SIG operator for declaratively deploying and rolling out MCP servers, not a general kubectl MCP server. |

### Official IaC MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official HashiCorp Terraform MCP server with registry, HCP Terraform, Terraform Enterprise, and OTel support. |
| [Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Pulumi hosted MCP server for Pulumi Cloud resources, registry lookup, policies, and Pulumi Neo workflows. |

### Official SRE MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official Grafana MCP server for Grafana and surrounding observability ecosystem access. |
| [datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server) | 🟢 🔵 🛡️ 📊 💎 | Official Datadog MCP server documentation and examples for connecting AI agents to Datadog observability. |
| [PagerDuty/pagerduty-mcp-server](https://github.com/PagerDuty/pagerduty-mcp-server) | 🟢 🔵 🛡️ 💎 ⚠️ | Official PagerDuty MCP server for incidents, services, schedules, event orchestrations, and embedded incident UIs. |

### Official Agent Skills and Frameworks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-skills](https://github.com/microsoft/azure-devops-skills) | 🟢 💎 ⚠️ | Official Microsoft Azure DevOps skill examples; approval gates should be verified per skill. |
| [microsoft/skills](https://github.com/microsoft/skills) | 🟢 🔵 🛡️ 💎 | Official Microsoft skills, MCP configurations, custom agents, and AGENTS.md guidance for coding agents. |
| [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Azure skills plugin with Azure skills, Azure MCP tools, and Foundry MCP coverage. |
| [google/skills](https://github.com/google/skills) | 🟢 🛡️ 💎 | Official Google Agent Skills repository for Google products and technologies. |
| [google/adk-python](https://github.com/google/adk-python) | 🟢 🛡️ 📊 💎 | Official Google Agent Development Kit for building, evaluating, and deploying agents. |
| [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | 🟢 🛡️ 📊 💎 | Official Google Cloud starter pack for shipping agents with CI/CD, evaluation, observability, and security. |

### Community Discovery and Skills

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 💎 | Community discovery source for MCP ecosystem mapping and candidate integrations. |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ 💎 | Community Terraform-specific prompt and workflow seed for the build lab. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 🟢 🛡️ 💎 | Community engineering skill reference; useful style and structure input for DevOps-specific scaffolds. |

## How to contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New entries should update [data/repos.yaml](data/repos.yaml), include a real operational use case, classify action level, and explain safety or approval behavior.

Run validation before opening a PR:

```bash
python scripts/validate_repos_yaml.py
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
