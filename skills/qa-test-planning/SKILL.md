---
name: qa-test-planning
description: >-
  Plan quality assurance for a feature, release, or product: decide what to
  test and how deeply based on risk, derive test cases with equivalence
  partitioning, boundary values, decision tables, and state-transition
  analysis, write exploratory testing charters, choose device/browser/OS
  coverage matrices, set entry and exit criteria, and write bug reports that
  reproduce. Use when asked for a "test plan", "QA plan", "test cases", "what
  should we test", "regression checklist", "test matrix", "exploratory
  testing", "how do I report this bug", or when a feature is about to go to QA.
  For the overall automated test architecture of a codebase use
  testing-strategy; for writing browser automation use end-to-end-testing.
metadata:
  category: quality
  related: testing-strategy, end-to-end-testing, requirements-analysis, user-stories, release-readiness, accessibility-audit, web-performance-audit, debugging
---

# QA Test Planning

A test plan is a set of deliberate bets about where defects are likely to be and how bad they would be. Its job is to spend a limited testing budget where it buys the most confidence, and to make that reasoning visible so others can challenge it. A plan that lists hundreds of cases with equal weight has made no bets at all.

## Scope

This skill covers planning and designing testing for a feature or release, from the perspective of a QA engineer or a developer acting as one:

- Risk analysis and test prioritization.
- Test design techniques that turn requirements into cases.
- Exploratory testing charters and sessions.
- Coverage matrices for platforms, devices, locales, and configurations.
- Entry/exit criteria, test data, environments.
- Bug reports and triage.

Neighbouring skills:

- `testing-strategy` — how a codebase's automated test suite should be structured (unit vs integration vs E2E, the test pyramid, CI gates).
- `end-to-end-testing` — implementing reliable automated UI tests.
- `release-readiness` — the go/no-go decision; a test plan feeds it.
- `requirements-analysis` / `user-stories` — when the requirements themselves are missing or contradictory; testing exposes that, but fixing it is a different job.

## Core principles

**1. Risk drives depth.** Risk is roughly likelihood of failure times impact of failure. Likelihood rises with complexity, novelty, churn, integration points, concurrency, and a history of bugs in that area. Impact rises with money, data loss, security, legal exposure, the number of users touched, and how visible the failure is. Test high-risk areas deeply and from several angles; give low-risk areas a smoke check. Write down why you ranked things as you did, because the ranking is the part people should argue with.

**2. Testing finds information, it does not prove absence of bugs.** Exhaustive testing is impossible for anything nontrivial (a form with five fields of ten values each already has 100,000 combinations). Every plan samples. The skill is in sampling cleverly: techniques like partitioning and pairwise selection exist to get the most defect-finding per test.

**3. Test against intent, not only against the spec.** Specs are incomplete. A feature can meet every written requirement and still be wrong for the user. Ask "what is this for, and what would make a user say it is broken?" alongside "does it do what the ticket says?".

**4. Scripted and exploratory testing are complements.** Scripted cases are repeatable, reviewable, and good for regression and compliance. Exploratory testing, where design and execution happen together guided by a charter, finds the bugs nobody thought to script. A good plan uses both and says how the time is split.

**5. A bug that cannot be reproduced cannot be fixed with confidence.** The value of a bug report is almost entirely in whether a developer can see the failure themselves. Precision there saves more time than any other QA habit.

**6. Plans should be as light as the context allows.** A two-line checklist in a pull request can be the right test plan for a small change. A regulated medical device needs traceability from requirement to test to result. Match the formality to the risk and the audience; do not produce ceremony nobody reads.

## Process

### 1. Understand what is changing and why

Gather before designing anything:

- The requirement, user story, or spec, plus acceptance criteria. Read designs and prototypes.
- What actually changed in code, if available: the diff, the components touched, migrations, new dependencies, feature flags. Changed code is where new bugs live; code it depends on and code that depends on it are where regressions live.
- Who uses this, on what platforms, how often, and what they are trying to accomplish.
- Constraints: release date, environments available, test data, who is testing, how much time.

Ambiguities found here are the first and cheapest defects. List them as questions for the product owner or developer rather than guessing. "What should happen if the discount code is applied after the cart total drops below the minimum?" is a test case and a requirement gap at once.

### 2. Map the risk

Break the feature into areas (functions, flows, integrations, quality attributes) and rate each. A simple table does the job:

| Area | Likelihood | Impact | Why | Depth |
|---|---|---|---|---|
| Payment capture with saved cards | Medium (new provider API) | High (money, trust) | Third-party integration, retries, partial failures | Deep: scripted + exploratory + negative + concurrency |
| Discount code validation | High (complex rules) | Medium | Many rule combinations, history of bugs | Deep: decision table, boundaries |
| Order confirmation email | Low (unchanged template) | Medium | Only the subject line changed | Smoke |
| Admin report export | Low | Low | Unchanged, internal | Regression suite only |

Do not forget non-functional risk: performance under load, security (authorization on new endpoints, injection on new inputs), accessibility, localization, data migration, backward compatibility of APIs, upgrade paths, offline and poor-network behavior, and observability (will we know if it fails in production?). Bring in specialist skills (`accessibility-audit`, `web-performance-audit`, `security-audit`) for areas rated high.

### 3. Design tests with techniques

Use the technique that fits the shape of the logic. These are tools for generating good cases systematically, so you are not relying on inspiration.

**Equivalence partitioning.** Divide each input's possible values into classes the system should treat the same way, then test one representative per class. Include invalid classes. For an age field accepting 18–120: below range, in range, above range, non-numeric, empty, decimal, negative. The reason it works: if one value in a class is handled correctly, others probably are too, so testing more of the same class adds little.

**Boundary value analysis.** Defects cluster at the edges of partitions, because that is where off-by-one errors and wrong comparison operators live. For each boundary test just below, on, and just above: 17, 18, 19 and 119, 120, 121. Also: zero, one, many; empty and maximum length strings; first and last item in a list; start and end of a day, month, year; time zone and daylight-saving transitions; maximum file size; integer and currency rounding limits.

**Decision tables.** When outcomes depend on combinations of conditions (user type, cart total, code validity, region), list the conditions as rows, each combination as a column, and the expected action for each. This exposes missing rules ("what happens for a guest user with an expired code?") and lets you collapse combinations that do not matter. Use it whenever you see business rules with several "if... and... unless".

**State-transition testing.** For anything with a lifecycle (order: draft, placed, paid, shipped, cancelled, refunded; account: invited, active, suspended, deleted), draw the states and allowed transitions. Test every valid transition at least once, then the invalid ones (can a shipped order be cancelled? what about double-clicking "pay" or replaying a request?). Pay attention to transitions triggered by time (expiry) or external events (webhooks), and to what happens when two transitions race.

**Pairwise / combinatorial testing.** When many independent parameters each have several values (browser, OS, language, account tier, payment method), testing all combinations explodes. Most interaction defects involve two factors, so a set covering every pair of values catches most of them with far fewer tests. Tools exist (e.g. PICT, allpairs-style generators); use constraints to exclude impossible combinations. Use higher-strength (three-way) coverage for the riskiest parameters.

**Use-case and scenario testing.** Write end-to-end scenarios as a real user would perform them, including interruptions: user leaves mid-checkout and returns tomorrow; two tabs open; back button after submit; session expiry during a long form. Scenarios catch integration failures that per-field techniques miss.

**Error guessing and checklists.** Experience-based heuristics: special characters and emoji, very long input, leading/trailing whitespace, copy-paste of formatted text, right-to-left scripts, SQL- and script-like strings (as a safety check, not a penetration test), duplicate submissions, slow and lost network, low storage, permissions denied, clock skew, browser autofill, zoomed or high-contrast display.

**Negative and robustness testing.** What happens with invalid input, missing dependencies, malformed responses from third parties, partial failures (payment succeeded but order write failed)? The question is not only "is it rejected?" but "does it fail safely, tell the user something useful, and leave data consistent?".

### Worked example: from a rule to cases

Suppose the requirement reads: "Free shipping applies to orders of 50.00 or more for members, and 75.00 or more for guests. It never applies to oversized items. Members in the trial period count as guests."

Step one, list the conditions: customer type (member, trial member, guest), subtotal (relative to the thresholds), cart contains an oversized item (yes/no).

Step two, partition subtotal per customer type. For members: below 50.00, exactly 50.00, above. For guests and trial members: below 75.00, exactly 75.00, above. Boundary values: 49.99, 50.00, 50.01 and 74.99, 75.00, 75.01. Also the interesting cross-case: a member at 60.00 (free) versus a trial member at 60.00 (not free), which is exactly where the "trial counts as guest" rule could be implemented wrong.

Step three, build the decision table and collapse it. Any cart with an oversized item yields "no free shipping" regardless of the other conditions, so that whole half collapses to a few representative columns. What remains is about a dozen meaningful cases instead of the full cross product.

Step four, ask the questions the table exposed: Is the threshold applied before or after discounts? Before or after tax? What if an oversized item is removed after shipping was calculated? What currency rounding applies? Each answer either becomes an expected result or reveals a requirement gap to raise.

Step five, add the state dimension: the subtotal can change after free shipping is granted (removing items, applying a code, a price change between sessions). Test that the shipping charge recalculates at each change and at final submission, since client and server may disagree.

This is the general pattern: conditions, partitions, boundaries, combinations, then changes over time.

### Worked example: a state machine

For a subscription with states Trial, Active, Past due, Cancelled, Expired:

- Valid transitions: Trial to Active (payment succeeds), Trial to Expired (trial ends unpaid), Active to Past due (renewal fails), Past due to Active (retry succeeds), Past due to Cancelled (retries exhausted), Active to Cancelled (user cancels).
- Test each once, checking side effects at each step: access rights, emails sent, invoices created, analytics events.
- Invalid transitions to attempt: Cancelled to Active without a new purchase; Expired to Past due; cancelling twice; reactivating while a payment retry is in flight.
- Time-driven transitions: manipulate the clock or use test hooks to cross trial end, renewal date, and grace period boundaries, including across a month with fewer days and a daylight-saving change.
- Races: user cancels at the same moment the renewal job runs. What wins, and is the result consistent in every system that stores the state?

Write each case with enough detail to execute and judge it: preconditions, steps or input, and the expected result. The expected result must be specific ("error 'Code expired' shown under the field; total unchanged") — "works correctly" is not an expected result.

### 4. Plan exploratory testing

An exploratory charter states a mission for a time-boxed session (commonly 60–120 minutes). A useful phrasing is: *explore* an area, *with* certain resources or techniques, *to discover* a kind of information. For example:

- Explore the discount code field with boundary values and rapid edits to discover how validation and the displayed total stay in sync.
- Explore checkout under a throttled, intermittently dropping network to discover how retries and duplicate submissions are handled.
- Explore the new settings page with a screen reader and keyboard only to discover barriers before the formal accessibility review.

During a session, take notes as you go: what you tried, what you observed, questions, bugs, and ideas for further charters. Afterwards, debrief briefly: what was covered, what was not, what surprised you. The notes are the evidence of coverage; without them exploratory testing looks like "clicked around".

Useful touring heuristics to generate ideas: follow the money; follow the data (create, read, update, delete it, then look at it everywhere it appears); interrupt everything; go back and forward; repeat everything twice; change configuration midway; use the feature as a new user, a power user, an admin, and an attacker would.

### 5. Choose the coverage matrix

Platforms, devices, browsers, and locales multiply fast. Choose from evidence:

- Use the product's analytics to find which browsers, OS versions, devices, and screen sizes real users use. Cover what accounts for the large majority of traffic, plus anything contractually supported.
- Cover each rendering engine family at least once (Chromium-based, WebKit/Safari, Gecko/Firefox) since engines differ more than brands do. Safari on iOS deserves explicit attention: all iOS browsers have historically used WebKit and it has distinct behaviors.
- Distinguish depth: run the full suite on the primary configuration, a smoke or critical-path subset on secondary configurations, and visual checks on the rest.
- For mobile apps: OS versions (oldest supported and newest, including betas near OS release season), small and large screens, a low-end device for performance, tablets if supported, different permission states, and OEM variants on Android.
- Locale and region: at least one right-to-left language if supported, a language with long words (text expansion), non-Latin scripts, date/number/currency formats, and time zones on both sides of UTC.
- Accessibility settings: large text/zoom, reduced motion, high contrast or forced colors, at least one screen reader.

An illustrative matrix (not a template; derive yours from data):

| Configuration | Depth | Reason |
|---|---|---|
| Chrome latest, Windows | Full | Largest share of traffic |
| Safari latest, iOS | Full | Second largest, distinct engine |
| Firefox latest, desktop | Critical paths | Engine coverage |
| Safari, macOS | Critical paths | Engine + OS variant |
| Chrome, Android low-end device | Critical paths + perf spot check | Performance risk |
| Edge, Windows, 200% zoom | Smoke + reflow | Accessibility and enterprise users |

Cloud device farms help with breadth; real devices still catch things emulators do not (touch, performance, camera, push notifications, battery and backgrounding).

### 6. Test data and environments

- Specify the data each case needs and how it gets there (seed scripts, fixtures, API setup). Shared, hand-maintained test accounts drift and cause false failures.
- Include realistic data volumes and shapes: long names, accented and non-Latin characters, accounts with thousands of items, legacy records created under old rules.
- Never use real customer personal data in non-production environments unless it is properly anonymized and policy allows it.
- Note environment differences from production (feature flags, third-party sandboxes, smaller databases, no CDN) and which risks they hide. A payment sandbox does not reproduce real decline patterns; say so.
- Testing in production (feature flags, canaries, synthetic monitoring) is legitimate for some risks, but plan it explicitly, with safeguards against touching real users' data or money.

### 7. Entry and exit criteria

State what must be true to start testing (build deployed, migrations run, test data ready, known blockers fixed) and what "done" means (all high-risk areas covered, no open critical or high-severity bugs without an explicit waiver, regression suite passing, accessibility and performance checks done if in scope). Exit criteria make the release conversation factual rather than a matter of mood. Feed the result into `release-readiness`.

### 8. Regression selection

You rarely have time to rerun everything. Choose regression tests by:

- Impact analysis: what code and data does the change touch, directly and through shared components?
- Business-critical paths that must never break (sign-in, purchase, data save), always included.
- Areas with recent defects or high churn.
- Automated suites for broad regression; manual effort for what changed and what automation cannot judge (visual quality, usability, copy).

### 9. Execute, track, and report progress

Track per area: planned, executed, passed, failed, blocked. Report coverage against risk, not just counts: "All high-risk areas tested; two medium-risk areas (export, notifications) not tested on Android" is more useful than "87% of cases executed". Report blocked tests prominently; a blocked test is untested risk.

### 10. What the written plan contains

Describe content, not a fixed layout; reuse the team's format if one exists. A plan for a typical feature usually covers:

- **Scope:** what is in and, just as important, what is explicitly out, so nobody assumes coverage that does not exist.
- **Risk analysis:** the area table and the reasoning behind it.
- **Approach per area:** techniques, scripted vs exploratory, automated vs manual.
- **Coverage matrix** and its justification.
- **Test data and environments,** with known differences from production.
- **Entry and exit criteria.**
- **Schedule and owners,** if more than one person is testing.
- **Open questions and assumptions.**
- **Cases and charters,** often in a linked tool or spreadsheet rather than the plan itself.

Keep the plan short enough to be read in full by the developer and product owner. Its main value is that they review the risk ranking and the out-of-scope list and tell you what you got wrong before testing starts.

### Heuristics for spotting likely defects

When estimating likelihood, these signals reliably predict trouble:

- Code that was hard to write (long review threads, many revisions, late changes).
- Logic split between client and server, or duplicated in two services.
- Anything involving time, money, units, rounding, or character encoding.
- Caching, retries, queues, and background jobs, where ordering and duplication bugs live.
- Permissions and multi-tenancy: can user A see or change user B's data?
- Code paths only reached on error, or behind rarely enabled flags.
- Third-party integrations, especially with sandboxes that behave differently from production.

## Writing bug reports that reproduce

A good report lets a developer see the failure in minutes without asking you anything. It contains:

- **A title that states the symptom and where.** "Discount total not recalculated after removing an item" beats "Cart bug".
- **Environment:** build/version or commit, environment URL, browser/app and version, OS, device, account type, locale, feature flags.
- **Preconditions and test data:** account state, items in cart, settings.
- **Numbered steps** starting from a known state, minimal and exact. Remove steps that do not matter: try reproducing with fewer steps before filing.
- **Expected result** and **actual result**, both specific, with the source of the expectation (spec, acceptance criterion, previous behavior, common sense — say which).
- **Frequency:** always, intermittent (e.g. 3 out of 10 attempts), once. For intermittent bugs, describe what you varied.
- **Evidence:** screenshots, short screen recordings, console errors, network request/response (redact tokens and personal data), server log excerpts, request IDs, timestamps with time zone.
- **Impact and severity**, plus any workaround.
- **Isolation notes:** what you tried that did not reproduce it (other browsers, other accounts), which narrows the cause dramatically. Whether it reproduces on the previous release (a regression) is especially valuable.

One bug per report. Search for duplicates first. Keep opinion out of the report; facts and impact persuade.

**Example (illustrative):**

> Title: Promo code total stays discounted after cart drops below minimum spend
> Env: staging build 4.12.0-rc2, Chrome 1xx on macOS, guest checkout, en-GB.
> Steps: 1. Add two items totaling 60.00 to cart. 2. Apply code SAVE10 (minimum 50.00). 3. Remove one item (cart subtotal 30.00).
> Expected: code removed or flagged invalid, total 30.00 (per promo rules in the spec, section 3.2).
> Actual: total shows 20.00; code still applied. Order can be placed at 20.00.
> Frequency: 5/5. Also on Firefox. Not on production 4.11 (feature new in 4.12).
> Severity: High — revenue loss, no user workaround needed to exploit.

### Intermittent bugs

Do not discard a failure because it happened once. Record everything about the moment (time, data, network conditions, what else was running), then vary one factor at a time: repeat count, speed of interaction, data, network throttling, concurrent sessions, cache state, time of day (scheduled jobs). Intermittency usually points to timing (races, async ordering), shared state (another tester's data, caches), environment (one of several servers behind a load balancer), or data-dependence. A report of "fails roughly 1 in 5 times, only when the second click happens within a second of the first" is often enough for a developer to find a race. See `debugging` for the developer's side.

### Severity vs priority

Severity is the impact of the bug on the product (data loss, crash, cosmetic). Priority is how soon the team will fix it, which also depends on business context, frequency, and release timing. A typo in the company name on the landing page is low severity and high priority. Keep both fields distinct if the tracker supports it, and use the team's existing scale.

## Decision guidance

**How formal should the plan be?**

| Situation | Appropriate plan |
|---|---|
| Small change, low risk | A checklist in the ticket or pull request: what to verify, what to regression-check |
| Typical feature | Risk table, key cases by technique, one or two charters, matrix subset, exit criteria |
| Major release or new product | Full plan with scope, risk analysis, schedule, environments, roles, matrix, entry/exit criteria |
| Regulated domain (medical, finance, aviation) | Traceability from requirements to cases to results; formal sign-off; follow the applicable standard and the organization's quality system |

**Scripted vs exploratory split.** Lean scripted when requirements are stable, the area is high-risk and must be repeatable, or audit evidence is needed. Lean exploratory when the feature is new and the spec thin, when time is short, or when you need to learn the product. A common starting split for new features is about half and half, shifting toward scripted (ideally automated) as the feature stabilizes.

**Manual vs automated.** Automate what is repeated often, stable, deterministic, and cheap to judge by machine (regression of critical paths, data validations, API contracts). Keep manual what needs human judgment, changes frequently, or is run rarely. Do not automate a test before you have run it manually at least once and understood it.

**Features with non-deterministic output** (recommendations, search ranking, AI-generated content). Exact expected results do not exist, so define properties instead: output is in the right format, within length limits, never includes prohibited content, ranks a known-relevant item in the top results, handles empty and adversarial input safely. Use a fixed evaluation set and compare against a baseline rather than judging single outputs. `llm-evaluation` covers this in depth for language-model features.

**When you can only plan, not execute.** If you have no access to the running product, deliver the plan, the cases, and the questions, and say which assumptions you made about behavior. If you can run the product (a browser, an emulator, an API client), execute at least the highest-risk cases and a short exploratory session, because a plan untested against reality usually misses the most important behavior.

## Bug triage

When many bugs arrive at once (end of a test cycle, a beta), triage them in a short, regular session with someone who can decide priority:

- Confirm each is reproducible and not a duplicate.
- Assign severity from impact, priority from business context.
- Decide: fix now, fix before release, fix later, won't fix (with reason recorded), or needs more information.
- Look for clusters: several bugs with a common cause are usually one fix, and a cluster signals an area needing more testing.
- Re-test fixes against the original steps and the surrounding area, since fixes cause regressions nearby.

## Discovering context

- Read existing test plans, regression suites, and bug history for the area; repeat offenders indicate risk.
- Check the team's tracker conventions: severity/priority scales, required fields, labels, templates they already use.
- Find the supported platform list (often in docs, contracts, or a support page) and analytics.
- Ask who else tests (developers, product, beta users, automated suites) to avoid duplicating or leaving gaps.
- Look for the definition of done and existing release checklists so the plan plugs into them.

## Pitfalls

- **Testing only the happy path.** Most severe production bugs are in error handling, edge states, and concurrency.
- **Equal weighting.** Hundreds of low-value cases crowd out depth on the risky parts.
- **Vague expected results.** "Should work" cannot fail, so it cannot find bugs.
- **Matrix by habit.** Testing on whatever devices are on the desk rather than what users use.
- **Ignoring data migration and existing data.** New code works on fresh test data and breaks on five-year-old records.
- **Testing the build, not the deployment.** Configuration, feature flags, caches, and CDNs differ in production.
- **Untracked exploratory testing.** Without notes, nobody knows what was covered.
- **Bug reports that narrate instead of specify.** Long stories without steps, environment, or expected result.
- **Combining several bugs in one report.** They get partially fixed and closed.
- **Treating the plan as fixed.** Update risk ratings as bugs are found: a cluster of defects in one area means more lurk there.
- **QA as a gate at the end.** The cheapest defects are the ones caught when reviewing requirements and designs. Involve testing thinking early.

## Quality bar and verification

- [ ] Every area has an explicit risk rating with a reason, and depth matches it.
- [ ] High-risk areas are covered by more than one technique and include negative cases.
- [ ] Boundaries, invalid classes, and state transitions (including invalid ones) are covered where relevant.
- [ ] Every test case has a specific, checkable expected result.
- [ ] Exploratory charters have a mission, time box, and a way to record findings.
- [ ] The coverage matrix is justified by usage data or support commitments, and covers each major engine/OS.
- [ ] Non-functional risks (security, performance, accessibility, localization, migration) were considered and either covered or explicitly excluded.
- [ ] Entry and exit criteria are stated.
- [ ] Open questions and requirement gaps are listed for the product owner.
- [ ] Bug reports can be reproduced by someone else from the report alone.
