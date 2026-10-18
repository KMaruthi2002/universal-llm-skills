# PDF and HTML documents

Read this when producing PDFs (from HTML/CSS, a typesetting system, or a drawing API), designing print CSS, meeting PDF accessibility or archival requirements, or producing HTML documents including email. Tools named are examples.

## Routes to PDF

| Route | Strengths | Weaknesses | Choose when |
|---|---|---|---|
| **HTML/CSS → PDF via a browser engine** (headless Chromium/Firefox via automation tools) | Modern CSS, web fonts, same templates as web; JS-rendered charts | Limited paged-media features (running headers, footnotes, advanced page selectors are partial); heavy runtime | Team knows web tech; rich visual layouts; reports that also appear on the web |
| **HTML/CSS → PDF via a paged-media renderer** (e.g. WeasyPrint, commercial CSS paged-media engines) | Good CSS Paged Media support: page counters, running headers, margin boxes, named pages | No JavaScript (in many); CSS support differs from browsers | Print-quality documents with precise pagination from HTML |
| **Office document → PDF** (office suite export or headless conversion) | Inherits a designed DOCX/PPTX template; editable source | Fidelity depends on engine; fonts | Organisation already designs in an office suite |
| **Typesetting** (LaTeX, Typst, similar) | Excellent typography, math, references, cross-references | Toolchain; template expertise | Academic, technical, math-heavy, book-like |
| **Drawing API** (ReportLab, PDFKit, pdf-lib, iText) | Pixel control; small runtime; fill existing PDFs | You manage layout, wrapping, pagination manually | Forms, labels, certificates, stamping, merging, overlays on existing PDFs |

## Print CSS essentials

- `@page { size: A4; margin: … }` (or `letter`) sets page size and margins; named pages allow different layouts (e.g. landscape appendices) in renderers that support them.
- Page breaks: `break-before`, `break-after`, `break-inside: avoid` on tables, figures, and headings-with-following-content. Support varies; test.
- Repeat table headers across pages with `thead { display: table-header-group; }` (supported in most engines).
- Running headers/footers and page counters (`counter(page)`, `counter(pages)`) are paged-media features — full in paged-media renderers, partial in browser engines (browser print automation often offers header/footer templates as an alternative).
- Use print-appropriate units (mm, pt) for page geometry; avoid viewport units.
- Hide interactive-only elements (`@media print`); show URLs for links if the document will be printed.
- Wait for fonts, images, and any JS-rendered content to finish before printing; lazy-loaded images and late web fonts are common causes of blank areas or fallback fonts.
- Load assets from local files or controlled URLs; a PDF renderer fetching arbitrary URLs from user-supplied HTML is a server-side request forgery risk. Sanitise user HTML and restrict network access for the renderer.

## Fonts in PDF

- Embed (subset) all fonts; non-embedded fonts are substituted by viewers and break layout. Most generators embed by default; verify in the viewer's document properties.
- Ensure the chosen font covers all scripts; configure fallback fonts for multilingual content.
- Check licence terms for embedding.

## Accessible PDFs

An untagged PDF is a picture of text to assistive technology. For accessibility:

- **Tagging**: structure tags (headings, paragraphs, lists, tables, figures) with correct reading order. Generators differ greatly — some produce tagged PDFs from semantic HTML or styled office documents; drawing APIs usually require manual tagging or don't support it.
- **Document title** set and displayed in the title bar; document **language** set.
- Alt text on figures; artifacts (decorative elements, running headers) marked as artifacts.
- Tables with header cells.
- Bookmarks for long documents (often generated from headings).
- Form fields with labels and logical tab order.
- **PDF/UA** (ISO 14289) is the accessibility standard; validate with a checker (e.g. veraPDF, PAC, or the PDF tool's built-in checker) when compliance is required. Automated checks don't cover everything — reading order and alt text quality need human review.

Choosing a semantic source (well-structured HTML, styled DOCX) and a tag-aware converter is far cheaper than remediating PDFs afterward.

## Archival and print production

- **PDF/A** (ISO 19005) for long-term archiving: embedded fonts, no external dependencies, no encryption, device-independent colour. Conformance levels differ (e.g. PDF/A-2b vs. 2u vs. 2a/PDF/A-3 with attachments); confirm which is required and validate.
- Professional print may require **PDF/X**, CMYK colour, bleed and crop marks, and minimum image resolution; get the printer's specification.
- Digital signatures, encryption, and permission flags: signatures must be applied last (any later modification invalidates them); permission flags ("no copy") are advisory, not security.

## Manipulating existing PDFs

- Merging, splitting, rotating, stamping, watermarking, and filling AcroForm fields are routine with PDF libraries.
- Flatten filled forms if recipients shouldn't edit them.
- Redaction must remove content streams, not overlay rectangles; use a tool with true redaction, then verify by extracting text and inspecting metadata.
- Text extraction from PDFs is heuristic: reading order, columns, ligatures, and tables are reconstructed, not read. Scanned PDFs need OCR. Validate extracted data.

## HTML as the deliverable

- **Self-contained vs. linked**: a single file with inlined CSS and embedded (data-URI) images is portable but larger; linked assets are lighter but break when moved. Choose by how it's shared.
- Use semantic elements (headings, lists, `table` with `th`, `figure`/`figcaption`) — they drive accessibility, reader modes, and conversion to other formats.
- Set `<html lang>`, `<title>`, and a viewport meta for mobile reading.
- Respect the destination: if it will be embedded in a CMS or docs site, match its CSS rather than shipping your own.

## HTML email

Email clients are not browsers; many strip `<style>` blocks, ignore modern layout (flexbox/grid support is inconsistent), block remote images by default, and apply dark-mode colour inversion.

- Use simple, table-based or well-tested hybrid layouts; inline critical CSS (tooling can automate inlining).
- Keep width around 600–700 px for the content column; make it fluid for mobile.
- Provide alt text — images are often blocked; never put essential information only in images.
- Always include a plain-text alternative part.
- Test across major clients (web, desktop, mobile; light and dark modes) with an email-preview service or real accounts.
- Follow anti-spam and consent law and include unsubscribe mechanisms for bulk mail; sending is an outward-facing action requiring confirmation.

## Verifying PDF and HTML output

- Open the PDF in at least two viewers (e.g. a dedicated reader and a browser); check fonts embedded, page size, page count, bookmarks, and links.
- Render pages to images for automated visual regression in pipelines.
- Extract text and confirm it's correct and in reading order (catches image-only output and broken tagging).
- Run accessibility and, if required, PDF/A or PDF/UA validators.
- For HTML, check in a browser at desktop and mobile widths, print preview if it will be printed, and an HTML validator or accessibility checker.
