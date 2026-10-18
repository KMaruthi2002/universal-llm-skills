---
name: testing-strategy
description: >-
  Decide what to test, at which level, and how: unit, integration, contract,
  end-to-end, property-based, snapshot and exploratory testing; test pyramid
  versus testing trophy trade-offs; mocks, stubs, fakes and other test
  doubles; test data and fixtures; flaky tests; and using coverage as a signal
  rather than a goal. Use when designing or reviewing a test suite, adding
  tests to a feature, choosing between test types, fixing a slow or flaky
  suite, or asking "how should we test this?". For the red-green-refactor
  workflow itself use test-driven-development; for test plans for a release
  use qa-test-planning; for browser E2E mechanics use end-to-end-testing.
metadata:
  category: development
  related: test-driven-development, end-to-end-testing, qa-test-planning, debugging, refactoring, ci-cd-pipelines, api-design, code-review
---

# Testing Strategy

A test suite is an investment whose return is **confidence to change code quickly**. Every test costs time to write, time to run, and time to maintain; every test pays back by catching regressions, documenting intent, and enabling refactoring. A good strategy maximises confidence per unit of cost. That framing resolves most debates about "how many unit tests" or "should we mock this".

## Scope

Covers: choosing test levels and types, designing test doubles, organising test data, dealing with flakiness and slowness, interpreting coverage, and evolving the strategy for a codebase.

Neighbours:

- The test-first workflow (red/green/refactor) → `test-driven-development`.
- Release-level test plans, manual QA, exploratory sessions, acceptance criteria → `qa-test-planning`.
- Browser automation specifics → `end-to-end-testing`, `browser-automation`.
- Wiring tests into pipelines → `ci-cd-pipelines`.
- Evaluating LLM outputs → `llm-evaluation`.

## Core principles

1. **Test behaviour, not implementation.** A test should fail when the observable behaviour breaks and pass when the code is refactored without changing behaviour. Tests coupled to internals (private methods, call order on mocks, exact SQL strings) break on every refactor and so *discourage* the improvements tests are supposed to enable.

2. **Confidence comes from realism; speed comes from isolation.** The more a test resembles production (real database, real HTTP, real browser), the more a pass means. The more it isolates, the faster and more precise it is. Every level is a point on this trade-off; no single level is "correct."

3. **Each test should have one reason to fail.** When a test fails, you should know roughly what broke from its name and assertion alone. Tests that check fifteen things fail for fifteen reasons and diagnose none.

4. **A test you don't trust is worse than no test.** Flaky tests train people to ignore red builds, which hides real failures. Fix, quarantine, or delete flaky tests promptly.

5. **Tests are code.** They deserve clear names, no duplication of *intent* (some duplication of setup is fine for readability), and refactoring. But they should be simpler than the code under test — minimal logic, no loops and conditionals that could themselves be wrong.

6. **Test where the risk is.** Put effort proportional to (likelihood of defect × cost of defect). Money, security, data integrity, concurrency, and complex business rules deserve dense testing; trivial getters and framework glue do not.

## Test levels and types

| Type | What it exercises | Strengths | Costs | Best for |
|---|---|---|---|---|
| **Unit** | One function/class/module with collaborators real or faked | Milliseconds; precise failure location; easy edge cases | Can pass while integration is broken; over-mocked units test nothing | Pure logic, algorithms, parsing, validation, business rules, state machines |
| **Integration** | Your code with real infrastructure (DB, queue, filesystem, framework) or several modules together | Catches wiring, query, serialisation, config bugs | Slower (tens of ms to seconds); needs setup/teardown | Repositories/queries, HTTP handlers, message consumers, framework configuration |
| **Contract** | The agreement between a consumer and provider (API shape, message schema) | Catches breaking API changes without running both sides together | Requires discipline to keep contracts published and verified | Service boundaries owned by different teams; public APIs; event schemas |
| **End-to-end (E2E)** | A full user journey through deployed or near-deployed system | Highest realism; tests what users actually do | Slow, brittle, hard to debug, expensive to maintain | A handful of critical journeys (signup, checkout, login) |
| **Property-based** | Invariants checked over many generated inputs | Finds edge cases humans don't think of; shrinks failures to minimal cases | Requires identifying good properties; generators take effort | Parsers, serialisers (round-trip), math, data structures, anything with algebraic laws |
| **Snapshot / golden** | Output compared to a stored reference | Cheap way to detect any change in large outputs | Approval fatigue — people update snapshots without reading them | Stable rendered output, CLI output, generated code, compiler output |
| **Fuzz** | Random/mutated inputs looking for crashes | Finds security and robustness bugs | Needs time budget; triage of findings | Parsers, decoders, anything accepting untrusted input |
| **Mutation testing** | Tests themselves: are they sensitive to code changes? | Measures test effectiveness better than coverage | Slow; noisy on equivalent mutants | Auditing tests for critical modules |
| **Performance / load** | Latency, throughput, resource use | Catches regressions that functional tests can't | Noisy; needs stable environment | Hot paths with SLOs (see `performance-optimization`) |
| **Exploratory / manual** | Human investigation | Finds the unknown unknowns | Not repeatable; doesn't scale | New features, UX, unusual workflows (see `qa-test-planning`) |

### What "unit" means is disputed

Two schools:

- **Solitary (London/mockist):** a unit is a class; all collaborators are replaced with doubles. Precise, but tests become coupled to the collaboration design.
- **Sociable (Detroit/classicist):** a unit is a behaviour; real collaborators are used unless they are slow, nondeterministic, or external. Tests survive refactoring better.

A pragmatic default: **use real objects for in-process collaborators; replace only things that are slow, nondeterministic, external, or have side effects you can't undo** (network, clock, randomness, third-party APIs, email, payments). Switch to mocking collaborators when the collaboration itself *is* the behaviour (e.g. "publishes an event when the order ships").

## Shapes: pyramid, trophy, and others

- **Test pyramid** — many unit tests, fewer integration, very few E2E. Rationale: lower tests are faster and more precise. Fits codebases with substantial domain logic (financial engines, compilers, libraries).
- **Testing trophy** — static analysis at the base, a thin layer of unit tests, a *thick* layer of integration tests, a few E2E. Rationale: in many applications most bugs live in the integration between pieces (UI ↔ state ↔ API ↔ DB), and modern tooling makes integration tests fast enough. Fits CRUD-heavy apps, frontends, services that mostly orchestrate.
- **Honeycomb** (for microservices) — emphasises integration tests of each service against its real dependencies and contracts between services, with few isolated unit tests and few cross-service E2E tests.
- **Ice-cream cone** (anti-pattern) — mostly manual and E2E tests, few unit tests. Slow, flaky, expensive. Usually the result of adding tests only after bugs reach users.

Choose by asking **where do bugs in this system actually come from?** Look at the last 20 bug reports or incident causes. If they are logic errors in calculations, weight toward unit/property tests. If they are "the field name changed," "the query was wrong," "the config was missing," weight toward integration and contract tests. If they are "the button doesn't work in Safari," you need some browser-level tests.

Static analysis (type checkers, linters) is part of the strategy: a type system eliminates whole classes of tests you'd otherwise write (wrong argument types, missing fields). Don't write tests for what the compiler already guarantees.

## Process: designing tests for a change or a codebase

### 1. Discover what exists

- Find the test framework(s), runner commands, directory layout, naming conventions, fixture/factory helpers, and CI configuration. Match them — a new test in a different style is a maintenance burden.
- Note the current shape: roughly how many tests at each level, how long the suite takes, which tests are flaky (CI history, skip/quarantine markers, retry annotations).
- Identify shared test infrastructure: test databases, containers, fake servers, builders, custom assertions.
- If there are no tests, ask whether the user wants them introduced and at what level; for legacy code see `legacy-modernization` and characterization tests in `test-driven-development`.

### 2. Identify behaviours and risks

For the feature or module, list:

- The behaviours a user or caller relies on (happy paths).
- The edge cases: empty, one, many; boundaries (0, −1, max, max+1); null/missing; duplicates; unicode; very large inputs; concurrent access; time boundaries (midnight, DST, month ends, leap years).
- The failure modes: invalid input, dependency down, timeout, partial failure, permission denied.
- The invariants: things that must always hold (balances never negative; output sorted; round-trip parse(format(x)) == x).

Rank by risk. High-risk items get tests at more than one level.

### 3. Choose the lowest level that can catch each risk with confidence

For each behaviour/risk ask: what is the *cheapest* test that would fail if this broke in a realistic way?

| Risk | Typical level |
|---|---|
| Calculation/branching logic | Unit (+ property-based for invariants) |
| SQL query correctness, ORM mapping, migrations | Integration against a real instance of the same database engine (an in-memory substitute of a different engine hides dialect bugs) |
| HTTP routing, auth middleware, serialisation, status codes | Integration at the HTTP layer (in-process test client) |
| Contract with another team's service | Contract test, or schema validation in both CI pipelines |
| Third-party API behaviour | A few integration tests against sandbox (run separately, not blocking every commit) + fakes elsewhere |
| UI component logic | Component tests rendering the component and interacting as a user would |
| Critical cross-system journey | One E2E test per journey |
| Concurrency correctness | Stress tests, deterministic schedulers, or model checking (see `concurrency-and-async`) |
| Performance regression | Benchmark with thresholds in a controlled environment |

### 4. Write tests that read as specifications

- **Name tests by behaviour**: `rejects_withdrawal_exceeding_balance`, `returns empty list when user has no orders`. The name is the first thing read on failure.
- **Arrange–Act–Assert** (or Given–When–Then): setup, one action, assertions about outcome. Visual separation helps.
- **Assert on outcomes**, not intermediate steps: returned values, persisted state, emitted events, HTTP responses.
- **Use specific assertions** with good failure messages (`assertEqual(expected, actual)` beats `assertTrue(a == b)`; collection matchers beat manual loops).
- **Keep logic out of tests.** If a test computes the expected value with the same algorithm as the code, it verifies nothing. Use literal expected values, or a different, simpler oracle.
- **Make relevant data visible; hide irrelevant data.** Use builders/factories with defaults so a test only specifies the fields that matter to it: `make_order(status="SHIPPED")`.

### 5. Run, observe failure, and evaluate

A test that has never failed has not been shown to test anything. When adding tests to existing code, break the code deliberately (or invert an assertion) to confirm the test fails, then restore. This is the manual version of mutation testing and catches tests that assert on the wrong thing.

## Test doubles

| Double | What it is | Use when |
|---|---|---|
| **Dummy** | Placeholder passed but never used | Satisfying a signature |
| **Stub** | Returns canned answers | You need a collaborator to return specific data to drive a path |
| **Spy** | Records calls for later assertions | You need to verify an interaction occurred (an email was sent) |
| **Mock** | Pre-programmed with expectations; fails if not met | The interaction *is* the behaviour, and the protocol matters |
| **Fake** | Working lightweight implementation (in-memory repo, fake clock, local fake server) | You want realistic behaviour without the cost; reused across many tests |

Guidelines:

- **Prefer fakes for things you own; prefer stubs at external boundaries.** An in-memory repository that implements the same interface as the real one, verified by the same contract test suite, gives realism plus speed.
- **Don't mock what you don't own.** Mocking a third-party SDK's methods encodes your *assumption* about how it behaves; when the assumption is wrong, tests pass and production fails. Wrap the third party in a thin adapter you own, mock the adapter in unit tests, and integration-test the adapter against the real thing (or its sandbox).
- **Over-mocking smell:** a test whose setup is mostly `when(x).thenReturn(y)` lines, or that asserts on the exact sequence of internal calls. It is testing the implementation, will break on refactor, and may pass while the system is broken.
- **Inject nondeterminism.** Clock, random number generator, UUID generator, environment — pass them in (or use the language's standard seam) so tests can control them. `now()` buried in business logic is a top cause of flaky, date-dependent tests.
- **Verify fakes.** A fake that drifts from the real implementation produces false confidence. Run a shared contract test suite against both.

## Test data

- **Each test owns its data.** Create what it needs; don't depend on rows another test created or on a shared seeded database whose contents drift. Shared mutable fixtures are the leading cause of order-dependent failures.
- **Isolation strategies for databases**, from fastest to most robust: wrap each test in a transaction rolled back at the end (fast, but fails if code under test commits or uses multiple connections); truncate tables between tests; unique namespaces/tenants per test (works with parallelism); fresh database or container per test run.
- **Builders/factories over fixtures files.** Code-based factories with sensible defaults are easier to evolve than large static JSON/YAML fixtures that every test depends on implicitly.
- **Realistic but synthetic.** Use generated data shaped like production (lengths, unicode, nulls, distributions). Never copy real personal data into test fixtures; if production-derived data is needed, anonymise it irreversibly and confirm with the user.
- **Randomised data needs seeds.** If you use random values, log the seed on failure so the failure is reproducible.
- **Golden files**: keep them small and reviewable; make updating them an explicit command, and review diffs as carefully as code.

## Property-based testing

Write properties rather than examples: "for all inputs satisfying P, Q holds." The framework generates many inputs and, on failure, **shrinks** to a minimal counterexample. Examples of tools: Hypothesis (Python), fast-check (JS/TS), QuickCheck/Hedgehog (Haskell), proptest (Rust), jqwik (Java), gopter/rapid (Go).

Useful property patterns:

- **Round-trip**: `decode(encode(x)) == x`.
- **Invariant preservation**: after `sort`, output is ordered and is a permutation of input.
- **Oracle / reference model**: optimised implementation agrees with a slow obviously-correct one.
- **Idempotence**: `f(f(x)) == f(x)` (normalisation, formatting, dedup).
- **Commutativity/associativity** where the domain says so.
- **Metamorphic**: changing input in a known way changes output in a known way (adding a filter never increases result count).
- **Stateful/model-based**: random sequences of operations on the real system and a simple model must agree — excellent for caches, data structures, and APIs.

Keep generators realistic and bounded; constrain them with the same preconditions real callers have, or you will drown in failures for inputs that can't occur.

## Flaky tests

A flaky test passes and fails on the same code. Causes, roughly by frequency:

1. **Timing assumptions** — fixed `sleep`s, timeouts too tight for CI, waiting for UI without proper wait conditions. Fix: wait on conditions, not durations; use fake clocks.
2. **Shared state / order dependence** — globals, singletons, shared DB rows, env vars, temp files, ports. Fix: isolate; run tests in random order to expose it.
3. **Concurrency** — real races in code or test. Fix the code if it's a real bug — the flake is telling you something.
4. **External dependencies** — network, third-party sandboxes, DNS. Fix: fakes for the main suite; isolate real-dependency tests into a separate, non-blocking job.
5. **Nondeterministic inputs** — current time, random values, unordered collections (hash maps, sets, unordered query results without `ORDER BY`). Fix: control or sort.
6. **Resource exhaustion** — memory, file descriptors, disk, connection pools in long runs.
7. **Environment differences** — timezone, locale, CPU count, filesystem.

Policy that works:

- Track flakiness (CI history, rerun statistics). Fix the most frequent first.
- **Quarantine** a flaky test (move to a non-blocking job with a tracked issue) rather than leaving it red or adding blind retries. Automatic retries hide real intermittent bugs; if you use them, report retried tests so they are visible.
- Never "fix" a flake by increasing a sleep without understanding it.

See `debugging` for the method of reproducing intermittent failures.

## Coverage

Coverage tells you what code was *executed*, not what was *verified*. A test with no assertions can produce 100% line coverage.

- **Use coverage to find gaps, not to grade.** Low coverage in a critical module is a real signal; high coverage is not proof of quality.
- **Look at branch coverage**, not only lines; untested `else` branches and error paths hide bugs.
- **Read uncovered code** and ask "would a bug here matter?" Error handling and edge cases are often the uncovered, high-risk parts.
- **Avoid hard global targets that drive behaviour** (e.g. "must be 90%") — they incentivise low-value tests of trivial code. Ratchets ("coverage of changed lines must not decrease," or "new code ≥ X%") are gentler and more useful.
- **Mutation score** is a better measure of test strength for critical code: if mutating `>` to `>=` doesn't fail a test, the boundary is untested.

## Suite health: speed and maintenance

- **Fast feedback tiers.** Keep a tier that runs in seconds to low minutes on every change (unit + fast integration). Slower tiers (full E2E, real third parties, load) run on merge, nightly, or pre-release. A suite developers won't run locally gets bypassed.
- **Parallelise** — requires test isolation; it's another reason to avoid shared state.
- **Profile the suite.** Usually a small number of tests account for most runtime (heavy setup, real sleeps, unnecessary E2E). Fix those first.
- **Delete tests that no longer earn their keep**: duplicates of other tests at a higher level, tests of removed features, tests that only verify a mock returns what it was told to.
- **When a bug escapes, ask which test should have caught it** and at what level. Add that test; if the right level was missing entirely, that's a strategy gap.

## Contract testing in practice

When two independently deployed components talk (frontend ↔ backend, service ↔ service, producer ↔ event consumer), E2E tests of every combination do not scale. Contracts do.

- **Consumer-driven contracts** (e.g. Pact-style): each consumer records the requests it makes and the response fields it relies on; the provider's CI replays these against the real provider. The provider learns exactly which fields are in use and can't remove one without a failing build.
- **Schema-first contracts**: an OpenAPI, protobuf, GraphQL, JSON Schema, or Avro definition is the source of truth; both sides validate against it in CI, and a compatibility checker flags breaking changes (removed fields, narrowed types, new required inputs).
- **What contracts don't cover**: semantics. A contract says `total` is a number; it doesn't say it includes tax. Pair contracts with a small number of integration tests of meaning for the most important flows.
- **Versioning**: contract tests are most valuable when combined with an explicit compatibility policy (see `api-design`): additive changes allowed, removals require deprecation.

## Testing specific kinds of code

**Asynchronous and concurrent code.** Await completion explicitly rather than sleeping; expose hooks or use fake schedulers/event loops that let the test advance time deterministically. For races, combine targeted stress tests (many iterations, many threads) with tools that systematically explore interleavings where available. See `concurrency-and-async`.

**Time-dependent code.** Inject a clock. Test the boundaries explicitly: end of month, leap day, DST transitions in a non-UTC zone, year boundaries, expiry exactly at the threshold.

**Code calling external APIs.** Three layers: unit tests with your adapter faked; adapter integration tests against recorded responses (record/replay tools) or the provider's sandbox; a small, separately scheduled smoke test against the real sandbox to detect provider drift. Recorded responses go stale — re-record periodically and scrub secrets and personal data from recordings.

**User interfaces.** Test components the way users interact with them — by visible text, roles, and labels rather than CSS classes or internal component state. This also exercises accessibility semantics. Reserve full-browser tests for flows that depend on real browser behaviour (routing, storage, cross-page navigation, payment iframes). Visual regression tools are useful for design systems but need stable rendering environments to avoid noise.

**Data pipelines and analytics.** Test transformations on small hand-built inputs with known outputs; add data quality checks (row counts, uniqueness, null rates, referential integrity) that run on real data in the pipeline itself, since many pipeline defects come from the data rather than the code (see `data-cleaning-and-validation`, `etl-pipelines`).

**Infrastructure and configuration.** Validate config files against schemas, lint infrastructure definitions, run plan/diff checks in CI, and smoke-test deployed environments (health checks, one real request). A missing environment variable is a production bug no unit test will catch.

**Machine learning and LLM features.** Deterministic code around the model is tested normally; model behaviour is evaluated statistically on datasets with thresholds rather than exact assertions (see `llm-evaluation`, `machine-learning-workflow`).

**Security-relevant code.** Authorisation needs negative tests for every role boundary ("user A cannot read user B's record"), not just positive ones. Input handling benefits from fuzzing. See `secure-coding`.

## A worked example (illustrative)

Feature: a discount engine that applies coupon rules to a cart, persisted through a repository and exposed by an HTTP endpoint.

- *Risks.* Wrong totals (money — high cost); rule combinations (stacking, exclusions, expiry); rounding; the endpoint returning the wrong status for invalid coupons; the repository query loading expired coupons.
- *Unit tests* for the rule engine with real in-process objects: one test per rule, boundary tests (expiry exactly now, minimum spend exactly met), combination tests for stacking and exclusions. Money uses an integer or decimal type, with explicit rounding tests.
- *Property-based tests*: discount never exceeds cart total; total never negative; applying the same coupon set in any order gives the same total (if the business says order-independence holds — check first).
- *Integration tests* for the repository against a real instance of the production database engine: expired and future coupons are excluded; the query uses the coupon code index (optional, but cheap to check).
- *HTTP-level integration tests*: valid coupon → 200 with the new total; unknown coupon → the project's error convention; malformed body → validation error; unauthenticated → 401.
- *E2E*: none new — the existing checkout journey test gains one step applying a coupon.
- *Not tested*: the framework's JSON serialiser, getters on the coupon model.

The result is dense testing where the money is, a thin layer where wiring could break, and no new slow tests.

## Decision guide: common forks

- **Mock the database or use a real one?** Use a real instance of the same engine for repository/query tests (containers make this cheap). Mock/fake the repository *interface* for business-logic unit tests above it.
- **Snapshot or explicit assertions?** Explicit assertions for behaviour you care about; snapshots only for large, stable outputs where "any change" is the signal, and only if diffs will actually be reviewed.
- **E2E or integration for a feature?** If the risk is in cross-system wiring that no lower test can see (real browser, real deploy config, real auth provider), E2E. Otherwise integration — E2E for every feature becomes the ice-cream cone.
- **Test private methods?** No — test through the public interface. If a private method is complex enough to need direct tests, it probably wants to be its own unit with its own public interface.
- **One assert per test?** One *concept* per test. Several assertions describing one outcome (status code and body) are fine.
- **Test generated code / framework code?** No; test your configuration of it and your use of it.

## Questions worth asking the user

When the right strategy depends on facts you can't see in the code, ask briefly:

- Which failures would be most costly — money, data loss, security, a key customer flow?
- How long may the pre-merge suite take before people start bypassing it?
- Are there environments available for integration tests (containers, sandboxes, test accounts)?
- Is this code long-lived or a prototype? (A throwaway spike needs far fewer tests; see `mvp-prototyping`.)
- Are there compliance requirements for test evidence or data handling?

## Evolving the strategy of an existing suite

When asked to improve a test suite rather than add one test:

1. **Measure first**: total runtime and its distribution, flake rate per test, number of tests per level, escaped defects over recent months and which level should have caught them.
2. **Fix trust before coverage**: eliminate or quarantine flaky tests, so red means red.
3. **Fix speed next**: the slowest 10% of tests usually dominate runtime; move logic-heavy E2E tests down to integration or unit, replace sleeps with condition waits, share expensive immutable setup.
4. **Fill risk gaps last**: add tests where escaped defects cluster.
5. **Change incrementally** and agree the direction with the user; rewriting a whole suite is rarely justified and pauses delivery.

## Pitfalls

- Tests that mirror the implementation line by line (break on every refactor, catch nothing new).
- Asserting on log messages, exact error strings, or internal call order when behaviour would do.
- Huge shared fixtures that every test silently depends on.
- Writing E2E tests for logic that could be unit-tested — slow, flaky, and poor at pinpointing failures.
- Mocking a third-party library directly; tests encode wrong assumptions.
- Ignoring the test's failure message quality — a red build that says `expected true but was false` costs minutes per failure.
- Tests that pass when the feature is deleted (assertions on mocks only).
- Retries hiding real intermittent bugs.
- Chasing coverage numbers with trivial tests while error paths stay untested.
- Using real personal data in tests or committing secrets for test environments.
- Leaving disabled/skipped tests indefinitely — they rot and nobody knows if they still matter. Each skip needs a reason and a tracking issue.

## Verification

Before considering a testing change done:

- [ ] Each new test fails when the behaviour it covers is broken (verified by deliberately breaking it at least once).
- [ ] Test names describe behaviour; failure messages point to the problem.
- [ ] Tests follow the project's existing framework, layout, and helper conventions.
- [ ] Tests pass in isolation, in random order, and in parallel (if the suite runs that way).
- [ ] No real network, real clock, or randomness without control in the fast tier.
- [ ] High-risk behaviours and failure paths are covered, not just happy paths.
- [ ] Suite runtime is still acceptable; slow tests are in the appropriate tier.
- [ ] No flaky test was "fixed" by retry or sleep alone.
- [ ] No real personal data or secrets in fixtures.
