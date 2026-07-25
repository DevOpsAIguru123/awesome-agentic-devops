#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

import yaml


GH_FIELDS = (
    "nameWithOwner,url,isArchived,isPrivate,defaultBranchRef,pushedAt,"
    "primaryLanguage,description,stargazerCount"
)
Runner = Callable[[list[str]], tuple[int, str, str]]


@dataclass
class AuditResult:
    name: str
    url: str
    reachable: bool
    skipped: bool = False
    archived: bool | None = None
    private: bool | None = None
    default_branch: str = ""
    pushed_at: str = ""
    primary_language: str = ""
    description: str = ""
    stars: int | None = None
    error: str = ""
    warnings: list[str] = field(default_factory=list)


def resolve_cli_path(path: Path, root: Path | None = None) -> Path:
    """Resolve a CLI path and require it to remain inside the working tree."""
    allowed_root = (root or Path.cwd()).resolve()
    candidate = path.expanduser()
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (allowed_root / candidate).resolve()
    )
    try:
        resolved.relative_to(allowed_root)
    except ValueError as exc:
        raise ValueError(f"path escapes the working tree: {path}") from exc
    return resolved


def parse_github_repo(value: str) -> tuple[str, str]:
    if value.startswith(("http://", "https://")):
        parsed = urlparse(value)
        if parsed.netloc.lower() != "github.com":
            raise ValueError(f"{value!r} is not a GitHub repo URL")
        parts = [part for part in parsed.path.split("/") if part]
    else:
        parts = [part for part in value.split("/") if part]

    if len(parts) < 2:
        raise ValueError(f"{value!r} is not a GitHub repo reference")
    return parts[0], parts[1]


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def _field_warnings(entry: dict[str, Any], metadata: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    expected_language = str(entry.get("primary_language", "")).strip()
    actual_language = (metadata.get("primaryLanguage") or {}).get("name") or ""

    if expected_language and expected_language.lower() not in {"unknown", "markdown"}:
        if actual_language and actual_language.lower() != expected_language.lower():
            warnings.append(
                f"primary_language is {expected_language!r}, GitHub reports {actual_language!r}"
            )

    if metadata.get("isArchived"):
        warnings.append("repository is archived")
    if metadata.get("isPrivate"):
        warnings.append("repository is private")

    return warnings


def audit_repo(entry: dict[str, Any], runner: Runner = run_command) -> AuditResult:
    name = str(entry["name"])
    url = str(entry["url"])
    try:
        owner, repo = parse_github_repo(url)
    except ValueError as exc:
        return AuditResult(
            name=name,
            url=url,
            reachable=False,
            skipped=True,
            error=str(exc),
            warnings=["skipped: not a GitHub repository"],
        )

    repo_ref = f"{owner}/{repo}"
    cmd = ["gh", "repo", "view", repo_ref, "--json", GH_FIELDS]
    returncode, stdout, stderr = runner(cmd)

    if returncode != 0:
        return AuditResult(
            name=name,
            url=url,
            reachable=False,
            error=(stderr or stdout).strip(),
        )

    try:
        metadata = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return AuditResult(
            name=name,
            url=url,
            reachable=False,
            error=f"invalid gh JSON output: {exc}",
        )

    default_branch = metadata.get("defaultBranchRef") or {}
    primary_language = metadata.get("primaryLanguage") or {}
    return AuditResult(
        name=name,
        url=metadata.get("url") or url,
        reachable=True,
        archived=metadata.get("isArchived"),
        private=metadata.get("isPrivate"),
        default_branch=default_branch.get("name") or "",
        pushed_at=metadata.get("pushedAt") or "",
        primary_language=primary_language.get("name") or "",
        description=metadata.get("description") or "",
        stars=metadata.get("stargazerCount"),
        warnings=_field_warnings(entry, metadata),
    )


def load_entries(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a list")
    return data


def audit_entries(entries: list[dict[str, Any]], workers: int) -> list[AuditResult]:
    results: list[AuditResult] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(audit_repo, entry) for entry in entries]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda result: result.name.lower())


def build_summary(results: list[AuditResult]) -> dict[str, int]:
    return {
        "total": len(results),
        "reachable": sum(1 for result in results if result.reachable),
        "unreachable": sum(
            1 for result in results if not result.reachable and not result.skipped
        ),
        "skipped": sum(1 for result in results if result.skipped),
        "archived": sum(1 for result in results if result.archived),
        "with_warnings": sum(1 for result in results if result.warnings),
    }


def _markdown_row(result: AuditResult) -> str:
    if result.skipped:
        reachable = "skipped"
    else:
        reachable = "yes" if result.reachable else "no"

    if result.archived is None:
        archived = ""
    else:
        archived = "yes" if result.archived else "no"
    warnings = "; ".join(result.warnings) if result.warnings else result.error
    return (
        f"| {result.name} | {reachable} | {archived} | "
        f"{result.primary_language} | {result.pushed_at} | {warnings} |"
    )


def write_report(
    results: list[AuditResult],
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "summary": build_summary(results),
        "results": [asdict(result) for result in results],
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# GitHub Repo Audit",
        "",
        "| Repo | Reachable | Archived | Language | Pushed at | Warnings/errors |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(_markdown_row(result) for result in results)
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GitHub repos in data/repos.yaml")
    parser.add_argument("--data", type=Path, default=Path("data/repos.yaml"))
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("reports/github-repo-audit.json"),
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=Path("reports/github-repo-audit.md"),
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--fail-on-unreachable", action="store_true")
    args = parser.parse_args()

    try:
        data_path = resolve_cli_path(args.data)
        json_path = resolve_cli_path(args.json_output)
        markdown_path = resolve_cli_path(args.markdown_output)
    except ValueError as exc:
        parser.error(str(exc))

    entries = load_entries(data_path)
    results = audit_entries(entries, workers=max(1, args.workers))
    write_report(results, json_path=json_path, markdown_path=markdown_path)

    summary = build_summary(results)
    print(
        "GitHub audit complete: "
        f"{summary['reachable']}/{summary['total']} reachable, "
        f"{summary['skipped']} skipped, "
        f"{summary['archived']} archived, "
        f"{summary['with_warnings']} with warnings"
    )
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")

    if args.fail_on_unreachable and summary["unreachable"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
