#!/usr/bin/env python3
"""Manage task notes"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import notes


def main():
    parser = argparse.ArgumentParser(description="Manage task notes")
    parser.add_argument("--task-id", type=int, required=True, help="Task ID")
    parser.add_argument("--list", action="store_true", help="List notes")
    parser.add_argument("--add", help="Add a text note")
    parser.add_argument("--add-link", help="Add a link/URL")
    parser.add_argument("--add-context", help="Add context note")

    args = parser.parse_args()

    if args.list:
        task_notes = notes.list_notes(args.task_id)
        if not task_notes:
            print(f"No notes for task #{args.task_id}")
            return

        print(f"\nNotes for task #{args.task_id}:")
        print("=" * 60)
        for note in task_notes:
            note_type_label = {
                'text': '📝',
                'link': '🔗',
                'context': '💡'
            }.get(note['note_type'], ' ')

            timestamp = note['created_at'][:16]  # Just date and time
            print(f"\n{note_type_label} [{timestamp}]")
            print(f"  {note['content']}")

    elif args.add:
        note = notes.add_note(args.task_id, args.add, note_type='text')
        print(f"✓ Note added to task #{args.task_id}")

    elif args.add_link:
        note = notes.add_note(args.task_id, args.add_link, note_type='link')
        print(f"✓ Link added to task #{args.task_id}")

    elif args.add_context:
        note = notes.add_note(args.task_id, args.add_context, note_type='context')
        print(f"✓ Context added to task #{args.task_id}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
