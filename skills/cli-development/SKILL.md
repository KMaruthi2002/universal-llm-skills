---
name: cli-development
description: >-
  Design and build command-line tools people and scripts can rely on:
  command and subcommand structure, flags and arguments, help text and error
  messages, exit codes, stdin/stdout/stderr discipline, human vs.
  machine-readable output (tables, JSON, colour, TTY detection), configuration
  precedence (flags, env vars, config files), interactivity and prompts,
  long-running operations, signals, cross-platform behaviour, testing, and
  packaging/distribution. Use when creating a CLI, adding commands or flags to
  one, improving help or errors, making output scriptable, or shipping a
  command-line tool. For one-off shell scripts use scripting-and-shell.
metadata:
  category: development
  related: scripting-and-shell, api-design, error-handling, testing-strategy, release-management, code-documentation, ux-writing, project-scaffolding
---

# CLI Development

A command-line tool has two kinds of users: people at a terminal and programs that call it. People need discoverability, clear feedback, and forgiving defaults. Programs need stable output, meaningful exit codes, and no surprises. A good CLI serves both without compromising either, and treats its commands, flags, and output as a public interface that others will build on.

## Scope

Covers designing and implementing reusable command-line tools in any language: interface design, I/O conventions, configuration, errors, interactivity, testing, and distribution.

Not covered:

- Quick one-off automation scripts — see `scripting-and-shell` (though its scripts benefit from several conventions here).
- Full-screen terminal UIs beyond prompts and progress — this skill touches them only briefly.
- Designing HTTP APIs the CLI might call — see `api-design` (many of the same interface-stability ideas apply).

## Core principles

### 1. The interface is a contract

Command names, flag names, argument order, output formats, and exit codes become dependencies the moment someone puts your tool in a script. Why: breaking them breaks automation silently and far from you. Design them deliberately, document them, and evolve them with deprecation rather than renaming freely.

### 2. Follow the conventions of the platform and the ecosystem

Users carry expectations from every other CLI they use: `--help`, `--version`, `-h`, `--` to end options, `-` meaning stdin, long flags with `--`, short flags with `-`, combining short flags (`-xvf`), exit code 0 for success. Why: conventions are free usability; every deviation costs every user a moment of confusion. Guidelines such as POSIX utility conventions, GNU long-option conventions, and community guides (e.g. clig.dev) describe them.

### 3. Stdout is for data, stderr is for everything else

The primary output — what a user would pipe to another program — goes to stdout. Progress, logs, warnings, prompts, and errors go to stderr. Why: this lets `tool | other-tool` work while the user still sees messages, and lets scripts capture results without parsing around chatter.

### 4. Be human-friendly by default, machine-friendly on request, and never ambiguous

Default output is for people (readable, maybe colourful, maybe a table). Provide a stable machine format (`--json` or similar, or plain line-oriented output) for scripts. Detect when output is not a terminal and drop decoration. Why: optimizing only for humans makes the tool unscriptable; optimizing only for machines makes it unpleasant to use.

### 5. Fail loudly, clearly, and early

Validate input before doing work; on error, say what went wrong, why, and what to do next, then exit non-zero. Why: silent failure or exit code 0 on error breaks scripts in the worst way — they continue with bad data.

### 6. Be safe by default

Destructive or expensive operations require confirmation in interactive use, an explicit flag in non-interactive use, and offer a dry run. Why: CLIs are fast and repeatable, which makes mistakes fast and repeatable too.

## Discovering context

Before building or changing a CLI:

- If the tool exists: read its current commands, flags, help output, and output formats; find who calls it (scripts, CI, other tools) — these constrain changes. Match its existing naming style (kebab-case flags, verb-noun vs. noun-verb subcommands) even if you would choose differently.
- Identify the language and argument-parsing library in use, or the ecosystem default if starting fresh (e.g. Python argparse, Click, Typer; Go cobra, urfave/cli, the standard `flag` package; Rust clap; Node commander, yargs, oclif; Java picocli; .NET System.CommandLine; shell `getopts`). Use the library's features (help generation, completion, validation) rather than hand-parsing.
- Identify the audience and environments: developers, operators, CI pipelines, end users on Windows/macOS/Linux, containers, air-gapped servers.
- If it is part of a family of tools (a company's CLIs, a framework's tooling), match the family's conventions for config locations, auth, output formats, and flags.

## Command structure

### Single-purpose vs. subcommands

- A tool that does one thing (`grep`, `jq`) takes flags and arguments directly.
- A tool that manages several resources or workflows uses subcommands (`git commit`, `kubectl get pods`, `docker image ls`).

Subcommand naming patterns:

| Pattern | Example | Fits |
|---|---|---|
| verb noun | `tool create project` | Tools with a few universal actions over many resource types |
| noun verb | `tool project create` | Tools with many resource types, each with its own actions; groups help by resource |
| flat verbs | `tool build`, `tool deploy` | Workflow tools with few concepts |

Pick one and use it consistently. Mixing patterns is the most common structural flaw.

Guidance:

- Use consistent verbs across resources: if it is `list` for one, do not make it `ls` for another and `show-all` for a third (aliases are fine; the canonical name should be consistent).
- Keep nesting shallow — two levels is usually enough.
- Avoid ambiguous near-synonyms as separate commands (`update` vs. `upgrade` doing different things).
- Do not allow arbitrary abbreviations of subcommands by prefix matching; it prevents adding new commands later without breaking someone's abbreviation. Explicit aliases are fine.
- Running the tool with no arguments should show brief usage (or do the obvious default action if there is one), not do something destructive.

### Arguments vs. flags

- **Positional arguments** for the primary, obvious inputs, especially when there are one or two (`cp SRC DEST`) or a list of the same kind (`rm FILE...`).
- **Flags** for everything optional, and for anything whose meaning would be unclear by position. Two positional arguments of different kinds are often fine; three is usually a sign that some should be flags.
- Every flag should have a long form (`--output`); give short forms (`-o`) only to frequently used flags, since the single-letter namespace is small and permanent.
- Use standard names where they exist: `-h/--help`, `--version`, `-v/--verbose` (or `-v` for version in some ecosystems — pick and be consistent), `-q/--quiet`, `-o/--output`, `-f/--force`, `-n/--dry-run` (beware: `-n` has other meanings in some tools), `--json`, `--no-color`, `--yes`/`-y` to skip confirmation, `--config`.
- Boolean flags: `--flag` to enable and `--no-flag` to disable, when the default might need overriding.
- Accept `--flag=value` and `--flag value`. Support `--` to end option parsing, so filenames starting with `-` can be passed.
- Accept `-` as a filename meaning stdin/stdout where file input/output is supported.
- Flags that take a list: repeatable (`--tag a --tag b`) is usually clearer than delimited (`--tags a,b`); if you use delimiters, document escaping.
- Prefer explicit names over clever ones: `--older-than 7d` is better than `--age -7`.
- Validate values early: enumerated choices, ranges, file existence, mutually exclusive flags. Report all problems in one message if practical.

## Help and documentation

Help text is the primary documentation for most users. It is read under time pressure, in a terminal.

Good help output:

- Starts with one line saying what the command does.
- Shows usage syntax (`tool deploy [OPTIONS] ENVIRONMENT`).
- Lists the most common flags first, or groups flags by purpose in larger tools. Shows defaults and allowed values.
- Includes a few **examples** of real invocations — users copy examples far more than they read flag descriptions.
- Points to fuller documentation (a URL or `man` page) and to subcommand help.
- Fits a typical terminal width (wrap around 80 columns, or to the detected width).

Behaviour:

- `-h` and `--help` work on every command and subcommand, and `tool help <command>` if the ecosystem expects it. Help goes to stdout and exits 0 when requested; usage shown because of an error goes to stderr and exits non-zero.
- On invalid usage, show a short error plus a hint (`Run 'tool deploy --help' for usage.`), not the full help wall.
- Suggest corrections for typos (`Unknown command 'delpoy'. Did you mean 'deploy'?`) — most parsing libraries support this.
- `--version` prints the version (and optionally build info) to stdout and exits 0.
- Generate help, man pages, shell completions, and the reference docs from the same command definitions so they cannot drift. Ship completions for common shells (bash, zsh, fish, PowerShell); most libraries generate them.

## Output

### Human output

- Lead with what the user needs. For a mutation, confirm what happened ("Created project 'atlas' (id prj_123)"). For a query, show the results. Do not print nothing on success if the user would wonder whether it worked — but also do not be chatty; `ls`-style tools rightly print only data.
- Tables for lists of records, aligned, with headers; truncate long fields to the terminal width with a way to see full values (`--wide`, `-o json`).
- Use colour and symbols to add meaning (errors red, success green, dim for secondary info), never as the only carrier of meaning — some users cannot see colour, and logs strip it.
- Disable colour and animations when: stdout/stderr is not a TTY, `NO_COLOR` is set (a widely adopted convention), `TERM=dumb`, or `--no-color` is passed. Some tools also honour `FORCE_COLOR` / `CLICOLOR_FORCE`.
- Show progress for operations longer than about a second or two (spinner or progress bar on stderr), and only when stderr is a TTY; in CI, print occasional plain status lines instead.
- Print paths, IDs, and URLs in forms users can copy and paste.

### Machine output

- Provide a structured output mode (`--json`, `--output json|yaml`, or a `--format` template) for anything scripts might consume. JSON is the most broadly useful.
- Machine output is a versioned contract: keep field names stable, add fields rather than renaming, and document the schema. Human output can change freely between releases; say so in docs, so nobody parses it.
- In machine mode, print only the data to stdout — no banners, progress, or warnings mixed in (those go to stderr).
- For list output in line-oriented mode, one record per line; offer null-delimited output (`-0`/`--null`) if values can contain newlines.
- Consider a `--quiet` mode that prints only essential identifiers (e.g. the ID of a created resource) for easy capture in shell variables.
- Stream large outputs rather than buffering everything; for JSON, newline-delimited JSON (one object per line) streams well.

## Exit codes

- `0`: success. Anything else: failure. Scripts and CI depend on this more than anything else you produce.
- Use a small, documented set of non-zero codes if callers need to distinguish failures. Common conventions: `1` general error, `2` usage error (invalid flags or arguments, as many parsing libraries and shells use). Some tools follow BSD `sysexits.h` (e.g. 64 usage, 65 data error, 69 unavailable, 75 temporary failure, 77 permission denied, 78 configuration error); choose one scheme and document it.
- Codes above 125 have shell meanings (126 not executable, 127 not found, 128+N killed by signal N — e.g. 130 for Ctrl-C/SIGINT); do not use them for your own errors, but do exit with 130 after handling SIGINT if you mimic shell behaviour.
- Partial success is a design decision: e.g. a batch where 3 of 100 items failed should usually exit non-zero and report which failed, unless a flag says otherwise. "Nothing to do" is usually success.
- Commands that test a condition (`tool check`, `diff`-like tools) may use exit codes as answers (0 = same/healthy, 1 = different/unhealthy, 2 = error); document it clearly.

## Errors

A good error message answers: what failed, why, and what the user can do.

- Weak: `Error: ENOENT`
- Strong: `Error: config file not found at ~/.config/tool/config.toml. Run 'tool init' to create one, or pass --config PATH.`

Guidance:

- Write errors to stderr, prefixed consistently (e.g. `error:`), and exit non-zero.
- Translate low-level errors (exceptions, system error codes, HTTP status codes) into the user's terms, keeping the original detail available with `--verbose`/`--debug` or in a log file.
- Do not print stack traces by default for expected errors (bad input, missing file, network down). Show them for unexpected internal errors, ideally with a hint to report a bug and the information to include.
- Put the most important information at the end of the output too, if there is a lot of output — users look at the last line.
- Never include secrets (tokens, passwords) in error messages or debug output; redact them.
- Warnings go to stderr and do not change the exit code unless a `--strict`-style flag says so.

## Input

- **Stdin**: if the tool processes data, accept it from stdin when no file is given or when `-` is passed. If the tool expects stdin and stdin is an interactive terminal, show a hint rather than appearing to hang.
- **Secrets**: never require secrets as flag values — they leak into shell history and process listings (`ps`). Accept them via environment variables, a file path (`--password-file`), stdin, a credential helper, or the OS keychain, or prompt with echo disabled.
- **Large or structured input**: accept files (`--file spec.yaml`) rather than enormous flag values.
- **Encoding**: treat input as UTF-8 by default where the platform allows, handle invalid bytes gracefully, and be careful with filenames, which on some systems are arbitrary bytes.

## Configuration

Common precedence, highest to lowest:

1. Command-line flags
2. Environment variables (e.g. `TOOL_OUTPUT=json`, with a consistent prefix)
3. Project-level config file (found in the current directory or a parent, e.g. `.toolrc`, `tool.toml`)
4. User-level config file (following platform conventions: XDG Base Directory on Linux, e.g. `~/.config/tool/`; `~/Library/Application Support/` or XDG-style on macOS; `%APPDATA%` on Windows)
5. System-level config (e.g. `/etc/tool/`)
6. Built-in defaults

Guidance:

- Document the precedence and every setting in one place; generate the reference from the same definitions if possible.
- Provide a way to see effective configuration and where each value came from (`tool config list --show-origin` or similar). It saves hours of debugging.
- Keep config file formats simple and common (TOML, YAML, JSON, INI); follow the ecosystem.
- Do not write config files without the user's action, and do not silently rewrite their formatting or comments if the tool edits config.
- Store credentials separately from general config, with restrictive file permissions (e.g. `0600`), or in the OS credential store.
- Respect standard environment variables where relevant: `NO_COLOR`, `TERM`, `PAGER`, `EDITOR`/`VISUAL`, `HTTP(S)_PROXY`/`NO_PROXY`, `TMPDIR`, `HOME`, `XDG_*`, `CI`.

## Interactivity

- Prompt only when stdin is a TTY. In non-interactive contexts (pipes, CI), never block waiting for input: fail with an error naming the flag that provides the value.
- Every prompt must have a flag equivalent, so everything can be scripted.
- Confirmations for destructive actions: describe exactly what will happen ("This will delete 14 objects in bucket 'prod-assets'"), default to "no", and accept `--yes`/`--force` to skip. For severe actions, consider requiring the user to type the resource name.
- Provide `--dry-run` for operations that change things, showing what would happen without doing it. Make dry-run output accurate — it must use the same code path for planning.
- Offer `--no-input` or detect `CI` to disable all prompts explicitly.
- Pagers: page long output only when stdout is a TTY, respect `PAGER`, and provide `--no-pager`.

## Long-running operations, signals, and robustness

- Handle Ctrl-C (SIGINT) and SIGTERM: stop promptly, clean up temporary files and child processes, leave no partial outputs that look complete (write to a temporary file and rename atomically), and exit non-zero. A second Ctrl-C should force exit.
- Make operations idempotent or resumable where possible (re-running after a failure should not duplicate work or corrupt state).
- Set timeouts on network operations, with a flag to adjust them; retry transient failures with backoff and say that you are retrying.
- Handle a closed stdout pipe (e.g. `tool | head`) gracefully: SIGPIPE/EPIPE should end the program quietly, not print a stack trace.
- Do not assume a particular current working directory; resolve paths relative to where the user ran the command unless documented otherwise.
- Avoid slow startup: CLIs are invoked often and in loops. Lazy-load heavy modules, avoid network calls at startup, and measure startup time (aim for well under a few hundred milliseconds for frequently used commands).
- Update checks and telemetry: if present, make them opt-in or clearly disclosed with an easy opt-out, never block on them, and disable them in CI. Respect the user's privacy and network constraints.

## Cross-platform behaviour

- Paths: use the language's path library; do not hardcode `/` or `\`. Handle spaces and Unicode in paths.
- Line endings: accept both LF and CRLF in input; emit the platform's or LF consistently per the tool's purpose.
- Terminal capabilities differ: Windows terminals now support ANSI colours in most cases, but detect and degrade gracefully.
- Shell quoting differs between POSIX shells, PowerShell, and cmd; examples in docs should note this if relevant.
- Executable naming (`.exe`), config locations, and home directory conventions differ; use platform-aware libraries.
- Test on every platform you claim to support, ideally in CI.

## Worked example: designing a cleanup command

Illustrative. A team's deployment tool needs a command to delete old build artifacts.

First draft: `tool cleanup 30` — deletes artifacts older than 30 days, prints each filename as it goes, exits 0.

Problems: the `30` is unexplained (days? count?); it is destructive with no confirmation; progress and results are mixed on stdout; failures on individual files are printed and ignored with exit 0; there is no way to preview.

Revised design:

- `tool artifacts prune --older-than 30d` — matches the tool's existing noun-verb structure; an explicit, unit-bearing flag.
- `--dry-run` lists what would be deleted (same selection code path) and exits 0.
- Interactive: prints a summary to stderr ("Will delete 214 artifacts, 18.3 GB, from 'builds-prod'. Continue? [y/N]"), defaulting to no. Non-interactive without `--yes`: exits 2 with "refusing to delete without --yes in non-interactive mode".
- Stdout: the deleted artifact IDs, one per line (or a JSON array with `--json`), so scripts can log them. Stderr: progress bar when on a TTY, final summary line.
- Partial failure: continues past individual errors, reports each on stderr, and exits 1 with "deleted 210 of 214; 4 failed (see above)".
- Ctrl-C: stops after the current deletion, prints how many were deleted, exits 130.
- Help includes two examples: a dry run and a CI invocation with `--yes --json`.

Each change maps to a principle: explicit flags (contract), stdout/stderr separation, safety by default, honest exit codes.

## Evolving the interface

- Add, don't change: new flags and subcommands are safe; renaming or changing meaning is breaking.
- Deprecate before removing: keep the old name working, print a deprecation warning to stderr naming the replacement and the version it will be removed in, and document it in the changelog.
- Version the tool with semantic versioning, treating the command interface and machine output formats as the public API.
- Do not change default behaviour in ways that turn safe invocations into destructive ones.

## Testing

- **Unit-test the logic** separately from argument parsing and I/O: structure commands so the core functions take typed inputs and return results, with a thin CLI layer on top.
- **Test the CLI layer end to end**: invoke the command (in-process via the library's test runner, or as a subprocess) and assert on stdout, stderr, and exit code separately. Most CLI libraries provide test helpers (e.g. Click's `CliRunner`, cobra's command execution with buffers, assert_cmd for Rust).
- **Snapshot/golden tests** for help text and human output catch accidental changes; review snapshot updates deliberately.
- **Contract tests for machine output**: parse the JSON and check fields, so format regressions fail loudly.
- Test non-TTY behaviour (no colour, no prompts), `NO_COLOR`, missing config, invalid flags, stdin input, Ctrl-C handling where practical, and error exit codes.
- Use temporary directories and controlled environment variables for each test; never let tests read the developer's real config or credentials, or hit production services.

## Packaging and distribution

Choose based on audience:

| Channel | Fits | Notes |
|---|---|---|
| Language package manager (e.g. pip/pipx/uv tool, npm, cargo install, go install, gem) | Developers in that ecosystem | Requires the runtime; easy updates |
| Single static binary (Go, Rust, or bundled runtimes) via release downloads | Broad audiences, servers, CI | Provide checksums and signatures; build per OS/architecture |
| OS package managers (e.g. Homebrew, apt/deb, rpm, winget, Scoop, Chocolatey) | End users and operators | More release work; best install experience |
| Container image | CI and environments with containers | Heavy for interactive use |

Guidance:

- Make installation one command and `--version` honest (embed the version and commit at build time).
- Publish checksums, and sign artifacts where the ecosystem supports it; users and security teams increasingly verify them. Avoid encouraging piping a remote script directly to a shell without at least offering a verifiable alternative.
- Keep runtime dependencies minimal; each one is an install failure waiting to happen on someone's machine.
- Automate releases from tags in CI so every platform build is reproducible. See `release-management`.
- Provide an upgrade path and mention breaking changes in release notes.

## Pitfalls

- Mixing logs or progress into stdout, breaking pipes and JSON consumers.
- Exit code 0 on failure (often from catching every exception and printing it).
- Prompts that hang in CI because stdin is not a TTY.
- Secrets accepted as flag values.
- Colour and spinners written to files and CI logs.
- Inconsistent naming: `--dry-run` here, `--dryrun` there, `-n` in a third command meaning something else.
- Too many positional arguments with non-obvious order.
- Breaking flag or output changes in a minor release.
- Destructive default actions, or a destructive command that runs when given no arguments.
- Help text that lists every flag but gives no examples.
- Error messages that show a stack trace or a low-level code without saying what to do.
- Slow startup from eager imports or network calls.
- Tests that depend on the developer's real home directory or config.

## Quality bar and verification

Before declaring a CLI change done, actually run it and check:

- `--help` on every new or changed command is accurate, includes examples, and fits the terminal; `--version` works.
- Primary output goes to stdout and everything else to stderr: `tool ... 2>/dev/null` shows only data and `tool ... >/dev/null` shows only messages.
- Exit codes: 0 on success; documented non-zero codes on usage errors and failures — check with `echo $?` (or the platform equivalent) for success and at least one failure.
- Piped/non-TTY output has no colour, spinners, or prompts; `NO_COLOR` is honoured; machine output parses.
- Destructive actions confirm interactively, require `--yes` (or similar) non-interactively, and offer a dry run.
- Configuration precedence works as documented (flag beats env beats file).
- Ctrl-C during a long operation stops cleanly without leaving corrupted outputs.
- Tests cover stdout, stderr, and exit codes for success and failure paths; help/output snapshots are updated deliberately.
- Existing scripts' usages still work, or breaking changes are deprecated and documented.

When reporting, show a short example session (command and output) for the new behaviour, list any interface changes and their compatibility impact, and state which platforms were tested.
