#!/usr/bin/env python3
"""Figures and tables of question 0064 (Bachet's weights: the fewest weights that weigh every
whole load from 1 to N, on one pan, on two pans, and with c copies of every weight).

    python tools/figures/fill.py 64        # put the blocks on the page

The reference here is independent of the page code: coefficients() finds the placement of
a load by searching every coefficient vector, and convert() replays the digit-by-digit
conversion for the tables (the rows the weights explorer steps through). blocks() returns,
in page order: part a's balance for 40 on one pan, the legend of the balances, the halving
table of 40; part b's balance for 25, the conversion tables of 25 and of 40; part c's
the table of the reach by the number of states per weight, the conversion of 40 in
balanced base 5, and its balance with two copies of each weight.
"""

from itertools import product

RLM = "‏"
NB = " "
MINUS = "−"
COUNT = {2: "שני", 3: "שלושה", 4: "ארבעה"}


def base_of(c: int, two: bool) -> int:
    """The states of one weight value with c copies: -c..c on two pans, 0..c on one pan."""
    return 2 * c + 1 if two else c + 1


def reach_bound(k: int, c: int, two: bool) -> int:
    """The most loads k weight values (c copies each) can weigh: every load 1..bound."""
    b = base_of(c, two)
    return (b ** k - 1) // 2 if two else b ** k - 1


def coefficients(n: int, k: int, c: int, two: bool):
    """The coefficient vector (lowest weight first) that weighs n with the weights
    base**i, found by trying every vector; None when no vector does."""
    b = base_of(c, two)
    lo = -c if two else 0
    found = [e for e in product(range(lo, c + 1), repeat=k) if sum(d * b ** i for i, d in enumerate(e)) == n]
    assert len(found) <= 1, (n, k, c, two)        # the tight bound: at most one way
    return list(found[0]) if found else None


def convert(n: int, k: int, c: int, two: bool):
    """The conversion step by step: (i, weight, n before, n mod base, digit, carry, n after)."""
    b = base_of(c, two)
    rows = []
    for i in range(k):
        r = n % b
        d = r - b if two and r > c else r
        nxt = (n - d) // b
        rows.append((i, b ** i, n, r, d, 1 if d < 0 else 0, nxt))
        n = nxt
    return rows


def num(v: int) -> str:
    return f"{MINUS}{-v}" if v < 0 else str(v)


# --- the balance -------------------------------------------------------------------------

def balance_svg(n: int, k: int, c: int, two: bool, label: str) -> str:
    """The balance, level: the load and the weights placed beside it on the left pan, the
    weights on the other pan on the right, every weight in a slot of its own (the heaviest
    on the left, as a number is written), and the copies not used in a row under the beam."""
    digits = coefficients(n, k, c, two)
    b = base_of(c, two)
    W, S, BH, LW, LH, top = 640, 56, 32, 64, 48, 8
    S = min(S, (280 - (LW + 10 if two else 0)) // k)
    SH = c * BH
    BY = top + max(SH, LH)
    lc, rc = W * 0.25, W * 0.75

    def xs(center, count):
        return [center - count * S / 2 + p * S + S / 2 for p in range(count)]

    right = xs(rc, k)                                   # slot p holds the weight b**(k-1-p)
    if two:
        grp = LW + 10 + k * S
        x0 = lc - grp / 2
        load_x = x0 + LW / 2
        left = [x0 + LW + 10 + p * S + S / 2 for p in range(k)]
    else:
        load_x, left = lc, []
    off = xs(W / 2, k)
    OY = BY + 46 + SH
    H = OY + 10

    def block(x, y, w, cls, title):
        return (f'<g class="wt-w {cls}"><title>{title}</title><rect x="{x - S / 2 + 3:g}" y="{y:g}" width="{S - 6:g}" height="{BH - 4}" rx="4"/>'
                f'<text class="wt-num" x="{x:g}" y="{y + BH / 2 + 4:g}" text-anchor="middle">{w}</text></g>')

    s = f'<svg class="figure wt-fig" viewBox="0 0 {W} {H:g}" role="img" aria-label="{label}">'
    half = max(W / 2 - (load_x - LW / 2) + 10, right[-1] + S / 2 + 10 - W / 2)   # the beam is even about the pivot
    lo_x, hi_x = W / 2 - half, W / 2 + half
    s += f'<path class="wt-stand" d="M{W / 2 - 26:g},{BY + 32:g} L{W / 2:g},{BY + 4:g} L{W / 2 + 26:g},{BY + 32:g} Z"/>'
    s += f'<line class="wt-beam" x1="{lo_x:g}" y1="{BY + 3:g}" x2="{hi_x:g}" y2="{BY + 3:g}"/>'
    s += (f'<g class="wt-load"><title>the load: {n}</title><rect x="{load_x - LW / 2:g}" y="{BY - LH:g}" width="{LW}" height="{LH}" rx="6"/>'
          f'<text class="wt-num" x="{load_x:g}" y="{BY - LH / 2 + 6:g}" text-anchor="middle">{n}</text></g>')
    for i, d in enumerate(digits):
        p = k - 1 - i
        w = b ** i
        where = right if d > 0 else left
        for m in range(abs(d)):
            cls = "is-other" if d > 0 else "is-beside"
            s += block(where[p], BY - (m + 1) * BH, w, cls, f"weight {w}: {'the other pan' if d > 0 else 'beside the load'}")
        for m in range(c - abs(d)):
            s += block(off[p], OY - (m + 1) * BH, w, "is-off", f"weight {w}: off the scale")
    s += f'<line class="wt-off-line" x1="{off[0] - S / 2:g}" y1="{OY:g}" x2="{off[-1] + S / 2:g}" y2="{OY:g}"/>'
    return s + "</svg>"


def legend(two: bool) -> str:
    keys = ['<span><i class="wt-key-load"></i>המשא</span>',
            '<span><i class="wt-key-other"></i>משקולת בכף השנייה</span>']
    if two:
        keys.append('<span><i class="wt-key-beside"></i>משקולת ליד המשא</span>')
    keys.append('<span><i class="wt-key-off"></i>משקולת בחוץ, מתחת למאזניים</span>')
    return f'<span class="viz-legend">{"".join(keys)}</span>'


# --- the tables ---------------------------------------------------------------------------

def halving_table(n: int, k: int) -> str:
    out = ["| הצעד | המשקולת | המספר | השארית mod 2 | הביט | איפה המשקולת | המספר אחרי |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i, w, before, r, d, _, nxt in convert(n, k, 1, False):
        out.append(f"| {RLM}{i + 1} | {RLM}{w} | {RLM}{before} | {RLM}{r} | {RLM}{d} | {'בכף השנייה' if d else 'בחוץ'} | {RLM}{nxt} |")
    return "\n".join(out)


def ternary_table(n: int, k: int, c: int = 1) -> str:
    b = base_of(c, True)
    out = [f"| הצעד | המשקולת | המספר | השארית mod {b} | הספרה | איפה | ההעברה | המספר אחרי |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i, w, before, r, d, carry, nxt in convert(n, k, c, True):
        copies = "" if abs(d) <= 1 else f"{COUNT[abs(d)]} עותקים "
        where = "בחוץ" if d == 0 else f"{copies}בכף השנייה" if d > 0 else f"{copies}ליד המשא"
        dig = f'{RLM}<b dir="ltr">{num(d)}</b>' if d < 0 else f"{RLM}{d}"
        out.append(f"| {RLM}{i + 1} | {RLM}{w} | {RLM}{before} | {RLM}{r} | {dig} | {where} | {RLM}{carry} | {RLM}{nxt} |")
    return "\n".join(out)


def reach_table() -> str:
    out = ["| המצב | המצבים למשקולת, הבסיס | ‏k = 1 | ‏k = 2 | ‏k = 3 | ‏k = 4 | המשקולות |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for name, c, two in [("כף אחת", 1, False), ("שתי כפות", 1, True), ("כף אחת, ‏2 עותקים", 2, False),
                         ("שתי כפות, ‏2 עותקים", 2, True), ("שתי כפות, ‏3 עותקים", 3, True)]:
        b = base_of(c, two)
        cells = " | ".join(f"{RLM}{reach_bound(k, c, two):,}" for k in range(1, 5))
        ws = ", ".join(str(b ** i) for i in range(4))
        out.append(f'| {name} | {RLM}{b} | {cells} | {RLM}<span dir="ltr">{ws}, …</span> |')
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [
        balance_svg(40, 6, 1, False, "כף אחת : המשא 40 מול המשקולות 32 ו-8, והמשקולות 1, 2, 4 ו-16 בחוץ"),
        legend(False),
        halving_table(40, 6),
        balance_svg(25, 4, 1, True, "שתי כפות : המשא 25 והמשקולת 3 בכף אחת, מול 27 ו-1 בכף השנייה, ו-9 בחוץ"),
        legend(True),
        ternary_table(25, 4),
        ternary_table(40, 4),
        reach_table(),
        ternary_table(40, 3, 2),
        balance_svg(40, 3, 2, True, "שני עותקים מכל משקולת : המשא 40 ושתי משקולות של 5 בכף אחת, מול שתי משקולות של 25 בכף השנייה"),
        legend(True),
    ]


if __name__ == "__main__":
    for n, k, c, two in [(40, 6, 1, False), (25, 4, 1, True), (40, 4, 1, True), (40, 3, 2, True)]:
        print(n, coefficients(n, k, c, two), convert(n, k, c, two))
    print("\n\n".join(blocks()))
