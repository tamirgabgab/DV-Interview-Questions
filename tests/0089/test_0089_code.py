"""Question 0089: the page's Python code (it runs as published) against the generator's
reference: two_coins and can_pay_two for every pair of small coins, smallest_payable,
can_pay, frobenius and frobenius_dp for many coin sets."""

import itertools
import sys
from functools import reduce
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0089  # noqa: E402

ns = load_python(89)


def test_two_coins():
    for a in range(1, 14):
        for b in range(1, 20):
            got = ns["two_coins"](a, b)
            if gcd(a, b) != 1:
                assert got is None
                continue
            assert got == (q0089.frob((a, b)), len(q0089.unpayable((a, b)))), (a, b)
            ok = q0089.payable((a, b), 3 * a * b)
            assert [ns["can_pay_two"](n, a, b) for n in range(3 * a * b + 1)] == ok, (a, b)
    assert ns["two_coins"](3, 5) == (7, 4)
    assert ns["two_coins"](6, 9) is None


def test_frobenius_and_dp():
    sets = list(itertools.combinations(range(2, 12), 2)) + list(itertools.combinations(range(3, 12), 3)) \
        + [(6, 9, 20), (4, 6, 9, 20), (31, 37, 41), (101, 103, 107), (1, 5), (11, 13, 15, 17)]
    for coins in sets:
        want = q0089.frob(coins)
        assert ns["frobenius"](list(coins)) == want, coins
        assert ns["frobenius_dp"](list(coins)) == want, coins
        if want is not None:
            dist = ns["smallest_payable"](list(coins))
            assert dist == q0089.apery(coins)[0], coins
    assert ns["frobenius"]([6, 9, 20]) == 43
    assert ns["frobenius"]([1, 5]) == -1


def test_can_pay():
    for coins in ([6, 9, 20], [3, 5], [4, 6], [5, 7, 9], [4, 6, 9, 20]):
        ok = q0089.payable(coins, 150)
        assert [ns["can_pay"](n, coins) for n in range(151)] == ok, coins
    assert not ns["can_pay"](43, [6, 9, 20]) and ns["can_pay"](44, [6, 9, 20])
    assert reduce(gcd, [4, 6]) == 2 and not ns["can_pay"](7, [4, 6])
