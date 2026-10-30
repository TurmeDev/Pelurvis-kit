# Expenses module (requires the notion module)

- The owner's expenses go into the **💰 Expenses** database of the Agenda (ID in `skin/data.md`):
  Concept, Amount, Currency, Category (Food, Groceries, Transport, Home, Utilities,
  Health, Leisure, Education, Other), Date, Payment method (Cash, Debit, Credit,
  Transfer), Source (Text, Voice, Photo).
- To record an expense or answer "how much did I spend…?", use the **`expense`** skill.
- The default currency is the one in `skin/data.md`.
- Never delete an expense: if it was wrong, fix it (by changing its properties) or mark it in
  the Concept as "(voided)", and say so.
- Do not give financial or investment advice; only record and summarize what they spent.
