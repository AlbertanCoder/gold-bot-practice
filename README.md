# gold-bot-practice

A small, safe Python project for learning. It is the practice project for the Python module of the free
[Hackathon Sim course](https://albertancoder.github.io/hackathon-sim/). It is shaped like a real Discord bot
that reads gold-market news, but it sends nothing anywhere and trades nothing.

## Get it running

Windows PowerShell (the course uses the same steps on Mac and Linux, with `python3` and `source .venv/bin/activate`):

```
git clone https://github.com/AlbertanCoder/gold-bot-practice projects/gold-bot
cd projects/gold-bot
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -q
```

You should see `41 passed`.

## What is in it

| File | What it holds |
| --- | --- |
| `goldbot/discord_bot/words.py` | `percent`, `usd`, `plural`, `direction_word` |
| `goldbot/risk.py` | `stop_distance`, `risk_usd` |
| `goldbot/scoring/keyword_filter.py` | `load_keywords`, `passes`, `groups_matched`, `fallback_impacts` |
| `goldbot/config.py` | `Paths`, `AppConfig`, `ConfigError`, `load_config` |
| `goldbot/main.py` | `run_post_demo` |
| `goldbot/db.py` | `get_json_state`, `set_json_state` (SQLite through aiosqlite) |
| `goldbot/feeds/ff_calendar.py` | `parse_export_json` |
| `tests/unit/` | the tests the lessons ask you to read and extend |

Every function here is quoted in a lesson, and every answer in the lessons was run against this code.

## Licence

MIT. Use it, change it, break it on purpose.
