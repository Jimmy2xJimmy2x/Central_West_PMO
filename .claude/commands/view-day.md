---
description: View your tasks and schedule for a given day
argument-hint: [YYYY-MM-DD or "today" or "tomorrow"]
allowed-tools: [Bash]
---

# View Day

Today's date: !`date +%Y-%m-%d`

## Current Day View

!`source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/view_day.py`

## Instructions

The above shows today's view. If the user specified a different date in their arguments ($ARGUMENTS), run:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/view_day.py --date "<date>"
```

Present the schedule and task list in a clear, readable format. Highlight high-priority items. Note any unscheduled tasks that might need time blocks.
