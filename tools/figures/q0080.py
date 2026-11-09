#!/usr/bin/env python3
"""Figures and tables of question 0080 (which pocket does the ball enter: a billiard table,
the unfolding of the table and the approximation of a slope by fractions).

    python tools/figures/fill.py 80        # put the blocks on the page

The table is A x B = 360 x 180 cm with the corner (0, 0) at the origin. A ball moves on a
straight line at the angle alpha above the x axis and bounces like light. Unfolding the
table (reflecting the table, not the ball, at every cushion) turns the path into the
straight line y = y0 + (x - x0) tan(alpha) over a grid of table copies, whose pocket
points are (k A/2, m B): even k the corners, odd k the middle pockets. The real point of an
unfolded one is fold(): x mod 2A, mirrored when it passes A (the same for y).

Parts a and b have point pockets at the four corners only: from (0, 0) the ball enters the
corner (p A, q B) of the first grid point on its line, r = A tan(alpha) / B = q / p in
lowest terms, after p + q - 2 cushions. Part c gives the six pockets a width W and asks for
the first k with ||k s|| < eps, s = A tan(alpha) / (2B), eps = W / (2B cos(alpha)). Part d
starts anywhere. Everything here is exact (Fractions) for a rational tan(alpha); the
37 degree example is a float.

blocks() returns, in page order: the statement's table, part a's path and its trace, the
unfolding of part a and its legend, part b's examples, part c's six cases, the steps of the
37 degree shot, part c's unfolded grid with the pockets and its legend, part d's path from
the centre, its steps and the legend of the paths. tests/0080 recomputes every value and
checks the page copies against this generator.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from q0030 import Net, text  # noqa: E402

A, B = 360, 180          # the table, cm (a snooker table, rounded: 357 x 178)
W = 9                    # the pocket width of parts c and d, cm

# the six pockets by their real point, and their names on the page
NAMES = {(0, 0): "הפינה השמאלית התחתונה", (A // 2, 0): "הכיס האמצעי התחתון", (A, 0): "הפינה הימנית התחתונה",
         (0, B): "הפינה השמאלית העליונה", (A // 2, B): "הכיס האמצעי העליון", (A, B): "הפינה הימנית העליונה"}
WALL = {"top": "דופן העליונה", "bottom": "דופן התחתונה", "left": "דופן השמאלית", "right": "דופן הימנית"}   # after "ב"


# --- the math ----------------------------------------------------------------------------------

def fold(v, length):
    """The real coordinate of an unfolded one: reflected at every multiple of length."""
    v = v % (2 * length)
    return 2 * length - v if v > length else v


def point_pocket(tan: Fr, a=A, b=B):
    """Parts a and b, from (0, 0) with point pockets at the corners: r = q/p, the pocket and the
    number of cushions."""
    r = Fr(a) * tan / b
    p, q = r.denominator, r.numerator
    return r, p, q, (a if p % 2 else 0, b if q % 2 else 0), p + q - 2


def trace(tan: Fr, a=A, b=B):
    """Part a by hand: the segments of the path from (0, 0) to its corner pocket, each as
    (from, to, what happens there): the crossings of the grid lines x = j a and y = i b by the
    unfolded line y = x tan, folded back onto the table."""
    _, p, q, pocket, _ = point_pocket(tan, a, b)
    xs = {Fr(j * a): "v" for j in range(1, p)}
    for i in range(1, q):
        xs[Fr(i * b) / tan] = "h"
    out, prev = [], (Fr(0), Fr(0))
    for x in sorted(xs):
        y = x * tan
        pt = (fold(x, a), fold(y, b))
        j = x / a if xs[x] == "v" else y / b
        wall = ("right" if j % 2 else "left") if xs[x] == "v" else ("top" if j % 2 else "bottom")
        out.append((prev, pt, wall))
        prev = pt
    out.append((prev, (Fr(pocket[0]), Fr(pocket[1])), "pocket"))
    return out


def norm(x):
    """The distance from x to the nearest whole number: ||x||."""
    return abs(x - round(x))


def corner_shot(tan, w=W, a=A, b=B):
    """Part c, from the corner (0, 0): the first k with ||k s|| < eps, and m = round(K s).
    Exact for a Fraction tan (eps compared squared), a float otherwise."""
    s = Fr(a) * tan / (2 * b) if isinstance(tan, Fr) else a * tan / (2 * b)
    k = 1
    while True:
        d = norm(k * s)
        if isinstance(tan, Fr):
            if d * d * 4 * b * b < Fr(w * w) * (1 + tan * tan):   # d < w / (2 b cos) squared
                break
        elif d < w * math.sqrt(1 + tan * tan) / (2 * b):
            break
        k += 1
    m = round(k * s)
    return k, m, pocket_of(k, m, a, b)


def pocket_of(k, m, a=A, b=B):
    """The real pocket of the grid point (k a/2, m b): k mod 4 gives x, the parity of m gives y."""
    return ((0, a // 2, a, a // 2)[k % 4], b if m % 2 else 0)


def general_shot(x0: Fr, y0: Fr, tan: Fr, w=W, a=A, b=B, kmax=10_000):
    """Part d, exactly: the first pocket the ray from (x0, y0) at slope tan (moving right) comes
    within w/2 of while approaching it. Returns (K, m, pocket, the steps checked) or None."""
    r2 = Fr(w, 2) ** 2
    k = math.floor((2 * x0 - w) / a)
    steps = []
    while k <= kmax:
        px = Fr(k * a, 2)
        yk = y0 + (px - x0) * tan
        row = math.floor(yk / b)
        best = None
        for m in (row, row + 1):
            fx, fy = px - x0, m * b - y0
            ahead = fx + fy * tan                       # along (1, tan)
            off2 = (fx * tan - fy) ** 2 / (1 + tan * tan)
            if ahead > 0 and off2 < r2:
                best = m
                break
        near = round(yk / b)
        steps.append((k, yk, near, abs(yk - near * b) / math.sqrt(1 + tan * tan)))
        if best is not None:
            return k, best, pocket_of(k, best, a, b), steps
        k += 1
    return None


def unfolded_cushions(x0, y0, tan, x_end, a=A, b=B):
    """The grid lines x = j a and y = i b the unfolded line crosses for x0 < x < x_end."""
    xs = [Fr(j * a) for j in range(math.floor(x0 / a) + 1, math.ceil(x_end / a)) if x0 < j * a < x_end]
    y_end = y0 + (x_end - x0) * tan
    ys = [Fr(i * b) for i in range(math.floor(y0 / b) + 1, math.ceil(y_end / b)) if y0 < i * b < y_end]
    return xs, ys


# --- formatting --------------------------------------------------------------------------------

def num(v, places=2):
    """40, 6.75, 0.0313, −120: no trailing zeros, a real minus sign."""
    if isinstance(v, Fr) and v.denominator == 1:
        out = str(v.numerator)
    elif isinstance(v, int):
        out = str(v)
    else:
        out = f"{float(v):.{places}f}".rstrip("0").rstrip(".")
    return out.replace("-", "−")


def frac(v: Fr) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def pt(p) -> str:
    """A point, with a no-break space so it never splits across lines."""
    return f"({num(p[0])},\u00a0{num(p[1])})"


def ltr(s: str) -> str:
    return f'<span dir="ltr">{s}</span>'


# --- drawings ----------------------------------------------------------------------------------

S = Fr(8, 5)             # px per cm on the table drawings


def table(n, x_lo=0, y_lo=0, pockets=True, r=None, hl=None):
    """The felt, the cushions and the pockets (dots, or circles of radius r cm)."""
    n.rect(x_lo, x_lo + A, y_lo, y_lo + B, "bil-felt")
    if pockets:
        for (px, py) in ([(0, 0), (A, 0), (0, B), (A, B)] if r is None else NAMES):
            cls = "bil-pocket is-in" if hl == (px, py) else "bil-pocket"
            n.add(f'<circle class="{cls}" cx="{n.X(x_lo + px):.1f}" cy="{n.Y(y_lo + py):.1f}" '
                  f'r="{(float(r) * float(n.scale) if r else 5):.1f}"><title>{NAMES[(px, py)]} {pt((px, py))}</title></circle>')
    return n


def statement_svg():
    n = Net(-62, A + 12, -26, B + 14, S, pad=(10, 8, 10, 8), max_rem=30,
            label=f"שולחן ביליארד של {A} על {B} ס״מ. הפינה השמאלית התחתונה בראשית (0, 0), ציר x לאורך השולחן "
                  "וציר y לרוחבו. הכדור יוצא מהראשית בזווית α מעל ציר x, והכיסים בארבע הפינות")
    table(n)
    n.line(0, 0, 70, 0, "ink-line", 1.2, "4 3")
    ang = math.atan2(3, 4)
    n.line(0, 0, 120 * math.cos(ang), 120 * math.sin(ang), "bil-path", 3)
    n.add(f'<path class="ink-line" d="M {n.X(46):.1f} {n.Y(0):.1f} A {46 * float(S):.1f} {46 * float(S):.1f} 0 0 0 '
          f'{n.X(46 * math.cos(ang)):.1f} {n.Y(46 * math.sin(ang)):.1f}" fill="none" stroke-width="1.2"/>')
    n.label(56, 12, "α", size=17)
    n.point(0, 0, "ink", r=6, title="הכדור בראשית (0, 0)")
    n.label(A / 2, -14, f"a = {A}", size=15)
    n.label(-14, B / 2, f"b = {B}", size=15, anchor="end")
    n.label(0, -14, "(0, 0)", size=13)
    n.label(A, B + 4, f"({A}, {B})", dy=-6, size=13, anchor="end")
    return n.svg()


def path_svg(points, hits, pocket, label, start=(0, 0), r=None, extra=""):
    """A real path: its segments, the cushion hits numbered and the pocket it enters."""
    n = Net(-16, A + 16, -16, B + 16, S, pad=(8, 8, 8, 8), max_rem=30, label=label)
    table(n, r=r, hl=pocket)
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        n.line(x0, y0, x1, y1, "bil-path", 3)
    for i, (x, y) in enumerate(hits, 1):
        dx = -12 if x >= A else 12 if x <= 0 else 0
        dy = 20 if y <= 0 else -10 if y >= B else 0
        n.point(x, y, "s1", r=5, title=f"פגיעה {i} בדופן {pt((x, y))}")
        n.label(x, y, str(i), dx=dx, dy=dy, size=15)
    n.point(start[0], start[1], "ink", r=6, title=f"הכדור יוצא מ-{pt(start)}")
    n.add(extra)
    return n.svg()


def part_a_svg():
    segs = trace(Fr(3, 4))
    pts = [segs[0][0]] + [s[1] for s in segs]
    return path_svg(pts, pts[1:-1], (0, B),
                    "סעיף א : הכדור יוצא מ-(0, 0) לכיוון (240, 180). הוא פוגע בדופן העליונה ב-(240, 180), בימנית "
                    "ב-(360, 90) ובתחתונה ב-(240, 0), ונכנס לכיס השמאלי העליון (0, 180) : שלוש פגיעות")


def part_a_table():
    rows = ["| מקטע | מנקודה | לנקודה | מה קורה שם |", "|:-:|:-:|:-:|:-:|"]
    for i, (p0, p1, what) in enumerate(trace(Fr(3, 4)), 1):
        event = f"**כניסה לכיס {ltr(pt(p1))}**" if what == "pocket" else f"פגיעה ב{WALL[what]}"
        rows.append(f"| {i} | {ltr(pt(p0))} | {ltr(pt(p1))} | {event} |")
    return "\n".join(rows)


def unfold_svg():
    """Part a unfolded: 2 x 3 copies of the table, the straight line from (0, 0) to (720, 540),
    the crossings of the grid lines (the cushion hits) and every grid point named by its real
    corner."""
    n = Net(-40, 2 * A + 30, -30, 3 * B + 22, Fr(3, 4), pad=(8, 8, 8, 8), max_rem=30,
            label="סעיף א אחרי פתיחת השולחן : שישה עותקים של השולחן, שתי עמודות ושלוש שורות. הקו הישר מ-(0, 0) "
                  "ל-(720, 540) חוצה קו אנכי אחד ושני קווים אופקיים, שלוש הפגיעות, ומגיע לנקודת הרשת (720, 540), "
                  "שהיא הפינה (0, 180) של השולחן האמיתי")
    for i in range(2):
        for j in range(3):
            n.rect(i * A, (i + 1) * A, j * B, (j + 1) * B, "bil-felt" if (i, j) == (0, 0) else "box-copy")
    for i in range(3):
        for j in range(4):
            x, y = i * A, j * B
            real = (fold(x, A), fold(y, B))
            hl = (x, y) == (2 * A, 3 * B)
            n.add(f'<circle class="bil-pocket{" is-in" if hl else ""}" cx="{n.X(x):.1f}" cy="{n.Y(y):.1f}" r="4">'
                  f'<title>{pt((x, y))} : הפינה {pt(real)}</title></circle>')
            n.label(x, y, pt(real), dx=-5 if i == 2 else 5, dy=14 if j == 0 else -6, size=12,
                    anchor="end" if i == 2 else "start")
    n.line(0, 0, 2 * A, 3 * B, "bil-path", 3)
    xs, ys = unfolded_cushions(Fr(0), Fr(0), Fr(3, 4), Fr(2 * A))
    hits = sorted([(x, x * Fr(3, 4)) for x in xs] + [(y / Fr(3, 4), y) for y in ys])
    for i, (x, y) in enumerate(hits, 1):
        n.point(x, y, "s1", r=5, title=f"חצייה {i} : פגיעה בדופן")
        n.label(x, y, str(i), dx=12, dy=4, size=14)
    n.point(0, 0, "ink", r=5, title="הכדור יוצא מ-(0, 0)")
    return n.svg()


def unfold_legend():
    return ('<span class="viz-legend"><span><i class="bil-key-felt"></i>השולחן עצמו</span>'
            '<span><i class="box-copy"></i>העותקים המשוקפים</span><span><i class="bil-path"></i>המסלול, קו ישר</span>'
            '<span><i class="s1"></i>חצייה של קו ברשת : פגיעה בדופן</span><span><i class="bil-key-pocket"></i>נקודת רשת : פינה</span></span>')


B_ROWS = [((360, 180), Fr(1, 2)), ((180, 180), Fr(1)), ((240, 180), Fr(3, 4)), ((270, 180), Fr(2, 3)),
          ((360, 120), Fr(1, 3)), ((360, 150), Fr(5, 12))]


def part_b_table():
    rows = ["| מכוונים ל- | ‏\\( \\tan\\alpha \\) | ‏\\( r = 2\\tan\\alpha \\) | ‏\\( p \\) | ‏\\( q \\) | הכיס | פגיעות |",
            "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for aim, tan in B_ROWS:
        r, p, q, pocket, hits = point_pocket(tan)
        rows.append(f"| {ltr(pt(aim))} | {ltr(frac(tan))} | {ltr(frac(r))} | {p} | {q} | {ltr(pt(pocket))} | {hits} |")
    rows.append(f"| ‏37° | {ltr('0.7536…')} | {ltr('1.5071…')} | – | – | אין | אינסוף |")
    return "\n".join(rows)


C_ROWS = [((A // 2, 0), "\\( K \\) אי־זוגי, \\( m \\) זוגי", "\\( p \\) אי־זוגי, \\( q \\) זוגי", Fr(2, 3)),
          ((A // 2, B), "\\( K \\) אי־זוגי, \\( m \\) אי־זוגי", "\\( p \\) אי־זוגי, \\( q \\) אי־זוגי", Fr(1)),
          ((A, B), "\\( K \\equiv 2 \\pmod 4 \\)", "\\( p \\equiv 2 \\pmod 4 \\)", Fr(1, 2)),
          ((0, B), "\\( K \\equiv 0 \\pmod 4 \\)", "\\( p \\equiv 0 \\pmod 4 \\)", Fr(3, 4)),
          ((A, 0), "**אף פעם**", "**אף פעם**", None),
          ((0, 0), "**אף פעם**", "**אף פעם**", None)]


def part_c_table():
    rows = ["| הכיס | נכנס כאשר | כיסים נקודתיים, \\( s = q/p \\) מצומצם | דוגמה : מכוונים ל- | ‏\\( K, m \\) ב-\\( w = 9 \\) |",
            "|:-:|:-:|:-:|:-:|:-:|"]
    for pocket, when, exact, tan in C_ROWS:
        if tan is None:
            aim = km = "–"
        else:
            k, m, got = corner_shot(tan)
            assert got == pocket
            aim, km = ltr(pt((Fr(B) / tan, B))), ltr(f"{k}, {m}")
        cell = lambda t: ("\u200f" + t) if t.startswith("\\(") else t   # RTL: a cell starts Hebrew or with RLM
        rows.append(f"| {NAMES[pocket]} {ltr(pt(pocket))} | {cell(when)} | {cell(exact)} | {aim} | {km} |")
    return "\n".join(rows)


def tan37():
    return math.tan(math.radians(37))


def eps(tan, w=W, b=B):
    return w * math.sqrt(1 + tan * tan) / (2 * b)


def steps37_table():
    t = tan37()
    e = eps(t)
    rows = ["| ‏\\( k \\) | ‏\\( k s \\) | ‏\\( \\lVert k s \\rVert \\) | קטן מ-\\( \\varepsilon \\approx " + f"{e:.4f}" + " \\)? |",
            "|:-:|:-:|:-:|:-:|"]
    k = 1
    while True:
        v = k * t
        d = norm(v)
        rows.append(f"| {k} | {ltr(f'{v:.4f}')} | {ltr(f'{d:.4f}')} | {'**כן** : ' + ltr(f'K = {k}, m = {round(v)}') if d < e else 'לא'} |")
        if d < e:
            break
        k += 1
    return "\n".join(rows)


def grid_svg():
    """Part c: the unfolded grid with the six kinds of pockets as circles of radius W/2 (to
    scale), the line of 37 degrees into the circle at (720, 540), and the line of tan = 2/3
    into the middle pocket at (540, 360)."""
    sc = Fr(3, 4)
    n = Net(-20, 2 * A + 30, -20, 3 * B + 20, sc, pad=(8, 8, 8, 8), max_rem=30,
            label="סעיף ג אחרי פתיחת השולחן : שישה עותקים, ונקודות הרשת כל 180 ס״מ לרוחב : פינות וכיסים אמצעיים "
                  "לסירוגין, כל כיס עיגול ברדיוס 4.5 ס״מ. הקו של 37° עובר ליד שלוש נקודות רשת ונכנס לעיגול של "
                  "(720, 540), הפינה (0, 180). הקו המקווקו, tan α = 2/3, נכנס כבר ב-(540, 360), הכיס האמצעי התחתון")
    for i in range(2):
        for j in range(3):
            n.rect(i * A, (i + 1) * A, j * B, (j + 1) * B, "bil-felt" if (i, j) == (0, 0) else "box-copy")
    for i in range(5):
        if i % 2:
            n.line(i * A / 2, 0, i * A / 2, 3 * B, "ink-line", 0.8, "2 4")
        for j in range(4):
            x, y = i * A // 2, j * B
            real = pocket_of(i, j)
            hl = (x, y) in ((2 * A, 3 * B), (3 * A // 2, 2 * B))
            n.add(f'<circle class="bil-hole{" is-in" if hl else ""}" cx="{n.X(x):.1f}" cy="{n.Y(y):.1f}" '
                  f'r="{W / 2 * float(sc):.2f}"><title>{pt((x, y))} : {NAMES[real]} {pt(real)}</title></circle>')
    t = tan37()
    n.line(0, 0, 2 * A, 2 * A * t, "bil-path", 2.5)
    n.line(0, 0, 3 * A / 2, B * 2, "s2-line", 2, "7 5")
    n.label(2 * A, 2 * A * t, "37°", dx=-14, dy=16, size=14, anchor="end")
    n.label(3 * A / 2, 2 * B, "tan α = 2/3", dx=10, dy=18, size=13, anchor="start")
    n.point(0, 0, "ink", r=5, title="הכדור יוצא מ-(0, 0)")
    return n.svg()


def grid_legend():
    return ('<span class="viz-legend"><span><i class="bil-key-felt"></i>השולחן עצמו</span>'
            '<span><i class="box-copy"></i>העותקים</span><span><i class="bil-key-hole"></i>כיס, ברדיוס 4.5 ס״מ</span>'
            '<span><i class="bil-path"></i>‏37° : נכנס ל-<span dir="ltr">(0, 180)</span></span><span><i class="bil-key-dash"></i>‏tan α = 2/3 : נכנס לאמצעי התחתון</span></span>')


D_START = (Fr(180), Fr(90))
D_TAN = Fr(7, 6)


def part_d_path():
    """The centre shot: the real points of its cushion hits and of the pocket."""
    x0, y0 = D_START
    k, m, pocket, _ = general_shot(x0, y0, D_TAN)
    x_end = Fr(k * A, 2)
    xs, ys = unfolded_cushions(x0, y0, D_TAN, x_end)
    hits = sorted([(x, y0 + (x - x0) * D_TAN) for x in xs] + [(x0 + (y - y0) / D_TAN, y) for y in ys])
    return [(fold(x, A), fold(y, B)) for x, y in hits], pocket


def part_d_svg():
    hits, pocket = part_d_path()
    pts = [D_START] + hits + [pocket]
    return path_svg(pts, hits, pocket,
                    "סעיף ד : הכדור יוצא ממרכז השולחן (180, 90) בשיפוע tan α = 7/6. הוא פוגע בדופן העליונה, בימנית, "
                    "בתחתונה ושוב בעליונה, ונכנס לכיס (0, 0) : ארבע פגיעות", start=D_START, r=Fr(W, 2))


def part_d_table():
    x0, y0 = D_START
    k_end, m_end, pocket, steps = general_shot(x0, y0, D_TAN)
    rows = ["| ‏\\( k \\) | ‏\\( k \\cdot 180 \\) | ‏\\( y_k \\) | ‏\\( m \\) | המרחק של הקו מהכיס | נכנס? |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for k, yk, m, d in steps:
        if k * A // 2 <= x0 and k != k_end:
            note = "מאחורי הכדור" if k * A // 2 < x0 else "נקודת היציאה"
            rows.append(f"| {k} | {k * A // 2} | {ltr(num(yk))} | – | – | לא : {note} |")
            continue
        yes = k == k_end
        rows.append(f"| {k} | {k * A // 2} | {ltr(num(yk))} | {m} | {ltr(num(d))} | "
                    f"{'**כן** : ' + ltr(pt(pocket)) if yes else 'לא'} |")
    return "\n".join(rows)


def paths_legend():
    return ('<span class="viz-legend"><span><i class="ink"></i>נקודת היציאה</span><span><i class="bil-path"></i>המסלול</span>'
            '<span><i class="s1"></i>פגיעה בדופן, לפי הסדר</span><span><i class="bil-key-in"></i>הכיס שהכדור נכנס אליו</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [
        statement_svg(),
        part_a_svg(),
        paths_legend(),
        part_a_table(),
        unfold_svg(),
        unfold_legend(),
        part_b_table(),
        grid_svg(),
        grid_legend(),
        part_c_table(),
        steps37_table(),
        part_d_svg(),
        paths_legend(),
        part_d_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
