# The Skill Standard

This document defines what a skill in this library is, how it is laid out on disk, and the bar every skill must clear. It is written for two audiences: people adding skills, and LLMs that need to understand how to read them.

---

## 1. What a skill is

A skill is a **self-contained body of working knowledge for one kind of task**: how an expert thinks about it, the process they follow, the decisions they make along the way, the mistakes they avoid, and how they check that the result is actually good.

A skill is **not**:

- a fill-in-the-blanks template,
- a house style (a specific color palette, font, tone of voice, folder layout, or framework preference),
- a prompt that produces one fixed output shape,
- a summary of documentation that the model already knows.

The library is deliberately **style-neutral**. Skills teach *principles, process, and judgment* so the model can produce work that fits **whatever project, codebase, brand, or audience it is working in**. When a project has its own conventions, those conventions win; a skill tells the model how to discover and honor them, not how to override them.

## 2. Layout on disk

The layout follows the open **Agent Skills** convention (`skills/<name>/SKILL.md`), which is read natively by Claude Code, Claude.ai, the Claude API, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI and others, and is trivially readable by any LLM that can open files.

```
skills/
  <skill-name>/
    SKILL.md            # required: frontmatter + main body
    references/         # optional: deeper material loaded only when needed
      <topic>.md
    scripts/            # optional: helper scripts the skill tells the model to run
    examples/           # optional: worked examples (illustrative, never prescriptive)
```

The directory is **flat** (one level under `skills/`) on purpose: flat layouts are what every skill-aware tool discovers. Categories live in metadata and in the generated catalog, not in folders.

## 3. Frontmatter

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: debugging
description: >-
  Systematically find and fix the root cause of bugs, crashes, test failures,
  and unexpected behavior in any language or system. Use when something is
  broken, behaves differently than expected, a test fails, or an error message
  appears — before guessing at fixes.
metadata:
  category: development
  related: testing-strategy, root-cause-analysis, observability
---
```

| Field | Rules |
|---|---|
| `name` | Required. Lowercase, digits and hyphens, 1–64 chars. Must equal the folder name. |
| `description` | Required. ≤ 1024 characters. States **what** the skill does **and when to use it**, including the words a user would naturally say. This is the only part a router sees before deciding to load the skill, so it must be specific enough to trigger correctly and to *not* trigger on neighbouring tasks. |
| `metadata.category` | Required. One of the categories in §6. |
| `metadata.related` | Optional. Comma-separated names of related skills. Every name must exist. |

No other top-level keys are needed. (`license` and `allowed-tools` are permitted by the Agent Skills spec but not used here.)

## 4. The body

The body is Markdown. There is **no mandatory section list** — structure follows the subject. But every skill must cover, in whatever arrangement reads best:

1. **Purpose and scope** — what problem this solves, and the boundaries: what it does *not* cover and which sibling skill does.
2. **Core principles** — the handful of ideas that, if understood, make most decisions obvious. Explain *why* each principle holds, not just *what* it is. A model that understands the reason can apply it to cases the skill never anticipated.
3. **Process** — how an expert actually moves through the task, step by step, including where to pause, gather information, or ask the user. Steps should be adaptable, with guidance on when to skip, reorder, or go deeper.
4. **Decision guidance** — the real forks in the road (e.g. "SQL vs. document store", "unit vs. integration test", "modal vs. inline edit") with the factors that decide them. Prefer trade-off tables and "choose X when…" lists over single answers.
5. **Discovering context** — how to find and respect the existing conventions of the project or the user's preferences before producing anything: existing code style, design tokens, docs tone, toolchain, constraints.
6. **Pitfalls and anti-patterns** — the specific, recurring ways this task goes wrong, and how to recognize each one early.
7. **Quality bar and verification** — how to tell good from merely plausible output, and concrete checks to run before declaring the work done.
8. **Depth on demand** — pointers to `references/` files for material that is valuable but not always needed.

### Depth

Skills are meant to be **deep**. A typical `SKILL.md` is 250–600 lines of substantive content. Depth means *more expert judgment*, not more words: concrete heuristics, thresholds, worked reasoning, edge cases, and failure modes. Padding, restating the obvious, and generic encouragement are not depth.

If a skill grows past ~600 lines, move the specialised parts into `references/<topic>.md` and link to them from the body with a one-line note on when to read each file. This keeps the main file fast to load while preserving depth.

### Writing rules

- **Imperative and direct.** "Reproduce the bug before changing code," not "It may be helpful to consider reproducing…".
- **Explain the why.** Every rule that is not self-evident gets a reason.
- **Neutral on tools and taste.** Name tools as examples ("e.g. pytest, Jest, Go's `testing`") rather than mandates. Never prescribe a visual style, voice, or framework unless the skill is literally about that thing — and even then present options.
- **No rigid templates.** You may describe what a good artifact *contains* and why; you may show an illustrative example clearly labelled as one. Do not give a skeleton to be filled in verbatim.
- **Model-agnostic.** Do not assume a particular LLM, vendor, or agent harness. Where tool use matters (running tests, reading files, browsing), describe the capability ("if you can execute code…") and the fallback when it is unavailable.
- **Honest about uncertainty.** Where experts disagree, say so and give the factors.
- **Safe.** Skills that touch credentials, production systems, user data, money, or destructive operations must include the relevant safeguards (confirm before irreversible actions, never log secrets, least privilege, etc.).

## 5. The quality bar

A skill is ready when:

- [ ] A capable model that reads only this skill would do the task noticeably better than without it.
- [ ] The description would route correctly: it fires for the right requests and stays quiet for neighbouring ones.
- [ ] It contains no house style, mandatory template, or project-specific assumption.
- [ ] Every principle has a reason; every process step has a purpose.
- [ ] It names its pitfalls and gives a way to verify the result.
- [ ] `related` links point to skills that exist.
- [ ] `python3 scripts/validate.py` passes.

## 6. Categories

| Category | Covers |
|---|---|
| `meta` | How to work: routing, clarifying, planning, exploring, verifying, reporting, authoring skills. |
| `development` | Writing software: architecture, APIs, frontend, backend, data stores, testing, debugging, refactoring, security. |
| `devops` | Shipping and running software: CI/CD, containers, infrastructure, cloud, observability, incidents, releases. |
| `ai-ml` | Building with models: prompting, LLM apps, RAG, agents, evaluation, ML workflows, MCP. |
| `app-generation` | Producing whole applications end to end: web, mobile, desktop, extensions, games, sites, MVPs. |
| `analysis` | Working with data and evidence: analysis, statistics, visualization, research, modelling, requirements. |
| `quality` | Assurance and review: code review, QA, accessibility, security audits, performance, fact-checking, release readiness. |
| `design` | UI, UX, visual and interaction design, design systems, research, accessibility, prototyping. |
| `automation` | Making machines do the repetitive work: scripts, workflows, scraping, pipelines, integrations, scheduling. |
| `product-and-communication` | Product thinking and written output: specs, stories, roadmaps, docs, slides, writing, project management, teaching. |

## 7. Adding a skill

1. Check `CATALOG.md` — extend an existing skill rather than creating a near-duplicate.
2. Read `skills/write-new-skill/SKILL.md`.
3. Create `skills/<name>/SKILL.md` following this standard.
4. Run `python3 scripts/validate.py` and `python3 scripts/build_catalog.py`.
5. Commit the skill together with the regenerated `CATALOG.md`, `catalog.json` and `llms.txt`.
