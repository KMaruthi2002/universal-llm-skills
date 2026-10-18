---
name: project-management
description: >-
  Plan, run, and close projects of any kind with any method (agile, kanban,
  waterfall, or hybrid): scope and charter the work, set milestones, assign
  clear ownership (RACI-style), keep a risk and issue log, track status
  honestly, control scope creep through explicit change decisions, set
  meeting and reporting cadences, unblock people, manage dependencies, and
  close out with handover and lessons learned. Use when someone asks to "plan
  this project", "set up a project plan", "we're behind, what do we do",
  "track risks", "write a status report", "who owns what", or "wrap up the
  project". Not for deciding what to build (roadmap-and-prioritization),
  breaking work into stories (user-stories), or sizing it (estimate-effort).
metadata:
  category: product-and-communication
  related: plan-and-decompose, estimate-effort, roadmap-and-prioritization, user-stories, business-communication, release-management, postmortem, technical-decision-making, report-results
---

# Project Management

Project management is the work of **getting a defined outcome delivered by a group of people, under constraints, with as few surprises as possible**. Its tools — plans, owners, risk logs, status reports, meetings — exist only to serve three ends: shared clarity about what done means, early detection of problems, and fast decisions when trade-offs appear.

This skill is method-neutral. Agile, kanban, waterfall, and hybrids are options, chosen by the nature of the work and the organization, not by fashion.

**Not covered here:**

- Choosing which projects or features to pursue — see `roadmap-and-prioritization`.
- Writing the product spec — see `product-requirements`.
- Writing backlog items — see `user-stories`.
- Estimating effort and forecasting — see `estimate-effort`.
- Breaking a technical task into steps for yourself — see `plan-and-decompose`.
- Shipping software releases — see `release-management`.
- Reviewing failures in depth — see `postmortem`.

## Core principles

### 1. Define done before planning how

A project without an agreed outcome, scope boundary, and success criteria cannot be planned, tracked, or finished. Why: every later argument about scope, delay, or quality traces back to a different picture of done. Writing it down costs an hour; disagreeing about it costs weeks.

### 2. Every piece of work and every decision has one accountable owner

Shared ownership is no ownership. For each deliverable, risk, and open decision, name exactly one person who is accountable, even if many contribute. Why: when something slips, the question "who is on this?" must have an immediate answer, and people prioritize what they are personally accountable for.

### 3. Make problems visible early; surprises are the real failure

Projects slip; that is normal. What damages trust and outcomes is late discovery. Why: a risk raised early can be mitigated cheaply or the plan adjusted; the same issue raised the week before the deadline leaves only bad options. Reward early bad news; never punish it.

### 4. Scope, time, cost, and quality trade against each other

You cannot fix all of them. When one changes, at least one other must flex, and someone with authority must choose which. Why: pretending otherwise produces hidden quality cuts or silent overruns, which are worse than explicit trade-offs.

### 5. The plan is a model, not a promise

A plan is the current best understanding of how the work will unfold. Update it as you learn. Why: a plan that is never revised either becomes fiction that people ignore or a stick to beat people with. Re-planning is not failure; refusing to re-plan is.

### 6. Minimize process to what the project needs

Use the lightest set of artifacts and rituals that gives clarity and early warning for this project's size, risk, and audience. Why: process has a cost in attention; excess process slows the work it is meant to protect and trains people to ignore it.

### 7. Fit the organization

Use the organization's existing tools, templates, terminology, reporting lines, and governance. Why: a project run in an alien way creates friction with every interface — finance, leadership, other teams — and the project manager spends their energy translating instead of unblocking.

## Choosing an approach

| Factor | Leans iterative (agile, kanban) | Leans plan-driven (waterfall, stage-gate) |
|---|---|---|
| Requirements | Uncertain, expected to evolve | Stable, well understood, externally fixed |
| Feedback | Users can try partial results | Value only exists when complete (a building, a migration cut-over, a regulatory submission) |
| Cost of change | Low (software, content) | High (hardware, construction, contracts, physical logistics) |
| Stakeholders | Available for frequent review | Available at defined checkpoints |
| Compliance | Light or adaptable | Requires documented phases and sign-offs |
| Work arrival | Continuous stream of varied items (kanban fits) | Discrete project with a defined end |

Hybrids are common and legitimate: a fixed-date, stage-gated program with iterative delivery inside each stage; a kanban flow for operational work alongside a planned migration. Choose consciously and tell the team which parts are fixed and which are adaptive.

Key mechanics by approach (brief):

- **Iterative / time-boxed** (e.g. sprints): fixed-length cycles; plan, build, review, adapt. Progress = working increments. Watch for: cycles that become mini-waterfalls, ceremonies without decisions.
- **Flow-based** (e.g. kanban): visualize work, limit work in progress, manage flow, measure cycle time and throughput. Watch for: no WIP limits (then it is just a list), no explicit policies for what "done" in each column means.
- **Plan-driven** (e.g. phased/waterfall): detailed upfront plan, phases with entry/exit criteria, change control. Progress = milestones achieved. Watch for: "90% done" syndrome, testing squeezed at the end, change requests ignored until too late.

## The project lifecycle

### 1. Initiate: charter the project

Capture, in whatever form the organization uses (charter, brief, kickoff doc, project page):

- **Why**: the problem or opportunity, and how this project ties to a goal.
- **Outcome and success criteria**: what will be true when it is done, and how it will be judged.
- **Scope**: what is in, and explicitly what is out.
- **Constraints**: deadline (and why it is a deadline), budget, people, technology, regulation.
- **Stakeholders**: who sponsors, who decides, who is affected, who must be consulted or informed.
- **Assumptions and known risks.**
- **Ownership**: the project lead, and the accountable owner of each major deliverable.

Get the sponsor to confirm it. Why: a charter is the reference point for every later change discussion.

### 2. Plan: just enough structure

- **Break down the work** into deliverables, then into work packages or items small enough to estimate and track (see `plan-and-decompose`, `user-stories`).
- **Estimate** with the people doing the work and express uncertainty as ranges (see `estimate-effort`).
- **Map dependencies** — internal and on other teams, vendors, approvals. The longest chain of dependent work (the critical path) determines the earliest finish; know it.
- **Set milestones**: meaningful, verifiable checkpoints (a demonstrable result, a decision, a sign-off), not dates when "phase 2 is 50% done". Good milestones are binary — achieved or not.
- **Build in buffer** where uncertainty is highest, and make buffer visible rather than padding every task invisibly. Why: hidden padding gets consumed by procrastination and scope; visible buffer can be managed.
- **Plan the cadences** (see below) and the reporting.
- **Start the risk log.**

Planning depth should match certainty: detailed for the next few weeks, coarser beyond. Rolling-wave planning — refining the near term as you go — is usually more accurate than detailed long-range plans.

### 3. Execute and monitor

The project lead's daily job:

- Keep work flowing: remove blockers, chase decisions, coordinate handoffs.
- Track progress against milestones and the critical path, not just activity.
- Maintain the risk and issue logs.
- Manage changes to scope through an explicit decision.
- Communicate status on the agreed cadence.
- Watch team health: overload, conflict, unclear priorities.

### 4. Close

Covered in its own section below. Projects that are not formally closed linger, consume attention, and never capture their lessons.

## Ownership: RACI as an idea

RACI (Responsible, Accountable, Consulted, Informed) and its variants are a way to make roles explicit for each deliverable or decision. The value is in the conversation it forces, not in the matrix itself.

| Role | Meaning | Rule of thumb |
|---|---|---|
| Accountable | Owns the outcome; makes the final call; answers for it | Exactly one per item |
| Responsible | Does the work | One or more |
| Consulted | Gives input before the decision or work (two-way) | Keep few; each adds delay |
| Informed | Told after (one-way) | Can be many; use broadcast channels |

Practical guidance:

- Apply it to **decisions and deliverables that cross team boundaries** — that is where ambiguity lives. A full matrix for every task is overkill.
- If an item has no Accountable or several, fix that before work starts.
- If many people are Consulted, decisions will be slow; ask whether some can be Informed instead.
- Write down **decision rights** for recurring decision types (scope changes, budget, design, go/no-go) — who decides, who must be consulted, and how fast.

Lighter alternatives: a simple "owner" column on each deliverable and decision; a "directly responsible individual" per workstream. Use what fits the organization.

## Risks and issues

A **risk** is something that might happen and would affect the project. An **issue** is something that has happened and needs resolution. Track both, separately or in one log with a type.

What a useful risk entry captures:

- **Description** in cause → event → effect form: "Because the vendor's API is still in beta (cause), it may change before our launch (event), forcing rework of the integration and a 2–4 week delay (effect)." Why: vague risks ("vendor risk") cannot be mitigated.
- **Likelihood and impact** — simple scales (low/medium/high) are fine; precision is false.
- **Owner** — one person.
- **Response**: avoid (change the plan to remove it), reduce (lower likelihood or impact), transfer (insurance, contract terms, another team), accept (consciously, with a contingency).
- **Trigger or early warning sign** — what would tell you it is happening.
- **Status and next review date.**

Practice:

- Run a **pre-mortem** at kickoff: "It is six months from now and the project failed. Why?" Each answer is a candidate risk. Why: people name risks more freely when imagining a failure than when asked to predict one.
- Review the top risks on a regular cadence; retire stale ones, add new ones.
- Escalate risks that exceed the team's authority to mitigate — early, with options.
- Common risk sources to probe: dependencies on other teams or vendors, key-person dependencies, unfamiliar technology, unclear requirements, regulatory or legal review, data migration, environment and access provisioning, approvals, holidays and availability, competing priorities for shared people.

## Status tracking and reporting

### Track outcomes and leading indicators, not busyness

Useful measures, depending on approach:

- Milestones achieved vs. planned; critical-path items on track or not.
- For iterative work: working increments delivered; scope remaining vs. time remaining (burn-up charts show scope changes honestly; burn-downs can hide them).
- For flow work: throughput, cycle time, work in progress, blocked items and how long they have been blocked.
- Budget spent vs. planned against value delivered.
- Open risks and issues by severity; decisions pending and how long they have been pending.

"Percent complete" by effort spent is a weak signal: the last 10% often takes as long as the first 90%. Prefer counting finished, verified deliverables.

### Status reports that work

A good status update:

- **Leads with the overall state and what the reader must do**: on track / at risk / off track, and any decision or help needed. Why: most readers read only the first lines.
- **Uses status labels honestly and with defined meanings.** If a traffic-light system is used, define it (e.g. at risk = a milestone may slip without action; off track = a milestone will slip, or scope/cost must change). Why: undefined colours drift toward "green until suddenly red" ("watermelon status": green outside, red inside).
- **Shows change since last report**: what was completed, what slipped, what is new.
- **Names top risks and issues** with owners and next steps.
- **Lists decisions needed**, from whom, by when, with options and a recommendation.
- **Is short.** Detail goes in links.

See `business-communication` for writing technique and tone. Status reports go to people on a schedule; send or post only after the sender has approved, unless they have explicitly delegated that.

### When the project is off track

1. **Get the facts**: what is late, by how much, why, and what it affects (critical path?).
2. **Generate options**: cut or defer scope, add capacity (rarely fast — new people slow a team at first), extend the date, accept lower quality in a specific, conscious way, change the approach, or stop.
3. **Estimate the consequences** of each option.
4. **Escalate with a recommendation** to whoever owns the trade-off — before the date passes, not after.
5. **Re-baseline** the plan once a decision is made, and communicate the new plan and why.

## Managing scope creep

Scope creep is unplanned growth in scope without corresponding change in time, cost, or acknowledged risk. Some scope change is healthy learning; the problem is change without decision.

- **Have a baseline**: the charter and plan define current scope.
- **Route every addition through a lightweight change decision**: what is requested, why, the impact on time/cost/risk/other scope, and who decides. For small projects this is a conversation and a note; for contracted or regulated work it may be a formal change request.
- **Offer trade-offs, not refusals**: "We can add this if we drop X or move the date by two weeks."
- **Watch for quiet creep**: gold-plating by the team, "small" asks that accumulate, requirements re-interpreted during review. Count them; their sum is often large.
- **Record decisions** in the change log or decision log, so later readers know why scope changed.

## Cadences and meetings

Every recurring meeting should have a purpose, an owner, a decision or output, and a reason it cannot be asynchronous. Typical cadences (choose what fits; names vary):

| Cadence | Purpose | Notes |
|---|---|---|
| Short daily or frequent sync | Coordinate today's work, surface blockers | Keep to coordination; take problem-solving offline with the relevant people |
| Weekly or iteration planning | Commit to near-term work | Based on capacity and priorities |
| Review / demo | Show working results to stakeholders, get feedback | Real results, not slides about progress |
| Retrospective | Improve how the team works | Produce one or two concrete changes, and check them next time |
| Risk and dependency review | Re-examine top risks and cross-team dependencies | Can fold into a weekly meeting for small projects |
| Steering / sponsor check-in | Decisions beyond the team's authority; overall health | Bring options and recommendations, not raw status |
| Status report | Keep wider stakeholders informed asynchronously | Often replaces a status meeting |

Prefer asynchronous updates for information and synchronous meetings for decisions and discussion. Cancel meetings that stop producing outcomes.

## Unblocking and dependencies

A large share of a project lead's value is removing obstacles quickly.

- **Make blockers visible**: a blocked flag on work items, with the date it became blocked and who can unblock.
- **Classify the blocker**: waiting on a decision, on another team, on access or environment, on information, on an external party. Each has a different remedy.
- **Act on blockers daily**: find the person who can resolve it, give them the context they need to act quickly, propose a resolution, set a date.
- **Escalate by age and impact**: a critical-path item blocked for more than a short agreed period goes up a level, with a clear ask.
- **Manage dependencies as commitments**: for each cross-team dependency, agree what, by when, who owns it on each side, and how you will know it is on track. Check in before the due date, not after.
- **Reduce dependencies structurally** where possible: decouple interfaces, stub or mock what is not ready, sequence work so the riskiest dependencies are resolved early.

## Closing out

Closing is a phase, not an event. It includes:

- **Acceptance**: confirm with the sponsor that success criteria are met, or record which are not and why.
- **Handover**: transfer ownership to whoever runs the result — operations, support, the product team, the client — with documentation, access, training, and known issues. Make the handover explicit and acknowledged. Why: unowned results decay, and post-project problems land on whoever is nearest.
- **Administrative closure**: release budget and people, close contracts and accounts, archive documents in the organization's usual place, revoke temporary access.
- **Outcome tracking**: if success depends on effects after delivery (adoption, savings), name who will measure them and when.
- **Lessons learned**: a retrospective of the whole project — what to repeat, what to change — captured where future projects will find it. Focus on systemic causes, not blame (see `postmortem` for technique).
- **Recognition**: acknowledge the people who did the work.
- **Communicate closure** to stakeholders so they know where to go next.

Projects that are cancelled deserve the same close-out, especially the lessons and the handover of anything partially built.

## Discovering context

- **Find the organization's project practices**: templates, tools, status formats, governance gates, approval thresholds, how budget is tracked. Use them.
- **Identify the real decision-makers and sponsor**, which may differ from the org chart.
- **Learn the calendar**: fiscal deadlines, freeze periods, holidays, other big launches competing for the same people.
- **Check the history**: similar past projects, their actual vs. planned duration, and what went wrong. Past performance on similar work is the best estimate.
- **Understand people's availability**: what share of each person's time is really available after support, meetings, and other projects.
- **Ask the team** how they prefer to work and communicate within the organization's constraints.

## Pitfalls and anti-patterns

- **No agreed definition of done.** Recognize by recurring "I thought it included…" conversations. Fix with a charter and success criteria signed off by the sponsor.
- **Plan built without the doers.** Estimates set by managers alone are routinely wrong. Fix by planning with the people doing the work.
- **Watermelon status.** Green reports until a sudden red. Fix by defining status meanings, reporting leading indicators, and rewarding early warning.
- **Activity mistaken for progress.** Long task lists ticked off while milestones slip. Fix by tracking verified deliverables and the critical path.
- **Everyone is consulted on everything.** Decisions stall. Fix with explicit decision rights.
- **Silent scope creep.** Fix with a baseline and change decisions.
- **Adding people to a late project.** Onboarding costs usually make it later in the short term. Consider it only for well-separable work with enough runway.
- **Risk log as ritual.** A list made at kickoff and never reviewed. Fix by reviewing the top few risks on a cadence and retiring or updating them.
- **Meetings as the work.** Calendars full of status meetings. Fix with asynchronous updates and a purpose for every meeting.
- **Hero dependency.** One person holds critical knowledge. Fix by pairing, documentation, and cross-training early.
- **The project that never ends.** No close-out, endless "phase 2". Fix with explicit acceptance and handover; new scope becomes a new project.
- **Method dogma.** Forcing a method onto work it does not fit, or debating ceremonies instead of delivering. Fix by choosing by the factors above and adapting.

## Quality bar and verification

At kickoff:

- [ ] Outcome, success criteria, scope in/out, and constraints are written and confirmed by the sponsor.
- [ ] Every major deliverable and recurring decision type has one accountable owner.
- [ ] The plan was built with the people doing the work; estimates have ranges; the critical path and key dependencies are known.
- [ ] Milestones are verifiable, not percentages.
- [ ] Top risks are logged in cause → event → effect form with owners and responses.
- [ ] Cadences and reporting are agreed and proportionate.

During the project:

- [ ] Status reports lead with state and asks, use defined status meanings, and show change since last time.
- [ ] Every blocked item has an owner and an age; old blockers are escalated.
- [ ] Scope changes have recorded decisions and their impact.
- [ ] Risks are reviewed on cadence; the log reflects reality.
- [ ] The plan has been re-baselined when reality diverged, and the change communicated.

At close:

- [ ] Acceptance against success criteria is recorded.
- [ ] Handover is explicit and acknowledged by the receiving owner.
- [ ] Lessons are captured where future projects will find them.
- [ ] Temporary access, budgets, and resources are released.

A useful health check at any point: could a stakeholder answer, in under a minute from the project's artifacts, "Are we on track? What's the biggest risk? What decision is needed from whom?" If not, the tracking is not serving its purpose.

## Working as an assistant

- When asked to "make a project plan", ask (or state assumptions about) the outcome, deadline and why it is fixed, available people, and the method the organization uses.
- Produce plans and status drafts for the human project lead to review; do not send status reports, meeting invites, or escalations on someone's behalf without explicit confirmation.
- When updating shared trackers, confirm before bulk changes, reassignments, or closing items, since they notify and affect other people.
- Never fabricate progress, percentages, or risk ratings; mark unknowns as unknown.

## Related skills

- `plan-and-decompose` — breaking work into steps.
- `estimate-effort` — estimates, ranges, and forecasts.
- `roadmap-and-prioritization` — what to do and in what order.
- `user-stories` — backlog items for iterative delivery.
- `business-communication` — status updates, escalations, announcements.
- `technical-decision-making` — recording decisions.
- `release-management` — shipping software results.
- `postmortem` — learning from failures and close-out retrospectives.
