"""How far away a stop goes, and what it costs if it is hit."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskRules:
    stop_atr_mult: float = 1.5


def stop_distance(atr14, rules):
    if not atr14 > 0:
        raise ValueError("ATR must be positive")
    return rules.stop_atr_mult * atr14


def risk_usd(distance, position_units, usd_per_quote=1.0):
    if position_units < 0:
        raise ValueError("units must not be negative")
    return distance * position_units * usd_per_quote
