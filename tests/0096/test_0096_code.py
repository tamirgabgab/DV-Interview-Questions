"""Question 0096: the page's growth, zero_growth, simulate, kelly_fraction, best_growth,
kelly_race and race_growth, run as published. The fractions are checked against direct
numerical maximization of the growth rate; the race against the Karush-Kuhn-Tucker
conditions with exact fractions and against a search over the simplex."""

import math
import random
from fractions import Fraction as Fr

from extract_code import load_python

ns = load_python(96)
growth, zero_growth, simulate = ns["growth"], ns["zero_growth"], ns["simulate"]
kelly_fraction, best_growth = ns["kelly_fraction"], ns["best_growth"]
kelly_race, race_growth = ns["kelly_race"], ns["race_growth"]


def g_ab(f, p, a, b):
    q = 1 - p
    if b * f >= 1:
        return -math.inf
    return p * math.log1p(a * f) + q * math.log1p(-b * f)


def argmax_ab(p, a, b):
    """Golden-section search of g on [0, 1/b): g is concave."""
    lo, hi = 0.0, (1 - 1e-12) / b
    r = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - r * (hi - lo), lo + r * (hi - lo)
    for _ in range(200):
        if g_ab(x1, p, a, b) < g_ab(x2, p, a, b):
            lo, x1 = x1, x2
            x2 = lo + r * (hi - lo)
        else:
            hi, x2 = x2, x1
            x1 = hi - r * (hi - lo)
    return (lo + hi) / 2


def test_growth_part_a():
    assert math.isclose(growth(0.2, 0.6), 0.6 * math.log(1.2) + 0.4 * math.log(0.8))
    assert growth(0, 0.6) == 0
    # the best of a fine grid is 0.2, and g is concave around it
    grid = [i / 1000 for i in range(0, 999)]
    best = max(grid, key=lambda f: growth(f, 0.6))
    assert best == 0.2
    root = zero_growth(0.6, 0.2)
    assert abs(growth(root, 0.6)) < 1e-9 and 0.389 < root < 0.3894
    assert growth(root - 1e-6, 0.6) > 0 > growth(root + 1e-6, 0.6)


def test_simulate():
    finals = simulate(0.2, 0.6, 100, 12, seed=96)
    assert finals == sorted(finals) and len(finals) == 12
    # every final is 100 * 1.2^k * 0.8^(100 - k) for a number of wins k
    for w in finals:
        k = round((math.log(w / 100) - 100 * math.log(0.8)) / (math.log(1.2) - math.log(0.8)))
        assert math.isclose(w, 100 * 1.2 ** k * 0.8 ** (100 - k), rel_tol=1e-9)
    # many paths: the median is near 100 e^(100 g(0.2)), about 749 (60 wins); its log within
    # a few wins of 60
    many = simulate(0.2, 0.6, 100, 2001, seed=7)
    med = many[1000]
    wins = (math.log(med / 100) - 100 * math.log(0.8)) / (math.log(1.2) - math.log(0.8))
    assert 57 <= wins <= 63
    # f = 1: only a path of 100 wins survives, so every path is 0
    assert simulate(1.0, 0.6, 100, 50, seed=3) == [0.0] * 50


def test_kelly_fraction_against_a_search():
    rnd = random.Random(96)
    cases = [(Fr(3, 5), 1, 1), (Fr(2, 5), 3, 1), (Fr(1, 2), 1, Fr(1, 2)), (Fr(1, 4), 5, 1), (Fr(3, 10), 2, 1)]
    for _ in range(300):
        cases.append((Fr(rnd.randint(1, 99), 100), Fr(rnd.randint(2, 50), 10), Fr(rnd.randint(1, 20), 20)))
    for p, a, b in cases:
        f = kelly_fraction(p, a, b)
        assert isinstance(f, Fr) and 0 <= f < 1 / Fr(b)
        if p * a <= (1 - p) * b:
            assert f == 0
            # no bet: g is not positive anywhere
            assert all(g_ab(x / 100 / float(b), float(p), float(a), float(b)) <= 1e-15 for x in range(1, 100))
        else:
            assert f == p / b - (1 - p) / a == (p * a - (1 - p) * b) / (a * b)
            assert math.isclose(float(f), argmax_ab(float(p), float(a), float(b)), abs_tol=1e-6)
            # the growth at the best fraction in closed form
            q = 1 - p
            closed = float(p) * math.log(float(p * (a + b) / b)) + float(q) * math.log(float(q * (a + b) / a))
            assert math.isclose(best_growth(p, a, b), closed, rel_tol=1e-12, abs_tol=1e-15)
    # even odds: 2p - 1, and ln 2 - H(p)
    for k in range(51, 100):
        p = Fr(k, 100)
        assert kelly_fraction(p) == 2 * p - 1
        H = -(float(p) * math.log(float(p)) + float(1 - p) * math.log(float(1 - p)))
        assert math.isclose(best_growth(p), math.log(2) - H, rel_tol=1e-12)
    assert kelly_fraction(Fr(1, 2)) == 0 and kelly_fraction(Fr(2, 5)) == 0
    # p = 1: no loss term
    assert kelly_fraction(1, 2, 1) == 1 and math.isclose(best_growth(1, 2, 1), math.log(3))


def kkt_ok(probs, odds, cash, bets):
    """The optimality conditions of max sum p_i ln(c + o_i b_i) on c + sum b_i = 1: every
    partial derivative of a positive variable is 1, the others at most 1."""
    probs, odds = [Fr(x) for x in probs], [Fr(x) for x in odds]
    if cash < 0 or any(b < 0 for b in bets) or cash + sum(bets) != 1:
        return False
    vals = [cash + o * b for o, b in zip(odds, bets)]
    if any(v <= 0 for p, v in zip(probs, vals) if p):
        return False
    d_cash = sum(p / v for p, v in zip(probs, vals) if p)
    d_bets = [p * o / v if p else Fr(0) for p, o, v in zip(probs, odds, vals)]
    lam = Fr(1)
    if cash > 0 and d_cash != lam:
        return False
    if cash == 0 and d_cash > lam:
        return False
    return all((d == lam) if b > 0 else (d <= lam) for d, b in zip(d_bets, bets))


def search_simplex(probs, odds, rnd, iters=4000):
    """A crude search for the best (cash, bets): random moves of mass between two variables."""
    m = len(probs)
    x = [1.0] + [0.0] * m

    def val(x):
        vs = [x[0] + o * b for o, b in zip(odds, x[1:])]
        if any(v <= 0 for p, v in zip(probs, vs) if p):
            return -math.inf
        return sum(p * math.log(v) for p, v in zip(probs, vs) if p)
    best = val(x)
    step = 0.2
    for it in range(iters):
        i, j = rnd.sample(range(m + 1), 2)
        d = min(x[i], step * rnd.random())
        y = x[:]
        y[i] -= d
        y[j] += d
        v = val(y)
        if v > best:
            x, best = y, v
        if it % 500 == 499:
            step /= 2
    return best


def test_kelly_race():
    P = [Fr(1, 2), Fr(3, 10), Fr(3, 20), Fr(1, 20)]
    O = [Fr(11, 5), Fr(7, 2), Fr(5), Fr(10)]
    cash, bets = kelly_race(P, O)
    assert cash == Fr(77, 100) and bets == [Fr(3, 20), Fr(2, 25), 0, 0]
    assert kkt_ok(P, O, cash, bets)
    # the variant of the trap: odds 6 on horse 3
    cash6, bets6 = kelly_race(P, [Fr(11, 5), Fr(7, 2), Fr(6), Fr(10)])
    assert cash6 == Fr(231, 430) and bets6 == [Fr(11, 43), Fr(63, 430), Fr(13, 215), 0]
    rnd = random.Random(96)
    for _ in range(150):
        m = rnd.randint(2, 6)
        w = [rnd.randint(1, 20) for _ in range(m)]
        probs = [Fr(x, sum(w)) for x in w]
        odds = [Fr(rnd.randint(11, 120), 10) for _ in range(m)]
        cash, bets = kelly_race(probs, odds)
        assert kkt_ok(probs, odds, cash, bets), (probs, odds, cash, bets)
        g = race_growth(cash, bets, probs, odds)
        found = search_simplex([float(p) for p in probs], [float(o) for o in odds], rnd)
        assert g >= found - 1e-9
        assert g >= 0          # keeping everything in cash gives 0
    # fair odds: nothing to bet
    probs = [Fr(1, 2), Fr(1, 3), Fr(1, 6)]
    assert kelly_race(probs, [1 / p for p in probs]) == (1, [0, 0, 0])


def test_all_in_is_proportional():
    rnd = random.Random(5)
    P = [0.5, 0.3, 0.15, 0.05]
    best = sum(p * math.log(p) for p in P)
    for _ in range(2000):
        w = [rnd.random() for _ in P]
        b = [x / sum(w) for x in w]
        assert sum(p * math.log(x) for p, x in zip(P, b)) <= best + 1e-12
