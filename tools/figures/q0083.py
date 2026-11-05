#!/usr/bin/env python3
"""Figures and tables of question 0083: the water jugs.

    python tools/figures/fill.py 83        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the test compares the
two): a breadth-first search over the jugs' contents, with the steps in a fixed order
(fill A, fill B, empty A, empty B, pour A into B, pour B into A; with three jugs and no tap,
every pour i into j by i, then j), the same order as the page's code and the box
(docs/javascripts/explorer/jugs.js).
"""

import sys
from collections import deque
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402
from stepper import stepper  # noqa: E402

NB = " "
RLM = "‏"
NAMES = "AB"


# --- the model -----------------------------------------------------------------------------------

def moves(caps, s, tap=True):
    """Every state one step from s, as (step, state); a step that changes nothing is left out.
    A step is ("fill", i), ("empty", i) or ("pour", i, j)."""
    n = len(caps)
    out = []
    if tap:
        out += [(("fill", i), s[:i] + (caps[i],) + s[i + 1:]) for i in range(n)]
        out += [(("empty", i), s[:i] + (0,) + s[i + 1:]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            t = min(s[i], caps[j] - s[j])
            nxt = list(s)
            nxt[i] -= t
            nxt[j] += t
            out.append((("pour", i, j), tuple(nxt)))
    return [(m, x) for m, x in out if x != s]


def bfs(caps, goal, start=None, tap=True):
    """The fewest steps from start (empty jugs) to a state where goal(state) holds:
    [(step, state), ...], or None."""
    start = start or (0,) * len(caps)
    parent = {start: None}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        if goal(s):
            path = []
            while parent[s] is not None:
                s0, m = parent[s]
                path.append((m, s))
                s = s0
            return path[::-1]
        for m, nxt in moves(caps, s, tap):
            if nxt not in parent:
                parent[nxt] = (s, m)
                queue.append(nxt)
    return None


def distances(caps, start=None, tap=True):
    """The fewest steps to every reachable state."""
    start = start or (0,) * len(caps)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for _, nxt in moves(caps, s, tap):
            if nxt not in dist:
                dist[nxt] = dist[s] + 1
                queue.append(nxt)
    return dist


def shortest(a, b, t):
    """Two jugs with a tap: the fewest steps to t litres in one of them, or None."""
    return bfs((a, b), lambda s: t in s)


def count_shortest(caps, target, start=None, tap=True):
    """How many shortest paths reach the target state (or a state with the target amount)."""
    dist = distances(caps, start, tap)
    start = start or (0,) * len(caps)
    ways = {start: 1}
    for s in sorted(dist, key=dist.get):
        for _, nxt in moves(caps, s, tap):
            if dist.get(nxt) == dist[s] + 1:
                ways[nxt] = ways.get(nxt, 0) + ways[s]
    hit = (lambda s: s == target) if isinstance(target, tuple) else (lambda s: target in s)
    best = min(dist[s] for s in dist if hit(s))
    return sum(ways[s] for s in dist if hit(s) and dist[s] == best)


def keep_pouring(a, b, t, from_a):
    """The "keep pouring" plan: always fill the same jug (A when from_a), pour it into the other,
    and empty the other when it is full; stops when one jug holds t (None after 200 steps)."""
    x = y = 0
    plan = []
    for _ in range(200):
        if t in (x, y):
            return plan
        if from_a:
            if x == 0:
                x, m = a, ("fill", 0)
            elif y == b:
                y, m = 0, ("empty", 1)
            else:
                d = min(x, b - y)
                x, y, m = x - d, y + d, ("pour", 0, 1)
        else:
            if y == 0:
                y, m = b, ("fill", 1)
            elif x == a:
                x, m = 0, ("empty", 0)
            else:
                d = min(y, a - x)
                x, y, m = x + d, y - d, ("pour", 1, 0)
        plan.append((m, (x, y)))
    return None


def measurable(a, b, t):
    return 0 <= t <= max(a, b) and t % gcd(a, b) == 0


# The numbers of the page
A, B, T = 3, 5, 4
PLAN = shortest(A, B, T)                                  # 6 steps, filling B first
OTHER = keep_pouring(A, B, T, from_a=True)                # 8 steps, filling A first
CAPS3, START3, GOAL3 = (8, 5, 3), (8, 0, 0), (4, 4, 0)
PLAN3 = bfs(CAPS3, lambda s: s == GOAL3, START3, tap=False)                  # 7 pours
OTHER3 = [(("pour", 0, 2), (5, 0, 3))] + bfs(CAPS3, lambda s: s == GOAL3, (5, 0, 3), tap=False)
EXAMPLES = [(3, 5, 4), (3, 5, 1), (3, 5, 2), (4, 6, 2), (4, 6, 3), (6, 10, 8), (7, 11, 6), (3, 5, 7)]


# --- words ---------------------------------------------------------------------------------------

def step_name(m, names=NAMES):
    if m[0] == "fill":
        return f"מילוי {names[m[1]]}"
    if m[0] == "empty":
        return f"ריקון {names[m[1]]}"
    return f"מזיגה מ-{names[m[1]]} ל-{names[m[2]]}"


def step_words(m, s, caps, names=None):
    """A caption: what the step does, in words (two jugs by name, three by capacity)."""
    if m[0] == "fill":
        return f"ממלאים את {names[m[1]]} מהברז"
    if m[0] == "empty":
        return f"שופכים את {names[m[1]]} לכיור"
    i, j = m[1], m[2]
    if names:
        why = f"עד ש-{names[j]} מלא" if s[j] == caps[j] else f"עד ש-{names[i]} ריק"
        return f"מוזגים מ-{names[i]} ל-{names[j]}, {why}"
    why = f"עד שהכד של {caps[j]} מלא" if s[j] == caps[j] else f"עד שהכד של {caps[i]} ריק"
    return f"מוזגים מהכד של {caps[i]} לכד של {caps[j]}, {why}"


def contents(s, caps, names=None):
    """The contents after a step: "A = 3, B = 4" isolated left to right, or by capacity
    in Hebrew order ("בכדים של 8, 5 ו-3 : 4, 4 ו-0")."""
    if names:
        return f"ב-{names[0]} יש {s[0]}, וב-{names[1]} יש {s[1]}"
    return (f"בכדים של {', '.join(map(str, caps[:-1]))} ו-{caps[-1]}{NB}: "
            f"{', '.join(map(str, s[:-1]))} ו-{s[-1]}")


def ltr(s):
    return f'<span dir="ltr">{s}</span>'


# --- the jugs ------------------------------------------------------------------------------------

def jugs_svg(caps, amounts, aria, names=None, labels=None, changed=(), pour=None, unit=22):
    """The jugs side by side (the first on the left), water to its level, the amount inside
    and the capacity under each; `changed` jugs framed, `pour` an arrow (i, j) over them."""
    n = len(caps)
    jw, gap, top = 64, 46, 34
    h_max = max(caps) * unit
    W = n * jw + (n - 1) * gap + 24
    H = top + h_max + 46
    s = [f'<svg class="figure wj-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" aria-label="{aria}">']
    xs = [12 + k * (jw + gap) for k in range(n)]
    base = top + h_max
    for k in range(n):
        x, hk = xs[k], caps[k] * unit
        wh = amounts[k] * unit
        if wh:
            s.append(f'<rect class="wj-water" x="{x + 3}" y="{base - wh}" width="{jw - 6}" height="{wh}"/>')
        for lev in range(1, caps[k]):
            s.append(f'<line class="wj-lev" x1="{x}" x2="{x + 8}" y1="{base - lev * unit}" y2="{base - lev * unit}"/>')
        cls = "wj-jug wj-chg" if k in changed else "wj-jug"
        s.append(f'<path class="{cls}" d="M{x},{base - hk} L{x},{base} L{x + jw},{base} L{x + jw},{base - hk}"/>')
        s.append(f'<text class="wj-num" x="{x + jw / 2}" y="{base - max(wh, unit * 0.6) / 2 + 5 if wh else base - 10}" text-anchor="middle">{amounts[k]}</text>')
        if names:
            s.append(f'<text class="wj-name" x="{x + jw / 2}" y="{base + 20}" text-anchor="middle">{names[k]}</text>')
        lab = labels[k] if labels else f"{caps[k]} ליטר"
        s.append(f'<text class="wj-cap" x="{x + jw / 2}" y="{base + (38 if names else 22)}" text-anchor="middle" direction="rtl">{lab}</text>')
    if pour:
        i, j = pour
        x1, x2 = xs[i] + jw / 2, xs[j] + jw / 2
        y = 14
        d = 1 if x2 > x1 else -1
        s.append(f'<path class="wj-arrow" d="M{x1},{base - caps[i] * unit - 4} Q{(x1 + x2) / 2},{y - 8} {x2 - d * 8},{base - caps[j] * unit - 10}"/>')
        tx, ty = x2 - d * 8, base - caps[j] * unit - 10
        s.append(f'<polygon class="wj-head" points="{tx - 5},{ty - 7} {tx + 5},{ty - 7} {tx},{ty + 2}"/>')
    s.append("</svg>")
    return "".join(s)


def statement_figure():
    return jugs_svg((A, B), (0, 0), "שני כדים ריקים בלי סימונים : A מחזיק 3 ליטר ו-B מחזיק 5 ליטר", names=NAMES)


def statement_legend():
    return ('<span class="viz-legend"><span><i class="wj-key-jug"></i>כד בלי סימונים, A של 3 ליטר ו-B של 5 ליטר</span>'
            '<span><i class="wj-key-water"></i>מים, והמספר בתוך הכד הוא הכמות בליטרים</span></span>')


def plan_stepper(caps, plan, start, names, aria, labels=None, unit=22):
    frames = [(jugs_svg(caps, start, "התחלה", names=names, labels=labels, unit=unit),
               f"התחלה{NB}: " + ("שני הכדים ריקים." if not any(start) else "הכד של 8 מלא, ושני האחרים ריקים."))]
    prev = start
    for k, (m, s) in enumerate(plan, 1):
        changed = [i for i in range(len(caps)) if s[i] != prev[i]]
        pour = (m[1], m[2]) if m[0] == "pour" else None
        words = step_words(m, s, caps, names)
        kind = "צעד" if names else "מזיגה"
        cap = f"{kind} {k}{NB}: {words}. {contents(s, caps, names)}."
        if k == len(plan):
            cap += " <strong>" + ("ב-B יש 4 ליטר." if len(caps) == 2 else "שני חצאים של 4 ליטר.") + "</strong>"
        frames.append((jugs_svg(caps, s, f"צעד {k}", names=names, labels=labels, changed=changed, pour=pour, unit=unit), cap))
        prev = s
    return stepper(frames, aria)


def plan_table(plan, names=NAMES, caps=(A, B)):
    head = "| צעד | הפעולה | " + " | ".join(RLM + n for n in names) + " |"
    rows = [head, "|:-:|---|" + ":-:|" * len(names)]
    for k, (m, s) in enumerate(plan, 1):
        rows.append(f"| {k} | {step_name(m, names)} | " + " | ".join(str(v) for v in s) + " |")
    return "\n".join(rows)


def grid_figure(caps, dist, paths, goal, aria, names=("A", "B"), dims=(0, 1), fixed=None):
    """The states as a grid: the first named jug across, the second up; a dot for every
    reachable state, a ring for the states never reached, and the paths drawn on it."""
    i0, i1 = dims
    ca, cb = caps[i0], caps[i1]
    w = 60 + 46 * (ca + 1)
    h = 40 + 34 * (cb + 1)
    c = Chart(aria, w=w, h=h, x0=44, right=12, top=12, base=h - 32,
              x_min=-0.5, x_max=ca + 0.5, y_min=-0.5, y_max=cb + 0.5,
              style=f"max-width:{w / 16:.1f}rem")
    c.grid_x(range(ca + 1), dashed=False)
    c.grid_y(range(cb + 1))
    c.axis()
    c.text(ca + 0.5, -0.5, names[0], cls="tick", anchor="end", dy=30)
    c.text(-0.5, cb + 0.5, names[1], cls="tick", anchor="end", dx=-10, dy=10)
    seen = {(s[i0], s[i1]) for s in dist}
    for kind, path in paths:
        pts = [(p[i0], p[i1]) for p in path]
        extra = ' stroke-dasharray="6 5"' if kind == "alt" else ""
        c.path(pts, "wj-route" + (" is-alt" if kind == "alt" else ""), width=3 if kind != "alt" else 2.5, extra=extra)
    for x in range(ca + 1):
        for y in range(cb + 1):
            if fixed is not None and not (0 <= fixed - x - y <= caps[3 - i0 - i1]):
                continue
            if (x, y) in seen:
                cls = "wj-goal" if goal(x, y) else "wj-reach"
                c.add(f'<circle class="{cls}" cx="{c.X(x):.1f}" cy="{c.Y(y):.1f}" r="6.5"><title>{names[0]} = {x}, {names[1]} = {y}</title></circle>')
            else:
                c.add(f'<circle class="wj-never" cx="{c.X(x):.1f}" cy="{c.Y(y):.1f}" r="4.5"><title>{names[0]} = {x}, {names[1]} = {y} : לא מגיעים</title></circle>')
    return c.svg()


def grid2():
    d = distances((A, B))
    paths = [("alt", [(0, 0)] + [s for _, s in OTHER]), ("best", [(0, 0)] + [s for _, s in PLAN])]
    return grid_figure((A, B), d, paths, lambda x, y: T in (x, y),
                       "מרחב המצבים של שני הכדים : A לרוחב מ-0 עד 3, B לגובה מ-0 עד 5. 16 מצבים נגישים, כולם על השפה, "
                       "ו-8 המצבים שבפנים לא נגישים. המסלול של 6 צעדים והמסלול של 8 צעדים מסומנים")


def grid2_legend():
    return ('<span class="viz-legend"><span><i class="wj-key-reach"></i>מצב שמגיעים אליו</span>'
            '<span><i class="wj-key-goal"></i>מצב עם 4 ליטר</span><span><i class="wj-key-never"></i>מצב שלא מגיעים אליו לעולם</span>'
            '<span><i class="wj-key-best"></i>6 הצעדים, מתחילים במילוי B</span><span><i class="wj-key-alt"></i>8 הצעדים, מתחילים במילוי A</span></span>')


def examples_table():
    rows = ["| ‏a | ‏b | ‏T | ‏gcd | אפשר? | הכי מעט צעדים | למה |", "|:-:|:-:|:-:|:-:|:-:|:-:|---|"]
    for a, b, t in EXAMPLES:
        g = gcd(a, b)
        p = shortest(a, b, t)
        if p is not None:
            why = f"כפולה של {g}, ולא יותר מ-{max(a, b)}"
        elif t > max(a, b):
            why = f"יותר מהכד הגדול, {max(a, b)}"
        else:
            why = f"לא כפולה של {g}"
        rows.append(f"| {a} | {b} | {t} | {g} | {'כן' if p is not None else 'לא'} | {len(p) if p is not None else '‏–'} | {why} |")
    return "\n".join(rows)


def other_table():
    return plan_table(OTHER)


NAMES3 = ["8", "5", "3"]


def plan3_stepper():
    return plan_stepper(CAPS3, PLAN3, START3, None,
                        "שבע המזיגות שמחלקות 8 ליטר לשני חצאים של 4, מזיגה אחרי מזיגה",
                        labels=["8 ליטר", "5 ליטר", "3 ליטר"], unit=15)


def plan3_table():
    rows = ["| מזיגה | מ- | ל- | הכד של 8 | הכד של 5 | הכד של 3 |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for k, (m, s) in enumerate(PLAN3, 1):
        rows.append(f"| {k} | {CAPS3[m[1]]} | {CAPS3[m[2]]} | {s[0]} | {s[1]} | {s[2]} |")
    return "\n".join(rows)


def grid3():
    d = distances(CAPS3, START3, tap=False)
    paths = [("alt", [START3] + [s for _, s in OTHER3]), ("best", [START3] + [s for _, s in PLAN3])]
    return grid_figure(CAPS3, d, paths, lambda y, z: (8 - y - z, y, z) == GOAL3,
                       "מרחב המצבים של שלושת הכדים לפי הכד של 5 לרוחב והכד של 3 לגובה, והכד של 8 מחזיק את השאר. "
                       "16 מצבים נגישים, כולם על השפה. המסלול של 7 מזיגות והמסלול של 8 מזיגות מסומנים",
                       names=("5", "3"), dims=(1, 2), fixed=8)


def grid3_legend():
    return ('<span class="viz-legend"><span><i class="wj-key-reach"></i>מצב שמגיעים אליו</span>'
            '<span><i class="wj-key-goal"></i>החלוקה : 4 ו-4</span><span><i class="wj-key-never"></i>מצב שלא מגיעים אליו</span>'
            '<span><i class="wj-key-best"></i>7 המזיגות, מתחילים מ-8 ל-5</span><span><i class="wj-key-alt"></i>8 המזיגות, מתחילים מ-8 ל-3</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [
        statement_figure(),
        statement_legend(),
        plan_stepper((A, B), PLAN, (0, 0), NAMES, "ששת הצעדים שמביאים 4 ליטר לכד B, צעד אחרי צעד"),
        plan_table(PLAN),
        other_table(),
        grid2(),
        grid2_legend(),
        examples_table(),
        plan3_stepper(),
        plan3_table(),
        grid3(),
        grid3_legend(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
