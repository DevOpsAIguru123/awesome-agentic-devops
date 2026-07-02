# Safety Model

Infrastructure agents need a stricter safety bar than generic chat assistants. The default posture should be read-only observation, proposal-mode recommendations, and human approval before any write action.

## Principles

### Read-only first

Start with commands that inspect state: `terraform plan`, `kubectl get`, `kubectl describe`, logs, metrics, traces, CI artifacts, and cloud inventory APIs. The first version of any agent should work without write credentials.

### Proposal mode before write mode

Agents should produce a proposed change, not apply it. For code changes, prefer pull requests. For infrastructure changes, require a reviewed plan and a separate human approval step.

### Human approval gates

Any action that mutates infrastructure, deploys code, changes IAM, deletes resources, rotates secrets, or updates production configuration must require explicit approval.

### Least-privilege credentials

Grant only the permissions needed for the current workflow. Separate read-only credentials from write credentials. Avoid broad admin tokens.

### Dry-run validation

Use dry-run capabilities where possible. Examples include Terraform plans, Kubernetes server-side dry runs, CI validation, policy-as-code checks, and preview environments.

### Terraform plan before apply

Terraform agents should inspect plans before apply. They should flag destroys, IAM changes, public exposure, cost-sensitive resources, missing tags, and high-blast-radius replacements.

### Kubernetes read paths before mutate paths

Kubernetes agents should use `kubectl get`, `kubectl describe`, events, and logs before any `patch`, `scale`, `delete`, or rollout command.

### CI checks before PR merge

Agents that edit pipelines or infrastructure code should rely on CI checks, tests, linters, policy checks, and human review before merge.

### Audit logs and evidence traces

Agent outputs should cite evidence: commands run, plan excerpts, log lines, metrics, docs, runbooks, and policy checks. Summaries without evidence are not enough for production-adjacent workflows.

### Secrets never exposed to model context

Do not paste secrets, cloud credentials, kubeconfigs, private keys, tokens, or sensitive customer data into model context. Redact logs and artifacts before analysis.

## Minimum safety bar for this repo

- Every listed project must have an `action_level`.
- Write-capable entries must carry the ⚠️ label unless the write surface is clearly isolated.
- Approval-aware entries should carry 🛡️ only when a meaningful approval or safety mechanism is documented or strongly evident.
- Evidence-aware entries should carry 📊 only when there is a trace, eval, audit, cited evidence, or equivalent mechanism.
