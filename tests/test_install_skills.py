"""Offline tests for scripts/install_skills.py.

These exercise install mechanics (discover -> plan -> apply), per-agent target
resolution, and source resolution against a local fake skill source, so they run
deterministically without network access.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.install_skills as install_skills  # noqa: E402
from scripts.install_skills import (  # noqa: E402
    AGENT_SKILLS,
    COMMUNITY_CATEGORY,
    agent_skills_dir,
    apply_installs,
    discover_skills,
    load_catalog_sources,
    plan_installs,
    resolve_sources,
)


def write_catalog(folder: Path, entries: list[dict]) -> Path:
    """Write a catalog.json/repos.yaml pair, returning the repos.yaml path."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "catalog.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
    (folder / "repos.yaml").write_text("- name: unused\n", encoding="utf-8")
    return folder / "repos.yaml"


def make_source(root: Path) -> Path:
    for name in ("alpha-skill", "beta-skill", "cloud-deploy"):
        folder = root / "skills" / name
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
        (folder / "reference.md").write_text("detail\n", encoding="utf-8")
    # scaffolding that must be ignored
    (root / "template").mkdir()
    (root / "template" / "SKILL.md").write_text("# template\n", encoding="utf-8")
    (root / "README.md").write_text("not a skill\n", encoding="utf-8")
    return root


def test_discover_finds_skill_dirs_and_ignores_template(tmp_path):
    source = make_source(tmp_path / "src")
    skills = discover_skills(source)
    names = [name for name, _ in skills]
    assert names == ["alpha-skill", "beta-skill", "cloud-deploy"]  # no 'template'
    for _name, folder in skills:
        assert (folder / "SKILL.md").exists()


def test_plan_and_apply_copies_full_skill_folder(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    actions = plan_installs(discover_skills(source), target, name_filter="", force=False)
    assert all(a[3] == "install" for a in actions)
    written = apply_installs(actions)
    assert len(written) == 3
    assert (target / "alpha-skill" / "SKILL.md").exists()
    assert (target / "alpha-skill" / "reference.md").exists()


def test_filter_limits_installs(tmp_path):
    source = make_source(tmp_path / "src")
    actions = plan_installs(discover_skills(source), tmp_path / "t", name_filter="cloud", force=False)
    installed = [name for name, _s, _d, action in actions if action == "install"]
    assert installed == ["cloud-deploy"]


def test_existing_skill_is_skipped_without_force(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    (target / "alpha-skill").mkdir(parents=True)
    (target / "alpha-skill" / "SKILL.md").write_text("old\n", encoding="utf-8")
    skills = discover_skills(source)
    assert plan_installs(skills, target, "alpha", force=False)[0][3] == "skip-exists"
    assert plan_installs(skills, target, "alpha", force=True)[0][3] == "install"


def test_apply_does_not_overwrite_existing_without_force(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    (target / "alpha-skill").mkdir(parents=True)
    (target / "alpha-skill" / "SKILL.md").write_text("keep me\n", encoding="utf-8")
    actions = plan_installs(discover_skills(source), target, "", force=False)
    apply_installs(actions)
    assert (target / "alpha-skill" / "SKILL.md").read_text(encoding="utf-8") == "keep me\n"
    assert (target / "beta-skill" / "SKILL.md").exists()


def test_every_agent_installs_to_its_own_global_folder():
    expected_tails = {
        "claude-code": (".claude", "skills"),
        "codex": (".codex", "skills"),
        "cursor": (".cursor", "skills"),
        "vscode": (".copilot", "skills"),
        "antigravity": (".gemini", "antigravity", "skills"),
    }
    for agent, tail in expected_tails.items():
        global_dir = agent_skills_dir(agent, project=False, override=None)
        assert global_dir == Path.home().joinpath(*tail), agent
        assert global_dir.parts[: len(Path.home().parts)] == Path.home().parts


def test_project_and_target_override_the_global_folder():
    project = agent_skills_dir("codex", project=True, override=None)
    override = agent_skills_dir("codex", project=False, override="/tmp/custom")
    assert project == Path(".codex") / "skills"
    assert override == Path("/tmp/custom")


def test_agent_skills_covers_all_supported_agents():
    assert set(AGENT_SKILLS) == {"claude-code", "codex", "cursor", "vscode", "antigravity"}


def test_catalog_sources_returns_official_skill_repos():
    sources = load_catalog_sources(Path("data/repos.yaml"))
    assert "google/skills" in sources.values()
    for owner_repo in sources.values():
        assert owner_repo.count("/") == 1


def test_explicit_owner_repo_source_never_loads_catalog(monkeypatch):
    """The stdlib-only path: an explicit owner/repo must not touch the YAML
    catalog (which needs PyYAML), even when --repos points at a real file."""

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("catalog loaded for an explicit owner/repo source")

    monkeypatch.setattr(install_skills, "load_catalog_sources", fail_if_called)
    args = argparse.Namespace(source="google/skills", repos="data/repos.yaml")

    assert resolve_sources(args) == ["google/skills"]


def test_source_all_still_expands_via_catalog():
    args = argparse.Namespace(source="all", repos="data/repos.yaml")
    sources = resolve_sources(args)
    assert "google/skills" in sources and len(sources) > 1


def test_catalog_path_works_without_pyyaml(tmp_path, monkeypatch):
    """Regression test for the real bug: `--source all` on a stock interpreter.

    macOS's /usr/bin/python3 has no PyYAML, so the documented curl installer
    died on its own headline command. With catalog.json present the catalog must
    resolve without importing yaml at all -- so make that import fail outright.
    """
    repos = write_catalog(
        tmp_path / "data",
        [{"name": "google/skills", "url": "https://github.com/google/skills",
          "category": "official-agent-skills"}],
    )
    monkeypatch.setitem(sys.modules, "yaml", None)  # any `import yaml` now raises

    assert load_catalog_sources(repos) == {"google/skills": "google/skills"}


def test_catalog_json_is_preferred_over_repos_yaml(tmp_path):
    repos = write_catalog(
        tmp_path / "data",
        [{"name": "from/json", "url": "https://github.com/from/json",
          "category": "official-agent-skills"}],
    )
    assert load_catalog_sources(repos) == {"from/json": "from/json"}


def test_community_category_is_selectable(tmp_path):
    """The bug that made community skills uninstallable: a hardcoded category."""
    repos = write_catalog(
        tmp_path / "data",
        [
            {"name": "official/one", "url": "https://github.com/official/one",
             "category": "official-agent-skills"},
            {"name": "community/one", "url": "https://github.com/community/one",
             "category": COMMUNITY_CATEGORY},
        ],
    )
    assert load_catalog_sources(repos) == {"official/one": "official/one"}
    assert load_catalog_sources(repos, (COMMUNITY_CATEGORY,)) == {"community/one": "community/one"}


def test_source_keywords_select_official_community_or_both():
    def sources_for(keyword):
        return resolve_sources(argparse.Namespace(source=keyword, repos="data/repos.yaml"))

    official, community = sources_for("official"), sources_for("community")
    assert official and community
    assert not set(official) & set(community), "official and community must not overlap"
    assert sorted(sources_for("everything")) == sorted(official + community)
    # 'all' is a published alias for 'official' and must not widen silently.
    assert sources_for("all") == official


def flag_args(**flags):
    """A Namespace as parse_args would produce it for the selection flags."""
    base = {"source": None, "repos": "data/repos.yaml",
            "official": False, "community": False, "all_skills": False}
    return argparse.Namespace(**{**base, **flags})


def test_selection_flags_pick_official_community_or_both():
    official = resolve_sources(flag_args(official=True))
    community = resolve_sources(flag_args(community=True))
    everything = resolve_sources(flag_args(all_skills=True))

    assert official and community
    assert not set(official) & set(community)
    assert sorted(everything) == sorted(official + community)


def test_official_and_community_flags_compose_like_all():
    both = resolve_sources(flag_args(official=True, community=True))
    assert sorted(both) == sorted(resolve_sources(flag_args(all_skills=True)))


def test_all_flag_is_broader_than_the_legacy_source_all():
    """--all includes community; --source all is a published official-only alias."""
    flag = resolve_sources(flag_args(all_skills=True))
    legacy = resolve_sources(argparse.Namespace(source="all", repos="data/repos.yaml"))
    assert set(legacy) < set(flag)


def test_selection_flags_conflict_with_source():
    try:
        resolve_sources(flag_args(official=True, source="google/skills"))
    except SystemExit as exc:
        assert "cannot be combined" in str(exc)
    else:
        raise AssertionError("combining --source with a selection flag must fail")


def test_explicit_owner_repo_still_wins_over_a_keyword_name(monkeypatch):
    """A repo literally named e.g. 'community/skills' must resolve as itself."""

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("catalog loaded for an explicit owner/repo source")

    monkeypatch.setattr(install_skills, "load_catalog_sources", fail_if_called)
    args = argparse.Namespace(source="someone/community", repos="data/repos.yaml")

    assert resolve_sources(args) == ["someone/community"]
