#!/usr/bin/env python3
"""Figures and tables of question 0032 (wolf, goat and cabbage).

    python tools/figures/fill.py 32        # put the blocks on the page

A farmer must ferry a wolf, a goat and a cabbage across a river in a boat that holds the
farmer and one more; left alone, the wolf eats the goat and the goat eats the cabbage. A
state is four bits (farmer, wolf, goat, cabbage: 0 near, 1 far). blocks() returns, in page
order: the statement figure, its legend, the step-through figure of the seven crossings
(its captions name both banks after every crossing), the table of the six forbidden
states, the state graph (sixteen states, the six forbidden ones struck out, the two
shortest paths) and its legend. tests/0032 checks the plan against brute force and the
page code.
"""

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

ITEMS = ["wolf", "goat", "cabbage"]
LETTER = {"farmer": "F", "wolf": "W", "goat": "G", "cabbage": "C"}
HEB = {"farmer": "האיכר", "wolf": "הזאב", "goat": "העז", "cabbage": "הכרוב", None: "לבד"}
FARMER, WOLF, GOAT, CABBAGE = 1, 2, 4, 8          # the bit of each one in the state mask
BITS = {"farmer": FARMER, "wolf": WOLF, "goat": GOAT, "cabbage": CABBAGE}


# --- the states ---------------------------------------------------------------------------

def safe(state):
    """Nobody is eaten: the goat is with the farmer, or away from both the wolf and the cabbage."""
    f, w, g, c = (bool(state & b) for b in (FARMER, WOLF, GOAT, CABBAGE))
    return g == f or (g != w and g != c)


def moves(state):
    """The states one crossing away: the farmer alone, or with one item on his bank."""
    out = []
    f = state & FARMER
    for item in [None] + ITEMS:
        if item is not None and bool(state & BITS[item]) != bool(f):
            continue                                     # that item is on the other bank
        new = state ^ FARMER ^ (BITS[item] if item else 0)
        out.append((item, new))
    return out


def solve():
    """BFS from everyone near (0) to everyone far (15): the items carried, None for alone."""
    start, goal = 0, FARMER | WOLF | GOAT | CABBAGE
    parent = {start: None}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        if s == goal:
            break
        for item, new in moves(s):
            if safe(new) and new not in parent:
                parent[new] = (s, item)
                queue.append(new)
    plan, s = [], goal
    while parent[s] is not None:
        s, item = parent[s]
        plan.append(item)
    return plan[::-1]


def all_solutions(limit=7):
    """Every safe crossing sequence of `limit` moves without repeating a state."""
    goal = 15
    out = []

    def rec(s, path, seen):
        if s == goal:
            out.append(path)
            return
        if len(path) == limit:
            return
        for item, new in moves(s):
            if safe(new) and new not in seen:
                rec(new, path + [item], seen | {new})

    rec(0, [], {0})
    return out


def replay(plan):
    """The states visited by a plan, or None when a crossing is illegal or unsafe."""
    s, states = 0, [0]
    for item in plan:
        legal = dict(moves(s))
        if item not in legal or not safe(legal[item]):
            return None
        s = legal[item]
        states.append(s)
    return states if s == 15 else None


# --- the crossing figure ---------------------------------------------------------------

def frame(state, carried=None, forward=True, moving=False, label="", unsafe=None):
    """Banks, river and boat; the farmer and the three items where they are."""
    w, h = 640, 190
    p = [f'<svg class="figure river-fig" viewBox="0 0 {w} {h}" style="max-width:40rem" role="img" aria-label="{label}">',
         '<rect class="bank" x="0" y="20" width="200" height="150" rx="8"/>',
         '<rect class="bank" x="440" y="20" width="200" height="150" rx="8"/>',
         '<rect class="river" x="200" y="20" width="240" height="150"/>',
         '<text class="legend" x="100" y="160" text-anchor="middle" direction="rtl">הגדה הקרובה</text>',
         '<text class="legend" x="540" y="160" text-anchor="middle" direction="rtl">הגדה הרחוקה</text>']

    def who(name, x, y, cls="st-cell"):
        p.append(f'<g><circle class="{cls}" cx="{x}" cy="{y}" r="18"/>'
                 f'<text class="st-text" x="{x}" y="{y + 5}" text-anchor="middle">{LETTER[name]}</text></g>')

    on_boat = {"farmer"} | ({carried} if carried else set()) if moving else set()
    for side, x0 in ((0, 45), (1, 485)):
        k = 0
        for name in ["farmer"] + ITEMS:
            if name in on_boat or bool(state & BITS[name]) != bool(side):
                continue
            cls = "st-bad" if unsafe and name in unsafe else ("st-stack" if name == "farmer" else "st-cell")
            who(name, x0 + 40 * k, 70, cls)
            k += 1
    # the boat, on the bank of the farmer or in the middle while crossing
    bx = 320 if moving else (215 if not state & FARMER else 365)
    p.append(f'<rect class="boat" x="{bx - 50}" y="100" width="100" height="26" rx="10"/>')
    if moving:
        who("farmer", bx - 20 if carried else bx, 93, "st-stack")
        if carried:
            who(carried, bx + 20, 93, "st-cell")
        x0, x1 = (250, 390) if forward else (390, 250)
        d = 9 if forward else -9
        p.append(f'<line class="ink-line" x1="{x0}" y1="150" x2="{x1}" y2="150" stroke-width="2"/>'
                 f'<polygon class="ink-fill" points="{x1},150 {x1 - d},145 {x1 - d},155"/>')
    p.append("</svg>")
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="st-stack"></i>האיכר (F)</span><span><i class="st-cell"></i>הזאב (W), העז (G) והכרוב (C)</span>'
            '<span><i class="boat"></i>הסירה : האיכר ועוד אחד</span></span>')


def statement_figure():
    return frame(0, label="האיכר, הזאב, העז והכרוב על הגדה הקרובה, והסירה לידם")


def crossing_stepper():
    plan = solve()
    states = replay(plan)
    frames = [(frame(0, label="התחלה : כולם על הגדה הקרובה"), "רגע 0 : כולם על הגדה הקרובה. הסירה מכילה את האיכר ועוד אחד.")]
    for k, (item, s_from, s_to) in enumerate(zip(plan, states, states[1:]), 1):
        forward = not s_from & FARMER
        way = "קדימה" if forward else "חזרה"
        what = f"האיכר לוקח את {HEB[item]} {way}" if item else ("האיכר חוזר לבד" if not forward else "האיכר חוצה לבד")
        left = [HEB[n] for n in ITEMS if bool(s_from & BITS[n]) == bool(s_from & FARMER) and n != item]
        left = " ו".join(left)
        after = "".join(f", על {name} {bank_text(s_to, side)}" if bank_text(s_to, side) != "–" else f", {name} ריקה"
                        for side, name in ((0, "הגדה הקרובה"), (1, "הרחוקה")))[2:]
        frames.append((frame(s_from, item, forward, moving=True, label=f"חצייה {k}"),
                       f"חצייה {k} : {what}. "
                       + (f"על הגדה שעזב : {left}, וזה בטוח. " if left else "הגדה שעזב ריקה. ")
                       + f"אחרי החצייה : {after}."))
    frames.append((frame(15, label="סיום"), f"כולם על הגדה הרחוקה אחרי {len(plan)} חציות."))
    return stepper(frames, "שבע החציות של האיכר, חצייה אחרי חצייה")


def bank_text(state, side):
    names = [LETTER[n] for n in ["farmer"] + ITEMS if bool(state & BITS[n]) == bool(side)]
    return "".join(names) or "–"


# --- the state graph ------------------------------------------------------------------

def graph_svg():
    """Sixteen states in two rows (the farmer near, the farmer far), the six unsafe ones
    struck out, the legal crossings as edges and the two shortest paths highlighted. Every
    state and crossing carries a key in data-fig (`n<state>`, `e<low>-<high>` for the two
    states a crossing joins), which the steps beside the figure light (question-page.js)."""
    w, h = 640, 250
    col = lambda s: (s >> 1) & 7                      # the item mask
    X = lambda s: 48 + col(s) * 78
    Y = lambda s: 60 if not s & FARMER else 190
    p = [f'<svg class="figure river-graph" viewBox="0 0 {w} {h}" style="max-width:40rem" role="img" '
         'aria-label="גרף המצבים : שש עשרה חלוקות של האיכר ושלושת הפריטים בין הגדות, שש אסורות, ושני המסלולים הקצרים ביותר">']
    on_path = set()
    for sol in all_solutions():
        states = replay(sol)
        on_path |= {frozenset((a, b)) for a, b in zip(states, states[1:])}
    for s in range(16):
        if not safe(s) or s & FARMER:
            continue
        for item, t in moves(s):
            if safe(t):
                cls = "box-path" if frozenset((s, t)) in on_path else "ink-line"
                p.append(f'<line class="{cls}" data-fig="e{min(s, t)}-{max(s, t)}" x1="{X(s)}" y1="{Y(s) + 20}" x2="{X(t)}" y2="{Y(t) - 20}" '
                         f'stroke-width="{3 if cls == "box-path" else 1}" {"" if cls == "box-path" else "stroke-opacity=\"0.4\""}/>')
    for s in range(16):
        ok = safe(s)
        cls = "st-ok" if s in (0, 15) else "st-cell" if ok else "st-bad"
        p.append(f'<g data-fig="n{s}"><rect class="{cls}" x="{X(s) - 32}" y="{Y(s) - 20}" width="64" height="40" rx="6"/>')
        p.append(f'<text class="st-text st-sm" x="{X(s)}" y="{Y(s) - 4}" text-anchor="middle">{bank_text(s, 0)}</text>'
                 f'<text class="st-text st-sm" x="{X(s)}" y="{Y(s) + 14}" text-anchor="middle">{bank_text(s, 1)}</text>')
        if not ok:
            p.append(f'<line class="pg-strike" x1="{X(s) - 26}" y1="{Y(s) + 16}" x2="{X(s) + 26}" y2="{Y(s) - 16}"/>')
        p.append("</g>")
    p.append('<text class="legend" x="8" y="16">farmer near: near bank / far bank</text>')
    p.append('<text class="legend" x="8" y="240">farmer far</text>')
    p.append("</svg>")
    return "".join(p)


def graph_legend():
    return ('<span class="viz-legend"><span><i class="st-ok"></i>ההתחלה והסיום</span><span><i class="st-cell"></i>מצב בטוח</span>'
            '<span><i class="st-bad"></i>מצב אסור : מישהו נאכל</span><span><i class="box-path"></i>שני המסלולים הקצרים ביותר</span>'
            '<span><i class="ink"></i>חצייה בטוחה אחרת</span></span>')


def forbidden_table():
    """The six forbidden states: the goat away from the farmer, with the wolf or the cabbage."""
    lines = ["| הגדה הקרובה | הגדה הרחוקה | מי נאכל |", "|---|---|---|"]
    for s in range(16):
        if safe(s):
            continue
        w, g, c = bool(s & WOLF), bool(s & GOAT), bool(s & CABBAGE)
        why = ("הזאב אוכל את העז, והעז את הכרוב" if g == c else "הזאב אוכל את העז") if g == w else "העז אוכלת את הכרוב"
        lines.append(f"| ‏{bank_text(s, 0)} | ‏{bank_text(s, 1)} | {why} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [statement_figure(), legend(), crossing_stepper(), forbidden_table(), graph_svg(), graph_legend()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
