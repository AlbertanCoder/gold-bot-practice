"""Decide whether a news headline matters to gold, and which way it pushes."""
import json
import re
from pathlib import Path

KEYWORDS_FILE = Path(__file__).with_name("keywords.json")

# group -> the (factor, score) pushes a headline in that group gives
GROUP_IMPACTS = {
    "gold": [("gold", 0.5)],
    "fed_dollar": [("usd", 0.5)],
    "inflation": [("usd", 0.25), ("risk_off", 0.25)],
    "jobs": [("usd", 0.5)],
    "geopolitics": [("risk_off", 0.5)],
    "treasury_yields": [("usd", 0.25)],
    "oil": [("risk_off", 0.25)],
}


class Keywords:
    """The compiled word lists. Build one with load_keywords()."""

    def __init__(self, groups):
        self._patterns = {}
        for name, spec in groups.items():
            flags = 0 if spec.get("case_sensitive") else re.IGNORECASE
            words = "|".join(re.escape(w) for w in spec["words"])
            self._patterns[name] = re.compile(rf"\b(?:{words})\b", flags)

    def groups_matched(self, title):
        return {name for name, pat in self._patterns.items() if pat.search(title)}

    def passes(self, title):
        return bool(self.groups_matched(title))


def load_keywords(path=KEYWORDS_FILE):
    with open(path, encoding="utf-8") as f:
        return Keywords(json.load(f))


def fallback_impacts(title, kw=None):
    """Add up every push a headline gives, one total per factor, limited to -1..+1."""
    kw = kw or load_keywords()
    totals = {}
    for group in sorted(kw.groups_matched(title)):
        for factor, score in GROUP_IMPACTS[group]:
            totals[factor] = totals.get(factor, 0.0) + score
    return {factor: max(-1.0, min(1.0, total)) for factor, total in totals.items()}
