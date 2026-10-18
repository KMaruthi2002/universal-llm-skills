---
name: root-cause-analysis
description: >-
  Explain why something went wrong in a system, process, product, or
  business and identify causes that, if addressed, prevent recurrence:
  scoping the problem precisely, building an evidence-based timeline,
  generating and testing hypotheses, using 5 whys, fishbone (cause-and-effect)
  diagrams, fault trees, and change analysis appropriately and knowing their
  limits, distinguishing triggers, contributing factors, and systemic causes,
  and turning findings into verifiable corrective actions. Use when asked
  "why did this happen", "find the root cause", "what caused the drop / spike
  / failure / outage / defect", for recurring problems, quality escapes,
  metric anomalies, process breakdowns, or missed targets. For live outages
  use incident-response first; for code-level bugs use debugging; for the
  blameless write-up use postmortem.
metadata:
  category: analysis
  related: debugging, incident-response, postmortem, observability, data-analysis, statistical-analysis, experiment-design, technical-decision-making
---

# Root Cause Analysis

Root cause analysis (RCA) answers "why did this happen, and what must change so it does not happen again?" The hard part is not generating explanations — people produce those instantly — but finding the explanation the evidence actually supports, at the level where a fix will prevent recurrence rather than patch one symptom.

## Scope

Covers: causal investigation of failures and anomalies in technical systems (outages, data errors, performance regressions), processes (quality escapes, missed handoffs, compliance lapses), products (adoption drops, support spikes), and businesses (missed targets, metric shifts).

Does not cover:

- Stabilising a live incident → `incident-response` (RCA comes after the bleeding stops; keep evidence while responding).
- Finding a defect in code → `debugging` (RCA may lead there, and debugging may reveal a deeper process cause).
- Writing and running the review meeting and document → `postmortem`.
- Testing a causal claim with a controlled experiment → `experiment-design`.
- Statistical tests on whether a metric change is real → `statistical-analysis`.

## Core principles

1. **Define the problem before explaining it.** A precise statement of what happened, where, when, how much, and compared to what expectation constrains the possible causes dramatically. *Why:* vague problems ("the system is unreliable") admit any explanation, so the investigation drifts toward the investigator's prior beliefs.

2. **Evidence over narrative.** A coherent story is not proof. Every causal link in the explanation should be supported by data, logs, records, reproduction, or testimony that can be checked. *Why:* humans find plausible narratives compelling and stop looking once one fits, even when it is wrong.

3. **There is rarely one root cause.** Most significant failures result from several conditions coinciding: a latent weakness, a trigger, and the absence or failure of defences. *Why:* naming a single cause ("human error", "the bad deploy") stops the analysis at the most visible link and leaves the other conditions in place to combine again.

4. **Ask why the system allowed it, not who did it.** People's actions are shaped by the tools, information, incentives, time pressure, and procedures around them. If a reasonable person in that position could have made the same choice, the cause lies in the system. *Why:* blame suppresses honest information, and replacing the person does not change the conditions that led to the action.

5. **A cause is useful only if addressing it would change the outcome.** Test candidate causes counterfactually: if this factor had been absent, would the problem have occurred? *Why:* investigations often list everything that was imperfect; only factors that mattered deserve corrective action.

6. **Fixes must be verifiable.** Corrective actions should be specific, owned, and checkable, and their effect should be measured. *Why:* "improve communication" and "be more careful" change nothing, and untracked actions are quietly dropped.

## Vocabulary

Terms vary across fields; agree on usage with the team. A useful set:

| Term | Meaning | Example (data pipeline produced wrong totals) |
|---|---|---|
| Symptom / problem | The observed deviation | Dashboard revenue 12% low for three days |
| Trigger / proximate cause | The event that immediately set it off | An upstream schema change renamed a column |
| Mechanism | How the trigger produced the symptom | The join silently dropped rows with null keys |
| Contributing factors | Conditions that made it possible or worse | No schema contract; no row-count check; alert thresholds too loose |
| Root / systemic causes | The deepest causes within your ability to change that, if fixed, would prevent this class of problem | No process for coordinating schema changes across teams; data quality checks not part of pipeline standards |
| Detection gap | Why it was not noticed sooner | Finance noticed manually; no automated reconciliation |

Two common confusions: the trigger is not the root cause (it is often a normal, unremarkable event), and a root cause should be something you can act on — "gravity" and "users make mistakes" are true but not useful stopping points.

## Process

### 1. Stabilise and preserve evidence

If the problem is ongoing, contain it first (see `incident-response`). While doing so, preserve what will be needed later: logs (before rotation), metrics at full resolution, configuration states, deploy and change records, chat transcripts, tickets, samples of affected data or products, and people's fresh recollections. *Why:* evidence decays fast, and the act of fixing often destroys it.

### 2. Define the problem precisely

Describe it in specifics. A helpful contrast is *is / is not*: for each dimension, what was affected and what comparable thing was not.

| Dimension | Is | Is not (but could have been) |
|---|---|---|
| What | Checkout API errors | Search and browse APIs |
| Where | Region A, mobile clients | Region B; web clients |
| When | From 14:05, after the 14:00 deploy; worst at peak | Before 14:00; the previous peak |
| Extent | 8% of requests, all payment methods | Not all requests; not a full outage |

The "is not" column is powerful: any proposed cause must explain why the affected things were affected *and* why the unaffected ones were not. Then ask what changed in the "is" area that did not change in the "is not" area.

Also state the expected behaviour and how large the deviation is. For business metrics, establish that the change is real (beyond normal variation, not a measurement change) before searching for causes — see `statistical-analysis` and `data-analysis`. A surprising number of "drops" are instrumentation changes, definitional changes, seasonality, or mix shifts.

### 3. Build a timeline

Construct a timeline of what happened, from the earliest relevant precondition to resolution. Include: changes (deploys, config, data, people, process, vendor, market), events (alerts, errors, customer reports), decisions and actions taken, and what people knew at each point.

- Use timestamps from systems where possible; reconcile time zones and clock differences.
- Distinguish facts (logged) from recollections (reported) and mark gaps.
- Note when information was available versus when it was noticed — the gap is often part of the cause.
- Look backward further than feels necessary. Latent conditions are often created weeks or months before the trigger.

The timeline is the backbone. Most wrong conclusions in RCA come from getting the order of events wrong or not knowing about a change.

### 4. Generate hypotheses broadly

Before testing anything, generate a wide set of candidate explanations. Sources:

- **Change analysis.** What changed shortly before the problem? Code, configuration, infrastructure, data, dependencies, traffic, people, processes, suppliers, policies, external environment. Problems that start at a specific time almost always correlate with some change.
- **Is / is not differences.** What distinguishes affected from unaffected cases?
- **Category prompts** (the fishbone idea, below), to avoid fixating on one area.
- **Prior incidents and known failure modes** of the system.
- **People closest to the work**, who often know which weaknesses exist.

Write hypotheses as testable statements with a predicted consequence: "If the connection pool was exhausted, we would see wait-time spikes in pool metrics and errors only on instances with the new pool size."

### 5. Test hypotheses against evidence

For each hypothesis, ask what evidence would support it and what would refute it, then look. Prefer the cheapest decisive test.

| Test | Strength | Notes |
|---|---|---|
| Reproduction under controlled conditions | Very strong | Reintroduce the suspected cause in a safe environment and see the symptom appear; remove it and see it go |
| Natural experiment / comparison | Strong | Affected vs. unaffected units differing mainly in the suspected factor |
| Timing and dose correlation | Moderate | Symptom starts with the change and scales with exposure; still vulnerable to coincidence |
| Mechanistic explanation consistent with logs and metrics | Moderate to strong | Must explain the full is/is-not pattern |
| Testimony and recollection | Weak to moderate | Valuable for context and decisions; corroborate where possible |
| Plausibility alone | Weak | A starting point, not a conclusion |

Eliminate hypotheses the evidence refutes, and keep track of those that remain consistent. Be wary of the first hypothesis that fits — check whether others also fit. When you cannot test, say so and record the explanation as probable, not established.

For production systems, test safely: reproduce in non-production environments, use read-only queries, and get approval before any test that could affect users or data.

### 6. Trace the causal chain to systemic causes

Once the mechanism is established, push past it. For each established cause, ask why it existed and why defences did not stop it. This is where 5 whys, fishbone, and fault trees come in — see the next section. Stop at causes that are actionable and within the organisation's control, and where fixing them would prevent a class of problems, not just this instance.

Also analyse **detection and response**: why was the problem not caught earlier, and what slowed recovery? These are often the highest-leverage fixes, because preventing every failure is impossible but shortening their impact is achievable.

### 7. Decide corrective and preventive actions

For each significant cause, consider actions across a hierarchy of effectiveness:

| Level | Example | Effectiveness |
|---|---|---|
| Eliminate the hazard | Remove the dangerous manual step entirely; make the invalid state unrepresentable | Highest |
| Engineer a safeguard | Automated validation, contract tests, rate limits, guard rails, safe defaults, interlocks | High |
| Detect and contain | Alerts, canaries, reconciliation checks, circuit breakers, fast rollback | Medium–high |
| Procedure and documentation | Checklists, runbooks, review requirements | Medium; decays without reinforcement |
| Training and reminders | "Be more careful", awareness sessions | Low on their own |

Prefer higher levels. Use lower levels as complements, not as the whole answer.

Each action should state: what will change, who owns it, by when, and how you will know it worked (a test, a metric, an audit). Prioritise by risk reduction per effort; a few completed high-value actions beat a long list of aspirational ones.

### 8. Verify and close

- Confirm the fix addresses the established mechanism (reproduce the original failure against the fixed system where possible).
- Monitor for recurrence over a period that would have shown it.
- Check that actions were actually completed.
- Share the learning beyond the team where the same weakness may exist.

## Tools and their limits

### 5 whys

Ask "why?" repeatedly from the problem toward its causes. It is fast, needs no special tools, and pushes past the obvious first answer.

Limits, and how to compensate:

- **It produces a single chain.** Real failures have branches. Ask "why?" of each contributing factor, not just the most visible one, and draw the result as a tree.
- **It depends on what the group knows.** Unknown causes cannot appear. Support each answer with evidence, not opinion.
- **It can stop arbitrarily** — at "human error" or at whatever the group feels comfortable fixing. Stop by criterion (actionable, systemic, within control), not by count. Five is a rough guide, not a rule.
- **It can jump levels or wander.** Each "because" should be a direct cause of the previous statement. Check by reading the chain backwards with "therefore".
- **Different groups produce different chains.** That is a sign the evidence is weak; return to step 5.

Illustrative chain with branching:

- Customers were charged twice. *Why?* The payment request was retried after a timeout.
- *Why did a retry charge again?* The payment call was not idempotent. *Why?* The integration did not pass an idempotency key, and the review checklist did not cover it. *Why?* No integration standard existed for external payment calls.
- *Why did the timeout happen?* The provider was slow under load, and our timeout was shorter than their documented p99.
- *Why was it not caught sooner?* No alert on duplicate charges; detected from customer complaints after two days.

Each branch yields different actions: idempotency standard (eliminates the class), timeout configuration review (reduces trigger frequency), duplicate-charge detection (shortens impact).

### Fishbone (cause-and-effect / Ishikawa) diagram

The problem is the head; major cause categories are the bones; specific candidate causes hang off each. Classic manufacturing categories are people, methods, machines, materials, measurement, and environment; for software and services, useful categories include code, configuration, infrastructure, dependencies, data, process, people and skills, monitoring, and external factors. Choose categories that fit the domain.

Use it to **generate** hypotheses broadly and avoid fixating on one area. It does not show causal order, interactions, or evidence; every item on it is a candidate until tested. Do not mistake a full fishbone for an analysis.

### Fault tree analysis

Starting from the top-level failure, decompose it into the combinations of lower-level events that could produce it, using logic gates: AND (all inputs needed) and OR (any input sufficient). Continue down to basic events.

Strengths: makes combinations explicit, shows which single failures are sufficient (single points of failure) and which require coincidences, and supports quantitative reasoning when failure probabilities are known. Useful for safety-critical systems and for designing defences. Limits: time-consuming, requires good system knowledge, and weak at modelling human and organisational factors or timing.

### Change analysis

Compare the situation where the problem occurred with a similar one where it did not, and list every difference; then ask which differences could produce the symptom. Particularly effective for "it used to work" problems. Pair with the timeline.

### Barrier analysis

List the defences that should have prevented the problem or limited it (reviews, tests, validations, alerts, access controls, approvals). For each, ask: did it exist, did it work, and if not, why? Shows why "the bad change" made it all the way through. The "Swiss cheese" idea — failures occur when holes in several layers of defence line up — is a useful mental model here.

### Choosing a tool

| Situation | Good fit |
|---|---|
| Quick, simple, low-stakes issue | 5 whys with evidence, branching where needed |
| Unclear cause, many possible areas | Is/is-not + fishbone to generate, then tests |
| Problem started at a specific time | Timeline + change analysis |
| Failure required several things to go wrong | Barrier analysis, fault tree |
| Safety-critical or high-consequence system | Fault tree, formal methods of the domain, independent review |
| Business metric moved | Data decomposition (by segment, channel, cohort, funnel step), change analysis, then causal testing |
| Recurring problem across many instances | Pareto analysis of categories, then deep dives on the top few |

Many investigations combine them: the timeline and change analysis find the trigger; tests confirm the mechanism; 5 whys and barrier analysis reach systemic causes.

## Business and metric RCA

When the "problem" is a number (revenue down, churn up, conversion fell), extra steps apply:

1. **Verify the measurement.** Was there a tracking change, a definition change, a data pipeline delay, a bot-filter update, a currency or time-zone change? Check before anything else.
2. **Check expected variation.** Seasonality, day-of-week effects, holidays, prior-year comparisons, and normal noise. Is the movement outside the usual range?
3. **Decompose.** Break the metric into components (e.g. revenue = customers × conversion × order value) and by segment (region, channel, device, plan, cohort, new vs. returning). Find where the change is concentrated. Beware mix shifts: an overall rate can fall even when every segment improves, if the mix moves toward lower-rate segments.
4. **Line up with changes.** Product releases, pricing, marketing spend, competitor moves, outages, policy changes, external events.
5. **Test causal claims** where possible: holdouts, staged rollbacks, comparisons with unaffected markets, or experiments (`experiment-design`). Correlation with a release date is a hypothesis, not a conclusion.
6. **Quantify contribution.** If several causes contributed, estimate how much each explains, with uncertainty, and note any unexplained remainder rather than forcing it onto a favourite cause.

## Human factors

When a person's action or decision is part of the chain:

- Reconstruct their situation: what they knew, what the tools showed, what the procedure said, what pressure they were under, what was normal practice. Judge decisions by what was knowable then, not by hindsight.
- Ask whether the error was likely given the design — ambiguous interfaces, missing confirmations, similar-looking commands, alert fatigue, conflicting procedures, understaffing.
- Look for normalised deviance: shortcuts that had become routine because they usually worked.
- Fix the conditions. "Retrain the operator" is rarely sufficient; making the error harder to make, easier to detect, and easier to recover from is.

Keep the analysis blameless in tone and substance. Accountability for completing improvements is compatible with not blaming individuals for system-shaped errors. Handle any genuine misconduct through a separate process; mixing them corrupts the analysis.

## Scaling the effort

Not every problem deserves a full investigation. Scale by impact, recurrence, and how surprising the event was:

| Situation | Appropriate depth |
|---|---|
| Minor, one-off, well understood | Short note: what happened, the fix, whether any cheap safeguard is worth adding |
| Moderate impact, or a repeat of a known issue | Timeline, tested mechanism, 5 whys with branches, a few owned actions |
| High impact, safety, security, legal, or customer-trust consequences | Full process: evidence preservation, structured hypotheses and tests, barrier analysis, independent review, tracked actions, follow-up check |
| Many small similar problems | Aggregate first (categorise and count), then investigate the largest categories in depth |

A surprising event deserves more depth than its impact alone suggests, because surprise means the team's model of the system was wrong — and that model will be wrong again.

## Presenting the findings

Lead with a short summary a non-specialist can follow: what happened, the impact, the main causes in plain language, and the most important actions. Then give the evidence: timeline, mechanism, how alternatives were ruled out, contributing and systemic causes, detection gaps, and the full action list. State confidence explicitly for each causal claim, and list open questions. Keep the format consistent with the organisation's existing reports (see `postmortem` for the review document and meeting).

## Discovering context

- **The organisation's RCA practice**: existing templates, severity criteria, review forums, action trackers, terminology. Fit into them rather than inventing a parallel process.
- **Available evidence sources**: logging, metrics, tracing (`observability`), change management records, ticket systems, data warehouses, quality records.
- **Stakeholders and sensitivities**: who was involved, who is affected, any legal, regulatory, or customer-communication obligations (some incidents have reporting deadlines; check before sharing details externally).
- **Prior incidents** with similar patterns; recurrence is itself a finding about the effectiveness of past fixes.

## Working with and without tools

**With access to systems and data:** query logs, metrics, and records directly; reproduce safely in non-production; run decomposition analyses. Use read-only access wherever possible and confirm before any action that changes production state or data. Do not expose secrets or personal data found in logs in the write-up.

**With only descriptions from the user:** reason from the facts given, separate what was reported from what is inferred, list the evidence that would confirm or refute each hypothesis, and tell the user exactly what to check (which logs, which metric breakdown, which comparison). Do not present a likely explanation as established.

## Pitfalls

- **Stopping at the trigger.** "The deploy caused it" — but why could a deploy cause it, and why was it not caught?
- **Stopping at "human error".** Treat human error as the start of the inquiry.
- **Narrative fallacy.** Accepting the first coherent story without testing alternatives.
- **Hindsight bias.** Judging past decisions by information that only became available later.
- **Confirmation bias.** Looking only for evidence of the suspected cause; ignoring the is-not pattern.
- **Single-cause thinking.** One root cause when several conditions were needed.
- **Correlation as causation.** Especially for metrics that moved around the time of a change.
- **Measurement artefacts.** Investigating a "drop" that was a tracking change.
- **Too many causes.** Listing every imperfection; dilutes action. Apply the counterfactual test.
- **Weak actions.** Reminders and training as the only response.
- **Unowned, untracked actions.** The same incident happens again in six months.
- **Destroying evidence** while fixing, or investigating so late that logs are gone.
- **Blame**, explicit or implied, which shuts down the information the analysis needs.
- **Analysis paralysis** for low-impact issues. Scale effort to impact and recurrence risk.

## Quality bar and verification

Before finalising, check:

- [ ] The problem statement is specific (what, where, when, extent, versus expected), with an is/is-not view where useful.
- [ ] For metric problems, the measurement and normal variation were checked first.
- [ ] A timeline exists, with facts distinguished from recollections.
- [ ] Multiple hypotheses were considered; the accepted one explains both affected and unaffected cases.
- [ ] Each causal link is supported by evidence; untested links are labelled as probable.
- [ ] Contributing factors and systemic causes are identified, not just the trigger.
- [ ] Detection and response gaps are analysed.
- [ ] The counterfactual test was applied to each cause listed.
- [ ] Actions favour elimination and engineered safeguards, are owned, dated, and verifiable.
- [ ] The language is blameless; sensitive data is excluded.
- [ ] A plan exists to confirm the fix and watch for recurrence.

A good test: would a skeptical engineer or analyst who was not involved, reading the evidence, reach the same causal conclusion — and would the actions, once completed, have prevented this incident and its close relatives?

## Related skills

- `incident-response` — before RCA, while the problem is live.
- `debugging` — code-level causes.
- `postmortem` — running the review and writing it up.
- `observability` — the evidence sources RCA depends on.
- `data-analysis` and `statistical-analysis` — decomposing and testing metric changes.
- `experiment-design` — confirming causal claims prospectively.
