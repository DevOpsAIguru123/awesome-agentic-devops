import json
from pathlib import Path

import pytest

from scripts.audit_github_repos import (
    AuditResult,
    audit_repo,
    build_summary,
    parse_github_repo,
    write_report,
)


def test_parse_github_repo_from_url_and_name():
    assert parse_github_repo("https://github.com/antonbabenko/terraform-skill") == (
        "antonbabenko",
        "terraform-skill",
    )
    assert parse_github_repo("antonbabenko/terraform-skill") == (
        "antonbabenko",
        "terraform-skill",
    )


def test_parse_github_repo_rejects_non_github_url():
    with pytest.raises(ValueError, match="not a GitHub repo"):
        parse_github_repo("https://gitlab.com/antonbabenko/terraform-skill")


def test_audit_repo_captures_metadata_from_gh_json():
    payload = {
        "nameWithOwner": "antonbabenko/terraform-skill",
        "url": "https://github.com/antonbabenko/terraform-skill",
        "isArchived": False,
        "isPrivate": False,
        "defaultBranchRef": {"name": "main"},
        "pushedAt": "2026-07-01T00:00:00Z",
        "primaryLanguage": {"name": "Python"},
        "description": "Terraform skill repo",
        "stargazerCount": 42,
    }

    def runner(_cmd):
        return 0, json.dumps(payload), ""

    result = audit_repo(
        {"name": "antonbabenko/terraform-skill", "url": payload["url"]},
        runner=runner,
    )

    assert result.reachable is True
    assert result.default_branch == "main"
    assert result.primary_language == "Python"
    assert result.stars == 42
    assert result.error == ""


def test_audit_repo_records_unreachable_repo():
    def runner(_cmd):
        return 1, "", "Could not resolve to a Repository"

    result = audit_repo(
        {
            "name": "rohitg00/awesome-devops-mcp-servers",
            "url": "https://github.com/rohitg00/awesome-devops-mcp-servers",
        },
        runner=runner,
    )

    assert result.reachable is False
    assert result.error == "Could not resolve to a Repository"


def test_build_summary_counts_reachability_and_archived_repos():
    results = [
        AuditResult(
            name="antonbabenko/terraform-skill",
            url="https://github.com/antonbabenko/terraform-skill",
            reachable=True,
        ),
        AuditResult(
            name="microsoft/azure-devops-skills",
            url="https://github.com/microsoft/azure-devops-skills",
            reachable=True,
            archived=True,
        ),
        AuditResult(
            name="rohitg00/awesome-devops-mcp-servers",
            url="https://github.com/rohitg00/awesome-devops-mcp-servers",
            reachable=False,
            error="missing",
        ),
    ]

    summary = build_summary(results)

    assert summary["total"] == 3
    assert summary["reachable"] == 2
    assert summary["unreachable"] == 1
    assert summary["archived"] == 1


def test_write_report_outputs_json_and_markdown(tmp_path):
    result = AuditResult(
        name="antonbabenko/terraform-skill",
        url="https://github.com/antonbabenko/terraform-skill",
        reachable=True,
        primary_language="Python",
    )

    json_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"
    write_report([result], json_path=json_path, markdown_path=markdown_path)

    report = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert report["summary"]["total"] == 1
    assert report["results"][0]["name"] == "antonbabenko/terraform-skill"
    assert "| antonbabenko/terraform-skill | yes |" in markdown
