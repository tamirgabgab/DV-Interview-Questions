#!/usr/bin/env python3
"""Shared math and drawings of questions 0027 and 0028 (a cake split by fractions that grow
as an arithmetic or a geometric sequence; who gets the largest share).

Person k takes the fraction p_k of what is left; a person whose fraction reaches 1 takes the
rest and the split ends. Exact values use Fractions; the drawings are inline SVG with the
site's chart classes. q0027.py and q0028.py print the blocks of each page.
"""

import math
from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction as Fr

from charts import Chart

getcontext().prec = 60
ARITH, GEO = "arith", "geo"


# --- the split -----------------------------------------------------------------------------

def raw_fraction(kind, a, step, k):
    """p_k before the cap at 1: a + (k - 1) d, or a q^(k - 1)."""
    return a + (k - 1) * step if kind == ARITH else a * step ** (k - 1)


def split(kind, a, step):
    """Rows (k, p, R, S): the fraction actually taken (capped at 1), what is left before
    person k, and the share of person k. Stops at the person who takes the rest."""
    a, step = Fr(a), Fr(step)
    rows, R, k = [], Fr(1), 1
    while True:
        p = min(raw_fraction(kind, a, step, k), Fr(1))
        rows.append((k, p, R, p * R))
        if p == 1:
            return rows
        R *= 1 - p
        k += 1


def best(rows):
    """The people with the largest share (two on a tie)."""
    top = max(S for _, _, _, S in rows)
    return [k for k, _, _, S in rows if S == top], top


def threshold(kind, step):
    """T: S(k + 1) > S(k) exactly when p_k < T (before the cap)."""
    step = float(step)
    return (math.sqrt(step * step + 4 * step) - step) / 2 if kind == ARITH else 1 - 1 / step


def formula(kind, a, step):
    """The page's closed form for the person with the largest share (d <= 1/2, q <= 2)."""
    a, step = Fr(a), Fr(step)
    if kind == ARITH:
        d = step
        # first k with a + (k - 1) d >= T, where T is the positive root of p^2 + d p - d
        k = 1
        while (raw_fraction(kind, a, d, k) ** 2 + d * raw_fraction(kind, a, d, k) - d) < 0:
            k += 1
        return k
    q = step
    k = 1
    while a * q ** k < q - 1:          # q^k >= (q - 1) / a
        k += 1
    return k


def ratios(rows):
    """S(k + 1) / S(k) for k = 1 .. n - 1."""
    return [(rows[i][0], rows[i + 1][3] / rows[i][3]) for i in range(len(rows) - 1)]


# --- formatting ------------------------------------------------------------------------------

def dec(x, places=4):
    """Round half up, like a hand calculation (0.01485 -> 0.0149)."""
    x = Fr(x)
    q = Decimal(1).scaleb(-places)
    return str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, ROUND_HALF_UP))


def short(x):
    """0.01, 0.1, 1.5 (no trailing zeros)."""
    s = dec(x, 6).rstrip("0").rstrip(".")
    return s or "0"


def table(kind, a, step):
    rows = split(kind, a, step)
    peak, _ = best(rows)
    lines = ["| האדם \\( k \\) | השבר \\( p_k \\) | נשאר לפניו \\( R_k \\) | מקבל \\( S_k \\) |",
             "|---|---|---|---|"]
    for k, p, R, S in rows:
        pk = "1, לוקח את השארית" if p == 1 else short(p) if Fr(dec(p)) == p else dec(p)
        cells = [str(k), pk, "1" if R == 1 else dec(R), dec(S)]
        if k in peak:
            cells = [f"**{c}**" for c in cells]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# --- drawings ----------------------------------------------------------------------------------

def slice_class(k, peak):
    if k in peak:
        return "cake-peak"
    return "cake-slice" if k % 2 else "cake-slice2"


def cake_rows(kind, a, step, show_peak=True):
    """One row per person: the cake as it is when person k arrives (grey: left for the
    next people, colour: the slice of person k, dashed: already taken), then the whole cake
    as one strip with every slice in place."""
    rows = split(kind, a, step)
    peak = best(rows)[0] if show_peak else []
    x0, W, h, gap, top = 52, 490, 24, 9, 8
    n = len(rows)
    strip_y = top + n * (h + gap) + 18
    H = strip_y + h + 26
    X = lambda v: x0 + float(v) * W
    p = [f'<svg class="figure" viewBox="0 0 640 {H}" style="max-width:40rem" role="img" '
         f'aria-label="חלוקת העוגה, שורה לכל אדם : כמה נשאר כשהוא מגיע והפרוסה שהוא חותך, ובסוף כל העוגה '
         f'עם הפרוסות של כל {n} האנשים">']
    for k, pk, R, S in rows:
        y = top + (k - 1) * (h + gap)
        rest = R - S
        p.append(f'<rect class="cake-gone" x="{x0}" y="{y}" width="{W}" height="{h}" rx="3"/>')
        if rest > 0:
            p.append(f'<rect class="cake-rest" x="{x0}" y="{y}" width="{float(rest) * W:.1f}" height="{h}"/>')
        p.append(f'<rect class="{slice_class(k, peak)}" x="{X(rest):.1f}" y="{y}" width="{max(float(S) * W, 0.6):.1f}" '
                 f'height="{h}"><title>אדם {k} : p = {short(dec(pk))}, S = {dec(S)}</title></rect>')
        p.append(f'<text class="legend" x="{x0 - 12}" y="{y + 17}" text-anchor="end" style="font-size:17px">{k}</text>')
        p.append(f'<text class="tick" x="{X(R) + 6:.1f}" y="{y + 16}" style="font-size:15px">p = {short(dec(pk))}</text>')
    for k, pk, R, S in rows:
        rest = R - S
        p.append(f'<rect class="{slice_class(k, peak)}" x="{X(rest):.1f}" y="{strip_y}" '
                 f'width="{max(float(S) * W, 0.6):.1f}" height="{h}"/>')
        if float(S) * W >= 16:
            p.append(f'<text class="tick" x="{X(rest + S / 2):.1f}" y="{strip_y + h + 18}" text-anchor="middle" style="font-size:15px">{k}</text>')
    p.append(f'<rect class="cake-edge" x="{x0}" y="{strip_y}" width="{W}" height="{h}" rx="3"/></svg>')
    return "".join(p)


def cake_legend(show_peak=True):
    peak = '<span><i class="cake-peak"></i>הפרוסה הגדולה ביותר</span>' if show_peak else ""
    return ('<span class="viz-legend"><span><i class="cake-slice"></i><i class="cake-slice2"></i>הפרוסה '
            'של האדם, בשני גוונים לסירוגין</span>' + peak +
            '<span><i class="cake-rest"></i>נשאר לבאים אחריו</span>'
            '<span><i class="cake-gone"></i>כבר נלקח</span></span>')


def shares_chart(kind, a, step):
    """Bars of S(k), the largest one highlighted."""
    rows = split(kind, a, step)
    peak, top_s = best(rows)
    n = len(rows)
    c = Chart(f"החלק של כל אדם. הגדול ביותר הוא של האדם ה-{peak[0]}, בערך {dec(top_s, 3)} מהעוגה",
              top=22, slots=n, y_max=math.ceil(float(top_s) * 20 + 0.6) / 20)
    c.grid_y([i * 0.05 for i in range(int(round(c.y_max / 0.05)) + 1)], "{:.2f}")
    for k, pk, R, S in rows:
        c.bar(k, S, "by-enum" if k in peak else "by-multiples", title=f"S({k}) = {dec(S)}",
              value_label=dec(S, 3) if n <= 13 else None)
    return c.x_ticks(range(1, n + 1)).axis("k").svg()


def shares_legend():
    return ('<span class="viz-legend"><span><i class="by-multiples"></i>‏\\( S_k \\), החלק של האדם ה-\\( k \\)</span>'
            '<span><i class="by-enum"></i>החלק הגדול ביותר</span></span>')


def fraction_chart(kind, a, step):
    """Stems of p(k) against the dashed threshold T; the first fraction at or above T is
    the person with the largest share."""
    rows = split(kind, a, step)
    T = threshold(kind, step)
    peak = best(rows)[0]
    c = Chart(f"השבר של כל אדם מול הסף T, בערך {T:.3f}. הראשון שמגיע לסף הוא האדם ה-{peak[0]}",
              slots=len(rows))
    c.grid_y([0, 0.25, 0.5, 0.75, 1]).hline(T, f"T ≈ {T:.3f}")
    for k, pk, R, S in rows:
        cls = "s2" if k == peak[0] else ("s1" if float(pk) < T - 1e-12 else "ink")
        c.stem(k, pk, cls, r=6 if k == peak[0] else 4.5, title=f"p({k}) = {dec(pk)}")
    return c.x_ticks(range(1, len(rows) + 1)).axis("k").svg()


def fraction_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>מתחת לסף : הבא אחריו מקבל יותר</span>'
            '<span><i class="s2"></i>הראשון שמגיע לסף : החלק הגדול ביותר</span>'
            '<span><i class="ink"></i>מעל הסף</span>'
            '<span><i class="ink-dash"></i>הסף \\( T \\)</span></span>')


def ratio_chart(kind, a, step, log=False):
    """S(k + 1) / S(k) at each k against the dashed line y = 1. The first point below the
    line is at the person with the largest share."""
    rows = split(kind, a, step)
    rs = ratios(rows)
    peak = best(rows)[0]
    label = f"היחס בין החלק של האדם הבא לחלק של האדם הנוכחי. הוא יורד מתחת ל-1 לראשונה אצל האדם ה-{peak[0]}"
    if log:
        c = Chart(label, slots=len(rows), log=True, y_min=0.05, y_max=20)
        ticks = [0.1, 0.2, 0.5, 1, 2, 5, 10]
    else:
        ymax = math.ceil(float(step) * 2) / 2
        c = Chart(label, slots=len(rows), y_max=ymax)
        ticks = [i / 2 for i in range(int(ymax * 2) + 1)]
    c.grid_y(ticks).hline(1).path(rs, "s1-line", width=1.5)
    last = rs[-1][0]
    for k, r in rs:
        cls = "s2" if k == peak[0] else ("ink" if k == last else "s1")
        c.dot(k, r, cls, r=6 if k == peak[0] else 4.5, title=f"S({k + 1}) / S({k}) = {dec(r, 3)}")
    return c.x_ticks(range(1, len(rows))).axis("k").svg()


def ratio_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>היחס \\( S_{k+1} / S_k \\)</span>'
            '<span><i class="s2"></i>הפעם הראשונה מתחת ל-1</span>'
            '<span><i class="ink"></i>היחס אל מי שלוקח את השארית</span>'
            '<span><i class="ink-dash"></i>הקו \\( y = 1 \\)</span></span>')


def f_curve(a=Fr(1, 100), d=Fr(1, 10), people=6):
    """f(p) = p^2 / (1 - p) against the line y = d; they cross at p = T. The fractions of
    the first people sit on the curve: below the line the next person gets more."""
    T = threshold(ARITH, d)
    c = Chart(f"הפונקציה p בריבוע חלקי 1 פחות p, מול הקו בגובה d = {short(d)}. הם נחתכים ב-T, בערך {T:.3f}",
              h=260, right=14, top=14, base=226, x_max=0.7, y_max=0.6)
    c.grid_y([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]).x_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                                     ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6"])
    pts, v = [], 0.0
    while v <= c.x_max + 1e-9 and v * v / (1 - v) <= c.y_max:
        pts.append((v, v * v / (1 - v)))
        v += 0.005
    c.path(pts, "s1-line", width=2.5).hline(d, f"y = d = {short(d)}", label_at="end")
    c.vline(T, d, f"T ≈ {T:.3f}")
    peak = best(split(ARITH, a, d))[0]
    for k, pk, _, _ in split(ARITH, a, d)[:people]:
        fv = float(pk) ** 2 / (1 - float(pk))
        if fv > c.y_max:
            continue
        cls = "s2" if k == peak[0] else ("s1" if float(pk) < T else "ink")
        c.dot(pk, fv, cls, r=6 if k == peak[0] else 4.5, title=f"p({k}) = {dec(pk)}")
        c.text(pk, fv, k, cls="tick", dy=-9)
    c.dot(T, d, "ink", r=3.5)
    return c.axis("p", at="end").svg()


def f_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>‏\\( f(p) = p^2 / (1 - p) \\)</span>'
            '<span><i class="ink-dash"></i>הקו \\( y = d \\)</span>'
            '<span><i class="s2"></i>האדם ה-4 : הראשון מעל הקו</span>'
            '<span><i class="ink"></i>אחריו, גם הם מעל הקו</span></span>')


def g_lines(a=Fr(1, 100), qs=(Fr(3, 2), Fr(2))):
    """y = q (1 - p) for a few q against y = 1; they cross at p = 1 - 1/q. The fractions of
    the people of the first q sit on its line."""
    c = Chart("הקווים q כפול 1 פחות p מול הקו y = 1. הם נחתכים ב-p = 1 פחות 1 חלקי q : שליש עבור q = 1.5, וחצי עבור q = 2",
              h=260, right=14, top=14, base=226, x_max=1, y_max=2.1)
    c.grid_y([0, 0.5, 1, 1.5, 2]).x_ticks([0, 0.25, 0.5, 0.75]).hline(1)
    for i, q in enumerate(qs):
        T = 1 - 1 / q
        c.segment((0, q), (1, 0), "s1-line" if i == 0 else "s3-line")
        c.text(0, q, f"q = {short(q)}", anchor="start", dx=8, dy=-6)
        c.vline(T, 1, f"{T.numerator}/{T.denominator}").dot(T, 1, "ink", r=3.5)
    q = qs[0]
    rows = split(GEO, a, q)
    peak = best(rows)[0]
    T = 1 - 1 / q
    for k, pk, _, _ in rows[:-1]:
        cls = "s2" if k == peak[0] else ("s1" if pk < T else "ink")
        c.dot(pk, q * (1 - pk), cls, r=6 if k == peak[0] else 4, title=f"p({k}) = {dec(pk)}")
    return c.axis("p", at="end").svg()


def g_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>‏\\( y = 1.5\\,(1 - p) \\)</span>'
            '<span><i class="s3"></i>‏\\( y = 2\\,(1 - p) \\)</span>'
            '<span><i class="ink-dash"></i>הקו \\( y = 1 \\)</span>'
            '<span><i class="s2"></i>האדם ה-10 : הראשון מתחת לקו</span>'
            '<span><i class="ink"></i>אחריו, גם הם מתחת לקו</span></span>')
