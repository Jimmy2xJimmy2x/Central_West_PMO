---
description: Assign a task to a time slot or block time on your schedule
argument-hint: <start_time>-<end_time> [task description or --task-id N]
allowed-tools: [Bash]
---

# Add Time Block

Today's date: !`date +%Y-%m-%d`
Current tasks: !`source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/view_day.py`

## Instructions

Parse the user's arguments: $ARGUMENTS

Extract the start time, end time, and either a task ID or a label. If the user references a task by name rather than ID, look it up from the current task list shown above.

Run:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/add_timeblock.py --date "<date>" --start "<HH:MM>" --end "<HH:MM>" [--task-id N | --label "description"]
```

Confirm the time block was added and show the updated schedule.
