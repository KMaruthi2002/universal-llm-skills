# Localization Readiness for Interface Copy

Read this when interface copy will be translated, or when a product is preparing to support more languages or regions. Most localization problems are created by the way source strings are written and assembled, long before a translator sees them.

## String construction

- **Use whole sentences with named placeholders**, not concatenation. Word order differs across languages; "Delete {fileName}?" can be reordered by a translator, while "Delete " + fileName + "?" cannot.
- **Name placeholders meaningfully** ({fileName}, {count}, {userName}) rather than positionally ({0}, %s), so translators know what they contain.
- **Handle plurals with plural-aware message formats** (e.g. ICU MessageFormat or the platform's equivalent). Languages have between one and six plural forms; "1 item / 2 items" logic in code fails for many of them.
- **Handle grammatical gender and case** where the product mentions people or objects in sentences; message formats with select statements can help. Where that is impractical, restructure sentences to avoid gendered agreement ("Shared by: {userName}" rather than "{userName} shared their file").
- **Don't reuse a string for different contexts.** "Open" as a button label and "Open" as a status may translate differently. Use separate keys.
- **Don't split sentences across UI elements** (e.g. part of a sentence in a dropdown) unless the localization system supports reordering the parts.
- **Keep markup out of strings where possible**, or use placeholders for links and emphasis so translators can position them.

## Text expansion and layout

- Translated text is often longer than English, sometimes much longer for short strings; some languages are more compact. Design layouts that flex: buttons that grow, labels that wrap, no fixed widths sized to the source text.
- Test with pseudo-localization (artificially lengthened and accented strings) to find truncation and hard-coded strings before translation begins.
- Support right-to-left languages if in scope: layout mirroring, bidirectional text with mixed scripts, icons that imply direction.
- Avoid putting text in images, icons, or videos without a localization plan.

## Formatting

Use locale-aware formatting libraries, never hand-built strings, for:

- dates and times (order, separators, 12/24-hour clocks, time zones, calendar systems);
- numbers (decimal and grouping separators);
- currencies (symbol position, decimal places);
- names (order of given and family names, single-name users; don't require two fields if the audience includes people with one name);
- addresses and phone numbers (formats vary widely by country);
- units of measure.

## Translator context

Provide, for each string or group:

- where it appears (screenshot or description) and what kind of element it is (button, heading, tooltip, error);
- what each placeholder will contain, with examples;
- character or space limits, if any;
- whether a word is a noun, verb, or adjective when ambiguous;
- terms from the glossary that must be translated consistently, and terms that must not be translated (product names, code).

Maintain a multilingual glossary alongside the source glossary so core terms stay consistent across languages.

## Writing source copy that translates well

- Use plain, literal language; avoid idioms, puns, slang, and culturally specific references (sports metaphors, holidays).
- Keep sentences short and unambiguous; ambiguous source text produces inconsistent translations.
- Use the same term for the same concept everywhere; inconsistency multiplies across languages.
- Avoid abbreviations unless they are standard in every target market.
- Be careful with humor: it rarely survives translation and can offend.

## Beyond translation

Localization also includes regional differences in legal requirements, payment methods, imagery, color associations, examples, and the level of formality expected. Where the product's voice is defined, decide per language how it maps (e.g. formal vs. informal second-person forms) and document it in the language's style guide.

## Verification

- Every user-visible string is externalized (no hard-coded text); pseudo-localization reveals none.
- No concatenated sentences; plurals and genders use the message format.
- Layouts survive expanded text and, if applicable, right-to-left rendering.
- Dates, numbers, currencies and names use locale formatting.
- Translators have context and a glossary; linguistic review happens in the real UI, not only in a spreadsheet.
