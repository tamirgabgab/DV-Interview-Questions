#!/usr/bin/env python3
"""Figures and tables of question 0081 (N queens: counting with bit masks, the symmetries of
the square, and an explicit construction for every N >= 4).

    python tools/figures/fill.py 81        # put the blocks on the page

Column c of a board is bit c of the masks, drawn with column 0 on the right, so a row of
the board lines up with the binary digits of its masks (the low bit on the right).

blocks() returns them in page order: for part a the board of 8 queens three rows into the
search with the next row's free cells, the table of its three masks and their free bits,
and its legend; the table of the counts and of the placements the search tries for N = 4
to 12; for part b the 12 distinct solutions of 8 queens as small boards and its legend,
and the table of the solutions each symmetry keeps (Burnside); for part c the board of the
construction for N = 10 and its legend, and the table of the construction for N = 4 to 12.
tests/0081 checks that the page copies match and recomputes every value.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- the reference -------------------------------------------------------------------------


def solutions(n: int) -> list[tuple[int, ...]]:
    """Every solution, in the order of the search (the lowest free bit first); p[r] is the
    column (bit) of the queen in row r."""
    full, out = (1 << n) - 1, []

    def place(row: int, cols: int, left: int, right: int, qs: list[int]) -> None:
        if row == n:
            out.append(tuple(qs))
            return
        free = full & ~(cols | left | right)
        while free:
            bit = free & -free
            free ^= bit
            place(row + 1, cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1, qs + [bit.bit_length() - 1])

    place(0, 0, 0, 0, [])
    return out


def placements(n: int) -> int:
    """How many queens the search places on the way (every call of place but the first)."""
    full, count = (1 << n) - 1, [0]

    def place(cols: int, left: int, right: int) -> None:
        count[0] += 1
        if cols == full:
            return
        free = full & ~(cols | left | right)
        while free:
            bit = free & -free
            free ^= bit
            place(cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1)

    place(0, 0, 0)
    return count[0] - 1


def masks(n: int, qs: list[int]) -> tuple[int, int, int, int]:
    """(cols, left, right, free) for the row after the queens qs (one per row, from row 0)."""
    full, cols, left, right = (1 << n) - 1, 0, 0, 0
    for c in qs:
        bit = 1 << c
        cols, left, right = cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1
    return cols, left, right, full & ~(cols | left | right)


def rotate(p: tuple[int, ...]) -> tuple[int, ...]:
    """The board turned a quarter: the queen (r, c) goes to (c, n - 1 - r)."""
    n, q = len(p), [0] * len(p)
    for r, c in enumerate(p):
        q[c] = n - 1 - r
    return tuple(q)


def mirror(p: tuple[int, ...]) -> tuple[int, ...]:
    """The board mirrored left to right: the queen (r, c) goes to (r, n - 1 - c)."""
    return tuple(len(p) - 1 - c for c in p)


def images(p: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The 8 images of p: the identity, the three quarter turns, and the four mirrors."""
    out, q = [], p
    for _ in range(4):
        out.append(q)
        q = rotate(q)
    return out + [mirror(q) for q in out]


SYM_NAMES = ["בלי שינוי", "רבע סיבוב", "חצי סיבוב", "שלושה רבעי סיבוב",
             "שיקוף ימין-שמאל", "שיקוף באלכסון", "שיקוף למעלה-למטה", "שיקוף באלכסון השני"]


def classes(n: int) -> list[list[tuple[int, ...]]]:
    """The solutions grouped by symmetry, each class sorted, the classes by their smallest."""
    seen, out = set(), []
    for p in solutions(n):
        if p not in seen:
            cls = sorted(set(images(p)))
            seen.update(cls)
            out.append(cls)
    return sorted(out)


def burnside(n: int) -> list[int]:
    """How many solutions each of the 8 symmetries (in images' order) leaves unchanged."""
    fixed = [0] * 8
    for p in solutions(n):
        for i, q in enumerate(images(p)):
            fixed[i] += q == p
    return fixed


def construct(n: int) -> list[int]:
    """The explicit solution for n >= 4: the column (from 1) of the queen in rows 1 .. n."""
    evens, odds = list(range(2, n + 1, 2)), list(range(1, n + 1, 2))
    if n % 6 == 2:
        odds = [3, 1] + [c for c in odds if c not in (1, 3, 5)] + [5]
    elif n % 6 == 3:
        evens = [c for c in evens if c != 2] + [2]
        odds = [c for c in odds if c not in (1, 3)] + [1, 3]
    return evens + odds


# --- drawing -------------------------------------------------------------------------------

def queen(x: float, y: float, s: float, cls: str = "") -> str:
    """A queen centred at (x, y) in a cell of side s: a crown on a base."""
    k = s / 100
    pts = [(-30, 18), (-36, -22), (-15, 0), (0, -32), (15, 0), (36, -22), (30, 18)]
    poly = " ".join(f"{x + a * k:.1f},{y + b * k:.1f}" for a, b in pts)
    return (f'<g class="nq-q{(" " + cls) if cls else ""}"><polygon points="{poly}"/>'
            f'<rect x="{x - 30 * k:.1f}" y="{y + 20 * k:.1f}" width="{60 * k:.1f}" height="{11 * k:.1f}" rx="{3 * k:.1f}"/></g>')


def board(n: int, qs: dict[int, int], *, s: int = 44, label: str, cell_cls=None, numbers: bool = True,
          extra: str = "", style: str = "max-width:22rem", base: str = "1") -> str:
    """An n x n board, column 0 on the right; qs maps a row to its queen's column; cell_cls(r, c)
    gives extra classes of a cell. numbers: the column numbers above and the row numbers on
    the right (from base, 0 or 1)."""
    pad = 24 if numbers else 2
    w, h = n * s + pad + 2, n * s + pad + 2
    out = [f'<svg class="figure nq-board{(" " + extra) if extra else ""}" viewBox="0 0 {w} {h}" style="{style}" role="img" '
           f'aria-label="{label}">']
    x0, y0 = 1, pad
    b0 = int(base)
    for r in range(n):
        for c in range(n):
            x, y = x0 + (n - 1 - c) * s, y0 + r * s
            cls = "nq-sq" + (" is-dark" if (r + c) % 2 else "")
            more = cell_cls(r, c) if cell_cls else ""
            out.append(f'<rect class="{cls}{(" " + more) if more else ""}" x="{x}" y="{y}" width="{s}" height="{s}"/>')
    out.append(f'<rect class="nq-frame" x="{x0}" y="{y0}" width="{n * s}" height="{n * s}"/>')
    if numbers:
        for c in range(n):
            out.append(f'<text class="nq-lab" x="{x0 + (n - 1 - c) * s + s / 2:.1f}" y="{y0 - 7}" text-anchor="middle">{c + b0}</text>')
        for r in range(n):
            out.append(f'<text class="nq-lab" x="{x0 + n * s + 5}" y="{y0 + r * s + s / 2 + 5:.1f}">{r + b0}</text>')
    for r, c in qs.items():
        out.append(queen(x0 + (n - 1 - c) * s + s / 2, y0 + r * s + s / 2, s))
    return "".join(out) + "</svg>"


# --- part a --------------------------------------------------------------------------------

EX_N = 8
EX_QS = [0, 4, 7]          # the search's first three queens (the first solution starts so)


def search_board() -> str:
    n, qs = EX_N, EX_QS
    cols, left, right, free = masks(n, qs)
    row = len(qs)

    def cell(r, c):
        if r != row:
            return ""
        return "is-free" if free >> c & 1 else "is-hit"
    return board(n, dict(enumerate(qs)), label=(
        "סעיף א : לוח של 8 על 8, העמודה 0 מימין. מלכות בשורה 0 בעמודה 0, בשורה 1 בעמודה 4 ובשורה 2 בעמודה 7. "
        "בשורה 3 מאוימות העמודות 0, 2, 3, 4, 6 ו-7, ופנויות רק העמודות 1 ו-5"), cell_cls=cell, base="0")


def search_masks() -> str:
    n = EX_N
    cols, left, right, free = masks(n, EX_QS)
    rows = [("cols", cols, ""), ("left", left, ""), ("right", right, ""), ("free", free, "is-free")]
    head = "".join(f"<th>{c}</th>" for c in range(n - 1, -1, -1))
    t = [f'<div class="gs-scroll" tabindex="0" role="region" aria-label="המסכות של שורה 3 בבינארי">'
         f'<table class="gs-bits nq-masks" dir="ltr" aria-label="המסכות של שורה 3, ביט 7 משמאל וביט 0 מימין">'
         f'<tbody><tr class="nq-bitno"><th>bit</th>{head}<td></td></tr>']
    for name, v, cls in rows:
        cells = "".join(f'<td class="gs-b{(" is-one" if v >> c & 1 else "")}{(" " + cls) if cls and v >> c & 1 else ""}">{v >> c & 1}</td>'
                        for c in range(n - 1, -1, -1))
        t.append(f'<tr><th>{name}</th>{cells}<td class="gs-val">= {v}</td></tr>')
    return "".join(t) + "</tbody></table></div>"


def search_legend() -> str:
    return ('<span class="viz-legend"><span><i class="nq-key-hit"></i>מאוימת בשורה הבאה</span>'
            '<span><i class="nq-key-free"></i>פנויה : ביט 1 ב-free</span>'
            '<span><i class="gs-key-one"></i>ביט 1 במסכה</span></span>')


def counts_table() -> str:
    lines = ["| ‏\\( N \\) | פתרונות | מלכות שהחיפוש מציב | ‏\\( N! \\) | ‏\\( N^N \\) |", "|:-:|:-:|:-:|:-:|:-:|"]
    for n in range(4, 13):
        lines.append(f"| {n} | {len(solutions(n)):,} | {placements(n):,} | {math.factorial(n):,} | {n ** n:,} |")
    return "\n".join(lines)


# --- part b --------------------------------------------------------------------------------

def class_boards() -> str:
    """The 12 classes of 8 queens, each by its smallest image, with the size of its class."""
    cl = classes(EX_N)
    n, s, gap, cols = EX_N, 14, 18, 6
    bw = n * s
    w = cols * bw + (cols - 1) * gap + 4
    rows = math.ceil(len(cl) / cols)
    bh = bw + 22
    h = rows * bh + (rows - 1) * 12 + 4
    out = [f'<svg class="figure nq-classes" viewBox="0 0 {w} {h}" style="max-width:40rem" role="img" '
           f'aria-label="סעיף ב : 12 הפתרונות השונים של 8 מלכות, כל אחד בתמונה הקטנה ביותר שלו. '
           f'לאחד עשר מהם יש 8 תמונות שונות, ולאחד, המסומן, רק 4 : הוא לא משתנה בחצי סיבוב">']
    for i, cls in enumerate(cl):
        p = cls[0]
        x0 = 2 + (i % cols) * (bw + gap)
        y0 = 2 + (i // cols) * (bh + 12)
        sym = len(cls) == 4
        for r in range(n):
            for c in range(n):
                dark = " is-dark" if (r + c) % 2 else ""
                out.append(f'<rect class="nq-sq{dark}" x="{x0 + (n - 1 - c) * s}" y="{y0 + r * s}" width="{s}" height="{s}"/>')
        out.append(f'<rect class="nq-frame{" is-sym" if sym else ""}" x="{x0}" y="{y0}" width="{bw}" height="{bw}"/>')
        for r, c in enumerate(p):
            out.append(f'<circle class="nq-dot" cx="{x0 + (n - 1 - c) * s + s / 2:.1f}" cy="{y0 + r * s + s / 2:.1f}" r="{s * 0.32:.1f}"/>')
        out.append(f'<text class="nq-lab" x="{x0 + bw / 2:.1f}" y="{y0 + bw + 16}" text-anchor="middle">×{len(cls)}</text>')
    return "".join(out) + "</svg>"


def class_legend() -> str:
    return ('<span class="viz-legend"><span><i class="nq-key-dot"></i>מלכה</span>'
            '<span><i class="nq-key-sym"></i>הפתרון שחצי סיבוב לא משנה</span>'
            '<span>‏×8 או ×4 : כמה פתרונות שונים יש במחלקה</span></span>')


def burnside_table() -> str:
    fixed = burnside(EX_N)
    lines = ["| הסימטריה | פתרונות שהיא לא משנה |", "|:-:|:-:|"]
    for name, k in zip(SYM_NAMES, fixed):
        lines.append(f"| {name} | {k} |")
    lines.append(f"| **הסכום** | **{sum(fixed)}** |")
    return "\n".join(lines)


# --- part c --------------------------------------------------------------------------------

CON_N = 10


def construction_board() -> str:
    n = CON_N
    cols = construct(n)              # 1-based
    m = n // 2
    qs = {r: cols[r] - 1 for r in range(n)}

    def cell(r, c):
        if qs.get(r) != c:
            return ""
        return "is-even" if r < m else "is-odd"
    return board(n, qs, s=36, base="1", style="max-width:22rem", label=(
        "סעיף ג : הבנייה ל-N = 10. בשורות 1 עד 5 המלכות בעמודות הזוגיות 2, 4, 6, 8, 10, "
        "ובשורות 6 עד 10 בעמודות האי-זוגיות 1, 3, 5, 7, 9. בכל חצי המלכות על קו ששיפועו 2, "
        "ולכן אף שתיים לא באותו אלכסון"), cell_cls=cell)


def construction_legend() -> str:
    return ('<span class="viz-legend"><span><i class="nq-key-even"></i>שורות 1 עד 5 : העמודות הזוגיות</span>'
            '<span><i class="nq-key-odd"></i>שורות 6 עד 10 : העמודות האי-זוגיות</span>'
            '<span>העמודה 1 מימין</span></span>')


def construction_table() -> str:
    lines = ["| ‏\\( N \\) | ‏\\( N \\bmod 6 \\) | העמודה של המלכה בשורות 1 עד \\( N \\) |", "|:-:|:-:|:-:|"]
    for n in range(4, 13):
        cols = construct(n)
        lines.append(f'| {n} | {n % 6} | <span dir="ltr">{", ".join(map(str, cols))}</span> |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [search_board(), search_masks(), search_legend(), counts_table(),
            class_boards(), class_legend(), burnside_table(),
            construction_board(), construction_legend(), construction_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
