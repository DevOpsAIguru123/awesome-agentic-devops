# Awesome Agentic DevOps

**Awesome Agentic DevOps** is a curated map for DevOps, Cloud, SRE, and Platform Engineering agents across Claude Code, Gemini ADK, OpenAI Agents SDK, and MCP.

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
3. Official CI/CD and GitOps MCP servers
4. Official security, code-quality, and agent-security resources
5. Official IaC MCP servers
6. Official SRE and observability MCP servers
7. Official agent skills and agent frameworks
8. Official platform agent toolkits
9. Official MCP SDKs, references, registries, and governance platforms
10. Official diagramming and architecture MCP tools
11. Community discovery and skill references

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| AWS agentic cloud automation | [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | Official AWS-supported MCP, skills, plugins, IAM-aware controls, CloudWatch metrics, and CloudTrail auditability. |
| Azure cloud automation | [microsoft/mcp](https://github.com/microsoft/mcp) and [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | Official Microsoft MCP and skills/plugin sources for Azure resource workflows. |
| Google Cloud automation | [google/mcp](https://github.com/google/mcp), [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp), and [google/skills](https://github.com/google/skills) | Official Google MCP and skills sources for GCP, Cloud Run, GKE, observability, and storage workflows. |
| Source-control DevOps | [github/github-mcp-server](https://github.com/github/github-mcp-server), [GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/), and [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) | Official MCP tool surfaces for repos, issues, PRs, Jira, Bitbucket, and related delivery workflows. |
| Terraform and IaC | [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) and [Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | Official IaC MCP sources for Terraform Registry/HCP Terraform and Pulumi Cloud automation. |
| SRE incident response | [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana), [datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server), and [PagerDuty/pagerduty-mcp-server](https://github.com/PagerDuty/pagerduty-mcp-server) | Official observability and incident-management MCPs for metrics, logs, traces, alerts, incidents, and on-call context. |
| Security and code quality | [SonarSource/sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server), [okta/okta-mcp-server](https://github.com/okta/okta-mcp-server), [Snyk Studio MCP docs](https://docs.snyk.io/evo-by-snyk/agentic-security-with-snyk-studio), and [Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server) | Official MCPs and security resources for code quality, application security, identity-aware workflows, agent security, and cloud-security posture. |
| CI/CD and GitOps | [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) and [argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd) | Official Jenkins and Argo Project resources for pipeline, build, deployment, and GitOps workflows. |
| MCP development and governance | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk), [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk), [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry), and [Docker MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | Official SDKs, registry, and Docker governance surfaces for building, packaging, and controlling DevOps MCP servers. |
| Agent frameworks and templates | [google/adk-python](https://github.com/google/adk-python) and [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | Official Google agent framework and production templates with CI/CD, evaluation, and observability. |

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

### Official Security and Code-Quality MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [SonarSource/sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server) | 🟢 🔵 🛡️ 💎 | Official SonarQube MCP server for code quality and security insights in AI agents. |
| [okta/okta-mcp-server](https://github.com/okta/okta-mcp-server) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Okta self-hosted MCP server for connecting agents to Okta identity workflows. |
| [Snyk Studio MCP docs](https://docs.snyk.io/evo-by-snyk/agentic-security-with-snyk-studio) | 🟢 🔵 🛡️ 📊 💎 | Official Snyk documentation for Snyk Studio agentic security workflows and Snyk MCP Server usage. |
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | 🟢 🛡️ 📊 💎 | Official Snyk security scanner for AI agents, MCP servers, and agent skills. |
| [Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server) | 🟢 🔵 🛡️ 📊 💎 | Official Wiz documentation for the WIN MCP server, adding CNAPP and cloud-security coverage. |

### Official CI/CD and GitOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Jenkins plugin that enables Jenkins to act as an MCP server for LLM-powered clients. |
| [argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd) | 🟡 🔵 🛡️ 💎 ⚠️ | Argo Project Labs MCP server implementation for Argo CD, filling the GitOps/CD gap in the catalog. |

### Official MCP SDKs, Reference Implementations, Registries, and Governance Platforms

| Repo | Labels | Operator note |
| --- | --- | --- |
| [Docker MCP Catalog and Toolkit docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Docker documentation for MCP Toolkit, MCP Catalog, profiles, CLI, and MCP Gateway. |
| [Docker MCP Gateway docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Docker MCP Gateway documentation for secure, centralized orchestration of containerized MCP tools. |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 🟢 🔵 🛡️ 💎 | Official MCP reference server implementations and ecosystem pointers. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 🟢 🔵 🛡️ 💎 | Official Python SDK for building MCP servers and clients. |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | 🟢 🔵 🛡️ 💎 | Official TypeScript SDK for Model Context Protocol servers and clients. |
| [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry) | 🟢 🔵 🛡️ 📊 💎 | Official community-driven registry service for Model Context Protocol servers. |

### Official CloudOps Agent Samples

| Repo | Labels | Operator note |
| --- | --- | --- |
| [aws-samples/sample-cloudops-multi-agent-platform](https://github.com/aws-samples/sample-cloudops-multi-agent-platform) | 🟡 🛡️ 📊 💎 ⚠️ | AWS Samples reference for a hierarchical multi-agent CloudOps platform using Bedrock AgentCore and Strands Agents SDK. |

### Official IaC MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official HashiCorp Terraform MCP server with registry, HCP Terraform, Terraform Enterprise, and OTel support. |
| [Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Pulumi hosted MCP server for Pulumi Cloud resources, registry lookup, policies, and Pulumi Neo workflows. |

### Official SRE MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official Grafana MCP server for Grafana and surrounding observability ecosystem access. |
| [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Official Sentry MCP service focused on human-in-the-loop coding agents and debugging workflows. |
| [datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server) | 🟢 🔵 🛡️ 📊 💎 | Official Datadog MCP server documentation and examples for connecting AI agents to Datadog observability. |
| [Datadog MCP Server setup docs](https://docs.datadoghq.com/mcp_server/setup/?tab=chatgpt) | 🟢 🔵 🛡️ 📊 💎 | Official Datadog MCP setup documentation, including the ChatGPT setup path. |
| [Splunk MCP Server](https://splunkbase.splunk.com/app/7931) | 🟢 🔵 🛡️ 📊 💎 | Splunkbase listing for the Splunk-supported MCP Server for Splunk Platform, Enterprise, and Cloud customers. |
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

### Official Platform Agent Toolkits

| Repo | Labels | Operator note |
| --- | --- | --- |
| [databricks-solutions/ai-dev-kit](https://github.com/databricks-solutions/ai-dev-kit) | 🟢 🔵 🛡️ 📊 💎 ⚠️ | Databricks field-engineering AI Dev Kit with Databricks MCP server, Databricks skills, tools core, and builder app support. |
| [kubeflow/mcp-server](https://github.com/kubeflow/mcp-server) | 🟢 🔵 🛡️ 💎 ⚠️ | Official Kubeflow MCP server for AI-assisted development with Kubeflow tools. |

### Official Diagramming and Architecture MCP Tools

| Repo | Labels | Operator note |
| --- | --- | --- |
| [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) | 🟢 🔵 🛡️ 💎 | draw.io MCP server and Claude Code plugin for generating, opening, and exporting draw.io diagrams with shape search. |

### Community Discovery and Skills

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 💎 | Community discovery source for MCP ecosystem mapping and candidate integrations. |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ 💎 | Community Terraform-specific prompt and workflow reference. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 🟢 🛡️ 💎 | Community engineering skill reference; useful style and structure input for DevOps-specific skills. |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 🟡 🛡️ 💎 | Community draw.io skill for natural-language diagram generation, visual self-checking, and exports. |

## How to contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New entries should update [data/repos.yaml](data/repos.yaml), include a real operational use case, classify action level, and explain safety or approval behavior.

Run validation before opening a PR:

```bash
python scripts/validate_repos_yaml.py
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
