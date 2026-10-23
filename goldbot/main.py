"""The bot's front door. Here it only builds a demo post; nothing is sent anywhere."""
from goldbot.config import ConfigError, load_config
from goldbot.discord_bot.words import direction_word, usd


def run_post_demo(base_dir, out=print):
    try:
        cfg = load_config(base_dir=base_dir, require_secrets=True)
    except ConfigError as exc:
        out(f"No demo posted: {exc}")
        return 1
    gold = cfg.market("XAUUSD")
    out(f"DEMO: {direction_word('buy')} {gold.symbol} at {usd(2400)}")
    return 0
