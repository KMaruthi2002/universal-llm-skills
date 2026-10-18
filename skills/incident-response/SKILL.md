---
name: incident-response
description: >-
  Handle a live production incident from first alert to resolution:
  confirming impact, declaring and classifying severity, assigning roles
  (incident commander, operations, communications), communicating with
  stakeholders and customers, mitigating before diagnosing (rollback,
  failover, feature-flag off, scaling, shedding load), keeping a timeline,
  handing over between responders, and handing off to a postmortem. Use when
  something is down, broken, or degraded in production right now, an alert
  has fired, users are reporting errors or outages, a deploy just broke
  something, data may be corrupted or leaking, or someone asks for help
  running or setting up an incident process and on-call. Not for the
  after-the-fact analysis (see postmortem) or for ordinary bug fixing.
metadata:
  category: devops
  related: observability, postmortem, root-cause-analysis, debugging, release-management, kubernetes, ci-cd-pipelines, business-communication
---

# Incident Response

An incident is an unplanned event that is hurting, or about to hurt, users or the business, and needs a coordinated response now. The goal during an incident is narrow: **restore service safely and quickly, keep people informed, and preserve enough information to learn from it later.** Understanding the root cause is a goal of the postmortem, not of the incident — and confusing the two is the most common reason outages last longer than they should.

This skill serves two situations: (a) you are helping with a live incident right now, and (b) you are helping someone design an incident process or on-call practice. The live path comes first.

## Scope

Covers: detection and triage, declaring incidents and severity, roles, communication, mitigation strategies, decision-making under uncertainty, timelines, handover, closing, security and data incidents (initial handling), and setting up the process.

Hands off to:

- Writing the postmortem and follow-ups → `postmortem`.
- Deep causal analysis after stabilisation → `root-cause-analysis`, `debugging`.
- Improving detection for next time → `observability`.
- Deploy/rollback mechanics → `ci-cd-pipelines`, `release-management`, `kubernetes`.

## If an incident is happening now: the first ten minutes

When the user indicates something is broken in production right now, move to this mode immediately. Be calm, concise, and structured. Ask few questions and only ones that change the next action.

1. **Confirm impact.** What are users experiencing? Since when? How many/which users, regions, features? Is it getting worse? Check the symptom-level signals: error rates, latency, synthetic checks, support tickets, status of upstream providers. Distinguish "an alert fired" from "users are affected".
2. **Declare.** If users are affected or likely to be, declare an incident in whatever way the organisation does (incident channel, tool command, page the on-call). Declaring early is cheap; declaring late is costly. It is fine to downgrade or close a false alarm.
3. **Assign an incident commander (IC).** One person coordinates. In a tiny team the IC may also be the person fixing it, but name the role anyway and hand off the hands-on work as soon as a second person arrives.
4. **Set severity** (see below) to decide who else to pull in and how often to communicate.
5. **Ask: what changed?** Recent deploys, config changes, feature-flag flips, infrastructure changes, dependency or provider incidents, traffic spikes, certificate or credential expiry, scheduled jobs. Most incidents follow a change. Check deploy markers on dashboards, change logs, and provider status pages.
6. **Mitigate first.** If a recent change correlates with the start of impact, roll it back or disable it now, before proving it was the cause. Other mitigations below.
7. **Communicate.** Post a first status update in the incident channel and, for customer-facing impact, on the status page — within minutes, even if it only says "we are investigating elevated errors on checkout; next update in 30 minutes".
8. **Start the timeline.** Note times (with time zone) of detection, declaration, key observations, actions, and their effects.

## Core principles

**1. Mitigate before you diagnose.** Restoring service is the priority; the cause can be understood afterwards from logs, metrics, and preserved state. A rollback that turns out unnecessary costs minutes; an hour of investigation while customers are down costs far more. "Stop the bleeding, then find the wound."

**2. One coordinator, clear roles.** Incidents fail through confusion — three people restarting different things, nobody updating stakeholders, two engineers applying conflicting fixes. A single incident commander who coordinates (rather than debugging) keeps the response coherent.

**3. Prefer reversible, low-risk actions.** Under stress, people make mistakes. Choose actions you can undo (rollback, flag off, failover, scale up) over irreversible ones (deleting data, rebuilding clusters, schema changes). Announce each action before taking it, and observe its effect before taking the next.

**4. Change one thing at a time where possible.** Simultaneous changes make it impossible to tell what helped or hurt. Exception: when impact is severe and several low-risk mitigations are clearly independent.

**5. Communicate on a schedule, even with no news.** Silence makes stakeholders anxious and leads to interruptions of responders. Regular, predictable updates ("next update at 14:30") buy responders focus.

**6. Blameless and factual.** The incident is about systems and decisions with the information available at the time. Blame makes people hide information, which slows the current response and poisons the postmortem.

**7. Preserve evidence.** Before restarting, recreating, or wiping things, capture what you can cheaply: logs, a heap/thread dump, the failing pod's description, the bad config. Do not let evidence-gathering delay mitigation in a severe incident, but take the 30 seconds when you can.

## Discovering context

Live or not, find and follow what the organisation already has before inventing anything:

- **Incident process documents:** severity definitions, declaration mechanism (chat command, incident tool, paging service), required roles, communication templates and approvers.
- **Runbooks** for the affected service, linked from alerts or kept in the repository or wiki; read them before improvising.
- **Ownership:** service catalogue or code-owner files that say which team owns the failing component, and their escalation path.
- **Where the signals are:** dashboards, log search, tracing, deploy history, feature-flag audit log, infrastructure change log, provider status pages.
- **Communication channels:** status page tool, customer-support liaison, executive notification rules, regulatory obligations for the industry.

If none of this exists and an incident is live, do not stop to design it; use the defaults in this skill and note the gaps for the postmortem.

## Severity

Use the organisation's definitions if they exist. If not, a common scale:

| Severity | Typical definition | Response |
|---|---|---|
| SEV1 / critical | Core service down or severely degraded for many users; data loss or security breach in progress; major revenue impact | All hands as needed; IC + comms lead; exec notification; customer comms; updates every 15–30 min |
| SEV2 / major | Significant feature broken or degraded; subset of users heavily affected; workaround may exist | On-call plus relevant owners; IC; customer comms if visible; updates every 30–60 min |
| SEV3 / minor | Limited impact, minor feature, small subset of users; or risk of escalation | Owning team handles during working hours; internal updates |
| SEV4 / low | No current user impact; near-miss or cosmetic | Ticket; may still merit a brief review |

Guidance: when unsure between two levels, choose the higher one; it is easy to downgrade. Severity is about impact, not about how hard the fix is. Re-evaluate as the picture changes.

## Roles

| Role | Responsibility | Not responsible for |
|---|---|---|
| Incident commander (IC) | Coordinates, decides, assigns work, keeps the big picture, calls for help, decides when to escalate or close | Hands-on debugging (in larger incidents) |
| Operations / subject-matter lead(s) | Investigate and execute mitigations, report findings and planned actions to IC | External communication |
| Communications lead | Status page, customer and stakeholder updates, support team liaison | Technical decisions |
| Scribe | Keeps the timeline and records decisions and actions | — |
| Liaisons (as needed) | Vendor/provider contact, legal, security, customer success for key accounts | — |

In small teams one person may hold several roles. The point is that each responsibility has a named owner. The IC can and should hand off the IC role if they get pulled into deep technical work or need rest.

## Mitigation toolbox

Ordered roughly from least to most risky; choose based on what changed and what the evidence suggests.

| Mitigation | When | Watch for |
|---|---|---|
| Roll back the last deploy | Impact started near a deploy | Database migrations that the old version cannot handle; rolling back mobile clients is impossible |
| Disable a feature flag / kill switch | New feature correlated with impact | Flag dependencies; partial disablement |
| Revert a config change | Config/infra change correlated | Cached config; need to restart to pick up |
| Fail over (zone, region, replica, provider) | Infrastructure or regional failure | Replication lag (data loss), capacity in target, DNS TTLs, split-brain |
| Scale out / up | Saturation from load | Downstream limits (database connections); cost; scaling the wrong tier |
| Shed load / rate limit / degrade gracefully | Overload; protecting core paths | Which traffic to sacrifice; communicate degradation |
| Block abusive traffic | Attack or runaway client | False positives blocking real users |
| Restart / recycle instances | Memory leak, wedged process, bad local state | Destroys evidence; can cause thundering herd; only buys time |
| Drain a bad node or instance | Single host misbehaving | Ensure enough capacity remains |
| Pause queues, jobs, or consumers | A job is corrupting data or overloading a dependency | Backlog to process later; ordering |
| Disable an integration | Third-party dependency failing and cascading | Feature loss; reconcile later |
| Hotfix forward | No safe rollback (e.g. migration already ran) and the fix is small and clear | Rushed code; see `release-management` hotfix process |

When rollback is impossible or risky (destructive migration, external side effects already sent), say so explicitly and choose forward mitigation deliberately.

## Rollback or fix forward?

| Factor | Favours rollback | Favours fix forward |
|---|---|---|
| Correlation with a recent change | Strong | None, or the change is long past |
| Reversibility | Previous artifact available and compatible | Migration or external side effects make the old version unsafe |
| Fix clarity | Cause unclear | Cause certain and the fix is a few lines, reviewed |
| Deploy speed | Rollback is fast (minutes) | Rollback is as slow as a forward deploy |
| Blast radius of the fix | — | Fix is isolated and can be flagged |

Default to rollback when in doubt. "We know what it is, the fix is quick" is said in many incidents that then last two more hours.

## Common incident patterns

| Pattern | Signature | First mitigations |
|---|---|---|
| Bad deploy | Errors start minutes after a release; only new version's instances fail | Roll back; halt the pipeline |
| Bad config or flag change | Sudden change with no deploy; correlates with a config/flag audit entry | Revert config; turn the flag off |
| Dependency outage | Timeouts or errors on calls to one dependency; their status page may confirm | Fail over, degrade gracefully, serve cached data, disable the integration |
| Retry storm / cascading failure | Load multiplies as clients retry; a small slowdown becomes total failure | Shed load, rate limit, disable retries or add backoff, scale the bottleneck carefully |
| Thundering herd after recovery | Service recovers then falls over again as all clients reconnect | Ramp traffic back gradually, jittered reconnects, warm caches |
| Capacity exhaustion | Saturation metrics at 100%: connections, threads, disk, memory, quotas | Scale, free space, raise quotas, stop the heaviest consumer |
| Certificate or credential expiry | Abrupt TLS or auth failures at a specific time | Renew/rotate; then add expiry monitoring |
| DNS problem | Resolution failures, partial reachability by region or network | Revert DNS change; mind TTLs; use known-good resolvers |
| Data corruption by a job | Wrong data appearing, often without errors | Stop the writer; assess scope; restore or repair from backups |
| Traffic spike or abuse | Request rate far above baseline from specific sources or patterns | Rate limit, block, cache, scale |
| Time-based bugs | Failures at midnight, month end, DST change, leap day | Disable the job or path; fix forward |

## Diagnosis during the incident

Diagnose only as much as needed to choose a mitigation:

- Start from the symptom and narrow scope: which endpoints, regions, customers, versions, hosts? Is it all traffic or a segment? Segmentation often points straight at the cause (one region → infrastructure; one version → deploy; one customer → data or usage pattern).
- Follow a trace or request ID through the system to find where errors originate (see `observability`).
- Look for saturation: connection pools, thread pools, queue depth, CPU throttling, disk, rate limits from providers.
- Check dependencies' health and status pages, but do not assume a provider is at fault without evidence; status pages lag.
- Form hypotheses explicitly and test the cheapest first. State them in the channel: "Hypothesis: the new connection pool size exhausts DB connections. Test: check DB connection count vs. limit."
- Timebox. If a line of investigation has not produced a mitigation in 15–30 minutes during a SEV1, step back and consider broader mitigations (rollback, failover) or more help.

## Decisions under uncertainty

Incidents force decisions with incomplete information. Useful habits for the IC:

- **Make the decision explicit.** "We are choosing between failing over to region B (risk: ~2 minutes of replication lag lost) and waiting for the provider (unknown duration). Decision: fail over at 15:20 unless the provider's ETA is under 15 minutes." Explicit decisions can be challenged and recorded.
- **Weigh cost of delay.** Every minute of SEV1 has a cost; compare it with the risk of the mitigation, not with an imaginary risk-free option.
- **Set decision deadlines.** "If error rate has not dropped by 14:45, we roll back the database parameter change too."
- **Invite dissent briefly,** then commit. Responders who see a risk must say so; once the IC decides, everyone executes that plan.
- **Know when to escalate:** pull in more help or a more senior IC when impact is growing, the cause is unclear after the first timebox, multiple teams are involved, or customer, legal, or security implications appear. Escalating early is a strength, not an admission of failure.

## Escalation and paging others

- Page the owning team of a suspected component directly rather than waiting for their alerts to fire.
- Give paged people a one-line summary and a link to the channel, so they arrive with context.
- Contact providers through their support channels with incident identifiers, timestamps, affected resource IDs, and regions; open the case early, since response times vary by support tier.
- Release people who are not needed, so they can rest for later shifts.

## Communication

**Internal (incident channel):**

- One dedicated channel or bridge per incident. Keep it for the incident; side discussions go elsewhere.
- IC posts regular summaries: current impact, what we know, what we are doing, next update time.
- Responders announce actions before taking them ("Rolling back api to v1.42 in prod now") and results after.

**Stakeholders and customers:**

- Status page and customer messages state: what is affected, from users' point of view; when it started; that the team is working on it; workarounds if any; time of next update. Avoid speculation about cause, blame on vendors, or promises of exact resolution times.
- Update at the promised time even if nothing changed.
- When resolved: confirm resolution, describe impact window, and say whether a follow-up report will be published.
- Coordinate with support so they can answer customers consistently.
- Wording for regulated or security events needs legal/security review; do not publish details about vulnerabilities or breaches without it.

An illustrative first customer update: "We are investigating increased errors when completing checkout, starting around 14:05 UTC. Some customers may be unable to place orders. Our team is actively working on it. Next update by 14:45 UTC." Adapt to the organisation's voice and channels.

## Timeline

Keep a running, timestamped log (UTC or a single stated time zone):

- First signal (alert, customer report) and when it was noticed.
- Declaration, severity changes, people paged and joined.
- Observations and hypotheses.
- Every action taken, by whom, and its observed effect.
- Communication sent.
- Mitigation time (impact stopped) and resolution time (fully back to normal).

This is the raw material for the postmortem and for metrics like time to detect, time to mitigate, and time to resolve. Capturing it live is far more accurate than reconstructing it from memory.

## Handover

Long incidents require shifts: fatigue degrades judgment within hours. Hand over deliberately:

- Outgoing IC summarises: current impact and severity, timeline highlights, what has been tried and the results, current hypotheses, actions in progress, pending decisions, communication schedule, and who is involved.
- Incoming IC confirms understanding and announces in the channel that they now hold the role.
- Write the summary in the channel, not only verbally, so everyone has the same picture.

## Resolving and closing

- **Mitigated** (impact stopped) is not **resolved** (system back in a normal, stable state with temporary measures removed or tracked). Do not close at mitigation if the system is fragile (e.g. running on a manual workaround, half capacity, or with a disabled safety mechanism).
- Before closing: confirm metrics are back to baseline for a reasonable period, temporary mitigations are documented (and either made permanent deliberately or scheduled for removal), and any data repair needed is identified.
- Send the final internal and external updates.
- Schedule the postmortem (usually within a few working days for SEV1/SEV2) and assign an owner. Capture obvious follow-ups immediately as tickets while memory is fresh. See `postmortem`.

## Security and data incidents

Incidents involving breaches, leaked credentials, data exposure, or data corruption have extra rules:

- **Involve the security team (and legal/privacy) immediately**, per the organisation's process. There may be legal notification deadlines (some regulations require notifying authorities within 72 hours of becoming aware of certain personal-data breaches).
- **Preserve evidence** more carefully: snapshots, logs, access records. Avoid wiping compromised systems before forensics if it can be avoided safely.
- **Contain:** revoke and rotate exposed credentials, block attacker access, isolate affected systems. Rotating a leaked secret is almost always the right first move.
- **Restrict communication** to need-to-know channels; do not discuss details in broad public channels or on the status page until approved.
- **Data corruption:** stop the writer first (pause jobs, disable the feature) so the damage stops growing; then assess scope from backups and logs; repair carefully with reviewed scripts on copies first. Point-in-time recovery may be needed; restoring over production is irreversible and must be confirmed.

## When you (the assistant) are helping in a live incident

- Keep messages short and actionable. Lead with the next step.
- Ask for the information that most narrows the problem: what is the symptom, since when, what changed, what do dashboards show.
- Propose mitigations with their risk and reversibility, and let the human decide and execute in production unless they explicitly ask you to run a specific command and you have confirmed the target.
- **Never run destructive or production-changing commands** (rollbacks, restarts, failovers, deletes, data fixes, scaling) without explicit confirmation naming the system and action. Prefer read-only investigation commands.
- Never ask for or echo credentials in the conversation; if a secret appears in logs or output, flag it for rotation.
- Keep a timeline for the user if no one else is.
- Watch for responder fatigue and suggest handover or escalation if the incident drags on.
- After mitigation, remind about preserving evidence, closing temporary measures, and scheduling the postmortem.

## Setting up an incident process and on-call

If the user is designing the practice rather than in an incident:

- **Define severities** with concrete, impact-based examples for their product.
- **On-call rotation:** at least 4–6 people per rotation for sustainability where possible (smaller rotations burn people out); clear primary/secondary; handoff ritual; compensation or time off in lieu per local norms and law.
- **Paging:** route by service ownership; escalation if not acknowledged (e.g. 5–15 minutes); make sure alerts are symptom-based and actionable (see `observability`).
- **Runbooks** for known failure modes, linked from alerts: symptoms, diagnosis steps, mitigations, escalation contacts. Keep them short and tested.
- **Tooling:** a way to declare an incident that creates a channel, pages the right people, and starts a timeline; a status page; a single place to find dashboards.
- **Practice:** game days and incident simulations, rollback drills, failover tests. The first time someone acts as IC should not be during a real SEV1.
- **Metrics:** count of incidents by severity, time to detect/mitigate/resolve, pages per shift, and follow-up completion rate. Use them for learning, not for blaming teams.

## Worked example: errors after a Friday deploy

14:02 UTC, a burn-rate alert pages for checkout errors at 6%. The on-call engineer confirms user impact on the dashboard and declares a SEV2, taking the IC role, and pulls in a second engineer for hands-on work.

The deploy marker shows a release at 13:55. Errors are only on instances running the new version. The IC decides to roll back without further diagnosis, announces it in the channel, and posts the first status update. The rollback completes at 14:11; errors fall to baseline by 14:14. The IC keeps the incident open for 20 minutes of observation, then marks it mitigated.

During observation the second engineer finds, from preserved logs of a failed request, that a new payment client library times out at 2 seconds instead of 10. The pipeline is paused for this service until a fix with a test lands. The incident is resolved at 14:40, the customer update says what was affected and for how long, and a postmortem is scheduled with an owner. One follow-up already looks clear: canary analysis would have caught this at 5% of traffic.

The reasoning to copy: confirm impact, declare, notice the correlated change, roll back before proving cause, communicate, observe before closing, and let diagnosis continue calmly after users are safe.

## After the incident: what to hand to the postmortem

The postmortem (see `postmortem`) goes faster and is more accurate when the incident leaves behind:

- The timeline with timestamps, actions, and observed effects.
- Links to the dashboards, queries, and traces that were used, with the time ranges.
- The incident channel transcript and any customer communications sent.
- A list of what helped (runbooks, alerts, tools) and what got in the way (missing access, confusing dashboards, slow rollbacks).
- Impact figures: duration, affected users or requests, failed transactions, data affected, SLO budget consumed.

## Pitfalls and anti-patterns

- **Debugging while the site is down** instead of rolling back the obvious recent change.
- **No IC,** or the IC deep in a terminal while nobody coordinates.
- **Hero mode:** one person trying to fix everything alone without declaring.
- **Too many cooks:** many people taking uncoordinated actions.
- **Going silent** with stakeholders for long stretches.
- **Restarting everything** repeatedly, destroying evidence and only buying minutes.
- **Closing at mitigation** with fragile workarounds left undocumented.
- **Making irreversible changes under pressure** (deleting data, force-pushing, dropping tables) without a second pair of eyes.
- **Assuming the vendor is at fault** without evidence, delaying internal investigation — or the reverse, ignoring a provider outage.
- **Skipping the postmortem** for incidents that "were just a bad deploy"; repeated "just a bad deploy" is a pipeline problem.
- **Blame,** which suppresses information.

## Quality bar and verification

During and after an incident, check:

- [ ] Impact was confirmed and scoped from user-facing signals.
- [ ] An incident was declared with a severity and a named IC.
- [ ] Mitigation was attempted promptly, with reversible actions preferred and each action announced.
- [ ] Communication went out early and on schedule internally and, where needed, externally.
- [ ] A timestamped timeline exists covering detection, actions, and effects.
- [ ] Service is back to baseline; temporary mitigations are documented and tracked.
- [ ] Evidence is preserved; secrets possibly exposed were rotated.
- [ ] A postmortem is scheduled with an owner; immediate follow-ups are ticketed.

When reporting back to the user, state current status (investigating / mitigated / resolved), impact window, actions taken and their effect, open risks, and what remains to be done.
