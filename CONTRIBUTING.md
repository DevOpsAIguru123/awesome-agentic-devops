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
- PRs should update [data/repos.yaml](data/repos.yaml) and [README.md](README.md) when the public index changes.

## Entry checklist

- The repo URL is public and reachable.
- The entry has a specific category.
- The `risk_notes` field explains what could go wrong.
- The `operator_note` field explains why an infrastructure operator should care.
- Labels match the observed behavior, not marketing claims.

## Local validation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/validate_repos_yaml.py
pytest -q
```

You do not need to touch the entry/category counts in the README intro: the `sync-readme-counts` CI job recomputes them from `data/repos.yaml` and commits the fix automatically. To sync them locally anyway, run `python scripts/sync_readme_counts.py`.
