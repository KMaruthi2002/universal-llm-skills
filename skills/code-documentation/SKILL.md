---
name: code-documentation
description: >-
  Write and maintain documentation that lives with code: comments that earn
  their place, docstrings and doc comments, READMEs, API reference, architecture
  and decision records, runbook-style operational notes, and changelogs — and
  keep them true as the code changes, in the project's existing voice and
  tooling. Use when adding or reviewing comments or docstrings, writing or
  fixing a README, documenting a module, public API, or design decision,
  updating a changelog, or when docs have drifted from the code. For a
  standalone docs website use documentation-site; for long-form prose guides
  use technical-writing.
metadata:
  category: development
  related: technical-writing, documentation-site, api-design, code-review, release-management, explore-codebase, refactoring
---

# Code Documentation

Code says what the machine does. Documentation says what a human needs to know that the code cannot tell them: why it is this way, how to use it, what it promises, what will hurt them. The craft is in choosing what to write, where to put it so it is found at the moment of need, and keeping it true.

## Scope

Covers documentation that sits in or beside the source: inline comments, docstrings/doc comments, READMEs, API reference generated from code, architecture notes and decision records, contributor notes, operational notes, and changelogs.

Not covered:

- Building and structuring a full documentation website — see `documentation-site`.
- Tutorials, guides, and long-form explanation as writing craft — see `technical-writing`.
- Designing the API itself — see `api-design`.
- Release notes as a release process — see `release-management` (this skill covers writing the changelog entries).

## Core principles

### 1. Document what the code cannot say

Code expresses *what* and *how*. It cannot express *why this approach*, *why not the obvious alternative*, *what the caller must guarantee*, *what was learned the hard way*, or *what the business rule is*. Spend words there. Why: comments that restate code add reading cost, go stale, and train readers to skip comments — including the important ones.

### 2. Prefer making the code clearer over explaining it

If a comment is needed to explain what a block does, first try a better name, an extracted function, a named constant, or a type. Why: names and types are checked by the compiler and refactoring tools; comments are not. Reserve comments for what clarity in code cannot achieve.

### 3. Put documentation where the reader will be

A reader calling a function looks at its signature and doc comment. A reader setting up the project looks at the README. A reader wondering why the system is shaped this way looks for architecture notes or decision records. A reader upgrading looks at the changelog. Why: documentation that is correct but somewhere else is, in practice, missing.

### 4. Docs that drift are worse than no docs

Wrong documentation actively misleads, and readers cannot tell which parts are stale. Why it matters for process: write less, keep it close to the code it describes (so changes touch both), make it executable where possible (doctests, example code compiled in CI, generated reference), and update it in the same change as the code.

### 5. Match the project's voice and tooling

Every project has an existing doc comment format, README shape, tone, and toolchain. Follow it. Why: consistency is what makes documentation navigable; a section written in a different style or format is harder to read and may break doc generators.

## Discovering context

Before writing:

- **Doc comment format**: which convention does the language and project use? (e.g. JSDoc/TSDoc, Python docstrings in Google, NumPy, or reST/Sphinx style, Javadoc/KDoc, Rust `///` with `# Examples` sections, Go doc comments starting with the identifier name, C# XML docs, Doxygen.) Read several existing ones and copy their structure, tense, and level of detail.
- **Doc generators and checks**: is there a docs build (Sphinx, TypeDoc, rustdoc, godoc, Javadoc, MkDocs plugins), a linter for docstrings, doctests, or link checks in CI? Your changes must pass them.
- **Where things live**: README sections, `docs/` folder, ADR directory (`docs/adr`, `docs/decisions`), `CONTRIBUTING`, `CHANGELOG`, wiki. Do not create a parallel location.
- **Voice**: formal or conversational, second person ("you") or impersonal, sentence-case or title-case headings, spelling variant, use of emoji or none. Mirror what is there.
- **Audience**: internal team, open-source users, API consumers, operators. A library's public docs and an internal service's README need different things.
- **Changelog format**: is it hand-written (e.g. "Keep a Changelog" style), generated from commit messages or changeset files, or produced by release tooling? Do not hand-edit a generated changelog.

If the project has little documentation, follow the language community's mainstream convention and keep it lightweight.

## Comments

### Comments that earn their place

- **Why, not what**: the reason for a non-obvious choice. "Sorted before dedupe because the upstream API returns duplicates non-adjacently."
- **Constraints and invariants**: "Must be called with the lock held." "IDs here are always lowercase; normalized at ingestion."
- **Warnings**: "Do not reorder these fields; the binary format depends on their order." "O(n²) but n ≤ 20 by construction."
- **Workarounds**, with a link: "Works around library bug #1234; remove once we upgrade past 3.2."
- **Business rules and their source**: "Tax-exempt threshold per 2024 regulation §4.2."
- **Non-obvious algorithms**: name the algorithm or cite the reference rather than re-explaining it.
- **Intentional oddities**: an empty catch, a deliberate fall-through, a magic number that is actually a protocol constant — say it is intentional and why, or a future reader will "fix" it.
- **TODO/FIXME with context**: what, why, and ideally an issue link or owner. A bare `TODO: fix this` is noise. Follow the project's TODO convention.

### Comments to avoid or remove

- Restating the code: `i += 1  # increment i`.
- Narrating history: "Changed by Bob to fix the bug" — that is what version control is for.
- Commented-out code: delete it; history keeps it.
- Journal-style or apologetic comments ("hack", "sorry") without actionable information.
- Section-divider banners in short files, if the project does not use them.
- Comments addressed to a reviewer or describing the change ("Now uses the new parser") — they make sense in the PR, not in the code a year later.
- Generated filler: boilerplate docstrings that only repeat the function and parameter names. These are especially common in machine-generated code; strip them.

### Placement and form

- Put the comment immediately above or beside what it explains; a comment far from its subject is soon detached from it by edits.
- Keep comments short. If an explanation needs many paragraphs, it probably belongs in a doc comment, a module-level note, or a design document linked from the code.
- Use complete sentences when the project does; terse fragments when that is the norm.
- When you change code, read the nearby comments and update or delete any that no longer hold. This is the most important maintenance habit.

## Docstrings and doc comments

These document an interface for its callers. They are often rendered into API reference and shown by editors on hover, so they are the most-read documentation in many codebases.

### What to include, by need

- **Summary line**: one sentence on what it does or returns, from the caller's perspective. Many generators show only this line in indexes, so make it stand alone.
- **Parameters**: meaning, units, allowed ranges, and whether they may be null/empty — only what the type does not already say.
- **Return value**: what it represents, and special values (empty list vs. null, sentinel values).
- **Errors/exceptions**: which ones, under what conditions. Callers need this to handle failure; it is often the most valuable part.
- **Side effects**: I/O, mutation of arguments, global state, network calls, caching.
- **Concurrency and lifecycle**: thread-safety, must-call-close, reentrancy, ordering requirements.
- **Performance** when it is surprising or matters (e.g. "makes one network request per item").
- **Examples** for anything non-trivial, especially public APIs. Short, realistic, and ideally executed as tests (doctests, compiled examples).
- **Deprecation**: what to use instead and when it will be removed, using the language's deprecation mechanism where one exists so tools can warn.

### What to leave out

- Restating the type signature in prose in a statically typed language.
- Implementation details callers should not depend on (they become accidental contracts).
- A docstring on every trivial private helper. Document public and non-obvious internal interfaces; let clear private code speak for itself, unless the project's policy or lint rules require full coverage.

### Worked example: improving a doc comment

Illustrative, in neutral pseudocode; use the project's real format.

Before:

```
// getRate gets the rate.
// Params: currency - the currency. date - the date.
// Returns: the rate.
function getRate(currency, date)
```

Everything here is already in the signature. Reading the implementation reveals what a caller actually needs to know, which becomes:

```
// Returns the exchange rate from `currency` to the account's base currency
// as of the end of `date` (UTC). Uses the last published rate if none was
// published that day (e.g. weekends).
//
// `currency` is an ISO 4217 code; matching is case-insensitive.
// Throws UnknownCurrencyError for unsupported codes.
// Throws RateUnavailableError if no rate exists on or before `date`.
//
// Results are cached for one hour; the first call per currency makes a
// network request to the rates provider.
```

The second version tells the caller the units, the time semantics, the fallback behaviour, both failure modes, and the cost. Each of those facts was verified in the code before it was written down.

### Precision matters

Doc comments are contracts. "Returns the user" is ambiguous; "Returns the user with the given ID, or `None` if no such user exists. Raises `PermissionError` if the caller cannot view users." is a contract a caller can program against. When unsure of the actual behaviour, read the code or run it — never document what you assume the code does.

## READMEs

The README is the front door. Its job is to get the right reader to the right next step fast.

A useful README usually answers, in roughly this order of importance (adapt to the project; this is not a template):

1. **What is this?** One or two sentences: what it does and for whom. Possibly a status (experimental, maintained, deprecated).
2. **How do I use it / get it running?** Installation or setup, the minimal working example or the command to start it locally, prerequisites with versions.
3. **How do I do the common things?** Key tasks or a short usage section; link to fuller docs instead of duplicating them.
4. **How do I develop on it?** Running tests, linting, the build — or a link to CONTRIBUTING.
5. **Where do I go next?** Links to docs, API reference, architecture notes, issue tracker, support channel, licence.

Guidance:

- Lead with the most common reader's needs. For a library that is usage; for an internal service it may be "how to run it locally and where it is deployed".
- Every command in a README should work when copy-pasted on a clean machine. Test them. Broken setup instructions are the most common and most damaging README failure.
- Pin versions or state minimums where they matter.
- Keep it short enough to scan; move depth into linked docs. A README that tries to be the whole manual is not maintained.
- Do not include secrets, internal hostnames, or credentials, even as "examples" — use obvious placeholders.
- Badges, logos, and tables of contents are style choices; follow the project.

Sub-READMEs in significant directories (a package in a monorepo, a `scripts/` folder, a `migrations/` folder) help readers who land there directly. Keep them brief and link up to the main one.

## API reference

- Generate it from doc comments or schemas (OpenAPI, GraphQL SDL, protobuf comments) whenever possible, so it cannot drift structurally from the code. Hand-written reference for a changing API will drift.
- Document every public endpoint or symbol: purpose, inputs, outputs, errors, authentication requirements, rate limits, pagination, and examples of real requests and responses.
- Document error responses with the same care as success responses; integrators spend most of their time on failures.
- State stability guarantees and versioning: what is public and stable vs. experimental or internal.
- Keep examples consistent with the current schema; run them in CI if the tooling allows (contract tests, example validation against the schema).
- See `api-design` for the API decisions themselves.

## Architecture notes and decision records

Code shows structure at the level of files and functions. It does not show the system shape or why it was chosen.

### Architecture overview

A short document (often in `docs/` or linked from the README) that explains:

- The main components and how they interact, ideally with a simple diagram (text-based diagram formats such as Mermaid or PlantUML stay diffable and editable next to the code; follow what the project uses).
- Where the important flows go (a request, a job, a data pipeline).
- Key boundaries, external dependencies, and data stores.
- Where to start reading the code for each area.

Keep it at a level of abstraction that changes slowly. Deep detail goes stale; component-level shape lasts.

### Decision records (ADRs)

A decision record captures one significant decision: the context and forces, the options considered, the decision, and its consequences (including the downsides accepted). Why they help: months later, people ask "why on earth did we do this?" and the record answers it, preventing both reversal of good decisions for bad reasons and paralysis over decisions that can safely be revisited.

- Write one when a decision is costly to reverse, contentious, or surprising.
- Keep them short (often under a page) and immutable: supersede an old decision with a new record that links back, rather than editing history.
- Follow the project's existing ADR format and numbering if one exists.
- See `technical-decision-making` for making the decision itself.

## Operational notes

For services and jobs, the people reading docs at 3 a.m. are operators. Useful operational documentation states how to tell whether it is healthy, the common failure modes and what to do about each, how to roll back, where the logs and dashboards are, and who owns it. Keep this near the code or in the team's runbook location; see `incident-response` and `observability`.

## Configuration and environment

Configuration is where undocumented knowledge hurts most, because the code that reads a setting is often far from where it is set.

- Document every setting in one place: name, meaning, type and format, default, allowed values, whether it is required, and which environments set it. Generate the list from a config schema or settings class where possible.
- Provide an example configuration file (e.g. `.env.example`, `config.sample.yaml`) with placeholder values — never real secrets — and keep it in sync with the code that reads settings. A CI check that every setting read in code appears in the example file is cheap and effective.
- Say what happens when a setting is missing or invalid: fail at startup, fall back to a default, or degrade silently. The last is the one people most need to know about.
- Document precedence when settings can come from several sources (flags, environment, files, defaults).

## Documenting tests and examples

- Test names are documentation: a name that states the behaviour and condition ("rejects expired tokens", "rounds half to even for JPY") tells the reader what the system promises. Follow the project's test-naming convention.
- A comment in a test is warranted when the setup encodes a non-obvious scenario (a regression for a specific bug, a tricky ordering) — link the issue.
- Examples directories should contain runnable, maintained programs; build or run them in CI, or they will rot first.

## Choosing the right kind of document

| Reader's question | Best home |
|---|---|
| "What does this line/block do, and why this way?" | Inline comment (or a better name) |
| "How do I call this, and what can go wrong?" | Doc comment on the interface |
| "What is this project and how do I start?" | README |
| "What are all the endpoints/options?" | Generated API or config reference |
| "How do the pieces fit together?" | Architecture overview |
| "Why was it built this way?" | Decision record |
| "How do I contribute, test, release?" | CONTRIBUTING / developer guide |
| "What changed, and must I do anything?" | Changelog / release notes |
| "It is broken in production — what now?" | Runbook / operational notes |
| "How do I accomplish a task end to end?" | Guide or tutorial (see `technical-writing`) |

When a single document tries to answer several of these, split it; each reader is looking for one answer.

## Changelogs

A changelog is written for users of the software, not its developers. It answers: "what changed that I need to know about, and do I need to do anything?"

- Group by version, newest first, with dates. Common categories: added, changed, deprecated, removed, fixed, security. Follow whatever categories the project uses.
- Write entries from the user's perspective: "Requests now time out after 30 s by default (previously no timeout)" rather than "Refactored HTTP client".
- **Call out breaking changes and required actions prominently**, with migration steps.
- Omit internal-only changes (refactors, test changes, CI tweaks) unless the audience is internal developers who want them.
- Link to issues or PRs if the project does.
- If the changelog is generated from commit messages or changeset files, the documentation work happens there: write the commit or changeset entry well, and do not edit the generated output by hand.
- Keep an "Unreleased" section (or equivalent) updated as changes land, rather than reconstructing it at release time from memory.

## Keeping docs true

Documentation decays unless the process resists it.

- **Same-change rule**: when behaviour, configuration, commands, or interfaces change, update the docs in the same commit or PR. Reviewers should treat missing doc updates as incomplete work.
- **Executable docs**: doctests, compiled examples, README commands run in CI, schema-validated examples, link checkers. Anything checked by a machine stays true.
- **Single source of truth**: document each fact once and link to it. Duplicated facts drift apart. Generate where possible (CLI help from the argument parser, config reference from the config schema, API docs from code).
- **Proximity**: the closer the doc is to the code, the more likely it is updated with it. Prefer doc comments over wiki pages for interface details.
- **Ownership and dates**: for docs that cannot be generated (architecture, runbooks), knowing who owns them and when they were last reviewed tells readers how much to trust them.
- **Delete aggressively**: obsolete docs for removed features, abandoned plans, and superseded designs (except decision records, which are kept and marked superseded) should go.

When you find a doc that disagrees with the code, determine which is wrong. Sometimes the code is the bug. Raise it rather than silently "fixing" the doc to match a bug.

## Writing for people and for tools

Documentation is also read by tools and by language models (code assistants, search, retrieval systems). The same qualities help both: precise summary lines, explicit contracts, consistent terminology, examples, and stable headings and anchors. Avoid relying on images alone for essential information; include the information in text too, which also serves accessibility.

## Pitfalls

- **Comment noise**: every line narrated, so the one important warning is invisible.
- **Stale comments** left behind after a change, now describing behaviour the code no longer has.
- **Documenting intention instead of behaviour**: describing what the code should do rather than what it does.
- **Boilerplate docstrings** that repeat the signature and add nothing — common in generated code.
- **README setup instructions that do not work** on a clean machine.
- **A second documentation location** that competes with the existing one.
- **Implementation details in public API docs**, which callers then depend on.
- **Changelogs written for developers** ("refactor X", "bump Y") instead of users.
- **Hand-editing generated docs or changelogs**, which are overwritten at the next build.
- **Secrets or internal URLs in examples.**
- **Style mismatch**: a different docstring format, heading style, or voice from the rest of the project, which can also break doc generators.

## Quality bar and verification

Before calling documentation work done:

- Every claim about behaviour was checked against the code or by running it, not assumed.
- Comments explain why or warn; none merely restate code. Comments near your changes were updated or removed.
- Doc comments on public interfaces state parameters' meaning, return values, errors, and side effects where non-obvious, in the project's format.
- README commands and examples were executed on a clean setup, or flagged as untested if that was impossible.
- The docs build, doctests, linters, and link checks pass.
- New content lives in the existing location and matches the project's voice, format, and terminology.
- Changelog entries describe user-visible impact and highlight breaking changes and required actions.
- No secrets, personal data, or internal-only details leaked into public documentation.

When reporting, say what was documented, what was verified by running it, and any discrepancies found between docs and code that need a decision.
