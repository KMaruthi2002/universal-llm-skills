---
name: rag-systems
description: >-
  Design, build, debug, and evaluate retrieval-augmented generation systems
  that answer questions from documents, knowledge bases, codebases, or
  databases: ingestion and parsing, chunking strategy, embeddings, vector and
  keyword (hybrid) search, reranking, metadata and permission filters, query
  rewriting, prompt assembly with citations, freshness and re-indexing, and
  separate evaluation of retrieval and answer quality. Use when building "chat
  with your docs", semantic search, a knowledge-base assistant, grounding an
  LLM in private data, or when a RAG system returns wrong, missing, stale, or
  uncited answers. Also covers deciding when RAG is the wrong tool. For the
  general LLM app plumbing use llm-application-development; for scoring use
  llm-evaluation.
metadata:
  category: ai-ml
  related: llm-application-development, prompt-engineering, llm-evaluation, ai-safety-and-guardrails, etl-pipelines, database-design, data-cleaning-and-validation, chatbot-and-conversational-apps
---

# Retrieval-Augmented Generation

RAG gives a model the right evidence at the moment it answers. It is a search system with a language model at the end. Most RAG failures are search failures: the right passage was never retrieved, so no prompt could have saved the answer. Build and measure it as a search system first.

## Scope

Covers: deciding whether RAG fits; ingestion and parsing; chunking; embeddings; indexes; lexical, semantic, and hybrid retrieval; reranking; filtering and access control; query transformation; context assembly; grounded generation with citations; freshness; evaluation and debugging.

Neighbours: `llm-application-development` (call plumbing, caching, budgets), `prompt-engineering` (the generation prompt), `llm-evaluation` (eval methodology), `etl-pipelines` (ingestion at scale), `ai-agents-and-tool-use` (agentic retrieval where the model issues its own searches), `ai-safety-and-guardrails` (injection through retrieved content).

## When RAG is the right tool, and when it is not

| Situation | Better approach |
|---|---|
| Answers live in a large, changing corpus of text the model has not seen | **RAG** |
| The whole corpus fits comfortably in the context window and changes rarely | Put it all in context (with prompt caching); simpler and often more accurate |
| Questions are about structured data ("how many orders last week?") | Text-to-SQL or an API tool, not embedding search over rows |
| The model needs a style, format, or skill, not facts | Prompting or fine-tuning (`fine-tuning-models`) |
| Questions require aggregating across the whole corpus ("what are the common themes in all 10,000 tickets?") | Map-reduce summarisation, analytics, or pre-computed summaries; top-k retrieval cannot see everything |
| Exact lookups by ID, name, or code | Keyword search or a database query |
| The answer must be computed (pricing, eligibility) | Deterministic code that the model calls as a tool |
| Precision is safety-critical and the corpus is small and stable | Curated FAQ or decision tree, possibly with the model only paraphrasing |

Often the answer is a hybrid: a model with several tools — document search, SQL, specific APIs — choosing among them.

## Core principles

### 1. Retrieval quality caps answer quality

If the relevant passage is not in the context, the model will either say it does not know (best case) or fabricate (common case). Measure retrieval separately from generation so you know which half is failing.

### 2. Chunks are the unit of retrieval and of meaning

A chunk must make sense on its own, because that is how the model will see it. A chunk that says "this setting must be disabled first" without saying which setting is useless. Chunking is the highest-leverage, most under-examined decision in most RAG systems.

### 3. Lexical and semantic search fail differently

Embedding search captures meaning and paraphrase but is weak on exact identifiers, rare terms, product codes, names, and negation. Keyword search (e.g. BM25) nails exact terms but misses paraphrase. Combining them (hybrid) is a robust default because their failure modes are largely complementary.

### 4. Permissions are enforced at retrieval, not in the prompt

If a user may not see a document, it must never enter their context. "Do not reveal confidential documents" in a prompt is not access control. Filter by the user's permissions in the retrieval query itself.

### 5. Ground and cite, so answers can be checked

Instruct the model to answer only from retrieved material, to say when the material is insufficient, and to cite which passage supports each claim. Citations let users verify, let you evaluate faithfulness, and make fabrication visible.

### 6. Retrieved text is untrusted input

Documents, web pages, and user-uploaded files can contain instructions aimed at the model. Delimit retrieved content as data and limit what actions the system can take based on it.

## Discovering context

- **The corpus**: formats (PDF, HTML, docs, slides, spreadsheets, code, transcripts), size, languages, structure (headings, sections, tables), quality (scans, OCR noise, duplicates, boilerplate), and how often it changes.
- **The questions**: collect real questions from users, support logs, or search logs. Classify them: factual lookup, how-to, comparison, troubleshooting, aggregation, out-of-scope. The mix determines the design.
- **Permissions**: who may see what, and where that information lives (document ACLs, groups, tenants).
- **Existing infrastructure**: an existing search engine or database with vector support may be better than adding a new vector store. Check what the project already runs (many relational and search databases now support vector indexes).
- **Freshness requirements**: minutes, hours, or days of acceptable staleness.
- **Quality and latency targets**, and the cost of a wrong answer in this domain.

## The pipeline

### 1. Ingestion and parsing

Garbage in is the most common root cause of bad RAG. Before tuning anything downstream, look at the parsed text of a sample of documents.

- Extract text with structure preserved: headings, lists, tables, code blocks. Headings become metadata and context for chunks.
- PDFs are hard: multi-column layouts, headers/footers, tables, and scanned pages need appropriate parsers or OCR. Check output by reading it.
- Tables: convert to a text form that keeps row/column relationships (e.g. markdown or "column: value" lines), or index them separately.
- Remove boilerplate (navigation, cookie banners, repeated footers) that pollutes embeddings and wastes context.
- Deduplicate near-identical documents and versions; otherwise top-k fills with copies.
- Capture metadata: source, title, URL or path, section path, author, created/updated dates, version, language, product, permissions, document type.
- Keep a stable document ID and a content hash to support incremental re-indexing.

### 2. Chunking

Goals: each chunk is self-contained enough to be understood, small enough to be specific, large enough to contain a full answer.

| Strategy | Good for | Weakness |
|---|---|---|
| Fixed-size token windows with overlap | Unstructured text, quick baseline | Splits mid-thought; overlap duplicates content |
| Structure-aware (by headings, sections, paragraphs) | Documentation, policies, manuals | Sections vary wildly in length; needs size limits and splitting of long sections |
| Semantic splitting (by topic shift) | Long narrative text, transcripts | Extra cost and complexity; inconsistent |
| Code-aware (by function, class, file) | Codebases | Cross-file context lost |
| Record-per-item (one FAQ, one ticket, one product) | Naturally atomic content | — |
| Hierarchical / parent-child (retrieve small, return the larger parent) | When precise matching and full context both matter | More storage and logic |

Heuristics:

- Start with structure-aware chunking with a size cap, a few hundred tokens per chunk as a starting point, then tune by measurement. There is no universally right size; it depends on the content and the questions.
- **Contextualise chunks**: prepend the document title and section path (and optionally a one-sentence summary of the document) to each chunk's text before embedding. This fixes a large class of "orphan chunk" failures where the chunk does not mention what it is about. Generating a short chunk-specific context with a model is a stronger version of this, at ingestion cost.
- Never split tables, code blocks, or numbered procedures in the middle if avoidable.
- Keep a pointer from each chunk to its neighbours and parent so you can expand context at query time.

### 3. Embeddings

- Choose an embedding model by testing on your own queries and documents; public benchmarks are only a rough guide. Consider languages, domain (legal, medical, code), maximum input length, dimension (storage cost), and hosting (API vs local).
- Use the same model (and version) for documents and queries. Some models expect different prefixes or modes for queries vs documents; follow their documentation.
- Changing the embedding model means re-embedding the entire corpus. Store the model name and version with each vector.
- Normalise vectors if the similarity metric requires it.

### 4. Indexing and storage

- Options include dedicated vector databases, vector extensions to existing relational or document databases, and search engines with vector support. Prefer what the project already operates unless scale or features demand otherwise.
- Approximate nearest neighbour indexes trade recall for speed; know your index parameters and measure recall against exact search on a sample.
- Store metadata in a filterable form alongside vectors. Filtering after retrieval (post-filtering) can return far fewer than k results; prefer pre-filtering or engines that filter during search.
- Maintain a keyword index too, for hybrid search.

### 5. Query processing

User queries are often short, vague, misspelled, or conversational ("what about the other one?").

- **Conversational rewriting**: in multi-turn chat, rewrite the latest message into a standalone query using conversation history. Without this, follow-up questions retrieve garbage.
- **Query expansion**: generate a few paraphrases or sub-queries and retrieve for each; merge results. Helps recall; costs latency.
- **Decomposition**: split multi-part questions ("compare plan A and plan B pricing") into separate retrievals.
- **Hypothetical answer embedding**: embed a model-generated draft answer instead of the question, which can sit closer to answer passages in embedding space. Test it; it helps on some corpora and hurts on others, and can inject the model's wrong assumptions.
- **Metadata extraction**: pull filters from the query (product name, date range, version) and apply them as structured filters.
- **Routing**: decide whether the query needs retrieval at all, which index, or a different tool (SQL, API).

### 6. Retrieval

- **Hybrid search**: run keyword and vector search, merge with a rank-fusion method (reciprocal rank fusion is a simple, robust default that needs no score calibration) or weighted scores.
- **Retrieve generously, then narrow**: fetch a larger candidate set (e.g. dozens) for the reranker, then pass a smaller set to the model.
- **Filters**: permissions always; plus tenant, language, product, version, date as appropriate.
- **Diversity**: avoid filling all slots with near-duplicate chunks from one document when the question needs breadth (e.g. maximal marginal relevance).

### 7. Reranking

A cross-encoder or model-based reranker scores each (query, chunk) pair jointly and is much more accurate than embedding similarity alone, at higher cost per candidate. Reranking a few dozen candidates down to a handful is one of the most reliable quality improvements available. Measure its latency; it is usually acceptable for interactive use at modest candidate counts.

### 8. Context assembly

- Order matters: put the most relevant chunks where the model attends best (often first, sometimes last; test).
- Include source metadata with each chunk (title, date, ID for citation).
- Expand to parent sections or neighbouring chunks when the matched chunk is a fragment.
- Respect the token budget: fewer, better chunks beat many mediocre ones. Irrelevant context actively degrades answers and costs money.
- Delimit each chunk clearly and mark the block as reference data, not instructions.

### 9. Generation

The generation prompt should:

- instruct the model to answer only from the provided sources;
- tell it what to do when sources are insufficient or conflict (say so, present both with dates, prefer the newer or more authoritative per your rules);
- require citations in a defined form that the application can parse and link;
- set the audience, length, and format.

Post-process: verify that cited IDs exist in the provided context; optionally verify that cited passages actually support the claims (a second model check or string matching for quotes). Strip or flag uncited claims in high-stakes domains.

### 10. Freshness and maintenance

- Incremental indexing using content hashes and updated timestamps; handle deletions (deleted source documents must disappear from the index, especially for permission or legal reasons).
- Re-index on parser, chunker, or embedding changes; version the index so you can roll back.
- Surface document dates in answers when currency matters.
- Monitor index size, ingestion failures, and the age distribution of content.

## Agentic retrieval

Instead of a fixed retrieve-then-generate pipeline, the model can be given search tools and decide what to search for, iteratively. This helps for multi-hop questions and exploratory research, at the cost of latency, tokens, and predictability. A good middle ground: a fixed first retrieval, then allow the model a bounded number of follow-up searches. See `ai-agents-and-tool-use`.

## Evaluation

Evaluate retrieval and generation separately, then end to end.

### Retrieval metrics

Build a set of questions with known relevant chunks or documents (labelled by people, or bootstrapped by having a model generate questions from chunks and then human-checking a sample — synthetic questions tend to be easier and more lexically similar than real ones, so do not rely on them alone).

- **Recall@k**: fraction of questions where a relevant chunk appears in the top k. The most important retrieval metric, because the generator cannot use what is not retrieved.
- **Precision@k / MRR / nDCG**: how highly relevant chunks rank, which matters when context budget is tight.
- Compute these for each change: chunk size, embedding model, hybrid weights, reranker, query rewriting.

### Answer metrics

- **Faithfulness / groundedness**: every claim is supported by the retrieved context.
- **Answer relevance / correctness**: it answers the question correctly (against a reference answer where available).
- **Citation accuracy**: citations point to passages that support the claim.
- **Abstention quality**: correctly says "not found" for unanswerable questions; include unanswerable questions in the test set on purpose.

Model-based judges can score these at scale; calibrate them against human labels first (`llm-evaluation`).

### Debugging a bad answer

Work backwards:

1. Is the answer in the corpus at all? If not, it is a content gap — tell the content owners.
2. Was it parsed correctly? Read the parsed text.
3. Is it in a coherent chunk? Read the chunk.
4. Was it retrieved in the candidate set? If not: query mismatch (try rewriting, hybrid, better embeddings), filter excluded it, or chunk lacks context.
5. Did it survive reranking and make it into the context? If not: reranker or budget issue.
6. Was it in the context but the model ignored or misread it? Then it is a generation problem: prompt, ordering, too much distracting context, conflicting sources.

Log every stage (rewritten query, candidates with scores, reranked list, final context) so this walk takes minutes, not hours.

## Latency and cost budget

A RAG request can include: query rewriting (model call), embedding the query, keyword and vector searches, reranking, and generation. Measure each stage.

- Run keyword and vector searches in parallel.
- Skip query rewriting for first-turn queries that are already standalone; use a small model when it is needed.
- Bound reranker candidates; reranking cost grows linearly with them.
- Cache query embeddings and retrieval results for frequent queries, keyed by permission scope and index version.
- Fewer, better chunks in the final context reduce generation cost and usually improve answers.
- Put stable instructions first in the generation prompt so provider prefix caching applies.

## User experience of grounded answers

- Show citations as links to the exact source location (page, section, anchor), not just the document title, so users can check quickly.
- Show document dates where currency matters.
- When the system cannot find an answer, say so plainly and offer what it did find or where to look next; a confident wrong answer does more damage than an honest "not found".
- Let users report wrong answers with one action, and route those reports into the evaluation set.

## Tuning procedure

Change one thing at a time against a fixed retrieval test set, in roughly this order, because earlier stages bound later ones:

1. **Parsing fixes** (read failures; fix extraction). Often the biggest single gain.
2. **Chunking**: try two or three strategies or sizes; add contextual headers. Re-measure recall@k.
3. **Hybrid search**: add keyword search if not present; tune fusion.
4. **Embedding model**: compare two or three candidates on your data.
5. **Reranker**: add one; tune candidate count and final k.
6. **Query rewriting** for conversational and vague queries.
7. **Generation prompt**: grounding, citations, abstention.

Record each configuration and its metrics. Keep the configuration that wins on the held-out portion, not only the development portion.

## Special content types

- **Code**: chunk by syntactic unit (function, class) with file path and enclosing class/module in the chunk header; combine with symbol search (exact names) and, for agentic coding, tools that grep and open files. Embeddings alone handle identifier lookups poorly.
- **Tables and spreadsheets**: small tables can be serialised into chunks; large ones belong in a database queried via a tool. Retrieval over rows of numbers rarely answers aggregate questions.
- **Multilingual corpora**: use a multilingual embedding model, or translate queries; test cross-language retrieval explicitly (query in one language, answer document in another). Keyword search needs language-appropriate analysers.
- **Transcripts and chat logs**: chunk by topic or time window, keep speaker labels, and include the meeting or thread title and date.
- **Images and scanned documents**: OCR or vision-model captions for text; multimodal embeddings for visual similarity. Verify OCR quality on a sample.
- **Highly versioned docs** (product versions, policy revisions): store version metadata, filter by the user's version, and default to the latest when unspecified — otherwise answers mix incompatible versions.

## Permissions in practice

- Store access-control metadata (owner, groups, tenant, visibility) with each chunk, sourced from the system of record at ingestion.
- Apply the filter for the requesting user in the search query itself, for both keyword and vector indexes.
- Permission changes in the source must propagate: re-sync ACLs on a schedule appropriate to the sensitivity, and immediately for revocations where possible.
- For strong isolation between tenants, consider separate indexes or namespaces rather than filters alone.
- Write tests that a user without access cannot retrieve a restricted document by any query, including by searching its exact title.
- Caches of retrieval results or answers must be keyed by permission scope.

## Worked reasoning: a wrong answer, traced

Illustrative. Users ask "Can I get a refund after 30 days?" and the assistant says "No, refunds are only available within 30 days", but the policy was changed last quarter to 60 days for annual plans.

- Corpus check: the new policy page exists. Parsed text is fine.
- Retrieval log: both the old and new policy pages are in the top candidates; the old one ranks first. Both chunks say "refund" and "30 days" (the new one says "30 days for monthly, 60 days for annual").
- The old page was never deleted from the index because ingestion only adds and updates — the source page was moved to an archive URL, so it looked like a new document.
- Generation: given two conflicting sources with no dates, the model chose the first.

Fixes, in order of importance: handle deletions and moves (archived pages excluded or tagged); add document effective dates to metadata and include them in context; instruct the model to prefer the most recent effective policy and to mention plan-type distinctions; add this question and an "annual plan" variant to the regression set. Note that no prompt change alone would have fixed the stale index.

## Pitfalls

- **Tuning prompts when retrieval is the problem.** Check recall first.
- **Never reading the parsed text or chunks.** Most quality problems are visible to the naked eye.
- **Orphan chunks** without the context needed to interpret them.
- **Vector-only search for identifier-heavy content** (part numbers, error codes, legal citations).
- **Prompt-based access control.** Data leaks across users or tenants.
- **Stale or deleted documents still served** because ingestion only adds.
- **Top-k for aggregation questions** that need the whole corpus.
- **Too much context**: twenty chunks "to be safe" lowers accuracy and raises cost.
- **Synthetic-only eval sets** that overestimate quality.
- **Changing several pipeline parameters at once** and not knowing which helped.
- **Mixing embedding model versions** in one index.
- **Citations that are not verified** and point to the wrong passage.
- **Ignoring conversational context** so follow-up questions fail.
- **Injected instructions in documents** obeyed as commands.

## Quality bar and verification

A RAG system is ready when:

- There is a test set of real (or human-checked) questions, including unanswerable and adversarial ones.
- Retrieval recall@k is measured and acceptable, and each pipeline change was justified by a measured improvement.
- Answers are grounded, cite sources, and abstain when sources are insufficient; this is measured.
- Permissions are enforced in the retrieval query, verified by tests that a user cannot retrieve a document they lack access to.
- Ingestion handles updates and deletions; freshness meets the requirement.
- Each stage is logged so any bad answer can be traced.
- Latency and cost per query meet budget with the reranker and any query expansion included.
- Retrieved content is delimited as data, and the system cannot take consequential actions solely on instructions found in documents.
