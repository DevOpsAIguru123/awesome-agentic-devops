# Authentication and CI configuration

Use GitHub Actions secrets for sensitive values and Google Cloud Workload
Identity Federation (WIF) for short-lived Vertex AI credentials. Do not commit a
service-account JSON key or Gemini API key.

## Repository settings

Create these under **Settings → Secrets and variables → Actions**:

| Name | Classification | Purpose |
| --- | --- | --- |
| `SONAR_TOKEN` | Secret | SonarCloud project analysis token |
| `SONAR_HOST_URL` | Secret in this reference | SonarCloud/SonarQube endpoint |
| `SONAR_ORGANIZATION` | Secret in this reference | SonarCloud organization key |
| `WIF_PROVIDER` | Secret in this reference | Full WIF provider resource name |
| `WIF_SERVICE_ACCOUNT` | Secret in this reference | Service account email used for impersonation |
| `GOOGLE_CLOUD_PROJECT` | Secret in this reference | Vertex AI project ID |
| `DOCKERHUB_USERNAME` | Secret in this reference | Docker Hub namespace |
| `DOCKERHUB_REPOSITORY` | Secret in this reference | Existing repository name |
| `DOCKERHUB_TOKEN` | Secret | Least-privilege Docker Hub access token |
| `ANTHROPIC_API_KEY` | Secret | Dedicated key for the Claude Sonnet 5 advisory stage |

The WIF provider, service-account email, project ID, and Docker namespace are
identifiers rather than credentials. This reference stores them as secrets to
avoid exposing account-specific metadata in public logs and configuration.

Copy `.github/container-release.settings.example` to the ignored
`.github/container-release.settings`, replace the placeholders, authenticate
the GitHub CLI, then run:

```bash
gh auth login --hostname github.com
.github/scripts/configure-container-release-settings.sh
```

The helper refuses unchanged placeholders and does not print values.

The Claude container image release workflow runs for matching pull
requests, trusted main-branch changes, and manual dispatches. Store a dedicated
key as the `ANTHROPIC_API_KEY` repository secret. Release approval and
publishing use the same deterministic policy and protected environment as the
Google ADK workflow; Claude output cannot satisfy either authorization gate.

## WIF requirements

Configure the provider with GitHub's OIDC issuer and mappings for at least
`google.subject`, `attribute.repository`, `attribute.repository_owner`, and
`attribute.ref`. Restrict the provider to your exact repository and trusted
branch; do not trust all identities from the shared GitHub issuer.

Example condition—replace placeholders in Google Cloud, never in committed
files:

```text
assertion.repository == '<OWNER>/<REPOSITORY>' &&
assertion.ref == 'refs/heads/main'
```

Grant the corresponding repository principal only
`roles/iam.workloadIdentityUser` on a dedicated, least-privilege service
account. Grant that service account only the Vertex AI permissions required by
the advisory call.

Set `WIF_PROVIDER` to the full provider name:

```text
projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<POOL_ID>/providers/<PROVIDER_ID>
```

Use the numeric project number in the provider resource name. An
`unauthorized_client` error with an attribute-condition message normally means
the workflow repository, ref, or event does not satisfy the provider's CEL
condition.

Authoritative references:

- [Google Cloud deployment-pipeline WIF guide](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines)
- [`google-github-actions/auth` documentation](https://github.com/google-github-actions/auth)
- [WIF security best practices](https://docs.cloud.google.com/iam/docs/best-practices-for-using-workload-identity-federation)

## Protected approval

Create the GitHub Environment `container-production`, add required reviewers,
prevent self-review where appropriate, and restrict deployment branches to
`main`. The ADK agent must remain outside this authorization decision.
