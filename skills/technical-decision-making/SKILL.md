---
name: technical-decision-making
description: >-
  Make and document sound technical choices: frame the actual decision and
  its constraints, generate genuinely different options, analyse trade-offs
  against criteria that matter here, weigh reversibility and cost of delay,
  make a clear recommendation rather than a survey, and record the decision
  and its reasoning (e.g. as an architecture decision record) so it can be
  revisited. Use when choosing between libraries, frameworks, databases,
  architectures, build-vs-buy, vendors, or approaches; when someone asks
  "should we use X or Y?", "what's the best way to…?", or "which option do
  you recommend?"; and when a decision needs to be written up for others.
  Not for detailed architecture work itself (see software-architecture,
  system-design) or reviewing an existing design (see architecture-review).
metadata:
  category: meta
  related: software-architecture, system-design, architecture-review, estimate-effort, clarify-requirements, plan-and-decompose, dependency-management, technical-writing
---

# Technical Decision-Making

Technical decisions are bets made with incomplete information. Good decision-making does not guarantee good outcomes, but it makes the reasoning explicit, matches the effort to the stakes, chooses options that keep the future open where that matters, and leaves a record so the next person knows why things are the way they are. The most common failure is not picking the wrong option — it is answering a question nobody asked, comparing options on criteria that do not matter here, or presenting a survey and leaving the decision to the reader.

## Scope

Covers choosing among technical options at any scale — a library, a data model, a service boundary, a vendor, a migration strategy, build vs. buy — and writing down the decision.

Does not cover:

- Producing the architecture itself — see `software-architecture`, `system-design`, `api-design`, `database-design`.
- Evaluating an existing design — see `architecture-review`.
- Product or business prioritization — see `roadmap-and-prioritization`.
- Managing dependencies after choosing them — see `dependency-management`.

## Core principles

### 1. Frame the decision before comparing options

Most bad decisions come from a badly framed question. "Which database should we use?" might really be "How do we handle 10× write growth next year?" or "How do we stop losing data during deploys?" — each leads to different options, some of which are not databases at all. State the problem, the goal, and the constraints first; options come second.

### 2. Criteria come from context, not from the options

Do not let the options' feature lists define what matters. Decide what matters in this situation — the team's skills, the scale actually expected, operational capacity, deadlines, compliance, existing systems — and weight those. A technology that is "better" in general can be worse for a team that cannot operate it.

### 3. Match effort to reversibility and stakes

Reversible, low-impact decisions ("two-way doors") should be made quickly by whoever is closest to the work; a wrong choice is cheap to undo, and deliberation costs more than error. Irreversible or high-impact decisions ("one-way doors") — data models, public APIs, core platforms, vendor lock-in, anything others will build on — deserve careful analysis, prototyping, and wider input. Misclassifying a two-way door as one-way creates paralysis; the reverse creates expensive regret.

### 4. Prefer options that preserve future choices — when the future is uncertain

When requirements are likely to change, favour options that are easy to change: clear interfaces, standard formats, fewer bespoke dependencies, incremental adoption. Optionality has a cost (abstraction, indirection), so pay for it only where change is genuinely likely, not everywhere "just in case".

### 5. Recommend, don't survey

A list of options with pros and cons hands the hardest part — weighing them — back to the reader. Do the weighing. Give a clear recommendation, the main reason, the conditions under which you would choose differently, and what you would watch for. The reader can still disagree, but now they are disagreeing with a position.

### 6. Write down the why

Code shows what was decided; it rarely shows why or what was rejected. Without a record, decisions get relitigated, or worse, reversed by someone who does not know the constraint that drove them. A short record of context, decision, alternatives, and consequences is cheap insurance.

## Process

### Step 1: Classify the decision

Quickly judge:

- **Reversibility** — what would it cost to change course in six months? Hours, weeks, or a rewrite?
- **Blast radius** — who and what does it affect? One module, a team, the company, customers?
- **Urgency** — what is the cost of deciding later? Does waiting buy useful information?

| Profile | Approach |
|---|---|
| Reversible, local | Decide now, by the person doing the work; note it briefly if non-obvious |
| Reversible, broad | Decide quickly with a short write-up; set a review point |
| Hard to reverse, local | Analyse options; a quick prototype if the key question is empirical |
| Hard to reverse, broad | Full process: framing, options, criteria, prototypes or proofs of concept, input from affected people, written record |

If waiting yields significant information at low cost (a vendor's release next month, results of a load test), deciding later can be the right decision — but set a date, because "later" without a date becomes default-by-drift.

### Step 2: Frame the problem

Write a few sentences covering:

- **The problem or goal** — in terms of outcomes, not technologies.
- **Constraints** — hard limits: budget, deadline, compliance, existing commitments, platforms, team size and skills.
- **Forces** — the tensions that make this a decision: speed vs. safety, flexibility vs. simplicity, cost now vs. cost later.
- **Out of scope** — related decisions you are deliberately not making now.

Check the framing with the user or stakeholders if the decision is large; a correction here saves the whole analysis.

### Step 3: Generate real options

Aim for two to four genuinely different options. Include:

- **The status quo / do nothing** — always a real option, and the baseline that others must beat.
- **The incremental option** — the smallest change that addresses the problem.
- **The conventional option** — what most teams in this situation would do.
- **A substantially different approach** — e.g. buy instead of build, remove the need instead of meeting it, solve at a different layer.

Avoid straw men: options included only to make the favourite look good waste the reader's time and erode trust in the analysis.

### Step 4: Choose and weight criteria

Pick the criteria that actually discriminate between options in this context. Common candidates:

- Fit to requirements (functional and non-functional: scale, latency, consistency, availability).
- Team familiarity and hiring market; learning cost.
- Operational burden: who runs it, monitors it, upgrades it, is paged for it.
- Total cost: licences, infrastructure, engineering time to build and maintain.
- Time to first value.
- Maturity, community, vendor health, licence terms.
- Security and compliance posture.
- Reversibility / lock-in; migration path out.
- Consistency with existing architecture and conventions.

Mark which criteria are **must-haves** (options failing them are eliminated) and which are **trade-offs** (weighed against each other). Two to five weighted criteria are usually enough; twenty criteria with spreadsheet weights tend to produce false precision and hide the real deciding factor.

### Step 5: Evaluate

For each option, against each criterion, assess with evidence:

- **Prefer evidence over reputation.** Benchmarks on your workload, a short prototype, the actual documentation of the limits, reports from teams at similar scale. Marketing pages and generic "X vs Y" articles are weak evidence.
- **Run a proof of concept for the critical unknown**, not for everything. If the decision hinges on whether option A can handle your query pattern, test that one thing.
- **Consider the second-order effects** — what does this choice force or make harder later? (A new datastore means new backups, monitoring, on-call knowledge, security review.)
- **Estimate costs in ranges** (`estimate-effort`), including ongoing maintenance, not just initial build.

A comparison table is useful when options and criteria are several; keep cells short and specific ("p99 12 ms on our benchmark" rather than "fast").

### Step 6: Decide and recommend

- State the recommendation in one sentence.
- Give the deciding reason — usually one or two criteria tipped it. Be honest about which.
- State the main trade-off accepted: what you are giving up.
- State the conditions under which another option would be better ("If we expect more than ~10k writes/sec within a year, B wins").
- Identify risks and how they will be mitigated or monitored.

When options are genuinely close, say so — and recommend the one that is more reversible, simpler, or more familiar, since the cost of being wrong is lower. A close call is a reason to decide quickly, not to deliberate longer.

If the decision is not yours to make, present the recommendation and ask for the decision explicitly. If it is yours (the user has delegated it, or it is a two-way door within your task), make it and state it.

### Step 7: Record the decision

Write a decision record proportionate to the decision's weight. A good record — sometimes called an architecture decision record (ADR), though format and name vary by organization — contains:

- **Context** — the problem, constraints, and forces at the time.
- **Decision** — what was chosen, stated plainly.
- **Alternatives considered** — briefly, and why each was not chosen.
- **Consequences** — what becomes easier, what becomes harder, new obligations (operations, migrations), risks accepted.
- **Status and date** — proposed, accepted, superseded (and by what).
- **Revisit triggers** — conditions that should prompt reconsideration.

Keep records short — often under a page. Store them where the people affected will find them: the project's existing decision log, docs folder, wiki, or the issue tracker. Follow the project's existing format if one exists. Records are immutable history: when a decision changes, write a new record that supersedes the old one rather than editing the old reasoning away.

Illustrative example of the substance (not a template) for a small decision:

> Context: background jobs currently run in-process and are lost on deploy. We need at-least-once execution for ~2k jobs/day; the team already operates Postgres and has no queue experience.
> Decision: use a Postgres-backed job queue library rather than introducing a dedicated message broker.
> Alternatives: a dedicated broker (more throughput and features, but new infrastructure to operate and secure); a managed cloud queue (low ops, but adds a vendor dependency and local-dev complexity).
> Consequences: no new infrastructure; throughput ceiling far above current need; jobs share the database's load and backups. Revisit if volume exceeds ~100k/day or we need fan-out to multiple consumers.

### Step 8: Follow through

- Communicate the decision to those affected, with a link to the record.
- Implement in a way that respects the reversibility you claimed (e.g. keep the abstraction boundary you said would make migration possible).
- At the revisit trigger, or if evidence contradicts the assumptions, reopen the decision deliberately rather than drifting.

## Decision heuristics

- **Boring technology for core concerns.** Prefer well-understood tools for critical paths; spend novelty on the problems that differentiate the product. Every new technology carries a fixed cost in learning, operations, and failure modes.
- **Build vs. buy.** Buy (or use open source) for commodity capabilities that are not your differentiator — auth, payments, email delivery, monitoring — unless constraints forbid it. Build when the capability is core to your value, when off-the-shelf options fit poorly enough that adaptation costs more than building, or when control and data residency demand it. Count the full lifetime cost of building, including maintenance.
- **Consistency vs. local optimum.** A slightly worse choice that matches the rest of the system often beats a slightly better one that introduces a second way of doing things. Each additional pattern raises the cost of understanding the whole.
- **Scale for the next order of magnitude, not three.** Design for realistic growth over the decision's lifespan; do not pay today for scale you may never reach, but avoid choices with a hard ceiling just above current load.
- **Simplicity as a tie-breaker.** Between options that meet the requirements, choose the one with fewer moving parts.
- **Disagree and commit.** Once a decision is made through a fair process, implement it fully. Re-open only with new information, not with the same arguments.

## Worked reasoning: a comparison that leads to a recommendation

Illustration only. A small team must add full-text search to a product catalogue of about 200k items. They run a relational database already; nobody has operated a search engine.

**Framing.** Goal: users find products by partial name, description, and synonyms, with results in under ~300 ms. Constraints: two engineers, no dedicated operations staff, launch in six weeks. Out of scope: personalized ranking.

**Options.** (A) The relational database's built-in full-text search. (B) A self-hosted dedicated search engine. (C) A managed search service. (D) Status quo: `LIKE` queries — already known to be too slow and poor at relevance, kept as the baseline.

| Criterion | A: built-in FTS | B: self-hosted engine | C: managed service |
|---|---|---|---|
| Relevance and typo tolerance | Adequate; weak typo handling | Strong | Strong |
| Latency at 200k items | Fine in a quick benchmark | Fine | Fine |
| Operational burden | None new | New cluster to run, upgrade, monitor | Low; vendor runs it |
| Data sync complexity | None (same database) | Indexing pipeline needed | Indexing pipeline needed |
| Cost | Existing | Infrastructure + engineering time | Subscription, grows with usage |
| Reversibility | High — can move to B/C later | Medium | Medium; some vendor-specific query features |

**Recommendation.** Start with A. The deciding factors are operational burden and the six-week deadline: A adds no new infrastructure and no sync pipeline, and its relevance is adequate for launch. Trade-off accepted: weaker typo tolerance. Choose C instead if user testing shows typo tolerance matters a lot, or the catalogue grows past a few million items — and keep search behind a small interface so that switch is a contained change. B is not recommended for a team without operations capacity.

This is a recommendation, not a survey: one option chosen, the deciding reasons named, the cost admitted, the switching conditions stated, and a design choice (the interface) that keeps the decision reversible.

## Making decisions more reversible

When a decision is hard to reverse but must be made, reduce the cost of being wrong:

- **Put a boundary around it** — an interface, adapter, or module that contains the choice, so changing it later touches one place.
- **Adopt incrementally** — pilot with one service, one team, or a fraction of traffic before committing broadly.
- **Use standard formats and protocols** for data and interfaces, so moving away does not require translating proprietary formats.
- **Keep an exit plan** — know how you would migrate off, even roughly, before committing. If no exit is conceivable, treat the decision with the highest care.
- **Time-box experiments** with explicit success criteria decided in advance, so a pilot does not quietly become permanent.

## Deciding with other people

- **Clarify who decides.** Many disputes are really about decision rights. Name the decision-maker (a person, not a committee) and who is consulted.
- **Separate facts from preferences.** Disagreements about facts can be settled with evidence (a benchmark, a prototype). Disagreements about weights (how much operational simplicity matters vs. features) need an explicit trade-off discussion.
- **Steelman the alternatives.** Describe each option as its strongest advocate would. People accept a decision more readily when they see their view represented fairly.
- **Record dissent briefly** in the decision record when it is substantive; it often contains the revisit trigger.
- **Time-box the discussion** in proportion to reversibility.

## Discovering context

- Look for existing decision records, architecture docs, and design discussions; the project may have decided this before or established principles.
- Inspect what the system already uses (manifests, infrastructure config) and how it is operated — the strongest constraint is often what the team already runs.
- Ask about or infer the team's skills, size, and operational capacity.
- Find the real non-functional requirements (traffic, data volume, latency, uptime, compliance) rather than assuming web-scale.
- Learn who must be consulted or must approve decisions of this kind.

## Pitfalls and anti-patterns

- **Solution-first framing.** Starting from "should we adopt X?" rather than from the problem. Fix: frame in terms of outcomes.
- **Résumé-driven choice.** Picking the interesting technology over the appropriate one. Fix: criteria from context; boring tech for core concerns.
- **The survey.** Pros and cons without a recommendation. Fix: weigh, recommend, give conditions.
- **False precision.** Weighted scoring matrices with decimals that disguise a gut call. Fix: name the one or two criteria that decide it.
- **Straw-man alternatives.** Fix: include genuinely viable options, including do-nothing.
- **Analysis paralysis on two-way doors.** Fix: classify reversibility first; decide reversible choices fast.
- **Hand-waving one-way doors.** Picking a data model or public API casually. Fix: slow down, prototype the critical unknown, consult.
- **Ignoring operations.** Comparing features while ignoring who runs, upgrades, and debugs it at 3 a.m. Fix: operational burden as an explicit criterion.
- **Reputation as evidence.** "Everyone uses it." Fix: evidence on your workload and constraints.
- **Undocumented decisions.** Fix: a short record, proportional to the stakes.
- **Relitigating without new information.** Fix: revisit triggers; disagree and commit.

## Safety notes

- For decisions touching security, privacy, data retention, or regulated domains, include security and compliance as must-have criteria and involve the people accountable for them.
- Note licence obligations of chosen components (copyleft terms, usage restrictions) and vendor data-handling terms; flag uncertainty for legal review rather than guessing.
- When a decision involves migrating or deleting data, ensure the plan includes backups and a verified rollback before the irreversible step.

## Verification

Before presenting or acting on a decision, check:

- [ ] The problem is framed in terms of outcomes and constraints, not a pre-chosen solution.
- [ ] Reversibility and blast radius were assessed, and effort matched them.
- [ ] Options are genuinely different and include the status quo.
- [ ] Criteria come from this context; must-haves are separated from trade-offs.
- [ ] Key claims rest on evidence relevant to this workload, not reputation.
- [ ] There is a clear recommendation, its deciding reason, the trade-off accepted, and the conditions that would change it.
- [ ] The decision is recorded where affected people will find it, with alternatives and consequences.
- [ ] Revisit triggers are defined for decisions that are hard to reverse.
