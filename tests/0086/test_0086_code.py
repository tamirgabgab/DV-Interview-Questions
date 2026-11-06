"""Question 0086: the page's Python code (it runs as published) against the generator's
breadth-first search: meetings_to and min_meetings on every state with counts up to 12, and
meeting_plan replayed meeting by meeting to the colour it was asked for, in exactly the
number of meetings the search finds."""

import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0086  # noqa: E402

ns = load_python(86)
meetings_to, min_meetings, meeting_plan = ns["meetings_to"], ns["min_meetings"], ns["meeting_plan"]

N = 12


def every_state():
    return [(r, g, b) for r in range(N + 1) for g in range(N + 1) for b in range(N + 1) if r + g + b]


def test_meetings_to_matches_the_search():
    for s in every_state():
        dist = q0086.distances(s)
        for c in range(3):
            want = dist.get(q0086.mono(sum(s), c))
            assert meetings_to(s, c) == want, (s, c)


def test_min_meetings_matches_the_search():
    for s in every_state():
        dist = q0086.distances(s)
        options = [(dist[q0086.mono(sum(s), c)], c) for c in range(3) if q0086.mono(sum(s), c) in dist]
        assert min_meetings(s) == (min(options) if options else None), s


def test_meeting_plan_reaches_the_colour_in_the_fewest_meetings():
    for s in every_state():
        for c in range(3):
            m = meetings_to(s, c)
            if m is None:
                continue
            plan = meeting_plan(s, c)
            assert len(plan) == m, (s, c)
            t = s
            for i, j in plan:
                assert i < j and t[i] > 0 and t[j] > 0, (s, c, plan)
                t = q0086.meet(t, i, j)
            assert t == q0086.mono(sum(s), c), (s, c)
            assert [p for p, _ in q0086.construct(s, c)] == plan, (s, c)


def test_the_page_numbers():
    assert min_meetings((13, 15, 17)) is None
    assert min_meetings((13, 16, 17)) == (16, 2)
    assert min_meetings((14, 15, 17)) == (17, 1)
    assert meetings_to((6, 0, 0), 2) is None and min_meetings((6, 0, 0)) == (0, 0)
    assert meeting_plan((7, 1, 3), 2) == [(0, 1), (0, 2), (0, 1), (0, 1), (0, 2), (0, 1), (0, 1)]
