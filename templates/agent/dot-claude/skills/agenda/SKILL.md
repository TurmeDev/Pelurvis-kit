---
name: agenda
description: Answers what the owner has on a specific day or range (tomorrow, Thursday, 5/11, this week, next week), combining classes, Calendar, assignments, exams and to-dos. Use it when they ask "what do I have tomorrow / Thursday / this week?", "am I free on …?", or "when is the midterm for …?". For today's summary, the `brief` skill; for "what do I have to hand in?", the university module.
---

# Check the agenda

It only **reads**: do not create, edit or delete anything. Send the result with
`reply` to the owner's chat (ID in `skin/data.md`), even if the request
arrived from the terminal.

## 1. The range

- Current date and time: `date '+%A %d/%m/%Y %H:%M'` (America/Asuncion
  timezone). Do not infer it: the session may carry over from the previous day.
- "tomorrow", "Thursday" (the next one), "5/11", "this week" (from today to
  Sunday), "next week" (Monday to Sunday). If no time is given, tomorrow.
  "When is the midterm for …?" = from today onward, exams only.

## 2. What to gather (IDs in `skin/data.md`)

1. **Classes**: *schedule* view, the rows whose `Day of Week` falls in
   the range, by `Start Time`. Time, course (`Name`) and `Room`.
2. **Calendar**: events in the range with `list_events`.
3. **Tasks/Assignments/Labs** (their view): `Due date` within the range and `Complete` unchecked.
   If the range starts today, also the overdue ones (`Due date` before today,
   without `Complete`).
4. **Exam Dates** (their view): `Date` within the range and `Completed` unchecked.
   With `Type` and `Room`.
5. **Dashboard to-dos**: `notion-fetch` of the dashboard and only the
   `## To-dos` section. The `- [ ]` items under 🚨 Urgent and ⚠️ Medium Urgency
   (🛃 Chill only if asked). If the text names a date,
   put it on that day; otherwise at the end.

For the question about a midterm, only source 4.

Databases are read with their views from `skin/data.md` (`view` mode), and you
filter the range yourself over what they return.

## 3. Format (short, for the phone)

```
📅 Thursday 30/10
📚 14:00–16:30 Programming Languages III (F37)
• 10:00 Doctor's appointment (Calendar)
• 23:59 DS · Unit 7 Assignment (Assignment)
📝 Networks II · 2nd Midterm · Room F21

⚠️ Overdue: Calculus · Process activity (was due Mon 26/10)
📌 To-dos: 🚨 Study BASH up to chap 3
```

- One block per day in the range, in order; omit empty days in a long range.
  For a single day with nothing: "Nothing scheduled for <day dd/mm>."
- "Am I free on …?": answer yes or no first and in which time slots they are
  busy, then the detail.
- If a source fails, put "⚠️ couldn't read <source>" and continue with the others.
- Only the data: no advice or study plans, unless they ask.
