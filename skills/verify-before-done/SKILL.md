---
name: verify-before-done
description: >-
  Prove that work actually does what was asked before calling it finished:
  run the build, tests, and the real thing; inspect actual output instead of
  assuming it; check edge cases and regressions; compare against the
  acceptance criteria; and report honestly what was verified, what was only
  inferred, and what was not checked. Use before saying "done", "fixed",
  "working", or "complete" on any code, data, document, configuration, or
  analysis — and whenever you are tempted to claim success without having
  observed it. Use when you are about to report a task as finished, when a
  fix "should" work, or when only some checks could be run. Not for
  designing a test suite (see testing-strategy) or formal
  release sign-off (see release-readiness).
metadata:
  category: meta
  related: testing-strategy, report-results, debugging, code-review, release-readiness, qa-test-planning, fact-checking, end-to-end-testing
---

# Verify Before Done

"Done" is a claim about the world. It should be backed by evidence you have observed, not by the fact that you wrote code that looks right. The gap between "I made the change" and "the change works" is where most embarrassing failures live: the test that never ran, the file that was not saved, the build that broke on an import, the fix that addressed a different bug than the one reported.

## Scope

Covers the final checks on any piece of work — code, configuration, data processing, documents, analyses — and the honesty discipline of reporting what those checks did and did not cover.

Does not cover:

- Deciding what tests a system should have long-term — see `testing-strategy`.
- Multi-stakeholder go/no-go for a release — see `release-readiness`.
- Writing the hand-off message itself — see `report-results` (this skill decides *what* is true to report).
- Checking factual claims in prose — see `fact-checking` (this skill points to it for written work).

## Core principles

### 1. Observe, don't infer

Reading your own code and concluding it works is inference. Running it and seeing the right output is observation. Inference is necessary when you cannot run things, but it is weaker evidence and must be reported as such. Whenever observation is possible at reasonable cost, observe.

### 2. Verify the thing that was asked, not a proxy

Tests passing is a proxy for "the feature works". A clean build is a proxy for "the app runs". Proxies are useful but can diverge: tests may not cover the changed path; the build may succeed while the page renders blank. Close the loop on the actual request — reproduce the user's scenario and confirm the outcome changed.

### 3. A check that cannot fail proves nothing

If a test would pass whether or not your change is present, it is not verifying your change. If a command's output is never read, it is not a check. For a bug fix, the strongest evidence is: the reproduction fails before the fix and passes after it. For a new feature, confirm a test fails when the feature is broken (temporarily revert or break it if cheap).

### 4. Look at the actual output

Read the test output, not just the exit code. Open the generated file. Look at the rendered page. Query the table you wrote to. Commands can "succeed" while doing nothing (zero tests collected, empty file written, wrong environment targeted). Many tools exit 0 on warnings that matter.

### 5. Regressions count

A change that fixes one thing and breaks another is not done. Run the broader checks — the full or relevant test suite, type checks, lint, build — not only the test for your change. Compare against the baseline you captured before starting (see `explore-codebase`) so you know which failures are yours.

### 6. Honesty over the appearance of completion

The user is better served by "done, except X which I could not verify because Y" than by an unqualified "done" that later turns out false. Never describe something as tested if it was not run. Never suppress a failure, weaken an assertion, or skip a test to get to green without saying so explicitly.

## The process

### Step 1: Restate what "done" means

Pull up the acceptance criteria (stated, agreed, or assumed — see `clarify-requirements`). If none exist, write the obvious ones now: what the user should be able to do or see, under what conditions. Verification without criteria degenerates into "it seems fine".

### Step 2: Check the basics mechanically

These catch the most common failures for the least effort. For code:

- All intended files were actually saved and changed (look at the diff — e.g. `git diff`, `git status`). Check for unintended changes too: stray debug prints, commented-out code, accidental formatting churn, temporary files.
- It builds or compiles; the type checker passes, if the project uses one.
- Linters and formatters the project enforces pass.
- The relevant tests pass, and test output shows the expected tests actually ran (count is not zero; your new tests are listed).

For non-code work, the equivalents: the file exists in the expected location and format, opens without errors, has the expected structure, and contains no placeholder text.

### Step 3: Verify the specific change

Choose checks appropriate to the kind of work:

| Work type | Strongest practical evidence |
|---|---|
| Bug fix | Reproduce the original failure, apply the fix, show the same reproduction now succeeds; add a regression test that fails without the fix |
| New feature | Exercise it as a user would (call the endpoint, run the command, click through the UI) and check each acceptance criterion; automated tests for the core paths |
| Refactor | Behavior unchanged: same test results before and after; spot-check outputs on representative inputs |
| Performance change | Measure before and after under the same conditions; report numbers, not adjectives |
| Configuration / infrastructure | Apply in a safe environment or dry-run/plan mode; confirm the resulting state, not just that the command returned |
| Data transformation | Row counts in vs. out; spot-check specific records end to end; check nulls, duplicates, and type coercions; validate against known totals |
| Analysis | Re-derive key numbers independently; sanity-check magnitudes; confirm filters and joins did what you think |
| Document / writing | Reread against the brief; check facts, links, numbers, names; render it in its target format |
| UI | Look at it rendered — at the sizes and states that matter (empty, loading, error, long content) |

### Step 4: Probe edge cases

Pick the edge cases most likely to break *this* change. Do not test everything; test where the risk is. Common high-yield cases:

- **Empty / missing** — empty list, empty string, null, missing file, no results, first run with no state.
- **Boundaries** — zero, one, exactly at a limit, one past it; first and last element; page boundaries.
- **Size** — large inputs, long strings, many items; check time and memory, not only correctness.
- **Malformed input** — wrong types, bad encoding, unexpected characters (quotes, commas, newlines, emoji, right-to-left text).
- **Failure of dependencies** — network down, timeout, permission denied, disk full, service returning an error.
- **Concurrency / repetition** — running twice (idempotency), running in parallel, retries.
- **Permissions** — a user who should not be able to do this, cannot.
- **Environment differences** — time zones, locales, operating systems, configuration absent vs. present.

### Step 5: Check for regressions

- Run the broader suite, or at least the tests for every module you touched and its direct dependents.
- Compare results to the baseline. New failures are yours until proven otherwise. Pre-existing failures should be noted, not silently ignored or "fixed" by deleting them.
- For shared code, check a few callers still behave correctly.
- If there is no suite, exercise the main paths of the surrounding feature by hand.

### Step 6: Review the diff as a reviewer would

Read your complete change top to bottom as if someone else wrote it. Look for: leftover debugging, hard-coded values that should be configurable, secrets, TODOs you meant to resolve, error paths that swallow failures, missing documentation updates, inconsistencies with surrounding conventions. (`code-review` has a fuller checklist.)

### Step 7: Classify what you verified

Before reporting, sort every claim you are about to make:

- **Verified** — observed directly: ran it, saw output, measured it.
- **Inferred** — reasoned from code or documentation but not observed (e.g. "this also fixes the mobile view, since it uses the same component" — unless you looked).
- **Not verified** — could not or did not check, with the reason (no access to the environment, requires credentials, requires production data, too slow to run here).

Report in those terms (see `report-results`). It is fine to leave things unverified; it is not fine to blur the categories.

## When you cannot run things

Some environments do not allow execution, or the work depends on systems you cannot reach. Then:

- Do the strongest static checks available: careful reading of the changed path end to end, checking types and signatures against definitions, tracing every caller, comparing with similar working code.
- Write the tests even if you cannot run them, and say so.
- Give the user the exact commands to run and what they should see, so they can close the loop quickly.
- Lower the confidence of your claim accordingly: "This should fix it; I couldn't run the suite here — please run `<command>` and check that `<test>` passes."

Never fabricate output. If you did not see it, do not present it as seen.

## Tests that lie

A passing suite is evidence only if the tests can detect the failure you care about. Watch for:

- **Assertions that cannot fail** — `assert result is not None` when the function never returns `None`; snapshot tests updated blindly to match new output.
- **Tests that never reach the changed code** — the branch you modified is behind a flag or condition the test never sets. If coverage tools are available, check that your changed lines execute.
- **Over-mocking** — the collaborator you changed is mocked out, so the test exercises the mock.
- **Shared state and order dependence** — tests pass together but fail alone (or vice versa); results depend on what ran first.
- **Flakiness** — a test that passed once may fail on rerun. If a test is known flaky, run it several times, and do not treat one pass as proof.
- **Environment drift** — tests run against a local database with different data, version, or settings than the real one.
- **Caught-and-ignored errors** — the code under test swallows an exception, so the test passes while the work silently fails.

The quick antidote: temporarily break the thing you changed (revert the fix, return a wrong value) and confirm a test goes red. If none does, you have no automated evidence for the change.

## Verifying non-code work

The same discipline — observe, check against criteria, probe edges — applies outside code:

- **Documents**: render in the target format (PDF, slides, web page) and look at it; check every number, name, date, and link; read it once as the intended audience; confirm it answers the brief rather than a nearby question. For factual claims, apply `fact-checking`.
- **Analyses**: recompute headline numbers by an independent route (a different query, a spreadsheet, a back-of-envelope estimate); check that totals reconcile with known figures; inspect a few raw records behind each key number; check for filters that silently drop data.
- **Research answers**: confirm each claim traces to a source you actually read; check source dates; note where sources disagree.
- **Designs and UI**: view at the sizes, states, and themes that matter; test with keyboard and, if possible, a screen reader; check real content lengths, not placeholder text.
- **Configuration and infrastructure**: inspect the resulting state (the service is running, the setting took effect, the permission is granted) rather than trusting the command's exit status.

## Worked reasoning: verifying a bug fix

Illustration only. Report: "Invoices for customers in Australia show the wrong date."

1. **Reproduce first.** Create (or find in test data) an invoice for a customer in an Australian time zone, created late in the evening UTC. Observe the wrong date: it shows the previous day. Now you have a failing check.
2. **Write it as a test** that fails for the same reason. Confirm it fails.
3. **Fix** — e.g. format the date in the customer's time zone instead of the server's.
4. **Observe the fix** — the test passes; the original reproduction shows the right date.
5. **Probe neighbours** — a customer exactly at midnight local time; a time zone with a half-hour offset; a date across a daylight-saving change; a customer with no time zone set (what is the fallback?).
6. **Regressions** — run the invoicing and date-formatting tests; check other places that call the formatting helper you changed, since they now behave differently too.
7. **Report** — "Fixed and verified with a new regression test; also checked half-hour offsets and DST boundaries. Not verified: PDFs generated by the external renderer, which formats dates separately — it may have the same bug."

Step 7's last line is the kind of honest, specific gap that saves the user from a second bug report.

## When verification fails at the end

Sometimes the final check reveals a problem after hours of work. Then:

- Do not report "done with a minor issue" if the issue defeats the purpose. Report the actual state.
- If the fix is small and clearly within scope, fix it and verify again.
- If it is not, stop, leave the work in a clean state (revert or isolate partial changes), and report what works, what does not, and the options.
- Never weaken the check to make it pass. If the check itself is wrong, explain why and change it openly.

## Evidence worth carrying into the report

Verification is only useful to the user if they can see it. Keep, in compact form:

- The commands or actions you ran and their key results ("full suite: 412 passed, 0 failed"; "dry run lists 1,204 rows to update, matching the count query").
- Before/after measurements for anything quantitative, with conditions (data size, environment).
- The reproduction steps for a fix, so the user can repeat them.
- Specific edge cases checked, so the user knows what was *not* checked by omission.
- Any pre-existing failures, warnings, or oddities you saw and left alone, with a note that they predate your change.

Summarize; do not paste full logs. Quote exact output only where the exact text matters, such as an error message or a number. See `report-results` for how to present this.

## Calibrating effort

Verification effort should scale with the cost of being wrong.

| Situation | Minimum verification |
|---|---|
| Throwaway script or exploratory spike | Run it once on real input; eyeball the output |
| Small change in well-tested code | Relevant tests + diff review |
| User-facing feature | Above, plus exercise it end to end; key edge cases |
| Shared library, public API, schema | Above, plus regression run across dependents; compatibility check |
| Data migration, deletion, or bulk change | Dry run, sample verification, counts before/after, backup or rollback confirmed |
| Security, auth, money, privacy | Above, plus explicit negative tests (who must NOT be able to do it); consider a second reviewer |
| Production config or deploy | Plan/dry-run first; post-change health checks; monitoring watched |

## Pitfalls and anti-patterns

- **"It compiles, ship it."** Compilation is the weakest meaningful check. Fix: run the behavior.
- **Green by subtraction.** Making tests pass by deleting, skipping, or loosening them. Fix: if a test is wrong, say so and explain the change; never do it silently.
- **Zero tests ran.** A filter typo or misconfigured path collects nothing, and the runner reports success. Fix: check the count and the names of tests that ran.
- **Testing the mock.** Tests so heavily mocked that they verify only the mocks. Fix: at least one check that exercises real integration for the changed path.
- **Wrong environment.** Verifying against a stale build, a cached result, a different branch, or a different config than the one that matters. Fix: confirm what you ran against; rebuild or clear caches when in doubt.
- **The fix for the wrong bug.** The symptom you fixed is not the one the user reported. Fix: reproduce the user's exact scenario.
- **Victory on the happy path.** Works for the example input; fails on empty, large, or malformed input. Fix: probe the edge cases that matter.
- **Ignoring warnings.** New deprecation, type, or runtime warnings often foreshadow failures. Fix: read them; resolve or report.
- **Claiming "tested" after reading.** Fix: use the verified / inferred / not-verified distinction.
- **Verification theater.** Running many cheap checks that cannot fail while skipping the one meaningful check that is slightly harder. Fix: ask which single check would most convince a skeptical reviewer, and do that one.
- **Leaving instrumentation behind.** Debug logging, temporary flags, test data in real databases. Fix: clean up and check the diff again.

## Safety notes

- Verification must not cause harm. Do not "test" by running against production data, sending real messages or payments, or calling destructive endpoints. Use staging, dry-run modes, sandboxes, test accounts, and copies.
- For destructive operations, verify the *plan* (what would be affected) before execution and the *result* after. Confirm a backup or rollback path exists first.
- Do not paste secrets, tokens, or personal data into logs or reports while showing verification output; redact them.

## Verification of the verification

Before you say "done", you should be able to say yes to:

- [ ] I know what "done" means for this task, and I checked each criterion.
- [ ] I observed the change working in the way the user will experience it, or I have stated clearly why I could not.
- [ ] The checks I ran could have failed if the work were wrong.
- [ ] I read actual outputs, not only exit codes.
- [ ] Broader checks (build, types, lint, related tests) pass, or failures are pre-existing and noted.
- [ ] I probed the edge cases most likely to break this change.
- [ ] My diff contains only intended changes.
- [ ] Every claim in my report is labelled honestly as verified, inferred, or not verified.
