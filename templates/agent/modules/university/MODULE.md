# University module (FPUNA example): Educa and Ealu, READ-ONLY

- **Educa** (Moodle, grado.pol.una.py): courses, upcoming assignments, tasks,
  contents, grades and announcements.
- **Ealu** (cnc.una.py/ealu, POLSL faculty): session and degree programs,
  grades, exam schedule, registered enrollments, debts, messages.
- Access **only** with `/home/pelurvis/pelurvis/modules/university/bin/uni`,
  one command per call and no pipes. `uni actions` lists what can be
  queried. Start with `uni educa pending` or `uni educa courses` to get the
  ids. If the output comes back truncated, ask for something more specific (a
  course id or an assignment id).
- In Ealu, the degree program argument is the code from `skin/data.md`. For
  example: `uni ealu ultimas-notas/ <code>`, `uni ealu horario-examen/ <code>`,
  `uni ealu inscripciones-registradas/ <code>`.
- For "what do I have to hand in?", cross-check `uni educa pending` with the
  assignments in Notion and with Calendar.
- **Never** submit assignments, enroll or unenroll, or change anything on
  those platforms. There is no way to do it and do not look for one. If the
  owner asks, explain how they can do it themselves and give them the link.
- If `uni` says credentials are missing, ask the owner to run
  `ssh -t pelurvis@pelupc ~/pelurvis/modules/university/bin/uni-setup`. Never
  ask for passwords over Telegram.
