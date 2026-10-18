# Office formats: DOCX, XLSX, PPTX

Read this when generating, templating, or debugging Word-processing, spreadsheet, or slide files. Library names are examples; use whatever the project already uses.

## Shared background: OOXML

DOCX, XLSX, and PPTX are Office Open XML: ZIP archives of XML parts plus relationship files (`_rels/*.rels`) and a content-types manifest (`[Content_Types].xml`). Practical consequences:

- You can unzip a file to inspect it. When a document renders strangely, compare its XML with a version saved by the target application.
- **Corruption usually means**: a relationship pointing to a missing part, a part missing from the content-types manifest, invalid XML (unescaped `&`, `<`, control characters), duplicate IDs, or elements in an order the schema forbids. Word's "unreadable content — repair?" prompt and Excel's "We found a problem with some content" are the symptoms.
- Control characters (U+0000–U+001F except tab, LF, CR) are invalid in XML. Strip or replace them from inserted text — they commonly arrive from copy-pasted or database text.
- ODF formats (ODT, ODS, ODP) are the open-standard equivalents; LibreOffice reads and writes both families.

## DOCX

### Styles are the document model

- **Paragraph styles** (Heading 1–n, Normal/Body, Caption, Quote, List Paragraph) control block formatting and outline level. Headings must use heading styles for navigation, TOC, and accessibility.
- **Character styles** (Emphasis, Strong, Code) for inline formatting that should be consistent.
- **Table styles** for borders, shading, header-row formatting — define once, apply to every table.
- **Numbering definitions** control bulleted and numbered lists. Lists built by typing "1." manually are not lists.
- When generating from code, load a base template (`.docx` or `.dotx`) that defines styles, then reference style names. Libraries that create a blank document often ship a minimal default style set; a custom base template avoids default fonts appearing unexpectedly.
- Style names are sometimes localised in the UI but referenced by internal IDs in XML; check how your library resolves names.

### Templating

- Template libraries (e.g. docxtpl/Jinja-in-Word, docx-templates, mail-merge fields, content controls) let designers own the layout.
- **Split-run problem**: Word splits text into runs when formatting, spell-check, or revision tracking changes mid-word, so `{{ name }}` may become several runs and fail to match. Retype placeholders in one go, clear formatting on them, or use a library that handles run merging. Content controls are a sturdier placeholder mechanism.
- Repeating sections (table rows, paragraphs) need the template engine's loop constructs placed at the right level (row, paragraph, or section).
- Keep logic minimal inside templates; pre-compute values in code.

### Layout

- Sections control page size, orientation, margins, headers/footers, and columns. Landscape pages mid-document require a section break.
- Fields (page numbers, TOC, cross-references) are computed by the application; a generated TOC field may show "Update field" until opened and refreshed. Either instruct users, set the document to update fields on open (which prompts the user), or render via an application that updates fields during conversion.
- Images are inline or floating; inline is far more predictable for generated documents.

### Rendering differences

Word, LibreOffice, Google Docs, Pages, and mobile viewers differ in line breaking, table auto-fit, floating objects, and font substitution. Test in the recipients' main application. Avoid floating text boxes and complex anchoring in generated content.

## XLSX

### Types and formats

- Write numbers as numbers, dates as dates, booleans as booleans. Numbers written as strings break sums, sorting, and filters and show warning markers.
- Dates are stored as serial numbers with a date number format. Be aware of the 1900 vs. 1904 date system and the historical 1900 leap-year quirk; use the library's date handling rather than manual arithmetic. Decide time-zone handling explicitly — spreadsheets store no time zone.
- **Number formats** (e.g. `#,##0.00`, `0.0%`, currency, ISO dates) control display without changing values. Apply via named styles or consistent format codes; never pre-format numbers into strings.
- Long numeric identifiers (account numbers, phone numbers, IDs with leading zeros, numbers > 15 significant digits) must be stored as text, or they lose leading zeros and precision.

### Formulas vs. values

- Writing a formula stores the formula; many libraries don't compute it, so cached values are empty until the file is opened in a calculating application. Consumers that read cached values (some parsers, previews) will see blanks. If downstream systems read the file, either write values or recalculate via an application engine before delivery.
- Use formulas when the recipient will change inputs; values when the file is a static export.
- Prefer structured references, named ranges, or clear cell layouts over opaque cell addresses (see `spreadsheet-modeling`).

### Usability

- Freeze header rows; enable autofilter on tabular data; set column widths from content (libraries rarely auto-fit; estimate from string lengths with a cap).
- Use Excel tables (ListObjects) for tabular data where supported — they bring filtering, banding, and structured references.
- One table per sheet for data meant to be analysed; separate sheets for raw data, summary, and notes/metadata (source, extraction time, definitions).
- Data validation (drop-downs, ranges) for input sheets; protect formula cells if the user should not edit them (protection is not security).
- Conditional formatting sparingly, with meaning conveyed by more than colour.

### Scale

- Large exports: use streaming/write-only modes to avoid memory blowups. Excel's hard limits are about 1,048,576 rows and 16,384 columns per sheet; beyond a few hundred thousand rows, consider CSV, Parquet, or a database extract instead.
- Avoid styling cells individually at scale; use column-level or named styles.

### CSV specifics

- Encoding: UTF-8 is standard; some spreadsheet applications need a BOM to detect it. Know the consumer.
- Delimiter and decimal separators vary by locale (some locales default to `;` as delimiter and `,` as decimal mark).
- Quote fields containing delimiters, quotes, or newlines (RFC 4180 style); double embedded quotes.
- Neutralise formula injection for untrusted values starting with `=`, `+`, `-`, `@`, tab, or CR when the file will be opened in a spreadsheet application.

## PPTX

- **Slide masters and layouts** define placeholders (title, body, picture, chart). Generate slides from the template's layouts and fill placeholders; text placed in placeholders inherits theme styles and appears correctly in outline view and to screen readers.
- **Overflow**: placeholders may auto-shrink text when opened in the application, but libraries don't measure text. Estimate text length against box size, cap content, split across slides, or measure using font metrics. Always render and check.
- Put the slide title in the title placeholder even if visually hidden — it drives navigation and accessibility.
- Native charts (editable, data embedded in the file) vs. images: native when presenters will update data; images for guaranteed appearance.
- Speaker notes are a separate notes slide part; most libraries support writing them.
- Set reading order (selection pane order) to match visual order for accessibility.
- Embedded fonts may not be honoured on all platforms; prefer fonts available to presenters.
- See `presentations` for what goes on the slides.

## Verifying office files

- Open in the target application; watch for repair prompts.
- Convert to PDF with an independent engine (e.g. headless LibreOffice) and inspect pages as images — useful in automated pipelines and when no GUI is available. Remember this engine's rendering may differ slightly from Microsoft Office's.
- Re-open with a parser and assert on structure: style names used, number of tables/rows, cell types, formulas present, placeholders absent.
- Run the application's accessibility checker.
- For XLSX, check that totals compute, filters sort correctly (types right), and dates display in the intended format.
