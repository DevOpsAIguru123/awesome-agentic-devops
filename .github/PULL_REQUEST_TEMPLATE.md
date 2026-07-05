## Summary

<!-- What entry, category, or docs change does this PR add or update? -->

## Entry checklist (skip if this PR doesn't add/change a catalog entry)

- [ ] The repo URL is public and reachable.
- [ ] The entry has a specific category.
- [ ] The `risk_notes` field explains what could go wrong.
- [ ] The `operator_note` field explains why an infrastructure operator should care.
- [ ] The `gemini_opportunity` field describes a concrete Gemini-compatible build or evaluation path.
- [ ] Labels match the observed behavior, not marketing claims.
- [ ] `data/repos.yaml` and `README.md` are both updated.

## Validation

```bash
python scripts/validate_repos_yaml.py
pytest -q
python scripts/run_mock_eval_scenarios.py
python scripts/audit_github_repos.py --workers 12 --fail-on-unreachable
```

- [ ] All of the above pass locally.
