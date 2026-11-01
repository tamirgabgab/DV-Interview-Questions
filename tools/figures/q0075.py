#!/usr/bin/env python3
"""Figures and tables of question 0075 (the transpose of an 8 x 8 bit matrix in a 64-bit word).

    python tools/figures/fill.py 75        # put the blocks on the page

The reference here is independent of the page code: element (r, c) is bit 8r + c (row r is
byte r), the transpose is built bit by bit, and each stage of the block transpose swaps the
index bits r_i and c_i. blocks() returns, in page order: the 8 x 8 grid of element names
before and after each stage (in two tables), the table of the three stages, the table of
the stages for N x N in one word, and the masks of 32 x 32 in 32 words. tests/0075 checks
the page's numbers and code against this module.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import table  # noqa: E402

RLM = "‏"


def transpose_bits(x, n=8):
    """The definition on an n x n matrix in an n*n-bit word: bit n r + c goes to bit n c + r."""
    y = 0
    for r in range(n):
        for c in range(n):
            if x >> (n * r + c) & 1:
                y |= 1 << (n * c + r)
    return y


def stage(n, i):
    """Stage i of the n x n block transpose in one word: (shift, mask). It swaps element
    (r, c) with r_i = 0, c_i = 1 and element (r + 2^i, c - 2^i): the mask has the bits n r + c
    with r_i = 0 and c_i = 1, and the shift is (n - 1) 2^i."""
    b = 1 << i
    mask = 0
    for r in range(n):
        for c in range(n):
            if not r & b and c & b:
                mask |= 1 << (n * r + c)
    return (n - 1) * b, mask


def delta_swap(x, mask, s):
    t = ((x >> s) ^ x) & mask
    return x ^ t ^ (t << s)


def word_masks(n=32):
    """The masks of the n x n transpose over n words, stage by stage (j = n/2 .. 1): the bits
    c with c_j = 0."""
    out = []
    j = n // 2
    while j:
        out.append((j, sum(1 << c for c in range(n) if not c & j)))
        j //= 2
    return out


# --- the blocks ---------------------------------------------------------------------------

def names_after(stages):
    """Which element (r, c) each place holds after the given stages, as "rc"."""
    place = {(r, c): (r, c) for r in range(8) for c in range(8)}      # place -> element
    for i in stages:
        b = 1 << i
        new = dict(place)
        for (r, c), e in place.items():
            if not r & b and c & b:
                new[(r, c)], new[(r + b, c - b)] = place[(r + b, c - b)], e
        place = new
    return place


def grid_pair(left, right, title):
    a, b = names_after(left), names_after(right)
    moved = {p for p in b if b[p] != a[p]}
    rows = []
    for r in range(8):
        cells = [(f"{a[(r, c)][0]}{a[(r, c)][1]}", "c3" if a[(r, c)][0] == a[(r, c)][1] else "") for c in range(8)]
        cells.append(("", "is-gap"))
        cells += [(f"{b[(r, c)][0]}{b[(r, c)][1]}", "c3" if b[(r, c)][0] == b[(r, c)][1] else ("c1 is-hl" if (r, c) in moved else "")) for c in range(8)]
        rows.append((f"בית {r}", cells, None))
    head = list(range(8)) + [""] + list(range(8))
    return table(rows, title, head=head)


def grids_a():
    return grid_pair([], [0], "המטריצה לפני, ואחרי השלב הראשון (הזזה 7) : בכל תא שם האיבר שבו, שורה ואז עמודה, והאיברים שזזו ממוסגרים")


def grids_b():
    return grid_pair([0, 1], [0, 1, 2], "אחרי השלב השני (הזזה 14), ואחרי השלישי (הזזה 28) : זה השחלוף")


def stages_table():
    lines = ["| השלב | מה מחליפים | ההזזה | המסכה | זוגות |", "|:-:|:-:|:-:|:-:|:-:|"]
    what = ["בתוך כל בלוק 2×2", "בלוקים 2×2 בתוך כל 4×4", "בלוקים 4×4"]
    for i in range(3):
        s, m = stage(8, i)
        lines.append(f"| {RLM}{i + 1} | {what[i]} | {RLM}{s} | {RLM}`0x{m:016X}` | {RLM}{bin(m).count('1')} |")
    return "\n".join(lines)


def general_table():
    lines = ["| ‏N | ביטים | השלבים, הזזה ומסכה |", "|:-:|:-:|:-:|"]
    for n in (2, 4, 8):
        parts = [f"{s}: 0x{m:0{n * n // 4}X}" for s, m in (stage(n, i) for i in range(n.bit_length() - 1))]
        lines.append(f"| {RLM}{n} | {RLM}{n * n} | {RLM}`{' · '.join(parts)}` |")
    return "\n".join(lines)


def words_table():
    lines = ["| ‏j | המסכה | זוגות של מילים |", "|:-:|:-:|:-:|"]
    for j, m in word_masks(32):
        lines.append(f"| {RLM}{j} | {RLM}`0x{m:08X}` | {RLM}16 |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [grids_a(), grids_b(), stages_table(), general_table(), words_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
