---
name: data-visualization
description: >-
  Turn data into charts that answer a specific question honestly and fast:
  choose the chart form from the comparison being made, build an encoding
  hierarchy, use color for meaning (categorical, sequential, diverging) with
  colorblind safety, label directly, keep axes honest, use small multiples,
  annotate the insight, and avoid misleading charts — with styling derived
  from the destination (report, slide, app, publication, brand) rather than a
  default. Use when someone asks for a chart, graph, plot or figure, which
  chart type to use, to improve or critique a chart, to pick chart colors, or
  to visualise results — in any library or tool (matplotlib, ggplot2, Vega,
  D3, Plotly, Excel, BI tools). For multi-chart monitoring views see
  dashboard-building; for slide decks see presentations.
metadata:
  category: analysis
  related: data-analysis, dashboard-building, statistical-analysis, presentations, accessible-design, visual-design, design-systems, technical-writing
---

# Data Visualization

A chart is an argument made with position, length, shape and color. A good one lets the reader see the answer to a question faster and more reliably than they could from a table. A bad one is decoration at best and deception at worst. The craft lies less in the tooling than in deciding what comparison the reader needs to make and then making that comparison effortless.

## Scope

This skill covers choosing, building, labelling and critiquing individual charts and small sets of charts, in any medium. Neighbours:

- `dashboard-building` — multi-chart, interactive, recurring monitoring views.
- `presentations` — charts in the context of a talk and a slide sequence.
- `data-analysis` and `statistical-analysis` — deciding what is true before deciding how to show it.
- `accessible-design` — broader accessibility requirements beyond those covered here.
- `visual-design` and `design-systems` — when charts must fit a visual identity or a component library.

## Core principles

### 1. Start from the question, not the data

Every chart should answer a question you can state in a sentence: "Did signups recover after the outage?", "Which regions are below target?", "How is order value distributed?". The question determines what is compared, which determines the chart. Putting all available columns on a chart and letting the reader find the story is not neutral; it pushes the analytical work onto the reader and usually fails.

### 2. Encode the most important comparison with the most accurate channel

People judge some visual properties far more precisely than others. Roughly, from most to least accurate for quantitative comparison:

1. Position along a common scale (dot plot, bar ends, line height on a shared axis)
2. Position along non-aligned scales (same chart type, separate panels)
3. Length (bars from a common baseline)
4. Angle and slope
5. Area
6. Volume, color saturation and lightness
7. Color hue (good for categories, poor for quantities)

Put the comparison that answers the question on position. Use weaker channels (color, size) for secondary information. **Why:** this ordering comes from perception research and explains most chart advice: why bar charts beat pie charts for precise comparison, why bubble sizes are hard to read, why 3D distorts.

### 3. Every ink mark should carry information or aid reading

Remove what does not help: heavy gridlines, borders, background fills, redundant legends, 3D effects, drop shadows, decorative icons. Keep what helps: light reference gridlines when values must be read, axis labels, a zero line, annotations. **Why:** clutter costs attention, and the reader's attention is the scarcest resource. But minimalism is not the goal — clarity is. Removing axis labels to look clean is a failure.

### 4. Honesty is non-negotiable

The visual impression must match the data. Bars start at zero; areas are proportional to values; axes are not truncated or broken without clear signalling; time intervals are evenly spaced; uncertainty is shown when it matters; cherry-picked windows are avoided. **Why:** readers take in the visual impression first and often never read the numbers. A chart that is technically labelled but visually misleading still misleads.

### 5. Style follows the destination

The right fonts, colors, sizes and density depend on where the chart will live: a journal figure, a slide seen across a room, a dashboard on a laptop, a mobile app, a printed report, a brand-governed marketing page, dark or light mode. Find the destination's conventions and design tokens and derive the chart's style from them rather than shipping a library default or a personal favourite style. **Why:** a chart that clashes with its context looks untrustworthy and is harder to read in that context (e.g., thin lines and small labels vanish on a projector).

## Process

### Step 1 — Write the question and the takeaway

Write the question the chart answers. If the analysis is done, also write the takeaway in one sentence ("Northern region is the only one below target for three consecutive months"). The takeaway often becomes the chart title. If you cannot write it, the analysis is not finished or the chart is exploratory — both are fine, but know which.

### Step 2 — Identify the comparison type

| Comparison | Typical forms |
|---|---|
| **Change over time** | Line chart (continuous), column chart (few discrete periods), slope chart (two points), area chart (cumulative totals or composition over time), sparkline (compact trend) |
| **Ranking / magnitude across categories** | Sorted horizontal bar, dot plot, lollipop; table with inline bars |
| **Part-to-whole** | Stacked bar (few parts), 100% stacked bar (compare composition across groups), treemap (many parts, hierarchy); pie or donut only for 2–3 parts where "roughly half" is the message |
| **Distribution** | Histogram, density, box plot, violin, strip/beeswarm (small n), ECDF (comparing distributions precisely), percentile bands |
| **Relationship between two numeric variables** | Scatter plot (add trend line or smoother if useful), hexbin or 2D density for many points, connected scatter for time |
| **Deviation from reference** | Diverging bar from a baseline, bullet chart (actual vs target), bar with a reference line |
| **Many series or groups** | Small multiples (same chart repeated per group, shared axes), highlighted line among grey context lines, heatmap |
| **Flow / process** | Sankey or alluvial (few nodes), funnel bars |
| **Geographic** | Choropleth (rates, not counts — counts just show population), proportional symbol map (counts), but ask whether geography is actually the point; a sorted bar chart of regions is often clearer |
| **Uncertainty** | Error bars or interval bands, gradient/fan charts, quantile dot plots; always say what the interval is |
| **Exact values matter** | A table. Not every number needs a chart. |

When two forms fit, pick the one the audience reads fluently. Novel chart types carry a learning cost; use them only when they show something the familiar forms cannot.

### Step 3 — Prepare the data for the chart

- Aggregate to the right level; sort categories by value (not alphabetically) unless they have a natural order (time, size bands, ordinal scales).
- Limit categories. Beyond ~7–10 lines or colors, readers cannot track them. Group the tail into "Other" (and say what is in it), highlight a few series against grey context, or use small multiples.
- Decide on rates vs counts, absolute vs indexed (indexing to 100 at a start date compares growth of series with different scales), and linear vs log scale (log for data spanning orders of magnitude or for comparing growth rates — label it clearly).
- Handle missing periods explicitly: a gap in the line, not interpolation that implies data you do not have.

### Step 4 — Build the encoding hierarchy

Decide, in order: what goes on x, what goes on y, what (if anything) is color, what is facet (small multiple), what is size or shape. Each additional encoding makes the chart harder to read; most good charts use two or three. If you need five, you probably need two charts.

### Step 5 — Apply color with purpose

See "Color" below. Default to one neutral color and add color only to encode something or to highlight.

### Step 6 — Label and annotate

- **Title states the takeaway** (for explanatory charts) or the question (for exploratory/reference charts). A subtitle can carry the metric definition, units, population and time range.
- **Label lines and bars directly** where possible instead of a legend; legends force eye travel and color matching.
- **Axis titles include units** ("Revenue (USD millions)", "Latency, p95 (ms)"). Format tick labels for readability (1.2M, not 1200000; dates in the audience's format).
- **Annotate the important point**: the event that caused a change, the threshold, the outlier worth explaining. Annotations do the work a presenter would do by pointing.
- **Source and notes**: data source, date extracted, definitions, exclusions, sample size. Small but present.

### Step 7 — Review against the destination

Render it at the actual size and medium: on the slide, in the document column, on a phone, in dark mode, in grayscale print. Check legibility of the smallest text, contrast, and whether the takeaway is visible within a few seconds.

## Color

### Choose the palette type from the data

| Data | Palette type | Notes |
|---|---|---|
| Unordered categories | **Categorical** (qualitative): distinct hues of similar lightness | Keep to roughly 6–8 distinguishable hues; beyond that, color stops working as an identifier |
| Ordered values from low to high | **Sequential**: one hue (or a perceptually uniform multi-hue ramp) varying mainly in lightness | Lightness should change monotonically; the darkest (or most saturated) end usually means "more" against a light background |
| Values diverging from a meaningful midpoint (zero, target, average, 50%) | **Diverging**: two hues meeting at a neutral midpoint | Only use when the midpoint is meaningful; the midpoint must be set at that value, not at the data's middle |
| Highlight vs context | **Accent**: one strong color, everything else neutral grey | Often the most effective palette in explanatory charts |

Use perceptually uniform colormaps (e.g., viridis-family, cividis, ColorBrewer and similar sets, or the project's own validated scales) for continuous data. Avoid rainbow/jet colormaps for quantitative data: their lightness is non-monotonic, which creates false boundaries and hides real ones, and they are hard for colorblind readers.

### Color must mean something, consistently

- The same category gets the same color across every chart in a report or dashboard.
- Do not use color for a dimension already encoded by position (bars colored by their own category label add nothing but noise and imply a legend lookup).
- Respect cultural and domain semantics where they exist (e.g., red for loss or error and green for gain or success in many finance and ops contexts) — and note that these are conventions, not universals; check the destination.
- Do not rely on color alone. Pair it with direct labels, position, shape, line style or patterns so the chart works for colorblind readers, in grayscale print, and on poor displays.

### Colorblind safety and contrast

- About 1 in 12 men and 1 in 200 women have some form of color vision deficiency, most commonly red–green. Avoid red/green as the only distinguishing pair; blue/orange is a robust alternative contrast.
- Vary lightness, not just hue, between categories that must be distinguished.
- Check with a color-vision-deficiency simulator (many design tools and browser devtools include one) and in grayscale.
- Text and essential graphical elements need adequate contrast against the background (WCAG suggests at least 4.5:1 for normal text and 3:1 for large text and meaningful graphics); see `accessible-design`.
- In dark mode, palettes need adjusting, not just inverting: saturated colors that work on white may vibrate on black, and sequential scales may need their direction reconsidered.

### Where colors come from

If the destination has a design system, brand palette or chart tokens, use them — and check that they include proper categorical, sequential and diverging scales with adequate contrast. If they do not, derive scales that harmonise with the brand's colors while meeting the perceptual rules above, and flag any brand color that fails contrast. If there is no context at all, use a well-tested neutral palette and keep it minimal. Never present one palette as "the" right one; it is a choice made for a context.

## Axes and scales: honesty rules

- **Bar and area charts start at zero.** Length and area encode magnitude; truncating the baseline exaggerates differences. If differences are small relative to the values, use a dot plot or line chart (which do not need zero) or plot the difference itself.
- **Line charts may start away from zero** when the point is change and the range is meaningful — but choose a range that does not manufacture drama; including context (e.g., historical range) helps.
- **Dual y-axes** are easy to manipulate: by rescaling either axis you can make any two series appear correlated or not. Prefer two aligned panels, indexing both series, or plotting the ratio. If a dual axis is unavoidable, color-code each axis to its series and say why.
- **Time on a uniform scale.** Uneven intervals (2010, 2015, 2020, 2021, 2022) plotted evenly distort trends.
- **Log scales** must be labelled as such, with readable tick values (1, 10, 100), and are inappropriate for audiences unfamiliar with them unless explained.
- **Aspect ratio** changes perceived slope. Aim for a ratio where the important slopes are near 45° rather than flattened or exaggerated; be consistent across comparable charts.
- **Shared axes in small multiples** unless the point is shape rather than magnitude; if axes are free, say so clearly.
- **Per-capita and rate normalisation** for comparisons across groups of different size (maps especially).
- **Cumulative charts** always go up and can hide a slowdown; show the per-period values when the rate matters.

## Form-specific craft

### Line charts

- Use for continuous data, usually time. Do not connect points across categories that have no order.
- Mark gaps for missing periods; show partial current periods as dashed or annotated, or exclude them.
- Label line ends directly with the series name; this nearly always beats a legend.
- More than about five lines: grey the context, color the focus series.
- Show event markers (launches, outages, policy changes) as vertical reference lines with short labels.

### Bar and column charts

- Horizontal bars for category names longer than a word or for many categories; vertical columns for time periods.
- Sort by value unless the order is intrinsic. Put the most important category where the eye lands first.
- Bar width roughly 1.5–2× the gap looks balanced; very thin bars read as lines.
- Grouped bars work for 2–3 subgroups; beyond that, use small multiples or a dot plot.
- Label values at the bar ends when exact values matter, and drop the value axis if every bar is labelled.

### Scatter plots

- Overplotting hides density: use transparency, smaller marks, jitter for discrete values, hexbin or contour density for thousands of points.
- Add a trend line only if it reflects a model you would defend; show the raw points too.
- Label notable points directly rather than all points.
- Correlation is not slope: a steep line through a cloud with r = 0.2 still means weak association.

### Distributions

- Histograms depend on bin width; try several, and choose one that shows structure without noise. State the bin width if it matters.
- Box plots hide multimodality and sample size; overlay points (for n below a few hundred) or use violins/strip plots.
- ECDFs compare distributions precisely and need no binning but are less familiar to general audiences.
- For heavily skewed data, consider a log axis and say so.

### Tables

A well-made table is often better than a chart when readers need to look up values. Right-align numbers, use consistent decimals, align on the decimal point, put units in headers, group rows meaningfully, use subtle row separation rather than heavy borders, and highlight the few cells that matter. Inline bars or small sparklines can add pattern to a table without losing precision.

### Interactive charts

Interactivity (tooltips, zoom, filters, hover highlighting) helps exploration and reference use, but the default view must still communicate the main point without interaction — many readers never hover, touch devices have no hover, and screenshots lose it. Do not hide essential information in tooltips. Make interactive elements keyboard-accessible and provide a data table alternative.

## Small multiples

Repeat the same chart for each group, with shared scales, arranged in a meaningful order (by value, by geography, by time). They beat overloaded single charts with ten colored lines, and they beat animation for comparison because all panels are visible at once. Keep each panel minimal, label panels clearly, and highlight the one that matters if there is a takeaway.

## Uncertainty

Show it when the decision depends on it: comparisons between groups, forecasts, survey estimates, experiment results. Options: error bars (say whether SD, SE or a confidence interval), shaded interval bands, fan charts for forecasts, multiple plausible outcomes. Avoid presenting a point forecast as a single crisp line into the future. Readers systematically overread precision from clean lines.

## Text, numbers and typography in charts

- Use the destination's typeface and sizes; chart text should feel like part of the surrounding document, not a pasted image.
- Size for the medium: text that is comfortable in a document is often unreadable on a projected slide or a phone. Check the smallest label at real size.
- Keep text horizontal. Rotated axis labels are a sign the chart should be flipped to horizontal bars.
- Round numbers to the precision that matters (two or three significant figures for most explanatory charts) and use consistent formats across a set of charts.
- Use thousands separators and abbreviations (k, M, B) appropriate to the audience's locale; be careful that "B" (billion) and "bn" conventions match.
- Hierarchy through weight and size: title most prominent, then data labels and annotations, then axis labels, then source notes.

## Critiquing an existing chart

When asked to review or improve a chart, work through these in order and report findings by impact:

1. **Question** — What is this chart supposed to answer? Does it answer it? Is the takeaway visible in a few seconds?
2. **Truth** — Are the numbers right (spot-check against data)? Are baselines, scales, areas and time intervals honest? Is uncertainty hidden?
3. **Form** — Does the chart type match the comparison? Would a different form, small multiples, or a table be clearer?
4. **Encoding** — Is the main comparison on position or length? Are there more encodings than the reader can decode?
5. **Color** — Purposeful, appropriate palette type, consistent, colorblind-safe, not the only cue?
6. **Labels** — Title, axis titles with units, direct labels, annotations, source?
7. **Fit** — Does the style match the destination, size and theme?

Lead with issues that would cause a reader to misunderstand, then issues that slow them down, then polish. Propose a concrete fix for each, and where possible show the revised chart.

## Discovering context

Before styling anything, find:

- **The destination and medium**: report, slide, dashboard, app, print, publication, social media. Each has size, density and legibility constraints.
- **Existing design tokens, chart themes or style guides** in the codebase, design system, BI tool theme, or brand guidelines. Use them.
- **Existing charts** in the same report, product or publication — match their conventions (fonts, number formats, date formats, color assignments for recurring categories).
- **The audience's fluency**: analysts can read box plots and log scales; a general audience may need simpler forms and more annotation.
- **Light/dark mode, localisation** (number and date formats, right-to-left layouts), and accessibility requirements.
- **The tool in use** and its theming mechanism, so styling is set once in a theme rather than per chart.

## Explanatory vs exploratory charts

| | Exploratory | Explanatory |
|---|---|---|
| Audience | You or other analysts | Decision-makers, readers |
| Goal | Find patterns, check assumptions | Communicate a specific finding |
| Volume | Many quick charts | Few, polished |
| Design | Defaults are fine; speed matters | Deliberate encoding, color, annotation, title stating the takeaway |
| Risk | Missing something | Misleading or confusing someone |

Do not ship exploratory charts as explanatory ones. Rework them: cut series, add the takeaway, annotate.

## Pitfalls and anti-patterns

- **Pie charts with many slices** or used to compare similar values; donut charts with a number in the middle that conveys everything the chart does not.
- **3D charts** of any kind for 2D data — perspective distorts lengths and areas.
- **Truncated bar baselines**.
- **Spaghetti charts**: many overlapping colored lines. Use highlight-and-grey or small multiples.
- **Rainbow colormaps** for quantitative data.
- **Legends far from the data** when direct labels would fit.
- **Alphabetical sorting** of categories that should be ranked.
- **Area or bubble size** scaled by radius instead of area (doubling the radius quadruples the area).
- **Choropleths of raw counts**, which just map population.
- **Stacked charts used to compare middle segments** — only the bottom segment and the total share a baseline.
- **Unlabelled axes, missing units, ambiguous dates** (is 03/04 March or April?).
- **Too many decimal places** in labels.
- **Smoothing that hides important features**, or interpolating across missing data.
- **Color for decoration**: every bar a different color for no reason.
- **Charts that only work in color** (failing in grayscale print and for colorblind readers).
- **Hiding uncertainty** behind crisp lines and precise-looking labels.
- **Default styling unexamined**: library defaults are designed for generic use, not your destination; they may be fine, but check.

## Quality bar and verification

- [ ] The chart answers a stated question; the title states the takeaway (explanatory) or the question (reference).
- [ ] The key comparison is encoded on position or length, not color or area.
- [ ] The chart form fits the comparison type, and a table was considered where exact values matter.
- [ ] Bars and areas start at zero; non-zero baselines on lines are justified; dual axes avoided or clearly justified.
- [ ] Categories are sorted meaningfully; the number of series or colors is manageable.
- [ ] Color has a purpose, uses the right palette type, is consistent across charts, and is not the only encoding.
- [ ] The chart passes a colorblind simulation and is legible in grayscale; text meets contrast requirements.
- [ ] Axes have titles with units; numbers are formatted for readability; dates are unambiguous.
- [ ] Direct labels or a nearby legend; annotations explain the key points.
- [ ] Source, definitions, time range and sample size are shown.
- [ ] Uncertainty is shown where the conclusion depends on it, with the interval type stated.
- [ ] Style matches the destination's conventions and tokens; checked at real size and in each relevant theme.
- [ ] **Values on the chart were verified against the underlying data** — spot-check at least the maximum, minimum and one middle value, and confirm totals match the source.
- [ ] A fresh viewer, given a few seconds, can say what the chart shows.

For accessibility beyond the visual: provide alt text or a caption that states the takeaway and key values, and where charts are interactive or critical, provide the underlying data as a table or download.

## Worked reasoning: redesigning a cluttered chart

Starting point: a 3D pie chart of revenue share by 11 product lines, with a legend, for a quarterly review asking "which product lines are growing?"

1. **The question is about growth, not share.** A pie cannot show change over time at all.
2. **Comparison type**: change across categories → slope chart (last year vs this year) or sorted bar of growth rate, possibly with revenue size indicated.
3. **Too many categories**: highlight the three lines with the largest absolute growth and the two declining ones; group or grey the rest.
4. **Encoding**: growth rate on a horizontal bar from zero, sorted descending; diverging colors only if the review cares about growth vs decline — here it does, so growth bars in one hue, decline in another, both checked for colorblind distinguishability, with values labelled at bar ends.
5. **Context**: subtitle gives the period and that growth is year-on-year revenue; a note gives the source.
6. **Destination**: a slide on a projector — larger text, fewer labels, the brand's chart colors from the deck theme.
7. **Title**: "Three product lines drove 80% of this year's growth; two declined."

The result answers the question in seconds, uses position for the key comparison, and every color carries meaning.
