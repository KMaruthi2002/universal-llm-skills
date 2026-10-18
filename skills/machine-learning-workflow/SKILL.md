---
name: machine-learning-workflow
description: >-
  Run a classic machine learning project end to end on tabular, text, image,
  or time-series data: framing the business problem as a prediction task,
  establishing baselines, splitting data correctly and preventing leakage,
  feature engineering, choosing model families, picking metrics that match the
  decision, validation and hyperparameter tuning, error analysis, experiment
  tracking and reproducibility, deployment for batch or real-time inference,
  and monitoring for data and concept drift. Use when building a classifier,
  regressor, forecaster, ranker, or anomaly detector; when a model scores well
  offline but fails in production; when choosing metrics or validation
  schemes; or when productionising a notebook model. For LLM-based features
  use llm-application-development; for training or adapting LLMs use
  fine-tuning-models.
metadata:
  category: ai-ml
  related: data-analysis, data-cleaning-and-validation, statistical-analysis, experiment-design, fine-tuning-models, llm-evaluation, etl-pipelines, observability, data-visualization
---

# Machine Learning Workflow

Most ML projects fail for reasons that have nothing to do with the choice of algorithm: the wrong problem was framed, the evaluation leaked future information, the metric did not match the decision, or nobody noticed the data changed after deployment. This skill is about the discipline around the model.

## Scope

Covers supervised learning (classification, regression, ranking), forecasting, and anomaly detection with classical and deep models, from problem framing to production monitoring.

Neighbours: `data-cleaning-and-validation` (deeper data quality work), `data-analysis` and `statistical-analysis` (exploration and inference), `experiment-design` (online A/B tests of model impact), `fine-tuning-models` (adapting large language models), `llm-application-development` (using LLM APIs), `etl-pipelines` (feature and data pipelines), `observability` (production monitoring infrastructure).

## Core principles

### 1. The decision comes first, the model second

A model is useful only if a prediction changes an action: approve or review a transaction, which items to show, how much stock to order. Start from that action, who takes it, and what each kind of error costs. This determines the target, the metric, the threshold, and whether ML is warranted at all.

### 2. Beat a simple baseline, or stop

Always build the dumbest reasonable baseline first: predict the majority class, the mean, last week's value, a hand-written rule, or a logistic regression on a few obvious features. It sets the bar, catches pipeline bugs (a fancy model that cannot beat the baseline usually has a bug), and sometimes turns out to be good enough to ship.

### 3. Validation must mimic deployment

Your offline estimate is only trustworthy if the validation split reproduces how the model will be used: trained on the past, predicting the future; trained on some customers, predicting new ones. A random split on data with time or group structure gives optimistic numbers that collapse in production.

### 4. Leakage is the most common cause of too-good results

Leakage is any information in training features that would not be available at prediction time, or that encodes the target. If results look remarkably good, assume leakage until proven otherwise.

### 5. Data quality dominates model sophistication

Better labels, more representative data, and a few well-understood features usually beat a more complex algorithm. Spend time looking at data and errors.

### 6. Reproducibility is a feature

You must be able to recreate any model: code version, data snapshot, features, hyperparameters, random seeds, environment. Without it you cannot debug, compare, audit, or roll back.

### 7. Models decay

The world changes: user behaviour, products, fraud patterns, seasonality, upstream data pipelines. A deployed model without monitoring silently gets worse.

## Discovering context

- **The decision and its owner.** What action, how often, by whom or what system, with what latency requirement?
- **Error costs.** What does a false positive cost vs a false negative? Are there fairness or regulatory constraints (credit, hiring, health, insurance often have specific legal requirements)?
- **The data.** Where it lives, how it is generated, how labels are produced (and how delayed and noisy they are), volume, time span, known quality issues.
- **What exists.** Current rules or models, their performance, project tooling (notebooks vs pipelines, experiment tracker, feature store, serving platform). Fit into existing infrastructure.
- **Prediction-time availability.** For each candidate feature, is it actually available, with the same definition and freshness, at the moment of prediction?

## Process

### 1. Frame the problem

Write down:

- **Target**: precisely defined, with the time window ("customer cancels within 30 days after the prediction date").
- **Prediction point**: when the prediction is made, which fixes what data is available.
- **Unit**: one prediction per what (user, transaction, day-store pair)?
- **Task type**: binary/multiclass classification, regression, ranking, forecasting, anomaly detection, or a combination.
- **Success**: the offline metric, the business metric, and the minimum improvement that justifies deployment.
- **Constraints**: latency, interpretability, fairness, privacy, cost.

Question whether ML is needed: if a few rules achieve most of the value, ship rules. If there are too few labelled examples or labels are unreliable, fix that first.

### 2. Explore and validate the data

- Check volumes over time, missingness, distributions, duplicates, impossible values, label balance, label noise.
- Plot the target over time; look for regime changes and seasonality.
- Verify join keys and grain (one row per unit?) — duplicated rows from joins are a classic silent bug.
- Read actual examples, including some of each class.

See `data-cleaning-and-validation` and `data-analysis`.

### 3. Split the data

| Data structure | Split strategy |
|---|---|
| Independent, identically distributed rows, no time effects | Random (stratified for imbalanced classes) |
| Time-dependent (most business data) | Time-based: train on earlier, validate on later, test on latest; rolling/expanding windows for CV |
| Grouped (multiple rows per user, patient, device) | Group split: all rows for a group in one fold |
| Both time and groups | Time-based with group awareness |
| Very small data | Repeated cross-validation; nested CV for tuning and evaluation together |

Rules:

- Create a **test set** once, early, and do not look at it until the end. Every peek converts it into a validation set.
- Fit all preprocessing (scalers, encoders, imputers, feature selection, target encoding, vocabulary) on training data only, inside the cross-validation loop. Use pipeline abstractions (e.g. scikit-learn pipelines) to make this automatic.
- For time series, leave a gap between train and validation when labels take time to materialise or features use windows that would otherwise overlap.

### 4. Hunt for leakage

Common sources:

- Features computed using data after the prediction point (aggregates over the full history, "last status").
- Features that are consequences of the target (a "refund issued" flag for predicting complaints; a treatment code that implies the diagnosis).
- Identifiers that correlate with the target through how data was collected.
- Duplicates or near-duplicates across train and test.
- Preprocessing fitted on all data.
- Target encoding without out-of-fold computation.
- Group leakage: the same entity in train and test.

Checks: if one feature dominates importance, investigate it; if offline performance is far above domain expectations, investigate; rebuild features with point-in-time joins (as-of joins) from raw event data.

### 5. Build a baseline

The trivial baseline plus a simple interpretable model. Record their metrics. Everything else is measured relative to these.

### 6. Engineer features

- Start from domain knowledge: what would an expert look at?
- Aggregations over time windows (counts, rates, recency, trends), computed point-in-time.
- Ratios and differences that encode meaningful relationships.
- Categorical encodings appropriate to the model (one-hot for few levels; target or frequency encoding for high cardinality, done out-of-fold; native categorical support in some gradient boosting libraries).
- Text: start with simple representations (bag of words, TF-IDF) as a baseline; pretrained embeddings often do better.
- Missingness can be informative: add indicators rather than silently imputing.
- Keep feature definitions in shared code used by both training and serving, to avoid training/serving skew.

### 7. Choose a model

| Data | Strong default | Notes |
|---|---|---|
| Tabular, structured | Gradient-boosted trees | Often the best accuracy for tabular data; handles mixed types and nonlinearity; needs tuning of depth, learning rate, rounds |
| Tabular, need interpretability or tiny data | Regularised linear/logistic regression, small trees, GAM-style models | Coefficients explainable; fast |
| Images, audio | Pretrained deep network, fine-tuned | Transfer learning beats training from scratch except with huge data |
| Text classification/extraction | Pretrained transformer fine-tuned, or embeddings + linear model, or an LLM with prompting | Compare cost/latency; LLM prompting is a strong baseline when labels are few |
| Time series forecasting | Seasonal naive baseline, then statistical models, then gradient boosting on lag features or deep models | Simple methods are surprisingly hard to beat; evaluate on rolling origin |
| Anomaly detection | Statistical thresholds, isolation-based methods, density or reconstruction models | Labels are scarce; evaluate with whatever labels exist and with human review |
| Ranking / recommendation | Learning-to-rank on engineered features; candidate generation + ranking at scale | Offline metrics correlate imperfectly with online behaviour |

Choose the simplest model that meets the bar. Consider latency, memory, retraining cost, interpretability needs, and the team's ability to maintain it.

### 8. Choose metrics

Match the metric to the decision:

| Situation | Metric |
|---|---|
| Balanced classes, symmetric costs | Accuracy, log loss |
| Imbalanced classes, care about positive class | Precision, recall, F1, precision-recall AUC (more informative than ROC AUC under heavy imbalance) |
| Ranking quality irrespective of threshold | ROC AUC, PR AUC |
| Fixed review capacity ("we can investigate 100 cases a day") | Precision@k, recall@k |
| Asymmetric costs | Expected cost at the chosen threshold |
| Probabilities used downstream | Calibration (reliability curves, Brier score), log loss |
| Regression, errors equally bad | MAE (robust) or RMSE (penalises large errors) |
| Relative errors matter | MAPE or similar, careful near zero |
| Forecasts | MAE/RMSE scaled against a naive forecast; quantile loss for prediction intervals |

Thresholds are a business decision: choose them on validation data using the cost of errors or capacity constraints, not a default of 0.5.

Report per-segment metrics (region, customer type, device, protected groups where relevant and lawful) — aggregates hide failures for subgroups.

### 9. Validate and tune

- Cross-validate with the split strategy from step 3.
- Tune hyperparameters with random search or Bayesian optimisation over sensible ranges; grid search wastes budget.
- Use early stopping on validation data for iterative models.
- Watch the gap between training and validation performance: a large gap means overfitting (regularise, simplify, add data); low performance on both means underfitting (better features, more capacity).
- Report variability across folds, not just the mean.
- Evaluate once on the untouched test set at the end.

### 10. Error analysis

- Inspect the worst errors and a random sample of errors.
- Slice errors by feature values and segments; look for clusters.
- Check calibration.
- Look for label errors: a meaningful fraction of "model errors" are wrong labels.
- Use the findings to decide what to do next: more data of a certain kind, new features, relabelling, or a different model.

### 11. Track experiments

Log for every run: code commit, data version or snapshot identifier, feature set, parameters, seeds, metrics (with fold variance), artifacts, and environment. Use an experiment tracker or at least a structured log. This prevents the "which notebook produced the good model?" problem.

### 12. Deploy

| Mode | Use when | Concerns |
|---|---|---|
| Batch scoring | Predictions needed periodically (daily churn scores) | Simplest; scheduling, freshness, backfills |
| Real-time API | Prediction needed at request time | Latency, scaling, feature freshness, fallbacks |
| Streaming | Continuous event processing | Complexity, state management |
| Embedded / edge | On-device | Model size, update mechanism |

Practices:

- Package the model with its preprocessing; version the artifact.
- Ensure features at serving time are computed identically to training (shared code or a feature store); test for training/serving skew by scoring a sample through both paths.
- Shadow-deploy (run alongside the current system without acting) before switching.
- Roll out gradually; measure business impact with an experiment where possible (`experiment-design`).
- Keep a fallback (previous model or rules) and a rollback path.
- Log inputs, predictions, model version, and later the outcomes, to enable monitoring and retraining.

### 13. Monitor and maintain

- **Data drift**: input feature distributions vs training (population stability index, distribution distance tests, simple summary statistics). Drift does not always hurt, but it is an early warning.
- **Prediction drift**: distribution of scores and predicted classes.
- **Concept drift / performance**: actual metrics once labels arrive (may be delayed; use proxies meanwhile).
- **Data quality**: missing values, schema changes, out-of-range values, upstream pipeline failures — the most common cause of sudden model failure.
- **Operational**: latency, errors, throughput.
- **Retraining policy**: scheduled, triggered by drift or performance drops, or both. Validate retrained models against the current one before promotion.

## Interpretability

Decide how much explanation the decision needs before choosing a model:

- **Global understanding** (what drives predictions overall): feature importance (permutation-based is more reliable than impurity-based), partial dependence plots, coefficients for linear models.
- **Local explanations** (why this prediction): attribution methods such as SHAP-style values; useful for reviewers and debugging, but they explain the model, not causality in the world.
- **Regulated decisions** may require reason codes or inherently interpretable models; check requirements before investing in a black-box model.
- Use explanations as a leakage detector: a feature that "explains" too much is a suspect.

## Label problems

Labels are often the weakest part of the dataset:

- **Delayed labels** (churn, default, fraud chargebacks) mean recent data has incomplete labels; exclude periods whose outcome window has not closed.
- **Proxy labels** (a click as a proxy for satisfaction) encode the proxy's biases; be explicit about what the label actually measures.
- **Feedback loops**: if the current system decides who gets reviewed, labels exist only for reviewed cases, and a new model trained on them inherits the old system's blind spots. Reserve a small random sample for unbiased labelling where possible.
- **Noisy labels**: audit a sample; consider training with robust losses or cleaning obviously wrong labels.

## Imbalanced classes

Rare positives (fraud, churn, defects) are common and change several choices:

- Use PR AUC, precision/recall at the operating threshold, or cost-based metrics; accuracy is meaningless.
- Stratify splits so every fold contains positives.
- Prefer class weights or adjusted thresholds to aggressive resampling; if you oversample or undersample, do it only on training folds, never before splitting.
- Resampling and weighting distort predicted probabilities; recalibrate on untouched validation data if probabilities are used downstream.
- With very few positives, metric estimates are noisy; report confidence intervals and consider whether the problem is better framed as anomaly detection or human review prioritisation.

## Forecasting specifics

- Always compare to a naive or seasonal-naive forecast (same as last period, same as same period last year). Many sophisticated forecasts fail to beat it.
- Evaluate with rolling-origin backtests across several cut-off dates, not one split; performance varies by season and regime.
- Features may only use information available at the forecast origin; for multi-step horizons, the lag features for later steps are not known yet.
- Produce prediction intervals, not only point forecasts, when decisions depend on risk (inventory, staffing); evaluate interval coverage.
- Special events (holidays, promotions, outages) need explicit features or handling, or the model learns them as noise.
- Hierarchies (store → region → total) should be reconciled so forecasts add up.

## Worked reasoning: a too-good churn model

Illustrative. A churn classifier reaches 0.97 ROC AUC; the domain expectation is around 0.75.

- Feature importance shows `days_since_last_login` dominates. Investigation: it was computed at data-extraction time, not at the prediction date. Customers who churned months ago naturally have large values. That is future information — leakage.
- Rebuilt with an as-of join at the prediction date, AUC drops to 0.78.
- A second check: the random split put rows for the same customer (monthly snapshots) in both train and test. Switching to a time-based split with customers grouped yields 0.74.
- The honest 0.74 still beats the rules baseline (0.66) and, at the retention team's capacity of 500 calls per week, precision@500 is double the current list. That is the number that justifies deployment.

The lesson generalises: suspiciously good results are a bug report, and the business-facing metric (precision at capacity) is what decides.

## Responsible use

- Assess whether predictions affect people's access to opportunities, services, or treatment. If so, check performance across groups, document limitations, and involve the appropriate legal or ethics review.
- Avoid features that are protected attributes or close proxies unless there is a lawful, justified reason.
- Protect personal data in training sets: minimise, pseudonymise, control access, honour deletion obligations.
- Document the model: purpose, data, metrics, segments, limitations, owner (a "model card" style document).

## Pitfalls

- **Framing a target that does not map to an action.**
- **Random splits on time-ordered or grouped data.**
- **Preprocessing fitted on the full dataset.**
- **Point-in-time violations** in feature joins.
- **No baseline**, so a broken model looks acceptable.
- **Optimising accuracy on imbalanced data** (a model predicting "no fraud" always is 99.9% accurate).
- **Default thresholds** instead of cost-based ones.
- **Repeatedly peeking at the test set.**
- **Training/serving skew** from reimplemented feature code.
- **Ignoring label delay**, evaluating on periods whose labels are incomplete.
- **Only aggregate metrics**, missing subgroup failures.
- **Deploying without monitoring or rollback.**
- **Notebook-only models** nobody can reproduce.
- **Chasing tiny offline gains** that do not move the business metric.

## Quality bar and verification

A model is ready for production when:

- The target, prediction point, and decision are written down and agreed with the decision owner.
- The split mirrors deployment; preprocessing is fitted inside training folds; leakage checks were done and suspicious features investigated.
- It beats a simple baseline by a margin that matters, on a test set touched once.
- Metrics and threshold reflect error costs; per-segment results were reviewed.
- Error analysis was performed and documented.
- The run is reproducible from tracked code, data version, and parameters.
- Serving features match training features, verified on a sample.
- Monitoring for data quality, drift, and performance is in place with alerts and owners; rollback is tested.
- Documentation covers purpose, data, performance, limitations, and fairness considerations.
