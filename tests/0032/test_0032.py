"""Question 0032: the plan and its two mirror solutions, the ten safe states and the table
of the six forbidden ones, the stepper's captions, the explorer's JavaScript against the
generator, and the page copies of the blocks."""

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
    rows = q0032.forbidden_table().splitlines()[2:]
    unsafe = [s for s in range(16) if not q0032.safe(s)]
    assert len(rows) == 6 == len(unsafe)
    for row, s in zip(rows, unsafe):
        assert row.startswith(f"| \u200f{q0032.bank_text(s, 0)} | \u200f{q0032.bank_text(s, 1)} |"), row
        f, w, g, c = (s >> k & 1 for k in range(4))
        assert ("הזאב אוכל את העז" in row) == (w == g != f) and ("את הכרוב" in row) == (g == c != f), row


def test_plan_and_solutions():
    plan = q0032.solve()
    assert plan == ["goat", None, "wolf", "goat", "cabbage", None, "goat"]
    assert q0032.replay(plan) == [0, 5, 4, 7, 2, 11, 10, 15]
    sols = q0032.all_solutions()
    assert sorted(map(str, sols)) == sorted(map(str, [plan, ["goat", None, "cabbage", "goat", "wolf", None, "goat"]]))
    assert q0032.all_solutions(6) == []                      # nothing shorter
    assert q0032.replay(["wolf"]) is None and q0032.replay(["goat", "goat"]) is None
    # the stepper's captions name both banks after every crossing (the plan table merged in)
    import re
    caps = re.findall(r"<figcaption>(.*?)</figcaption>", q0032.crossing_stepper())
    states = q0032.replay(plan)
    assert len(caps) == 9
    for cap, s in zip(caps[1:8], states[1:]):
        near, far = q0032.bank_text(s, 0), q0032.bank_text(s, 1)
        assert (f"על הגדה הקרובה {near}," if near != "–" else "הגדה הקרובה ריקה,") in cap and cap.endswith(f"על הרחוקה {far}."), cap


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


def test_steps_light_the_right_parts():
    """The state graph beside part b's steps: every key a step lights is in the figure; the
    expansion step lights the start, its four crossings' states and the one safe crossing;
    the path step walks part a's plan, and the step before it walks it backwards."""
    from page_tests import fig_steps, lit

    ((plan, keys),) = fig_steps(32)
    assert lit(plan) <= keys, lit(plan) - keys
    assert plan[0] == "n0" and plan[1] == "n15"
    near = [t for _, t in q0032.moves(0)]
    assert set(plan[2].split()) == {"n0"} | {f"n{t}" for t in near} | {f"e0-{t}" for t in near if q0032.safe(t)}
    states = q0032.replay(["goat", None, "wolf", "goat", "cabbage", None, "goat"])
    fwd = ["n0"] + [f"e{min(a, b)}-{max(a, b)} n{b}" for a, b in zip(states, states[1:])]
    assert plan[4].split(">") == fwd
    back = states[::-1]
    assert plan[3].split(">") == ["n15"] + [f"e{min(a, b)}-{max(a, b)} n{b}" for a, b in zip(back, back[1:])]
    mirror = q0032.replay(["goat", None, "cabbage", "goat", "wolf", None, "goat"])
    assert len(plan) == 6 and plan[5].split(">") == ["n0"] + [f"e{min(a, b)}-{max(a, b)} n{b}" for a, b in zip(mirror, mirror[1:])]
    # step 6's text: the mirror leaves the plan after crossing 2 and meets it again after crossing 5
    assert states[:3] == mirror[:3] and states[5:] == mirror[5:] and states[3:5] != mirror[3:5]
    assert [q0032.bank_text(s, 0) + " | " + q0032.bank_text(s, 1) for s in mirror[3:5]] == ["W | FGC", "FWG | C"]
    assert [q0032.bank_text(s, 0) + " | " + q0032.bank_text(s, 1) for s in states[3:5]] == ["C | FWG", "FGC | W"]


def test_box_task():
    """The box paragraph: the wolf first is refused; at C | FWG (after G, alone, W) going
    alone is unsafe, the wolf back undoes crossing 3, and the goat back is the only safe
    move forward."""
    assert not q0032.safe(dict(q0032.moves(0))["wolf"])
    s = q0032.replay(["goat", None, "wolf", "goat", "cabbage", None, "goat"])[3]
    assert (q0032.bank_text(s, 0), q0032.bank_text(s, 1)) == ("C", "FWG")
    moves = dict(q0032.moves(s))
    assert set(moves) == {None, "wolf", "goat"} and not q0032.safe(moves[None])
    assert moves["wolf"] == 4 and q0032.safe(moves["wolf"]) and q0032.safe(moves["goat"]) and moves["goat"] == 2
