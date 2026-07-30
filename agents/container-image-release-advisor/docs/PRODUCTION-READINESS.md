# Portfolio versus production readiness

## Implemented in the reference

- Separate pre-build and post-build deterministic scans
- Fail-closed configuration and release-policy checks
- Vulnerability, misconfiguration, and embedded-secret detection with Trivy
- SonarCloud code analysis
- Advisory-only Google ADK or Claude Agent SDK triage with bounded scanner input
- Protected environment approval before authentication and push
- Immutable GitHub Action commit pins
- Sanitized HTML/PDF/JSON/Markdown/SARIF evidence
- A safe-by-default release path plus synthetic fail-closed policy tests

## Organization-specific work required for production

- Replace the sample severity threshold with an approved policy that accounts
  for exploitability, fix availability, exception ownership, and expiry.
- Enforce branch protection, CODEOWNERS, signed commits/releases, and required
  checks outside this repository.
- Restrict WIF with immutable repository identifiers and trusted refs; use a
  dedicated service account with least privilege.
- Pin deployable images by digest and add image signing, provenance/SLSA
  attestations, SBOM verification, and registry admission policy.
- Add recurring registry rescans because vulnerability databases change after
  a build.
- Define artifact retention, access control, audit-log export, incident
  response, and approved exception workflows.
- Validate runner isolation and consider trusted/self-hosted runners for
  sensitive builds.
- Move release policy into organization-owned reusable workflows or a policy
  service so application repositories cannot weaken it.
- Add integration tests against your registry, SonarCloud organization,
  protected environments, and selected model-provider IAM/API configuration.

## Non-authoritative components

The selected Google ADK/Vertex AI or Claude Agent SDK/Sonnet 5 stage explains
evidence, proposes prioritization, and lists verification steps. It is not a
security gate. Model unavailability must be reported, but it cannot convert a
deterministic block into approval or create authorization when policy was not
evaluated.
