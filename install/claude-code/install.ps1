# One-command installer: official agent skills -> Claude Code (~/.claude/skills).
#
# Preview (dry run, writes nothing):
#   irm https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/claude-code/install.ps1 | iex
#
# To pass options (source, --yes), download then run:
#   iwr .../install/claude-code/install.ps1 -OutFile install.ps1
#   ./install.ps1 --source google/skills --filter cloud --yes
#
# Nothing is written until you add --yes.
$ErrorActionPreference = "Stop"

$raw = "https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main"

$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "Python 3 is required. Install it, then re-run."; exit 1 }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
    Invoke-WebRequest "$raw/scripts/install_skills.py" -OutFile (Join-Path $tmp "install_skills.py")
    Invoke-WebRequest "$raw/data/repos.yaml" -OutFile (Join-Path $tmp "repos.yaml")
    & $py.Path (Join-Path $tmp "install_skills.py") --agent claude-code --repos (Join-Path $tmp "repos.yaml") @args
}
finally {
    Remove-Item -Recurse -Force $tmp
}
