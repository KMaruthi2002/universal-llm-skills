---
name: web-performance-audit
description: >-
  Measure, diagnose, and prioritize improvements to how fast web pages load
  and respond for real users. Covers Core Web Vitals (check the current metric
  set and thresholds), field data versus lab data, reading network waterfalls
  and performance traces, render-blocking resources, images and fonts,
  JavaScript cost and long tasks, layout shift, server response time, caching
  and CDNs, third-party scripts, performance budgets, and writing a
  prioritized, evidence-based report. Use when asked "why is my site slow",
  "audit page speed", "improve Lighthouse score", "fix LCP/INP/CLS", "Core Web
  Vitals failing in Search Console", or to set performance budgets. For
  optimizing backend or algorithmic code paths use performance-optimization.
metadata:
  category: quality
  related: performance-optimization, frontend-development, observability, seo, website-and-landing-pages, ci-cd-pipelines, accessibility-audit, data-analysis
---

# Web Performance Audit

A web performance audit finds out **how fast the site actually is for its real users, why, and which changes would make the biggest difference for the least effort**. The deliverable is a short list of prioritized, evidence-backed recommendations, not a screenshot of a score.

## Scope

Covers front-end and delivery performance of websites and web apps as experienced in the browser: loading, rendering, responsiveness to input, and visual stability, plus the server and network factors that feed them (time to first byte, caching, CDNs, compression).

Neighbouring skills:

- `performance-optimization` — profiling and speeding up application code, queries, and algorithms in general, including backend services.
- `observability` — instrumenting systems and building monitoring; this skill uses its output (real-user monitoring) and may recommend it.
- `seo` — search visibility, where page experience is one factor among many.
- `frontend-development` — implementing the fixes.

## Check the current metrics first

Google's **Core Web Vitals** are the most widely used user-centric metrics, and they change over time. At the time of writing they are:

| Metric | Measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| Largest Contentful Paint (LCP) | Loading: when the largest content element in the viewport rendered | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| Interaction to Next Paint (INP) | Responsiveness: latency from user input to the next frame, across the page's interactions | ≤ 200 ms | 200–500 ms | > 500 ms |
| Cumulative Layout Shift (CLS) | Visual stability: unexpected movement of content | ≤ 0.1 | 0.1–0.25 | > 0.25 |

INP replaced First Input Delay (FID) as a Core Web Vital in March 2024; older reports and tools may still mention FID. Thresholds are assessed at the **75th percentile** of page loads, segmented by mobile and desktop. If you can browse, confirm the current metric set and thresholds on the official web.dev / Chrome documentation before auditing; if you cannot, state the version of the definitions you are using.

Supporting diagnostic metrics (not Core Web Vitals, but useful for explaining them): Time to First Byte (TTFB, good is roughly ≤ 0.8 s), First Contentful Paint (FCP, good roughly ≤ 1.8 s), Total Blocking Time (TBT, a lab proxy for responsiveness), and long tasks (main-thread tasks over 50 ms).

Metrics are means, not ends. A site can pass all three and still feel slow on its key interaction (a search that takes four seconds to show results), and the audit should notice that. Ask what "fast" means for this product's users: time to see the product image, time until the editor is usable, time for a filter to apply.

## Core principles

**1. Field data is the truth; lab data is the microscope.** Field data (real-user monitoring, RUM; or the Chrome UX Report, CrUX, a public 28-day rolling dataset of real Chrome users for sufficiently popular origins and URLs) tells you what users actually experience across their devices and networks. Lab data (Lighthouse, WebPageTest, browser devtools performance panel) runs one load in a controlled environment and tells you *why*. Start from field data to find which pages and metrics are bad and for whom; use lab tools to diagnose. A lab score of 98 on a fast laptop says nothing about users on mid-range phones on congested mobile networks.

**2. Distributions, not averages.** Performance has long tails. Look at the 75th percentile (the Core Web Vitals standard) and the 90th/95th for key journeys. Segment by device class, connection, geography, page template, and logged-in versus anonymous. An average hides the users who are suffering.

**3. Diagnose before prescribing.** Generic advice ("minify JavaScript, lazy-load images, use a CDN") is cheap and often irrelevant. Find the actual bottleneck for the actual metric: an LCP problem caused by a slow server needs a different fix from one caused by a late-discovered hero image. Each recommendation should trace back to evidence in a trace, waterfall, or field breakdown.

**4. The critical path decides loading.** For the first render, what matters is the chain of resources the browser must fetch and process before it can paint the important content: HTML, render-blocking CSS, synchronous scripts in the head, fonts, the LCP image. Shorten that chain (fewer round trips, earlier discovery, less blocking) and loading improves; optimizing resources not on it changes little.

**5. The main thread is a single lane.** Parsing, style, layout, paint, and all JavaScript share one thread. Long tasks block input handling, which is what INP measures. Most responsiveness problems are too much JavaScript doing too much work at the wrong time.

**6. Prioritize by impact times reach divided by effort.** A change that improves LCP by one second on the template serving 60% of traffic beats a perfect fix on a rarely visited page. Recommend in order, with estimated impact and effort, and identify quick wins.

## Process

### 1. Frame the audit

Establish, asking if unclear:

- Which pages or templates and which user journeys matter most (landing pages, product pages, search, checkout, app dashboard).
- Who the users are: device mix, regions, networks. Analytics usually answers this.
- What triggered the audit: failing Core Web Vitals, a drop in conversions, a regression after a release, a redesign, a target score.
- Constraints: tech stack, hosting/CDN, build system, CMS, third-party contracts (ads, analytics, chat widgets), and who can change what.
- Access: field data sources (RUM tool, CrUX via PageSpeed Insights or the CrUX API/dashboard, Search Console's Core Web Vitals report), production and staging URLs, source code.

### 2. Gather field data

- Pull CrUX data for the origin and key URLs (PageSpeed Insights shows it at the top when available; the CrUX API and BigQuery dataset go deeper). Note whether URL-level data exists or only origin-level, and the mobile/desktop split.
- If the site has RUM (commercial RUM tools, or the open-source web-vitals library reporting to analytics), segment by template, device, country, and connection, and look at trends over time to spot regressions tied to releases.
- Identify the worst metric on the most important templates. That is where the audit focuses.
- For INP, field data with attribution (which interaction, which element, which phase was slow) is far more useful than lab tests, because lab tools cannot know what users click. The web-vitals library's attribution build and some RUM tools provide it.
- Note limitations: CrUX covers Chrome users only, needs enough traffic, and lags by up to 28 days, so it will not yet reflect recent fixes.

If there is no field data at all, say so, recommend adding RUM, and use lab data with throttling that approximates the user base (a mid-range mobile device and a slow 4G profile is a common default), clearly labelled as an approximation.

### 3. Collect lab evidence

For each key template:

- Run a lab test several times (results vary; take the median of three to five runs) with mobile emulation and throttling. Lighthouse in devtools or CLI, PageSpeed Insights, and WebPageTest are typical; WebPageTest adds real devices, locations, filmstrips, and repeat-view caching tests.
- Record a performance trace in browser devtools for detailed main-thread analysis, with CPU throttling enabled.
- Test both first visit (cold cache) and repeat visit (warm cache), and both logged-out and logged-in states if they differ.
- Test from a location near the users, because distance dominates latency.

Without browser or network access, work from what the user can provide: exported Lighthouse JSON or HTML reports, HAR files, WebPageTest result links, trace files, RUM screenshots, or the source code and build output. Say which conclusions are inferred.

### 4. Read the waterfall

A network waterfall shows each request on a timeline. Read it top to bottom asking:

- **When does the HTML arrive?** A long bar before the first byte means server time or redirects (TTFB). Count redirects: each costs a full round trip, and a mobile redirect or an `http` to `https` hop at the start delays everything.
- **What blocks the first render?** Stylesheets in the head and synchronous scripts block rendering. How many are there, how big, from how many origins? Each new origin needs DNS, TCP, and TLS setup.
- **When is the LCP resource discovered and requested?** If the hero image only starts downloading after JavaScript runs (e.g. a client-rendered carousel or a CSS background image), the request starts late no matter how small the image is. This "resource load delay" is one of the most common LCP problems.
- **Are there request chains?** CSS importing CSS, scripts loading scripts, fonts discovered only after CSS loads. Chains serialize latency.
- **What is big?** Sort by transfer size: unoptimized images, huge JavaScript bundles, uncompressed text resources, video autoplaying above the fold.
- **What is from third parties?** Tag managers, analytics, ads, A/B testing, chat, consent tools, social embeds. They often dominate both bytes and main-thread time.
- **Is caching working?** In a repeat view, static assets should come from cache. Check `Cache-Control` headers and whether file names are fingerprinted.
- **Is the protocol and compression right?** HTTP/2 or HTTP/3, Brotli or gzip on text resources.

### 5. Diagnose each failing metric

**LCP.** Break it into its parts (a breakdown available in devtools and RUM attribution): TTFB, resource load delay (time from TTFB until the LCP resource starts loading), resource load duration, and element render delay (time from resource loaded until painted). Fix the largest part:

| Largest part | Likely causes | Typical fixes |
|---|---|---|
| TTFB | Slow server rendering, uncached HTML, database work, distant origin, redirects | Cache HTML at the CDN/edge where possible, optimize server code and queries, remove redirects, use a CDN close to users, stream HTML early |
| Load delay | LCP image discovered late (inserted by JS, lazy-loaded, CSS background), low fetch priority | Put the image in the initial HTML, never lazy-load the LCP image, use `fetchpriority="high"` or a preload, server-render the hero |
| Load duration | Large image, wrong format, no responsive sizes, slow origin | Modern formats (AVIF/WebP), correct dimensions with `srcset`/`sizes`, compression, image CDN |
| Render delay | Render-blocking CSS/JS, client-side rendering, web font blocking text LCP, hydration | Inline critical CSS, defer non-critical JS, server-side or static rendering, font-display strategy |

**INP.** An interaction's latency has three parts: input delay (main thread busy when the user interacts), processing time (the event handlers themselves), and presentation delay (rendering the next frame). Find the slow interactions from field attribution, reproduce them with a trace, and:

- Reduce input delay by breaking up long tasks during load and idle (third-party scripts, hydration, timers), yielding to the main thread between chunks of work, and deferring non-essential work.
- Reduce processing time by doing less in handlers: show visual feedback first, then do the heavy work after yielding; debounce; avoid synchronous layout reads after writes (layout thrashing); move heavy computation to a web worker.
- Reduce presentation delay by keeping DOM size reasonable, avoiding large re-renders triggered by small state changes, and using CSS containment or virtualization for long lists.

Framework-specific causes are common: re-rendering large component trees on every keystroke, expensive hydration of the whole page, large state stores triggering broad updates.

**CLS.** Identify which elements shift and why (devtools highlights layout shift regions; RUM attribution names the element). Usual causes and fixes:

- Images, video, iframes, and ad slots without reserved space: set `width`/`height` attributes or `aspect-ratio`, and reserve space for ads and embeds.
- Content injected above existing content (banners, consent notices, "load more" above the fold): reserve space or insert below, or overlay.
- Web fonts swapping and changing text metrics: use fallback font metric overrides (`size-adjust`, `ascent-override`) or a well-matched fallback, preload key fonts.
- Animations of layout properties (top, height): animate `transform` and `opacity` instead.
- Late-loading client-rendered components that change size.

Shifts within 500 ms of a user input are excluded from CLS, but unexpected shifts during interaction still frustrate users.

**TTFB** on its own: check server timing (`Server-Timing` headers help), cache hit ratio at the CDN, cold starts on serverless platforms, and geographic distance. Back-end slowness is diagnosed with `performance-optimization` and `observability`.

### Reading a performance trace

The waterfall shows the network; the trace shows what the browser's main thread did with it. In a devtools performance recording (with CPU throttling on):

- **Find long tasks** (marked when over 50 ms). Expand them: is the time in script evaluation, a specific function, style recalculation, layout, or paint? The bottom-up and call-tree views attribute time to functions and source files, which tells you whose code it is (your bundle, a framework, a third party).
- **Look at the period between FCP and LCP,** and between page load and the first likely interaction. Large blocks of script here are hydration, framework boot, or third-party initialization.
- **Watch for forced synchronous layout** (layout triggered inside script, often flagged with a warning): reading `offsetHeight` or `getBoundingClientRect` right after changing styles forces the browser to compute layout early, and repeated in a loop it becomes layout thrashing.
- **Check the frames track** during interactions and scrolling for dropped frames.
- **Record an interaction:** start recording, perform the slow interaction (type in the search box, open the menu), stop. The interactions track shows input delay, processing, and presentation per interaction, which lets you reproduce what field INP attribution reported.

### Worked reasoning: a slow LCP

Field data: product pages, mobile, LCP at the 75th percentile is 4.6 s. TTFB at the 75th percentile is 0.7 s, so the server is not the main problem.

The lab trace on a throttled mid-range profile shows the LCP element is the main product image. Its request starts at 2.9 s. The waterfall explains why: the image URL is set by a gallery component after its JavaScript bundle (420 KB compressed) downloads, parses, and runs. The image itself is a 380 KB JPEG at 2000 px wide displayed at 400 CSS px.

Breakdown: TTFB ~0.7 s, load delay ~2.2 s, load duration ~0.9 s, render delay small. The largest part is load delay, so the first recommendation is to render the first gallery image as a plain `img` in the server HTML with `fetchpriority="high"` and correct `srcset`/`sizes`, leaving the gallery script to enhance it later. Second, serve responsive AVIF/WebP variants through the existing image CDN, cutting load duration. Third, code-split the gallery so its script does not compete with the image.

Estimated effect: the request would start near the end of HTML parsing (well under 1 s) and transfer a fraction of the bytes, putting the 75th percentile LCP plausibly under 2.5 s. Confidence: moderate, from the trace; confirm with a lab before/after and RUM after release.

Notice the sequence: field data finds the problem, the breakdown points to the part, the waterfall and trace explain the cause, and the recommendation targets that cause with an estimate and a verification step.

### Single-page apps and navigations

Core Web Vitals were designed around full page loads. In single-page apps, most navigations after the first are client-side ("soft navigations"), which traditional LCP does not measure, though INP and CLS accumulate over the whole page lifetime, so a long session with many slow interactions shows up in INP. Check the current status of soft-navigation measurement in browsers and RUM tools. Meanwhile, measure route transitions with custom timing (User Timing marks from navigation start to the new view's key content rendered) and treat them as product metrics.

### Low-end devices and constrained networks

Mid-range and low-end Android phones dominate in many markets, and their CPUs can be several times slower than a recent laptop. JavaScript-heavy sites that feel fine on developer hardware can be unusable there. If analytics shows such users, test on a real low-end device or with heavier CPU throttling, and give extra weight to JavaScript reduction. Respect data-saving signals where available, and avoid autoplaying video and heavy images on cellular connections.

### 6. Check the common culprits

Beyond the per-metric diagnosis, scan for these, which recur across most sites:

- **Images:** oversized dimensions, legacy formats, no responsive variants, lazy loading of above-the-fold images (bad) or eager loading of everything below (wasteful), missing dimensions.
- **Fonts:** too many families and weights, no subsetting, late discovery, blocking text render without a fallback. Self-hosting can remove a third-party connection; `font-display` controls the swap behavior. Variable fonts can replace several files.
- **JavaScript:** bundle size per route, unused code (the devtools coverage panel shows it), large dependencies for small features, polyfills shipped to modern browsers, everything bundled into one entry instead of split by route, hydration of mostly-static content. Bytes of JavaScript cost far more than bytes of images because they must be parsed, compiled, and executed, which is slow on low-end devices.
- **CSS:** large unused stylesheets blocking render, CSS-in-JS runtime cost.
- **Third parties:** each one's main-thread time and bytes. Tag managers accumulate tags nobody remembers adding. Question every tag; load the rest after the page is interactive, or with facades (a static placeholder that loads the real chat widget or video embed on interaction).
- **Caching:** long-lived immutable caching for fingerprinted assets, sensible revalidation for HTML, CDN in front of static and, where possible, dynamic content. Check the back/forward cache (bfcache) eligibility, since instant back navigation is a large real-world win and is often blocked by `unload` handlers or `Cache-Control: no-store`.
- **Resource hints:** `preconnect` to critical third-party origins, `preload` for late-discovered critical resources (sparingly: preloading too much competes with what matters), speculation rules or prefetch for likely next navigations.
- **Rendering strategy:** client-side rendering of content that could be server-rendered or static.

### Delivery and server checklist

Much of loading performance is decided before the browser runs anything. Check:

- **Compression:** Brotli (or at least gzip) on HTML, CSS, JavaScript, JSON, and SVG. Images and video are already compressed; do not double-compress.
- **Protocol:** HTTP/2 or HTTP/3 enabled at the edge; legacy workarounds from HTTP/1.1 (domain sharding, aggressive concatenation, sprite sheets) can now hurt.
- **CDN coverage:** static assets served from a CDN near users; HTML cached at the edge where content allows (even a short cache with stale-while-revalidate helps), with personalization moved to client-side or edge logic where feasible.
- **Cache headers:** fingerprinted assets with long `max-age` and `immutable`; HTML with revalidation; no accidental `no-store` on everything.
- **Connection setup:** number of distinct origins on the critical path; TLS configuration; `preconnect` for the one or two unavoidable critical third-party origins.
- **Early hints and streaming:** where the platform supports it, 103 Early Hints or streaming the head of the HTML early lets the browser start fetching critical resources while the server finishes rendering.
- **Redirect chains** on common entry URLs (with and without `www`, trailing slashes, locale redirects, marketing links).
- **Origin performance:** cold starts on serverless functions, database calls on every request, missing application caching. Measure with server timing and hand off to `performance-optimization`.

### Estimating impact before building

Stakeholders will ask "how much faster?" before approving work. Estimate from evidence rather than guessing:

- From a trace, compute the delay a fix removes: if the LCP request starts 2.2 s after TTFB because it waits on a script, moving it into HTML removes most of that 2.2 s, minus the time needed to parse the HTML up to the image.
- For byte reductions, divide saved bytes by the effective throughput of the throttling profile, and remember that only bytes on the critical path matter for LCP.
- For main-thread work, the time of the removed or deferred tasks in a throttled trace is an upper bound on the INP or TBT gain.
- Use local overrides (devtools can override responses with edited files) or a test deployment to try the change in the lab before committing to it. This turns an estimate into a measurement cheaply.
- State ranges and confidence, never a single precise promise; field results depend on the user mix.

### 7. Prioritize recommendations

For each candidate fix, estimate:

- **Impact:** which metric, by roughly how much, on which templates, for what share of traffic. Use the trace to justify the estimate ("the LCP image starts at 2.1 s because it is injected by the carousel script; moving it to HTML should start it near 0.6 s").
- **Effort and risk:** configuration change, code change, architecture change, vendor negotiation.
- **Confidence:** measured, estimated from trace, or speculative.

Then order: quick wins (high impact, low effort) first, then structural changes with large impact, then minor polish. Group by owner (infrastructure, front-end, content/marketing for images and third-party tags) so each team knows its list.

### 8. Write the report

A good report usually contains, in whatever form suits the audience:

- **Summary:** current state in plain terms (e.g. "On mobile, product pages load their main image in about 4.2 s for the slowest quarter of visits; the target is 2.5 s"), the top three to five recommendations, and expected outcome.
- **Method:** data sources, date ranges, devices and throttling, tools and versions, pages tested, number of runs.
- **Findings by template or journey,** each tied to evidence: a waterfall excerpt, a trace observation, field percentile.
- **Prioritized recommendations** with impact, effort, owner, and how to verify.
- **Budgets and monitoring** proposal so gains are not lost.

Avoid leading with a lab score. Scores compress many metrics with weights that change between tool versions; they are useful for tracking a page over time in the same setup, not as a goal.

### 9. Verify improvements

- Measure before and after in the same lab configuration, multiple runs, and confirm the change moved the metric it was meant to move.
- Confirm in field data afterwards. CrUX takes up to 28 days to fully reflect a change; RUM shows it within days. Watch for regressions in other metrics (e.g. deferring a script may improve LCP but delay an interaction).
- For A/B-testable changes, measuring business outcomes (conversion, bounce, engagement) alongside metrics makes the case for further work. See `experiment-design`.

### 10. Set budgets and guardrails

Performance degrades by default as features accumulate. Recommend:

- **Budgets** per template: metric budgets (LCP, INP, CLS at the 75th percentile in the field), and resource budgets that are easier to enforce in CI (JavaScript kilobytes per route, image weight, number of third-party requests).
- **CI checks:** Lighthouse CI or similar on key pages with assertions, bundle-size checks on pull requests. Lab checks in CI are noisy; use median of several runs and thresholds with some margin.
- **Monitoring:** RUM dashboards with alerts on regressions per template, reviewed after each release.
- **Process:** a review step for adding third-party tags; performance acceptance criteria for new features.

## Decision guidance

**Lab vs field disagreement.** If lab looks good and field looks bad, the lab setup is not representative (device, network, location, cache state, logged-in content, personalization, ads that only appear for real users, consent banners) or the problem is in interactions the lab does not perform. If lab looks bad and field looks good, users may be on faster devices than the throttling profile, or have warm caches; still fix lab-identified issues that affect the slowest users.

**Lighthouse score vs Core Web Vitals.** Search ranking and real experience use field Core Web Vitals, not the lab score. Optimize the field metrics; use the lab score as a diagnostic.

**Server-side rendering vs client-side rendering vs static.** Static or edge-cached HTML gives the best TTFB and LCP for content that is the same for many users. Server rendering helps LCP for dynamic content but adds server time and can create hydration cost (INP risk). Client-side rendering delays meaningful content behind JavaScript download and execution and usually hurts LCP on mobile. Recommend the change only when the evidence shows rendering strategy is the bottleneck, since it is expensive.

**Preload or not.** Preload a resource when it is critical for the first render and discovered late. Do not preload everything; preloads compete for bandwidth and can delay the HTML-discovered resources that matter.

**Remove a third party or defer it.** Remove if nobody can name its business value. Defer or use a facade if it is needed but not for the first view. Keep and optimize (self-host, reduce configuration) only for scripts essential to the page's function.

### Fixes that backfire

Some popular optimizations make things worse when applied without evidence:

| Change | How it backfires | Apply when |
|---|---|---|
| Lazy-load all images | LCP image loads late | Only below-the-fold images |
| Preload many resources | Competes with critical requests; HTML-discovered resources slow down | One or two late-discovered critical resources |
| Inline all CSS | HTML grows, nothing cached across pages | Only critical above-the-fold CSS, small |
| Delay all JS until interaction | First interaction is very slow (bad INP), features broken until then | Truly non-essential third parties, with facades |
| Bundle everything into one file | Every route downloads everything | Rarely; split by route and load on demand |
| Split into hundreds of tiny chunks | Request overhead, waterfalls of dynamic imports | Balance: route-level plus a few shared chunks |
| Aggressive image compression | Visibly degraded product imagery, lost conversions | Tune quality per image type; review visually |
| `font-display: swap` without fallback tuning | Large layout shift when the font arrives | Pair with metric-matched fallbacks |

## Discovering context

- Find the framework, rendering mode, build tool, and hosting/CDN; recommendations must fit them (e.g. image components and font loaders built into the framework, CDN image transformation features).
- Look for existing performance budgets, Lighthouse CI configs, RUM tools, and past audits.
- Check analytics for the device and network mix and the highest-traffic templates.
- Identify who owns third-party tags (often marketing) and content images (often editors), because many fixes are organizational.
- Respect design and brand decisions; propose performance-friendly alternatives (a static hero instead of an autoplay video on mobile) rather than unilaterally removing features.

## Pitfalls

- **Chasing the score.** Gaming lab metrics (e.g. delaying all scripts until user interaction so the lab sees nothing) can make real experience worse, especially INP.
- **Testing on a fast machine and network** without throttling, then reporting the site is fast.
- **Single runs.** Lab variance of 10–20% between runs is normal; one run proves nothing.
- **Generic checklists.** Recommending a CDN for a site already behind one, or lazy loading for a site whose problem is TTFB.
- **Lazy-loading the LCP image.** A common regression from blanket lazy loading.
- **Ignoring third parties** because "we don't control them." You control whether and how they load.
- **Only testing the home page.** Product, article, and search pages usually carry most traffic and most problems.
- **Ignoring INP because the lab cannot measure it.** Lab TBT is a weak proxy; use field attribution.
- **Over-preloading and over-prioritizing,** which reshuffles the queue without shortening it.
- **Forgetting the repeat visit and navigation:** caching, bfcache, and prefetching often matter more for multi-page journeys than first-load tweaks.
- **No verification in the field,** so nobody knows whether the work helped.

## Quality bar and verification

- [ ] Current Core Web Vitals definitions and thresholds confirmed or stated.
- [ ] Field data examined (or its absence stated), segmented at least by mobile/desktop and template.
- [ ] Lab tests use realistic throttling, multiple runs, cold and warm cache.
- [ ] Each failing metric is broken into its sub-parts, and recommendations target the largest part.
- [ ] Every recommendation cites evidence and estimates impact, effort, and confidence.
- [ ] Recommendations are ordered and grouped by owner.
- [ ] Third-party cost has been quantified, not just mentioned.
- [ ] A verification plan (lab before/after and field follow-up) and a budget/monitoring proposal are included.
- [ ] Nothing recommended harms accessibility or functionality (e.g. removing focus styles, breaking keyboard access by deferring scripts that make controls work).
