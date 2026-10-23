"""The bot's memory: a tiny key/value table in SQLite."""
import json

import aiosqlite


async def open_db(path):
    db = await aiosqlite.connect(path)
    await db.execute("CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT)")
    await db.commit()
    return db


async def get_state(db, key: str):
    async with db.execute("SELECT value FROM state WHERE key = ?", (key,)) as cur:
        row = await cur.fetchone()
    return None if row is None else row[0]


async def set_state(db, key: str, value: str) -> None:
    await db.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)", (key, value))
    await db.commit()


async def get_json_state(db, key: str, default=None):
    raw = await get_state(db, key)
    return default if raw is None else json.loads(raw)


async def set_json_state(db, key: str, value) -> None:
    await set_state(db, key, json.dumps(value, sort_keys=True))
