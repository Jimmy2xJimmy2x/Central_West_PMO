"""Google Calendar integration"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pmo import timeblocks

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events']

PROJECT_ROOT = Path(__file__).parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / 'credentials.json'
TOKEN_FILE = PROJECT_ROOT / 'token.json'


def get_credentials():
    """Get valid user credentials from storage or run OAuth flow."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"credentials.json not found at {CREDENTIALS_FILE}\n"
                    "Please download OAuth 2.0 credentials from Google Cloud Console"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_calendar_service():
    """Build and return Calendar API service."""
    creds = get_credentials()
    return build('calendar', 'v3', credentials=creds)


def fetch_events(calendar_id: str, date: str, service=None) -> list[dict]:
    """
    Fetch events from a specific calendar for a given date.

    Args:
        calendar_id: Calendar ID (e.g., 'primary' or email address)
        date: Date in YYYY-MM-DD format
        service: Optional pre-built service

    Returns:
        List of event dictionaries
    """
    if service is None:
        service = get_calendar_service()

    # Parse date and create time bounds for the full day
    target_date = datetime.fromisoformat(date)
    time_min = target_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    time_max = (target_date + timedelta(days=1)).replace(hour=0, minute=0, second=0).isoformat() + 'Z'

    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []


def event_to_timeblock(event: dict, date: str) -> Optional[dict]:
    """
    Convert a Google Calendar event to timeblock parameters.

    Returns dict with timeblock fields or None if event should be skipped.
    """
    # Skip all-day events
    start = event['start'].get('dateTime')
    end = event['end'].get('dateTime')

    if not start or not end:
        return None

    # Parse times
    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))

    # Extract meeting link
    meeting_link = ''
    if 'hangoutLink' in event:
        meeting_link = event['hangoutLink']
    elif 'conferenceData' in event:
        entry_points = event['conferenceData'].get('entryPoints', [])
        for entry in entry_points:
            if entry.get('entryPointType') == 'video':
                meeting_link = entry.get('uri', '')
                break

    # Also check description for meeting links
    if not meeting_link and 'description' in event:
        desc = event['description']
        for prefix in ['https://meet.google.com/', 'https://zoom.us/', 'https://teams.microsoft.com/']:
            if prefix in desc:
                # Extract URL
                start_idx = desc.index(prefix)
                end_idx = desc.find(' ', start_idx)
                if end_idx == -1:
                    end_idx = desc.find('\n', start_idx)
                if end_idx == -1:
                    end_idx = len(desc)
                meeting_link = desc[start_idx:end_idx]
                break

    return {
        'date': date,
        'start_time': start_dt.strftime('%H:%M'),
        'end_time': end_dt.strftime('%H:%M'),
        'label': event.get('summary', 'Untitled Event'),
        'meeting_link': meeting_link,
        'task_id': None
    }


def sync_calendar(calendar_id: str, date: str, calendar_name: str = None) -> dict:
    """
    Sync events from a Google Calendar to time blocks.

    Args:
        calendar_id: Calendar ID
        date: Date in YYYY-MM-DD format
        calendar_name: Optional display name for the calendar

    Returns:
        Dict with sync stats
    """
    service = get_calendar_service()
    events = fetch_events(calendar_id, date, service)

    stats = {
        'calendar': calendar_name or calendar_id,
        'events_found': len(events),
        'blocks_created': 0,
        'blocks_skipped': 0,
        'errors': []
    }

    # Get existing time blocks for this date
    existing_blocks = timeblocks.list_timeblocks(date)
    existing_times = {(b['start_time'], b['end_time'], b['label']) for b in existing_blocks}

    for event in events:
        block_data = event_to_timeblock(event, date)

        if not block_data:
            stats['blocks_skipped'] += 1
            continue

        # Check if block already exists (avoid duplicates)
        block_key = (block_data['start_time'], block_data['end_time'], block_data['label'])
        if block_key in existing_times:
            stats['blocks_skipped'] += 1
            continue

        try:
            timeblocks.create_timeblock(**block_data)
            stats['blocks_created'] += 1
        except Exception as e:
            stats['errors'].append(f"Failed to create block for '{block_data['label']}': {str(e)}")

    return stats


def sync_all_calendars(date: str, calendar_configs: list[dict]) -> list[dict]:
    """
    Sync multiple calendars.

    Args:
        date: Date in YYYY-MM-DD format
        calendar_configs: List of dicts with 'id' and optional 'name' keys

    Returns:
        List of stats dicts, one per calendar
    """
    results = []

    for config in calendar_configs:
        calendar_id = config.get('id')
        calendar_name = config.get('name')

        if not calendar_id:
            continue

        stats = sync_calendar(calendar_id, date, calendar_name)
        results.append(stats)

    return results
