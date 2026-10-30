---
title: Pelurvis — guide to replicating the assistant
type: guide
status: active
summary: Architecture, services, decisions, security and steps to set up an always-on personal assistant like Pelurvis, with Claude Code or Codex, plus templates without personal data.
related: [../README.md, DECISIONS.md, ../templates/]
tags: [agent, assistant, claude-code, codex, telegram, notion, guide]
updated: 2026-10-29
---

# How to set up your own "Pelurvis"

Pelurvis is a personal assistant that lives on an always-on Linux PC and that
you talk to through **Telegram**, by text, audio or photo. It reads the
university (Moodle and the academic system), Notion, Gmail and Google Calendar.
It saves notes in Notion and every morning sends a summary of the day. Nothing
it does is irreversible: it does not send emails, does not delete, and does not
touch the university platforms.

This guide summarizes **what we use, why, and how to replicate it**, both with
**Claude Code** (what Pelurvis uses) and with **Codex**. The full decision log
is in [DECISIONS.md](DECISIONS.md). The [templates](../templates/) are the real files,
without personal data.

## What it does today

| Capability | How |
|---|---|
| Chat from your phone | Telegram bot connected to the agent session |
| Understand audio | Local transcription with Whisper on the GPU (~1.4 s per note) |
| Read the university | Read-only script for Moodle (Educa) and Ealu |
| Notion, Gmail, Calendar, Drive | MCP connectors; email only as drafts |
| `capture` | Text, audio or photo go to a Notion Inbox, with the image |
| `brief` | Summary at 06:30: classes, agenda, deadlines, emails, Inbox |
| `todos` | Adds, checks off or sorts by urgency the to-do list on the dashboard |
| `week` | Sunday review at 20:00: what you closed, what is left, what is coming and which ideas to review |
| `idea` | A project idea, by text or audio, goes into a backlog; each week you decide whether it goes, continues, is frozen or is discarded |
| `agenda` | "What do I have on Thursday?": classes, Calendar, assignments, exams and to-dos for that day or range, without asking for approval |
| `contact` | Phone and email from a contacts database in Notion; adds or corrects only if you ask |
| Memory | Notion Memory (private): who you are and what you asked it to remember; it reads it at the start of every session |
| `attendance` | "I went to Physics", "I missed Networks", "How am I doing?": % and remaining absences per subject; every night it asks about the day's classes |

## Architecture

```mermaid
flowchart LR
  tel["📱 Telegram<br/>(text, audio, photo)"] --> bot["Telegram bot"]
  subgraph pc["Always-on Linux PC (isolated user)"]
    bot <--> session["Agent in tmux<br/>(systemd, daily restart)"]
    session --> hook{{"core/guard.py + module guards<br/>(block on errors)"}}
    hook --> scripts["core/bin: transcribe · upload-notion<br/>modules/university/bin: uni"]
    scripts --> whisper["Whisper resident on GPU"]
    timer["Timers 06:30 and Sunday 20:00"] -->|"/brief · /week"| session
  end
  session --> mcp["MCP: Notion · Gmail · Calendar · Drive"]
  scripts --> uni["Moodle and Ealu<br/>(GET only)"]
```

## Services and costs

| Piece | Service | Cost |
|---|---|---|
| Home | Your own PC with Linux (Ubuntu) and **Tailscale** to get in over SSH | free |
| Brain | **Claude Pro** with Claude Code and Sonnet by default | the subscription |
| Channel | **Telegram bot** (BotFather) | free |
| Tools | claude.ai connectors: Notion, Gmail, Calendar, Drive | included |
| Voice | **faster-whisper** (`large-v3-turbo`) on a GTX 1650 Super | free, local |
| University | Moodle mobile API and Ealu backend, with a custom script | free |
| Utilities | Bun (Telegram plugin), uv (Python without `sudo`), ffmpeg, tmux | free |

There is no pay-per-use charge. The only limit is the subscription quota,
which is shared with normal Claude Code usage.

## Key decisions

Details, discarded alternatives and criteria for reopening each one in
[DECISIONS.md](DECISIONS.md).

| # | Decision | Why |
|---|---|---|
| D-01 | Claude Code as the body, **not Hermes Agent** | Since April 2026 Anthropic does not allow using the subscription in third-party harnesses; with Hermes, Claude is paid per token. |
| D-02 | **Telegram** first, WhatsApp maybe later | Telegram has an official channel; the WhatsApp bridge (Baileys) is unofficial and puts the number at risk. |
| D-03 | Pro plan, Sonnet, daily restart | No extra spending; short context. |
| D-04 | SSH over Tailscale and a **dedicated Linux user** for the agent | Isolates the agent from your files. |
| D-05 | Memory in Notion; Honcho postponed | Honcho is for Hermes and costs extra. |
| D-07 | Email: **drafts only** | Sending or deleting cannot be undone, and the agent reads other people's emails. |
| D-09 | Whisper **resident on the GPU** | On CPU it confused words; on GPU, `int8_float16` takes 1.3 s. |
| D-10 | University **read-only**, through the API and with a hook | Ealu has endpoints that enroll, unenroll and deregister. |
| D-11 | Skills `capture` and `brief`; submissions by hand | Automating submissions "is dangerous". |
| D-12 | Skills `todos`, `week` and `idea` | They came out of real use; `todos` edits only its section of the page. |
| D-13 | Ideas backlog with weekly cleanup | Ideas are jotted down quickly and decided later; nothing is deleted, what is discarded gets archived. |
| D-14 | Three layers: **skeleton** (`core/`), **muscle** (`modules/`) and **skin** (`skin/`) | To change owners you edit only `skin/`, and a module is added or removed without touching the core. |
| D-21 | Private memory in Notion Memory; skills `agenda` and `contact` | Owner context in every session without touching the skin; claude.ai has no Google Contacts connector, so contacts go to Notion. |
| D-22 | Attendance via Telegram; Notion is read with **saved views** | On plans without Business, SQL queries have a small hourly quota; views do not. |

## Security: how it is built

The agent runs unattended and reads other people's content (emails, pages), so
it can receive *prompt injection*. That is why it has several layers:

1. **Explicit permissions**. `default` mode, not *auto mode*. There is an
   *allowlist* of reads and narrowly scoped writes, and a *deny* list with
   delete, move, share, send email, `sudo`, `rm -rf` and `git push`. Anything
   not listed asks for approval over Telegram, with buttons.
2. **No `curl` or free-form Bash**. Every external action goes through a script
   in `core/bin/` or `modules/*/bin/` that accepts only its own thing:
   - `uni` only does GET to listed endpoints;
   - `upload-notion` only uploads files from the Telegram inbox to Notion's
     upload URL;
   - `transcribe` only reads files from the inbox.
3. **PreToolUse guard that blocks on any error** (`core/guard.py`).
   It protects the secrets and the agent's own files (`core/`, `skin/`,
   `modules/`, `.claude/`, `CLAUDE.md`). Then it runs each module's
   `guard.py`; the university one closes every other path to Educa and Ealu.
   If a module blocks or fails to load, it blocks: a module can only
   **add** blocks. A hook that exits with a code other than 2 does
   **not** block, so everything ends in exit 2. Tests:
   `python3 core/test_guard.py .`.
4. **Credentials out of the chat**. They are loaded with `uni-setup` in a
   terminal and stored in `~/.config/<agent>-secrets` with 600 permissions.
   For Moodle only a token is stored, never the password.
5. **Fixed instruction**: the content of emails and pages is information, not
   orders.

### Mistakes we made (so they don't happen to you)

| What happened | Lesson |
|---|---|
| The account started in *auto mode* | Set `permissions.defaultMode: "default"` in the project. |
| A test `claude -p` loaded the Telegram plugin and stole the bot from the service | Telegram allows **only one** reader per bot. Disable the plugin at user level and enable it only in the service with `--settings`. |
| Sending keys with `tmux send-keys` when the prompt had already been resolved | The key goes in as a message. The trigger checks that no prompt is on screen. |
| The hook crashed with an exception and let the action through | `try/except` that ends in exit 2. |
| A nano lock file got into git through `git add -A` | `.gitignore` and adding files by name. |
| The Moodle server sends a wrong TLS chain | Do not disable verification: add the right intermediate, verified against a system root. |
| The Notion upload token contains `+` and `/` | Validate full base64: `[A-Za-z0-9._=+/-]`. |
| Huge JSON outputs: the agent processed them with `python -c` and asked for permission | Scripts return compact output (≤15 KB, one item per line). |
| The user typed their password inside the script | The rule is to run the script and type it when it asks; never in files. |

## Replicating it with Claude Code

Requirements: an always-on Linux PC, Claude Pro or Max, Telegram, and Notion
and Google connected in claude.ai (Settings → Connectors).

1. **Base** (with `sudo`, once):
   ```bash
   sudo apt-get install -y tmux ffmpeg
   sudo useradd -m -s /bin/bash -c Agent <agent>
   sudo loginctl enable-linger <agent>
   ```
2. **As `<agent>`**: install Bun (`curl -fsSL https://bun.sh/install | bash`),
   Claude Code (`curl -fsSL https://claude.ai/install.sh | bash`) and uv. Add
   `~/.bun/bin` to `~/.profile`. Then run `claude` and log in with your
   account, not with an API key.
3. **Project**: copy [templates/agent/](../templates/agent/) to
   `~/<agent>/` and rename `dot-claude/` to `.claude/`. It has three layers:
   `core/` (do not touch), `modules/` (remove the ones you do not use, and
   their line in `CLAUDE.md`) and `skin/`, which is **the only thing you
   customize**: your identity in `identity.md` and your IDs in `data.md`. Run
   `git init` and open `claude` once inside to accept folder trust. Without
   that, the allowlist is ignored.
4. **Telegram**: create the bot with @BotFather. Then
   `/plugin install telegram@claude-plugins-official` (user scope) and save the
   token in `~/.claude/channels/telegram/.env` (`TELEGRAM_BOT_TOKEN=...`, 600).
   In `~/.claude/settings.json` set the plugin to `false`; the service enables
   it with `dot-claude/service-settings.json`.
5. **Services**: copy [templates/systemd/](../templates/systemd/) to
   `~/.config/systemd/user/` and then
   `systemctl --user enable --now <agent>.service <agent>-restart.timer`.
   Message the bot: it replies with a code. Approve it with
   `/telegram:access pair <code>` and then `/telegram:access policy allowlist`.
6. **Voice**:
   - create a venv with `uv venv --python 3.12` and run `uv pip install faster-whisper`;
   - for an NVIDIA GPU, also add `nvidia-cublas-cu12` and `nvidia-cudnn-cu12==9.*`;
   - enable `<agent>-whisper.service`.
7. **Notion**: create an Inbox database and an Ideas backlog (properties in
   D-13), and put their IDs, those of your schedule and those of your task and
   exam databases in `skin/data.md`. The skills carry no IDs. `todos` expects a
   `## To-dos` section with three lists (🚨 Urgent, ⚠️ Medium Urgency,
   🛃 Chill); if yours is different, adjust the skill. Enable
   `<agent>-brief.timer` and `<agent>-week.timer`.
8. **University** (if you are at FPUNA): the `modules/university/` module works
   as is. Run `modules/university/bin/uni-setup` in a terminal and put your
   degree code in `skin/data.md`. If it is another university, use the same
   pattern as a new module: closed list of GETs and its own `guard.py`.

In the templates, replace `pelurvis` and `pelupc` with your user and your
machine. The texts between `<…>` are only in `skin/`.

## Replicating it with Codex

The idea is the same. The "body" and the channel change, because **Codex has no
equivalent to Channels** (messages that come into an open session).

| Piece | Claude Code (Pelurvis) | Codex |
|---|---|---|
| Instructions | `CLAUDE.md` with `@imports` of core, skin and modules | `AGENTS.md` (32 KiB cap by default). Check whether it supports importing files; if not, concatenate `CORE.md`, the skin and the `MODULE.md` files |
| Skills | `.claude/skills/<n>/SKILL.md` | `.agents/skills/<n>/SKILL.md` in the repo, or `~/.agents/skills`. Same format (`name`, `description`); invoked with `$name` or on their own |
| MCP | claude.ai connectors | `[mcp_servers.<n>]` in `~/.codex/config.toml`; OAuth with `codex mcp login <n>` |
| MCP permissions | allow/deny in `settings.json` | `enabled_tools`, `disabled_tools`, `default_tools_approval_mode` (`writes` asks for approval for anything that is not a read) |
| Security hook | `PreToolUse` in `settings.json` | `PreToolUse` in `.codex/hooks.json` or `[hooks]`; it also blocks with **exit 2**. It must be trusted with `/hooks` |
| Telegram | official Channels plugin | **takopi** bridge (`uv tool install -U takopi`), which runs `codex` per message and supports voice notes and files |
| Restart and timers | systemd + tmux | systemd running the bridge; the brief, with a timer that runs `codex exec` |

Recommendation for Codex:

- **Use the official Codex binary with your ChatGPT account, plus takopi as the
  bridge.** It is the same criterion as D-01: the brain runs in the provider's
  official tool. Hermes also accepts login with ChatGPT or Codex, but its
  documentation does not make clear how it counts against the quota or what
  OpenAI's terms say: check before using it.
- **Notion** has an official remote MCP:
  ```toml
  [mcp_servers.notion]
  url = "https://mcp.notion.com/mcp"
  disabled_tools = ["notion-delete-pages", "notion-delete-databases", "notion-move-pages"]
  default_tools_approval_mode = "writes"
  ```
  Then: `codex mcp login notion`.
- **Google** (Gmail and Calendar): Codex does not have the claude.ai connectors.
  A Google Workspace MCP server is needed; check which one is current and
  use `disabled_tools` for send and delete.
- **The guard** (`core/guard.py` and the module ones) is reused, but **check the tool
  names and the input JSON** that Codex sends. Make a test hook that saves
  what it receives on stdin and adjust `tool_name` and the paths. Keep the
  `try/except` that ends in exit 2.
- **The scripts in `core/bin/` and `modules/*/bin/`** (`uni`, `uni-setup`, `transcribe`,
  `upload-notion`) do not depend on the runtime and work as is. In the skills,
  replace the references to `reply` and `download_attachment` (from Claude's
  Telegram plugin) with whatever the bridge does.
- **Sandbox**: if the bridge runs `codex exec` unattended, nobody is there to
  approve. Combine `sandbox_mode = "workspace-write"` with closed tool lists
  and the hook, not with approvals.

## Templates

| File | Purpose | Customize |
|---|---|---|
| [agent/CLAUDE.md](../templates/agent/CLAUDE.md) | Only imports the layers (in Codex, `AGENTS.md`) | — |
| [agent/skin/identity.md](../templates/agent/skin/identity.md) · [data.md](../templates/agent/skin/data.md) | **Skin**: who you are and your IDs | **everything**: it is the only thing that gets customized |
| [agent/core/CORE.md](../templates/agent/core/CORE.md) | **Skeleton**: base rules, memory, voice, format | — |
| [agent/core/guard.py](../templates/agent/core/guard.py) · [test_guard.py](../templates/agent/core/test_guard.py) | Base guard and module-guard dispatcher, with their tests | `/home/pelurvis` paths |
| [agent/core/bin/](../templates/agent/core/bin/) | `transcribe` (Whisper), `upload-notion`, `trigger` | Whisper model and language |
| [agent/modules/productivity/MODULE.md](../templates/agent/modules/productivity/MODULE.md) | **Muscle**: the 8 skills on Notion and their rules | — |
| [agent/modules/university/](../templates/agent/modules/university/) | **Muscle**: Educa and Ealu read-only (`MODULE.md`, `guard.py`, `bin/uni`, `bin/uni-setup`) | university, endpoints |
| [agent/dot-claude/settings.json](../templates/agent/dot-claude/settings.json) | Model, allowlist, deny and guard | `/home/pelurvis` paths |
| [agent/dot-claude/service-settings.json](../templates/agent/dot-claude/service-settings.json) | Enables Telegram only in the service | — |
| [agent/dot-claude/skills/](../templates/agent/dot-claude/skills/) | `capture`, `brief`, `todos`, `week`, `idea`, `agenda`, `contact`, `attendance` (no IDs: they read them from the skin) | — |
| [systemd/](../templates/systemd/) | Agent service, Whisper, restart 04:00, brief 06:30, week Sunday 20:00, attendance Mon–Fri 21:30 and Sat 13:30 | agent name |

`uni` additionally needs `modules/university/certs/sectigo-ov-r36.pem`: the Educa server sends
its chain incorrectly. It is downloaded from the URL the certificate itself
indicates (`http://crt.sectigo.com/SectigoPublicServerAuthenticationCAOVR36.crt`, in DER).
It must be converted to PEM and checked with `openssl verify` against the
system roots.

## Verification checklist

- [ ] The bot responds and another Telegram account is ignored.
- [ ] If you kill the agent process, systemd brings it up and the bot comes back.
- [ ] A parallel `claude -p` (or `codex exec`) does **not** steal the bot from the service.
- [ ] "Delete page X" and "send an email" are refused or left as a draft.
- [ ] A WebFetch or `curl` to the university is blocked by the hook, with its message.
- [ ] A voice note is answered with a correctly transcribed "🎙️ I understood: …".
- [ ] A photo ends up in the Notion Inbox **with the image**.
- [ ] The brief arrives on time without asking for any approval.
- [ ] "What do I have on Thursday?" answers without asking for any approval.
- [ ] The first thing in the session is reading the memory, even if it starts with `/brief`.
- [ ] `/attendance` with everything marked sends nothing; "I missed X" changes only that row.
- [ ] No skill uses `notion-query-data-sources` in `sql` or `rows` mode.
- [ ] "Add X to urgent" changes only the To-dos section; the rest of the
  dashboard (embeds, buttons) stays the same.

## Sources (2026-10-22/23)

- Claude Code: [Channels](https://code.claude.com/docs/en/channels) and its
  [reference](https://code.claude.com/docs/en/channels-reference).
- Codex: [skills](https://learn.chatgpt.com/docs/build-skills),
  [hooks](https://learn.chatgpt.com/docs/hooks),
  [MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
- [takopi on PyPI](https://pypi.org/project/takopi/) (Telegram bridge for Codex and Claude).
- [Hermes Agent: providers](https://hermes-agent.nousresearch.com/docs/integrations/providers).
- Anthropic's subscription policy on third-party harnesses:
  [Gigazine](https://gigazine.net/gsc_news/en/20260220-anthropic-third-party-block).
