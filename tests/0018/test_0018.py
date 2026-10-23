import re
import subprocess
import sys

from extract_code import ROOT, load_python, question_path

ns = load_python(18)
solve = ns["solve"]


def replay(A, B, plan):
    """Replay a plan from rest; return the event times. Fails on an inconsistent plan."""
    t = a = b = 0
    events = [0]
    for when in sorted(plan):
        assert when == t, f"action at {when} but the next event is at {t}"
        if "A" in plan[when]:
            a = A - a
        if "B" in plan[when]:
            b = B - b
        running = [s for s in (a, b) if s > 0]
        assert running, "nothing is running"
        wait = min(running)
        t, a, b = t + wait, max(a - wait, 0), max(b - wait, 0)
        events.append(t)
    return events


def measurable(A, B, D):
    """Independent oracle: exhaustive search over every flip sequence (no visited set)."""
    def rec(t, a, b):
        if t == D:
            return True
        for fa in (0, 1):
            for fb in (0, 1):
                a2, b2 = (A - a if fa else a), (B - b if fb else b)
                if a2 == 0 and b2 == 0:
                    continue
                w = min(s for s in (a2, b2) if s > 0)
                if t + w <= D and rec(t + w, max(a2 - w, 0), max(b2 - w, 0)):
                    return True
        return False
    return rec(0, 0, 0)


def test_page_example():
    assert solve(7, 11, 15) == {0: "AB", 7: "A", 11: "A"}
    assert solve(4, 7, 9) == {0: "AB", 4: "A", 7: "B", 8: "B"}
    assert solve(7, 11, 0) == {}


def test_impossible_from_zero():
    for D in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 16):
        assert solve(7, 11, D) is None, D
    assert solve(4, 6, 3) is None          # not a multiple of gcd(4, 6)


def test_plans_replay_to_d_and_match_oracle():
    for A in range(2, 9):
        for B in range(A + 1, 12):
            for D in range(1, 25):
                plan = solve(A, B, D)
                assert (plan is not None) == measurable(A, B, D), (A, B, D)
                if plan is not None:
                    assert replay(A, B, plan)[-1] == D, (A, B, D, plan)


def test_figures_up_to_date():
    # The step-through figure and the branching figure are the output of tools/figures/q0018.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0018.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(18).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="figure hourglass-fig".*?</svg>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern


def test_explorer_matches_page_code():
    """The BFS of the explorer (docs/javascripts/explorer/hourglass.js) returns the page's plan, or
    None exactly when the page does, on a grid of A, B, D; and its list of measurable D
    agrees with the oracle."""
    from page_tests import explorer_require, node_json

    cases = [(A, B, D) for A in range(1, 9) for B in range(A, 12) for D in range(1, 25)]
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify({ plans: cases.map(([A, B, D]) => m.hourglassSolve(A, B, D)),"
                    " reach: [[7, 11], [4, 6], [3, 5]].map(([A, B]) => m.hourglassReachable(A, B, 30)) }));")
    for (A, B, D), plan in zip(cases, got["plans"]):
        ref = solve(A, B, D)
        if ref is None:
            assert plan is None, (A, B, D)
            continue
        assert plan is not None and {t: act for t, act in plan} == ref, (A, B, D)
        assert replay(A, B, {t: act for t, act in plan})[-1] == D
    for (A, B), times in zip([(7, 11), (4, 6), (3, 5)], got["reach"]):
        assert times == [D for D in range(1, 31) if measurable(A, B, D)], (A, B)


def test_explorer_general_search():
    """The follow-ups in the box: the general search on two hourglasses with the events
    objective measures D in as many events as the page's BFS (or none exactly when the
    page finds none), the flips objective never uses more flips and its plan replays to
    D, and with a third hourglass the plan replays to D and the fewest flips agree with
    an independent Dijkstra."""
    import heapq
    import itertools

    from page_tests import explorer_require, node_json

    def step_n(sizes, tops, mask):
        nxt = [sizes[i] - v if (mask >> i) & 1 else v for i, v in enumerate(tops)]
        running = [v for v in nxt if v > 0]
        if not running:
            return None
        w = min(running)
        return w, tuple(max(v - w, 0) for v in nxt)

    def replay_n(sizes, plan, D):
        t, tops = 0, tuple(0 for _ in sizes)
        acts = {w: act for w, act in plan}
        flips = 0
        while t in acts:
            mask = sum(1 << i for i in range(len(sizes)) if "ABC"[i] in acts[t])
            flips += bin(mask).count("1")
            r = step_n(sizes, tops, mask)
            assert r is not None
            t, tops = t + r[0], r[1]
        assert t == D, (sizes, plan, t, D)
        return flips

    def min_flips(sizes, D):
        best = {(0, tuple(0 for _ in sizes)): 0}
        heap = [(0, 0, tuple(0 for _ in sizes))]
        while heap:
            c, t, tops = heapq.heappop(heap)
            if c > best[(t, tops)]:
                continue
            if t == D:
                return c
            for mask in range(1 << len(sizes)):
                r = step_n(sizes, tops, mask)
                if r is None or t + r[0] > D:
                    continue
                k, c2 = (t + r[0], r[1]), c + bin(mask).count("1")
                if c2 < best.get(k, 10 ** 9):
                    best[k] = c2
                    heapq.heappush(heap, (c2, k[0], k[1]))
        return None

    two = [(A, B, D) for A in range(2, 8) for B in range(A + 1, 12) for D in range(1, 25)]
    three = [(3, 5, 7, 11), (7, 11, 5, 15), (4, 6, 9, 13), (2, 3, 7, 8), (5, 8, 13, 30), (6, 10, 15, 7)]
    got = node_json(f"const m = {explorer_require()}; const two = {[list(c) for c in two]}, three = {[list(c) for c in three]};"
                    "console.log(JSON.stringify({ two: two.map(([A, B, D]) => [m.hourglassSolve(A, B, D), m.hourglassSearch([A, B], D), m.hourglassSearch([A, B], D, { objective: 'flips' })]),"
                    " three: three.map(([A, B, C, D]) => [m.hourglassSearch([A, B, C], D), m.hourglassSearch([A, B, C], D, { objective: 'flips' }), m.hourglassReachableN([A, B, C], 30)]) }));")
    for (A, B, D), (page, ev, fl) in zip(two, got["two"]):
        if page is None:
            assert ev is None and fl is None, (A, B, D)
            continue
        assert ev["events"] == len(page) and replay_n([A, B], ev["plan"], D) == ev["flips"]
        assert fl["flips"] == replay_n([A, B], fl["plan"], D) == min_flips([A, B], D) <= ev["flips"], (A, B, D)
    for (A, B, C, D), (ev, fl, reach) in zip(three, got["three"]):
        want = min_flips([A, B, C], D)
        if want is None:
            assert ev is None and fl is None and D not in reach, (A, B, C, D)
            continue
        assert replay_n([A, B, C], ev["plan"], D) == ev["flips"] and ev["events"] == len(ev["plan"])
        assert fl["flips"] == replay_n([A, B, C], fl["plan"], D) == want <= ev["flips"], (A, B, C, D)
        assert D in reach or D > 30
