# Contributing

Thanks for helping make this a practical operator-grade index instead of a hype list.

## Contribution rules

- No hype-only entries.
- Identify the real DevOps, Cloud, SRE, Kubernetes, Terraform, CI/CD, or platform engineering use case.
- Classify the action level as `read-only`, `proposal`, `write-capable`, or `unknown`.
- Note the safety and approval model.
- Include evidence of activity, documentation, examples, or implementation detail.
- Disclose if the project is commercial-only or if key functionality is not available in OSS form.
- Do not include tools that require unsafe credential practices.
- Prefer entries that can be evaluated without real cloud credentials.
- For write-capable, credentialed, or production-adjacent entries, use the [operator safety checklist](docs/operator-safety-checklist.md) to confirm domain-specific least-privilege credential boundaries, no-secret-in-context handling, dry-run/proposal behavior, approval gates, blast-radius limits, and audit evidence.
- PRs should update [data/repos.yaml](data/repos.yaml) and [README.md](README.md) when the public index changes.
- Use the [catalog schema reference](docs/catalog-schema.md) when choosing category slugs, artifact types, maturity values, and evaluation labels.

## Entry checklist

- The repo URL is public and reachable.
- The entry has a specific category.
- The `category` value is one of the existing catalog slugs validated by `scripts/validate_repos_yaml.py`; add a new slug only when you are also adding the matching README section and tests.
- The `type` value uses one of the validator-backed artifact kinds, such as `mcp-server`, `hosted-mcp-server`, `documentation`, `sdk`, `skill`, or `skill-library`; add a new kind only when the existing set cannot describe the artifact clearly.
- The `risk_notes` field explains what could go wrong.
- The `operator_note` field explains why an infrastructure operator should care.
- Labels match the observed behavior, not marketing claims.
- `labels` uses only the current evaluation tokens: `prod`, `prototype`, `mcp`, `approval`, `evidence`, and `write`.
- Keep README-facing labels synchronized with structured scores: `human_approval: true` requires `approval`; `evidence_tracing: yes` requires `evidence`; `evidence` is allowed only for `yes` or `partial` evidence tracing; and `write` is allowed only with `action_level: write-capable`.
- Do not combine `prod` and `prototype` on the same entry; choose the stricter maturity signal that matches the evidence.

## Local validation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/validate_repos_yaml.py
python scripts/sync_readme_counts.py
pytest -q
```

`sync_readme_counts.py` refreshes the entry/category counts in the README intro from `data/repos.yaml`, so you never edit those numbers by hand.

For a deeper freshness check before substantial catalog work, run `python scripts/audit_github_repos.py --stale-days 365`; it writes JSON and Markdown reports under `reports/` and warns on unreachable, archived, private, language-drifted, or stale GitHub repositories.
