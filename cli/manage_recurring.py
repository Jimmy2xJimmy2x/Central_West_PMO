#!/usr/bin/env python3
"""Manage recurring task templates"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import recurring


def list_recurring():
    """List all recurring tasks"""
    templates = recurring.list_recurring()

    if not templates:
        print("No recurring tasks configured.")
        return

    print(f"\nRecurring Tasks ({len(templates)}):")
    print("=" * 60)

    for tmpl in templates:
        print(f"\n#{tmpl['id']}: {tmpl['title']} [{tmpl['priority'][:3].upper()}]")
        if tmpl['description']:
            print(f"  Description: {tmpl['description']}")

        schedule_type = tmpl['schedule_type']
        print(f"  Schedule: {schedule_type}", end="")

        if tmpl['schedule_days']:
            import json
            days = json.loads(tmpl['schedule_days'])
            if schedule_type == 'weekly':
                day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                day_labels = [day_names[d-1] for d in days if 1 <= d <= 7]
                print(f" ({', '.join(day_labels)})")
            elif schedule_type == 'custom':
                print(f" ({len(days)} dates)")
        else:
            print()


def add_recurring(args):
    """Add a new recurring task"""
    schedule_days = None

    if args.schedule == 'weekly':
        if not args.days:
            print("Error: --days required for weekly schedule (1-7, comma-separated)")
            sys.exit(1)
        schedule_days = [int(d.strip()) for d in args.days.split(',')]
    elif args.schedule == 'custom':
        if not args.days:
            print("Error: --days required for custom schedule (YYYY-MM-DD dates, comma-separated)")
            sys.exit(1)
        schedule_days = [d.strip() for d in args.days.split(',')]

    tmpl = recurring.create_recurring(
        title=args.title,
        schedule_type=args.schedule,
        schedule_days=schedule_days,
        priority=args.priority,
        description=args.description
    )

    print(f"✓ Recurring task #{tmpl['id']} created: {tmpl['title']}")
    print(f"  Schedule: {tmpl['schedule_type']}")
    print(f"  Priority: {tmpl['priority']}")


def remove_recurring(args):
    """Remove a recurring task"""
    if recurring.delete_recurring(args.id):
        print(f"✓ Recurring task #{args.id} deleted")
    else:
        print(f"Error: Recurring task #{args.id} not found")


def main():
    parser = argparse.ArgumentParser(description="Manage recurring tasks")
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # List command
    subparsers.add_parser('list', help='List recurring tasks')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add recurring task')
    add_parser.add_argument('--title', required=True, help='Task title')
    add_parser.add_argument('--schedule', required=True, choices=['daily', 'weekly', 'custom'],
                           help='Schedule type')
    add_parser.add_argument('--days', help='Days (weekly: 1-7 comma-separated, custom: YYYY-MM-DD dates)')
    add_parser.add_argument('--priority', default='medium', choices=['high', 'medium', 'low'])
    add_parser.add_argument('--description', default='', help='Description')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove recurring task')
    remove_parser.add_argument('--id', type=int, required=True, help='Recurring task ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'list':
        list_recurring()
    elif args.command == 'add':
        add_recurring(args)
    elif args.command == 'remove':
        remove_recurring(args)


if __name__ == "__main__":
    main()
