---
name: design-to-code-handoff
description: >-
  Make designs buildable and keep implementation faithful to them: writing
  specs and annotations, mapping design decisions to design tokens and
  existing components, specifying every state and edge case, responsive and
  adaptive behavior, interaction and motion details, accessibility
  requirements, preparing and exporting assets, collaborating from both the
  design and engineering side, and running design QA against the built
  product. Use when preparing designs for developers, implementing a design
  from a mockup or design file, writing a design spec, reviewing a build
  against designs, or reducing rework between design and engineering. For
  building the design system itself use design-systems; for frontend
  implementation technique use frontend-development.
metadata:
  category: design
  related: design-systems, frontend-development, ui-design-fundamentals, layout-and-responsive-design, interaction-design, motion-design, accessible-design, ux-writing, wireframing-and-prototyping, code-review, qa-test-planning, design-critique, estimate-effort, mobile-app-development
---

# Design-to-Code Handoff

"Handoff" is a misleading word. It suggests a moment when a finished design passes from one person to another. In practice, the gap between design intent and shipped product is closed by continuous collaboration: developers involved before designs are final, designers available while code is written, and both checking the result together. The artifacts — specs, tokens, annotations, assets — exist to make that collaboration precise.

This skill is for both sides: designers preparing work so it can be built as intended, and developers (or AI assistants) implementing from designs so that what ships matches what was meant — including everything the mockup didn't show.

**Out of scope, handled elsewhere:**

- Building and governing a design system and its token architecture: `design-systems`.
- Frontend engineering technique (frameworks, state management, performance): `frontend-development`.
- Layout and breakpoint strategy itself: `layout-and-responsive-design`.
- Detailed interaction and motion design: `interaction-design`, `motion-design`.
- Accessibility design principles and audits: `accessible-design`, `accessibility-audit`.

## Core principles

**1. A mockup is one frame of a living system.** A static design shows one state, at one size, with ideal content. The built thing has to handle every state, every size, every content length, every input method, and every failure. Most handoff problems are not mismatches with what was drawn; they are decisions nobody made about what wasn't drawn.

**2. Communicate intent, not just measurements.** "16px gap" is a measurement. "Related items are grouped tightly; separate groups get more space" is intent. When developers know the intent, they make correct decisions in cases the spec didn't cover. Pair key measurements with the rule behind them.

**3. Speak the system's language.** If a design system exists, the design should be expressed in its tokens and components ("spacing-md", "Button / secondary", "text-body-sm"), not raw values. Raw values that almost match a token create drift; a developer either matches the pixel (breaking consistency) or the token (breaking the design). Where the design genuinely needs something new, flag it as new.

**4. Collaborate early; the cheapest fix is before code exists.** Developers reviewing designs at the wireframe or early visual stage catch feasibility problems, missing data, performance concerns, and existing components that already do the job. Designers reviewing early builds catch misinterpretations before they spread.

**5. Single source of truth.** There should be one current version of the design, clearly marked, with superseded versions archived. Building from an outdated frame is one of the most common and most avoidable sources of rework.

**6. Both sides own the result.** Designers own making intent clear and being available; developers own asking when something is unclear rather than guessing, and flagging when implementation must differ. Design QA is a shared check, not a designer's inspection of developers' work.

**7. Fidelity is to intent and to users, not to pixels.** Small deviations that preserve intent (a few pixels from platform rendering differences, a native control instead of a custom one) are usually fine. Deviations that change hierarchy, behavior, accessibility, or meaning are not. Know which is which.

## Discovering context

Before preparing or implementing a handoff, find out:

- **The design system**: tokens (color, typography, spacing, radius, elevation, motion), components in design and in code, and how closely they correspond. Check whether design and code versions are in sync; often they are not.
- **The codebase's conventions**: framework, styling approach (utility classes, CSS modules, styled components, platform-native styling), component library, how tokens are consumed, file and naming conventions, how icons and images are handled. Read similar existing screens in code.
- **Team workflow**: where designs live, how they are versioned, how specs are written (in the design tool, a doc, tickets), how questions get asked, whether there's a design QA step and who signs off.
- **Platforms and targets**: browsers, operating systems, devices, screen sizes, input methods, minimum supported versions, performance budgets.
- **Requirements beyond visuals**: accessibility standard the product commits to, localization languages, analytics events, feature flags, legal text.
- **Data realities**: what the API actually returns, field lengths, nullability, latency, pagination. Designs built on imagined data break on real data.

When implementing, if any of these are unknown and matter, ask. Guessing produces work that looks right in the demo and fails in production.

## What a buildable design contains

The spec doesn't need to be a separate document; annotations in the design file, a ticket, or a short doc are all fine. What matters is that these questions have answers somewhere both sides can find.

### Structure and components

- Which existing components are used, in which variants, and with which properties.
- Which elements are new, and whether they should become reusable components or stay local.
- The content hierarchy and semantic structure: headings and their levels, landmarks or regions, lists, tables, form groupings. This drives both accessibility and layout.

### Tokens and styles

- Colors, type styles, spacing, radii, shadows, borders, and motion expressed as tokens.
- Any values that intentionally fall outside the system, flagged with the reason.
- Theme behavior if the product supports several themes (light/dark, high contrast, brands).

### Layout and responsive behavior

See `layout-and-responsive-design` for strategy. The spec needs:

- How the layout adapts across the supported range, not only at the drawn sizes: what stacks, what hides, what reorders, what scales, what scrolls.
- Fixed vs. flexible dimensions: which elements have set widths, which fill available space, minimum and maximum sizes.
- Alignment rules and grid behavior.
- Behavior at extremes: narrowest supported width, very wide screens, large text or zoom settings, landscape on mobile.
- Overflow handling: truncation (with tooltip or expand?), wrapping, scrolling, "show more".

### States

For every interactive element and every data-driven region, specify the states that apply. See `references/states-and-edge-cases.md` for a full checklist. At minimum:

- **Interactive states**: default, hover, focus (visible), active/pressed, selected, disabled, loading.
- **Data states**: empty (first use, no results, cleared), loading (initial, refresh, pagination), partial, error (load failed, action failed), success, stale or offline.
- **Permission states**: read-only, restricted, upgrade-required.
- **Validation states** for forms: per field and per form, when validation triggers, where messages appear.

### Content and edge cases

- Real copy (from `ux-writing`), with character limits and truncation rules.
- Long and short content: names, titles, numbers, translations, user-generated text.
- Quantity extremes: zero, one, many, thousands.
- Missing data: no avatar, no image, null fields, unknown values.
- Formatting rules for dates, numbers, currencies, and names (locale-aware).

### Behavior and interaction

- What each interaction does, including non-obvious ones (what happens on submit while a request is pending? on double-click? on back navigation?).
- Keyboard interaction: tab order, shortcuts, arrow-key behavior in composite widgets, focus movement when dialogs open and close or content changes.
- Touch interaction: target sizes, gestures and their alternatives.
- Motion: what animates, duration and easing (as tokens where possible), and behavior when the user prefers reduced motion. See `motion-design`.
- Timing: debounce on search, auto-dismiss durations for transient messages (and whether they should auto-dismiss at all), timeouts.

### Accessibility requirements

Designers should specify what code can't infer:

- Accessible names for icon-only buttons and meaningful images; which images are decorative.
- Heading structure and landmark regions.
- Focus order where it differs from visual order, and focus management for dialogs, menus, and dynamic content.
- Announcements for dynamic changes (status messages, errors, live updates).
- Color contrast verified for text and essential non-text elements in all states; meaning not conveyed by color alone.
- Behavior with zoom, large text, and reduced motion.

Developers should use native semantics first and verify with keyboard and at least one screen reader. See `accessible-design`.

### Assets

- Icons from the established icon set where possible; new icons provided in the format the codebase uses (often vector), on a consistent grid, with names that match the codebase convention.
- Images in appropriate formats and sizes for the platforms (multiple resolutions or responsive sources), with guidance on cropping and focal points for variable aspect ratios, and alt text or the rule for generating it.
- Illustrations and animations in formats the codebase can use, with fallbacks.
- Fonts licensed for the intended use (web, app embedding).
- Asset export settings documented so assets can be regenerated consistently.

### Data and integration notes

- Which data each element displays and where it comes from, when not obvious.
- Sorting, filtering, and pagination rules.
- Analytics events tied to interactions, if the team specifies them at design time.
- Feature flags or phased rollout affecting what's shown.

## Process from the design side

1. **Involve engineering early.** Share direction at the wireframe stage; ask about feasibility, data availability, existing components, and performance concerns.
2. **Design with the system.** Use existing components and tokens; keep a list of proposed additions to discuss with system owners.
3. **Design the states and edge cases**, not just the happy path. Where you can't design every one, define the rule ("all empty states follow the pattern in X").
4. **Annotate intent** where measurements alone would be ambiguous: behavior, responsive rules, rationale for unusual choices.
5. **Clean up the file**: mark the current version, remove or archive explorations, name layers and frames meaningfully, ensure components are linked to the library (not detached copies).
6. **Walk through it together.** A short walkthrough with the developers who'll build it surfaces questions faster than any document. Record the answers where others can find them.
7. **Stay available** during implementation; answer questions quickly. Decisions made in chat should be written back into the spec.
8. **Review early builds**, not just the final one.
9. **Run design QA** (below) before release.

## Process from the engineering side (including AI assistants implementing designs)

1. **Read the whole design before coding**: all screens, states, annotations, and the flow between them. Note what's missing.
2. **Map to the system.** For each element, find the existing component and tokens in the codebase. Prefer existing components even if the design is slightly different; ask whether the difference is intentional. Do not hard-code values that correspond to tokens.
3. **List questions and gaps** — missing states, unclear responsive behavior, data that doesn't exist, interactions not specified — and ask them in one batch, early. Where you must proceed without an answer, choose the most conservative option consistent with existing patterns and record the assumption.
4. **Build structure and semantics first**, then layout, then visual detail, then motion. Getting semantics right first makes accessibility and responsiveness much easier.
5. **Test with real and extreme content**, at the full range of sizes, with keyboard and screen reader, in the supported browsers or devices, with reduced motion and large text settings.
6. **Flag deviations** you had to make (technical constraints, platform behavior) to the designer with the reason, before release.
7. **Invite design QA** on a running build (a preview environment, a branch build, or a recording), not just screenshots.

When implementing from an image or a design-tool export without access to the designer, be especially explicit in reporting: which tokens and components you mapped to, which values you inferred, which states and behaviors you designed yourself because they weren't shown, and what should be confirmed.

## Mapping designs to tokens and components

This is where most drift is born. A systematic approach:

1. **Inventory the design's values**: every color, type style, spacing value, radius, shadow, and duration used.
2. **Match each to a token.** Exact matches are easy. For near-misses (the design uses 14px spacing; the scale has 12 and 16), decide deliberately:
   - If the design's styles are linked to the library, the near-miss is likely an accident; use the token.
   - If the value recurs consistently across the design, it may signal a missing token; ask.
   - If it's a single one-off adjustment for optical alignment, the token plus a documented local exception may be acceptable — follow team convention.
3. **Prefer semantic tokens over primitive ones** where the system has both ("color-text-danger" rather than "red-600"), so themes and future changes propagate.
4. **Match components by role, not looks.** A design's "pill" might be the system's Tag, Badge, or Chip; each has different semantics and behavior. Pick by what it does.
5. **Record new tokens and components** as proposals for the design-system owners rather than silently adding them in feature code (see `design-systems`).

## Handling change during implementation

Designs change mid-build: research results arrive, stakeholders react, real data surprises everyone.

- Designers: announce changes explicitly to the people building, with what changed and why; don't silently update frames that developers are building from. Version or date the change.
- Developers: when a design changes under you, confirm scope and timing before switching; partial implementations of two versions are worse than either.
- Both: keep a short change log alongside the spec for anything changed after build began.
- If a change is large, re-estimate; handoff is also where schedule risk becomes visible (see `estimate-effort`).

## Collaboration models

| Model | How it works | Works well when | Watch out for |
|---|---|---|---|
| Sequential handoff | Design completes, then engineering builds | Small, well-understood changes using existing patterns | Late discovery of feasibility issues; rework |
| Overlapping | Engineering reviews from wireframes; design stays involved through build | Most product work | Needs discipline about the single source of truth |
| Pairing | Designer and developer work side by side, sometimes directly in code | Complex interactions, new patterns, tight deadlines | Decisions made in the moment must still be recorded |
| Design in code | Designers prototype or finish details in the codebase | Teams with code-fluent designers and a strong component library | Code quality and review standards still apply (`code-review`) |

Choose by the novelty and risk of the work, not by habit. The more novel the pattern, the more overlap pays off.

## Platform considerations

- **Web**: semantics come from HTML elements and attributes; responsive behavior is continuous across widths; browser and font rendering differ slightly. Specify behavior in terms of content and container size, not device names.
- **Native mobile**: platform conventions (navigation patterns, system controls, gestures, typography scaling) carry strong user expectations; designs should state where they intentionally depart from them. Dynamic type, safe areas, and platform accessibility services need explicit attention.
- **Cross-platform products**: decide per component whether it should look identical everywhere (brand consistency) or adapt to each platform (familiarity). Document the decision; mixing approaches arbitrarily confuses users and developers.
- **Desktop applications**: window resizing, multiple windows, menus, keyboard shortcuts, and high-density displays need specification beyond what web or mobile designs usually cover.

## Worked example: implementing from a mockup with gaps

*Situation*: an assistant is asked to implement a "Team members" settings page from a single high-fidelity mockup showing a table of five members, an "Invite" button, and a role dropdown per row. The codebase has a component library and a token file.

1. **Read the codebase first**: find the existing table, button, select, and dialog components; the token file; a similar settings page to copy conventions from (routing, data fetching, error handling, page structure).
2. **Map the mockup**: the table matches the library's table; the role dropdown matches the select component; the "Invite" button is a primary button. The mockup's grey header color is close to, but not exactly, the "surface-subtle" token — use the token. Row padding of 14px is between scale steps; other tables in the product use the medium step, so use that and note it.
3. **List the gaps**: empty state (no members besides the owner), loading, failed load, many members (pagination or scroll?), a member with a very long name or email, pending invitations (are they shown?), what non-admins see (read-only roles? hidden page?), what happens when someone changes their own role or removes the last admin, confirmation for removal, narrow screen layout of a five-column table.
4. **Ask** the batch of questions. For anything unanswered by the time work must proceed, follow existing product patterns: reuse the product's standard empty and error states; make roles read-only for non-admins; prevent removing the last admin with an explanatory message; on narrow screens, follow how other tables in the product adapt.
5. **Implement semantics first**: a real table with header cells, labelled selects with accessible names that include the member's name ("Role for Dana Ruiz"), focus moving into and out of the invite dialog correctly, status announcements when a role change saves or fails.
6. **Test** with zero, one, and fifty members, long names, slow network, failed requests, keyboard only, a screen reader, zoomed text, and both themes.
7. **Report back**: which components and tokens were used, the near-miss decisions, each gap and the assumption made, and what should be confirmed by the designer.

## Design QA

Design QA compares the implementation to the design intent and catches issues before users do. See `references/design-qa.md` for a detailed checklist. In outline:

- **Check on the real build**, in the real environment, with real data where possible, at several sizes, not just in the developer's local setup at one width.
- **Go state by state**: each designed state reachable and correct; undesigned states handled sensibly.
- **Check visual details**: tokens used (not near-miss raw values), typography, spacing, alignment, colors in all themes, icons, images.
- **Check behavior**: interactions, transitions, keyboard, focus, error handling, loading.
- **Check accessibility**: keyboard paths, focus visibility, screen reader names and announcements, contrast, zoom.
- **Check content**: real copy in place, truncation and wrapping as intended, localization if applicable.
- **Log issues** specifically (where, expected, actual, screenshot or recording, severity), in the team's tracker, and agree which block release.
- **Distinguish** deviations that change intent (fix) from acceptable platform differences (accept and document) from design problems revealed by real content (redesign).

Severity for design QA issues:

| Level | Examples |
|---|---|
| Blocking | Broken flow, inaccessible control, wrong or misleading content, missing error handling, layout broken at a supported size |
| High | Wrong component or variant, missing state, incorrect hierarchy, inconsistent with the system in a visible way |
| Medium | Noticeable spacing or alignment issues, minor motion differences, slight token mismatches |
| Low | Sub-pixel differences, platform rendering variations that don't affect perception |

## Decision guidance

**Pixel-perfect vs. system-faithful.** When a design's raw value conflicts with the nearest token, default to the token and ask. Pixel-matching a one-off value fragments the system; if the design needs a new value, it should become a deliberate addition.

**Custom vs. native controls.** Native controls (selects, date pickers, checkboxes) bring accessibility, platform familiarity, and robustness for free; custom ones cost a lot to make equally accessible. Prefer native or the design system's accessible components unless the design need is strong and the team can afford the work.

**Spec detail level.** More detail for new patterns, complex interactions, and teams new to each other; less for familiar patterns built with an established system by a team that works closely. A good test: could a competent developer who wasn't in the design discussions build it correctly from what's written?

**Static spec vs. prototype vs. code.** Static annotations suffice for layout and state. Interactive prototypes clarify flows and transitions. For complex interactions or motion, a coded reference (or a recording with timing values) removes ambiguity better than any description.

**When implementation must differ from design.** Raise it before building the alternative when possible. If the deadline forces it, ship the closest faithful version, document the difference, and log the follow-up.

**Who writes the spec?** Usually the designer, but specs written jointly — the designer stating intent, the developer adding implementation notes and questions — catch more gaps and leave fewer surprises.

**Generating code from design tools.** Auto-generated code or design-to-code exports can speed up scaffolding and extracting tokens, but they typically produce absolute positioning, raw values, and missing semantics. Treat output as a reference, map it to the codebase's components and tokens, and verify accessibility and responsiveness.

## Pitfalls

- **Happy-path handoff**: only the ideal state designed; developers invent empty, error, and loading states inconsistently.
- **Designs at two sizes only**: behavior in between, and beyond, left to chance.
- **Detached components and raw values** in design files, so developers can't tell what maps to the system.
- **Stale files**: developers build from an outdated frame because the current one isn't marked.
- **Decisions lost in chat**: answers given in messages never make it back into the spec.
- **Lorem ipsum and ideal data**: layouts that break on real names, numbers, and translations.
- **Specifying visuals, not semantics**: no heading levels, no accessible names, no focus order; accessibility retrofitted late.
- **Silent deviation**: developers change something for good reasons but don't tell anyone; design and product diverge.
- **QA by screenshot**: checking static captures at one size instead of using the running product.
- **Assets exported ad hoc**: inconsistent sizes, names, and formats; icons as raster images where vectors were needed; images without responsive variants.
- **Nitpick QA**: flooding the tracker with sub-pixel issues while a missing error state goes unnoticed. Prioritize.
- **Over-trusting design-tool measurements**: rendering differs between tools, browsers, and platforms; text metrics especially.
- **Spec as contract**: treating the spec as a fixed contract to be fulfilled to the letter, even when real data shows it was wrong. The goal is the user outcome; reopen the design when evidence demands it.
- **Late involvement**: engineering sees the design for the first time when it's "final", and feasibility problems force redesign under deadline.

## Quality bar and verification

A design is ready to build when:

- [ ] The current version is unambiguous, and explorations are archived or clearly separated.
- [ ] Elements map to existing components and tokens, and new ones are flagged with rationale.
- [ ] All relevant states and edge cases are designed or covered by stated rules.
- [ ] Responsive behavior is defined across the supported range, including extremes.
- [ ] Interactions, keyboard behavior, focus management, and motion (including reduced motion) are specified.
- [ ] Accessibility requirements code can't infer are written down.
- [ ] Real copy and realistic content are in place, with truncation and localization rules.
- [ ] Assets are prepared in usable formats with consistent naming.
- [ ] Engineering has reviewed it and open questions are answered or tracked.

An implementation is ready to ship when:

- [ ] Design QA was run on a real build across sizes, states, themes, and input methods.
- [ ] Blocking and high-severity issues are fixed; others are logged with owners.
- [ ] Tokens and system components are used rather than near-miss raw values.
- [ ] Keyboard, screen reader, contrast, and zoom checks pass.
- [ ] Any deviations from the design are known to the designer and documented.
- [ ] Spec updates made during build and QA are written back to the design source of truth, so the next person starts from what actually shipped.

**A final self-check for implementers**: open the built screen next to the design at the same size, then shrink it to the narrowest supported width, empty its data, break its network, and tab through it. If any of those surprises you, so will it surprise users.

## Depth on demand

- `references/states-and-edge-cases.md` — an exhaustive checklist of states, content extremes, and environmental conditions to specify or test. Read when preparing a spec or before implementing a complex screen.
- `references/design-qa.md` — a detailed design QA procedure and checklist, including how to write and prioritize QA issues. Read when reviewing an implementation against designs.
