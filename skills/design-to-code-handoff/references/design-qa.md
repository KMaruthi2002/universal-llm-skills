# Design QA Procedure

Read this when reviewing an implementation against its designs, whether you are the designer, the developer, or an assistant asked to compare a build with a mockup.

## Set up

- **Get a running build** in an environment as close to production as practical: a preview deployment, a branch build, a device build. Screenshots alone cannot show behavior, focus, responsiveness, or motion.
- **Use the current design version** and its annotations; confirm with the designer if unsure.
- **Prepare data**: accounts or fixtures that produce each state (empty, many, error, restricted). Without them, half the states can't be reached.
- **Agree on scope and severity rules** with the team before starting, so the issue list is proportionate.
- **Prepare tools**: the supported browsers and devices, a screen reader, a contrast checker, the ability to throttle network speed, and settings for zoom, text size, theme, and reduced motion.

## Pass 1 — Flow and behavior

Walk the main tasks end to end as a user would.

- Can every task be completed? Do transitions between screens behave as designed?
- Do interactions do what the spec says, including non-obvious ones (submit while pending, back navigation, cancel)?
- Are loading and error states reachable and correct? Force errors (disconnect the network, use invalid inputs, use a restricted account).
- Are success confirmations and undo present where designed?

## Pass 2 — Structure and accessibility

- **Keyboard**: tab through everything; order is logical, focus is always visible, nothing is unreachable, no keyboard traps, composite widgets use expected arrow-key behavior, dialogs trap and return focus.
- **Screen reader**: controls have meaningful names, headings form a sensible outline, landmarks exist, dynamic changes are announced, error messages are associated with fields.
- **Contrast**: text and essential non-text elements meet the product's standard in all states and themes.
- **Zoom and text size**: content reflows without loss or overlap at increased zoom and text sizes.
- **Reduced motion**: non-essential motion is reduced or removed when the preference is set.
- **Touch targets**: large enough and adequately spaced on touch devices.

## Pass 3 — Layout and responsiveness

- Check at the drawn sizes and in between, and at the narrowest and widest supported sizes.
- Elements stack, wrap, hide, or reorder as specified.
- No horizontal scrolling unless intended; no clipped content; no overlapping elements.
- Long content truncates or wraps as specified.
- Orientation changes and on-screen keyboards don't break the layout.

## Pass 4 — Visual details

- **Components**: the right component and variant from the system is used, not a lookalike.
- **Tokens**: colors, type styles, spacing, radii, shadows match tokens; flag near-miss raw values, which are the main source of drift.
- **Typography**: correct styles, weights, line heights; no unexpected font fallbacks.
- **Spacing and alignment**: rhythm matches intent; grouping is preserved.
- **Icons and images**: correct assets, sizes, alignment; images crisp on high-density screens; correct cropping.
- **Themes**: everything correct in each supported theme.
- **Motion**: durations, easing, and choreography match the spec closely enough to preserve the intended feel.

## Pass 5 — Content

- Final copy is in place; no placeholders or lorem ipsum.
- Terminology matches the product's glossary.
- Dates, numbers, and currencies are formatted per locale.
- Localization: expanded strings fit, right-to-left mirroring works if supported.

## Writing QA issues

Each issue should allow someone to find and fix it without asking:

- **Title**: what's wrong, specifically ("Primary button uses secondary variant on Settings > Billing")
- **Where**: screen, component, state, size, browser or device, theme
- **Expected**: per the design (link to the frame or annotation)
- **Actual**: what the build does (screenshot or recording)
- **Steps to reproduce** when it depends on state or data
- **Severity**: per the agreed scale
- **Type**: implementation bug, missing spec (design never defined it), design problem revealed by real content, or acceptable platform difference

Group many small visual issues into one ticket per screen or component rather than dozens of separate tickets, unless the team prefers otherwise.

## Deciding what to do with each issue

| Type | Action |
|---|---|
| Implementation doesn't match a clear spec | Fix in code |
| Spec was missing or ambiguous | Designer decides; update spec; then fix |
| Real content or data reveals a design flaw | Designer revises the design; may be follow-up work |
| Platform rendering difference that preserves intent | Accept and note |
| Deliberate deviation for technical reasons | Confirm with designer; document |

## Sign-off

- Blocking and high-severity issues are fixed and verified on a fresh build.
- Remaining issues are logged with owners and agreed timing.
- Spec updates made during QA are written back to the design source of truth.
- Lessons for the next handoff (recurring gaps, unclear annotations) are noted, so the process improves.
