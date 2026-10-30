---
name: agenda
description: Answers what the owner has today, tomorrow, this week or on a specific day, combining Google Calendar and the Notion tasks. Use it when they ask "what do I have…?", "what's on for today?", "am I free on…?", "what am I missing?".
---

# Check the agenda

Read-only: do not create or change anything.

1. Work out the range they ask for (today, tomorrow, the week, a day) in the time zone from
   `skin/data.md`.
2. Gather:
   - the Google Calendar events in the range, if the google module is present;
   - from ✅ Tasks, those with a Date inside the range and, if the range includes today, also the
     overdue ones (Date before today). Excluding those that are Done or Dropped.
3. Reply briefly, ordered by day and time:

```
📅 <day dd/mm>
• 10:00 Meeting with the accountant (Calendar)
• Hand in the assignment · 🔴 (Task)
⚠️ Overdue: <task> (was due <dd/mm>)
```

If there is nothing: "You have nothing noted for <range>." If a source fails, say so in one
line and show what you could read.
