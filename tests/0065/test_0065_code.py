"""Question 0065: the page's count_islands, count_islands8 and island_sizes (as published)
against union-find on random grids; the page's examples and claims (every land cell pushed
once, the queue against the stack and the recursion on an all-land grid, the digital
topology paradox, the sum and the length of the sizes), the traps (recursion depth, marking
at the pop, the missing lower bound, the sort) and the follow-ups (the count after every
added cell, the perimeter, the distinct shapes, a 3D grid)."""

import random
import sys
from collections import deque

import pytest
from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0065  # noqa: E402

ns = load_python(65)
count_islands, count_islands8, island_sizes, flood = ns["count_islands"], ns["count_islands8"], ns["island_sizes"], ns["flood"]
DIRS4, DIRS8 = ns["DIRS4"], ns["DIRS8"]
GRID = q0065.GRID


def random_grid(rng, m, n, p):
    return ["".join("1" if rng.random() < p else "0" for _ in range(n)) for _ in range(m)]


def test_page_examples():
    assert count_islands(GRID) == 3 and count_islands8(GRID) == 2
    assert island_sizes(GRID) == [4, 3, 2] and island_sizes(GRID, True) == [5, 4]
    assert sum(island_sizes(GRID)) == sum(island_sizes(GRID, True)) == sum(row.count("1") for row in GRID) == 9
    # the islands the statement names: the square, the three cells on the right, the two at the bottom
    comps = q0065.components(GRID)
    assert comps == [{(0, 0), (0, 1), (1, 0), (1, 1)}, {(1, 4), (1, 5), (2, 4)}, {(3, 3), (4, 3)}]
    # with eight neighbours (2, 4) and (3, 3) touch at a corner and the two islands merge
    assert abs(2 - 3) == 1 and abs(4 - 3) == 1
    assert q0065.components(GRID, True)[1] == {(1, 4), (1, 5), (2, 4), (3, 3), (4, 3)}
    # the X: five islands with four neighbours, one with eight
    assert count_islands(["101", "010", "101"]) == 5 and count_islands8(["101", "010", "101"]) == 1
    assert DIRS8[:4] == DIRS4 and len(DIRS8) == 8 and all((-dr, -dc) in DIRS8 for dr, dc in DIRS8)


def test_edge_cases():
    assert count_islands([]) == 0 and island_sizes([]) == [] and count_islands8([]) == 0
    assert count_islands(["000", "000"]) == 0 and island_sizes(["000"], True) == []
    assert count_islands(["111", "111"]) == 1 and island_sizes(["111", "111"]) == [6]
    assert count_islands(["1011101"]) == 3 and island_sizes(["1011101"]) == [3, 1, 1]
    assert count_islands(["1", "0", "1", "1"]) == 2 and island_sizes(["1", "0", "1", "1"]) == [2, 1]
    board = ["10101", "01010", "10101", "01010"]                   # a checkerboard
    assert count_islands(board) == 10 and count_islands8(board) == 1 and island_sizes(board, True) == [10]


def test_against_union_find():
    rng = random.Random(65)
    for _ in range(3000):
        m, n = rng.randint(1, 9), rng.randint(1, 9)
        grid = random_grid(rng, m, n, rng.choice([0.2, 0.4, 0.5, 0.6, 0.85]))
        land = sum(row.count("1") for row in grid)
        for diag in (False, True):
            sizes = island_sizes(grid, diag)
            comps = q0065.components(grid, diag)
            assert sizes == sorted((len(c) for c in comps), reverse=True), (grid, diag)
            assert len(sizes) == (count_islands8(grid) if diag else count_islands(grid)) == len(comps)
            assert sum(sizes) == land and (not sizes or sizes[0] == max(len(c) for c in comps))
        assert count_islands8(grid) <= count_islands(grid)         # corners only merge islands


def test_every_land_cell_once():
    """The proof: every land cell leaves the queue once, is pushed once, and the labels of
    the trace are exactly the components."""
    rng = random.Random(651)
    for _ in range(300):
        grid = random_grid(rng, rng.randint(1, 7), rng.randint(1, 7), rng.choice([0.4, 0.6, 0.9]))
        land = sum(row.count("1") for row in grid)
        for diag in (False, True):
            frames = q0065.trace(grid, diag)
            pops = [f["cell"] for f in frames if f["kind"] == "pop"]
            pushes = [tuple(c) for f in frames if f["kind"] != "end" for c in f["pushed"]]
            assert len(pops) == land == len(set(map(tuple, pops))) and len(pushes) == land == len(set(pushes))
            labels = frames[-1]["labels"]
            groups = {}
            for r, row in enumerate(labels):
                for c, k in enumerate(row):
                    if k:
                        groups.setdefault(k, set()).add((r, c))
            assert sorted(groups.values(), key=min) == q0065.components(grid, diag)
            # the neighbours are checked in the order of the directions, 4 or 8 of them
            assert all(len(f["nb"]) == (8 if diag else 4) for f in frames if f["kind"] == "pop")
    # the page's walk: 9 pops, and 9 cells skipped between the first and the second island
    frames = q0065.trace(GRID)
    assert sum(1 for f in frames if f["kind"] == "pop") == 9
    assert [f["skipped"] for f in frames if f["kind"] == "start"] == [0, 9, 10] and frames[-1]["skipped"] == 8
    assert frames[1]["pushed"] == [[1, 0], [0, 1]] and frames[3]["pushed"] == []
    assert len(frames) == 13


def test_queue_stack_and_recursion_numbers():
    """20 x 20 all land: the queue reaches 20 cells, a DFS stack 191, a recursion the depth
    400 (every cell); marking at the pop makes 761 pushes instead of 400."""
    s = q0065.queue_stats(20, 20)
    assert s == {"queue": 20, "stack": 191, "recursion": 400, "pushes_late": 761, "queue_late": 39}
    for m, n in [(3, 5), (6, 4), (8, 10), (12, 12)]:
        t = q0065.queue_stats(m, n)
        assert t["queue"] <= m + n and t["recursion"] == m * n and t["pushes_late"] > m * n
    # the page's flood on the examples: the queue holds at most 2 cells
    assert max(len(f["q"]) for f in q0065.trace(GRID)) == 2


def test_paradox():
    g = q0065.DIAG_GRID
    assert count_islands(g) == 4 and count_islands8(g) == 1
    assert q0065.water_pieces(g) == 2 and q0065.water_pieces(g, True) == 1
    # a closed ring of land with four neighbours separates its lake from the sea in both senses
    ring = ["00000", "01110", "01010", "01110", "00000"]
    assert count_islands(ring) == 1 and q0065.water_pieces(ring) == 2 and q0065.water_pieces(ring, True) == 2


def dfs_recursive(grid, diag=False):
    """The trap: a recursive DFS, which needs a frame per cell of the path."""
    m, n = len(grid), len(grid[0]) if grid else 0
    seen = [[False] * n for _ in range(m)]
    dirs = DIRS8 if diag else DIRS4

    def dfs(r, c):
        seen[r][c] = True
        for dr, dc in dirs:
            a, b = r + dr, c + dc
            if 0 <= a < m and 0 <= b < n and grid[a][b] == "1" and not seen[a][b]:
                dfs(a, b)

    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                dfs(r, c)
    return count


def test_trap_recursion_depth():
    assert dfs_recursive(GRID) == 3 and dfs_recursive(GRID, True) == 2
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        with pytest.raises(RecursionError):
            dfs_recursive(["1" * 40] * 40)                           # 1,600 cells, a path through them all
        assert count_islands(["1" * 40] * 40) == 1                   # the queue has no such limit
        assert island_sizes(["1" * 60] * 60) == [3600]
    finally:
        sys.setrecursionlimit(old)


def count_mark_at_pop(grid):
    """The trap: seen checked only when a cell leaves the queue. The count is right, the
    pushes are not one per cell."""
    m, n = len(grid), len(grid[0]) if grid else 0
    seen = [[False] * n for _ in range(m)]
    count = pushes = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                q = deque([(r, c)])
                pushes += 1
                while q:
                    i, j = q.popleft()
                    if seen[i][j]:
                        continue
                    seen[i][j] = True
                    for di, dj in DIRS4:
                        a, b = i + di, j + dj
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == "1" and not seen[a][b]:
                            q.append((a, b))
                            pushes += 1
    return count, pushes


def count_no_lower_bound(grid):
    """The trap: without 0 <= a and 0 <= b, grid[-1] is the last row (or column)."""
    m, n = len(grid), len(grid[0]) if grid else 0
    seen = [[False] * n for _ in range(m)]
    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True
                q = deque([(r, c)])
                while q:
                    i, j = q.popleft()
                    for di, dj in DIRS4:
                        a, b = i + di, j + dj
                        if a < m and b < n and grid[a][b] == "1" and not seen[a][b]:
                            seen[a][b] = True
                            q.append((a, b))
    return count


def test_traps():
    rng = random.Random(652)
    for _ in range(300):
        grid = random_grid(rng, rng.randint(1, 7), rng.randint(1, 7), 0.6)
        count, pushes = count_mark_at_pop(grid)
        assert count == count_islands(grid) and pushes >= sum(row.count("1") for row in grid)
    assert count_mark_at_pop(["1" * 20] * 20) == (1, 761)
    # the missing lower bound: the first and the last row join silently
    wrap = ["100", "000", "100"]
    assert count_islands(wrap) == 2 and count_no_lower_bound(wrap) == 1
    # counting corners in part a, or forgetting them in part b: one check tells
    assert count_islands(GRID) != count_islands8(GRID)
    # sorting the wrong way, or only checking the length and the sum
    asc = sorted(island_sizes(GRID))
    assert asc != island_sizes(GRID) and len(asc) == 3 and sum(asc) == 9 and asc[0] != 4
    # at most ceil(mn / 2) islands: the checkerboard
    for m, n in [(3, 3), (4, 5), (5, 5)]:
        board = ["".join("1" if (r + c) % 2 == 0 else "0" for c in range(n)) for r in range(m)]
        assert count_islands(board) == (m * n + 1) // 2


def test_follow_ups():
    # LC 305: the count after every cell added in scan order, against a recount
    order = [(r, c) for r in range(5) for c in range(6) if GRID[r][c] == "1"]
    assert q0065.count_online(5, 6, order) == [1, 1, 1, 1, 2, 2, 2, 3, 3]
    rng = random.Random(653)
    for _ in range(200):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        cells = [(rng.randrange(m), rng.randrange(n)) for _ in range(rng.randint(1, 20))]
        for diag in (False, True):
            got = q0065.count_online(m, n, cells, diag)
            have = set()
            for k, cell in enumerate(cells):
                have.add(cell)
                grid = ["".join("1" if (r, c) in have else "0" for c in range(n)) for r in range(m)]
                assert got[k] == (count_islands8(grid) if diag else count_islands(grid))
    # LC 463: 4 per cell minus 2 per shared edge; the square 16 - 8 = 8, the L 12 - 4 = 8
    assert q0065.perimeter(GRID) == [(4, 8), (3, 8), (2, 6)]
    for _ in range(200):
        grid = random_grid(rng, rng.randint(1, 6), rng.randint(1, 6), 0.6)
        for size, per in q0065.perimeter(grid):
            assert per % 2 == 0 and per >= 4 * (size ** 0.5) - 1e-9 and per <= 2 * size + 2
        # counted the other way: every side of a land cell facing water or the edge
        comps = q0065.components(grid)
        direct = sorted(((len(c), sum(1 for (r, cc) in c for (dr, dc) in DIRS4 if (r + dr, cc + dc) not in c)) for c in comps), reverse=True)
        assert direct == q0065.perimeter(grid)
    # LC 694: the example has three shapes (a square, an L and a stick); copies count once
    assert q0065.distinct_shapes(GRID) == 3
    assert q0065.distinct_shapes(["1010", "1010", "0000", "1010"]) == 2 and count_islands(["1010", "1010", "0000", "1010"]) == 4
    # a 3D grid: the same flood with a table of six directions, against union-find in 3D
    rng3 = random.Random(654)
    for _ in range(100):
        p, m, n = rng3.randint(1, 4), rng3.randint(1, 4), rng3.randint(1, 4)
        cube = [[[rng3.random() < 0.6 for _ in range(n)] for _ in range(m)] for _ in range(p)]
        parent = {(z, r, c): (z, r, c) for z in range(p) for r in range(m) for c in range(n) if cube[z][r][c]}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for (z, r, c) in list(parent):
            for dz, dr, dc in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                if (z + dz, r + dr, c + dc) in parent:
                    a, b = find((z, r, c)), find((z + dz, r + dr, c + dc))
                    if a != b:
                        parent[a] = b
        want = len({find(x) for x in parent})
        dirs6 = [(dz, dr, dc) for dz, dr, dc in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]]
        seen, got = set(), 0
        for start in sorted(parent):
            if start in seen:
                continue
            got += 1
            seen.add(start)
            q = deque([start])
            while q:
                z, r, c = q.popleft()
                for dz, dr, dc in dirs6:
                    nb = (z + dz, r + dr, c + dc)
                    if nb in parent and nb not in seen:
                        seen.add(nb)
                        q.append(nb)
        assert got == want
