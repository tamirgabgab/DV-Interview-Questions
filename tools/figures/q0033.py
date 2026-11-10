#!/usr/bin/env python3
"""Figures and tables of question 0033 (FIFO depth from the write and read rates).

    python tools/figures/fill.py 33        # put the blocks on the page

The example: a burst of 120 words written one per cycle at 100 MHz, read one per cycle at
80 MHz (part a), or read with one idle read slot in every four (part b). blocks() returns,
in page order (all in part b's proof): the legend and the fill-level chart of both readers
over the burst, and the table of a few bursts and rates with the formula against the cycle
simulation. The formula is exact (fractions, no floating point); the simulation of the table
runs on a time step that divides both periods (1 / (f_w f_r / gcd) us), so it is exact too.
tests/0033 checks the numbers and that the page copies match.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

BURST, F_WRITE, F_READ = 120, 100, 80          # words, MHz, MHz
UNIT = 0.05                                      # ns per simulation step (20 steps = 1 ns)
T_WRITE, T_READ = round(1000 / F_WRITE / UNIT), round(1000 / F_READ / UNIT)   # 200, 250 steps
IDLE_EVERY = 4                                   # part b: the reader skips one read slot in four
RLM = "‏"


def depth(burst, f_write, f_read, idle_every=0):
    """The closed form, exact: words left when the burst ends, the reader draining at its
    rate (one read slot in idle_every skipped), at least 1."""
    rate = Fraction(f_read) / Fraction(f_write)
    if idle_every:
        rate *= 1 - Fraction(1, idle_every)
    return max(1, math.ceil(burst * (1 - rate)))


def periods(f_write, f_read):
    """Exact integer periods (t_write, t_read) for two rates in MHz: the step is
    1 / (f_write f_read / g) us with g = gcd, so a write cycle is f_read / g steps."""
    g = math.gcd(f_write, f_read)
    return f_read // g, f_write // g


def fill(burst, t_write, t_read, idle_every=0, phase=0):
    """Cycle simulation: (max fill, trace of (step, fill) at every change). A write lands at
    step k * t_write, a read edge comes at every step t > 0 with t % t_read == phase, and the
    reader skips one read slot in idle_every; the fill is measured after the write and before
    the read of the same step."""
    count = written = slot = t = max_fill = 0
    trace = [(0, 0)]
    while written < burst or count > 0:
        if t % t_write == 0 and written < burst:
            count += 1
            written += 1
            trace.append((t, count))
        max_fill = max(max_fill, count)
        if t > 0 and t % t_read == phase:
            slot += 1
            if not (idle_every and slot % idle_every == 0) and count > 0:
                count -= 1
                trace.append((t, count))
        t += 1
    return max_fill, trace


def legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>קורא ב-80 MHz, כל מחזור</span>'
            '<span><i class="s2"></i>קורא ב-80 MHz, מדלג על קריאה אחת מכל ארבע</span>'
            '<span><i class="ink"></i>הנוסחה : 24 ו-48</span></span>')


def fill_chart():
    a_max, a = fill(BURST, T_WRITE, T_READ)
    b_max, b = fill(BURST, T_WRITE, T_READ, IDLE_EVERY)
    end_ns = max(a[-1][0], b[-1][0]) * UNIT
    x_max = math.ceil(end_ns / 250) * 250
    c = Chart("רמת המילוי של ה-FIFO לאורך הזמן, לשני הקוראים; הקו המקווקו הוא הנוסחה", w=640, h=260,
              x0=44, right=16, top=16, base=222, x_max=x_max, y_max=60)
    c.grid_y(range(0, 61, 10))
    c.grid_x(range(0, x_max + 1, 250), labels=[f"{v} ns" if v else "0" for v in range(0, x_max + 1, 250)])
    for trace, cls in ((a, "s1-line"), (b, "s2-line")):
        pts = []
        for i, (t, v) in enumerate(trace):
            if i:
                pts.append((t * UNIT, trace[i - 1][1]))     # a step: hold the old value until t
            pts.append((t * UNIT, v))
        c.path(pts, cls, width=2)
    for v, label in ((depth(BURST, F_WRITE, F_READ), "24"), (depth(BURST, F_WRITE, F_READ, IDLE_EVERY), "48")):
        c.hline(v, None, cls="ink-line", width=1, dash="6 4")
        c.add(f'<text class="legend" x="{c.x1 - 4}" y="{c.Y(v) - 5:.1f}" text-anchor="end">{label}</text>')
    c.text(BURST * 1000 / F_WRITE, 58, "סוף הפרץ", anchor="middle", rtl=True)
    c.vline(BURST * 1000 / F_WRITE, 56)
    c.axis()
    return c.svg()


CASES = [(120, 100, 80, 0), (120, 100, 80, 4), (64, 200, 150, 0), (256, 100, 50, 0), (100, 100, 99, 0), (32, 125, 100, 2),
         (64, 100, 70, 3)]


def cases_table():
    rows = ["| הפרץ | כתיבה | קריאה | הקורא מדלג | הנוסחה | הסימולציה |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for burst, fw, fr, idle in CASES:
        sim = fill(burst, *periods(fw, fr), idle)[0]
        skip = f"אחת מכל {idle}" if idle else "לא"
        rows.append(f"| {RLM}{burst} | {RLM}{fw} MHz | {RLM}{fr} MHz | {skip} | {RLM}{depth(burst, fw, fr, idle)} | {RLM}{sim} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [legend(), fill_chart(), cases_table()]


if __name__ == "__main__":
    print(depth(BURST, F_WRITE, F_READ), fill(BURST, T_WRITE, T_READ)[0])
    print(depth(BURST, F_WRITE, F_READ, IDLE_EVERY), fill(BURST, T_WRITE, T_READ, IDLE_EVERY)[0])
    print("\n\n".join(blocks()))
