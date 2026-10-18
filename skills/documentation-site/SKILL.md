---
name: documentation-site
description: >-
  Plan, build and maintain a documentation website for a product, API, library,
  platform or internal system: information architecture (tutorials, how-to
  guides, reference, explanation), choosing a static site generator or hosted
  docs platform, navigation and search, versioning for multiple releases,
  generated API reference, code samples that are tested and actually run,
  docs-as-code workflow with review, previews, link checking and CI, plus
  accessibility, internationalisation and analytics. Use when someone asks to
  create a docs site, developer portal, knowledge base, handbook site, migrate
  docs to a new generator, add versioning or search to docs, or fix docs that
  users cannot navigate or that have drifted from the product.
metadata:
  category: app-generation
  related: technical-writing, code-documentation, information-architecture, api-design, ci-cd-pipelines, seo, accessible-design, website-and-landing-pages, ux-writing, release-management
---

# Documentation Site

A documentation site is a product whose users arrive with a goal, usually mid-task, often from a search engine, and leave as soon as they have what they need — or as soon as they conclude they will not find it. Its quality is measured by how fast the right reader finds the right, correct page. That depends less on the generator and theme than on structure, findability, correctness and the workflow that keeps docs in step with the product.

## Scope

Covers: building or restructuring a docs website; information architecture; generator/platform choice; navigation, search and URLs; versioning; API reference generation; runnable and tested code samples; docs-as-code workflow, CI and previews; accessibility, i18n, analytics and maintenance.

Defers to: `technical-writing` for writing individual pages well, `code-documentation` for in-code comments and docstrings, `information-architecture` for IA method in depth, `api-design` for designing the API being documented, `seo` for search-engine optimisation beyond the basics here, `website-and-landing-pages` for marketing pages that sit next to docs.

## Core principles

1. **Organise by what the reader is trying to do.** Readers come in different modes: learning (tutorials), accomplishing a specific task (how-to guides), looking something up (reference), and understanding why (explanation). This four-way split — popularised as the Diátaxis framework — works because each mode needs a different kind of page; mixing them produces pages that serve no one. Use it as a lens, not a dogma: small projects may need only a quickstart, a few guides and reference.

2. **Most readers arrive on a deep page from search.** Every page must make sense on its own: say what it covers, state prerequisites, link to context. The home page and sidebar are secondary entry points. Why: search engines and in-product links bypass your navigation.

3. **Wrong docs are worse than missing docs.** A missing page sends readers elsewhere; a wrong one costs them hours and their trust in every other page. Prioritise correctness mechanisms — tested samples, generated reference, docs updated in the same change as code — over coverage.

4. **Docs live with the thing they describe.** Docs-as-code: source in plain text (Markdown, MDX, reStructuredText, AsciiDoc) in version control, reviewed like code, built and checked in CI, ideally in the same repository as the product so a pull request changes code and docs together. Why: this is the only workflow that reliably keeps docs current.

5. **Generate what can be generated; write what must be written.** API reference, CLI flags, configuration options and error codes should come from the source of truth (schemas, annotations, code). Concepts, tutorials and guides need humans. Why: generated reference cannot drift; handwritten reference always does.

6. **The generator is an implementation detail.** Pick one that fits the team and content, and keep content portable (standard Markdown, minimal custom components) so you can move later. Why: generators come and go; content is the asset.

7. **Measure findability, not page count.** Search queries with no results, high exit rates on key pages, support tickets that docs should have answered and feedback widgets tell you what to fix.

## Process

### 1. Understand readers and content

- **Who reads?** End users, developers integrating an API, operators, contributors, internal staff. Each group has different vocabulary and goals; many sites serve several and need clear entry points per audience.
- **What do they need to do?** List top tasks from support tickets, community questions, search logs and sales/onboarding feedback.
- **What exists?** Inventory current docs (pages, READMEs, wikis, blog posts, generated references), their owners, freshness and traffic. Mark each: keep, rewrite, merge, delete.
- **What constraints?** Hosting (public, private behind auth, air-gapped), compliance, branding requirements, number of products and versions, languages, who will write (engineers, technical writers, community).

### 2. Discover context

- If a docs site exists: identify the generator and version, the theme/customisations, how navigation is defined (file tree, config, front matter), URL structure, build and deploy pipeline, search provider, versioning mechanism, and the content conventions (style guide, admonition usage, front matter fields). Extend these.
- Follow the organisation's design system and brand for the site's look; do not invent a visual style. Use the generator's theming hooks so updates remain possible.
- Find existing style and terminology guides; follow them for new content (see `technical-writing`).
- Check where product truth lives: OpenAPI/AsyncAPI/GraphQL schemas, protobufs, CLI definitions, config schemas, type definitions — these feed generated reference.

### 3. Design the information architecture

Start from reader tasks, then group:

- **Top level** by audience or product area when there are several; by doc type (Get started / Guides / Reference / Concepts) within each. Keep top-level choices few (roughly 4–7) and named in the readers' words, not internal team names.
- **Getting started** path that takes a new reader from zero to a first success in minutes: prerequisites, install, smallest working example, what next. This is the single most important page set.
- **How-to guides** titled by task ("Rotate API keys", "Deploy behind a proxy"), each self-contained.
- **Reference** organised mirroring the product's structure (endpoints, commands, config keys, components), complete and consistent, generated where possible.
- **Explanation** pages for architecture, concepts, design decisions and trade-offs — linked from guides where the "why" matters.
- **Troubleshooting/FAQ** built from real support issues, searchable by error message text.
- **Changelog / release notes** and **migration guides** for breaking changes.

Then validate: walk through the top ten reader tasks and check each has an obvious path within two or three clicks from the entry points, and an obvious landing page from a plausible search. Card sorting or tree testing (`information-architecture`, `usability-evaluation`) helps for large sites.

### 4. Choose the generator or platform

| Option | Fits | Watch for |
|---|---|---|
| **Static site generator focused on docs** (e.g. Docusaurus, MkDocs with a docs theme, Sphinx, Starlight, VitePress, Hugo with a docs theme, Jekyll-based themes) | Docs-as-code, open source, engineering-heavy teams, full control, free hosting on static hosts | You own upgrades, search integration, theming |
| **Language-ecosystem tooling** (e.g. Sphinx for Python, rustdoc/mdBook for Rust, Javadoc/Dokka for JVM, TypeDoc for TypeScript, godoc/pkgsite for Go) | Library reference tightly bound to code | Narrative docs may need a companion site; combine carefully |
| **Hosted docs platforms** (commercial docs SaaS, knowledge-base tools) | Non-engineering writers, quick start, built-in search/analytics/feedback, API playgrounds | Cost, lock-in, content export format, docs-as-code support varies |
| **API-reference renderers** (OpenAPI/AsyncAPI/GraphQL renderers) | API reference specifically | Usually paired with a narrative docs site |
| **Wiki** | Internal, fast-changing, low-stakes knowledge | Poor review, drift, weak structure; rarely right for product docs |

Decision factors, in rough priority:

1. **Who writes?** Engineers comfortable with Git and Markdown → SSG. Writers or support staff without Git → hosted platform or a CMS with Git sync.
2. **What content types?** Heavy API reference → strong OpenAPI/language integration. Interactive examples → MDX/component support. Multi-format output (PDF, offline) → generators with those builders.
3. **Versioning and i18n needs** — not every generator handles them well; check before committing.
4. **Search** — built-in local search is fine for small sites; large sites benefit from a hosted search index.
5. **Hosting and access control** — public static hosting, or private behind SSO.
6. **Team familiarity and ecosystem** — match the project's language ecosystem if the team will maintain it.
7. **Maintenance health** of the generator — release activity, upgrade path, plugin ecosystem.

Prototype the riskiest requirement (versioning, generated reference, custom component) before migrating content.

### 5. Set up the site

- Scaffold with the generator's official starter, then remove demo content (see `project-scaffolding`).
- Define **URL structure** deliberately: readable, lowercase, hyphenated, stable, reflecting IA not file names that may change. URLs are a public API: links from blogs, Stack Overflow answers, code comments and search results depend on them.
- **Navigation**: sidebar generated from structure or config; breadcrumbs; previous/next for sequential content (tutorials) only; in-page table of contents for long pages.
- **Landing page**: routes readers by goal or audience; gets new users to "Getting started" in one click; surfaces search prominently.
- **Theming**: apply the organisation's brand via the generator's theme configuration; ensure light/dark modes (if offered) both meet contrast requirements; keep reading width comfortable for prose and allow wider areas for tables and code.
- **Code blocks**: syntax highlighting for every language used, copy button, language/OS tabs where readers differ (package managers, operating systems), line highlighting for walkthroughs. Avoid putting shell prompt characters inside copyable text, or make the copy button strip them.
- **Admonitions** (note, warning, danger) used sparingly with consistent meaning; a page full of warnings trains readers to skip them.
- **Page metadata**: title, description, last-updated date (from version control), edit-this-page link to the source file.
- **Feedback**: a "Was this helpful?" control and/or link to file an issue on each page.

### 6. Make search work

- Index titles, headings and body text; boost titles and headings.
- Ensure error messages, CLI flags, config keys and API names are findable verbatim — readers paste them.
- Add synonyms for common alternate terms (e.g. users' words vs your product's terms).
- Scope or facet search by version and product area when there are several.
- Review "no results" queries regularly; each one is a missing page, a missing synonym, or a missing keyword.
- For public docs, basic SEO: unique titles and descriptions, clean URLs, sitemap, canonical URLs across versions (point canonical to the latest version for evergreen content), no accidental `noindex` on production (see `seo`).

### 7. Handle versioning

Version the docs when users run different product versions at the same time and behaviour differs meaningfully between them.

| Strategy | Choose when | Costs |
|---|---|---|
| No versioning (docs = latest) | SaaS with one live version; libraries with strong backward compatibility; early-stage products | Users on old versions may get wrong instructions — call out version requirements inline ("Available from 2.3") |
| Inline version notes | Few differences; long-lived single docs | Notes accumulate and need pruning |
| Snapshot per major version | Clear major releases with breaking changes | Fixes must be backported to snapshots; build time grows |
| Branch per version built separately | Large docs, many versions, separate release processes | More infrastructure; cross-version search and switching need work |

Rules: keep only supported versions published (archive the rest with a clear banner); show a version switcher and an "outdated version" banner linking to the same page in the latest version; keep URLs stable across versions (`/docs/2.x/guide/...` and `/docs/latest/guide/...`), and let the default URL track latest. Version the API reference with the product, generated from the matching schema.

### 8. Generate reference from the source of truth

- **HTTP APIs**: render from the OpenAPI (or equivalent) specification used by the actual service; validate the spec in CI; include request/response examples in the spec itself so they render and can be contract-tested.
- **Libraries**: extract from docstrings/annotations with the ecosystem's tool; enforce docstring presence on public APIs in lint.
- **CLIs**: generate from the command definitions (most CLI frameworks can emit help as Markdown or man pages).
- **Configuration**: generate from the config schema, including types, defaults and allowed values.
- **Error codes**: generate from the error catalogue in code.

Generated pages still need human-written overview pages linking them and explaining how pieces fit.

### 9. Make code samples run

Untested samples rot first. Ways to keep them correct, from lightest to strongest:

- **Extract samples from real files** in an examples directory that is compiled/tested in CI, and include them into pages by reference (most generators support file includes with line ranges or region markers). Why: the page shows exactly the code CI ran.
- **Doctest-style** execution of code blocks embedded in docs, where the ecosystem supports it (e.g. Python doctest, Rust doc tests, Elixir doctests).
- **Snippet testing harnesses** that extract fenced code blocks by annotation and run them in CI.
- **End-to-end tutorial tests**: run the tutorial's commands in a clean environment (container) on a schedule and on release.

Sample quality rules: complete enough to run (imports, setup) or clearly marked as a fragment; realistic but minimal; no real credentials — use obvious placeholders and explain where to get real values; pin versions in install commands where behaviour depends on them; show expected output where it helps readers check themselves.

### 10. Establish the docs-as-code workflow

- Docs changes go through pull requests with review — technical accuracy by an engineer, clarity by a writer or peer.
- Product changes that affect behaviour include docs updates in the same PR, or a linked docs task; a PR template checkbox helps.
- **CI on every PR**: build the site (fail on warnings where the generator supports it), check internal links and anchors, check external links on a schedule (they flake), validate front matter, lint prose (e.g. Vale with the project's style rules) if the team wants it, run sample tests, check spelling with a project dictionary.
- **Preview deployments** per PR so reviewers see rendered output, not raw Markdown.
- **Ownership**: assign owners per section (CODEOWNERS or equivalent) so reviews and freshness checks have someone accountable.
- **Freshness**: track last-reviewed dates for critical pages; review on a cadence and on each major release.
- **Redirects**: whenever a page moves or is deleted, add a redirect. Maintain the redirect map in the repo and test it.

### 11. Accessibility, i18n and performance

- **Accessibility**: semantic headings in order, one H1 per page, descriptive link text, alt text for meaningful images, captions for videos, keyboard-operable navigation and search, visible focus, sufficient contrast in code highlighting themes too, no information conveyed only by colour. Diagrams need text equivalents. See `accessible-design` and `accessibility-audit`.
- **Internationalisation**: decide which content is translated (often getting started and top guides first, reference later or never); use the generator's i18n support; keep the source language canonical with translation status visible; do not machine-translate silently without review; plan how translations stay current when the source changes.
- **Performance**: docs sites should be fast static pages; keep client-side JavaScript light, optimise images, lazy-load heavy embeds (playgrounds, videos). Readers on slow connections and in restrictive networks rely on docs too.

### 12. Measure and maintain

- Analytics (respecting privacy rules and consent): top pages, entry pages, search queries and zero-result queries, exits, feedback votes, time-to-first-success where it can be instrumented (e.g. quickstart completion via product telemetry).
- Correlate with support: tag tickets that docs should have prevented; feed them back as issues.
- Periodically prune: delete or archive pages that are obsolete, merge duplicates, add redirects.

## Content conventions to settle early

Decide these once, write them in a short contributor guide, and enforce what you can in CI. Inconsistency here is what makes large docs sites feel untrustworthy.

- **File naming and location** rules that map predictably to URLs.
- **Front matter fields** required on every page (title, description, owner, doc type, applicable versions) and validated in CI.
- **Heading conventions**: sentence or title case per the style guide; one H1; no skipped levels.
- **Terminology list**: product names, capitalisation, words to avoid; feed it into the prose linter and spell-check dictionary.
- **Code block conventions**: language tags always set; placeholder format (e.g. `<YOUR_API_KEY>` or `YOUR_API_KEY` — pick one); whether commands show prompts; how output is distinguished from input.
- **Admonition meanings**: what qualifies as a warning vs a note.
- **Linking**: relative links to source files (so the generator can validate them) rather than absolute URLs to your own site.
- **Images**: where they live, max size, required alt text, and a policy for screenshots (they go stale fastest — use them only where they add real value).

## Docs consumed by tools and AI assistants

Readers increasingly reach docs through coding assistants, IDE integrations and chat tools that fetch pages. Make the content machine-friendly without degrading it for humans:

- Serve clean, semantic HTML (real headings, lists, tables, code elements) and avoid content that only appears after client-side interaction.
- Consider publishing plain Markdown versions of pages and an index file listing key pages (conventions such as `llms.txt` exist for this); keep them generated from the same source.
- Keep each page self-contained with explicit version and prerequisite statements, since tools often retrieve a single page out of context.
- Make code samples complete and correct — they are copied verbatim by tools even more than by people.

## What each page type must contain

Use these as checks when reviewing pages, not as fill-in templates.

| Type | Reader's question | Must have | Must avoid |
|---|---|---|---|
| Tutorial | "Teach me by doing" | A concrete end result; every step works in order from a clean start; checkpoints showing expected output; minimal choices | Branching options, exhaustive explanation, steps that depend on unstated setup |
| How-to guide | "How do I do X?" | Task-named title; prerequisites; numbered steps; the result and how to verify it; variations at the end | Teaching basics the reader already knows; unrelated tangents |
| Reference | "What exactly is Y?" | Complete, consistent entries (name, type, default, constraints, example); same structure for every entry | Narrative and opinions; gaps "documented elsewhere" |
| Explanation | "Why / how does it work?" | Context, design rationale, trade-offs, diagrams, links to guides | Step-by-step instructions |
| Troubleshooting | "Why is this failing?" | The exact symptom/error text as heading; cause; fix; how to confirm | Vague "check your configuration" advice |
| Release notes / migration | "What changed and what must I do?" | Breaking changes first; before/after examples; deprecation timelines | Marketing copy instead of specifics |

## Migrating docs to a new generator or platform

1. **Inventory and decide** per page: migrate, rewrite, merge, retire. Migration is the cheapest moment to delete outdated content.
2. **Capture all current URLs** (from the sitemap, the old build output, and analytics for top inbound links) before touching anything.
3. **Prototype** the hardest features on the new generator with real content: generated reference, versioning, custom components, search.
4. **Convert mechanically** with a script where formats differ (e.g. reStructuredText → Markdown, wiki markup → Markdown), then fix by hand; review a sample of converted pages for lost content (tables, admonitions, includes, anchors).
5. **Build the redirect map** from every old URL to its new home (or the nearest relevant page — not the home page for everything).
6. **Run both in parallel** briefly if possible; compare search and link-check results.
7. **Cut over**, deploy redirects at the same time, then watch 404 logs and search console data for missed URLs over the following weeks.

## Interactive elements

- **API explorers/playgrounds** help developers try calls quickly. Default them to a sandbox or test environment, label the environment clearly, never prefill real keys, and avoid storing keys in local storage or URLs unless the user opts in.
- **Embedded runnable code** (sandboxed editors, notebooks) is valuable for tutorials; keep a static fallback for readers who block scripts, print, or use assistive technology, and keep the embedded code in the tested examples set.
- **Diagrams**: prefer text-based diagram sources (e.g. Mermaid, PlantUML, D2) in the repo so they are reviewable and updatable; render to accessible images with text descriptions.
- **Videos**: useful for orientation; never the only way to get an instruction (unsearchable, hard to update, inaccessible without captions and transcripts).

## Internal docs, handbooks and runbooks

Internal sites have different failure modes: content sprawl, no owners, and stale pages trusted during incidents.

- Put **access control** at the host (SSO), and keep sensitive material (credentials, personal data) out regardless — link to the secret manager instead.
- Give every page an **owner and last-reviewed date**; surface stale pages automatically.
- **Runbooks** need the highest correctness standard: test them in drills, keep them next to the systems they describe, and update them in postmortems.
- Search across tools matters more internally (docs, tickets, chat); if a unified search exists, make sure the docs site is indexed by it.
- Resist making the internal docs site a dumping ground for meeting notes and drafts; give those a separate space.

## When to pause and ask

Stop and confirm with the user before:

- choosing a hosted platform with ongoing cost or a licence, or replacing a generator the team already maintains;
- changing the URL structure of a live site (even with redirects, it affects search ranking and external links);
- deleting or archiving pages, or unpublishing old versions that customers may still run;
- publishing anything previously internal, or enabling analytics/feedback tools that collect reader data;
- deploying to the production docs domain.

## Decision guidance: same repo or separate docs repo

Choose the **same repository** as the code when docs mostly describe one product/codebase and engineers write them — changes ship together, previews can include code changes, reviewers see both.

Choose a **separate docs repository** when docs span many products/repos, writers own the docs and need their own release cadence, or the site aggregates content from multiple sources (pulling generated reference from each product's build). Mitigate drift with automation: product release pipelines open PRs against the docs repo, or the docs build pulls reference artefacts from product releases.

## Worked example

Request: "We have a REST API and an SDK in two languages, docs are a mix of README files and an old wiki. Build us a proper docs site."

Reasoning:

1. **Readers**: external developers integrating the API; two SDK audiences. Top tasks from tickets: authenticate, make the first call, handle pagination, webhooks, error codes.
2. **IA**: Get started (auth + first request in each SDK and raw HTTP), Guides (pagination, webhooks, idempotency, rate limits, testing), API reference (generated from the service's OpenAPI spec), SDK reference (generated per language), Concepts (data model, environments), Troubleshooting (by error code), Changelog.
3. **Generator**: engineers write docs; need OpenAPI rendering and language tabs → a docs-focused SSG with an OpenAPI plugin, chosen to match the team's ecosystem; prototype the OpenAPI integration first.
4. **Samples**: an `examples/` directory with runnable programs per language, tested in CI against a sandbox; pages include snippets from these files; language tabs remember the reader's choice.
5. **Versioning**: API is backward compatible with dated changes → no snapshots; inline "Available since" notes plus a changelog. SDK major versions → version the SDK reference only.
6. **Workflow**: docs in the API repo; CI builds, checks links, validates the spec, runs examples; preview per PR; redirects from old wiki URLs.
7. **Measure**: search zero-results review monthly; feedback widget; quickstart completion via API telemetry (first successful call within a day of key creation).

## Pitfalls

| Pitfall | Why it hurts | Instead |
|---|---|---|
| IA mirrors the org chart or code layout | Readers don't know your teams or modules | Organise by reader task and doc type |
| Tutorials that are really reference (or vice versa) | Learners drown; experts can't scan | Separate doc types; link between them |
| Theme customisation before content | Weeks on looks, nothing to read | Default theme + brand tokens; content first |
| Handwritten API reference | Drifts from reality within a release | Generate from schema/code |
| Untested code samples | Copy-paste fails; trust lost | Include from tested files; doctests; CI |
| Broken links after reorganisation | Search traffic and external links die | Redirect map; link checks in CI |
| Versioning everything by default | Backport burden, build time, confusing search | Version only when users truly run divergent versions |
| Search that misses error messages | Readers paste errors and find nothing | Index verbatim; dedicated troubleshooting pages |
| Real keys or internal hostnames in examples | Security exposure | Placeholders; scan docs in CI for secrets |
| Docs updated "later" | Later never comes | Same-PR rule; docs check in PR template |
| Massive single pages | Hard to link, scan and search | One task or concept per page; anchors for sections |
| Archived versions indexed above current | Readers follow outdated instructions | Canonicals to latest; outdated banner; deindex unsupported versions |

## Quality bar and verification

- [ ] The site builds from a clean checkout with one documented command, without warnings the team has not accepted.
- [ ] Internal link and anchor check passes; external link check runs on a schedule.
- [ ] Every code sample shown is either included from tested source or tested in place; you ran the getting-started path end to end yourself in a clean environment (or told the user it is unverified and how to verify it).
- [ ] The top ten reader tasks each have an obvious page reachable from navigation and from search.
- [ ] Search finds pages by exact error messages, API names and config keys.
- [ ] Generated reference matches the current product version's schema/code.
- [ ] Every moved or deleted URL redirects.
- [ ] Accessibility basics checked: heading order, keyboard navigation, contrast in both themes and in code blocks, alt text.
- [ ] No secrets, internal URLs or personal data in content or examples.
- [ ] Each section has an owner and the workflow requires docs updates with product changes.
- [ ] If versioned: version switcher works, outdated banners appear, canonical URLs set.

## Safety

- Treat docs repositories as public if the site is public: no credentials, internal hostnames, customer names or screenshots containing personal data. Add secret scanning to docs CI.
- For private docs, put access control at the hosting layer (SSO), not obscurity; search indexes and preview deployments must be protected too — previews are a common leak.
- Analytics and feedback tools collect reader data; follow consent and privacy requirements, and avoid tracking more than you will use.
- Interactive API consoles that use real credentials must make clear which environment they hit and never persist keys in shareable URLs.
