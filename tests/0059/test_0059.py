"""Question 0059: the page's next_same / prev_same against a search number by number, for
every number in a few widths; rank_same against a count and unrank_same as its inverse;
the page's numbers (99 after 92, 80 before 96, 24 smaller than 92, 25 smaller than 99);
the explorer's JavaScript; and the page copies of the blocks."""

import json
import random
import sys
from math import comb

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0059  # noqa: E402

ns = load_python(59)
next_same, prev_same, rank_same, unrank_same = ns["next_same"], ns["prev_same"], ns["rank_same"], ns["unrank_same"]


def test_page_examples():
    assert next_same(92, 8) == 99 and q0059.brute_next(92, 8) == 99
    assert prev_same(99, 8) == 92 and prev_same(96) == 80 == q0059.brute_prev(96, 8)
    assert rank_same(92) == 24 == q0059.brute_rank(92) and rank_same(99) == 25
    assert comb(2, 1) + comb(3, 2) + comb(4, 3) + comb(6, 4) == 24
    assert next_same(0) == 0 and prev_same(0) == 0
    assert next_same(0b11100000, 8) == 0 and prev_same(0b00000111, 8) == 0
    assert next_same(0b0111111100000000, 16) == 0b1000000000111111      # the trap: 319 numbers apart


def test_against_search():
    for w in range(1, 11):
        for x in range(1 << w):
            assert next_same(x, w) == q0059.brute_next(x, w), (x, w)
            assert prev_same(x, w) == q0059.brute_prev(x, w), (x, w)
    rng = random.Random(59)
    for _ in range(300):                                  # 32 bits by default, near the top
        x = rng.getrandbits(32)
        y = next_same(x)
        assert y == 0 or (y > x and bin(y).count("1") == bin(x).count("1") and prev_same(y) == x)


def test_rank_and_unrank():
    for w in range(1, 11):
        for x in range(1, 1 << w):
            k = bin(x).count("1")
            assert rank_same(x) == q0059.brute_rank(x)
            assert unrank_same(rank_same(x), k) == x
    for k in range(1, 6):                                 # every place of k ones in 12 bits, in order
        xs = [unrank_same(m, k) for m in range(comb(12, k))]
        assert xs == sorted(y for y in range(1 << 12) if bin(y).count("1") == k)


def test_rows_of_the_formula():
    rows, nxt = q0059.gosper(92, 8)
    assert [v for _, v, _ in rows] == [92, 4, 96, 60, 15, 3, 99] and nxt == 99
    assert q0059.gosper(0b11100000, 8)[1] == 0


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(x, w) for w in (3, 5, 8) for x in range(1, 1 << w)] + [(x, 16) for x in random.Random(60).sample(range(1, 1 << 16), 200)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([x, w]) => [m.gsNext(x, w), m.gsPrev(x, w), m.gsRank(x),
        m.gsSteps(x, w).rows.map((r) => [r.v, r.marks]), m.gsSteps(x, w).next])));""")
    for (x, w), (nx, pv, rk, rows, nx2) in zip(cases, got):
        assert nx == nx2 == q0059.brute_next(x, w) and pv == q0059.brute_prev(x, w) and rk == q0059.brute_rank(x), (x, w)
        ref, _ = q0059.gosper(x, w)
        assert rows == [[v, sorted(m)] for _, v, m in ref], (x, w)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(59)
