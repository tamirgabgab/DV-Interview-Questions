#!/usr/bin/env python3
"""Chart of question 0006 (one trade, long or short, on a list of daily prices).

    python tools/figures/fill.py 6         # put the blocks on the page

blocks() returns the legend and the price chart of the page example: the price per day,
the running minimum (used by the long trade) and the running maximum (used by the short
trade), and the best trade of each kind as a thick segment. tests/0006 checks the trades
against the page code and the page copy against this file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

PRICES = [5, 8, 3, 9, 2, 6]


def best_trades(prices=PRICES):
    """((long profit, buy day, sell day), (short profit, sell day, buy day)) by brute force."""
    long = max(((prices[j] - prices[i], i, j) for i in range(len(prices))
                for j in range(i + 1, len(prices))), key=lambda t: (t[0], -t[1], -t[2]))
    short = max(((prices[i] - prices[j], i, j) for i in range(len(prices))
                 for j in range(i + 1, len(prices))), key=lambda t: (t[0], -t[1], -t[2]))
    return long, short


def running(prices, pick):
    out, cur = [], prices[0]
    for p in prices:
        cur = pick(cur, p)
        out.append(cur)
    return out


def legend():
    return ('<span class="viz-legend"><span><i class="ink"></i>מחיר המניה</span>'
            '<span><i class="s1"></i>המינימום עד כה (לונג)</span>'
            '<span><i class="s2"></i>המקסימום עד כה (שורט)</span></span>')


def chart(prices=PRICES):
    n = len(prices)
    (lp, lb, ls), (sp, ss, sb) = best_trades(prices)
    c = Chart("גרף מחירי המניה לפי יום, עם המינימום והמקסימום עד כה ועסקאות הלונג והשורט הטובות ביותר",
              w=640, h=300, x0=44, right=40, top=20, base=260, x_max=n - 1, y_max=10)
    c.grid_y(range(0, 11, 2))
    for d in range(n):
        c.add(f'<text class="tick" x="{c.X(d):.1f}" y="{c.base + 26}" text-anchor="middle" direction="rtl">יום {d}</text>')
    for series, cls in ((running(prices, min), "s1-line"), (running(prices, max), "s2-line")):
        d = f"M{c.X(0):.1f},{c.Y(series[0]):.1f}" + "".join(
            f" H{c.X(i):.1f} V{c.Y(v):.1f}" for i, v in enumerate(series) if i)
        c.add(f'<path class="{cls}" d="{d}" fill="none" stroke-width="2"/>')
    for (a, b), cls in (((lb, ls), "s1-line"), ((ss, sb), "s2-line")):
        c.add(f'<line class="{cls}" x1="{c.X(a):.1f}" y1="{c.Y(prices[a]):.1f}" x2="{c.X(b):.1f}" '
              f'y2="{c.Y(prices[b]):.1f}" stroke-width="8" opacity="0.35"/>')
    c.path(list(enumerate(prices)), "ink-line")
    for d, p in enumerate(prices):
        up = d > 0 and p > prices[d - 1] or d == 0 and p >= prices[1]
        c.dot(d, p, "ink", r=5, title=f"יום {d}: מחיר {p}", label=p, dy=-11 if up else 20, label_size=12)
    c.text((lb + ls) / 2, 5.8, f"long +{lp}", anchor="end", dx=-12)
    c.text((ss + sb) / 2, 5.8, f"short +{sp} ✓", anchor="start", dx=12)
    return c.svg()


def blocks():
    """The generated blocks, in page order."""
    return [legend(), chart()]


if __name__ == "__main__":
    print(best_trades())
    print("\n\n".join(blocks()))
