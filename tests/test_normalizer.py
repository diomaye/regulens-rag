"""Tests for text normalization."""

from regulens.normalizer import normalize


def test_rejoin_hyphenated_words() -> None:
    assert normalize("regu-\nlation") == "regulation"


def test_collapse_blank_lines() -> None:
    result = normalize("a\n\n\n\nb")
    assert result == "a\n\nb"


def test_strip_trailing_whitespace() -> None:
    result = normalize("hello   \nworld  ")
    assert "   " not in result


def test_remove_page_numbers() -> None:
    result = normalize("Some text\n42\nMore text")
    assert result == "Some text\n\nMore text"
