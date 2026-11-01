"""Question 0071: the exact backward induction of the generator (every option kept) against
a Monte Carlo run of the same policies; the page's numbers (513/805 in parts a and b,
13101/20125 in part c, part d's 91/220, 233/550, 1187/2750 and the snipers' 0.4, 0.08, 0.6,
0.12), the closed forms and inequalities of every step, written with p1, p2, p3 and V; the
general maxima of the three positions on a grid; the follow-ups; the explorer's JavaScript;
and the page copies of the blocks. The page has no code: the reference is
tools/figures/q0071.py."""

import json
import random
import sys
from fractions import Fraction as Fr

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0071  # noqa: E402

V, E, H = q0071.F, q0071.EPS, Fr(1, 2)


def near(x, y, tol=1e-9):
    return abs(float(x) - float(y)) < tol


def test_duel_formula():
    """V(x, y) = x + (1-x)(1-y) V: the sum over the round in which the opener first hits."""
    for x, y in [(0.6, 0.8), (0.3, 0.3), (1.0, 0.5), (0.1, 0.9)]:
        series = sum(((1 - x) * (1 - y)) ** k * x for k in range(2000))
        assert near(V(Fr(x), Fr(y)), series)
        assert V(Fr(x), Fr(y)) + q0071.G(Fr(x), Fr(y)) == 1


def test_monte_carlo():
    """The chances of the reference by playing the game itself with its round-1 choices."""
    rng = random.Random(61)
    for p in ([0.6 - 1e-9, 0.6, 0.8], [0.6, 0.6 - 1e-9, 0.8], [0.6, 0.8, 0.6 - 1e-9], [1.0, 0.8, 0.4], [0.8, 0.4, 0.4 - 1e-9]):
        want, trace = q0071.round_options([Fr(x) for x in p])
        choice = {w: best for w, _, best in trace}
        wins, n = [0, 0, 0], 40000
        for _ in range(n):
            alive, winner = [0, 1, 2], None
            for w in (0, 1, 2):                                  # the first round
                t = choice[w + 1]
                if t != "air" and rng.random() < p[w]:
                    alive.remove(t - 1)
                    o = alive[0] if alive[0] != w else alive[1]
                    turn = o
                    while winner is None:                          # the duel, o first
                        if rng.random() < p[turn]:
                            winner = turn
                        turn = w if turn == o else o
                    break
            if winner is not None:
                wins[winner] += 1
        for k in range(3):
            assert abs(wins[k] / n - float(want[k])) < 0.012, (p, k, wins[k] / n, float(want[k]))


def test_page_numbers():
    rv, rd = q0071.RIVALS, q0071.RIVALS_D
    w = lambda me, own, r: q0071.win(me, own, r)              # noqa: E731
    assert near(w(1, Fr(6, 10) - E, rv), Fr(513, 805)) and near(w(2, Fr(6, 10) - E, rv), Fr(513, 805))
    assert near(w(3, Fr(6, 10) - E, rv), Fr(13101, 20125))
    assert w(1, Fr(1), rv) == Fr(2, 5) == w(2, Fr(1), rv) and w(3, Fr(1), rv) == Fr(2, 25)
    assert near(w(1, Fr(4, 10) - E, rd), Fr(91, 220)) and w(1, Fr(1), rd) == Fr(3, 5)
    assert near(w(2, Fr(4, 10) - E, rd), Fr(233, 550)) and w(2, Fr(1), rd) == Fr(3, 25)
    assert near(w(3, Fr(4, 10) - E, rd), Fr(1187, 2750)) and w(3, Fr(1), rd) == Fr(3, 25)


def one_minus_v(x, y):
    """The second wizard of a duel wins: 1 - V(x, y) = (1 - x) y / (x + y - xy)."""
    return 1 - V(x, y)


def test_steps_of_part_a():
    p2, p3 = Fr(6, 10), Fr(8, 10)
    # step 1: the four duels
    assert V(p2, p3) == Fr(15, 23) and V(p3, p2) == Fr(20, 23) and V(p2, p2) == Fr(5, 7)
    # step 2: wizard 3 aims at me exactly when p1 > p2 (= 0.6)
    for k in range(1, 100):
        p1 = Fr(k, 100)
        at_me, at_2 = p3 * one_minus_v(p2, p3), p3 * one_minus_v(p1, p3)
        assert (at_2 < at_me) == (p1 > p2) or p1 == p2
        assert at_me == p3 * Fr(8, 23)
    # step 3: A = 12/23, D1 = 3/23, and D3 > A only below 11/31 (6.6 > 18.6 p1)
    A = p3 * V(p2, p3)
    assert A == Fr(12, 23) and one_minus_v(p3, p2) == Fr(3, 23)
    for k in range(1, 100):
        p1 = Fr(k, 100)
        assert one_minus_v(p1, p2) == p2 * (1 - p1) / (p2 + (1 - p2) * p1)
        assert (one_minus_v(p1, p2) > A) == (p1 < Fr(11, 31))
    # step 4: H3 > H2 for every wand; step 5: W > H3 (p2 >= 1/2), W rises, the limit 513/805
    W = lambda p1: p2 * V(p1, p2) + (1 - p2) * p3 * V(p1, p3)      # noqa: E731
    prev = 0
    for k in range(1, 60):
        p1 = Fr(k, 100)
        H3, H2 = one_minus_v(p2, p1), one_minus_v(p3, p1)
        assert H3 > H2 and W(p1) > H3 and W(p1) > prev
        assert W(p1) == Fr(6, 10) * p1 / (Fr(6, 10) + Fr(4, 10) * p1) + Fr(32, 100) * p1 / (Fr(8, 10) + Fr(2, 10) * p1)
        prev = W(p1)
    assert V(p2, p2) == 1 / (2 - p2)
    weak = p2 / (2 - p2) + (1 - p2) * p3 * V(p2, p3)
    assert weak == Fr(36, 84) + Fr(192, 920) == Fr(3, 7) + Fr(24, 115) == Fr(513, 805) == W(p2)
    # step 6: p1 H3 = 0.4 p1^2 / (0.6 + 0.4 p1), rising to 1 - p2 at p1 = 1
    for k in range(61, 101):
        p1 = Fr(k, 100)
        assert p1 * one_minus_v(p2, p1) == Fr(4, 10) * p1 ** 2 / (Fr(6, 10) + Fr(4, 10) * p1) <= Fr(4, 10)
        assert near(q0071.win(1, p1, q0071.RIVALS), p1 * one_minus_v(p2, p1))
    assert 1 * one_minus_v(p2, 1) == 1 - p2


def test_steps_of_parts_b_and_c():
    p1, p3 = Fr(6, 10), Fr(8, 10)                                  # part b: I am wizard 2
    for k in range(1, 60):
        p2 = Fr(k, 100)
        A, H3, H1 = p3 * V(p2, p3), one_minus_v(p1, p2), one_minus_v(p3, p2)
        assert A > H3 > H1
        assert one_minus_v(p2, p1) > one_minus_v(p3, p1)          # wizard 1 aims at 3
    assert p1 / (2 - p1) + (1 - p1) * p3 * V(p1, p3) == Fr(513, 805)
    assert p1 * (1 - p3) >= 1 - 2 * p3 and one_minus_v(p3, p1) == Fr(3, 23)   # the sniper: wizard 1 waits
    p1, p2 = Fr(6, 10), Fr(8, 10)                                  # part c: I am wizard 3
    for k in range(1, 60):
        p3 = Fr(k, 100)
        assert p3 * one_minus_v(p2, p3) < p3 * one_minus_v(p1, p3)  # I aim at 2
        assert one_minus_v(p3, p2) > one_minus_v(p1, p2)            # 2 aims at 1
        R1 = (1 - p2) * p3 * V(p1, p3)
        assert one_minus_v(p3, p1) > R1                             # 1 aims at 2
        W = p1 * V(p3, p1) + (1 - p1) * (p2 * V(p3, p2) + (1 - p2) * p3 * one_minus_v(p1, p3))
        assert near(q0071.win(3, p3, q0071.RIVALS), W)
    assert (1 - p2) * Fr(6, 10) * V(p1, p1) == Fr(3, 35) and one_minus_v(p1, p1) == Fr(2, 7)
    R1 = p2 * V(p1, p2) + (1 - p2) * p1                             # the sniper
    assert near(R1, 0.6417, 1e-4) and one_minus_v(p2, p1) == Fr(3, 23)
    assert (1 - p2) * (1 - p1) == Fr(2, 25)


def test_steps_of_part_d():
    x, y = Fr(4, 10), Fr(8, 10)
    assert V(x, y) == Fr(5, 11) and V(x, x) == Fr(5, 8) and one_minus_v(x, x) == Fr(3, 8)
    for k in range(1, 100):                                       # the fact of step 1
        for j in range(1, 100):
            p2, p3 = Fr(k, 100), Fr(j, 100)
            assert p3 * V(p2, p3) - one_minus_v(p3, p2) == p2 * (2 * p3 - 1) / (p2 + p3 - p2 * p3)
    assert y * V(x, y) + (1 - y) * x * V(x, x) == Fr(91, 220) and one_minus_v(x, x) < Fr(91, 220)
    assert x * Fr(3, 8) + (1 - x) * x * V(x, x) == Fr(3, 10) and y * V(x, y) + (1 - y) * Fr(3, 10) == Fr(233, 550)
    assert x * V(x, x) + (1 - x) * x * one_minus_v(x, x) == Fr(34, 100) and y * V(x, y) + (1 - y) * Fr(34, 100) == Fr(1187, 2750)
    assert V(x, 1) == x and (1 - y) * (1 - x) == Fr(12, 100)
    for k in range(1, 20):                                        # equal rivals (a follow-up): W = q
        q = Fr(k, 20)
        assert q * V(q, q) + (1 - q) * q * V(q, q) == q


def test_who_wins_adds_up():
    for me in (1, 2, 3):
        for rivals in (q0071.RIVALS, q0071.RIVALS_D):
            for own in (q0071.weak(rivals), Fr(59, 100), Fr(1)):
                p = q0071.place(me, own, rivals)
                ways, cats = q0071.outcomes(p)
                chances = q0071.round_options(p)[0]
                total = [Fr(0)] * 3
                for k, v, pr in ways:
                    s = 3 - k - v
                    total[s] += pr * V(p[s], p[k])
                    total[k] += pr * one_minus_v(p[s], p[k])
                assert total == chances and sum(chances) + cats == 1
    p = q0071.place(1, q0071.weak(q0071.RIVALS), q0071.RIVALS)
    ch, cats = q0071.round_options(p)[0], q0071.outcomes(p)[1]
    assert near(ch[1], Fr(6, 35)) and near(ch[2], Fr(32, 100) * Fr(8, 23)) and near(cats, Fr(8, 100))


def test_the_table_of_part_a():
    _, trace = q0071.round_options(q0071.place(1, Fr(6, 10) - E, q0071.RIVALS))
    assert [(w, best) for w, _, best in trace] == [(3, 2), (2, 3), (1, "air")]
    _, trace = q0071.round_options(q0071.place(1, Fr(1), q0071.RIVALS))
    assert [(w, best) for w, _, best in trace] == [(3, 1), (2, "air"), (1, 3)]
    assert near(q0071.win(1, Fr(6, 10) + E, q0071.RIVALS), 0.1714, 1e-4)     # the trap: just above


def test_general_maxima():
    """P1 = max(W1(m-), 1 - m) on a grid; positions 2 and 3: the best is at m-, 0.5- or 1
    except the narrow band of position 2 and one point of position 3."""
    vals = [Fr(k, 10) for k in range(1, 10)]
    for x in vals:
        for y in vals:
            if x == y:
                continue
            m = min(x, y)
            best = q0071.best_on_grid(1, (x, y), 200)[0]
            W1 = x * V(m, x) + (1 - x) * y * V(m, y)
            assert near(best, max(W1, 1 - m), 1e-6), (x, y)
            for me in (2, 3):
                best = q0071.best_on_grid(me, (x, y), 200)[0]
                cand = max(v for _, _, v in q0071.candidates(me, (x, y)))
                if me == 2 and x < y < H:
                    assert best >= cand - Fr(1, 10**9)
                else:
                    assert near(best, cand, 1e-6), (me, x, y)


def test_follow_ups():
    orig = (Fr(7, 10), Fr(9, 10))
    assert near(q0071.win(1, Fr(6, 10), orig), 0.6460, 1e-4) and near(q0071.win(1, Fr(8, 10), orig), 0.2043, 1e-4)
    assert q0071.win(1, Fr(1), orig) == Fr(3, 10) and near(q0071.win(1, Fr(7, 10) - E, orig), 0.7333, 1e-4)
    # no deliberate miss in part a: I shoot at 3 at a just under 0.6
    p1, p2, p3 = Fr(6, 10), Fr(6, 10), Fr(8, 10)
    W = p2 * V(p1, p2) + (1 - p2) * p3 * V(p1, p3)
    assert near(p1 * one_minus_v(p2, p1) + (1 - p1) * W, 0.4263, 1e-4)
    # the cat rule in every round, position 1: max(m (1 - (1-b)(1-c)), 1 - m)
    assert near(Fr(6, 10) * (1 - Fr(4, 10) * Fr(2, 10)), 0.552) and near(Fr(6, 10) * (1 - Fr(3, 10) * Fr(1, 10)), 0.582)
    # the narrow band of position 2: a = 0.3, c = 0.4
    band = q0071.win(2, Fr(906, 1000), (Fr(3, 10), Fr(4, 10)))
    assert near(band, 0.615, 1e-3) and q0071.win(2, Fr(1), (Fr(3, 10), Fr(4, 10))) == Fr(49, 100)


def test_best_wand():
    for me, rivals, chance, wand in [(1, (0.6, 0.8), Fr(513, 805), 0.6), (2, (0.6, 0.8), Fr(513, 805), 0.6),
                                     (3, (0.6, 0.8), Fr(13101, 20125), 0.6), (1, (0.8, 0.4), Fr(3, 5), 1.0),
                                     (2, (0.8, 0.4), Fr(233, 550), 0.4), (3, (0.8, 0.4), Fr(1187, 2750), 0.4)]:
        got, q = q0071.best_on_grid(me, tuple(Fr(r).limit_denominator(10) for r in rivals), 1000)
        assert near(got, chance) and near(q, wand, 1e-6), (me, rivals, float(got), float(q))


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(62)
    cases = [[rng.randint(1, 100) / 100 for _ in range(3)] for _ in range(200)] + [[0.6 - 1e-9, 0.6, 0.8], [1, 0.8, 0.4]]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((p) => m.wzRound(p))));""")
    for p, g in zip(cases, got):
        if len(set(p)) < 3:
            continue
        want, trace = q0071.round_options([Fr(x) for x in p])
        assert all(near(a, b) for a, b in zip(g["win"], want)), p
        assert [t["choice"] for t in g["trace"]] == [str(best) for _, _, best in trace], p


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(71)
