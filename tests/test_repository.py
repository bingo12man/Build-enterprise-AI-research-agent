import sqlite3


def test_sqlite_research_history_round_trip(
    tmp_path,
):

    database_path = (
        tmp_path
        / "test_history.db"
    )

    connection = sqlite3.connect(
        database_path
    )

    connection.execute(
        """
        CREATE TABLE research_history (
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
            "research-123",
            "How can AI help manufacturing?",
            "AI can improve operations.",
            "High",
            "Strong evidence.",
            "2026-08-26T10:00:00",
        ),
    )

    connection.commit()

    connection.row_factory = (
        sqlite3.Row
    )

    row = connection.execute(
        """
        SELECT *
        FROM research_history
        WHERE research_id = ?
        """,
        (
            "research-123",
        ),
    ).fetchone()

    connection.close()

    assert row is not None

    assert (
        row["research_id"]
        == "research-123"
    )

    assert (
        row["confidence_level"]
        == "High"
    )