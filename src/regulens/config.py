"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration loaded from env / .env file."""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # LLM
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-5-5"
    judge_model: str = "claude-sonnet-5-5"

    # Embeddings
    embedding_model: str = "BAAI/bge-m3"

    # Database
    database_url: str = "postgresql://regulens:regulens@localhost:5432/regulens"

    # Data
    data_dir: str = "data"

    # Logging
    log_level: str = "INFO"


def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
