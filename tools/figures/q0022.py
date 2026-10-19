#!/usr/bin/env python3
"""Figures and tables of question 0022 (the Josephus problem with "one stays, two leave",
and the general "one stays, L - 1 leave").

    python tools/figures/q0022.py > /tmp/q0022.html

Prints, in page order: the step-through circle for N = 30, the round-by-round table for
N = 30, the values table for N = 1..20 (L = 3), the survivor chart for N = 1..60 (L = 3),
the relabelling figure after one step, the one-round figure for N = 9; then for the bonus
part the zero-point table for L = 2..5, the values table for L = 4 and the chart for L = 4.
The drawing code lives in q0016.py; tests/0022 checks that the page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import q0016 as j  # noqa: E402

if __name__ == "__main__":
    print(j.circle_stepper(30, 3), "\n")
    print(j.rounds_table(30, 3), "\n")
    print(j.values_table(3, 20), "\n")
    print(j.chart_legend(3), "\n")
    print(j.chart(3, 60, 6), "\n")
    print(j.relabel_svg(8, 3), "\n")
    print(j.round_svg(9, 3), "\n")
    print(j.zeros_table(), "\n")
    print(j.values_table(4, 20, with_residue=True), "\n")
    print(j.chart_legend(4), "\n")
    print(j.chart(4, 64, 8))
