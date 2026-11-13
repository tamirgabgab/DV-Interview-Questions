"""Question 0102: the page's topo_kahn, topo_dfs and critical_path (as published) against the
references of tools/figures/q0102.py (every valid order by backtracking, the transitive
closure for a cycle, every path for the critical path) on random graphs; the page's
examples, the edge cases (no edges, a self loop, two components, duplicate edges, several
valid orders), the traps (one expected order, two colours, duplicates counted one way,
recursion depth, the check only at the start, the longest chain by count) and the
follow-ups (the rounds of a scoreboard, the smallest order, a unique order, k workers, the
cycle from Kahn)."""

import heapq
import random
import sys

import pytest

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0102  # noqa: E402
from q0102 import A, B, C, D, E, F, G  # noqa: E402

ns = load_python(102)
topo_kahn, topo_dfs, critical_path = ns["topo_kahn"], ns["topo_dfs"], ns["critical_path"]
N, EDGES, CYCLE, DUR = q0102.N, q0102.EDGES, q0102.CYCLE_EDGES, q0102.DUR


def random_graph(rng, n, m, dag=None, loops=True, dups=True):
    """Up to m edges over n tasks; a DAG (every edge from a smaller to a larger task of a random
    permutation) when dag is True, anything when False, a coin when None."""
    dag = rng.random() < 0.5 if dag is None else dag
    perm = list(range(n))
    rng.shuffle(perm)
    rank = {v: i for i, v in enumerate(perm)}
    out = []
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a == b and (dag or not loops):
            continue
        if dag and rank[a] > rank[b]:
            a, b = b, a
        if not dups and (a, b) in out:
            continue
        out.append((a, b))
    return out


def graphs(seed, count=400, nmax=8):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(1, nmax)
        yield n, random_graph(rng, n, rng.randint(0, 2 * n + 2))


def test_page_examples():
    order = topo_kahn(N, EDGES)
    assert order == [A, E, B, C, D, F, G] and q0102.valid(N, EDGES, order)
    assert topo_dfs(N, EDGES) == ([E, A, C, B, D, F, G], None)
    assert len(q0102.all_orders(N, EDGES)) == 5
    # "A and E may swap, so may B and C, and B may run before E"
    for o in ([E, A, B, C, D, F, G], [A, E, C, B, D, F, G], [A, B, E, C, D, F, G]):
        assert q0102.valid(N, EDGES, o)
    # the rounds: A and E, then B and C, then D, F, G one by one; the in-degrees 0 1 2 2 0 1 1
    assert q0102.levels(N, EDGES) == [[A, E], [B, C], [D], [F], [G]]
    ev = q0102.kahn_events(N, EDGES)
    assert ev[0]["indeg"] == [0, 1, 2, 2, 0, 1, 1]   # after A's pop, nothing lowered yet
    assert [sum(1 for a, b in EDGES if b == v) for v in range(N)] == [0, 1, 2, 2, 0, 1, 1]
    # the cycle: D -> E; A and B come out, then the queue is empty, C D E F G left with 1 each
    assert topo_kahn(N, CYCLE) is None
    end = q0102.kahn_events(N, CYCLE)[-1]
    assert end["order"] == [A, B] and end["left"] == [C, D, E, F, G]
    assert [end["indeg"][v] for v in end["left"]] == [1] * 5 and end["cycle"] == [C, D, E]
    # DFS: the grey path A B D E C and the back edge C -> D, the cycle D E C
    order, cyc = topo_dfs(N, CYCLE)
    assert order is None and cyc == [D, E, C] and q0102.is_cycle(CYCLE, cyc)
    colors, path, hit = q0102.dfs_back(N, CYCLE)
    assert path == [A, B, D, E, C] and hit == (C, D)
    assert [v for v in range(N) if colors[v] == 2] == [F, G]   # F and G left before E
    # the DFS table: entries and exits, D black at time 8 before C looks at it
    d, f, exits = q0102.dfs_times(N, EDGES)
    assert d == [1, 2, 10, 3, 13, 4, 5] and f == [12, 9, 11, 8, 14, 7, 6]
    assert exits == [G, F, D, B, C, A, E] and f[D] == 8 < d[C]
    assert all(f[a] > f[b] for a, b in EDGES)
    # the vertex numbers in the statement
    assert EDGES == [(0, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 5), (5, 6)]


def test_part_c_example():
    total, start, slack = critical_path(N, EDGES, DUR)
    assert total == 15 == q0102.longest(N, EDGES, DUR) and sum(DUR) == 20
    assert start == [0, 3, 5, 9, 0, 10, 11] and slack == [2, 4, 0, 0, 0, 0, 0]
    es, ef, late, sl, tot = q0102.times(N, EDGES, DUR)
    assert (es, sl, tot) == (start, slack, total)
    assert ef == [3, 5, 9, 10, 5, 11, 15] and late == [5, 9, 9, 10, 5, 11, 15]
    assert [v for v in range(N) if slack[v] == 0] == [C, D, E, F, G]
    # the chains: E C D F G is 5 + 4 + 1 + 1 + 4 = 15, A B D F G as many tasks but 11
    assert sum(DUR[v] for v in (E, C, D, F, G)) == 15 and sum(DUR[v] for v in (A, B, D, F, G)) == 11
    assert critical_path(N, CYCLE, DUR) is None
    # the box's task: A takes 6, the path moves to A C D F G, the end to 16, E gets slack
    d2 = DUR[:]
    d2[A] = 6
    total, start, slack = critical_path(N, EDGES, d2)
    assert total == 16 and [v for v in range(N) if slack[v] == 0] == [A, C, D, F, G] and slack[E] == 1
    # two workers are enough: at most two tasks run at once in the earliest schedule
    total, start, _ = critical_path(N, EDGES, DUR)
    assert max(sum(1 for v in range(N) if start[v] <= t < start[v] + DUR[v]) for t in range(total)) == 2


def test_random_graphs_against_the_references():
    seen = {"dag": 0, "cyc": 0}
    for n, edges in graphs(10201):
        cyc_ref = q0102.has_cycle(n, edges)
        seen["cyc" if cyc_ref else "dag"] += 1
        order = topo_kahn(n, edges)
        assert (order is None) == cyc_ref, (n, edges)
        dorder, dcyc = topo_dfs(n, edges)
        if cyc_ref:
            assert dorder is None and q0102.is_cycle(edges, dcyc), (n, edges)
            assert q0102.is_cycle(edges, q0102.kahn_events(n, edges)[-1]["cycle"])
        else:
            assert dcyc is None and q0102.valid(n, edges, order) and q0102.valid(n, edges, dorder)
            orders = set(q0102.all_orders(n, edges)) if n <= 7 else None
            if orders is not None:
                assert tuple(order) in orders and tuple(dorder) in orders
            rng = random.Random(n * 1000 + len(edges))
            dur = [rng.randint(0, 9) for _ in range(n)]
            total, start, slack = critical_path(n, edges, dur)
            assert total == q0102.longest(n, edges, dur), (n, edges, dur)
            # every dependency respected, nothing could start earlier, slack >= 0, a task of
            # slack 0 on every heaviest path (the critical tasks reach total)
            assert all(start[b] >= start[a] + dur[a] for a, b in edges)
            assert all(start[v] == max([start[a] + dur[a] for a, b in edges if b == v], default=0) for v in range(n))
            assert min(slack, default=0) >= 0
            # delaying a task by its slack keeps the total, one more minute (dur > 0) moves it
            for v in range(n):
                d2 = dur[:]
                d2[v] += slack[v]
                assert critical_path(n, edges, d2)[0] == total
                d2[v] += 1
                assert critical_path(n, edges, d2)[0] == total + 1
    assert seen["dag"] > 100 and seen["cyc"] > 100


def test_edge_cases():
    # no edges: everything in the queue at once, the order 0..n-1
    assert topo_kahn(5, []) == [0, 1, 2, 3, 4] and topo_dfs(5, [])[1] is None
    assert critical_path(3, [], [2, 7, 1]) == (7, [0, 0, 0], [5, 0, 6])
    assert topo_kahn(0, []) == [] and topo_dfs(0, []) == ([], None) and critical_path(0, [], []) == (0, [], [])
    # a self loop is a cycle of length 1
    assert topo_kahn(3, [(0, 1), (1, 1), (1, 2)]) is None
    assert topo_dfs(3, [(0, 1), (1, 1), (1, 2)]) == (None, [1])
    assert q0102.kahn_events(3, [(0, 1), (1, 1), (1, 2)])[-1]["cycle"] == [1]
    # two components: a task of each in the starting queue
    two = [(0, 1), (1, 2), (3, 4)]
    assert topo_kahn(5, two) == [0, 3, 1, 4, 2] and q0102.valid(5, two, topo_dfs(5, two)[0])
    # duplicate edges: counted twice and lowered twice
    dup = [(0, 1), (0, 1), (1, 2), (1, 2), (1, 2)]
    assert topo_kahn(3, dup) == [0, 1, 2] and topo_dfs(3, dup) == ([0, 1, 2], None)
    assert critical_path(3, dup, [1, 2, 3])[0] == 6
    # several valid orders: the property, not one order
    assert len(q0102.all_orders(4, q0102.DIAMOND)) == 2
    assert topo_kahn(4, q0102.DIAMOND) == [0, 1, 2, 3] and topo_dfs(4, q0102.DIAMOND)[0] == [0, 2, 1, 3]
    # a cycle of two and one through every task
    assert topo_dfs(2, [(0, 1), (1, 0)]) == (None, [0, 1])
    ring = [(v, (v + 1) % 6) for v in range(6)]
    assert topo_kahn(6, ring) is None and sorted(topo_dfs(6, ring)[1]) == list(range(6))


def test_long_chain_and_the_recursion_trap():
    n = 10000
    chain = [(v, v + 1) for v in range(n - 1)]
    assert topo_kahn(n, chain) == list(range(n)) and topo_dfs(n, chain) == (list(range(n)), None)
    assert topo_dfs(n, chain + [(n - 1, 0)])[1] == list(range(n))
    assert sys.getrecursionlimit() >= 1000

    def topo_rec(n, edges):
        succ = [[] for _ in range(n)]
        for a, b in edges:
            succ[a].append(b)
        color, done = [0] * n, []

        def visit(u):
            color[u] = 1
            for v in succ[u]:
                if color[v] == 0:
                    visit(v)
            color[u] = 2
            done.append(u)

        for s in range(n):
            if color[s] == 0:
                visit(s)
        return done[::-1]

    assert topo_rec(N, EDGES) == [E, A, C, B, D, F, G]
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)   # Python's default
    try:
        with pytest.raises(RecursionError):
            topo_rec(n, chain)
    finally:
        sys.setrecursionlimit(old)


def test_traps():
    # two colours: "seen means cycle" reports one on the diamond, "skip what was seen" never does
    def two_colour(n, edges, seen_is_cycle):
        succ = [[] for _ in range(n)]
        for a, b in edges:
            succ[a].append(b)
        seen, done = [False] * n, []

        def visit(u):
            seen[u] = True
            for v in succ[u]:
                if seen[v]:
                    if seen_is_cycle:
                        return True
                    continue
                if visit(v):
                    return True
            done.append(u)
            return False

        for s in range(n):
            if not seen[s] and visit(s):
                return None
        return done[::-1]

    assert two_colour(4, q0102.DIAMOND, True) is None and not q0102.has_cycle(4, q0102.DIAMOND)
    assert two_colour(2, [(0, 1), (1, 0)], False) == [0, 1] and q0102.has_cycle(2, [(0, 1), (1, 0)])
    # duplicates: successors as a set but in-degrees from the list, a false cycle
    def kahn_set_succ(n, edges, le_zero=False, deg_from_set=False):
        succ = [set() for _ in range(n)] if not deg_from_set else [[] for _ in range(n)]
        indeg = [0] * n
        for a, b in edges:
            succ[a].add(b) if not deg_from_set else succ[a].append(b)
        for a, b in (set(edges) if deg_from_set else edges):
            indeg[b] += 1
        q, order = [v for v in range(n) if indeg[v] == 0], []
        while q:
            u = q.pop(0)
            order.append(u)
            for v in sorted(succ[u]) if not deg_from_set else succ[u]:
                indeg[v] -= 1
                if (indeg[v] <= 0) if le_zero else (indeg[v] == 0):
                    q.append(v)
        return order if len(order) >= n else None   # a task twice shows as a longer list

    dup = [(A, B), (A, B)]
    assert kahn_set_succ(2, dup) is None and topo_kahn(2, dup) == [A, B]
    assert kahn_set_succ(2, dup, le_zero=True, deg_from_set=True) == [A, B, B]   # B twice: wrong
    # the check only at the start: the cycle graph has a task of in-degree 0
    assert any(all(b != v for _, b in CYCLE) for v in range(N)) and topo_kahn(N, CYCLE) is None
    # the self loop dropped as noise gives an order for a flow that never ends
    loop = [(0, 1), (1, 1), (1, 2)]
    assert topo_kahn(3, [(a, b) for a, b in loop if a != b]) == [0, 1, 2] and topo_kahn(3, loop) is None


def test_follow_ups():
    # a scoreboard issues a whole round per clock: 5 clocks instead of 7
    assert len(q0102.levels(N, EDGES)) == 5
    # the smallest order: a min-heap instead of the queue
    def topo_min(n, edges):
        succ, indeg = [[] for _ in range(n)], [0] * n
        for a, b in edges:
            succ[a].append(b)
            indeg[b] += 1
        h = [v for v in range(n) if indeg[v] == 0]
        heapq.heapify(h)
        out = []
        while h:
            u = heapq.heappop(h)
            out.append(u)
            for v in succ[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    heapq.heappush(h, v)
        return out if len(out) == n else None

    assert topo_min(N, EDGES) == [A, B, E, C, D, F, G] == list(min(q0102.all_orders(N, EDGES)))
    for n, edges in graphs(10202, 300, 7):
        if not q0102.has_cycle(n, edges):
            orders = q0102.all_orders(n, edges)
            assert tuple(topo_min(n, edges)) == min(orders)
            # unique iff Kahn's queue never holds two tasks
            ev = q0102.kahn_events(n, edges)
            start = [v for v in range(n) if all(b != v for _, b in edges)]
            one = len(start) <= 1 and all(len(e["q"]) <= 1 for e in ev)
            assert one == (len(orders) == 1), (n, edges)
            # ... iff every two neighbours of the order have an edge between them
            o = topo_kahn(n, edges)
            assert one == all((o[i], o[i + 1]) in set(edges) for i in range(n - 1))
    # k workers: list scheduling by the least slack; two workers give 15 on the example
    def list_schedule(n, edges, dur, k):
        total, start, slack = critical_path(n, edges, dur)
        preds = [{a for a, b in edges if b == v} for v in range(n)]
        finish, running, t, done = {}, [], 0, set()
        while len(done) < n:
            ready = sorted((slack[v], v) for v in range(n) if v not in finish and preds[v] <= done)
            while ready and len(running) < k:
                _, v = ready.pop(0)
                finish[v] = t + dur[v]
                running.append(v)
            t = min(finish[v] for v in running)
            for v in [v for v in running if finish[v] == t]:
                running.remove(v)
                done.add(v)
        return max(finish.values())

    assert list_schedule(N, EDGES, DUR, 2) == 15 and list_schedule(N, EDGES, DUR, 1) == 20
    rng = random.Random(10203)
    for n, edges in graphs(10204, 200, 7):
        if q0102.has_cycle(n, edges):
            continue
        dur = [rng.randint(1, 9) for _ in range(n)]
        for k in (1, 2, 3):
            got = list_schedule(n, edges, dur, k)
            # Graham: a list schedule takes at most W/k + (1 - 1/k) CP, with W the total work
            # and CP the critical path; the best takes at least max(W/k, CP), so the ratio is
            # at most 2 - 1/k
            cp = critical_path(n, edges, dur)[0]
            assert max(cp * k, sum(dur)) <= got * k <= sum(dur) + (k - 1) * cp
