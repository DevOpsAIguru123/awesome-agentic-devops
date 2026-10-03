from pathlib import Path

README = Path("README.md")
CONTRIBUTING = Path("CONTRIBUTING.md")
SAFETY_MODEL = Path("docs/safety-model.md")
OPERATOR_CHECKLIST = Path("docs/operator-safety-checklist.md")
SCORECARD = Path("templates/agent-scorecard.md")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_operator_safety_checklist_covers_core_controls():
    text = _text(OPERATOR_CHECKLIST)

    required_phrases = [
        "Start read-only",
        "Keep secrets out of model context",
        "Require dry-run or proposal mode before writes",
        "Define the human approval gate",
        "Limit blast radius",
        "Capture evidence and audit logs",
        "Production-adjacent go/no-go",
        "read-only token",
        "namespace-scoped role",
        "plan-only workspace token",
        "approval record and approver",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_operator_safety_checklist_is_linked_from_entry_points():
    expected_links = [
        "docs/operator-safety-checklist.md",
        "operator-safety-checklist.md",
    ]

    assert expected_links[0] in _text(README)
    assert expected_links[0] in _text(CONTRIBUTING)
    assert expected_links[1] in _text(SAFETY_MODEL)


def test_agent_scorecard_preserves_safety_preflight_fields():
    text = _text(SCORECARD)

    for phrase in [
        "Credential and context boundary",
        "Least-privilege scope to grant",
        "Secrets excluded from model context",
        "Dry-run or preview command",
        "Approval recorded in",
        "Audit artifacts",
        "Production-readiness decision",
    ]:
        assert phrase in text
