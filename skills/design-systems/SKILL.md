---
name: design-systems
description: >-
  Create, extend, audit and evolve design systems: design tokens (primitive,
  semantic and component tiers), naming, theming and multi-brand support,
  component APIs, variants and composition, documentation, contribution and
  governance models, versioning and deprecation, adoption and migration, and
  keeping design files and code in sync. Starts by discovering and working
  within any existing system. Use when asked to build a component library,
  UI kit, style guide or token set, add dark mode or a second brand theme,
  add or change a shared component, consolidate inconsistent UI, set up
  design-to-code token pipelines, or decide whether something belongs in the
  system. For choosing the colors and type themselves use visual-design; for
  a single screen use ui-design-fundamentals.
metadata:
  category: design
  related: visual-design, ui-design-fundamentals, frontend-development, design-to-code-handoff, accessible-design, code-documentation, dependency-management, release-management, technical-decision-making
---

# Design Systems

A design system is a shared, maintained set of decisions — expressed as tokens, components, patterns, guidelines and the process around them — that lets many people build consistent products faster. It is a **product with users** (designers and engineers), not a one-off deliverable. Its value comes from adoption, and adoption comes from being easier to use than not using it.

This skill covers the architecture and lifecycle of a system. The *content* of the visual language comes from `visual-design`; individual screen design from `ui-design-fundamentals`; implementation details from `frontend-development`.

## Core principles

1. **Work within the existing system first.** Most work is extending, not inventing. Before adding anything, find what exists and use it. A near-duplicate component is worse than none: it splits usage and doubles maintenance.
2. **Systematise what has proven itself.** Extract components and tokens from patterns that already recur in real products (rule of thumb: when a pattern exists in roughly three places, consider promoting it). Speculative components designed in isolation tend to fit no real use.
3. **Decisions, not pixels.** A token named for its *purpose* (`color.text.danger`) survives a rebrand; a token named for its value (`red-600` used directly in components) does not. Encode intent so the system can change underneath consumers.
4. **Constrain the common, enable the rare.** Make the right thing the easy default; allow escape hatches (composition, slots, documented overrides) for legitimate edge cases, so teams do not fork.
5. **Accessibility is built in, not added on.** Components carry correct semantics, keyboard behaviour, focus management and contrast-safe defaults, so every consumer inherits them (see `accessible-design`).
6. **Change is managed.** Every change to a shared system affects many products. Version, communicate, deprecate gradually, and provide migrations.
7. **Single source of truth, many outputs.** Tokens and component specs should originate in one place and be transformed into each platform's format, not hand-copied.

## Discovering an existing system

Look for, in roughly this order:

- **Code:** packages named `ui`, `components`, `design-system`, `tokens`; theme files; CSS custom properties; Tailwind/theme configs; platform asset catalogs and style resources (e.g. iOS asset catalogs, Android `themes.xml`/Compose `MaterialTheme`); Storybook or other component explorers; token pipeline configs (e.g. Style Dictionary, Terrazzo/Cobalt, Theo).
- **Design files:** shared libraries, styles, variables/modes, component sets with variants.
- **Documentation:** a docs site, README, usage guidelines, contribution guide, changelog.
- **Reality:** what is actually used in products. Audit a few screens: which components, which token values, how many hard-coded overrides. Drift between documented and actual usage is normal and important to know.
- **Owners and process:** who maintains it, how contributions work, release cadence.

If a third-party system or framework is the base (e.g. Material, Fluent, Carbon, Polaris, a headless library such as Radix, React Aria or Headless UI, or a utility framework), learn its extension points and theming model before customising. Fighting a foundation costs more than choosing a different one.

Then decide the mode of work:

| Situation | Mode |
|---|---|
| Mature system, need a screen | Compose existing components; no system change. |
| System lacks a variant | Propose a variant via the contribution process. |
| System lacks a component used in several places | Propose a new component with evidence of need. |
| Inconsistent UI, no real system | Audit → consolidate → extract tokens → extract components incrementally. |
| Greenfield product | Start with a minimal foundation (tokens + a few core components); grow from real needs. |
| Rebrand or new theme | Change semantic token mappings; avoid touching components. |

## Tokens

### Tiers

| Tier | Also called | What it holds | Example names (illustrative) | Who references it |
|---|---|---|---|---|
| **Primitive** | Base, global, reference, core | The raw palette and scales: every available value. | `color.blue.600`, `space.4`, `font.size.300`, `radius.2` | Only semantic tokens. |
| **Semantic** | Alias, system, decision | The purpose of a value in the interface. | `color.text.primary`, `color.surface.raised`, `color.border.focus`, `space.inset.md`, `font.body` | Components and product code. |
| **Component** | Specific | A component's own decisions, when it needs to diverge from or be tuned independently of semantics. | `button.primary.background`, `input.border.error` | That component only. |

Why tiers: themes, brands and modes swap **semantic → primitive mappings** without touching components. Component tokens are optional; use them when a component must be themeable independently or when multiple brands diverge at component level. Many systems keep component tokens to a minimum because each one is an API to maintain.

### Naming

There is no single correct scheme, but good names are:

- **Structured** consistently, e.g. `category.concept.property.variant.state` — `color.background.button.primary.hover` — choose the order once and keep it.
- **Purpose-based at the semantic tier** (`danger`, `subtle`, `inverse`, `disabled`) rather than appearance (`red`, `light-grey`).
- **Scalable**: numeric scales leave room (e.g. 100–900 steps or t-shirt sizes with room for additions). Avoid names like `small`, `smaller`, `smallest` that cannot grow.
- **Platform-neutral** in source; transformed to platform conventions on output (`--color-text-primary`, `colorTextPrimary`, `ColorTextPrimary`).

### Format and pipeline

- Store tokens in a structured source format. The W3C Design Tokens Community Group (DTCG) format is an emerging interchange standard supported by a growing number of tools; adopting it eases moving between design tools and build pipelines.
- Transform into each target (CSS custom properties, JS/TS, iOS, Android, design-tool variables) with a build step (examples: Style Dictionary, Terrazzo, or custom scripts).
- Keep design-tool variables and code tokens in sync through the pipeline or a sync plugin, with one side declared the source of truth.
- Types of tokens beyond color: spacing, size, typography (composite), radius, border width, shadow/elevation, opacity, z-index layers, motion duration and easing (see `motion-design`), breakpoints.

### Theming and modes

- **Modes** (light/dark/high-contrast, density compact/comfortable, brand A/B) are alternative semantic mappings. Define every semantic token in every mode; a missing value silently falls back and breaks contrast.
- Validate contrast **per mode** for every foreground/background semantic pair the components use (see `visual-design`, `accessible-design`).
- Multi-brand: share components and semantic structure; vary primitives and mappings per brand. If brands need different *component structure*, they may need different systems — do not force it.
- Runtime theming on the web is typically done by swapping CSS custom property values under a selector or attribute; native platforms use their theme mechanisms. Avoid compiling a separate stylesheet per theme unless necessary.

## Components

### What belongs in the system

Include when the component is **reused across teams or products**, **benefits from consistent behaviour** (accessibility, interaction), and **has a stable purpose**. Keep out (leave in product code) when it is one-off, highly domain-specific, or still being explored. A middle layer of shared "patterns" or recipes (composition guidance without a coded component) is often right for things like page layouts or flows.

### Component API design

The API (props, slots, variants, events) is a contract. Design it as carefully as a public code API (see `api-design` for general API principles).

- **Name by purpose, not appearance:** `variant="danger"` rather than `color="red"`; `emphasis="high"` rather than `filled`.
- **Variants are a closed set** of sanctioned options (e.g. emphasis levels, sizes, tones). Each variant multiplies design, code, test and documentation work: every new prop value is maintenance forever. Prefer fewer, meaningful variants.
- **Avoid boolean explosion** (`isPrimary`, `isLarge`, `isDanger`, `isGhost` — 16 combinations, many invalid). Use enumerated props that make invalid combinations unrepresentable.
- **Composition over configuration:** for complex components (cards, dialogs, menus, tables), expose sub-components or slots (`Dialog.Title`, `Dialog.Body`, `Dialog.Actions`) rather than dozens of props. This handles edge cases without forking.
- **Sensible defaults:** the default rendering should be the most common, correct use.
- **Controlled and uncontrolled** modes for stateful inputs where the framework supports them.
- **Pass-through** of standard attributes (ARIA attributes, `id`, data attributes, event handlers, refs) so consumers can integrate.
- **Escape hatches are documented** (`className`/`style` overrides, theme overrides) and their use is monitored; frequent overrides signal a missing variant.
- **States** are part of the API: hover, focus-visible, active, disabled, loading, selected, invalid, read-only — designed and coded for every variant.

### Design-file structure

In design tools, mirror the code API: same component names, same variant property names and values, same slot structure. When the design library and code library speak the same language, handoff becomes lookup rather than translation (see `design-to-code-handoff`). Tools such as code-connect features or Storybook links can make the mapping explicit.

### Accessibility in components

- Use native elements where they exist (`button`, `a`, `input`, `select`, `dialog`) before custom ones.
- For custom widgets, follow established keyboard interaction patterns (the WAI-ARIA Authoring Practices Guide is the usual reference) or build on a vetted headless library.
- Manage focus (dialogs trap and restore focus; menus support arrow keys and Escape).
- Ship visible focus styles that meet WCAG 2.4.7 and contrast requirements; never remove outlines without a replacement.
- Document what consumers must still supply (labels, alt text, headings, error messages).

## Documentation

Good documentation answers, for each component or token:

- **What it is for and when to use it** — and, equally important, **when not to** and what to use instead.
- **Anatomy** (named parts), **variants** and **states**, with live examples.
- **Behaviour**: interaction, responsive behaviour, keyboard support, screen reader output.
- **Content guidance**: label length, tone, truncation rules (see `ux-writing`).
- **Code usage** with copyable examples, props table generated from source where possible.
- **Accessibility notes** and consumer responsibilities.
- **Status** (experimental, stable, deprecated) and changelog.

Generate what you can from source (props tables, token lists) so docs cannot drift. Hand-write guidance and rationale; those are what prevent misuse. See `documentation-site` and `code-documentation`.

## Governance and contribution

Choose a model that fits the organisation's size:

| Model | Description | Fits |
|---|---|---|
| **Centralised** | A dedicated team builds and owns everything. | Larger orgs needing consistency; risk: bottleneck. |
| **Federated** | Contributors from product teams build to shared standards; a small core team reviews and maintains. | Medium–large orgs; scales better; needs clear standards. |
| **Hybrid** | Core team owns foundations and core components; product teams contribute patterns. | Common middle ground. |
| **Solo / informal** | One person or a small team maintains it alongside product work. | Small teams; keep the system small. |

A workable contribution process: **propose** (problem, evidence of need, existing alternatives considered) → **review** (fit with system, API, accessibility) → **design and build** (to standards, with tests and docs) → **release** (versioned, announced) → **support**.

Decision rule for requests: Can existing components compose to solve it? → Yes: document the pattern. → No: Is it needed in multiple places? → No: build locally, revisit later. → Yes: is it a variant of an existing component or a new one? Proceed accordingly.

## Versioning, change and deprecation

- Use **semantic versioning** for packages: breaking changes (removed props, renamed tokens, behaviour changes) require a major version. Visual changes that shift layouts can be breaking in practice even if the API is unchanged — communicate them.
- **Deprecate before removing**: mark as deprecated (in code warnings, docs, design library), provide the replacement and a migration path, give a timeline, then remove in a later major version.
- Provide **codemods** or search-and-replace guidance for renames where feasible.
- Maintain a **changelog** written for consumers (what changed, why, what to do).
- Consider visual regression testing (e.g. screenshot comparison in a component explorer) so unintended changes are caught before release. See `release-management`, `dependency-management`.

## Adoption

A system nobody uses has failed regardless of quality.

- **Reduce friction**: easy installation, good defaults, copyable examples, fast answers to questions.
- **Migrate incrementally**: new screens use the system; existing screens migrate when touched. Big-bang rewrites rarely finish.
- **Measure** adoption: percentage of UI using system components, number of hard-coded values/overrides, number of local duplicates, time to build common screens. Tools can scan code for imports and raw values.
- **Listen**: frequent overrides, forks and "can I just…" questions indicate missing capabilities, not disobedient teams.
- **Show value**: before/after consistency, accessibility fixes inherited for free, faster delivery.

## Auditing and consolidating inconsistent UI

When there is no real system, or the system has drifted:

1. **Inventory**: screenshot and catalogue every instance of each element type (buttons, inputs, colors, font sizes, spacings, shadows). Code scanning (searching for hex values, pixel sizes) quantifies drift.
2. **Cluster**: group near-duplicates (e.g. 23 greys that collapse into 8 roles).
3. **Decide canonical values and components** with stakeholders, based on `visual-design` principles and real usage.
4. **Extract tokens first** (cheapest and highest leverage), then the most common components (buttons, inputs, typography, layout primitives).
5. **Migrate** incrementally with tracked progress.

## Worked example: token tiers and a dark theme

Illustrative structure only — names and values show the mechanism, not a recommended palette.

```
Primitive (raw options)
  color.neutral.0   … color.neutral.1000   (a lightness ramp)
  color.accent.100  … color.accent.900
  color.red.100     … color.red.900
  space.0, space.1, space.2, space.3, space.4, space.6, space.8 …

Semantic, light mode                       Semantic, dark mode
  color.surface.default  → neutral.0         → neutral.950
  color.surface.raised   → neutral.0         → neutral.900
  color.text.primary     → neutral.900       → neutral.50
  color.text.secondary   → neutral.700       → neutral.300
  color.border.default   → neutral.300       → neutral.700
  color.action.primary   → accent.600        → accent.400
  color.text.on-action   → neutral.0         → neutral.950
  color.text.danger      → red.700           → red.300
  color.border.focus     → accent.700        → accent.300

Component (only where needed)
  button.primary.background        → color.action.primary
  button.primary.background.hover  → (a semantic hover token)
```

What to notice:

- Components never mention `accent.600`; switching to dark mode, or to a second brand with a different accent ramp, changes only the semantic mapping.
- Dark mode is not "reverse the ramp": raised surfaces get *lighter* in dark mode, accents shift to lighter steps to keep contrast, and `text.on-action` may flip.
- Each semantic foreground/background pair (`text.primary` on `surface.default`, `text.on-action` on `action.primary`, `text.danger` on `surface.raised`) is checked for contrast in both modes, and the result recorded.

## Worked example: component API, before and after

Illustrative, framework-neutral pseudo-API.

Before (configuration by booleans, appearance-named):

```
Button(isPrimary, isSecondary, isDanger, isSmall, isLarge, isOutline, isLoading, icon, iconRight)
```

Problems: contradictory combinations (`isPrimary` + `isSecondary`), unclear defaults, appearance names that break on rebrand, two icon props that cannot express icon-only buttons with accessible names.

After (enumerated, purpose-named, composable):

```
Button(
  emphasis: "high" | "medium" | "low"        default "medium"
  tone:     "neutral" | "danger"             default "neutral"
  size:     "sm" | "md" | "lg"               default "md"
  loading:  boolean                          keeps width, announces busy state
  children: label content (may include an Icon sub-component at start or end)
)
IconButton(icon, label)                      label is required → accessible name
```

Invalid states are unrepresentable, the icon-only case forces an accessible name, and "danger" survives any color change.

## Starting a system from nothing

A minimal, high-leverage first release usually contains:

1. **Foundations as tokens:** color roles (with light/dark if needed), type scale by role, spacing scale, radius, elevation, motion durations/easings, breakpoints, z-index layers.
2. **Layout primitives:** stack, cluster/inline, grid, container — these remove most one-off spacing.
3. **Core interactive components:** button, link, text input, select, checkbox, radio, switch, and a dialog; each with all states and accessibility built in.
4. **Feedback components:** inline message, toast/snackbar, banner, loading indicators, empty state.
5. **Documentation and a contribution path**, however lightweight.

Add components as real product work demands them. A system with ten excellent components beats one with eighty unreliable ones.

## Multi-platform systems

When one system serves web, iOS, Android and desktop:

- **Share decisions, not necessarily components.** Tokens, naming, content guidelines and interaction principles can be shared; component implementations are usually per platform.
- **Respect platform idioms.** A date picker, navigation bar or switch should behave the way each platform's users expect; enforcing identical controls everywhere often makes every platform feel foreign. Decide per component whether it is "brand-consistent" or "platform-native", and document the choice.
- **Transform tokens per platform** (units: px/rem, pt, dp/sp; color spaces; naming conventions) from one source.
- **Track parity** in a component matrix (which component exists on which platform, at which version) so gaps are visible.

## Testing a design system

- **Unit / interaction tests** for component behaviour (keyboard handling, state changes, controlled/uncontrolled modes).
- **Automated accessibility checks** on every component story/example (e.g. axe-based tooling), plus periodic manual screen-reader and keyboard passes — automated tools catch only part of the issues.
- **Visual regression** across variants, states, themes and breakpoints, so a token change's blast radius is visible before release.
- **Token validation:** every semantic token defined in every mode; contrast thresholds checked automatically for declared pairs; no references to undefined tokens.
- **Consumer smoke tests:** build one or two real product screens against a release candidate before publishing.

## Process for adding to an existing system

1. Search the system (code, design library, docs) for something that already does the job, or nearly.
2. Check whether composition or an existing variant solves it.
3. If not, gather evidence: where else is this needed, what do those uses have in common?
4. Draft the API and anatomy in the system's existing conventions (naming, prop style, token tiers, file structure).
5. Design every state and variant; validate accessibility and contrast in all modes.
6. Implement with tests (unit, accessibility checks, visual regression where available) and documentation.
7. Release with a version bump and changelog; tell consumers.

## Pitfalls

- **Building in a vacuum**: a big upfront library based on imagined needs; unused components, missing real ones.
- **Duplicate components** created because the existing one was not found or slightly did not fit.
- **Primitive tokens used directly in components**, making theming impossible.
- **Token sprawl**: hundreds of component tokens nobody can navigate; semantic tokens that encode every possible combination.
- **Boolean-prop explosion** and variant combinatorics no one tests.
- **Design library and code diverging** in names, variants and behaviour.
- **Docs that show but do not advise** — every component shown, no guidance on when to use which.
- **Accessibility left to consumers** — the system is the best place to fix it once.
- **Breaking changes without notice**, which teaches teams to pin old versions and never upgrade.
- **Over-rigid governance** that makes the system a bottleneck, causing forks.
- **Imposing a house aesthetic**: the system should express the organisation's brand, not a framework default left unthemed or a designer's personal taste.

## Quality bar and verification

- [ ] Before adding anything, the existing system was searched and the outcome recorded (reuse, variant, or new with evidence).
- [ ] Tokens are tiered; components reference semantic (or component) tokens, never raw values or primitives.
- [ ] Every semantic token has a value in every supported mode/theme, and all used foreground/background pairs meet contrast targets in each.
- [ ] Component APIs use purposeful names, closed variant sets, composition for complex structure, and pass through standard attributes.
- [ ] All states are designed and implemented for all variants, including focus-visible, disabled, loading and error.
- [ ] Keyboard and screen-reader behaviour matches established patterns; automated accessibility checks pass, and manual keyboard testing was done.
- [ ] Design-library names and variants match code.
- [ ] Documentation covers when to use / when not to, anatomy, behaviour, accessibility, and code examples.
- [ ] The change is versioned correctly, with a changelog and migration notes for anything breaking or deprecated.

**How to check**, depending on capability: build the token pipeline and inspect outputs for every platform and mode; render components in a component explorer across variants, states and themes; run automated accessibility tests and visual regression; grep consumer code for raw values and overrides to measure adoption. If you cannot execute, provide the token map and API spec in a reviewable form and list the checks that must be run.
