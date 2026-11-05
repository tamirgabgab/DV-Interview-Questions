#!/usr/bin/env python3
"""Figure of question 0002 (swap two variables), part c: the four bits of a and b at the
start and after each of the three XOR steps of the page's example (a = 5, b = 3), the bits
that a step changed framed, and its legend.

    python tools/figures/fill.py 2        # put the blocks on the page

The steps are computed here from the definition of XOR, independently of the page code;
tests/0002 checks them against the page's swap_xor and its numeric example table.
"""

from html import escape

A0, B0, BITS = 5, 3, 4
CELL, GAP, PAD, TOP, ROW = 26, 3, 8, 30, 38
STEPS = [("a", "a = a ^ b"), ("b", "b = a ^ b"), ("a", "a = a ^ b")]


def rows(a=A0, b=B0):
    """[(label, written variable or None, a, b)]: the start, then the state after every step."""
    out = [("start", None, a, b)]
    for target, code in STEPS:
        if target == "a":
            a = a ^ b
        else:
            b = a ^ b
        out.append((code, target, a, b))
    return out


def bits(v):
    """The bits of v, the most significant first (left)."""
    return [(v >> k) & 1 for k in range(BITS - 1, -1, -1)]


def figure():
    group = BITS * CELL + (BITS - 1) * GAP
    xb, xa = PAD, PAD + group + 44
    xl = xa + group + 52                       # the step labels, right of a
    W = xl + 112
    H = TOP + len(rows()) * ROW - (ROW - CELL) + PAD
    p = [f'<svg class="figure" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
         f'aria-label="{escape(aria())}">']
    p.append(f'<text class="fc-t fc-b" x="{xb + group / 2:g}" y="{TOP - 10}" text-anchor="middle">b</text>'
             f'<text class="fc-t fc-b" x="{xa + group / 2:g}" y="{TOP - 10}" text-anchor="middle">a</text>')
    prev = None
    for r, (label, target, a, b) in enumerate(rows()):
        y = TOP + r * ROW
        for x0, name, v in ((xb, "b", b), (xa, "a", a)):
            old = None if prev is None or target != name else (prev[2] if name == "a" else prev[3])
            for k, bit in enumerate(bits(v)):
                x = x0 + k * (CELL + GAP)
                cls = "fig-one" if bit else "st-cell"
                p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>'
                         f'<text class="st-text" x="{x + CELL / 2:g}" y="{y + CELL / 2 + 5:g}" text-anchor="middle">{bit}</text>')
                if old is not None and bits(old)[k] != bit:
                    p.append(f'<rect class="fc-chg" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>')
            p.append(f'<text class="fc-sub" x="{x0 + group + 8}" y="{y + CELL / 2 + 5:g}">({v})</text>')
        if target is None:
            p.append(f'<text class="fc-he" x="{xl + 50}" y="{y + CELL / 2 + 5:g}" text-anchor="middle" direction="rtl">התחלה</text>')
        else:
            p.append(f'<text class="fc-t" x="{xl}" y="{y + CELL / 2 + 5:g}">{r}: {escape(label)}</text>')
        prev = (label, target, a, b)
    return "".join(p) + "</svg>"


def aria():
    steps = ", ".join(f"אחרי שלב {r} a = {a} ו-b = {b}" for r, (_, _, a, b) in enumerate(rows()) if r)
    return f"ארבעת הביטים של a ושל b : בהתחלה a = {A0} ו-b = {B0}, {steps}"


def legend():
    return ('<span class="viz-legend"><span><i class="fig-key-one"></i>ביט 1</span>'
            '<span><i class="fc-key-chg"></i>ביט שהשלב שינה</span>'
            '<span>הביט הגבוה משמאל, והערך העשרוני בסוגריים</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [figure() + "\n\n" + legend()]


if __name__ == "__main__":
    print(rows())
    print("\n\n".join(blocks()))
