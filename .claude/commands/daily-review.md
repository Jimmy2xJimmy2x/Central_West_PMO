---
description: End-of-day review with completion stats and task rollover
argument-hint: [--date YYYY-MM-DD]
allowed-tools: [Bash]
---

# Daily Review

Today's date: !`date +%Y-%m-%d`

## Today's Status

!`source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/view_day.py`

## Instructions

Run the daily review:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/daily_review.py
```

Present the results to the user. The script shows completion stats and prepares tomorrow's recurring tasks. If there are incomplete tasks, ask the user whether they want to move them to tomorrow or cancel them.
