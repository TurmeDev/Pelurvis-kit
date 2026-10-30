---
name: capture
description: Saves to the Notion Inbox what the user sends so they do not forget it (text, voice note or photo, for example of the whiteboard). Use it when they say "note", "save", "capture", "remind me", or when they send a photo or an audio that is a note and not a question. Not for to-dos by urgency (`todos` skill) or project ideas (`idea` skill).
---

# Capture to the Inbox

**Single** destination: the *📥 Pelurvis Inbox* database
(ID in `skin/data.md`), inside the dashboard.
Do not write to any other database or page: not to Tasks/Assignments/Labs nor
Exam Dates. The user moves those by hand. If they ask to note it under "To-dos" or
with an urgency ("urgent", "medium", "chill"), use the `todos` skill; if it is
a project idea, the `idea` skill (it goes to the Ideas Backlog).

## Steps

1. **Get the content**:
   - Text: the message as is.
   - Audio: `download_attachment` and `/home/pelurvis/pelurvis/core/bin/transcribe <path>`.
   - Photo: `download_attachment` and look at it with `Read`. Transcribe the
     visible text or formulas and describe diagrams in one or two lines.
2. **Classify**:
   - `Type`: Task (something to do), Note (class content), Idea,
     Link, Photo (if it is mainly an image) or Other.
   - `Course`: only if it is clear. Relation to the course's Courses page;
     the URLs are in `skin/data.md`.
   - `Deadline`: only if a date is mentioned ("Thursday", "for the 30th").
     Compute it from today, in the America/Asuncion timezone.
   - `Source`: Text, Audio or Photo.
3. **Create a page** in the Inbox with `notion-create-pages`:
   - `Name`: a short, clear title (max ~8 words), not the whole text.
   - Body: the full content (text, transcript or description of the
     photo). If it came from an audio, add at the end "🎙️ Automatic transcription".
   - **If it is a photo, include the image** in the page:
     1. `notion-create-file-upload` with a short `filename` and the real
        extension of the file (e.g. `whiteboard-calculus.jpg`).
     2. `/home/pelurvis/pelurvis/core/bin/upload-notion <path> <upload_url> <token>`,
        where `<token>` is what follows `Bearer ` in
        `upload_headers.authorization`. A single command, nothing else.
     3. Put the `suggested_markdown` from the response in the body of the
        page, before the transcript.
     If the upload fails, create the page anyway with the transcript and say so.
   - Do not check `Processed`.
4. **Confirm over Telegram** in one line:
   `📥 Saved: <Name> · <Type>[ · <Course>][ · 📅 <date>]` and the link.

## Rules

- If the message is a question or a request, it is **not** a capture: answer it.
- One capture per message. If a message brings several clearly different
  things, create one page for each (max 5) and confirm them together.
- If you are unsure between two courses, set neither and say so in the confirmation.
