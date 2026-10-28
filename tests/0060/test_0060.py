"""Question 0060: the page's next_same / prev_same against a search number by number, for
every number in a few widths; next_zeros / prev_zeros against a search over lengths; the
page's numbers (99 after 92, 80 before 96, 143 after 120 with three zeros); the
explorer's JavaScript; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0060  # noqa: E402

ns = load_python(60)
next_same, prev_same, next_zeros, prev_zeros = ns["next_same"], ns["prev_same"], ns["next_zeros"], ns["prev_zeros"]


def test_page_examples():
    assert next_same(92, 8) == 99 and q0060.brute_next(92, 8) == 99
    assert prev_same(99, 8) == 92 and prev_same(96) == 80 == q0060.brute_prev(96, 8)
    assert next_zeros(120) == 143 == q0060.brute_next0(120) and prev_zeros(143) == 120
    assert next_zeros(92) == 99 and next_zeros(7) == 15 and prev_zeros(8) == 0 and prev_zeros(2) == 0
    assert [y for y in range(1, 40) if q0060.zeros(y) == 3][:5] == [8, 17, 18, 20, 24]
    assert next_same(0) == 0 and prev_same(0) == 0
    assert next_same(0b11100000, 8) == 0 and prev_same(0b00000111, 8) == 0
    assert next_same(0b0111111100000000, 16) == 0b1000000000111111      # the trap: 319 numbers apart


def test_against_search():
    for w in range(1, 11):
        for x in range(1 << w):
            assert next_same(x, w) == q0060.brute_next(x, w), (x, w)
            assert prev_same(x, w) == q0060.brute_prev(x, w), (x, w)
    rng = random.Random(59)
    for _ in range(300):                                  # 32 bits by default, near the top
        x = rng.getrandbits(32)
        y = next_same(x)
        assert y == 0 or (y > x and bin(y).count("1") == bin(x).count("1") and prev_same(y) == x)


def test_zeros():
    for x in range(1, 1 << 11):
        assert next_zeros(x) == q0060.brute_next0(x), x
        assert prev_zeros(x) == q0060.brute_prev0(x), x
    assert q0060.next0_rows(120)[1] == 143


def test_rows_of_the_formula():
    rows, nxt = q0060.gosper(92, 8)
    assert [v for _, v, _ in rows] == [92, 4, 96, 60, 15, 3, 99] and nxt == 99
    assert q0060.gosper(0b11100000, 8)[1] == 0


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(x, w) for w in (3, 5, 8) for x in range(1, 1 << w)] + [(x, 16) for x in random.Random(60).sample(range(1, 1 << 16), 200)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([x, w]) => [m.gsNext(x, w), m.gsPrev(x, w), m.gsNext0(x), m.gsPrev0(x),
        m.gsSteps(x, w).rows.map((r) => [r.v, r.marks]), m.gsSteps(x, w).next])));""")
    for (x, w), (nx, pv, nz, pz, rows, nx2) in zip(cases, got):
        assert nx == nx2 == q0060.brute_next(x, w) and pv == q0060.brute_prev(x, w), (x, w)
        assert nz == q0060.brute_next0(x) and pz == q0060.brute_prev0(x), x
        ref, _ = q0060.gosper(x, w)
        assert rows == [[v, sorted(m)] for _, v, m in ref], (x, w)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(60)
