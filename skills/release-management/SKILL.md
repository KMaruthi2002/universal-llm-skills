---
name: release-management
description: >-
  Plan and run how software changes reach users: versioning schemes (SemVer,
  CalVer, build numbers), changelogs and release notes, release trains versus
  continuous delivery, release branches and tags, feature flags and
  decoupling deploy from release, staged and percentage rollouts, rollback
  and roll-forward plans, coordinating database migrations and API changes
  with releases, deprecations, and hotfixes. Use when someone asks how to
  version or tag a release, write a changelog, set up a release process or
  cadence, ship a risky feature safely, roll out gradually, plan a rollback,
  sequence a migration with a deploy, deprecate an API, or ship an urgent
  hotfix. Not for building the pipeline mechanics (see ci-cd-pipelines) or
  for a go/no-go review of one specific release (see release-readiness).
metadata:
  category: devops
  related: ci-cd-pipelines, release-readiness, git-workflow, database-migrations, api-design, dependency-management, incident-response, code-documentation
---

# Release Management

Release management is the set of decisions and habits that govern *what* ships, *when*, *to whom*, and *how you get back* if it goes wrong. The pipeline (see `ci-cd-pipelines`) is the machinery; release management is the policy that drives it. Good release management makes releases small, frequent, predictable, and reversible, so that shipping is routine rather than an event. Poor release management shows up as big-bang launches, frozen weeks, mystery versions in production, and rollbacks that do not work.

## Scope

Covers: versioning, tags and branches for releases, changelogs and release notes, cadence models, feature flags, staged rollouts, rollback planning, migration and API-change sequencing, deprecation, hotfixes, and release communication. Applies to services, libraries, mobile/desktop apps, and on-prem or packaged software, with differences called out.

Hands off to:

- Pipeline implementation, deployment strategies' mechanics → `ci-cd-pipelines`.
- A go/no-go checklist for a particular release → `release-readiness`.
- Branching model for everyday work → `git-workflow`.
- Writing safe schema migrations → `database-migrations`.
- API compatibility design → `api-design`.
- Handling a release that breaks production → `incident-response`.

## Core principles

**1. Small batches reduce risk.** The risk of a release grows with the amount of change in it: more interactions, harder diagnosis, harder rollback. Releasing ten small changes separately is safer than releasing them together, even though it feels like more releases. Delivery-performance research consistently finds that teams deploying more frequently also have lower change failure rates and faster recovery.

**2. Separate deploy from release.** Deploying puts code in production; releasing exposes behaviour to users. Feature flags, dark launches, and staged rollouts let you deploy continuously while choosing when and to whom features are released. This turns risky launches into gradual, reversible exposures.

**3. Every release needs a way back.** Before shipping, know how to undo it: roll back the artifact, turn off the flag, or roll forward with a fix. The plan has to account for the things that do not roll back: database migrations, data written in new formats, messages sent, mobile app binaries already installed, published packages.

**4. Versions communicate.** A version number tells consumers what to expect. For libraries and APIs, a semantic version is a promise about compatibility; breaking it without bumping the major version breaks other people's software. For services, versions identify exactly what is running.

**5. Changelogs are for the people affected.** Users, integrators, support, and future maintainers need to know what changed in terms of behaviour and impact, not a dump of commit messages.

**6. Expand, then contract.** Any change that crosses a compatibility boundary (database schema, API, message format, config) is done in phases where old and new coexist, so each release is independently deployable and reversible.

## Discovering context first

1. **What is being released?** Web service (continuous, controlled by you), library/SDK (consumers upgrade on their schedule), mobile app (store review, users update slowly), desktop/on-prem (customers may run old versions for years), firmware. The constraints differ sharply.
2. **Existing conventions:** version scheme in tags and manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `*.csproj`, `build.gradle`, app store version/build numbers), changelog file and format (e.g. Keep a Changelog style, generated from conventional commits, release notes in GitHub/GitLab releases), release branch naming, tagging, release tooling (semantic-release, release-please, changesets, goreleaser, fastlane, custom scripts).
3. **Cadence and approvals:** continuous deployment, scheduled trains, change advisory processes, freeze periods, compliance needs for change records.
4. **Feature-flag system** in use (commercial service, open-source, homegrown config) and its conventions for naming, ownership, and cleanup.
5. **Support commitments:** which versions are supported, for how long, and whether there are LTS lines.
6. **Consumers:** who depends on this (internal teams, public users, partners), and how they learn about changes.

Follow existing conventions. Changing the versioning scheme or changelog format of an established project affects every consumer and tool; propose it only with a clear reason.

## Versioning

| Scheme | Format | Best for | Notes |
|---|---|---|---|
| Semantic Versioning (SemVer) | `MAJOR.MINOR.PATCH` | Libraries, SDKs, APIs, CLIs — anything with consumers who need compatibility signals | MAJOR = breaking, MINOR = backward-compatible features, PATCH = backward-compatible fixes. Pre-releases like `2.0.0-rc.1` |
| Calendar Versioning (CalVer) | e.g. `2026.10`, `2026.10.2`, `26.10` | Applications and products released on a schedule, where "how old is this?" matters more than API compatibility | Make the scheme explicit (year, month, sequence) |
| Build/commit identifiers | Commit SHA, build number | Internal services deployed continuously | Still tag releases or record deployed SHAs so "what is running" is answerable |
| Platform-mandated | Store version string + monotonically increasing build number | Mobile apps | Build numbers must always increase; marketing version can follow SemVer or CalVer |

SemVer practicalities:

- **What counts as breaking** is about the public contract: removed or renamed functions, endpoints, fields, CLI flags; changed types or defaults; stricter validation; changed error behaviour that callers depend on; raised minimum runtime or platform versions. If in doubt, assume consumers depend on it (Hyrum's law: with enough users, every observable behaviour is depended on by somebody).
- `0.x` versions signal instability; many ecosystems treat a `0.MINOR` bump as breaking. Move to `1.0.0` when you are ready to make compatibility promises.
- Never re-publish a different artifact under an existing version. Versions are immutable; a mistake gets a new version (and the bad one is yanked/deprecated where the registry supports it).
- Ecosystem conventions matter: Go module major versions change the import path; some ecosystems' resolvers rely on specific version semantics. Follow the language's norms.
- Automating version bumps from commit messages (e.g. conventional commits with release tooling) works well when the team writes commits consistently; otherwise it produces wrong bumps. A changeset-style approach (contributors add a small file describing the change and its bump level in the PR) is more explicit.

## Changelogs and release notes

A changelog records changes per version for people who use or maintain the software. Release notes are the user-facing announcement for a release, often more curated.

What good entries contain:

- Grouping by impact: breaking changes (first, prominently, with migration steps), new features, fixes, deprecations, security fixes (with identifiers like CVEs where applicable), performance changes.
- Written from the reader's point of view: "Exports now include the time zone in timestamps; parsers expecting naive timestamps must be updated", not "refactor exporter".
- Links to issues, PRs, and documentation for detail.
- Version and release date.
- For breaking changes: what breaks, who is affected, what to do, and until when the old behaviour is available.

Practice:

- Maintain an "Unreleased" section updated in each PR, or generate notes from structured commit messages or changeset files, then edit for readability. Raw commit-log dumps are not useful changelogs.
- Exclude noise (internal refactors, CI tweaks) unless they affect users or contributors.
- For services without external consumers, an internal release log (what was deployed, when, with links) still helps incidents and audits.

## Cadence models

| Model | How | Strengths | Weaknesses | Fits |
|---|---|---|---|---|
| Continuous deployment | Every merged change deploys automatically, behind flags as needed | Smallest batches, fastest feedback, no release events | Needs strong tests, monitoring, automated rollback, flag discipline | Web services and SaaS with mature pipelines |
| Continuous delivery with on-demand releases | Every change is releasable; humans choose when | Flexibility, still small batches if done often | Batches grow if releases are infrequent | Teams building confidence, or with coordination needs |
| Release train | Fixed schedule (e.g. weekly, every two weeks); whatever is ready boards the train | Predictable for stakeholders, QA, and marketing; missing a train is cheap because the next one is soon | Wait time for changes; release-day risk if trains are large | Mobile apps, multi-team products, customer-facing schedules |
| Versioned/major releases | Large planned releases, often with LTS lines | Fits customers who upgrade rarely, on-prem | Big batches, long stabilisation, backporting burden | On-prem, enterprise, OS/platform software |

Heuristics:

- Shorten the cycle before adding process. A weekly release with a short checklist usually beats a monthly release with a long one.
- On a train, the date is fixed and scope flexes. Features that are not ready stay behind flags or wait for the next train; do not hold the train.
- Code freezes are a symptom of low confidence in the release process. If you need them (e.g. peak retail season), keep them short, define what is allowed (security fixes, critical bugs), and use the time to fix the underlying causes.

## Branching and tagging for releases

- **Trunk-based with tags:** release from main; tag the commit (`v1.4.0`). Simplest; works with continuous delivery.
- **Release branches:** cut `release/1.4` from main for stabilisation, fix on main and cherry-pick to the branch (or fix on the branch and merge back — pick one direction and stick to it to avoid lost fixes). Needed when you support multiple versions or when stabilisation takes days.
- **Long-lived maintenance branches** for supported older majors or LTS versions. Each adds backporting work; limit how many you maintain and publish the support policy.
- Tags are the source of truth for what a version contains. Protect release tags from being moved or deleted.
- See `git-workflow` for everyday branching; release branching is a narrower concern.

## Feature flags

Flags let you deploy code dark and control exposure at runtime.

Types, with different lifetimes:

| Type | Purpose | Lifetime |
|---|---|---|
| Release flag | Hide unfinished or newly launched features; progressive exposure | Days to weeks; remove after full rollout |
| Experiment flag | A/B tests | Duration of the experiment |
| Ops flag / kill switch | Disable expensive or risky functionality under load or during incidents | Long-lived, intentionally |
| Permission/entitlement flag | Features by plan or customer | Long-lived; arguably product configuration, not a flag |

Practice:

- Name flags descriptively, record an owner and expected removal date at creation.
- Default to the safe state (off) when the flag service is unavailable; the app must work without it.
- Test both paths of a flag, and the transition while traffic is flowing.
- **Remove release flags promptly.** Stale flags are dead code that hides bugs, multiplies test combinations, and occasionally gets flipped by accident with surprising results. Track flag count and age; add removal to the definition of done for a launch.
- Flag changes are production changes: audit who changed what and when, and show flag changes alongside deploys on dashboards (see `observability`).
- Avoid flags that gate database schema differences; schema changes follow expand/contract regardless of flags.

## Staged and progressive rollouts

Release to a small, observable audience first, then widen:

1. Internal users / employees (dogfooding).
2. A small percentage of users or a low-risk segment (e.g. 1–5%), or specific beta customers.
3. Increasing percentages (e.g. 10% → 25% → 50% → 100%), with bake time at each stage long enough to observe meaningful traffic and daily cycles.
4. Full rollout; then remove the flag.

Decide **before starting**: which metrics determine go/no-go at each stage (error rates, latency, key business events, support tickets, crash-free sessions for mobile), what thresholds trigger a halt or rollback, and who decides. Compare the exposed cohort against the unexposed one where tooling allows; absolute metrics drift with time of day.

Platform specifics:

- **Mobile app stores** support phased/staged rollouts by percentage and the ability to halt; a halted release still remains on devices that installed it, so pair with remote kill switches and server-side compatibility for old app versions. Users update slowly; servers must support several app versions at once, often for many months. Consider a minimum-supported-version mechanism to force upgrades when necessary.
- **Libraries:** pre-releases (`-beta`, `-rc`) let early adopters test; a release candidate period before a major version catches breakage.
- **On-prem/desktop:** early-access channels or rings; customers control upgrades, so long support windows and clear upgrade guides matter more.

## Rollback planning

For each release, answer before shipping:

- **What is the rollback mechanism?** Redeploy previous artifact, flip flag, revert config, app-store halt plus server-side kill switch, publish a patch version.
- **How long does it take,** and has it been exercised recently?
- **What will not roll back?** Schema changes, data migrations, new data written in new formats, events emitted to other systems, emails or notifications sent, external API calls made, cache entries in new formats, published packages, installed mobile binaries.
- **Is the previous version compatible with data the new version wrote?** If the new version writes a new enum value, a new field, or a new format, the old version may crash reading it. This is the most common reason rollbacks fail.
- **Who can decide to roll back,** and on what signals? Make it a low-friction decision: rollback should not require a meeting.

If rollback is genuinely impossible for a release (an irreversible migration, for example), say so explicitly in the release plan, reduce the risk by other means (more staging time, backup, smaller scope, a tested fix-forward path), and make sure approvers understand.

## Coordinating migrations and compatibility changes

The safe pattern for any change that crosses a boundary between independently deployed things (app ↔ database, service ↔ service, server ↔ mobile client, producer ↔ consumer):

1. **Expand:** add the new thing alongside the old (new column, new endpoint/field, new message version). Old code is unaffected. Ship.
2. **Migrate writers/readers:** deploy code that writes both, or reads new with fallback to old. Ship. Backfill existing data if needed, in batches, as a separate step.
3. **Switch:** move reads to the new thing; verify. Ship.
4. **Contract:** after all consumers have moved (including old mobile versions and other teams), and a safe period has passed, remove the old thing. Ship.

Each step is a separate release that can be rolled back independently. Never combine "remove old column" with "stop using old column" in one release: the old version, if rolled back to, will need it.

Specific guidance:

- Run schema migrations as an explicit step before the app deploy that needs them, and make them backward compatible with the currently running version (see `database-migrations`).
- Long-running migrations (large table rewrites, backfills) should be decoupled from deploys entirely, run online in batches, and be resumable.
- For APIs, add fields rather than change them; version endpoints or media types for breaking changes (see `api-design`).
- For event/message formats, consumers should tolerate unknown fields; producers should not remove fields until consumers stop needing them; schema registries with compatibility checks help.

## Deprecation

- Announce early with a timeline: deprecated in version X / on date D, removed no earlier than version Y / date E. Give consumers enough time for their own release cycles — for public APIs, often 6–12 months or more.
- Emit warnings in the old path: deprecation headers in API responses, runtime warnings in libraries, logs or metrics you can watch.
- **Measure usage** of the deprecated path before removing it; contact remaining heavy users directly.
- Provide a migration guide with before/after examples.
- Remove in a major version (libraries) or after the announced date (services), and note it prominently in the changelog.

## Hotfixes

A hotfix is an urgent fix that bypasses the normal cadence because waiting would cause unacceptable harm.

- **First ask whether a rollback or flag-off solves it faster.** It usually does, and it is lower risk than new code written under pressure.
- Keep the change minimal: fix the one problem, no refactors or bundled features.
- Still review it (a second person, even if fast) and still run the automated tests. Skipping all checks under pressure is how one incident becomes two.
- Branch from the exact version in production (the release tag), not from main if main has moved on with unreleased changes; otherwise the hotfix ships those changes too.
- Bump the patch version (or the platform's equivalent), tag, deploy through the normal pipeline path (perhaps with an expedited approval), and watch metrics.
- **Merge the fix back to main** (and any other active release branches) immediately, or the bug returns in the next release.
- Record it: changelog entry, link to the incident, and a postmortem if it followed an incident.

## Release communication

- Internal: who needs to know before the release (support, sales, operations, other teams with dependencies), at release, and after — especially for behaviour changes and known issues.
- External: release notes, migration guides, status updates for scheduled maintenance, announcements for major features.
- Timing: announce breaking changes and deprecations well in advance; announce features once they are actually available to the audience reading the announcement (staged rollouts complicate "launched" messages).
- Keep one place where people can see what is released and what is coming.

## How release concerns differ by artifact

| Concern | Web service | Library / SDK | Mobile app | On-prem / desktop |
|---|---|---|---|---|
| Who controls upgrade timing | You | Consumers | Users and stores | Customers |
| Rollback | Redeploy previous artifact | Publish a fix version; yank/deprecate bad one | Halt rollout; kill switch; ship new build | Ship patch; customers must apply |
| Versions in the wild | One or two at a time | Many, indefinitely | Many, for months | Many, for years |
| Compatibility burden | Between your own components | Public API and behaviour | Server must support old clients | Upgrade paths across many versions, data migrations at customer sites |
| Lead time | Minutes | Minutes to publish, months to adopt | Store review (hours to days) plus adoption | Customer change windows |
| Most important safeguard | Progressive rollout + fast rollback | Strict SemVer + changelog + pre-releases | Server-side flags + minimum-version control | Tested upgrade path + long support policy |

## Measuring release health

Track a few delivery metrics to see whether the process is improving (often called the DORA metrics):

- **Deployment frequency:** how often changes reach production.
- **Lead time for changes:** commit to running in production.
- **Change failure rate:** percentage of releases causing degradation that needs remediation (rollback, hotfix, incident).
- **Time to restore:** how long it takes to recover from a failed change.

Use them as a team learning tool, not individual targets; gaming them (splitting releases artificially, not declaring failures) destroys their value. A rising change failure rate after increasing frequency points to missing safeguards (tests, canaries, flags), not to a need to slow down. Also watch flag debt (count and age of release flags) and the age of the oldest unreleased change on main.

## Process: setting up or repairing a release process

1. **Map the current path** from merged change to users: steps, waits, approvals, manual actions, and how long each takes. Where does work queue up?
2. **Find recent release failures** and what caused them (incident and rollback history). They tell you which safeguards are missing.
3. **Make the artifact and version traceable** first: immutable artifacts, tags, a way to ask "what is running?".
4. **Establish the way back** for every release type: rollback mechanics, flag kill switches, compatibility rules for data.
5. **Shrink batches:** increase release frequency gradually, moving risky features behind flags so the cadence does not depend on feature completion.
6. **Automate the repetitive parts:** version bumps, changelog assembly, tagging, publishing, release notes drafts.
7. **Write down the policy briefly:** cadence, who approves, versioning rules, support windows, hotfix procedure, flag lifecycle. A one-page policy that people follow beats a long one nobody reads.
8. **Review after a few cycles** with the release-health metrics and adjust.

## Safety notes

- Do not publish packages, push release tags, promote to production, or trigger app-store submissions without explicit user confirmation that names the version and target. Publishing to public registries is effectively irreversible.
- Do not flip feature flags in production, or change rollout percentages, without confirmation; they are production changes.
- Never include secrets, internal hostnames, customer names, or unpatched-vulnerability details in public release notes. Coordinate security fix disclosures with the security team.
- Destructive migration steps (dropping columns or tables, deleting data) require a backup, confirmation, and a passed waiting period after the code stopped using them.

## Pitfalls and anti-patterns

- **Big-bang releases** with weeks of accumulated changes and a "release day" war room.
- **Version numbers that do not mean anything,** or breaking changes shipped as minor or patch versions.
- **Re-publishing or moving tags** for an existing version.
- **Changelogs that are commit dumps,** or no changelog at all.
- **Flags never removed;** hundreds of stale flags with unknown owners.
- **Rollback plans that ignore data,** so the old version crashes on new data.
- **Migration and destructive cleanup in the same release.**
- **Hotfix branched from main,** accidentally shipping unreleased features.
- **Hotfix never merged back,** so the bug reappears next release.
- **Holding the train** for one late feature, delaying everything else.
- **Long freezes** instead of fixing the confidence problem that makes them necessary.
- **Assuming all clients update immediately** (mobile, desktop, partner integrations).
- **Launch announcements before the rollout reaches the audience,** so users read about a feature they cannot see.
- **Release notes written after the fact from memory,** missing breaking changes; capture notes in each PR instead.
- **Supporting too many old versions** without a published policy, so backports consume the team.
- **Manual, undocumented release steps** known to one person; when they are away, nobody can ship or roll back.

## Verification

- [ ] The version follows the project's scheme and correctly reflects compatibility (any breaking change → major bump for SemVer consumers).
- [ ] Release tag points at the exact commit built and tested; the artifact is immutable and identifiable in production.
- [ ] Changelog/release notes describe user-visible changes, list breaking changes with migration steps, and contain nothing sensitive.
- [ ] Rollback mechanism identified, timed, and recently exercised; non-reversible elements listed with mitigations.
- [ ] Migrations sequenced expand → migrate → contract; the previous version works against the new schema and data.
- [ ] Rollout plan has stages, metrics, thresholds, and a named decision-maker.
- [ ] New flags have owners and removal dates; flags from completed rollouts are scheduled for removal.
- [ ] Hotfixes are merged back to main and other active branches.
- [ ] Stakeholders who need to know have been told, at the right time.

Report: version and what it contains, rollout plan and current stage, rollback plan, what does not roll back, communications done or pending, and any risks accepted.

## Worked example: renaming a field used by mobile clients

Situation: the API's `user.name` should become `user.display_name`, and the database column should be renamed accordingly. The mobile apps, whose old versions stay in use for months, read `name`.

Plan:

1. Release A: add a `display_name` column; the app writes both columns; backfill existing rows in batches. The API returns both `name` and `display_name`. (Expand.)
2. Release B (mobile): new app versions read `display_name`, falling back to `name`.
3. Release C: the API reads from `display_name` only, still writing both and returning both fields.
4. Wait until usage of old app versions that read `name` falls below the agreed threshold (measured from request headers carrying the app version), possibly using a minimum-version prompt.
5. Release D: stop returning `name`; announce in API release notes. Stop writing the old column.
6. Release E, after a safety period and a backup: drop the old column. (Contract.)

Each release can be rolled back on its own; no single deploy breaks either old clients or the previous server version. The process is slower than a single rename, and that is the point: it trades calendar time for safety.
