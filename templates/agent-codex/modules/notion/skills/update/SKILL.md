---
name: update
description: Changes the status, date or priority of a task or idea in the Notion agenda. Use it when the owner says "I did it", "done with…", "move it to tomorrow", "change the date", "that's off", "it's urgent".
---

# Update the agenda

1. Find the row in ✅ Tasks or 💡 Ideas (IDs in `skin/data.md`) by the words they used.
   If two look alike or none does, ask which one (a single question) before changing anything.
2. Change **only properties** with `notion_update_page` (`update_properties`):
   - "I did it", "done" → Status = Done.
   - "move it to…", "change the date" → new Date (calculated from today). If it had a
     reminder in Calendar, say that the owner changes that event from Calendar.
   - "it's urgent", "it's not urgent" → Priority.
   - "that's off", "cancel it" → Status = Dropped. **Never delete.**
3. Confirm in one line with the link:
   `✔️ <title>: <what changed> (Tasks, Notion)`.
