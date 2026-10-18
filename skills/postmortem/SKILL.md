---
name: postmortem
description: >-
  Run and write a blameless post-incident review (postmortem, incident review,
  retrospective, after-action review, learning review) once an incident is
  resolved: gathering evidence, reconstructing an accurate timeline,
  analysing contributing factors across technology, process and organisation,
  recording what went well and where the team got lucky, producing action
  items that are specific, owned, prioritised and tracked, facilitating the
  review meeting, and sharing learnings. Use when asked to "write the
  postmortem", "do an incident review", "what went wrong and how do we
  prevent it", "run a retro on the outage", or to review a near miss, failed
  release or data incident. Not for handling an incident still in progress
  (incident-response) or for deep causal analysis techniques on their own
  (root-cause-analysis).
metadata:
  category: quality
  related: incident-response, root-cause-analysis, observability, release-readiness, project-management, technical-writing, business-communication, debugging
---

# Postmortem

A postmortem turns an incident, which the organisation has already paid for, into learning that reduces the chance and cost of the next one. It produces three things: a **shared, accurate understanding** of what happened and why; **changes** (action items) that make the system and the organisation more resilient; and **knowledge spread** to people beyond those who were involved.

It is not a trial. The moment a review becomes a search for whom to blame, people stop sharing what they actually saw and did, and the review learns only the official story. Blamelessness is not softness; it is the condition for getting accurate information.

Scope: this skill starts once the incident is mitigated. For running the response itself, see `incident-response`. For causal analysis techniques in depth (fault trees, five whys and their limits, causal graphs), see `root-cause-analysis`. This skill applies them in the postmortem context.

## Core principles

**1. Blameless means focusing on conditions, not culprits.** People made the decisions that seemed reasonable given what they knew, the tools they had, and the pressures they were under. The useful question is "what made that action seem right at the time, and what would have made a different action easier?" Fixing the conditions protects against everyone making the same mistake; punishing one person protects against nothing and teaches everyone to hide.

**2. Blameless is not accountability-free.** Teams remain accountable for following up: owning action items, fixing systems, and improving practices. Blamelessness removes punishment for honest mistakes; it does not remove responsibility for learning.

**3. There is rarely a single root cause.** Incidents in complex systems usually need several contributing factors to line up: a latent bug, a change that exposed it, monitoring that did not catch it, a runbook that was out of date, a busy on-call. Naming one "root cause" stops analysis early and leads to a single fix that leaves the rest in place. Look for the set of contributing factors, and for what normally prevents this and why it did not this time.

**4. "Human error" is a starting point, not a conclusion.** If an operator ran the wrong command, ask why the system allowed it, why it looked like the right command, why there was no confirmation or dry run, and why the effect was so large. Every "human error" finding should lead to a system or process change.

**5. Hindsight distorts.** After the fact, the signals look obvious and the right action looks clear. During the incident they were mixed with noise and other plausible explanations. Reconstruct what was known at each moment, not what is known now.

**6. Action items are the product.** A beautifully written narrative with vague or unowned actions changes nothing. Each action should be specific enough to be done, owned by a named person or team, prioritised, and tracked to completion.

**7. Learn from success and near misses too.** What went well, and where the team was lucky, are as informative as what went wrong. Luck that saved you this time is a risk next time. Near misses are cheap incidents; review the significant ones.

**8. Follow the organisation's process.** Many teams have a postmortem format, severity thresholds that require one, a review meeting cadence, and a tracker for actions. Use them. Where none exists, this skill describes what a good review contains.

## Discovering context

Before writing anything:

- **Find the existing process**: postmortem templates or examples, the threshold that triggers one (by severity, customer impact, data loss, near miss), who must attend or approve, where postmortems are published, how actions are tracked.
- **Find the evidence sources**: incident channel and chat logs, ticket history, paging and alert history, dashboards and metrics for the period, logs and traces, deploy and change history, configuration diffs, status page updates, customer support tickets, call recordings or notes.
- **Identify the people involved**: responders, incident commander, the people who made relevant changes, people who noticed the problem, support staff who handled customers, and owners of affected systems. Each saw a different part.
- **Understand the audience**: engineers on the affected team, the wider engineering organisation, leadership, and perhaps customers. The core document is usually for engineers; summaries may be written for others.
- **Check sensitivity**: incidents involving security, personal data or legal exposure may have restricted distribution and specific reporting obligations. Confirm before sharing broadly.

## Timing

Start gathering evidence immediately after mitigation, while memory is fresh and before logs rotate. Hold the review meeting soon (commonly within a few working days), after people have rested. Do not run a review while the incident is still active or while responders are exhausted; quality and tone both suffer.

## The process

### 1. Gather evidence

Collect artefacts before interviewing, so conversations can focus on what the artefacts do not show (intent, reasoning, what people were looking at).

- Export the incident channel and any side conversations relevant to decisions.
- Capture graphs for the relevant metrics with timestamps; dashboards change and data ages out.
- Pull the deploy, configuration and feature-flag history for the affected systems and their dependencies for a window before the incident.
- Pull alert and paging history: what fired, when, who acknowledged, what did not fire.
- Note customer-facing timelines: first support ticket, status page updates, external reports.
- Preserve evidence for security incidents per the organisation's forensic process; do not alter systems under investigation.

Do not copy secrets, credentials or customer personal data into the postmortem document. Summarise or redact.

### 2. Reconstruct the timeline

The timeline is the backbone of the review. Build it from evidence, then fill gaps through conversations.

What a useful timeline contains:

- Timestamps in a single, stated time zone.
- Events from multiple perspectives: system events (deploys, errors, alerts), human actions (who did what), observations (what someone noticed), decisions (and the options considered), and communications (status updates, escalations).
- The source for each entry where possible, so others can verify.
- Key milestones marked: when the triggering change happened, when impact started, when it was detected, when responders engaged, when it was diagnosed, when it was mitigated, when it was resolved.

From the milestones, derive the intervals that matter, for example time to detect (impact start to detection), time to engage, time to mitigate, and total customer impact duration. These show where the largest improvements are available. A two-hour outage with a ninety-minute detection gap needs detection work more than a faster rollback.

**Reconstruct what was known, not just what happened.** For each significant decision, note what information the person had, what they believed, and what else they considered. This is where most learning lives: "the dashboard showed normal error rates because it was filtering out the new endpoint" explains a delayed diagnosis far better than "diagnosis took 40 minutes".

Common timeline gaps to look for:

- The period before detection: when did the problem actually start, as opposed to when anyone noticed?
- Missed signals: alerts that fired but were ignored or not routed, or signals that existed in data but had no alert.
- Unrecorded actions: changes made during response that were not announced in the channel.

### 3. Describe impact

State the impact precisely and honestly:

- Who was affected (all users, a region, a tenant, internal users), how many, and for how long.
- What they experienced (errors, slowness, wrong data, lost data, security exposure).
- Business consequences where known (failed transactions, SLA breaches, support volume, revenue).
- Data effects: any data lost, corrupted or exposed, and whether it has been repaired.

Use measured numbers where available, with the source, and state uncertainty ("between 2% and 5% of checkout attempts, estimated from gateway logs; precise count unavailable because of log sampling"). Neither minimise nor dramatise; the credibility of the whole review depends on this section.

### 4. Analyse contributing factors

Ask, for each part of the timeline: why did this happen, why was it possible, and why was it not caught sooner? Work through several layers rather than stopping at the first answer.

Useful categories to make sure the analysis is broad (a lens, not a form):

| Category | Questions |
|---|---|
| Trigger | What change or event started it? (Deploy, config change, traffic spike, dependency failure, expired certificate, data condition) |
| Latent conditions | What pre-existing weakness did the trigger expose? (Bug, missing limit, single point of failure, capacity headroom gone) |
| Detection | Why did it take as long as it did to notice? Which signals existed, and why did they not alert or get acted on? |
| Response | What helped or hindered diagnosis and mitigation? Access, tooling, runbooks, knowledge, coordination, communication |
| Recovery | Why did recovery take as long as it did? Rollback speed, data repair, dependencies on other teams |
| Process and change management | Did review, testing, staged rollout, or release checks have a gap this passed through? |
| Organisational | Ownership, staffing, on-call load, competing priorities, documentation, training, incentives |

Techniques (see `root-cause-analysis` for depth):

- **Repeated "why", branching**: ask why several times, but allow each answer to branch into multiple causes rather than forcing a single chain.
- **"What normally prevents this?"**: for each failure, identify the control that should have stopped it (a test, a review, an alert, a limit) and why it did not this time. This finds the systemic gaps.
- **Counterfactuals with care**: "if the alert had fired, we would have caught it at 10:05" is useful to estimate the value of a fix; "if Sam had not deployed" is not useful at all.

Signals that analysis stopped too early:

- The conclusion is "human error", "lack of attention", or "should have been more careful".
- There is exactly one cause, and it is the trigger.
- The fix is "be more careful", "remember to", or "communicate better" with nothing structural.
- Detection and response delays are not analysed at all.

### Worked example: from "human error" to contributing factors

First draft finding: "An engineer ran a cleanup script against production instead of staging, deleting 40,000 active sessions and logging out all users."

Taking it further:

- *Why did the script run against production?* The script reads its target from an environment variable. The engineer's terminal still had the production value set from an earlier, legitimate task.
- *Why was that easy to miss?* The prompt did not show the active environment; the script printed no confirmation of the target; staging and production session counts differ by 100x but the script did not show a count before deleting.
- *Why could a cleanup script delete active sessions at all?* It was written to remove expired sessions but its filter used a timestamp column that is reset on every request in production (but not in staging, where a background job is disabled). The filter matched everything.
- *Why did this filter pass review?* It was tested only in staging, where the data shape differed.
- *Why did it take 25 minutes to understand?* The first alert was a login spike, which looked like a traffic surge; session deletion was not logged.
- *What went well?* Sessions are not critical data; users could log back in; support had a status page update out within 10 minutes.
- *Where were we lucky?* The script targeted sessions, not orders, and it ran at a low-traffic hour.

Resulting actions (each tied to a factor): scripts that modify data require an explicit target argument and print the target and affected row count, asking for confirmation, with a dry-run default; production credentials for ad-hoc scripts become short-lived and require an explicit elevation step; staging data shape issue fixed by enabling the background job there; deletion operations logged with counts; runbook for "mass logout" symptoms added. None of these is "be more careful", and together they would have prevented the incident or made it far smaller, regardless of who ran the script.

### Interviewing participants

Short one-to-one conversations before the meeting often surface more than the group session, especially from people who feel exposed.

- Explain the purpose: understanding the system and the conditions, not evaluating performance.
- Ask the person to narrate their experience in order, in their own words, before asking specific questions.
- Ask about what they saw and believed at each point, what they expected to happen, and what surprised them.
- Ask what would have helped: information, tools, access, people.
- Note where their account differs from the logs without challenging them; differences usually reveal a misleading signal, not dishonesty.
- Let them review how their actions are described in the draft.

### 5. Record what went well and where you got lucky

Note specifically what worked: an alert that fired promptly, a runbook that was accurate, a feature flag that allowed fast mitigation, a responder who escalated early, good customer communication. These should be preserved and spread, and stating them makes the review feel fair to the people involved.

Also record luck: "the failure happened during business hours when the database expert was online", "only one region was affected because the rollout was paused for an unrelated reason". Each piece of luck is a dependency on circumstance that may not hold next time, and often deserves its own action item.

### 6. Define action items

Good action items are:

- **Specific**: describes a concrete change with a clear done state. "Add an alert when the payments queue age exceeds 5 minutes, routed to the payments on-call" rather than "improve monitoring".
- **Owned**: one named person or team responsible for getting it done (not "everyone", not "engineering").
- **Prioritised**: distinguishes what must happen soon (to prevent recurrence) from longer-term improvements.
- **Tracked**: lives in the team's normal work tracker with a link from the postmortem, so it competes for time like other work instead of being forgotten in a document.
- **Linked to a contributing factor**: it is clear which weakness each action addresses.
- **Proportionate**: the effort is justified by the risk it reduces.

Aim for a balance across the layers of defence:

| Type | Purpose | Example |
|---|---|---|
| Prevent | Stop this trigger or latent condition | Add validation that rejects the malformed config; fix the bug |
| Detect | Notice faster | Alert on the symptom users experience, not only on the cause |
| Mitigate | Reduce blast radius and speed recovery | Feature flag, staged rollout, faster rollback, rate limits |
| Respond | Improve how people handle it | Update runbook; grant on-call the access they lacked; clarify escalation path |
| Systemic | Address a class of problem | Make the same check apply to all services; add a release-readiness item |

Prefer fewer, high-value actions that will actually be done over a long list that will be ignored. A useful test: if every action is completed, would this incident be prevented, much shorter, or much smaller? If not, something is missing. If a needed action is too large to commit to now, record it as a proposal with an owner responsible for deciding.

Actions to be wary of:

- "Train people" or "remind the team" as the only response to a mistake. Training helps; systems that make the right action easy and the wrong action hard help more.
- Adding a manual approval step to everything; it slows all work and becomes a rubber stamp.
- Actions owned by a team that was not consulted.
- Actions with no realistic chance of being prioritised. Better to state the risk is accepted, explicitly, than to pretend it will be fixed.

### 7. Facilitate the review meeting

The meeting validates the document and deepens understanding; it should not be the first time anyone reads the timeline.

- **Circulate the draft beforehand** so participants can correct facts in advance.
- **Have a facilitator who was not central to the incident** where possible; they can ask naive questions and keep the tone blameless.
- **Open by setting the frame**: the goal is to learn and improve the system; people acted reasonably given what they knew.
- **Walk the timeline**, inviting each participant to add what they saw and thought at key moments.
- **Ask open, curious questions**: "What were you seeing at that point?", "What options did you consider?", "What made that seem like the right call?", "What would have helped?". Avoid "why didn't you…", which presumes the answer and invites defensiveness.
- **Redirect blame gently and immediately** when it appears ("Let's look at what made that step easy to get wrong").
- **Capture new contributing factors and action candidates** as they come up, then agree on actions, owners and priority at the end.
- **Keep it time-boxed**; deep technical dives can continue afterwards with the relevant people.

If you are an AI assistant drafting a postmortem from logs and chat history, you can reconstruct the timeline and propose contributing factors, but mark inferences as such and leave interpretation of people's reasoning to the people involved. Do not assign owners or commit teams to actions on their behalf; propose them for the team to confirm.

### 8. Write and share

A good postmortem document usually contains, in whatever order the organisation uses:

- A short **summary** a busy reader can absorb in a minute: what happened, impact, duration, main contributing factors, and the most important actions.
- **Impact** in measured terms.
- **Timeline** with key milestones and intervals.
- **Contributing factors** analysis.
- **What went well** and **where we got lucky**.
- **Action items** with owners, priority and links.
- **Supporting detail**: graphs, relevant log excerpts (redacted), and links to evidence.
- **Glossary or context** for readers outside the team, when it will be shared widely.

Write in neutral, factual language. Use roles or system names rather than individuals' names where the organisation's norms favour that, and never characterise people ("careless", "should have known"). Describe actions and the conditions around them.

Share appropriately: publish internally where others can find and search it, present significant ones at a wider engineering forum, and consider cross-team action when the same weakness exists elsewhere. For customer-facing incidents, a separate external summary may be needed; it should be accurate, avoid internal blame and internal detail that is not relevant to customers, and be reviewed by whoever owns external communication. See `business-communication`.

### 9. Follow through

The review is not complete until its actions are:

- Review action status at a regular cadence (team meeting, incident review forum).
- When an action is deprioritised, record the decision and who made it, so the accepted risk is explicit.
- Close the postmortem when the critical actions are done, and note the date.
- Periodically look across postmortems for recurring themes (the same service, the same class of change, the same detection gap). Patterns across incidents are often more valuable than any single review.

## Decision guidance

**Does this need a full postmortem?** Follow the organisation's threshold. Absent one, write one when there was significant customer impact, data loss or exposure, a security incident, an SLA breach, a long or confusing response, a near miss that could have been severe, or a recurrence of a previous incident. Smaller incidents may warrant a lightweight review: a short timeline, factors and one or two actions.

**How deep to go?** Scale with impact and with novelty. A recurrence of a known issue may need less narrative and more scrutiny of why the previous actions did not prevent it. A first-of-its-kind failure deserves deeper analysis.

**Who should write it?** Usually someone closely involved (often the incident commander or the owning team), with a facilitator for the meeting. Rotating authorship spreads the skill.

**Recurring incidents**: when an incident resembles a previous one, the most important question is why the earlier review did not prevent it. Common answers:

- The earlier actions were never completed, or were deprioritised without an explicit risk decision.
- The actions addressed the specific trigger, not the latent condition or the class of problem.
- The fix was applied to one service, and the same weakness existed elsewhere.
- The earlier review stopped at "human error" and changed nothing structural.

Link the previous postmortem, state which of its actions were done, and treat the gap in follow-through as a contributing factor in its own right. Recurrence is strong evidence that the review process, not just the system, needs attention.

**Near misses**: something almost went wrong and was caught (by a canary, a sharp-eyed reviewer, or luck). These are the cheapest lessons available. A lightweight review that asks "what stopped this, was that reliable or lucky, and what would have happened otherwise?" is usually enough.

**Security and legal incidents**: may need restricted distribution, involvement of security, legal or privacy teams, and regulatory timelines for notification. Confirm the process before writing or sharing; a blameless internal review is still possible but distribution may be limited.

## Pitfalls

- **Blame, explicit or implied**: naming individuals as causes, or phrasing such as "failed to" and "should have". People stop talking honestly.
- **Single root cause**: stopping at the trigger and missing detection, response and organisational factors.
- **"Human error" as the finding**, with "be more careful" as the action.
- **Hindsight bias**: judging decisions using information that was not available at the time.
- **Timeline from memory only**: inaccurate and missing the pre-detection period. Use evidence.
- **Vague, unowned actions** that are never done; or a long wish list that is equally ignored.
- **Actions not in the tracker**, so they never compete for priority.
- **Postmortem as paperwork**: written, filed, never read, never followed up.
- **Skipping what went well and luck**, missing both what to preserve and hidden risks.
- **Too late**: evidence lost, memories reconstructed, momentum gone.
- **Sensitive data in the document**: credentials, customer data, or security details shared too widely.
- **Defensiveness about the system**: the owning team minimising impact or contributing factors. A neutral facilitator helps.

## Quality bar and verification

A postmortem is good when:

- The timeline is built from evidence, has a single time zone, covers the period before detection, and marks the key milestones and intervals.
- Impact is measured, sourced, and honest about uncertainty.
- Contributing factors span trigger, latent conditions, detection, response and organisation, and the analysis goes beyond "human error".
- Decisions are described in terms of what people knew at the time.
- What went well and where the team got lucky are both recorded.
- Every action is specific, owned, prioritised, tracked and linked to a factor; together they would materially reduce recurrence or impact.
- Language is neutral and blameless throughout.
- No secrets or unnecessary personal data are included, and distribution matches sensitivity.
- The people involved have reviewed the facts and agree it is accurate.
- There is a plan to follow up on actions and a place where others can find and learn from it.

Final check: if a team elsewhere in the organisation read this, would they learn something that helps them avoid a similar incident? If not, the analysis is probably too shallow or too narrowly framed.

## Related skills

- `incident-response` — handling the incident before the review.
- `root-cause-analysis` — deeper causal analysis techniques.
- `observability` — implementing detection improvements.
- `release-readiness` — feeding lessons into future go/no-go checks.
- `technical-writing`, `business-communication` — writing the internal document and external summaries.
- `project-management` — tracking actions to completion.
