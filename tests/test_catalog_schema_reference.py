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


def test_catalog_schema_reference_documents_identity_and_duplicate_rules():
    text = _schema_text()

    assert "## Identity and duplicate rules" in text
    assert "`name` must be unique" in text
    assert "`url` must be unique" in text
    assert "canonical" in text
    assert "Do not add a second row for the same artifact" in text
    assert "Separate documentation and runnable surfaces" in text


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
