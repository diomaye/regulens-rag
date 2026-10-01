CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    doc_id       TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    issuer       TEXT NOT NULL,
    language     TEXT NOT NULL CHECK (language IN ('en', 'fr')),
    version_date TEXT NOT NULL,
    sha256       TEXT NOT NULL,
    num_pages    INTEGER NOT NULL,
    detected_language TEXT NOT NULL,
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sections (
    id          SERIAL PRIMARY KEY,
    doc_id      TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    level       INTEGER NOT NULL,
    page_start  INTEGER NOT NULL,
    page_end    INTEGER NOT NULL,
    body        TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sections_doc_id ON sections(doc_id);

CREATE TABLE IF NOT EXISTS corpus_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
