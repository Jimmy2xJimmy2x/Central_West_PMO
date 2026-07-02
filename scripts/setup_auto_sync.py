#!/usr/bin/env python3
"""Setup automatic morning calendar sync using cron"""

import os
import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / 'config.json'


def get_sync_time():
    """Get configured sync time from config.json"""
    if not CONFIG_FILE.exists():
        return "07:00"  # Default

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    return config.get('google_calendar', {}).get('auto_sync_time', '07:00')


def setup_cron():
    """Add cron job for morning sync"""
    sync_time = get_sync_time()
    hour, minute = sync_time.split(':')

    # Paths
    python_path = PROJECT_ROOT / 'venv' / 'bin' / 'python3'
    script_path = PROJECT_ROOT / 'cli' / 'sync_calendar.py'

    # Cron command
    cron_cmd = f'{minute} {hour} * * * cd {PROJECT_ROOT} && {python_path} {script_path} >> {PROJECT_ROOT}/logs/calendar_sync.log 2>&1'

    print(f"\n📅 Setting up automatic calendar sync at {sync_time} daily\n")
    print("Add this line to your crontab:")
    print(f"\n  {cron_cmd}\n")
    print("To edit crontab, run: crontab -e\n")

    # Create logs directory
    logs_dir = PROJECT_ROOT / 'logs'
    logs_dir.mkdir(exist_ok=True)

    response = input("Would you like me to add this to your crontab automatically? (y/N): ")

    if response.lower() == 'y':
        try:
            # Get current crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ""

            # Check if already exists
            if 'sync_calendar.py' in current_cron:
                print("⚠️  Calendar sync cron job already exists")
                return

            # Add new job
            new_cron = current_cron + cron_cmd + '\n'

            # Write back
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
            process.communicate(new_cron)

            print(f"✓ Cron job added successfully!")
            print(f"  Sync will run daily at {sync_time}")
            print(f"  Logs: {PROJECT_ROOT}/logs/calendar_sync.log\n")

        except Exception as e:
            print(f"❌ Error setting up cron: {e}")
            print("Please add manually using: crontab -e\n")
    else:
        print("Manual setup - copy the command above and add to crontab with: crontab -e\n")


if __name__ == "__main__":
    setup_cron()
