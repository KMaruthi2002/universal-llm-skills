---
name: skill-lab-sync
description: >-
  Keep this skills library growing from real daily work: notice the distinct
  kinds of task you did today, compare each against the library's catalog,
  reuse the skill that already covers it, and propose a pull request only for
  what is genuinely new (or a section for what is nearly covered). Use when a
  person asks to "sync skills", "update the skills lab", "add what I learned
  today", at the end of a working session, or whenever you finish a task type
  that no skill in the catalog describes. Not for routing a single request to
  skills (see using-skills) or for the craft of writing a skill well (see
  write-new-skill, which this skill hands off to).
metadata:
  category: meta
  related: using-skills, write-new-skill, manage-context, verify-before-done, pull-request-workflow, git-workflow, report-results
---

# Skill Lab Sync

This library only stays useful if it grows from what people actually do, and only stays trustworthy if it does not fill up with near-duplicates. This skill is the loop that does both: each person's assistant keeps a light record of the kinds of work it did today, compares that record against the shared catalog at the end of the day, points back at the skill that already exists for most of it, and proposes a pull request for the rest.

It is written so that one file is enough. Put this `SKILL.md` in whatever assistant you use and it knows where the library is, how to compare, what the bar for a new skill is, and how to get a proposal into the repository with or without tools.

**Library:** `https://github.com/KMaruthi2002/universal-llm-skills`
**Catalog (machine-readable, public, no login):** `https://raw.githubusercontent.com/KMaruthi2002/universal-llm-skills/main/catalog.json`
**Catalog (readable):** `https://github.com/KMaruthi2002/universal-llm-skills/blob/main/CATALOG.md`

## Scope

Covers: recognising skill-worthy work during a session, keeping the day's record, comparing candidates against the catalog, deciding existing / extend / new, and landing the result as a pull request (or a ready-to-paste file when you have no git access).

Does not cover:

- Choosing skills for the task in front of you — `using-skills`.
- How to write a deep, style-neutral skill — `write-new-skill` and `docs/SKILL_STANDARD.md`. This skill tells you *whether* to write one and *how to ship it*; those tell you how to write it well.
- Git mechanics and PR etiquette in general — `git-workflow`, `pull-request-workflow`.

## Core principles

### 1. Compare before you create

A library of 120 focused skills is more useful than one of 400 overlapping ones, because routing degrades as descriptions start to overlap: the router loads the wrong neighbour, or loads three skills where one would do. So every candidate is checked against the catalog first, and the default verdict when in doubt is **existing**. Creating a skill is the exception that has to earn itself.

### 2. A skill is a kind of task, not a task

"Fixed the login bug" is a task. "Debugging" is a kind of task. Only kinds of task become skills, and only kinds that recur for other people too. The test: would someone else, on a different project, with a different stack, ask for this? If the answer needs your project's name to make sense, it is not a skill.

### 3. Capture judgment, not a diary

What makes a new skill worth a pull request is the expert judgment you exercised: the decision you had to make and why you made it that way, the trap you hit, the check that caught a mistake. A record of what you did without the why produces a thin skill that the validator warns about and reviewers decline. Note the why while it is fresh; it is the first thing you forget.

### 4. Nothing private leaves the session

Skills are public. Client names, internal hostnames, credentials, proprietary numbers, and anything the person would not post publicly stay out — not anonymised, out. If a skill cannot be written without them, it is not a general skill.

### 5. Propose, never push

Every change lands as a pull request against `main`. Continuous integration validates the frontmatter, the links, and the regenerated catalog; a person merges. This is what makes it safe for many assistants to contribute at once: a bad proposal costs a declined PR, not a broken library.

### 6. One skill per pull request

A reviewer can judge one skill in a few minutes and merge it independently. A bundle of five has to wait for the weakest one. Keep proposals separate even when you wrote them on the same day.

## Setup: putting this skill in an assistant

The skill is one file. Where it goes depends on the tool; the behaviour is the same.

| Assistant | How to add it |
|---|---|
| Claude Code, Codex CLI, Cursor, Gemini CLI, other skill-aware harnesses | Copy `skills/skill-lab-sync/` into the tool's skills directory (e.g. `~/.claude/skills/`), or install the whole library as described in the repository README. |
| Claude.ai / Claude Desktop | Zip the `skill-lab-sync` folder and upload it as a Skill, or add this file to a Project's knowledge. |
| ChatGPT, Gemini, other chat assistants | Add the file to a Project / custom GPT / Gem as knowledge, or paste its contents into custom instructions. |
| Anything that can read a URL | Point it at this file's raw URL at the start of a session. |

Nothing else is required. If the assistant can run shell commands and has `git` and the GitHub CLI (`gh`) logged in, it can land proposals itself. If it cannot, it hands the person a finished file and a one-click link (see "Landing a proposal without tools").

## Process

### 1. Track during the session

Keep a short running note — in memory for a chat session, in a scratch file (for example `skills-today.md` outside the project) for an agent with a file system. Add an entry whenever you *finish* a distinct kind of task. Do not add one-line answers, lookups, or the tenth instance of the same kind of work today.

Each entry needs three things, and they can be one line each:

- **candidate name** — lowercase-hyphenated, as a skill would be named (`api-rate-limiting`, not `the rate limit thing`)
- **when to use** — one sentence in the words a user would say
- **what you learned** — the decisions, pitfalls, and checks that made this go well or badly; a few bullets at most, written while they are fresh

An entry without the third part is a placeholder: either fill it in before the end of the day or drop it, because it cannot become a skill.

For agents with persistent memory: the running note belongs in working state, not durable memory. It is consumed by the sync and should not accumulate across days (`manage-context`).

### 2. Trigger the sync

Run the sync when the person asks ("sync skills", "update the skills lab", "add today's skills"), at the end of a working session when they say they are done, or when a task type during the day clearly has no skill in the catalog and the person wants it captured now. Do not run it unprompted in the middle of unrelated work; it is a wrap-up activity.

If the running note is empty, say so in one line and stop. Do not invent candidates to have something to sync.

### 3. Compare against the catalog

**With a shell and a clone of the library:**

```bash
python3 scripts/skill_lab_sync.py compare "name: when to use" "name: when to use" ...
python3 scripts/skill_lab_sync.py compare --file skills-today.md
```

Without a clone, the same script works on the public catalog: `--catalog https://raw.githubusercontent.com/KMaruthi2002/universal-llm-skills/main/catalog.json`.

The script prints a verdict per candidate (`EXISTING`, `EXTEND`, `NEW`) and the three closest skills with scores. The verdict is a floor, not a ruling: scores come from word overlap, so **always read the top match's description** (and its `SKILL.md` if the verdict is `EXTEND`) before deciding. The script cannot be talked into a kinder verdict; that is the point of running it rather than judging by eye.

**Without a shell:** fetch `catalog.json` (or open `CATALOG.md`) and compare by hand using the rules in step 4. Search for the candidate's key nouns in the descriptions, not just the names: a skill called `api-design` covers "rate limiting" because its description says so.

### 4. Decide: existing, extend, or new

| Verdict | Rule | What to do |
|---|---|---|
| **Existing** | A skill's description already says it is for this kind of task, even if it uses different words. | Tell the person which skill to use next time (`skills/<name>/SKILL.md`). Nothing to propose. This is the most common and the best outcome. |
| **Extend** | A skill covers the general task but says nothing about the specific situation you hit, and what you learned would change what a reader of that skill does. | Propose a section in *that* skill (a decision table row, a pitfall, a check). Open its `SKILL.md`, add the material where it belongs, keep its voice, and submit with `propose --extend`. |
| **New** | No skill's description would route this request, and the kind of task recurs for other people. | Write a new skill (step 5), then propose it. |

Tie-breakers, because the middle is where mistakes happen:

- If you can name the existing skill a user *should* have been routed to, it is **existing**, even if the match score is low.
- If your "new" skill would share more than half its principles with an existing one, it is **extend**.
- If the candidate is specific to one product, client, codebase, or team, it is **none of these**: keep it in that project's own documentation.
- If the candidate is a tool's documentation that the model already knows (how to use `git rebase`, the syntax of a library), it is not a skill; skills carry judgment, not reference.

Say the verdict and the reason in one line each. The person can overrule; if they do, note that the override came from them in the PR description.

### 5. Write what is new

Hand off to `write-new-skill` and `docs/SKILL_STANDARD.md`; they are the authority on quality. The non-negotiables, because the validator and reviewers check them:

- Frontmatter with `name` (equals the folder name; lowercase, digits, hyphens), a `description` under 1024 characters that says what the skill does **and when to use it** (include "Use when …"), `metadata.category` from the standard's list, and `metadata.related` naming only skills that exist.
- A body that is deep: typically 250–600 lines, never under 120 non-empty lines. Depth is judgment — thresholds, trade-offs, failure modes — not padding.
- Principles with reasons, a process, decision guidance, how to discover the project's conventions, pitfalls, and verification.
- Style- and model-neutral: no palette, voice, framework, or vendor mandates; tools named only as examples; capabilities described with fallbacks ("if you can run the tests…, otherwise…").
- Nothing private (principle 4). Reread the draft specifically for names, URLs, and numbers that identify a project.

Write the draft to a file outside the clone (or in your scratch space), named `SKILL.md` inside a folder with the skill's name, so `propose` can pick up optional `references/`, `scripts/`, or `examples/` next to it.

For an **extend**, edit a copy of the existing `SKILL.md` instead. Add; do not rewrite. Keep the existing structure and tone, and do not change the description unless the new material changes when the skill should load.

### 6. Land it as a pull request

**With a shell, `git`, and `gh` logged in** (from a clone of the library):

```bash
python3 scripts/skill_lab_sync.py propose path/to/<name>/SKILL.md --dry-run   # validate, build catalog, commit locally
python3 scripts/skill_lab_sync.py propose path/to/<name>/SKILL.md             # push and open the PR
python3 scripts/skill_lab_sync.py propose path/to/<name>/SKILL.md --extend    # for changes to an existing skill
```

The script works in a temporary worktree on a `skill-lab/<name>` branch cut from `origin/main`, runs `scripts/validate.py` and `scripts/build_catalog.py`, commits the skill together with the regenerated `CATALOG.md`, `catalog.json`, and `llms.txt`, pushes (to a fork if you lack write access, creating it if needed), and opens the PR. Your own working tree is untouched. If validation fails, fix the draft and rerun; do not edit the validator.

Run `--dry-run` first. It is cheap and it catches the two common failures — a thin body and a `related` name that does not exist — before anything leaves the machine.

**Without the script but with git:** branch from `main`, add `skills/<name>/SKILL.md`, run the two scripts, commit everything they changed, push, open a PR titled `Add <name> skill` (or `Extend <name> skill`). Never commit to `main`.

### 7. Landing a proposal without tools

A chat assistant with no shell can still finish the job; it just ends with the person clicking once.

1. Output the complete `SKILL.md` in a single code block, exactly as it should be committed.
2. Give this link, with the name filled in:
   `https://github.com/KMaruthi2002/universal-llm-skills/new/main?filename=skills/<name>/SKILL.md`
   Opening it in a browser shows GitHub's new-file editor at the right path. The person pastes the file, chooses "Create a new branch for this commit and start a pull request", and submits.
3. Tell them what happens next: CI validates the file and checks the catalog; the catalog check will fail on a browser-submitted PR because the generated files were not rebuilt, and the maintainer regenerates them on merge. Say this plainly so the red check does not look like their mistake.

For an **extend** without tools, give the edit link instead:
`https://github.com/KMaruthi2002/universal-llm-skills/edit/main/skills/<name>/SKILL.md`, and output only the section to add with a note on where it goes.

### 8. Report

Close the sync with a short, honest summary (`report-results`): each candidate with its verdict and, for existing ones, the skill to use; links to any PRs opened or files handed over; anything you could not verify (for example, the PR's CI result if you did not wait for it). Then clear the running note.

## Discovering context

Before proposing, look at what the library already expects:

- `AGENTS.md` for how skills are used, `docs/SKILL_STANDARD.md` for the format, `skills/write-new-skill/SKILL.md` for the craft.
- Two or three existing skills in the same category, to match depth and tone. The library has a voice — imperative, reasons attached — even though it has no house style.
- Recent merged PRs, if you can see them, for what reviewers asked to change.

And look at the person's own context: if they or their team keep a private skills folder for project-specific material, project-specific candidates go there, not here.

## Pitfalls

- **Harvesting the day into a dozen candidates.** Most days produce zero or one skill-worthy kind of task. If your list has five, you are listing tasks, not kinds.
- **Naming it new to avoid reading the neighbour.** The `EXTEND` verdict exists because reading an existing 400-line skill feels slower than writing a fresh one. It is not; the fresh one gets declined.
- **Writing a skill from one instance.** One experience gives you one path through the task. Skills need the forks. If this is the first time, note it and wait for the second.
- **Leaking context.** A hostname in an example, a client's product in a scenario, a real API key in a snippet. Reread for these on purpose; they do not jump out.
- **Padding to pass the line count.** The validator's minimum is a floor; reviewers read for judgment. Generic encouragement and restated basics lower the skill's value and waste the reader's context.
- **Editing the generated files by hand.** `CATALOG.md`, `catalog.json`, and `llms.txt` are built by `scripts/build_catalog.py`; hand edits are overwritten and fail CI.
- **Pushing to `main`.** Even with write access. The PR is the review; CI is the safety net.
- **Running the sync mid-task.** It interrupts the person's work and the record is incomplete. Wrap up first.

## Quality bar and verification

A sync is done when:

- [ ] Every candidate has a one-line verdict with the reason, and existing ones name the skill to use.
- [ ] Every new or extended skill passed `scripts/validate.py` with no errors (and no warnings you could fix) and `scripts/build_catalog.py` was run — by the script, or by you, or declared not run because there was no shell.
- [ ] Each proposal is its own pull request (or its own file and link), titled `Add <name> skill` or `Extend <name> skill`.
- [ ] The draft was reread once specifically for private information and once for style mandates.
- [ ] The person has the PR links or the file-and-link pairs, and knows what CI will say.
- [ ] The running note is cleared.

If you cannot verify a step, say which one and why; do not report the sync as complete.
