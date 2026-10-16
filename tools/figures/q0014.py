#!/usr/bin/env python3
"""Inline SVG figures of question 0014 (random non-overlapping squares and rectangles).

    python tools/figures/q0014.py > /tmp/q0014.html

Prints six figures separated by blank lines, in page order: the problem, legal / illegal
pairs of squares, the four zones, random squares, the cross trap, random rectangles.
The random examples come from the page's own Python code (fixed seeds).
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extract_code import load_python  # noqa: E402

ns = load_python(14)

SQUARE_SEEDS = (13, 12, 26)
RECT_SEEDS = (16, 11, 19)


class Grid:
    """A grid of points (1,1)..(n,m) drawn with its top-left corner at (x0, y0)."""

    def __init__(self, x0, y0, n, m, c):
        self.x0, self.y0, self.n, self.m, self.c = x0, y0, n, m, c

    def px(self, x):
        return self.x0 + (x - 1) * self.c

    def py(self, y):                     # y grows upwards
        return self.y0 + (self.m - y) * self.c

    def background(self, numbers=False):
        out = []
        for x in range(1, self.n + 1):
            out.append(f'<line class="gp-line" x1="{self.px(x)}" x2="{self.px(x)}" '
                       f'y1="{self.py(self.m)}" y2="{self.py(1)}"/>')
        for y in range(1, self.m + 1):
            out.append(f'<line class="gp-line" x1="{self.px(1)}" x2="{self.px(self.n)}" '
                       f'y1="{self.py(y)}" y2="{self.py(y)}"/>')
        for x in range(1, self.n + 1):
            for y in range(1, self.m + 1):
                out.append(f'<circle class="gp-dot" cx="{self.px(x)}" cy="{self.py(y)}" r="1.8"/>')
        if numbers:
            for x in range(1, self.n + 1):
                out.append(f'<text class="tick" x="{self.px(x)}" y="{self.py(1) + 18}" '
                           f'text-anchor="middle">{x}</text>')
            for y in range(1, self.m + 1):
                out.append(f'<text class="tick" x="{self.px(1) - 10}" y="{self.py(y) + 4}" '
                           f'text-anchor="end">{y}</text>')
        return "".join(out)

    def rect(self, s, cls, label=None):
        x1, y1, x2, y2 = s
        out = [f'<rect class="{cls}" x="{self.px(x1)}" y="{self.py(y2)}" '
               f'width="{(x2 - x1) * self.c}" height="{(y2 - y1) * self.c}"/>']
        if label is not None:
            out.append(f'<text class="shp-num" x="{(self.px(x1) + self.px(x2)) / 2}" '
                       f'y="{(self.py(y1) + self.py(y2)) / 2 + 4}" text-anchor="middle">{label}</text>')
        return "".join(out)

    def caption(self, text, dy=22):
        return (f'<text class="legend" x="{(self.px(1) + self.px(self.n)) / 2}" '
                f'y="{self.py(1) + dy}" text-anchor="middle" direction="rtl">{text}</text>')


def svg(width, height, aria, body, max_w=None):
    style = f' style="max-width:{max_w}rem"' if max_w else ""
    return (f'<svg class="figure" viewBox="0 0 {width} {height}"{style} role="img" '
            f'aria-label="{aria}">{body}</svg>')


def shapes(g, items):
    """Shapes with cycling colours and their number in the middle."""
    return "".join(g.rect(s, f"shp-{k % 3 + 1}", k + 1) for k, s in enumerate(items))


def intersection(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def problem():
    g = Grid(40, 14, 10, 8, 30)
    sq = (2, 2, 5, 5)
    rect = (7, 2, 10, 6)
    body = [g.background(numbers=True), g.rect(sq, "shp-1"), g.rect(rect, "shp-2")]
    for (x, y), text, dx, dy, anchor in [((2, 2), "(x1, y1)", 6, 18, "start"),
                                         ((5, 5), "(x2, y2)", -6, -8, "end"),
                                         ((7, 2), "(7, 2)", 6, 18, "start"),
                                         ((10, 6), "(10, 6)", -6, -8, "end")]:
        body.append(f'<circle class="ink-fill" cx="{g.px(x)}" cy="{g.py(y)}" r="4"/>')
        body.append(f'<text class="coord" x="{g.px(x) + dx}" y="{g.py(y) + dy}" text-anchor="{anchor}">{text}</text>')
    body.append(f'<text class="legend halo" x="{(g.px(2) + g.px(5)) / 2}" y="{g.py(3.5) + 5}" '
                f'text-anchor="middle" direction="rtl">ריבוע 3 על 3</text>')
    body.append(f'<text class="legend halo" x="{(g.px(7) + g.px(10)) / 2}" y="{g.py(4.5) + 5}" '
                f'text-anchor="middle" direction="rtl">מלבן</text>')
    body.append(f'<text class="legend halo" x="{(g.px(7) + g.px(10)) / 2}" y="{g.py(3.5) + 5}" '
                f'text-anchor="middle" direction="rtl">רוחב 3, גובה 4</text>')
    return svg(g.px(10) + 20, g.py(1) + 26, "grid של 10 על 8 נקודות, ריבוע מ-(x1, y1) עד (x2, y2) ומלבן מ-(7, 2) עד (10, 6)",
               "".join(body), max_w=30)


def pair_panels(pairs, cols, n, m, c, aria):
    """Panels with two shapes each; the overlap area (if any) is highlighted."""
    w, h = (n - 1) * c + 34, (m - 1) * c + 52
    body = []
    for k, (a, b, ok, text) in enumerate(pairs):
        g = Grid(17 + (k % cols) * w, 10 + (k // cols) * h, n, m, c)
        body += [g.background(), g.rect(a, "shp-1"), g.rect(b, "shp-2")]
        cut = intersection(a, b)
        if cut[0] < cut[2] and cut[1] < cut[3]:
            body.append(g.rect(cut, "shp-bad"))
        body.append(g.caption(("✓ " if ok else "✗ ") + text))
    rows = (len(pairs) + cols - 1) // cols
    return svg(cols * w, rows * h, aria, "".join(body))


def cases():
    a = (1, 1, 3, 3)
    pairs = [(a, (4, 2, 6, 4), True, "רחוקים"),
             (a, (3, 1, 5, 3), True, "צלע משותפת"),
             (a, (3, 2, 6, 5), True, "חלק מצלע"),
             (a, (3, 3, 5, 5), True, "פינה משותפת"),
             ((1, 1, 4, 4), (3, 2, 5, 4), False, "חפיפה"),
             ((1, 1, 5, 5), (2, 2, 4, 4), False, "אחד בתוך השני")]
    return pair_panels(pairs, 3, 6, 5, 22, "זוגות של ריבועים: ארבעה מותרים ושניים אסורים")


def zones():
    g = Grid(20, 10, 10, 8, 30)
    a = (4, 3, 7, 6)
    x1, y1, x2, y2 = a
    body = [g.background()]
    for z in [(1, 1, x1, 8), (x2, 1, 10, 8), (1, 1, 10, y1), (1, y2, 10, 8)]:
        body.append(g.rect(z, "sep-zone"))
    for x in (x1, x2):
        body.append(f'<line class="dash" x1="{g.px(x)}" x2="{g.px(x)}" y1="{g.py(8)}" y2="{g.py(1)}"/>')
    for y in (y1, y2):
        body.append(f'<line class="dash" x1="{g.px(1)}" x2="{g.px(10)}" y1="{g.py(y)}" y2="{g.py(y)}"/>')
    body.append(g.rect(a, "shp-1"))
    body.append(f'<text class="shp-num" x="{(g.px(x1) + g.px(x2)) / 2}" y="{(g.py(y1) + g.py(y2)) / 2 + 5}" '
                f'text-anchor="middle">i</text>')
    for text, x, y in [("משמאל", (1 + x1) / 2, 4.5), ("מימין", (x2 + 10) / 2, 4.5),
                       ("מתחת", 5.5, (1 + y1) / 2), ("מעל", 5.5, (y2 + 8) / 2)]:
        body.append(f'<text class="zone-label" x="{g.px(x)}" y="{g.py(y) + 5}" text-anchor="middle" '
                    f'direction="rtl">{text}</text>')
    return svg(g.px(10) + 20, g.py(1) + 12, "ארבעת האזורים סביב ריבוע i: משמאל, מימין, מתחת ומעל",
               "".join(body), max_w=22)


def random_examples(squares, seeds):
    c, w = 22, 9 * 22 + 40
    body = []
    for k, seed in enumerate(seeds):
        items = ns["random_shapes"](10, 8, 6, squares=squares, rng=random.Random(seed))
        assert ns["shapes_ok"](10, 8, items, squares)
        g = Grid(20 + k * w, 10, 10, 8, c)
        name = "ריבועים" if squares else "מלבנים"
        body += [g.background(), shapes(g, items), g.caption(f"הגרלה {k + 1}: {len(items)} {name}")]
    what = "ריבועים" if squares else "מלבנים"
    return svg(len(seeds) * w, 7 * c + 44, f"שלוש הגרלות של {what} בלי חפיפה", "".join(body))


def cross():
    c = 26
    g = Grid(46, 10, 9, 8, c)
    a, b = (1, 4, 9, 6), (4, 1, 6, 8)
    body = [g.background(), g.rect(a, "shp-1"), g.rect(b, "shp-2"), g.rect(intersection(a, b), "shp-bad")]
    for s, cls in ((a, "s1-fill"), (b, "s3-fill")):          # corners: none inside the other shape
        for x in (s[0], s[2]):
            for y in (s[1], s[3]):
                body.append(f'<circle class="{cls}" cx="{g.px(x)}" cy="{g.py(y)}" r="4"/>')
    # projections: x below the grid, y to the left
    for k, (s, cls) in enumerate(((a, "s1-fill"), (b, "s3-fill"))):
        body.append(f'<rect class="{cls}" x="{g.px(s[0])}" y="{g.py(1) + 10 + 9 * k}" '
                    f'width="{(s[2] - s[0]) * c}" height="6" rx="3"/>')
        body.append(f'<rect class="{cls}" x="{g.px(1) - 34 + 9 * k}" y="{g.py(s[3])}" '
                    f'width="6" height="{(s[3] - s[1]) * c}" rx="3"/>')
    body.append(g.caption("✗ צלב: אין פינה בפנים, ויש חפיפה", dy=50))

    h = Grid(g.px(9) + 70, 10, 7, 8, c)
    legal = [(1, 1, 4, 3), (4, 1, 7, 6), (1, 3, 3, 8), (3, 6, 7, 8), (3, 3, 4, 6)]
    assert ns["shapes_ok"](7, 8, legal, squares=False)
    body += [h.background(), shapes(h, legal), h.caption("✓ מלבנים צמודים", dy=50)]
    return svg(h.px(7) + 16, g.py(1) + 60,
               "שני מלבנים בצורת צלב חופפים בלי שאף פינה נמצאת בתוך המלבן השני, ולידם חמישה מלבנים צמודים בלי חפיפה",
               "".join(body))


if __name__ == "__main__":
    for fig in (problem, cases, zones, lambda: random_examples(True, SQUARE_SEEDS),
                cross, lambda: random_examples(False, RECT_SEEDS)):
        print(fig(), "\n")
