#!/usr/bin/env python3
"""Figures and tables of question 0087 (Lights Out: XOR and linear algebra over GF(2)).

    python tools/figures/fill.py 87        # put the blocks on the page

A board of n x n lights; cell (r, c) is bit r*n + c, drawn with row 0 on top and column 0
on the left. A press flips the cell and its neighbours up, down, left and right (with the
diagonals, the eight around it). A lit light is a filled bulb, a light that is off a hollow
one, and a press a blue frame around its cell.

blocks() returns them in page order: the three kinds of press on a 3 x 3 board (the
statement); part a's example (the top row lit, the presses, the board after them) and its
9 x 9 system; part b's table of the boards 3 to 7 (free variables, the share of states that
can be solved), the three quiet patterns of 5 x 5, and the table of light chasing on 5 x 5
(the bottom row left on, the first row to press); part c's quiet line 1 1 0 1 1 and two
quiet patterns of the 5 x 5 board with diagonals, and the table of the boards with
diagonals; part d's polynomials of n = 4 and 5 and the table of the boards 1 to 20 by rank
and by the polynomial gcd. tests/0087 checks that the page copies match and recomputes
every value.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- the reference -------------------------------------------------------------------------


def masks(n: int, diag: bool = False) -> list[int]:
    """masks[k]: the lights a press on cell k flips."""
    out = []
    for r in range(n):
        for c in range(n):
            m = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr and dc and not diag:
                        continue
                    if 0 <= r + dr < n and 0 <= c + dc < n:
                        m |= 1 << ((r + dr) * n + c + dc)
            out.append(m)
    return out


def apply(n: int, lit: int, press: int, diag: bool = False) -> int:
    for k, m in enumerate(masks(n, diag)):
        if press >> k & 1:
            lit ^= m
    return lit


def rref(rows: list[int], nvars: int) -> tuple[list[int], list[int]]:
    """Reduced row echelon form over GF(2) of the rows (variables in bits 0..nvars-1):
    (the rows, the pivot column of each of the first len(pivots) rows)."""
    rows, piv = list(rows), []
    for col in range(nvars):
        r = len(piv)
        p = next((i for i in range(r, len(rows)) if rows[i] >> col & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> col & 1:
                rows[i] ^= rows[r]
        piv.append(col)
    return rows, piv


def rank(n: int, diag: bool = False) -> int:
    return len(rref(masks(n, diag), n * n)[1])


def free(n: int, diag: bool = False) -> int:
    return n * n - rank(n, diag)


def kernel(n: int, diag: bool = False) -> list[int]:
    """Every press set that changes nothing (the kernel), sorted, 0 left out."""
    rows, piv = rref(masks(n, diag), n * n)
    basis = []
    for f in (c for c in range(n * n) if c not in piv):
        v = 1 << f
        for i, c in enumerate(piv):
            if rows[i] >> f & 1:
                v |= 1 << c
        basis.append(v)
    out = {0}
    for b in basis:
        out |= {v ^ b for v in out}
    return sorted(out - {0})


def solve(n: int, lit: int, diag: bool = False) -> int | None:
    """The press set of fewest presses that turns lit off, or None."""
    N = n * n
    rows, piv = rref([m | (lit >> j & 1) << N for j, m in enumerate(masks(n, diag))], N)
    if any(r == 1 << N for r in rows[len(piv):]):
        return None
    x = sum(1 << c for i, c in enumerate(piv) if rows[i] >> N & 1)
    return min([x] + [x ^ k for k in kernel(n, diag)], key=lambda v: (bin(v).count("1"), v))


def chase_rest(n: int, lit: int, first: int) -> int:
    """Light chasing: press first on row 0, then under every light on, row by row; the
    lights left on the bottom row (bit c for column c)."""
    m = masks(n)
    for c in range(n):
        if first >> c & 1:
            lit ^= m[c]
    for r in range(n - 1):
        for c in range(n):
            if lit >> (r * n + c) & 1:
                lit ^= m[(r + 1) * n + c]
    return lit >> (n - 1) * n


def chase_table(n: int) -> dict[int, list[int]]:
    """For every bottom row light chasing can leave: the first rows that clear it,
    fewest presses first."""
    out: dict[int, list[int]] = {}
    for f in range(1 << n):
        out.setdefault(chase_rest(n, 0, f), []).append(f)
    return {k: sorted(v, key=lambda f: (bin(f).count("1"), bits(f, n))) for k, v in out.items()}


def path_poly(n: int) -> int:
    """det(xI + A) over GF(2) for the line of n lights, bit k the coefficient of x^k."""
    a, b = 1, 0b10
    for _ in range(n):
        a, b = b, (b << 1) ^ a
    return a


def shift1(p: int) -> int:
    """p(x + 1) over GF(2)."""
    q = 0
    for k in range(p.bit_length() - 1, -1, -1):
        q = (q << 1) ^ q ^ (p >> k & 1)
    return q


def pgcd(a: int, b: int) -> int:
    while b:
        while a and a.bit_length() >= b.bit_length():
            a ^= b << (a.bit_length() - b.bit_length())
        a, b = b, a
    return a


def gcd_degree(n: int) -> int:
    p = path_poly(n)
    return pgcd(p, shift1(p)).bit_length() - 1


def poly_text(p: int) -> str:
    """x⁴ + x² + 1, highest power first."""
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    terms = []
    for k in range(p.bit_length() - 1, -1, -1):
        if p >> k & 1:
            terms.append("1" if k == 0 else "x" if k == 1 else "x" + str(k).translate(sup))
    return " + ".join(terms) or "0"


def bits(v: int, n: int) -> str:
    """The bits 0..n-1 of v left to right: column 0 first."""
    return "".join(str(v >> c & 1) for c in range(n))


# --- drawing -------------------------------------------------------------------------------

def cells(n: int, v: int) -> list[tuple[int, int]]:
    return [(k // n, k % n) for k in range(n * n) if v >> k & 1]


def board(n: int, x0: float, y0: float, s: int, lit: int, press: int = 0, caption: str = "",
          index: bool = False, now: int = -1) -> str:
    """One board at (x0, y0), cells of side s: the bulbs, the presses, a caption under it."""
    out = []
    for r in range(n):
        for c in range(n):
            k, x, y = r * n + c, x0 + c * s, y0 + r * s
            out.append(f'<rect class="lo-cell" x="{x}" y="{y}" width="{s}" height="{s}"/>')
            if press >> k & 1:
                out.append(f'<rect class="lo-press" x="{x + 3}" y="{y + 3}" width="{s - 6}" height="{s - 6}" rx="4"/>')
            if k == now:
                out.append(f'<rect class="lo-now" x="{x + 3}" y="{y + 3}" width="{s - 6}" height="{s - 6}" rx="4"/>')
            on = lit >> k & 1
            cy, rad = (y + s / 2 + 3, s * 0.22) if index else (y + s / 2, s * 0.27)   # room for the number
            out.append(f'<circle class="{"lo-on" if on else "lo-off"}" cx="{x + s / 2:g}" cy="{cy:g}" r="{rad:.1f}"/>')
            if index:
                out.append(f'<text class="lo-ix" x="{x + 4}" y="{y + 13}">{k}</text>')
    out.append(f'<rect class="lo-frame" x="{x0}" y="{y0}" width="{n * s}" height="{n * s}"/>')
    if caption:
        out.append(f'<text class="lo-cap" x="{x0 + n * s / 2:g}" y="{y0 + n * s + 20}" text-anchor="middle" direction="rtl">{caption}</text>')
    return "".join(out)


def row_of_boards(items: list[dict], n: int, s: int, label: str, gap: int = 26, width: str | None = None,
                  index: bool = False) -> str:
    bw = n * s
    w = len(items) * bw + (len(items) - 1) * gap + 4
    h = bw + (30 if any(i.get("caption") for i in items) else 4) + 2
    style = width or f"{w / 16:.1f}rem"
    out = [f'<svg class="figure lo-fig" viewBox="0 0 {w} {h}" style="max-width:{style}" role="img" aria-label="{label}">']
    for j, it in enumerate(items):                      # the first board on the right, as the page reads
        out.append(board(n, 2 + (len(items) - 1 - j) * (bw + gap), 2, s, it.get("lit", 0), it.get("press", 0), it.get("caption", ""),
                         index=index, now=it.get("now", -1)))
    return "".join(out) + "</svg>"


def legend(*keys: tuple[str, str]) -> str:
    return '<span class="viz-legend">' + "".join(f'<span><i class="{k}"></i>{t}</span>' for k, t in keys) + "</span>"


KEY_ON = ("lo-key-on", "נורה דולקת")
KEY_OFF = ("lo-key-off", "נורה כבויה")
KEY_PRESS = ("lo-key-press", "לחיצה")


def ltr(s: str) -> str:
    return f'<span dir="ltr">{s}</span>'


# --- the statement -------------------------------------------------------------------------

def press_kinds() -> str:
    n = 3
    items = [{"lit": masks(n)[k], "press": 1 << k, "caption": cap} for k, cap in
             [(4, "פנימית : 5 נורות"), (1, "בשפה : 4 נורות"), (0, "בפינה : 3 נורות")]]
    svg = row_of_boards(items, n, 40, gap=34, label=(
        "שלושה לוחות של 3 על 3, על כל אחד לחיצה אחת על לוח כבוי. לחיצה על הנורה האמצעית מדליקה "
        "5 נורות : אותה ואת 4 השכנות שלה. לחיצה על נורה בשפה מדליקה 4, ולחיצה על פינה 3"))
    return svg + "\n\n" + legend(KEY_PRESS, KEY_ON, KEY_OFF)


# --- part a --------------------------------------------------------------------------------

A_N, A_LIT = 3, 0b000000111


def part_a_example() -> str:
    n, lit = A_N, A_LIT
    x = solve(n, lit)
    items = [{"lit": lit, "caption": "ההתחלה"}, {"lit": lit, "press": x, "caption": "הלחיצות"},
             {"lit": apply(n, lit, x), "caption": "אחרי הלחיצות"}]
    on = ", ".join(str(k) for k, _ in enumerate(range(n * n)) if x >> k & 1)
    svg = row_of_boards(items, n, 40, gap=34, index=True, label=(
        f"סעיף א : לוח של 3 על 3 שבו דולקת רק השורה העליונה, הנורות 0, 1 ו-2. הפתרון הוא ארבע "
        f"לחיצות, על הנורות {on} : כל השורה האמצעית והאמצעית שבשורה התחתונה. אחריהן כל הנורות כבויות"))
    return svg + "\n\n" + legend(KEY_PRESS, KEY_ON, ("lo-key-ix", "המספר של הנורה, ‏r·3 + c"))


def part_a_system() -> str:
    """The 9 x 9 system: row j is light j, column i is press x_i, then the right side."""
    n, lit = A_N, A_LIT
    N, m = n * n, masks(n)
    x = solve(n, lit)
    head = "".join(f"<th>x{i}</th>" for i in range(N))
    t = [f'<div class="gs-scroll" tabindex="0" role="region" aria-label="סעיף א : מערכת המשוואות של הלוח 3 על 3">'
         f'<table class="gs-bits lo-sys" dir="ltr" aria-label="סעיף א : מערכת 9 על 9 מעל GF(2). שורה j היא הנורה j, '
         f'עמודה i היא הלחיצה x_i, ו-1 אומר שהלחיצה הופכת את הנורה. בעמודה האחרונה הנורות שדולקות בהתחלה. '
         f'בשורה התחתונה הפתרון">'
         f'<tbody><tr class="lo-head"><th>light</th>{head}<th></th><th>lit</th></tr>']
    for j in range(N):
        row = "".join(f'<td class="gs-b{" is-one" if m[j] >> i & 1 else ""}">{m[j] >> i & 1}</td>' for i in range(N))
        b = lit >> j & 1
        t.append(f'<tr><th>{j}</th>{row}<td class="lo-eq">=</td><td class="gs-b{" is-one" if b else ""}">{b}</td></tr>')
    row = "".join(f'<td class="gs-b{" lo-x" if x >> i & 1 else ""}">{x >> i & 1}</td>' for i in range(N))
    t.append(f'<tr class="lo-sol"><th>x</th>{row}<td></td><td></td></tr>')
    return "".join(t) + "</tbody></table></div>\n\n" + legend(
        ("gs-key-one", "1 : הלחיצה הופכת את הנורה"), ("lo-key-x", "1 בפתרון : לוחצים"))


# --- part b --------------------------------------------------------------------------------

def sizes_table() -> str:
    lines = ["| הלוח | נעלמים | הדרגה | משתנים חופשיים | המצבים שאפשר לכבות | פתרונות לכל מצב כזה |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for n in range(3, 8):
        N, f = n * n, free(n)
        share = "כולם" if f == 0 else f"‏1 מתוך {2 ** f}"
        lines.append(f"| {n} × {n} | {N} | {N - f} | {f} | {share} | {2 ** f} |")
    return "\n".join(lines)


def quiet_5() -> str:
    n = 5
    ks = kernel(n)
    items = [{"lit": 0, "press": k} for k in ks]
    svg = row_of_boards(items, n, 22, gap=26, label=(
        "סעיף ב : שלושת הדפוסים השקטים של הלוח 5 על 5, לחיצות שלא משנות אף נורה. כל אחד מהם הוא "
        "סכום XOR של שני האחרים, ויחד עם הדפוס הריק הם ארבעה"))
    return svg + "\n\n" + legend(("lo-key-press", "לחיצה בדפוס השקט"), ("lo-key-off", "כל הנורות נשארות כמו שהן"))


def chase_5() -> str:
    tab = chase_table(5)
    lines = ["| נשארו דולקות בשורה התחתונה | לוחצים בשורה העליונה | לחיצות |", "|:-:|:-:|:-:|"]
    for rest in sorted(tab, key=lambda v: (v != 0, bits(v, 5))):
        f = tab[rest][0]
        lines.append(f'| ‏{ltr(bits(rest, 5))} | ‏{ltr(bits(f, 5))} | {bin(f).count("1")} |')
    return "\n".join(lines)


# --- part c --------------------------------------------------------------------------------

def line_quiet() -> str:
    """The line of 5 lights: pressing 1 1 0 1 1 (a press flips a light and its two neighbours)
    flips every light twice or not at all."""
    n, s = 5, 40
    u = 0b11011
    w, h = n * s + 4, 2 * s + 34
    out = [f'<svg class="figure lo-fig" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.1f}rem" role="img" aria-label="'
           "סעיף ג : שורה של 5 נורות, ולחיצה הופכת נורה ואת שתי השכנות שלה בשורה. לוחצים על הנורות 0, 1, 3 ו-4. "
           "מתחת, כמה פעמים כל נורה מתהפכת : 2, 2, 2, 2, 2. כל נורה מתהפכת מספר זוגי של פעמים, ולכן הלחיצות לא משנות כלום\">"]
    for c in range(n):
        x = 2 + c * s
        out.append(f'<rect class="lo-cell" x="{x}" y="2" width="{s}" height="{s}"/>')
        if u >> c & 1:
            out.append(f'<rect class="lo-press" x="{x + 3}" y="5" width="{s - 6}" height="{s - 6}" rx="4"/>')
        out.append(f'<circle class="lo-off" cx="{x + s / 2:g}" cy="{2 + s / 2:g}" r="{s * 0.27:.1f}"/>')
        flips = sum(1 for d in (-1, 0, 1) if 0 <= c + d < n and u >> (c + d) & 1)
        out.append(f'<text class="lo-num" x="{x + s / 2:g}" y="{s + 30}" text-anchor="middle">{flips}</text>')
    out.append(f'<rect class="lo-frame" x="2" y="2" width="{n * s}" height="{s}"/>')
    out.append(f'<text class="lo-cap" x="{w / 2:g}" y="{2 * s + 28}" text-anchor="middle" direction="rtl">כמה פעמים כל נורה מתהפכת</text>')
    return "".join(out) + "</svg>"


def king_quiet_5() -> str:
    n = 5
    on = [i for i in range(n) if i % 3 != 2]
    col0 = sum(1 << (r * n + 0) for r in on)
    row0 = sum(1 << (0 * n + c) for c in on)
    both = sum(1 << (r * n + c) for r in on for c in on)
    items = [{"lit": 0, "press": col0, "caption": "בעמודה 0"}, {"lit": 0, "press": row0, "caption": "בשורה 0"},
             {"lit": 0, "press": both, "caption": "בשורות ובעמודות"}]
    svg = row_of_boards(items, n, 26, gap=30, label=(
        "סעיף ג : שלושה דפוסים שקטים של הלוח 5 על 5 עם אלכסונים. הראשון הוא 1 1 0 1 1 בעמודה 0, "
        "השני 1 1 0 1 1 בשורה 0, והשלישי הלחיצות בכל משבצת שהשורה שלה והעמודה שלה הן 0, 1, 3 או 4"))
    return svg + "\n\n" + legend(("lo-key-press", "לחיצה בדפוס השקט"))


def king_table() -> str:
    lines = ["| ‏\\( n \\) | ‏\\( n \\bmod 3 \\) | משתנים חופשיים עם אלכסונים | ‏\\( 2n - 1 \\) |", "|:-:|:-:|:-:|:-:|"]
    for n in range(2, 15):
        f = free(n, True)
        lines.append(f"| {n} | {n % 3} | {f} | {2 * n - 1 if n % 3 == 2 else '–'} |")
    return "\n".join(lines)


# --- part d --------------------------------------------------------------------------------

def poly_table() -> str:
    lines = ["| ‏\\( n \\) | ‏\\( p_n(x) \\) | ‏\\( p_n(x + 1) \\) | המחלק המשותף | המעלה |", "|:-:|:-:|:-:|:-:|:-:|"]
    for n in (3, 4, 5, 6):
        p = path_poly(n)
        q = shift1(p)
        g = pgcd(p, q)
        lines.append(f"| {n} | ‏{ltr(poly_text(p))} | ‏{ltr(poly_text(q))} | ‏{ltr(poly_text(g))} | {g.bit_length() - 1} |")
    return "\n".join(lines)


def nullity_table() -> str:
    lines = ["| ‏\\( n \\) | חופשיים, מהדרגה | המעלה של המחלק המשותף | כל מצב פתיר? | עם אלכסונים |", "|:-:|:-:|:-:|:-:|:-:|"]
    for n in range(1, 21):
        f, g, k = free(n), gcd_degree(n), free(n, True)
        lines.append(f"| {n} | {f} | {g} | {'כן' if f == 0 else '**לא**'} | {k} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order (a colon in Hebrew text gets a no-break space)."""
    return [b.replace(" : ", "\u00a0: ") for b in [press_kinds(), part_a_example(), part_a_system(),
            sizes_table(), quiet_5(), chase_5(),
            line_quiet(), king_quiet_5(), king_table(),
            poly_table(), nullity_table()]]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
