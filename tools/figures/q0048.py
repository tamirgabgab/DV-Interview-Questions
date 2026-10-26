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

blocks() returns, in page order: the problem with a path that is not the shortest (the
statement), its legend, the unfolding of part a (a = H/3, b = 2H/3), the unfolding of part
b (a = 0, b = H) and their legend. tests/0048 checks the numbers and that the page copies
match.
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


def blocks():
    """The generated blocks, in page order."""
    return [
        problem_svg(),
        problem_legend(),
        part_a_svg(),
        part_b_svg(),
        unfold_legend(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
