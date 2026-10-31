"""Question 0067: the generator's references against the page code, the explorer's
JavaScript (the BFS and the Dijkstra of netdelay, its ready graphs and random graphs)
against the generator's traces, and the page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0067  # noqa: E402

ns = load_python(67)


def random_graph(rng, n, m):
    pairs = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
    rng.shuffle(pairs)
    return [[u, v, rng.randint(0, 9)] for u, v in pairs[:m]]


def test_generator_matches_the_page_code():
    rng = random.Random(6700)
    for _ in range(500):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.randint(0, 14))
        k = rng.randint(1, n)
        assert q0067.bfs_trace(n, [[u, v] for u, v, _ in edges], k)[-1]["ans"] == ns["delay_bfs"](n, [[u, v] for u, v, _ in edges], k)
        assert q0067.dijkstra_trace(n, edges, k)[-1]["ans"] == ns["delay_dijkstra"](n, edges, k)
        assert q0067.dijkstra_trace(n, edges, k, True)[-1]["ans"] == ns["delay_directed"](n, edges, k)
        assert q0067.answer_of(q0067.brute_times(n, edges, k, True)) == ns["delay_directed"](n, edges, k)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(6701)
    cases = [(q0067.N, q0067.EDGES, q0067.K), (4, [[1, 2, 4], [1, 3, 1], [3, 2, 1], [2, 4, 2], [3, 4, 5]], 1), (3, [[1, 2, 2]], 2), (1, [], 1)]
    cases += [(n, random_graph(rng, n, rng.randint(0, 14)), rng.randint(1, n)) for n in (rng.randint(1, 8) for _ in range(40))]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = {json.dumps(cases)};
      console.log(JSON.stringify([C.map(([n, E, k]) => m.ndBfs(n, E, k)), C.map(([n, E, k]) => m.ndDijkstra(n, E, k, false)),
        C.map(([n, E, k]) => m.ndDijkstra(n, E, k, true)),
        ["line", "ring", "tree", "dense"].map((g) => [3, 6, 8].map((n) => m.ndReady(g, n))), m.ndReady("example", 6),
        [1, 2, 3, 77, 1234].map((s) => [5, 8].map((n) => m.ndRandomGraph(m.mulberry32(s), n)))]));""")
    keys_a = ("kind", "u", "d", "v", "w", "i", "nd", "improved", "ans", "t", "q", "order")
    keys_b = ("kind", "u", "d", "v", "w", "i", "nd", "old", "improved", "ans", "t", "heap", "settled")
    norm = lambda ev, keys: [tuple(json.dumps(e.get(x)) for x in keys) for e in ev]   # noqa: E731
    for (n, edges, k), ev in zip(cases, got[0]):
        assert norm(ev, keys_a) == norm(q0067.bfs_trace(n, [[u, v] for u, v, _ in edges], k), keys_a), (n, edges, k)
    for directed, col in ((False, 1), (True, 2)):
        for (n, edges, k), ev in zip(cases, got[col]):
            ref = q0067.dijkstra_trace(n, edges, k, directed)
            assert norm(ev, keys_b) == norm([{**e, "heap": [list(h) for h in e["heap"]]} for e in ref], keys_b), (n, edges, k, directed)
    # the ready graphs: a line and a tree have n - 1 links, a ring n, a dense one n(n-1)/2;
    # every one is connected and every weight is 1..9
    for g, per_n in zip(["line", "ring", "tree", "dense"], got[3]):
        for n, edges in zip([3, 6, 8], per_n):
            want = {"line": n - 1, "ring": n, "tree": n - 1, "dense": n * (n - 1) // 2}[g]
            assert len(edges) == want and all(1 <= w <= 9 and 1 <= u <= n and 1 <= v <= n and u != v for u, v, w in edges), (g, n)
            assert q0067.answer_of(q0067.brute_times(n, edges, 1)) >= 0
    assert got[4] == q0067.EDGES
    # random graphs: distinct pairs, n - 1 to 2n - 2 of them, weights 1..9
    for per_seed in got[5]:
        for n, edges in zip([5, 8], per_seed):
            pairs = {frozenset((u, v)) for u, v, _ in edges}
            assert len(pairs) == len(edges) and n - 1 <= len(edges) <= 2 * n - 2
            assert all(1 <= w <= 9 and u != v for u, v, w in edges)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(67)
