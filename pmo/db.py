"""Database connection and schema management"""

import sqlite3
from pathlib import Path
from typing import Optional

# Derive project root from this file's location
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "pmo.db"


def get_db_path() -> Path:
    """Returns the path to the SQLite database file"""
    return DB_PATH


def get_connection() -> sqlite3.Connection:
    """
    Returns a database connection with:
    - Row factory for dict-like access
    - Foreign keys enabled
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Initialize the database schema"""
    conn = get_connection()
    cursor = conn.cursor()

    # Version tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY,
            applied_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Recurring task templates
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority    TEXT CHECK(priority IN ('high', 'medium', 'low')) DEFAULT 'medium',
            schedule_type TEXT CHECK(schedule_type IN ('daily', 'weekly', 'custom')) NOT NULL,
            schedule_days TEXT,
            active      INTEGER DEFAULT 1,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # Tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority    TEXT CHECK(priority IN ('high', 'medium', 'low')) DEFAULT 'medium',
            status      TEXT CHECK(status IN ('pending', 'in_progress', 'done', 'cancelled')) DEFAULT 'pending',
            date        TEXT NOT NULL,
            position    INTEGER DEFAULT 0,
            recurring_id INTEGER REFERENCES recurring_tasks(id) ON DELETE SET NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # Time blocks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS time_blocks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id     INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
            date        TEXT NOT NULL,
            start_time  TEXT NOT NULL,
            end_time    TEXT NOT NULL,
            label       TEXT DEFAULT '',
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # Task notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_notes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id     INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
            content     TEXT NOT NULL,
            note_type   TEXT CHECK(note_type IN ('text', 'link', 'context')) DEFAULT 'text',
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_date ON tasks(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_recurring ON tasks(recurring_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_time_blocks_date ON time_blocks(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_task_notes_task ON task_notes(task_id)")

    # Record schema version
    cursor.execute("INSERT OR IGNORE INTO schema_version (version) VALUES (1)")

    conn.commit()
    conn.close()


def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict]:
    """Convert a sqlite3.Row to a dict"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    """Convert a list of sqlite3.Row to a list of dicts"""
    return [row_to_dict(row) for row in rows]
