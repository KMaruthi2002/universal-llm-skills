---
name: frontend-development
description: >-
  Build client-side user interfaces in any framework or none: component design
  and composition, state management, data fetching and caching, routing, forms
  and validation, loading/empty/error states, performance, accessibility, and
  faithfully matching an existing design system. Use when implementing a
  screen, component, or feature in a web (or web-like) UI; choosing where state
  lives; wiring a UI to an API; fixing a sluggish or janky interface; building
  forms; or turning a design into working UI code. For visual and UX decisions
  use ui-design-fundamentals and interaction-design; for page-load audits use
  web-performance-audit; for whole apps use full-stack-app-build.
metadata:
  category: development
  related: ui-design-fundamentals, design-systems, accessible-design, layout-and-responsive-design, interaction-design, design-to-code-handoff, web-performance-audit, api-design, testing-strategy, end-to-end-testing
---

# Frontend Development

Frontend code lives at the most hostile boundary in software: unreliable networks, every screen size, slow devices, assistive technology, impatient humans, and a design that must be matched exactly. A frontend is good when it is **correct in every state** (not just the happy path), **fast enough on the devices people actually use**, **usable by everyone**, and **consistent with the product's existing look and patterns**.

## Scope

Covers building UI in code: components, state, data fetching, routing, forms, rendering performance, accessibility implementation, and design-system fidelity. Applies to component frameworks (React, Vue, Svelte, Angular, Solid and others), server-rendered HTML with progressive enhancement, and framework-free code. Much of it transfers to mobile and desktop UI toolkits.

Neighbours:
- What the UI should look like and why — `ui-design-fundamentals`, `visual-design`, `layout-and-responsive-design`.
- How it should behave and feel — `interaction-design`, `motion-design`.
- Accessibility requirements in depth — `accessible-design`; auditing — `accessibility-audit`.
- Building and maintaining the component library itself — `design-systems`.
- Implementing from design files — `design-to-code-handoff`.
- Measuring and fixing load performance — `web-performance-audit`.
- Browser-level end-to-end tests — `end-to-end-testing`.

## Core principles

### 1. The project's design system and conventions are the spec

A new screen that looks or behaves slightly differently from the rest of the product is a defect, even if it is "nicer". Before writing UI, find the existing components, tokens (colours, spacing, typography, radii, shadows), layout primitives, icon set, and interaction patterns, and build from them. Never invent new colours, spacing values, or one-off variants of existing components; if the system lacks something, compose from its primitives or raise the gap.

### 2. Every UI has more states than the happy path

For any view that depends on data or input, account for: initial/loading, empty, partial, populated, error (network, permission, validation, not found), stale/refreshing, offline, and very large data (long lists, long strings, many items). Most production UI bugs are a missing state. Design the states explicitly before writing markup.

### 3. State should live in exactly one place, as close to where it is used as possible

Duplicated state drifts out of sync; global state couples unrelated parts and re-renders too much. Derive what you can instead of storing it. Lift state only as high as the components that share it. Treat server data as a cache of the server, not as client state you own.

### 4. Semantics first, styling second

Use the element that means what you are building: a `<button>` for actions, `<a href>` for navigation, `<label>` bound to inputs, headings in order, lists for lists, tables for tabular data. Native semantics give you keyboard support, focus behaviour, and screen reader announcements for free; a `<div>` with a click handler gives you none of them and costs you hours to retrofit. ARIA is for filling gaps native elements cannot, not for replacing them.

### 5. Performance is a feature, measured on realistic devices

Developers test on fast laptops and fast networks; many users have neither. Ship less code, render less, avoid layout thrash, and measure with throttling. Perceived performance (immediate feedback, stable layout, optimistic updates) matters as much as raw speed.

### 6. Keep components small, honest, and composable

A component should do one job, receive what it needs explicitly (props/inputs), and not reach into global state or the network unless that is its explicit role. Composition (children, slots, render props) is more flexible than configuration via ever-growing boolean props.

## Discovering context

Before implementing, find:

- **Framework, version, and rendering model**: client-only SPA, server-side rendering, static generation, server components, islands, or classic multi-page. This determines where data fetching and state belong.
- **Component library and design tokens**: the in-house component directory, a third-party library, a tokens file or theme object, CSS variables. Look at a few existing screens similar to the one you are building and reuse their components and layout.
- **Styling approach**: CSS modules, utility classes, CSS-in-JS, preprocessor, plain stylesheets, component-scoped styles. Follow it exactly, including naming conventions.
- **State and data libraries**: global store, server-state/query cache library, form library, routing library. Do not add a second one of any kind.
- **API client**: generated client from a spec, a shared fetch wrapper with auth and error handling. Use it rather than calling `fetch` directly.
- **Conventions**: file and folder structure, component naming, how tests are written (component tests, visual regression, end-to-end), lint and formatting rules, internationalisation setup (translation keys rather than hard-coded strings).
- **Supported browsers and devices**, and accessibility standard targeted (commonly WCAG 2.x AA).
- **Design source**: mockups or design files with specs for this feature, including states and responsive behaviour. If none exist for some state, infer from the closest existing screen and note your assumption.

## Process

1. **Understand the feature**: user goal, data needed, actions available, the states listed above, responsive behaviour, and accessibility needs (keyboard flow, announcements).
2. **Break the UI into components**: identify which already exist; sketch the tree; decide which components are presentational (render props) and which are containers (fetch data, hold state). Reuse before creating.
3. **Decide where each piece of state lives** (see the state table).
4. **Define the data contract**: what the UI needs from the API, in what shape; map API errors to UI states. If the API is awkward for the UI, discuss changing it (see `api-design`) rather than piling transformation logic into components.
5. **Build structure and semantics first**, then styling with existing tokens and components, then behaviour.
6. **Handle every state**: loading, empty, error, long content, slow network.
7. **Make it accessible**: keyboard, focus, labels, announcements, contrast (using system tokens should preserve contrast; verify).
8. **Make it responsive** across the project's breakpoints.
9. **Test**: component behaviour, key user flows, and visual checks.
10. **Check performance** for anything list-heavy, animation-heavy, or on a critical page.

## Component design

- **Single responsibility**: if describing a component needs "and", consider splitting.
- **Explicit inputs**: props/inputs with clear types and sensible defaults. Avoid components that read unrelated global state.
- **Controlled vs. uncontrolled**: offer controlled mode (parent owns the value) when parents need to coordinate; uncontrolled with a default is simpler for isolated use. Do not mix both for the same value without a clear contract.
- **Composition over configuration**: when a component sprouts `showHeader`, `headerVariant`, `withIcon`, `iconPosition`, it is time to accept children or slots instead.
- **Variants come from the design system**, not from ad hoc style props. `variant="danger"` maps to tokens; `color="#e33"` bypasses the system.
- **Keys and identity**: list items need stable, unique keys from the data (IDs), not array indices, or state and focus attach to the wrong items when the list changes.
- **Side effects** (subscriptions, timers, event listeners) must be cleaned up on unmount, or they leak and fire on stale components.
- **Avoid premature abstraction**: a component used once does not need to be generic. Extract when the second or third real use appears.
- **Separate data from presentation where it helps testing**: a presentational component that takes data as props can be rendered in isolation (in tests, or a component explorer such as a storybook-style tool if the project has one) in every state, including error and empty, without a live API.
- **Name by role in the product, not by appearance**: `OrderSummary` survives a redesign; `BlueBox` does not.

## State management

| Kind of state | Examples | Where it belongs |
|---|---|---|
| Local UI state | Open/closed, hover, current tab, input draft | The component that uses it |
| Shared UI state | Selected item used by sibling panels | Nearest common parent, or a scoped context/store |
| Server state | Lists, records, user profile from the API | A server-state cache (query library, framework loaders, or a disciplined store slice) keyed by request — not copied into component state |
| URL state | Current page, filters, search query, selected tab that should survive reload or be shareable | The URL (path and query parameters) |
| Form state | Field values, touched/dirty, validation errors | The form (form library or local state) until submitted |
| Global app state | Authenticated user, theme, feature flags, locale | App-level context/store, kept small |
| Persistent client state | Preferences, drafts | Local storage or similar, with versioning and fallbacks |

Rules:
- **Derive, don't duplicate.** If `fullName` is computed from `first` and `last`, compute it; storing it creates a sync bug.
- **Put shareable state in the URL.** Users expect back/forward, reload, and shared links to preserve filters and pages.
- **Server state is a cache**: it has staleness, revalidation, deduplication, and invalidation after mutations. Handling these by hand in every component is how stale data and duplicate requests spread; a dedicated mechanism (library or framework feature) is usually worth it.
- **Global stores stay small.** Putting everything in a global store creates coupling and wide re-renders.

## Data fetching

- **Fetch where the framework expects**: route loaders, server components, or server-side rendering when available; client-side hooks or effects otherwise. Avoid request waterfalls where a child cannot start fetching until its parent finishes — fetch in parallel or at the route level.
- **Cancel or ignore stale responses.** If the user types quickly or navigates away, earlier responses can arrive after later ones and overwrite fresher data. Use abort signals or request identity checks.
- **Deduplicate** identical requests made by several components.
- **Loading UX**: show skeletons or placeholders that match the final layout (to avoid layout shift) for content; spinners for short actions; delay spinners by a couple of hundred milliseconds so fast responses do not flash.
- **Error UX**: show what failed, in context, with a retry where possible. Do not blank the whole page because one panel failed.
- **Mutations**: disable or guard against double submission; show progress; on success, update or invalidate the affected cached data so the UI reflects the change. Use **optimistic updates** when the operation usually succeeds and is easily reversible, with rollback and an error message on failure. Avoid optimistic updates for payments and other high-stakes actions.
- **Pagination and infinite lists**: preserve scroll position on back navigation; for very long lists, virtualise rendering.
- **Never put secrets in client code.** Anything shipped to the browser is public, including environment variables bundled at build time. API keys that must stay secret belong on a server.

## Routing and navigation

- Every meaningful view gets a URL. Users bookmark, share, reload, and use back.
- Navigation uses links (`<a href>` or the router's link component), so open-in-new-tab and middle-click work.
- On client-side navigation, move focus to the new page's main heading or content and update the document title, so screen reader and keyboard users know the page changed.
- Handle unknown routes (404 view) and unauthorised routes (redirect to sign-in, then back).
- Guard against losing unsaved work on navigation when it matters, without nagging for trivial forms.
- Code-split by route so users download only what the current view needs.

## Forms

Forms are where users give you their data and their patience; most usability and accessibility failures concentrate here.

- **Labels**: every input has a visible label programmatically associated with it. Placeholders are not labels — they disappear on input and often fail contrast.
- **Correct input types and attributes** (`type="email"`, `inputmode`, `autocomplete` tokens) for mobile keyboards and autofill.
- **Validation timing**: validate on submit, and on blur for fields already touched; avoid shouting errors while the user is still typing their first attempt. Re-validate on change once an error is shown so it clears promptly.
- **Error messages**: specific and actionable ("Enter a date after 1 Jan 2024"), shown next to the field, associated programmatically (e.g. `aria-describedby`), and summarised at the top with focus moved there on submit failure for long forms.
- **Client validation is a convenience; server validation is the authority.** Map server-side field errors back onto fields.
- **Submission**: prevent double submits, show progress, keep the user's input on failure, and confirm success clearly.
- **Don't disable the submit button as the only signal** of invalid state; users can't tell why it is disabled. Let them submit and show errors.
- **Respect existing form patterns** in the product: layout, required-field marking, help text style.

## Accessibility in implementation

See `accessible-design` for the full picture. Non-negotiables while coding:

- Everything operable by mouse is operable by keyboard, in a logical order, with a visible focus indicator.
- Interactive custom widgets (menus, tabs, comboboxes, dialogs) follow established keyboard and ARIA patterns; prefer a well-tested accessible component from the design system or a headless library over building your own.
- Dialogs trap focus while open, close on Escape, and return focus to the trigger when closed.
- Images have meaningful `alt` text, or empty `alt` if decorative. Icon-only buttons have accessible names.
- Dynamic updates that matter (form errors, toasts, results loaded) are announced via live regions or focus management.
- Colour is never the only carrier of meaning; contrast meets the target.
- Respect user preferences: reduced motion, text resizing to 200% without breaking layout, and the operating system's colour scheme if the product supports it.
- Do not remove focus outlines without providing an equally visible replacement.

## Performance

Measure before optimising; see `web-performance-audit` for load-time auditing. Common levers:

- **Ship less JavaScript**: route-level code splitting, lazy-load heavy components (editors, charts, maps), avoid large dependencies for small tasks, check bundle composition with the bundler's analyser.
- **Render less**: avoid re-rendering large subtrees on every keystroke; keep frequently-changing state low in the tree; memoise expensive computations and components only where profiling shows a benefit (memoisation everywhere adds cost and complexity).
- **Virtualise long lists** (hundreds to thousands of rows) so only visible rows are in the DOM.
- **Images**: correct sizes per breakpoint, modern formats, lazy loading below the fold, explicit dimensions to prevent layout shift.
- **Avoid layout thrash**: don't interleave DOM reads (measurements) and writes in loops; animate `transform` and `opacity` rather than layout properties.
- **Debounce or throttle** high-frequency handlers (search-as-you-type, scroll, resize).
- **Move heavy computation off the main thread** (web workers) or to the server when it blocks interaction.
- **Fonts**: limit families and weights; use a font-display strategy that avoids invisible text.
- **Keep interactions responsive**: aim for feedback within ~100 ms of input; long tasks over ~50 ms on the main thread delay interaction.

## Styling and design-system fidelity

- Use tokens for every colour, space, size, radius, shadow, z-index, and duration. A raw hex value or a magic `13px` in a component is almost always a bug.
- Use the system's layout primitives (stack, grid, container) where they exist.
- Match the design's responsive behaviour; when designs show only desktop and mobile, interpolate sensibly and check the in-between widths.
- Test with real content lengths: long names, translated strings (often 30–40% longer than English), missing images, numbers with many digits, right-to-left scripts if supported.
- Support the product's themes (e.g. dark mode) by using semantic tokens (`surface`, `text-muted`) rather than literal colours.
- Keep styles scoped to avoid leaking; avoid `!important` and deep selector overrides of library components — use the library's extension points.

## Resilience

- **Contain failures**: wrap independent regions (widgets, panels, routes) in error boundaries or equivalent, so a rendering error in one panel shows a local fallback instead of a blank page. Report caught errors to the project's error-tracking tool if it has one.
- **Defensive rendering of API data**: treat optional fields as optional; a missing nested object from an older API version should not crash the view.
- **Offline and flaky networks**: at minimum, detect failures and offer retry; for apps that need it, queue mutations and sync later, with clear indication of unsynced changes.
- **Version skew**: after a deploy, users with old bundles may call the new API, or lazy-loaded chunks may 404. Handle chunk-load failures by prompting a reload rather than failing silently.

## Internationalisation and localisation

- Route every user-visible string through the project's translation mechanism, including alt text, ARIA labels, and error messages.
- Never build sentences by concatenating fragments; word order differs between languages. Use message formats with placeholders and plural/gender rules.
- Format dates, numbers, currencies, and lists with locale-aware APIs (e.g. the platform's `Intl` facilities), not hand-written formatting.
- Allow for text expansion and, if supported, right-to-left layout: use logical CSS properties (start/end) rather than left/right.

## Testing frontend code

See `testing-strategy` for the overall balance and `end-to-end-testing` for browser-level flows.

- **Test behaviour through what the user perceives**: query elements by role, label, and visible text, and interact as a user would (click, type, keyboard). Tests coupled to class names, internal state, or component structure break on every refactor and miss real regressions. Querying by accessible role also checks that semantics exist.
- **Component tests** for components with logic: state transitions, validation, conditional rendering of each state (loading, empty, error).
- **Mock at the network boundary** (e.g. a request-interception layer) rather than mocking your own hooks or modules, so data-fetching code is exercised.
- **A few end-to-end tests** for critical flows (sign in, checkout, the core task), run against a real build.
- **Visual regression tests** where the project has them, to catch unintended style changes; review diffs rather than blindly updating snapshots.
- **Avoid large snapshot tests of markup**; they get rubber-stamped and catch little.
- **Make tests deterministic**: control time, randomness, and animation; wait for conditions rather than fixed delays.

## Common UI elements and their traps

| Element | Get right | Common trap |
|---|---|---|
| Modal dialog | Focus moves in and is trapped; Escape closes; focus returns to trigger; background inert; scroll locked | Opening dialogs from dialogs; content unreachable on small screens |
| Toast / snackbar | Announced via a polite live region; long enough to read; actions also available elsewhere | Critical errors shown only in a toast that disappears |
| Data table | Header cells, sortable columns announce sort state, responsive strategy for narrow screens | Rebuilding a table from divs; horizontal overflow hiding columns with no cue |
| Dropdown / combobox | Keyboard navigation, type-ahead, announced active option | Custom select that breaks native mobile pickers without a reason |
| Tabs | Arrow-key navigation between tabs, the selected tab linked to its panel | Tabs used for navigation between pages (use links) |
| Infinite scroll | A way to reach the footer, preserved position on back, a "load more" fallback | Unreachable footer; losing place after viewing an item |
| Tooltips | Triggered by hover *and* focus, dismissible, never the only place essential info lives | Tooltip-only labels on icon buttons on touch devices |
| Destructive action | Clear wording, confirmation or undo proportional to the damage | Same visual weight as safe actions |

## Working without a framework

Plain HTML, CSS, and JavaScript remain a good choice for small interactive pieces, content sites, and progressive enhancement. The same principles apply: semantic HTML first, CSS with custom properties as tokens, small modules with explicit inputs, event delegation for dynamic lists, and explicit state objects with a single render function rather than scattered DOM mutations. Do not introduce a framework into a project that does not use one just to build one feature.

## Decision guidance

### Client rendering vs. server rendering vs. static

| Approach | Choose when | Costs |
|---|---|---|
| Static generation | Content changes rarely; marketing, docs | Rebuilds on change; personalisation must happen client-side |
| Server-side rendering / server components | SEO matters, fast first paint on slow devices, data-heavy pages | Server infrastructure, hydration cost and mismatches, more complex caching |
| Client-side rendering (SPA) | Highly interactive apps behind login, where SEO is irrelevant | Slower first load, more JavaScript, blank-page risk on errors |
| Multi-page with progressive enhancement | Content and forms that should work without heavy JavaScript | Less app-like interactivity unless enhanced |

In an existing project this is already decided; work within it.

### Build a component vs. use the design system's vs. use a library

Use the design system's component if one exists, even if imperfect — raise improvements with its owners. For complex accessible widgets not in the system (date pickers, comboboxes, data grids), prefer a mature headless or accessible library styled with the system's tokens over hand-rolling. Build from scratch only for genuinely product-specific components.

### Global store vs. server-state cache vs. local state

If the data comes from the server, use the server-state mechanism. If it is UI state used by one component tree, keep it local or in a scoped context. Reach for a global store only for truly app-wide client state.

## Worked reasoning example

*Illustrative.* Build a searchable, filterable list of orders.

1. State placement: search text, status filter, sort, and page go in the URL (shareable, survives reload). The input's in-progress text is local state, debounced (~300 ms) into the URL. The order list is server state keyed by the URL parameters.
2. Fetching: requests for stale parameters are cancelled when parameters change, so a slow early response cannot overwrite a newer one. Previous results stay visible (dimmed or with an inline indicator) while new ones load, instead of flashing a skeleton on every keystroke.
3. States: initial skeleton matching row layout; "no orders yet" (first-use empty state with the primary action); "no results for these filters" (with a clear-filters action) — a different empty state; error with retry; very long customer names truncated with the full text available.
4. Accessibility: the search input has a label; the result count is announced politely when results change; filters are real form controls; the table uses table semantics with header cells.
5. Performance: if pages can hold hundreds of rows, virtualise; otherwise paginate server-side.
6. Fidelity: table, input, badge, and pagination components come from the design system; status badge colours map to existing semantic tokens.

## Pitfalls

- **Only the happy path implemented**: no empty, error, or long-content handling.
- **Divs as buttons**, missing labels, broken focus — retrofitting accessibility is far more expensive than starting with semantics.
- **Invented styles**: new colours, spacings, or near-duplicate components that drift from the design system.
- **Server data copied into local state** and never updated after mutations.
- **Race conditions** in fetching: out-of-order responses, state updates after unmount.
- **Request waterfalls** from nested components each fetching on mount.
- **Index keys** in dynamic lists, causing wrong items to keep state.
- **Effects used for derivations**, causing extra renders and transient wrong values; compute during render instead.
- **Prop drilling through many layers** or the opposite, everything in a global store.
- **Over-memoisation** without measurement, adding complexity for no gain.
- **Secrets or privileged logic in client bundles.**
- **Layout shift** from images without dimensions, late-loading fonts, or content inserted above what the user is reading.
- **Breaking the back button** and deep links by keeping navigational state only in memory.
- **Hard-coded user-facing strings** in an internationalised app.
- **Untested on mobile, keyboard, or slow networks.**

## Security notes

- Never inject unsanitised user content as HTML; frameworks escape by default, so treat any "raw HTML" escape hatch as a security review point and sanitise with a vetted library.
- Do not store long-lived tokens where scripts can read them if the project can use HTTP-only cookies; follow the project's auth approach (see `authentication-and-authorization`).
- Validate and encode URLs before using user input in `href` or `src` (block `javascript:` URLs).
- Client-side checks (hidden buttons, disabled routes) are UX, not security; the server must enforce authorization.

## Quality bar and verification

Before calling frontend work done:

- [ ] The UI uses existing components and tokens; no new raw colours, spacings, or one-off variants without agreement.
- [ ] Every state is implemented: loading, empty (each kind), error, populated, long content, slow network.
- [ ] State lives in one place; shareable view state is in the URL; server data is refreshed or invalidated after mutations.
- [ ] Fetching handles cancellation and out-of-order responses; no duplicate or waterfall requests on the critical path.
- [ ] Keyboard-only walkthrough works with visible focus; dialogs and menus manage focus correctly; inputs have labels; dynamic changes are announced.
- [ ] Automated accessibility checks pass if a tool is available (e.g. an axe-based checker or linter plugin); remember these catch only a portion of issues.
- [ ] Layout works across the project's breakpoints, at 200% zoom, with long and translated strings.
- [ ] No console errors or warnings introduced; no hydration mismatch warnings in server-rendered setups.
- [ ] Component and flow tests cover the main interactions and the error state; existing tests, type checks, and lints pass.
- [ ] If you can run the app, you exercised the feature in a browser, including throttled network, and compared it to the design. If you cannot, say so and list exactly what the user should check.
