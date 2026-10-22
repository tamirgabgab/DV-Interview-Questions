import itertools
import math
import random
from fractions import Fraction
from math import comb

from extract_code import load_python

ns = load_python(7)


def test_generated_triangles_contain_center():
    random.seed(7)
    for _ in range(5000):
        assert ns["center_inside"](ns["random_triangle_with_center"]())


def test_gap_rule_matches_cross_product():
    rng = random.Random(1)
    for _ in range(20000):
        angles = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
        points = [(math.cos(t), math.sin(t)) for t in angles]
        assert ns["contains_center"](angles) == ns["center_inside"](points)


def test_continuous_probability_is_a_quarter():
    rng = random.Random(2)
    n = 40000
    hits = sum(ns["contains_center"]([rng.uniform(0, 2 * math.pi) for _ in range(3)]) for _ in range(n))
    assert abs(hits / n - 0.25) < 0.01


def p_formula(m):
    return Fraction(m + 1, 4 * (m - 2)) if m % 2 else Fraction(m - 4, 4 * (m - 1))


def test_discrete_formula():
    # Brute-force count of triangles whose arcs are all shorter than half a circle.
    for m in range(3, 41):
        good = sum(all(2 * g < m for g in (b - a, c - b, m - (c - a)))
                   for a, b, c in itertools.combinations(range(m), 3))
        assert good == comb(m, 3) - m * comb(m // 2, 2)
        assert Fraction(good, comb(m, 3)) == p_formula(m)
    assert p_formula(360) == Fraction(89, 359)


def test_generator_formula_and_examples():
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0007

    assert all(q0007.p_formula(m) == p_formula(m) for m in range(3, 41))
    for angles, inside in q0007.EXAMPLES:
        gaps = [(angles[(i + 1) % 3] - angles[i]) % 360 for i in range(3)]
        assert (max(gaps) < 180) == inside
    a1, a2, a3 = q0007.HALF_POINTS
    assert 0 < (a2 - a1) % 360 < 180 and 0 < (a3 - a1) % 360 < 180   # P2, P3 in the half circle from P1


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(7)


def test_explorer_matches_brute_force():
    """The triangle explorer: its class of a triangle against the page's contains_center
    and an exact integer rule, and its enumeration (frame -> angles, angles -> frame, the
    running counts) against a plain loop over every a < b < c."""
    import json

    from page_tests import explorer_require, node_json

    def kind(a, b, c):
        s = sorted((a % 360, b % 360, c % 360))
        arcs = (s[1] - s[0], s[2] - s[1], 360 - (s[2] - s[0]))
        if 0 in arcs or 360 in arcs:
            return "degenerate"
        top = max(arcs)
        return "in" if top < 180 else "edge" if top == 180 else "out"

    rng = random.Random(3)
    triples = [[rng.randrange(360) for _ in range(3)] for _ in range(3000)]
    triples += [[0, 180, 90], [10, 190, 300], [5, 5, 100], [7, 7, 7], [20, 140, 250], [20, 70, 150]]

    # the enumeration by brute force, with the counts after a set of checkpoint frames
    total = comb(360, 3)
    checks = sorted({0, 1, 177, 358, 359, 63_903, 1_000_000, 3_855_659, total - 2, total - 1}
                    | {rng.randrange(total) for _ in range(40)})
    want, counts, k, nxt = {}, {"in": 0, "edge": 0, "out": 0}, 0, 0
    for a in range(360):
        for b in range(a + 1, 360):
            for c in range(b + 1, 360):
                counts[kind(a, b, c)] += 1
                if k == checks[nxt]:
                    want[k] = ([a, b, c], dict(counts))
                    nxt += 1
                    if nxt == len(checks):
                        break
                k += 1
            else:
                continue
            break
        else:
            continue
        break
    assert set(want) == set(checks)

    got = node_json(f"""
      const m = {explorer_require()};
      const triples = {json.dumps(triples)}, checks = {json.dumps(checks)};
      console.log(JSON.stringify({{
        total: m.TRI_TOTAL,
        kinds: triples.map((t) => m.triClass(t)),
        arcs: triples.map((t) => m.triArcs(t)),
        frames: checks.map((k) => m.triFrame(k)),
        index: checks.map((k) => m.triIndex(m.triFrame(k))),
        counts: checks.map((k) => m.triCounts(k)),
      }}));""")

    assert got["total"] == total == 7_711_320
    for t, g, arcs in zip(triples, got["kinds"], got["arcs"]):
        assert g == kind(*t), t
        s = sorted(t)
        assert arcs == [s[1] - s[0], s[2] - s[1], 360 - (s[2] - s[0])]
        if g in ("in", "out"):                      # away from the boundary the page agrees
            assert ns["contains_center"]([math.radians(v) for v in t]) == (g == "in"), t
            pts = [(math.cos(math.radians(v)), math.sin(math.radians(v))) for v in t]
            assert ns["center_inside"](pts) == (g == "in"), t
    for k, frame, index, c in zip(checks, got["frames"], got["index"], got["counts"]):
        angles, cnt = want[k]
        assert frame == angles and index == k
        assert c == {"seen": k + 1, **cnt}

    # the totals the page quotes: part c's count, the 180 diameters times 358 third points
    end = got["counts"][-1]
    assert end["in"] == comb(360, 3) - 360 * comb(180, 2) == 1_911_720
    assert end["edge"] == 180 * 358 == 64_440
    assert end["out"] == 5_735_160
    assert Fraction(end["in"], total) == Fraction(89, 359)
    from extract_code import ROOT

    page = next((ROOT / "docs" / "questions" / "senior").glob("0007-*.md")).read_text(encoding="utf-8")
    for n in ("7,711,320", "1,911,720", "64,440", "5,735,160"):
        assert n in page


def test_polygon_matches_triangle_and_cross_products():
    """Part b: the n-vertex rule agrees with the triangle rule for n = 3, with the
    cross-product check on random polygons, and the generator only returns polygons
    that contain the centre; the acceptance rate follows 1 - n / 2^(n - 1)."""
    rng = random.Random(70)
    for _ in range(5000):
        angles = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
        assert ns["contains_center_poly"](angles) == ns["contains_center"](angles)
    for n in range(3, 11):
        for _ in range(3000):
            angles = [rng.uniform(0, 2 * math.pi) for _ in range(n)]
            points = [(math.cos(t), math.sin(t)) for t in sorted(angles)]
            assert ns["contains_center_poly"](angles) == ns["center_inside_poly"](points), (n, angles)
        random.seed(n)
        for _ in range(300):
            points = ns["random_polygon_with_center"](n)
            assert len(points) == n and ns["center_inside_poly"](points)
        hits = sum(ns["contains_center_poly"]([rng.uniform(0, 2 * math.pi) for _ in range(n)]) for _ in range(20000))
        assert abs(hits / 20000 - (1 - n / 2 ** (n - 1))) < 0.015, n
    # the sorted order matters: the same points in another order are not the same polygon
    pts = [(math.cos(t), math.sin(t)) for t in (0.1, 2.2, 4.3, 5.9)]
    assert ns["center_inside_poly"](pts) and not ns["center_inside_poly"]([pts[0], pts[2], pts[1], pts[3]])


def test_polygon_explorer_matches_page_code():
    """The polygon explorer: its class on whole-degree polygons against the page's
    contains_center_poly / center_inside_poly, its arcs, its probability formula and its
    random draws (n different angles)."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(71)
    cases = [[rng.randrange(360) for _ in range(rng.randint(3, 10))] for _ in range(2000)]
    cases += [[0, 90, 180, 270], [0, 10, 20, 30, 40], [0, 120, 240], [5, 5, 100, 200], [0, 180, 90], [0, 72, 144, 216, 288]]
    got = node_json(f"""
      const m = {explorer_require()};
      const rnd = (() => {{ let a = 7; return () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();
      const cases = {json.dumps(cases)};
      console.log(JSON.stringify({{
        kinds: cases.map((c) => m.polyClass(c)), arcs: cases.map((c) => m.polyArcs(c)),
        probs: [3, 4, 5, 10].map((n) => m.polyProb(n)),
        draws: Array.from({{length: 200}}, (_, k) => m.polyRandom(3 + (k % 8), rnd)),
        tri: cases.filter((c) => c.length === 3).map((c) => [m.polyClass(c), m.triClass(c)]),
      }}));""")
    for angles, kind, arcs in zip(cases, got["kinds"], got["arcs"]):
        s = sorted(angles)
        want_arcs = [s[i + 1] - s[i] for i in range(len(s) - 1)] + [360 - (s[-1] - s[0])]
        assert arcs == want_arcs
        if 0 in want_arcs or 360 in want_arcs:
            assert kind == "degenerate"
            continue
        top = max(want_arcs)
        assert kind == ("in" if top < 180 else "edge" if top == 180 else "out")
        if kind in ("in", "out"):
            rad = [math.radians(v) for v in angles]
            assert ns["contains_center_poly"](rad) == (kind == "in")
            assert ns["center_inside_poly"]([(math.cos(t), math.sin(t)) for t in sorted(rad)]) == (kind == "in")
    assert all(a == b for a, b in got["tri"])
    assert got["probs"] == [1 - 3 / 4, 1 - 4 / 8, 1 - 5 / 16, 1 - 10 / 512]
    for k, d in enumerate(got["draws"]):
        assert len(d) == 3 + (k % 8) == len(set(d)) and all(0 <= v < 360 for v in d)


def test_explorer_discrete_count_and_histogram():
    """The follow-ups in the boxes: the exact discrete probability for n vertices is the
    count of part d generalised (checked against a brute force over all n-subsets of M
    points for small M, and 89/359 for n = 3), and the largest-arc histogram of 1,000
    seeded draws is consistent (bins add up, a largest arc below 180 is inside, the
    expected densities follow the continuous distribution function, which agrees with
    the enumeration of part d at 180)."""
    import json
    from fractions import Fraction
    from itertools import combinations

    from page_tests import explorer_require, node_json

    def brute(n, M):
        good = 0
        for pts in combinations(range(M), n):
            arcs = [pts[i + 1] - pts[i] for i in range(n - 1)] + [M - (pts[-1] - pts[0])]
            good += max(arcs) < M / 2
        return Fraction(good, comb(M, n))

    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{
        small: [[12, 3], [12, 4], [12, 5], [11, 3], [11, 4], [13, 5], [20, 6]].map(([M, n]) => [M, n, m.polyProbDiscrete(n, M)]),
        full: [3, 4, 5, 10].map((n) => m.polyProbDiscrete(n)),
        hist: m.triHistogram(m.mulberry32(4242), 1000, 10),
        cdf: [120, 150, 180, 240, 300, 360].map((x) => m.triArcCdf(x)),
      }}));""")
    for M, n, d in got["small"]:
        assert Fraction(int(d["num"]), int(d["den"])) == brute(n, M), (M, n)
    assert (got["full"][0]["num"], got["full"][0]["den"]) == ("89", "359")
    for n, d in zip([3, 4, 5, 10], got["full"]):
        want = Fraction(comb(360, n) - 360 * comb(180, n - 1), comb(360, n))
        assert Fraction(int(d["num"]), int(d["den"])) == want and abs(d["value"] - float(want)) < 1e-12
    h = got["hist"]
    assert sum(b["in"] + b["out"] for b in h["bins"]) + h["degenerate"] == 1000 == h["draws"]
    assert [b["lo"] for b in h["bins"]] == list(range(120, 360, 10))
    assert all(b["out"] == 0 for b in h["bins"] if b["hi"] <= 180) and all(b["in"] == 0 for b in h["bins"] if b["lo"] >= 180)
    assert abs(sum(b["expected"] for b in h["bins"]) - 1000) < 1e-9
    assert got["cdf"][0] == 0 and got["cdf"][-1] == 1 and abs(got["cdf"][2] - 0.25) < 1e-12
    # the continuous distribution against the whole-degree enumeration: within a percent
    inside = sum(b["in"] for b in h["bins"])
    assert abs(inside / (1000 - h["degenerate"]) - 0.25) < 0.05
    assert abs(got["cdf"][3] - (1 - 3 * (1 / 3) ** 2)) < 1e-12
