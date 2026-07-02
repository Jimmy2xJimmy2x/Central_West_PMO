#!/usr/bin/env python3
"""Add meeting_link column to time_blocks table"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo.db import get_connection

if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()

    # Check if column already exists
    cursor.execute("PRAGMA table_info(time_blocks)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'meeting_link' not in columns:
        print("Adding meeting_link column to time_blocks...")
        cursor.execute("ALTER TABLE time_blocks ADD COLUMN meeting_link TEXT DEFAULT ''")
        conn.commit()
        print("✓ Column added successfully")
    else:
        print("✓ meeting_link column already exists")

    conn.close()
