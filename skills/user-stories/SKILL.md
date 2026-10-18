---
name: user-stories
description: >-
  Write, split, and refine user stories and their acceptance criteria so each
  backlog item delivers a thin, testable slice of user value: apply INVEST,
  slice vertically rather than by layer, split epics with proven patterns,
  write acceptance criteria (Given/When/Then as one option among several),
  cover edge cases, agree a definition of done, and catch tasks disguised as
  stories. Use when someone asks to "write user stories", "break this epic
  down", "add acceptance criteria", "refine the backlog", "this story is too
  big", or is preparing items for sprint or iteration planning. Not for the
  overall feature spec (product-requirements), choosing what to build first
  (roadmap-and-prioritization), or test-case design (qa-test-planning).
metadata:
  category: product-and-communication
  related: product-requirements, requirements-analysis, plan-and-decompose, estimate-effort, qa-test-planning, project-management, roadmap-and-prioritization, test-driven-development
---

# User Stories

A user story is a **placeholder for a conversation** about a small piece of value for someone, plus enough written agreement (usually acceptance criteria) that the team will know when it is done. The written card is not the requirement; the shared understanding is. The goal of this skill is to produce backlog items that a team can pick up, build, verify, and ship independently, and that each move a real user outcome forward.

**Not covered here:**

- The overall problem, goals, and metrics for a feature — see `product-requirements`.
- Eliciting needs from stakeholders — see `requirements-analysis`.
- Deciding which stories to do first across the backlog — see `roadmap-and-prioritization`.
- Sizing and forecasting — see `estimate-effort`.
- Detailed test case design and test planning — see `qa-test-planning`.
- Breaking down purely technical work with no user-facing slice — see `plan-and-decompose`.

## Core principles

### 1. A story describes a change in what someone can do, not work someone will do

"As a shopper I can save my cart and return to it on another device" is a story. "Build the cart persistence API" is a task. Why it matters: a task can be completed without anyone being better off, so it gives no signal of progress and no opportunity for feedback. A story, when done, can be demonstrated to a user and judged.

### 2. Thin vertical slices beat thick horizontal layers

A vertical slice cuts through every layer needed (interface, logic, data) to deliver a small but complete behaviour. Horizontal slicing ("database story", "API story", "UI story") delays all value and all integration risk until the last layer lands. Why: integration is where surprises live, and feedback is only possible on something a user can touch. Thin slices also make progress honest: 7 of 10 slices done means roughly 70% of value, whereas 2 of 3 layers done means 0%.

### 3. Acceptance criteria define "done" before work starts

Criteria agreed before building turn arguments at the end into decisions at the beginning. They are the contract between product, development, and testing. Why: if "done" is decided after the work, it is decided by whoever is most tired or most senior, not by what the user needs.

### 4. Small enough to finish, large enough to matter

A story should be completable well within one iteration (a common heuristic: a few days of team effort at most), and still deliver something a user or stakeholder can observe. Why: small items flow, expose problems quickly, and reduce the cost of being wrong. But a story so small that it has no observable effect is a task.

### 5. The conversation is the point

Stories are refined through discussion between the people who understand the need and the people who will build and test it. Why: written words underspecify; examples and questions surface the misunderstandings. A perfectly written story nobody discussed is riskier than a rough one the team talked through.

### 6. Follow the team's conventions

Teams differ in whether they use the "As a… I want… so that…" form, how they write criteria, what fields their tracker requires, and how they define ready and done. Match them. Why: consistency lets people scan the backlog and trust it; a novel format, however good, adds friction.

## INVEST, and why each letter matters

INVEST is a checklist for whether an item is a good story. Treat it as diagnostic, not as a gate that every story must pass perfectly.

| Letter | Meaning | Why it matters | Common violation and fix |
|---|---|---|---|
| **I**ndependent | Can be built and shipped without waiting on another story | Allows reordering by value; avoids blocked work | Story B needs story A's data model. Fix: merge, or re-slice so each carries the piece it needs, or accept the dependency and order them explicitly |
| **N**egotiable | Describes the need, not a fixed solution | Leaves room for the team to find cheaper ways | Story dictates UI layout and endpoints. Fix: move details to notes or criteria that state outcomes |
| **V**aluable | Delivers value to a user, customer, or stakeholder | Ensures every item moves an outcome | "Set up database tables". Fix: fold into the first story that needs the tables |
| **E**stimable | The team understands it well enough to size | Signals sufficient shared understanding | Unknown technology or vague need. Fix: split out a time-boxed spike, or clarify |
| **S**mall | Fits comfortably in an iteration | Flow, fast feedback, less risk | Epic-sized story. Fix: split with the patterns below |
| **T**estable | Has clear criteria to verify | Makes done unambiguous | "Should be user-friendly". Fix: concrete criteria or remove |

Independence is the hardest to achieve and the one most worth relaxing deliberately when the alternative is artificial slicing. Valuable and Testable are the ones never to relax.

## Anatomy of a good story

What a story usually contains (field names vary by team and tool):

- **A short title** that names the behaviour, readable in a list: "Save cart across devices", not "Cart story 3".
- **Who, what, why** — in whatever form the team uses. The "As a [role], I want [capability], so that [benefit]" form is popular because it forces the *who* and the *why*; teams that drop it should still capture both. The *why* is the most frequently omitted part and the most useful, because it lets the team choose a simpler solution that still meets the need.
- **Acceptance criteria** — the conditions that must hold for the story to be accepted.
- **Notes and context** — links to the spec, designs, research, related stories; known constraints; out-of-scope reminders.
- **Open questions** — anything that must be answered before or during work.
- Optional, depending on the team: size estimate, priority, labels, dependencies.

The role should be specific: "returning shopper with a saved payment method" tells the team more than "user". Avoid "As a developer" or "As the system" for user-facing stories; those are usually technical tasks or enablers (see below).

## Acceptance criteria

### What good criteria do

- State **observable outcomes**, not implementation steps.
- Cover the **main flow**, the important **alternate flows**, and the **edge and error cases** that matter.
- Are **unambiguous enough to test** — two people reading them would test the same thing.
- Are **few enough to read** — if a story needs fifteen criteria, it probably needs splitting.

### Formats (choose one consistent with the team)

| Format | Looks like | Strengths | Weaknesses | Choose when |
|---|---|---|---|---|
| Checklist / rule list | "Cart contents persist for 30 days after last change." | Fast, compact, easy to scan | Context and preconditions can be implicit | Simple stories; experienced team with shared context |
| Given / When / Then scenarios | "Given a signed-in shopper with 3 items in their cart, when they sign in on another device, then the cart shows the same 3 items." | Makes preconditions, action, and outcome explicit; maps to automated tests | Verbose; can bloat into scripts of UI clicks | Behaviour with important preconditions or many variants; teams using behaviour-driven tooling |
| Example tables | Rows of inputs and expected outputs | Excellent for rules with many combinations (pricing, permissions, validation) | Less readable for flows | Business rules, calculations, permission matrices |
| Rules + examples | A rule stated plainly, followed by one or two concrete examples | Captures intent and precision together | Requires discipline | Any story where the rule is subtle |

Given/When/Then is one option, not the definition of acceptance criteria. Use it where its explicitness pays for its verbosity.

Illustrative example (rules + examples, for a discount-code story):

> Rule: A code applies only if the cart subtotal meets the code's minimum, measured before tax and shipping.
> - Example: Code SAVE10 (minimum 50.00), subtotal 49.99 → code rejected with message explaining the minimum.
> - Example: Code SAVE10, subtotal 50.00 → 10% discount applied.
>
> Rule: Only one code per order.
> - Example: SAVE10 applied, shopper enters FREESHIP → shopper is told only one code can be used and offered to replace the current one.

### Writing scenarios well (when using Given/When/Then)

- Describe **behaviour in domain language**, not UI mechanics. "When they apply the code" rather than "When they click the blue Apply button at top right". Why: UI-coupled scenarios break with every design change and hide the actual rule.
- **One behaviour per scenario.** Multiple "When" steps usually mean multiple scenarios.
- Make **Given** state only what matters for this outcome. Irrelevant setup obscures the point.
- **Then** should be observable by a user or tester, not an internal state ("record is written to table X") unless the story is explicitly about that.
- Use **concrete values**. "A cart with 3 items totalling 62.00" is testable; "a cart with some items" is not.

### Edge-case prompts

Run through these when drafting criteria; include the ones that matter for this story, and consciously exclude the rest:

- **Empty / none**: no items, no results, no history, first-ever use.
- **Boundaries**: exactly at a limit, one over, one under, maximum length, zero, negative.
- **Volume**: very many items, very long text, large files.
- **Invalid input**: wrong format, missing required data, unsupported characters.
- **Permissions**: user lacks access; access changes mid-flow; shared vs. private data.
- **State and timing**: concurrent edits, stale data, session expiry, retry, double submission, interruption mid-flow.
- **Failure of dependencies**: network loss, third-party service down, timeout, partial success.
- **Recovery**: undo, cancel, back navigation, error messages that tell the user what to do.
- **Context**: different devices, locales, time zones, currencies, assistive technologies.
- **Existing data**: what happens to records created before this change.

Not every edge case belongs in the same story. Splitting rare or complex cases into their own stories is often the right move (see splitting patterns).

## Definition of Ready and Definition of Done

These are team agreements, not per-story criteria.

- **Definition of Ready** (optional, use with care): what a story needs before the team commits to it — typically clear value, acceptance criteria, known dependencies, a size estimate, designs if required. Why it helps: prevents starting work that will stall. Why to use with care: a strict ready gate can become a bureaucratic handoff that kills the collaboration stories depend on. Prefer "ready enough to start the conversation in planning".
- **Definition of Done** (strongly recommended): what is true of *every* completed story regardless of its specific criteria — e.g. code reviewed, tests written and passing, accessible, documented where needed, deployed to a given environment, analytics events firing, product owner accepted. Why: it keeps quality standards from being renegotiated per story, and keeps hidden work (docs, monitoring, accessibility) from being skipped under pressure.

Acceptance criteria are specific to a story; the definition of done applies to all. Do not repeat the definition of done inside every story's criteria — reference it.

## Slicing and splitting

### Why split vertically

The test of a good split: **each resulting story is still valuable and demonstrable on its own**, and the first slice can ship even if later slices never do. If one piece is useless without the others, you have split horizontally.

### Splitting patterns

Try these roughly in order; the first that yields sensible, valuable slices wins.

| Pattern | How | Illustrative (epic: "Shoppers can pay at checkout") |
|---|---|---|
| Workflow steps | Deliver steps of a flow separately, or a simple end-to-end version first then enrich steps | First: pay with a card, no saved methods. Later: save card; choose saved card |
| Business rule variations | Implement the simplest rule first, then variants | First: one currency. Later: multi-currency |
| Happy path, then alternatives | Main success path first; errors and alternatives as later stories (but basic error handling in the first) | First: successful payment and a generic decline message. Later: specific decline reasons and retry guidance |
| Data variations | Handle one type of data, then others | First: credit cards. Later: digital wallets; bank transfer |
| Input/interface variations | One input method or channel first | First: web. Later: mobile app |
| Operations (CRUD) | Create and view first; edit and delete later | Saved addresses: add and use first; edit; delete |
| Performance / quality levels | Make it work, then make it fast or scale | First: works for typical carts. Later: performance target for 200+ line carts |
| Defer complexity | Manual or simplified handling of a rare case first | First: refunds handled by support manually. Later: self-service refunds |
| Roles / personas | Serve one user type first | First: individual buyers. Later: business accounts with approvers |
| Spike + implementation | When unknowns block estimation: a time-boxed investigation, then the real story | Spike: evaluate payment provider's 3-D Secure flow (2 days, output: decision and sample) |

Patterns that usually indicate a bad split:

- By technical layer (frontend / backend / database).
- By component or team ownership, unless teams genuinely cannot collaborate on a slice — and then fix the collaboration if you can.
- "Part 1 / Part 2" of the same behaviour with no independent value.
- Splitting off "testing" or "documentation" as separate stories — these belong in the definition of done.

### Worked reasoning (illustrative)

> Epic: "Team admins can manage member permissions."
>
> First instinct: "Build permissions data model", "Build permissions API", "Build permissions UI". All horizontal — nothing usable until all three ship.
>
> Ask: what is the smallest thing an admin could actually use? Probably: *make another member an admin*. That alone solves the most common support request (admins leaving the company). So:
>
> 1. Admin can promote a member to admin, and demote an admin to member (but not the last admin). — Valuable alone; touches all layers thinly.
> 2. Admin can see a list of members with their roles. — Might fold into 1 if trivial.
> 3. Admin can assign a read-only role. — New rule variation.
> 4. Admin can set per-project permissions. — Large; likely its own epic later.
> 5. Changes to roles are recorded in the audit log. — Could be in definition of done if audit is required for all admin actions; otherwise a story.
>
> Story 1's criteria must include the edge case "cannot demote the last admin", because shipping without it creates a lock-out bug.

### Hierarchy and naming

Teams use different words — theme, initiative, epic, feature, story, task, sub-task. Use the team's terms. The useful distinction is:

- **Larger containers** (epic or feature): a goal or capability too big for one iteration; usually maps to a spec or a roadmap item.
- **Stories**: the unit of value that flows through the team.
- **Tasks**: the technical steps a developer takes to deliver a story; usually not prioritised by product and often not tracked individually.

## Tasks disguised as stories, and what to do with real technical work

Signs a "story" is really a task:

- The role is "developer", "system", or "team".
- The benefit is technical ("so that the code is cleaner").
- Nobody outside the team could tell it was done.
- It is one layer of a feature.

What to do:

- **If it supports a user story**, fold it into that story as a task, or into the first slice that needs it.
- **If it is genuine enabling work** (upgrading a framework before end of support, reducing build time, paying down debt that slows delivery, compliance or security work), keep it as a distinct item but state the **real benefit in outcome terms**: "so that we can keep receiving security patches after <date>", "so that deploys take under 10 minutes instead of 40". Make it testable. Some teams call these enablers, technical stories, or chores; use whatever label is local.
- **Do not dress technical work in a fake user** ("As a user, I want the database migrated…"). It misleads prioritisation and erodes trust in the backlog.

Bugs are usually tracked separately, with steps to reproduce and expected vs. actual behaviour; they can still be prioritised alongside stories.

## Process

### 1. Start from the goal

Read the spec, epic, or request. Identify the user, the outcome, and how success will be measured. If those are missing, ask before writing stories — see `product-requirements` and `clarify-requirements`. Stories written without a goal tend to describe features rather than value.

### 2. Map the flow before writing cards

For anything bigger than a few stories, sketch the user's journey as a sequence of activities and steps (story mapping is one technique for this). Under each step, list possible capabilities. Then draw a line: what is the smallest set across all steps that delivers an end-to-end outcome? That set is the first release or "walking skeleton". Why: writing stories one at a time from the top of a list tends to perfect the first step and never reach the end of the flow.

### 3. Draft stories and criteria

Write each story with who, what, and why, and a first set of acceptance criteria. Mark assumptions and open questions. Use concrete examples.

### 4. Refine together

Review with the people who will build and test (often called refinement, grooming, or a "three amigos" session: product, development, testing). Walk through examples, find edge cases, challenge size, look for cheaper solutions. Update the story with what was agreed. If you are drafting without access to the team, list the questions this conversation should answer.

### 5. Split what is too big or too uncertain

Apply the splitting patterns. Turn blocking unknowns into time-boxed spikes with a defined output (a decision, a prototype, an estimate).

### 6. Order by value, risk, and dependency

Put the slices that deliver most value or retire most risk first. Make necessary dependencies explicit. See `roadmap-and-prioritization`.

### 7. Verify on completion

When a story is done, check it against every acceptance criterion and the definition of done, and demonstrate it to the person who represents the user. If criteria turned out wrong during build, update them and record why — do not quietly accept something different.

## Discovering context

- **Look at existing stories** in the team's tracker, especially ones the team considered well-written. Match their structure, level of detail, criteria format, and labels.
- **Find the definition of done and any definition of ready.** Reference rather than restate them.
- **Check the team's sizing approach** (points, t-shirt sizes, counts, no estimates) and the typical size of completed stories, so new stories are comparable.
- **Learn domain vocabulary** — names of user roles, objects, and states — and use them consistently. Inconsistent names in criteria cause defects.
- **Check what automated testing exists.** If the team turns scenarios into automated tests, criteria format matters more and should follow their tooling conventions.

## Pitfalls and anti-patterns

- **Horizontal slicing.** Stories per layer or component. Recognize by stories that cannot be demonstrated alone. Fix by re-slicing around user-visible behaviour.
- **Missing "so that".** The benefit is omitted or circular ("so that I can save my cart"). Without a real why, the team cannot propose simpler solutions. Fix by asking what the user achieves.
- **Fake users.** "As a developer" or "As the product owner, I want…" for work that has no user. Fix by finding the real beneficiary or reclassifying as a task or enabler.
- **Solution specification.** Stories that dictate layouts and endpoints. Fix by stating outcomes and moving design details to linked artifacts.
- **Criteria as UI scripts.** Click-by-click scenarios. Fix by stating behaviour in domain terms.
- **Too many criteria.** A story with a dozen-plus criteria is usually several stories. Fix by splitting by rule or flow.
- **Untestable criteria.** "Fast", "intuitive", "works on all devices". Fix with concrete thresholds and named devices or browsers, or remove.
- **Happy-path-only criteria.** Errors, empties, and permissions discovered in QA. Fix with the edge-case prompts.
- **Epics that never close.** A container that accumulates stories forever. Fix by defining the epic's outcome and closing it when reached; move further ideas to a new item.
- **Backlog hoarding.** Hundreds of detailed stories far beyond the next few iterations. They rot and waste refinement time. Fix by keeping detail only for near-term work; distant items stay coarse.
- **Refinement by one person.** The product person writes everything alone and hands it over. Fix by refining together, even briefly.
- **Done means "code merged".** Stories marked done before they are tested, deployed, or accepted. Fix with an explicit definition of done.

## Quality bar and verification

For each story:

- [ ] A non-team member can tell from the title and description who benefits and how.
- [ ] The benefit ("why") is a real outcome, not a restatement of the feature.
- [ ] It is a vertical slice: when done, someone can demonstrate it end to end.
- [ ] Acceptance criteria are observable, use concrete examples, and cover the important edge and error cases; excluded cases are noted.
- [ ] Two readers would test the criteria the same way.
- [ ] It is small enough to finish within an iteration, with room to spare.
- [ ] Dependencies on other stories or teams are explicit.
- [ ] It follows the team's format and vocabulary, and refers to (not restates) the definition of done.

For a set of stories from one epic:

- [ ] The first slice delivers an end-to-end outcome on its own.
- [ ] Together, the stories cover the epic's goal; gaps are deliberate and recorded.
- [ ] No story is a pure technical layer unless it is a clearly justified enabler.
- [ ] Unknowns that would block estimation have time-boxed spikes with defined outputs.
- [ ] The order reflects value, risk, and genuine dependencies.

A quick self-test: read only the titles of the stories in order. Do they tell the story of a user getting progressively more capable? If they read like a construction schedule, re-slice.

## Working as an assistant

- When asked to write stories from a spec, produce a draft set with clear assumptions and a list of questions for refinement, rather than presenting them as final.
- When asked to "add acceptance criteria", ask (or infer from existing stories) which format the team uses.
- When updating a team's tracker directly, confirm before creating or bulk-editing items, since changes are visible to the whole team and can be noisy to undo.

## Related skills

- `product-requirements` — the problem, goals, and scope stories are derived from.
- `requirements-analysis` — eliciting rules and edge cases from stakeholders.
- `estimate-effort` — sizing and forecasting stories.
- `qa-test-planning` — turning criteria into a test approach.
- `test-driven-development` — using criteria as the starting point for tests.
- `project-management` and `roadmap-and-prioritization` — sequencing and tracking the work.
