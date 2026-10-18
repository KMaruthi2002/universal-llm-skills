---
name: text-processing-and-regex
description: >-
  Construct correct, readable, efficient regular expressions and perform text
  transformations safely: anchors, greediness, character classes, groups and
  lookarounds, regex flavor differences, catastrophic backtracking (ReDoS),
  Unicode and encodings; line-oriented tools such as grep, sed, awk, jq, yq and
  their GNU/BSD differences; using real parsers for JSON, CSV, HTML, XML, YAML
  and code instead of regex; and making bulk search-and-replace edits across
  many files without breaking them. Use when writing or debugging a regex,
  extracting fields from logs or text, transforming files with sed/awk/jq,
  doing a codebase-wide find-and-replace, or validating input formats.
metadata:
  category: automation
  related: scripting-and-shell, data-cleaning-and-validation, refactoring, web-scraping, secure-coding, etl-pipelines
---

# Text Processing and Regex

Regular expressions are a compact language for describing patterns in text. Their compactness is the problem: a pattern that looks right matches too much, too little, or takes exponential time on one unlucky input. Most text-processing mistakes come from three sources — not anchoring and bounding the pattern, using regex on structures it cannot parse, and making bulk edits without previewing them.

## Scope

Covers: writing and reviewing regexes in any flavor; extracting and transforming text with command-line tools and scripting languages; choosing a real parser; bulk edits across files.

Related:
- Shell mechanics (quoting, pipelines, portability) for the commands you write: `scripting-and-shell`.
- Validating and cleaning whole datasets: `data-cleaning-and-validation`.
- Structural code changes (renames, API migrations): `refactoring` — prefer language-aware tools there.
- Extracting data from web pages: `web-scraping` (use HTML parsers).

## Core principles

1. **Decide whether regex is the right tool.** Regex is excellent for flat, token-level patterns: identifiers, dates in a known format, log line fields, simple validation. It is the wrong tool for nested or context-dependent structure: HTML, XML, JSON, programming languages, quoted CSV. Use a parser for those. Why: these formats have rules (nesting, escaping, quoting) that regex can only approximate, and the approximation fails on real-world input.

2. **Be exactly as specific as the data.** Anchor patterns (`^…$`, `\b`), bound repetitions, and prefer explicit character classes (`[^"]*`, `\d{4}`) over `.*`. An under-constrained pattern matches things you did not intend; you will not see those matches unless you look for them.

3. **Test against counterexamples, not only examples.** Write down strings that must match and strings that must not, including edge cases. A regex that matches all your positive examples proves little.

4. **Mind the flavor.** POSIX BRE/ERE, PCRE, JavaScript, Python `re`, Go RE2, .NET and Java differ in syntax and features (lookbehind, possessive quantifiers, named groups, Unicode classes, backreferences). Check which engine runs your pattern.

5. **Preview bulk edits, then apply, then verify.** A replace across a repository is a large, mechanical change. See every match before changing it, keep changes reviewable (version control), and run the project's checks afterwards.

## Regex fundamentals that prevent bugs

### Anchors and boundaries

- `^` and `$` anchor to the start/end of the string — or of each line in multiline mode. For validation, anchor both ends, or the pattern matches a substring: `\d{3}` "validates" `abc12345xyz`.
- Many languages offer full-match APIs (`re.fullmatch` in Python, `matches()` in Java) which are clearer than manual anchors.
- In some flavors `$` matches before a trailing newline. Python's `\Z` and PCRE's `\z` mean the absolute end.
- `\b` is a word boundary, defined by the engine's notion of "word character" — ASCII-only in some flavors, Unicode-aware in others.

### Greedy, lazy and explicit classes

- `.*` is greedy: in `"a" and "b"`, the pattern `".*"` matches `"a" and "b"`, the whole thing.
- `.*?` (lazy) matches `"a"`, but lazy quantifiers still backtrack and are slower and less clear than saying what you mean.
- Best: a negated class that cannot overrun the delimiter: `"[^"]*"`.
- Remember `.` usually does not match newline unless a dotall/single-line flag is set.

### Groups

- Use non-capturing groups `(?:…)` for alternation and grouping when you do not need the capture; it clarifies intent and avoids shifting group numbers.
- Use named groups `(?P<year>\d{4})` / `(?<year>\d{4})` for anything with more than two captures.
- Alternation has the lowest precedence: `^cat|dog$` means `(^cat)|(dog$)`. Write `^(?:cat|dog)$`.

### Escaping

- Escape metacharacters (`. * + ? ( ) [ ] { } | \ ^ $`) when matching them literally. When inserting user or variable input into a pattern, use the language's escape function (`re.escape`, a regex-escape helper) — never interpolate raw input. Unescaped input is both a correctness bug and a security issue (ReDoS, pattern injection).
- Use raw strings or the language's regex literal syntax to avoid double-escaping (`r"\d+"` in Python).
- Inside a character class, most metacharacters are literal; `]`, `\`, `^` (at the start) and `-` (between characters) are not.

### Lookarounds

- Lookahead `(?=…)` / `(?!…)` and lookbehind `(?<=…)` / `(?<!…)` assert context without consuming it. Useful for "a number not followed by %", password-composition checks, or inserting thousands separators.
- Support varies: RE2/Go and POSIX tools lack them; JavaScript gained lookbehind relatively late; some engines require fixed-length lookbehind.
- If a pattern needs several lookarounds, consider splitting it into multiple simpler checks in code; it is usually clearer.

### Readability

For non-trivial patterns, use verbose/extended mode with comments, or build the pattern from named pieces:

```python
import re
LOG_LINE = re.compile(r"""
    ^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)\s+
    (?P<level>DEBUG|INFO|WARN|ERROR)\s+
    \[(?P<component>[\w.-]+)\]\s+
    (?P<message>.*)$
""", re.VERBOSE)
```

A regex nobody can read will not be maintained correctly; it will be replaced by a second regex that is also wrong.

### Flavor differences that most often matter

| Feature | POSIX BRE/ERE (grep, sed, awk) | PCRE / Perl | Python `re` | JavaScript | RE2 / Go / Rust `regex` |
|---|---|---|---|---|---|
| `\d`, `\w`, `\s` | Not in strict POSIX (use `[[:digit:]]` etc.); GNU tools accept some | Yes | Yes (Unicode by default for str) | Yes (ASCII unless `u`/`v` flag semantics apply) | Yes |
| Lazy quantifiers `*?` | No | Yes | Yes | Yes | Yes |
| Lookahead / lookbehind | No | Yes | Yes (fixed-width lookbehind) | Yes (modern engines) | No |
| Backreferences `\1` | BRE yes, ERE varies | Yes | Yes | Yes | No |
| Possessive / atomic | No | Yes | Python 3.11+ | No | Not needed (linear time) |
| Named groups | No | `(?<n>…)` | `(?P<n>…)` (and `(?<n>…)` not in older versions) | `(?<n>…)` | `(?P<n>…)` / `(?<n>…)` |
| Guaranteed linear time | Implementation-dependent | No | No | No | Yes |

When a pattern moves between tools (prototype in a tester, run in `grep`, deploy in Go), re-test it in the final engine.

## Catastrophic backtracking (ReDoS)

Backtracking engines (PCRE, Python, JavaScript, Java, .NET, Ruby) can take exponential time when a pattern offers many ways to match the same text and the overall match fails.

Danger signs:
- Nested quantifiers: `(a+)+`, `(\w*)*`, `(.*,)*`.
- Alternation with overlapping branches inside a repetition: `(a|a)*`, `(\w|\d)+`.
- Adjacent quantified pieces that can match the same characters: `\s*.*\s*$`, `\d+\d+x`.

Example: `^(\w+\s?)*$` against a long string of word characters followed by `!` tries an astronomical number of splits before failing.

Mitigations:
- Make alternatives mutually exclusive and repetitions unambiguous: `^\w+(?:\s\w+)*$`.
- Use negated classes instead of `.*` between delimiters.
- Use possessive quantifiers or atomic groups (`\w++`, `(?>…)`) where the flavor supports them.
- Bound input length before matching.
- For untrusted input in services, prefer a linear-time engine (RE2, Rust's `regex`, Go's `regexp`) or set a match timeout where available (.NET, some libraries).
- Test performance with adversarial inputs (long near-matches), not only typical ones.

Any regex applied to user-supplied input in a server is a potential denial-of-service vector; treat it as security-relevant (see `secure-coding`).

## Unicode and encodings

- **Know the encoding** of your input. Decode bytes to text explicitly (usually UTF-8) at the boundary, and handle invalid bytes deliberately (error, replace, or preserve as bytes). Mojibake (`Ã©` for `é`) means a decode used the wrong encoding.
- **Character classes differ by mode**: `\w`, `\d`, `\b` may be ASCII-only or Unicode-aware. In Unicode mode, `\d` can match Arabic-Indic and other digits — surprising when you then parse with `int()` or expect ASCII. Use `[0-9]` when you mean ASCII digits.
- **Case-insensitivity** is locale- and Unicode-dependent (Turkish dotless i, German ß). Use the engine's Unicode case folding when matching human text.
- **Normalisation**: "é" can be one code point or `e` plus a combining accent. Normalise (NFC usually) before comparing or matching user text.
- **Grapheme clusters**: one visible character (emoji with skin tone, flags) can be several code points; `.` matches one code point. Use grapheme-aware libraries for "first N characters" on user text.
- **Line endings**: CRLF vs LF changes `$` behaviour and leaves `\r` in captures. Normalise or match `\r?\n`.
- **Byte order marks** at file starts break anchored first-line matches.
- Command-line tools obey the locale (`LC_ALL`); set `LC_ALL=C` for byte-wise speed and predictability on ASCII data, and a UTF-8 locale when character semantics matter.

## Command-line tools

Choose the tool by the shape of the task:

| Task | Tool (examples) | Notes |
|---|---|---|
| Find lines/files matching | `grep`, `rg` (ripgrep) | `-F` for literal strings; `-w` word match; `-E` ERE; `rg` respects `.gitignore` |
| Substitute within lines | `sed` | Line-oriented; multi-line edits are awkward |
| Field-based processing, aggregation | `awk` | Fields, conditions, sums, simple reports |
| JSON | `jq` | Real parser; never sed JSON |
| YAML | `yq` (several incompatible tools share this name) | Check which `yq` is installed |
| CSV/TSV with quoting | `mlr` (Miller), `csvkit`, `xsv`/`qsv`, or a scripting language | `cut -d,` breaks on quoted commas |
| XML/HTML | `xmllint --xpath`, `xmlstarlet`, `pup`, or a scripting language parser | |
| Complex logic | Python/Perl/Ruby/Node script | Once a one-liner needs comments, it is a script |

Useful idioms:

```bash
# Count requests per status code in a space-delimited access log (field 9)
awk '{count[$9]++} END {for (s in count) print s, count[s]}' access.log | sort -k2,2nr

# Extract a field from JSON lines, skipping records without it
jq -r 'select(.user.id != null) | .user.id' events.jsonl

# Update a JSON value safely (writes to temp, then replaces)
jq '.version = $v' --arg v "2.3.0" package.json > package.json.tmp && mv package.json.tmp package.json

# Literal search for a string containing regex metacharacters
grep -rnF 'config[0].timeout' src/
```

GNU vs BSD differences bite constantly: `sed -i` (BSD requires a suffix argument, e.g. `-i ''`), `sed` handling of `\n` and `\t` in replacements, `grep -P` (absent on BSD), `\+` and `\?` in BRE (GNU extension). For portable edits, `perl -pi -e 's/…/…/g'` behaves the same on both, or use a scripting language. See `scripting-and-shell` for the portability table.

## Use a parser for structured formats

| Format | Why regex fails | Use instead |
|---|---|---|
| JSON | Nesting, escapes in strings, key order, whitespace | `jq`, language JSON libraries |
| CSV | Quoted fields containing delimiters, newlines and escaped quotes | CSV libraries, Miller, csvkit |
| HTML | Malformed markup, nesting, attributes in any order, entities, comments, scripts | HTML parsers (BeautifulSoup/lxml, cheerio, html5 parsers) |
| XML | Namespaces, CDATA, entities, nesting | XML parsers with XPath; disable external entity resolution for untrusted input |
| YAML | Indentation semantics, anchors, multiple scalar styles | YAML libraries (safe loaders for untrusted input) |
| Source code | Strings, comments, nesting, syntax | Language parsers/AST tools, IDE refactoring, structural search (e.g. ast-grep, Semgrep, Comby) |
| URLs, emails, dates | Many edge cases and standards | Standard library parsers (URL parsers, date libraries); for email, minimal validation plus a confirmation step |

Regex is still useful *after* parsing: validating a single field value, cleaning a string you already extracted.

Example of the trap: `sed 's/"version": "[^"]*"/"version": "2.0"/'` on JSON also edits a nested dependency's `"version"` key. `jq '.version = "2.0"'` edits exactly the top-level key.

## Bulk edits across many files

A codebase-wide replace is a refactoring with a weak tool. Process:

1. **Prefer semantic tools** when the change is about code meaning: IDE rename, language server rename, codemods, AST-based structural search-and-replace. They understand scopes, imports and strings vs identifiers.
2. **Start from a clean version-control state** so the change is one reviewable diff and trivially revertible.
3. **Search first, and read the results.** List every match with context (`rg -n -C2 'pattern'`). Count them. Look for false positives: occurrences in strings, comments, docs, generated files, vendored dependencies, lockfiles, binary files, migrations that must not change.
4. **Narrow the scope** by path and file type (`-g '*.ts'`, exclude `vendor/`, `node_modules/`, generated directories).
5. **Use word boundaries and context** so `user` does not also change `username` and `superuser`.
6. **Dry-run the replacement** and review the diff before writing (many tools have a preview mode; otherwise write to a branch and diff).
7. **Apply**, then **verify**: build, type-check, lint, run tests; search again for leftovers of the old pattern and for accidental new patterns.
8. **Review the diff** as a whole; spot-check a sample of files in full.

Safety notes:
- `sed -i` across many files with a wrong pattern can corrupt them all at once; without version control, there is no undo. Keep backups (or a suffix with `-i.bak`) when not under version control.
- Respect file encodings and line endings; some tools rewrite them silently.
- Do not edit binary files with text tools.
- Do not run bulk edits over generated or vendored code; regenerate it instead.

## Validation patterns: guidance

- **Validate with a parser when one exists** (dates, numbers, URLs, IP addresses). Regex checks shape, not meaning: `\d{4}-\d{2}-\d{2}` accepts `2026-02-31`.
- **Email**: no practical regex matches the full standard and only real addresses. Use a permissive check (one `@`, something on each side, no whitespace) and confirm by sending a message.
- **Phone numbers, postal codes, names**: vary hugely by country and culture. Use dedicated libraries or permissive validation; do not reject real people's names with `^[A-Za-z]+$`.
- **Allow-lists over deny-lists** for security-relevant input: define what is permitted (`^[a-z0-9_-]{3,32}$`) rather than trying to block bad characters.
- **Never rely on regex to sanitise** HTML, SQL or shell input against injection. Use parameterised queries, proper escaping/encoding libraries, and context-aware templating.

## Process for writing a regex

1. **Collect real samples** of input, including the weird ones. Write lists of must-match and must-not-match strings.
2. **Identify the flavor** and match mode (search vs full match, multiline, case, Unicode, dotall).
3. **Build incrementally** from anchors and the most distinctive literal parts; use explicit classes and bounded quantifiers.
4. **Test** against both lists, in the actual engine (a REPL, a unit test, or an online tester set to the correct flavor). Use a debugger/visualiser for complex patterns.
5. **Check performance** with long and near-matching inputs if input can be large or untrusted.
6. **Make it readable**: verbose mode, named groups, or a comment with examples.
7. **Encode the tests** as unit tests when the regex lives in code.

## Worked examples

### Building a pattern from samples

Task: extract order IDs like `ORD-2026-000123` from support emails.

Must match: `ORD-2026-000123`, `(ORD-2025-998877)`, `ref ORD-2026-000001.`
Must not match: `ORD-26-123`, `XORD-2026-000123`, `ORD-2026-0001234` (too many digits), `ord-2026-000123` (if IDs are case-sensitive).

First attempt: `ORD-\d+-\d+`. Fails the must-not list: accepts `ORD-26-123` and matches inside `XORD-…` and the 7-digit case.

Refined: `\bORD-\d{4}-\d{6}\b`.
- `\b` on both sides rejects `XORD-…` and the trailing seventh digit.
- `\d{4}` and `\d{6}` encode the real format.
- If text may contain non-ASCII digits and the engine is Unicode-aware, use `[0-9]` instead of `\d`.

Then encode both lists as a unit test so the next person who "simplifies" the pattern finds out immediately.

### Fixing a backtracking pattern

A validation pattern for comma-separated tags, `^(\w+,?)*$`, hangs on a long input ending in a space. The inner `\w+,?` can match the same run of letters in many ways because the comma is optional. Rewrite so each repetition must consume a separator: `^\w+(?:,\w+)*$`. Now there is exactly one way to match any input, and failure is detected in linear time. Bound input length as well if it comes from users.

### Safe log extraction with awk instead of a regex chain

To compute the 95th-percentile latency per endpoint from lines like
`2026-03-01T10:00:00Z GET /api/orders 200 183ms`:

```bash
awk '{ sub(/ms$/, "", $5); print $3, $5 }' app.log |
  sort -k1,1 -k2,2n |
  awk '{ v[$1][++n[$1]] = $2 }                       # gawk arrays of arrays
       END { for (e in n) { i = int(n[e] * 0.95); if (i < 1) i = 1; print e, v[e][i] } }'
```

This uses gawk-specific arrays of arrays; on other awks, or once the logic grows, a short Python script with a CSV/log parser is clearer and portable. Choosing the script early is usually the better call.

### A preview-then-apply rename across a repository

Renaming a config key `max_retry` to `max_retries` in YAML and Python files, but not in the changelog or vendored code:

```bash
rg -n -w 'max_retry' -g '*.py' -g '*.yaml' -g '!vendor/**'        # 1. list and read every match
rg -l -w 'max_retry' -g '*.py' -g '*.yaml' -g '!vendor/**' |
  xargs perl -pi -e 's/\bmax_retry\b/max_retries/g'              # 2. apply (portable in-place edit)
git diff --stat && git diff                                       # 3. review
rg -n -w 'max_retry' .                                            # 4. leftovers? (expect only docs/vendor)
```

Then run the test suite. If the key is also read from environment variables, deployed config, or external systems, a text replace in the repository is not the whole change — those need a migration path that accepts both names for a while.

## Pitfalls and anti-patterns

- **Unanchored validation** accepting strings that merely contain a valid substring.
- **`.*` between delimiters** overrunning into the next field or line.
- **Parsing HTML/JSON/CSV with regex** and breaking on the first real-world variation.
- **Interpolating unescaped input** into patterns.
- **Nested quantifiers** causing catastrophic backtracking on untrusted input.
- **Assuming ASCII**: `\w` and `\d` behaving differently than expected; case-insensitive matching failing for non-English text.
- **Flavor mismatch**: testing in PCRE, deploying in RE2/JavaScript/POSIX where lookbehind or backreferences are unsupported.
- **Write-only regexes** with no comments or tests.
- **Bulk sed over a repository** without preview, version control, or exclusions.
- **Reading and writing the same file in one pipeline** (`sed … f > f` truncates `f`).
- **Locale surprises**: sort order and character ranges like `[a-z]` that include unexpected characters in some locales.

## Verification

- [ ] The regex passes all must-match and must-not-match cases, in the target engine and flavor.
- [ ] Validation patterns are anchored (or use full-match APIs).
- [ ] No ambiguous nested quantifiers; adversarial long inputs complete quickly.
- [ ] Unicode behaviour checked where text can be non-ASCII.
- [ ] Structured formats were handled with a parser, not regex.
- [ ] For bulk edits: match list reviewed, diff reviewed, build/tests pass, leftover search is clean.
- [ ] Complex patterns are commented or covered by tests.

## Reporting back

Show the pattern or command, explain briefly what it matches and why it is constrained the way it is, list the cases you tested (especially the tricky non-matches), name the flavor/tool it is written for, and for bulk edits state how many files and occurrences changed and what you verified.
