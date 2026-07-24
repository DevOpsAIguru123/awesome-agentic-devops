# Catalog data files

The repository keeps `data/repos.yaml` as the hand-curated source of truth and
projects it into JSON files for automation.

## `data/catalog.json`

`data/catalog.json` is intentionally small. It contains only installable agent
skill sources used by `scripts/install_skills.py`, so the installer can run on a
stock Python interpreter without PyYAML.

Regenerate it with:

```bash
python scripts/sync_catalog_json.py
```

Check it in CI with:

```bash
python scripts/sync_catalog_json.py --check
```

## `data/catalog.full.json`

`data/catalog.full.json` is the full machine-readable public catalog. It mirrors
all entries from `data/repos.yaml` and keeps the operator safety model grouped
under a `safety` object:

```json
{
  "name": "PagerDuty/pagerduty-mcp-server",
  "category": "official-sre-mcp-servers",
  "use_cases": ["incident-management"],
  "safety": {
    "action_level": "write-capable",
    "human_approval": true,
    "evidence_tracing": "partial",
    "maturity": "production-adjacent",
    "risk_notes": "..."
  }
}
```

This file is meant for:

- static search/filter UIs;
- MCP catalog servers;
- dashboards and badges;
- downstream audits and comparison tools;
- consumers that want the full safety-scored catalog without parsing YAML.

Regenerate it with:

```bash
python scripts/sync_full_catalog_json.py
```

Check it in CI with:

```bash
python scripts/sync_full_catalog_json.py --check
```

## Editing rule

Do not hand-edit generated JSON files. Update `data/repos.yaml`, then run the
sync scripts and commit the generated changes together.
