#!/usr/bin/env python3
"""Figures and tables of question 0058 (the tags that did not come back: one missing by
XOR, two missing by a split on a bit, one missing and one duplicated by sums, k missing
by power sums).

    python tools/figures/fill.py 58        # put the blocks on the page

The reference here is independent of the page code: the missing and duplicated tags are
found by counting (a multiset difference), and the accumulators are written from their
definitions. blocks() returns, in page order: the running XOR of part a's example, the
split table of part b, the sums of part c, and the memory of each method for 8-bit tags.
tests/0058 checks the page code against these.
"""

from collections import Counter

RLM = "‏"

# part a: tags 0..7, tag 4 never comes back
A_SENT = list(range(8))
A_RET = [3, 0, 6, 1, 7, 2, 5]
# part b: tags 0..15, tags 5 and 12 never come back
B_N, B_W, B_MISS = 16, 4, (5, 12)
# part c: tags 0..9, tag 7 missing and tag 3 twice
C_N, C_MISS, C_DUP = 10, 7, 3


def truth(sent, returned):
    """(the tags missing, the tags returned too often), by counting."""
    c = Counter(sent)
    c.subtract(returned)
    return sorted(t for t, v in c.items() if v > 0), sorted(t for t, v in c.items() if v < 0)


def accumulators(sent, returned, width):
    """The checker's registers: the XOR of all, the XOR per bit, the sum and the sum of
    squares of sent minus returned, and the count still out."""
    x, part = 0, [0] * width
    for t in sent + returned:
        x ^= t
        for j in range(width):
            if t >> j & 1:
                part[j] ^= t
    s = sum(sent) - sum(returned)
    q = sum(t * t for t in sent) - sum(t * t for t in returned)
    return x, part, s, q, len(sent) - len(returned)


def bits(v, w):
    return format(v, f"0{w}b")


# --- blocks ------------------------------------------------------------------------------

def xor_table():
    rows = ["| הצעד | ה-tag | בבינארי | ה-XOR עד עכשיו |", "|:-:|:-:|:-:|:-:|"]
    acc = 0
    for t in A_SENT:
        acc ^= t
    rows.append(f"| נשלחו 0 עד 7 | | | {RLM}`{bits(acc, 3)}` = {RLM}{acc} |")
    for k, t in enumerate(A_RET, 1):
        acc ^= t
        rows.append(f"| {RLM}{k} | {RLM}{t} | {RLM}`{bits(t, 3)}` | {RLM}`{bits(acc, 3)}` = {RLM}{acc} |")
    return "\n".join(rows)


def split_table():
    sent = list(range(B_N))
    ret = [t for t in sent if t not in B_MISS]
    x, part, _, _, _ = accumulators(sent, ret, B_W)
    rows = ["| הביט j | ה-tags החסרים שהביט j שלהם 1 | ‏`part[j]` | ‏`x` בביט j |", "|:-:|:-:|:-:|:-:|"]
    for j in range(B_W):
        has = [t for t in B_MISS if t >> j & 1]
        rows.append(f"| {RLM}{j} | {RLM}{', '.join(map(str, has)) or '—'} | {RLM}`{bits(part[j], B_W)}` = {RLM}{part[j]} | {RLM}{x >> j & 1} |")
    return "\n".join(rows)


def sums_table():
    sent = list(range(C_N))
    ret = [t for t in sent if t != C_MISS] + [C_DUP]
    _, _, s, q, out = accumulators(sent, ret, 4)
    rows = ["| המצבר | נשלחו | חזרו | ההפרש | מה זה |", "|:-:|:-:|:-:|:-:|---|"]
    rows.append(f"| ‏`s` : סכום | {RLM}{sum(sent)} | {RLM}{sum(ret)} | {RLM}{s} | ‏\\( a - d \\) |")
    rows.append(f"| ‏`q` : סכום ריבועים | {RLM}{sum(t * t for t in sent)} | {RLM}{sum(t * t for t in ret)} | {RLM}{q} | ‏\\( a^2 - d^2 \\) |")
    rows.append(f"| ‏XOR | | | {RLM}{C_MISS ^ C_DUP} | ‏\\( a \\oplus d \\), כמו שני חסרים |")
    rows.append(f"| מונה | {RLM}{len(sent)} | {RLM}{len(ret)} | {RLM}{out} | אף אחד לא \"בחוץ\" |")
    return "\n".join(rows)


def final_bits(width=8):
    """The width each register needs for its final value, for tags of `width` bits (n =
    2^width of them). A running sum may wrap: adding and subtracting modulo 2^b is exact
    modulo 2^b, so only the value at the end must fit. s = a - d and q = a^2 - d^2 of part c
    can be negative (a sign bit); the power sums p_i of at most k missing tags are at most
    k (n - 1)^i."""
    top = (1 << width) - 1
    signed = lambda m: m.bit_length() + 1                 # -m .. m in two's complement
    return {
        "sums": [signed(top), signed(top * top)],
        **{k: [(k * top ** i).bit_length() for i in range(1, k + 1)] for k in (2, 3, 4)},
    }


def memory_table(width=8):
    """Bits of each method for tags of `width` bits, the counter not counted: the final
    value of each register (final_bits), the parts in an LTR span that does not wrap."""
    n = 1 << width
    fb = final_bits(width)
    total = lambda ws: f'{RLM}{sum(ws)} (<span dir="ltr">{"\u00a0+\u00a0".join(map(str, ws))}</span>)'
    rows = ["| השיטה | מה היא מוצאת | הרגיסטרים | ביטים ל-tags של 8 ביטים |", "|---|---|---|:-:|"]
    rows.append(f"| ‏XOR | חסר אחד | ‏`x` | {RLM}{width} |")
    rows.append(f"| ‏XOR לפי ביט | שני חסרים | ‏`x` ו-`part[0..W-1]` | {RLM}{width + width * width} |")
    rows.append(f"| סכום וסכום ריבועים | חסר אחד וכפול אחד | ‏`s` ו-`q`, עם סימן | {total(fb['sums'])} |")
    for k in (2, 3, 4):
        rows.append(f"| סכומי חזקות עד {k} | עד {k} חסרים | ‏\\( p_1, \\dots, p_{{{k}}} \\) | {total(fb[k])} |")
    rows.append(f"| טבלה של ביט לכל tag | הכול | ‏{n} ביטים | {RLM}{n} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [xor_table(), split_table(), sums_table(), memory_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
