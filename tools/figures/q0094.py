#!/usr/bin/env python3
"""Figures and tables of question 0094, the credit counter as a random walk.

    python tools/figures/fill.py 94        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Every number comes from the exact formulas below (fractions), which the
question's test checks against the page's code and against a direct solution of the
first-step equations. Colours come from the site's chart classes (s1 for "full", s2 for
"empty", ink for the fair walk).
"""

import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

NB = " "
RLM = "‏"
K0, N0 = 3, 10


def odds(k, n, p, q):
    """(P(full: n before 0), P(empty), expected cycles) from k, for +1 with p, -1 with q and
    no change with 1 - p - q, exactly."""
    p, q = Fr(p), Fr(q)
    s = p + q
    if k <= 0:
        return Fr(0), Fr(1), Fr(0)
    if k >= n:
        return Fr(1), Fr(0), Fr(0)
    a, b = p / s, q / s
    if a == b:
        full, moves = Fr(k, n), Fr(k * (n - k))
    elif a == 0:
        full, moves = Fr(0), Fr(k)
    else:
        rho = b / a
        full = (1 - rho ** k) / (1 - rho ** n)
        moves = (k - n * full) / (b - a)
    return full, 1 - full, moves / s


def rates(l1, l2):
    """The walk of geometric waits: a credit back with l1 and one used with l2 in a cycle."""
    l1, l2 = Fr(l1), Fr(l2)
    return l1 * (1 - l2), l2 * (1 - l1)


def d3(x):
    return f"{float(x):.3f}"


def d2(x):
    v = float(x)
    return f"{v:.2f}" if abs(v - round(v)) > 1e-9 else str(round(v))


# --- part a: two runs of the fair walk from 3 --------------------------------------------------

def fair_run(seed, k=K0, n=N0):
    """One run of the fair walk from k: the counter after every cycle, until a wall."""
    rnd = random.Random(seed)
    path = [k]
    while 0 < path[-1] < n:
        path.append(path[-1] + (1 if rnd.random() < 0.5 else -1))
    return path


# two seeds picked once: one run fills after 29 cycles, one empties after 11
RUN_FULL, RUN_EMPTY = 1, 24


def runs_figure():
    full, empty = fair_run(RUN_FULL), fair_run(RUN_EMPTY)
    T = max(len(full), len(empty)) - 1
    label = (f"שתי ריצות של המונה מ-{K0}, עולה או יורד ב-1 בהסתברות חצי בכל מחזור. אחת מגיעה "
             f"ל-{N0} אחרי {len(full) - 1} מחזורים, והשנייה ל-0 אחרי {len(empty) - 1} מחזורים")
    c = Chart(label, x_max=T, y_max=N0, h=250, base=214)
    c.grid_y([0, 2, 4, 6, 8, 10])
    c.hline(N0, f"N = {N0}", cls="s1-line", width=2, dash="6 4")
    c.hline(0, None, cls="s2-line", width=2, dash="6 4")
    c.path(list(enumerate(full)), "s1-line", width=2.5)
    c.path(list(enumerate(empty)), "s2-line", width=2.5)
    c.dot(0, K0, "ink", label=f"k = {K0}", dx=22, dy=4)
    c.dot(len(full) - 1, N0, "s1")
    c.dot(len(empty) - 1, 0, "s2")
    c.x_ticks(list(range(0, T + 1, 5)))
    c.axis("t")
    legend = (f'<span class="viz-legend"><span><i class="s1"></i><span>ריצה שהתמלאה, אחרי {len(full) - 1} מחזורים</span></span>'
              f'<span><i class="s2"></i><span>ריצה שהתרוקנה, אחרי {len(empty) - 1} מחזורים</span></span>'
              f'<span><i class="ink"></i><span>ההתחלה, {K0} credits</span></span></span>')
    return f'<div class="cw-fig">{c.svg()}</div>\n\n{legend}'


def fair_table():
    rows = ["| ‏k | הסיכוי להתמלא | הסיכוי להתרוקן | מחזורים בממוצע |", "|:-:|:-:|:-:|:-:|"]
    for k in range(1, N0):
        f, e, m = odds(k, N0, Fr(1, 2), Fr(1, 2))
        mark = "**" if k == K0 else ""
        rows.append(f"| {mark}{k}{mark} | {mark}{f.numerator}/{f.denominator}{mark} | "
                    f"{mark}{e.numerator}/{e.denominator}{mark} | {mark}{m}{mark} |")
    return "\n".join(rows)


# --- part b: a bias ------------------------------------------------------------------------------

P_ROWS = [Fr(2, 5), Fr(9, 20), Fr(1, 2), Fr(11, 20), Fr(3, 5), Fr(7, 10)]


def bias_table():
    rows = ["| ‏p | ‏q | הסיכוי להתמלא | הסיכוי להתרוקן | מחזורים בממוצע |", "|:-:|:-:|:-:|:-:|:-:|"]
    for p in P_ROWS:
        f, e, m = odds(K0, N0, p, 1 - p)
        mark = "**" if p == Fr(3, 5) else ""
        rows.append(f"| {mark}{d2(p)}{mark} | {mark}{d2(1 - p)}{mark} | {mark}{d3(f)}{mark} | "
                    f"{mark}{d3(e)}{mark} | {mark}{float(m):.2f}{mark} |")
    return "\n".join(rows)


CURVES = [(Fr(2, 5), "s2-line", "s2"), (Fr(1, 2), "ink-line", "ink"), (Fr(3, 5), "s1-line", "s1")]


def curves_figure():
    label = (f"הסיכוי להתמלא מכל נקודת התחלה k, מ-0 עד {N0}, בשלוש הסתברויות לעלות : 0.4, 0.5 ו-0.6. "
             "בחצי זה קו ישר, ובהטיה הקו מתעקם למעלה או למטה")
    c = Chart(label, x_max=N0, y_max=1, h=250, base=214)
    c.grid_y([0, 0.25, 0.5, 0.75, 1])
    for p, line, dot in CURVES:
        pts = [(k, odds(k, N0, p, 1 - p)[0]) for k in range(N0 + 1)]
        c.path(pts, line, width=2.5)
        for k, v in pts:
            c.dot(k, v, dot, r=3.5)
    c.add(f'<line class="ink-line" x1="{c.X(K0):.1f}" x2="{c.X(K0):.1f}" y1="{c.top - 4}" y2="{c.base}" '
          'stroke-width="1" stroke-dasharray="3 3"/>')
    c.x_ticks(list(range(N0 + 1)))
    c.axis("k")
    legend = ('<span class="viz-legend"><span><i class="s1"></i><span>‏p = 0.6</span></span>'
              '<span><i class="ink"></i><span>‏p = 0.5, הקו הישר k/N</span></span>'
              '<span><i class="s2"></i><span>‏p = 0.4</span></span>'
              f'<span><i class="ink-dash"></i><span>ההתחלה k = {K0}</span></span></span>')
    return f'<div class="cw-fig">{c.svg()}</div>\n\n{legend}'


# --- part c: the cycles that do not move -----------------------------------------------------------

PQR_ROWS = [(Fr(3, 5), Fr(2, 5)), (Fr(3, 10), Fr(1, 5)), (Fr(3, 25), Fr(2, 25)), (Fr(1, 4), Fr(1, 4)), (Fr(1, 10), Fr(1, 10))]


def stay_table():
    rows = ["| ‏p | ‏q | ‏r | ‏p/(p + q) | הסיכוי להתמלא | מחזורים בממוצע |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for p, q in PQR_ROWS:
        f, _, m = odds(K0, N0, p, q)
        mark = "**" if (p, q) == (Fr(3, 10), Fr(1, 5)) else ""
        rows.append(f"| {mark}{d2(p)}{mark} | {mark}{d2(q)}{mark} | {mark}{d2(1 - p - q)}{mark} | "
                    f"{mark}{d2(p / (p + q))}{mark} | {mark}{d3(f)}{mark} | {mark}{float(m):.2f}{mark} |")
    return "\n".join(rows)


# --- part d: geometric waits ---------------------------------------------------------------------

RATE_ROWS = [(Fr(1, 2), Fr(1, 4)), (Fr(2, 5), Fr(1, 2)), (Fr(1, 2), Fr(1, 2)), (Fr(1, 10), Fr(1, 10)), (Fr(9, 10), Fr(4, 5))]


def rates_table():
    rows = ["| ‏λ1 | ‏λ2 | ‏p | ‏q | ‏r | הסיכוי להתמלא | מחזורים בממוצע |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for l1, l2 in RATE_ROWS:
        p, q = rates(l1, l2)
        f, _, m = odds(K0, N0, p, q)
        mark = "**" if (l1, l2) == (Fr(1, 2), Fr(1, 4)) else ""
        rows.append(f"| {mark}{d2(l1)}{mark} | {mark}{d2(l2)}{mark} | {mark}{d3(p)}{mark} | {mark}{d3(q)}{mark} | "
                    f"{mark}{d3(1 - p - q)}{mark} | {mark}{d3(f)}{mark} | {mark}{float(m):.2f}{mark} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [runs_figure(), fair_table(), bias_table(), curves_figure(), stay_table(), rates_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
