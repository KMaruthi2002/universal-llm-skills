---
name: ci-cd-pipelines
description: >-
  Design, build, speed up, and repair continuous integration and delivery
  pipelines on any CI system (e.g. GitHub Actions, GitLab CI, Jenkins,
  CircleCI, Buildkite, Azure Pipelines): stages, caching, parallelism,
  artifacts, environments and promotion, secrets, deployment strategies
  (rolling, blue/green, canary), and pipeline speed and flakiness. Use when
  someone asks to set up CI, add a deploy step, make the build faster, fix a
  flaky or broken pipeline, add caching, gate deploys on tests, or choose a
  deployment strategy. Not for writing the tests themselves or for versioning
  and release planning.
metadata:
  category: devops
  related: testing-strategy, containerization, infrastructure-as-code, release-management, release-readiness, secure-coding, git-workflow, kubernetes
---

# CI/CD Pipelines

A pipeline is the factory that turns a commit into running software. A good one is fast enough that people wait for it instead of working around it, trustworthy enough that green means "safe to ship", and boring enough that deploying on a Friday afternoon is not an act of courage. This skill covers how to design one, how to make an existing one faster and less flaky, and how to deploy from it safely.

## Scope

Covers: pipeline structure, triggers, jobs and stages, caching, parallelism, artifacts, environment promotion, secrets in CI, deployment strategies, pipeline performance, flaky-test handling, and supply-chain hygiene of the pipeline itself.

Does not cover, and hands off to:

- What tests to write and at which level → `testing-strategy`, `end-to-end-testing`.
- Building the container image itself → `containerization`.
- Provisioning the infrastructure the pipeline deploys to → `infrastructure-as-code`.
- Version numbers, changelogs, release cadence, feature flags → `release-management`.
- Go/no-go checklist for a specific release → `release-readiness`.
- Branching model and merge policy → `git-workflow`, `pull-request-workflow`.

## Core principles

**1. Build once, promote the same artifact.** Compile, package, or build the image exactly once per commit, give it an immutable identifier (commit SHA, content digest), and deploy *that identical artifact* to every environment. Rebuilding per environment means what you tested is not what you shipped: a dependency resolved differently, a base image moved, a build flag differed. Configuration differs between environments; the artifact does not.

**2. The pipeline is code and is reviewed like code.** Keep pipeline definitions in the repository, versioned with the code they build. A pipeline edited through a web UI has no history, no review, and no way to reproduce last month's build.

**3. Fast feedback first, expensive confidence later.** Order work so the cheapest, most likely-to-fail checks run first (lint, type-check, unit tests) and the slow ones (integration, end-to-end, performance) run after or in parallel. A developer should learn about a typo in under five minutes, not after a 40-minute end-to-end suite.

**4. Green must mean something.** If the team routinely re-runs failures until they pass, or merges on red "because that test is always flaky", the pipeline has stopped carrying information. Flakiness is a reliability bug in the pipeline, not background noise.

**5. Deploys must be reversible and observable.** Every deployment strategy is a way to limit blast radius and make rollback cheap. A deploy you cannot watch (no health signal) or undo (no previous artifact, irreversible migration) is a gamble regardless of how good the tests are.

**6. Least privilege for the pipeline.** CI runners execute arbitrary code from every branch and pull request. Treat them as a high-value attack surface: scoped, short-lived credentials; production secrets only available to protected branches and approved jobs; third-party actions/plugins pinned.

**7. Hermetic and reproducible where it matters.** Pin tool versions, lock dependencies, and avoid "latest" tags so that a re-run of an old commit produces the same result. Non-reproducible builds turn every failure into an archaeology project.

## Discovering context first

Before proposing or changing anything:

1. **Find the existing CI config.** Look for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `azure-pipelines.yml`, `buildkite/`, `bitbucket-pipelines.yml`, `cloudbuild.yaml`, `Taskfile`, `Makefile`, `justfile`. Many repos have more than one (legacy plus new); find out which is live.
2. **Find the local entry points.** Most good pipelines call the same commands developers run locally (`make test`, `npm run ci`, `./scripts/test.sh`). Reuse them rather than duplicating logic in YAML; it keeps local and CI behaviour in sync.
3. **Read recent run history if you can.** Durations per job, failure rates, which jobs are re-run most. This tells you where time and flakiness actually are, rather than where you guess they are.
4. **Identify the deploy target and mechanism.** Container orchestrator, serverless platform, VM fleet, static hosting, app store, package registry. The strategy options depend on it.
5. **Identify the branching and release model** (trunk-based, release branches, tags trigger releases). The trigger design must match it.
6. **Find how secrets get in today** (CI secret store, OIDC federation to a cloud, vault, env files). Do not introduce a second mechanism without reason.
7. **Note organisational constraints:** required approvals, change windows, compliance evidence (who approved, what was deployed when), self-hosted runner requirements, network restrictions.

Follow the project's conventions for job naming, script locations, and reusable templates. If they have a shared pipeline library or reusable workflows, extend it rather than writing a one-off.

## Designing a pipeline

### Typical stage shape

There is no mandatory layout, but most healthy pipelines converge on something like this, with each stage gating the next:

| Stage | Purpose | Typical budget |
|---|---|---|
| Validate | Lint, format check, type-check, config validation, secret scanning | < 2–3 min |
| Build | Compile, bundle, build image; produce versioned artifact | < 5–10 min |
| Unit test | Fast isolated tests, coverage | < 5–10 min, parallelised |
| Integration | Tests against real dependencies (DB, queue) in containers | < 10–15 min |
| Package & publish | Push artifact/image to registry with immutable tag, SBOM, signature | < 2–5 min |
| Deploy to staging/preview | Same artifact, staging config | minutes |
| Post-deploy checks | Smoke tests, synthetic checks, E2E against the deployed env | < 10–15 min |
| Promote to production | Manual approval or automated gate; progressive rollout | minutes to hours |

Budgets are heuristics: a commit-to-merge-signal under ~10 minutes keeps people in flow; 10–20 is tolerable; past 30 people batch changes, context-switch, and start bypassing it.

### Triggers

- **Pull/merge request:** run validate, build, unit, integration. Do not deploy to production. Preview environments per PR are valuable for web apps if cheap to spin up and torn down automatically.
- **Push to main/trunk:** full pipeline, publish artifact, deploy to staging, optionally continue to production.
- **Tag or release branch:** for projects that release discretely (libraries, mobile, on-prem software).
- **Schedule:** nightly long suites, dependency audits, rebuilding images to pick up base-image security patches.
- **Manual:** deploy a specific artifact to a specific environment, rollback, re-run migrations. Make the inputs explicit (artifact ID, environment) and validated.

Use path filters in monorepos so a docs change does not run the backend suite, but be careful: path filters that skip required checks can block merges or, worse, let a change through untested if a shared file is missed. Prefer "compute affected targets" tooling (e.g. Nx, Turborepo, Bazel, Pants, or a dependency-aware script) over hand-maintained path lists once a monorepo grows.

### Artifacts and promotion

- Tag artifacts with the commit SHA (and optionally a semantic version). Never deploy a mutable tag like `latest` to production; you lose the ability to know what is running and to roll back precisely. For images, deploy by digest where the platform supports it.
- Store build outputs in a registry or artifact store with retention policies; keep enough history to roll back several releases.
- Pass artifacts between jobs explicitly (upload/download, registry) rather than rebuilding in later jobs.
- Record provenance: which commit, which pipeline run, who approved. Supply-chain frameworks (e.g. SLSA provenance, Sigstore/cosign signatures, SBOMs via Syft or similar) make this verifiable, which some customers and regulators require.

### Environments

- Keep the number of long-lived environments small (often: preview/ephemeral, staging, production). Each extra one costs money and drifts.
- Environment differences belong in configuration (variables, secrets, config files per env), not in code branches or different build commands.
- Staging is only predictive if it resembles production in the ways that matter: same deploy mechanism, same artifact, similar data shape, same infra code with different sizes.
- Use the CI system's environment protection features (required reviewers, branch restrictions, wait timers) for production.

## Caching

Caching is the single largest speed lever and the most common source of "works on CI sometimes" bugs.

**What to cache:** dependency downloads (package manager caches, not necessarily `node_modules` itself), compiler caches (ccache, sccache, Gradle build cache, Go build cache), container layer caches, test-tool binaries.

**Keying rules:**

- Key on the lockfile hash plus OS/architecture plus tool version: e.g. `deps-linux-x64-node20-<hash(lockfile)>`.
- Provide restore-key fallbacks (prefix match) so a lockfile change restores a near cache and only fetches the diff.
- Never key only on branch name; the cache never invalidates when dependencies change.
- Never cache outputs that embed secrets or environment-specific config.

**Container builds:** order the Dockerfile so dependency installation happens before copying source (see `containerization`), and use a remote/registry layer cache (e.g. BuildKit `--cache-from`/`--cache-to`) because ephemeral runners start cold.

**When a cache hurts:** if restoring the cache takes longer than recomputing (huge caches over slow storage), or cache corruption causes intermittent failures. Measure restore time vs. job time. Cap cache size and let it expire.

**Debugging suspected cache poisoning:** re-run with caching disabled. If it passes, the cache key is missing an input. Add the missing input to the key rather than disabling caching permanently.

## Parallelism

- **Job-level:** independent jobs (lint, unit, build) run in parallel. Draw the dependency graph; anything without a real data dependency should not wait.
- **Test sharding:** split a long suite across N runners. Shard by historical timing, not file count, or one shard ends up with all the slow tests. Most test runners or CI systems support timing-based splitting.
- **Matrix builds:** test across language versions, OSes, or databases only where you actually support them. A 4×3×2 matrix is 24 jobs per commit; restrict the full matrix to main/nightly and run a representative subset on PRs.
- **Diminishing returns:** each runner has startup overhead (provisioning, checkout, cache restore) of often 30s–2min. Past the point where shard runtime approaches startup overhead, more shards add cost without speed.
- **Fail fast selectively:** cancel sibling shards on first failure for PR feedback; let all shards finish on main to see the full failure set.
- **Cancel superseded runs:** when a new commit is pushed to a PR, cancel in-progress runs for the old commit (concurrency groups). Do not do this for deploy jobs mid-flight, which can leave an environment half-deployed.

## Making a slow pipeline fast

Work from data, not intuition:

1. Collect durations for each job over the last few dozen runs. Find the critical path: the longest chain of dependent jobs determines wall-clock time.
2. Look for time spent *not* doing work: queue wait for runners, image pulls, dependency installs, checkout of large repos (use shallow clones / partial clones), uploading huge artifacts.
3. Then attack the critical path in roughly this order of payoff:
   - Add or fix caching (dependencies, build cache, layer cache).
   - Remove unnecessary serialisation between jobs.
   - Shard the longest test job by timing.
   - Skip unaffected work in monorepos.
   - Move rarely-failing slow suites to post-merge or nightly, *only* if there's a clear owner who acts on failures there.
   - Bigger runners for CPU-bound jobs (often cheaper overall than many small ones because of startup overhead).
   - Fix individually slow tests (sleeps, real network calls, per-test database creation).
4. Re-measure. Report the before/after on the critical path, not on individual jobs.

## Flakiness

A flaky test fails sometimes without a code change. Even a 1% flake rate per test becomes dramatic across a large suite: with 200 tests each 0.5% flaky, a run passes cleanly only about 37% of the time.

**Recognise:** same commit passes on re-run; failures cluster around timing, ordering, shared state, network, or specific runners.

**Common causes:**

| Cause | Signature | Fix direction |
|---|---|---|
| Timing / sleeps | Fails under load, passes locally | Wait on conditions, not durations; use fake clocks |
| Order dependence | Fails when run with certain other tests or in parallel | Isolate state; randomise order locally to reproduce |
| Shared external state | Test DB rows, files, ports reused | Unique names per test/run; ephemeral containers |
| Real network calls | Failures correlate with third-party outages | Stub external services; contract tests separately |
| Resource exhaustion | Fails on smaller runners, OOM, disk full | Right-size runners; clean up; limit parallelism |
| Time zone / locale / date | Fails at midnight, month end, DST | Pin TZ in CI, inject clock |
| Non-deterministic data | Random seeds, unordered map iteration | Seed and log seeds; sort before asserting |
| Infra flake | Registry pulls, runner provisioning | Retries at the *infra* step with backoff, mirrors |

**Policy that works:**

- Track flake rate per test (many CI systems and test reporters can; otherwise parse JUnit XML across runs).
- Quarantine: move a known-flaky test to a non-blocking job *with an owner and a ticket*, not into oblivion. Quarantine without a deadline is deletion with extra steps.
- Automatic retry of *tests* hides real race conditions that also affect users. If you allow one retry, record retried-then-passed as a flake signal and review it. Retrying *infrastructure steps* (network fetches) is fine.
- Never "fix" flakiness by increasing timeouts without understanding the cause; it slows the pipeline and usually only lowers the failure rate.

## Secrets in CI

- **Prefer federated, short-lived credentials** (OIDC from the CI provider to the cloud's identity service, workload identity) over long-lived static keys stored as secrets. They expire on their own and can be scoped to repo, branch, and environment.
- Scope secrets to the environments and branches that need them. PRs from forks must not receive production or even staging secrets; most CI systems withhold secrets from fork PRs by default — do not override that without understanding the risk.
- Beware triggers that run untrusted PR code with elevated permissions (e.g. workflows triggered on PR target events that check out the PR head). That is a known credential-exfiltration pattern.
- Masking in logs is a backstop, not a control: secrets can leak via base64, partial echoes, error messages, or uploaded artifacts. Do not `echo` secrets, do not run shells with `set -x` around them, and do not bake them into images or artifacts.
- Pin third-party actions/orbs/plugins to a full commit SHA or verified version, not a moving tag; a compromised upstream tag runs in your pipeline with your secrets.
- Give the pipeline's default token the minimum permissions (read-only by default, elevated per job).
- Rotate any secret that may have appeared in a log, artifact, or fork run. Treat "might have leaked" as "leaked".
- Never paste a real secret into a pipeline file, commit, or chat to test something. Use the CI secret store or the project's secret manager.

## Deployment strategies

| Strategy | How it works | Rollback | Cost | Choose when |
|---|---|---|---|---|
| Recreate | Stop old, start new | Redeploy old | Lowest; has downtime | Dev envs, batch workers, apps that cannot run two versions at once |
| Rolling | Replace instances in batches | Roll forward/back in batches; minutes | No extra capacity (or small surge) | Default for stateless services behind a load balancer |
| Blue/green | Full new environment, switch traffic at once | Switch back instantly | 2× capacity during deploy | Need instant rollback; can afford duplicate capacity; schema compatible both ways |
| Canary | Route small % of traffic to new version, increase on healthy signals | Route back to 0% | Small extra capacity, needs traffic splitting + metrics | High traffic services where real-user signal matters; risky changes |
| Feature flags (dark launch) | Deploy code off, enable per user/cohort | Flip flag | Flag system, code complexity | Decouple deploy from release; see `release-management` |
| Shadow / mirror | Copy traffic to new version, discard responses | Not needed | Duplicate compute | Validating rewrites without user impact; read-only paths only |

**Rules that apply to all of them:**

- **Two versions run at once** in every strategy except recreate. Code, APIs, message formats, and database schemas must tolerate old and new side by side. Use expand/contract migrations (add column → deploy code that writes both → backfill → switch reads → remove old) — see `database-migrations`.
- **Health gates must reflect user experience.** A canary analysis on CPU usage alone will happily promote a version that returns errors fast. Gate on error rate, latency percentiles, and key business events, compared against the baseline version over the same window.
- **Canary needs enough traffic to be statistically meaningful.** At 1% of 100 requests/min you get 1 request/min; a 0.5% error rate regression is invisible for hours. Either use larger percentages, longer bake times, or synthetic traffic. Rough rule: you need hundreds to thousands of requests in the canary per step to detect error-rate shifts of a percentage point.
- **Automate rollback on failed gates** where possible; humans at 2 a.m. hesitate.
- **Database migrations are the usual reason rollback fails.** Run them as a separate, explicit step; make them backward compatible with the previous app version; never couple a destructive migration with the deploy that stops using the column.
- **Long-lived connections and queues** (WebSockets, consumers) need graceful draining: stop accepting new work, finish in-flight, then exit. Check termination grace periods.

### Mobile, desktop, libraries, and firmware

Not everything deploys to servers. For app-store releases, staged rollouts by percentage replace canaries, and rollback means shipping a new version (so a kill-switch flag matters more). For libraries, "deploy" is publishing to a registry; publishing is effectively irreversible (yanking does not remove copies), so gate publishing on tags and protected branches. For firmware/edge, add device-cohort rollouts and a tested recovery path.

## Safety rules for pipeline work

- **Do not trigger production deploys, rollbacks, or migrations without explicit confirmation** from the user, stating the artifact, environment, and expected effect.
- **Do not weaken protections to make something pass** (removing required checks, disabling branch protection, granting broad token permissions, skipping approval gates). If a protection blocks legitimate work, propose a scoped change and explain the trade-off.
- **Test pipeline changes on a branch first.** Many CI systems support running the changed workflow on the PR that changes it. For deploy-path changes, target a non-production environment first.
- **Beware cost blowups:** matrices that explode combinatorially, scheduled jobs running every minute, self-hosted autoscaling without caps, large runner sizes left on, artifact retention left unlimited. State expected cost impact when adding substantial compute.
- **Destructive steps** (environment teardown, cache purges, registry cleanup) must be scoped by explicit identifiers and never derived from unvalidated input like branch names that could be manipulated.

## Pitfalls and anti-patterns

- **Rebuilding per environment.** Staging tested artifact A, production runs artifact B. Fix: build once, promote by digest.
- **Logic in YAML.** Hundreds of lines of shell embedded in pipeline config, impossible to run locally. Fix: move to scripts in the repo; the pipeline calls them.
- **`latest` tags and unpinned tools.** Builds change without commits. Fix: pin versions, lockfiles, digests; update deliberately via a dependency bot.
- **Everything serial.** Jobs wait on each other without data dependencies. Fix: draw the DAG.
- **Retry-until-green culture.** Fix: track flakes, quarantine with owners, fix root causes.
- **Deploying on merge with no post-deploy verification.** Fix: smoke tests and health gates after each environment.
- **Manual production steps documented in a wiki.** They drift and get skipped under pressure. Fix: encode them in the pipeline as manual-approval jobs.
- **Secrets available to all branches.** Fix: environment-scoped secrets, OIDC with branch/environment conditions.
- **Giant monolithic "deploy everything" job.** One failing component blocks all others and rollback is all-or-nothing. Fix: per-service deploy jobs with independent artifacts where the architecture allows.
- **No rollback path tested.** Fix: periodically exercise rollback in staging; make it a single, documented pipeline action.
- **Ignoring queue time.** Jobs are fast but wait 10 minutes for a runner. Fix: capacity, autoscaling, or fewer, larger jobs.

## Verification

Before declaring a pipeline change done:

- [ ] The pipeline runs green on a branch with the change, and a deliberately broken commit (failing test, lint error) turns it red at the expected stage.
- [ ] Artifacts are tagged immutably and the same identifier is deployed to each environment (check the deploy logs or the running version endpoint).
- [ ] Cache hits on a second run with unchanged dependencies; a lockfile change produces a miss/partial restore and still passes.
- [ ] Secrets are not visible in logs or artifacts; fork PRs do not get privileged secrets; tokens have minimal permissions.
- [ ] Deploy jobs have health checks and a documented, tested rollback.
- [ ] Wall-clock time of the critical path is measured before and after any performance change.
- [ ] Path filters or affected-target logic do not skip required checks for changes that should trigger them (test with a change to a shared file).
- [ ] The local commands the pipeline calls also work for a developer locally.

When reporting, include: what changed, measured durations, any new cost, which protections exist on production, and anything not verified (e.g. "production deploy step not exercised; validated against staging only").

## Decision guidance: common forks

### Hosted vs. self-hosted runners

| Factor | Hosted runners | Self-hosted runners |
|---|---|---|
| Setup and maintenance | None | You patch, scale, and secure them |
| Startup | Cold every time; caches must be remote | Can keep warm caches on disk |
| Network access | Public internet only (unless private networking add-on) | Can reach private networks, on-prem systems |
| Hardware | Standard sizes, some GPU/ARM options | Anything, including GPUs, special devices |
| Security | Ephemeral, isolated per job by the provider | Persistent runners leak state between jobs unless made ephemeral |
| Cost | Per minute; expensive at very high volume | Fixed infra cost; cheaper at scale if well utilised |

Choose self-hosted when you need private network access, special hardware, or very high volume. If you do, make runners **ephemeral** (one job per runner instance, then destroy) and never attach persistent self-hosted runners to public repositories, where any fork PR can run code on your machine.

### Continuous delivery vs. continuous deployment

- **Continuous delivery:** every green main commit is *deployable*; a human (or schedule) decides when. Choose when releases need business coordination, compliance sign-off, or when monitoring/rollback is not yet good enough to trust automation.
- **Continuous deployment:** every green main commit goes to production automatically. Choose when tests are trustworthy, deploys are progressive with automated rollback, and feature flags separate deploy from release. It produces small, low-risk changes and the fastest feedback.

Moving from the first to the second is mostly about confidence infrastructure (health gates, rollback, flags), not about the pipeline YAML.

### One pipeline per repo vs. per service

In a monorepo with many deployable units, a single pipeline that builds and deploys everything is simple at first but couples unrelated services' failures and lead times. Prefer per-unit build/test/deploy jobs computed from what changed, sharing common templates. In polyrepo setups, prefer shared reusable pipeline templates over copy-paste so fixes propagate.

### Where to run integration tests

- Containers spun up in the CI job (service containers, compose, testcontainers libraries): hermetic, parallel-safe, fast to reset. Default choice.
- A shared long-lived test environment: realistic but becomes a contended, stateful bottleneck and a flake source. Use for post-deploy checks, not PR gating.
- Ephemeral per-PR environments: most realistic for full systems; cost and spin-up time scale with system size. Ensure automatic teardown and a TTL so abandoned PRs do not keep billing.

## Pipeline as evidence

Regulated teams often need to prove what was deployed, when, by whom, and that it passed required checks. A well-built pipeline provides this as a side effect:

- Required status checks and protected branches show every production change was reviewed and tested.
- Environment approvals record who authorised production deploys.
- Immutable artifact IDs plus deploy logs map running versions to commits.
- Retain pipeline logs and approvals for the period the organisation's policy requires; default retention on many CI systems is shorter than audit periods.

If the project has compliance requirements, ask what evidence is needed before redesigning the pipeline, so the redesign does not silently drop it.

## Worked example: a 45-minute PR pipeline

Situation: PR checks take ~45 minutes; developers stack PRs and merge without waiting.

Investigation over 30 runs shows: 6 min queue wait, 4 min dependency install (no cache), 3 min image build with no layer cache, a single 28-minute test job, and 4 minutes of E2E that depend on the full test job finishing although they only need the built image.

Changes, in order of payoff: dependency cache keyed on lockfile (−3.5 min), registry layer cache for image builds (−2 min), timing-based sharding of the test job into 4 shards (28 → ~8 min including startup), E2E made dependent only on the image build so it runs in parallel with unit tests, and runner autoscaling minimum raised during working hours to remove queue wait. Critical path drops to ~14 minutes. Two tests discovered failing only when sharded (shared fixture file) are fixed rather than pinned to one shard.

The reasoning to copy: measure, find the critical path, remove waiting before optimizing work, and treat newly exposed flakiness as a real bug.
