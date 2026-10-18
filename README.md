# Universal LLM Skills

A library of **deep, style-neutral skills** that any LLM can load on demand to do expert-level work across software development, DevOps, AI/ML, whole-application generation, data analysis and research, quality assurance and reviews, UI/UX and visual design, automation, and product and communication work.

Connect it once, and whatever you ask, the model picks the relevant playbooks and follows them, applied to *your* project rather than to a generic template.

---

## What makes it different

- **Deep, not shallow.** Each skill holds the expert judgment for its task: principles and *why* they hold, a step-by-step process, decision tables for the real trade-offs, recurring pitfalls, and concrete checks that the work is right. Most are 300–600 lines, with `references/` files for specialist depth.
- **No templates, no house style.** Nothing prescribes a palette, font, voice, framework or file layout. Each skill tells the model how to find and follow *your* conventions (your codebase, design system, brand, docs), and only then how to fill the gaps.
- **Model- and tool-agnostic.** Plain Markdown with a small frontmatter header, in the open Agent Skills layout (`skills/<name>/SKILL.md`). It works with Claude, GPT, Gemini, Llama and others, and with harnesses that discover skills natively as well as with any model that can read files.
- **Routable.** Every skill's description says *when* to use it. [`AGENTS.md`](AGENTS.md) tells a model how to route, [`CATALOG.md`](CATALOG.md) lists everything, and `catalog.json` / `llms.txt` serve tools.

## What's inside

| Category | Examples |
|---|---|
| **Meta** | clarifying requirements, planning, exploring a codebase, verifying work, reporting results, writing new skills |
| **Development** | architecture, system design, APIs, frontend, backend, databases, SQL, debugging, testing, TDD, refactoring, performance, concurrency, security, auth, migrations, CLIs |
| **DevOps** | CI/CD, containers, Kubernetes, infrastructure as code, cloud architecture, observability, incident response, releases |
| **AI / ML** | prompt engineering, LLM apps, RAG, agents and tool use, evaluation, ML workflow, MCP servers, fine-tuning, guardrails |
| **App generation** | full-stack apps, MVPs, websites and landing pages, mobile, desktop, browser extensions, games, scaffolding, chatbots, docs sites |
| **Analysis** | data analysis, statistics, data cleaning, visualization, dashboards, experiments, spreadsheets, web research, literature review, competitive analysis, root-cause analysis, financial models, requirements |
| **Quality** | code review, PR workflow, security audits, architecture review, release readiness, postmortems, accessibility audits, QA planning, E2E testing, web performance, editing, fact-checking, authentic writing |
| **Design** | UI fundamentals, visual design, layout and responsive design, design systems, interaction, motion, accessible design, UX research, IA, UX writing, prototyping, usability evaluation, critique, handoff |
| **Automation** | scripting, workflow automation, scraping, browser automation, ETL, API integrations and webhooks, scheduled jobs, text processing |
| **Product and communication** | PRDs, user stories, roadmaps, project management, business writing, technical writing, presentations, document generation, copywriting, SEO, curriculum design |

The full, current list is in **[CATALOG.md](CATALOG.md)**.

## Connecting it

Short version: put the repo where your model can read it, and point the model at `AGENTS.md`.

| Tool | How |
|---|---|
| **Claude Code** | `/plugin marketplace add KMaruthi2002/universal-llm-skills`, then `/plugin install universal-llm-skills`. Or copy or symlink `skills/*` into `~/.claude/skills/`. |
| **Claude.ai / Claude Desktop** | Upload individual skill folders as Skills (zip each `skills/<name>/` folder). |
| **OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, other agents** | Clone into or alongside your project. They read `AGENTS.md` (pointer files are provided for `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md`), and many discover `skills/*/SKILL.md` natively. |
| **Any LLM with file or MCP access** | Expose the folder through a filesystem or GitHub MCP server and tell the model: *"Read AGENTS.md and use the skills library for this task."* |
| **API / custom apps** | Load `catalog.json`, route with the descriptions, and inject the chosen `SKILL.md` bodies into context. |
| **Plain chat** | Paste `AGENTS.md` plus the one or two relevant `SKILL.md` files. |

Step-by-step instructions for each are in **[docs/CONNECTING.md](docs/CONNECTING.md)**.

## How a model uses it

1. Reads `AGENTS.md` once.
2. Names the deliverable, then picks a primary skill (plus a few supporting ones) from `CATALOG.md`.
3. Loads only those `SKILL.md` files, and their `references/` only when needed.
4. Discovers your project's conventions, which always override generic guidance.
5. Does the work, runs the skill's verification checks, and reports honestly.

## Repository layout

```
AGENTS.md               entry point for any LLM
CATALOG.md              generated index of all skills
catalog.json, llms.txt  generated machine-readable indexes
skills/<name>/SKILL.md  one folder per skill (+ optional references/, scripts/, examples/)
docs/SKILL_STANDARD.md  the format and quality bar
docs/CONNECTING.md      setup for each tool
scripts/                validate.py and build_catalog.py (Python standard library only)
.claude-plugin/         Claude Code plugin and marketplace manifests
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: read the [standard](docs/SKILL_STANDARD.md), extend an existing skill before adding a near-duplicate, then run:

```bash
python3 scripts/validate.py && python3 scripts/build_catalog.py
```

## License

[MIT](LICENSE)
