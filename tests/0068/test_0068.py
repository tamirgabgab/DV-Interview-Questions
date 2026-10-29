"""Question 0068: the generator's references against the page code, the explorer's
JavaScript (the three modes of twoheaps) against the generator's traces, frame by frame
with the heap layouts, and the page copies of the generated blocks."""

import json
import random
import sys
from fractions import Fraction

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0068  # noqa: E402

ns = load_python(68)


def test_generator_matches_the_page_code():
    rng = random.Random(6800)
    for _ in range(300):
        n = rng.randint(1, 16)
        nums = [rng.randint(-4, 6) for _ in range(n)]
        num, den = rng.choice([(0, 1), (1, 1), (1, 2), (1, 4), (9, 10), (rng.randint(0, 100), 100)])
        w = rng.randint(1, 7)
        meds = [f["ans"] for f in q0068.trace_median(nums) if f["kind"] == "balance"]
        assert [Fraction(m) for m in ns["stream_medians"](nums)] == [Fraction(m) for m in meds]
        assert [f["ans"] for f in q0068.trace_quantile(nums, num, den) if f["kind"] == "target"] == ns["stream_quantiles"](nums, num, den)
        assert [f["ans"] for f in q0068.trace_window(nums, w, num, den) if f["kind"] == "target"] == ns["window_quantiles"](nums, w, num, den)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(6801)
    S = q0068.STREAM
    acases = [S, [4, 4, 4, 4], [1], [3, 2, 1, 0, -1]]
    acases += [[rng.randint(-5, 9) for _ in range(rng.randint(1, 15))] for _ in range(25)]
    bcases = [(S, 90), (S, 25), (S, 0), (S, 100), ([2, 2, 2], 50)]
    bcases += [([rng.randint(0, 9) for _ in range(rng.randint(1, 15))], rng.randint(0, 100)) for _ in range(25)]
    ccases = [(S, 4, 50), (S, 1, 50), (S, 7, 100), (list(range(12)), 2, 50), ([3, 3, 3, 3, 3, 3], 2, 0)]
    ccases += [([rng.randint(0, 6) for _ in range(rng.randint(1, 15))], rng.randint(1, 7), rng.randint(0, 100)) for _ in range(30)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([{json.dumps(acases)}.map((a) => m.thTraceMedian(a)),
        {json.dumps(bcases)}.map(([a, p]) => m.thTraceQuantile(a, p, 100)),
        {json.dumps(ccases)}.map(([a, w, p]) => m.thTraceWindow(a, w, p, 100)),
        [0, 1, 2, 3, 7, 8, 15].map((n) => m.thLevels(n)),
        [[5, 9, 10], [10, 9, 10], [4, 0, 1], [100, 7, 100]].map(([n, a, b]) => m.thRank(n, a, b))]));""")
    keys_a = ("kind", "i", "x", "low", "high", "moved")
    for nums, ev in zip(acases, got[0]):
        ref = q0068.trace_median(nums)
        assert [tuple(e.get(k) for k in keys_a) + (float(e["ans"]) if "ans" in e else None,) for e in ev] == \
            [tuple(e.get(k) for k in keys_a) + (float(e["ans"]) if "ans" in e else None,) for e in ref], nums
    keys_b = ("kind", "i", "x", "low", "high", "moved", "t", "ans")
    for (nums, p), ev in zip(bcases, got[1]):
        ref = q0068.trace_quantile(nums, p, 100)
        assert [tuple(e.get(k) for k in keys_b) for e in ev] == [tuple(e.get(k) for k in keys_b) for e in ref], (nums, p)
    keys_c = ("kind", "i", "x", "low", "high", "moved", "t", "ans", "left", "live", "dead", "pruned", "rebuilt", "gone", "gone_side")
    for (nums, w, p), ev in zip(ccases, got[2]):
        ref = q0068.trace_window(nums, w, p, 100)
        assert [tuple(json.dumps(e.get(k)) for k in keys_c) for e in ev] == [tuple(json.dumps(e.get(k)) for k in keys_c) for e in ref], (nums, w, p)
    assert got[3] == [q0068.levels(n) for n in [0, 1, 2, 3, 7, 8, 15]]
    assert got[4] == [q0068.rank_of(5, 9, 10), q0068.rank_of(10, 9, 10), q0068.rank_of(4, 0, 1), q0068.rank_of(100, 7, 100)] == [5, 9, 1, 7]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(68)
