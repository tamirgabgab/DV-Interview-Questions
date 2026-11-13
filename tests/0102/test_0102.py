"""Question 0102, topological sort: the references of tools/figures/q0102.py against brute
force (every order, the closure, every path), the generated blocks, and the box's models
(docs/javascripts/explorer/toposort.js) under Node against the same references: the Kahn
events step by step, the cycle it reports, the critical path, the parsing of the fields and
the ready graphs."""

import json
import random
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0102  # noqa: E402

N, EDGES, CYCLE, DUR = q0102.N, q0102.EDGES, q0102.CYCLE_EDGES, q0102.DUR


def random_graph(rng, n, m):
    return [[rng.randrange(n), rng.randrange(n)] for _ in range(m)]


def test_references():
    rng = random.Random(10210)
    for _ in range(300):
        n = rng.randint(1, 7)
        edges = random_graph(rng, n, rng.randint(0, 2 * n))
        if rng.random() < 0.5:
            edges = [[a, b] for a, b in edges if a < b]
        orders = q0102.all_orders(n, edges)
        assert (not orders) == q0102.has_cycle(n, edges)
        assert all(q0102.valid(n, edges, o) for o in orders)
        end = q0102.kahn_events(n, edges)[-1]
        assert bool(end["left"]) == q0102.has_cycle(n, edges)
        if end["left"]:
            assert q0102.is_cycle(edges, end["cycle"]) and set(end["cycle"]) <= set(end["left"])
            color, path, hit = q0102.dfs_back(n, edges)
            u, v = hit
            assert path[-1] == u and v in path and q0102.is_cycle(edges, path[path.index(v):])
        else:
            assert tuple(end["order"]) in orders
            assert sum(len(lv) for lv in q0102.levels(n, edges)) == n
            d, f, exits = q0102.dfs_times(n, edges)
            assert tuple(exits[::-1]) in orders
            dur = [rng.randint(0, 9) for _ in range(n)]
            es, ef, late, slack, total = q0102.times(n, edges, dur)
            assert total == q0102.longest(n, edges, dur) and min(slack) >= 0


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(102)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(10211)
    cases = [(N, EDGES, DUR), (N, CYCLE, DUR), (4, q0102.DIAMOND, [2, 3, 1, 2]), (3, [[0, 1], [1, 1], [1, 2]], [2, 2, 2]), (5, [], [3, 1, 4, 1, 5]),
             (3, [[0, 1], [0, 1], [1, 2]], [1, 2, 3])]
    for _ in range(200):
        n = rng.randint(2, 8)
        edges = random_graph(rng, n, rng.randint(0, 2 * n))
        if rng.random() < 0.6:
            edges = [[a, b] for a, b in edges if a < b]
        cases.append((n, edges, [rng.randint(0, 9) for _ in range(n)]))
    cases = [(n, [list(e) for e in E], d) for n, E, d in cases]
    texts = ["A>B, A>C, E>C, B>D, C>D, D>F, F>G", "a>b>c d->a", "A>B,,B>B;C>A", "", "A>H", "A>", "AB", "A>B>", "x>y",
             ", ".join(["A>B"] * 25)]
    durs = ["3, 2, 4, 1, 5, 1, 4", "3 2 4 1 5 1", "3,2,4,1,5,1,100", "1, 2, x, 4, 5, 6, 7", "0,0,0,0,0,0,0"]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = {json.dumps(cases)};
      const P = m.tsPresets();
      console.log(JSON.stringify([C.map(([n, E, d]) => m.tsKahn(n, E, d)),
        C.map(([n, E, d]) => {{ const end = m.tsKahn(n, E, d).slice(-1)[0]; return end.cycle ? null : m.tsCritPath(n, E, d, end); }}),
        {json.dumps(texts)}.map((t) => m.tsParse(t, 7)), {json.dumps(durs)}.map((t) => m.tsParseDur(t, 7)),
        Object.fromEntries(Object.entries(P).filter(([, p]) => p.n).map(([k, p]) => [k, [p.n, p.edges, p.dur, m.tsPreset(p.n, p.edges)]])),
        m.tsFormat([[0, 1], [4, 2]]), m.tsPreset(7, [[0, 1]]), C.map(([n, E]) => m.tsLayout(n, E))]));""")
    events, paths, parsed, pdurs, presets, fmt, other, layouts = got
    keys = ("kind", "u", "v", "i", "zero", "indeg", "q", "order", "start", "left", "cycle", "total", "slack", "late")
    norm = lambda ev: [tuple(json.dumps(e.get(k)) for k in keys) for e in ev]   # noqa: E731
    for (n, edges, dur), ev in zip(cases, events):
        ref = q0102.kahn_events(n, [tuple(e) for e in edges], dur)
        for e in ref:
            e.setdefault("late", None) if e["kind"] == "done" else None
        assert norm(ev) == norm(ref), (n, edges, dur)
    # the critical path: a chain of edges with no slack, no gap between them, from 0 to the total
    for (n, edges, dur), path in zip(cases, paths):
        if path is None:
            assert q0102.has_cycle(n, edges)
            continue
        es, ef, late, slack, total = q0102.times(n, [tuple(e) for e in edges], dur)
        if n and total > 0:
            assert path and es[path[0]] == 0 and ef[path[-1]] == total
            assert all(slack[v] == 0 for v in path)
            assert all([a, b] in edges and ef[a] == es[b] for a, b in zip(path, path[1:]))
    # the fields: chains, any separator, lower case, the letters within n, at most 24 edges
    assert parsed[0] == {"edges": [list(e) for e in EDGES]}
    assert parsed[1] == {"edges": [[0, 1], [1, 2], [3, 0]]} and parsed[2] == {"edges": [[0, 1], [1, 1], [2, 0]]}
    assert parsed[3] == {"edges": []}
    assert [p.get("err") for p in parsed[4:9]] == ["A>H", "A>", "AB", "A>B>", "x>y"] and parsed[9] == {"err": None, "many": True}
    assert pdurs == [DUR, None, None, None, [0] * 7]
    # the ready graphs: the page's example and its cycle, each found again by its edges
    assert presets["example"] == [N, [list(e) for e in EDGES], DUR, "example"]
    assert presets["cycle"][:3] == [N, [list(e) for e in CYCLE], DUR] and presets["cycle"][3] == "cycle"
    assert presets["diamond"][1] == [list(e) for e in q0102.DIAMOND]
    assert all(p[3] == k for k, p in presets.items())
    assert q0102.has_cycle(3, [tuple(e) for e in presets["loop"][1]]) and presets["free"][1] == []
    assert fmt == "A>B, E>C" and other == "custom"
    # the steps the page names: 15 steps on the example, the queue empty after A and B with the cycle
    assert len(events[0]) == 15 and events[1][-1]["order"] == [0, 1] and events[1][-1]["cycle"] == [2, 3, 4]
    assert paths[0] == [4, 2, 3, 5, 6]
    # the layout: the back edges of a DFS set aside leave no cycle, each of them closes one
    # (or is a self loop), every other edge goes to a later column; the example by its rounds
    for (n, edges, dur), lay in zip(cases, layouts):
        back = set(lay["back"])
        rest = [tuple(e) for i, e in enumerate(edges) if i not in back]
        assert not q0102.has_cycle(n, rest)
        reach = q0102.closure(n, rest)
        assert all(edges[i][0] == edges[i][1] or reach[edges[i][1]][edges[i][0]] for i in back)
        assert bool(back) == q0102.has_cycle(n, [tuple(e) for e in edges])
        assert all(lay["rank"][b] > lay["rank"][a] for a, b in rest)
        assert sorted(v for col in lay["cols"] for v in col) == list(range(n))
    assert layouts[0]["cols"] == q0102.levels(N, EDGES)
    # the page's task in part c: A takes 6, the critical path moves to A C D F G, the total to 16
    d2 = DUR[:]
    d2[0] = 6
    es, ef, late, slack, total = q0102.times(N, EDGES, d2)
    assert total == 16 and [v for v in range(N) if slack[v] == 0] == [0, 2, 3, 5, 6] and slack[4] == 1
