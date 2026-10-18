---
name: product-requirements
description: >-
  Write, review, and maintain product requirements documents (PRDs), feature
  specs, one-pagers, and briefs: frame the problem before the solution, name
  the users and their jobs, set goals, non-goals and success metrics, define
  scope, write requirements at the right altitude, record alternatives and open
  questions, and keep the spec alive as the work changes. Use when someone asks
  to "write a PRD", "draft a spec", "spec out this feature", "turn this idea
  into requirements", "review my product doc", or needs a shared definition of
  what to build and why before design or engineering starts. Not for
  backlog-level stories (user-stories), eliciting needs from stakeholders
  (requirements-analysis), or engineering design docs (system-design).
metadata:
  category: product-and-communication
  related: user-stories, requirements-analysis, clarify-requirements, roadmap-and-prioritization, ux-research, experiment-design, technical-writing, technical-decision-making
---

# Product Requirements

A product requirements document exists to create **shared understanding of a problem worth solving and the shape of an acceptable solution**, so that design, engineering, and other teams can make good decisions without asking the author about every detail. It is a decision-making tool, not a contract and not a record of everything anyone said.

This skill covers the content and reasoning of PRDs, specs, one-pagers, briefs, and similar artifacts, whatever the organization calls them.

**Not covered here:**

- Breaking a spec into backlog items with acceptance criteria — see `user-stories`.
- Discovering what stakeholders actually need through interviews and analysis — see `requirements-analysis` and `ux-research`.
- Deciding what to build next across many candidates — see `roadmap-and-prioritization`.
- How the system will be built (architecture, data model, APIs) — see `system-design`, `software-architecture`, `api-design`.
- Prose quality and editing — see `technical-writing` and `writing-review-and-editing`.

## Core principles

### 1. Problem before solution

State the problem, who has it, and the evidence it matters before describing anything to build. Why: a solution-first spec cannot be evaluated. Reviewers can only argue about the solution's details, never about whether it addresses something real. When the problem is explicit, a cheaper or better solution can be proposed by anyone, and the team can tell when they have solved it.

A useful test: if you delete every sentence describing the solution, does the document still convince a skeptical reader that something should be done? If not, the problem section is too thin.

### 2. Altitude: say *what* and *why*, leave *how* to the people who own it

Requirements should constrain outcomes and behaviour, not implementation, unless an implementation constraint is genuinely required (regulatory, contractual, platform). Why: over-specifying removes the judgment of designers and engineers who know more about their domain than the spec author, and it freezes decisions before the information to make them exists. Under-specifying, on the other hand, pushes product decisions into code review, where they get made by accident.

The right altitude is the level at which a requirement could be verified by someone who did not write it.

### 3. Non-goals are as important as goals

Explicitly list what this work will *not* do, especially the things a reasonable reader might assume it will. Why: scope ambiguity is the most common source of late conflict. A non-goal converts a future argument into a present, cheap one.

### 4. Measure the outcome, not the activity

Success metrics should describe a change in user or business behaviour ("share of new teams that invite a second member within 7 days"), not shipping ("feature launched"). Why: shipping is the cost, not the benefit. A spec without an outcome measure cannot tell you whether to iterate, keep, or remove the thing you built.

### 5. Make uncertainty visible

Separate what is known (with evidence), what is assumed, and what is unknown. Why: a spec that reads as uniformly confident hides its riskiest bets. Reviewers can only challenge assumptions they can see, and the team can only de-risk what has been named.

### 6. The spec is a living document until the work ships

A spec that diverges from what is being built is worse than no spec, because people trust it. Decisions made during design and build go back into the document, with a dated note. Why: the spec is the reference for QA, support, documentation, sales, and the next team to touch the feature.

### 7. Fit the organization's format, not an ideal one

Most organizations have an existing PRD shape, a review ritual, and unwritten expectations. Use them. Why: a document in an unfamiliar format gets less engagement and more procedural objections, which costs more than any structural improvement buys. Improve the format gradually and by agreement, not by surprise.

## What a good spec contains

There is no mandatory section list. The elements below are the content a reader needs; arrange, merge, rename, or drop them to suit the size of the work and local conventions. A two-week change may need half a page covering four of these. A multi-quarter initiative may need all of them plus appendices.

| Element | What it answers | Why it matters | Signs it is weak |
|---|---|---|---|
| Context / background | Why are we talking about this now? | Gives cold readers enough to engage | Assumes the reader was in the meeting |
| Problem statement | What is wrong or missing, for whom, with what consequence? | Anchors every later decision | Describes a missing feature ("users can't export to CSV") rather than a need ("finance teams re-key data into their ledger each month") |
| Evidence | How do we know the problem is real and sizable? | Separates opinion from signal | Only anecdotes, or only one loud customer |
| Users and their jobs | Who specifically, in what situation, trying to accomplish what? | Lets designers and engineers make trade-offs | "Users" with no segment; personas with no situation |
| Goals | What outcomes will be true if this succeeds? | Defines success | Goals that are restated features |
| Non-goals | What is deliberately excluded? | Prevents scope creep and false expectations | Absent, or trivially obvious exclusions |
| Success metrics | How will we measure the goals, against what baseline, by when? | Makes success checkable | No baseline; vanity metrics; no guardrails |
| Proposed solution / scope | What will we build, at what fidelity? | Shared picture of the thing | Pixel-level detail in a requirements doc, or so vague anything qualifies |
| Requirements | What must be true of the solution? | Verifiable contract for design, build, test | Implementation instructions, or untestable adjectives ("fast", "intuitive") |
| User experience notes | Key flows, states, and edge cases | Avoids design surprises | Only the happy path |
| Alternatives considered | What else could solve this, and why not? | Shows the decision was made, not defaulted | "None" |
| Risks and assumptions | What could make this fail or not matter? | Targets de-risking | Generic risks ("timeline might slip") |
| Dependencies | What other teams, systems, or decisions does this need? | Surfaces coordination early | Discovered during build |
| Open questions | What is undecided, who decides, by when? | Keeps decisions moving | Questions without owners |
| Rollout and launch | Phasing, flags, migration, communication, support readiness | Shipping safely | "Launch to everyone" for a risky change |
| Change log | What changed in the spec since review, and why | Keeps trust in the document | Silent edits |

### Problem statement: how to make it strong

A strong problem statement names:

- **Who** — a specific segment, ideally with size ("admins at teams of 50+ seats, roughly 18% of accounts").
- **The situation** — when and where the problem occurs.
- **The struggle** — what they do today and why it is painful (time, money, risk, frustration, abandonment).
- **The consequence** — for the user and for the business.
- **The evidence** — data, research, support volume, sales loss reasons, observed behaviour.

Illustrative example (weak vs. strong):

> Weak: "We need bulk editing for tasks."
>
> Stronger: "Project leads managing more than 100 open tasks re-prioritise weekly. Today they edit tasks one at a time; in session recordings this takes 20–40 minutes and 30% of sessions end before completion. Support receives ~60 tickets a month asking for bulk changes, and 'too much admin work' appears in 11% of churn surveys for teams over 20 seats."

The strong version invites alternatives (smarter defaults, auto-prioritisation, keyboard shortcuts) — that is a feature, not a bug.

### Users and jobs

Describe the user in terms of the job they are trying to get done and the context they are in, not demographics. A "job" framing — "when [situation], I want to [motivation], so I can [outcome]" — is one useful lens, not a required format. What matters:

- Distinguish **primary** users (the problem is theirs) from **secondary** users (affected by the solution: admins, support agents, recipients of output).
- Name the **buyer** if different from the user; their goals may conflict.
- Note **who is explicitly not served** by this work.

### Goals, non-goals, and metrics

Good goals are outcomes, few in number (one to three), and ranked when they could conflict. If the team would trade goal B for goal A under pressure, say so now.

Good non-goals are things a reasonable person might expect to be included:

> Illustrative: "Non-goal: bulk editing of custom fields in this phase. Custom fields have per-workspace validation rules; supporting them would roughly double the scope. We will revisit once usage data shows whether standard fields cover most bulk edits."

Metrics come in three kinds; good specs usually have at least one of the first and one of the third:

| Kind | Purpose | Illustrative |
|---|---|---|
| Primary / success metric | Did we achieve the goal? | Median time to re-prioritise 100 tasks |
| Secondary / diagnostic | Why did the primary move (or not)? | Adoption of bulk-select; bulk actions per active lead |
| Guardrail / counter-metric | Did we break something else? | Accidental bulk-change undo rate; support tickets about lost edits; page load time |

For each metric, state the **baseline**, the **target or minimum meaningful change**, the **time window**, and **how it will be measured** (existing event, new instrumentation, survey). If the metric needs new instrumentation, that instrumentation is a requirement. If the change will be judged by an experiment, see `experiment-design` for sample size and duration.

Beware targets pulled from the air. If you cannot justify a target, say "directional: we expect an increase and will decide on continuation at a review on <date>" rather than inventing precision.

### Requirements at the right altitude

A requirement should be:

- **Verifiable** — someone other than the author could check it is met.
- **Necessary** — removing it would make the solution fail a goal or a constraint.
- **Solution-tolerant** — it does not dictate implementation unless that is a real constraint.
- **Prioritised** — at least must / should / could, or a phase marker.

Altitude ladder (illustrative):

| Too high | Right altitude | Too low |
|---|---|---|
| "Bulk editing should be easy." | "A lead can change priority, assignee, or due date on up to 500 selected tasks in one action, and undo it within the session." | "Add a checkbox column at 24px width; on shift-click call `selectRange()`." |
| "It must be fast." | "Applying a bulk change to 500 tasks completes, or shows progress, within 2 seconds for the 95th percentile workspace." | "Use a batched PATCH endpoint with 50-item pages." |
| "Secure." | "Only users with edit permission on every selected task can apply a bulk change; tasks they cannot edit are excluded and reported." | "Check `can_edit` in the controller loop." |

Distinguish **functional** requirements (behaviour) from **non-functional** ones (performance, reliability, accessibility, privacy, security, localisation, compliance). Non-functional requirements are the ones most often forgotten and most expensive to retrofit. Ask explicitly: what about accessibility, permissions, data retention, audit logs, internationalisation, offline or degraded states, existing integrations and APIs, migration of existing data, and support tooling?

### Edge cases and states

For each key flow, think through: empty state, first use, error, partial failure, very large input, concurrent edits, permission boundaries, undo/recovery, and what happens to existing data. You do not need to design each one, but the spec should say which ones matter and any non-obvious required behaviour.

### Alternatives considered

List the realistic options, including "do nothing" and "solve it without software" (process change, docs, a setting). For each, a sentence on why it was not chosen. Why: this is the strongest evidence that the proposal is a decision rather than a default, and it prevents reviewers relitigating options already weighed. If an alternative was rejected for cost, say what would make it attractive again.

### Open questions

Each open question should have an **owner** and a **date or trigger** by which it must be answered, plus a note on what it blocks. Questions that block design should be resolved before design starts; questions that only affect rollout can stay open longer. Remove or mark answered questions as they close, recording the answer.

## Process

### 1. Find out what kind of document is needed

Ask, or infer from context:

- **Purpose**: getting approval to invest? aligning a team that already agreed? handing off to an external partner? documenting for compliance? Each changes depth and tone.
- **Size of the work**: days, weeks, quarters.
- **Audience**: executives deciding funding, a squad building it, other teams depending on it, customers.
- **Existing format**: is there a template, a recent good example, a review process? Look for it before writing. If you have access to the organization's docs, find two or three recent specs that were considered good and match their shape and depth.

Rough sizing guide:

| Work size | Typical artifact | Usually includes |
|---|---|---|
| Small change (days) | A ticket description or short brief | Problem, desired behaviour, acceptance criteria, metric if any |
| Feature (weeks) | One-pager or short PRD | Problem, users, goals/non-goals, metric, scope, key requirements, open questions |
| Initiative (months+) | Full PRD, often paired with a design doc | All elements, phased scope, rollout, dependencies, risks |
| Exploratory bet | Opportunity brief or hypothesis doc | Problem, evidence, hypotheses, what we will learn and how, kill criteria |

### 2. Gather the inputs before writing

Collect: the request and who made it, any research, data, support or sales signals, prior attempts, related specs, technical constraints, and the strategic goal this ladders up to. If you lack evidence for the problem, say so in the document rather than manufacturing it. Where a stakeholder conversation is needed to resolve real ambiguity, ask — see `clarify-requirements` for which questions are worth asking.

Never invent data, quotes, or research findings to make the case look stronger. If you are drafting for someone, mark placeholders clearly ("[baseline needed — from analytics]") so they cannot be mistaken for facts.

### 3. Draft the problem and goals first, and get them reviewed

Write context, problem, users, goals, non-goals, and metrics. Share this partial draft with the key decision-maker before writing the solution. Why: if the problem framing is wrong, all solution work is wasted. This early review is the highest-leverage moment in the whole process and the one most often skipped.

### 4. Develop the solution with the people who will build it

Sketch the proposed scope, then involve design and engineering before writing detailed requirements. They will find cheaper options, hidden complexity, and constraints you do not know. A spec written alone and "handed over" tends to be both over-specified in the wrong places and silent on the hard parts.

### 5. Write requirements and edge cases

Convert the agreed solution into verifiable requirements at the right altitude. Prioritise them. Mark which are needed for the first release versus later phases. Flag requirements that carry most of the risk or cost.

### 6. Review deliberately

Send to reviewers with a specific ask: "Please check whether the non-goals are acceptable to Sales" is more useful than "Thoughts?". Give a deadline. Collect comments in one place. Resolve disagreements explicitly and record the decision and its owner in the document.

### 7. Keep it alive

During design and build, update the spec when decisions change it. Use a change log or dated notes for meaningful changes, and notify people who depend on it. After launch, add the actual results against the success metrics, or link to where they live, and mark the document's status (shipped, superseded, abandoned).

## Decision guidance

### How much solution detail belongs in the PRD?

| Choose more detail when… | Choose less detail when… |
|---|---|
| The work is handed to an external team or vendor | The building team helped shape the solution |
| Regulatory, legal, or contractual constraints apply | The domain is new and learning is the goal |
| Multiple teams must implement consistent behaviour | Designers will explore the solution space |
| The behaviour is subtle and has been gotten wrong before | Detail would be speculative and likely to change |

### PRD, design doc, or both?

- A **PRD** answers what and why from the user's and business's point of view.
- A **design doc** (technical spec, RFC) answers how, with architecture and trade-offs.

For non-trivial work, keep them separate but linked, owned by the people best placed to write each. Mixing them tends to produce a document nobody fully owns and that is too technical for one audience and too vague for the other. For small work, one combined document is fine.

### Fixed scope or fixed time?

If the date is fixed (a conference, a contract, a regulation), write the spec with an explicit **must-have core** and a **cut list** in priority order, so the team knows what to drop. If scope is fixed, say so and give an honest range for timing (see `estimate-effort`). Pretending both are fixed is the root of most late projects.

### When the request is really a solution

Requests often arrive as solutions ("add a dark mode", "we need an API"). Do not refuse them, and do not write them up uncritically. Ask what problem the requester expects it to solve, for whom, and how they will know it worked. Often the requested solution is right; occasionally a smaller or different solution is better. Either way, the spec now has a problem statement.

## Discovering and honouring context

Before drafting:

- **Find existing templates and recent exemplars.** Match section names, depth, and tone. If the organization's template lacks something important (e.g. non-goals or guardrail metrics), add it within the template rather than replacing the template.
- **Learn the vocabulary.** Use the organization's names for customer segments, plans, product areas, and metrics. Introducing new names for existing concepts creates confusion.
- **Identify the decision process.** Who approves? Is there a review meeting? Is the document read silently at the start of the meeting, or before? Pre-read documents can be longer; documents presented live need a strong summary.
- **Know the strategy.** Connect the problem to stated company or team goals, using their wording, so reviewers can see why this matters now.
- **Check the record.** Has this been tried before? Is there a prior spec, an abandoned experiment, a customer commitment? Ignoring history loses credibility quickly.
- **Respect the writer's voice.** If drafting for someone, write in a register they would plausibly use, and leave decisions that are theirs to make as marked options rather than choosing silently.

## Pitfalls and anti-patterns

- **The feature list in disguise.** A document that is a list of capabilities with a one-line "why". Recognize it by the absence of a problem statement with evidence. Fix by writing the problem first and seeing which features survive.
- **Solution lock-in.** The first idea is described in detail and alternatives are absent. Fix by forcing at least two real alternatives, including a smaller one.
- **Vanity or unmeasurable metrics.** Page views, "engagement", "satisfaction" without a measurement method or baseline. Fix by naming the behaviour, the event, the baseline, and the window.
- **Missing guardrails.** Optimising one metric while degrading another (conversion up, refunds up). Fix by pairing each success metric with what must not get worse.
- **Wish-list scope.** Every stakeholder's request is a must-have. Fix with honest prioritisation and a written cut list.
- **Adjective requirements.** "Simple", "fast", "robust", "intuitive". Fix by making each one testable or deleting it.
- **Implementation by the back door.** Requirements dictate database fields, endpoints, or component choices without a reason. Fix by stating the underlying need and letting the owners choose.
- **Happy-path only.** No errors, empty states, permissions, migration, or undo. These are found in QA or by customers instead. Fix with a deliberate edge-case pass.
- **Orphan open questions.** Lists of questions without owners or dates, still open at launch. Fix by assigning each one and reviewing them weekly.
- **The frozen spec.** Decisions change in chat and the document does not. Fix by making "update the spec" part of the definition of done for any decision.
- **The encyclopaedia.** Thirty pages nobody reads, where the important decisions are buried. Fix with a short summary up front, appendices for detail, and ruthless deletion of history that no longer matters.
- **Fabricated certainty.** Invented numbers, inflated market sizes, or quotes paraphrased beyond what was said. This destroys trust when discovered. Mark estimates as estimates and cite sources.
- **Writing for approval rather than for building.** A persuasive document that leaves the builders without answers. Both audiences need to be served; if that is impossible in one document, split it.

## Quality bar and verification

Before calling a spec ready for review, check:

- [ ] Someone unfamiliar with the project can state the problem, the user, and the goal in their own words after reading the first page.
- [ ] The problem section stands alone without the solution and cites evidence (or clearly flags that evidence is missing).
- [ ] There are explicit non-goals that a reasonable reader might otherwise have assumed were in scope.
- [ ] Each success metric has a baseline (or a plan to establish one), a target or decision threshold, a time window, and a measurement method; at least one guardrail is named.
- [ ] Each requirement is verifiable by someone other than the author, and prioritised.
- [ ] Non-functional requirements (accessibility, performance, security, privacy, localisation, migration) were considered and either addressed or explicitly excluded.
- [ ] At least one real alternative, including "do nothing" or a smaller option, is recorded with a reason.
- [ ] Every open question has an owner and a date or trigger.
- [ ] Dependencies on other teams are named and those teams have been told.
- [ ] Nothing in the document is presented as fact without a source; placeholders are unmistakable.
- [ ] The format, vocabulary, and depth match the organization's existing practice.

Useful review exercises:

- **The five-minute read**: ask a reviewer to read only the first page and summarise it back. Gaps in their summary are gaps in the document.
- **The engineer test**: could an engineer start estimating from this? List the questions they would have to ask. Answer the important ones or add them as open questions.
- **The QA test**: could a tester derive test cases from the requirements? Untestable requirements will be argued about at the end.
- **The cut test**: if the team had half the time, does the document already say what to cut?
- **The "so what" test**: for each goal, ask "so what?" until you reach something a customer or the business actually values. Stop there.

After launch, compare actual results to the success metrics and record what was learned. Specs whose outcomes are never checked teach the organization nothing.

## Working as an assistant on someone else's spec

- When asked to draft, produce a draft clearly marked as such, with assumptions listed and placeholders for facts you do not have.
- When asked to review, lead with the two or three issues that most affect whether the right thing gets built (usually problem clarity, scope, and metrics), then smaller points. Distinguish blocking issues from suggestions. See `writing-review-and-editing` for review technique.
- Do not resolve product decisions silently. Where the spec needs a choice, present the options and their trade-offs and let the owner decide.
- Do not circulate, publish, or send the spec to others on the author's behalf without explicit confirmation.

## Related skills

- `requirements-analysis` — eliciting and analysing needs before or alongside the spec.
- `user-stories` — decomposing the spec into deliverable backlog items.
- `roadmap-and-prioritization` — deciding whether this spec's work should happen now.
- `experiment-design` — when success will be judged by a controlled experiment.
- `ux-research` — gathering evidence for the problem section.
- `technical-decision-making` — recording consequential choices and their rationale.
- `technical-writing` — clarity and structure of the prose.
