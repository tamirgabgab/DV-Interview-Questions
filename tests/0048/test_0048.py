"""Question 0048: the numbers of parts a and b with exact arithmetic, the reflection answer
against a search over the two stops, the inverse of part b with its conditions; part c (the
tilted food line): the page's tilted_path against the generator and against a search over
the two stops on thousands of random cases, exact checks at angles with rational cos and sin
(the stops on their lines, the unfolded legs on one straight line, the rotation about O),
the reduction to part a at theta = 0, the validity condition, the follow-ups (converging
lines, theta above 60, a fence at x = 0); the explorer's math (farm.js) against the
generator, and the page copies of the generated blocks."""

import math
import random
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0048  # noqa: E402

tilted_path = load_python(48)["tilted_path"]


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


def gold(f, lo, hi, n=70):
    """The minimum of a convex function on [lo, hi] by golden-section search: (argmin, min)."""
    g = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
    f1, f2 = f(x1), f(x2)
    for _ in range(n):
        if f1 < f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - g * (hi - lo)
            f1 = f(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + g * (hi - lo)
            f2 = f(x2)
    return (lo + hi) / 2, min(f1, f2)


def tilted_search(L, H, a, b, theta, s_lo=None, q_lo=None, s_hi=None, q_hi=None):
    """The shortest tilted path by a search over the food stop (its distance s from (0, H)
    along the food line) and the water stop (qx, 0). The length is convex in (s, qx), and so is
    its minimum over qx as a function of s: two nested golden-section searches find it. The
    default range is the whole rays from O, where the lines meet (or wide, at theta = 0)."""
    t, R = math.radians(theta), 20 * (L + H)
    if s_lo is None:
        s_lo = -H / math.sin(t) if theta > 0 else -R
    if q_lo is None:
        q_lo = -H / math.tan(t) if theta > 0 else -R
    s_hi, q_hi = R if s_hi is None else s_hi, R if q_hi is None else q_hi
    inner = lambda s: gold(lambda q: q0048.tilted_length(L, H, a, b, theta, s, q), q_lo, q_hi)
    s, _ = gold(lambda s: inner(s)[1], s_lo, s_hi)
    q, v = inner(s)
    return v, s, q


def random_tilted(rng, lo=0, hi=60):
    L, H, th = rng.uniform(0.5, 20), rng.uniform(0.5, 10), rng.uniform(lo, hi)
    return L, H, rng.uniform(0, H), rng.uniform(0, H + L * math.tan(math.radians(th))), th


def test_part_c_example():
    r = q0048.tilted(7, 3, 1, 2, 15)
    s3 = math.sqrt(3)
    assert math.isclose(r["z_sq"], 92 + 10 * s3) and f"{r['z']:.3f}" == "10.456"
    assert math.isclose(r["B2"][0], (7 * s3 - 5) / 2) and math.isclose(r["B2"][1], (13 + 5 * s3) / 2)
    assert math.isclose(r["sf"], 2 * (7 * s3 - 5) / (7 * math.sqrt(6)))
    assert (f"{r['sf']:.3f}", f"{r['P'][0]:.2f}", f"{r['P'][1]:.2f}", f"{r['Q'][0]:.2f}") == ("0.831", "0.80", "3.22", "4.62")
    assert math.isclose(r["O"][0], -3 * (2 + s3))
    assert (f"{r['O'][0]:.2f}", f"{r['alpha']:.2f}", f"{r['beta']:.2f}", f"{r['turn']:.2f}") == ("-11.20", "5.10", "6.27", "31.17")
    assert (f"{r['z1']:.3f}", f"{r['z2']:.3f}", f"{r['z3']:.3f}") == ("2.356", "4.993", "3.106")
    assert math.isclose(r["z1"] + r["z2"] + r["z3"], r["z"])
    assert f"{math.sqrt(98):.2f}" == "9.90"                                    # part a, for the comparison
    # the food stop is left of A from tan 2 theta = L / (H + b): 27.2 degrees; at 30, x = -0.15
    assert f"{math.degrees(math.atan(7 / 5)) / 2:.1f}" == "27.2"
    assert f"{q0048.tilted(7, 3, 1, 2, 30)['P'][0]:.2f}" == "-0.15"
    # the self-check: theta = 45, B2 = (-5, 10), z^2 = 106
    r = q0048.tilted(7, 3, 1, 2, 45)
    assert math.isclose(r["B2"][0], -5) and math.isclose(r["B2"][1], 10) and math.isclose(r["z_sq"], 106)
    assert f"{r['z']:.2f}" == "10.30"
    # the page's code gives the same numbers
    z, food, water = tilted_path(7, 3, 1, 2, 15)
    assert math.isclose(z, 10.455644794831585) and math.isclose(food[0], 0.8026860219310012) and math.isclose(water[0], 4.6233096782319105)


PYTH = [(Fr(1), Fr(0)), (Fr(24, 25), Fr(7, 25)), (Fr(12, 13), Fr(5, 13)), (Fr(35, 37), Fr(12, 37)), (Fr(15, 17), Fr(8, 17)),
        (Fr(4, 5), Fr(3, 5)), (Fr(21, 29), Fr(20, 29)), (Fr(20, 29), Fr(21, 29)), (Fr(3, 5), Fr(4, 5))]


def test_part_c_exact():
    """At angles with rational cos and sin (and theta = 0) every claim holds exactly."""
    rng = random.Random(4801)
    cross = lambda o, p, q: (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    for c, s in PYTH:
        assert c * c + s * s == 1 and math.degrees(math.atan2(s, c)) <= 60
        for _ in range(40):
            L, H = Fr(rng.randint(1, 60), 4), Fr(rng.randint(1, 40), 4)
            a = H * Fr(rng.randint(0, 12), 12)
            b = (H + L * s / c) * Fr(rng.randint(0, 12), 12)
            r = q0048.tilted_cs(L, H, a, b, c, s)
            A, B, P, Q, Qs, B1, B2 = (0, a), (L, b), r["P"], r["Q"], r["Qs"], r["B1"], r["B2"]
            assert (P[1] - H) * c == P[0] * s and Q[1] == 0                   # the stops on their lines
            assert cross(A, P, B2) == 0 and cross(A, Qs, B2) == 0              # the unfolded legs on one line
            assert cross(P, Q, B1) == 0                                        # folded once: P, Q, B1 in line
            d = lambda p, q: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
            assert d(Q, B) == d(Q, B1) and d(P, Q) == d(P, Qs) and d(Qs, B2) == d(Q, B1)
            u, v = H + b, H - a
            c2, s2 = c * c - s * s, 2 * c * s
            assert r["z_sq"] == d(A, B2) == L ** 2 + u ** 2 + v ** 2 + 2 * v * (L * s2 + u * c2)
            # B2 is B rotated by 2 theta about O (a translation by 2H at theta = 0)
            if s == 0:
                assert B2 == (L, 2 * H + b)
                part_a = q0048.shortest(L, H, a, b)
                assert r["z_sq"] == L ** 2 + part_a["D"] ** 2
                assert P == (part_a["x"], H) and Q[0] == part_a["x"] + part_a["y"]
            else:
                O = (-H * c / s, 0)
                rel = (B[0] - O[0], B[1])
                assert B2 == (O[0] + c2 * rel[0] - s2 * rel[1], s2 * rel[0] + c2 * rel[1])
            # the order along the straight line: A, P, Qs, B2 (the parameters grow)
            par = lambda p: ((p[0] - A[0]) * (B2[0] - A[0]) + (p[1] - A[1]) * (B2[1] - A[1])) / r["z_sq"]
            assert 0 <= par(P) <= par(Qs) <= 1
            # the perpendicular distances of A and B1 from the food line
            dist = lambda p: (p[1] - H) * c - p[0] * s                         # signed, up is positive
            assert dist(A) == -v * c and dist(B1) == -(L * s + u * c) and dist(B2) == L * s + u * c


def test_part_c_is_the_minimum():
    rng = random.Random(4802)
    cases = [(7, 3, 1, 2, 15), (7, 3, 1, 2, 0), (7, 3, 0, 3 + 7 * math.sqrt(3), 60), (7, 3, 3, 0, 60), (7, 3, 1, 2, 30)]
    cases += [random_tilted(rng) for _ in range(1500)]
    for L, H, a, b, th in cases:
        r = q0048.tilted(L, H, a, b, th)
        z, food, water = tilted_path(L, H, a, b, th)
        assert math.isclose(z, r["z"]) and math.isclose(food[0], r["P"][0], abs_tol=1e-9) and math.isclose(water[0], r["Q"][0], abs_tol=1e-9)
        assert math.isclose(r["z1"] + r["z2"] + r["z3"], z, rel_tol=1e-9)    # the stops reach the lower bound
        assert r["turn"] <= 180 + 1e-9                                         # the condition holds for every theta <= 60
        best, s, q = tilted_search(L, H, a, b, th)
        assert best >= z - 1e-7 * z and math.isclose(best, z, rel_tol=1e-9), (L, H, a, b, th, best, z)
        assert abs(s - r["sf"]) < 1e-4 * (L + H) and abs(q - r["Q"][0]) < 1e-4 * (L + H), (L, H, a, b, th)
    # the extreme case: theta = 60, A on the water line, B on the food line: the path goes through O
    L, H = 7, 3
    r = q0048.tilted(L, H, 0, H + L * math.sqrt(3), 60)
    assert math.isclose(r["turn"], 180) and math.isclose(r["P"][0], r["O"][0]) and math.isclose(r["P"][1], 0, abs_tol=1e-9)
    assert math.isclose(r["z"], math.dist(r["O"], (0, 0)) + math.dist(r["O"], (L, H + L * math.sqrt(3))))


def test_part_c_traps():
    L, H, a, b, th = 7, 3, 1, 2, 15
    z = q0048.tilted(L, H, a, b, th)["z"]
    # the wrong order (food line first, then water) is the rotation by -2 theta: a longer line
    t = math.radians(th)
    wrong = q0048.reflect(q0048.reflect((L, b), (0, H), math.cos(t), math.sin(t)), (0, 0), 1, 0)
    assert math.dist((0, a), wrong) != z
    # the vertical reflection of B1 through the food line's height at x = L
    vert = (L, 2 * (H + L * math.tan(t)) + b)
    assert abs(math.dist((0, a), vert) - z) > 0.5
    # degrees taken as radians: cos(15 radians) is about -0.76, cos(15 degrees) about 0.97
    assert math.cos(15) < 0 < math.cos(math.radians(15))


def test_part_c_follow_ups():
    rng = random.Random(4803)
    # converging lines: the same formulas with theta < 0, while the lines meet beyond the cow
    for _ in range(150):
        L, H = rng.uniform(0.5, 20), rng.uniform(0.5, 10)
        th = -rng.uniform(0, min(60, math.degrees(math.atan(H / L)) * 0.999))
        a, b = rng.uniform(0, H), rng.uniform(0, H + L * math.tan(math.radians(th)))
        z = q0048.tilted(L, H, a, b, th)["z"]
        t = math.radians(-th)
        best = tilted_search(L, H, a, b, th, s_lo=-20 * (L + H), q_lo=-20 * (L + H), s_hi=H / math.sin(t) if th else None,
                             q_hi=H / math.tan(t) if th else None)[0]
        assert math.isclose(best, z, rel_tol=1e-9), (L, H, a, b, th)
    # theta above 60: the reflection when the turn is at most 180, else the path through O
    apex = 0
    for _ in range(150):
        L, H, a, b, th = random_tilted(rng, 60, 89)
        r = q0048.tilted(L, H, a, b, th)
        via_o = math.dist(r["O"], (0, a)) + math.dist(r["O"], (L, b))
        want = r["z"] if r["turn"] <= 180 else via_o
        apex += r["turn"] > 180
        assert math.isclose(tilted_search(L, H, a, b, th)[0], want, rel_tol=1e-9), (L, H, a, b, th)
    assert apex > 10
    # a fence at x = 0: food at (0, H) when the free food stop is left of it
    left = 0
    for _ in range(150):
        L, H, a, b, th = random_tilted(rng)
        r = q0048.tilted(L, H, a, b, th)
        want = r["z"] if r["sf"] >= 0 else (H - a) + math.hypot(L, H + b)
        left += r["sf"] < 0
        assert math.isclose(tilted_search(L, H, a, b, th, s_lo=0, q_lo=0)[0], want, rel_tol=1e-9), (L, H, a, b, th)
    assert left > 20


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


def test_explorer_tilted_matches_python():
    from page_tests import explorer_require, node_json

    rng = random.Random(22)
    cases = [(7, 3, 1, 2, 15), (7, 3, 1, 2, 0), (7, 3, 0, 3 + 7 * math.sqrt(3), 60), (0.5, 10, 10, 0, 60)]
    cases += [random_tilted(rng) for _ in range(60)]
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify(cases.map(([L, H, a, b, t]) => m.farmTilt(L, H, a, b, t))));")
    for (L, H, a, b, th), r in zip(cases, got):
        w = q0048.tilted(L, H, a, b, th)
        for k in ("z", "z1", "z2", "z3", "sf", "alpha", "beta", "turn"):
            assert math.isclose(r[k], w[k], rel_tol=1e-9, abs_tol=1e-9), (L, H, a, b, th, k)
        for k in ("B1", "B2", "P", "Q", "Qs"):
            assert all(math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-9) for x, y in zip(r[k], w[k])), (L, H, a, b, th, k)
        assert (r["O"] is None) == (w["O"] is None)
        if w["O"]:
            assert math.isclose(r["O"][0], w["O"][0])


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(48)
