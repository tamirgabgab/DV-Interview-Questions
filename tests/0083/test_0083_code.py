"""Question 0083: the page's Python code (it runs as published) against the generator's
independent breadth-first search: can_measure on every small case, jugs_shortest step by
step (the same steps in the same order, the contents after each), and split_shortest on the
8, 5, 3 jugs and on other three-jug splits."""

import sys
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0083  # noqa: E402

ns = load_python(83)
can_measure, jugs_shortest, split_shortest = ns["can_measure"], ns["jugs_shortest"], ns["split_shortest"]


def as_page(m):
    """A generator step, ("fill", 0) or ("pour", 1, 0), in the page's names."""
    return (m[0],) + tuple("AB"[i] for i in m[1:])


def test_can_measure():
    for a in range(1, 10):
        for b in range(1, 13):
            reach = {v for s in q0083.distances((a, b)) for v in s}
            for t in range(0, 15):
                assert can_measure(a, b, t) == (t in reach), (a, b, t)
                assert can_measure(a, b, t) == (t <= max(a, b) and t % gcd(a, b) == 0)


def test_jugs_shortest_matches_the_reference():
    for a in range(1, 8):
        for b in range(1, 10):
            for t in range(0, 11):
                got, want = jugs_shortest(a, b, t), q0083.shortest(a, b, t)
                if want is None:
                    assert got is None, (a, b, t)
                    continue
                assert [(as_page(m), s) for m, s in want] == [(step, (x, y)) for step, x, y in got], (a, b, t)


def test_the_page_plan():
    plan = jugs_shortest(3, 5, 4)
    assert [s for s, *_ in plan] == [("fill", "B"), ("pour", "B", "A"), ("empty", "A"),
                                      ("pour", "B", "A"), ("fill", "B"), ("pour", "B", "A")]
    assert [(x, y) for _, x, y in plan] == [(0, 5), (3, 2), (0, 2), (2, 0), (2, 5), (3, 4)]
    assert jugs_shortest(3, 5, 7) is None and jugs_shortest(4, 6, 3) is None
    assert jugs_shortest(3, 5, 0) == []


def test_replay_checker():
    """The follow-up's checker, independent of the search: a plan exists exactly when the gcd
    rule says so, every step of it is legal and changes something, the reported contents are
    the replayed ones, and the last state holds t. Covers gcd > 1, t over both jugs, t = 0, a = b."""
    def apply(a, b, x, y, step):
        if step == ("fill", "A"):
            return a, y
        if step == ("fill", "B"):
            return x, b
        if step == ("empty", "A"):
            return 0, y
        if step == ("empty", "B"):
            return x, 0
        if step == ("pour", "A", "B"):
            d = min(x, b - y)
            return x - d, y + d
        assert step == ("pour", "B", "A"), step
        d = min(y, a - x)
        return x + d, y - d

    seen = set()
    for a in range(1, 10):
        for b in range(1, 13):
            for t in range(0, 14):
                plan = jugs_shortest(a, b, t)
                assert (plan is not None) == can_measure(a, b, t), (a, b, t)
                if plan is None:
                    seen.add("over" if t > max(a, b) else "gcd")
                    continue
                x = y = 0
                for step, px, py in plan:
                    nx, ny = apply(a, b, x, y, step)
                    assert (nx, ny) != (x, y) and (nx, ny) == (px, py), (a, b, t, step)
                    x, y = nx, ny
                assert t in (x, y), (a, b, t)
                seen.add("zero" if t == 0 else "equal" if a == b else "gcd>1" if gcd(a, b) > 1 else "plain")
    assert seen == {"over", "gcd", "zero", "equal", "gcd>1", "plain"}


def test_split_shortest():
    got = split_shortest((8, 5, 3), (8, 0, 0), (4, 4, 0))
    assert [(i, j, s) for i, j, s in got] == [(m[1], m[2], s) for m, s in q0083.PLAN3]
    assert [s for *_, s in got] == [(3, 5, 0), (3, 2, 3), (6, 2, 0), (6, 0, 2), (1, 5, 2), (1, 4, 3), (4, 4, 0)]
    for caps, goal in [((10, 7, 3), (5, 5, 0)), ((12, 7, 5), (6, 6, 0)), ((6, 4, 1), (3, 3, 0)), ((8, 5, 3), (8, 0, 0)),
                       ((9, 4, 2), (5, 4, 0)), ((6, 4, 2), (3, 3, 0))]:
        start = (caps[0], 0, 0)
        want = q0083.bfs(caps, lambda s, g=goal: s == g, start, tap=False)
        got = split_shortest(caps, start, goal)
        if want is None:
            assert got is None, caps
        else:
            assert [(m[1], m[2], s) for m, s in want] == list(got), caps
    assert split_shortest((6, 4, 2), (6, 0, 0), (3, 3, 0)) is None     # every amount stays even
