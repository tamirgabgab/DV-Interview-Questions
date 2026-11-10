"""Question 0033: the page's Python code (fifo_depth and fifo_fill, as published) on the page
numbers, against exact fractions, against the generator, against each other on random
cases (the bounds the page states), over the read clock's phase, and the explorer's
JavaScript against the Python."""

import math
import random
import sys
from fractions import Fraction

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0033  # noqa: E402

ns = load_python(33)
fifo_depth, fifo_fill = ns["fifo_depth"], ns["fifo_fill"]


def exact_depth(burst, fw, fr, idle=0):
    rate = Fraction(fr, fw) * (1 - Fraction(1, idle) if idle else 1)
    return max(1, math.ceil(burst * (1 - rate)))


def test_page_numbers():
    assert fifo_depth(120, 100, 80) == 24
    assert fifo_fill(120, 200, 250)[0] == 25
    assert fifo_depth(120, 100, 80, 4) == 48
    assert fifo_fill(120, 200, 250, 4)[0] == 48
    assert fifo_depth(64, 100, 120) == 1
    assert fifo_fill(64, 6, 5)[0] == 1                       # 100 and 120 MHz on a 1/600 us step
    # the float bugs of the old code: 40 (1 - 0.7) and 100 (1 - 0.99) are whole numbers
    assert fifo_depth(40, 100, 70) == 12 and fifo_depth(12, 60, 55) == 1 and fifo_depth(100, 100, 99) == 1
    # equal clocks: the formula's floor of one word, the simulation two (a shared edge)
    assert fifo_depth(120, 100, 100) == 1 and fifo_fill(120, 200, 200)[0] == 2


def test_phase_part_a():
    """Step 5 and the verification follow-up: the read edges `phase` steps (0.05 ns) after the
    write edges; aligned (0) gives 25, the worst; a first read edge less than 2.5 ns after
    the first write gives 24. The skipping reader of part b gives 48 at every phase."""
    got = {p: fifo_fill(120, 200, 250, 0, p)[0] for p in range(250)}
    assert got[0] == 25 and max(got.values()) == 25
    assert [p for p, v in got.items() if v == 24] == list(range(1, 50))
    assert {fifo_fill(120, 200, 250, 4, p)[0] for p in range(0, 250, 5)} == {48}


def test_matches_generator():
    for burst, fw, fr, idle in q0033.CASES:
        tw, tr = q0033.periods(fw, fr)
        assert fifo_depth(burst, fw, fr, idle) == q0033.depth(burst, fw, fr, idle) == exact_depth(burst, fw, fr, idle)
        for p in (0, tr // 3):
            assert fifo_fill(burst, tw, tr, idle, p) == q0033.fill(burst, tw, tr, idle, p)


def test_formula_exact_on_the_box_grid():
    """The box's sliders (B 4..512, rates 10..400 MHz in 5s, every skip): the closed form
    against Fraction arithmetic, sampled."""
    for burst in range(4, 513, 36):
        for fw in range(10, 401, 15):
            for fr in range(10, 401, 25):
                for idle in (0, 2, 3, 4, 5, 8, 16):
                    assert fifo_depth(burst, fw, fr, idle) == exact_depth(burst, fw, fr, idle), (burst, fw, fr, idle)


def test_simulation_against_formula():
    """Exact periods (a write every tw steps, a read every tr: the rates are tr and tw): with
    the aligned phase the simulation is the formula or one more for a continuous reader, and
    exactly one more when B (1 - f_r / f_w) is a whole number; a skipping reader skips
    floor(slots / k) reads, so it lands within one word either way. Any other phase takes at
    most one more read before the last write: the fill drops by at most one, so the aligned
    phase is the worst."""
    rng = random.Random(33)
    seen = set()
    for _ in range(600):
        tw = rng.randint(2, 40)
        tr = rng.randint(tw, 80)
        burst = rng.randint(1, 200)
        idle = rng.choice([0, 0, 2, 3, 4, 8])
        d = fifo_depth(burst, tr, tw, idle)
        s, trace = fifo_fill(burst, tw, tr, idle)
        cont = burst * (1 - Fraction(tw, tr) * (1 - Fraction(1, idle) if idle else 1))
        if idle == 0:
            assert d <= s <= d + 1, (burst, tw, tr, d, s)
            if cont.denominator == 1:
                assert s == d + 1
        else:
            assert d - 1 <= s <= d + 1, (burst, tw, tr, idle, d, s)
            seen.add(s - d)
        assert trace[0] == (0, 0) and trace[-1][1] == 0 and max(v for _, v in trace) == s
        p = rng.randint(1, tr - 1) if tr > 1 else 0
        assert s - 1 <= fifo_fill(burst, tw, tr, idle, p)[0] <= s
    assert seen == {-1, 0, 1}


def test_trace_is_consistent():
    s, trace = fifo_fill(10, 3, 4)
    for (t0, v0), (t1, v1) in zip(trace, trace[1:]):
        assert t1 >= t0 and abs(v1 - v0) == 1


def test_explorer_matches_python():
    """The box's fifoDepth (integers) against the page's fifo_depth on the slider grid, and its
    event simulation against the page's step simulation (trace and maximum) on random
    integer periods, skips and phases."""
    import json

    from page_tests import explorer_require, node_json

    grid = [(b, fw, fr, k) for b in range(4, 513, 52) for fw in range(10, 401, 35) for fr in range(10, 401, 45) for k in (0, 2, 3, 5, 16)]
    rng = random.Random(330)
    sims = []
    for _ in range(150):
        tw, tr = rng.randint(1, 30), rng.randint(1, 40)
        sims.append((rng.randint(1, 120), tw, tr, rng.choice([0, 0, 2, 3, 4, 8]), rng.randint(0, tr - 1)))
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{
        d: {json.dumps(grid)}.map(([b, fw, fr, k]) => m.fifoDepth(b, fw, fr, k)),
        s: {json.dumps(sims)}.map(([b, tw, tr, k, p]) => m.fifoFill(b, tw, tr, k, p)),
      }}));
    """)
    assert got["d"] == [fifo_depth(*c) for c in grid]
    for (burst, tw, tr, k, p), r in zip(sims, got["s"]):
        best, trace = fifo_fill(burst, tw, tr, k, p)
        assert r["max"] == best and [tuple(x) for x in r["trace"]] == trace, (burst, tw, tr, k, p)


def test_explorer_staircases():
    """The staircase box of part a (J293): the writes and the reads of the simulation as
    two step curves, the peak of the gap (writes up to a write, reads before it) equal to
    the page's fifo_fill maximum and at the last write when the reader is slower, the
    page's 120 words at 100 / 80 MHz peaking at 1,190 ns with 120 - 95 = 25 (aligned) and
    24 with the read edges 7 / 40 of a read cycle (2.19 ns) later, and the gap at any time
    the fill of the trace."""
    import json

    from page_tests import explorer_require, node_json

    cases = [(120, 100, 80, 0), (120, 100, 80, 7), (120, 100, 80, 8), (64, 200, 150, 0), (256, 100, 50, 5), (100, 100, 99, 0),
             (32, 125, 100, 30), (40, 80, 100, 0), (16, 400, 10, 0), (8, 50, 50, 0)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([b, fw, fr, p]) => {{
        const q = m.fifoPeriods(fw, fr), tW = q.tW, tR = q.tR, ph = p * tR / q.sub, s = m.fifoStairs(b, tW, tR, ph), probes = [];
        for (let k = 0; k <= 50; k++) {{ const t = Math.round(k * s.end / 50); probes.push([t, m.fifoGapAt(s, t)]); }}
        return {{ tW, tR, ph, ns: q.ns, s, probes }};
      }})));""")
    for (burst, fw, fr, p), r in zip(cases, got):
        s, tW, tR, ph = r["s"], r["tW"], r["tR"], r["ph"]
        best, trace = fifo_fill(burst, tW, tR, 0, ph)
        assert s["writes"] == [k * tW for k in range(burst)] and len(s["reads"]) == burst
        assert all((t - ph) % tR == 0 and t > 0 for t in s["reads"]) and s["reads"] == sorted(s["reads"])
        assert s["peak"]["fill"] == best == s["peak"]["w"] - s["peak"]["r"]
        if fr < fw:
            assert s["peak"]["t"] == (burst - 1) * tW and s["peak"]["w"] == burst
        for t, g in r["probes"]:
            before = [c for u, c in trace if u <= t]
            reads_at_t = sum(u == t for u in s["reads"])
            assert g["fill"] == before[-1] + reads_at_t, (burst, fw, fr, t)   # the trace is after the read of step t
    peaks = [(round(r["s"]["peak"]["t"] * r["ns"], 6), r["s"]["peak"]["w"], r["s"]["peak"]["r"], r["s"]["peak"]["fill"]) for r in got[:3]]
    assert peaks == [(1190, 120, 95, 25), (1190, 120, 96, 24), (1190, 120, 95, 25)]
