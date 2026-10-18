---
name: motion-design
description: >-
  Design and implement purposeful interface animation: deciding when motion
  helps (feedback, orientation, continuity, attention, character) and when it
  harms, easing curves and springs, duration by distance and size,
  choreography and staggering, transitions between states and screens
  (including shared-element and view transitions), loading and skeleton
  motion, performance (compositor-friendly properties, frame budgets, layout
  thrash), and reduced-motion and vestibular safety. Use when adding
  animations or transitions, picking easing or timing, making a UI feel
  "smoother", "snappier" or "more alive", fixing janky or laggy animation,
  defining motion tokens, or handling prefers-reduced-motion. For what the
  interaction should do (not how it moves) use interaction-design.
metadata:
  category: design
  related: interaction-design, ui-design-fundamentals, accessible-design, design-systems, performance-optimization, web-performance-audit, frontend-development, game-development
---

# Motion Design

Motion in an interface is information delivered over time. Done well it explains what changed, where things came from and went, what responds to what, and what deserves attention. Done badly it slows people down, distracts, makes some users physically ill, and drains battery. The question is never "how do we add animation?" but "what does the user need to understand that motion can explain better than a cut?"

This skill covers the craft and engineering of UI motion. The behaviour being animated (states, flows, feedback) is `interaction-design`. Motion graphics for video, marketing animation and game animation share principles but have additional craft not covered here (see `game-development` for real-time game feel).

## Core principles

1. **Motion must have a job.** Legitimate jobs: **feedback** (the button registered the press), **orientation** (the panel slid in from the right, so it lives to the right), **continuity** (this thumbnail became that detail view), **state change** (the item was deleted, not just gone), **attention** (something needs you, sparingly), and **character** (brand expression, sparingly and never at the cost of speed). If you cannot name the job, remove the motion.
2. **Fast by default.** Interface motion is there to clarify, not to perform. Most UI transitions sit roughly between 100 and 500 ms (the range given by Material Design and Nielsen Norman Group guidance); small, frequent feedback toward the short end, large spatial transitions toward the long end. Anything that delays the user's next action must earn its time.
3. **Natural, not linear.** Real objects accelerate and decelerate. Linear motion looks mechanical except for continuous loops (spinners, progress) and opacity fades.
4. **Consistent physics.** Similar things move similarly across the product. Motion is part of the visual language and belongs in tokens (durations, easings, springs) like color and spacing.
5. **Respect the user's body and settings.** Large or parallax motion can trigger vestibular symptoms (dizziness, nausea, migraines). Honour reduced-motion preferences, avoid flashing (WCAG 2.3.1: no more than three flashes per second above thresholds), and let users pause anything that moves for more than five seconds (WCAG 2.2.2).
6. **Smooth or none.** A janky animation is worse than an instant change. Animate properties the rendering engine can handle cheaply and test on modest hardware.

## Discovering context

- **Existing motion language:** look for motion tokens (duration and easing variables), animation utilities, a motion section in the design system docs, platform defaults in use (e.g. native navigation transitions), and how existing components animate. Extend these rather than inventing new curves.
- **Brand character:** some brands call for crisp, minimal motion; others for playful, springy motion. Ask, or infer from brand attributes (see `visual-design`), and present options.
- **Platform conventions:** iOS, Android, Windows and the web have characteristic system transitions and spring behaviours. Native apps should usually match platform navigation transitions; users notice when they do not.
- **Technical stack and constraints:** CSS transitions/animations, the Web Animations API, View Transitions API, framework libraries (examples: Motion/Framer Motion, GSAP, React Spring, Vue transitions), native APIs (Core Animation, SwiftUI animations, Jetpack Compose animation, Flutter implicit/explicit animations), Lottie/Rive for authored vector animation. Know what the project already uses before adding a dependency.
- **Performance budget and devices:** low-end Android phones, older laptops, TVs and embedded webviews may not keep up.

## When to animate — decision guide

| Situation | Motion helps? | Notes |
|---|---|---|
| Element enters or leaves the screen (dialog, sheet, toast, menu) | Usually yes | Shows origin and that it is a layer. Keep short. |
| Navigating between hierarchical levels | Often yes | Directional movement (push/pop) supports spatial model. |
| Item added, removed, reordered in a list | Yes | Prevents "where did it go?"; animate surrounding items into place. |
| Expanding/collapsing content | Yes, briefly | Shows what expanded; avoid long height animations. |
| Thumbnail → detail view | Yes | Shared-element transition shows continuity. |
| State change of a control (toggle, checkbox, like) | Yes, small | Feedback; tens to low hundreds of ms. |
| Data updates in a chart | Sometimes | Helps track change; avoid when updates are frequent. |
| Page load / initial render | Rarely | Entrance animations on every load delay content and repeat on each visit. |
| Scroll-driven effects, parallax | Rarely | High vestibular risk, performance cost; must be optional and reduced. |
| Decorative ambient motion (floating blobs, animated gradients) | Rarely | Distracting, battery cost; must be pausable if >5 s. |
| Frequent, repeated actions (typing, rapid navigation in expert tools) | Minimise | Repetition turns any delay into friction. |
| Errors | Small, specific | A brief shake or highlight can draw attention, but always with text; never motion alone. |

Rule of thumb: the more often an interaction happens, the less motion it should have.

## Easing

Easing describes how velocity changes over the animation.

| Curve | Character | Typical use |
|---|---|---|
| **Ease-out** (decelerate: fast start, slow end) | Responsive, arriving | Elements **entering** the screen, responses to user input. The most generally useful UI curve. |
| **Ease-in** (accelerate: slow start, fast end) | Departing | Elements **leaving** the screen permanently. Avoid for entrances — it feels sluggish at the start. |
| **Ease-in-out** (accelerate then decelerate) | Deliberate | Elements **moving** from one on-screen position to another, or changing size in place. |
| **Linear** | Mechanical | Opacity-only fades, continuous rotation (spinners), progress, and scroll-linked effects where position maps to scroll. |
| **Spring / physics** | Natural, interruptible | Gesture-driven motion (drag, swipe, fling), playful brands, anything that may be interrupted mid-animation. Parameterised by stiffness/damping (or response/bounce) rather than duration. |

Notes:

- The CSS keyword curves (`ease`, `ease-in`, `ease-out`, `ease-in-out`) are mild. Many systems define custom cubic-béziers with stronger deceleration for more "snap". Define a small set (e.g. standard, enter, exit, emphasised) as tokens.
- **Springs handle interruption gracefully**: when a user reverses a gesture mid-animation, a spring continues from current velocity instead of restarting. Prefer them for direct manipulation.
- **Overshoot / bounce** conveys playfulness and physicality; it also adds perceived duration and can feel unprofessional in serious contexts. Use deliberately and subtly.

## Duration

Duration should scale with **distance travelled, size of the element, and complexity of the change**, and inversely with frequency of use.

Indicative ranges (examples consistent with Material Design and NN/g guidance; tune to the product):

| Change | Indicative duration |
|---|---|
| Micro feedback (press, hover, toggle, checkbox) | ~50–150 ms |
| Small component transitions (tooltip, menu, fade) | ~100–200 ms |
| Medium (dialog, sheet, card expand, list reorder) | ~200–350 ms |
| Large, full-screen or complex choreography | ~300–500 ms |
| Beyond ~500 ms | Rare in UI; feels slow unless it is an intentional, infrequent moment |

Further guidance:

- **Exits are usually faster than entrances** (the user has already decided to dismiss; do not make them watch it go).
- **Larger screens can use shorter durations for the same element** because relative distance is smaller; Material's guidance has suggested longer transitions on tablets and shorter on wearables relative to phones. Treat as context, not rule.
- **Do not block input during motion.** Users should be able to act before the animation finishes; animations should be interruptible.
- Motion durations go in tokens (`duration.fast`, `duration.moderate`, `duration.slow`) so they can be tuned globally and reduced under reduced-motion settings.

## Choreography

When several elements move, their relationship matters.

- **One focal motion at a time.** Several equally prominent simultaneous movements compete for attention.
- **Stagger** related items (list entries, grid cards) with short offsets (often ~20–50 ms per item) and cap the total so long lists do not take seconds to appear — stagger the first handful, show the rest together.
- **Lead with the most important element**, follow with supporting ones.
- **Shared elements** that persist across a transition should move continuously (shared-element / "hero" / view transitions); everything else fades or slides in a supporting role.
- **Consistent direction:** forward navigation moves one way, back the opposite; sheets come from and return to the same edge. Mirror direction for RTL layouts.
- **Hierarchy of movement:** parent containers move first, children settle after (or the reverse when collapsing).

## Transitions between states and screens

Common patterns, with their jobs:

| Pattern | Job | Notes |
|---|---|---|
| Fade (cross-fade) | Replace content without spatial relationship | Safest; also the default reduced-motion substitute. |
| Slide / push | Hierarchical or sequential navigation | Direction encodes forward/back. |
| Scale + fade from origin | Element emerges from its trigger (menu from button, dialog from card) | Show the connection; transform-origin at the trigger. |
| Container transform / shared element | One element becomes another (card → detail) | Strongest continuity; more engineering effort. |
| Expand / collapse | Disclosure | Animating height is expensive on the web; consider transform-based techniques, grid-row tricks, or very short durations. |
| Skeleton shimmer / pulse | Loading | Keep subtle; respect reduced motion (static skeleton). |
| Layout animation (FLIP technique) | Items reflowing after add/remove/reorder | Measure first and last positions, animate the difference using transforms. |

On the web, the **View Transitions API** provides cross-fade and shared-element transitions between DOM states (and between documents in supporting browsers); check browser support for the project and provide a no-transition fallback.

## Performance

Smooth motion needs each frame produced within the display's budget: about **16.7 ms at 60 Hz**, **8.3 ms at 120 Hz**. Any work in the frame (scripts, style recalculation, layout, paint, composite) counts.

### Animate cheap properties

On the web, **`transform`** (translate, scale, rotate) and **`opacity`** can typically be animated on the compositor without triggering layout or paint; some filters can also be composited depending on browser. Animating layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`) triggers layout every frame; animating paint properties (`box-shadow`, `background-color`, `border-radius` in some cases) triggers repaint. Native platforms have analogous rules (e.g. animate layer transforms and alpha rather than frame/layout constraints where possible).

Techniques:

- Express movement as `transform` and size changes as `scale` (compensating children if needed), or use FLIP for layout changes.
- Fade shadows by animating the opacity of a pseudo-element with the shadow, not the shadow itself.
- Use `will-change` (or equivalent layer promotion) **sparingly and temporarily**: each promoted layer costs memory, and over-promotion can make things slower.
- Avoid reading layout (e.g. `getBoundingClientRect`, `offsetHeight`) and writing styles alternately in the same frame (layout thrashing); batch reads then writes; use `requestAnimationFrame` for script-driven animation.
- Prefer CSS transitions/animations or the Web Animations API for simple cases; they can run off the main thread when animating compositor properties. JavaScript animation libraries are useful for physics, sequencing and gesture tracking; ensure they animate transforms.
- Scroll-linked effects: prefer native scroll-driven animations (CSS scroll timelines where supported) or passive listeners with `requestAnimationFrame`; never do heavy work in scroll handlers.
- Large blurred or translucent layers (backdrop filters, glass effects) are expensive, especially on low-end devices and while animating.
- Pause off-screen and background-tab animations; continuous animation costs battery.
- Lottie/Rive and video animations: check file size, CPU use and that they can be paused.

Measure with the platform's profiler (browser devtools performance panel with CPU throttling, frame rendering stats, Xcode Instruments, Android GPU rendering profiling). See `performance-optimization` and `web-performance-audit`.

## Reduced motion and vestibular safety

Users can request reduced motion at OS level (macOS/iOS "Reduce Motion", Windows "Show animations" setting, Android "Remove animations"), exposed on the web as the `prefers-reduced-motion` media query and on native platforms through accessibility APIs.

**Reduced motion does not mean no feedback.** It means removing or replacing motion that involves large movement, zoom, parallax, spinning or scroll-linked effects — while keeping state changes perceivable.

| Full motion | Reduced-motion substitute |
|---|---|
| Slide / push navigation | Cross-fade or instant change |
| Zoom / scale-in of large surfaces | Fade |
| Parallax and scroll-linked movement | Static |
| Auto-playing carousels and background video | Paused by default with play control |
| Bouncy springs | Short ease-out or instant |
| Skeleton shimmer | Static placeholder |
| Small color/opacity feedback on controls | Usually keep (low risk, carries information) |

Relevant WCAG criteria:

- **2.2.2 Pause, Stop, Hide (A):** moving, blinking or scrolling content that starts automatically, lasts more than 5 seconds and is shown alongside other content must be pausable, stoppable or hideable.
- **2.3.1 Three Flashes or Below Threshold (A):** nothing flashes more than three times per second (unless below general and red flash thresholds).
- **2.3.3 Animation from Interactions (AAA):** motion triggered by interaction can be disabled unless essential. Even if not targeting AAA, honouring `prefers-reduced-motion` is the standard way to meet this and is widely expected.

Implementation approaches: define motion tokens that collapse to near-zero or fade-only values under reduced motion; or write motion as an enhancement applied only when the user has *no* preference. Test with the OS setting actually enabled.

Also consider: an in-product motion toggle for users who do not know the OS setting; avoiding large-scale motion entirely for health and medical audiences or users likely to be on moving vehicles; and that motion can be cognitively distracting for some users even when not physically triggering.

## Character: deriving a motion personality

Motion expresses brand as much as type and color. Derive it from the same attributes used in `visual-design`, then present options.

| Attribute leaning | Motion tendencies (options, not rules) |
|---|---|
| Precise, efficient, professional | Short durations, strong deceleration, little or no overshoot, minimal choreography. |
| Warm, friendly, approachable | Slightly softer curves, gentle springs with low bounce, modest stagger. |
| Playful, energetic | Springier motion, visible overshoot on small elements, more expressive feedback — confined to low-frequency moments. |
| Calm, premium, editorial | Slower, smoother fades and long eases on large media moments; still fast on controls. |
| Serious, high-stakes (health, finance, safety) | Minimal, predictable motion; no bounce; nothing that could read as frivolous or distracting. |

Two cautions: personality belongs mainly in **infrequent** moments (onboarding, success states, empty states), not in the controls used hundreds of times a day; and platform-native navigation transitions usually should not be replaced for the sake of brand.

## Platform conventions

- **iOS:** system navigation uses push/pop slides with interactive edge-swipe back, sheets slide up and can be dragged, and most system motion is spring-based. Custom navigation that ignores edge-swipe back feels broken.
- **Android:** Material motion patterns (container transform, shared axis, fade through, fade) are a well-documented vocabulary; predictive back gestures preview the destination before commit in recent versions.
- **Desktop:** users expect less motion and faster responses; window and menu animations are brief, and many users disable animations entirely.
- **Web:** no single convention; follow the product's design system, honour browser back behaviour, and avoid scroll hijacking.

## Gesture-driven motion

When the user's finger or pointer drives motion (drag, swipe to dismiss, pull to refresh, bottom-sheet resizing, carousels):

- **Track the input 1:1** while the gesture is active. Any lag or easing applied during tracking makes the object feel detached.
- **On release, hand off velocity** to a spring or decay animation so the motion continues naturally; decide the destination by position *and* velocity (a fast flick dismisses even if it has not crossed the halfway point).
- **Provide resistance at limits** (rubber-banding) instead of hard stops, so users know they have reached an edge.
- **Allow reversal** at any point; the gesture should be cancellable by moving back.
- **Offer a non-gesture alternative** (button, menu) for every gesture-driven action (WCAG 2.5.1, 2.5.7).

## Loading and progress motion

- Indeterminate spinners are linear, continuous rotation; keep them small and delay their appearance for short waits (see latency guidance in `interaction-design`).
- Skeleton shimmer should be slow and low-contrast; a gentle pulse or a static skeleton is often enough, and static is the reduced-motion substitute.
- Determinate progress should never move backwards and should not stall at 99%; if progress is unknowable, say so rather than faking it.
- When content arrives, cross-fade skeleton to content in place with no layout shift.

## Motion in data visualisation

- Animate transitions between data states (filter change, time step) so viewers can track which mark became which; keep durations short (the data, not the animation, is the point).
- Use consistent object constancy: the same data item should map to the same mark across transitions.
- Do not animate on every live update in high-frequency streams; batch or disable to avoid a constantly moving chart.
- Initial "grow-in" animations on charts rarely add information; skip them in dashboards users visit daily. See `data-visualization`.

## Worked example: specifying a dialog

Illustrative spec (values are examples within the ranges above, not a mandate):

| Element | Property | Enter | Exit |
|---|---|---|---|
| Scrim | opacity | 0 → target, ~150–200 ms, linear or ease-out | target → 0, ~100–150 ms |
| Dialog | opacity | 0 → 1, ~150–250 ms, ease-out | 1 → 0, ~100–150 ms, ease-in |
| Dialog | transform | slight scale-up (e.g. from ~0.95) or short translate, same duration, ease-out | optional; often fade only |
| Focus | — | moves into dialog when it becomes interactive (do not wait for the animation to end) | returns to trigger |
| Reduced motion | — | opacity only, or instant | opacity only, or instant |
| Interruption | — | closing mid-enter reverses from current state | — |

Why these choices: ease-out on entry so the dialog feels responsive; faster exit because the user already decided; scale/translate small enough to suggest emergence without large movement; focus moves immediately so keyboard and screen-reader users are not delayed by decoration.

## Worked example: removing an item from a list

1. The removed item fades and/or collapses (short, ease-in, since it is leaving).
2. Items below move up to fill the gap (ease-in-out, since they move on screen), starting as the removed item collapses, using transform-based layout animation (FLIP) to avoid animating height on many elements.
3. A toast with Undo enters (ease-out). If Undo is pressed, the item re-enters at its original position and neighbours make room.
4. Reduced motion: item disappears, neighbours reposition instantly, toast fades in.

This makes the state change legible ("it was removed, and that is where it was") which also makes undo understandable.

## Implementing reduced motion

Two common patterns (web shown as illustration; native platforms expose equivalent settings):

- **Reduce by override:** write motion normally and, inside a `prefers-reduced-motion: reduce` media query, swap duration tokens to near-zero and replace movement transforms with fades.
- **Enhance by opt-in:** write the static/fade version by default and add movement only inside `prefers-reduced-motion: no-preference`. This fails safe: if the query is unsupported, users get the calmer version.

For script-driven animation, read the preference (e.g. `matchMedia` on the web, accessibility settings APIs natively), listen for changes, and route all animation through a helper that respects it, so individual components cannot forget.

## Motion as a system

Encode motion like any other design decision (see `design-systems`):

- **Duration tokens** (a small scale), **easing tokens** (standard, enter, exit, emphasised; plus spring presets if used), and **pattern definitions** (how dialogs enter, how lists reorder, how navigation transitions).
- Document the job of each pattern and the reduced-motion substitute.
- Provide specs designers and engineers both use: property, from/to values, duration, easing, delay, trigger, interruption behaviour. Prototyping tools (examples: Figma prototypes, Principle, ProtoPie, Rive, After Effects with Lottie export) or coded prototypes can demonstrate; the spec is what makes it reproducible (see `design-to-code-handoff`).

## Process

1. **Identify moments** where users lose track of change, need feedback, or need orientation (from the state model in `interaction-design`).
2. **Name the job** of motion at each moment; drop moments without one.
3. **Check the existing motion language** and platform conventions; reuse tokens and patterns.
4. **Choose pattern, easing and duration** by job, distance, size and frequency.
5. **Choreograph** multi-element changes: one focal motion, short staggers, consistent direction.
6. **Define the reduced-motion substitute** for each.
7. **Prototype in the real medium** (coded or high-fidelity), because timing perceived in a static spec rarely matches reality; tune by watching at actual speed, and again at slowed speed to spot glitches.
8. **Profile performance** on low-end target hardware.
9. **Spec and tokenise** for handoff.

## Pitfalls

- **Motion as decoration:** entrance animations on every section of a page, floating shapes, constant pulses. Common in generic, template-like UI; it slows reading and signals "demo" rather than "tool".
- **Too slow:** 600–1000 ms transitions for routine actions; users wait for the interface.
- **Blocking input** until an animation completes.
- **Wrong easing:** ease-in for entrances (sluggish), linear for movement (robotic).
- **Everything moves at once** with no focal point.
- **Long staggers** on long lists.
- **Animating layout properties** causing jank; heavy blur/glass effects animating on low-end devices.
- **Ignoring reduced motion**, or implementing it by removing all feedback.
- **Parallax and scroll hijacking** that override native scrolling, harming accessibility and control.
- **Auto-playing carousels** with no pause (WCAG 2.2.2), which also tend to be ignored by users.
- **Inconsistent curves and durations** across components because each was tuned by eye in isolation.
- **Motion that conveys meaning alone** (a shake for error with no message).
- **Testing only on a fast development machine.**

## Quality bar and verification

- [ ] Every animation has a named job (feedback, orientation, continuity, state change, attention, character); decorative motion is minimal and justified.
- [ ] Durations and easings come from a small, tokenised set and follow job/distance/size/frequency logic; routine transitions are within ~100–500 ms.
- [ ] Entrances decelerate, exits are quicker, on-screen moves ease in and out; gesture-driven motion is interruptible.
- [ ] Input is never blocked by animation.
- [ ] Multi-element transitions have a clear focal motion and bounded total duration.
- [ ] Animations use compositor-friendly properties where possible and hold frame rate on low-end target devices (profiled, not assumed).
- [ ] `prefers-reduced-motion` (or platform equivalent) is honoured with defined substitutes that preserve feedback; tested with the OS setting on.
- [ ] Nothing flashes more than three times per second; auto-moving content over 5 s can be paused.
- [ ] Motion never carries meaning by itself.

**How to check:** if you can run the UI, watch each transition at full speed and at reduced speed (browser devtools animation panel, simulator slow animations), record frame rates with CPU throttling or on a low-end device, enable the OS reduced-motion setting and repeat, and interrupt animations mid-flight. If you cannot run it, review specs/code for animated layout properties, durations above ~500 ms, missing reduced-motion handling and input blocking, and list what must be verified on device.
