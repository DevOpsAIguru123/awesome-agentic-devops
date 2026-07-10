#!/bin/sh
# One-command installer: official agent skills -> Claude Code (~/.claude/skills).
#
# Preview (dry run, writes nothing):
#   curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.sh | sh
#
# Install a specific source:
#   curl -fsSL .../install/claude-code/install.sh | sh -s -- --source google/skills --filter cloud --yes
#
# Nothing is written until you add --yes. See --help for all options.
set -eu

RAW="https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Install it, then re-run." >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

curl -fsSL "$RAW/scripts/install_skills.py" -o "$tmp/install_skills.py"
curl -fsSL "$RAW/data/repos.yaml" -o "$tmp/repos.yaml"

exec python3 "$tmp/install_skills.py" --agent claude-code --repos "$tmp/repos.yaml" "$@"
