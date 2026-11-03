"""Question 0078: rand7 from rand5, and randN from any randM.

Every number on the page is recomputed here with exact fractions: the 5 x 5 table (each v
from one pair, three cells for every output, 22..25 rejected), 50/21; the page's rand7 fed
every pair and a rejected pair first; the general rand_n against an exact count of its
outcomes for many (M, N, k), expected_calls against k M^k / L and against the bound 2k, the
examples table and the table of rand5 from rand2 by k (k = 4 cheapest, 24/5 and 64/15);
part c: exact_calls against a brute force over every algorithm shape (N | M^B) and against
the prime factors, the examples; the traps' counts; the follow-ups (recycling 1115/504, rand5
from rand7, the bias of a modulo); a statistical check of the page code under a fixed seed;
the generated blocks; and the randmn box's models under Node against the Python reference."""

import itertools
import math
import random
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from extract_code import load_python

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0078  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0078-rand-n-from-rand-m.md").read_text(encoding="utf-8")
ns = load_python(78)
calls_needed, rand_n, expected_calls, exact_calls = ns["calls_needed"], ns["rand_n"], ns["expected_calls"], ns["exact_calls"]


def feed(seq):
    """A source that returns the values of seq in order (and fails when they run out)."""
    it = iter(seq)
    return lambda: next(it)


def test_part_a_table_and_rand7():
    seen = Counter()
    for a in range(1, 6):
        for b in range(1, 6):
            v = 5 * (a - 1) + b
            seen[v] += 1
            ns["rand5"] = feed([a, b])
            if v <= 21:
                assert ns["rand7"]() == (v - 1) % 7 + 1 == q0078.out7(v)
            else:
                # a rejected pair: rand7 calls twice more; the pair (1, 3) gives v = 3
                ns["rand5"] = feed([a, b, 1, 3])
                assert ns["rand7"]() == 3 and q0078.out7(v) == 0
    assert sorted(seen) == list(range(1, 26)) and set(seen.values()) == {1}
    per_output = Counter((v - 1) % 7 + 1 for v in range(1, 22))
    assert per_output == {r: 3 for r in range(1, 8)}
    assert Fraction(3, 25) / Fraction(21, 25) == Fraction(1, 7)
    assert 2 * Fraction(25, 21) == Fraction(50, 21) and round(50 / 21, 2) == 2.38
    assert {v for v in range(1, 22) if (v - 1) % 7 == 0} == {1, 8, 15}
    assert {v for v in range(1, 22) if (v - 1) % 7 == 6} == {7, 14, 21}
    ns["rand5"] = lambda: random.randint(1, 5)


def exact_distribution(m, n, k):
    """The output of one round of rand_n for every sequence of k calls (None when rejected)."""
    out = Counter()
    size = m ** k
    for seq in itertools.product(range(1, m + 1), repeat=k):
        v = 0
        for a in seq:
            v = m * v + a - 1
        out[v % n + 1 if v < size - size % n else None] += 1
    return out


def test_part_b_rand_n_is_uniform_and_the_expectation():
    for m in range(2, 8):
        for n in range(2, 30):
            k0 = calls_needed(m, n)
            assert m ** k0 >= n and (k0 == 1 or m ** (k0 - 1) < n)
            assert k0 == q0078.calls_needed(m, n)
            for k in range(k0, k0 + 3):
                if m ** k > 5000:
                    continue
                dist = exact_distribution(m, n, k)
                accepted = {r: c for r, c in dist.items() if r is not None}
                L = q0078.limit(m, n, k)
                assert set(accepted) == set(range(1, n + 1)) and set(accepted.values()) == {L // n}
                assert dist[None] == m ** k - L
                e = expected_calls(m, n, k)
                assert e == Fraction(k * m ** k, L) == q0078.expected(m, n, k)
                assert e < 2 * k                                 # L > M^k / 2
                # rand_n itself, fed every sequence of one round
                for seq in itertools.product(range(1, m + 1), repeat=k):
                    v = 0
                    for a in seq:
                        v = m * v + a - 1
                    if v < L:
                        assert rand_n(feed(seq), m, n, k) == v % n + 1
            assert expected_calls(m, n) == expected_calls(m, n, k0)


def test_part_b_tables():
    assert q0078.expected(5, 7) == Fraction(50, 21)
    assert q0078.expected(2, 5, 3) == Fraction(24, 5) and q0078.expected(2, 5, 4) == Fraction(64, 15)
    assert q0078.expected(2, 5, 5) == Fraction(16, 3) and q0078.expected(2, 5, 6) == Fraction(32, 5)
    assert min(range(3, 7), key=lambda k: q0078.expected(2, 5, k)) == 4
    assert Fraction(15, 16) / Fraction(5, 8) == Fraction(3, 2) and Fraction(4, 3) < Fraction(3, 2)
    rows = q0078.examples_table().splitlines()[2:]
    assert "| 5 | 7 | 2 | 25 | 21 | 4 | <span dir=\"ltr\">50/21 ≈ 2.38</span> |" in rows
    assert "| 7 | 5 | 1 | 7 | 5 | 2 | <span dir=\"ltr\">7/5 ≈ 1.40</span> |" in rows
    assert "| 6 | 8 | 2 | 36 | 32 | 4 | <span dir=\"ltr\">9/4 ≈ 2.25</span> |" in rows
    k = q0078.by_k_table().splitlines()[2:]
    assert "**<span dir=\"ltr\">64/15 ≈ 4.27</span>**" in k[1] and "24/5 ≈ 4.80" in k[0]


def test_part_c_exact_calls():
    for m in range(2, 21):
        for n in range(2, 61):
            primes = q0078.prime_factors(n)
            assert math.prod(primes) <= n and all(n % p == 0 for p in primes)
            k = exact_calls(m, n)
            assert k == q0078.exact_calls(m, n)
            assert (k > 0) == all(m % p == 0 for p in primes)
            # the fewest B with N | M^B, by brute force up to a generous bound
            brute = next((b for b in range(1, 40) if m ** b % n == 0), 0)
            assert k == brute
            if k:
                assert k <= n.bit_length() and q0078.limit(m, n, k) == m ** k   # no rejection
    # any algorithm with at most B calls: an output's probability is j / M^B, never 1/7 for M = 5
    for B in range(1, 12):
        assert 5 ** B % 7 != 0
    assert exact_calls(5, 7) == 0 and exact_calls(6, 8) == 3 and 6 ** 3 == 216 == 27 * 8
    assert exact_calls(6, 9) == 2 and exact_calls(2, 6) == 0 and exact_calls(4, 6) == 0
    assert exact_calls(20, 10) == 1 and exact_calls(10, 4) == 2 and exact_calls(2, 4) == 2
    assert q0078.expected(6, 8, 2) == Fraction(9, 4)                     # the rejection beats 3 calls
    rows = q0078.bounded_table().splitlines()[2:]
    assert any("6^3 = 216 = 27 \\cdot 8" in r for r in rows) and any("| אין | 7 לא מחלק את 5 |" in r for r in rows)


def test_traps():
    pairs = list(itertools.product(range(1, 6), repeat=2))
    sums = Counter(a + b for a, b in pairs)
    assert sums[6] == 5 and sums[2] == 1
    mod = Counter((a + b) % 7 + 1 for a, b in pairs)
    assert mod == {7: 5, 1: 4, 6: 4, 2: 3, 3: 3, 4: 3, 5: 3}
    assert {5 * a for a in range(1, 6)} == {5, 10, 15, 20, 25}
    prod = Counter(a * b for a, b in pairs)
    assert prod[4] == 3 and len(prod) < 25
    # redrawing only b: row a = 5 accepts only b = 1 (v = 21, output 7)
    p7 = Fraction(0)
    for a in range(1, 6):
        ok = [b for b in range(1, 6) if 5 * (a - 1) + b <= 21]
        p7 += Fraction(1, 5) * Fraction(sum(1 for b in ok if (5 * (a - 1) + b - 1) % 7 + 1 == 7), len(ok))
    assert p7 > Fraction(1, 7)
    five = Counter(sum(s) % 7 for s in itertools.product(range(1, 6), repeat=5))
    assert min(five.values()) == 441 and max(five.values()) == 451 and sum(five.values()) == 3125


def recycled(m, n):
    """The expected calls of one output when the rejected remainder is kept (exact)."""
    trans, todo = {}, [1]
    while todo:
        s = todo.pop()
        if s in trans:
            continue
        size = s * m
        if size < n:
            trans[s] = (Fraction(0), size)
            todo.append(size)
        else:
            L = size - size % n
            trans[s] = (Fraction(L, size), size - L or None)
            if size - L:
                todo.append(size - L)
    keys = sorted(trans)
    idx = {s: i for i, s in enumerate(keys)}
    A = [[Fraction(0)] * (len(keys) + 1) for _ in keys]
    for s, (p, nxt) in trans.items():
        i = idx[s]
        A[i][i] += 1
        A[i][-1] = Fraction(1)
        if nxt:
            A[i][idx[nxt]] -= 1 - p
    for c in range(len(keys)):
        piv = next(r for r in range(c, len(keys)) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        for r in range(len(keys)):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return A[idx[1]][-1] / A[idx[1]][idx[1]]


def test_follow_ups():
    assert recycled(5, 7) == Fraction(1115, 504) and round(1115 / 504, 2) == 2.21
    assert round(math.log(7, 5), 2) == 1.21
    assert q0078.expected(7, 5) == Fraction(7, 5)
    assert Counter(r % 5 for r in range(1, 8)) == {1: 2, 2: 2, 3: 1, 4: 1, 0: 1}
    # $urandom % N: 2^32 mod N small outputs get one value more
    for n in (3, 6, 7, 10, 1000):
        counts = (2 ** 32 // n, 2 ** 32 // n + 1)
        assert 2 ** 32 % n > 0 and counts[1] - counts[0] == 1
    # a 3-bit LFSR gives 7 values: rand6 by rejecting 7, 7/6 cycles; no bounded way
    assert q0078.expected(7, 6) == Fraction(7, 6) and exact_calls(7, 6) == 0


def test_page_code_statistically():
    rng = random.Random(78)
    ns["rand5"] = lambda: rng.randint(1, 5)
    counts = Counter(ns["rand7"]() for _ in range(70000))
    assert set(counts) == set(range(1, 8)) and all(abs(c - 10000) < 450 for c in counts.values())
    for m, n, k in ((5, 7, 0), (2, 5, 4), (6, 8, 0), (7, 10, 0)):
        calls = [0]

        def src():
            calls[0] += 1
            return rng.randint(1, m)
        out = Counter(rand_n(src, m, n, k) for _ in range(20000))
        assert set(out) == set(range(1, n + 1))
        for c in out.values():
            assert abs(c - 20000 / n) < 5 * math.sqrt(20000 / n)
        assert abs(calls[0] / 20000 - float(expected_calls(m, n, k))) < 0.05
    ns["rand5"] = lambda: random.randint(1, 5)


def test_page_numbers():
    for s in ["50/21 \\approx 2.38", "2 \\cdot 25/21", "v = 5(a - 1) + b", "(v - 1) \\bmod 7 + 1", "64/15 \\approx 4.27",
              "6^3 = 216 = 27 \\cdot 8", "2 \\cdot 36/32 = 9/4 = 2.25", "1115/504 \\approx 2.21", "\\log_5 7 \\approx 1.21",
              "7/5 = 1.4", "441 עד 451", "3125", "P_3 = 5/8", "P_4 = 15/16", 'data-kind="randmn" data-m="5" data-n="7"']:
        assert s in PAGE, s
    assert re.search(r"הפלט 7 מקבל 5, ‏?1 ו-6 מקבלים 4", PAGE)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(78)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(m, n) for m in range(2, 11) for n in range(2, 41)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({[list(c) for c in cases]}.map(([a, b]) => {{"
                    f"const k0 = m.rnCalls(a, b); return [k0, [0, 1, 2, 3].map((i) => [m.rnLimit(a, b, k0 + i), m.rnExpected(a, b, k0 + i)]),"
                    f" m.rnFactors(b), m.rnExact(a, b), m.rnShape(a, k0)]; }})));")
    for (m, n), (k0, rows, primes, exact, shape) in zip(cases, got):
        assert k0 == q0078.calls_needed(m, n)
        for i, (L, (num, den)) in enumerate(rows):
            k = k0 + i
            assert L == q0078.limit(m, n, k)
            assert Fraction(num, den) == q0078.expected(m, n, k) and math.gcd(num, den) == 1
        assert primes == q0078.prime_factors(n)
        assert exact == q0078.exact_calls(m, n) == exact_calls(m, n)
        assert shape["rows"] * shape["cols"] == m ** k0 and shape["rows"] == m ** (k0 // 2)
    runs = node_json(f"const m = {explorer_require()};"
                     "console.log(JSON.stringify([[5, 7, 2, 7], [2, 5, 4, 3], [6, 8, 3, 11], [10, 40, 2, 5]].map(([a, b, k, s]) => [a, b, k, m.rnRun(a, b, k, s)])));")
    for m, n, k, rounds in runs:
        assert len(rounds) == 10
        for r in rounds:
            assert len(r["calls"]) == k and all(1 <= a <= m for a in r["calls"])
            v = 0
            for a in r["calls"]:
                v = m * v + a - 1
            assert r["v"] == v and r["ok"] == (v < q0078.limit(m, n, k))
            assert r["out"] == (v % n + 1 if r["ok"] else 0)
    # the page's box: seed 7 on rand7 from rand5 has a rejected round among the ten
    assert any(not r["ok"] for r in runs[0][3]) and any(r["ok"] for r in runs[0][3])
