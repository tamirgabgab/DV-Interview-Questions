"""Question 0101, Sicherman dice: the numbers the page states, recomputed from the references in
tools/figures/q0101.py (a search of every pair of dice by their counts, the split of the factors of
the standard die, k dice by their factors, by a search of three dice from scratch and by the
partition count, the mixed sizes), the generated blocks, and the box's models under Node against
the same references."""

import itertools
import json
import random
import sys
from collections import Counter
from itertools import permutations
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0101  # noqa: E402

STD6 = (1, 2, 3, 4, 5, 6)
SICH = ((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8))
ZERO = [((0, 1, 1, 2, 2, 3), (2, 4, 5, 6, 7, 9)), ((0, 1, 2, 3, 4, 5), (2, 3, 4, 5, 6, 7)),
        ((0, 2, 3, 4, 5, 7), (2, 3, 3, 4, 4, 5)), SICH, (STD6, STD6)]
SICH3 = tuple(sorted((SICH[0], STD6, SICH[1])))


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
    # the statement: three standard dice, the sums 3 to 18 out of 216 rolls, 10 and 11 the most
    cnt = q0101.sums(q0101.sums(STD6, STD6).elements(), STD6)
    assert [cnt[s] for s in range(3, 19)] == [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
    assert sum(cnt.values()) == 216 and cnt[10] == cnt[11] == 27 == max(cnt.values())
    # the three kinds of dice and the fourth that is none: x (1 + x)(1 + x + x^2)(1 - x + x^2)^e
    assert [q0101.faces_of(q0101.kind_poly(e)) for e in range(3)] == [SICH[0], STD6, SICH[1]]
    assert q0101.kind_poly(0) == [0, 1, 2, 2, 1] and q0101.mul([1, 1], [1, 1, 1]) == [1, 2, 2, 1]
    e3 = q0101.kind_poly(3)
    assert e3 == [0, 1, -1, 2, 0, 1, 1, 0, 2, -1, 1] and sum(e3) == 6 and e3[2] == -1
    # the coefficient of x^2 is 2 - e for every e, so a die takes at most two copies
    for e in range(8):
        p = q0101.kind_poly(e)
        assert p[:3] == [0, 1, 2 - e] and sum(p) == 6 and (min(p) >= 0) == (e <= 2), e
    # step 1: three dice, by the factors and by a search from scratch
    assert q0101.factor_sets(3) == q0101.brute_triples(1) == sorted([SICH3, (STD6, STD6, STD6)])
    zero3 = q0101.factor_sets(3, 0)
    assert zero3 == q0101.brute_triples(0) and len(zero3) == 13
    # step 2: j Sicherman pairs and k - 2j standard dice, floor(k / 2) + 1 sets
    for k in range(1, 9):
        sets = q0101.factor_sets(k)
        want = sorted(tuple(sorted([SICH[0]] * j + [STD6] * (k - 2 * j) + [SICH[1]] * j)) for j in range(k // 2 + 1))
        assert sets == want and len(sets) == k // 2 + 1 == q0101.count_sets(k), k
    # step 3 and its table: a face 0 allowed, counted by partitions, 5 for two dice as in part b
    counts = [len(q0101.factor_sets(k, 0)) for k in range(2, 7)]
    assert counts == [5, 13, 41, 98, 250] == [q0101.count_sets(k, 0) for k in range(2, 7)]
    assert q0101.factor_sets(2) == q0101.factor_pairs(6) == q0101.brute_pairs(6)
    assert q0101.factor_sets(2, 0) == q0101.factor_pairs(6, 0) == q0101.brute_pairs(6, 0)
    assert q0101.partitions(3, 3) == 3 and comb(5, 2) == 10 and 3 + 10 == 13
    bases = []
    for dice in zero3:   # the first face of each die is its number of x's; they add up to 3
        assert sum(min(d) for d in dice) == 3
        bases.append(tuple(sorted(tuple(f - min(d) + 1 for f in d) for d in dice)))
    assert bases.count((STD6, STD6, STD6)) == 3 and bases.count(SICH3) == 10
    # every set has the sum of k standard dice, counted roll by roll
    for k in range(1, 6):
        for low in (1, 0):
            assert all(q0101.same_k(d) for d in q0101.factor_sets(k, low)), (k, low)
    # the cost: C(k + 2, 2) choices of k of 3 dice; with 0, 3(k + 1) dice and C(4k + 2, k)
    # choices, 230,230 for k = 6; a search from scratch of 3 dice: 134,596 dice from 0 to 18
    assert [comb(k + 2, 2) for k in range(1, 5)] == [len(list(itertools.combinations_with_replacement(range(3), k))) for k in range(1, 5)]
    assert comb(3 * 7 + 6 - 1, 6) == comb(26, 6) == 230230
    assert comb(19 + 6 - 1, 6) == 134596


def test_followups():
    # a 4-sided and a 9-sided die with the sum of two standard six-sided dice: three pairs
    want = [((1, 2, 2, 3), (1, 3, 3, 5, 5, 5, 7, 7, 9)), ((1, 2, 4, 5), (1, 2, 3, 3, 4, 5, 5, 6, 7)),
            ((1, 4, 4, 7), (1, 2, 2, 3, 3, 3, 4, 4, 5))]
    assert q0101.mixed_pairs(4, 9) == q0101.mixed_brute(4, 9) == want
    target = q0101.sums(STD6, STD6)
    assert all(q0101.sums(a, b) == target for a, b in want)
    # n faces: another pair exactly when n is composite; n = 4 one, n = 8 three
    for n in range(2, 25):
        prime = all(n % d for d in range(2, n))
        assert (len(q0101.factor_pairs(n)) == 1) == prime, n
    for n in range(2, 9):
        assert q0101.brute_pairs(n) == q0101.factor_pairs(n), n
    assert q0101.factor_pairs(4) == [((1, 2, 2, 3), (1, 3, 3, 5)), ((1, 2, 3, 4), (1, 2, 3, 4))]
    assert len(q0101.factor_pairs(8)) == 4
    for n in range(4, 31):    # the pair 1 + u + w and 1 + p v + m z for n = p m
        for p in range(2, n):
            if n % p or n // p < 2:
                continue
            m = n // p
            a = sorted(1 + u + w for u in range(p) for w in range(m))
            b = sorted(1 + p * v + m * z for v in range(m) for z in range(p))
            assert q0101.same(a, b) and a != list(range(1, n + 1)), (n, p)
    # the traps: faces up to 11 for two dice (Sicherman has 8), 16 for three, 18 with a face 0;
    # Sicherman and a standard die in six orders
    assert max(SICH[1]) == 8 <= 11 == 12 - 1
    assert max(max(d) for s in q0101.factor_sets(3) for d in s) <= 16 == 18 - 2
    assert max(max(d) for s in q0101.factor_sets(3, 0) for d in s) <= 18
    assert len(set(permutations(SICH3))) == 6
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


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(101)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(101)
    cases = []
    for _ in range(200):
        cases.append([[rng.randint(0, 20) for _ in range(6)], [rng.randint(0, 20) for _ in range(6)]])
    for (a, b) in [SICH, *ZERO]:
        cases.append([list(a), list(b)])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([a, b]) => [m.scSums(a, b), m.scDiff(a, b)])));")
    want = q0101.sums(STD6, STD6)
    for (a, b), (sums, diff) in zip(cases, got):
        ref = q0101.sums(a, b)
        assert sums == [ref.get(s, 0) for s in range(max(a) + max(b) + 1)]
        assert diff == sorted(s for s in set(ref) | set(want) if ref[s] != want[s])
    levels = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(Array.from({length: 45}, (_, s) => [m.scLevel(s, 6), m.scHue(s, 6)])));")
    assert levels == [[q0101.level(s, 6), q0101.hue(s, 6)] for s in range(45)]
    pairs, tries = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([m.scPairs, m.scTries]));")
    assert sorted(tuple(sorted((tuple(a), tuple(b)))) for _, a, b in pairs) == q0101.factor_pairs(6, 0)
    assert [p[0] for p in pairs][:2] == ["רגילות", "‏Sicherman"]
    (name, a, b), = tries
    assert a == [1, 1, 2, 3, 4, 5] and b == list(STD6) and not q0101.same(a, b)
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['1.2.2.3.3.4', '0.20.3.4.5.6', '1.2.3', '1.21.3.4.5.6', '1.x.3.4.5.6', '', '1.2.3.4.5.6.7.8'].map((t) => m.scParse(t))));")
    assert parsed == [[1, 2, 2, 3, 3, 4], [0, 20, 3, 4, 5, 6], None, None, None, None, None]
