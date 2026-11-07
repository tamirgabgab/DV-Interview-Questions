"""Question 0022: the page's Python code (it runs as published) against the generator's
reference: paths_rd, paths_rd_dp and paths_rd_mod on every small board and on big ones;
paths_rd_blocked and paths_rud_blocked on random boards, exact and mod p; paths_rud,
paths_rud_mod and count_walks."""

import random
import sys
from math import comb

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0022  # noqa: E402

ns = load_python(22)
P = 10**9 + 7


def rand_grid(rng, m, n, p):
    g = [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(m)]
    g[0][0] = 0
    if rng.random() < 0.9:
        g[m - 1][n - 1] = 0
    return g


def test_part_a():
    assert ns["paths_rd"](3, 7) == ns["paths_rd_dp"](3, 7) == 28
    for m in range(1, 40):
        for n in range(1, 40):
            exact = comb(m + n - 2, m - 1)
            assert ns["paths_rd"](m, n) == ns["paths_rd_dp"](m, n) == exact
            assert ns["paths_rd_mod"](m, n) == exact % P
    for m, n in ((100, 100), (1000, 3), (500, 777)):
        assert ns["paths_rd_mod"](m, n) == comb(m + n - 2, m - 1) % P
        assert ns["paths_rd_mod"](m, n, 998244353) == comb(m + n - 2, m - 1) % 998244353


def test_part_b():
    b = q0022.parse(q0022.BOARD_B)
    assert ns["paths_rd_blocked"](b) == 9
    rng = random.Random(3)
    for _ in range(1500):
        m, n = rng.randint(1, 9), rng.randint(1, 9)
        g = rand_grid(rng, m, n, rng.choice((0, 0.1, 0.3, 0.5)))
        ref = q0022.count(g)
        assert ns["paths_rd_blocked"](g) == ref, g
        assert ns["paths_rd_blocked"](g, 97) == ref % 97
        if not any(map(any, g)):
            assert ref == comb(m + n - 2, m - 1)
    big = [[0] * 60 for _ in range(60)]
    big[30][30] = 1
    assert ns["paths_rd_blocked"](big, P) == q0022.count(big) % P


def test_part_c():
    assert ns["paths_rud"](3, 7) == 729 and ns["paths_rud"](10, 10) == 10**9
    assert ns["paths_rud_mod"](10, 10**18) == pow(10, 10**18 - 1, P)
    rd, rud, all4 = [(0, 1), (1, 0)], [(0, 1), (1, 0), (-1, 0)], [(0, 1), (1, 0), (-1, 0), (0, -1)]
    for m in range(1, 5):
        for n in range(1, 6):
            g = q0022.empty(m, n)
            assert ns["count_walks"](g, rd) == comb(m + n - 2, m - 1)
            assert ns["count_walks"](g, rud) == ns["paths_rud"](m, n) == m ** (n - 1)
            assert ns["count_walks"](g, all4) == q0022.count_walks(g, q0022.ALL)
    rng = random.Random(4)
    for _ in range(300):
        g = rand_grid(rng, rng.randint(1, 4), rng.randint(1, 5), 0.3)
        assert ns["count_walks"](g, rud) == q0022.count(g, True)


def test_part_d():
    assert ns["paths_rud_blocked"](q0022.parse(q0022.BOARD_B)) == 32
    assert ns["paths_rud_blocked"](q0022.parse(q0022.ZIGZAG)) == 9 and ns["paths_rd_blocked"](q0022.parse(q0022.ZIGZAG)) == 0
    rng = random.Random(6)
    for _ in range(1500):
        m, n = rng.randint(1, 9), rng.randint(1, 9)
        g = rand_grid(rng, m, n, rng.choice((0, 0.1, 0.3, 0.5)))
        ref = q0022.count(g, True)
        assert ns["paths_rud_blocked"](g) == ref, g
        assert ns["paths_rud_blocked"](g, 1009) == ref % 1009
        if not any(map(any, g)):
            assert ref == m ** (n - 1)
    big = [[0] * 40 for _ in range(30)]
    assert ns["paths_rud_blocked"](big, P) == pow(30, 39, P)
