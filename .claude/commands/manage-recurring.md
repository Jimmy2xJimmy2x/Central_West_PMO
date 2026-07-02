---
description: Create, list, or remove recurring tasks
argument-hint: <list|add|remove> [options]
allowed-tools: [Bash]
---

# Manage Recurring Tasks

Current recurring tasks: !`source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/manage_recurring.py list`

## Instructions

Parse the user's arguments: $ARGUMENTS

Supported operations:
- **list**: Show all recurring task templates (already shown above)
- **add**: Create a new recurring task. Ask for title, schedule (daily/weekly/custom), and priority if not provided.
- **remove**: Delete a recurring task template by ID

For adding weekly tasks, the user can specify days like "weekdays", "MWF", "Monday,Wednesday,Friday", etc. Convert these to comma-separated ISO day numbers (1=Monday through 7=Sunday).

Run the appropriate command:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/manage_recurring.py <operation> [--title "name"] [--schedule daily|weekly|custom] [--days 1,2,3,4,5] [--priority medium] [--id N]
```

Examples:
- Daily task: `add --title "Morning review" --schedule daily`
- Weekdays: `add --title "Standup" --schedule weekly --days 1,2,3,4,5`
- Specific days: `add --title "Planning" --schedule weekly --days 1,3,5` (Mon, Wed, Fri)
