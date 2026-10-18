---
name: architecture-review
description: >-
  Evaluate a proposed or existing software design (design doc, RFC, ADR,
  architecture diagram, system proposal, or a running system's structure) and
  give a clear, reasoned verdict. Covers checking fit to requirements and
  quality attributes (scalability, reliability, security, latency, cost,
  operability, evolvability), finding risks and failure modes, probing
  assumptions, judging whether alternatives were genuinely considered, asking
  the questions that expose weak spots, and writing feedback with severity and
  a go / go-with-conditions / rethink outcome. Use when asked to "review this
  design", "critique this architecture", "poke holes in this RFC", "is this
  approach sound", "sanity-check our system design", or to prepare for a
  design review meeting. Not for producing a design from scratch
  (software-architecture, system-design) or reviewing a code diff
  (code-review).
metadata:
  category: quality
  related: software-architecture, system-design, technical-decision-making, security-audit, cloud-architecture, api-design, database-design, observability, requirements-analysis, estimate-effort
---

# Architecture Review

An architecture review asks whether a design will **meet its real requirements, under realistic conditions, at an acceptable cost and risk, and remain changeable** for as long as it needs to live. Its output is a decision (proceed, proceed with conditions, or rethink) backed by specific, prioritised concerns and the questions that must be answered.

Reviews are cheapest when the design is still on paper: changing a diagram costs an hour; changing a deployed system costs a quarter. That is why this skill emphasises probing assumptions early rather than polishing details.

Scope: this skill is for evaluating someone's design, including your own. To create a design, see `software-architecture` (structure, boundaries, patterns) and `system-design` (scaling distributed systems). For choosing between options in general, see `technical-decision-making`. For a dedicated security assessment, see `security-audit`. For a code diff, see `code-review`.

## Core principles

**1. Requirements first, design second.** A design is only good or bad relative to what it must achieve. Many review disagreements are really disagreements about requirements ("it must handle 10x growth" versus "we need it next month"). Establish the requirements and their priority before critiquing the solution, or you will argue past each other.

**2. Quality attributes decide architectures.** Functional requirements rarely determine structure; almost any architecture can implement the features. What separates designs is how they handle scale, latency, availability, consistency, security, cost, operability and change. Make the important attributes explicit and measurable.

**3. Every design is a set of trade-offs; find them.** There is no design without downsides. A proposal that lists none has not been examined. Your job is to surface the trade-offs, check they were chosen deliberately, and confirm they fit the priorities.

**4. Failure is the normal case at scale.** Networks partition, dependencies slow down, disks fill, deploys go wrong, humans misconfigure. Ask what happens when each component fails or degrades, not just whether it works.

**5. The simplest design that meets the requirements wins.** Complexity has carrying costs: more to operate, more to learn, more to break. Extra moving parts need a requirement that justifies them. "We might need it later" is a weak justification unless the cost of adding it later is very high.

**6. Reversibility sets the bar.** Decisions that are cheap to reverse (a library choice behind an interface) deserve a light review. Decisions that are expensive to reverse (data model, public API, storage engine, service boundaries, vendor lock-in) deserve a heavy one. Spend scrutiny where change is expensive.

**7. Context and constraints are real.** Team size and skills, existing systems, deadlines, budget and organisational standards are legitimate inputs, not excuses. A design that is ideal in the abstract but cannot be built or run by this team is not a good design for them.

**8. Give a verdict.** A review that lists thirty observations and no conclusion pushes the decision back to the author without help. Say clearly whether you would proceed, and what must change first.

## Discovering context

Before forming opinions, gather:

- **The problem statement and goals**: what is being solved, for whom, and how success is measured. If the document does not say, ask; this is often the most valuable review comment.
- **Requirements and constraints**: load and growth projections, latency and availability targets, data volumes, consistency needs, compliance obligations, budget, deadline, team capacity.
- **The current state**: existing systems the design replaces, integrates with, or depends on. Migration is frequently harder than the target design.
- **Organisational standards**: approved platforms, languages, data stores, security baselines, ADRs, and previous decisions this design should respect or explicitly revisit.
- **The review's purpose**: is this an early sanity check, a formal approval gate, or a post-hoc assessment of a running system? The depth and tone differ.
- **Who decides**: the reviewer advises; usually the owning team or an architecture group decides. Know which.

If you can inspect a running system or its code, check the claims in the design against reality (actual traffic, actual dependencies, actual failure history). Designs drift from documents.

## The review process

### 1. Restate the problem and the design

Write, in a few sentences, what problem the design solves and how it solves it. If you cannot, the document is unclear, and that is the first finding. Restating also catches misreadings before you build criticism on them. In a meeting, saying it aloud and asking "is that right?" is often revealing.

### 2. Extract and rank the quality attributes

Turn vague goals into concrete scenarios. "Highly available" is not reviewable; "checkout keeps accepting orders when the recommendation service is down" is.

| Attribute | Turn it into a scenario like… |
|---|---|
| Performance | p99 latency under X ms at Y requests per second with realistic payloads |
| Scalability | handles 10x current volume by adding instances, without redesign |
| Availability | survives loss of one zone with under N minutes of degraded service |
| Consistency | a user always sees their own writes immediately; others within N seconds |
| Durability | no acknowledged write is lost on single-node failure |
| Security | a compromised tenant credential cannot read another tenant's data |
| Operability | on-call can identify a failing dependency within 5 minutes from dashboards |
| Evolvability | adding a new payment provider touches one module and no schemas |
| Cost | infrastructure cost grows sub-linearly with users; under $X/month at launch |
| Compliance | personal data stays in region; deletion requests complete within N days |

Ask the authors to rank the top three to five. Conflicts between attributes (latency versus consistency, cost versus availability) are where the important trade-offs live.

### 3. Check fit: does the design achieve each scenario?

Walk each high-priority scenario through the design. Follow a request or a data item end to end: what components does it touch, what does each do, where is state held, what can fail? This is the architectural equivalent of tracing code with concrete inputs.

Useful lenses during the walk:

- **Data**: where is each piece of data owned, stored, replicated, cached, and derived? Who can write it? What is the source of truth? How is it migrated, backed up, deleted?
- **Coupling**: which components must change together, deploy together, or be up together? Synchronous call chains multiply latency and failure probability.
- **Boundaries**: do service or module boundaries align with how the domain and the teams actually change? Boundaries cut across a frequently-changing concept cause constant cross-team coordination.
- **Load**: where are the hot paths, fan-out points, and bottlenecks? Back-of-envelope numbers (requests per second, bytes per request, rows per day) quickly show whether a component is near its limits. See `system-design` for estimation.
- **State and consistency**: where are distributed transactions, dual writes, or caches that can diverge? What does a user see during a partial failure?

### 4. Probe failure modes

For each component and dependency, ask:

- What happens when it is down? Slow? Returning errors? Returning wrong data?
- Does failure cascade (retry storms, thread pool exhaustion, queue backlogs)? Are there timeouts, circuit breakers, bulkheads, and backpressure?
- What is the blast radius? One user, one tenant, one region, everything?
- How is it detected? How is it recovered? Is recovery automatic or does it need a human at 3 a.m.?
- What happens during deploys, schema migrations, and configuration changes, which cause a large share of real outages?
- What happens with poison messages, duplicate deliveries, and out-of-order events?
- What happens at the limits: disk full, quota exceeded, certificate expired, rate limit from a third party?

A pre-mortem is effective here: "It is a year from now and this system has had a serious incident. What was it most likely to be?" Ask the authors; their answers often reveal the risks they are quietly worried about.

### 5. Assess operability, security and cost

**Operability**: how is it deployed, configured, monitored, debugged, scaled and upgraded? Who is on call, and do they have the skills? Is there a runbook for the predictable failures? Are there dashboards and alerts on the scenarios from step 2? See `observability`.

**Security**: identify trust boundaries and where authentication, authorisation and data protection happen. Is sensitive data minimised and encrypted? Is the design multi-tenant, and how is isolation enforced? For anything handling sensitive data or money, recommend a focused threat model (see `security-audit`).

**Cost**: estimate the main cost drivers (compute, storage, data transfer, managed service pricing, licences, and people time to operate). Check how cost scales with load. Watch for designs whose cost is fine at launch and alarming at success, and for managed services priced per request at high volume.

### 6. Evaluate alternatives

Ask what other approaches were considered and why they were rejected. Healthy signs: at least one genuinely different alternative (not a straw man), including "do nothing" or "extend the existing system", with reasons tied to the ranked quality attributes.

If alternatives are missing, suggest one or two plausible ones yourself and ask how they compare. You are not trying to substitute your design; you are testing whether the chosen one survives comparison.

Common alternative axes worth raising:

- Build versus buy versus use an existing internal platform.
- Monolith or modular monolith versus separate services.
- Synchronous request/response versus asynchronous events or queues.
- One general data store versus specialised stores.
- Strong consistency versus eventual consistency with compensating actions.
- Incremental migration (strangler pattern) versus big-bang replacement.

### 7. Check the path, not just the destination

Many designs describe the target state and ignore how to get there. Ask:

- What is the migration plan from the current system? Can it be done incrementally with rollback at each step?
- How is data migrated and verified? Is there a period of dual running, and how are the two kept consistent?
- What is the smallest first milestone that delivers value and tests the riskiest assumption?
- Which decisions can be deferred until more is known?

### 8. Write the review and give the verdict

See "Writing the review" below.

## Asking the right questions

Good questions expose weak spots without putting authors on the defensive. They are specific, open, and tied to a requirement. A bank of questions, by area (pick what applies):

- **Requirements**: "What happens to this design if the load projection is wrong by 10x in either direction?" "Which of these goals would you give up first?"
- **Data**: "What is the source of truth for X? What happens if the cache and the database disagree?" "How do you delete a user's data across all these stores?"
- **Failure**: "Walk me through what a user sees when service B is down for ten minutes." "What retries what, and what stops a retry storm?"
- **Consistency**: "Is there a window where two services disagree about an order's state? What happens if a request lands in that window?"
- **Operability**: "How will on-call know this is broken before customers tell them?" "What is the rollback for a bad schema change?"
- **Evolution**: "What is the most likely change in the next year, and what would it touch?" "Which part would be hardest to replace?"
- **Cost**: "What does this cost per thousand users, and what dominates it?"
- **Team**: "Who will run this? Has the team operated this technology in production before?"
- **Alternatives**: "Why not extend the existing service?" "What would a version with half the components look like?"
- **Assumptions**: "What has to be true for this to work that we have not verified?"

Avoid questions that are really assertions ("Wouldn't it be better to use X?"). If you believe something, say it and give the reason; then ask what you are missing.

## Severity of concerns

Rank concerns so the authors know what must change. One workable scale (use the organisation's if it has one):

| Level | Meaning | Examples |
|---|---|---|
| Fundamental | The design does not meet a top-priority requirement, or rests on a false assumption. Proceeding would waste the investment | Synchronous fan-out to twelve services cannot meet the 200 ms latency target; chosen store cannot provide the transactional guarantees billing requires |
| Major | Significant risk that must be mitigated or explicitly accepted before proceeding | No plan for cross-region failover despite availability target; tenant isolation relies only on application code with no defence in depth |
| Moderate | Should be addressed during implementation; does not change the overall approach | Missing back-pressure on the ingestion queue; no defined data retention |
| Minor | Improvement or clarification | Diagram inconsistent with text; naming of components |
| Open question | Insufficient information to judge; needs an answer | Projected write volume unknown |

State the concrete scenario behind every fundamental or major concern. "This won't scale" is not reviewable; "at the projected 5k writes per second, a single primary with synchronous replication will saturate around 2k based on current benchmarks" is.

## Writing the review

A useful written review contains:

- **Summary and verdict** up front, in a few sentences. Typical outcomes:
  - *Proceed*: sound for its requirements; minor comments only.
  - *Proceed with conditions*: sound approach; specific major concerns must be addressed or explicitly accepted (list them and who decides).
  - *Rethink*: a fundamental concern means the approach should change; say which assumption or requirement breaks it and, if you can, what direction looks more promising.
  - *Cannot assess yet*: key information is missing; list exactly what is needed.
- **Your understanding** of the problem and design, briefly, so misreadings are visible.
- **Strengths**: what the design does well and should keep. This is not politeness; it prevents good parts being lost in revision.
- **Concerns**, ordered by severity, each with the scenario, the impact, and a suggested mitigation or the question that would resolve it.
- **Open questions** and assumptions to verify, ideally with how to verify them (a load test, a spike, a benchmark, a conversation with another team).
- **Risks accepted**: anything the authors have chosen to accept, recorded so the decision is explicit and revisitable.
- **Scope of your review**: what you did not assess (e.g. "did not review the mobile client or the cost model").

Keep tone collaborative. The authors usually know more about their domain than you; your contribution is a fresh, adversarial perspective. Disagree with specifics and evidence; acknowledge uncertainty where experts would reasonably differ.

## Decision guidance

**How heavy should the review be?**

| Signal | Light review | Heavy review |
|---|---|---|
| Reversibility | Behind an interface; can swap later | Data model, public API, vendor lock-in, service boundaries |
| Blast radius | One team, internal tool | Customer-facing, revenue, regulated data |
| Novelty | Well-trodden pattern for this team | New technology, new scale, new domain |
| Cost | Small, bounded | Large ongoing spend or headcount |
| Uncertainty | Requirements clear | Requirements contested or unknown |

**When to recommend a spike or prototype instead of more debate**: when the disagreement hinges on an empirical question (throughput of a component, latency of a provider, ease of a migration) that a few days of experiment can answer. Specify what result would settle it.

**When the design is fine but you would do it differently**: say so as a minor note or not at all. Preference is not a concern. Block only on requirements, risks and evidence.

**When reviewing an existing (running) system**: compare its current behaviour against current requirements, which may have shifted since it was built. Use incident history, performance data and change frequency as evidence of where the architecture is under strain. Recommendations should usually be incremental (see `legacy-modernization`).

## Worked example of review reasoning

A proposal: split a monolith's notification feature into a new service. The monolith will publish "notify" events to a queue; the new service consumes them and sends email, SMS and push via third-party providers. Stated goals: let the notifications team deploy independently, and stop provider slowness from slowing down the main app.

Reasoning a reviewer might go through:

1. **Restate**: the problem is coupling (deploys and latency), not scale. Good: the queue directly addresses latency coupling, and a separate deployable addresses deploy coupling.
2. **Quality attributes**: the authors rank independence and isolation first. Asking about delivery guarantees reveals a missing requirement: password-reset emails must arrive within a minute and must not be lost; marketing emails can be delayed. That distinction is absent from the design.
3. **Walk the scenario** "user requests password reset": the monolith writes a token to its database and publishes an event. If the process crashes between the write and the publish, the user never receives the email (a dual-write problem). Concern, *major*: suggest a transactional outbox or equivalent.
4. **Failure modes**: the email provider is down for 30 minutes. The consumer retries; does the queue keep reset emails behind 200k marketing emails? Concern, *major*: separate priorities or queues so critical messages are not starved.
5. **Duplicates**: the queue is at-least-once. Will users get two reset emails? Probably tolerable, but double-sent SMS costs money; ask for idempotency keys. *Moderate*.
6. **Data ownership**: the new service needs user contact preferences. The design reads them directly from the monolith's database. Concern, *major*: this keeps a hidden coupling (schema changes in the monolith break the service), undermining the main goal. Options: include needed fields in the event, or expose a read API.
7. **Operability**: who is paged when the dead-letter queue grows? The notifications team, but they have no alerting defined yet. *Moderate*.
8. **Alternatives**: "keep it in the monolith but make sends asynchronous via a background job" would solve the latency goal without the new deployable. The authors' reason for rejecting it (team autonomy, different release cadence) is legitimate; record it.

Verdict: *proceed with conditions*: address the dual write, priority isolation, and direct database access before implementation; the moderate items during it. Strengths noted: clear motivation, sensible use of a queue, a realistic incremental migration (one notification type at a time).

Note what made this review useful: it found a missing requirement, traced concrete failure scenarios, and checked whether the design actually achieved its own stated goal (decoupling), which the shared database quietly undermined.

## Running a review meeting

When the review is synchronous:

- Ask for the document in advance and read it before the meeting; meetings spent reading are wasted.
- Open by restating the problem and asking the authors to confirm the top quality attributes.
- Spend most of the time on the riskiest scenarios and open questions, not on presentation.
- Keep a visible list of concerns with severity as they arise, so the end of the meeting is a review of that list rather than a vague summary.
- End with the verdict, the conditions, owners for each open question, and when the design will be revisited.
- Send the written outcome afterwards; decisions made only in a meeting are forgotten or remembered differently.

## Reviewing your own design

When asked to review a design you produced (or an agent produced in the same session), the usual blind spots are stronger: you remember the intent and read it into the document. Compensate deliberately:

- Re-read the document as if you had only the text, and check that the problem, requirements and trade-offs are actually written down.
- Force at least one genuinely different alternative and argue for it as strongly as you can.
- Run the pre-mortem against yourself and list the three most likely ways it fails.
- Check every numeric claim with a quick calculation rather than recalling that it "seemed fine".
- State plainly what you are least sure about; that is what a human reviewer should look at first.

## Reviewing decision records and lightweight proposals

Not every review is a long design document. For an architecture decision record or a short proposal, the core questions compress to:

- Is the context (forces, constraints) stated, so a future reader understands why this was decided?
- Are the options real, and are the consequences, including the negative ones, listed?
- Is the decision reversible, and if not, is the evidence proportionate?
- Does it conflict with or supersede an earlier decision, and is that recorded?

A two-paragraph review is often right for these. Match the weight of the review to the weight of the decision.

## Pitfalls

- **Reviewing the diagram, not the system**: boxes and arrows look tidy while hiding synchronous dependencies, shared databases and unowned data. Ask what each arrow means (sync call, async message, shared store) and what happens when it fails.
- **Solution-first critique**: arguing about technologies before agreeing on requirements.
- **Unranked concerns**: a flat list where a fundamental flaw sits next to a naming nit.
- **Hand-waving at scale**: "won't scale" or "should be fine" without numbers. Do the back-of-envelope estimate.
- **Ignoring the migration**: approving an elegant target state with no realistic path from today.
- **Ignoring operations**: a design no one on the team can debug at 3 a.m. is a risk regardless of its elegance.
- **Gold-plating**: pushing for multi-region, event sourcing, or microservices when the requirements do not need them. Complexity is a cost you are imposing on the team.
- **Resume-driven review**: favouring fashionable technology over what the team knows.
- **Rubber-stamping**: approving because the authors are senior or the deadline is close.
- **Relitigating settled decisions** without new information.
- **No verdict**: leaving the authors to guess whether they may proceed.
- **Reviewer as designer**: rewriting the design in your own image instead of testing theirs.

## Quality bar and verification

A review is ready to send when:

- It states the requirements and quality attributes it reviewed against, and these were confirmed with the authors or flagged as assumptions.
- High-priority scenarios were walked end to end, including failure cases.
- Each fundamental or major concern has a concrete scenario and, where relevant, rough numbers.
- Alternatives were considered (by the authors, or suggested in the review).
- Operability, security and cost were each at least checked, with depth proportional to risk.
- The migration path was considered.
- Concerns are ranked, and there is a clear verdict with conditions.
- Uncertain judgments are labelled as such, with how to resolve them.
- Coverage gaps are stated.

Final check: if this design ships as written and fails, would the failure surprise you? If not, that risk belongs in the review.

## Depth on demand

- [references/failure-modes-and-tactics.md](references/failure-modes-and-tactics.md) — a catalogue of common distributed-system failure modes, the questions that expose each, and typical mitigations. Read when reviewing anything with multiple services, queues, caches or regions.

## Related skills

- `software-architecture`, `system-design` — producing and improving designs.
- `technical-decision-making` — structuring trade-off decisions and recording them.
- `security-audit` — focused threat modelling for sensitive designs.
- `cloud-architecture`, `database-design`, `api-design` — depth on specific layers.
- `observability` — judging whether a design can be operated.
- `requirements-analysis` — when the review exposes unclear or conflicting requirements.
- `estimate-effort` — sanity-checking the plan's timeline and cost.
