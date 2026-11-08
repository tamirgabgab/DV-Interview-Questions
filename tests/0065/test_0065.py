"""Question 0065: the generator's references against the page code, the explorer's
JavaScript (the frames of the islands flood) against the generator's trace, the extra example
grids, and the page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0065  # noqa: E402

ns = load_python(65)


def random_grid(rng, m, n, p):
    return ["".join("1" if rng.random() < p else "0" for _ in range(n)) for _ in range(m)]


def test_generator_matches_the_page_code():
    rng = random.Random(6500)
    for _ in range(400):
        m, n = rng.randint(1, 8), rng.randint(1, 8)
        grid = random_grid(rng, m, n, rng.choice([0.3, 0.5, 0.7]))
        for diag in (False, True):
            assert q0065.sizes_brute(grid, diag) == ns["island_sizes"](grid, diag) == sorted(q0065.flood_sizes(grid, diag), reverse=True)
        assert len(q0065.components(grid)) == ns["count_islands"](grid)
        assert len(q0065.components(grid, True)) == ns["count_islands8"](grid)


def test_extra_examples():
    # part a: the X with four neighbours, five islands; part b: with eight, one
    assert ns["count_islands"](q0065.SC_GRID) == 5 and ns["count_islands8"](q0065.SC_GRID) == 1
    assert ns["island_sizes"](q0065.SC_GRID, True) == [5]
    # part c: the largest island of the extra example grid, and the cells the answer names
    assert ns["island_sizes"](q0065.SC_GRID_C) == [5, 3]
    big = max(q0065.components(q0065.SC_GRID_C), key=len)
    assert big == {(0, 3), (1, 3), (2, 3), (2, 2), (2, 1)}


def test_trap_cases():
    """The boxes' trap buttons: a U-shaped island (part a) is one island although the scan
    meets two land cells in row 0; the diagonal line (part b) is four islands with four
    neighbours and one with eight; a small island before a large one (part c) is found
    first, and only the final sort puts the large one first."""
    u, diag, small = q0065.TRAP_GRIDS["a"], q0065.TRAP_GRIDS["b"], q0065.TRAP_GRIDS["c"]
    assert ns["count_islands"](u) == 1 and u[0].count("1") == 2 and u[0][1:-1].count("1") == 0
    starts = [f for f in q0065.trace(u) if f["kind"] == "start"]
    reach = next(k for k, f in enumerate(q0065.trace(u)) if f["kind"] == "pop" and f["cell"] == [0, 4])
    assert len(starts) == 1 and reach == 9                   # the flood takes (0, 4) in step 10, last
    assert ns["count_islands"](diag) == 4 and ns["count_islands8"](diag) == 1
    assert sum(1 for f in q0065.trace(diag, True) if f["kind"] == "start") == 1
    assert q0065.flood_sizes(small) == [3, 5] and ns["island_sizes"](small) == [5, 3]
    box = (ROOT / "docs" / "javascripts" / "explorer" / "islands.js").read_text(encoding="utf-8")
    for mode, grid in q0065.TRAP_GRIDS.items():
        assert f'{mode}: {{ label: ' in box and ".".join(grid) in box


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(6501)
    cases = [(q0065.GRID, False), (q0065.GRID, True), (q0065.SC_GRID, False), (q0065.SC_GRID, True), (q0065.DIAG_GRID, True), (["0"], False), (["1"], True)]
    cases += [(random_grid(rng, rng.randint(1, 6), rng.randint(1, 7), rng.choice([0.3, 0.5, 0.8])), rng.random() < 0.5) for _ in range(30)]
    js_cases = [([[int(ch) for ch in row] for row in grid], diag) for grid, diag in cases]
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {json.dumps(js_cases)};
      console.log(JSON.stringify([cases.map(([g, d]) => m.ilTrace(g, d)), cases.map(([g, d]) => m.ilSizes(g, d)),
        m.ilParse("110000.110011.000010.000100.000100"), m.ilParse("11.1"), m.ilText([[1, 0], [0, 1]])]));""")
    for (grid, diag), frames in zip(cases, got[0]):
        ref = json.loads(json.dumps(q0065.trace(grid, diag)))          # tuples to lists
        assert frames == ref, (grid, diag)
    for (grid, diag), sizes in zip(cases, got[1]):
        assert sizes == q0065.sizes_brute(grid, diag)
    assert got[2] == [[int(ch) for ch in row] for row in q0065.GRID]
    assert got[3] is None and got[4] == "10.01"


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(65)
