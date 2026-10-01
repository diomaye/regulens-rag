"""Extract text and detect sections from PDFs using PyMuPDF."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pymupdf

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class PageText:
    """Raw extracted text for one page."""

    page_num: int  # 1-based
    text: str


@dataclass(frozen=True)
class RawSection:
    """A section detected in the PDF before normalization."""

    title: str
    level: int
    page_start: int  # 1-based
    page_end: int  # 1-based
    body: str


# Patterns for numbered headings like "1.", "1.2", "1.2.3", "A.", "A.1"
_NUMBERED_HEADING = re.compile(
    r"^(?P<num>(?:[A-Z]|\d+)(?:\.\d+)*)\.\s+(?P<title>.+)$",
    re.MULTILINE,
)

# ALL-CAPS lines that look like headings (at least 3 chars, no lowercase)
_ALLCAPS_HEADING = re.compile(
    r"^(?P<title>[A-Z][A-Z\s\d\-–—:]{2,})$",
    re.MULTILINE,
)


def extract_pages(pdf_path: Path) -> list[PageText]:
    """Extract text from each page of a PDF."""
    pages: list[PageText] = []
    with pymupdf.open(str(pdf_path)) as doc:  # type: ignore[no-untyped-call]
        for i, page in enumerate(doc):
            text = page.get_text("text")
            pages.append(PageText(page_num=i + 1, text=text))
    return pages


def _heading_level(numbering: str) -> int:
    """Infer heading level from numbering depth: '1' -> 1, '1.2' -> 2, '1.2.3' -> 3."""
    return numbering.count(".") + 1


def detect_sections(pages: list[PageText]) -> list[RawSection]:
    """Detect sections from extracted pages using heading patterns.

    Strategy: scan for numbered headings (e.g. "1.2 Capital Requirements") and
    ALL-CAPS headings (e.g. "DEFINITIONS"). Text between headings becomes the body
    of the preceding section. A synthetic "Preamble" section captures text before
    the first heading.
    """
    # Build a flat text with page markers so we can map back to pages
    markers: list[tuple[int, int]] = []  # (char_offset, page_num)
    full_text_parts: list[str] = []
    offset = 0
    for p in pages:
        markers.append((offset, p.page_num))
        full_text_parts.append(p.text)
        offset += len(p.text) + 1  # +1 for the join newline
    full_text = "\n".join(full_text_parts)

    def _page_at(char_pos: int) -> int:
        """Return the 1-based page number for a character position."""
        result = 1
        for m_offset, m_page in markers:
            if m_offset <= char_pos:
                result = m_page
            else:
                break
        return result

    # Collect all heading matches with position
    headings: list[tuple[int, str, int]] = []  # (char_pos, title, level)

    for m in _NUMBERED_HEADING.finditer(full_text):
        num = m.group("num")
        title = f"{num}. {m.group('title').strip()}"
        headings.append((m.start(), title, _heading_level(num)))

    for m in _ALLCAPS_HEADING.finditer(full_text):
        title = m.group("title").strip()
        if len(title) >= 4:  # avoid false positives on short acronyms
            headings.append((m.start(), title, 1))

    headings.sort(key=lambda h: h[0])

    # Build sections
    sections: list[RawSection] = []
    if not headings:
        # No headings found — single section from all text
        if full_text.strip():
            sections.append(
                RawSection(
                    title="Document",
                    level=1,
                    page_start=pages[0].page_num if pages else 1,
                    page_end=pages[-1].page_num if pages else 1,
                    body=full_text.strip(),
                )
            )
        return sections

    # Preamble before first heading
    preamble = full_text[: headings[0][0]].strip()
    if preamble:
        sections.append(
            RawSection(
                title="Preamble",
                level=0,
                page_start=pages[0].page_num if pages else 1,
                page_end=_page_at(headings[0][0]),
                body=preamble,
            )
        )

    for i, (pos, title, level) in enumerate(headings):
        # Body extends from end of this heading line to start of next heading
        line_end = full_text.index("\n", pos) if "\n" in full_text[pos:] else len(full_text)
        next_pos = headings[i + 1][0] if i + 1 < len(headings) else len(full_text)
        body = full_text[line_end:next_pos].strip()

        sections.append(
            RawSection(
                title=title,
                level=level,
                page_start=_page_at(pos),
                page_end=_page_at(next_pos - 1) if next_pos > pos else _page_at(pos),
                body=body,
            )
        )

    return sections
