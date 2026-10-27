#!/usr/bin/env python3
"""Figure of question 0046 (the largest square, rectangle and right triangle of ones): the
example grid of part a beside its dp table, with the first largest square marked in both,
and its legend.

    python tools/figures/fill.py 46        # put the blocks on the page

The dp table is computed here from its definition (the side of the largest square of ones
whose bottom-right corner is the cell), by checking every square, independently of the
page code.
"""

GRID = ["10111", "11111", "01111", "11110"]
CELL, GAP, PAD, HEAD, SPACE = 32, 3, 6, 24, 34


def grid(rows=GRID):
    return [[int(c) for c in r] for r in rows]


def side(g, i, j):
    """The largest k such that the k-by-k square ending at (i, j) is all ones."""
    k = 0
    while k <= min(i, j) and all(g[a][b] for a in range(i - k, i + 1) for b in range(j - k, j + 1)):
        k += 1
    return k


def dp(g):
    return [[side(g, i, j) for j in range(len(g[0]))] for i in range(len(g))]


def best(g):
    """The first cell, row by row, with the largest side, and that side."""
    d = dp(g)
    k = max(max(r) for r in d)
    i, j = next((i, j) for i in range(len(g)) for j in range(len(g[0])) if d[i][j] == k)
    return k, (i - k + 1, j - k + 1), (i, j)


def grids_svg(rows=GRID):
    g = grid(rows)
    d = dp(g)
    k, (r1, c1), (r2, c2) = best(g)
    m, n = len(g), len(g[0])
    one = n * CELL + (n - 1) * GAP
    width = 2 * PAD + 2 * one + SPACE
    height = HEAD + m * CELL + (m - 1) * GAP + PAD
    p = [f'<svg class="figure" viewBox="0 0 {width} {height}" style="max-width:{width / 16:.1f}rem" role="img" '
         f'aria-label="המערך וטבלת dp : הריבוע הגדול ביותר בצלע {k}, מ-({r1}, {c1}) עד ({r2}, {c2})">']
    for t, (title, values) in enumerate((("grid", g), ("dp", d))):
        x0 = PAD + t * (one + SPACE)
        p.append(f'<text class="st-text st-sm" x="{x0 + one / 2:g}" y="{HEAD - 8}" text-anchor="middle">{title}</text>')
        for i in range(m):
            for j in range(n):
                x, y = x0 + j * (CELL + GAP), HEAD + i * (CELL + GAP)
                inside = r1 <= i <= r2 and c1 <= j <= c2
                cls = "st-ok" if inside else "fig-one" if g[i][j] else "st-cell"
                p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>'
                         f'<text class="st-text st-sm" x="{x + CELL / 2:g}" y="{y + CELL / 2 + 4:g}" text-anchor="middle">{values[i][j]}</text>')
    return "".join(p) + "</svg>"


def legend():
    k, (r1, c1), (r2, c2) = best(grid())
    return ('<span class="viz-legend"><span><i class="fig-key-one"></i>תא של 1</span>'
            f'<span><i class="fig-key-square"></i>הריבוע הגדול ביותר, צלע {k}</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [grids_svg(), legend()]


if __name__ == "__main__":
    print(dp(grid()), best(grid()))
    print("\n\n".join(blocks()))
