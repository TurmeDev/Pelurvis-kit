#!/usr/bin/env python3
"""Skeleton PreToolUse (Codex): self-protection and module guards.

Blocks (exit 2) any tool that:
- reads or writes the secrets (~/.codex/auth.json, ~/.takopi/, ~/.config/*-secrets);
- modifies the core, the skin, the modules, AGENTS.md or the Codex and takopi
  configuration;
- launches subagents: each one consumes tokens separately, and Codex offers them even if
  `multi_agent` is off;
- uses an external tool (`mcp__…`: apps and MCP servers) that no module
  has declared in modules/<m>/allowed (one regex per line).
Logs every decision in ~/.local/state/bot/guard.log.
Then it runs `check(tool, tool_input)` of each modules/*/guard.py: if one
returns a reason, or if it fails to load or to run, it blocks. That way a
module can only add blocks.

Codex calls commands `Bash` and edits `apply_patch`; both carry
the text in tool_input.command, and paths may be relative to `cwd`.
"""
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True  # do not leave __pycache__ inside modules/
ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
PROTECTED = [ROOT / "core", ROOT / "skin", ROOT / "modules", ROOT / "AGENTS.md",
             ROOT / ".agents", HOME / ".agents", HOME / ".codex", HOME / ".takopi"]
SECRETS = re.compile(r"\.codex/auth\.json|\.takopi|-secrets\b|/\.config/[^/\s]*secrets")
# In Bash, protected names as a path component (absolute or relative).
NAMES = re.compile(r"(^|[\s'\"=/;&|(])(core|skin|modules|\.agents|\.codex|\.takopi)(/|$|[\s'\";&|)])|AGENTS\.md")
WRITES_IN_BASH = re.compile(r"(>|\btee\b|\bsed\b.*-i|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\bln\b|\btruncate\b|\binstall\b|\bdd\b)")
SUBAGENTS = re.compile(r"spawn_agent|^Agent$|followup_task")
PATCH_PATH = re.compile(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", re.M)


LOG = HOME / ".local/state/bot/guard.log"
_tool = "?"


def log(decision: str, reason: str = "") -> None:
    """One line per decision: serves as an audit trail and to see the tools' real names."""
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a") as f:
            f.write(json.dumps({"t": int(time.time()), "tool": _tool,
                                "decision": decision, "reason": reason}, ensure_ascii=False) + "\n")
    except OSError:
        pass  # without a log, protection does not stop


def block(reason: str) -> None:
    log("block", reason)
    print(f"Blocked by the guard: {reason}", file=sys.stderr)
    sys.exit(2)


def allowed() -> list:
    """External tools (apps, MCP) enabled by some module, in modules/*/allowed."""
    patterns = []
    for file in sorted(ROOT.glob("modules/*/allowed")):
        for line in file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(re.compile(line))
    return patterns


def protected(path: Path) -> bool:
    path = path.resolve()
    return any(path == p or p in path.parents for p in PROTECTED)


def base(tool: str, tin: dict, cwd: Path) -> None:
    if SUBAGENTS.search(tool):
        block("the bot does not launch subagents.")
    text = tin.get("command", "") if isinstance(tin.get("command"), str) else json.dumps(tin, ensure_ascii=False)
    if tool == "Bash":
        if SECRETS.search(text):
            block("secrets are neither read nor written.")
        # Silencing errors (2>/dev/null, 2>&1) does not write to any protected file.
        unsilenced = re.sub(r"\d?>>?\s*/dev/null|\d>&\d", "", text)
        if NAMES.search(text) and WRITES_IN_BASH.search(unsilenced):
            block("the core, the skin, the modules and the configuration are not modified.")
        return
    if tool == "apply_patch":
        for path in PATCH_PATH.findall(text):
            if protected(cwd / path.strip()):
                block("the core, the skin, the modules and the configuration are not modified.")
        return
    if SECRETS.search(json.dumps(tin, ensure_ascii=False)):
        block("secrets are neither read nor written.")
    # External tools: denied unless a module enables them. That way an app that the
    # account syncs on its own does not become available without the administrator deciding.
    if tool.startswith("mcp__") and not any(p.fullmatch(tool) for p in allowed()):
        block(f"\"{tool}\" is not enabled by any module.")


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
    global _tool
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    _tool = tool
    tin = event.get("tool_input") or {}
    cwd = Path(event.get("cwd") or ROOT)
    base(tool, tin, cwd)
    modules(tool, tin)
    log("allow")


if __name__ == "__main__":
    # On any error, block: a hook that fails with another code does not block.
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        block(f"internal error ({type(e).__name__}); blocking for safety.")
