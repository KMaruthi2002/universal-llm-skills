---
name: scripting-and-shell
description: >-
  Write robust, safe, maintainable scripts in shell (bash, zsh, POSIX sh),
  PowerShell, or a scripting language such as Python: strict modes, quoting,
  argument parsing, idempotency, dry-run flags, logging, portability between
  GNU, BSD/macOS and Windows, safe destructive operations, and knowing when a
  script has outgrown the shell. Use when asked to write, fix, review or harden
  a shell script, one-liner, Makefile recipe, install/setup script, glue
  script, or "a quick script to..." automate something on a machine.
metadata:
  category: automation
  related: cli-development, text-processing-and-regex, scheduled-jobs, workflow-automation, error-handling, secure-coding, ci-cd-pipelines
---

# Scripting and Shell

Scripts are the most-copied, least-reviewed code in most organisations. They start as "just a quick thing", get run from cron, CI, or a colleague's laptop, and eventually delete the wrong directory because a variable was empty. This skill is about writing scripts that behave predictably on the second, hundredth and thousandth run, on machines other than yours, with inputs you did not anticipate.

## Scope

Covers: shell scripts (bash, zsh, POSIX `sh`), PowerShell scripts, and short scripting-language programs (Python, Ruby, Node, Perl) used as glue; install and bootstrap scripts; Makefile and task-runner recipes; one-liners that will be saved and reused.

Not covered here:
- Building a polished command-line *product* with subcommands, help, completion and distribution: `cli-development`.
- Regex construction and text transforms in depth (sed, awk, jq): `text-processing-and-regex`.
- Running scripts on a schedule, locking and alerting: `scheduled-jobs`.
- Multi-step business workflows spanning services: `workflow-automation`.
- CI pipeline structure: `ci-cd-pipelines`.

## Core principles

1. **Fail loudly and early.** A script that continues after a failed step does damage with partial state. The default in most shells is to ignore failures, so you must opt in to strictness. Why: the cost of a script stopping unexpectedly is a rerun; the cost of it continuing is often data loss.

2. **Every variable expansion is a potential injection or split.** In shells, unquoted `$var` is word-split and glob-expanded. A filename with a space or a `*` becomes several arguments or a list of files. Quote by default; unquote only deliberately.

3. **Make reruns safe (idempotency).** Scripts get rerun after partial failure, by a second person, or by a retrying scheduler. Each step should check "is this already done?" or be naturally repeatable (`mkdir -p`, `ln -sfn`, upserts). Why: you cannot always know how far the previous run got.

4. **Preview before you destroy.** Anything that deletes, overwrites, moves, sends, or bills should support a dry run and should print exactly what it will touch. Humans catch wrong targets when they see the list; they do not catch them in code.

5. **Assume a different machine.** The next runner has a different OS, shell version, locale, `PATH`, working directory, and user. State and check your assumptions at the top of the script instead of discovering them halfway.

6. **Shell is for orchestrating programs, not for computing.** Shell is excellent at running commands, wiring pipes and moving files. It is poor at data structures, error handling, arithmetic, and parsing. When the logic dominates the command-running, switch languages.

## Discovering context first

Before writing or editing a script in an existing project:

- **Look for existing scripts** (`scripts/`, `bin/`, `tools/`, `Makefile`, `justfile`, `package.json` scripts, `Taskfile`). Match their shell (bash vs sh vs PowerShell), their strict-mode header, logging helpers, and argument style. A new script that looks different from its siblings is harder to maintain.
- **Find the target environments.** Developer laptops (often macOS with BSD tools and an old bash 3.2, or zsh as the login shell), Linux CI images (GNU tools, sometimes busybox/Alpine with `ash`), Windows (PowerShell 5.1 vs 7, or Git Bash/WSL). The answer decides portability work.
- **Check for a linter or formatter config** (e.g. ShellCheck directives, `.editorconfig`, PSScriptAnalyzer settings, a Python formatter). Follow it.
- **Ask who runs it and how**: by hand, CI, cron, a container entrypoint, as root? Interactive scripts can prompt; unattended ones must not.

If you cannot inspect the environment, state your assumptions explicitly in the script header and in your reply.

## Choosing the language

| Situation | Reasonable choice | Why |
|---|---|---|
| Run a sequence of commands, move files, set env, call CLIs | Shell (bash or POSIX sh) | Native fit; minimal dependencies |
| Must run on minimal containers / busybox / init systems | POSIX `sh` | bash may not exist |
| Windows-first admin tasks, AD, registry, .NET objects | PowerShell | Object pipeline, native APIs |
| Parsing JSON/YAML/CSV beyond trivial `jq` filters | Python/Node/etc. | Real parsers, real data structures |
| More than ~100–150 lines of logic, functions calling functions, arrays of records | Scripting language | Testability, error handling, readability |
| Concurrency, retries with backoff, HTTP APIs with auth | Scripting language | Shell versions are fragile and hard to test |
| Needs to be fast and distributed as a binary | Compiled language (see `cli-development`) | No runtime dependency |

**Signals a shell script should be rewritten:** nested data handling with `awk`/`sed` chains you cannot read back; associative arrays used as records; string-built JSON; more than a couple of `trap` handlers; you are writing a retry loop around `curl` with token refresh; the script needs unit tests. These are not prohibitions, just the point where the shell's costs start exceeding its convenience.

Shell vs PowerShell: PowerShell passes objects, not text, so most quoting and parsing problems of bash disappear, but it has its own pitfalls (see below). Choose the shell the target environment and the team already use.

## The safe shell header

For bash, a common strict header:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
```

What each part does and its caveats (understand these; do not cargo-cult them):

- `-e` (errexit): exit when a command fails. **Caveats:** it is suppressed inside `if`, `while`, `&&`/`||` lists, and in functions called from those contexts; commands in `$(...)` assigned with `local x=$(cmd)` lose their status because `local` succeeds. Write `local x; x=$(cmd)`.
- `-u` (nounset): error on unset variables. Catches typos like `$TARGTE_DIR`. Use `${VAR:-default}` for intentionally optional values. Old bash (< 4.4) treats `"${arr[@]}"` of an empty array as unset; guard with `${arr[@]+"${arr[@]}"}` if you must support bash 3.2 (macOS default).
- `-o pipefail`: a pipeline fails if any stage fails, not only the last. Without it, `curl ... | jq ...` "succeeds" when curl fails. Caveat: `cmd | head -1` can now fail with SIGPIPE on the writer; handle explicitly when that matters.
- `-E` (errtrace): makes `ERR` traps fire inside functions.
- `IFS=$'\n\t'`: stops word-splitting on spaces. Helpful as a safety net, but **quoting is still required**; changing IFS also changes how `read` and `"$*"` behave, so be deliberate.

POSIX `sh` has `set -eu` and (in recent POSIX and most shells) `set -o pipefail`; check your target shell. zsh has different defaults (no word-splitting of unquoted parameters by default, arrays are 1-indexed); if you write for zsh, say so in the shebang and do not assume bash semantics.

PowerShell equivalents:

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
# PowerShell 7.3+: also consider $PSNativeCommandUseErrorActionPreference = $true
# so non-zero exit codes from external programs raise errors.
```

Without the last line, a failing external executable (e.g. `git`, `az`) does not stop the script; check `$LASTEXITCODE` explicitly on older versions.

Python as a script language: let exceptions propagate (they exit non-zero with a traceback), use `subprocess.run([...], check=True)` with a list of arguments rather than `shell=True`, and use `argparse` for flags.

## Quoting and expansion

Rules that prevent most shell bugs:

- Quote every expansion: `"$var"`, `"$(cmd)"`, `"${arr[@]}"`. Exceptions are rare and should be commented.
- Use arrays to build commands, never strings:

```bash
args=(--recursive --exclude '*.tmp')
[[ $verbose == 1 ]] && args+=(--verbose)
rsync "${args[@]}" "$src/" "$dest/"
```

  Building `cmd="rsync $opts $src"` and running `$cmd` or `eval "$cmd"` breaks on spaces and invites injection.
- Never `eval` input you did not construct. If you think you need `eval`, you usually need an array, an indirect expansion, or a different language.
- Use `--` to end options before user-supplied paths: `rm -- "$file"`, `grep -- "$pattern" "$file"`. A file named `-rf` is otherwise an option.
- Prefix globs with `./` when iterating the current directory: `for f in ./*` so names starting with `-` are safe.
- Handle "no match" globs: in bash an unmatched `*.log` stays literal. Use `shopt -s nullglob` or test `[[ -e $f ]]` inside the loop.
- Use `printf '%s\n' "$x"` instead of `echo "$x"` for arbitrary data; `echo` interprets `-n`, `-e` and backslashes inconsistently across shells.
- In `[[ ]]` the right side of `==` is a pattern; quote it to compare literally: `[[ $a == "$b" ]]`.

Filenames can contain spaces, newlines, leading dashes, and non-UTF-8 bytes. When processing lists of files, use null delimiters end to end:

```bash
find "$dir" -type f -name '*.csv' -print0 |
  while IFS= read -r -d '' f; do
    process "$f"
  done
```

Avoid `for f in $(ls ...)` and `for f in $(find ...)`; both split on whitespace and glob-expand results.

## Arguments and configuration

- Validate early. Check required arguments, file existence, and value formats before doing any work. Print a usage message and exit with a non-zero code (conventionally 2 for usage errors).
- Prefer explicit flags over positional magic for anything beyond one or two arguments. `getopts` handles short options portably in POSIX sh/bash; long options need a manual `while/case` loop or a scripting language's argument parser.
- Accept configuration in a clear order of precedence: flags > environment variables > config file > defaults. Document which env vars are read.
- Never accept secrets as command-line arguments: they appear in process listings (`ps`), shell history, and CI logs. Read them from environment variables, a file with restricted permissions, or a secret manager.
- Provide `-h/--help`. A heredoc usage text at the top doubles as documentation.

Illustrative pattern for long options in bash:

```bash
dry_run=0
target=""
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--dry-run) dry_run=1; shift ;;
    -t|--target)  target=${2:?--target needs a value}; shift 2 ;;
    -h|--help)    usage; exit 0 ;;
    --)           shift; break ;;
    -*)           echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *)            break ;;
  esac
done
[[ -n $target ]] || { echo "--target is required" >&2; exit 2; }
```

## Idempotency patterns

| Operation | Non-idempotent | Idempotent alternative |
|---|---|---|
| Create directory | `mkdir dir` | `mkdir -p dir` |
| Symlink | `ln -s a b` | `ln -sfn a b` (check flags on your platform) |
| Append config line | `echo line >> file` | `grep -qxF line file \|\| echo line >> file` |
| Install package | install unconditionally | check `command -v tool` or the package manager's state first |
| Create cloud/db resource | `create` | "create if not exists", or describe-then-create, or an upsert API |
| Download | always fetch | fetch to temp, verify checksum, move into place only if changed |
| Edit file in place | `sed -i` repeatedly | write the full desired content, or use a marker block you replace |

Write outputs atomically: write to a temp file in the same directory, then `mv` it over the target. `mv` within one filesystem is atomic, so readers never see a half-written file.

```bash
tmp=$(mktemp "${out}.XXXXXX")
trap 'rm -f -- "$tmp"' EXIT
generate > "$tmp"
mv -f -- "$tmp" "$out"
```

## Temporary files and cleanup

- Use `mktemp` / `mktemp -d`, never fixed names like `/tmp/out.txt` (collisions between concurrent runs, and symlink attacks in shared `/tmp`).
- Register cleanup with `trap '...' EXIT` immediately after creating the resource. The EXIT trap runs on normal exit and on `-e` failures; add `INT TERM` handling if you need to forward signals to children.
- Do not leave background processes running: track their PIDs and kill/wait on exit.

## Logging and output

- **stdout is for data, stderr is for humans.** Scripts are composed in pipelines; progress messages on stdout corrupt the next command's input.
- Log what you are about to do, with the actual values: `log "deleting 42 files under /var/app/cache"`. "Done!" without context is useless in a CI log.
- Add a timestamp and level when output goes to files or schedulers. Keep it greppable.
- Support `-v/--verbose` and `-q/--quiet` rather than commenting out echo lines. `set -x` (xtrace) is a useful debug switch; enable it behind a flag (`[[ ${DEBUG:-} ]] && set -x`) and remember it prints secrets too.
- Exit codes are the contract with callers: 0 success, non-zero failure, distinct codes for distinct failure classes if callers need to react differently. Document them.
- Never print secrets. Mask tokens in logs (`${token:0:4}…`), avoid `set -x` around commands that include credentials, and beware of error messages that echo full URLs with embedded keys.

## Dry-run and confirmation for destructive operations

Destructive means: deletes, overwrites, truncates, moves out of place, drops tables, revokes access, sends messages, triggers payments, or calls any API that changes remote state.

A good dry-run:
- Is selected by a flag (`--dry-run`/`-n`) and, for dangerous scripts, is the **default** with `--apply`/`--yes` required to act.
- Runs all the same discovery and validation code as the real run, and prints the exact list of targets and actions. Only the mutating calls are skipped.
- Is implemented with a single wrapper so it cannot drift:

```bash
run() {
  if (( dry_run )); then
    printf 'DRY-RUN:'; printf ' %q' "$@"; printf '\n'
  else
    "$@"
  fi
}
run rm -rf -- "$build_dir"
```

Guard rails for deletes (each one has prevented real outages):
- `rm -rf "$dir/"*` with an empty `$dir` becomes `rm -rf /*`. Use `${dir:?}` to abort when empty: `rm -rf -- "${dir:?}/"*`.
- Refuse obviously dangerous targets: `/`, `$HOME`, the repo root, paths shorter than some sanity length, paths outside an expected prefix. Resolve to an absolute canonical path first and check it is under the allowed root.
- Count before acting and abort if the count exceeds an expected bound ("about to delete 48,213 files; expected < 1000; pass --force to continue").
- Prefer moving to a quarantine/trash location with a retention period over immediate deletion when the data matters.
- For interactive runs, confirm with the specific summary ("Delete 12 files from prod-bucket? [y/N]"); for unattended runs, require an explicit flag instead of prompting.
- If an assistant or agent is running the script on someone's behalf, run the dry run first, show the output, and get explicit approval before the real run. Do not run destructive commands against production or a user's real data on your own initiative.

## Portability: GNU vs BSD/macOS vs Windows

Common traps when the same script runs on Linux (GNU coreutils) and macOS (BSD userland):

| Task | GNU (Linux) | BSD (macOS) | Portable approach |
|---|---|---|---|
| In-place sed | `sed -i 's/a/b/' f` | `sed -i '' 's/a/b/' f` | Write to temp and `mv`, or use `perl -pi -e` |
| Extended regex in sed | `sed -E` (also `-r`) | `sed -E` | Use `-E` |
| Date arithmetic | `date -d '1 day ago'` | `date -v-1d` | Compute in a scripting language, or detect the platform |
| File size / mtime | `stat -c %s` | `stat -f %z` | `wc -c < file`; scripting language for mtime |
| `readlink -f` | available | only on newer macOS | `cd "$(dirname "$p")" && pwd -P`, or `realpath` if present |
| `grep -P` (PCRE) | usually available | not available | `grep -E`, or `perl` |
| `xargs -r` (no-run-if-empty) | available | default behaviour, flag absent in older versions | Check emptiness first |
| `find -printf` | available | not available | `-exec stat ...` or a scripting language |
| `mktemp` template | flexible | requires `X`s; `-t` semantics differ | Always pass an explicit template |
| bash version | 4.x/5.x | 3.2 at `/bin/bash` (newer via package managers) | Avoid associative arrays, `mapfile`, `${var,,}` if 3.2 must work |

Other portability notes:
- Use `#!/usr/bin/env bash` when bash may live in different places; use `#!/bin/sh` only when the script is genuinely POSIX (test it with a strict POSIX shell such as `dash`).
- Set `LC_ALL=C` for byte-wise sorting and predictable regex character classes when processing data; leave locale alone when handling user-facing text.
- Line endings: scripts edited on Windows with CRLF fail on Unix with confusing errors (`$'\r': command not found`). Enforce LF via `.gitattributes` or editor config.
- PowerShell on Windows vs PowerShell 7 cross-platform differ in default encodings, available modules, and aliases (`curl`, `ls` are aliases on Windows PowerShell 5.1). Use full cmdlet names in scripts.
- Paths: never hard-code `/` vs `\` in cross-platform PowerShell or Python; use `Join-Path` / `pathlib`.

## Working directory and environment

- Do not assume the current directory. Resolve paths relative to the script: `script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)`.
- If the script `cd`s, check it succeeded (`cd "$dir" || exit`) even under `-e`, and prefer subshells `( cd "$dir" && ... )` so the change does not leak.
- Check required tools up front: `command -v jq >/dev/null || { echo "jq is required" >&2; exit 127; }`. Avoid `which`, whose behaviour varies.
- Cron, systemd, CI and containers run with a minimal `PATH` and no interactive profile. Set `PATH` explicitly or use absolute paths for critical binaries.
- Be explicit about which user the script runs as. Refuse to run as root when it does not need to (`[[ $EUID -eq 0 ]] && die "do not run as root"`), and use `sudo` for the specific commands that do.

## Running remote and privileged commands

- Over SSH, pass commands as a single quoted argument and be aware that the remote shell re-parses it. Prefer copying a script and executing it, or `printf %q` to quote arguments.
- `curl ... | bash` executes whatever the server returns, possibly a truncated download. When you control the installer, offer a download-then-verify-then-run path (checksum or signature). When you consume one, read it first.
- Least privilege: request only the permissions the script needs; avoid `chmod 777`; create files with restrictive `umask` when they may contain secrets (`umask 077`).

## PowerShell-specific pitfalls

- Functions return everything written to the output stream, not just the `return` value. Stray command output pollutes return values; pipe to `Out-Null` or assign to `$null`.
- `-WhatIf` and `-Confirm` are the native dry-run/confirmation mechanism. Implement `[CmdletBinding(SupportsShouldProcess)]` and wrap changes in `if ($PSCmdlet.ShouldProcess($target, 'Delete'))`.
- Comparison operators are `-eq`, `-lt`, etc.; `>` is redirection and silently creates a file named after the right-hand side.
- Arrays of one element unroll to a scalar; wrap with `@(...)` when you need a count.
- Execution policy is a convenience guard, not security; do not instruct users to disable it globally. Sign scripts or set the policy for the process scope if needed.
- Quoting for native executables changed across versions; test arguments containing quotes or spaces on the PowerShell version you target.

## Python-as-glue pitfalls

- `subprocess.run(cmd, shell=True)` reintroduces every shell-quoting problem; pass a list instead.
- Check exit codes (`check=True`) and capture stderr for error messages.
- Use `pathlib`, `shutil`, `tempfile` instead of shelling out to `cp`/`mv`/`mktemp`.
- Pin the interpreter assumption (`#!/usr/bin/env python3`) and avoid non-stdlib dependencies in bootstrap scripts, or document how to install them.

## Process: writing a script

1. **Write down the contract**: inputs (args, env, files), outputs (files, stdout, exit codes), side effects, who runs it, where. One comment block at the top is enough.
2. **Choose the language** using the table above.
3. **Start from a strict header** and the project's existing helpers.
4. **Parse and validate inputs** before touching anything.
5. **Discover, then act**: compute the full list of targets first, print it, then apply. This makes dry-run trivial and makes the log meaningful.
6. **Make each step idempotent** or guarded.
7. **Add cleanup traps** at the moment you create temp resources.
8. **Lint** (e.g. ShellCheck for shell, PSScriptAnalyzer for PowerShell, a linter/type checker for Python). Treat warnings as bugs unless you can justify each suppression in a comment.
9. **Test the edges** (below), on every target platform if you can.

When reviewing an existing script, read it with the pitfalls list in hand and run it in dry-run or against a scratch directory before changing it.

## Pitfalls and anti-patterns

- **Unquoted variables in `rm`, `mv`, `cp`, `chmod`, `chown`.** The single largest source of destructive script bugs.
- **`cd` without checking**, followed by destructive commands in the wrong directory.
- **Parsing `ls` output** for filenames.
- **Ignoring pipeline failures** (no `pipefail`), so `download | extract` reports success on a failed download.
- **`local var=$(cmd)` masking failures** under `set -e`.
- **Reading a file while writing it**: `sed 's/a/b/' f > f` truncates `f` before sed reads it.
- **`while read` without `-r` and `IFS=`**, which mangles backslashes and trims whitespace.
- **Command substitution stripping trailing newlines**, which matters for exact file content.
- **Interactive prompts in unattended contexts**: a script waiting on `read` in CI hangs until timeout.
- **Hard-coded absolute paths** to one person's home directory.
- **String-built JSON** (`"{\"name\": \"$name\"}"`) breaking on quotes; use `jq -n --arg name "$name" '{name:$name}'` or a real language.
- **Secrets in argv, logs, or `set -x` output.**
- **Retry loops without limits or backoff**, hammering a failing service forever.
- **Assuming GNU flags** on macOS or busybox.
- **Silent `|| true`** sprinkled to make errors go away; handle the specific expected failure instead (`grep ... || [[ $? -eq 1 ]]`).

## Verification

Before calling a script done:

- [ ] Linter passes (or every suppression is justified).
- [ ] Runs from a different working directory than the script's own.
- [ ] Handles: no arguments, `--help`, a missing required argument, an invalid value.
- [ ] Handles paths with spaces, a leading dash, and (if relevant) newlines and unicode.
- [ ] Handles the empty case: zero matching files, empty input, empty variable.
- [ ] Rerun immediately after a successful run is safe and reports "nothing to do" or equivalent.
- [ ] Interrupting midway (Ctrl-C, or killing a step) leaves no half-written outputs and cleans temp files; a rerun recovers.
- [ ] Dry-run output matches what the real run does (compare on a scratch target).
- [ ] Exit code is non-zero on every failure path you can trigger.
- [ ] Runs on each target platform (or you stated which ones you could not test).
- [ ] No secrets in arguments, logs, or committed files.

If you cannot execute the script, say so and list the exact commands the user should run to check it, including a dry run against a disposable directory.

## Reporting back

Tell the user: what the script does, how to run it (including the dry-run form), which platforms and shell versions you tested or assumed, what it deletes or changes, and any assumptions they need to confirm (paths, permissions, environment variables).
