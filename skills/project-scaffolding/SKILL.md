---
name: project-scaffolding
description: >-
  Start a new software repository well: choose a language toolchain and
  package manager from the real constraints, lay out directories for the
  project type (library, CLI, service, web app, monorepo), and set up
  formatting, linting, type checking, tests, CI, environment configuration,
  scripts, README, licence and ignore files from day one — the minimum that
  pays off, not every tool available. Use when someone says "start a new
  project", "set up a repo", "bootstrap", "scaffold", "initialize", "create a
  starter", "what should my folder structure be", or needs to add missing
  foundations (tests, lint, CI, env handling) to a young repository.
metadata:
  category: app-generation
  related: full-stack-app-build, mvp-prototyping, dependency-management, ci-cd-pipelines, git-workflow, testing-strategy, code-documentation, technical-decision-making, cli-development, containerization, secure-coding
---

# Project Scaffolding

The first hour of a repository decides much of its next year. Choices made now — toolchain, layout, how config is loaded, whether tests and CI exist — are cheap to make and expensive to change later, because every later file is written on top of them. The goal is a repository that a newcomer can clone, set up with one documented command, run, test and change safely, carrying no tool or folder that does not earn its place.

## Scope

Covers: creating a new repository or bringing a very young one up to a sound baseline; choosing toolchains; directory layout; formatting, linting, type checking; test setup; CI; environment and configuration; scripts and task runners; README, licence, ignore files and editor config; first commit.

Does not cover: building the actual application (see `full-stack-app-build`, `mvp-prototyping`, or the platform skills), deep CI/CD design (`ci-cd-pipelines`), container and deployment setup beyond a pointer (`containerization`), dependency upgrade strategy (`dependency-management`), branching models (`git-workflow`).

## Core principles

1. **Minimal, not maximal.** Add a tool when it removes a real, present cost. Every tool is a dependency to update, a config file to understand, and a failure mode in CI. A starter with twelve configured tools and three lines of code is harder to work in than an empty folder. Why: complexity is paid for continuously by everyone who touches the repo; its benefits arrive only when the problem it solves appears.

2. **But some foundations are cheapest on day one.** Formatter, a test runner with one passing test, CI that runs them, an ignore file, and a README with setup steps cost minutes now and are painful to retrofit (reformatting a large codebase pollutes history; adding tests to untestable code requires refactoring). These are the exceptions to principle 1.

3. **Constraints choose the toolchain, not fashion.** The language, runtime and framework follow from: where it must run, who will maintain it, what the team already knows, what the ecosystem offers for the problem, and what the surrounding organisation standardises on. "What is newest" is a weak reason; "what the team can debug at 2 a.m." is a strong one.

4. **One obvious way to do each thing.** One command to install, one to run, one to test, one to lint/format. Documented in the README, identical locally and in CI. Why: divergence between local and CI is the most common reason "it works on my machine".

5. **Configuration comes from the environment; secrets never enter the repo.** Code reads settings from environment variables or config files that are not committed for secrets, with a committed example listing every key. Why: this is what lets the same build run in dev, test and production, and keeps credentials out of history (where they stay even after deletion).

6. **Reproducible from a clean clone.** Pin the language version, commit the lockfile, and make setup deterministic. A project that only works on the machine that created it is not scaffolded.

7. **Follow the ecosystem's conventions.** Each language has a conventional layout and tool set (e.g. `src/` and `pyproject.toml` in Python, `cmd/` and `internal/` in Go, `src/main` and `src/test` in JVM builds, Cargo's layout in Rust). Newcomers and tools expect them. Deviate only for a reason you can state.

## Process

### 1. Gather constraints before choosing anything

Ask or infer:

- **What is it?** Library, CLI, web service/API, web frontend, full-stack app, mobile/desktop app, data/ML project, infrastructure, docs site, monorepo of several.
- **Where does it run?** User machines (which OSes), servers/containers, serverless, browsers, devices.
- **Who maintains it?** Solo, a team (what languages do they know?), open-source contributors (lower barrier matters more).
- **Organisational standards?** Many companies mandate languages, CI systems, licences, code owners, security scanning. Look for an internal template or sibling repos and ask the user.
- **Lifespan?** A throwaway prototype deserves less ceremony than a service expected to live for years — but even prototypes get a README and a lockfile.
- **Distribution?** Published package (registry naming, versioning, licence), deployed service, internal tool.

If the user has already chosen the stack, do not relitigate it. Mention a concern once if there is a serious one.

### 2. Discover context

- Is there an existing repo (even partial)? Read what exists before adding anything.
- Are there sibling projects in the organisation? Match their tooling, CI and layout; consistency across repos is worth more than local optimisation.
- Is there an official generator for the chosen framework (e.g. the framework's own `create`/`new`/`init` command)? Prefer it over hand-rolling or third-party mega-templates: it tracks framework changes and matches docs. Then remove what you do not need.
- What versions are current and supported? Check the runtime's release schedule; do not start on a version near end-of-life.

### 3. Choose the toolchain

For each slot, pick one tool, preferring the ecosystem default unless a constraint says otherwise:

| Slot | Decide by | Notes |
|---|---|---|
| Runtime/language version | Supported/LTS status, deployment target, team | Pin it in a version file the tooling reads (e.g. `.nvmrc`/`.node-version`, `.python-version`, `rust-toolchain.toml`, `go.mod`'s go directive, `.tool-versions`) |
| Package/dependency manager | Ecosystem default, team familiarity, monorepo needs | Commit the lockfile for applications; libraries usually commit it too for reproducible dev, while declaring ranges for consumers |
| Formatter | The ecosystem's dominant formatter | Zero or near-zero config; the point is to end debate |
| Linter | Ecosystem default; start with recommended rules | Add rules when a real bug class appears, not preemptively |
| Type checker | Language-dependent; strongly consider for anything beyond a script | Start strict on new code — loosening is easy, tightening later is a migration |
| Test runner | Ecosystem default or framework's recommended | One trivial passing test proves the wiring |
| Task runner | Native scripts first (package scripts, Makefile, `justfile`, language task tools) | Only one entry point for commands |
| CI | Whatever hosts the repo or the org standard | Mirror local commands exactly |

Orientation to common ecosystem defaults (examples only — verify current practice, and defer to the team's or organisation's choices):

| Ecosystem | Manifest / lock | Typical formatter / linter | Typical test runner | Version pin |
|---|---|---|---|---|
| JavaScript/TypeScript | `package.json` + the package manager's lockfile | Prettier or Biome; ESLint or Biome | Vitest, Jest, the runtime's built-in runner | `.nvmrc` / `.node-version`, `engines` |
| Python | `pyproject.toml` + a lockfile from the chosen tool (uv, Poetry, pip-tools) | Ruff (format + lint) or Black + a linter; mypy/pyright for types | pytest | `.python-version`, `requires-python` |
| Go | `go.mod` + `go.sum` | `gofmt`; `go vet`, staticcheck or golangci-lint | `go test` | `go` directive / toolchain line |
| Rust | `Cargo.toml` + `Cargo.lock` | `rustfmt`; `clippy` | `cargo test` | `rust-toolchain.toml` |
| JVM (Java/Kotlin) | Gradle or Maven build files + wrapper | Spotless, ktlint, Checkstyle | JUnit | Toolchain config in the build file |
| .NET | `.csproj`/`.sln`, `global.json` | `dotnet format`, analyzers | xUnit, NUnit, MSTest | `global.json` SDK version |

Commit build-tool wrappers (e.g. Gradle wrapper) where the ecosystem uses them; they pin the build tool version the same way a lockfile pins dependencies.

### 4. Lay out the directories

Use the layout the ecosystem and project type expect. Patterns, described rather than prescribed:

- **Library**: source in one package directory (often under `src/`), tests alongside or in a parallel `tests/`, examples in `examples/`, public API surface explicit (an index/`__init__`/`lib` entry that re-exports). Keep it flat until it hurts.
- **CLI**: thin entry point that parses arguments and calls into a library-like core; the core is testable without spawning processes. See `cli-development`.
- **Service/API**: entry point; modules organised by feature/domain rather than by technical layer when the app will grow (a `billing/` folder containing its routes, logic and data access tends to age better than top-level `controllers/`, `models/`, `services/` folders — though many frameworks expect layer folders, and following the framework wins). Config loading in one place. Migrations in a dedicated folder.
- **Web frontend**: follow the framework's conventions (routing folders, public assets, components); colocate component tests and styles if the framework supports it.
- **Full-stack**: either one framework that spans both, or clearly separated `frontend`/`backend` (or `web`/`api`) packages with a shared types/contract package if needed.
- **Monorepo**: `apps/` (deployables) and `packages/` (shared libraries) is a common convention; adopt a workspace-aware package manager and a build tool that understands the dependency graph only when there are several packages. Do not start with a monorepo for one app "in case".
- **Data/ML**: separate raw data (usually not committed), notebooks for exploration, importable source for reusable code, configs for experiments, and outputs/artifacts outside version control. See `machine-learning-workflow`.

Heuristics: fewer, well-named top-level folders beat many; avoid generic dumping grounds (`utils/`, `helpers/`, `common/`) growing without bound — they are acceptable early but should be split by purpose as they grow; put generated output in ignored folders.

### 5. Set up quality tooling

- **Formatter** wired to run on save (editor config) and checked in CI. Run it once over everything now, before real code exists.
- **Linter** with the recommended preset. Make CI fail on errors; decide whether warnings fail (failing on warnings keeps the count at zero, but only if the rule set is curated).
- **Type checking** in CI if the language supports it.
- **Pre-commit hooks** are optional: they give fast feedback but can be bypassed, slow down commits, and need installation per clone. CI is the real gate. If you add hooks, keep them fast (format and lint changed files only).
- **Editor config** (`.editorconfig` and/or shared editor settings recommending extensions) helps contributors; keep it minimal and avoid forcing personal preferences.

### 6. Set up tests

- Install the runner, write one real test of something trivial but real (e.g. a pure function, or the app's health endpoint), and make `test` command run it.
- Decide where tests live (ecosystem convention) and how test data/fixtures are organised.
- If the project will need integration tests against a database or service, decide now how they get one (containers, an in-memory substitute, a test instance) and document it; see `testing-strategy`.
- Coverage reporting is useful once there is code worth measuring; coverage thresholds on day one mostly produce meaningless tests.

### 7. Set up CI

Minimum viable pipeline, triggered on pull requests and the default branch:

1. Check out, set up the pinned runtime, restore dependency cache keyed on the lockfile.
2. Install dependencies with the lockfile-respecting command (frozen/clean install).
3. Format check, lint, type check.
4. Run tests.
5. Build (if there is a build).

Keep it fast — under a few minutes at the start. Use the same commands the README documents. Add matrix builds (multiple OS/runtime versions) only if you support them. Add security scanning, dependency update automation and release workflows when the project needs them or the org requires them. See `ci-cd-pipelines` for depth.

Use least-privilege tokens for CI (read-only by default), and never print secrets in logs.

### 8. Configuration and environment

- Define every configuration key the app reads in one module that loads, validates and types them at startup, failing fast with a clear message if a required key is missing. Why: misconfiguration should crash at boot, not at the first request that needs the value.
- Commit an example env file (e.g. `.env.example`) listing every key with dummy values and a comment; ignore the real `.env`.
- Separate config by environment through values, not code branches (`if env == "production"` scattered in code is a smell; feature flags and config values are better).
- Defaults: safe for development, never silently insecure for production (e.g. no default secret key that works in prod).
- Document how to get real values (secret manager, team vault) without including them.

### 9. Write the README and project files

The README answers, in order: what this is (one or two sentences), how to set it up, how to run it, how to test it, how to configure it, and where to learn more. Plus status/maintenance if relevant. Keep it accurate rather than long; a wrong setup step is worse than a missing one.

Other files, each only if it applies:

- **Licence** — required for open source (choose with the user; the licence is a legal decision, not a scaffolding default) and often for internal compliance. Do not pick one silently.
- **`.gitignore`** — from the ecosystem's standard list plus the editor/OS files you know about, plus local env files, build output, caches and logs.
- **`.gitattributes`** — line ending normalisation; LFS patterns if large binaries are expected.
- **CONTRIBUTING, CODE_OF_CONDUCT, SECURITY** — for open-source or multi-team projects.
- **CODEOWNERS**, issue and PR templates — when the hosting platform and team size make them useful.
- **Changelog** — when releases are versioned for consumers.

### 10. Verify from a clean clone, then make the first commit

- Delete local artefacts (or clone fresh into a temp directory) and follow the README exactly: install, run, test, lint, build. Every step must work as written.
- Confirm CI passes on the first push.
- First commit contains the scaffold only, with a clear message. Do not mix scaffold with feature code; it makes history harder to read.
- Do not commit generated files, secrets, `.env`, `node_modules`-style dependency folders, or build output.

## Decision guidance

### Generator vs template vs by hand

| Option | Choose when | Watch for |
|---|---|---|
| Official framework generator | Using that framework | Generates demo code and optional extras — remove what you will not use |
| Organisation template | One exists | Ensure it is maintained; pull improvements back into it |
| Community starter/boilerplate | Rarely; when it matches needs precisely and is actively maintained | Unmaintained dependencies, opinions you inherit, bloat |
| By hand | Libraries, CLIs, small services, unusual stacks | Forgetting a foundation — use the checklist below |

### Monorepo vs multiple repos

Choose a **monorepo** when packages change together, share types or tooling, and are owned by one team or a coordinated set; atomic cross-package changes are the big win. Choose **separate repos** when components have independent release cycles, owners, access controls or languages, or when the org's tooling assumes one-repo-per-service. Starting with one app? Start with one repo; split or merge later is feasible if boundaries are clean.

### How much ceremony for a prototype

Keep: README with run steps, lockfile, ignore file, formatter, one test runner set up, env example.
Skip until needed: CI matrix, release automation, coverage thresholds, pre-commit hooks, containerisation, docs site.
Revisit when: someone other than the author starts contributing, or the prototype is about to be deployed for real users.

### Containers on day one?

Add a container definition early if the deployment target is containers, or if local setup needs services (database, queue) — a compose file that starts dependencies is often the single biggest onboarding speed-up. Skip it for libraries, CLIs and simple apps where the language toolchain alone suffices. See `containerization`.

### Strictness of lint/type settings

Start strict on a greenfield project; it costs nothing when there is no code. Starting loose and tightening later requires fixing every violation at once or living with exceptions. The exception is a prototype whose purpose is speed — even then, formatting stays on.

## Scripts and command naming

Whatever the task runner, expose a small, predictable command vocabulary. Common names (adapt to the ecosystem's habits):

| Command | Does | Notes |
|---|---|---|
| `setup` / `bootstrap` | Install dependencies, prepare local services, copy example env if missing | Idempotent: safe to run twice |
| `dev` / `start` | Run the app locally with reload | Make the distinction between dev and production start clear |
| `test` | Run the fast test suite | Separate `test:integration` or similar if slow suites exist |
| `lint` | Linters and type checks | Read-only |
| `format` | Rewrite files with the formatter | And a `format:check` (or `lint`) for CI |
| `build` | Produce the distributable or deployable | Output to an ignored folder |
| `clean` | Remove build output and caches | Never deletes source or user data |

Why: a newcomer or an automated agent can guess commands across many repos; CI files stay short because they call these commands rather than duplicating logic.

Keep scripts cross-platform if contributors use different OSes: avoid shell-specific syntax in package scripts, or provide scripts in a language the toolchain already has.

## Libraries: extra decisions

- **Package name**: check availability on the registry early, and check it is not confusingly close to an existing popular package.
- **Versioning**: semantic versioning is the common expectation; start at `0.x` while the API is unstable and say so.
- **Public API surface**: define it explicitly (exports map, `__all__`, visibility modifiers). Everything public becomes a compatibility promise.
- **Supported versions**: declare the minimum runtime/language version and test it in CI if you claim it.
- **Build outputs**: decide what ships (source, compiled output, type declarations, multiple module formats) and verify the published artefact by installing it into a scratch project — packaging mistakes are invisible from inside the repo.
- **Changelog and release process**: lightweight is fine, but decide it before the first release (see `release-management`).

## Bringing a young repository up to baseline

When a repo already exists but lacks foundations, add them in an order that keeps each step reviewable:

1. Pin runtime and commit a lockfile (if missing), so subsequent steps are reproducible.
2. Add the formatter and reformat everything in **one isolated commit** with no other changes; if the host supports it, add that commit to an ignore-revs file for blame.
3. Add the linter with recommended rules; fix or explicitly suppress existing violations in separate commits; consider a baseline mechanism if there are hundreds.
4. Add the test runner with one real test; then tests for whatever is most risky.
5. Add CI running the above.
6. Extract configuration to environment variables with an example file; rotate any secret that was ever committed (removing it from the current tree does not remove it from history).
7. Rewrite the README from a fresh-clone walkthrough.

Coordinate with collaborators before step 2: a mass reformat conflicts with every open branch.

## Scaffold checklist

Use this as a reminder of what to consider, not a list to install blindly. Each item is either done, deliberately skipped with a reason, or not applicable.

- [ ] Runtime/language version pinned in a file the tooling reads
- [ ] Package manager chosen; lockfile committed
- [ ] Directory layout follows ecosystem/framework convention
- [ ] Formatter configured and applied to all files
- [ ] Linter with a recommended preset
- [ ] Type checking (where the language supports it)
- [ ] Test runner with at least one real passing test
- [ ] Standard commands: setup, dev/run, test, lint, format, build
- [ ] CI on pull requests and default branch, using those commands
- [ ] Config module with validation; example env file; real env ignored
- [ ] `.gitignore` covering dependencies, build output, env files, caches, OS/editor files
- [ ] `.gitattributes` / LFS if needed
- [ ] `.editorconfig` or shared editor settings (minimal)
- [ ] README: what, setup, run, test, configure
- [ ] Licence decided with the user
- [ ] Contributing/security docs if open source or multi-team
- [ ] Local service dependencies (database, queue) startable with one command if any
- [ ] Generator demo code removed
- [ ] Fresh-clone verification done

## Worked example

Request: "Set up a new repo for a small internal HTTP service that reads from Postgres, maintained by a team that writes TypeScript."

Reasoning:

- Constraints: server-side, team knows TypeScript, internal, long-lived, needs a database. → TypeScript on the current LTS runtime, the team's usual package manager (check sibling repos), strict type checking.
- Layout: the chosen HTTP framework's convention if it has one; otherwise an entry point, a config module, feature folders, a migrations folder, tests colocated or in a `tests/` folder per team habit.
- Quality: the ecosystem's dominant formatter and linter with recommended presets; strict compiler settings.
- Tests: unit runner plus one integration test hitting a real Postgres started via a container in CI and a compose file locally.
- Config: one module validating `DATABASE_URL`, `PORT`, `LOG_LEVEL` at startup; `.env.example` committed.
- CI: install with frozen lockfile, format check, lint, type check, test (with a database service), build.
- Skip for now: release automation, multiple runtime versions, docs site, monorepo tooling.
- Deliverable check: fresh clone → documented setup command → `test` passes → service starts and responds on its health endpoint.

## Pitfalls

| Pitfall | Why it hurts | Instead |
|---|---|---|
| Kitchen-sink starter | Unused tools still break, update and confuse | Start minimal; add on demand |
| No lockfile / unpinned runtime | Builds differ by machine and day | Pin runtime; commit lockfile; frozen install in CI |
| CI runs different commands than local | Green locally, red in CI (or the reverse) | One set of scripts used by both |
| Secrets committed "temporarily" | They remain in history and leak | Example env file; secret manager; scan before first push |
| Formatting added months later | One giant diff, blame noise, merge conflicts | Formatter from the first commit |
| Layer-folder sprawl in large apps | Every feature change touches five folders | Feature/domain folders when the framework allows |
| Premature monorepo | Tooling overhead with one package | One repo, one app, until a second package exists |
| README drift | New contributors fail at step two | Verify README from a clean clone; update with every setup change |
| Licence chosen silently | Legal consequences the user did not choose | Ask; explain common options briefly |
| Copying config from another repo wholesale | Inherits irrelevant rules and stale versions | Start from the ecosystem defaults; bring over only what you understand |
| Generated demo code left in | Confuses readers; ships dead code | Remove generator samples after first run |

## Quality bar and verification

- [ ] A fresh clone, following only the README, installs, runs, tests, lints and builds successfully. Do this, don't assume it. If you cannot execute commands, give the user the exact sequence to run and state that it is unverified.
- [ ] CI is green on the first push and runs the same commands as local development.
- [ ] Runtime version pinned; lockfile committed; install in CI uses the lockfile strictly.
- [ ] Every configuration key appears in the example env file; the app fails fast on missing required keys.
- [ ] No secrets, env files, dependency folders, build outputs or OS/editor clutter are tracked (`git status` clean after a build; check the ignore file).
- [ ] Each tool in the repo has a reason you can state in a sentence.
- [ ] Layout follows the ecosystem or framework convention, or deviates for a written reason.
- [ ] Licence decided with the user (or deliberately omitted for private code, per org policy).

## Safety

- Before running generators or init commands in an existing directory, check that it is empty or that the command will not overwrite files; some generators silently replace config files.
- Never paste real credentials into example files, tests, CI configuration or README examples. Use placeholders.
- When configuring CI secrets, use the platform's secret store and the minimum scope needed; prefer short-lived credentials (OIDC-style federation) where available.
- Check new dependencies' provenance and maintenance before adding them; typosquatted packages target exactly the "install a few packages to get started" moment.
