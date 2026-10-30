"""Guard for the university module: Educa and Ealu are read-only, and only through bin/uni.

It is run by core/guard.py. `check` returns the reason to block, or None.
Mentioning the domain in Notion or in Telegram (for example, a link) is
allowed; what is blocked is accessing it by any path other than `uni`.
"""
import json
import re

UNI_CMD = re.compile(r"^/home/pelurvis/pelurvis/modules/university/bin/uni( (educa|ealu) [A-Za-z0-9/_-]{1,40}( [A-Za-z0-9_-]{1,40})?| actions)$")
UNA = re.compile(r"una\.py", re.I)
BROWSER = re.compile(r"browser|chrome|playwright|puppeteer", re.I)


def check(tool, tin):
    if tool == "Bash":
        cmd = tin.get("command", "").strip()
        if UNI_CMD.match(cmd):
            return None
        if "/bin/uni" in cmd:
            return "`uni` is only run on its own, with no redirections, pipes or other commands."
        if UNA.search(cmd):
            return "Educa/Ealu are only accessed with `uni`."
        return None
    browses = tool == "WebFetch" or BROWSER.search(tool)
    if browses and UNA.search(json.dumps(tin, ensure_ascii=False)):
        return "Educa/Ealu are only accessed with `uni`."
    return None
