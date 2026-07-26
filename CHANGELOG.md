# Changelog

All notable changes to this catalog — beyond routine entry additions, which are
tracked in the README's [Recently added](README.md#recently-added) table — are
documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- **Replaced the emoji evaluation labels with text badges.** The six glyphs
  (🟢 🟡 🔵 🛡️ 📊 ⚠️) are now readable tokens — `prod`, `prototype`, `mcp`,
  `approval`, `evidence`, `write` — across the legend, all catalog rows,
  `data/repos.yaml`, `docs/scoring.md`, and `docs/safety-model.md`. Scoring
  semantics are unchanged; the labels are now screen-reader accessible and
  searchable (you can Ctrl-F for `write`), and each label renders on its own line
  in the catalog. (#68)
