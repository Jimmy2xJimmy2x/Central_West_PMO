"""Task CRUD operations"""

from typing import Optional
from .db import get_connection, row_to_dict, rows_to_dicts


def list_tasks(date: str, status: Optional[str] = None) -> list[dict]:
    """List tasks for a specific date, optionally filtered by status"""
    conn = get_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute(
            "SELECT * FROM tasks WHERE date = ? AND status = ? ORDER BY position, priority DESC, created_at",
            (date, status)
        )
    else:
        cursor.execute(
            "SELECT * FROM tasks WHERE date = ? ORDER BY position, priority DESC, created_at",
            (date,)
        )

    rows = cursor.fetchall()
    conn.close()
    return rows_to_dicts(rows)


def get_task(task_id: int) -> Optional[dict]:
    """Get a single task by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def create_task(
    title: str,
    date: str,
    priority: str = "medium",
    description: str = "",
    recurring_id: Optional[int] = None
) -> dict:
    """Create a new task"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, date, priority, description, recurring_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, date, priority, description, recurring_id)
    )

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_task(task_id)


def update_task(task_id: int, **fields) -> Optional[dict]:
    """Update task fields"""
    if not fields:
        return get_task(task_id)

    # Build dynamic SQL for allowed fields
    allowed_fields = {'title', 'description', 'priority', 'status', 'date', 'position'}
    updates = {k: v for k, v in fields.items() if k in allowed_fields}

    if not updates:
        return get_task(task_id)

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    set_clause += ", updated_at = datetime('now')"
    values = list(updates.values()) + [task_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

    return get_task(task_id)


def delete_task(task_id: int) -> bool:
    """Delete a task"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def reorder_tasks(date: str, task_ids: list[int]) -> None:
    """Reorder tasks for a date by setting position based on the list order"""
    conn = get_connection()
    cursor = conn.cursor()

    for position, task_id in enumerate(task_ids):
        cursor.execute(
            "UPDATE tasks SET position = ? WHERE id = ? AND date = ?",
            (position, task_id, date)
        )

    conn.commit()
    conn.close()
