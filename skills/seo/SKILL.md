---
name: seo
description: >-
  Improve how content and sites are found through search engines and AI
  answer engines, without spam tactics. Covers search intent, keyword and
  topic research, on-page optimisation (titles, headings, meta descriptions,
  internal links, structured data), technical SEO (crawlability, indexing,
  sitemaps, robots rules, canonicals, redirects, JavaScript rendering,
  performance, mobile, international hreflang), content quality and
  usefulness, earning links, visibility in AI-generated answers, local search
  basics, and measuring results. Use when asked to "improve SEO", "rank for",
  "why isn't this page indexed", "optimise titles/meta", "add schema markup",
  "plan content for search", "SEO audit", "migrate a site without losing
  traffic", or "show up in AI answers". Not for persuasive page copy
  (copywriting), page-speed engineering in depth (web-performance-audit), or
  building the site (website-and-landing-pages, documentation-site).
metadata:
  category: product-and-communication
  related: copywriting, technical-writing, website-and-landing-pages, web-performance-audit, information-architecture, frontend-development, data-analysis, competitive-analysis, documentation-site
---

# SEO

Search engine optimisation is the practice of making useful content easy to find, easy to understand, and easy to choose — for people searching and for the systems that index and rank pages for them. Search engines' stated goal is to surface the most helpful result for a query; durable SEO aligns with that goal rather than trying to game it. Tactics that exploit ranking loopholes stop working, often abruptly, and can get a site demoted. The work that lasts is: understand what searchers need, make the best page for it, and remove the technical obstacles between that page and the index.

## Scope

Covers: intent and keyword research, content planning for search, on-page elements, structured data, technical SEO, internal linking, link earning, AI/answer-engine visibility, local and international basics, migrations, and measurement.

Neighbours:

- `copywriting` — persuasion and conversion once someone lands.
- `technical-writing` — writing the explanatory content well.
- `web-performance-audit` — deep performance diagnosis (Core Web Vitals overlap).
- `information-architecture` — site structure and navigation in depth.
- `website-and-landing-pages`, `documentation-site`, `frontend-development` — building the pages.
- `data-analysis` — analysing search and traffic data rigorously.
- `competitive-analysis` — broader competitor study.

Specific ranking-system details change continually. This skill teaches principles that have stayed stable; check current search-engine documentation (e.g. Google Search Central, Bing Webmaster Guidelines) for specifics such as current structured-data eligibility or metric thresholds.

## Core principles

### 1. Intent first

Every query carries an intent, and the page that ranks is the one that best satisfies it. Common intent types:

| Intent | Searcher wants | Pages that tend to satisfy it |
|---|---|---|
| Informational | To learn or understand ("how does X work", "what is Y") | Guides, explanations, tutorials |
| Navigational | A specific site or page ("[brand] login") | That page — don't fight for others' navigational queries |
| Commercial investigation | To compare before deciding ("best X for Y", "X vs Y", "X reviews") | Comparisons, reviews, buyer's guides |
| Transactional | To act ("buy X", "X pricing", "download X") | Product, pricing, signup, download pages |
| Local | Something nearby ("X near me", "X in [city]") | Local business profiles, location pages |

The fastest way to determine intent is to look at what currently ranks: the search results page shows what the engine has learned searchers want (format, depth, freshness, type). A product page will struggle to rank for a query where every result is a how-to guide. Match the dominant intent, then do it better.

### 2. Make the best page for the query

"Best" means: answers the searcher's actual question completely and accurately, quickly, with evidence of real expertise or experience, in a format that suits the need, from a source the searcher can trust. Search engines increasingly emphasise content that demonstrates first-hand experience, expertise, and trustworthiness (Google's guidance frames this as E-E-A-T). Pages that summarise what already ranks without adding anything give the engine no reason to prefer them.

### 3. Remove obstacles to crawling, rendering, and indexing

A page can only rank if the engine can discover it, fetch it, render it, understand it, and decide to index it. Technical SEO is mostly about not breaking that chain. Most technical problems are invisible to visitors and obvious in search-console data — so check the data.

### 4. Clarity for machines follows clarity for humans

Descriptive titles, logical headings, clear page purpose, meaningful link text, and structured data help engines understand what a page is about — and are the same things that help people. Optimising for one rarely hurts the other; when it seems to, favour the person.

### 5. Authority is earned, not manufactured

Links and mentions from relevant, reputable sources remain important signals. They come from making things worth referencing — original data, tools, definitive guides, genuine expertise, newsworthy work — and telling the right people about them. Buying links, link schemes, and mass-produced guest posts violate search-engine policies and risk penalties.

### 6. Measure against business outcomes

Rankings and traffic are means. The goal is the outcome the site exists for — signups, sales, leads, support deflection, readership. A page ranking #1 for a query that never converts may matter less than a page ranking #6 for one that does. Track both search metrics and outcomes.

## Process

### Step 1: Establish goals and context

- What is the site for, and what outcome should search traffic drive?
- Who are the target searchers, and in which markets and languages?
- What's the current state: indexed pages, existing traffic, known problems, recent changes (redesigns, migrations, CMS changes)?
- What access exists: search-console accounts (e.g. Google Search Console, Bing Webmaster Tools), analytics, the codebase or CMS, server logs?
- Constraints: brand rules, legal/regulatory content limits, development capacity.

If you have access to the site's code or a crawl, look before recommending. If you have no data access, say so and frame recommendations as hypotheses to check.

### Step 2: Audit what exists (for existing sites)

Prioritise by impact. A typical order:

1. **Indexing health**: is the site indexed? Are important pages excluded (noindex, robots blocks, canonicalised elsewhere, soft 404s, "crawled — currently not indexed")? Search-console coverage/indexing reports are the primary source.
2. **Crawlability**: robots rules, sitemap accuracy, internal links reaching important pages, redirect chains, broken links, server errors, rendering of JavaScript content.
3. **Duplicate and thin content**: parameter variants, HTTP/HTTPS or www/non-www duplicates, faceted navigation explosions, near-empty pages.
4. **On-page basics**: titles, headings, meta descriptions, internal linking on the pages that matter most.
5. **Performance and mobile usability**.
6. **Content quality and coverage** relative to target queries.
7. **Links**: referring domains, broken inbound links to fix with redirects, toxic patterns (rarely the main issue; don't obsess).

Crawling tools (various desktop and hosted crawlers) and search-console data together give a fuller picture than either alone.

### Step 3: Research queries and topics

- **Seed** from the business: products, problems solved, customer language (support tickets, sales calls, reviews, site search logs).
- **Expand** with keyword tools (search engines' own planners and autocomplete, "people also ask"-style features, third-party SEO tools) to find related queries, volumes, and difficulty. Treat volume estimates as rough — tools disagree, often by large factors.
- **Inspect results** for each important query: intent, format, who ranks (big brands? forums? niche experts?), what SERP features appear (featured snippets, videos, local packs, AI summaries).
- **Cluster** queries that share intent and would be satisfied by the same page; one page per intent cluster, not one page per keyword variant. Separate pages for the same intent cannibalise each other.
- **Prioritise** by relevance to the business outcome × realistic ability to rank × demand. Long-tail, specific queries are often lower volume but higher intent and easier to win, especially for newer sites.

### Step 4: Plan content and architecture

- Map each cluster to an existing page (improve it) or a new one (create it). Prefer improving and consolidating over proliferating.
- Organise related pages into topic hubs: a broad overview page linking to specific subtopic pages, which link back and to each other where relevant. This helps users navigate and helps engines understand topical coverage.
- Keep important pages within a few clicks of the homepage and linked from relevant context, not only from footers or sitemaps.
- Plan URLs that are short, readable, stable, and descriptive (`/guides/rotate-api-keys` rather than `/p?id=8812`). Changing URLs later costs equity even with redirects.

### Step 5: Create or improve pages

Write for the searcher's need (see `technical-writing` and `copywriting`), then check on-page elements below.

### Step 6: Fix technical issues

Implement technical fixes in priority order, verify each, and re-request indexing for critical pages where the engine provides that option.

### Step 7: Earn visibility

Promote content that merits links to people who care about it; pursue digital PR, partnerships, and genuine community participation. See Links.

### Step 8: Measure and iterate

Results take weeks to months. Track, learn, refresh content, and revisit priorities. See Measurement.

## On-page elements

### Title element

- The single most influential on-page element for relevance and click-through. Make it unique per page, descriptive of the page's content, front-loaded with the main topic, and appealing to click.
- Length: long titles are truncated in results (the limit is pixel-based; roughly 50–60 characters is a common guideline). Put what matters first.
- Engines may rewrite titles they find unhelpful, mismatched with the content, or stuffed; that's a signal to improve them.
- Include the brand where it helps recognition, usually at the end, unless the brand is the query.

### Meta description

Not a direct ranking factor, but often shown as the snippet and therefore affects click-through. Summarise the page's value specifically, match intent, and keep it reasonably concise (roughly 150–160 characters before truncation on desktop). Engines often generate their own snippet from page text; that's normal.

### Headings and structure

- One clear main heading (typically the `h1`) stating the page's topic; it can differ from the title.
- Logical subheadings that reflect the questions searchers have — these also make passages easier for engines to extract as answers.
- Answer the core question early and plainly, then elaborate.

### Body content

- Cover the topic as thoroughly as the intent requires — not padded to a word count. Length correlates with rankings only because thorough pages tend to be longer.
- Use the terms searchers use, naturally; include related concepts a knowledgeable treatment would cover. Don't repeat exact phrases unnaturally (keyword stuffing).
- Show expertise and experience: original examples, data, screenshots, step-by-step process, named and qualified authors where relevant, sources cited.
- Keep it current; date it if freshness matters to the topic, and update substantively rather than just changing the date.

### Internal links

- Link from relevant pages to the pages you want found, using descriptive anchor text (what the target is about, not "click here").
- Fix orphan pages (no internal links in).
- Avoid excessive sitewide links that dilute meaning; context links within body content carry the clearest signal.

### Images and media

- Descriptive file names and alt text (alt text is primarily for accessibility; it also helps image search).
- Compressed, appropriately sized, modern formats; lazy-load below-the-fold media but not the main (largest) above-the-fold image.
- For video, provide a dedicated, crawlable page, title, description, thumbnail, and transcript.

### Structured data

- Structured data (typically schema.org vocabulary in JSON-LD) describes entities on the page — articles, products, offers, reviews, events, organisations, FAQs, how-tos, breadcrumbs, recipes, job postings, local businesses, software applications.
- It can make pages eligible for rich results and helps machines (including AI systems) understand content. It does not guarantee rich results, and eligibility rules change — check the search engine's current documentation for which types are supported.
- Mark up only what is visible on the page and true. Marking up hidden or false content (fake reviews, misleading prices) violates guidelines and can trigger manual actions.
- Validate with the engine's rich-results test and a schema validator.

## Technical SEO

Detailed checklists and edge cases (JavaScript rendering, faceted navigation, migrations, international) are in `references/technical-seo.md` — read it when auditing a site's technical health, planning a migration or redesign, dealing with JS-rendered sites, or targeting multiple countries/languages.

The essentials:

- **Robots rules** (`robots.txt`) control crawling, not indexing. A page blocked by robots can still be indexed (from links) without content. To keep a page out of the index, allow crawling and use `noindex` (meta robots tag or `X-Robots-Tag` header).
- **XML sitemaps** list canonical, indexable URLs you want found, with accurate last-modified dates. Submit them in search consoles. Keep them free of redirects, errors, and noindexed URLs.
- **Canonicalisation**: one canonical URL per piece of content. Use `rel="canonical"` to consolidate duplicates (parameters, tracking codes, print versions), consistent internal linking to the canonical, and redirects for protocol/host variants. Canonical tags are hints; contradictory signals (sitemap lists URL A, canonical says B, internal links point to C) confuse engines.
- **Redirects**: permanent (301/308) for moved content; avoid chains and loops; redirect to the most relevant equivalent, not everything to the homepage.
- **Status codes**: real 404/410 for removed content (not 200 "not found" pages — soft 404s); avoid 5xx errors; handle maintenance with 503 and `Retry-After`.
- **JavaScript**: engines can render JS but with delays and limits; critical content and links should be in the server-rendered HTML where feasible (server-side rendering, static generation, or hydration of pre-rendered content). Links must be real `<a href>` elements.
- **Performance and page experience**: fast loading, stable layout, responsive interaction (measured by Core Web Vitals in Google's case), HTTPS, no intrusive interstitials. These are modest ranking factors but strong user-experience and conversion factors. See `web-performance-audit`.
- **Mobile**: engines index primarily the mobile version; content, structured data, and links must be equivalent on mobile.
- **International**: `hreflang` annotations link language/region alternates; use consistent URL structures (subdirectories, subdomains, or country domains, each with trade-offs).

## AI and answer-engine visibility

Search increasingly includes AI-generated summaries, and people also query conversational AI assistants that cite or draw from web content. The field is young and evolving; practitioners disagree on tactics, and measurement is immature. Principles that appear robust:

- **The fundamentals still apply.** AI search features generally draw from indexed, crawlable, trusted pages. Pages that rank well and are clearly structured are more likely to be cited.
- **Be extractable.** State answers clearly and early, in self-contained passages under descriptive headings; define terms; use lists and tables for steps and comparisons. A passage that answers a question without needing surrounding context is easy to quote.
- **Be citable.** Original data, specific facts, named expertise, and clear sourcing make content worth citing. Generic rewrites of common knowledge offer nothing distinctive to cite.
- **Be consistent about entities.** Consistent naming of the organisation, products, and people across the site, structured data, and reputable third-party profiles helps systems connect facts to the right entity.
- **Mind crawler access.** AI providers operate their own crawlers with their own user-agent tokens, and several honour robots rules. Decide deliberately which to allow — blocking them may reduce visibility in those systems; allowing them may permit training use. This is a business decision; surface it to the user rather than deciding silently.
- **Emerging conventions** such as `llms.txt` files are proposals without broad confirmed adoption by major engines; treat them as low-cost experiments, not essentials.
- **Measure what you can**: referral traffic from AI assistants and search features, brand mentions in AI answers for your key queries (sampled manually or with emerging tools), and impression changes on queries with AI summaries.

Be wary of anyone promising guaranteed placement in AI answers.

## Decision guidance

### Improve, consolidate, or create?

| Situation | Usually best |
|---|---|
| A page exists for the intent but underperforms | Improve it in place (keeps URL history and links) |
| Several weak pages target the same intent | Consolidate into one strong page; 301 the others to it |
| No page satisfies an intent the business cares about | Create one |
| Page has no traffic, links, or business value, and can't be made useful | Remove (404/410) or noindex; redirect only if a true equivalent exists |
| Page is outdated but still attracts searches | Refresh substantively; update facts, examples, and date |

Pruning low-value pages can help a site overall by concentrating crawling and quality signals, but delete cautiously: check traffic, links, and conversions before removing anything.

### Programmatic (templated) pages at scale

Generating many pages from data (locations, integrations, product combinations) can be legitimate when each page answers a distinct real query with distinct, useful data — e.g. a page per integration with real setup details. It becomes spam when pages differ only by a swapped keyword. Test: would a searcher landing on any one of these pages find it genuinely useful and different from its siblings? Launch a sample, monitor indexing rates and engagement, then scale.

### Subdomain vs. subdirectory for content (blog, docs, help)

Subdirectories (`example.com/blog`) keep everything under one host and tend to be simpler for consolidating signals; subdomains are sometimes needed for technical or organisational reasons. Practitioners disagree on how much it matters; engines say they can handle both. If the platform makes subdirectories feasible, they're the lower-risk default; if not, a subdomain with strong internal linking works.

### When SEO isn't the right channel

Search serves existing demand. For a product creating a new category with no search volume, search can capture the adjacent problems people do search for, but awareness may need other channels first. Say so rather than promising search traffic for queries no one types.

## Local search basics

For businesses serving physical locations: claim and complete the business profile on the major map/search platforms; keep name, address, phone consistent everywhere (site, profiles, directories); create genuine location pages with unique content; earn and respond to reviews honestly (never buy or fake them, and follow platform rules on soliciting them); use LocalBusiness structured data.

## Links

- **What works**: original research and data, free tools and calculators, definitive resources, expert commentary for journalists, partnerships and integrations, community contributions, being genuinely newsworthy, fixing broken inbound links via redirects, asking sites that mention you without linking to add a link.
- **What to avoid**: buying or selling links that pass ranking credit, link exchanges at scale, private blog networks, automated link building, low-quality directory and comment spam, mass guest posting for links. Paid, sponsored, and user-generated links should carry `rel="sponsored"`, `rel="ugc"`, or `rel="nofollow"` as appropriate.
- Don't panic about spammy inbound links you didn't create; engines largely ignore them. Disavow tools exist for specific manual-action situations, not routine cleanup.

## Spam tactics: never

Search-engine spam policies prohibit, among others: keyword stuffing; hidden text or links; cloaking (showing engines different content from users); doorway pages; scraped or mass-produced content with little value (including unedited bulk AI output aimed at ranking rather than helping); sneaky redirects; link schemes; fake structured data; site-reputation abuse (hosting low-quality third-party content on a trusted domain to exploit its ranking). These risk manual actions or algorithmic demotion of the whole site. If a user requests them, explain the risk and offer a legitimate alternative.

Using AI to help produce content is not itself prohibited; publishing content at scale *primarily to manipulate rankings* without adding value is. Human review, real expertise, and original value are the safeguards.

## Measurement

- **Search consoles** (impressions, clicks, average position, click-through rate by query and page; indexing and enhancement reports) are the ground truth for search visibility.
- **Analytics** for behaviour and outcomes of organic visitors (engagement, conversions, revenue).
- **Rank tracking** for key queries — useful for trends, but rankings vary by location, device, and personalisation, so treat as indicative.
- **Server logs** for crawl behaviour on large sites (what bots fetch, how often, errors).

Interpreting changes:

- SEO effects lag: crawling, indexing, and re-ranking take days to months.
- Compare like periods (seasonality), and annotate changes (deploys, content updates, known algorithm updates) so causes can be reasoned about.
- Distinguish impressions (visibility) from clicks (appeal) from conversions (value). Rising impressions with falling CTR may mean titles/snippets need work or that SERP features (including AI summaries) are answering the query directly.
- Where traffic allows, test changes on groups of similar pages (split tests on page templates) rather than inferring from single-page before/after comparisons, which are confounded by everything else changing. See `experiment-design`.

## Pitfalls

- **Optimising for keywords instead of intent** — a product page aimed at a how-to query.
- **One page per keyword variant** — cannibalisation and thin pages.
- **Blocking with robots.txt to deindex** — stops crawling, not indexing; use noindex.
- **Accidental noindex** carried from staging to production. Check after every launch.
- **Migrations without redirect maps** — the most common cause of catastrophic traffic loss. See references.
- **Client-side-only rendering** of essential content and links.
- **Contradictory canonical signals.**
- **Chasing every tool score** — automated audit scores flag many trivia; prioritise by impact on important pages.
- **Treating volume estimates as truth.**
- **Thin "SEO content"** written to hit keywords, offering nothing new.
- **Ignoring conversion** — traffic that doesn't serve the business.
- **Changing many things at once** and being unable to attribute results.
- **Expecting instant results**, or declaring failure after a week.
- **Promising rankings** — no one controls them; set expectations about effort and likelihood, not positions.

## Quality bar

For a page:

- [ ] Targets a clearly identified intent cluster, matching the format of what satisfies it.
- [ ] Adds something beyond existing results: experience, data, depth, clarity, or usability.
- [ ] Unique, descriptive title and meta description; logical headings; answer stated early.
- [ ] Linked internally from relevant pages with descriptive anchors; links out to sources where useful.
- [ ] Indexable (no stray noindex, not blocked, canonical points to itself or deliberately elsewhere), in the sitemap, returns 200.
- [ ] Renders essential content in HTML; fast and usable on mobile.
- [ ] Structured data, if used, is valid and matches visible content.
- [ ] Accurate, current, attributed where expertise matters.

For a site or audit: issues prioritised by impact; each recommendation states what, why, where, and how to verify; data sources and their limitations named; no spam tactics; measurement plan in place.

When reporting, separate what you verified (from code, crawls, or console data) from what you inferred, and give expected timelines honestly.

## Illustrative example: a page that won't rank

*Illustrative only.* A SaaS company's "Invoice templates" page gets impressions but almost no clicks, at position ~25.

Investigation: the query's results are dominated by pages offering free downloadable templates with previews; the company's page is a product feature page describing its invoicing software. Intent mismatch: searchers want templates, not software. The title is "Invoicing | [Brand]".

Recommendation: create a genuinely useful templates page (several downloadable formats, previews, guidance on what an invoice must legally include in key markets, written with the company's accounting expertise), with a natural path to the software for those who want automation. Title it for the intent ("Free invoice templates (Word, Excel, PDF) — with what to include"). Keep the feature page targeting software-intent queries ("invoicing software for freelancers"). Link the two. Measure impressions, CTR, template downloads, and trial starts from the page over the next two to three months.
