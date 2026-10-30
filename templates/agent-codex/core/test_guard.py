"""Tests for core/guard.py (Codex).  usage: python3 core/test_guard.py <agent-root>"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
H = str(ROOT / "core/guard.py")
# The tests run with a temporary HOME: that way their log does not go to the bot's.
TEST_HOME = tempfile.mkdtemp(prefix="guard-tests-")
HOME = Path(TEST_HOME)


def ev(tool, command=None, cwd=ROOT, **tin):
    if command is not None:
        tin["command"] = command
    return {"tool_name": tool, "tool_input": tin, "cwd": str(cwd)}


def patch(*lines):
    return "*** Begin Patch\n" + "\n".join(lines) + "\n*** End Patch\n"


cases = [
    ("ls of the workspace", ev("Bash", "ls -la"), True),
    ("read CORE.md", ev("Bash", "cat core/CORE.md"), True),
    ("read AGENTS.md", ev("Bash", f"cat {ROOT}/AGENTS.md"), True),
    ("read with 2>/dev/null", ev("Bash", "rg --files -g AGENTS.md . ~/.agents/skills 2>/dev/null"), True),
    ("write and silence", ev("Bash", "echo x > AGENTS.md 2>/dev/null"), False),
    ("note outside the layers", ev("apply_patch", patch("*** Add File: work/note.md", "+hello")), True),
    ("echo to a work file", ev("Bash", "echo hello > work/x.txt"), True),
    ("app with no module enabling it", ev("mcp__codex_apps__gmail_search_emails", query="today"), False),
    ("edit CORE.md (relative)", ev("apply_patch", patch("*** Update File: core/CORE.md", "@@", "-a", "+b")), False),
    ("edit skin (absolute)", ev("apply_patch", patch(f"*** Update File: {ROOT}/skin/identity.md")), False),
    ("create module", ev("apply_patch", patch("*** Add File: modules/x/guard.py", "+def check(t, i): return None")), False),
    ("delete AGENTS.md", ev("apply_patch", patch("*** Delete File: AGENTS.md")), False),
    ("move into the core", ev("apply_patch", patch("*** Update File: work/a.py", "*** Move to: core/guard.py")), False),
    ("patch from another cwd", ev("apply_patch", patch("*** Update File: ../skin/data.md"), cwd=ROOT / "work"), False),
    ("edit Codex config", ev("apply_patch", patch(f"*** Update File: {HOME}/.codex/config.toml")), False),
    ("echo > skin", ev("Bash", "echo x > skin/data.md"), False),
    ("edit a skill", ev("apply_patch", patch("*** Update File: .agents/skills/note/SKILL.md")), False),
    ("ln -s into .agents", ev("Bash", "ln -sf /tmp/x .agents/skills/bad"), False),
    ("sed -i AGENTS.md", ev("Bash", "sed -i s/a/b/ AGENTS.md"), False),
    ("rm of the core", ev("Bash", f"rm -rf {ROOT}/core"), False),
    ("cp over hooks.json", ev("Bash", "cp /tmp/x ~/.codex/hooks.json"), False),
    ("read auth.json", ev("Bash", "cat ~/.codex/auth.json"), False),
    ("read takopi token", ev("Bash", "grep token ~/.takopi/takopi.toml"), False),
    ("read bridge token", ev("Bash", "cat ~/.config/bot-secrets/telegram.env"), False),
    ("MCP with secrets", ev("mcp__fs__read", path=f"{HOME}/.takopi/takopi.toml"), False),
    ("launch subagent", ev("spawn_agent", message="hello"), False),
    ("subagent as Agent", ev("Agent", message="hello"), False),
]

def run(h, e):
    stdin = e if isinstance(e, str) else json.dumps(e)
    env = dict(os.environ, HOME=TEST_HOME)
    return subprocess.run([sys.executable, h], input=stdin, capture_output=True, text=True,
                          encoding="utf-8", env=env).returncode

failures = 0
def report(name, ok, detail):
    global failures
    failures += not ok
    print(f"{'OK ' if ok else 'BAD'} {name:32} {detail}")

for name, e, should in cases:
    rc = run(H, e)
    report(name, (rc == 0) == should, "allows" if rc == 0 else f"blocks (exit {rc})")
rc = run(H, "this is not json")
report("corrupt input", rc == 2, f"exit {rc}")

# A broken module guard blocks everything, even what used to pass.
with tempfile.TemporaryDirectory() as tmp:
    shutil.copytree(ROOT / "core", Path(tmp) / "core")
    (Path(tmp) / "modules/broken").mkdir(parents=True)
    (Path(tmp) / "modules/broken/guard.py").write_text("def check(t, i):\n    raise ValueError('x')\n")
    rc = run(str(Path(tmp) / "core/guard.py"), ev("Bash", "ls", cwd=Path(tmp)))
    report("module that raises", rc == 2, f"exit {rc}")
    (Path(tmp) / "modules/broken/guard.py").write_text("this is not python (\n")
    rc = run(str(Path(tmp) / "core/guard.py"), ev("Bash", "ls", cwd=Path(tmp)))
    report("module that does not compile", rc == 2, f"exit {rc}")
    (Path(tmp) / "modules/broken/guard.py").write_text("def check(t, i):\n    return 'no' if 'curl' in i.get('command', '') else None\n")
    rc = run(str(Path(tmp) / "core/guard.py"), ev("Bash", "curl x", cwd=Path(tmp)))
    report("module that blocks", rc == 2, f"exit {rc}")
    (Path(tmp) / "modules/broken/guard.py").unlink()
    (Path(tmp) / "modules/broken/allowed").write_text("# Gmail read\nmcp__codex_apps__gmail_(search|read)_.*\n")
    rc = run(str(Path(tmp) / "core/guard.py"), ev("mcp__codex_apps__gmail_search_emails", cwd=Path(tmp), query="today"))
    report("app enabled by a module", rc == 0, f"exit {rc}")
    rc = run(str(Path(tmp) / "core/guard.py"), ev("mcp__codex_apps__gmail_send_email", cwd=Path(tmp), to="x"))
    report("app outside the module's list", rc == 2, f"exit {rc}")

total = len(cases) + 6
shutil.rmtree(TEST_HOME, ignore_errors=True)
print(f"\n{total - failures}/{total} cases correct")
sys.exit(1 if failures else 0)
