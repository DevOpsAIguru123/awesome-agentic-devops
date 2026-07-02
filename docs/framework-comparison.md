# Framework Comparison

This comparison focuses on DevOps, Cloud, SRE, Kubernetes, Terraform, CI/CD, and MCP agents.

| Framework | Best fit | Strengths | Weaknesses | DevOps agent examples | Safety model | Gemini-credit relevance | Recommended first use case |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Repository-local engineering agents and codebase-aware automation | Strong file editing, code review, shell workflows, test loops, and repo refactoring | Less ideal as a hosted multi-agent service boundary by itself | Terraform module reviewer, CI failure fixer, runbook linter | Human-in-the-loop code diffs, local git review, test-before-commit | Useful benchmark for comparing Gemini ADK developer workflows | Terraform plan reviewer that comments on a PR |
| Gemini ADK | Agent workflows that need Google ecosystem fit, multi-step orchestration, and GCP-friendly evaluation | Natural fit for GCP, Gemini credits, multimodal docs, and agent orchestration | Ecosystem patterns are still maturing for production DevOps use | GKE SRE assistant, Terraform plan reviewer, Cloud Logging summarizer | Read-only tools first, approval callbacks, policy checks, audit traces | Primary target for daily Gemini workloads and rebuild experiments | GKE read-only incident triage agent |
| OpenAI Agents SDK | Structured tool-using agents, guardrails, evaluations, and handoffs | Clear agent abstractions, tool calling, tracing/evals fit, and policyable workflows | Requires careful deployment and credential isolation | CI copilot, incident summarizer, Terraform risk scorer | Tool allowlists, approval functions, tracing, eval gates | Useful comparison point to test Gemini parity and gaps | Proposal-mode CI/CD failure analysis |
| MCP | Tool and data connector layer for agents | Explicit server boundaries, reusable integrations, IDE/client portability | Safety depends on each server's tool surface and permissions | Cloud inventory MCP server, Azure DevOps MCP tools, Kubernetes read-only MCP server | Least-privilege servers, read-only tools, explicit destructive-operation separation | Strong opportunity to expose Gemini-compatible DevOps tools behind MCP | Read-only Terraform state or cloud inventory MCP server |

## Practical takeaways

- Use Claude Code when the main job is repository editing, review, tests, and git hygiene.
- Use Gemini ADK when the goal is to build repeatable Gemini-powered cloud workflows, especially around GCP.
- Use OpenAI Agents SDK when tracing, tool orchestration, and evals are central to the reference implementation.
- Use MCP when the problem is tool exposure and integration boundaries rather than agent reasoning alone.
