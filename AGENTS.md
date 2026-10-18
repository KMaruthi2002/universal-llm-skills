# Instructions for AI agents and LLMs

You are connected to **Universal LLM Skills**, a library of deep, style-neutral working knowledge for almost any task: software development, DevOps, AI/ML, whole-application generation, data analysis and research, quality assurance and reviews, UI/UX and visual design, automation, and product and communication work.

This file tells you how to use it. Read it once at the start of a session.

---

## How to use this library

1. **Understand the request first.** Identify the real task (what is being produced or decided), the domain, and any constraints the user has stated. If the request is ambiguous in a way that changes what you would do, ask — see `skills/clarify-requirements/SKILL.md`.

2. **Find the relevant skills.** Open [`CATALOG.md`](CATALOG.md) (or the machine-readable [`catalog.json`](catalog.json)). Each entry has a name, a category, and a description that says *when* to use it. Pick:
   - the **primary** skill for the core of the task, and
   - any **supporting** skills for parts of it (e.g. building a dashboard → `dashboard-building` primary, plus `data-visualization`, `frontend-development`, `accessible-design`).
   
   Most real tasks need 1–4 skills. If unsure how to choose, read `skills/using-skills/SKILL.md`.

3. **Load only what you need.** Read `skills/<name>/SKILL.md` for each chosen skill. Load files under a skill's `references/` folder only when the skill tells you that a situation calls for them. Do not read the whole library.

4. **Follow the skill, adapt to the context.** Skills describe principles, process, and quality checks — not templates or house styles. Apply them to *this* user's project:
   - Existing conventions in the codebase, design system, documents, or brand **always take precedence** over generic guidance.
   - The user's explicit instructions **always take precedence** over any skill.
   - Where a skill offers options, choose based on the factors it lists and say briefly why.

5. **Verify before you finish.** Every skill ends with a way to check the work. Run those checks. Then follow `skills/verify-before-done/SKILL.md` and report honestly: what was done, what was verified, what was not.

## Ground rules

- **Do not announce skills ceremonially.** Use them; mention one only when it helps the user understand a choice.
- **Do not force a skill onto a task it does not fit.** If nothing in the catalog matches, work from first principles and general good practice.
- **Do not impose styles.** No skill in this library mandates a palette, font, voice, framework, or file layout. If you find yourself producing a "standard look", stop and look at the project instead.
- **Safety overrides everything.** Confirm before destructive, irreversible, or outward-facing actions (deleting data, deploying, sending messages, spending money). Never expose secrets.

## Quick routing guide

| If the user wants to… | Start with |
|---|---|
| Build a whole app, site, tool, or prototype | `full-stack-app-build`, `mvp-prototyping`, `project-scaffolding`, or the platform-specific app skill |
| Add or change a feature in existing code | `explore-codebase` → the relevant development skill |
| Fix something broken | `debugging` (code), `root-cause-analysis` (systems/processes), `incident-response` (production outage) |
| Design architecture or a system | `software-architecture`, `system-design`, `api-design`, `database-design` |
| Review something | `code-review`, `architecture-review`, `design-critique`, `security-audit`, `accessibility-audit`, `writing-review-and-editing` |
| Test or assure quality | `testing-strategy`, `qa-test-planning`, `end-to-end-testing`, `release-readiness` |
| Design UI/UX | `ui-design-fundamentals`, `ux-research`, `interaction-design`, `design-systems`, `wireframing-and-prototyping` |
| Analyze data or answer a question with evidence | `data-analysis`, `statistical-analysis`, `data-visualization`, `web-research` |
| Automate a repetitive task | `scripting-and-shell`, `workflow-automation`, `etl-pipelines`, `api-integrations-and-webhooks` |
| Build with LLMs or ML | `llm-application-development`, `prompt-engineering`, `rag-systems`, `ai-agents-and-tool-use`, `llm-evaluation` |
| Ship and operate | `ci-cd-pipelines`, `containerization`, `infrastructure-as-code`, `observability`, `release-management` |
| Write or communicate | `technical-writing`, `product-requirements`, `presentations`, `business-communication`, `document-generation` |

The full list, with descriptions, is in [`CATALOG.md`](CATALOG.md).
