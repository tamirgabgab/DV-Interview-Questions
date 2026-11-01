#!/usr/bin/env python3
"""Figures and tables of question 0072 (rotating an array by k places in place).

    python tools/figures/fill.py 72        # put the blocks on the page

The reference here is independent of the page code: the rotation is a[i] = old[(i + k) mod n]
taken straight from the definition, the three reversals and the cycles are traced from it,
and the memory accesses of part c are counted by formula. blocks() returns, in page order:
the three reversals on 1..7 with k = 3, the cycles of n = 12 and k = 8 with their legend
and their list, and the table of memory accesses of part c. tests/0072 checks the page's
numbers and code against this module.
"""

from __future__ import annotations

import sys
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import legend, table  # noqa: E402

RLM = "‏"
EX_N, EX_K = 7, 3            # part a's example
CY_N, CY_K = 12, 8           # part b's example


def rotated(a, k):
    """The definition: rotate left by k places."""
    n = len(a)
    return [a[(i + k) % n] for i in range(n)] if n else []


def reversal_rows(a, k):
    """The array after each of the three reversals, with the range each one reversed."""
    n, k = len(a), k % len(a)
    cur, rows = list(a), [(list(a), None)]
    for lo, hi in ((0, k), (k, n), (0, n)):
        cur[lo:hi] = cur[lo:hi][::-1]
        rows.append((list(cur), (lo, hi)))
    return rows


def swaps(n, k):
    """The swaps of the three reversals (a reversal of L entries swaps floor(L / 2) pairs)."""
    k %= n
    return 0 if k == 0 else k // 2 + (n - k) // 2 + n // 2


def cycles(n, k):
    """The cycles of the rotation from each start s: s <- s + k <- s + 2k ... (mod n)."""
    k %= n
    out, seen = [], set()
    for s in range(n):
        if s in seen:
            continue
        cyc, i = [], s
        while True:
            cyc.append(i)
            seen.add(i)
            i = (i + k) % n
            if i == s:
                break
        out.append(cyc)
    return out


def accesses_reversals(n, h):
    """Memory accesses of the three reversals on a single-port memory: a swap reads two
    entries and writes two."""
    return 4 * swaps(n, h)


def accesses_cycles(n, h):
    """Memory accesses of the cycles: every entry read once and written once."""
    return 0 if h % n == 0 else 2 * n


# --- the blocks ---------------------------------------------------------------------------

NAMES = ["לפני", "היפוך של A", "היפוך של B", "היפוך של הכול"]


def reversal_table():
    a = list(range(1, EX_N + 1))
    rows = []
    for (cur, rng), name in zip(reversal_rows(a, EX_K), NAMES):
        cells = [(v, "is-hl" if rng and rng[0] <= i < rng[1] else ("c1" if v <= EX_K else "c2")) for i, v in enumerate(cur)]
        rows.append((name, cells, None))
    return table(rows, "שלושת ההיפוכים על 1 עד 7 עם k = 3 : בכל שורה המערך אחרי ההיפוך, והקטע שהתהפך ממוסגר",
                 head=list(range(EX_N)))


def cycle_table():
    cs = cycles(CY_N, CY_K)
    which = {i: c for c, cyc in enumerate(cs) for i in cyc}
    rows = [("המעגל", [(which[i] + 1, f"c{which[i] + 1}") for i in range(CY_N)], None)]
    return table(rows, f"המעגלים של n = {CY_N} ו-k = {CY_K} : לכל אינדקס, מספר המעגל שלו", head=list(range(CY_N)))


def cycle_legend():
    return legend([(f"pm-key-c{c + 1}", f"מעגל {c + 1}") for c in range(gcd(CY_N, CY_K))])


def cycle_list():
    lines = ["| המעגל | ההעברות | האורך |", "|:-:|:-:|:-:|"]
    for c, cyc in enumerate(cycles(CY_N, CY_K)):
        moves = " ← ".join(f"a[{i}]" for i in cyc) + " ← tmp"
        lines.append(f"| {RLM}{c + 1} | {RLM}`{moves}` | {RLM}{len(cyc)} |")
    return "\n".join(lines)


def access_table():
    lines = ["| ‏n | ‏head | שלושה היפוכים | מעגלים |", "|:-:|:-:|:-:|:-:|"]
    for n, h in ((8, 3), (8, 4), (12, 5), (1024, 300)):
        lines.append(f"| {RLM}{n} | {RLM}{h} | {RLM}{accesses_reversals(n, h)} | {RLM}{accesses_cycles(n, h)} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [reversal_table(), cycle_table(), cycle_legend(), cycle_list(), access_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
