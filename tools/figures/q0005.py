#!/usr/bin/env python3
"""Chart of question 0005 (smallest multiple of x written with the digits 0 and 1).

    python tools/figures/fill.py 5         # put the blocks on the page

blocks() returns the legend and the log-scale bar chart that compare the number of steps
of the three methods for x in 7, 9, 99, 999, 9999: scanning the multiples of x (y / x
candidates), enumerating the 0/1 numbers in order (the answer read as binary is its
position), and the BFS over remainders (dequeued remainders). tests/0005 checks the step
counts against the page code and the page copy against this file.
"""

import math
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

XS = [7, 9, 99, 999, 9999]
METHODS = [("by-multiples", "מעבר על כפולות של x"), ("by-enum", "מעבר על מספרי 0/1"),
           ("by-bfs", "BFS על שאריות")]


def smallest_01_multiple(x):
    """The answer as a string and the number of remainders the BFS dequeues."""
    parent, digit, visited = [-1] * x, [""] * x, [False] * x
    start = 1 % x
    visited[start], digit[start] = True, "1"
    queue, steps = deque([start]), 0
    while not visited[0]:
        r = queue.popleft()
        steps += 1
        for d in (0, 1):
            nr = (r * 10 + d) % x
            if not visited[nr]:
                visited[nr], parent[nr], digit[nr] = True, r, str(d)
                queue.append(nr)
    out, r = [], 0
    while r != -1:
        out.append(digit[r])
        r = parent[r]
    return "".join(reversed(out)), steps


def steps(x):
    """(multiples scanned, 0/1 numbers enumerated, remainders dequeued) for x."""
    y, bfs = smallest_01_multiple(x)
    return int(y) // x, int(y, 2), bfs


def fmt(n):
    """A count with thousands separators, or in scientific notation past twelve digits."""
    if n < 10 ** 12:
        return f"{n:,}"
    e = int(math.log10(n))
    return f"{n / 10 ** e:.2f}·10^{e}"


def legend():
    return ('<span class="viz-legend">' +
            "".join(f'<span><i class="{cls}"></i>{name}</span>' for cls, name in METHODS) + "</span>")


def chart():
    c = Chart("השוואת מספר הצעדים של שלוש השיטות, בסקאלה לוגריתמית", w=640, h=280, x0=64,
              right=16, top=18, base=252, slots=len(XS), y_min=1, y_max=10 ** 32, log=True)
    ticks = [10 ** e for e in range(0, 33, 4)]
    c.grid_y(ticks, labels=[f'10<tspan dy="-6" font-size="9">{e}</tspan>' for e in range(0, 33, 4)])
    bw = c.slot * 0.26
    for i, x in enumerate(XS):
        counts = steps(x)
        for k, ((cls, name), n) in enumerate(zip(METHODS, counts)):
            X = c.X(i + 1) + (k - 1) * bw
            Y = c.Y(n)
            c.add(f'<rect class="bar {cls}" x="{X - bw / 2:.1f}" y="{Y:.1f}" width="{bw:.1f}" '
                  f'height="{c.base - Y:.1f}" rx="2"><title>{name}, x = {x} : {fmt(n)} צעדים</title></rect>')
    c.x_ticks(range(1, len(XS) + 1), labels=[f"x = {x}" for x in XS])
    c.axis()
    return c.svg()


def blocks():
    """The generated blocks, in page order."""
    return [legend(), chart()]


if __name__ == "__main__":
    for x in XS:
        print(x, steps(x))
    print("\n\n".join(blocks()))
