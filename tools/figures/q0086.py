#!/usr/bin/env python3
"""Figures and tables of question 0086: the chameleons.

    python tools/figures/fill.py 86        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the tests compare the
two): a breadth-first search over the states (r, g, b), the counts of the red, the green and
the blue chameleons. A meeting is the pair of colours (i, j), i < j, that meet; both turn to
the third colour 3 - i - j. The same model is in the box (docs/javascripts/explorer/chameleons.js).
"""

import math
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401

NB = " "
RLM = "‏"
NAMES = ("אדומות", "ירוקות", "כחולות")       # plural, the colour of a group
ONE = ("אדומה", "ירוקה", "כחולה")            # singular, one chameleon
START = (13, 15, 17)                          # part a
SMALL = (2, 5, 4)                             # the triangle of part c
CONSTRUCT = (7, 1, 3)                         # the construction of part b
PAIRS = ((0, 1), (0, 2), (1, 2))


# --- the model -----------------------------------------------------------------------------------

def meet(s, i, j):
    """The state after a chameleon of colour i meets one of colour j (i != j)."""
    t = list(s)
    t[i] -= 1
    t[j] -= 1
    t[3 - i - j] += 2
    return tuple(t)


def moves(s):
    """Every meeting possible in s, as (pair, state)."""
    return [((i, j), meet(s, i, j)) for i, j in PAIRS if s[i] and s[j]]


def distances(start):
    """The fewest meetings from start to every reachable state."""
    dist = {tuple(start): 0}
    queue = deque([tuple(start)])
    while queue:
        s = queue.popleft()
        for _, t in moves(s):
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    return dist


def mono(n, c):
    """Every chameleon of colour c."""
    return tuple(n if k == c else 0 for k in range(3))


def bfs_to(start, c):
    """The fewest meetings until every chameleon is of colour c, by search, or None."""
    d = distances(start).get(mono(sum(start), c))
    return d


def formula_to(s, c):
    """The closed form: the counts sx, sy of the other two colours x, y must agree mod 3, and
    the answer is the larger of them; a state of one other colour has no meeting at all."""
    sx, sy = (s[k] for k in range(3) if k != c)
    if (sx - sy) % 3:
        return None
    if s[c] == 0 and min(sx, sy) == 0 and max(sx, sy) > 0:
        return None
    return max(sx, sy)


def formula_min(s):
    """(meetings, colour) for the best colour, the lowest colour on a tie, or None."""
    best = None
    for c in range(3):
        m = formula_to(s, c)
        if m is not None and (best is None or m < best[0]):
            best = (m, c)
    return best


def construct(s, c):
    """The construction of part b: of the other two colours, x (the larger count) meets y
    until y is gone, then three meetings at a time (x with c, then twice x with y)."""
    s = list(s)
    x, y = [k for k in range(3) if k != c]
    if s[x] < s[y]:
        x, y = y, x
    plan = []

    def go(i, j):
        nonlocal s
        s = list(meet(s, i, j))
        plan.append(((min(i, j), max(i, j)), tuple(s)))

    while s[y] > 0:
        go(x, y)
    while s[x] > 0:
        go(x, c)
        go(x, y)
        go(x, y)
    return plan


def invariant(s):
    """What no meeting changes: r - g and g - b mod 3."""
    return ((s[0] - s[1]) % 3, (s[1] - s[2]) % 3)


def states(n):
    return [(r, g, n - r - g) for r in range(n + 1) for g in range(n + 1 - r)]


def ltr(s):
    return f'<span dir="ltr">{s}</span>'


def pair_name(p):
    i, j = p
    return f"{ONE[i]} ו{ONE[j]}"


# --- the statement -------------------------------------------------------------------------------

def dot(cx, cy, c, r=7):
    return f'<circle class="ch-dot ch-c{c}" cx="{cx}" cy="{cy}" r="{r}"/>'


def statement_figure():
    """The three groups with their counts, and the three meetings as dots: two of different
    colours, an arrow, two of the third colour."""
    W, H = 300, 214
    s = [f'<svg class="figure ch-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
         f'aria-label="13 זיקיות אדומות, 15 ירוקות ו-17 כחולות. כששתיים בצבעים שונים נפגשות, שתיהן עוברות לצבע השלישי : '
         f'אדומה וירוקה הופכות לשתי כחולות, אדומה וכחולה לשתי ירוקות, ירוקה וכחולה לשתי אדומות">']
    for k, (cnt, x) in enumerate(zip(START, (60, 150, 240))):
        s.append(f'<circle class="ch-disc ch-c{k}" cx="{x}" cy="40" r="30"/>')
        s.append(f'<text class="ch-big" x="{x}" y="48" text-anchor="middle">{cnt}</text>')
    for row, (i, j) in enumerate(PAIRS):
        y = 106 + row * 40
        k = 3 - i - j
        s.append(dot(84, y, i) + dot(104, y, j))
        s.append(f'<line class="ch-arrow" x1="124" x2="170" y1="{y}" y2="{y}"/>')
        s.append(f'<polygon class="ch-head" points="170,{y - 5} 179,{y} 170,{y + 5}"/>')
        s.append(dot(196, y, k) + dot(216, y, k))
    s.append("</svg>")
    return "".join(s)


def statement_legend():
    return ('<span class="viz-legend"><span><i class="ch-key ch-c0"></i>אדומה</span><span><i class="ch-key ch-c1"></i>ירוקה</span>'
            '<span><i class="ch-key ch-c2"></i>כחולה</span><span>בכל שורה : שתי זיקיות בצבעים שונים נפגשות, ושתיהן עוברות לצבע השלישי</span></span>')


# --- part a ------------------------------------------------------------------------------------

def first_meetings():
    """Three meetings from 13, 15, 17, one of each kind, and the residues mod 3."""
    out, s = [("התחלה", START)], START
    for p in PAIRS:
        s = meet(s, *p)
        out.append((pair_name(p), s))
    return out


def residues_table():
    """The counts and their residues mod 3, a cell per colour: "13 ≡ 1"."""
    rows = ["| הפגישה | אדומות | ירוקות | כחולות |", "|---|:-:|:-:|:-:|"]
    for name, s in first_meetings():
        rows.append(f"| {name} | " + " | ".join(f"{RLM}\\( {v} \\equiv {v % 3} \\)" for v in s) + " |")
    return "\n".join(rows)


# --- part b ------------------------------------------------------------------------------------

def construct_table():
    rows = ["| פגישה | מי נפגשות | אדומות | ירוקות | כחולות |", "|:-:|---|:-:|:-:|:-:|",
            "| 0 | התחלה | " + " | ".join(str(v) for v in CONSTRUCT) + " |"]
    for k, (p, s) in enumerate(construct(CONSTRUCT, 2), 1):
        rows.append(f"| {k} | {pair_name(p)} | " + " | ".join(str(v) for v in s) + " |")
    return "\n".join(rows)


# --- part c ------------------------------------------------------------------------------------

def tri_xy(s, n, left, top, side):
    """A state as a point of the triangle: all red at the top, all green at the bottom left,
    all blue at the bottom right."""
    h = side * math.sqrt(3) / 2
    R, G, B = (left + side / 2, top), (left, top + h), (left + side, top + h)
    r, g, b = s
    return ((r * R[0] + g * G[0] + b * B[0]) / n, (r * R[1] + g * G[1] + b * B[1]) / n)


def triangle_figure():
    start, n = SMALL, sum(SMALL)
    dist = distances(start)
    plan = construct(start, 2)
    left, top, side = 30, 30, 260
    W, H = side + 60, int(top + side * math.sqrt(3) / 2 + 40)
    P = lambda s: tri_xy(s, n, left, top, side)  # noqa: E731
    out = [f'<svg class="figure ch-tri" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
           f'aria-label="כל המצבים של 11 זיקיות כנקודות במשולש : למעלה כולן אדומות, למטה משמאל כולן ירוקות, למטה מימין כולן כחולות. '
           f'מההתחלה, 2 אדומות, 5 ירוקות ו-4 כחולות, מגיעים ל-{len(dist)} מתוך {len(states(n))} המצבים, ביניהם הפינה שבה כולן כחולות. '
           f'הדרך של {len(plan)} פגישות מסומנת">']
    corners = [mono(n, c) for c in range(3)]
    xs = [P(c) for c in corners]
    out.append(f'<polygon class="ch-edge" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in xs)}"/>')
    pts = [start] + [s for _, s in plan]
    out.append('<polyline class="ch-route" points="' + " ".join(f"{P(s)[0]:.1f},{P(s)[1]:.1f}" for s in pts) + '"/>')
    for s in states(n):
        x, y = P(s)
        if s in dist:
            cls = "ch-goal" if s == mono(n, 2) else "ch-reach"
            out.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{6 if cls == "ch-goal" else 4.2}"/>')
        else:
            out.append(f'<circle class="ch-never" cx="{x:.1f}" cy="{y:.1f}" r="2.6"/>')
    x, y = P(start)
    out.append(f'<circle class="ch-start" cx="{x:.1f}" cy="{y:.1f}" r="8"/>')
    for c, (x, y) in enumerate(xs):
        dy = -12 if c == 0 else 22
        out.append(f'<circle class="ch-dot ch-c{c}" cx="{x:.1f}" cy="{y + dy - 4:.1f}" r="6"/>')
    out.append("</svg>")
    return "".join(out)


def triangle_legend():
    n = sum(SMALL)
    reach = len(distances(SMALL))
    return ('<span class="viz-legend"><span><i class="ch-key-reach"></i>מצב שמגיעים אליו</span>'
            '<span><i class="ch-key-never"></i>מצב שלא מגיעים אליו</span>'
            '<span><i class="ch-key-start"></i>ההתחלה : 2 אדומות, 5 ירוקות ו-4 כחולות</span>'
            '<span><i class="ch-key-goal"></i>כולן כחולות</span><span><i class="ch-key-route"></i>הבנייה : 5 פגישות</span>'
            f'<span>פינה מסומנת בצבע שלה : שם כל {n} הזיקיות באותו צבע. {reach} מתוך {len(states(n))} המצבים נגישים</span></span>')


EXAMPLES = [(13, 15, 17), (13, 16, 17), (14, 15, 17), (1, 4, 0), (9, 0, 3), (5, 8, 11), (3, 3, 3), (6, 0, 0)]


def examples_table():
    rows = ["| אדומות | ירוקות | כחולות | השאריות שוות | הצבע בסוף | הכי מעט פגישות |", "|:-:|:-:|:-:|---|---|:-:|"]
    for s in EXAMPLES:
        best = formula_min(s)
        eq = [f"{NAMES[i]} ו{NAMES[j]}" for i, j in PAIRS if (s[i] - s[j]) % 3 == 0]
        same = "כל השלוש" if len(eq) == 3 else eq[0] if eq else "אף זוג"
        if best is None:
            rows.append(" | ".join([f"| {s[0]}", str(s[1]), str(s[2]), same, "אי אפשר", "‏–"]) + " |")
        else:
            m, c = best
            rows.append(" | ".join([f"| {s[0]}", str(s[1]), str(s[2]), same, NAMES[c], str(m)]) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        statement_figure(),
        statement_legend(),
        residues_table(),
        construct_table(),
        triangle_figure(),
        triangle_legend(),
        examples_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
