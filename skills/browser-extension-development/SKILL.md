---
name: browser-extension-development
description: >-
  Design, build, test and publish browser extensions (Chrome, Edge, Firefox,
  Safari and other WebExtensions-based browsers): manifest and permissions,
  background service workers, content scripts, popups, side panels and options
  pages, message passing, storage, cross-browser differences, store review and
  extension security. Use when someone asks to make a browser extension, add-on
  or plugin, a Chrome/Firefox extension, a content script that modifies pages,
  a toolbar popup, migrate to Manifest V3, fix an extension that stopped working,
  or get an extension through store review.
metadata:
  category: app-generation
  related: frontend-development, secure-coding, interaction-design, end-to-end-testing, release-management, web-scraping, browser-automation, project-scaffolding
---

# Browser Extension Development

A browser extension is a small distributed system that lives inside someone else's application. It has several isolated execution contexts that cannot share memory, a background process the browser may kill at any moment, code injected into pages it does not control, and a permission model that users and store reviewers scrutinise. Most extension bugs come from forgetting one of those facts. This skill is about building extensions that work reliably across those boundaries, ask for as little power as possible, and pass review.

## Scope

Covers: WebExtensions-style extensions (the shared model used by Chromium browsers, Firefox and, with adaptations, Safari), Manifest V3 as the current baseline, architecture, messaging, storage, permissions, cross-browser packaging, testing, store submission and security.

Does not cover: the UI design of the popup itself (see `interaction-design`, `ui-design-fundamentals`), general frontend framework practice (`frontend-development`), automating a browser from outside (`browser-automation`), or extracting data from sites at scale (`web-scraping` — and note that an extension scraping on the user's behalf still inherits that skill's legal and ethical concerns).

## Core principles

1. **Each context is a separate program.** The background worker, each content script instance, the popup, the options page and any extension pages run in different JavaScript realms. They communicate only by messages and shared storage. Design the extension as cooperating processes with an explicit protocol, not as one app with globals. Why: a global set in the popup is gone when the popup closes; a variable in the service worker is gone when it is suspended.

2. **The background is ephemeral.** In Manifest V3 the background is a service worker (an event page in some Firefox configurations) that the browser terminates after a short idle period and restarts on the next event. Any in-memory state can vanish between two events. Persist state you need in `storage`, register listeners synchronously at the top level, and treat each event handler as if it were a fresh start. Why: listeners registered asynchronously (after an `await`) may not be attached when the browser wakes the worker to deliver an event, so the event is silently dropped.

3. **Least privilege is a feature, not a chore.** Every permission broadens what an attacker gets if your extension or its dependencies are compromised, increases install-time warnings (which cut install rates), and lengthens review. Prefer `activeTab` and optional permissions requested at the moment of need over blanket host access. Why: users and reviewers read "Read and change all your data on all websites" as a red flag, correctly.

4. **Pages are hostile territory.** Content scripts run alongside arbitrary page code. The page can read and alter the DOM you inject into, spoof events, and send you crafted messages via `window.postMessage`. Never trust data from the page, never pass privileged capabilities into it, and validate every message's sender.

5. **The store is part of the runtime.** Store policies (single purpose, data disclosure, remote code bans, permission justification) constrain architecture. Discover them before designing, not after rejection. Why: "load logic from my server" is a reasonable web pattern and a review failure for extensions.

6. **The browser APIs are the platform; frameworks are optional.** Many good extensions are a few hundred lines of plain scripts. Reach for a bundler or UI framework when the popup or options UI is genuinely complex or the team already uses one — not by default.

## Architecture: the parts and what each is for

| Part | Lives | Can do | Cannot do | Use it for |
|---|---|---|---|---|
| Manifest | `manifest.json` | Declares everything: permissions, entry points, icons, matches, CSP | Run code | The contract with the browser and the store |
| Background service worker | One per extension, ephemeral | Most `chrome.*`/`browser.*` APIs, network, alarms, context menus, cross-tab coordination | Touch the DOM; hold state across suspension; use `window` | Central coordinator, event handling, API calls, privileged work |
| Content scripts | Injected into matching pages, one instance per frame | Read/modify page DOM, a limited subset of extension APIs (messaging, storage, i18n) | Access page JS variables directly (isolated world); call most privileged APIs | Reading or changing pages |
| Popup | Opens from toolbar action; destroyed when closed | Full extension APIs, DOM of its own page | Persist anything in memory after closing | Quick interactions, status, toggles |
| Side panel / sidebar | Persistent panel (browser-dependent) | Like an extension page, survives navigation | Exist on every browser in the same form | Long-lived tools alongside browsing |
| Options page | Extension page | Full extension APIs | — | Settings that change rarely |
| Offscreen document (Chromium) | Hidden extension page created on demand | DOM APIs (audio, clipboard, DOM parsing) the worker lacks | Be permanent; be used for arbitrary reasons | Work that needs a DOM but not a visible page |
| Injected page-world script | Page's own JS realm | See and patch page variables | Use extension APIs; be trusted | Only when you must interact with page JS — minimise it |

**Isolated vs main world.** Content scripts run in an isolated world: they share the DOM with the page but not the JavaScript globals. If you need to read a page variable or hook a page function, you must inject into the main world (via `scripting.executeScript` with a world option where supported, or a `<script>` element), and that code has no extension privileges and is visible to the page. Bridge the two with DOM events or `postMessage`, and validate on the isolated side.

## Process

### 1. Pin down the job and the minimum capability

Before writing a manifest, write one sentence: "When the user does X on Y pages, the extension does Z." Then derive the minimum capability:

- **Which pages?** All sites, a known list of domains, or only the page the user is on when they click? "Only when clicked" means `activeTab` and no host permissions.
- **Triggered how?** Toolbar click, context menu, keyboard command, page load, a schedule? Page-load triggers require declared content scripts or host permissions; user-gesture triggers can often use `activeTab`.
- **What data leaves the browser?** None, to your server, to a third party? This decides privacy disclosures and possibly the whole design.
- **Which browsers?** Chromium only, plus Firefox, plus Safari? Safari requires an Xcode/macOS packaging step and a developer account; confirm before promising it.

Ask the user when these are unclear — they change the permission set, which changes the warning users see.

### 2. Discover context

If extending an existing extension:

- Read `manifest.json` first: manifest version, permissions, host permissions, content script matches, background type, CSP, `browser_specific_settings`.
- Find the build: is the manifest generated (by a bundler plugin or framework) or hand-written? Edit the source of truth, not the build output.
- Identify the message protocol already in use (message `type` names, a router, a typed schema) and extend it rather than adding a parallel one.
- Check storage keys and any migration logic; changing a key shape without migration breaks existing users.
- Look for a polyfill or wrapper (`browser` namespace polyfill, a project-specific API wrapper) and use it consistently.

### 3. Choose the shape

Decide the minimum set of contexts. Common shapes:

- **Action-only:** popup + `activeTab` + `scripting.executeScript` on click. No background at all, or a trivial one. Smallest permission footprint; great for "do something to this page".
- **Page enhancer:** declared content scripts on specific matches, little or no background. Good for "always tweak site X".
- **Coordinator:** background worker owns state, network and API calls; content scripts and UI are thin clients that message it. Good when multiple tabs share state or when calls need credentials.
- **Request modifier:** declarative network rules (`declarativeNetRequest` in Chromium MV3; Firefox also retains blocking `webRequest`). Prefer declarative rules — they are faster, need fewer permissions and are what MV3 expects.

### 4. Write the manifest deliberately

- Start from the smallest permission set and add only with a stated reason. Keep a short note (in the repo or PR) of why each permission exists — reviewers ask, and future you will forget.
- Put rarely needed permissions in `optional_permissions` / `optional_host_permissions` and request them from a user gesture when the feature is first used.
- Scope content script `matches` as narrowly as the job allows. `<all_urls>` is a decision to defend, not a default.
- Set `run_at` intentionally: `document_idle` (default, safest), `document_end`, or `document_start` (only when you must act before page scripts, and then expect a partially built DOM).
- Consider `all_frames` explicitly: iframes are where many "works on some pages" bugs live.
- Declare `web_accessible_resources` only for resources pages genuinely need, with `matches` restricted; these resources let sites fingerprint that your extension is installed.
- Do not loosen the extension CSP to allow remote scripts or `eval`; MV3 forbids remote code and stores reject it.

### 5. Design the message protocol

Treat messages like a small API:

- Every message has a `type` (or equivalent discriminator) and a payload with a known shape. Validate shape on receipt.
- Decide request/response vs fire-and-forget per message. For responses, either return a Promise from the listener (where the browser supports it) or call `sendResponse` and return `true` to keep the channel open. Mixing these is a classic source of `undefined` responses.
- Check `sender`: for messages from content scripts, `sender.tab` and `sender.url`/`origin` tell you which page asked. For external messages (`externally_connectable`), allow-list origins and extension IDs.
- Use long-lived ports (`runtime.connect`) for streams or chatty exchanges; use one-off messages otherwise. Ports also keep a worker alive while open in some browsers, which is useful and also a way to accidentally burn resources.
- Handle "receiving end does not exist": the content script may not be injected yet (tab loaded before install, restricted page, wrong frame). Catch this, and inject on demand if appropriate.

### 6. Design storage

| Store | Scope | Survives | Typical use | Watch out for |
|---|---|---|---|---|
| `storage.local` | Device | Restarts, worker suspension | Caches, larger data, state | Quotas (generous but finite; `unlimitedStorage` if justified) |
| `storage.sync` | User's signed-in browsers | Across devices | Small preferences | Tight per-item and total quotas, write-rate limits; never secrets |
| `storage.session` | Browser session, memory-backed | Worker suspension, not restart | Ephemeral state the worker needs between events, tokens you do not want on disk | Not exposed to content scripts by default; small quota |
| `storage.managed` | Set by enterprise policy | — | Admin-configured settings | Read-only |
| IndexedDB (extension origin) | Device | Restarts | Large structured data | Not reachable from content scripts' extension origin directly — go via messages |
| `localStorage` | Extension page origin | Restarts | Avoid | Unavailable in service workers; synchronous |

Rules: version your stored schema (`schemaVersion` key) and migrate on `runtime.onInstalled` with reason `update`. Use `storage.onChanged` to keep UIs in sync instead of polling. Batch writes; `storage.sync` especially throttles.

### 7. Build the background for suspension

- Register every event listener synchronously at module top level.
- Treat in-memory variables as a cache over `storage`, never the source of truth.
- Use `alarms` instead of `setInterval`/long `setTimeout` for anything beyond seconds; timers die with the worker. Alarms have a minimum period (around 30 seconds in current Chromium; check the browser's docs).
- Keep handlers short. Long-running work (large fetches, processing) should be resumable: persist progress so a killed worker can continue.
- Avoid keep-alive hacks (pinging yourself to stay awake). They waste battery, are fragile across versions, and can draw review attention. If you truly need sustained work, consider an offscreen document for its specific allowed reason, or move the work to a server.

### 8. Write content scripts defensively

- Assume the DOM changes. Single-page apps re-render; use a `MutationObserver` scoped to the smallest relevant subtree, debounce work, and disconnect when done.
- Guard against double injection (a marker attribute or a module-level flag) — scripts can be injected both by manifest and by `executeScript`.
- Isolate your UI from page CSS. Injected UI inherits page styles; a Shadow DOM root, or an iframe pointing at an extension page, prevents collisions in both directions. Iframes give stronger isolation and full extension APIs but cost more.
- Never use `innerHTML` with data from the page or a server; build nodes or use a sanitiser. The extension's privileges make XSS in a content script or extension page worse than ordinary site XSS.
- Prefix any classes, attributes, custom events or global names you add to avoid collisions with the page and other extensions.

### 9. Cross-browser compatibility

See `references/cross-browser-matrix.md` for a detailed list. Headline points:

- Firefox exposes `browser.*` with Promises; Chromium exposes `chrome.*` (Promises now supported for most MV3 APIs). A small polyfill or wrapper hides the difference.
- Background declaration differs: Chromium uses `background.service_worker`; Firefox has historically used `background.scripts` (event page). One manifest can carry both keys for many cases, but test on each browser.
- Firefox needs `browser_specific_settings.gecko.id` for signing and storage persistence in many workflows.
- Feature gaps: `declarativeNetRequest` capabilities, side panel vs sidebar, offscreen documents, `storage.session` access levels and `world: "MAIN"` support differ. Feature-detect (`if (chrome.sidePanel)`) rather than browser-sniff.
- Safari extensions are WebExtensions wrapped in a native app; conversion tooling exists but requires macOS and Xcode, and some APIs are absent or behave differently.

Decide early whether cross-browser support is a requirement. If it is, build and test on every target from the first week; retrofitting is expensive because architectural assumptions (offscreen documents, side panels) do not port.

### 10. Test

- **Load unpacked** in each target browser and exercise every entry point. Use the extension's own devtools: inspect the service worker, the popup (right-click → inspect), and the page console for content scripts (select the extension's context in the console dropdown).
- **Test suspension:** stop the service worker manually from the browser's extension management/debugging page, then trigger events. If behaviour changes, you have in-memory state.
- **Test install and update paths:** fresh install, update from the previous version with existing storage, and tabs that were open before install (content scripts are not auto-injected into them in Chromium).
- **Test restricted pages:** browser internal pages, store pages, PDF viewers, `file://` URLs (need user opt-in) and pages with strict CSP. Your extension should fail gracefully there.
- **Unit test** pure logic (parsers, message routers, storage migration) with a normal test runner and mocked extension APIs.
- **End-to-end:** automation tools such as Playwright or Puppeteer can load an unpacked extension in Chromium (usually requiring a headed or new-headless mode); Firefox has its own tooling (e.g. `web-ext run`). See `end-to-end-testing`.
- **Lint the package:** `web-ext lint` for Firefox catches manifest and policy issues; Chromium browsers surface manifest errors on load.

### 11. Package and publish

- Build a clean, reproducible zip: no source maps with secrets, no `.env`, no tests, no stray files. Many stores require readable (non-obfuscated) code; minification is generally allowed, obfuscation is not. Firefox may ask for source code and build instructions if you ship bundled output.
- Write the listing honestly: single purpose stated plainly, every permission justified in the review form, privacy practices declared accurately, a privacy policy if you handle any user data.
- Prepare screenshots that show the actual extension.
- Expect review latency from hours to weeks; broad host permissions and sensitive APIs lengthen it. Plan releases accordingly and do not promise a ship date tied to approval.
- Use staged/percentage rollouts where the store offers them. Extensions auto-update silently; a bad release reaches every user quickly.
- Bump `version` monotonically; stores reject reused versions.

See `references/store-review-checklist.md` before the first submission and before any release that changes permissions.

## Decision guidance

### `activeTab` vs host permissions

Choose **`activeTab`** when the extension acts only after an explicit user gesture (toolbar click, context menu, keyboard shortcut) on the current tab. No install warning for site access, temporary access, simplest review.

Choose **specific host permissions** when the extension must act automatically on page load on known sites, or make cross-origin requests to specific APIs from the background.

Choose **broad host permissions** only when the core purpose genuinely requires every site (e.g. an ad blocker, a universal accessibility tool), and expect heavier review. Even then, consider making broad access optional and letting the user grant it per site; Chromium users can already restrict site access manually, so your extension must cope with partial grants anyway.

### Declared vs programmatic content scripts

- **Declared** (`content_scripts` in manifest): always run on matches; simplest; requires host permissions for those matches.
- **Programmatic** (`scripting.executeScript`): run on demand; pairs with `activeTab`; can target a specific frame; must handle "already injected".
- **Dynamically registered** (`scripting.registerContentScripts`): register matches at runtime after the user grants a site — the right tool for "enable on this site" features.

### Where to call third-party APIs

- From the **background**, if the call needs credentials, must avoid page CORS, or must not be visible to the page. Note that content-script fetches are subject to the page's origin in modern Chromium; route cross-origin calls through the background.
- From **extension pages** (popup/options) for user-initiated calls whose results display there.
- **Never** from page-world injected code with secrets.

### Framework or plain scripts

| Signal | Lean plain | Lean framework/bundler |
|---|---|---|
| Popup UI | A few controls | Multi-view, forms, complex state |
| Code size | Hundreds of lines | Thousands, shared modules across contexts |
| Team | Solo, quick utility | Team with an established stack |
| TypeScript wanted | Possible with `tsc` alone | Bundler simplifies multi-entry builds |
| Cross-browser builds | One manifest works | Per-browser manifest generation needed |

Extension-specific build tooling (several exist) can generate manifests, handle hot reload and multi-browser output. They save time on medium-to-large projects and add a dependency whose upgrade cycle you inherit; pick one only if its trade-offs suit the project and verify it is maintained.

## Worked example: "summarise the selected text"

Request: "An extension where I highlight text on any page, right-click, and get a summary from our API."

Reasoning through the minimum capability:

1. Trigger is a user gesture (context menu) on the current tab → `contextMenus` + `activeTab`. No host permissions for pages are needed, so no "all websites" warning.
2. The selected text arrives in the context-menu click event (`info.selectionText`), so no content script is needed just to read it. A content script (injected on click via `scripting`) is needed only if the result should be shown inline on the page; otherwise show it in a popup, side panel or notification.
3. The API call needs authentication. The key must not ship in the extension. → The background calls the team's API with a per-user token obtained via a sign-in flow; the API holds the provider key. Host permission is needed only for the team's API origin.
4. State: the last summary might need to survive the worker being killed between the click and the popup opening → write it to `storage.session`.
5. Data disclosure: selected page text is sent to a server → the listing and privacy policy must say so.

Resulting permissions: `contextMenus`, `activeTab`, `scripting` (only if inline display), `storage`, and host permission for one API origin. Compare with the naive version — `<all_urls>` content script listening for selection on every page — which costs a scary warning, runs code on every page load, and gains nothing.

## Migrating from Manifest V2 to V3

Treat migration as a re-architecture of the background, not a find-and-replace.

1. **Inventory** every background global, timer, `webRequest` blocking listener, `chrome.extension.getBackgroundPage()` call, remote script and `eval`. Each is a migration item.
2. **Background page → service worker.** Remove DOM usage (move it to an offscreen document or a content script), replace globals with storage, replace timers with alarms, move listeners to top level.
3. **Blocking `webRequest` → `declarativeNetRequest`** in Chromium. Express rules declaratively (static rulesets in the package, dynamic/session rules at runtime). Some dynamic behaviours (inspecting bodies, arbitrary per-request logic) cannot be expressed; decide what to drop and tell the user. Firefox still supports blocking `webRequest`, so a cross-browser extension may keep two code paths behind feature detection.
4. **`browser_action`/`page_action` → `action`.** Update API calls accordingly.
5. **Host permissions** move from `permissions` to `host_permissions`. Re-check whether each is still needed.
6. **Remote code and `eval`** must go. Bundle libraries; replace templating that uses `new Function` with one that does not.
7. **`executeScript` and `insertCSS`** move to the `scripting` API with different signatures.
8. **Test upgrade in place** with real stored data from the old version before publishing.

## Performance and footprint

Users notice extensions that slow every page. Keep content-script cost near zero on pages where the extension has nothing to do:

- Inject the smallest possible bootstrap; lazy-load heavier modules (via dynamic `import` of a web-accessible module, or by messaging the background) only when needed.
- Prefer `document_idle` unless you must run earlier.
- Scope `MutationObserver` to a subtree, observe only needed mutation types, and batch work in `requestAnimationFrame` or an idle callback.
- Avoid synchronous layout reads in loops (`offsetHeight`, `getBoundingClientRect`) interleaved with writes.
- In the background, avoid waking the worker needlessly: frequent alarms and chatty ports keep it hot.
- Measure with the browser's performance tools on a heavy real page with and without the extension (see `web-performance-audit`).

## Authentication patterns

- **No auth** is best if the feature can work locally.
- **Piggy-back on the site's session** (content script acting in a page the user is already logged into) is acceptable when the extension is a companion to that site, but you inherit fragility whenever the site changes, and you must never exfiltrate session cookies.
- **Your own backend** with user sign-in: use the browser's identity/web-auth-flow API to run OAuth (with PKCE) in a browser-managed window; store tokens in `storage.session` (memory) or `storage.local`; refresh in the background; handle revocation.
- **Never** ship long-lived shared API keys in the package. If the user insists on a bring-your-own-key design (the user pastes their own key into options), store it in `storage.local`, never `sync`, never log it, and only send it to the one API it belongs to.

## Internationalisation and accessibility

- Use the extension i18n mechanism (`_locales/<lang>/messages.json` with `__MSG_name__` in the manifest) if the listing or UI will ever be localised; retrofitting is tedious.
- Popups and options pages are web pages: they need keyboard operability, focus management on open, labels and sufficient contrast (`accessible-design`). Injected UI must not trap focus or break the host page's keyboard navigation.
- Respect the user's colour scheme where the UI shows it (`prefers-color-scheme`), consistent with the project's design if it has one.

## Security

- **No remote code.** Ship all executable code in the package. Fetching configuration or data is fine; fetching and executing scripts is not (and is a store violation in MV3).
- **Secrets.** Anything shipped in the extension is public — anyone can unzip it. Never embed API keys that grant meaningful access; put a server in front of the API and authenticate users to it. For user OAuth, use the browser's identity API flow where available and store tokens in `storage.session` or `storage.local`, never `sync`.
- **Validate senders and inputs** for every message, especially `runtime.onMessageExternal` and anything bridged from the page world.
- **Avoid dangerous sinks** in extension pages and content scripts: `innerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, `setTimeout` with strings.
- **Do not leak capability to the page.** Do not expose a generic "fetch this URL for me" or "run this API" message that a page can trigger; that turns your extension into a confused deputy with the user's cookies and your permissions.
- **Minimise `web_accessible_resources`** and use the option to randomise or restrict their URLs where supported.
- **Dependencies.** Supply-chain compromise of an extension reaches every user's browser with your permissions. Pin versions, keep the dependency tree small, review updates (see `dependency-management`).
- **Developer account security.** Store accounts are high-value targets; extension takeovers via phished developer accounts are a known attack. Recommend strong 2FA on the publishing account and restrict who can publish.
- **Data handling.** Collect only what the single purpose needs; disclose it; do not sell or repurpose browsing data. Browsing history and page contents are sensitive personal data in most jurisdictions.

## Pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| Works right after load, breaks after a minute | Service worker suspended; in-memory state lost or listener registered late | Persist to storage; register listeners at top level |
| `sendResponse` arrives as `undefined` | Listener did async work without returning `true` (or a Promise) | Return `true` / return the Promise; use one style consistently |
| "Could not establish connection. Receiving end does not exist." | Content script not in that tab/frame (pre-install tab, restricted page, wrong frame) | Catch it; inject on demand; target the correct frame |
| Works on some pages, not others | Iframes, SPA navigation (no page load), strict CSP, shadow DOM in the page | `all_frames`, observe history/URL changes, avoid inline scripts, query into open shadow roots if needed |
| Injected UI looks broken | Page CSS bleeding in | Shadow DOM or iframe isolation |
| Popup loses state | Popup is destroyed on close | Persist on change; restore on open |
| Store rejection: "excessive permissions" | Permissions not tied to stated features | Remove, make optional, or justify each one concretely |
| Store rejection: remote code / obfuscation | Loading scripts from a CDN, eval, obfuscated bundle | Bundle everything; turn off obfuscation; provide sources |
| Extension slows down pages | Heavy work on every page, unscoped `MutationObserver`, `<all_urls>` with `document_start` | Narrow matches, debounce, defer work, measure |
| Settings vanish for Firefox users | No stable add-on ID | Set `browser_specific_settings.gecko.id` |
| Update broke existing users | Storage shape changed without migration | Version and migrate in `onInstalled` |

## Quality bar and verification

Before calling an extension done:

- [ ] The extension loads without manifest errors or warnings in every target browser.
- [ ] Each permission has a written justification tied to a user-visible feature; nothing is requested "just in case".
- [ ] All entry points (action, popup, context menu, commands, content scripts, options) were exercised by actually loading the extension, not just reading code.
- [ ] Behaviour survives a forced service-worker stop and a browser restart.
- [ ] Fresh install, upgrade-with-existing-data and uninstall/reinstall were tested.
- [ ] Restricted and unusual pages (internal pages, iframes, SPAs, strict-CSP sites) fail gracefully.
- [ ] No secrets in the package; `grep` the built zip for keys and tokens.
- [ ] No `eval`-like sinks or `innerHTML` with untrusted data; external messages validated.
- [ ] Listing text, privacy disclosure and the actual data flow agree.
- [ ] The package is built from a clean checkout by a documented command.

If you cannot run a browser in your environment, say so explicitly, give the user exact steps to load the unpacked extension and what to check, and do not claim it was tested.

## Depth on demand

- `references/cross-browser-matrix.md` — read when targeting more than one browser engine or porting an existing extension.
- `references/store-review-checklist.md` — read before first submission, before any release that adds permissions, or after a rejection.
