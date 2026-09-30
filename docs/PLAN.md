# Build plan: regulens-rag

Each milestone ends with: `make lint` and `make test` green, `docs/PROGRESS.md` updated,
ADRs written for decisions made, one or more commits. Then stop.

## M0: Scaffold (day 1–2)

Build:
- `uv` project, src layout, package `regulens`, `py.typed`
- ruff, mypy (strict), pytest config in `pyproject.toml`; `llm` pytest marker
- `Makefile` with the targets listed in CLAUDE.md
- `docker-compose.yml` with `pgvector/pgvector:pg16`, healthcheck, named volume
- `src/regulens/config.py` using pydantic-settings; complete `.env.example`
- `.github/workflows/ci.yml`: uv sync --frozen, lint, mypy, `pytest -m "not llm"`
- README skeleton (problem, architecture placeholder, results placeholder, limits)
- `docs/architecture.md` with a mermaid diagram of the planned flow
- `.gitignore` covering `.env`, `data/raw/`, caches

Done when: fresh clone → `make setup && make test` passes; CI green on first push.

## M1: Ingestion (week 1)

Build:
- Loader for `data/manifest.csv` (the owner curates URLs; you validate the schema)
- Downloader: saves to `data/raw/`, computes SHA-256, fails loudly on hash mismatch
- PDF extraction with page numbers; section detection (headings/numbering)
- Language detection per document; normalization (whitespace, hyphenation, headers/footers)
- Tables `documents` and `sections` with migrations (plain SQL files are fine)
- Unit tests on a tiny fixture PDF in `tests/fixtures/`

Done when: all manifest documents ingested; per-document report (pages, sections, language);
corpus hash computed and stored.

## M2: Chunking, embeddings, hybrid retrieval

Build:
- `Chunker` interface with two strategies: section-aware (with overlap) and fixed-size
- `Embedder` interface; `bge-m3` implementation; batch embedding with progress
- `chunks` table with pgvector HNSW index and a `tsvector` column (language-aware config)
- `Retriever`: vector search, lexical search, and hybrid via reciprocal rank fusion
- Optional `Reranker` (e.g. `bge-reranker-v2-m3`) behind a flag
- `index_version` recorded for each build
- CLI: `uv run regulens search "question" --k 5`

Done when: retrieval works in FR and EN from the CLI; ADRs for chunking and embedding choice.

## M3: Eval harness

Build:
- Golden set schema (Pydantic) and validator for `evals/golden_set.jsonl`
  (see `evals/golden_set.example.jsonl`)
- Retrieval metrics without LLM: recall@k, MRR, split by language and category
- Runner writing `evals/results/<date>_<gitsha>.json` and a markdown summary
- Threshold check against `evals/thresholds.yaml`, non-zero exit on failure
- Config sweep: compare chunking × hybrid × reranker, output a comparison table

OWNER TASK (not Claude): write 80–120 questions by hand. 25% French, 20% out of scope,
10% traps (outdated versions, neighbouring sections).

Done when: `make eval-smoke` runs on 20 questions; comparison table in README.

## M4: Generation with citations and refusal

Build:
- Prompt files in `src/regulens/prompts/` with an explicit version id
- Structured output: `Answer{answer, citations[], confidence, refused}`
- Citation validation: every citation must map to a retrieved chunk; otherwise flag and refuse
- Refusal when retrieval confidence is low or evidence is missing
- JSON logging of every call with the four version fields from CLAUDE.md
- LLM evals: faithfulness (LLM-as-judge), citation accuracy, refusal accuracy, latency p95,
  cost per query. Judge calibration against 30 human-labelled answers (owner labels them).

Done when: thresholds in `evals/thresholds.yaml` met, or misses reported with a fix plan.

## M5: API, UI, documentation

Build:
- FastAPI: `POST /ask`, `GET /health`; request ids; input validation
- Minimal UI (Streamlit or a single HTML page)
- `docs/model_card.md`: intended use, out-of-scope use (no legal advice), limits, FR/EN performance
- README: results table before/after each improvement, how to run, limits
- Dockerfile (multi-stage, non-root)

Done when: a new user can run the demo from the README in under 10 minutes.
