---
name: estimate-effort
description: >-
  Size work credibly: decompose it, estimate in ranges rather than single
  numbers, account for unknowns, integration, review, and rework, calibrate
  against past data, and communicate confidence and assumptions so others can
  plan around the estimate. Use when asked "how long will this take?", "how
  big is this?", "can we do it by Friday?", for sprint or project sizing,
  quotes, scoping a proposal, comparing options by cost, or deciding whether a
  task fits in the time available. Not for building the step-by-step plan
  (see plan-and-decompose) or prioritizing between initiatives (see
  roadmap-and-prioritization).
metadata:
  category: meta
  related: plan-and-decompose, clarify-requirements, project-management, roadmap-and-prioritization, technical-decision-making, mvp-prototyping
---

# Estimate Effort

An estimate is a forecast under uncertainty, not a promise. Its job is to help someone decide — whether to start, what to cut, when to schedule, which option to pick. Single-number estimates hide the uncertainty that the decision-maker most needs to see, and estimates made without decomposition are mostly optimism. This skill is about producing estimates that are honest, useful, and improve over time.

## Scope

Covers sizing tasks and projects in time, effort, or relative size; expressing uncertainty; and communicating estimates. Applies to software work and to other knowledge work (analysis, writing, research, design).

Does not cover:

- Ordering and structuring the work — see `plan-and-decompose` (the decomposition here reuses it).
- Choosing what to do from a portfolio — see `roadmap-and-prioritization`.
- Ongoing tracking against estimates across a team — see `project-management`.
- Cost of compute or infrastructure — that is a modelling problem (`cloud-architecture`, `spreadsheet-modeling`).

Note for AI agents: when estimating work you will do yourself, your own speed differs from a human's — often much faster on writing and searching, sometimes slower on things requiring waiting, access, or human decisions. Estimate in terms the user cares about (calendar time, their review effort, number of round trips), and separate your work from the parts that depend on people or external systems.

## Core principles

### 1. Estimates are ranges, because the future is

Any non-trivial task has a distribution of possible durations, usually skewed right: it can only finish a little early, but it can finish very late. A range ("3–6 days") communicates this; a point ("4 days") hides it and invites being treated as a commitment. When a single number is demanded, give it with its confidence ("about 5 days; 80% confident under 7").

### 2. Decompose to estimate

People estimate small, concrete tasks far better than large, vague ones. Breaking work into pieces of roughly half a day to two days each and summing (with care) produces better estimates than a gut feel for the whole — and the decomposition reveals forgotten work. The act of decomposing is often more valuable than the number.

### 3. The forgotten work is the biggest error

Most underestimates come not from misjudging the known tasks but from omitting entire categories: integration, testing, edge cases, review cycles, deployment, documentation, migration of existing data, environment setup, waiting for others, and rework after feedback. A checklist of these is the cheapest accuracy improvement available.

### 4. Unknowns get their own treatment

Known work can be estimated; unknown work cannot — but it can be bounded. Separate them. For each significant unknown, either reduce it (a short spike before estimating) or give it an explicit wide range and say what would narrow it.

### 5. Estimate, target, and commitment are different things

The **estimate** is your honest forecast. The **target** is what the business wants. The **commitment** is what you agree to deliver, which should include a buffer appropriate to the cost of missing it. Conflating them — shrinking the estimate to match the target — produces plans that are wrong from the start. If the target is tighter than the estimate, the conversation is about scope, resources, or risk, not about a smaller number.

### 6. Calibrate against reality

Your estimates are biased in a consistent direction (usually optimistic). Compare past estimates with actuals and correct for it. Historical data from similar work beats expert intuition whenever it exists.

## Process

### Step 1: Clarify what is being estimated

Ask (or determine) the essentials before estimating, since each one changes the number substantially:

- **Scope** — what is in and out. Which edge cases, platforms, quality level? Prototype or production? (`clarify-requirements`.)
- **Definition of done** — code merged? Deployed? Documented? Reviewed by legal? Each adds effort.
- **Unit** — effort (person-hours of work) or duration (calendar time until done)? Duration includes waiting, meetings, context switching, and other work; it is typically 1.5–3× effort for a person with other responsibilities.
- **Who does it** — familiarity with the codebase or domain can change effort by a factor of two or more.
- **Purpose** — a rough order of magnitude for a go/no-go decision needs minutes of work; a quote for a client needs hours.

### Step 2: Choose an estimation approach

| Approach | How | Best when |
|---|---|---|
| Analogy | "Similar to feature X, which took N" — then adjust for differences | Comparable past work exists |
| Bottom-up decomposition | Sum estimates of small tasks, add integration and overhead | Work is reasonably well understood |
| Three-point | For each task: optimistic, most likely, pessimistic | Meaningful uncertainty per task |
| Relative sizing | Size relative to reference tasks (points, T-shirt sizes) | Teams with stable velocity data; comparing many items |
| Time-boxed spike, then estimate | Spend a fixed small effort reducing the main unknown first | Uncertainty is too high to estimate responsibly |
| Reference class / historical | Look at the distribution of actuals for similar projects | Large projects; organizations with records |

Combine approaches where stakes are high: if bottom-up and analogy disagree by more than ~50%, find out why before reporting either.

### Step 3: Decompose

Break the work into tasks small enough to estimate with reasonable confidence — typically half a day to two days of effort each for human work. Then run the forgotten-work checklist and add what applies:

- Understanding the existing system / onboarding
- Environment, access, and tooling setup
- Design and decision time; prototyping
- Core implementation
- Edge cases and error handling
- Data migration or backfill for existing records
- Automated tests; fixing what tests reveal
- Integration with other components and services
- Code review, revisions after review
- Documentation, changelogs, user communication
- Deployment, configuration, feature flags, rollout and monitoring
- QA / user acceptance; bug fixes from feedback
- Coordination: meetings, waiting for answers, approvals, dependencies on other teams
- Clean-up: removing old code paths, temporary scaffolding

The non-implementation items commonly total as much as, or more than, the implementation itself.

### Step 4: Estimate each piece with uncertainty

For each task, give a range or a three-point estimate (optimistic *O*, most likely *M*, pessimistic *P*). The pessimistic case should be genuinely pessimistic — "things go wrong in the usual ways", not "everything goes perfectly but a bit slower".

A common way to combine three-point estimates per task is the PERT approximation: expected ≈ (O + 4M + P) / 6, with spread ≈ (P − O) / 6. Use it as a rough tool, not as false precision.

### Step 5: Aggregate carefully

- **Expected values add**; ranges do not simply add. Summing every task's optimistic value gives an absurdly optimistic total; summing every pessimistic value gives an absurdly pessimistic one. For independent tasks, the total's spread grows roughly with the square root of the sum of squared spreads — so the relative uncertainty of the total is smaller than that of each task.
- **But tasks are rarely independent.** If the same misunderstanding affects many tasks (an unexpectedly messy codebase, an unclear requirement), they all run late together. When risks are shared, widen the total range rather than narrowing it.
- **Add integration and coordination overhead** explicitly if not already itemized. Integration effort grows faster than linearly with the number of parts and people.

### Step 6: Account for unknowns and risks

List the main unknowns and, for each, its plausible impact. Choose:

- **Reduce** — spike first, then estimate. Best when the unknown dominates the range.
- **Bound** — give a wide range for that part and state what would narrow it.
- **Contingency** — add a buffer sized to the risk. Typical contingency for well-understood work is 10–25%; for novel work, 50–100% or more is not unusual.
- **Exclude explicitly** — "This estimate assumes the vendor API supports batch writes; if not, add 3–5 days."

### Step 7: Sanity-check

- **Compare to analogies.** Does the total make sense against similar past work?
- **Check the ratio of implementation to everything else.** If implementation is 90% of the estimate, overhead is missing.
- **Check the calendar.** Effort to duration: subtract holidays, other commitments, review latency. Two weeks of effort for someone at 50% allocation is a month.
- **Check the long pole.** Is any single task more than ~a week? It probably hides sub-tasks or unknowns — decompose it further.
- **Run a pre-mortem.** "It's three months later and this took twice as long. Why?" The answers are risks to add or assumptions to state.

### Step 8: Communicate the estimate

A useful estimate includes:

- **The range**, and what confidence it represents ("likely 2–3 weeks; could stretch to 5 if the migration needs a rewrite").
- **What it covers** — the scope and definition of done assumed.
- **Key assumptions** — which, if false, change the number.
- **The main risks and unknowns**, and what you would do to reduce them.
- **Options**, if the estimate exceeds the target: what scope could be cut, what could be phased, what a smaller first slice would cost.

Match precision to certainty. "11.5 days" implies a precision you do not have; "2–3 weeks" is more honest. Use units that fit the scale: hours for small tasks, days for features, weeks or months for projects.

### Step 9: Track and re-estimate

Estimates should change as information arrives. Re-estimate when:

- A spike or early task resolves a major unknown.
- Early tasks overrun by a consistent factor — apply that factor to remaining similar work (early overrun rarely self-corrects).
- Scope changes.

Communicate changes early. A revised estimate delivered at the first sign of slippage is useful; one delivered at the deadline is not. Record actuals against estimates so future estimates improve.

## Worked reasoning: an estimate end to end

Illustration only; numbers are invented. Request: "How long to add single sign-on to our web app?"

**Clarify.** One identity provider or several? Does SSO replace passwords or sit alongside them? Are accounts provisioned automatically? Assume, after asking: one provider, alongside passwords, existing accounts linked by email, no automatic provisioning. Done means: deployed to production behind a flag, documented for support.

**Decompose and estimate (days of effort, O / M / P):**

| Task | O | M | P |
|---|---|---|---|
| Spike: provider's protocol flow in a throwaway app | 0.5 | 1 | 2 |
| Login flow and callback handling | 1 | 2 | 4 |
| Account linking (match by email, handle conflicts) | 1 | 2 | 5 |
| Session and logout integration | 0.5 | 1 | 3 |
| Admin configuration screen | 1 | 1.5 | 3 |
| Tests (unit + one end-to-end) | 1 | 2 | 3 |
| Security review and fixes | 0.5 | 1 | 3 |
| Docs for support, rollout behind flag, monitoring | 0.5 | 1 | 2 |

PERT expected per task sums to roughly 13 days; summing the most-likely values gives 11.5; summing all pessimistic values gives 25.

**Aggregate.** Not 11.5 (that is the most-likely path everywhere, which rarely happens) and not 25 (everything going wrong at once). The tasks share one big risk — the account-linking edge cases and the provider's quirks — so they are not independent; keep the range wide. Reasonable statement: **about 2.5–4 weeks of effort**.

**Convert to duration.** The developer is at roughly 70% availability and security review has a queue of several days. **Roughly 4–6 calendar weeks.**

**Communicate.** "About 4–6 weeks to production behind a flag, for one provider, alongside passwords. The biggest uncertainty is account linking when emails don't match; a 1–2 day spike would tighten the range. Supporting a second provider later adds roughly a week. If we need it sooner, launching to internal users first with manual account linking could cut 1–2 weeks."

Note what makes this useful: scope stated, range with reasoning, effort separated from duration, the main risk named with a way to reduce it, and options for a tighter deadline.

## Calibration practice

Estimators improve only with feedback.

- **Record estimates with their ranges** before starting, along with the assumptions.
- **Record actuals** when done, and note the main cause of any gap: scope change, an unknown that bit, forgotten work, interruptions.
- **Check your hit rate.** If you give 80% ranges, about 80% of actuals should fall inside them. If far fewer do, widen your ranges; if nearly all do with room to spare, you may be padding.
- **Look for systematic bias by category.** Many people are accurate on implementation and consistently low on integration, review cycles, or deployment. Adjust the categories, not just the total.
- **Use team history** where available: throughput per week or sprint, cycle time distributions for similarly sized items. Forecasting from these distributions often outperforms task-by-task estimation for teams with stable processes.

## Decision guidance

### How much effort to put into an estimate

| Purpose | Effort |
|---|---|
| "Is this an hour, a day, or a month?" | Seconds to minutes: analogy and gut, give an order of magnitude |
| Choosing between options | Enough to compare relatively; same method for each option |
| Sprint or near-term scheduling | Decompose to tasks; ranges per task |
| External quote, contract, or major investment | Full decomposition, three-point estimates, risk register, contingency, peer review |

### Responding to pressure

When asked to "just give a number" or to reduce an estimate:

- Give the number with its range and confidence; do not drop the range.
- Ask which constraint is fixed — date, scope, or quality — and offer trade-offs on the others.
- Do not lower an estimate without a change to scope, resources, or approach. Lowering it by negotiation makes the plan wrong, not the work smaller.
- Offer to reduce uncertainty: "Give me a day to spike the migration and I can tighten this range a lot."

### Estimates for unfamiliar or novel work

When nobody has done anything similar:

- Prefer a spike or a thin first slice, then estimate from what you learned.
- Give wide ranges and say plainly why.
- Estimate in phases: firm estimate for the next phase, rough for later phases, re-estimate at each phase boundary.

## Discovering context

- Look for historical data: past tickets with estimates and actuals, commit history for similar features, previous project timelines.
- Learn the team's or user's estimation units and conventions (hours, days, points, T-shirt sizes) and use them.
- Find the real constraints: deadlines and why they exist, availability of the people involved, review and release cadences that add calendar time.
- Check for known sources of drag: flaky test suites, slow deploys, approvals, shared environments.

## Pitfalls and anti-patterns

- **Point estimates.** Hide uncertainty; get treated as commitments. Fix: ranges with confidence.
- **The implementation-only estimate.** Omits testing, review, deployment, migration, coordination. Fix: forgotten-work checklist.
- **Anchoring.** Adjusting toward a number someone mentioned first ("this should be a quick one, right?"). Fix: estimate independently before hearing targets; decompose.
- **Planning fallacy.** Imagining the best-case path. Fix: genuine pessimistic cases; reference class; pre-mortem.
- **Effort reported as duration.** Five days of work reported as "done by Friday" for someone with meetings and other work. Fix: convert explicitly.
- **Negotiated estimates.** Shrinking the number to fit a target without changing scope. Fix: separate estimate, target, and commitment.
- **False precision.** "37 hours." Fix: round to the precision of your confidence.
- **Ignoring early overrun.** Assuming the next tasks will make up time. Fix: apply the observed factor to the remainder.
- **Estimating someone else's work without them.** Fix: involve the people who will do it, or state that the estimate assumes a given familiarity.
- **Silent re-estimation.** Letting a deadline slip without updating anyone. Fix: re-estimate and communicate at the first strong signal.

## Verification

Before giving an estimate, check:

- [ ] Scope, definition of done, and units (effort vs. duration) are stated.
- [ ] The work is decomposed into pieces small enough to estimate, with the forgotten-work categories considered.
- [ ] The estimate is a range (or a point with confidence), with precision matching certainty.
- [ ] Major unknowns are identified and either reduced, bounded, or explicitly excluded.
- [ ] Shared risks are reflected in the total range rather than averaged away.
- [ ] The result passes an analogy check and a calendar check.
- [ ] Assumptions, risks, and options (if over target) are communicated with the number.
- [ ] There is a plan to re-estimate when key unknowns are resolved.
