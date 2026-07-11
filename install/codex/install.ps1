# One-command installer: official agent skills -> codex.
#
#   iwr https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/codex/install.ps1 -OutFile install.ps1
#   ./install.ps1 --source google/skills --filter cloud
#
# Installs immediately. Add --dry-run to preview, --source all for every source.
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
    & $py.Path (Join-Path $tmp "install_skills.py") --agent codex --repos (Join-Path $tmp "repos.yaml") @args
}
finally { Remove-Item -Recurse -Force $tmp }
