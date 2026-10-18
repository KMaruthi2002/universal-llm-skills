# Security Review Checklists

Detailed checklists for the manual review phase of `security-audit`. Use them **after** the threat model has told you which areas matter; they are prompts for completeness, not a substitute for thinking about this system's specific assets and logic. Not every item applies to every stack. Each item is phrased as a question whose "wrong" answer is a lead to investigate and confirm.

## Authentication

- Are passwords hashed with a slow, salted, purpose-built algorithm (e.g. bcrypt, scrypt, Argon2, or PBKDF2 with a high work factor)? Is the work factor current?
- Is there any path that compares secrets with a non-constant-time comparison?
- Does login, password reset, and OTP/MFA verification have rate limiting or lockout? Is it per account *and* per source, so it resists both brute force and credential stuffing?
- Do login, signup and reset reveal whether an account exists (different messages, status codes, or timing)?
- Are reset tokens long, random, single-use, short-lived, and invalidated when a new one is issued or the password changes?
- Is the reset link built from a trusted base URL, not the request's Host header?
- Can MFA be bypassed through an alternate flow (legacy login endpoint, API token login, "remember this device", account recovery, SSO fallback)?
- Are sessions invalidated server-side on logout, password change, MFA change, and account disablement?
- Are session identifiers regenerated after login (session fixation)?
- For tokens (e.g. JWTs): is the signature verified, the algorithm pinned (not taken from the token header), and are expiry, issuer and audience checked? Is the signing key strong and secret?
- Are long-lived API keys scoped, revocable, listed to their owners, and stored hashed?
- For SSO/OAuth/OIDC: is the `state` parameter (or PKCE) used and checked? Are redirect URIs matched exactly? Is the identity taken from a verified ID token rather than an unverified profile field such as email?
- Are service-to-service calls authenticated, or does anything trust "it came from the internal network"?

## Authorisation

- For every endpoint and handler, is there a server-side check of both the action and the specific object? (Build the endpoint-to-check table.)
- Are object IDs guessable (sequential integers)? Unguessable IDs reduce risk but are not authorisation.
- In multi-tenant systems, is the tenant always derived from the authenticated identity? Are queries scoped by tenant in a way that is hard to forget (e.g. enforced in a data-access layer or by row-level policies)?
- Can a user update fields that should be server-controlled (role, owner, tenant, price, status, verified flags) via mass assignment or unfiltered update payloads?
- Are admin and internal endpoints protected by role checks, not just by being undocumented or behind a UI that hides them?
- Do bulk operations, exports, search, reporting, GraphQL nested resolvers, and webhooks apply the same checks as single-object endpoints?
- Are file download links and pre-signed URLs scoped and short-lived?
- Does caching (CDN, application cache) ever serve one user's response to another?
- Is authorisation re-checked for long-running sessions and queued jobs, or does a revoked user's job still run with old rights?
- Are privilege changes (granting roles, inviting admins) themselves protected and audited?

## Injection and dangerous sinks

For each, trace untrusted sources (request parameters, headers, cookies, bodies, uploaded files, queue messages, webhook payloads, database values originally from users, third-party API responses) to the sink.

- **SQL / NoSQL**: are all queries parameterised? Watch dynamic `ORDER BY`, table or column names, `IN` lists, raw query escape hatches in ORMs, and NoSQL operator injection via JSON objects.
- **Shell**: is user input ever passed to a shell? Prefer argument arrays without a shell; check for argument injection (values beginning with `-`).
- **Paths**: can input contain `..`, absolute paths, or encoded variants that escape the intended directory? Archive extraction (zip slip)?
- **Templates**: is user input ever used *as* a template rather than as data (server-side template injection)?
- **HTML/JS output**: is output encoded for its context (HTML body, attribute, JavaScript, URL, CSS)? Any use of raw-HTML insertion APIs or template "safe" markers on user data?
- **Deserialisation**: are untrusted bytes deserialised with formats that can instantiate arbitrary types?
- **XML**: are external entities and DTDs disabled?
- **URLs fetched server-side**: is there an allow-list? Are internal addresses, metadata endpoints, redirects, and DNS rebinding handled?
- **Redirects**: are redirect targets validated against an allow-list?
- **Headers and logs**: can input inject newlines into headers or log lines?
- **Regex**: are user-supplied patterns, or patterns with catastrophic backtracking applied to user input, possible?
- **LLM prompts**: can untrusted content instruct a model that has tools or access to other users' data?

## Web application specifics

- Cookies: `Secure`, `HttpOnly` where appropriate, sensible `SameSite`, narrow domain and path.
- CSRF protection on state-changing requests that rely on cookies.
- Content Security Policy present and not trivially bypassed (no broad `unsafe-inline` plus wildcard sources).
- Clickjacking protection (frame-ancestors or equivalent) on sensitive pages.
- CORS: no reflection of arbitrary origins with credentials allowed.
- File uploads: type validated by content not just extension, size limits, stored outside the web root or on a separate domain, served with safe content types and `Content-Disposition`, scanned if required.
- Error pages and responses do not leak stack traces, queries, or internal hostnames in production.
- Third-party scripts loaded from external origins: pinned, integrity-checked, and justified.

## API specifics

- Every endpoint authenticated unless deliberately public, and the public list is reviewed.
- Responses return only fields the caller needs; no internal or sensitive fields serialised by default.
- Pagination and limits enforced server-side; maximum page size bounded.
- Rate limits per client on expensive and sensitive operations.
- Older API versions still deployed are held to the same standard, or retired.
- GraphQL: query depth and complexity limits, introspection policy considered, authorisation at the resolver/field level.
- Webhooks received: signatures verified, timestamps checked to prevent replay, processing idempotent.

## Secrets and cryptography

- No secrets in source, history, config examples, test fixtures, container images, client bundles, mobile apps, or logs.
- Secrets loaded from a secret manager or environment at runtime, with least-privilege access, and rotated.
- Standard, current algorithms and library implementations; no custom cryptography.
- Security-relevant randomness from a cryptographically secure generator.
- TLS certificate verification never disabled outside of tests (and not "temporarily" in production code paths).
- Encryption keys separated from the data they protect; key access audited.

## Cloud and infrastructure

- No public storage buckets or snapshots unless deliberately public; listing disabled.
- Security groups and firewall rules: no management ports or databases open to the internet.
- IAM: no wildcard actions on wildcard resources; humans use federated short-lived credentials; workload identities scoped per service; unused keys and roles removed.
- Instance metadata service protected against SSRF (e.g. requiring session tokens where the platform supports it).
- Encryption at rest enabled for data stores and backups; backups access-controlled and tested.
- Audit logging enabled for the control plane and retained; alerts on high-risk events (root/owner login, policy changes, key creation).
- DNS: no dangling records pointing at deprovisioned resources (subdomain takeover).
- Containers: non-root users, minimal base images, no privileged mode or host mounts without need, images scanned and pinned by digest.
- Orchestrators: role-based access scoped, secrets not in plain manifests, network policies restricting east-west traffic.

## CI/CD and supply chain

- Who can modify pipeline definitions, and are changes reviewed?
- Can pull requests from forks or untrusted contributors run jobs with access to secrets or deployment credentials?
- Are third-party actions, plugins and build images pinned to immutable versions or digests?
- Are dependency lockfiles committed and used in builds? Are new dependencies reviewed?
- Are build artifacts produced in a controlled environment and, where appropriate, signed and verified at deploy?
- Are deployment credentials scoped per environment, with production deploys requiring approval?
- Do build logs ever print secrets?

## Logging, detection and response

- Are authentication events, authorisation failures, privilege changes and administrative actions logged with who, what, when and from where?
- Are logs protected from tampering and from access by the people whose actions they record?
- Do logs avoid recording secrets, tokens, full card numbers, and unnecessary personal data?
- Would the attacks implied by your findings generate an alert, and does someone receive it?
- Is there a documented way to revoke sessions, rotate keys, and disable accounts quickly?
