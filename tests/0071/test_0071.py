"""Question 0071: the page's first_round against the exact backward induction of the
generator (every option kept) and against a Monte Carlo run of the same policies; the
page's numbers (513/805 in parts a and b, 13101/20125 in part c, part d's 91/220, 233/550,
1187/2750 and the snipers' 0.4, 0.08, 0.6, 0.12) and the closed forms of the steps; the
general maxima of the three positions on a grid; the follow-ups; best_wand; the
explorer's JavaScript; and the page copies of the blocks."""

import json
import random
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0071  # noqa: E402

ns = load_python(71)
first_round, best_wand, duel = ns["first_round"], ns["best_wand"], ns["duel"]
F, G, E, H = q0071.F, q0071.G, q0071.EPS, Fr(1, 2)


def near(x, y, tol=1e-9):
    return abs(float(x) - float(y)) < tol


def test_duel_formula():
    for x, y in [(0.6, 0.8), (0.3, 0.3), (1.0, 0.5), (0.1, 0.9)]:
        series = sum(((1 - x) * (1 - y)) ** k * x for k in range(2000))      # the opener hits at round k
        assert near(duel(x, y), series) and near(duel(x, y), F(Fr(x), Fr(y)), 1e-12)
        assert F(Fr(x), Fr(y)) + G(Fr(x), Fr(y)) == 1


def test_page_matches_the_reference():
    rng = random.Random(60)
    for _ in range(3000):
        p = [rng.randint(1, 100) / 100 for _ in range(3)]
        if len(set(p)) < 3:
            continue
        want, _ = q0071.round_options([Fr(x) for x in p])
        assert all(near(a, b) for a, b in zip(first_round(p), want)), p


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
    a, b, c = Fr(6, 10), Fr(6, 10), Fr(8, 10)                  # the steps' closed forms
    assert F(a, b) == Fr(5, 7) and F(a, c) == Fr(15, 23) and G(a, a) == Fr(2, 7) and c * F(a, c) == Fr(12, 23)
    assert b * F(a, b) + (1 - b) * c * F(a, c) == Fr(513, 805)
    V3 = c * F(a, c) + (1 - c) * a * G(a, a)
    assert a * F(a, a) + (1 - a) * V3 == Fr(13101, 20125)
    assert (1 - c) * a * F(a, a) == Fr(3, 35) and near(G(c, a), Fr(3, 23)) and near(c * F(a, c) + (1 - c) * a, 0.6417, 1e-4)
    x, y = Fr(4, 10), Fr(8, 10)
    assert F(x, y) == Fr(5, 11) and F(x, x) == Fr(5, 8) and G(x, x) == Fr(3, 8)
    assert x * G(x, x) + (1 - x) * x * F(x, x) == Fr(3, 10) and x * F(x, x) + (1 - x) * x * G(x, x) == Fr(34, 100)
    for k in range(1, 100):                                       # the "fact" of part a
        for j in range(1, 100):
            b, c = Fr(k, 100), Fr(j, 100)
            assert c * F(b, c) - G(c, b) == b * (2 * c - 1) / (b + c - b * c)
    for k in range(1, 20):                                        # equal rivals: W1 = p
        p = Fr(k, 20)
        assert p * F(p, p) + (1 - p) * p * F(p, p) == p


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
            W1 = x * F(m, x) + (1 - x) * y * F(m, y)
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
    a, b, c = Fr(6, 10), Fr(6, 10), Fr(8, 10)
    W1 = b * F(a, b) + (1 - b) * c * F(a, c)
    assert near(a * G(b, a) + (1 - a) * W1, 0.4263, 1e-4)
    # the cat rule in every round, position 1: max(m (1 - (1-b)(1-c)), 1 - m)
    assert near(Fr(6, 10) * (1 - Fr(4, 10) * Fr(2, 10)), 0.552) and near(Fr(6, 10) * (1 - Fr(3, 10) * Fr(1, 10)), 0.582)
    # the narrow band of position 2: a = 0.3, c = 0.4
    band = q0071.win(2, Fr(906, 1000), (Fr(3, 10), Fr(4, 10)))
    assert near(band, 0.615, 1e-3) and q0071.win(2, Fr(1), (Fr(3, 10), Fr(4, 10))) == Fr(49, 100)


def test_best_wand():
    for me, rivals, chance, wand in [(1, [0.6, 0.8], 513 / 805, 0.6), (2, [0.6, 0.8], 513 / 805, 0.6),
                                     (3, [0.6, 0.8], 13101 / 20125, 0.6), (1, [0.8, 0.4], 0.6, 1.0),
                                     (2, [0.8, 0.4], 233 / 550, 0.4), (3, [0.8, 0.4], 1187 / 2750, 0.4)]:
        got, q = best_wand(me, rivals)
        assert abs(got - chance) < 1e-6 and abs(q - wand) < 1e-6, (me, rivals, got, q)


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
