# Demonstration runs

The repository intentionally supports one clean path and one blocked path.
Both produce evidence; only the clean path can reach approval and publishing.

## Successful, non-publishing validation

In **Actions**, choose either **ADK container image release** or **Claude
container image release**, then select:

```text
dockerfile: Dockerfile
publish: false
approval_test: false
```

Expected behavior:

1. SonarCloud and pre-build Trivy configuration scans pass.
2. The candidate image is built locally on the runner.
3. Trivy scans the real image for vulnerabilities and embedded secrets.
4. Deterministic policy authorizes the candidate.
5. The selected ADK or Claude agent produces non-authoritative advisory triage
   when its authentication is available.
6. The overall summary and all three deterministic reports are produced.
7. Approval and publishing are skipped because `publish` is false.

Download the generated report artifacts from the workflow run. Scanner evidence
is point-in-time data, so always rerun current scanners for a release decision.

## Intentionally blocked validation

Run the same workflow with:

```text
dockerfile: Dockerfile.vulnerable
publish: true
approval_test: false
```

Expected behavior:

1. The pre-build configuration gate detects intentional HIGH findings.
2. A pre-build HTML/PDF report is still uploaded.
3. The Docker build, image scan, approval, login, and push jobs are unreachable.
4. The workflow is red by design; this proves fail-closed behavior.

Download the pre-build report artifact to review the intentional findings and
the deterministic blocked decision.

> Never weaken the policy merely to make the intentionally blocked run green.

## The three team-facing reports

| Artifact | Contents | Primary audience |
| --- | --- | --- |
| `pre-build-security-report-*` | Sonar code findings plus Trivy misconfigurations | Developers and platform engineers |
| `container-image-security-report-*` | Image CVEs, packages, secrets, and triage | Application and container owners |
| `consolidated-release-security-report-*` | Overall decision, all gate results, and provider-specific advisory status | Release approvers and security teams |

The separate `Claude container image release` workflow produces the
same three required reports and deterministic decisions as the Google ADK
workflow. Its consolidated report contains a non-authoritative Claude Sonnet 5
interpretation; that interpretation cannot affect authorization.
