# Terraform Plan Reviewer ADK Agent

Reviews Terraform plan text and returns a structured risk review.

This version uses a Google Cloud account-bound API key with Vertex AI:

```python
client = genai.Client(api_key=key, vertexai=True)
```

The API key must allow `aiplatform.googleapis.com` and be bound to a service
account with Vertex AI permissions.

## Run Locally

```bash
python -m pip install -r requirements.txt
cp .env.example .env
python run_review.py < terraform-plan.txt
```

## Terraform Cloud Plan Review

An example GitHub Actions workflow can run a real Terraform Cloud speculative
plan from:

```text
agents/adk/terraform-plan-reviewer/terraform/gcs-sample
```

Terraform Cloud target:

```text
organization: devops_vv
workspace: agents
```

The workflow sends the streamed Terraform Cloud plan output to `run_review.py`
and fails unless the agent returns `safe-to-apply`.

Expected output:

```json
{
  "findings": [],
  "evidence": [],
  "recommendation": "safe-to-apply",
  "risk_summary": "..."
}
```
