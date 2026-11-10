#!/usr/bin/env python3
"""Figures and tables of question 0060 (the next number with as many ones: Gosper's step,
the previous one through the complement, and the same for zeros, counted without the
leading ones, where the length of the number may change), the one-cycle datapath and
the enumerator of every k of n.

    python tools/figures/fill.py 60        # put the blocks on the page

The reference here is independent of the page code: brute_next / brute_prev and
brute_next0 / brute_prev0 search number by number. gosper() gives the rows of the
formula, the same rows the box draws. blocks() returns, in page order: the steps of
next(92) in 8 bits, their legend, the block diagram of the one-cycle next_same and its
legend, the numbers with two ones in 5 bits next to their complements, the steps of
prev(99), the numbers with three zeros by length, the rows of the next number after 120
with three zeros (a longer one), and the enumerator of every 3 of 5, a row per clock.
"""

from html import escape

RLM = "‏"
NB = "\u00a0"
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


# The one-cycle next_same (part a's cost, follow-up 2): three stages in series, each of
# depth log w: the lowest one (-x is a carry chain), the adder, the barrel shifter. Drawn
# left to right. (id, x, y, w, h, stage 0-3, title, second line)
HW_W, HW_H = 560, 228
HW_BLOCKS = (
    ("iso", 38, 20, 100, 46, 1, "x & −x", ""),
    ("enc", 176, 20, 124, 46, 0, "one-hot→t", ""),
    ("add", 176, 96, 100, 58, 2, "+", "w+1 bits"),
    ("xor", 296, 166, 56, 46, 0, "XOR", ""),
    ("shf", 392, 160, 96, 58, 3, ">> t+2", "barrel"),
    ("or", 504, 96, 44, 58, 0, "OR", ""),
)
# (points, arrow at the end, label, label x, label y, anchor)
HW_WIRES = (
    (((6, 110), (176, 110)), True, "x", 6, 102, "start"),
    (((20, 43), (20, 200)), False, "", 0, 0, ""),
    (((20, 43), (38, 43)), True, "", 0, 0, ""),
    (((20, 200), (296, 200)), True, "", 0, 0, ""),
    (((138, 43), (176, 43)), True, "c", 157, 35, "middle"),
    (((157, 43), (157, 140), (176, 140)), True, "", 0, 0, ""),
    (((300, 43), (440, 43), (440, 160)), True, "t", 370, 35, "middle"),
    (((250, 96), (250, 72)), True, "none", 258, 88, "start"),
    (((276, 125), (504, 125)), True, "r", 330, 117, "middle"),
    (((284, 125), (284, 178), (296, 178)), True, "", 0, 0, ""),
    (((352, 189), (392, 189)), True, "x^r", 372, 181, "middle"),
    (((488, 189), (496, 189), (496, 145), (504, 145)), True, "s", 496, 214, "middle"),
    (((526, 96), (526, 64)), True, "next", 526, 56, "middle"),
)
HW_DOTS = ((20, 110), (157, 43), (284, 125))


def hw_diagram():
    """The block diagram of the one-cycle next_same, with no divider: s = (x ^ r) >> (t + 2)."""
    label = ("תרשים המלבנים של next_same במחזור אחד" + NB + ": x & −x מבודד את האחד הנמוך c, ‏encoder של one-hot "
             "נותן ממנו את t, המחבר נותן r = x + c ואת ה-carry העליון none, ‏XOR של x ו-r נותן את הבלוק והביט "
             "החדש, ‏barrel shifter מזיז אותו ב-t + 2, ו-OR עם r נותן את next. שלושה שלבים בטור" + NB + ": "
             "הבידוד, החיבור וההזזה")
    o = [f'<svg class="figure pn-dp" viewBox="0 0 {HW_W} {HW_H}" direction="ltr" style="max-width:{HW_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="pn-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="pn-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for _id, x, y, w, h, stage, title, sub in HW_BLOCKS:
        ty = y + h / 2 + (-3 if sub else 5)
        cls = f" pn-st{stage}" if stage else ""
        o.append(f'<g class="pn-blk{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{escape(title)}</text>'
                 + (f'<text class="pn-sub" x="{x + w / 2:g}" y="{y + h / 2 + 13:g}" text-anchor="middle">{escape(sub)}</text>' if sub else "")
                 + "</g>")
    for pts, arrow, lab, lx, ly, anchor in HW_WIRES:
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        head = ' marker-end="url(#pn-hb)"' if arrow else ""
        o.append(f'<path class="pn-wire" d="{d}"{head}/>')
        if lab:
            o.append(f'<text class="pn-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    o += [f'<circle class="pn-dot" cx="{x}" cy="{y}" r="3.5"/>' for x, y in HW_DOTS]
    return "".join(o) + "</svg>"


def hw_legend():
    return ('<span class="viz-legend"><span><i class="pn-key-1"></i>שלב 1' + NB + ': בידוד האחד הנמוך</span>'
            '<span><i class="pn-key-2"></i>שלב 2' + NB + ': החיבור</span>'
            '<span><i class="pn-key-3"></i>שלב 3' + NB + ': ההזזה</span>'
            '<span><i class="pn-key-0"></i>שער אחד בעומק, או במקביל לחיבור</span></span>')


def enumerate_rows(n, k):
    """Every k of n, a mask per clock: (mask, c, r, next); next is 0 after the last one."""
    rows, y = [], (1 << k) - 1
    while y:
        c = y & -y
        r = y + c
        nxt = brute_next(y, n)
        rows.append((y, c, r, nxt))
        y = nxt
    return rows


def enum_table(n, k):
    """The enumerator of follow-up 1 as a table, a row per clock."""
    out = [f"| מחזור | {RLM}mask | {RLM}c | {RLM}r | {RLM}next | {RLM}none |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i, (y, c, r, nxt) in enumerate(enumerate_rows(n, k)):
        out.append(f"| {RLM}{i} | {RLM}{y:0{n}b} | {RLM}{c:0{n}b} | {RLM}{r:0{n + 1}b} | {RLM}{nxt:0{n}b} | {RLM}{int(nxt == 0)} |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    rows, _ = gosper(X_A, W_A)
    return [bits_table(rows, W_A, "השלבים של הנוסחה על 92 ב-8 ביטים"), legend(), hw_diagram(), hw_legend(),
            complement_table(W_C, K_C),
            bits_table(prev_rows(X_B, W_A), W_A, "הקודם של 99 דרך המשלים"), zeros_table(3, [4, 5, 6]),
            bits_table(next0_rows(X_C)[0], X_C.bit_length() + 1, "הבא אחרי 120 עם שלושה אפסים"),
            enum_table(5, 3)]


if __name__ == "__main__":
    print(brute_next(X_A, W_A), brute_prev(X_B, W_A), brute_prev(96, 8), brute_next0(X_C), brute_prev0(143))
    print("\n\n".join(blocks()))
