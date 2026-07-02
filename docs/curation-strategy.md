# Curation Strategy

This repo has two jobs: curate the ecosystem and turn promising patterns into buildable reference agents.

## 1. Curate the ecosystem

Track DevOps, Cloud, SRE, Kubernetes, Terraform, CI/CD, MCP, and platform-engineering agent projects. Favor public repos with runnable examples, docs, tests, or clear architecture.

## 2. Score repos

Each entry is scored by:

- Real infrastructure usefulness.
- Operational risk.
- Human approval gates.
- Tracing, evidence, and eval support.
- Maturity.
- Gemini-compatible rebuild opportunity.

## 3. Extract patterns

The goal is not only to list repos. The goal is to identify repeatable agent patterns:

- Terraform plan reviewer.
- Kubernetes CrashLoopBackOff triage assistant.
- CI failure explainer.
- Cloud cost anomaly investigator.
- Incident runbook assistant.
- MCP server for read-only cloud inventory.

## 4. Build reference implementations

Promising patterns should become scaffolded implementations across Claude Code, Gemini ADK, OpenAI Agents SDK, and MCP. The first pattern is the Terraform Plan Reviewer Agent.

## 5. Use daily Gemini workloads

Gemini can help classify entries, summarize docs, extract risk notes, build eval cases, and compare framework implementations. Each Gemini task should produce reviewed changes to `data/repos.yaml`, docs, or build-lab scaffolds.

## 6. Turn it into an interview and portfolio artifact

This repo should demonstrate practical judgment: infrastructure safety, agent design, DevOps workflows, and framework comparison. The best future version includes scored entries, runnable evals, and reference agents that never require real credentials by default.
