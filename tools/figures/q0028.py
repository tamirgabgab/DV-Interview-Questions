#!/usr/bin/env python3
"""Figures and tables of question 0028 (a cake split by fractions that grow as a geometric
sequence).

    python tools/figures/q0028.py > /tmp/q0028.html

Prints, in page order: the statement figure (a = 0.1, q = 2, no peak marked); for part a
(a = 0.01, q = 1.5) the shares bars, the fractions against T, the ratio chart, the cake
rows with the peak and the value table; for part b the lines q (1 - p) against y = 1 and
the table for other q. The drawing code lives in cake.py; tests/0028 checks that the page
copies match.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cake as c  # noqa: E402

A, Q = Fr(1, 100), Fr(3, 2)
QS = [Fr(2), Fr(3, 2), Fr(11, 10)]


def q_table(a=A):
    lines = ["| ‏\\( q \\) | הסף \\( 1 - 1/q \\) | ‏\\( \\log_q \\frac{q - 1}{a} \\) | המקבל הגדול | חלקו |",
             "|---|---|---|---|---|"]
    for q in QS:
        rows = c.split(c.GEO, a, q)
        peak, top = c.best(rows)
        x = math.log(float((q - 1) / a)) / math.log(float(q))
        lines.append(f"| ‏{c.short(q)} | ‏{float(1 - 1 / q):.3f} | ‏{x:.2f} | האדם ה-{peak[0]} | ‏{c.dec(top, 3)} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(c.cake_rows(c.GEO, Fr(1, 10), Fr(2), show_peak=False), "\n")
    print(c.cake_legend(False), "\n")
    print(c.shares_chart(c.GEO, A, Q), "\n")
    print(c.shares_legend(), "\n")
    print(c.fraction_chart(c.GEO, A, Q), "\n")
    print(c.fraction_legend(), "\n")
    print(c.ratio_chart(c.GEO, A, Q), "\n")
    print(c.ratio_legend(), "\n")
    print(c.cake_rows(c.GEO, A, Q), "\n")
    print(c.cake_legend(), "\n")
    print(c.table(c.GEO, A, Q), "\n")
    print(c.g_lines(A), "\n")
    print(c.g_legend(), "\n")
    print(q_table())
