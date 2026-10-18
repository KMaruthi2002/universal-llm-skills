---
name: code-review
description: >-
  Review a code change (pull request, merge request, patch, diff, or a set of
  edited files) for correctness, safety, maintainability and fit with the
  codebase, and write feedback the author can act on. Covers understanding
  intent first, prioritising logic and edge cases over style, concurrency,
  security, tests, API and schema changes, performance, severity levels,
  reviewing AI-generated code, and avoiding nitpick noise. Use when asked to
  "review this PR", "look over my diff", "check this change before I merge",
  "is this code OK", or to self-review your own change. Not for auditing a
  whole existing system (security-audit, architecture-review) or for preparing
  and landing your own PR (pull-request-workflow).
metadata:
  category: quality
  related: pull-request-workflow, secure-coding, testing-strategy, performance-optimization, concurrency-and-async, api-design, refactoring, git-workflow, error-handling, database-migrations
---

# Code Review

A code review is a second, independent reading of a change by someone whose job is to find what the author could not see. Its value is almost entirely in **defects caught before they ship** and **knowledge shared between people**. Everything else (consistency, polish) is secondary and should be cheap, or automated.

This skill covers reviewing a *change*. For assessing a whole system's security posture use `security-audit`; for judging a design before it is built use `architecture-review`; for the author's side of the process (scoping, describing, responding, merging) use `pull-request-workflow`.

## Core principles

**1. Understand the intent before judging the code.** You cannot say whether code is correct without knowing what it is supposed to do. A perfectly clean function that solves the wrong problem is the most expensive defect a review can miss, and it is invisible if you read line by line. Read the description, linked issue, and tests first; state the intended behaviour to yourself in a sentence.

**2. Correctness beats style.** A missed off-by-one costs an incident; a misnamed variable costs a few seconds of a future reader's time. Spend attention in proportion to the cost of being wrong. If you have a limited budget (and you always do), spend it on logic, data, security, and failure handling first.

**3. Review the change in its context, not the diff in isolation.** Diffs hide what did not change: the caller that now receives a different type, the second code path that needed the same fix, the config that still references the removed flag. Open the surrounding files. Search for other users of anything whose contract changed.

**4. Every comment should be actionable and ranked.** The author has to decide what to do with each comment. A comment that does not say what is wrong, why it matters, and how serious it is forces a round trip. Labelling severity lets the author fix blockers first and ignore preferences without guilt.

**5. Only claim what you have verified.** A false positive costs the author time, erodes trust in every later comment, and sometimes leads them to "fix" correct code. If you suspect a bug, trace it or test it; if you cannot, phrase it as a question.

**6. The project's norms win.** Review against the codebase's conventions, the team's documented review guidelines, and its linters, not against your personal taste or another ecosystem's idioms. If a convention seems harmful, raise that separately; do not block a change for following it.

**7. Review the code, not the person.** Feedback is about the artifact. This is not only kindness: defensive authors stop explaining their reasoning, and reviews get worse.

## Discovering context before you read the diff

Gather, cheaply and in roughly this order:

- **The stated goal**: PR description, linked ticket, commit messages. If there is no description, write down what you *think* the goal is and confirm it in your first comment.
- **Review norms**: a `CONTRIBUTING` file, `CODEOWNERS`, PR template, review checklist, style guide, ADRs. These tell you what the team cares about and what is already enforced by tooling.
- **What tooling already checks**: linters, formatters, type checkers, static analysis, CI test results. Do not spend human attention on anything a machine already enforces; if CI is red, find out why before reviewing in depth.
- **The blast radius**: which modules, services, public APIs, schemas, or user-facing behaviours this touches. Shared libraries, auth, billing, data migrations and concurrency primitives deserve a slower read than a leaf UI component.
- **Who else should look**: if the change touches an area with an owner or a specialist (security, database, accessibility), say so rather than pretending to cover it.

If you can run code: check out the branch, build it, run the tests, and exercise the changed behaviour. Reading finds design problems; running finds the ones you would have argued about.

## The review process

### Pass 1 — Shape (minutes)

Read the description, the file list, and the tests before any implementation. Ask:

- Does the change do what it says, and only that? Unrelated refactors mixed into a behaviour change make both harder to review and to revert.
- Is this the right *place* for the change? (Fixing a symptom in the caller when the bug is in the callee; adding a special case instead of fixing a general rule.)
- Is it the right *size*? Very large changes get rubber-stamped. If you cannot hold it in your head, say so and suggest a split along a seam you can name.
- Is the approach sound at all? If not, stop here and say so. Line comments on a change that should be redone waste everyone's time.

### Pass 2 — Correctness (most of your time)

Walk each changed code path with concrete inputs. For each function or block, try:

- the normal case,
- empty, zero, null/none, missing key, empty collection,
- one, many, and the boundary (max length, last page, exactly at the limit),
- malformed or hostile input,
- the failure of every call it makes (network, disk, DB, parse, permission),
- being called twice, concurrently, or out of order.

The detailed checklist below lists what to look for in each area. You do not need every item for every change; pick the areas the change actually touches.

### Pass 3 — Tests

Read the tests as a specification. Would they fail if the change were reverted? Do they cover the edge cases you found in pass 2? (See "Tests" below.)

### Pass 4 — Maintainability and fit

Naming, structure, duplication, comments, consistency with neighbouring code. Keep this pass short and keep its comments low-severity unless something will genuinely mislead a future maintainer.

### Pass 5 — Write up

Order your feedback by severity, add a summary, give a clear overall verdict. (See "Writing the review".)

For a small change, these passes collapse into one read. For a large or risky one, do them separately; mixing them is how style comments crowd out the real bug.

## What to look for

### Logic and data

- Off-by-one in loops, slices, pagination, ranges (inclusive vs exclusive end).
- Inverted or incomplete conditions; `and`/`or` precedence; De Morgan mistakes; early returns that skip cleanup.
- Wrong variable (copy-paste from the block above is the classic).
- Integer overflow, division by zero, floating point used for money or equality.
- Time: time zones, DST, naive vs aware timestamps, clock skew between machines, "now" captured once vs repeatedly, leap days, month-end arithmetic.
- Text: encoding, normalisation, case-folding in non-English locales, byte length vs character length.
- Mutation of shared or input data the caller did not expect; aliasing.
- State machines: every transition handled, no impossible states representable, idempotency of retries.
- Behaviour change for existing callers or stored data that the description does not mention.

### Error handling

- Errors swallowed, logged and ignored, or converted into success.
- Catch blocks that are too broad (catch-all hiding programmer errors) or too narrow (missing a failure the code can actually produce).
- Partial failure: if step 3 of 5 fails, what state are we left in? Is it recoverable?
- Resources released on every path (files, connections, locks, transactions).
- Retries without backoff, without a limit, or of non-idempotent operations.
- Error messages that leak internals to users, or that lose the cause chain needed for debugging.

See `error-handling` for depth.

### Concurrency and async

- Shared mutable state accessed from multiple threads, tasks, requests or processes without synchronisation.
- Check-then-act races (`if not exists: create`), read-modify-write without atomicity or optimistic locking.
- Lock ordering (deadlock), locks held across I/O or `await`, missing release on error.
- Unawaited promises/futures, fire-and-forget tasks whose errors vanish, cancellation not propagated.
- Blocking calls on an event loop or UI thread.
- Assumptions that a job runs once, that messages arrive in order, or that a cache is consistent with its source.

Concurrency bugs rarely show up in tests. If the change introduces shared state, ask explicitly how it is protected. See `concurrency-and-async`.

### Security

Read every change that handles input, identity, money, files, or external calls with an attacker's question: *what if this value is chosen by someone hostile?*

- Injection: SQL, shell, template, LDAP, path, header, log. Is untrusted data ever concatenated into an interpreted string?
- Authorisation: is there a check that *this* user may act on *this* object (not just that they are logged in)? Is it on the server? Is it on every new endpoint, including the ones added "just for the admin UI"?
- Authentication and sessions: token handling, expiry, comparison in constant time, logout/invalidation.
- Output encoding for HTML/JS contexts (XSS); unsafe deserialisation; server-side requests to user-supplied URLs (SSRF); open redirects.
- Secrets in code, config, test fixtures, logs, or error messages.
- Cryptography: home-made schemes, weak algorithms, predictable randomness for security purposes, disabled certificate verification.
- New dependencies: are they maintained, necessary, and from the expected source? (Typosquatting is real.)
- Data exposure: are new fields in API responses or logs personal or sensitive?

When a security issue is plausible but you are not sure, flag it as a question and suggest a specialist look. See `secure-coding` and `authentication-and-authorization`.

### Tests

- **Would the test fail without the change?** A test that passes against the old code tests nothing. If you can, revert the implementation locally and run it.
- Does it test behaviour (inputs and observable outputs) rather than implementation details that will break on any refactor?
- Are edge cases and failure paths covered, not just the happy path?
- Are assertions specific? (`assert result` or "does not throw" is rarely enough.)
- Is it deterministic? Watch for real time, randomness, network, ordering of hash maps, shared global state, sleeps.
- Is mocking hiding the interesting part? A test that mocks the database cannot catch a wrong query.
- For bug fixes: is there a regression test that reproduces the original bug?

Missing tests are not automatically a blocker. Weigh against risk: untested changes to billing logic are; untested copy changes are not. See `testing-strategy`.

### API, schema and contract changes

Anything another component, team, client, or stored record depends on deserves extra care, because the cost of a mistake is paid by people outside this PR.

- Is it backward compatible? Removed or renamed fields, changed types, new required parameters, changed defaults, changed error codes, changed ordering.
- If it is breaking: is it versioned, announced, and is there a migration path?
- Database migrations: can they run on a large table without locking it? Are they reversible? Is the code compatible with both the old and new schema during a rolling deploy? See `database-migrations`.
- Serialised data, queues, caches and events: will consumers running the previous version understand the new format, and vice versa?
- Feature flags and config: new settings have safe defaults; removed ones are not still referenced elsewhere.

See `api-design`.

### Performance

Raise performance only when there is a plausible real cost, not on principle.

- Work inside loops that could be done once: queries (N+1), allocations, regex compilation, network calls.
- Unbounded operations on user-controlled sizes: loading a whole table, unpaginated endpoints, unbounded caches or queues, recursion depth.
- Missing indexes for new query patterns.
- Algorithmic complexity that is fine at today's size but quadratic in something that grows.
- Synchronous work on a latency-critical path that could be deferred.

Ask for a measurement when the claim matters; do not demand micro-optimisations in cold code. See `performance-optimization`.

### Maintainability and fit

- Does it follow the patterns used nearby? A new way of doing an existing thing doubles the concepts a maintainer must know.
- Names that say what something *is* or *does*; misleading names are worth a comment, merely imperfect ones usually are not.
- Duplication that will drift; abstraction introduced for a single use (both are failure modes).
- Dead code, commented-out code, leftover debug output, TODOs without an owner.
- Comments that explain *why*, especially for non-obvious constraints; comments that now contradict the code.
- Observability: will an operator be able to tell this failed? Are new failure modes logged or measured? See `observability`.

## Severity levels

Use whatever labels the project uses. If it has none, a scale like this works because it maps directly to the author's decision:

| Level | Meaning | Author's expected action | Examples |
|---|---|---|---|
| Blocker | Will cause incorrect behaviour, data loss, a security hole, or an outage; or the approach is wrong | Must be resolved before merge | Missing authorisation check; migration that locks a hot table; race that double-charges |
| Should fix | Real defect or risk, but limited impact or easy to follow up | Fix now, or agree on a tracked follow-up | Unhandled error on a rare path; missing test for an edge case; confusing API name in a public interface |
| Suggestion | Would make the code better; reasonable people could disagree | Author's call | Simpler structure; clearer name; extracting a helper |
| Nit | Trivial, cosmetic, or taste | Optional; ignore freely | Wording of a comment; ordering of imports not enforced by a linter |
| Question | You do not understand something, or suspect but have not confirmed | Answer; may become any of the above | "What happens here if the list is empty?" |
| Praise | Something done notably well | None | A clean fix for a subtle bug; a test that pins the edge case |

Rules of thumb:

- If you cannot explain the concrete harm, it is not a blocker.
- If more than a handful of your comments are nits, delete most of them. Nits have a cost: they bury the important comments and make reviews feel like hazing.
- Recurring nits are a signal to add a linter rule or a style note, not to keep commenting.
- Mark questions as questions. "Is this right?" reads as an accusation if the author cannot tell whether you have found a bug.

## Writing actionable comments

A good comment contains:

1. **Where** — anchored to the specific line or range.
2. **What** — the problem, stated concretely ("if `items` is empty, `items[0]` raises").
3. **Why it matters** — the consequence ("this endpoint is called with an empty cart on first load, so every new user hits a 500").
4. **Severity** — explicitly labelled.
5. **A direction** — a suggested fix, alternative, or the question that would resolve it. Offer, do not dictate, unless it is a blocker with one right answer.

Illustrative contrast (not a required format):

- Weak: "This looks wrong."
- Better: "Blocker: `user_id` here comes from the request body, so any logged-in user can update another user's profile by changing it. Use the authenticated session's user id instead, and add a test that a mismatched id returns 403."

Further guidance:

- **Ask about intent when the intent is unclear**, rather than assuming a mistake: "Was dropping the retry intentional? Previously transient failures were retried three times."
- **Show, don't describe**, for small fixes: a suggested code snippet removes ambiguity. Make sure the snippet is correct; a wrong suggestion is worse than none.
- **Point to the pattern, then stop.** If the same issue appears in ten places, comment once with "same in N other places, e.g. X and Y" rather than ten times.
- **Separate "must" from "could"** in the same comment if both apply.
- **Do not relitigate settled decisions** in the PR (e.g. a framework choice made in a design review) unless the change reveals new information.
- **Avoid scope creep.** "While you're here, could you also refactor X" belongs in a follow-up ticket unless the change made X worse.

## The overall verdict and summary

End with a summary the author (and anyone skimming) can act on:

- A one-line verdict: approve, approve with minor comments, request changes, or "needs a different approach". Match the project's review states.
- The blockers, listed, so nothing gets lost in a long thread.
- What you did *not* review or could not verify ("I didn't review the migration's performance on production-size data", "I couldn't run the integration tests locally"). This is critical: an approval implies coverage, and silent gaps are how bad changes get through two reviewers who each assumed the other checked.
- Optionally, what was done well. Specific praise teaches as much as criticism.

Approve when the change makes the codebase better and has no unresolved blockers, even if it is not how you would have written it. Perfection is not the bar; "better than before and safe to ship" is.

## Decision guidance

**Block, or approve with comments?**

| Situation | Lean towards |
|---|---|
| Defect with user-visible, security or data impact | Block |
| Defect, low impact, author is responsive and the follow-up is tracked | Approve with comments |
| Disagreement about style or structure, no defect | Approve; leave suggestion |
| You do not understand the change well enough to judge | Neither: ask questions, or hand off to someone who does |
| Change is fine but its premise is questionable | Comment on premise; block only if shipping it causes harm or lock-in |
| Urgent hotfix | Review for correctness and safety only; file follow-ups for the rest |

**How deep to go?** Scale effort to risk, not to size. A three-line change to an authorisation check deserves more care than three hundred lines of generated test fixtures. Signals of high risk: touches security, money, persistence, concurrency, public contracts, or deletes things; is hard to roll back; runs at high volume; has no tests; author is new to the area.

**Comment in the PR or talk?** If a thread goes beyond two rounds, or the disagreement is about approach rather than a line, move to a synchronous conversation and then record the outcome in the PR.

## Reviewing AI-generated code

Code produced by an LLM or agent fails differently from human code, and reviewing it well needs adjusted attention. Treat it as code from a fast, fluent, confident contributor who has never run it and does not know your system.

What to look for specifically:

- **Plausible but non-existent APIs**: functions, flags, config keys or library methods that look right but do not exist, or exist in a different version. Check imports and calls against the actual dependency version in the project.
- **Hallucinated or unnecessary dependencies**: new packages that are not needed, are unmaintained, or have names suspiciously close to popular ones.
- **Silent scope expansion**: unrelated files reformatted, functions "improved", or behaviour changed beyond the request. Diff the whole change, not just the part you asked for.
- **Tests that test nothing**: tests that assert on mocks, that mirror the implementation, that were adjusted to match buggy output, or that were deleted or skipped to make CI pass. Look for removed assertions and new `skip` markers.
- **Weakened checks**: loosened types (`any`), widened catch blocks, disabled lint rules, lowered thresholds, removed validation. These often appear when generated code was iterated until it "worked".
- **Over-engineering or duplication**: a new helper that duplicates one already in the codebase, because the generator did not know it existed; abstraction layers for a single use.
- **Surface consistency hiding semantic errors**: well-named, well-commented code whose logic is subtly wrong. The polish lowers reviewers' guard; do not let it.
- **Security defaults**: generated code frequently builds queries by string concatenation, disables certificate checks "for testing", logs whole request objects, or skips authorisation on new endpoints.
- **Confident comments and descriptions that do not match the code**: verify claims like "handles all edge cases" or "thread-safe" against the implementation.

If you are the agent reviewing your own generated change, the same list applies with more force: you are the least likely reviewer to see your own blind spots, so actually run the code and the tests, and re-read the full diff from the top before calling it done (see `verify-before-done`).

Do not apply a lower or higher bar based on who or what wrote the code. The bar is the same; the places to look are different.

## Verifying your own findings

Before posting, check each finding that is more serious than a nit:

- **Trace it.** Follow the value from its source to the line you are flagging. Is it actually reachable with the bad input? Is there validation upstream you missed?
- **Check the context.** Is there a framework guarantee, middleware, base class, or caller that already handles this? (Many "missing auth check" findings are handled by a decorator three files away; many are not.)
- **Run it if you can.** A failing test or a reproduction turns an argument into a fact.
- **Check the version.** Library behaviour and language semantics differ by version; confirm against the version the project uses.
- **Downgrade if unsure.** If you could not confirm it, post it as a question with your reasoning. "I think this can be null when X; am I missing a check?" is useful. "This will crash" when it will not is costly.

Likewise, before approving, ask: what would I be embarrassed to have missed here? Check that.

## Pitfalls

- **Line-by-line tunnel vision**: reviewing each hunk in isolation and missing that the overall approach is wrong, or that a second code path needed the same change.
- **Bikeshedding**: long threads on naming and formatting while a logic bug goes unmentioned. If a machine could enforce it, it should.
- **Rubber-stamping large PRs**: approving because it is too big to read. Say it is too big instead.
- **Review by reputation**: skimming a senior engineer's change or nitpicking a junior's. Same bar for all.
- **Taste as requirement**: blocking on "I would have done it differently" without a concrete harm.
- **Moving goalposts**: new, unrelated requests in each review round. Raise everything you can in the first full pass.
- **Unverified claims**: asserting a bug you did not trace; suggesting a fix that does not compile.
- **Ignoring deletions**: removed code, tests, checks and config can be the most dangerous part of a diff.
- **Ignoring non-code files**: CI config, dependency lockfiles, infrastructure, permissions, migrations, and feature-flag defaults often carry the real risk.
- **Silent partial review**: approving after reading half the change without saying so.
- **Hostile or sarcastic tone**: makes authors defensive and less forthcoming; slows every future review.

## Quality bar

A good review:

- demonstrates that the reviewer understood what the change is for;
- finds the important problems, ranked, with blockers clearly separated from preferences;
- contains no claims the reviewer did not verify or mark as uncertain;
- gives each comment a concrete reason and a direction;
- respects the project's conventions and tooling;
- states what was not covered;
- ends with a clear verdict;
- is proportionate: depth matches risk, and nit volume is low.

Quick self-check before posting:

- Did I read the description and tests before the implementation?
- Did I look outside the diff (callers, other code paths, config)?
- Did I check failure paths, not just the happy path?
- Is every blocker backed by a concrete scenario?
- Would the tests fail if the change were reverted?
- Have I stated what I did not review?

## Related skills

- `pull-request-workflow` — the author's side: preparing, describing and landing a change.
- `secure-coding`, `authentication-and-authorization` — depth on the security checks above.
- `testing-strategy` — judging whether tests are adequate.
- `concurrency-and-async`, `error-handling`, `performance-optimization` — depth on those review areas.
- `api-design`, `database-migrations` — contract and schema changes.
- `refactoring` — when the review reveals that structure, not the change, is the problem.
