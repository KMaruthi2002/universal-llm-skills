---
name: llm-evaluation
description: >-
  Build evaluations that tell you whether an LLM feature, prompt, model, RAG
  pipeline, or agent is actually good and whether a change made it better or
  worse: defining success criteria, building golden and adversarial test sets,
  code-based checks, rubric scoring, LLM-as-judge with its known biases and
  calibration against humans, pairwise comparisons, regression suites in CI,
  online metrics and user feedback, error analysis, and handling sampling
  noise and statistical significance. Use when someone asks "is this prompt
  better?", "which model should we use?", wants evals or a benchmark for an AI
  feature, needs to catch regressions, or is shipping LLM output without a way
  to measure it. For classic supervised-model metrics use
  machine-learning-workflow.
metadata:
  category: ai-ml
  related: prompt-engineering, llm-application-development, rag-systems, ai-agents-and-tool-use, statistical-analysis, experiment-design, testing-strategy, machine-learning-workflow
---

# LLM Evaluation

Without evaluation, every prompt edit, model swap, and pipeline change is a guess, and "it looks better" means "it looks better on the three examples I happened to try". Evaluation turns LLM development from taste into engineering: you define what good means, measure it on representative data, and make decisions on evidence that accounts for noise.

## Scope

Covers offline evaluation (test sets, metrics, judges), comparative evaluation (A vs B), regression testing, online evaluation (production signals, A/B tests), error analysis, and the statistics needed to avoid fooling yourself.

Neighbours: `prompt-engineering` (uses small test sets informally), `rag-systems` (retrieval-specific metrics), `ai-agents-and-tool-use` (trajectory evaluation), `machine-learning-workflow` (classic supervised metrics), `statistical-analysis` and `experiment-design` (deeper statistics and online experiments), `testing-strategy` (deterministic software tests).

## Core principles

### 1. Start from failure analysis, not from metrics

Generic metrics ("helpfulness", "coherence") chosen up front often measure nothing that matters. Look at real outputs first, find how they actually fail, and build evaluators for those failure modes. The metric set should be derived from observed errors and from what users and the business care about.

### 2. The test set is the specification

What is in the eval set is what you will optimise. If it lacks hard cases, edge cases, adversarial inputs, or the distribution of real traffic, you will ship something that passes the eval and fails users. Curating the set is the core work; scoring is the easy part.

### 3. Prefer the cheapest reliable evaluator

In order of preference when they suffice: deterministic code checks (exact match, schema validity, contains/excludes, regex, numeric tolerance, executes and passes tests) → reference-based comparison → model-based judge → human review. Code checks are fast, free, and consistent; reach for model judges where judgment is genuinely required.

### 4. Every automated judge must be validated against humans

An LLM judge is a model with its own biases and errors. Until you have measured its agreement with careful human labels on your task, its scores are uncalibrated opinions.

### 5. Outputs are samples from a distribution

With non-zero temperature, the same input gives different outputs. Even at zero temperature, many APIs are not perfectly deterministic. A difference of a few points on a small eval set can be pure noise. Quantify uncertainty before declaring a winner.

### 6. Measure what you will decide on

Every evaluation should map to a decision: ship or not, model A or B, which failure to fix next. Metrics that do not inform any decision are overhead.

## Discovering context

- What is the feature for, who uses it, and what does a bad output cost (annoyance, wrong decision, legal risk, safety)?
- What outputs exist already? Pull a sample of real production inputs and outputs if any (respecting privacy rules).
- Is there existing human feedback: ratings, edits, escalations, complaints, support tickets?
- What eval tooling does the project use (a test framework, an eval library, a tracing platform with eval features)? Fit into it rather than inventing a parallel system.
- Who can label? Domain experts are often needed; budget their time.

## Process

### Step 1 — Error analysis on real outputs

Collect 50–100 real or realistic inputs, run the current system, and read every output. For each failure, write a short free-text note describing what went wrong. Then group the notes into categories (open coding, then grouping). Count them. The resulting failure taxonomy tells you what to measure and what to fix first.

Repeat error analysis periodically and after major changes; new failure modes appear.

### Step 2 — Define success criteria

For each important dimension, write a criterion specific enough that two people would usually agree. "Accurate" is not a criterion. "Every number in the summary appears in the source document" is. Prefer binary pass/fail criteria per dimension over 1–10 scales: they are easier to label consistently, easier for judges to apply, and easier to interpret. Use graded scales only when the gradations are clearly defined and you need them.

### Step 3 — Build the test sets

Sources, roughly in order of value:

1. **Real production inputs**, sampled to reflect the actual distribution, plus over-sampled rare but important types.
2. **Known failures** from bug reports, error analysis, and user complaints.
3. **Expert-written cases** for important scenarios not yet seen in traffic.
4. **Adversarial and edge cases**: empty, very long, ambiguous, off-topic, multilingual, injection attempts, requests that should be refused, requests that should *not* be refused.
5. **Synthetic cases** generated by a model, varied along explicit dimensions (persona, intent, difficulty, format). Always review a sample; synthetic data tends to be cleaner and easier than reality.

Size: dozens of cases catch gross problems; a few hundred are needed to detect moderate differences between variants; distinguishing small differences needs more (see the statistics section). Start small and grow.

Keep separate sets:

- **Development set** you iterate against.
- **Held-out set** you check less often, to detect overfitting the prompt to the dev set.
- **Regression set**: every fixed bug, so it stays fixed.
- **Safety/adversarial set**.

For each case store: input, any context (retrieved documents, conversation history), reference output or expected properties where possible, tags (type, difficulty, source), and provenance.

### Step 4 — Choose evaluators per criterion

| Criterion type | Evaluator |
|---|---|
| Format, schema, length, required/forbidden content | Code |
| Exact answers (classification, extraction, maths) | Code: exact or normalised match, F1 per field |
| Code generation | Execute against tests in a sandbox |
| Factual consistency with a source | Model judge with the source; or claim extraction plus verification |
| Tone, helpfulness, adherence to nuanced guidelines | Model judge with a rubric, calibrated to humans |
| Comparative quality between variants | Pairwise judge or human preference |
| Safety / policy compliance | Classifier or judge, plus human review of positives |
| Tool use / agent success | Check final state of environment; trajectory checks |

Reference-overlap metrics from older NLP (n-gram overlap) correlate poorly with quality for open-ended generation; use them only where outputs are nearly deterministic.

### Step 5 — Build and calibrate model judges

Writing a judge:

- One judge per criterion, binary when possible. A judge asked to score six things at once does each poorly.
- Give the judge the criterion definition, pass and fail examples (including borderline ones), the input, the output, and any reference or source material.
- Ask for a short rationale before the verdict; this tends to improve accuracy and helps you audit it.
- Use a capable model; judging is often harder than generating.
- Constrain the output format and parse it.

Calibrating:

- Have humans label a sample (50–200 cases, stratified to include passes and failures).
- Measure judge–human agreement: accuracy, and separately the true-positive and true-negative rates (a judge that says "pass" to everything has high accuracy on a mostly-passing set and is useless). Cohen's kappa is a useful chance-corrected summary.
- Read disagreements; revise the judge prompt and examples; re-measure on a fresh sample to avoid overfitting the judge.
- Re-calibrate when you change the judge model or the product changes.

Known judge biases:

| Bias | Effect | Mitigation |
|---|---|---|
| Position bias | In pairwise comparisons, prefers the first (or second) option | Evaluate both orders; count only consistent verdicts or average |
| Verbosity bias | Prefers longer answers | Instruct to ignore length; control for length; include concise good examples |
| Self-preference | Prefers outputs from its own model family | Use a different model family as judge, or validate carefully |
| Style over substance | Rewards confident, well-formatted, fluent text even when wrong | Provide references or source material; make factual checks separate criteria |
| Leniency | Rarely fails anything | Include clear failing examples; use binary criteria; check TNR |
| Sensitivity to prompt wording | Scores shift with small judge-prompt changes | Freeze judge prompts; version them; re-calibrate on change |

### Step 6 — Pairwise comparison

When absolute scores are hard to define, compare variants directly: show the judge (or humans) both outputs for the same input and ask which better meets the criteria, with ties allowed. Randomise order and evaluate both orders. Aggregate as win rate with a confidence interval, or with a rating model over many comparisons. Pairwise is often more sensitive than absolute scoring for detecting improvements, but it only tells you relative quality — "B beats A" does not mean B is good enough.

### Step 7 — Run, analyse, decide

- Run each variant on the same cases, with the same settings. Run multiple samples per case when outputs vary.
- Look at per-category and per-tag results, not just the aggregate; a change can improve the average while breaking an important slice.
- Read the cases that changed outcome between variants. This is where you learn.
- Decide with uncertainty in view (next section).

### Step 8 — Automate regression

- Run fast code-based checks on every change (as part of CI).
- Run the full suite, including judges, on prompt/model/pipeline changes and before releases.
- Track scores over time; alert on drops beyond noise.
- Version everything: test set, prompts, judge prompts, models, parameters. A score is meaningless without knowing which versions produced it.

## Statistics: avoiding self-deception

- **Confidence intervals**: for a pass rate p on n independent cases, a rough 95% interval is p ± 2·sqrt(p(1−p)/n). At n = 100 and p = 0.8 that is roughly ±8 points — so a 3-point difference on 100 cases is not evidence of anything. At n = 400 it is about ±4 points.
- **Paired comparisons**: because both variants run on the same cases, analyse per-case differences (e.g. paired tests such as McNemar for pass/fail, or a paired bootstrap). Paired analysis is much more sensitive than comparing two independent averages.
- **Bootstrap** confidence intervals by resampling cases are simple and assumption-light.
- **Sampling variance**: run several samples per case for stochastic outputs and estimate per-case pass probability; or at least re-run the whole suite to see run-to-run variation before trusting small differences.
- **Multiple comparisons**: testing twenty prompt variants and picking the best guarantees some lucky noise. Confirm the winner on the held-out set.
- **Distribution shift**: an eval set built months ago may not reflect current traffic. Refresh it.

If the needed statistics get involved, use `statistical-analysis`.

## Online evaluation

Offline evals predict; production confirms.

- **Implicit signals**: retries/regenerations, edits to generated text, copy actions, abandonment, follow-up questions that indicate confusion, escalation to a human, task completion. Each is a noisy proxy; combine them.
- **Explicit feedback**: thumbs up/down, ratings, comments. Biased toward extremes and low response rates, but valuable for finding failures.
- **Sampled review**: periodically sample production traces for human or judge review, stratified to over-sample risky categories.
- **Online judges**: run cheap judges on a sample of live traffic to monitor quality trends (watch cost).
- **A/B tests**: for decisions with real user impact, randomise users to variants and compare business and quality metrics; see `experiment-design`.
- **Guardrail metrics**: latency, cost, refusal rate, error rate, safety flags — a quality win that doubles latency may not be a win.

Feed production failures back into the offline sets. This loop — production failure → error analysis → new test case → fix → regression check — is the engine of improvement.

## Evaluating specific system types

- **RAG**: evaluate retrieval (recall@k, ranking) separately from generation (faithfulness, correctness, citation accuracy, abstention). See `rag-systems`.
- **Agents**: task success via final environment state, steps/cost per success, unsafe-action attempts, run several times per task. See `ai-agents-and-tool-use`.
- **Classification and extraction**: precision, recall, F1 per class or field, confusion matrices; these are classic metrics and code-checkable.
- **Conversational systems**: evaluate whole conversations (simulated users with defined goals and personas can generate multi-turn tests; validate the simulator's realism).
- **Safety**: harmful-output rate on adversarial sets *and* over-refusal rate on benign-but-edgy sets; optimising one alone wrecks the other.

## What a good judge prompt contains

Described, not a template. A judge for "the summary contains no claims unsupported by the source" would include:

- the role framing only insofar as it sets the standard of care ("you are checking factual consistency for a compliance review");
- a precise definition of the criterion, including what does *not* count as a failure (paraphrase is fine; omissions are a different criterion and should not fail this one);
- the source document and the output, each clearly delimited;
- two or three labelled examples, including a subtle failure (a number slightly changed, a hedge removed) and a pass that looks suspicious but is fine;
- an instruction to identify each claim, check it against the source, then give a verdict;
- a fixed output shape: brief reasoning, then `pass` or `fail`, then the offending claim if failed.

Narrow scope keeps the judge accurate; the explicit non-failures prevent it from smuggling in other criteria; the subtle examples address leniency.

## Evaluating multi-turn and long-horizon behaviour

- **Conversation-level criteria**: did the assistant achieve the user's goal, stay consistent with earlier turns, remember stated preferences, recover from misunderstandings, and ask clarifying questions when needed?
- **Simulated users**: a model plays a user with a defined goal, persona, and information that it reveals only when asked. Useful for scale; validate by comparing simulated conversations against real ones, since simulators are usually more cooperative and articulate than people.
- **Trajectory checks for agents**: beyond final success, check for forbidden actions, unnecessary steps, and whether it verified its work.
- **Cost of evaluation**: long conversations and agent runs are expensive to evaluate; sample, and evaluate cheaper proxies (per-turn checks) more often than full runs.

## Choosing between models with evaluation

When comparing candidate models (or providers) for a feature:

- Use the same test set, the same prompt *adapted fairly* to each model (a prompt tuned for one model disadvantages others; give each a reasonable tuning pass), and the same parameters where comparable.
- Report quality, latency (p50 and p95, time to first token where relevant), cost per request, and failure rates (format errors, refusals, timeouts) side by side.
- Look at the cost-quality frontier: often a cheaper model is within noise of the best on most slices and only worse on one slice, which can be routed to the stronger model.
- Re-run when providers release new versions; the ranking changes.
- Use current published prices and limits, not remembered ones.

## Keeping evaluation affordable

Full suites with model judges and repeated samples get expensive. Control cost without losing signal:

- Tier the suite: fast code checks on every commit; a small, high-signal judged subset on every prompt change; the full suite nightly or before release.
- Cache outputs keyed by input, prompt version, model, and parameters, so unchanged variants are not regenerated.
- Use a cheaper judge for screening only after showing it agrees with the calibrated judge; escalate disagreements.
- Prune redundant cases that never fail and test nothing distinct — but keep regression cases, which guard specific past bugs.
- Track evaluation spend like any other cost.
- Run large offline suites through provider batch APIs where available; they are typically cheaper and latency does not matter for offline evaluation.
- Sample from the full suite between releases, with fixed seeds so successive samples are comparable.

## Labelling well

Human labels are the ground truth everything else is calibrated against, so their quality matters.

- Write labelling guidelines with the criterion, pass and fail examples, and rules for borderline cases. Revise them as labellers hit ambiguities.
- Use domain experts where correctness requires expertise; a generalist cannot judge whether medical or legal output is right.
- Have at least two people label an overlapping sample and measure agreement. Low agreement means the criterion is ambiguous — fix the criterion before blaming the labellers or the model.
- Hide which variant produced an output when labelling comparisons, to avoid bias.
- Make the labelling interface fast: show input, context, output, and criterion together; one keystroke per verdict; a notes field for "why". Slow tools produce few, careless labels.
- A single trusted domain expert who reviews many outputs and writes down their reasoning is often more valuable early on than a large crowd.

## Rough sample-size guide

For pass/fail metrics, approximate 95% margin of error for a single variant at a pass rate near 50% (the worst case), assuming independent cases:

| Cases | Approx. margin |
|---|---|
| 50 | ± 14 points |
| 100 | ± 10 points |
| 200 | ± 7 points |
| 400 | ± 5 points |
| 1,000 | ± 3 points |

Margins shrink near 0% or 100%. Paired comparisons between two variants on the same cases can detect smaller differences than these margins suggest, because only the cases that flip matter. Use these numbers to decide how many cases to build, and to sanity-check claims.

## Worked reasoning: is prompt B better than prompt A?

Illustrative. A team changes the summarisation prompt and reports "accuracy went from 82% to 86%" on 100 cases, judged by a model.

Questions to ask:

1. **Is the judge trustworthy?** It was never compared to human labels. Label 80 cases by hand; measure agreement. Suppose the judge agrees 90% of the time but passes 40% of the outputs humans failed — its true-negative rate is poor, so "accuracy" overstates quality for both prompts.
2. **Is the difference real?** Look at per-case changes: 9 cases flipped from fail to pass, 5 from pass to fail. A net of 4 out of 14 discordant cases is well within noise (a paired test would not come close to significance).
3. **Is it stable?** Re-run both prompts twice more. The pass rates bounce by 2–3 points per run, so single-run differences of this size are uninformative.
4. **Which slices moved?** The five regressions are all long, multi-topic threads — a slice that matters for the heaviest users.

Conclusion: no evidence B is better overall, and a possible regression on long threads. Next steps: fix the judge's leniency with failing examples, grow the set (especially long threads), use several samples per case, and re-compare. This is the normal outcome of looking carefully, and it saves shipping a regression.

## Pitfalls

- **Vibes-based iteration**: changing prompts based on a handful of eyeballed outputs.
- **Generic off-the-shelf metrics** unrelated to observed failures.
- **Uncalibrated LLM judges** trusted as ground truth.
- **Likert scales without anchors**: a "4 out of 5" means different things to different raters and runs.
- **One judge scoring many criteria at once.**
- **Only the aggregate score**, hiding regressions in important slices.
- **Overfitting to the dev set**, never checking held-out data.
- **Declaring winners on noise** from small sets or single runs.
- **Test sets that do not resemble production**: too clean, too easy, too synthetic.
- **Leaking test cases into prompts** as few-shot examples, inflating scores.
- **Unversioned evals**: scores that cannot be reproduced or compared.
- **Ignoring cost and latency** in model comparisons.
- **Never refreshing** the eval set as the product and traffic change.
- **Using production user data in eval sets** without honouring privacy and retention rules; anonymise or obtain the right permissions.

## Quality bar and verification

An evaluation setup is trustworthy when:

- Metrics trace to observed failure modes and to decisions.
- Test sets include real-distribution, hard, adversarial, and regression cases, with a held-out split, and are versioned.
- Code-based checks are used wherever possible.
- Every model judge has measured agreement with human labels (including true-negative rate) and documented biases mitigated.
- Comparisons are paired, report uncertainty, and account for sampling variance.
- Results are broken down by slice, and changed cases were read.
- Fast checks run in CI; the full suite runs on every prompt/model change.
- Production signals and sampled reviews feed new cases back into the sets.

When reporting results, state the set size, versions compared, the metric definitions, the uncertainty, the slices that moved, and the known limitations of the evaluation.
