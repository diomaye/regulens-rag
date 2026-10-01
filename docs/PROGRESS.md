# Progress

| Milestone | Status | Notes |
|---|---|---|
| M0 Scaffold | done | pyproject.toml, config, Makefile, docker-compose, CI, tests, architecture.md |
| M1 Ingestion | done | 4 docs ingested (101 pages, 147 sections), corpus hash stored, 17 tests, 2 ADRs |
| M2 Retrieval | not started | |
| M3 Eval harness | not started | |
| M4 Generation | not started | |
| M5 API/UI/docs | not started | |

## Open questions

- 3 manifest entries removed (fintrac, canafe, qc-loi25) due to broken URLs. Can be re-added with correct PDF links.
- Docker port set to 5434 (local Postgres already uses 5432).

## Decisions log
See `docs/adr/`.
