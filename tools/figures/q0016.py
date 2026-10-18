#!/usr/bin/env python3
"""Figures and tables of question 0016 (the Josephus problem).

    python tools/figures/q0016.py > /tmp/q0016.html

Prints, in page order: the step-through circle for n = 10, k = 2; the table of survivors
for n = 1..16; the survivor chart for n = 1..40; the "one round" tables for n = 10 and 11;
the bit-rotation figure; the step-through circle for n = 7, k = 3; the recurrence table
for n = 7, k = 3. Paste them into the page; tests/0016 checks that the page copies match.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402


def elimination(n, k):
    """People 1..n in a circle; counting starts at person 1 and every k-th person leaves.
    Returns the list of (counted, victim) for every elimination, and the survivor."""
    circle = list(range(1, n + 1))
    steps, i = [], 0
    while len(circle) > 1:
        idx = [(i + j) % len(circle) for j in range(k)]
        counted, victim = [circle[j] for j in idx[:-1]], circle[idx[-1]]
        steps.append((counted, victim))
        i = idx[-1]
        circle.pop(i)
        i %= len(circle)
    return steps, circle[0]


def survivor(n, k=2):
    return elimination(n, k)[1]


def circle_frame(n, out, counted=(), victim=None, winner=None):
    """n people on a circle, person 1 at the top, numbered clockwise."""
    w, h, cx, cy, R, r = 300, 280, 150, 140, 105, 17
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         f'aria-label="{n} אנשים במעגל">']
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" class="ink-line" stroke-width="1" '
             'stroke-dasharray="3 5" opacity="0.5"/>')
    for i in range(1, n + 1):
        a = -math.pi / 2 + 2 * math.pi * (i - 1) / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        if i == winner:
            cls = "st-ok"
        elif i == victim:
            cls = "st-bad"
        elif i in counted:
            cls = "st-stack"
        elif i in out:
            cls = "st-done"
        else:
            cls = "st-cell"
        faded = ' class="st-faded"' if i in out and i != victim else ""
        p.append(f'<g{faded}><circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
                 f'<text class="st-text" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{i}</text>')
        if i in out:
            p.append(f'<line class="pg-strike" x1="{x - 12:.1f}" y1="{y + 12:.1f}" x2="{x + 12:.1f}" y2="{y - 12:.1f}"/>')
        p.append("</g>")
    left = n - len(out)
    p.append(f'<text class="st-text" x="{cx}" y="{cy + 6}" text-anchor="middle">{left}</text>')
    p.append("</svg>")
    return "".join(p)


def circle_stepper(n, k):
    steps, win = elimination(n, k)
    frames = [(circle_frame(n, set()),
               f"{n} אנשים במעגל. סופרים מאדם 1, וכל {'שני' if k == 2 else 'שלישי'} יוצא. "
               "המספר במרכז הוא כמה אנשים נשארו.")]
    out = set()
    for s, (counted, victim) in enumerate(steps, 1):
        if k == 2:
            text = f"יציאה {s}: אדם {counted[0]} מדלג, ואדם {victim} יוצא."
        else:
            text = f"יציאה {s}: סופרים את {' ו-'.join(map(str, counted))}, ואדם {victim} יוצא."
        frames.append((circle_frame(n, out | {victim}, counted, victim), text))
        out.add(victim)
    frames.append((circle_frame(n, out, winner=win), f"נשאר אדם {win}. הוא השורד."))
    return stepper(frames, f"יוספוס עם {n} אנשים, כל {'שני' if k == 2 else 'שלישי'} יוצא")


def survivors_table(N=16):
    lines = ["| ‏\\( n \\) | בבינארי | ‏\\( 2^m + L \\) | השורד |", "|---|---|---|---|"]
    for n in range(1, N + 1):
        top = 1 << (n.bit_length() - 1)
        lines.append(f"| {n} | ‏`{n:b}` | ‏\\( {top} + {n - top} \\) | **{survivor(n)}** |")
    return "\n".join(lines)


def chart(N=40):
    w, h, x0, top, base = 640, 290, 44, 14, 250
    sx = (w - x0 - 16) / N
    sy = (base - top) / N
    X = lambda n: x0 + (n - 0.5) * sx
    Y = lambda v: base - v * sy
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" role="img" '
         f'aria-label="השורד כפונקציה של מספר האנשים, מ-1 עד {N}">']
    for v in range(0, N + 1, 8):
        p.append(f'<line class="grid" x1="{x0}" x2="{w - 16}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                 f'<text class="tick" x="{x0 - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    p.append(f'<line class="ink-line" x1="{X(0.5):.1f}" y1="{Y(0):.1f}" x2="{X(N + 0.5):.1f}" y2="{Y(N):.1f}" '
             'stroke-width="1.2" stroke-dasharray="5 4"/>')
    prev = None
    for n in range(1, N + 1):
        j = survivor(n)
        if prev and j > prev[1]:
            p.append(f'<line class="s1-line" x1="{X(prev[0]):.1f}" y1="{Y(prev[1]):.1f}" '
                     f'x2="{X(n):.1f}" y2="{Y(j):.1f}" stroke-width="1.5"/>')
        prev = (n, j)
    for n in range(1, N + 1):
        j = survivor(n)
        cls = "s2-dot" if n & (n - 1) == 0 else "s1-dot"
        p.append(f'<circle class="{cls}" cx="{X(n):.1f}" cy="{Y(j):.1f}" r="4.5"><title>n = {n}: {j}</title></circle>')
        if n % 4 == 0 or n == 1:
            p.append(f'<text class="tick" x="{X(n):.1f}" y="{base + 18}" text-anchor="middle">{n}</text>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - 16}" y1="{base}" y2="{base}"/>')
    p.append(f'<text class="tick" x="{(x0 + w) / 2:.0f}" y="{h - 4}" text-anchor="middle">n</text></svg>')
    return "".join(p)


def chart_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>השורד</span>'
            '<span><i class="s2"></i>חזקה של 2: השורד הוא 1</span>'
            '<span><i class="ink"></i>הקו \\( J = n \\)</span></span>')


def one_round(n):
    """k = 2: who leaves in the first pass around the circle, and who is left, in the order
    of the next count. Even n: 2, 4, ..., n leave and the count goes on from 1. Odd n:
    2, 4, ..., n - 1 leave, then 1, and the count goes on from 3."""
    steps, _ = elimination(n, 2)
    removed = [v for _, v in steps[: n // 2 + n % 2]]
    alive = [q for q in range(1, n + 1) if q not in removed]
    first = 1 if n % 2 == 0 else 3
    return removed, alive[alive.index(first):] + alive[:alive.index(first)]


def one_round_table():
    lines = ["| ‏\\( n \\) | יוצאים | נשארים, לפי הסדר |", "|---|---|---|"]
    for n in (10, 11):
        removed, order = one_round(n)
        lines.append(f"| {n} | {', '.join(map(str, removed))} | {', '.join(map(str, order))} |")
    return "\n".join(lines)


def bits_svg(examples=(10, 41)):
    cell, gap = 30, 4
    longest = max(len(f"{n:b}") for n in examples)
    w, h = 70 + 2 * longest * (cell + gap) + 90 + 50, 24 + 86 * len(examples)
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="הסיבוב של הביטים: הביט העליון של n עובר לסוף, והתוצאה היא השורד"><defs>'
         '<marker id="q16-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker>'
         '<marker id="q16-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs>']
    y = 14
    for n in examples:
        b = f"{n:b}"
        rot = b[1:] + b[0]
        xa, xb = 70, 70 + len(b) * (cell + gap) + 90
        p.append(f'<text class="legend" x="{xa - 12}" y="{y + 20}" text-anchor="end">{n}</text>')
        for i, ch in enumerate(b):
            cls = "st-bad" if i == 0 else "st-cell"
            p.append(f'<rect class="{cls}" x="{xa + i * (cell + gap)}" y="{y}" width="{cell}" height="{cell}" rx="4"/>'
                     f'<text class="st-text" x="{xa + i * (cell + gap) + cell / 2}" y="{y + 21}" text-anchor="middle">{ch}</text>')
        for i, ch in enumerate(rot):
            cls = "st-ok" if i == len(rot) - 1 else "st-cell"
            p.append(f'<rect class="{cls}" x="{xb + i * (cell + gap)}" y="{y}" width="{cell}" height="{cell}" rx="4"/>'
                     f'<text class="st-text" x="{xb + i * (cell + gap) + cell / 2}" y="{y + 21}" text-anchor="middle">{ch}</text>')
        x_end = xb + len(rot) * (cell + gap)
        p.append(f'<text class="legend" x="{x_end + 8}" y="{y + 20}">{int(rot, 2)}</text>')
        p.append(f'<line class="ink-line" x1="{xa + len(b) * (cell + gap) + 12}" y1="{y + cell / 2}" '
                 f'x2="{xb - 14}" y2="{y + cell / 2}" stroke-width="1.5" marker-end="url(#q16-ink)"/>')
        # the leading 1 travels to the end
        x0 = xa + cell / 2
        x1 = xb + (len(rot) - 1) * (cell + gap) + cell / 2
        p.append(f'<path class="s2-line" d="M{x0},{y + cell + 4} C{x0},{y + cell + 40} {x1},{y + cell + 40} {x1},{y + cell + 6}" '
                 f'fill="none" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#q16-s2)"/>')
        y += 86
    p.append("</svg>")
    return "".join(p)


def recurrence(n, k):
    f = 0
    rows = [(1, "", 0)]
    for m in range(2, n + 1):
        new = (f + k) % m
        rows.append((m, f"({f} + {k}) \\bmod {m}", new))
        f = new
    return rows


def recurrence_table(n=7, k=3):
    lines = ["| מספר האנשים \\( m \\) | החישוב | ‏\\( f(m) \\) | השורד, \\( f(m) + 1 \\) |", "|---|---|---|---|"]
    for m, calc, f in recurrence(n, k):
        calc = f"‏\\( {calc} \\)" if calc else "בסיס: אדם אחד"
        lines.append(f"| {m} | {calc} | {f} | {f + 1} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(circle_stepper(10, 2), "\n")
    print(survivors_table(), "\n")
    print(chart_legend(), "\n")
    print(chart(), "\n")
    print(one_round_table(), "\n")
    print(bits_svg(), "\n")
    print(circle_stepper(7, 3), "\n")
    print(recurrence_table())
