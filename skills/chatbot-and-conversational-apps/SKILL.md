---
name: chatbot-and-conversational-apps
description: >-
  Design and build chatbots, virtual assistants and voice or messaging
  applications end to end: conversation design, choosing between scripted
  flows, intent classification and LLM-driven dialogue, conversation state and
  memory, turn-taking, clarification, fallback and escalation to humans,
  channel constraints (web chat widgets, SMS, WhatsApp and chat platforms like
  Slack/Teams/Discord, voice/IVR), safety, analytics and evaluation. Use when
  someone wants to build a chatbot, support bot, assistant, conversational
  interface, Slack/Discord/Teams bot, SMS or WhatsApp bot, voice assistant or
  phone bot, or to fix a bot that misunderstands users, loops, or hands off
  badly.
metadata:
  category: app-generation
  related: llm-application-development, prompt-engineering, rag-systems, ai-agents-and-tool-use, llm-evaluation, ai-safety-and-guardrails, ux-writing, interaction-design, api-integrations-and-webhooks, observability
---

# Chatbot and Conversational Apps

A conversational app is a user interface where the user's input is unbounded and the interface must still behave predictably. That combination is the whole difficulty: users say anything, in any order, with typos, half-sentences and changes of mind, and the bot must still complete tasks, stay on topic, not make things up, and know when to stop and hand over to a person. Good conversational products are designed around the failures as much as the happy path.

## Scope

Covers: product and conversation design for bots and assistants; architecture choice (scripted, intent-based, LLM-driven, hybrid); dialogue state and memory; turn-taking and response design; fallback and human escalation; channel-specific constraints; integration with back-end systems; safety and privacy; analytics and evaluation.

Defers to: `llm-application-development` for LLM app plumbing in general, `prompt-engineering` for writing the system prompt, `rag-systems` for grounding answers in documents, `ai-agents-and-tool-use` for tool-calling loops, `llm-evaluation` for building eval suites, `ai-safety-and-guardrails` for guardrail design, `ux-writing` for the words themselves, `api-integrations-and-webhooks` for channel webhooks.

## Core principles

1. **Start from the jobs, not the technology.** List the concrete tasks users come to do (check order status, reset a password, book a slot, ask policy questions) and how often. A bot that does five high-volume jobs well beats one that chats about everything and completes nothing. Why: conversational scope is invisible to users — they will try anything — so the design must make the bot's actual capabilities discoverable and dependable.

2. **Conversation is a UI, so it needs affordances.** Users cannot see the menu in a text box. Tell them what the bot can do, offer suggestions or buttons where the channel supports them, and confirm what the bot understood before acting. Why: blank-box anxiety and misunderstood requests are the top causes of abandonment.

3. **Deterministic where it must be, generative where it helps.** Use structured flows and code for anything that moves money, changes accounts, collects consent or must follow regulation. Use language models for understanding messy input, answering open questions from trusted sources, and phrasing. Why: generative models are excellent at language and unreliable at guarantees.

4. **State is explicit.** Track what the bot knows about the conversation (goal, collected slots, confirmations, user identity, channel) in a data structure, not only implicitly in transcript text. Why: explicit state can be validated, persisted, resumed, handed to a human and debugged.

5. **Every path ends somewhere good.** Each conversation either completes the task, hands off to a human with context, or tells the user clearly where to go next. Dead ends, loops and "I didn't understand that" repeated three times are design bugs.

6. **The channel shapes the conversation.** A voice call, an SMS thread, a Slack thread and a web widget have different message lengths, latency expectations, rich-element support, identity signals and regulations. Design per channel; do not port a web widget's script to voice unchanged.

7. **Measure with real conversations.** Transcripts, task completion and escalation reasons are the ground truth. Designers' imagined dialogues miss most of what users actually say.

## Choosing the architecture

| Approach | How it works | Strengths | Weaknesses | Choose when |
|---|---|---|---|---|
| **Scripted / menu flows** | Buttons, keywords, decision trees | Predictable, auditable, cheap, works on every channel | Brittle with free text; feels rigid | Few tasks, regulated steps, low-tech channels (SMS keywords, IVR menus) |
| **Intent + slot (NLU)** | Classify utterance into intents, extract entities, drive a dialogue manager | Controllable, measurable per intent, fast | Needs training data per intent; out-of-scope handling is hard; long tail of phrasings | Moderate number of well-defined tasks, need for strict control, existing NLU platform |
| **LLM-driven** | A model reads the conversation and decides responses, possibly calling tools | Handles messy language, open questions, long tail, natural phrasing | Can hallucinate, drift off-policy, be prompt-injected; latency and cost; harder to guarantee flows | Open-ended Q&A over documents, assistance tasks, broad and varied requests |
| **Hybrid** (common default for new builds) | LLM for understanding and open answers; deterministic flows/tools for transactions and policy | Natural language with guarantees where they matter | More moving parts; must define the boundary clearly | Most production assistants with both Q&A and actions |

Hybrid patterns that work:

- **LLM as router**: the model classifies the request into a known task (or "open question" / "out of scope" / "human"), then a deterministic flow or a grounded answering path takes over.
- **LLM as slot filler**: a flow defines what must be collected; the model extracts slot values from free text and generates the next question; code validates values.
- **Tools behind policy**: the model may call tools, but tools enforce authorisation, validation and confirmation in code; the model never holds the authority.
- **Grounded answering**: answers to factual questions come only from retrieved, approved content, with the bot saying it does not know otherwise (see `rag-systems`).

If the project already uses a bot platform or framework (e.g. a cloud conversational AI service, an open-source dialogue framework, a channel's own bot SDK), work within it; it likely owns state, channel adapters and analytics.

### When not to build a chatbot

Say so when a conversation is the wrong interface:

- The task is a short, structured form (a chat that asks five fixed questions in order is a worse form).
- Users need to compare many options visually (tables, filters and galleries beat a chat transcript).
- The information is already easy to find and the real problem is navigation or search.
- There is no reliable back-end to act on, so the bot could only tell users to go elsewhere.
- The organisation cannot staff the escalation path or maintain the knowledge it draws on.

Often the best answer is a better page, search, or form plus a narrow bot for the remaining cases.

### Platform vs custom build

| Factor | Lean on a bot platform/service | Lean on a custom build |
|---|---|---|
| Channels | Many channels, standard features | One or two channels, unusual UX |
| Team | Conversation designers, few engineers | Engineering-heavy team |
| Control | Standard flows, built-in analytics and handoff acceptable | Need full control of model, data flow, hosting |
| Compliance | Platform offers required certifications/residency | Data must stay in your infrastructure |
| Lock-in tolerance | Acceptable | Low |

Either way, keep your conversation designs, test scenarios and knowledge content in a portable form so you can move.

## Process

### 1. Define jobs, users and boundaries

- List tasks with estimated volume, value and risk. Pick a first set that covers a large share of volume at manageable risk.
- Write what is **out of scope** and how the bot responds to it.
- Identify users and context: authenticated or anonymous, first-time or repeat, emotional state (support contacts are often frustrated), accessibility needs, languages.
- Decide the human fallback: is there a team, what hours, what channel, what queue, what wait times. A bot without a real escalation path must say so honestly.
- Gather real data: historical chat logs, support tickets, call transcripts, search queries, FAQs. They reveal actual phrasing and task distribution. Handle them as personal data (see Safety).

### 2. Discover context

- Existing bot? Read its flows/intents, prompts, tool definitions, state schema, and recent transcripts before changing anything. Find the analytics on where conversations fail.
- Brand voice and UX-writing guidelines: follow them for persona and tone; do not invent a persona if one exists.
- Back-end systems: which APIs the bot must call, their auth model, rate limits and failure modes.
- Channel accounts and constraints: which numbers, workspaces, pages; approval requirements (e.g. message templates on some messaging platforms, sender registration for SMS in many countries).
- Compliance: recording consent for voice, opt-in/opt-out rules for SMS, data residency, sector rules (health, finance, children).

### 3. Design conversations

- **Write sample dialogues** for each task: happy path, missing info, wrong info, change of mind, user asks something else mid-task, user goes silent, user is angry, user asks for a human. Read them aloud — voice designers do this for every prompt; it helps text too.
- **Define slots and validation**: what must be known to complete each task, how each is validated, and how to re-ask without repeating the same sentence.
- **Confirmation strategy** by risk: implicit confirmation for low-risk ("Okay, showing orders from March."), explicit for anything consequential ("Cancel order 4412 for $38.20? Yes / No").
- **Openings**: say what the bot is (users have a right to know they are talking to a bot in many jurisdictions and it sets expectations), and what it can help with, briefly.
- **Error and repair**: escalate gradually — rephrase the question, offer options, then offer a human. Never repeat the identical failure message.
- **Closings**: confirm the outcome, give references (order numbers, ticket IDs), and ask if anything else is needed only when that is useful.

See `references/conversation-design-patterns.md` for detailed patterns on prompts, repair and confirmations.

### 4. Model state and memory

Separate kinds of memory, each with its own lifetime and privacy rules:

| Memory | Contents | Lifetime | Notes |
|---|---|---|---|
| Turn context | The latest message and immediate history | Turn | What the model or NLU sees |
| Dialogue state | Current task, filled slots, pending confirmation, step | Conversation | Structured; persisted so conversations survive restarts and channel delays |
| Session/user profile | Identity, preferences, language, account links | Across conversations | Requires authentication; subject to consent and retention policy |
| Long-term memory (LLM assistants) | Facts the user asked to remember, summaries | User-controlled | Let users see and delete it; never store sensitive data without clear consent |
| Knowledge | Documents, policies, product data | Independent of user | Versioned; retrieved, not memorised |

Practical rules:

- Persist dialogue state keyed by conversation ID (and channel), not in process memory; channels deliver messages to whichever instance is up.
- For LLM conversations, manage the context window: keep the system instructions and current state fixed, summarise or trim older turns, and re-inject the structured state each turn rather than trusting the model to remember slots from far back.
- Define timeouts: when does a half-finished task expire? What does the bot say when the user returns a day later?
- Make state handoff-ready: a human agent should receive the task, collected slots, what the bot tried, and the transcript.

### 5. Build integrations and tools

- Back-end calls go through a server you control. Never let a client or a model call privileged APIs with credentials it holds directly.
- **Authorise in code**, per call, for the authenticated user; the model's opinion that the user is allowed is irrelevant.
- Make actions **idempotent** (channels redeliver webhooks; users double-tap buttons) and confirm before irreversible ones.
- Handle API failures in-conversation: tell the user what happened in plain language and what they can do; do not expose stack traces or internal IDs that mean nothing.
- Set timeouts below the channel's patience: many chat platforms expect a webhook acknowledgement within seconds; acknowledge immediately and respond asynchronously for slow work, with a typing indicator or "checking…" message where supported.

### 6. Implement fallback and escalation

Escalate to a human when:

- the user asks for one (always honour this, ideally immediately, at most after one attempt to route the request);
- repeated failure to understand (commonly two consecutive misses);
- detected frustration or distress;
- high-risk or sensitive topics (complaints, legal threats, safety, bereavement, vulnerability, medical or financial hardship);
- the task requires judgement or authority the bot lacks.

Good handoff: tells the user what happens next and roughly how long, transfers context so the user does not repeat themselves, works outside business hours (ticket, callback, or honest hours info), and lets the bot step back without interjecting while the human is active.

For emergencies or self-harm signals, provide appropriate crisis resources for the user's region immediately, and route per the organisation's safety policy; this must be designed with the organisation, not improvised by the model.

### 7. Adapt to the channel

| Channel | Key constraints | Design implications |
|---|---|---|
| Web/in-app widget | Rich UI possible (buttons, cards, forms, file upload); user may be anonymous | Use quick replies and forms for structured input; show typing; persist across page navigation; make it keyboard and screen-reader accessible |
| SMS | Plain text, segment length limits (longer messages split and cost more; non-Latin characters reduce per-segment length), no buttons, delivery delays, carrier rules, opt-in/out keywords | Very short messages; numbered options; honour STOP/HELP-style keywords as regulations require; sender registration where required |
| Messaging apps (e.g. WhatsApp, Messenger) | Templates and session windows on some platforms; rich elements vary; business verification | Plan template approval; handle the window rules for proactive messages |
| Team chat (Slack, Teams, Discord) | Threads, mentions, slash commands, interactive components, workspace permissions, rate limits, short acknowledgement deadlines | Reply in threads; avoid channel noise; request minimal scopes; ack fast, process async |
| Voice / IVR / phone | Speech recognition errors, no visual memory, barge-in, latency is felt acutely, recording consent | Short prompts, at most ~3 options at once, confirm critical values by reading back, allow interruption, keep response latency low, provide DTMF fallback, offer the operator early |
| Voice assistants / smart speakers | Platform invocation models and certification | Follow the platform's design guidelines; short turns |
| Email-style async | Long latency, long messages | Structure answers; one exchange should resolve as much as possible |

For voice in particular: write for the ear (front-load key info, no long lists, no URLs read aloud unless necessary), use spoken confirmations for numbers and names, handle silence with reprompts and a graceful exit, and measure end-to-end latency (recognition + reasoning + synthesis) — long pauses feel broken.

### 8. Safety, privacy and abuse

- **Disclose that it is a bot.** Many jurisdictions require it; it also calibrates expectations.
- **Prompt injection**: user messages, retrieved documents and tool outputs can contain instructions. Treat them as data; keep authority in code; constrain tools; never let the model reveal secrets it should not have (and preferably do not give it secrets at all). See `ai-safety-and-guardrails`.
- **Hallucination**: for factual or policy answers, ground in approved sources and prefer "I don't know, here is who can help" over a confident guess. Never let the bot invent prices, policies, legal or medical advice.
- **Personal data**: collect the minimum; avoid asking for full card numbers, passwords or government IDs in chat (redirect to secure flows); redact sensitive data in logs and transcripts; define retention; honour deletion requests; restrict who can read transcripts.
- **Authentication**: verify identity before revealing account information; channel identifiers (phone number, platform user ID) are evidence, not proof, depending on risk.
- **Abuse and misuse**: rate-limit per user, handle harassment gracefully, keep the bot from being used to generate off-topic content at your expense, and monitor for jailbreak attempts.
- **Children and vulnerable users**: if they may use the bot, involve the organisation's policy and legal guidance.

### 9. Evaluate and iterate

Before launch:

- **Scenario tests**: scripted multi-turn conversations for each task and each failure path, run automatically on every change (prompt, model, flow, knowledge). Assert on outcomes (task completed, correct tool call with correct arguments, escalation triggered), not exact wording.
- **Understanding tests**: a labelled set of real utterances per task/intent including out-of-scope ones; track accuracy and confusion between tasks.
- **Grounding tests** for Q&A: questions with known answers from the knowledge base and questions whose answer is not in it (the bot must decline).
- **Adversarial tests**: injection attempts, requests to break policy, abusive messages, attempts to extract other users' data.
- **Channel tests**: real devices and real accounts on each channel (SMS splitting, voice recognition of names and numbers, rendering of rich elements).

After launch:

| Metric | What it tells you | Caveat |
|---|---|---|
| Task completion / containment | Share of conversations resolved without a human | High containment can hide users giving up; pair with satisfaction and repeat-contact rate |
| Escalation rate and reasons | Where the bot falls short | Distinguish user-requested from bot-triggered |
| Fallback/misunderstanding rate | NLU or prompt gaps | Review the actual utterances |
| Drop-off point | Which step loses users | Often a confusing question or a request for information users lack |
| Repeat contact within N days | Whether "resolved" was real | Needs identity linking |
| User satisfaction (CSAT/thumbs) | Perceived quality | Low response rates, biased toward extremes |
| Latency | Perceived responsiveness | Measure per channel, end to end |
| Cost per conversation | Viability | Include model, channel and human handoff costs |

Review transcripts weekly (sampled, with privacy controls): read failures, cluster them, fix the top clusters, add them to the test set. See `llm-evaluation` for building judged evaluations.

## Operating the bot

- **Version everything that changes behaviour** — flows, prompts, model identifiers, knowledge snapshots, tool schemas — and record which versions served each conversation, so a bad transcript can be traced to its cause.
- **Release gradually**: route a percentage of traffic to the new version and compare completion, escalation and satisfaction before full rollout.
- **Keep a kill switch** that routes all traffic to a safe fallback (scripted menu or straight to humans) if the bot misbehaves or a dependency fails.
- **Monitor** error rates, latency, escalation spikes and unusual topics; alert on sudden changes (see `observability`).
- **Keep knowledge fresh**: an outdated policy answer is worse than none. Assign an owner and a review cadence for every content source the bot uses.

## Building the LLM-driven parts well

When a language model handles part of the dialogue, most quality comes from the surrounding structure rather than prompt wording:

- **Instructions the model receives** should cover: who it serves and what it can do; what it must not do; how to use each tool and when; how to behave when unsure (ask a clarifying question vs. hand off); tone and length per channel; and the current structured state. Keep policy that must hold in code as well — the prompt states it, the code enforces it.
- **Give the model state, not just history.** Each turn, include the current task, filled and missing slots, the authenticated user's relevant facts, and any pending confirmation. Models are better at acting on an explicit state summary than at reconstructing it from a long transcript.
- **Structured outputs for decisions.** When the model routes or extracts, have it return a structured object (task, slots, confidence or "unsure", whether to escalate) that code validates, rather than parsing prose.
- **Constrain tools narrowly.** `get_order_status(order_id)` for the authenticated user is safe; `run_sql(query)` is not. Tools validate arguments and ownership and return minimal data.
- **Clarify rather than guess** when the request is ambiguous between tasks with different consequences; guess (and state the assumption) when the cost of being wrong is trivial.
- **Streaming** improves perceived latency in web chat; on channels that cannot stream (SMS, most platform bots), send a brief acknowledgement for slow operations.
- **Pin and test model versions.** A model upgrade changes behaviour across every conversation; run the scenario suite before switching.
- **Cost control**: route simple, high-volume tasks through cheaper paths (deterministic flows, smaller models), cap conversation length, and cache retrieval where appropriate.

## Proactive and outbound messaging

Bots that message first (reminders, notifications, outbound calls, follow-ups) carry extra obligations:

- Obtain and record consent for the channel and purpose; many regions regulate unsolicited SMS, calls and messaging-app contact strictly, including time-of-day limits.
- Provide an easy opt-out in every message where required, and honour it immediately across systems.
- Make the first message self-explanatory: who is contacting, why, and what the user can reply.
- Expect replies at any time, including long after the message — the bot must recognise what the reply refers to.
- Throttle sends and respect platform rate limits and template rules.

## Multilingual and inclusive conversations

- Detect or ask for language early; keep the choice in state; respond consistently in it.
- Translate flows and prompts with native review; machine translation of scripted prompts often produces stilted or wrong phrasing for the domain.
- Make sure the human escalation path supports the languages the bot claims.
- Avoid idioms, sarcasm and culturally specific references in core flows.
- Support users with low literacy, cognitive differences or screen readers: plain language, short sentences, clear choices, no time pressure, accessible widget controls (see `accessible-design`).
- For voice, test recognition with diverse accents and speech patterns; offer keypad or text alternatives.

## Worked example: retail support assistant

Request: "Build a chatbot for our online store's website to reduce support tickets."

Reasoning:

1. **Jobs** from last quarter's tickets: order status (40%), returns (20%), delivery problems (15%), product questions (15%), other (10%). First release: order status, return initiation, product/policy Q&A; everything else routes to human.
2. **Architecture**: hybrid. Model routes and extracts; order status and returns are deterministic flows using tools against the order system; product and policy questions use retrieval over the help centre and product catalogue with refusal when unsupported.
3. **Identity**: order status requires either sign-in or order number plus email; tools enforce that the order belongs to the verified customer.
4. **Confirmation**: starting a return is consequential → explicit confirmation listing item and refund method.
5. **Fallback**: two misunderstandings or any request for a person → handoff to the support inbox with summary; outside hours, create a ticket and give the expected response time.
6. **Channel**: web widget, so quick-reply buttons for the top tasks in the opening, accessible keyboard navigation, conversation persists across page navigation.
7. **Evaluation**: 60 scripted scenarios from real tickets (including angry customers, wrong order numbers, items outside the return window), 200 labelled real first messages for routing accuracy, 50 policy questions with known answers plus 20 with none, an injection set. Launch to a percentage of traffic; review transcripts weekly; track repeat contact within 7 days.

## Response design

- Lead with the answer or the next step; keep messages short for chat, shorter for SMS and voice.
- One question per turn when collecting information; multiple questions per message get partial answers.
- Offer choices when the set is small and known; accept free text anyway.
- Use the user's words back to them in confirmations so misunderstandings surface.
- Vary repeated prompts slightly; identical re-asks feel robotic and signal a loop.
- Match persona to brand and context but keep it subordinate to clarity; jokes during a billing dispute land badly.
- Formatting: use what the channel renders (markdown in some chat platforms, none in SMS, SSML for voice where supported). Test rendering — raw asterisks and broken links undermine trust.
- Be honest about limits ("I can't change delivery addresses, but I can connect you with someone who can").

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Bot loops "I didn't understand" | No repair escalation | Rephrase → options → human after two misses |
| Users ask for a human immediately | Bot hides capabilities or past experiences were poor | Clear opening, quick wins, honour handoff requests promptly |
| Bot confidently states wrong policy | Ungrounded generation | Ground answers in approved sources; decline when absent |
| Bot performs an action the user didn't intend | Weak confirmation, ambiguous slot extraction | Explicit confirmation for consequential actions; read back values |
| Context lost mid-conversation | State in memory, instance restart, or context trimming dropped slots | Persist structured state; re-inject it every turn |
| Duplicate orders/messages | Webhook redelivery, double taps | Idempotency keys; dedupe inbound message IDs |
| Works in web, fails in SMS/voice | Script designed for one channel | Channel-specific prompts and limits |
| Prompt injection via pasted text or documents | Model treats data as instructions; tools trust model | Keep authority in code; constrain tools; test adversarially |
| Handoff makes users repeat everything | No context transfer | Pass summary, slots and transcript to the agent |
| Platform rejects or throttles the bot | Missed ack deadlines, excess scopes, rate limits, unregistered senders | Ack fast; minimal scopes; backoff; complete registration |
| Metrics look good, complaints rise | Containment counted as success when users abandon | Track repeat contacts and satisfaction alongside containment |

## Quality bar and verification

- [ ] Each in-scope task has been completed end to end in the real channel (not just a simulator), including the back-end effect.
- [ ] Each failure path in the sample dialogues was exercised: missing info, invalid info, change of mind, off-topic, silence, frustration, "talk to a human".
- [ ] Out-of-scope and unanswerable questions get honest, helpful responses rather than invented answers.
- [ ] Consequential actions require explicit confirmation and are authorised and validated in code.
- [ ] Handoff delivers context to the human side and sets user expectations, including outside staffed hours.
- [ ] Automated multi-turn scenario tests and adversarial tests run on every change and pass.
- [ ] Logs and transcripts redact sensitive data; retention and access are defined.
- [ ] Bot disclosure, consent (recording, SMS opt-in) and opt-out mechanisms work as required for each channel and region.
- [ ] Latency per channel is within user tolerance under realistic load.

If you cannot test on a real channel in your environment, state that clearly and give the user the exact test conversations to run.

## Depth on demand

- `references/conversation-design-patterns.md` — read when writing prompts, re-prompts, confirmations, disambiguation and handoff messages, or when reviewing transcripts for design fixes.
