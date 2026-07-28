# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from app.agent import root_agent


@pytest.mark.asyncio
async def test_agent_exposes_only_read_only_trivy_tools() -> None:
    """The agent tool surface must not expose mutation or deployment actions."""
    tool_names = {tool.name for tool in await root_agent.canonical_tools()}

    assert root_agent.name == "container_hardening_copilot"
    assert tool_names == {"scan_with_trivy", "analyze_trivy_report"}
