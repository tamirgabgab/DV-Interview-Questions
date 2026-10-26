"""Question 0048 has no code on the page; these tests check its numbers with exact
arithmetic, the reflection answer against a search over the two stops, the inverse of part
b with its conditions, the explorer's math (docs/javascripts/explorer/farm.js) against the
generator, and the page copies of the generated blocks."""

import math
import random
import sys
from fractions import Fraction as Fr

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0048  # noqa: E402


def search(L, H, a, b, n=400):
    """The shortest path by a search over the two stops (food at p1, water at p2), refined
    twice around the best grid point."""
    lo1, hi1, lo2, hi2 = 0.0, float(L), 0.0, float(L)
    best = None
    for _ in range(3):
        for i in range(n + 1):
            p1 = lo1 + (hi1 - lo1) * i / n
            for j in range(n + 1):
                p2 = lo2 + (hi2 - lo2) * j / n
                v = q0048.length(L, H, a, b, p1, p2)
                if best is None or v < best[0]:
                    best = (v, p1, p2)
        _, p1, p2 = best
        s1, s2 = (hi1 - lo1) / n * 4, (hi2 - lo2) / n * 4
        lo1, hi1, lo2, hi2 = max(0, p1 - s1), min(L, p1 + s1), max(0, p2 - s2), min(L, p2 + s2)
    return best


def test_part_a():
    for L, H in ((7, 3), (1, 1), (Fr(5, 2), 6), (20, 10)):
        s = q0048.shortest(L, H, Fr(H) / 3, Fr(2 * H) / 3)
        assert s["D"] == Fr(7 * H, 3)
        assert (s["x"], s["y"], s["w"]) == (Fr(2 * L, 7), Fr(3 * L, 7), Fr(2 * L, 7))
        assert s["x"] + s["y"] + s["w"] == L
        assert math.isclose(s["z"], math.sqrt(L ** 2 + 49 * Fr(H) ** 2 / 9))
        # the table: z1, z2, z3 are 2/7, 3/7 and 2/7 of z, and add up to it
        for zi, k in zip((s["z1"], s["z2"], s["z3"]), (2, 3, 2)):
            assert math.isclose(zi, k * s["z"] / 7)
    # the numbers of the example: L = 7, H = 3, a = 1, b = 2
    s = q0048.shortest(7, 3, 1, 2)
    assert (s["D"], s["x"], s["y"], s["w"]) == (7, 2, 3, 2) and math.isclose(s["z"], math.sqrt(98))
    assert f"{s['z']:.1f}" == "9.9"


def test_reflection_is_the_minimum():
    rng = random.Random(48)
    cases = [(7, 3, 1, 2), (7, 3, 0, 3), (7, 3, 3, 0), (7, 3, 0, 0), (2, 5, 2.5, 1)]
    cases += [(rng.uniform(1, 10), h, rng.uniform(0, h), rng.uniform(0, h)) for h in (1, 3, 6) for _ in range(3)]
    for L, H, a, b in cases:
        s = q0048.shortest(Fr(L), Fr(H), Fr(a), Fr(b))
        best, p1, p2 = search(L, H, a, b, n=120)
        assert best >= s["z"] - 1e-9, (L, H, a, b)
        assert math.isclose(best, s["z"], abs_tol=1e-6), (L, H, a, b)
        assert abs(p1 - float(s["x"])) < 1e-2 and abs(p2 - float(s["x"] + s["y"])) < 1e-2, (L, H, a, b)
        # the reflection formula is the length of the path through its stops
        assert math.isclose(q0048.length(L, H, a, b, float(s["x"]), float(s["x"] + s["y"])), s["z"])


def test_part_b():
    for L, H in ((7, 3), (3, 1), (Fr(9, 2), 10)):
        L, H = Fr(L), Fr(H)
        assert q0048.heights(L, H, L / 3, L / 3) == (0, H)
        s = q0048.shortest(L, H, 0, H)
        assert (s["D"], s["x"], s["y"], s["w"]) == (3 * H, L / 3, L / 3, L / 3)
    # the inverse undoes part a for every pair of heights
    rng = random.Random(7)
    for _ in range(200):
        L, H = Fr(rng.randint(1, 40), 2), Fr(rng.randint(1, 20), 2)
        a, b = H * Fr(rng.randint(0, 20), 20), H * Fr(rng.randint(0, 20), 20)
        s = q0048.shortest(L, H, a, b)
        assert q0048.heights(L, H, s["x"], s["y"]) == (a, b)
        assert s["x"] <= s["y"] and s["w"] <= s["y"]          # the conditions hold on every answer
    # the conditions: y the longest of the three, else no heights
    L, H = Fr(7), Fr(3)
    assert q0048.heights(L, H, 3, 2) is None                  # x > y: a < 0
    assert q0048.heights(L, H, 1, 2) is None                  # w = 4 > y: b > H
    assert q0048.heights(L, H, 2, 3) == (1, 2)
    assert q0048.heights(L, H, 0, Fr(7, 2)) == (H, H)          # x = 0 and w = y: both on the food line


def test_follow_ups():
    # water first: A -> water (a) -> food (H) -> B (H - b), so D = 2H + a - b; the better
    # order has D = 2H - |a - b|
    rng = random.Random(3)
    for _ in range(5):
        L, H = rng.uniform(1, 9), rng.uniform(1, 5)
        a, b = rng.uniform(0, H), rng.uniform(0, H)
        water_first = q0048.shortest(L, H, H - a, H - b)["z"]       # flip the picture upside down
        assert math.isclose(water_first, math.hypot(L, 2 * H + a - b))
        assert math.isclose(min(water_first, q0048.shortest(L, H, a, b)["z"]), math.hypot(L, 2 * H - abs(a - b)))


def test_explorer_matches_python():
    from page_tests import explorer_require, node_json

    rng = random.Random(21)
    cases = [(7, 3, 1, 2), (7, 3, 0, 3), (0.5, 10, 10, 0), (20, 0.5, 0.25, 0.5)]
    cases += [(rng.uniform(0.5, 20), h, rng.uniform(0, h), rng.uniform(0, h)) for h in (0.5, 2, 7, 10) for _ in range(10)]
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify(cases.map(([L, H, a, b]) => { const s = m.farmShortest(L, H, a, b);"
                    " return { s, back: m.farmHeights(L, H, s.x, s.y),"
                    " food: m.farmStopRange(L, s.x, s.x + s.y, 'food'), water: m.farmStopRange(L, s.x, s.x + s.y, 'water') }; })));")
    for (L, H, a, b), r in zip(cases, got):
        s = q0048.shortest(Fr(L), Fr(H), Fr(a), Fr(b))
        for k in ("x", "y", "w", "D"):
            assert math.isclose(r["s"][k], float(s[k]), abs_tol=1e-9), (L, H, a, b, k)
        for k in ("z1", "z2", "z3", "z"):
            assert math.isclose(r["s"][k], s[k], abs_tol=1e-9), (L, H, a, b, k)
        assert math.isclose(r["back"][0], a, abs_tol=1e-9) and math.isclose(r["back"][1], b, abs_tol=1e-9)
        # the ends of the drag ranges are the edges of part b's conditions
        p1, p2 = float(s["x"]), float(s["x"] + s["y"])
        fhi, (wlo, whi) = r["food"][1], r["water"]
        assert fhi >= p1 - 1e-9 and wlo <= p2 + 1e-9 and math.isclose(whi, L)
        edge = lambda x, y: math.isclose(H * (1 - x / y), 0, abs_tol=1e-9) or math.isclose(H * (L - x - y) / y, H)
        assert edge(fhi, p2 - fhi), (L, H, a, b)                   # the food stop stops where a = 0 or b = H
        assert edge(p1, wlo - p1), (L, H, a, b)                    # and so does the water stop
    out = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify([m.farmHeights(7, 3, 3, 2), m.farmHeights(7, 3, 1, 2)]));")
    assert out == [None, None]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(48)
