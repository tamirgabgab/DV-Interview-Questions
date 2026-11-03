#!/usr/bin/env python3
"""Figures and tables of question 0078 (rand7 from rand5, and randN from any randM).

    python tools/figures/fill.py 78        # put the blocks on the page

blocks() returns them in page order: for part a the 5 x 5 table of the two calls (each
cell with its v = 5(a - 1) + b and its output, the 21 accepted cells tinted by the output,
three cells each, the four rejected ones dashed) and its legend; for part b the table of
examples (M, N, the fewest calls k, M^k, L, the rejected values, the expected calls) and
the table of rand5 from rand2 by k (the fewest k is not the cheapest); for part c the table
of when an exact algorithm with a bounded number of calls exists. tests/0078 checks that the
page copies match and recomputes every value.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401


def calls_needed(m: int, n: int) -> int:
    """The fewest calls k with m**k >= n."""
    k, size = 1, m
    while size < n:
        k, size = k + 1, size * m
    return k


def limit(m: int, n: int, k: int) -> int:
    """L: the largest multiple of n not above m**k (the accepted values are 0 .. L - 1)."""
    size = m ** k
    return size - size % n


def expected(m: int, n: int, k: int = 0) -> Fraction:
    """The expected number of calls: k calls a round, m**k / L rounds."""
    k = k or calls_needed(m, n)
    return Fraction(k * m ** k, limit(m, n, k))


def prime_factors(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def exact_calls(m: int, n: int) -> int:
    """The fewest k with n | m**k, or 0 when there is none (a prime of n does not divide m)."""
    if any(m % p for p in prime_factors(n)):
        return 0
    k = 1
    while m ** k % n:
        k += 1
    return k


def dec(x: Fraction) -> str:
    return f"{float(x):.2f}"


def frac(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def both(x: Fraction) -> str:
    """A fraction and its decimal, or a whole number alone."""
    return frac(x) if x.denominator == 1 else f"{frac(x)} ≈ {dec(x)}"


# ---------------------------------------------------------------- part a: the 5 x 5 table

def out7(v: int) -> int:
    """The output of a 1-based v = 5(a - 1) + b, 1..21; 0 for a rejected v."""
    return (v - 1) % 7 + 1 if v <= 21 else 0


def grid() -> str:
    """Part a: rows a (the first call), columns b (the second); a cell shows v and the output."""
    s = ['<table class="rn-grid rn-fig" dir="ltr" aria-label="סעיף א : טבלה של 5 על 5. השורה היא הקריאה '
         'הראשונה a והעמודה היא השנייה b. בכל תא v = 5(a − 1) + b והפלט. 21 התאים הראשונים צבועים לפי '
         'הפלט, שלושה תאים לכל פלט מ-1 עד 7, וארבעת התאים 22 עד 25 נדחים">']
    s.append('<thead><tr><th class="rn-corner">a \\ b</th>' + "".join(f"<th>{b}</th>" for b in range(1, 6)) + "</tr></thead><tbody>")
    for a in range(1, 6):
        row = f"<tr><th>{a}</th>"
        for b in range(1, 6):
            v = 5 * (a - 1) + b
            r = out7(v)
            cls = f"rn-t{r}" if r else "rn-rej"
            row += f'<td class="rn-c {cls}"><span class="rn-v">{v}</span><b>{r if r else "✗"}</b></td>'
        s.append(row + "</tr>")
    return "".join(s) + "</tbody></table>"


def grid_legend() -> str:
    keys = "".join(f'<span><i class="rn-key-t{r}"></i>פלט {r}</span>' for r in range(1, 8))
    return f'<span class="viz-legend">{keys}<span><i class="rn-key-rej"></i>נדחה, מגרילים שוב</span></span>'


# ---------------------------------------------------------------- part b: examples

EXAMPLES = [(5, 7), (7, 10), (2, 3), (2, 6), (7, 5), (6, 8), (20, 10)]


def examples_table() -> str:
    lines = ["| המקור \\( M \\) | היעד \\( N \\) | קריאות בסבב \\( k \\) | ‏\\( M^k \\) | ‏\\( L \\) | נדחים | תוחלת הקריאות |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for m, n in EXAMPLES:
        k = calls_needed(m, n)
        e = expected(m, n, k)
        lines.append(f'| {m} | {n} | {k} | {m ** k} | {limit(m, n, k)} | {m ** k - limit(m, n, k)} | '
                     f'<span dir="ltr">{both(e)}</span> |')
    return "\n".join(lines)


BY_K = (2, 5, range(3, 7))


def by_k_table() -> str:
    """rand5 from rand2 with k = 3 .. 6 calls a round: k = 4 is the cheapest."""
    m, n, ks = BY_K
    best = min(ks, key=lambda k: expected(m, n, k))
    lines = ["| קריאות בסבב \\( k \\) | ‏\\( 2^k \\) | ‏\\( L \\) | הסיכוי לקבל | תוחלת הקריאות |",
             "|:-:|:-:|:-:|:-:|:-:|"]
    for k in ks:
        e = expected(m, n, k)
        cell = f'<span dir="ltr">{both(e)}</span>'
        lines.append(f'| {k} | {m ** k} | {limit(m, n, k)} | <span dir="ltr">{limit(m, n, k)}/{m ** k}</span> | '
                     + (f"**{cell}**" if k == best else cell) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- part c: bounded

BOUNDED = [(2, 4), (20, 10), (10, 4), (6, 9), (6, 8), (2, 6), (4, 6), (5, 7)]


def bounded_table() -> str:
    lines = ["| המקור \\( M \\) | היעד \\( N \\) | הגורמים הראשוניים של \\( N \\) | מספר הקריאות המדויק | למה |",
             "|:-:|:-:|:-:|:-:|:-:|"]
    for m, n in BOUNDED:
        k = exact_calls(m, n)
        ps = ", ".join(str(p) for p in prime_factors(n))
        if k:
            got, why = str(k), f"‏\\( {m}^{k} = {m ** k} = {m ** k // n} \\cdot {n} \\)"
        else:
            bad = [p for p in prime_factors(n) if m % p]
            got, why = "אין", f"{bad[0]} לא מחלק את {m}"
        lines.append(f'| {m} | {n} | <span dir="ltr">{ps}</span> | {got} | {why} |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [grid(), grid_legend(), examples_table(), by_k_table(), bounded_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
