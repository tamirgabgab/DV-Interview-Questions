#!/usr/bin/env python3
"""Figures and tables of question 0060 (the three-wizard duel with the cat rule).

    python tools/figures/fill.py 60        # put the blocks on the page

The reference here is independent of the page code: the first round is solved by backward
induction with exact fractions, every option of every wizard kept, so the tables can show
the value of each option. Turn order 1 -> 2 -> 3; if all three are alive after wizard 3's
first turn, all three lose. After the first death the two survivors duel to the end, and
the survivor moves first (it is next in turn after the killer). A limit from below (a wand
"just under" a rival) is taken as the value at x - 10^-18, which agrees with the exact limit
to far more than the three places shown.

blocks() returns, in page order: the decision table of part a, the part a chart and its
legend, the decision tables of parts b and c, the chart of the three positions, its legend
and its table, the table of part d, and the part d chart with its legend. tests/0060 checks
the page's numbers and code against this module.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

RLM = "‏"
EPS = Fr(1, 10**18)
HALF = Fr(1, 2)
RIVALS = (Fr(6, 10), Fr(8, 10))        # parts a to c: the rivals in turn order
RIVALS_D = (Fr(8, 10), Fr(4, 10))      # part d


# --- the model --------------------------------------------------------------------------

def F(x, y):
    """The opener of a duel to the end wins (opener x, second y)."""
    return x / (x + y - x * y)


def G(x, y):
    """The second wizard of the duel wins."""
    return (1 - x) * y / (x + y - x * y)


def round_options(p):
    """Backward induction over the first round. p = [p1, p2, p3] in turn order.

    Returns (values, trace): the win chances of the three wizards from the first turn, and
    for each wizard in turn (3, 2, 1) a dict option -> own value, with the option taken.
    Options are the target 1, 2, 3 or "air". Ties keep the air, then the lower target."""
    after = [Fr(0)] * 3                         # nobody hit in the round: three cats
    trace = []
    for w in (2, 1, 0):
        opts = {"air": after}
        for t in range(3):
            if t == w:
                continue
            o = 3 - w - t                       # the survivor moves next and opens the duel
            hit = [Fr(0)] * 3
            hit[o], hit[w] = F(p[o], p[w]), G(p[o], p[w])
            opts[t + 1] = [p[w] * h + (1 - p[w]) * a for h, a in zip(hit, after)]
        best = "air"
        for k in (1, 2, 3):
            if k in opts and opts[k][w] > opts[best][w]:
                best = k
        trace.append((w + 1, {k: v[w] for k, v in opts.items()}, best))
        after = opts[best]
    return after, trace


def place(me, own, rivals):
    """The three chances with my wand `own` at position `me` (1..3), rivals in turn order."""
    p = list(rivals)
    p.insert(me - 1, own)
    return p


def win(me, own, rivals):
    return round_options(place(me, own, rivals))[0][me - 1]


def weak(rivals):
    """A wand just under the weaker rival."""
    return min(rivals) - EPS


def candidates(me, rivals):
    """(name, wand, chance) of the weak wand, the sniper and, when it applies, 0.5-."""
    out = [("weak", weak(rivals), win(me, weak(rivals), rivals)), ("sniper", Fr(1), win(me, Fr(1), rivals))]
    if me == 3 and min(rivals) > HALF:
        out.append(("half", HALF - EPS, win(me, HALF - EPS, rivals)))
    return out


def best_on_grid(me, rivals, n=1000):
    """The best chance over the wands k/n and the points just under the rivals and 0.5."""
    pts = [Fr(k, n) for k in range(1, n + 1)] + [r - EPS for r in rivals] + [HALF - EPS]
    return max((win(me, q, rivals), q) for q in pts)


# --- tables -------------------------------------------------------------------------------

def pct(v):
    return f"{float(v) * 100:.1f}%"


def num(v):
    return f"{float(v):.3f}"


def decision_table(me, rivals):
    """Per strategy, the wizards in backward order with the value of each option to the
    wizard in turn; the option taken in bold."""
    head = "| התור | על 1 | על 2 | על 3 | באוויר | הבחירה |"
    lines = [head, "|---|:-:|:-:|:-:|:-:|:-:|"]
    for label, own in (("חלש", weak(rivals)), ("צלף", Fr(1))):
        _, trace = round_options(place(me, own, rivals))
        for w, opts, best in trace:
            who = f"קוסם {w}" + (" (אני)" if w == me else "")
            cells = []
            for k in (1, 2, 3, "air"):
                if k not in opts:
                    cells.append("—")
                else:
                    s = f"{RLM}{num(opts[k])}"
                    cells.append(f"**{s}**" if k == best else s)
            choice = "באוויר" if best == "air" else f"על {best}"
            lines.append(f"| {label} · {who} | " + " | ".join(cells) + f" | {choice} |")
    return "\n".join(lines)


def positions_table(rivals):
    lines = ["| המיקום שלי | השרביט החלש | הצלף | הבחירה |", "|---|:-:|:-:|:-:|"]
    names = {1: "ראשון", 2: "שני", 3: "שלישי"}
    for me in (1, 2, 3):
        p = place(me, Fr(0), rivals)
        who = ", ".join(f"קוסם {i + 1} = {float(p[i]):g}" for i in range(3) if i != me - 1)
        c = {n: v for n, _, v in candidates(me, rivals)}
        m = float(min(rivals))
        choice = f"{RLM}{m:g}⁻" if c["weak"] >= c["sniper"] else f"{RLM}1"
        w, s = f"{RLM}{pct(c['weak'])}", f"{RLM}{pct(c['sniper'])}"
        w, s = (f"**{w}**", s) if c["weak"] >= c["sniper"] else (w, f"**{s}**")
        lines.append(f"| {names[me]} ({who}) | {w} | {s} | {choice} |")
    return "\n".join(lines)


# --- charts -------------------------------------------------------------------------------

def curve(me, rivals, n=200):
    """Pieces of the chance against my wand, split where it jumps (at a rival or 0.5)."""
    breaks = sorted({float(r) for r in rivals} | ({0.5} if me == 3 else set()))
    xs = sorted({k / n for k in range(1, n + 1)} | {b - 1e-6 for b in breaks} | {b + 1e-6 for b in breaks if b < 1})
    pieces, cur, prev = [], [], None
    for x in xs:
        v = float(win(me, Fr(x), rivals))
        if prev is not None and abs(v - prev) > 0.04:      # a jump: a decision changed
            pieces.append(cur)
            cur = []
        cur.append((x, v))
        prev = v
    pieces.append(cur)
    return pieces


STYLE = {1: ("s1-line", ""), 2: ("s2-line", ' stroke-dasharray="7 5"'), 3: ("ink-line", "")}
NAME = {1: "ראשון", 2: "שני", 3: "שלישי"}


def chart(positions, rivals, label, y_max=0.8):
    c = Chart(label, x_max=1, y_max=y_max, h=250, base=216)
    c.grid_y([k / 10 for k in range(0, int(y_max * 10) + 1, 2)], labels=[f"{k * 10}%" for k in range(0, int(y_max * 10) + 1, 2)])
    c.grid_x([0, 0.2, 0.4, 0.6, 0.8, 1])
    for me in positions:
        cls, extra = STYLE[me]
        for piece in curve(me, rivals):
            c.path(piece, cls, width=2.5, extra=extra)
    for me in positions:
        cand = max(candidates(me, rivals), key=lambda t: t[2])
        cls = {1: "s1", 2: "s2", 3: "ink"}[me]
        x = float(cand[1])
        c.dot(x, cand[2], cls, title=f"{NAME[me]}: {pct(cand[2])} at {x:.3g}")
    c.axis()
    return c.svg()


def legend(positions):
    keys = {1: '<i class="s1"></i>', 2: '<i class="s2"></i>', 3: '<i class="ink"></i>'}
    items = "".join(f"<span>{keys[me]}אני {NAME[me]}</span>" for me in positions)
    return f'<span class="viz-legend">{items}<span>הנקודה\u00a0: הסיכוי הטוב ביותר; הציר האופקי\u00a0: השרביט שלי</span></span>'


def chart_a():
    return chart([1], RIVALS, "הסיכוי שלי לנצח כפונקציה של השרביט, כשאני ראשון והיריבים 0.6 ו-0.8 : עולה עד 63.7% ממש לפני 0.6, צונח, ועולה שוב עד 40% ב-1")


def chart_abc():
    return chart([1, 2, 3], RIVALS, "הסיכוי שלי לנצח כפונקציה של השרביט בשלושת המיקומים, היריבים 0.6 ואחריו 0.8")


def chart_d():
    return chart([1, 2, 3], RIVALS_D, "הסיכוי שלי לנצח כפונקציה של השרביט בשלושת המיקומים, היריבים 0.8 ואחריו 0.4", y_max=0.6)


def blocks():
    """The generated blocks, in page order."""
    return [
        decision_table(1, RIVALS), chart_a(), legend([1]),
        decision_table(2, RIVALS), decision_table(3, RIVALS),
        chart_abc(), legend([1, 2, 3]), positions_table(RIVALS),
        positions_table(RIVALS_D), chart_d(), legend([1, 2, 3]),
    ]


if __name__ == "__main__":
    for me in (1, 2, 3):
        for rv in (RIVALS, RIVALS_D):
            print(me, [float(x) for x in rv], [(n, float(q), float(v)) for n, q, v in candidates(me, rv)])
    print("\n\n".join(blocks()))
