# One-command installer: agent skills -> cursor.
#
#   iwr https://raw.githubusercontent.com/DevOpsAIguru123/awesome-agentic-devops/main/install/cursor/install.ps1 -OutFile install.ps1
#   ./install.ps1 --source google/skills --filter cloud
#
# Installs immediately. Add --dry-run to preview. Use --source official,
# --source community, or --source everything to install a whole set.
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
    # catalog.json lets install_skills.py read the catalog without PyYAML.
    Invoke-WebRequest "$raw/data/catalog.json" -OutFile (Join-Path $tmp "catalog.json")
    & $py.Path (Join-Path $tmp "install_skills.py") --agent cursor --repos (Join-Path $tmp "repos.yaml") @args
}
finally { Remove-Item -Recurse -Force $tmp }
