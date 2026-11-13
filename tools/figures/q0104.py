#!/usr/bin/env python3
"""Figures and tables of question 0104, gas stations on a circle: from which station can a car
with an empty tank of unlimited size drive a full lap, taking gas[i] at station i and paying
cost[i] for the leg from i to the next station.

    python tools/figures/fill.py 104        # put the blocks on the page

The references here are independent of the page code:

- walk(gas, cost, s) drives the lap from s leg by leg and returns the tank after every leg,
  up to the first one that goes below zero; good(gas, cost) is every start whose walk is a
  whole lap (the brute force, O(n^2)).
- levels(gas, cost) are the levels P_0 .. P_n, P_k = d_0 + ... + d_(k-1) with d = gas - cost:
  the tank on arriving at station k from station 0 if the tank were allowed below zero.
  by_levels(gas, cost) lists the good starts by the page's condition of part c (S >= 0,
  P_s <= every later level of the lap and P_s <= every earlier level + S), checked in O(n^2).
- one_pass(gas, cost) is the greedy restart of part b, written here again.

blocks() returns, in page order: the example ring and its legend, part a's table of the tank
from every start, the two-lap chart of the example's levels and its legend, part b's table of
the one pass, the chart of the levels of the ring with sum 0 and four good starts, the two-lap
chart of the ring with sum 3 and its legend, and part c's table of that ring's conditions.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from charts import Chart  # noqa: E402

RLM = "‏"
NB = " "
MINUS = "−"

# the rings of the page and of the box: (gas, cost)
EXAMPLE = ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])          # the statement: sum 0, one start, 3
NONE = ([2, 3, 4], [3, 4, 3])                        # sum -1: no start
ZERO = ([3, 1, 2, 1, 2, 2, 1], [1, 3, 1, 2, 2, 1, 2])  # part c: sum 0, four good starts
MORE = ([1, 3, 2, 3, 4], [2, 1, 3, 2, 2])            # part c: sum 3, starts 1, 3, 4; the minimum only 1


# --- the reference ---------------------------------------------------------------------------------

def diffs(gas, cost) -> list[int]:
    return [g - c for g, c in zip(gas, cost)]


def walk(gas, cost, s: int) -> list[int]:
    """The tank after every leg of the lap from s, up to and with the first that is negative."""
    n, tank, out = len(gas), 0, []
    for k in range(n):
        i = (s + k) % n
        tank += gas[i] - cost[i]
        out.append(tank)
        if tank < 0:
            break
    return out


def good(gas, cost) -> list[int]:
    """Every station from which the lap never runs dry, by driving it."""
    n = len(gas)
    return [s for s in range(n) if len(walk(gas, cost, s)) == n and walk(gas, cost, s)[-1] >= 0]


def legs_naive(gas, cost) -> int:
    """How many legs part a's search drives before it answers (it stops at the first good start)."""
    total = 0
    for s in range(len(gas)):
        w = walk(gas, cost, s)
        total += len(w)
        if len(w) == len(gas) and w[-1] >= 0:
            break
    return total


def levels(gas, cost) -> list[int]:
    p = [0]
    for x in diffs(gas, cost):
        p.append(p[-1] + x)
    return p


def by_levels(gas, cost) -> list[int]:
    """Part c's condition, checked level by level."""
    p, n = levels(gas, cost), len(gas)
    S = p[n]
    if S < 0:
        return []
    return [s for s in range(n) if all(p[s] <= p[k] for k in range(s + 1, n + 1)) and all(p[s] <= p[k] + S for k in range(s))]


def at_min(gas, cost) -> list[int]:
    """The stations whose level is the lowest of P_0 .. P_(n-1)."""
    p, n = levels(gas, cost), len(gas)
    m = min(p[:n])
    return [s for s in range(n) if p[s] == m]


def one_pass(gas, cost) -> tuple[int, list[dict]]:
    """Part b's greedy restart, with its state after every station."""
    start = tank = total = 0
    low, rows = 0, []
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        tank += d
        total += d
        dry = tank if tank < 0 else None
        if dry is not None:
            start, tank = i + 1, 0
        low = min(low, total)
        rows.append(dict(i=i, d=d, total=total, low=low, tank=tank, start=start, dry=dry))
    return (start if total >= 0 else -1), rows


# --- formatting --------------------------------------------------------------------------------------

def num(v: int) -> str:
    """A whole number with a true minus sign (U+2212)."""
    return f"{MINUS}{-v}" if v < 0 else str(v)


def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def cellnum(v: int) -> str:
    """A number for a table cell: a negative one in an LTR span after an RLM, so the minus stays
    on its left in a right-to-left cell."""
    return f"{RLM}{ltr(num(v))}" if v < 0 else str(v)


def numlist(vs) -> str:
    return ltr(", ".join(num(v) for v in vs))


# --- the ring ------------------------------------------------------------------------------------

def ring_svg(gas, cost, label, good_set=(), start=None) -> str:
    """The stations on a circle, clockwise from the top: each with its number, the gas it gives
    (+, outside) and the cost of the leg to the next one (-, inside the circle, on the arrow)."""
    n = len(gas)
    W, H, cx, cy, R, r = 360, 316, 180, 158, 104, 17
    ang = lambda k: -math.pi / 2 + 2 * math.pi * k / n  # noqa: E731
    pt = lambda a, rad: (cx + rad * math.cos(a), cy + rad * math.sin(a))  # noqa: E731
    o = [f'<svg class="figure gs-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" direction="ltr" role="img" aria-label="{label}">']
    gap = (r + 5) / R
    for i in range(n):
        a0, a1 = ang(i) + gap, ang(i + 1) - gap - 0.06
        x0, y0 = pt(a0, R)
        x1, y1 = pt(a1, R)
        tip = pt(ang(i + 1) - gap, R)
        tx, ty = -math.sin(ang(i + 1) - gap), math.cos(ang(i + 1) - gap)   # the tangent, clockwise
        nx, ny = math.cos(ang(i + 1) - gap), math.sin(ang(i + 1) - gap)
        bx, by = tip[0] - 8 * tx, tip[1] - 8 * ty
        head = f"M{tip[0]:.1f},{tip[1]:.1f} L{bx + 4.5 * nx:.1f},{by + 4.5 * ny:.1f} L{bx - 4.5 * nx:.1f},{by - 4.5 * ny:.1f} Z"
        mx, my = pt((ang(i) + ang(i + 1)) / 2, R - 26)
        o.append(f'<g class="gs-leg"><title>leg {i} → {(i + 1) % n}: costs {cost[i]}</title>'
                 f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}" fill="none"/><path class="gs-head" d="{head}"/>'
                 f'<text class="gs-cost" x="{mx:.1f}" y="{my + 4.5:.1f}" text-anchor="middle">{num(-cost[i])}</text></g>')
    for i in range(n):
        x, y = pt(ang(i), R)
        gx, gy = pt(ang(i), R + 34)
        cls = " is-good" if i in good_set else ""
        cls += " is-start" if i == start else ""
        o.append(f'<g class="gs-st{cls}"><title>station {i}: gas {gas[i]}</title><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
                 f'<text class="gs-num" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{i}</text>'
                 f'<text class="gs-gas" x="{gx:.1f}" y="{gy + 5:.1f}" text-anchor="middle">+{gas[i]}</text></g>')
    o.append("</svg>")
    return "".join(o)


def ring_legend() -> str:
    return ('<span class="viz-legend"><span><i class="gs-key-gas"></i>הדלק שמקבלים בתחנה (+)</span>'
            '<span><i class="gs-key-cost"></i>המחיר של הקטע לתחנה הבאה (−)</span>'
            '<span><i class="gs-key-good"></i>תחנה שממנה אפשר להשלים סיבוב</span></span>')


# --- the charts of the levels ------------------------------------------------------------------------

def lap_chart(gas, cost, label, laps=2, window=None, floors=(), show_values=True) -> str:
    """The levels P_0 .. P_(laps n), the second lap P_k + S, against the station of every point.
    `window` shades the lap from that start (the tank is the height above its floor), `floors`
    draws the dashed floor of every start named, the lowest level of the first lap is the
    dotted line, and the first lap's good starts are green."""
    p, n = levels(gas, cost), len(gas)
    S = p[n]
    q = [p[k % n] + (k // n) * S for k in range(laps * n + 1)]
    goods, low = set(good(gas, cost)), min(p[:n])
    lo, hi = min(q) - 1, max(q) + 1
    c = Chart(label, w=640, h=232, x0=40, right=14, top=22, base=196, x_min=-0.5, x_max=laps * n + 0.5, y_min=lo, y_max=hi)
    c.parts[0] = c.parts[0].replace('class="perf-chart"', 'class="perf-chart gs-chart"')
    if window is not None:
        c.add(f'<rect class="gs-win" x="{c.X(window - 0.35):.1f}" y="{c.top - 6}" width="{c.X(window + n + 0.35) - c.X(window - 0.35):.1f}" height="{c.base - c.top + 6}" rx="4"/>')
    step = 1 if hi - lo <= 8 else 2
    ticks = [v for v in range(math.ceil(lo), math.floor(hi) + 1) if v % step == 0]
    c.grid_y(ticks, labels=[num(v) for v in ticks])
    for k in range(1, laps):
        X = c.X(k * n)
        c.add(f'<line class="gs-lap" x1="{X:.1f}" x2="{X:.1f}" y1="{c.top - 8}" y2="{c.base}"/>')
    c.add(f'<line class="gs-low" x1="{c.x0}" x2="{c.x1}" y1="{c.Y(low):.1f}" y2="{c.Y(low):.1f}"/>')
    for s in floors:
        c.add(f'<line class="gs-floor" x1="{c.X(s):.1f}" x2="{c.X(s + n):.1f}" y1="{c.Y(p[s]):.1f}" y2="{c.Y(p[s]):.1f}"/>')
    c.path([(k, v) for k, v in enumerate(q)], "gs-line", width=2)
    for k, v in enumerate(q):
        st = k % n
        cls = "gs-pt"
        if k < n and st in goods:
            cls += " is-good"
        if k < n and p[st] == low:
            cls += " is-min"
        X, Y = c.X(k), c.Y(v)
        c.add(f'<circle class="{cls}" cx="{X:.1f}" cy="{Y:.1f}" r="{5.5 if "is-good" in cls else 4}"><title>P{k} = {num(v)}, station {st}</title></circle>')
        if show_values:
            c.add(f'<text class="gs-val" x="{X:.1f}" y="{Y - 9:.1f}" text-anchor="middle">{num(v)}</text>')
        c.add(f'<text class="tick" x="{X:.1f}" y="{c.base + 18}" text-anchor="middle">{st}</text>')
    c.axis()
    return c.svg()


def chart_legend(window=False, floors=False) -> str:
    parts = [f'<span><i class="gs-key-line"></i>הרמה \\( P_k \\){NB}: סכום ה-\\( d \\) עד התחנה, מתחנה 0</span>',
             '<span><i class="gs-key-low"></i>הרמה הנמוכה בסיבוב הראשון</span>',
             '<span><i class="gs-key-good"></i>תחנה שממנה אפשר להשלים סיבוב</span>']
    if window:
        parts.append(f'<span><i class="gs-key-win"></i>הסיבוב מתחנה 3{NB}: המכל הוא הגובה מעל הרמה שלה</span>')
    if floors:
        parts.append('<span><i class="gs-key-floor"></i>הרמה של תחנה טובה, לאורך הסיבוב ממנה</span>')
    parts.append(f'<span><i class="gs-key-lap"></i>תחילת הסיבוב השני{NB}: כל רמה גבוהה ב-\\( S \\)</span>')
    return '<span class="viz-legend">' + "".join(parts) + "</span>"


# --- the tables ----------------------------------------------------------------------------------------

def naive_table() -> str:
    gas, cost = EXAMPLE
    n = len(gas)
    head = "| התחנה ההתחלתית | " + " | ".join(f"קטע {k + 1}" for k in range(n)) + " | התוצאה |"
    rows = [head, "|:-:|" + ":-:|" * n + "---|"]
    for s in range(n):
        w = walk(gas, cost, s)
        cells = [cellnum(v) if v >= 0 else f"{RLM}**{ltr(num(v))}**" for v in w] + ["–"] * (n - len(w))
        if len(w) == n and w[-1] >= 0:
            res = "סיבוב שלם"
        else:
            j = (s + len(w) - 1) % n
            res = f"נתקעים בקטע {ltr(f'{j} → {(j + 1) % n}')}"
        rows.append(f"| {s} | " + " | ".join(cells) + f" | {res} |")
    return "\n".join(rows)


def pass_table() -> str:
    gas, cost = EXAMPLE
    _, rows = one_pass(gas, cost)
    out = [f"| התחנה \\( i \\) | {RLM}\\( d_i \\) | המכל מההתחלה הנוכחית | ההתחלה | הרמה \\( P_{{i+1}} \\) | הרמה הנמוכה עד כה |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        tank = cellnum(r["tank"]) if r["dry"] is None else f"{RLM}**{ltr(num(r['dry']))}**, מתחילים מחדש"
        out.append(f"| {r['i']} | {cellnum(r['d'])} | {tank} | {r['start']} | {cellnum(r['total'])} | {cellnum(r['low'])} |")
    return "\n".join(out)


def more_table() -> str:
    gas, cost = MORE
    p, n = levels(gas, cost), len(gas)
    S = p[n]
    goods = set(good(gas, cost))
    out = [f"| התחנה \\( s \\) | {RLM}\\( P_s \\) | הנמוכה אחריה בסיבוב | הנמוכה לפניה, ועוד \\( S \\) | המכל בסיבוב ממנה | טובה? |",
           "|:-:|:-:|:-:|:-:|---|:-:|"]
    for s in range(n):
        after = min(p[s + 1:n + 1])
        before = f"{RLM}{ltr(f'{num(min(p[:s]))} + {S} = {num(min(p[:s]) + S)}')}" if s else "אין"
        w = walk(gas, cost, s)
        tanks = f"{RLM}{numlist(w)}" + ("" if s in goods else ", נתקעים")
        ok = "כן" if s in goods else "לא"
        out.append(f"| {s} | {cellnum(p[s])} | {cellnum(after)} | {before} | {tanks} | {ok} |")
    return "\n".join(out)


# --- the blocks ----------------------------------------------------------------------------------------

def blocks():
    gas, cost = EXAMPLE
    return [
        ring_svg(gas, cost, f"הדוגמה{NB}: חמש תחנות על מעגל, 0 עד 4 בכיוון השעון. הדלק בתחנות 1, 2, 3, 4, 5 והמחיר של הקטעים 3, 4, 5, 1, 2. "
                 f"תחנה 3 מסומנת{NB}: ממנה אפשר להשלים סיבוב", good_set=set(good(gas, cost))),
        ring_legend(),
        naive_table(),
        lap_chart(gas, cost, f"הרמות של הדוגמה לאורך שני סיבובים{NB}: 0, −2, −4, −6, −3, 0 ושוב. הנמוכה, −6, לפני תחנה 3. "
                  "הסיבוב מתחנה 3 מוצלל, וכל הרמות בו לפחות −6", window=3),
        chart_legend(window=True),
        pass_table(),
        lap_chart(*ZERO, f"הרמות של הטבעת עם הסכום 0{NB}: 0, 2, 0, 1, 0, 0, 1 ובסוף שוב 0. הרמה הנמוכה, 0, מתקבלת לפני התחנות 0, 2, 4 ו-5, "
                  "ואלה ארבע התחנות הטובות", laps=1),
        lap_chart(*MORE, f"הרמות של הטבעת עם הסכום 3 לאורך שני סיבובים{NB}: 0, −1, 1, 0, 1, ובסיבוב השני כל אחת גבוהה ב-3. "
                  f"הרמה הנמוכה רק לפני תחנה 1, אבל גם 3 ו-4 טובות{NB}: מכל אחת מהן הסיבוב לא יורד מתחת לרמה שלה", floors=good(*MORE)),
        chart_legend(floors=True),
        more_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
