"""Command-line entry point for standalone Claude advisory generation."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .agent import (
    MAX_PROVIDER_ATTEMPTS,
    PROVIDER_ATTEMPT_TIMEOUT_SECONDS,
    generate,
)
from .report import write_outputs
from .triage import DEFAULT_MAX_FINDINGS, confined_path, load_triage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-report", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--max-findings", type=int, default=DEFAULT_MAX_FINDINGS)
    parser.add_argument(
        "--max-provider-attempts", type=int, default=MAX_PROVIDER_ATTEMPTS
    )
    parser.add_argument(
        "--provider-timeout-seconds",
        type=float,
        default=PROVIDER_ATTEMPT_TIMEOUT_SECONDS,
    )
    args = parser.parse_args()
    if not 1 <= args.max_findings <= 200:
        parser.error("--max-findings must be between 1 and 200")
    if not 1 <= args.max_provider_attempts <= MAX_PROVIDER_ATTEMPTS:
        parser.error(
            "--max-provider-attempts must be between 1 and "
            f"{MAX_PROVIDER_ATTEMPTS}"
        )
    if args.provider_timeout_seconds <= 0:
        parser.error("--provider-timeout-seconds must be greater than zero")
    try:
        root = Path.cwd()
        input_path = confined_path(args.triage_report, root, must_exist=True)
        json_path = confined_path(args.json_output, root, must_exist=False)
        markdown_path = confined_path(args.markdown_output, root, must_exist=False)
        result = asyncio.run(
            generate(
                load_triage(input_path),
                args.max_findings,
                max_attempts=args.max_provider_attempts,
                attempt_timeout_seconds=args.provider_timeout_seconds,
            )
        )
        write_outputs(json_path, markdown_path, result)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Claude agent status: {result['agent_status']}")
    print(f"Deterministic policy unchanged: {result['policy_unchanged']}")
    print(f"Agent report: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
