---
name: requirements-analysis
description: >-
  Elicit, analyse, and specify requirements for a system, product, feature,
  process, or procurement: identifying stakeholders and their goals,
  separating needs from proposed solutions, capturing functional and
  non-functional (quality) requirements and constraints, modelling use cases
  and scenarios, finding edge cases and error paths, detecting and resolving
  conflicts, prioritising, maintaining traceability, and turning vague asks
  into precise, testable requirements. Use when asked to gather or analyse
  requirements, write a requirements or specification document, review
  requirements for gaps, scope a system or integration, prepare acceptance
  criteria, compare vendor responses against needs, or when stakeholders
  disagree about what is needed. For quickly clarifying a single task
  request use clarify-requirements; for product requirement documents use
  product-requirements; for backlog stories use user-stories.
metadata:
  category: analysis
  related: clarify-requirements, product-requirements, user-stories, ux-research, qa-test-planning, system-design, software-architecture, roadmap-and-prioritization
---

# Requirements Analysis

Requirements analysis turns what people say they want into a precise, shared, testable statement of what a solution must do and how well. Most failed projects did not fail at building; they built the wrong thing, or the right thing without the qualities (performance, security, usability, compliance) that mattered, or something nobody could agree was finished. This skill is how to prevent that.

## Scope

Covers: requirements for software systems, features, integrations, data and reporting, internal processes, and procurements — from elicitation through analysis, specification, validation, and change management. Applies to plan-driven and iterative development alike; only the timing and level of detail change.

Does not cover:

- Clarifying a single ambiguous request before doing a task → `clarify-requirements`.
- Writing a product requirements document with strategy, goals, and launch context → `product-requirements` (uses this skill's techniques).
- Writing backlog items in story form → `user-stories`.
- Researching users' behaviours and needs in depth → `ux-research`.
- Designing the solution → `system-design`, `software-architecture`.
- Planning tests from requirements → `qa-test-planning`.

## Core principles

1. **Separate the need from the proposed solution.** Stakeholders usually express requirements as solutions ("add an export button"). Ask what they are trying to achieve ("finance needs the monthly totals in their own reporting tool"). *Why:* the stated solution is often not the best one, and capturing only the solution loses the information needed to judge alternatives and to know when the need is met.

2. **A requirement must be verifiable.** If no test, inspection, demonstration, or measurement could show it is satisfied, it is a wish. *Why:* unverifiable requirements ("fast", "user-friendly", "secure") cannot guide design or settle disagreement about whether the work is done.

3. **Quality attributes and constraints are requirements too.** Performance, availability, security, privacy, accessibility, compliance, maintainability, and operating cost often drive architecture more than features do. *Why:* they are the requirements most often left implicit, and the most expensive to retrofit.

4. **Requirements come from many stakeholders, and they conflict.** Users, buyers, operators, support, security, legal, finance, and integrators all have needs. Conflicts should be surfaced and resolved deliberately, not discovered in production. *Why:* unresolved conflicts get resolved implicitly by whoever writes the code, usually without the authority or information to do it well.

5. **Explore the edges, not just the happy path.** Errors, exceptions, limits, concurrency, permissions, empty states, migrations, and failure of dependencies are where most defects and disputes originate. *Why:* the main scenario is the one everyone already agrees on.

6. **Detail follows risk.** Specify precisely where misunderstanding is costly or likely (money, safety, compliance, integrations, data); stay lighter where the team can iterate cheaply. *Why:* over-specifying everything wastes effort and goes stale; under-specifying the risky parts causes rework and failures.

7. **Requirements change; manage the change, do not resist it.** Keep requirements traceable to their source and rationale so changes can be evaluated. *Why:* without rationale, nobody knows whether a requirement can safely be altered or removed.

## Kinds of requirements

| Kind | What it states | Example |
|---|---|---|
| Business requirement / goal | Why the organisation is doing this; measurable outcome | Reduce invoice processing time from 5 days to 1 |
| Stakeholder / user requirement | What a stakeholder needs to be able to do | An accounts clerk can approve an invoice from the review screen |
| Functional requirement | A behaviour the system must exhibit | The system shall reject an invoice whose total differs from the sum of its lines by more than 0.01 |
| Non-functional (quality) requirement | How well the system must perform a behaviour or hold a property | 95% of invoice searches return within 1 second with 1 million stored invoices |
| Constraint | A restriction on the solution space | Must run on the existing cloud provider; must integrate with the current accounting system's API |
| Data requirement | What information must be stored, its structure, retention, quality | Invoices retained for the legally required period; supplier tax IDs validated |
| Interface / integration requirement | Exchanges with other systems or people | Exports approved invoices to the accounting system daily in its import format |
| Transition requirement | What is needed to move from the current to the new state | Migrate open invoices; run both systems in parallel for one month-end |
| Assumption / dependency | Things taken as true, or needed from others | The supplier portal will provide structured data by Q3 |

Keep goals, needs, and system requirements linked: each functional requirement should trace to a stakeholder need, and each need to a goal. Orphan requirements (no goal) are candidates for removal; goals with no requirements are gaps.

### Quality attributes checklist

Use as prompts, not as a form. Ask which apply and how much they matter:

- **Performance**: response times, throughput, batch windows — under stated load and data volume.
- **Scalability**: growth in users, data, transactions; peak vs. average.
- **Availability and reliability**: uptime target, maintenance windows, recovery time and data-loss tolerance after failure.
- **Security**: authentication, authorisation model, audit logging, data protection in transit and at rest, threat considerations (see `secure-coding`, `authentication-and-authorization`).
- **Privacy and compliance**: personal data handled, consent, retention and deletion, applicable regulations and industry standards, data residency.
- **Usability and accessibility**: target users' skills, task-completion expectations, accessibility standards to meet.
- **Compatibility**: browsers, devices, operating systems, versions of integrated systems.
- **Maintainability and operability**: monitoring, logging, configurability, deployment frequency, supportability.
- **Localisation**: languages, time zones, currencies, formats.
- **Cost**: operating budget, licensing limits.

Express each as a measurable statement with context: "Under 500 concurrent users, 95th-percentile page load under 2 seconds on a typical mobile connection" rather than "fast".

## Process

### 1. Understand the context and goals

Before collecting requirements, learn: the problem or opportunity, who is sponsoring the work and why now, how success will be measured, what is in and out of scope, the timeline and budget, and what exists today (current systems, processes, workarounds, prior attempts). A short problem statement and a list of measurable goals keep elicitation focused.

### 2. Identify stakeholders

List everyone who is affected by, uses, pays for, operates, supports, regulates, or can block the solution. Commonly missed: operations and support staff, security and legal, data and reporting consumers, integration owners of neighbouring systems, administrators, auditors, people affected but not using the system directly, and future maintainers.

For each, note their interest, influence, and the decisions they own. Identify who has authority to resolve conflicts and approve requirements; if nobody does, raise that early — it is a project risk.

### 3. Elicit

Use several techniques; each finds things the others miss:

| Technique | Good for | Limitation |
|---|---|---|
| Interviews | Goals, pain points, context, priorities | People describe what they think they do, not what they do |
| Observation / contextual inquiry | Actual workflows, workarounds, tacit knowledge | Time-consuming; observer effect |
| Workshops | Resolving conflicts, building shared understanding, prioritising | Dominant voices; needs skilled facilitation |
| Document and system analysis | Existing rules, data, interfaces, regulations | Documents are often outdated; systems encode historical accidents |
| Analysing data and logs | Real volumes, frequencies, edge cases, usage patterns | Shows what happens, not why |
| Prototypes and mock-ups | Eliciting reactions to concrete options; UI requirements | Risk of fixating on the prototype's design details |
| Surveys | Breadth across many users | Shallow; framing biases answers |
| Scenarios and examples | Pinning down behaviour precisely, especially rules | Must be chosen to include edge cases |

Good elicitation questions move from solution to need and from general to specific:

- "What are you trying to accomplish when you do this?"
- "What happens today? What goes wrong? What do you do when it goes wrong?"
- "How would you know this is working? What would you measure?"
- "Walk me through the last time this happened."
- "What is the most common case? The worst case? The strangest case you have seen?"
- "Who else needs this information or is affected when it changes?"
- "What must never happen?"
- "If we could only deliver part of this first, which part?"

Record answers in the stakeholder's words alongside your interpretation, and note the source of every requirement.

### 4. Analyse and model

Raw elicitation notes are inconsistent, overlapping, and incomplete. Analysis structures them:

- **Use cases and scenarios.** For each goal an actor has, describe the main success flow, then alternative flows and exceptions. Writing the exception flows is where most hidden requirements surface.
- **Process models.** For process-heavy work, map the current and future process (steps, roles, handoffs, decisions). Gaps between them become requirements; handoffs are where errors cluster.
- **Data models.** Identify entities, attributes, relationships, ownership, lifecycle (creation, change, archival, deletion), and quality rules. Many functional requirements are really data rules.
- **State models.** For entities with a lifecycle (orders, tickets, applications), list states and allowed transitions, who can trigger each, and what happens on invalid transitions.
- **Business rules.** Extract rules (eligibility, calculations, validations, approvals) into an explicit list, ideally with examples; decision tables work well for rules with several conditions.
- **Context and interface diagrams.** Show the system's boundary, external actors, and data flows; every arrow is an interface requirement.

Choose the models that fit the problem; a reporting project needs data and rule models more than use cases, a workflow tool needs process and state models.

### 5. Hunt for edge cases

Systematically probe each requirement and scenario:

| Category | Questions |
|---|---|
| Boundaries | Zero, one, many, maximum; empty input; exactly at the limit; just over |
| Invalid input | Wrong type, format, encoding, out-of-range values, duplicates, malicious input |
| Time | Time zones, daylight saving, month-end, leap years, deadlines that pass, clock differences, long-running operations |
| Concurrency | Two people editing the same record; repeated submissions; race between approval and cancellation |
| Permissions | Who can see and do what; delegation; what happens when a role changes mid-process |
| Failure of dependencies | Integration down, slow, or returning errors; partial failure; retries and duplicates |
| Lifecycle | Cancel, undo, amend after submission, reopen, archive, delete; what happens to dependent records |
| Volume and scale | Peak periods, bulk operations, very large records |
| Migration and coexistence | Existing data that does not fit new rules; running old and new in parallel |
| Localisation | Names, addresses, currencies, languages, right-to-left scripts |
| Accessibility | Users of assistive technology, keyboard-only use, low vision |
| Abuse | Misuse by legitimate users; fraud; automated attacks |

Not every edge case needs handling by the system, but each needs a decision: handle, prevent, accept and document, or defer. Recording that decision is what prevents later disputes.

### 6. Turn vague asks into testable requirements

A practical rewrite routine:

1. Identify the vague term ("fast", "easy", "secure", "flexible", "real-time", "support", "handle", "appropriate", "etc.").
2. Ask what observable outcome the stakeholder actually cares about and under what conditions.
3. Quantify with a metric, a threshold, and a measurement method, or replace with concrete examples.
4. Check that a tester could design a pass/fail test from the statement alone.

Illustrative rewrites:

| Vague | Testable |
|---|---|
| The report should be fast | The monthly sales report for any single region generates within 10 seconds for data volumes up to 5 years of history |
| The system must be secure | Only users with the Finance Approver role can approve invoices over 10,000; every approval is recorded with user, timestamp, and prior state, and the record cannot be edited |
| Easy to use | A first-time clerk, after the standard 15-minute introduction, can enter and submit a three-line invoice without assistance in under 3 minutes in at least 4 of 5 test sessions |
| Real-time updates | Status changes appear on other users' open screens within 5 seconds |
| Support large files | Accepts uploads up to 200 MB; files over the limit are rejected before upload starts with a message stating the limit |
| Handle errors gracefully | If the accounting system is unavailable, approved invoices are queued and exported automatically when it recovers; finance is notified if the queue is older than 4 hours |

Characteristics of a good individual requirement: necessary (traces to a need), unambiguous (one interpretation), verifiable, feasible, consistent with others, singular (one requirement per statement), implementation-neutral unless it is a genuine constraint, and with a known source and priority. Concrete examples (inputs and expected outputs) are often the clearest specification of all, especially for business rules and calculations; they also become test cases directly.

### 7. Detect and resolve conflicts

Look for conflicts:

- **Between stakeholders** (sales wants flexible discounts; finance wants strict approval).
- **Between quality attributes** (security vs. convenience; consistency vs. availability; flexibility vs. simplicity; performance vs. cost).
- **Between requirements and constraints** (the timeline vs. the scope; the existing platform vs. the required scale).
- **Between requirements and reality** (a requirement contradicts how the work is actually done).

Resolve by returning to goals: which option better serves the measurable goals, at what cost and risk? Make the trade-off explicit, identify who decides, record the decision and rationale, and tell affected stakeholders. Options include: prioritising one side, finding a design that satisfies both (e.g. discount flexibility within limits, with approval above a threshold), phasing, or making behaviour configurable (use sparingly — configurability is itself a cost).

### 8. Prioritise

Prioritise so that scope can flex without losing what matters most. Common approaches: must / should / could / won't (for this release); value versus cost or risk; ranking against goals; or the organisation's existing prioritisation method (see `roadmap-and-prioritization`). Whatever the method:

- "Must" means the release is unacceptable without it — keep this set small, or the category stops meaning anything.
- Prioritise with the people who own the value and the people who know the cost.
- Record what is explicitly out of scope; it prevents scope creep and disappointed expectations.

### 9. Specify and communicate

The form of the specification should fit the team and the risk: a structured requirements document, a set of use cases, user stories with acceptance criteria, a model with annotations, examples and decision tables, or a combination. Follow the organisation's existing format if it has one. Regardless of form, a good specification makes clear:

- the goals and scope (including out of scope),
- stakeholders and the decisions each owns,
- functional requirements and business rules, with examples,
- quality attributes with measurable targets,
- constraints, assumptions, and dependencies,
- edge-case and error-handling decisions,
- priorities,
- open questions with owners and due dates,
- glossary of domain terms (ambiguous vocabulary is a frequent source of misunderstanding — "customer", "active", "order date" often mean different things to different teams).

### 10. Validate

Check that the requirements are right, not just well written:

- **Review with stakeholders**: walk through scenarios and examples rather than asking people to read and approve a long document — reviewers approve documents they have not understood.
- **Prototype or simulate** high-risk requirements to get reactions to something concrete.
- **Derive test cases**: if testers cannot derive tests, the requirement is not verifiable yet (see `qa-test-planning`).
- **Check against goals**: does meeting all must-have requirements achieve the goals?
- **Feasibility check** with the people who will build and operate it.

### 11. Trace and manage change

Maintain links from goals → needs → requirements → design elements → tests (and back). The depth of traceability should match the context: regulated and safety-critical work may require formal traceability; a small team may only need each story linked to a goal and to its acceptance tests.

Traceability answers: why does this requirement exist? What is affected if it changes? Is every requirement tested? Is every test justified?

When changes arrive, evaluate impact (on other requirements, design, schedule, cost, and tests), decide with the right authority, update the specification and links, and communicate. Version the requirements so it is always clear which version a design or test refers to.

## Requirements for procurement and vendor selection

When requirements will be used to choose a product or supplier:

- Distinguish mandatory requirements (pass/fail) from weighted ones (scored).
- Phrase requirements so vendors cannot answer "yes" to everything: ask how a requirement is met, ask for demonstrations of key scenarios, and request evidence (certifications, references, documentation).
- Include non-functional, contractual, and exit requirements: support levels, data ownership and export, security assessments, pricing at projected scale.
- Score responses consistently with a pre-agreed method and weights, ideally by more than one evaluator.

## Discovering context

- **Existing documentation**: prior specifications, process documents, policies, regulations, system documentation, support tickets, and change logs. Requirements often already exist implicitly in the current system's behaviour — including behaviours users depend on that nobody documented.
- **Organisation's methods and templates**: how they write and approve requirements, the tools they use (issue trackers, requirements tools, wikis), and their terminology.
- **Regulatory and contractual obligations** that impose requirements regardless of stakeholder preferences.
- **The team's delivery approach**: iterative teams need a prioritised backlog with just-in-time detail; contract-based or regulated work needs more upfront specification and formal sign-off.
- **If working in a codebase**, read the existing behaviour (see `explore-codebase`) before writing requirements for changes, so you specify the delta and do not accidentally remove behaviour.

## Working with and without tools

**With access to systems, documents, or data:** analyse them directly — real data reveals volumes, formats, and edge cases that stakeholders forget. Handle personal data in samples carefully and only as needed.

**In conversation only:** act as the analyst: ask focused questions in small batches, reflect back your understanding with examples, propose testable rewrites for the user to confirm, and keep a running list of requirements, decisions, and open questions. Make assumptions explicit rather than silently filling gaps.

**When asked to produce requirements without access to stakeholders:** produce a draft clearly marked as such, with assumptions and open questions listed prominently, and identify which stakeholders should validate which parts.

## Pitfalls

- **Solution masquerading as requirement.** "Use a dropdown" instead of "select one of the approved cost centres".
- **Ambiguous words**: "fast", "user-friendly", "flexible", "support", "etc.", "and/or", "as appropriate".
- **Missing non-functional requirements**, discovered after launch.
- **Happy-path-only specification**: no error, exception, or edge-case decisions.
- **Missing stakeholders**: operations, support, security, legal, data consumers, integration owners.
- **Asking people what they want instead of observing what they do.**
- **Gold-plating**: requirements no goal needs, often added "while we are at it".
- **Everything is a must.** Prioritisation that does not discriminate.
- **Undefined terms** leading to different interpretations across teams.
- **Silent conflict resolution**: developers choosing between conflicting requirements without telling anyone.
- **Specification without validation**: documents approved but not understood.
- **Stale requirements**: the specification diverges from what is being built, and nobody trusts it.
- **Over-specification** of low-risk areas, freezing design decisions prematurely.
- **Ignoring transition**: no plan for data migration, training, or coexistence.

## Quality bar and verification

Before delivering requirements, check:

- [ ] Goals are stated and measurable; every requirement traces to a goal or need, and every goal has requirements.
- [ ] All relevant stakeholder groups were considered, including operational and compliance roles.
- [ ] Needs are separated from proposed solutions; constraints are genuine constraints.
- [ ] Functional requirements cover main, alternative, and exception flows.
- [ ] Quality attributes are present and measurable with conditions.
- [ ] Edge cases were systematically probed and each has a recorded decision.
- [ ] Each requirement is unambiguous, verifiable, singular, and has a source and priority.
- [ ] Business rules and calculations have worked examples.
- [ ] Conflicts are identified, resolved by the right person, and the rationale recorded.
- [ ] Out-of-scope items, assumptions, dependencies, and open questions are listed with owners.
- [ ] Domain terms are defined.
- [ ] Stakeholders validated the requirements through scenarios or prototypes, and testers can derive tests.

A strong test: hand a requirement to a developer and a tester separately and ask each what they would build and test. If their answers differ, the requirement is not done.

## Related skills

- `clarify-requirements` — the quick, in-task version of this discipline.
- `product-requirements` and `user-stories` — packaging requirements for product teams and backlogs.
- `ux-research` — deeper discovery of user needs and behaviour.
- `qa-test-planning` — deriving tests from requirements.
- `system-design` and `software-architecture` — designing to meet the requirements, especially quality attributes.
- `roadmap-and-prioritization` — prioritising across releases.
