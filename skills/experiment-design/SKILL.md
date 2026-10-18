---
name: experiment-design
description: >-
  Design, run and interpret controlled experiments — A/B tests, multivariate
  and multi-arm tests, holdouts — and quasi-experiments when you cannot
  randomize: write a falsifiable hypothesis, choose primary, secondary and
  guardrail metrics, pick the randomization unit, compute power, sample size
  and duration, avoid peeking, sample-ratio mismatch and novelty effects, and
  read results honestly. Use when someone wants to "A/B test", "run an
  experiment", "split test", "measure the impact of a change", asks how long a
  test should run or how many users it needs, wants experiment results
  interpreted, or needs a difference-in-differences or other causal design
  from observational data. Not for general statistics questions
  (statistical-analysis) or exploratory metric analysis (data-analysis).
metadata:
  category: analysis
  related: statistical-analysis, data-analysis, product-requirements, observability, llm-evaluation, roadmap-and-prioritization
---

# Experiment Design

A controlled experiment is the most reliable way to learn whether a change causes an outcome. Randomly assigning units to versions makes the groups comparable in every respect except the change, so differences in outcomes can be attributed to it. That guarantee is powerful and fragile: it is broken by the wrong randomization unit, by peeking at results, by measuring the wrong thing, by bugs in assignment, and by interpreting noise. Most of the value of experimentation comes from the discipline before launch and the honesty after it.

## Scope

This skill covers online and offline controlled experiments (product, marketing, pricing, operations, model and prompt changes) and quasi-experimental designs. Neighbours:

- `statistical-analysis` — the underlying tests, intervals and corrections.
- `data-analysis` — observational investigation and causal reasoning without a designed comparison.
- `llm-evaluation` — offline evaluation of model outputs; online tests of LLM features use this skill.
- `product-requirements` and `roadmap-and-prioritization` — deciding what is worth testing.
- `observability` — monitoring the system health metrics that often serve as guardrails.

## Core principles

### 1. Decide before you look

Write down the hypothesis, the primary metric, the minimum effect worth detecting, the sample size, the duration and the decision rule *before* the experiment starts. **Why:** after seeing data, every choice (which metric, which segment, when to stop) can be bent toward the result you hoped for, and you will not notice yourself doing it. Pre-registration — even an informal note in the ticket — is the cheapest protection against fooling yourself.

### 2. Randomize at the level where the effect happens, and analyse at that level

The unit of randomization (user, session, device, account, store, region) must match how the treatment is experienced and must be the unit used to compute variance. **Why:** if a user sees both versions across sessions, effects bleed together; if you randomize by account but count by user, standard errors are too small and false positives soar.

### 3. One primary metric decides; guardrails protect

Pick one primary metric that captures success for this change. Add guardrail metrics that must not get worse (revenue, latency, error rate, unsubscribes, complaints). Secondary metrics help explain *why*. **Why:** with many metrics and no hierarchy, some will move by chance, and the team will cite whichever ones moved favourably.

### 4. Power is decided in advance, not hoped for

An underpowered test cannot detect realistic effects; its "no significant difference" is uninformative, and its significant results are exaggerated (when underpowered tests are significant, the estimated effect is usually inflated — the "winner's curse"). **Why:** without a power calculation you do not know whether the test can answer the question at all.

### 5. Trust the plumbing before the result

Before reading outcome metrics, verify assignment: the split matches the design (sample ratio), units are not in both groups, the treatment actually rendered, and logging is equal across arms. **Why:** a large share of surprising experiment results turn out to be implementation bugs; a sample-ratio mismatch invalidates the comparison regardless of the p-value.

### 6. Most ideas do not work

In mature products, a large fraction of experiments — often well over half — show no meaningful improvement. **Why it matters:** the prior probability of a large win is low, so an unexpectedly large effect is more likely a bug or noise than a breakthrough. Scrutinise big wins hardest (Twyman's law: any figure that looks interesting or different is usually wrong).

## Process

### Step 1 — Decide whether an experiment is the right tool

Run a controlled experiment when: the change is under your control, you can randomize, the outcome is measurable within a reasonable time, you have enough traffic, and being wrong is costly. Consider alternatives when:

| Situation | Better approach |
|---|---|
| The change is required anyway (legal, security, bug fix) | Ship; monitor; maybe a holdout to measure impact |
| Too little traffic to detect any plausible effect | Qualitative research, larger changes, longer-term metrics with less noise, or a quasi-experiment |
| Outcome takes months (e.g., annual renewal) | A validated leading indicator, a long-running holdout, or accept a slow test |
| Strong network effects between units | Cluster randomization or switchback designs |
| Ethical or fairness concerns about withholding treatment | Phased rollout (stepped wedge), or don't test |
| You need to learn what to build | User research (see `ux-research`), not A/B tests |

### Step 2 — Write the hypothesis

A good hypothesis states the change, the expected effect on a specific metric, the mechanism, and the population: "Showing shipping costs on the product page (instead of only at checkout) will increase checkout completion among new visitors, because surprise costs are the most-cited abandonment reason." The mechanism tells you which secondary metrics should move if you are right (fewer exits at the shipping step), which helps distinguish a real effect from a fluke.

### Step 3 — Choose metrics

- **Primary (overall evaluation criterion)**: sensitive to the change, aligned with long-term value, measurable within the test duration. Often a rate or per-unit average at the randomization unit (conversion per user, revenue per user).
- **Guardrails**: business health (revenue, retention), user experience (latency, errors, crashes), and trust (complaints, unsubscribes, refunds). Decide in advance what degradation would block a launch.
- **Secondary / diagnostic**: the mechanism metrics and funnel steps.
- **Data-quality metrics**: sample ratio, assignment counts per day, logging volumes per arm.

Prefer metrics with lower variance when they are valid proxies (conversion rather than revenue, capped revenue rather than raw), and consider variance-reduction methods such as using pre-experiment values of the metric as a covariate (CUPED-style regression adjustment), which can cut required sample size substantially when pre-period behaviour predicts the outcome.

Beware metrics the treatment can game: a change that increases clicks by making the button harder to find on the first try is not an improvement. Ask what behaviour the metric rewards.

### Step 4 — Choose the randomization unit and population

| Unit | Use when | Watch out for |
|---|---|---|
| User (logged-in ID) | Most product changes; consistent experience across sessions and devices | Requires identity; logged-out users need a fallback |
| Device / cookie | Logged-out experiences | Same person on several devices sees several versions; cookie churn |
| Session / page view | Changes with no memory between visits (e.g., search ranking) | Users see both versions; learning effects contaminate; higher variance in "user" metrics |
| Account / organisation | B2B products where colleagues interact | Fewer units → less power; analyse at account level |
| Cluster (region, store, school, market) | Network effects, marketplace interactions, offline interventions | Very few units; need cluster-aware analysis; pre-period balance checks matter |
| Time period (switchback) | Marketplaces and systems where all users share a resource (pricing, dispatch algorithms) | Carryover between periods; need many periods |

**Interference.** If treated units affect control units (a marketplace where buyers in treatment buy up supply, social features, shared inventory), the comparison is biased. Use cluster or switchback randomization, or accept and estimate the bias.

**Population and triggering.** Include only units that could be affected by the change (e.g., users who reach the checkout page), assigned or analysed from the moment they would have seen the difference. Including unaffected users dilutes the effect and needs much more traffic. But trigger on something that happens identically in both arms — triggering on a treatment-only event biases the comparison.

**Assignment mechanics.** Deterministic hashing of (unit ID, experiment ID) into buckets gives consistent, reproducible assignment. Use a fresh salt per experiment so the same users are not always in treatment together across tests. Log the assignment exposure event when the unit actually encounters the experiment.

### Step 5 — Power, sample size and duration

You need: the baseline value and variance of the primary metric, the minimum detectable effect (MDE) that would be worth acting on, the significance level (commonly α = 0.05 two-sided), and power (commonly 80%).

Approximations for two equal groups at α = 0.05 two-sided and 80% power:

- **Proportions**: n per group ≈ 16 · p(1 − p) / Δ², with Δ the absolute difference. Baseline 5% conversion, detect a 10% relative lift (Δ = 0.005): 16 × 0.0475 / 0.000025 ≈ 30,400 per group.
- **Means**: n per group ≈ 16 · σ² / Δ².
- **Rule of thumb**: halving the MDE quadruples the sample size.

Choose the MDE from the business, not from the traffic available: "what is the smallest effect that would justify the cost of shipping and maintaining this?" If the sample needed for that MDE is unattainable, the honest options are: test a bolder change, use a more sensitive metric, apply variance reduction, run longer, or don't run the test.

Unequal splits (e.g., 90/10 to limit risk) need more total traffic for the same power; the smaller arm drives the variance.

**Duration**:

- Run for at least one full business cycle — usually whole weeks — so day-of-week effects are balanced; two weeks is a common minimum for consumer products.
- Long enough to reach the planned sample size.
- Long enough for novelty and learning effects to settle (see below).
- Avoid holiday periods unless the change targets them, and note atypical events.
- Fix the end date in advance.

Use a proper calculator or library (statsmodels power functions, R's `pwr`, an organisation's experimentation platform) for the final number, and record the inputs.

### Step 6 — Pre-launch checks

- **A/A test** (both arms identical) on new infrastructure or new metrics: confirms the split is balanced and the false-positive rate is about α. Running A/A tests periodically keeps the platform honest.
- **QA both variants** on all major platforms, browsers, locales, and in logged-in and logged-out states.
- **Verify logging** of exposure and outcome events in both arms.
- **Check for collisions** with other running experiments that touch the same surface; use mutually exclusive layers if they would interact.
- **Define stop conditions for harm**: a guardrail threshold (error rate, revenue drop) that triggers immediate shutdown regardless of the primary metric. This is a safety stop, not a "we're winning" stop.

### Step 7 — Run without peeking (or peek correctly)

Checking results repeatedly and stopping when p < 0.05 inflates the false-positive rate far above 5% — with daily checks over a month, it can exceed 20–30%. Options:

| Approach | How | Trade-off |
|---|---|---|
| **Fixed horizon** | Look only at the planned end | Simple, correct; no early stopping for wins |
| **Group sequential** (e.g., O'Brien–Fleming boundaries) | A few pre-planned interim looks with stricter thresholds early | Allows early stopping; requires planning; slightly larger maximum sample |
| **Always-valid / sequential tests** (e.g., mSPRT, confidence sequences) | Results valid at any time | Can look continuously; lower power than fixed horizon at the same n |
| **Bayesian with a decision rule** | Posterior probability and expected loss | Intuitive; still assess the decision rule's error rates by simulation |

Monitoring dashboards for *health* (guardrails, sample ratio, errors) during the test is fine and necessary. Making the ship decision from the primary metric before the planned end is the problem.

### Step 8 — Analyse

In this order:

1. **Sample ratio mismatch (SRM).** Compare the observed split to the design with a chi-square test. A very small p-value (commonly < 0.001) means assignment or logging is broken — e.g., a 50/50 test with 50,000 vs 48,900 units. Do not interpret outcomes until it is explained. Common causes: bots filtered differently, redirects that lose users in one arm, the treatment crashing before logging, caching.
2. **Exposure and balance.** Pre-experiment metrics should be similar across arms; large imbalances suggest assignment problems.
3. **Primary metric**: effect estimate, confidence interval (or posterior), relative and absolute lift. Use the randomization unit for variance (delta method or bootstrap for ratio metrics; see `statistical-analysis`).
4. **Guardrails**: any meaningful degradation?
5. **Secondary and mechanism metrics**: do they move consistently with the hypothesis?
6. **Segments**: only pre-planned segments are confirmatory. Others are exploratory; with many segments, some will show "significant" effects by chance. Correct for multiplicity and confirm with a follow-up test before acting on a segment finding.
7. **Time trends within the test**: is the effect stable, fading (novelty) or growing (learning)?

### Step 9 — Decide and document

Combine the evidence into a decision against the pre-registered rule: ship, iterate, or abandon. Document the hypothesis, design, results (with intervals), guardrails, decision, and what was learned — including null and negative results, which are as valuable as wins and are the most often lost. A searchable log of past experiments prevents re-running the same failed idea and calibrates future expectations.

## Interpretation hazards

### Novelty and primacy effects

Users react to change itself. New features get extra clicks at first (novelty) and fade; changes to familiar workflows initially hurt as users relearn (primacy/change aversion), then recover. Check the effect by days-since-first-exposure, compare new and returning users (new users have no prior habits), and run long enough for curves to flatten. Long-running holdouts measure the sustained effect.

### Statistical vs practical significance

A significant 0.1% lift may not justify the complexity of the change; a non-significant result whose interval spans −1% to +6% is inconclusive, not "no effect". Compare the interval to the MDE and to the cost of shipping.

### Winner's curse

The estimated effect of a test chosen because it won is biased upward, especially when underpowered. Expect smaller effects after launch. Holdouts or replication give a better estimate.

### Multiple variants

Testing k variants against control multiplies the comparisons; correct (e.g., Holm or Dunnett-style comparisons against control) or treat it as a screening stage followed by a confirmatory head-to-head.

### Multivariate (factorial) tests

Testing several factors at once (headline × image × button) in a full factorial lets you estimate main effects efficiently and detect interactions — but interaction estimates need much more traffic than main effects, and the number of cells grows multiplicatively. Use factorial designs when interactions are plausible and traffic is ample; otherwise run sequential A/B tests on the most important factor first.

### Long-term vs short-term

Short-term metrics can mislead: more notifications raise engagement this week and churn next quarter; aggressive discounts raise conversion and lower margins and future full-price purchases. Use guardrails for long-term health, long-running holdouts for cumulative effects of many launches, and validated leading indicators.

### Heterogeneous effects

An average effect can hide a positive effect for some users and a negative one for others. Look at pre-planned segments and distribution of outcomes (not just means), and be cautious about fairness: an improvement on average that harms a specific group may be unacceptable.

## Quasi-experiments: when you cannot randomize

When randomization is impossible (a policy applied to everyone, a launch in one country, a past event), use a design that constructs a credible comparison. Each rests on an assumption you must state and probe.

| Design | Idea | Key assumption | How to probe it |
|---|---|---|---|
| **Difference-in-differences** | Compare the change over time in treated vs untreated groups | Parallel trends: absent treatment, both would have moved alike | Plot pre-period trends; placebo tests on pre-periods; event-study plot by period |
| **Synthetic control** | Build a weighted combination of untreated units that matches the treated unit's pre-period | Pre-period fit implies post-period counterfactual | Pre-period fit quality; placebo runs on untreated units |
| **Interrupted time series** | Break in level or trend at the intervention time | No other change at the same time; trend and seasonality correctly modelled | Long pre-period; check for co-occurring events; comparison series |
| **Regression discontinuity** | Units just above vs just below a threshold that determines treatment | Units cannot precisely manipulate their position; nothing else changes at the threshold | Density of the running variable near the cutoff; covariate balance near it |
| **Matching / propensity scores** | Compare treated units to similar untreated units | No unmeasured confounders (strong and untestable) | Balance diagnostics; sensitivity analysis for hidden bias |
| **Instrumental variables** | Use a factor that affects treatment but affects the outcome only through treatment | Exclusion restriction (largely untestable) and a strong instrument | Instrument strength; argue exclusion carefully |
| **Staggered / phased rollout** | Roll out to random groups over time | Timing is random or unrelated to outcomes | Randomize the order if you can — then it is an experiment |

Quasi-experimental results deserve wider caveats than randomized ones. Present them as "consistent with an effect of X under assumption Y", show the evidence for the assumption, and run sensitivity analyses. If you control the rollout, randomize its order — that turns a quasi-experiment into a real one at almost no extra cost.

## Special cases

### Holdouts

A holdout keeps a small random group (often 1–10%) out of a feature or a set of launches for weeks or months. It measures long-term and cumulative effects that short tests miss, and checks whether short-term wins persist. Costs: the held-out users get a worse (or at least different) experience, and the holdout must be maintained through code changes. Keep holdouts small, time-limited and documented.

### Ranking, search and recommendation changes

Standard A/B tests on ranking work but are often low-powered because users' downstream behaviour is noisy. Interleaving (merging results from two rankers into one list and seeing which ranker's items users choose) is far more sensitive for comparing rankers, at the cost of measuring preference rather than business outcomes; use it to screen and an A/B test to confirm impact. Offline evaluation on logged data is useful but biased by the old system's choices of what to show.

### LLM and ML-model features

- Offline evaluation (see `llm-evaluation`) should gate what goes to an online test; online tests measure what users actually do with the output.
- Outputs are often non-deterministic: log the model version, prompt version and parameters per exposure so results are attributable.
- Latency and cost are natural guardrails; a better answer that takes twice as long may lose.
- Quality metrics from user signals (thumbs, regenerations, copy events, task completion) are sparse and biased toward engaged users; combine them with sampled human or automated grading of outputs from both arms.
- Safety guardrails (harmful-output rates, policy violations, escalations) should have hard blocking thresholds.

### Pricing and promotions

Price tests raise fairness, legal and trust issues (customers comparing prices), and effects on revenue are delayed (stockpiling, churn, future full-price purchases). Consider geographic or time-based tests, test packaging rather than headline price where possible, measure revenue and margin rather than conversion alone, and run long enough to see repeat-purchase effects. Check applicable consumer-protection rules before running.

### Email, notifications and marketing

Randomize at the recipient; measure downstream outcomes (purchases, retention, unsubscribes), not just opens or clicks — opens are increasingly unreliable due to privacy features in mail clients. Account for fatigue: more messages raise short-term response and long-term unsubscribes. Holdout groups that receive no campaign at all measure true incrementality, which is often much smaller than attributed conversions suggest.

### Small samples and B2B

With a few hundred accounts, detecting realistic effects on business outcomes is often impossible. Use stratified or paired randomization (pair similar accounts, randomize within pairs) to reduce variance, use more sensitive leading metrics, accept wider intervals and say so, or rely on qualitative evidence plus a phased rollout.

## Discovering context

- **Use the organisation's experimentation platform and its conventions** (assignment service, metric definitions, analysis methods). Check its default statistical method (fixed horizon, sequential, Bayesian) and interpret results accordingly.
- **Find the standard metric definitions** and guardrails used by other teams; reuse them.
- **Check the experiment log** for prior tests on the same surface or idea, and their effect sizes — they inform the MDE and the prior.
- **Know the traffic**: units per day reaching the affected surface, not total site traffic.
- **Know concurrent experiments** that touch the same users or surfaces.
- **Check ethical, legal and policy constraints**: consent and privacy rules, pricing fairness, regulated domains (health, finance, employment), and any review process for experiments on people. Experiments that could cause harm need explicit review, minimised exposure and clear stop conditions.

## Pitfalls and anti-patterns

- **No pre-registration**: metric, duration and segments chosen after seeing the data.
- **Peeking and stopping on significance.**
- **Ignoring sample ratio mismatch.**
- **Randomizing by one unit and analysing by another** (e.g., by user, analysing by page view without clustering).
- **Too many metrics, no hierarchy**, then highlighting the ones that moved.
- **Underpowered tests** declared "no impact".
- **Post-hoc segment hunting** presented as findings ("it worked for Android users in Germany on weekends").
- **Triggering on post-treatment behaviour** (analysing only users who clicked the new button).
- **Stopping at a novelty peak.**
- **Running during atypical periods** and generalising.
- **Interacting experiments** on the same surface without isolation.
- **Shipping a "flat" result as if it were a win** because it "didn't hurt" — when the interval includes meaningful harm.
- **Losing the learnings**: negative results not recorded.
- **Treating the experimentation platform as infallible**: assignment, logging and metric pipelines have bugs; A/A tests and SRM checks catch them.

## Quality bar and verification

Before launch:

- [ ] A written hypothesis with mechanism, population and expected direction.
- [ ] One primary metric, defined precisely; guardrails with blocking thresholds; secondary metrics listed.
- [ ] Randomization unit chosen to match the treatment and interference risks; analysis planned at that unit.
- [ ] Triggering defined on an event common to both arms.
- [ ] MDE justified by the business; sample size and duration computed with recorded inputs; whole weeks covered.
- [ ] Stopping rule fixed (fixed horizon or a planned sequential method); harm-stop conditions defined.
- [ ] Both variants QA'd; exposure and outcome logging verified; collisions with other experiments checked.
- [ ] Ethical and policy review completed where relevant.

After the test:

- [ ] SRM checked and passed (or explained and the analysis invalidated).
- [ ] Pre-period balance checked.
- [ ] Primary effect reported with an interval, absolute and relative, compared to the MDE.
- [ ] Guardrails reviewed; no meaningful harm or a conscious trade-off documented.
- [ ] Novelty or learning effects assessed by exposure time.
- [ ] Segment findings labelled confirmatory (pre-planned) or exploratory.
- [ ] Surprising results scrutinised for bugs before celebrating.
- [ ] Decision and learnings recorded, including null results.

## Worked reasoning: "Can we test a new checkout design next week?"

1. **Feasibility.** 18,000 users reach checkout per day. Baseline checkout completion 62%. The team says a 2-point absolute lift would justify the redesign.
2. **Power.** n per group ≈ 16 × 0.62 × 0.38 / 0.02² ≈ 9,400. With a 50/50 split, that is ~19,000 triggered users — about one day of traffic. But duration must cover full weeks for day-of-week effects and some novelty settling: plan two weeks.
3. **Unit.** Logged-in user; for guest checkout, a first-party device ID; analysis at that unit.
4. **Trigger.** Assign at checkout page view (identical in both arms).
5. **Metrics.** Primary: completed orders per triggered user within the session. Guardrails: average order value, payment errors, page load time, refund requests within 14 days. Secondary: step-level drop-off.
6. **Plan.** Fixed horizon at 14 days; daily health checks for errors and SRM only; harm stop if payment errors rise by more than 0.5 points.
7. **Result.** SRM p = 0.4 (fine). Completion +1.4 points (95% CI +0.6 to +2.2). AOV flat; payment errors flat. Effect stable across the two weeks; new and returning users similar.
8. **Read.** Real improvement, very likely positive, but probably smaller than the hoped-for 2 points (the interval only just reaches it). Ship if the redesign is worth ~1–2 points; expect the post-launch effect toward the lower end because of the winner's curse. Record the result in the experiment log.
