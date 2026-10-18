---
name: secure-coding
description: >-
  Write code that resists attack: trust boundaries and input validation,
  output encoding, injection classes (SQL, command, template, path traversal,
  LDAP/NoSQL), XSS, CSRF, SSRF, open redirects, insecure deserialization, file
  upload handling, secrets management, cryptography do's and don'ts, safe
  error handling and logging, least privilege, and the OWASP Top 10 as a
  checking lens. Use when writing or changing code that handles untrusted
  input, user data, files, URLs, credentials, tokens, or crypto; when fixing a
  vulnerability; or when asked to make code "secure". For auditing an existing
  system use security-audit; for login, sessions, and permissions use
  authentication-and-authorization.
metadata:
  category: development
  related: authentication-and-authorization, security-audit, error-handling, dependency-management, api-design, backend-development, frontend-development, code-review, ai-safety-and-guardrails
---

# Secure Coding

Security bugs are ordinary bugs with an adversary. The adversary chooses the inputs, the timing, and the sequence of requests, and they will find the one path you did not think about. Secure coding is mostly the discipline of knowing where untrusted data enters, keeping it from being interpreted as code or commands, and limiting what any single mistake can do.

## Scope

Covers writing and modifying application code so that it is secure by construction: input handling, injection prevention, web-specific attacks, secrets, cryptography usage, deserialization, files, logging, and privilege.

Not covered here:

- Systematically assessing an existing system, threat modelling a whole product, or producing an audit report — see `security-audit`.
- Login, session management, tokens, password storage, and permission models — see `authentication-and-authorization` (this skill covers the code-level hygiene around them).
- Vulnerable third-party packages and supply chain — see `dependency-management`.
- Prompt injection and LLM-specific risks — see `ai-safety-and-guardrails`.
- Infrastructure and network hardening — see `infrastructure-as-code`, `containerization`, `cloud-architecture`.

## Core principles

### 1. Know your trust boundaries

A trust boundary is anywhere data crosses from a less trusted source into code that acts on it: HTTP requests (every part — body, query, path, headers, cookies), files, uploads, message queues, webhooks, third-party API responses, database contents written by other systems, environment set by others, URLs fetched, model outputs, and even your own client-side code (an attacker controls the browser). Why: every class of injection and most logic bugs come from treating data from beyond a boundary as if it were trusted. Identify the boundaries first; most of the remaining work follows.

### 2. Keep data and code separate

Injection happens when data is concatenated into something that will be parsed and executed: a SQL statement, a shell command, HTML, a template, a file path, an LDAP filter, a regex. The fix is structural — use APIs that pass data separately from code (parameterized queries, argument arrays, auto-escaping templates, safe path joins) — not filtering "bad characters". Why: blocklists miss encodings, contexts, and dialects; structural separation makes the data impossible to interpret as code no matter what it contains.

### 3. Validate input, encode output

Validation at the boundary rejects data that is not what the application expects (type, length, format, range, allowed values). Encoding at the output adapts data to the specific context it is placed in (HTML body, HTML attribute, JavaScript, URL, SQL, shell). They solve different problems and you need both. Why: validation alone cannot know every future output context; encoding alone lets malformed data deep into the system where it causes logic errors.

### 4. Deny by default, allow explicitly

Allowlists over blocklists: allowed file types, allowed redirect hosts, allowed fields for mass assignment, allowed URL schemes, allowed sort columns. Default to no access, no permissions, features off. Why: the set of bad inputs is infinite and adversarially chosen; the set of good ones is usually small and known.

### 5. Least privilege and defence in depth

Every component — process, database user, service account, API token, container — gets only the permissions it needs. Layer controls so one failure is not catastrophic (validation plus parameterization plus a restricted database user). Why: you will make mistakes; least privilege bounds the damage of each one.

### 6. Use proven building blocks

Use the framework's built-in protections (CSRF tokens, template auto-escaping, ORM parameterization, security headers middleware) and well-reviewed libraries for crypto, parsing, and sanitization. Why: these encode years of fixes for edge cases you will not think of. Disabling a framework protection should require a comment explaining why and what replaces it.

### 7. Fail securely

When something fails — validation, authorization, a dependency, a parse — the result must be denial, not accidental access. Error messages to clients should be generic; details go to logs. Why: many vulnerabilities are error paths that fall through to success, or verbose errors that reveal internals.

## Discovering context

Before writing security-relevant code:

- Find the existing mechanisms: validation library or schema layer, ORM or query builder, template engine and its escaping mode, CSRF middleware, security headers configuration, secrets loading, logging redaction, authorization helpers. Use them rather than introducing parallel ones.
- Read any security guidelines, threat models, or previous security findings in the repository or docs.
- Determine the deployment context: public internet vs. internal, multi-tenant vs. single-tenant, regulated data (payments, health, personal data), which changes the stakes and sometimes the rules.
- Check framework versions; some protections are default-on only in newer versions.
- Look at how existing code handles similar inputs. If it is unsafe, do not copy the pattern; follow the safe approach and mention the existing issue to the user.

## Process for writing security-sensitive code

1. **List the inputs and their sources.** For the code you are writing, which values come from beyond a trust boundary?
2. **List the sinks.** Where does each input end up — a query, a command, a file path, HTML, a redirect, an outbound request, a log, a deserializer, a permission decision?
3. **For each source-to-sink path, apply the matching control** from the sections below.
4. **Check authorization** for every operation on a resource: is this caller allowed to do this to this specific object? (See `authentication-and-authorization`.)
5. **Consider abuse, not just use**: what happens with huge inputs, many requests, concurrent requests, out-of-order steps, negative numbers, repeated submissions, missing fields?
6. **Write tests for the attack cases**, not only the happy path: an injection payload, a cross-tenant ID, an oversized upload, a path with `../`.
7. **Review error handling and logging** for leaks.

## Input validation

- Validate on the server. Client-side validation is a usability feature; attackers skip it.
- Validate as early as possible, at the boundary, against a schema: type, required/optional, length bounds, numeric ranges, formats (with a strict parser, not a loose regex), enumerated allowed values.
- **Parse, don't just check**: convert input into typed domain values (a parsed date, an integer ID, an enum) and pass those through the system, so downstream code cannot receive unvalidated strings.
- Reject unknown fields where practical, or explicitly pick allowed fields. This prevents **mass assignment** (an attacker adding `"role": "admin"` or `"price": 0` to a request bound directly to a model).
- Bound everything: string lengths, array sizes, nesting depth, request body size, number of items per page, file sizes. Unbounded inputs are denial-of-service vectors.
- Normalize before validating when the input has multiple representations (Unicode normalization, case, path canonicalization, URL decoding) — and validate the normalized form, then use that same form. Validating one representation and using another is a classic bypass.
- Be careful with regular expressions on untrusted input: nested quantifiers can cause catastrophic backtracking (ReDoS). Prefer simple patterns, length limits before matching, or regex engines with linear-time guarantees.
- Treat data from your own database or other internal services as untrusted if anyone else can write to it.

## Injection classes

| Class | Sink | Structural fix | Notes |
|---|---|---|---|
| SQL injection | Database query | Parameterized queries / prepared statements; ORM query APIs | Identifiers (table/column names, sort order) cannot be parameterized — map from an allowlist |
| NoSQL injection | Document DB queries | Typed query builders; reject objects where scalars are expected | e.g. `{"$ne": null}` sent in place of a password string |
| OS command injection | Shell | Avoid the shell: call programs with an argument array, no `shell=True`/string commands | Still validate arguments; a leading `-` can be read as an option — use `--` where supported |
| Code injection | `eval`, dynamic import, reflection | Never evaluate untrusted input; use data formats and dispatch tables | Includes expression languages and spreadsheet formulas |
| Template injection (SSTI) | Server-side template engine | Never build templates from user input; pass user data as variables | Templates are code |
| Path traversal | File system | Resolve the canonical path and check it is inside the intended base directory; better, map IDs to paths server-side | `../`, absolute paths, encoded variants, symlinks, Windows drive letters and UNC paths |
| LDAP / XPath injection | Directory and XML queries | Library escaping functions or parameterized APIs | |
| Header / log injection | HTTP headers, log lines | Reject or encode CR/LF; structured logging | Response splitting, forged log entries |
| CSV / formula injection | Exported spreadsheets | Prefix cells beginning with `=`, `+`, `-`, `@`, tab, or CR, or follow the target application's guidance | Matters when exports are opened in spreadsheet software |
| Prompt injection | LLM prompts | See `ai-safety-and-guardrails` | Model output that reaches other sinks needs the same controls as user input |

Example of the core idea (illustrative, generic):

```
# Vulnerable: data becomes part of the query text
query("SELECT * FROM orders WHERE id = '" + order_id + "'")

# Safe: the driver sends data separately from the statement
query("SELECT * FROM orders WHERE id = ?", [order_id])
```

The same shape applies to commands (`run(["convert", input_path, output_path])` instead of a concatenated shell string) and HTML (template variables rendered with auto-escaping instead of string-built markup).

## Web-specific attacks

### Cross-site scripting (XSS)

Untrusted data rendered into a page in a way the browser executes.

- Use a templating system or UI framework that escapes by default, and do not bypass it (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|safe`, `{!! !!}`, `html_safe`, `bypassSecurityTrust…`) with untrusted data.
- Encoding is context-specific: HTML body, HTML attribute, JavaScript string, URL, and CSS each need different encoding. Never place untrusted data directly into a `<script>` block, an event-handler attribute, or a `style` attribute.
- URLs from users in `href`/`src` must be checked for allowed schemes (`https:`, maybe `mailto:`) — `javascript:` URLs execute.
- When rich HTML from users is required (comments, WYSIWYG), sanitize with a maintained allowlist-based HTML sanitizer, server-side, and keep it updated. Never write your own.
- Add a Content Security Policy as defence in depth; a strict policy (nonces or hashes, no `unsafe-inline`) blocks most injected scripts even when an encoding bug slips through.
- DOM-based XSS: client-side code reading from `location`, `postMessage`, storage, or API responses into dangerous sinks. The same rules apply in front-end code.
- Set cookies carrying sessions as `HttpOnly` so injected scripts cannot read them (they can still act as the user, so this limits but does not prevent damage).

### Cross-site request forgery (CSRF)

Another site causes the victim's browser to send an authenticated request.

- Relevant when authentication is ambient (cookies, HTTP auth). Bearer tokens in headers sent by your own JavaScript are not automatically attached cross-site.
- Use the framework's CSRF protection (synchronizer tokens or signed double-submit cookies) for state-changing requests.
- Set `SameSite` on session cookies (`Lax` is a reasonable default; `Strict` where usability allows). Treat it as a layer, not the only defence.
- Never change state on `GET`. Safe methods must be safe.
- Check `Origin` (or `Referer`) headers on sensitive state-changing endpoints as an additional layer.
- CORS is not CSRF protection. A permissive CORS policy (`Access-Control-Allow-Origin` reflecting any origin with credentials allowed) is itself a vulnerability: it lets other sites read authenticated responses. Allowlist origins explicitly.

### Server-side request forgery (SSRF)

Your server fetches a URL influenced by the attacker and reaches places the attacker cannot: internal services, cloud metadata endpoints (e.g. `169.254.169.254`), localhost admin interfaces.

- Avoid fetching arbitrary user-supplied URLs. If the feature requires it (webhooks, link previews, imports), then:
  - Allowlist schemes (`https`, maybe `http`) and, where possible, destination hosts.
  - Resolve the hostname and reject private, loopback, link-local, and reserved address ranges (IPv4 and IPv6, including IPv4-mapped IPv6), then connect to the resolved IP you checked — otherwise DNS rebinding swaps the address between check and use.
  - Disable or re-validate redirects; a public URL can redirect to an internal one.
  - Run the fetcher with network egress restrictions (a separate service or proxy that cannot reach internal networks) — the most robust control.
  - Limit response size and time; do not return raw responses or detailed errors to the user.
- Use the cloud provider's hardened metadata service mode (e.g. session-token-required) as defence in depth.

### Open redirects

Redirecting to a URL taken from a parameter (`?next=`) lets attackers use your domain for phishing and can leak OAuth codes or tokens. Allow only relative paths (and reject `//host` and `/\host` forms, which browsers treat as absolute) or map to an allowlist of destinations.

### Other web controls

- **Security headers**: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, a frame-ancestors policy (CSP `frame-ancestors` or `X-Frame-Options`) against clickjacking, a sensible `Referrer-Policy`. Use the framework's or a maintained middleware's defaults.
- **Cookies**: `Secure`, `HttpOnly`, `SameSite`, narrow `Path`/`Domain`, and the `__Host-` prefix where possible.
- **HTTPS everywhere**, including internal service-to-service traffic where feasible.

## Files and uploads

- Validate type by content (magic bytes) and an allowlist of extensions; never trust the client-supplied `Content-Type` or filename.
- Generate your own storage filenames (random IDs); never use the uploaded name as a path.
- Store uploads outside the web root or in object storage, and serve them with `Content-Disposition: attachment` and a safe `Content-Type` (or from a separate domain) so uploaded HTML or SVG cannot run scripts in your origin.
- Enforce size limits at the proxy and application layers, and limits on decompressed size for archives (zip bombs). When extracting archives, check every entry's path against traversal ("zip slip").
- Process untrusted files (images, documents, media) with up-to-date libraries, ideally in a sandboxed or isolated worker; parsers for complex formats are a frequent source of critical vulnerabilities.
- Consider malware scanning when files are shared with other users.
- XML: disable external entity resolution and DTD processing (XXE) unless explicitly needed; many parsers are unsafe by default in older versions.

## Deserialization

- Never deserialize untrusted data with formats that can instantiate arbitrary types or run code: e.g. Python `pickle`, Java native serialization, .NET `BinaryFormatter`, PHP `unserialize`, Ruby `Marshal`, YAML loaders in unsafe mode. These turn data into remote code execution.
- Use data-only formats (JSON, protobuf, plain YAML with a safe loader) and map into explicit types with validation.
- If a polymorphic format is unavoidable, restrict deserialization to an allowlist of types, and authenticate the data (signature/MAC) before parsing it.
- Signed data (cookies, tokens) must be verified before being deserialized or trusted.

## Secrets

- Never hardcode secrets in source, tests, config files committed to version control, container images, or front-end bundles. Anything shipped to a browser or mobile app is public.
- Load secrets at runtime from the environment or a secret manager (e.g. a cloud secret manager, Vault, the orchestrator's secret store). Follow the project's existing mechanism.
- Keep example config files with placeholders only; add real secret files to `.gitignore`.
- Never log secrets, tokens, passwords, session IDs, full card numbers, or authorization headers. Configure redaction in the logging layer, and be careful with logging whole request objects, exception contexts, or debug dumps.
- Give each environment and each service its own credentials with least privilege; never reuse production secrets in development or tests.
- Plan for rotation: code should pick up new secrets without redeploying where possible, and support two valid keys during a rotation window.
- If a secret is exposed (committed, logged, pasted), rotate it immediately; removing it from the code or history is secondary. See `git-workflow` for history cleanup.
- Use constant-time comparison for secrets, tokens, and MACs (e.g. `hmac.compare_digest`, `crypto.timingSafeEqual`, `MessageDigest.isEqual`) to avoid timing leaks.

## Cryptography

Rule zero: do not design cryptography, and avoid implementing it. Use high-level, well-reviewed libraries (e.g. libsodium and its bindings, the platform's vetted crypto library, Tink) that make safe choices for you.

Do:

- Use the platform's cryptographically secure random generator for tokens, IDs that must be unguessable, salts, and keys (e.g. `secrets` in Python, `crypto.randomBytes`/`crypto.getRandomValues`, `SecureRandom`). Never `Math.random`, `rand()`, or time-seeded generators. Use at least 128 bits of entropy for security tokens.
- Use authenticated encryption (e.g. AES-GCM or ChaCha20-Poly1305) via a high-level API. It provides confidentiality and integrity together.
- Use unique nonces/IVs per encryption as the algorithm requires; nonce reuse with GCM is catastrophic. Prefer APIs that generate them for you.
- Hash passwords only with a password-hashing function (Argon2id, scrypt, bcrypt, or PBKDF2 with high iteration counts where required by policy) — see `authentication-and-authorization`.
- Use HMAC (e.g. HMAC-SHA-256) to authenticate messages and webhooks; verify with constant-time comparison, and include a timestamp to prevent replay.
- Use TLS for data in transit, with certificate verification enabled.
- Manage keys separately from data (a KMS or secret manager), with rotation and least-privilege access.

Don't:

- Don't use MD5 or SHA-1 for anything security-relevant; don't use fast hashes (SHA-256 alone) for passwords.
- Don't use ECB mode, unauthenticated CBC, or raw block ciphers.
- Don't use encryption when you need integrity (use a MAC or signature), or hashing when you need secrecy.
- Don't disable certificate verification, even "temporarily" or in a script; fix the trust store instead.
- Don't invent token formats, padding schemes, or "obfuscation". Base64 is not encryption.
- Don't roll your own JWT validation; use a maintained library, pin the expected algorithm(s), and reject `none`.

## Error handling and logging

- Return generic errors to clients ("invalid credentials", "not found") and log details server-side with a correlation ID the user can quote.
- Never expose stack traces, SQL errors, internal paths, or framework debug pages in production. Check that debug mode is off in production configuration.
- Avoid distinguishable errors that enable enumeration (e.g. "user not found" vs. "wrong password", or different response times).
- Log security-relevant events — authentication successes and failures, authorization denials, input validation failures at unusual rates, administrative actions — with enough context to investigate, but without secrets or unnecessary personal data.
- Catch exceptions deliberately; an overly broad catch that continues after a failed security check can grant access. See `error-handling`.

## Least privilege in code and runtime

- Database accounts used by the application should have only the needed privileges (often no DDL, no access to other schemas). Migrations can run with a separate, more privileged account.
- Services, containers, and jobs run as non-root users with only the filesystem and network access they need.
- API tokens and cloud roles scoped to specific resources and actions; avoid wildcard permissions.
- Feature code should call authorization checks for each resource access rather than relying on the UI hiding buttons. Insecure direct object references (changing `/invoices/123` to `/invoices/124`) are among the most common real-world vulnerabilities.
- Rate-limit and add quotas on expensive or abusable operations (login, password reset, search, exports, sending email or SMS, LLM calls).

## Concurrency and business logic

- **Race conditions** in security checks: check-then-act on balances, coupon redemption, inventory, or invites can be exploited by sending many requests at once. Use database constraints, transactions with appropriate isolation, atomic updates, or idempotency keys.
- **Time-of-check to time-of-use** with files: check and use the same file handle, not the path twice.
- **Workflow bypass**: steps that can be called out of order (pay → confirm skipped, email verification skipped). Enforce state on the server.
- **Numeric edge cases**: negative quantities, overflow, floating-point money. Use integer minor units or decimal types for money, and validate signs and ranges.

## Worked example: a file download endpoint

Illustrative. A request asks for "an endpoint that returns a user's exported report by filename": `GET /reports?file=q3-summary.pdf`.

Walk the source-to-sink paths:

1. **Source**: `file` comes from the query string — fully attacker-controlled.
2. **Sink 1, file system**: joining it onto a reports directory allows `../../etc/passwd` or an absolute path. Fix structurally: do not accept a filename at all. Accept a report ID, look up the report record, and read the server-side storage key from it.
3. **Sink 2, authorization**: even with IDs, `GET /reports/812` must check that report 812 belongs to the caller (and their tenant). Otherwise this is an IDOR. Scope the lookup query by owner rather than checking afterwards.
4. **Sink 3, response**: set `Content-Disposition: attachment` with a sanitized filename and the stored content type, plus `X-Content-Type-Options: nosniff`, so a report containing HTML is never rendered in your origin.
5. **Abuse**: rate-limit downloads; ensure large files stream rather than load into memory.
6. **Errors**: return the same 404 for "does not exist" and "not yours", so IDs cannot be probed.
7. **Tests**: another user's report ID → 404; a traversal string in the ID → 400/404; the owner → 200 with the correct headers.

The design change in step 2 (IDs instead of paths) removed an entire vulnerability class instead of filtering for it — the pattern to look for whenever user input names a server-side resource.

## Client-side and mobile code

- Anything in a browser bundle or mobile binary is readable and modifiable by the user: no secrets, no trusted business rules, no hidden admin features protected only by obscurity.
- Treat client-side checks (price calculations, feature gates, validation) as UX; repeat them on the server.
- Do not store long-lived tokens or sensitive data in web storage; use the platform secure store on mobile.
- Validate `postMessage` origins and message shapes; use `targetOrigin` explicitly when sending.
- Keep third-party scripts to a minimum and load them with Subresource Integrity where versions are fixed; each one can read the page.
- Deep links and custom URL schemes are untrusted input to a mobile app.

## OWASP Top 10 as a lens

The OWASP Top 10 is a periodically updated awareness list of the most common web application risk categories. Use it as a checklist lens over your change, not as a complete standard. Recent editions include categories along these lines (names and order change between editions — check the current one):

- **Broken access control** — missing per-object authorization, IDOR, privilege escalation, CORS misconfiguration.
- **Cryptographic failures** — plaintext sensitive data, weak algorithms, poor key management.
- **Injection** (including XSS) — data interpreted as code.
- **Insecure design** — missing controls at the design level (no rate limiting, no tenant isolation model).
- **Security misconfiguration** — debug on, default credentials, verbose errors, permissive headers or cloud settings.
- **Vulnerable and outdated components** — see `dependency-management`.
- **Identification and authentication failures** — see `authentication-and-authorization`.
- **Software and data integrity failures** — unsigned updates, insecure deserialization, untrusted CI pipelines.
- **Security logging and monitoring failures** — attacks not detected or not investigable.
- **SSRF**.

For deeper, more complete checking use a verification standard such as OWASP ASVS, and for mobile or API-specific risks the corresponding OWASP lists.

## Pitfalls

- **Sanitizing with blocklists** ("strip `<script>`", "remove quotes") instead of structural separation and context encoding.
- **Validating in one representation, using another** (checking a path before decoding, a URL before following redirects, a hostname before DNS resolution).
- **Trusting client-side checks**, hidden form fields, or IDs in the URL.
- **Authorization only in the UI**, not on the server for each request and object.
- **Building SQL identifiers or `ORDER BY` from input** because "you can't parameterize those".
- **`shell=True` with interpolated strings**, or passing user input as the first argument of a command.
- **Disabling a framework protection** (CSRF, auto-escaping, TLS verification) to make something work, without replacing it.
- **Secrets in logs**, error messages, URLs (query strings end up in logs and referrers), or front-end code.
- **Weak randomness** for tokens, reset links, or IDs that must not be guessable.
- **Copying an insecure pattern** already present in the codebase for consistency.
- **Security through obscurity** as the only control (unlisted URLs, "nobody knows this endpoint").
- **Fixing one instance** of a vulnerability while identical code elsewhere remains. Search for the pattern.

## Quality bar and verification

Before declaring security-relevant work done:

- Every untrusted input in the change is identified, validated at the boundary, and bounded in size.
- Every sink uses a structural control: parameterized queries, argument arrays, auto-escaped templates, canonicalized-and-contained paths, safe deserializers.
- Every resource access has a server-side authorization check scoped to the caller.
- No secrets in code, config committed to version control, logs, or error responses. Debug features are off in production config.
- Crypto uses vetted libraries and current algorithms; random values come from a secure generator.
- Tests include attack cases (injection payloads, traversal paths, cross-tenant IDs, oversized inputs, replayed or tampered tokens) and they fail against a deliberately vulnerable variant.
- Static analysis or security linters (e.g. Semgrep, CodeQL, Bandit, gosec, eslint security plugins) and secret scanners run clean or with triaged findings, if available in the project.
- Similar code elsewhere was searched for the same issue when fixing a vulnerability.

When reporting, state which threats the change addresses, which controls were applied, what was tested, and any residual risks or follow-ups (e.g. "the export feature elsewhere uses the same unsafe pattern").
