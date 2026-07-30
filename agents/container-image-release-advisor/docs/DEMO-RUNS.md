# Validation and demonstration runs

The distributable workflows are safe by default: they build only the hardened
sample and scan its hardened Kubernetes deployment. Fail-closed behavior is
covered by synthetic policy tests. Intentionally vulnerable, deployable
fixtures are kept outside this production-ready branch.

## Successful, non-publishing validation

In **Actions**, choose either **ADK container image release** or **Claude
container image release**, then select:

```text
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

## Isolated blocked-run evidence

The intentionally vulnerable demonstration is preserved separately in
[demonstration PR #74](https://github.com/DevOpsAIguru123/awesome-agentic-devops/pull/74).
Its [successful security demonstration run](https://github.com/DevOpsAIguru123/awesome-agentic-devops/actions/runs/30571416613)
built an isolated candidate, collected complete SonarQube and Trivy evidence,
and proved that deterministic policy prevents approval and publishing.

The demonstration branch is evidence, not a source for deployment. Teams that
need their own blocked-path exercise should use an organization-approved test
repository or short-lived fixture branch with publishing disabled. Never add
the vulnerable fixture to the default or release branch, and never weaken
policy merely to make a deliberately blocked run green.

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
