---
name: release-readiness
description: >-
  Run a go/no-go assessment for shipping a release, launch, major feature,
  migration or deployment: identify what this release actually risks, check
  test and quality status, known issues and their severity, migration and
  rollback plans, feature flags and staged rollout, monitoring and alerting,
  documentation, support and stakeholder readiness, and record explicit risk
  acceptance. Builds checklists derived from the release's real risk rather
  than a generic list, and produces a clear go, go-with-conditions, or no-go
  recommendation. Use when asked "are we ready to ship", "go/no-go for the
  release", "launch checklist", "release review", "can we deploy this on
  Friday", or "what's blocking the release". Not for designing the release
  process or versioning itself (release-management) or for test planning
  from scratch (qa-test-planning).
metadata:
  category: quality
  related: release-management, qa-test-planning, testing-strategy, database-migrations, observability, incident-response, ci-cd-pipelines, end-to-end-testing, postmortem, business-communication
---

# Release Readiness

Release readiness is a decision under uncertainty: **is the expected benefit of shipping now greater than the risk, and are we prepared for the ways it could go wrong?** "Ready" never means "risk-free". It means the risks are known, sized, mitigated where it matters, explicitly accepted where they remain, and that the team can detect and recover from a bad outcome quickly.

The deliverable is a recommendation (go, go with conditions, or no-go) with the evidence behind it, the open risks and who accepted them, and the conditions under which the release would be halted or rolled back.

Scope: this skill is the assessment. For designing the release process, versioning, branching and changelogs, see `release-management`. For building a test plan, see `qa-test-planning`. For the pipeline mechanics of deploying, see `ci-cd-pipelines`. If something goes wrong after release, see `incident-response`.

## Core principles

**1. Derive the checklist from this release's risk, not from a generic template.** A copy change and a payment-system migration do not need the same review. Generic checklists either bloat small releases (and get ignored) or miss the specific danger of large ones. Start by asking what could go wrong with *this* release, then check exactly those things.

**2. Recoverability matters as much as correctness.** You cannot test away every defect. A release with a tested, fast rollback and good monitoring can tolerate more uncertainty than one that is irreversible and invisible. Ask "how fast can we notice and undo a problem?" before "have we found every bug?".

**3. Irreversible steps deserve the most scrutiny.** Code can usually be rolled back; data migrations, sent emails, external API contracts, published app binaries, and announcements usually cannot. Identify the irreversible steps and treat them as separate, gated decisions.

**4. Evidence over assertion.** "QA signed off" and "it's tested" are claims. Test results, coverage of the risky paths, a rehearsed migration, and a working dashboard are evidence. Ask for the evidence that matches each risk.

**5. Known issues need owners and decisions, not just a list.** Every known defect shipping with the release should have a severity, an impact statement, a workaround if any, and a named person who accepted it. Unowned known issues are how "we knew about that" incidents happen.

**6. The decision needs a decider.** A readiness review advises; someone with the authority accepts the residual risk. Make clear who that is, and record the decision.

**7. Readiness includes people, not just software.** Support needs to know what changed; on-call needs to be available and briefed; users and stakeholders may need notice. A technically perfect release can still fail operationally.

## Discovering context

Find out first:

- **What is in the release**: changes, features, fixes, dependency upgrades, infrastructure and configuration changes, migrations. A release note draft or the diff between versions is the starting point. Surprise contents are a common risk; confirm the actual build matches the intended scope.
- **The release process the team already uses**: existing checklists, release templates, approval gates, change management requirements, deployment windows, freeze periods. Use and extend them rather than replacing them.
- **How it deploys**: continuous deployment, scheduled release train, app store submission, on-premise customer installs, firmware. This changes what rollback means.
- **Who is affected**: all users, a segment, internal only, specific customers with contractual commitments.
- **Deadlines and their reality**: a regulatory date or a contractual launch is a hard constraint; an internal target date is negotiable. Know which this is before weighing "ship anyway".
- **Recent history**: previous incidents in this area, flaky tests, outstanding issues from the last release.

## The process

### 1. Characterise the release's risk

Before any checklist, sort the release along these dimensions. The answers decide how deep the rest of the assessment goes.

| Dimension | Lower risk | Higher risk |
|---|---|---|
| Size and scope | Few, isolated changes | Many changes, cross-cutting, multiple teams |
| Area | Leaf UI, internal tools | Auth, payments, data pipelines, core APIs, infrastructure |
| Reversibility | Instant rollback or flag off | Data migrations, client binaries, external contracts, notifications sent |
| Exposure | Internal, beta cohort, gradual rollout | All users at once, high-traffic period |
| Novelty | Routine change to familiar code | New system, new dependency, new vendor, first release of a product |
| Detection | Strong monitoring on affected paths | Failure would be silent or delayed (data corruption, billing errors) |
| Timing | Normal hours, team available | End of week, before holidays, during peak season, during another change |

Then write down, specifically, the **top risks**: the handful of ways this release is most likely to hurt users or the business. Examples: "the migration locks the orders table during peak", "the new pricing logic charges some customers incorrectly", "the mobile build crashes on older OS versions", "the new provider rate-limits us at launch traffic".

Every later step should trace back to these risks.

### 2. Check quality evidence against the risks

For each top risk, ask what evidence shows it is controlled.

- **Automated tests**: do they pass on the exact build being released (not a nearby commit)? Do they cover the risky paths specifically, or only the happy path? Are any tests skipped, quarantined or marked flaky in this area? A quarantined test in the area you are changing is effectively no test.
- **Manual or exploratory testing**: was it done on a production-like environment, with realistic data volumes and configurations?
- **Non-functional testing** where the risk calls for it: load or performance tests for traffic-sensitive changes, security review for auth or data exposure changes, accessibility checks for UI changes, compatibility testing across browsers, devices, OS versions, or client versions.
- **Upgrade testing**: does the new version work with existing data, existing client versions, and existing configurations, not just a clean install?
- **Dependency changes**: are upgraded libraries' breaking changes and known issues reviewed?

Ask for test *results*, not just test *existence*. "Do we have tests for X?" is weaker than "did the tests for X run against this build, and what did they show?".

### 3. Triage known issues

List every known open defect that will ship or that affects the release. For each:

- **Severity and impact**: who is affected, how badly, how often.
- **Workaround**: exists and is documented for support?
- **Decision**: fix before release, ship with known issue, or pull the affected feature (often via flag).
- **Owner**: who accepted it, and the follow-up ticket.

A useful default rule (adapt to the team's definitions): no known issues that cause data loss, security exposure, incorrect money movement, or blocking failure of a core flow for a meaningful share of users. Anything below that bar is a judgement weighing impact against the cost of delay.

Watch for clusters: several "minor" issues in the same feature may add up to a poor experience that is effectively major.

### 4. Review migrations and irreversible steps

For each database migration, data backfill, or other irreversible step:

- Has it been rehearsed on production-like data volume? How long does it take? Does it lock anything users depend on?
- Is the code compatible with both the old and new schema during the rollout (so code and schema can be deployed and rolled back independently)?
- Is there a backup or snapshot taken immediately before, and has restoration from it been tested?
- What is the "point of no return", and who makes the call to cross it?
- How will you verify the migration succeeded (row counts, checksums, spot checks, invariants)?

See `database-migrations` for technique. For non-database irreversible steps (emails, push notifications, app store releases, partner API changes), consider sending to a small cohort first or gating behind an explicit final approval.

### 5. Confirm the rollback and roll-forward plan

A rollback plan is only real if it is specific and tested:

- **Mechanism**: redeploy previous version, flip a feature flag, revert config, restore data, or roll forward with a hotfix? Which one for which failure?
- **Speed**: how long from decision to restored service? Is it within what users and the business can tolerate?
- **Preconditions**: does rollback work after the migration has run? After new data has been written in the new format? For mobile or desktop clients, rollback is often impossible; you need server-side kill switches or flags instead.
- **Rehearsal**: has rollback been exercised for this kind of change, ideally in staging for this specific release?
- **Triggers**: the specific signals that mean "roll back" (error rate above X, latency above Y, a failed verification check, support ticket spike). Decide these in advance; under pressure, people rationalise waiting.
- **Authority**: who can call the rollback without needing a meeting?

### 6. Plan the rollout

Choose the exposure strategy that matches the risk:

| Strategy | Use when | Notes |
|---|---|---|
| All at once | Low risk, easy rollback, strong tests | Fastest; largest blast radius |
| Canary (small % of traffic or hosts first) | Server-side changes with good metrics | Needs comparison between canary and baseline |
| Staged / percentage rollout | Most user-facing changes of moderate or higher risk | Define stages, hold times, and promotion criteria |
| Feature flag, dark launch | Code ships disabled; enable separately | Decouples deploy from release; flag hygiene needed afterwards |
| Cohort / beta | New products or big UX changes | Internal users, opted-in users, or a region first |
| Blue-green | Need instant switch back at infrastructure level | Costs duplicate capacity; data layer still shared |
| Scheduled maintenance window | Unavoidable downtime | Communicate in advance; rehearse the timeline |

For staged rollouts, define promotion criteria ("error rate and latency within X of baseline for N hours; no new P1 tickets") rather than promoting on a timer.

Timing: prefer releases when the people who can fix problems are available and traffic is normal. A high-risk change late before a weekend or holiday is a choice to make deliberately, not by default.

### 7. Check monitoring and detection

The release is not ready if you would not notice it failing.

- Are there dashboards and alerts covering the top risks specifically? (Generic CPU graphs do not detect a pricing bug.)
- Can you distinguish the new version from the old in metrics and logs (version tags, flag state)?
- For silent-failure risks (data correctness, billing, emails), is there an explicit verification check after release, such as a query, a reconciliation, or a sample review?
- Are alert thresholds set, and do they page someone who knows about this release?
- Is someone assigned to watch the release for a defined period afterwards?

See `observability`.

### 8. Check documentation, support and communication

- **User-facing docs, help articles, in-app text, release notes**: updated and accurate for what is actually shipping (not what was planned).
- **API changes**: changelogs, deprecation notices, and migration guides for integrators; sufficient notice for breaking changes.
- **Support**: briefed on what changed, known issues and workarounds, how to escalate; macros or FAQs prepared for expected questions.
- **On-call**: knows the release is happening, what it changes, where the runbook and rollback instructions are.
- **Stakeholders**: sales, customer success, marketing, partners, and any customers with contractual notice requirements informed as appropriate.
- **Internal**: other teams whose systems interact with this change know the timing.

### 9. Make and record the decision

Bring the evidence together in a short readiness summary and get an explicit decision from the person with authority. A good summary contains:

- **Recommendation**: go, go with conditions, or no-go, in the first line.
- **What is shipping** and its risk characterisation.
- **Top risks and their mitigations**, each with the evidence.
- **Known issues shipping**, with severity and the person who accepted each.
- **Conditions** for a conditional go (e.g. "go for 5% rollout only; promote after migration verification passes").
- **Rollback triggers and owner.**
- **Open items** and their deadlines.
- **What was not checked**, so nobody assumes coverage that was not done.

Record the decision where the team will find it later. If the release goes badly, the record makes the postmortem fair: it shows what was known and accepted, rather than leaving people to reconstruct it from memory.

### 10. After release

Readiness continues through the rollout:

- Watch the agreed signals for the agreed period; run post-release verification checks.
- Promote stages only when criteria are met.
- Roll back promptly if triggers fire; do not wait for certainty.
- Close out: remove or schedule removal of temporary flags, update the known-issues list, file follow-ups, and note anything the readiness process missed for next time (feeds `postmortem` if there was an incident).

## Decision guidance

**Go, conditional go, or no-go?**

| Situation | Typical outcome |
|---|---|
| Top risks have evidence of control, rollback tested, monitoring in place, no unaccepted severe issues | Go |
| One or more risks are partially controlled but exposure can be limited | Go with conditions (staged rollout, flag off for a segment, extra verification) |
| A severe known issue lacks a decision or owner | No-go until decided, not necessarily until fixed |
| Irreversible step without rehearsal or backup | No-go for that step; the reversible parts may still ship |
| No way to detect the most likely failure | No-go, or conditional go with manual verification and very limited exposure |
| Critical tests failing or not run against this build | No-go until resolved or explicitly risk-accepted at the right level |
| Hard external deadline with unresolved moderate risk | Usually conditional go with mitigation and an explicit, recorded acceptance |

**Delay versus ship with known issue**: weigh the cost of delay (lost value, missed commitments, a larger and riskier batch later) against the impact of the issue times its probability, and how quickly it could be fixed after release. Delaying is not automatically safe: batching more changes into the next release increases its risk.

**Splitting a release**: if one component is not ready, consider shipping the rest and holding that component behind a flag. This is usually better than delaying everything, provided the components are genuinely independent.

**Release freezes and "no deploys on Friday" rules**: they exist because recovery capacity is lower at those times. Treat them as risk inputs; if the team has such a rule, follow it, and exceptions should be explicit decisions with additional safeguards.

## Building a risk-derived checklist

When the team has no checklist, or the generic one does not fit, build one from the risk characterisation:

1. Start from the top risks identified in step 1.
2. For each risk, write the check that would give evidence it is controlled, the check that would detect it in production, and the action if it happens.
3. Add the always-relevant baseline items that are cheap: build matches intended scope; tests pass on the release build; rollback mechanism identified; on-call aware.
4. Add domain items only if the release touches the domain (migrations, client binaries, public API, compliance-sensitive data, pricing, notifications).
5. Remove items that do not apply. A short checklist that is actually used beats a long one that is skimmed.

Illustrative fragment for a release that changes how invoices are calculated (one possible shape):

- Risk: incorrect invoice totals for some plan types. Evidence: tests for every plan type and proration case pass on the release build; comparison of old vs new calculation on last month's real invoices shows only the intended differences. Detection: post-release reconciliation query comparing totals for the first day's invoices; alert on refund requests. Action: flag off new calculation; regenerate affected invoices.
- Risk: customers surprised by changed amounts. Evidence: customer notice sent N days before; support briefed with explanation and macro.

## Who takes part

Readiness is cross-functional; the assessor's job is to gather the right inputs, not to know everything. Depending on the release, involve:

- **Engineering owners** of each changed component: confirm scope, tests, migrations and rollback.
- **QA or test owners**: test results, coverage of risky paths, open defects.
- **Operations / on-call / SRE**: monitoring, alerts, capacity, rollback mechanics, availability during and after release.
- **Product owner**: known-issue acceptance, scope trade-offs, the cost of delay.
- **Support and customer-facing teams**: readiness to handle questions and known issues.
- **Security, privacy or compliance**: when the release touches their areas or policy requires sign-off.
- **The decider**: the person with authority to accept residual risk, often the product or engineering lead, sometimes a change advisory group.

Keep the go/no-go conversation short and evidence-based. If a meeting is needed, circulate the readiness summary first and use the meeting only for open risks and the decision.

If you are an AI assistant preparing the assessment, gather and summarise the evidence and give a recommendation, but do not trigger the deployment, flip production flags, send customer communications, or record risk acceptance on someone's behalf without that person's explicit instruction.

## Domain-specific considerations

Add these only when the release touches the domain.

**Mobile and desktop clients**: binaries cannot be rolled back once installed, and store review adds delay to any fix. Check: server-side kill switches or flags for new features; compatibility of the new client with the current server and of the current (old) clients with any server changes; crash reporting in place; staged rollout percentages in the store; minimum supported versions; behaviour on older OS versions and low-end devices.

**Public APIs and SDKs**: other people's code depends on you. Check: backward compatibility (or versioning and deprecation notice); changelog and migration guide; behaviour for clients that send old request shapes; rate limit changes; SDK and API releases sequenced correctly.

**Infrastructure and platform changes**: often affect everything at once. Check: change applied to a non-production environment of the same shape first; plan reviewed (for infrastructure-as-code, the actual diff of resources to be replaced or destroyed); capacity headroom; maintenance window and communication if there is downtime; rollback that does not depend on the thing being changed (e.g. you can still reach the deploy system if the network change fails).

**Data pipelines and analytics**: failures are often silent and delayed. Check: backfill plan and duration; downstream consumers notified of schema changes; data quality checks after the first run; ability to reprocess from source.

**ML models and LLM features**: behaviour changes without code changes. Check: evaluation results on representative and adversarial sets for the exact model version and prompts being released; comparison with the current version; guardrails and fallbacks; cost and latency at expected volume; monitoring of output quality, not just uptime. See `llm-evaluation`.

**Pricing, billing and money movement**: errors are costly and erode trust. Check: calculations compared against real historical data; reconciliation after release; customer communication; refund and correction process ready.

**Notifications and communications**: emails, SMS and push are irreversible and can reach every user in minutes. Check: content and targeting reviewed; send to an internal or small cohort first; rate limits; unsubscribe and preference handling; a stop mechanism.

**Compliance-sensitive changes** (personal data, health, payments, regulated regions): check whether a privacy, security or legal review is required by policy, and that it happened before the release, not after.

## Worked example of a readiness call

A team wants to release on Thursday: a new search backend replacing the old one, plus twelve small UI fixes.

- **Risk characterisation**: search is used on most sessions (high exposure); the new backend is new technology for the team (novelty); rollback is a config switch back to the old backend, which keeps running (reversible); the index is rebuilt from the database (no irreversible data step). The UI fixes are low risk.
- **Top risks**: relevance worse for common queries; latency under peak load; index lagging behind writes so new items do not appear.
- **Evidence found**: relevance compared on the top 500 real queries, with reviewed differences (good); load test at 1.5x peak passed at p99 within target (good); index lag measured in staging only, with no production alert (gap).
- **Known issues**: special characters in queries return no results (affects about 0.3% of searches, workaround is rephrasing; product owner accepts it, fix planned next sprint).
- **Rollback**: config switch, tested in staging, takes two minutes; on-call can trigger it.

Recommendation: *go with conditions*. Ship the UI fixes normally. Enable the new backend for 10% of traffic on Thursday with an index-lag alert added first; promote to 50% then 100% over the following days if relevance complaints, zero-result rate and p99 latency stay within the agreed bounds. Accepted known issue recorded with its owner. Not checked: behaviour for the non-English locales, which have low traffic; flagged as a follow-up before promoting beyond 50%.

## Pitfalls

- **Checklist theatre**: ticking generic items while the specific risk of this release goes unexamined.
- **Testing a different build**: tests passed on a branch, but the release build includes extra or different commits.
- **Untested rollback**: a rollback plan that has never run, or that fails after the migration.
- **Ignoring irreversibility**: treating a data migration or customer email like a code deploy.
- **Monitoring that cannot see the risk**: green dashboards while the bug silently corrupts data.
- **Known issues without owners**: listed in a document nobody reads.
- **Deadline pressure overriding evidence**: the date becomes the only criterion. Make the trade-off explicit and recorded instead.
- **Big-bang batching**: delaying many small releases into one large, risky one.
- **People not ready**: support learning about the change from customers; on-call not informed.
- **No defined rollback triggers**: teams wait for certainty while impact grows.
- **Declaring victory at deploy**: the release is not done until it is verified in production.

## Quality bar and verification

A readiness assessment is complete when:

- The release's actual contents are known and match the intended scope.
- Top risks are written down specifically, and every check traces to one of them.
- Each top risk has evidence of control, a detection mechanism, and a response.
- Tests have passed on the exact build being released; skipped or quarantined tests in risky areas are called out.
- Every known shipping issue has severity, impact, workaround and a named accepter.
- Irreversible steps are identified, rehearsed, backed up, and separately gated.
- Rollback is specific, feasible after migrations, and has defined triggers and an owner.
- Rollout strategy matches the risk, with promotion criteria.
- Monitoring covers the top risks, and someone is assigned to watch.
- Docs, support, on-call and stakeholders are prepared.
- There is an explicit recommendation and a recorded decision by the person with authority, including what was not checked.

## Related skills

- `release-management` — the process, versioning and mechanics of releases.
- `qa-test-planning`, `testing-strategy`, `end-to-end-testing` — building the test evidence.
- `database-migrations` — safe schema and data changes.
- `observability` — making failures visible.
- `ci-cd-pipelines` — deployment, canaries and automated rollback.
- `incident-response` — when the release goes wrong.
- `postmortem` — learning from a release that went badly.
