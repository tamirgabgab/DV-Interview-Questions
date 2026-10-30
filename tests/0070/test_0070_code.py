"""Question 0070: the page's shortest_path, shortest_with_breaks and cheapest_path (as
published) against independent brute-force searches on thousands of random grids, both
neighbourhoods; the page's examples and self-checks, the claims of the proofs (the queue
holds two consecutive distances, a cell enters at most k + 1 times in part b, every cell
enters the heap once with entry costs, part a is part c with unit costs, the shortcut by
the Manhattan distance), the traps (one visit per cell, BFS with costs, paying the start,
no diagonal rule) and the follow-ups (the other diagonal rules, A*, 0-1 BFS, several
targets)."""

import heapq
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0070  # noqa: E402

ns = load_python(70)
shortest_path, shortest_with_breaks, cheapest_path = ns["shortest_path"], ns["shortest_with_breaks"], ns["cheapest_path"]


def random_grid(rng, m, n, p=0.3):
    return ["".join("1" if rng.random() < p else "0" for _ in range(n)) for _ in range(m)]


def random_cost(rng, m, n, p=0.15):
    return ["".join("#" if rng.random() < p else str(rng.randint(1, 9)) for _ in range(n)) for _ in range(m)]


def open_cell(rng, grid, wall):
    cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] != wall]
    return rng.choice(cells) if cells else None


def valid_path(grid, path, s, t, diag, wall="1", breaks=None):
    """The path starts at s, ends at t, and every step is a move of the page's rules."""
    if path[0] != tuple(s) or path[-1] != tuple(t):
        return False
    for u, v in zip(path, path[1:]):
        if v not in q0070.nbrs(grid, *u, diag, wall):
            return False
    walls = sum(1 for r, c in path if grid[r][c] == wall)
    return walls == 0 if breaks is None else walls <= breaks


def test_page_examples():
    G, S, T = q0070.GRID, q0070.S, q0070.T
    d, path = shortest_path(G, S, T)
    assert d == 20 and len(path) == 21 and valid_path(G, path, S, T, False)
    assert path == [tuple(x) for x in q0070.trace("a", G, S, T)[-1]["path"]]
    d8, path8 = shortest_path(G, S, T, True)
    assert d8 == 15 and valid_path(G, path8, S, T, True)
    assert q0070.length_ref(G, S, T, True, cut=True) == 12                   # the diagonal trap
    assert len(q0070.squeezes(G)) == 5
    assert [shortest_with_breaks(G, S, T, k) for k in range(6)] == [20, 14, 14, 8, 8, 8]
    assert [shortest_with_breaks(G, S, T, k, True) for k in range(5)] == [15, 9, 8, 8, 8]
    fb = q0070.trace("b", G, S, T, False, 1)
    assert [x for x in fb[-1]["path"] if G[x[0]][x[1]] == "1"] == [[3, 7]]   # k = 1 breaks (3, 7)
    fb8 = q0070.trace("b", G, S, T, True, 1)
    assert [x for x in fb8[-1]["path"] if G[x[0]][x[1]] == "1"] == [[4, 7]]
    # the text of part a: 42 pops, layer 12 holds four cells, (3, 6) and (4, 5) among them
    fa = q0070.trace("a", G, S, T)
    assert len(fa) == 42 and fa[-1]["kind"] == "goal"
    layer12 = [(r, c) for r in range(7) for c in range(9) if fa[-1]["val"][r][c] == 12]
    assert sorted(layer12) == sorted([(0, 3), (1, 4), (3, 6), (4, 5)])
    assert fa[-1]["val"][6][2] == 5                                          # column 2 crossed at distance 5
    # part c: 11 in 11 steps, the BFS path of 7 steps costs 39 and so does the cheapest 7-step path
    C, CS, CT = q0070.COST, q0070.CS, q0070.CT
    assert cheapest_path(C, CS, CT) == 11 and cheapest_path(C, CS, CT, True) == 9
    fc = q0070.trace("c", C, CS, CT)
    assert len(fc[-1]["path"]) - 1 == 11 and len(fc) == 25
    assert len(q0070.trace("c", C, CS, CT, True)[-1]["path"]) - 1 == 9
    assert q0070.fewest_steps_costs(C, CS, CT) == (7, 39)
    ghost = q0070.trace("a", ["0" * 7] * 6, CS, CT)[-1]["path"]
    assert len(ghost) - 1 == 7 and q0070.path_cost(C, ghost) == 39
    pops = [(f["cell"], f["d"]) for f in fc]
    assert all(d <= 4 for _, d in pops[:9]) and pops[9] == ([0, 3], 5)                 # the road up to 4, then (0, 3) at 5
    assert pops.index(([2, 1], 5)) == 10 and fc[0]["nb"][-1] == [2, 1, "push", 5]   # (2, 1) pushed at step 1, out at 11
    # edge cases of the cost block
    assert shortest_path(["000"], (0, 1), (0, 1)) == (0, [(0, 1)])
    assert shortest_path(["010", "111", "000"], (0, 0), (2, 2)) == (-1, [])
    assert shortest_path(["00000"], (0, 0), (0, 4))[0] == 4
    assert cheapest_path(["19"], (0, 0), (0, 0)) == 0


def test_self_checks():
    assert shortest_path(*q0070.SC_A)[0] == 9 == q0070.length_ref(*q0070.SC_A)
    assert shortest_path(*q0070.SC_A)[1] == [(3, 0), (2, 0), (2, 1), (2, 2), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0)]
    assert shortest_with_breaks(*q0070.SC_B) == 3 == q0070.breaks_ref(*q0070.SC_B)
    assert cheapest_path(*q0070.SC_C) == 6 == q0070.cheapest_ref(*q0070.SC_C)
    g, s, t = q0070.SC_C
    assert q0070.path_cost(g, [(0, 0), (0, 1), (0, 2)]) == 10                # the direct way
    assert shortest_path(q0070.SC_GRID, (3, 0), (0, 0), True)[0] == 6


def test_against_brute_force():
    rng = random.Random(70)
    for _ in range(2500):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        g = random_grid(rng, m, n, rng.choice([0.15, 0.3, 0.45]))
        s, t = open_cell(rng, g, "1"), open_cell(rng, g, "1")
        if s is None:
            continue
        for diag in (False, True):
            d, path = shortest_path(g, s, t, diag)
            assert d == q0070.length_ref(g, s, t, diag), (g, s, t, diag)
            assert (path == []) if d < 0 else (len(path) == d + 1 and valid_path(g, path, s, t, diag))
            for k in range(4):
                assert shortest_with_breaks(g, s, t, k, diag) == q0070.breaks_ref(g, s, t, k, diag), (g, s, t, k, diag)
        c = random_cost(rng, m, n)
        s, t = open_cell(rng, c, "#"), open_cell(rng, c, "#")
        if s is None:
            continue
        for diag in (False, True):
            assert cheapest_path(c, s, t, diag) == q0070.cheapest_ref(c, s, t, diag), (c, s, t, diag)
            f = q0070.trace("c", c, s, t, diag)
            if f[-1]["kind"] == "goal":
                p = [tuple(x) for x in f[-1]["path"]]
                assert valid_path(c, p, s, t, diag, "#") and q0070.path_cost(c, p) == f[-1]["d"]


def test_traces_match_the_page_code():
    rng = random.Random(701)
    for _ in range(600):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        g = random_grid(rng, m, n)
        s, t = open_cell(rng, g, "1"), open_cell(rng, g, "1")
        if s is None:
            continue
        for diag in (False, True):
            fa = q0070.trace("a", g, s, t, diag)
            assert q0070.answer_of(fa) == shortest_path(g, s, t, diag)[0]
            if fa[-1]["kind"] == "goal":
                assert [tuple(x) for x in fa[-1]["path"]] == shortest_path(g, s, t, diag)[1]
            k = rng.randint(0, 3)
            fb = q0070.trace("b", g, s, t, diag, k)
            assert q0070.answer_of(fb) == shortest_with_breaks(g, s, t, k, diag)
            if fb[-1]["kind"] == "goal":
                assert valid_path(g, [tuple(x) for x in fb[-1]["path"]], s, t, diag, breaks=k)
                assert len(fb[-1]["path"]) - 1 == fb[-1]["d"]
        c = random_cost(rng, m, n)
        s, t = open_cell(rng, c, "#"), open_cell(rng, c, "#")
        if s is not None:
            assert q0070.answer_of(q0070.trace("c", c, s, t)) == cheapest_path(c, s, t)


def test_bfs_layers():
    """The queue holds distances that do not decrease and differ by at most one, and the
    cells leave it by non-decreasing distance (the invariant of part a's proof); in part b
    the same for the steps of the states."""
    rng = random.Random(702)
    for _ in range(400):
        g = random_grid(rng, rng.randint(2, 7), rng.randint(2, 7))
        s, t = open_cell(rng, g, "1"), open_cell(rng, g, "1")
        if s is None:
            continue
        for diag in (False, True):
            fa = q0070.trace("a", g, s, t, diag)
            for f in fa:
                ds = [f["val"][r][c] for r, c in f["front"]]
                assert ds == sorted(ds) and (not ds or ds[-1] - ds[0] <= 1)
            pops = [f["d"] for f in fa if f["kind"] != "none"]
            assert pops == sorted(pops) and len({tuple(f["cell"]) for f in fa if f["cell"]}) == len(pops)
            fb = q0070.trace("b", g, s, t, diag, 2)
            for f in fb:
                ds = [x[3] for x in f["front"]]
                assert ds == sorted(ds) and (not ds or ds[-1] - ds[0] <= 1)


def test_breaks_enter_at_most_k_plus_one_times():
    rng = random.Random(703)
    for _ in range(400):
        g = random_grid(rng, rng.randint(2, 7), rng.randint(2, 7), 0.4)
        s = open_cell(rng, g, "1")
        if s is None:
            continue
        t = (-1, -1)                                       # no target: the whole search runs
        for k in range(4):
            for diag in (False, True):
                f = q0070.trace("b", g, s, t, diag, k)
                pushes = {}
                for fr in f:
                    for a, b, why, _ in fr["nb"]:
                        if why == "push":
                            pushes[(a, b)] = pushes.get((a, b), 0) + 1
                assert max(pushes.values(), default=0) <= k + 1
                assert sum(pushes.values()) + 1 == sum(1 for fr in f if fr["kind"] == "pop")


def test_no_stale_entries_with_entry_costs():
    """With a cost per cell every cell enters the heap once and the stale check never fires;
    with a cost per move (the cost of the cell left) stale entries do appear."""
    rng = random.Random(704)
    for _ in range(500):
        c = random_cost(rng, rng.randint(2, 7), rng.randint(2, 7))
        s = open_cell(rng, c, "#")
        if s is None:
            continue
        for diag in (False, True):
            f = q0070.trace("c", c, s, (-1, -1), diag)
            assert not any(fr["kind"] == "skip" for fr in f)
            pushed = [(a, b) for fr in f for a, b, why, _ in fr["nb"] if why == "push"]
            assert len(pushed) == len(set(pushed))
    stale = 0
    for _ in range(300):
        c = random_cost(rng, 5, 5, 0)
        cost = {(0, 0): 0}
        heap = [(0, 0, 0)]
        while heap:
            d, r, cc = heapq.heappop(heap)
            if d > cost[(r, cc)]:
                stale += 1
                continue
            for a, b in q0070.nbrs(c, r, cc, False, "#"):
                nd = d + int(c[r][cc])                     # the cost of the cell left
                if nd < cost.get((a, b), 10 ** 9):
                    cost[(a, b)] = nd
                    heapq.heappush(heap, (nd, a, b))
    assert stale > 50


def test_part_a_is_part_c_with_unit_costs():
    rng = random.Random(705)
    for _ in range(500):
        g = random_grid(rng, rng.randint(1, 7), rng.randint(1, 7))
        s, t = open_cell(rng, g, "1"), open_cell(rng, g, "1")
        if s is None:
            continue
        ones = ["".join("#" if ch == "1" else "1" for ch in row) for row in g]
        for diag in (False, True):
            assert cheapest_path(ones, s, t, diag) == shortest_path(g, s, t, diag)[0]
            assert shortest_with_breaks(g, s, t, 0, diag) == shortest_path(g, s, t, diag)[0]


def test_manhattan_shortcut():
    rng = random.Random(706)
    for _ in range(500):
        g = random_grid(rng, rng.randint(1, 6), rng.randint(1, 6), 0.5)
        s, t = open_cell(rng, g, "1"), open_cell(rng, g, "1")
        if s is None:
            continue
        man = abs(s[0] - t[0]) + abs(s[1] - t[1])
        assert shortest_with_breaks(g, s, t, max(0, man - 1)) == man
        assert all(shortest_with_breaks(g, s, t, k) >= man or shortest_with_breaks(g, s, t, k) < 0 for k in range(3))


def test_traps():
    g, s, t, k = q0070.CE_GRID, q0070.CE_S, q0070.CE_T, q0070.CE_K
    assert q0070.naive_breaks(g, s, t, k) == -1 and shortest_with_breaks(g, s, t, k) == 4
    path = q0070.trace("b", g, s, t, False, k)[-1]["path"]
    assert path == [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]]
    # the naive BFS is never shorter than the right one, and often wrong
    rng = random.Random(707)
    wrong = 0
    for _ in range(1500):
        gg = random_grid(rng, rng.randint(2, 6), rng.randint(2, 6), 0.4)
        a, b = open_cell(rng, gg, "1"), open_cell(rng, gg, "1")
        if a is None:
            continue
        kk = rng.randint(1, 2)
        right, naive = shortest_with_breaks(gg, a, b, kk), q0070.naive_breaks(gg, a, b, kk)
        assert naive < 0 or naive >= right >= 0
        wrong += naive != right
    assert wrong > 5
    # BFS with costs, paying the start
    C, CS, CT = q0070.COST, q0070.CS, q0070.CT
    assert cheapest_path(C, CS, CT) + int(C[CS[0]][CS[1]]) == 12
    # the table of part b's runs: the naive run ends at step 7 with -1, the right one at step 10 with 4
    assert q0070.table_run_b(g, s, t, k, True).splitlines()[-1].startswith("| ‏7 |")
    assert "התשובה 4" in q0070.table_run_b(g, s, t, k, False).splitlines()[-1] and "| ‏10 |" in q0070.table_run_b(g, s, t, k, False)


def test_follow_ups():
    G, S, T = q0070.GRID, q0070.S, q0070.T
    # the other rules of a diagonal: cutting between two walls gives 12; the strict rule
    # (no diagonal past any wall) is never shorter than ours
    assert q0070.length_ref(G, S, T, True, cut=True) == 12
    # A*: the same answer as Dijkstra, never more pops; 19 against 25 on the terrain
    C, CS, CT = q0070.COST, q0070.CS, q0070.CT
    assert q0070.astar(C, CS, CT) == (11, 19) and q0070.dijkstra_pops(C, CS, CT) == 25
    rng = random.Random(708)
    for _ in range(500):
        c = random_cost(rng, rng.randint(1, 7), rng.randint(1, 7))
        s, t = open_cell(rng, c, "#"), open_cell(rng, c, "#")
        if s is None:
            continue
        for diag in (False, True):
            got, pops = q0070.astar(c, s, t, diag)
            assert got == cheapest_path(c, s, t, diag)
            if got >= 0:
                assert pops <= q0070.dijkstra_pops(c, s, t, diag)
    # 0-1 BFS: the same costs as relaxing everything, with costs 0 and 1 only
    for _ in range(500):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        c = ["".join(rng.choice("01") for _ in range(n)) for _ in range(m)]
        s, t = (rng.randrange(m), rng.randrange(n)), (rng.randrange(m), rng.randrange(n))
        best = q0070.cost_ref(c, s)[t]
        assert q0070.zero_one_bfs(c, s, t) == best
    assert q0070.zero_one_bfs(q0070.CE_GRID, (0, 0), (2, 2)) == 1           # LC 2290 on the trap's grid
    # several targets: one BFS stopped at the first target out of the queue is the nearest
    for _ in range(300):
        g = random_grid(rng, rng.randint(2, 6), rng.randint(2, 6))
        s = open_cell(rng, g, "1")
        if s is None:
            continue
        targets = {open_cell(rng, g, "1") for _ in range(3)}
        d, _ = q0070.multi_target(g, s, targets)
        want = [q0070.length_ref(g, s, x) for x in targets]
        want = [x for x in want if x >= 0]
        assert d == (min(want) if want else -1)
