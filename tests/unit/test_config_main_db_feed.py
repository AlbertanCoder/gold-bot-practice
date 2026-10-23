import asyncio
import dataclasses
import json
from pathlib import Path

import pytest

from goldbot.config import ConfigError, Paths, load_config
from goldbot.db import get_json_state, open_db, set_json_state
from goldbot.feeds.ff_calendar import FFEvent, parse_export_json
from goldbot.main import run_post_demo

REPO = Path(__file__).resolve().parents[2]


def test_paths_under():
    p = Paths.under(Path("C:/bot"))
    assert p.db_path == Path("C:/bot") / "data" / "goldbot.db"


def test_paths_are_frozen():
    p = Paths.under(Path("C:/bot"))
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.base_dir = Path("D:/")


def test_load_config_missing_file(tmp_path):
    with pytest.raises(ConfigError, match="config file not found"):
        load_config(tmp_path)


def test_market_lookup(monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://example.invalid/hook")
    cfg = load_config(REPO, require_secrets=True)
    assert cfg.market("XAUUSD").pip_size == 0.1


def test_run_post_demo_missing_config(tmp_path):
    lines = []
    assert run_post_demo(tmp_path / "nope", out=lines.append) == 1
    assert lines[0].startswith("No demo posted: config file not found:")


def test_run_post_demo_ok(monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://example.invalid/hook")
    lines = []
    assert run_post_demo(REPO, out=lines.append) == 0
    assert lines == ["DEMO: BUY XAUUSD at $2,400.00"]


def test_json_state_round_trip(tmp_path):
    async def go():
        db = await open_db(tmp_path / "t.db")
        try:
            assert await get_json_state(db, "last_run", default={}) == {}
            await set_json_state(db, "last_run", {"usd": 0.75, "gold": 1})
            return await get_json_state(db, "last_run")
        finally:
            await db.close()

    assert asyncio.run(go()) == {"gold": 1, "usd": 0.75}


def test_parse_export_json_bytes_and_text():
    rows = [{"title": "CPI m/m", "country": "USD", "date": "2026-10-14T08:30:00-04:00",
             "impact": "High", "forecast": "0.3%", "previous": "0.2%"}]
    for content in (json.dumps(rows), json.dumps(rows).encode("utf-8")):
        events = parse_export_json(content)
        assert events == [FFEvent("CPI m/m", "USD", "2026-10-14T08:30:00-04:00", "High", "0.3%", "0.2%")]
