---
name: game-development
description: >-
  Plan and build playable games — 2D or 3D, browser, desktop, mobile or console
  — from first prototype to shippable build: choosing an engine, framework or
  from-scratch approach, the game loop and timing, state and scene management,
  input, rendering, physics and collision basics, game feel, audio, asset
  pipeline, save data, scope control, playtesting and performance. Use when
  someone asks to make a game, prototype a game mechanic, build a game jam
  entry, add a feature to an existing game, fix jittery movement or frame-rate
  problems, choose between engines, or make a game "feel better".
metadata:
  category: app-generation
  related: mvp-prototyping, interaction-design, motion-design, performance-optimization, software-architecture, testing-strategy, frontend-development, desktop-app-development, mobile-app-development, project-scaffolding
---

# Game Development

A game is software whose primary requirement is that it is fun to interact with, frame by frame. That requirement cannot be specified up front; it is discovered by playing. Everything in this skill follows from that: get something playable immediately, iterate on feel with fast feedback, keep scope brutally small, and build only the architecture the game has proven it needs.

## Scope

Covers: making games of any genre and size with any toolset — engines (e.g. Godot, Unity, Unreal, GameMaker, Bevy, Defold), frameworks and libraries (e.g. Phaser, PixiJS, Three.js, Babylon.js, LÖVE, raylib, MonoGame, SDL, pygame), or from scratch on Canvas/WebGL/WebGPU/native graphics APIs. Game loop, architecture, input, rendering, physics, feel, audio, assets, saving, playtesting, performance and shipping.

Does not cover in depth: monetisation and live-ops strategy, multiplayer netcode beyond orientation (see `references/multiplayer-orientation.md`), shader programming as a discipline, or art and music creation. Visual and UI design of menus draws on `ui-design-fundamentals` and `interaction-design`; animation timing principles on `motion-design`.

## Core principles

1. **Playable first, always playable after.** Within the first session of work the game should run and respond to input, even if everything is coloured rectangles. Every change after that keeps it runnable. Why: fun is only observable in play, and a game that has been unplayable for a week has accumulated untested assumptions about what is fun.

2. **Find the core loop and protect it.** The core loop is the 10–60 seconds of activity the player repeats (jump-collect-avoid; aim-shoot-reposition; plan-place-watch). If the core loop is not engaging with placeholder art, more content and polish will not save it. Spend the first iterations only on the core loop.

3. **Scope is the main risk.** Most unfinished games die of scope, not technical difficulty. Cut features until the game is embarrassingly small, then build that. A finished small game teaches more and ships; an ambitious half-game does neither. Why: content cost scales with features multiplicatively (each new mechanic interacts with every level, enemy and UI state).

4. **Separate simulation from presentation.** Game state and rules (where things are, what happens when they touch) should be updatable without rendering, and rendering should read state without changing it. Why: this makes timing correct, enables pausing, replays, saving, testing, headless servers and frame-rate independence, and it keeps bugs localised.

5. **Time is a first-class input.** Every movement and timer depends on elapsed time. Handle it deliberately — fixed or variable step, clamped deltas — or the game will run differently on different machines.

6. **Feel is made of small things.** Responsiveness, feedback and readability come from dozens of tiny details: input buffering, acceleration curves, hit pause, screen shake, sound on every action. They are cheap individually and decisive together. Budget time for them.

7. **Respect the tool's way.** Every engine has an intended architecture (scenes and nodes, GameObjects and components, entities and systems). Working with it is faster than fighting it. When extending an existing game, follow its patterns even if you would have chosen differently.

## Choosing the approach

Ask first: target platforms, team skills, 2D vs 3D, scope and timeline, whether the user already has a tool, and whether learning low-level techniques is itself a goal.

| Approach | Choose when | Costs |
|---|---|---|
| **Full engine** (editor, scene system, physics, export pipeline) | 3D of any seriousness; console or many-platform export; non-programmers on the team; you want tools for levels and animation | Learning curve; engine conventions; binary/project file formats in version control; licensing terms to check |
| **Framework/library** (rendering, input, maybe physics; you write the structure) | 2D, browser-first, programmers only, want code-centric control, small download size | You build scene management, tooling, editors yourself |
| **From scratch** (graphics API or Canvas directly) | Tiny games, learning goals, extreme constraints (size-limited jams, unusual hardware), or the game's core is novel rendering | Everything takes longer; easy to spend the project on the engine instead of the game |

Heuristics:

- If the user has a tool they know, use it. Familiarity beats theoretical fit for almost every game-sized project.
- For a quick browser game or prototype, a 2D web framework or plain Canvas gets to "playable" fastest and shares easily via a URL.
- For 3D with physics, animation and lighting, an engine saves months.
- "I want to build my own engine" is a valid goal — but confirm whether the user wants to build an engine or ship a game, because those are different projects.
- Check licensing (revenue thresholds, royalties, runtime fees, open-source licences) before committing to a commercial project; terms have changed abruptly in the industry before.

## Process

### 1. Clarify the game in one paragraph

Capture: genre and reference games, the core loop, the player's verb(s), win/lose conditions, target platform and input device, session length, and the single thing that makes it interesting. Ask for whatever is missing that changes the build. "A platformer" is not enough; "a one-screen platformer where gravity flips on every jump, keyboard, browser, 2-minute runs" is buildable.

### 2. Discover context (existing project)

- Identify engine/framework and version; open the project the way its users do (editor or build command).
- Find the main scene/entry, the game loop owner, and how objects are organised (scene tree, prefabs, ECS, plain classes).
- Find how input is mapped (input map/actions vs raw keys) and reuse it.
- Find the asset import conventions (folders, naming, import settings, atlases).
- Check how the project runs and whether there are tests or debug scenes.
- Note coding conventions and follow them — signal/event usage, naming, folder layout.

### 3. Prototype the core loop with placeholder everything

- Shapes for art, no menus, one level/arena, debug keys to reset and tweak.
- Expose tuning values (speed, gravity, jump height, cooldowns) as variables in one place, ideally live-editable. Feel is tuned by changing numbers while playing.
- Play it. Have someone else play it. Ask: what do I want to do next? Where am I bored? Where am I confused?
- Decide: keep, change or kill. Killing a prototype after two hours is a success.

### 4. Build the vertical slice

One complete, representative portion of the game at near-final quality: start to end of one level, with real feedback, sound, UI, and fail/retry. This exposes the real pipeline and the real per-content cost, which you then use to plan the rest.

### 5. Produce content, then polish, then ship

- Estimate content from the vertical slice's actual cost and cut to fit time.
- Polish in priority order: anything that confuses players, anything that makes core actions feel unresponsive, then juice and visual flourish.
- Leave real time for menus, settings, saving, pause, resolution/scaling, audio volume, input remapping where appropriate, build/export, and store pages. These routinely take longer than the game itself expected.

## Scope control in practice

Scope control is a habit, not a single decision. Techniques that work:

- **Write a "not this game" list** alongside the feature list. Every new idea goes on one list or the other, explicitly. Ideas on the "not" list are not lost; they are the sequel.
- **Count the multiplier.** Before adding a mechanic, ask how many existing things it interacts with (levels, enemies, UI states, save data, tutorial). A mechanic that touches everything costs more than three that touch nothing.
- **Time-box prototypes** (hours, not days). If the mechanic is not interesting by the end of the box, it is unlikely to become interesting with more time.
- **Cut sideways, not down.** Prefer fewer levels at full quality over many at half quality; fewer enemies with distinct behaviour over many reskins.
- **Ship-shaped milestones.** Each milestone should be something you could release if you had to stop.

Worked example — user: "Make me a roguelike with crafting, procedural dungeons, multiplayer and a story."

Reasoning: each of those is a project. Ask which one is the heart of the idea. Suppose it is "dungeon crawling where you build weapons from enemy parts". Proposed first build: one procedurally arranged floor from hand-made rooms, three enemy types each dropping one part, a crafting screen combining two parts into a weapon with a visible effect, death restarts the run. Explicitly deferred: story, multiplayer, more floors, meta-progression. That build is playable in days and answers the only question that matters yet: is building weapons from parts fun?

## Shipping and builds

- Automate the export/build for each platform as early as the vertical slice; a build that only works from one developer's editor is a release risk.
- Test the exported build, not only the editor run — asset loading, paths, case-sensitive filesystems, and stripped debug code differ.
- For web: check file sizes and compression, loading screen, mobile browsers, and that the game handles tab hiding (pause on visibility change).
- For stores: prepare icons, capsule/screenshot images, age ratings questionnaires, privacy disclosures, and platform-required features (achievements, controller support declarations) well before the target date; certification for consoles has its own long checklists.
- Keep a changelog and version numbers visible in the game for bug reports.
- Crash/error reporting in released builds (with consent where required) shortens the bug loop dramatically.

## The game loop and timing

Every game repeats: read input → update simulation → render. The decisions are about time.

**Variable timestep**: update once per frame with `dt` = time since last frame. Simple, smooth, but physics and collision become frame-rate dependent (tunnelling at low fps, different jump heights at different rates).

**Fixed timestep with accumulator**: simulation advances in fixed steps (e.g. 1/60 s); rendering happens once per frame and may interpolate between the last two simulation states.

```
accumulator += min(frame_dt, MAX_FRAME_DT)    // clamp avoids the spiral of death
while accumulator >= STEP:
    previous_state = current_state
    update(current_state, STEP)
    accumulator -= STEP
alpha = accumulator / STEP
render(interpolate(previous_state, current_state, alpha))
```

Illustrative pseudocode; engines usually provide this split (a fixed/physics update and a per-frame update/process callback).

| Choose | When |
|---|---|
| Fixed step | Physics, platformers, anything where determinism, replays, or fairness matter; networked games |
| Variable step | Simple arcade games, UI-heavy games, when the engine handles physics separately |
| Engine default split | Almost always when using an engine: physics in its fixed callback, visuals/input polling in the per-frame callback |

Timing rules:

- Multiply every velocity, timer and interpolation by `dt` (in variable-step code). Missing a `dt` is the classic "game runs faster on a 144 Hz monitor" bug.
- Clamp large `dt` (tab switch, breakpoint, load hitch) so objects do not teleport through walls.
- Use `requestAnimationFrame` (browser) or vsync'd present (native); do not drive the loop with fixed-interval timers.
- Lerping toward a target with a constant factor per frame (`x += (target - x) * 0.1`) is frame-rate dependent; use an exponential decay form based on `dt` (`x += (target - x) * (1 - exp(-rate * dt))`).
- Pausing means not advancing simulation time, not stopping the render loop — menus still need to draw and animate.

## State and architecture

Grow architecture as the game proves the need. Typical progression:

1. **A few objects with update/draw methods** — fine for a jam game.
2. **Scenes/states** (title, play, pause, game over) managed by a state machine or scene stack. Needed almost immediately; menus and pause appear early.
3. **Entities with composable behaviour** — engine nodes/components, or an entity-component-system when entity counts are large or behaviours combine in many ways.
4. **Events/signals** to decouple systems (score UI listens for "enemy died" instead of enemies calling the UI).

Guidelines:

- Use **finite state machines** for anything with modes: player (idle, run, jump, fall, hurt), enemies' AI, game flow. Most "the player can jump while dead" bugs are missing states.
- Keep **one source of truth** for each piece of state. If the score lives in the HUD label and a variable, they will diverge.
- **Data-drive content**: levels, enemy stats, waves, dialogue in data files or engine resources rather than code, so tuning and content work does not require code changes.
- **Object pooling** for frequently spawned/destroyed things (bullets, particles) when allocation or garbage collection causes hitches — measure first.
- **Avoid deep inheritance hierarchies** for game objects (`Enemy → FlyingEnemy → ShootingFlyingEnemy`); composition handles combinatorial behaviour better.
- **Singletons/autoloads** are acceptable for genuinely global services (audio, save, settings) and hazardous for game state; prefer passing references or events for the latter.

## Input

- Map **physical inputs to actions** ("jump", "fire", "move_x") rather than reading keys directly. This enables rebinding, multiple devices and cleaner code.
- Distinguish **pressed this frame**, **held**, and **released this frame**. Read them in the per-frame update; consume them in the fixed update with care so short presses are not missed between fixed steps (buffer them).
- **Input buffering**: remember a jump pressed slightly before landing (e.g. ~100 ms) and execute it on landing.
- **Coyote time**: allow a jump shortly after walking off a ledge.
- Support the platform's expected devices: gamepad on desktop/console, touch on mobile (with on-screen controls sized for thumbs and placed away from system gesture areas), keyboard and mouse on web.
- Handle focus loss: release all held inputs when the window loses focus, or keys stick.
- Consider accessibility from the start: remappable controls, no required rapid tapping without an alternative, hold-vs-toggle options, readable text size, colour-blind-safe signalling, subtitles, and reduced screen shake/flash options.

## Rendering

- Pick a **coordinate and scaling strategy** early: fixed virtual resolution scaled to the window (pixel art usually integer-scaled with nearest-neighbour filtering), or resolution-independent with UI anchored to edges. Test at several aspect ratios.
- **Draw order**: layers or z-index for 2D; understand transparency sorting in 3D.
- **Batching**: draw calls, not pixels, are often the bottleneck. Use texture atlases/sprite sheets and the engine's batching. In 3D, watch material count and use instancing for repeated meshes.
- **Camera**: smooth follow with dead zones and look-ahead; clamp to level bounds; snap to whole pixels in pixel art to avoid shimmer.
- **Readability over fidelity**: the player must instantly distinguish themselves, threats, pickups and the background. Contrast, silhouette and motion matter more than detail.

## Physics and collision basics

- Decide between **engine physics** (rigid bodies, joints — good for physics-driven play) and **kinematic/character controllers** (you control movement and resolve collisions — usually better for tight platformer/action control). Many games mix them.
- Use the simplest shapes that work: circles and axis-aligned boxes for 2D gameplay; capsules for characters in 3D.
- **Broad phase then narrow phase**: spatial grid or tree to find candidate pairs, then exact tests. Engines do this; from-scratch code with O(n²) checks stops scaling around a few hundred objects.
- **Tunnelling**: fast objects pass through thin walls in one step. Fix with continuous collision detection, smaller steps, raycasts along the movement, or thicker colliders.
- **Collision layers/masks**: define early which categories collide with which (player, enemy, player bullets, world, triggers). Ad hoc checks in code rot quickly.
- Resolve collisions **per axis** for simple 2D tile games to avoid sticking on corners.
- Don't scale physics bodies non-uniformly or set positions of simulated bodies directly every frame; it fights the solver.

## Game feel

Feel is the moment-to-moment sense of control and impact. Techniques, roughly in order of payoff:

- **Responsiveness**: action begins on the frame the input arrives; animation can catch up. Long wind-up animations before a jump make controls feel mushy.
- **Acceleration and deceleration curves** rather than instant full speed — but short; tune per game.
- **Variable jump height** (cut upward velocity on release), higher gravity when falling.
- **Feedback for every action**: sound, particle, flash, animation squash/stretch. Silence and stillness read as "nothing happened".
- **Hit pause/hitstop**: freeze for a few frames on impact.
- **Screen shake** and camera kick — small, brief, and with a setting to reduce or disable.
- **Easing and tweening** on UI and pickups (see `motion-design`).
- **Forgiveness**: generous hitboxes for the player's attacks and pickups, tight ones for hazards.

Change one tuning variable at a time while playing, and write down values that felt right.

## Audio

- Every player action and important event deserves a sound; it is half of feedback.
- Separate buses/groups for music, effects, UI, voice; expose volume settings.
- Randomise pitch/volume slightly on repeated sounds to avoid fatigue.
- Limit simultaneous instances of the same sound.
- Browsers block audio until a user gesture; start or resume the audio context on the first click/keypress.
- Use compressed formats appropriate to the platform; stream long music, preload short effects.

## Assets and pipeline

- Keep **source assets** (layered art files, project files for audio) separate from **exported runtime assets**, and make export repeatable.
- Establish naming and folder conventions early; follow the project's if they exist.
- Use texture atlases, power-of-two textures where the platform prefers them, and appropriate compression per platform.
- Large binaries in version control: use Git LFS or the engine's recommended VCS setup, and configure ignore files for engine caches (see `git-workflow`).
- **Licensing**: record the source and licence of every third-party asset (art, audio, fonts, code). Do not use assets without clear rights; "found on the internet" is not a licence. Many free asset packs require attribution.
- Placeholder assets should be obviously placeholder so none ship by accident.

## Save data and settings

- Version the save format from the first save. Migrate old saves on load.
- Save atomically (write to a temp file, then rename) to avoid corruption on crash or power loss.
- Separate settings (volume, controls, display) from progress.
- Never trust save files for anything security-relevant in online games; validate on the server.
- On web, local storage can be cleared by the user or browser; tell players if progress is local only.

## Procedural generation and AI behaviour

- **Procedural content** multiplies replay value but is hard to make interesting. Start from hand-made pieces combined procedurally (rooms, chunks, wave templates) before generating from pure noise; it keeps quality controllable.
- Always generate from a **seed** and make the seed visible in debug builds, so a bad level can be reproduced and fixed.
- Add **validation passes**: is the exit reachable, is the difficulty within bounds, are required items placed? Regenerate or repair on failure.
- **Enemy AI** in most games is a state machine or behaviour tree plus a few readable tells, not sophisticated planning. Players need to read and anticipate behaviour; telegraph attacks, and prefer predictable-but-interesting over clever-but-opaque.
- Pathfinding: grid A* or the engine's navigation mesh. Recompute paths at a throttled rate, not every frame for every agent.
- Difficulty comes from combinations (two simple enemies together) more cheaply than from complex individual enemies.

## Playtesting

- Watch people play without helping. Note where they hesitate, die, get bored or misunderstand. What they *do* matters more than what they *say*.
- Test with people who are not the developer early and often; developers are experts in their own game and blind to its difficulty.
- Ask open questions afterwards ("What were you trying to do there?") rather than leading ones.
- Instrument key moments locally (deaths per level, time per level, quits) when there are enough testers for numbers to mean something.
- Fix confusion before adding content; fix unfair deaths before adjusting difficulty.

## Performance

- Set a target (e.g. stable 60 fps on a named minimum device) and measure against it on that device, not only on the development machine.
- **Profile before optimising.** Use the engine profiler or browser performance tools to see whether time goes to scripts, physics, rendering or garbage collection.
- Common fixes: fewer draw calls (atlases, batching, instancing), pooling to stop GC spikes, spatial partitioning for collisions, culling off-screen objects, level-of-detail, lower-resolution effects, avoiding per-frame allocations in hot loops, moving heavy work off the main thread where the platform allows.
- Look at **frame time consistency** (spikes, hitches), not only average fps. A steady 45 can feel better than a 60 that stutters.
- Load times matter: async loading with progress, streaming large worlds, and compressed assets.
- See `performance-optimization` for general method.

## Testing and debugging

- Debug overlays (collision shapes, state names, fps, entity counts) toggleable by a key are worth building early.
- Unit test pure logic: damage formulas, inventory, procedural generation (with fixed seeds), save migration.
- Seeded randomness makes bugs reproducible; log the seed.
- For fixed-step deterministic games, input recording and replay is an excellent regression tool.
- Automated smoke test: boot the game, load each level, run N frames headless if the engine supports it, assert no errors.
- Test on real target hardware and input devices before calling anything done.

## Pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Game speed varies by machine/monitor | Missing `dt` or frame-locked logic | Multiply by `dt`; fixed step for simulation |
| Jittery movement | Mixing fixed physics with per-frame rendering without interpolation; sub-pixel camera in pixel art | Interpolate; snap camera; move physics bodies only in the physics step |
| Objects pass through walls | Tunnelling | CCD, raycasts, smaller steps, thicker colliders |
| Player gets stuck on tile seams | Box colliders on adjacent tiles | Merge colliders, per-axis resolution, capsule/rounded shapes |
| Controls feel unresponsive | Animation-gated actions, input read only in fixed step, no buffering | Act immediately; buffer input; coyote time |
| Periodic hitches | GC from per-frame allocation, synchronous loading | Pool, preallocate, load asynchronously |
| Months spent, nothing playable | Building engine/tools/architecture before gameplay | Prototype the core loop first with placeholders |
| Feature creep | No written scope; every idea accepted | Keep a "not this game" list; cut to a vertical slice |
| Audio silent in browser | Autoplay policy | Resume audio context on first user gesture |
| UI broken on other screens | Hard-coded resolution | Virtual resolution + anchoring; test aspect ratios |
| Save corruption | Non-atomic writes, unversioned format | Temp file + rename; version and migrate |

## Quality bar and verification

- [ ] The game builds and runs from a clean checkout using documented steps.
- [ ] You actually played it after the last change — including start, win, lose, retry, pause and quit paths. If you cannot run it, say so and give the user exact steps and what to look for.
- [ ] Speed and physics behave the same at different frame rates (test by capping fps low and high).
- [ ] Inputs work on each target device; focus loss does not leave keys stuck.
- [ ] Every core action has visible and audible feedback.
- [ ] Someone other than the developer played it and the main confusions were addressed.
- [ ] Performance meets the stated target on the minimum target device, with no recurring hitches.
- [ ] Saves survive quitting mid-session; old saves load after an update.
- [ ] All third-party assets have recorded licences; no placeholder assets remain unintentionally.
- [ ] Accessibility basics present where they apply: remapping, text size, reduced motion/flash, subtitles.

## Safety and ethics

- Seizure risk: avoid rapid full-screen flashing (a common guideline is no more than three flashes per second) and offer reduced-flash options.
- If the game collects data, uses online features, or targets children, privacy law and platform rules apply (for example children's privacy regulations in many jurisdictions); flag this to the user rather than designing around it silently.
- Monetisation mechanics that resemble gambling (paid random rewards) are regulated in some jurisdictions and require disclosure on many platforms.

## Depth on demand

- `references/multiplayer-orientation.md` — read when a game needs online or local multiplayer, before choosing an architecture.
