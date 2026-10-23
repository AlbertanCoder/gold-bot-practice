"""Settings: where things live on disk, and which markets the bot watches."""
import json
import os
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """The settings are missing or wrong."""


@dataclass(frozen=True)
class Paths:
    base_dir: Path
    config_dir: Path
    db_path: Path

    @classmethod
    def under(cls, base_dir):
        base = Path(base_dir)
        return cls(base_dir=base, config_dir=base / "config",
                   db_path=base / "data" / "goldbot.db")


@dataclass(frozen=True)
class MarketDef:
    symbol: str
    pip_size: float


@dataclass(frozen=True)
class AppConfig:
    paths: Paths
    markets: dict
    webhook_url: str = ""

    def market(self, instrument: str) -> MarketDef:
        return self.markets[instrument]


def load_config(base_dir, require_secrets=False):
    paths = Paths.under(base_dir)
    settings_file = paths.config_dir / "settings.json"
    if not settings_file.exists():
        raise ConfigError(f"config file not found: {settings_file}")
    with open(settings_file, encoding="utf-8") as f:
        raw = json.load(f)
    markets = {name: MarketDef(**spec) for name, spec in raw["markets"].items()}
    webhook = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if require_secrets and not webhook:
        raise ConfigError("missing secret: set DISCORD_WEBHOOK_URL")
    return AppConfig(paths=paths, markets=markets, webhook_url=webhook)
