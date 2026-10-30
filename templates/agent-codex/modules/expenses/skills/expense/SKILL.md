---
name: expense
description: Records an expense in the 💰 Expenses database in Notion or answers how much the owner spent in a period or category. Use it when they say "I spent…", "I paid…", "I bought … for …", send a receipt, or ask "how much did I spend…?".
---

# Expenses

Database: 💰 Expenses (ID in `skin/data.md`). Default currency: the one in `skin/data.md`.

## Record

1. From the message (or the receipt) take: a short **Concept** ("Stock Supermarket"), the **Amount**
   as a number ("50 thousand" → 50000, "1.5 million" → 1500000, no separators or symbols),
   **Currency**, **Category** (the best fit; otherwise Other), **Date** (today if not
   stated, in the time zone from `skin/data.md`), **Payment method** if stated, **Source**
   (Voice if it came from a voice note, Photo if it is a receipt, otherwise Text).
2. If the amount is missing, ask only for that. Do not ask for the rest: leave empty what was not stated.
3. Create the row and confirm in one line, with the link:
   `💰 Recorded in Expenses (Notion): <concept> · <currency> <amount with thousands separators> · <category> · <dd/mm>`
4. If one message has several expenses, one row for each (maximum 10).

## Summarize

"How much did I spend this month?", "how much on food last week?":

1. Query the rows for the period (and the category, if stated).
2. Add up by currency. Reply briefly:
   ```
   💰 October (so far): Gs 1,250,000
   • Groceries: Gs 600,000
   • Transport: Gs 350,000
   • Other: Gs 300,000
   ```
3. No advice: only the numbers. If there are no expenses in the period, say so.
