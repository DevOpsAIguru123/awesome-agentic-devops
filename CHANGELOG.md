# Changelog

All notable changes to this catalog — beyond routine entry additions, which are
tracked in the README's [Recently added](README.md#recently-added) table — are
documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **Container image release advisor.** Added a complete policy-driven reference
  pipeline with SonarCloud code analysis, pre-build Trivy configuration checks,
  exact-image vulnerability and secret scanning, three team-facing reports,
  deterministic release authorization, protected human approval, and Docker Hub
  publishing. Separate GitHub Actions workflows select either Google ADK with
  Vertex AI or Claude Agent SDK with Sonnet 5 for non-authoritative triage.

### Changed

- **Expanded pull request safety checklist.** The PR template now asks
  contributors to confirm no-secret-in-context handling, least-privilege
  credential guidance, approval gates, dry-run/preview behavior, audit evidence,
  rollback expectations, and telemetry/external API disclosure before review.
- **Hardened catalog schema validation.** Required string fields now reject blank
  values, and `labels` / `use_cases` must contain at least one non-empty string
  item so incomplete catalog rows fail locally before reaching README generation
  or CI.
- **Hardened catalog URL validation.** Catalog entries now require absolute
  `https://` URLs, blocking accidental relative links, bare hostnames, and
  insecure `http://` sources from entering the operator index.
- **Hardened write-capability label validation.** The catalog validator now
  rejects entries where `action_level: write-capable` and the README-facing
  `write` label drift apart, keeping blast-radius warnings consistent between
  `data/repos.yaml` and generated catalog tables.
- **Replaced the emoji evaluation labels with text badges.** The six glyphs
  (🟢 🟡 🔵 🛡️ 📊 ⚠️) are now readable tokens — `prod`, `prototype`, `mcp`,
  `approval`, `evidence`, `write` — across the legend, all catalog rows,
  `data/repos.yaml`, `docs/scoring.md`, and `docs/safety-model.md`. Scoring
  semantics are unchanged; the labels are now screen-reader accessible and
  searchable (you can Ctrl-F for `write`), and each label renders on its own line
  in the catalog. (#68)
