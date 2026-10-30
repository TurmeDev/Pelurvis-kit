"""Guard of the google module: nothing irreversible in email or the calendar.

Run by core/guard.py. It is a second barrier, in case the `allowed` list or the
Codex configuration were opened by mistake: it blocks by verb, in any app.
"""
import re

IRREVERSIBLE = re.compile(r"^mcp__.*__(send|forward|delete|trash|archive|respond|share|unshare|"
                          r"batch_modify|bulk_|apply_labels|update_app_permissions|uninstall)")


def check(tool, tin):
    if IRREVERSIBLE.search(tool):
        return "sending, forwarding, deleting, archiving or replying is not done by the bot: the owner does it."
    return None
