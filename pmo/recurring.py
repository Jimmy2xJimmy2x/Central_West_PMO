"""Recurring task template management and instantiation"""

import json
from datetime import datetime
from typing import Optional
from .db import get_connection, row_to_dict, rows_to_dicts
from . import tasks as tasks_module


def list_recurring() -> list[dict]:
    """List all recurring task templates"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recurring_tasks WHERE active = 1 ORDER BY title")
    rows = cursor.fetchall()
    conn.close()
    return rows_to_dicts(rows)


def create_recurring(
    title: str,
    schedule_type: str,
    schedule_days: Optional[list] = None,
    priority: str = "medium",
    description: str = ""
) -> dict:
    """Create a new recurring task template"""
    conn = get_connection()
    cursor = conn.cursor()

    schedule_days_json = json.dumps(schedule_days) if schedule_days else None

    cursor.execute(
        """
        INSERT INTO recurring_tasks (title, schedule_type, schedule_days, priority, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, schedule_type, schedule_days_json, priority, description)
    )

    recurring_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM recurring_tasks WHERE id = ?", (recurring_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def update_recurring(recurring_id: int, **fields) -> Optional[dict]:
    """Update recurring task template fields"""
    if not fields:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recurring_tasks WHERE id = ?", (recurring_id,))
        row = cursor.fetchone()
        conn.close()
        return row_to_dict(row)

    allowed_fields = {'title', 'description', 'priority', 'schedule_type', 'schedule_days', 'active'}
    updates = {}

    for k, v in fields.items():
        if k in allowed_fields:
            if k == 'schedule_days' and v is not None:
                updates[k] = json.dumps(v)
            else:
                updates[k] = v

    if not updates:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recurring_tasks WHERE id = ?", (recurring_id,))
        row = cursor.fetchone()
        conn.close()
        return row_to_dict(row)

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    set_clause += ", updated_at = datetime('now')"
    values = list(updates.values()) + [recurring_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE recurring_tasks SET {set_clause} WHERE id = ?", values)
    conn.commit()

    cursor.execute("SELECT * FROM recurring_tasks WHERE id = ?", (recurring_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row)


def delete_recurring(recurring_id: int) -> bool:
    """Delete a recurring task template"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recurring_tasks WHERE id = ?", (recurring_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def generate_for_date(date: str) -> list[dict]:
    """
    Generate recurring tasks for a specific date (idempotent).
    Returns newly created tasks.
    """
    # Parse the date to get ISO weekday (1=Monday, 7=Sunday)
    try:
        date_obj = datetime.fromisoformat(date)
        weekday = date_obj.isoweekday()
    except ValueError:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    # Get all active recurring tasks
    cursor.execute("SELECT * FROM recurring_tasks WHERE active = 1")
    recurring_tasks = rows_to_dicts(cursor.fetchall())

    created_tasks = []

    for rec in recurring_tasks:
        # Check if task already exists for this date and recurring template
        cursor.execute(
            "SELECT id FROM tasks WHERE date = ? AND recurring_id = ?",
            (date, rec['id'])
        )
        if cursor.fetchone():
            continue  # Already exists

        # Determine if we should create a task for this date
        should_create = False

        if rec['schedule_type'] == 'daily':
            should_create = True
        elif rec['schedule_type'] == 'weekly':
            if rec['schedule_days']:
                schedule_days = json.loads(rec['schedule_days'])
                if weekday in schedule_days:
                    should_create = True
        elif rec['schedule_type'] == 'custom':
            if rec['schedule_days']:
                schedule_days = json.loads(rec['schedule_days'])
                if date in schedule_days:
                    should_create = True

        if should_create:
            task = tasks_module.create_task(
                title=rec['title'],
                date=date,
                priority=rec['priority'],
                description=rec['description'],
                recurring_id=rec['id']
            )
            created_tasks.append(task)

    conn.close()
    return created_tasks
