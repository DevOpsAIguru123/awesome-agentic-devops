# DevOps AI Operating Skill

Use this workspace as an operator-grade DevOps/SRE/Cloud MCP catalog and build lab.

## Safety rules

- Prefer read-only and proposal-mode workflows before any write-capable tool.
- Never paste secrets, tokens, kubeconfigs, cloud credentials, or private logs into model context.
- Require a human approval gate for deploys, Terraform applies, incident mutations, identity changes, and production writes.
- Preserve evidence: link PRs, plans, CI logs, traces, runbooks, and incident timelines.
- Treat catalog labels as a first-pass risk signal, not a production approval.

## MCP catalog tool

This setup registers a local MCP server named `awesome-agentic-devops-catalog`.
Use it to search official DevOps MCP entries before recommending integrations.

Suggested prompts:

- Search the DevOps MCP catalog for Terraform/IaC tools and compare blast radius.
- Find official observability MCP servers with audit or tracing evidence.
- List write-capable CI/CD or GitOps tools and explain required approval gates.
- Recommend a read-only starting point for Kubernetes/SRE investigation.

## Included official MCP categories

- `official-agent-skills`
- `official-ci-cd-mcp-servers`
- `official-cloud-agent-toolkits`
- `official-cloud-mcp-servers`
- `official-cloud-security-mcp-servers`
- `official-data-platform-mcp-servers`
- `official-devops-mcp-platforms`
- `official-devops-mcp-servers`
- `official-diagramming-mcp-tools`
- `official-finops-mcp-servers`
- `official-gitops-mcp-servers`
- `official-iac-mcp-servers`
- `official-mcp-reference-implementations`
- `official-mcp-registry`
- `official-mcp-sdks`
- `official-platform-agent-toolkits`
- `official-security-mcp-servers`
- `official-sre-mcp-servers`

## Sample entries

| Entry | Category | Action level | Maturity | Operator note |
| --- | --- | --- | --- | --- |
| [microsoft/azure-skills](https://github.com/microsoft/azure-skills) | official-agent-skills | write-capable | production-adjacent | Official Azure skills plugin with Azure skills, Azure MCP tools, and Foundry MCP coverage. |
| [microsoft/skills](https://github.com/microsoft/skills) | official-agent-skills | proposal | skill-library | Official Microsoft skills, MCP configurations, custom agents, and AGENTS.md guidance for coding agents. |
| [CircleCI-Public/mcp-server-circleci](https://github.com/CircleCI-Public/mcp-server-circleci) | official-ci-cd-mcp-servers | read-only | production-adjacent | Official CircleCI MCP server for build failure logs, pipeline status, flaky test detection, and usage analysis. |
| [jenkinsci/mcp-server-plugin](https://github.com/jenkinsci/mcp-server-plugin) | official-ci-cd-mcp-servers | write-capable | production-adjacent | Official Jenkins plugin that enables Jenkins to act as an MCP server for LLM-powered clients. |
| [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | official-cloud-agent-toolkits | write-capable | production-adjacent | Official AWS-supported toolkit that bundles MCP server configuration, skills, plugins, and DevSecOps agent workflows. |
| [awslabs/mcp](https://github.com/awslabs/mcp) | official-cloud-mcp-servers | write-capable | production-adjacent | Official AWS Labs MCP server collection; useful legacy/source reference while AWS transitions capabilities into Agent Toolkit. |
| [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) | official-cloud-mcp-servers | write-capable | production-adjacent | Official Cloudflare MCP servers for account, Workers, and edge configuration workflows, with both curated domain servers and a code-mode server. |
| [google/mcp](https://github.com/google/mcp) | official-cloud-mcp-servers | write-capable | production-adjacent | Official Google MCP repository listing managed and open-source MCP servers for Google and Google Cloud. |
| [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp) | official-cloud-mcp-servers | write-capable | production-adjacent | Official Google API repository for gcloud, observability, storage, and backup/disaster-recovery MCP servers. |
| [GoogleCloudPlatform/cloud-run-mcp](https://github.com/GoogleCloudPlatform/cloud-run-mcp) | official-cloud-mcp-servers | write-capable | production-adjacent | Official Google Cloud Platform MCP server for deploying apps to Cloud Run. |
| [microsoft/mcp](https://github.com/microsoft/mcp) | official-cloud-mcp-servers | write-capable | production-adjacent | Official Microsoft MCP catalog, including Azure cloud and infrastructure MCP references. |
| [vercel/vercel-mcp-overview](https://github.com/vercel/vercel-mcp-overview) | official-cloud-mcp-servers | write-capable | production-adjacent | Official public overview of Vercel's hosted MCP server, documented at vercel.com/docs/mcp/vercel-mcp; this repo tracks the docs, not a standalone local server. |
