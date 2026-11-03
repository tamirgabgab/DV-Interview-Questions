#!/usr/bin/env python3
"""Figures and tables of question 0079 (biased coins: a fair bit from a coin of unknown
bias, a coin of any p from a fair coin, and a fair die from a biased coin).

    python tools/figures/fill.py 79        # put the blocks on the page

blocks() returns them in page order: for part a the 2 x 2 grid of a pair of flips with the
probability of each cell (the two mixed cells equal, the two equal cells thrown away) and
its legend, and the table of the expected flips for a few p; for part b the bits of
p = 1/3 against the fair flips of an example, the first difference marked, its legend, and
the table of the flips for a few p; for part c the table of the eight values of three fair
bits and the table of the flips per die roll. tests/0079 checks that the page copies match
and recomputes every value with fractions.
"""

from __future__ import annotations

from fractions import Fraction as Fr

# --- the numbers -----------------------------------------------------------------------------


def vn_flips(p: Fr) -> Fr:
    """Part a: the expected flips of the biased coin per fair bit (pairs until they differ)."""
    return 1 / (p * (1 - p))


def die_flips(p: Fr) -> Fr:
    """Part c: the expected flips of the biased coin per die roll: 8/6 rounds of three fair bits."""
    return 3 * Fr(8, 6) * vn_flips(p)


def digits(p: Fr, k: int) -> str:
    """The first k binary digits of p in (0, 1), the finite expansion for a dyadic p."""
    out = []
    for _ in range(k):
        p *= 2
        d = int(p >= 1)
        p -= d
        out.append(str(d))
    return "".join(out)


def dyadic_len(p: Fr) -> int | None:
    """k when p = a / 2^k with a odd (k binary digits), None when p is not dyadic."""
    d = p.denominator
    return d.bit_length() - 1 if d & (d - 1) == 0 else None


def cmp_flips(p: Fr) -> Fr:
    """Part b: the expected fair flips until the comparison decides: one flip, then one more
    with probability 1/2 each time, until the digits of p run out (2 - 2^(1-k) for a dyadic
    p of k digits, 2 for every other p)."""
    k = dyadic_len(p)
    return Fr(2) if k is None else 2 - Fr(2) ** (1 - k)


def fmt(x: Fr) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x: Fr, places: int = 2) -> str:
    """A decimal with at most `places` places, trailing zeros dropped."""
    s = f"{float(x):.{places}f}".rstrip("0").rstrip(".")
    return s


# --- part a ----------------------------------------------------------------------------------

P_ROWS = [Fr(1, 2), Fr(1, 3), Fr(1, 4), Fr(1, 10)]


def pair_grid() -> str:
    """The four outcomes of a pair of flips, the first flip by row and the second by column."""
    x0, y0, cw, ch, gap = 64, 44, 150, 84, 8
    w, h = x0 + 2 * cw + gap + 12, y0 + 2 * ch + gap + 12
    cells = {("H", "H"): ("p²", "↺", "is-again"), ("H", "T"): ("p(1−p)", "1", "is-one"),
             ("T", "H"): ("(1−p)p", "0", "is-zero"), ("T", "T"): ("(1−p)²", "↺", "is-again")}
    s = [f'<svg class="figure bc-grid" viewBox="0 0 {w} {h}" style="max-width:24rem" role="img" '
         f'aria-label="סעיף א : ארבע התוצאות של זוג הטלות. עץ ואחריו פלי, בהסתברות p(1−p), נותן 1. '
         f'פלי ואחריו עץ, באותה הסתברות, נותן 0. שני עץ או שני פלי נזרקים, ומטילים זוג חדש">']
    for c, second in enumerate("HT"):
        s.append(f'<text class="bc-head" x="{x0 + c * (cw + gap) + cw / 2:.1f}" y="{y0 - 14}" text-anchor="middle">{second}</text>')
    for r, first in enumerate("HT"):
        y = y0 + r * (ch + gap)
        s.append(f'<text class="bc-head" x="{x0 - 22}" y="{y + ch / 2 + 7:.1f}" text-anchor="middle">{first}</text>')
        for c, second in enumerate("HT"):
            x = x0 + c * (cw + gap)
            prob, out, cls = cells[(first, second)]
            s.append(f'<rect class="bc-cell {cls}" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6"/>')
            s.append(f'<text class="bc-prob" x="{x + cw / 2:.1f}" y="{y + 34}" text-anchor="middle">{first}{second} : {prob}</text>')
            s.append(f'<text class="bc-out" x="{x + cw / 2:.1f}" y="{y + 66}" text-anchor="middle">→ {out}</text>')
    return "".join(s) + "</svg>"


def pair_legend() -> str:
    return ('<span class="viz-legend"><span><i class="bc-key-one"></i>‏HT : הביט 1</span>'
            '<span><i class="bc-key-zero"></i>‏TH : הביט 0</span>'
            '<span><i class="bc-key-again"></i>‏HH או TT : זוג חדש (↺)</span>'
            '<span>שורה : ההטלה הראשונה, עמודה : השנייה</span></span>')


def table_a() -> str:
    lines = ["| ‏\\( p \\) | זוג שונה : ‏\\( 2p(1-p) \\) | הטלות לביט : ‏\\( \\frac{1}{p(1-p)} \\) | ביטים מ-100 הטלות |",
             "|:-:|:-:|:-:|:-:|"]
    for p in P_ROWS:
        e = vn_flips(p)
        e_txt = fmt(e) if e.denominator == 1 else f'<span dir="ltr">{fmt(e)} ≈ {dec(e)}</span>'
        lines.append(f"| ‏{fmt(p)} | ‏{fmt(2 * p * (1 - p))} | ‏{e_txt} | ‏{dec(100 / e, 2)} |")
    return "\n".join(lines)


# --- part b ----------------------------------------------------------------------------------

EX_P = Fr(1, 3)
EX_FLIPS = "0100"            # the example: equal three times, then U has 0 where p has 1
SHOW = 8


def compare() -> str:
    """The digits of p = 1/3 above the fair flips of the example; the first difference marked."""
    pd = digits(EX_P, SHOW)
    stop = next(i for i, (a, b) in enumerate(zip(pd, EX_FLIPS)) if a != b)
    assert stop == len(EX_FLIPS) - 1
    lx, x0, cw, gap, ch, y1, y2 = 118, 130, 40, 6, 40, 20, 84
    w = x0 + SHOW * (cw + gap) + 40
    h = y2 + ch + 16
    s = [f'<svg class="figure bc-cmp" viewBox="0 0 {w} {h}" style="max-width:34rem" role="img" '
         f'aria-label="סעיף ב : הספרות הבינאריות של p = 1/3 בשורה העליונה, וההטלות ההוגנות 0, 1, 0, 0 '
         f'בשורה התחתונה. שלוש הראשונות שוות. ברביעית ל-p יש 1 ולהטלה 0, ולכן U קטן מ-p והתוצאה 1">']
    for row, (y, bits, label) in enumerate([(y1, pd, "p = 0."), (y2, EX_FLIPS, "U = 0.")]):
        s.append(f'<text class="bc-head" x="{lx}" y="{y + ch / 2 + 7:.1f}" text-anchor="end">{label}</text>')
        for c in range(SHOW):
            x = x0 + c * (cw + gap)
            if c >= len(bits):
                s.append(f'<rect class="bc-bit is-later" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="5"/>')
                continue
            bit = bits[c]
            cls = " is-same" if c < stop else (" is-stop" if c == stop else "")
            s.append(f'<rect class="bc-bit{cls}" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="5"/>')
            s.append(f'<text class="bc-bitv" x="{x + cw / 2:.1f}" y="{y + ch / 2 + 7:.1f}" text-anchor="middle">{bit}</text>')
        s.append(f'<text class="bc-head" x="{x0 + SHOW * (cw + gap) + 4}" y="{y + ch / 2 + 7:.1f}">…</text>')
    return "".join(s) + "</svg>"


def compare_legend() -> str:
    return ('<span class="viz-legend"><span><i class="bc-key-same"></i>ההטלה שווה לספרה של p : ממשיכים</span>'
            '<span><i class="bc-key-stop"></i>ההבדל הראשון : מחליטים</span>'
            '<span><i class="bc-key-later"></i>הטלה שלא צריך</span></span>')


B_ROWS = [Fr(1, 2), Fr(3, 4), Fr(5, 8), Fr(1, 3), Fr(2, 5)]


def table_b() -> str:
    lines = ["| ‏\\( p \\) | בבינארי | הטלות לכל היותר | תוחלת ההטלות |", "|:-:|:-:|:-:|:-:|"]
    for p in B_ROWS:
        k = dyadic_len(p)
        expansion = f"0.{digits(p, k)}" if k else f"0.{digits(p, SHOW)}…"
        most = f"‏{k}" if k else "אין חסם"
        lines.append(f'| ‏{fmt(p)} | <span dir="ltr">{expansion}</span> | {most} | ‏{fmt(cmp_flips(p))} |')
    return "\n".join(lines)


# --- part c ----------------------------------------------------------------------------------


def table_c() -> str:
    lines = ["| שלושה ביטים הוגנים | הערך | התוצאה |", "|:-:|:-:|:-:|"]
    for v in range(8):
        face = f"‏{v + 1}" if v < 6 else "שוב, ביטים חדשים"
        lines.append(f'| <span dir="ltr">{v:03b}</span> | ‏{v} | {face} |')
    return "\n".join(lines)


def table_c_flips() -> str:
    lines = ["| ‏\\( p \\) | ביטים הוגנים להטלת קובייה | הטלות של המטבע המוטה |", "|:-:|:-:|:-:|"]
    for p in P_ROWS:
        e = die_flips(p)
        e_txt = fmt(e) if e.denominator == 1 else f'<span dir="ltr">{fmt(e)} ≈ {dec(e, 1)}</span>'
        lines.append(f"| ‏{fmt(p)} | ‏4 | ‏{e_txt} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [pair_grid(), pair_legend(), table_a(), compare(), compare_legend(), table_b(),
            table_c(), table_c_flips()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
