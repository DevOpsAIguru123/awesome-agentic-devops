#!/usr/bin/env python3
"""Install official agent skills into a coding agent's skills directory.

Skills are sourced from the ``official-agent-skills`` repositories catalogued in
``data/repos.yaml`` (e.g. ``google/skills``, ``microsoft/skills``). A "skill" is
any directory containing a ``SKILL.md`` file; the installer copies that folder
into the target agent's skills location.

Currently supports Claude Code, the one agent with a native Agent Skills
mechanism. Other agents can be added as separate targets later.

Safety: dry-run by default. Nothing is written until ``--yes`` is passed. The
core install path (``--source owner/repo``) uses only the Python standard
library, so it runs in a bare ``python3`` without third-party packages.
"""

from __future__ import annotations

import argparse
import io
import shutil
import ssl
import tarfile
import urllib.error
import urllib.request
from pathlib import Path


def _ssl_context() -> ssl.SSLContext | None:
    """Default TLS context, falling back to certifi's CA bundle if the system
    store is unavailable (common on python.org macOS builds)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ModuleNotFoundError:
        return None

CATALOG_CATEGORY = "official-agent-skills"

# Agent -> skills target directory, by scope. Only agents with a real skills
# mechanism belong here; Claude Code is the first.
AGENT_TARGETS: dict[str, dict[str, Path]] = {
    "claude-code": {
        "global": Path.home() / ".claude" / "skills",
        "project": Path(".claude") / "skills",
    },
}


def load_catalog_sources(repos_path: Path) -> dict[str, str]:
    """Map catalog entry name -> ``owner/repo`` for official skill repos.

    Imports PyYAML lazily so the common ``--source owner/repo`` path stays
    dependency-free; only ``--list-sources`` / ``--source all`` need the catalog.
    """
    try:
        import yaml
    except ModuleNotFoundError:  # pragma: no cover - only hit without PyYAML
        raise SystemExit(
            "Reading the catalog needs PyYAML. Either 'pip install pyyaml' or "
            "pass an explicit --source owner/repo (e.g. --source google/skills)."
        )
    data = yaml.safe_load(repos_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"{repos_path} must contain a list of entries")
    sources: dict[str, str] = {}
    for entry in data:
        if str(entry.get("category", "")) != CATALOG_CATEGORY:
            continue
        url = str(entry.get("url", ""))
        if "github.com/" not in url:
            continue
        owner_repo = url.split("github.com/", 1)[1].strip("/")
        if owner_repo.endswith(".git"):
            owner_repo = owner_repo[: -len(".git")]
        if owner_repo.count("/") != 1:  # only plain owner/repo, not deep links
            continue
        sources[str(entry.get("name", owner_repo))] = owner_repo
    return sources


def _safe_extract(tar: tarfile.TarFile, dest: Path) -> None:
    dest_resolved = dest.resolve()
    for member in tar.getmembers():
        target = (dest / member.name).resolve()
        if dest_resolved != target and dest_resolved not in target.parents:
            raise SystemExit(f"unsafe path in archive: {member.name}")
    tar.extractall(dest)


def download_source(owner_repo: str, dest: Path) -> Path:
    """Download and extract a GitHub repo tarball; return the extracted root."""
    last_error: Exception | None = None
    for branch in ("main", "master"):
        url = f"https://codeload.github.com/{owner_repo}/tar.gz/refs/heads/{branch}"
        try:
            with urllib.request.urlopen(url, timeout=60, context=_ssl_context()) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 404:
                continue
            raise SystemExit(f"failed to download {owner_repo}: {exc}")
        except urllib.error.URLError as exc:  # network/DNS failure
            raise SystemExit(f"failed to reach GitHub for {owner_repo}: {exc}")
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
            _safe_extract(tar, dest)
        roots = [p for p in dest.iterdir() if p.is_dir()]
        if not roots:
            raise SystemExit(f"empty archive for {owner_repo}")
        return roots[0]
    raise SystemExit(f"could not download {owner_repo} (tried main, master): {last_error}")


def discover_skills(root: Path) -> list[tuple[str, Path]]:
    """Return sorted, name-deduplicated (skill_name, folder) pairs under root."""
    found: list[tuple[str, Path]] = [
        (skill_md.parent.name, skill_md.parent) for skill_md in root.rglob("SKILL.md")
    ]
    seen: set[str] = set()
    unique: list[tuple[str, Path]] = []
    for name, path in sorted(found, key=lambda item: item[0]):
        if name in seen:
            continue
        seen.add(name)
        unique.append((name, path))
    return unique


def plan_installs(
    skills: list[tuple[str, Path]], target_dir: Path, name_filter: str, force: bool
) -> list[tuple[str, Path, Path, str]]:
    """Return (name, src, dst, action) where action is 'install' or 'skip-exists'."""
    needle = name_filter.lower().strip()
    actions: list[tuple[str, Path, Path, str]] = []
    for name, src in skills:
        if needle and needle not in name.lower() and needle not in str(src).lower():
            continue
        dst = target_dir / name
        action = "skip-exists" if dst.exists() and not force else "install"
        actions.append((name, src, dst, action))
    return actions


def apply_installs(actions: list[tuple[str, Path, Path, str]]) -> list[Path]:
    written: list[Path] = []
    for _name, src, dst, action in actions:
        if action != "install":
            continue
        if dst.exists():
            shutil.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
        written.append(dst)
    return written


def resolve_target(agent: str, project: bool, override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    scope = "project" if project else "global"
    return AGENT_TARGETS[agent][scope]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install official agent skills into a coding agent's skills directory.",
    )
    parser.add_argument("--agent", default="claude-code", choices=sorted(AGENT_TARGETS))
    parser.add_argument(
        "--source",
        help="'owner/repo' (e.g. google/repo), a catalog entry name, or 'all' for every official skill repo.",
    )
    parser.add_argument("--repos", default="data/repos.yaml", help="Path to the catalog YAML.")
    parser.add_argument("--filter", default="", help="Only install skills whose name/path contains this substring.")
    parser.add_argument("--project", action="store_true", help="Install into ./.claude/skills instead of the global dir.")
    parser.add_argument("--target", help="Override the target skills directory entirely.")
    parser.add_argument("--list-sources", action="store_true", help="List official skill repos from the catalog and exit.")
    parser.add_argument("--list", action="store_true", help="List skills a source provides without installing.")
    parser.add_argument("--yes", action="store_true", help="Actually copy skills. Without this it is a dry run.")
    parser.add_argument("--force", action="store_true", help="Overwrite skills that already exist in the target.")
    return parser.parse_args(argv)


def resolve_sources(args: argparse.Namespace) -> list[str]:
    """Resolve --source into a list of owner/repo strings."""
    catalog = load_catalog_sources(Path(args.repos)) if Path(args.repos).exists() else {}
    if args.source == "all":
        if not catalog:
            raise SystemExit("no catalog found; cannot expand --source all")
        return sorted(set(catalog.values()))
    if args.source in catalog:  # a catalog entry name
        return [catalog[args.source]]
    if args.source and args.source.count("/") == 1:  # owner/repo
        return [args.source]
    raise SystemExit(f"unrecognized --source {args.source!r}; try --list-sources")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_sources:
        catalog = load_catalog_sources(Path(args.repos)) if Path(args.repos).exists() else {}
        if not catalog:
            print("No official skill sources found in the catalog.")
            return 0
        print("Official skill sources (use with --source):")
        for name, owner_repo in sorted(catalog.items()):
            print(f"  {owner_repo}")
        return 0

    if not args.source:
        print("Pick a source with --source. Available official skill repos:")
        catalog = load_catalog_sources(Path(args.repos)) if Path(args.repos).exists() else {}
        for owner_repo in sorted(set(catalog.values())):
            print(f"  {owner_repo}")
        print("\nExample: --agent claude-code --source google/skills --filter cloud --yes")
        return 2

    target = resolve_target(args.agent, args.project, args.target)
    owner_repos = resolve_sources(args)

    import tempfile

    all_actions: list[tuple[str, Path, Path, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        for owner_repo in owner_repos:
            root = download_source(owner_repo, Path(tmp) / owner_repo.replace("/", "_"))
            skills = discover_skills(root)
            all_actions.extend(plan_installs(skills, target, args.filter, args.force))

        if args.list:
            print(f"{len(all_actions)} skill(s) available from {', '.join(owner_repos)}:")
            for name, _src, _dst, _action in all_actions:
                print(f"  {name}")
            return 0

        installs = [a for a in all_actions if a[3] == "install"]
        skips = [a for a in all_actions if a[3] == "skip-exists"]

        print(f"Target: {target}")
        print(f"Source(s): {', '.join(owner_repos)}")
        print(f"{len(installs)} to install, {len(skips)} already present (use --force to overwrite).")
        for name, _src, dst, _action in installs:
            print(f"  install {name} -> {dst}")

        if not args.yes:
            print("\nDry run. Re-run with --yes to install.")
            return 0

        written = apply_installs(all_actions)
        print(f"\nInstalled {len(written)} skill(s) into {target}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
