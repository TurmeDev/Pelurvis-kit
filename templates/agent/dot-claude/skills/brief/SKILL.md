---
name: brief
description: Morning summary of the day for the user, sent over Telegram. It fires on its own at 06:30; also use it when they ask for "the brief", "daily summary" or "what do I have today?".
---

# Morning brief

It only **reads**: do not create, edit or delete anything anywhere. Send the
result with `reply` to the owner's chat (ID in `skin/data.md`), even if the request arrived from
the terminal (the automatic trigger arrives that way).

## What to gather (today, America/Asuncion timezone)

1. **Today's classes**: the *schedule* view (`skin/data.md`), the rows with
   `Day of Week` = today's weekday name (Monday … Saturday), by
   `Start Time`. Show time, course and room. Sunday: "no classes".
2. **Calendar**: today's events with `list_events`.
3. **Educa due dates** in the next 72 h: `uni educa pending`.
   Only report the date and the name; do not check the status of each submission.
4. **University email** from the last 24 h: `search_threads` with
   `newer_than:1d (from:pol.una.py OR from:una.py)`. Up to 5, with sender and
   subject on one line. No drafts or replies.
5. **Unprocessed Inbox**: count the rows of the *unprocessed* Inbox view
   (`skin/data.md`).

## Format (short, to read on the phone)

```
☀️ <Day> <dd/mm>

📚 Classes
• 14:00–16:30 Programming Languages III (F37)

📅 Agenda
• …   (or "nothing in Calendar")

⏰ Due soon
• Sat 24/10 23:59 · DS · Unit 6 Assignment – Web Services

✉️ University
• Prof. X · Subject   (or "no new emails")

📥 Inbox: N unprocessed
```

- Omit a whole section if it has nothing, except "Classes".
- If a source fails, put "⚠️ couldn't read <source>" and continue with the others.
- No advice or filler: only the data.
