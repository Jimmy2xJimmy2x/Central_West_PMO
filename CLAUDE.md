# Central West PMO - Management Assistant

## Project Overview
Personal daily task manager with two interfaces:
- Claude Code slash commands (in .claude/commands/)
- React web GUI served by Flask

## Tech Stack
- **Data layer**: Python package in pmo/, SQLite database at data/pmo.db
- **CLI**: Python scripts in cli/, invoked by Claude Code commands
- **API**: Flask server in api/, runs on port 5000
- **Frontend**: React + Vite in web/

## Common Commands
- Start API server: `source venv/bin/activate && python3 -m api.app`
- Start React dev server: `cd web && npm run dev`
- Initialize database: `source venv/bin/activate && python3 scripts/init_db.py`
- Build React for production: `cd web && npm run build`

## Database
SQLite at data/pmo.db. Schema managed by pmo/db.py.
Do not modify the database schema without updating pmo/db.py.

## Conventions
- Dates are always ISO format YYYY-MM-DD
- Times are always 24-hour HH:MM
- Priority values: high, medium, low
- Status values: pending, in_progress, done, cancelled
- Python scripts always run via virtual environment: `source venv/bin/activate`

## Available Slash Commands
- `/add-task` - Add a new task
- `/view-day` - View tasks and schedule for a day
- `/daily-review` - End-of-day review with stats
- `/add-timeblock` - Assign task to time slot
- `/manage-recurring` - Manage recurring task templates
- `/task-notes` - Add notes/links to tasks
