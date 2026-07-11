# Official agent skills catalog — by company & product

Every skill the [skills installer](install-skills.md) can pull, grouped by **company and product**. Sources are the `official-agent-skills` repos in [`data/repos.yaml`](../data/repos.yaml). Counts are `SKILL.md` folders at time of writing; run the command with `--dry-run` to preview or `--list` for the live count.

**The commands below are complete — copy the one you want and run it.** They install into **Claude Code on macOS/Linux**. For a different setup, change only the start of the line:

- **Other agent** — swap `claude-code` in the URL for `cursor`, `codex`, `antigravity`, `vscode`, or `all`.
- **Windows** — replace `curl -fsSL <url>/install.sh | sh -s --` with `irm <url>/install.ps1 -OutFile install.ps1; ./install.ps1`.

---

## Everything, every source

```bash
# Every official skill below, deduped — several hundred skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source all
```

Or pick a company/product below to install just that set.

## Google — `google/skills` (72)

```bash
# Cloud / DevOps — 59 skills (Cloud Run, GKE, BigQuery, AlloyDB, Cloud SQL, …)
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter cloud

# Ads — 11 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter ads

# Analytics — 2 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter analytics

# Everything from Google — 72 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills
```

## Microsoft — `microsoft/skills` (191)

```bash
# Azure SDK — Python — 40 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk-python

# Azure skills — 33 skills
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

# Core skills (skill-creator, kql, mcp-builder, microsoft-docs, entra-agent-id, …) — 13 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter github/skills

# Every Azure SDK language at once — 129 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills --filter azure-sdk

# Everything from Microsoft — 191 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/skills
```

## Microsoft Azure — `microsoft/azure-skills` (33)

Azure-focused skills (AKS, Microsoft Foundry models, and more).

```bash
# Everything from Azure skills — 33 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/azure-skills
```

## Microsoft Azure DevOps — `microsoft/azure-devops-skills` (6)

```bash
# Everything from Azure DevOps — 6 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source microsoft/azure-devops-skills
```
