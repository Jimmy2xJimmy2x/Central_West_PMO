#!/usr/bin/env python3
"""Add a task to the daily task list"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import tasks


def main():
    parser = argparse.ArgumentParser(description="Add a new task")
    parser.add_argument("--title", required=True, help="Task title")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date (YYYY-MM-DD)")
    parser.add_argument("--priority", default="medium", choices=["high", "medium", "low"], help="Priority level")
    parser.add_argument("--description", default="", help="Task description")

    args = parser.parse_args()

    task = tasks.create_task(
        title=args.title,
        date=args.date,
        priority=args.priority,
        description=args.description
    )

    print(f"✓ Task #{task['id']} created: {task['title']}")
    print(f"  Priority: {task['priority']}")
    print(f"  Date: {task['date']}")
    if task['description']:
        print(f"  Description: {task['description']}")


if __name__ == "__main__":
    main()
