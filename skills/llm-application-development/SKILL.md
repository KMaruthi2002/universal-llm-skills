---
name: llm-application-development
description: >-
  Design and build production software on top of large language model APIs
  from any vendor or self-hosted runtime: application architecture, model
  selection and routing, streaming, structured output and validation, tool
  calling, context-window management, prompt and response caching, cost and
  latency budgets, retries, timeouts, fallbacks between providers, logging,
  tracing, and data handling. Use when building or reviewing a feature, API,
  or product that calls an LLM, choosing a model or provider, wiring an SDK,
  fixing slow or expensive LLM calls, handling rate limits, or adding
  observability to an AI feature. For the prompt text itself use
  prompt-engineering; for retrieval use rag-systems; for autonomous loops use
  ai-agents-and-tool-use.
metadata:
  category: ai-ml
  related: prompt-engineering, rag-systems, ai-agents-and-tool-use, llm-evaluation, ai-safety-and-guardrails, chatbot-and-conversational-apps, backend-development, error-handling, observability, api-integrations-and-webhooks
---

# LLM Application Development

An LLM call is a slow, expensive, non-deterministic, occasionally unavailable remote function whose output must be treated as untrusted input. Building good LLM applications is mostly ordinary good engineering applied to that unusual function: clear interfaces, validation, timeouts, budgets, observability, and tests. The model is a component, not the architecture.

## Scope

Covers the software around model calls: architecture, SDK integration, model selection, streaming, structured output, tool-call plumbing, context management, caching, cost and latency control, resilience, logging, privacy, and shipping.

Neighbours:

- `prompt-engineering` — writing the prompts.
- `rag-systems` — retrieval pipelines.
- `ai-agents-and-tool-use` — autonomous multi-step loops and tool design.
- `llm-evaluation` — measuring quality and catching regressions.
- `ai-safety-and-guardrails` — threat model, injection, moderation.
- `chatbot-and-conversational-apps` — conversation UX and dialogue design.
- `fine-tuning-models` — training custom weights.

## Core principles

### 1. Model output is untrusted input

Treat every response like data from an unauthenticated user: it can be malformed, wrong, incomplete, or adversarially influenced by content the model read. Validate structure, check values, escape before rendering as HTML, never pass to a shell or SQL engine without the same safeguards you would apply to user input, and never let it authorise an action by itself.

### 2. Put the model behind your own interface

Wrap model calls in a thin internal module with your own types: `summarise_ticket(ticket) -> Summary`, not raw SDK calls scattered through the codebase. Why: vendors change APIs and models get deprecated; you will want to switch providers, add caching, log uniformly, enforce budgets, and mock in tests. One seam makes all of that a local change.

### 3. Use the least model that passes the eval

Bigger models are slower and cost more per token. The right model is the cheapest and fastest one that meets your quality bar *on your own test set*. You can only know this if you have a test set (`llm-evaluation`). Decide by measurement, not by leaderboard reputation.

### 4. Deterministic code for deterministic work

Use the model for what only a model can do: understanding language, judgment, generation. Use code for arithmetic, date maths, lookups, validation, sorting, permission checks, and anything with a right answer computable by rules. Every task moved from the model into code becomes faster, cheaper, and testable.

### 5. Design for latency from the start

Users perceive time to first visible output, not total time. Streaming, progressive UI, parallel calls, and smaller models for early steps matter more than micro-optimising prompts. Retrofitting streaming into a non-streaming architecture is painful.

### 6. Everything must be observable

You cannot debug a non-deterministic system you cannot see. Log the inputs, the full prompt version, the model and parameters, the output, token counts, latency, cost, and errors for every call — subject to your privacy rules. Without this, "the AI gave a weird answer yesterday" is uninvestigable.

### 7. Assume the provider will fail

Rate limits, timeouts, overloaded errors, regional outages, and model deprecations are normal operating conditions. Budget for them in design: timeouts, bounded retries with backoff and jitter, fallbacks, graceful degradation, and clear user messaging.

## Discovering context

Before building, find out:

- **Existing integration.** Search for SDK imports, API base URLs, environment variable names for keys, existing wrappers. Extend the existing wrapper rather than adding a parallel one.
- **Which provider(s) and models are approved.** Organisations often have contracts, data-processing agreements, regional requirements, or bans. Ask if unclear.
- **Data sensitivity.** What user data will be sent? Is there PII, health, financial, or confidential business data? What do the provider's data-retention and training terms say? Are there regional data-residency rules?
- **Current documentation.** Model names, context limits, pricing, rate limits, and features (structured output, caching, batch APIs, reasoning modes) change frequently. Check the provider's current docs and pricing page; do not rely on remembered numbers.
- **Budgets.** Acceptable latency (p50 and p95), cost per request or per user per month, and expected volume.
- **Quality bar.** What does acceptable output look like, and is there a test set? If not, building a small one is part of the job.

## Architecture

### Common shapes

| Pattern | Use when | Watch out for |
|---|---|---|
| **Single call** (input → prompt → output) | Classification, extraction, summarisation, rewriting | Over-stuffing one prompt with many jobs |
| **Chain / pipeline** (fixed sequence of calls) | Multi-stage tasks where each stage is well-defined | Error propagation, cumulative latency |
| **Router** (classify, then dispatch to specialised prompt/model) | Heterogeneous requests with different needs | Router errors send requests to the wrong handler |
| **Parallel fan-out + merge** | Independent sub-tasks; multiple perspectives; voting | Cost multiplication; merge quality |
| **Retrieval-augmented** | Answers depend on your private or changing data | See `rag-systems` |
| **Tool-using single turn** | Model needs one or two lookups or actions | Validation of tool arguments |
| **Agent loop** (model decides next step repeatedly) | Open-ended tasks where steps cannot be predetermined | Cost, unpredictability; see `ai-agents-and-tool-use` |

Prefer the simplest shape that works. Workflows with fixed steps are easier to test, cheaper, and more predictable than agents. Move toward agents only when the task genuinely requires dynamic decisions.

### Where the model sits

- **Server side, always, for keys.** Never ship provider API keys in client code (browser, mobile, desktop bundles). Proxy through your backend, which authenticates the user and enforces quotas.
- **Synchronous vs asynchronous.** User-facing interactive features: synchronous with streaming. Bulk processing (thousands of documents, nightly jobs): queue-based workers, and consider the provider's batch API, which is often substantially cheaper in exchange for higher latency.
- **Stateless calls.** Most chat APIs are stateless: you send the full conversation each time. Your application owns conversation state, storage, and truncation.

## Model selection

Decide along these axes, by testing on your own data:

| Axis | Questions |
|---|---|
| Quality | Does it pass the eval? Where does it fail? |
| Latency | Time to first token and total time at your typical input/output sizes |
| Cost | Input and output token prices; output tokens usually cost more; reasoning tokens may be billed |
| Context window | Fits your largest realistic input plus output with margin? |
| Features | Structured output, tool calling, vision/audio, caching, batch, streaming |
| Data terms | Retention, training use, residency, compliance certifications |
| Operational | Rate limits at your tier, uptime history, deprecation policy |
| Hosting | API vs self-hosted open-weight model (control and privacy vs ops burden) |

Heuristics:

- Start prototyping with a strong model to learn what is achievable, then try smaller models against the eval to find the cheapest that passes.
- Use different models for different steps: a small fast model for routing or classification, a stronger model for the hard generation step.
- Self-hosting open-weight models makes sense for strict data control, very high volume where GPU cost beats API cost, offline use, or need for custom fine-tunes — and it brings serving, scaling, and upgrade work. Do the total-cost arithmetic honestly.
- Pin model versions in production where the provider allows it, so behaviour does not shift under you. Track deprecation dates.

## Streaming

Stream whenever a human waits for more than a second or two of output.

- **Transport**: server-sent events or chunked HTTP are common; websockets when you need bidirectional streaming. Make sure every proxy, load balancer, and serverless platform in the path supports streaming and does not buffer.
- **Rendering**: render incrementally; handle partial markdown gracefully (unclosed code fences, half-written tables).
- **Structured output while streaming** is harder: either stream and parse at the end, use a streaming JSON parser, or stream a human-readable part and deliver structured data separately.
- **Cancellation**: when the user navigates away or presses stop, abort the upstream request to stop paying for tokens.
- **Errors mid-stream**: the response may fail after partial output. Decide how the UI shows that and whether to retry.
- **Moderation and validation** of streamed output can only be partial before completion. If output must be checked before display (for example, a regulated domain), buffer or check in chunks, accepting the latency cost.

## Structured output

When code consumes the output:

1. Use the provider's native schema-constrained output or tool-calling mode if available.
2. Define the schema once in code (e.g. Pydantic, Zod, JSON Schema) and generate the provider schema from it.
3. Validate the response against the schema *and* business rules (IDs exist, dates in range, enums valid).
4. On validation failure: retry once or twice with the validation error included, then fall back or fail loudly. Bound the retries.
5. Allow nullable fields for genuinely unknown values, or the model will fabricate.

Schema design tips: keep schemas shallow and fields well-named with descriptions; put free-text reasoning fields before decision fields when you want reasoning to inform the decision; prefer enums over free strings for categories.

## Tool calling plumbing

When the model can call functions:

- Validate every argument against the schema and against authorisation: the model choosing to call `refund(order_id)` does not mean the current user may refund that order. Authorisation is checked in your code with the *user's* identity, never the model's claim.
- Return tool errors to the model as informative results rather than crashing; it can often recover.
- Cap the number of tool-call rounds per request.
- Log every tool call with arguments and results.
- Require human confirmation for consequential or irreversible actions.

Tool design itself is covered in `ai-agents-and-tool-use`.

## Context management

The context window is a budget shared by system prompt, conversation history, retrieved documents, tool results, and the output.

- **Measure tokens**, do not estimate by characters. Use the provider's tokenizer or token-counting endpoint.
- **Reserve output space**: input + maximum output must fit within the limit.
- **Conversation history**: keep recent turns verbatim; summarise or drop older ones; keep pinned facts (user preferences, task state) in a structured block rather than relying on old turns.
- **Retrieved content**: include what is relevant, not everything that matched. More context is not free: it costs money and latency, and irrelevant context can degrade answers.
- **Tool results**: truncate or summarise large outputs before returning them to the model; return identifiers that let it fetch more if needed.
- **Long-context degradation**: models often attend less reliably to material in the middle of very long contexts. Put the most important material near the start or end, and test.

## Caching

Several distinct caches, often confused:

| Cache | What it saves | When to use | Risk |
|---|---|---|---|
| **Provider prompt/prefix caching** | Cost and latency on repeated prompt prefixes | Long stable system prompts, shared documents, multi-turn conversations | Only works if the prefix is byte-identical; put stable content first, variable content last |
| **Exact response cache** (your side) | Whole calls for identical inputs | Deterministic tasks with repeated inputs (classification of the same item) | Stale results when prompt or model changes — include prompt version and model in the key |
| **Semantic cache** (similar queries) | Calls for paraphrased queries | High-volume FAQ-like traffic | Returns a wrong answer for a subtly different question; needs careful thresholds and evaluation |
| **Intermediate result cache** | Embeddings, retrieval results, expensive tool outputs | Pipelines with reusable steps | Invalidation when source data changes |

Never share cached responses across users when the response may contain user-specific or permission-scoped data. Include the tenant and permission scope in the cache key.

## Cost and latency budgets

Make cost and latency explicit numbers, then engineer to them.

Cost per request ≈ (input tokens × input price) + (output tokens × output price) + (reasoning tokens if billed) + retrieval/embedding/tool costs, multiplied by the number of calls per user action, including retries. Then multiply by expected volume. Do this arithmetic with current prices before committing to a design; agent loops and fan-outs routinely cost ten times the naive estimate.

Levers, roughly in order of impact:

1. Fewer calls (merge steps, cache, skip the model when code can decide).
2. Smaller models for easy steps; route only hard requests to large models.
3. Shorter outputs (they are slower and usually pricier than inputs); ask for concise formats.
4. Prompt caching for stable prefixes.
5. Shorter inputs: trim history, retrieve less but better.
6. Batch APIs for non-interactive work.
7. Parallelise independent calls to cut wall-clock latency (cost unchanged).

Enforce budgets in code: per-request token caps, per-user and per-tenant quotas, alerts on spend anomalies. Runaway loops and abuse can generate surprising bills overnight.

## Resilience

- **Timeouts** on every call, sized to realistic p99 for that model and output length. A missing timeout turns a provider hiccup into a hung request.
- **Retries** on retryable errors only (rate limits, overloaded, transient network, 5xx), with exponential backoff and jitter, respecting any retry-after header. Do not retry on invalid-request errors; fix them.
- **Idempotency**: retries of calls that trigger side effects (tool actions) must not double-execute. Use idempotency keys in your own action layer.
- **Fallbacks**: a secondary model or provider for when the primary is down or rate-limited. Fallback models need their own prompts tested on the eval — prompts rarely transfer perfectly.
- **Graceful degradation**: decide what the feature does when no model is available — hide it, show cached results, queue the request, or fall back to a non-AI path.
- **Rate limit management**: client-side concurrency limits and queues so bursts do not trip provider limits; separate pools for interactive and batch traffic.
- **Circuit breakers** to stop hammering a failing provider.

## Logging, tracing, and privacy

Log per call: request ID, user/tenant (pseudonymised if needed), feature name, prompt template version, model and parameters, input and output (or hashes/redacted versions), tool calls, token counts, latency, cost, finish reason, errors, and any user feedback. Trace multi-step flows with a shared trace ID so a chain or agent run can be reconstructed. Dedicated LLM tracing tools exist (open-source and commercial); standard tracing (e.g. OpenTelemetry) also works.

Privacy and security:

- Never log API keys or secrets. Redact or tokenise PII where policy requires it before logging and, where feasible, before sending to the provider.
- Set retention periods for prompt/response logs; they often contain the most sensitive data in your system.
- Restrict who can read logs.
- Confirm the provider's data-retention settings match your obligations; some offer zero-retention options.
- Tell users when they are interacting with AI and what happens to their data, as law and policy require.

## Testing

- **Unit tests** with the model mocked: test your parsing, validation, routing, fallback, and error paths deterministically.
- **Recorded fixtures** (record real responses, replay in CI) for integration tests that should not hit the network.
- **Evaluation suites** against real models for quality: run on prompt or model changes and before releases (`llm-evaluation`).
- **Load tests** for rate-limit and concurrency behaviour.
- **Adversarial tests** for injection and abuse (`ai-safety-and-guardrails`).

Do not assert exact output strings from a live model; assert properties.

## Worked reasoning: estimating a feature before building it

Illustrative numbers only; substitute current prices from the provider's pricing page.

Suppose a "summarise this support thread" button. Typical thread: about 3,000 input tokens plus a 1,000-token system prompt; summary about 200 output tokens. Expected use: 20,000 clicks per day.

- Per call: 4,000 input + 200 output tokens. With a mid-tier model, input dominates here because outputs are short.
- The 1,000-token system prompt is identical across calls, so prefix caching can cut its cost and latency substantially if the provider supports it — but only if the system prompt comes first and contains no per-request values (no timestamps, no user names).
- Retries: assume a few percent of calls retry; budget for it.
- If the product later adds "re-summarise when a new message arrives", volume could multiply by the average number of messages per thread. Ask about this before signing off on the estimate; it is the kind of change that turns an affordable feature into an expensive one.
- Latency: a 200-token output streams quickly; the dominant cost is time to first token on 4,000 input tokens. A smaller model may halve that. Test both on the eval set before choosing.

The conclusion is not the number; it is knowing which assumptions drive it (thread length, trigger frequency, model tier) so the design can control them.

## Multi-tenant and conversational state

- **Conversation storage** is your responsibility. Store turns with IDs, timestamps, the model and prompt version that produced each assistant turn, and tool calls. This makes debugging and replay possible.
- **Tenant isolation**: per-tenant system prompts, retrieved documents, and caches must never leak across tenants. Enforce isolation in the data layer, not in the prompt.
- **User-editable instructions** (custom personas, "memory") are untrusted input — store, size-limit, and delimit them like any other user content.
- **Regenerate and edit**: if users can regenerate or edit earlier turns, decide whether downstream turns are discarded or branched, and model that explicitly in storage.
- **Deletion**: when a user deletes a conversation or account, delete it from logs, caches, and vector stores too, per your retention policy.

## Process for building a feature

1. **Frame the task.** What does the user get? What does good look like? What happens when the model is wrong — how costly is an error, and who catches it?
2. **Build a small eval set** (twenty to fifty realistic cases) before choosing a model or polishing prompts.
3. **Prototype the simplest architecture** with a strong model; check feasibility on the eval.
4. **Design the interface**: internal function signatures, schemas, error types.
5. **Add production plumbing**: timeouts, retries, validation, logging, budget enforcement, auth on the backend proxy.
6. **Optimise**: try cheaper models and caching against the eval; add streaming; parallelise.
7. **Add guardrails** proportional to risk.
8. **Ship behind a flag**, monitor quality signals, cost, latency, and errors; collect user feedback.
9. **Feed production failures back** into the eval set.

## SDKs and frameworks

- **Vendor SDKs** are the thinnest dependable layer: typed requests, streaming helpers, retries. Pin versions; read the changelog on upgrades, since parameter names and defaults change.
- **Multi-provider abstraction libraries** ease switching and fallback, but lag new vendor features and can hide provider-specific behaviour (caching controls, reasoning parameters). Use one when multi-provider support is a real requirement, and keep the escape hatch to call a provider directly.
- **Orchestration frameworks** (chains, agents, graph runners) speed prototyping but add abstraction that complicates debugging and upgrades. Adopt when their primitives match your design and the team will invest in understanding them; otherwise a few hundred lines of your own code around the SDK are often clearer.
- Whatever you choose, keep it behind your own internal interface (principle 2), so the choice is reversible.

## Pitfalls

- **Keys in the client.** Extracted within days; the bill is yours.
- **No timeout.** A slow provider exhausts your worker pool.
- **Unbounded retries or loops.** One bug becomes a large invoice.
- **Parsing free text with regex** when structured output was available.
- **Trusting tool-call arguments** as authorised.
- **Swapping models without re-running the eval.** Quality, format, and refusal behaviour change.
- **Caching across permission boundaries.** One user sees another's data.
- **Ignoring output tokens in cost estimates.** They dominate in generation-heavy features.
- **Context bloat.** Sending entire documents or full history "just in case", raising cost and lowering quality.
- **Rendering model output as raw HTML.** Cross-site scripting via injected content.
- **No non-AI fallback** for a critical path.
- **Hard-coded model names everywhere**, making deprecations a scavenger hunt. Centralise configuration.
- **Building an agent when a three-step workflow would do.**
- **Stale assumptions about prices and limits.** Always re-check current documentation.

## Quality bar and verification

Before calling an LLM feature done:

- Keys are server-side only; the backend authenticates and rate-limits users.
- Every model call has a timeout, bounded retries, and a defined failure behaviour visible to the user.
- Machine-consumed output is schema-validated and business-rule-checked.
- Tool calls are authorised in code against the real user's permissions.
- Cost per request and per month is estimated with current prices, and budgets are enforced in code.
- Latency meets the target at p95 on realistic inputs; streaming is used where users wait.
- Logs and traces allow reconstructing any request, with secrets and PII handled per policy.
- An eval set exists and passes; it runs on every prompt or model change.
- Model versions and configuration are centralised.
- Fallback or degradation path is tested by actually simulating provider failure.
