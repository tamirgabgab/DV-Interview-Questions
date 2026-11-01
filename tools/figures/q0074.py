#!/usr/bin/env python3
"""Figures and tables of question 0074 (rotating a square image and transposing a matrix in place).

    python tools/figures/fill.py 74        # put the blocks on the page

The reference here is independent of the page code: the transpose is built entry by entry
from its definition (row-major m x n in, row-major n x m out), and its cycles are found by
following where each entry goes. blocks() returns, in page order: a 3 x 3 image rotated in
two steps, the 2 x 3 example in memory with its legend, the cycles of 3 x 5, and the cost
of finding the leaders without marks. tests/0074 checks the page's numbers and code against
this module.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import legend, table  # noqa: E402

RLM = "‏"


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
    return table(rows, "תמונה 3 על 3 : המקורית, אחרי שחלוף (האלכסון לא זז), ואחרי היפוך של כל שורה, סיבוב של רבע סיבוב בכיוון השעון",
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
    return legend([("pm-key-c1", "‏0 לא זז"), ("pm-key-c2", "המעגל 1 → 2 → 4 → 3 → 1"), ("pm-key-c3", "‏5 לא זז")])


def cycle_list():
    m, n = 3, 5
    lines = ["| המעגל | המקומות, לאן כל ערך עובר | האורך |", "|:-:|:-:|:-:|"]
    for c, cyc in enumerate(cycles(m, n)):
        lines.append(f"| {RLM}{c + 1} | {RLM}`{' → '.join(map(str, cyc))}{' → ' + str(cyc[0]) if len(cyc) > 1 else ''}` | {RLM}{len(cyc)} |")
    return "\n".join(lines)


SIZES = ((2, 3), (3, 5), (8, 12), (64, 48), (100, 37))


def cost_table():
    lines = ["| המטריצה | ‏mn | מעגלים | השמות | צעדים בחיפוש המנהיגים |", "|:-:|:-:|:-:|:-:|:-:|"]
    for m, n in SIZES:
        cs = cycles(m, n)
        lines.append(f"| {RLM}<span dir=\"ltr\">{m}×{n}</span> | {RLM}{m * n} | {RLM}{len(cs)} | {RLM}{m * n} | {RLM}{leader_checks(m, n)} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [rotate_table(), memory_table(), memory_legend(), cycle_list(), cost_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
