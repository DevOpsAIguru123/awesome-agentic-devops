import json
import subprocess
import sys
from pathlib import Path

import yaml


def copy_seed_repo(tmp_path):
    root = tmp_path / "workspace"
    (root / "data").mkdir(parents=True)
    source = Path("data/repos.yaml")
    (root / "data/repos.yaml").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts/devops_catalog_mcp_server.py").write_text(Path("scripts/devops_catalog_mcp_server.py").read_text(encoding="utf-8"), encoding="utf-8")
    return root


def run_setup(root, *args):
    return subprocess.run(
        [sys.executable, "scripts/setup_devops_ai_clients.py", "--workspace", str(root), *args],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=True,
    )


def test_setup_dry_run_does_not_write(tmp_path):
    root = copy_seed_repo(tmp_path)

    result = run_setup(root, "--clients", "claude-code", "cursor")

    assert "dry run only" in result.stdout
    assert "would write" in result.stdout
    assert not (root / "CLAUDE.md").exists()
    assert not (root / ".cursor/mcp.json").exists()


def test_setup_writes_all_client_configs_and_catalog(tmp_path):
    root = copy_seed_repo(tmp_path)

    result = run_setup(root, "--clients", "all", "--write")

    assert "write" in result.stdout
    expected_files = [
        "devops-ai/official-devops-mcp-catalog.json",
        "devops-ai/DEVOPS_SKILL.md",
        "devops-ai/README.md",
        "CLAUDE.md",
        "AGENTS.md",
        ".cursor/rules/awesome-agentic-devops.mdc",
        ".mcp.json",
        ".codex/mcp.json",
        ".cursor/mcp.json",
        ".antigravity/mcp.json",
        ".vscode/mcp.json",
    ]
    for file_name in expected_files:
        assert (root / file_name).exists(), file_name

    catalog = json.loads((root / "devops-ai/official-devops-mcp-catalog.json").read_text(encoding="utf-8"))
    seed_entries = yaml.safe_load(Path("data/repos.yaml").read_text(encoding="utf-8"))
    expected_count = sum(
        1
        for entry in seed_entries
        if str(entry.get("category", "")).startswith("official-")
        and "mcp" in " ".join(str(entry.get(field, "")) for field in ("category", "type", "framework")).lower()
    )
    assert len(catalog["entries"]) == expected_count
    assert expected_count > 10

    for config_path in [".mcp.json", ".codex/mcp.json", ".cursor/mcp.json", ".antigravity/mcp.json", ".vscode/mcp.json"]:
        config = json.loads((root / config_path).read_text(encoding="utf-8"))
        server = config["mcpServers"]["awesome-agentic-devops-catalog"]
        assert server["command"] == "python3"
        assert "devops_catalog_mcp_server.py" in server["args"][0]
        assert server["env"] == {}


def test_catalog_mcp_server_search_tool(tmp_path):
    root = copy_seed_repo(tmp_path)
    run_setup(root, "--clients", "claude-code", "--write")

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "search_devops_mcp_catalog", "arguments": {"query": "terraform", "limit": 5}},
    }
    result = subprocess.run(
        [sys.executable, str(root / "scripts/devops_catalog_mcp_server.py"), "--catalog", str(root / "devops-ai/official-devops-mcp-catalog.json")],
        input=json.dumps(request) + "\n",
        text=True,
        capture_output=True,
        check=True,
    )

    response = json.loads(result.stdout.strip())
    payload = json.loads(response["result"]["content"][0]["text"])
    assert any("terraform" in json.dumps(entry).lower() for entry in payload)
