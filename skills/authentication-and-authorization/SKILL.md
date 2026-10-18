---
name: authentication-and-authorization
description: >-
  Design and implement who-are-you and what-may-you-do correctly: choosing
  between managed identity providers, auth libraries, and custom code; sessions
  vs. tokens (JWT, opaque, refresh); OAuth 2.0 and OpenID Connect flows (auth
  code + PKCE, client credentials, device flow); password storage, reset, and
  account recovery; MFA and passkeys/WebAuthn; API keys and service-to-service
  auth; RBAC, ABAC, and relationship-based access control; multi-tenant
  isolation; and the common auth bugs. Use when adding login, signup, SSO,
  social login, MFA, API authentication, roles and permissions, tenant
  isolation, or when debugging or reviewing auth code.
metadata:
  category: development
  related: secure-coding, api-design, backend-development, frontend-development, database-design, security-audit, mobile-app-development, system-design
---

# Authentication and Authorization

Authentication (authn) establishes who is making a request. Authorization (authz) decides whether that identity may perform this action on this resource. Both are deceptively simple to sketch and notoriously easy to get subtly wrong, and mistakes are directly exploitable. The central rule of this skill: reuse proven systems for the hard parts, and put your own effort into the parts only you can get right — your permission model and enforcing it everywhere.

## Scope

Covers end-user and machine authentication, session and token handling, federated login, credentials and recovery, MFA, permission models, multi-tenancy, and the implementation hazards around all of these.

Related skills:

- General input handling, crypto hygiene, CSRF/XSS, secrets — `secure-coding`.
- Auditing an existing system — `security-audit`.
- API surface design (how auth appears in the API) — `api-design`.
- Schema for users, roles, and tenants — `database-design`.

## Core principles

### 1. Don't build what you can adopt

Use a managed identity provider (e.g. Auth0/Okta, Cognito, Entra ID, Firebase Auth, Clerk, Supabase Auth, WorkOS, Keycloak self-hosted) or a mature framework auth library (e.g. Django's auth, Devise, ASP.NET Identity, Spring Security, Auth.js/NextAuth, Passport, Lucia-style libraries) before writing authentication from scratch. Why: password hashing, timing-safe comparisons, session fixation, token validation, account enumeration, MFA enrolment, recovery flows, and federation protocols each contain well-known traps. A proven system has already been attacked and fixed. Your custom code has not.

Choosing among them:

| Option | Choose when | Trade-offs |
|---|---|---|
| Managed IdP | You want SSO/social/enterprise federation, MFA, passkeys quickly; small team; compliance pressure | Cost per user, vendor lock-in, less control over UX and data residency |
| Self-hosted IdP (e.g. Keycloak, Ory, Authentik, Zitadel) | Need control, on-prem, data residency, many apps | You operate and patch it |
| Framework auth library | Single app, conventional login, framework already has strong defaults | Federation and MFA may need extra work |
| Custom | Truly unusual requirements, and you have security expertise and review capacity | Highest risk; justify explicitly |

Follow whatever the project already uses. If it uses a provider, integrate with it properly rather than adding a second mechanism.

### 2. Authorization is enforced on the server, on every request, for every object

The UI can hide what a user may not do; only the server can prevent it. Every endpoint, job, and query that touches a resource must check that the authenticated principal may perform that action on that specific resource. Why: broken access control — especially insecure direct object references (changing an ID in a URL) — is the most common serious vulnerability in real applications, and it comes from checks that exist in most places but not all.

### 3. Centralize policy, decentralize nothing

Express permission rules in one place (a policy module, a policy engine, or middleware with a clear API), and make the safe path the easy path: e.g. data-access functions that require a principal and scope their queries, so forgetting the check is hard. Why: scattered `if user.role == "admin"` checks drift, contradict each other, and are impossible to audit.

### 4. Default deny

No access unless a rule grants it. New endpoints are protected by default; making something public is an explicit, reviewable act. Why: the failure mode of a forgotten rule should be "someone gets an error", not "everyone gets the data".

### 5. Credentials are toxic; minimize, protect, and expire them

Store as few credentials as possible, hash what you must store, scope and time-limit what you issue, and make revocation possible. Why: every credential will eventually leak somewhere (logs, browser storage, a laptop, a breach); limited scope and lifetime bound the damage.

## Discovering context

Before changing auth:

- Identify the existing identity source (provider, library, custom tables), session or token mechanism, and where authorization checks live. Trace one authenticated request end to end: where is the credential read, validated, turned into a principal, and checked?
- Find the user, role, permission, and tenant models in the schema.
- Determine clients: server-rendered web, single-page app, mobile, CLI, third-party API consumers, other services. Each affects the right flow.
- Check requirements: enterprise SSO (SAML/OIDC), social login, MFA mandates, compliance (e.g. SOC 2, HIPAA, PCI DSS, regional privacy laws), password policy, session timeouts, audit logging.
- Look for existing tests of authorization; their absence is itself a finding.
- If the project already has a pattern for checking permissions, use it consistently. If it lacks one, raise that rather than adding another ad hoc check.

## Sessions vs. tokens

### Server-side sessions (session ID in a cookie)

The server stores session state; the browser holds an opaque random ID in a cookie.

- Pros: instant revocation (delete the session), small cookie, no sensitive data on the client, mature framework support.
- Cons: requires a session store shared across instances (database, Redis), cookies need CSRF protection.
- Best default for browser-based apps served from your own domain, including most SPAs on the same site (use a backend-for-frontend if the SPA talks to APIs).

### Self-contained tokens (e.g. JWT access tokens)

Signed tokens carrying claims, validated without a lookup.

- Pros: stateless validation across services; suits APIs and distributed systems.
- Cons: hard to revoke before expiry; claims go stale (role changed, user disabled); size; many implementation pitfalls.
- Mitigations: short lifetimes (minutes), refresh tokens for renewal, a revocation or denylist check for high-risk actions, and re-reading critical attributes from the source of truth.

### Opaque tokens

Random strings validated by lookup or introspection. Revocable like sessions, usable in headers like JWTs. A good choice for API keys and refresh tokens.

### Decision table

| Client | Recommended default |
|---|---|
| Server-rendered web app | Server-side session in a `Secure; HttpOnly; SameSite` cookie |
| SPA on same site as its API | Cookie session (often via a backend-for-frontend), not tokens in JavaScript-accessible storage |
| SPA calling third-party APIs | OAuth auth code + PKCE; prefer a backend-for-frontend holding tokens server-side |
| Native mobile/desktop app | OAuth auth code + PKCE via the system browser; tokens in the platform secure store (Keychain, Keystore) |
| CLI | Device authorization flow or loopback-redirect auth code + PKCE; tokens in the OS credential store |
| Service-to-service | Client credentials, workload identity (cloud IAM, SPIFFE), or mTLS |
| Third-party developers | API keys or OAuth client credentials, scoped and revocable |

### Token and session handling rules

- Session IDs and tokens: generated by a CSPRNG, ≥128 bits of entropy.
- Regenerate the session ID on login and on privilege change (prevents session fixation).
- Cookies: `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict`, narrow scope; consider the `__Host-` prefix.
- Avoid storing long-lived tokens in `localStorage`/`sessionStorage` — any XSS can read them. If a browser must hold tokens, keep access tokens short-lived and in memory.
- Expire sessions: an idle timeout and an absolute lifetime, set according to risk (banking minutes; consumer apps days to weeks with re-authentication for sensitive actions).
- Logout must invalidate server-side state (session, refresh token), not just delete the cookie.
- Refresh tokens: rotate on each use and detect reuse (a reused refresh token means theft — revoke the whole family). Bind to the client where the platform allows.
- Never put tokens in URLs (they end up in logs, history, and referrer headers), except where a protocol requires short-lived single-use codes.

### JWT pitfalls

Use a maintained library and configure it strictly:

- Pin the accepted algorithm(s); reject `alg: none` and algorithm switching (e.g. an RS256 public key used as an HS256 secret).
- Validate signature, `exp`, `nbf`, `iss`, and `aud` every time. Missing audience checks let a token for one service be used at another.
- Fetch signing keys from the issuer's JWKS endpoint with caching and key rotation support; do not hardcode keys that will rotate.
- Do not put sensitive data in JWT payloads — they are encoded, not encrypted.
- Do not use an ID token as an API access token; they have different audiences and purposes.

## OAuth 2.0 and OpenID Connect

OAuth 2.0 is for **delegated authorization** (an app obtaining access to an API on a user's behalf). OpenID Connect (OIDC) adds **authentication** on top (an ID token saying who the user is). "Log in with X" is OIDC.

Current best practice (reflected in the OAuth 2.0 Security Best Current Practice and OAuth 2.1 drafts):

| Flow | Use for | Notes |
|---|---|---|
| Authorization code + PKCE | All user-facing clients: web, SPA, mobile, desktop, CLI with browser | PKCE for every client, including confidential ones |
| Client credentials | Machine-to-machine, no user | Keep client secrets server-side; prefer private-key JWT or mTLS client auth where supported |
| Device authorization | Input-constrained devices, CLIs without a browser | User approves on another device |
| Refresh token | Renewing access | Rotation and reuse detection |
| Implicit flow | Do not use | Tokens in URL fragments; superseded by code + PKCE |
| Resource owner password credentials | Do not use | App sees the user's password; defeats the point of federation and MFA |

Implementation checks:

- Use a certified or widely used client library; do not hand-roll the protocol.
- Use and verify the `state` parameter (CSRF protection for the redirect) and the `nonce` for OIDC.
- Register exact redirect URIs; no wildcards, no open redirects on the callback path.
- Validate ID tokens fully (signature, issuer, audience, expiry, nonce).
- Request minimal scopes.
- Identify users by the stable subject identifier (`sub`, scoped to the issuer), never by email alone. Emails change, can be unverified, and can be reused; linking accounts by unverified email enables account takeover.
- For enterprise customers, SAML is still common; use a library or provider that handles it, as XML signature validation is a notorious source of bypasses.

## Passwords

If you store passwords at all (prefer delegating to a provider):

- **Hash with a password-hashing function**: Argon2id (preferred where available), scrypt, or bcrypt; PBKDF2 with a high iteration count where policy requires FIPS-validated algorithms. Use the library's recommended or current recommended parameters (e.g. from the OWASP Password Storage Cheat Sheet) and tune for roughly tens to a few hundred milliseconds per hash on your hardware. Salts are handled by these functions; do not invent your own scheme.
- Store the algorithm and parameters with each hash (standard encoded formats do this) so you can upgrade: rehash on next successful login when parameters change.
- Note bcrypt's 72-byte input limit; handle long passwords per your library's guidance rather than silently truncating.
- **Policy** (per current NIST SP 800-63B guidance): minimum length (at least 8, preferably more; allow at least 64), allow all characters including spaces and Unicode, check against breached-password lists, no forced composition rules, no periodic forced rotation without evidence of compromise. Encourage password managers (allow paste).
- **Throttle** login attempts per account and per source, with progressive delays; avoid hard lockouts that let attackers lock out victims, or pair them with safe unlock paths.
- **Do not reveal which part failed**: "invalid email or password". Keep timing similar for existing and non-existing accounts (hash against a dummy when the user does not exist).
- Compare with the library's verify function (constant-time).

### Password reset and account recovery

Recovery is often the weakest link — it is an alternative way to log in.

- Reset tokens: random, high-entropy, single-use, short-lived (minutes to an hour), stored hashed, invalidated after use and when another is issued.
- Send to a verified channel; respond identically whether or not the account exists.
- After reset: invalidate existing sessions and refresh tokens, notify the user through their known channels.
- Do not use security questions; they are guessable and researchable.
- Recovery must not bypass MFA silently: require a second factor or a deliberate, slower recovery process with notifications.
- Build reset links from a configured base URL, never from the request's `Host` header (host-header poisoning sends the link to an attacker's domain).

## Multi-factor authentication and passkeys

Factor strength, roughly strongest to weakest:

1. **Passkeys / WebAuthn / FIDO2 security keys** — phishing-resistant because the credential is bound to the site origin. Prefer these.
2. **Authenticator app TOTP** — good, but phishable through real-time proxies.
3. **Push notifications** — convenient, vulnerable to fatigue attacks; use number matching.
4. **SMS / voice codes** — vulnerable to SIM swap and interception; better than nothing, avoid for high-value accounts.
5. **Email codes/links** — as strong as the email account.

Implementation guidance:

- Use the provider's MFA or a maintained WebAuthn library; WebAuthn verification (challenge, origin, RP ID, signature counter, attestation choices) is intricate.
- Passkeys: support multiple credentials per user, allow naming and removing them, and offer a recovery path that does not collapse security to a weak factor.
- TOTP: rate-limit attempts, prevent code reuse within its window, store secrets encrypted.
- Provide recovery codes at enrolment: random, single-use, stored hashed.
- Require step-up re-authentication for sensitive actions (changing email, password, MFA settings, payout details, deleting the account), even within a valid session.
- MFA changes and removals must be notified and should themselves require MFA.

## Machine and API authentication

- **API keys**: random, high-entropy, shown once, stored hashed (a fast hash such as SHA-256 is acceptable for high-entropy random keys; slow hashing is for low-entropy passwords), with a visible prefix for identification and secret scanning. Scope them (permissions, resources, environments), allow multiple active keys for rotation, record last-used time, and support immediate revocation.
- **Service-to-service**: prefer platform workload identity (cloud IAM roles, Kubernetes service account tokens with audience binding, SPIFFE/SPIRE) or mTLS over long-lived shared secrets. If secrets are unavoidable, keep them in a secret manager and rotate.
- **Webhooks** you receive: verify the provider's signature (HMAC over the raw body with constant-time comparison, timestamp checks against replay). Webhooks you send: sign them and document verification.
- Propagate user identity across services deliberately (e.g. token exchange or signed internal headers stripped at the edge), and never trust an identity header that an external client could set.

## Authorization models

| Model | How it decides | Fits | Watch out for |
|---|---|---|---|
| **ACL** | Per-resource lists of who may do what | File-sharing, small scale | Hard to manage at scale; hard to answer "what can X access?" |
| **RBAC** | Users have roles; roles have permissions | Most business apps; clear job functions | Role explosion; roles that encode specific resources ("editor-of-project-42") |
| **ABAC** | Rules over attributes of user, resource, action, environment ("same department and document not classified and during business hours") | Fine-grained, contextual, regulated environments | Rules hard to reason about and audit; performance |
| **ReBAC** | Permissions derived from relationships in a graph ("viewer of folder → viewer of its documents"; "member of org that owns repo") — e.g. Zanzibar-style systems such as OpenFGA, SpiceDB, Permify | Collaboration, sharing, hierarchies, nested teams | Requires keeping relationship data in sync; another system to operate |

Practical guidance:

- Start with **RBAC scoped per tenant/organization** (roles assigned within an org, not globally) plus **ownership checks**. This covers most applications.
- Check **permissions, not roles**, in code: `can(user, "invoice:approve", invoice)` rather than `user.role == "manager"`. Roles map to permissions in one place, so changing what a role may do does not require hunting through code.
- Add ABAC-style conditions or move to ReBAC when sharing, hierarchies, or per-resource grants dominate the requirements. A policy engine (e.g. OPA/Rego, Cedar, Casbin, or a ReBAC service) helps when rules are complex, shared across services, or must be audited independently.
- Model **who can grant what**: an admin who can assign any role can make themselves owner. Prevent privilege escalation through role assignment and invitation flows.
- Make **"list" endpoints filter** by authorization, not just "get" endpoints. Search, export, reports, autocomplete, counts, and aggregate statistics leak data too.
- Field-level authorization: some users can see an object but not all its fields (salary, internal notes). Shape responses per permission; do not rely on the client to hide fields.

## Multi-tenant isolation

In multi-tenant systems, the worst bug is one tenant seeing another's data. Treat tenant isolation as a first-class invariant.

Isolation strategies:

| Strategy | Isolation | Cost and complexity |
|---|---|---|
| Shared tables with `tenant_id` column | Logical; depends on every query being scoped | Cheapest; highest risk of leaks through a missing filter |
| Shared tables + database row-level security (e.g. PostgreSQL RLS) | Database enforces scoping using a per-connection tenant setting | Moderate; strong safety net; watch connection pooling and superuser bypass |
| Schema per tenant | Stronger; per-tenant migrations | Operational overhead with many tenants |
| Database or deployment per tenant | Strongest; can satisfy data residency | Highest cost; fleet management |

Rules:

- Derive the tenant from the authenticated principal, never from a client-supplied parameter or header alone. If a user can belong to several tenants, verify membership for the requested tenant on every request.
- Scope every query by tenant through a mechanism that is hard to forget: a repository layer that requires the tenant, ORM default scopes, or row-level security. Code review alone does not scale.
- Remember the non-obvious paths: background jobs, caches (include tenant in cache keys), search indexes, file storage paths, analytics exports, logs, message queues, admin tools, and support impersonation.
- Use non-sequential, unguessable IDs for externally visible resources as defence in depth — never as the only control.
- Write automated tests that create two tenants and assert that every endpoint refuses cross-tenant access.
- Support/admin access to tenant data ("impersonation") should be explicit, audited, time-limited, and visible to the customer where appropriate.

## Worked example: adding "share a document with a teammate"

Illustrative. An app has per-organization RBAC (owner, admin, member) and documents owned by users. The feature: members can share a document with specific teammates as viewer or editor.

1. **Model**: plain RBAC cannot express "Alice may edit document 7". Add per-resource grants (a `document_shares` relation of document, user, permission) — a small ReBAC-style step — rather than inventing roles per document.
2. **Policy**: in the central policy module, `can(user, "document:edit", doc)` becomes: same org as the document **and** (owner **or** org admin **or** has an editor share). `document:view` additionally accepts a viewer share.
3. **Grant rules**: who may share? Only the owner or an editor, and an editor may grant at most editor — never ownership. Both grantee and document must be in the same organization; check that on the server, since the client sends the grantee ID.
4. **Enforcement paths**: the document page, the API, search results, the "recent documents" list, export, notifications that include document titles, and the realtime collaboration channel all go through the same policy check or a query scoped by it.
5. **Revocation**: removing a share must take effect immediately, including open realtime sessions — so permissions cannot live only in a long-lived token.
6. **Tests**: a viewer cannot edit; a non-shared member sees nothing in search; a user from another org cannot be added as grantee; an editor cannot grant ownership; revoking a share closes access on the next request.

## Common auth bugs

- **IDOR**: object fetched by ID without checking it belongs to the caller or their tenant.
- **Missing check on one path**: the web route checks, but the API route, GraphQL resolver, batch endpoint, export, or websocket handler does not.
- **Trusting client claims**: role, tenant, or user ID taken from the request body, a header, or a client-decoded token instead of the verified session.
- **Privilege escalation via mass assignment**: updating your own user record with `role` or `is_admin` in the payload.
- **Account linking by email**: social login matched to an existing account using an unverified email.
- **JWT misvalidation**: no audience check, accepting `none`, algorithm confusion, not checking expiry, trusting the token after the user is disabled.
- **Session fixation**: session ID not rotated at login.
- **Logout that does not revoke**: tokens remain valid server-side.
- **Recovery bypass**: reset flow that skips MFA, leaks token in referrer, or uses predictable tokens.
- **Enumeration**: different errors, status codes, or timings for "no such user" on login, signup, or reset.
- **Missing rate limits** on login, MFA verification, reset, and signup.
- **Authorization cached too long**: permissions in a long-lived token or cache that survives a role revocation.
- **Confused deputy**: a service with broad privileges acting on a user's behalf without checking the user's rights.
- **Insecure redirects** after login (`?next=` to an external site).
- **Hardcoded or default admin credentials**, debug backdoors, or "temporary" bypass flags left enabled.
- **Race conditions** in invitations, role changes, or one-time tokens (used twice concurrently).

## Testing auth

- Unit-test the policy layer exhaustively: a matrix of principals × actions × resource states, including denial cases. Denials matter more than grants.
- Integration-test each endpoint with: no credentials, invalid/expired credentials, a valid user without permission, a user from another tenant, and the authorized user.
- Test token edge cases: expired, wrong audience, wrong issuer, tampered signature, revoked refresh token reuse.
- Test recovery and MFA flows, including attempts to skip steps.
- Use separate test identities and test tenants; never test against real user accounts or production identity provider tenants without explicit permission. Test credentials belong in fixtures or a seeded test environment, not hardcoded alongside production config.
- Where possible, add a test that enumerates all routes and fails if any is missing an explicit auth/public declaration — a cheap guard for default deny.

## Pitfalls in the process

- Adding a second auth mechanism next to the existing one, leaving two inconsistent sources of truth.
- Implementing auth flows from a blog post instead of a maintained library.
- Designing permissions around today's screens rather than resources and actions, then retrofitting.
- Forgetting non-HTTP entry points (jobs, CLIs, queue consumers, admin scripts).
- Logging tokens, passwords, reset links, or authorization headers while debugging. Remove debug logging and check log configuration.
- Treating "internal network" as authentication.

## Quality bar and verification

Before declaring auth work done:

- The mechanism is a proven provider or library, or custom code with explicit justification and review.
- Every new or changed endpoint and job has an explicit authentication requirement and a server-side, per-object authorization check through the central policy mechanism; defaults deny.
- Tenant scoping is enforced structurally and covered by cross-tenant tests.
- Sessions/tokens: secure generation, correct cookie flags or secure storage, rotation at login, expiry, real revocation on logout and credential change; JWTs fully validated.
- Passwords (if stored) use a current password-hashing function with appropriate parameters; reset and recovery flows are single-use, short-lived, enumeration-resistant, and do not bypass MFA.
- Sensitive actions require step-up authentication.
- Rate limits exist on credential-checking endpoints.
- Tests cover denial cases, token edge cases, and cross-tenant access, and pass.
- No credentials or tokens appear in logs, URLs, or committed configuration.

When reporting, describe the authentication flow and authorization model in a few sentences, list what was tested (especially denials), and call out any accepted risks or gaps (e.g. "admin export endpoint predates this change and lacks tenant scoping").
