#!/usr/bin/env python3
"""Figures and tables of question 0096, the Kelly criterion.

    python tools/figures/fill.py 96        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The growth rates are floats of the formulas below; the bets of the race are
exact fractions. The question's test checks them against the page's code. Colours come
from the site's chart classes (s1 for the best fraction and its curve, s2 for the line
W0 e^(g t) and for "the wealth shrinks", s3 for half Kelly, ink for the median).
"""

import math
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

NB = " "
RLM = "‏"
P0, W0, ROUNDS = 0.6, 100, 100


def growth(f, p, a=1.0, b=1.0):
    """The growth rate per round: p ln(1 + a f) + q ln(1 - b f); -inf when a loss ruins."""
    q = 1 - p
    if b * f >= 1:
        return -math.inf if q > 0 else p * math.log1p(a * f)
    return p * math.log1p(a * f) + (q * math.log1p(-b * f) if q else 0.0)


def best(p, a=1, b=1):
    """The Kelly fraction, exact: p/b - q/a when p a > q b, else 0."""
    p, a, b = Fr(p), Fr(a), Fr(b)
    q = 1 - p
    return p / b - q / a if p * a > q * b else Fr(0)


def zero_root(p, lo, hi=1.0):
    """The fraction above lo where the growth falls back to 0 (even odds), by bisection."""
    hi = hi - 1e-15
    for _ in range(200):
        mid = (lo + hi) / 2
        if growth(mid, p) > 0:
            lo = mid
        else:
            hi = mid
    return lo


F_ZERO = zero_root(P0, 0.2)


def race(probs, odds):
    """Kelly's bets on a race with cash kept: (cash, bets), exact."""
    probs, odds = [Fr(x) for x in probs], [Fr(x) for x in odds]
    order = sorted(range(len(probs)), key=lambda i: probs[i] * odds[i], reverse=True)
    chosen, reserve = [], Fr(1)
    for i in order:
        if probs[i] * odds[i] <= reserve:
            break
        chosen.append(i)
        reserve = (1 - sum(probs[j] for j in chosen)) / (1 - sum(1 / odds[j] for j in chosen))
    bets = [Fr(0)] * len(probs)
    for i in chosen:
        bets[i] = probs[i] - reserve / odds[i]
    return reserve, bets


def race_growth(cash, bets, probs, odds):
    return sum(float(p) * math.log(float(cash + o * b)) for p, o, b in zip(probs, odds, bets) if p)


def num(x, fmt="{:g}"):
    """A number for a right-to-left cell: a negative one isolated left to right, with a true
    minus sign (a hyphen would be laid out after the digits)."""
    s = fmt.format(abs(float(x)))
    return f'{RLM}<span dir="ltr">−{s}</span>' if float(x) < 0 else s


def pct(x):
    v = float(x) * 100
    return f"{v:.1f}%" if abs(v - round(v)) > 1e-9 else f"{round(v)}%"


# --- part a: the curve g(f) ------------------------------------------------------------------------

def curve_figure():
    label = ("קצב הגדילה לסיבוב g(f) במטבע של 0.6 עם תשלום 1:1, כשמהמרים על חלק f מההון. השיא "
             f"ב-f = 0.2, כ-0.0201 לסיבוב. חצי מזה, 0.1, נותן 0.0150. מעל {F_ZERO:.3f} הקצב שלילי")
    c = Chart(label, x_max=0.5, y_min=-0.04, y_max=0.025, h=260, base=222)
    c.grid_y([-0.04, -0.02, 0, 0.02], fmt="{:g}")
    c.hline(0, None, cls="ink-line", width=1.5, dash="")
    pts = [(i / 500, growth(i / 500, P0)) for i in range(0, 251)]
    c.path(pts, "s1-line", width=2.5)
    c.vline(0.2, growth(0.2, P0))
    c.dot(0.2, growth(0.2, P0), "s1", label="f* = 0.2", dy=-10)
    c.dot(0.1, growth(0.1, P0), "s3", label="0.1", dy=-10)
    c.dot(F_ZERO, 0, "s2", label=f"{F_ZERO:.3f}", dy=-10)
    c.x_ticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], labels=["0", "0.1", "0.2", "0.3", "0.4", "0.5"])
    c.axis("f")
    legend = ('<span class="viz-legend"><span><i class="s1"></i><span>‏<span dir="ltr">g(f)</span>, והשיא ב-<span dir="ltr">f* = 0.2</span></span></span>'
              '<span><i class="s3"></i><span>חצי Kelly, <span dir="ltr">f = 0.1</span></span></span>'
              f'<span><i class="s2"></i><span>הקצב חוזר ל-0 ב-<span dir="ltr">f ≈ {F_ZERO:.3f}</span></span></span></span>')
    return f'<div class="ky-fig">{c.svg()}</div>\n\n{legend}'


# --- part a: paths and the table of strategies -------------------------------------------------------

PATHS, PATH_SEED = 12, 96


def wealth_paths(f, p, rounds, n, w0=W0, seed=PATH_SEED):
    """n paths of the wealth after every round; the draws are those of the page's simulate()."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        w, path = w0, [w0]
        for _ in range(rounds):
            w *= 1 + f if rnd.random() < p else 1 - f
            path.append(w)
        out.append(path)
    return out


def paths_figure():
    paths = wealth_paths(0.2, P0, ROUNDS, PATHS)
    finals = sorted(p[-1] for p in paths)
    label = (f"{PATHS} מסלולים של ההון מ-100, ב-f = 0.2 לאורך 100 סיבובים, בסקאלה לוגריתמית. הקו המקווקו "
             f"הוא 100 כפול e בחזקת 0.0201 t, ומגיע ל-749 אחרי 100 סיבובים. המסלולים מסתיימים בין "
             f"{finals[0]:.0f} ל-{finals[-1]:.0f}")
    c = Chart(label, x_max=ROUNDS, y_min=10, y_max=100000, log=True, h=260, base=222)
    c.grid_y([10, 100, 1000, 10000, 100000], labels=["10", "100", "1,000", "10⁴", "10⁵"])
    for path in paths:
        c.path(list(enumerate(path)), "ky-path", width=1.5)
    c.path([(t, W0 * math.exp(growth(0.2, P0) * t)) for t in range(0, ROUNDS + 1, 5)], "s2-line", width=2.5,
           extra=' stroke-dasharray="7 5"')
    c.dot(ROUNDS, W0 * math.exp(growth(0.2, P0) * ROUNDS), "s2", label="749", dx=-18, dy=-8)
    c.x_ticks([0, 20, 40, 60, 80, 100])
    c.axis("t")
    legend = ('<span class="viz-legend"><span><i class="ky-key-path"></i><span>מסלול אחד של ההון</span></span>'
              '<span><i class="s2"></i><span>‏<span dir="ltr">100 · e^(0.0201 t)</span>, הקצב <span dir="ltr">g(0.2)</span></span></span></span>')
    return f'<div class="ky-fig">{c.svg()}</div>\n\n{legend}'


F_ROWS = [0.05, 0.1, 0.2, 0.3, None, 0.5, 1.0]     # None: the zero root


def big(x):
    """A large number in words of digits: 8.3 · 10^9 as math."""
    e = int(math.floor(math.log10(x)))
    return f"{RLM}\\( {x / 10 ** e:.1f} \\cdot 10^{{{e}}} \\)"


def strategy_table():
    rows = ["| ‏f | ‏<span dir=\"ltr\">g(f)</span> לסיבוב | ההון החציוני אחרי 100 | ההון הממוצע אחרי 100 |", "|:-:|:-:|:-:|:-:|"]
    for f in F_ROWS:
        name = f"{F_ZERO:.3f}" if f is None else f"{f:g}"
        f = F_ZERO if f is None else f
        mean = W0 * (1 + (2 * P0 - 1) * f) ** ROUNDS
        if f >= 1:
            g, med = f"{RLM}\\( -\\infty \\)", "0"
        else:
            g = num(growth(f, P0), "{:.4f}")
            med = f"{W0 * (1 + f) ** 60 * (1 - f) ** 40:,.0f}" if f < 0.45 else f"{W0 * (1 + f) ** 60 * (1 - f) ** 40:.2f}"
        mean_s = f"{mean:,.0f}" if mean < 1e6 else big(mean)
        mark = "**" if f == 0.2 else ""
        rows.append(f"| {mark}{name}{mark} | {mark}{g}{mark} | {mark}{med}{mark} | {mark}{mean_s}{mark} |")
    return "\n".join(rows)


# --- part b: any p, even odds ----------------------------------------------------------------------

PB_ROWS = [Fr(1, 2), Fr(51, 100), Fr(11, 20), Fr(3, 5), Fr(7, 10), Fr(4, 5), Fr(9, 10)]


def even_table():
    rows = ["| ‏p | ‏<span dir=\"ltr\">f* = 2p − 1</span> | ‏<span dir=\"ltr\">g(f*)</span> לסיבוב | סיבובים עד הכפלה |", "|:-:|:-:|:-:|:-:|"]
    for p in PB_ROWS:
        f = best(p)
        g = growth(float(f), float(p))
        dbl = "אין גדילה" if g <= 0 else f"{math.log(2) / g:,.1f}"
        mark = "**" if p == Fr(3, 5) else ""
        rows.append(f"| {mark}{float(p):g}{mark} | {mark}{float(f):g}{mark} | {mark}{g:.4f}{mark} | {mark}{dbl}{mark} |")
    return "\n".join(rows)


# --- part c: a win of a, a loss of b --------------------------------------------------------------

PC_ROWS = [(Fr(3, 5), 1, 1), (Fr(2, 5), 3, 1), (Fr(1, 2), 1, Fr(1, 2)), (Fr(1, 4), 5, 1), (Fr(3, 10), 2, 1),
           (Fr(3, 5), 1, Fr(1, 4))]


def ab_table():
    rows = ["| ‏p | ‏a | ‏b | ‏<span dir=\"ltr\">pa − qb</span> | ‏<span dir=\"ltr\">f*</span> | ‏<span dir=\"ltr\">g(f*)</span> לסיבוב |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for p, a, b in PC_ROWS:
        p, a, b = Fr(p), Fr(a), Fr(b)
        edge = p * a - (1 - p) * b
        f = best(p, a, b)
        if f == 0:
            fs, gs = "לא מהמרים", "0"
        else:
            fs = f"{float(f):g}"
            gs = f"{growth(float(f), float(p), float(a), float(b)):.4f}"
            if f > 1:
                fs = f"{RLM}{fs}, יותר מההון"
        mark = "**" if (p, a, b) == (Fr(2, 5), 3, 1) else ""
        rows.append(f"| {mark}{float(p):g}{mark} | {mark}{float(a):g}{mark} | {mark}{float(b):g}{mark} | "
                    f"{mark}{num(edge)}{mark} | {mark}{fs}{mark} | {mark}{gs}{mark} |")
    return "\n".join(rows)


# --- part d: the race ------------------------------------------------------------------------------

RACE_P = [Fr(1, 2), Fr(3, 10), Fr(3, 20), Fr(1, 20)]
RACE_O = [Fr(11, 5), Fr(7, 2), Fr(5), Fr(10)]


def race_table():
    cash, bets = race(RACE_P, RACE_O)
    rows = ["| הסוס | ‏p | יחס התשלום o | ‏p · o | הכול על הסוסים, <span dir=\"ltr\">b = p</span> | עם מזומן (Kelly) |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i, (p, o, b) in enumerate(zip(RACE_P, RACE_O, bets), 1):
        rows.append(f"| {i} | {float(p):g} | {float(o):g} | {float(p * o):g} | {pct(p)} | {pct(b) if b else '0'} |")
    rows.append(f"| מזומן | | | | 0 | {pct(cash)} |")
    g_all = race_growth(0, RACE_P, RACE_P, RACE_O)
    g_kelly = race_growth(cash, bets, RACE_P, RACE_O)
    rows.append(f"| **‏g לסיבוב** | | | | **{num(g_all, '{:.4f}')}** | **{num(g_kelly, '{:.4f}')}** |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [curve_figure(), strategy_table(), paths_figure(), even_table(), ab_table(), race_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
