---
name: statistical-analysis
description: >-
  Choose, apply and interpret statistical methods correctly: descriptive
  statistics, distributions, hypothesis tests, confidence and credible
  intervals, regression, multiple-comparison corrections, effect sizes versus
  p-values, assumption checks, resampling, and Bayesian versus frequentist
  framing. Use when someone asks "is this difference significant", "which test
  should I use", "what's the confidence interval", "run a regression", "how do
  I interpret this p-value / coefficient", needs to quantify uncertainty, or
  needs a statistical result checked — in R, Python (scipy, statsmodels),
  spreadsheets or any stats package. Not for framing a business question or
  exploratory analysis (data-analysis), planning a test before it runs
  (experiment-design), or predictive model building (machine-learning-workflow).
metadata:
  category: analysis
  related: data-analysis, experiment-design, data-cleaning-and-validation, data-visualization, machine-learning-workflow, llm-evaluation
---

# Statistical Analysis

Statistics is the discipline of reasoning about quantities when the data is noisy, incomplete, or a sample of something larger. Its job is to separate signal from noise and to say honestly how big an effect is and how sure we can be. The most common failures are not computational: they are using a method whose assumptions do not hold, testing a question nobody asked, confusing statistical significance with importance, and running many tests while reporting one.

## Scope

This skill covers method selection, application, assumption checking and interpretation for descriptive and inferential statistics and for explanatory regression. Neighbouring skills:

- `data-analysis` — framing the question, understanding the data, causal reasoning in context.
- `experiment-design` — power, sample size, randomization and stopping rules *before* data is collected.
- `machine-learning-workflow` — models built for prediction rather than for estimating and explaining effects.
- `data-cleaning-and-validation` — getting the input into a state where statistics mean something.
- `llm-evaluation` — statistical comparison of model outputs (it uses this skill's methods).

## Core principles

### 1. Start from the estimand, not the test

The estimand is the quantity you want to know: "the difference in mean basket size between new and returning customers", "the odds ratio of churn for users on plan B versus plan A, holding tenure fixed", "the 90th percentile of latency". Name it first. The appropriate estimator, interval and test follow from it. Choosing "a t-test" before saying what you are estimating is how people end up answering a question nobody asked.

### 2. Effect sizes answer the question; p-values do not

A p-value is the probability of seeing data at least this extreme *if the null hypothesis were true*. It is not the probability that the null is true, not the probability the result is a fluke, and not a measure of importance. With enough data, trivially small effects become "significant"; with too little, important effects are "not significant". Always report the effect size with an interval. The interval shows both the magnitude and the uncertainty; the p-value adds little beyond it.

**Why:** decisions depend on how big an effect is and whether it plausibly matters, not on whether it crosses an arbitrary threshold.

### 3. Every method has assumptions; check the ones that matter

Each test or model assumes something: independence, a distributional shape, equal variances, linearity, no strong outliers. Some assumptions matter enormously (independence — violating it invalidates standard errors), others barely at reasonable sample sizes (normality of the data for a t-test with large n, thanks to the central limit theorem). Know which is which and check the important ones.

### 4. Independence is the assumption that bites hardest

Most standard errors assume observations are independent. Repeated measures on the same user, students within schools, sessions within users, time series observations, and randomization by cluster but analysis by individual all violate it. The result is standard errors that are too small and p-values that are too optimistic — sometimes by an order of magnitude. Identify the unit of independence before analysing.

### 5. The number of tests you ran is part of the result

If you test 20 hypotheses at α = 0.05, you expect one false positive even when nothing is going on. Reporting the one hit without the 19 misses is misleading even if each test is computed correctly. Track every test and correct or qualify accordingly.

### 6. Plot first

Summary statistics can be identical for wildly different data (Anscombe's quartet, the "datasaurus" set). Look at histograms, scatter plots, residual plots and Q-Q plots before trusting a number. Many assumption violations and data errors are obvious in a plot and invisible in a table.

## Process

### Step 1 — State the question statistically

Convert the request into:

- **Estimand** — what quantity, in what population.
- **Unit of analysis** — what is one independent observation? (User, not session; school, not student, if treatment was assigned to schools.)
- **Outcome type** — continuous, binary, count, ordinal, time-to-event, proportion, rate.
- **Comparison structure** — one sample vs a reference value, two independent groups, paired / repeated measures, several groups, association between continuous variables, adjustment for covariates.
- **Whether the analysis is confirmatory or exploratory.** Confirmatory analyses have a pre-specified hypothesis; exploratory ones generate hypotheses and should be reported as such.

### Step 2 — Describe the data

- **Size**: n per group, missingness per variable.
- **Centre and spread**: mean and SD for roughly symmetric data; median and IQR (or percentiles) for skewed data. Report both when unsure.
- **Shape**: histogram or density; check skew, multimodality, heaping (values clustered at round numbers), floors and ceilings.
- **Outliers**: identify, investigate, decide. Do not delete outliers because they are inconvenient. Delete only if they are errors, and report that you did; otherwise use robust methods or report with and without.
- **For binary outcomes**: counts and proportions, not just percentages.
- **For relationships**: scatter plots, correlation (Pearson for linear, Spearman for monotonic / rank-based).

### Step 3 — Choose the method

Use the decision tables below. When two methods are defensible, prefer the one that is more robust to the assumptions you are least sure of, and consider running both as a sensitivity check.

### Step 4 — Check assumptions

See "Assumption checks" below. Diagnose with plots more than with formal tests: formal normality tests (Shapiro–Wilk, etc.) reject trivial deviations at large n and miss important ones at small n.

### Step 5 — Estimate, then infer

Compute the effect estimate and its interval first. Then, if a decision rule needs it, the test. Report both together.

### Step 6 — Handle multiplicity

Count the tests. Apply a correction or a hierarchy (see below), or clearly label results as exploratory.

### Step 7 — Interpret and communicate

Translate the result into the units and terms of the question. State the assumptions made and the main threats. Avoid the standard misinterpretations (see pitfalls).

## Decision guidance

### Comparing groups

| Outcome | Two independent groups | Paired / repeated (same units) | Three or more groups |
|---|---|---|---|
| Continuous, roughly symmetric or large n | Welch's t-test (default over Student's — it does not assume equal variances and loses almost nothing when they are equal) | Paired t-test on differences | One-way ANOVA (Welch's ANOVA if variances differ), then planned contrasts or Tukey |
| Continuous, skewed, small n, or ordinal | Mann–Whitney U (tests whether one group tends to have larger values — not a test of medians unless shapes are identical); or bootstrap CI for the difference in medians/means | Wilcoxon signed-rank | Kruskal–Wallis, then pairwise with correction |
| Binary | Difference in proportions with CI; chi-square or two-proportion z-test for large counts; Fisher's exact for small expected counts (< 5 in any cell) | McNemar's test | Chi-square test of independence; logistic regression |
| Count | Poisson or negative binomial regression (check overdispersion: if variance ≫ mean, Poisson SEs are too small) | Paired models / mixed models | Same, with group as factor |
| Time-to-event | Kaplan–Meier curves + log-rank test; Cox regression for adjustment | — | Log-rank / Cox |
| Ratio metrics (e.g., revenue per session where sessions are random) | Delta method or bootstrap at the randomization unit | — | — |

Heavy-tailed business metrics (revenue per user): the mean may be what matters, but the t-test can be slow to become reliable. Use a large n, a bootstrap, winsorization (report it), or a log-transform if the estimand on the log scale is acceptable — remember the mean of logs back-transforms to a geometric mean, not the arithmetic mean.

### Associations and adjustment: regression

| Outcome | Model | Coefficient means |
|---|---|---|
| Continuous | Linear regression (OLS) | Change in outcome per unit change in predictor, holding others fixed |
| Binary | Logistic regression | Change in log-odds; exponentiate for odds ratio. For communication, convert to predicted probabilities or average marginal effects — odds ratios are routinely misread as risk ratios |
| Count | Poisson / negative binomial | Exponentiated = rate ratio |
| Proportion of a total (bounded 0–1) | Beta regression or binomial GLM with trials | — |
| Ordinal | Ordinal (proportional-odds) logistic | — |
| Time-to-event | Cox proportional hazards | Exponentiated = hazard ratio |
| Clustered / repeated | Mixed-effects (random intercepts/slopes) or GEE, or cluster-robust standard errors | Same as above, with correct uncertainty |

Regression rules of thumb:

- **Decide which variables to include from a causal picture, not from p-values.** Include confounders (causes of both treatment and outcome). Do not include mediators (on the causal path) if you want the total effect. Never adjust for colliders (common effects of treatment and outcome) — it creates spurious associations. Sketching a causal diagram, even informally, is the best defence.
- **Stepwise selection by p-value** produces biased coefficients, too-narrow intervals and unreplicable models. Avoid it for inference. For prediction use regularisation and cross-validation (see `machine-learning-workflow`).
- **Events per variable.** For logistic regression, very roughly 10–20 events (the rarer outcome) per estimated parameter before estimates become unstable. Fewer means overfitting; simplify or use penalised methods.
- **Multicollinearity** inflates standard errors of the correlated predictors but does not bias predictions. Check variance inflation factors (VIF > 5–10 is a flag). It matters if you want to interpret individual coefficients.
- **Interactions** mean the effect of one variable depends on another; a main-effect coefficient in a model with an interaction is the effect at the reference level of the other variable. Centre continuous variables to make main effects interpretable.
- **Extrapolation.** Coefficients are only meaningful within the range of the data.
- **R² is not a quality score for explanatory models.** A low R² with a precisely estimated coefficient can be exactly what you need; a high R² can come from a spurious trend.

### Intervals

| Need | Method |
|---|---|
| Mean, reasonable n | t-interval |
| Proportion | Wilson or Agresti–Coull interval (not the naive Wald interval, which fails near 0, 1 and at small n) |
| Difference in proportions | Newcombe or Wald with continuity for large n; bootstrap |
| Median, percentile, ratio, any awkward statistic | Bootstrap (percentile or BCa), resampling at the independent unit |
| Regression coefficient | Model SE (robust/cluster-robust if heteroskedastic or clustered) |
| Rare events (0 observed out of n) | "Rule of three": 95% upper bound ≈ 3/n |

A 95% confidence interval means: the procedure, repeated over many samples, captures the true value 95% of the time. It does *not* mean there is a 95% probability the true value lies in this particular interval (that is a Bayesian credible interval's interpretation). In practice, describe it as "the range of values compatible with the data, given the model".

### Multiple comparisons

| Situation | Approach |
|---|---|
| A few pre-planned comparisons, strong control wanted | Bonferroni (α/m) — simple, conservative; Holm — uniformly more powerful, same guarantee. Prefer Holm. |
| Many tests, discovery setting (screening many segments, genes, metrics) | Benjamini–Hochberg to control the false discovery rate |
| All pairwise comparisons after ANOVA | Tukey's HSD |
| One primary hypothesis plus secondary ones | Pre-specify the primary; test it at full α; treat others as supporting or apply a correction among them |
| Exploratory slicing | Do not pretend to correct; label as exploratory and require confirmation on new data |

Count tests honestly: every segment, every metric, every time window you looked at counts, whether you reported it or not.

### Frequentist vs Bayesian framing

Both are legitimate; they answer slightly different questions.

| | Frequentist | Bayesian |
|---|---|---|
| Output | Estimate, CI, p-value | Posterior distribution, credible interval, probabilities of hypotheses |
| Natural statements | "If there were no effect, data this extreme would be rare" | "Given the data and prior, there is an 87% probability the effect is positive" |
| Prior knowledge | Not formally included | Included explicitly via the prior |
| Stopping and peeking | Requires pre-planned stopping rules or sequential methods | Posterior is valid at any time, but decision rules applied repeatedly still have error-rate properties worth checking |
| Small samples / hierarchical data | Can be unstable | Priors and partial pooling stabilise estimates |
| Familiarity / review | Widely expected in many fields, regulators, journals | Increasingly common; requires justifying the prior |

Choose Bayesian when: you have genuine prior information, you want direct probability statements for decision-making, you have many small groups that benefit from partial pooling, or you need to update continuously. Choose frequentist when: the audience or a standard requires it, priors would be contentious, or simple well-understood methods suffice. With weak priors and decent data, the two usually agree numerically; disagreements are informative and usually point to small data or strong priors. Report the prior and check sensitivity to it.

### Parametric vs non-parametric vs resampling

- **Parametric** methods are more powerful when their assumptions hold and give effect estimates in natural units.
- **Rank-based** non-parametric tests are robust to outliers and shape but test a different hypothesis (stochastic dominance), and give less interpretable effect sizes.
- **Bootstrap and permutation** methods make few distributional assumptions and work for awkward statistics, but still require independent resampling units and enough data for the sample to represent the population (they do not rescue n = 8).

## Assumption checks

| Assumption | How to check | If violated |
|---|---|---|
| Independence | Think about the design: repeated measures, clusters, time order. Plot residuals vs time; autocorrelation function for time series. | Mixed models, GEE, cluster-robust SEs, aggregate to the independent unit, time-series models |
| Normality (of residuals / sampling distribution, not raw data) | Q-Q plot of residuals; for t-tests, consider n and skew | Large n usually fine; otherwise transform, bootstrap, or non-parametric |
| Equal variances | Residual vs fitted plot; compare group SDs (ratio > 2 is a flag) | Welch's tests; heteroskedasticity-robust SEs |
| Linearity | Residuals vs each predictor; partial residual plots | Transform, splines, polynomial terms |
| No influential outliers | Cook's distance, leverage; fit with and without | Investigate; robust regression; report both |
| Proportional hazards (Cox) | Schoenfeld residuals | Time-varying coefficients, stratification |
| Overdispersion (Poisson) | Residual deviance / df ≫ 1; variance ≫ mean | Negative binomial, quasi-Poisson |
| Expected counts (chi-square) | Any expected cell < 5 | Fisher's exact test, combine categories |
| Missing at random | Compare characteristics of missing vs non-missing; reason about the mechanism | Multiple imputation, sensitivity analysis; complete-case analysis is biased unless missingness is unrelated to the outcome |

## Effect sizes worth reporting

- **Difference in means** (in original units) with CI — usually the most interpretable.
- **Relative difference / ratio** — for skewed positive outcomes and business metrics.
- **Standardised mean difference** (Cohen's d, Hedges' g) — when units are arbitrary or for meta-analysis. Conventional "small/medium/large" labels (0.2/0.5/0.8) are field-agnostic guesses; context beats them.
- **Risk difference, risk ratio, odds ratio** — for binary outcomes. Risk difference is easiest to act on ("3 more per 100"); odds ratios approximate risk ratios only when the outcome is rare (< ~10%).
- **Number needed to treat** (1 / risk difference) — intuitive for interventions.
- **Correlation r and R²** — strength of association; r = 0.3 explains only 9% of variance.

## Practical recipes and intuitions

### How big a sample do you need to see anything?

Useful back-of-envelope figures (two-sided α = 0.05, 80% power, equal groups):

- **Comparing means**: n per group ≈ 16 / d², where d is the standardised difference. d = 0.5 needs ~64 per group; d = 0.2 needs ~400; d = 0.1 needs ~1,600.
- **Comparing proportions**: n per group ≈ 16 · p(1 − p) / Δ², where Δ is the absolute difference. Detecting 10% vs 11% (Δ = 0.01, p ≈ 0.1) needs ~14,500 per group.
- **Precision of a proportion**: the 95% margin of error is about ±1/√n at p near 0.5. n = 100 gives ±10 points; n = 1,000 gives ±3; n = 10,000 gives ±1.
- **Halving the margin of error needs four times the data.**

Use these to judge whether a "non-significant" result was ever capable of being significant, and to warn early when a question cannot be answered with the available data. For full planning, see `experiment-design`.

### Bootstrap, done properly

1. Identify the independent unit (user, cluster) and resample *those* with replacement, carrying all their rows.
2. Recompute the statistic on each resample; 2,000–10,000 resamples is typically plenty for intervals.
3. Use the percentile interval for well-behaved statistics; BCa when the bootstrap distribution is skewed or biased.
4. Set and record the random seed.
5. Remember the bootstrap cannot fix bias in the sample itself, and it performs poorly for extremes (max, very high percentiles) and for very small n.

### Permutation tests

To test whether a difference between randomized groups could be chance, shuffle the group labels (at the randomization unit) many times, recompute the difference each time, and see where the observed difference falls. It makes almost no distributional assumptions and directly mirrors the randomization. It tests the sharp null of no effect for anyone, which is a slightly different hypothesis from "no difference in means".

### Time series cautions

- Observations close in time are correlated; naive tests and regressions on time series overstate certainty. A trend that looks highly significant in OLS can be pure autocorrelated noise.
- Two trending series will correlate strongly even when unrelated (spurious regression). Difference the series, or model the dependence, before claiming association.
- Remove or model seasonality (day-of-week, annual) before looking for effects.
- For "did the intervention change the series?", use interrupted time series with a pre-period long enough to estimate trend and seasonality, or a synthetic control built from unaffected comparison series.
- For forecasting, evaluate on a hold-out period later than the training period, never by random split.

### Survey and weighted data

- If the sample was drawn with unequal probabilities or adjusted with weights, use the weights in estimates *and* in standard errors (survey-aware methods); unweighted SEs are wrong, and naive weighted SEs are also wrong.
- Report the effective sample size: heavy weighting reduces it, sometimes dramatically (Kish's approximation: (Σw)² / Σw²).
- Non-response bias is not fixed by larger samples. Compare respondents with known population characteristics.

### Ratio metrics

Metrics like "clicks per session" or "revenue per visit", where the denominator is itself random and both are aggregated per randomization unit, have variances that standard formulas get wrong if you treat sessions as independent. Use the delta method or a bootstrap at the unit level. This is a frequent source of over-confident results in product analytics.

### Language for reporting results

Calibrated phrasing, from weakest to strongest evidence:

- "The data is consistent with no difference; it cannot rule out an effect as large as X."
- "There is weak evidence of a difference (estimate X, 95% CI including zero to Y)."
- "B was higher than A by X (95% CI L to U)."
- "Across three independent replications, B consistently exceeded A by X–Y."

Avoid "proved", "trending toward significance", "highly significant" as a substitute for an effect size, and "no effect" when the interval is wide.

## Discovering context

- **Field conventions.** Medicine, psychology, economics, and product analytics have different defaults (e.g., clustered SEs in economics, pre-registration in trials, two-sided α = 0.05 almost everywhere). Check what the audience expects and what the organisation already uses.
- **Existing analysis code.** Reuse the team's established methods for the same metrics (e.g., an internal delta-method library for ratio metrics) unless they are wrong — then flag it.
- **Pre-registered plans.** If an analysis plan exists, follow it, and label any deviations.
- **Tool defaults.** Know what your software does by default: R's `t.test` is Welch by default; some spreadsheet and older library functions default to Student's; `scipy.stats.ttest_ind` requires `equal_var=False` for Welch. Some functions return one-sided p-values. Read the documentation for the exact function.

## Pitfalls and anti-patterns

- **"p > 0.05, so there is no effect."** Absence of evidence is not evidence of absence. Report the interval: if it includes large effects, the study was inconclusive. Use equivalence tests (TOST) if you need to show an effect is negligibly small.
- **"p = 0.001, so the effect is big."** p reflects sample size as much as magnitude.
- **"The difference between significant and not significant is not itself significant."** Group A's effect is significant and group B's is not does not mean A and B differ. Test the interaction directly.
- **Pseudoreplication.** Treating 10,000 page views from 200 users as 10,000 independent observations.
- **Peeking and optional stopping.** Checking a test repeatedly and stopping when p < 0.05 inflates false positives massively (to 20–30% with frequent looks). Use fixed horizons or sequential methods (see `experiment-design`).
- **HARKing** (hypothesising after results are known). Presenting an exploratory finding as if it were the planned hypothesis.
- **p-hacking.** Trying transforms, exclusions, covariates and subgroups until p < 0.05.
- **Dichotomising continuous variables** (e.g., "high vs low" at the median) throws away information and power and can create artefacts.
- **Ignoring regression to the mean** in before/after comparisons on selected units.
- **Adjusting for post-treatment variables or colliders**, which introduces bias.
- **Confusing standard deviation and standard error.** SD describes spread of data; SE describes uncertainty in an estimate. Error bars must say which.
- **Comparing overlapping confidence intervals** as a test. Two 95% CIs can overlap even when the difference is significant at 5%. Compute the CI of the difference.
- **Treating Likert items as precise interval data** without thought. Often acceptable for summed scales; questionable for single items.
- **Reporting only the model you liked.** Report the specification you pre-planned, or report the range across reasonable specifications.
- **Using a Wald interval for small or extreme proportions.** It can extend below 0 or above 1 and badly undercovers.
- **Assuming a linear trend in time series** with autocorrelation and seasonality, then reporting a significant slope. Time series need models that respect dependence.

## Quality bar and verification

- [ ] The estimand, unit of analysis and outcome type are stated.
- [ ] Data was plotted; distributions and outliers were examined and handled explicitly.
- [ ] The method matches the outcome type and the dependence structure; the choice is justified.
- [ ] Key assumptions were checked, preferably graphically, and violations handled.
- [ ] Effect sizes are reported in meaningful units, with intervals; p-values, if reported, are exact (p = 0.031, not "p < 0.05") and accompany rather than replace the effect.
- [ ] The number of tests performed is known and multiplicity is handled or disclosed.
- [ ] Confirmatory and exploratory results are clearly separated.
- [ ] Interpretation avoids the classic misreadings of p-values and intervals.
- [ ] Error bars and intervals are labelled (SD, SE, 95% CI, credible interval).
- [ ] Results were sanity-checked: a quick simulation, a simpler method, or a hand calculation agrees in magnitude.
- [ ] Code and software versions are recorded so the result can be reproduced.

Verification techniques that catch real errors:

- **Simulate known truth.** Generate data with a known effect under your assumed structure and confirm your pipeline recovers it — and that with no effect it rejects about α of the time. This catches clustering mistakes and broken code.
- **Recompute a simple case by hand** (or in a second tool). A two-group difference and its CI should match between your regression and a direct calculation.
- **Compare robust and standard versions.** If Welch and Student, or robust and classical SEs, differ substantially, an assumption is doing a lot of work.

If you cannot run code, show the formulas and inputs so the user can check them, and say which values are calculated versus assumed.

## Worked reasoning: "Is the new onboarding flow better?"

Data: 4,100 users saw flow A, 3,950 saw flow B, by random assignment at user level. 7-day activation: A 1,107 (27.0%), B 1,177 (29.8%).

1. **Estimand**: difference in 7-day activation probability, B − A, among new users.
2. **Unit**: user (randomized by user; one outcome each) — independence is fine.
3. **Method**: difference in proportions. Large counts, so normal approximation is fine.
4. **Estimate**: 2.8 percentage points. SE ≈ √(0.27·0.73/4100 + 0.298·0.702/3950) ≈ 0.0101. 95% CI ≈ 0.8 to 4.8 pp. Relative lift ≈ 10% (CI roughly 3% to 18%).
5. **Multiplicity**: activation was the pre-registered primary metric; the team also looked at five secondary metrics — those get a Holm correction and are reported as supporting.
6. **Interpretation**: "Flow B increased 7-day activation by about 3 percentage points (95% CI 1 to 5). The effect is very likely positive, but the low end of the interval (0.8 pp) sits just below the 1-point lift the team said would be worthwhile, so the gain could be smaller than hoped." Whether to ship then depends on the cost of shipping and on whether a small positive effect is acceptable — a business judgement, not a statistical one. Then check guardrails and novelty effects (see `experiment-design`) before calling it.
