---
name: mobile-app-development
description: >-
  Build mobile applications for iOS and Android: choose native vs
  cross-platform by constraints, follow each platform's navigation and
  interaction conventions, design for offline use and data sync, request
  permissions in context, implement push notifications, manage performance,
  battery and app size, meet app store review and privacy requirements, and
  test on real devices. Use when asked to build, extend or ship a phone or
  tablet app, choose between Swift/Kotlin and cross-platform frameworks
  (e.g. React Native, Flutter), add offline mode, push, deep links or in-app
  purchases, or prepare an app for store submission. Not for mobile-friendly
  websites (website-and-landing-pages, layout-and-responsive-design) or the
  backend alone (backend-development, full-stack-app-build).
metadata:
  category: app-generation
  related: full-stack-app-build, frontend-development, api-design, authentication-and-authorization, interaction-design, accessible-design, performance-optimization, testing-strategy, end-to-end-testing, release-management, secure-coding, ci-cd-pipelines
---

# Mobile App Development

## Purpose and scope

This skill covers building and shipping apps that run on phones and tablets: choosing how to build them, structuring them so they feel at home on each platform, making them work when the network does not, handling permissions and notifications correctly, keeping them fast and frugal with battery and data, getting them through store review, and verifying them on real hardware.

The deliverable is an app that **installs, launches, and completes its core jobs on real devices of the target platforms, across the conditions users actually have** — slow or absent networks, small screens, large text settings, interruptions, denied permissions, old OS versions — and that is ready, or clearly documented as not yet ready, for store submission.

Boundaries:

- The server and API the app talks to: `backend-development`, `api-design`, or `full-stack-app-build` for the whole system.
- Responsive websites and progressive web apps viewed in a mobile browser: `website-and-landing-pages`, `frontend-development`, `layout-and-responsive-design` (this skill helps decide whether a PWA is enough).
- Games: `game-development`.
- Visual and interaction design in depth: `interaction-design`, `ui-design-fundamentals`, `accessible-design`.

## Core principles

1. **The device is hostile and the network is optional.** Assume the app can be killed at any moment, backgrounded mid-operation, run on an old phone with little memory, and lose connectivity between two taps. Why: these are normal conditions on mobile, not edge cases; apps built for a developer's fast phone on office Wi-Fi fail for real users.

2. **Respect each platform's conventions.** Navigation, back behaviour, gestures, typography, system controls and permission flows differ between iOS and Android. Why: users carry muscle memory from every other app on their device; violating it makes an app feel broken even when it works. Cross-platform code does not mean identical UI.

3. **Releases are slow and sticky.** Store review takes time, users update late or never, and a shipped binary cannot be patched instantly. Why: this makes backward compatibility of the API, remote configuration, feature flags and careful testing far more important than on the web.

4. **Ask for trust, do not assume it.** Permissions, notifications, tracking and data collection must be requested in context, justified, and degrade gracefully when refused. Why: platforms enforce this, stores reject apps that ignore it, and users who are asked badly say no permanently.

5. **Performance is felt, not measured.** Jank in scrolling, slow start and battery drain are what users notice and review. Why: mobile hardware ranges widely, and perceived responsiveness drives retention and ratings more than features do.

6. **Test on real devices.** Simulators and emulators are essential for speed but miss real performance, sensors, push delivery, camera, permission behaviour, memory pressure and manufacturer quirks. Why: those are exactly where mobile bugs live.

## Process

### 1. Clarify the product and the constraints

Establish (ask where it matters — see `clarify-requirements`):

- **Platforms**: iOS, Android, or both; phones only or tablets too; any wearables, TV or car surfaces.
- **Minimum OS versions**, which determine available APIs. Check the target audience's device mix if data exists; older-device-heavy markets change the answer.
- **Core jobs** and which must work offline.
- **Device capabilities needed**: camera, location (foreground or background), microphone, Bluetooth, NFC, health data, contacts, photos, biometrics, background execution.
- **Notifications**: transactional, reminders, marketing? From the server, scheduled locally, or both?
- **Accounts and auth**: sign-in methods; note that store rules may require offering a platform sign-in option when third-party social sign-in is offered, and require in-app account deletion when account creation is offered — check current guidelines.
- **Monetisation**: free, paid, subscriptions, in-app purchases, ads. Store rules on digital goods purchases significantly constrain the design; check current rules for the target regions.
- **Existing assets**: a web app, a design system, an API, an existing mobile codebase, team skills.
- **Distribution**: public stores, enterprise or managed distribution, internal testing only.

### 2. Discover context

If an app exists, read before writing (see `explore-codebase`): language and framework versions, architecture pattern in use (e.g. MVVM, unidirectional data flow, the framework's recommended pattern), navigation library, state management, networking and persistence layers, dependency manager, build configurations and flavours, signing setup, CI, test suites, analytics and crash reporting, and the minimum OS settings. Follow them. Introducing a second state management or navigation approach into an existing app is a common, expensive mistake.

Check the backend contract: versioning strategy, authentication tokens, pagination, error format, and whether old app versions in the field are still supported.

### 3. Choose the approach

| Approach | Choose when | Costs |
|---|---|---|
| Native per platform (e.g. Swift/SwiftUI or UIKit on iOS; Kotlin/Jetpack Compose or Views on Android) | Deep platform integration, best performance and platform feel, heavy use of new OS features, the team has platform specialists, or only one platform is targeted | Two codebases for two platforms; two skill sets |
| Cross-platform with native UI rendering via a bridge or compiled layer (e.g. React Native) | Team strong in web/JavaScript technologies; shared business logic and much UI across platforms; moderate native integration | Native modules still needed for some features; upgrade churn; platform conventions require deliberate effort |
| Cross-platform with its own rendering engine (e.g. Flutter) | Highly custom, consistent UI across platforms; strong performance needs with one codebase | Platform look-and-feel must be recreated deliberately; native integrations via plugins or channels |
| Shared core logic, native UI (e.g. Kotlin Multiplatform, or a shared library in another language) | Complex business logic must be identical across platforms while UI stays fully native | Build complexity; team needs both platform skills |
| Progressive web app | Content or simple tools; distribution without stores; frequent updates; limited device APIs needed | Restricted background execution, push and device APIs, varying by platform; weaker discoverability in stores |
| Web view wrapper | Rarely; mainly to package an existing responsive web app quickly | Stores may reject thin wrappers that add no app value; feels non-native |

Decision factors, in rough order: team skills and who maintains it; required native capabilities; performance and UI demands; time to market for both platforms; existing code to share. Name the deciding factors in the handover (see `technical-decision-making`). If an app already exists, staying on its approach is almost always right unless there is a specific, stated reason to change.

### 4. Architect the app

Structure the app in layers so the hard parts are testable and replaceable:

- **UI layer**: screens and components; holds no business rules; renders state.
- **State / presentation layer**: view models or equivalent; turns user intent into actions and data into display state; survives configuration changes (rotation, dark mode, process death where the platform restores state).
- **Domain / data layer**: repositories that hide whether data comes from the network, the local database or a cache.
- **Platform services**: wrappers around permissions, notifications, location, camera, secure storage, so they can be faked in tests and on simulators.

Choose the framework's mainstream, documented patterns over clever ones. Handle the app lifecycle explicitly: what happens on launch (cold vs warm), background, foreground, termination and restoration. Long operations must survive or resume across these.

### 5. Navigation per platform

| Concern | iOS conventions (typical) | Android conventions (typical) |
|---|---|---|
| Primary navigation | Tab bar at the bottom for top-level sections; navigation stack within each | Bottom navigation bar or navigation rail/drawer; back stack per destination |
| Back | Back button top-left in the navigation bar; edge swipe to go back | System back gesture/button, which must behave predictably across the whole app; predictive back on newer versions |
| Modals | Sheets for focused tasks, dismissible by swipe down where safe | Dialogs and bottom sheets; full-screen dialogs for complex tasks |
| Actions | Navigation bar buttons, context menus, swipe actions on lists | Top app bar actions, floating action button for a primary action where appropriate, overflow menu |
| Typography and controls | System font and Dynamic Type, system controls | Platform type scale and font scaling, Material components or platform equivalents |

These are tendencies; verify against current platform design guidelines, which evolve. On cross-platform frameworks, use platform-adaptive components or branch where conventions differ — at minimum for back behaviour, modals, date/time pickers, alerts and share sheets.

Also plan:

- **Deep links and app links** (universal links on iOS, app links on Android) from day one if the app will receive links from email, web or notifications. Every deep-linkable screen must cope with being opened cold, logged out, or with a stale or missing resource.
- **State restoration**: returning to the app after the system killed it should restore the user's place where reasonable.
- **Authentication gates**: route logged-out users to sign-in and back to their intended destination afterwards.

### 6. Offline and sync

Decide per feature what offline means:

| Level | Behaviour | Fits |
|---|---|---|
| Online only | Clear message when offline; retry when back | Live data where stale is useless (e.g. live trading, live chat presence) |
| Cache for reading | Show last known data with its age; refresh when online | Feeds, catalogues, reference content |
| Offline writes, queued | User actions saved locally and sent when online; optimistic UI | Notes, forms, field data collection, to-dos |
| Full offline-first with sync | Local database is the source of truth for the UI; bidirectional sync with conflict handling | Field work, collaborative or long-offline use cases |

For anything beyond online-only:

- **Local persistence** in a real database or the platform's persistence framework, not ad-hoc files, for structured data.
- **Write queue** that survives app termination, retries with backoff, and is idempotent on the server (send a client-generated ID per operation so retries do not duplicate).
- **Conflict strategy**, chosen deliberately: last-write-wins (simple, loses data in concurrent edits), field-level merge, server-authoritative with user resolution, or conflict-free data types for collaborative editing. Document which and why.
- **Sync status visible to users**: pending, synced, failed — so they trust that their work is saved.
- **Schema migrations** for the local database across app versions; users skip versions, so migrations must chain.
- **Background sync** using the platform's sanctioned mechanisms, which limit frequency and duration; do not assume your sync will run on a schedule.

### 7. Permissions

- Request **in context**, at the moment the feature needs it, after the user has taken an action that makes the reason obvious. Avoid requesting several permissions at launch.
- Explain value first where helpful with your own screen, then trigger the system prompt; users who decline your explanation have not burned the one-time system prompt.
- Write accurate purpose strings (required on iOS for many permissions; stores review them).
- Request the **least access** that works: approximate rather than precise location, foreground rather than background, selected photos rather than the whole library, where the platform offers it.
- **Handle every outcome**: granted, denied, denied permanently, limited/partial, revoked later in system settings. The app must stay usable; offer a path to settings where the feature is essential.
- Re-check permission state on each use; it can change while the app is backgrounded.
- Background location, health data, contacts and similar sensitive access often receive extra store scrutiny; justify them in the review notes and privacy disclosures.

### 8. Push notifications

- Choose the delivery path: the platform push services (APNs for Apple platforms, FCM commonly for Android and often as a cross-platform layer), directly or through a provider.
- Register for push and request notification permission **after** the user understands why (e.g. after they create something they would want updates on). Newer Android versions require a runtime permission for notifications, like iOS.
- Send device tokens to the backend tied to the user and device; refresh them when they change; remove them on logout and when the push service reports them invalid.
- Use **notification channels/categories** so users can control types separately; respect quiet preferences.
- Make notifications **deep link** to the relevant screen, and handle the app being cold-started from a notification.
- Payloads should not carry sensitive data in clear text where lock-screen display would expose it.
- Delivery is best-effort; never depend on push for correctness. The app must fetch the true state when opened.
- Test on real devices: simulators have limited or no real push support depending on platform and version.

### 9. Networking, auth and security

- Treat the network as unreliable: timeouts, retries with backoff for idempotent requests, cancellation when screens close, and clear error states.
- Version the API and keep old versions working as long as old app versions are in use; consider a minimum-supported-version check that can prompt users to update.
- Store tokens and secrets in the platform's secure storage (Keychain on iOS, Keystore-backed storage on Android), never in plain preferences, logs or the app bundle.
- **Anything in the app binary is extractable.** Do not embed private API keys or secrets; proxy sensitive third-party calls through your backend.
- Use secure transport only; consider certificate pinning only if you have a plan to rotate pins without bricking old versions.
- Authorise on the server; never trust that a request came from your app.
- Use the platform's biometric APIs for local unlock, backed by secure storage, rather than storing a password.
- Strip debug logging, test endpoints and debug menus from release builds.
- See `secure-coding` and `authentication-and-authorization`.

### 10. Performance, battery and size

- **Startup**: defer non-essential initialisation (analytics, SDKs, prefetches) until after the first screen renders; measure cold start on a low-end device.
- **Lists**: use the platform's virtualised list components; avoid heavy work during scroll; size images to their display size; cache images.
- **Main thread**: never block it with disk, network, parsing or heavy computation. Use the platform's concurrency tools (see `concurrency-and-async`).
- **Memory**: release large resources off-screen; handle low-memory warnings; watch image memory.
- **Battery and data**: batch network calls, avoid polling, use push or sanctioned background tasks, use location at the lowest accuracy and frequency that works, respect low-power and data-saver modes.
- **App size**: remove unused assets and dependencies; use platform app-thinning or app-bundle mechanisms; each third-party SDK adds size, startup time and privacy obligations.
- Profile with the platform tools (e.g. Xcode Instruments, Android Studio profilers) on real devices. See `performance-optimization`.

### 11. Accessibility and adaptability

- Support system text scaling (Dynamic Type, font scale) without truncation or overlap; test at the largest sizes.
- Every interactive element has an accessible label, role and state for VoiceOver and TalkBack; images that convey meaning have descriptions.
- Touch targets meet platform minimums (roughly 44 pt on iOS, 48 dp on Android).
- Contrast sufficient in light and dark modes; do not convey meaning by colour alone.
- Respect reduced motion settings.
- Support both orientations unless there is a reason not to; handle notches, rounded corners, dynamic islands, foldables and split-screen by respecting safe areas and window size classes.
- Localise: externalise strings, support plural rules, right-to-left layouts, locale-aware dates, numbers and currencies.
- See `accessible-design` and `accessibility-audit`.

### 12. Visual design

Derive the look from the product's brand and audience, expressed within each platform's conventions. Use the project's design system if one exists (see `design-systems`). Do not impose one platform's design language on the other, and do not apply a default palette or component style; when no direction is given, keep to platform-standard components, which are accessible and familiar, and state that visual design is open.

### 13. Testing

Layer the tests (see `testing-strategy`):

- **Unit tests** for domain logic, view models, sync and conflict resolution, date/time and money handling.
- **Integration tests** for the data layer against a fake or local server, and local database migrations from every previously shipped schema version.
- **UI tests** for the core journeys using the platform's UI testing tools or a cross-platform end-to-end tool (see `end-to-end-testing`).
- **Real-device matrix**: at least the oldest supported OS version, the newest, a small-screen device, a large or tablet device, and a low-end Android device. Include at least one non-reference Android manufacturer if Android is a target.
- **Condition tests**, manual or automated: airplane mode mid-operation, slow network (use network conditioning tools), app killed during a write, permission denied and later revoked, notification tap from a cold start, deep link while logged out, largest text size, dark mode, screen reader on, rotation, low storage, system language with long words and right-to-left script.
- **Beta distribution** through the platforms' testing channels (e.g. TestFlight, Play Console testing tracks) to real users before release.

If you can build and run apps in a simulator or emulator, do so after each feature and drive the core journey. State plainly what was tested on simulators only and what needs a real device.

### 14. Store readiness

Requirements change; check the current official guidelines for each store before submission. Typical areas:

- **Metadata**: name, description, keywords, category, age rating questionnaire, screenshots for required device sizes, support URL, privacy policy URL.
- **Privacy disclosures**: data collected, its purposes, whether linked to the user or used for tracking — including data collected by third-party SDKs. Platform-specific declarations (e.g. privacy manifests, data safety forms) must match what the app and its SDKs actually do.
- **Tracking consent** where the platform requires an explicit prompt before cross-app tracking.
- **Account deletion** offered in-app when account creation is.
- **Purchases of digital goods** through the platform's in-app purchase system where required by the rules for that region and category.
- **Permissions and background modes** justified and actually used.
- **Target API level / SDK requirements** that stores raise over time.
- **Review notes and a demo account** for reviewers if features are behind login — use a dedicated review account, never a real user's credentials.
- **Signing**: certificates, provisioning profiles and keystores managed securely; the Android upload/signing key backed up, because losing it can block future updates.

Plan releases with staged rollouts, crash monitoring and a way to disable features remotely (see `release-management`, `observability`). Automate builds and signing in CI where possible (see `ci-cd-pipelines`), keeping signing secrets in the CI secret store.

### 15. Observe and maintain

- **Crash and error reporting** in release builds, with symbol files (dSYMs, mapping files) uploaded so stack traces are readable. Scrub personal data from reports.
- **Product analytics** limited to the events that answer real questions, declared in privacy disclosures, and respecting consent.
- **Remote configuration and feature flags** to disable a broken feature without a release; use them sparingly and remove stale flags.
- **Minimum version enforcement**: a server-driven check that can ask users of a dangerously old build to update.
- **OS release cadence**: each major OS release can change permissions, background limits and UI behaviour. Test against beta OS versions before they ship and budget yearly upgrade work for SDK and target-level requirements.
- **Dependency hygiene**: cross-platform frameworks and plugins move fast; upgrade in small steps rather than in one painful jump years later (see `dependency-management`).

## Decision guidance

### In-app purchases and subscriptions

- Decide early whether purchases are of digital goods consumed in the app (usually subject to the store's payment system under current rules, with regional exceptions) or physical goods and real-world services (usually allowed to use other payment methods). Check current rules for the specific category and region; they have changed repeatedly and differ by store.
- Validate purchases and subscription state **on your server** using the stores' server APIs and notifications, not only on the device.
- Handle the full lifecycle: trials, renewals, grace periods, billing retry, refunds, upgrades/downgrades, family sharing where applicable, and restoring purchases on a new device.
- Test with the stores' sandbox or test accounts and their accelerated renewal timelines; never with real payment methods during development.

### Cross-platform app needing native capability

When a cross-platform framework lacks something (a new OS API, a hardware SDK):

1. Look for a maintained, widely used plugin; check its last release, open issues and support for both platforms.
2. If none exists, write a small native module with a narrow interface, and keep platform code isolated.
3. Document the native parts clearly; they are where framework upgrades break.
4. If the app is accumulating many native modules, reconsider whether the cross-platform choice still fits.

### Phone and tablet

Supporting tablets well is more than stretching the phone layout: use adaptive layouts (e.g. list-detail side by side), support multitasking and keyboard/pointer input where the platform expects it. If tablets are not a priority, make sure the phone layout at least does not break on them, since users will install it there anyway.

### Background work

Platforms restrict background execution heavily and differently. Use the sanctioned mechanism for each job type — background fetch or work schedulers for deferrable work, foreground services (Android) or specific background modes (iOS) only when the use case qualifies — and design every background job to be interruptible, resumable and safe to run late or not at all.

### Debug vs. release differences that bite

Release builds behave differently, and bugs that only appear there reach users. Before calling a feature done, run a release-configuration build on a device and check:

- **Code shrinking and obfuscation** (e.g. R8/ProGuard on Android) removing classes used by reflection or serialisation — add keep rules and test.
- **Optimisation-level differences** exposing race conditions hidden in debug.
- **Different API endpoints, keys and push environments** (e.g. sandbox vs production push) configured per build.
- **Entitlements and capabilities** present in the release provisioning profile, not only in development.
- **Network security configuration** that allowed local or insecure endpoints in debug but blocks them in release.
- **Logging and debug menus** stripped as intended.
- **Startup time**, which is often better in release — measure there, not in debug.

## Data and state checklist

Apply to every screen that shows or edits data:

- What does it show while loading, when empty, on error, and when offline with cached data?
- What happens if the user leaves mid-edit — is the draft kept?
- What happens on rotation, split-screen resize, dark-mode switch and process death?
- Is there a double-tap or double-submit risk on its actions?
- Does pull-to-refresh or reopening the app refresh stale data?
- Are timestamps shown in the user's timezone and locale?

## Working without a device or build tools

If you cannot compile or run the app in your environment:

- Keep to APIs you are confident exist at the stated SDK and framework versions, and pin versions in the project files.
- Remember the configuration code does not cover: permission purpose strings, manifest entries, entitlements, capabilities, URL schemes and associated domains files. List each one explicitly for the user, since missing configuration is a frequent cause of crashes on first use.
- Give the user precise build and test steps per platform and a checklist of what to look for, and ask for compiler errors and device logs verbatim.
- Mark the handover clearly as not built or device-tested.

## Worked reasoning

Illustrative only.

**Request:** "An app for our field technicians to record inspections at customer sites, with photos, often in basements without signal. Android tablets issued by the company, some staff use personal iPhones."

- Platforms: Android (managed company tablets, likely managed distribution) and iOS (personal phones, likely public store or business distribution). Tablet and phone layouts both matter.
- Offline: full offline-first for inspections — the core job happens without signal. Local database as source of truth, write queue with client-generated IDs, photo uploads resumable and deferred to Wi-Fi if the user prefers, visible sync status per inspection.
- Conflicts: inspections are usually edited by one technician; last-write-wins per inspection with an audit trail is likely enough — confirm that supervisors never edit simultaneously.
- Approach: team skills decide. If the company has web developers and modest native needs (camera, files), a cross-platform framework fits; if they have platform specialists, native is fine. Camera and background upload are well supported by mainstream plugins in either case — verify before committing.
- Permissions: camera at the first photo, location only if inspections must be geotagged (ask), notifications only for assignment updates.
- Testing: real tablets of the issued model, an older iPhone, airplane-mode inspections end to end, app killed during photo upload, storage nearly full.
- Data: customer addresses and photos of private property are personal data — secure storage, encryption on device via platform defaults, retention rules agreed with the user.

## Pitfalls and anti-patterns

- **"It works on the simulator."** Untested on real hardware: push, camera, performance and permission behaviour differ.
- **Asking for every permission at first launch.** High refusal, store friction, and a feature set crippled by an early "no".
- **Blocking the main thread** with network or disk work, causing jank or "application not responding" dialogs.
- **No offline handling.** Spinners forever, lost form input, duplicate submissions on retry.
- **Non-idempotent retries.** Queued writes that create duplicates when the response was lost but the request succeeded.
- **One platform's UI on the other.** iOS-style back buttons on Android with a broken system back; Android-style menus on iOS.
- **Secrets in the binary.** API keys for paid services or admin endpoints compiled into the app.
- **Breaking old app versions** with a backend change; users on old builds see failures you cannot patch quickly.
- **Unhandled lifecycle.** Losing state on rotation or process death; crashing when restored on a screen whose data is gone.
- **Push as source of truth.** Missed notifications leave the app in the wrong state.
- **Undeclared SDK data collection.** A third-party analytics or ads SDK collecting data the privacy disclosures do not mention — a store rejection and a trust problem.
- **Fixed text sizes and pixel-perfect layouts** that break at large font settings or on small screens.
- **Generated code that does not compile.** Imagined APIs, wrong framework versions, missing native configuration (permissions strings, entitlements, manifest entries). Build after each step.
- **Losing the signing key.** Treat it as critical infrastructure.
- **Ignoring time and locale.** Dates parsed in the device timezone, currencies formatted for one locale, hardcoded English strings concatenated into sentences that cannot be translated.
- **Unbounded caches and logs** that grow until the device runs out of space.
- **Testing only logged-in, happy paths.** Fresh install, logged out, expired session and upgrade-from-previous-version are the paths real users hit first.

## Quality bar and verification

- [ ] The app builds from a clean checkout with documented commands for each platform, in debug and release configuration.
- [ ] Core journeys pass on a real device for each target platform, including the oldest supported OS version.
- [ ] Offline behaviour matches the decided level per feature; no data loss when killed mid-operation; no duplicates on retry.
- [ ] Every permission is requested in context, with accurate purpose text, and every denial path is usable.
- [ ] Push notifications arrive on real devices, deep link correctly from cold start, and tokens are handled on login/logout.
- [ ] Navigation and back behaviour follow each platform's conventions.
- [ ] Largest text size, screen reader, dark mode and rotation checked on the main flows.
- [ ] No secrets in the binary; tokens in secure storage; debug features absent from release builds.
- [ ] Cold start, scrolling and memory checked on a low-end device; no main-thread blocking found in profiling.
- [ ] Privacy disclosures match the app's and SDKs' actual data collection.
- [ ] Store checklist reviewed against current official guidelines; outstanding items listed.
- [ ] The handover states what was verified on real devices, on simulators only, and not at all.

## Safety notes

- Never submit to a store, publish a release, or change production remote configuration without explicit user confirmation.
- Never use real user credentials or personal data for testing or reviewer accounts.
- Keep signing keys, certificates and store credentials out of the repository and logs; store them in a secret manager and back them up.
- Collect the least data needed, disclose it accurately, and secure it on the device and in transit.
- Treat health, location, children's data and payments as regulated areas; flag the implications to the user.

## Related skills

- `full-stack-app-build`, `backend-development`, `api-design` for the server side.
- `authentication-and-authorization`, `secure-coding` for accounts and data protection.
- `interaction-design`, `accessible-design`, `design-systems` for the experience.
- `performance-optimization`, `concurrency-and-async` for responsiveness.
- `testing-strategy`, `end-to-end-testing` for verification.
- `release-management`, `ci-cd-pipelines`, `observability` for shipping and running it.
