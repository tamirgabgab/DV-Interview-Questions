"""Question 0046: the page's largest_square and largest_rectangle against a brute force
(every grid up to 3 x 3 and 2 x 5, random grids up to 8 x 8, the edge cases), the page's
own tester (the `py` block of the interviewer, run after the solutions), the numbers the
page states (the dp example, the histogram rows, the stack trace of row 1, the traps), and
the explorer's JavaScript: the same dp, heights, stack events and answers as the page."""

import json
import random
from itertools import product

from extract_code import blocks, load_python
from page_tests import explorer_require, node_json

ns = load_python(46)
square, rect = ns["largest_square"], ns["largest_rectangle"]

SQ = [[1, 0, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
RECT = [[1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 0, 1]]


def ones(grid, tl, br):
    (r1, c1), (r2, c2) = tl, br
    return all(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))


def brute(grid, sq):
    m, n = len(grid), len(grid[0])
    best = 0
    for r1, r2 in ((a, b) for a in range(m) for b in range(a, m)):
        for c1, c2 in ((a, b) for a in range(n) for b in range(a, n)):
            if sq and r2 - r1 != c2 - c1:
                continue
            if ones(grid, (r1, c1), (r2, c2)):
                best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
    return best


def valid(grid, got, sq):
    area, tl, br = got
    assert area == brute(grid, sq), grid
    if not area:
        assert tl is None and br is None
        return
    (r1, c1), (r2, c2) = tl, br
    assert (r2 - r1 + 1) * (c2 - c1 + 1) == area and ones(grid, tl, br)
    assert not sq or r2 - r1 == c2 - c1


def grids(m, n):
    for bits in product((0, 1), repeat=m * n):
        yield [list(bits[r * n:(r + 1) * n]) for r in range(m)]


def test_every_small_grid():
    for m, n in [(1, 1), (1, 4), (4, 1), (2, 2), (2, 3), (3, 2), (3, 3), (2, 5), (5, 2)]:
        for g in grids(m, n):
            valid(g, square(g), True)
            valid(g, rect(g), False)


def test_random_grids():
    rng = random.Random(46)
    for _ in range(3000):
        m, n, p = rng.randint(1, 8), rng.randint(1, 8), rng.choice([0.3, 0.6, 0.8, 0.95, 1])
        g = [[int(rng.random() < p) for _ in range(n)] for _ in range(m)]
        valid(g, square(g), True)
        valid(g, rect(g), False)


def test_edge_cases():
    for g in ([], [[]], [[0]], [[0, 0], [0, 0]]):
        assert square(g) == rect(g) == (0, None, None)
    assert square([[1]]) == rect([[1]]) == (1, (0, 0), (0, 0))
    assert square([[1, 1, 1]]) == (1, (0, 0), (0, 0)) and rect([[1, 1, 1]]) == (3, (0, 0), (0, 2))
    assert rect([[1], [1], [1]]) == (3, (0, 0), (2, 0))


def test_the_page_tester():
    # the interviewer's tester is fenced as py so that the run panel does not run it
    (tester,) = blocks(46, "py")
    exec(compile(tester, "<question 0046 tester>", "exec"), dict(ns))


def full_dp(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                dp[i][j] = 1 + min(dp[i - 1][j] if i else 0, dp[i][j - 1] if j else 0, dp[i - 1][j - 1] if i and j else 0)
    return dp


def rect_events(grid):
    """The page's stack loop, recorded: ('row', i, heights), ('pop', i, j, col, height,
    left, area) and ('push', i, j), as the explorer steps it."""
    n = len(grid[0])
    heights, out = [0] * n, []
    for i, row in enumerate(grid):
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == 1 else 0
        out.append(("row", i, heights[:]))
        stack = []
        for j in range(n + 1):
            h = heights[j] if j < n else 0
            while stack and heights[stack[-1]] >= h:
                col = stack.pop()
                left = stack[-1] + 1 if stack else 0
                out.append(("pop", i, j, col, heights[col], left, heights[col] * (j - left)))
            stack.append(j)
            if j < n:
                out.append(("push", i, j))
    return out


def test_page_numbers():
    assert full_dp(SQ) == [[1, 0, 1, 1, 1], [1, 1, 1, 2, 2], [0, 1, 2, 2, 3], [1, 1, 2, 3, 0]]
    assert square(SQ) == (9, (0, 2), (2, 4)) and ones(SQ, (1, 1), (3, 3))
    assert rect(RECT) == (8, (0, 0), (1, 3)) and square(RECT)[0] == 4
    ev = rect_events(RECT)
    assert [e[2] for e in ev if e[0] == "row"] == [[1, 1, 1, 1, 0], [2, 2, 2, 2, 1], [0, 3, 3, 0, 2]]
    assert [max(e[6] for e in ev if e[0] == "pop" and e[1] == i) for i in range(3)] == [4, 8, 6]
    # the stack trace of row 1: the pops at j = 1 to 5 and their areas
    pops = [(e[2], e[3], e[4], e[5], e[6]) for e in ev if e[0] == "pop" and e[1] == 1]
    assert pops == [(1, 0, 2, 0, 2), (2, 1, 2, 0, 4), (3, 2, 2, 0, 6), (4, 3, 2, 0, 8), (5, 4, 1, 0, 5)]
    # the traps: the widest row and the tallest column at (1, 1) of [[0, 1], [1, 1]] are no rectangle
    assert rect([[0, 1], [1, 1]])[0] == 2
    assert rect([[1, 1, 1]])[0] == 3


def test_explorer_matches_the_page():
    rng = random.Random(7)
    cases = [SQ, RECT, [[0]], [[1]], [[0, 1], [1, 1]]]
    for _ in range(150):
        m, n, p = rng.randint(1, 16), rng.randint(1, 16), rng.choice([0.5, 0.7, 0.9])
        cases.append([[int(rng.random() < p) for _ in range(n)] for _ in range(m)])
    data = node_json(f"""
      const m = {explorer_require()};
      const cases = {json.dumps(cases)};
      console.log(JSON.stringify(cases.map((g) => {{
        const s = m.moSquare(g), r = m.moRect(g);
        return {{
          sq: s.result, dp: s.dp, sqFrames: s.frames.length,
          rect: r.result, H: r.H,
          ev: r.events.map((e) => e.t === "row" ? ["row", e.i] : e.t === "pop" ? ["pop", e.i, e.j, e.col, e.height, e.left, e.cand.area] : ["push", e.i, e.j]),
          countSq: m.moCount(g, s.result.area, true), countRect: m.moCount(g, r.result.area, false),
          text: m.moText(g), back: m.moParse(m.moText(g)),
        }};
      }})));
    """)
    for g, d in zip(cases, data):
        tup = lambda r: (r["area"], tuple(r["tl"]) if r["tl"] else None, tuple(r["br"]) if r["br"] else None)
        assert tup(d["sq"]) == square(g) and tup(d["rect"]) == rect(g)
        assert d["dp"] == full_dp(g) and d["sqFrames"] == len(g) * len(g[0])
        ev = rect_events(g)
        assert d["H"] == [e[2] for e in ev if e[0] == "row"]
        assert [tuple(e) for e in d["ev"]] == [(e[0], e[1]) if e[0] == "row" else tuple(e) for e in ev]
        assert d["back"] == g
        if len(g) * len(g[0]) <= 64:
            for sq, key in ((True, "countSq"), (False, "countRect")):
                area = (square if sq else rect)(g)[0]
                want = 0 if not area else sum(
                    1 for r1 in range(len(g)) for r2 in range(r1, len(g)) for c1 in range(len(g[0])) for c2 in range(c1, len(g[0]))
                    if (r2 - r1 + 1) * (c2 - c1 + 1) == area and (not sq or r2 - r1 == c2 - c1) and ones(g, (r1, c1), (r2, c2)))
                assert d[key] == want
    assert data[0]["countSq"] == 2            # the page's two 3 x 3 squares
