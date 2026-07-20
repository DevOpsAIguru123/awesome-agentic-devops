# Install agent skills into your coding agent

Install [Agent Skills](https://github.com/anthropics/skills) into your coding agent with one command. Skills come from the skill repos catalogued here — Google, Microsoft, Azure, Azure DevOps and Harness on the official side, plus a separate community set.

## Choose what to install

Pass a flag to pick how much you want:

| Flag | Installs | Count |
| --- | --- | --- |
| `--official` | every official skill repo | 361 skills |
| `--community` | every community skill repo | 26 skills |
| `--all` | both | 387 skills |

The flags compose, so `--official --community` is the same as `--all`.

For a single repo, use `--source owner/repo` instead, e.g. `--source google/skills`. To install just one company or product, use the ready-to-run commands in the [official skills catalog](official-skills-catalog.md) or the [community skills catalog](community-skills-catalog.md) — or add `--filter`, e.g. `--source microsoft/skills --filter azure-sdk-python` or `--source google/skills --filter cloud`.

> `--source` also accepts the keywords `official`, `community` and `everything`. Note that `--source all` is a long-standing alias for `official`, so unlike the `--all` flag it does **not** include community skills.

## macOS / Linux

```bash
# Claude Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --official

# Cursor
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.sh | sh -s -- --official

# Codex
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.sh | sh -s -- --official

# Antigravity
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.sh | sh -s -- --official

# VS Code
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.sh | sh -s -- --official

# All agents at once
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.sh | sh -s -- --official
```

Swap `--official` for `--community` or `--all` as needed.

## Windows (PowerShell)

```powershell
# Claude Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.ps1 -OutFile install.ps1; ./install.ps1 --official

# Cursor
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.ps1 -OutFile install.ps1; ./install.ps1 --official

# Codex
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.ps1 -OutFile install.ps1; ./install.ps1 --official

# Antigravity
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.ps1 -OutFile install.ps1; ./install.ps1 --official

# VS Code
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.ps1 -OutFile install.ps1; ./install.ps1 --official

# All agents at once
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/all/install.ps1 -OutFile install.ps1; ./install.ps1 --official
```

## What gets installed

`--official` installs every official skill — Google (80), Microsoft (188), Azure (32), Azure DevOps (7), and Harness (54), deduped to 361. `--community` adds 26 more. To install just one company or product, use the [official](official-skills-catalog.md) or [community](community-skills-catalog.md) catalog.

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

It also works from inside a virtualenv. A python.org build (and any venv made from one) has an empty certificate store until its `Install Certificates.command` has been run, which otherwise fails every download with `CERTIFICATE_VERIFY_FAILED`; the installer falls back to the operating system's own CA bundle in that case.

## Safety

Installs directly (skill folders are additive and reversible); pass `--dry-run` to preview first. It only writes skill folders — never secrets or other settings. `--list-sources` / `--list` show what's available. Community skills are not vendor-supported — review before trusting them to act on infrastructure; see the [safety model](safety-model.md).

Prefer not to pipe a remote script to your shell? Read [`scripts/install_skills.py`](../scripts/install_skills.py) and run it from a clone: `python3 scripts/install_skills.py --agent claude-code --official`.
