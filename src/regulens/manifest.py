"""Load and validate data/manifest.csv."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING

from pydantic import BaseModel, field_validator

if TYPE_CHECKING:
    from pathlib import Path


class ManifestRow(BaseModel):
    """One row of the document manifest."""

    doc_id: str
    title: str
    issuer: str
    language: str
    version_date: str
    url: str
    sha256: str

    @field_validator("language")
    @classmethod
    def _check_language(cls, v: str) -> str:
        if v.lower() not in {"en", "fr"}:
            msg = f"language must be 'en' or 'fr', got '{v}'"
            raise ValueError(msg)
        return v.lower()

    @field_validator("doc_id")
    @classmethod
    def _check_doc_id(cls, v: str) -> str:
        if not v.strip():
            msg = "doc_id must not be empty"
            raise ValueError(msg)
        return v.strip()


def load_manifest(path: Path) -> list[ManifestRow]:
    """Read and validate the manifest CSV.

    Raises ValueError on schema violations.
    """
    if not path.exists():
        msg = f"Manifest file not found: {path}"
        raise FileNotFoundError(msg)

    rows: list[ManifestRow] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected = {"doc_id", "title", "issuer", "language", "version_date", "url", "sha256"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            msg = f"Manifest columns must be {sorted(expected)}, got {reader.fieldnames}"
            raise ValueError(msg)

        for i, raw in enumerate(reader, start=2):
            try:
                rows.append(ManifestRow(**raw))
            except Exception as exc:
                msg = f"Manifest row {i}: {exc}"
                raise ValueError(msg) from exc

    return rows
