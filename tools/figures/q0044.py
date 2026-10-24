#!/usr/bin/env python3
"""Figures of question 0044: the gap D_k (largest digit minus smallest) after k steps of
Kaprekar's routine on three digits, for every starting gap, in base 10 and in base 5.

    python tools/figures/fill.py 44        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Shared chart helpers are in charts.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402


def gaps(d0, base, k_max):
    """D_0 = d0, D_{k+1} = max(D_k - 1, base - D_k): the gap after each step."""
    out = [d0]
    for _ in range(k_max):
        out.append(max(out[-1] - 1, base - out[-1]))
    return out


def gap_chart(base, k_max, highlight, label):
    """Every starting gap 1..base-1 as a line of D_k against k; the one of the worked
    example emphasised, the fixed point (even base) or the two values of the cycle (odd)
    as dashed lines."""
    c = Chart(label, w=640, h=250, x0=46, right=16, top=16, base=212, x_min=0, x_max=k_max, y_max=base, y_min=0)
    c.grid_y(range(0, base + 1, 1 if base <= 6 else 1))
    c.grid_x(range(0, k_max + 1))
    if base % 2 == 0:
        c.hline(base // 2, f"D = {base // 2}", label_at="end")
    else:
        h = (base - 1) // 2
        c.hline(h, f"D = {h}", label_at="end").hline(h + 1, f"D = {h + 1}", label_at="end")
    for d0 in range(1, base):
        if d0 == highlight:
            continue
        c.path(list(enumerate(gaps(d0, base, k_max))), "s1-line", width=1.5, extra=' stroke-opacity="0.55"')
    path = gaps(highlight, base, k_max)
    c.path(list(enumerate(path)), "s2-line", width=3)
    for k, d in enumerate(path):
        c.dot(k, d, "s2", r=4, title=f"k = {k}: D = {d}")
    return c.axis("k").svg()


def legend(example):
    return ('<span class="viz-legend"><span><i class="s1"></i>כל פער התחלתי d₀</span>'
            f'<span><i class="s2"></i>{example}</span>'
            '<span><i class="ink"></i>נקודת השבת, או שני הערכים של המחזור</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [
        gap_chart(10, 8, 1, "הפער D_k אחרי k פעולות בבסיס 10, לכל פער התחלתי מ-1 עד 9; כולם מגיעים ל-5"),
        legend("הדוגמה 211, שבה d₀ = 1"),
        gap_chart(5, 8, 4, "הפער D_k אחרי k פעולות בבסיס 5, לכל פער התחלתי מ-1 עד 4; כולם נכנסים למחזור בין 2 ל-3"),
        legend("הדוגמה 401 בבסיס 5, שבה d₀ = 4"),
    ]


if __name__ == "__main__":
    print([gaps(d, 10, 8) for d in range(1, 10)])
    print([gaps(d, 5, 8) for d in range(1, 5)])
