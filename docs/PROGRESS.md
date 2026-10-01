# Progress

| Milestone | Status | Notes |
|---|---|---|
| M0 Scaffold | done | pyproject.toml, config, Makefile, docker-compose, CI, tests, architecture.md |
| M1 Ingestion | done | manifest, downloader, extractor, lang, normalizer, db, migrations, ingest orchestrator, 17 tests, 2 ADRs |
| M2 Retrieval | not started | |
| M3 Eval harness | not started | |
| M4 Generation | not started | |
| M5 API/UI/docs | not started | |

## Open questions

- End-to-end ingestion with real PDFs + Postgres not yet run (Docker was not available). Should be tested before M2.
- `sha256` column in manifest.csv is empty — will be filled on first real download.
- FINTRAC and Loi 25 URLs may need adjustment (one is HTML not PDF, one has a typo).

## Decisions log
See `docs/adr/`.
