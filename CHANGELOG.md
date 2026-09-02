# Changelog

All notable changes to this catalog — beyond routine entry additions, which are
tracked in the README's [Recently added](README.md#recently-added) table — are
documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **Catalog external-signal guidance.** Added schema-reference guidance and
  regression coverage for using broad MCP indexes, registry mirrors, popularity
  dashboards, and third-party evaluations as discovery prompts rather than
  acceptance evidence or replacements for first-party source verification.
- **Catalog change decision guide.** Added schema-reference guidance and
  regression coverage for choosing whether a catalog PR should refresh, replace,
  add, downgrade, or remove a row based on canonical-source and operator-safety
  evidence.
- **Catalog deprecation/removal guidance.** Added schema-reference guidance and
  regression coverage for refreshing, downgrading, replacing, or removing
  archived, deprecated, unreachable, unsafe, or superseded catalog entries
  without preserving obsolete rows just to maintain counts.
- **Catalog risk-note writing guide.** Added contributor guidance and regression
  coverage for writing `risk_notes` as concrete operator warnings that name
  credential boundaries, write/telemetry risks, dry-run-first controls, approval
  expectations, and missing evidence.
- **Catalog freshness audit guidance.** The schema reference now tells
  contributors when and how to run the GitHub metadata audit, what report files
  it produces, how to treat stale or archived warnings, and when manual
  non-GitHub reachability checks are still required.
- **Catalog schema reference.** Added a validator-backed reference for required
  `data/repos.yaml` fields, allowed category slugs, artifact types, maturity
  values, evaluation labels, score-to-label invariants, and pre-submit commands
  so contributors can classify entries consistently before CI runs.
- **Catalog entry template.** Added a minimal `data/repos.yaml` entry template
  and review checklist to the schema reference so daily catalog additions start
  with safe defaults, top-level list placement, credential-scoping notes, and
  label-to-score consistency reminders.
- **Catalog source verification checklist.** Added reproducible pre-submit checks
  for reachability, freshness, tool surface, credential boundaries, and safety
  signals so catalog reviewers can validate entries from public evidence before
  trusting external indexes or marketing copy.
- **Catalog evidence capture worksheet.** Added a PR-ready source-evidence note
  template with harmless GitHub metadata checks and no-secret reminders so
  reviewers can reproduce catalog claims without exposing credentials.
- **Catalog identity rules.** Documented unique `name` and `url` expectations,
  canonical source selection, single-row use-case handling, and the narrow case
  where separate documentation and runnable artifact rows can coexist.
- **README synchronization rules.** Documented the README surfaces that must stay
  aligned with `data/repos.yaml`, including Recently added, catalog section
  tables, quick picks, top-picks guidance, and the README count check.
- **Operator safety checklist.** Added a practical preflight runbook for
  evaluating DevOps agents and MCP servers with read-only-first credentials,
  domain-specific credential boundaries, no-secret-in-context handling,
  dry-run/proposal gates, explicit approvals, blast-radius limits, and audit
  evidence before production-adjacent use.
- **Container image release advisor.** Added a complete policy-driven reference
  pipeline with SonarCloud code analysis, pre-build Trivy configuration checks,
  exact-image vulnerability and secret scanning, three team-facing reports,
  deterministic release authorization, protected human approval, and Docker Hub
  publishing. Separate GitHub Actions workflows select either Google ADK with
  Vertex AI or Claude Agent SDK with Sonnet 5 for non-authoritative triage.

### Changed

- **Guarded the operator safety checklist.** Added regression coverage so the
  read-only-first, no-secret-in-context, dry-run/proposal, approval, blast-radius,
  audit-evidence, and go/no-go guidance stays linked from the main entry points
  and remains present during future documentation edits.
- **Clarified catalog provenance classification.** The catalog schema reference now
  defines when `official-*` categories are appropriate versus `community-*`
  categories, and regression tests keep that contributor guidance present so
  ecosystem-adjacent tools are not misclassified as official sources.
- **Expanded the agent scorecard safety review.** The reusable scorecard now
  captures least-privilege credential scope, no-secret-in-context checks,
  redaction expectations, dry-run/preview commands, approval records, and audit
  artifacts, plus an explicit production-readiness decision, before recommending
  production-adjacent use.
- **Expanded pull request safety checklist.** The PR template now asks
  contributors to confirm schema-reference alignment, source-evidence capture,
  no-secret-in-context handling, least-privilege credential guidance, approval
  gates, dry-run/preview behavior, audit evidence, rollback expectations, and
  telemetry/external API disclosure before review.
- **Hardened catalog schema validation.** Required string fields now reject blank
  values, and `labels` / `use_cases` must contain at least one non-empty string
  item so incomplete catalog rows fail locally before reaching README generation
  or CI.
- **Hardened score-to-label consistency.** The catalog validator now keeps
  README-facing `approval` and `evidence` labels synchronized with the structured
  `human_approval` and `evidence_tracing` fields, preventing safety and audit
  signals from drifting between `data/repos.yaml` and the public tables.
- **Hardened catalog URL validation.** Catalog entries now require absolute
  `https://` URLs, blocking accidental relative links, bare hostnames, and
  insecure `http://` sources from entering the operator index.
- **Hardened contributor label guidance.** The contribution checklist now names the
  allowed evaluation-label tokens alongside the validator allowlist, making label
  review expectations clear before contributors edit `data/repos.yaml`.
- **Hardened catalog label validation.** Evaluation labels are now restricted to
  the documented text badges (`prod`, `prototype`, `mcp`, `approval`,
  `evidence`, `write`) so typos and legacy label names fail in local validation
  before they can drift into the README.
- **Hardened catalog category validation.** Catalog entries must use one of the
  curated category slugs, and tests now require the validator allowlist to stay
  synchronized with the categories currently used in `data/repos.yaml`, preventing
  README/YAML drift from typos or new sections that lack matching tests and
  public documentation.
- **Hardened catalog type validation.** Catalog entries must use one of the
  curated artifact kinds, and tests now require the validator allowlist to stay
  synchronized with the `type` values currently used in `data/repos.yaml`,
  preventing ambiguous or misspelled tool-surface metadata.
- **Hardened write-capability label validation.** The catalog validator now
  rejects entries where `action_level: write-capable` and the README-facing
  `write` label drift apart, keeping blast-radius warnings consistent between
  `data/repos.yaml` and generated catalog tables.
- **Hardened maturity label validation.** The catalog validator now rejects rows
  that mix `prod` and `prototype` labels, and rejects `maturity: prototype` rows
  that omit `prototype` or use `prod`, forcing contributors to keep beta and
  experimental entries aligned with README readiness shorthand.
- **Expanded GitHub repository freshness audits.** The audit script now flags
  GitHub repos with no pushes in the configured freshness window (`--stale-days`,
  default 365), alongside reachability, archived/private, and language-drift
  warnings.
- **Replaced the emoji evaluation labels with text badges.** The six glyphs
  (🟢 🟡 🔵 🛡️ 📊 ⚠️) are now readable tokens — `prod`, `prototype`, `mcp`,
  `approval`, `evidence`, `write` — across the legend, all catalog rows,
  `data/repos.yaml`, `docs/scoring.md`, and `docs/safety-model.md`. Scoring
  semantics are unchanged; the labels are now screen-reader accessible and
  searchable (you can Ctrl-F for `write`), and each label renders on its own line
  in the catalog. (#68)
