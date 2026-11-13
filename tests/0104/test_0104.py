"""Question 0104, gas stations on a circle: the numbers the page states, recomputed from the
references of tools/figures/q0104.py (the lap driven from every start, the levels P_k), the
claims of every part checked by brute force on random rings (the one pass and the start at the
lowest level give the first good start; part c's condition gives every good start; with sum 0
exactly the stations at the minimum), the cycle lemma, the traps and the follow-ups, the
generated blocks, and the box's models under Node against the same references."""

import json
import random
import sys
from itertools import combinations
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0104  # noqa: E402
from q0104 import EXAMPLE, MORE, NONE, ZERO  # noqa: E402


def ring_of(d):
    """A ring whose differences are d."""
    return [max(x, 0) for x in d], [max(-x, 0) for x in d]


def random_ring(rng, nmax=8, vmax=6):
    n = rng.randint(1, nmax)
    return [rng.randint(0, vmax) for _ in range(n)], [rng.randint(0, vmax) for _ in range(n)]


def first_good(gas, cost):
    g = q0104.good(gas, cost)
    return g[0] if g else -1


def test_statement():
    gas, cost = EXAMPLE
    assert q0104.diffs(gas, cost) == [-2, -2, -2, 3, 3]
    assert q0104.walk(gas, cost, 3) == [3, 6, 4, 2, 0]
    assert q0104.good(gas, cost) == [3]
    assert q0104.levels(gas, cost) == [0, -2, -4, -6, -3, 0]


def test_part_a():
    gas, cost = EXAMPLE
    # the table: stations 0, 1 and 2 fail on their first leg, 4 on leg 1 -> 2 as station 1 does
    assert [q0104.walk(gas, cost, s) for s in range(5)] == [[-2], [-2], [-2], [3, 6, 4, 2, 0], [3, 1, -1]]
    assert (4 + 3 - 1) % 5 == 1 and (1 + 1 - 1) % 5 == 1
    assert q0104.legs_naive(gas, cost) == 8
    # the necessary condition: after a whole lap the tank is S from every start
    rng = random.Random(1)
    for _ in range(3000):
        gas, cost = random_ring(rng)
        S = sum(gas) - sum(cost)
        for s in range(len(gas)):
            tank = 0
            for k in range(len(gas)):
                i = (s + k) % len(gas)
                tank += gas[i] - cost[i]
            assert tank == S
        if S < 0:
            assert q0104.good(gas, cost) == []
    # the worst case: n - 2 ones, -(n - 1) and n - 1; n(n + 1) / 2 legs although S >= 0
    assert [1] * 3 + [-4, 4] == [1, 1, 1, -4, 4]
    for n in range(2, 16):
        d = [1] * (n - 2) + [-(n - 1), n - 1]
        gas, cost = ring_of(d)
        assert sum(d) >= 0 and q0104.legs_naive(gas, cost) == n * (n + 1) // 2, n
        assert q0104.good(gas, cost)[0] == n - 1
        for s in range(n - 1):   # every start before the last runs until station n - 2
            assert (s + len(q0104.walk(gas, cost, s)) - 1) % n == n - 2
    assert 5 * 6 // 2 == 15


def test_part_b():
    gas, cost = EXAMPLE
    start, rows = q0104.one_pass(gas, cost)
    assert start == 3
    assert [r["dry"] for r in rows] == [-2, -2, -2, None, None]
    assert [r["total"] for r in rows] == [-2, -4, -6, -3, 0] and [r["low"] for r in rows] == [-2, -4, -6, -6, -6]
    assert [r["tank"] for r in rows] == [0, 0, 0, 3, 6] and -3 - (-6) == 3 and 0 - (-6) == 6
    # the lowest level is -6, before station 3; the lap from 3 is the height above it
    p = q0104.levels(gas, cost)
    assert min(p[:5]) == -6 and p.index(-6) == 3
    assert [p[k] - p[3] for k in (4, 5)] + [p[5] + p[k] - p[3] for k in (1, 2, 3)] == [3, 6, 4, 2, 0]
    # on random rings: the one pass returns the first good start (the answer of part a), which is
    # the station after the first place of the lowest level, and a start exists iff S >= 0
    rng = random.Random(2)
    for _ in range(20000):
        gas, cost = random_ring(rng)
        n, p = len(gas), q0104.levels(gas, cost)
        want = first_good(gas, cost)
        assert q0104.one_pass(gas, cost)[0] == want
        assert (want >= 0) == (p[n] >= 0)
        if p[n] >= 0:
            assert want == p[:n].index(min(p[:n]))
        # the invariant: the tank of the one pass is the level minus the lowest level so far
        for r in q0104.one_pass(gas, cost)[1]:
            assert r["tank"] == r["total"] - r["low"]


def test_part_c():
    # the condition, against driving the lap, and the two-lap window
    rng = random.Random(3)
    counts = set()
    for _ in range(20000):
        gas, cost = random_ring(rng)
        n, p = len(gas), q0104.levels(gas, cost)
        S, g = p[n], q0104.good(gas, cost)
        assert q0104.by_levels(gas, cost) == g
        q = [p[k % n] + (k // n) * S for k in range(2 * n + 1)]
        assert g == ([s for s in range(n) if p[s] == min(q[s:s + n + 1])] if S >= 0 else [])
        if S == 0:
            assert g == q0104.at_min(gas, cost)
        if S >= 0:
            assert set(q0104.at_min(gas, cost)) <= set(g)
        if S > 0 and len(g) > len(q0104.at_min(gas, cost)):
            counts.add("more")
        counts.add(len(g))
    assert "more" in counts and set(range(0, 9)) <= counts
    # the examples of the page
    assert sum(ZERO[0]) - sum(ZERO[1]) == 0 and q0104.diffs(*ZERO) == [2, -2, 1, -1, 0, 1, -1]
    assert q0104.levels(*ZERO) == [0, 2, 0, 1, 0, 0, 1, 0] and q0104.good(*ZERO) == [0, 2, 4, 5] == q0104.at_min(*ZERO)
    p = q0104.levels(*MORE)
    assert p == [0, -1, 1, 0, 1, 3] and p[5] == 3
    assert q0104.good(*MORE) == [1, 3, 4] and q0104.at_min(*MORE) == [1] and min(p[:5]) == -1
    assert p[3] == 0 and p[1] == -1 and -1 + 3 == 2 >= 0 and p[3] <= min(p[4:])
    assert [q0104.walk(*MORE, s) for s in range(5)] == [[-1], [2, 1, 2, 4, 3], [-1], [1, 3, 2, 4, 3], [2, 1, 3, 2, 3]]
    # the count of good starts runs from 0 to n: all d >= 0 gives n
    assert q0104.good([2, 2, 2], [1, 2, 0]) == [0, 1, 2]


def test_cycle_lemma():
    """m + 1 ones and m minus ones: exactly one rotation has every partial sum positive, so
    C(2m + 1, m) / (2m + 1) sequences do, the Catalan number."""
    for m in range(0, 7):
        L = 2 * m + 1
        positive = 0
        for ups in combinations(range(L), m + 1):
            seq = [1 if i in ups else -1 for i in range(L)]
            rot = 0
            for r in range(L):
                s, ok = 0, True
                for x in seq[r:] + seq[:r]:
                    s += x
                    ok = ok and s > 0
                rot += ok
            assert rot == 1
            positive += all(sum(seq[:k + 1]) > 0 for k in range(L))
        assert comb(L, m) % L == 0 and positive == comb(L, m) // L == comb(2 * m, m) // (m + 1)


def test_traps():
    def restart_at_j(gas, cost):
        start = tank = total = 0
        for i in range(len(gas)):
            d = gas[i] - cost[i]
            tank += d
            total += d
            if tank < 0:
                start, tank = i, 0
        return start if total >= 0 else -1

    def no_check(gas, cost):
        start = tank = 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:
                start, tank = i + 1, 0
        return start

    def restart_le(gas, cost):
        start = tank = total = 0
        for i in range(len(gas)):
            d = gas[i] - cost[i]
            tank += d
            total += d
            if tank <= 0:
                start, tank = i + 1, 0
        return start if total >= 0 else -1

    def min_le(gas, cost):
        level = low = at = 0
        for i in range(len(gas)):
            level += gas[i] - cost[i]
            if level <= low:
                low, at = level, i + 1
        return at if level >= 0 else -1

    def until_back(gas, cost):
        """The trap of n = 1: drives from the station after the start and decides "a full lap" when
        it is back at the start, not by the tank."""
        n = len(gas)
        for s in range(n):
            tank, j = gas[s] - cost[s], (s + 1) % n
            while j != s and tank >= 0:
                tank += gas[j] - cost[j]
                j = (j + 1) % n
            if j == s:
                return s
        return -1

    gas, cost = EXAMPLE
    assert restart_at_j(gas, cost) == 2 and q0104.walk(gas, cost, 2)[0] == -2
    assert [r["total"] for r in q0104.one_pass(gas, cost)[1]][2] == -6
    assert no_check(*NONE) == 2 and q0104.walk(*NONE, 2) == [1, 0, -1] and sum(NONE[0]) - sum(NONE[1]) == -1
    assert q0104.good(*NONE) == [] and q0104.one_pass(*NONE)[0] == -1
    assert restart_le([1, 0], [0, 1]) == 2 == min_le([1, 0], [0, 1]) and q0104.levels([1, 0], [0, 1]) == [0, 1, 0]
    assert q0104.good([1, 0], [0, 1]) == [0] and q0104.one_pass([1, 0], [0, 1])[0] == 0
    assert len(q0104.good(*ZERO)) == 4
    # n = 1: the loop that stops when back at the start answers 0 even when the leg runs dry
    assert until_back([1], [2]) == 0 and until_back(*NONE) == 2 and q0104.walk(*NONE, 2)[-1] < 0 and q0104.good([1], [2]) == [] and q0104.good([2], [2]) == [0]
    # a station with d = 0 at a tied minimum: both are good starts (the trap's d = 0 case)
    assert q0104.good([3, 1, 2, 2, 1], [1, 4, 2, 1, 1]) == [2, 3] == q0104.at_min([3, 1, 2, 2, 1], [1, 4, 2, 1, 1])


def test_followups():
    rng = random.Random(4)

    def good_o1(gas, cost):
        """Two passes and O(1) memory: S, the lowest level m of P_0..P_(n-1) and its first place a,
        then from the end back to a with the lowest level after."""
        n, level, m, a = len(gas), 0, 0, 0
        for i in range(n):
            if level < m:
                m, a = level, i
            level += gas[i] - cost[i]
        S = level
        if S < 0:
            return []
        out, low_after, lev = [], S, S
        for s in range(n - 1, a - 1, -1):
            lev -= gas[s] - cost[s]          # lev is now P_s
            if lev <= low_after and lev <= m + S:
                out.append(s)
            low_after = min(low_after, lev)
        return sorted(out)

    def reverse(gas, cost):
        """Counterclockwise: station j of the new ring is station -j, the leg to the next costs
        cost[-j - 1]."""
        n = len(gas)
        return [gas[(-j) % n] for j in range(n)], [cost[(-j - 1) % n] for j in range(n)]

    def good_ccw(gas, cost):
        n, out = len(gas), []
        for s in range(n):
            tank, ok = 0, True
            for k in range(n):
                i = (s - k) % n
                tank += gas[i] - cost[(i - 1) % n]
                ok = ok and tank >= 0
            if ok:
                out.append(s)
        return out

    for _ in range(20000):
        gas, cost = random_ring(rng)
        n = len(gas)
        assert good_o1(gas, cost) == q0104.good(gas, cost)
        rg, rc = reverse(gas, cost)
        assert sorted((-j) % n for j in q0104.good(rg, rc)) == good_ccw(gas, cost)
        assert sum(rg) - sum(rc) == sum(gas) - sum(cost)
    # the hardware: one pair a clock, the sum, the lowest sum and its place (start_at_min)
    for _ in range(2000):
        gas, cost = random_ring(rng)
        total, low, at = 0, 0, 0
        for i, (g, c) in enumerate(zip(gas, cost)):
            d = g - c                      # the subtractor
            nxt = total + d                # the adder
            if nxt < low:                  # the comparator
                low, at = nxt, i + 1
            total = nxt
        assert (at if total >= 0 else -1) == first_good(gas, cost)


def test_try_it_paragraphs():
    gas, cost = EXAMPLE
    assert q0104.walk(gas, cost, 4) == [3, 1, -1] and (4 + 2) % 5 == 1     # dry on leg 1 -> 2
    assert all(q0104.walk(*NONE, s)[-1] < 0 for s in range(3)) and sum(NONE[0]) - sum(NONE[1]) == -1
    g = [2] + MORE[0][1:]
    assert g == [2, 3, 2, 3, 4] and sum(g) - sum(MORE[1]) == 4 and q0104.good(g, MORE[1]) == [0, 1, 3, 4]
    assert all(min(q0104.levels(*MORE)[k] for k in range(3, 6)) >= q0104.levels(*MORE)[3] for _ in [0])


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(104)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(104)
    cases = [list(map(list, r)) for r in (EXAMPLE, NONE, ZERO, MORE)]
    for _ in range(300):
        gas, cost = random_ring(rng, nmax=10, vmax=9)
        cases.append([gas, cost])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([g, c]) => [m.gsLevels(g, c), m.gsGood(g, c), m.gsOnePass(g, c),"
                    f" g.map((_, s) => m.gsWalk(g, c, s))])));")
    for (gas, cost), (lev, gd, one, walks) in zip(cases, got):
        assert lev == q0104.levels(gas, cost)
        assert gd == q0104.good(gas, cost)
        assert one == q0104.one_pass(gas, cost)[0]
        assert walks == [q0104.walk(gas, cost, s) for s in range(len(gas))]
    presets = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.gsPresets));")
    assert [[p[1], p[2]] for p in presets] == [list(map(list, r)) for r in (EXAMPLE, NONE, ZERO, MORE)]
    assert [len(q0104.good(p[1], p[2])) for p in presets] == [1, 0, 4, 3]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['1, 2, 3', '1.2.3', '7', '0 99', '1,,2', '', '1, 100', '-1, 2', 'a, 2', '1,2,3,4,5,6,7,8,9,10', '1,2,3,4,5,6,7,8,9,10,11'].map((t) => m.gsParse(t))));")
    assert parsed == [[1, 2, 3], [1, 2, 3], [7], [0, 99], [1, 2], None, None, None, None, list(range(1, 11)), None]
