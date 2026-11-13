"""Question 0106: the page's single_twice, single_thrice_count, single_thrice, single_thrice_any
and single_mod_k (as published) against the references of tools/figures/q0106.py (a count of
every value, the lanes counted one by one) on random arrays of 32-bit numbers, negative ones
included, the page's examples and the edge cases (one number, zeros, the extremes of 32 bits)."""

import random
import sys

import pytest

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0106  # noqa: E402

ns = load_python(106)
single_twice, single_thrice_count, single_thrice = ns["single_twice"], ns["single_thrice_count"], ns["single_thrice"]
single_thrice_any, single_mod_k = ns["single_thrice_any"], ns["single_mod_k"]
LO, HI = -(1 << 31), (1 << 31) - 1


def arrays(seed, k, p, count=2000, vmax=None):
    """Arrays where every value appears k times but one, which appears p times, shuffled."""
    rng = random.Random(seed)
    for _ in range(count):
        span = vmax or rng.choice([3, 50, 1000, HI])
        vals = set()
        while len(vals) < rng.randint(1, 8):
            vals.add(rng.randint(max(LO, -span), min(HI, span)))
        vals = list(vals)
        single = vals[0]
        nums = [single] * p + [v for v in vals[1:] for _ in range(k)]
        rng.shuffle(nums)
        yield nums, single


def test_page_examples():
    assert single_twice(q0106.TWICE) == 4
    for f in (single_thrice_count, single_thrice, single_thrice_any):
        assert f(q0106.EXAMPLE) == 3
        assert f(q0106.NINETY_NINE) == 99
        assert f(q0106.NEGATIVE) == -4
    assert single_thrice_any(q0106.TWO_OF_THREE) == 5
    assert single_mod_k(q0106.K5, 5) == 6
    assert single_mod_k(q0106.EXAMPLE, 3) == 3 and single_mod_k(q0106.TWICE, 2) == 4


def test_twice():
    for nums, single in arrays(1060, 2, 1):
        assert single_twice(nums) == single, nums


@pytest.mark.parametrize("f", [single_thrice_count, single_thrice, single_thrice_any], ids=lambda f: f.__name__)
def test_thrice(f):
    for nums, single in arrays(1061, 3, 1):
        assert f(nums) == single, nums


def test_thrice_one_missing():
    for nums, single in arrays(1062, 3, 2):
        assert single_thrice_any(nums) == single, nums
        assert q0106.trace(nums)[-1] == (0, single)


@pytest.mark.parametrize("k", [2, 3, 4, 5, 6, 7, 8, 9, 16, 17])
def test_mod_k(k):
    rng = random.Random(1063 + k)
    for p in range(1, 2 * k + 1):
        if p % k == 0:
            continue
        for nums, single in arrays(rng.random(), k, p, count=150):
            assert single_mod_k(nums, k) == single, (k, p, nums)


def test_edge_cases():
    for f in (single_thrice_count, single_thrice, single_thrice_any):
        assert f([7]) == 7 and f([0]) == 0 and f([-1]) == -1
        assert f([LO]) == LO and f([HI]) == HI
        assert f([LO, HI, HI, LO, HI, LO, 0]) == 0
        assert f([-1, -1, -1, LO]) == LO
    assert single_twice([LO, -1, LO]) == -1
    for k in (2, 3, 4, 5, 8):
        assert single_mod_k([LO] * k + [-7], k) == -7
        assert single_mod_k([HI] * (k - 1) + [5] * k, k) == HI
