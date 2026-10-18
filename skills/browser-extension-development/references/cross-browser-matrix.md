# Cross-browser differences for WebExtensions

Read this when an extension must run on more than one browser engine, or when porting an existing extension. Browser behaviour changes between releases; treat this as a map of *where differences tend to be*, and confirm specifics against each browser's current documentation and by loading the extension.

## Strategy

1. **Decide targets up front.** Chromium-family browsers (Chrome, Edge, Brave, Opera, Vivaldi) share most behaviour. Firefox (Gecko) and Safari (WebKit) are the real second and third platforms.
2. **Feature-detect, do not browser-sniff.** `if (chrome.sidePanel) …` survives browser updates; user-agent checks do not.
3. **Isolate differences** behind a thin module (e.g. `platform.js`) so the rest of the code calls one API.
4. **Generate per-browser manifests** if the differences exceed what one manifest can express. Keep one source manifest plus small per-target overrides merged at build time.
5. **Run on every target in CI or at least before every release.** "It works in Chrome" says nothing about Firefox's event page lifecycle.

## Namespace and Promises

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| Namespace | `chrome.*` | `browser.*` (also `chrome.*` alias) | `browser.*` (and `chrome.*`) |
| Promise-returning APIs | Most MV3 APIs return Promises; some older ones callback-only | Promises throughout | Promises |
| Common approach | Use a `browser` polyfill or a local wrapper | Native | Native |

## Background

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| MV3 background | `background.service_worker` | `background.scripts` (non-persistent event page); service worker support varies by version | Non-persistent background; service worker support varies |
| DOM in background | None (use offscreen document) | Event pages have a DOM | Varies |
| Lifecycle | Terminated after idle (~30 s), extended by active events | Event page unloaded after idle | Aggressive unloading, especially on iOS |

A manifest can often declare both `service_worker` and `scripts`; each browser uses what it supports. Verify this works on the minimum versions you target.

## Network modification

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| `declarativeNetRequest` | Primary mechanism in MV3 | Supported | Supported (subset) |
| Blocking `webRequest` | Not available to regular MV3 extensions (policy-installed exceptions exist) | Still available | Not available |
| Rule limits | Static/dynamic rule quotas | Own limits | Own limits |

## UI surfaces

| Surface | Chromium | Firefox | Safari |
|---|---|---|---|
| Toolbar action + popup | Yes | Yes | Yes |
| Side panel | `sidePanel` API | `sidebar_action` (different API and manifest key) | Not equivalent |
| Context menus | `contextMenus` | `menus` (with `contextMenus` alias) | Supported, subset |
| Keyboard commands | Yes | Yes | Limited |
| Options page | `options_ui` / `options_page` | `options_ui` | Yes |

## Content scripts and scripting

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| `scripting.executeScript` | Yes, with `world: "MAIN"` support | Yes; main-world support depends on version | Yes, check main-world support |
| Cross-origin fetch from content script | Subject to page origin rules — route via background | Has historically allowed more with host permissions; do not rely on it | Restricted |
| Access in pre-existing tabs after install | Not auto-injected | Not auto-injected | Varies |

## Storage

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| `storage.session` | Yes; content-script access off by default (`setAccessLevel`) | Yes in recent versions | Check |
| `storage.sync` | Synced via browser account | Synced via Firefox account | Limited / may behave like local |
| Persistence without stable ID | ID derived from key | Needs `browser_specific_settings.gecko.id` | Tied to app bundle |

## Identity and auth

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| Web auth flow | `identity.launchWebAuthFlow` | `identity.launchWebAuthFlow` | Limited; often use a web page flow |
| Redirect URL | `https://<id>.chromiumapp.org/` | `https://<hash>.extensions.allizom.org/` (via `identity.getRedirectURL()`) | Differs |

Always obtain the redirect URL from `identity.getRedirectURL()` rather than hard-coding it.

## Packaging and distribution

| Topic | Chromium | Firefox | Safari |
|---|---|---|---|
| Package | Zip uploaded to store(s); Edge has its own store | Zip/XPI, signed by Mozilla (listed or self-distributed) | Xcode project wrapping the extension in a native app; distributed via the App Store |
| Required ID | Assigned by store | `gecko.id` recommended/required | Bundle identifier |
| Source review | Readable code expected | May require full source and build steps for bundled code | App Store review applies |
| Dev loading | Load unpacked | `about:debugging` temporary add-on or `web-ext run` | Enable unsigned extensions in developer settings |

## Porting checklist

- [ ] Wrap namespace differences in one module.
- [ ] Confirm background declaration works on every target.
- [ ] Replace or feature-gate APIs missing on any target (side panel, offscreen, DNR features).
- [ ] Add `gecko.id` and minimum version settings for Firefox.
- [ ] Re-test auth redirect URLs per browser.
- [ ] Re-check storage quotas and `sync` behaviour.
- [ ] Load, exercise and force-unload the background on every target.
