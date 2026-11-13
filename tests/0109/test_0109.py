"""Question 0109, car fleets: the numbers the page states, recomputed from the references of
tools/figures/q0109.py (an exact event-driven simulation with Fractions, the running maximum of
part a, the stack of part b, the lower envelope of the free lines); the claims checked against
each other on random roads (the maximum gives every arrival time, the envelope is the real path,
a car never gets free again, the stack gives every collision time), the traps, the follow-ups,
the generated blocks, and the box's models under Node against the same references."""

import json
import random
import sys
from fractions import Fraction

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0109  # noqa: E402
from q0109 import CHAIN, CHAIN_TARGET, EXAMPLE, FLOAT, THREE, TWO  # noqa: E402

F = Fraction


def random_road(rng, nmax=7, pmax=20, smax=6, target=True):
    n = rng.randint(1, nmax)
    pos = rng.sample(range(pmax), n)
    speed = [rng.randint(1, smax) for _ in range(n)]
    if target:
        return max(pos) + rng.randint(1, 12), pos, speed
    return sorted(pos), speed


def fleets(target, pos, speed):
    """The fleets of the simulation: the distinct arrival times."""
    _, arrive, _ = q0109.simulate(pos, speed, target)
    return len(set(arrive))


def times_of(pos, speed):
    """Part b by the simulation: the touch times, -1 for never."""
    touch, _, _ = q0109.simulate(pos, speed)
    return [-1 if c is None else c for c in touch]


def first_touch(pos, speed, target, r):
    """The first time car r's free line reaches the envelope of the cars ahead (by brute force
    over the crossings of its line with every line ahead), None if never (before the target)."""
    cars, _ = q0109.road(pos, speed)
    p, s = cars[r]
    best = None
    for q, v in cars[r + 1:]:
        if s > v:
            t = F(q - p, s - v)
            if p + s * t == q0109.envelope(pos, speed, target, r + 1, t) and (target is None or p + s * t <= target):
                best = t if best is None else min(best, t)
    return best


def test_statement():
    target, pos, speed = EXAMPLE
    assert fleets(*EXAMPLE) == 3
    touch, arrive, events = q0109.simulate(pos, speed, target)
    cars, _ = q0109.road(pos, speed)
    assert cars == [(0, 1), (3, 3), (5, 1), (8, 4), (10, 2)]
    assert arrive == [12, 7, 7, 1, 1]                           # road order: from 0, 3, 5, 8, 10
    meets = [(e[1], e[2], e[3], e[4]) for e in events if e[0] == "meet"]
    assert (1, 12, 3, 4) in meets                               # 8 and 10 meet at the target at time 1
    assert (1, 6, 1, 2) in meets                                # 3 catches 5 at time 1, at 6
    assert touch[0] is None                                     # 0 arrives alone at 12


def test_part_a():
    target, pos, speed = EXAMPLE
    rows, count = q0109.by_formula(target, pos, speed)
    assert count == 3
    assert [r[3] for r in rows] == [1, 1, 7, 3, 12]             # t from the front
    assert [r[4] for r in rows] == [1, 1, 7, 7, 12]             # the running maximum
    assert sum(r[6] for r in rows) == 3
    # the fractional example
    t, p, s = TWO
    assert q0109.lone(t, 1, 1) == 9 and q0109.lone(t, 0, 3) == F(10, 3)
    tau = F(1 - 0, 3 - 1)
    assert tau == F(1, 2) and 3 * tau == 1 + tau == F(3, 2)
    assert 10 - F(3, 2) == F(17, 2) and tau + F(17, 2) == 9 == max(F(10, 3), 9)
    touch, arrive, _ = q0109.simulate(p, s, t)
    assert touch[0] == F(1, 2) and arrive == [9, 9]
    assert q0109.envelope(p, s, t, 0, F(1, 2)) == F(3, 2)


def test_formula_matches_the_simulation():
    rng = random.Random(109)
    for _ in range(3000):
        target, pos, speed = random_road(rng)
        rows, count = q0109.by_formula(target, pos, speed)
        _, arrive, _ = q0109.simulate(pos, speed, target)
        assert count == fleets(target, pos, speed), (target, pos, speed)
        for r, *_rest, T, _k, _new in rows:
            assert arrive[r] == T                               # T_i = max(t_i, T_{i-1}) is the arrival time
            cars, _ = q0109.road(pos, speed)
            assert T == max(q0109.lone(target, *c) for c in cars[r:])   # the maximum of every line ahead


def test_envelope_is_the_real_path():
    """The envelope reaches the target at the arrival time, its kinks are the meetings, and car
    r touches car r + 1 exactly where its free line first reaches the envelope ahead; the gap
    between the free line and the envelope ahead, once 0, stays 0 (a car never gets free)."""
    rng = random.Random(1090)
    for k in range(1500):
        if k % 2:
            target, pos, speed = random_road(rng)
        else:
            target, (pos, speed) = None, random_road(rng, target=False)
        touch, arrive, _ = q0109.simulate(pos, speed, target)
        cars, _ = q0109.road(pos, speed)
        n = len(cars)
        for r in range(n):
            if target is not None:
                assert q0109.envelope(pos, speed, target, r, arrive[r]) == target
                assert arrive[r] == 0 or q0109.envelope(pos, speed, target, r, arrive[r] - F(1, 1000)) < target
            if r < n - 1:
                assert touch[r] == first_touch(pos, speed, target, r), (target, pos, speed, r)
                p, s = cars[r]
                grid = [F(j, 8) for j in range(0, 8 * 25)]
                gap = [p + s * t - q0109.envelope(pos, speed, None, r + 1, t) for t in grid]
                seen = False
                for g in gap:
                    if g >= 0:
                        seen = True
                    elif seen:
                        raise AssertionError((pos, speed, r))
                # the gap is convex: a line minus a concave function
                for a, b, c in zip(gap, gap[1:], gap[2:]):
                    assert a + c >= 2 * b


def test_part_b():
    pos, speed = CHAIN
    ans, on, trace = q0109.by_stack(pos, speed)
    assert ans == [2, 1, F(3, 2), -1] == times_of(pos, speed)
    assert on == [3, 2, 3, None]
    assert F(6 - 3, 4 - 3) == 3 and F(9 - 3, 4 - 1) == 2         # 0 crosses 2's line at 3, 3's at 2
    # the trace of the table
    assert trace[0] == (3, [], [], -1, None)
    assert trace[1] == (2, [3], [], F(3, 2), 3)
    assert trace[2] == (1, [3, 2], [], 1, 2)
    assert trace[3] == (0, [3, 2, 1], [(1, "speed", None), (2, "late", 3)], 2, 3)
    # after 1 catches 2 the fleet drives at 3, after it catches 3 at 1
    touch, _, events = q0109.simulate(pos, speed)
    assert [(e[1], e[3], e[4]) for e in events] == [(1, 1, 2), (F(3, 2), 2, 3), (2, 0, 1)]
    assert q0109.envelope(pos, speed, None, 1, F(5, 4)) - q0109.envelope(pos, speed, None, 1, F(9, 8)) == 3 * F(1, 8)
    assert q0109.envelope(pos, speed, None, 1, F(7, 4)) - q0109.envelope(pos, speed, None, 1, F(13, 8)) == F(1, 8)


def test_stack_matches_the_simulation():
    rng = random.Random(1091)
    for _ in range(3000):
        pos, speed = random_road(rng, nmax=9, target=False)
        ans, on, _ = q0109.by_stack(pos, speed)
        assert ans == times_of(pos, speed), (pos, speed)
        for i, j in enumerate(on):                              # it meets j's free line, while j is on it
            if j is not None:
                assert pos[i] + speed[i] * ans[i] == pos[j] + speed[j] * ans[i]
                assert ans[j] == -1 or ans[i] <= ans[j]


def test_strict_or_not_in_the_stack():
    """`<` and `<=` against c_j give the same answers (at c_j the next line also passes there)."""
    rng = random.Random(1092)
    for _ in range(3000):
        pos, speed = random_road(rng, nmax=8, pmax=12, smax=4, target=False)
        n, ans, stack = len(pos), [-1] * len(pos), []
        for i in range(n - 1, -1, -1):
            while stack:
                j = stack[-1]
                if speed[i] > speed[j]:
                    t = F(pos[j] - pos[i], speed[i] - speed[j])
                    if ans[j] == -1 or t <= ans[j]:
                        ans[i] = t
                        break
                stack.pop()
            stack.append(i)
        assert ans == times_of(pos, speed)


def test_traps():
    # floats: built from several operations the arrival is late; one division is still exact
    target, pos, speed = FLOAT
    tau = F(1, 6)
    assert 7 * tau == 1 + tau == F(7, 6) and tau + (target - F(7, 6)) == 1
    assert fleets(*FLOAT) == 1
    tf = 1 / 6
    assert tf + (target - 7 * tf) / 1 == 1.0000000000000002 > 1.0
    assert (target - 0) / 7 < (target - 1) / 1 == 1.0
    # integer division: 10 / 3 and 9 / 3 are both 3, yet the two cars never meet
    assert 10 // 3 == 9 // 3 == 3 and fleets(10, [0, 1], [3, 3]) == 2
    # a tie at the target counted twice with >=
    t, p, s = EXAMPLE
    cnt, ahead = 0, F(0)
    for q, v in sorted(zip(p, s), reverse=True):
        if F(t - q, v) >= ahead:
            cnt, ahead = cnt + 1, F(t - q, v)
    assert cnt == 4
    # only the line of the car ahead
    t, p, s = THREE
    touch, arrive, events = q0109.simulate(p, s, t)
    assert touch == [3, F(4, 3), None] and arrive == [4, 4, 4]
    assert [(e[1], e[2]) for e in events if e[0] == "meet"] == [(F(4, 3), F(22, 3)), (3, 9)]
    assert q0109.lone(t, 0, 3) == F(10, 3) and q0109.lone(t, 6, 1) == 4 and q0109.lone(t, 2, 4) == 2
    assert fleets(*THREE) == 1
    pairwise = 1 + sum(1 for (a, sa), (b, sb) in zip(sorted(zip(p, s)), sorted(zip(p, s))[1:])
                       if not (sa > sb and a + sa * F(b - a, sa - sb) <= t))
    assert pairwise == 2
    assert max(F(10, 3), 4) == 4
    # time steps: at t = 1 in the fractional example A has passed B
    assert 0 + 3 * 1 == 3 and 1 + 1 * 1 == 2
    assert fleets(20, [0, 1], [2, 2]) == 2
    assert q0109.lone(20, 0, 2) == 10 and q0109.lone(20, 1, 2) == F(19, 2)
    import math
    assert math.ceil(q0109.lone(20, 0, 2)) == math.ceil(q0109.lone(20, 1, 2)) == 10
    # part b: only the neighbour, or the first line crossed in road order
    pos, speed = CHAIN
    neighbour = [-1 if speed[i] <= speed[i + 1] else F(pos[i + 1] - pos[i], speed[i] - speed[i + 1]) for i in range(3)]
    assert neighbour[0] == -1
    first_line = next(F(pos[j] - pos[0], speed[0] - speed[j]) for j in range(1, 4) if speed[0] > speed[j])
    assert first_line == 3 and q0109.by_stack(pos, speed)[0][0] == 2


def test_followups():
    pos, speed = CHAIN
    touch, _, _ = q0109.simulate(pos, speed)
    assert q0109.fleets_at(touch, 1) == 3
    assert [r for r, c in enumerate(touch) if c is None or c > 1] == [0, 2, 3]
    # fleets_at against the simulation at many times (positions of cars equal = same fleet)
    rng = random.Random(1093)
    for _ in range(500):
        pos, speed = random_road(rng, target=False)
        touch, _, _ = q0109.simulate(pos, speed)
        for t in [F(j, 4) for j in range(0, 40)]:
            places = {q0109.envelope(pos, speed, None, r, t) for r in range(len(pos))}
            assert q0109.fleets_at(touch, t) == len(places)
    # in-order retire
    ready = [5, 3, 4, 9, 8]
    retire, last = [], 0
    for r in ready:
        last = max(r, last)
        retire.append(last)
    assert retire == [5, 5, 5, 9, 9] and len(set(retire)) == 2


def test_edge_cases():
    assert fleets(5, [0], [1]) == 1 and q0109.by_formula(5, [0], [1])[1] == 1
    assert fleets(10, [0, 2, 4], [2, 2, 2]) == 3                    # the same speed: never meet
    assert fleets(10, [4, 2, 0], [3, 4, 5]) == 1                    # all meet at the target, t = 2
    assert q0109.by_formula(10, [4, 2, 0], [3, 4, 5])[0][0][3] == 2
    assert q0109.by_stack([0], [1])[0] == [-1]
    assert q0109.by_stack([0, 1, 2], [3, 2, 1])[0] == times_of([0, 1, 2], [3, 2, 1])
    # the chain in part a's box: one fleet; car 0 catches it at 2, at 11
    touch, arrive, _ = q0109.simulate(*CHAIN, CHAIN_TARGET)
    assert arrive == [3, 3, 3, 3] and touch[0] == 2 and 3 + 4 * 2 == 11 <= CHAIN_TARGET


def test_try_it_paragraphs():
    # part a: at t = 1 cars 3 and 4 (road order) meet at the target, with equal t
    target, pos, speed = EXAMPLE
    _, _, events = q0109.simulate(pos, speed, target)
    assert ("meet", 1, 12, 3, 4) in events
    rows, _ = q0109.by_formula(target, pos, speed)
    assert rows[0][3] == rows[1][3] == 1
    # "a meeting at half": car 0 catches 1 at 1/2, at 3/2
    _, _, events = q0109.simulate(TWO[1], TWO[2], TWO[0])
    assert ("meet", F(1, 2), F(3, 2), 0, 1) in events
    # the chain: 0 and 1 have the same speed, yet arrive together
    assert CHAIN[1][0] == CHAIN[1][1]
    _, arrive, _ = q0109.simulate(*CHAIN, CHAIN_TARGET)
    assert arrive[0] == arrive[1]
    # part b's box: 0 on 3's line, 1 catches 2 at 1, the fleet catches 3 at 3/2
    ans, on, _ = q0109.by_stack(*CHAIN)
    assert on[0] == 3 and ans[1] == 1 and ans[2] == F(3, 2)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(109)


def _q(v):
    return None if v is None else [v.numerator, v.denominator]


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(10900)
    cases = [[EXAMPLE[0], EXAMPLE[1], EXAMPLE[2]], [TWO[0], TWO[1], TWO[2]], [CHAIN_TARGET, *CHAIN],
             [THREE[0], THREE[1], THREE[2]], [FLOAT[0], FLOAT[1], FLOAT[2]], [None, *CHAIN]]
    for k in range(300):
        if k % 3 == 2:
            cases.append([None, *random_road(rng, nmax=6, target=False)])
        else:
            cases.append(list(random_road(rng, nmax=6)))
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([t, p, s]) => {{"
                    "const sim = m.cfSim(p, s, t), st = m.cfStack(p, s);"
                    "return [sim.touch, sim.arrive, sim.events, t === null ? null : m.cfFormula(t, p, s), st.ans, st.on,"
                    " p.map((_, r) => m.cfAt(p, s, t, r, [7, 4]))];})));")
    for (target, pos, speed), (touch, arrive, events, formula, ans, on, at) in zip(cases, got):
        rt, ra, rev = q0109.simulate(pos, speed, target)
        assert touch == [_q(c) for c in rt], (target, pos, speed)
        assert arrive == [_q(c) for c in ra]
        want = []
        for e in rev:
            if e[0] == "meet":
                want.append({"kind": "meet", "t": _q(e[1]), "x": _q(F(e[2])), "a": e[3], "b": e[4]})
            else:
                want.append({"kind": "arrive", "t": _q(e[1]), "cars": e[2]})
        assert events == want
        if target is not None:
            rows, count = q0109.by_formula(target, pos, speed)
            assert formula["count"] == count
            assert formula["rows"] == [[r, p, s, _q(t), _q(T), k, nw] for r, p, s, t, T, k, nw in rows]
        cars, order = q0109.road(pos, speed)
        sa, so, _ = q0109.by_stack([c[0] for c in cars], [c[1] for c in cars])
        assert ans == [None if a == -1 else _q(a) for a in sa]
        assert on == so
        assert at == [_q(q0109.envelope(pos, speed, target, r, F(7, 4))) for r in range(len(pos))]
    presets = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.cfPresets));")
    assert [p[1:] for p in presets] == [list(EXAMPLE), list(TWO), [CHAIN_TARGET, *CHAIN]]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify([['10, 8, 0', 0, 99], ['1.2.3', 1, 20], ['7', 0, 99], ['', 0, 99],"
                       " ['1,2,3,4,5,6,7', 0, 99], ['0, 100', 0, 99], ['0', 1, 20], ['a, 2', 0, 99], ['1 2;3', 1, 20]]"
                       ".map(([t, lo, hi]) => m.cfParse(t, lo, hi))));")
    assert parsed == [[10, 8, 0], [1, 2, 3], [7], None, None, None, None, None, [1, 2, 3]]
    checks = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify([[12, [10, 8], [2, 4]], [12, [1, 1], [2, 4]], [12, [1, 2], [2]],"
                       " [8, [10, 8], [2, 4]], [null, [3, 5], [4, 4]], [12, null, [1]], [12, [1], null]]"
                       ".map(([t, p, s]) => m.cfCheck(t, p, s))));")
    assert checks[0] == "" and checks[4] == ""
    assert all(c for c in checks[1:4] + checks[5:])
    frames = node_json(f"const m = {explorer_require()};"
                       "const sim = m.cfSim([10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 12), end = m.cfEnd(sim, 12);"
                       "console.log(JSON.stringify([end, m.cfFrames(end, sim.events).length, m.cfEnd(m.cfSim([3, 5, 6, 9], [4, 4, 3, 1], null), null)]));")
    assert frames[0] == [12, 1] and frames[1] == 25 and frames[2] == [5, 2]
