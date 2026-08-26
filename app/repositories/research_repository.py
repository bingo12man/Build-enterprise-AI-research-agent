import sqlite3
from datetime import datetime
from typing import List, Optional

from app.config.database import DATABASE_PATH
from app.models.evidence import EvidenceItem

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(
        str(DATABASE_PATH)
    )


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS research_history (
                research_id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                summary TEXT NOT NULL,
                confidence_level TEXT NOT NULL,
                confidence_explanation TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS research_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                research_id TEXT NOT NULL,
                citation_id TEXT NOT NULL,
                source_id TEXT,
                source_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_url TEXT,
                evidence_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def save_research(
    research_id: str,
    query: str,
    summary: str,
    confidence_level: str,
    confidence_explanation: str,
) -> None:

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO research_history (
                research_id,
                query,
                summary,
                confidence_level,
                confidence_explanation,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                research_id,
                query,
                summary,
                confidence_level,
                confidence_explanation,
                datetime.utcnow().isoformat(),
            ),
        )

        connection.commit()

    finally:
        connection.close()

def save_research_sources(
    research_id: str,
    evidence_items: List[EvidenceItem],
) -> None:

    if not evidence_items:
        return

    connection = get_connection()

    try:
        rows = []

        for item in evidence_items:
            rows.append(
                (
                    research_id,
                    item.citation_id,
                    item.source_id,
                    item.source_name,
                    item.source_type,
                    item.source_url,
                    item.content,
                    datetime.utcnow().isoformat(),
                )
            )

        connection.executemany(
            """
            INSERT INTO research_sources (
                research_id,
                citation_id,
                source_id,
                source_name,
                source_type,
                source_url,
                evidence_text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        connection.commit()

    finally:
        connection.close()

def get_research_sources(
    research_id: str,
) -> List[dict]:

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM research_sources
            WHERE research_id = ?
            ORDER BY id ASC
            """,
            (
                research_id,
            ),
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()
        
def get_research_by_id(
    research_id: str,
) -> Optional[dict]:

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM research_history
            WHERE research_id = ?
            """,
            (
                research_id,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def get_recent_research(
    limit: int = 10,
) -> List[dict]:

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM research_history
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (
                limit,
            ),
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()