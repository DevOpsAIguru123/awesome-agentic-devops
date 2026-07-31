# Agentic DevOps Portfolio

A static, responsive sample portfolio served by an unprivileged NGINX process.

## Build and run

```bash
docker build -t agentic-devops-portfolio:local .
docker run --rm -p 8080:8080 agentic-devops-portfolio:local
curl --fail http://127.0.0.1:8080/healthz
```

## Scan

```bash
mkdir -p reports
trivy image --format json --output reports/trivy-image.json agentic-devops-portfolio:local
trivy config --format json --output reports/trivy-config.json .
```

The image runs as the `nginx` user, listens on port 8080, writes temporary files
under `/tmp`, and sends logs to stdout/stderr.

## Hardened deployment template

`deployment.yaml` is a safe-by-default Kubernetes template. It requires a
non-root UID, drops Linux capabilities, disables privilege escalation and
service-account token mounting, uses the runtime-default seccomp profile, and
mounts a bounded temporary volume so the container root filesystem can remain
read-only. Replace its example image digest with the immutable digest produced
by your release pipeline before deployment.

Fail-closed release behavior is tested with synthetic scanner JSON in the unit
test suite. The distributable branch does not include deployable intentionally
vulnerable images or manifests.

## GitHub Actions release pipeline

The repository workflow `.github/workflows/container-image-release-adk.yml`
uses isolated jobs:

1. SonarQube source analysis and Quality Gate enforcement runs in parallel
   with a dedicated Trivy configuration scan of the hardened Dockerfile and
   deployment configuration used for release.
2. The pipeline records the deterministic pre-build configuration decision,
   then builds the candidate locally to collect Trivy image vulnerability and
   secret evidence even when an earlier scanner blocks release. The final
   deterministic release-policy gate preserves every blocked decision and is
   the only path to authorization. Every Trivy occurrence is also ranked into
   an advisory triage queue, rendered in the Actions job summary, retained as
   Markdown/JSON/SARIF evidence, and uploaded to GitHub Code Scanning when that
   repository feature is available.
3. A report aggregation stage that exports SonarQube Cloud findings and joins
   them with the normalized Trivy image/configuration triage. It publishes one
   complete Markdown report for people and one JSON report for automation.
4. A separate Vertex AI/ADK advisory stage that consumes the bounded,
   secret-safe deterministic triage data and proposes prioritized remediation,
   compatibility checks, attack-path hypotheses, and verification steps.
5. A required-reviewer approval gate on the protected
   `container-production` GitHub Environment, followed by Docker Hub
   authentication and push. The publish job is reachable only after the Sonar
   and deterministic container-security jobs succeed and the machine-readable
   decision says `publish_allowed: true`.
6. A non-authoritative report-delivery stage sends the sanitized consolidated
   PDF and decision summary through Resend email and a compact Discord webhook
   embed. Delivery runs for blocked and release-ready candidates but cannot
   alter scanner evidence, deterministic policy, human approval, or publishing.

The generated **Consolidated Release Security Report** is the primary
team-facing report and is rendered directly in the Actions job summary. It
combines SonarQube source-code findings, Trivy configuration and container-image
findings, deterministic release policy, and agent advisory triage. Its internal
filename remains `ci-unified-security.md` for compatibility. Its companion
`ci-unified-security.json` retains the complete Sonar code findings, security
hotspots, Trivy image/configuration findings, metrics, and independent gate
outcomes. The original `ci-triage.json`, `ci-triage.md`, and `ci-trivy.sarif`
remain available as scanner-specific evidence and GitHub Security-tab input.
Scanner and agent triage are advisory: `policy_decision: not_evaluated` is
never approval. Only `ci-policy-decision.json` can authorize publishing.

Each scan stage also produces printable, sanitized reports:

- `ci-misconfiguration-report.html` and `ci-misconfiguration-report.pdf`
  describe the pre-build Dockerfile/deployment findings and configuration
  policy outcome.
- `ci-image-security-report.html` and `ci-image-security-report.pdf` describe
  the normalized image vulnerability, secret, and configuration findings.
  They are rendered from `ci-triage.json`, so raw secret match values are never
  included.

The PDFs are generated from the corresponding self-contained HTML using
headless Chrome. Required verification checks the PDF signature, trailer,
page objects, size, and embedded report title. When Poppler is available,
page-count and selectable-text verification run as additional checks.

### Report delivery configuration

Configure these GitHub repository secrets to enable delivery after the
consolidated report is generated:

- `RESEND_API_KEY`: a Resend key restricted to sending email.
- `RESEND_FROM_ADDRESS`: a sender on a Resend-verified domain.
- `RESEND_TO_ADDRESS`: one address or a comma-separated list of recipients.
- `DISCORD_WEBHOOK_URL_DEVSECOPS`: an incoming Discord channel webhook.

Email includes the sanitized consolidated PDF. Discord receives aggregate
counts, the deterministic decision, the bounded agent executive summary, and
links to the workflow and report artifact. Raw secret matches, credentials,
recipient addresses, and webhook URLs are never written to delivery evidence.

For production, store delivery secrets in a protected GitHub Environment and
restrict that environment to trusted branches. Pull requests from forks never
receive these secrets or run the delivery job.

If a release is blocked, reporting and evidence upload still run before the job
fails. This gives developers and security reviewers the explanation needed to
remediate the candidate without weakening the fail-closed release gate.

The ADK job is deliberately non-authoritative. A model outage or malformed
model response is recorded as `agent_status: unavailable` and cannot approve,
block, or change a release decision. Pull-request code receives no Google Cloud
credential; it produces the deterministic report plus an explicit unavailable
agent report. Trusted `main` runs authenticate to Vertex AI through Workload
Identity Federation. Pull requests and feature branches do not receive Google
Cloud credentials; the advisory is explicitly marked unavailable while
deterministic scanner and policy evidence remains authoritative.

Configure these GitHub repository settings before running it:

| Type | Name | Value |
| --- | --- | --- |
| Secret | `SONAR_TOKEN` | SonarQube project analysis token |
| Secret | `SONAR_HOST_URL` | SonarQube URL, such as `https://sonar.example.com` |
| Secret | `SONAR_ORGANIZATION` | SonarQube Cloud organization key |
| Secret | `WIF_PROVIDER` | Full Google Cloud WIF provider resource name |
| Secret | `WIF_SERVICE_ACCOUNT` | Least-privilege service account email |
| Secret | `GOOGLE_CLOUD_PROJECT` | Vertex AI project ID |
| Secret | `DOCKERHUB_TOKEN` | Docker Hub access token; do not use the account password |
| Secret | `DOCKERHUB_USERNAME` | Docker Hub namespace |
| Secret | `DOCKERHUB_REPOSITORY` | Existing public Docker Hub repository name |

Create a SonarQube project whose key is `agentic-devops-portfolio`, matching
`sonar-project.properties`. For SonarQube Cloud, set `SONAR_ORGANIZATION` to
the organization **key** shown in the SonarQube Cloud organization settings,
not the display name. Configure the Docker Hub repository as public in Docker
Hub; pushing an image does not itself change repository visibility.

To configure the settings without exposing tokens in the repository, edit the
git-ignored `.github/container-release.settings` placeholder file from the
repository root. Then authenticate GitHub CLI and upload the values:

```bash
gh auth login --hostname github.com
.github/scripts/configure-container-release-settings.sh
```

The helper refuses to upload unchanged placeholders and never prints token
values. A safe, commit-ready template is available at
`.github/container-release.settings.example`.

Pull requests run every analysis and gate but never publish. Pushes to `main`
publish the hardened `Dockerfile` only after deterministic authorization and a
reviewer approves the `container-production` deployment. Synthetic unit tests
prove that blocking findings cannot reach approval or publishing without
placing an unsafe deployable fixture in the production-ready branch.

To exercise the protected-environment approval UI without publishing, dispatch
the workflow from `main` with `approval_test: true` and `publish: false`. The
release-approval job waits for the configured reviewer, records the approval,
and the Docker Hub publish job remains skipped. Publishing is restricted to
`main`; feature branches cannot federate, approve, or push an image.
