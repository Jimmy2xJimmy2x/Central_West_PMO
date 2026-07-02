---
description: Add a new task to your daily task list
argument-hint: <title> [--priority high|medium|low] [--date YYYY-MM-DD]
allowed-tools: [Bash]
---

# Add Task

Today's date: !`date +%Y-%m-%d`

## Instructions

Parse the user's arguments: $ARGUMENTS

Extract:
- **title** (required): the task name
- **priority** (optional, default: medium): high, medium, or low
- **date** (optional, default: today): YYYY-MM-DD format

Run this command to add the task:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/add_task.py --title "<title>" --date "<date>" --priority "<priority>"
```

Report the result to the user. If they did not specify a date, confirm it was added to today.
