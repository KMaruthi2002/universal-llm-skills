---
name: data-analysis
description: >-
  Answer real questions with data: frame the question as a decision, establish
  the data's provenance, grain and coverage, explore before concluding, segment
  and compare like with like, reason about confounders and selection effects,
  and report findings with honest uncertainty and caveats. Use when someone
  asks "why did X change", "what drives Y", "is A better than B", "how many /
  how much", wants insights from a dataset, a metric investigation, a funnel or
  cohort analysis, or an ad-hoc analytical answer — in SQL, pandas, R, a
  spreadsheet or a BI tool. Not for choosing statistical tests (see
  statistical-analysis), cleaning raw data (data-cleaning-and-validation),
  designing experiments (experiment-design), or building a recurring dashboard
  (dashboard-building).
metadata:
  category: analysis
  related: statistical-analysis, data-cleaning-and-validation, data-visualization, sql-and-queries, experiment-design, root-cause-analysis, report-results, clarify-requirements
---

# Data Analysis

Data analysis is the work of turning a question into a defensible answer using data. The output is not a chart or a table; it is a claim about the world, with the evidence for it, the strength of that evidence, and what would change it. Most analyses that go wrong do so not because of arithmetic errors but because the question was vague, the data did not mean what the analyst assumed, or the comparison was not fair.

## Scope

This skill covers the end-to-end analytical loop: framing, understanding the data, exploration, comparison, causal reasoning, and reporting. It leans on siblings for specialised parts:

- `statistical-analysis` — which test, interval or model to use and how to check its assumptions.
- `data-cleaning-and-validation` — profiling, fixing and documenting raw data problems.
- `data-visualization` — turning findings into charts that communicate honestly.
- `experiment-design` — when the right answer is "run a controlled test" rather than mine observational data.
- `sql-and-queries` — writing correct and efficient queries.
- `root-cause-analysis` — when the question is "why did this system fail", not "what does the data say".
- `dashboard-building` — when the deliverable is a recurring view, not a one-time answer.

## Core principles

### 1. The question comes before the data

An analysis is only as good as the question it answers. "Look at the sales data and find insights" has no stopping condition and no way to be wrong, so it produces a pile of observations nobody acts on. "Should we extend the spring promotion to the northern region?" tells you which metric matters, which comparison is relevant, what precision is enough, and when you are done.

**Why:** the question decides the grain, the population, the time window, the comparison group and the metric. Without it, every one of those choices is arbitrary, and arbitrary choices are where bias creeps in — you end up choosing the cut that looks most interesting.

### 2. Know what a row is

Every dataset has a grain: one row per order, per order line, per user-day, per session, per event. Almost every serious analytical bug — double counting, inflated averages, impossible conversion rates — is a grain mistake. State the grain in words before computing anything, and re-state it after every join.

**Why:** "average order value" computed over order lines is a different (and wrong) number from the same metric computed over orders. Nothing in the query will warn you.

### 3. Data is a record of a process, not the world

Every column was produced by something: a form, a sensor, a tracking script, an ETL job, a human typing. That process has gaps, defaults, delays, and changes over time. A spike in "signups" may be a tracking change; a drop in "errors" may be a logging outage; "country" may be the billing address, the IP location, or whatever the user picked from a dropdown that defaulted to the first option.

**Why:** if you do not know how a number was produced, you do not know what it means, and you cannot tell a real change from a measurement change.

### 4. Compare like with like

A number on its own means almost nothing. Meaning comes from comparison: against last period, a control group, a benchmark, another segment, an expectation. And the comparison must be fair — same definitions, same population, same time window length, same maturity (a 3-day-old cohort cannot be compared with a 30-day-old cohort on 30-day retention).

**Why:** unfair comparisons produce confident, wrong conclusions. "Users who use feature X retain better" is usually "engaged users retain better, and engaged users find feature X".

### 5. Correlation is cheap; causation needs an argument

Observational data can show you that two things move together. To claim that one causes the other you need either a randomized comparison or a specific argument for why the obvious alternative explanations (confounding, reverse causation, selection, chance) do not apply. When you cannot make that argument, say so in plain words.

**Why:** decisions are causal ("if we do X, Y will improve"). Presenting an association as if it were causal leads people to pull levers that do nothing.

### 6. Uncertainty is part of the answer

Every estimate has error: sampling noise, measurement error, definitional ambiguity, and the possibility that your model of the situation is wrong. A finding reported without its uncertainty invites over-reaction to noise. A finding buried in caveats is useless. The skill is to state the answer, how sure you are, and what would most likely make it wrong — in that order.

## Process

### Step 1 — Frame the question

Turn the request into a question you could, in principle, be wrong about. Clarify:

- **The decision.** What will someone do differently depending on the answer? If nothing, ask whether the analysis is needed or reframe it.
- **The metric.** Which number, defined how? "Revenue" — gross or net of refunds? booked or recognised? including tax?
- **The population.** Which users, products, regions, time window? Who is excluded and why?
- **The comparison.** Versus what? Last year, a control group, a target, other segments?
- **The precision needed.** Does the decision flip at 2% or at 20%? This sets how much rigour is worth spending.
- **The deadline.** A rough answer today is often worth more than a rigorous one next month. Say which you are delivering.

If the request is ambiguous in a way that changes the answer, ask (see `clarify-requirements`). If you cannot ask, state your interpretation explicitly at the top of the result.

Write a one-paragraph analysis plan before querying: the question, the metric definition, the comparison, the data sources, and what result would lead to which conclusion. Writing down what you expect protects you from the temptation to declare whatever you find "interesting".

### Step 2 — Understand the data before trusting it

For each source, establish:

| Question | Why it matters |
|---|---|
| What is the grain (one row per what)? | Determines how to count and aggregate. |
| What is the primary key? Is it actually unique? | Duplicate keys silently inflate joins and counts. |
| Where does it come from, and how is it produced? | Tells you what the values mean and what they miss. |
| What period does it cover, and when was it last refreshed? | Partial recent periods look like drops. |
| What is excluded (test accounts, bots, internal users, deleted records, refunds)? | Inclusion rules change totals. |
| Have definitions or tracking changed over the window? | Changes look like trends. |
| Are there known incidents, outages or backfills? | These create artefacts. |
| What units, currencies, timezones? | Mixed units produce nonsense averages. |

Sources for these answers, in rough order of reliability: the code or pipeline that produces the data; data dictionaries and model docs; the people who own the source; the data itself (profiling); and last, column names (which lie).

Run a profile: row counts by period, null rates by column, distinct counts, min/max, top values (see `data-cleaning-and-validation`). Plot the row count over time — gaps, steps and spikes in volume are the single fastest way to find tracking and pipeline problems.

### Step 3 — Reconcile to a known number

Before any analysis, reproduce one number someone already trusts: last month's revenue from finance, the user count on the official dashboard, the order count in the operational system. If you cannot match it, find out why before going further. Differences of a few tenths of a percent may be explainable (timezones, refund timing); differences of 10% mean you have misunderstood something.

**Why:** if your baseline is wrong, every downstream number is wrong in a way you cannot see. And when you present results, the first question will be "why doesn't this match the dashboard?" — have the answer ready.

### Step 4 — Explore

Exploration is looking at the data with an open but disciplined mind. Useful moves:

- **Distributions before averages.** Look at histograms or percentiles (p1, p10, p50, p90, p99) of key metrics. Means hide skew, bimodality and outliers; most business metrics (revenue per user, session length, order value) are heavily right-skewed, so the mean is driven by a small tail.
- **Time series at more than one resolution.** Daily data shows day-of-week cycles and incidents; weekly smooths them; monthly shows trends and seasonality. Compare with the same period last year to separate seasonality from change.
- **Counts alongside rates.** A conversion rate going up because the denominator collapsed is a different story from one going up because conversions grew. Always show numerator and denominator.
- **Top-N and bottom-N.** Which customers, products, regions dominate? Concentration (e.g., top 1% of customers = 40% of revenue) changes how to interpret every aggregate.
- **Look at raw rows.** Pull 20 random records and 20 extreme ones and read them. Many problems (test data, duplicates, bot traffic, unit errors) are obvious to the eye and invisible in aggregates.

Keep a running log of what you looked at and what you found, including dead ends. It protects you from the garden of forking paths (see pitfalls) and makes the analysis reproducible.

### Step 5 — Segment and decompose

Aggregate changes are almost always the sum of different movements in different segments. Decompose:

- **By dimension.** Break the metric down by the dimensions most likely to matter: platform, region, channel, customer tenure, product line, plan tier. Look for where the change is concentrated.
- **Rate vs mix.** A total rate can change because rates within segments changed, or because the mix of segments shifted, or both. Compute both components. Example: overall conversion fell from 4.0% to 3.6%, but conversion within both mobile and desktop was flat — the drop is entirely because mobile (lower-converting) went from 40% to 60% of traffic. The action is completely different from "conversion is broken".
- **Funnel stages.** For multi-step processes, find which step moved.
- **Cohorts.** Group entities by when they started (signup month, first purchase) and track them over age, not calendar time. This separates "new users behave differently" from "everyone's behaviour changed".

Simpson's paradox is the extreme case of mix effects: a trend that holds in every segment reverses in the aggregate. Whenever segments differ greatly in size and in the metric, check the segmented view before trusting the aggregate — and decide, based on the causal story, which view answers the question.

Watch the size of segments as you slice: with many dimensions you will always find some small segment with a dramatic change. Report segment sizes, and treat findings in small segments as hypotheses.

### Step 6 — Reason about causes

When the question is "why" or "what if", lay out the candidate explanations explicitly and test each:

| Alternative explanation | How to probe it |
|---|---|
| **Measurement change** (tracking, definition, pipeline) | Check deploy logs, release notes, tracking plans; look for step changes at exact dates; compare with an independent source. |
| **Seasonality / calendar** | Compare with the same period in prior years; check holidays, paydays, day-of-week mix. |
| **Mix shift** | Rate-vs-mix decomposition (Step 5). |
| **Confounding** (a third factor drives both) | Stratify by plausible confounders; compare within strata; ask what differs between the groups besides the treatment. |
| **Selection** (who ends up in the group is not random) | Ask how units got into each group; look at pre-period behaviour of each group. |
| **Reverse causation** | Check timing: did the cause precede the effect? |
| **Regression to the mean** | Groups selected for being extreme (worst stores, top users) drift back toward average on their own. Compare with a similarly selected untreated group. |
| **Chance** | Size of the effect relative to normal week-to-week variation; formal test if needed (see `statistical-analysis`). |
| **Survivorship** | Are churned, deleted or failed entities missing from the data? |

Techniques to strengthen causal claims from observational data, in increasing order of effort: stratification and matching on known confounders; difference-in-differences (compare the change in a treated group to the change in an untreated one over the same period, assuming parallel pre-trends — check them); interrupted time series (look for a break at the intervention date against the prior trend); regression discontinuity (where treatment depends on a threshold); instrumental variables (rarely available and easy to misuse). See `experiment-design` for quasi-experimental detail. If the decision is important and a randomized test is feasible, recommend one instead of straining observational data.

Be explicit about the strength of the causal claim you are making. A useful scale:

1. **Descriptive** — "X happened." (no causal claim)
2. **Associational** — "X is higher where Y is higher."
3. **Plausibly causal** — "The timing, dose-response, and absence of obvious confounders suggest Y contributed to X."
4. **Causal** — "In a randomized test, Y increased X by 3–5%."

Match your language to the level you actually reached.

### Step 7 — Quantify and pressure-test

- **Sanity-check magnitudes.** Does the number make sense against things you know? A conversion rate of 140%, a user who placed 10,000 orders, average session of 9 hours, revenue larger than the company's reported total — stop and investigate.
- **Reconcile totals.** Segment sums should equal the total (or you should know why not — e.g., users in multiple segments). Pre-join and post-join counts should be explainable.
- **Sensitivity.** Does the conclusion survive reasonable alternative choices — different window, excluding outliers, a different definition of "active"? If a conclusion flips under a defensible alternative, report that it is fragile.
- **Effect size in business terms.** Translate "0.4 percentage-point lift" into "about 1,200 extra orders a month, roughly $60k". Decision-makers need magnitudes, not just signs.
- **Try to break it.** Ask: if this conclusion were wrong, what would I expect to see? Then look for that.

### Step 8 — Report

Lead with the answer. A good analytical write-up, in whatever format the audience uses, contains:

- **The answer to the question** in one or two sentences, with magnitude and confidence.
- **The key evidence** — the two or three comparisons that support it, usually as a chart or small table.
- **What it means for the decision** — the recommendation or implication, if appropriate.
- **Caveats that could change the conclusion** — not every caveat, just the ones that matter, ranked.
- **Method and definitions** — enough that someone could reproduce it: sources, filters, metric definitions, time window, exclusions.
- **What would make this more certain** — the next query, the experiment, the data that is missing.

Write for the reader's decision, not for your process. Nobody needs the chronological story of your exploration. See `report-results` and `data-visualization`.

Express uncertainty in plain language matched to evidence: "almost certainly", "probably", "we can't tell from this data". Give ranges, not point estimates, when the range is wide enough to matter. Never round away important uncertainty to make a slide cleaner.

## Common analysis patterns

Most analytical requests are variations of a handful of shapes. Each has a characteristic trap.

### Funnel analysis

Count entities reaching each step in order, and compute step-to-step conversion.

- **Define the funnel strictly or loosely, and say which.** Strict: a user must complete step 2 before step 3 counts. Loose: anyone who reached step 3 counts. They give different numbers; the strict version is usually what people mean.
- **Fix a conversion window** ("within 7 days of step 1"). Without one, recent entrants have had less time to convert and depress recent conversion rates.
- **Count unique entities, not events**, at each step — unless the question is about repeated attempts.
- **Report both step and cumulative conversion.** A 2-point drop at an early step can matter more than a 10-point drop at a late one, depending on volumes.
- **Trap:** tracking gaps at one step (an event that stopped firing on one platform) look exactly like a conversion drop. Check step volumes by platform and app version.

### Cohort and retention analysis

Group entities by start period; track an outcome by age (days/weeks/months since start).

- **Align on age, not calendar time.** The table is cohorts × age; the triangle shape is expected because young cohorts have no data at high ages.
- **Only compare cohorts at ages all of them have reached.** Never compare a cohort's "month 3" to another's incomplete "month 3".
- **Define "retained" precisely**: active in exactly week N (classic), active in week N or later (unbounded/rolling), or still subscribed (for subscriptions). Each answers a different question.
- **Watch cohort composition.** A cohort acquired during a big promotion behaves differently; a retention "improvement" may just be a different acquisition mix. Segment cohorts by acquisition channel when mix shifted.
- **Revenue retention vs logo retention**: net revenue retention can exceed 100% while most customers leave, if survivors expand. Report both when relevant.

### Before/after comparisons

"We changed X on the 10th; did Y improve?" is the most frequently requested and most frequently over-interpreted analysis.

- Compare equal-length windows that contain the same days of the week, away from holidays, and wide enough to cover normal variation.
- Show the longer history: is the "after" level outside the range of normal fluctuation before the change?
- Use a comparison group that was not affected (another region, platform, or product) and compare the *change* in both — a simple difference-in-differences.
- Check that nothing else changed at the same time (other launches, marketing, pricing, seasonality, tracking).
- Be explicit that, without a control, the result is suggestive rather than causal.

### Driver / "what explains Y" analysis

- Start with simple cross-tabs and segmented comparisons before any multivariate model; they are easier to explain and expose data problems.
- A regression can describe partial associations, but a coefficient is not a causal effect unless the model includes the right confounders and excludes mediators and colliders (see `statistical-analysis`).
- Variable importance from predictive models (tree importance, SHAP values) explains the *model's* behaviour, not causal drivers in the world. Say so when presenting them.
- Present drivers with magnitudes: "customers with more than 3 support tickets in month one churn at 2.4× the rate of those with none (18% vs 7.5%)" beats "support tickets are the top driver".

### Concentration and Pareto

- Sort entities by contribution, compute cumulative share; report "top X% account for Y%".
- Concentration changes how to read averages and how fragile totals are: if 5 customers are 40% of revenue, the loss of one dominates any trend.
- Check whether the top entities are real (a wholesale account, a reseller, an internal test account, a bot).

### Sizing and estimation

When data is partial and you must estimate a total ("how many potential customers"), build it from independent pieces (population × eligible share × adoption rate), state each assumption with a range, and compute low/base/high cases. Cross-check with an independent method (top-down vs bottom-up). Report the range, not just the base case, and say which assumption drives most of the uncertainty.

## Decision guidance

### How much rigour?

| Situation | Appropriate depth |
|---|---|
| Quick operational question, easily reversible decision | Directional answer, sanity-checked, caveats in a line. Hours. |
| Recurring metric investigation ("why did X dip") | Decomposition by key dimensions, check measurement changes, compare to seasonality. A day. |
| Strategic or expensive, hard-to-reverse decision | Full plan, reconciliation, causal reasoning, sensitivity analysis, peer review of method. Consider an experiment. |
| Claim going to external audiences, regulators, publications | All of the above plus pre-registration of method where possible, full reproducibility, independent check. |

### Observational analysis vs an experiment

Choose an experiment (`experiment-design`) when: the decision is causal, the intervention is under your control, randomization is feasible and ethical, and the cost of being wrong exceeds the cost and delay of testing. Choose observational analysis when: the event already happened, randomization is impossible, you need a fast directional read, or you are generating hypotheses for a future test.

### Mean, median, or something else?

| Use | When |
|---|---|
| Mean | You care about totals (revenue per user × users = revenue). Distribution not extremely skewed, or you have enough data that the tail is stable. |
| Median / percentiles | You care about the typical case, the distribution is skewed, outliers are noise. |
| Trimmed or winsorized mean | You need something total-like but a few extreme values dominate and are not representative. State the trimming rule. |
| Proportion above a threshold | The decision is about crossing a line (e.g., % of pages loading under 2s). |

Report the one that answers the question, and show the distribution when the choice is contentious.

### Absolute vs relative change

Report both when either could mislead. "Conversion up 50%" from 0.2% to 0.3% is small in absolute terms; "up 1 point" from 1% to 2% is a doubling. For rates, use "percentage points" for absolute differences and "%" for relative ones, and never mix them.

### Tool choice

Use whatever the data lives in and the team can review. SQL for large, warehouse-resident data and for anything that should be reproducible against the source; pandas / R / Julia for complex reshaping, statistics and iteration; spreadsheets for small data and audiences who need to poke at numbers (see `spreadsheet-modeling`); BI tools for exploration over well-modelled data. Keep the logic in code or a saved query, not in manual clicks, whenever the result matters — you will be asked to re-run it.

## Discovering context

Before producing an analysis in an existing environment:

- **Find existing definitions.** Most organisations already have a definition of "active user", "churn", "revenue". Look in metric layers, dbt models, BI semantic layers, data dictionaries, and existing dashboards. Using a private definition that disagrees with the official one creates confusion even if yours is better — if you think it is better, use the official one and show the difference.
- **Find prior analyses** of the same question. They reveal known data issues and save repeating dead ends.
- **Learn the reporting conventions.** Fiscal vs calendar periods, the timezone reports are cut in, which currency, whether weeks start on Monday or Sunday, how the team presents uncertainty.
- **Identify the data owners** and the known-issues list. Ask them before drawing a conclusion from an anomaly.
- **Match the audience's format.** A notebook for analysts, a short memo for executives, a ticket comment for engineers.

## Pitfalls and anti-patterns

- **Fishing.** Slicing until something looks significant. With 20 dimensions and 10 values each, chance alone produces striking segments. Decide the main cuts in advance; label everything else as exploratory.
- **The garden of forking paths.** Many small, reasonable-seeming choices (window, exclusions, definitions) made after seeing the data, each nudging toward a result. Write down choices before you look, and report sensitivity to the ones you made later.
- **Join fan-out.** Joining orders to order lines, or users to events, multiplies rows; sums and counts after the join are inflated. Count rows before and after every join; aggregate to the right grain before joining. See `data-cleaning-and-validation`.
- **Averaging averages.** The mean of per-store conversion rates is not the overall conversion rate unless stores are equally sized. Compute ratios as sum(numerator)/sum(denominator) at the level you report.
- **Incomplete periods.** The current day, week or month is partial; the last few days may also be incomplete due to pipeline lag or delayed events (refunds, chargebacks, late-arriving conversions). Exclude or flag them.
- **Survivorship bias.** Analysing only customers who still exist, products still on sale, or companies still in business.
- **Denominator drift.** Rates whose denominator changed definition or population over time (e.g., a bot filter introduced mid-period).
- **Ignoring base rates.** "80% of churned users never used feature X" means little if 80% of all users never used feature X.
- **Ecological fallacy.** Inferring individual behaviour from group-level correlations (regions with more X have more Y does not mean individuals with X have Y).
- **Regression to the mean mistaken for impact.** Interventions targeted at the worst performers always appear to work.
- **Precision theatre.** Reporting 23.847% when the uncertainty is ±5 points. Round to what the evidence supports.
- **Burying the answer.** Thirty charts and no conclusion. The reader should get the answer from the first two sentences.
- **Cherry-picking the time window.** Starting a trend line at a convenient trough. Show enough history to give context, and justify the window.
- **Treating missing as zero (or zero as missing).** Decide deliberately what an absent value means.

## Quality bar and verification

Before delivering, check:

- [ ] The question and the decision it informs are stated, and the analysis answers that question rather than a nearby one.
- [ ] The grain of every table used is known, and every join's effect on row counts is explained.
- [ ] At least one headline number reconciles to an independent trusted source, or the discrepancy is explained.
- [ ] Metric definitions, filters, exclusions and time windows are written down and match the organisation's standard definitions (or the deviation is flagged).
- [ ] Partial periods and data-lag effects have been excluded or flagged.
- [ ] Changes have been checked against measurement changes, seasonality and mix shifts.
- [ ] Ratios are computed as ratio-of-sums at the reported level; segment totals reconcile to the overall total.
- [ ] Causal language matches the strength of evidence.
- [ ] Uncertainty is stated: ranges, sample sizes, and the main threats to the conclusion.
- [ ] The conclusion survives at least one reasonable alternative analytic choice — or its fragility is reported.
- [ ] Magnitudes are translated into terms the decision-maker cares about.
- [ ] The analysis is reproducible: saved queries or code, versioned, with inputs identified.
- [ ] Someone reading only the first paragraph gets the answer.

If you cannot execute queries yourself, write the queries and the checks for the user to run, say what result would confirm or refute each step, and do not present expected results as if they were observed.

## Worked reasoning: "Why did weekly revenue drop 12%?"

1. **Frame.** Decision: whether to escalate to product and marketing. Precision: need to know if it is real and where; ±2% is fine.
2. **Reconcile.** Reproduce last week's revenue from the finance figure — matches within 0.3% (timezone of cut-off). Good.
3. **Measurement.** Check the pipeline: last two days' volume is normal, no partial loads. Check releases: a checkout tracking change shipped on Tuesday — but revenue comes from the payment system, not tracking. Rule out.
4. **Calendar.** Last week included a public holiday in two major markets; same week last year also dropped 8%. So most of the drop is expected seasonality; residual is about 4%.
5. **Decompose.** Orders down 9%, average order value down 3%. By region: the drop is concentrated in the two holiday markets (orders down 25%), others flat. By channel: paid search orders down 15% across all regions — larger than the holiday explains.
6. **Probe.** Paid search spend was cut 20% on Monday by a budget change. Timing matches; all regions affected; dose roughly matches historical spend elasticity.
7. **Report.** "Revenue fell 12% week-on-week. About two-thirds is the holiday (seen in prior years and concentrated in the holiday markets). Most of the rest coincides with Monday's 20% cut to paid search spend; paid-search orders fell 15% in every region. This is consistent with the cut causing the drop but is not proven — a short holdback test would confirm. Other channels and AOV are within normal variation."

Note what the report does: answer first, magnitudes attributed, causal claim hedged to the evidence, and a concrete next step to raise certainty.
