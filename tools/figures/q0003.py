#!/usr/bin/env python3
"""Figure of question 0003 (what does this double loop with swap do): the page's example
array at the start and after every pass of the outer loop, the sorted part A[0..i] shaded,
the cells the pass changed framed, an arc over the two cells of every swap of the pass, and
its legend.

    python tools/figures/fill.py 3        # put the blocks on the page

The passes are recorded from the page's own `mystery` (its Python block, run on a list that
logs every write), not written by hand; tests/0003 checks them against a plain replay.
"""

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extract_code import load_python  # noqa: E402

EXAMPLE = [3, 1, 4, 2]
CELL, GAP, PAD, ARC, ROW_GAP = 30, 4, 8, 16, 8


class _Logged(list):
    """A list that records the index of every item write."""

    def __init__(self, items):
        super().__init__(items)
        self.writes = []

    def __setitem__(self, k, v):
        self.writes.append(k)
        super().__setitem__(k, v)


def passes(array=EXAMPLE):
    """[(i, the swaps (i, j) of the pass, the array after it)] from the page's mystery."""
    mystery = load_python(3)["mystery"]
    logged = _Logged(array)
    mystery(logged)
    w = logged.writes                              # A[i], A[j] = A[j], A[i]: two writes per swap
    swaps = [(w[k], w[k + 1]) for k in range(0, len(w), 2)]
    out, a = [], list(array)
    for i in range(len(array)):
        mine = [s for s in swaps if s[0] == i]
        for x, y in mine:
            a[x], a[y] = a[y], a[x]
        out.append((i, mine, list(a)))
    assert a == list(logged)
    return out


def figure(array=EXAMPLE):
    n = len(array)
    row_h = ARC + CELL + ROW_GAP
    width_cells = n * CELL + (n - 1) * GAP
    xl = PAD + width_cells + 16                    # the row labels, right of the cells
    W = xl + 78
    rows = [(None, [], list(array))] + passes(array)
    H = PAD + len(rows) * row_h - ROW_GAP
    p = [f'<svg class="figure" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
         f'aria-label="{escape(aria(array))}">']
    prev = None
    for r, (i, swaps, a) in enumerate(rows):
        y = PAD + r * row_h + ARC
        cx = [PAD + k * (CELL + GAP) + CELL / 2 for k in range(n)]
        for x, z in swaps:
            lo, hi = sorted((cx[x], cx[z]))
            lift = ARC - 3 if hi - lo > CELL + GAP else ARC - 7
            p.append(f'<path class="fc-arc" d="M{lo:g},{y - 2} Q{(lo + hi) / 2:g},{y - 2 - 2 * lift} {hi:g},{y - 2}"/>')
        for k, v in enumerate(a):
            x = PAD + k * (CELL + GAP)
            cls = "fig-one" if i is not None and k <= i else "st-cell"
            p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>'
                     f'<text class="st-text" x="{x + CELL / 2:g}" y="{y + CELL / 2 + 5:g}" text-anchor="middle">{v}</text>')
            if prev is not None and prev[k] != v:
                p.append(f'<rect class="fc-chg" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>')
        ty = y + CELL / 2 + 5
        if i is None:
            p.append(f'<text class="fc-he" x="{xl + 36}" y="{ty:g}" text-anchor="middle" direction="rtl">התחלה</text>')
        else:
            p.append(f'<text class="fc-t" x="{xl}" y="{ty:g}">i = {i}</text>')
        prev = a
    return "".join(p) + "</svg>"


def aria(array=EXAMPLE):
    parts = []
    for i, swaps, a in passes(array):
        sw = "בלי החלפות" if not swaps else "החלפות " + ", ".join(f"A[{x}] עם A[{z}]" for x, z in swaps)
        parts.append(f"אחרי i = {i} ({sw}) : {' '.join(map(str, a))}")
    return f"המערך {' '.join(map(str, array))} אחרי כל מעבר של הלולאה החיצונית. " + "; ".join(parts)


def legend():
    return ('<span class="viz-legend"><span><i class="fc-key-sorted"></i>החלק הממוין <code>A[0..i]</code></span>'
            '<span><i class="fc-key-chg"></i>תא שהמעבר שינה</span>'
            '<span><i class="fc-key-arc"></i>החלפה של <code>A[i]</code> ו-<code>A[j]</code></span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [figure() + "\n\n" + legend()]


if __name__ == "__main__":
    print(passes())
    print("\n\n".join(blocks()))
