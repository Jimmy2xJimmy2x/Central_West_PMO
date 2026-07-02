#!/usr/bin/env python3
"""View tasks and schedule for a specific day"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import tasks, timeblocks, recurring


def format_time_range(start, end):
    """Format time range for display"""
    return f"{start}-{end}"


def main():
    parser = argparse.ArgumentParser(description="View day tasks and schedule")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date (YYYY-MM-DD)")

    args = parser.parse_args()

    # Generate recurring tasks for this date
    recurring.generate_for_date(args.date)

    # Get all tasks
    all_tasks = tasks.list_tasks(args.date)
    blocks = timeblocks.list_timeblocks(args.date)

    # Parse date for display
    try:
        date_obj = datetime.fromisoformat(args.date)
        day_name = date_obj.strftime("%A, %B %d, %Y")
    except ValueError:
        day_name = args.date

    print(f"\n{'='*60}")
    print(f"{day_name}")
    print(f"{'='*60}\n")

    # Display schedule
    if blocks:
        print("SCHEDULE:")
        task_map = {t['id']: t for t in all_tasks}
        scheduled_task_ids = set()

        for block in blocks:
            time_range = format_time_range(block['start_time'], block['end_time'])
            if block['task_id']:
                task = task_map.get(block['task_id'])
                if task:
                    status_icon = "✓" if task['status'] == 'done' else " "
                    priority_label = f"[{task['priority'][:3].upper()}]"
                    print(f"  {time_range:15} [{status_icon}] {priority_label} {task['title']}")
                    scheduled_task_ids.add(block['task_id'])
            else:
                print(f"  {time_range:15} {block['label']}")
        print()

    # Display tasks grouped by priority
    print(f"TASKS ({len(all_tasks)} total):")

    # Group by priority
    by_priority = defaultdict(list)
    for task in all_tasks:
        by_priority[task['priority']].append(task)

    # Display in order: high, medium, low
    for priority in ['high', 'medium', 'low']:
        if priority in by_priority:
            for task in by_priority[priority]:
                status_icon = "✓" if task['status'] == 'done' else " "
                recurring_icon = "↻" if task['recurring_id'] else " "
                print(f"  [{status_icon}] [{priority[:3].upper()}] {recurring_icon} {task['title']}")
                if task['description']:
                    print(f"      → {task['description']}")

    # Show unscheduled tasks
    if blocks:
        unscheduled = [t for t in all_tasks if t['id'] not in scheduled_task_ids]
        if unscheduled:
            print(f"\nUNSCHEDULED ({len(unscheduled)}):")
            for task in unscheduled:
                status_icon = "✓" if task['status'] == 'done' else " "
                print(f"  [{status_icon}] [{task['priority'][:3].upper()}] {task['title']}")

    # Stats
    done_count = sum(1 for t in all_tasks if t['status'] == 'done')
    print(f"\nCompleted: {done_count}/{len(all_tasks)}")
    print()


if __name__ == "__main__":
    main()
