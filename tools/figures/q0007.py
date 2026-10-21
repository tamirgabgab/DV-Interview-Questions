#!/usr/bin/env python3
"""Figures of question 0007 (a random triangle on the unit circle that contains the centre).

    python tools/figures/fill.py 7         # put the blocks on the page

blocks() returns, in page order: the two example triangles with their three arcs (one
contains the centre, one does not), the half-circle figure of the proof (P2 and P3 fall in
the half circle that starts at P1), the legend and the chart of P(M) for M points on a
grid, odd and even M as two series around 1/4. tests/0007 checks the formula against brute
force and the page copy against this file.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

R = 100
EXAMPLES = [((20, 140, 250), True), ((20, 70, 150), False)]       # angles in degrees, counterclockwise
HALF_POINTS = (200, 260, 330)                                     # P1, P2, P3 of the proof figure


def p_formula(m):
    """P(M): the share of triangles on M equally spaced points that contain the centre."""
    return Fraction(m + 1, 4 * (m - 2)) if m % 2 else Fraction(m - 4, 4 * (m - 1))


def pt(cx, cy, deg, r=R):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def arc(cx, cy, a, b, cls, width, r=R + 12):
    """The arc from angle a to angle b counterclockwise, drawn outside the circle."""
    (x1, y1), (x2, y2) = pt(cx, cy, a, r), pt(cx, cy, b, r)
    big = 1 if (b - a) % 360 > 180 else 0
    return f'<path class="{cls}" d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {big} 0 {x2:.1f},{y2:.1f}" fill="none" stroke-width="{width}"/>'


def triangle(cx, cy, angles, inside):
    p = [f'<circle class="axis-c" cx="{cx}" cy="{cy}" r="{R}" fill="none"/>']
    for i in range(3):
        a, b = angles[i], angles[(i + 1) % 3]
        gap = (b - a) % 360
        bad = gap >= 180
        p.append(arc(cx, cy, a, b, "s2-line" if bad else "s1-line", 5 if bad else 3))
        lx, ly = pt(cx, cy, a + gap / 2, R + 26)
        p.append(f'<text class="legend" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">{gap}°</text>')
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(cx, cy, a, R - 6) for a in angles))
    p.append(f'<polygon class="{"tri-ok" if inside else "tri-bad"}" points="{pts}"/>')
    for a in angles:
        x, y = pt(cx, cy, a, R - 6)
        p.append(f'<circle class="ink-dot" cx="{x:.1f}" cy="{y:.1f}" r="5"><title>{a}°</title></circle>')
    p.append(f'<circle class="center-dot" cx="{cx}" cy="{cy}" r="4"/><text class="tick" x="{cx + 6}" y="{cy + 14}">O</text>')
    caption = ("✓ מכיל את המרכז: כל הפערים קטנים מ-180°" if inside else
               f"✗ לא מכיל: יש פער של {max((angles[(i + 1) % 3] - angles[i]) % 360 for i in range(3))}° > 180°")
    p.append(f'<text class="legend" x="{cx}" y="{cy + 162}" text-anchor="middle" direction="rtl">{caption}</text>')
    return "".join(p)


def examples_figure():
    body = "".join(triangle(160 + 320 * i, 150, angles, inside) for i, (angles, inside) in enumerate(EXAMPLES))
    return ('<svg class="figure" viewBox="0 0 640 330" role="img" aria-label="שתי דוגמאות: משולש שמכיל את מרכז '
            f'המעגל ומשולש שלא מכיל אותו">{body}</svg>')


def half_figure():
    cx, cy = 180, 140
    a1 = HALF_POINTS[0]
    (x1, y1), (x2, y2) = pt(cx, cy, a1), pt(cx, cy, a1 + 180)
    p = [f'<svg class="figure" viewBox="0 0 360 300" style="max-width:22rem" role="img" '
         'aria-label="חצי המעגל שמתחיל בנקודה P1 נגד כיוון השעון">',
         f'<path class="half-fill" d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{R},{R} 0 0 0 {x2:.1f},{y2:.1f} Z"/>',
         f'<circle class="axis-c" cx="{cx}" cy="{cy}" r="{R}" fill="none"/>',
         f'<line class="axis-c" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>']
    for i, a in enumerate(HALF_POINTS):
        x, y = pt(cx, cy, a)
        lx, ly = pt(cx, cy, a, R + 20)
        p.append(f'<circle class="ink-dot" cx="{x:.1f}" cy="{y:.1f}" r="5"/>'
                 f'<text class="legend" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">P{i + 1}</text>')
    p.append(f'<circle class="center-dot" cx="{cx}" cy="{cy}" r="4"/>'
             f'<text class="tick" x="{cx}" y="288" text-anchor="middle" direction="rtl">'
             'P2 ו-P3 נפלו בחצי המעגל שמתחיל ב-P1, ולכן המרכז בחוץ</text></svg>')
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>M אי-זוגי</span>'
            '<span><i class="s2"></i>M זוגי</span></span>')


def chart(m_max=40):
    c = Chart("ההסתברות שהמשולש מכיל את המרכז כפונקציה של M", w=640, h=300, x0=48, right=40,
              top=16, base=260, x_min=4, x_max=m_max, y_max=0.5)
    c.grid_y([i / 10 for i in range(6)], fmt="{:.1f}")
    c.hline(0.25, "¼", dash="none", width=1, cls="axis")
    c.x_ticks(range(4, m_max + 1, 4), labels=[f"M = {m}" for m in range(4, m_max + 1, 4)])
    for parity, cls in ((1, "s1"), (0, "s2")):
        ms = [m for m in range(4, m_max + 1) if m % 2 == parity]
        c.path([(m, p_formula(m)) for m in ms], f"{cls}-line")
        for m in ms:
            c.dot(m, p_formula(m), cls, r=4, title=f"M = {m}: P = {float(p_formula(m)):.4f}")
    return c.svg()


def blocks():
    """The generated blocks, in page order."""
    return [examples_figure(), half_figure(), legend(), chart()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
