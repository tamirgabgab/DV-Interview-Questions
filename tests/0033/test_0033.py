"""Question 0033: the generator's numbers (the page example and the cases table) and the
generated blocks on the page."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0033  # noqa: E402


def test_example():
    assert q0033.depth(120, 100, 80) == 24
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ)[0] == 25
    assert q0033.depth(120, 100, 80, 0.75) == 48
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ, 4)[0] == 48


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(33)


def test_explorer_events_and_grid():
    """The timing strip of the box (X147): its event simulation is the fill simulation
    (the same trace and maximum) with every write and every read slot kept (burst writes,
    burst reads, the reader skipping one slot in k exactly), and the integer grid of the
    WaveDrom export is the reduced ratio of the two periods when it is small, the closest
    ratio with a write cycle of at most 6 units otherwise."""
    import json
    from fractions import Fraction

    from page_tests import explorer_require, node_json

    cases = [(120, 100, 80, 4), (64, 200, 150, 0), (256, 100, 50, 0), (100, 100, 99, 0), (32, 125, 100, 2), (40, 105, 80, 3), (16, 400, 10, 16)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([b, fw, fr, idle]) => {{
        const tW = m.fifoSteps(fw), tR = m.fifoSteps(fr), a = m.fifoFill(b, tW, tR, idle), e = m.fifoEvents(b, tW, tR, idle);
        return {{ tW, tR, same: JSON.stringify(a.trace) === JSON.stringify(e.trace) && a.max === e.max, e, grid: m.fifoGrid(tW, tR) }};
      }})));""")
    for (burst, fw, fr, idle), r in zip(cases, got):
        e, tW, tR = r["e"], r["tW"], r["tR"]
        assert r["same"], (burst, fw, fr, idle)
        assert e["writes"] == [k * tW for k in range(burst)]
        assert [s["t"] for s in e["slots"]] == [j * tR for j in range(1, len(e["slots"]) + 1)]
        assert sum(s["read"] for s in e["slots"]) == burst
        assert all(s["idle"] == (idle > 0 and (j + 1) % idle == 0) for j, s in enumerate(e["slots"]))
        assert not any(s["idle"] and s["read"] for s in e["slots"])
        ratio, g = Fraction(tR, tW), r["grid"]
        if ratio.numerator <= 8 and ratio.denominator <= 8:
            assert (g["a"], g["b"], g["exact"]) == (ratio.denominator, ratio.numerator, True)
        else:
            best = min(abs(Fraction(max(1, round(a * ratio)), a) - ratio) for a in range(1, 7))
            assert g["a"] <= 6 and abs(Fraction(g["b"], g["a"]) - ratio) == best
            assert g["exact"] == (best == 0)
