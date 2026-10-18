---
name: accessibility-audit
description: >-
  Audit an existing website, web app, mobile app, or document (PDF, slides,
  office files) against the Web Content Accessibility Guidelines (WCAG) and
  produce a prioritized report of barriers with concrete fixes. Covers
  automated scanning versus manual testing, keyboard and focus, screen readers,
  color contrast, forms and errors, motion, zoom and reflow, cognitive load,
  severity rating, and retesting. Use when asked to "check accessibility",
  "run an a11y audit", "is this WCAG compliant", "test with a screen reader",
  prepare a conformance report or VPAT/ACR, or review a product before launch
  or procurement. For designing accessible interfaces from scratch, use
  accessible-design instead.
metadata:
  category: quality
  related: accessible-design, usability-evaluation, frontend-development, ux-writing, interaction-design, qa-test-planning, end-to-end-testing, document-generation
---

# Accessibility Audit

An accessibility audit answers one question: **can people with disabilities perceive, operate, understand, and rely on this product, and where they cannot, what exactly must change?** The output is not a score. It is a list of real barriers, each tied to a user impact, a standard, a location, and a fix a developer or author can act on.

## Scope and boundaries

This skill covers evaluating something that already exists (or exists as a build, prototype, or document). It covers:

- Web pages and web apps, including single-page apps and component libraries.
- Native mobile and desktop apps (the principles are the same; the tools differ).
- Documents: PDF, word-processor files, slide decks, spreadsheets, emails.
- Conformance reporting (e.g. a VPAT / Accessibility Conformance Report).

It does not cover:

- Designing accessible patterns from a blank page — see `accessible-design`.
- General usability studies — see `usability-evaluation` (although testing with disabled users is the strongest form of accessibility evaluation; see below).
- Legal advice. You can map findings to standards that laws reference (e.g. EN 301 549 in the EU, Section 508 in the US, the European Accessibility Act); you cannot certify legal compliance. Say so when asked.

## Check the current standard first

At the time of writing the current W3C recommendation is **WCAG 2.2** (published October 2023), with WCAG 3 in draft. Standards move. Before auditing:

- If you can browse, confirm the current WCAG version and whether the target regulation references an older one (many laws and contracts still cite WCAG 2.1 AA or even 2.0 AA). Audit against what the user is actually obliged to meet, and mention newer criteria as advisory.
- If you cannot browse, state the version you are auditing against and that the user should confirm it.
- Default target when nobody specifies: **WCAG 2.2 Level AA**, since that is what most policies require. Level AAA is rarely required in full; flag AAA items only when they are cheap or high-impact.

Notable 2.2 additions people miss because older checklists predate them: Focus Not Obscured (2.4.11, AA), Dragging Movements (2.5.7, AA), Target Size Minimum of 24 by 24 CSS pixels with spacing exceptions (2.5.8, AA), Consistent Help (3.2.6, A), Redundant Entry (3.3.7, A), and Accessible Authentication (3.3.8, AA — no cognitive function tests such as transcribing codes or solving puzzles without an alternative; allowing paste and password managers usually satisfies it). Criterion 4.1.1 Parsing was removed in 2.2.

## Core principles

**1. Automated tools find a minority of problems.** Rule engines (e.g. axe-core, WAVE, Lighthouse's accessibility audit, Pa11y, IBM Equal Access, Accessibility Insights) reliably detect machine-checkable failures: missing alt attributes, contrast of plain text on solid backgrounds, missing form labels, invalid ARIA, duplicate IDs. They cannot judge whether alt text is meaningful, whether focus order makes sense, whether an error message is understandable, or whether a custom widget works with a screen reader. Estimates of automated coverage vary by method, but expect that most WCAG success criteria need human judgment. A clean automated scan is the start of an audit, not the end. Never report "passes accessibility" on a scan alone.

**2. Test the experience, not the markup.** Correct-looking code can produce a broken experience (an ARIA role that announces "button" on something that does nothing on Enter), and unusual code can produce a fine one. Final judgments come from actually operating the thing with a keyboard, a screen reader, zoom, and so on.

**3. Impact over checklist.** Two failures of the same criterion can differ enormously. A missing alt on a decorative divider is trivial; a missing label on the "Pay now" button blocks the whole purchase. Severity follows what the barrier stops a person from doing.

**4. Sample deliberately.** You cannot test every page of a large site. Pick a representative sample that covers every template, every distinct component, and every critical user journey end to end (sign up, sign in, search, checkout, submit form, account settings, error and empty states). Journeys matter more than pages, because barriers often live in transitions: a modal that traps focus, a redirect that loses state, a timeout.

**5. Every finding needs a fix.** A report that says "fails 1.3.1" helps no one. Each finding should say who is affected, where, what happens, what should happen, and a concrete remediation (code-level for developers, content-level for authors).

**6. Respect the existing system.** Fixes should use the project's own component library, design tokens, and patterns. Recommend fixing the shared component once rather than patching fifty instances, and point out when a design-system component is the root cause.

## Process

### 1. Establish scope and target

Settle, asking the user if unclear:

- What is being audited: URLs, app build, environment (staging vs production), documents, logged-in areas (you may need test accounts — never ask for or enter the user's real credentials; ask them to provide test accounts or to sign in themselves).
- Target standard and level, and any regulation or contract driving it.
- Platforms: which browsers, which screen readers, desktop vs mobile, native apps.
- Deliverable: issue list for developers, executive summary, formal conformance report, or all three.
- Constraints: time budget, which journeys matter most to the business.

### 2. Build the sample

List templates and components, then the critical journeys. A typical sample for a medium web app is 10 to 25 screens plus 3 to 6 journeys. Include states that are easy to forget: validation errors, loading, empty results, expired session, modals and drawers, toasts, menus open, mobile breakpoint, dark mode if offered.

### 3. Run automated scans

Run a rule engine on every sampled screen and state (states matter: a scan of a closed modal tests nothing). Record results but treat them as leads:

- Deduplicate: one broken component appearing on 40 pages is one finding with 40 instances.
- Verify each reported issue manually before including it; rule engines produce false positives (e.g. contrast over gradients or images, text hidden intentionally) and "needs review" items that are not failures.
- Note what the scan cannot see: content in iframes, shadow DOM, canvas, closed states.

Without tool access, review the source or rendered HTML the user provides for the same machine-checkable patterns, and say clearly that runtime checks were not performed.

### 4. Manual testing passes

Do these in roughly this order; each catches a different class of barrier.

**Keyboard only (unplug the mouse mentally).**
- Every interactive element reachable with Tab / Shift+Tab, operable with Enter / Space / arrow keys as the pattern expects.
- Focus is always visible, with enough contrast against its surroundings, and not hidden behind sticky headers, cookie banners, or chat widgets (2.4.11).
- Focus order follows the visual and logical order. Positive `tabindex` values are a red flag.
- No keyboard traps (2.1.2). Modals trap focus intentionally *while open*, return focus to the trigger on close, and close with Escape.
- Skip link or landmarks let users bypass repeated navigation (2.4.1).
- Custom widgets (menus, tabs, comboboxes, sliders, date pickers, carousels) follow established keyboard conventions; the ARIA Authoring Practices Guide is a good reference, though it shows patterns, not requirements.
- Single-character shortcuts can be turned off or remapped (2.1.4).
- Anything requiring drag has a single-pointer alternative (2.5.7).

**Screen reader.**
- Use at least one desktop and, if mobile is in scope, one mobile screen reader. Common pairings: NVDA or JAWS with Chrome/Firefox/Edge on Windows, VoiceOver with Safari on macOS and iOS, TalkBack with Chrome on Android. Behavior differs between them; if you can only test one, say which.
- Navigate by headings, landmarks, links, and form controls, not only linearly; that is how experienced users move.
- Every control announces a name, role, and state (expanded, selected, checked, disabled) that matches what it does (4.1.2).
- The visible label text is contained in the accessible name (2.5.3), so voice-control users can say what they see.
- Dynamic changes are announced when they matter: form errors, cart updates, search results count, toasts (4.1.3 status messages). Overuse of live regions is also a failure in practice: constant chatter.
- Images: informative images have alt text that conveys their purpose in context; decorative ones are hidden (`alt=""`); complex images (charts, diagrams) have a text equivalent nearby.
- Reading order matches meaning, especially on layouts built with CSS grid or absolute positioning.

If you cannot run a screen reader, inspect the accessibility tree (browser devtools expose it) and say that results are inferred, not observed.

**Visual: contrast, color, zoom, reflow, spacing.**
- Text contrast at least 4.5:1, or 3:1 for large text (roughly 24 CSS px regular or 18.66 px bold) (1.4.3). Measure actual rendered colors, including over images, gradients, and in hover/focus/disabled states. Disabled controls are exempt, but question whether anything important is shown only in disabled styling.
- Non-text contrast at least 3:1 for UI component boundaries, focus indicators, and meaningful graphics such as chart lines and icons (1.4.11).
- Color is never the only way to convey meaning: required fields, errors, link vs text, chart series, status badges (1.4.1).
- Zoom to 200% (1.4.4) and reflow at 320 CSS px width (equivalent to 400% zoom on a 1280 px window) without loss of content or two-dimensional scrolling, except for content that genuinely needs it like maps or data tables (1.4.10).
- Text spacing override (line height 1.5, paragraph spacing 2x, letter 0.12em, word 0.16em) does not clip or overlap text (1.4.12). A bookmarklet or user stylesheet makes this quick.
- Content that appears on hover or focus (tooltips, menus) is dismissible, hoverable, and persistent (1.4.13).
- Orientation is not locked unless essential (1.3.4).

**Forms and errors.**
- Every input has a programmatic label; placeholders are not labels (they vanish, and often fail contrast).
- Instructions and format requirements are given before the input, not only after an error.
- Errors identify the field, describe the problem in text, and suggest a fix (3.3.1, 3.3.3); focus moves to or announces the error summary on submit.
- Input purpose is exposed with `autocomplete` for personal data fields (1.3.5).
- Users are not asked again for information they already provided in the same process (3.3.7).
- Authentication does not require memorizing, transcribing, or puzzle-solving without an alternative; paste works in password and code fields (3.3.8).
- Legal, financial, or data-changing submissions are reversible, checked, or confirmed (3.3.4).
- Time limits can be extended or turned off (2.2.1); warn before session timeout.

**Motion, media, and timing.**
- Nothing flashes more than three times per second (2.3.1). This is a safety issue (seizures), not a preference; treat any failure as critical.
- Auto-playing, moving, or auto-updating content lasting more than five seconds can be paused, stopped, or hidden (2.2.2). Carousels and background videos are common offenders.
- Respect reduced-motion preferences for non-essential animation, especially parallax, zoom, and large movement (2.3.3 is AAA but vestibular harm is real; recommend it).
- Audio playing automatically for more than three seconds can be stopped (1.4.2).
- Prerecorded video has accurate captions (not just auto-generated, unchecked captions) and audio description or a transcript where visual information is not conveyed by audio (1.2.x). Live video needs live captions at AA.

**Structure and semantics.**
- One clear page title per page that describes it (2.4.2); in single-page apps the title updates on route change and focus moves sensibly.
- Headings form a meaningful outline; no skipping just for styling, no visually-styled "headings" that are plain text.
- Landmarks (header, nav, main, footer) exist and are not duplicated without labels.
- Lists, tables, and their headers are marked up as such; layout tables are not data tables.
- Language of page (and of passages in other languages) is set (3.1.1, 3.1.2).
- Link text makes sense in context; "click here" and repeated "read more" links are a usability problem and often a 2.4.4 failure.

**Cognitive and understanding.** Many cognitive needs sit in AAA or outside WCAG entirely, but they are often where real users fail. Note, at least as advisory:
- Plain language and short sentences for critical instructions.
- Consistent navigation and naming across pages (3.2.3, 3.2.4); help mechanisms in a consistent location (3.2.6).
- No unexpected context changes when focusing or entering data (3.2.1, 3.2.2): a select that navigates on change is the classic.
- Predictable, forgiving flows: progress indicators, saved progress, undo.
- Distraction: auto-playing content, pop-ups interrupting tasks.

**Pointer and touch (mobile and touchscreens).**
- Targets at least 24 by 24 CSS px or adequately spaced (2.5.8); 44 by 44 is a better practical aim for primary controls.
- Gestures with multiple fingers or paths have simple alternatives (2.5.1).
- Actions trigger on up-event, so users can slide off to cancel (2.5.2).
- Motion actuation (shake to undo) has a UI alternative and can be disabled (2.5.4).

**Single-page apps and dynamic content.** Client-rendered apps break assumptions screen readers rely on. Check specifically:
- On route change, focus moves somewhere sensible (the new page's main heading or main region) and the page title updates. Otherwise screen reader users do not know anything happened.
- Content injected after load (infinite scroll, lazy panels, chat messages) appears in a sensible place in the reading order, and "load more" is reachable without tabbing past everything already loaded.
- Loading indicators are announced (a polite status message) and do not steal focus.
- Client-side validation and server-side validation produce the same accessible error experience.
- Components rendered into portals (modals, popovers, toasts) are placed in the accessibility tree where users can find them, and the background is made inert while a modal is open.

### Worked reasoning: alt text and names

Judging text alternatives is where automated tools are weakest and auditors disagree most. Ask three questions in order:

1. **Does this image or control convey information or function?** If it is purely decorative (a flourish, a background texture, an icon next to text that already says the same thing), it should be hidden from assistive technology. Announcing it is noise.
2. **What would a sighted user take from it in this context?** A photo of a red shoe on a product page needs color, style, and distinguishing detail; the same photo as a thumbnail link in a list needs only the product name, because the link's purpose is navigation. A chart needs its key finding in text ("Sales doubled between Q1 and Q3"), plus access to the data for anyone who wants it.
3. **Does the name match what is visible?** An icon button labelled visually as "Save" must have an accessible name that includes "Save", not "Submit form data". Voice-control users say what they see.

Common failures: alt text that repeats adjacent caption text (users hear it twice); "image of" prefixes (screen readers already announce "image"); file names; alt text on a linked image describing the picture rather than the link destination; icon-only buttons with no name at all.

### 5. Native apps

The same principles apply through WCAG-to-native mappings (e.g. W3C's guidance on applying WCAG to non-web technology). Use platform tools: Accessibility Inspector and VoiceOver on Apple platforms, Accessibility Scanner and TalkBack on Android. Check: content descriptions / accessibility labels, traits/roles, Dynamic Type or font scaling up to the largest sizes, focus order with external keyboard and switch control, sufficient touch target sizes, and that custom views expose themselves to the accessibility API at all.

### 6. Documents and PDFs

Documents fail in ways web pages do not. For each document:

- **Tagged structure.** PDFs must be tagged; untagged PDFs read as an undifferentiated stream or not at all. Check the tag tree, not just the visual appearance. Scanned PDFs without OCR are images of text and fully inaccessible.
- **Reading order.** Multi-column layouts, sidebars, and footnotes often read in the wrong order. Check the tag order or the reading-order view.
- **Headings, lists, and tables** use real structure (styles in word processors, tags in PDF), with table header cells identified.
- **Alternative text** for meaningful images; artifacts for decorative ones.
- **Document title and language** set in properties.
- **Links** with meaningful text; **bookmarks** for long documents.
- **Forms** in PDFs have labelled fields and logical tab order.
- **Contrast and color-only meaning** apply exactly as on the web.
- **Slides:** every slide has a unique title; reading order of objects is set; embedded video has captions.
- **Spreadsheets:** named sheets, header rows defined, no meaning encoded only in cell color, no merged cells breaking navigation.

Tools that help: built-in accessibility checkers in office suites, PDF accessibility checkers (e.g. PAC for PDF/UA, the checker in Acrobat), and actually reading the document with a screen reader. Built-in checkers miss reading order and alt-text quality, just as web scanners do. Often the best recommendation is to fix the source document and re-export, rather than remediating the PDF by hand, and to publish an accessible HTML version alongside.

### 7. Include disabled users when possible

Expert auditing finds conformance failures; people who use assistive technology daily find the barriers experts rationalize away. If budget allows, recommend sessions with users of screen readers, magnification, voice control, switch access, and people with cognitive disabilities. Pay them. If you are an AI working alone, say plainly that your findings are expert review, not user testing.

### 8. Rate severity

Use a scale the team understands; if they have none, a four-level impact scale works:

| Severity | Meaning | Examples |
|---|---|---|
| Critical | Blocks a core task for a group of users with no workaround, or creates a safety risk | Checkout button not keyboard operable; CAPTCHA with no alternative; flashing content; modal traps focus with no exit |
| Serious | Task possible only with significant difficulty or a workaround most users will not find | Form errors not announced; focus invisible on main nav; contrast 2.5:1 on body text |
| Moderate | Causes friction or confusion but the task is completable | Heading levels skip; redundant link text; tooltip not dismissible |
| Minor | Low impact, cosmetic, or best practice | Decorative image announced with a filename; slightly undersized secondary targets |

Severity considers: how critical the affected task is, how many users and which disabilities are affected, whether a workaround exists, and how often the component appears. Report WCAG level separately from severity; a Level A failure can be minor in context, and an advisory (non-WCAG) issue can be serious.

### 9. Write the report

What a useful report contains (adapt the shape to the audience; this is not a template):

- **Summary for decision makers:** overall state in plain language, the handful of blockers, which journeys are affected, and the recommended order of work. No WCAG jargon in the first paragraph.
- **Scope and method:** what was tested, standard and level, sample, tools and assistive technology with versions, browsers, dates, and what was out of scope. This lets someone reproduce or extend the audit, and protects against overclaiming.
- **Findings,** each with: title stating the barrier; location(s) and steps to reproduce; who is affected and how; the WCAG criterion and level (or "advisory"); severity; expected behavior; recommended fix with a code or content example where helpful; and a note when the root cause is a shared component.
- **Positive findings:** what works well, so it is not broken by future changes.
- **Retest plan:** how fixes will be verified.

Group findings by component or journey for developers, by criterion for a conformance report. Keep raw scanner output in an appendix, never as the main body.

**Example finding (illustrative only):**

> **Search filters cannot be operated by keyboard.** On the Results page, the "Price" and "Brand" filter chips respond only to mouse clicks. They are `div` elements with click handlers, no `tabindex`, and no role. Keyboard and switch users cannot narrow results, and screen reader users hear them as plain text. WCAG 2.1.1 Keyboard (A), 4.1.2 Name, Role, Value (A). Severity: Serious (search still works without filters). Fix: render chips as `button` elements with `aria-pressed` reflecting the selected state; the design system's `ToggleButton` already does this. Affects every listing page (one shared component).

### Conformance reports (VPAT / ACR)

When the deliverable is a formal Accessibility Conformance Report, typically built on the VPAT format (check for the current edition, which exists in WCAG, Section 508, EN 301 549, and international variants):

- Use the edition that matches the buyer's requirement; procurement teams usually specify it.
- For each criterion, choose the conformance term honestly: "Supports", "Partially Supports", "Does Not Support", "Not Applicable". "Partially Supports" with a precise remark ("Form errors on the Payment step are not announced; all other forms support") is far more credible than a wall of "Supports".
- Remarks should describe the user-facing exception, not the code.
- State the product version, date, and evaluation methods. A report is a snapshot; it goes stale with every release.
- Never write an ACR claiming support for criteria that were not tested. Reviewers who check one claim and find it false stop trusting the whole document.

### Measuring without full tooling

If you cannot run a browser, assistive technology, or scanner (for example, you only have source files or screenshots):

- Compute contrast from the hex values in stylesheets or design tokens using the WCAG relative-luminance formula; note that rendered colors may differ (opacity, overlays, images).
- Read the markup for semantics: native elements, labels, heading outline, landmarks, `alt`, ARIA validity, `tabindex` values, `lang`.
- Read event handlers to infer keyboard support (click handlers on non-focusable elements with no key handling are a strong signal).
- From screenshots, you can judge visual contrast roughly, color-only meaning, target sizes, visible focus (if captured), and text clarity — not semantics.
- Label every such finding as "from code review" or "from visual inspection" and list the runtime checks still needed.

### 10. Retest and regression-proof

After fixes, retest each finding with the same method that found it. Recommend preventive measures: automated accessibility rules in component tests and CI (see `end-to-end-testing`), linting for JSX/templates, accessibility acceptance criteria in tickets, and a short manual keyboard-and-screen-reader check in the definition of done for UI changes.

## Decision guidance

**Native element vs ARIA fix.** Prefer native HTML (`button`, `a href`, `label`, `select`, `details`) over ARIA on generic elements. Native elements bring keyboard handling, focus, and semantics for free; ARIA only changes what is announced and adds a duty to implement behavior yourself. Recommend ARIA when a native element cannot express the pattern (tabs, comboboxes, tree views) or when restructuring is not feasible.

**Fix the component vs fix the instance.** If the same failure appears on many pages, find the shared source (component, template, CMS field, design token) and fix there. Instance fixes are for content (alt text, link text, heading text) authored per page.

**Remediate the PDF vs replace it.** Remediate when the document is final, legally required in PDF, and few in number. Fix the source and re-export when the document will be revised. Replace with HTML when content is meant to be read on screen and updated.

**Conformance claim vs progress report.** A formal claim ("conforms to WCAG 2.2 AA") requires that every page in scope meets every criterion; one failure breaks it. Most real products do not conform, and that is normal. Offer an honest picture ("partially supports" in ACR terms) with a roadmap rather than a claim that will not survive scrutiny.

**Overlays.** Third-party "accessibility overlay" widgets that promise automatic compliance do not fix underlying code barriers, can interfere with users' own assistive technology, and are widely criticised by disabled users and practitioners. If the product uses one, test with it both on and off, and recommend fixing the source rather than relying on it.

## Discovering context

Before auditing, look for:

- An existing accessibility statement, previous audits, a known-issues list, or an ACR. Retesting previous findings is often the most valuable first step.
- The design system and its documented accessibility behavior; check whether components meet their own documentation.
- The team's issue tracker conventions, severity labels, and definition of done, so findings land in a form they will use.
- Which assistive technologies the actual users rely on, if analytics or support tickets reveal it (be careful: analytics rarely detect assistive technology, and absence of data is not absence of users).
- Brand colors and tokens: suggest compliant alternatives within the palette rather than arbitrary new colors.

## Pitfalls

- **Reporting the scanner output as the audit.** Hundreds of duplicated lines, false positives, and none of the real blockers. Deduplicate, verify, and do the manual passes.
- **"Fixing" by adding ARIA everywhere.** Redundant roles (`role="button"` on `button`), `aria-label` that overrides useful visible text, `aria-hidden` on focusable elements. Bad ARIA is worse than none.
- **Testing only the happy path.** Errors, timeouts, and empty states are where barriers cluster.
- **Ignoring states.** Contrast in hover, focus, disabled, selected, and dark mode; menus open; content behind modals.
- **Alt text judgments without context.** The same image needs different alt text on a product page and a news article. Ask what the image is for.
- **Screen reader tested only by a sighted tester reading the visual screen.** Turn off or ignore the screen; navigate by the announcement alone.
- **Equating mobile responsive with accessible.** Reflow is one criterion of many.
- **Hiding content "for screen readers only" that should be visible to everyone** (e.g. instructions), or hiding visible content from assistive technology.
- **Overstating certainty.** If a check was inferred from code rather than observed with assistive technology, say so.
- **Severity inflation.** Calling everything critical makes the report unusable. Reserve critical for blocked tasks and safety.
- **Legal conclusions.** Report against standards; leave legal determinations to counsel.

## Quality bar and verification

Before delivering, check:

- [ ] Standard and version are stated and match what the user must meet.
- [ ] Every critical journey was walked end to end with keyboard and at least one screen reader (or the limitation is stated).
- [ ] Automated results were deduplicated and manually verified; scanner false positives removed.
- [ ] Each finding has location, reproduction, user impact, criterion (or "advisory"), severity, and a concrete fix.
- [ ] Shared-component root causes are identified rather than listed per page.
- [ ] Contrast values are measured, not eyeballed, and include interactive states.
- [ ] Documents were checked for tags, reading order, and alt text, not only visual appearance.
- [ ] Positive findings and out-of-scope areas are stated.
- [ ] Nothing in the report claims full conformance or legal compliance that the evidence does not support.
- [ ] A developer reading any single finding could start fixing it without asking you a question.
