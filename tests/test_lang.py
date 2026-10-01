"""Tests for language detection."""

from regulens.lang import detect_language


def test_detect_english() -> None:
    text = (
        "This guideline sets out expectations for federally regulated "
        "financial institutions regarding model risk management."
    )
    assert detect_language(text) == "en"


def test_detect_french() -> None:
    text = (
        "La presente ligne directrice enonce les attentes du BSIF a l'egard "
        "de la gestion du risque lie aux modeles pour les institutions financieres."
    )
    assert detect_language(text) == "fr"


def test_short_text_defaults_to_english() -> None:
    assert detect_language("hi") == "en"
