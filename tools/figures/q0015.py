#!/usr/bin/env python3
"""Figures and the value table of question 0015 (two children, at least one boy).

    python tools/figures/q0015.py > /tmp/q0015.html

Prints the 2x2 grid of part a, the 14x14 grid of part b (sex x weekday of each child) and
the table of the general formula for a few values of q; paste them into the question page.
Rows are the first child, columns the second child; both run right to left, like the page.
"""

from fractions import Fraction
from itertools import product

DAYS = "אבגדהוש"            # Sunday .. Saturday; Tuesday is the third day, "ג"
TUESDAY = 2
SEXES = ["בן", "בת"]


def cell_class(cond, hit):
    return "pg-hit" if hit else "pg-cond" if cond else "pg-out"


def grid_a():
    """Part a: the four equally likely families; BB is the target, GG is ruled out."""
    cw, ch, x_right, top = 110, 56, 240, 28
    w, h = 300, top + 2 * ch + 10
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="ארבע המשפחות האפשריות : בן בן, בן בת, בת בן, בת בת. בת בת נפסלת, ומבין שלוש הנותרות '
         'רק אחת היא בן בן">']
    for j, s in enumerate(SEXES):                         # column headers: the second child
        x = x_right - (j + 0.5) * cw
        p.append(f'<text class="pg-head" x="{x:.0f}" y="{top - 10}" text-anchor="middle" direction="rtl">{s}</text>')
    for i, s in enumerate(SEXES):                         # row headers: the first child
        y = top + (i + 0.5) * ch + 5
        p.append(f'<text class="pg-head" x="{x_right + 30}" y="{y:.0f}" text-anchor="middle" direction="rtl">{s}</text>')
    for i, j in product(range(2), repeat=2):
        boy1, boy2 = i == 0, j == 0
        cls = cell_class(boy1 or boy2, boy1 and boy2)
        x, y = x_right - (j + 1) * cw, top + i * ch
        p.append(f'<rect class="{cls}" x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="6"/>')
        if not (boy1 or boy2):                            # ruled out: struck through, drawn under the text
            p.append(f'<line class="pg-strike" x1="{x + 12}" y1="{y + ch - 10}" x2="{x + cw - 12}" y2="{y + 10}"/>')
        label = f"{SEXES[i]}, {SEXES[j]}"
        p.append(f'<text class="pg-label" x="{x + cw / 2:.0f}" y="{y + ch / 2 - 2:.0f}" text-anchor="middle" '
                 f'direction="rtl">{label}</text>')
        p.append(f'<text class="pg-small" x="{x + cw / 2:.0f}" y="{y + ch / 2 + 15:.0f}" text-anchor="middle">1/4</text>')
    p.append("</svg>")
    return "".join(p)


def tuesday_boy(sex, day):
    return sex == 0 and day == TUESDAY


def grid_b():
    """Part b: 14 x 14 equally likely (sex, day) pairs; the cross of 27 cells is the condition,
    the 13 cells inside the boy-boy quadrant are the target."""
    c, x_right, top = 26, 370, 44
    w, h = 432, top + 14 * c + 8
    kinds = [(s, d) for s in range(2) for d in range(7)]
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="טבלה של 196 צירופים של מין ויום לידה לשני הילדים. 27 משבצות מקיימות את התנאי, '
         'ו-13 מהן הן בן ובן">']
    for g, s in enumerate(SEXES):                         # group headers
        x = x_right - (g * 7 + 3.5) * c
        p.append(f'<text class="pg-head" x="{x:.0f}" y="16" text-anchor="middle" direction="rtl">{s}</text>')
        y = top + (g * 7 + 3.5) * c + 5
        p.append(f'<text class="pg-head" x="{x_right + 44}" y="{y:.0f}" text-anchor="middle" direction="rtl">{s}</text>')
    for k, (s, d) in enumerate(kinds):                    # weekday letters
        cls = "pg-day pg-day-hl" if tuesday_boy(s, d) else "pg-day"
        x = x_right - (k + 0.5) * c
        p.append(f'<text class="{cls}" x="{x:.0f}" y="{top - 8}" text-anchor="middle">{DAYS[d]}</text>')
        y = top + (k + 0.5) * c + 4
        p.append(f'<text class="{cls}" x="{x_right + 14}" y="{y:.0f}" text-anchor="middle">{DAYS[d]}</text>')
    for (i, (s1, d1)), (j, (s2, d2)) in product(enumerate(kinds), repeat=2):
        cond = tuesday_boy(s1, d1) or tuesday_boy(s2, d2)
        hit = cond and s1 == 0 and s2 == 0
        x, y = x_right - (j + 1) * c, top + i * c
        p.append(f'<rect class="{cell_class(cond, hit)}" x="{x + 1}" y="{y + 1}" width="{c - 2}" height="{c - 2}" rx="3"/>')
        if tuesday_boy(s1, d1) and tuesday_boy(s2, d2):
            p.append(f'<circle class="pg-twice" cx="{x + c / 2}" cy="{y + c / 2}" r="{c / 2 - 6}"/>')
    # the boy-boy quadrant (every family with two boys) and the boy / girl dividers
    p.append(f'<rect class="pg-quad" x="{x_right - 7 * c}" y="{top}" width="{7 * c}" height="{7 * c}"/>')
    p.append(f'<line class="pg-split" x1="{x_right - 7 * c}" y1="{top}" x2="{x_right - 7 * c}" y2="{top + 14 * c}"/>')
    p.append(f'<line class="pg-split" x1="{x_right - 14 * c}" y1="{top + 7 * c}" x2="{x_right}" y2="{top + 7 * c}"/>')
    p.append("</svg>")
    return "".join(p)


def legend(full):
    items = ['<span><i class="pg-hit"></i>מקיים את התנאי, ושני הילדים בנים</span>',
             '<span><i class="pg-cond"></i>מקיים את התנאי, יש גם בת</span>',
             '<span><i class="pg-out"></i>לא מקיים את התנאי</span>']
    if full:
        items += ['<span><i class="pg-quad"></i>כל המשפחות עם שני בנים (49)</span>',
                  '<span><i class="pg-twice"></i>שני בנים שנולדו ביום שלישי, נספר פעם אחת</span>']
    return '<span class="viz-legend">' + "".join(items) + "</span>"


def answer(C, p, q):
    """P(all C children are boys | at least one child is a boy with the trait)."""
    return p ** C * (1 - (1 - q) ** C) / (1 - (1 - p * q) ** C)


VALUES = [("בלי תכונה (סעיף א), \\( q = 1 \\)", Fraction(1)),
          ("הטלת מטבע, \\( q = 1/2 \\)", Fraction(1, 2)),
          ("יום בשבוע, \\( q = 1/7 \\)", Fraction(1, 7)),
          ("יום בשנה, \\( q = 1/365 \\)", Fraction(1, 365))]


def values_table():
    half = Fraction(1, 2)
    lines = ["| התכונה | ‏\\( C = 2 \\) | ‏\\( C = 3 \\) |", "|---|---|---|"]
    for name, q in VALUES:
        cells = []
        for C in (2, 3):
            v = answer(C, half, q)
            cells.append(f"‏\\( {v.numerator}/{v.denominator} \\approx {float(v):.3f} \\)")
        lines.append(f"| {name} | {cells[0]} | {cells[1]} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(grid_a(), "\n")
    print(legend(False), "\n")
    print(grid_b(), "\n")
    print(legend(True), "\n")
    print(values_table())
