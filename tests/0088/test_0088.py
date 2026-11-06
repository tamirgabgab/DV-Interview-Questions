"""Question 0088: differences in a circle (the Ducci sequence). Every number on the page is
recomputed with the generator's reference (part a: the run of 2, 6, 11, 4 and the parity after
four rounds; part b: every start of 4 and 8 numbers with small values reaches zeros within
n(floor(log2 M) + 1) rounds, the binomials of row 2^k, a single 1 vanishing mod 2 exactly
when n is a power of 2; part c: a start that never reaches zeros for every other n, every
orbit entering a cycle of 0 and one number c, the table of cycle lengths; the follow-ups:
the Tribonacci starts and the real start that keeps its shape); the generated blocks are
checked; and the box's model is compared under Node with this reference."""

import itertools
import math
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0088  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0088-ducci-differences.md").read_text(encoding="utf-8")


def test_part_a_run():
    tail, period, seq = q0088.orbit(q0088.START)
    assert (tail, period) == (6, 1)
    assert seq[1] == (4, 5, 7, 2)
    assert seq[4] == (2, 0, 2, 0) and all(x % 2 == 0 for x in seq[4])
    assert [max(s) for s in seq] == [11, 7, 5, 3, 2, 2, 0]
    assert q0088.bound(q0088.START) == 16
    assert q0088.step((2, 0, 2, 0)) == (2, 2, 2, 2)          # the max can stand still


def test_part_a_four_rounds_make_everything_even():
    for v in itertools.product(range(8), repeat=4):
        w = v
        for _ in range(4):
            w = q0088.step(w)
        assert all(x % 2 == 0 for x in w), v


def test_part_b_powers_of_two_reach_zero_within_the_bound():
    for n, vals in ((2, range(12)), (4, range(9)), (8, range(3))):
        for v in itertools.product(vals, repeat=n):
            s = q0088.steps_to_zero(v)
            assert s is not None, v
            if any(v):
                assert s <= q0088.bound(v), v
            maxes = [max(x) for x in q0088.orbit(v)[2]]
            assert all(a >= b for a, b in zip(maxes, maxes[1:])), v


def test_part_b_binomials_and_single_one():
    for k in range(1, 7):
        n = 2 ** k
        assert all(math.comb(n, j) % 2 == 0 for j in range(1, n))
    for n in range(2, 65):
        b = 1
        for _ in range(n):
            b = q0088.parity_step(b, n)
        assert (b == 0) == q0088.power_of_two(n), n
        if n <= 18:                     # longer circles have huge cycles (19 numbers: 2^18 - 1)
            assert (q0088.steps_to_zero(tuple(1 if i == 0 else 0 for i in range(n))) is not None) == q0088.power_of_two(n), n
    # the parity of a single 1 after t rounds is row t of Pascal's triangle mod 2, wrapped
    rows = q0088.single_one_rows(8, 8)
    for t, row in enumerate(rows):
        want = [0] * 8
        for j in range(t + 1):
            want[(7 - j) % 8] ^= math.comb(t, j) % 2       # x_i takes x_{i+j}: the 1 at x_8 reaches x_{8-j}
        assert row == want, t
    assert not any(rows[8]) and all(any(r) for r in q0088.single_one_rows(6, 8))


def test_part_c_never_zero_for_other_n():
    for n in list(range(3, 19)) + [20, 24]:
        if q0088.power_of_two(n):
            continue
        m = n
        while m % 2 == 0:
            m //= 2
        v = tuple(1 if i % m == 0 else 0 for i in range(n))      # a 1 at every m-th place
        assert q0088.steps_to_zero(v) is None, n
        # on an odd circle, every 0/1 start other than zeros and all ones never reaches zeros
        if n % 2 and n <= 11:
            for w in itertools.product((0, 1), repeat=n):
                if 0 < sum(w) < n:
                    assert q0088.steps_to_zero(w) is None, w
    assert q0088.orbit((0, 0, 1))[:2] == (1, 3)
    assert q0088.orbit(q0088.N3)[:2] == (2, 3)


def test_part_c_cycles_are_zero_and_one_number():
    for n in range(3, 11):
        vals = range(4) if n <= 7 else range(3)
        lens = set()
        for v in itertools.product(vals, repeat=n):
            tail, period, seq = q0088.orbit(v)
            lens.add(period)
            for w in seq[tail:]:
                assert len({x for x in w if x}) <= 1, (v, w)
        assert lens == set(q0088.cycle_lengths(n)), n


def test_part_c_table():
    want = {3: [3], 4: [], 5: [15], 6: [3, 6], 7: [7], 8: [], 9: [3, 63], 10: [15, 30]}
    for n, w in want.items():
        assert [x for x in q0088.cycle_lengths(n) if x > 1] == w, n
    singles = {n: q0088.orbit(tuple(1 if i == 0 else 0 for i in range(n)))[1] for n in want}
    assert singles == {3: 3, 4: 1, 5: 15, 6: 6, 7: 7, 8: 1, 9: 63, 10: 30}
    tail, period, _ = q0088.orbit((1, 2, 3, 4, 5))
    assert (tail, period) == (2, 15) and tail + period == 17


def test_follow_ups():
    assert q0088.steps_to_zero(q0088.TRIB) == 13
    assert q0088.steps_to_zero(q0088.TRIB_BIG) == 25
    assert q0088.bound(q0088.TRIB) == 24 and q0088.bound(q0088.TRIB_BIG) == 56
    # the real start 1, q, q^2, q^3 keeps its shape: after a round it is the same up to scale
    q = 1.0
    for _ in range(200):
        q = 1 + 1 / q + 1 / q ** 2                                  # q^3 = q^2 + q + 1
    assert abs(q - 1.839286755) < 1e-8
    v = [1, q, q * q, q ** 3]
    for _ in range(6):
        w = [abs(v[i] - v[(i + 1) % 4]) for i in range(4)]
        a, b = sorted(v), sorted(w)
        assert all(abs(b[i] / b[0] - a[i] / a[0]) < 1e-6 for i in range(4))
        assert min(w) > 0
        v = w


def test_page_text():
    for words in ["אחרי **6 סיבובים**", "\\( 4(\\lfloor \\log_2 M \\rfloor + 1) \\)", "החסם הוא 16",
                  "\\( n(\\lfloor \\log_2 M \\rfloor + 1) \\)", "מחזור באורך 3", "לוקחים\n            13 סיבובים",
                  "לוקחים 25", "\\( q \\approx 1.839 \\)", "ל-1 עד 5 זה 17", "המחזור באורך 15",
                  "\\( n = 10 \\)"]:
        assert words in PAGE, words


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(88)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [list(q0088.START), list(q0088.TRIB), list(q0088.TRIB_BIG), [0, 0, 1], [1, 2, 3, 4, 5],
             [3, 1, 4, 1, 5, 9, 2, 6], [1, 0, 0, 0, 0, 0], [7, 0, 3, 3, 9, 1, 4, 4, 2]]
    cases += [list(v) for v in itertools.product(range(3), repeat=5)][:60]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    "console.log(JSON.stringify({"
                    "orb: cases.map((v) => { const o = m.duOrbit(v); return [o.tail, o.period, o.states]; }),"
                    "zero: Array.from({ length: 30 }, (_, i) => m.duAlwaysZero(i + 2)),"
                    "parse: [m.duParse('2 6 11 4'), m.duParse('1,2'), m.duParse('1, 2, 3'), m.duParse('a b c')],"
                    "}));")
    for v, (tail, period, states) in zip(cases, got["orb"]):
        t, p, seq = q0088.orbit(v)
        assert (tail, period) == (t, p), v
        assert [tuple(s) for s in states] == seq, v
    assert got["zero"] == [q0088.power_of_two(n) for n in range(2, 32)]
    assert got["parse"] == [[2, 6, 11, 4], None, [1, 2, 3], None]
