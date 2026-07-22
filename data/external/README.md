# External catalog signals

External MCP catalogs are useful radar, but their scores are not curator
acceptance decisions. This directory stores generated sidecars that can enrich
reviews without changing the safety-scored source of truth in `data/repos.yaml`.

## Archestra signals

`data/external/archestra-signals.json` is generated from a local clone of
`archestra-ai/archestra`:

```bash
git clone --depth 1 https://github.com/archestra-ai/archestra.git /tmp/archestra
python scripts/import_archestra_signals.py \
  /tmp/archestra/mcp-catalog/data/mcp-evaluations
```

The generated file matches Archestra evaluation records to this catalog by
GitHub URL or remote MCP URL and records:

- external quality score;
- protocol feature booleans;
- local vs remote server type;
- sensitive and required sensitive config fields;
- OAuth presence;
- selected GitHub metadata from the external evaluation.

## Review rule

Use external signals as review prompts only. Before adding or changing a catalog
entry, still verify official ownership, freshness, action level, human approval,
evidence tracing, credential behavior, and blast radius from first-party sources.
