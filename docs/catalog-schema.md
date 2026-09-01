# Catalog schema reference

`data/repos.yaml` is the structured source of truth for the public catalog. Each entry is a top-level YAML list item with the required fields below. Keep this file and `scripts/validate_repos_yaml.py` aligned whenever a new category, artifact type, or scoring value is introduced.

## Required fields

Every catalog entry must include:

- `name` — stable display name, usually `owner/repo` for GitHub projects or a concise documentation title for hosted/vendor docs.
- `url` — absolute `https://` URL. Relative links, bare hostnames, and `http://` URLs are rejected.
- `category` — one of the allowed catalog section slugs below.
- `type` — one of the allowed artifact kinds below.
- `framework` — implementation framework or `unknown` when not applicable.
- `primary_language` — main language or content surface, such as `Go`, `Python`, `TypeScript`, `Documentation`, or `unknown`.
- `cloud_provider` — provider scope, such as `aws`, `azure`, `gcp`, `multi-cloud`, `kubernetes`, or `none`.
- `use_cases` — non-empty list of concrete operator use cases.
- `action_level` — one of `read-only`, `proposal`, `write-capable`, or `unknown`.
- `human_approval` — `true`, `false`, or `unknown`.
- `evidence_tracing` — one of `yes`, `partial`, `none`, or `unknown`. Quote `"yes"` in YAML so it stays a string.
- `maturity` — one of the allowed maturity values below.
- `risk_notes` — non-empty blast-radius and credential-risk note.
- `operator_note` — non-empty reason an infrastructure operator should care.
- `labels` — non-empty list using only the README evaluation labels below.

## Identity and duplicate rules

Catalog identity is intentionally strict so generated README tables, audits, and
review discussions can point to a single stable row:

- `name` must be unique across the whole flat list. Prefer `owner/repo` for
  GitHub-backed projects so the display name stays stable even if the README
  section changes.
- `url` must be unique across the whole flat list and must be the canonical
  operator-facing source for the artifact being cataloged.
- Do not add a second row for the same artifact only to represent another use
  case or README section. Capture additional operator use cases in `use_cases`
  and choose the best single `category`.
- Separate documentation and runnable surfaces may have distinct rows only when
  they are genuinely different artifacts, such as vendor docs plus a separate
  installable `mcp-server` repository.

## README synchronization rules

When `data/repos.yaml` changes, update every README surface that helps operators
discover or verify the row. At minimum, run `python3 scripts/sync_readme_counts.py`
so the intro count stays aligned with the YAML source of truth. For new catalog
entries, also update these README sections in the same pull request:

- `## Recently added` — prepend a dated row for the new or refreshed entry.
- The matching catalog section table for the entry's `category`.
- The intro quick-pick table when the category already has a representative row.
- `## Top picks by use case` only when the entry is genuinely a top recommendation
  for that operator workflow; do not add weak entries just to fill the table.

Run `python3 scripts/sync_readme_counts.py --check` before review so README count
drift fails locally rather than in CI.

## Allowed categories

Category slugs define the curated README sections and are validated in CI. The prefix is also a provenance signal:

- `official-*` categories are for first-party vendor, CNCF/Kubernetes SIG, foundation, or upstream project-governed sources where maintainership is clear from the repository owner or official documentation.
- `community-*` categories are for useful third-party tools, discovery lists, or skill collections that are not governed by the vendor/project whose platform they operate.

Do not classify a repo as official just because it integrates with an official API, appears in a third-party list, or uses a vendor name. When provenance is unclear, prefer a community category or hold the entry until a first-party source confirms ownership.

- `community-agent-skills`
- `community-discovery`
- `community-mcp-servers`
- `official-agent-frameworks`
- `official-agent-security-tools`
- `official-agent-skills`
- `official-browser-automation-mcp-servers`
- `official-ci-cd-mcp-servers`
- `official-cloud-agent-toolkits`
- `official-cloud-mcp-servers`
- `official-cloud-security-mcp-servers`
- `official-cloudops-agent-samples`
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

Add a new category only when the existing taxonomy cannot describe the entry clearly, and update all of these together:

1. `scripts/validate_repos_yaml.py`
2. `tests/test_repos_yaml.py`
3. `README.md` catalog section and quick-pick references when applicable
4. This schema reference

## Allowed artifact types

Use the narrowest type that describes the actual operator surface:

- `agent-framework`
- `agent-plugin`
- `agent-security-scanner`
- `agent-template`
- `agent-toolkit`
- `curated-list`
- `documentation`
- `hosted-mcp-server`
- `mcp-operator`
- `mcp-plugin`
- `mcp-registry`
- `mcp-server`
- `mcp-server-catalog`
- `mcp-server-collection`
- `mcp-server-plugin`
- `reference-architecture`
- `reference-implementations`
- `registry`
- `sdk`
- `security-guidance`
- `security-tool`
- `skill`
- `skill-library`

Docs pages and runnable servers are distinct artifacts. A vendor may have both a `documentation` entry and a separate `mcp-server` or `hosted-mcp-server` entry when both are useful to operators.

## Minimal entry template

Start new entries from this shape, then replace every placeholder with verified
facts from the official repository or documentation. `data/repos.yaml` is a flat
list, so add this as a new top-level list item rather than nesting it under a
category key.

```yaml
- name: owner/repo-or-doc-name
  url: https://example.com/official-source
  category: official-devops-mcp-servers
  type: mcp-server
  framework: unknown
  primary_language: unknown
  cloud_provider: none
  use_cases:
    - Short operator task this tool supports
  action_level: read-only
  human_approval: unknown
  evidence_tracing: unknown
  maturity: production-adjacent
  risk_notes: Verify credential scope, write tools, telemetry, and audit behavior before production-adjacent use.
  operator_note: Explain why a DevOps, SRE, platform, cloud, security, or MLOps operator should evaluate it.
  labels:
    - mcp
```

Template review checklist:

- Replace placeholder `unknown` values whenever official docs expose a more
  specific framework, language, credential, approval, or tracing signal.
- Use `action_level: proposal` for dry-run or plan-generating tools, and
  `action_level: write-capable` plus the `write` label when any tool can mutate
  infrastructure, code, tickets, cloud resources, or production data.
- Prefer read-only, scoped, or test credentials in `risk_notes`; do not paste
  secrets, tokens, customer data, or private endpoints into catalog metadata.
- Add `approval` only with `human_approval: true`, and add `evidence` only when
  official docs or code show audit logs, traces, citations, run artifacts, or
  similarly durable evidence.

## Source verification checklist

Before adding or refreshing a catalog row, collect harmless public evidence for
the operator-facing surface rather than relying on marketing copy or a broad MCP
index. A reviewer should be able to reproduce these checks without secrets:

- Reachability: confirm the repository or documentation URL returns successfully
  and is the canonical upstream, vendor, foundation, or community project page.
- Freshness: for GitHub projects, check that the repository is not archived and
  has recent enough activity for the maturity claim; otherwise explain the stale
  or archival signal in `risk_notes`.
- Tool surface: verify whether the artifact is a runnable `mcp-server`, a hosted
  endpoint, an SDK, documentation, a skill, or only a curated list, then set
  `type` to the narrowest matching value.
- Credential boundary: identify the least-privilege credential mode an operator
  can use for evaluation, or state clearly when the project only documents broad
  credentials or leaves credential scope unspecified.
- Safety signals: map observed dry-run behavior, approval gates, evidence or
  audit artifacts, telemetry, and write capability back to `action_level`,
  `human_approval`, `evidence_tracing`, `risk_notes`, and `labels`.

### Risk notes writing guide

Write `risk_notes` as a short operator warning, not a marketing summary. Good
risk notes answer what could go wrong during evaluation and what guardrail should
be used first:

- Name the credential boundary: read-only token, scoped test account, sandbox
  cloud project, limited Kubernetes namespace, or unknown scope.
- Identify write capability, destructive actions, external API calls, telemetry,
  or data exfiltration paths when the tool can reach infrastructure or sensitive
  systems.
- Prefer dry-run, proposal, preview, or plan-only workflows before write-capable
  execution, and mention required human approval when official docs or code show
  an approval gate.
- Call out missing evidence honestly: use `unknown` scoring or note when audit
  logs, traces, citations, or run artifacts are not documented.

Example:

```yaml
risk_notes: Use a read-only GitHub token for evaluation; write-capable issue and pull-request tools require scoped test repositories, explicit approval, and audit-log review before production use.
```

### Automated GitHub freshness audit

For substantial catalog edits, run the lightweight GitHub metadata audit before
review so stale or unreachable repositories are visible next to the proposed
metadata change:

```bash
python3 scripts/audit_github_repos.py --stale-days 365
```

The command writes `reports/github-repo-audit.json` and
`reports/github-repo-audit.md` with reachability, archived/private status,
primary-language drift, last push time, and stale-repository warnings for GitHub
URLs in `data/repos.yaml`. Treat the reports as curator evidence, not generated
catalog source: summarize relevant warnings in the pull request body, update
`risk_notes` when an entry is stale or archived, and do not commit the reports
unless a reviewer explicitly asks for a point-in-time audit artifact.

For non-GitHub documentation and hosted MCP endpoints, record a separate manual
reachability check because the GitHub audit intentionally skips those URLs.

### Deprecation and removal handling

When a cataloged project becomes archived, deprecated, unreachable, or materially
less safe than its current score suggests, prefer a traceable refresh over a
silent delete:

- Replace the row with the current official successor when vendor or upstream
  documentation points to a maintained repository, hosted endpoint, or docs page.
- Keep a stale row only when it still has operator value, lower the maturity or
  action score as needed, and explain the archived, deprecated, or unsupported
  status in `risk_notes`.
- Remove a row when the source is unreachable, unsafe, abandoned without clear
  operator value, or superseded by a better canonical entry; mention the removal
  in `CHANGELOG.md` unless it is part of routine duplicate cleanup.
- Never preserve an obsolete entry just to maintain README counts. Run
  `python3 scripts/sync_readme_counts.py` after removals or replacements.

### Evidence capture worksheet

Paste a short evidence note into the pull request body when catalog metadata
changes. Keep it factual, reproducible, and free of secrets:

```markdown
Source evidence:
- Canonical source: <official repository or vendor docs URL>
- Reachability check: <command or URL check used, with date>
- Freshness signal: <GitHub pushedAt/not archived, docs date, or documented caveat>
- Tool surface: <mcp-server | hosted endpoint | sdk | docs | skill | list>
- Credential boundary: <read-only token, scoped test credential, OAuth scope, or unknown>
- Safety signals: <dry-run/proposal mode, approval gate, tracing/audit artifact, write capability>
```

Suggested harmless commands for GitHub-backed entries:

```bash
gh repo view OWNER/REPO --json nameWithOwner,isArchived,pushedAt,defaultBranchRef,licenseInfo,url,repositoryTopics
gh api repos/OWNER/REPO/contents/README.md --jq .download_url
```

For non-GitHub documentation, record the canonical URL, HTTP status, redirected
URL if any, and content type. Do not include access tokens, private tenant URLs,
internal hostnames, customer data, or screenshots that expose credentials.

## Maturity values

- `production-adjacent` — official or mature enough to evaluate near production, but not a production-readiness guarantee.
- `active-oss` — active open-source project with useful operator value.
- `prototype` — useful but early, experimental, or lower-confidence.
- `curated-list` — index or registry rather than a runnable tool.
- `skill-library` — installable agent-skill collection.
- `unknown` — insufficient evidence; prefer avoiding this for new entries unless the operator value is clear.

## Evaluation labels and consistency rules

Labels are the README-facing shorthand for structured safety fields:

- `prod` — production-adjacent maturity.
- `prototype` — prototype maturity.
- `mcp` — MCP/server integration.
- `approval` — `human_approval: true`.
- `evidence` — `evidence_tracing: "yes"` or `partial`.
- `write` — `action_level: write-capable`.

Validator-enforced invariants:

- `write` requires `action_level: write-capable`, and write-capable entries must include `write`.
- `approval` requires `human_approval: true`, and human-approval entries must include `approval`.
- `evidence_tracing: "yes"` requires `evidence`; `evidence` cannot be used with `none` or `unknown`.
- `prod` and `prototype` are mutually exclusive.
- `maturity: prototype` requires `prototype` and cannot use `prod`.

## Pre-submit commands

Run these before opening a catalog PR:

```bash
python3 scripts/sync_readme_counts.py
python3 scripts/sync_catalog_json.py
python3 scripts/validate_repos_yaml.py
python3 -m pytest -q
git diff --check
```

If `pytest` is unavailable, create a local virtual environment and install dev dependencies first:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
```
