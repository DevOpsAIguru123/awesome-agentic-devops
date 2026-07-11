"""Offline tests for scripts/install_skills.py.

These exercise install mechanics (discover -> plan -> apply), per-agent target
resolution, and pointer-file rendering against a local fake skill source, so
they run deterministically without network access.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.install_skills as install_skills  # noqa: E402
from scripts.install_skills import (  # noqa: E402
    AGENTS,
    POINTER_BEGIN,
    POINTER_END,
    SHARED_SKILLS_DIR,
    agent_skills_dir,
    apply_installs,
    discover_skills,
    load_catalog_sources,
    plan_installs,
    render_pointer,
    resolve_sources,
    write_pointer,
)


def make_source(root: Path) -> Path:
    for name in ("alpha-skill", "beta-skill", "cloud-deploy"):
        folder = root / "skills" / name
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
        (folder / "reference.md").write_text("detail\n", encoding="utf-8")
    (root / "README.md").write_text("not a skill\n", encoding="utf-8")
    return root


def test_discover_finds_only_skill_dirs(tmp_path):
    source = make_source(tmp_path / "src")
    skills = discover_skills(source)
    assert [name for name, _ in skills] == ["alpha-skill", "beta-skill", "cloud-deploy"]
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


def test_native_agent_skills_dir_global_vs_project():
    global_dir = agent_skills_dir("claude-code", project=False, override=None)
    project_dir = agent_skills_dir("claude-code", project=True, override=None)
    assert global_dir.parts[-2:] == (".claude", "skills")
    assert project_dir == Path(".claude") / "skills"


def test_pointer_agents_use_shared_dir():
    for agent, spec in AGENTS.items():
        if spec["mode"] != "pointer":
            continue
        assert agent_skills_dir(agent, project=False, override=None) == SHARED_SKILLS_DIR


def test_render_pointer_lists_skills_and_is_agent_shaped():
    names = ["cloud-run-basics", "bigquery-basics"]
    cursor = render_pointer("cursor", names, SHARED_SKILLS_DIR)
    assert cursor.startswith("---")  # cursor rules front matter
    assert "alwaysApply: true" in cursor
    agents_md = render_pointer("codex", names, SHARED_SKILLS_DIR)
    assert not agents_md.startswith("---")
    for body in (cursor, agents_md):
        assert POINTER_BEGIN in body and POINTER_END in body
        for name in names:
            assert f"{SHARED_SKILLS_DIR}/{name}/SKILL.md" in body


def test_write_pointer_inserts_then_replaces_managed_block(tmp_path):
    path = tmp_path / "AGENTS.md"
    path.write_text("# Existing project agents doc\n\nKeep this.\n", encoding="utf-8")

    write_pointer(path, render_pointer("codex", ["alpha-skill"], SHARED_SKILLS_DIR))
    first = path.read_text(encoding="utf-8")
    assert "Keep this." in first  # pre-existing content preserved
    assert first.count(POINTER_BEGIN) == 1
    assert "alpha-skill" in first

    write_pointer(path, render_pointer("codex", ["beta-skill"], SHARED_SKILLS_DIR))
    second = path.read_text(encoding="utf-8")
    assert second.count(POINTER_BEGIN) == 1  # block replaced, not duplicated
    assert "beta-skill" in second and "alpha-skill" not in second
    assert "Keep this." in second


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
