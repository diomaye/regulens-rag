# 0002. Language detection approach

- Status: accepted
- Date: 2026-10-01

## Context

Each document has a `language` field curated by the owner in `data/manifest.csv`. We also need
to detect the actual language of the extracted text for two reasons: (1) validate the manifest
entry, and (2) set language-aware tsvector configuration for full-text search in M2.

The corpus is bilingual (French/English) with no other languages expected.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **Trust manifest only** (no detection) | Zero complexity; owner controls the value | No validation; errors in manifest silently degrade retrieval |
| **langdetect library** (statistical n-gram model) | Well-tested, handles FR/EN well, deterministic with seed, no external API | Extra dependency; can be wrong on very short text; overkill for a 2-language corpus |
| **Simple French keyword heuristic** (count "les", "des", "une", etc.) | No dependency; fast; transparent | Fragile on bilingual documents; hard to extend if more languages are added |

## Decision

Use **langdetect** as a validation layer. The manifest `language` field remains the source of
truth, but `detected_language` is stored alongside it. If they disagree, the ingestion report
flags the mismatch for the owner to investigate — it does not block ingestion.

langdetect is seeded for determinism. Short text (< 20 chars) defaults to English.

## Consequences

- **Easier:** mismatches between manifest and detected language surface early, before they
  affect retrieval quality.
- **Harder:** adds one dependency (`langdetect`). If it becomes unmaintained, replace with the
  heuristic approach.
- **Monitor:** count mismatches in the ingestion report. If > 5% mismatch, either the manifest
  has errors or the detector is unreliable on the corpus.
- **Wrong signal:** if langdetect is wrong on well-formed regulatory French text, replace with
  a simple heuristic or a newer library like `lingua`.
