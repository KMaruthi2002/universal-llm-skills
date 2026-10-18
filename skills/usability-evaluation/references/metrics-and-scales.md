# Usability Metrics and Scales

Read this when a study reports numbers, especially in summative or comparative studies. Metrics make usability visible to stakeholders and allow comparison over time, but only if they are defined consistently and reported honestly.

## Effectiveness

**Task success rate.** The share of attempts in which participants achieved the task's predefined success criterion.

- Binary (success/failure) is simplest and most comparable.
- Graded (complete, partial, fail) captures nuance; define each grade before testing.
- Assisted completions count as failures (or a separate category), never as successes.
- Self-reported success in unmoderated tests is unreliable; verify by end state where possible (the right page reached, the right data saved).

**Errors.** Actions that deviate from a path to success: wrong selections, incorrect entries, invalid submissions. Define what counts as an error for each task in advance. Report error counts per task and categorize them (slips vs. mistakes in understanding), because different causes need different fixes.

## Efficiency

**Time on task.** Elapsed time from task start to completion.

- Report for successful attempts only, or separately for successes and failures; mixing them is misleading.
- Time distributions are usually right-skewed (a few very long attempts). Report the median or geometric mean rather than the arithmetic mean for small samples.
- Concurrent think-aloud inflates time; if time is a key metric, don't use think-aloud during timed tasks.
- Compare against a baseline (previous version, competitor, or an expert's time) to make the number meaningful.

**Path efficiency.** Steps or clicks taken relative to the optimal path. Useful for navigation-heavy tasks; deviations show where people detour.

**Assists and help usage.** How often participants needed moderator help, documentation, or search.

## Perceived ease and satisfaction

**Single post-task question.** After each task, a single rating of how easy or difficult the task was (commonly a seven-point scale from very difficult to very easy). Quick, sensitive to differences between tasks, and correlates reasonably with performance. Ask it consistently after every task.

**Confidence rating.** "How confident are you that you completed the task correctly?" Low confidence with actual success reveals fragile designs; high confidence with failure reveals dangerous ones (users think they did it right and didn't).

**System Usability Scale (SUS).** A widely used ten-item post-study questionnaire with alternating positive and negative statements on a five-point agreement scale. It produces a score from 0 to 100 (it is not a percentage).

- Scoring: for positively worded items, subtract 1 from the response; for negatively worded items, subtract the response from 5; sum the adjusted values and multiply by 2.5.
- Interpretation: published benchmarks across many studies place the average around 68; scores well above that are generally considered good, well below poor. Compare against your own previous scores and context-specific benchmarks where available, rather than treating any single cut-off as absolute.
- Use the standard wording if you want comparability; small wording changes (e.g. replacing "system" with the product name) are commonly accepted, but rewriting items breaks comparison.
- SUS measures perceived usability overall, not which parts are problematic; pair it with task-level data.

Other standardized questionnaires exist for perceived usability, user experience, and specific domains. Choose one that is validated for your purpose and use it unchanged.

**Avoid home-made satisfaction scales** for benchmarking. Unvalidated items have unknown reliability and cannot be compared with anything.

## Composite and business metrics

- Composite usability scores (combining success, time, and satisfaction) can summarize, but hide which dimension changed. Always report the components.
- Business metrics (conversion, task completion in analytics, support contacts, time-to-value) show real-world outcomes. Link usability findings to them when you can, but don't claim causality without an experiment (`experiment-design`).

## Sample size and uncertainty

- **Formative (finding problems)**: around five per user group per round reveals most frequent serious issues. Report counts ("3 of 5"), not percentages or statistical claims.
- **Summative (measuring)**: precision grows slowly with sample size. With 20 participants, a task success rate observed at 70% has a confidence interval roughly from the mid-40s to the mid-80s percent. Narrow intervals need large samples.
- Use appropriate interval methods for small-sample proportions (e.g. adjusted Wald / Agresti–Coull) and for time data (log-transform before computing intervals). See `statistical-analysis`.
- **Comparing designs**: within-subjects designs (each participant tries both, in counterbalanced order) need fewer participants than between-subjects designs, at the cost of learning effects. Decide the comparison and its required sample before running.
- **Pre-register targets**: decide success thresholds and comparisons before collecting data, to avoid finding whichever difference looks good.

## Benchmarking over time

- Keep tasks, wording, participant profile, environment, and metrics identical across rounds; any change breaks comparability.
- Store raw data, not just summary numbers, so you can recompute with new methods.
- Report changes with intervals; a small apparent improvement may be noise.

## Reporting numbers responsibly

- Always give n alongside any metric.
- Show distributions (or at least ranges) as well as central values.
- Don't average across tasks of very different difficulty without showing per-task results.
- Label inspection-derived numbers (e.g. "violations found") clearly; they are not user performance.
- When numbers and observations conflict (high SUS, low success), report both and investigate; don't pick the flattering one.
