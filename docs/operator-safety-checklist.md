# Operator safety checklist for DevOps agents

Use this checklist before connecting any MCP server, agent skill, or reference agent from this catalog to real infrastructure. It turns the repo's safety model into a short runbook that works for Terraform, Kubernetes, CI/CD, identity, secrets, observability, and incident-response tools.

## 1. Start read-only

- Create a read-only token, service account, kubeconfig, or database user first.
- Prefer hosted read-only MCP endpoints or server flags when the vendor provides them.
- Do not give the agent broad cloud-admin, org-owner, cluster-admin, production database writer, or secrets-admin access for evaluation.
- Confirm the first demo can run without modifying infrastructure.

Good first actions:

```text
terraform plan
kubectl get / kubectl describe
cloud inventory list/read APIs
CI run, artifact, and log reads
observability metric/log/trace queries
issue, PR, incident, or ticket reads
```

## 2. Keep secrets out of model context

- Never paste raw tokens, kubeconfigs, private keys, customer data, database dumps, or unredacted logs into chat.
- Pass credentials through the MCP server, local environment, secret manager, or platform identity layer instead of prompt text.
- Redact command output before sharing it with the model.
- Treat screenshots and copied terminal buffers as possible secret carriers.

## 3. Require dry-run or proposal mode before writes

For write-capable entries, require one of these before any mutation:

| Domain | Safer preview |
| --- | --- |
| Terraform / OpenTofu | `plan`, drift report, policy check, cost estimate |
| Kubernetes | server-side dry run, diff, event/log review, scoped namespace test |
| CI/CD and GitOps | PR-only change, pipeline validation, preview environment |
| Cloud resources | change set, deployment preview, read-only inventory diff |
| Identity / secrets | separate request ticket, scoped test object, rollback plan |
| Incidents / tickets | draft/comment proposal before paging, closing, assigning, or escalating |

If the tool has no dry-run mode, keep it in read-only/proposal mode until a human can review the exact command or API request it would run.

## 4. Define the human approval gate

Before enabling writes, record:

- who can approve;
- where approval is captured, such as a PR review, protected environment, ticket, incident timeline, or chatops approval;
- which actions require approval, including deploy, delete, rotate, page, close, merge, or permission changes;
- which actions remain blocked entirely.

Client-side approval prompts are useful, but server-side controls, RBAC, protected environments, and policy-as-code are stronger because they do not depend on a single chat client behaving correctly.

## 5. Limit blast radius

- Scope cloud roles to one account, project, subscription, region, or resource group for the first run.
- Scope Kubernetes credentials to one namespace and avoid `cluster-admin`.
- Use a non-production workspace, preview stack, sandbox repository, or test incident service when possible.
- Separate read and write credentials so switching to write mode is an explicit operator action.
- Time-box elevated tokens and rotate or revoke them after evaluation.

## 6. Capture evidence and audit logs

Keep enough evidence for another operator to replay the decision:

- catalog entry and version or commit reviewed;
- upstream documentation links used for scoring;
- commands, tool calls, and redacted outputs;
- plan/diff/report artifacts;
- approval record and approver;
- final action result and rollback/follow-up.

For deeper reviews, copy the findings into [`templates/agent-scorecard.md`](../templates/agent-scorecard.md) and attach the scorecard to the PR, ticket, incident, or runbook that authorized the agent.

## 7. Production-adjacent go/no-go

Do not move beyond evaluation until all statements are true:

- the entry's `action_level`, `human_approval`, `evidence_tracing`, `maturity`, `risk_notes`, `operator_note`, and labels match the real tool surface;
- credentials are least-privilege and not present in model context;
- dry-run/proposal evidence was reviewed;
- write actions have an explicit human approval path;
- audit logs or evidence traces are available after the run;
- rollback, revoke, or disable steps are known.

If any item is unclear, keep the agent read-only and open a catalog or upstream issue before production use.
