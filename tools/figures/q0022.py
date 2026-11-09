#!/usr/bin/env python3
"""Figures and tables of question 0022, counting the paths in a grid from the top-left corner
to the bottom-right one: right and down (C(m+n-2, m-1)), with obstacles (a DP over the
cells), right, up and down without visiting a cell twice (m^(n-1)), and that with obstacles
(a DP over the columns).

    python tools/figures/fill.py 22        # put the blocks on the page

The references here are independent of the page code: counts() runs the DP of either kind
over the cells (the number of paths that end at every cell), walks() lists every path by a
depth-first search that never visits a cell twice (any set of moves, left included), and
the closed forms come from math.comb and powers. blocks() returns, in page order: the six
paths of a 3 x 3 board, the counts of the 3 x 7 board with their legend, the obstacles board
of part b with its counts, the nine paths of a 3 x 3 board with up allowed, the table of
the two counts (and of four directions) for a few sizes, the obstacles board of part d with
the counts of both kinds, and the zigzag board where only the paths with up arrive.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "
MOD = 10**9 + 7

M, N = 3, 7                                           # the board of parts a and c
# the obstacles of parts b and d (1 = obstacle), and the zigzag of part d: column 1 open only
# at the bottom, column 3 open only at the top, so a path has to go up
BOARD_B = ["0000010", "0100000", "0001000"]
ZIGZAG = ["0100000", "0101000", "0001000"]

RIGHT, DOWN, UP, LEFT = (0, 1), (1, 0), (-1, 0), (0, -1)
RD, RUD, ALL = (RIGHT, DOWN), (RIGHT, DOWN, UP), (RIGHT, DOWN, UP, LEFT)
ARROW = {RIGHT: "→", DOWN: "↓", UP: "↑", LEFT: "←"}


# --- the reference ---------------------------------------------------------------------------------

def parse(rows: list[str]) -> list[list[int]]:
    return [[int(ch) for ch in row] for row in rows]


def empty(m: int, n: int) -> list[list[int]]:
    return [[0] * n for _ in range(m)]


def paths_rd(m: int, n: int) -> int:
    return math.comb(m + n - 2, m - 1)


def paths_rud(m: int, n: int) -> int:
    return m ** (n - 1)


def counts(grid: list[list[int]], up: bool = False) -> list[list[int]]:
    """The number of paths from (0, 0) that end at every cell: right and down (a cell is the
    cell on its left plus the cell above it), or with up (a column at a time: the paths that
    end at a cell entered the column somewhere in its run of free cells)."""
    m, n = len(grid), len(grid[0])
    out = empty(m, n)
    for c in range(n):
        enter = [0] * m
        for r in range(m):
            if grid[r][c]:
                continue
            if c == 0:
                enter[r] = 1 if r == 0 else 0
            else:
                enter[r] = out[r][c - 1]
        if not up:
            for r in range(m):
                if not grid[r][c]:
                    out[r][c] = enter[r] + (out[r - 1][c] if r else 0)
            continue
        r = 0
        while r < m:
            if grid[r][c]:
                r += 1
                continue
            s = r
            while r < m and not grid[r][c]:
                r += 1
            total = sum(enter[s:r])
            for k in range(s, r):
                out[k][c] = total
    return out


def count(grid: list[list[int]], up: bool = False) -> int:
    return counts(grid, up)[-1][-1]


def walks(grid: list[list[int]], moves=RD, limit: int | None = None) -> list[list[tuple[int, int]]]:
    """Every path from (0, 0) to the bottom-right cell that uses only these moves and never
    visits a cell twice, in the order of the depth-first search."""
    m, n = len(grid), len(grid[0])
    if grid[0][0] or grid[m - 1][n - 1]:
        return []
    out, path, seen = [], [(0, 0)], {(0, 0)}

    def go(r, c):
        if limit is not None and len(out) >= limit:
            return
        if (r, c) == (m - 1, n - 1):
            out.append(path.copy())
            return
        for dr, dc in moves:
            a, b = r + dr, c + dc
            if 0 <= a < m and 0 <= b < n and not grid[a][b] and (a, b) not in seen:
                seen.add((a, b))
                path.append((a, b))
                go(a, b)
                path.pop()
                seen.remove((a, b))

    go(0, 0)
    return out


def count_walks(grid, moves=RD) -> int:
    return len(walks(grid, moves))


def arrows(path) -> str:
    return "".join(ARROW[(b[0] - a[0], b[1] - a[1])] for a, b in zip(path, path[1:]))


def exit_rows(path, n: int) -> list[int]:
    """The row where the path leaves each of the columns 0 .. n-2 (part c's bijection)."""
    last = {c: r for r, c in path}
    return [last[c] for c in range(n - 1)]


# --- drawing ---------------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def heat(v: int, top: int) -> int:
    """The tint level 0..4 of a count, on a log scale against the largest count on the board."""
    if v <= 0 or top <= 0:
        return 0
    return 1 + min(3, int(3.999 * math.log(v) / math.log(top))) if top > 1 else 1


def board_svg(grid, label, values=None, path=None, cs=34) -> str:
    """A board: obstacles dark, S and T in their corners, the count of every open cell (on a
    tint that grows with it), and a path from centre to centre."""
    m, n = len(grid), len(grid[0])
    lw, top = 24, 22
    W, H = lw + n * cs + 6, top + m * cs + 6
    s = f'<svg class="figure gx-fig lp-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">'
    for c in range(n):
        s += f'<text class="tick" x="{lw + c * cs + cs / 2:g}" y="14" text-anchor="middle">{c}</text>'
    for r in range(m):
        s += f'<text class="tick" x="{lw - 7}" y="{top + r * cs + cs / 2 + 4:g}" text-anchor="end">{r}</text>'
    big = max((v for row in values for v in row), default=0) if values else 0
    texts = ""
    for r in range(m):
        for c in range(n):
            x, y = lw + c * cs, top + r * cs
            tag = "S" if (r, c) == (0, 0) else "T" if (r, c) == (m - 1, n - 1) else ""
            if grid[r][c]:
                cls, tip = "is-wall", f"cell ({r}, {c}): an obstacle"
            else:
                v = values[r][c] if values else None
                cls = "is-open" + (f" lp-h{heat(v, big)}" if v is not None else "")
                tip = f"cell ({r}, {c})" + (f": {v} path{'' if v == 1 else 's'} end{'s' if v == 1 else ''} here" if v is not None else "")
                if v is not None:
                    texts += (f'<text class="gx-val" x="{x + cs / 2:g}" y="{y + cs / 2 + (8 if tag else 5):g}" '
                              f'text-anchor="middle">{v}</text>')
            s += (f'<g class="gx-cell {cls}"><title>{tip}</title>'
                  f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{cs - 3}" height="{cs - 3}" rx="3"/></g>')
            if tag:
                texts += f'<text class="gx-tag" x="{x + 4}" y="{y + 12}">{tag}</text>'
    if path:
        pts = " ".join(f"{lw + c * cs + cs / 2:g},{top + r * cs + cs / 2:g}" for r, c in path)
        s += f'<polyline class="gx-path" points="{pts}"><title>a path: {arrows(path)}</title></polyline>'
    return s + texts + "</svg>"


def multiples_svg(paths, m, n, label, per_row) -> str:
    """Small boards side by side, one path on each."""
    cs, gap = 13, 12
    bw, bh = n * cs, m * cs
    rows = math.ceil(len(paths) / per_row)
    W = per_row * bw + (per_row - 1) * gap + 4 + 30      # an empty strip on the right for the enlarge button
    H = rows * bh + (rows - 1) * gap + 4
    s = f'<svg class="figure gx-fig lp-fig lp-small" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">'
    for i, p in enumerate(paths):
        ox, oy = 2 + (i % per_row) * (bw + gap), 2 + (i // per_row) * (bh + gap)   # left-aligned
        s += f'<g class="lp-one"><title>path {i + 1}: {arrows(p)}</title>'
        for r in range(m):
            for c in range(n):
                end = " lp-end" if (r, c) in ((0, 0), (m - 1, n - 1)) else ""
                s += f'<rect class="lp-sq{end}" x="{ox + c * cs + 0.75:g}" y="{oy + r * cs + 0.75:g}" width="{cs - 1.5:g}" height="{cs - 1.5:g}" rx="1.5"/>'
        pts = " ".join(f"{ox + c * cs + cs / 2:g},{oy + r * cs + cs / 2:g}" for r, c in p)
        s += f'<polyline class="lp-line" points="{pts}"/></g>'
    return s + "</svg>"


def legend(path=False) -> str:
    keys = ('<span><i class="gx-key-s"></i>S ההתחלה, T היעד</span>'
            '<span><i class="lp-key-lo"></i>מעט מסלולים</span><span><i class="lp-key-hi"></i>הרבה מסלולים</span>'
            '<span><i class="gx-key is-wall"></i>מכשול</span>')
    if path:
        keys += '<span><i class="gx-key-path"></i>מסלול אחד</span>'
    return f'<span class="viz-legend">{keys}</span>'


def table_sizes() -> str:
    rows = ["| הלוח | ימינה ולמטה | ימינה, למעלה ולמטה | גם שמאלה |", "|---|:-:|:-:|:-:|"]
    for m, n in ((2, 2), (3, 3), (3, 7), (4, 4), (5, 5)):
        g = empty(m, n)
        a, b = paths_rd(m, n), paths_rud(m, n)
        assert a == count(g) == count_walks(g, RD) and b == count(g, True) == count_walks(g, RUD)
        rows.append(f"| {RLM}{ltr(f'{m} × {n}')} | {a:,} | {b:,} | {count_walks(g, ALL):,} |")
    return "\n".join(rows)


def table_zigzag() -> str:
    """Column by column: what enters each row and the count of every cell, as vectors from
    row 0 down (# an obstacle)."""
    g = parse(ZIGZAG)
    up = counts(g, True)
    m = len(g)

    def vec(vals):
        return RLM + ltr("[" + ", ".join(vals) + "]")

    rows = ["| עמודה | נכנסים בכל שורה | המסלולים שנגמרים בכל תא | למה |", "|:-:|:-:|:-:|---|"]
    why = {0: "ההתחלה בשורה 0, וכל העמודה קטע אחד", 1: "רק שורה 2 פנויה", 2: "קטע אחד : כל תא מקבל 1, גם שורה 0",
           3: "רק שורה 0 פנויה", 4: "קטע אחד : " + ltr("1 + 0 + 0"), 5: "קטע אחד : " + ltr("1 + 1 + 1"), 6: "קטע אחד : " + ltr("3 + 3 + 3")}
    for c in range(len(g[0])):
        enter = ["#" if g[r][c] else str(1 if c == 0 and r == 0 else 0 if c == 0 else up[r][c - 1]) for r in range(m)]
        out = ["#" if g[r][c] else str(up[r][c]) for r in range(m)]
        rows.append(f"| {c} | {vec(enter)} | {vec(out)} | {why[c]} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    g7 = empty(M, N)
    b = parse(BOARD_B)
    z = parse(ZIGZAG)
    rd3 = walks(empty(3, 3), RD)
    rud3 = walks(empty(3, 3), RUD)
    zpath = walks(z, RUD)[0]
    out = [
        multiples_svg(rd3, 3, 3, "ששת המסלולים של לוח 3 על 3 בצעדים ימינה ולמטה : בכל אחד שני צעדים ימינה ושני צעדים למטה, בסדר אחר", 6),
        board_svg(g7, "לוח 3 על 7 : בכל תא מספר המסלולים מ-S שנגמרים בו, ימינה ולמטה. השורה העליונה והעמודה השמאלית הן 1, כל תא אחר הוא סכום של התא משמאלו והתא מעליו, ובתא T יש 28",
                  values=counts(g7)),
        legend(),
        board_svg(b, "הלוח של סעיף ב : 3 על 7 עם שלושה מכשולים. בכל תא פנוי מספר המסלולים מ-S שנגמרים בו, ימינה ולמטה, ובתא T יש 9",
                  values=counts(b)),
        multiples_svg(rud3, 3, 3, "תשעת המסלולים של לוח 3 על 3 כשמותר גם למעלה, בלי לחזור לתא : בכל עמודה המסלול הוא קטע אנכי אחד, ובשתי העמודות הראשונות בוחרים את שורת היציאה", 5),
        table_sizes(),
        board_svg(b, "אותו לוח של סעיף ב כשמותר גם למעלה : בכל תא פנוי מספר המסלולים מ-S שנגמרים בו, ובתא T יש 32",
                  values=counts(b, True)),
        board_svg(z, "לוח הזיגזג : עמודה 1 פתוחה רק למטה ועמודה 3 רק למעלה. בצעדים ימינה ולמטה אין אף מסלול, וכשמותר גם למעלה יש 9. בכל תא מספר המסלולים שנגמרים בו, ומסלול אחד מסומן",
                  values=counts(z, True), path=zpath),
        legend(path=True),
        table_zigzag(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    print("a", paths_rd(M, N), count(empty(M, N)), [arrows(p) for p in walks(empty(3, 3))])
    print("b", count(parse(BOARD_B)), count(parse(BOARD_B), True))
    print("c", paths_rud(M, N), count(empty(M, N), True), len(walks(empty(3, 3), RUD)))
    print("z", count(parse(ZIGZAG)), count(parse(ZIGZAG), True), count_walks(parse(ZIGZAG), ALL))
    print("4dir", [count_walks(empty(k, k), ALL) for k in range(1, 6)], count_walks(empty(3, 7), ALL))
