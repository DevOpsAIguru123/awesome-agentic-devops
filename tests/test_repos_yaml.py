from pathlib import Path

import pytest
import yaml

from scripts.validate_repos_yaml import (
    ALLOWED_ACTION_LEVELS,
    ALLOWED_MATURITY,
    REQUIRED_FIELDS,
    ValidationError,
    resolve_cli_path,
    validate_entries,
    validate_file,
)


def valid_entry(**overrides):
    entry = {
        "name": "antonbabenko/terraform-skill",
        "url": "https://github.com/antonbabenko/terraform-skill",
        "category": "terraform-iac-agents",
        "type": "agent",
        "framework": "unknown",
        "primary_language": "Python",
        "cloud_provider": "multi-cloud",
        "use_cases": ["terraform-plan-review"],
        "action_level": "proposal",
        "human_approval": True,
        "evidence_tracing": "partial",
        "maturity": "prototype",
        "risk_notes": "Requires review before use.",
        "operator_note": "Useful reference pattern.",
        "labels": ["🟡"],
    }
    entry.update(overrides)
    return entry


def test_validates_seed_data_file():
    entries = validate_file(Path("data/repos.yaml"))

    # Lower-bound check: catalog grows over time; avoid brittle equality.
    assert len(entries) >= 63
    assert all(field in entries[0] for field in REQUIRED_FIELDS)


def test_seed_data_has_unique_repo_names():
    entries = validate_file(Path("data/repos.yaml"))
    names = [entry["name"] for entry in entries]

    assert len(names) == len(set(names))


@pytest.mark.parametrize("action_level", sorted(ALLOWED_ACTION_LEVELS))
def test_accepts_allowed_action_levels(action_level):
    validate_entries([valid_entry(action_level=action_level)])


@pytest.mark.parametrize("maturity", sorted(ALLOWED_MATURITY))
def test_accepts_allowed_maturity_values(maturity):
    validate_entries([valid_entry(maturity=maturity)])


def test_rejects_missing_required_field():
    entry = valid_entry()
    del entry["risk_notes"]

    with pytest.raises(ValidationError, match="missing required field: risk_notes"):
        validate_entries([entry])


def test_rejects_invalid_action_level():
    entries = [valid_entry(action_level="autonomous-apply")]

    with pytest.raises(ValidationError, match="invalid action_level"):
        validate_entries(entries)


def test_rejects_labels_that_are_not_a_list():
    entries = [valid_entry(labels="🟡")]

    with pytest.raises(ValidationError, match="labels must be a list"):
        validate_entries(entries)


def test_rejects_non_list_yaml(tmp_path):
    yaml_path = tmp_path / "repos.yaml"
    yaml_path.write_text(yaml.safe_dump({"name": "not-a-list"}), encoding="utf-8")

    with pytest.raises(ValidationError, match="must contain a list"):
        validate_file(yaml_path)


def test_resolve_cli_path_rejects_working_tree_escape(tmp_path):
    untrusted_path = Path("../outside.yaml")
    root = tmp_path / "repo"
    with pytest.raises(ValidationError, match="escapes the working tree"):
        resolve_cli_path(untrusted_path, root=root)
