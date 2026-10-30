#!/usr/bin/env python3
"""MCP server (stdio) of the weather module: forecast from open-meteo.com, nothing else.

Codex launches it outside the sandbox, so this process does have network access, but it only
talks to the two fixed open-meteo URLs (geocoding and forecast): the bot gains no internet
access. One tool: `forecast(city, days)`. Standard library only.
"""
import json
import sys
import urllib.parse
import urllib.request

GEO = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST = "https://api.open-meteo.com/v1/forecast"
CODES = {0: "clear", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
         45: "fog", 48: "freezing fog", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
         61: "light rain", 63: "rain", 65: "heavy rain", 66: "freezing rain", 67: "heavy freezing rain",
         71: "light snow", 73: "snow", 75: "heavy snow", 80: "light showers", 81: "showers",
         82: "heavy showers", 95: "thunderstorm", 96: "thunderstorm with hail", 99: "severe thunderstorm with hail"}
TOOL = {
    "name": "forecast",
    "description": "Current weather and daily forecast (up to 7 days) for a city: conditions, temperatures "
                   "and chance of rain. Source: open-meteo.com.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City, for example \"Asunción, Paraguay\"."},
            "days": {"type": "integer", "minimum": 1, "maximum": 7, "description": "Forecast days (1 = today)."},
        },
        "required": ["city"],
    },
    "annotations": {"readOnlyHint": True, "openWorldHint": True},
}


def fetch(url, **params):
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=15) as r:
        return json.load(r)


def forecast(city, days=1):
    days = max(1, min(int(days or 1), 7))
    name = city.split(",")[0].strip()
    places = fetch(GEO, name=name, count=5, language="en").get("results") or []
    country = city.split(",")[1].strip().lower() if "," in city else ""
    if country:
        places = [p for p in places if country in (p.get("country") or "").lower()] or places
    if not places:
        return f"I could not find the city \"{city}\"."
    p = places[0]
    d = fetch(FORECAST, latitude=p["latitude"], longitude=p["longitude"], timezone="auto",
              forecast_days=days, current="temperature_2m,weather_code",
              daily="weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max")
    lines = [f"{p['name']}, {p.get('admin1', '')}, {p.get('country', '')}".replace(", ,", ",")]
    c = d.get("current") or {}
    if c:
        lines.append(f"Now: {c.get('temperature_2m')} °C, {CODES.get(c.get('weather_code'), 'no data')}")
    dd = d.get("daily") or {}
    for i, date in enumerate(dd.get("time", [])):
        lines.append(f"{date}: {CODES.get(dd['weather_code'][i], 'no data')}, "
                     f"{dd['temperature_2m_min'][i]}–{dd['temperature_2m_max'][i]} °C, "
                     f"rain {dd['precipitation_probability_max'][i]} %")
    return "\n".join(lines)


def reply(id_, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    if error:
        msg["error"] = {"code": -32601, "message": error}
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        try:
            m = json.loads(line)
        except ValueError:
            continue
        method, id_ = m.get("method"), m.get("id")
        if id_ is None:
            continue  # notifications (e.g. notifications/initialized)
        if method == "initialize":
            reply(id_, {"protocolVersion": (m.get("params") or {}).get("protocolVersion", "2025-06-18"),
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "weather", "version": "1.0"}})
        elif method == "tools/list":
            reply(id_, {"tools": [TOOL]})
        elif method == "tools/call":
            p = m.get("params") or {}
            try:
                if p.get("name") != "forecast":
                    raise ValueError("unknown tool")
                a = p.get("arguments") or {}
                text, error = forecast(a.get("city", ""), a.get("days", 1)), False
            except Exception as e:
                text, error = f"I could not fetch the weather: {e}", True
            reply(id_, {"content": [{"type": "text", "text": text}], "isError": error})
        elif method == "ping":
            reply(id_, {})
        else:
            reply(id_, error=f"unsupported method: {method}")


if __name__ == "__main__":
    main()
