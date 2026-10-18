---
name: accessible-design
description: >-
  Design products that people with disabilities can use from the first
  sketch, not after an audit: color and contrast, text size and spacing,
  visible focus, target sizes, keyboard and screen-reader-friendly structure
  and semantics, headings and landmarks, accessible names, forms and error
  messaging, alt text and image descriptions, captions and transcripts,
  motion and flashing, cognitive accessibility and plain language, and
  inclusive representation and language. Grounded in WCAG 2.2 and platform
  guidance. Use when designing or building any UI, document, or media and you
  want it accessible, inclusive, ADA/EAA/Section 508 ready, screen-reader or
  keyboard friendly, or "usable by everyone". To evaluate an existing product
  for conformance use accessibility-audit instead.
metadata:
  category: design
  related: accessibility-audit, ui-design-fundamentals, visual-design, interaction-design, layout-and-responsive-design, motion-design, ux-writing, design-systems, frontend-development
---

# Accessible Design

Accessible design means people with a wide range of abilities — visual, auditory, motor, cognitive, speech, and temporary or situational limitations — can perceive, understand, navigate and operate what you make. It is cheapest and most effective when built in from the start: retrofitting accessibility into a finished design is slower, more expensive and usually produces worse results than designing it in.

This skill is for **making** accessible things. It complements `accessibility-audit`, which is for **evaluating** an existing product against standards. Visual specifics (`visual-design`), layout (`layout-and-responsive-design`), behaviour (`interaction-design`) and motion (`motion-design`) each carry accessibility guidance too; this skill brings it together and adds what they do not cover.

## Why it matters

- **Scale:** the WHO estimates about 1.3 billion people — roughly 1 in 6 — experience significant disability. Many more have temporary (broken arm) or situational (bright sunlight, holding a baby, noisy room) limitations, and ageing populations increase low vision, hearing loss and motor limitations.
- **Law:** many jurisdictions require accessibility, typically by reference to WCAG: e.g. the European Accessibility Act (applies to many products and services from June 2025, via EN 301 549), the ADA in the US (courts and DOJ rules reference WCAG; DOJ's 2024 Title II rule adopts WCAG 2.1 AA for state and local government), Section 508 for US federal ICT, the UK Equality Act and public sector regulations, AODA in Ontario. Obligations vary — identify which apply; this skill is not legal advice.
- **Quality:** accessible design is usually better design for everyone: clearer structure, better contrast, larger targets, plainer language, captions in noisy places, keyboard efficiency.

## Standards to anchor on

- **WCAG 2.2** (W3C, 2023) is the current widely referenced standard, organised under four principles — **Perceivable, Operable, Understandable, Robust** — with success criteria at levels A, AA and AAA. **Level AA is the common legal and contractual target.** WCAG 2.2 is backward compatible with 2.1 and 2.0, adding criteria such as Focus Not Obscured (2.4.11), Dragging Movements (2.5.7), Target Size Minimum (2.5.8), Consistent Help (3.2.6), Redundant Entry (3.3.7) and Accessible Authentication (3.3.8); it removed 4.1.1 Parsing.
- **Platform guidance:** Apple Human Interface Guidelines (accessibility), Android/Material accessibility guidance, Microsoft inclusive design and Fluent guidance.
- **WAI-ARIA Authoring Practices Guide (APG):** keyboard and semantics patterns for custom widgets.
- **WCAG 3** is in development and not yet a standard; do not cite it for conformance.

Always confirm the target the project has committed to (often "WCAG 2.2 AA" or "2.1 AA"); design to at least that, and go beyond where cheap.

## Core principles

1. **Design for the range, not the average.** Consider the persona spectrum (Microsoft Inclusive Design): permanent, temporary and situational versions of each limitation. A solution for one-handed use by an amputee also helps a parent holding a child and a commuter holding a rail.
2. **Multiple ways to perceive.** Do not depend on any single sense: color plus text or shape; audio plus captions; visual layout plus semantic structure.
3. **Structure is the interface for many users.** Screen-reader, voice-control and keyboard users navigate by headings, landmarks, labels and focus order. If the structure is wrong, the visual design is irrelevant to them.
4. **Native first.** Platform-native controls come with keyboard support, semantics and assistive-technology integration that custom controls must laboriously recreate. "No ARIA is better than bad ARIA" (the first rule of ARIA use: if a native element exists, use it).
5. **User settings win.** Respect zoom, text size, color schemes, contrast modes, reduced motion and assistive technology. Never fight them.
6. **Nothing about us without us.** Include disabled people in research and testing (see `ux-research`, `usability-evaluation`). Checklists catch defects; people reveal whether the experience actually works.

## Discovering context

- **Commitment and obligations:** which standard and level; which jurisdictions; contractual requirements (procurement often asks for an Accessibility Conformance Report based on the VPAT template).
- **Existing system support:** do the design-system components already handle focus, semantics and contrast? Which are known-problematic? (See `design-systems`.)
- **Known issues:** previous audit reports, user complaints, assistive-tech bug lists.
- **Audience specifics:** older users, users with cognitive disabilities, low-literacy users, deaf communities (sign language needs), users in low-bandwidth or low-end-device conditions.
- **Platforms and assistive technologies to support:** e.g. screen readers (VoiceOver on macOS/iOS, TalkBack on Android, NVDA and JAWS on Windows, Narrator), voice control, switch access, screen magnifiers, Windows high-contrast/forced colors.

## Design areas

### Color and contrast

| Requirement | Minimum (WCAG 2.2) | Criterion |
|---|---|---|
| Normal text | 4.5:1 | 1.4.3 (AA) |
| Large text (≥24 px, or ≥18.66 px bold) | 3:1 | 1.4.3 (AA) |
| Enhanced text | 7:1 normal / 4.5:1 large | 1.4.6 (AAA) |
| UI component boundaries and states, graphical objects needed to understand content | 3:1 against adjacent colors | 1.4.11 (AA) |
| Information not by color alone | Color is never the sole visual means | 1.4.1 (A) |

Design practice:

- Check contrast for every state (default, hover, focus, active, disabled is exempt but should still be distinguishable), every theme (light, dark, high-contrast), and text on images or gradients at the worst point.
- Pair status colors with icons and text. Links in body text need an underline or other non-color cue unless they reach 3:1 contrast against surrounding text *and* gain a cue on hover/focus.
- Charts: use direct labels, patterns or shapes, and color palettes distinguishable under common color vision deficiencies (see `data-visualization`).
- Support forced-colors / high-contrast modes: boundaries should not rely only on background color or box-shadow.

### Text and readability

- Body text sized for comfortable reading on the target devices (16 CSS px is a common web floor); relative units so user settings apply.
- **Resize to 200%** without loss of content or function (1.4.4) and **reflow** at 320 CSS px width / 400% zoom (1.4.10).
- **Text spacing overrides** (1.4.12): line height 1.5×, paragraph spacing 2×, letter spacing 0.12×, word spacing 0.16× must not break layout — avoid fixed-height text boxes.
- Line length about 45–75 characters, line height about 1.5 for body, left/start-aligned, not justified (1.4.8 AAA guidance) — see `visual-design`.
- Avoid images of text (1.4.5) except logos.
- Avoid long passages in all caps, italics or very light weights.

### Focus visibility and keyboard

- Every interactive element is reachable and operable by keyboard (2.1.1) with no traps (2.1.2).
- **Focus order** follows a logical reading sequence (2.4.3); visual reordering must not scramble it.
- **Focus indicator visible** (2.4.7, AA). Design it deliberately, do not leave it to defaults that may be invisible on your colors. A robust indicator has at least 3:1 contrast against adjacent colors (1.4.11) and a substantial area; WCAG 2.4.13 Focus Appearance (AAA) describes a strong target: an area at least as large as a 2 CSS px perimeter around the component, with at least 3:1 change in contrast between focused and unfocused states.
- **Focus not obscured** (2.4.11, AA): sticky headers, footers, cookie banners and chat widgets must not completely hide the focused element.
- Provide **skip links** or landmark navigation to bypass repeated blocks (2.4.1).
- Design keyboard interactions for custom widgets following APG patterns (arrow keys within menus, tabs, grids; Escape to close; Enter/Space to activate).
- Manage focus on dynamic changes: move focus into dialogs and return it to the trigger on close; after deletion, move focus to a sensible neighbour; after route change in single-page apps, move focus to the new content or heading.

### Target size and motor access

- **WCAG 2.5.8 (AA):** targets at least 24×24 CSS px, or spaced so a 24 px circle on each does not overlap others (with exceptions for inline text links and others).
- **WCAG 2.5.5 (AAA)** and platform guidance: 44×44 CSS px (WCAG AAA), 44×44 pt (Apple), 48×48 dp (Material). Use these for touch-first and primary actions.
- **Pointer gestures (2.5.1):** multi-point or path-based gestures need a single-pointer alternative (buttons for pinch-zoom, swipe).
- **Dragging (2.5.7, AA):** provide a non-drag alternative (move buttons, menus, keyboard reorder).
- **Pointer cancellation (2.5.2):** trigger on release so accidental presses can be aborted.
- **Motion actuation (2.5.4):** shake or tilt features need a UI alternative and a way to disable.
- **Timeouts (2.2.1):** warn before session expiry and allow extension; avoid time limits where possible.

### Semantics and structure

Design documents should specify structure, not just appearance, so engineers can implement it:

- **Headings:** one clear page title, then a logical hierarchy (do not skip levels for visual size; style is separate from level). Screen-reader users commonly navigate by headings.
- **Landmarks / regions:** header, navigation, main, complementary, footer, search, and named regions for major areas.
- **Lists, tables and forms** marked as such; data tables with proper header cells; no layout tables.
- **Accessible names** for every interactive element: visible label where possible; for icon-only buttons, a name describing the action ("Close dialog", "Search"). Visible label text should be contained in the accessible name (2.5.3 Label in Name) so voice-control users can say what they see.
- **Roles, states and properties** (4.1.2): toggles expose pressed/checked, disclosures expose expanded/collapsed, current page in navigation is exposed.
- **Status messages** (4.1.3): toasts, inline save confirmations and result counts are announced without moving focus (live regions or platform equivalents).
- **Page titles** (2.4.2) that describe the page and update in single-page apps.
- **Language** of the page and of passages in other languages declared (3.1.1, 3.1.2) so screen readers pronounce correctly.

A practical method: annotate designs with heading levels, landmarks, reading/focus order, accessible names for non-text controls, and dynamic announcements. Many teams use an annotation kit in their design tool; the content matters more than the tool.

### Forms

- Visible, persistent labels (not placeholders as labels); programmatic association.
- Instructions before the field, not only after an error (3.3.2).
- Required fields indicated in text or symbol explained at the top, not by color alone.
- Errors identified in text, adjacent to the field, specific about how to fix (3.3.1, 3.3.3), associated programmatically, plus a summary on submit with links to fields.
- Error prevention for legal, financial and data-changing submissions: review, confirm or reverse (3.3.4).
- Autocomplete attributes for personal data so browsers and assistive tech can fill them (1.3.5).
- Do not require re-entering information already provided in the same process (3.3.7).
- Authentication without cognitive tests (3.3.8): allow password managers and paste, offer alternatives to puzzles; CAPTCHAs need accessible alternatives.
- Group related controls (radio groups, address blocks) with a group label.

See `interaction-design` for validation timing and `ux-writing` for message wording.

### Images and alt text

Decide by the image's **purpose** in context (the W3C alt decision tree is a good reference):

| Image purpose | Alternative text |
|---|---|
| Informative (conveys content) | Concise description of the information it conveys in this context, not of every visual detail. |
| Functional (a linked image or image button) | The action or destination ("Search", "Home"), not the picture ("magnifying glass"). |
| Decorative (adds nothing) | Empty alt (`alt=""`) or the platform's decorative flag, so assistive tech skips it. |
| Complex (charts, diagrams, maps) | Short alt summarising the point, plus a longer description or data table nearby. |
| Image of text | The text itself (and avoid images of text). |
| Logo | The organisation name (and "home" if it links home). |

Guidance:

- Context matters: the same photo needs different alt text on a news article vs. a product page vs. a photographer's portfolio.
- Do not start with "Image of" — screen readers already announce it is an image.
- Keep it concise; put long descriptions in visible text that benefits everyone.
- Designers should supply alt text intent with images in specs; it is content, not an engineering afterthought.
- For user-generated images, provide a way for users to add alt text and prompt them to do so. Automatically generated descriptions can help but should be reviewable; they often miss the purpose.

### Audio, video and time-based media

| Media | Requirement (level) |
|---|---|
| Prerecorded video with audio | Captions (1.2.2, A); audio description or media alternative (1.2.3, A); audio description (1.2.5, AA) |
| Live video with audio | Captions (1.2.4, AA) |
| Prerecorded audio-only (podcasts) | Transcript (1.2.1, A) |
| Prerecorded video-only | Transcript or audio track describing it (1.2.1, A) |
| Sign language | 1.2.6 (AAA); important for some Deaf audiences |

Design practice:

- Captions are synchronised, accurate, include speaker identification and meaningful sounds; auto-generated captions need human correction.
- Plan audio description early: if key visual information is spoken in the narration ("as you can see on the chart, sales doubled"), less description is needed later.
- Media players need keyboard-operable, labelled controls, and captions toggles.
- No auto-playing audio for more than 3 seconds without a control to pause or adjust volume (1.4.2).
- Transcripts benefit everyone (search, skimming, translation).

### Motion and flashing

- Honour reduced-motion preferences; provide substitutes rather than removing feedback (see `motion-design`).
- Moving, blinking, auto-updating content over 5 seconds must be pausable (2.2.2).
- Nothing flashes more than three times per second (2.3.1); avoid large flashing areas and saturated red flashes entirely.
- Avoid parallax and scroll-hijacking for vestibular safety.

### Cognitive accessibility

Cognitive and learning disabilities, memory impairments, attention differences and mental-health conditions affect many users, and many WCAG criteria help only partially. W3C's *Making Content Usable for People with Cognitive and Learning Disabilities* (COGA) provides deeper guidance. Key practices:

- **Plain language:** short sentences, common words, active voice, one idea per sentence; explain jargon and abbreviations (see `ux-writing`).
- **Clear structure:** headings, short paragraphs, lists, consistent layout and navigation (3.2.3, 3.2.4), consistent location of help (3.2.6).
- **Predictability:** no unexpected changes of context on focus or input (3.2.1, 3.2.2); links and buttons do what their labels say.
- **Reduce memory load:** show information needed for the current step; do not require remembering codes across screens; support copy/paste.
- **Error tolerance:** forgiving inputs, clear recovery, undo (see `interaction-design`).
- **Time:** avoid time pressure; allow saving progress.
- **Minimise distraction:** limit simultaneous animation, pop-ups and competing calls to action.
- **Support multiple formats:** text plus icons, illustrations or video for complex instructions.
- **Avoid manipulative design** (dark patterns), which disproportionately harms users with cognitive disabilities.

### Inclusive language and representation

- Use language the community prefers; preferences differ (e.g. person-first "person with a disability" vs. identity-first "disabled person", "Deaf" vs. "deaf"); follow the audience or organisation's style guide, and ask when unsure.
- Avoid ableist idioms where alternatives are as clear ("sanity check", "blind spot", "crippled" in UI copy).
- Avoid assumptions in forms: gender options and pronouns, name formats (single names, long names, non-Latin characters), address formats, title requirements; ask only what is needed and explain why.
- Represent diversity in imagery and examples authentically (disability, age, ethnicity, body types, gender) without tokenism or inspiration framing.
- Do not use sensory-only instructions ("click the green button on the right") — 1.3.3 Sensory Characteristics.

## Platform-specific considerations

- **iOS / iPadOS:** support Dynamic Type (including the larger accessibility sizes, where layouts must reflow — e.g. horizontal rows become vertical), VoiceOver labels, traits and hints, Reduce Motion, Increase Contrast, Bold Text, Smart Invert, and Switch Control. Prefer system text styles so scaling works automatically.
- **Android:** support font scaling and display size changes, TalkBack content descriptions and roles, sufficient touch target sizes (Material's 48 dp), "Remove animations", and high-contrast text. Test with Switch Access and Voice Access.
- **Windows / desktop:** support high-contrast (forced colors) themes, Narrator and third-party screen readers (NVDA, JAWS), full keyboard operation including menus and shortcuts, and system scaling.
- **Web:** semantic HTML first, ARIA only to fill gaps, respect user stylesheets and browser zoom, and test across browser/screen-reader pairings commonly used by the audience.

## Documents, email and other outputs

Accessibility applies beyond app screens:

- **Documents and PDFs:** real headings, lists and table structures (not visual formatting only), document title and language set, alt text for images, logical reading order, tagged PDF output from the authoring tool, sufficient contrast. Avoid scanned images of text. Consider whether an HTML version would serve better (see `document-generation`).
- **Slides:** unique slide titles, reading order of objects, alt text, sufficient contrast and size for projection, captions for embedded video, and a shareable accessible version (see `presentations`).
- **Email:** semantic structure, live text rather than images of text, meaningful link text, sufficient contrast in both light and dark mail clients, and a plain-text alternative where possible.
- **Data visualisations:** text summaries of the key insight, accessible data tables, non-color encodings (see `data-visualization`).

## Worked example: annotating a sign-in screen

Illustrative annotations a designer would hand to engineering:

- **Page title:** "Sign in – [Product name]".
- **Landmarks:** header (logo, language switcher), main (sign-in form), footer (help, legal links).
- **Heading:** one level-1 heading "Sign in".
- **Focus order:** language switcher → email → password → show-password toggle → "Forgot password?" link → Sign in button → "Create account" link → footer links.
- **Fields:** visible labels "Email" and "Password"; `autocomplete` set to the email/username and current-password tokens; paste allowed; password manager friendly.
- **Show-password toggle:** a button with accessible name "Show password", state exposed as pressed/not pressed; the name stays stable while the state changes.
- **Errors:** on submit failure, an error summary at the top of the form receives focus and reads "There is a problem: Email or password is incorrect"; the fields remain filled (except password, by convention), and messages are associated with the relevant field.
- **Authentication alternatives:** no cognitive puzzle CAPTCHA; if bot protection is needed, use a non-interactive or accessible alternative (WCAG 3.3.8).
- **Targets:** all controls at least 44×44 px on touch layouts; the "Forgot password?" link is in its own line, not crowded against the button.
- **Contrast:** label, input text, borders, focus ring and link colors listed with measured ratios for light and dark themes.
- **Reduced motion:** the form's shake-on-error animation is replaced by no motion; the error text carries the meaning in both cases.

## Process

1. **Set the target** (standard and level) and identify obligations and audiences.
2. **Choose accessible foundations**: native controls, accessible design-system components, color roles with validated contrast in every theme, type scale with legible sizes, focus style, target sizes.
3. **Structure first**: headings, landmarks, reading order, focus order — in wireframes, before visual design.
4. **Design every interaction for keyboard, touch, pointer and assistive tech**, including dynamic changes and focus management.
5. **Write accessible content**: labels, instructions, error messages, alt text, captions and transcripts plans, plain language.
6. **Annotate designs** with semantics, names, order and announcements for handoff (see `design-to-code-handoff`).
7. **Check during design** (contrast, target sizes, zoom/reflow behaviour, color-blind simulation) and **during build** (automated tests plus manual keyboard and screen-reader passes).
8. **Test with disabled users** for key flows, and act on what you learn.
9. **Hand off to audit** when formal conformance evidence is needed (`accessibility-audit`).

## Decision guidance

| Question | Guidance |
|---|---|
| Native control or custom? | Native unless a documented need cannot be met; if custom, follow APG and test with real assistive tech. |
| Target AA or AAA? | AA is the usual requirement; adopt specific AAA criteria where cheap and valuable (7:1 body text for low-vision audiences, 44 px targets, no timing, reduced motion). Full AAA conformance is not recommended as a general policy by W3C because some content cannot meet it. |
| Hide content visually but keep for screen readers? | Use sparingly (extra context for icon buttons, table captions). If sighted users would also benefit, show it. |
| Overlay / widget products promising automatic compliance? | Treat with strong scepticism: they do not fix underlying issues and are widely criticised by disabled users and practitioners. Fix the product. |
| Separate "accessible version"? | Avoid; it lags and segregates. Make the main product accessible. |
| Disabled buttons? | Prefer enabled controls with explanatory errors; if disabled, explain why nearby. |

## Pitfalls

- **Accessibility deferred to "later"** or to an audit at the end.
- **Removing focus outlines** for aesthetics without a visible replacement.
- **Low-contrast grey text and placeholder-as-label** — common in generic, minimalist UI.
- **Color-only meaning** in status, charts, form errors and links.
- **Div/span "buttons"** without role, keyboard support and name.
- **ARIA misuse:** roles that contradict behaviour, `aria-label` hiding visible text, `aria-hidden` on focusable elements.
- **Heading levels chosen for size**, skipped or missing.
- **Icon-only controls** without accessible names or tooltips.
- **Alt text that describes pixels, not purpose**, or filenames as alt.
- **Modals without focus management**, toasts that are never announced.
- **Fixed-size text containers** that break at 200% or with text-spacing overrides.
- **Auto-playing media and carousels** without controls.
- **Time limits** without warning or extension.
- **Relying only on automated checkers:** they catch an estimated minority of issues (commonly cited as roughly 30–40%); keyboard, screen-reader and cognitive issues need humans.
- **Testing with one screen reader on one browser only** and assuming all work alike.

## Quality bar and verification

Before calling a design accessible-ready:

- [ ] Target standard and level stated; foundations (color roles, type, focus, targets) meet it in every theme and state.
- [ ] Every text/background and UI/adjacent color pair measured (4.5:1 / 3:1 / 3:1); nothing relies on color alone.
- [ ] Layout survives 200% text resize, 400% zoom reflow at 320 px, and text-spacing overrides.
- [ ] Structure annotated: page title, heading hierarchy, landmarks, reading and focus order, accessible names, live announcements.
- [ ] Every interaction is keyboard-operable with a visible, unobscured focus indicator and correct focus management.
- [ ] Targets meet 24×24 px minimum (2.5.8) and the chosen platform/AAA size for touch-primary actions; gestures and drags have alternatives.
- [ ] Forms have visible labels, upfront instructions, specific, associated error messages and allow autofill and paste.
- [ ] Every image has a purpose-based alternative or is marked decorative; complex images have long descriptions.
- [ ] Media has captions, transcripts and audio description plans as required; no auto-playing audio.
- [ ] Reduced-motion substitutes exist; no flashing above thresholds; moving content can be paused.
- [ ] Content uses plain language, consistent navigation and predictable behaviour; inclusive language and imagery reviewed.

**How to check**, depending on capability:

- **Automated:** run tools such as axe, Lighthouse, WAVE, Accessibility Insights, or platform accessibility scanners (Xcode Accessibility Inspector, Android Accessibility Scanner) on built UI. Design-tool plugins can check contrast and target sizes in mockups.
- **Manual keyboard pass:** unplug the mouse; complete every key task with Tab, Shift+Tab, Enter, Space, arrows and Escape; watch focus visibility and order.
- **Screen reader pass:** at least one desktop and one mobile screen reader on the target platforms; navigate by headings, landmarks and form controls; trigger dynamic updates.
- **Zoom and settings pass:** 200%/400% zoom, larger default font, text-spacing override, forced colors/high contrast, reduced motion, dark mode.
- **Color vision simulation** (browser devtools emulation or simulators).
- **User testing** with people with disabilities for critical flows.
- If you cannot run anything, provide the annotations, computed contrast table and the list of manual tests that must be performed, and say clearly that conformance is not verified. For formal conformance evaluation, hand over to `accessibility-audit`.
