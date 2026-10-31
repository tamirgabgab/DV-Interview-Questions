"""Question 0067: the page's delay_bfs, delay_dijkstra and delay_directed (as published)
against every simple path on random graphs; the page's examples and self-checks, the
claims of the proofs (the queue holds at most two consecutive times, every node settles
once, part a is part b with unit weights), the traps (BFS with weights, a negative weight,
the stale entries, the sum, the -1 case, both directions in part c) and the follow-ups
(the round trip on the reversed graph, a virtual source)."""

import heapq
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0067  # noqa: E402

ns = load_python(67)
delay_bfs, delay_dijkstra, delay_directed = ns["delay_bfs"], ns["delay_dijkstra"], ns["delay_directed"]


def random_graph(rng, n, m, wmax=9):
    """m distinct links (u != v) with weights 1..wmax; not necessarily connected."""
    pairs = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
    rng.shuffle(pairs)
    return [[u, v, rng.randint(1, wmax)] for u, v in pairs[:m]]


def test_page_examples():
    assert delay_bfs(q0067.N, q0067.EDGES_A, q0067.K) == 3
    assert delay_dijkstra(q0067.N, q0067.EDGES, q0067.K) == 6
    assert delay_directed(q0067.N, q0067.EDGES, q0067.K) == -1
    assert delay_dijkstra(5, q0067.EDGES[:6], 1, directed=True) == 7            # without node 6
    # the times the text names
    assert q0067.brute_times(6, q0067.EDGES_A, 1, weighted=False) == [0, 1, 1, 2, 2, 3]
    assert q0067.brute_times(6, q0067.EDGES, 1) == [0, 1, 2, 4, 5, 6]
    assert q0067.brute_times(6, q0067.EDGES, 1, directed=True) == [0, 1, 5, 7, 7, None]
    assert sum(q0067.brute_times(6, q0067.EDGES, 1)) == 18                      # the sum trap
    # the edge cases of the cost block
    assert delay_bfs(1, [], 1) == 0 and delay_dijkstra(1, [], 1) == 0
    assert delay_bfs(3, [[1, 2], [1, 2], [2, 2], [2, 3]], 1) == 2                # a double link, a self-loop
    assert delay_bfs(3, [[1, 2]], 1) == -1 and delay_dijkstra(3, [[1, 2, 4]], 1) == -1
    assert delay_dijkstra(2, [[1, 2, 0]], 1) == 0                                # a zero weight is allowed


def test_self_checks():
    ring = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [1, 7], [2, 6]]
    assert delay_bfs(7, ring, 1) == 3
    assert q0067.brute_times(7, ring, 1, weighted=False) == [0, 1, 2, 3, 3, 2, 1]
    four = [[1, 2, 4], [1, 3, 1], [3, 2, 1], [2, 4, 2], [3, 4, 5]]
    assert delay_dijkstra(4, four, 1) == 4 and q0067.brute_times(4, four, 1) == [0, 2, 1, 4]
    four_c = [[1, 2, 4], [1, 3, 1], [2, 3, 1], [2, 4, 2], [3, 4, 5]]
    assert delay_directed(4, four_c, 1) == 6 and q0067.brute_times(4, four_c, 1, directed=True) == [0, 4, 1, 6]


def test_against_every_path():
    rng = random.Random(67)
    for _ in range(3000):
        n = rng.randint(1, 7)
        m = rng.randint(0, min(12, n * (n - 1)))
        edges = random_graph(rng, n, m)
        k = rng.randint(1, n)
        want_a = q0067.answer_of(q0067.brute_times(n, edges, k, weighted=False))
        assert delay_bfs(n, [[u, v] for u, v, _ in edges], k) == want_a, (n, edges, k)
        want_b = q0067.answer_of(q0067.brute_times(n, edges, k))
        assert delay_dijkstra(n, edges, k) == want_b, (n, edges, k)
        want_c = q0067.answer_of(q0067.brute_times(n, edges, k, directed=True))
        assert delay_directed(n, edges, k) == want_c == delay_dijkstra(n, edges, k, directed=True), (n, edges, k)
        # part a is part b with every weight 1, and BFS is then right
        ones = [[u, v, 1] for u, v, _ in edges]
        assert delay_dijkstra(n, ones, k) == delay_bfs(n, [[u, v] for u, v, _ in edges], k)
        assert q0067.answer_of(q0067.bfs_with_weights(n, ones, k)) == want_a


def test_bfs_invariant_and_order():
    """The queue holds times that do not decrease and differ by at most one; the nodes leave
    it by non-decreasing time, each once."""
    rng = random.Random(671)
    for _ in range(500):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.randint(0, 14))
        k = rng.randint(1, n)
        ev = q0067.bfs_trace(n, [[u, v] for u, v, _ in edges], k)
        for e in ev:
            times = [e["t"][v - 1] for v in e["q"]]
            assert times == sorted(times) and (not times or times[-1] - times[0] <= 1), (edges, k)
        pops = [e for e in ev if e["kind"] == "pop"]
        assert [e["d"] for e in pops] == sorted(e["d"] for e in pops)
        assert len({e["u"] for e in pops}) == len(pops)
        assert ev[-1]["ans"] == delay_bfs(n, [[u, v] for u, v, _ in edges], k)
    ev = q0067.bfs_trace(q0067.N, q0067.EDGES_A, q0067.K)
    assert [e["u"] for e in ev if e["kind"] == "pop"] == [1, 2, 3, 5, 4, 6]


def test_dijkstra_settles_once_and_in_order():
    """Every reachable node settles exactly once, in non-decreasing time, with its shortest
    time; every pop that is not the first of its node is stale and skipped; the heap never
    holds more than E + 1 entries."""
    rng = random.Random(672)
    for _ in range(500):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.randint(0, 14))
        k = rng.randint(1, n)
        for directed in (False, True):
            ev = q0067.dijkstra_trace(n, edges, k, directed)
            best = q0067.brute_times(n, edges, k, directed)
            pops = [e for e in ev if e["kind"] == "pop"]
            assert [e["d"] for e in pops] == sorted(e["d"] for e in pops)
            assert sorted(e["u"] for e in pops) == [v for v in range(1, n + 1) if best[v - 1] is not None]
            assert all(e["d"] == best[e["u"] - 1] for e in pops)
            for e in ev:
                if e["kind"] == "skip":
                    assert e["d"] > e["t"][e["u"] - 1] and e["u"] in e["settled"]
                assert len(e["heap"]) <= len(edges) * (1 if directed else 2) + 1
            assert ev[-1]["ans"] == delay_dijkstra(n, edges, k, directed)
    # the example: (5,3) and (7,5) are the stale entries, skipped at steps 5 and 8
    ev = q0067.dijkstra_trace(q0067.N, q0067.EDGES, q0067.K)
    taken = [(e["kind"], e["d"], e["u"]) for e in ev if e["kind"] in ("pop", "skip")]
    assert taken == [("pop", 0, 1), ("pop", 1, 2), ("pop", 2, 3), ("pop", 4, 4), ("skip", 5, 3), ("pop", 5, 5), ("pop", 6, 6), ("skip", 7, 5)]
    assert q0067.parents(ev) == {2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
    evc = q0067.dijkstra_trace(q0067.N, q0067.EDGES, q0067.K, directed=True)
    assert evc[-1]["settled"] == [1, 2, 3, 4, 5] and evc[-1]["t"] == [0, 1, 5, 7, 7, None]


def test_trap_bfs_with_weights():
    wrong = q0067.bfs_with_weights(q0067.N, q0067.EDGES, q0067.K)
    assert wrong == [0, 1, 5, 7, 7, 8] and q0067.answer_of(wrong) == 8
    rng = random.Random(673)
    seen_wrong = 0
    for _ in range(500):
        n = rng.randint(2, 7)
        edges = random_graph(rng, n, rng.randint(1, 12))
        k = rng.randint(1, n)
        right = q0067.brute_times(n, edges, k)
        wrong = q0067.bfs_with_weights(n, edges, k)
        assert all(a is None and b is None or a >= b for a, b in zip(wrong, right))   # never shorter than possible
        seen_wrong += wrong != right
    assert seen_wrong > 100


def lazy_dijkstra_times(n, edges, k):
    """The page's loop, returning the times and how many pops settled (the proof's count)."""
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
    t = [float("inf")] * (n + 1)
    t[k] = 0
    heap, settled = [(0, k)], 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > t[u]:
            continue
        settled += 1
        for v, w in adj[u]:
            if d + w < t[v]:
                t[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return t[1:], settled


def test_trap_negative_weight():
    """Node 2 settles at 5 and improves to 2 after node 3 settles: the lazy loop reopens it
    and counts it twice, so with a fourth, unreachable node the -1 check fails."""
    neg = [[1, 2, 5], [1, 3, 10], [3, 2, -8]]
    times, settled = lazy_dijkstra_times(3, neg, 1)
    assert times == [0, 2, 10] and settled == 4
    assert delay_directed(3, neg, 1) == 10
    assert delay_directed(4, neg, 1) == float("inf")           # node 4 is unreachable, yet settled >= n


def test_trap_stale_entries_cost():
    """Without the skip the answer is still right, but a dense graph relaxes far more."""
    def without_skip(n, edges, k):
        adj = [[] for _ in range(n + 1)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        t = [float("inf")] * (n + 1)
        t[k] = 0
        heap, relaxed = [(0, k)], 0
        while heap:
            d, u = heapq.heappop(heap)
            for v, w in adj[u]:
                relaxed += 1
                if d + w < t[v]:
                    t[v] = d + w
                    heapq.heappush(heap, (d + w, v))
        return max(t[1:]), relaxed

    def with_skip(n, edges, k):
        ev = q0067.dijkstra_trace(n, edges, k)
        return ev[-1]["ans"], sum(1 for e in ev if e["kind"] == "relax")

    rng = random.Random(674)
    n = 12
    dense = [[u, v, rng.randint(1, 9)] for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    for k in range(1, n + 1):
        a, ra = without_skip(n, dense, k)
        b, rb = with_skip(n, dense, k)
        assert a == b and rb == 2 * len(dense) and ra >= rb


def test_trap_both_directions_in_part_c():
    assert delay_dijkstra(q0067.N, q0067.EDGES, q0067.K, directed=False) == 6
    assert delay_directed(q0067.N, q0067.EDGES, q0067.K) == -1


def test_follow_up_round_trip_and_virtual_source():
    rng = random.Random(675)
    for _ in range(300):
        n = rng.randint(1, 7)
        edges = random_graph(rng, n, rng.randint(0, 12))
        k = rng.randint(1, n)
        out = q0067.brute_times(n, edges, k, directed=True)
        back = q0067.brute_times(n, [[v, u, w] for u, v, w in edges], k, directed=True)
        # back[v] on the reversed graph is the shortest v -> k on the original graph
        for v in range(1, n + 1):
            direct = q0067.brute_times(n, edges, v, directed=True)[k - 1]
            assert back[v - 1] == direct
        # a virtual source with zero-weight links to a set of sources
        srcs = sorted(rng.sample(range(1, n + 1), rng.randint(1, n)))
        virt = edges + [[n + 1, s, 0] for s in srcs]
        want = [min(x for x in (q0067.brute_times(n, edges, s, directed=True)[v - 1] for s in srcs) if x is not None)
                if any(q0067.brute_times(n, edges, s, directed=True)[v - 1] is not None for s in srcs) else None for v in range(1, n + 1)]
        assert q0067.brute_times(n + 1, virt, n + 1, directed=True)[:n] == want
        assert all(x is None or x >= 0 for x in out)
