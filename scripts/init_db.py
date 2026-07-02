#!/usr/bin/env python3
"""Initialize the PMO database"""

import sys
from pathlib import Path

# Add parent directory to path so we can import pmo
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo.db import init_db, get_db_path

if __name__ == "__main__":
    db_path = get_db_path()

    # Create data directory if it doesn't exist
    db_path.parent.mkdir(exist_ok=True)

    print(f"Initializing database at: {db_path}")
    init_db()
    print("✓ Database initialized successfully")
