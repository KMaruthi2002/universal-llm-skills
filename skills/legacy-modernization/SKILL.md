---
name: legacy-modernization
description: >-
  Safely change, extend, migrate, or replace old, undocumented, or poorly
  tested systems: code archaeology, characterization tests, finding seams,
  strangler-fig replacement, incremental migration, framework and language
  version upgrades, and managing the risk of touching code nobody understands.
  Use when working in a legacy codebase, inheriting a system with no docs or
  tests, planning a rewrite or replatforming, upgrading an end-of-life
  framework/runtime, or when someone says "nobody knows how this works" or "we
  can't touch that module".
metadata:
  category: development
  related: refactoring, explore-codebase, testing-strategy, dependency-management, database-migrations, software-architecture, technical-decision-making, release-management
---

# Legacy Modernization

Legacy code is code that is valuable, in production, and hard to change safely. It is usually not "bad code" in any simple sense: it encodes years of business rules, bug fixes, and edge cases that nobody wrote down. Modernization is the discipline of changing that code without losing what it knows.

## Scope

This skill covers working in and evolving existing systems whose behaviour is only partly understood: discovering what they do, pinning that behaviour down, creating places to make changes, and moving incrementally to a new structure, framework, language, or platform.

It does not cover:

- Small behaviour-preserving restructurings inside well-tested code — see `refactoring`.
- Choosing an architecture for a new system from scratch — see `software-architecture`.
- Upgrading a single library version in a healthy project — see `dependency-management`.
- Schema changes on their own — see `database-migrations` (but read it alongside this skill whenever data moves).

## Core principles

### 1. The existing behaviour is the specification

In a legacy system, the code is the only complete record of what the business actually requires. Comments lie, documentation drifts, and the people who knew have left. Treat current behaviour, including its bugs, as the contract until someone with authority decides otherwise. Why: "fixing" an apparent bug in passing frequently breaks a downstream consumer who has learned to depend on it (Hyrum's law: every observable behaviour will be depended on by somebody).

### 2. Never change behaviour and structure in the same step

Restructuring (moving, renaming, extracting) and behaviour change (fixing, adding, removing) must be separate commits, ideally separate deployments. Why: when something breaks, you need to know which kind of change caused it. Mixed changes turn every regression into an investigation.

### 3. Get feedback before you get clever

Before any meaningful change, establish a way to know whether you broke something: characterization tests, golden-output comparisons, production traffic replay, shadow runs, or at minimum a manual checklist executed against the real system. Why: the main risk in legacy work is not writing wrong new code, it is silently losing old behaviour. Feedback is what converts that invisible risk into a visible failure.

### 4. Incremental beats big-bang

Prefer a sequence of small, independently shippable, reversible steps over a rewrite that ships all at once. Why: big-bang rewrites fail at a high rate because they must re-discover every hidden requirement before delivering any value, the old system keeps changing underneath them, and there is no point at which partial work is useful. Incremental migration delivers value early, exposes hidden requirements one at a time, and can stop at any point with a working system.

### 5. Leave the system more understandable than you found it

Every excursion into legacy code should leave behind something: a test, a note, a clarified name, a diagram, a deleted dead branch. Why: understanding is the scarcest resource in a legacy system, and most of it evaporates when the session ends unless written down.

## Process

### Step 1: Clarify the actual goal

"Modernize" means different things. Pin down which one before planning, because each implies a different strategy:

| Stated goal | What it usually really means | Likely strategy |
|---|---|---|
| "Make it maintainable" | Changes are slow and scary | Characterization tests, seams, targeted refactoring of hot spots |
| "Upgrade the framework/runtime" | EOL, security patches, hiring | Stepwise version upgrades, compatibility shims |
| "Move to the cloud / new platform" | Ops cost, scaling, data centre exit | Lift-and-shift first, then re-architect selectively |
| "Rewrite in language X" | Often a mix of the above plus frustration | Challenge it; strangler fig if justified |
| "Split the monolith" | Team autonomy, deploy independence | Modularize in place first, then extract |
| "Add feature Y" to old code | Ship Y without breaking anything | Sprout/wrap, minimal footprint |

Ask what pain is being felt, how it is measured, and what "done" looks like. If the honest answer is "add one feature", do not start a modernization programme.

### Step 2: Archaeology — learn what exists

Do this before proposing anything. Budget real time for it; it is the cheapest risk reduction available.

**Map the territory**

- Entry points: main functions, HTTP routes, scheduled jobs, message consumers, triggers, stored procedures, cron entries, file watchers. Legacy systems often have entry points nobody remembers (a nightly batch, an FTP drop).
- Data stores and who writes to them. Shared databases are the most common hidden coupling in legacy systems: another application may read or write the same tables.
- External integrations: outbound calls, inbound callers, file exchanges, email, printers.
- Build and deploy: how it is actually built and shipped, which may differ from what the README claims. Find the real build script, the real server config.
- Runtime configuration: environment variables, config files, feature flags, database-stored settings.

**Read the history**

- Version control history reveals intent better than comments. Look at why frequently changed files changed (`git log --follow`, blame on surprising lines, commit messages that reference tickets).
- Hot spots — files that change often *and* are large or complex — are where modernization effort pays back most. Files that are ugly but never change can usually be left alone.
- Look for reverted commits and "fix the fix" chains; they mark fragile areas.

**Find the real behaviour**

- Logs and metrics from production show which code paths actually run. A feature that receives zero traffic in 90 days is a deletion candidate (confirm with owners; some paths are annual, e.g. year-end processing).
- Database contents reveal states the code supports: query distinct values of status columns, find nulls in "required" fields, find rows with dates in the far past or future.
- Talk to people: support staff, operators, long-tenured users. They know the workarounds the system depends on.

**Write it down as you go**: a short living note of entry points, data flows, surprises, and open questions. This becomes the shared map for everyone after you.

See `explore-codebase` for general code-reading technique.

### Step 3: Pin down behaviour with characterization tests

A characterization test records what the code *does*, not what it *should* do. You write it by calling the code, observing the output, and asserting that output.

How to write them:

1. Pick the unit you are about to change (a function, an endpoint, a batch job).
2. Write a test that calls it with realistic input and asserts something obviously wrong (e.g. `assert result == "PLACEHOLDER"`).
3. Run it; the failure tells you the actual output. Paste that into the assertion.
4. Repeat for edge cases: empty input, nulls, boundaries, unusual characters, large values, the weird cases you found in the database.
5. Use coverage tools to find branches you have not exercised, and add inputs until the code you will touch is covered.

Techniques that scale:

- **Golden master / approval testing**: run a large set of inputs through the system, store all outputs as files, and diff future runs against them. Excellent for report generators, pricing engines, and transformations. Scrub non-determinism (timestamps, IDs, ordering) before comparing.
- **Traffic capture and replay**: record real requests and responses (sanitized) and replay against the new version. Strongest evidence for API-level behaviour.
- **Database snapshot comparison**: run a batch against a copy of production data with old and new code, then diff resulting tables.

Rules:

- When a characterization test reveals a bug, do not fix it in the same change. Record it (a comment on the test, a ticket), keep the assertion matching current behaviour, and decide separately whether fixing it is safe.
- Never run characterization against production data without sanitizing personal and sensitive fields, and never write test fixtures containing real customer data into the repository.
- Characterization tests are often ugly and slow. That is fine; they are scaffolding. Replace them with intent-revealing tests once the area is understood.

### Step 4: Find or create seams

A seam is a place where you can change behaviour without editing the code at that place: you substitute something at the boundary instead. Seams make legacy code testable and replaceable.

Common seams, from least to most invasive:

| Seam | How it works | Good for |
|---|---|---|
| Configuration / feature flag | Behaviour switched by config | Routing between old and new paths |
| Link / module seam | Swap an implementation at import, link, or DI-container level | Replacing a dependency in tests |
| Object seam | Pass a dependency in (parameter, constructor) instead of constructing it inside | Isolating I/O for unit tests |
| Subclass-and-override | Override a method in a test subclass | Breaking a dependency in a class you cannot yet restructure |
| Network / process seam | Proxy, gateway, or queue in front of a component | Strangler fig at service level |
| Data seam | View, trigger, or change-data-capture on a table | Migrating data ownership |

Dependency-breaking moves that are safe even without tests (because they are mechanical and tool-assisted): extract method, introduce parameter, extract interface, wrap a static/global call in an instance method. Use automated refactoring tools where the language has them; hand-edits are where regressions creep in.

For adding new behaviour to untested code:

- **Sprout**: write the new logic as a new, tested function or class and call it from the old code with a one-line change.
- **Wrap**: rename the old function, create a new one with the old name that calls the old one plus the new behaviour.

Both keep the untested footprint of your change to a line or two.

### Step 5: Choose a migration strategy

| Strategy | How | Choose when | Main risk |
|---|---|---|---|
| **Refactor in place** | Improve structure incrementally inside the existing system | Platform is fine; code is the problem | Slow; needs discipline to keep going |
| **Strangler fig** | Put a routing layer in front; move one capability at a time to the new system; retire old pieces as traffic moves | Replacing a system with many capabilities | Routing layer complexity; long dual-running period |
| **Branch by abstraction** | Introduce an abstraction inside the codebase; implement new version behind it; switch; delete old | Replacing a component inside one codebase (e.g. ORM, logging, storage layer) | Abstraction leaks old assumptions |
| **Parallel run / shadow** | Run old and new on the same input; compare; old remains authoritative | Calculations where correctness is critical (billing, payroll, pricing) | Cost of running both; noisy diffs |
| **Lift and shift** | Move as-is to new infrastructure | Infrastructure deadline, code is acceptable | Carries all old problems along |
| **Rewrite** | Build new, cut over | Very small system, or old platform truly unrunnable, *and* behaviour is well specified | Hidden requirements, moving target, no value until done |

Heuristics:

- Default to strangler fig or branch by abstraction. Choose a rewrite only when you can list the system's behaviour completely and the system is small enough to rewrite in a few weeks.
- Pick the first slice for learning, not for value: something real but low-risk, with clear boundaries, that exercises the full path (routing, data, deploy, monitoring). Then do the high-value slices.
- Define the retirement criterion for each old piece up front (e.g. "zero traffic for 30 days, then delete"). Strangler migrations that never delete the old path end up with two systems forever.

### Step 6: Handle the data

Data is usually the hardest part. Code can be routed; data has one source of truth at a time.

- Decide who owns each piece of data at each phase. Two systems writing the same records is the most dangerous state; keep it short and explicit.
- Patterns: old system stays the writer and the new system reads (via replica, view, or change-data-capture) → dual-write with reconciliation → new system becomes writer and syncs back to old for remaining consumers → old consumers migrate → sync removed.
- Run reconciliation jobs that compare both sides and report differences. Do not trust dual-write without them; partial failures make the copies drift.
- Legacy data is dirtier than the schema says. Profile it before designing the new schema: actual null rates, actual value ranges, encoding problems, duplicate "unique" keys, orphaned foreign keys.
- See `database-migrations` for safe schema evolution and backfills.

### Step 7: Framework, runtime, and language upgrades

Large version jumps are their own kind of migration.

1. **Inventory**: current versions of runtime, framework, and every direct dependency; target versions; their compatibility matrix. Find which dependencies block the upgrade (abandoned libraries are the usual blocker).
2. **Read the upgrade guides for every intermediate major version.** Skipping versions skips deprecation warnings that explain what will break.
3. **Step through majors one at a time** where the ecosystem supports it. Each step: upgrade, fix, run full tests, deploy. A jump from version 2 to 6 in one go makes every failure ambiguous.
4. **Turn on deprecation warnings** and fix them on the current version before upgrading; most ecosystems warn one major ahead.
5. **Use automated migration tools** (codemods, rewrite tools, official upgrade assistants) for mechanical changes, then review the diff; they are fast but not always right.
6. **Replace abandoned dependencies before the upgrade**, behind a seam, as a separate change.
7. **Watch for silent semantic changes**: default encodings, integer division, date and time zone handling, sort stability, null handling, regex dialects, floating-point formatting. These do not fail to compile; they produce different answers. Characterization tests catch them.
8. **Keep both versions buildable** for a while if possible (a CI job on the new version that is allowed to fail at first), so the upgrade can proceed in parallel with feature work.

For language-to-language migrations, prefer running both side by side through a seam (service boundary, FFI, shared runtime) and moving module by module. Machine translation of whole codebases tends to produce code that is unidiomatic in the target language and still needs every hidden requirement re-verified.

### Step 8: Ship safely

- Use feature flags or routing rules to move traffic gradually: internal users → small percentage → larger → all. Watch error rates, latency, and business metrics (orders, payments) at each step, not just technical health.
- Keep the old path deployable and switchable for the whole rollout. Rollback should be a config change, not a redeploy of old code.
- Agree in advance on the metrics and thresholds that trigger rollback.
- Coordinate with consumers you discovered in Step 2. Undocumented consumers are found by deprecation notices, access logs, and, too often, by breaking them.
- See `release-management` for rollout mechanics and `observability` for what to monitor.

## Prioritizing what to modernize

You will never modernize everything, and you should not try. Rank candidate areas by:

- **Change frequency**: how often does this area need to change? (From version history and the backlog.)
- **Change cost**: how long do changes take, and how often do they cause incidents?
- **Business criticality**: what breaks, and for whom, if this area fails?
- **Platform risk**: is it on an unsupported runtime, a vendor going EOL, or hardware that cannot be replaced?
- **Knowledge risk**: does understanding live in one person's head?

High frequency × high cost is where improvement pays back fastest. High platform risk is where deadlines come from. Low frequency × low criticality is where you leave the code alone, however ugly it is, and write a note so the next person does not waste time on it.

## Common legacy obstacles and responses

| Obstacle | Response |
|---|---|
| Giant function (thousands of lines) | Characterize at its boundary; extract pure sub-computations first (they are easy to test); leave I/O-heavy parts for later |
| Global mutable state | Wrap access in a single accessor so you can see and later replace every read/write; then pass state explicitly where you are working |
| Business logic in stored procedures or triggers | Treat the database as a component with its own tests (run procedures against a test database); migrate logic out one procedure at a time via a seam in the calling code |
| Code that only runs on a specific server | Reproduce the environment in a container or VM first; you cannot modernize what you cannot run |
| Copy-pasted variants of the same logic | Characterize each copy; they have usually diverged deliberately in small ways. Consolidate only after confirming which differences matter |
| Dead languages / tooling with no developers | Wrap at a process or service boundary and replace behind it, rather than editing in place |
| Missing source code (only binaries) | Treat as a black box: characterize inputs and outputs exhaustively; replace behind a seam |
| Configuration spread across files, database, and environment | Build an inventory of every setting and its effective value per environment before changing deployment |

## Worked example: replacing a pricing module

Illustrative only; the shape matters more than the specifics.

A ten-year-old order system computes prices in a 3,000-line module with no tests. The business wants a new discount rule, and the team wants to move pricing into its own service eventually.

1. **Archaeology.** Version history shows the module changes monthly (hot spot). Logs show four call sites, one of which is a nightly invoice batch nobody mentioned. The database has orders with negative quantities (returns, handled by a special branch).
2. **Characterization.** Pull 50,000 historical orders (sanitized), run them through the current module, and store inputs and outputs as a golden master. Coverage shows the returns branch and a currency-rounding branch are exercised; a "legacy coupon" branch is never hit by recent data, so hand-craft inputs for it.
3. **Seam.** The module is called directly from four places. Introduce a single `PriceCalculator` interface whose first implementation just delegates to the old code (structural commit, no behaviour change, golden master still matches).
4. **Feature via sprout.** Implement the new discount rule as a new, unit-tested component invoked from the delegating implementation behind a flag. Golden master still matches with the flag off; new tests cover flag on.
5. **Branch by abstraction.** Write the new implementation behind the same interface. Run both in shadow on live traffic, logging differences. The diffs reveal a rounding rule (banker's rounding for one currency) nobody had documented; reproduce it.
6. **Cutover.** When differences are zero for two full billing cycles (including month-end), switch the flag for 5% of traffic, then 50%, then 100%. Keep the old implementation for one more cycle, then delete it.
7. **Later**, extracting the new implementation into its own service is now a deployment change behind an already-stable interface, not a rewrite.

Notice what did not happen: no big rewrite, no bug fixes mixed into the migration, no cutover without evidence, and at every step the system was shippable.

## When there is no time for any of this

Sometimes you must make a change to untested legacy code today. Minimum safe practice:

- Make the smallest possible change. Prefer sprout or wrap so the edit to old code is one or two lines.
- Write at least one characterization test for the exact path you touch, even a crude end-to-end one.
- Manually exercise the change against a realistic environment, including one unhappy path.
- Ship behind a flag if the system has flags; otherwise, ship alone (not bundled with other changes) so rollback is clean.
- Record what you did not verify, and create a follow-up item to add proper tests. Tell the user plainly what the residual risk is.

## Using automated assistance on legacy code

Code-generation and automated refactoring tools are useful for archaeology (summarizing modules, tracing call graphs, drafting characterization tests) and for mechanical transformations. Treat their output on legacy systems with extra suspicion: they tend to "correct" odd-looking code toward the common idiom, which is exactly how hidden requirements are lost. Every generated change must pass the same characterization and parity checks as a human one, and generated explanations of what code does must be confirmed by running it.

## Communicating the plan

Legacy modernization usually needs sustained buy-in from people who will not read the code.

- Frame each phase by the risk it removes or the capability it unlocks, not by technical tidiness.
- Give estimates as ranges and say what discovery could widen them; legacy work has fat-tailed uncertainty. See `estimate-effort`.
- Show progress in terms of retired surface area (endpoints moved, jobs migrated, old code deleted), which is more meaningful than lines of new code.
- Surface decisions that need an owner: preserving vs. fixing a discovered bug, retiring a little-used feature, accepting a dual-running cost.

## Risk management

Legacy work fails through accumulated small risks. Track them explicitly.

- **Risk register**: unknown consumers, undocumented jobs, data quality, key-person dependencies, vendor EOL dates, compliance constraints. Review it at each phase.
- **Blast radius**: for each change, ask what the worst outcome is and how many users or records it touches. Higher blast radius → more feedback before shipping (shadow, canary, reconciliation).
- **Reversibility**: classify each step as reversible (code behind a flag), slow to reverse (schema change), or irreversible (data deletion, external notification sent, contract cut over). Irreversible steps need explicit sign-off from the user or owner, a backup, and a rehearsal.
- **Stop points**: plan the migration so that you could stop after any phase and still have a coherent, supported system. Programmes get cancelled; leave no half-migrated states that are worse than the start.

## Discovering context

Before acting in a legacy codebase:

- Find out who owns it and who has changed it recently; ask them about known landmines.
- Identify the build, test, and deploy commands that actually work today. If the tests do not pass on a clean checkout, record which fail before you change anything, so you do not later blame yourself (or get blamed) for pre-existing failures.
- Match the existing code style in the files you touch, even if it is dated. A modernization that also reformats everything makes review impossible. Do formatting as its own mechanical commit, if at all.
- Check for constraints that are not in the code: regulatory retention rules, audit requirements, contractual file formats, hardware dependencies, licence restrictions.
- Find whether a migration has been attempted before. Half-finished previous attempts are common; learn why they stalled.

## Pitfalls

- **The rewrite trap**: estimating the rewrite from the visible features and missing the hidden ones. Symptom: the new system is "90% done" for months.
- **Fixing bugs during migration**: changes the contract mid-flight and makes diffs between old and new uninterpretable. Log them; fix after parity.
- **Modernizing cold code**: spending effort on ugly modules that never change. Prioritize by change frequency × pain.
- **Abstraction that mirrors the old mess**: branch-by-abstraction interfaces shaped exactly like the old implementation, so the new implementation inherits its constraints. Design the interface around what callers need.
- **Permanent dual-running**: no retirement criteria, so the old path never dies and everyone maintains two systems.
- **Trusting the README**: the documented build, config, or architecture is out of date. Verify against what actually runs.
- **Assuming tests exist means tests protect you**: legacy tests may assert little, be skipped, or mock away the behaviour that matters. Check what they actually verify.
- **Deleting "dead" code too eagerly**: reflection, dynamic dispatch, config-driven loading, external callers, and annual jobs make code look dead when it is not. Confirm with runtime evidence over a full business cycle, or put it behind a logging tripwire before deleting.
- **Big-bang data cutover** without rehearsal on production-sized data.
- **Ignoring the people**: operators and users have built workflows around quirks; changing them without warning causes support load even when the change is "correct".

## Quality bar and verification

Before declaring a modernization step done:

- Characterization or parity tests covering the changed area pass, and you have checked they would fail if the behaviour changed (break something deliberately once to see).
- Structural and behavioural changes are in separate commits.
- For migrations: old and new produce the same results on representative real-world input (golden master, shadow, or reconciliation), with differences explained and approved.
- The rollback path has been tested, not just described.
- No sensitive production data has been copied into fixtures, logs, or the repository.
- Notes on what you learned (entry points, surprises, decisions) are recorded where the team will find them.
- Retirement criteria for anything left running in parallel are written down.

When reporting back, say clearly which behaviours were verified, which were assumed, which known bugs were deliberately preserved, and what risks remain.
