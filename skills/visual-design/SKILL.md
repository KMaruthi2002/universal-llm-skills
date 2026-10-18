---
name: visual-design
description: >-
  Build a coherent visual language for an interface, document or brand
  surface from its given constraints: typography (type scales, pairing,
  measure, leading, weights, numerals), color (palette construction, roles,
  contrast, dark mode, state and meaning), spacing scales, elevation and
  shape, imagery, illustration and iconography. Presents justified options
  instead of a house look, and extends an existing brand rather than
  replacing it. Use when choosing fonts or colors, defining a palette or type
  scale, theming, adding dark mode, making something "look more polished",
  "more professional" or "on-brand", or when visuals feel inconsistent. For
  screen structure use ui-design-fundamentals; for turning choices into
  tokens and components use design-systems.
metadata:
  category: design
  related: ui-design-fundamentals, design-systems, layout-and-responsive-design, accessible-design, motion-design, data-visualization, presentations, website-and-landing-pages, design-critique
---

# Visual Design

Visual design is the system of type, color, space, shape and imagery that makes an interface legible, gives it character, and makes its parts feel like they belong together. It is not decoration added at the end. Every visual property either carries meaning (hierarchy, state, grouping, brand) or adds noise.

This skill teaches how to **derive** a visual language from constraints — brand, audience, content, platform, medium, accessibility — and how to **extend** one that already exists. It deliberately prescribes no palette, typeface or aesthetic.

**Out of scope here:** screen structure and component choice (`ui-design-fundamentals`), grids and responsive behaviour (`layout-and-responsive-design`), encoding them as tokens and components (`design-systems`), charts (`data-visualization`), animation (`motion-design`).

## Core principles

1. **Constraints first, taste last.** Start from what is fixed: brand assets, platform conventions, accessibility requirements, content type, rendering medium (screen, print, projector, e-ink), localisation needs. Taste operates in the space that remains. Why: choices made against constraints are defensible and durable; choices made from personal or trend preference get redone.
2. **Few values, used consistently.** A small set of sizes, colors and spacings applied systematically looks intentional; many near-duplicate values look accidental. Restraint is what makes emphasis possible.
3. **Every property has a job.** Before adding a color, weight, border or shadow, name what it communicates. If the answer is "it looked empty", the fix is usually spacing or content, not ornament.
4. **Contrast creates hierarchy; similarity creates unity.** Make important differences large enough to be seen at a glance; make unimportant differences disappear.
5. **Legibility is non-negotiable.** Character must never cost readability. Contrast, size, measure and leading have evidence-based floors (below). Brand expression lives above them.
6. **Design for the real rendering conditions.** Font rendering differs across OSes, screens vary in gamut and brightness, users zoom, override fonts and switch to dark or high-contrast modes. A visual language that only works on the designer's monitor does not work.

## Discovering context

Before proposing anything, find out:

- **Existing brand:** logo, brand colors (with any official values in RGB/HEX, CMYK, Pantone), licensed typefaces, imagery and illustration style, tone words. Ask for the brand book; inspect the marketing site and product.
- **Existing product visuals:** what fonts, sizes, colors and spacings the live product actually uses. In code, look for theme files, CSS custom properties, token JSON, Tailwind/theme configs, SCSS variables, platform asset catalogs. In design files, look for shared styles and variables.
- **Licensing:** whether fonts are licensed for web embedding, app embedding, or only desktop. A font in the brand book may not be usable in the product.
- **Platform:** native apps often should use (or at least respect) system fonts and system colors; the web has more freedom but costs performance for each font file.
- **Audience and environment:** age (older eyes need larger text and more contrast), reading load, lighting conditions, cultural associations of color.
- **Languages and scripts:** Latin only? Cyrillic, Greek, Arabic, Hebrew, Devanagari, CJK? Script coverage eliminates many typefaces.

Honour what exists. If the brand palette has poor contrast for text, do not discard it — derive accessible tints/shades for UI roles and keep the official values for brand moments (logo, large display areas), then explain the split.

## Typography

### Choosing typefaces

Choose for function first, voice second.

| Factor | What to check |
|---|---|
| Legibility at body size | Generous x-height, open apertures, distinguishable `Il1` and `O0`, clear punctuation. |
| Script and language coverage | All required scripts, diacritics, and punctuation for target locales. |
| Weights and styles | At least regular, a bolder weight, and italics if text content needs them. Variable fonts can provide a range in one file. |
| Numerals | Tabular (fixed-width) figures for tables, prices, timers; proportional for prose. Lining vs. old-style to match context. |
| Rendering | Test on the target OSes and at small sizes; some display faces fall apart below ~16 px. |
| Performance and licensing | Number and size of font files; web/app licence. System font stacks cost nothing to load. |
| Voice | Formal, technical, friendly, editorial, institutional, playful — consistent with brand attributes. |

**Pairing heuristics** (options, not rules):

- **One family** with multiple weights is the safest and often the best choice for product UI.
- **Two families** when you need clear contrast in role: e.g. a distinctive display face for headings plus a highly legible text face for body. Pair faces that differ clearly in one dimension (structure or classification) but share proportions such as x-height; faces that are *almost* the same look like a mistake.
- **A monospace** only where content is code, data or fixed-width by nature.
- Three or more families rarely helps outside editorial or expressive work.

### Type scale

A type scale is a limited set of sizes with consistent relationships. Two common approaches:

- **Modular (ratio-based):** each step multiplies by a ratio. Smaller ratios (≈1.125–1.2) suit dense UI with many levels; larger ratios (≈1.25–1.333) suit marketing and editorial; ≈1.5 and above suit expressive, display-led layouts with few levels.
- **Hand-tuned:** pick sizes that work at each role and round them to the spacing grid. Many mature design systems do this because pure ratios produce awkward values at extremes.

Guidance:

- Define sizes by **role** (display, heading levels, body, small/caption, label), not by "h1 = 32".
- Five to eight sizes cover most products. More than ten usually indicates drift.
- **Body text size:** for web reading, 16 CSS px is a common floor for body copy, and many reading-heavy products go larger. Platform defaults are sensible starting points (e.g. Apple's default body text is 17 pt on iOS). Very small text (under ~12 px) should be rare and never carry essential information.
- Use relative units on the web (`rem`/`em`) so user font-size preferences are respected; WCAG 1.4.4 requires text to resize to 200% without loss of content or function.
- Fluid type with `clamp()` is useful for display sizes; include a `rem` component in the formula so it still responds to zoom (see `layout-and-responsive-design`).

### Measure (line length)

- **45–75 characters per line** (including spaces) is the widely cited range for comfortable reading of continuous text, with around 66 often given as ideal (Bringhurst, *The Elements of Typographic Style*). WCAG 1.4.8 (AAA) recommends no more than 80 characters (40 for CJK).
- Constrain text columns with a `max-width` in `ch` or `em` rather than letting text span a wide screen.
- Short UI strings (labels, buttons) are not continuous reading and are not bound by this.

### Leading (line height)

- Body text typically reads well at **1.4–1.6× the font size**; WCAG 1.4.8 (AAA) recommends at least 1.5 for blocks of text.
- Headings need tighter leading (≈1.1–1.3) because large sizes with body leading look disconnected.
- Longer lines need more leading; short lines need less.
- **Layouts must survive user overrides** (WCAG 1.4.12, AA): line height 1.5×, paragraph spacing 2×, letter spacing 0.12×, word spacing 0.16× must not break content. Avoid fixed-height text containers.

### Weight, case and spacing

- Use weight changes sparingly; two or three weights in a UI is typical. Very light weights (under ~300) fail on low-quality screens and at small sizes.
- ALL CAPS reduces reading speed for long text; for short labels it works if letter-spacing is opened slightly. Screen readers may spell out all-caps text in some cases — apply caps with CSS `text-transform`, not in the source string.
- Never use letter-spacing to fit text into a box.
- Italic for emphasis and titles; underline is reserved for links on the web.
- Left-aligned (start-aligned) text is the default for reading in LTR languages; centred text suits only short passages; justified text without good hyphenation creates rivers, and WCAG 1.4.8 (AAA) recommends against it.

## Color

### Build from roles, not swatches

A palette is a set of **roles** the interface needs, each filled by values that work in context:

| Role | Purpose |
|---|---|
| Background / surface (several levels) | Page, containers, raised layers. |
| Foreground / text (primary, secondary, disabled) | Readable content at different emphasis. |
| Border / divider | Structure, input outlines. |
| Accent / brand / primary | Primary actions, selected states, key highlights. |
| Status: success, warning, danger/error, info | Semantics that users must recognise. |
| Focus indicator | Keyboard focus, must contrast with everything it can sit on. |
| Data visualisation | Categorical, sequential and diverging scales (see `data-visualization`). |

Then define each role in each theme (light, dark, high contrast if supported). This is the bridge to semantic tokens (`design-systems`).

### Constructing ramps

- For each hue you need, build a ramp of tints and shades (commonly 9–12 steps). Generate it in a **perceptually uniform color space** such as OKLCH or CIELAB/LCh, where equal steps in lightness look equal; ramps made by mixing with white/black in sRGB tend to go muddy or uneven.
- Keep perceived lightness consistent across hues at the same step, so "step 600" means roughly the same contrast for blue, green and red. This makes roles swappable and contrast predictable.
- Tools (examples only): Leonardo, Radix-style generators, Huetone, color.js, Figma plugins, or code.
- Validate every text/background pair you will actually use, not just the ramp.

### Contrast (the numbers)

WCAG 2.2 Level AA, the most commonly required baseline:

| Content | Minimum ratio | Criterion |
|---|---|---|
| Body text and images of text | 4.5:1 | 1.4.3 |
| Large text (≥24 px regular, or ≥18.66 px / 14 pt bold) | 3:1 | 1.4.3 |
| UI component boundaries, states, focus indicators, meaningful graphics (icons, chart lines) | 3:1 against adjacent colors | 1.4.11 |
| Level AAA text | 7:1 (4.5:1 large) | 1.4.6 |

Notes:

- Logos and purely decorative text are exempt; disabled controls are exempt from 1.4.3 but should still be perceivable as disabled.
- WCAG 2's luminance formula is imperfect (it overstates contrast for some dark pairs and understates it for some light-on-dark pairs). **APCA** is a newer perceptual model being developed for WCAG 3; it is not yet a legal or normative standard. Meet WCAG 2 for compliance; APCA can inform choices for dark themes and thin type.
- Text on images or gradients must meet contrast at the **worst point**; use scrims, overlays or solid panels.

### Meaning and culture

- **Never use color as the only cue** (WCAG 1.4.1): pair status colors with icons, text or patterns. About 8% of men and 0.5% of women of Northern European ancestry have a red–green color vision deficiency; red/green pairs are the classic failure.
- Keep semantic colors reserved: if red means danger, do not also use it as a brand accent on harmless buttons.
- Color associations vary by culture and domain (red can mean loss in Western finance and gain in some East Asian markets; white is associated with mourning in some cultures). Check for the target audience.
- Saturated colors over large areas cause fatigue; reserve them for emphasis.

### Proportion

A common heuristic is that most surfaces are neutral, a smaller portion carries secondary color, and a small portion carries the accent (sometimes stated as 60/30/10). Treat it as a reminder that accents work by scarcity, not as a formula.

### Dark mode

Dark mode is a separate theme, not an inversion.

- Do not simply invert; **re-map roles**. Text, surfaces and accents each need dark-theme values that meet contrast.
- Pure black (#000) backgrounds maximise contrast and save power on OLED, but can cause halation/smearing for some users with bright text; many systems use a very dark grey. Both are defensible — decide by audience and brand.
- Avoid pure white text on very dark backgrounds for long reading; slightly reduced brightness is more comfortable.
- **Desaturate and lighten accents**; saturated mid-tones that work on white often vibrate or fail contrast on dark.
- Elevation reads as **lighter surfaces** rather than shadows, since shadows are barely visible on dark.
- Re-check images, illustrations, logos and charts; provide dark variants where needed.
- Respect the OS preference (`prefers-color-scheme`) and offer an override if the product has a settings area. Avoid a flash of the wrong theme on load.
- Also consider forced-colors / high-contrast modes (Windows): use system colors and do not rely on background images or box-shadows for essential boundaries.

## Spacing

- Choose a **base unit** (4 and 8 are common because they divide well and align with many platform grids) and a scale built from it (e.g. multiples or a non-linear progression for larger gaps).
- Use spacing to express relationships: tight within a group, larger between groups, largest between sections (see grouping in `ui-design-fundamentals`).
- Keep the scale small — around 8–12 steps — and avoid one-off values.
- Align type to spacing where practical (line heights that resolve to the base unit), but do not contort type to a baseline grid on the web if it fights responsive behaviour; consistency of vertical rhythm matters more than mathematical purity.
- Padding inside a container should usually be at least as large as the gap between its children, otherwise content looks cramped against edges.

## Shape, elevation and borders

- **Corner radius** carries tone: sharper reads more technical/formal, rounder reads softer/friendlier. Pick a small set (e.g. none, small, large, full) and nest correctly — an inner element's radius should be smaller than its container's (roughly outer radius minus padding) so curves look concentric.
- **Elevation** (shadow or surface tone) communicates layering: what floats above what. Use a few levels tied to meaning (resting, raised, overlay, modal). Shadows on everything flatten hierarchy.
- **Borders vs. shadows vs. background tints:** choose one primary method of separating surfaces and use the others sparingly. Many products mixing all three look busy.
- Non-text boundaries that identify controls (input outlines, toggle tracks) need 3:1 contrast (WCAG 1.4.11).

## Imagery, illustration and iconography

### Photography and illustration

- Define *what* imagery is for (show the product, convey mood, explain a concept, humanise) before choosing a style.
- Consistency of treatment — lighting, crop, color grading, illustration line weight and palette — matters more than any single image's quality.
- Represent people inclusively and realistically for the audience; avoid tokenism and clichés (see `accessible-design`).
- Provide alt text by purpose: informative images describe content; decorative images get empty alt (see `accessible-design`).
- Optimise: responsive sizes, modern formats where supported, explicit dimensions to avoid layout shift (see `web-performance-audit`).

### Icons

- Use **one icon family** (or icons drawn to identical rules): same grid, stroke width, corner treatment, fill style and optical size.
- Size icons to the text they accompany and align them optically, not just mathematically.
- Label icons unless the meaning is near-universal in context; provide accessible names for icon-only buttons.
- Icons that convey meaning need 3:1 contrast (WCAG 1.4.11).
- Filled vs. outlined variants can indicate selected vs. unselected state — if used, be consistent.
- Mind cultural specificity (mailboxes, hand gestures, currency symbols, check marks vs. crosses in some locales).

## Process: building a visual language

1. **Gather constraints and assets** (Discovering context, above).
2. **Write 3–5 attributes** that describe the desired character, each paired with what it is *not* ("confident, not loud"; "precise, not cold"). Get agreement on these; they become the test for every later choice.
3. **Collect references** that express the attributes — including ones outside the product category — and note what specifically each contributes. References inform; they are not to be copied.
4. **Explore two or three distinct directions** at low cost: one screen or card rendered in each, with type, color, spacing and shape varied together. Present each with a rationale tied to the attributes and trade-offs (e.g. "Direction B is warmer but its accent needs a darker variant for text"). Do not present a single "correct" answer unless the brand already dictates it.
5. **Converge**: choose with the stakeholder, then systematise — type scale by role, color roles per theme, spacing scale, radius and elevation sets, icon rules.
6. **Apply to hard cases**: dense tables, forms with errors, long localised strings, dark mode, empty states, data visualisations. Most visual languages that fail, fail here, not on the hero.
7. **Encode** as tokens and document usage (`design-systems`).
8. **Verify** (below).

### Illustrative example (not a prescription)

> Constraints: a regional public library; brand book specifies a deep green and a slab-serif logo; audience includes older readers and children; content is long event descriptions and catalogue listings; must meet AA.
> Attributes: welcoming, not childish; civic, not bureaucratic; readable above all.
> Reasoning: the brand green is too dark for large surfaces but excellent for text and primary buttons; derive a ramp in OKLCH and use light tints for surfaces. The logo's slab serif is too heavy for body text, so use it (if licensed for web) for headings only and pair with a highly legible humanist sans for body at a generous base size. Status colors get icons as well as color. Images of real patrons rather than stock.
> Two alternative directions might be offered: one with a serif body face for an editorial feel, one fully sans for maximum UI clarity.

A different library might reasonably end up somewhere entirely different. That is the point.

## Typography and color in demanding contexts

The hero screen is easy. The visual language proves itself in the contexts below; design for them explicitly.

### Data-dense interfaces

- Use **tabular figures** for any column of numbers, timers and prices so digits align and values do not jitter as they update.
- Right-align numbers in tables (or align on the decimal); left-align text; keep units in headers rather than repeating them per cell.
- Reduce the number of type sizes, not their legibility: differentiate with weight and color role rather than many sizes.
- Zebra striping, row dividers or neither: pick one method of row separation. Dense tables often read best with subtle dividers and generous row height rather than heavy stripes.
- Reserve color for exceptions (alerts, deltas, selections). A table where every cell is colored has no signal left.

### Long-form reading

- Larger body size, constrained measure, comfortable leading, clear paragraph spacing, and a strong but quiet heading hierarchy.
- Consider a text face designed for extended reading; check italics and bold exist and are distinct.
- Provide visible link styling that does not disrupt reading (underline thickness and offset can be tuned).

### Multilingual and multi-script

- Verify glyph coverage for every script; pair a Latin face with a script-appropriate partner (with matched x-height/visual weight) if one family does not cover all.
- CJK text often needs larger line height and no letter-spacing; Arabic and Devanagari have tall ascenders/descenders that clip in tight line heights.
- Do not rely on italics or all-caps for emphasis in scripts that lack them.

### Status and semantic color at scale

- Each status needs at least three values per theme: a strong value for icons and text, a subtle surface for backgrounds, and a border. Check text-on-subtle-surface contrast, not just text-on-white.
- Keep warning (amber/yellow families) legible: yellow text on white almost always fails contrast; use dark text on a yellow surface or a darker shade for text.
- Disabled is not a status color; it is a reduced-emphasis role and must still be distinguishable.

## Worked reasoning: from a brand color to UI roles

Illustrative only — the numbers are an example of the method, not a recommended palette.

1. The brand provides one hex value for its primary color. Measure it: suppose it reaches 3.2:1 against white.
2. Conclusion: acceptable for large text and UI component boundaries (≥3:1), **not** for body text or small text links (needs 4.5:1).
3. Build a ramp around it in OKLCH, keeping hue and adjusting lightness (and gently reducing chroma at the extremes so the darkest and lightest steps do not look garish or grey).
4. Pick the step that reaches ≥4.5:1 on white for `text.accent` and `link`; keep the original value for large brand surfaces, illustrations and the primary button background **if** the button text on it meets 4.5:1 (check white vs. dark text on the brand color; choose whichever passes).
5. For dark theme, choose a lighter step that reaches ≥4.5:1 on the dark surface for accent text, and a slightly desaturated mid-step for button fills.
6. Record each pair and ratio in the documentation, so the reasoning survives the next designer.

The brand keeps its identity; the UI gets legible roles; nothing was invented that the brand owner has not seen.

## Auditing an existing visual language

When asked to "clean up" or "make consistent" an existing product:

1. **Extract actual values in use.** In code, search stylesheets and components for hex/rgb/hsl values, font sizes, line heights, spacings, radii and shadows; count occurrences. In design files, list local (non-library) styles.
2. **Cluster near-duplicates** (e.g. several greys within a small lightness range, font sizes 13/14/15 px used for the same role).
3. **Map clusters to roles** and propose a canonical value per role, preferring the most common value unless it fails accessibility.
4. **Show the before/after** on a few representative screens so stakeholders see that consolidation does not erase character.
5. **Hand over to tokens** (`design-systems`) so the consolidation sticks.

## Presenting visual options

When you offer directions, make them genuinely different and comparable:

- Apply each direction to the **same** content and the **same** hard case (e.g. a form with an error and a data table), not each to its most flattering screen.
- Vary type, color, shape and spacing **together** as a coherent set; mixing one direction's type with another's color later is the stakeholder's prerogative, but each option should stand on its own.
- State, for each: the attributes it expresses, its trade-offs (performance cost of fonts, contrast headroom, how it scales to dense views), and what it would take to implement within the existing system.
- Recommend one if asked, with reasons; do not disguise a preference as the only option.

## Decision guidance

| Question | Choose A when… | Choose B when… |
|---|---|---|
| System font stack vs. custom font | Native feel, performance and broad script coverage matter most; product UI. | Brand distinctiveness matters and licensing/performance budget allows. |
| One family vs. pairing | Product UI, data-dense screens, many languages. | Editorial, marketing, or brand needs a distinct voice in headings. |
| Ratio scale vs. hand-tuned scale | Starting fresh, few sizes, expressive layouts. | Many UI levels, need precise control at small sizes. |
| Shadows vs. borders for surfaces | Layering and overlays are central, light themes. | Dense UIs, dark themes, printing, forced-colors support. |
| Near-black vs. pure black dark background | Long reading, bright accents, halation concerns. | OLED power saving, very high contrast brand, media viewing. |
| Strong accent color vs. neutral UI | Few key actions that must stand out; brand-forward products. | Content (photos, data, documents) should carry the color. |

## Pitfalls

- **Default aesthetic syndrome:** the same fashionable sans, purple/blue gradient accent, rounded cards and soft shadows applied regardless of product — the hallmark of generic or AI-generated UI. Fix by re-deriving from attributes and constraints.
- **Too many values:** dozens of greys, font sizes like 13/14/15 px used interchangeably, spacing like 10/12/14/15. Audit and collapse to a scale.
- **Brand colors used for text** without checking contrast.
- **Low-contrast "elegant" grey text** — fails AA and is hard to read for many users.
- **Color-only status** (red/green dots without labels).
- **Inverted dark mode** with the same saturated accents and shadows.
- **Ornament instead of hierarchy:** gradients, glows, glass effects, and shadows used because space looked empty.
- **Mixed icon families** and inconsistent stroke weights.
- **Fonts without the needed glyphs**, causing fallback fonts to appear mid-word in other languages.
- **Text baked into images** — not translatable, not searchable, not resizable, often fails contrast.
- **Copying a reference** too literally, including its brand-specific traits.
- **Ignoring rendering:** thin weights that disappear on Windows or low-DPI screens; colors that look different on wide-gamut vs. sRGB displays.

## Quality bar and verification

- [ ] Every visual choice traces to an attribute, constraint or role; you can explain each in one sentence.
- [ ] The palette is defined by roles for every supported theme, and every used text/background pair has been measured: ≥4.5:1 body, ≥3:1 large text, ≥3:1 for UI boundaries, icons and focus indicators (WCAG 2.2 AA), or the project's stricter target.
- [ ] No information is conveyed by color alone.
- [ ] Type scale has a bounded set of role-named sizes; body text is comfortably legible on target devices; measure is within ~45–75 characters for reading text; leading ~1.4–1.6 for body.
- [ ] Text spacing override test (WCAG 1.4.12) and 200% zoom test do not break layouts.
- [ ] Spacing, radius and elevation use small, named scales; no stray one-off values.
- [ ] Icons are one consistent family with accessible names where needed.
- [ ] Dark mode (if any) is checked screen by screen, including images and charts.
- [ ] Hard cases (forms with errors, dense tables, long strings, empty states) look as resolved as the hero screen.
- [ ] If extending a brand, the new work is indistinguishable in grammar from the existing system, and any deviations are listed with reasons.

**How to check**, depending on capability: run contrast checks with a tool or script (e.g. browser devtools, axe, a WCAG contrast calculator, or compute relative luminance in code); render in a browser and test zoom, text-spacing bookmarklets and `prefers-color-scheme`; simulate color vision deficiencies (devtools rendering emulation, Sim Daltonism, Color Oracle); view on more than one OS and screen; print a page if print matters. If you cannot render, list each color pair with its computed ratio and each type role with size, weight and line height, so a reviewer can verify.
