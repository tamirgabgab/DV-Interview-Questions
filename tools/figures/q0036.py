#!/usr/bin/env python3
"""Tables of question 0036 (a 4-bit LFSR: maximal taps against a short cycle).

    python tools/figures/fill.py 36        # put the blocks on the page

Fibonacci LFSR, 4 bits, shifting right: the output bit is s[0], the feedback bit is the
XOR of the tapped bits and enters at the top. A polynomial x^4 + x^k + ... + 1 taps the
state bits s[4 - k]; x^4 itself is s[0], the bit that leaves. blocks() returns, in page
order: the state sequence of x^4 + x^3 + 1 from 0001 (15 states), the sequence of
x^4 + x^2 + 1 from 0001 (6 states), and the table of every polynomial x^4 + ... + 1 with
its period from 0001. tests/0036 checks the numbers against the page code.
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
    rows = ["| הפולינום | ביטי ה-taps (‏`s[3:0]`) | התקופה מ-`0001` | מקסימלי? |", "|:-:|:-:|:-:|:-:|"]
    for taps, p in all_polys():
        rows.append(f"| {RLM}\\( {poly(taps)} \\) | {RLM}`{mask_of(taps):04b}` | {RLM}{p} | {'✓' if p == 2 ** WIDTH - 1 else ''} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [sequence_table(MAXIMAL), sequence_table(SHORT), polys_table()]


if __name__ == "__main__":
    print(period(MAXIMAL), period(SHORT), [(t, p) for t, p in all_polys()])
    print("\n\n".join(blocks()))
