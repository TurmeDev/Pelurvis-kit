# Productivity module (Notion)

Skills in `.claude/skills/`: `capture`, `brief`, `todos`, `week`,
`idea`, `agenda`, `contact` and `attendance`. The IDs of each database are in `skin/data.md`.

| Skill | Writes to |
|---|---|
| `capture` | only the Inbox |
| `todos` | only the `## To-dos` section of the dashboard |
| `idea` | only the ideas Backlog |
| `contact` | only 👥 Contacts, and only if the owner asks or confirms |
| `attendance` | only Attendance Control: `Status`, `Notes` and missing rows |
| `brief`, `week`, `agenda` | nothing: they only read |

## Rules

- When in doubt about where to save something, it goes to the Inbox.
- The dashboard is edited only with `update_content` and exact
  `old_str`/`new_str` pairs. **Never** `replace_content`: the page arrives
  truncated and has blocks that the fetch does not show, so replacing it
  deletes them.
- Tasks/Assignments/Labs, Exam Dates and Schedule are read-only.
- Databases are read with the "Pelurvis · …" views from `skin/data.md`. Do not
  change their filters: the skills depend on them.
- In the ideas Backlog nothing is deleted: what is discarded stays as 🗑️ Discarded.
- In Contacts nothing is deleted, and their data does not leave there unless
  the owner asks.

## Schedules

They are fired by `core/bin/trigger` from systemd: `/brief` at 06:30,
`/week` on Sundays at 20:00 and `/attendance` Monday to Friday at
21:30 and on Saturdays at 13:30 (if everything is already marked, it sends nothing). Its result always goes by Telegram to the
owner's chat, even if the request arrives from the terminal.
