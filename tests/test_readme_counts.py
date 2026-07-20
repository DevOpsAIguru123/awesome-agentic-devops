"""The README intro's catalog counts must match data/repos.yaml.

Companion tripwire to the entry-count assertion in test_repos_yaml.py: adding
a catalog entry without refreshing the intro pitch numbers fails here with the
exact fix (run scripts/sync_readme_counts.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.sync_readme_counts import COUNTS_PATTERN, README, expected_counts_phrase  # noqa: E402


def test_readme_intro_counts_match_catalog():
    phrase = expected_counts_phrase()
    found = COUNTS_PATTERN.findall(README.read_text())
    assert found, (
        "README.md lost its "
        "'<N> entries organized into <M> catalog sections' phrase"
    )
    assert found == [phrase], (
        f"README counts {found} are stale, expected '{phrase}'. "
        "Run: python scripts/sync_readme_counts.py"
    )


def test_counts_phrase_describes_readme_sections_not_yaml_categories():
    phrase = expected_counts_phrase()
    assert phrase.endswith("entries organized into 14 catalog sections")
    assert COUNTS_PATTERN.fullmatch(phrase)
