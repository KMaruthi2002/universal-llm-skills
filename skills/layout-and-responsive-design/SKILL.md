---
name: layout-and-responsive-design
description: >-
  Plan and build layouts that adapt to any viewport, container, input method
  and zoom level: grid systems, CSS Flexbox vs. Grid thinking (and their
  equivalents in native toolkits), intrinsic and fluid layouts, content-driven
  breakpoints, fluid type and spacing with clamp(), reflow at 320 px and 400%
  zoom, container queries, touch target sizing, safe areas, large and
  ultra-wide screens, print styles, and RTL/localisation. Use when making a
  page or app "responsive", "mobile-friendly" or "work on tablets", fixing
  overflow, horizontal scroll or layout breaking at certain widths, choosing
  breakpoints, designing a grid, or adapting a desktop design to mobile (or
  the reverse). For screen content and hierarchy use ui-design-fundamentals.
metadata:
  category: design
  related: ui-design-fundamentals, visual-design, frontend-development, accessible-design, design-systems, mobile-app-development, website-and-landing-pages, web-performance-audit, design-to-code-handoff
---

# Layout and Responsive Design

Layout is the arrangement of content in space; responsive design is making that arrangement hold up when the space changes — viewport width, container width, orientation, zoom, font size, input method, language length and output medium. The modern goal is not "a mobile version and a desktop version" but **layouts that are intrinsically adaptive**, with explicit breakpoints only where the content needs them.

This skill is about the spatial system and its behaviour. Hierarchy and component choice live in `ui-design-fundamentals`; spacing and type scales in `visual-design`; implementation details of a given framework in `frontend-development` or `mobile-app-development`.

## Core principles

1. **Content decides, devices do not.** Device widths change every year; content does not care. Add a breakpoint where *this content* starts to look or work badly (lines too long, cards too squashed, navigation wrapping), not at "iPhone" or "iPad" widths.
2. **Start from the most constrained case.** Design the narrowest, most constrained layout first (small viewport, large text, touch). It forces prioritisation; expanding a good narrow layout is easier than cramming a wide one. This is the reasoning behind "mobile first" — the principle is constraint-first, whichever device that is for your users.
3. **Prefer intrinsic over prescribed.** Let components size to their content and available space (wrapping flex rows, auto-fitting grids, `minmax()`, percentage and `fr` units) so fewer breakpoints are needed. Every fixed width is a future overflow bug.
4. **Respond to the container, not only the viewport.** A card in a sidebar and the same card in a main column face different space on the same screen. Components that adapt to their container are reusable; components tied to viewport width are not.
5. **Reflow, do not shrink.** On small screens and at high zoom, content should reorganise into a single column, not scale down or demand horizontal scrolling. WCAG 1.4.10 (AA) requires content to reflow at a width equivalent to 320 CSS px (1280 px at 400% zoom) without two-dimensional scrolling, except for content that genuinely needs it (maps, data tables, diagrams, toolbars).
6. **Respect the user's settings.** Font-size preferences, zoom, orientation (WCAG 1.3.4: do not lock orientation unless essential), reduced motion, dark mode, and text-spacing overrides must all leave the layout usable.
7. **Source order is meaning order.** Visual reordering (CSS `order`, grid placement, `row-reverse`) must not break reading and focus order for keyboard and screen reader users (WCAG 1.3.2, 2.4.3).

## Discovering context

- **Which devices and viewports do users actually use?** Check analytics if available. Also ask about embedded contexts: webviews, kiosks, TVs, in-car displays, smart watches, iframes in other products.
- **Existing grid and breakpoint conventions:** look for breakpoint variables, theme configs (e.g. a Tailwind `screens` config, SCSS maps, CSS custom properties), layout primitives (`Stack`, `Grid`, `Container` components), design-file layout grids. Use them; propose changes only with reason.
- **Platform rules:** native apps follow size classes (iOS), window size classes (Android), or effective pixels (Windows); the web follows CSS. Safe areas (notches, home indicators, rounded corners, foldable hinges) apply on mobile.
- **Browser support targets:** container queries, subgrid, `:has()`, `dvh` units and similar features are broadly supported in current evergreen browsers, but check the project's support matrix before relying on them, and provide sensible fallbacks.
- **Content variability:** shortest and longest translations, user-generated content length, image aspect ratios, number of items.

## Layout thinking

### One-dimensional vs. two-dimensional

| Need | Think in… | Web tool | Native analogues (examples) |
|---|---|---|---|
| Items in a row or column that wrap, distribute or align along one axis (toolbars, tag lists, nav bars, button groups) | One dimension | Flexbox | SwiftUI `HStack`/`VStack`, Compose `Row`/`Column`, Flutter `Row`/`Column`/`Wrap` |
| Rows and columns that must line up with each other (page layouts, card grids, forms with aligned labels, dashboards) | Two dimensions | CSS Grid (and subgrid for nested alignment) | `Grid`/`LazyVGrid`, Compose `LazyVerticalGrid`, Flutter `GridView` |
| Layers stacked on top of each other (overlays, badges, hero text on image) | Z-axis | Grid with overlapping areas, or positioning | `ZStack`, `Box`, `Stack` |

A useful rule: **Flexbox is content-out** (items decide their size, the container distributes), **Grid is layout-in** (the container defines tracks, items are placed). Most interfaces combine both: Grid for the page and major regions, Flexbox inside components.

### Grids

A grid is a set of columns, gutters and margins that gives elements shared alignment lines.

- **Column count:** 12 is common because it divides into 2, 3, 4 and 6; 4 columns on small screens and 8 on medium are frequent pairings. These are conventions, not requirements. A content-led layout might use a single reading column plus a sidebar, or named areas rather than numbered columns.
- **Gutters and margins** come from the spacing scale (`visual-design`) and usually grow with the viewport.
- **Fluid grids** (columns as fractions of available width) are the default; **fixed grids** (fixed column widths, centred) suit content with a strict measure.
- **Max content width:** constrain reading content (see measure in `visual-design`, ~45–75 characters) even on wide screens; let backgrounds, media and data surfaces extend further if useful.
- **Auto-fit grids** (e.g. columns of "at least N, otherwise share the space") handle many collections without any breakpoints.
- **Subgrid** lets nested items (card titles, prices, buttons) align across sibling cards — a frequent visual-polish problem solved structurally.

### Common layout patterns

| Pattern | Narrow behaviour | Wide behaviour |
|---|---|---|
| Stack / single column | Default | Constrain width or become multi-column |
| Sidebar + main | Sidebar moves above/below main, or becomes a drawer | Side by side; sidebar fixed or minimum width, main flexible |
| Master–detail (list + detail) | List and detail are separate screens | Both visible; detail updates in place |
| Holy grail (header, nav, main, aside, footer) | Single column in source order | Three columns |
| Card grid | One column, maybe horizontal carousel only if content is browsable | Auto-fit columns |
| Dashboard | Priority-ordered stack of widgets | Grid of widgets by priority and size |
| Split / hero | Image above or below text | Side by side |
| Data table | Horizontal scroll inside the table (allowed by 1.4.10), priority columns, or row → card transform | Full table with sticky header/first column |

### Breakpoints by content

Process for finding breakpoints:

1. Build the narrow layout with intrinsic sizing.
2. Widen the viewport (or container) slowly.
3. Note where the layout *starts* to fail: line length exceeds the comfortable measure, cards become too wide, whitespace becomes awkward, nav has room to expand, a second column would fit comfortably.
4. Add a breakpoint there, expressed in `em`/`rem` where practical so it scales with user font size.
5. Repeat. Aim for a few major breakpoints (often 2–4) plus component-level adjustments.

Expressing breakpoints in `em` units means that when a user enlarges the default font size, the layout switches to the narrower arrangement earlier — which is what they need.

## Fluid type and space

- Fluid values interpolate between a minimum and maximum across a range of widths, typically with `clamp(min, preferred, max)`.
- **Include a `rem` term in the preferred value** (e.g. a `rem` base plus a `vw` component) so text still responds to browser zoom and font-size settings. Pure `vw` type does not scale with zoom in some browsers and can fail WCAG 1.4.4 (resize text to 200%).
- Keep the max/min ratio moderate for body text (body sizes should change little); use larger ranges for display headings and section spacing.
- Fluid spacing scales (spacing values that grow with viewport) keep proportions without breakpoints.
- Container query units (`cqi`, `cqw`, etc.) allow type and space to scale with a component's container rather than the viewport.

## Container queries

Use container queries when a component appears in multiple contexts with different available widths (cards, media objects, widgets, form layouts in sidebars vs. main content).

- Declare a container (e.g. `container-type: inline-size`) on the wrapper that defines the available space.
- Write component rules against the container width: stacked when narrow, side-by-side when wide.
- Keep **viewport** media queries for page-level structure (overall grid, navigation pattern) and **user preferences** (`prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`, `forced-colors`, `pointer`, `hover`).
- Style queries and other newer features have narrower support; check before use.

Design-tool equivalent: auto layout, constraints and variants for "narrow" and "wide" component configurations; document the switch width.

## Input methods and touch targets

Do not equate "small screen" with "touch" or "large screen" with "mouse": tablets have keyboards, laptops have touchscreens, TVs use remotes, many users rely on keyboard or switch access.

- Query **capabilities** (`pointer: coarse | fine`, `hover: hover | none`) rather than width when the question is about input.
- **Hover must not be the only way** to reveal essential controls or information; touch has no hover and keyboard users need focus equivalents (see WCAG 1.4.13 for hover/focus content).

Target size guidance (state which standard you are applying):

| Source | Guidance |
|---|---|
| WCAG 2.2 SC 2.5.8 Target Size (Minimum), AA | At least 24×24 CSS px, or enough spacing that a 24 px circle centred on each target does not overlap another target; exceptions for inline links in text, equivalent controls elsewhere, user-agent controls and essential presentation. |
| WCAG 2.2 SC 2.5.5 Target Size (Enhanced), AAA | At least 44×44 CSS px. |
| Apple Human Interface Guidelines | At least 44×44 pt for touch controls. |
| Material Design | At least 48×48 dp touch targets (visual element may be smaller, with padding). |

Practical rules:

- The **hit area** can be larger than the visual element (padding, pseudo-elements); make it so for icons and small controls.
- Space adjacent targets so that mis-taps are unlikely; destructive actions should not sit next to frequent ones.
- On large phones, place frequent actions within thumb reach (lower part of the screen); place destructive or rare actions out of the easy-reach zone.
- Provide alternatives to complex gestures (WCAG 2.5.1 pointer gestures, 2.5.7 dragging movements in 2.2).

## Viewport and device specifics

- **Viewport units on mobile:** classic `vh` ignores the appearing/disappearing browser toolbar; `svh`, `lvh` and `dvh` address this. Avoid full-height layouts that cut off content or jump on scroll.
- **Safe areas:** use the platform's safe-area insets (e.g. `env(safe-area-inset-*)` on the web with `viewport-fit=cover`) so content avoids notches, rounded corners and home indicators.
- **Virtual keyboards** cover the lower part of the screen; ensure focused inputs and their submit buttons remain visible, and that fixed bottom bars do not cover fields.
- **Orientation:** support both unless essential (WCAG 1.3.4). Landscape phones have very little height; sticky headers and footers can consume most of it.
- **Foldables and dual screens:** avoid placing critical content across the hinge; treat each segment as a layout region if the platform exposes them.
- **Large and ultra-wide screens:** do not just stretch. Constrain reading measure, add columns for genuinely parallel content (master–detail, multi-panel), increase whitespace, consider larger type for distance viewing (TV/kiosk "10-foot" interfaces need much larger type and focus-based navigation).
- **Density:** high-DPI displays need appropriately sized raster assets (`srcset`, asset catalogs) or vector assets.

## Content strategies for constrained space

When space shrinks, choose deliberately among:

| Strategy | Use for | Risk |
|---|---|---|
| Reflow (stack) | Most content | Long pages; mitigate with headings and anchors |
| Prioritise (show most important, move the rest down) | Dashboards, product pages | Hiding something users need |
| Disclose (collapse into accordion, menu, "more") | Secondary content and actions | Discoverability drops sharply |
| Transform (table → cards, tabs → select, sidebar → drawer) | Complex components | Inconsistency across sizes; re-test interactions |
| Scroll within a region (horizontal) | Tables, carousels of browsable items, code | Hidden content; signpost with partial items or shadows |
| Remove | Pure decoration only | Removing content mobile users need — mobile users want the same tasks |

**Do not remove functionality on small screens** just because it is harder to lay out. Users on phones expect to complete the same tasks.

## Localisation and direction

- Text in other languages may be 30–40% longer than English for short UI strings (German, Finnish, Russian are frequent examples), and sometimes far more for very short labels; CJK may be shorter but taller. Design flexible containers; never fix widths to English text.
- **RTL languages** (Arabic, Hebrew, Persian, Urdu) mirror layout direction. Use logical properties (`margin-inline-start`, `padding-block`, `inset-inline-end`) instead of left/right so mirroring is automatic. Mirror directional icons (back arrows) but not universal ones (media play, clocks, logos).
- Vertical writing modes exist for some CJK contexts; logical properties help here too.

## Print and other media

If pages may be printed or saved as PDF (receipts, invoices, articles, documentation, tickets, reports):

- Provide `@media print` styles: remove navigation, interactive chrome and backgrounds that waste ink; ensure text is dark on light.
- Expand link URLs where useful; avoid content cut off in fixed-height or scroll containers.
- Control page breaks (`break-inside: avoid` for figures, table rows, cards) and repeat table headers.
- Use physical units sensibly and test actual printing or print preview on more than one browser.

Other media to consider when relevant: projectors (low contrast — increase it), e-ink (no color, slow refresh — avoid motion), TV (overscan, distance), embedded webviews (restricted height, no browser chrome).

## Hard components

### Data tables

Tables are the most common responsive failure. Options, in rough order of preference:

1. **Keep the table, scroll it horizontally inside its own container**, with the first column (row identity) sticky and a visible cue that more columns exist. WCAG 1.4.10 explicitly allows two-dimensional scrolling for data tables. Make the scroll container keyboard-focusable and labelled so keyboard users can scroll it.
2. **Prioritise columns:** show the most important columns at narrow widths and let users reveal others (column picker, "details" expansion per row).
3. **Transform rows into stacked cards** with label–value pairs — good for read-only lists of few attributes, poor for comparison, and it needs care to keep table semantics or an equivalent structure.
4. **Summarise** with a drill-down to detail.

Never shrink table text to fit; never let a table silently overflow the page.

### Forms

- Single column is the default at all sizes for sequential forms; widen the form only to a comfortable maximum, not to the viewport.
- Labels above fields survive narrow widths and long translations better than labels beside fields; side labels can work on wide screens for dense admin forms, switching to top labels via a container query.
- Keep action buttons near the last field; on mobile, full-width primary buttons are easier to hit, but check they still read as distinct from secondary actions.

### Navigation

- Wide: visible primary navigation (top bar or side nav). Narrow: a bottom tab bar for a few primary destinations on app-like products, or a menu button for content sites with many destinations. Test that the switch point is content-driven (where items stop fitting at the user's font size), not a guessed device width.
- "Priority+" navigation (show as many items as fit, overflow the rest into "More") adapts continuously without a hard breakpoint.

### Media

- Use `aspect-ratio` or explicit dimensions to reserve space, and `object-fit` to control cropping.
- Provide art direction where cropping changes meaning (a wide landscape photo may need a different crop on narrow screens — e.g. `<picture>` with sources, or platform asset variants).
- Video and embeds need responsive containers; avoid fixed iframe sizes.

### Sticky, fixed and layered elements

- Every sticky or fixed element (header, footer bar, cookie banner, chat bubble, floating action button) consumes viewport. Budget them: at narrow heights (landscape phones, 400% zoom) consider un-sticking headers or collapsing them on scroll.
- Define a **small set of layering levels** (base, raised, sticky, dropdown, overlay, modal, toast) instead of ad-hoc z-index values; encode them as tokens so components stack predictably (see `design-systems`).

## Worked reasoning: finding breakpoints for a card grid

Illustrative example of the method:

> Content: product cards with an image, a title of up to ~60 characters, a price and an "Add" button.
> 1. At the narrowest width, one card per row looks fine, but on medium phones the cards become very wide and the image very tall. Rather than a breakpoint, set the grid to "as many columns as fit, each at least a minimum width" — at that minimum, the title wraps to at most two lines and the button still fits beside the price.
> 2. Widening further, columns are added automatically. At very wide viewports there would be eight or more columns, making the page feel like a spreadsheet and pushing the filter sidebar far from the content. A max content width solves this without a breakpoint.
> 3. The filter sidebar needs a real breakpoint: below the width where sidebar plus two card columns fit, filters move into a disclosure above the grid. That width is expressed in `em`, so users with larger text get the stacked layout sooner.
> 4. Inside each card, a container query switches the price/button row from side-by-side to stacked when the card itself is narrow — which also handles the card appearing in a narrow "recently viewed" rail elsewhere.
>
> Result: one page-level breakpoint and one component-level container query, instead of four device breakpoints.

## Specifying responsive behaviour

A responsive specification describes rules, not snapshots. For each region or component, state:

- **Sizing rule:** fixed, fluid, intrinsic (content-sized), min/max constraints.
- **Adaptation:** what changes, at what container or viewport width (in `em`/`rem` where possible), and why.
- **Overflow:** wrap, truncate (with how the full value is reachable), scroll within region, or reflow.
- **Order:** whether order changes, confirming reading and focus order remain logical.
- **Input differences:** hover vs. touch behaviours.
- **Extremes:** behaviour at 320 px, at very wide widths, at 200% text size, with the longest expected translation.

In design tools, use auto-layout/constraint features and component variants to model this, and annotate the rest. In code, the CSS (or layout code) *is* the spec — review it for the same points.

## Responsive images and performance

Layout and performance are coupled: the wrong image for the slot is either blurry or wasteful.

- Serve **multiple resolutions** (`srcset` with width descriptors plus an accurate `sizes` attribute on the web; asset variants natively) so each device downloads what its slot needs.
- Write `sizes` from the layout: if an image is full-width on narrow screens and a third of the content width on wide screens, say so; an inaccurate `sizes` silently wastes bandwidth.
- **Do not lazy-load** the largest above-the-fold image (often the Largest Contentful Paint element); do lazy-load images below the fold.
- Reserve space for every image, embed and ad slot to prevent layout shift.
- Prefer CSS/vector for decorative shapes and icons; they scale without extra requests.
- Measure on throttled mobile connections, not office Wi-Fi (see `web-performance-audit`).

## Spacing and alignment across sizes

- Gutters, margins and section spacing typically grow with available space; component-internal spacing usually does not. Separate these two kinds of spacing in tokens (e.g. layout spacing vs. component spacing) so they can scale independently.
- Keep the **relationship** between within-group and between-group spacing at every size; shrinking everything uniformly on small screens destroys grouping.
- Alignment lines should persist when columns collapse: a single column should still align its headings, body and actions to one edge.
- Edge margins on small screens must keep content away from rounded corners and screen edges (and safe areas) — commonly at least one or two base spacing units.

## Native platform notes

- **iOS / iPadOS:** design for size classes (compact/regular width and height), Split View and Slide Over multitasking, Dynamic Type (text sizes up to very large accessibility sizes must reflow layouts), and safe areas.
- **Android:** window size classes (compact, medium, expanded), configuration changes (rotation, resizing, foldables), font scale (users commonly set larger scales; recent Android versions support nonlinear scaling up to 200%), and edge-to-edge insets.
- **Desktop apps:** windows resize arbitrarily and can be very small; define minimum window sizes deliberately and support high-DPI scaling.

See `mobile-app-development` and `desktop-app-development` for implementation.

## Process

1. **Inventory content and priorities** for the screen (from `ui-design-fundamentals`).
2. **Define the layout system:** grid or regions, spacing, max widths — reuse the project's system if it exists.
3. **Design the narrowest/most constrained case** with real content, at default and enlarged text sizes.
4. **Widen and find breakpoints** where content needs them; decide component-level (container) vs. page-level (viewport) adaptations.
5. **Specify behaviour**, not just snapshots: what wraps, what stacks, what collapses, what scrolls, what stays fixed, minimum and maximum sizes, and at which width each change happens. Static mockups at three widths do not describe the in-between.
6. **Build or prototype intrinsically** and test continuously across widths (drag the window, do not just jump between presets).
7. **Test with real conditions:** zoom, font-size settings, long strings, RTL, touch, keyboard, orientation, virtual keyboard, print.
8. **Hand off** with the behaviour spec (`design-to-code-handoff`).

## Pitfalls

- **Device-named breakpoints** ("mobile", "tablet", "desktop") that fail on everything in between.
- **Three static mockups** with no specification for intermediate widths.
- **Fixed heights** on text containers — overflow when text wraps, zooms, translates or user spacing applies.
- **Fixed pixel widths** on components that then overflow on narrow screens or in narrow containers.
- **Horizontal page scroll** caused by a single wide element (long URL, wide image, unbreakable string, table). Use `min-width: 0` on flex/grid children, `overflow-wrap: anywhere` for user content, and responsive media.
- **Viewport-only components** that break when placed in a sidebar.
- **Hover-dependent menus and tooltips** on touch.
- **`vw`-only font sizes** that ignore zoom.
- **Visual reorder that scrambles focus order.**
- **Fixed headers/footers** that eat the screen on landscape phones or at high zoom; WCAG 2.4.11 (AA, 2.2) requires focused items not be entirely hidden by such content.
- **Hiding content on mobile** "to simplify" when users need it.
- **Testing only in a desktop browser's device emulator.** Emulation does not reproduce real touch, virtual keyboards, browser toolbars or performance; test on real devices when possible.
- **Layout shift** when images, fonts, ads or async content load — reserve space (explicit dimensions, `aspect-ratio`) (see `web-performance-audit`).

## Quality bar and verification

- [ ] No horizontal scrolling at 320 CSS px width / 400% zoom except for content that requires two dimensions (WCAG 1.4.10).
- [ ] Text resizes to 200% without loss of content or function (1.4.4), and text-spacing overrides do not break layout (1.4.12).
- [ ] Breakpoints are justified by content; behaviour between breakpoints is specified and checked by continuous resizing.
- [ ] Components that appear in multiple contexts adapt to their container.
- [ ] Reading and focus order match the visual order at every size.
- [ ] Touch targets meet the chosen standard (state which: WCAG 2.5.8 24 px minimum, or 44/48 px platform guidance).
- [ ] Essential functions are available on every size and input method; nothing depends on hover alone.
- [ ] Long strings, translations, RTL, empty and overflowing content are handled.
- [ ] Safe areas, virtual keyboard and orientation are handled on mobile.
- [ ] Reading measure is constrained on wide screens; large screens use space meaningfully.
- [ ] Print styles exist where printing is plausible.
- [ ] No cumulative layout shift from late-loading media or fonts.

**How to check:** if you can run the UI, resize continuously from narrow to very wide; use browser zoom to 200% and 400%; set the browser's default font size larger; apply a text-spacing bookmarklet or stylesheet; toggle `dir="rtl"`; emulate coarse pointer and test on at least one real phone; print-preview. Automated tools (e.g. Lighthouse, axe) catch some issues (target size, layout shift, viewport meta), but most responsive failures need visual inspection. If you cannot run it, review the code/spec for fixed widths and heights, missing `min-width: 0`, device-named breakpoints, hover-only interactions and physical (left/right) properties, and list what must be checked on real devices.
