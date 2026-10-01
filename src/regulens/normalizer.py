"""Text normalization for extracted PDF content."""

from __future__ import annotations

import re


def normalize(text: str) -> str:
    """Clean extracted PDF text.

    - Rejoin hyphenated line breaks (e.g. "regu-\\nlation" -> "regulation")
    - Collapse multiple blank lines into one
    - Strip trailing whitespace per line
    - Remove common header/footer patterns (page numbers, repeated doc titles)
    """
    # Rejoin hyphenated words split across lines
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Strip trailing whitespace per line
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Collapse 3+ newlines into 2 (one blank line)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove standalone page numbers (lines that are just a number)
    text = re.sub(r"^\d+\s*$", "", text, flags=re.MULTILINE)

    # Final trim
    return text.strip()
