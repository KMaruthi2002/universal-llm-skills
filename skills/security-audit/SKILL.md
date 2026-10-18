---
name: security-audit
description: >-
  Assess an existing system, application, codebase or deployment for security
  weaknesses within an authorised scope, and report them responsibly. Covers
  scoping and rules of engagement, threat modelling (STRIDE and similar as
  lenses), attack surface and trust boundary mapping, dependency and secret
  scanning, authentication and authorisation review, data flow and storage
  review, configuration and infrastructure checks, confirming findings without
  false positives, severity rating with CVSS-like reasoning, and writing
  findings with remediation. Use when asked to "audit the security of",
  "find vulnerabilities in", "threat model", "pentest-style review",
  "check this repo for security issues", or to prepare for a security
  assessment or compliance review. Not for writing secure new code
  (secure-coding), reviewing a single change (code-review), or responding to
  an active breach (incident-response).
metadata:
  category: quality
  related: secure-coding, authentication-and-authorization, dependency-management, code-review, architecture-review, infrastructure-as-code, cloud-architecture, incident-response, api-design, observability
---

# Security Audit

A security audit answers: **how could this system be made to do something its owners do not want, how likely and how damaging is that, and what should be done about it?** The deliverable is a set of confirmed, prioritised findings with enough evidence and remediation guidance for the owners to act, plus an honest statement of what was and was not examined.

Scope of this skill: assessing something that already exists (code, a running service, infrastructure, configuration). For building securely from the start, see `secure-coding`. For reviewing one change, see `code-review`. For evaluating a proposed design, see `architecture-review` (and use the threat-modelling section here). If an attack is happening now, stop auditing and switch to `incident-response`.

## Authorisation and safety first

Security testing that is not authorised can be illegal and harmful, even with good intentions. Before doing anything active:

- **Confirm authorisation and scope in writing (or in the conversation with the user, for their own systems).** Which systems, environments, repositories, accounts and techniques are in scope? Who owns them? Third-party services (cloud providers, SaaS, payment processors) usually have their own testing policies; the system owner cannot authorise testing of infrastructure they do not own.
- **Prefer passive and white-box methods.** Reading code and configuration, running scanners against a local checkout, and reviewing a staging environment carry far less risk than probing production.
- **Never test production destructively** (load, fuzzing that writes data, exploiting injection to modify records) without explicit agreement on timing, blast radius and rollback.
- **Minimise data exposure.** If you encounter real personal data, credentials, or secrets, do not copy, exfiltrate, or display more than needed to prove the finding. Redact in reports (show a prefix or hash, not the secret).
- **Treat found credentials as compromised** and tell the owner promptly so they can rotate them; do not use them to go further unless that use is explicitly in scope.
- **Stop and escalate** if you find evidence of an existing compromise, or a critical issue being actively exploitable from the internet. That is no longer an audit timeline.
- **Report only to the authorised owner** through the agreed channel. Never publish, post publicly, or send vulnerability details to anyone else.

If you are an agent: do not run network scanners, exploit attempts, or tools that send traffic to systems outside the local environment unless the user has explicitly authorised that target and technique. Static review and local tooling are the default.

## Core principles

**1. Think like an attacker, report like an engineer.** Finding issues needs adversarial creativity: what can I control, what is trusted that should not be, what happens if I do things out of order? Reporting needs precision: reproducible evidence, realistic impact, and a fix.

**2. Model before you scan.** Scanners find known patterns; they cannot tell you that the refund endpoint trusts a client-supplied price. A threat model of what matters (assets, actors, trust boundaries) tells you where to look and what severity a finding really has.

**3. Trust boundaries are where bugs live.** Every place data or control crosses from less-trusted to more-trusted (browser to server, tenant to shared service, public queue to internal worker, user upload to parser) is where validation, authentication and authorisation must happen. Map them explicitly.

**4. Severity is impact times exploitability in context.** The same missing header is trivial on an internal status page and serious on a login page. Rate findings against this system's assets and exposure, not a generic list.

**5. A false positive is a cost, not a safe default.** Unconfirmed findings waste remediation effort, bury real issues, and destroy the report's credibility. Confirm, or label clearly as unconfirmed with what would confirm it.

**6. Absence of findings is not proof of security.** Report coverage honestly. "No issues found in the authentication module; payment integration and the mobile app were not reviewed" is a useful result. "No issues found" without coverage is a dangerous one.

**7. Fit the owners' context.** Respect their risk appetite, compliance obligations, existing security tooling and conventions. Recommend fixes that fit their stack and patterns, not a rewrite into your preferred one.

## Process overview

1. Scope and rules of engagement.
2. Understand the system: purpose, users, assets, architecture.
3. Threat model: actors, trust boundaries, STRIDE-style enumeration.
4. Map the attack surface.
5. Automated sweeps: dependencies, secrets, static analysis, configuration.
6. Manual review of high-risk areas: authentication, authorisation, input handling, data flows, business logic, infrastructure.
7. Confirm each finding; rate severity.
8. Report; support remediation; retest.

Time-box each phase to the scope. A one-day review of a small service does steps 2–4 in an hour and spends most of the day in 6. A broad assessment of a platform might spend days on 2–4 alone.

## Step 1 — Scope

Agree on:

- **Targets**: repositories, services, environments, cloud accounts, mobile apps, third-party integrations. Explicitly list what is out of scope.
- **Access**: source code (white-box), credentials for test accounts at each privilege level, architecture docs, read-only cloud console access, logs.
- **Techniques allowed**: static review only, or dynamic testing; against which environment; any limits on rate, timing or data modification.
- **Goals and concerns**: compliance requirement, recent incident, upcoming launch, a specific worry ("can one tenant see another's data?"). These shape where depth is spent.
- **Reporting**: format, recipients, channel for urgent findings, confidentiality.

## Step 2 — Understand the system

You cannot judge impact without knowing what the system is for. Establish:

- **Assets**: what would hurt to lose, leak, or have tampered with? Customer personal data, credentials, money movement, intellectual property, availability of a critical function, the integrity of audit logs, signing keys.
- **Actors**: anonymous internet users, registered users, paying customers, tenants, administrators, support staff, internal services, CI systems, third-party integrations, and malicious insiders.
- **Architecture**: components, data stores, external dependencies, how requests flow, where secrets live, how deployment works. Draw it (even roughly) if no diagram exists; the act of drawing reveals unknown connections.
- **Existing controls**: authentication provider, WAF, rate limiting, secret manager, encryption at rest, logging and alerting, security review processes.

Use `explore-codebase` techniques to find entry points: route definitions, controllers, message consumers, scheduled jobs, CLI commands, webhooks, and infrastructure definitions.

## Step 3 — Threat model

A threat model is a structured way to enumerate what could go wrong. Frameworks are lenses for completeness, not forms to fill in. Use whichever helps; the project may already have one.

**STRIDE**, applied to each component and each trust-boundary crossing:

| Threat | Property violated | Question to ask | Typical findings |
|---|---|---|---|
| Spoofing | Authentication | Can someone pretend to be another user or service? | Weak login, missing service-to-service auth, unsigned webhooks, forgeable tokens |
| Tampering | Integrity | Can someone modify data or code they should not? | Mass assignment, unsigned client-side state, writable storage buckets, CI pipeline injection |
| Repudiation | Non-repudiation | Can someone act and later deny it? | Missing audit logs, logs users can alter, shared accounts |
| Information disclosure | Confidentiality | Can someone read what they should not? | IDOR, verbose errors, public buckets, secrets in repos, over-broad API responses |
| Denial of service | Availability | Can someone degrade or stop the service? | Unbounded uploads or queries, regex blowups, missing rate limits, expensive unauthenticated endpoints |
| Elevation of privilege | Authorisation | Can someone gain rights they should not have? | Missing role checks, path traversal to config, deserialisation to code execution, container escape |

Other useful lenses:

- **Attacker goals** ("steal customer data", "get free product", "take over an admin account") and working backwards through attack trees. Good for business logic.
- **Abuse cases**: for each feature, how would a fraudster, a spammer, or a competitor misuse it?
- **Data lifecycle**: for each sensitive data type, where is it collected, stored, processed, transmitted, logged, backed up, exported and deleted?
- **Known weakness catalogues** (e.g. the OWASP Top 10 for web apps, OWASP API and mobile lists, CWE) as checklists after you have done the system-specific thinking, not instead of it.

Output of this step: a ranked list of the threats that matter most for this system, which determines where manual review effort goes.

## Step 4 — Attack surface mapping

List everything an attacker can reach or influence, and at what privilege:

- HTTP/RPC endpoints (including admin, debug, health, metrics, legacy and undocumented ones), GraphQL schemas, WebSockets.
- Authentication flows: login, signup, password reset, MFA, SSO callbacks, API key issuance, token refresh.
- File uploads and anything that parses complex formats (images, PDFs, archives, XML, office documents).
- Inbound integrations: webhooks, message queues, email ingestion, imports.
- Outbound requests driven by user input (URL fetchers, previewers, integrations): SSRF candidates.
- Client-side code and mobile apps (anything shipped to users is readable by attackers, including embedded keys).
- Infrastructure: exposed ports, storage buckets, management consoles, DNS records (dangling subdomains), CI/CD systems and their secrets, container registries.
- Supply chain: dependencies, build scripts, base images, third-party scripts loaded in the browser.
- People and process, if in scope: who can deploy, who holds admin, how access is revoked.

For each item note: who can reach it (anonymous, authenticated, internal), what it trusts, and what it can affect. High-reach, high-impact items get reviewed first.

## Step 5 — Automated sweeps

Run broad, cheap tooling early, but treat its output as leads to verify, not findings. Examples of categories (pick tools that fit the stack; the project may already run some in CI):

- **Dependency vulnerability scanning** (software composition analysis): ecosystem audit commands, lockfile scanners, container image scanners. Check whether the vulnerable code path is actually reachable and whether the vulnerable version is actually deployed before rating.
- **Secret scanning** across the full git history, not just the current tree: secrets removed in a later commit are still exposed. Also check CI logs, container images, client bundles, and config examples.
- **Static analysis (SAST)** for injection, unsafe APIs, and taint flows. Expect noise; triage by reachability from untrusted input.
- **Infrastructure-as-code and configuration scanners** for public storage, open security groups, missing encryption, over-broad IAM.
- **Dynamic scanning (DAST)** against a test environment, only if authorised.

Record versions and commands used, so results are reproducible and retestable.

Triage approach: group findings by root cause, discard confirmed false positives with a recorded reason, and carry the rest into manual review. Fifty "SQL injection" alerts that all come from one query builder misuse are one finding.

## Step 6 — Manual review of high-risk areas

This is where most real vulnerabilities are found. Prioritise by the threat model. Depth checklists for each area are in [references/review-checklists.md](references/review-checklists.md); read it when you reach this step.

### Authentication

- How are identities established (passwords, SSO, magic links, API keys, mTLS)? Is each path equally protected?
- Credential storage (slow, salted hashing for passwords), reset flows (token entropy, expiry, single use, no user enumeration), MFA bypasses (alternate login paths that skip it), session lifetime, invalidation on logout and password change, token validation (signature, algorithm, audience, expiry actually checked).
- Rate limiting and lockout on login, reset and OTP verification.
- Service-to-service authentication: do internal services trust anything on the internal network?

### Authorisation

Broken authorisation is consistently among the most common and most damaging classes. For each operation, ask: **is there a server-side check that this principal may perform this action on this specific object?**

- Object-level access (IDOR/BOLA): change an ID in a request; does it return someone else's data?
- Function-level access: can a regular user call admin endpoints directly?
- Tenant isolation in multi-tenant systems: is the tenant derived from the authenticated identity, or from client input? Are all queries scoped?
- Field-level: can a user set fields they should not (role, owner, price, status) via mass assignment?
- Consistency: is authorisation enforced in one central place, or re-implemented per endpoint (where it will eventually be forgotten)?
- Indirect paths: exports, search, reporting, background jobs, file download URLs, and caches often bypass the checks the main API has.

A practical white-box technique: list every endpoint or handler and, next to it, the authorisation check it performs (or "none"). Gaps become obvious.

### Input handling and injection

Trace untrusted input to dangerous sinks: database queries, shell commands, file paths, templates, HTML output, deserialisers, XML parsers, URL fetchers, log statements, LDAP and NoSQL queries, and LLM prompts that can trigger tools. For each source-to-sink path, is the data parameterised, encoded for the context, or validated against an allow-list?

### Data flow and storage

- Where does sensitive data go? Logs, analytics, error trackers, caches, backups, third parties, browser storage, URLs (which end up in logs and referrers).
- Encryption in transit (including internal hops) and at rest; key management (who can access keys, rotation).
- Data minimisation and retention: is data kept longer than needed, or collected without need?
- API responses: do they return more fields than the client needs?

### Business logic

Automated tools almost never find these. Look for:

- Workflows that can be executed out of order, skipped, or repeated (applying a discount twice, completing a checkout without paying, replaying a one-time action).
- Race conditions in balance, inventory and quota checks (check-then-act without locking).
- Client-side enforcement of server-side rules (prices, limits, feature gating).
- Negative, zero, huge, or fractional quantities.

### Infrastructure and configuration

- Default credentials, debug modes and admin consoles exposed; verbose error pages in production.
- Over-permissive IAM roles, wildcard policies, long-lived access keys, shared accounts.
- Network exposure: databases or caches reachable from the internet; flat internal networks.
- Security headers and cookie flags on web apps; TLS configuration.
- CI/CD: who can modify pipelines, whether untrusted pull requests can access secrets, whether build artifacts are signed or pinned.
- Logging and detection: would an attack on the findings above be noticed? (See `observability`.)

### LLM and agent features (if present)

Prompt injection from any untrusted content the model reads, tools the model can call with user-influenced arguments, data leakage between users through shared context or caches, and output rendered without encoding. See `ai-safety-and-guardrails`.

## Step 7 — Confirm and rate

### Confirming findings

For each candidate finding:

1. **Establish reachability**: can untrusted input actually reach the vulnerable code, through which entry point, with what privilege?
2. **Check for compensating controls**: framework auto-escaping, middleware auth, WAF rules, network isolation, input validation upstream. A real control lowers severity; a bypassable one does not.
3. **Reproduce safely** where authorised: a proof of concept in a test environment, with harmless payloads (read your own test record, not a real user's; use a marker string, not a destructive command).
4. **If you cannot confirm**, keep it but label it clearly as "potential" or "needs verification", with what evidence would confirm or rule it out.
5. **Find the root cause**: one missing central check may explain ten symptom-level findings; report the root cause and list instances.

### Rating severity

Use the owner's scheme if they have one. Otherwise, reason through the factors that frameworks like CVSS formalise, then adjust for context:

| Factor | Lowers severity | Raises severity |
|---|---|---|
| Attack vector | Requires physical or local access | Reachable from the internet |
| Privileges required | Admin only | Anonymous |
| User interaction | Victim must take unusual steps | None needed |
| Complexity | Needs rare conditions, race timing, or insider knowledge | Reliable, scriptable |
| Scope | Contained to the vulnerable component | Crosses tenants, escapes to host, pivots to other systems |
| Confidentiality / integrity / availability impact | Low-value data, minor degradation | Sensitive data at scale, money, code execution, full outage |
| Context (not in base scores) | Compensating controls, low asset value | Regulated data, known active exploitation, high-value target |

Typical bands (illustrative, adjust to context):

- **Critical**: remote, unauthenticated (or trivially authenticated) compromise of sensitive data at scale, code execution, or full account takeover. Act immediately.
- **High**: serious impact with some precondition (authenticated user, specific configuration), e.g. cross-tenant data access by any customer.
- **Medium**: limited impact or significant preconditions; e.g. stored XSS on a low-traffic admin page, user enumeration.
- **Low**: minor information leakage, defence-in-depth gaps, hardening issues.
- **Informational**: observations and best-practice notes with no direct exploit path.

Be explicit about the reasoning behind each rating ("High: any authenticated customer can read other customers' invoices by changing the ID; no compensating control") so owners can disagree on facts rather than labels. Do not inflate severity to get attention; it devalues the whole report.

## Step 8 — Report and remediation

A good report lets each audience act:

- **Executive summary**: overall posture, the few findings that matter most, and the top recommendations, in plain language.
- **Scope and method**: what was examined, how, when, with what access, and **what was not covered**.
- **Findings**, ordered by severity, each with: a clear title, affected component and location, description, evidence (redacted), reproduction steps, impact in this system's terms, severity with reasoning, remediation (specific to their stack, with the root-cause fix preferred over the symptom patch), and references (e.g. CWE identifiers) where useful.
- **Positive observations**: controls that work well, so they are kept.
- **Systemic recommendations**: patterns across findings (e.g. "authorisation is re-implemented per endpoint; centralise it") that prevent the next batch.

Responsible handling:

- Report critical findings immediately through the agreed urgent channel; do not hold them for the final report.
- Keep the report confidential and shared only with authorised recipients; it is a map for attackers.
- Never include live secrets or real personal data in the report.
- For vulnerabilities in third-party software found during the audit, follow coordinated disclosure: report to the vendor or maintainer through their published channel, with the owner's agreement, and give them reasonable time to fix before any wider disclosure.
- Offer a retest of fixed findings and record the result; a fix that addresses one instance but not the root cause should be reopened.

## Discovering context

Before and during the audit, look for and respect:

- Existing threat models, security policies, previous audit reports and their open findings, bug bounty reports.
- Security tooling already in place (CI scanners, dependency bots, secret scanning) and its configuration and suppressions. Suppressions are worth reviewing: they are sometimes justified and sometimes hiding real issues.
- Compliance requirements (e.g. payment card, health, privacy regulations) that change which findings are mandatory to fix.
- The team's stack and patterns, so remediation advice uses their framework's mechanisms.

## Pitfalls

- **Scanner dump as report**: pasting tool output without triage. Owners drown, real issues are missed, credibility drops.
- **Checklist without model**: running through a generic list and missing the system-specific business logic flaw that matters most.
- **Severity by category**: rating "XSS = High" without context of where it is and who can trigger it.
- **Unconfirmed findings presented as fact**.
- **Missing the indirect paths**: auditing the main API carefully while exports, admin tools, background jobs and old API versions bypass its checks.
- **Ignoring git history**: secrets "removed" in a later commit are still exposed.
- **Ignoring the supply chain and CI**: the pipeline that can deploy to production is often less protected than production.
- **Scope drift into unauthorised targets**: following a link into a third-party system, or testing production when only staging was authorised.
- **Handling sensitive data carelessly**: copying real secrets or personal data into notes, tickets, or reports.
- **Silent coverage gaps**: implying the whole system was reviewed when only part was.
- **Over-rotation on exotic issues** while basic hygiene (patching, MFA for admins, least privilege) is missing.

## Quality bar and verification

The audit is done when:

- Scope and authorisation are documented, and nothing outside them was touched.
- The threat model identifies assets, actors and trust boundaries specific to this system, and review depth followed it.
- Every finding is either confirmed with evidence or clearly labelled as unconfirmed with what would confirm it.
- Every severity has written reasoning grounded in this system's context.
- Every finding has actionable remediation fitting the owners' stack, with root causes identified.
- Coverage gaps are stated explicitly.
- No secrets or real personal data appear in the report; exposed credentials were reported for rotation.
- Critical issues were escalated as soon as they were found.

Final self-check: if an attacker had the same time and access, what would they try first? Did I check that?

## Depth on demand

- [references/review-checklists.md](references/review-checklists.md) — detailed checklists for authentication, authorisation, injection sinks, web, API, cloud and CI/CD review. Read during step 6.

## Related skills

- `secure-coding` — how to fix what you find, and how to prevent it.
- `authentication-and-authorization` — design depth on identity and access.
- `dependency-management` — managing vulnerable dependencies and supply chain.
- `infrastructure-as-code`, `cloud-architecture` — fixing configuration findings.
- `incident-response` — if the audit uncovers an active compromise.
- `architecture-review` — evaluating designs before they are built.
