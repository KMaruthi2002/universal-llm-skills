---
name: plan-and-decompose
description: >-
  Break a non-trivial task into ordered, verifiable steps: decide whether a
  plan is worth making, find dependencies, sequence risky and uncertain work
  first, define milestones that each leave the system working, and re-plan
  when reality diverges. Use when a task has more than a few steps, spans
  several files or systems, mixes unknowns with routine work, will run long
  or be handed off, or when someone asks "how should we approach this?" or
  "what's the plan?". Not for time estimates (see estimate-effort) or
  long-term product roadmaps (see roadmap-and-prioritization).
metadata:
  category: meta
  related: clarify-requirements, estimate-effort, manage-context, verify-before-done, technical-decision-making, project-management, roadmap-and-prioritization
---

# Plan and Decompose

A plan is a bet about the order in which to learn things and build things. Good plans reduce risk early, keep the work in a working state, and make progress visible. Bad plans are either missing (so work wanders) or so detailed that they are wrong by step three and nobody updates them.

## Scope

Covers turning a goal into an ordered set of steps for one piece of work — a feature, a migration, a research question, a document, an analysis — and keeping that plan honest as you go.

Does not cover:

- Sizing the work in time — see `estimate-effort`.
- Multi-team schedules, staffing, and status reporting — see `project-management`.
- Deciding which of many goals to pursue — see `roadmap-and-prioritization`.
- Choosing between technical options inside a step — see `technical-decision-making`.

## Core principles

### 1. Plan in proportion to uncertainty and cost

Planning is overhead that pays off only when it prevents wasted work. A one-line fix needs no plan. A twenty-file refactor with a data migration needs one. The more steps, the more irreversible the operations, the more people or sessions involved, and the more unknowns, the more planning earns its keep.

### 2. Every step should end in a checkable state

A step is not "work on the parser". A step is "parser handles quoted fields; tests for quoted fields pass". If you cannot say how you will know a step is done, the step is too vague to execute or to report on. Checkable steps also make interruptions cheap: you can resume at the last verified state.

### 3. Attack the riskiest unknowns first

The steps most likely to invalidate the plan are the ones whose outcome you cannot predict: an unfamiliar API, a performance requirement, an assumption about data shape, a dependency you have not tried. Do those early — as spikes if needed — because discovering at step nine that step two's assumption was false wastes steps three through eight. Routine work is predictable; it can wait.

### 4. Keep the system working between steps

Prefer sequences where each milestone leaves something runnable, testable, and shippable (or at least revertible). This is why experienced engineers add a new code path alongside the old one, migrate callers, then delete the old path — rather than ripping out and rebuilding. A working intermediate state means you can stop, hand off, or ship partially at any milestone.

### 5. Plans are hypotheses; re-plan on evidence

The plan is the best guess with current information. When a step reveals something that changes the picture, update the plan explicitly rather than silently drifting. A stale plan is worse than none because it misleads anyone reading it — including you after an interruption.

### 6. Detail near, sketch far

Plan the next few steps in concrete detail and later phases only in outline. Detailed plans for distant work are mostly fiction, and the time spent on them is wasted when early steps change the picture.

## When to plan versus just act

| Signal | Lean toward |
|---|---|
| Fewer than ~3 steps, all obvious, one file or one command | Just act |
| Reversible, cheap to retry, quick feedback | Just act, maybe a mental checklist |
| More than ~5 steps, or several files/systems/people | Write a plan |
| Any irreversible or destructive step (data migration, deploy, delete, send) | Write a plan, isolate that step, confirm before it |
| Significant unknowns about feasibility | Plan a spike first, then plan the rest |
| Work will span sessions, be interrupted, or be handed off | Write the plan down where it persists |
| User asked "how would you approach this?" | Present a plan before doing anything |
| You notice yourself unsure what to do next | Stop and plan |

A useful middle ground: a three-to-seven line plan stated at the start of a medium task. It costs seconds and catches ordering mistakes.

## The process

### Step 1: Fix the goal and the finish line

State the deliverable and how you will know it is done (acceptance criteria — see `clarify-requirements`). Planning against a fuzzy goal produces a fuzzy plan. Note explicit constraints: deadline, things that must not change, environments you may not touch.

### Step 2: Discover the terrain

Before decomposing, learn enough about the existing system to plan realistically: where the relevant code or content lives, how it is built and tested, what depends on what. (`explore-codebase` for code; for documents and analyses, the equivalent is reading the sources and existing material.) Plans made without looking are typically wrong about which steps exist.

### Step 3: List the work

Brainstorm the pieces without ordering them yet. Useful lenses:

- **Outputs backward.** What must exist at the end? What must exist for each of those? Continue until you hit things you can do now.
- **Layers.** Data/storage, logic, interfaces, presentation, configuration, documentation, tests, rollout.
- **Lifecycle.** Build, verify, migrate, deploy, monitor, clean up. The last two are routinely forgotten.
- **Unhappy paths.** Error handling, rollback, backfill for existing data, permissions.
- **People.** Reviews, approvals, announcements, handoffs.

### Step 4: Size each piece

A step is the right size when:

- It has one clear outcome you can verify.
- It can be finished in one sitting (for an agent: without needing to hold more context than comfortably fits).
- If it fails, you know what to roll back.

Split a step that has "and" in its outcome, touches several unrelated areas, or that you cannot describe how to verify. Merge steps that are trivially small and always done together. Do not decompose further than you can usefully track — twenty steps of five minutes each is bookkeeping, not planning.

### Step 5: Map dependencies

For each step, ask: what must be true before this can start? Common dependency kinds:

- **Data/artifact** — B uses an output of A (a schema, a generated client, a dataset).
- **Knowledge** — B's design depends on what A reveals (a spike, a measurement, a user answer).
- **Environment** — B needs access, credentials, a deployed service, an approval.
- **Ordering for safety** — B must happen after A to avoid breaking things (deploy the reader before the writer; add the column before writing to it).

Steps with no dependencies between them can run in parallel (or in any order). Identify the critical path: the longest chain of dependent steps. That chain sets the minimum duration and is where delays hurt most.

### Step 6: Sequence

Order the steps using, in priority:

1. **Hard dependencies** — non-negotiable.
2. **Risk first** — among available steps, do the one most likely to invalidate the plan.
3. **Feedback early** — get something end-to-end running thinly (a "walking skeleton" or "tracer bullet") before deepening any one part, so integration problems appear early.
4. **Value early** — if the work might be cut short, front-load what the user most needs.
5. **Irreversible last and isolated** — put destructive or externally visible steps as late as possible, each behind a checkpoint where you verify and (if appropriate) get confirmation.

When these conflict — the riskiest step is also irreversible — split it: de-risk with a reversible experiment first (dry run, staging, a copy of the data), then do the irreversible part late.

### Step 7: Define milestones

Group steps into milestones: points where the work is in a coherent, verified state that could be paused, demoed, reviewed, or shipped. A good milestone:

- Is meaningful to the user, not just internally ("search works for exact matches" rather than "tokenizer written").
- Leaves tests and builds passing.
- Has a short verification you will actually perform.

For larger work, milestones are where you check in with the user. For agent work in a single session, they are where you re-read the plan and confirm it still holds.

### Step 8: Write it down (at the right fidelity)

Write the plan where it will be seen: in the conversation, a task list your environment provides, a notes file, or a ticket. Include for each step: the outcome, how you will verify it, and notable dependencies or risks. Do not include speculative detail for distant steps.

Illustrative example — a plan for "add soft-delete to projects":

1. Spike: check every query that reads projects; list the ones that must filter deleted rows. (Unknown: how many there are. Determines effort.)
2. Add nullable `deleted_at` column via migration; deploy-safe because nothing reads it yet. Verify: migration runs forward and back on a copy.
3. Introduce a single "active projects" query helper; switch readers to it. Verify: existing tests pass, new test shows deleted rows are hidden.
4. Change delete action to set `deleted_at`. Verify: deleting hides the project; data remains.
5. Admin restore action (if confirmed in scope).
6. Clean up: remove direct table reads that bypass the helper; document behavior.

Note the shape: the risky unknown is first; the schema change is additive and safe; the behavior change comes only after all readers are protected.

### Step 9: Execute, track, and re-plan

While executing:

- Mark steps done only after verifying them, not after writing the code.
- Keep exactly one step "in progress" at a time unless you are deliberately running parallel work. This keeps the state legible.
- After each milestone, ask: does the remaining plan still make sense given what I learned?

Re-plan triggers:

- A step took far longer or was far bigger than expected (signal that later estimates are also off).
- An assumption failed (the API doesn't support batching; the data has nulls everywhere).
- A new requirement or constraint appeared.
- You discovered an easier route.
- The user changed direction.

When re-planning, update the written plan, note briefly why, and if the change affects scope, effort, or risk materially, tell the user before continuing.

## Decomposition patterns

Different kinds of work decompose differently. Choose the pattern that fits.

| Pattern | When it fits | Shape |
|---|---|---|
| Vertical slices | Features with UI, logic, and data | Thin end-to-end slice first, then widen; each slice is usable |
| Horizontal layers | Infrastructure, libraries, when layers have different owners | Bottom-up; risk of late integration — add an early integration check |
| Expand–migrate–contract | Changing anything that others depend on (schemas, APIs, interfaces) | Add new alongside old → move callers → remove old |
| Spike then build | High uncertainty about feasibility or approach | Time-boxed experiment, discard or keep, then plan the real work |
| Strangler | Replacing a legacy component | Route traffic piece by piece to the new component |
| Divide by data | Large batch work, migrations, content edits | Process a small sample, verify, then the rest in batches |
| Question tree | Research and analysis | Main question → sub-questions → evidence needed for each |
| Draft–review–revise | Writing, design | Outline → rough draft → structural review → polish |

### Spikes

A spike is a deliberately throwaway step to answer a question. Give it:

- A specific question ("Can the library stream 1 GB files without loading them into memory?").
- A time box or effort cap. When it runs out, report what you learned even if the answer is "unknown".
- A decision it feeds ("If yes, we stream; if no, we chunk on disk").

Spikes that grow into production code without being revisited are a common source of fragile systems.

## Worked reasoning: re-planning mid-task

Illustration only. The original plan for "migrate image storage from local disk to object storage":

1. Write an upload adapter for object storage behind the existing storage interface.
2. Switch new uploads to the adapter.
3. Copy existing files in batches.
4. Switch reads to object storage.
5. Remove local-disk code.

During step 1 you discover that thumbnails are generated on read by a library that only accepts local file paths. That invalidates step 4 as written: switching reads will break thumbnails. The right move is not to push on and "deal with it at step 4". Instead:

- Record the finding and why it matters.
- Insert a new risky step and move it forward: "Spike: can thumbnail generation take a stream, or should thumbnails be pre-generated at upload time?" — because its answer changes the shape of steps 2–4.
- Re-check later steps: pre-generated thumbnails would also need to be backfilled for existing images, adding work to step 3.
- Tell the user, briefly, that the plan changed and why, if the change affects effort or scope materially.

The general pattern: when a discovery invalidates an assumption, the new unknown becomes the next step, and every downstream step that relied on the old assumption is re-examined before continuing.

## Plans at the right fidelity for the audience

The same work may need different plan representations:

| Reader | What the plan should show |
|---|---|
| You, executing now | Concrete next steps, verification for each, current status |
| The user approving an approach | Milestones, key decisions and risks, irreversible steps, rough size |
| A reviewer | Order of changes and why; where the risky parts are |
| A future resumer (you or someone else) | Status per step, decisions made, what's next, where notes are |
| A stakeholder | Milestones with user-visible outcomes and dates or ranges |

Do not show a stakeholder a forty-step task list, and do not execute from a three-bullet milestone summary.

## Planning in agentic and tool-using work

When you are an agent working with tools:

- **Use the environment's task-tracking facility if one exists**, so the plan is visible to the user and survives context changes. Otherwise keep it in notes or restate it at milestones.
- **Update status as you go** rather than in bulk at the end. A plan that shows three steps in progress at once, or that is updated only when the work is finished, has lost its purpose.
- **Parallelize only independent steps.** Searches across different areas, or edits to unrelated files, can run concurrently. Steps that share files, databases, or decisions must be serialized.
- **Batch what you can predict.** If the next three actions are certain (read these files, then run the tests), do them together; reserve step-by-step caution for actions whose results determine what comes next.
- **Put a check after every action whose effect you have not observed** — writes, commands, deploys — before building on it.

## Discovering context

- Look for existing plans, tickets, roadmaps, or design docs that already decompose the work.
- Check how the project usually ships changes — feature flags, migration tooling, release trains, review requirements — and fit the plan to that process.
- Look at recent similar changes (commit history, merged PRs) to see what steps they needed; they reveal hidden steps like updating fixtures, changelogs, or generated files.
- Respect the user's preferred granularity: some want to approve each step, others want only milestones.

## Pitfalls and anti-patterns

- **Planning instead of learning.** Producing an elaborate plan when the first step should be a quick experiment. If your plan has many steps that depend on an untested assumption, test the assumption first.
- **The happy-path plan.** No steps for errors, migration of existing data, rollback, or clean-up. These are often half the work.
- **Big-bang integration.** Building all parts separately and connecting them at the end. Integration surprises arrive all at once and late. Fix: walking skeleton early.
- **Vague steps.** "Implement backend." Unverifiable and unestimatable. Fix: name the outcome and the check.
- **Irreversible step in the middle.** Deleting the old system before the new one is proven. Fix: expand–migrate–contract; delete last.
- **Plan drift.** The written plan says one thing, the work does another, and nobody updated it. Fix: update on every re-plan trigger.
- **Over-decomposition.** A forty-item checklist for a two-hour task. Fix: merge steps; track at the level where steps have distinct outcomes.
- **Sequencing by comfort.** Doing the familiar, easy parts first and leaving the hard unknown for last. Feels productive, maximizes risk. Fix: risk first.
- **Ignoring the critical path.** Polishing a non-blocking part while the blocking chain waits. Fix: identify the chain; keep it moving.
- **Hidden parallelism assumptions.** Planning parallel tracks that actually share a file, a database, or a reviewer. Fix: check for shared resources before parallelizing.

## Safety notes

Make irreversible and externally visible steps explicit in the plan: deploys, data migrations, deletions, sending messages, spending money, changing permissions. For each, plan a verification beforehand (dry run, backup, staging run, sample batch) and a confirmation point with the user where appropriate. Plan a rollback path or state honestly that none exists.

## Verification

A plan is ready to execute when:

- [ ] The goal and the finish line are stated.
- [ ] Each step has a single outcome and a way to verify it.
- [ ] Dependencies are explicit; the critical path is known.
- [ ] The riskiest unknowns are addressed early, by spikes if necessary.
- [ ] Every milestone leaves the work in a working, verifiable state.
- [ ] Irreversible steps are late, isolated, and preceded by a check.
- [ ] Unhappy paths, migration, clean-up, and documentation are represented where relevant.
- [ ] Detail is concentrated on the near steps; far steps are outlined.
- [ ] The plan is written where it will persist for the duration of the work.

During execution, re-check the plan at each milestone and after any surprise. At the end, every step is either verified done, explicitly dropped with a reason, or listed as remaining in the report.
