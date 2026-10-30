"""Guard of the notion module: the agenda is never deleted or emptied.

Run by core/guard.py. Second barrier behind `allowed`:
- blocks by verb (delete, move, duplicate, restore, agent sessions, skills,
  Notion calendar, schema changes);
- in notion_update_page, only lets properties be changed or specific text be edited: never
  `replace_content`, which replaces the whole page and may delete what the fetch does not show.
"""
import re

IRREVERSIBLE = re.compile(r"^mcp__codex_apps__notion__(notion_)?(delete|move|duplicate|restore|spawn|stop_session|"
                          r"send_message|upload_skill|convert_page_to_skill|update_enabled_skills|xldb_|calendar_|"
                          r"update_data_source|update_folder)")


def check(tool, tin):
    if IRREVERSIBLE.search(tool):
        return "in Notion nothing is deleted, moved or duplicated: what is no longer useful goes to \"Dropped\"."
    if tool == "mcp__codex_apps__notion__notion_update_page" and isinstance(tin, dict):
        if tin.get("command") not in (None, "update_properties", "update_content"):
            return "only properties are changed or specific text is edited; a whole page is never replaced."
        if tin.get("allow_deleting_content"):
            return "an edit cannot delete child pages or databases."
    return None
