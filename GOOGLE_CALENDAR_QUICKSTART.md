# Google Calendar Sync - Quick Start

Get your Google Calendar events synced to the PMO app in 5 minutes.

## Quick Setup

### 1. Get OAuth Credentials (5 min)

1. Go to https://console.cloud.google.com
2. Create project → Enable "Google Calendar API"
3. Create OAuth credentials (Desktop app)
4. Download as `credentials.json` → place in project root

**Detailed steps:** See [GOOGLE_CALENDAR_SETUP.md](GOOGLE_CALENDAR_SETUP.md#step-1-get-google-calendar-api-credentials)

### 2. Configure Calendars (2 min)

```bash
cp config.example.json config.json
```

Edit `config.json`:
```json
{
  "google_calendar": {
    "enabled": true,
    "auto_sync_time": "07:00",
    "calendars": [
      {
        "id": "primary",
        "name": "Personal",
        "read_only": false
      },
      {
        "id": "team-calendar@group.calendar.google.com",
        "name": "Team",
        "read_only": true
      }
    ]
  }
}
```

**Find calendar IDs:** Google Calendar → Settings → Integrate calendar → Calendar ID

### 3. First Sync (1 min)

```bash
source venv/bin/activate
python3 cli/sync_calendar.py
```

- Browser opens → Sign in → Grant permissions → Done
- `token.json` created (stores auth, don't commit to git)

### 4. Setup Auto-Sync (30 sec)

```bash
python3 scripts/setup_auto_sync.py
```

Choose "y" to add cron job automatically, or manually add to crontab.

## Usage

**Via Claude Code:**
```
/sync-calendar
/sync-calendar tomorrow
```

**Via CLI:**
```bash
source venv/bin/activate
python3 cli/sync_calendar.py --date 2026-07-15
```

**View synced events:**
- Open http://localhost:5173
- Calendar column shows appointments with meeting links
- Or use `/view-day`

## What Gets Synced

✅ Event title → Time block label  
✅ Start/end times  
✅ Meeting links (Google Meet, Zoom, Teams)  
✅ Event descriptions  
❌ All-day events (skipped)  
❌ Duplicates (detected and skipped)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "credentials.json not found" | Download from Google Cloud Console |
| "No config.json" | Copy from config.example.json |
| Duplicates created | Normal - sync detects by time+title |
| Cron not running | Check: `crontab -l` and `cat logs/calendar_sync.log` |

**Full guide:** [GOOGLE_CALENDAR_SETUP.md](GOOGLE_CALENDAR_SETUP.md)
