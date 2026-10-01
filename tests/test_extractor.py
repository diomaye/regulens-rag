"""Tests for PDF extraction and section detection."""

from pathlib import Path

from regulens.extractor import detect_sections, extract_pages

FIXTURE = Path(__file__).parent / "fixtures" / "sample.pdf"


def test_extract_pages() -> None:
    pages = extract_pages(FIXTURE)
    assert len(pages) == 2
    assert pages[0].page_num == 1
    assert pages[1].page_num == 2
    assert "Introduction" in pages[0].text
    assert "Definitions" in pages[1].text


def test_detect_sections() -> None:
    pages = extract_pages(FIXTURE)
    sections = detect_sections(pages)
    # Should find at least: SAMPLE GUIDELINE (allcaps), 1. Introduction, 1.1. Scope,
    # 2. Definitions, 3. Expectations
    titles = [s.title for s in sections]
    assert any("Introduction" in t for t in titles)
    assert any("Scope" in t for t in titles)
    assert any("Definitions" in t for t in titles)
    assert any("Expectations" in t for t in titles)


def test_sections_have_bodies() -> None:
    pages = extract_pages(FIXTURE)
    sections = detect_sections(pages)
    for s in sections:
        # Every section with a real heading should have some body text
        if s.title not in {"Preamble", "SAMPLE GUIDELINE"}:
            assert len(s.body) > 0, f"Section '{s.title}' has empty body"


def test_sections_have_valid_pages() -> None:
    pages = extract_pages(FIXTURE)
    sections = detect_sections(pages)
    for s in sections:
        assert 1 <= s.page_start <= 2
        assert 1 <= s.page_end <= 2
        assert s.page_start <= s.page_end
