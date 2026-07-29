"""Render machine-readable and human-readable advisory artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def safe(value: Any) -> str:
    text = " ".join(str(value or "unknown").split())
    for source, replacement in (
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("|", "&#124;"),
        ("`", "&#96;"),
    ):
        text = text.replace(source, replacement)
    return text


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Claude Agent SDK container security review",
        "",
        "**Overall release decision:** `not_evaluated`  ",
        f"**Agent status:** `{safe(result['agent_status'])}`  ",
        "**Scoped deterministic policy decision:** "
        f"`{safe(result['policy_decision'])}`",
        "",
        "> This review is advisory. It cannot approve, reject, waive, publish, or ",
        "> override deterministic policy. `policy_decision: not_evaluated` "
        "is not approval.",
        "",
        "## Input coverage",
        "",
        f"- Full findings: **{result['input']['total_findings']}**",
        f"- Bounded findings supplied: **{result['input']['returned_findings']}**",
        f"- Input truncated: **{str(result['input']['truncated']).lower()}**",
        "",
    ]
    review = result.get("review")
    if not isinstance(review, dict):
        lines.extend(
            [
                "## Agent availability",
                "",
                "Claude was unavailable; deterministic evidence and policy "
                "remain authoritative.",
                f"Failure category: `{safe(result.get('failure_category'))}`",
                "",
            ]
        )
        return "\n".join(lines)
    lines.extend(
        [
            "## Executive summary",
            "",
            safe(review["executive_summary"]),
            "",
            "## Risk assessment",
            "",
            safe(review["risk_assessment"]),
            "",
            "## Prioritized actions",
            "",
        ]
    )
    for index, action in enumerate(review.get("prioritized_actions") or [], 1):
        lines.extend(
            [
                f"### {index}. {safe(action['action'])}",
                "",
                "- Finding IDs: "
                f"{', '.join(safe(item) for item in action['finding_ids'])}",
                f"- Rationale: {safe(action['rationale'])}",
                f"- Compatibility impact: {safe(action['compatibility_impact'])}",
                "",
            ]
        )
    for title, key in (
        ("Attack-path hypotheses", "attack_paths"),
        ("Verification steps", "verification_steps"),
        ("Limitations", "limitations"),
    ):
        lines.extend([f"## {title}", ""])
        values = review.get(key) or ["None reported."]
        lines.extend(f"- {safe(item)}" for item in values)
        lines.append("")
    return "\n".join(lines)


def write_outputs(json_path: Path, markdown_path: Path, result: dict[str, Any]) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(result) + "\n", encoding="utf-8")
