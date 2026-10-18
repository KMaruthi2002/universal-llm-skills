---
name: dependency-management
description: >-
  Choose, add, pin, update, audit, and remove third-party dependencies safely:
  evaluating packages, semantic versioning and version ranges, lockfiles,
  reproducible installs, update strategy and automation, vulnerability and
  licence auditing, supply-chain risk (typosquatting, compromised maintainers,
  install scripts), vendoring, private registries, and monorepo workspaces.
  Use when adding a library, bumping versions, fixing a dependency conflict or
  broken install, responding to a security advisory, reviewing a lockfile
  diff, setting up dependency update bots, or deciding whether to build vs.
  depend.
metadata:
  category: development
  related: secure-coding, legacy-modernization, ci-cd-pipelines, project-scaffolding, release-management, security-audit, technical-decision-making
---

# Dependency Management

Every dependency is code you did not write, run with your program's privileges, maintained on someone else's schedule. Dependencies are enormously valuable and also the largest attack surface and maintenance burden most projects have. This skill is about getting the value while keeping the cost visible and bounded.

## Scope

Covers application and library dependencies managed by language package managers (e.g. npm/pnpm/yarn, pip/uv/Poetry, Cargo, Go modules, Maven/Gradle, Bundler, Composer, NuGet, SwiftPM), plus system packages and base images where they behave like dependencies.

Not covered here:

- Large framework or runtime upgrades in old systems — see `legacy-modernization`.
- Pipeline configuration for running audits — see `ci-cd-pipelines`.
- Container base images in depth — see `containerization`.
- Broader security review of an application — see `security-audit`.

## Core principles

### 1. Every dependency is a liability as well as an asset

Adding a package brings its transitive tree, its bugs, its vulnerabilities, its licence, its maintainers' security practices, and its future breaking changes. Why it matters: the cost is paid later, by whoever maintains the project, usually at an inconvenient time (a critical CVE on a Friday, an abandoned package blocking a runtime upgrade). Make the decision deliberately.

### 2. Builds must be reproducible

The same commit must install the same dependency versions everywhere: developer machines, CI, production. That is what lockfiles are for. Why: "works on my machine" bugs, surprise breakage from upstream releases, and supply-chain attacks via a newly published malicious version all exploit non-reproducible installs.

### 3. Update continuously in small steps

Small, frequent updates are cheap; large, rare updates are expensive and risky. Why: a one-minor-version bump has a short changelog and a small blast radius; a three-year jump combines dozens of breaking changes into one ambiguous failure. Staying current also means security patches apply cleanly when you need them urgently.

### 4. Trust is transitive, so verify at the boundary

You trust not just the package you chose but everything it depends on and everyone who can publish any of it. You cannot audit all of it, so control what you can: what gets in (review new dependencies), how it gets in (lockfiles with integrity hashes, trusted registries), and what it can do (no unnecessary install scripts, least privilege in CI).

### 5. Follow the ecosystem's conventions

Each ecosystem has established norms for ranges, lockfiles, and workspaces. Fighting them (e.g. committing a lockfile for a library where the ecosystem expects consumers to resolve, or hand-editing lockfiles) causes subtle problems. Learn the norm, then deviate only with a reason.

## Discovering context

Before adding or changing anything:

- Identify the package manager and its version actually in use: lockfile type, `packageManager` or toolchain fields, CI install commands, version files (`.nvmrc`, `.python-version`, `rust-toolchain`, `.tool-versions`). Using a different tool than the project uses (npm in a pnpm repo, pip in a uv/Poetry repo) rewrites or ignores the lockfile.
- Is this an **application** (deployed artifact) or a **library** (consumed by others)? Version-range strategy differs.
- Read existing policy: CONTRIBUTING notes, an approved-licence list, a renovate/dependabot config, a private registry config, a vendoring directory, an internal "approved packages" list.
- Check how the project pins: exact versions vs. ranges, and whether peer dependencies or constraint files are used.
- Note the supported runtime versions; a new dependency must support all of them.
- Look at how often dependencies are updated historically. A repo with years-stale dependencies needs a catch-up plan, not one more stale addition.

## Deciding whether to add a dependency

### Build vs. depend

| Factor | Favors depending | Favors writing it yourself |
|---|---|---|
| Problem complexity | Hard and well-specified (crypto, date/time zones, parsing standard formats, HTTP, database drivers) | A few dozen lines you fully understand |
| Correctness risk | Edge cases you would get wrong (Unicode, time zones, security) | Small, testable logic |
| Maintenance | Mature package, active maintainers | Package abandoned or one-person hobby project |
| Footprint | Small transitive tree | Pulls in dozens of packages for one function |
| Stability needs | Stable API, semver-respecting | Frequent breaking releases |
| Licence | Compatible | Incompatible or unclear |

Never hand-roll cryptography, password hashing, authentication protocols, or parsers for complex standard formats when a well-maintained library exists. Do prefer a few lines of your own code over a dependency for trivial helpers (padding a string, checking if a number is even): the supply-chain and maintenance cost of a micro-package exceeds its value.

### Evaluating a candidate package

Check, in roughly this order:

1. **Is it the real package?** Confirm the exact name from official docs or the project's repository. Typosquats (`reqeusts`, `colourama`), scope confusion, and lookalike names are common attack vectors. Never install a name suggested only by memory or by a model without verifying it exists and is the intended project — hallucinated package names are a known attack vector ("slopsquatting").
2. **Maintenance signals**: recent releases, responsiveness to issues and security reports, more than one maintainer, a public source repository matching the published package.
3. **Adoption**: download counts and dependents are weak but useful signals. A package with very few users has had few eyes on it.
4. **Transitive footprint**: how many packages does it bring? Inspect with the package manager's tree or "why" command after a trial install.
5. **Install-time behaviour**: does it run install/postinstall scripts or build native code? Those run with your user's privileges at install time.
6. **Licence**: compatible with your project and distribution model (see below).
7. **Known vulnerabilities**: check advisory databases for the version you would install.
8. **API quality and fit**: types available, documentation, stable API, no global side effects on import.
9. **Runtime and platform support**: matches your supported versions and targets.

If two candidates are close, prefer the one with fewer transitive dependencies and a longer track record.

## Semantic versioning and ranges

Semver: `MAJOR.MINOR.PATCH`. Major = breaking changes, minor = backward-compatible features, patch = backward-compatible fixes. Pre-1.0 (`0.y.z`) carries no stability promise; in many tools a caret range on `0.y` only allows patch updates for that reason.

Semver is a promise made by humans and broken regularly, usually unintentionally. Treat it as a hint about risk, not a guarantee. Some ecosystems do not use semver at all (calendar versioning, or "every release may break").

Common range syntaxes (exact semantics vary by tool — check its docs):

| Notation | Typical meaning |
|---|---|
| `1.4.2` / `==1.4.2` | Exactly this version |
| `^1.4.2` | `>=1.4.2 <2.0.0` (compatible with 1.x) |
| `~1.4.2` / `~=1.4.2` | Patch-level updates only, roughly `>=1.4.2 <1.5.0` (Python's `~=1.4` differs: `>=1.4 <2.0`) |
| `>=1.4` | Any newer version, including future majors — rarely what you want |
| `*` / unpinned | Anything — avoid |

Choosing ranges:

- **Applications**: ranges in the manifest matter less because the lockfile pins exact versions. Use the ecosystem's default compatible range and rely on the lockfile plus deliberate updates. Some teams pin exact versions in the manifest too for clarity; either is fine if consistent.
- **Libraries**: use the widest range you actually support and test, usually a compatible-major range (`^1.4`). Overly tight pins in a library cause unresolvable conflicts for consumers. Never pin a library's dependency to an exact version without strong reason.
- **Lower bounds** should be the oldest version you actually test or know works, not merely whatever was current when you added it. Some ecosystems let you test with minimal versions (e.g. a "lowest direct" resolution mode); use it for libraries.
- **Peer dependencies / plugins**: declare what the host must provide, with a range matching versions you support.

## Lockfiles

A lockfile records the exact resolved version (and usually an integrity hash and source) of every direct and transitive dependency.

Rules:

- **Commit the lockfile for applications and services.** Always.
- **For libraries**, follow ecosystem norms. Many communities now recommend committing it for reproducible development and CI, while consumers resolve their own; check the project's existing practice.
- **Install from the lockfile in CI and production** using the "frozen" or "clean install" mode (e.g. `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `uv sync --locked`, `poetry install` with a checked lock, `cargo build --locked`, Go's `go.sum` verification). This fails the build if the manifest and lockfile disagree instead of silently re-resolving.
- **Never hand-edit lockfiles.** Change the manifest or run the tool's update command, then commit the regenerated file.
- **Lockfile merge conflicts**: do not resolve by hand line-by-line. Take one side (usually the target branch's), re-apply your manifest changes, and regenerate with the tool. Then review the result.
- **Review lockfile diffs** in pull requests, at least at a glance: unexpected new packages, unexpected major bumps, changed registry URLs or integrity hashes for an unchanged version (a red flag), or packages resolving from an unexpected source.
- **One package manager per project.** Multiple lockfiles (e.g. both `package-lock.json` and `yarn.lock`) mean different people install different trees.

## Updating dependencies

### Strategy

- Keep a steady cadence: automated update PRs (e.g. Dependabot, Renovate, or ecosystem equivalents) grouped sensibly, merged frequently.
- **Group** low-risk updates (patch and minor of dev tooling, type definitions) to reduce noise. **Isolate** major updates and updates to critical runtime libraries into their own PRs so failures are attributable.
- Consider a short **cooldown** (e.g. wait a few days after a release before adopting it, except for security fixes). Many malicious or broken releases are detected and yanked within days.
- **Security updates jump the queue.** Assess severity and reachability (below), then patch.
- Do not let automation auto-merge major versions or anything without passing tests. Auto-merging patch updates of dev dependencies with a green test suite is a reasonable trade-off for many teams.

### Process for a meaningful update

1. Read the changelog and release notes between your version and the target, especially "breaking", "deprecated", and "security" entries. For majors, read the migration guide.
2. Update on a branch using the package manager's command, not by editing the lockfile.
3. Inspect the lockfile diff: what else moved transitively?
4. Run the full test suite, type checks, and build. Pay attention to new deprecation warnings.
5. For runtime-critical libraries (database drivers, HTTP clients, serialization, auth), test against a realistic environment, not only unit tests with mocks.
6. Ship it alone or in a small group so a regression can be traced and reverted.

### Large catch-ups

When a project is far behind:

- Upgrade the runtime/toolchain first if dependencies require it, or the reverse if the old runtime blocks new dependency versions — map the constraint graph first.
- Go one major version at a time for big frameworks.
- Fix deprecation warnings on the current version before bumping.
- Expect some packages to be abandoned; plan replacements behind a seam (see `legacy-modernization`).

### Resolving conflicts

Version conflicts happen when two dependencies need incompatible versions of a shared package.

- Use the tool's explanation command (`npm explain`, `pnpm why`, `pip show`/`pipdeptree`, `cargo tree -i`, `go mod why`, `gradle dependencyInsight`) to see who requires what.
- Prefer upgrading the dependent packages so their requirements overlap.
- Overrides/resolutions/constraints (forcing a transitive version) are a legitimate tool for security patches and conflict breaking, but each one is a bet that the package works with a version it did not ask for. Document why each override exists and remove it once upstream catches up.
- Some ecosystems allow multiple versions side by side (JavaScript); others require one (Python, most JVM setups). Duplicate versions bloat bundles and can break singletons (two copies of a framework, two React instances).

## Security auditing

### Vulnerability scanning

- Run the ecosystem's audit tool or a scanner (e.g. `npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, OSV-Scanner, or a hosted service) in CI and on a schedule — new advisories appear against code you have not changed.
- **Triage, do not just count.** For each finding, ask:
  - Is the vulnerable package in production code or only dev tooling?
  - Is the vulnerable function reachable from our code? (Some tools, like `govulncheck`, analyse reachability.)
  - Is the attack precondition possible in our deployment (e.g. a ReDoS in a parser only fed trusted input)?
  - Is a fixed version available? If not, is there a workaround or mitigation?
- Fix reachable, high-severity, production issues promptly. Record decisions to defer or ignore with a reason and an expiry date; silent ignore lists become permanent blind spots.
- Do not run "fix everything" commands that perform major upgrades automatically (e.g. a force-fix mode) without reviewing what they change.

### Supply-chain hygiene

- Install from trusted registries; configure scoped packages to resolve from your private registry to prevent **dependency confusion** (an attacker publishing a public package with your internal package's name and a higher version).
- Keep lockfile integrity hashes; enable hash checking where the tool supports it (e.g. pip `--require-hashes`).
- Disable or restrict install scripts where the ecosystem allows (e.g. an ignore-scripts setting with an explicit allowlist), especially in CI, and run installs without access to deployment secrets.
- Prefer packages with provenance or signing support where the ecosystem offers it (e.g. npm provenance, Sigstore-signed artifacts), and verify it if your tooling can.
- Generate a software bill of materials (SBOM, e.g. CycloneDX or SPDX) for deployed artifacts when compliance or incident response requires knowing exactly what shipped.
- Pin CI actions, base images, and build tools by digest or exact version too; they are dependencies with even more privilege.
- Be suspicious of: a new maintainer suddenly publishing to a long-stable package, a patch release with large unexpected changes, obfuscated code, network access at install time, a package that is new but claims to be a popular one.

### Never

- Never paste credentials into registry config files that get committed. Use environment variables or the CI secret store, and keep `.npmrc`/`pip.conf`-style files with tokens out of version control.
- Never disable TLS verification to "fix" an install.
- Never install packages as root/administrator on a developer machine to work around a permissions error.

### Worked example: responding to an advisory

Illustrative. A scanner reports a high-severity vulnerability in a transitive XML parser, pulled in by a reporting library.

1. **Confirm and locate**: the tree command shows two paths to the parser — the reporting library (production) and a test fixture generator (dev only).
2. **Assess reachability**: the advisory concerns external-entity expansion on untrusted input. The reporting library parses user-uploaded templates, so the production path is reachable. Priority: high.
3. **Find the fix**: the parser has a patched release in the same major. The reporting library's range allows it, so a targeted update of just the parser fixes it without touching anything else. (If the range did not allow it, the options would be: upgrade the reporting library, apply an override with a comment, or mitigate by disabling external entities in configuration.)
4. **Apply narrowly**: update only that package with the tool's targeted update command; confirm the lockfile diff touches only the parser.
5. **Verify**: tests pass; the scanner reports clean; a quick test with a malicious payload is rejected.
6. **Record**: the PR references the advisory, explains reachability, and notes that the dev-only path is fixed by the same update.

The pattern — locate, assess reachability, fix narrowly, verify, record — applies to every advisory.

## Runtimes, system packages, and tooling

Dependencies are not only libraries in the manifest.

- **Language runtime and package manager versions** are dependencies. Pin them (version files, toolchain files, a `packageManager` field, or the CI image), so everyone runs the same interpreter or compiler. A different minor runtime version can change resolution and behaviour.
- **System libraries** (OpenSSL, libc, image libraries, database client libraries) come from the OS or base image. Track them through the base image version and rebuild images regularly to pick up patches.
- **Build tools, linters, formatters, code generators** should be versioned in the project (as dev dependencies or pinned tool versions), not installed globally, so output is consistent across machines.
- **Generated clients and SDKs** derived from API schemas are dependencies on the schema version; record which version they were generated from.

## Ecosystem notes

Behaviour differs enough between ecosystems that these are worth checking each time:

| Concern | Things that vary |
|---|---|
| Duplicate versions | Allowed in JavaScript (nested `node_modules`); one version per package in Python environments and most JVM builds; Go and Rust pick per major version |
| Resolution | Highest-compatible (most) vs. minimal version selection (Go) — Go upgrades only when a module asks for a newer version |
| Lockfile name | e.g. `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `uv.lock`, `poetry.lock`, `Pipfile.lock`, `Cargo.lock`, `go.sum`, `Gemfile.lock`, `composer.lock`, `packages.lock.json` |
| Isolation | Python needs a virtual environment per project; installing into the system interpreter causes conflicts and on some OSes is blocked deliberately |
| Install scripts | Common in JavaScript and Python source builds; Rust build scripts (`build.rs`) and Go generate steps run code too |
| Yanking | Most registries let maintainers yank or deprecate a version; locked installs may still fetch yanked versions, which is why audit tools matter |

## Licences

- Know the project's distribution model: internal service, SaaS, distributed binary, open-source library. Obligations differ.
- Broad categories: permissive (MIT, BSD, Apache-2.0 — attribution, Apache adds patent terms); weak copyleft (LGPL, MPL — obligations on modified files or linking); strong copyleft (GPL — obligations when distributing derivative works); network copyleft (AGPL — obligations even when offered over a network); source-available or non-commercial licences (often incompatible with commercial use).
- Check transitive licences too; scanners can report them.
- When unclear, flag it to the user rather than guessing. Licence interpretation can be a legal question; do not present an opinion as legal advice.

## Vendoring

Vendoring means copying dependency source into your repository.

Choose vendoring when:

- Builds must work offline or in air-gapped environments.
- You need to patch a dependency and cannot wait for upstream (keep the patch small and documented; prefer the tool's patch mechanism if it has one).
- The ecosystem supports it natively and the team prefers it (e.g. Go's `vendor/`).

Costs: repository size, review noise, and updates that are easy to forget. If vendoring, record the upstream source and version for each vendored package, keep local modifications as separate, explained patches, and still run vulnerability scanning against the vendored versions.

Forking a dependency is vendoring with extra steps: you now maintain it. Try to upstream fixes and return to the published package.

## Monorepos and workspaces

Workspaces (e.g. npm/pnpm/yarn workspaces, Cargo workspaces, Go workspaces, uv workspaces, Gradle multi-project builds) manage several packages in one repository.

- **Single version policy vs. independent versions**: a single version of each third-party dependency across the repo avoids conflicts and duplicate bundles but forces everyone to upgrade together. Independent versions give flexibility at the cost of drift. Most monorepos benefit from a single policy with rare, documented exceptions. Follow what the repo already does.
- **Declare dependencies where they are used.** Each package lists its own direct dependencies even if hoisting would make them available. Relying on hoisted "phantom" dependencies breaks when the hoisting changes or the package is published.
- **Internal dependencies** use the workspace protocol or path references so local changes are picked up; make sure publishing converts them to real versions.
- **Shared tooling** (linters, test runners, type checker) usually belongs at the root; runtime dependencies belong in the package that needs them.
- **Affected-only builds**: in large monorepos, use the build tool's dependency graph to test only what a change affects; still run the full suite periodically.
- One lockfile at the root is normal for workspace-aware tools; do not create per-package lockfiles unless the tool requires it.

## Removing dependencies

Dependencies accumulate. Periodically:

- Find unused ones with an analysis tool (e.g. depcheck/knip, deptry, cargo-udeps, `go mod tidy`) and confirm manually — dynamic imports, plugins, and config-referenced packages produce false positives.
- Remove packages that duplicate functionality available in the standard library or in another dependency you already have.
- Move tools used only in development to dev dependencies so they do not ship to production.

## Pitfalls

- **Installing with the wrong tool** and rewriting the lockfile.
- **Not committing the lockfile** for an application, or committing a lockfile regenerated from scratch with every transitive version changed in an unrelated PR.
- **Upgrading everything at once** to fix one advisory, then being unable to tell which upgrade broke the build.
- **Range too wide** (`>=` or `*`), so a future major silently breaks a fresh install.
- **Library pinned too tight**, causing conflicts for every consumer.
- **Ignoring audit output** until it is so noisy nobody reads it. Triage and track instead.
- **Trusting a package name you have not verified**, especially one produced from memory or by an AI assistant.
- **Overrides that outlive their reason**, pinning a transitive dependency to an old version long after upstream fixed the conflict — sometimes re-introducing the vulnerability.
- **Dev dependency in production** (or the reverse: a runtime import of a package only listed as dev, which works locally and fails in the production install).
- **Phantom dependencies** in workspaces.
- **Treating semver as a guarantee** and skipping tests on minor bumps of critical libraries.

## Quality bar and verification

Before calling dependency work done:

- The project's own package manager was used; the manifest and lockfile are consistent (a frozen/locked install succeeds from a clean state).
- The lockfile diff contains only expected changes, and you have looked at it.
- Full tests, type checks, and build pass; for runtime-critical libraries, a realistic integration check passed.
- Audit/scan results were reviewed; any remaining findings are triaged with reasons.
- New dependencies have been checked for authenticity, maintenance, footprint, licence, and install scripts; the reason for adding each is recorded in the PR.
- Overrides and ignores carry a comment explaining why and when to revisit.
- No credentials were added to committed config.

When reporting, list what was added, updated, or removed (with versions), notable breaking changes handled, and any risks accepted.
