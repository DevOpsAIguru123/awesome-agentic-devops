# Awesome Agentic DevOps

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/DevOpsAIguru123/awesome-agentic-devops/actions/workflows/validate.yml/badge.svg)](https://github.com/DevOpsAIguru123/awesome-agentic-devops/actions/workflows/validate.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Awesome Agentic DevOps** is a curated map for DevOps, Cloud, SRE, and Platform Engineering agents across Claude Code, Gemini ADK, OpenAI Agents SDK, and MCP.

This repository evaluates which agents are safe, useful, and production-adjacent for infrastructure automation. Every link is re-audited by scheduled CI for reachability, archival, and freshness.

## Contents

- [Recently added](#recently-added)
- [Why this exists](#why-this-exists)
- [Who it is for](#who-it-is-for)
- [Safety-first disclaimer](#safety-first-disclaimer)
- [Evaluation labels](#evaluation-labels)
- [How entries are scored](#how-entries-are-scored)
- [Categories](#categories)
- [Top picks by use case](#top-picks-by-use-case)
- [Local reference agents](#local-reference-agents)
- [Curated catalog](#curated-catalog)
- [How to contribute](#how-to-contribute)

## Recently added

| Date | Entry | Category |
| --- | --- | --- |
| 2026-07-09 | [redis/mcp-redis](https://github.com/redis/mcp-redis) | Data platform / Redis |
| 2026-07-08 | [Elastic Agent Builder MCP server docs](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server) | SRE / observability |
| 2026-07-07 | [skyhook-io/radar](https://github.com/skyhook-io/radar) | Kubernetes / community MCP |
| 2026-07-07 | [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) | Agent security / MCP risk framework |
| 2026-07-06 | [vantage-sh/vantage-mcp-server](https://github.com/vantage-sh/vantage-mcp-server) | FinOps / cloud cost |
| 2026-07-05 | [hashicorp/vault-mcp-server](https://github.com/hashicorp/vault-mcp-server) | IaC / secrets management |
| 2026-07-05 | [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) | Cloud / edge |
| 2026-07-05 | [CircleCI-Public/mcp-server-circleci](https://github.com/CircleCI-Public/mcp-server-circleci) | CI/CD |
| 2026-07-05 | [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) | Data platform |
| 2026-07-05 | [backstage/backstage (mcp-actions-backend)](https://github.com/backstage/backstage/tree/master/plugins/mcp-actions-backend) | Platform toolkits |

## Why this exists

Most agent lists stop at discovery. Infrastructure teams need more than discovery: they need to know whether an agent can touch production, whether it has approval gates, whether it preserves evidence, and whether it can be rebuilt as a safe reference workflow.

This repo is intentionally operator-grade. Each entry is scored by real infrastructure usefulness, operational risk, human approval gates, tracing/evidence, and maturity.

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
| ⚠️ | write-capable; review before use |

Labels are shorthand for structured fields recorded on every entry in [data/repos.yaml](data/repos.yaml): ⚠️ maps to `action_level: write-capable`, 🛡️ to `human_approval: true`, 📊 to tracing or eval evidence, and 🟢/🟡 to `maturity`.

## How entries are scored

Every entry records five verifiable dimensions. They are assessed by reading each project's documentation and exposed tool surface, not its marketing.

| Field | Question it answers | How it is verified |
| --- | --- | --- |
| `action_level` | Can it touch production? | Read the project's exposed tool list. Only query tools (`get`, `list`, `search`) means `read-only`. Suggesting changes for a human to execute means `proposal`. Any tool that mutates real state (`create`, `deploy`, `delete`, `sync`) means `write-capable` and the entry gets ⚠️. |
| `human_approval` | Does a human gate write actions? | Look for gates in the server (write tools disabled by default, dry-run modes, confirmation flags) or in the client (permission prompts). Server-side gates are stronger because they hold no matter which client connects. |
| `evidence_tracing` | Can you prove what it did afterward? | Check for audit logs, OpenTelemetry support, structured run records, or evaluation output. Scored `yes`, `partial`, or `none`. |
| `maturity` | Is it stable enough to depend on? | Observable signals only: vendor support status, API stability (GA versus alpha), and recent activity. The audit script checks freshness and archived status automatically. |
| `risk_notes` | What is the blast radius if it goes wrong? | Combines the above with what the tool connects to. Write-capable identity tooling is treated very differently from a read-only diagram generator. |

### Example: reading one entry

```yaml
- name: PagerDuty/pagerduty-mcp-server
  action_level: write-capable    # tools can create incidents and schedule overrides
  human_approval: true           # write tools ship disabled by default
  evidence_tracing: partial      # logs exist, but no structured trace guarantee
  maturity: production-adjacent  # official vendor server
  risk_notes: "Keep write tools disabled by default and require approval for changes."
```

Read as: safe to connect for incident context today, but flip on its write tools only after you have decided who approves an agent-created incident.

### What is automated and what is judgment

Link reachability, archived status, and freshness are checked automatically by [scripts/audit_github_repos.py](scripts/audit_github_repos.py) and enforced in CI. The safety scores themselves are curator judgment from reviewing each project's docs and tool surface at the time of entry. Verify against your own environment before connecting anything to real infrastructure — [templates/agent-scorecard.md](templates/agent-scorecard.md) is the full per-project checklist used for deep review.

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
11. Official data platform MCP servers
12. Official FinOps and cloud-cost MCP servers
13. Community discovery and skill references

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| AWS agentic cloud automation | [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | Official AWS-supported MCP, skills, plugins, IAM-aware controls, CloudWatch metrics, and CloudTrail auditability. |
| Azure cloud automation | [microsoft/mcp](https://github.com/microsoft/mcp) and [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | Official Microsoft MCP and skills/plugin sources for Azure resource workflows. |
| Google Cloud automation | [google/mcp](https://github.com/google/mcp), [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp), and [google/skills](https://github.com/google/skills) | Official Google MCP and skills sources for GCP, Cloud Run, GKE, observability, and storage workflows. |
| Source-control DevOps | [github/github-mcp-server](https://github.com/github/github-mcp-server), [GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/), and [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) | Official MCP tool surfaces for repos, issues, PRs, Jira, Bitbucket, and related delivery workflows. |
| Terraform and IaC | [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) and [Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | Official IaC MCP sources for Terraform Registry/HCP Terraform and Pulumi Cloud automation. |
| SRE incident response | [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana), [datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server), [Elastic Agent Builder MCP server docs](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server), and [PagerDuty/pagerduty-mcp-server](https://github.com/PagerDuty/pagerduty-mcp-server) | Official observability and incident-management MCPs for metrics, logs, traces, indexed operational data, alerts, incidents, and on-call context. |
| FinOps and cloud cost | [vantage-sh/vantage-mcp-server](https://github.com/vantage-sh/vantage-mcp-server) | Official Vantage MCP server for cloud spend analysis, budgets, anomalies, reports, and provider-resource cost context across Vantage-connected providers. |
| Security and code quality | [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/), [SonarSource/sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server), [okta/okta-mcp-server](https://github.com/okta/okta-mcp-server), [Snyk Studio MCP docs](https://docs.snyk.io/evo-by-snyk/agentic-security-with-snyk-studio/getting-started-with-snyk-studio), and [Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server) | Official MCPs and security resources for MCP threat modeling, code quality, application security, identity-aware workflows, agent security, and cloud-security posture. |
| Data platform operations | [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) and [redis/mcp-redis](https://github.com/redis/mcp-redis) | Official database MCP servers for MongoDB and Redis operational context, cache/session data, vector search, streams, and data-platform agent workflows. |
| CI/CD and GitOps | [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) and [argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd) | Official Jenkins and Argo Project resources for pipeline, build, deployment, and GitOps workflows. |
| MCP development and governance | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk), [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk), [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry), and [Docker MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | Official SDKs, registry, and Docker governance surfaces for building, packaging, and controlling DevOps MCP servers. |
| Agent frameworks and templates | [google/adk-python](https://github.com/google/adk-python) and [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | Official Google agent framework and production templates with CI/CD, evaluation, and observability. |

## Local Reference Agents

This repo keeps runnable reference agents under [`agents/`](agents/).

| Path | Purpose |
| --- | --- |
| [`agents/adk/terraform-plan-reviewer`](agents/adk/terraform-plan-reviewer) | Gemini ADK agent that reviews Terraform plan output and returns structured risk findings. |
| [`agents/adk/terraform-drift-detector`](agents/adk/terraform-drift-detector) | Gemini ADK agent that reviews Terraform Cloud refresh-only plans and sends Discord-ready drift alerts. |

## Curated catalog

The source of truth is [data/repos.yaml](data/repos.yaml). The list below is a readable index of the current official and community research-backed entries.

### Official Cloud MCP Servers and Agent Toolkits

| Repo | Labels | Operator note |
| --- | --- | --- |
| [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | 🟢 🔵 🛡️ 📊 ⚠️ | Official AWS-supported toolkit that bundles MCP server configuration, skills, plugins, and DevSecOps agent workflows. |
| [awslabs/mcp](https://github.com/awslabs/mcp) | 🟢 🔵 🛡️ ⚠️ | Official AWS Labs MCP server collection; useful legacy/source reference while AWS transitions capabilities into Agent Toolkit. |
| [microsoft/mcp](https://github.com/microsoft/mcp) | 🟢 🔵 🛡️ ⚠️ | Official Microsoft MCP catalog, including Azure cloud and infrastructure MCP references. |
| [google/mcp](https://github.com/google/mcp) | 🟢 🔵 🛡️ ⚠️ | Official Google MCP repository listing managed and open-source MCP servers for Google and Google Cloud. |
| [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp) | 🟢 🔵 🛡️ ⚠️ | Official Google API repository for gcloud, observability, storage, and backup/disaster-recovery MCP servers. |
| [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) | 🟢 🔵 🛡️ ⚠️ | Official Google Cloud Platform MCP server for deploying apps to Cloud Run. |
| [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) | 🟢 🔵 🛡️ ⚠️ | Official Cloudflare MCP servers for account, Workers, and edge configuration workflows. |
| [vercel/vercel-mcp-overview](https://github.com/vercel/vercel-mcp-overview) | 🟢 🔵 🛡️ ⚠️ | Official public overview of Vercel's hosted MCP server for project and deployment context. |

### Official DevOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp) | 🟢 🔵 🛡️ ⚠️ | Official Azure DevOps MCP server with remote-first onboarding and local server option. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official GitHub MCP server for repository, issue, pull request, code, and workflow automation. |
| [GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/) | 🟢 🔵 🛡️ ⚠️ | Official GitLab MCP server is documented as a GitLab-hosted endpoint rather than a standalone GitHub repo. |
| [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official Atlassian Rovo MCP server for Jira, Confluence, Jira Service Management, Bitbucket, and Compass. |
| [docker/mcp-registry](https://github.com/docker/mcp-registry) | 🟢 🔵 🛡️ 📊 | Official Docker MCP registry and catalog source for verified containerized MCP servers. |
| [kubernetes-sigs/mcp-lifecycle-operator](https://github.com/kubernetes-sigs/mcp-lifecycle-operator) | 🟡 🔵 🛡️ ⚠️ | Official Kubernetes SIG operator for declaratively deploying and rolling out MCP servers, not a general kubectl MCP server. |

### Official Security and Code-Quality MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [SonarSource/sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server) | 🟢 🔵 🛡️ | Official SonarQube MCP server for code quality and security insights in AI agents. |
| [okta/okta-mcp-server](https://github.com/okta/okta-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official Okta self-hosted MCP server for connecting agents to Okta identity workflows. |
| [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) | 🟢 🔵 🛡️ 📊 | Official OWASP MCP Top 10 documentation for assessing Model Context Protocol security risks across agentic DevOps integrations. |
| [Snyk Studio MCP docs](https://docs.snyk.io/evo-by-snyk/agentic-security-with-snyk-studio/getting-started-with-snyk-studio) | 🟢 🔵 🛡️ 📊 | Official Snyk documentation for Snyk Studio agentic security workflows and Snyk MCP Server usage. |
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | 🟢 🛡️ 📊 | Official Snyk security scanner for AI agents, MCP servers, and agent skills. |
| [Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server) | 🟢 🔵 🛡️ 📊 | Official Wiz documentation for the WIN MCP server, adding CNAPP and cloud-security coverage. |

### Official CI/CD and GitOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) | 🟢 🔵 🛡️ ⚠️ | Official Jenkins plugin that enables Jenkins to act as an MCP server for LLM-powered clients. |
| [argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd) | 🟡 🔵 🛡️ ⚠️ | Argo Project Labs MCP server implementation for Argo CD, filling the GitOps/CD gap in the catalog. |
| [CircleCI-Public/mcp-server-circleci](https://github.com/CircleCI-Public/mcp-server-circleci) | 🟢 🔵 🛡️ 📊 | Official CircleCI MCP server for build failure logs, pipeline status, flaky test detection, and usage analysis. |

### Official MCP SDKs, Reference Implementations, Registries, and Governance Platforms

| Repo | Labels | Operator note |
| --- | --- | --- |
| [Docker MCP Catalog and Toolkit docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | 🟢 🔵 🛡️ ⚠️ | Official Docker documentation for MCP Toolkit, MCP Catalog, profiles, CLI, and MCP Gateway. |
| [Docker MCP Gateway docs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) | 🟢 🔵 🛡️ ⚠️ | Official Docker MCP Gateway documentation for secure, centralized orchestration of containerized MCP tools. |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 🟢 🔵 🛡️ | Official MCP reference server implementations and ecosystem pointers. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 🟢 🔵 🛡️ | Official Python SDK for building MCP servers and clients. |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | 🟢 🔵 🛡️ | Official TypeScript SDK for Model Context Protocol servers and clients. |
| [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry) | 🟢 🔵 🛡️ 📊 | Official community-driven registry service for Model Context Protocol servers. |

### Official CloudOps Agent Samples

| Repo | Labels | Operator note |
| --- | --- | --- |
| [aws-samples/sample-cloudops-multi-agent-platform](https://github.com/aws-samples/sample-cloudops-multi-agent-platform) | 🟡 🛡️ 📊 ⚠️ | AWS Samples reference for a hierarchical multi-agent CloudOps platform using Bedrock AgentCore and Strands Agents SDK. |

### Official IaC MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) | 🟢 🔵 🛡️ 📊 ⚠️ | Official HashiCorp Terraform MCP server with registry, HCP Terraform, Terraform Enterprise, and OTel support. |
| [Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | 🟢 🔵 🛡️ ⚠️ | Official Pulumi hosted MCP server for Pulumi Cloud resources, registry lookup, policies, and Pulumi Neo workflows. |
| [hashicorp/vault-mcp-server](https://github.com/hashicorp/vault-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official HashiCorp Vault MCP server (beta) for secrets and mount management alongside Terraform-driven IaC workflows. |

### Official SRE MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) | 🟢 🔵 🛡️ 📊 ⚠️ | Official Grafana MCP server for Grafana and surrounding observability ecosystem access. |
| [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) | 🟢 🔵 🛡️ 📊 ⚠️ | Official Sentry MCP service focused on human-in-the-loop coding agents and debugging workflows. |
| [datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server) | 🟢 🔵 🛡️ 📊 | Official Datadog MCP server documentation and examples for connecting AI agents to Datadog observability. |
| [Datadog MCP Server setup docs](https://docs.datadoghq.com/mcp_server/setup/?tab=chatgpt) | 🟢 🔵 🛡️ 📊 | Official Datadog MCP setup documentation, including the ChatGPT setup path. |
| [Splunk MCP Server](https://splunkbase.splunk.com/app/7931) | 🟢 🔵 🛡️ 📊 | Splunkbase listing for the Splunk-supported MCP Server for Splunk Platform, Enterprise, and Cloud customers. |
| [PagerDuty/pagerduty-mcp-server](https://github.com/PagerDuty/pagerduty-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official PagerDuty MCP server for incidents, services, schedules, event orchestrations, and embedded incident UIs. |
| [newrelic/mcp-server](https://github.com/newrelic/mcp-server) | 🟢 🔵 🛡️ 📊 | Official New Relic MCP server for APM, dashboard, and NRQL-based observability context. |
| [Elastic Agent Builder MCP server docs](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server) | 🟢 🔵 🛡️ 📊 | Official Elastic documentation for exposing Agent Builder tools through MCP with Kibana URL and API-key authentication. |

### Official Agent Skills and Frameworks

| Repo | Labels | Operator note |
| --- | --- | --- |
| [microsoft/azure-devops-skills](https://github.com/microsoft/azure-devops-skills) | 🟢 ⚠️ | Official Microsoft Azure DevOps skill examples; approval gates should be verified per skill. |
| [microsoft/skills](https://github.com/microsoft/skills) | 🟢 🔵 🛡️ | Official Microsoft skills, MCP configurations, custom agents, and AGENTS.md guidance for coding agents. |
| [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | 🟢 🔵 🛡️ ⚠️ | Official Azure skills plugin with Azure skills, Azure MCP tools, and Foundry MCP coverage. |
| [google/skills](https://github.com/google/skills) | 🟢 🛡️ | Official Google Agent Skills repository for Google products and technologies. |
| [google/adk-python](https://github.com/google/adk-python) | 🟢 🛡️ 📊 | Official Google Agent Development Kit for building, evaluating, and deploying agents. |
| [GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | 🟢 🛡️ 📊 | Official Google Cloud starter pack for shipping agents with CI/CD, evaluation, observability, and security. |

### Official Platform Agent Toolkits

| Repo | Labels | Operator note |
| --- | --- | --- |
| [databricks-solutions/ai-dev-kit](https://github.com/databricks-solutions/ai-dev-kit) | 🟢 🔵 🛡️ 📊 ⚠️ | Databricks field-engineering AI Dev Kit with Databricks MCP server, Databricks skills, tools core, and builder app support. |
| [kubeflow/mcp-server](https://github.com/kubeflow/mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official Kubeflow MCP server for AI-assisted development with Kubeflow tools. |
| [backstage/backstage (mcp-actions-backend)](https://github.com/backstage/backstage/tree/master/plugins/mcp-actions-backend) | 🟢 🔵 🛡️ ⚠️ | Official CNCF Backstage plugin that exposes Internal Developer Portal actions as MCP tools for AI agents. |

### Official Diagramming and Architecture MCP Tools

| Repo | Labels | Operator note |
| --- | --- | --- |
| [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) | 🟢 🔵 🛡️ | draw.io MCP server and Claude Code plugin for generating, opening, and exporting draw.io diagrams with shape search. |

### Official Data Platform MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official MongoDB MCP server (public preview) connecting agents to MongoDB Community, Enterprise, and Atlas deployments. |
| [redis/mcp-redis](https://github.com/redis/mcp-redis) | 🟢 🔵 🛡️ ⚠️ | Official Redis MCP Server for natural-language Redis data management, cache/session workflows, vector search, streams, pub/sub, and Redis documentation lookup. |

### Official FinOps and Cloud-Cost MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [vantage-sh/vantage-mcp-server](https://github.com/vantage-sh/vantage-mcp-server) | 🟢 🔵 🛡️ 📊 ⚠️ | Official Vantage MCP server for natural-language FinOps workflows over Vantage cloud spend, budgets, anomalies, reports, and provider resources. |

### Community Discovery and Skills

| Repo | Labels | Operator note |
| --- | --- | --- |
| [rohitg00/awesome-devops-mcp-servers](https://github.com/rohitg00/awesome-devops-mcp-servers) | 🔵 🟡 | Community discovery source for MCP ecosystem mapping and candidate integrations. |
| [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) | 🟡 🛡️ | Community Terraform-specific prompt and workflow reference. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 🟢 🛡️ | Community engineering skill reference; useful style and structure input for DevOps-specific skills. |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 🟡 🛡️ | Community draw.io skill for natural-language diagram generation, visual self-checking, and exports. |
| [skyhook-io/radar](https://github.com/skyhook-io/radar) | 🟢 🔵 🛡️ 📊 ⚠️ | Community open-source Kubernetes UI with a built-in MCP server: read-only cluster/topology/event queries plus RBAC-scoped write and GitOps/Helm tools for AI-assisted operations. |

## How to contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New entries should update [data/repos.yaml](data/repos.yaml), include a real operational use case, classify action level, and explain safety or approval behavior.

Run validation before opening a PR:

```bash
python scripts/validate_repos_yaml.py
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
