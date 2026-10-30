---
title: Pelurvis — decision log
type: adr
status: active
summary: Dated Pelurvis decisions, each with its context, the discarded alternatives and the criterion for reopening it.
related: []
tags: [agent, decisions, claude-code, hermes, honcho, telegram, whatsapp]
updated: 2026-10-30
---

# Decision log

Each new decision is appended at the end with the next number. A reopened
decision is not edited: another one that supersedes it is added and the
original is annotated.

## D-01 — Body: headless Claude Code, not Hermes Agent

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: Hermes Agent (Nous Research, MIT) ships with a messaging
  gateway with WhatsApp, cron, memory, Honcho and a systemd service. But since
  April 2026 Anthropic does not allow using the Pro/Max subscription in
  third-party harnesses. With Hermes, Claude goes through an API key, pay per
  token; only Max with purchased extra credits is the exception, and Pro does
  not have it.
- **Decision**: Claude Code on pelupc, in tmux under systemd, with Channels,
  skills and the claude.ai connectors. It uses the subscription at no extra
  cost.
- **Discarded**: Hermes + API key (cost per token); Hermes with a cheap model
  and Claude Code only for heavy work (the brain stops being Claude).
- **Reopen if**: Channels ceases to exist or cannot handle daily use, or
  paying for the API becomes acceptable.

## D-02 — Channel: Telegram first, WhatsApp later

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: Channels includes Telegram, Discord and iMessage; WhatsApp has
  no official plugin. The Baileys bridge (WhatsApp Web) is unofficial, can
  break with updates and risks getting the number blocked. Meta's Cloud API is
  official, but requires a Meta Business account, a dedicated number and a
  public URL.
- **Decision**: Telegram with the official plugin, pairing and allowlist.
  WhatsApp, if it is still needed, in F6 as its own channel with a dedicated
  prepaid SIM, after 2–3 stable weeks.
- **Discarded for now**: WhatsApp with Baileys from the start; WhatsApp Cloud
  API.
- **Reopen if**: an official WhatsApp plugin for Channels is released.

## D-03 — Brain: Pro plan with no extra spend, Sonnet by default

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: the user has Pro and does not want a separate expense. Pro
  shares its 5-hour and weekly limits with normal Claude Code use.
- **Decision**: Sonnet as the default model, few routines, daily session reset
  to keep the context short.
- **Reopen if**: after one week, `/usage` shows that Pro is not enough.

## D-04 — Access: SSH over Tailscale

- **Date**: 2026-10-22 · **Status**: accepted
- **Decision**: the installation is done from this Windows PC with `ssh pelupc`
  over Tailscale. The agent runs under its own Linux user, `pelurvis`, which
  isolates it from personal files.

## D-05 — Memory: Notion Memory; Honcho postponed

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: Honcho (Plastic Labs) integrates with Hermes, needs its own API
  key and adds cost. The Notion connector already brings Notion Memory (an
  *About* page and a *Memories* database), and Notion is the main source.
- **Decision**: Notion Memory plus Claude Code's automatic memory.
- **Reopen if**: after 2–3 weeks of use, the agent forgets relevant context
  between sessions.

## D-06 — Mascot: original character, not Link

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: Link is owned by Nintendo.
- **Decision**: an original avatar inspired by the green-tunic hero, designed
  in Claude Design, as the bot's picture and stickers. Optional phase (F7).

## D-07 — Email: drafts only; deleting is denied

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: an unsupervised agent that reads other people's email is
  exposed to prompt injection, and sending or deleting cannot be undone.
- **Decision**: Pelurvis reads Gmail and prepares drafts; sending, replying,
  forwarding, deleting and marking as spam are in `deny`. In Notion it can
  create and edit, but not delete or move. The user sends the drafts.
- **Reopen if**: the Telegram permission relay works and sends should be
  confirmed from the phone.

## D-08 — Voice notes: local transcription with faster-whisper

- **Date**: 2026-10-22 · **Status**: superseded by D-09 (moves to GPU)
- **Context**: the user wants to send audio to the bot. The Telegram plugin
  already delivers voice and audio as an attachment, but Claude does not
  process audio.
- **Decision**: transcribe on pelupc with faster-whisper (`small`, CPU, int8,
  Spanish). It is free, the audio does not leave the machine and it takes
  seconds. A custom script that only accepts files from the channel's inbox.
- **Discarded**: cloud transcription APIs (cost and privacy); using the GPU
  (GTX 1650 Super) from the start (requires CUDA libraries).
- **Reopen if**: the quality with `small` is not enough (try `medium` or
  `large-v3-turbo`, or the GPU) or it takes too long on long audio.

## D-09 — Voice notes on GPU with a resident model

- **Date**: 2026-10-22 · **Status**: accepted · **Supersedes**: D-08
- **Context**: with `small` on CPU there were errors in the first real notes
  ("odio" for "audio", "pelo" for "Pelu", no punctuation). The user asked to
  use the GTX 1650 Super.
- **Decision**: `large-v3-turbo` on CUDA with `int8_float16`, loaded once by
  the `pelurvis-whisper` service and queried over a Unix socket. If the
  service does not respond, the script transcribes on its own on GPU; if the
  service is alive but fails, on CPU with `small`. CUDA 12 libraries (cuBLAS,
  cuDNN 9) via pip in the venv, without `sudo`.
- **Measured** (2 real notes of 3–5 s): `small` CPU ~3 s with errors;
  `large-v3-turbo` `float16` ~5 s; `int8_float16` ~1.3 s with the same text;
  with the service, ~1.4 s end to end. VRAM ~1.3 GB.
- **Reopen if**: the GPU is needed for something else (the service can be
  stopped and the script keeps working) or it fails with long audio.

## D-10 — Educa and Ealu: read-only, through the API and with a hook

- **Date**: 2026-10-22 · **Status**: accepted
- **Context**: the user wants Pelurvis to see his two FPUNA platforms, but to
  **never** submit work or enroll. The Ealu API has POST endpoints that enroll
  and unenroll from exams, withdraw from courses and split debts. Educa
  (Moodle) has the mobile API enabled. The user suggested using the browser
  with his saved passwords.
- **Decision**: defense in three layers.
  1. `bin/uni`: a client that only implements reading. Educa, with the mobile
     app token and a closed list of `get` functions. Ealu, with form login
     (the only POST) and GET to a closed list of endpoints.
  2. PreToolUse hook `uni-read-only.py`, which blocks on any error. It closes
     every other path to `una.py` (Bash, WebFetch, browser MCP), reading and
     writing credentials, and changes to hooks, permissions and `bin/`. It
     holds even if the user approves by mistake.
  3. `deny` rules in `settings.json`.
  The user loads the credentials with `uni-setup`, from the terminal, never
  through the chat. From Educa only the token is stored; from Ealu, username
  and password (600), because it has no tokens.
- **Discarded**: browser with saved passwords. Pelurvis lives on pelupc and
  not on the browser's PC; extracting passwords from the browser is not done;
  and a browser can press any button.
- **Known limitation**: the agent runs under the same Linux user that owns the
  credentials, so the barrier is the hook, not the file system. A separate
  Linux user for `uni` would close it completely (requires `sudo`).
- **Reopen if**: Pelurvis should perform any action on these platforms (not
  planned).

## D-11 — First skills: `capture` and `brief`; submissions by hand

- **Date**: 2026-10-23 · **Status**: accepted; D-12 adds the skill that edits
  "To-dos" (the `capture` rule does not change)
- **Context**: from a list of 10 candidate skills, the user chose `capture`
  and `brief` (06:30). He discarded `submissions` and `sync-submissions`: he
  prefers to handle submissions by hand because automating them "is
  dangerous".
- **Decision**:
  - `capture` writes **only** to a new database, *📥 Pelurvis Inbox*
    (one-way relation to Courses). It does not touch the dashboard's "To-dos"
    or the Tasks or Exams databases: editing that page risks breaking its
    embeds and buttons.
  - `brief` is read-only: Class schedule, Calendar, Educa due dates within 72
    h, university emails and the number of unprocessed captures.
  - Trigger: `pelurvis-brief.timer` (06:30) runs `bin/trigger /brief`, which
    writes the command into the session only if it is idle and never if an
    approval prompt is in view.
- **Reopen if**: the user asks for more sections in the brief or wants
  capture to write somewhere else.

## D-12 — Skills `todos`, `week` and `idea`

- **Date**: 2026-10-23 · **Status**: accepted; D-13 changes the destination of
  `idea` (from the Inbox to the Ideas Backlog)
- **Context**: in real use, the user twice asked by voice message to edit the
  dashboard's "To-dos" by urgency ("let's clean up the to-dos… by urgency",
  "note in medium urgency…"). Pelurvis did it well, but without a fixed
  procedure, and D-11 left that section out of `capture`. From the remaining
  list, the user chose `todos`, `week` and `idea`; he left out `notes`,
  `alerts`, `review` and `uni-mail`.
- **Decision**:
  - `todos` edits **only** the `## To-dos` section (🚨 Urgent, ⚠️ Medium
    Urgency, 🛃 Chill) with `update_content` and a single `old_str`/`new_str`
    pair. Never `replace_content`: the page arrives truncated and has a button
    that the fetch does not show, so replacing it would delete it. It adds
    only what the user names; from Educa it only reads dates.
  - `week` is read-only (To-dos, Tasks/Assignments/Labs, Exams within 14 days,
    Educa, Calendar and Inbox) and is triggered by `pelurvis-week.timer` on
    Sundays at 20:00 with `bin/trigger /week`.
  - `idea` creates a card (problem, for whom, proposal, first step, questions)
    in the Inbox with `Type` Idea. It does not touch the project pages.
  - `capture` hands off to these two skills when the request carries an
    urgency or is a project idea.
- **Reopen if**: editing To-dos breaks something on the dashboard, or the user
  wants ideas to go to a project database of their own.

## D-13 — Ideas backlog with weekly cleanup

- **Date**: 2026-10-23 · **Status**: accepted · **Supersedes**: the
  destination of `idea` in D-12
- **Context**: the user wants his project ideas in *Personal projects*, as a
  backlog with a minimal format, to pick them up during the week and clean out
  the ones not worth pursuing. In the Inbox they got mixed with captures and
  nobody reviewed them.
- **Decision**:
  - *💡 Ideas Backlog* database in the dashboard's *🏗️ Personal projects*
    column. Properties: `Idea`, `Pitch` (one line), `Status` (🌱 New,
    🔍 In review, ✅ Go, 🧊 Frozen, 🗑️ Discarded), `Effort` (S/M/L,
    estimated by Pelurvis), `Enthusiasm` (set by the user), `Source`, `Logged`,
    `Reviewed` and `Reviews`. Views: Active, By status and Archive.
  - Minimal body: problem, for whom, first step and what he said.
  - Cleanup: on Sunday, `week` lists up to 5 ideas that are new or have gone 7
    days without review, numbered. The user answers "1 go, 2 discard" and
    `idea` applies it. If an idea goes through a third time undecided,
    Pelurvis proposes freezing it, but only the user changes the status.
    Nothing is deleted: discarded ideas stay in Archive.
  - An idea that moves to ✅ Go can enter To-dos (Chill) as "Start <Idea>", if
    the user confirms.
- **Reopen if**: the backlog grows without being reviewed, or the user wants
  an approved idea to turn into a project page automatically.

## D-14 — Three layers: skeleton, muscle and skin

- **Date**: 2026-10-24 · **Status**: accepted; migrated on pelupc (`9c34f7c`)
- **Context**: the base rules, the university module and the personal data
  were mixed in `CLAUDE.md`, in the hook and in the skills (chat ID, Notion
  IDs, course URLs). Replicating the bot or changing one piece meant touching
  everything. The user asked to design the skeleton before the skin and the
  muscle.
- **Decision**:
  - **Skeleton** in `core/`: `CORE.md` (base rules), `bin/` (`transcribe`,
    `upload-notion`, `trigger`) and `guard.py`. It knows no module and no
    personal data.
  - **Muscle** in `modules/<m>/`: a `MODULE.md` imported from `CLAUDE.md`, and
    optionally `bin/`, `guard.py`, its permissions block and its timers. The
    skills stay in `.claude/skills/` because Claude Code looks for them there.
    Current modules: `productivity` and `university`.
  - **Skin** in `skin/`: `identity.md` and `data.md`. It is the **only** place
    with personal data and it is in imported Markdown, because no script needs
    the data today.
  - `CLAUDE.md` only imports (`@path`) the layers.
  - **Two-level guard**: `core/guard.py` protects the secrets and the agent's
    files, and runs the `check()` of each `modules/*/guard.py`. If one blocks
    or fails to load, it blocks: a module can only add blocks. Tested with
    33/33 cases (`core/test_guard.py`).
  - The agent also cannot edit `CLAUDE.md`, `skin/`, `core/` or `modules/`
    (deny + guard).
- **Discarded**: modules as local Claude Code plugins. They change the skill
  names (`/productivity:brief`), break the `trigger` regex and add unknowns
  about hooks and permissions. Skin as a data file (`.env` or JSON): there is
  no script yet that reads it.
- **Reopen if**: the modules grow or are shared between bots (then plugins),
  or a script needs skin data (then a file that both read).

## D-15 — Bots for third parties with Codex on pelupc: the skeleton

- **Date**: 2026-10-24 · **Status**: accepted; two bots running (bot A and bot B)
- **Context**: people close to the user want their own bot hosted on pelupc,
  with Codex. **They are not technical**: they will not use SSH or a terminal,
  only Telegram. First test with an administrator's Codex account.
- **Decision**:
  - One Linux user per bot (`bot-a`, `bot-b`), no `sudo`, with linger
    and `750` homes. Verified: a bot cannot read another's home or secrets.
  - Codex **per user** in `~/.local` (`npm -g --prefix`): updating one bot does
    not touch the others. The global Codex (the administrator's) is not used.
  - Codex login with `codex login --device-auth`: the administrator generates
    the code and the owner enters it in the browser. A terminal is never
    needed.
  - Same 3 layers as D-14 in `~/bot`. Since `AGENTS.md` does not support
    imports, `core/bin/build-agents` builds it by joining the layers; the
    administrator runs it.
  - Guard adapted to Codex's tools (`Bash` and `apply_patch`, with paths
    relative to `cwd`): 24/24 cases. The hook goes in `~/.codex/hooks.json`
    and must be **approved** in the `codex` TUI (it ends up as `trusted_hash`
    in `config.toml`). Without approval, Codex does not run it: in the first
    test it edited the core and also said it had not. `--dangerously-bypass-hook-trust`
    was discarded, because it would run any hook, including one that the agent
    managed to create.
  - Codex without approvals (`approval_policy = "never"`), `workspace-write`
    sandbox with no network and `web_search = "disabled"`, because web search
    does not go through the hooks.
  - Telegram with a **custom bridge** (`core/bin/telegram-bridge`, standard
    library only), as the `bot.service` service. takopi 0.23.4 was used first,
    but it always shows a progress message that gets edited, a header
    ("done · codex · 5s") and a footer ("ctx: …") that cannot be turned off,
    and the administrator wants Pelurvis's output: a single final reply. The
    bridge only serves the owner, shows "typing…" while working, resumes the
    conversation with `codex exec resume` (a new one with `/new` or after
    12 h) and answers voice, photos and files with a fixed phrase. The token
    moved to `~/.config/bot-secrets/telegram.env` (600), which the guard
    blocks.
  - The core forbids it from asking the owner to run commands.
  - **Plugins and connectors off** (`features.plugins`, `apps` and
    `remote_plugin` set to `false`). Codex had installed and enabled six
    plugins synced from the ChatGPT account, among them **github** and
    **notion**. With `approval_policy = "never"`, the bot could use the
    owner's connected accounts outside its modules.
  - **No subagents.** `multi_agent` and `multi_agent_v2` were already `false`
    and `spawn_agent` still worked: a subagent answered in a separate session.
    The base guard blocks `spawn_agent`, `Agent` and `followup_task` (27/27
    cases). `browser_use`, `computer_use` and `in_app_browser` were also
    turned off.
  - **`/model`** in the chat: buttons to choose the model (the account's
    visible ones, read from `~/.codex/models_cache.json`) and the reasoning
    (low, medium and high; the extreme levels are left out). It shows the
    day's tokens. Switching models mid-conversation works with `resume`.
    Measured: a minimal message costs ~9,400 input tokens because of the fixed
    context, and in a resumed conversation it grows with the history, so
    `/new` also saves tokens.
- **Verified**: over Telegram it answers with the skin's identity, refuses to
  touch the core and, in an authorized test, the guard blocked the
  `apply_patch`.
- **Audit of `exec` and the sandbox** (2026-10-24):
  - The `exec` tool (JavaScript) does not import modules ("unsupported import
    in exec") and has no `fetch`. None of the 4 attempts touched the disk; it
    only goes out through `tools.*`, which passes through the hooks.
  - Problem found: with `cwd` in `~/bot`, the sandbox allowed **writing to
    `core/`** and the only barrier was the guard's regex, which an obfuscated
    command evades. Now Codex works from `~/bot/work`: core, skin, modules and
    `AGENTS.md` are read-only for the system ("Read-only file system"), and
    Codex still reads `~/bot/AGENTS.md` from the repo root.
  - Problem found: the sandbox lets it **read the whole disk**, including
    `~/.codex/auth.json`. The `bot` permissions profile (`default_permissions`,
    `extends = ":workspace"`) denies reading `auth.json` and
    `~/.config/bot-secrets`. Tested with a command that evaded the guard using
    wildcards: "Permission denied".
  - No network, verified: `curl` does not resolve names.
- **Clock** (skeleton contract 4): a task is
  `modules/<module>/tasks/<task>.md`, and since the modules are read-only, the
  agent cannot create them. `core/bin/schedule <module>/<task> "<OnCalendar>"`
  creates `bot-task-<module>-<task>.timer`, which launches
  `bot-task@.service` → `telegram-bridge --task`. The task runs inside the
  chat's conversation, so the owner can reply to the notice, but it does not
  keep it alive. If Codex answers `NOTHING`, nothing is sent. A `flock`
  prevents the chat and a task from running Codex at the same time, and the
  state is re-read from disk before each change. Tested: a greeting arrived
  over Telegram and a task with no news sent nothing.
- **Setup with a script** (`templates/agent-codex/create-bot`): runs as the
  bot's user, without sudo, and skips what is already done. It does
  everything: Codex in `~/.local`, layers in `~/bot`, configuration, login
  with code, guard approval (through tmux, only if the screen shows exactly
  one new hook and it is ours; afterwards it checks the `trusted_hash`), token
  and owner (the owner taps "Start" and the administrator confirms who it is),
  service and final checks (guard, read-only core, unreadable credentials, no
  network). Beforehand, with sudo: `useradd` and `enable-linger`.
  - From Windows, Git Bash is not needed. The template is copied to
    `~/.create-template` in the account and run from PowerShell with
    `ssh -t <user>@pelupc '~/.create-template/create-bot "<Name>" "<owner>"'`.
    Afterwards `~/.create-template` is deleted. `install-bot` does both steps
    from a bash.
  - The approval hash is not reproducible from the hook definition (50
    variants were tried), and Codex has no command to approve.
- **Bot B** (2026-10-24) was set up with the script: service active, guard
  27/27 and reply over Telegram.
- **Reopen if**: a client needs voice, files or modules with network access.

## D-16 — Muscle in the Codex bots: the google module

- **Date**: 2026-10-24 · **Status**: accepted; tested on bot B
- **Context**: first module for the third-party bots: read the day's Gmail and
  schedule in Google Calendar with the apps the owner connected in ChatGPT.
  The skeleton (D-15) turns off plugins and apps wholesale.
- **Decision**: a Codex module has, besides `MODULE.md`:
  - `codex.toml`: its block for `~/.codex/config.toml`. `core/bin/build-config`
    joins it with `core/codex.toml` (the base now lives in the core), the same
    way `build-agents` does with `AGENTS.md`, and preserves `[hooks.state]`
    and `[tui]`.
  - `allowed`: regex of the external tools it enables. **The base guard denies
    by default every `mcp__…` tool** that no module declares, so an app that
    the account syncs on its own does not become available.
  - `guard.py`: its own blocks.
  - Each guard decision is logged in `~/.local/state/bot/guard.log` (audit,
    and a way to see the real tool names).
- **google module**, closed on three levels:
  1. Configuration: `apps._default.enabled = false`; only Gmail and Calendar,
     with `default_tools_enabled = false` and the list of tools.
  2. `allowed`: the same tools.
  3. Its guard blocks by verb: `send`, `forward`, `delete`, `trash`,
     `archive`, `respond`, `share`, bulk changes and permission changes.
  - Gmail: search, read, attachments, labels and drafts. Calendar: view,
    availability and create events. The owner's time zone is in `skin/data.md`.
- **Findings**:
  - The tools reach the hooks as `mcp__codex_apps__<app>__<tool>`
    (e.g. `mcp__codex_apps__gmail__search_email_ids`).
  - `features.apps = true` is enough: `plugins` is not needed.
  - In the configuration, an app is identified by the **connector id**
    (`connector_2128…` is Gmail, `connector_947e…` is Calendar). With the name
    (`apps.gmail`) the app disappears. The tools go by their short name
    (`tools.search_email_ids`).
  - `gmail.send_email` is **not** marked as destructive: the generic option
    `destructive_enabled = false` would not stop it. Hence the allowlist.
- **Verified**: the day's 7 emails, read; a send request had no tool ("does not
  expose any tool for sending"); tomorrow's agenda, read. Guard 29/29.
- **Pending**: confirm that the connector ids are the same across all ChatGPT
  accounts (only tested with the administrator's); move the new guard and
  `build-config` to bot A and to the setup.

## D-17 — Voice for the bots: Pelurvis's Whisper, shared

- **Date**: 2026-10-24 · **Status**: accepted
- **Context**: the Codex bots must understand voice notes like Pelurvis does
  (D-09). The GPU has 4 GB and Pelurvis's resident model takes ~1.4 GB;
  loading one per bot does not scale. The bots cannot read pelurvis's files
  nor can pelurvis read theirs (`750` homes).
- **Decision**:
  - Pelurvis's `transcribe` server opens, besides its private socket, an
    **abstract socket `@pelupc-voice`**. It receives the **audio itself** (not
    a path), up to 20 MB, and only serves the users in
    `~/pelurvis/core/voice-allowed`, verified with `SO_PEERCRED`. A single
    model on the GPU, serving one note at a time.
  - In each bot, the bridge downloads the note from Telegram, sends it to the
    socket and passes Codex the text marked "[Voice note from the owner…]".
    The core asks it to start with "🎙️ I understood: …", like Pelurvis. Codex
    never touches the socket. If the service does not respond: "I couldn't
    listen to the audio right now".
  - No `sudo` or new groups: the permission is the list of users.
- **Verified**: Pelurvis still transcribes through its socket; from
  `bot-a`, the same note in 1.3 s; an account not on the list was
  rejected. Commits `b0f3770` (Pelurvis), `2fdec39` (bot A), `94b5099`
  (bot B).
- **Cost**: a client's long audio can delay a Pelurvis note by a few seconds.
  The service logs each use: bytes and uid.
- **Setting up a new bot**: add its user to `~/pelurvis/core/voice-allowed`
  (the administrator does it as `pelurvis`; Pelurvis's agent cannot edit
  `core/`).
- **Reopen if**: the audio queue becomes noticeable in Pelurvis, or the GPU is
  needed for something else.

## D-18 — notion module: an agenda like Pelurvis's

- **Date**: 2026-10-24 · **Status**: accepted; installed on bot B
- **Context**: the administrator wants the bots to work like Pelurvis, with a
  general agenda (tasks, ideas backlog, notes) designed for a non-technical
  person. Bot B's owner connected Notion in ChatGPT and has their own
  dashboard workspace.
- **Decision**:
  - "📒 Agenda" page with three databases and one page. **✅ Tasks**: Status,
    Priority, Date, Area, Source; views Today, Next 7 days, By priority and
    Done. **💡 Ideas**: the backlog from D-13; views Active and Archive.
    **📝 Notes**: facts and jottings. **📌 About me**: the owner's context,
    which the bot only extends with the owner's confirmation.
  - Classification rule: with a day and time it goes to Google Calendar;
    something to do, to Tasks; a passing thought, to Ideas; a fact, to Notes.
    If it is not clear, a single question.
  - Nothing is ever deleted: discarded items move to "Discarded".
  - The bot installs it itself with `modules/notion/tasks/install.md`, which
    the administrator runs once, because the administrator has no access to
    the client's Notion. The IDs it returns go to `skin/data.md`.
  - Clock: `notion/brief` at 07:00 (Calendar, today's and overdue tasks, up to
    3 emails) and `notion/week` on Sunday at 20:00 (closed, pending, what's
    coming and up to 5 ideas to decide). If there is nothing, they answer
    `NOTHING`.
- **Finding**: for Notion (`asdk_app_69c18c28…`), Codex **does not apply** the
  per-tool filter: no `tools.<tool>` key had any effect. So the app goes in
  whole, with `default_tools_approval_mode = "approve"`, and the real filter is
  the guard:
  - `allowed` only lets it search, read, query databases, create pages, change
    properties and create databases and views;
  - the module's guard blocks by verb (delete, move, duplicate, agent
    sessions, skills, Notion calendar, schema) and `replace_content` or
    `allow_deleting_content` in `notion_update_page`.
  Tested: 6 of 6 blocks.
- **Cost**: the installation used ~1.1 M input tokens (94% cached). It happens
  only once.

## D-19 — Skills per module in the Codex bots, and a new conversation when instructions change

- **Date**: 2026-10-24 · **Status**: accepted
- **Context**: bot B logged a submission only in Calendar and replied
  "Done, noted" without saying where. Two causes:
  1. The conversation had started **before** the notion module. Codex loads
     `AGENTS.md` when a conversation starts, and when resuming it (`resume`)
     it keeps the old instructions.
  2. The agenda rules were general text, not a fixed procedure like
     Pelurvis's skills.
- **Decision**:
  - The bridge keeps a fingerprint of `AGENTS.md` and the skills. If they
    change, it starts a new conversation: an administrator's change takes
    effect from the next message.
  - Each module brings its skills in `modules/<m>/skills/<s>/SKILL.md`.
    `build-agents` links them into **`~/.agents/skills`** (user scope). In
    `~/bot/.agents/skills` (repo scope) Codex only sees them if launched from
    `~/bot`; the bot runs from `work/` and did not load them (verified with
    `codex debug prompt-input`). `~/.agents` is outside what the sandbox lets
    it write ("Read-only file system"), and the guard protects it.
  - notion module: `note` (classifies and **always** says which database it
    ended up in, with a link), `agenda`, `update` (never deletes: Discarded)
    and `review-ideas`. `MODULE.md` stays short: structure, rules and which
    skill to use.
  - Corrected rule: something to do with a date goes to **Tasks** even if it
    has a time, plus a 15-minute reminder in Calendar if a time was given.
    Without a time, it does not ask. Only meetings, appointments and
    shifts go to Calendar alone.
- **Verified**: Codex lists the 4 skills from `work/`; guard 31/31.

## D-20 — Modules contacts, drive, weather and expenses (and photos, pending)

- **Date**: 2026-10-24 · **Status**: accepted; installed on bot B
- **contacts** and **drive**: Google Contacts and Drive read-only, with a
  per-tool filter in `codex.toml` (they are `connector_…` connectors) and
  `allowed`; drive also blocks by verb create, edit, share and delete. Tested:
  Drive lists recent files and does not offer the create tool.
- **weather**: custom MCP server (`modules/weather/server.py`, standard library
  only) that queries only open-meteo.com. Codex launches it outside the
  sandbox, so the bot still has no network. MCP tools are loaded on demand,
  which is why the `weather` skill is needed for the model to find it.
  `build-config` replaces `__HOME__` in the modules' blocks. Default city in
  `skin/data.md`.
- **expenses**: 💰 Expenses database inside the Agenda (installed with
  `modules/expenses/tasks/install.md`) and `expense` skill (log and summarize
  by period or category, no financial advice). Default currency in the skin.
- Guard: `2>/dev/null` no longer counts as a write (it was a false positive).
  33/33.
- **Pending: photos and documents.** The bridge must download them to
  `work/inbox/`, and Codex reads them with `view_image`, or with `pdftotext`,
  `pdftoppm` and `tesseract` (installed and available in the sandbox). To put
  the image in Notion, `notion_create_file_upload` gives an upload URL that
  requires a multipart POST. The sandbox has no network, so the upload has to
  be done by the bridge or a script outside the sandbox, like `upload-notion`
  in Pelurvis.
- Earlier pending items: confirm the connector ids with another account
  (bot A, new account); test contacts with a real name.

## D-21 — Private memory in Notion Memory; skills `agenda` and `contact`

- **Date**: 2026-10-29 · **Status**: accepted; `contact` awaits the initial
  import
- **Context**: compared with the Codex bots (D-15 to D-20), the owner wants
  three things for Pelurvis: contacts, an "about me" so it has context on who
  he is, and checking the agenda for any day without approvals. The rest
  (expenses, weather, `/model`…) is left to think over to fit his needs.
- **Decision**:
  - **About me = Notion Memory**, as D-05 already said, and **private**: the
    workspace has only one person. Pelurvis reads it **first thing in every
    session**, before any other tool, even if it starts with a skill. It saves
    only with "remember…" or with the owner's yes, never copies it elsewhere,
    and does not save health, finances or relationships unless asked. The
    rules live in `CORE.md`, because memory belongs to the skeleton (contract
    5). This completes F4.
  - **Contacts**: claude.ai has no Google Contacts connector, so they go in a
    **👥 Contacts** database on the dashboard (Name, Phone, Email, Group,
    Organization, Birthday, Notes), with the initial load imported from the
    Google CSV. `contact` skill: searches, gives the email to drafts and
    events, and adds or corrects only if the owner asks; never deletes.
  - **`agenda`**: any day or range, with classes, Calendar,
    Tasks/Assignments/Labs, Exam dates and the dashboard's To-dos. No Educa:
    for "what do I have to submit?" the university module still applies. It
    only reads, and all its tools were already on the allowlist.
    `Bash(date:*)` was added, because the date cannot be deduced from the
    session.
- **Finding**: with the rule "on the session's first message", a freshly
  restarted `/agenda` did **not** read the memory: the skill took control.
  With "before any other tool, even a skill" it does read it first.
- **Verified** (2026-10-29): guard 33/33. `/agenda` without a date answered
  tomorrow over Telegram in ~20 s, with no approvals, and the first thing was
  `notion-fetch memory`. Commits `dc82983` and `231cdf5`.
- **Pending**: import the Google Contacts CSV and test `contact` from the
  phone; fill in the memory with the owner.
- **Reopen if**: a Google Contacts connector appears, or reading the memory in
  every session weighs on the Pro quota.

## D-22 — Attendance by Telegram, and Notion read through views

- **Date**: 2026-10-29 · **Status**: accepted
- **Context**: the owner wants to track attendance from Telegram by
  reusing an existing attendance database in Notion: one row per
  class held, with `Status` (Attended, Missed, Excused, Pending) and the
  relation to the course. While reviewing it, Notion's
  SQL query quota ran out.
- **Decision**:
  - `attendance` skill: marks ("I went to…", "I missed…", "today I went to all
    of them", an announced absence as Excused with the reason in `Notes`),
    creates the row if missing (with data from the Schedule) and queries the %
    and the absences left per course. Minimum **75%** in the skin; ⚠️ warning
    below 80% or with 2 absences or fewer remaining, and 🚨 below the minimum.
    Never deletes.
  - **Reminder**: `pelurvis-attendance.timer` triggers `/attendance` Monday to
    Friday at 21:30 and Saturdays at 13:30. If there are classes today in
    Pending, it asks; otherwise it sends nothing.
  - **Notion through views**: on the owner's plan, the `sql` and `rows` mode
    of `notion-query-data-sources` has a small quota, shared by the workspace
    and replenished every hour; `view` mode does not. Seven "Pelurvis · …"
    views (schedule; open or recent tasks; pending or recent exams;
    unprocessed Inbox; ideas in progress; attendance ±7-day window and all),
    with relative dates (`one_week_ago`…). Their URLs go in the skin.
    `CORE.md` forbids `sql` and `rows`; `brief`, `week`, `idea`, `agenda` and
    `attendance` read through views, and `contact` searches with
    `notion-search`.
- **Alternatives**: Notion Business (more quota, with a cost); keep using SQL
  and say "I couldn't read it" when the quota runs out.
- **Reopen if**: the next semester uses another attendance database, or a view
  is not enough for a frequent question.

## D-23 — Complete private repo and generated public mirror

- **Date**: 2026-10-30 · **Status**: accepted
- **Context**: the shareable material (guide, templates and this log) lived
  alongside documents that name the workspace and contain personal data. The
  package was put together by hand in a `.rar` that went stale after every
  change, and publishing the whole folder in a public repo was risky.
- **Decision**:
  - Two sibling folders: `Pelurvis` (**private** repo, everything as is, as a
    backup) and `Pelurvis-kit` (**public** repo, generated; never edited by
    hand).
  - A script in the private repo copies only an allowlist (the guide, the templates,
    `docs/DECISIONS.md` and a public README of its own), deletes from the
    mirror whatever is no longer in the source and runs a list of forbidden
    patterns (IDs, users, emails and credentials) plus
    the marker check. On a hit it exits with an error and warns not to
    publish.
  - The script does not commit or push: the `git diff` is reviewed and
    published by hand to both repos.
  - Shareable material is cleaned at the source, not only in the mirror.
- **Discarded alternatives**: a `.gitignore` in a single repo, because it does
  not exclude individual lines and history is permanent (a piece of data that
  slips in stays forever); keeping the `.rar`, which goes stale and depends on
  the memory of whoever assembles it.
- **Reopen if**: the allowlist grows enough to need per-file rules, or the
  public history must be rewritable.

## D-24 — The public kit is in English

- **Date**: 2026-10-30 · **Status**: accepted
- **Context**: the kit is meant for anyone, not only Spanish speakers. The
  private repo stays in Spanish because that is the owner's working language.
- **Decision**:
  - The public kit is a hand-maintained English translation, including file,
    folder, skill and command names (`core/`, `modules/`, `skin/`,
    `/capture`, `/todos`…). A fixed glossary keeps the names consistent.
  - The publish script maps each English file to its Spanish source and stores
    the source's hash at translation time. If a source changes later, it warns
    that the translation is stale.
  - The README is written for people arriving at the repo, not for the owner.
- **Discarded alternatives**: publishing in Spanish (smaller audience);
  translating the private repo too (it would change the working bot and the
  owner's daily language).
- **Reopen if**: keeping two languages in sync costs more than it is worth.
