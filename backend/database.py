import sqlite3
from contextlib import contextmanager

from .config import DB_PATH


def initialize_database() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                department TEXT NOT NULL,
                location TEXT NOT NULL,
                employment_type TEXT NOT NULL,
                description TEXT NOT NULL,
                requirements TEXT NOT NULL DEFAULT '[]',
                status TEXT NOT NULL DEFAULT 'published',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS applications (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                resume_path TEXT NOT NULL,
                score REAL,
                rationale TEXT,
                strengths TEXT NOT NULL DEFAULT '[]',
                gaps TEXT NOT NULL DEFAULT '[]',
                consent INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS jobs_status_created_idx ON jobs(status, created_at);
            CREATE INDEX IF NOT EXISTS applications_job_score_idx ON applications(job_id, score DESC);
            """
        )


@contextmanager
def connect():
    connection = sqlite3.connect(DB_PATH, timeout=15)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def row_dict(row: sqlite3.Row) -> dict:
    return dict(row)
