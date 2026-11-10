#!/usr/bin/env python3
"""Figures and tables of question 0074 (rotating a square image and transposing a matrix in place).

    python tools/figures/fill.py 74        # put the blocks on the page

The reference here is independent of the page code: the transpose is built entry by entry
from its definition (row-major m x n in, row-major n x m out), and its cycles are found by
following where each entry goes. blocks() returns, in page order: a 3 x 3 image rotated in
two steps, the 2 x 3 example in memory with its legend, the cycles of 3 x 5, the four
placements of 2 x 3 one by one, the cost of finding the leaders without marks, and for the
hardware follow-up the block diagram of the streaming transposer (two memories, ping-pong)
with its legend and a table of its clocks on 2 x 3. tests/0074 checks the page's numbers
and code against this module.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import table  # noqa: E402

from html import escape  # noqa: E402

RLM = "‏"
NB = "\u00a0"


def ltr(text):
    return f'<span dir="ltr">{text}</span>'


def own_legend(items):
    """A legend line whose texts are HTML (an LTR span for an ordered chain of numbers)."""
    return '<span class="viz-legend">' + "".join(f'<span><i class="{k}"></i>{t}</span>' for k, t in items) + "</span>"


def transposed(a, m, n):
    """The definition: entry (i, j) of the m x n matrix becomes entry (j, i) of the n x m one."""
    return [a[i * n + j] for j in range(n) for i in range(m)]


def rotated90(a):
    """A quarter turn clockwise of a square matrix given as rows: new[i][j] = old[n-1-j][i]."""
    n = len(a)
    return [[a[n - 1 - j][i] for j in range(n)] for i in range(n)]


def cycles(m, n):
    """The cycles of the transpose's permutation of places (where each entry goes)."""
    t = transposed(list(range(m * n)), m, n)
    where = {v: p for p, v in enumerate(t)}
    seen, out = set(), []
    for s in range(m * n):
        if s in seen:
            continue
        cyc, p = [], s
        while p not in seen:
            seen.add(p)
            cyc.append(p)
            p = where[p]
        out.append(cyc)
    return out


def leader_checks(m, n):
    """The steps of the walks that look for each cycle's leader without marks: from every s,
    the steps k -> k m mod (mn - 1) until the walk is back at s or below it."""
    size = m * n
    if size <= 2:
        return 0
    steps = 0
    for s in range(1, size - 1):
        k = s * m % (size - 1)
        steps += 1
        while k > s:
            k = k * m % (size - 1)
            steps += 1
    return steps


# --- the blocks ---------------------------------------------------------------------------

def rotate_table():
    n = 3
    a = [[f"{chr(97 + i * n + j)}" for j in range(n)] for i in range(n)]
    t = [[a[j][i] for j in range(n)] for i in range(n)]
    r = [row[::-1] for row in t]
    rows = []
    for i in range(n):
        cells = [(v, "c1") for v in a[i]] + [("", "is-gap")] + [(v, "c2" if i != j else "c3") for j, v in enumerate(t[i])] \
            + [("", "is-gap")] + [(v, "c1") for v in r[i]]
        rows.append((f"שורה {i}", cells, None))
    head = list(range(n)) + [""] + list(range(n)) + [""] + list(range(n))
    return table(rows, "תמונה 3 על 3 : המקורית, אחרי שחלוף (האלכסון לא זז), ואחרי היפוך של כל שורה, סיבוב של רבע סיבוב בכיוון השעון",
                 head=head)


def memory_table():
    m, n = 2, 3
    a = [chr(97 + i) for i in range(m * n)]
    cyc = {p: c for c, cs in enumerate(cycles(m, n)) for p in cs}
    t = transposed(a, m, n)
    rows = [("לפני", [(v, f"c{cyc[p] + 1}") for p, v in enumerate(a)], None),
            ("אחרי", [(v, f"c{cyc[a.index(v)] + 1}") for v in t], None)]
    return table(rows, "המטריצה 2 על 3 בזיכרון לפני השחלוף ואחריו, כל ערך צבוע לפי המעגל של המקום שלו", head=list(range(m * n)))


def memory_legend():
    return own_legend([("pm-key-c1", "‏0 לא זז"), ("pm-key-c2", "המעגל " + ltr("1 → 2 → 4 → 3 → 1")), ("pm-key-c3", "‏5 לא זז")])


def cycle_list():
    m, n = 3, 5
    lines = ["| המעגל | המקומות, לאן כל ערך עובר | האורך |", "|:-:|:-:|:-:|"]
    for c, cyc in enumerate(cycles(m, n)):
        lines.append(f"| {RLM}{c + 1} | {RLM}`{' → '.join(map(str, cyc))}{' → ' + str(cyc[0]) if len(cyc) > 1 else ''}` | {RLM}{len(cyc)} |")
    return "\n".join(lines)


SIZES = ((2, 3), (3, 5), (8, 12), (64, 48), (100, 37))


def placements(m, n):
    """The writes of the in-place transpose, cycle after cycle from the smallest index of
    each: (start of the cycle, value in hand, the place it is put at, the value picked up
    there). A place that does not move is one write of its own value, as the page's code
    does it; the first and the last entry are never written."""
    a = list(range(m * n))
    rows = []
    for cyc in cycles(m, n):
        if cyc[0] in (0, m * n - 1):
            continue
        hand = a[cyc[0]]
        for k in cyc[1:] + cyc[:1]:
            rows.append((cyc[0], hand, k, a[k]))
            a[k], hand = hand, a[k]
    assert a == transposed(list(range(m * n)), m, n) or m * n <= 2
    return rows


def trace_table():
    """The 2 x 3 example placed by hand: one row per write."""
    m, n = 2, 3
    name = [chr(97 + i) for i in range(m * n)]
    lines = ["| הצעד | ביד | מניחים באינדקס | מרימים משם |", "|:-:|:-:|:-:|:-:|"]
    rows = placements(m, n)
    for t, (s, hand, k, up) in enumerate(rows, 1):
        last = k == s
        lines.append(f"| {RLM}{t} | {RLM}`{name[hand]}` | {RLM}{k} | " + ("כלום, המעגל נסגר |" if last else f"{RLM}`{name[up]}` |"))
    return "\n".join(lines)


def cost_table():
    lines = ["| המטריצה | ‏mn | מעגלים שזזים | מקומות שלא זזים | הנחות | צעדים בחיפוש המנהיגים |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for m, n in SIZES:
        cs = cycles(m, n)
        moving = sum(1 for c in cs if len(c) > 1)
        lines.append(f"| {RLM}<span dir=\"ltr\">{m}×{n}</span> | {RLM}{m * n} | {RLM}{moving} | {RLM}{len(cs) - moving} | {RLM}{len(placements(m, n))} | {RLM}{leader_checks(m, n)} |")
    return "\n".join(lines)


# --- the hardware follow-up: a streaming transposer with two memories -----------------------

def read_order(m, n):
    """The read addresses that give the transpose row by row: column j of the stored frame
    from the top, the address i n + j; a counter that adds n and wraps to the next column."""
    out, addr = [], 0
    for j in range(n):
        addr = j
        for _ in range(m):
            out.append(addr)
            addr += n
    return out


HW_W, HW_H = 470, 200
HW_BLOCKS = [(10, 16, 130, 52, "wr_addr", "0, 1, 2, …"), (10, 132, 130, 52, "rd_addr", "i·n + j"),
             (200, 16, 110, 52, "RAM A", "mn"), (200, 132, 110, 52, "RAM B", "mn"), (368, 74, 54, 52, "mux", "")]


def hw_diagram():
    label = ("תרשים המלבנים של משחלף בזרם" + NB + ": מונה הכתיבה wr_addr סופר 0, 1, 2 וכותב את התמונה שנכנסת לזיכרון אחד, "
             "ומונה הקריאה rd_addr עובר על האינדקסים i·n + j, עמודה אחרי עמודה, וקורא את התמונה הקודמת מהזיכרון השני. "
             "‏mux בוחר את הזיכרון שנקרא ומוציא את dout. בכל תמונה שני הזיכרונות מתחלפים בתפקידים")
    o = [f'<svg class="figure tp-hw" viewBox="0 0 {HW_W} {HW_H}" direction="ltr" style="max-width:{HW_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="tp-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="tp-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for x, y, w, h, title, sub in HW_BLOCKS:
        ty = y + h / 2 + (-3 if sub else 5)
        o.append(f'<g class="tp-blk"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{escape(title)}</text>'
                 + (f'<text class="tp-sub" x="{x + w / 2:g}" y="{y + h / 2 + 15:g}" text-anchor="middle">{escape(sub)}</text>' if sub else "")
                 + "</g>")
    solid = [[(140, 34), (200, 34)], [(140, 166), (200, 166)],
             [(310, 42), (340, 42), (340, 88), (368, 88)], [(310, 158), (340, 158), (340, 112), (368, 112)],
             [(422, 100), (462, 100)]]
    swap = [[(140, 54), (200, 146)], [(140, 146), (200, 54)]]
    for pts in solid:
        o.append('<path class="tp-wire" d="M' + " L".join(f"{x},{y}" for x, y in pts) + '" marker-end="url(#tp-hb)"/>')
    for pts in swap:
        o.append('<path class="tp-wire tp-swap" d="M' + " L".join(f"{x},{y}" for x, y in pts) + '" marker-end="url(#tp-hb)"/>')
    o.append('<text class="tp-wlab" x="170" y="26" text-anchor="middle">din</text>')
    o.append('<text class="tp-wlab" x="442" y="90" text-anchor="middle">dout</text>')
    return "".join(o) + "</svg>"


def hw_legend():
    return own_legend([("tp-key-now", "התמונה הזו" + NB + ": כותבים ל-A וקוראים מ-B"),
                   ("tp-key-swap", "התמונה הבאה" + NB + ": התפקידים מתחלפים")])


def hw_rows(m, n):
    """The clocks of the second frame: the frame a, b, c, ... sits in RAM B and is read out
    transposed while the next frame is written to RAM A. (clock, wr_addr, din, rd_addr, dout)."""
    size = m * n
    first = [chr(97 + i) for i in range(size)]
    second = [chr(97 + size + i) for i in range(size)]
    return [(size + t, t, second[t], addr, first[addr]) for t, addr in enumerate(read_order(m, n))]


def hw_table():
    m, n = 2, 3
    assert [r[4] for r in hw_rows(m, n)] == transposed([chr(97 + i) for i in range(m * n)], m, n)
    lines = ["| המחזור | ‏wr_addr, ל-A | ‏din | ‏rd_addr, מ-B | ‏dout |", "|:-:|:-:|:-:|:-:|:-:|"]
    for clk, wa, din, ra, dout in hw_rows(m, n):
        lines.append(f"| {RLM}{clk} | {RLM}{wa} | {RLM}`{din}` | {RLM}{ra} | {RLM}`{dout}` |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [rotate_table(), memory_table(), memory_legend(), cycle_list(), trace_table(), cost_table(),
            hw_diagram() + "\n\n" + hw_legend(), hw_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
