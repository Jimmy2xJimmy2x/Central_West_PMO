"""Time block CRUD operations"""

from typing import Optional
from .db import get_connection, row_to_dict, rows_to_dicts


def list_timeblocks(date: str) -> list[dict]:
    """List all time blocks for a specific date"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM time_blocks WHERE date = ? ORDER BY start_time",
        (date,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows_to_dicts(rows)


def create_timeblock(
    date: str,
    start_time: str,
    end_time: str,
    task_id: Optional[int] = None,
    label: str = "",
    meeting_link: str = ""
) -> dict:
    """Create a new time block"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO time_blocks (date, start_time, end_time, task_id, label, meeting_link)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (date, start_time, end_time, task_id, label, meeting_link)
    )

    block_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM time_blocks WHERE id = ?", (block_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def update_timeblock(block_id: int, **fields) -> Optional[dict]:
    """Update time block fields"""
    if not fields:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM time_blocks WHERE id = ?", (block_id,))
        row = cursor.fetchone()
        conn.close()
        return row_to_dict(row)

    allowed_fields = {'start_time', 'end_time', 'task_id', 'label', 'meeting_link'}
    updates = {k: v for k, v in fields.items() if k in allowed_fields}

    if not updates:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM time_blocks WHERE id = ?", (block_id,))
        row = cursor.fetchone()
        conn.close()
        return row_to_dict(row)

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [block_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE time_blocks SET {set_clause} WHERE id = ?", values)
    conn.commit()

    cursor.execute("SELECT * FROM time_blocks WHERE id = ?", (block_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def delete_timeblock(block_id: int) -> bool:
    """Delete a time block"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time_blocks WHERE id = ?", (block_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
