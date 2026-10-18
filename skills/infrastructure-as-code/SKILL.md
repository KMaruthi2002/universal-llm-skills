---
name: infrastructure-as-code
description: >-
  Define, change, and review cloud and platform infrastructure as code with
  tools such as Terraform, OpenTofu, Pulumi, CloudFormation, CDK, Bicep,
  Crossplane, or Ansible: state management and locking, modules, environment
  separation, plan review, drift detection, secrets, blast radius, refactoring
  without destroying resources, and importing existing infrastructure. Use
  when someone asks to write or modify Terraform/Pulumi/CloudFormation, review
  a plan, set up remote state, structure modules or environments, import
  click-ops resources, fix drift or state errors, or safely rename or move
  resources. Not for choosing which cloud services to use (see
  cloud-architecture) or for app deployment pipelines.
metadata:
  category: devops
  related: cloud-architecture, ci-cd-pipelines, kubernetes, secure-coding, git-workflow, code-review, dependency-management
---

# Infrastructure as Code

Infrastructure as code (IaC) means the desired state of servers, networks, databases, permissions, and DNS lives in version-controlled files, and a tool computes and applies the difference between that desired state and reality. The benefits — review, repeatability, audit trail, disaster recovery — only materialise if the code is the real source of truth and every change goes through plan, review, and apply. The cost of mistakes is unusually high: a one-line change can delete a production database. This skill is as much about safety as about structure.

Terraform/OpenTofu HCL is used in examples because it is the most widespread; the principles apply to Pulumi, CloudFormation/CDK, Bicep/ARM, Crossplane, and configuration-management tools like Ansible.

## Scope

Covers: tool choice, state, modules, environments, plan/apply workflow, review of plans, drift, secrets, blast radius, refactoring (moves/renames), imports, testing and policy, and CI for IaC.

Hands off to:

- Which services and architecture to use → `cloud-architecture`.
- Kubernetes manifests and in-cluster objects → `kubernetes` (though IaC often provisions the cluster).
- App build/deploy pipelines → `ci-cd-pipelines`.
- General code review practice → `code-review`.

## Core principles

**1. The plan is the change; review the plan, not just the code.** A small code diff can produce a large plan (a renamed resource becomes destroy-and-create; a changed immutable attribute forces replacement). Always read the full plan output before applying, with particular attention to destroy and replace actions.

**2. State is critical, sensitive infrastructure.** For state-based tools (Terraform/OpenTofu, Pulumi), the state file maps code to real resource IDs. Lose it and the tool forgets what it manages; corrupt it and applies do strange things; leak it and you may leak secrets (state often contains passwords, keys, and connection strings in plain text). Store it remotely, encrypted, access-controlled, versioned, and locked.

**3. Small blast radius.** Split infrastructure into units (stacks, root modules, workspaces) so a single apply can only affect a bounded set of resources. A monolithic state with every environment and service in it means every plan is slow, every apply is risky, and one lock blocks everyone.

**4. Environments are instances of the same code.** Dev, staging, and production should differ in inputs (sizes, counts, names, feature toggles), not in code paths. Copy-pasted environment directories drift until staging proves nothing about production.

**5. Everything through the pipeline, nothing by hand.** Manual console changes ("click-ops") create drift that the next apply will revert or fight. Emergency manual changes happen; reconcile them back into code promptly.

**6. Make destruction hard.** Protect stateful and critical resources with deletion protection, prevent-destroy lifecycle rules, retention policies, and backups. Deletion should require deliberate, reviewed steps.

**7. Pin versions.** Pin the IaC tool version, provider/plugin versions (with a lock file), and module versions. An unpinned provider upgrade can change defaults or plan unexpected replacements.

## Discovering context first

1. **Identify the tool(s) and versions:** `*.tf` / `.terraform.lock.hcl` / `.terraform-version` / `.opentofu-version`, `Pulumi.yaml` and `Pulumi.<stack>.yaml`, `template.yaml` / `*.cfn.yaml`, `cdk.json`, `*.bicep`, Crossplane compositions, `ansible.cfg` and playbooks, wrappers like Terragrunt, Atmos, or Spacelift/Env0/Terraform Cloud configs.
2. **Find the state backend and how locking works** (object storage plus lock table, managed backend, Pulumi service, CloudFormation's own stack state). Never change the backend casually.
3. **Map the layout:** which directories/stacks are root modules, which are reusable modules, how environments are separated (directories, workspaces, stacks, separate accounts/projects/subscriptions).
4. **Find the apply workflow:** CI pipeline with plan-on-PR and apply-on-merge? A PR automation tool (e.g. Atlantis)? Manual applies by named people? You must fit into it.
5. **Read conventions:** naming and tagging schemes, required tags (owner, cost centre, environment), module sources (registry, git tags, monorepo paths), variable validation patterns, formatting/linting config.
6. **Check for policy-as-code** (OPA/Conftest, Sentinel, Checkov, tfsec/Trivy, cfn-guard, cloud-native policies) that will reject non-compliant changes.
7. **Check credentials you would run with.** Prefer read-only credentials for planning. Never apply with credentials broader than the change requires.

## Tool choice (when starting fresh)

| Tool | Model | Strengths | Trade-offs | Choose when |
|---|---|---|---|---|
| Terraform / OpenTofu | Declarative HCL, state file | Huge provider ecosystem, multi-cloud, mature | HCL limited for complex logic; state to manage; licensing differences between the two | Default for multi-cloud or mixed SaaS providers |
| Pulumi | General-purpose languages, state | Real loops/abstractions, testing in your language | Easier to write overly clever code; team must know the language | Teams wanting software-engineering practices in infra |
| CloudFormation / CDK | AWS-native, provider-managed state | No state files to host, deep AWS integration, rollback on failure | AWS-only; slower; CDK synthesises to CloudFormation | AWS-only shops |
| Bicep / ARM | Azure-native | First-class Azure support, no state files | Azure-only | Azure-only shops |
| Crossplane | Kubernetes controllers reconcile cloud resources | Continuous reconciliation, k8s-native APIs for platform teams | Requires k8s and operator expertise | Platform teams offering self-service via Kubernetes |
| Ansible / Chef / Puppet / Salt | Configuration management (mostly procedural/convergent) | Configure OS and software on servers | Weaker at provisioning cloud resources; idempotency depends on module quality | Configuring long-lived VMs; complements provisioning tools |

If the project already uses a tool, stay with it unless the user asks for a migration; mixing tools for the same resources causes ownership fights.

## State management

- **Remote backend** with encryption at rest, versioning (to recover from corruption), and locking (to stop concurrent applies). Restrict access to the people and pipelines that plan and apply.
- **One state per blast-radius unit.** Typical splits: by environment × layer (network, data, compute/app), or by service. Shared foundations (VPC, DNS zones, identity) are separate from fast-changing app infrastructure.
- **Cross-state references:** read outputs from another state (remote state data sources, stack references) or look resources up by tag/name via data sources. Prefer explicit outputs over reaching into another stack's internals; keep dependencies one-directional (app depends on network, never the reverse).
- **Never edit state by hand.** Use the tool's commands (`state mv`, `state rm`, `import`, `moved`/`import`/`removed` blocks, Pulumi `state` commands). Back up state before any state operation.
- **Lock problems:** a stale lock after a crashed run can be force-unlocked, but only after confirming nobody else is mid-apply. Force-unlocking during someone's apply corrupts state.
- **Secrets in state:** assume state contains secrets. Treat read access to state as read access to those secrets. Prefer designs where secrets are generated and stored in a secret manager and only referenced by ARN/ID.

## Modules

Modules package reusable infrastructure. They are valuable and frequently overdone.

**Write a module when** the same group of resources is instantiated several times with variation (a service's standard stack, a standard bucket with encryption and logging), or when it encodes organisational standards others must follow.

**Do not write a module when** it would wrap a single resource with the same inputs (a pass-through that adds indirection, not value), or when there is only one instance and no expectation of more.

Good module design:

- Small, focused interface: required inputs for what genuinely varies, sensible secure defaults for the rest. Dozens of optional variables mirroring every provider argument is a sign the module adds nothing.
- Validate inputs (types, allowed values, validation rules) so mistakes fail at plan time.
- Output what consumers need (IDs, ARNs, endpoints), nothing more.
- No provider configuration inside reusable modules; the caller configures providers. This keeps modules usable across accounts and regions.
- Version modules (git tags, registry versions) and pin consumers to versions; change modules with release notes, because every consumer's plan may change.
- Avoid deep nesting (module calling module calling module); it makes plans and debugging opaque. Two levels is usually plenty.
- Prefer well-maintained community or vendor modules for commodity patterns only after reading them: they can be large, opinionated, and change behaviour between major versions.

## Environments

Common approaches:

| Approach | How | Pros | Cons |
|---|---|---|---|
| Directory per environment calling shared modules | `envs/prod/main.tf` with prod inputs | Explicit, separate state and backend per env, easy to give different permissions | Some boilerplate repeated; mitigate with wrappers like Terragrunt |
| Workspaces (Terraform/OpenTofu) | Same code, different state per workspace | Little duplication | Easy to apply to the wrong workspace; same backend credentials for all envs; differences hidden in conditionals |
| Stacks with config files (Pulumi, CDK) | `Pulumi.prod.yaml` | Clean separation of config | Same caveats on credentials as workspaces unless configured separately |

Strong recommendations regardless of approach:

- **Separate cloud accounts/projects/subscriptions per environment** (at least production vs. everything else). This is the strongest blast-radius control available: a mistake in dev credentials physically cannot touch production.
- Different credentials and approval requirements for production applies.
- Promote changes through environments in order (dev → staging → prod) using the same module versions.
- Keep environment differences in variables; avoid `if env == "prod"` branches scattered through code, except for genuine differences such as deletion protection or multi-AZ.

## The plan → review → apply workflow

1. **Format, validate, lint:** `fmt`, `validate`, linters (e.g. tflint), security scanners (e.g. Checkov, Trivy, tfsec), policy checks.
2. **Plan** against the target environment with read-only or plan-scoped credentials. Save the plan file so the apply executes exactly what was reviewed (`plan -out`, change sets in CloudFormation, `pulumi preview` followed by `up` with the same inputs).
3. **Review the plan**, not just the code diff. Post the plan summary to the PR. Reviewers look for:
   - **Destroy (`-`) and replace (`-/+`) actions**, especially on stateful resources (databases, disks, buckets, queues, DNS zones, KMS keys, identity resources). Ask: why is this being replaced? Is data lost? Is there downtime?
   - **Unexpected changes** to resources the PR did not intend to touch, which usually indicate drift, a provider upgrade, or a shared module change.
   - **IAM and network exposure changes:** new public access, wildcard permissions, security group rules open to `0.0.0.0/0`.
   - **Count/`for_each` key changes** that will recreate many resources.
   - **Cost implications:** new instances, larger sizes, NAT gateways, provisioned throughput.
4. **Apply** through the pipeline, after approval, from the saved plan. For production, require a second person's approval.
5. **Verify** the result: resources exist and work, application health is fine, a fresh plan shows no changes.

If a plan is too large to review meaningfully, the change is too large; split it.

## Refactoring without destroying

Renaming a resource, moving it into a module, or changing a `count` to `for_each` changes its address, which the tool interprets as "destroy old, create new" unless told otherwise.

- Use declarative move instructions (`moved` blocks in Terraform/OpenTofu, `aliases` in Pulumi) or state move commands, and confirm the plan then shows **no** destroy/create for the moved resources.
- Removing a resource from management without deleting it: `removed` blocks / `state rm`, plus `prevent_destroy` or deletion protection as a safety net while refactoring.
- CloudFormation: changing logical IDs replaces resources; use stack refactoring features or retain policies plus import.
- Test the refactor in a lower environment and compare plans before production.

## Importing existing infrastructure

Bringing click-ops resources under management:

1. Inventory what exists (console, CLI listing, cloud asset inventory). Decide ownership: which stack will own each resource. One resource must have exactly one owner.
2. Write the resource code to match the existing configuration as closely as possible, or use the tool's config generation from import to get a starting point (then clean it up — generated code is verbose and often hard-codes values).
3. Import (`import` blocks or command, `pulumi import`, CloudFormation resource import).
4. **Plan until it shows no changes** (or only intended, reviewed changes). An import followed by a plan that wants to modify or replace the resource means the code does not match reality; fix the code, do not apply.
5. Add protections (deletion protection, prevent-destroy) for critical imported resources.
6. Lock down the console path afterwards (permissions, policy) so drift does not immediately recur.

Tools that bulk-generate code from existing accounts can help with inventory but produce code that needs significant restructuring into sensible modules and states.

## Drift

Drift is any difference between code/state and reality: manual changes, other tools modifying the same resources, provider-side defaults, autoscaling.

- Detect it with scheduled plans (or the platform's drift detection) that alert when the plan is non-empty.
- For each drift, decide: was the manual change correct? Then **update the code to match** and plan to zero. Was it wrong? Then apply to revert it — but check first whether something depends on it now (an emergency fix during an incident, for example).
- For attributes legitimately managed elsewhere (autoscaler-managed desired counts, tags added by other systems), tell the tool to ignore them (e.g. `ignore_changes`) with a comment explaining why. Overusing ignore hides real drift.

## Secrets

- Never put secret values in code, `tfvars` committed to git, or default variable values. Mark variables and outputs as sensitive so they are redacted in plan output (redaction in output does not remove them from state).
- Prefer letting the cloud generate and store secrets (managed database master passwords stored in a secret manager, generated keys stored directly in a secret store) and pass references, not values.
- Inject credentials for the IaC run via short-lived federated identity (OIDC from CI to the cloud) rather than long-lived keys in CI variables.
- Plan output, logs, and state can all reveal secrets; restrict who can view them and avoid pasting plans with sensitive values into public places.
- Encrypted-in-git approaches (SOPS, sealed secrets, git-crypt) are acceptable when the team already manages the keys well.

## Testing and policy

- **Static checks** on every PR: formatting, validation, linting, security/policy scanning. Cheap and catch most mistakes.
- **Plan-based tests:** assert properties of the plan (no public buckets, required tags present, no destroys in production) with policy-as-code tools.
- **Module tests:** the tool's native test framework (e.g. `terraform test` / `tofu test`), Terratest, Pulumi unit tests with mocks, or deploying the module to a sandbox account and checking it works, then destroying it. Integration tests cost money and time; reserve them for widely used modules.
- **Policy guardrails** at the cloud level (organisation policies, service control policies, Azure Policy) catch what IaC policy misses, including click-ops.

## Structuring a repository

There is no single correct layout; follow the project's. When starting fresh, an illustrative shape that keeps blast radius small:

```text
modules/                 # reusable, versioned building blocks
  network/
  service/
  database/
live/                    # root modules, one state each
  shared/                # org-wide: DNS zones, identity, logging account
  prod/
    network/
    data/
    app-orders/
  staging/
    network/
    data/
    app-orders/
```

What makes it work, regardless of exact names:

- Each leaf under `live/` is a separate root with its own state, backend key, and credentials.
- Layers change at different rates: networks rarely, data stores occasionally, app infrastructure often. Separate states let the frequent changes happen without touching the rare, dangerous ones.
- Dependencies flow downward: apps read network and data outputs; network never reads app outputs.
- A monorepo for infrastructure eases cross-cutting changes; separate repos per team ease ownership and permissions. Either works if module versions are pinned.

## CI for infrastructure code

- **On pull request:** format check, validate, lint, security/policy scan, cost estimate, and a plan for every affected root, with the plan summary posted to the PR. Plans run with read-only credentials where the tool allows.
- **On merge (or on an explicit approval comment, as with PR-automation tools):** apply the reviewed plan to non-production automatically and to production after required approval.
- **Serialise applies per state.** Locking prevents corruption, but queueing applies per root avoids confusing failures and stale plans.
- **Stale plans:** a plan reviewed on Monday may be wrong on Wednesday if main moved or reality drifted. Re-plan immediately before apply and fail if the plan differs from the reviewed one in destructive ways.
- **Scheduled drift plans** for each root, alerting on non-empty plans.
- **Affected-root detection:** changes to a shared module should trigger plans for every root that uses it; otherwise a module change lands silently and surprises the next unrelated PR.

## Version and provider upgrades

- Upgrade the IaC tool and providers deliberately, one at a time, in a dedicated PR, and read the changelog for default changes and deprecations.
- Run plans across all roots after an upgrade; an upgrade PR should produce empty plans (or only explained changes). Any planned replacement of an existing resource after a provider bump is a red flag to investigate before applying.
- Major-version upgrades of community modules often rename resources internally; check whether the module ships move instructions, and plan carefully.
- Keep lock files committed so every developer and pipeline uses the same provider builds.

## What goes wrong during apply

| Failure | What it means | Response |
|---|---|---|
| Apply fails midway | Some resources created/changed, others not; state reflects what succeeded | Read the error, fix the cause, re-plan, review the remaining changes, apply again |
| "Resource already exists" | Something outside this state created it (click-ops, another stack, previous partial apply that lost state) | Find the owner; import it or rename; never delete the existing one to make apply pass without confirming it is unused |
| Lock held | Another run is active, or a crashed run left a lock | Confirm no active run, then force-unlock |
| Timeouts on slow resources | Databases, clusters, certificates can take tens of minutes | Increase timeouts in config; check the resource in the console before retrying, it may still be creating |
| Dependency violation on destroy | Something still uses the resource (ENIs, attached policies, non-empty buckets) | Find and remove the dependent first, through code; avoid force-delete flags on data stores |
| Permission denied | Apply identity lacks rights | Grant the minimal additional permission; do not switch to an admin identity to get past it |
| Eventual consistency errors | Cloud API returned before the resource was usable (often IAM) | Retry once; if recurrent, add explicit dependencies or waits |

## Configuration management alongside provisioning

When IaC provisions VMs that are then configured with Ansible, Chef, Puppet, Salt, or cloud-init:

- Prefer immutable images (built with a tool like Packer) plus minimal boot-time configuration over long-lived servers mutated repeatedly; immutable images make every instance identical and rollback a matter of choosing the previous image.
- When configuration management is needed, keep it idempotent: running it twice should change nothing the second time. Check with a dry-run/check mode before applying to production hosts.
- Keep a clear boundary: the provisioning tool owns the existence of the machine and its network; configuration management owns what runs on it.

## Blast radius and safety

Mandatory safeguards when working with IaC:

- **Never run `apply` or `destroy` against production without explicit user confirmation** after they have seen the plan. State the environment, account, and the count of adds/changes/destroys.
- **Never run `destroy`** on shared or production stacks without the user explicitly requesting it, and confirm backups/snapshots for stateful resources first. Prefer targeted removal through code changes, reviewed in a plan.
- Avoid `-target` / partial applies except for recovery; they leave state inconsistent with code and skip dependencies. If used, follow with a full plan.
- Avoid `-auto-approve` outside fully automated pipelines that apply a reviewed saved plan.
- Protect critical resources: deletion protection on databases and load balancers, `prevent_destroy` lifecycle rules, bucket versioning and object lock where appropriate, retention on KMS keys (key deletion makes data encrypted with them unrecoverable).
- Confirm the active credentials/profile/subscription before any plan; print the caller identity. Planning prod with dev credentials fails harmlessly; applying dev code with prod credentials does not.
- **Cost blowups:** watch for resources with large or open-ended costs — NAT gateways, provisioned IOPS, large GPU instances, high-throughput streams, cross-region replication, logging with no retention. Mention expected cost when adding them; use cost-estimation tools (e.g. Infracost) in PRs where available.
- If something goes wrong mid-apply, do not keep re-running blindly. Read the error, check what was partially created, plan again, and decide.

## What belongs in IaC, and what does not

| Usually in IaC | Usually elsewhere | Why |
|---|---|---|
| Networks, DNS zones, load balancers, clusters, databases, buckets, queues | Application releases and container image versions | Apps change many times a day; their deploys belong to the app pipeline or GitOps |
| IAM roles, policies, service accounts | Secret *values* | Values belong in a secret manager; IaC creates the container and grants access |
| Monitoring, alert rules, dashboards (when the tool supports them) | Data inside databases | Data is not infrastructure; use migrations and backups |
| Third-party SaaS config with providers (CDN, DNS, monitoring) | One-off experiments in a sandbox account | Experiments can be click-ops in an isolated account that is wiped regularly |

Putting app versions into the same state as the database means every app deploy plans against the database; keep them apart.

## Pitfalls and anti-patterns

- **Applying without reading the plan**, or reading only the summary line.
- **One giant state** for everything: slow, risky, lock contention.
- **Copy-pasted environment code** diverging over time.
- **Hard-coded IDs and ARNs** scattered through code instead of references or data lookups.
- **Unpinned providers and modules** producing surprise plans after upgrades.
- **`count` with lists** where removing an element shifts indices and recreates everything after it; prefer `for_each` with stable keys.
- **Secrets in tfvars, defaults, or outputs** committed to git.
- **Two tools (or two stacks) managing the same resource**, fighting each other on every apply.
- **Ignoring drift** until an apply reverts an emergency fix during the next incident.
- **Lifecycle `ignore_changes` used to silence plans** rather than to model genuine external ownership.
- **Modules wrapping single resources** with every argument passed through.
- **Long-lived admin keys** on developer laptops used for applies.

## Verification

- [ ] `fmt`/`validate`/lint/security scans pass.
- [ ] Plan reviewed in full: no unintended destroys/replacements, no unexpected resources, IAM/network exposure changes understood, cost noted.
- [ ] Applied via the agreed workflow, from a saved/reviewed plan, to the intended environment (identity confirmed).
- [ ] A fresh plan after apply shows no changes.
- [ ] The resulting infrastructure works (application health, connectivity, permissions), not just exists.
- [ ] State is remote, locked, encrypted, and backed up; no secrets added to git.
- [ ] Critical resources have deletion protection.
- [ ] For refactors and imports: plan showed zero destroy/create for moved/imported resources before applying.

Report: which environment(s), the plan summary (add/change/destroy counts), what was applied or deliberately not applied, and any follow-ups (drift found, imports pending, risky resources without protection).

## Worked example: a rename that would have deleted the database

Situation: a PR "tidies up naming" by renaming `aws_db_instance.main` to `aws_db_instance.orders` and moving it into a new `database` module. The code diff is clean and small.

The plan shows `1 to add, 0 to change, 1 to destroy` for the database. Applying would create an empty new database and delete the production one (deletion protection would make the destroy fail halfway, leaving a confusing partial state; without it, data is gone unless a final snapshot is taken).

Correct approach: add a `moved` block from `aws_db_instance.main` to `module.database.aws_db_instance.orders`, re-plan, and confirm the plan shows the database as moved with zero destroy/create. Apply in staging first, compare, then production.

The lesson to carry: renames and module moves are address changes; any plan that destroys a stateful resource needs an explanation before anyone approves it.
