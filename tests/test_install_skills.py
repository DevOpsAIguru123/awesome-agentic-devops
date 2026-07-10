"""Offline tests for scripts/install_skills.py.

These exercise the install mechanics (discover -> plan -> apply) against a local
fake skill source, so they run deterministically without network access.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.install_skills import (  # noqa: E402
    apply_installs,
    discover_skills,
    load_catalog_sources,
    plan_installs,
    resolve_target,
)


def make_source(root: Path) -> Path:
    """Create a fake source repo with three skill folders and some noise."""
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

    names = [name for name, _ in skills]
    assert names == ["alpha-skill", "beta-skill", "cloud-deploy"]  # sorted
    for _name, folder in skills:
        assert (folder / "SKILL.md").exists()


def test_plan_and_apply_copies_full_skill_folder(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    skills = discover_skills(source)

    actions = plan_installs(skills, target, name_filter="", force=False)
    assert all(action == "install" for *_rest, action in actions)

    written = apply_installs(actions)

    assert len(written) == 3
    # the whole folder is copied, not just SKILL.md
    assert (target / "alpha-skill" / "SKILL.md").exists()
    assert (target / "alpha-skill" / "reference.md").exists()


def test_filter_limits_installs(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    skills = discover_skills(source)

    actions = plan_installs(skills, target, name_filter="cloud", force=False)

    installed = [name for name, _s, _d, action in actions if action == "install"]
    assert installed == ["cloud-deploy"]


def test_existing_skill_is_skipped_without_force(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    (target / "alpha-skill").mkdir(parents=True)
    (target / "alpha-skill" / "SKILL.md").write_text("old\n", encoding="utf-8")
    skills = discover_skills(source)

    without_force = plan_installs(skills, target, name_filter="alpha", force=False)
    assert without_force[0][3] == "skip-exists"

    with_force = plan_installs(skills, target, name_filter="alpha", force=True)
    assert with_force[0][3] == "install"


def test_apply_skips_are_not_written(tmp_path):
    source = make_source(tmp_path / "src")
    target = tmp_path / "target"
    (target / "alpha-skill").mkdir(parents=True)
    (target / "alpha-skill" / "SKILL.md").write_text("keep me\n", encoding="utf-8")
    skills = discover_skills(source)

    actions = plan_installs(skills, target, name_filter="", force=False)
    apply_installs(actions)

    # the pre-existing skill was not overwritten
    assert (target / "alpha-skill" / "SKILL.md").read_text(encoding="utf-8") == "keep me\n"
    # the others were installed
    assert (target / "beta-skill" / "SKILL.md").exists()


def test_resolve_target_project_vs_global():
    global_target = resolve_target("claude-code", project=False, override=None)
    project_target = resolve_target("claude-code", project=True, override=None)
    override = resolve_target("claude-code", project=False, override="/tmp/custom")

    assert global_target.parts[-2:] == (".claude", "skills")
    assert project_target == Path(".claude") / "skills"
    assert override == Path("/tmp/custom")


def test_catalog_sources_returns_official_skill_repos():
    sources = load_catalog_sources(Path("data/repos.yaml"))

    # values are owner/repo strings for official skill repositories
    assert "google/skills" in sources.values()
    for owner_repo in sources.values():
        assert owner_repo.count("/") == 1
