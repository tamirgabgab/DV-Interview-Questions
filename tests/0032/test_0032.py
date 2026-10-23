"""Question 0032: the plan and its two mirror solutions, the ten safe states, the tables,
the explorer's JavaScript against the generator, and the page copies of the blocks."""

import sys
from itertools import product

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0032  # noqa: E402


def safe_by_words(f, w, g, c):
    """The rule in words: the wolf eats the goat and the goat eats the cabbage when the farmer is away."""
    eaten = (w == g != f) or (g == c != f)
    return not eaten


def test_safe_states():
    for f, w, g, c in product((0, 1), repeat=4):
        s = f * 1 + w * 2 + g * 4 + c * 8
        assert q0032.safe(s) == safe_by_words(f, w, g, c), (f, w, g, c)
    assert sum(q0032.safe(s) for s in range(16)) == 10
    rows = q0032.states_table().splitlines()[2:]
    assert len(rows) == 16 and sum("| כן |" in r for r in rows) == 10


def test_plan_and_solutions():
    plan = q0032.solve()
    assert plan == ["goat", None, "wolf", "goat", "cabbage", None, "goat"]
    assert q0032.replay(plan) == [0, 5, 4, 7, 2, 11, 10, 15]
    sols = q0032.all_solutions()
    assert sorted(map(str, sols)) == sorted(map(str, [plan, ["goat", None, "cabbage", "goat", "wolf", None, "goat"]]))
    assert q0032.all_solutions(6) == []                      # nothing shorter
    assert q0032.replay(["wolf"]) is None and q0032.replay(["goat", "goat"]) is None
    rows = q0032.plan_table().splitlines()[2:]
    assert len(rows) == 7 and rows[-1].endswith("| ‏– | ‏FWGC |")


def test_explorer_matches_generator():
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "console.log(JSON.stringify({ plan: m.riverPlan(), safe: [...Array(16).keys()].map(m.riverSafe),"
                    " moves: [...Array(16).keys()].map((s) => m.riverMoves(s)) }));")
    assert got["plan"] == [None if p is None else p for p in q0032.solve()]
    assert got["safe"] == [q0032.safe(s) for s in range(16)]
    for s in range(16):
        assert sorted(got["moves"][s], key=str) == sorted([[i, t] for i, t in q0032.moves(s)], key=str), s


def test_explorer_bfs_layers():
    """The proof panel of the box: the BFS layers from the start with every parent one layer
    up, against a plain Python BFS over the generator's moves; the goal is in layer 7 and the
    parents give exactly the page's two mirror plans."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify(m.riverLayers()));")
    depth, layers = {0: 0}, [[0]]
    while True:
        nxt = []
        for s in layers[-1]:
            for _, t in q0032.moves(s):
                if q0032.safe(t) and t not in depth:
                    depth[t] = len(layers)
                    nxt.append(t)
        if not nxt:
            break
        layers.append(nxt)
    assert [sorted(layer) for layer in got["layers"]] == [sorted(layer) for layer in layers]
    assert {int(k): v for k, v in got["depth"].items()} == depth and depth[15] == 7
    for t, ps in got["parents"].items():
        t = int(t)
        want = [[i, s] for s in depth for i, u in q0032.moves(s) if u == t and depth[s] == depth[t] - 1]
        assert sorted([[i, p] for p, i in ps], key=str) == sorted(want, key=str), t

    def plans(t):
        if t == 0:
            return [[]]
        return [plan + [item] for p, item in got["parents"][str(t)] for plan in plans(p)]

    assert sorted(map(str, plans(15))) == sorted(map(str, q0032.all_solutions()))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(32)
