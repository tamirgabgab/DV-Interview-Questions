import re
import subprocess
import sys
from collections import deque

from extract_code import ROOT, load_python, question_path

ns = load_python(19)
solve = ns["solve"]


def step(A, B, a, b, fa, fb):
    """Apply the flips, wait for the next hourglass; return (wait, a, b) or None."""
    a2, b2 = (A - a if fa else a), (B - b if fb else b)
    if a2 == 0 and b2 == 0:
        return None
    w = min(s for s in (a2, b2) if s > 0)
    return w, max(a2 - w, 0), max(b2 - w, 0)


def replay(A, B, plan):
    """Replay a plan from rest; return the event times. Fails on an inconsistent plan."""
    t = a = b = 0
    events = [0]
    for when in sorted(plan):
        assert when == t, f"action at {when} but the next event is at {t}"
        res = step(A, B, a, b, "A" in plan[when], "B" in plan[when])
        assert res is not None, "nothing is running"
        w, a, b = res
        t += w
        events.append(t)
    return events


def reachable(A, B, limit):
    """All (t, a, b) event states reachable from rest with t <= limit."""
    seen = {(0, 0, 0)}
    todo = deque(seen)
    while todo:
        t, a, b = todo.popleft()
        for fa in (0, 1):
            for fb in (0, 1):
                res = step(A, B, a, b, fa, fb)
                if res and t + res[0] <= limit and (t + res[0], res[1], res[2]) not in seen:
                    seen.add((t + res[0], res[1], res[2]))
                    todo.append((t + res[0], res[1], res[2]))
    return seen


def can_measure_from(A, B, a, b, D):
    """Independent oracle: can exactly D minutes pass from configuration (a, b) to an event?"""
    seen = {(0, a, b)}
    todo = deque(seen)
    while todo:
        t, a, b = todo.popleft()
        if t == D:
            return True
        for fa in (0, 1):
            for fb in (0, 1):
                res = step(A, B, a, b, fa, fb)
                if res and t + res[0] <= D and (t + res[0], res[1], res[2]) not in seen:
                    seen.add((t + res[0], res[1], res[2]))
                    todo.append((t + res[0], res[1], res[2]))
    return False


def test_page_examples():
    assert solve(7, 11, 1) == (21, {0: "AB", 7: "A", 11: "B", 14: "A", 21: ""})
    assert solve(7, 11, 4) == (7, {0: "AB", 7: ""})
    assert solve(7, 11, 15) == (0, {0: "AB", 7: "A", 11: "A"})
    assert solve(4, 6, 3) is None          # not a multiple of gcd(4, 6)


def test_earliest_end_matches_oracle():
    for A in range(2, 9):
        for B in range(A + 1, 10):
            for D in range(1, 11):
                result = solve(A, B, D)
                bound = 4 * (A + B) + D
                candidates = [t + D for t, a, b in reachable(A, B, bound)
                              if can_measure_from(A, B, a, b, D)]
                if result is None:
                    assert not candidates, (A, B, D)
                    continue
                start, plan = result
                events = replay(A, B, plan)
                assert start in events and events[-1] == start + D, (A, B, D, result)
                assert start + D == min(candidates), (A, B, D, result)


def test_explorer_matches_page_code():
    """The Dijkstra of the explorer returns the page's (start, plan), or None exactly when
    the page does, on a grid of A, B, D."""
    from page_tests import explorer_require, node_json

    cases = [(A, B, D) for A in range(2, 9) for B in range(A + 1, 12) for D in range(1, 13)]
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify(cases.map(([A, B, D]) => m.hourglassInterval(A, B, D))));")
    for (A, B, D), r in zip(cases, got):
        ref = solve(A, B, D)
        if ref is None:
            assert r is None, (A, B, D)
            continue
        start, plan = ref
        assert r is not None and r["start"] == start and {t: act for t, act in r["plan"]} == plan, (A, B, D)


def test_figures_up_to_date():
    # The step-through figure on the page is the output of tools/figures/q0019.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0019.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(19).read_text(encoding="utf-8")
    pattern = r'<div class="stepper".*?</div></div>'
    generated = re.findall(pattern, out)
    assert generated and re.findall(pattern, text) == generated


def test_explorer_general_search_interval():
    """The follow-ups in the box: the general search with the time objective ends when the
    page's Dijkstra ends (or finds nothing exactly when the page does), the flips objective
    measures D with the fewest flips (an independent Dijkstra over (tops, measured)), and
    a third hourglass measures the page's impossible D = 3 with 4, 6 and 5."""
    import heapq

    from page_tests import explorer_require, node_json

    def step_n(sizes, tops, mask):
        nxt = [sizes[i] - v if (mask >> i) & 1 else v for i, v in enumerate(tops)]
        running = [v for v in nxt if v > 0]
        if not running:
            return None
        return min(running), tuple(max(v - min(running), 0) for v in nxt)

    def min_flips_interval(sizes, D):
        start = (tuple(0 for _ in sizes), -1)
        best = {start: 0}
        heap = [(0, 0, start)]
        tie = 1
        while heap:
            c, _, (tops, m) = heapq.heappop(heap)
            if c > best[(tops, m)]:
                continue
            if m == D:
                return c
            options = []
            if m == -1:
                options.append((0, (tops, 0)))
            for mask in range(1 << len(sizes)):
                r = step_n(sizes, tops, mask)
                if r is None:
                    continue
                m2 = -1 if m == -1 else m + r[0]
                if m2 > D:
                    continue
                options.append((bin(mask).count("1"), (r[1], m2)))
            for dc, k in options:
                if c + dc < best.get(k, 10 ** 9):
                    best[k] = c + dc
                    heapq.heappush(heap, (c + dc, tie, k))
                    tie += 1
        return None

    def replay_interval(sizes, res, D):
        t, tops = 0, tuple(0 for _ in sizes)
        acts = {w: act for w, act in res["plan"]}
        flips = 0
        while t in acts:
            mask = sum(1 << i for i in range(len(sizes)) if "ABC"[i] in acts[t])
            flips += bin(mask).count("1")
            r = step_n(sizes, tops, mask)
            assert r is not None
            t, tops = t + r[0], r[1]
        assert t == res["end"] == res["start"] + D, (sizes, res, D)
        return flips

    two = [(A, B, D) for A in range(2, 8) for B in range(A + 1, 12) for D in range(1, 13)]
    three = [(4, 6, 5, 3), (7, 11, 5, 4), (3, 5, 7, 2), (4, 6, 8, 3)]
    got = node_json(f"const m = {explorer_require()}; const two = {[list(c) for c in two]}, three = {[list(c) for c in three]};"
                    "console.log(JSON.stringify({ two: two.map(([A, B, D]) => [m.hourglassInterval(A, B, D), m.hourglassSearch([A, B], D, { interval: true, objective: 'time' }), m.hourglassSearch([A, B], D, { interval: true, objective: 'flips' })]),"
                    " three: three.map(([A, B, C, D]) => [m.hourglassSearch([A, B, C], D, { interval: true, objective: 'time' }), m.hourglassSearch([A, B, C], D, { interval: true, objective: 'flips' })]) }));")
    for (A, B, D), (page, tm, fl) in zip(two, got["two"]):
        if page is None:
            assert tm is None and fl is None, (A, B, D)
            continue
        assert tm["end"] == page["start"] + D and replay_interval([A, B], tm, D) == tm["flips"]
        assert fl["flips"] == replay_interval([A, B], fl, D) == min_flips_interval([A, B], D) <= tm["flips"], (A, B, D)
    for (A, B, C, D), (tm, fl) in zip(three, got["three"]):
        want = min_flips_interval([A, B, C], D)
        if want is None:
            assert tm is None and fl is None, (A, B, C, D)
            continue
        assert replay_interval([A, B, C], tm, D) == tm["flips"] and tm["end"] <= fl["end"]
        assert fl["flips"] == replay_interval([A, B, C], fl, D) == want <= tm["flips"], (A, B, C, D)
    assert got["three"][0][0] is not None and got["three"][3][0] is None


def test_explorer_search_trace():
    """The proof panel of the box: the traced Dijkstra pops in order of t (stale copies
    skipped), measures exactly D at the goal, and the path to the goal is the page's start
    and plan."""
    from page_tests import explorer_require, node_json

    cases = [(A, B, D) for A in range(2, 9) for B in range(A + 1, 12) for D in range(1, 13)]
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify(cases.map(([A, B, D]) => m.hourglassIntervalTrace(A, B, D))));")
    for (A, B, D), tr in zip(cases, got):
        nodes, pops, ref = tr["nodes"], tr["pops"], solve(A, B, D)
        times = [nodes[p["id"]]["t"] for p in pops]
        assert times == sorted(times), (A, B, D)
        if ref is None:
            assert tr["goal"] is None, (A, B, D)
            continue
        start, plan = ref
        goal = nodes[tr["goal"]]
        assert goal["m"] == D and goal["t"] == start + D
        got_plan, got_start, i = {}, None, tr["goal"]
        while nodes[i]["parent"] >= 0:
            parent = nodes[nodes[i]["parent"]]
            if nodes[i]["act"] == "start":
                got_start = parent["t"]
            else:
                got_plan[parent["t"]] = nodes[i]["act"]
            i = nodes[i]["parent"]
        assert got_start == start and got_plan == plan, (A, B, D)
