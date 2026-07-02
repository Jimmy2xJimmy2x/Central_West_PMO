#!/usr/bin/env python3
"""Add a time block to the schedule"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import timeblocks


def main():
    parser = argparse.ArgumentParser(description="Add a time block")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date (YYYY-MM-DD)")
    parser.add_argument("--start", required=True, help="Start time (HH:MM)")
    parser.add_argument("--end", required=True, help="End time (HH:MM)")
    parser.add_argument("--task-id", type=int, help="Task ID to assign")
    parser.add_argument("--label", default="", help="Label (if no task)")
    parser.add_argument("--meeting-link", default="", help="Meeting link (Google Meet, Zoom, etc.)")

    args = parser.parse_args()

    block = timeblocks.create_timeblock(
        date=args.date,
        start_time=args.start,
        end_time=args.end,
        task_id=args.task_id,
        label=args.label,
        meeting_link=args.meeting_link
    )

    print(f"✓ Time block created: {block['start_time']}-{block['end_time']}")
    if block['task_id']:
        print(f"  Assigned to task #{block['task_id']}")
    elif block['label']:
        print(f"  Label: {block['label']}")
    if block['meeting_link']:
        print(f"  Meeting: {block['meeting_link']}")


if __name__ == "__main__":
    main()
