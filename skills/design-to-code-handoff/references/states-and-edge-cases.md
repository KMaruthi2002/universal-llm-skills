# States and Edge Cases Checklist

Read this when preparing a spec, or before implementing a complex screen or component. Not every item applies to every design; go through the list and decide, for each, whether it's designed, covered by a general rule, or irrelevant. "Not thought about" is the state to eliminate.

## Interactive element states

- Default / rest
- Hover (pointer devices only; never the only way to reveal something)
- Focus — visible, meeting the product's contrast requirements, distinct from hover
- Focus-visible vs. focus from pointer (if the product distinguishes them)
- Active / pressed
- Selected / checked / on; indeterminate (for checkboxes and tree selections)
- Disabled — and whether a disabled control should instead be hidden, or enabled with an explanatory message
- Read-only
- Loading / pending (after activation, before result)
- Dragging, drop target valid, drop target invalid (for drag-and-drop)
- Expanded / collapsed
- Current (in navigation: current page or step)

## Data and view states

- **First use / empty**: before anything exists; guidance and first action
- **Empty after filtering or search**: no results, with recovery options
- **Empty because the user cleared everything**: completion state
- **Loading — initial**: skeleton, spinner, or progressive rendering; layout stability
- **Loading — refresh / background update**: whether existing content stays visible
- **Loading — pagination or infinite scroll**: end-of-list state
- **Partial**: one item; few items; some fields missing
- **Full / overflow**: many items, very long lists, pagination or virtualization
- **Error — load failed**: message, retry, preserved context
- **Error — action failed**: what's preserved, how to retry, partial success (some items succeeded)
- **Stale / out of date**: data changed elsewhere; conflict on save
- **Offline / degraded connectivity**: what still works, what's queued
- **Success**: confirmation, next steps, undo
- **Permission-restricted**: read-only view, hidden actions, "request access"
- **Plan- or quota-limited**: upgrade path, limit reached
- **Feature-flagged**: what appears when the flag is off

## Forms

- Required vs. optional indication
- Hints and format guidance before entry
- Validation timing: on blur, on submit, as-you-type (and when that's appropriate)
- Field-level error, form-level summary, focus behavior on submit failure
- Server-side validation errors mapped back to fields
- Disabled submit vs. enabled submit with validation (and why)
- Pending submit: preventing double submission, showing progress
- Autofill and password manager compatibility
- Preserving input on error and on navigation away (with warning if unsaved)
- Multi-step: progress indication, back navigation, saving partial progress

## Content extremes

- Text: very short, very long, single word longer than its container, multi-line, user-generated text with emoji or mixed scripts
- Names: one name, very long names, non-Latin scripts, right-to-left text
- Numbers: zero, negative, very large, decimals, currencies with different symbol placement, percentages above 100
- Dates and times: today, yesterday, far past, far future, time zones, relative vs. absolute formats
- Counts: 0, 1, 2, many, thousands, "99+" style capping rules
- Images: missing, broken, loading, different aspect ratios, very large or very small source, transparency
- Avatars: missing (initials or placeholder rule), duplicate initials
- Lists and tags: none, one, overflowing a row
- Translations: longest expected expansion; plural forms

## Environment and settings

- Supported screen sizes across the full range, not just the drawn ones
- Orientation changes on mobile and tablets
- Browser zoom and operating-system text size increases
- High contrast or forced-colors modes
- Light and dark themes (and any other themes)
- Reduced motion preference
- Keyboard-only use
- Screen readers on the main supported platforms
- Touch, mouse, pen, and keyboard on the same device (hybrid devices)
- Slow networks and slow devices
- On-screen keyboard covering inputs on mobile
- Safe areas and notches; system bars
- Print styles, if users print

## Behavior edge cases

- Double clicks and rapid repeated actions
- Back and forward navigation; refresh mid-flow; deep links into the middle of a flow
- Multiple tabs or devices editing the same thing
- Session expiry during a task
- Long-running operations: progress, cancellation, leaving and returning
- Undo after navigation
- Notifications or real-time updates arriving while the user is acting

## Accessibility specifics

- Accessible names for icon-only controls
- Alt text rules for content images; decorative images marked as such
- Heading levels and landmark regions
- Focus order, focus trapping in modals, focus return after closing
- Live announcements for status changes, errors, and async results
- Error association with fields
- Target sizes for touch
- Not conveying meaning by color, shape, or position alone
