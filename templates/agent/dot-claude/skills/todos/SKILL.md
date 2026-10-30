---
name: todos
description: Adds, marks as done, moves or sorts the items of the "To-dos" section of the Notion dashboard (🚨 Urgent, ⚠️ Medium Urgency, 🛃 Chill). Use it when the user says "to-dos", "note under urgent / medium / chill", "I already handed in …", "done …", "clean up / sort the to-dos" or asks for something by urgency.
---

# Dashboard to-dos

Page: the owner's dashboard (URL in `skin/data.md`). You only touch the
`## To-dos` section; the rest of the page (embeds, buttons, databases,
projects) is **never touched**.

## Section structure

```
## To-dos

🚨 Urgent

- [ ] …

---

⚠️ Medium Urgency

- [ ] …

---

🛃 Chill

- [ ] …
```

Format of each item: `- [ ] <Short course>: <what> (due <day> dd/mm[ hh:mm])`.
No course if it is personal. No `(due …)` if there is no date.

## How to edit (always the same)

1. `notion-fetch` the page and copy the **exact** text from `🚨 Urgent`
   to the last item of `🛃 Chill`, before `</column>`.
2. If you do not find `## To-dos` or any of the three headings, **do not
   edit**: say that the structure changed.
3. Build the new block and apply it with `notion-update-page`, `command`
   `update_content`, with a single `old_str` (the copied block) →
   `new_str` (the new block) pair.
4. **Never** use `replace_content` on this page: the page arrives truncated
   and has blocks that the fetch does not show (a button); replacing it deletes them.
5. If `update_content` fails because the text does not match, fetch again
   once and retry. If it fails again, say so and do not insist.

## Operations

- **Add**: in the section the user says. If they do not say which, decide by
  the date (today, America/Asuncion timezone): due in 3 days or less → Urgent;
  up to 10 days → Medium; no date or further away → Chill. Say so in the
  confirmation so they can correct it.
- **Done** ("I already handed in X", "done X"): change `- [ ]` to `- [x]` on that
  item. Do not delete it yet.
- **Move**: take the item out of its section and put it in the other.
- **Clean or sort**: remove the `- [x]` items and empty ones (`- [ ] ` with no
  text); within each section, sort by date (undated at the end).
  Promote to a more urgent section what, by date, now belongs there; never
  demote something the user set as urgent.
- Add **only** what the user names. To fill in a date or an exact task
  name you may read `uni educa pending`, but do not copy Educa tasks
  they did not ask for into To-dos.
- If the item they mention is not there or two look alike, ask which (a
  single question) before editing.

## Confirmation (one or two lines)

`📌 To-dos: + <item> → 🚨 Urgent` (or `✔️ done: …`, `↕️ moved: …`,
`🧹 cleaned N, sorted by date`) and the link to the page.

## What it does not do

- It does not create pages or rows in Tasks/Assignments/Labs, Exam Dates or the Inbox
  (for loose notes there is `capture`).
- It does not hand in anything or touch Educa or Ealu: it only reads them.
