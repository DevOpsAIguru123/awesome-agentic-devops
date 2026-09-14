## Summary

<!-- What entry, category, or docs change does this PR add or update? -->

## Entry checklist (skip if this PR doesn't add/change a catalog entry)

- [ ] The repo URL is public and reachable.
- [ ] The entry has a specific category.
- [ ] Required fields, category slug, artifact type, maturity, and labels match the [catalog schema reference](../docs/catalog-schema.md).
- [ ] Source evidence is captured in the PR body using the worksheet in the [catalog schema reference](../docs/catalog-schema.md#evidence-capture-worksheet).
- [ ] The `risk_notes` field explains what could go wrong.
- [ ] The `operator_note` field explains why an infrastructure operator should care.
- [ ] Labels match the observed behavior, not marketing claims.
- [ ] `data/repos.yaml` and `README.md` are both updated.

## Safety checklist

- [ ] No secrets, tokens, kubeconfigs, customer data, or private logs are included in the PR, fixtures, screenshots, or generated artifacts.
- [ ] Write-capable tools document approval gates, dry-run or preview behavior, audit/evidence output, and rollback expectations.
- [ ] Credential guidance uses least privilege and separates read-only credentials from write-capable credentials.
- [ ] Any new telemetry, hosted service, or external API dependency is disclosed with operator-facing risk notes.

## Validation

```bash
python scripts/validate_repos_yaml.py
python scripts/sync_readme_counts.py --check
python -m pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```

- [ ] Relevant commands above pass locally, or this PR explains why a command is not applicable.
