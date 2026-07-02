"""Task notes CRUD operations"""

from typing import Optional
from .db import get_connection, row_to_dict, rows_to_dicts


def list_notes(task_id: int) -> list[dict]:
    """List all notes for a task"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM task_notes WHERE task_id = ? ORDER BY created_at",
        (task_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows_to_dicts(rows)


def add_note(task_id: int, content: str, note_type: str = "text") -> dict:
    """Add a note to a task"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO task_notes (task_id, content, note_type) VALUES (?, ?, ?)",
        (task_id, content, note_type)
    )

    note_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM task_notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def update_note(note_id: int, content: str) -> Optional[dict]:
    """Update note content"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE task_notes SET content = ? WHERE id = ?",
        (content, note_id)
    )

    conn.commit()

    cursor.execute("SELECT * FROM task_notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def delete_note(note_id: int) -> bool:
    """Delete a note"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task_notes WHERE id = ?", (note_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
