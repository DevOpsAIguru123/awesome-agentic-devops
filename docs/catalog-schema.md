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

## Allowed categories

Category slugs define the curated README sections and are validated in CI:

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
