"""Tests for application configuration."""

import pytest

from regulens.config import Settings


def test_settings_defaults() -> None:
    """Settings can be instantiated with defaults (no .env needed)."""
    s = Settings()
    assert s.llm_model == "claude-sonnet-5-5"
    assert s.embedding_model == "BAAI/bge-m3"
    assert s.log_level == "INFO"
    assert "regulens" in s.database_url


def test_settings_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables override defaults."""
    monkeypatch.setenv("LLM_MODEL", "claude-haiku-4-5-20251001")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    s = Settings()
    assert s.llm_model == "claude-haiku-4-5-20251001"
    assert s.log_level == "DEBUG"
