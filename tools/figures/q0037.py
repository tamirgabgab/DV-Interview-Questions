#!/usr/bin/env python3
"""Table and chart of question 0037 (MTBF of a synchronizer: one, two and three flops).

    python tools/figures/fill.py 37        # put the blocks on the page

MTBF = exp(t_res / tau) / (T0 * f_clk * f_data), with t_res = N * T_clk - t_overhead the
time the N flops leave for the first one to resolve (t_overhead = setup + clock-to-q).
The page example: f_clk 500 MHz, f_data 50 MHz, tau 100 ps, T0 50 ps, overhead 0.3 ns.
blocks() returns, in page order: the table of the example at 500 MHz and 1 GHz for one
to three flops, the legend and the chart of MTBF against the clock frequency for the
three depths. tests/0037 checks the numbers against the page code.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

F_CLK, F_DATA, TAU, T0, OVERHEAD = 500e6, 50e6, 100e-12, 50e-12, 0.3e-9
YEAR = 365.25 * 86400
RLM = "‏"


def mtbf(f_clk, f_data, tau, t0, t_overhead, flops):
    """Seconds between failures; 0 when nothing is left to resolve."""
    t_res = flops / f_clk - t_overhead
    if t_res <= 0:
        return 0.0
    return math.exp(t_res / tau) / (t0 * f_clk * f_data)


def human(seconds):
    """A readable duration: the largest unit that is at least one."""
    if seconds <= 0:
        return "0"
    for name, unit in (("שנים", YEAR), ("ימים", 86400), ("שעות", 3600), ("דקות", 60), ("שניות", 1), ("ms", 1e-3), ("µs", 1e-6)):
        if seconds >= unit:
            v = seconds / unit
            text = f"{v:.3g}" if v < 1e6 else f"{v:.2e}".replace("e+", "·10^")
            return f"{text} {name}"
    return f"{seconds:.2e} s"


CLOCKS = (500e6, 1e9)


def cases_table():
    rows = ["| שעון | פלופים | ‏\\( t_{res} \\) | ‏\\( e^{t_{res}/\\tau} \\) | ‏MTBF |", "|:-:|:-:|:-:|:-:|:-:|"]
    for f in CLOCKS:
        for n in (1, 2, 3):
            t_res = n / f - OVERHEAD
            rows.append(f"| {RLM}{f / 1e6:g} MHz | {RLM}{n} | {RLM}{t_res * 1e9:.1f} ns | {RLM}{math.exp(t_res / TAU):.2e} "
                        f"| {RLM}{human(mtbf(f, F_DATA, TAU, T0, OVERHEAD, n))} |".replace("e+", "·10^"))
    return "\n".join(rows)


def legend():
    return ('<span class="viz-legend"><span><i class="s2"></i>פלופ אחד</span><span><i class="s1"></i>שני פלופים</span>'
            '<span><i class="s3"></i>שלושה פלופים</span><span><i class="ink"></i>שנה אחת, ואלף שנים</span></span>')


def chart():
    y_min, y_max = 1e-6, 1e24
    c = Chart("MTBF בשניות, בסקאלה לוגריתמית, כפונקציה של תדר השעון, לפלופ אחד, שניים ושלושה", w=640, h=300,
              x0=56, right=16, top=16, base=258, x_min=200, x_max=2000, y_min=y_min, y_max=y_max, log=True)
    ticks = [10.0 ** e for e in range(-6, 25, 6)]
    c.grid_y(ticks, labels=[f'10<tspan dy="-6" font-size="9">{e}</tspan>' for e in range(-6, 25, 6)])
    c.grid_x(range(200, 2001, 300), labels=[f"{v} MHz" for v in range(200, 2001, 300)])
    for v, label in ((YEAR, "שנה"), (1000 * YEAR, "אלף שנים")):
        c.hline(v, None, width=1)
        c.add(f'<text class="legend" x="{c.x1 - 4}" y="{c.Y(v) - 5:.1f}" text-anchor="start" direction="rtl">{label}</text>')
    for n, cls in ((1, "s2"), (2, "s1"), (3, "s3")):
        pts = []
        for f_mhz in range(200, 2001, 10):
            v = mtbf(f_mhz * 1e6, F_DATA, TAU, T0, OVERHEAD, n)
            if v <= 0 or v > y_max:          # above the frame: the curve starts where it enters
                continue
            pts.append((f_mhz, max(v, y_min)))
        c.path(pts, f"{cls}-line", width=2)
    for n, cls in ((1, "s2"), (2, "s1"), (3, "s3")):
        v = mtbf(F_CLK, F_DATA, TAU, T0, OVERHEAD, n)
        c.dot(500, min(v, y_max), cls, r=4.5, title=f"{n} flops at 500 MHz : {human(v)}")
    c.axis()
    return c.svg()


def blocks():
    """The generated blocks, in page order."""
    return [cases_table(), legend(), chart()]


if __name__ == "__main__":
    for f in CLOCKS:
        print(f, [human(mtbf(f, F_DATA, TAU, T0, OVERHEAD, n)) for n in (1, 2, 3)])
    print("\n\n".join(blocks()))
