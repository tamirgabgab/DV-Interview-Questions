#!/usr/bin/env python3
"""Figures of question 0048 (the farmer, the food and the water).

    python tools/figures/fill.py 48        # put the blocks on the page

The water line is y = 0 and the food line y = H. The farmer A stands at (0, a) and the cow
B at (L, b), with 0 <= a, b <= H. The farmer walks to the food line, then to the water line,
then to the cow; x, y and w are the horizontal parts of the three legs (x + y + w = L) and
z1, z2, z3 their lengths. Reflecting B through the water line gives B' = (L, -b), and B'
through the food line gives B'' = (L, 2H + b): every path has the length of a broken line
from A to B'', so the shortest one is the straight line, of length sqrt(L^2 + D^2) with
D = 2H + b - a.

Part c tilts the food line: it passes through (0, H) at an angle theta above the
horizontal (0 to 60 degrees), and meets the water line at O = (-H / tan theta, 0), left of
A. Both lines are rays from O. The two reflections are a rotation by 2 theta about O, so
B2 = (0, H) + R(2 theta)(L, H + b), and the shortest path is |A B2|: seen from O the
straight line from A to B2 turns by 2 theta + beta - alpha <= 3 theta <= 180 degrees, so it
crosses the food line and then the image of the water line, and the reflection is valid
for every theta up to 60 degrees (tilted() and tilted_cs()).

blocks() returns: the problem with a path that is not the shortest (the statement), its
legend, the unfolding of part a (a = H/3, b = 2H/3), the unfolding of part b (a = 0,
b = H), their legend; then part c with theta = 15 degrees: its statement, its legend, the
unfolding with the rotation about O, its legend and the table of the three legs.
tests/0048 checks the numbers and that the page copies match.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from q0030 import Net  # noqa: E402

L0, H0 = 7, 3                             # the drawings' rectangle (part a then has whole numbers)


# --- the math ---------------------------------------------------------------------------

def shortest(L, H, a, b):
    """Part a: the stops and the length of the shortest path, exact for Fractions.
    Returns dict(x, y, w, z1, z2, z3, z, D) (the z's as floats, D = 2H + b - a)."""
    L, H, a, b = map(Fr, (L, H, a, b))
    D = 2 * H + b - a
    x, y, w = L * (H - a) / D, L * H / D, L * b / D
    z1, z2, z3 = math.hypot(x, H - a), math.hypot(y, H), math.hypot(w, b)
    return {"x": x, "y": y, "w": w, "D": D, "z1": z1, "z2": z2, "z3": z3, "z": math.hypot(L, D)}


def heights(L, H, x, y):
    """Part b: the heights (a, b) whose shortest path stops after x and x + y, or None when
    there are none (the stops are valid when 0 <= x <= y and 0 <= w <= y)."""
    L, H, x, y = map(Fr, (L, H, x, y))
    w = L - x - y
    if y <= 0 or x < 0 or w < 0 or x > y or w > y:
        return None
    return H * (1 - x / y), H * w / y


def length(L, H, a, b, p1, p2):
    """The length of the path that takes food at p1 and water at p2 (horizontal positions)."""
    return math.hypot(p1, H - a) + math.hypot(p2 - p1, H) + math.hypot(L - p2, b)


TH0 = 15                                  # part c's example: L = 7, H = 3, a = 1, b = 2, theta = 15


def reflect(p, q, c, s):
    """The point p reflected through the line through q with direction (c, s), c^2 + s^2 = 1:
    move q to the origin, flip y, rotate by twice the angle."""
    dx, dy = p[0] - q[0], -(p[1] - q[1])
    c2, s2 = c * c - s * s, 2 * c * s
    return (q[0] + c2 * dx - s2 * dy, q[1] + s2 * dx + c2 * dy)


def tilted_cs(L, H, a, b, c, s):
    """Part c with cos theta = c and sin theta = s (Fractions give exact values): B1, B2, the
    food stop P (at distance sf from (0, H) along the food line), the water stop Q, the image
    Qs of Q in the food line, the square of the length z_sq (the legs and z as floats)."""
    c2, s2 = c * c - s * s, 2 * c * s
    u, v = H + b, H - a
    B1 = (L, -b)
    B2 = (L * c2 - u * s2, H + L * s2 + u * c2)
    z_sq = B2[0] ** 2 + (B2[1] - a) ** 2
    sf = v * (L * c2 - u * s2) / (L * s + (2 * H + b - a) * c)
    P = (sf * c, H + sf * s)
    qx = P[0] + (L - P[0]) * P[1] / (P[1] + b)
    Q = (qx, 0 * qx)
    Qs = reflect(Q, (0, H), c, s)
    legs = (math.dist((0, a), P), math.dist(P, Q), math.dist(Q, (L, b)))
    return {"B1": B1, "B2": B2, "z_sq": z_sq, "sf": sf, "P": P, "Q": Q, "Qs": Qs,
            "z1": legs[0], "z2": legs[1], "z3": legs[2], "z": math.sqrt(z_sq)}


def tilted(L, H, a, b, theta):
    """Part c in floats, theta in degrees, with the meeting point O (None at theta = 0), the
    angles alpha and beta of A and B seen from O and the turn 2 theta + beta - alpha of the
    straight line, in degrees (the reflection is valid when it is at most 180)."""
    t = math.radians(theta)
    r = tilted_cs(*map(float, (L, H, a, b)), math.cos(t), math.sin(t))
    if theta == 0:
        r.update(O=None, alpha=0.0, beta=0.0, turn=0.0)
    else:
        ox = -H / math.tan(t)
        al, be = math.degrees(math.atan2(a, -ox)), math.degrees(math.atan2(b, L - ox))
        r.update(O=(ox, 0.0), alpha=al, beta=be, turn=2 * theta + be - al)
    return r


def tilted_length(L, H, a, b, theta, sf, qx):
    """The length of the path that takes food at distance sf from (0, H) along the tilted food
    line and water at (qx, 0)."""
    t = math.radians(theta)
    P = (sf * math.cos(t), H + sf * math.sin(t))
    return math.dist((0, a), P) + math.dist(P, (qx, 0)) + math.hypot(L - qx, b)


# --- drawings ---------------------------------------------------------------------------

def lines(n, x_lo, x_hi, levels):
    """The food and water lines (and their images) at the given heights, dashed."""
    for v, cls in levels:
        n.line(x_lo, v, x_hi, v, cls, 3, "9 6")
    return n


def problem_svg():
    """The statement: the strip, A and B, and a path that is not the shortest, with x, y, w,
    z1, z2, z3, a, b, H and L."""
    L, H, a, b = L0, H0, Fr(1), Fr(2)
    p1, p2 = Fr(3), Fr(5)                 # a path with x = 3, y = 2, w = 2 (not the shortest)
    n = Net(-1.6, L + 1.6, -1.6, H + 0.5, 54, pad=(14, 12, 14, 6),
            label="שני קווים אופקיים במרחק H זה מזה : קו האוכל למעלה וקו המים למטה. החוואי A בגובה a מעל קו המים "
                  "והפרה B בגובה b, במרחק אופקי L. מסלול לדוגמה : מ-A לקו האוכל (z1, התקדמות אופקית x), משם לקו המים "
                  "(z2, התקדמות y) ומשם לפרה (z3, התקדמות w)", max_rem=30)
    n.rect(0, L, 0, H, "box-face")
    lines(n, -1.2, L + 1.2, [(0, "s1-line"), (H, "s3-line")])
    # the path
    n.line(0, a, p1, H, "box-path", 3).line(p1, H, p2, 0, "box-path", 3).line(p2, 0, L, b, "box-path", 3)
    n.label(p1 / 2, (a + H) / 2, "z1", dx=-12, dy=-4, size=17)
    n.label((p1 + p2) / 2, H / 2, "z2", dx=16, dy=-4, size=17)
    n.label((p2 + L) / 2, b / 2, "z3", dx=-10, dy=-8, size=17)
    # horizontal parts under the water line
    for lo, hi, s in ((0, p1, "x"), (p1, p2, "y"), (p2, L, "w")):
        n.line(lo, -0.45, hi, -0.45, "ink-line", 1.2)
        n.line(lo, -0.3, lo, -0.6, "ink-line", 1.2).line(hi, -0.3, hi, -0.6, "ink-line", 1.2)
        n.label((lo + hi) / 2, -0.45, s, dy=-6, size=16)
    n.line(0, -1.15, L, -1.15, "ink-line", 1.2).line(0, -1.0, 0, -1.3, "ink-line", 1.2).line(L, -1.0, L, -1.3, "ink-line", 1.2)
    n.label(L / 2, -1.15, "L", dy=-6, size=16)
    # heights: a and H on the left, b on the right
    n.line(-0.35, 0, -0.35, a, "ink-line", 1.2).label(-0.35, a / 2, "a", dx=-10, dy=5, size=16)
    n.line(-1.0, 0, -1.0, H, "ink-line", 1.2).label(-1.0, H / 2, "H", dx=-10, dy=5, size=16)
    n.line(L + 0.35, 0, L + 0.35, b, "ink-line", 1.2).label(L + 0.35, b / 2, "b", dx=10, dy=5, size=16)
    # stops and the two people
    n.point(p1, H, "s3", r=6, title="נקודת האוכל")
    n.point(p2, 0, "s1", r=6, title="נקודת המים")
    n.point(0, a, "ink", "A", dx=14, dy=-8, r=6, title="החוואי A")
    n.point(L, b, "s2", "B", dx=-14, dy=-8, r=6, title="הפרה B")
    return n.svg()


def problem_legend():
    return ('<span class="viz-legend"><span><i class="s3"></i>קו האוכל</span><span><i class="s1"></i>קו המים</span>'
            '<span><i class="ink"></i>החוואי A</span><span><i class="s2"></i>הפרה B</span>'
            '<span><i class="box-path"></i>מסלול לדוגמה, לא הקצר ביותר</span></span>')


def unfold_svg(a, b, label, legs):
    """The unfolding: the strip, its reflection below through the water line (with B') and
    two reflections above (with B''); the shortest path, the straight line from A to B'',
    the big right triangle and the three small triangles along it. legs names the six legs
    (x, H - a, y, H, w, b) as they are labelled."""
    L, H = L0, H0
    s = shortest(L, H, a, b)
    D, x, y = s["D"], s["x"], s["y"]
    p1, p2 = x, x + y
    n = Net(-2.3, L + 3.6, -H - 0.3, 3 * H + 0.5, 36, pad=(8, 10, 8, 8), label=label, max_rem=26)
    n.rect(0, L, -H, 0, "box-copy").rect(0, L, 0, H, "box-face").rect(0, L, H, 2 * H, "box-copy").rect(0, L, 2 * H, 3 * H, "box-copy")
    lines(n, -0.4, L + 0.4, [(-H, "s3-line"), (0, "s1-line"), (H, "s3-line"), (2 * H, "s1-line"), (3 * H, "s3-line")])
    for v, t in ((-H, "−H"), (0, "0"), (H, "H"), (2 * H, "2H"), (3 * H, "3H")):
        n.label(-0.55, v, t, dy=5, size=14, anchor="end")
    # the real path, and its reflected legs as the straight line
    n.line(0, a, p1, H, "box-path", 3).line(p1, H, p2, 0, "box-path", 3).line(p2, 0, L, b, "box-path", 3)
    n.line(p2, 0, L, -b, "ink-line", 1.5, "4 3")                    # the last leg reflected to B'
    n.line(0, a, L, 2 * H + b, "box-path", 3, "8 5")
    # the reflections of the cow
    n.line(L, b, L, -b, "ink-line", 1, "2 3")
    # the big triangle: legs L and D
    n.line(0, a, L, a, "ink-line", 1.2).line(L, a, L, 2 * H + b, "ink-line", 1.2)
    n.label(L / 2, a, "L", dy=18, size=15)
    # the small triangles: horizontal and vertical legs, the hypotenuses z1, z2, z3
    corners = [((0, a), (p1, a), (p1, H)), ((p1, H), (p2, H), (p2, 2 * H)), ((p2, 2 * H), (L, 2 * H), (L, 2 * H + b))]
    for i, ((x0, y0), (x1, _), (_, y1)) in enumerate(corners):
        n.line(x0, y0, x1, y0, "ink-line", 1, "3 3").line(x1, y0, x1, y1, "ink-line", 1, "3 3")
        n.label((x0 + x1) / 2, y0, legs[2 * i], dy=-5, size=13)
        n.label(x1, (y0 + y1) / 2, legs[2 * i + 1], dx=5, dy=5, size=13, anchor="start")
        n.label((x0 + x1) / 2, (y0 + y1) / 2, f"z{i + 1}", dx=-8, dy=-4, size=15, anchor="end")
    n.line(L + 0.7, a, L + 0.7, 2 * H + b, "ink-line", 1.2)
    n.line(L + 0.55, a, L + 0.85, a, "ink-line", 1.2).line(L + 0.55, 2 * H + b, L + 0.85, 2 * H + b, "ink-line", 1.2)
    n.label(L + 0.7, (a + 2 * H + b) / 2, "2H + b − a", dx=6, dy=5, size=14, anchor="start")
    n.point(p1, H, "s3", r=5, title="נקודת האוכל").point(p2, 0, "s1", r=5, title="נקודת המים")
    n.point(p2, 2 * H, "s1", r=4, title="נקודת המים אחרי השיקוף")
    n.point(0, a, "ink", "A", dx=-12, dy=-6, r=6, title="החוואי A")
    n.point(L, b, "s2", "B", dx=12, dy=-6, r=6, title="הפרה B")
    n.point(L, -b, "ink", "B′", dx=14, dy=16, r=4, title="B′ : השיקוף של B דרך קו המים")
    n.point(L, 2 * H + b, "s2", "B″", dx=0, dy=-12, r=6, title="B″ : השיקוף של B′ דרך קו האוכל")
    return n.svg()


def part_a_svg():
    return unfold_svg(Fr(1), Fr(2),
                      "סעיף א עם H = 3, a = 1, b = 2, L = 7 : הרצועה, השיקוף שלה למטה דרך קו המים עם B′, ושני שיקופים "
                      "למעלה עם B″ בגובה 2H + b = 8. הקו הישר מ-A ל-B″ חוצה את קו האוכל ואת השיקוף של קו המים בנקודות "
                      "העצירה. הוא היתר של משולש ישר זווית עם ניצבים L ו-2H + b − a, ושלושת המשולשים הקטנים לאורכו "
                      "דומים לו",
                      ["x", "H − a", "y", "H", "w", "b"])


def part_b_svg():
    return unfold_svg(Fr(0), Fr(3),
                      "סעיף ב עם H = 3, a = 0, b = 3, L = 7 : החוואי על קו המים והפרה על קו האוכל. B″ בגובה 3H, והקו "
                      "הישר מ-A אליו חוצה את קו האוכל ואת השיקוף של קו המים בשליש ובשני שלישים מהדרך : שלושה משולשים "
                      "חופפים עם ניצבים L/3 ו-H",
                      ["L/3", "H", "L/3", "H", "L/3", "H"])


def unfold_legend():
    return ('<span class="viz-legend"><span><i class="s3"></i>קו האוכל ושיקופיו</span><span><i class="s1"></i>קו המים ושיקופיו</span>'
            '<span><i class="box-face"></i>השטח עצמו</span><span><i class="box-copy"></i>השיקופים שלו</span>'
            '<span><i class="box-path"></i>המסלול הקצר ביותר, והקו הישר מ-A ל-B″</span></span>')


# --- part c: the tilted food line ---------------------------------------------------------

def clip(poly, q, d, keep_left):
    """The convex polygon cut by the line through q with direction d: the part on its left
    (keep_left) or on its right (Sutherland-Hodgman)."""
    side = lambda p: (d[0] * (p[1] - q[1]) - d[1] * (p[0] - q[0])) * (1 if keep_left else -1)
    out = []
    for i, p in enumerate(poly):
        r = poly[i - 1]
        sp, sr = side(p), side(r)
        if (sp >= 0) != (sr >= 0):
            k = sr / (sr - sp)
            out.append((r[0] + k * (p[0] - r[0]), r[1] + k * (p[1] - r[1])))
        if sp >= 0:
            out.append(p)
    return out


def ray_end(o, d, box):
    """Where the ray from o in direction d leaves the rectangle box = (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    ts = [(x1 - o[0]) / d[0] if d[0] > 1e-12 else math.inf, (x0 - o[0]) / d[0] if d[0] < -1e-12 else math.inf,
          (y1 - o[1]) / d[1] if d[1] > 1e-12 else math.inf, (y0 - o[1]) / d[1] if d[1] < -1e-12 else math.inf]
    t = min(ts)
    return (o[0] + t * d[0], o[1] + t * d[1])


def polygon(n, pts, cls):
    n.add(f'<polygon class="{cls}" points="{" ".join(f"{n.X(x):.1f},{n.Y(y):.1f}" for x, y in pts)}"/>')
    return n


def arc(n, o, r, a0, a1, cls="farm-arc", width=1.5, dash=None):
    """An arc about o of radius r (units) from angle a0 to a1 (degrees, counterclockwise)."""
    p0 = (o[0] + r * math.cos(math.radians(a0)), o[1] + r * math.sin(math.radians(a0)))
    p1 = (o[0] + r * math.cos(math.radians(a1)), o[1] + r * math.sin(math.radians(a1)))
    R = r * n.scale
    d = f' stroke-dasharray="{dash}"' if dash else ""
    n.add(f'<path class="{cls}" d="M {n.X(p0[0]):.1f} {n.Y(p0[1]):.1f} A {R:.1f} {R:.1f} 0 0 0 {n.X(p1[0]):.1f} '
          f'{n.Y(p1[1]):.1f}" stroke-width="{width}"{d}/>')
    return n


def wedge(o, k0, k1, theta, box):
    """The copy of the field between the rays from o at angles k0 theta and k1 theta, inside box."""
    x0, x1, y0, y1 = box
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    t0, t1 = math.radians(k0 * theta), math.radians(k1 * theta)
    poly = clip(poly, o, (math.cos(t0), math.sin(t0)), True)
    return clip(poly, o, (math.cos(t1), math.sin(t1)), False)


def tilt_problem_svg():
    """Part c's statement: the wedge between the water line and the tilted food line, from
    their meeting point O, with A, B, the heights a, b and H, the angle theta and a path."""
    L, H, a, b, th = L0, H0, 1, 2, TH0
    t = math.radians(th)
    o = (-H / math.tan(t), 0.0)
    box = (o[0], L + 0.9, -0.1, H + (L + 0.9) * math.tan(t))
    n = Net(o[0] - 0.6, L + 1.5, -1.5, box[3] + 0.4, 26, pad=(10, 10, 10, 6), max_rem=32,
            label="סעיף ג : קו המים אופקי, וקו האוכל עובר דרך (0, H) ונוטה כלפי מעלה בזווית θ. הקווים נפגשים "
                  "בנקודה O משמאל לחוואי ומתרחקים זה מזה לכיוון הפרה. החוואי A בגובה a על הקו x = 0, הפרה B "
                  "בגובה b על הקו x = L, ומסלול לדוגמה : מ-A לקו האוכל, משם לקו המים ומשם לפרה")
    polygon(n, [o, (box[1], 0), (box[1], box[3])], "box-face")
    n.line(o[0], 0, box[1] + 0.4, 0, "s1-line", 3, "9 6")
    n.line(o[0], 0, box[1] + 0.4, H + (box[1] + 0.4) * math.tan(t), "s3-line", 3, "9 6")
    arc(n, o, 3.2, 0, th)
    n.label(o[0] + 3.6 * math.cos(t / 2), 3.6 * math.sin(t / 2), "θ", dx=6, dy=5, size=16, anchor="start")
    n.line(0, 0, 0, H, "ink-line", 1, "2 3").line(L, 0, L, H + L * math.tan(t), "ink-line", 1, "2 3")
    # a path that is not the shortest: food at x = 3, water at x = 5
    pf = (3, H + 3 * math.tan(t))
    n.line(0, a, *pf, "box-path", 3).line(*pf, 5, 0, "box-path", 3).line(5, 0, L, b, "box-path", 3)
    n.line(-0.35, 0, -0.35, a, "ink-line", 1.2).label(-0.35, a / 2, "a", dx=-8, dy=5, size=15, anchor="end")
    n.line(-1.1, 0, -1.1, H, "ink-line", 1.2).label(-1.1, H / 2, "H", dx=-8, dy=5, size=15, anchor="end")
    n.line(L + 0.35, 0, L + 0.35, b, "ink-line", 1.2).label(L + 0.35, b / 2, "b", dx=8, dy=5, size=15, anchor="start")
    n.line(0, -0.55, L, -0.55, "ink-line", 1.2).line(0, -0.4, 0, -0.7, "ink-line", 1.2).line(L, -0.4, L, -0.7, "ink-line", 1.2)
    n.label(L / 2, -0.55, "L", dy=17, size=15)
    n.point(*pf, "s3", r=5, title="נקודת האוכל").point(5, 0, "s1", r=5, title="נקודת המים")
    n.point(*o, "ink", "O", dx=0, dy=20, r=5, title="O : נקודת המפגש של הקווים, (−H/tanθ, 0)")
    n.point(0, a, "ink", "A", dx=13, dy=-7, r=6, title="החוואי A = (0, a)")
    n.point(L, b, "s2", "B", dx=-13, dy=-7, r=6, title="הפרה B = (L, b)")
    return n.svg()


def tilt_problem_legend():
    return ('<span class="viz-legend"><span><i class="s3"></i>קו האוכל, בזווית θ</span><span><i class="s1"></i>קו המים</span>'
            '<span><i class="box-face"></i>השטח בין הקווים</span><span><i class="ink"></i>החוואי A ונקודת המפגש O</span>'
            '<span><i class="s2"></i>הפרה B</span><span><i class="box-path"></i>מסלול לדוגמה, לא הקצר ביותר</span></span>')


def tilt_unfold_svg():
    """Part c's unfolding: the field, its copy through the water line (with B1) and two copies
    through the food line (the image of the water line at 2 theta, B2 at 2 theta + beta); the
    rotation of B about O by 2 theta, the straight line from A to B2 and the real path."""
    L, H, a, b, th = L0, H0, 1, 2, TH0
    r = tilted(L, H, a, b, th)
    o, B1, B2, P, Q, Qs = r["O"], r["B1"], r["B2"], r["P"], r["Q"], r["Qs"]
    box = (o[0], L + 0.8, -2.9, 12.0)
    n = Net(o[0] - 0.7, L + 1.5, box[2] - 0.5, box[3] + 0.3, 24, pad=(10, 10, 10, 8), max_rem=30,
            label="סעיף ג עם L = 7, H = 3, a = 1, b = 2, θ = 15° : השטח בין הקווים, השיקוף שלו דרך קו המים עם B1, "
                  "ושני שיקופים דרך קו האוכל, עם תמונת קו המים בזווית 2θ ועם B2. B2 הוא B מסובב ב-2θ = 30° סביב O. "
                  "הקו הישר מ-A ל-B2 חוצה את קו האוכל בנקודת האוכל ואת תמונת קו המים בתמונה של נקודת המים")
    for k0, k1, cls in ((-1, 0, "box-copy"), (0, 1, "box-face"), (1, 2, "box-copy"), (2, 3, "box-copy")):
        polygon(n, wedge(o, k0, k1, th, box), cls)
    for k, cls, w in ((-1, "s3-line", 2), (0, "s1-line", 3), (1, "s3-line", 3), (2, "s1-line", 2), (3, "s3-line", 2)):
        tk = math.radians(k * th)
        e = ray_end(o, (math.cos(tk), math.sin(tk)), box)
        n.line(*o, *e, cls, w, "9 6")
    # the rotation: B to B2 about O by 2 theta, and the angle theta at O
    rb = math.dist(o, (L, b))
    arc(n, o, rb, r["beta"], r["beta"] + 2 * th, "farm-arc", 1.5, "5 4")
    am = math.radians(r["beta"] + th)
    n.label(o[0] + rb * math.cos(am), rb * math.sin(am), "2θ", dx=8, dy=0, size=16, anchor="start")
    arc(n, o, 2.6, 0, th)
    n.label(o[0] + 3.0 * math.cos(math.radians(th / 2)), 3.0 * math.sin(math.radians(th / 2)), "θ", dx=4, dy=5, size=15, anchor="start")
    # the two reflections of the cow, each perpendicular to its line
    n.line(L, b, *B1, "ink-line", 1, "2 3").line(*B1, *B2, "ink-line", 1, "2 3")
    # the real path, the last leg reflected to B1, and the straight line A -> B2
    n.line(0, a, *P, "box-path", 3).line(*P, *Q, "box-path", 3).line(*Q, L, b, "box-path", 3)
    n.line(*Q, *B1, "ink-line", 1.5, "4 3")
    n.line(0, a, *B2, "box-path", 3, "8 5")
    n.point(*P, "s3", r=5, title="נקודת האוכל P").label(*P, "P", dx=-10, dy=-8, size=15, anchor="end")
    n.point(*Q, "s1", r=5, title="נקודת המים Q").label(*Q, "Q", dx=0, dy=20, size=15)
    n.point(*Qs, "s1", r=4, title="Q* : התמונה של Q דרך קו האוכל").label(*Qs, "Q*", dx=10, dy=4, size=15, anchor="start")
    n.point(*o, "ink", "O", dx=0, dy=20, r=5, title="O : נקודת המפגש של הקווים")
    n.point(0, a, "ink", "A", dx=-12, dy=-6, r=6, title="החוואי A")
    n.point(L, b, "s2", "B", dx=13, dy=-6, r=6, title="הפרה B")
    n.point(*B1, "ink", "B1", dx=16, dy=6, r=4, title="B1 : השיקוף של B דרך קו המים")
    n.point(*B2, "s2", "B2", dx=0, dy=-12, r=6, title="B2 : השיקוף של B1 דרך קו האוכל, B מסובב ב-2θ סביב O")
    return n.svg()


def tilt_unfold_legend():
    return ('<span class="viz-legend"><span><i class="s3"></i>קו האוכל ושיקופיו</span><span><i class="s1"></i>קו המים ושיקופיו</span>'
            '<span><i class="box-face"></i>השטח עצמו</span><span><i class="box-copy"></i>השיקופים שלו</span>'
            '<span><i class="farm-arc"></i>הסיבוב של B סביב O</span>'
            '<span><i class="box-path"></i>המסלול הקצר ביותר, והקו הישר מ-A ל-B2</span></span>')


def tilt_table():
    """Part c's example: the three legs, each with the point it ends at and its length, and the
    straight line A -> B2 that they add up to (A = (0, 1) is where the first leg starts)."""
    L, H, a, b = L0, H0, 1, 2
    r = tilted(L, H, a, b, TH0)
    rows = [("מהחוואי \\( A \\) לאוכל", "P", r["P"], "z1", r["z1"]), ("מהאוכל למים", "Q", r["Q"], "z2", r["z2"]),
            ("מהמים לפרה", "B", (L, b), "z3", r["z3"]), ("הקו הישר מ-\\( A \\) ל-\\( B_2 \\)", "B2", r["B2"], "z", r["z"])]
    out = ["| הקטע | עד הנקודה | האורך |", "|---|:-:|:-:|"]
    for name, pn, q, zn, z in rows:
        out.append(f'| {name} | ‏<span dir="ltr">{pn} = ({q[0]:.2f}, {q[1]:.2f})</span> | ‏<span dir="ltr">{zn} ≈ {z:.3f}</span> |')
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [
        problem_svg(),
        problem_legend(),
        part_a_svg(),
        part_b_svg(),
        unfold_legend(),
        tilt_problem_svg(),
        tilt_problem_legend(),
        tilt_unfold_svg(),
        tilt_unfold_legend(),
        tilt_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
