---
name: website-and-landing-pages
description: >-
  Build content-first websites and marketing pages: define the goal and
  audience, structure pages and visual hierarchy around one primary action,
  write or place real content before styling, choose static vs CMS vs
  framework by who edits it and how often, and ship it fast, responsive,
  accessible and indexable, with working forms and analytics. Visual direction
  is derived from the brand and audience, never a default look. Use when asked
  for a landing page, homepage, marketing site, product or launch page,
  portfolio, small-business or event site, waitlist page, or a redesign of an
  existing site. Not for web applications with accounts and app logic
  (full-stack-app-build), documentation portals (documentation-site), or deep
  SEO strategy (seo).
metadata:
  category: app-generation
  related: copywriting, seo, visual-design, layout-and-responsive-design, accessible-design, information-architecture, frontend-development, web-performance-audit, ux-writing, documentation-site, design-systems
---

# Websites and Landing Pages

## Purpose and scope

This skill covers sites whose job is to **communicate and convert**: a landing page that gets sign-ups, a product site that explains and sells, a small-business site that brings in enquiries, a portfolio that wins work, an event page that gets registrations. The deliverable is a published-ready site that loads fast, reads well on every screen, works with a keyboard and a screen reader, can be found by search engines, and moves the intended visitor toward the intended action.

Boundaries:

- Applications with logged-in users, data and workflows: `full-stack-app-build`.
- Documentation and knowledge bases: `documentation-site`.
- Writing the persuasive text itself in depth: `copywriting`; interface microcopy: `ux-writing`.
- Search strategy, keyword research and technical SEO beyond the basics here: `seo`.
- Visual identity work (creating a brand): `visual-design`. This skill applies a direction; it does not invent a brand from nothing without saying so.
- Measuring and fixing an existing site's speed in depth: `web-performance-audit`.

## Core principles

1. **One page, one job.** Every page has a primary goal (sign up, buy, book, contact, download, learn) and a primary audience. Why: pages that try to serve every visitor and every action end up serving none; hierarchy is impossible without a top priority.

2. **Content before layout, layout before decoration.** Write or gather the real headline, value proposition, proof and calls to action before designing around them. Why: designs built on placeholder text break when real content arrives — headlines are longer, proof is thinner, images have the wrong aspect ratio — and the design ends up dictating what the business says.

3. **Visual direction comes from the brand and the audience.** Colours, type, imagery, density and tone are derived from existing brand assets, the audience's expectations and the offer's character. Why: a default look makes every site interchangeable and signals "template" — exactly what a marketing page cannot afford. A law firm, a children's art class and a developer tool should not look alike.

4. **Fast is a feature, and the default is slow.** Every image, font, script and third-party tag costs load time, and load time costs visitors. Why: most visitors to a landing page are first-time, often on mobile networks; they leave before a slow page renders.

5. **Accessible by construction.** Semantic HTML, sufficient contrast, keyboard operation and meaningful text alternatives from the first commit. Why: retrofitting accessibility is harder than building it in, inaccessible pages exclude real customers, and in many jurisdictions it is a legal requirement.

6. **The editor is a user too.** Choose the build approach by who will change the content, how often, and with what skills. Why: a beautiful site the owner cannot update goes stale, and a stale site loses trust.

7. **Measure the goal.** If the page exists to get sign-ups, sign-ups must be counted, attributable and checked. Why: without measurement, every future change is a guess.

## Process

### 1. Establish goal, audience and offer

Find out, or ask (see `clarify-requirements`):

- **Primary goal** and the single primary action. Secondary actions, if any, in priority order.
- **Audience.** Who arrives, from where (search, ads, social, email, word of mouth, a QR code), knowing what, on what device, with what doubts?
- **Offer.** What exactly is being offered, at what price or commitment, and why this rather than alternatives?
- **Proof available.** Testimonials, logos, numbers, reviews, case studies, awards, guarantees — real ones only.
- **Brand assets.** Logo files, colours, typefaces, photography, illustration style, tone-of-voice guidance, existing site. Ask for them explicitly; they are the source of the visual direction.
- **Constraints.** Domain and hosting, who edits content, languages, legal requirements (privacy notice, cookie consent, accessibility standard, regulated claims), launch date.
- **Success metric.** Conversion rate, number of enquiries, sign-ups, bookings.

When the brand is thin or absent, say so and derive direction from the audience and offer (step 4) rather than reaching for a familiar style. Offer the user two or three distinct directions with a reason for each if the choice is genuinely open.

### 2. Discover what exists

For a redesign or addition to an existing site:

- Inventory the current pages, their traffic if available, and which pages rank in search or receive inbound links. Breaking these URLs loses search equity and bookmarks; plan redirects for every changed URL.
- Note the current stack, CMS and hosting, and who maintains them.
- Extract the existing design tokens (colours, type scale, spacing) and components if a design system exists — follow it unless the brief is to replace it.
- Check analytics, forms and integrations (CRM, email marketing, booking tools) currently wired in, so nothing silently stops working at launch.
- Look at the traffic sources and devices in analytics, if available: they tell you which viewport and which visitor intent to design for first.
- Read the existing copy and support questions or reviews; the customers' own words are the best source for headlines and objections.
- Check for legal and compliance pages and statements already in use (privacy, accessibility, regulated disclaimers) that must be preserved.
- For a new site in an existing organisation, look at sibling properties (the product, the app, other sites) so the new one feels like the same organisation.

### 3. Structure the content

Decide the sitemap and, for each page, the content order. See `information-architecture` for larger sites.

For a landing page, the visitor's questions arrive roughly in this order, and the page answers them in turn:

1. **What is this, and is it for me?** Headline and supporting line stating the outcome for the visitor, in their language. Primary call to action visible without scrolling on common screens.
2. **Why should I believe it?** Proof close to the claim: a recognisable logo strip, a specific number, a short testimonial with a real name.
3. **How does it work / what do I get?** Benefits tied to features; a short sequence or a visual that makes the offer concrete.
4. **What about my objection?** Address the top doubts directly: price, effort, risk, compatibility, trust. FAQs work well here.
5. **What does it cost / what happens next?** Pricing or the next step, stated plainly.
6. **Final call to action**, repeating the primary action.

This is a common order, not a template — reorder for the audience. A visitor from a price-comparison ad wants pricing sooner; a visitor who already knows the brand needs less explanation and more direct action.

For multi-page sites, keep navigation short (typically five to seven top-level items), label items with the words visitors use, and ensure every page has a clear next step rather than a dead end.

Write real copy now, or obtain it from the user. Where you must draft, draft specifically (see `copywriting`): concrete outcomes, numbers where true, the customer's words. Never invent testimonials, statistics, client logos, awards or reviews; leave clearly marked gaps for the user to fill instead.

### 4. Derive the visual direction

Inputs, in priority order:

1. Existing brand guidelines and assets.
2. An existing site or product the page must feel continuous with.
3. The audience's expectations and the offer's character (formal or playful, premium or accessible, technical or emotional, calm or energetic).
4. The content itself: image-heavy offers need room for imagery; data-heavy offers need excellent tables and type.

Translate these into decisions on: type choices and scale, colour roles (background, text, primary action, accents, states), spacing rhythm and density, imagery style, shape language (corners, borders, shadows), and motion (if any). Define them as tokens (CSS custom properties or the project's equivalent) so they are consistent and changeable.

Checks on the direction:

- The primary call to action is the most visually prominent interactive element on the page.
- Text and background colours meet contrast requirements (WCAG AA as a minimum: 4.5:1 for body text, 3:1 for large text and UI components).
- The direction would look wrong for a different, unrelated business. If it would fit anyone, it is a default, not a direction.

See `visual-design` and `ui-design-fundamentals` for depth.

### 5. Choose the build approach

| Approach | Choose when | Watch out for |
|---|---|---|
| Hand-written static HTML/CSS | One to a few pages; a developer maintains it; maximum speed and longevity | Repetition across pages; non-developers cannot edit |
| Static site generator (e.g. Eleventy, Hugo, Astro, Jekyll) | Several pages or a blog; developers or technical editors; content in files | Build step and toolchain to maintain |
| Static generator plus a headless CMS | Non-technical editors need to update content regularly; developers own the templates | CMS cost, content modelling, preview workflow |
| Traditional CMS (e.g. WordPress and similar) | Non-technical owners, frequent updates, plugin ecosystem needed, hosting already in place | Plugin bloat, security updates, theme-induced slowness |
| Hosted website builder | Owner wants full self-service, no developer involved, standard needs | Limited control over performance, markup and portability |
| Application framework (e.g. React-, Vue- or Svelte-based meta-frameworks) | The site is part of a larger web app, or needs heavy interactivity, personalisation or shared components with the product | Shipping unnecessary JavaScript to content pages; use static or server rendering for them |

Decide by: who edits, how often, technical skill of editors, existing hosting and stack, need for interactivity, and budget. Do not reach for an application framework for a five-page brochure site unless one of its conditions applies. If the project already has a stack, use it.

### 6. Build

**Markup and structure**

- Semantic HTML: one `h1` per page, logical heading order, landmarks (`header`, `nav`, `main`, `footer`), lists for lists, buttons for actions and links for navigation.
- Mobile-first, fluid layouts (see `layout-and-responsive-design`). Test at narrow phone widths, tablets, laptops and wide screens; content should reflow, never require horizontal scrolling, and line lengths should stay readable on wide screens.
- Touch targets large enough to tap reliably and spaced apart.
- Respect user preferences: reduced motion, and dark mode if the brand supports it.

**Images and media**

- Correct format for the content (modern compressed formats with fallbacks where needed; vector for logos and icons).
- Responsive sizes (`srcset`/`sizes` or the framework's image component) so phones do not download desktop images.
- Explicit width and height (or aspect ratio) to prevent layout shift.
- Lazy-load below-the-fold images; do not lazy-load the main above-the-fold image.
- Meaningful `alt` text for informative images; empty `alt` for decorative ones.
- Video: no autoplay with sound; captions; a poster image; consider whether a video is needed at all.

**Fonts**

- Limit families and weights; each costs a download.
- Use `font-display` behaviour that shows text promptly; preload only the critical face; consider system fonts where they fit the direction.

**Scripts and third parties**

- Ship as little JavaScript as the page needs. Content pages often need almost none.
- Every third-party tag (analytics, chat widgets, heatmaps, embeds, ad pixels) costs performance and privacy. Include only those with a stated purpose, load them deferred, and list them for the privacy notice.

**Forms**

- Ask only for what is needed; every extra field reduces completion.
- Visible labels (not placeholder-only), correct input types and `autocomplete` attributes, clear required markers.
- Validate on the server as well as in the browser; show errors next to fields, in text, and announce them to assistive technology.
- Spam protection that does not punish humans: honeypot fields, rate limiting, server-side checks; use challenge services only if needed and accessibly.
- A clear success state and, where appropriate, a confirmation email.
- Decide where submissions go (email, CRM, spreadsheet, form service) and **test that they arrive**.
- Consent: if submissions add people to a marketing list, ask explicitly with an unticked box, and link the privacy notice.

**Performance budget**

Set a budget before building and check against it, because performance erodes one reasonable addition at a time. Starting points to adapt (not laws):

- Largest contentful paint comfortably under about 2.5 seconds on a mid-range phone over a throttled mobile connection.
- Cumulative layout shift near zero (under about 0.1).
- Interactions responding within about 200 ms.
- Total transfer for a landing page in the low hundreds of kilobytes before images below the fold; be suspicious of anything approaching several megabytes.
- Third-party scripts: each one justified in writing.

If a requested feature would break the budget (a background video, a heavy chat widget), say so, offer a lighter alternative (a poster image with a play button; a link to a contact page), and let the user decide.

### 7. SEO basics

Enough to be found and shared; see `seo` for strategy.

- Unique, descriptive `<title>` and meta description per page, written for humans.
- Clean, readable URLs; one canonical URL per page; redirects for any changed URLs.
- Headings that reflect the content structure and use the words the audience searches for.
- Crawlable content: important text in HTML, not only inside images or client-rendered after load.
- `sitemap.xml` and a `robots.txt` that does not accidentally block the site (staging sites often ship `Disallow: /` to production).
- Open Graph and social card metadata so shared links render with a title, description and image.
- Structured data where it fits the content (organisation, local business, product, event, FAQ) — only describing what is genuinely on the page.
- Language attribute on the `html` element; `hreflang` for multilingual sites.
- Fast, mobile-friendly pages — performance and usability are ranking inputs.

### 8. Analytics and measurement

- Track the primary conversion as an explicit event (form submitted successfully, not button clicked).
- Preserve campaign attribution (UTM parameters) through to the conversion where the tools allow.
- Choose analytics proportionate to need; privacy-friendly options exist. Where the law requires consent for cookies or tracking, implement a consent mechanism that actually blocks non-essential tags until consent, with rejecting as easy as accepting.
- Verify events fire, once, on the correct action, in a real browser.

### 9. Verify before launch

Run through, on the built site rather than in your head:

- **Content**: every placeholder replaced; no invented claims; spelling and names checked; prices and dates current; legal pages present (privacy, terms, imprint where required).
- **Links**: no broken internal or external links; the logo links home; email and phone links work.
- **Forms**: submit each one for real (to a test destination) and confirm arrival, success state, error states and confirmation email.
- **Responsive**: check at several widths and on at least one real phone if possible; landscape too.
- **Accessibility**: keyboard-only navigation through the whole page with a visible focus indicator; screen reader pass on the main path; automated checker for contrast, labels and alt text — automated tools catch only part of the problems (see `accessibility-audit`).
- **Performance**: run a lab test (e.g. Lighthouse or WebPageTest) on a throttled mobile profile; look at the largest content paint, layout shift and interaction responsiveness, and the total page weight. Fix the largest contributors first (usually images, fonts and third-party scripts). See `web-performance-audit`.
- **SEO**: titles and descriptions present; `robots.txt` and meta robots allow indexing on production; sitemap reachable; social card renders in a preview tool.
- **Browsers**: current versions of the major engines; no console errors.
- **Analytics**: conversion event fires once on success.
- **Redirects** from old URLs in place for a redesign.
- **Security basics**: HTTPS everywhere, no secrets in client code, form endpoints protected from abuse, CMS and plugins updated.

If you can run a browser, do these checks yourself; otherwise give the user the checklist and say which items you could not verify.

### 10. Launch and hand over

- Do not change DNS, publish, or switch a live site without the user's explicit go-ahead.
- Provide: how to edit content, how to deploy, where forms go, which third-party services are used and why, analytics access, and the list of open items.
- After launch, check the live site once more: forms, analytics, indexing directives, redirects and HTTPS.

## Decision guidance

### Single long page vs. multiple pages

| Single page | Multiple pages |
|---|---|
| One offer, one audience, one action | Several offers, audiences or depths of information |
| Paid traffic to a focused campaign | Organic search across many topics |
| Short buying decision | Long consideration, comparison, documentation |

### Site types and what each needs most

| Site type | The job | Needs most | Common mistake |
|---|---|---|---|
| Campaign landing page | Convert one audience from one traffic source | Message match with the ad or email that sent them; one action; no navigation leaks | Linking to the whole site and losing the visitor |
| Product / SaaS marketing site | Explain, differentiate, convert to trial or demo | Clear category and outcome, proof, pricing clarity, comparison and objection handling | Feature lists without outcomes; hidden pricing without reason |
| Local or small business | Get calls, bookings or visits | Name, what you do, where, hours, phone and booking above the fold; local business structured data; maps | Beautiful imagery, no phone number on mobile |
| Portfolio | Win work or a job | Curated best work with context (problem, role, result), easy contact | Showing everything; images with no explanation |
| Event | Register attendees | Date, time with timezone, place or link, agenda, speakers, price, registration — up front | Missing timezone; registration buried |
| Waitlist / pre-launch | Measure and capture interest | Clear promise, short form, honest timeline, confirmation | Implying the product exists |
| Nonprofit / cause | Inform and drive donations or volunteering | Emotional clarity, trust signals, frictionless giving, impact proof | Donation flow that leaves the site with no reassurance |

### Content modelling for a CMS

When non-technical editors will change content, model it so they cannot break the design:

- Model content types by meaning (testimonial, team member, service, event), not by layout ("left column block").
- Give fields constraints that match the design: character guidance for headlines, required alt text for images, image aspect ratios, limited rich-text options.
- Provide a preview of the real page before publishing.
- Keep page-builder freedom proportionate: total freedom produces off-brand pages; no freedom produces developer tickets for every change.
- Document editing tasks the owner will do often (change a price, add a testimonial, post an update) step by step.

### Multilingual sites

- Decide the URL strategy (subdirectories, subdomains or separate domains) once, and add `hreflang` annotations between equivalents.
- Design for text expansion; some languages run substantially longer than English, and some read right-to-left — use logical CSS properties so layouts mirror correctly.
- Translate metadata, alt text, form messages and legal pages, not only body copy.
- Let visitors choose a language; do not force it from IP location alone.

### How much interactivity

Interactive elements (calculators, configurators, demos) earn their cost when they make the offer concrete for the visitor. Carousels, scroll-jacking and animated counters usually do not: they hide content, distract and slow the page. Prefer showing the content plainly. See `interaction-design` and `motion-design` for when motion helps.

### Above-the-fold priorities

The opening viewport should answer "what is it and is it for me" and expose the primary action. It does not need to contain everything; people scroll when the top earns it. Do not cram the whole page into the first screen.

## Redesigns and migrations

Redesigning an existing site carries risks a new site does not:

- **Map every old URL** to its new equivalent (or the closest relevant page) and implement permanent redirects. Pages with inbound links and search traffic are the priority.
- **Carry over what works.** Pages and messages that convert well today are evidence; do not rewrite them on taste alone.
- **Freeze content** shortly before launch or plan a content sync, so edits made on the old site are not lost.
- **Replicate integrations**: analytics IDs, form destinations, CRM hooks, tracking used by marketing, verification files for search consoles.
- **Compare before and after**: performance, accessibility and conversion. Launch is the start of measurement, not the end.
- **Keep a rollback** — the ability to point the domain back to the old site for a period if something critical breaks.

## Worked reasoning

Illustrative only: the reasoning is the point.

**Request:** "Landing page for our physiotherapy clinic's new sports-injury programme. We'll run local social ads."

- Goal: booked initial assessments. Audience: local amateur athletes, mostly on phones, arriving from an ad that promised a fast return to training. Doubts: cost, whether insurance covers it, whether it works for their injury, how soon they can be seen.
- Structure: headline echoing the ad's promise in plain words; booking button and phone number immediately; short proof (real outcomes or reviews the clinic provides — none invented); how the programme works in three concrete steps; who it is for and not for; prices and insurance; practitioner credentials; FAQ; booking again; address, map and hours.
- Visual direction: from the clinic's existing logo and colours; imagery of real staff and space if available, because trust in a local health service depends on seeing the actual people; calm and clear rather than flashy, since the audience is in pain and wants reassurance. Contrast checked against the brand colours, adjusting shades if the brand's primary colour fails on white.
- Build: the clinic already uses a hosted builder for their main site and staff edit it — build within it if it can meet performance and accessibility needs; otherwise a small static page with the booking tool's embed, and explain the trade-off.
- Measurement: booking completions from the ad's campaign parameter; phone taps as a secondary event.
- Compliance flags for the user: health claims must be accurate; reviews must be genuine; privacy notice for any booking data.

**A different request** — "a homepage for our open-source database tool" — would lead through the same steps to different answers: developers as audience, a code sample or benchmark as proof, documentation links as a key secondary action, a direction derived from the project's existing identity and community.

## Pitfalls and anti-patterns

- **The default look.** Same hero, gradient, card grid and stock illustrations as a thousand other sites. Derive direction from the brand and audience.
- **Lorem ipsum design.** Layouts that collapse when real content arrives. Use real or realistic content from the start.
- **Fabricated proof.** Made-up testimonials, logos, numbers or awards. This misleads customers and can breach consumer-protection law. Leave gaps instead.
- **Vague headline.** Clever or abstract phrasing that does not say what the thing is. Test: could a stranger say what is offered after five seconds?
- **Competing calls to action** of equal weight. Pick one primary.
- **Heavy hero media.** A multi-megabyte video or image above the fold that delays the first meaningful render on mobile.
- **JavaScript-rendered content** for pages that could be static, slowing first render and risking poor indexing.
- **Forms that go nowhere.** Submissions sent to an unmonitored inbox, a misconfigured endpoint, or lost entirely. Test end to end.
- **Accessibility as an afterthought**: low-contrast grey text, placeholder-only labels, icon-only buttons without names, focus outlines removed.
- **Staging settings in production**: `noindex`, `Disallow: /`, test analytics IDs, debug banners.
- **Broken URLs after a redesign** with no redirects, losing search ranking and bookmarks.
- **Tag soup**: many third-party scripts nobody remembers adding, each slowing the page and collecting visitor data.
- **Cookie banners that nudge** (huge accept, hidden reject) — increasingly unlawful and erode trust.
- **Message mismatch.** The ad promises one thing, the page headline says another; visitors assume they are in the wrong place and leave.
- **Navigation leaks on campaign pages.** A full site menu on a focused landing page invites visitors away from the one action.
- **Hidden contact details.** Phone, address and email buried in a footer or an image, unreadable to screen readers and untappable on phones.
- **Generic stock imagery** that contradicts the brand's claim of being personal, local or real. Real photos of the actual people, product or place, even modest ones, usually outperform polished generic ones.
- **Ignoring the narrow viewport.** Designing at desktop width and "making it fit" on phones — while most campaign traffic arrives on phones.
- **Infinite tweaking before launch.** A page that is never live converts nobody; ship when the quality bar is met, then improve with data.
- **Unmaintainable for the owner**: a custom build handed to someone who needs to change prices weekly and cannot.

## Quality bar

- [ ] Primary goal, audience and success metric are written down, and the page hierarchy serves them.
- [ ] Visual direction is traceable to the brand, the audience and the content — and would not fit an unrelated business.
- [ ] All content is real or clearly marked as awaiting the user's input; nothing fabricated.
- [ ] Works and reads well from narrow phone to wide desktop, with no horizontal scroll.
- [ ] Keyboard and screen reader usable; contrast meets at least WCAG AA.
- [ ] Lab performance on a throttled mobile profile is good, with the largest contributors addressed.
- [ ] Each form tested end to end; submissions arrive; consent handled correctly.
- [ ] Titles, descriptions, canonical URLs, sitemap, robots, social metadata in place and production-correct.
- [ ] Conversion tracking verified in a real browser; consent respected.
- [ ] Owner can edit what they need to edit, and knows how.

## Safety and ethics

- Never publish, change DNS or overwrite a live site without confirmation.
- Never fabricate reviews, endorsements, statistics or credentials; flag regulated claims (health, finance, legal) for the user to verify.
- Collect only the personal data needed; disclose what is collected and why; secure form endpoints and storage.
- Keep API keys and form-service secrets server-side; anything in the page source is public.
- Use only images, fonts and media the user has the right to use; note licences in the handover.

## Related skills

- `copywriting` and `ux-writing` for the words.
- `visual-design`, `ui-design-fundamentals`, `layout-and-responsive-design`, `design-systems` for the look and structure.
- `accessible-design` and `accessibility-audit` for inclusion.
- `seo` and `web-performance-audit` for discoverability and speed.
- `information-architecture` for larger sitemaps.
- `frontend-development` for implementation detail.
