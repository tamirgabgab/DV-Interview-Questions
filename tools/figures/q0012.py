#!/usr/bin/env python3
"""Tables and figures of part c of question 0012 (sort the digits and subtract, three
digits in base b).

    python tools/figures/fill.py 12        # put the blocks on the page

The reference here is independent of the page code: step() sorts the three digits of x in
base b and subtracts, attractor() is the fixed point (b even) or the two values of the
cycle (b odd) from the closed forms, and chain() applies the step until the value is in
the attractor or 0. blocks() returns, in page order: the table of the fixed points of
the even bases, the table of the cycles of the odd bases, the step-by-step example in
base 7, the map d -> max(b - d, d - 1) drawn for base 10 and for base 7, and its legend.
tests/0012 checks every number against the page code and against an exhaustive run over
every base from 2 to 16.
"""

import sys
from pathlib import Path

RLM = "‏"
DIGITS = "0123456789ABCDEF"


# --- the model --------------------------------------------------------------------------

def digits(x, b):
    return [x // (b * b), x // b % b, x % b]


def text(x, b):
    """x as three digits in base b (leading zeros kept)."""
    return "".join(DIGITS[v] for v in digits(x, b))


def step(x, b):
    lo, mid, hi = sorted(digits(x, b))
    return (hi * b * b + mid * b + lo) - (lo * b * b + mid * b + hi)


def spread(x, b):
    """d = the largest digit minus the smallest."""
    v = digits(x, b)
    return max(v) - min(v)


def attractor(b):
    """The fixed point of an even base, the two values of the cycle of an odd base."""
    if b % 2 == 0:
        return [(b // 2) * (b * b - 1)]
    k = b // 2
    return [k * (b * b - 1), (k + 1) * (b * b - 1)]


def chain(x, b):
    """The values from x until one is in the attractor (or 0): the first is x."""
    out = [x]
    while out[-1] != 0 and out[-1] not in attractor(b):
        out.append(step(out[-1], b))
        assert len(out) < 40
    return out


def chain_lengths(b):
    """How many of the b^3 numbers need k steps (to the attractor, or to 0)."""
    hist = {}
    for x in range(b ** 3):
        n = len(chain(x, b)) - 1
        hist[n] = hist.get(n, 0) + 1
    return hist


# --- tables ------------------------------------------------------------------------------

def even_table(bases=(2, 4, 6, 8, 10, 12, 14, 16)):
    lines = ["| הבסיס b | ‏d = b / 2 | נקודת השבת בבסיס b | הערך העשרוני |", "|:-:|:-:|:-:|:-:|"]
    for b in bases:
        x = attractor(b)[0]
        lines.append(f"| {RLM}{b} | {RLM}{b // 2} | {RLM}**{text(x, b)}** | {RLM}{x:,} |")
    return "\n".join(lines)


def odd_table(bases=(3, 5, 7, 9, 11, 13, 15)):
    lines = ["| הבסיס b | ‏d במחזור | המחזור בבסיס b | הערכים העשרוניים |", "|:-:|:-:|:-:|:-:|"]
    for b in bases:
        x1, x2 = attractor(b)
        lines.append(f"| {RLM}{b} | {RLM}{b // 2} ↔ {b // 2 + 1} | {RLM}**{text(x1, b)}** ↔ **{text(x2, b)}** | {RLM}{x1:,} ↔ {x2:,} |")
    return "\n".join(lines)


def example_table(x0=301, b=7, steps=5):
    lines = [f"| צעד | ‏X בבסיס {b} | מהגדול לקטן | מהקטן לגדול | ההפרש | ‏d |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    x = x0
    for i in range(1, steps + 1):
        lo, mid, hi = sorted(digits(x, b))
        big = hi * b * b + mid * b + lo
        small = lo * b * b + mid * b + hi
        y = step(x, b)
        lines.append(f"| {RLM}{i} | {RLM}{text(x, b)} ({x}) | {RLM}{text(big, b)} ({big}) | {RLM}{text(small, b)} ({small}) | "
                     f"{RLM}{big} − {small} = {y} = **{text(y, b)}** | {RLM}{spread(x, b)} |")
        x = y
    return "\n".join(lines)


# --- the figures --------------------------------------------------------------------------

def dmap_svg(b, path=None):
    """The map d -> max(b - d, d - 1) on an axis from 1 to b - 1: an arrow from every d to
    its image (above the axis when d goes up, below when it goes down), the fixed point or
    the cycle marked, and optionally the path of one number's chain emphasised."""
    W, H, X0, X1, YA = 640, 170, 40, 600, 100
    X = lambda d: X0 + (d - 1) * (X1 - X0) / (b - 2) if b > 2 else (X0 + X1) / 2
    att = [v // (b * b - 1) for v in attractor(b)]                   # the d values of the attractor
    path = set(path or [])
    p = [f'<svg class="figure kb-map" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
         f'aria-label="המפה של d בבסיס {b} : מכל d חץ ל-max(b − d, d − 1), {"נקודת שבת ב-" + str(att[0]) if len(att) == 1 else "מחזור בין " + str(att[0]) + " ל-" + str(att[1])}">',
         f'<line class="kb-axis" x1="{X0}" x2="{X1}" y1="{YA}" y2="{YA}"/>']
    for d in range(1, b):
        nd = max(b - d, d - 1)
        p.append(f'<text class="kb-tick" x="{X(d):.1f}" y="{YA + 18}" text-anchor="middle">{d}</text>')
        if nd == d:
            continue
        up = nd > d
        xa, xb = X(d), X(nd)
        bulge = (YA - 12 - 8 * abs(nd - d)) if up else (YA + 26 + 8 * abs(nd - d))
        cls = "kb-arrow" + (" is-path" if (d, nd) in path else "") + (" is-cycle" if d in att and nd in att else "")
        p.append(f'<path class="{cls}" d="M {xa:.1f} {YA - 4 if up else YA + 4} Q {(xa + xb) / 2:.1f} {bulge:.1f} {xb:.1f} {YA - 4 if up else YA + 4}"/>')
        p.append(f'<circle class="{cls}" cx="{xb:.1f}" cy="{YA - 4 if up else YA + 4}" r="2.6"/>')
    for d in att:
        p.append(f'<circle class="kb-fixed" cx="{X(d):.1f}" cy="{YA}" r="7"><title>d = {d}</title></circle>')
    p.append(f'<text class="legend" x="{X0}" y="{H - 8}">b = {b}</text></svg>')
    return "".join(p)


def dmap_legend():
    return ('<span class="viz-legend"><span><i class="kb-key-arrow"></i>החץ מ-d ל-max(b − d, d − 1) : מעל הציר כש-d עולה, מתחתיו כשהוא יורד</span>'
            '<span><i class="kb-key-fixed"></i>נקודת השבת (בסיס זוגי) או שני ערכי המחזור (אי-זוגי)</span>'
            '<span><i class="kb-key-path"></i>המסלול של הדוגמה 610 בבסיס 7</span></span>')


def blocks():
    """The generated blocks, in page order."""
    path7 = [(spread(x, 7), spread(step(x, 7), 7)) for x in chain(301, 7)[:-1]]
    return [even_table(), odd_table(), example_table(), dmap_svg(10), dmap_svg(7, path7), dmap_legend()]


if __name__ == "__main__":
    print([text(v, 7) for v in chain(301, 7)], attractor(10), attractor(7))
    print("\n\n".join(blocks()))
