# Owner data

The only personal data of the bot. Skills and modules refer to it; do not
copy it anywhere else.

## Telegram

- Owner's chat: `<YOUR_TELEGRAM_CHAT_ID>`

## Notion

| What | ID or URL |
|---|---|
| Dashboard (*<Your Notion dashboard>*) | `<YOUR_DASHBOARD_URL>` |
| 📥 Pelurvis Inbox | `collection://<YOUR_INBOX_ID>` |
| 💡 Ideas Backlog | `collection://<YOUR_IDEAS_BACKLOG_ID>` |
| Tasks/Assignments/Labs | `collection://<YOUR_TASKS_DATABASE_ID>` |
| Exam Dates | `collection://<YOUR_EXAMS_DATABASE_ID>` |
| Class Schedule | `collection://<YOUR_SCHEDULE_ID>` |
| 👥 Contacts | `collection://<YOUR_CONTACTS_ID>` |
| Attendance Control | `collection://<YOUR_ATTENDANCE_ID>` |

## Notion views (to read without spending the SQL quota)

| "Pelurvis · …" view | Database and filter | URL |
|---|---|---|
| schedule | Class Schedule, all rows, by day and time | `view://<SCHEDULE_VIEW>` |
| open or recent | Tasks/Assignments/Labs: not `Complete` or from the last 7 days | `view://<TASKS_VIEW>` |
| pending or recent | Exam Dates: not `Completed` or from the last 7 days | `view://<EXAMS_VIEW>` |
| unprocessed | Inbox: `Processed` unchecked | `view://<INBOX_VIEW>` |
| in progress | Ideas Backlog: 🌱 New or 🔍 In review | `view://<IDEAS_VIEW>` |
| window | Attendance: from 7 days ago to 7 days ahead | `view://<ATTENDANCE_WINDOW_VIEW>` |
| all | Attendance: all rows, by date | `view://<ATTENDANCE_ALL_VIEW>` |

## Courses (pages in Courses)

- <Course 1> (<alias>): <URL of the course page in your Courses database>
- <Course 2>: <URL of the course page in your Courses database>

## University

- Degree program code in Ealu: `<DEGREE_CODE>`
- Minimum attendance: `<PERCENTAGE>` %
