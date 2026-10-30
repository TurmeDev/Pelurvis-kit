---
name: weather
description: Current weather and forecast for up to 7 days. Use it when the owner asks about the weather, the temperature, whether it will rain, whether it is cold or hot, or what to wear, today or in the coming days.
---

# Weather

1. Call the **`forecast` tool of the `weather` MCP server** (`weather.forecast`).
   Do not use the shell or the internet: you have no network, and that tool is the only source.
   - `city`: the one the owner named; if they named none, the "City" in `skin/data.md`.
   - `days`: 1 for today, 2 if they ask about tomorrow, up to 7 for the week.
2. Reply briefly, without tables:
   `🌦️ <city>: now <temp> °C, <conditions>. Tomorrow: <conditions>, <min>–<max> °C, rain <%>.`
   If the chance of rain is 50% or more, add "☔ bring an umbrella".
3. If the tool fails, say so in one line; do not invent the forecast.
