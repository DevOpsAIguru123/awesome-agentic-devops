# Install agent skills into your coding agent

Install [Agent Skills](https://github.com/anthropics/skills) into your coding agent with one command. Skills come from the skill repos catalogued here — Google, Microsoft, Azure, Azure DevOps and Harness on the official side, plus a separate community set.

## Choose what to install

`--source` decides breadth:

| `--source` | Installs | Count |
| --- | --- | --- |
| `official` | every official skill repo | 361 skills |
| `community` | every community skill repo | 26 skills |
| `everything` | both | 387 skills |
| `owner/repo` | one specific repo, e.g. `google/skills` | varies |

`--source all` is a long-standing alias for `official` and still works.

To install just one company or product, use the ready-to-run commands in the [official skills catalog](official-skills-catalog.md) or the [community skills catalog](community-skills-catalog.md) — or add `--filter`, e.g. `--source microsoft/skills --filter azure-sdk-python` or `--source google/skills --filter cloud`.

## macOS / Linux

```bash
# Claude Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source official

# Cursor
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.sh | sh -s -- --source official

# Codex
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.sh | sh -s -- --source official

# Antigravity
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.sh | sh -s -- --source official

# VS Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.sh | sh -s -- --source official

# All agents at once
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.sh | sh -s -- --source official
```

Swap `--source official` for `--source community` or `--source everything` as needed.

## Windows (PowerShell)

```powershell
# Claude Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.ps1 -OutFile install.ps1; ./install.ps1 --source official

# Cursor
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.ps1 -OutFile install.ps1; ./install.ps1 --source official

# Codex
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.ps1 -OutFile install.ps1; ./install.ps1 --source official

# Antigravity
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.ps1 -OutFile install.ps1; ./install.ps1 --source official

# VS Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.ps1 -OutFile install.ps1; ./install.ps1 --source official

# All agents at once
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.ps1 -OutFile install.ps1; ./install.ps1 --source official
```

## What gets installed

`--source official` installs every official skill — Google (80), Microsoft (188), Azure (32), Azure DevOps (7), and Harness (54), deduped to 361. `--source community` adds 26 more. To install just one company or product, use the [official](official-skills-catalog.md) or [community](community-skills-catalog.md) catalog.

Installing everything is a lot of skills, and every installed skill's description is loaded by your agent in each session. Prefer a per-vendor or `--filter` scope unless you genuinely want the full set.

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

## Requirements

Python 3 only — no `pip install` step. The installer reads its catalog from [`data/catalog.json`](../data/catalog.json), a generated file the standard library can parse, so it works on a stock interpreter such as macOS's `/usr/bin/python3`.

## Safety

Installs directly (skill folders are additive and reversible); pass `--dry-run` to preview first. It only writes skill folders — never secrets or other settings. `--list-sources` / `--list` show what's available. Community skills are not vendor-supported — review before trusting them to act on infrastructure; see the [safety model](safety-model.md).

Prefer not to pipe a remote script to your shell? Read [`scripts/install_skills.py`](../scripts/install_skills.py) and run it from a clone: `python3 scripts/install_skills.py --agent claude-code --source official`.
