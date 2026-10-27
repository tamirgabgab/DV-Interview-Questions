#!/usr/bin/env python3
"""Figures and tables of question 0052 (the expected number of fair coin tosses until a
pattern such as HH or HT appears; any pattern; a race between two patterns).

    python tools/figures/fill.py 52        # put the blocks on the page

The reference here is independent of the page code (which uses Conway's correlation): a
Markov chain whose state is the longest suffix of the tosses that is a prefix of the
pattern, solved exactly with fractions; the distribution of the waiting time by dynamic
programming on the same chain; and the race of two patterns solved on the chain of the
last few tosses. blocks() returns, in page order: the state diagrams of HH and HT, their
legend, the chart and the table of P(T = t), the table of every pattern of length 3, and
the race table of length 3 (Penney's game).
"""

import sys
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

RLM = "‏"
HALF = Fr(1, 2)


# --- the model ---------------------------------------------------------------------------

def step(pattern, s, c):
    """The next state: the longest suffix of pattern[:s] + c that is a prefix of the pattern."""
    seen = pattern[:s] + c
    for k in range(min(len(seen), len(pattern)), -1, -1):
        if seen.endswith(pattern[:k]):
            return k
    return 0


def solve(rows):
    """Gaussian elimination over fractions: rows of [a_0 .. a_{n-1} | b]."""
    n = len(rows)
    rows = [r[:] for r in rows]
    for c in range(n):
        p = next(i for i in range(c, n) if rows[i][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        for i in range(n):
            if i != c and rows[i][c] != 0:
                f = rows[i][c] / rows[c][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[c])]
    return [rows[i][n] / rows[i][i] for i in range(n)]


def expected(pattern):
    """E[T] from state 0: E_s = 1 + (E_next(s, H) + E_next(s, T)) / 2, E_L = 0."""
    L = len(pattern)
    rows = []
    for s in range(L):
        row = [Fr(0)] * (L + 1)
        row[s] += 1
        for c in "HT":
            t = step(pattern, s, c)
            if t < L:
                row[t] -= HALF
        row[L] = Fr(1)
        rows.append(row)
    return solve(rows)[0]


def dist(pattern, tmax):
    """P(T = t) for t = 1..tmax, exactly."""
    L, now, out = len(pattern), {0: Fr(1)}, []
    for _ in range(tmax):
        nxt, hit = {}, Fr(0)
        for s, p in now.items():
            for c in "HT":
                t = step(pattern, s, c)
                if t == L:
                    hit += p * HALF
                else:
                    nxt[t] = nxt.get(t, Fr(0)) + p * HALF
        out.append(hit)
        now = nxt
    return out


def race(a, b):
    """P(a appears before b), on the chain of the last max(len) - 1 tosses."""
    K = max(len(a), len(b)) - 1
    states = [""] + ["".join(p) for k in range(1, K + 1) for p in product("HT", repeat=k)]
    idx = {s: i for i, s in enumerate(states)}
    rows = []
    for s in states:
        row = [Fr(0)] * (len(states) + 1)
        row[idx[s]] += 1
        for c in "HT":
            t = s + c
            if t.endswith(a):
                row[-1] += HALF
            elif t.endswith(b):
                pass
            else:
                row[idx[t[-K:] if K else ""]] -= HALF
        rows.append(row)
    return solve(rows)[0]


def overlaps(p):
    return [k for k in range(1, len(p) + 1) if p[-k:] == p[:k]]


# --- blocks ------------------------------------------------------------------------------

def chain_svg(pattern, y, mid):
    """One row of the state diagram: start, H, the pattern; the arrows and their tosses."""
    xs = [80, 270, 460]
    s = ""
    names = ["start", pattern[0], pattern]
    # forward arrows
    s += f'<line class="fs-edge" x1="{xs[0] + 26}" y1="{y}" x2="{xs[1] - 28}" y2="{y}" marker-end="url(#cp-arrow)"/>'
    s += f'<text class="fs-label halo" x="{(xs[0] + xs[1]) / 2}" y="{y - 8}" text-anchor="middle">H</text>'
    s += f'<line class="fs-edge is-found" x1="{xs[1] + 26}" y1="{y}" x2="{xs[2] - 28}" y2="{y}" marker-end="url(#cp-arrow)"/>'
    s += f'<text class="fs-label is-found halo" x="{(xs[1] + xs[2]) / 2}" y="{y - 8}" text-anchor="middle">{pattern[1]}</text>'
    # T keeps the start
    x = xs[0]
    s += f'<path class="fs-edge" d="M{x - 9},{y - 23} C{x - 30},{y - 64} {x + 30},{y - 64} {x + 9},{y - 24}" marker-end="url(#cp-arrow)"/>'
    s += f'<text class="fs-label halo" x="{x}" y="{y - 54}" text-anchor="middle">T</text>'
    other = "T" if pattern[1] == "H" else "H"
    x = xs[1]
    if step(pattern, 1, other) == 1:          # HT: an H after H keeps the H
        s += f'<path class="fs-edge" d="M{x - 9},{y - 23} C{x - 30},{y - 64} {x + 30},{y - 64} {x + 9},{y - 24}" marker-end="url(#cp-arrow)"/>'
        s += f'<text class="fs-label halo" x="{x}" y="{y - 54}" text-anchor="middle">H</text>'
    else:                                     # HH: a T after H goes back to the start
        s += f'<path class="fs-edge is-back" d="M{x},{y + 26} Q{(xs[0] + x) / 2},{y + 70} {xs[0]},{y + 28}" marker-end="url(#cp-arrow)"/>'
        s += f'<text class="fs-label halo" x="{(xs[0] + x) / 2}" y="{y + 62}" text-anchor="middle">T</text>'
    for i, x in enumerate(xs):
        cls = " is-start" if i == 0 else " is-out" if i == 2 else ""
        size = ' style="font-size:11px"' if i == 0 else ""
        s += f'<g class="fs-node{cls}"><circle cx="{x}" cy="{y}" r="26"/><text x="{x}" y="{y + 4}" text-anchor="middle"{size}>{names[i]}</text></g>'
    s += f'<text class="cp-exp" x="{600}" y="{y + 6}" text-anchor="middle">E = {mid}</text>'
    return s


def diagram():
    s = ('<svg class="figure cp-fig" viewBox="0 0 660 300" style="max-width:41rem" role="img" '
         'aria-label="שרשראות המצבים של HH ושל HT : שלושה מצבים כל אחת, החצים מסומנים בהטלה">'
         '<defs><marker id="cp-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    s += chain_svg("HT", 92, expected("HT"))
    s += chain_svg("HH", 222, expected("HH"))
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="fs-key"></i>מעבר : ההטלה</span>'
            '<span><i class="fs-key-found"></i>ההטלה שמשלימה את הרצף</span>'
            '<span><i class="cp-key-back"></i>HH : זנב אחרי H מחזיר להתחלה</span></span>')


TMAX = 16


def dist_chart():
    hh, ht = dist("HH", TMAX), dist("HT", TMAX)
    c = Chart("ההסתברות שהרצף מופיע לראשונה בהטלה t, ל-HT ול-HH : ל-HT שיא גבוה ב-2 ו-3 וזנב קצר, ל-HH זנב ארוך",
              slots=TMAX - 1, y_max=0.3, h=250, base=216)
    c.grid_y([0, 0.1, 0.2, 0.3])
    for t in range(2, TMAX + 1):
        x = t - 1
        c.add(f'<g transform="translate({-c.slot * 0.19:.1f},0)">')
        c.bar(x, ht[t - 1], "by-multiples", title=f"HT: P(T = {t}) = {ht[t - 1]}", frac=0.36)
        c.add('</g><g transform="translate(' + f"{c.slot * 0.19:.1f}" + ',0)">')
        c.bar(x, hh[t - 1], "by-enum", title=f"HH: P(T = {t}) = {hh[t - 1]}", frac=0.36)
        c.add("</g>")
    c.x_ticks(range(1, TMAX), labels=[str(t) for t in range(2, TMAX + 1)])
    c.axis("t")
    return c.svg()


def dist_legend():
    return ('<span class="viz-legend"><span><i class="by-multiples"></i>HT : ‏(t − 1) / 2^t</span>'
            '<span><i class="by-enum"></i>HH : ‏F(t − 1) / 2^t (פיבונאצ׳י)</span></span>')


def dist_table():
    hh, ht = dist("HH", 8), dist("HT", 8)
    rows = ["| ההטלה t | ‏P(T = t) ל-HT | ‏P(T = t) ל-HH |", "|:-:|:-:|:-:|"]
    for t in range(2, 9):
        rows.append(f"| {RLM}{t} | {RLM}{ht[t - 1]} | {RLM}{hh[t - 1]} |")
    return "\n".join(rows)


def patterns_table():
    rows = ["| הרצף | חפיפות עם עצמו (אורכים) | התוחלת |", "|:-:|:-:|:-:|"]
    for p in ("".join(t) for t in product("HT", repeat=3)):
        ov = overlaps(p)
        terms = " + ".join(str(2 ** k) for k in ov)
        rows.append(f"| {RLM}`{p}` | {RLM}{', '.join(map(str, ov))} | {RLM}{terms} = {expected(p)} |")
    return "\n".join(rows)


def best_reply(a):
    """The pattern of the same length that beats a most often, and its chance."""
    best = None
    for b in ("".join(t) for t in product("HT", repeat=len(a))):
        if b == a:
            continue
        p = 1 - race(a, b)
        if best is None or p > best[1]:
            best = (b, p)
    return best


def race_table():
    rows = ["| היריב בוחר | התשובה הטובה ביותר | הסיכוי שהתשובה מופיעה קודם |", "|:-:|:-:|:-:|"]
    for a in ("".join(t) for t in product("HT", repeat=3)):
        b, p = best_reply(a)
        rows.append(f"| {RLM}`{a}` | {RLM}`{b}` | {RLM}{p} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [diagram(), legend(), dist_chart(), dist_legend(), dist_table(), patterns_table(), race_table()]


if __name__ == "__main__":
    print(expected("HH"), expected("HT"), expected("HHH"), race("HH", "HT"), race("HHH", "THH"))
    print("\n\n".join(blocks()))
