#!/bin/sh
# One-command installer: official agent skills -> antigravity.
#
#   curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/antigravity/install.sh | sh -s -- --source google/skills --filter cloud
#
# Installs immediately. Add --dry-run to preview, --source all for every source.
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
exec python3 "$tmp/install_skills.py" --agent antigravity --repos "$tmp/repos.yaml" "$@"
