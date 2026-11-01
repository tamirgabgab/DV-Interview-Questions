#!/usr/bin/env python3
"""Figures and tables of question 0071 (the three-wizard duel with the cat rule).

    python tools/figures/fill.py 71        # put the blocks on the page

The reference here is independent of the page code: the first round is solved by backward
induction with exact fractions, every option of every wizard kept, so the tables can show
the value of each option. Turn order 1 -> 2 -> 3; if all three are alive after wizard 3's
first turn, all three lose. After the first death the two survivors duel to the end, and
the survivor moves first (it is next in turn after the killer). A limit from below (a wand
"just under" a rival) is taken as the value at x - 10^-18, which agrees with the exact limit
to far more than the three places shown.

blocks() returns, in page order: for parts a, b and c the table of my chance per wand (with
the sum over the ways the round ends), the rivals' check at a wand of 0.59 and who wins in
the end (part a also its chart and legend; part c then the chart of the three positions,
its legend and its table); for part d the table of the positions, my chance per wand in the
three positions, the chart with its legend, the rivals' check at 0.39 and who wins.
tests/0071 checks the page's numbers against this module.
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


def positions_table(rivals):
    lines = ["| המיקום שלי | השרביט החלש | הצלף | הבחירה |", "|---|:-:|:-:|:-:|"]
    names = {1: "ראשון", 2: "שני", 3: "שלישי"}
    for me in (1, 2, 3):
        p = place(me, Fr(0), rivals)
        who = ", ".join(f"קוסם {i + 1} = {float(p[i]):g}" for i in range(3) if i != me - 1)
        c = {n: v for n, _, v in candidates(me, rivals)}
        m = float(min(rivals))
        choice = f"{RLM}\\( {m:g}^- \\)" if c["weak"] >= c["sniper"] else f"{RLM}1"
        w, s = f"{RLM}{pct(c['weak'])}", f"{RLM}{pct(c['sniper'])}"
        w, s = (f"**{w}**", s) if c["weak"] >= c["sniper"] else (w, f"**{s}**")
        lines.append(f"| {names[me]} ({who}) | {w} | {s} | {choice} |")
    return "\n".join(lines)


def short(v):
    """A probability with up to three places and no trailing zeros: 0.6, 0.32, 0.714."""
    s = f"{float(v):.3f}".rstrip("0").rstrip(".")
    return s if s else "0"


def outcomes(p):
    """The first round played with everyone's best choice: the list of (killer, victim,
    chance) of the ways it can end in a duel (wizards 0..2), and the chance of three cats."""
    _, trace = round_options(p)
    choice = {w - 1: best for w, _, best in trace}
    out, alive = [], Fr(1)
    for w in (0, 1, 2):
        t = choice[w]
        if t == "air":
            continue
        out.append((w, t - 1, alive * p[w]))
        alive *= 1 - p[w]
    return out, alive


def wand_label(q):
    """0.6- for a wand just under a round number, else the number."""
    if ((q + EPS) * 100).denominator == 1 and (q * 100).denominator != 1:
        return f"{RLM}\\( {float(q + EPS):g}^- \\)"
    return f"{RLM}{float(q):g}"


def my_choice(me, p):
    _, trace = round_options(p)
    best = {w: b for w, _, b in trace}[me]
    return "באוויר" if best == "air" else f"על קוסם {best}"


def wand_table(me, rivals, wands):
    """Per wand: what I do in my first turn, my chance as a sum over the ways the round ends
    (the chance of the way times my chance in the duel that follows), and the total."""
    lines = ["| השרביט שלי | מה אני עושה | החישוב | הסיכוי שלי |", "|:-:|:-:|:-:|:-:|"]
    rows = []
    for q in wands:
        p = place(me, q, rivals)
        ways, _ = outcomes(p)
        terms = []
        for k, v, pr in ways:
            s = 3 - k - v
            mine = F(p[s], p[k]) if s == me - 1 else G(p[s], p[k]) if k == me - 1 else None
            if mine is not None:
                terms.append(f"{short(pr)} \\cdot {short(mine)}")
        calc = f"\\( {' + '.join(terms)} \\)" if terms else "‏0"
        rows.append((q, my_choice(me, p), calc, win(me, q, rivals)))
    top = max(r[3] for r in rows)
    for q, what, calc, v in rows:
        val = f"{RLM}{num(v)}"
        lines.append(f"| {wand_label(q)} | {what} | {RLM}{calc} | " + (f"**{val}**" if v == top else val) + " |")
    return "\n".join(lines)


def name(w, me, case=""):
    """Wizard w (0..2) in a sentence: "אני" or "קוסם 3"; with case "ב" the victim form."""
    if w == me - 1:
        return "בי" if case == "ב" else "אני"
    return f"{case}קוסם {w + 1}"


def who_wins(me, own, rivals):
    """Each wizard's chance to win from the start, with the ways it happens; and the cats."""
    p = place(me, own, rivals)
    ways, cats = outcomes(p)
    lines = ["| מי | איך | הסיכוי |", "|---|---|:-:|"]
    order = [me - 1] + [w for w in range(3) if w != me - 1]
    for w in order:
        how, total = [], Fr(0)
        for k, v, pr in ways:
            s = 3 - k - v
            if w == k:
                q = G(p[s], p[k])
                how.append(f"פוגע {name(v, me, 'ב')} ({short(pr)}), ומנצח כשני בדו-קרב ({short(q)})")
            elif w == s:
                q = F(p[s], p[k])
                who = "אני" if w == me - 1 else "הוא"
                how.append(f"{name(k, me)} פוגע {name(v, me, 'ב')} ({short(pr)}), ו{who} פותח את הדו-קרב ומנצח ({short(q)})")
            else:
                continue
            total += pr * q
        label = "**אני**" if w == me - 1 else f"**קוסם {w + 1}**"
        lines.append(f"| {label} | {'; או '.join(how) if how else 'אף מסלול'} | {RLM}{pct(total)} |")
    lines.append(f"| **כולם חתולים** | אף אחד לא נפגע בסבב הראשון | {RLM}{pct(cats)} |")
    return "\n".join(lines)


def check_rows(me, own, rivals, prefix=""):
    """The rivals' rows of the first round at my wand: each one's own chance when it aims
    at me, at the other rival or at the air, and its choice."""
    p = place(me, own, rivals)
    _, trace = round_options(p)
    rows = []
    for w, opts, best in trace:
        if w == me:
            continue
        other = 6 - w - me
        cells = []
        for k in (me, other, "air"):
            s = f"{RLM}{num(opts[k])}"
            cells.append(f"**{s}**" if k == best else s)
        choice = "באוויר" if best == "air" else ("עליי" if best == me else f"על קוסם {best}")
        rows.append(f"| {prefix}קוסם {w} ({float(p[w - 1]):g}) | " + " | ".join(cells) + f" | {choice} |")
    return rows


CHECK_HEAD = ["| הקוסם | מכשף עליי | מכשף על היריב השני | באוויר | הבחירה |", "|---|:-:|:-:|:-:|:-:|"]


def check_table(me, own, rivals):
    return "\n".join(CHECK_HEAD + check_rows(me, own, rivals))


def check_table_d(own):
    rows = []
    for me in (1, 2, 3):
        rows += check_rows(me, own, RIVALS_D, f"{NAME[me]} · ")
    return "\n".join(CHECK_HEAD + rows)


def wand_table_d(wands):
    """Part d: my chance per wand in the three positions, the best of each position in bold."""
    lines = ["| השרביט שלי | ראשון | שני | שלישי |", "|:-:|:-:|:-:|:-:|"]
    vals = {me: [win(me, q, RIVALS_D) for q in wands] for me in (1, 2, 3)}
    for i, q in enumerate(wands):
        cells = []
        for me in (1, 2, 3):
            v = vals[me][i]
            s = f"{RLM}{num(v)}"
            cells.append(f"**{s}**" if v == max(vals[me]) else s)
        lines.append(f"| {wand_label(q)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def who_wins_d():
    """Part d: the chance of each wizard to win, with my best wand in each position."""
    lines = ["| מי | ראשון | שני | שלישי |", "|---|:-:|:-:|:-:|"]
    rows = {"me": [], "strong": [], "weak": [], "cats": []}
    for me in (1, 2, 3):
        own = max(candidates(me, RIVALS_D), key=lambda t: t[2])[1]
        p = place(me, own, RIVALS_D)
        chances = round_options(p)[0]
        _, cats = outcomes(p)
        others = [w for w in range(3) if w != me - 1]
        strong = max(others, key=lambda w: p[w])
        weak_w = min(others, key=lambda w: p[w])
        rows["me"].append(chances[me - 1])
        rows["strong"].append(chances[strong])
        rows["weak"].append(chances[weak_w])
        rows["cats"].append(cats)
    labels = {"me": "**אני**", "strong": "**היריב של 0.8**", "weak": "**היריב של 0.4**", "cats": "**כולם חתולים**"}
    for key, label in labels.items():
        lines.append(f"| {label} | " + " | ".join(f"{RLM}{pct(v)}" for v in rows[key]) + " |")
    return "\n".join(lines)


WANDS = [Fr(3, 10), Fr(5, 10), Fr(59, 100), Fr(6, 10) - EPS, Fr(7, 10), Fr(9, 10), Fr(1)]
WANDS_D = [Fr(2, 10), Fr(3, 10), Fr(39, 100), Fr(4, 10) - EPS, Fr(6, 10), Fr(9, 10), Fr(1)]
CHECK = Fr(59, 100)          # a concrete wand just under 0.6 for the checks of the rivals
CHECK_D = Fr(39, 100)


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
    weak_a = weak(RIVALS)
    return [
        wand_table(1, RIVALS, WANDS), chart_a(), legend([1]), check_table(1, CHECK, RIVALS), who_wins(1, weak_a, RIVALS),
        wand_table(2, RIVALS, WANDS), check_table(2, CHECK, RIVALS), who_wins(2, weak_a, RIVALS),
        wand_table(3, RIVALS, WANDS), check_table(3, CHECK, RIVALS), who_wins(3, weak_a, RIVALS),
        chart_abc(), legend([1, 2, 3]), positions_table(RIVALS),
        positions_table(RIVALS_D), wand_table_d(WANDS_D), chart_d(), legend([1, 2, 3]),
        check_table_d(CHECK_D), who_wins_d(),
    ]


if __name__ == "__main__":
    for me in (1, 2, 3):
        for rv in (RIVALS, RIVALS_D):
            print(me, [float(x) for x in rv], [(n, float(q), float(v)) for n, q, v in candidates(me, rv)])
    print("\n\n".join(blocks()))
