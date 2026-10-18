---
name: technical-writing
description: >-
  Explain technical subjects clearly to a defined audience: guides, tutorials,
  how-tos, reference pages, conceptual explanations, design docs, runbooks,
  READMEs, internal wikis, knowledge-base articles, and technical blog posts.
  Covers establishing purpose and reader prior knowledge, choosing a document
  type (tutorial, how-to, reference, explanation), structure, examples,
  precision, diagrams, scannability, and matching the destination's existing
  voice. Use when asked to write, rewrite, or restructure documentation or any
  prose whose job is to make a technical thing understood or usable — "write
  docs for", "explain how X works", "document this API/process", "write a
  guide/tutorial/runbook". Not for in-code comments and docstrings
  (code-documentation), building a docs website (documentation-site), editing
  someone else's draft (writing-review-and-editing), or UI microcopy
  (ux-writing).
metadata:
  category: product-and-communication
  related: code-documentation, documentation-site, writing-review-and-editing, ux-writing, information-architecture, business-communication, fact-checking, api-design
---

# Technical Writing

Technical writing exists to move a specific reader from *not able* to *able*: able to understand a concept, complete a task, look up a fact, or make a decision. Every choice — what to include, the order, the level of detail, the examples, the voice — is judged against that one outcome. Elegance, completeness, and cleverness matter only insofar as they serve it.

## Scope

This skill covers prose whose purpose is technical understanding or use: tutorials, how-to guides, reference material, conceptual explanations, design and architecture documents, runbooks and playbooks, READMEs, onboarding guides, troubleshooting articles, release notes, and technical blog posts.

Neighbouring skills own adjacent work:

- `code-documentation` — docstrings, inline comments, generated API docs from source.
- `documentation-site` — the site that hosts docs: tooling, navigation, search, versioning, deployment.
- `information-architecture` — organising a large body of content (taxonomy, navigation) beyond a single document set.
- `writing-review-and-editing` — reviewing and tightening an existing draft, especially someone else's.
- `ux-writing` — interface text: labels, errors, empty states.
- `business-communication` — emails, status updates, memos where the goal is coordination, not explanation.
- `api-design` — designing the API itself; this skill documents it.

## Core principles

### 1. Write for one named reader

"Developers" is not a reader. "A backend developer who knows HTTP and has used one other payments API, integrating ours for the first time, under deadline" is a reader. A named reader tells you what to skip (what they know), what to define (what they don't), what to put first (what they are trying to do), and how much patience they have. Without one, writers default to writing for themselves — which produces docs that are obvious to the author and impenetrable to everyone else (the *curse of knowledge*).

When a document must serve several readers, either pick the primary one and give the others an exit ("If you are already running v2, skip to Migrating"), or split the document. Trying to serve a novice and an expert in the same paragraph serves neither.

### 2. State the purpose before writing a word

Write one sentence: "After reading this, the reader can ___." If the blank contains two unrelated verbs ("install the CLI *and* understand our consistency model"), you probably have two documents. The purpose sentence is the test for every paragraph: does this help the reader get there? If not, cut it or move it.

### 3. Match the document type to the reader's mode

Readers arrive in different modes, and each mode needs a different kind of document. A widely used lens (popularised as the Diátaxis framework) distinguishes four:

| Type | Reader's mode | Reader's question | What it contains | What it must not contain |
|---|---|---|---|---|
| **Tutorial** | Learning, by doing | "Teach me" | A guided, guaranteed-to-work path to a small success; every step specified | Choices, alternatives, deep explanation, edge cases |
| **How-to guide** | Working, has a goal | "How do I do X?" | Steps to a real-world outcome, assuming competence; branches for real variations | Teaching basics, background theory |
| **Reference** | Working, needs a fact | "What exactly is X?" | Complete, accurate, consistently structured descriptions (parameters, options, limits, errors) | Narrative, opinion, tutorials |
| **Explanation** | Studying, wants understanding | "Why / how does this work?" | Concepts, context, design rationale, trade-offs, history | Step-by-step instructions, exhaustive parameter lists |

Use this as a lens, not a bureaucracy. Its value is diagnostic: most bad docs are two types tangled together — a reference page that wanders into a tutorial, a tutorial that stops every step to explain theory, a how-to that tries to cover every option. When a draft feels muddled, ask which mode the reader is in and move the off-mode material to where it belongs, linking between them.

Other common forms map onto these: a **runbook** is a how-to written for stress (see below); a **design doc** is explanation plus a decision record; a **README** is a front door that routes to the others (what it is, why you'd use it, quickstart, where to go next); **troubleshooting** is a how-to indexed by symptom.

### 4. Lead with what the reader needs most

Put the answer, the outcome, or the most common case first. Readers scan the opening to decide whether to keep reading. Inverted-pyramid order (conclusion → key details → background) works for most technical content. For procedures, state the end state and prerequisites before step 1, so the reader can tell if they're in the right place and ready to start.

### 5. Precision beats eloquence

Technical readers act on what you write. Ambiguity causes outages, wasted afternoons, and support tickets.

- Use one term per concept, and never use the same term for two concepts. If the UI says "workspace", the docs do not say "project" for the same thing.
- Give exact values: names, paths, versions, units, defaults, limits. "A few seconds" → "up to 30 seconds (configurable via `timeout`)".
- Distinguish *must*, *should*, and *may*, and use them consistently.
- Name the actor: "The server retries the request" rather than "the request is retried" when it matters who does it.
- State scope and conditions: which versions, platforms, plans, or permissions a statement applies to.

### 6. Show, then tell

An example is often worth more than the explanation it accompanies. Concrete examples anchor abstract descriptions, reveal format details no prose captures, and give the reader something to copy. A good example is minimal (nothing irrelevant), realistic (plausible values, not `foo`/`bar` when the meaning matters), correct (it runs), and complete enough to use (imports, context, expected output).

### 7. Make it scannable, because most readers scan

Readers hunt for the one part they need. Help them: descriptive headings (a heading should tell you what's under it — "Configure retries", not "Advanced"), short paragraphs with the point in the first sentence, numbered lists for sequences, bulleted lists for parallel items, tables for comparisons across the same attributes, and visual distinction for code, commands, and UI labels. Scannability is not decoration; it is the difference between a two-minute lookup and abandoning the page.

### 8. The destination's voice wins

Documentation lives somewhere — a product docs site, an internal wiki, a repository, a support centre, a publication. Each has conventions: person (you/we), tense, formality, heading case, how UI elements are formatted, admonition style, terminology, spelling variant. Matching them matters more than any personal preference because inconsistency across pages makes a docs set feel unreliable and forces readers to re-learn conventions. Discover them first (see below); when none exist, choose plain, direct defaults and apply them consistently.

## Process

### Step 1: Gather the brief

Before drafting, establish:

- **Reader**: role, prior knowledge, what they're trying to do, context (calm learning vs. 3 a.m. incident), language proficiency (many readers are not native speakers of the doc's language).
- **Purpose**: the "after reading, the reader can…" sentence.
- **Type**: tutorial, how-to, reference, explanation, or a defined composite.
- **Destination**: where it will live, existing conventions, format constraints (Markdown dialect, wiki markup, CMS, PDF).
- **Source of truth**: the code, the system, the subject-matter expert, the spec. Technical writing that is not grounded in the real system is fiction.
- **Maintenance**: who will update it, and what change in the system would make it wrong.

If the reader or purpose is genuinely unclear and the guess would change the document substantially, ask. If it is a small doc, state your assumption at the top of your reply and proceed.

### Step 2: Learn the subject well enough to be wrong out loud

You cannot explain what you don't understand. Read the code or spec, run the commands, use the feature, read existing issues and support questions (they reveal where readers actually get stuck). If you can execute things, execute them: run every command you will document and capture real output. If you cannot, mark what you have not verified and say so to the user.

A useful test: can you explain the thing in three sentences to someone outside the team? If not, you aren't ready to write the long version.

### Step 3: Outline before prose

Draft the headings first. Read the headings alone: they should tell the story or form a usable map. Check the order against the reader's journey — for procedures, the order they'll do things; for explanation, from familiar to unfamiliar, from the big picture to the details; for reference, a predictable, consistent order across every entry.

Decide what *not* to include. Every document has a boundary; mark the boundary explicitly and link out ("Authentication is covered in…").

### Step 4: Draft

Draft fast, then fix. While drafting:

- Write the opening last, or rewrite it once the body exists — you'll know what the document actually says.
- Put each procedure step as one action, with the expected result when it isn't obvious ("You should see `Listening on :8080`"). Results let readers detect failure early instead of ten steps later.
- Put conditions before instructions: "If you use a proxy, set `HTTPS_PROXY` first" rather than the reverse, so the reader doesn't act before reading the caveat.
- Put warnings *before* the step they apply to, never after.
- Define a term at first use, or link to its definition.
- Prefer active voice and second person for instructions ("Run…", "You can…") unless the destination's voice differs.

### Step 5: Add examples, diagrams, and reference tables where they earn their place

See the decision sections below.

### Step 6: Verify technically

- Run every command and code sample in a clean environment matching the reader's (fresh install, documented prerequisites only). "Works on my machine" docs fail on the reader's machine because of something you had installed and forgot.
- Check every value (defaults, limits, versions) against the source of truth, not memory.
- Click every link.
- Have a subject-matter expert review for accuracy, if one exists. Ask them specific questions ("Is the default really 30s in v4?") rather than "looks okay?".

### Step 7: Verify for the reader

- **Cold read**: reread as the named reader, pretending you know only what they know. Flag every unexplained term, skipped step, and assumed context.
- **Task test**: if possible, have someone from the target audience (or simulate one carefully) follow the doc to the outcome without help. Every point where they hesitate is a defect.
- **Scan test**: look only at headings, first sentences, and code blocks. Can a reader find what they need?

### Step 8: Edit for length and clarity

Cut words that don't carry meaning: throat-clearing intros ("In this section we will discuss…"), hedges that aren't true uncertainty, repeated explanations, marketing adjectives. Replace vague words with specific ones. Shorter is better *until* it drops something the reader needs; don't compress procedures into ambiguity. See `writing-review-and-editing` for a fuller editing pass.

## Discovering the destination's conventions

Before writing in an existing docs set or repository:

1. **Read three to five neighbouring documents** of the same type. Note person, tense, formality, heading case, list punctuation, how code/commands/UI labels/file paths are formatted, how notes and warnings look, whether pages begin with a summary or prerequisites.
2. **Look for a style guide** — a `STYLE.md`, `CONTRIBUTING.md`, docs README, a linter config (e.g. Vale, markdownlint, textlint rules), or a referenced public guide. Explicit rules override what you inferred from examples.
3. **Collect the terminology**: product names and capitalisation, glossary, the UI's exact labels. Copy UI labels exactly as displayed.
4. **Check structure conventions**: front matter fields, file naming, where images live, how cross-links are written, sidebar or index registration.
5. **Note the format's capabilities**: does the platform render tables, admonitions, tabs, diagrams-as-code (e.g. Mermaid), collapsible sections? Don't use features the destination can't render.

When conventions conflict with this skill's advice (say, the house style uses passive voice throughout), follow the house style in the document and mention the trade-off only if it actively harms comprehension.

## Decision guidance

### How much to explain

| Signal | Lean toward |
|---|---|
| Reader is new to the domain, learning mode | Explain terms, show every step, fewer choices |
| Reader is experienced, working mode | Skip basics, link to fundamentals, show options |
| Mixed audience | Write for the less experienced primary reader; give experts skip-links and a quick-reference summary |
| Stressful context (incident, outage) | Minimal prose, explicit commands, decision points, no theory |
| Reader is not a native speaker | Short sentences, literal language, no idioms, consistent terms; avoid culturally specific references |

### Examples: which kind

- **Minimal snippet** — when demonstrating one call or option. Strip everything else.
- **Complete runnable example** — for a reader's first success (tutorials, quickstarts). Include imports, setup, and expected output.
- **Before/after** — for migrations and configuration changes.
- **Realistic scenario** — for explanation; a concrete story ("a user uploads a 2 GB file on a flaky connection") makes design trade-offs tangible.
- **Counter-example** — when there's a common mistake; show the wrong way, clearly marked, then the right way.

Keep values in examples meaningful (`order_id = "ord_1042"` rather than `x = 1`) and safe: never real credentials, real personal data, or values that are destructive if pasted (e.g. `rm -rf` with a path that could resolve somewhere real). Use clearly fake placeholders and say what to replace.

### Diagrams: when they earn their place

Draw a diagram when the reader needs to grasp **relationships** that prose serialises badly: components and their connections, data or request flow, state transitions, sequences between actors, hierarchies. Don't draw a diagram that just restates a list.

- Choose the diagram type for the question: architecture/box-and-arrow for "what talks to what", sequence for "in what order", state machine for "what states and transitions", flowchart for "what decision leads where".
- Label every arrow with what flows along it; unlabeled arrows are the most common diagram failure.
- Keep one level of abstraction per diagram; make a second diagram for detail.
- Prefer diagrams-as-code (Mermaid, PlantUML, Graphviz, D2, etc.) when the destination supports it — they stay editable and diffable. Use exported images when the platform requires it, and keep the source file alongside.
- Always provide alt text or a prose summary that conveys the same information, for accessibility and for readers who can't see it render.
- Reference the diagram in the text and explain what to notice.

### Tables vs. lists vs. prose

- **Table** when several items share the same attributes (options × type/default/description; plan × limits).
- **Numbered list** for sequential steps.
- **Bulleted list** for unordered, parallel items, three or more.
- **Prose** for reasoning, causation, trade-offs — anywhere "because" and "but" matter. Bulleting an argument destroys the connections between its parts.

### Splitting vs. combining documents

Split when: the purpose sentence has two verbs; sections serve different readers; the page has become a scroll where readers can't find their part; parts change at different rates (stable concepts vs. version-specific steps). Combine when readers routinely bounce between two short pages to complete one task.

## Special forms

### Tutorials

Guarantee success. Pin versions, specify every step, and avoid choices ("use whatever editor you like" is fine; "configure the database of your choice" is not). End with a visible result and a "what next". Keep explanation to one line per step with links for depth — the learner is learning by doing, not by reading.

### How-to guides

Title by goal ("Rotate an API key", not "API keys"). State prerequisites and the end state up front. Assume competence. Handle real-world variation with clearly marked branches ("If you use Kubernetes…"). Include verification ("Confirm the new key works by…") and, where relevant, rollback.

### Reference

Completeness and consistency are the product. Every entry has the same structure in the same order (e.g. name, description, type, default, allowed values, constraints, example, related errors). Generate from source where possible (OpenAPI, CLI help, schema) so it can't drift; hand-write the descriptions that generation can't provide, like *when* you'd use an option. Document errors and limits — they're what readers look up when something goes wrong.

### Explanation and design docs

Explain the *why*: the problem, the constraints, the alternatives considered and why they were rejected, the trade-offs accepted. Use analogies carefully — they help with intuition but break at the edges; say where. For design docs, put the decision and its rationale near the top so reviewers can disagree early. Record what is out of scope and open questions.

### Runbooks

Written for a tired, stressed reader at the worst moment. Lead with symptom → impact → immediate safe actions. Make commands copy-pasteable with placeholders clearly marked. Mark destructive or irreversible steps conspicuously and state their blast radius before the step. Include how to verify each step worked and when to escalate (and to whom, by role rather than by person, since people change). Test it in a drill; untested runbooks fail when needed.

### READMEs

Answer in order: what is this, why would I use it, how do I try it in under five minutes, where do I go for more (docs, contributing, support, license). Keep it short; link out rather than embedding full docs.

### Release notes and changelogs

Organise by what the reader must do: breaking changes and required actions first, then new features, then fixes. Describe user-visible effects, not internal commit messages. Link migration guides.

### Troubleshooting

Index by symptom as the reader experiences it — the exact error message, the observed behaviour — because that's what they'll search for. For each: likely causes (most common first), how to confirm which one, and the fix.

## Writing for global and translated readers

Much technical documentation is read by non-native speakers, run through machine translation, or professionally localised. Writing that survives translation is also clearer for everyone:

- Keep sentences short and one idea each; long sentences with nested clauses translate poorly.
- Avoid idioms, sports and cultural metaphors, puns, and humour that depends on wordplay ("hit it out of the park", "a no-brainer").
- Keep the optional words that clarify structure: "Verify that the file exists" is easier to parse than "Verify the file exists".
- Avoid ambiguous pronouns ("it", "this") when more than one noun could be the referent.
- Don't build sentences around UI strings or variables in ways that break when the string is translated or reordered.
- Use unambiguous date, number, and unit formats (e.g. ISO 8601 dates; state units explicitly).
- Leave text out of images, or provide the text separately, so it can be localised.

## Keeping docs alive

Documentation decays the moment the system changes. Design for maintenance from the start:

- **Single source of truth.** Don't duplicate the same fact (a default value, a supported-versions list) across pages; reference or include it from one place, or generate it from the code.
- **Docs travel with changes.** Where possible, update docs in the same change as the code (docs-as-code, a docs checkbox in the PR template). Docs scheduled "for later" rarely arrive.
- **Test what you can.** Executable examples, doctests, link checkers, and prose linters catch drift automatically.
- **Date or version-scope volatile content**, and record an owner so readers know who to ask and maintainers know who must update it.
- **Retire deliberately.** Delete or clearly mark deprecated pages and redirect old URLs; stale pages ranking in search mislead readers indefinitely.

## Pitfalls

- **The curse of knowledge.** Skipped steps, undefined jargon, "simply" and "just" before things that aren't simple to the reader. Detect it with the cold read and by deleting "simply", "just", "obviously", "easy" — they add nothing and make struggling readers feel stupid.
- **Writing about the system's structure instead of the reader's task.** Docs organised by internal module ("The Scheduler Service") when readers think in goals ("Run a job every night"). Organise reference by system structure if that's how readers look things up; organise guides by task.
- **Mixed modes.** Tutorials that branch into options, reference pages that tell stories. Use the four-type lens to untangle.
- **Untested instructions.** The single most damaging defect. A doc with a wrong command costs every reader time and trust.
- **Stale content.** Docs that describe last year's UI. Note version applicability, tie docs to the release process where possible, and remove or mark obsolete content rather than leaving it to mislead.
- **Wall of text.** Long paragraphs with the key instruction buried in the middle. Front-load points; break up procedures.
- **Over-formatting.** Every sentence bolded, admonition boxes stacked three deep, nested bullets five levels in. When everything is emphasised, nothing is. Reserve warnings for things that cause harm.
- **Inconsistent terminology.** Synonyms used for variety. In technical writing, a different word implies a different thing.
- **Vague quantities and conditions.** "Large files", "recent versions", "may take a while".
- **Screenshots as the only carrier of information.** They go stale, can't be searched, and are inaccessible without alt text. Use them to orient, with text carrying the actual instruction.
- **Burying the prerequisite.** The reader finds out at step 7 they needed admin rights.
- **Marketing voice in docs.** "Our blazing-fast, revolutionary engine" — readers came to learn, and hype reduces trust in the accurate parts.
- **Inventing facts to fill gaps.** If you don't know a default, limit, or behaviour, find out or flag it as unverified. A plausible guess presented as fact is worse than a visible TODO.

## Quality bar

A finished document passes these checks:

- [ ] The purpose and target reader are clear from the first screen.
- [ ] It is one document type, or composite types are clearly separated.
- [ ] Every command and code sample has been run (or is explicitly marked unverified, with a reason given to the user).
- [ ] Every value matches the source of truth; versions and scope are stated where they matter.
- [ ] Every term is defined or linked at first use and used consistently thereafter.
- [ ] Prerequisites appear before the steps that need them; warnings appear before the risky step.
- [ ] Headings alone form a usable map; a reader can find any section by scanning.
- [ ] Diagrams have labelled relationships and a text alternative.
- [ ] It matches the destination's voice, formatting, and terminology.
- [ ] Links resolve; images render; the doc renders correctly on its actual platform.
- [ ] Nothing in it is there for the author rather than the reader.

When handing back, tell the user what you verified, what you could not verify, and any assumptions about the reader you made — they can correct the assumptions faster than they can find the resulting problems.

## Illustrative example: restructuring a muddled page

*Illustrative only — not a template.*

A draft page titled "Webhooks" opens with three paragraphs on event-driven architecture, then lists every event type with its payload, then walks through creating an endpoint, mentions signature verification in a note at the bottom, and ends with a story about why the team chose at-least-once delivery.

Diagnosis with the four-type lens: it mixes explanation (architecture, delivery semantics), reference (event catalogue), and how-to (create endpoint). The security-critical step (signature verification) is buried after the reader has already shipped an endpoint.

Restructure:

1. **How-to: "Receive webhooks"** — prerequisites; create an endpoint; verify signatures (as a required step, before going live, with a warning that skipping it lets anyone forge events); respond with 2xx within the timeout; test with a sample event; expected results at each step.
2. **Reference: "Webhook events"** — one consistently structured entry per event, with payload schema and example, generated from the schema if possible.
3. **Explanation: "How webhook delivery works"** — at-least-once delivery, retries and backoff, why handlers must be idempotent, ordering guarantees (or lack of them).

Each links to the others at the points where a reader would naturally need them ("Handlers may receive the same event twice — see How webhook delivery works"). The same content, reorganised by reader mode, now serves the integrator on deadline and the architect evaluating the design.
