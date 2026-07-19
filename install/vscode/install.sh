#!/bin/sh
# One-command installer: agent skills -> vscode.
#
#   curl -fsSL https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/vscode/install.sh | sh -s -- --source google/skills --filter cloud
#
# Installs immediately. Add --dry-run to preview. Use --official, --community,
# or --all to install a whole set.
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
# catalog.json lets install_skills.py read the catalog without PyYAML,
# which a stock python3 (e.g. macOS /usr/bin/python3) does not have.
curl -fsSL "$RAW/data/catalog.json" -o "$tmp/catalog.json"
exec python3 "$tmp/install_skills.py" --agent vscode --repos "$tmp/repos.yaml" "$@"
