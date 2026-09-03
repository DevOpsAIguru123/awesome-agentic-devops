from pathlib import Path

from scripts.validate_repos_yaml import (
    ALLOWED_ACTION_LEVELS,
    ALLOWED_CATEGORIES,
    ALLOWED_EVIDENCE_TRACING,
    ALLOWED_HUMAN_APPROVAL,
    ALLOWED_LABELS,
    ALLOWED_MATURITY,
    ALLOWED_TYPES,
    REQUIRED_FIELDS,
)

SCHEMA_DOC = Path("docs/catalog-schema.md")


def _schema_text() -> str:
    return SCHEMA_DOC.read_text(encoding="utf-8")


def test_catalog_schema_reference_lists_required_fields():
    text = _schema_text()

    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in text


def test_catalog_schema_reference_documents_catalog_change_decision_guide():
    text = _schema_text()

    assert "## Catalog change decision guide" in text
    assert "smallest safe catalog change" in text
    assert "**Refresh**" in text
    assert "**Replace**" in text
    assert "**Add**" in text
    assert "**Downgrade**" in text
    assert "**Remove**" in text
    assert "evidence worksheet" in text


def test_catalog_schema_reference_documents_identity_and_duplicate_rules():
    text = _schema_text()

    assert "## Identity and duplicate rules" in text
    assert "`name` must be unique" in text
    assert "`url` must be unique" in text
    assert "canonical" in text
    assert "Do not add a second row for the same artifact" in text
    assert "Separate documentation and runnable surfaces" in text


def test_catalog_schema_reference_documents_readme_synchronization_rules():
    text = _schema_text()

    assert "## README synchronization rules" in text
    assert "python3 scripts/sync_readme_counts.py" in text
    assert "python3 scripts/sync_readme_counts.py --check" in text
    assert "## Recently added" in text
    assert "matching catalog section table" in text
    assert "intro quick-pick table" in text
    assert "## Top picks by use case" in text


def test_catalog_schema_reference_lists_allowed_categories():
    text = _schema_text()

    for category in ALLOWED_CATEGORIES:
        assert f"`{category}`" in text


def test_catalog_schema_reference_documents_category_provenance():
    text = _schema_text()

    assert "`official-*`" in text
    assert "first-party vendor" in text
    assert "`community-*`" in text
    assert "not governed by the vendor/project" in text


def test_catalog_schema_reference_includes_minimal_entry_template():
    text = _schema_text()

    assert "## Minimal entry template" in text
    assert "add this as a new top-level list item" in text
    assert "```yaml" in text
    assert "- name: owner/repo-or-doc-name" in text
    assert "action_level: read-only" in text
    assert "labels:" in text
    assert "- mcp" in text
    assert "Template review checklist" in text
    assert "do not paste" in text


def test_catalog_schema_reference_includes_source_verification_checklist():
    text = _schema_text()

    assert "## Source verification checklist" in text
    assert "without secrets" in text
    assert "Reachability" in text
    assert "Freshness" in text
    assert "not archived" in text
    assert "Tool surface" in text
    assert "Credential boundary" in text
    assert "Safety signals" in text


def test_catalog_schema_reference_includes_safety_score_evidence_rules():
    text = _schema_text()

    assert "### Safety-score evidence rules" in text
    assert "category assumptions or marketing language" in text
    assert "`action_level: read-only`" in text
    assert "`action_level: write-capable`" in text
    assert "create," in text
    assert "rotate, acknowledge, remediate" in text
    assert "`human_approval: true` only when" in text
    assert "explicit approval gate" in text
    assert "`evidence_tracing: \"yes\"` or `partial`" in text
    assert "durable traces" in text
    assert "Keep labels synchronized" in text


def test_catalog_schema_reference_includes_hosted_mcp_credential_boundary_guidance():
    text = _schema_text()

    assert "### Hosted MCP credential boundary guidance" in text
    assert "`hosted-mcp-server`" in text
    assert "Authentication mode" in text
    assert "OAuth" in text
    assert "Scope boundary" in text
    assert "read-only endpoint" in text
    assert "Data handling" in text
    assert "prompts, tool arguments, logs, traces" in text
    assert "disposable workspaces" in text
    assert "never paste tokens" in text
    assert "most privileged documented capability" in text


def test_catalog_schema_reference_includes_external_signal_guidance():
    text = _schema_text()

    assert "### External index and evaluation signals" in text
    assert "not catalog" in text
    assert "acceptance evidence by themselves" in text
    assert "review prompts" in text
    assert "first-party" in text
    assert "generated sidecars" in text
    assert "Do not let third-party scores override the local rubric" in text
    assert "pull request evidence worksheet" in text


def test_catalog_schema_reference_includes_risk_notes_writing_guide():
    text = _schema_text()

    assert "### Risk notes writing guide" in text
    assert "short operator warning" in text
    assert "credential boundary" in text
    assert "write capability" in text
    assert "telemetry" in text
    assert "dry-run, proposal, preview, or plan-only" in text
    assert "missing evidence" in text
    assert "risk_notes: Use a read-only GitHub token" in text


def test_catalog_schema_reference_includes_github_freshness_audit_guidance():
    text = _schema_text()

    assert "### Automated GitHub freshness audit" in text
    assert "python3 scripts/audit_github_repos.py --stale-days 365" in text
    assert "reports/github-repo-audit.json" in text
    assert "reports/github-repo-audit.md" in text
    assert "reachability, archived/private status" in text
    assert "do not commit the reports" in text
    assert "non-GitHub documentation and hosted MCP endpoints" in text


def test_catalog_schema_reference_includes_deprecation_and_removal_guidance():
    text = _schema_text()

    assert "### Deprecation and removal handling" in text
    assert "archived, deprecated, unreachable" in text
    assert "current official successor" in text
    assert "lower the maturity or" in text
    assert "explain the archived, deprecated, or unsupported" in text
    assert "Remove a row when the source is unreachable" in text
    assert "Never preserve an obsolete entry just to maintain README counts" in text


def test_catalog_schema_reference_includes_evidence_capture_worksheet():
    text = _schema_text()

    assert "### Evidence capture worksheet" in text
    assert "pull request body" in text
    assert "Source evidence:" in text
    assert "Canonical source" in text
    assert "Reachability check" in text
    assert "Credential boundary" in text
    assert "gh repo view OWNER/REPO --json" in text
    assert "Do not include access tokens" in text


def test_catalog_schema_reference_lists_allowed_action_levels():
    text = _schema_text()

    for action_level in ALLOWED_ACTION_LEVELS:
        assert f"`{action_level}`" in text


def test_catalog_schema_reference_lists_allowed_human_approval_values():
    text = _schema_text()

    expected_values = {
        "true" if value is True else "false" if value is False else value
        for value in ALLOWED_HUMAN_APPROVAL
    }
    for human_approval in expected_values:
        assert f"`{human_approval}`" in text


def test_catalog_schema_reference_lists_allowed_evidence_tracing_values():
    text = _schema_text()

    for evidence_tracing in ALLOWED_EVIDENCE_TRACING:
        assert f"`{evidence_tracing}`" in text


def test_catalog_schema_reference_lists_allowed_artifact_types():
    text = _schema_text()

    for artifact_type in ALLOWED_TYPES:
        assert f"`{artifact_type}`" in text


def test_catalog_schema_reference_lists_allowed_maturity_values():
    text = _schema_text()

    for maturity in ALLOWED_MATURITY:
        assert f"`{maturity}`" in text


def test_catalog_schema_reference_lists_allowed_evaluation_labels():
    text = _schema_text()

    for label in ALLOWED_LABELS:
        assert f"`{label}`" in text
