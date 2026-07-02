## Google Calendar Integration Setup

This guide walks you through setting up Google Calendar sync for the Central West PMO Management Assistant.

### Features

- ✅ **One-way sync** from Google Calendar to PMO app
- ✅ **Multiple calendars** - sync personal + group calendars
- ✅ **Auto-sync** every morning at configurable time (default 7:00 AM)
- ✅ **On-demand sync** via `/sync-calendar` command
- ✅ **Smart duplicate detection** - won't create duplicate time blocks
- ✅ **Meeting link extraction** - auto-detects Google Meet, Zoom, Teams links
- ✅ **All-day event filtering** - only syncs timed events

---

## Step 1: Get Google Calendar API Credentials

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Name it "Central West PMO" (or similar)
4. Click "Create"

### 1.2 Enable Google Calendar API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 1.3 Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: **Internal** (if using Google Workspace) or **External**
   - App name: "Central West PMO"
   - User support email: your email
   - Scopes: Add `../auth/calendar.readonly` and `../auth/calendar.events`
   - Test users: Add your email (if External)
4. Application type: **Desktop app**
5. Name: "PMO Desktop Client"
6. Click "Create"

### 1.4 Download Credentials

1. Click the download icon next to your new OAuth client
2. Save the file as `credentials.json`
3. Move it to your project root:
   ```bash
   mv ~/Downloads/credentials.json /Users/jpezzone/Central_West_PMO/
   ```

---

## Step 2: Configure Your Calendars

### 2.1 Create config.json

```bash
cd /Users/jpezzone/Central_West_PMO
cp config.example.json config.json
```

### 2.2 Find Your Calendar IDs

**Personal calendar:**
- ID is usually just `"primary"`

**Group/shared calendars:**
1. Open [Google Calendar](https://calendar.google.com)
2. Find the calendar in the left sidebar
3. Click the three dots → "Settings and sharing"
4. Scroll down to "Integrate calendar"
5. Copy the "Calendar ID" (looks like `team@example.com` or `abc123@group.calendar.google.com`)

### 2.3 Edit config.json

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
        "id": "your-team-calendar@group.calendar.google.com",
        "name": "Team Calendar",
        "read_only": true
      }
    ]
  }
}
```

**Notes:**
- `auto_sync_time`: When to run automatic sync (24-hour format, e.g., "07:00" = 7 AM)
- `read_only`: Set to `false` for personal calendar (future: can write back), `true` for group calendars

---

## Step 3: First Sync (OAuth Authorization)

Run the sync command for the first time:

```bash
source venv/bin/activate
python3 cli/sync_calendar.py
```

**What happens:**
1. Your browser will open
2. Google will ask you to sign in (if not already)
3. Grant permissions to the app
4. Browser will show "The authentication flow has completed"
5. Close the browser and return to terminal

A `token.json` file will be created - this stores your authorization so you don't need to authenticate again.

**Output example:**
```
🔄 Syncing Google Calendar for 2026-07-02...

📅 Personal Calendar
   Events found: 5
   Blocks created: 4
   Blocks skipped: 1

📅 Team Calendar
   Events found: 3
   Blocks created: 3
   Blocks skipped: 0

✓ Sync complete!
  Total events: 8
  Blocks created: 7
  Blocks skipped: 1 (duplicates or all-day events)
```

---

## Step 4: Setup Automatic Morning Sync

Run the setup script:

```bash
python3 scripts/setup_auto_sync.py
```

This will:
1. Read your configured sync time from `config.json`
2. Generate a cron job command
3. Optionally add it to your crontab automatically

**Or manually add to crontab:**

```bash
crontab -e
```

Add this line (adjust paths if needed):
```
0 7 * * * cd /Users/jpezzone/Central_West_PMO && /Users/jpezzone/Central_West_PMO/venv/bin/python3 /Users/jpezzone/Central_West_PMO/cli/sync_calendar.py >> /Users/jpezzone/Central_West_PMO/logs/calendar_sync.log 2>&1
```

Save and exit. The sync will now run every morning at 7 AM.

---

## Usage

### Manual Sync (On-Demand)

**Via Claude Code:**
```
/sync-calendar
/sync-calendar tomorrow
/sync-calendar 2026-07-15
```

**Via CLI:**
```bash
source venv/bin/activate
python3 cli/sync_calendar.py --date 2026-07-15
```

### View Synced Appointments

1. Open web GUI: http://localhost:5173
2. Calendar appointments appear in the right column
3. Click meeting links to join

Or use:
```
/view-day
```

---

## Troubleshooting

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Place in project root as `credentials.json`

### "No config.json found"
- Copy `config.example.json` to `config.json`
- Configure your calendar IDs

### "Authentication flow failed"
- Check you're using the correct Google account
- Verify OAuth consent screen is configured
- For External apps, make sure your email is added as a test user

### Duplicate blocks created
- The sync detects duplicates by (start_time, end_time, label)
- If you manually created a time block, sync will skip the matching event

### All-day events not syncing
- By design - only timed events are synced
- All-day events don't have meeting links or specific times

### Cron job not running
- Check crontab: `crontab -l`
- Check logs: `cat logs/calendar_sync.log`
- Verify paths in cron command are absolute

---

## Security Notes

- **credentials.json**: Contains your OAuth client secret - do NOT commit to git (already in .gitignore)
- **token.json**: Contains your access/refresh tokens - do NOT commit to git (already in .gitignore)
- **Read-only calendars**: Group calendars are read-only by default to prevent accidental modifications

---

## What Gets Synced

**Included:**
- ✅ Event title → time block label
- ✅ Start/end time → time block times
- ✅ Google Meet links → meeting_link
- ✅ Zoom/Teams links from description → meeting_link
- ✅ Event date

**Excluded:**
- ❌ All-day events
- ❌ Declined events
- ❌ Canceled events
- ❌ Private events (if calendar permissions don't allow)

---

## Future Enhancements

- Two-way sync for personal calendar (write tasks back to Google Calendar)
- Sync task updates back to calendar events
- Attendee information
- Reminders
- Event colors → priority mapping
