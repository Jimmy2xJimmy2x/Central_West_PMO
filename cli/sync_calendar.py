#!/usr/bin/env python3
"""Sync Google Calendar events to time blocks"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.google_calendar import sync_all_calendars

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / 'config.json'


def load_config():
    """Load calendar configuration"""
    if not CONFIG_FILE.exists():
        print(f"⚠️  No config.json found. Copy config.example.json to config.json and configure your calendars.")
        return None

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Sync Google Calendar")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"),
                       help="Date to sync (YYYY-MM-DD, default: today)")

    args = parser.parse_args()

    config = load_config()
    if not config:
        return 1

    gcal_config = config.get('google_calendar', {})

    if not gcal_config.get('enabled'):
        print("Google Calendar sync is disabled in config.json")
        return 1

    calendars = gcal_config.get('calendars', [])
    if not calendars:
        print("No calendars configured in config.json")
        return 1

    print(f"\n🔄 Syncing Google Calendar for {args.date}...\n")

    try:
        results = sync_all_calendars(args.date, calendars)

        total_created = 0
        total_skipped = 0
        total_events = 0

        for result in results:
            print(f"📅 {result['calendar']}")
            print(f"   Events found: {result['events_found']}")
            print(f"   Blocks created: {result['blocks_created']}")
            print(f"   Blocks skipped: {result['blocks_skipped']}")

            if result['errors']:
                print(f"   ⚠️  Errors:")
                for error in result['errors']:
                    print(f"      {error}")

            total_created += result['blocks_created']
            total_skipped += result['blocks_skipped']
            total_events += result['events_found']
            print()

        print(f"✓ Sync complete!")
        print(f"  Total events: {total_events}")
        print(f"  Blocks created: {total_created}")
        print(f"  Blocks skipped: {total_skipped} (duplicates or all-day events)\n")

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ {str(e)}\n")
        print("To set up Google Calendar integration:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create a new project (or select existing)")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download credentials.json and place in project root")
        print("6. Run this script again to authenticate\n")
        return 1

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
