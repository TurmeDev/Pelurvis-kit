---
name: note
description: Records in the Notion agenda what the owner wants to do, remember or keep (task, idea or fact). Use it when they say "note down", "remind me", "I have to…", "don't let me forget", "save", "idea:", or mention something pending, even if it arrives as a voice note.
---

# Record in the agenda

The databases are in `skin/data.md` (✅ Tasks, 💡 Ideas, 📝 Notes).

## 1. Classify

| It is… | Goes to | Example |
|---|---|---|
| something to do, even with a date or time | **✅ Tasks** | "hand in the assignment tomorrow" |
| a meeting, appointment or slot with other people or at a place | **Google Calendar** (if the google module is present), not Tasks | "meeting with the accountant Tuesday at 10" |
| a brainwave or project | **💡 Ideas** | "idea: sell cakes on Sundays" |
| a fact not to forget | **📝 Notes** | "the car's license plate is ABC123" |

If it truly cannot be known, ask **one** question. Do not ask for the time if they did not give one.

## 2. Fill in and create

- **Tasks**: Task (short title, at most ~8 words), Status = To do, Date if stated (calculated from today, in the time zone from `skin/data.md`; with time if stated), Priority (if not given: due in 3 days or less → 🔴 High, up to 10 days → 🟡 Medium, no date or further out → 🟢 Low), Area if clear, Source = Voice if it came from a voice note, otherwise Text.
  - **If they gave a time**, also create a short (15 min) event in Google Calendar as a reminder, with the same title.
- **Ideas**: Idea, Pitch (one line), Status = 🌱 New, Reviews = 0, Effort estimated by you.
- **Notes**: Note (title), Type (Note, Fact, Link or Purchase), Area if clear, Date = today. The full fact goes in the body.
- One row per item. If the message has several, create one for each (maximum 5).

## 3. Always confirm where it ended up

One line per item, with the row's link:

`✅ Recorded in Tasks (Notion): <title> · 📅 <day dd/mm[ hh:mm]> · <priority>`
`🔔 Reminder in Calendar: <day dd/mm hh:mm>` (only if you created it)
`💡 Recorded in Ideas (Notion): <idea>` · `📝 Recorded in Notes (Notion): <title>`
`📅 Scheduled in Calendar: <title> · <day dd/mm hh:mm>`

If something failed, say so and do not say "recorded".
