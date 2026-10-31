"""Question 0063: the generator's references against the page code, the explorer's
JavaScript (the three modes of slidemax) against the generator's traces, and the page
copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0063  # noqa: E402

ns = load_python(63)


def test_generator_matches_the_page_code():
    rng = random.Random(6300)
    for _ in range(300):
        n = rng.randint(1, 12)
        nums = [rng.randint(-4, 4) for _ in range(n)]
        k = rng.randint(1, n)
        assert [r["out"] for r in q0063.rows_max(nums, k) if r["out"] is not None] == ns["window_max"](nums, k)
        limit = rng.randint(0, 5)
        assert q0063.trace_limit(nums, limit)[-1]["best"] == ns["longest_within"](nums, limit)
        assert [r["out"] for r in q0063.hw_trace([v + 4 for v in nums], k)] == ns["win_max_run"]([v + 4 for v in nums], k)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(6301)
    acases = [(q0063.NUMS, 3), ([9, 8, 7, 6, 5, 10], 4), ([2, 2, 2, 2], 2)]
    acases += [([rng.randint(-5, 5) for _ in range(n)], rng.randint(1, n)) for n in (rng.randint(1, 16) for _ in range(25))]
    bcases = [(q0063.NUMS_B, 5), ([4, 2, 2, 2, 4, 4, 2, 2], 0), ([1, 2, 3, 10], 2)]
    bcases += [([rng.randint(-5, 5) for _ in range(rng.randint(1, 16))], rng.randint(0, 6)) for _ in range(25)]
    ccases = [(q0063.STREAM, 3), ([5, 5, 5, 5], 2)]
    ccases += [([rng.randint(0, 9) for _ in range(rng.randint(1, 16))], rng.randint(1, 6)) for _ in range(25)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([{json.dumps(acases)}.map(([a, k]) => m.smTraceMax(a, k)),
        {json.dumps(bcases)}.map(([a, l]) => m.smTraceLimit(a, l)),
        {json.dumps(ccases)}.map(([a, k]) => m.smTraceHw(a, k))]));""")
    for (nums, k), ev in zip(acases, got[0]):
        ref = q0063.trace_max(nums, k)
        assert [(e["kind"], e["i"], e["idx"], e["q"], e["out"]) for e in ev] == [(e["kind"], e["i"], e["idx"], e["q"], e["out"]) for e in ref], (nums, k)
    for (nums, limit), ev in zip(bcases, got[1]):
        ref = q0063.trace_limit(nums, limit)
        keys = ("kind", "right", "idx", "hi", "lo", "left", "best", "win", "measured", "gone")
        assert [tuple(e[x] for x in keys) for e in ev] == [tuple(e[x] for x in keys) for e in ref], (nums, limit)
    for (stream, k), rows in zip(ccases, got[2]):
        ref = q0063.hw_trace(stream, k)
        assert [(r["t"], r["x"], r["keep"], r["p"], r["drop"], [list(e) for e in r["before"]], [list(e) for e in r["after"]], r["out"]) for r in rows] == \
            [(r["t"], r["x"], r["keep"], r["p"], r["drop"], [list(e) for e in r["before"]], [list(e) for e in r["after"]], r["out"]) for r in ref], (stream, k)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(63)
