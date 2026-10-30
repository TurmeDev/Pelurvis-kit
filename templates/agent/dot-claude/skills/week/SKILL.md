---
name: week
description: Weekly review over Telegram (what you closed, what is still pending and what is coming next week). It fires on its own on Sundays at 20:00; also use it when they ask for "the week", "weekly review" or "how did I close the week?".
---

# Weekly review

It only **reads**: do not create, edit or delete anything. Send the result with `reply`
to the owner's chat (ID in `skin/data.md`), even if the request arrived from the terminal (the
automatic trigger arrives that way).

"This week" = the last 7 days up to today; "next" = the following 7 days.
America/Asuncion timezone.

## What to gather

1. **Dashboard to-dos**: `notion-fetch` the dashboard (URL in
   `skin/data.md`) and read only the
   `## To-dos` section: the `- [x]` (done) and the `- [ ]` per section.
2. **Tasks/Assignments/Labs**, from their view (`skin/data.md`):
   with `Due date` this week, split by `Complete`.
3. **Exam Dates**, from their view (`skin/data.md`):
   those of this week and the non-`Completed` ones in the next **14** days.
4. **Educa**: `uni educa pending`, only those due next week.
   Name and date; do not check the status of each submission.
5. **Calendar**: next week's events with `list_events`.
6. **Inbox**, *unprocessed* view (`skin/data.md`): how many captures and
   which is the oldest (the first).
7. **Ideas to review**: the candidates from the *in progress* view
   (`skin/data.md`), with the criteria,
   order and numbered format from the "Reviewing ideas" section of the
   `idea` skill.

## Format (short, for the phone)

```
🗓️ Week <dd/mm>–<dd/mm>

✅ Closed
• DS · Unit 6 Assignment – Web Services

⏳ Still pending
• 🚨 Calculus · Process activity (was due Mon 26/10)

📅 Next week
• Wed 28/10 · Networks 2 · Weekly quiz
• Fri 30/10 23:59 · Physics III · Report 5

📝 Exams (14 days)
• …

📥 Inbox: N unprocessed (oldest: <title>, <dd/mm>)

🎯 To get started: 1) … 2) … 3) …

💡 Ideas to review
1. <Idea> — <Pitch> · M · logged 20/10
2. …
Reply by number: go / keep / freeze / discard
```

- "To get started": the 3 most urgent things of next week, by date.
  It is the only thing that is not a copied datum; no general advice.
- Omit empty sections, except "Next week" ("nothing in sight").
- If a source fails, put "⚠️ couldn't read <source>" and continue.
- If there are `- [x]` in To-dos, add at the end: "Should I clean up the
  done to-dos?". If they say yes, the `todos` skill does that.
- Ideas always go last, so the numbered reply is the last thing in the
  message. This skill does not change their status: the `idea` skill applies
  the answer. If there are no candidates, omit the section.
