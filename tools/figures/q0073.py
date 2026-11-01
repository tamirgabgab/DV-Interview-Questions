#!/usr/bin/env python3
"""Figures and tables of question 0073 (perfect shuffles of a deck, and the interleave in place).

    python tools/figures/fill.py 73        # put the blocks on the page

The reference here is independent of the page code: a shuffle is done by splitting the deck
and dealing the halves alternately, and the number of shuffles that bring the deck back is
found by shuffling until it does. blocks() returns, in page order: eight cards through
three out-shuffles with their legend, the table of shuffles per deck size, and the
interleave of [a0..a3 b0..b3] by rotations. tests/0073 checks the page's numbers and code
against this module.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import legend, table  # noqa: E402

RLM = "‏"


def shuffle(deck, kind="out"):
    """One perfect shuffle, top of the deck first. out: the top card stays on top (an odd
    deck's top half is the larger one); in: the top card goes second."""
    n = len(deck)
    h = (n + 1) // 2 if kind == "out" else n // 2
    top, bottom = deck[:h], deck[h:]
    first, second = (top, bottom) if kind == "out" else (bottom, top)
    out = []
    for i in range(len(first)):
        out.append(first[i])
        if i < len(second):
            out.append(second[i])
    return out


def order_by_shuffling(n, kind="out"):
    deck = list(range(n))
    cur, t = shuffle(deck, kind), 1
    while cur != deck:
        cur, t = shuffle(cur, kind), t + 1
    return t


def modulus(n, kind="out"):
    """The modulus M of the map p -> 2p mod M that the shuffle is."""
    return n if n % 2 else (n - 1 if kind == "out" else n + 1)


def mult_order(m):
    """The order of 2 modulo an odd m."""
    if m == 1:
        return 1
    e, p = 1, 2 % m
    while p != 1:
        p, e = 2 * p % m, e + 1
    return e


def cycles(n, kind="out"):
    """The cycles of the positions under one shuffle."""
    deck = list(range(n))
    after = shuffle(deck, kind)
    where = {card: pos for pos, card in enumerate(after)}
    seen, out = set(), []
    for s in range(n):
        if s in seen:
            continue
        cyc, p = [], s
        while p not in seen:
            seen.add(p)
            cyc.append(p)
            p = where[p]
        out.append(cyc)
    return out


def interleave_rows(m):
    """[a0..a(m-1) b0..b(m-1)] through the levels of the interleave by rotations: the deck
    after each level, and the ranges rotated in it."""
    a = [f"a{i}" for i in range(m)] + [f"b{i}" for i in range(m)]
    rows, level = [(list(a), [])], [(0, m)]
    while any(mm > 1 for _, mm in level):
        nxt, ranges = [], []
        for lo, mm in level:
            if mm <= 1:
                continue
            h = mm // 2
            seg = a[lo + h:lo + mm + h]
            a[lo + h:lo + mm + h] = seg[mm - h:] + seg[:mm - h]
            ranges.append((lo + h, lo + mm + h))
            nxt += [(lo, h), (lo + 2 * h, mm - h)]
        rows.append((list(a), ranges))
        level = nxt
    return rows


# --- the blocks ---------------------------------------------------------------------------

def deck_table():
    n = 8
    cyc = {p: c for c, cs in enumerate(cycles(n)) for p in cs}
    deck, rows = list(range(n)), []
    for t in range(order_by_shuffling(n) + 1):
        rows.append(("לפני" if t == 0 else f"אחרי {t}", [(card, f"c{cyc[card] + 1}") for card in deck], None))
        deck = shuffle(deck)
    return table(rows, "שמונה קלפים בשלושה out-shuffles : בכל שורה הסדר מלמעלה, ואחרי שלושה ערבובים הסדר חוזר",
                 head=list(range(n)))


def deck_legend():
    names = ["0 נשאר למעלה", "‏1, 2, 4", "‏3, 6, 5", "‏7 נשאר למטה"]
    return legend([(f"pm-key-c{c + 1}", t) for c, t in enumerate(names)])


SIZES = (8, 10, 16, 52, 64, 100, 7, 51)


def sizes_table():
    lines = ["| ‏n | ‏out | ‏in |", "|:-:|:-:|:-:|"]
    for n in SIZES:
        if n % 2:
            lines.append(f"| {RLM}{n} (אי-זוגי) | {RLM}{mult_order(n)} (מודולו {n}) | — |")
        else:
            o, i = mult_order(n - 1), mult_order(n + 1)
            lines.append(f"| {RLM}{n} | {RLM}{o} (מודולו {n - 1}) | {RLM}{i} (מודולו {n + 1}) |")
    return "\n".join(lines)


def interleave_table():
    m = 4
    names = ["לפני", "רמה 1", "רמה 2"]
    rows = []
    for (cur, ranges), name in zip(interleave_rows(m), names):
        cells = []
        for i, v in enumerate(cur):
            cls = "c1" if v[0] == "a" else "c2"
            if any(lo <= i < hi for lo, hi in ranges):
                cls += " is-hl"
            cells.append((v, cls))
        rows.append((name, cells, None))
    return table(rows, "השילוב במקום של a0 עד a3 ו-b0 עד b3 : בכל רמה מסובבים את הקטעים הממוסגרים", head=list(range(2 * m)))


def blocks():
    """The generated blocks, in page order."""
    return [deck_table(), deck_legend(), sizes_table(), interleave_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
