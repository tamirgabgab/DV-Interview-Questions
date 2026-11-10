"""Question 0033: the generator's numbers (the page example and the cases table) and the
generated blocks on the page."""

import math
import sys
from fractions import Fraction

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0033  # noqa: E402


def test_example():
    assert q0033.depth(120, 100, 80) == 24
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ)[0] == 25
    assert q0033.depth(120, 100, 80, 4) == 48
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ, 4)[0] == 48


def event_fill(burst, fw, fr, idle):
    """The simulation on rational times: writes at k / fw, read edges at j / fr (j >= 1), the
    write first on a tie; the largest fill after a write."""
    count = written = slot = top = 0
    j = 1
    while written < burst or count:
        if written < burst and Fraction(written, fw) <= Fraction(j, fr):
            count, written = count + 1, written + 1
            top = max(top, count)
            continue
        slot, j = slot + 1, j + 1
        if not (idle and slot % idle == 0) and count:
            count -= 1
    return top


def test_table_exact():
    """The table's rows: the formula against Fraction arithmetic (no float rounding: 100 words
    at 100 / 99 MHz give 1, not 2), the simulation on exact periods equal to an event
    simulation on rational times, and the rules the page states: a continuous reader gives
    the formula + 1 when B (1 - f_r / f_w) is a whole number; a skipping reader lands within
    one word either way (the last row is one below)."""
    rows = []
    for burst, fw, fr, idle in q0033.CASES:
        rate = Fraction(fr, fw) * (1 - Fraction(1, idle) if idle else 1)
        d = q0033.depth(burst, fw, fr, idle)
        assert d == max(1, math.ceil(burst * (1 - rate)))
        s = q0033.fill(burst, *q0033.periods(fw, fr), idle)[0]
        assert s == event_fill(burst, fw, fr, idle), (burst, fw, fr, idle)
        if not idle and (burst * (1 - rate)).denominator == 1:
            assert s == d + 1
        assert d - 1 <= s <= d + 1
        rows.append((d, s))
    assert rows == [(24, 25), (48, 48), (16, 17), (128, 129), (1, 2), (20, 20), (35, 34)]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(33)


def test_explorer_events_and_grid():
    """The timing strip of the box (X147): its event simulation is the fill simulation
    (the same trace and maximum) with every write and every read slot kept (burst writes,
    burst reads, the reader skipping one slot in k exactly, the read edges shifted by the
    phase), on exact integer periods (a write cycle of 1000 / f_w ns, the read cycle over the
    write cycle f_w / f_r, the phase p / 40 of a read cycle); and the integer grid of the
    WaveDrom export is the reduced ratio of the two periods when it is small, the closest
    ratio with a write cycle of at most 6 units otherwise."""
    import json

    from page_tests import explorer_require, node_json

    cases = [(120, 100, 80, 4, 0), (64, 200, 150, 0, 0), (256, 100, 50, 0, 13), (100, 100, 99, 0, 0),
             (32, 125, 100, 2, 39), (40, 105, 80, 3, 7), (16, 400, 10, 16, 20)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([b, fw, fr, idle, p]) => {{
        const q = m.fifoPeriods(fw, fr), tW = q.tW, tR = q.tR, ph = p * tR / q.sub;
        const a = m.fifoFill(b, tW, tR, idle, ph), e = m.fifoEvents(b, tW, tR, idle, ph);
        return {{ tW, tR, ph, sub: q.sub, ns: q.ns, same: JSON.stringify(a.trace) === JSON.stringify(e.trace) && a.max === e.max, e, grid: m.fifoGrid(tW, tR) }};
      }})));""")
    for (burst, fw, fr, idle, p), r in zip(cases, got):
        e, tW, tR, ph = r["e"], r["tW"], r["tR"], r["ph"]
        assert r["sub"] == 40 and abs(tW * r["ns"] - 1000 / fw) < 1e-9
        assert Fraction(tR, tW) == Fraction(fw, fr) and ph == Fraction(p * tR, 40) and 0 <= ph < tR
        assert r["same"], (burst, fw, fr, idle)
        assert e["writes"] == [k * tW for k in range(burst)]
        first = ph if ph else tR
        assert [s["t"] for s in e["slots"]] == [first + j * tR for j in range(len(e["slots"]))]
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
