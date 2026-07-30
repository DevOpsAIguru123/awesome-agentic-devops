# Five-minute setup

This quick start exercises the deterministic pipeline locally. SonarCloud,
Vertex AI, Anthropic, protected approvals, and Docker Hub are optional until you
run a complete GitHub Actions workflow.

## 1. Install prerequisites

Install Docker, Python 3.11+, Git, and [Trivy](https://trivy.dev/). Install `uv`
if you also want to run either agent implementation and its tests.

```bash
git clone https://github.com/<OWNER>/<REPOSITORY>.git
cd <REPOSITORY>/agents/container-image-release-advisor/adk
uv sync --frozen
```

## 2. Run deterministic tests

```bash
uv run pytest tests/unit
```

These tests do not require a model API key or Google Cloud credentials.

## 3. Build and scan the hardened sample

```bash
cd examples/agentic-devops-portfolio
docker build --tag agentic-devops-portfolio:local .
mkdir -p reports/local
trivy config --format json --output reports/local/config.json .
trivy image --scanners vuln,secret --format json \
  --output reports/local/image.json agentic-devops-portfolio:local
```

Generated local evidence belongs under `reports/local/`, which is ignored by
Git. Do not commit fresh scanner output without sanitizing and intentionally
curating it as a test fixture.

## 4. Verify fail-closed policy without deployable vulnerable fixtures

```bash
cd ../..
uv run pytest tests/unit/test_release_policy.py tests/unit/test_config_policy.py
```

The tests supply synthetic scanner JSON in memory and verify that blocking
findings cannot authorize a release. The distributable branch therefore tests
fail-closed behavior without shipping an image or manifest that should never be
deployed. See [Demonstration runs](DEMO-RUNS.md) for separately isolated blocked
run evidence.

## 5. Enable the complete hosted workflow

1. Create the SonarCloud project and repository secrets documented in
   [Authentication and CI configuration](AUTHENTICATION.md).
2. Create a `container-production` GitHub Environment and require reviewers.
3. Choose **ADK container image release** for Google ADK/Vertex AI or **Claude
   container image release** for Claude Agent SDK/Sonnet 5.
4. Run the selected workflow with `publish: false`.
5. Inspect the overall job summary and the three report artifacts.

Keep `publish: false` until your own policy, IAM, registry, branch protection,
and environment-review controls have been validated.
