"""Question 0080: which pocket the ball enters.

The page's point_pocket, corner_shot and find_pocket are run as published and compared with a
physical simulation (real reflections, segment by segment, the pockets as discs at the corners
and the middles) on many random shots: from the corner, from anywhere, in any direction, with
separate widths for the middles and with a ball radius. Every number on the page is recomputed
here: exactly with fractions for the rational slopes (parts a, b and the six cases), in floats
with a margin for 37 degrees. The generated blocks are checked against tools/figures/q0080.py,
and the billiard box's model (bilShot) is compared under Node with the simulation."""

import math
import random
import re
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0080  # noqa: E402

ns = load_python(80)
point_pocket, corner_shot, find_pocket = ns["point_pocket"], ns["corner_shot"], ns["find_pocket"]
PAGE = (ROOT / "docs" / "questions" / "senior" / "0080-billiard-pocket.md").read_text(encoding="utf-8")
A, B = 360, 180


# --- the reference: a physical simulation -----------------------------------------------------

def simulate(x0, y0, deg, wc, wm=None, a=A, b=B, rho=0.0, max_bounces=20000, max_len=None):
    """Real reflections on the table shrunk by rho, pockets at its corners and middles (discs of
    radius wc/2 and wm/2). The ball enters the first disc it moves into; a disc it starts in
    counts only when it moves towards the centre (the pocket it leaves from its centre is
    ignored). Returns (pocket index (i, j) in {0,1,2} x {0,1}, cushions, path length) or
    (None, cushions, length) when no pocket within the limits."""
    wm = wc if wm is None else wm
    lo_x, hi_x, lo_y, hi_y = rho, a - rho, rho, b - rho
    pockets = [((i, j), lo_x + i * (hi_x - lo_x) / 2, lo_y + j * (hi_y - lo_y), (wm if i == 1 else wc) / 2)
               for i in range(3) for j in range(2)]
    th = math.radians(deg)
    dx, dy = math.cos(th), math.sin(th)
    if abs(dx) < 1e-12:
        dx = 0.0
    if abs(dy) < 1e-12:
        dy = 0.0
    x, y, length, bounces = x0, y0, 0.0, 0
    while bounces <= max_bounces and (max_len is None or length < max_len):
        tx = (hi_x - x) / dx if dx > 0 else (lo_x - x) / dx if dx < 0 else math.inf
        ty = (hi_y - y) / dy if dy > 0 else (lo_y - y) / dy if dy < 0 else math.inf
        t = max(0.0, min(tx, ty))
        best = None
        for key, px, py, r in pockets:
            fx, fy = x - px, y - py
            bb = fx * dx + fy * dy
            cc = fx * fx + fy * fy - r * r
            disc = bb * bb - cc
            if disc <= 0:
                continue
            t1, t2 = -bb - math.sqrt(disc), -bb + math.sqrt(disc)
            if cc < 0 and bb >= 0:            # inside, moving away (or at the centre)
                continue
            if t2 > 0 and t1 <= t:
                te = max(t1, 0.0)
                if best is None or te < best[0]:
                    best = (te, key)
        if best:
            return best[1], bounces, length + best[0]
        x, y, length = x + t * dx, y + t * dy, length + t
        if tx <= ty:
            dx = -dx
        if ty <= tx:
            dy = -dy
        bounces += 1
    return None, bounces, length


def index_of(p, a=A, b=B):
    return ({0: 0, a / 2: 1, a: 2}[p[0]], {0: 0, b: 1}[p[1]])


def random_shots(n, seed, anywhere=True):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        deg = rnd.uniform(1, 89)
        w = rnd.uniform(1, min(A / 2, B * math.cos(math.radians(deg))) * 0.9)
        x0, y0 = (rnd.uniform(0, A), rnd.uniform(0, B)) if anywhere else (0.0, 0.0)
        if anywhere and min(math.hypot(x0 - i * A / 2, y0 - j * B) for i in range(3) for j in range(2)) < w / 2:
            continue
        out.append((x0, y0, deg, w))
    return out


# --- part a ------------------------------------------------------------------------------------

def test_part_a():
    segs = q0080.trace(Fr(3, 4))
    assert [(s[1], s[2]) for s in segs] == [((240, 180), "top"), ((360, 90), "right"), ((240, 0), "bottom"),
                                            ((0, 180), "pocket")]
    length = sum(math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]) for s in segs)
    assert length == 900
    assert point_pocket(A, B, Fr(3, 4)) == ((0, 180), 3)
    assert simulate(0.0, 0.0, math.degrees(math.atan2(3, 4)), 1e-3)[:2] == ((0, 1), 3)
    for s in ("\\( 720 \\cdot 5/4 = 900 \\)", "\\( 720 = 2a \\)", "\\( 540 = 3b \\)", "\\( 180 \\cdot 4/3 = 240 \\)"):
        assert s in PAGE, s


# --- part b ------------------------------------------------------------------------------------

def exact_corner(tan: Fr, limit=200):
    """Exact reflections with point pockets at the corners: the corner reached and the bounces."""
    x, y, dx, dy, bounces = Fr(0), Fr(0), Fr(1), tan, 0
    while bounces < limit:
        tx = ((A - x) if dx > 0 else -x) / dx
        ty = ((B - y) if dy > 0 else -y) / dy
        t = min(tx, ty)
        x, y = x + t * dx, y + t * dy
        if tx == ty:
            return (int(x), int(y)), bounces
        if tx < ty:
            dx = -dx
        else:
            dy = -dy
        bounces += 1
    return None


def test_part_b_point_pockets():
    for p in range(1, 13):
        for q in range(1, 13):
            tan = Fr(q, p) / 2                    # r = 2 tan = q / p
            assert point_pocket(A, B, tan) == exact_corner(tan), tan
            assert q0080.point_pocket(tan)[3:] == exact_corner(tan)
    # the parity table: never back to the origin
    assert all(point_pocket(A, B, Fr(q, p) / 2)[0] != (0, 0) for p in range(1, 30) for q in range(1, 30))
    rows = {aim: point_pocket(A, B, tan) for aim, tan in q0080.B_ROWS}
    assert rows[(360, 180)] == ((360, 180), 0) and rows[(180, 180)] == ((360, 0), 1)
    assert rows[(240, 180)] == ((0, 180), 3) and rows[(270, 180)] == ((360, 0), 5)
    assert rows[(360, 120)] == ((360, 0), 3) and rows[(360, 150)] == ((0, 180), 9)
    # the follow-up: aiming at (241, 180)
    assert point_pocket(A, B, Fr(180, 241)) == ((360, 0), 599)
    assert Fr(A) * Fr(180, 241) / B == Fr(360, 241)
    assert "אחרי 599 פגיעות" in PAGE and "\\( r = 360/241 \\)" in PAGE


# --- part c ------------------------------------------------------------------------------------

def test_part_c_six_cases():
    for pocket, _, _, tan in q0080.C_ROWS:
        if tan is None:
            continue
        k, m, got = q0080.corner_shot(tan)
        assert got == pocket
        assert corner_shot(A, B, math.degrees(math.atan(float(tan))), 9)[2] == pocket
    assert q0080.corner_shot(Fr(2, 3))[:2] == (3, 2) and q0080.corner_shot(Fr(1))[:2] == (1, 1)
    assert q0080.corner_shot(Fr(1, 2))[:2] == (2, 1) and q0080.corner_shot(Fr(3, 4))[:2] == (4, 3)
    # the impossible corners, Dirichlet's bound K <= ceil(1/eps) <= 40 at w = 9, on a sweep of angles
    for i in range(1, 3000):
        deg = 89.5 * i / 3000
        k, m, (x, y) = corner_shot(A, B, deg, 9)
        assert not (y == 0 and x in (0, A)), deg
        eps = 9 / (2 * B * math.cos(math.radians(deg)))
        assert k <= math.ceil(1 / eps) <= 40


def convergent_denominators(s, n=30):
    out, q0, q1, x = [], 1, 0, s           # q_{-2} = 1, q_{-1} = 0
    for _ in range(n):
        ai = math.floor(x)
        q0, q1 = q1, ai * q1 + q0
        out.append(q1)
        if x - ai < 1e-12:
            break
        x = 1 / (x - ai)
    return out


def test_part_c_37_degrees():
    t = math.tan(math.radians(37))
    eps = q0080.eps(t)
    assert f"{eps:.4f}" == "0.0313" and f"{t:.4f}" == "0.7536"
    assert [round(q0080.norm(k * t), 4) for k in range(1, 5)] == [0.2464, 0.4929, 0.2607, 0.0142]
    assert corner_shot(A, B, 37, 9) == (4, 3, (0, 180))
    assert simulate(0.0, 0.0, 37, 9)[:2] == ((0, 1), 3)
    # with point pockets it never ends: tan 37 is irrational (only 0 and ±1 are rational tangents
    # at a whole number of degrees); a long simulation with tiny pockets finds none
    assert simulate(0.0, 0.0, 37, 1e-3, max_bounces=3000)[0] is None
    # the follow-up: w = 1 cm, K = 211, a convergent denominator of tan 37
    k, m, _ = corner_shot(A, B, 37, 1)
    assert (k, m) == (211, 159)
    eps1 = 1 / (2 * B * math.cos(math.radians(37)))
    assert abs(q0080.norm(211 * t) - eps1) > 1e-6            # far from the edge in floats
    den = convergent_denominators(t)
    assert den[:6] == [1, 1, 4, 69, 142, 211]
    assert "1, 4,\n            69, 142 ו-211" in PAGE or "1, 4, 69, 142 ו-211" in re.sub(r"\s+", " ", PAGE)


def test_part_c_first_k_is_a_convergent():
    rnd = random.Random(80)
    for _ in range(5000):
        s, eps = rnd.uniform(0.01, 3), rnd.uniform(0.001, 0.3)
        k = 1
        while q0080.norm(k * s) >= eps:
            k += 1
        assert k in convergent_denominators(s)


def test_corner_shots_against_the_simulation():
    for x0, y0, deg, w in random_shots(1500, 1, anywhere=False):
        k, m, got = corner_shot(A, B, deg, w)
        sim = simulate(x0, y0, deg, w)
        assert sim[0] == index_of(got), (deg, w)
        assert find_pocket(A, B, deg, w) == got


def test_cushions_follow_up():
    """⌈K/2⌉ − 1 vertical and m − 1 horizontal lines, and one more when the line crosses a
    cushion beside the pocket before it enters the pocket's circle."""
    extra_seen = set()
    for _, _, deg, w in random_shots(1500, 2, anywhere=False):
        k, m, _ = corner_shot(A, B, deg, w)
        _, cushions, _ = simulate(0.0, 0.0, deg, w)
        base = math.ceil(k / 2) - 1 + m - 1
        assert cushions - base in (0, 1)
        extra_seen.add(cushions - base)
    assert extra_seen == {0, 1}
    k, m, _ = corner_shot(A, B, 37, 9)
    assert math.ceil(k / 2) - 1 + m - 1 == simulate(0.0, 0.0, 37, 9)[1] == 3


def test_separate_widths_follow_up():
    rnd = random.Random(3)
    for _ in range(1500):
        deg = rnd.uniform(0.2, 89)
        wm = rnd.uniform(1, 10)
        wc = rnd.uniform(1, 2 * wm)
        if max(wc, wm) >= B * math.cos(math.radians(deg)):
            continue
        got = simulate(0.0, 0.0, deg, wc, wm)[0]
        assert got not in ((0, 0), (2, 0)), (deg, wc, wm)
    assert simulate(0.0, 0.0, 0.5, 9, 1)[0] == (2, 0)          # the page's 0.5 degree shot
    assert "\\( w_c \\le 2 w_m \\)" in PAGE


# --- part d ------------------------------------------------------------------------------------

def test_part_d_centre():
    x0, y0 = q0080.D_START
    k, m, pocket, steps = q0080.general_shot(x0, y0, q0080.D_TAN)
    assert (k, m, pocket) == (4, 4, (0, 0))
    assert [(s[0], s[1]) for s in steps] == [(0, -120), (1, 90), (2, 300), (3, 510), (4, 720)]
    assert [round(s[3], 2) for s in steps[2:]] == [39.05, 19.52, 0]
    deg = math.degrees(math.atan2(7, 6))
    assert find_pocket(A, B, deg, 9, 180, 90) == (0, 0)
    sim = simulate(180.0, 90.0, deg, 9)
    assert sim[:2] == ((0, 0), 4)
    hits, _ = q0080.part_d_path()
    assert [(float(x), float(y)) for x, y in hits] == [(1800 / 7, 180.0), (360.0, 60.0), (2160 / 7, 0.0), (1080 / 7, 180.0)]
    assert "\\( y_k = 90 + 210(k - 1) \\)" in PAGE


def test_part_d_never():
    # from (180, 45) at 45 degrees: s = 1, c = -0.75, ||c|| = 0.25 > eps
    eps = 9 / (2 * B * math.cos(math.radians(45)))
    assert round(eps, 3) == 0.035
    assert q0080.general_shot(Fr(180), Fr(45), Fr(1)) is None
    assert find_pocket(A, B, 45, 9, 180, 45, max_k=10000) is None
    assert simulate(180.0, 45.0, 45, 9, max_bounces=2000)[0] is None


def find_pocket_source(a, b, alpha_deg, w, x0=0.0, y0=0.0, max_k=10**5):
    """The source's version: from the line after the ball, the distance to the whole line."""
    alpha = math.radians(alpha_deg)
    tan_a, cos_a = math.tan(alpha), math.cos(alpha)
    k = math.floor(2 * x0 / a) + 1
    while k <= max_k:
        y_k = y0 + (k * a / 2 - x0) * tan_a
        m = round(y_k / b)
        if abs(y_k - m * b) * cos_a < w / 2:
            return ([0, a / 2, a, a / 2][k % 4], b if m % 2 else 0)
        k += 1
    return None


def test_part_d_against_the_simulation():
    bad_source = 0
    shots = random_shots(3000, 4)
    for x0, y0, deg, w in shots:
        got = find_pocket(A, B, deg, w, x0, y0, max_k=20000)
        sim = simulate(x0, y0, deg, w)
        assert (None if got is None else index_of(got)) == sim[0], (x0, y0, deg, w)
        if find_pocket_source(A, B, deg, w, x0, y0) != got:
            bad_source += 1
    assert bad_source > 0
    # the trap's two shots
    assert simulate(2.0, 170.0, 80, 9)[0] == (0, 1) and find_pocket(A, B, 80, 9, 2, 170) == (0, 180)
    assert find_pocket_source(A, B, 80, 9, 2, 170) != (0, 180)
    assert find_pocket_source(A, B, 60, 9, 179, 5) == (180, 0)
    assert simulate(179.0, 5.0, 60, 9)[0] != (1, 0) and find_pocket(A, B, 60, 9, 179, 5) != (180, 0)
    assert math.hypot(1, 5) > 4.5 and math.hypot(2, 10) > 4.5          # neither starts in a pocket
    # the source's own random check, as the owner was told: 21 of 3651
    assert "21 מתוך 3651" in PAGE


def test_ball_radius_follow_up():
    assert (A - 2 * 2.625, B - 2 * 2.625) == (354.75, 174.75)
    assert "354.75 על 174.75" in PAGE


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(80)
    # every attribute of the figures is closed where it should be (a quote in ס"מ broke one)
    for block in q0080.blocks():
        for tag in re.findall(r"<[a-z]+ [^<>]*>", block):
            assert re.fullmatch(r'<[a-z]+( [a-zA-Z0-9-]+="[^"]*")*/?>', tag), tag[:80]


# --- the box -----------------------------------------------------------------------------------

def test_explorer_matches_the_simulation():
    from page_tests import explorer_require, node_json

    rnd = random.Random(80)
    cases = []
    while len(cases) < 400:
        rho = rnd.choice([0, 2.625])
        wc = rnd.uniform(1, 20)
        wm = rnd.choice([wc, rnd.uniform(1, 20)])
        deg = rnd.uniform(0, 360)
        x0, y0 = rnd.uniform(rho, A - rho), rnd.uniform(rho, B - rho)
        aa, bb = A - 2 * rho, B - 2 * rho
        if min(math.hypot(x0 - rho - i * aa / 2, y0 - rho - j * bb) for i in range(3) for j in range(2)) < max(wc, wm) / 2:
            continue
        cases.append(dict(x0=x0, y0=y0, deg=deg, wc=wc, wm=wm, rho=rho))
    presets = [dict(x0=0, y0=0, deg=36.87, wc=9, wm=9, rho=0), dict(x0=0, y0=0, deg=37, wc=9, wm=9, rho=0),
               dict(x0=0, y0=0, deg=37, wc=1, wm=1, rho=0), dict(x0=0, y0=0, deg=45, wc=9, wm=9, rho=0),
               dict(x0=180, y0=90, deg=49.4, wc=9, wm=9, rho=0), dict(x0=180, y0=45, deg=45, wc=9, wm=9, rho=0),
               dict(x0=0, y0=0, deg=0.5, wc=9, wm=1, rho=0), dict(x0=100, y0=100, deg=90, wc=9, wm=9, rho=0),
               dict(x0=180, y0=100, deg=270, wc=9, wm=9, rho=0)]
    import json
    got = node_json(f"const m = {explorer_require()};"
                    f"const cs = {json.dumps(cases + presets)};"
                    "console.log(JSON.stringify(cs.map((c) => { const r = m.bilShot(c);"
                    " return { p: r.pocket && [r.pocket.i, r.pocket.j], n: r.cushions, T: r.T, K: r.hit && r.hit.k, m: r.hit && r.hit.m,"
                    " end: r.end, walls: r.cross.filter((e) => e.t < r.T).map((e) => e.wall) }; })));")
    for c, r in zip(cases + presets, got):
        sim = simulate(c["x0"], c["y0"], c["deg"], c["wc"], c["wm"], rho=c["rho"])
        if r["p"] is None:
            assert sim[0] is None, c
            continue
        assert tuple(r["p"]) == sim[0], c
        assert r["n"] == sim[1], c
        assert math.isclose(r["T"], sim[2], rel_tol=1e-6, abs_tol=1e-6), c
    by = dict(zip(range(len(presets)), got[len(cases):]))
    assert by[0]["p"] == [0, 1] and by[0]["n"] == 3 and by[0]["walls"] == ["top", "right", "bottom"]
    assert by[1]["p"] == [0, 1] and (by[1]["K"], by[1]["m"]) == (4, 3)
    assert (by[2]["K"], by[2]["m"]) == (211, 159)
    assert by[3]["p"] == [1, 1] and by[3]["n"] == 0
    assert by[4]["p"] == [0, 0] and by[4]["walls"] == ["top", "right", "bottom", "top"]
    assert by[5]["p"] is None
    assert by[6]["p"] == [2, 0]
    assert by[7]["p"] is None and by[8]["p"] == [1, 0]
