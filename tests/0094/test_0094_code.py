"""Question 0094: the page's walk_odds, by_recurrence, rates_to_steps and simulate, run as
published. walk_odds is checked exactly (fractions) against an independent solution of the
whole absorbing chain by Gaussian elimination, and against by_recurrence; rates_to_steps
against the four outcomes of a cycle; simulate against the formula within four standard
errors under fixed seeds."""

import math
from fractions import Fraction as Fr

from extract_code import load_python

ns = load_python(94)
walk_odds, by_recurrence = ns["walk_odds"], ns["by_recurrence"]
rates_to_steps, simulate = ns["rates_to_steps"], ns["simulate"]


def solve(rows):
    """Gauss-Jordan on an augmented matrix of fractions."""
    n = len(rows)
    m = [r[:] for r in rows]
    for c in range(n):
        piv = next(i for i in range(c, n) if m[i][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        inv = 1 / m[c][c]
        m[c] = [v * inv for v in m[c]]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[c])]
    return [m[i][n] for i in range(n)]


def chain(N, p, q, upper="absorb"):
    """P(full) and the expected cycles for every start 1..N-1 of the chain itself: the
    first-step equations for every state, solved as one linear system. upper="reflect"
    keeps the counter at N (an up step lost) and solves only the cycles to empty."""
    p, q = Fr(p), Fr(q)
    r = 1 - p - q
    states = list(range(1, N)) if upper == "absorb" else list(range(1, N + 1))
    ix = {s: i for i, s in enumerate(states)}

    def system(const, top):
        rows = []
        for s in states:
            row = [Fr(0)] * (len(states) + 1)
            row[ix[s]] += 1
            stay = r + (p if s == N else 0)
            row[ix[s]] -= stay
            if s + 1 in ix:
                row[ix[s + 1]] -= p
            elif s + 1 == N and upper == "absorb":
                row[-1] += p * top
            if s - 1 in ix:
                row[ix[s - 1]] -= q
            row[-1] += const
            rows.append(row)
        return solve(rows)

    if upper == "reflect":
        return None, dict(zip(states, system(Fr(1), 0)))
    full = dict(zip(states, system(Fr(0), Fr(1))))
    cycles = dict(zip(states, system(Fr(1), Fr(0))))
    return full, cycles


GRID = [(Fr(1, 2), Fr(1, 2)), (Fr(3, 5), Fr(2, 5)), (Fr(2, 5), Fr(3, 5)), (Fr(3, 10), Fr(1, 5)),
        (Fr(1, 4), Fr(1, 4)), (Fr(1, 10), Fr(7, 10)), (Fr(9, 10), Fr(1, 20)), (Fr(1, 3), Fr(1, 6)),
        (Fr(1, 1), Fr(0)), (Fr(0), Fr(1, 2))]


def test_walk_odds_against_the_chain():
    for N in (2, 3, 5, 10, 13):
        for p, q in GRID:
            if p == 0:
                for k in range(1, N):
                    assert walk_odds(k, N, p, q) == (0, 1, Fr(k) / q)
                continue
            full, cycles = chain(N, p, q)
            for k in range(1, N):
                f, e, m = walk_odds(k, N, p, q)
                assert f == full[k] and e == 1 - full[k] and m == cycles[k]
            assert walk_odds(0, N, p, q) == (0, 1, 0) and walk_odds(N, N, p, q) == (1, 0, 0)


def test_the_numbers_of_the_parts():
    assert walk_odds(3, 10, Fr(1, 2), Fr(1, 2)) == (Fr(3, 10), Fr(7, 10), 21)
    assert walk_odds(3, 10, Fr(3, 5), Fr(2, 5)) == (Fr(41553, 58025), Fr(16472, 58025), Fr(48291, 2321))
    assert walk_odds(3, 10, Fr(3, 10), Fr(1, 5)) == (Fr(41553, 58025), Fr(16472, 58025), Fr(96582, 2321))
    p, q = rates_to_steps(Fr(1, 2), Fr(1, 4))
    assert (p, q) == (Fr(3, 8), Fr(1, 8))
    assert walk_odds(3, 10, p, q) == (Fr(28431, 29524), Fr(1093, 29524), Fr(195738, 7381))
    # every k of part a: k/N and k(N - k)
    for k in range(11):
        assert walk_odds(k, 10, Fr(1, 2), Fr(1, 2))[::2] == (Fr(k, 10), k * (10 - k))
    # floats run too (Fraction of a float is exact)
    f, _, m = walk_odds(3, 10, 0.6, 0.4)
    assert math.isclose(float(f), 41553 / 58025) and math.isclose(float(m), 48291 / 2321)


def test_by_recurrence_agrees():
    for N in (2, 4, 10, 17):
        for p, q in GRID:
            if p == 0:
                continue
            full, cycles = by_recurrence(N, p, q)
            for k in range(N + 1):
                f, _, m = walk_odds(k, N, p, q)
                assert full[k] == f and cycles[k] == m


def test_stays_change_only_the_time():
    for p, q in [(Fr(3, 10), Fr(1, 5)), (Fr(1, 10), Fr(1, 10)), (Fr(1, 5), Fr(1, 2))]:
        s = p + q
        for k in range(1, 10):
            f, e, m = walk_odds(k, 10, p, q)
            f1, e1, m1 = walk_odds(k, 10, p / s, q / s)
            assert (f, e) == (f1, e1) and m == m1 / s


def test_rates_to_steps_is_the_four_outcomes():
    for l1 in (Fr(1, 10), Fr(1, 4), Fr(1, 2), Fr(9, 10)):
        for l2 in (Fr(1, 10), Fr(1, 4), Fr(4, 5)):
            out = {}
            for back, pb in ((1, l1), (0, 1 - l1)):
                for used, pu in ((1, l2), (0, 1 - l2)):
                    out[back - used] = out.get(back - used, 0) + pb * pu
            assert rates_to_steps(l1, l2) == (out[1], out[-1])
            # the odds ratio: q/p < 1 exactly when credits come back faster than they are used
            p, q = out[1], out[-1]
            assert (q / p < 1) == (l1 > l2)
    # equal rates: a fair walk, k/N and k(N - k) / (2 lam (1 - lam))
    for lam in (Fr(1, 10), Fr(1, 2), Fr(3, 4)):
        f, _, m = walk_odds(3, 10, *rates_to_steps(lam, lam))
        assert f == Fr(3, 10) and m == 21 / (2 * lam * (1 - lam))
    assert walk_odds(3, 10, *rates_to_steps(Fr(1, 2), Fr(1, 2)))[2] == 42


def test_geometric_waits_have_no_memory():
    for lam in (Fr(1, 10), Fr(1, 3), Fr(1, 2)):
        pmf = lambda t: lam * (1 - lam) ** (t - 1)     # noqa: E731
        for t in range(0, 12):
            tail = 1 - sum(pmf(i) for i in range(1, t + 1))
            assert tail == (1 - lam) ** t
            assert pmf(t + 1) / tail == lam


def test_simulate_is_near_the_formula():
    for (l1, l2, seed) in [(0.5, 0.25, 1), (0.5, 0.5, 2), (0.4, 0.5, 3), (0.9, 0.8, 4)]:
        runs = 6000
        share, empty, mean = simulate(3, 10, l1, l2, runs, seed=seed)
        f, _, m = walk_odds(3, 10, *rates_to_steps(Fr(l1), Fr(l2)))
        f = float(f)
        assert abs(share - f) <= 4 * math.sqrt(f * (1 - f) / runs) + 1e-9
        assert math.isclose(share + empty, 1)
        assert abs(mean - float(m)) <= 0.06 * float(m)
    # the same seed, the same runs
    assert simulate(3, 10, 0.5, 0.25, 50, seed=9) == simulate(3, 10, 0.5, 0.25, 50, seed=9)
