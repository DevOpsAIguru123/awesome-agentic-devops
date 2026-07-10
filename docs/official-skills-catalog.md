# Official agent skills catalog — by company & product

Every skill the [skills installer](../README.md#install-official-skills-into-your-coding-agent) can pull, grouped by **company and product**. Sources are the `official-agent-skills` repos in [`data/repos.yaml`](../data/repos.yaml).

**Install any row with one command** — pick your agent's installer (`claude-code`, `cursor`, `codex`, `antigravity`, `vscode`, or `all`) and append the row's `--source …` from the tables below:

```bash
# macOS / Linux (example: Google Cloud/DevOps skills into Claude Code)
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source google/skills --filter cloud
```

```powershell
# Windows
irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.ps1 -OutFile install.ps1; ./install.ps1 --source google/skills --filter cloud
```

Preview any row first with `--dry-run`, or list exact skill names with `--list`. Counts are the number of `SKILL.md` folders at the time of writing; run `--list` for the current live count.

---

## Google — `google/skills` (72)

| Product | Skills | Append to the install command |
| --- | ---: | --- |
| Cloud / DevOps (Cloud Run, GKE, BigQuery, AlloyDB, Cloud SQL, …) | 59 | `--source google/skills --filter cloud` |
| Ads | 11 | `--source google/skills --filter ads` |
| Analytics | 2 | `--source google/skills --filter analytics` |
| **Everything from Google** | **72** | `--source google/skills` |

## Microsoft — `microsoft/skills` (191)

| Product | Skills | Append to the install command |
| --- | ---: | --- |
| Azure SDK — Python | 40 | `--source microsoft/skills --filter azure-sdk-python` |
| Azure skills | 33 | `--source microsoft/skills --filter azure-skills` |
| Azure SDK — .NET | 29 | `--source microsoft/skills --filter azure-sdk-dotnet` |
| Azure SDK — Java | 26 | `--source microsoft/skills --filter azure-sdk-java` |
| Azure SDK — TypeScript | 25 | `--source microsoft/skills --filter azure-sdk-typescript` |
| Deep Wiki | 10 | `--source microsoft/skills --filter deep-wiki` |
| Azure SDK — Rust | 9 | `--source microsoft/skills --filter azure-sdk-rust` |
| Microsoft 365 Agents Toolkit | 6 | `--source microsoft/skills --filter microsoft-365-agents-toolkit` |
| Core skills (skill-creator, kql, mcp-builder, microsoft-docs, entra-agent-id, …) | 13 | `--source microsoft/skills --filter github/skills` |
| **Everything from Microsoft** | **191** | `--source microsoft/skills` |

`--filter azure-sdk` (no language suffix) installs every Azure SDK skill across languages.

## Microsoft Azure — `microsoft/azure-skills` (33)

Azure-focused skills (AKS, Microsoft Foundry models, and more).

| Product | Skills | Append to the install command |
| --- | ---: | --- |
| **Everything from Azure skills** | **33** | `--source microsoft/azure-skills` |

## Microsoft Azure DevOps — `microsoft/azure-devops-skills` (6)

| Product | Skills | Append to the install command |
| --- | ---: | --- |
| **Everything from Azure DevOps** | **6** | `--source microsoft/azure-devops-skills` |

---

## Everything, every source

| Scope | Append to the install command |
| --- | --- |
| Every official skill above (deduped by name) | `--source all` |

`--source all` pulls from every official skill repo — several hundred skills. Prefer a company/product row above, or add `--filter <substring>` to scope it.
