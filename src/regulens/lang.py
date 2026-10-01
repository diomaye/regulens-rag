"""Language detection for documents."""

from __future__ import annotations

from langdetect import DetectorFactory, detect  # type: ignore[import-untyped]

# Make langdetect deterministic
DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """Detect whether *text* is French or English.

    Returns ``"fr"`` or ``"en"``.  Falls back to ``"en"`` for
    very short or ambiguous text.
    """
    if len(text.strip()) < 20:
        return "en"
    try:
        lang = detect(text)
    except Exception:  # noqa: BLE001 — langdetect raises LangDetectException
        return "en"
    if lang.startswith("fr"):
        return "fr"
    return "en"
