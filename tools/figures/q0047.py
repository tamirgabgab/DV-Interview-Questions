#!/usr/bin/env python3
"""Figure of question 0047 (trapping rain water): the example row [3, 0, 2, 0, 4] as
columns of ground with the water that stays between them, and its legend.

    python tools/figures/fill.py 47        # put the blocks on the page

The water above each column is computed here from its definition, min(highest on the left,
highest on the right) minus the height, independently of the page code.
"""

HEIGHTS = [3, 0, 2, 0, 4]
CELL, GAP, PAD, TOP = 40, 4, 8, 8


def water(heights):
    """The water above every column: the lower of the two highest walls, minus the column."""
    return [max(0, min(max(heights[: i + 1]), max(heights[i:])) - h) for i, h in enumerate(heights)]


def columns_svg(heights=HEIGHTS):
    levels = max(heights)
    w_of = water(heights)
    n = len(heights)
    width = 2 * PAD + n * CELL + (n - 1) * GAP
    base = TOP + levels * (CELL + GAP)
    height = base + 26
    total = sum(w_of)
    p = [f'<svg class="figure" viewBox="0 0 {width} {height}" style="max-width:{width / 16:.1f}rem" role="img" '
         f'aria-label="העמודים {", ".join(map(str, heights))} : נשארות {total} יחידות מים">']
    for i, (h, wv) in enumerate(zip(heights, w_of)):
        x = PAD + i * (CELL + GAP)
        for lv in range(levels):
            y = base - (lv + 1) * (CELL + GAP) + GAP
            cls = "fig-ground" if lv < h else "fig-water" if lv < h + wv else "st-cell"
            p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>')
        p.append(f'<text class="st-text" x="{x + CELL / 2:g}" y="{base + 20}" text-anchor="middle">{h}</text>')
    return "".join(p) + "</svg>"


def legend():
    total = sum(water(HEIGHTS))
    return ('<span class="viz-legend"><span><i class="fig-key-ground"></i>עמוד</span>'
            f'<span><i class="fig-key-water"></i>מים שנשארים, {total} יחידות</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [columns_svg(), legend()]


if __name__ == "__main__":
    print(water(HEIGHTS), sum(water(HEIGHTS)))
    print("\n\n".join(blocks()))
