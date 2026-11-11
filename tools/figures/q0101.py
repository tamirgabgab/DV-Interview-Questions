#!/usr/bin/env python3
"""Figures and tables of question 0101, Sicherman dice: two dice with other numbers on their
faces whose sum has the same distribution as the sum of two standard dice.

    python tools/figures/fill.py 101        # put the blocks on the page

The references here are independent of the page code:

- brute_pairs(n, low) searches every pair of dice by their counts alone: a die is a multiset
  of n faces from low to 2n - low, and two dice can match only when their sums and their
  sums of squares add up to those of the standard pair (the mean and the variance of the
  sum), so the pairs are looked up by those two numbers and then compared sum by sum.
- factor_pairs(n, low) splits the factors of the standard die's polynomial,
  x * the cyclotomic polynomials Phi_d for every d > 1 that divides n, between the two dice.
- mixed_pairs(na, nb) is the follow-up: an na-sided and an nb-sided die (na * nb = n * n)
  with the sum of two standard n-sided dice.

blocks() returns, in page order: the 6 x 6 table of the sums of the Sicherman dice coloured
by the sum and its legend, the picture of the factors given to each die (the standard pair
and the Sicherman pair) and its legend, the table of the five pairs when a face may be 0,
the table of the number of pairs for n = 2 to 12, and the table of the pairs of n = 4 and 8.
"""

from __future__ import annotations

import itertools
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from charts import Chart  # noqa: E402

RLM = "‏"
NB = " "
SICHERMAN = ((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8))


# --- the reference ---------------------------------------------------------------------------------

def standard(n: int) -> tuple[int, ...]:
    return tuple(range(1, n + 1))


def sums(a, b) -> Counter:
    """How many of the len(a) * len(b) equally likely rolls give every sum."""
    return Counter(x + y for x in a for y in b)


def same(a, b, n: int | None = None) -> bool:
    n = n or len(a)
    return len(a) == len(b) == n and sums(a, b) == sums(standard(n), standard(n))


def brute_pairs(n: int, low: int = 1) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Every pair of n-sided dice, faces whole numbers >= low, with the sum of two standard
    dice, found from the counts alone (no polynomials). Each pair once, the smaller die first."""
    hi = 2 * n - low                                   # the other die's smallest face is >= low
    std = standard(n)
    s_need = 2 * sum(std)                              # the means add up
    q_need = n * 2 * sum(v * v for v in std) - 2 * sum(std) ** 2   # n * sum(q) - sum(s)^2: the variances add up
    by_key: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    dice = list(itertools.combinations_with_replacement(range(low, hi + 1), n))
    for d in dice:
        by_key.setdefault((sum(d), sum(v * v for v in d)), []).append(d)
    target = sums(std, std)
    out = set()
    for a in dice:
        sa, qa = sum(a), sum(v * v for v in a)
        sb = s_need - sa
        rest = q_need - (n * qa - sa * sa) + sb * sb
        if rest % n:
            continue
        for b in by_key.get((sb, rest // n), ()):
            if a <= b and sums(a, b) == target:
                out.add((a, b))
    return sorted(out)


def mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def div_exact(p, q):
    """p / q for polynomials (lowest power first) that divide exactly."""
    p = list(p)
    while q[-1] == 0:
        q = q[:-1]
    out = [0] * (len(p) - len(q) + 1)
    for i in range(len(out) - 1, -1, -1):
        c, r = divmod(p[i + len(q) - 1], q[-1])
        assert r == 0
        out[i] = c
        for j, v in enumerate(q):
            p[i + j] -= c * v
    assert not any(p)
    return out


_CYC: dict[int, list[int]] = {}


def cyclotomic(d: int) -> list[int]:
    """Phi_d: x^d - 1 divided by Phi_e for every e < d that divides d."""
    if d not in _CYC:
        p = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0:
                p = div_exact(p, cyclotomic(e))
        _CYC[d] = p
    return _CYC[d]


def die_poly(faces) -> list[int]:
    c = [0] * (max(faces) + 1)
    for f in faces:
        c[f] += 1
    return c


def faces_of(p) -> tuple[int, ...]:
    return tuple(e for e, c in enumerate(p) for _ in range(c))


def divisors(n: int) -> list[int]:
    return [d for d in range(2, n + 1) if n % d == 0]


def factor_pairs(n: int, low: int = 1, keep_split: bool = False):
    """The pairs of n-sided dice from the factors x * Phi_d (d | n, d > 1) of the standard die:
    die A takes k_d of the two Phi_d of P(x)^2 and the x's split as the low faces allow; a
    split is a die when A(1) = B(1) = n and no coefficient is negative."""
    ds = divisors(n)
    xs = (1,) if low == 1 else (0, 1, 2)
    out = {}
    for split in itertools.product((0, 1, 2), repeat=len(ds)):
        for xa in xs:
            a, b = [0] * xa + [1], [0] * (2 - xa) + [1]
            for d, k in zip(ds, split):
                for _ in range(k):
                    a = mul(a, cyclotomic(d))
                for _ in range(2 - k):
                    b = mul(b, cyclotomic(d))
            if sum(a) != n or sum(b) != n or min(a) < 0 or min(b) < 0:
                continue
            pair = tuple(sorted((faces_of(a), faces_of(b))))
            out.setdefault(pair, (xa, dict(zip(ds, split))) if pair[0] == faces_of(a) else (2 - xa, {d: 2 - k for d, k in zip(ds, split)}))
    pairs = sorted(out)
    return [(p, out[p]) for p in pairs] if keep_split else pairs


def bad_splits(n: int) -> list[tuple[dict[int, int], list[int]]]:
    """The splits with A(1) = n whose A has a negative coefficient (not a die)."""
    ds, bad = divisors(n), []
    for split in itertools.product((0, 1, 2), repeat=len(ds)):
        a = [0, 1]
        for d, k in zip(ds, split):
            for _ in range(k):
                a = mul(a, cyclotomic(d))
        if sum(a) == n and min(a) < 0:
            bad.append((dict(zip(ds, split)), a))
    return bad


def mixed_pairs(na: int, nb: int, n: int = 6):
    """An na-sided die and an nb-sided die, positive faces, with the sum of two standard n-sided
    dice (na * nb = n * n), from the factors of P(x)^2."""
    assert na * nb == n * n
    ds = divisors(n)
    out = set()
    for split in itertools.product((0, 1, 2), repeat=len(ds)):
        a, b = [0, 1], [0, 1]
        for d, k in zip(ds, split):
            for _ in range(k):
                a = mul(a, cyclotomic(d))
            for _ in range(2 - k):
                b = mul(b, cyclotomic(d))
        if sum(a) == na and sum(b) == nb and min(a) >= 0 and min(b) >= 0:
            out.add((faces_of(a), faces_of(b)))
    return sorted(out)


def mixed_brute(na: int, nb: int, n: int = 6):
    """The same by search: die A any multiset of na faces from 1 to 2n - 1, B what is left."""
    target = sums(standard(n), standard(n))
    tp = [target.get(s, 0) for s in range(2 * n + 1)]
    out = set()
    for a in itertools.combinations_with_replacement(range(1, 2 * n), na):
        pa = die_poly(a)
        try:
            pb = div_exact(tp, pa)
        except AssertionError:
            continue
        if min(pb) >= 0 and sum(pb) == nb and pb[0] == 0:        # B's faces positive too
            out.add((a, faces_of(pb)))
    return sorted(out)



# --- the figures -----------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def flist(faces) -> str:
    """A die's faces as an ordered list in a left-to-right span."""
    return ltr(", ".join(map(str, faces)))


def level(s: int, n: int) -> int:
    """The tint of the sum s: how often two standard n-sided dice give it, on a scale of 1 to 6
    (0 for a sum they never give). tools/figures/q0101.py and explorer/sicherman.js agree."""
    f = n - abs(s - (n + 1))
    if f <= 0:
        return 0
    return -(-6 * f // n)


def hue(s: int, n: int) -> str:
    """Below the middle sum blue, the middle green, above it purple."""
    return "sc-lo" if s < n + 1 else "sc-mid" if s == n + 1 else "sc-hi"


def triangle_chart() -> str:
    """The distribution of the sum of two standard dice: the triangle of the statement."""
    c = Chart("התפלגות הסכום של שתי קוביות רגילות : הסכומים 2 עד 12, ומספר ההטלות מתוך 36 שנותנות כל סכום, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1",
              w=420, h=196, x0=34, right=8, top=18, base=166, slots=11, y_max=6, style="max-width:26.25rem")
    c.grid_y([0, 2, 4, 6])
    cnt = sums(standard(6), standard(6))
    for s in range(2, 13):
        c.bar(s - 1, cnt[s], "by-multiples", title=f"sum {s}: {cnt[s]} of 36", value_label=cnt[s])
    c.x_ticks(range(1, 12), labels=[str(s) for s in range(2, 13)])
    c.axis()
    return c.svg()


CELL = 28


def sum_table_svg(a, b, label) -> str:
    """The table of the sums: a row per face of A, a column per face of B, each cell its sum,
    tinted by the sum."""
    n = len(a)
    w = (n + 1) * CELL + 4
    o = [f'<svg class="figure sc-sums" viewBox="0 0 {w} {w}" style="max-width:{w / 16:g}rem" role="img" aria-label="{label}">',
         f'<text class="sc-corner" x="{2 + CELL / 2}" y="{2 + CELL / 2 + 4}" text-anchor="middle">+</text>']
    for j, f in enumerate(b):
        o.append(f'<text class="sc-face" x="{2 + (j + 1.5) * CELL}" y="{2 + CELL / 2 + 4}" text-anchor="middle">{f}</text>')
    for i, e in enumerate(a):
        y = 2 + (i + 1) * CELL
        o.append(f'<text class="sc-face" x="{2 + CELL / 2}" y="{y + CELL / 2 + 4}" text-anchor="middle">{e}</text>')
        for j, f in enumerate(b):
            s, x = e + f, 2 + (j + 1) * CELL
            o.append(f'<g class="sc-cell {hue(s, n)} sc-f{level(s, n)}"><title>{e} + {f} = {s}</title>'
                     f'<rect x="{x + 1}" y="{y + 1}" width="{CELL - 2}" height="{CELL - 2}" rx="3"/>'
                     f'<text x="{x + CELL / 2}" y="{y + CELL / 2 + 4}" text-anchor="middle">{s}</text></g>')
    o.append("</svg>")
    return "".join(o)


def sum_tables() -> str:
    std = standard(6)
    a, b = SICHERMAN
    left = sum_table_svg(std, std, "טבלת הסכומים של שתי קוביות רגילות : שורה לכל פאה של A, עמודה לכל פאה של B. כל סכום יושב על אלכסון אחד, 7 על האלכסון הארוך")
    right = sum_table_svg(a, b, "טבלת הסכומים של קוביות Sicherman, A עם הפאות 1, 2, 2, 3, 3, 4 ו-B עם 1, 3, 4, 5, 6, 8 : אותם 36 סכומים, מפוזרים אחרת, ושוב 7 שש פעמים")
    return ('<div class="sc-pair">'
            f'<figure class="sc-fig">{left}<figcaption>קוביות רגילות</figcaption></figure>'
            f'<figure class="sc-fig">{right}<figcaption>קוביות Sicherman : ‏{ltr("A = {" + ", ".join(map(str, a)) + "}")} ו-{ltr("B = {" + ", ".join(map(str, b)) + "}")}</figcaption></figure>'
            '</div>')


def tables_legend() -> str:
    return ('<span class="viz-legend"><span><i class="sc-key-lo"></i>סכום קטן מ-7</span>'
            '<span><i class="sc-key-mid"></i>הסכום 7</span><span><i class="sc-key-hi"></i>סכום גדול מ-7</span>'
            '<span>ככל שהסכום נפוץ יותר, הצבע עמוק יותר</span></span>')


# the factors of P(x) = x + ... + x^6 in the order of the picture, with their CSS class
FACTORS = [("x", "sc-px", None), ("1 + x", "sc-p2", 2), ("1 + x + x²", "sc-p3", 3), ("1 − x + x²", "sc-p6", 6)]


def split_svg(split_a: dict[int, int], label: str) -> str:
    """The factors each die gets: a column per die, a chip per factor (two slots for the free
    factor 1 - x + x^2, an empty slot dashed), and the faces they multiply out to."""
    cw, ch, gap, top = 96, 22, 6, 28
    w, h = 2 * cw + 14, top + 5 * (ch + gap) + 30
    o = [f'<svg class="figure sc-split" viewBox="0 0 {w} {h}" style="max-width:{w / 16:g}rem" role="img" aria-label="{label}">']
    split_b = {d: 2 - k for d, k in split_a.items()}
    for col, (name, split) in enumerate((("A", split_a), ("B", split_b))):
        x0 = 2 + col * (cw + 10)
        o.append(f'<text class="sc-head" x="{x0 + cw / 2}" y="16" text-anchor="middle">{name}</text>')
        poly = [0, 1]
        slots = [("x", "sc-px")] + [(t, c) for t, c, d in FACTORS[1:3]] + [(FACTORS[3][0], FACTORS[3][1]) if i < split[6] else None for i in range(2)]
        for t, c, d in FACTORS[1:]:
            for _ in range(split[d]):
                poly = mul(poly, cyclotomic(d))
        for i, slot in enumerate(slots):
            y = top + i * (ch + gap)
            if slot is None:
                o.append(f'<rect class="sc-chip sc-empty" x="{x0 + 4}" y="{y}" width="{cw - 8}" height="{ch}" rx="11"/>')
                continue
            t, c = slot
            o.append(f'<g class="sc-chip {c}"><rect x="{x0 + 4}" y="{y}" width="{cw - 8}" height="{ch}" rx="11"/>'
                     f'<text x="{x0 + cw / 2}" y="{y + 15}" text-anchor="middle">{t}</text></g>')
        y = top + 5 * (ch + gap) + 4
        o.append(f'<line class="sc-rule" x1="{x0 + 4}" x2="{x0 + cw - 4}" y1="{y}" y2="{y}"/>'
                 f'<text class="sc-faces" x="{x0 + cw / 2}" y="{y + 18}" text-anchor="middle">{" ".join(map(str, faces_of(poly)))}</text>')
    o.append("</svg>")
    return "".join(o)


def split_figure() -> str:
    std = split_svg({2: 1, 3: 1, 6: 1}, "הגורמים של הקוביות הרגילות : לכל קובייה x, ‏1 + x, ‏1 + x + x² ו-1 − x + x² אחד, והפאות 1 עד 6")
    sic = split_svg({2: 1, 3: 1, 6: 0}, "הגורמים של קוביות Sicherman : ל-A רק x, ‏1 + x ו-1 + x + x², והפאות 1, 2, 2, 3, 3, 4. ל-B אותם שלושה ושני הגורמים 1 − x + x², והפאות 1, 3, 4, 5, 6, 8")
    return ('<div class="sc-pair">'
            f'<figure class="sc-fig">{std}<figcaption>הזוג הרגיל : ‏{ltr("1 − x + x²")} אחד לכל קובייה</figcaption></figure>'
            f'<figure class="sc-fig">{sic}<figcaption>זוג Sicherman : שניהם לקובייה B</figcaption></figure>'
            '</div>')


def split_legend() -> str:
    return ('<span class="viz-legend"><span><i class="sc-key-px"></i>הגורם x</span>'
            f'<span><i class="sc-key-p2"></i>הגורם {ltr("1 + x")}</span>'
            f'<span><i class="sc-key-p3"></i>הגורם {ltr("1 + x + x²")}</span>'
            f'<span><i class="sc-key-p6"></i>הגורם החופשי {ltr("1 − x + x²")}</span>'
            '<span><i class="sc-key-empty"></i>מקום ריק</span></span>')


def pair_rows(pairs, names) -> list[str]:
    return [f"| {name} | {RLM}{flist(a)} | {RLM}{flist(b)} |" for name, (a, b) in zip(names, pairs)]


ZERO_NAMES = {
    ((1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6)): "הרגילות",
    ((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)): f"{RLM}Sicherman",
    ((0, 1, 2, 3, 4, 5), (2, 3, 4, 5, 6, 7)): "הרגילות, A פחות 1 ו-B ועוד 1",
    ((0, 1, 1, 2, 2, 3), (2, 4, 5, 6, 7, 9)): "‏Sicherman, הקטנה פחות 1 והגדולה ועוד 1",
    ((0, 2, 3, 4, 5, 7), (2, 3, 3, 4, 4, 5)): "‏Sicherman, הגדולה פחות 1 והקטנה ועוד 1",
}


def table_zero() -> str:
    """The five pairs of six-sided dice when a face may be 0: part a's two and three shifts."""
    pairs = factor_pairs(6, 0)
    order = sorted(pairs, key=lambda p: list(ZERO_NAMES).index(p))
    rows = ["| הזוג | קובייה A | קובייה B |", "|---|---|---|"]
    for a, b in order:
        rows.append(f"| {ZERO_NAMES[(a, b)]} | {RLM}{flist(a)} | {RLM}{flist(b)} |")
    return "\n".join(rows)


def poly_tex(p) -> str:
    """A polynomial (lowest power first) in TeX, the lowest power first; 1 + x + ... + x^(d-1)
    when every coefficient is 1 and there are more than four."""
    if len(p) > 5 and all(c == 1 for c in p):
        return rf"1 + x + \dots + x^{{{len(p) - 1}}}"
    out = []
    for e, c in enumerate(p):
        if not c:
            continue
        mono = "1" if e == 0 else "x" if e == 1 else f"x^{{{e}}}" if e > 9 else f"x^{e}"
        term = mono if abs(c) == 1 else f"{abs(c)}{mono}" if e else str(abs(c))
        out.append(("- " if c < 0 else "+ ") + term if out else ("-" if c < 0 else "") + term)
    return " ".join(out)


def table_cyclotomic() -> str:
    rows = [r"| המחלק d | הגורם \( \Phi_d(x) \) | הערך \( \Phi_d(1) \) |", "|:-:|---|:-:|"]
    for d in range(2, 13):
        p = cyclotomic(d)
        rows.append(rf"| {d} | {RLM}\( {poly_tex(p)} \) | {sum(p)} |")
    return "\n".join(rows)


def table_counts() -> str:
    rows = ["| הפאות n | הגורמים של \\( P_n \\) מלבד x | הזוגות, פאות חיוביות | הזוגות, גם 0 |", "|:-:|---|:-:|:-:|"]
    for n in range(2, 13):
        fs = r" \, ".join(rf"\Phi_{{{d}}}" for d in divisors(n))
        rows.append(rf"| {n} | {RLM}\( {fs} \) | {len(factor_pairs(n))} | {len(factor_pairs(n, 0))} |")
    return "\n".join(rows)


def factor_tex(xa: int, split: dict[int, int]) -> str:
    parts = ["x" if xa == 1 else f"x^{xa}"] if xa else []
    for d, k in split.items():
        if k:
            parts.append(rf"\Phi_{{{d}}}" + (f"^{k}" if k > 1 else ""))
    return r" \, ".join(parts)


def table_pairs_48() -> str:
    rows = ["| הפאות n | קובייה A | הגורמים של A | קובייה B | הגורמים של B |", "|:-:|---|---|---|---|"]
    for n in (4, 8):
        for (a, b), (xa, split) in reversed(factor_pairs(n, keep_split=True)):
            sb = {d: 2 - k for d, k in split.items()}
            rows.append(rf"| {n} | {RLM}{flist(a)} | {RLM}\( {factor_tex(xa, split)} \) | {RLM}{flist(b)} | {RLM}\( {factor_tex(2 - xa, sb)} \) |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    out = [
        triangle_chart(),
        sum_tables(),
        tables_legend(),
        split_figure(),
        split_legend(),
        table_zero(),
        table_cyclotomic(),
        table_counts(),
        table_pairs_48(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    for n in range(2, 13):
        print(n, len(factor_pairs(n)), factor_pairs(n) if n in (4, 8) else "")
    print("zero", factor_pairs(6, 0))
    print("brute", brute_pairs(6), brute_pairs(6, 0))
    print("bad12", bad_splits(12)[:1])
    for na in (2, 3, 4):
        print(na, 36 // na, mixed_pairs(na, 36 // na))
