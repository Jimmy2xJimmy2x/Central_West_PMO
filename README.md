# Central West PMO - Management Assistant

A personal task management system with both CLI and web interfaces.

## Features

- **Daily task lists** with priorities (high/medium/low)
- **Time blocking** - assign tasks to specific time slots
- **Recurring tasks** - daily, weekly, or custom schedules
- **Task notes** - add context, links, or notes to any task
- **Dual interface** - use Claude Code slash commands or web GUI

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies
source venv/bin/activate
pip install -r requirements.txt

# Node dependencies
cd web && npm install
```

### 2. Initialize Database

```bash
source venv/bin/activate
python3 scripts/init_db.py
```

### 3. Start Development Servers

```bash
./scripts/start_dev.sh
```

This starts:
- Flask API server on http://localhost:5000
- React dev server on http://localhost:5173

## Claude Code Commands

Use these slash commands in any Claude Code session in this directory:

- `/add-task <title> [--priority high|medium|low]` - Add a new task
- `/view-day [date]` - View tasks and schedule
- `/daily-review` - End-of-day review with stats
- `/add-timeblock <start>-<end> [task]` - Schedule a task
- `/manage-recurring <add|list|remove>` - Manage recurring tasks
- `/task-notes <task> [note]` - Add notes to a task

## Manual CLI Usage

```bash
source venv/bin/activate

# Add a task
python3 cli/add_task.py --title "Review PR" --priority high

# View today's tasks
python3 cli/view_day.py

# View specific date
python3 cli/view_day.py --date 2026-07-03

# Add recurring task (weekdays)
python3 cli/manage_recurring.py add --title "Standup" --schedule weekly --days 1,2,3,4,5

# Daily review
python3 cli/daily_review.py
```

## Architecture

```
Central_West_PMO/
├── pmo/              # Core Python package (shared data layer)
├── cli/              # CLI scripts invoked by slash commands
├── api/              # Flask REST API
├── web/              # React frontend
└── data/             # SQLite database (pmo.db)
```

## Customizing the UI

Edit `web/src/styles/theme.css` to customize colors, fonts, and spacing. Changes take effect immediately (just refresh the browser).

## Database

SQLite database at `data/pmo.db`. Schema managed by `pmo/db.py`.

## Future Enhancements

- Google Workspace integration (Calendar, Gmail, Slack)
- Drag-and-drop task reordering
- Time block visualization
- Task templates
- Search and filtering
