#!/usr/bin/env python3
"""Figures and tables of question 0026 (three people, one motorcycle, minimum arrival time).

    python tools/figures/q0026.py > /tmp/q0026.html

Prints, in page order: the strategy comparison table and bar chart (alpha = 13), the road
figure with the points and the three phases (schematic, drawn to scale for alpha = 4 so
that every segment is wide enough to label), and the position-time chart with its
timeline and points tables (alpha = 13). Units: AB = 1 and t1 = 1 (the ride time of the
whole road), so the walking speed is 1 / alpha. tests/0026 checks that the page copies match.
"""

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

ALPHA = 13          # walk 13 hours, ride 1 hour
ROAD_ALPHA = 4      # proportions of the schematic road figure


def plan(alpha):
    """Segment lengths, point positions and phase times of the optimal plan (AB = 1, t1 = 1)."""
    a = Fr(alpha)
    x = (a - 1) / (a * (a + 3))
    y = r = (a + 1) / (a * (a + 3))
    z = a * x
    Q, C = y, y + x
    D = C + z
    E = D + x
    t1 = D                       # phase 1: the motorcycle rides A -> D
    t2 = t1 + z                  # phase 2: back D -> C
    t3 = t2 + (1 - C)            # phase 3: C -> B
    return dict(x=x, y=y, z=z, r=r, Q=Q, C=C, D=D, E=E, t1=t1, t2=t2, T=t3)


def t_optimal(alpha):
    a = Fr(alpha)
    return (3 * a + 1) / (a + 3)


def t_wait(alpha):
    """Ride one person to B, ride back empty to A, ride the second one; the second waits."""
    return Fr(3)


def t_walk_meanwhile(alpha):
    """As t_wait, but the second person walks towards B while the motorcycle is away."""
    a = Fr(alpha)
    return (3 * a - 1) / (a + 1)


def frac(v):
    v = Fr(v)
    return f"{v.numerator}" if v.denominator == 1 else f"\\tfrac{{{v.numerator}}}{{{v.denominator}}}"


def slash(v):
    v = Fr(v)
    return f"{v.numerator}" if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def hours(v):
    """Hours as '2.5' or '2.71' (two decimals at most, no trailing zeros)."""
    return f"{float(v):.3f}".rstrip("0").rstrip(".")


# --- strategies ----------------------------------------------------------------------------

STRATEGIES = [
    ("by-multiples", "השני מחכה ב-\\( A \\)", "‏\\( 3\\,t_1 \\)", t_wait),
    ("by-enum", "השני הולך בינתיים", "‏\\( \\dfrac{3\\alpha - 1}{\\alpha + 1}\\, t_1 \\)", t_walk_meanwhile),
    ("by-bfs", "הנוסע יורד בדרך", "‏\\( \\dfrac{3\\alpha + 1}{\\alpha + 3}\\, t_1 \\)", t_optimal),
]


def strategies_table(alpha=ALPHA):
    lines = [f"| האסטרטגיה | הזמן הכללי | כש-\\( \\alpha = {alpha} \\) |", "|---|---|---|"]
    for _, name, general, f in STRATEGIES:
        v = f(alpha)
        exact = f"\\( {frac(v)} \\approx {hours(v)} \\)" if v.denominator > 2 else f"\\( {hours(v)} \\)"
        lines.append(f"| {name} | {general} | ‏{exact} שעות |")
    return "\n".join(lines)


def strategies_chart(alpha=ALPHA):
    w, h, x0, right, top, bh, gap = 560, 150, 24, 60, 10, 28, 12
    tmax = 3
    sx = (w - x0 - right) / tmax
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="הזמן של שלוש האסטרטגיות: 3 שעות כשהשני מחכה, כ-2.71 שעות כשהוא הולך בינתיים, '
         'ו-2.5 שעות כשהנוסע יורד בדרך">']
    base = top + 3 * (bh + gap)
    for t in range(tmax + 1):
        X = x0 + t * sx
        p.append(f'<line class="grid" x1="{X:.1f}" x2="{X:.1f}" y1="{top - 4}" y2="{base}"/>'
                 f'<text class="tick" x="{X:.1f}" y="{base + 16}" text-anchor="middle">{t}</text>')
    for i, (cls, name, _, f) in enumerate(STRATEGIES):
        v = f(alpha)
        y = top + i * (bh + gap)
        p.append(f'<rect class="bar {cls}" x="{x0}" y="{y}" width="{float(v) * sx:.1f}" height="{bh}" rx="3">'
                 f'<title>{hours(v)}</title></rect>'
                 f'<text class="legend" x="{x0 + float(v) * sx + 8:.1f}" y="{y + bh / 2 + 5:.0f}">{hours(v)}</text>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - right + 10}" y1="{base}" y2="{base}"/>'
             f'<text class="tick" x="{w - right + 24}" y="{base + 16}" text-anchor="middle">t</text></svg>')
    return "".join(p)


def strategies_legend():
    return ('<span class="viz-legend">'
            + "".join(f'<span><i class="{cls}"></i>{name}</span>' for cls, name, _, _ in STRATEGIES)
            + "</span>")


# --- the road ------------------------------------------------------------------------------

DEFS = ('<defs>' + "".join(
    f'<marker id="q26-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{m}" markerHeight="{m}" '
    f'orient="auto-start-reverse"><path class="{c}-fill" d="M0,0 L10,5 L0,10 z"/></marker>'
    for c, m in (("ink", 4), ("s1", 6), ("s2", 6))) + '</defs>')


def road_svg(alpha=ROAD_ALPHA):
    """The road A..B with Q, C, D, E and the lengths y, x, z, x, r; below it one row per
    phase with who moves where (the motorcycle, the passenger on foot, the walker on foot)."""
    pl = plan(alpha)
    w, x0, x1 = 640, 40, 610
    X = lambda v: x0 + float(v) * (x1 - x0)
    pts = [("A", 0), ("Q", pl["Q"]), ("C", pl["C"]), ("D", pl["D"]), ("E", pl["E"]), ("B", 1)]
    segs = ["y", "x", "z", "x", "r"]
    ya, row0, rh = 50, 108, 40
    h = row0 + 3 * rh
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="הדרך מ-A ל-B עם הנקודות Q, C, D, E והקטעים y, x, z, x, r, ומתחתיה שלושת השלבים: '
         'מי נוסע ומי הולך בכל שלב">', DEFS]
    p.append(f'<line class="ink-line" x1="{X(0)}" y1="{ya}" x2="{X(1)}" y2="{ya}" stroke-width="2"/>')
    for (_, a), (_, b), s in zip(pts, pts[1:], segs):
        xm = (X(a) + X(b)) / 2
        p.append(f'<line class="axis-c" x1="{X(a) + 3:.1f}" y1="{ya - 14}" x2="{X(b) - 3:.1f}" y2="{ya - 14}" stroke-width="1"/>'
                 f'<text class="legend" x="{xm:.1f}" y="{ya - 20}" text-anchor="middle" font-style="italic" style="font-size:20px">{s}</text>')
    for name, v in pts:
        p.append(f'<line class="axis-c" x1="{X(v):.1f}" y1="{ya - 7}" x2="{X(v):.1f}" y2="{ya + 7}"/>'
                 f'<text class="legend" x="{X(v):.1f}" y="{ya + 28}" text-anchor="middle" style="font-size:20px">{name}</text>')
    moves = [  # (phase, [(class, from, to, offset)])
        (1, [("ink", 0, pl["D"], -7), ("s2", 0, pl["Q"], 7)]),
        (2, [("ink", pl["D"], pl["C"], -7), ("s1", pl["D"], pl["E"], 7), ("s2", pl["Q"], pl["C"], 7)]),
        (3, [("ink", pl["C"], 1, -7), ("s1", pl["E"], 1, 7)]),
    ]
    for k, row in moves:
        yc = row0 + (k - 1) * rh
        p.append(f'<text class="legend" x="{x0 - 22}" y="{yc + 7}" text-anchor="middle" style="font-size:20px">{k}</text>')
        for c, a, b, off in row:
            sgn = 1 if b > a else -1
            p.append(f'<line class="{"ink" if c == "ink" else c}-line" x1="{X(a) + sgn * 2:.1f}" y1="{yc + off}" '
                     f'x2="{X(b) - sgn * 2:.1f}" y2="{yc + off}" stroke-width="{3 if c == "ink" else 2}" '
                     f'marker-end="url(#q26-{c})"/>')
    p.append("</svg>")
    return "".join(p)


def road_legend():
    return ('<span class="viz-legend"><span><i class="ink"></i>האופנוע (הנהג, ואיתו נוסע או לא)</span>'
            '<span><i class="s1"></i>הנוסע הולך ברגל</span><span><i class="s2"></i>ההולך הולך ברגל</span></span>')


# --- position over time ----------------------------------------------------------------------

def spacetime_svg(alpha=ALPHA):
    """Position (0 = A, 1 = B) against time for the motorcycle and the two non-drivers."""
    pl = plan(alpha)
    T = pl["T"]
    c = Chart("המקום של האופנוע ושל שני האנשים שאינם נוהגים כפונקציה של הזמן: האופנוע נוסע קדימה, "
              "חוזר ונוסע שוב קדימה, ושלושתם מגיעים ל-B יחד אחרי 2.5 שעות",
              h=320, x0=52, right=24, top=34, base=286, x_max=float(T), y_max=1)
    c.add(DEFS)
    ys = (0, pl["C"], pl["D"], 1)
    c.grid_y(ys, labels=[slash(v) for v in ys])
    ts = (0, pl["t1"], pl["t2"], T)
    c.grid_x(ts, [hours(t) for t in ts])
    for k, (a, b) in enumerate(((0, pl["t1"]), (pl["t1"], pl["t2"]), (pl["t2"], T)), 1):
        c.add(f'<text class="legend" x="{(c.X(a) + c.X(b)) / 2:.1f}" y="{c.top - 14}" text-anchor="middle" '
              f'direction="rtl">שלב {k}</text>')
    c.path([(0, 0), (pl["t1"], pl["D"]), (pl["t2"], pl["C"]), (T, 1)], "ink-line", width=7,
           extra=' stroke-opacity="0.28" stroke-linejoin="round"')
    c.path([(0, 0), (pl["t1"], pl["D"]), (pl["t2"], pl["E"]), (T, 1)], "s1-line", width=2.5)
    c.path([(0, 0), (pl["t1"], pl["Q"]), (pl["t2"], pl["C"]), (T, 1)], "s2-line", width=2.5)
    marks = [("Q", pl["t1"], pl["Q"], "s2", 0, -10, "ההולך כשהנוסע יורד"),
             ("D", pl["t1"], pl["D"], "s1", 0, -12, "הנוסע יורד"),
             ("C", pl["t2"], pl["C"], "s2", 0, 22, "האופנוע אוסף את ההולך"),
             ("E", pl["t2"], pl["E"], "s1", 0, -12, "הנוסע כשההולך עולה"),
             ("B", T, 1, "ink", -16, -6, "שלושתם מגיעים")]
    for name, t, v, cls, dx, dy, title in marks:
        c.dot(t, v, cls, r=5, title=f"{name}: {title}, t = {hours(t)}", label=name, dx=dx, dy=dy, label_size=17)
    c.add(f'<line class="axis" x1="{c.x0}" x2="{c.x1}" y1="{c.base}" y2="{c.base}"/>'
          f'<text class="tick" x="{c.x1 + 14}" y="{c.base + 4}" text-anchor="middle">t</text>')
    return c.svg()


def spacetime_legend():
    return ('<span class="viz-legend"><span><i class="ink" style="opacity:0.4"></i>האופנוע</span>'
            '<span><i class="s1"></i>הנוסע</span><span><i class="s2"></i>ההולך</span></span>')


def timeline_table(alpha=ALPHA):
    pl = plan(alpha)
    rows = [
        (1, 0, pl["t1"], "‏\\( A \\to D \\)", "על האופנוע", "‏\\( A \\to Q \\)"),
        (2, pl["t1"], pl["t2"], "‏\\( D \\to C \\)", "‏\\( D \\to E \\)", "‏\\( Q \\to C \\)"),
        (3, pl["t2"], pl["T"], "‏\\( C \\to B \\)", "‏\\( E \\to B \\)", "על האופנוע"),
    ]
    lines = ["| שלב | השעות | האופנוע | הנוסע | ההולך |", "|---|---|---|---|---|"]
    for k, a, b, bike, pas, walk in rows:
        lines.append(f"| שלב {k} | ‏{hours(a)} עד {hours(b)} | {bike} | {pas} | {walk} |")
    return "\n".join(lines)


def points_table(alpha=ALPHA):
    pl = plan(alpha)
    rows = [("Q", pl["Q"], "ההולך, כשהנוסע יורד מהאופנוע"),
            ("C", pl["C"], "האופנוע אוסף את ההולך"),
            ("D", pl["D"], "הנוסע יורד מהאופנוע"),
            ("E", pl["E"], "הנוסע, כשהאופנוע אוסף את ההולך")]
    lines = ["| הנקודה | המרחק מ-\\( A \\) | מה קורה שם |", "|---|---|---|"]
    for name, v, what in rows:
        lines.append(f"| ‏\\( {name} \\) | ‏\\( {frac(v)}\\,AB \\approx {float(v):.3f}\\,AB \\) | {what} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order (tools/figures/fill.py puts them on the page)."""
    return [
        strategies_table(),
        strategies_chart(),
        strategies_legend(),
        road_svg(),
        road_legend(),
        spacetime_svg(),
        spacetime_legend(),
        timeline_table(),
        points_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
