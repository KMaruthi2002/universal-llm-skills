# Technical SEO in depth

Read this when auditing a site's technical health, planning a migration or redesign, working on a JavaScript-heavy site, managing large or faceted sites, or targeting several countries or languages. Check current search-engine documentation for specifics that change (supported directives, thresholds, tool names).

## The indexing pipeline

Discovery → crawl → render → index → rank. Diagnose by locating where a page drops out:

| Stage | Question | Evidence |
|---|---|---|
| Discovery | Does the engine know the URL exists? | In sitemap? Linked internally? Search-console URL inspection says "URL is unknown"? |
| Crawl | Can it fetch it? | robots.txt allows it; server returns 200 quickly; no auth wall; logs show bot hits |
| Render | Does the rendered HTML contain the content and links? | URL inspection's rendered HTML/screenshot; compare with the raw HTML |
| Index | Did the engine choose to index it? | Indexing report status: noindex, duplicate (canonical chosen elsewhere), soft 404, "crawled/discovered — not indexed" (often quality or crawl-priority signals) |
| Rank | Does it appear for relevant queries? | Impressions by query in search console |

"Crawled — currently not indexed" and "discovered — not indexed" at scale usually point to low perceived value (thin, duplicate, or templated pages) or insufficient internal linking/crawl priority, not to a technical switch you can flip.

## robots.txt

- Located at the host root; applies per host and protocol.
- Controls crawling only. Blocking a URL prevents the engine from seeing a `noindex` on it.
- Don't block CSS/JS resources needed for rendering.
- Use it to keep bots out of infinite spaces (internal search results, endless calendars, faceted combinations) and low-value areas, conserving crawl capacity on large sites.
- Test changes before deploying; a single `Disallow: /` shipped from staging deindexes over time.
- AI crawlers: providers publish their user-agent tokens; some distinguish crawling for search features from crawling for model training. Decide per business policy and document it.

## Indexing directives

- `<meta name="robots" content="noindex">` or `X-Robots-Tag: noindex` header (the header works for PDFs and other non-HTML files).
- `nofollow` on a page-level robots tag stops the engine following that page's links — rarely what you want.
- Snippet controls (`nosnippet`, `max-snippet`, `data-nosnippet`) limit what can be shown in results and may affect use in AI summaries; trade visibility for control knowingly.
- Password-protect or remove truly private content; noindex is not access control.

## Sitemaps

- Include only canonical, indexable, 200-status URLs.
- Accurate `lastmod` (only when content meaningfully changed) helps engines prioritise recrawls; fake freshness is ignored over time.
- Split large sitemaps (limits are around 50,000 URLs or 50 MB uncompressed per file) and use a sitemap index; separate by type (pages, products, articles) to monitor indexing rates per section.
- Specialised sitemaps exist for images, video, and news; check current support.
- Reference sitemaps in robots.txt and submit them in search consoles.

## Canonicalisation and duplicates

Sources of duplication: protocol (http/https), host (www/non-www), trailing slashes, case, parameters (sorting, tracking, session IDs), print/AMP/alternate versions, pagination, syndicated content, faceted navigation, staging sites left public.

- Pick one canonical form and enforce it: redirects for host/protocol variants, self-referencing canonical tags on canonical pages, canonical tags on variants pointing to the canonical.
- Keep signals consistent: internal links, sitemaps, canonicals, hreflang, and structured data should all reference the same canonical URL.
- Canonical tags must point to indexable, 200-status pages, not redirects or noindexed pages.
- For syndicated content, ask partners to canonical back to the original or to noindex their copy.
- Protect staging environments with authentication, not just noindex.

## Pagination and faceted navigation

- Paginated series: let each page be crawlable and indexable with self-canonicals (don't canonical page 2+ to page 1 if they contain different items); link pages with plain links. Engines no longer use `rel=prev/next` as an indexing signal (Google), though it does no harm.
- Facets (colour × size × brand × price) can create millions of URLs. Decide which combinations have search demand and deserve indexable, linkable URLs; for the rest, avoid crawlable links (e.g. use non-link controls or parameters blocked in robots), or noindex, or canonical to the parent. Choose based on whether the engine should see the pages at all (robots) or see but not index them (noindex) — not both on the same URL.

## Redirects and status codes

- 301/308 for permanent moves; 302/307 for genuinely temporary ones. Engines eventually treat long-standing temporary redirects as permanent, but be explicit.
- Avoid chains (A→B→C) and loops; update internal links to point to final destinations.
- Removed content: 404 or 410; redirect only when there's a genuinely equivalent replacement. Redirecting everything to the homepage is treated as a soft 404.
- Soft 404s: pages returning 200 with "not found" or empty content (e.g. empty search results, out-of-stock pages with no content). Return real error codes or add useful content.
- Server errors (5xx) and timeouts reduce crawl rate; monitor them.
- Geolocation or language redirects based on IP/Accept-Language can prevent engines (which crawl mostly from one region) from seeing alternates; prefer suggestion banners plus hreflang.

## JavaScript sites

- Engines render JavaScript but may do so later than the initial crawl and with resource limits; other engines and many AI crawlers render little or no JS.
- Prefer server-side rendering, static generation, or pre-rendering for content and links that matter for search. Client-side rendering is acceptable for app-like, logged-in, or non-search areas.
- Links must be `<a href="/real/url">`; click handlers on divs and `href="#"` aren't followed.
- Each indexable view needs its own URL (History API routing, not fragments `#/view`).
- Metadata (title, meta description, canonical, robots, structured data) should be present in the server response; if set client-side, verify the rendered output, and never send conflicting values (e.g. server says noindex, JS removes it — the engine may honour the first).
- Don't block JS/CSS/API endpoints needed for rendering.
- Lazy-loaded content must load without user interaction (scroll events alone may not fire for crawlers); use native lazy loading or intersection observers that work during rendering.
- Verify with the engine's URL-inspection rendered HTML, not just your browser.

## Performance and page experience

- Core Web Vitals (Google's user-experience metrics — currently loading, interactivity responsiveness, and visual stability) are measured from real-user data. Field data (from real users) is what counts for ranking; lab tools help diagnose.
- Common wins: optimise and properly size the largest above-the-fold image and prioritise its loading; reduce render-blocking resources; reserve space for images, ads, and embeds to prevent layout shift; reduce main-thread JavaScript; use caching and a CDN.
- See `web-performance-audit` for method.

## Mobile-first indexing

- The mobile rendering is what's indexed. Ensure parity: same primary content, headings, structured data, metadata, internal links, and images (with alt text) on mobile.
- Content hidden behind tabs/accordions on mobile is generally indexed, but don't remove it from the mobile DOM.

## International SEO

- **URL structure** options: country-code domains (strong geo signal, costly to maintain authority across many domains), subdirectories (`/de/` — consolidates authority, simple), subdomains (`de.example.com` — middle ground). Choose by business and operational factors; consistency matters more than the choice.
- **hreflang**: annotate each language/region version with all alternates, including itself; annotations must be reciprocal; use correct language (ISO 639-1) and optional region (ISO 3166-1 alpha-2) codes (`en-GB`, not `en-UK`); include `x-default` for a fallback/selector page. Implement in HTML head, HTTP headers, or sitemaps — one method consistently.
- Canonicals on each language version should be self-referencing; never canonicalise translations to one language.
- Translate properly, including titles, metadata, structured data, and URLs where appropriate; machine translation without review often produces low-quality pages.
- Localise beyond language: currency, units, examples, local search behaviour and terminology (keyword research per market — direct translations of keywords often miss what locals search).

## Site migrations and redesigns

Migrations (domain changes, URL restructures, platform/CMS changes, HTTPS moves, merges) are the highest-risk SEO events. Process:

1. **Inventory** every URL with traffic, links, or rankings (from crawls, analytics, search console, backlink data, sitemaps, logs).
2. **Map** every old URL to the most relevant new URL (one-to-one where possible). Unmapped valuable URLs lose their equity.
3. **Preserve** what works: content, titles, headings, internal linking, structured data on high-value pages — change as little as possible at the same time as the move, so problems are attributable.
4. **Stage and test**: crawl the staging site (protected by auth); test redirects in bulk against the map; check canonicals, hreflang, robots rules, noindex tags, sitemaps, and rendering.
5. **Launch**: deploy redirects simultaneously with the switch; remove staging noindex/robots blocks; submit new sitemaps (and keep old sitemaps temporarily to speed redirect discovery); use the search console's change-of-address tool for domain moves where available.
6. **Monitor** daily for the first weeks: crawl errors, 404s, indexing counts, traffic by section, rankings for key queries. Fix gaps quickly.
7. **Keep redirects** in place for at least a year, ideally indefinitely.

Expect temporary fluctuation even when done well. A redirect map that sends everything to the homepage, or a forgotten `noindex`, can cause losses that take months to recover.

## Structured data implementation notes

- JSON-LD in the page head or body is the generally recommended format; keep it in sync with visible content (generate both from the same data).
- Use the most specific applicable type; include required and recommended properties for the rich-result type you target.
- Nest entities logically (Product → Offer → AggregateRating) and connect organisation/website/author entities with consistent `@id` references across pages.
- Validate with the engine's rich-results testing tool and monitor enhancement reports for errors after deploys.
- Rich-result eligibility changes (types are added, restricted, or retired); recheck documentation rather than relying on past behaviour.

## Logs and crawl budget (large sites)

Crawl budget matters mainly for sites with hundreds of thousands of URLs or more, or with rapidly changing content. Analyse server logs (verified bot user agents via reverse DNS) to see which sections are crawled, how often, and what errors bots meet. Improve by eliminating crawl traps, consolidating duplicates, speeding up server responses, fixing errors, and strengthening internal links to important sections.
