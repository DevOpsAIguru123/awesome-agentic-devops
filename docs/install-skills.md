# Install official skills into your coding agent

Install official [Agent Skills](https://github.com/anthropics/skills) into your coding agent with one command. Skills come from every `official-agent-skills` repo in this catalog — Google, Microsoft, Azure, and Azure DevOps.

The commands below use `--source all` to install **every** official skill (several hundred). To install just one company or product instead, use the ready-to-run commands in the [skills catalog by company & product](official-skills-catalog.md) — or swap `--source all` for a specific source, e.g. `--source microsoft/skills --filter azure-sdk-python` or `--source google/skills --filter cloud`.

## macOS / Linux

```bash
# Claude Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source all

# Cursor
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.sh | sh -s -- --source all

# Codex
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.sh | sh -s -- --source all

# Antigravity
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.sh | sh -s -- --source all

# VS Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.sh | sh -s -- --source all

# All agents at once
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.sh | sh -s -- --source all
```

## Windows (PowerShell)

```powershell
# Claude Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.ps1 -OutFile install.ps1; ./install.ps1 --source all

# Cursor
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.ps1 -OutFile install.ps1; ./install.ps1 --source all

# Codex
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.ps1 -OutFile install.ps1; ./install.ps1 --source all

# Antigravity
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.ps1 -OutFile install.ps1; ./install.ps1 --source all

# VS Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.ps1 -OutFile install.ps1; ./install.ps1 --source all

# All agents at once
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.ps1 -OutFile install.ps1; ./install.ps1 --source all
```

## What gets installed

The commands above (`--source all`) install every official skill — Google (72), Microsoft (191), Azure (33), and Azure DevOps (6). To install just one company or product, use the ready-to-run commands in the [official skills catalog by company & product](official-skills-catalog.md).

## Where skills land

Each agent installs real skill folders into its own global skills directory:

| Agent | Skills folder |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| VS Code Copilot | `~/.copilot/skills/` |
| Antigravity | `~/.gemini/antigravity/skills/` |

Add `--project` to install into the same layout under the current directory instead (e.g. `./.claude/skills/`), or `--target <dir>` to choose an explicit path.

> **Other folders some agents read.** Cursor can also load skills from `~/.agents/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`; VS Code Copilot can also read `~/.agents/skills/` and `~/.claude/skills/`. Antigravity's path is `~/.gemini/antigravity-cli/skills/` on some versions — install there with `--target ~/.gemini/antigravity-cli/skills`. Use `--target` for any folder not in the table above.

## Safety

Installs directly (skill folders are additive and reversible); pass `--dry-run` to preview first. It only writes skill folders — never secrets or other settings. `--list-sources` / `--list` show what's available. Prefer not to pipe a remote script to your shell? Read [`scripts/install_skills.py`](../scripts/install_skills.py) and run it from a clone: `python3 scripts/install_skills.py --agent claude-code --source all`.
