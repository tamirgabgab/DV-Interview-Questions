#!/usr/bin/env python3
"""Tables of question 0036 (a 4-bit LFSR: maximal taps against a short cycle).

    python tools/figures/fill.py 36        # put the blocks on the page

Fibonacci LFSR, 4 bits, shifting right: the output bit is s[0], the feedback bit is the
XOR of the tapped bits and enters at the top. A polynomial x^4 + x^k + ... + 1 taps the
state bits s[4 - k]; x^4 itself is s[0], the bit that leaves. blocks() returns, in page
order: the state sequence of x^4 + x^3 + 1 from 0001 (15 states), the sequence of
x^4 + x^2 + 1 from 0001 (6 states), the table of every polynomial x^4 + ... + 1 with
its period from 0001, and the register of the hardware follow-up (the flops s[3] .. s[0],
the taps of x^4 + x^3 + 1 wired to one XOR; the classes are the box's, 11-questions.css).
tests/0036 checks the numbers against the page code.
"""

from itertools import combinations

WIDTH = 4
RLM = "‏"
MAXIMAL = (4, 3)
SHORT = (4, 2)


def mask_of(taps, width=WIDTH):
    """The state bits a polynomial taps: power k is bit width - k (x^width is bit 0)."""
    return sum(1 << (width - k) for k in taps)


def step(state, taps, width=WIDTH):
    fb = bin(state & mask_of(taps, width)).count("1") & 1
    return (state >> 1) | (fb << (width - 1))


def sequence(taps, seed=1, width=WIDTH):
    """The states from the seed until the first repeat (the cycle, when the seed is on it)."""
    out, s = [], seed
    while s not in out:
        out.append(s)
        s = step(s, taps, width)
    return out


def period(taps, seed=1, width=WIDTH):
    """Length of the cycle reached from the seed (the tail before it is not counted)."""
    seen, s, k = {}, seed, 0
    while s not in seen:
        seen[s] = k
        s = step(s, taps, width)
        k += 1
    return k - seen[s]


def poly(taps):
    return " + ".join(f"x^{k}" if k > 1 else "x" for k in sorted(taps, reverse=True)) + " + 1"


def sequence_table(taps):
    seq = sequence(taps)
    rows = ["| צעד | המצב | הביט היוצא | היזון חוזר |", "|:-:|:-:|:-:|:-:|"]
    for i, s in enumerate(seq):
        fb = bin(s & mask_of(taps)).count("1") & 1
        rows.append(f"| {RLM}{i} | {RLM}`{s:04b}` | {RLM}{s & 1} | {RLM}{fb} |")
    nxt = step(seq[-1], taps)
    rows.append(f"| {RLM}{len(seq)} | {RLM}`{nxt:04b}` | | חוזר לצעד {seq.index(nxt)} |")
    return "\n".join(rows)


def all_polys():
    """Every x^4 + (some of x^3, x^2, x) + 1, with the period from 0001."""
    out = []
    for r in range(0, 4):
        for extra in combinations((3, 2, 1), r):
            taps = (4, *extra)
            out.append((taps, period(taps)))
    return out


def polys_table():
    rows = ["| הפולינום | ביטי ה-taps (‏`s[3:0]`) | אורך המחזור מ-`0001` | מקסימלי? |", "|:-:|:-:|:-:|:-:|"]
    for taps, p in all_polys():
        rows.append(f"| {RLM}\\( {poly(taps)} \\) | {RLM}`{mask_of(taps):04b}` | {RLM}{p} | {'✓' if p == 2 ** WIDTH - 1 else ''} |")
    return "\n".join(rows)


def register_svg(taps=MAXIMAL, width=WIDTH):
    """The register as hardware: the flops s[width - 1] .. s[0] left to right, the tapped
    ones outlined and wired to one XOR under the row, fb back into the left end, s[0] out
    at the right (the geometry of the box's live register, explorer/lfsr.js regSvg)."""
    cw, x0, y, ch = 40, 64, 22, 40
    bus = y + ch + 34
    w, h = x0 + width * (cw + 4) + 70, bus + 38
    cx = lambda b: x0 + (width - 1 - b) * (cw + 4) + cw // 2  # noqa: E731
    tapped = [b for b in range(width) if (mask_of(taps, width) >> b) & 1]
    o = [f'<div class="lf-fig"><svg class="figure lf-regsvg" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.1f}rem" role="img" '
         f'aria-label="ה-LFSR כחומרה : ארבעה פלופים s[3] עד s[0] בשורה, XOR של s[0] ו-s[1] חוזר כ-fb אל s[3], ו-s[0] הוא המוצא">',
         '<defs><marker id="lf-arrow-hw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 Z" class="lf-head"/></marker></defs>']
    for b in tapped:
        o.append(f'<line class="lf-wire" x1="{cx(b)}" y1="{y + ch}" x2="{cx(b)}" y2="{bus}"/><circle class="lf-dot" cx="{cx(b)}" cy="{bus}" r="3"/>')
    xor = 26
    o.append(f'<line class="lf-wire" x1="{xor + 12}" y1="{bus}" x2="{max(cx(b) for b in tapped)}" y2="{bus}"/>'
             f'<circle class="lf-xor" cx="{xor}" cy="{bus}" r="12"/><path class="lf-wire" d="M{xor - 8},{bus} H{xor + 8} M{xor},{bus - 8} V{bus + 8}"/>'
             f'<path class="lf-wire" d="M{xor},{bus - 12} V{y + ch // 2} H{x0 - 2}" fill="none" marker-end="url(#lf-arrow-hw)"/>'
             f'<text class="lf-regfb" x="{xor + 4}" y="{bus + 30}" text-anchor="middle">fb</text>')
    for b in range(width):
        cls = "lf-cell is-tap" if b in tapped else "lf-cell"
        o.append(f'<rect class="{cls}" x="{cx(b) - cw // 2}" y="{y}" width="{cw}" height="{ch}" rx="4"/>'
                 f'<text class="lf-celli" x="{cx(b)}" y="{y + ch // 2 + 4}" text-anchor="middle">s[{b}]</text>')
    ox = cx(0) + cw // 2
    o.append(f'<path class="lf-wire" d="M{ox + 2},{y + ch // 2} H{ox + 34}" marker-end="url(#lf-arrow-hw)"/>'
             f'<text class="lf-regfb" x="{ox + 50}" y="{y + ch // 2 + 4}" text-anchor="middle">out</text>')
    return "".join(o) + "</svg></div>"


def blocks():
    """The generated blocks, in page order."""
    return [sequence_table(MAXIMAL), sequence_table(SHORT), polys_table(), register_svg()]


if __name__ == "__main__":
    print(period(MAXIMAL), period(SHORT), [(t, p) for t, p in all_polys()])
    print("\n\n".join(blocks()))
