"""Question 0092: points on a circle (Moser's circle problem). Every number on the page is
recomputed with the generator's reference: the small cases 1, 2, 4, 8 and 16, the chord-by-
chord table of five points, 31 for six points, the formula against the geometric count (Euler
on the actual arrangement, the faces traced one by one) for random points up to n = 10, the
Euler table, the regular polygons (30 for the hexagon, the odd ones on the formula, a point
of m chords losing C(m - 1, 2) regions), the identity with 2^(n-1) up to n = 5 and the
follow-ups; the generated blocks are checked; and the box's model is compared under Node
with this reference."""

import itertools
import math
import random
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0092  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "student" / "0092-circle-regions.md").read_text(encoding="utf-8")
SEQ = [1, 2, 4, 8, 16, 31, 57, 99, 163, 256]


def test_small_cases_and_the_sequence():
    assert [q0092.regions(q0092.SMALL[n]) for n in (1, 2, 3, 4)] == [1, 2, 4, 8]
    assert [q0092.moser(n) for n in range(1, 11)] == SEQ
    assert [2 ** (n - 1) for n in range(1, 6)] == SEQ[:5] and 2 ** 5 == 32 != SEQ[5]


def test_part_a_five_points_chord_by_chord():
    inc = q0092.chord_increments(5)
    assert 1 + sum(add for *_, add in inc) == 16
    assert [k for _, _, k, _ in inc] == [0, 0, 0, 0, 0, 1, 2, 0, 2, 0]
    assert sum(k for _, _, k, _ in inc) == math.comb(5, 4)
    assert q0092.regions(q0092.N5) == 16 and len(q0092.faces(q0092.N5)[0]) == 16


def test_part_b_formula_both_ways_and_geometry():
    for n in range(0, 13):
        inc = q0092.chord_increments(n)
        assert 1 + sum(add for *_, add in inc) == q0092.moser(n)
        assert sum(k for _, _, k, _ in inc) == math.comb(n, 4)
        V, E = n + math.comb(n, 4), n + math.comb(n, 2) + 2 * math.comb(n, 4)
        assert E - V + 1 == q0092.moser(n)
    assert q0092.counts(q0092.N6) == (6 + 15, 6 + 15 + 30, 31)
    assert len(q0092.faces(q0092.N6)[0]) == 31
    rnd = random.Random(92)
    for n in range(1, 11):
        for _ in range(3):
            a = [rnd.uniform(0, 360) for _ in range(n)]
            assert q0092.regions(a) == q0092.moser(n), (n, a)
            assert len(q0092.faces(a)[0]) == q0092.moser(n), (n, a)


def test_part_b_pattern_identity():
    # sum_{j <= 4} C(n - 1, j) = C(n, 4) + C(n, 2) + 1 for every n, and it is all of 2^(n-1) while n - 1 <= 4
    for n in range(1, 30):
        assert sum(math.comb(n - 1, j) for j in range(5)) == q0092.moser(n)
        assert (q0092.moser(n) == 2 ** (n - 1)) == (n <= 5)


def test_part_c_regular_polygons():
    reg = {n: q0092.regions([90 + 360 * k / n for k in range(n)]) for n in range(3, 13)}
    assert reg[6] == 30 and q0092.regions(q0092.REG6) == 30
    assert reg == {3: 4, 4: 8, 5: 16, 6: 30, 7: 57, 8: 88, 9: 163, 10: 230, 11: 386, 12: 456}
    for n in (3, 5, 7, 9, 11):
        assert reg[n] == q0092.moser(n)
        assert not q0092.triple_points([90 + 360 * k / n for k in range(n)])
    trip = q0092.triple_points(q0092.REG6)
    assert len(trip) == 1 and trip[0][1] == 3 and math.hypot(*trip[0][0]) < 1e-9
    _, _, inner, _ = q0092.arrangement(q0092.REG6)
    assert len(inner) == 13
    # every point where m chords meet loses C(m - 1, 2) regions
    for n in range(3, 13):
        a = [90 + 360 * k / n for k in range(n)]
        loss = sum(math.comb(m - 1, 2) for _, m in q0092.triple_points(a))
        assert q0092.moser(n) - q0092.regions(a) == loss, n


def test_follow_ups():
    for n in range(0, 8):          # n lines in the plane: every new line cut into k + 1 pieces
        assert 1 + sum(k + 1 for k in range(n)) == math.comb(n, 2) + n + 1
    assert q0092.moser(10) == 256 and 2 ** 9 == 512
    assert q0092.moser(60) / 2 ** 59 < 1e-10


def test_page_text():
    for words in ["**16 חלקים.**", "**31 חלקים, לא 32.**", "**30 חלקים** ולא 31", "15 נקודות חיתוך, ו-31 חלקים",
                  "יש 13 נקודות חיתוך ו-30 חלקים", "\\( \\binom{m-1}{2} \\)", 
                  "מוסיפים 15, ועם החלק ההתחלתי יש 16"]:
        assert words in PAGE, words
    flat = " ".join(PAGE.split())
    assert "256 מול 512" in flat and "ומ-8 יש גם נקודות אחרות" in flat


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(92)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rnd = random.Random(7)
    cases = [q0092.N5, q0092.N6, q0092.REG6] + [[round(rnd.uniform(0, 360), 1) for _ in range(n)] for n in range(1, 11) for _ in range(2)]
    cases += [[90 + 360 * k / n for k in range(n)] for n in range(3, 11)]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    "console.log(JSON.stringify({"
                    "count: cases.map((a) => { const c = m.mcCount(a); return [c.V, c.E, c.regions, c.crossings, c.triples.length]; }),"
                    "faces: cases.map((a) => m.mcFaces(a)),"
                    "inc: m.mcIncrements([90, 162, 234, 306, 18]).map((x) => [x.chord, x.meets, x.added, x.total]),"
                    "moser: Array.from({ length: 11 }, (_, n) => m.mcMoser(n)),"
                    "defaults: Array.from({ length: 10 }, (_, i) => m.mcDefault(i + 1)),"
                    "}));")
    for a, (V, E, r, cr, tri), f in zip(cases, got["count"], got["faces"]):
        assert (V, E, r) == q0092.counts(a), a
        assert cr == len(q0092.arrangement(a)[2]) and tri == len(q0092.triple_points(a)), a
        assert f == r, a
    assert got["inc"] == [[[a, b], k, add, None] for a, b, k, add in q0092.chord_increments(5)] or \
        [x[:3] for x in got["inc"]] == [[[a, b], k, add] for a, b, k, add in q0092.chord_increments(5)]
    totals = list(itertools.accumulate([1] + [add for *_, add in q0092.chord_increments(5)]))[1:]
    assert [x[3] for x in got["inc"]] == totals
    assert got["moser"] == [q0092.moser(n) for n in range(11)]
    for n, a in enumerate(got["defaults"], 1):          # the box starts every n in general position
        assert len(a) == n and q0092.regions(a) == q0092.moser(n), (n, a)
        assert min((abs((x - y + 540) % 360 - 180) for x, y in itertools.combinations(a, 2)), default=360) >= 2
