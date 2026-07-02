---
description: Add notes, links, or context to a task
argument-hint: <task_id or task_name> [note text or URL]
allowed-tools: [Bash]
---

# Task Notes

Today's tasks: !`source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/view_day.py`

## Instructions

Parse the user's arguments: $ARGUMENTS

If the user references a task by name, find its ID from the task list above.

Operations:
- If the user provides note text: add a note
- If the user provides a URL: add it as a link-type note
- If no note content: list existing notes for the task

Run the appropriate command:
```bash
source /Users/jpezzone/Central_West_PMO/venv/bin/activate && python3 /Users/jpezzone/Central_West_PMO/cli/task_notes.py --task-id <N> [--add "note text" | --add-link "URL" | --list]
```

Show the result. When listing notes, format them clearly with timestamps and type indicators.
