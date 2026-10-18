---
name: desktop-app-development
description: >-
  Build and ship desktop applications for Windows, macOS and Linux: choose
  between native toolkits, web-technology shells (e.g. Electron, Tauri) and
  cross-platform UI toolkits (e.g. Qt, .NET MAUI/Avalonia, Flutter desktop)
  by constraints; integrate with the OS (menus, shortcuts, file associations,
  tray, notifications, drag and drop); follow per-OS conventions; handle the
  file system and security boundaries correctly; and package, code-sign,
  notarize and auto-update the app. Use when asked to build a desktop app,
  wrap a web app for the desktop, add installers, signing or auto-update, fix
  "app is damaged / unidentified developer / SmartScreen" warnings, or port a
  desktop app between operating systems. Not for command-line tools
  (cli-development), browser extensions (browser-extension-development), or
  games (game-development).
metadata:
  category: app-generation
  related: full-stack-app-build, frontend-development, secure-coding, interaction-design, accessible-design, performance-optimization, testing-strategy, end-to-end-testing, release-management, ci-cd-pipelines, dependency-management, cli-development
---

# Desktop App Development

## Purpose and scope

This skill covers applications installed and run on personal computers: editors, utilities, productivity tools, clients for online services, creative tools, internal line-of-business apps, and web apps given a desktop presence. The deliverable is an app that **installs cleanly, launches without security warnings, behaves like a good citizen on each target OS, keeps the user's files and data safe, and updates itself reliably** — or a clear statement of which of those are not yet in place.

Boundaries:

- Command-line tools and terminal UIs: `cli-development`.
- Browser extensions: `browser-extension-development`.
- Games: `game-development`.
- The backend for a desktop client: `backend-development`, `api-design`, `full-stack-app-build`.
- UI implementation detail in web technologies: `frontend-development`.

## Core principles

1. **Distribution is half the work.** Building the UI is the familiar part; packaging, signing, notarization, installers, updates and uninstalls are where desktop projects stall. Why: unsigned or badly packaged apps trigger OS security warnings that most users will not click through, and an app that cannot update is stuck with its first bugs forever. Plan distribution on day one, not release week.

2. **Each OS has its own idea of "correct".** Menu placement, keyboard shortcuts, window behaviour, file locations, settings conventions and installers differ between Windows, macOS and Linux. Why: users judge a desktop app by how well it fits their OS; a cross-platform codebase must still produce per-platform behaviour.

3. **The app runs with the user's power.** A desktop app can read the user's files, run programs and talk to the network. Why: any vulnerability — especially in web-technology shells that render remote or untrusted content — becomes code execution on the user's machine. Least privilege and strict boundaries are essential.

4. **Choose the technology by constraints.** Team skills, performance and footprint, native integration depth, platforms targeted, and whether a web app already exists decide the stack. Why: every choice has a real cost profile (bundle size, memory, native feel, development speed), and no option wins on all of them.

5. **User data is sacred.** Documents, settings and caches belong in the right places, are written safely, and survive crashes, updates and uninstall/reinstall as the user would expect. Why: losing or corrupting a user's file is the one failure they never forgive.

6. **Test on each real OS.** Behaviour differs across OS versions, CPU architectures, display scaling, file systems and security software. Why: "works on my machine" is a more literal problem on the desktop than anywhere else.

## Process

### 1. Clarify the product and constraints

- **Target OSes and versions**, and CPU architectures (x64, ARM64 on Windows and macOS; Linux distributions and packaging formats).
- **Core jobs** and whether they involve documents (open/save files), background work (sync, monitoring), system integration (tray, startup, global shortcuts, file associations, protocol handlers) or hardware.
- **Online or offline**: does it need a server? Does it work without the network?
- **Existing assets**: a web app or design system to reuse, an existing desktop codebase, team skills.
- **Distribution**: public download, platform app stores, enterprise deployment (managed installs, group policy, MDM), internal only.
- **Update policy**: automatic, prompted, or managed by IT.
- **Performance and footprint expectations**: always-running utility vs. occasionally-opened heavy tool.
- **Security and compliance context**: handling sensitive files, enterprise security software, offline/air-gapped use.

### 2. Discover context

For an existing app (see `explore-codebase`): framework and version, how the main/UI processes are split, how native code is called, build and packaging tooling, signing setup and where certificates live, update mechanism and feed location, settings storage, logging, crash reporting, supported OS matrix, and CI. Follow established patterns; mixing two packaging or update systems is a reliable source of broken installs.

### 3. Choose the approach

| Approach | Examples | Choose when | Costs |
|---|---|---|---|
| Native per OS | Swift/SwiftUI or AppKit (macOS); C#/WinUI or WPF, C++/Win32 (Windows); GTK or Qt-based for Linux desktops | Best integration, performance and platform feel; one primary OS; deep OS features | Separate codebases per OS; specialised skills |
| Web-technology shell with bundled browser engine | Electron | Existing web app or web team; rich UI; consistent rendering across OSes; large ecosystem | Large download and memory use; must manage browser-engine security and updates |
| Web-technology shell using the OS web view, native backend | Tauri (Rust backend), similar web-view hosts | Web UI with a smaller footprint; security-conscious design; team comfortable with the backend language | Rendering differences across OS web views; smaller ecosystem; native backend skills |
| Cross-platform native-widget or custom-rendered toolkit | Qt (C++/Python bindings), Avalonia or .NET MAUI, Flutter desktop, wxWidgets, others | One codebase with native performance; complex desktop UI; teams in those languages | Toolkit-specific skills; native look varies by toolkit; licensing terms to check (e.g. Qt's dual licensing) |
| Progressive web app installed from the browser | — | Simple tools; minimal OS integration; zero-install distribution | Limited file system, background and OS integration; browser-dependent |

Decision factors, roughly in order:

1. **Who builds and maintains it**, and what they know.
2. **Native integration depth** needed (file system, background services, hardware, system-wide shortcuts, accessibility APIs).
3. **Footprint**: an always-on tray utility should not cost hundreds of megabytes of memory; a heavy creative tool can.
4. **Platforms**: one OS favours native; three favour cross-platform.
5. **Existing code**: a mature web app strongly favours a web-tech shell.
6. **Distribution constraints**: app stores impose sandboxing that some approaches handle more easily than others.

State the deciding factors in the handover (see `technical-decision-making`).

### 4. Architecture

- **Separate UI from privileged logic.** In web-tech shells this is enforced by process separation: a privileged main/back-end process and an unprivileged renderer. Keep it that way; expose a narrow, validated set of operations from the privileged side to the UI rather than giving the UI general access.
- **Keep business logic testable** outside the UI framework.
- **Do slow work off the UI thread**: file I/O, parsing, network, image processing (see `concurrency-and-async`).
- **Single instance or multiple?** Decide whether launching the app again (or opening a file with it) should focus the existing instance and hand it the file, or start a new one. Implement accordingly per OS.
- **Lifecycle**: on macOS, apps usually keep running when the last window closes; on Windows and most Linux desktops, closing the last window usually quits, unless the app is a tray utility. Handle shutdown, logoff and sleep/wake (reconnect network, refresh state).

### 5. OS integration and per-OS conventions

| Concern | Windows (typical) | macOS (typical) | Linux (typical) |
|---|---|---|---|
| Menus | Menu bar inside the window, or command bar/ribbon | Global menu bar at the top of the screen with an app menu (About, Settings, Quit) | In-window menu bar or header bar, depending on desktop environment |
| Primary modifier | Ctrl | Cmd | Ctrl |
| Settings | "Settings" or "Options", often under a File/Tools menu | "Settings…" in the app menu, Cmd+, | Varies by desktop environment; "Preferences" common |
| Quit | File > Exit, Alt+F4 closes window | App menu > Quit, Cmd+Q | Ctrl+Q common |
| Window controls | Top-right | Top-left | Varies |
| Background presence | Notification-area (tray) icon | Menu-bar extra; Dock icon | Tray support varies by environment |
| Per-user data location | `%APPDATA%` / `%LOCALAPPDATA%` | `~/Library/Application Support`, `~/Library/Caches` | XDG directories (`~/.config`, `~/.local/share`, `~/.cache`) |
| Installers | MSIX, MSI, or an installer executable; winget and Microsoft Store | Signed and notarized `.app` in a `.dmg` or `.pkg`; Mac App Store | Distribution packages (`.deb`, `.rpm`), Flatpak, Snap, AppImage |

These are conventions to verify against current platform guidelines, not laws. Also implement where relevant:

- **Keyboard shortcuts** that follow each OS (undo/redo, cut/copy/paste, find, new, open, save, close window, preferences), and full keyboard operation of the UI.
- **Standard dialogs** for open/save/print/colour/font via the OS or framework, so users get familiar navigation, recent locations and cloud-drive integration.
- **File associations and protocol handlers** (custom URL schemes), registered by the installer, with the app handling being launched with a file or URL argument — including while already running.
- **Drag and drop** in and out of the app, with the OS's native data formats.
- **Notifications** via the OS notification system, respecting do-not-disturb and user settings.
- **Recent documents** integration (jump lists, Dock menus, recent files).
- **High-DPI and multiple monitors** with different scale factors; windows restored to a visible monitor if the previous one is gone.
- **Dark mode and accent colours** following system settings where the app's design allows.
- **Accessibility**: expose controls to the OS accessibility APIs (screen readers such as Narrator, NVDA, JAWS, VoiceOver, Orca), support high-contrast modes, keyboard focus visibility and text scaling. Web-tech shells inherit much of this from semantic HTML; custom-rendered toolkits often need explicit work. See `accessible-design`.
- **Visual design** derived from the product's brand and audience, adapted to each OS's conventions; use the project's design system if one exists. Do not impose a default look; with no direction, prefer native or toolkit-standard controls and say visual design is open.

### 6. Files, data and settings

- **Store data in the OS-appropriate per-user locations** (table above), separating settings, user data and disposable caches. Never write into the application's install directory; it is often read-only and is replaced on update.
- **Documents belong to the user** and live where the user chooses. Remember the last location; do not hide documents inside app data folders unless the app is explicitly library-based (and then offer export).
- **Write files safely**: write to a temporary file in the same directory, flush, then atomically rename over the original. Keep a backup or autosave for documents. This prevents corruption on crash or power loss.
- **Handle the real file system**: long paths, non-ASCII names, case-insensitive vs. case-sensitive file systems, network and cloud-synced folders (files may be placeholders, locked or changed externally), permission errors, full disks, and files modified by other programs while open.
- **Watch for external changes** to open documents and offer to reload.
- **Settings schema versioning** with migration across app versions; tolerate missing or corrupted settings by falling back to defaults rather than crashing.
- **Secrets** (tokens, passwords) in the OS credential store (Windows Credential Manager/DPAPI, macOS Keychain, Linux Secret Service), not in plain settings files.
- **Uninstall behaviour**: decide what is removed. Usually the app and caches go; user documents stay; settings either stay (for reinstall) or are removed on request.

### 7. Security

General desktop rules:

- Validate every input that crosses a boundary: files opened, URLs received via protocol handlers, command-line arguments, IPC messages, network responses. Malicious documents and links are a primary attack path.
- Never execute or evaluate content from files or the network as code. Be careful with libraries that parse complex formats; keep them updated.
- Use secure transport for all network traffic; verify certificates.
- Run with normal user privileges. Request elevation only for the specific operation that needs it, never for the whole app.
- Sign every executable and installer (see step 9); unsigned binaries are easier to tamper with and trigger warnings.
- Keep dependencies, including bundled runtimes and browser engines, current (see `dependency-management`).

Additional rules for web-technology shells:

- **Do not load remote content into a privileged context.** The UI should be bundled local content; if remote content must be shown, display it in an isolated, unprivileged view.
- **Keep the renderer unprivileged**: no direct access to OS or Node-style APIs from renderer code; enable context isolation and sandboxing; expose only specific, validated functions through a preload or command bridge. In Tauri-style hosts, restrict exposed commands and capabilities to what is needed.
- **Set a strict Content Security Policy.**
- **Control navigation and new windows**: block navigation to unexpected origins; open external links in the user's default browser rather than in the app.
- **Validate IPC on the privileged side**, including the sender, as if every message could be hostile.
- **Update the bundled engine** promptly; an outdated browser engine carries publicly known vulnerabilities.

See `secure-coding` and `security-audit`.

### 8. Performance and footprint

- **Startup time**: show a window quickly; defer loading of plugins, caches and network calls. Measure on a modest machine, not a developer workstation.
- **Memory**: measure idle and working memory; tray utilities and always-on apps should be frugal.
- **Responsiveness**: keep the UI thread free; virtualise long lists; stream large files instead of loading them whole.
- **Bundle size**: remove unused dependencies and assets; for web-tech shells, the engine dominates — choose accordingly in step 3.
- **Power**: avoid timers and polling that wake the CPU; pause work when hidden, minimised or on battery where sensible.
- Profile with OS tools and framework profilers. See `performance-optimization`.

### 9. Packaging, signing and notarization

Plan this before the first external build. Details change; check current official documentation for each platform.

**Windows**

- Sign executables, libraries and installers with a code-signing certificate from a trusted certificate authority; use timestamping so signatures remain valid after the certificate expires.
- Unsigned or newly signed apps may trigger SmartScreen reputation warnings; reputation builds over time and with the signing identity. Current certificate rules typically require keys stored in hardware or a cloud signing service rather than a file on disk.
- Choose a package format: MSIX (modern, clean install/uninstall, store-friendly, some sandbox constraints), MSI (enterprise-friendly, deployable via group policy), or an installer executable built with an installer toolkit. Enterprise customers often require MSI or MSIX with silent install options.
- Decide per-user vs. per-machine install; per-user avoids elevation.

**macOS**

- Sign with a Developer ID certificate for distribution outside the Mac App Store, using the hardened runtime and only the entitlements actually needed.
- **Notarize** the app with Apple's notarization service and **staple** the ticket to the app or disk image, so Gatekeeper allows it to open without warnings, including offline.
- Sign every nested binary, framework and helper; unsigned nested code is the usual cause of notarization failures and "app is damaged" errors.
- Ship universal binaries or separate builds for Apple silicon and Intel as the audience requires.
- The Mac App Store requires App Sandbox and its own signing and review; file access then goes through user-granted access (open/save panels, security-scoped bookmarks to remember access).

**Linux**

- Pick formats for the target audience: distribution packages (`.deb`/`.rpm`) for specific distributions and repositories, Flatpak or Snap for sandboxed cross-distribution distribution with store-like updates, AppImage for a single portable file.
- Sign packages and repository metadata where the format supports it; publish checksums.
- Provide desktop entry files and icons so the app appears in menus, and declare file-type associations there.

**All platforms**

- Automate builds, signing and notarization in CI (see `ci-cd-pipelines`), with signing credentials in a secret store or hardware/cloud signing service, never in the repository, never printed in logs.
- Build release artefacts reproducibly from tagged commits and publish checksums.
- Include licences and third-party notices for bundled dependencies.

### 10. Auto-update

- Use the framework's or platform's established update mechanism where one exists (e.g. framework updater modules, platform package managers, store updates) rather than writing your own download-and-replace logic.
- **Updates must be signed and verified** before installation; serve them over HTTPS. An unverified updater is a remote-code-execution channel.
- Support **staged rollouts** and the ability to pause or roll back a bad release.
- Respect enterprise settings: allow updates to be disabled or managed centrally when deployed by IT.
- Handle the update moment carefully: do not restart without consent while the user has unsaved work; apply on next launch or at a convenient time.
- **Migrate data and settings** forward safely; keep a backup of settings before migrating; test upgrading from several old versions, not only the previous one.
- Test the update path itself before every release: install version N−1, publish N to a test channel, update, verify. A broken updater cannot fix itself.

### 11. Observability and support

- **Logs** written to the OS-appropriate log or app-data location, rotated and size-capped, with no secrets or document contents. Provide a "copy diagnostics" or "open logs folder" action so users can share them with support.
- **Crash reporting** with symbol files retained for each release so native stack traces are readable; ask for consent and disclose what is sent.
- **Version and build information** visible in an About dialog, so support can tell which build a user runs.
- **Safe mode** or a "reset settings" option for apps with plugins or complex settings, so a bad configuration does not lock users out.

### 12. Testing

- **Unit tests** for core logic, file handling (including corrupted and huge files), settings migration and IPC validation.
- **UI/end-to-end tests** with the framework's tooling or OS automation tools for core journeys (see `end-to-end-testing`).
- **OS matrix**: each target OS at the oldest supported and current versions; both CPU architectures where shipped; at least one Linux environment per packaging format.
- **Environment conditions**: high-DPI and mixed-DPI multi-monitor setups, non-English system locale and right-to-left languages, usernames and paths with spaces and non-ASCII characters, a standard (non-admin) user account, network loss, sleep/resume, cloud-synced folders, antivirus or endpoint-protection software present.
- **Install, update and uninstall tests** on clean machines or virtual machines: first install, launch without warnings, file associations working, update from older versions, uninstall leaving the system clean as intended, reinstall.
- **Accessibility pass** with at least one screen reader per OS and keyboard-only operation.

If you can build and run the app, do so after each feature and drive the core journey on each OS available to you. State clearly which OSes and conditions were tested and which were not.

## Decision guidance

### Electron-style vs. OS-web-view-style shells

| Factor | Bundled engine (Electron-style) | OS web view (Tauri-style) |
|---|---|---|
| Rendering consistency across OSes | High — same engine everywhere | Lower — different engines per OS; test each |
| Download size and memory | Larger | Smaller |
| Backend language | JavaScript/TypeScript runtime | Typically Rust or another native language |
| Ecosystem and examples | Very large | Smaller, growing |
| Security posture | Strong if configured carefully; many historical misconfiguration pitfalls | Restrictive capability model by design; still requires care |

### Store vs. direct distribution

| Store | Direct |
|---|---|
| Discovery, trusted install, managed updates, payment handling | Full control, no review delays, no sandbox constraints beyond the OS's |
| Sandbox and review rules may limit features (file access, background tasks, plugins) | You own signing, notarization, update infrastructure and payment |

Many apps do both; plan feature flags for store-specific restrictions.

### Background presence, startup and services

| Need | Typical mechanism | Caution |
|---|---|---|
| Quick access while running | Tray / menu-bar icon | Not every Linux desktop shows tray icons; provide another way to reach the app |
| Start at login | The OS's login-item / startup registration, opt-in from settings | Off by default unless the app's purpose requires it; easy to turn off |
| Work while no user is logged in | A system service or daemon, installed separately with elevation | Large security and support surface; justify carefully; run with least privilege |
| Scheduled work | The OS scheduler or the app's own timer while running | Respect sleep, battery and metered networks |

### Plugins and extensibility

If the app loads plugins or scripts, treat them as code running with the user's rights: load only from defined locations, show what is installed, allow disabling, and, where third parties publish plugins, consider signing or a reviewed registry. Version the plugin API and keep it narrow so the app can evolve without breaking every plugin.

### Enterprise deployment

When businesses deploy the app to many machines:

- Provide silent install and uninstall options and machine-wide install packages.
- Allow configuration through managed settings (e.g. policy files, registry policies on Windows, configuration profiles on macOS) for update behaviour, telemetry and server URLs.
- Document network endpoints the app contacts, for firewall and proxy rules; honour system proxy settings and corporate certificate stores.
- Keep behaviour predictable under endpoint-protection software, which may delay or block unsigned helpers, scripts or self-modifying updates.

### When a desktop app is not the answer

If the app needs no file system access, no offline use, no OS integration and no heavy local computation, a web app may serve users better: no installs, instant updates, every OS. Say so when it applies.

## Working without access to every target OS

You will often not have all three operating systems available, or any build environment at all:

- Use CI runners for each target OS to build, sign and run automated tests, so every platform is at least compiled and smoke-tested on every change.
- Use virtual machines for install and update testing where licensing allows; macOS builds and notarization require Apple hardware or hosted macOS runners.
- List the per-OS configuration the code alone does not express — entitlements, manifests, installer definitions, desktop entry files, file-association registrations, signing identities — and confirm each exists.
- Never describe an OS as supported in the handover when nothing has run on it; say "builds in CI, not manually tested" or "not built" as applicable.

## Worked reasoning

Illustrative only.

**Request:** "Turn our web-based diagram editor into a desktop app so users can save files locally and work offline. Windows and macOS first."

- Existing web app and web team → a web-technology shell; whether bundled engine or OS web view depends on how sensitive the editor is to rendering differences (canvas-heavy editors often favour consistency) and how much the team values footprint — test the editor in each OS web view before deciding.
- Files: native open/save dialogs, a registered file extension and icon, atomic saves, autosave and crash recovery, reload prompt on external change, recent files.
- Offline: the bundled UI works offline; any cloud features degrade with clear status.
- Security: UI bundled locally; renderer unprivileged; a small set of file operations exposed through the bridge, each validating paths and types; links to the web open in the default browser; strict CSP.
- Conventions: macOS app menu and Cmd shortcuts, Windows menu and Ctrl shortcuts; app stays running on macOS when the last window closes.
- Distribution: Developer ID signing and notarization on macOS; code signing and a choice of MSIX or installer executable on Windows (ask about enterprise customers); signed auto-updates with a staged rollout.
- Tests: open, edit, save, crash-recover and update on both OSes, a high-DPI Windows laptop, a non-admin account, a cloud-synced folder.

## Pitfalls and anti-patterns

- **Distribution left to the end.** Discovering signing, notarization and installer requirements in release week. Set them up with the first build.
- **Unsigned or partially signed builds**, producing "unidentified developer", "app is damaged" or SmartScreen warnings that most users will not bypass.
- **Privileged renderer.** Web-tech shells with OS-level APIs available to page scripts, or remote content loaded into the main window — turning any cross-site scripting bug into full machine compromise.
- **Unverified updates** downloaded over plain HTTP or installed without signature checks.
- **Writing into the install directory** or the user's home root instead of the proper per-user data locations.
- **Non-atomic saves** that corrupt documents on crash.
- **One OS's conventions everywhere**: Ctrl shortcuts on macOS, no app menu, quitting when the last window closes on macOS, macOS-style menus on Windows.
- **Hardcoded paths and separators**, assumptions of ASCII usernames, case-sensitive file comparisons on case-insensitive file systems (and the reverse).
- **Blocking the UI thread** with file or network work, freezing the window ("not responding").
- **Ignoring display scaling**: blurry or tiny UI on high-DPI screens, windows reopening off-screen after a monitor is unplugged.
- **Updater that breaks itself**: a release with a bug in the update code strands every user on that version.
- **Restarting to update while the user has unsaved work.**
- **Requiring admin rights** for install or every launch when per-user would do.
- **Generated code that never ran on the target OS**: native configuration (entitlements, manifests, installer definitions, desktop entries) invented or missing. Build and launch on each OS.
- **Licence surprises**: shipping a toolkit or library under terms incompatible with the app's distribution model.
- **Ignoring proxies and corporate networks**: hardcoded direct connections that fail behind authenticating proxies or TLS-inspecting firewalls.
- **Assuming one architecture**: shipping only x64 builds that run under emulation (slowly) on ARM machines, or native modules compiled for the wrong architecture.
- **Settings that cannot be reset**, so a corrupted or bad configuration forces users to find and delete hidden files by hand.
- **Silent data loss on quit**: closing without prompting for unsaved changes, or OS shutdown interrupting a save.
- **Forgetting the second instance**: double-clicking a file while the app is open starts a second copy that fights the first over the same settings and files.

## Quality bar and verification

- [ ] Builds for every target OS and architecture from a clean checkout with documented commands.
- [ ] Installs on a clean machine for each OS and launches without security warnings (signed; notarized and stapled on macOS).
- [ ] Core jobs work on each target OS, tested on that OS, including as a non-admin user.
- [ ] Menus, shortcuts, window and quit behaviour follow each OS's conventions.
- [ ] Files saved atomically; external changes detected; crash recovery or autosave works for documents.
- [ ] Data, settings and caches in the correct per-user locations; secrets in the OS credential store.
- [ ] Web-tech shells: renderer unprivileged, context isolation and sandboxing on, CSP set, navigation restricted, IPC validated.
- [ ] Auto-update verified end to end from an older version, with signature verification, and does not discard unsaved work.
- [ ] Uninstall behaves as documented.
- [ ] High-DPI, multi-monitor, dark mode, keyboard-only use and a screen reader checked on the main flows.
- [ ] Startup time and memory measured on a modest machine and acceptable for the app's role.
- [ ] Signing credentials stored securely and not present in the repository, build logs or artefacts.
- [ ] Opening a file or custom-scheme link while the app is already running hands it to the existing instance (or behaves as deliberately designed).
- [ ] Quitting, logging off or shutting down with unsaved changes prompts or preserves the work.
- [ ] Logs and crash reports contain no secrets or document contents, and users can find them for support.
- [ ] Bundled third-party licences and notices are included and compatible with the distribution model.
- [ ] The handover lists what was verified on which OS, and what was not.

## Safety notes

- Never publish a release, push an update to users, or submit to a store without explicit user confirmation.
- Treat code-signing keys and notarization credentials as highly sensitive: hardware or cloud signing where possible, CI secret stores otherwise, never in repositories or logs. A stolen signing key lets attackers ship malware as you.
- Do not request administrator privileges, install system services, add startup entries or modify system settings unless the app genuinely needs them and the user has agreed.
- Never silently collect telemetry; disclose it and offer a way to opt out where required.
- Be careful running destructive file operations; confirm before deleting or overwriting user files, and prefer moving to the OS trash.

## Related skills

- `frontend-development` for web-technology UIs.
- `secure-coding`, `security-audit` for the security boundaries.
- `interaction-design`, `accessible-design` for the experience.
- `performance-optimization`, `concurrency-and-async` for responsiveness.
- `release-management`, `ci-cd-pipelines`, `dependency-management` for shipping and maintaining.
- `cli-development` when a command-line companion or a CLI alone would serve better.
