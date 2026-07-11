"""Guard the README intro's counts phrase without blocking contributors.

Staleness of the numbers is repaired automatically by the sync-readme-counts
CI job (it runs scripts/sync_readme_counts.py and commits the fix), so these
tests only assert the phrase the script rewrites still exists and that the
expected value is computable — deleting either would silently disable the sync.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.sync_readme_counts import COUNTS_PATTERN, README, expected_counts_phrase  # noqa: E402


def test_readme_keeps_the_counts_phrase():
    found = COUNTS_PATTERN.findall(README.read_text())
    assert len(found) == 1, (
        f"README.md must contain exactly one '<N> entries across <M> categories' "
        f"phrase for sync_readme_counts.py to rewrite; found {found}"
    )


def test_expected_counts_are_computable():
    assert COUNTS_PATTERN.fullmatch(expected_counts_phrase())
