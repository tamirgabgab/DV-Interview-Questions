"""Question 0101, Sicherman dice: the numbers the page states, recomputed from the references in
tools/figures/q0101.py (a search of every pair of dice by their counts, the split of the factors of
the standard die, the mixed sizes), the generated blocks, and the box's models under Node against
the same references."""

import itertools
import json
import random
import sys
from collections import Counter
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0101  # noqa: E402

STD6 = (1, 2, 3, 4, 5, 6)
SICH = ((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8))
ZERO = [((0, 1, 1, 2, 2, 3), (2, 4, 5, 6, 7, 9)), ((0, 1, 2, 3, 4, 5), (2, 3, 4, 5, 6, 7)),
        ((0, 2, 3, 4, 5, 7), (2, 3, 3, 4, 4, 5)), SICH, (STD6, STD6)]
PAIRS8 = [((1, 2, 2, 3, 3, 4, 4, 5), (1, 3, 5, 5, 7, 7, 9, 11)), ((1, 2, 2, 3, 5, 6, 6, 7), (1, 3, 3, 5, 5, 7, 7, 9)),
          ((1, 2, 3, 3, 4, 4, 5, 6), (1, 2, 5, 5, 6, 6, 9, 10)), (tuple(range(1, 9)), tuple(range(1, 9)))]


def poly(*coeffs):
    return list(coeffs)


def test_statement_and_part_a():
    cnt = q0101.sums(STD6, STD6)
    assert [cnt[s] for s in range(2, 13)] == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1] and sum(cnt.values()) == 36
    assert q0101.sums(*SICH) == cnt and q0101.same(*SICH)
    # the search by counts alone and the factors agree: two pairs for six faces
    assert q0101.brute_pairs(6) == q0101.factor_pairs(6) == sorted([SICH, (STD6, STD6)])
    # the worked example: (x + x^2)(2x + x^3) = 2x^2 + 2x^3 + x^4 + x^5
    assert q0101.mul([0, 1, 1], [0, 2, 0, 1]) == [0, 0, 2, 2, 1, 1]
    assert q0101.die_poly((1, 1, 3)) == [0, 2, 0, 1] and sorted(q0101.sums((1, 2), (1, 1, 3)).items()) == [(2, 2), (3, 2), (4, 1), (5, 1)]
    # P(x) = x (1 + x)(1 + x + x^2)(1 - x + x^2); the values 1, 2, 3, 1 at x = 1; discriminant -3
    p = q0101.mul(q0101.mul(q0101.mul([0, 1], [1, 1]), [1, 1, 1]), [1, -1, 1])
    assert p == q0101.die_poly(STD6) and q0101.cyclotomic(6) == [1, -1, 1] and q0101.cyclotomic(3) == [1, 1, 1]
    assert [sum(f) for f in ([0, 1], [1, 1], [1, 1, 1], [1, -1, 1])] == [1, 2, 3, 1] and 1 - 4 == -3
    # 2^i 3^j = 6 only for i = j = 1 (i, j from 0 to 2)
    assert [(i, j) for i in range(3) for j in range(3) if 2**i * 3**j == 6] == [(1, 1)]
    a = q0101.mul(q0101.mul([0, 1], [1, 1]), [1, 1, 1])
    assert a == [0, 1, 2, 2, 1] and q0101.faces_of(a) == SICH[0]
    b = q0101.mul(q0101.mul(a, [1, -1, 1]), [1, -1, 1])
    assert b == [0, 1, 0, 1, 1, 1, 1, 0, 1] and q0101.faces_of(b) == SICH[1]
    # the trial and error: face 1 twice gives the sum 2 twice and 12 never
    t = q0101.sums((1, 1, 2, 3, 4, 5), STD6)
    assert t[2] == 2 and t[12] == 0
    # the cost: C(3n - 2, n) dice A, 8,008 for n = 6, more than half a billion for n = 12
    assert len(list(itertools.combinations_with_replacement(range(1, 12), 6))) == comb(16, 6) == 8008
    assert comb(34, 12) > 5 * 10**8


def test_part_b():
    assert q0101.factor_pairs(6, 0) == sorted(ZERO) == q0101.brute_pairs(6, 0)
    for (a, b) in ZERO[:3]:   # the three new pairs are shifts by 1 of part a's
        up = tuple(f + 1 for f in a)
        down = tuple(f - 1 for f in b)
        assert tuple(sorted((up, down))) in (SICH, (STD6, STD6))
    # 3 x 3 ordered splits, the standard one its own mirror: 1 + 8 / 2 = 5
    assert 1 + (9 - 1) // 2 == 5


def test_part_c():
    counts = [len(q0101.factor_pairs(n)) for n in range(2, 13)]
    assert counts == [1, 1, 2, 1, 2, 1, 4, 2, 2, 1, 8]
    assert [len(q0101.factor_pairs(n, 0)) for n in range(2, 13)] == [2, 2, 5, 2, 5, 2, 11, 5, 5, 2, 23]
    for n in range(2, 9):
        assert q0101.brute_pairs(n) == q0101.factor_pairs(n), n
    for n in range(2, 7):
        assert q0101.brute_pairs(n, 0) == q0101.factor_pairs(n, 0), n
    assert q0101.factor_pairs(4) == [((1, 2, 2, 3), (1, 3, 3, 5)), ((1, 2, 3, 4), (1, 2, 3, 4))]
    assert q0101.factor_pairs(8) == sorted(PAIRS8)
    # another pair exactly when n is composite
    for n in range(2, 25):
        prime = all(n % d for d in range(2, n))
        assert (len(q0101.factor_pairs(n)) == 1) == prime, n
    # Phi_d(1) = p for d a power of the prime p, else 1; their product over d | n, d > 1 is n
    for d in range(2, 40):
        ps = [p for p in range(2, d + 1) if d % p == 0 and all(p % q for q in range(2, p))]
        assert sum(q0101.cyclotomic(d)) == (ps[0] if len(ps) == 1 else 1), d
    for n in range(2, 40):
        prod = 1
        for d in q0101.divisors(n):
            prod *= sum(q0101.cyclotomic(d))
        assert prod == n
    # the construction for n = p m: A = 1 + u + w, B = 1 + p v + m z
    for n in range(4, 31):
        for p in range(2, n):
            if n % p or n // p < 2:
                continue
            m = n // p
            a = sorted(1 + u + w for u in range(p) for w in range(m))
            b = sorted(1 + p * v + m * z for v in range(m) for z in range(p))
            assert q0101.same(a, b) and a != list(range(1, n + 1)), (n, p)
    assert sorted(1 + u + w for u in range(2) for w in range(3)) == list(SICH[0])
    assert sorted(1 + 2 * v + 3 * z for v in range(3) for z in range(2)) == list(SICH[1])
    assert sorted(1 + 2 * v + 2 * z for v in range(2) for z in range(2)) == [1, 3, 3, 5]
    # the negative example of n = 12: x Phi_3 Phi_4^2 Phi_6^2 counts 12 faces, x^2 has -1
    bad = [a for split, a in q0101.bad_splits(12) if split == {2: 0, 3: 1, 4: 2, 6: 2, 12: 0}]
    assert len(bad) == 1 and bad[0][:4] == [0, 1, -1, 4] and sum(bad[0]) == 12 == 3 * 2**2
    # the cost: 6 divisors of 12, 3^5 = 243 splits
    assert len(q0101.divisors(12)) + 1 == 6 and 3 ** len(q0101.divisors(12)) == 243


def test_followups():
    # a 4-sided and a 9-sided die with the sum of two standard six-sided dice: three pairs
    want = [((1, 2, 2, 3), (1, 3, 3, 5, 5, 5, 7, 7, 9)), ((1, 2, 4, 5), (1, 2, 3, 3, 4, 5, 5, 6, 7)),
            ((1, 4, 4, 7), (1, 2, 2, 3, 3, 3, 4, 4, 5))]
    assert q0101.mixed_pairs(4, 9) == q0101.mixed_brute(4, 9) == want
    target = q0101.sums(STD6, STD6)
    assert all(q0101.sums(a, b) == target for a, b in want)
    # three dice: a die of six faces dividing P^3 (faces 1 to 16), then every pair of them
    p3 = q0101.mul(q0101.mul(q0101.die_poly(STD6), q0101.die_poly(STD6)), q0101.die_poly(STD6))
    divs = []
    for a in itertools.combinations_with_replacement(range(1, 17), 6):
        try:
            rest = q0101.div_exact(p3, q0101.die_poly(a))
        except AssertionError:
            continue
        if min(rest) >= 0:
            divs.append(a)
    triples = set()
    for a in divs:
        for b in divs:
            try:
                c = q0101.div_exact(q0101.div_exact(p3, q0101.die_poly(a)), q0101.die_poly(b))
            except AssertionError:
                continue
            if min(c) >= 0 and sum(c) == 6 and c[0] == 0:
                triples.add(tuple(sorted((a, b, q0101.faces_of(c)))))
    assert triples == {(STD6, STD6, STD6), tuple(sorted((SICH[0], SICH[1], STD6)))}
    # the split 3, 0, 0 of 1 - x + x^2 has a negative coefficient
    a = [0, 1]
    for f in ([1, 1], [1, 1, 1], [1, -1, 1], [1, -1, 1], [1, -1, 1]):
        a = q0101.mul(a, f)
    assert min(a) < 0 and sum(a) == 6
    # the covergroup: A never shows 5 and 6, B never 2 and once 8; the legal cross 20 of 36
    assert set(STD6) - set(SICH[0]) == {5, 6} and set(STD6) - set(SICH[1]) == {2} and 8 in SICH[1]
    assert len({(x, y) for x in SICH[0] for y in SICH[1] if y <= 6}) == 20


def test_try_it_paragraphs():
    """The changes the "try it" paragraphs ask for and what they say the box shows."""
    def diff(a, b):
        n = len(a)
        got, want = q0101.sums(a, b), q0101.sums(range(1, n + 1), range(1, n + 1))
        return sorted(s for s in set(got) | set(want) if got[s] != want[s])

    assert diff(SICH[0], (1, 3, 4, 5, 6, 7)) == [8, 9, 11, 12]            # part a: B's 8 to 7
    assert diff((1, 1, 1, 2, 2, 3), (2, 4, 5, 6, 7, 9)) == [2, 3, 4, 8, 9, 10]   # part b: A's 0 to 1
    assert diff(PAIRS8[0][0], (1, 3, 5, 5, 7, 7, 9, 10)) == [11, 12, 15, 16]     # part c: B's 11 to 10


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(101)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(101)
    cases = []
    for _ in range(200):
        n = rng.choice([4, 6, 8])
        cases.append([[rng.randint(0, 20) for _ in range(n)], [rng.randint(0, 20) for _ in range(n)]])
    for (a, b) in [SICH, *ZERO, *PAIRS8]:
        cases.append([list(a), list(b)])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([a, b]) => [m.scSums(a, b), m.scDiff(a, b)])));")
    for (a, b), (sums, diff) in zip(cases, got):
        n = len(a)
        ref = q0101.sums(a, b)
        assert sums == [ref.get(s, 0) for s in range(max(a) + max(b) + 1)]
        want = q0101.sums(range(1, n + 1), range(1, n + 1))
        assert diff == sorted(s for s in set(ref) | set(want) if ref[s] != want[s])
    levels = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify([4, 6, 8].map((n) => Array.from({length: 45}, (_, s) => [m.scLevel(s, n), m.scHue(s, n)]))));")
    for n, row in zip([4, 6, 8], levels):
        assert row == [[q0101.level(s, n), q0101.hue(s, n)] for s in range(45)]
    pairs = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([m.scPairs, m.scTries]));")
    keyed = {n: sorted(tuple(sorted((tuple(a), tuple(b)))) for _, a, b in pairs[0][n]) for n in pairs[0]}
    assert keyed == {"4": q0101.factor_pairs(4), "6": q0101.factor_pairs(6, 0), "8": q0101.factor_pairs(8)}
    assert [p[0] for p in pairs[0]["6"]][:2] == ["רגילות", "‏Sicherman"]
    (name, a, b), = pairs[1]["6"]
    assert a == [1, 1, 2, 3, 4, 5] and b == list(STD6) and not q0101.same(a, b)
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify([['1.2.2.3.3.4', 6], ['0.20.3.4', 4], ['1.2.3', 4], ['1.21.3.4', 4], ['1.x.3.4', 4], ['', 6]].map(([t, n]) => m.scParse(t, n))));")
    assert parsed == [[1, 2, 2, 3, 3, 4], [0, 20, 3, 4], None, None, None, None]
