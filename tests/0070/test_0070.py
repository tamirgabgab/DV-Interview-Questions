"""Question 0070: the generator's traces against the page code, the explorer's JavaScript
(the three searches of gridpath frame by frame, its random grids and its parser) against
the generator, and the page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0070  # noqa: E402

ns = load_python(70)


def random_case(rng, mode):
    m, n = rng.randint(4, 8), rng.randint(4, 8)
    if mode == "c":
        g = ["".join("#" if rng.random() < 0.12 else str(rng.randint(1, 9)) for _ in range(n)) for _ in range(m)]
        wall = "#"
    else:
        g = ["".join("1" if rng.random() < 0.3 else "0" for _ in range(n)) for _ in range(m)]
        wall = "1"
    cells = [(r, c) for r in range(m) for c in range(n) if g[r][c] != wall]
    if len(cells) < 2:
        return None
    s, t = rng.sample(cells, 2)
    return [mode, g, list(s), list(t), rng.random() < 0.5, rng.randint(0, 3)]


def test_generator_matches_the_page_code():
    rng = random.Random(7000)
    for _ in range(600):
        for mode in "abc":
            case = random_case(rng, mode)
            if not case:
                continue
            _, g, s, t, diag, k = case
            got = q0070.answer_of(q0070.trace(mode, g, tuple(s), tuple(t), diag, k))
            want = {"a": lambda: ns["shortest_path"](g, tuple(s), tuple(t), diag)[0],
                    "b": lambda: ns["shortest_with_breaks"](g, tuple(s), tuple(t), k, diag),
                    "c": lambda: ns["cheapest_path"](g, tuple(s), tuple(t), diag)}[mode]()
            assert got == want, case


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(7001)
    cases = [["a", q0070.GRID, list(q0070.S), list(q0070.T), d, 0] for d in (False, True)]
    cases += [["b", q0070.GRID, list(q0070.S), list(q0070.T), d, k] for d in (False, True) for k in range(4)]
    cases += [["b", q0070.CE_GRID, [0, 0], [2, 2], False, 1], ["c", q0070.COST, list(q0070.CS), list(q0070.CT), False, 0],
              ["c", q0070.COST, list(q0070.CS), list(q0070.CT), True, 0], ["a", ["010", "111", "000"], [0, 0], [2, 2], False, 0]]
    cases += [c for c in (random_case(rng, mode) for mode in "abc" for _ in range(40)) if c]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = {json.dumps(cases)};
      console.log(JSON.stringify([C.map(([mode, g, s, t, d, k]) => m.gpTrace(mode, g, s, t, d, k)),
        [1, 2, 3, 77, 1234].map((seed) => ["a", "c"].map((mode) => m.gpRandom(m.mulberry32(seed), mode, 9, 11, [3, 0], [3, 8]))),
        [m.gpParse("0000.0101.0000.0010", "a"), m.gpParse("0000.010", "a"), m.gpParse("19#1.1111.1111.1111", "c"), m.gpParse("0102.0000.0000.0000", "a"),
         m.gpParse("000.000.000", "a")]]));""")
    for case, frames in zip(cases, got[0]):
        mode, g, s, t, diag, k = case
        ref = json.loads(json.dumps(q0070.trace(mode, g, tuple(s), tuple(t), diag, k)))
        assert frames == ref, case
    for per_seed in got[1]:
        a, c = per_seed
        assert len(a) == 9 and all(len(r) == 11 and set(r) <= {"0", "1"} for r in a)
        assert a[3][0] == "0" and a[3][8] == "0"
        assert len(c) == 9 and all(set(r) <= set("123456789#") for r in c) and c[3][0] != "#" and c[3][8] != "#"
    assert got[2] == [["0000", "0101", "0000", "0010"], None, ["19#1", "1111", "1111", "1111"], None, None]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(70)
