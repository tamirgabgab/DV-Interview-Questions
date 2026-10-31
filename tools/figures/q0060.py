#!/usr/bin/env python3
"""Figures and tables of question 0060 (the next number with as many ones: Gosper's step,
the previous one through the complement, and the same for zeros, counted without the
leading ones, where the length of the number may change).

    python tools/figures/fill.py 60        # put the blocks on the page

The reference here is independent of the page code: brute_next / brute_prev and
brute_next0 / brute_prev0 search number by number. gosper() gives the rows of the
formula, the same rows the box draws. blocks() returns, in page order: the steps of
next(92) in 8 bits, their legend, the numbers with two ones in 5 bits next to their
complements, the steps of prev(99), the numbers with three zeros by length, and the
rows of the next number after 120 with three zeros (a longer one).
"""

from html import escape

RLM = "‏"
X_A, W_A = 92, 8            # 0101_1100 -> 0110_0011 = 99
X_B = 99                    # prev(99) = 92
W_C, K_C = 5, 2             # the complement table
X_C = 120                   # 111_1000, three zeros -> 1000_1111 = 143


def ones(x):
    return bin(x).count("1")


def brute_next(x, w):
    """The smallest number above x in w bits with as many ones; 0 if there is none."""
    k = ones(x)
    return next((y for y in range(x + 1, 1 << w) if ones(y) == k), 0) if x else 0


def brute_prev(x, w):
    k = ones(x)
    return next((y for y in range(x - 1, 0, -1) if ones(y) == k), 0) if x else 0


def zeros(x):
    """The zeros of x from its top one down (no leading zeros)."""
    return x.bit_length() - ones(x)


def brute_next0(x):
    """The smallest number above x with as many zeros (any length); x >= 1."""
    z = zeros(x)
    return next(y for y in range(x + 1, 1 << (x.bit_length() + 2)) if zeros(y) == z)


def brute_prev0(x):
    """The largest number below x with as many zeros; 0 if there is none."""
    z = zeros(x)
    return next((y for y in range(x - 1, 0, -1) if zeros(y) == z), 0)


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
    rows = ["| ‏x, עולה | ‏~x, יורד |", "|:-:|:-:|"]
    for x in xs:
        y = ~x & mask
        rows.append(f"| {RLM}`{x:0{w}b}` ({x}) | {RLM}`{y:0{w}b}` ({y}) |")
    return "\n".join(rows)


def prev_rows(x, w):
    mask = (1 << w) - 1
    y = brute_next(~x & mask, w)
    return [("x", x, set()), ("~x", ~x & mask, set()), ("next(~x)", y, set()), ("~next(~x)", ~y & mask, set())]


def zeros_table(z, lengths):
    """The numbers with z zeros, by length: within a length they are the numbers with as
    many ones, and the next length starts with 1 0..0 1..1."""
    rows = ["| האורך | המספרים עם שלושה אפסים, לפי הסדר |", "|:-:|:-:|"]
    for L in lengths:
        xs = [y for y in range(1 << (L - 1), 1 << L) if zeros(y) == z]
        rows.append(f"| {RLM}{L} | " + ", ".join(f"{RLM}`{y:b}` ({y})" for y in xs) + " |")
    return "\n".join(rows)


def next0_rows(x):
    """The rows of the next number with as many zeros when the length runs out."""
    L, z = x.bit_length(), zeros(x)
    rows, nxt = gosper(x, L)
    if nxt:
        return rows + [], nxt
    y = (1 << L) + (1 << (L - z)) - 1
    return rows + [("1 0…0 1…1", y, {L} | set(range(L - z)))], y


def blocks():
    """The generated blocks, in page order."""
    rows, _ = gosper(X_A, W_A)
    return [bits_table(rows, W_A, "השלבים של הנוסחה על 92 ב-8 ביטים"), legend(), complement_table(W_C, K_C),
            bits_table(prev_rows(X_B, W_A), W_A, "הקודם של 99 דרך המשלים"), zeros_table(3, [4, 5, 6]),
            bits_table(next0_rows(X_C)[0], X_C.bit_length() + 1, "הבא אחרי 120 עם שלושה אפסים")]


if __name__ == "__main__":
    print(brute_next(X_A, W_A), brute_prev(X_B, W_A), brute_prev(96, 8), brute_next0(X_C), brute_prev0(143))
    print("\n\n".join(blocks()))
