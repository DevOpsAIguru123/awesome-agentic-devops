#!/usr/bin/env python3
"""Install official agent skills into a coding agent, cross-platform.

Skills are sourced from the ``official-agent-skills`` repositories catalogued in
``data/repos.yaml`` (e.g. ``google/skills``, ``microsoft/skills``). A "skill" is
any directory containing a ``SKILL.md``; the installer copies that folder whole.

Agents:
- claude-code  : native Agent Skills -> ~/.claude/skills (or ./.claude/skills with --project)
- cursor       : skill folders -> ./.agent-skills + a .cursor/rules pointer file
- codex        : skill folders -> ./.agent-skills + an AGENTS.md pointer block
- antigravity  : skill folders -> ./.agent-skills + an AGENTS.md pointer block
- vscode       : skill folders -> ./.agent-skills + a .github/copilot-instructions.md pointer block

Only Claude Code loads SKILL.md folders natively; the others get the real skill
folders in a shared ./.agent-skills directory plus a pointer written into their
own always-on instructions file (approach A: one copy of the content, native
pointer per agent).

Installs directly (no confirmation step) since skill folders are additive and
reversible. Use --dry-run to preview. The core path (--source owner/repo) uses
only the standard library; PyYAML is needed only for --list-sources/--source all.
"""

from __future__ import annotations

import argparse
import io
import shutil
import ssl
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

CATALOG_CATEGORY = "official-agent-skills"
SHARED_SKILLS_DIR = Path(".agent-skills")
POINTER_BEGIN = "<!-- BEGIN awesome-agentic-devops skills -->"
POINTER_END = "<!-- END awesome-agentic-devops skills -->"

# Per-agent install strategy.
#   native : SKILL.md folders the agent loads directly (Claude Code).
#   pointer: folders copied to a shared dir + an instructions file that points at them.
AGENTS: dict[str, dict[str, object]] = {
    "claude-code": {
        "mode": "native",
        "skills_global": Path.home() / ".claude" / "skills",
        "skills_project": Path(".claude") / "skills",
    },
    "cursor": {
        "mode": "pointer",
        "pointer": Path(".cursor") / "rules" / "awesome-agentic-devops-skills.mdc",
        "pointer_kind": "cursor",
    },
    "codex": {
        "mode": "pointer",
        "pointer": Path("AGENTS.md"),
        "pointer_kind": "agents",
    },
    "antigravity": {
        "mode": "pointer",
        "pointer": Path("AGENTS.md"),
        "pointer_kind": "agents",
    },
    "vscode": {
        "mode": "pointer",
        "pointer": Path(".github") / "copilot-instructions.md",
        "pointer_kind": "copilot",
    },
}


# ---------------------------------------------------------------------------
# Catalog + source fetch
# ---------------------------------------------------------------------------
def load_catalog_sources(repos_path: Path) -> dict[str, str]:
    """Map catalog entry name -> ``owner/repo`` for official skill repos.

    PyYAML is imported lazily so the ``--source owner/repo`` path stays
    dependency-free.
    """
    try:
        import yaml
    except ModuleNotFoundError:  # pragma: no cover - only without PyYAML
        raise SystemExit(
            "Reading the catalog needs PyYAML. Either 'pip install pyyaml' or "
            "pass --source owner/repo (e.g. --source google/skills)."
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
        if owner_repo.count("/") != 1:
            continue
        sources[str(entry.get("name", owner_repo))] = owner_repo
    return sources


def _ssl_context() -> ssl.SSLContext | None:
    """Default TLS context, falling back to certifi if the system store is
    unavailable (common on python.org macOS builds)."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ModuleNotFoundError:
        return None


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
        except urllib.error.URLError as exc:
            raise SystemExit(f"failed to reach GitHub for {owner_repo}: {exc}")
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
            _safe_extract(tar, dest)
        roots = [p for p in dest.iterdir() if p.is_dir()]
        if not roots:
            raise SystemExit(f"empty archive for {owner_repo}")
        return roots[0]
    raise SystemExit(f"could not download {owner_repo} (tried main, master): {last_error}")


# ---------------------------------------------------------------------------
# Skill discovery / plan / copy
# ---------------------------------------------------------------------------
# Folder names that hold a SKILL.md but are scaffolding, not a real skill.
SKILL_NAME_IGNORE = {"template", "templates", "example", "examples"}


def discover_skills(root: Path) -> list[tuple[str, Path]]:
    """Return sorted, name-deduplicated (skill_name, folder) pairs under root."""
    found = [
        (skill_md.parent.name, skill_md.parent)
        for skill_md in root.rglob("SKILL.md")
        if skill_md.parent.name.lower() not in SKILL_NAME_IGNORE
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


# ---------------------------------------------------------------------------
# Agent targets + pointer files
# ---------------------------------------------------------------------------
def agent_skills_dir(agent: str, project: bool, override: str | None) -> Path:
    """Where an agent's skill folders are copied."""
    if override:
        return Path(override).expanduser()
    spec = AGENTS[agent]
    if spec["mode"] == "native":
        return spec["skills_project"] if project else spec["skills_global"]  # type: ignore[return-value]
    return SHARED_SKILLS_DIR


def render_pointer(agent: str, skill_names: list[str], skills_dir: Path) -> str:
    """Render the managed pointer body for a pointer-mode agent."""
    listing = "\n".join(f"- `{skills_dir}/{name}/SKILL.md`" for name in skill_names)
    body = (
        f"{POINTER_BEGIN}\n"
        "## Installed agent skills\n\n"
        "Official DevOps/SRE/Cloud Agent Skills are installed in this workspace. "
        f"Before relevant work, read the matching `SKILL.md` under `{skills_dir}/`:\n\n"
        f"{listing}\n\n"
        "Prefer read-only/proposal workflows and require human approval for write "
        "actions (deploys, Terraform applies, identity or production changes).\n"
        f"{POINTER_END}\n"
    )
    kind = AGENTS[agent]["pointer_kind"]
    if kind == "cursor":
        return (
            "---\n"
            "description: Official DevOps agent skills installed in this workspace\n"
            "alwaysApply: true\n"
            "---\n\n" + body
        )
    return body


def write_pointer(path: Path, body: str) -> None:
    """Insert or replace the managed block in a (possibly pre-existing) file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if POINTER_BEGIN in existing and POINTER_END in existing:
        pre = existing.split(POINTER_BEGIN, 1)[0].rstrip("\n")
        post = existing.split(POINTER_END, 1)[1].lstrip("\n")
        parts = [p for p in (pre, body.strip("\n"), post) if p]
        new = "\n\n".join(parts) + "\n"
    elif existing.strip():
        new = existing.rstrip("\n") + "\n\n" + body
    else:
        new = body
    path.write_text(new, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install official agent skills into a coding agent (macOS/Windows/Linux).",
    )
    parser.add_argument("--agent", default="claude-code", choices=sorted(AGENTS) + ["all"])
    parser.add_argument("--source", help="'owner/repo', a catalog entry name, or 'all' for every official skill repo.")
    parser.add_argument("--repos", default="data/repos.yaml", help="Path to the catalog YAML.")
    parser.add_argument("--filter", default="", help="Only install skills whose name/path contains this substring.")
    parser.add_argument("--project", action="store_true", help="Claude Code: install into ./.claude/skills instead of the global dir.")
    parser.add_argument("--target", help="Override the skill-folder target directory.")
    parser.add_argument("--list-sources", action="store_true", help="List official skill repos from the catalog and exit.")
    parser.add_argument("--list", action="store_true", help="List the skills a source provides without installing.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be installed without writing.")
    parser.add_argument("--force", action="store_true", help="Overwrite skills that already exist.")
    return parser.parse_args(argv)


def resolve_sources(args: argparse.Namespace) -> list[str]:
    catalog = load_catalog_sources(Path(args.repos)) if Path(args.repos).exists() else {}
    if args.source == "all":
        if not catalog:
            raise SystemExit("no catalog found; cannot expand --source all")
        return sorted(set(catalog.values()))
    if args.source in catalog:
        return [catalog[args.source]]
    if args.source and args.source.count("/") == 1:
        return [args.source]
    raise SystemExit(f"unrecognized --source {args.source!r}; try --list-sources")


def _print_sources(repos: str) -> None:
    catalog = load_catalog_sources(Path(repos)) if Path(repos).exists() else {}
    for owner_repo in sorted(set(catalog.values())):
        print(f"  {owner_repo}")


def install_for_agent(
    agent: str, skills: list[tuple[str, Path]], args: argparse.Namespace
) -> None:
    skills_dir = agent_skills_dir(agent, args.project, args.target)
    actions = plan_installs(skills, skills_dir, args.filter, args.force)
    installs = [a for a in actions if a[3] == "install"]
    skips = [a for a in actions if a[3] == "skip-exists"]

    print(f"[{agent}] target {skills_dir}: {len(installs)} to install, {len(skips)} already present.")
    if args.dry_run:
        for name, _src, dst, _action in installs:
            print(f"  would install {name} -> {dst}")
        return

    written = apply_installs(actions)
    installed_names = [name for name, _s, _d, action in actions if action == "install"]
    if AGENTS[agent]["mode"] == "pointer":
        all_names = sorted({a[0] for a in actions})
        pointer = Path(str(AGENTS[agent]["pointer"]))
        if args.target:
            pointer = Path(args.target).parent / pointer.name
        write_pointer(pointer, render_pointer(agent, all_names, skills_dir))
        print(f"  wrote pointer {pointer} ({len(all_names)} skills)")
    print(f"  installed {len(written)} skill folder(s) into {skills_dir}")
    if not installed_names and not args.force:
        print("  (all already present; re-run with --force to overwrite)")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_sources:
        print("Official skill sources (use with --source):")
        _print_sources(args.repos)
        return 0

    if not args.source:
        print("Pass --source to choose what to install. Available official skill repos:")
        _print_sources(args.repos)
        print("\nExample: --agent claude-code --source google/skills --filter cloud")
        return 2

    agents = sorted(AGENTS) if args.agent == "all" else [args.agent]
    owner_repos = resolve_sources(args)

    with tempfile.TemporaryDirectory() as tmp:
        skills: list[tuple[str, Path]] = []
        for owner_repo in owner_repos:
            root = download_source(owner_repo, Path(tmp) / owner_repo.replace("/", "_"))
            skills.extend(discover_skills(root))

        if args.list:
            needle = args.filter.lower().strip()
            shown = [
                name
                for name, src in skills
                if not needle or needle in name.lower() or needle in str(src).lower()
            ]
            print(f"{len(shown)} skill(s) from {', '.join(owner_repos)}:")
            for name in shown:
                print(f"  {name}")
            return 0

        print(f"Source(s): {', '.join(owner_repos)}")
        for agent in agents:
            install_for_agent(agent, skills, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
