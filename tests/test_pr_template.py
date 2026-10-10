from pathlib import Path

PR_TEMPLATE = Path(".github/PULL_REQUEST_TEMPLATE.md")


def _template_text() -> str:
    return PR_TEMPLATE.read_text(encoding="utf-8")


def test_pr_template_points_catalog_submitters_to_schema_reference():
    text = _template_text()

    assert "catalog schema reference" in text
    assert "docs/catalog-schema.md" in text
    assert "docs/catalog-schema.md#evidence-capture-worksheet" in text
    assert "data/repos.yaml" in text
    assert "README.md" in text


def test_pr_template_validation_block_includes_core_local_checks():
    text = _template_text()

    expected_commands = (
        "python3 scripts/validate_repos_yaml.py",
        "python3 scripts/sync_readme_counts.py --check",
        "python3 scripts/sync_catalog_json.py --check",
        "python3 -m pytest -q",
        "python3 scripts/run_mock_eval_scenarios.py",
        "python3 scripts/audit_github_repos.py --workers 12 --fail-on-unreachable",
    )
    for command in expected_commands:
        assert command in text
