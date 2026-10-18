---
name: document-generation
description: >-
  Produce document files — DOCX, PDF, XLSX, PPTX, Markdown, HTML, CSV — either
  programmatically (libraries, templates, converters, report pipelines) or by
  hand, and verify they open and render correctly. Covers choosing the format
  by how the file will be used, template-based vs. built-from-code generation,
  using the document's own style system (styles, masters, themes, named
  formats) instead of ad-hoc formatting, tables, images, page layout, fonts,
  accessibility of documents, conversion between formats, and checking output
  by actually opening or rendering it. Use when asked to "generate a Word
  doc/PDF/spreadsheet/slide file", build a report or invoice generator,
  mail-merge, export data to Excel, convert Markdown to PDF/DOCX, fill a
  template, or fix a file that renders wrong. Not for deciding what a document
  should say (technical-writing, business-communication), deck storyline
  (presentations), or spreadsheet model logic (spreadsheet-modeling).
metadata:
  category: product-and-communication
  related: technical-writing, presentations, spreadsheet-modeling, data-visualization, accessible-design, scripting-and-shell, workflow-automation, verify-before-done
---

# Document Generation

Generating a document is a two-part problem: the **content** (what it says) and the **artifact** (a file in a specific format that must open, render, print, and behave correctly in the reader's software). This skill is about the artifact. The defining hazard is that a document can be *structurally valid* and still look broken — overflowing tables, missing fonts, images at the wrong resolution, a spreadsheet whose numbers are stored as text. The only reliable test is to open or render the result and look.

## Scope

Covers: choosing a format; generating DOCX, PDF, XLSX, PPTX, Markdown, HTML, and CSV files from code or templates; producing them by hand in an office tool when that's the right call; styling through the format's own style system; tables, images, charts, headers/footers, page layout, fonts; accessible documents; format conversion; and verification.

Neighbours:

- `technical-writing`, `business-communication`, `copywriting` — what the document says.
- `presentations` — the storyline and design of a deck; this skill covers producing the .pptx/.pdf file.
- `spreadsheet-modeling` — formulas and model structure; this skill covers producing and formatting the workbook file.
- `data-visualization` — chart design; this skill covers embedding charts in documents.
- `workflow-automation`, `scheduled-jobs` — running generation on a schedule or trigger.

## Core principles

### 1. Choose the format by how the file will be used

The format is a promise about what the recipient can do with the file. A PDF promises fixed appearance and resists editing; a DOCX promises editability with variable rendering; an XLSX promises live calculation and sorting; HTML promises reflow and links; Markdown promises plain-text diffability. Pick the promise the recipient needs. Generating a beautiful PDF for someone who has to edit it, or a DOCX for a contract that must look identical everywhere, fails regardless of quality.

### 2. Use the document's own style system

Every serious format has a style mechanism: paragraph and character styles in Word/ODF, slide masters and layouts in PowerPoint/Keynote, named cell styles and number formats in spreadsheets, CSS in HTML and many PDF pipelines, themes and packages in LaTeX. Apply formatting through it, not by setting font/size/colour on each run of text. Reasons:

- **Editability** — a recipient can change "Heading 2" once instead of hunting through 80 manually formatted headings.
- **Structure** — headings defined as heading styles produce navigation panes, tables of contents, PDF bookmarks, and screen-reader structure. Bold 16 pt text produces none of that.
- **Consistency** — generated output can't drift when every element references a style.
- **Brand fit** — an organisation's template carries its styles; generating into it inherits them.

### 3. Start from the organisation's template when one exists

If the user has a letterhead, report template, slide master, or invoice layout, generate *into* it rather than recreating it in code. Templates carry fonts, colours, logos, margins, headers, and legal boilerplate that are tedious and error-prone to replicate — and the owner can update the template without touching code. When no template exists, keep the visual system restrained and derived from the content's purpose; don't invent a decorative house style.

### 4. Separate content, data, and presentation

Generation code should not mix business data, prose, and formatting decisions in one tangle. Keep data (records, figures), content (text, possibly templated), and presentation (template/styles) separate, joined at render time. This makes each changeable independently and lets you test data correctness without rendering, and rendering without real data.

### 5. Verify by opening or rendering — always

Libraries happily write files that the target application renders badly or refuses to open. "The script ran without errors" proves nothing about the document. Render it (convert to PDF or images, open in the target application, or inspect in a viewer) and look at every page or a representative sample, plus the edge cases: the longest name, the empty table, the 300-row dataset, the non-Latin text.

### 6. Accessible by default

Documents are read with screen readers, magnifiers, and reflow tools; many organisations are legally required to publish accessible documents. Real headings, alt text, table header rows, logical reading order, sufficient contrast, a document title and language — these cost little when built in at generation time and a lot to retrofit.

## Choosing a format

| Format | Choose when | Avoid when | Watch out for |
|---|---|---|---|
| **PDF** | Fixed layout matters (contracts, invoices, print, archival, forms to sign); must look identical everywhere | Recipient must edit substantially; content must reflow on small screens | Fonts must be embedded; accessibility needs tagging (PDF/UA); archival may need PDF/A |
| **DOCX** (or ODT) | Recipient will edit, comment, track changes; organisational workflows run on word processors | Exact layout must be guaranteed | Renders differently across Word, LibreOffice, Google Docs, and versions; test in the recipient's tool |
| **XLSX** (or ODS) | Recipient will sort, filter, calculate, pivot; tabular data with types | Narrative documents; very large raw data dumps (consider CSV/Parquet) | Numbers/dates stored as text; formulas vs. values; locale differences |
| **CSV** | Data interchange between systems; simplest possible tabular export | Formatting, multiple sheets, types matter | Delimiters, quoting, encoding (UTF-8 with or without BOM for Excel), formula injection |
| **PPTX** (or Keynote/ODP) | Slides to present or edit in a slide tool | Long-form reading | Text overflow in placeholders; fonts; master/layout mismatch |
| **HTML** | Web delivery, reflow, links, interactivity, responsive reading | Printing with precise pagination (possible with print CSS, but harder) | Self-contained vs. linked assets; email clients render HTML very differently from browsers |
| **Markdown** | Source in a repository, docs-as-code, diffable text, input to other renderers | The final artifact for non-technical recipients | Dialect differences (CommonMark, GFM, others); tables and extensions vary by renderer |
| **LaTeX → PDF** | Heavy mathematics, academic publishing with required class files | Collaborators who don't use LaTeX; quick business documents | Toolchain installation; long compile cycles |

A common robust architecture: author or assemble content in a structured source (Markdown, HTML, a data model), then render to one or more output formats. Generate the editable and the fixed versions from the same source when both are needed.

## Approaches to generation

### By hand vs. by code

Generate by code when the document is produced repeatedly, from data, in volume, or must be reproducible. Produce by hand (in an office tool) when it's a one-off where layout judgment dominates and no data pipeline exists. If you are an agent with code execution but no office GUI, generate with code and verify by rendering; tell the user what to tweak by hand if fine layout matters.

### Generation strategies

| Strategy | How | Best for | Trade-offs |
|---|---|---|---|
| **Fill a template** | A designed DOCX/PPTX/XLSX/HTML template with placeholders; code substitutes values, repeats rows/sections | Branded recurring documents: letters, invoices, reports, certificates | Designers own the look; complex logic in templates gets messy; placeholder syntax must survive editing |
| **Build from code (object model)** | Library APIs create paragraphs, tables, slides, cells | Highly variable structure; documents driven entirely by data | Verbose; styling should still reference styles defined in a base template |
| **Render HTML/CSS → PDF** | Templating engine produces HTML; a browser engine or HTML-to-PDF renderer prints it | Web-skilled teams; rich layouts; same template for web and PDF | Pagination control (page breaks, running headers) varies by renderer |
| **Markup → converter** | Markdown/AsciiDoc/LaTeX source converted by a universal converter (e.g. Pandoc) with a reference document or template for styles | Docs-as-code; multiple outputs from one source | Fine layout control is limited; style mapping via reference docs needs care |
| **Typesetting/layout language** | Purpose-built typesetting systems (e.g. LaTeX, Typst) or a PDF drawing API | Precise layout, math, publication quality | Learning curve; drawing APIs make you manage layout manually |

Illustrative library examples (non-exhaustive; prefer what the project already uses):

- **DOCX**: python-docx, docxtpl (templating on top), docx (JavaScript), Apache POI (Java), Open XML SDK (.NET), Pandoc with a reference .docx.
- **PDF**: headless browser printing (e.g. Playwright/Puppeteer), WeasyPrint, wkhtmltopdf-style tools, ReportLab, pdf-lib or PDFKit (JS), iText/OpenPDF (Java), LaTeX/Typst; pypdf/qpdf for merging and manipulating existing PDFs.
- **XLSX**: openpyxl or XlsxWriter (Python), ExcelJS or SheetJS (JS), Apache POI, ClosedXML/EPPlus (.NET); pandas `to_excel` for quick exports.
- **PPTX**: python-pptx, PptxGenJS, Apache POI; see `presentations` for content.
- **HTML**: any templating engine (Jinja, Handlebars, Liquid, JSX/server rendering); email HTML has its own constraints.
- **Conversion**: Pandoc for markup formats; LibreOffice in headless mode for office-format → PDF conversion and rendering checks.

Choosing among libraries, weigh:

- **What the project already uses** — a second document stack doubles maintenance.
- **Fidelity to the target application** — some libraries cover only part of a format (e.g. no charts, limited table styling, no tagged PDF output).
- **Template support** — can designers edit the template in their normal tool?
- **Runtime cost** — headless browsers and office suites are heavyweight for serverless or high-volume jobs; pure libraries are lighter but more limited.
- **Accessibility and standards output** — tagged PDF, PDF/A, real heading structure.
- **Maintenance and community** — active releases, issue responsiveness, documentation.

Check licences — some PDF and office libraries are dual-licensed or commercial for certain uses.

Per-format depth lives in references:

- `references/office-formats.md` — read when generating or fixing DOCX, XLSX, or PPTX: object models, styles, tables, number formats, templates, common corruption causes.
- `references/pdf-and-html.md` — read when producing PDF (from HTML, typesetting, or drawing APIs), print CSS, PDF accessibility/archival, or HTML documents and email.

## Process

### Step 1: Pin down the requirements

- **Recipient and use**: read, edit, print, sign, archive, analyse, import into another system?
- **Format(s)**: from the table above, or as specified.
- **Volume and frequency**: one document, a batch of 10,000, a nightly report?
- **Template/brand**: existing template, letterhead, style guide, or sample document to match?
- **Content sources**: database, API, spreadsheet, user input, LLM output (treat as untrusted text to be escaped).
- **Constraints**: page size (A4 vs. Letter matters — ask or infer from locale), margins, fonts and their licences, languages/scripts, file size limits (email attachments), accessibility or archival standards, security (passwords, redaction, metadata).

### Step 2: Discover existing conventions

In an existing codebase, find how documents are already produced: search for library imports, template folders, report modules, export endpoints. Reuse the existing toolchain and templates rather than introducing a second stack. Look at previously generated outputs to understand expectations. If the user supplied a sample document, inspect its styles (style names, fonts, page setup), not just its look.

### Step 3: Model the content

Define the data structure the document renders from: sections, tables, repeating groups, optional parts. Decide what happens with missing or extreme data — empty lists, very long strings, null values, huge numbers. These cases cause most production defects.

### Step 4: Build the presentation layer

- Create or load the template; define styles (headings, body, captions, table styles, number formats) once.
- Map content elements to styles, never to raw formatting.
- Set document-level properties: title, author/organisation, language, subject; page size, margins, orientation; headers/footers with page numbers where useful.

### Step 5: Generate

Write generation code that is deterministic (same input → same output, aside from timestamps you choose to include), escapes or sanitises inserted text for the target format, and fails loudly on missing required data rather than emitting a half-empty document.

### Step 6: Verify

Run the verification checks below. Fix and regenerate until clean.

### Step 7: Deliver

Name files meaningfully and safely (no characters illegal on common filesystems; include identifiers/dates as appropriate). Report what was generated, how it was verified, and any rendering differences across target applications you know of or could not test.

## Cross-format concerns

### Tables

- Define header rows as headers (repeat on each page in long documents; mark as header for accessibility).
- Set column widths deliberately; auto-width behaviour differs between renderers and causes overflow.
- Right-align numbers, use consistent decimals, and include units in headers rather than every cell.
- Plan for page breaks: allow rows to break across pages or not, consistently; avoid orphaned header rows.
- Keep tables for tabular data, not for page layout (layout tables confuse screen readers and reflow).
- Test with the largest realistic dataset, not three sample rows.

### Images and charts

- Use adequate resolution for the medium (print needs more than screen; ~150–300 DPI at final printed size is a common target) without bloating file size — compress photos, use vector formats (SVG, EMF, PDF) for charts and diagrams where the format supports them.
- Preserve aspect ratio; size images to the content width, not their native pixels.
- Add alt text for informative images; mark decorative ones as decorative.
- For charts, decide between native charts (editable, live in XLSX/PPTX) and embedded images (consistent rendering everywhere). Native is better when recipients will update data; images when appearance must be fixed.

### Fonts

- Use fonts available on the recipient's systems, or embed them (PDF always should; Office embedding is possible but inconsistently honoured), or accept a fallback.
- Check font licences permit embedding.
- Ensure the font covers every script in the content — missing glyphs render as boxes ("tofu").
- Right-to-left scripts and complex shaping (Arabic, Hebrew, Indic scripts) need renderer support; test them explicitly.

### Page layout

- Page size and margins per locale or requirement (A4 vs. US Letter is the most frequent mismatch).
- Headers/footers: page numbers ("Page 3 of 12" where useful), document title, confidentiality marking if required.
- Control breaks: keep headings with the following paragraph; avoid widows/orphans; start major sections on a new page only when it helps.

### Text and data safety

- Escape inserted text for the target format (XML special characters in OOXML, HTML entities, LaTeX special characters). Unescaped user or model-generated text corrupts files or injects markup.
- **Spreadsheet formula injection**: values beginning with `=`, `+`, `-`, `@` (and sometimes tab/carriage return) in CSV/XLSX may execute as formulas when opened. When exporting untrusted data, neutralise them (commonly by prefixing a single quote or otherwise forcing text) — and decide deliberately, since this alters the data.
- Strip or control metadata (author names, file paths, revision history, comments, hidden sheets) before external distribution.
- Redaction must remove the underlying content, not draw a black box over it. Verify by extracting text from the result.
- Don't place secrets, credentials, or unnecessary personal data in generated documents; documents get forwarded.

### Accessibility checklist for documents

- Document title and language set in metadata.
- Headings use heading styles in a logical hierarchy (no skipped levels for visual effect).
- Lists use real list structures.
- Tables have header rows/columns marked; avoid merged cells where possible; no layout tables.
- Images have alt text; decorative images are marked as such.
- Meaningful link text (not "click here"); URLs in print documents are readable.
- Sufficient colour contrast; information not conveyed by colour alone.
- Reading order matches visual order (particularly in PDFs and slides).
- PDFs are tagged; forms have labelled fields.
- Run the target tool's accessibility checker where available (most office suites and PDF tools have one) and treat its output as a floor, not proof. See `accessible-design` and `accessibility-audit` for depth.

## Format conversion

Conversions are lossy in predictable ways. Know what each direction loses before promising it:

| Conversion | Usually preserved | Usually lost or degraded |
|---|---|---|
| Markdown → DOCX/PDF/HTML | Headings, lists, emphasis, code, links, simple tables | Precise layout; complex tables; anything the dialect lacks (styles come from a reference doc/template) |
| DOCX → PDF | Layout, if fonts are present and the converter matches the authoring app | Exact fidelity when converted by a different engine than the one used to author; interactive fields; tracked changes (unless deliberately shown) |
| HTML → PDF | Styling via CSS, links | Interactivity; reliable pagination unless print CSS is designed; lazy-loaded content that wasn't triggered |
| PDF → DOCX/text | Text, mostly | Structure, reading order, tables, layout — PDF is a page description, not a document model. Treat PDF extraction as best-effort and verify |
| XLSX → CSV | Values of one sheet | Formulas, formatting, other sheets, types (everything becomes text) |
| PPTX → PDF | Slide appearance | Animations, builds (flattened or dropped), speaker notes unless exported explicitly |

Rules of thumb:

- Convert from the richest source, never round-trip (DOCX → PDF → DOCX destroys structure).
- Use the same engine for conversion that recipients' software uses when fidelity matters, or render-check the result.
- For PDF input (parsing invoices, extracting tables), expect variation by producer; build validation on the extracted data, and treat scanned PDFs as images requiring OCR, with accuracy checks.

## Documents assembled from model-generated content

When text in a document comes from an LLM or other generator:

- Treat it as untrusted input: escape it for the format, strip control characters, and constrain it to the structure the template expects (e.g. ask for structured output, then validate before rendering).
- Map generated structure (headings, lists, tables) onto the template's styles rather than letting free-form Markdown or HTML leak into the file unconverted.
- Enforce length budgets for fixed-size areas (slide placeholders, table cells, form fields) before rendering, and re-check overflow after.
- Fact-check figures, names, and claims before the document is distributed; a polished format lends unearned authority to errors (see `fact-checking`).

## Batch and pipeline generation

When generating many documents or on a schedule:

- **Validate data before rendering.** Check required fields, types, and ranges first; a bad record should be reported and skipped (or stop the run, by policy), not silently produce a broken document.
- **Make runs idempotent and resumable.** Deterministic file names keyed by record ID and period let you re-run safely and skip completed items after a crash.
- **Isolate failures.** One malformed record must not abort 9,999 good ones unless that's the desired policy; log which records failed and why.
- **Control resources.** Headless browsers and office converters are memory-hungry and occasionally hang; reuse instances where safe, set timeouts, and limit concurrency.
- **Sample-verify every run.** Automatically render and check a few documents per batch (first, last, random, and the largest), and alert on anomalies such as file size outliers or page-count jumps.
- **Treat distribution as a separate, confirmed step.** Generating 10,000 invoices is reversible; emailing them is not. Keep a dry-run mode, review a sample, and get explicit confirmation before sending externally.
- **Protect personal data** in generated files and intermediate artefacts: restrict storage, set retention, and don't leave copies in temp directories or logs.

## Verification

Verification is not optional; it is the part of the task that distinguishes a working generator from one that merely runs.

1. **Open it** in the application the recipient will use (or the nearest available). If you can't run that application, convert to PDF or images with an independent renderer (e.g. headless LibreOffice for office formats, a browser for HTML) and inspect the result. A file that opens in one app may trigger a "repair" prompt in another — Word's repair dialog usually means invalid XML or relationships.
2. **Look at every page** for short documents; for long or batch outputs, inspect a sample *plus* edge cases: first and last records, longest values, empty sections, maximum row counts, special characters, other scripts.
3. **Check structure, not only looks**: heading navigation pane/bookmarks, table of contents, accessibility checker, text extractable from PDF (copy-paste a paragraph), spreadsheet cells have the right types (numbers sum, dates sort), formulas compute.
4. **Validate programmatically where possible**: re-open the file with a parser; validate PDF/A or PDF/UA with a validator if required; diff extracted text against expected content for regression tests; snapshot-render pages to images and compare against approved baselines for recurring reports.
5. **Check file properties**: size reasonable, metadata correct, no leftover placeholder text (search for your placeholder syntax and "lorem"), no hidden sheets or comments unintentionally included.
6. **Test in the second-most-likely app** if recipients vary (e.g. Word and Google Docs, Excel and LibreOffice, Acrobat and a browser PDF viewer).

If you have no way to render the output, say so explicitly in your report and tell the user what to check when they open it.

## Pitfalls

- **Declaring success because the script ran.** The most common failure. Render it.
- **Direct formatting everywhere.** Manually setting font and size on every run produces documents without structure that are painful to edit and inaccessible. Use styles.
- **Recreating the brand in code** instead of loading the organisation's template — results in near-misses (wrong blue, wrong margins) and duplicated maintenance.
- **Wrong page size** for the recipient's locale.
- **Missing fonts and glyphs** — fallback fonts reflow layouts; unsupported scripts render as boxes.
- **Text overflow** in fixed boxes (slide placeholders, table cells with fixed heights, PDF drawing APIs that don't wrap).
- **Numbers as text** in spreadsheets: values don't sum, sort wrongly, show green warning triangles. Write numeric types and apply number formats.
- **Dates and time zones**: dates written as strings, wrong serial-date epoch, implicit time-zone conversions shifting dates by a day.
- **CSV encoding and delimiter surprises**: non-ASCII text garbled when opened in some spreadsheet apps without a BOM; semicolon-delimiter locales; unquoted commas and newlines.
- **Formula injection** from untrusted data in CSV/XLSX.
- **Fake redaction** and leaked metadata.
- **Huge files** from uncompressed images or embedding the same image repeatedly instead of once by reference.
- **Untested edge data** — the one customer with a 90-character company name breaks the invoice layout.
- **Corrupted OOXML** from hand-edited XML, invalid relationships, or library misuse; detected only when Word offers to repair.
- **Non-deterministic output** that makes regression testing impossible (random IDs, unordered dict iteration, current timestamps everywhere).
- **Assuming one renderer represents all** — HTML emails, DOCX in different suites, and PDFs in different viewers can all differ.

## Quality bar

- [ ] Format matches how the recipient will use the file.
- [ ] Generated into the organisation's template where one exists; otherwise a restrained, purpose-derived style.
- [ ] All formatting applied through styles/masters/named formats; headings are real headings.
- [ ] Document metadata (title, language) set; page size and margins correct.
- [ ] Tables have headers, sensible widths, and survive the largest realistic data.
- [ ] Images sized and compressed appropriately, with alt text.
- [ ] Fonts available or embedded, covering all scripts used.
- [ ] Inserted text escaped; untrusted spreadsheet data neutralised against formula injection where appropriate.
- [ ] No placeholder text, leaked metadata, or hidden content.
- [ ] Opened or rendered and visually inspected, including edge cases; accessibility checker run where available.
- [ ] Report to the user states how it was verified and what was not.

## Illustrative example: a monthly report pipeline

*Illustrative only.* A team wants a monthly PDF report emailed to clients and an editable DOCX for account managers to annotate.

Reasoning: two recipients, two promises — fixed appearance for clients (PDF), editability for staff (DOCX). Generate both from one source so they can't diverge. The team already has a branded Word template, and account managers live in Word, so the source of truth for styles is that template.

Approach: query the data into a structured model (sections, KPI table, a chart per region); render charts as vector images; fill the branded DOCX template with a templating library, mapping every element to the template's existing styles ("Heading 1", "Table – KPI", "Caption"); convert the DOCX to PDF with a headless office renderer so the PDF inherits the same layout; tag and title the PDF. Verification: render both outputs for the largest and smallest client, check page breaks around the KPI table, check navigation and accessibility checker output in the DOCX, extract text from the PDF to confirm it's real text, and snapshot-compare page images against last month's approved output to catch regressions.
