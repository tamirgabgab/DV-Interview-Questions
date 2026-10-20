"""Question 0030: every number the page states (the 42, the 43.17, the 40 with its legs 32
and 24, the crossing points and segment lengths, the candidates table, the images table,
the follow-ups), the figure generator against the independent reference in reference.py
on random boxes, and the page copies of the generated blocks."""

import math
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import q0030  # noqa: E402
import reference  # noqa: E402


def test_statement_numbers():
    assert (q0030.A, q0030.B, q0030.H) == (30, 12, 12)
    assert q0030.S == (0, 6, 11) and q0030.F == (30, 6, 1)
    assert math.isclose(math.hypot(30, 10), 31.62, abs_tol=0.005)       # through the air


def test_best_route():
    c = q0030.best()
    assert c["length"] == 40 and (c["dx"], c["dp"]) == (32, -24)
    assert c["faces"] == ["end0", "top", "sideB", "bottom", "enda"]
    assert c["p_exit"] == Fr(117, 4) and c["p_enter"] == Fr(27, 4)
    assert q0030.edge_point("top", c["p_exit"]) == (Fr(27, 4), 12)       # (0, 6.75, 12)
    assert q0030.edge_point("bottom", c["p_enter"]) == (Fr(27, 4), 0)    # (30, 6.75, 0)
    # the path in 3D, from the reference, and its segment lengths
    rs = reference.routes(30, 12, 12, (0, 6, 11), (30, 6, 1))
    best = [r for r in rs if abs(r[0] - 40) < 1e-9]
    assert sorted(r[1] for r in best) == [["end0", "top", "side0", "bottom", "enda"],
                                          ["end0", "top", "sideB", "bottom", "enda"]]
    via_b = next(r for r in best if r[1][2] == "sideB")
    pts = [tuple(round(v, 9) for v in p) for p in via_b[2]]
    assert pts == [(0, 6, 11), (0, 6.75, 12), (7, 12, 12), (23, 12, 0), (30, 6.75, 0), (30, 6, 1)]
    seg = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
    assert [round(s, 9) for s in seg] == [1.25, 8.75, 20, 8.75, 1.25] and math.isclose(sum(seg), 40)


def test_candidates_table():
    rows = [c for c in q0030.candidates() if c["valid"] and len(set(c["faces"])) == len(c["faces"])]
    assert len(rows) == 16 and len(q0030.candidates()) == 48
    lengths = sorted(round(c["length"], 2) for c in rows)
    assert lengths == [40, 40, 40.72, 40.72, 40.72, 40.72, 42, 42, 43.17, 43.17,
                       47.52, 47.52, 47.52, 47.52, 57.27, 57.27]
    legs = {(c["dx"], abs(c["dp"])) for c in rows}
    assert legs == {(32, 24), (37, 17), (42, 0), (42, 10), (47, 7), (52, 24)}
    assert math.isclose(math.hypot(42, 10), 43.17, abs_tol=0.005)
    assert [c["faces"] for c in rows if c["length"] == 42] == [["end0", "bottom", "enda"], ["end0", "top", "enda"]]
    # the same 16 routes as the independent enumeration, with the same lengths
    ref = reference.routes(30, 12, 12, (0, 6, 11), (30, 6, 1))
    assert sorted((round(r[0], 6), tuple(r[1])) for r in ref) == sorted((round(c["length"], 6), tuple(c["faces"])) for c in rows)
    # the table on the page lists exactly these rows
    table = q0030.candidates_table().splitlines()[2:]
    assert len(table) == 16 and table[0].endswith("| ‏32 | ‏24 | ‏40 |")


def test_images_table():
    s = {e: (d, p, lo, hi) for e, d, p, lo, hi in q0030.images(6, 11)}
    assert s == {"bottom": (11, 6, 0, 12), "sideB": (6, 23, 12, 24), "top": (1, 30, 24, 36), "side0": (6, 37, 36, 48)}
    f = {e: (d, p, lo, hi) for e, d, p, lo, hi in q0030.images(6, 1)}
    assert f == {"bottom": (1, 6, 0, 12), "sideB": (6, 13, 12, 24), "top": (11, 30, 24, 36), "side0": (6, 47, 36, 48)}
    assert q0030.period() == 48
    rows = q0030.images_table().splitlines()[2:]
    assert rows[2] == "| ‏S | ‏top | ‏1 | ‏−1 | ‏30 | ‏24 עד 36 |" and rows[4] == "| ‏F | ‏bottom | ‏1 | ‏31 | ‏6 | ‏0 עד 12 |"
    # the page's worked example of the two tests
    assert Fr(30) - 24 * Fr(1, 32) == Fr(117, 4) == 29.25 and Fr(30) - 24 * Fr(31, 32) == Fr(27, 4)
    assert 12 - (29.25 - 24) == 6.75


def test_generator_matches_reference():
    rng = random.Random(30)
    for _ in range(300):
        a, b, h = rng.choice([2, 5, 10, 30]), rng.choice([3, 7, 12]), rng.choice([2, 6, 12, 25])
        s = (0, Fr(rng.randint(0, 100 * b), 100), Fr(rng.randint(0, 100 * h), 100))
        f = (a, Fr(rng.randint(0, 100 * b), 100), Fr(rng.randint(0, 100 * h), 100))
        best = q0030.best(a, b, h, s, f)
        ref = reference.routes(a, b, h, tuple(map(float, s)), tuple(map(float, f)))
        assert math.isclose(best["length"], ref[0][0], abs_tol=1e-9), (a, b, h, s, f)
        valid = [c for c in q0030.candidates(a, b, h, s, f) if c["valid"] and len(set(c["faces"])) == len(c["faces"])]
        assert sorted((round(c["length"], 7), tuple(c["faces"])) for c in valid) == sorted((round(r[0], 7), tuple(r[1])) for r in ref)


def test_follow_ups():
    assert reference.shortest(30, 12, 12, 6, 11, 6, 6)[0] == 37 == 1 + 30 + 6
    assert reference.shortest(1, 1, 1, 0.5, 0.5, 0.5, 0.5)[0] == 2
    assert reference.shortest(30, 12, 12, 6, 11, 6, 1)[1] == [["end0", "top", "side0", "bottom", "enda"],
                                                            ["end0", "top", "sideB", "bottom", "enda"]]


def test_explorer_matches_python():
    """The strip math of docs/javascripts/explorer.js (the live strip) against the generator
    and the independent reference: the 48 lines, which are valid, the best length, the
    exit point and the path point by point, on the question and on random boxes."""
    from page_tests import explorer_require, node_json

    rng = random.Random(87)
    cases = [(30, 12, 12, 6, 11, 6, 1), (30, 12, 12, 6, 1, 6, 11), (30, 12, 12, 6, 11, 6, 6), (1, 1, 1, 0.5, 0.5, 0.5, 0.5),
             (30, 12, 12, 0, 0, 12, 12), (0.5, 12, 12, 6, 11, 6, 1)]
    for _ in range(120):
        a, b, h = rng.choice([2, 5, 10, 30, 60]), rng.choice([3, 7, 12, 30]), rng.choice([2, 6, 12, 25])
        cases.append((a, b, h, rng.randint(0, 4 * b) / 4, rng.randint(0, 4 * h) / 4, rng.randint(0, 4 * b) / 4, rng.randint(0, 4 * h) / 4))
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "const out = cases.map(([a, b, h, y0, z0, y1, z1]) => { const r = m.stripBest(a, b, h, y0, z0, y1, z1);"
                    " return { length: r.line.length, faces: r.faces, exit: r.exit, enter: r.enter, segs: r.segs, pts: r.pts,"
                    " valid: r.lines.filter((l) => l.valid).map((l) => [l.sEdge, l.fEdge, l.k, l.length]) }; });"
                    "console.log(JSON.stringify(out));")
    for case, r in zip(cases, got):
        a, b, h, y0, z0, y1, z1 = case
        s, f = (0, Fr(y0), Fr(z0)), (a, Fr(y1), Fr(z1))
        best = q0030.best(a, b, h, s, f)
        assert math.isclose(r["length"], best["length"], abs_tol=1e-9), case
        ref_best, ref_seqs, ref_exits = reference.shortest(a, b, h, y0, z0, y1, z1)
        assert math.isclose(r["length"], ref_best, abs_tol=1e-7), case
        assert any(math.dist(r["exit"], e) < 1e-6 for e in ref_exits), case
        assert r["faces"] in ref_seqs, case
        # the strip's valid lines are the generator's, with the same lengths
        mine = sorted((c["s_edge"], c["f_edge"], c["k"], round(c["length"], 7)) for c in q0030.candidates(a, b, h, s, f) if c["valid"])
        assert sorted((e, g, k, round(v, 7)) for e, g, k, v in r["valid"]) == mine, case
        # the segments add up, follow the faces, and the points are the reference's
        assert len(r["segs"]) == len(r["faces"]) == len(r["pts"]) - 1
        assert math.isclose(sum(r["segs"]), r["length"], abs_tol=1e-9)
        assert all(math.isclose(math.dist(p, q), g, abs_tol=1e-9) for p, q, g in zip(r["pts"], r["pts"][1:], r["segs"]))
        ref_pts = next(rt[2] for rt in reference.routes(a, b, h, (0, y0, z0), (a, y1, z1)) if rt[1] == r["faces"])
        assert all(math.dist(p, q) < 1e-6 for p, q in zip(r["pts"], ref_pts)), case
    # the question's numbers
    r = got[0]
    assert r["faces"] == ["end0", "top", "sideB", "bottom", "enda"] and r["segs"] == [1.25, 8.75, 20, 8.75, 1.25]
    assert r["exit"] == [0, 6.75, 12] and r["enter"] == [30, 6.75, 0] and len(r["valid"]) == 22


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(30)
