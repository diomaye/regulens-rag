# regulens-rag

Bilingual (FR/EN) question-answering over public Canadian financial-regulation documents
(OSFI/BSIF, AMF, FINTRAC/CANAFE, Québec Law 25). Answers must cite document, section and
page, and must refuse when the answer is not in the corpus.

This is a portfolio project for an AI Forward Deployed Engineer role. Code quality, evals and
governance artifacts matter as much as features.

## How we work (read first)

- Work one milestone at a time. Milestones and acceptance criteria are in `docs/PLAN.md`.
- Before editing files for a milestone, present a short plan and wait for approval.
- Stop at the end of a milestone. Do not start the next one unprompted.
- When a choice is genuinely ambiguous (library, schema, trade-off), ask. For small choices,
  pick a sensible default and state it.
- Any non-trivial technical decision gets an ADR in `docs/adr/` (use `/adr`).
- Keep `docs/PROGRESS.md` updated: what was done, what is left, open questions.
- Explain the *why* of key choices in your summary. The owner is learning; teach, don't just do.

## Stack

- Python 3.12, `uv`, src layout, package `regulens` in `src/regulens/`
- FastAPI + Pydantic v2, `pydantic-settings` for config
- Postgres 16 + `pgvector` (docker compose), `psycopg` v3
- PDF extraction: `pymupdf`
- Embeddings: multilingual only (default `BAAI/bge-m3` via `sentence-transformers`)
- LLM: Anthropic API, model name from config (`LLM_MODEL`), never hardcoded
- Tests: `pytest`; lint/format: `ruff`; types: `mypy --strict`

## Commands

- `make setup` install deps, start db
- `make test` unit tests (no network, no LLM)
- `make lint` ruff + mypy
- `make eval` full eval suite; `make eval-smoke` fast subset
- `make run` start API locally

## Code standards

- Full type hints; `mypy --strict` must pass.
- Dependencies behind interfaces (`Embedder`, `Retriever`, `Reranker`, `LLMClient`) so
  implementations can be swapped and faked in tests.
- Unit tests never call the network or an LLM. Tests that do are marked `@pytest.mark.llm`.
- No print debugging in committed code; use structured JSON logging.
- Small, focused commits with conventional commit messages (`feat:`, `fix:`, `docs:`, `test:`).

## Governance rules (non-negotiable)

- Public or synthetic data only. Never add client, employer or personal data.
- Never read, print or commit secrets. `.env` is off-limits; use `.env.example` for keys.
- Every generated answer is logged with: `prompt_version`, `model`, `index_version`,
  `corpus_hash`. No raw user PII in logs.
- `evals/golden_set.jsonl` is written by a human. Do not generate, edit or "fix" its questions.
  You may build tooling that reads and validates it.
- Never lower `evals/thresholds.yaml` or change the golden set to make evals pass. If a
  threshold is missed, report it and propose fixes to the system instead.
- Every downloaded source is recorded in `data/manifest.csv` with URL, issuer, language,
  version date and SHA-256.
