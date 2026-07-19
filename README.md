# Awesome Agentic DevOps

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/DevOpsAIguru123/awesome-agentic-devops/actions/workflows/validate.yml/badge.svg)](https://github.com/DevOpsAIguru123/awesome-agentic-devops/actions/workflows/validate.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A curated, **official-first** catalog of MCP servers, agent skills, AI agents, frameworks, and supporting resources for DevOps, Cloud, SRE, and Platform Engineering. It includes vendor and open-source project resources alongside a clearly labeled community-driven section.

Most agent lists stop at discovery. This one is built for operators:

- **Official-first, community-inclusive** — 65 entries organized into 14 catalog sections; official vendor and project resources are prioritized, while community-driven entries are separated in a dedicated [community section](#community-discovery-and-skills).
- **Scored, not just listed** — every entry records action capability, human-approval controls, tracing evidence, maturity, and operational risk ([how entries are scored](docs/scoring.md)).
- **Audited by CI** — GitHub repository entries are checked weekly for reachability and archived status; non-GitHub documentation links are outside this automated check and require curator review.
- **Installable, not just readable** — [one command](#install-skills-into-your-coding-agent) installs hundreds of skills from cataloged Google, Microsoft, Azure, Azure DevOps, and Harness sources — plus a separate community set — into Claude Code, Cursor, Codex, VS Code, or Antigravity.
- **Runnable, not just theoretical** — documented [reference-agent examples](#local-reference-agents) cover Terraform plan review and drift detection.

**Safety first:** some cataloged tools and agents can change infrastructure. Prefer read-only or proposal mode, require human approval before write actions, and use least-privilege credentials — full guidance in the [safety model](docs/safety-model.md).

## Contents

- [Evaluation labels](#evaluation-labels)
- [Top picks by use case](#top-picks-by-use-case)
- [Install skills into your coding agent](#install-skills-into-your-coding-agent)
- [Recently added](#recently-added)
- [Local reference agents](#local-reference-agents)
- [Curated catalog](#curated-catalog)
- [How to contribute](#how-to-contribute)

## Evaluation labels

| Label | Meaning |
| --- | --- |
| 🟢 | assessed as production-adjacent; not a readiness guarantee |
| 🟡 | assessed as a useful prototype |
| 🔵 | MCP/server integration |
| 🛡️ | documents an approval or safety mechanism; enforcement varies |
| 📊 | has tracing/evidence/evals |
| ⚠️ | write-capable; review before use |

Labels are shorthand for structured fields recorded on every entry in [data/repos.yaml](data/repos.yaml) — [how entries are scored](docs/scoring.md) explains each field and how it is verified.

## Top picks by use case

| Use case | Start with | Why |
| --- | --- | --- |
| AWS agentic cloud automation | [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | Official AWS-supported MCP, skills, plugins, IAM-aware controls, CloudWatch metrics, and CloudTrail auditability. |
| Azure cloud automation | [microsoft/mcp](https://github.com/microsoft/mcp)<br>[microsoft/azure-skills](https://github.com/microsoft/azure-skills) | Official Microsoft MCP and skills/plugin sources for Azure resource workflows. |
| Google Cloud automation | [google/mcp](https://github.com/google/mcp)<br>[googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp)<br>[google/skills](https://github.com/google/skills) | Official Google MCP and skills sources for GCP, Cloud Run, GKE, observability, and storage workflows. |
| Source-control DevOps | [github/github-mcp-server](https://github.com/github/github-mcp-server)<br>[GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/)<br>[atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) | Official MCP tool surfaces for repos, issues, PRs, Jira, Bitbucket, and related delivery workflows. |
| Terraform and IaC | [hashicorp/terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server)<br>[Pulumi MCP Server](https://www.pulumi.com/docs/ai/mcp-server/) | Official IaC MCP sources for Terraform Registry/HCP Terraform and Pulumi Cloud automation. |
| SRE incident response | [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana)<br>[datadog-labs/mcp-server](https://github.com/datadog-labs/mcp-server)<br>[Elastic Agent Builder MCP server docs](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server)<br>[PagerDuty/pagerduty-mcp-server](https://github.com/PagerDuty/pagerduty-mcp-server) | Official observability and incident-management MCPs for metrics, logs, traces, indexed operational data, alerts, incidents, and on-call context. |
| FinOps and cloud cost | [vantage-sh/vantage-mcp-server](https://github.com/vantage-sh/vantage-mcp-server) | Official Vantage MCP server for cloud spend analysis, budgets, anomalies, reports, and provider-resource cost context across Vantage-connected providers. |
| Security and code quality | [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)<br>[SonarSource/sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server)<br>[okta/okta-mcp-server](https://github.com/okta/okta-mcp-server)<br>[Snyk Studio MCP docs](https://docs.snyk.io/evo-by-snyk/agentic-security-with-snyk-studio/getting-started-with-snyk-studio)<br>[snyk/studio-mcp](https://github.com/snyk/studio-mcp)<br>[Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server)<br>[CrowdStrike/falcon-mcp](https://github.com/CrowdStrike/falcon-mcp) | Official MCPs and security resources for MCP threat modeling, code quality, application security, identity-aware workflows, agent security, cloud-security posture, and Falcon-platform SOC automation. |
| Data platform operations | [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server)<br>[redis/mcp-redis](https://github.com/redis/mcp-redis) | Official database MCP servers for MongoDB and Redis operational context, cache/session data, vector search, streams, and data-platform agent workflows. |
| CI/CD and GitOps | [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin)<br>[argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd)<br>[harness/mcp-server](https://github.com/harness/mcp-server) | Official Jenkins, Argo Project, and Harness resources for pipeline, build, deployment, rollback, and GitOps workflows. |
| MCP development and governance | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)<br>[modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)<br>[modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry)<br>[Docker MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | Official SDKs, registry, and Docker governance surfaces for building, packaging, and controlling DevOps MCP servers. |
| Agent frameworks and templates | [google/adk-python](https://github.com/google/adk-python)<br>[GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) | Official Google agent framework and production templates with CI/CD, evaluation, and observability. |

## Install skills into your coding agent

Install hundreds of [Agent Skills](https://github.com/anthropics/skills) from the cataloged Google, Microsoft, Azure, Azure DevOps, and Harness sources with one command:

```bash
# Claude Code, macOS/Linux — installs every official skill into ~/.claude/skills/
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source official
```

Choose breadth with `--source`: `official` (361 skills), `community` (26), or `everything` (387). Python 3 is the only requirement — there is no `pip install` step.

Pass `--dry-run` to preview first. Commands for Cursor, Codex, VS Code, Antigravity (Mac and Windows) — plus target folders and safety notes — are in the [install guide](docs/install-skills.md). To install just one company or product, use the [official skills catalog](docs/official-skills-catalog.md) or the [community skills catalog](docs/community-skills-catalog.md).

## Recently added

| Date | Entry | Category |
| --- | --- | --- |
| 2026-07-17 | [CrowdStrike/falcon-mcp](https://github.com/CrowdStrike/falcon-mcp) | Security / CrowdStrike Falcon SOC automation |
| 2026-07-14 | [dynatrace-oss/dynatrace-mcp](https://github.com/dynatrace-oss/dynatrace-mcp) | SRE / Dynatrace observability |
| 2026-07-12 | [harness/mcp-server](https://github.com/harness/mcp-server) | CI/CD / Harness |
| 2026-07-12 | [harness/harness-skills](https://github.com/harness/harness-skills) | Agent skills / Harness |
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

## Local reference agents

This repo keeps runnable reference agents under [`agents/`](agents/).

| Path | Purpose |
| --- | --- |
| [`agents/adk/terraform-plan-reviewer`](agents/adk/terraform-plan-reviewer) | Gemini ADK agent that reviews Terraform plan output and returns structured risk findings. |
| [`agents/adk/terraform-drift-detector`](agents/adk/terraform-drift-detector) | Gemini ADK agent that reviews Terraform Cloud refresh-only plans and sends Discord-ready drift alerts. |

## Curated catalog

The source of truth is [data/repos.yaml](data/repos.yaml). The catalog combines official vendor and open-source project resources with a dedicated section for community-driven tools and references. Entries include executable software as well as SDKs, documentation, security frameworks, registries, and other ecosystem resources.

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
| [snyk/studio-mcp](https://github.com/snyk/studio-mcp) | 🟢 🔵 🛡️ 📊 | Official Snyk MCP server (Go) providing snyk_sca_scan, snyk_code_scan, snyk_iac_scan, snyk_container_scan, snyk_sbom_scan, snyk_secret_scan, and snyk_aibom tools via the `snyk mcp` CLI command. |
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | 🟢 🛡️ 📊 | Official Snyk security scanner for AI agents, MCP servers, and agent skills. |
| [Wiz WIN MCP Server docs](https://docs.wiz.io/dev/win-mcp-server) | 🟢 🔵 🛡️ 📊 | Official Wiz documentation for the WIN MCP server, adding CNAPP and cloud-security coverage. |
| [CrowdStrike/falcon-mcp](https://github.com/CrowdStrike/falcon-mcp) | 🟡 🔵 🛡️ ⚠️ | Official CrowdStrike MCP server (Python, public preview) for threat detection, incident investigation, threat intelligence, endpoint inventory, identity protection, NG-SIEM, and cloud security (CSPM/CSVM). Use least-privilege API scopes; write-capable modules can change endpoint policy and detection rules. |

### Official CI/CD and GitOps MCP Servers

| Repo | Labels | Operator note |
| --- | --- | --- |
| [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) | 🟢 🔵 🛡️ ⚠️ | Official Jenkins plugin that enables Jenkins to act as an MCP server for LLM-powered clients. |
| [argoproj-labs/mcp-for-argocd](https://github.com/argoproj-labs/mcp-for-argocd) | 🟡 🔵 🛡️ ⚠️ | Argo Project Labs MCP server implementation for Argo CD, filling the GitOps/CD gap in the catalog. |
| [controlplaneio-fluxcd/flux-operator (MCP)](https://github.com/controlplaneio-fluxcd/flux-operator/tree/main/cmd/mcp) | 🟢 🔵 🛡️ 📊 ⚠️ | Official Flux Operator MCP server from CNCF Flux core maintainers; Go single-binary with read-only mode, kubeconfig scoping, and Kubernetes impersonation. Covers Kustomizations, HelmReleases, drift detection, root cause analysis, and multi-cluster comparison. |
| [CircleCI-Public/mcp-server-circleci](https://github.com/CircleCI-Public/mcp-server-circleci) | 🟢 🔵 🛡️ 📊 | Official CircleCI MCP server for build failure logs, pipeline status, flaky test detection, and usage analysis. |
| [harness/mcp-server](https://github.com/harness/mcp-server) | 🟢 🔵 🛡️ ⚠️ | Official Harness MCP server (Go) for CI/CD pipelines, deployments, connectors, feature flags, and infrastructure operations; risk-tiered model blocks destructive ops without confirmation. |

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
| [dynatrace-oss/dynatrace-mcp](https://github.com/dynatrace-oss/dynatrace-mcp) | 🟢 🔵 🛡️ 📊 ⚠️ | Official Dynatrace open-source MCP server for DQL querying, anomaly/incident/Kubernetes investigation, Davis Copilot AI chat, and deployment automation. |
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
| [harness/harness-skills](https://github.com/harness/harness-skills) | 🟢 🛡️ ⚠️ | Official Harness agent skills for Claude Code, Cursor, and GitHub Copilot enabling natural-language CI/CD automation via harness/mcp-server. |

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
python scripts/sync_readme_counts.py   # refreshes the intro's entry/category counts
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```
