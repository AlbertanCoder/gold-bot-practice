import pytest

from goldbot.risk import RiskRules, risk_usd, stop_distance


def test_stop_distance():
    assert stop_distance(10, RiskRules()) == 15.0


@pytest.mark.parametrize("atr", [0, -2])
def test_stop_distance_refuses_bad_atr(atr):
    with pytest.raises(ValueError, match="ATR must be positive"):
        stop_distance(atr, RiskRules())


def test_risk_usd():
    assert risk_usd(15.0, 2, 1.0) == 30.0


def test_risk_usd_refuses_negative_units():
    with pytest.raises(ValueError, match="units must not be negative"):
        risk_usd(15.0, -1)
