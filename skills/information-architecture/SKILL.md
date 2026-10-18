---
name: information-architecture
description: >-
  Organize and label content and features so people can find, understand,
  and use them: content inventories and audits, mental models, taxonomies and
  metadata, labeling, global/local/contextual navigation, search versus
  browse, card sorting and tree testing, findability metrics, and scaling an
  IA as a product or site grows. Use when designing or restructuring a site
  map, app navigation, menu, settings area, help center, documentation
  structure, product catalog, or content taxonomy, or when users say they
  "can't find" things. For visual page layout use layout-and-responsive-design;
  for the wording of individual labels and messages use ux-writing.
metadata:
  category: design
  related: ux-research, ux-writing, usability-evaluation, interaction-design, wireframing-and-prototyping, documentation-site, website-and-landing-pages, seo, layout-and-responsive-design, design-systems, api-design, accessible-design
---

# Information Architecture

Information architecture (IA) is the structural design of an information space: how content and functionality are grouped, named, related, and reached. It sits beneath visual design and interaction design. A beautiful interface on a confused structure stays confusing; a sound structure survives many redesigns.

This skill applies to websites, apps, SaaS products, intranets, documentation, e-commerce catalogs, settings screens, file systems, and even chat or voice products where the "navigation" is a set of intents. It is about the **structure and the names**, tested against how real people think.

**Out of scope, handled elsewhere:**

- Page-level layout, grids and breakpoints: `layout-and-responsive-design`.
- Microcopy and messages beyond navigation labels: `ux-writing`.
- General user research methods: `ux-research` (card sorting and tree testing are covered here in depth because they are IA-specific).
- Documentation site tooling and docs-specific structure: `documentation-site`.
- Search-engine optimization of public pages: `seo` (though good IA helps it).

## Core principles

**1. Structure follows users' mental models, not the org chart.** People look for things using their own concepts of how the domain is organized. Internal structures (departments, teams, product lines, database tables) leak into navigation constantly because they are what the builders know. Users do not care that "Billing" and "Invoices" are owned by different teams.

**2. Findability is the job.** An item that cannot be found does not exist for the user. Every structural decision is ultimately judged by: can the intended people find what they need, quickly, with confidence that they are in the right place?

**3. Labels carry most of the weight.** In a navigation menu, the label is the only information the user has to predict what is behind it. A great hierarchy with vague labels fails; a mediocre hierarchy with clear labels often works. Test labels as hard as structure.

**4. People forage by scent.** Users follow cues ("information scent") that suggest they are getting closer to their goal. Strong scent: labels and previews that clearly predict content. Weak scent: clever names, jargon, generic buckets ("Resources", "More", "Solutions"). When scent fades, people back out, search, or give up.

**5. Breadth usually beats depth, up to a point.** Fewer levels with more options per level tend to outperform deep trees, because every extra level is another guess that can go wrong. But a level with too many undifferentiated options is hard to scan. Grouping and clear labels let a level hold more items comfortably; there is no magic number.

**6. Support multiple ways in.** People find things by browsing, searching, following related links, filtering, and arriving from outside (search engines, shared links, notifications). A good IA serves all of these and does not force a single path.

**7. Design for growth and change.** Content grows and products add features. A structure that works for 30 items may collapse at 300. Choose organizing schemes and naming conventions that can absorb new items without reshuffling everything.

**8. Every item has one home, many routes.** Each piece of content should have a single canonical location (avoiding duplicates that drift apart), while cross-links, tags, and search can surface it in other contexts.

## Key concepts

| Concept | What it is | Why it matters |
|---|---|---|
| Organization scheme | The principle used to group: by topic, task, audience, alphabet, time, location, format | Wrong scheme makes every label feel arbitrary |
| Organization structure | The shape: hierarchy, hub-and-spoke, faceted, sequential, network | Determines how people move between items |
| Taxonomy | A controlled set of categories, often hierarchical | Consistent classification across content and teams |
| Metadata / facets | Attributes of items (type, date, author, size, status) | Enables filtering, sorting, and alternate views |
| Controlled vocabulary | Preferred terms plus synonyms mapped to them | Makes search and tagging consistent |
| Navigation systems | Global, local, contextual, supplementary (site map, index), utility | Different jobs; each needs a clear purpose |
| Labeling system | The set of names used for links, headings, menu items | Consistency builds predictability |
| Search system | Query handling, results, filters, zero-results recovery | The fallback when browse fails, and the primary path for many |

### Organization schemes

- **Exact schemes** (alphabetical, chronological, geographical) work when users know exactly what they want and how it is named: a list of countries, an archive by date, a staff directory.
- **Ambiguous schemes** (topical, task-based, audience-based) work when users explore or do not know the exact name. They are harder to design and need testing.
- **Task-based** groupings ("Pay a bill", "Report a problem") suit products and services where users arrive with a job to do. They age badly if tasks change, and can become verbose.
- **Audience-based** groupings ("For students", "For businesses") help when audiences need genuinely different content, but fail when people do not identify with one audience or need content from several. Use sparingly.
- **Hybrid** schemes are common and fine at different levels, but mixing schemes within one menu ("Products", "For Developers", "Pricing", "2024 Report") weakens scent because users cannot predict what kind of thing each label is.

### Organization structures

- **Hierarchy**: the default for most products. Easy to understand; forces each item into one parent.
- **Faceted**: items have multiple attributes; users combine filters. Best for large, homogeneous collections (products, documents, listings, datasets).
- **Hub-and-spoke**: a central screen from which users go into a task and come back. Common in mobile apps and dashboards.
- **Sequential**: a linear flow (wizard, course, checkout). Use when order matters.
- **Network / hypertext**: items linked by relationships. Powerful for exploration (wikis, knowledge bases) but disorienting without a backbone hierarchy.

## Process

### 1. Understand the content and functionality

- **Inventory**: list everything that exists or is planned: pages, features, settings, document types, product categories. For large sites, crawl or export; for apps, walk every screen. Record title, location, type, owner, last updated, traffic if available.
- **Audit**: assess quality and relevance. Mark items to keep, merge, rewrite, archive, or delete. Restructuring is the best moment to remove content; moving clutter into a new structure just makes a new cluttered structure.
- **Find the objects**: identify the core objects users work with (e.g. projects, invoices, customers, articles) and their relationships. Object-oriented IA (structuring around nouns users recognize, with actions attached) often yields clearer navigation than structuring around verbs or features.

### 2. Understand the users

- Who uses the space, what are their top tasks, and what vocabulary do they use? Pull from research, search logs (the words people type are unfiltered mental-model data), support tickets, and analytics of current navigation paths.
- Identify **top tasks**: the small set of tasks that account for most visits. Structure should make these effortless even if it makes rare tasks slightly harder. A top-task survey (users pick their top few from a long list) is a fast way to rank them.
- Distinguish user groups whose mental models differ substantially (e.g. novices vs. experts, buyers vs. operators), and decide whether one structure can serve them or whether you need entry points per group.

### 3. Explore mental models with card sorting

See `references/card-sorting-and-tree-testing.md` for running and analysing studies.

- **Open card sort**: participants group items and name the groups. Reveals how people cluster and what they call things. Use early.
- **Closed card sort**: participants sort items into predefined categories. Tests whether a proposed set of categories is understood. Use to compare options.
- **Hybrid**: predefined categories, but participants may add their own.

Card sort results are input, not output. They show patterns and vocabulary; you still have to design a structure that also accounts for business needs, growth, and items people disagree about.

### 4. Draft the structure

- Start from top tasks and core objects, then place everything else.
- Sketch 2–3 alternative structures that use different organization schemes. Comparing alternatives exposes assumptions; a single draft tends to be defended rather than evaluated.
- For each top-level category, write a one-sentence scope definition ("Everything about money owed to you: invoices, payments received, reminders"). If you cannot write it, the category is incoherent.
- Decide where ambiguous items live, and plan cross-links for them. Items that half the card sort placed in A and half in B need one home and a link from the other.
- Keep the top level small enough to scan and distinct enough that labels do not overlap in meaning.

Represent the structure in whatever format the team uses: an indented outline, a spreadsheet, a site map diagram, a tree in a design tool. Outlines and spreadsheets are easiest to edit and to feed into tree tests.

### 5. Label

- Use the words users use (from card sorts, search logs, interviews), not internal names. If the product has a branded feature name, pair it with a descriptive word or put it in a group whose label is descriptive.
- Make labels mutually exclusive in meaning. "Support", "Help", and "Resources" side by side guarantees guessing.
- Front-load the word users scan for. People read the first word or two of each item in a list. If they scan for objects, start with the object ("Invoices", "Invoice templates"); if they scan for actions, start with the verb. Avoid lists where every item begins with the same word ("Manage users", "Manage roles", "Manage teams"), because the repeated word carries no information and pushes the distinguishing one out of view.
- Let the hierarchy do some work: inside a "Billing" section, "History" and "Payment method" are enough; repeating "Billing" in each child adds noise.
- Be specific: "Pricing" beats "Plans & Offers & More". Avoid catch-alls ("Other", "Miscellaneous", "More"); they become dumping grounds.
- Keep grammatical form consistent within a set (all nouns, or all verb phrases).
- Check labels with `ux-writing` for terminology consistency, and with the product's established vocabulary.

### 6. Validate with tree testing

Tree testing gives participants the text-only hierarchy and tasks ("Where would you go to change the card you pay with?") and records where they click. It isolates structure and labels from visual design.

- Write tasks from top tasks and from risky areas (ambiguous items, renamed sections).
- Phrase tasks without using the target label's words, otherwise you test word-matching.
- Measure success (ended in the right place), directness (got there without backtracking), first click (where they went first), and time.
- Iterate: change labels and placement, retest. Two or three rounds are typical for a significant restructure.

### 7. Design the navigation systems

Navigation renders the IA; it is not the IA itself.

- **Global navigation**: the persistent top-level. Keep it stable across the product; changing it per page destroys orientation.
- **Local navigation**: within a section. Shows siblings and children.
- **Contextual navigation**: links embedded in content ("Related", inline links, next steps). Where scent is often strongest.
- **Breadcrumbs**: show location in a hierarchy; useful for deep structures and for users arriving from search.
- **Utility navigation**: account, settings, help, language. Conventionally placed where users expect it on the platform.
- **Supplementary**: site map, A–Z index, guided tours. Useful safety nets for large spaces.

Mobile and small screens constrain global navigation; prioritize top tasks visibly and accept that secondary items move into a menu. Hiding everything behind a menu icon reduces discovery of anything not already known. Follow platform conventions for the product's platform (tab bars, side drawers, top nav) unless research shows a reason not to; convention is a form of findability.

### 8. Design search and filtering

When to lean on search vs. browse:

| Lean on browse when… | Lean on search when… |
|---|---|
| The collection is small or moderate | The collection is large or growing fast |
| Users explore or compare | Users know what they want and its name |
| Items are well-categorized | Items are heterogeneous or cross-cutting |
| Users are novices learning the domain | Users are experts or returning |
| Scope must be communicated (what exists) | Speed to a known item matters most |

Most real products need both. Search design essentials:

- Handle synonyms, misspellings, plurals, and abbreviations; build the synonym list from search logs and the controlled vocabulary.
- Show the scope of what is being searched and allow narrowing (facets, filters, content types).
- Make zero-results useful: suggest corrections, related categories, broader queries, or a contact path.
- Review search logs regularly: top queries (what people want), zero-result queries (missing content or vocabulary gaps), and queries for things that exist in navigation (a sign navigation scent is failing).

For faceted collections: choose facets users actually use to decide (from research and query data), show counts, keep facet labels consistent with the vocabulary, and avoid facets that produce empty results.

### 8a. Model content and metadata

Navigation is only as good as the information about the items it organizes. For any collection larger than a handful of items:

- **Define content types** (e.g. article, how-to guide, product, release note, policy) with the fields each needs. Types decide which templates, facets and search filters are possible.
- **Choose metadata deliberately.** Every field must serve a user-facing purpose (filtering, sorting, display, related-content rules) or a governance purpose (owner, review date). Fields nobody fills in reliably are worse than none, because they make filters lie.
- **Build a controlled vocabulary** for fields that classify: preferred term, definition, synonyms, and broader/narrower terms. Map synonyms to the preferred term for search ("bill", "invoice", "statement" → Invoice).
- **Categories vs. tags.** Categories are few, controlled, mutually exclusive and structural; tags are many, overlapping, and descriptive. Use categories for primary navigation and tags for cross-cutting discovery, and govern tags too — at least merge duplicates and prune rarely used ones periodically.
- **Make metadata cheap to apply.** Defaults, pick lists, and auto-suggestion beat free text. If authors must classify by hand with no help, quality will decay.

### 9. Plan governance and scale

- Define who can create new top-level categories, add tags, and rename things. Without governance, taxonomies sprawl and synonyms multiply.
- Document the IA: category scope definitions, labeling rules, the controlled vocabulary, where new content types go.
- Plan for growth: will each category comfortably absorb 3× more items? If a category is expected to grow faster than others, give it room (its own section, facets) before it overflows.
- Retire content: assign ownership and review dates so outdated pages do not accumulate.
- When restructuring an existing public site, plan redirects for every changed URL to preserve users' bookmarks and search-engine standing.

## Discovering context

Before proposing structure for an existing product:

- **Read the current navigation and site map**, and the data model (routes, database entities, content types). The data model shows the objects; the navigation shows how they are exposed.
- **Pull analytics**: most-visited pages, entry pages, common paths, where people search from, exit points.
- **Read search logs** and support tickets for "where is…", "how do I find…".
- **Check the existing vocabulary**: product glossary, design-system copy guidelines, marketing terms, any localization glossary. New labels should fit it or deliberately replace it, with a migration plan.
- **Learn the constraints**: platform conventions (mobile tab bar limits, desktop menus), CMS or routing limitations, SEO and URL commitments, legal requirements for where certain content must appear.
- **Ask about upcoming features** so the structure has room for them.

## Measuring findability

Pick measures before changing anything, so you can compare before and after.

- **Tree-test success, directness, first click** for the structure itself (see the reference file).
- **Task success in usability tests** for the structure as rendered (see `usability-evaluation`).
- **Navigation analytics**: path length to key pages, pogo-sticking (going into a section and immediately back out), use of the back button, menu-open-then-close without selection.
- **Search signals**: search rate from pages where navigation should suffice, zero-result rate, query refinement rate, searches for items that exist in navigation.
- **Support signals**: volume of "where is" and "how do I find" tickets; tags that cluster around a section.

No single metric is decisive. An increase in search usage might mean navigation got worse, or that search got better and people prefer it; read metrics alongside qualitative evidence.

## IA beyond menus

The same principles apply wherever people navigate a space of options:

- **Documentation**: structure by user journey (get started, learn concepts, do tasks, look up reference) rather than by internal component; each page type has a different job. See `documentation-site`.
- **E-commerce and catalogs**: categories for browsing plus facets for narrowing; categories should reflect how shoppers think ("Running shoes"), facets the attributes they decide by (size, price, use). Products may legitimately sit in several categories; give them one canonical URL.
- **Intranets and knowledge bases**: the hardest IA problem in practice, because content is produced by many teams and organized by them. Task-based entry points ("Book leave", "Find a policy"), strong search, and ruthless governance matter more than the perfect tree.
- **Settings and admin consoles**: structure by scope and object; settings that affect others should look and live differently from personal preferences.
- **Conversational and voice interfaces**: the "navigation" is the set of intents the system understands. Users cannot see the menu, so discoverability depends on prompts, examples, and graceful handling of out-of-scope requests. Group intents by user goals, and keep names of things consistent with the visual product if there is one.
- **File and asset organization**: folder hierarchies inherit all the problems of single-parent hierarchies; tags and saved searches provide alternative views.
- **APIs and developer products**: resource naming and grouping are IA; consistent nouns and predictable paths make them findable (see `api-design`).

## Worked example: restructuring an app's navigation

*Situation*: a project-management product's sidebar has grown to 14 items, including "Hub", "Insights", "Workspace", "Admin", "Tools", "Integrations", "Templates", and "Labs". Support reports frequent "where is" tickets about time tracking and exports.

1. **Inventory and audit**: list every screen and setting under each item. Discover that exports live in three places (a report screen, "Tools", and a project menu), and time tracking is under "Labs" because it began as a beta.
2. **Users and top tasks**: search logs show "time", "export", "invoice", "archive" as top queries. A top-task survey ranks: update my tasks, see what is due, log time, share status with stakeholders, manage team members.
3. **Card sort**: an open sort of 40 described items with 15 participants per group (members, admins). Members cluster around their own work vs. the team's work; admins add a clear "people and permissions" cluster. Nobody creates groups resembling "Hub", "Tools", or "Labs".
4. **Draft alternatives**: (A) object-based: Tasks, Projects, Time, Reports, Team; with Settings and Admin in utility navigation. (B) personal vs. shared: My work, Team, Reports, Admin. Write scope definitions for each.
5. **Tree test** both with the same ten tasks, 50 participants per tree. A outperforms on time-tracking and export tasks; B on "see what is due for me". Combine: object-based structure with a "My work" home view.
6. **Label and governance**: rename "Insights" to "Reports" (the word users typed). Give exports one home under Reports, with contextual links from projects. Graduate time tracking out of "Labs" and define a rule that experiments live within the area they belong to, flagged as beta, not in a separate bucket.
7. **Migration**: staged rollout, a one-time "what moved" notice, temporary pointers in old locations, redirect old routes, compare before/after search queries and support tickets.

## When working as an AI assistant

- You can draft inventories from a codebase (routes, screens, content types) or a site crawl, propose alternative structures, write scope definitions, and suggest label candidates. Make clear that these are hypotheses until tested with real users; do not present a model's own grouping as users' mental model.
- When asked to "simulate a card sort", decline to treat the output as data. Offer instead to prepare the study materials and analyse real results.
- When reading search logs or analytics, aggregate; do not surface individual users' queries or identities.

## Decision guidance

**Task-based vs. object-based navigation.** Object-based (Projects, Customers, Reports) suits products where users repeatedly manage things; it scales and stays stable as tasks evolve. Task-based (Send money, Request a refund) suits occasional-use services where users arrive with one job. Many products combine: object-based structure with task shortcuts on a home screen.

**Mega-menus, flyouts, or simple menus.** Mega-menus help when a large site has many mid-level categories users need to see to choose; they are costly on touch and for keyboard and screen-reader users unless carefully built. Prefer the simplest pattern that exposes enough scent.

**Duplicate entries in navigation.** Placing an item in two categories helps when card sorting shows a genuine split and the item is important. Overused, it bloats menus and confuses the canonical location. Prefer one home plus contextual links; duplicate in navigation only for high-traffic ambiguous items.

**Personalized or role-based navigation.** Showing different navigation per role reduces noise but makes support, documentation, and collaboration harder ("I don't see that menu"). Prefer hiding irrelevant items over rearranging shared ones, and keep the structure the same for everyone where possible.

**Categories for one audience or several entry points.** When audiences overlap heavily, one structure with good labels serves all. When audiences need almost entirely different content (e.g. patients vs. clinicians, buyers vs. sellers), separate entry points at the top are justified, but keep shared content in one place and link to it from each.

**How many top-level items?** Enough to cover the space distinctly, few enough to scan at a glance. On small screens the platform often caps visible slots (e.g. a tab bar holds only a handful), which forces prioritization of top tasks. If you need many top-level items on a large screen, group them visually and test whether users can predict which group to scan.

**Reorganize or rename?** If tree tests show people go to the right section but cannot pick the right child, the problem is usually labels or local navigation, not the top-level structure. Rename and test before reorganizing; renaming is cheaper and less disruptive for existing users.

**Global search placement.** Make search visible (not hidden behind an icon) when it is a primary path for many users or the collection is large; an icon suffices when browse dominates. On content-heavy sites, a visible search box is a strong convention.

**Settings architecture.** Group by the object being configured (account, workspace, project, notifications) and by scope (personal vs. shared); put the scope in the structure, because "who does this change affect?" is users' first question. Provide search inside settings when they exceed a few dozen items.

**Flat vs. deep.** Prefer fewer levels when labels are clear and items at each level can be grouped visually. Go deeper when a level would otherwise contain many items users cannot easily distinguish, or when sub-collections are genuinely independent.

## Pitfalls

- **Org-chart navigation.** Categories map to teams. Test by asking: would a new customer know which of these to choose?
- **Clever or branded labels.** Names that delight the team convey nothing to users. Pair or replace with descriptive words.
- **Overlapping categories.** "Tools", "Utilities", "Features". If you cannot explain the difference in one sentence, neither can users.
- **Catch-all buckets.** "Resources", "More", "Other" grow until they hold the most important content with the weakest scent.
- **Designing for everything equally.** Giving rare tasks the same prominence as top tasks makes common ones harder.
- **Treating card sort results as the answer.** Averaging dendrograms without judgment produces structures nobody actually proposed.
- **Testing with visual design only.** Usability tests on a polished UI confound structure, labels, and visuals; tree test the structure separately.
- **Search as a crutch.** "Users can just search" excuses broken navigation; many users browse first, and search quality depends on vocabulary work too.
- **No redirects.** Restructuring breaks links from bookmarks, emails, docs, and search engines.
- **Taxonomy sprawl.** Free-form tagging without governance produces "invoice", "invoices", "Invoicing", "billing-invoice".
- **Navigation that changes with context.** Menus that reorder themselves by usage or hide items based on hidden rules break spatial memory; people rely on things staying where they were.
- **Metadata nobody maintains.** Filters that return incomplete results because half the items lack the field teach users not to trust filtering.
- **Local navigation that hides siblings.** Once inside a section, users should see what else is in it; otherwise they cannot tell whether they picked the right branch.
- **Inconsistent naming across surfaces.** The menu says "Reports", the page heading says "Analytics", the help docs say "Insights". Each mismatch makes users doubt they arrived. Use one name everywhere.
- **Ignoring arrival from outside.** Many users land deep in the structure from search engines, shared links, or notifications; pages need to show where they are and how to get to related content.
- **Moving everything at once.** Big-bang IA changes disorient existing users; for established products consider staged migrations, announcements, and temporary pointers ("Reports has moved to Insights").

## Quality bar and verification

- [ ] Every top-level category has a one-sentence scope definition, and categories do not overlap in meaning.
- [ ] Top tasks are reachable in few, confident steps; tree-test success rates for top tasks are high and first clicks go to the right branch for most participants. (Set targets with the team before testing; e.g. a common bar is that most participants succeed directly on top tasks, with lower success acceptable for rare tasks.)
- [ ] Labels use users' vocabulary (traceable to card sorts, search logs, or interviews) and are consistent in form.
- [ ] Every inventory item has exactly one canonical home; ambiguous items have planned cross-links.
- [ ] The structure absorbs foreseeable growth without renaming top-level categories.
- [ ] Search handles common synonyms and misspellings from logs; zero-results pages offer recovery.
- [ ] Navigation works with keyboard and screen readers and on small screens (see `accessible-design`, `layout-and-responsive-design`).
- [ ] Governance is defined: who adds categories and tags, how terms are approved, how content is retired.
- [ ] For existing products: redirects, migration messaging, and analytics to compare before and after are planned.
- [ ] Deep pages show the user's location (breadcrumbs, section highlighting, page titles) and offer related routes, for people arriving from outside.
- [ ] Content types and metadata fields each serve a stated purpose, and filters return complete results.
- [ ] The controlled vocabulary and synonym list exist in a place where writers, developers, and search configuration all use the same terms.
- [ ] Alternatives were compared, not just one structure defended; the chosen one is justified by evidence, and known trade-offs are written down.

**Smell test before testing with users.** Read the top level aloud to someone unfamiliar with the product and ask them where they would go for three top tasks. If they hesitate between two labels, or ask what a label means, fix that before spending on a formal study.

**Common signs the IA is failing after launch**: rising search usage from navigation pages, frequent "where is" tickets, users bookmarking deep pages to avoid navigating, teams asking for their own top-level item, and an "Other" or "More" section that keeps growing.

## Depth on demand

- `references/card-sorting-and-tree-testing.md` — designing, running, and analysing card sorts and tree tests, including sample sizes, task writing, and interpreting results. Read before running either study.
