"""Question 0052: the page's corr, expected_tosses and p_first against the generator's
exact Markov chains (tools/figures/q0052.py) for every pattern of up to 8 letters and every
race of two patterns of up to 4 letters (neither inside the other); a seeded simulation;
the page's numbers (6, 4, 14, a 1/2 race, Penney's 7/8, the follow-ups); the explorer's
JavaScript; and the page copies of the generated blocks."""

import json
import random
import sys
from fractions import Fraction as Fr
from itertools import product

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0052  # noqa: E402

ns = load_python(52)
corr, expected_tosses, p_first = ns["corr"], ns["expected_tosses"], ns["p_first"]


def words(L):
    return ["".join(t) for t in product("HT", repeat=L)]


def test_page_numbers():
    assert (expected_tosses("HH"), expected_tosses("HT"), expected_tosses("HHH")) == (6, 4, 14)
    assert p_first("HT", "HH") == Fr(1, 2) == q0052.race("HT", "HH")
    assert p_first("THH", "HHH") == Fr(7, 8)
    assert (corr("HH", "HH"), corr("HH", "HT"), corr("HT", "HT"), corr("HT", "HH")) == (6, 2, 4, 0)
    # the distributions: (t - 1) / 2^t for HT, F(t - 1) / 2^t for HH
    fib = [0, 1, 1]
    while len(fib) < 40:
        fib.append(fib[-1] + fib[-2])
    ht, hh = q0052.dist("HT", 30), q0052.dist("HH", 30)
    for t in range(1, 31):
        assert ht[t - 1] == Fr(t - 1, 2 ** t) and hh[t - 1] == Fr(fib[t - 1], 2 ** t)
    # the follow-ups: 1011 waits 18, 1111 waits 30; the variances 4 and 22; the extremes
    assert expected_tosses("HTHH") == 18 and expected_tosses("HHHH") == 30
    for p, var in (("HT", 4), ("HH", 22)):
        d = q0052.dist(p, 400)
        mean = sum(t * v for t, v in enumerate(d, 1))
        second = sum(t * t * v for t, v in enumerate(d, 1))
        assert abs(float(mean) - expected_tosses(p)) < 1e-9 and abs(float(second - mean ** 2) - var) < 1e-6
    for L in range(1, 9):
        es = [expected_tosses(w) for w in words(L)]
        assert max(es) == 2 ** (L + 1) - 2 and min(es) == 2 ** L
    # a biased coin: 1/q + 1/q^2 for HH, by the chain with q = 1/3
    assert biased_hh(Fr(1, 3)) == 3 + 9


def biased_hh(q):
    # E0 = 1 + q E1 + (1 - q) E0, E1 = 1 + (1 - q) E0  ->  E0 = (1 + q) / q^2
    return (1 + q) / q ** 2


def test_expected_matches_the_chain():
    for L in range(1, 9):
        for w in words(L):
            assert expected_tosses(w) == q0052.expected(w), w


def test_race_matches_the_chain():
    for La in range(1, 5):
        for Lb in range(1, 5):
            for a in words(La):
                for b in words(Lb):
                    if a in b or b in a:
                        continue
                    assert p_first(a, b) == q0052.race(a, b), (a, b)


def test_penney_table():
    for a in words(3):
        b, p = q0052.best_reply(a)
        assert p == 1 - p_first(a, b) and p >= Fr(2, 3)
        assert b == ("T" if a[1] == "H" else "H") + a[:2]       # the recipe on the page


def test_simulation():
    rng = random.Random(52)
    for p in ("HH", "HT", "HTH", "HHT"):
        runs, total = 20000, 0
        for _ in range(runs):
            seen = ""
            while not seen.endswith(p):
                seen = (seen + rng.choice("HT"))[-len(p):]
                total += 1
        assert abs(total / runs - expected_tosses(p)) < 0.05 * expected_tosses(p), p


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    pats = words(1) + words(2) + words(3) + ["HTHH", "HHHH", "THTHT", "HHTTHH"]
    pairs = [(a, b) for a in words(2) + words(3) for b in words(2) + words(3) if not (a in b or b in a)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([
        {json.dumps(pats)}.map((p) => [m.coinExpected(p), m.coinTable(p), m.coinDist(p, 12)]),
        {json.dumps(pairs)}.map(([a, b]) => m.coinFirst(a, b)),
      ]));""")
    for p, (e, table, d) in zip(pats, got[0]):
        assert e == expected_tosses(p)
        assert table == [[q0052.step(p, s, c) for c in "HT"] for s in range(len(p) + 1)], p
        assert all(abs(x - float(y)) < 1e-12 for x, y in zip(d, q0052.dist(p, 12))), p
    for (a, b), v in zip(pairs, got[1]):
        assert abs(v - float(p_first(a, b))) < 1e-12, (a, b)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(52)
