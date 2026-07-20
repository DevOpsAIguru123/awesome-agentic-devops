# Community agent skills catalog — by author & product

Community-maintained skills the [skills installer](install-skills.md) can pull. Sources are the `community-agent-skills` repos in [`data/repos.yaml`](../data/repos.yaml). Counts were measured with `--list` at time of writing; run the command with `--dry-run` to preview or `--list` for the live count.

> **These are not vendor-supported.** This catalog is official-first; the entries below are community-driven and carry the same caveats as any third-party code you install. Review a skill before trusting it to act on your infrastructure, and prefer `--dry-run` first. See the [safety model](safety-model.md).

For vendor-published skills, see the [official skills catalog](official-skills-catalog.md).

**The commands below are complete — copy the one you want and run it.** They install into **Claude Code on macOS/Linux**. For a different setup, change only the start of the line:

- **Other agent** — swap `claude-code` in the URL for `cursor`, `codex`, `antigravity`, `vscode`, or `all`.
- **Windows** — replace `curl -fsSL <url>/install.sh | sh -s --` with `irm <url>/install.ps1 -OutFile install.ps1; ./install.ps1`.

---

## Everything community

```bash
# Every community skill below, deduped — 26 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --community

# Official + community together — 387 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --all
```

Or pick a single source below.

## Addy Osmani — `addyosmani/agent-skills` (24)

General engineering skills — API and interface design, CI/CD and automation, browser testing with DevTools, and more.

```bash
# Everything from addyosmani/agent-skills — 24 skills
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source addyosmani/agent-skills
```

## Anton Babenko — `antonbabenko/terraform-skill` (1)

Terraform guidance, IaC review, and module authoring.

```bash
# Everything from antonbabenko/terraform-skill — 1 skill
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source antonbabenko/terraform-skill
```

## Agents365 — `Agents365-ai/drawio-skill` (1)

Diagramming with draw.io.

```bash
# Everything from Agents365-ai/drawio-skill — 1 skill
curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh -s -- --source Agents365-ai/drawio-skill
```
