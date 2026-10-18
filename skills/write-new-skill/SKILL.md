---
name: write-new-skill
description: >-
  Author a new skill, or substantially improve an existing one, for this
  library according to docs/SKILL_STANDARD.md: decide whether a new skill is
  warranted, research the domain, capture real expert judgment rather than
  generic advice, write a description that routes correctly, structure depth
  between SKILL.md and references/, keep it style- and model-neutral, and
  validate it. Use when someone asks to add, write, create, draft, extend,
  split, or review a skill or playbook in this library, or when a recurring
  task type has no matching skill. Not for writing general documentation
  (see technical-writing) or prompts for an application (see
  prompt-engineering).
metadata:
  category: meta
  related: using-skills, technical-writing, prompt-engineering, web-research, literature-review, writing-review-and-editing, clarify-requirements
---

# Write a New Skill

A skill is worth writing only if a capable model that reads it does the task *noticeably better* than one that does not. Models already know the textbook. What they lack is the judgment an experienced practitioner brings: which steps actually matter, where the traps are, what to check before calling it done, and how to adapt to the situation in front of them. This skill is about capturing that judgment in a form that loads at the right time and transfers to cases the author never imagined.

The binding specification is `docs/SKILL_STANDARD.md`. Read it before writing; this skill explains how to meet it well, not what it says.

## Scope

Covers: deciding whether to create a skill, researching its domain, structuring and writing `SKILL.md` and any `references/` files, writing the frontmatter (especially the description), and validating the result.

Does not cover:

- General documentation for humans — see `technical-writing`.
- System prompts or prompt templates for an LLM product — see `prompt-engineering`.
- Using the library to route a task — see `using-skills`.

## Core principles

### 1. Judgment over information

Every sentence should earn its place by changing what the reader would do. "Write tests" changes nothing. "For a bug fix, write the reproducing test first and watch it fail; a test that passes before the fix proves nothing" changes behavior. Prefer thresholds, decision criteria, worked trade-offs, and specific failure modes over definitions and overviews.

### 2. Explain why, so it generalizes

A rule without a reason applies only to the cases the author anticipated. A rule with a reason lets the reader decide when the rule applies, when it doesn't, and what to do in a new case. Give the reason in a clause; it rarely needs more.

### 3. Neutral on style, opinionated on quality

The library serves every project, brand, and codebase. A skill may be firm about what makes work *good* (verify output, handle errors, test edge cases, make text accessible) but must not mandate *taste* (a palette, a font, a framework, a folder layout, a voice). When the domain has real alternatives, present them with the factors that decide between them. Teach the reader to discover and follow the project's existing conventions.

### 4. The description is the router

In most environments, only the frontmatter description is visible when deciding whether to load a skill. If the description does not match how users phrase the need, the skill never loads; if it is too broad, it loads for neighbouring tasks and crowds out the right skill. Treat the description as the most important paragraph you will write.

### 5. Depth is earned, not padded

The standard asks for substantial length because good playbooks are dense with judgment. Length that comes from restating the obvious, generic encouragement, or long lists of things the model already knows lowers quality: it costs context and dilutes the signal. If you cannot fill the length with substance, the scope may be too narrow — merge it into a neighbouring skill.

### 6. Portable across models and harnesses

Readers range from agents with code execution and file access to a chat model with pasted text. Describe capabilities ("if you can run the test suite…") and fallbacks ("…otherwise give the user the exact command and what to look for"). Name tools only as examples. Never assume a specific vendor, product, or agent framework.

## Process

### Step 1: Decide whether a new skill is warranted

Check the catalog (`CATALOG.md` / `catalog.json`) and read the descriptions of likely neighbours.

| Situation | Action |
|---|---|
| An existing skill covers the task but lacks depth or a pitfall | Improve that skill |
| An existing skill covers it, but one sub-area needs much more depth | Add a `references/` file to that skill |
| The task has a distinct deliverable, process, and quality bar from every existing skill | New skill |
| The task is a combination of existing skills | No new skill; possibly mention the combination in `using-skills` or the primary skill |
| The task is a single tool, product, or vendor | Usually no — the library is tool-neutral. Fold tool-specific notes into the general skill as examples |
| The proposed skill would be under ~150 lines of real substance | Probably part of something larger; merge |

A good test of distinctness: can you write a description whose "Use when…" triggers would *not* also fire for an existing skill? If not, you are describing a section, not a skill.

### Step 2: Define the boundary

Before writing, state:

- **The deliverable** — what exists at the end of a task this skill guides.
- **In scope** — the situations and sub-tasks covered.
- **Out of scope** — the neighbouring tasks and which sibling skill owns each.
- **The reader** — a capable generalist model that knows the basics of the domain but not its experienced judgment.

Writing the out-of-scope list first often reveals the real boundaries faster than writing the in-scope one.

### Step 3: Research the domain

Do not write from memory alone, even in familiar areas — memory is strongest on textbook content and weakest on the practical judgment the skill needs. Sources, in rough order of value for judgment:

- **Practitioner material** — postmortems, incident write-ups, engineering blogs, conference talks, "lessons learned", well-regarded books by practitioners. These are where pitfalls and thresholds live.
- **Primary references and standards** — official documentation, specifications, standards bodies' guidance. Use these for correctness of facts and terminology.
- **Review checklists and rubrics** used by teams in the field — they encode what experts check.
- **Disagreements** — find where competent practitioners differ, and the factors behind each side.
- **Your own worked attempts** — try doing the task with and without draft guidance and see where the work goes wrong; those are the pitfalls to name.

If you can browse, use `web-research` and `literature-review` techniques and check that claims are current. If you cannot, say so to whoever commissioned the skill and mark any claims you are unsure of for review. Do not copy text from sources; synthesize. Avoid specific version numbers, prices, or limits that will go stale unless they are essential, and then say they may change.

### Step 4: Extract the expert judgment

From the research, pull out:

- **The handful of core principles** that make most decisions obvious, each with its reason.
- **The process** an expert follows, including where they pause to gather information or ask.
- **The real decision points** and the factors that tip each one.
- **Thresholds and heuristics** — numbers and rules of thumb practitioners actually use, with caveats.
- **Recurring failure modes**, and the early warning sign of each.
- **The quality bar** — what distinguishes good output from plausible-looking output, and the concrete checks that reveal the difference.
- **Safety concerns** — anything involving credentials, production systems, user data, money, legal exposure, or irreversible operations.

A useful exercise: list ten mistakes a competent newcomer would make on this task. If you cannot, you do not yet know the domain well enough to write the skill.

### Step 5: Write the description

Requirements from the standard: ≤ 1024 characters, states *what* the skill does and *when* to use it, including words a user would naturally say. Guidance for doing it well:

- **Lead with the capability**, in concrete verbs: "Design, run, and analyse A/B tests…" rather than "A skill about experiments."
- **Include "Use when…" triggers** that mirror real requests: the deliverables ("a migration plan"), the symptoms ("a test fails", "the page is slow"), and the phrasings ("how should I structure…", "review this…").
- **Include synonyms and adjacent vocabulary** users actually use — "A/B test, split test, experiment, uplift" — because routing is often lexical.
- **Disambiguate from neighbours** with a brief "Not for X (see sibling)". This keeps the skill from loading for adjacent tasks and points the router to the right one.
- **Avoid vague value words** ("best practices", "comprehensive", "powerful") — they match everything and help nothing.
- **Check length** — long enough to be specific, short enough to scan. Most good descriptions are 350–800 characters.

Test it: write five realistic requests that should load the skill and five neighbouring requests that should not. Read only the descriptions of this skill and its neighbours. Would a router choose correctly each time? Revise until it would.

### Step 6: Structure the body

There is no mandatory section list; structure should follow the subject. But every skill must cover the eight elements in the standard: purpose and scope, core principles, process, decision guidance, discovering context, pitfalls, quality bar and verification, and depth on demand. Typical arrangements:

- **Process-centric** (most task skills): scope → principles → step-by-step process with decision tables inline → context discovery → pitfalls → verification.
- **Decision-centric** (choosing among options, e.g. data stores): scope → principles → decision framework and trade-off tables → process for applying it → pitfalls → verification.
- **Review-centric** (audits, critiques): scope → principles → what to examine, in priority order → how to rate and report findings → pitfalls → verification of the review itself.

Use headings to make the file scannable. Use tables for trade-offs and decision criteria, lists for discrete checks and steps, and prose for reasoning. Put the most decision-relevant material early; a reader in a hurry may only read the first half.

### Step 7: Write the body

Writing rules that matter most in practice:

- **Imperative and direct.** "Measure before optimizing," not "It can be valuable to consider measuring."
- **Concrete over abstract.** Every principle should be followed, nearby, by a specific instance.
- **Examples are illustrative, never templates.** Label them as one possibility among many. Do not provide a skeleton to be filled verbatim — it produces uniform output and fights the project's own conventions.
- **No ceremony.** No introductions about how important the topic is, no closing encouragement.
- **Honest uncertainty.** Where experts disagree or evidence is thin, say so and give the deciding factors.
- **Context discovery is explicit.** Tell the reader *where* to look for the project's conventions in this domain (config files, existing artifacts, style guides, prior work) and that those conventions win.
- **Safety is specific.** "Confirm before running the migration against production; take a backup and verify it restores" rather than "be careful".
- **Cross-reference siblings by name** where their territory begins, so the reader can load them.

### Step 8: Decide what goes in references/

Keep `SKILL.md` to what most uses of the skill need. Move material to `references/<topic>.md` when it is:

- Valuable only in a specific situation (a particular platform, a rare sub-task, an advanced technique).
- Long reference data (extended checklists, catalogues of patterns, detailed worked examples).
- Pushing the main file past roughly 600 lines.

Each reference file should be self-contained and linked from the body with a one-line note saying *when* to read it ("Read `references/large-migrations.md` when the table has more than ~10M rows or the migration cannot take a lock"). One to three reference files is typical; many small ones fragment the knowledge. Scripts belong in `scripts/` only if the skill tells the reader exactly when and how to run them, and they must be safe and dependency-light. Examples belong in `examples/` and must be labelled illustrative.

### Step 9: Frontmatter details

- `name` equals the folder name: lowercase letters, digits, hyphens; short and descriptive of the task (prefer the activity or deliverable, e.g. `database-migrations`, over a role or a tool).
- `metadata.category` is one of the categories in the standard; choose by the *kind of work*, not the subject matter.
- `metadata.related` is a comma-separated list of existing skill names: the skills a reader would most plausibly need next or instead. Three to eight is typical. Do not list the skill itself. Every name must exist.

### Step 10: Validate

Run, from the repository root (if you can execute code):

- `python3 scripts/validate.py` — fixes all errors (frontmatter, name/folder mismatch, unknown category, over-long description, broken related links). Treat warnings (thin body, missing "Use when", broken reference links) as things to fix unless there is a clear reason.
- `python3 scripts/build_catalog.py` — regenerates the catalog and index files so the new skill is discoverable.

If you cannot execute code, check those properties by hand and say that validation was not run.

Then review against the quality bar (below). The strongest review is behavioral: take two or three realistic tasks in the domain, attempt them guided only by the skill, and look for places where the guidance was missing, wrong, ambiguous, or ignored. Fix those.

## Worked reasoning: revising a description

Illustration only. A first draft for a hypothetical skill on database indexing:

> "Best practices for database performance. Covers indexes, queries, and optimization."

Problems: "best practices" and "optimization" match nearly any database request; there is no "Use when"; it overlaps with `sql-and-queries`, `database-design`, and `performance-optimization`; it never uses the words users actually say ("slow query", "full table scan", "EXPLAIN").

Revised:

> "Diagnose slow database queries and design indexes that fix them: read query plans, choose index types and column order, weigh write and storage costs, and confirm the improvement with measurements. Use when a query is slow, a plan shows a full scan, a new access pattern needs an index, or someone asks 'should I add an index for this?'. Not for schema design (see database-design) or general SQL authoring (see sql-and-queries)."

What changed: concrete verbs describing the deliverable; natural trigger phrases; explicit neighbours. Then test with requests: "this report query takes 40 seconds" (should fire), "design tables for a booking system" (should route to `database-design`), "write a query to find duplicate emails" (should route to `sql-and-queries`).

## Worked reasoning: from generic advice to judgment

Illustration only. A draft line in a hypothetical caching skill: "Be careful with cache invalidation; it is hard."

True, but it changes nothing. Ask: *what would an experienced engineer actually do differently?* Research and experience suggest:

- Prefer short time-to-live values plus explicit invalidation on write over either alone, because explicit invalidation alone fails silently when a write path is missed, and TTL alone serves stale data for the full TTL.
- Key caches by everything the result depends on (user, locale, permissions, version), because a missing key component serves one user's data to another — a security bug, not just a staleness bug.
- Measure hit rate before and after; a cache below roughly half hit rate often costs more complexity than it saves (a rule of thumb, workload-dependent).

Each line now names a decision, gives the reason, and — where a number appears — marks it as a heuristic. That is the transformation the whole skill should undergo.

## Testing a skill behaviorally

Reading a skill tells you whether it is well written; using it tells you whether it works. Where you can:

1. **Pick two or three realistic tasks** that span the skill's scope — one typical, one edge case, one that should route elsewhere.
2. **Attempt each with only the skill as guidance** (or have another model instance do so, if your environment supports it). Note where the guidance helped, where it was silent, and where it was ignored because it was buried or vague.
3. **Compare against a baseline** attempt without the skill. If the outputs are indistinguishable, the skill is not yet adding judgment.
4. **Check style neutrality** by applying it to two very different contexts (e.g. a tiny script and a large enterprise codebase; a playful brand and a formal one). If the output looks the same in both, the skill is imposing a style.
5. **Revise** and repeat for the weakest areas.

If behavioral testing is not possible, say so when submitting, and review especially critically for vague guidance and missing pitfalls.

## Improving an existing skill

- Read it fully first, and its neighbours, so you do not duplicate or contradict them.
- Prefer targeted additions — a missing pitfall, a decision table, a better reason — over rewrites. Preserve what works.
- When content grows past ~600 lines, move a specialised part to `references/` rather than trimming substance.
- Re-test the description if you change the scope.
- If two skills overlap heavily, propose a merge or a sharper boundary rather than letting both grow.

## Pitfalls and anti-patterns

- **The encyclopedia entry.** Defines concepts the model already knows; light on decisions. Fix: cut definitions; add thresholds, trade-offs, failure modes.
- **The house style.** "Use 8px spacing", "always use framework X", "write in a friendly tone". Fix: replace with principles and how to discover the project's choice.
- **The template in disguise.** A rigid outline to fill in. Fix: describe what good output *contains* and why; offer an illustrative example clearly labelled.
- **Rules without reasons.** Fix: add the why in a clause; drop rules whose reason you cannot articulate.
- **Vague description.** "Helps with data." Never routes, or routes everywhere. Fix: concrete verbs, real triggers, a "Not for…" clause.
- **Overlapping scope.** Two skills both claim the same requests. Fix: sharpen boundaries; cross-reference.
- **Stale specifics.** Version numbers, prices, API details that change. Fix: generalize, or mark as time-sensitive.
- **Tool lock-in.** Instructions that only work with one harness, model, or product. Fix: describe the capability and the fallback.
- **Missing safety.** A skill about deployments or data that never mentions backups, confirmation, or least privilege. Fix: add specific safeguards.
- **Padding to length.** Repetition and generic advice to hit a line count. Fix: if substance runs out, the skill is done — or should be merged.
- **Unverified claims.** Confident thresholds with no basis. Fix: source them, mark them as rules of thumb, or remove them.

## Safety notes

- Skills are instructions that models will follow; a wrong instruction is replicated at scale. Be especially careful with guidance on security, data deletion, financial operations, medical or legal topics, and production systems, and include the safeguards experts use.
- Never include real secrets, credentials, internal hostnames, or personal data in examples.
- Do not include instructions that would have a reader bypass user consent, safety controls, or permissions.
- Do not reproduce copyrighted text from sources; summarize and synthesize in your own words.

## Quality bar and verification

A skill is ready when:

- [ ] A capable model reading only this skill would do the task noticeably better than without it — tested on at least two realistic tasks where possible.
- [ ] The description routes correctly for realistic requests and stays quiet for neighbouring ones; it contains a "Use when…" clause and natural user vocabulary.
- [ ] Scope and out-of-scope are explicit, with sibling skills named.
- [ ] Every principle has a reason; every process step has a purpose.
- [ ] Decision points are presented with the factors that decide them, not single answers.
- [ ] It tells the reader how to discover and honour project conventions.
- [ ] Pitfalls are specific and recognizable; verification steps are concrete.
- [ ] It contains no house style, mandatory template, vendor lock-in, or project-specific assumption.
- [ ] Safety guidance is present wherever the domain touches risk.
- [ ] Length comes from substance; specialised material lives in linked `references/` files with "when to read" notes.
- [ ] `related` names all exist; `python3 scripts/validate.py` passes and the catalog is regenerated.
