#!/usr/bin/env python3
"""Figures and tables of question 0059 (the next number with as many ones: Gosper's step,
the previous one through the complement, and the place of a number in the sorted list).

    python tools/figures/fill.py 59        # put the blocks on the page

The reference here is independent of the page code: brute_next / brute_prev search
number by number, and brute_rank counts the smaller numbers with as many ones. gosper()
gives the rows of the formula, the same rows the box draws. blocks() returns, in page
order: the steps of next(92) in 8 bits, their legend, the numbers with two ones in 5 bits
next to their complements, the steps of prev(99), and the sum that gives the place of 92.
"""

from html import escape
from math import comb

RLM = "‏"
X_A, W_A = 92, 8            # 0101_1100 -> 0110_0011 = 99
X_B = 99                    # prev(99) = 92
W_C, K_C = 5, 2             # the complement table


def ones(x):
    return bin(x).count("1")


def brute_next(x, w):
    """The smallest number above x in w bits with as many ones; 0 if there is none."""
    k = ones(x)
    return next((y for y in range(x + 1, 1 << w) if ones(y) == k), 0) if x else 0


def brute_prev(x, w):
    k = ones(x)
    return next((y for y in range(x - 1, 0, -1) if ones(y) == k), 0) if x else 0


def brute_rank(x):
    k = ones(x)
    return sum(1 for y in range(x) if ones(y) == k)


def set_bits(v):
    return {p for p in range(v.bit_length()) if (v >> p) & 1}


def gosper(x, w):
    """The rows of next(x): (label, value, marked bits). The last row is the answer, or the
    overflow when the block of ones is already at the top."""
    c = x & -x
    r = x + c
    t = c.bit_length() - 1                       # the lowest one
    m = ((x >> t) ^ ((x >> t) + 1)).bit_length() - 1   # the length of the lowest block
    rows = [("x", x, set(range(t, t + m))), ("c = x & −x", c, {t}), ("r = x + c", r, {t + m})]
    if r >> w:
        return rows, 0
    s = ((x ^ r) >> 2) // c
    rows += [("x ^ r", x ^ r, set(range(t, t + m + 1))), ("(x ^ r) >> 2", (x ^ r) >> 2, set_bits((x ^ r) >> 2)),
             ("s = … / c", s, set(range(m - 1))), ("r | s", r | s, set(range(m - 1)) | {t + m})]
    return rows, r | s


def bits_table(rows, w, label):
    """An HTML table of bit rows: the name, the w bits (most significant on the left), the value."""
    h = f'<div class="gs-scroll"><table class="gs-bits" dir="ltr" aria-label="{label}"><tbody>'
    for name, v, marks in rows:
        cells = "".join(f'<td class="gs-b{" is-one" if (v >> p) & 1 else ""}{" is-mark" if p in marks else ""}">{(v >> p) & 1}</td>'
                        for p in range(w - 1, -1, -1))
        h += f'<tr><th>{escape(name)}</th>{cells}<td class="gs-val">{v}</td></tr>'
    return h + "</tbody></table></div>"


def legend():
    return ('<span class="viz-legend"><span><i class="gs-key-one"></i>ביט דולק</span>'
            '<span><i class="gs-key-mark"></i>הביטים שהשלב עוסק בהם</span></span>')


def complement_table(w, k):
    """The numbers with k ones in w bits in order, next to their complements."""
    xs = [y for y in range(1 << w) if ones(y) == k]
    mask = (1 << w) - 1
    rows = ["| המקום של x | ‏x | ‏~x | המקום של ~x |", "|:-:|:-:|:-:|:-:|"]
    for i, x in enumerate(xs):
        y = ~x & mask
        rows.append(f"| {RLM}{i} | {RLM}`{x:0{w}b}` ({x}) | {RLM}`{y:0{w}b}` ({y}) | {RLM}{brute_rank(y)} |")
    return "\n".join(rows)


def prev_rows(x, w):
    mask = (1 << w) - 1
    y = brute_next(~x & mask, w)
    return [("x", x, set()), ("~x", ~x & mask, set()), ("next(~x)", y, set()), ("~next(~x)", ~y & mask, set())]


def rank_table(x):
    rows = ["| ‏i (האחד ה-i מלמטה) | המקום שלו \\( p_i \\) | ‏\\( \\binom{p_i}{i} \\) |", "|:-:|:-:|:-:|"]
    total, i = 0, 0
    for p in range(x.bit_length()):
        if (x >> p) & 1:
            i += 1
            total += comb(p, i)
            rows.append(f"| {RLM}{i} | {RLM}{p} | {RLM}{comb(p, i)} |")
    rows.append(f"| **סך הכול** | | **{RLM}{total}** |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    rows, _ = gosper(X_A, W_A)
    return [bits_table(rows, W_A, "השלבים של הנוסחה על 92 ב-8 ביטים"), legend(), complement_table(W_C, K_C),
            bits_table(prev_rows(X_B, W_A), W_A, "הקודם של 99 דרך המשלים"), rank_table(X_A)]


if __name__ == "__main__":
    print(brute_next(X_A, W_A), brute_prev(X_B, W_A), brute_rank(X_A), brute_prev(96, 8), comb(8, 4))
    print("\n\n".join(blocks()))
