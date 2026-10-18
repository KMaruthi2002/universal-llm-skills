---
name: interaction-design
description: >-
  Design how an interface behaves over time: task flows, feedback and system
  status, state transitions, forms and validation, navigation and wayfinding,
  progressive disclosure, error prevention and recovery, confirmation vs.
  undo, optimistic UI and latency perception, keyboard and gesture input,
  notifications and microinteractions. Use when designing or fixing a flow
  (sign-up, checkout, onboarding, settings, multi-step wizard), deciding how a
  form validates, what happens when an action is slow or fails, whether to
  confirm or offer undo, how users move between screens, or when a UI "feels
  clunky", "confusing" or "unresponsive". For static layout and component
  choice use ui-design-fundamentals; for animation craft use motion-design.
metadata:
  category: design
  related: ui-design-fundamentals, motion-design, ux-writing, information-architecture, wireframing-and-prototyping, usability-evaluation, accessible-design, error-handling, frontend-development
---

# Interaction Design

Interaction design shapes the conversation between a person and a system: what the person can do, how the system responds, how both sides know where they stand, and what happens when things go wrong. A screen can look right and still fail if it does not respond, explain, forgive and guide.

This skill covers behaviour over time. Static composition is `ui-design-fundamentals`; how transitions move is `motion-design`; the words are `ux-writing`; the overall structure of destinations is `information-architecture`.

## Core principles

Most of these trace to well-established usability heuristics (Nielsen's ten heuristics, Norman's design principles, Shneiderman's golden rules). They are stated here with reasons so they can be applied to new cases.

1. **Make system status visible.** People need to know what is happening: is it working, did it save, what changed, where am I? Uncertainty causes repeated clicks, abandonment and distrust. Every action deserves feedback proportionate to its importance and duration.
2. **Match the user's mental model.** Use the user's concepts, words and sequence, not the database's. A flow that mirrors the backend ("create account entity, then profile entity, then payment method entity") is not a flow users understand.
3. **Prevent errors before handling them.** Constrain inputs, provide good defaults, make destructive actions harder to hit, show consequences before commitment. Prevented errors cost nothing; recovered errors cost time and trust.
4. **Make recovery easy.** When errors happen (they will), explain in plain language what happened and how to fix it, preserve the user's work, and offer the fix directly. Reversible actions (undo) make people confident enough to act.
5. **Recognition over recall.** Show options, recent items and examples rather than requiring users to remember them. Memory is the scarcest resource in an interface.
6. **User control and freedom.** Clear exits (cancel, back, close), the ability to pause and return, no traps. Respect the platform's back behaviour.
7. **Reduce effort where it repeats.** Shortcuts, defaults, bulk actions and remembered preferences for frequent users; guidance for new users. Design both paths (see density in `ui-design-fundamentals`).
8. **Responsiveness is a feature.** Perceived speed shapes satisfaction more than measured speed; design for how waiting feels.

## Discovering context

- **Existing flows and patterns** in the product: how do other forms validate, how are deletions handled, what feedback components exist (toasts, banners, inline messages)? Follow them for consistency.
- **Platform conventions**: back navigation, swipe gestures, pull-to-refresh, keyboard shortcuts, system dialogs and share sheets differ across iOS, Android, desktop OSes and the web.
- **Backend realities**: latency, failure modes, idempotency, offline support, rate limits, what can be undone server-side. Interaction design that ignores these promises behaviours engineering cannot deliver. Talk to engineers early (see `error-handling`, `api-design`).
- **User research and analytics**: where do users drop off, what errors are common, what support tickets say (see `ux-research`).
- **Regulatory constraints**: consent, cancellation, data deletion, financial confirmations may have legal requirements.

## Flows

### Mapping a flow

1. **Name the goal** in the user's terms ("send money to a friend"), and the entry points (where users start from).
2. **List the steps** in the user's order, including decisions and the information needed at each.
3. **Map branches**: errors, edge cases, alternative paths, abandonment and return, first-time vs. returning users, permissions.
4. **Find what can be removed, deferred or defaulted.** Every step and every field is friction; challenge each one ("what happens if we don't ask this now?").
5. **Mark the moments of commitment** (pay, publish, delete, send) — these need the most clarity and protection.
6. **Prototype and test** (see `wireframing-and-prototyping`, `usability-evaluation`).

A flow diagram, user journey or state diagram is useful here — describe what it must show (steps, decisions, system responses, error branches), not a fixed notation.

### Structuring multi-step tasks

| Approach | Use when |
|---|---|
| Single page form | Few fields, users benefit from seeing everything, editing is common. |
| Multi-step wizard | Many fields that group naturally, later steps depend on earlier answers, novice users. Show progress, allow back without data loss, save progress for long flows. |
| Progressive / conditional form | Most users need a few fields; some need more based on answers. Reveal fields as they become relevant. |
| Hub and spoke (checklist / task list) | Many independent sections completed in any order over time (applications, onboarding setup, account configuration). |
| Conversational (one question at a time) | Very simple data, mobile, low-literacy or anxious users; can be slow for experts. |

Put the commitment step last with a review summary when stakes are high (purchases, applications, legal declarations).

### Onboarding

- Prefer **learning by doing** with good empty states and contextual hints over front-loaded tours, which most users skip and few remember.
- Ask only what is needed to deliver first value; defer profile completion.
- Let users skip and return.

## Feedback and system status

### Proportionate feedback

| Action | Appropriate feedback |
|---|---|
| Hover / focus / press | Immediate visual state change on the control (well under 100 ms). |
| Toggle, select, small edit | Immediate state change in place; save indicator if persisted. |
| Background action (archive, move, send) | Inline change plus a brief, dismissible confirmation, ideally with Undo. |
| Long-running work | Progress indicator, then completion notification; allow leaving and returning. |
| High-stakes completion (payment, submission) | Dedicated confirmation with reference details and next steps, also sent by another channel if appropriate. |
| Failure | Clear message at the point of failure, preserved input, a way forward. |

Status changes must be perceivable by assistive technology too: use live regions or platform equivalents for messages that appear without focus moving (WCAG 4.1.3 Status Messages).

### Latency perception

Long-standing response-time limits (Miller 1968; Card, Robertson & Mackinlay 1991; popularised by Nielsen):

| Duration | Perception | Design response |
|---|---|---|
| ≤ ~0.1 s | Instantaneous | Direct manipulation feels connected; no indicator needed. |
| ~0.1–1 s | Noticeable but flow preserved | Usually no spinner; a subtle indicator can help after ~300–500 ms. Avoid flashing indicators for very short waits (delay showing them). |
| ~1–10 s | Attention starts to wander | Show a loading indicator; skeleton screens for content; keep layout stable. |
| > ~10 s | Users switch tasks | Determinate progress, estimated time, ability to continue elsewhere, notification on completion. |

Techniques:

- **Optimistic UI:** show the expected result immediately and reconcile when the server responds. Use when success is highly likely and failure is recoverable (likes, reorder, rename, send message). On failure, revert visibly and explain. Avoid for payments, irreversible actions, or anything with significant failure rates.
- **Skeletons** for content with predictable shape; spinners for indeterminate short actions; progress bars for measurable work.
- **Prefetch and preload** likely next steps.
- **Do the work in the background** and let users continue.
- **Delay indicators** briefly (e.g. a few hundred ms) so fast responses do not flash, and once shown, keep them long enough to be read to avoid flicker.
- **Disable double submission** while preserving feedback (show progress on the button rather than silently disabling it).

## Forms and validation

Forms are where most interaction design goes wrong and where small changes produce measurable conversion gains.

### Structure

- Ask only what is necessary; mark optional fields (or required ones — be consistent; marking whichever is the minority reduces noise).
- One column usually completes faster than multi-column layouts for sequential input; short related fields (city/postcode, expiry month/year) may share a row.
- Labels visible above or beside fields, never placeholder-only (placeholders vanish, have low contrast, and are unreliable accessible names).
- Group related fields with headings or fieldsets.
- Match field size to expected input length; it signals what is expected.
- Use the right input types and attributes (on the web: `type`, `inputmode`, `autocomplete`) so mobile keyboards and autofill help. Support autofill and password managers; never block paste (WCAG 3.3.8 Accessible Authentication discourages cognitive-test login steps and blocking paste into password fields).
- Do not ask for the same information twice in a process (WCAG 3.3.7 Redundant Entry).
- Be liberal in accepted formats (spaces in phone numbers and card numbers, different date formats) and normalise them yourself.

### Validation timing

| Timing | Use for | Caution |
|---|---|---|
| On submit | Always, as a backstop. Summarise errors at the top with links to fields, and move focus to the summary or first error. | Alone, it delays feedback for long forms. |
| On blur (leaving the field) | Format and completeness errors. | Do not show errors on fields the user has not interacted with yet. |
| While typing (live) | Constraints that help as you type (password requirements checklist, character count, username availability). Clear an existing error as soon as it is fixed. | Do not show "invalid" while the user is still typing a valid value (e.g. an incomplete email). |
| Server-side | Anything that needs data (uniqueness, eligibility, fraud). | Show results in the same inline style; preserve input. |

Error messages: say what is wrong and how to fix it, in plain language, next to the field, and associated programmatically with it. Do not rely on color alone; include an icon or text (WCAG 1.4.1, 3.3.1, 3.3.3). See `ux-writing`.

Never clear the user's input on error. Never reset a whole form because one field failed.

## Navigation and wayfinding

Users must always be able to answer: Where am I? Where can I go? How do I get back? What will happen if I click this?

- Indicate the current location (selected nav state, page title, breadcrumbs for deep hierarchies).
- Keep navigation consistent across pages (WCAG 3.2.3 Consistent Navigation, 3.2.6 Consistent Help).
- Respect back: the browser or OS back action should do what users expect (return to the previous view, close a sheet, step back in a wizard) without losing data. Use URLs for states users would want to share, bookmark or return to (filters, tabs, search results, selected item).
- Make links and buttons predictable: links navigate, buttons act. Say where a link goes or what a button does.
- Search for large content sets; filters and sorting for collections; recent items for repeat access.
- Structure itself (what destinations exist, how they are grouped and named) is `information-architecture`.

## Progressive disclosure

Show what most users need now; make the rest available on demand.

- **Good candidates to defer:** advanced settings, rarely used options, detailed explanations, secondary metadata.
- **Do not hide:** information needed to make the current decision, prices and fees, required steps, consequences of actions.
- **Signal that more exists** (a clear "Advanced options" control, a "Show details" link) and make the disclosure reversible.
- Limit to one or two levels; nested disclosures lose users.
- Staged disclosure (wizards) and contextual disclosure (reveal on relevant input) are both forms of this.

## Error prevention and recovery

### Prevention techniques

- **Constraints:** pickers instead of free text where values are fixed; disable impossible dates; limit input length with visible counters.
- **Good defaults:** pre-select the most common safe option.
- **Forcing functions for irreversible actions:** type-to-confirm (repository names, account deletion), a review step, or a delay window.
- **Separation:** keep destructive actions away from frequent ones; different visual treatment.
- **Previews:** show consequences before commitment ("This will email 2,341 people").
- **Inline guidance:** formats, examples and constraints shown before the user errs.

### Confirm vs. undo

| Situation | Prefer |
|---|---|
| Action is reversible and frequent (archive, delete to trash, move, mark as read) | **Undo** (immediate action + brief undo option). Confirmation dialogs for frequent actions become habitual clicks that protect no one. |
| Action is irreversible but the system can delay it (send email, bulk delete) | **Delayed commit with undo window**, then perform. |
| Action is irreversible, rare and high-impact (delete account, transfer funds, publish to many) | **Confirmation** that names the specific consequence and uses a specific action label ("Delete project 'Atlas'"), possibly with type-to-confirm. |
| Action is legally binding | Explicit review and confirmation; keep records. |

Undo needs backend support (soft delete, delayed jobs, versioning). Raise this early. Multi-level undo/redo is expected in editors and creative tools; provide history where users make many changes.

### Error messages (system level)

A good error message tells the user: what happened (in their terms), whether their data is safe, what they can do now (retry, edit, contact support with a reference code), and does not blame them. Logs and stack traces belong in logs, not on screen (see `error-handling`).

## Input modalities

- **Keyboard:** every interactive element reachable and operable by keyboard (WCAG 2.1.1), logical focus order (2.4.3), visible focus (2.4.7), no keyboard traps (2.1.2). Expert tools benefit from shortcuts; make them discoverable (tooltips, a shortcut sheet) and avoid single-character shortcuts that conflict with assistive tech unless they can be turned off or remapped (2.1.4).
- **Pointer:** large enough targets (see `layout-and-responsive-design`), actions on up-event so users can cancel by sliding away (2.5.2), no hover-only functions.
- **Touch gestures:** gestures are invisible; provide visible alternatives for every gesture-only action (2.5.1, and 2.5.7 for dragging). Respect platform gestures (edge swipes for back).
- **Voice and assistive tech:** visible labels should match accessible names so voice users can say what they see (2.5.3 Label in Name).
- **Drag and drop:** show drag affordance, valid drop targets, insertion position, and provide a non-drag alternative (move menu, keyboard reorder).

## Microinteractions

A microinteraction is a single contained moment: a toggle, a like, a pull-to-refresh, a password strength meter. Dan Saffer's model is useful: **trigger** (what starts it), **rules** (what happens), **feedback** (how the user perceives it), **loops and modes** (what happens over time and repeated use).

Design each with: a clear trigger, immediate feedback, state that persists correctly, and graceful behaviour on failure. Motion detail belongs to `motion-design`; delight should never cost speed or clarity.

## Notifications and interruptions

- Interrupt only when the user would want to be interrupted: time-sensitive, personally relevant, actionable.
- Let users control channels and frequency; default conservatively.
- Group and summarise rather than notifying for every event.
- In-app notifications should link to the relevant context and be markable as read.
- Avoid manipulative patterns (fake urgency, guilt-tripping copy, hard-to-find unsubscribe). See dark patterns in `ui-design-fundamentals`.

## State modelling

For anything non-trivial, enumerate states and transitions explicitly — a state table or diagram — before designing screens. For example, a file upload: idle → selecting → validating → uploading (progress) → processing → done | failed (retryable) | rejected (not retryable) | cancelled. For each state: what the user sees, what they can do, what transitions are possible, and what happens on refresh, navigation away, or network loss. This surfaces missing designs and aligns with how engineers implement it (state machines, reducers). It also feeds `motion-design` (transitions) and `qa-test-planning` (test cases).

## Saving and editing models

How changes are committed is a fundamental interaction decision; mixing models within one surface confuses users.

| Model | Use when | Design needs |
|---|---|---|
| **Auto-save** | Documents, notes, preferences where every change is safe and reversible. | Visible save status ("Saving…", "Saved", "Offline — will sync"), version history or undo, conflict handling. |
| **Immediate apply** (toggles, inline edits) | Independent settings with low risk. | Instant feedback; errors revert the control with a message. |
| **Explicit save / submit** | Changes that are interdependent, consequential or need validation together (profile with payment, permissions, publishing). | Clear dirty state, a warning on leaving with unsaved changes, Save and Cancel/Discard actions. |
| **Draft and publish** | Content that others will see. | Distinguish draft from live, preview, scheduled publishing, revert. |

Within one settings page, do not combine switches that apply immediately with fields that need a Save button unless the regions are clearly separated.

## Search and filtering

- Put search where users expect it and make the field large enough for typical queries.
- Offer suggestions and recent searches; tolerate typos, plurals and synonyms where the backend allows.
- Show the query and active filters on the results page, with result count and an easy way to clear each filter.
- Decide **instant vs. applied filters**: instant updates suit fast backends and small result sets; an "Apply" step suits slow queries and mobile filter sheets (avoid re-rendering behind a sheet with every tap). Announce result count changes to assistive tech.
- Preserve search and filter state in the URL and on back navigation.
- Design the zero-results state with ways forward (see `ui-design-fundamentals`).

## Collaboration and conflicts

When several people (or devices) can edit the same thing:

- Show presence (who else is here) and, for real-time editing, others' cursors or selections.
- Decide conflict strategy with engineering: last-write-wins (simple, can lose work), locking (safe, blocks others), merge or real-time collaborative editing (best experience, most complex).
- Never discard a user's changes silently; if a conflict occurs, show both versions or preserve theirs as a draft.
- For stale data (another user changed a record you are viewing), notify and offer refresh rather than overwriting.

## Worked reasoning: redesigning a "delete" interaction

Illustrative example of applying the principles.

> Current behaviour: in a file manager, selecting files and pressing Delete opens a dialog "Are you sure? OK / Cancel". Analytics show the dialog is confirmed over 99% of the time within a second, and support still receives "I deleted the wrong folder" tickets weekly.
>
> Reasoning: the confirmation has become a reflex, so it protects no one (confirmations for frequent actions train automatic clicking). The real need is recoverability.
>
> Redesign:
> 1. Delete moves items to a trash state immediately (backend: soft delete with a retention period — confirmed feasible with engineering).
> 2. Inline feedback: items animate out of the list (see `motion-design`), and a toast says "3 files moved to Trash" with **Undo**; the toast is announced to screen readers and persists long enough to act (and is not the only path — Trash is reachable from navigation).
> 3. Permanent deletion ("Empty Trash", or deleting from Trash) keeps a specific confirmation naming the count and stating it cannot be undone.
> 4. Bulk deletion above a threshold (e.g. an entire shared folder) shows a preview of consequences ("This folder is shared with 12 people").
> 5. Keyboard: Delete key works, Ctrl/Cmd+Z undoes, focus moves to the next item after deletion.
>
> Verification: test with users deleting and recovering files; monitor undo usage and support tickets after release.

## Process

1. Define the goal, users, entry points and success measures.
2. Discover existing patterns, platform conventions and backend constraints.
3. Map the flow and states, including error and edge branches.
4. Remove, defer and default wherever possible.
5. Decide feedback, validation, confirmation/undo, and latency strategies per step.
6. Prototype at the lowest fidelity that tests the behaviour (paper or clickable for flow; coded for latency, validation and gestures).
7. Test with users on realistic tasks; observe hesitation, errors and recovery (see `usability-evaluation`).
8. Specify behaviour for handoff: states, transitions, timings, validation rules, error messages, keyboard behaviour (see `design-to-code-handoff`).

## Pitfalls

- **Happy-path flows** with no error, empty, slow or offline branches.
- **Silent actions:** clicking does nothing visible; users click again and create duplicates.
- **Spinners everywhere**, including for operations that take 100 ms, causing flicker.
- **Validating too early** ("invalid email" after one keystroke) or only on submit for long forms.
- **Clearing forms on error.**
- **Confirmation dialogs for everything**, training users to click "OK" without reading.
- **Undo promised without backend support.**
- **Breaking the back button** in single-page apps, or losing state on back.
- **Hidden gestures** as the only way to perform actions.
- **Modal stacks and dead ends** with no clear exit.
- **Asking for data before showing value** (forced sign-up walls, long onboarding questionnaires).
- **Optimistic UI for unreliable or high-stakes operations**, causing "it said it worked" incidents.
- **Interaction designed only for mouse.**
- **Interrupting with notifications** and modals for marketing.

## Quality bar and verification

- [ ] Every user action produces perceivable feedback appropriate to its stakes and duration, including for assistive technology.
- [ ] All states and transitions of each flow are defined, including error, empty, slow, offline, cancelled and permission-limited paths.
- [ ] Each flow has been challenged for removable, deferrable or defaultable steps and fields.
- [ ] Validation timing is deliberate; errors are specific, adjacent, programmatically associated and preserve input.
- [ ] Destructive actions use undo where possible and specific confirmation where not; backend support is confirmed.
- [ ] Back, cancel and exit work everywhere without data loss; shareable states have URLs.
- [ ] Fully operable by keyboard; gestures and drag have visible alternatives; targets meet size guidance.
- [ ] Loading behaviour is defined for <1 s, 1–10 s and >10 s cases, without flicker or layout shift.
- [ ] The flow has been walked through with realistic tasks (ideally by representative users) and observed problems addressed.

**How to check:** if you can run a prototype or the app, perform each task end to end with keyboard only, on a touch device, with network throttling (slow and offline modes in browser devtools or a proxy), and with deliberate errors at each step. Note every moment of uncertainty ("did that work?"). If you cannot run anything, write the state table and walk through each row, stating what the user sees and can do; gaps in the table are gaps in the design.
