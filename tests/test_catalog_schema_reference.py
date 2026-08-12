from pathlib import Path

from scripts.validate_repos_yaml import (
    ALLOWED_CATEGORIES,
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


def test_catalog_schema_reference_lists_allowed_categories():
    text = _schema_text()

    for category in ALLOWED_CATEGORIES:
        assert f"`{category}`" in text


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
