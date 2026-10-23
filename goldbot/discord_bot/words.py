"""Small helpers that turn numbers into the words a Discord post uses."""


def percent(fraction, digits=0):
    """0.667 -> '67%'."""
    return f"{fraction * 100:.{digits}f}%"


def usd(value, *, signed=False):
    """$42.00, -$42.00, or +$12.30 when signed."""
    rounded = round(value, 2)
    if rounded == 0:
        return "$0.00"
    sign = "-" if rounded < 0 else ("+" if signed else "")
    return f"{sign}${abs(rounded):,.2f}"


def plural(count: int, word: str) -> str:
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def direction_word(direction: str) -> str:
    return "BUY" if direction == "buy" else "SELL"
