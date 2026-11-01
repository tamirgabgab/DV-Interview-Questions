"""Question 0071: the exact backward induction of the generator (every option kept) against
a Monte Carlo run of the same policies; the page's numbers (part a: 513/805 and the others'
6/35, 64/575, 2/25; part b: the six orders and 13101/20125 with 36/175, 64/575, 4/125;
part c: the two plans, their closed forms and the threshold), the inequality of every step;
the rule of part c against every place, order and wand on a grid of rival pairs; the
follow-ups; the explorer's JavaScript; and the page copies of the blocks. The page has no
code: the reference is tools/figures/q0071.py."""

import json
import math
import random
import sys
from fractions import Fraction as Fr

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0071  # noqa: E402

V, E = q0071.F, q0071.EPS
R = q0071.RIVALS


def near(x, y, tol=1e-9):
    return abs(float(x) - float(y)) < tol


def one_minus_v(x, y):
    """The second wizard of a duel wins: 1 - V(x, y) = (1 - x) y / (x + y - xy)."""
    return 1 - V(x, y)


def test_duel_formula():
    """V(x, y) = x + (1-x)(1-y) V: the sum over the round in which the opener first hits."""
    for x, y in [(0.6, 0.8), (0.3, 0.3), (1.0, 0.5), (0.1, 0.9)]:
        series = sum(((1 - x) * (1 - y)) ** k * x for k in range(2000))
        assert near(V(Fr(x), Fr(y)), series)
        assert V(Fr(x), Fr(y)) + q0071.G(Fr(x), Fr(y)) == 1


def test_monte_carlo():
    """The chances of the reference by playing the game itself with its round-1 choices."""
    rng = random.Random(61)
    for p in ([0.6 - 1e-9, 0.6, 0.8], [0.6, 0.8, 0.6 - 1e-9], [0.8, 0.6, 0.6 - 1e-9], [1.0, 0.8, 0.4], [0.47, 0.9, 0.47 - 1e-9]):
        want, trace = q0071.round_options([Fr(x) for x in p])
        choice = {w: best for w, _, best in trace}
        wins, cats, n = [0, 0, 0], 0, 40000
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
            else:
                cats += 1
        for k in range(3):
            assert abs(wins[k] / n - float(want[k])) < 0.012, (p, k, wins[k] / n, float(want[k]))
        assert abs(cats / n - float(q0071.outcomes([Fr(x) for x in p])[1])) < 0.012


def test_steps_of_part_a():
    p2, p3 = Fr(6, 10), Fr(8, 10)
    # step 1: the duels, mine as functions of p1
    assert V(p2, p3) == Fr(15, 23) and V(p3, p2) == Fr(20, 23) and V(p2, p2) == Fr(5, 7)
    for k in range(1, 100):
        p1 = Fr(k, 100)
        assert V(p1, p2) == p1 / (Fr(6, 10) + Fr(4, 10) * p1) and V(p1, p3) == p1 / (Fr(8, 10) + Fr(2, 10) * p1)
        assert one_minus_v(p1, p2) == Fr(6, 10) * (1 - p1) / (Fr(6, 10) + Fr(4, 10) * p1)
    # step 2: wizard 3 aims at me exactly when p1 > 0.6
    for k in range(1, 100):
        p1 = Fr(k, 100)
        at_me, at_2 = p3 * one_minus_v(p2, p3), p3 * one_minus_v(p1, p3)
        assert at_me == p3 * Fr(8, 23)
        assert (at_2 < at_me) == (p1 > p2) or p1 == p2
        assert (Fr(8, 10) * (1 - p1) / (Fr(8, 10) + Fr(2, 10) * p1) < Fr(8, 23)) == (Fr(184, 10) - Fr(184, 10) * p1 < Fr(64, 10) + Fr(16, 10) * p1) == (p1 > p2)
    # step 3: A = 12/23, D1 = 3/23, and hitting 3 beats the air only below 11/31 (6.6 > 18.6 p1)
    A = p3 * V(p2, p3)
    assert A == Fr(12, 23) and one_minus_v(p3, p2) == Fr(3, 23) and near(Fr(11, 31), 0.355, 1e-3)
    for k in range(1, 100):
        p1 = Fr(k, 100)
        assert (one_minus_v(p1, p2) > A) == (p1 < Fr(11, 31))
    # steps 4-5: H3 > H2 always, W > H3, W rises; step 6: P(p1) <= 0.4
    W = lambda p1: p2 * V(p1, p2) + (1 - p2) * p3 * V(p1, p3)      # noqa: E731
    prev = 0
    for k in range(1, 60):
        p1 = Fr(k, 100)
        H3, H2 = one_minus_v(p2, p1), one_minus_v(p3, p1)
        assert H3 == Fr(4, 10) * p1 / (Fr(6, 10) + Fr(4, 10) * p1) and H2 == Fr(2, 10) * p1 / (Fr(8, 10) + Fr(2, 10) * p1)
        assert H3 > H2 and W(p1) > H3 and W(p1) > prev
        assert W(p1) == Fr(6, 10) * p1 / (Fr(6, 10) + Fr(4, 10) * p1) + Fr(32, 100) * p1 / (Fr(8, 10) + Fr(2, 10) * p1)
        assert near(q0071.win(1, p1, R), W(p1))
        prev = W(p1)
    for k in range(61, 101):
        p1 = Fr(k, 100)
        assert p1 * one_minus_v(p2, p1) == Fr(4, 10) * p1 ** 2 / (Fr(6, 10) + Fr(4, 10) * p1) <= Fr(4, 10)
        assert near(q0071.win(1, p1, R), p1 * one_minus_v(p2, p1))
    # step 7: the limit
    assert W(p2) == Fr(3, 7) + Fr(24, 115) == Fr(513, 805)
    # step 8: the others and the cats at the best wand
    ch = q0071.round_options(q0071.place(1, q0071.weak(R), R))[0]
    cats = q0071.outcomes(q0071.place(1, q0071.weak(R), R))[1]
    assert near(ch[0], Fr(513, 805)) and near(ch[1], Fr(6, 35)) and near(ch[2], Fr(64, 575)) and cats == Fr(2, 25)
    assert Fr(6, 10) * Fr(2, 7) == Fr(6, 35) and Fr(32, 100) * Fr(8, 23) == Fr(64, 575)
    assert [Fr(513, 805) * 4025, Fr(6, 35) * 4025, Fr(64, 575) * 4025, Fr(2, 25) * 4025] == [2565, 690, 448, 322]
    assert 2565 + 690 + 448 + 322 == 4025


def test_the_choices_of_part_a():
    _, trace = q0071.round_options(q0071.place(1, Fr(6, 10) - E, R))
    assert [(w, best) for w, _, best in trace] == [(3, 2), (2, 3), (1, "air")]
    _, trace = q0071.round_options(q0071.place(1, Fr(1), R))
    assert [(w, best) for w, _, best in trace] == [(3, 1), (2, "air"), (1, 3)]
    assert near(q0071.win(1, Fr(6, 10) + E, R), 0.1714, 1e-4)     # the trap: just above
    assert q0071.win(1, Fr(1), R) == Fr(2, 5)


def test_the_six_orders():
    rows = q0071.orders(R)
    got = {(me, tuple(float(x) for i, x in enumerate(p) if i != me - 1)): (q, ch, cats) for p, me, q, ch, cats in rows}
    want = {(1, (0.6, 0.8)): (0.6373, 0.1714, 0.1113, 0.08), (1, (0.8, 0.6)): (0.6075, 0.2783, 0.0343, 0.08),
            (2, (0.6, 0.8)): (0.6373, 0.1714, 0.1113, 0.08), (2, (0.8, 0.6)): (0.6075, 0.2783, 0.0343, 0.08),
            (3, (0.6, 0.8)): (0.6510, 0.2057, 0.1113, 0.032), (3, (0.8, 0.6)): (0.5560, 0.2783, 0.0857, 0.08)}
    for key, (m, r1, r2, c) in want.items():
        q, ch, cats = got[key]
        me = key[0]
        others = [ch[i] for i in range(3) if i != me - 1]
        assert near(q, 0.6, 1e-6)                                  # the best wand is 0.6- in every order
        assert near(ch[me - 1], m, 1e-4) and near(others[0], r1, 1e-4) and near(others[1], r2, 1e-4) and near(cats, c, 1e-9)
        assert near(sum(ch) + cats, 1)
    best = max(rows, key=lambda r: r[3][r[1] - 1])
    assert best[1] == 3 and [float(x) for x in best[0][:2]] == [0.6, 0.8]
    assert near(best[3][2], Fr(13101, 20125))
    # the orders where 0.8 shoots before 0.6, exactly
    assert near(q0071.win(1, Fr(6, 10) - E, (Fr(8, 10), Fr(6, 10))), Fr(12, 23) + Fr(3, 35))
    assert near(q0071.win(3, Fr(6, 10) - E, (Fr(8, 10), Fr(6, 10))), Fr(2238, 4025))


def test_steps_of_part_b():
    p1, p2 = Fr(6, 10), Fr(8, 10)                                  # I am wizard 3
    for k in range(1, 60):
        p3 = Fr(k, 100)
        # step 3: I aim at 2
        assert Fr(4, 10) / (Fr(6, 10) + Fr(4, 10) * p3) > Fr(2, 10) / (Fr(8, 10) + Fr(2, 10) * p3)
        assert p3 * one_minus_v(p2, p3) < p3 * one_minus_v(p1, p3)
        # step 4: 2 aims at 1
        assert one_minus_v(p3, p2) > one_minus_v(p1, p2) == Fr(8, 23)
        # step 5: 1 aims at 2
        air = Fr(2, 10) * p3 * Fr(6, 10) / (Fr(6, 10) + Fr(4, 10) * p3)
        hit = Fr(6, 10) * (1 - p3) / (Fr(6, 10) + Fr(4, 10) * p3)
        assert air == (1 - p2) * p3 * V(p1, p3) and hit == one_minus_v(p3, p1)
        assert (hit > air) == (p3 < Fr(5, 6)) and hit > one_minus_v(p2, p1)
        # step 6: W
        Wp = Fr(6, 10) * p3 / (Fr(6, 10) + Fr(4, 10) * p3) + Fr(32, 100) * p3 / (Fr(8, 10) + Fr(2, 10) * p3) \
            + Fr(32, 1000) * p3 ** 2 / (Fr(6, 10) + Fr(4, 10) * p3)
        assert near(q0071.win(3, p3, R), Wp)
    assert one_minus_v(p1, p1) == Fr(2, 7) and (1 - p2) * Fr(6, 10) * V(p1, p1) == Fr(3, 35)
    assert Fr(6, 10) * Fr(5, 7) + Fr(32, 100) * Fr(15, 23) + Fr(48, 1000) * Fr(2, 7) == Fr(13101, 20125)
    # step 7: the sniper and the strong side
    assert q0071.win(3, Fr(1), R) == Fr(2, 25)
    _, trace = q0071.round_options(q0071.place(3, Fr(1), R))
    assert [(w, best) for w, _, best in trace] == [(3, 2), (2, 3), (1, "air")]
    for k in range(61, 101):
        assert q0071.win(3, Fr(k, 100), R) <= Fr(2, 25)
    # step 8: the others, the cats and the sum
    p = q0071.place(3, q0071.weak(R), R)
    ch, cats = q0071.round_options(p)[0], q0071.outcomes(p)[1]
    assert near(ch[0], Fr(36, 175)) and near(ch[1], Fr(64, 575)) and near(cats, Fr(4, 125))
    assert Fr(6, 10) * Fr(2, 7) + Fr(48, 1000) * Fr(5, 7) == Fr(36, 175)
    assert [Fr(13101, 20125) * 20125, Fr(36, 175) * 20125, Fr(64, 575) * 20125, Fr(4, 125) * 20125] == [13101, 4140, 2240, 644]
    assert 13101 + 4140 + 2240 + 644 == 20125


def test_part_c_closed_forms():
    """The two plans: their chances against the induction, the decisions of plan b, and the
    middle wizard's fact of step 3."""
    N = 20
    for i in range(1, N):
        for j in range(i + 1, N + 1):
            a, b = Fr(i, N), Fr(j, N)
            hide = q0071.hide_third(a, b)
            p = q0071.place(3, a - E, (a, b))
            ch, cats = q0071.round_options(p)[0], q0071.outcomes(p)[1]
            assert all(near(x, y) for x, y in zip(hide, (ch[2], ch[0], ch[1], cats))), (a, b)
            assert near(sum(hide), 1)
            _, trace = q0071.round_options(p)
            assert [(w, best) for w, _, best in trace] == [(3, 2), (2, 1), (1, 2)], (a, b)
            assert 1 - a > (1 - b) * a                                # a shoots rather than the air
            snip = q0071.sniper_first(a, b)
            assert q0071.win(1, Fr(1), (a, b)) == snip[0] == q0071.win(1, Fr(1), (b, a))
            assert q0071.round_options(q0071.place(1, Fr(1), (a, b)))[0][1] == a
    for k in range(1, 100):                                       # step 3's fact
        for j in range(1, 100):
            p2, p3 = Fr(k, 100), Fr(j, 100)
            assert p3 * V(p2, p3) - one_minus_v(p3, p2) == p2 * (2 * p3 - 1) / (p2 + p3 - p2 * p3)
    # step 8: the first term alone passes 1 - a at 2 - sqrt 2, and the threshold table
    for k in range(1, 100):
        a = Fr(k, 100)
        assert (a / (2 - a) >= 1 - a) == (a >= 2 - math.sqrt(2))
        assert a * V(a, a) == a / (2 - a)
    ts = [q0071.threshold(Fr(b, 10)) for b in (5, 6, 7, 8, 9, 10)]
    assert all(x > y for x, y in zip(ts, ts[1:]))
    assert near(ts[0], 0.4759, 1e-4) and near(ts[-1], 0.4563, 1e-4) and near(q0071.threshold(None), 0.4776, 1e-4)


def test_part_c_rule_covers_everything():
    """No place, order or wand beats max(hiding third, the sniper first): rival pairs in
    steps of 0.025, wands in steps of 0.005 and the points just under the rivals and 0.5."""
    N = 40
    for i in range(1, N):
        for j in range(i + 1, N):
            a, b = Fr(i, N), Fr(j, N)
            rule = max(q0071.hide_third(a, b)[0], 1 - a)
            top = max(q0071.best_on_grid(me, rv, 200)[0] for rv in ((a, b), (b, a)) for me in (1, 2, 3))
            assert top <= rule + Fr(1, 10**12), (a, b, float(top), float(rule))
            for me in (1, 2, 3):                                  # a sniper never gets more than 1 - a
                for rv in ((a, b), (b, a)):
                    assert q0071.win(me, Fr(1), rv) <= 1 - a


def test_examples_of_part_c():
    want = {(0.6, 0.8): ("hide", 0.6510), (0.4, 0.8): ("sniper", 0.6), (0.47, 0.9): ("hide", 0.5526),
            (0.47, 0.55): ("sniper", 0.53), (0.7, 0.9): ("hide", 0.7382)}
    for a, b in q0071.EXAMPLES:
        h, s = q0071.hide_third(a, b)[0], q0071.sniper_first(a, b)[0]
        kind, val = want[(float(a), float(b))]
        assert (kind == "hide") == (h > s) and near(max(h, s), val, 1e-4)
        top = max(q0071.best_on_grid(me, rv, 200)[0] for rv in ((a, b), (b, a)) for me in (1, 2, 3))
        assert near(top, max(h, s), 1e-9)
    assert q0071.hide_third(Fr(6, 10), Fr(8, 10)) == (Fr(13101, 20125), Fr(36, 175), Fr(64, 575), Fr(4, 125))


def test_who_wins_adds_up():
    for me in (1, 2, 3):
        for rivals in (R, (R[1], R[0]), (Fr(4, 10), Fr(8, 10))):
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
    # equal rivals: W = q
    for k in range(1, 20):
        q = Fr(k, 20)
        assert q * V(q, q) + (1 - q) * q * V(q, q) == q


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(62)
    cases = [[rng.randint(1, 100) / 100 for _ in range(3)] for _ in range(200)] + [[0.6 - 1e-9, 0.6, 0.8], [1, 0.8, 0.4]]
    pairs = [(0.6, 0.8), (0.4, 0.8), (0.45, 0.9), (0.7, 0.75), (0.25, 0.3)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{ rounds: {json.dumps(cases)}.map((p) => m.wzRound(p)),
        orders: {json.dumps(pairs)}.map(([a, b]) => m.wzOrders(a, b)) }}));""")
    for p, g in zip(cases, got["rounds"]):
        if len(set(p)) < 3:
            continue
        want, trace = q0071.round_options([Fr(x) for x in p])
        assert all(near(a, b) for a, b in zip(g["win"], want)), p
        assert [t["choice"] for t in g["trace"]] == [str(best) for _, _, best in trace], p
        assert near(g["cats"], q0071.outcomes([Fr(x) for x in p])[1]), p
    for (a, b), rows in zip(pairs, got["orders"]):
        ref = q0071.orders((Fr(a).limit_denominator(100), Fr(b).limit_denominator(100)))
        assert len(rows) == 6
        for row, (p, me, q, ch, cats) in zip(rows, ref):
            assert row["me"] == me and near(row["wand"], q, 1e-6), (a, b, row, float(q))
            assert all(near(x, y, 1e-6) for x, y in zip(row["win"], ch)) and near(row["cats"], cats, 1e-6), (a, b, me)


def test_chain_states_and_their_explanations():
    """The numbers behind each state of the chain (q0071.chain_states): the wins and the cats
    add up to the reference; the box's wzStates gives the same numbers; the explanation of a
    state quotes them; the page's chain carries the chances it is drawn from."""
    from page_tests import explorer_require, node_json

    rng = random.Random(63)
    cases = [[0.6 - 1e-9, 0.6, 0.8], [0.6, 0.8, 0.6 - 1e-9], [1, 0.8, 0.4]] + \
        [[rng.randint(1, 100) / 100 for _ in range(3)] for _ in range(80)]
    cases = [p for p in cases if len(set(p)) == 3]
    for p in cases:
        st = q0071.chain_states([Fr(x) for x in p])
        want, _ = q0071.round_options([Fr(x) for x in p])
        assert [st[f"W{k}"]["reach"] for k in (1, 2, 3)] == want, p
        assert st["CATS"]["reach"] == q0071.outcomes([Fr(x) for x in p])[1], p
    keys = ["R1", "R2", "R3", "CATS", "1,2,1", "1,2,2", "1,3,1", "1,3,3", "2,3,2", "2,3,3", "W1", "W2", "W3"]
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {json.dumps(cases)}, keys = {json.dumps(keys)};
      console.log(JSON.stringify({{ states: cases.map((p) => m.wzStates(p)),
        text: keys.map((k) => m.explainState(k, cases[0], 1).replace(/<[^>]+>/g, "")) }}));""")
    for p, g in zip(cases, got["states"]):
        st = q0071.chain_states([Fr(x) for x in p])
        for k in keys:
            assert near(g[k]["reach"], st[k]["reach"], 1e-7), (p, k)
            if "duel" in st[k]:
                assert near(g[k]["duel"], st[k]["duel"], 1e-7), (p, k)
    text = dict(zip(keys, got["text"]))
    assert "1 · (1 − 0.6) · (1 − 0.8) = 0.08" in text["CATS"]
    assert "0.4 · 0.8 = 0.32" in text["1,3,1"] and "= 0.652" in text["1,3,1"]
    assert "0.6 · 0.714 + 0.32 · 0.652 = 0.637" in text["W1"]
    assert "0.6 · 0.286 = 0.171" in text["W2"] and "0.32 · 0.348 = 0.111" in text["W3"]
    assert "אף מסלול לא מגיע לכאן" in text["2,3,2"]
    page = (ROOT / "docs/questions/senior/0071-three-wizards-duel.md").read_text(encoding="utf-8")
    assert page.count('class="figure mk-chain"') == 1 and 'data-p="0.599999999,0.6,0.8"' in page and 'data-me="1"' in page
    assert 'id="mk-explain-a"' in page


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(71)
