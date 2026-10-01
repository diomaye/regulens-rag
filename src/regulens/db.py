"""Database connection and migration helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import psycopg

if TYPE_CHECKING:
    from regulens.config import Settings

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def get_connection(settings: Settings) -> psycopg.Connection[tuple[object, ...]]:
    """Open a synchronous psycopg3 connection."""
    return psycopg.connect(settings.database_url)


def run_migrations(conn: psycopg.Connection[object]) -> None:
    """Execute all SQL migration files in order."""
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for mf in migration_files:
        logger.info("Running migration: %s", mf.name)
        sql = mf.read_text(encoding="utf-8")
        conn.execute(sql)
    conn.commit()
    logger.info("All migrations applied (%d files)", len(migration_files))
