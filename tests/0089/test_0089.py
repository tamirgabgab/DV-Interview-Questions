"""Question 0089, coins you cannot make up: the numbers the page states, recomputed from the
reference in tools/figures/q0089.py and checked against a brute force over all the amounts;
the generated blocks; the box's models under Node against the same reference."""

import itertools
import json
import sys
from functools import reduce
from math import gcd

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0089  # noqa: E402


def brute(coins, upto):
    """Every payable amount up to upto, by trying every count of every coin."""
    ok = [False] * (upto + 1)
    ranges = [range(upto // c + 1) for c in coins]
    for ks in itertools.product(*ranges):
        s = sum(k * c for k, c in zip(ks, coins))
        if s <= upto:
            ok[s] = True
    return ok


def test_payable_against_brute_force():
    for coins in [(3, 5), (4, 7), (6, 9, 20), (2, 9), (4, 6), (5, 7, 9), (4, 6, 9, 20)]:
        assert q0089.payable(coins, 70) == brute(coins, 70), coins


def test_largest_against_brute_force():
    """g by the residues = g by the plain run = the last False of a long brute-force list."""
    for coins in itertools.chain(itertools.combinations(range(2, 13), 2), itertools.combinations(range(3, 11), 3)):
        if reduce(gcd, coins) != 1:
            assert q0089.frob(coins) is None
            continue
        g = q0089.frob(coins)
        ok = brute(coins, g + 2 * max(coins))
        last = max(n for n, v in enumerate(ok) if not v) if not all(ok) else -1
        assert g == last == q0089.dp_end(coins)[0], coins


def test_two_coins_formula_count_and_symmetry():
    for a in range(2, 16):
        for b in range(a + 1, 25):
            if gcd(a, b) != 1:
                continue
            g = a * b - a - b
            assert q0089.frob((a, b)) == g
            ok = q0089.payable((a, b), g)
            assert len(q0089.unpayable((a, b))) == (a - 1) * (b - 1) // 2 == sum(not v for v in ok)
            assert all(ok[n] != ok[g - n] for n in range(g + 1)), (a, b)    # exactly one of n, g - n


def test_three_coins_have_no_symmetry():
    """The count is half of 0..g only for two coins: 3, 5, 7 has 3 unpayable of 0..4."""
    assert q0089.unpayable((3, 5, 7)) == [1, 2, 4]
    assert q0089.frob((3, 5, 7)) == 4


def test_page_numbers():
    # part a
    assert q0089.frob((3, 5)) == 7 and q0089.unpayable((3, 5)) == [1, 2, 4, 7]
    assert q0089.apery((3, 5))[0] == [0, 10, 5]
    # part b
    assert q0089.frob((4, 7)) == 17 and len(q0089.unpayable((4, 7))) == 9
    assert q0089.frob((4, 6)) is None and 4 * 6 - 4 - 6 == 14 and q0089.payable((4, 6), 14)[14]
    # part c
    dist, _, order = q0089.apery((6, 9, 20))
    assert dist == [0, 49, 20, 9, 40, 29]
    assert order == [(0, 0), (3, 9), (2, 20), (5, 29), (4, 40), (1, 49)]
    assert q0089.coins_of((6, 9, 20), 1) == [20, 20, 9]
    assert q0089.frob((6, 9, 20)) == 43 == q0089.dp_end((6, 9, 20))[0]
    assert len(q0089.unpayable((6, 9, 20))) == 22
    ok = q0089.payable((6, 9, 20), 60)
    assert all(ok[n] for n in range(38, 43)) and not ok[43]                # the run of five, then 43
    assert 6 * 9 * 20 - 6 - 9 - 20 == 1045
    # the greedy trap: 24 starts with 20 and gets stuck, 24 = 4 * 6
    assert ok[24] and not ok[24 - 20]
    # the follow-ups
    assert q0089.frob((4, 6, 9, 20)) == 11 and q0089.apery((4, 6, 9, 20))[0] == [0, 9, 6, 15]
    ways = [1] + [0] * 60
    for c in (6, 9, 20):
        for n in range(c, 61):
            ways[n] += ways[n - c]
    assert ways[60] == 5
    # the cost table
    assert [q0089.dp_end(cs) for cs in q0089.SETS] == [(7, 10), (43, 49), (13, 18), (293, 324), (3533, 3634)]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(89)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    sets = [[3, 5], [4, 7], [6, 9, 20], [4, 6, 9, 20], [5, 7, 9], [4, 6], [6, 10, 15], [1, 7], [9], [19, 20], [11, 13, 15, 17]]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(sets)}.map((c) => [m.fbFrob(c), m.fbApery(c), m.fbPayable(c, 80), m.fbGcd(c)])));")
    for coins, (g, ap, ok, d) in zip(sets, got):
        dist, last, order = q0089.apery(coins)
        want_dist = [None if x == float("inf") else x for x in dist]
        assert ap["dist"] == want_dist, coins
        assert [(s["r"], s["d"]) for s in ap["steps"]] == order, coins
        assert g == q0089.frob(coins), coins
        assert ok == q0089.payable(coins, 80), coins
        assert d == reduce(gcd, coins)
    # paying: every amount up to 120 for a few sets, against the brute force
    for coins in ([6, 9, 20], [3, 5], [4, 6], [5, 7, 9]):
        pays = node_json(f"const m = {explorer_require()};"
                         f"console.log(JSON.stringify(Array.from({{length: 121}}, (_, n) => m.fbPay({json.dumps(coins)}, n))));")
        ok = brute(coins, 120)
        for n, p in enumerate(pays):
            assert p["ok"] == ok[n], (coins, n)
            if p["ok"]:
                assert sum(c * k for c, k in p["counts"]) == n, (coins, n)
            elif reduce(gcd, coins) == 1:
                assert p["why"] == "below", (coins, n)
    greedy = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.fbGreedy([6, 9, 20], 24)));")
    assert greedy == {"counts": [[20, 1]], "left": 4}
    cases = ["6, 9, 20", "20 9 6", "3,5", "7", "4, 6, 9, 20", "1, 2, 3, 4, 5", "0, 5", "21, 4", "a, 3", "", "6,6,9"]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map((t) => m.fbParse(t))));")
    assert parsed == [[6, 9, 20], [6, 9, 20], [3, 5], [7], [4, 6, 9, 20], None, None, None, None, None, [6, 9]]
