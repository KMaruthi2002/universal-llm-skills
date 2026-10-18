---
name: debugging
description: >-
  Systematically find and fix the root cause of bugs, crashes, wrong output,
  failing tests, hangs, and intermittent failures in any language or system:
  reproduce, minimize, form and test hypotheses, bisect, instrument, read error
  messages and stack traces, handle heisenbugs, fix the cause rather than the
  symptom, and lock the fix in with a regression test. Use when something is
  broken, an error or stack trace appears, a test fails, behaviour differs
  from expectations, or "it works on my machine" — before guessing at fixes.
  For organisational post-incident analysis use root-cause-analysis or
  postmortem; for live outages use incident-response.
metadata:
  category: development
  related: testing-strategy, test-driven-development, root-cause-analysis, observability, error-handling, concurrency-and-async, performance-optimization, explore-codebase, verify-before-done
---

# Debugging

Debugging is the process of closing the gap between what you believe the system does and what it actually does. Every bug is, at bottom, a false belief: about the input, the state, the order of events, the environment, a library's contract, or your own code. The work is to find which belief is false as cheaply as possible, then change the code (or the belief) so the two agree.

## Scope

Covers: diagnosing defects in code you can run or inspect — crashes, exceptions, wrong results, failing tests, hangs, leaks, intermittent failures, environment-specific behaviour — and fixing them durably.

Does not cover (see siblings):

- Live production outage coordination, comms, mitigation first → `incident-response`.
- Organisational "why did this happen and how do we prevent the class" → `root-cause-analysis`, `postmortem`.
- "It works but is slow" → `performance-optimization` (debugging techniques apply, but the method there is measurement-driven).
- Race conditions and deadlocks in depth → `concurrency-and-async` (this skill covers the debugging approach; that one covers the mechanics).
- Adding logging/metrics/tracing infrastructure → `observability`.

## Core principles

1. **Reproduce before you fix.** A fix you cannot demonstrate failing-then-passing is a guess. Without a reproduction you cannot tell whether your change helped, did nothing, or masked the symptom. If you truly cannot reproduce, your job becomes "gather enough evidence to reproduce," not "patch something plausible."

2. **Debugging is search; optimise the search.** You are narrowing a space (of commits, inputs, code paths, config values, time) until one cause remains. Prefer operations that cut the space in half (bisecting, toggling one variable) over operations that inspect one point at a time (reading code linearly and hoping). Ten binary cuts isolate one item in a thousand.

3. **Trust observations over beliefs.** The code you are reading may not be the code running (stale build, wrong branch, cached artifact, different config, a different service instance). The variable you "know" is set may not be. When an observation contradicts your model, the model is wrong — update it rather than explaining the observation away.

4. **One change at a time.** If you change three things and the bug disappears, you do not know which change mattered, whether the others introduced new bugs, or whether the bug is merely hidden. Revert experimental changes that didn't help.

5. **Fix the cause, not the symptom.** A `null` check where a `null` should never arrive moves the failure somewhere quieter. Ask "why was this value wrong?" repeatedly until you reach a point where the fix is a correction of intent, not a suppression of evidence.

6. **Read the error, all of it.** Error messages and stack traces are the system telling you where your belief diverged. Most "mysterious" bugs are explained by a line of the message that was skimmed past.

7. **Leave a tripwire.** A regression test (or at minimum an assertion) ensures the bug cannot silently return. A fixed bug without a test is a bug with a timer on it.

## Process

The steps are ordered, but loop freely. Small, obvious bugs may go from step 2 straight to step 6; nasty ones cycle through 3–5 many times.

### 1. Establish the facts

Before touching code, write down (mentally or in notes):

- **Expected behaviour** — precisely. "Should return the user's three most recent orders, newest first."
- **Actual behaviour** — precisely, with the exact error text, output, or observation. "Returns orders oldest first; only when the user has > 20 orders."
- **Conditions** — environment, version/commit, input, config, user, time, load, OS, locale, timezone.
- **History** — did this ever work? When did it start? What changed around then (deploys, dependency bumps, config, data, traffic, clocks)?

If you are working from a user report, ask for missing facts that would change the search: exact steps, exact message, environment, frequency. A vague report ("login is broken") debugged without clarification wastes far more time than one question.

"Did it ever work?" is the single most valuable question. If yes, you have a known-good state and can bisect. If no, you are debugging a design or an assumption, not a regression.

### 2. Reproduce

Get the failure to happen on demand, in the cheapest loop possible.

- Start with the reported path; then shrink it. A failing end-to-end flow → a failing API call → a failing function call → a failing unit test.
- Aim for a **feedback loop under ~10 seconds**. If each attempt takes five minutes (deploy, click through UI), invest in a faster harness first; it pays back after a few iterations.
- Capture the reproduction as a script or test immediately. You will run it dozens of times, and it becomes the regression test later.
- Record the **frequency** if it is not deterministic: "fails 3 of 20 runs." You need this baseline to know whether a change helped.

If you cannot reproduce:

| Situation | What to try |
|---|---|
| Only fails in one environment | Diff the environments: versions (runtime, OS, libraries, lockfile), config/env vars, feature flags, data, locale/timezone, CPU count, file system case sensitivity, network/proxy, permissions. |
| Only fails in CI | Run the CI container/image locally; check parallelism, test ordering, missing services, clean vs warm caches, resource limits, timezone (CI often runs UTC). |
| Only fails in production | Get logs, traces, crash dumps, request IDs; replicate the input data (sanitised); check for load- or time-dependent behaviour. Never debug by experimenting on production without the user's explicit agreement. |
| Intermittent | See "Heisenbugs and intermittent failures" below. |
| Only for one user/record | Get that record's data shape (sanitised). Bugs hiding in data — unexpected nulls, unicode, huge values, legacy formats — are very common. |

### 3. Minimise

Strip the reproduction down until removing anything else makes the bug vanish. Minimisation often reveals the cause by itself, because the last thing you could not remove *is* the cause or is adjacent to it.

- Remove input: halve the data file, drop fields, shorten strings.
- Remove code: stub out collaborators, delete unrelated setup, inline config.
- Remove environment: run without the framework, without the network, single-threaded.
- Keep a record of what you removed without effect; it rules out hypotheses.

Delta debugging (automated halving of an input until it is 1-minimal) is worth reaching for when inputs are large — many fuzzers and test tools include a minimiser/shrinker.

### 4. Form hypotheses and test them

A useful hypothesis is **specific and falsifiable**: "the cache returns the stale entry because the key omits the locale," not "something's wrong with caching."

For each hypothesis, design the cheapest experiment whose outcome would differ depending on whether it is true:

- **Predict before you run.** "If the key omits locale, then requesting with locale A then B returns A's value for B." If you cannot state a prediction, the hypothesis is too vague.
- **Prefer experiments that can kill the hypothesis.** Confirmation is weak; a failed prediction is decisive.
- **Rank hypotheses** by (likelihood × cheapness to test). Test cheap, plausible ones first, even if a less likely one is your favourite.

Generate hypotheses from:

- The error message and stack trace (see below).
- What changed recently (code, deps, config, data, infrastructure).
- The boundary between components — most bugs live at interfaces: serialisation, units, encodings, nullability, off-by-one ranges, time zones, async boundaries.
- Your list of "things that must be true for this to work"; check each.

Keep a short log of hypotheses tried and results. On long sessions this prevents re-testing the same idea and makes hand-off possible.

### 5. Locate with the right technique

Choose based on what you know:

| You have | Technique |
|---|---|
| A known-good commit and a known-bad commit | **Bisect the history.** `git bisect` (with `git bisect run <script>` for automation) or the equivalent in your VCS. ~log2(N) builds to find the commit. |
| A known-good input and a bad input | **Bisect the input.** Mix halves of good and bad until the minimal differing piece is found. |
| A long code path with a wrong value at the end | **Bisect the execution.** Check the value at the midpoint of the path; recurse into the half where it goes wrong. |
| A good and a bad environment | **Bisect the environment.** Swap one dimension at a time (dependency version, config file, env var). |
| Suspicion of a specific region | **Instrument** (logging, assertions) or use a **debugger** with breakpoints/watchpoints. |
| A crash with no useful trace | Enable core dumps / crash reporting, run under a sanitizer or memory checker, or add a top-level handler that logs full context. |
| Code you don't understand | Read it with a question in mind ("where is this field written?"), using search for writes/assignments rather than reading top to bottom. |

**Debugger vs print statements.** Both are legitimate.

- Debugger: best when you need to explore interactively, inspect complex state, or don't yet know what to look at. Conditional breakpoints and watchpoints ("break when `balance` becomes negative") are underused and very powerful.
- Logging/prints: best for timing-sensitive code, distributed systems, production-like environments, loops with thousands of iterations, or when you want a diffable trace of two runs (log good run, log bad run, diff).
- Either way, log **values and identities**, not just "got here": `order_id=42 status=PENDING items=3 thread=worker-2`.

**Assertions as probes.** Inserting `assert invariant(state)` at several points turns a late, confusing failure into an early, precise one. Fail-fast assertions near the source are often faster than tracing backwards from the symptom.

**Differential debugging.** If a similar thing works (another endpoint, another record, an older version, another platform), compare the two in detail. The difference is a short list of candidates.

### 6. Understand the cause fully before fixing

You have found the cause when you can explain the **entire causal chain** from trigger to symptom, and that explanation accounts for all the observations — including the odd ones (why only on Tuesdays, why only for >20 orders). If some observation is unexplained, you may have found *a* bug but not *the* bug.

Ask the "why" chain until it stops being productive:

> The page crashed → `user.address` was null → the address fetch returned 404 → the user was created through the legacy import → the import skips addresses for accounts with no country set.

Where to fix is a judgement call. Fixing at the deepest link (the import) prevents the class of problem; fixing at the shallowest (null check on the page) only hides one symptom. Often the right answer is both: fix the source, *and* make the consumer handle the case gracefully if the data can legitimately be absent. Decide which state is valid, and make the code say so.

### 7. Fix

- Write or keep the failing test first; watch it fail for the right reason (the actual bug, not a setup error).
- Make the smallest change that corrects the cause. Resist rewriting the area "while you're there" — it mixes a behaviour change with refactoring and makes review and rollback harder (see `refactoring`).
- Search for **siblings**: the same mistake is often copy-pasted. Grep for the pattern and check other call sites.
- Consider whether existing **bad data** created by the bug needs repair (a migration, a backfill, a one-off script) — fixing the code does not fix records already written. Treat data repairs as destructive operations: confirm with the user, back up, and run on a copy first.

### 8. Verify

- The regression test passes; it failed before the fix. (If you can, temporarily revert the fix and confirm the test fails again — this proves the test actually covers the bug.)
- The original reproduction (the user's real steps) no longer fails.
- For intermittent bugs: run enough iterations to be statistically convincing (see below).
- The full relevant test suite passes; you have not broken neighbours.
- Remove temporary instrumentation, debug flags, and commented-out experiments — or deliberately keep useful logging at an appropriate level.

### 9. Report

State the cause, the evidence, the fix, and the test. Mention anything you noticed but did not fix (siblings, data repair, a design weakness). A short causal chain ("X happened because Y, because Z") is more useful to reviewers than a narrative of everything you tried. See `report-results`.

## Reading errors and stack traces

- **Read the whole message, including the parts after the first line.** Many runtimes put the useful detail last ("caused by…", "during handling of the above exception, another exception occurred", "note:", "hint:").
- **Find the root exception.** In chained traces (Java "Caused by:", Python `__cause__`/`__context__`, .NET `InnerException`, Rust error chains, Go wrapped errors via `%w`), the deepest cause is usually the informative one; the outer layers are wrappers.
- **Find the first frame in your code.** Library frames tell you *what* failed; your frames tell you *why* it was called that way. Start from the topmost frame you own and inspect its arguments.
- **Note direction.** Python prints most recent call *last*; Java, JavaScript, Go, and .NET print most recent *first*. Misreading the order sends you to the wrong end of the trace.
- **Async traces are truncated.** Stack traces across `await`, callbacks, promises, or thread pools often lose the caller. Enable async stack traces where available (e.g. long stack traces in Node, `asyncio` debug mode, structured concurrency tools), or log a correlation ID at each hop.
- **Decode the error class.** `NullPointerException`/`TypeError: cannot read properties of undefined` → find where the value was supposed to be set. `KeyError`/`IndexError` → the data shape differs from your assumption; print the actual keys/length. `ConnectionRefused` vs `Timeout` vs `DNS failure` are three different problems. `Permission denied` → which user, which path, which policy.
- **Search the exact message** (minus your own identifiers) in the project's issue tracker, the dependency's issues, and the web. Someone has often hit it, especially for library and toolchain errors. Weight results by recency and version match.
- **Line numbers can lie** with transpiled, minified, macro-expanded, or optimised code. Make sure source maps / debug symbols match the running build.

## Heisenbugs and intermittent failures

A bug that changes or vanishes when observed almost always involves one of: timing/concurrency, uninitialised or shared state, ordering (test order, hash iteration order, filesystem order), resource limits, external dependencies, time/clock, or randomness.

Approach:

1. **Measure the rate.** Run the reproduction N times (e.g. 50–500) in a loop and count failures. Without a baseline you cannot evaluate fixes.
2. **Amplify.** Make the rare thing common: add load, reduce CPU (`taskset`/container limits), inject sleeps at suspected interleaving points, run tests in random or reversed order, run in parallel, shorten timeouts, fill the disk, use a slow network simulator.
3. **Control nondeterminism.** Fix random seeds (and log them on failure), freeze clocks, run single-threaded, pin test order. If the bug vanishes when you remove a source of nondeterminism, you have localised it.
4. **Observe without perturbing.** Prints and debuggers change timing. Prefer low-overhead logging to an in-memory ring buffer dumped on failure, recorded traces, or record-and-replay debuggers (e.g. `rr` on Linux) that make a failing run replayable deterministically.
5. **Check shared state.** Tests that pass alone but fail together → leaked global state, shared DB rows, singletons, environment variables, temp files, ports. Run the failing test alone, then with each preceding test, bisecting the test order.

**Statistics of "fixed".** If a bug fails with probability p per run, then n consecutive passes happen by luck with probability (1 − p)^n. To be ~95% confident a 1-in-10 bug is gone you need about 30 clean runs; for a 1-in-100 bug, about 300. Five green runs proves little for a rare flake.

## Common bug families and where to look

| Symptom | Frequent causes |
|---|---|
| Works locally, fails elsewhere | Different versions (unpinned deps), env vars, config, case-sensitive FS, path separators, line endings, locale/timezone, missing services, permissions, CPU architecture. |
| Off by one / boundary | Inclusive vs exclusive ranges, pagination, empty collections, first/last element, fence-post loops, date ranges across midnight or DST. |
| Wrong numbers | Integer overflow/division, float precision (never compare money as floats), unit mismatch (ms vs s, bytes vs KB), rounding mode, implicit type coercion. |
| Text garbled | Encoding mismatch (UTF-8 vs Latin-1), double-encoding, normalisation (NFC vs NFD), byte vs character length, unescaped input. |
| Time bugs | Timezone naive vs aware, DST transitions, server vs client clock, clock skew across machines, leap days, storing local time. |
| Stale data | Caches without invalidation, memoisation keyed on mutable objects, read replicas lag, browser/CDN caches, stale build artifacts. |
| Works first time, fails second | State not reset, idempotency missing, resource not released, connection pool exhausted, file left open/locked. |
| Hangs | Deadlock, waiting on a never-resolved future/promise, blocking call on an event loop, infinite retry, full queue/backpressure, DNS or network without timeout. Take a thread dump / stack dump of the hung process — it usually shows exactly where. |
| Memory grows | Unbounded caches/collections, listeners never removed, closures capturing large objects, retained references in globals. Compare heap snapshots over time. |
| Only under load | Races, pool exhaustion, timeouts, lock contention, rate limits, non-atomic read-modify-write. |
| Silent wrong behaviour | Swallowed exceptions, default values masking missing data, fallbacks that "work" (see `error-handling`). |

## Debugging by system type

The method is constant; the instruments differ.

**Distributed systems and services.**

- Follow one request end to end using a correlation/trace ID. If none exists, adding one is often the first fix.
- Line up timestamps across services, but remember clocks differ; prefer causal ordering (trace spans, message IDs) over wall-clock comparison.
- Ask "which hop first saw the wrong value?" and bisect along the path: log or inspect the payload at each boundary.
- Consider retries and duplicates: a message processed twice, a timeout that actually succeeded on the server, an at-least-once queue redelivering.
- Partial failure is the default: one replica on an old version, one shard unavailable, one region with different config.

**Memory problems.**

- Leaks: take heap snapshots at two points under the same workload and diff retained objects by type and count; follow the retention path (what holds the reference).
- Corruption, use-after-free, buffer overflows (native code): run under address/undefined-behaviour sanitizers or a memory checker; these turn random later crashes into immediate, precise reports.
- Out-of-memory crashes: check whether usage is growing (leak) or spiking (one huge allocation, unbounded result set, loading a whole file).

**Build, dependency, and toolchain failures.**

- Clean build first (clear caches, remove build directories, reinstall dependencies from the lockfile) to separate real errors from stale state.
- Read the *first* compiler error, not the last; later errors are often cascades.
- Compare resolved dependency trees between a working and failing machine; a transitive version difference is a common culprit (see `dependency-management`).
- "Module not found" / "symbol not found" usually means path, version, or architecture mismatch rather than missing code.

**Frontend and UI.**

- Use the browser's developer tools: console errors, network tab (actual request/response, status, headers, CORS), element inspector, and performance/render panels.
- Distinguish data bugs (the API returned the wrong thing) from rendering bugs (the right data displayed wrongly) by inspecting the network response first.
- Check across browsers, viewport sizes, and with extensions disabled; cached service workers and stale bundles are frequent false trails.

**Data pipelines and SQL.**

- Run the query or transformation on a tiny, hand-checkable subset.
- Count rows at each stage; a join that silently multiplies or drops rows is the most common pipeline bug.
- Check null semantics (`NULL = NULL` is not true in SQL), implicit type casts, and time zone conversion at each step.

**Tests that fail.**

- Read which assertion failed and the actual vs expected values before reading the code.
- Decide first whether the test or the code is wrong; a recently changed test with an incorrect expectation is as common as a real regression.
- If it fails only in the full suite, bisect the test order for a polluting predecessor.

## A worked example (illustrative)

Report: "Invoices are occasionally emailed twice."

1. *Facts.* Since last Tuesday; roughly 1 in 200 invoices; only on the worker service; no code changes to the email module, but the queue library was upgraded on Tuesday.
2. *Reproduce.* Locally, sending 1,000 invoices through the worker produces no duplicates. Under a CPU limit and 4 workers, 3 duplicates appear in 1,000. Baseline: ~0.3%.
3. *Hypotheses, ranked.* (a) The new queue library redelivers messages whose processing exceeds a visibility timeout. (b) Two workers claim the same job due to a race in the claim query. (c) The email provider retries on its side.
4. *Experiments.* Prediction for (a): duplicates correlate with jobs whose processing time exceeds the timeout. Logging job duration and delivery count shows every duplicate had delivery count 2 and duration > 30s. (b) predicts duplicates with delivery count 1 on two workers — none seen. (c) predicts duplicates with one send call in our logs — not the case.
5. *Cause.* The upgrade changed the default visibility timeout from 120s to 30s; PDF generation under load sometimes takes longer; the message is redelivered while the first worker is still working; the handler is not idempotent.
6. *Fix.* Two parts: set the timeout explicitly to fit the workload, *and* make the handler idempotent (record "invoice N emailed" before sending, skip if already recorded) because redelivery is a legitimate behaviour of at-least-once queues.
7. *Verify.* A test that delivers the same message twice asserts one email. The load reproduction runs 10,000 invoices with zero duplicates (at a 0.3% baseline, 10,000 clean runs is overwhelming evidence).
8. *Report.* Cause, evidence, both fixes, and a note that other handlers on the same queue should be checked for idempotency.

Note what the example does *not* do: it does not add a "dedupe" filter in the email-sending function without knowing why duplicates occur, and it does not stop at raising the timeout, which would leave the system fragile to the next slow job.

## Discovering context

Before and during debugging in an existing project:

- **Find the project's way to run things**: test commands, dev scripts, Makefile/task runner targets, CI config. Use them; they encode environment setup you would otherwise rediscover.
- **Check the build is current.** Rebuild/clear caches if any doubt; confirm the version you are running matches the source you are reading (print a build ID or add a deliberate log line and see it appear).
- **Look for existing debugging aids**: debug flags, verbose log levels, feature flags, admin endpoints, test fixtures, seed data, recorded fixtures.
- **Read recent history** of the files involved (`git log -p`, blame) — the bug may have arrived with a recent change whose intent explains it.
- **Check the issue tracker** for known reports; someone may already have a reproduction.
- **Follow the project's test conventions** when writing the regression test (framework, location, naming, fixture style).

If you cannot execute code, you can still debug: trace the logic by hand with the specific failing input, state your hypothesis and the experiment that would confirm it, and tell the user exactly what to run and what output would confirm or refute it.

## Pitfalls

- **Shotgun debugging** — changing things at random until the symptom stops. Even when it "works," you don't know why, and you have often introduced new problems. Recognise it when you can't state the hypothesis your current change tests.
- **Fixing the first suspicious thing.** Code is full of things that look wrong but are not the bug. Confirm by prediction and experiment before fixing.
- **Symptom patches**: catching and ignoring the exception, adding a null check, adding a retry, increasing a timeout, adding a sleep. Each can be legitimate, but only after you know *why* the condition occurs and decide it is expected.
- **Assuming the bug is in the library/compiler/OS.** Possible, but rare compared with your own code. Require a minimal reproduction that implicates it before concluding so — and then you have a good bug report to file.
- **Debugging the wrong build** — stale artifacts, wrong environment, cached container image, browser cache, a second instance answering requests. Verify you see your instrumentation.
- **Losing the reproduction.** Not saving the exact steps/input that triggered it, then being unable to trigger it again.
- **Not reverting failed experiments.** Leftover changes from disproven hypotheses confuse later reasoning and leak into the fix.
- **Tunnel vision.** If you have spent a long time on one hypothesis without progress, step back: re-read the facts, list assumptions you haven't verified, explain the problem out loud (rubber-duck), or take a break. The stuck feeling usually means a "known" fact is false.
- **Declaring victory on a flake** after a handful of green runs (see statistics above).
- **Fixing code but not data** that the bug already corrupted.
- **Debugging in production** by modifying live state without agreement. Prefer read-only observation; any write needs explicit user approval and a rollback plan.

## Verification checklist

Before declaring a bug fixed:

- [ ] You can state the causal chain from trigger to symptom, and it explains every observation.
- [ ] A test reproduces the bug, failed before the fix, and passes after (ideally confirmed by temporarily reverting).
- [ ] The original reported scenario no longer fails.
- [ ] Intermittent bugs: enough repeated runs to be convincing given the original failure rate.
- [ ] Related call sites with the same mistake were checked.
- [ ] The full relevant test suite passes.
- [ ] Temporary instrumentation and experiments are removed.
- [ ] Corrupted data, if any, is identified and a repair plan agreed with the user.
- [ ] The report says what was wrong, why, what changed, and what remains.

## When to escalate or stop

- If the bug is in a third-party dependency: produce a minimal reproduction, check for an upstream fix or newer version, apply a narrow, commented workaround, and suggest an upstream issue.
- If the root cause is a design flaw whose real fix is large: fix or mitigate the immediate symptom safely, document the deeper issue, and propose the larger change to the user rather than silently undertaking it.
- If you need access you don't have (production logs, a customer's data, hardware): say exactly what evidence you need and why.
