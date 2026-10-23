"""Read the economic calendar JSON that Forex Factory publishes."""
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class FFEvent:
    title: str
    country: str
    date: str
    impact: str
    forecast: str = ""
    previous: str = ""


def parse_export_json(content: bytes | str) -> list[FFEvent]:
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    return [
        FFEvent(
            title=row["title"],
            country=row["country"],
            date=row["date"],
            impact=row["impact"],
            forecast=row.get("forecast", ""),
            previous=row.get("previous", ""),
        )
        for row in json.loads(content)
    ]
