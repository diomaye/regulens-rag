"""Domain models for ingested documents and sections."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Section:
    """A detected section within a document."""

    doc_id: str
    title: str
    level: int
    page_start: int
    page_end: int
    body: str


@dataclass(frozen=True)
class Document:
    """A fully processed document ready for storage."""

    doc_id: str
    title: str
    issuer: str
    language: str
    version_date: str
    sha256: str
    num_pages: int
    detected_language: str
    sections: list[Section] = field(default_factory=list)
