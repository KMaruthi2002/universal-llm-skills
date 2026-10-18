---
name: fine-tuning-models
description: >-
  Decide whether to fine-tune a language or other foundation model versus
  improving prompts or adding retrieval, and if so, carry it out well:
  collecting, cleaning, and formatting training data, supervised fine-tuning,
  parameter-efficient methods such as LoRA, preference tuning, distillation
  from a larger model, hyperparameters at a practical level, evaluation
  against the base model and a prompted baseline, detecting overfitting and
  capability loss, deployment, and cost. Use when someone asks "should we
  fine-tune?", wants a model to follow a format, style, or domain behaviour
  more reliably, wants to shrink cost by moving to a smaller tuned model, is
  preparing a training dataset, or a fine-tuned model underperforms. For
  classic ML training use machine-learning-workflow.
metadata:
  category: ai-ml
  related: prompt-engineering, rag-systems, llm-evaluation, machine-learning-workflow, data-cleaning-and-validation, llm-application-development, ai-safety-and-guardrails
---

# Fine-Tuning Models

Fine-tuning changes a model's weights using examples of the behaviour you want. It is powerful for teaching *how* to respond — format, style, task-specific judgement, tool-use patterns — and weak at teaching *what is true*, especially facts that change. It is also slower to iterate on, needs maintained data, and must be redone as base models improve. The first expert move is usually to check whether you need it at all.

## Scope

Covers the decision to fine-tune, data work, method selection (full fine-tuning, parameter-efficient methods, preference optimisation, distillation), training at a practical level, evaluation, deployment, and maintenance. Applies to hosted fine-tuning APIs and to self-managed training of open-weight models.

Neighbours: `prompt-engineering` (try first), `rag-systems` (for knowledge), `llm-evaluation` (essential before and after), `machine-learning-workflow` (classic models), `data-cleaning-and-validation`.

## Should you fine-tune?

| Goal | Prompting / RAG usually sufficient | Fine-tuning is a strong candidate |
|---|---|---|
| Add knowledge of your documents | Yes — RAG; knowledge changes and needs citations | Rarely; tuned-in facts go stale, cannot be cited, and are recalled unreliably |
| Consistent output format | Often, with structured output features | When format is complex, strict, and prompting still fails a measurable fraction of the time |
| Specific tone or style | Often, with examples in the prompt | When style must be consistent at scale and is hard to describe |
| Narrow task (classification, extraction, routing) at high volume | A capable model with prompting may work | Yes — a small tuned model can match a large prompted one at a fraction of cost and latency |
| Reduce prompt length | Prompt caching may solve cost | Yes — behaviour baked in removes long instructions and examples |
| Domain language (medical, legal, code dialect) | Strong general models often handle it | When evaluation shows the base model consistently misunderstands domain usage |
| Teach a new skill the base model fundamentally lacks | — | Possible but hard; requires lots of high-quality data |
| Safety/policy behaviour | System prompts and guardrails | Sometimes, but tuning can also weaken built-in safety behaviour; test carefully |

Decision process:

1. Build an evaluation set and measure the best prompted solution (with retrieval if knowledge is involved) on a strong model. This is the baseline to beat (`llm-evaluation`).
2. Identify the specific remaining failures. Are they about knowledge (→ RAG), about missing instructions (→ prompting), or about consistent behaviour that prompting cannot pin down (→ fine-tuning)?
3. Estimate costs: data collection and labelling, training, hosting (tuned models may need dedicated or more expensive serving), and re-tuning when you change base model.
4. Fine-tune only if the expected gain on the eval, or the cost/latency saving at your volume, justifies these.

Check current provider documentation for which models can be fine-tuned, available methods, pricing for training and inference, and data-usage terms. These change often.

## Core principles

### 1. Data quality is almost everything

The model learns exactly what the examples show, including their mistakes, inconsistencies, and quirks. A few hundred to a few thousand excellent, consistent examples often beat tens of thousands of noisy ones. Every hour spent cleaning data is worth more than an hour spent tuning hyperparameters.

### 2. Train on what you will serve

Examples must match production inputs in format, length, distribution, and system prompt. A model tuned on clean, short inputs will struggle on messy, long ones. If production uses a specific system prompt or tool definitions, include them in training examples the same way.

### 3. Evaluate against the right baselines

Compare the tuned model to the base model with your best prompt, and to a stronger prompted model. "Better than the untuned base with no prompt" is not a useful finding.

### 4. Fine-tuning trades generality for specialisation

Tuning narrowly can degrade abilities outside the training distribution (sometimes called catastrophic forgetting) and can weaken safety behaviours. Measure general capabilities and safety alongside the target task.

### 5. Plan for re-tuning

Base models are superseded regularly. A fine-tune is a dataset plus a recipe that you will re-run; treat the dataset and pipeline as the durable asset, not the weights.

## Discovering context

- What exactly is failing today, with examples and measured rates?
- Hosted fine-tuning API, or self-managed open-weight model? Decided by data-sensitivity rules, required control, volume economics, available GPU expertise, and which models are permitted.
- What data exists: logs of past interactions, human-written examples, corrections from reviewers, labelled datasets? What are its licensing and privacy constraints?
- Who can produce or review high-quality examples (domain experts)?
- Production constraints: latency, cost per call, hosting environment.

## Methods

### Supervised fine-tuning (SFT)

Train on input–output pairs (or full conversations) showing the desired response. The default method for format, style, task behaviour, and tool-use patterns.

### Parameter-efficient fine-tuning (PEFT)

Rather than updating all weights, train a small number of added parameters. Low-rank adaptation (LoRA) and its quantised variants (e.g. QLoRA) are common. Benefits: far less memory and compute, small adapter files, the ability to swap adapters for different tasks on one base model. Quality is often close to full fine-tuning for task adaptation. Main knobs: rank (capacity of the adapter), which layers get adapters, learning rate. Most hosted APIs use some parameter-efficient method internally.

### Full fine-tuning

Updates all weights. More capacity, much more compute and memory, higher risk of forgetting. Rarely necessary for application-level adaptation.

### Preference tuning

Train on comparisons (a preferred and a rejected response for the same input) to shift the model toward preferred behaviours: helpfulness, tone, refusing appropriately, avoiding specific failure patterns. Methods include direct preference optimisation and related approaches, and reinforcement learning from human or AI feedback. Typically applied after SFT. Useful when "better" is easy to judge but hard to demonstrate with a single ideal answer. Needs carefully constructed pairs where the difference reflects exactly what you want to change.

### Reinforcement fine-tuning with graders

Some platforms support training with a programmatic or model-based grader that scores outputs, for tasks with verifiable answers (maths, code that must pass tests, extraction checkable against ground truth). Powerful where a reliable grader exists; the model will exploit any weakness in the grader, so validate it thoroughly.

### Distillation

Use a large, strong model (with your best prompt and possibly retrieval) to generate outputs, review and filter them, then fine-tune a smaller model on them. A common, effective way to get large-model quality on a narrow task at small-model cost and latency. Check the larger model's terms of use permit using its outputs to train other models.

### Continued pre-training

Further training on large amounts of raw domain text to shift the model's language distribution. Expensive, needs large corpora, and rarely the right first step for application builders.

## Data

### Collection

Sources:

- **Production logs** with good outcomes (high ratings, accepted without edits), after privacy review.
- **Human corrections**: outputs that reviewers edited; the edited version is a training target.
- **Expert-written examples** for important or rare cases.
- **Distilled outputs** from a stronger model, filtered by humans or validated by checks.
- **Synthetic inputs** generated to cover gaps, varied along explicit dimensions, with outputs produced and validated.

Cover the real distribution, including edge cases, refusals or "cannot answer" responses, ambiguous inputs (with the desired clarifying behaviour), and multi-turn interactions if the product is conversational.

### Cleaning and validation

- **Consistency**: the same kind of input should get the same kind of output. Inconsistent labelling teaches randomness. Write labelling guidelines and measure inter-annotator agreement for subjective tasks.
- **Correctness**: review outputs; one confidently wrong pattern repeated a hundred times becomes a confident model behaviour.
- **Deduplicate** exact and near-duplicates; they over-weight certain patterns and leak into eval splits.
- **Balance**: avoid letting one category dominate unless it dominates production; class imbalance in classification tasks shifts predictions.
- **Length and format**: check outliers; truncated examples teach truncation.
- **Privacy**: remove or pseudonymise personal data and secrets. Models can memorise and regurgitate training data.
- **Licensing**: confirm you have the right to use the data for training.
- **Contamination**: make sure evaluation examples do not appear in training data.

### Formatting

- Use the exact chat or prompt format required by the provider or model family (role structure, special tokens handled by the template). Mismatched templates silently degrade results.
- Include the production system prompt in each example if production will use one. Alternatively, train with a minimal prompt and use the same minimal prompt in production. Be consistent.
- For tool-use tuning, include tool definitions and tool-call/result turns in the format the model expects.
- For multi-turn data, decide which assistant turns contribute to the loss (typically all assistant turns; some setups train only on the final).

### How much data

Rules of thumb, to be verified by measurement: tens to low hundreds of examples can shift format and style; hundreds to a few thousand for robust task behaviour; more for complex tasks or substantial new skills. Plot eval performance against training set size (train on 25%, 50%, 100%) — if quality is still rising steeply, more data will help; if flat, data quality or method is the bottleneck.

## Training at a practical level

- **Splits**: train, validation (for monitoring during training and choosing checkpoints), and a held-out test set drawn from the evaluation process.
- **Epochs**: small datasets often need a few epochs; too many cause memorisation. Monitor validation loss and, more importantly, task metrics at checkpoints.
- **Learning rate**: the most sensitive hyperparameter. Start from the provider's or library's recommended defaults; too high causes instability or forgetting, too low under-trains. For LoRA, rates are typically higher than for full fine-tuning.
- **Batch size**: affects stability and throughput; use gradient accumulation if memory-limited.
- **Checkpoints**: save and evaluate several; the last is not always the best.
- **Reproducibility**: record base model version, dataset version, hyperparameters, seeds, and library versions.
- **Hardware (self-managed)**: estimate memory for model weights, optimiser state, activations; quantisation and parameter-efficient methods reduce needs dramatically. Use established training libraries rather than custom loops.

Signals:

| Observation | Likely meaning | Action |
|---|---|---|
| Training loss falls, validation loss rises | Overfitting | Fewer epochs, more data, lower learning rate, more regularisation, earlier checkpoint |
| Both losses plateau high | Under-fitting or noisy/inconsistent data | Inspect data consistency; more epochs; higher rank or capacity |
| Loss low but task metric poor | Loss does not reflect task; format/template mismatch; eval mismatch | Check templates; evaluate on task metric directly |
| Outputs repeat training examples verbatim | Memorisation | Fewer epochs; more diverse data; deduplicate |
| Great on target task, worse elsewhere | Forgetting | Mix in general-purpose data; lower learning rate; parameter-efficient method |
| Safety behaviour weakened | Tuning eroded alignment | Include safety examples; evaluate on safety set; reconsider data |

## Evaluation

Run before and after, on the same held-out set:

1. Base model with the best prompt.
2. A stronger general model with the best prompt (the "would a bigger model just solve it?" baseline).
3. The fine-tuned model with the production prompt.

Measure:

- Target-task quality (with the metrics from `llm-evaluation`).
- Out-of-distribution inputs, edge cases, and unanswerable cases.
- General capabilities relevant to the product (a small sample of unrelated tasks).
- Safety and refusal behaviour on adversarial and benign-edgy sets.
- Calibration of uncertainty: does it still say "I don't know" appropriately, or has tuning made it overconfident?
- Latency and cost per call.
- Memorisation: probe for regurgitation of training data, especially anything sensitive.

Read outputs, not just scores. Fine-tuned models can hit metrics while picking up odd stylistic tics from training data.

## Deployment and maintenance

- Serve with the same prompt template and parameters used in evaluation.
- Roll out gradually, compare against the existing solution on live traffic (`experiment-design`), and keep the previous solution as fallback.
- Monitor quality signals and drift; production distribution shifts can undermine a narrowly tuned model faster than a general one.
- Version the dataset, recipe, and resulting model together.
- Re-evaluate when a new base model is released: a newer base model with prompting may beat your old fine-tune; re-running the recipe on the new base may beat both.
- Keep collecting data (corrections, failures) for the next iteration.

## Labelling guidelines for SFT data

Training targets are only as consistent as the instructions given to whoever writes or reviews them. Good guidelines:

- define the task, the audience, and what an ideal response does, with reasons;
- specify format rules precisely (length range, structure, what to do with missing fields);
- define behaviour for edge cases: ambiguous inputs, out-of-scope requests, insufficient information, unsafe requests;
- include several reference examples, plus examples of common mistakes and their corrections;
- say how to handle disagreement and who resolves it.

Run a calibration round: several reviewers label the same 30–50 items, compare, discuss differences, and revise the guidelines before labelling at scale. Re-run calibration periodically; drift in labelling standards over a long project shows up as inconsistency in the model.

## Hosted API vs self-managed training

| Factor | Hosted fine-tuning API | Self-managed (open-weight) |
|---|---|---|
| Setup effort | Low: upload data, start job | High: GPUs, libraries, pipelines |
| Control over method and hyperparameters | Limited to exposed options | Full |
| Model choice | Provider's tunable models | Any open-weight model whose licence fits |
| Data residency | Data goes to provider (check terms) | Stays in your environment |
| Serving | Provider hosts the tuned model | You serve it (or use a hosting service) |
| Cost profile | Per-token training and inference fees | Hardware and engineering time |
| Portability | Tied to provider | Weights are yours (subject to licence) |

Check the licence of open-weight models for commercial use, redistribution, and acceptable-use restrictions before investing.

## Iterating on a fine-tune

Treat each training run as an experiment with a hypothesis:

1. Start with a small, very clean dataset and a short run to validate the pipeline end to end (format, template, evaluation). Most early failures are pipeline bugs.
2. Evaluate and do error analysis on the tuned model's outputs, as you would for a prompt.
3. Fix the data first: add examples for failing categories, correct inconsistent targets, remove examples that teach the wrong thing.
4. Change hyperparameters only when data looks right and the training curves suggest under- or over-fitting.
5. Keep a log of runs: dataset version, recipe, metrics, observations. Without it, you will re-run experiments you already did.

## Fine-tuning for tool use and agents

- Include the full tool definitions and realistic multi-step trajectories (tool calls, results including errors, and the final answer) in the format the model expects.
- Teach recovery: include examples where a tool fails and the model corrects its arguments or reports clearly.
- Include examples where the right move is *not* to call a tool, or to ask the user.
- Evaluate on held-out tasks with tools the training data did not over-represent, to check that the model learned a pattern rather than memorised sequences.

## Building preference data

Preference pairs teach the difference between two responses, so the difference must be exactly what you want learned.

- Generate candidates from the current model (several samples per prompt), then have humans or a calibrated judge choose the better one against written criteria.
- Make pairs differ mainly on the target dimension. If preferred responses are also systematically longer, the model learns "be longer".
- Include pairs on hard and borderline prompts; easy pairs teach little.
- Include safety-relevant pairs (appropriate refusal vs harmful compliance, and helpful answer vs unnecessary refusal) so tuning does not shift the balance unintentionally.
- Track annotator agreement; discard pairs where judges disagree strongly, as they encode noise.

## Parameter-efficient tuning knobs

| Knob | Effect | Starting point |
|---|---|---|
| Rank | Adapter capacity; higher fits more complex changes, risks overfitting small data | Low to moderate; increase only if under-fitting |
| Scaling factor (alpha) | Strength of adapter updates relative to rank | Follow library defaults, often tied to rank |
| Target modules | Which layers receive adapters; more layers, more capacity | Attention projections; add feed-forward layers if under-fitting |
| Learning rate | Speed and stability | Library/provider recommendation; tune first if results are poor |
| Dropout | Regularisation on adapter | Small; raise on tiny datasets |
| Quantised base | Fits larger models on smaller GPUs, small quality cost | Use when memory-bound |

Change one knob at a time and evaluate on the task metric. These are starting heuristics; verify against current library documentation.

## Worked reasoning: should this team fine-tune?

Illustrative. A team classifies incoming support emails into 25 categories. A large prompted model with category definitions and ten examples reaches 91% accuracy on a 500-email held-out set, at a cost and latency that are too high for their volume of a few hundred thousand emails a month.

- Knowledge is not the issue (categories are defined in the prompt); this is a narrow, high-volume task — a good fit for distillation.
- They label 3,000 emails using the large model, have support leads review a stratified 600 (correcting about 6%), and fix the definitions of three categories that caused most disagreement.
- They tune a small model with a parameter-efficient method, holding out the original 500 emails (checked for duplicates against the training set).
- The tuned small model reaches 92% overall, but per-category results show two rare categories dropping sharply. They add 150 more reviewed examples of those categories and re-tune; both recover.
- Serving cost drops by an order of magnitude and latency falls enough to classify on arrival.
- They keep the large prompted model as a fallback for low-confidence predictions and re-evaluate when new base models appear.

Notice what did the work: clear category definitions, reviewed labels, per-category evaluation, and a held-out set — not exotic hyperparameters.

## Cost reasoning

Total cost = data creation (often the largest: expert time) + training runs (including failed experiments) + evaluation + serving premium for tuned models (where applicable) + maintenance and re-tuning. Compare to the alternative: prompted large model cost per call × volume. Distillation into a small model pays off at high volume; at low volume, a prompted strong model is usually cheaper overall. Use current prices; do this arithmetic explicitly.

## Pitfalls

- **Fine-tuning to add knowledge** that belongs in retrieval.
- **Skipping the prompted baseline**, then attributing gains to tuning that a better prompt would have delivered.
- **Noisy, inconsistent training data.**
- **Template mismatch** between training and inference.
- **Training on a distribution unlike production.**
- **Evaluation contamination**: test examples present in training data.
- **Too many epochs on small data**, leading to memorisation.
- **Ignoring forgetting and safety regressions.**
- **Personal data in training sets**, later regurgitated.
- **Using another model's outputs** for training in violation of its terms.
- **Treating weights as the asset** rather than the dataset and recipe.
- **Not re-checking against newer base models.**

## Quality bar and verification

A fine-tuning effort is justified and done when:

- A documented baseline (best prompting, with retrieval if relevant) showed specific failures that fine-tuning targets.
- The dataset is consistent, correct, deduplicated, privacy-reviewed, licensed for the use, representative of production, and versioned; eval data is not in it.
- Training used the correct template, was monitored on validation data, and the chosen checkpoint was selected on task metrics.
- The tuned model beats the baselines on the held-out set by a meaningful, noise-aware margin, without unacceptable losses on general capability or safety sets.
- Cost and latency in production meet budget, with the full lifecycle cost considered.
- Deployment is gradual, monitored, and reversible; the recipe can be re-run on a new base model.
