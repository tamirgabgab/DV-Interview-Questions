"""Question 0031: every number the page states (17, 19, the plan, the strategies table and
the examples table), the generator's Dijkstra against brute force and against the greedy
rule on random sets, the explorer's JavaScript against the generator, and the page copies
of the generated blocks."""

import random
import sys
from itertools import combinations

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0031  # noqa: E402


def brute(times):
    """The least total time by exhaustive search over crossing sequences (small n)."""
    n = len(times)
    everyone = (1 << n) - 1
    best = [float("inf")]

    def rec(across, side, t, seen):
        if t >= best[0]:
            return
        if across == everyone:
            best[0] = t
            return
        bank = [i for i in range(n) if ((across >> i) & 1) == side]
        for g in [(i,) for i in bank] + list(combinations(bank, 2)):
            new = (across ^ sum(1 << i for i in g), 1 - side)
            if new in seen:
                continue
            rec(new[0], new[1], t + max(times[i] for i in g), seen | {new})

    rec(0, 0, 0, {(0, 0)})
    return best[0]


def test_page_numbers():
    total, moves = q0031.plan([1, 2, 5, 10])
    assert total == 17 and moves == [(0, 1), (0,), (2, 3), (1,), (0, 1)]
    assert q0031.replay([1, 2, 5, 10], moves) == 17
    assert q0031.escort([1, 2, 5, 10]) == 19 and q0031.greedy([1, 2, 5, 10]) == 17
    assert q0031.replay([1, 2, 5, 10], [(0, 3), (0,), (0, 2), (0,), (0, 1)]) == 19      # the trap
    assert q0031.replay([1, 2, 5, 10], [(0, 1), (1,), (2, 3), (0,), (0, 1)]) == 17      # the other 17
    assert q0031.replay([1, 2, 5, 10], [(2, 3), (0, 1)]) is None                        # no torch
    assert brute([1, 2, 5, 10]) == 17
    # the follow-ups
    assert q0031.plan([1, 2, 5, 10, 20])[0] == 33 == q0031.greedy([1, 2, 5, 10, 20])
    assert all(q0031.plan([t] * n)[0] == (2 * n - 3) * t for n in (2, 3, 4, 5) for t in (1, 3))
    assert q0031.greedy([1, 2, 3, 4]) == 11 == 2 * 1 + 3 + 4 + 2       # the escort move wins there


def test_tables():
    rows = q0031.plan_table().splitlines()[2:]
    assert len(rows) == 5 and rows[-1].endswith("| 2 | 17 |")
    strat = q0031.strategies_table().splitlines()[2:]
    assert [r.rsplit("|", 2)[1].strip() for r in strat] == ["‏19", "‏17", "‏17"]
    ex = q0031.examples_table().splitlines()[2:]
    assert len(ex) == len(q0031.EXAMPLES)
    for ts, row in zip(q0031.EXAMPLES, ex):
        cells = [c.strip().lstrip("‏") for c in row.strip("|").split("|")]
        assert cells[1:] == [str(q0031.escort(ts)), str(q0031.plan(ts)[0]), str(q0031.greedy(ts))]


def test_search_matches_brute_force_and_greedy():
    rng = random.Random(31)
    for _ in range(150):
        n = rng.randint(1, 5)
        ts = [rng.randint(1, 12) for _ in range(n)]
        total, moves = q0031.plan(ts)
        assert total == brute(ts) == q0031.greedy(ts), ts
        assert q0031.replay(ts, moves) == total
    for _ in range(300):
        n = rng.randint(1, 8)
        ts = [rng.randint(1, 30) for _ in range(n)]
        total, moves = q0031.plan(ts)
        assert total == q0031.greedy(ts) and q0031.replay(ts, moves) == total, ts
        assert total <= q0031.escort(ts) or n < 3


def test_explorer_matches_generator():
    from page_tests import explorer_require, node_json

    rng = random.Random(3131)
    cases = [[1, 2, 5, 10], [1, 2, 5, 10, 20], [1, 2, 3, 4], [7], [3, 9], [2, 2, 2, 2, 2]]
    cases += [[rng.randint(1, 25) for _ in range(rng.randint(1, 8))] for _ in range(60)]
    got = node_json(f"const m = {explorer_require()}; const cases = {cases};"
                    "console.log(JSON.stringify(cases.map((ts) => { const r = m.bridgeSolve(ts); return [r.time, r.moves, m.bridgeEscort(ts)]; })));")
    for ts, (time, moves, esc) in zip(cases, got):
        assert time == q0031.plan(ts)[0] and esc == q0031.escort(ts), ts
        assert q0031.replay(ts, [tuple(g) for g in moves]) == time, ts
    assert got[0][1] == [[0, 1], [0], [2, 3], [1], [0, 1]]


def test_explorer_capacity_and_classic_plans():
    """The box's follow-ups: a bridge of three (Dijkstra against a brute force with groups
    of up to three; 13 for the page's times), and the two classic plans as crossings,
    whose replay gives the page's escort time and the pair rule's time."""
    from page_tests import explorer_require, node_json

    def brute3(times):
        n, everyone = len(times), (1 << len(times)) - 1
        best = [float("inf")]

        def rec(across, side, t, seen):
            if t >= best[0]:
                return
            if across == everyone:
                best[0] = t
                return
            bank = [i for i in range(n) if ((across >> i) & 1) == side]
            groups = [(i,) for i in bank] + list(combinations(bank, 2)) + list(combinations(bank, 3))
            for g in groups:
                new = (across ^ sum(1 << i for i in g), 1 - side)
                if new not in seen:
                    rec(new[0], new[1], t + max(times[i] for i in g), seen | {new})

        rec(0, 0, 0, {(0, 0)})
        return best[0]

    def pair_rule(times):
        s = sorted(times)
        total = 0
        while len(s) > 3:
            total += s[0] + 2 * s[1] + s[-1]
            s = s[:-2]
        return total + (sum(s) if len(s) == 3 else s[-1])

    rng = random.Random(3132)
    cases = [[1, 2, 5, 10], [1, 2, 3, 4], [1, 2, 5, 10, 20], [7], [3, 9], [2, 2, 2]]
    cases += [[rng.randint(1, 25) for _ in range(rng.randint(1, 6))] for _ in range(40)]
    got = node_json(f"const m = {explorer_require()}; const cases = {cases};"
                    "console.log(JSON.stringify(cases.map((ts) => { const r3 = m.bridgeSolve(ts, 3), e = m.bridgeEscortMoves(ts), p = m.bridgePairMoves(ts);"
                    " return [r3.time, r3.moves, m.bridgeTime(ts, e), e, m.bridgeTime(ts, p), p]; })));")
    for ts, (t3, m3, te, me, tp, mp) in zip(cases, got):
        assert t3 == brute3(ts) and all(len(g) <= 3 for g in m3), ts
        assert t3 <= q0031.plan(ts)[0]
        assert te == q0031.escort(ts) and q0031.replay(ts, [tuple(g) for g in me]) == te, ts
        assert tp == pair_rule(ts) and q0031.replay(ts, [tuple(g) for g in mp]) == tp, ts
        assert tp >= q0031.plan(ts)[0] and te >= q0031.plan(ts)[0]
    assert got[0][0] == 13


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(31)
