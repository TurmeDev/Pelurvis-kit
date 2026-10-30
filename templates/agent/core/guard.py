#!/usr/bin/env python3
"""Skeleton PreToolUse hook: self-protection and module guards.

Blocks (exit 2) any tool that:
- reads or writes the secrets (~/.config/pelurvis-secrets);
- modifies the core, the skin, the modules, CLAUDE.md or the project
  configuration (.claude/).
Then it runs `check(tool, tool_input)` from each modules/*/guard.py: if one
returns a reason, or if it fails to load or to run, the call is blocked. This
way a module can only add blocks.
A PreToolUse block holds in any permission mode, even if the user approves the
action by mistake.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # do not leave __pycache__ inside modules/
ROOT = Path(__file__).resolve().parent.parent
SECRETS = re.compile(r"pelurvis-secrets")
PROTECTED = re.compile(r"/pelurvis/(core/|skin/|modules/|\.claude/|CLAUDE\.md)|/\.claude/settings(\.local)?\.json")
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
BASH_WRITES = re.compile(r"(>|\btee\b|\bsed\b.*-i|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\bln\b)")


def block(reason: str) -> None:
    print(f"Blocked by the guard: {reason}", file=sys.stderr)
    sys.exit(2)


def base(tool: str, tin: dict) -> None:
    if tool == "Bash":
        cmd = tin.get("command", "")
        if SECRETS.search(cmd):
            block("secrets are neither read nor written.")
        if PROTECTED.search(cmd) and BASH_WRITES.search(cmd):
            block("the core, the skin, the modules and the configuration are not modified.")
        return
    if SECRETS.search(json.dumps(tin, ensure_ascii=False)):
        block("secrets are neither read nor written.")
    if tool in WRITE_TOOLS:
        target = tin.get("file_path") or tin.get("notebook_path") or json.dumps(tin, ensure_ascii=False)
        if PROTECTED.search(target):
            block("the core, the skin, the modules and the configuration are not modified.")


def modules(tool: str, tin: dict) -> None:
    for guard in sorted(ROOT.glob("modules/*/guard.py")):
        name = guard.parent.name
        spec = importlib.util.spec_from_file_location(f"guard_{name}", guard)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        reason = mod.check(tool, tin)
        if reason:
            block(f"[{name}] {reason}")


def main() -> None:
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    tin = event.get("tool_input") or {}
    base(tool, tin)
    modules(tool, tin)


if __name__ == "__main__":
    # On any error, block: a hook that fails with another exit code does not block.
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        block(f"internal error ({type(e).__name__}); blocking for safety.")
