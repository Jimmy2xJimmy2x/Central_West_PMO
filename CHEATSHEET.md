# Central West PMO - Quick Reference Guide

## 🚀 Starting the Application

### Start Both Servers (Recommended)
```bash
cd /Users/jpezzone/Central_West_PMO
./scripts/start_dev.sh
```
- Flask API: http://localhost:5000
- React Web GUI: http://localhost:5173

### Start Flask API Only
```bash
cd /Users/jpezzone/Central_West_PMO
source venv/bin/activate
python3 -m api.app
```

### Start React Dev Server Only
```bash
cd /Users/jpezzone/Central_West_PMO/web
npm run dev
```

---

## 💬 Claude Code Slash Commands

Use these in any Claude Code session in `/Users/jpezzone/Central_West_PMO`:

### Task Management
```bash
/add-task Buy groceries --priority high
/add-task Review PR #42 --priority medium --date 2026-07-05
/view-day                    # View today
/view-day tomorrow           # View tomorrow
/view-day 2026-07-10        # View specific date
```

### Time Blocking
```bash
/add-timeblock 09:00-10:30 --task-id 5
/add-timeblock 14:00-15:00 --label "Team meeting"
```

### Recurring Tasks
```bash
/manage-recurring list
/manage-recurring add --title "Daily standup" --schedule daily
/manage-recurring add --title "Planning" --schedule weekly --days 1,3,5
/manage-recurring remove --id 3
```

### Notes & Context
```bash
/task-notes 5 --list                              # List notes for task #5
/task-notes 5 --add "Remember to check with Sarah"
/task-notes 5 --add-link "https://docs.google.com/..."
```

### Daily Review
```bash
/daily-review              # End of day stats + rollover
```

---

## 🖥️ Direct CLI Usage

When you need the raw CLI (no Claude Code):

### Activate Virtual Environment First
```bash
cd /Users/jpezzone/Central_West_PMO
source venv/bin/activate
```

### Add Tasks
```bash
python3 cli/add_task.py --title "Task name" --priority high
python3 cli/add_task.py --title "Future task" --date 2026-07-10 --priority medium
```

### View Day
```bash
python3 cli/view_day.py                # Today
python3 cli/view_day.py --date 2026-07-05
```

### Manage Recurring Tasks
```bash
python3 cli/manage_recurring.py list
python3 cli/manage_recurring.py add --title "Standup" --schedule weekly --days 1,2,3,4,5
python3 cli/manage_recurring.py remove --id 2
```

### Add Time Blocks
```bash
python3 cli/add_timeblock.py --start 09:00 --end 10:30 --task-id 5
python3 cli/add_timeblock.py --start 14:00 --end 15:00 --label "Lunch"
```

### Task Notes
```bash
python3 cli/task_notes.py --task-id 5 --list
python3 cli/task_notes.py --task-id 5 --add "Important context"
python3 cli/task_notes.py --task-id 5 --add-link "https://example.com"
```

### Daily Review
```bash
python3 cli/daily_review.py
python3 cli/daily_review.py --date 2026-07-02
```

---

## 🎨 Customizing the UI

### Change Colors/Fonts/Spacing
Edit: `web/src/styles/theme.css`

```css
:root {
    --color-accent: #4a90d9;        /* Change accent color */
    --color-priority-high: #dc3545;  /* Change high priority color */
    --font-family: 'Your Font';      /* Change font */
    --spacing-unit: 8px;             /* Change spacing scale */
}
```
Refresh browser to see changes (no rebuild needed).

### Dark Mode
Already configured via `@media (prefers-color-scheme: dark)` in `theme.css`.

---

## 🗄️ Database Access

### Direct SQLite Access
```bash
sqlite3 /Users/jpezzone/Central_West_PMO/data/pmo.db
```

### Common Queries
```sql
-- View all tasks
SELECT * FROM tasks;

-- View today's tasks
SELECT * FROM tasks WHERE date = '2026-07-02';

-- View recurring templates
SELECT * FROM recurring_tasks;

-- View time blocks
SELECT * FROM time_blocks;

-- Delete a task
DELETE FROM tasks WHERE id = 5;

-- Update task status
UPDATE tasks SET status = 'done' WHERE id = 5;
```

### Reset Database
```bash
rm data/pmo.db
source venv/bin/activate
python3 scripts/init_db.py
```

---

## 📁 Project Structure Quick Reference

```
Central_West_PMO/
├── pmo/                  # Core Python package (edit business logic here)
│   ├── db.py            # Database schema & connection
│   ├── tasks.py         # Task CRUD operations
│   ├── timeblocks.py    # Time block operations
│   ├── recurring.py     # Recurring task logic
│   └── notes.py         # Notes operations
│
├── cli/                 # CLI scripts (edit command behavior)
│   ├── add_task.py
│   ├── view_day.py
│   ├── daily_review.py
│   ├── add_timeblock.py
│   ├── manage_recurring.py
│   └── task_notes.py
│
├── api/                 # Flask REST API
│   ├── app.py          # Main Flask app
│   └── routes/         # API endpoints
│
├── web/                # React frontend
│   └── src/
│       ├── components/ # UI components
│       ├── styles/     # CSS (customize here)
│       └── api/        # API client
│
├── .claude/
│   ├── commands/       # Slash command definitions
│   └── settings.json   # Pre-approved permissions
│
└── data/
    └── pmo.db         # SQLite database
```

---

## 🔧 Common Modifications

### Add a New Slash Command
1. Create `.claude/commands/your-command.md`
2. Follow the pattern from existing commands
3. Add bash permission to `.claude/settings.json` if needed

### Add a New CLI Script
1. Create `cli/your_script.py`
2. Import from `pmo/` package
3. Make it executable: `chmod +x cli/your_script.py`

### Add a New API Endpoint
1. Edit or create route file in `api/routes/`
2. Register blueprint in `api/app.py`
3. Restart Flask server

### Add a New React Component
1. Create `web/src/components/YourComponent.jsx`
2. Import and use in `App.jsx` or other components
3. Changes auto-reload in dev mode

---

## 🐛 Troubleshooting

### Flask won't start
```bash
# Check if port 5000 is in use
lsof -i :5000
# Kill process if needed
kill -9 <PID>
```

### React won't start
```bash
cd web
rm -rf node_modules package-lock.json
npm install
```

### Database is corrupted
```bash
rm data/pmo.db
source venv/bin/activate
python3 scripts/init_db.py
```

### Git push fails
```bash
# Check remote
git remote -v

# Re-add if needed
git remote set-url origin git@github.com:Jimmy2xJimmy2x/Central_West_PMO.git
```

---

## 📊 Priority Levels

- **high** - Urgent, critical tasks
- **medium** - Important but not urgent (default)
- **low** - Nice to have, can be deferred

## 📅 Date Format

Always use **ISO format**: `YYYY-MM-DD` (e.g., `2026-07-15`)

## 🔄 Recurring Schedule Types

- **daily** - Every day
- **weekly** - Specific days (1=Mon, 2=Tue, ..., 7=Sun)
- **custom** - Specific dates (provide list of YYYY-MM-DD dates)

### Weekday Examples
```bash
# Monday, Wednesday, Friday
--schedule weekly --days 1,3,5

# Weekdays only
--schedule weekly --days 1,2,3,4,5

# Weekends
--schedule weekly --days 6,7
```

---

## 🔗 Quick Links

- **GitHub Repo**: https://github.com/Jimmy2xJimmy2x/Central_West_PMO
- **Web GUI** (dev): http://localhost:5173
- **API** (dev): http://localhost:5000
- **Documentation**: See `CLAUDE.md` and `README.md`

---

## 💡 Tips

- Use `/view-day` to auto-generate recurring tasks for any date
- Click tasks in the web GUI to toggle done/pending
- The ↻ symbol indicates a recurring task instance
- Theme customization requires no rebuild - just edit CSS and refresh
- All dates are in your local timezone
