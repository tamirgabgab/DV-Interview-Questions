"""Question 0032: the page's Python code (river_safe and river_plan, as published) against
the generator's enumeration."""

import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0032  # noqa: E402

ns = load_python(32)
river_safe, river_plan = ns["river_safe"], ns["river_plan"]


def test_safe():
    assert [river_safe(s) for s in range(16)] == [q0032.safe(s) for s in range(16)]


def test_plan():
    plan = river_plan()
    assert len(plan) == 7 and plan in q0032.all_solutions()
    assert plan == ["goat", None, "wolf", "goat", "cabbage", None, "goat"]
    states = q0032.replay(plan)
    assert states is not None and all(river_safe(s) for s in states)
