#!/usr/bin/env python3
"""Figure of question 0045 (the odd ball among 12 in three weighings): what the first
weighing, 1 to 4 against 5 to 8, leaves for each of its three results, as a row of the
twelve balls per result, and its legend.

    python tools/figures/fill.py 45        # put the blocks on the page

The candidates are worked out here from the 24 cases (each ball heavy or light) and the
result each one gives, independently of the page code.
"""

LEFT, RIGHT = range(1, 5), range(5, 9)
BALLS = range(1, 13)
R, STEP, PAD, ROW, TITLE = 14, 33, 10, 70, 22
RESULTS = [("left", "שמאל כבד"), ("even", "מאוזן"), ("right", "ימין כבד")]


def result(ball, heavy):
    """The first weighing when `ball` is the odd one, heavy or light."""
    if ball in LEFT:
        return "left" if heavy else "right"
    if ball in RIGHT:
        return "right" if heavy else "left"
    return "even"


def candidates(res):
    """Ball -> "heavy", "light", "both" or None (known good) after the result `res`."""
    out = {}
    for b in BALLS:
        h, l = result(b, True) == res, result(b, False) == res
        out[b] = "both" if h and l else "heavy" if h else "light" if l else None
    return out


def rows_svg():
    width = 2 * PAD + 12 * STEP
    height = len(RESULTS) * ROW + PAD
    p = [f'<svg class="figure" viewBox="0 0 {width} {height}" style="max-width:{width / 16:.1f}rem" role="img" '
         'aria-label="מה נשאר אחרי השקילה הראשונה, 1 עד 4 מול 5 עד 8 : שמונה אפשרויות בכל תוצאה">']
    for r, (res, title) in enumerate(RESULTS):
        y0 = r * ROW + TITLE
        cases = sum((v == "both") + (v is not None) for v in candidates(res).values())
        p.append(f'<text class="st-text st-sm" x="{width - PAD}" y="{y0 - 6}" text-anchor="start" direction="rtl">{title}\u00a0: {cases} אפשרויות</text>')
        for k, b in enumerate(BALLS):
            cls = {"heavy": "fig-heavy", "light": "fig-light", "both": "fig-both", None: "st-done"}[candidates(res)[b]]
            cx, cy = PAD + R + 2 + k * STEP, y0 + R + 8
            p.append(f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{R}"/>'
                     f'<text class="st-text st-sm" x="{cx}" y="{cy + 4}" text-anchor="middle">{b}</text>')
    return "".join(p) + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="fig-key-heavy"></i>אולי כבד</span>'
            '<span><i class="fig-key-light"></i>אולי קל</span>'
            '<span><i class="fig-key-both"></i>אולי כבד ואולי קל</span>'
            '<span><i class="fig-key-good"></i>תקין</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [rows_svg(), legend()]


if __name__ == "__main__":
    for res, _ in RESULTS:
        print(res, candidates(res))
    print("\n\n".join(blocks()))
