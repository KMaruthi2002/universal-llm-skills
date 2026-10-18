---
name: mcp-server-development
description: >-
  Build, test, secure, and ship Model Context Protocol (MCP) servers and
  clients that expose tools, resources, and prompts to LLM applications:
  choosing between tools, resources, and prompts; picking a transport (stdio
  for local, HTTP-based for remote); designing tool names, input schemas,
  descriptions, and results; error handling; authentication and authorisation
  for remote servers; testing with inspector tools and real hosts; and
  limiting the blast radius of exposed actions. Use when someone wants to
  "build an MCP server", wrap an API or database for an AI assistant, connect
  a tool to an MCP-capable host, debug an MCP server that will not connect or
  whose tools the model misuses, or review an MCP server's security. For
  general tool and agent design use ai-agents-and-tool-use.
metadata:
  category: ai-ml
  related: ai-agents-and-tool-use, api-design, authentication-and-authorization, secure-coding, ai-safety-and-guardrails, api-integrations-and-webhooks, cli-development, llm-application-development
---

# MCP Server Development

The Model Context Protocol is an open protocol that lets an LLM host application (a chat client, IDE, agent framework) connect to external servers that provide capabilities: tools the model can call, resources the application can read, and prompts the user can invoke. Writing a server once makes those capabilities available to any compatible host. The protocol handles the plumbing; the hard parts are the same as any tool design — clarity for the model, and safety for the user.

The protocol evolves. Before building, read the current specification and the official SDK documentation for your language: transport options, authorisation requirements, and capability features have changed across versions, and details here are deliberately conceptual.

## Scope

Covers: when MCP is appropriate, choosing primitives, transports, server structure, schema and description design, results and errors, auth for remote servers, testing, packaging, and security.

Neighbours: `ai-agents-and-tool-use` (tool design in depth, agent loops), `api-design` (the underlying API), `authentication-and-authorization` (OAuth and token handling), `secure-coding` and `ai-safety-and-guardrails` (threat model), `api-integrations-and-webhooks` (talking to upstream services).

## When to build an MCP server

Build one when:

- you want a capability usable from multiple LLM hosts without per-host integration;
- users should be able to install and connect the capability themselves;
- you are wrapping an existing API, database, file store, or internal service for AI use.

Consider alternatives when:

- the tool is used by a single application you control: native tool calling in that application may be simpler;
- the operation is a fixed pipeline with no model choice involved: a normal script or service is enough;
- a well-maintained server for the same system already exists: evaluate it (including its security) before writing your own.

## Core concepts

### Roles

- **Host**: the application the user interacts with; it contains the model and manages connections.
- **Client**: the host's connector to one server (one client per server connection).
- **Server**: your program, exposing capabilities.

### Primitives — choosing the right one

| Primitive | Controlled by | Use for | Example |
|---|---|---|---|
| **Tools** | The model decides to call them | Actions and dynamic queries with parameters | `search_issues(query)`, `create_ticket(...)` |
| **Resources** | The application/user decides what to attach | Read-only content identified by URI that can be put into context | A file, a database schema, a document by ID |
| **Prompts** | The user explicitly invokes them | Reusable templated workflows or instructions | "Summarise this PR", "Draft release notes" |

Guidance:

- If the model needs to decide when to fetch it, or it needs parameters the model chooses, make it a tool.
- If it is reference content the user or app selects (like attaching a file), make it a resource. Note that host support for resources and prompts varies; many hosts primarily use tools. If your audience's hosts do not surface resources, expose a read tool as well.
- Prompts are for user-initiated workflows, not for hiding instructions to the model.

The protocol also defines client-side features a server may request, such as asking the host's model to generate text (sampling) or asking the user for input (elicitation), and notifications for changes and progress. Support varies by host; check before depending on them.

### Transports

| Transport | Use when | Notes |
|---|---|---|
| **stdio** | Local server launched by the host as a subprocess | Simple; inherits the user's local permissions; stdout is the protocol channel — never print logs to stdout, use stderr |
| **HTTP-based streaming transport** | Remote/hosted server, multiple users, web deployment | Requires authentication, TLS, origin checks, session handling; check the current spec for the recommended HTTP transport (older HTTP+SSE transports have been superseded in recent versions) |

## Core principles

### 1. Design for the model as the user

The model sees tool names, descriptions, and schemas, and nothing else. Every rule from `ai-agents-and-tool-use` applies: specific verb-object names, descriptions that say when to use and when not to, precise schemas, compact results, actionable errors.

### 2. Expose intents, not your API surface

Do not mechanically map every REST endpoint to a tool. A server with eighty thin tools overwhelms the model's selection and context. Design around what users want to accomplish, combining multiple API calls inside one tool where that serves a single intent (e.g. `find_customer` that searches by email or name and returns key details including recent orders).

### 3. Least privilege, always

The server holds credentials to real systems and the model can be manipulated by content it reads. Every exposed tool is something an attacker who controls a web page or document the model reads might try to trigger. Expose the minimum, scope credentials narrowly, and separate read from write.

### 4. The server enforces; the model requests

Validation, authorisation, rate limits, and safety checks live in server code. Never rely on the tool description ("only use for the current user's records") to enforce anything.

### 5. Fail informatively

Tool errors should come back as tool results the model can read and act on, not as protocol crashes. Protocol-level errors are for protocol problems (unknown method, malformed request).

## Discovering context

- Which hosts must the server work with, and which MCP features do they support (tools only? resources? prompts? which transports? which auth flows)?
- Local or remote? Single user or multi-tenant?
- What upstream system is wrapped, its API, auth model, rate limits, and the permissions of the credentials available?
- What do users actually want to do? List the top five to ten tasks; these drive the toolset.
- Language and SDK: official SDKs exist for several languages; prefer the official SDK for the project's language. Follow existing project conventions for structure, config, and testing.

## Process

### 1. Define the capability set

From the user tasks, design a small toolset (often three to fifteen tools for a focused server). For each tool decide:

- name and one-sentence purpose;
- read-only or side-effecting; reversible or not;
- inputs the model will realistically have;
- what it returns;
- which upstream calls it makes;
- failure modes.

Mark tools with any available annotations or metadata the protocol provides for hints such as read-only or destructive behaviour, so hosts can present appropriate confirmation. Treat such hints as advisory: hosts may ignore them, and clients should not trust hints from untrusted servers.

### 2. Write schemas and descriptions

- Input schemas in JSON Schema (often generated from typed definitions in the SDK): types, enums, formats, required fields, defaults, descriptions per field with examples.
- Keep parameters few and natural. Prefer `email` or `order_number` over opaque internal IDs, or provide a lookup tool.
- Descriptions: what it does, when to use it, when to use a different tool, side effects, limits, examples.
- If the protocol version supports declaring output schemas or structured results, use them for machine-consumable outputs while keeping a readable text form.

### 3. Implement

Structure:

- Thin handler layer: parse and validate input, check authorisation, call domain logic, format result.
- Domain/service layer: the actual work, testable without MCP.
- Upstream client: retries, timeouts, rate-limit handling for the wrapped API.

Implementation rules:

- **Timeouts** on every upstream call; hosts and models wait poorly on hung tools.
- **Pagination and truncation**: cap result sizes; tell the model how to get more.
- **Idempotency** for writes where feasible, since models retry.
- **Long operations**: return quickly with a job reference and a status tool, or use progress notifications where supported.
- **Logging to stderr or files** for stdio servers — anything on stdout that is not protocol messages breaks the connection.
- **No secrets in results or logs.** Strip tokens, internal URLs, and sensitive fields from what is returned to the model.
- **Configuration** via environment variables or host-provided config, documented, with clear startup errors when missing.

### 4. Errors

| Error kind | How to return | Example message |
|---|---|---|
| Invalid input the model can fix | Tool result flagged as error, actionable text | "Date must be YYYY-MM-DD; got 'next Tuesday'." |
| Not found | Tool error with suggestion | "No project named 'apollo'. Available: apollo-web, apollo-api." |
| Permission denied | Tool error, clear and non-leaky | "You do not have access to that repository." |
| Upstream unavailable / rate-limited | Tool error indicating retry is possible, with wait time if known | "Upstream rate limit reached; retry after 30 seconds." |
| Bug in server | Tool error with a generic message; details to server logs | "Internal error (ref 8f2c). Please report." |

### 5. Authentication and authorisation

**Local (stdio) servers** run with the user's local privileges and typically read credentials (API tokens) from environment variables or the OS keychain. Document the minimum scopes needed. Never hard-code credentials or write them to logs.

**Remote servers** must authenticate clients. The MCP specification defines an OAuth-based authorisation flow for HTTP transports; read the current version for requirements on discovery, token handling, and audience validation. Key practices:

- Validate tokens on every request, including audience (the token was issued for *your* server) — do not accept tokens intended for another service.
- Do not pass the client's token through to upstream APIs ("token passthrough"); obtain separate upstream credentials appropriate to the user.
- Map the authenticated identity to upstream permissions so each user can do only what they could do directly.
- Enforce per-user rate limits and quotas.
- Use TLS; validate the request origin to prevent DNS-rebinding attacks against locally bound HTTP servers; bind local HTTP servers to localhost, not all interfaces.
- Sessions: generate unguessable session identifiers; never use a session ID as authentication.

See `authentication-and-authorization`.

### 6. Test

- **Unit tests** for domain logic and handlers, without the protocol.
- **Protocol-level tests** with the SDK's in-process or test client: list tools, call each tool with valid and invalid input, check errors.
- **Inspector tools**: use an MCP inspector (an interactive debugging client) to connect, view advertised capabilities, call tools manually, and see raw messages. This is the fastest way to debug "server will not connect" and schema problems.
- **Real host testing**: connect to the actual hosts your users use. Give the model realistic tasks and read what it does: which tools it picks, what arguments it passes, how it handles errors. Revise names and descriptions based on what you see.
- **Security tests**: attempts to access other users' data, path traversal in file tools, injection in query parameters, oversized inputs, and prompt-injection content in upstream data.

Common connection problems: wrong command or path in host config, missing environment variables, server printing to stdout (stdio), crash on startup visible only in stderr logs, protocol version mismatch, wrong URL or auth configuration for remote servers.

### 7. Package and document

- Distribution appropriate to the ecosystem (a package installable by a single command, a container image, or a hosted endpoint).
- A README covering: what the server does, the tool list with descriptions, required configuration and credential scopes, an example host configuration, security considerations, and known limitations.
- Version the server; note breaking changes to tool names or schemas, which break users' workflows and prompts.

## Security of exposed actions

MCP servers are a significant attack surface because they connect untrusted text (what the model reads) to real capabilities (what the server can do).

Threats and mitigations:

| Threat | Mitigation |
|---|---|
| **Prompt injection** via content the model reads (web pages, emails, issue comments returned by your own tools) triggering harmful tool calls | Least privilege; read/write separation; require host-side confirmation for destructive tools; mark destructive tools; consider sanitising or clearly delimiting untrusted fields in results |
| **Tool poisoning**: malicious servers with descriptions containing hidden instructions | As a client/host developer, show users tool descriptions, pin server versions, review third-party servers before installing, alert on description changes |
| **Confused deputy**: server acts with its own broad credentials on behalf of a user who lacks those rights | Per-user credentials or explicit per-user authorisation checks |
| **Data exfiltration**: model is induced to send private data to an attacker via a tool (e.g. fetch a URL with data in the query) | Restrict outbound destinations; avoid generic "fetch any URL" or "send to any address" tools in servers that also access sensitive data |
| **Path traversal / injection** in file, shell, or query tools | Validate and canonicalise paths against an allowlisted root; parameterised queries; never construct shell commands from model input |
| **Excessive data exposure** | Return only needed fields; redact secrets and PII where not required |
| **Credential leakage** | Secrets in environment or secret stores, never in results, logs, or error messages |
| **Denial of wallet / resource exhaustion** | Rate limits, result size caps, timeouts |

Avoid shipping maximally generic tools (run arbitrary shell, execute arbitrary SQL, fetch arbitrary URL) unless that is the explicit, understood purpose, the server runs in a sandbox, and users are warned. Narrow tools are both safer and easier for models to use correctly.

## Worked reasoning: designing a toolset for a ticketing system

Illustrative. The ticketing API has about forty endpoints. A naive server exposes forty tools: `get_ticket`, `list_tickets`, `get_ticket_comments`, `list_users`, `get_user`, `update_ticket_field`, and so on. In testing, the model calls `list_tickets` with no filter (thousands of results), confuses `get_user` and `list_users`, and needs four calls to answer "what's the status of the login bug?".

Redesign around intents:

- `search_tickets(query, status?, assignee_email?, updated_since?)` — full-text and filtered search; returns up to 20 compact rows (id, title, status, assignee, updated) and says how to narrow further.
- `get_ticket(ticket_id)` — one ticket with description, key fields, and the latest few comments; notes how many older comments exist.
- `add_comment(ticket_id, body)` — side-effecting, reversible-ish; marked as a write.
- `update_ticket(ticket_id, status?, assignee_email?, priority?)` — side-effecting; validates allowed transitions server-side; accepts emails rather than internal user IDs.
- A resource for the team's ticket workflow (statuses and their meanings), for hosts that support resources, plus a mention of the valid statuses in `update_ticket`'s description for hosts that do not.

No delete tool: deleting tickets is rare, irreversible, and better done by humans in the ticketing UI. The remote server uses each user's own OAuth token for the ticketing API, so the model can never see or modify tickets the user could not.

Result: the status question now takes one or two calls, and the destructive surface is minimal.

## Designing resources well

When hosts support them, resources let users and applications attach context without the model spending tool calls:

- Use stable, meaningful URIs (a scheme and path that identify the content, such as a file path or a record type and ID); the same URI should always refer to the same logical content.
- Provide a name, description, and media type so hosts can display and choose them.
- Use resource templates (parameterised URIs) for families of resources, such as one per database table or per document.
- Keep individual resources reasonably sized; very large content should be split or summarised.
- Support change notifications or subscriptions for content that updates, where hosts use them.
- Apply the same access control as tools: listing and reading a resource must respect the user's permissions.

## Writing prompts for the server

If you expose prompts, make each one a genuine, user-invoked workflow with a clear name and description ("Review a pull request for security issues"), well-defined arguments (with descriptions and which are required), and content that references the server's own tools and resources by name so the model knows how to carry out the workflow. Do not use prompts to inject hidden instructions; hosts show them to users, and users must be able to understand what they will do.

## Performance

- Keep tool latency low: models and users wait on every call, and agents may make many in sequence.
- Reuse upstream connections and clients across calls rather than reconnecting per request.
- Cache stable lookups (schemas, user directories, configuration) with sensible expiry.
- Make independent tools safe to call in parallel; hosts may issue concurrent calls.

## Local server hygiene

- Start fast and fail clearly: validate configuration at startup and print actionable errors to stderr.
- Do not perform network or file actions beyond what the tools need; a local server inherits the user's full permissions, so its scope should be visibly narrow.
- For file-system servers, restrict operations to explicitly configured root directories and canonicalise paths before checking.
- Clean up child processes and temporary files on shutdown.
- If you bind a local HTTP port, bind to localhost only and validate the origin header.

## Versioning and compatibility

- Tool names and parameter meanings are a public interface: users' saved prompts, workflows, and host configurations depend on them. Add new optional parameters freely; rename or remove only with a deprecation period and a version bump.
- Advertise capability changes through the protocol's change notifications where supported, so hosts refresh tool lists.
- Test against the protocol versions your target hosts support; negotiate gracefully.

## Observability

- Log each tool invocation with timestamp, user or session (pseudonymised as needed), tool, validated arguments (with sensitive fields redacted), duration, outcome, and error category.
- Emit metrics: calls per tool, error rate, latency, upstream rate-limit hits. Tools that are never called or always fail are design signals.
- Correlate with host-side traces where possible to reconstruct why the model chose a call.

## Building clients and hosts

If you are on the other side, integrating MCP servers into an application:

- Present tools to the model with clear provenance (which server) and handle name collisions across servers.
- Obtain user consent before connecting servers and before executing tools with side effects; show the actual arguments.
- Treat server-provided descriptions and results as untrusted.
- Apply timeouts and cancellation to tool calls.
- Limit the number of tools in context; let users enable only the servers they need.
- Log tool invocations for audit.

## Pitfalls

- **One tool per API endpoint**, flooding the model with near-duplicates.
- **Thin descriptions** that do not say when to use the tool.
- **Logging to stdout** in a stdio server, corrupting the protocol stream.
- **Huge JSON dumps** as results.
- **Protocol errors for business failures**, so the model cannot recover.
- **Broad admin credentials** shared across all users of a remote server.
- **Token passthrough** and missing audience validation.
- **Generic dangerous tools** (shell, SQL, URL fetch) in a server that also touches private data.
- **Relying on descriptions or annotations for enforcement.**
- **Testing only with the inspector**, never with a real model doing real tasks.
- **Silent breaking changes** to tool names and schemas.
- **Assuming all hosts support resources, prompts, or other optional features.**
- **Stale protocol knowledge**: not checking the current specification.

## Quality bar and verification

A server is ready when:

- The toolset maps to real user intents and is small enough to choose from reliably.
- Every tool has a clear name, a description with when/when-not guidance, a precise schema, bounded results, and actionable errors.
- Read and write capabilities are separated; destructive tools are marked and require confirmation in the target hosts.
- Credentials are least-privilege, never logged or returned; remote servers validate tokens (including audience) and enforce per-user authorisation.
- File, query, and command inputs are validated against injection and traversal.
- Unit, protocol, inspector, and real-host tests pass; real-model trajectories were reviewed.
- Configuration and security considerations are documented.
- The implementation was checked against the current MCP specification version targeted.
