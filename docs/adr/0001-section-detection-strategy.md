# 0001. Section detection strategy

- Status: accepted
- Date: 2026-10-01

## Context

Ingested PDFs must be split into meaningful sections (with title, level, page range) so that
downstream chunking and retrieval can cite specific sections. The quality of section boundaries
directly affects citation accuracy and retrieval recall.

Regulatory PDFs vary widely: some have clean numbered headings ("1.2.3 Title"), others use
ALL-CAPS headings, and some have inconsistent formatting. Scanned PDFs are out of scope.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Regex on text patterns** (numbered headings + ALL-CAPS) | Simple, no font metadata needed, works on any text extraction output, easy to debug and extend | Misses headings that don't follow conventions; false positives on short ALL-CAPS acronyms |
| **PyMuPDF font-size analysis** (detect headings by larger/bolder font) | Catches visually distinct headings regardless of text pattern; closer to human reading | Depends on PDF internal structure; unreliable for PDFs with inconsistent font metadata; more complex to tune per-document |
| **LLM-based section splitting** | Handles arbitrary formatting; understands semantic boundaries | Expensive at ingestion time; non-deterministic; adds LLM dependency to offline pipeline |

## Decision

Use **regex-based detection** on numbered headings (`1.`, `1.2`, `A.1`) and ALL-CAPS lines
(minimum 4 characters to reduce false positives). A synthetic "Preamble" section captures text
before the first heading.

This is the simplest approach that works for well-structured regulatory documents (which are
the target corpus). It keeps ingestion deterministic, fast, and free of LLM calls.

## Consequences

- **Easier:** ingestion is fast, deterministic, and testable with fixture PDFs.
- **Harder:** documents with non-standard headings (e.g., bold-only, no numbering) will produce
  fewer or larger sections. Some ALL-CAPS lines may be false positives.
- **Monitor:** during M3 evals, check whether retrieval recall is lower for specific documents.
  If a document consistently produces poor sections, inspect its heading patterns.
- **Wrong signal:** if more than 20% of documents produce only 1-2 sections, the regex patterns
  are too narrow and we should add font-size analysis as a fallback.
