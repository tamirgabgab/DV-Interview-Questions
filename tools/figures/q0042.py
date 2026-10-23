#!/usr/bin/env python3
"""Figures and tables of question 0042 (the camel and the water: 450 litres at the start,
150 on the camel, half a litre per km, 30 litres to deliver; then any a, c, w and T).

    python tools/figures/fill.py 42        # put the blocks on the page

The reference here is independent of the page code and exact (fractions): with j loads in
motion every km costs (2j - 1) a litres (j passes forward, j - 1 back), the water in
motion drops from w to every multiple of c above T and then to T, each segment is as long
as its drop in water divided by the price of its loads, and passes() plays the camel pass
by pass (full loads first, the partial load last). blocks() returns, in page order: the
price table, the stops table, the walks of segments 1 and 2, the water-in-motion chart
with its legend, the examples table of part b, the chart of the distance against the
water with the logarithmic approximation, and the approximation table of the bonus.
tests/0042 checks every number against the page code, the explorer and brute force.
"""

import sys
from fractions import Fraction as F
from math import ceil, log
from pathlib import Path

A, C, W, T = F(1, 2), 150, 450, 30
GAMMA = 0.5772156649015329
APPROX_CONST = 2 * log(2) + GAMMA                      # 1.9635..., the "1.96" of the page
RLM = "‏"


# --- the model --------------------------------------------------------------------------

def price(j, a):
    """Litres per km with j loads in motion: j passes forward and j - 1 back."""
    return (2 * j - 1) * a


def levels(c, w, T):
    """The water in motion at the start, at every multiple of c strictly between T and w
    (where a load ends and the price drops), and at the end."""
    k = ceil(F(w) / c)
    return [F(w)] + [F(j * c) for j in range(k - 1, 0, -1) if j * c > T] + [F(T)]


def segments(a, c, w, T):
    """The route as (x0, x1, loads, n0, n1): the segment from x0 to x1 moves the water from
    n0 down to n1 litres with `loads` loads, at the price of those loads."""
    out, x = [], F(0)
    lv = levels(c, w, T)
    for n0, n1 in zip(lv, lv[1:]):
        j = ceil(n0 / c)
        x1 = x + (n0 - n1) / price(j, a)
        out.append((x, x1, j, n0, n1))
        x = x1
    return out


def distance(a, c, w, T):
    return segments(a, c, w, T)[-1][1]


def stops(a, c, w, T):
    return [x1 for _, x1, *_ in segments(a, c, w, T)[:-1]]


def formula(a, c, w, T):
    """The closed form of part b (T <= c): (1/a) [c (1 + 1/3 + ... + 1/(2k - 3)) + r / (2k - 1) - T]."""
    k = ceil(F(w) / c)
    r = w - (k - 1) * c
    return (c * sum(F(1, 2 * j - 1) for j in range(1, k)) + F(r, 2 * k - 1) - T) / F(a)


def range_of(a, c, n):
    """Phi(n): the km that n litres buy at the price list (T = 0)."""
    return distance(a, c, n, 0) if n > 0 else F(0)


def approx(a, c, w, T):
    """The logarithmic approximation of the bonus: c / (2a) (ln(w / c) + 1.96) - T / a."""
    return c / (2 * a) * (log(w / c) + APPROX_CONST) - T / a


def passes(a, c, w, T):
    """Every pass of the camel as a dict: the segment, out or back, the litres when it
    leaves and when it arrives, what it drops at the far end, and the depots after it
    (litres at the start and at the end of every segment). Full loads first, the partial
    load last, so every return trip is made by a camel that left with a full load."""
    segs = segments(a, c, w, T)
    depots = [F(w)] + [F(0)] * len(segs)
    out = []
    for s, (x0, x1, j, _, _) in enumerate(segs):
        cost = a * (x1 - x0)
        for i in range(j):
            take = min(F(c), depots[s])
            keep = F(0) if i == j - 1 else cost
            depots[s] -= take
            depots[s + 1] += take - cost - keep
            out.append(dict(seg=s, back=False, carry0=take, carry1=take - cost, drop=take - cost - keep, depots=list(depots)))
            if keep:
                out.append(dict(seg=s, back=True, carry0=keep, carry1=F(0), drop=F(0), depots=list(depots)))
    return out


def walked(a, c, w, T):
    """The km the camel walks in total, every pass counted."""
    segs = segments(a, c, w, T)
    return sum((x1 - x0) * (2 * j - 1) for x0, x1, j, _, _ in segs)


# --- formatting ------------------------------------------------------------------------

def num(v, nd=1):
    """A fraction as text: an integer as is, otherwise with nd decimals."""
    v = F(v)
    if v.denominator == 1:
        return f"{v.numerator:,}"
    return f"{float(v):,.{nd}f}"


def frac(v):
    """A fraction as LaTeX: an integer, or \\frac."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"\\frac{{{v.numerator}}}{{{v.denominator}}}"


# --- tables ------------------------------------------------------------------------------

def price_table(a=A, c=C, w=W):
    k = ceil(F(w) / c)
    lines = ["| מטענים בתנועה | מעברים בכל ק\"מ | המחיר לק\"מ |", "|:-:|:-:|:-:|"]
    for j in range(k, 0, -1):
        lines.append(f"| {RLM}{j} | {RLM}{2 * j - 1} ({j} הלוך, {j - 1} חזור) | {RLM}{num(price(j, a))} ליטר |")
    return "\n".join(lines)


def stops_table(a=A, c=C, w=W, T=T):
    lines = ["| קטע | מטענים | אורך הקטע | מסתיים ב- | מים בתנועה בסופו |", "|:-:|:-:|:-:|:-:|:-:|"]
    segs = segments(a, c, w, T)
    for i, (x0, x1, j, n0, n1) in enumerate(segs, 1):
        last = i == len(segs)
        where = f"{RLM}**{num(x1)} ק\"מ** (היעד)" if last else f"{RLM}**{num(x1)} ק\"מ**"
        lines.append(f"| {RLM}{i} | {RLM}{j} | {RLM}{num(n0 - n1)} / {num(price(j, a))} = {num(x1 - x0)} | {where} | {RLM}{'**' + num(n1) + '**' if last else num(n1)} |")
    return "\n".join(lines)


def walks_table(seg, a=A, c=C, w=W, T=T):
    """The walks of segment `seg` (1-based): a row per round trip, as the owner's write-up."""
    segs = segments(a, c, w, T)
    x0, x1, j, _, _ = segs[seg - 1]
    cost = a * (x1 - x0)
    lines = [f"| הליכה | מה הגמל עושה | במחסן {num(x0)} | במחסן {num(x1)} |", "|:-:|---|:-:|:-:|"]
    rows = [p for p in passes(a, c, w, T) if p["seg"] == seg - 1 and not p["back"]]
    for i, p in enumerate(rows, 1):
        d = p["depots"]
        keep = p["carry1"] - p["drop"]
        what = (f"{RLM}לוקח {num(p['carry0'])}, מגיע עם {num(p['carry1'])}, מוריד {num(p['drop'])}, חוזר עם {num(keep)}" if keep
                else f"{RLM}לוקח {num(p['carry0'])}, מגיע עם {num(p['carry1'])}, מוריד הכול")
        far = f"{RLM}**{num(d[seg])}**" if i == len(rows) else f"{RLM}{num(d[seg])}"
        lines.append(f"| {RLM}{i} | {what} | {RLM}{num(d[seg - 1])} | {far} |")
    return "\n".join(lines)


EXAMPLES = [(F(1, 2), 150, 450, 30), (F(1, 2), 150, 450, 0), (F(1, 2), 150, 250, 30), (F(1, 2), 150, 150, 30),
            (F(1, 2), 150, 600, 150), (1, 100, 1000, 0), (F(1, 5), 300, 3000, 200), (1, 100, 1000, 50)]


def examples_table():
    lines = ["| ‏a | ‏c | ‏w | ‏T | ‏k | ‏r | המרחק המקסימלי | העצירות | מעברים |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|:-:|"]
    for a, c, w, T in EXAMPLES:
        k = ceil(F(w) / c)
        r = w - (k - 1) * c
        st = stops(a, c, w, T)
        shown = ", ".join(num(x) for x in st) if len(st) <= 4 else ", ".join(num(x) for x in st[:3]) + ", …"
        lines.append(f"| {RLM}{num(a)} | {RLM}{c} | {RLM}{w:,} | {RLM}{T} | {RLM}{k} | {RLM}{r} | {RLM}**{num(distance(a, c, w, T))}** | {RLM}{shown or '—'} | {RLM}{len(passes(a, c, w, T))} |")
    return "\n".join(lines)


APPROX_NS = [1, 2, 3, 5, 10, 20, 100]


def approx_table(a=A, c=C, T=T):
    lines = ["| מים בהתחלה w | מטענים n = w / c | המרחק המדויק | הקירוב | ההפרש |", "|:-:|:-:|:-:|:-:|:-:|"]
    for n in APPROX_NS:
        w = n * c
        exact, ap = distance(a, c, w, T), approx(a, c, w, T)
        lines.append(f"| {RLM}{w:,} | {RLM}{n} | {RLM}{num(exact)} | {RLM}{ap:,.1f} | {RLM}{float(exact) - ap:+.2f} |")
    return "\n".join(lines)


# --- the figures --------------------------------------------------------------------------

def chart_module():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from charts import Chart
    return Chart


def profile_chart(a=A, c=C, w=W, T=T):
    """The water in motion against the km: a line from w at 0 down to T at the end, one
    slope per segment (the price of its loads), the stops marked."""
    Chart = chart_module()
    segs = segments(a, c, w, T)
    d = segs[-1][1]
    cc = Chart(f"המים בתנועה לאורך הדרך : מ-{num(w)} ליטר ב-0 ל-{num(T)} ב-{num(d)} ק\"מ, קטע לכל מחיר",
               x_max=float(d), y_max=float(w), h=250, base=210)
    cc.grid_y([0, 150, 300, 450] if w == 450 else [0, float(w) / 2, float(w)])
    cc.grid_x([float(x1) for _, x1, *_ in segs[:-1]], labels=[""] * (len(segs) - 1), dashed=True)
    cc.x_ticks([0] + [float(x1) for _, x1, *_ in segs], labels=[num(0)] + [num(x1) for _, x1, *_ in segs])
    cc.hline(float(T), f"{num(T)} ליטר מגיעים ליעד", label_at="end")
    pts = [(0.0, float(w))] + [(float(x1), float(n1)) for _, x1, _, _, n1 in segs]
    cc.path(pts, "s1-line", width=2.5)
    for x0, x1, j, n0, n1 in segs:
        xm, ym = float(x0 + x1) / 2, float(n0 + n1) / 2
        cc.text(xm, ym, f"{num(price(j, a))} ליטר לק\"מ", dx=0, dy=-10, rtl=True)
    for x0, x1, j, n0, n1 in segs[:-1]:
        cc.dot(float(x1), float(n1), "s2", r=5, title=f"עצירה ב-{num(x1)} ק\"מ : נשארו {num(n1)} ליטר, {j - 1} מטענים")
    cc.dot(float(d), float(T), "ink", r=5, title=f"היעד ב-{num(d)} ק\"מ עם {num(T)} ליטר")
    cc.axis("ק\"מ")
    return cc.svg()


def profile_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>המים שעוד בתנועה (במחסן של תחילת הקטע ועל הגמל)</span>'
            '<span><i class="s2"></i>עצירה : מטען שלם נגמר והמחיר לק"מ יורד</span>'
            '<span><i class="ink"></i>היעד</span></span>')


def distance_chart(a=A, c=C, T=T, wmax=3000):
    """d_max against w from T to wmax: the exact curve (a kink at every multiple of c) and
    the logarithmic approximation dashed, the page's w marked."""
    Chart = chart_module()
    ws = sorted(set([T] + list(range(int(T), wmax + 1, 10)) + [j * c for j in range(1, wmax // c + 1)] + [wmax]))
    exact = [(w, float(distance(a, c, w, T))) for w in ws]
    ymax = exact[-1][1] * 1.08
    cc = Chart(f"המרחק המקסימלי לפי כמות המים בהתחלה, מ-{T} עד {wmax:,} ליטר, עם הקירוב הלוגריתמי",
               x_max=wmax, y_max=ymax, h=250, base=210)
    cc.grid_y([0, 200, 400, 600, 800])
    cc.grid_x([j * c for j in range(1, wmax // c + 1) if j in (1, 2, 3, 5, 10, 20)], labels=[""] * 6, dashed=True)
    cc.x_ticks([0, 450, 1000, 1500, 2000, 2500, 3000], labels=["0", "450", "1,000", "1,500", "2,000", "2,500", "3,000"])
    ap = [(w, approx(a, c, w, T)) for w in ws if w >= c]
    cc.path(ap, "ink-line", width=1.5, extra=' stroke-dasharray="6 4"')
    cc.path(exact, "s1-line", width=2.5)
    cc.dot(W, float(distance(a, c, W, T)), "s2", r=5, title=f"{W} ליטר : {num(distance(a, c, W, T))} ק\"מ")
    cc.axis("ליטר בהתחלה")
    return cc.svg()


def distance_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>המרחק המדויק (שבר בכל כפולה של 150)</span>'
            '<span><i class="ink-dash"></i>הקירוב 150 (ln n + 1.96) − 60</span>'
            '<span><i class="s2"></i>סעיף א : 450 ליטר, 400 ק"מ</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [price_table(), stops_table(), walks_table(1), walks_table(2), profile_chart(), profile_legend(),
            examples_table(), distance_chart(), distance_legend(), approx_table()]


if __name__ == "__main__":
    print(distance(A, C, W, T), stops(A, C, W, T), formula(A, C, W, T), len(passes(A, C, W, T)), walked(A, C, W, T))
    print("\n\n".join(blocks()))
