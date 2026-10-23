import pytest

from goldbot.discord_bot.words import direction_word, percent, plural, usd


@pytest.mark.parametrize("value, expected", [
    (-42, "-$42.00"),
    (0.004, "$0.00"),
    (1234.5, "$1,234.50"),
    (0, "$0.00"),
])
def test_usd(value, expected):
    assert usd(value) == expected


def test_usd_signed():
    assert usd(12.3, signed=True) == "+$12.30"


def test_usd_signed_must_be_named():
    with pytest.raises(TypeError):
        usd(12.3, True)


def test_percent():
    assert percent(0.667) == "67%"
    assert percent(0.667, 1) == "66.7%"


@pytest.mark.parametrize("count, expected", [(1, "1 signal"), (0, "0 signals"), (3, "3 signals")])
def test_plural(count, expected):
    assert plural(count, "signal") == expected


def test_direction_word():
    assert direction_word("buy") == "BUY"
    assert direction_word("sell") == "SELL"
