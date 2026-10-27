#!/usr/bin/env python3
"""Figures and tables of question 0053 (a covergroup for an ALU: coverpoints, a cross with
ignored cells, and how many random transactions close it).

    python tools/figures/fill.py 53        # put the blocks on the page

The reference here is independent of the page code: the bins written from their
definitions, and the expected number of transactions until every cell of the cross is hit
computed exactly with fractions by inclusion-exclusion over the three kinds of cell (the
page integrates numerically). blocks() returns, in page order: the table of the bins, the
cross map figure with its legend, and the table of closure times for three stimulus
distributions. tests/0053 checks the page code and the covergroup itself (Verilator)
against these.
"""

import sys
from fractions import Fraction as Fr
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
OPS = ["ADD", "SUB", "AND", "OR", "SHL"]
CLASSES = ["zero", "max", "msb", "mid"]              # 0, 0xFF, 0x80, everything else
SHORT = {"zero": "0", "max": "FF", "msb": "80", "mid": "mid"}
CARRY_OPS = {"ADD", "SUB", "SHL"}


def value_class(v):
    return {0: "zero", 255: "max", 128: "msb"}.get(v, "mid")


def ignored(op, a_cls, b_cls):
    """SHL by 0x80 or 0xFF shifts everything out: those cells are ignored."""
    return op == "SHL" and b_cls in ("max", "msb")


CELLS = [(o, x, y) for o in OPS for x in CLASSES for y in CLASSES if not ignored(o, x, y)]


def bins_count():
    return {"cp_op": len(OPS), "cp_a": len(CLASSES), "cp_b": len(CLASSES), "cp_carry": 2, "x_op_a_b": len(CELLS)}


def coverage(samples):
    """The group's coverage in percent, the LRM way: the average of the five items, each the
    share of its bins hit. samples are (op, a, b, carry)."""
    hit = {k: set() for k in bins_count()}
    for op, a, b, carry in samples:
        xa, xb = value_class(a), value_class(b)
        hit["cp_op"].add(op)
        hit["cp_a"].add(xa)
        hit["cp_b"].add(xb)
        if op in CARRY_OPS:
            hit["cp_carry"].add(carry)
        if not ignored(op, xa, xb):
            hit["x_op_a_b"].add((op, xa, xb))
    n = bins_count()
    return 100 * sum(Fr(len(hit[k]), n[k]) for k in n) / len(n)


# --- closure time --------------------------------------------------------------------------

# the probability of each value class of a (and of b) under three stimulus distributions
DISTS = {
    "uniform": {"zero": Fr(1, 256), "max": Fr(1, 256), "msb": Fr(1, 256), "mid": Fr(253, 256)},
    "dist":    {"zero": Fr(1, 5), "max": Fr(1, 5), "msb": Fr(1, 5), "mid": Fr(2, 5)},
    "equal":   {"zero": Fr(1, 4), "max": Fr(1, 4), "msb": Fr(1, 4), "mid": Fr(1, 4)},
}


def cell_probs(dist):
    pa = DISTS[dist]
    return [Fr(1, len(OPS)) * pa[x] * pa[y] for _, x, y in CELLS]


def expected_closure(probs):
    """E[transactions until every cell is hit], exactly: the cells come in groups of equal
    probability, and E = sum over nonempty choices (j_g of each group) of
    (-1)^(J + 1) prod C(n_g, j_g) / sum j_g p_g."""
    groups = {}
    for p in probs:
        groups[p] = groups.get(p, 0) + 1
    items = list(groups.items())
    total = Fr(0)

    def rec(i, sign, mult, rate):
        nonlocal total
        if i == len(items):
            if rate:
                total += sign * mult / rate
            return
        p, n = items[i]
        for j in range(n + 1):
            rec(i + 1, sign * (-1) ** j, mult * comb(n, j), rate + j * p)

    rec(0, -1, 1, Fr(0))
    return total


# --- blocks ------------------------------------------------------------------------------

def bins_table():
    rows = ["| ה-coverpoint | ה-bins | כמה |", "|---|---|:-:|"]
    rows.append(f"| {RLM}`cp_op` | {RLM}ADD, ‏SUB, ‏AND, ‏OR, ‏SHL; ‏`illegal_bins` לקודים 5 עד 7 | {RLM}5 |")
    rows.append(f"| {RLM}`cp_a` | ‏zero ‏(0), ‏max ‏(0xFF), ‏msb ‏(0x80), ‏mid (כל השאר) | {RLM}4 |")
    rows.append(f"| {RLM}`cp_b` | כמו `cp_a` | {RLM}4 |")
    rows.append(f"| {RLM}`cp_carry` | ‏0 ו-1, רק כש-`op` הוא ADD, ‏SUB או SHL (‏`iff`) | {RLM}2 |")
    rows.append(f"| {RLM}`x_op_a_b` | ‏\\( 5 \\times 4 \\times 4 = 80 \\), פחות 8 תאים של SHL ב-0x80 או 0xFF | {RLM}{len(CELLS)} |")
    return "\n".join(rows)


def cross_figure():
    """The cross as five 4 x 4 maps (a down, b across), each cell shaded by its probability
    under uniform stimulus; the ignored cells hatched."""
    W, H, S, G = 660, 196, 26, 14
    s = (f'<svg class="figure cg-fig" viewBox="0 0 {W} {H}" style="max-width:41rem" role="img" '
         'aria-label="ה-cross של op, a ו-b : חמש מפות של 4 על 4, תאים נדירים כהים, ושמונה תאים של SHL מסומנים כמושמטים">'
         '<defs><pattern id="cg-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="6" class="cg-hatch-line"/></pattern></defs>')
    pa = DISTS["uniform"]
    x0 = 46
    for k, op in enumerate(OPS):
        gx = x0 + k * (4 * S + G)
        s += f'<text class="cg-op" x="{gx + 2 * S}" y="22" text-anchor="middle">{op}</text>'
        for i, xa in enumerate(CLASSES):
            for j, xb in enumerate(CLASSES):
                x, y = gx + j * S, 34 + i * S
                if ignored(op, xa, xb):
                    cls = "cg-cell is-ign"
                else:
                    rare = (xa != "mid") + (xb != "mid")
                    cls = f"cg-cell is-r{rare}"
                p = Fr(1, 5) * pa[xa] * pa[xb]
                s += f'<rect class="{cls}" x="{x}" y="{y}" width="{S - 2}" height="{S - 2}"><title>{op}, a {xa}, b {xb}: {"ignored" if ignored(op, xa, xb) else f"p = {p}"}</title></rect>'
        if k == 0:
            for i, xa in enumerate(CLASSES):
                s += f'<text class="tick" x="{gx - 6}" y="{34 + i * S + 17}" text-anchor="end">{SHORT[xa]}</text>'
        for j, xb in enumerate(CLASSES):
            s += f'<text class="tick" x="{gx + j * S + S / 2 - 1}" y="{34 + 4 * S + 14}" text-anchor="middle">{SHORT[xb]}</text>'
    s += f'<text class="legend" x="{W - 8}" y="{H - 8}" text-anchor="end">rows: a, columns: b</text>'
    return s + "</svg>"


def cross_legend():
    return ('<span class="viz-legend"><span><i class="cg-key-r2"></i>שני ערכי קצה : ‏1 ל-327,680</span>'
            '<span><i class="cg-key-r1"></i>ערך קצה אחד : ‏1 ל-1,295 בערך</span>'
            '<span><i class="cg-key-r0"></i>בלי ערכי קצה : ‏1 ל-5.1 בערך</span>'
            '<span><i class="cg-key-ign"></i>‏ignore_bins</span></span>')


def closure_table():
    names = {"uniform": "אחיד (‏`randomize` רגיל)", "dist": "‏`dist` : כל ערך קצה 1/5, השאר 2/5", "equal": "‏`dist` : כל מחלקה 1/4"}
    rows = ["| הגירוי | התא הנדיר ביותר | תוחלת הטרנזקציות עד שכל ה-cross מכוסה |", "|---|:-:|:-:|"]
    for d in ("uniform", "dist", "equal"):
        ps = cell_probs(d)
        e = expected_closure(ps)
        rows.append(f"| {names[d]} | {RLM}1/{1 / min(ps)} | {RLM}{float(e):,.0f} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [bins_table(), cross_figure(), cross_legend(), closure_table()]


if __name__ == "__main__":
    for d in DISTS:
        print(d, float(expected_closure(cell_probs(d))))
    print("\n\n".join(blocks()))
