# Official agent skills catalog — by company & product

Every skill the [skills installer](install-skills.md) can pull, grouped by **company and product**. Sources are the `official-agent-skills` repos in [`data/repos.yaml`](../data/repos.yaml). Counts were measured with `--list` at time of writing; upstream repos change, so run the command with `--dry-run` to preview or `--list` for the live count.

For community-maintained skills, see the [community skills catalog](community-skills-catalog.md).

**The commands below are complete — copy the one you want and run it.** They install into **Claude Code on macOS/Linux**. For a different setup, change only the start of the line:

- **Other agent** — swap `claude-code` in the URL for `cursor`, `codex`, `antigravity`, `vscode`, or `all`.
- **Windows** — replace `curl -fsSL <url>/install.sh | sh -s --` with `irm <url>/install.ps1 -OutFile install.ps1; ./install.ps1`.

---

## Everything, every source

```bash
# Every official skill below, deduped — 361 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --official

# Official + community together — 387 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --all
```

The flags compose: `--official --community` is the same as `--all`. The older `--source all` still works, but is an alias for `--official` and so excludes community skills.

Or pick a company/product below to install just that set.

## Google — `google/skills` (80)

```bash
# Cloud / DevOps — 67 skills (Cloud Run, GKE, BigQuery, AlloyDB, Cloud SQL, …)
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter cloud

# Ads — 11 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter ads

# Analytics — 3 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter analytics

# Everything from Google — 80 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills
```

## Microsoft — `microsoft/skills` (188)

```bash
# Azure SDK — Python — 40 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-python

# Azure skills — 32 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-skills

# Azure SDK — .NET — 29 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-dotnet

# Azure SDK — Java — 26 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-java

# Azure SDK — TypeScript — 25 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-typescript

# Deep Wiki — 10 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter deep-wiki

# Azure SDK — Rust — 9 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-rust

# Microsoft 365 Agents Toolkit — 6 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter microsoft-365-agents-toolkit

# Core skills (skill-creator, kql, mcp-builder, microsoft-docs, entra-agent-id, …) — 11 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter github/skills

# Every Azure SDK language at once — 129 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk

# Everything from Microsoft — 188 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills
```

## Microsoft Azure — `microsoft/azure-skills` (32)

Azure-focused skills (AKS, Microsoft Foundry models, and more).

```bash
# Everything from Azure skills — 32 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/azure-skills
```

## Microsoft Azure DevOps — `microsoft/azure-devops-skills` (7)

```bash
# Everything from Azure DevOps — 7 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/azure-devops-skills
```

## Harness — `harness/harness-skills` (54)

CI/CD, pipelines, deployments, and platform workflows for Harness.

```bash
# Everything from Harness — 54 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source harness/harness-skills
```
