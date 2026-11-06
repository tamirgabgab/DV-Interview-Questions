#!/usr/bin/env python3
"""Figures and tables of question 0089, coins you cannot make up (the Frobenius coin problem).

    python tools/figures/fill.py 89        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The functions above blocks() are the reference the question's tests use: the
smallest payable amount of every remainder mod the smallest coin (shortest paths), the
largest amount that cannot be paid, and a plain run over all the amounts.
"""

from __future__ import annotations

import heapq
import sys
from functools import reduce
from html import escape
from math import gcd, inf
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "


# --- the reference ---------------------------------------------------------------------------------

def payable(coins, upto):
    """ok[n] for n = 0..upto: can n be paid with any number of each coin?"""
    ok = [True] + [False] * upto
    for n in range(1, upto + 1):
        ok[n] = any(c <= n and ok[n - c] for c in coins)
    return ok


def apery(coins):
    """dist[r]: the smallest payable amount with remainder r mod a = min(coins) (inf when
    none), last[r]: the coin added last on the way to it, and the order in which Dijkstra
    settles the remainders, [(r, dist), ...]."""
    a = min(coins)
    dist, last, order = [0] + [inf] * (a - 1), [None] * a, []
    heap = [(0, 0)]
    while heap:
        d, r = heapq.heappop(heap)
        if d > dist[r]:
            continue
        order.append((r, d))
        for c in coins:
            nd, nr = d + c, (r + c) % a
            if nd < dist[nr]:
                dist[nr], last[nr] = nd, c
                heapq.heappush(heap, (nd, nr))
    return dist, last, order


def coins_of(coins, r):
    """The coins of the smallest payable amount with remainder r, largest first."""
    dist, last, _ = apery(coins)
    a, out = min(coins), []
    while dist[r] > 0:
        c = last[r]
        out.append(c)
        r = (r - c) % a
    return sorted(out, reverse=True)


def frob(coins):
    """The largest amount that cannot be paid, or None when gcd(coins) > 1 (no largest)."""
    if reduce(gcd, coins) != 1:
        return None
    return max(apery(coins)[0]) - min(coins)


def dp_end(coins):
    """The plain run: amounts 1, 2, 3, ... until min(coins) payable amounts in a row; returns
    (the largest unpayable, the last amount checked)."""
    a = min(coins)
    ok, run, n = [True], 1, 0
    while run < a:
        n += 1
        ok.append(any(c <= n and ok[n - c] for c in coins))
        run = run + 1 if ok[n] else 0
    return n - a, n


def unpayable(coins):
    """Every amount that cannot be paid (gcd 1)."""
    g = frob(coins)
    ok = payable(coins, max(g, 0))
    return [n for n in range(g + 1) if not ok[n]]


# --- the blocks ----------------------------------------------------------------------------------

def wrap(label, rows, cls=""):
    return (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
            f'<table class="gs-bits fb-tab{(" " + cls) if cls else ""}" dir="ltr" aria-label="{escape(label)}"><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def cell_class(n, ok, g, a):
    if not ok:
        return "fb-no fb-g" if n == g else "fb-no"
    return "fb-ok fb-run" if g is not None and g < n <= g + a else "fb-ok"


def line_grid(coins, upto, label):
    """The amounts 0..upto in rows of ten (tens down the side, units across): payable or not,
    the largest unpayable framed, and the run of min(coins) payable amounts after it."""
    ok, g, a = payable(coins, upto), frob(coins), min(coins)
    rows = ["<tr><th></th>" + "".join(f'<td class="fb-ix">{u}</td>' for u in range(10)) + "</tr>"]
    for t in range(0, upto + 1, 10):
        tds = []
        for u in range(10):
            n = t + u
            tds.append(f'<td class="gs-b {cell_class(n, ok[n], g, a)}">{n}</td>' if n <= upto
                       else '<td class="gs-b fb-pad"></td>')
        rows.append(f"<tr><th>{t}</th>{''.join(tds)}</tr>")
    return wrap(label, rows, "fb-line")


def residue_grid(coins, rows_n, label):
    """The amounts in columns by their remainder mod a = min(coins): r + a·m down column r.
    Above the first payable amount of a column nothing is payable, from it on everything."""
    dist, _, _ = apery(coins)
    a, g = min(coins), frob(coins)
    rows = ["<tr><th>r</th>" + "".join(f'<td class="fb-ix">{r}</td>' for r in range(a)) + "</tr>"]
    for m in range(rows_n):
        tds = []
        for r in range(a):
            n = r + a * m
            if n < dist[r]:
                cls = "fb-no fb-g" if n == g else "fb-no"
            elif n == dist[r]:
                cls = "fb-ok fb-first"
            else:
                cls = "fb-ok"
            tds.append(f'<td class="gs-b {cls}">{n}</td>')
        rows.append(f"<tr><th></th>{''.join(tds)}</tr>")
    return wrap(label, rows, "fb-res")


def key(cls, text):
    return f'<span><i class="{cls}"></i><span>{text}</span></span>'


def legend_line(g, run):
    return ('<span class="viz-legend">' + key("fb-key-ok", "אפשר לשלם") + key("fb-key-no", "אי אפשר לשלם")
            + key("fb-key-g", f"הסכום הגדול ביותר שאי אפשר, {g}")
            + key("fb-key-run", f"{run} סכומים ברצף שאפשר, ומכאן הכול אפשר") + "</span>")


def legend_res(a):
    return ('<span class="viz-legend">' + key("fb-key-first", f"הסכום הראשון שאפשר בעמודה, וכל מה שמתחתיו אפשר (מוסיפים {a})")
            + key("fb-key-no", "אי אפשר לשלם") + key("fb-key-g", "הסכום הגדול ביותר שאי אפשר") + "</span>")


def part_a_line():
    return (line_grid((3, 5), 14, "הסכומים מ-0 עד 14 במטבעות של 3 ו-5 : אי אפשר לשלם 1, 2, 4 ו-7, "
                      "ואת 8, 9 ו-10 אפשר, ומהם כל סכום גדול יותר")
            + "\n\n" + legend_line(7, 3))


def part_a_residues():
    return (residue_grid((3, 5), 5, "הסכומים לפי השארית שלהם בחלוקה ל-3 : בעמודה של 0 הכול אפשר, "
                         "בעמודה של 1 הראשון שאפשר הוא 10, ובעמודה של 2 הראשון הוא 5")
            + "\n\n" + legend_res(3))


TWO = ((3, 5), (4, 7), (5, 8), (2, 9), (7, 11), (6, 9), (4, 10))


def examples_table():
    rows = ["| המטבעות | הגדול שאי אפשר | כמה סכומים אי אפשר |", "|:-:|:-:|:-:|"]
    for a, b in TWO:
        pair = f'{RLM}<span dir="ltr">{a}, {b}</span>'
        d = gcd(a, b)
        if d > 1:
            rows.append(f"| {pair} | אין, ה-gcd הוא {d} | אינסוף |")
            continue
        g, k = frob((a, b)), len(unpayable((a, b)))
        assert g == a * b - a - b and k == (a - 1) * (b - 1) // 2
        rows.append(f"| {pair} | {g} | {k} |")
    return "\n".join(rows)


def symmetry_table():
    a, b = 4, 7
    g = frob((a, b))
    ok = payable((a, b), g)
    half = g // 2
    top = "".join(f'<td class="gs-b {"fb-ok" if ok[n] else "fb-no"}">{n}</td>' for n in range(half + 1))
    bot = "".join(f'<td class="gs-b {"fb-ok" if ok[g - n] else "fb-no"}">{g - n}</td>' for n in range(half + 1))
    label = (f"מטבעות של {a} ו-{b}, הסכום הגדול שאי אפשר {g}. בכל עמודה זוג שמסתכם ל-{g}, "
             "ובכל זוג בדיוק אחד אפשר לשלם")
    return (wrap(label, [f"<tr><th>n</th>{top}</tr>", f"<tr><th>{g} − n</th>{bot}</tr>"], "fb-sym")
            + "\n\n" + '<span class="viz-legend">' + key("fb-key-ok", "אפשר לשלם") + key("fb-key-no", "אי אפשר לשלם")
            + "</span>")


def part_c_residues():
    return (residue_grid((6, 9, 20), 9, "הסכומים במטבעות של 6, 9 ו-20 לפי השארית בחלוקה ל-6. הסכומים הראשונים "
                         "שאפשר בכל עמודה : 0, 49, 20, 9, 40 ו-29. הגדול מהם 49, ולכן 43 הוא הגדול שאי אפשר")
            + "\n\n" + legend_res(6))


def order_table():
    coins = (6, 9, 20)
    dist, last, order = apery(coins)
    a = min(coins)
    rows = ["| הסדר | השארית | הראש של העמודה | איך מגיעים אליו |", "|:-:|:-:|:-:|---|"]
    for k, (r, d) in enumerate(order, 1):
        if d == 0:
            came = "ההתחלה, בלי מטבעות"
        else:
            c = last[r]
            came = f"הראש {dist[(r - c) % a]} של שארית {(r - c) % a}, ועוד מטבע של {c}"
        rows.append(f"| {k} | {r} | {d} | {came} |")
    return "\n".join(rows)


SETS = ((3, 5), (6, 9, 20), (5, 7, 9), (31, 37, 41), (101, 103, 107))


def cost_table():
    rows = ["| המטבעות | הגדול שאי אפשר | סכומים שהריצה הפשוטה בודקת | שאריות ש-Dijkstra מסדר |", "|:-:|:-:|:-:|:-:|"]
    for cs in SETS:
        g, end = dp_end(cs)
        rows.append(f'| {RLM}<span dir="ltr">{", ".join(map(str, cs))}</span> | {g:,} | {end:,} | {min(cs)} |')
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        part_a_line(),
        part_a_residues(),
        examples_table(),
        symmetry_table(),
        part_c_residues(),
        order_table(),
        cost_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
