---
name: attendance
description: Marks and checks class attendance in the Attendance Control database in Notion. Use it when they say "I went to …", "I missed …", "I went to all of them today", "I'm not going to … (excused)", "how many absences do I have in …?", "how am I doing on attendance?", or when they answer the nightly attendance question ("yes", "I missed Calculus"). With no text (the nightly trigger), ask about today's classes.
---

# Attendance

**Single** database: *Attendance Control* (ID in `skin/data.md`). One row per
class held: `Class` (title), `Date`, `Day`, `Time`, `Course` (relation
to Courses), `Status` (Attended, Missed, Excused, Pending) and `Notes`.
Minimum attendance: the one in `skin/data.md`.

Read **only with the views** from `skin/data.md` (`notion-query-data-sources`
in `view` mode): *window* (from 7 days ago to 7 ahead) for marking and
asking, *all* for percentages (paginate with `start_cursor` until
`has_more: false`). Date and time: `date '+%A %d/%m/%Y %H:%M'`.

## Nightly question (`/attendance` arrives with no text)

1. From the *window* view, the rows for **today** with `Status` = Pending.
2. If there are none, **send nothing** over Telegram and finish.
3. If there are, send with `reply` to the owner's chat (ID in `skin/data.md`):
   `🎓 Today you had: Physics 3 (15:00) and Calculus (17:30). Did you go? Reply "yes", "no" or "missed Calculus".`
   Do not mark anything until they answer.

## Marking

1. **Which class and which day**: today unless they name another day
   ("yesterday", "on Monday"). Recognize the course by alias:
   Physics 3 / Physics III, Calc / Calculus, Networks, DB / Databases
   (replace with your own courses and their nicknames).
   "I went to all of them" or "yes" = all of that day's. "No" = none.
2. **Status**: "I went", "yes" → Attended; "I missed", "I didn't go" →
   Missed; with a reason that excuses it ("I was sick, I have a certificate")
   or if they say "excused" → Excused, with the reason in `Notes`. If in
   doubt, ask once.
3. **Find the row** in the *window* view (same `Class` and `Date`). If it is
   there, change only `Status` (and `Notes` if there is a reason) with
   `notion-update-page` (`update_properties`). If it is from before the
   window, ask for the exact date and look for it in *all*.
4. **If the row does not exist** (a make-up class, or after the last date
   loaded), create it with `notion-create-pages` in the database, with the data
   from the *schedule* view in `skin/data.md`: `Class` and `Time` like the
   other rows of that course, `Day`, `Date`, `Course` and the `Status`.
5. **Confirm** in one line:
   `✔️ Attendance 30/10: Physics 3 ✅ · Calculus ❌` (✅ Attended, ❌ Missed, 🟡 Excused).
   If an absence was recorded, add the warning line (below) only if it applies.

If a row says "DUPLICATE" in `Notes`, ignore it and tell the owner to delete it.

## Checking

"How many absences do I have in Networks?", "how am I doing?": read *all* and,
per course (grouping by `Course`):

- **Held** = rows with `Date` up to today and `Status` other than Pending.
- **Attendance %** = (Attended + Excused) / held.
- **Absences left** = floor(total rows of the course × (1 − minimum))
  − absences. The total includes future classes already loaded.

```
🎓 Attendance (minimum 75 %)
• Networks II: 92 % · 2 absences · 3 left
• Calculus: 100 % · 0 absences · 3 left
⚠️ Physics 3: 78 % · 1 absence left
```

Sort from the most at risk to the least. Rows in Pending with a past date do
not count: at the end, "⏳ Unmarked: <class dd/mm>, …".

## Warning

Flag a course with ⚠️ if its % falls below minimum + 5 points or it has 2
absences left or fewer; 🚨 if it is already below the minimum or has no
absences left.

## Rules

- You only write to *Attendance Control*, and only `Status`, `Notes` or new
  rows. **Never delete** a row.
- Do not mark future classes as Attended. If the owner says they are going to
  miss one, the future one can be left as Missed or Excused.
