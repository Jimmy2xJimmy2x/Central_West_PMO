---
description: Sync Google Calendar events to time blocks
argument-hint: [YYYY-MM-DD or "today" or "tomorrow"]
allowed-tools: [Bash]
---

# Sync Google Calendar

Today's date: !`date +%Y-%m-%d`

## Instructions

This command syncs events from your configured Google Calendars into time blocks.

Parse the user's arguments: $ARGUMENTS

If no date specified, sync today. If "tomorrow" is specified, calculate tomorrow's date.

Run the sync command:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/sync_calendar.py --date "<date>"
```

**First-time setup:**

If the user hasn't set up Google Calendar yet, they need to:

1. **Get OAuth credentials:**
   - Go to https://console.cloud.google.com
   - Create a project or select existing
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download as `credentials.json` and place in project root

2. **Configure calendars:**
   - Copy `config.example.json` to `config.json`
   - Edit to add your calendar IDs:
     ```json
     {
       "google_calendar": {
         "enabled": true,
         "auto_sync_time": "07:00",
         "calendars": [
           {
             "id": "primary",
             "name": "Personal Calendar",
             "read_only": false
           },
           {
             "id": "team@example.com",
             "name": "Team Calendar",
             "read_only": true
           }
         ]
       }
     }
     ```

3. **Run sync** - first time will open browser for OAuth consent

Present the sync results to the user, showing:
- How many events were found
- How many time blocks were created
- How many were skipped (duplicates)
- Any errors

Remind the user that auto-sync runs every morning at the configured time (default 7:00 AM).
