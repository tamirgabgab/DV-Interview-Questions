"""Question 0042: every number the page states (400 km, the stops 60 and 160, the price
list, 460 for an empty arrival, 9 passes and 840 km walked, the bonus examples), the
page's segments against the closed form with exact fractions, the page's passes against
the generator's (full loads first, the partial load last) with the water balanced, a
brute-force search over the stop positions with two and three loads that never beats the
formula, the logarithmic approximation, the explorer's JavaScript, and the page copies of
the generated blocks."""

import json
import random
import sys
from fractions import Fraction as F
from math import ceil, log

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0042  # noqa: E402

ns = load_python(42)
camel_levels, camel_segments, camel_distance = ns["camel_levels"], ns["camel_segments"], ns["camel_distance"]
camel_passes, camel_check = ns["camel_passes"], ns["camel_check"]

A, C, W, T = 0.5, 150, 450, 30
CASES = [(0.5, 150, 450, 30), (0.5, 150, 450, 0), (0.5, 150, 250, 30), (0.5, 150, 150, 30), (0.5, 150, 600, 150),
         (1, 100, 1000, 0), (0.2, 300, 3000, 200), (1, 100, 1000, 50), (0.5, 150, 450, 200), (0.3, 120, 1000, 40)]


def near(x, y, tol=1e-9):
    return abs(float(x) - float(y)) < tol


def test_page_numbers():
    assert near(camel_distance(A, C, W, T), 400) and q0042.distance(F(1, 2), C, W, T) == 400
    assert [(round(x0, 9), round(x1, 9), j) for x0, x1, j in camel_segments(A, C, W, T)] == [(0, 60, 3), (60, 160, 2), (160, 400, 1)]
    assert [q0042.price(j, F(1, 2)) for j in (3, 2, 1)] == [F(5, 2), F(3, 2), F(1, 2)]
    assert near(camel_distance(A, C, W, 0), 460)                                # Phi(450): arriving empty
    passes = camel_passes(A, C, W, T)
    assert len(passes) == 9 and camel_check(A, C, W, T) == (420, 30)
    assert q0042.walked(F(1, 2), C, W, T) == 840
    # the walks of segment 1: take 150, arrive with 120, leave 90, keep 30; the third leaves everything
    assert [(p[2], p[3], p[4][1]) for p in passes[:5]] == [(150, 120, 90), (30, 0, 90), (150, 120, 180), (30, 0, 180), (150, 120, 300)]
    assert passes[4][4] == [0, 300, 0, 0] and passes[7][4] == [0, 0, 150, 0] and passes[8][4] == [0, 0, 0, 30]
    # the bonus: T > c, and the logarithmic approximation
    assert q0042.distance(F(1, 2), C, W, 200) == F(380, 3) and near(camel_segments(A, C, W, 200)[-1][1], 380 / 3, 1e-9)
    assert [round(x1, 1) for _, x1, _ in camel_segments(A, C, W, 200)] == [60, 126.7]
    assert near(q0042.approx(A, C, W, T), 399.3, 0.05) and near(q0042.APPROX_CONST, 1.9635, 1e-4)
    assert near(q0042.approx(A, C, 1500, T), 580, 0.1) and near(q0042.distance(F(1, 2), C, 1500, T), 580, 0.05)
    # the traps: 1.5 instead of 2.5 would give 440; a stop at 50 km leaves 325 litres (more than two loads)
    assert near(150 / 1.5 + 150 / 1.5 + (150 - 30) / 0.5, 440) and W - 5 * 50 * A == 325


def test_segments_match_the_closed_form():
    rng = random.Random(42)
    for a, c, w, T in CASES + [(F(rng.randint(2, 10), 10), rng.randint(10, 30) * 10, rng.randint(1, 300) * 10, rng.randint(0, 20) * 5) for _ in range(60)]:
        a, w, T = F(a), F(w), F(T)
        if w <= T:
            continue
        segs = q0042.segments(a, c, w, T)
        assert all(x1 > x0 for x0, x1, *_ in segs)
        assert q0042.levels(c, w, T) == [w] + [F(j * c) for j in range(ceil(w / c) - 1, 0, -1) if j * c > T] + [T]
        if T <= c:
            assert q0042.distance(a, c, w, T) == q0042.formula(a, c, w, T), (a, c, w, T)
        # Phi(w) - Phi(T) in every case, the bonus included
        assert q0042.distance(a, c, w, T) == q0042.range_of(a, c, w) - q0042.range_of(a, c, T)
        # the page's floats against the exact fractions
        page = camel_segments(float(a), c, float(w), float(T))
        if T <= c:
            assert near(camel_distance(float(a), c, float(w), float(T)), q0042.formula(a, c, w, T), 1e-6)
        assert near(page[-1][1], q0042.distance(a, c, w, T), 1e-6)
        assert len(page) == len(segs)
        for (x0, x1, j), (e0, e1, ej, _, _) in zip(page, segs):
            assert near(x0, e0, 1e-6) and near(x1, e1, 1e-6) and j == ej


def test_passes_balance_the_water():
    rng = random.Random(4242)
    for a, c, w, T in CASES + [(rng.randint(2, 10) / 10, rng.randint(10, 30) * 10, rng.randint(1, 300) * 10, rng.randint(0, 30) * 5) for _ in range(40)]:
        if w <= T:
            continue
        passes = camel_passes(a, c, w, T)
        burned, delivered = camel_check(a, c, w, T)
        assert near(burned + delivered, w, 1e-6) and near(delivered, T, 1e-6)
        segs = camel_segments(a, c, w, T)
        assert len(passes) == sum(2 * j - 1 for _, _, j in segs)
        exact = q0042.passes(F(a), c, w, T)
        assert len(exact) == len(passes)
        for p, e in zip(passes, exact):
            assert p[0] == e["seg"] and p[1] == e["back"]
            assert near(p[2], e["carry0"], 1e-6) and near(p[3], e["carry1"], 1e-6)
            assert all(near(u, v, 1e-6) for u, v in zip(p[4], e["depots"]))
            assert p[2] <= c + 1e-9 and p[3] >= -1e-9
        # every return trip is made by a camel that left full, and the depots end at the levels
        for p in exact:
            if p["back"]:
                assert p["carry0"] == F(a) * (q0042.segments(F(a), c, w, T)[p["seg"]][1] - q0042.segments(F(a), c, w, T)[p["seg"]][0])
        assert exact[-1]["depots"][-1] == T and all(v == 0 for v in exact[-1]["depots"][:-1])


def plan_distance(a, c, w, T, stops):
    """The farthest point with T litres when the camel stops exactly at `stops` (sorted) and
    pays the price list of the loads it has in every segment; None when a segment cannot
    be walked. A brute-force check of the stop positions, not of the price list."""
    water, x = F(w), F(0)
    for y in list(stops) + [None]:
        j = ceil(water / c)
        price = (2 * j - 1) * a
        if y is None:
            return x + (water - T) / price
        if y <= x:
            return None
        water -= price * (y - x)
        if water < T:
            return None
        x = y


def test_no_stop_placement_beats_the_formula():
    a, c, T = F(1, 2), 150, 30
    for w in (250, 300):                                        # two loads: one stop on a fine grid
        best = max(plan_distance(a, c, w, T, [F(y, 10)]) or -1 for y in range(1, 4000))
        assert best <= q0042.formula(a, c, w, T) and best > q0042.formula(a, c, w, T) - F(1, 2), w
        assert plan_distance(a, c, w, T, q0042.stops(a, c, w, T)) == q0042.formula(a, c, w, T)
    for w in (450, 400):                                        # three loads: two stops on a coarser grid
        best = -1
        for y1 in range(1, 200):
            for y2 in range(y1 + 1, 400):
                d = plan_distance(a, c, w, T, [F(y1), F(y2)])
                if d is not None and d > best:
                    best = d
        assert best <= q0042.formula(a, c, w, T) and best > q0042.formula(a, c, w, T) - 3, w
        assert plan_distance(a, c, w, T, q0042.stops(a, c, w, T)) == q0042.formula(a, c, w, T)
    # a stop anywhere else is strictly worse (the trap: 50 instead of 60)
    assert plan_distance(a, c, 450, T, [F(50), F(160)]) < 400 and plan_distance(a, c, 450, T, [F(70), F(160)]) < 400


def test_approximation():
    for n in (1, 2, 3, 5, 10, 20, 100, 1000):
        exact, ap = float(q0042.distance(F(1, 2), C, n * C, T)), q0042.approx(0.5, C, n * C, T)
        assert abs(exact - ap) < 6 / n + 0.02, n
    # the constant: 2 ln 2 + gamma, and the sum of the odd reciprocals is H_2m - H_m / 2
    m = 5000
    s = sum(F(1, 2 * j - 1) for j in range(1, m + 1))
    assert near(float(s), 0.5 * log(m) + q0042.APPROX_CONST / 2, 1e-4)
    # each e-fold of water adds c / (2a) km
    assert abs((q0042.approx(0.5, C, 4500 * 2.718281828, T) - q0042.approx(0.5, C, 4500, T)) - 150) < 1e-6


def test_tables():
    rows = q0042.price_table().splitlines()[2:]
    assert [r.split("|")[3].strip().lstrip("‏") for r in rows] == ["2.5 ליטר", "1.5 ליטר", "0.5 ליטר"]
    st = q0042.stops_table().splitlines()[2:]
    assert "**60 ק\"מ**" in st[0] and "**160 ק\"מ**" in st[1] and "**400 ק\"מ** (היעד)" in st[2] and st[2].endswith("| ‏**30** |")
    w1 = q0042.walks_table(1).splitlines()[2:]
    assert len(w1) == 3 and w1[0].endswith("| ‏300 | ‏90 |") and w1[2].endswith("| ‏0 | ‏**300** |")
    w2 = q0042.walks_table(2).splitlines()[2:]
    assert len(w2) == 2 and w2[1].endswith("| ‏0 | ‏**150** |") and "מוריד 50, חוזר עם 50" in w2[0]
    ex = q0042.examples_table().splitlines()[2:]
    assert len(ex) == len(q0042.EXAMPLES) and "‏**400**" in ex[0] and "‏**460**" in ex[1] and "‏**306.7**" in ex[2] and "‏**240**" in ex[3]
    ap = q0042.approx_table().splitlines()[2:]
    assert len(ap) == len(q0042.APPROX_NS) and "| ‏400 | ‏399.3 |" in ap[2]


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    cases = [list(c) for c in CASES]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([a, c, w, T]) => [
        m.camelDistance(a, c, w, T), m.camelSegments(a, c, w, T).map((s) => [s.x0, s.x1, s.loads]), m.camelApprox(a, c, w, T),
        m.camelPasses(a, c, w, T).map((p) => [p.seg, p.back, p.carry0, p.carry1, p.depots])])));""")
    for (a, c, w, T), (dist, segs, ap, passes) in zip(CASES, got):
        assert near(dist, camel_distance(a, c, w, T), 1e-9)
        page_segs = camel_segments(a, c, w, T)
        assert len(segs) == len(page_segs) and all(near(x0, p[0]) and near(x1, p[1]) and j == p[2] for (x0, x1, j), p in zip(segs, page_segs))
        assert near(ap, q0042.approx(a, c, w, T), 1e-9)
        page_passes = camel_passes(a, c, w, T)
        assert len(passes) == len(page_passes)
        for js, py in zip(passes, page_passes):
            assert js[0] == py[0] and js[1] == py[1] and near(js[2], py[2]) and near(js[3], py[3])
            assert all(near(u, v) for u, v in zip(js[4], py[4]))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(42)
