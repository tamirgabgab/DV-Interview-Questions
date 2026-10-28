"""Question 0061: the page's longest_ones and longest_same against every window on random
vectors and bus strings; the page's numbers (6 on 11100011110 with k = 2, 4 with k = 0,
6 on the bus with k = 2, the self-checks); the generator's traces; the explorer's
JavaScript against the generator's traces; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0061  # noqa: E402

ns = load_python(61)
longest_ones, longest_same = ns["longest_ones"], ns["longest_same"]
CHECK_A = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1]      # the self-check of part a, k = 1
CHECK_B = "ABAACAAB"                           # the self-check of part b, k = 2


def test_page_examples():
    assert longest_ones(q0061.BITS, 2) == 6 == q0061.brute_ones(q0061.BITS, 2)
    assert [longest_ones(q0061.BITS, k) for k in range(5)] == [4, 5, 6, 10, 11]
    assert longest_ones(CHECK_A, 1) == 5 == q0061.brute_ones(CHECK_A, 1)
    assert longest_same(q0061.BUS, 2) == 6 == q0061.brute_same(q0061.BUS, 2)
    assert [longest_same(q0061.BUS, k) for k in range(3)] == [3, 4, 6]
    assert longest_same(CHECK_B, 2) == 7 and longest_same(CHECK_B, 1) == 5
    assert longest_same(list(q0061.BUS), 2) == 6                  # a list works like a string
    assert longest_same(q0061.BITS, 0) == 4 == longest_ones(q0061.BITS, 0)
    assert longest_ones([], 3) == 0 and longest_same("", 1) == 0 and longest_ones([0, 0], 0) == 0
    # the best window of the figures: 4..9 flips the zeros at 4 and 5, 3..8 turns into B
    rows = q0061.trace_ones(q0061.BITS, 2)
    assert rows[-1]["win"] == (4, 9) and rows[5]["moved"] == 4 and rows[10]["moved"] == 1
    rows = q0061.trace_same(q0061.BUS, 2)
    assert rows[-1]["win"] == (3, 8) and rows[8]["top"] == "B"


def test_against_every_window():
    rng = random.Random(60)
    for _ in range(300):
        n, k = rng.randint(0, 14), rng.randint(0, 4)
        bits = [1 if rng.random() < 0.6 else 0 for _ in range(n)]
        vals = "".join(rng.choice("ABC") for _ in range(n))
        assert longest_ones(bits, k) == q0061.brute_ones(bits, k), (bits, k)
        assert longest_same(vals, k) == q0061.brute_same(vals, k), (vals, k)
        if n:
            assert q0061.trace_ones(bits, k)[-1]["best"] == longest_ones(bits, k)
            assert q0061.trace_same(vals, k)[-1]["best"] == longest_same(vals, k)
    # the left end only moves right, and the window is valid after every step
    for _ in range(50):
        bits = [rng.randint(0, 1) for _ in range(20)]
        left = 0
        for r in q0061.trace_ones(bits, 2):
            assert r["left"] >= left and r["zeros"] <= 2 and bits[r["left"]:r["right"] + 1].count(0) == r["zeros"]
            left = r["left"]


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(61)
    cases = [(q0061.BITS, 2), (CHECK_A, 1)] + [([rng.randint(0, 1) for _ in range(rng.randint(1, 16))], rng.randint(0, 3)) for _ in range(20)]
    vcases = [(q0061.BUS, 2), (CHECK_B, 2)] + [("".join(rng.choice("ABC") for _ in range(rng.randint(1, 16))), rng.randint(0, 3)) for _ in range(20)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([{json.dumps(cases)}.map(([b, k]) => m.okTraceBits(b, k)),
        {json.dumps(vcases)}.map(([v, k]) => m.okTraceSame([...v], k))]));""")
    for (bits, k), frames in zip(cases, got[0]):
        ref = q0061.trace_ones(bits, k)
        assert [(f["right"], f["left"], f["zeros"], f["moved"], f["best"], f["win"]) for f in frames] == \
            [(r["right"], r["left"], r["zeros"], r["moved"], r["best"], list(r["win"]) if r["win"] else None) for r in ref], (bits, k)
    for (vals, k), frames in zip(vcases, got[1]):
        ref = q0061.trace_same(vals, k)
        assert [(f["right"], f["left"], f["most"], f["top"], f["moved"], f["best"], f["win"]) for f in frames] == \
            [(r["right"], r["left"], max(r["count"].values()), r["top"], r["moved"], r["best"], list(r["win"]) if r["win"] else None) for r in ref], (vals, k)
        assert [{c: n for c, n in f["count"].items() if n} for f in frames] == [{c: n for c, n in r["count"].items() if n} for r in ref]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(61)
