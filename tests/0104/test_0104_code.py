"""Question 0104: the page's start_naive, start_one_pass, start_at_min and good_starts (as
published) against the references of tools/figures/q0104.py (every start driven around the
ring) on random rings, the page's examples and the edge cases (one station, every d zero,
a ring with no start, ties at the minimum)."""

import random
import sys

import pytest

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0104  # noqa: E402

ns = load_python(104)
start_naive, start_one_pass = ns["start_naive"], ns["start_one_pass"]
start_at_min, good_starts = ns["start_at_min"], ns["good_starts"]
FUNCS = [start_naive, start_one_pass, start_at_min]


def rings(seed, count=3000, nmax=9, vmax=6):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(1, nmax)
        yield [rng.randint(0, vmax) for _ in range(n)], [rng.randint(0, vmax) for _ in range(n)]


def first(gas, cost):
    g = q0104.good(gas, cost)
    return g[0] if g else -1


def test_page_examples():
    for f in FUNCS:
        assert f(*q0104.EXAMPLE) == 3
        assert f(*q0104.NONE) == -1
        assert f(*q0104.ZERO) == 0
        assert f(*q0104.MORE) == 1
    assert good_starts(*q0104.EXAMPLE) == [3]
    assert good_starts(*q0104.NONE) == []
    assert good_starts(*q0104.ZERO) == [0, 2, 4, 5]
    assert good_starts(*q0104.MORE) == [1, 3, 4]


@pytest.mark.parametrize("f", FUNCS, ids=lambda f: f.__name__)
def test_first_start_on_random_rings(f):
    for gas, cost in rings(1040):
        assert f(gas, cost) == first(gas, cost), (gas, cost)


def test_good_starts_on_random_rings():
    for gas, cost in rings(1041):
        assert good_starts(gas, cost) == q0104.good(gas, cost), (gas, cost)


def test_edge_cases():
    for f in FUNCS:
        assert f([1], [2]) == -1
        assert f([2], [2]) == 0
        assert f([5], [1]) == 0
        assert f([0, 0, 0], [0, 0, 0]) == 0
        assert f([1, 0], [0, 1]) == 0          # a tie at the minimum: the first station
        assert f([0, 1], [1, 0]) == 1
    assert good_starts([1], [2]) == []
    assert good_starts([2], [2]) == [0]
    assert good_starts([0, 0, 0], [0, 0, 0]) == [0, 1, 2]
    assert good_starts([1, 0], [0, 1]) == [0]
    assert good_starts([2, 0, 1], [0, 1, 1]) == [0, 2]
