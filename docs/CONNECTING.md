# Connecting the library to your LLM

The library is plain Markdown in the open Agent Skills layout, so there are many ways to connect it. Pick the section for your tool. In every case, the instruction that matters is the same:

> **Read `AGENTS.md`, choose the relevant skills from `CATALOG.md`, and follow them for this task.**


---

## Claude Code

**As a plugin (recommended; stays up to date):**

```
/plugin marketplace add KMaruthi2002/universal-llm-skills
/plugin install universal-llm-skills@universal-llm-skills
```

Claude Code discovers every `skills/*/SKILL.md` and loads each one automatically when its description matches your request.

**As personal skills (available in every project):**

```bash
git clone https://github.com/KMaruthi2002/universal-llm-skills ~/universal-llm-skills
mkdir -p ~/.claude/skills
ln -s ~/universal-llm-skills/skills/* ~/.claude/skills/
```

**For one project only:** symlink or copy the chosen skill folders into `<project>/.claude/skills/`.

## Claude.ai and Claude Desktop

Under Settings → Capabilities → Skills, upload a skill as a zip of its folder:

```bash
cd skills && for d in */; do (cd "$d" && zip -qr "../../dist/${d%/}.zip" .); done
```

(Create `dist/` first.) Upload the skills you use most. Alternatively, add the repo to a Project's knowledge and paste `AGENTS.md` into the project instructions.

## Claude API / Agent SDK

The API supports custom Skills. Upload skill folders through the Skills endpoints and attach them to requests, or route yourself as described under *Custom applications* below. Check the current Anthropic documentation for the exact endpoints and beta headers.

## OpenAI Codex (CLI / IDE / cloud)

Codex reads `AGENTS.md` from the repository root and supports `skills/*/SKILL.md`. Either:

- clone the library **into** your project (e.g. as `vendor/universal-llm-skills`, or as a git submodule), and add one line to your project's own `AGENTS.md`: *"Skills library: see vendor/universal-llm-skills/AGENTS.md"*; or
- link the skills into Codex's user skills directory (see the current Codex docs for the path).

## Cursor

Clone the library into or next to your workspace. Cursor reads `AGENTS.md` and project rules. Add a rule file (`.cursor/rules/skills.mdc`) to your project containing:

```
Use the skills library at <path>/universal-llm-skills. Read its AGENTS.md first,
pick relevant skills from CATALOG.md, and follow them.
```

## GitHub Copilot (agent mode / coding agent)

Copilot reads `.github/copilot-instructions.md` and `AGENTS.md`. Add the library as a submodule or folder in your repo and reference it from your project's `.github/copilot-instructions.md`.

## Gemini CLI

Gemini CLI reads `GEMINI.md` context files (and can be configured to read `AGENTS.md`). This repo ships a `GEMINI.md` that points to `AGENTS.md`. Reference the library path from your project's `GEMINI.md`.

## Any agent with MCP

Expose the folder through any MCP server that can read files:

- a **filesystem MCP server** pointed at your local clone, or
- a **GitHub MCP server** with read access to the repo.

Then tell the model: *"Use the skills library at <path or repo>. Start with AGENTS.md."*

## Custom applications (any model, any vendor)

1. Load `catalog.json` at startup. It lists every skill's `name`, `category`, `description`, `path`, `references` and `related` skills.
2. **Route.** Give the model the user request plus the list of names and descriptions, and ask it to return 1–4 skill names. Embedding similarity over descriptions works as a cheaper first pass.
3. **Inject.** Put `AGENTS.md` (once) and the chosen `SKILL.md` bodies into the system prompt or context.
4. **Expand on demand.** Expose a `read_skill_file(path)` tool so the model can open `references/` files when a skill points to them.

Keep the context lean. Load bodies only for chosen skills, not the whole library.

## Plain chat (no tools)

Paste `AGENTS.md`, then the one or two `SKILL.md` files relevant to your task, then your request. `CATALOG.md` helps you choose which to paste.

---

## Keeping it updated

- Plugin installs: `/plugin marketplace update universal-llm-skills`.
- Clones and submodules: `git pull` (or `git submodule update --remote`).
- If you customize skills for your organization, fork the repo and keep your changes in the fork.
