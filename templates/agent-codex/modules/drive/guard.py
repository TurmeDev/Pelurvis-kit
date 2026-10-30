"""Guard of the drive module: read-only. Second barrier behind `allowed`."""
import re

WRITE = re.compile(r"^mcp__codex_apps__google_drive__(create|update|batch_update|bulk_update|delete|share|"
                   r"upload|copy|import|duplicate)")


def check(tool, tin):
    if WRITE.search(tool):
        return "in Drive the bot only searches and reads: it does not create, change, share or delete files."
    return None
