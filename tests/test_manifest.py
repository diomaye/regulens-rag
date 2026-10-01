"""Tests for manifest loading and validation."""

from pathlib import Path

import pytest

from regulens.manifest import ManifestRow, load_manifest


@pytest.fixture()
def valid_manifest(tmp_path: Path) -> Path:
    p = tmp_path / "manifest.csv"
    p.write_text(
        "doc_id,title,issuer,language,version_date,url,sha256\n"
        "osfi-e23,E-23 Model Risk,OSFI,en,2024-01-01,"
        "https://example.com/e23.pdf,abc123\n"
    )
    return p


@pytest.fixture()
def bad_lang_manifest(tmp_path: Path) -> Path:
    p = tmp_path / "manifest.csv"
    p.write_text(
        "doc_id,title,issuer,language,version_date,url,sha256\n"
        "x,Title,Issuer,de,2024-01-01,https://example.com/x.pdf,abc\n"
    )
    return p


def test_load_valid(valid_manifest: Path) -> None:
    rows = load_manifest(valid_manifest)
    assert len(rows) == 1
    assert rows[0].doc_id == "osfi-e23"
    assert rows[0].language == "en"


def test_load_bad_language(bad_lang_manifest: Path) -> None:
    with pytest.raises(ValueError, match="language must be"):
        load_manifest(bad_lang_manifest)


def test_load_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_manifest(tmp_path / "nope.csv")


def test_manifest_row_normalizes_language() -> None:
    row = ManifestRow(
        doc_id="x",
        title="T",
        issuer="I",
        language="FR",
        version_date="2024-01-01",
        url="https://example.com",
        sha256="abc",
    )
    assert row.language == "fr"
