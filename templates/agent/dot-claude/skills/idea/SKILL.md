---
name: idea
description: Notes project ideas in the Notion Ideas Backlog and reviews them to decide whether they continue or are discarded. Use it when they say "idea:", "it occurred to me", "I have an idea for …", "project idea", describe something they want to build, ask "let's review the ideas" or answer the idea list from the weekly review ("1 go, 2 discard").
---

# Ideas Backlog

**Single** database: *💡 Ideas Backlog*
(ID in `skin/data.md`), in the dashboard's
*🏗️ Personal projects* column. Do not create pages anywhere else or
edit the project pages. Nothing is deleted: what is not useful stays as
*🗑️ Discarded*, in the Archive view.

## Noting an idea

1. **Text**: the message, or if it is audio, `download_attachment` and
   `/home/pelurvis/pelurvis/core/bin/transcribe <path>`.
2. **Create the row** with `notion-create-pages`:
   - `Idea`: the name in a few words.
   - `Pitch`: what it is, in **one** line.
   - `Status`: 🌱 New. `Reviews`: 0. `Source`: Text or Audio.
   - `Effort`: your estimate (S · a weekend, M · a few weeks, L · months).
   - `Enthusiasm`: only if the user says so.
   - Body, in this format and nothing else:
     ```
     **Problem:** …
     **For whom:** …
     **First step:** …
     ---
     <what they said, full text or transcript>
     🎙️ Automatic transcription   (only if it came from an audio)
     ```
     Fill in only what they said; what they did not say stays "—". In *First
     step* you may propose a line, marked "(suggestion)".
   - If it clearly belongs to a project that already exists in *Personal projects*,
     add a line "Project: <link>" at the end. Do not edit that project.
3. **Confirm** in one line:
   `💡 Added to backlog: <Idea> · <Effort>` and the link.

## Reviewing ideas (the cleanup)

**Candidates**: from the *in progress* view (`skin/data.md`), the
🌱 New ones, plus the 🔍 In review ones with `Reviewed` empty or 7 days old
or more. Sort them by `Logged`, from oldest to
newest, and take up to 5.

1. **Show them numbered**:
   `1. <Idea> — <Pitch> · <Effort> · logged dd/mm`. If `Reviews` is 2
   or more, add "⏳ <n+1>th time: I suggest freezing it".
2. **Ask for the decision**: "Reply by number: go / keep / freeze /
   discard". An idea with no answer is not touched.
3. **Apply** the answer with `notion-update-page` (`update_properties`):
   - **go** → ✅ Go.
   - **keep** → 🔍 In review and `Reviews` + 1.
   - **freeze** → 🧊 Frozen. **discard** → 🗑️ Discarded.
   - In all cases, `Reviewed` = today. If they state their enthusiasm ("go, very
     excited"), put it in `Enthusiasm`.
4. **Confirm** in one line per idea. If any moved to ✅ Go, ask:
   "Should I add it to To-dos (Chill) as 'Start <Idea>'?". If they say
   yes, the `todos` skill does that.

If the answer arrives and you no longer have the list in context (for example,
after the daily restart), rebuild it with the same view and the
same order, show it and **ask for confirmation** before applying.

## Rules

- If it is a question ("could X be done?"), answer it. At the end you may
  offer: "Should I add it to the backlog?".
- A note that is not a project (a reminder, a jotting) goes with
  `capture`, to the Inbox.
- Never change the `Status` unless the user decided it: proposing yes,
  deciding no.
- Do not research the idea on the internet unless they ask.
