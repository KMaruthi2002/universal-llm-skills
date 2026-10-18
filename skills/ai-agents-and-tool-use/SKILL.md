---
name: ai-agents-and-tool-use
description: >-
  Design, build, and debug LLM agents and tool-using systems: deciding between
  a fixed workflow and an autonomous agent, the agent loop and its stopping
  conditions, designing tools (names, schemas, descriptions, return values,
  error messages), planning, short- and long-term memory, multi-agent
  orchestration and delegation, human-in-the-loop approval, guardrails on
  actions, cost and runaway control, and tracing. Use when building an agent,
  giving a model function or tool calling, writing tool definitions,
  orchestrating sub-agents, or when an agent loops, picks the wrong tool,
  hallucinates tool arguments, or takes unsafe actions. For MCP server
  specifics use mcp-server-development; for general LLM plumbing use
  llm-application-development.
metadata:
  category: ai-ml
  related: llm-application-development, prompt-engineering, mcp-server-development, ai-safety-and-guardrails, llm-evaluation, rag-systems, workflow-automation, api-design, observability
---

# AI Agents and Tool Use

An agent is a model running in a loop: it observes, decides on an action (usually a tool call), receives the result, and repeats until it judges the task done. That loop is powerful because the model chooses the path, and dangerous for the same reason. Good agent engineering is about giving the model excellent tools and clear goals, bounding what it can do, and making every step visible.

## Scope

Covers: workflow-vs-agent decisions, loop design, tool design, planning, memory, multi-agent patterns, human approval, action guardrails, cost control, and testing agents.

Neighbours: `mcp-server-development` (exposing tools via the Model Context Protocol), `llm-application-development` (API plumbing, streaming, retries), `prompt-engineering` (system prompt wording), `ai-safety-and-guardrails` (threat model, injection), `llm-evaluation` (measuring agent success), `workflow-automation` (non-LLM automation).

## Workflow or agent?

The most important decision, and most often made wrongly in the agent direction.

| Factor | Prefer a **workflow** (fixed steps, model used inside steps) | Prefer an **agent** (model chooses steps) |
|---|---|---|
| Step sequence | Known in advance | Depends on what is discovered along the way |
| Variability of inputs | Low to moderate | High; open-ended tasks |
| Need for predictability, auditability | High (compliance, finance) | Tolerates variation |
| Cost and latency sensitivity | High | Can afford extra calls |
| Error tolerance | Low | Errors are recoverable or reviewed |
| Testing | Easy per step | Harder; requires trajectory-level evaluation |

Middle grounds are often best: a workflow with one agentic step ("research this sub-question with up to five searches"), or an agent restricted to a small toolset with mandatory checkpoints. Start with the simplest structure, and add autonomy only where measurement shows the rigid version fails.

## Core principles

### 1. Tools are an interface for a model user — design them like a good API

The model knows only the tool's name, description, and schema. It cannot read your source code. Vague names, ambiguous parameters, and silent failures produce wrong calls. Invest in tool design as you would in a public API — arguably more, because this user cannot ask questions.

### 2. The environment's feedback drives the loop

Agents improve their next step based on tool results. Results that are informative (clear errors, relevant data, hints about what to do next) make the agent self-correcting. Results that are empty, huge, or cryptic make it flail.

### 3. Bound everything

Maximum iterations, maximum tokens, maximum wall-clock time, maximum spend, and a limited set of permitted actions. An unbounded agent will eventually loop, and a looping agent with a credit card is an incident.

### 4. Authority stays with the system, not the model

The model proposes actions; your code decides whether they are allowed. Authorisation uses the real user's identity and permissions. Consequential or irreversible actions need explicit human confirmation or a policy check outside the model. Anything the agent reads (web pages, emails, documents, tool outputs) can contain injected instructions; the agent's privileges should be such that obeying an injection cannot cause serious harm.

### 5. Make the trajectory observable

Every thought (where exposed), tool call, argument, result, and decision must be logged and replayable. Agent bugs are trajectory bugs: the failure is often several steps before the visible symptom.

### 6. Fewer, better tools beat many overlapping ones

Each additional tool adds selection ambiguity and context cost. Overlapping tools (three ways to search) cause inconsistent choices. Consolidate where tools serve one intent.

## Discovering context

- What task does the agent accomplish, and how is success judged? Write down three to five realistic tasks end to end, including a failure case.
- What actions are needed, and which of them are reversible, consequential, or external (sending messages, spending money, deleting, deploying)?
- What systems will the tools touch, and what credentials and scopes are available? Can you get narrower ones?
- Who is the human in the loop, if any, and how fast can they respond?
- What does the harness or framework already provide (loop, tool registry, memory, tracing)? Use the project's existing framework conventions if there is one. Check current documentation for the model's tool-calling format, parallel tool calls, and limits.
- Budgets: acceptable cost and time per task.

## The agent loop

A minimal loop:

1. Build context: system prompt (goal, rules, tool guidance), task, relevant memory, history so far.
2. Call the model with tool definitions.
3. If it requests tool calls: validate arguments, check authorisation and policy, execute (possibly in parallel if independent), capture results or errors, append to history.
4. If it returns a final answer, or a stop condition triggers, exit.
5. Otherwise go to 1.

Design decisions in the loop:

- **Stopping conditions**: model declares completion; iteration, token, time, or cost cap reached; repeated identical calls detected (loop detection); unrecoverable error; human cancels. When a cap is hit, end gracefully with a summary of progress, not a crash.
- **Definition of done**: tell the model concretely what "done" means and to verify it (run the tests, re-read the file, confirm the record was saved) before declaring completion. Agents often declare victory early.
- **Parallel tool calls**: allow them for independent reads; serialise writes and dependent steps.
- **Error recovery**: return errors as tool results; let the model retry with corrected arguments a bounded number of times.
- **Context growth**: long trajectories overflow context. Truncate or summarise old tool results, keep a running task state (plan, progress, findings), and drop raw data already used.

## Tool design

### Names

- Verb-object, specific, unambiguous: `search_orders`, `get_order_by_id`, `cancel_order`. Not `orders`, `handle`, `do_action`.
- Consistent naming scheme across tools; namespace by system when many exist (`crm_search_contacts`, `billing_get_invoice`).

### Descriptions

The description is the most important part. Write it for a capable newcomer:

- what the tool does and returns;
- **when to use it, and when not to** (and which tool to use instead);
- important constraints (rate limits, side effects, irreversibility, cost);
- the meaning and format of each parameter, with an example value;
- common mistakes to avoid.

Several clear sentences are normal; a one-line description is usually too thin.

### Parameters and schemas

- Use precise types, enums for closed sets, formats for dates and IDs, required vs optional clearly marked, and sensible defaults.
- Accept natural identifiers the model will actually have (an email, an order number) rather than internal surrogate keys it must first look up — or provide the lookup tool.
- Avoid parameters that require the model to compute something error-prone (offsets, encoded strings). Do it in the tool.
- Keep the number of parameters small; split tools that have modes controlled by a flag into separate tools when the modes have different semantics.
- Make destructive behaviour explicit in the tool's identity (`delete_file`), never a hidden flag on an innocuous-sounding tool.

### Return values

- Return what the model needs for its next decision, in a compact, readable form. Raw API dumps with dozens of irrelevant fields waste context and confuse.
- Prefer human-meaningful fields (names, titles, statuses) alongside IDs.
- Paginate or truncate large results, and say so in the result ("showing 20 of 340; refine the query or request page 2").
- Include next-step hints when helpful.

### Errors

Errors are instructions for recovery. Compare:

- Poor: `Error 400`.
- Good: `No customer found with email "jon@exmple.com". Check spelling or search by name with search_customers.`

Distinguish errors the model can fix (bad argument) from ones it cannot (service down, permission denied), so it can decide to retry, change approach, or stop and report.

### Idempotency and side effects

- Reads should be safe to repeat.
- Writes should be idempotent where possible (idempotency keys, upserts), because agents retry.
- Long-running operations: return a job ID and provide a status tool rather than blocking.

### Test tools with the model, not just with code

Give the model realistic tasks and read the trajectories. Where it picks the wrong tool, passes bad arguments, or misreads results, revise names, descriptions, and outputs. This tool-description iteration is one of the highest-return activities in agent work.

## Planning

- For multi-step tasks, asking the agent to write a short plan first (and to update it as it learns) improves coherence and gives you a checkpoint for human review.
- Keep plans as explicit state (a list with statuses) in context or in a scratch file, not only implicit in reasoning.
- Re-plan on surprises; do not let the agent stubbornly follow a plan that tool results have invalidated.
- For high-stakes tasks, have a human approve the plan before execution.

## Memory

| Kind | What it is | How to implement |
|---|---|---|
| **Working memory** | The current context: task, plan, recent steps | The prompt; manage by truncation and summarisation |
| **Task state / scratchpad** | Notes, findings, progress for this task | A structured block in context or a file/tool the agent writes to |
| **Long-term memory** | Facts and preferences across sessions | A store (database, files, vector index) with explicit read/write tools or automatic retrieval |
| **Episodic memory** | Records of past tasks and outcomes | Logs indexed for retrieval; useful for learning from past failures |

Cautions for long-term memory: it can store wrong or injected facts that then persist; it accumulates stale information; it may hold personal data subject to deletion requests. Make memory inspectable and editable by users, validate what is written, scope it per user or tenant, and expire it.

## Multi-agent orchestration

Patterns:

- **Orchestrator–workers**: a lead agent decomposes the task and delegates sub-tasks to worker agents (often with narrower tools and fresh context), then synthesises. Good for broad research or parallelisable work.
- **Pipeline of specialists**: fixed sequence of agents with different roles (draft, review, fix).
- **Generator–critic**: one produces, another evaluates against criteria; loop until pass or cap.
- **Routing**: a classifier dispatches to specialised agents.

Benefits: parallelism, clean context per sub-task, specialised prompts and tools. Costs: more tokens (often several times a single agent), coordination failures, lost context between agents, harder debugging.

Make delegation work:

- Give each sub-agent a self-contained brief: the goal, the context it needs, constraints, the expected output format, and what not to do. Sub-agents do not share the orchestrator's history unless you pass it.
- Define the hand-back format so the orchestrator can merge results.
- Avoid duplicated work by assigning non-overlapping scopes.
- Cap the number of agents and depth of delegation.
- Do not use multi-agent architectures for tasks a single agent handles well; measure.

## Human in the loop

Choose the intervention points by consequence:

| Action class | Examples | Control |
|---|---|---|
| Read-only, internal | Search, read files, query | Autonomous |
| Reversible writes | Draft a document, create a branch, stage changes | Autonomous with logging, or batch review |
| Consequential or external | Send email, post publicly, merge to main, modify production data | Explicit approval per action, showing exactly what will happen |
| Irreversible or financial | Delete data, transfer money, purchase, change permissions | Approval with strong confirmation; often better left to humans entirely |

Approval UX matters: show the concrete action and its parameters ("Send this email to these three recipients"), not "Agent wants to use send_email". Approvals must happen in a channel the agent cannot spoof, and an approval covers one action, not a category.

## Guardrails on actions

- **Least privilege**: give tools the narrowest credentials and scopes that work. Separate read tools from write tools so read-only agents simply do not have write tools.
- **Allowlists** for destinations (domains, recipients, file paths, database tables).
- **Policy checks in code** before execution: amount limits, rate limits, business rules.
- **Sandboxing** for code execution: isolated containers or VMs, no network or restricted network, resource limits, no access to host secrets.
- **Dry-run modes** that show what would happen.
- **Injection containment**: treat content from tools as data; after the agent reads untrusted content, consider restricting its ability to take consequential actions in the same run, or requiring approval.
- **Audit logs** of every action, who approved it, and the triggering context.

See `ai-safety-and-guardrails` for the broader threat model.

## Cost and runaway control

- Track tokens and cost per run; enforce caps.
- Detect loops: same tool with same arguments repeatedly, or no progress over several steps.
- Prefer cheaper models for simple sub-tasks (routing, extraction, summarising tool output) and stronger models for planning and hard reasoning.
- Summarise large tool outputs before they enter context.
- Cache deterministic tool results within a run.

## Evaluating agents

- Build a set of realistic tasks with checkable outcomes (the file contains X, the ticket has status Y, the answer matches).
- Measure: task success rate, steps and cost per success, rate of unsafe or unauthorised action attempts, how often it asks for help appropriately.
- Run each task several times; agent outcomes vary run to run, and a single pass proves little.
- Read trajectories for failures; classify by cause (wrong tool, bad arguments, misread result, premature stop, loop, plan error, injection).
- Test in a sandboxed copy of the environment, never against production systems.

See `llm-evaluation`.

## Writing the agent's system prompt

The system prompt is the agent's job description. It should cover, in whatever structure suits the project:

- the goal and what success looks like, including how to verify it;
- the environment: what systems exist, what the tools are for, any conventions (file layout, naming, where outputs go);
- autonomy level: which decisions to make alone, when to ask, which actions always need confirmation;
- how to handle uncertainty, missing information, and tool failures;
- how to report results: what to include, how to state what was and was not verified;
- the rule that content read through tools is information, not instructions.

Keep tool-specific guidance in the tool descriptions where possible, so it travels with the tool. See `prompt-engineering` for wording.

## Worked reasoning: improving a tool from trajectories

Illustrative. An internal support agent has a tool `lookup(q)` described as "Look up customer info." In trajectories, the agent:

- passes full sentences ("find the customer who emailed about the broken charger") and gets no results;
- calls it repeatedly with slight variations;
- sometimes uses it to search orders, which it does not support, and then claims the order does not exist.

Diagnosis: the name and description hide what the tool accepts and covers; the empty result gives no guidance; the model cannot tell "no match" from "wrong tool".

Revision:

- Rename to `find_customer`; describe that it matches on exact email, phone, or customer ID, or fuzzy-matches names; state that it does *not* search orders and point to `search_orders` for that.
- Schema: separate optional fields `email`, `phone`, `customer_id`, `name`, at least one required.
- Results: up to five matches with name, email, plan, and customer ID; on no match, return "No customer matched name='…'. Try email or phone, or check spelling." 
- Add loop detection: three consecutive calls with no results ends the step with a request for more information from the user.

Re-running the same tasks: fewer calls per task, no false "order does not exist" claims. The change was entirely in the interface, not the model or the main prompt — which is typical.

## Computer-use and browser agents

Agents that operate a GUI or browser (screenshots, clicks, typing) are the least predictable kind: slow, sensitive to layout changes, and exposed to every piece of text on every page they visit.

- Prefer an API or a structured tool over GUI automation whenever one exists.
- Run in an isolated browser profile or VM without the user's saved credentials or sessions, unless the task requires them and the user agrees.
- Treat all on-page text as untrusted; require confirmation before submitting forms, purchasing, sending, or changing settings.
- Never let the agent enter passwords, payment details, or government identifiers on the user's behalf unless the system has an explicit, user-controlled mechanism for it.
- Record screenshots or step logs for review.

## Choosing a framework or building the loop yourself

Agent frameworks and harnesses provide loops, tool registries, memory, tracing, and multi-agent primitives. They save time when their model of the world matches yours. A hand-written loop around a vendor SDK is short, transparent, and easy to bound and debug. Prefer what the project already uses; otherwise start with the simplest option that provides tracing and caps, and check that whichever you choose lets you see and control every model call and tool execution.

## Pitfalls

- **Building an agent for a fixed workflow.** Slower, costlier, less reliable.
- **Thin tool descriptions** that do not say when to use the tool.
- **Huge raw tool outputs** flooding the context.
- **Opaque errors** leaving the agent nothing to recover with.
- **No iteration or cost cap.**
- **Premature "done"** without verification.
- **Overlapping tools** causing inconsistent choices.
- **Authorisation by model judgement** ("only refund if the user is eligible" in the prompt rather than in code).
- **Broad credentials** (admin tokens) given to an agent that reads untrusted content.
- **Approval prompts that hide the actual action.**
- **Sub-agents without enough context**, which then redo work or go off-scope.
- **Persisting unvalidated memory**, letting one injected fact affect future sessions.
- **Testing once** and assuming reliability.
- **Running evaluation against production.**

## Quality bar and verification

An agent is ready when:

- The workflow-vs-agent choice is justified; autonomy exists only where needed.
- Every tool has a specific name, a description including when (not) to use it, a precise schema, compact results, and actionable errors — and these were refined by reading real trajectories.
- Loops have iteration, token, time, and cost caps with graceful termination.
- Authorisation and policy are enforced in code with the real user's identity; credentials are least-privilege.
- Consequential and irreversible actions require explicit, specific human approval.
- Code execution is sandboxed.
- Every run is traced and replayable.
- Success rate, cost, and unsafe-action rate are measured over repeated runs on a realistic task set in a sandbox.
- Long-term memory, if any, is scoped, inspectable, editable, and expires.
