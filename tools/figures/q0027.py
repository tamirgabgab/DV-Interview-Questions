#!/usr/bin/env python3
"""Figures and tables of question 0027 (a cake split by fractions that grow as an
arithmetic sequence).

    python tools/figures/q0027.py > /tmp/q0027.html

Prints, in page order: the statement figure (a = d = 0.2, no peak marked); for part a
(a = 0.01, d = 0.1) the shares bars, the fractions against T, the ratio chart (log scale),
the cake rows with the peak and the value table; for part b the curve p^2 / (1 - p)
against y = d and the table of more examples. The drawing code lives in cake.py;
tests/0027 checks that the page copies match.
"""

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cake as c  # noqa: E402

A, D = Fr(1, 100), Fr(1, 10)
EXAMPLES = [  # (a, d, how the parameters are written, note)
    (Fr(1, 100), Fr(1, 10), "‏\\( a = 0.01,\\ d = 0.1 \\)", "סעיף א"),
    (Fr(1, 10), Fr(1, 10), "‏\\( a = d = 0.1 \\)", "‏\\( 12 \\ge 10 \\)"),
    (Fr(1, 100), Fr(1, 100), "‏\\( a = d = 0.01 \\)", "‏\\( 110 \\ge 100 \\)"),
    (Fr(1, 12), Fr(1, 12), "‏\\( a = d = 1/12 \\)", "‏\\( 12 = 12 \\)"),
]


def winner(a, d):
    peak, _ = c.best(c.split(c.ARITH, a, d))
    return f"תיקו בין ה-{peak[0]} ל-{peak[1]}" if len(peak) > 1 else f"האדם ה-{peak[0]}"


def examples_table():
    lines = ["| הפרמטרים | הסף \\( T \\) | המקבל הגדול | הערה |", "|---|---|---|---|"]
    for a, d, name, note in EXAMPLES:
        lines.append(f"| {name} | ‏{c.threshold(c.ARITH, d):.3f} | {winner(a, d)} | {note} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(c.cake_rows(c.ARITH, Fr(1, 5), Fr(1, 5), show_peak=False), "\n")
    print(c.cake_legend(False), "\n")
    print(c.shares_chart(c.ARITH, A, D), "\n")
    print(c.shares_legend(), "\n")
    print(c.fraction_chart(c.ARITH, A, D), "\n")
    print(c.fraction_legend(), "\n")
    print(c.ratio_chart(c.ARITH, A, D, log=True), "\n")
    print(c.ratio_legend(), "\n")
    print(c.cake_rows(c.ARITH, A, D), "\n")
    print(c.cake_legend(), "\n")
    print(c.table(c.ARITH, A, D), "\n")
    print(c.f_curve(A, D), "\n")
    print(c.f_legend(), "\n")
    print(examples_table())
