---
name: using-skills
description: >-
  How to route a user request to the right skills in this library, combine
  several skills for one task, resolve conflicts between a skill and a
  project's conventions, and work without a skill when none fits. Use when
  starting a session with this library, when it is unclear which skill
  applies, when a task spans several domains, or when two skills seem to give
  conflicting advice.
metadata:
  category: meta
  related: clarify-requirements, plan-and-decompose, manage-context, verify-before-done, write-new-skill
---

# Using Skills

This library is a set of expert playbooks. The value comes from loading the *right* ones at the *right* moment and applying them with judgment. This skill is the operating manual for doing that well.

## Why routing matters

A skill only helps if it is relevant. Loading the wrong one wastes context and can actively mislead (for example, applying web-app conventions to a CLI tool). Loading none when one exists means re-deriving expertise from scratch and usually missing the non-obvious pitfalls the skill would have warned about. Loading everything drowns the task in noise. The goal is a **small, well-chosen set**.

## The routing process

### 1. Name the deliverable

Before looking at the catalog, state to yourself in one sentence what will exist when the task is done: "a fixed failing test", "a decision on which database to use", "a landing page", "a cleaned dataset and three charts", "a review comment list". The deliverable decides the primary skill far more reliably than the topic words in the request.

Examples of why this matters:

- "Our checkout is slow" could be `performance-optimization` (make the code faster), `web-performance-audit` (measure and diagnose page load), `root-cause-analysis` (explain a regression), or `incident-response` (it is down *right now*). The deliverable tells you which.
- "Make a dashboard for sales" is `dashboard-building` if the deliverable is a working dashboard, `data-analysis` if the user really wants answers, and `ui-design-fundamentals` if they want a mockup.

### 2. Pick a primary skill

Scan `CATALOG.md` by category, then read descriptions. Choose the one skill whose description most directly matches the deliverable. Descriptions are written to say *when* to use the skill — trust the "Use when…" clauses.

### 3. Add supporting skills sparingly

Ask: which parts of this task would an expert in the primary area hand to a specialist, or check against a separate body of knowledge? Those are the supporting skills. Typical patterns:

| Primary | Common supporting skills |
|---|---|
| `full-stack-app-build` | `project-scaffolding`, `api-design`, `database-design`, `frontend-development`, `authentication-and-authorization`, `testing-strategy` |
| `frontend-development` | `ui-design-fundamentals`, `accessible-design`, `layout-and-responsive-design` |
| `dashboard-building` | `data-visualization`, `data-analysis`, `frontend-development` |
| `llm-application-development` | `prompt-engineering`, `rag-systems`, `llm-evaluation`, `ai-safety-and-guardrails` |
| `code-review` | `secure-coding`, `testing-strategy`, `performance-optimization` |
| `presentations` | `data-visualization`, `technical-writing`, `visual-design` |
| `workflow-automation` | `scripting-and-shell`, `api-integrations-and-webhooks`, `error-handling` |

Every skill's frontmatter lists `related` skills; use that list as a shortlist, not an obligation. Two to four skills is normal. More than five usually means the task should be decomposed (see `plan-and-decompose`).

### 4. Load in order of need

Read the primary skill first. Read supporting skills when you reach the part of the work they cover — not all up front. If a skill points to a `references/` file for a specific situation, load it only when you are in that situation.

### 5. Always-on meta skills

Some skills apply to almost every non-trivial task. You do not need to re-read them each time once you know them, but their habits should be constant:

- `clarify-requirements` — when the request is ambiguous in a way that matters.
- `explore-codebase` — before changing any existing project.
- `plan-and-decompose` — when the task has more than a few steps.
- `verify-before-done` — before declaring anything finished.
- `report-results` — when handing work back.

## Precedence: who wins when guidance conflicts

From highest to lowest:

1. **Safety and the law.** Never overridden.
2. **The user's explicit instructions** in this conversation.
3. **The project's existing conventions** — its code style, architecture, design tokens, docs voice, toolchain, tests. Discover these first (`explore-codebase`).
4. **The skill's principles and process.**
5. **Your general defaults.**

Two subtleties:

- **Conventions vs. principles.** If a project's convention violates a skill principle (say, the codebase swallows errors silently), follow the convention for consistency in the code you touch *and* mention the issue to the user. Do not unilaterally rewrite a project's patterns.
- **User instruction vs. quality.** If a user asks for something a skill warns against, do it their way, but say once, briefly, what the risk is. Then drop it.

When two skills disagree (e.g. `mvp-prototyping` says "skip tests for throwaway spikes" and `testing-strategy` says "test critical paths"), the skill closest to the deliverable wins, because it was written with that context in mind.

## When no skill fits

The catalog is broad but not infinite. If nothing matches:

1. Look for the nearest neighbour and borrow its *process* (most tasks share the shape: understand → explore → plan → do → verify).
2. Work from first principles: what would an experienced practitioner care about? What usually goes wrong?
3. Keep the meta habits (clarify, plan, verify, report).
4. If the task type is likely to recur, suggest adding a skill (`write-new-skill`).

Do not stretch an ill-fitting skill to cover the task. A wrong frame is worse than none.

## Using skills without ceremony

Users want results, not a tour of the library. Do not open responses with "I will now use the X skill." Apply the knowledge silently. Mention a skill only when it explains a choice the user may question ("I added an index migration rather than editing the table in place, because rolling back schema changes safely needs a separate step").

## Context budget

Skills are long by design. In a constrained context window:

- Read the primary skill fully, but skim supporting skills for the sections that apply.
- Summarise what you took from a skill into your working notes rather than keeping the whole text in view.
- Drop skills from attention once their part of the work is done.

See `manage-context` for long-running tasks.

## Different environments

This library is read in many ways:

- **Agent harnesses with native skill support** (e.g. tools that discover `skills/*/SKILL.md` automatically) show you skill names and descriptions and load bodies on demand. Routing works the same way: choose by description.
- **File access only** (a cloned repo, a mounted folder, an MCP filesystem server): open `CATALOG.md`, then the chosen `SKILL.md` files.
- **Pasted or uploaded content**: if only some skills were given to you, use those; if you need one that was not provided, say which one would help and ask the user to supply it.
- **No tool access**: you can still follow a skill's process in conversation; where it says "run the tests", tell the user what to run and what to look for.

## Worked routing examples

These show the reasoning, not a lookup table. The same words can route differently depending on the deliverable and context.

**"Build me a habit tracker app."**
Deliverable: a running application. Primary: `full-stack-app-build` (or `mvp-prototyping` if the user signals "quick", "demo", "test the idea"). Supporting, as each phase arrives: `clarify-requirements` (platform? accounts? offline?), `project-scaffolding`, `database-design`, `ui-design-fundamentals`, `testing-strategy`. If the user says "for iPhone", swap the primary to `mobile-app-development`. Do not load `system-design`: a habit tracker has no distributed-systems problem, and loading it invites over-engineering.

**"Why did signups drop last week?"**
Deliverable: an explanation backed by evidence. Primary: `data-analysis`. Supporting: `root-cause-analysis` (structuring candidate causes), `statistical-analysis` (is the drop outside normal variance?), `data-visualization` (one or two charts in the answer). Not `incident-response` unless signups are failing outright, right now.

**"Review my PR."**
Deliverable: review findings. Primary: `code-review`. Supporting only as the diff demands: `secure-coding` if it touches auth, input handling or secrets; `database-migrations` if it changes schema; `concurrency-and-async` if it adds shared state. Read the diff first, then decide which supporting skills apply. Do not pre-load them all.

**"Make our docs better."**
Ambiguous: rewrite the content, restructure the site, or fix the tooling? Primary candidates: `technical-writing`, `documentation-site`, `writing-review-and-editing`. Ask one question, or inspect the docs and propose, before choosing (`clarify-requirements`).

**"Design a landing page for my bakery."**
Deliverable: a page, either a design or built. Primary: `website-and-landing-pages`. Supporting: `visual-design` and `copywriting`, both taking direction from the bakery's existing brand (signage, logo, menu, photos). If there is no brand, ask for references or propose a few distinct directions. Never fall back on a generic default look. Add `seo` for local search and `accessible-design` throughout.

**"Automate sending the weekly report email."**
Deliverable: a scheduled, working automation. Primary: `workflow-automation`. Supporting: `scheduled-jobs`, `api-integrations-and-webhooks`, `document-generation` if the report is a file. Safety: anything that sends messages on someone's behalf gets an explicit confirmation step and a test run to the user alone before it goes to real recipients.

**"Is this claim in my essay true?"**
Primary: `fact-checking`. Supporting: `web-research` if you can browse; otherwise say what you can and cannot verify from your own knowledge, and how confident you are.

## Common routing mistakes

- **Matching on topic words instead of the deliverable.** "Database" appears in requests about design, query tuning, migrations, outages, and analysis. Each needs a different skill.
- **Treating every request as a build.** Many requests want a decision, an explanation, or a review. Producing code when the user wanted advice wastes their time.
- **Loading the platform-agnostic skill when a platform-specific one exists**, or the reverse. "Mobile app" should reach `mobile-app-development`, not just `frontend-development`.
- **Skipping the meta skills on "simple" tasks.** The bugs that come from not reading the code first, or not running the tests at the end, are rarely about difficulty.
- **Never revisiting the choice.** If you discover mid-task that the deliverable is different from what you thought (the "slow page" is really a failing database), re-route.

## Quality check for routing

Before starting the work, you should be able to answer:

- What is the deliverable?
- Which skill is primary, and why that one rather than its neighbour?
- Which supporting skills, if any, and which part of the task does each cover?
- What project conventions have I found that override generic guidance?

If you cannot answer the last one for a task in an existing project, you have not looked yet.
