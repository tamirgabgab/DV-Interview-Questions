"""Question 0108: the page's min_flips_naive, min_flips, min_flips_inplace, min_flips_2d_naive and
min_flips_2d (as published) against the brute force of tools/figures/q0108.py (every set of
window starts) on every array of up to 12 bits and every k (all sets of starts at once, q0108.table), on random longer arrays, and on every
grid of up to 4 x 4 and random larger grids; the in-place version must give the array back."""

import random
import sys
from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0108  # noqa: E402

ns = load_python(108)
naive, fast, inplace = ns["min_flips_naive"], ns["min_flips"], ns["min_flips_inplace"]
naive2, fast2 = ns["min_flips_2d_naive"], ns["min_flips_2d"]


def check_row(a, k, want):
    copy = list(a)
    assert naive(copy, k) == want and copy == a, (a, k)
    assert fast(copy, k) == want and copy == a, (a, k)
    assert inplace(copy, k) == want and copy == a, (a, k)     # the marks are wiped, also on -1


def test_examples():
    assert fast(q0108.EXAMPLE, 3) == 3
    assert fast(*q0108.ONE_ZERO) == 2 and fast(*q0108.STUCK) == -1
    for f in (naive, inplace):
        assert f(list(q0108.EXAMPLE), 3) == 3 and f([0, 1, 0], 1) == 2 and f([1, 1, 0], 2) == -1
    assert fast2(q0108.GRID, 2) == 4 == naive2(q0108.GRID, 2)
    assert fast2(q0108.GRID_BAD, 2) == -1 == naive2(q0108.GRID_BAD, 2)


def test_every_small_array():
    for n in range(1, 13):
        for k in range(1, n + 2):
            sols = q0108.table(n, k)
            for m in range(1 << n):
                a = [m >> j & 1 for j in range(n)]
                want = len(sols[m][0]) if m in sols else -1
                check_row(a, k, want)


def test_random_arrays():
    rng = random.Random(1080)
    for _ in range(3000):
        n = rng.randint(1, 60)
        k = rng.randint(1, n + 2)
        if rng.random() < 0.5 and k <= n:          # a fixable array: from a random set of starts
            starts = [p for p in range(n - k + 1) if rng.random() < 0.4]
            a = q0108.apply([1] * n, k, starts)
            want = len(starts)
        else:
            a = [rng.randint(0, 1) for _ in range(n)]
            want = q0108.answer(a, k)
        check_row(a, k, want)


def test_every_small_grid():
    for R in range(1, 5):
        for C in range(1, 5):
            for k in range(1, max(R, C) + 1):
                sols = q0108.table2(R, C, k)
                for m in range(1 << (R * C)):
                    g = [[m >> (r * C + c) & 1 for c in range(C)] for r in range(R)]
                    want = len(sols[m][0]) if m in sols else -1
                    before = [row[:] for row in g]
                    assert naive2(g, k) == want == fast2(g, k), (g, k)
                    assert g == before


def test_random_grids():
    rng = random.Random(1081)
    for _ in range(1500):
        R, C = rng.randint(1, 12), rng.randint(1, 12)
        k = rng.randint(1, max(R, C))
        if rng.random() < 0.6 and k <= min(R, C):
            starts = [(r, c) for r in range(R - k + 1) for c in range(C - k + 1) if rng.random() < 0.3]
            g = q0108.cover2([[1] * C for _ in range(R)], k, k, starts)
            want = len(starts)
        else:
            g = [[rng.randint(0, 1) for _ in range(C)] for _ in range(R)]
            want = q0108.answer2(g, k)
        assert naive2(g, k) == want == fast2(g, k), (g, k)
