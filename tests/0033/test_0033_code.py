"""Question 0033: the page's Python code (fifo_depth and fifo_fill, as published) on the page
numbers, against the generator, against each other on random cases, and the explorer's
JavaScript against the Python."""

import math
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0033  # noqa: E402

ns = load_python(33)
fifo_depth, fifo_fill = ns["fifo_depth"], ns["fifo_fill"]


def steps(f_mhz):
    return round(1000 / f_mhz / q0033.UNIT)


def test_page_numbers():
    assert fifo_depth(120, 100, 80) == 24
    assert fifo_fill(120, steps(100), steps(80))[0] == 25
    assert fifo_depth(120, 100, 80, 0.75) == 48
    assert fifo_fill(120, steps(100), steps(80), 4)[0] == 48
    assert fifo_depth(64, 100, 120) == 1
    assert fifo_fill(64, steps(100), steps(120))[0] == 1


def test_matches_generator():
    for burst, fw, fr, idle in q0033.CASES:
        duty = 1 - 1 / idle if idle else 1.0
        assert fifo_depth(burst, fw, fr, duty) == q0033.depth(burst, fw, fr, duty)
        assert fifo_fill(burst, steps(fw), steps(fr), idle) == q0033.fill(burst, steps(fw), steps(fr), idle)


def test_simulation_against_formula():
    """Exact periods (the step counts themselves are the rates): the simulation is the
    formula or one more for a continuous reader; a skipping reader skips floor(slots / k)
    reads, which is not exactly a quarter, so it can land up to two away on either side."""
    rng = random.Random(33)
    for _ in range(300):
        tw = rng.randint(2, 40)
        tr = rng.randint(tw, 80)
        burst = rng.randint(1, 200)
        idle = rng.choice([0, 0, 2, 3, 4, 8])
        duty = 1 - 1 / idle if idle else 1.0
        d = fifo_depth(burst, 1 / tw, 1 / tr, duty)
        s, trace = fifo_fill(burst, tw, tr, idle)
        assert (d <= s <= d + 1) if idle == 0 else (d - 2 <= s <= d + 2), (burst, tw, tr, idle, d, s)
        assert trace[0] == (0, 0) and trace[-1][1] == 0 and max(v for _, v in trace) == s


def test_trace_is_consistent():
    s, trace = fifo_fill(10, 3, 4)
    for (t0, v0), (t1, v1) in zip(trace, trace[1:]):
        assert t1 >= t0 and abs(v1 - v0) == 1


def test_explorer_matches_python():
    from page_tests import explorer_require, node_json

    cases = [(120, 100, 80, 0), (120, 100, 80, 4), (64, 200, 150, 0), (256, 100, 50, 0), (32, 125, 100, 2), (10, 100, 300, 0)]
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {[list(c) for c in cases]};
      console.log(JSON.stringify(cases.map(([b, fw, fr, idle]) => {{
        const r = m.fifoFill(b, m.fifoSteps(fw), m.fifoSteps(fr), idle);
        return [m.fifoDepth(b, fw, fr, idle ? 1 - 1 / idle : 1), r.max, r.trace.length, r.trace[r.trace.length - 1]];
      }})));
    """)
    for (burst, fw, fr, idle), (d, s, n, last) in zip(cases, got):
        duty = 1 - 1 / idle if idle else 1.0
        assert d == fifo_depth(burst, fw, fr, duty)
        py_s, py_trace = fifo_fill(burst, steps(fw), steps(fr), idle)
        assert s == py_s and n == len(py_trace) and tuple(last) == py_trace[-1]
