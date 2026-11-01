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

blocks() returns, in page order: the Markov chain of the game in p1, p2, p3 and its legend;
part a (I am first against 0.6 then 0.8): my chance per wand (a sum over the ways the round
ends), its chart and legend, the rivals' check at a wand of 0.59, the chain with the numbers
of the best wand and its legend, and who wins in the end; part b (I choose my place, the
order and the wand): the six orders, my chance per wand in the winning order, its check, who
wins, and the chart of the three places with its legend; part c (any rivals a < b): the
threshold of the rule and the rule on example pairs. tests/0071 checks the page's numbers
against this module.
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
    """The best chance over the wands k/n and the points just under the rivals and 0.5. A
    wand exactly equal to a rival is left out: there a rival is indifferent and the tie rule,
    not the game, decides; the point just under it stands for that value."""
    pts = [Fr(k, n) for k in range(1, n + 1) if Fr(k, n) not in rivals] + [r - EPS for r in rivals] + [HALF - EPS]
    return max((win(me, q, rivals), q) for q in pts)




def orders(rivals):
    """Part b: my place (1..3) and the order of the two rivals around me. For each of the six
    orders: (p in turn order with my wand, me, my best wand, the chances of the three wizards,
    the cats). The rivals are given as a set; both orders of them are tried."""
    a, b = sorted(rivals)
    out = []
    for me in (1, 2, 3):
        for rv in ((a, b), (b, a)):
            v, q = best_on_grid(me, rv, 1000)
            p = place(me, q, rv)
            ch = round_options(p)[0]
            out.append((p, me, q, ch, outcomes(p)[1]))
    return out


# --- the general rule of part c (rivals a < b) --------------------------------------------

def hide_third(a, b):
    """The chances when I play third behind the weak rival a and then the strong b, with a
    wand just under a: (me, the weak rival, the strong rival, cats). The weak rival shoots at
    the strong one, the strong one at the weak one, I (if both missed) at the strong one;
    the survivor and I duel, the one who did not shoot opening."""
    me = a * F(a, a) + (1 - a) * b * F(a, b) + (1 - a) * (1 - b) * a * G(a, a)
    weak_w = a * G(a, a) + (1 - a) * (1 - b) * a * F(a, a)
    strong = (1 - a) * b * G(a, b)
    cats = (1 - a) * (1 - b) * (1 - a)
    return me, weak_w, strong, cats


def sniper_first(a, b):
    """A sniper playing first kills the strong rival; the weak one opens against it."""
    return 1 - a, a, Fr(0), Fr(0)


def threshold(b, steps=60):
    """The weak rival's chance a* below which the sniper beats hiding third, for a strong
    rival b (b = None: the two rivals equal)."""
    lo, hi = 0.3, 0.5
    for _ in range(steps):
        m = (lo + hi) / 2
        bb = Fr(m) if b is None else b
        if hide_third(Fr(m), bb)[0] > 1 - Fr(m):
            hi = m
        else:
            lo = m
    return lo


# --- tables -------------------------------------------------------------------------------

def pct(v):
    return f"{float(v) * 100:.1f}%"


def num(v):
    return f"{float(v):.3f}"


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
        label = "**אני**" if w == me - 1 else f"**קוסם {w + 1}** ({float(p[w]):g})"
        lines.append(f"| {label} | {'; או '.join(how) if how else 'אף מסלול'} | {RLM}{pct(total)} |")
    lines.append(f"| **כולם חתולים** | אף אחד לא נפגע בסבב הראשון | {RLM}{pct(cats)} |")
    lines.append(f"| **סך הכול** | | {RLM}100.0% |")
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


def orders_table(rivals):
    """Part b: the six orders, each with my best wand and the four chances; the best in bold."""
    a, b = sorted(rivals)
    rows = orders(rivals)
    top = max(ch[me - 1] for _, me, _, ch, _ in rows)
    lines = [f"| ראשון | שני | שלישי | השרביט שלי | אני | {float(a):g} | {float(b):g} | חתולים |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for p, me, q, ch, cats in rows:
        who = ["**אני**" if i == me - 1 else f"{RLM}{float(p[i]):g}" for i in range(3)]
        mine = ch[me - 1]
        ia = next(i for i in range(3) if i != me - 1 and p[i] == a)
        ib = next(i for i in range(3) if i != me - 1 and p[i] == b)
        cell = f"{RLM}{pct(mine)}"
        cell = f"**{cell}**" if mine == top else cell
        lines.append(f"| {who[0]} | {who[1]} | {who[2]} | {wand_label(q)} | {cell} | {RLM}{pct(ch[ia])} | "
                     f"{RLM}{pct(ch[ib])} | {RLM}{pct(cats)} |")
    return "\n".join(lines)


def threshold_table():
    """Part c: the weak rival's threshold a* for several strong rivals b."""
    lines = ["| היריב החזק \\( b \\) | הסף \\( a^* \\) |", "|:-:|:-:|"]
    for b in (Fr(1, 2), Fr(6, 10), Fr(7, 10), Fr(8, 10), Fr(9, 10), Fr(1)):
        lines.append(f"| {RLM}{float(b):g} | {RLM}{threshold(b):.3f} |")
    lines.append(f"| ‏שווה ל-\\( a \\) | {RLM}{threshold(None):.3f} |")
    return "\n".join(lines)


EXAMPLES = [(Fr(6, 10), Fr(8, 10)), (Fr(4, 10), Fr(8, 10)), (Fr(47, 100), Fr(9, 10)),
            (Fr(47, 100), Fr(55, 100)), (Fr(7, 10), Fr(9, 10))]


def examples_table():
    """Part c: the rule on a few rival pairs, against the best of all six orders on a grid."""
    lines = ["| היריבים | ההסתרה | הצלף | הבחירה | אני | החלש | החזק | חתולים |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for a, b in EXAMPLES:
        h, s = hide_third(a, b), sniper_first(a, b)
        best = h if h[0] > s[0] else s
        what = "שלישי, \\( a^- \\)" if best is h else "צלף ראשון"
        hv, sv = f"{RLM}{pct(h[0])}", f"{RLM}{pct(s[0])}"
        hv, sv = (f"**{hv}**", sv) if best is h else (hv, f"**{sv}**")
        lines.append(f"| {RLM}{float(a):g} ו-{float(b):g} | {hv} | {sv} | {RLM}{what} | "
                     + " | ".join(f"{RLM}{pct(v)}" for v in best) + " |")
    return "\n".join(lines)


WANDS = [Fr(3, 10), Fr(5, 10), Fr(59, 100), Fr(6, 10) - EPS, Fr(7, 10), Fr(9, 10), Fr(1)]
CHECK = Fr(59, 100)          # a concrete wand just under 0.6 for the checks of the rivals


# --- the Markov chain ---------------------------------------------------------------------

# The states: R1, R2, R3 (everyone alive, wizard k to shoot), the six duel states (i, j, k:
# wizards i < j left, k to shoot), the four absorbing ones (W1, W2, W3, the cats).
CW, CH = 480, 418
POS = {"R1": (62, 46), "R2": (180, 46), "R3": (298, 46), "CATS": (420, 46),
       (1, 2, 1): (44, 214), (1, 2, 2): (122, 214), (1, 3, 1): (200, 214), (1, 3, 3): (278, 214),
       (2, 3, 2): (356, 214), (2, 3, 3): (434, 214),
       "W1": (90, 372), "W2": (240, 372), "W3": (390, 372)}
SUB = {1: "₁", 2: "₂", 3: "₃"}
# Where the label of each first-round hit sits on its edge (the share of the way, a shift
# sideways), so that no two labels meet where the edges cross.
LABEL_AT = {(1, 2): (0.55, 0), (1, 3): (0.45, -10), (2, 3): (0.25, 10), (2, 1): (0.35, 8),
            (3, 1): (0.6, 12), (3, 2): (0.42, -12)}


def duel_of(killer, victim):
    """The duel state after `killer` (1..3) hit `victim` in the first round: the survivor opens."""
    i, j = sorted({1, 2, 3} - {victim})
    return (i, j, 6 - killer - victim)


def _box(key, lines, cls, w, h=40, me=False):
    x, y = POS[key]
    out = f'<rect class="{cls}{" mk-me" if me else ""}" x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="7"/>'
    if len(lines) == 1:
        out += f'<text class="mk-text" x="{x}" y="{y + 5}" text-anchor="middle" direction="rtl">{lines[0]}</text>'
    else:
        out += (f'<text class="mk-text" x="{x}" y="{y - 3}" text-anchor="middle" direction="rtl">{lines[0]}</text>'
                f'<text class="mk-text mk-sub" x="{x}" y="{y + 13}" text-anchor="middle" direction="rtl">{lines[1]}</text>')
    return out


def _edge(a, b, cls, label=None, t=0.5, dx=0, dy=0, bend=0):
    (x1, y1), (x2, y2) = POS[a], POS[b]
    hw = {True: 42, False: 32}
    # leave and enter at the box edges (vertical edges between the rows, horizontal within one)
    if y1 == y2:
        s = 1 if x2 > x1 else -1
        w1 = 42 if isinstance(a, str) else 32
        w2 = 42 if isinstance(b, str) else 32
        if bend:
            x1, x2 = x1 + s * 10, x2 - s * 10
            y1 = y2 = y1 + bend * 20
            sx, sy, ex, ey = x1, y1, x2, y2
            cx, cy = (sx + ex) / 2, sy + bend * 14
            path = f"M{sx:.0f},{sy:.0f} Q{cx:.0f},{cy:.0f} {ex:.0f},{ey:.0f}"
            lx, ly = cx, sy + bend * 12 + (12 if bend > 0 else -4)
            out = f'<path class="{cls}" d="{path}" fill="none" marker-end="url(#mk-arrow)"/>'
        else:
            sx, ex = x1 + s * w1, x2 - s * w2
            sy = ey = y1
            out = f'<line class="{cls}" x1="{sx:.0f}" y1="{sy}" x2="{ex:.0f}" y2="{ey}" marker-end="url(#mk-arrow)"/>'
            lx, ly = (sx + ex) / 2, sy - 7
    else:
        sy, ey = y1 + 20, y2 - 21
        sx, ex = x1 + (x2 - x1) * 0.12, x2 - (x2 - x1) * 0.04
        out = f'<line class="{cls}" x1="{sx:.0f}" y1="{sy}" x2="{ex:.0f}" y2="{ey}" marker-end="url(#mk-arrow)"/>'
        lx, ly = sx + (ex - sx) * t, sy + (ey - sy) * t + 4
    if label:
        out_l = f'<text class="mk-lab" x="{lx + dx:.0f}" y="{ly + dy:.0f}" text-anchor="middle">{label}</text>'
        return out, out_l
    return out, ""


def chain_svg(p=None, me=None, aria=""):
    """The game as a Markov chain. With p None, the general chain in p1, p2, p3 (every target
    each wizard may choose, solid; the miss or the air, dashed). With p (in turn order), the
    chain of everyone's best choice: the transition chances on the edges, the chances of the
    absorbing states in them, the unused states faded; `me` (1..3) marks my states."""
    general = p is None
    if general:
        lab = lambda w: f"p{SUB[w]}"                                  # noqa: E731
        mis = lambda w: f"1−p{SUB[w]}"                                # noqa: E731
        choice = None
    else:
        lab = lambda w: short(p[w - 1])                               # noqa: E731
        mis = lambda w: short(1 - p[w - 1])                           # noqa: E731
        _, trace = round_options(p)
        choice = {w: b for w, _, b in trace}
        chances, _ = round_options(p)
        cats = outcomes(p)[1]
    edges, labels, used = [], [], {"R1"}
    # the first round
    prev = "R1"
    for w, nxt in ((1, "R2"), (2, "R3"), (3, "CATS")):
        key = f"R{w}"
        targets = [t for t in (1, 2, 3) if t != w] if general else ([] if choice[w] == "air" else [choice[w]])
        if not general and key not in used:
            break
        for t in targets:
            d = duel_of(w, t)
            at, dx = LABEL_AT[(w, t)]
            e, l = _edge(key, d, "mk-hit", lab(w), t=at, dx=dx)
            edges.append(e); labels.append(l); used.add(d)
        air = not general and choice[w] == "air"
        miss = mis(w) if (general or not air) else "1"
        if general and w < 3:
            miss = mis(w)
        e, l = _edge(key, nxt, "mk-miss", miss)
        edges.append(e); labels.append(l); used.add(nxt)
        if not general and air:
            labels.append(f'<text class="mk-lab" x="{(POS[key][0] + POS[nxt][0]) / 2:.0f}" y="{POS[key][1] + 34}" text-anchor="middle" direction="rtl">באוויר</text>')
    # the duels
    for (i, j, k), _ in [(d, 0) for d in POS if isinstance(d, tuple)]:
        d = (i, j, k)
        if not general and d not in used:
            continue
        other = (i, j, j if k == i else i)
        used.add(other)
        e, l = _edge(d, f"W{k}", "mk-hit", lab(k), t=0.4, dx=14 if POS[f'W{k}'][0] > POS[d][0] else -14)
        edges.append(e); labels.append(l); used.add(f"W{k}")
        bend = -1 if k == i else 1
        e, l = _edge(d, other, "mk-miss", mis(k), bend=bend)
        edges.append(e); labels.append(l)
    for k in (1, 2, 3):
        if f"W{k}" in used:
            pass
    # the boxes
    boxes = []
    mine = lambda w: me is not None and w == me                       # noqa: E731
    for w in (1, 2, 3):
        key = f"R{w}"
        boxes.append((key, _box(key, ["כולם חיים", f"תור {w}"], "mk-node", 84, me=mine(w))))
    boxes.append(("CATS", _box("CATS", ["חתולים"] + ([] if general else [pct(cats)]), "mk-cat", 84)))
    for d in [d for d in POS if isinstance(d, tuple)]:
        i, j, k = d
        boxes.append((d, _box(d, [f"{i} מול {j}", f"תור {k}"], "mk-node", 64, me=mine(k))))
    for k in (1, 2, 3):
        key = f"W{k}"
        txt = [f"{k} מנצח"] + ([] if general else [pct(chances[k - 1])])
        boxes.append((key, _box(key, txt, "mk-win", 96, me=mine(k))))
    parts = [f'<svg class="figure mk-chain" viewBox="0 0 {CW} {CH}" style="max-width:34rem" role="img" aria-label="{aria}">',
             '<defs><marker id="mk-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="mk-head"/></marker></defs>']
    parts += edges
    for key, b in boxes:
        parts.append(b if general or key in used else f'<g class="st-faded">{b}</g>')
    parts += labels
    parts.append("</svg>")
    return "".join(parts)


def chain_general():
    return chain_svg(aria="שרשרת מרקוב של הדו-קרב : שלושת התורות של הסבב הראשון, ששת מצבי הדו-קרב, שלושת הניצחונות והחתולים, עם הסתברויות המעבר ב-p1, p2, p3")


def chain_a():
    p = place(1, weak(RIVALS), RIVALS)
    return chain_svg(p, me=1, aria="שרשרת מרקוב של סעיף א עם השרביט הטוב ביותר : אני באוויר, קוסם 2 על 3, קוסם 3 על 2, והסיכויים הסופיים 63.7%, 17.1%, 11.1% ו-8%")


def chain_legend(general):
    me = "" if general else '<span><i class="mk-key-me"></i>המצבים שבהם אני יורה, ואני מנצח</span>'
    tail = ("החץ המלא : פגיעה, עם ההסתברות שלה; המקווקו : החטאה או כישוף באוויר"
            if general else "על החצים הסתברויות המעבר, ובמצבים הסופיים הסיכוי להגיע אליהם")
    return (f'<span class="viz-legend"><span><i class="mk-key-hit"></i>פגיעה</span><span><i class="mk-key-miss"></i>החטאה או באוויר</span>'
            f'<span><i class="mk-key-win"></i>ניצחון</span><span><i class="mk-key-cat"></i>חתולים</span>{me}<span>{tail}</span></span>').replace(" :", " :")


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
    return f'<span class="viz-legend">{items}<span>הנקודה : הסיכוי הטוב ביותר; הציר האופקי : השרביט שלי</span></span>'


def chart_a():
    return chart([1], RIVALS, "הסיכוי שלי לנצח כפונקציה של השרביט, כשאני ראשון והיריבים 0.6 ו-0.8 : עולה עד 63.7% ממש לפני 0.6, צונח, ועולה שוב עד 40% ב-1")


def chart_abc():
    return chart([1, 2, 3], RIVALS, "הסיכוי שלי לנצח כפונקציה של השרביט בשלושת המיקומים, היריבים 0.6 ואחריו 0.8")


def blocks():
    """The generated blocks, in page order."""
    weak_a = weak(RIVALS)
    return [
        chain_general(), chain_legend(True),
        wand_table(1, RIVALS, WANDS), chart_a(), legend([1]), check_table(1, CHECK, RIVALS),
        chain_a(), chain_legend(False), who_wins(1, weak_a, RIVALS),
        orders_table(RIVALS), wand_table(3, RIVALS, WANDS), check_table(3, CHECK, RIVALS),
        who_wins(3, weak_a, RIVALS), chart_abc(), legend([1, 2, 3]),
        threshold_table(), examples_table(),
    ]


if __name__ == "__main__":
    for row in orders(RIVALS):
        print(row[1], [float(x) for x in row[0]], [float(c) for c in row[3]], float(row[4]))
    print("\n\n".join(blocks()))
