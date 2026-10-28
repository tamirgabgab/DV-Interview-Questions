"""Question 0047: the page's trap and trap_2d against direct computations (the column
formula for every row up to length 7 with heights 0 to 3 and random rows; the escape height
by relaxation for every map up to 3 x 3 with heights 0 to 2 and random maps up to 7 x 7),
the numbers the page states (the tables, the trace of part b, the traps, the edge cases),
and the explorer's JavaScript: the same steps, water and answers as the page."""

import heapq
import json
import random
from itertools import product

from extract_code import load_python
from page_tests import explorer_require, node_json

ns = load_python(47)
trap, trap_2d = ns["trap"], ns["trap_2d"]

ROW = [3, 0, 2, 0, 4]
LEET = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
MAP = [[3, 3, 3, 3, 3], [3, 1, 1, 1, 3], [3, 1, 5, 1, 3], [3, 1, 1, 1, 2], [3, 3, 3, 3, 3]]


def columns(h):
    """Water per column: min(the highest wall to the left, to the right) minus the height."""
    return [min(max(h[:i + 1]), max(h[i:])) - h[i] for i in range(len(h))]


def escape(h):
    """The escape height of every cell by relaxation: the border is its own height, and a
    cell is max(its height, the lowest escape among its neighbours), until nothing changes."""
    m, n = len(h), len(h[0])
    inf = float("inf")
    e = [[h[i][j] if i in (0, m - 1) or j in (0, n - 1) else inf for j in range(n)] for i in range(m)]
    changed = True
    while changed:
        changed = False
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                v = max(h[i][j], min(e[i + 1][j], e[i - 1][j], e[i][j + 1], e[i][j - 1]))
                if v < e[i][j]:
                    e[i][j], changed = v, True
    return e


def water_map(h):
    e = escape(h)
    return [[e[i][j] - h[i][j] for j in range(len(h[0]))] for i in range(len(h))]


def test_row_every_small_case():
    for n in range(0, 8):
        for h in product(range(4), repeat=n):
            assert trap(list(h)) == sum(columns(list(h))), h


def test_row_random():
    rng = random.Random(47)
    for _ in range(3000):
        h = [rng.randint(0, rng.choice([3, 9, 100])) for _ in range(rng.randint(1, 40))]
        assert trap(h) == sum(columns(h))


def test_map_every_small_case():
    for m, n in [(1, 1), (1, 3), (3, 1), (2, 2), (3, 3), (3, 4), (4, 3)]:
        top = 2 if m * n <= 9 else 1
        for bits in product(range(top + 1), repeat=m * n):
            h = [list(bits[r * n:(r + 1) * n]) for r in range(m)]
            assert trap_2d(h) == sum(map(sum, water_map(h))), h


def test_map_random():
    rng = random.Random(7)
    for _ in range(3000):
        m, n, top = rng.randint(1, 7), rng.randint(1, 7), rng.choice([2, 5, 9])
        h = [[rng.randint(0, top) for _ in range(n)] for _ in range(m)]
        assert trap_2d(h) == sum(map(sum, water_map(h))), h


def test_page_numbers():
    assert trap(ROW) == 7 and columns(ROW) == [0, 3, 1, 3, 0]
    assert [max(ROW[:i + 1]) for i in range(5)] == [3, 3, 3, 3, 4]
    assert [max(ROW[i:]) for i in range(5)] == [4, 4, 4, 4, 4]
    assert trap(LEET) == 6
    assert trap_2d(MAP) == 8 and water_map(MAP) == [[0] * 5, [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0] * 5]
    assert trap_2d([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]) == 4     # LeetCode 407
    # the edge cases
    assert trap([]) == trap([5]) == trap([1, 2]) == trap([2, 2, 2]) == 0
    assert trap_2d([]) == trap_2d([[]]) == trap_2d([[1, 0, 1]]) == trap_2d([[2, 0], [0, 2]]) == 0


def test_two_pointer_trace():
    """The table of part a: the left pointer moves four times, adding 0, 3, 1, 3."""
    h, l, r, lm, rm, total, rows = ROW, 0, 4, 0, 0, 0, []
    while l < r:
        if h[l] < h[r]:
            lm = max(lm, h[l]); total += lm - h[l]; rows.append((l, r, lm, lm - h[l], total)); l += 1
        else:
            rm = max(rm, h[r]); total += rm - h[r]; rows.append((l, r, rm, rm - h[r], total)); r -= 1
    assert rows == [(0, 4, 3, 0, 0), (1, 4, 3, 3, 3), (2, 4, 3, 1, 4), (3, 4, 3, 3, 7)]


def flood(h, wall=lambda level, x: max(level, x)):
    """The page's loop, recorded: (popped, level, new neighbour, its height, water)."""
    m, n = len(h), len(h[0])
    seen = [[i in (0, m - 1) or j in (0, n - 1) for j in range(n)] for i in range(m)]
    heap = [(h[i][j], i, j) for i in range(m) for j in range(n) if seen[i][j]]
    heapq.heapify(heap)
    log, water = [], 0
    while heap:
        level, i, j = heapq.heappop(heap)
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < m and 0 <= b < n and not seen[a][b]:
                seen[a][b] = True
                w = max(0, level - h[a][b])
                water += w
                log.append(((i, j), level, (a, b), h[a][b], w))
                heapq.heappush(heap, (wall(level, h[a][b]), a, b))
    return water, log


def test_map_trace_and_traps():
    water, log = flood(MAP)
    assert water == 8
    assert log == [((3, 4), 2, (3, 3), 1, 1), ((3, 3), 2, (2, 3), 1, 1), ((3, 3), 2, (3, 2), 1, 1),
                   ((2, 3), 2, (1, 3), 1, 1), ((2, 3), 2, (2, 2), 5, 0), ((1, 3), 2, (1, 2), 1, 1),
                   ((1, 2), 2, (1, 1), 1, 1), ((1, 1), 2, (2, 1), 1, 1), ((2, 1), 2, (3, 1), 1, 1)]
    # the trap: the ground pushed instead of the water surface
    assert flood(MAP, wall=lambda level, x: x)[0] == 1
    # the trap: the row formula with four straight walls
    four = sum(min(max(MAP[i][:j + 1]), max(MAP[i][j:]), max(r[j] for r in MAP[:i + 1]), max(r[j] for r in MAP[i:])) - MAP[i][j]
               for i in range(5) for j in range(5))
    assert four == 13
    # the trap: moving the higher pointer
    h, l, r, lm, rm, total = LEET, 0, len(LEET) - 1, 0, 0, 0
    while l < r:
        if h[l] > h[r]:
            lm = max(lm, h[l]); total += lm - h[l]; l += 1
        else:
            rm = max(rm, h[r]); total += rm - h[r]; r -= 1
    assert total == 14


def test_explorer_matches_the_page():
    rng = random.Random(3)
    rows = [ROW, LEET, [5], [1, 2], [2, 0, 2]] + [[rng.randint(0, 9) for _ in range(rng.randint(1, 24))] for _ in range(100)]
    maps = [MAP, [[1]], [[1, 0, 1]], [[2, 0], [0, 2]]] + [
        [[rng.randint(0, 9) for _ in range(nn)] for _ in range(mm)]
        for mm, nn in ((rng.randint(1, 10), rng.randint(1, 10)) for _ in range(100))]
    data = node_json(f"""
      const m = {explorer_require()};
      const rows = {json.dumps(rows)}, maps = {json.dumps(maps)};
      console.log(JSON.stringify({{
        rows: rows.map((h) => {{ const t = m.rwRow(h); return {{ total: t.total, steps: t.steps.length, water: t.water }}; }}),
        maps: maps.map((h) => {{ const t = m.rwMap(h); return {{ total: t.total, pops: t.steps.length, water: t.water,
          log: t.steps.flatMap((s) => s.fills.map((f) => [[s.r, s.c], s.level, [f.r, f.c], f.h, f.w])) }}; }}),
        text: m.rwText(maps[0]), back: m.rwParse(m.rwText(maps[0])),
      }}));
    """)
    for h, d in zip(rows, data["rows"]):
        assert d["total"] == trap(h) and d["water"] == columns(h) and d["steps"] == max(0, len(h) - 1)
    for h, d in zip(maps, data["maps"]):
        assert d["total"] == trap_2d(h) and d["water"] == water_map(h) and d["pops"] == len(h) * len(h[0])
    assert [(tuple(a), b, tuple(c), e, f) for a, b, c, e, f in data["maps"][0]["log"]] == flood(MAP)[1]
    assert data["back"] == MAP


def test_figure():
    """The figure of the statement: the generator's water is the page's, and the page copy
    is up to date."""
    import sys
    from extract_code import ROOT
    from page_tests import assert_figures_match

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0047

    assert sum(q0047.water(q0047.HEIGHTS)) == trap(list(q0047.HEIGHTS)) == 7
    assert_figures_match(47)
