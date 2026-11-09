#!/usr/bin/env python3
"""Figures and tables of question 0077 (f(1) = 1, f(3) = 3, f(2n) = f(n),
f(4n+1) = 2f(2n+1) - f(n), f(4n+3) = 3f(2n+1) - 2f(n): f reverses the binary digits).

    python tools/figures/fill.py 77        # put the blocks on the page

blocks() returns them in page order: for part a the table that computes f(2027) by the
rules alone, from the bottom up; for part b the table of n and f(n) up to 16 in decimal
and binary, and the bit cells of 2027 and 1727 with a line from every bit to its mirrored
place, and its legend; for part c the table of the binary palindromes by length.
tests/0077 checks that the page copies match and recomputes every value.
"""

import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401


@lru_cache(maxsize=None)
def f(n: int) -> int:
    """f by the five rules of the question, nothing else."""
    if n in (1, 3):
        return n
    if n % 2 == 0:
        return f(n // 2)
    m = n // 4
    return 2 * f(2 * m + 1) - f(m) if n % 4 == 1 else 3 * f(2 * m + 1) - 2 * f(m)


def rev(n: int) -> int:
    """R(n): the binary digits of n in the opposite order (part b)."""
    return int(bin(n)[:1:-1], 2)


def needed(n: int) -> list[int]:
    """Every value the rules need on the way to f(n), each once, smallest first."""
    out: set[int] = set()

    def walk(k: int) -> None:
        if k in out:
            return
        out.add(k)
        if k in (1, 3):
            return
        if k % 2 == 0:
            walk(k // 2)
        else:
            walk(2 * (k // 4) + 1)
            walk(k // 4)

    walk(n)
    return sorted(out)


def rule_row(k: int) -> tuple[str, str]:
    """(the rule that applies to k, the computation with the values), as page text."""
    if k in (1, 3):
        return "נתון", f"‏\\( f({k}) = {k} \\)"
    if k % 2 == 0:
        return f"‏\\( 2 \\cdot {k // 2} \\)", f"‏\\( f({k // 2}) = {f(k)} \\)"
    m = k // 4
    if k % 4 == 1:
        return (f"‏\\( 4 \\cdot {m} + 1 \\)",
                f"‏\\( 2 \\cdot {f(2 * m + 1)} - {f(m)} = {f(k)} \\)")
    return (f"‏\\( 4 \\cdot {m} + 3 \\)",
            f"‏\\( 3 \\cdot {f(2 * m + 1)} - 2 \\cdot {f(m)} = {f(k)} \\)")


PICK = 2027


def rules_table() -> str:
    """Part a: the values the rules need for f(2027), from the bottom up."""
    lines = ["| ‏\\( n \\) | בבינארי | הכלל | החישוב | ‏\\( f(n) \\) |", "|---|---|---|---|---|"]
    for k in needed(PICK):
        rule, calc = rule_row(k)
        lines.append(f'| {k} | <span dir="ltr">{bin(k)[2:]}</span> | {rule} | {calc} | {f(k)} |')
    return "\n".join(lines)


TABLE_TOP = 16


def small_table() -> str:
    """Part b: n and f(n) up to 16, in decimal and in binary."""
    lines = ["| ‏\\( n \\) | ‏\\( n \\) בבינארי | ‏\\( f(n) \\) | ‏\\( f(n) \\) בבינארי |", "|---|---|---|---|"]
    for n in range(1, TABLE_TOP + 1):
        lines.append(f'| {n} | <span dir="ltr">{bin(n)[2:]}</span> | {f(n)} | <span dir="ltr">{bin(f(n))[2:]}</span> |')
    return "\n".join(lines)


def mirror() -> str:
    """Part b: the bits of 2027 above, of 1727 below, a line from every bit to its place."""
    top, bot = bin(PICK)[2:], bin(rev(PICK))[2:]
    L = len(top)
    assert len(bot) == L                       # 2027 is odd: no leading zero to drop
    cw, gap, x0, y1, y2, ch = 40, 6, 12, 40, 160, 40
    w = 2 * x0 + L * (cw + gap) - gap
    h = y2 + ch + 36
    s = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:32rem" role="img" '
         f'aria-label="סעיף ב : הביטים של {PICK} למעלה והביטים של {rev(PICK)} למטה. קו יוצא מכל ביט '
         f'של {PICK} אל המקום המשתקף שלו : הביט הנמוך הופך לעליון, והעליון לנמוך">']
    cx = lambda c: x0 + c * (cw + gap) + cw / 2  # noqa: E731
    for c in range(L):
        bit = top[c]
        cls = "s1-line" if bit == "1" else "ink-line"
        width = 2.5 if bit == "1" else 1.4
        s.append(f'<line class="{cls}" x1="{cx(c):.1f}" y1="{y1 + ch + 4}" x2="{cx(L - 1 - c):.1f}" y2="{y2 - 4}" '
                 f'stroke-width="{width}"/>')
    for row, (y, bits) in enumerate([(y1, top), (y2, bot)]):
        for c, bit in enumerate(bits):
            x = x0 + c * (cw + gap)
            s.append(f'<rect class="lf-cell{" is-one" if bit == "1" else ""}" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="5"/>')
            s.append(f'<text class="lf-cellv" x="{x + cw / 2:.1f}" y="{y + ch / 2 + 7:.1f}" text-anchor="middle">{bit}</text>')
        label = f"n = {PICK}" if row == 0 else f"f(n) = {rev(PICK)}"
        ly = y - 12 if row == 0 else y + ch + 28
        s.append(f'<text class="legend" x="{w / 2:.1f}" y="{ly}" text-anchor="middle" style="font-size:20px">{label}</text>')
    return "".join(s) + "</svg>"


def mirror_legend() -> str:
    return ('<span class="viz-legend"><span><i class="gs-key-one"></i>ביט 1</span>'
            '<span><i class="s1"></i>הדרך של ביט 1 אל המקום המשתקף</span>'
            '<span><i class="ink"></i>הדרך של ביט 0</span></span>')


PAL_TOP = 11


def palindromes(L: int) -> int:
    """Binary palindromes of length L: the first bit is 1, the first half sets the rest."""
    return 2 ** ((L + 1) // 2 - 1)


def pal_table() -> str:
    """Part c: palindromes by length, and their running total."""
    lines = ["| אורך \\( L \\) | המספרים | פלינדרומים | סך הכול עד האורך הזה |", "|---|---|---|---|"]
    total = 0
    for L in range(1, PAL_TOP + 1):
        total += palindromes(L)
        lines.append(f'| {L} | <span dir="ltr">{2 ** (L - 1)}–{2 ** L - 1}</span> | {palindromes(L)} | {total} |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [rules_table(), small_table(), mirror(), mirror_legend(), pal_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
