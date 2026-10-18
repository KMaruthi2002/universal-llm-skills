---
name: prompt-engineering
description: >-
  Write, debug, and improve prompts and system prompts for any large language
  model: giving clear instructions and context, choosing a role, adding
  few-shot examples, structuring long prompts with delimited sections,
  controlling output format, deciding when to ask for step-by-step reasoning,
  iterating against test cases, and hardening prompts against injection from
  untrusted input. Use when someone asks to write or fix a prompt, a system
  prompt, an instruction block for an agent or tool, a classification or
  extraction prompt, or says "the model keeps ignoring X", "make the output
  consistent", or "why does it do Y". Not for building the surrounding
  application (llm-application-development) or measuring quality at scale
  (llm-evaluation).
metadata:
  category: ai-ml
  related: llm-application-development, llm-evaluation, ai-agents-and-tool-use, ai-safety-and-guardrails, rag-systems, technical-writing, chatbot-and-conversational-apps
---

# Prompt Engineering

A prompt is a specification written for a reader who is extremely capable, extremely literal in places you did not expect, and has zero context about your situation beyond what you put in front of it. Prompt engineering is the discipline of writing that specification so the model reliably does what you meant, then proving it does with tests rather than vibes.

## Scope

This skill covers the text you send to a model: system prompts, user-turn templates, tool and agent instructions, few-shot examples, output-format instructions, and the loop of testing and revising them.

It does not cover:

- the application around the prompt — streaming, retries, caching, model routing (`llm-application-development`);
- building a proper evaluation harness and statistics (`llm-evaluation`) — this skill uses small test sets; that skill makes them rigorous;
- tool schema design and agent loops (`ai-agents-and-tool-use`);
- the full threat model for untrusted input (`ai-safety-and-guardrails`) — this skill covers the prompt-level part;
- retrieval (`rag-systems`).

## Core principles

### 1. The model only knows what is in the context

Every ambiguity you leave is resolved by the model's priors, which are averaged over the whole internet, not over your product. When output is "generic", it is almost always because the prompt was generic. Before blaming the model, ask: could a smart new contractor, handed only this text, produce what I want? If they would need to ask five questions first, the model is guessing at all five.

Things people routinely omit: who the output is for, what it will be used for, what "good" looks like, what has been tried and rejected, what the constraints are (length, tone, legal, format consumed by a parser), and what to do in edge cases.

### 2. Say why, not just what

"Never use ellipses" is a rule the model follows brittlely. "This text is read aloud by a text-to-speech engine, which cannot pronounce ellipses, so never use them" lets the model generalise to other unpronounceable things (emoji, tables, URLs). Reasons let the model handle cases you did not enumerate, and they reduce over-application of rules in situations where the rule's purpose does not apply.

### 3. Specific beats emphatic

Capital letters, "CRITICAL", "you MUST", and repetition were compensations for older, less attentive models. With current models they often cause over-triggering: the model applies the shouted rule everywhere, including where it hurts. If something is being ignored, first make it clearer, more specific, and better placed; add emphasis only after testing shows clarity alone is insufficient, and then sparingly.

### 4. Tell the model what to do, not only what to avoid

"Don't write long paragraphs" leaves the target undefined. "Write in short paragraphs of two to three sentences" defines it. Negative-only instructions also prime the forbidden thing by naming it. Keep prohibitions for real hard limits, and pair each with the desired alternative.

### 5. Examples are the strongest signal in the prompt

Models imitate examples more faithfully than they follow descriptions. That is a superpower and a hazard: an example's length, tone, structure, and even incidental details (all examples happen to be about cats) will be copied. Choose examples deliberately, vary them along the dimensions that should vary, and keep them consistent along the dimensions that should not.

### 6. A prompt is code: version it and test it

A prompt change can fix one case and silently break ten others. Treat prompts as artifacts with a test set, a diff history, and a reason for every clause. "It looked good on the three inputs I tried" is not verification.

### 7. Instructions and data must be distinguishable

Whenever a prompt contains content you did not write — user messages, documents, web pages, tool results, emails — the model must be able to tell your instructions from that content. Delimit untrusted data clearly and tell the model it is data. This is necessary but not sufficient protection against injection; real safety comes from what the system is *allowed* to do (see `ai-safety-and-guardrails`).

## Discovering context first

Before writing a prompt, find out:

- **Which model(s) and API.** Capabilities differ: context length, whether a separate system role exists, native structured output, reasoning modes, tool calling, prefill support. Check the current vendor documentation and prompting guide rather than relying on memory; these change frequently.
- **Where the output goes.** A human reading a chat? A JSON parser? Another model? Text-to-speech? A UI with a character limit? This drives format more than anything else.
- **Existing prompts in the project.** Search the codebase for prompt files, templates, or strings sent to the model. Match their structure and conventions (delimiter style, variable syntax, where examples live) unless they are the problem.
- **Existing failures.** Ask for or collect real inputs where the current prompt fails. These are the seeds of your test set and are worth more than any amount of theorising.
- **Constraints.** Latency and cost budgets (longer prompts and reasoning cost both), privacy rules about what may be sent to the model, and whether the prompt is cached (stable prefixes matter then).

If you cannot get real failing inputs, write a handful of realistic ones yourself, including at least two hard or adversarial ones, and say that you did.

## Process

### Step 1 — Define success before writing

Write down, concretely:

- the task in one sentence;
- three to ten representative inputs, including edge cases (empty input, very long input, off-topic input, ambiguous input, hostile input);
- for each, what a good output looks like, or at least the properties it must have (contains X, under N words, valid against schema, refuses, asks a clarifying question).

If you cannot write expected properties, the task is under-specified; go back to the user (`clarify-requirements`).

### Step 2 — Draft the prompt

A strong prompt usually contains, in some arrangement that suits the task:

- **Context**: what the situation is, who the user is, what the product does, why this task exists.
- **The task**: what to do, stated directly.
- **Inputs**: the variable data, clearly delimited and labelled.
- **Constraints and rules**, each with its reason.
- **Edge-case handling**: what to do when input is missing, ambiguous, out of scope, or contradictory. This is where most production prompts are weakest.
- **Output specification**: format, length, structure, what to include and exclude.
- **Examples**, if the format or judgment is subtle.

You do not need all of these for a simple task. A one-line request to a capable model is fine when the task is unambiguous and the output is for a human who can follow up.

### Step 3 — Run it against the test inputs

Run every test input, read every output. Not a sample; all of them, at this stage. Note failures and classify them: misunderstood task, ignored constraint, wrong format, hallucinated fact, wrong tone, over-refusal, under-refusal, inconsistent across runs.

Run each input more than once if the model is sampled at non-zero temperature. A prompt that succeeds once and fails once on the same input is not fixed.

### Step 4 — Diagnose and revise, one change at a time

For each failure class, ask what in the prompt allowed it:

| Symptom | Usual cause | Typical fix |
|---|---|---|
| Output is generic or bland | Missing context about audience and purpose | Add who it is for, what it is used for, what distinguishes good from adequate |
| A rule is ignored | Rule buried, vague, or contradicted elsewhere | Make it specific, give its reason, move it near the relevant part, remove contradictions |
| A rule is over-applied | Emphatic phrasing, no stated scope | State when the rule applies and why; tone down emphasis |
| Format drifts | Format described only in prose | Show an example of the format; use native structured output if available |
| Copies example too closely | Too few or too similar examples | Add varied examples; say examples are illustrative |
| Makes things up | No permission to say "unknown"; asked for facts not in context | Explicitly allow "I don't know"/null; require grounding in provided material; ask for quotes |
| Inconsistent between runs | Task underspecified; judgment call with no criteria | Add decision criteria or a rubric; lower temperature if the API allows |
| Refuses benign requests | Over-broad safety wording | Narrow the restriction and explain the actual concern |
| Long-winded | No length guidance; verbose examples | State a target length; shorten examples |
| Answers before thinking on hard tasks | No room to reason | Allow reasoning (see below) |

Change one thing, re-run the whole test set, compare. Changing five things at once leaves you unable to tell which helped and which hurt.

### Step 5 — Add regression cases

Every failure you fix becomes a permanent test case. Over time this set becomes the real specification of the prompt. When the set grows past what you can read by hand, move to `llm-evaluation` for automated scoring.

### Step 6 — Simplify

Once it works, try deleting clauses. Many instructions added during debugging turn out to be unnecessary once the real cause was fixed. Shorter prompts are cheaper, faster, easier to maintain, and leave less room for contradictions. Re-run the tests after each deletion.

## Techniques and when to use them

### Roles and personas

A role line ("You are a senior tax accountant reviewing…") primes vocabulary, depth, and perspective. It helps most when the domain has a distinct register or standard of rigour. It does not substitute for the actual context: "You are an expert copywriter" does less than describing the brand, audience, and goal. Avoid roles that imply capabilities the system lacks ("you have access to the customer database") — the model may pretend.

### Structure for long prompts

When a prompt has several distinct parts — instructions, reference documents, examples, the user's input — separate them so the model (and future maintainers) can tell where each starts and ends. Options:

- Tagged sections with descriptive names (XML-style tags work well with many models and are easy to reference: "using the policy in the policy section…").
- Markdown headings.
- Clearly labelled delimiters (triple quotes, fenced blocks).

Pick one style and use it consistently; follow the project's existing convention if there is one. Name sections for their content, and refer to them by name in the instructions.

**Placement:** for long context (many documents), many models do better when the long material comes first and the question or instruction comes after it, close to where generation begins. Instructions that must govern the whole conversation belong in the system prompt. Test both placements if it matters; it is model-dependent.

### Few-shot examples

Use examples when:

- the output format is unusual or strict;
- the judgment is subtle (what counts as "urgent" in this support queue);
- tone or style is hard to describe but easy to show;
- you need consistent labelling on a classification task.

Guidelines:

- Three to five diverse examples are usually enough; more helps on hard classification but costs tokens.
- Cover the boundaries: include at least one tricky case and one "none of the above / refuse / ask" case if those are valid outputs.
- Balance labels. If four of five examples are "positive", the model learns a prior toward positive.
- Randomise or vary order; models can be biased toward the label of the last example.
- Make examples realistic, not toy-sized, if real inputs are long and messy.
- Label them clearly as examples so they are not mistaken for the actual input.
- If examples should only inform style and not content, say so.

**Zero-shot first.** With capable models, try a clear description before adding examples. Add examples when testing shows the description is not enough. Examples are expensive context and strong anchors.

### Output format control

In order of reliability:

1. **Native structured output / schema-constrained decoding**, where the API supports it. This guarantees syntactic validity against a schema. It does not guarantee the *values* are right.
2. **Tool/function calling** used as a structured-output channel.
3. **Prefill** (starting the assistant's turn with, e.g., `{`), where the API allows it, to force the format's opening.
4. **An explicit example of the exact format** plus a description.
5. **Prose description alone** — least reliable.

Always validate on the application side anyway (parse, check schema, check value constraints), and decide what happens on failure: retry with the error message, fall back, or surface the error.

Format tips:

- Match the prompt's own style to the desired output style. A prompt written in heavy markdown tends to produce heavy markdown; a prose prompt nudges toward prose.
- For machine-consumed output, forbid preambles ("Here is the JSON:") explicitly, or extract the payload from known delimiters.
- If a field may legitimately be unknown, allow `null` or a sentinel and say so; otherwise the model fabricates a value to satisfy the schema.
- Put an explanation or reasoning field *before* the answer field in a schema if you want the reasoning to inform the answer — generation order matters.

### Reasoning and chain of thought

Asking the model to reason before answering ("think through this step by step, then give the answer") improves accuracy on multi-step problems: maths, logic, multi-constraint planning, careful classification with criteria. Many current models also have built-in reasoning modes controlled by an API parameter; check the documentation, because when a native reasoning mode exists, manual "think step by step" instructions may be redundant or even counterproductive.

Trade-offs:

| Factor | Reasoning helps | Reasoning hurts or wastes |
|---|---|---|
| Task type | Multi-step, constraint-heavy, analytical | Simple lookup, extraction, short creative text |
| Latency budget | Generous | Tight, user waiting on first token |
| Cost | Acceptable | High volume, low value per call |
| Output consumer | Can separate reasoning from answer | Parser expects only the answer |
| Need for auditability | Reasoning helps humans review | — |

Practical rules:

- Separate reasoning from the final answer with clear delimiters or schema fields so the application can strip or log it.
- Prefer general guidance ("consider each constraint, check the answer against them") over a rigid prescribed sequence of steps; capable models often reason better than the script you would write. Prescribe steps when the process genuinely must be followed (compliance checklists).
- Do not treat displayed reasoning as a faithful account of how the model reached its answer. It is useful, but it can be post-hoc.
- Asking the model to verify its own answer against the stated criteria before finishing catches a meaningful fraction of errors cheaply.

### Grounding and reducing hallucination

- Provide the source material and instruct the model to answer only from it.
- Explicitly permit "the provided material does not say" as an answer.
- For long documents, ask the model to first extract the relevant quotes, then answer from those quotes. This both improves accuracy and gives you something to verify.
- Require citations to specific passages when the answer will be trusted.
- Do not ask for facts the model cannot know (today's prices, internal data) without supplying them.

### Decomposition and prompt chaining

When one prompt is doing many things — research, analysis, drafting, formatting — and quality suffers, split it into a chain: each step a focused prompt whose output feeds the next. Benefits: each prompt is simpler and testable on its own, intermediate outputs are inspectable, and different steps can use different models or settings. Costs: latency, more calls, error propagation. Chain when a single prompt's failures cluster in one sub-task; do not chain preemptively.

A common, effective chain: generate → critique against criteria → revise.

### Long-running and agentic prompts

For system prompts that govern agents or long conversations:

- State the goal and the definition of done, not just behaviours.
- Say how much autonomy to take: when to act versus when to ask, and which actions require confirmation.
- Describe the tools in terms of *when* to use each, not only what they do.
- Tell the model how to handle uncertainty and failure (retry, report, stop).
- Keep it scannable: future you will debug it under pressure.

See `ai-agents-and-tool-use` for tool and loop design.

### Prompt injection awareness

Any untrusted text in the context can contain instructions ("ignore previous instructions and…"). At the prompt level:

- Put untrusted content inside clearly labelled delimiters and say, in your instructions, that content inside them is data to be processed, never instructions to follow.
- Put your instructions in the system prompt or before the data, and restate the key task after long untrusted content.
- Ask the model to report, not obey, instructions found in data.
- Never put secrets in a prompt that a user can influence the output of; assume the system prompt can be extracted.

These measures reduce but do not eliminate injection. A determined attacker can often get through. The real controls are architectural: least-privilege tools, confirmation for consequential actions, output validation. See `ai-safety-and-guardrails`.

## Decision guidance

**System prompt vs user turn.** Put durable identity, rules, tone, and tool guidance in the system prompt; put the per-request task and data in the user turn. Some models weight the system prompt more for behavioural rules; others treat them similarly. If the API has no system role, use a clearly delimited preamble.

**One big prompt vs a chain.** Start with one. Split when tests show failures concentrated in a sub-task, when you need to inspect intermediate results, or when steps need different models.

**Prompt vs fine-tuning vs retrieval.** Prompting first, always: it is fastest to iterate. Retrieval when the problem is missing knowledge. Fine-tuning when you need a consistent style or format at scale that prompting cannot achieve reliably, or need to cut prompt length/cost dramatically. See `fine-tuning-models` and `rag-systems`.

**Temperature.** Lower for extraction, classification, and anything parsed; higher for brainstorming and creative variation. Some APIs restrict sampling parameters in reasoning modes — check the docs.

**Bigger model vs better prompt.** If a stronger model solves it with the same prompt, the prompt may be fine and the task genuinely hard. If a stronger model fails the same way, the prompt is underspecified. Testing on two model sizes is a cheap diagnostic.

## Porting prompts between models

Prompts tuned for one model often degrade on another. When switching:

- Re-run the full test set; never assume parity.
- Remove workarounds that compensated for the old model's quirks (shouting, repetition, odd phrasing).
- Check format adherence, verbosity, and refusal behaviour, which vary most.
- Read the new vendor's current prompting guide; recommended structures differ.

## Pitfalls

- **Testing on the inputs you wrote the prompt from.** The prompt will look perfect. Hold out cases, and collect real ones.
- **Accumulating patches.** Each failure gets a new sentence until the prompt is a contradictory pile. Periodically rewrite from the test set.
- **Contradictory instructions.** "Be concise" in one section and "explain thoroughly" in another; the model picks unpredictably. Search for conflicts when behaviour is erratic.
- **Hidden format coupling.** An example uses bullet points, so every output uses bullet points even when you asked for prose.
- **Ambiguous pronouns and references.** "Summarise it and send it to them" in a prompt with three documents and two parties.
- **Asking for the impossible silently.** "Always give a definitive answer" plus insufficient data guarantees fabrication.
- **Overfitting to one model version.** Behaviour shifts across versions; keep the test set and re-run on upgrades.
- **Leaking secrets in prompts.** API keys, internal URLs, or other customers' data in a system prompt are one extraction away from exposure.
- **Judging by a single run.** Sampling variance is real; run multiple times when outputs vary.
- **Relying on the prompt for security.** "Never reveal the system prompt" and "never take harmful actions" are suggestions to the model, not enforcement.
- **Over-engineering simple tasks.** A twelve-section template for a one-line rewrite wastes tokens and attention.

## Quality bar and verification

A prompt is ready when:

- It passes every case in its test set across repeated runs, or the remaining failures are documented and accepted.
- Edge cases (empty, oversized, off-topic, adversarial input) have defined, tested behaviour.
- Every rule has a stated reason or is self-evident.
- There are no internal contradictions (read it once purely looking for them).
- Untrusted content is delimited and labelled as data.
- Output that is machine-consumed is validated in code, with a defined failure path.
- No secrets or sensitive data are embedded.
- It has been simplified: removing any remaining clause makes a test fail or is a deliberate safety margin.
- If it will run at volume, there is a plan for ongoing evaluation (`llm-evaluation`).

When handing back a prompt, report what it was tested on, what still fails, and which assumptions about the model or inputs it depends on.

## An illustrative before/after

Illustrative only, not a template.

Before: "Summarise this support ticket."

Problems: no audience, no length, no definition of what matters, no handling of tickets that are spam or in another language, no format for the downstream dashboard.

After (described rather than shown verbatim): the prompt explains that summaries appear in a triage dashboard read by on-call engineers who decide within seconds whether to escalate; that the summary must therefore lead with the customer-visible impact and affected product area, then the reproduction details if any; that it must be at most two sentences because the dashboard truncates; that if the ticket is spam or contains no actionable issue, output a fixed marker the dashboard filters; that tickets in other languages are summarised in English with the original language noted; and that the ticket body is delimited and is data, not instructions. Two varied examples show the shape. A test set of fifteen real tickets, including spam, a multilingual ticket, and one containing an injection attempt, verifies it.

The improvement came almost entirely from context and edge-case handling, not clever phrasing. That is typical.
