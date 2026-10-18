---
name: ui-design-fundamentals
description: >-
  Design user interfaces that are clear, usable and fit their product:
  visual hierarchy, alignment, proximity and grouping, contrast, consistency,
  affordances and signifiers, information density, the full set of UI states
  (empty, loading, partial, error, success, disabled), and choosing between
  common component patterns (modal vs. inline, tabs vs. accordion, table vs.
  cards, menus, toasts). Derives design direction from the product, audience,
  platform and existing brand rather than a default aesthetic. Use when asked
  to design, mock up, lay out, improve, redesign or "make look better" a
  screen, page, form, dashboard, settings panel or app UI, or when building a
  UI in code without a designer. For typography/color/visual language use
  visual-design; for tokens and component libraries use design-systems.
metadata:
  category: design
  related: visual-design, layout-and-responsive-design, interaction-design, accessible-design, design-systems, information-architecture, ux-writing, wireframing-and-prototyping, design-critique, frontend-development
---

# UI Design Fundamentals

A user interface is a set of decisions about what someone needs to see, understand and do, in what order, under what conditions. Good UI design makes the right action obvious, the current state legible, and mistakes cheap. It is mostly about **structure and behaviour**; surface styling matters, but it is the last layer, and it must be derived from the product rather than imported from habit.

This skill covers the screen-level craft: hierarchy, grouping, states, component choice and density. It is the primary skill when the deliverable is "a screen (or set of screens) that works".

**Not covered here, see siblings:**

- Typography, color systems, spacing scales, iconography, visual language → `visual-design`
- Grids, breakpoints, reflow, container queries → `layout-and-responsive-design`
- Flows, validation, feedback timing, undo → `interaction-design`
- Animation → `motion-design`
- Tokens, component APIs, governance → `design-systems`
- Accessibility from the start → `accessible-design` (and `accessibility-audit` for review)
- Navigation structures and labelling at the site level → `information-architecture`
- Words on the interface → `ux-writing`
- Low-fidelity exploration and clickable prototypes → `wireframing-and-prototyping`

## Core principles

### 1. Direction comes from context, never from a default

There is no neutral-good look. A trading terminal, a children's reading app, a hospital charting tool and a fashion storefront need different density, tone, pace and emphasis. Before choosing anything visual, establish:

- **Who** uses it (expertise, frequency, age, accessibility needs, devices, environment — bright sunlight, gloved hands, a noisy ward).
- **What job** the screen does (monitor, compare, create, decide, configure, browse, transact).
- **How often** (daily expert tools reward density and keyboard paths; once-a-year flows reward explanation and hand-holding).
- **What already exists** (brand guidelines, a design system, the current app, platform conventions such as Apple HIG, Material, Fluent, or the web's own conventions).
- **What it must feel like** — and ask for evidence: competitor references the stakeholder likes or dislikes, adjectives, existing marketing material.

Why: when these are not established, output converges to a generic average (centred hero, three feature cards, soft shadows, a gradient, a sans-serif everyone uses). That average is not wrong because it is common; it is wrong because it was not chosen for *this* problem. See "Generic UI" under pitfalls.

### 2. Hierarchy is the order of attention

Every screen has a reading order whether you design one or not. Decide it on purpose: what must be seen first, second, third, and what can be ignored until needed. Then use the cheapest means that create that order.

Levers for emphasis, roughly from strongest to subtlest:

| Lever | Notes |
|---|---|
| Position | Top and start-side (left in LTR, right in RTL) are read first on most screens; centre in focused, single-task views. |
| Size | Larger reads as more important; works for type, controls and imagery. |
| Contrast / weight | Darker, bolder or more saturated against the surface draws the eye. |
| Color (hue) | Strong for "this is different", weak for ordering; never the only cue (see `accessible-design`). |
| Whitespace | Isolation increases importance; crowding decreases it. |
| Motion | Overpowering; reserve for state changes (see `motion-design`). |

Rules of thumb:

- **One primary action per view** (or per distinct region). If two things compete equally, neither wins. Secondary actions are visibly quieter; tertiary actions can live in overflow menus.
- **De-emphasise before you emphasise.** Making labels, metadata and chrome quieter often achieves hierarchy without making anything louder.
- **Hierarchy has about three to four useful levels** per region. Beyond that, people stop perceiving the distinctions and the screen just looks busy.
- **Test with a squint or blur.** Blur a screenshot (or step back): the shapes that remain should be the ones you intended to dominate.

### 3. Grouping is meaning (Gestalt)

People infer relationships from layout before reading a word.

- **Proximity:** things close together are read as related. Space *between* groups must be clearly larger than space *within* groups — a common working ratio is 1.5–2× or more. Equal spacing everywhere destroys grouping.
- **Similarity:** things that look alike are assumed to behave alike. Two buttons that look the same but do very different things (one destructive) are a bug.
- **Common region:** a card, panel or background tint binds content together. Use it when proximity alone is not enough, not by default — boxes inside boxes inside boxes is a frequent failure.
- **Alignment / continuity:** elements on a shared edge read as a set; misalignments of a few pixels read as mistakes. Fewer alignment lines = calmer screen.
- **Figure/ground:** overlays, sheets and popovers must clearly separate from what is behind them (scrim, elevation, border).

### 4. Affordances and signifiers

An affordance is what an element lets you do; a signifier is the visible cue that tells you so (Norman). Users act on signifiers. Interactive things must look interactive and non-interactive things must not.

- Links are distinguishable from text by more than color alone (underline, weight, or context such as a nav bar) — WCAG 1.4.1 requires a non-color cue or 3:1 contrast with surrounding text plus a cue on hover/focus.
- Buttons have a recognisable shape or treatment *in this product's language* — whatever that is, apply it consistently.
- Draggable, swipeable, resizable or expandable items need a visible hint (handle, chevron, partial off-screen card) because hidden gestures are undiscoverable.
- Disabled controls should still say why, or be replaced by an explanation (see "Disabled" state below).
- Flat design is fine; *signifier-free* design is not. If a user must hover everything to find what is clickable, the design has failed.

### 5. Consistency, internal then external

- **Internal:** same thing, same look, same place, same word, across the product. Inconsistency forces re-learning and erodes trust.
- **External:** follow platform and industry conventions (Jakob's Law: users spend most of their time on *other* products). Back behaviour, a search field's look, where the account menu lives, date pickers, pull-to-refresh on mobile.
- **Break convention only deliberately**, when the gain is large and measurable, and then signal the difference clearly.

### 6. Density is a design decision, not a side effect

| Context | Typical density | Why |
|---|---|---|
| Expert, frequent use (trading, IDEs, admin consoles, analytics) | High; compact rows, more columns, keyboard shortcuts | Users scan, compare, and value seeing more over guidance. |
| Occasional, task-driven (checkout, onboarding, government forms) | Low; one topic per step, generous spacing, explanatory text | Users need orientation and confidence. |
| Browsing / content (media, reading, shopping) | Medium, imagery-led | Discovery and pleasure. |
| Touch / mobile | Lower per screen, larger targets | Fingers are less precise than pointers (see target sizes in `accessible-design`). |

Offer a density toggle (compact / comfortable) when one product serves both novice and expert users with dense data. Never reach high density by shrinking text below legible sizes or removing affordances; reach it by removing redundancy.

### 7. Every screen is a set of states

A design that shows only the happy, full-of-data state is a third of a design. Design all of these explicitly (they are covered in detail below): **empty, loading, partial, ideal, too-much, error, success, disabled, offline, permission-limited**.

## Process

### Step 1 — Frame the problem (do not skip)

Write down, briefly: the user, the job, the primary action, success criteria, constraints (platform, existing system, deadline, technical stack), and what is out of scope. If key items are unknown and matter, ask (see `clarify-requirements`). If you cannot ask, state assumptions explicitly in the output.

### Step 2 — Discover what already exists

Before drawing anything, look for:

- **A design system or component library** (in code: a `components/`, `ui/`, or `design-system` package; token files such as `tokens.json`, CSS custom properties, a Tailwind or theme config; Storybook. In design tools: shared libraries, styles, variables).
- **Brand guidelines** (logo usage, color, type, voice, imagery rules).
- **Existing screens** in the product — the nearest analogue to what you are designing. Reuse its patterns.
- **Platform guidelines** for the target (HIG, Material, Fluent, the relevant web conventions).
- **Analytics, support tickets, research** that explain current problems (see `ux-research`).

If a system exists, **work inside it first**. Compose existing components; only propose new ones when composition genuinely fails, and flag them as proposals (see `design-systems`). If nothing exists, you are defining a direction — present it as options (Step 4).

### Step 3 — Content and structure before visuals

1. Inventory the content and actions the screen must support. Real content, not lorem ipsum: realistic names (long and short), real numbers (zero, one, huge), real error messages. Lorem ipsum hides every layout problem that real data reveals.
2. Prioritise the inventory: must-see, should-see, on-demand.
3. Sketch the structure at low fidelity (boxes and labels). Several alternatives cheaply beat one polished guess (see `wireframing-and-prototyping`).
4. Choose components (decision guidance below).

### Step 4 — Derive visual direction (when not given)

Translate context into attributes, then attributes into choices. Illustrative example only:

> Context: internal tool for warehouse supervisors on rugged tablets, used on a noisy floor, often outdoors near loading bays.
> Attributes: legible at arm's length and in glare; fast to hit; calm, not decorative.
> Choices that follow: high contrast, large type and targets, few colors used strictly for status, little imagery, strong state signalling.

Compare a different context:

> Context: a boutique hotel's booking site whose brand book emphasises "quiet luxury".
> Attributes: unhurried, image-led, restrained.
> Choices that follow: generous whitespace, photography as the primary carrier of mood, a type pairing from the brand book, very few interface accents.

When there is no brand to honour, present **two or three distinct directions** with a short rationale each, and let the stakeholder choose. Do not present one direction as "the" answer. Details of building the visual language are in `visual-design`.

### Step 5 — Design the states

Walk each component and screen through the state list below. This is where most of the real work and most of the user pain lives.

### Step 6 — Check against principles and constraints

Run the verification checklist at the end. Then, if possible, put it in front of a user or a proxy (see `usability-evaluation`) or a reviewer (see `design-critique`).

### Step 7 — Hand off precisely

Annotate behaviour, states, responsive rules and edge cases, not just pixels (see `design-to-code-handoff`).

## Designing the states

| State | What to design | Common failure |
|---|---|---|
| **Empty (first use)** | Explain what will appear here and offer the action that makes it appear. Illustration optional; a clear sentence and a button are not. | A blank table with headers and nothing else. |
| **Empty (no results)** | Echo the query/filter, suggest broadening, offer to clear filters. | "No results" with no way forward. |
| **Empty (cleared / done)** | Positive closure ("All caught up") — different tone from first-use. | Treating inbox-zero like an error. |
| **Loading** | Under ~1 s: often nothing or a subtle indicator; 1–10 s: skeleton or progress; over ~10 s: determinate progress, estimate, ability to leave and come back. Keep layout stable so content does not jump when it arrives. | Full-screen spinner for every fetch; layout shift on load. |
| **Partial** | Some data loaded, some failed or still pending — show what you have and mark the rest. | Failing the whole page because one widget failed. |
| **Ideal** | The designed-for case with realistic data. | Designing *only* this. |
| **Too much** | Long names, 10,000 rows, 40 tags, very long words in German or Finnish, missing images. Decide truncation, wrapping, pagination, virtualisation. | Overflow, overlap, broken cards. |
| **Error (field / inline)** | Next to the field, says what is wrong and how to fix it, preserved input. | Red border with no message; clearing the form. |
| **Error (page / system)** | What happened, whether data is safe, what to do now (retry, contact, go back). | Raw stack traces or "Something went wrong" alone. |
| **Success** | Confirm proportionate to stakes: inline change for small edits, a toast for background actions, a confirmation page for purchases or submissions. | Silent success on high-stakes actions; modal "Saved!" for trivial ones. |
| **Disabled** | Prefer keeping controls enabled and explaining on activation, or show why it is disabled nearby. Disabled controls are often skipped by assistive tech and are low-contrast by design. | Greyed-out submit button with no explanation. |
| **Offline / degraded** | What still works, what is queued, when it will sync. | Silent failure, lost data. |
| **Permission-limited** | What the user can see, why they cannot act, who can grant access. | Hiding features so users do not know they exist. |

Timing thresholds come from long-standing response-time research (Miller 1968; Card, Robertson & Mackinlay 1991; popularised by Nielsen): about 0.1 s feels instantaneous, about 1 s keeps flow of thought, about 10 s is the limit of attention. See `interaction-design` for latency perception.

## Component pattern decisions

Choose by the job, not by habit. These are defaults with reasons; an existing system's conventions override them.

### Overlays: modal dialog vs. inline vs. sheet vs. popover vs. new page

| Choose | When | Avoid when |
|---|---|---|
| **Inline edit / expand** | Small, reversible edits in context; user needs to see surrounding content. | The edit has many fields or consequences. |
| **Popover / dropdown** | Small, transient choices anchored to a control (filters, pickers, menus). | Content needs scrolling or is essential. |
| **Modal dialog** | A decision that must be made before continuing, or a short focused task that should not lose context (confirm destructive action, short form). | Long forms, multi-step flows, informational content, anything users want to compare against the page beneath. Stacked modals. |
| **Side sheet / drawer** | Detail or edit panel while keeping the list visible (master–detail on wide screens). | Narrow screens (becomes full-screen anyway). |
| **Bottom sheet (mobile)** | Contextual actions or detail on touch devices, within thumb reach. | Desktop pointer interfaces. |
| **Full page / route** | Substantial tasks, anything that should be linkable, bookmarkable or survive refresh. | Quick confirmations. |

Modals interrupt. Each one should pass the question "would the user be worse off without this interruption?"

### Showing sections: tabs vs. accordion vs. long page vs. stepper

| Pattern | Use when | Note |
|---|---|---|
| Tabs | 2–7 peer sections, users switch between them, rarely need two at once. | Labels must predict content. Do not use tabs for sequential steps. |
| Accordion | Many sections, users need one or a few, scanning headings is enough (FAQs, settings groups). | Hides content from search-in-page and skimming; avoid for content everyone needs. |
| Single long page with anchors | Users read or compare across sections. | Usually better than both tabs and accordions for content people must read. |
| Stepper / wizard | Sequential task with dependencies between steps, novice users. | Show progress and allow going back without losing data. |

### Collections: table vs. list vs. cards vs. grid

| Pattern | Best for |
|---|---|
| Table | Comparing many items across the same attributes; sorting; bulk actions; numeric data (right-align numbers, use tabular figures). |
| List | Scanning many items by one or two primary attributes; mobile. |
| Cards | Heterogeneous items, visual content, items with distinct actions; browsing rather than comparing. |
| Image grid | Visual recognition is the main task (photos, products, files with thumbnails). |

Cards are overused because they look "designed". If users need to compare prices or dates across items, a table or list serves them better.

### Choices: radio vs. select vs. segmented vs. checkbox vs. toggle vs. combobox

- **2–5 mutually exclusive options, all worth seeing:** radio buttons or a segmented control.
- **Many options or space is tight:** select / dropdown; with more than ~15, a searchable combobox.
- **Independent yes/no options to submit later:** checkboxes.
- **An immediate on/off setting that takes effect right away:** toggle switch. Do not use a switch inside a form that needs a submit button — the switch implies immediate effect.
- **Multiple selection from a long list:** searchable multi-select with visible chosen items.

### Feedback: toast vs. banner vs. inline message vs. dialog

| Pattern | Use for | Rule |
|---|---|---|
| Inline message | Feedback about a specific field or section. | Closest to the cause; persistent until resolved. |
| Toast / snackbar | Low-stakes confirmation of a background action, ideally with Undo. | Never the only place for errors or essential info; auto-dismissing content must not be required reading (WCAG 2.2.1 timing, 4.1.3 status messages must be announced). |
| Banner | System-wide or page-wide conditions (offline, trial ending, maintenance). | Dismissible unless critical; do not stack several. |
| Dialog | Blocking decisions only. | See modal guidance above. |

### Navigation (screen level)

Top bar, side navigation, bottom tab bar, hamburger menu, breadcrumbs — the right choice depends on number of destinations, depth of hierarchy and platform. Rough guide: under ~5 primary destinations on mobile → bottom tabs; many destinations or deep hierarchy on desktop → side nav; hidden menus reduce discoverability and usage, so do not hide primary destinations if there is room to show them. Structure itself is `information-architecture`.

### Buttons and actions

- Label buttons with the specific outcome ("Delete 3 files", "Send invoice") rather than "OK" / "Submit" (see `ux-writing`).
- Visual weight follows importance: one primary, quieter secondary, plain tertiary. Destructive actions get a distinct treatment and often a confirmation or undo.
- Button order follows the platform convention (some place the primary action last, some first); be consistent within the product.
- Do not disable the primary button to signal invalid forms without saying what is missing.

## Discovering and honouring an existing brand or system

1. **Collect artefacts:** brand book, marketing site, app store screenshots, existing product UI, token files, component library, Figma/Sketch/Penpot libraries, Storybook.
2. **Extract the rules actually in use**, not only the documented ones: what type sizes, colors and spacing values appear in the live product? Where documentation and reality disagree, ask which wins.
3. **Identify the gaps** — the states, components or densities the system does not cover yet.
4. **Extend in the system's own grammar:** if it uses subtle borders not shadows, your new component uses borders. If its corners are square, yours are square. A new element should look like it was always there.
5. **Flag deviations** you believe are justified, with reasons, for the owner to decide.

Signals that you are drifting from the system: introducing new hex values, new font sizes, new spacing numbers, or a component that duplicates an existing one with small differences.

## Pitfalls and anti-patterns

### Generic, "AI-looking" or template UI

Recognise it by: a centred hero with a gradient blob, a headline in a fashionable geometric sans, three equal feature cards with icons, rounded everything, soft drop shadows on all surfaces, purple-to-blue accents, emoji as icons, glassmorphism with no reason, stock 3D illustrations, every section the same rhythm. The problem is not any one choice; it is that none was made for the user. Fix by returning to Step 1 and Step 4: name the audience and attributes, then make choices you can justify against them. A plain interface with a clear reason beats a fashionable one without.

### Other recurring failures

- **Decoration before structure:** polishing gradients while the primary action is unclear.
- **Everything emphasised:** bold, color and size used on many elements so nothing stands out.
- **Equal spacing everywhere:** loss of grouping; the page reads as a uniform list.
- **Boxes in boxes:** cards inside panels inside cards; borders compete with content.
- **Mystery meat:** icon-only controls without labels or tooltips for non-universal actions. Only a handful of icons are near-universal (close, search, home, menu in context, play); label the rest.
- **Placeholder as label:** placeholder text disappears on input, has poor contrast, and is not a reliable accessible name (see `accessible-design`).
- **Happy-path only:** no empty, error or long-content states.
- **Lorem ipsum and perfect data:** hides truncation and wrapping problems.
- **Over-modal:** confirmation dialogs for reversible actions; prefer undo.
- **Hidden primary features** behind hamburger menus or hover-only reveals on touch devices.
- **Inventing components** that the existing system already provides.
- **Designing at one screen size** (see `layout-and-responsive-design`).
- **Dark patterns:** pre-checked upsells, confirmshaming, hard-to-find cancel, disguised ads. They are unethical, increasingly illegal (e.g. EU Digital Services Act, US FTC enforcement), and erode trust. Refuse to design them and offer a fair alternative.

## Quality bar and verification

Before calling a UI design done, check:

**Purpose**
- [ ] The primary action of each view is identifiable within a couple of seconds (five-second test or squint test).
- [ ] Every visual choice can be explained by audience, task, brand or platform — not "it looks modern".

**Structure**
- [ ] Reading order matches priority order.
- [ ] Grouping is clear from spacing alone; between-group space clearly exceeds within-group space.
- [ ] Elements align to a small number of shared edges.
- [ ] Similar things look alike; different things look different.

**States**
- [ ] Empty, loading, error, success, disabled and too-much states exist for every data-bearing component.
- [ ] Tested with realistic, extreme and missing content (long strings, zero, thousands, no image, RTL text if relevant).

**Consistency**
- [ ] Uses existing components and tokens; any new ones are flagged and justified.
- [ ] Follows platform conventions unless a deviation is deliberate and explained.

**Usability and access**
- [ ] Interactive elements look interactive; non-interactive ones do not.
- [ ] Meets contrast, target size and focus requirements (see `accessible-design`; WCAG 2.2 AA is a common baseline).
- [ ] Works at the required breakpoints and with zoom (see `layout-and-responsive-design`).

**Verification methods**, depending on what you can do:
- If you can render the UI (code or prototype), view it at several widths, with keyboard only, with 200% zoom, and in light and dark modes if supported. Screenshot and compare against intent.
- If you cannot render, walk through each state in writing and describe what the user sees and can do.
- Ask for (or run) a quick usability check with 3–5 representative users on the core task; it catches most severe problems cheaply (see `usability-evaluation`).
- Request a structured critique against the stated goals (see `design-critique`).

## Working without visual output

If you can only produce text or code, you can still design well: describe hierarchy explicitly ("the order total is the most prominent element; line items are secondary"), specify states, and produce semantic, component-based markup that inherits the project's existing styling rather than hard-coding a new look. When you write CSS without a system, define a small set of named values (see `visual-design` and `design-systems`) instead of scattering one-off numbers.
