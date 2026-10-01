"""Ingestion orchestrator: manifest -> download -> extract -> store."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from regulens.downloader import download_document, sha256_file
from regulens.extractor import detect_sections, extract_pages
from regulens.lang import detect_language
from regulens.manifest import load_manifest
from regulens.models import Document, Section
from regulens.normalizer import normalize

if TYPE_CHECKING:
    import psycopg

    from regulens.config import Settings
    from regulens.manifest import ManifestRow

logger = logging.getLogger(__name__)


@dataclass
class IngestReport:
    """Summary report for one ingested document."""

    doc_id: str
    title: str
    num_pages: int
    num_sections: int
    detected_language: str
    sha256: str


def process_document(row: ManifestRow, pdf_path: Path) -> Document:
    """Extract, detect language, normalize, and build a Document from a downloaded PDF."""
    pages = extract_pages(pdf_path)
    raw_sections = detect_sections(pages)

    # Detect language from concatenated text
    all_text = "\n".join(p.text for p in pages)
    detected_lang = detect_language(all_text)

    # Normalize section bodies
    sections = [
        Section(
            doc_id=row.doc_id,
            title=s.title,
            level=s.level,
            page_start=s.page_start,
            page_end=s.page_end,
            body=normalize(s.body),
        )
        for s in raw_sections
    ]

    file_hash = sha256_file(pdf_path)

    return Document(
        doc_id=row.doc_id,
        title=row.title,
        issuer=row.issuer,
        language=row.language,
        version_date=row.version_date,
        sha256=file_hash,
        num_pages=len(pages),
        detected_language=detected_lang,
        sections=sections,
    )


def store_document(conn: psycopg.Connection[object], doc: Document) -> None:
    """Insert or replace a document and its sections in the database."""
    conn.execute(
        "DELETE FROM documents WHERE doc_id = %s",
        (doc.doc_id,),
    )
    conn.execute(
        """INSERT INTO documents
           (doc_id, title, issuer, language, version_date, sha256, num_pages, detected_language)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            doc.doc_id,
            doc.title,
            doc.issuer,
            doc.language,
            doc.version_date,
            doc.sha256,
            doc.num_pages,
            doc.detected_language,
        ),
    )
    for s in doc.sections:
        conn.execute(
            """INSERT INTO sections (doc_id, title, level, page_start, page_end, body)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (s.doc_id, s.title, s.level, s.page_start, s.page_end, s.body),
        )
    conn.commit()


def compute_corpus_hash(docs: list[Document]) -> str:
    """Deterministic hash of all document hashes (sorted by doc_id)."""
    combined = "".join(d.sha256 for d in sorted(docs, key=lambda d: d.doc_id))
    return hashlib.sha256(combined.encode()).hexdigest()


def run_ingest(settings: Settings, conn: psycopg.Connection[object]) -> list[IngestReport]:
    """Full ingestion pipeline.

    Returns a per-document report.
    """
    data_dir = Path(settings.data_dir)
    manifest_path = data_dir / "manifest.csv"
    raw_dir = data_dir / "raw"

    rows = load_manifest(manifest_path)
    if not rows:
        logger.warning("Manifest is empty — nothing to ingest")
        return []

    reports: list[IngestReport] = []
    docs: list[Document] = []

    for row in rows:
        pdf_path = download_document(row, raw_dir)
        doc = process_document(row, pdf_path)
        store_document(conn, doc)
        docs.append(doc)

        report = IngestReport(
            doc_id=doc.doc_id,
            title=doc.title,
            num_pages=doc.num_pages,
            num_sections=len(doc.sections),
            detected_language=doc.detected_language,
            sha256=doc.sha256,
        )
        reports.append(report)
        logger.info(
            "Ingested %s: %d pages, %d sections, lang=%s",
            doc.doc_id,
            doc.num_pages,
            len(doc.sections),
            doc.detected_language,
        )

    # Store corpus hash
    corpus_hash = compute_corpus_hash(docs)
    conn.execute(
        """INSERT INTO corpus_meta (key, value) VALUES ('corpus_hash', %s)
           ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value""",
        (corpus_hash,),
    )
    conn.commit()
    logger.info("Corpus hash: %s", corpus_hash[:16])

    return reports
