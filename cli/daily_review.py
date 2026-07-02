#!/usr/bin/env python3
"""Daily review - completion stats and task rollover"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import tasks, recurring


def main():
    parser = argparse.ArgumentParser(description="Daily review")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date to review (YYYY-MM-DD)")

    args = parser.parse_args()

    # Get all tasks for the day
    all_tasks = tasks.list_tasks(args.date)

    if not all_tasks:
        print(f"\nNo tasks for {args.date}")
        return

    # Calculate stats
    done = [t for t in all_tasks if t['status'] == 'done']
    incomplete = [t for t in all_tasks if t['status'] != 'done' and t['status'] != 'cancelled']

    try:
        date_obj = datetime.fromisoformat(args.date)
        day_name = date_obj.strftime("%A, %B %d, %Y")
    except ValueError:
        day_name = args.date

    print(f"\n{'='*60}")
    print(f"Daily Review: {day_name}")
    print(f"{'='*60}\n")

    print(f"Total tasks: {len(all_tasks)}")
    print(f"Completed: {len(done)} ({len(done)/len(all_tasks)*100:.0f}%)")
    print(f"Incomplete: {len(incomplete)}")

    if done:
        print(f"\n✓ Completed:")
        for task in done:
            print(f"  • {task['title']}")

    if incomplete:
        print(f"\n⚠ Incomplete:")
        for task in incomplete:
            print(f"  • {task['title']} [{task['priority'][:3].upper()}]")

        print(f"\nOptions for incomplete tasks:")
        print(f"  1. Move to tomorrow")
        print(f"  2. Cancel")
        print(f"  3. Leave on today's list")
        print(f"\nUse task update commands to move or cancel specific tasks")

    # Preview tomorrow
    tomorrow = (datetime.fromisoformat(args.date) + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"\n{'='*60}")
    print(f"Preparing: {tomorrow}")
    print(f"{'='*60}")

    # Generate tomorrow's recurring tasks
    new_recurring = recurring.generate_for_date(tomorrow)
    if new_recurring:
        print(f"\n✓ Generated {len(new_recurring)} recurring task(s):")
        for task in new_recurring:
            print(f"  • {task['title']} [{task['priority'][:3].upper()}]")
    else:
        print("\nNo new recurring tasks for tomorrow")

    print()


if __name__ == "__main__":
    main()
