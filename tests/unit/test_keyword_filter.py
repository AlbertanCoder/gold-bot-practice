import pytest

from goldbot.scoring.keyword_filter import fallback_impacts, load_keywords


@pytest.fixture(scope="module")
def kw():
    return load_keywords()


class TestPrefilter:
    @pytest.mark.parametrize("title, group", [
        ("Gold climbs to record as investors seek safety", "gold"),
        ("Fed's Waller says more easing likely", "fed_dollar"),
        ("Powell signals patience on rate cuts", "fed_dollar"),
        ("US CPI inflation cools for third month", "inflation"),
        ("Payrolls beat forecasts as unemployment falls", "jobs"),
        ("Missile strike lifts tensions in the region", "geopolitics"),
        ("Treasury yields slip ahead of auction", "treasury_yields"),
        ("OPEC agrees to extend oil output cuts", "oil"),
        ("Bullion holds steady near record high", "gold"),
        ("Jobless claims rise more than expected", "jobs"),
        ("Sanctions on exporters widen", "geopolitics"),
    ])
    def test_groups(self, kw, title, group):
        assert group in kw.groups_matched(title)

    @pytest.mark.parametrize("title, expected", [
        ("Fed's Waller says more easing likely", True),
        ("Gold climbs to record as investors seek safety", True),
        # 'Fed' is case-sensitive
        ("Investors fed up with low returns", False),
        ("Local bakery wins best bread award", False),
    ])
    def test_passes(self, kw, title, expected):
        assert kw.passes(title) is expected


def test_fallback_impacts_adds_up_and_clips(kw):
    impacts = fallback_impacts("CPI inflation: Fed holds, gold jumps as war tensions grow", kw)
    assert impacts == {"gold": 0.5, "usd": 0.75, "risk_off": 0.75}


def test_fallback_impacts_empty_for_boring_news(kw):
    assert fallback_impacts("Local bakery wins best bread award", kw) == {}
