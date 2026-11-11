"""Question 0101: the page's Python code (it runs as published) against the generator's
references: sum_counts and same_sum on random dice, dice_pairs with faces from 1 and from 0,
cyclotomic and factor_pairs for n up to 20."""

import random
import sys
from collections import Counter

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0101  # noqa: E402

ns = load_python(101)


def test_examples():
    assert ns["same_sum"]((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8))
    assert not ns["same_sum"]((1, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6))
    assert ns["sum_counts"]((1, 2), (1, 1, 3)) == [0, 0, 2, 2, 1, 1]
    assert ns["dice_pairs"](6) == [((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)), ((1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6))]
    assert ns["factor_pairs"](4) == [((1, 2, 2, 3), (1, 3, 3, 5)), ((1, 2, 3, 4), (1, 2, 3, 4))]
    assert ns["poly_div"]([0, 0, 2, 2, 1, 1], [0, 1, 1]) == [0, 2, 0, 1]
    assert ns["poly_div"]([1, 1, 1], [1, 1]) is None


def test_sums_random():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 8)
        a = [rng.randint(0, 12) for _ in range(n)]
        b = [rng.randint(0, 12) for _ in range(n)]
        ref = Counter(x + y for x in a for y in b)
        got = ns["sum_counts"](a, b)
        assert got == [ref.get(s, 0) for s in range(max(a) + max(b) + 1)]
        assert ns["same_sum"](a, b) == q0101.same(a, b)
        assert ns["faces_of"](ns["die_poly"](a)) == tuple(sorted(a))


def test_dice_pairs():
    for n in range(1, 8):
        assert ns["dice_pairs"](n) == q0101.brute_pairs(n) == q0101.factor_pairs(n), n
    for n in range(1, 7):
        assert ns["dice_pairs"](n, low=0) == q0101.factor_pairs(n, 0), n
    assert len(ns["dice_pairs"](6, low=0)) == 5


def test_factor_pairs():
    for d in range(1, 31):
        assert ns["cyclotomic"](d) == q0101.cyclotomic(d), d
    for n in range(1, 21):
        assert ns["factor_pairs"](n) == q0101.factor_pairs(n), n
