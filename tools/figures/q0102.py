#!/usr/bin/env python3
"""Figures and tables of question 0102, topological sort: an order to run tasks that depend
on one another, a cycle that makes one impossible, and the critical path when tasks run in
parallel.

    python tools/figures/fill.py 102        # put the blocks on the page

The tasks are 0..n-1, shown as the letters A, B, C, ...; an edge (a, b) means "b after a".
The references here are independent of the page code:

- all_orders(n, edges) lists every valid order by backtracking (small graphs only), and
  valid(n, edges, order) checks one by positions;
- has_cycle(n, edges) is the transitive closure: a task that reaches itself;
- kahn_events(n, edges, dur) is the Kahn of part a event by event, as the box steps it
  (docs/javascripts/explorer/toposort.js): a pop takes the front of the queue, a lower
  takes one edge out of it, and done names the tasks left and one cycle among them
  (find_cycle: from the smallest task left, walk back through the smallest predecessor
  left until a task repeats), and, without a cycle, the total time and the slack of part c;
- dfs_times(n, edges) is the DFS of part b with entry and exit times, and dfs_back the
  grey path and the back edge it finds on a graph with a cycle;
- longest(n, edges, dur) is the critical path of part c by walking every path.

blocks() returns, in page order: the example graph and its table of tasks, the graph by
Kahn rounds with the in-degrees and its legend, the table of Kahn's steps, the example with
one more edge (the cycle) and its legend, the table of the in-degrees left, the DFS table,
the graph at the back edge and its legend, the diamond of the two-colour trap, the Gantt
chart of part c and its legend, and the table of the times of part c.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from charts import Chart  # noqa: E402

RLM = "‏"
NB = " "
NAMES = "ABCDEFGH"
A, B, C, D, E, F, G = range(7)
N = 7
# the example: B after A, C after A and after E, D after B and C, F after D, G after F
EDGES = [(A, B), (A, C), (E, C), (B, D), (C, D), (D, F), (F, G)]
CYCLE_EDGES = EDGES + [(D, E)]       # the register model now needs the elaborated design
DUR = [3, 2, 4, 1, 5, 1, 4]          # part c: minutes per task
DIAMOND = [(0, 1), (0, 2), (1, 3), (2, 3)]
TASKS = [
    ("קומפילציה של הספריות המשותפות", "–"),
    ("קומפילציה של ה-RTL", "A"),
    ("קומפילציה של סביבת האימות", "A, E"),
    ("‏elaboration של ה-RTL עם הסביבה", "B, C"),
    ("יצירת מודל הרגיסטרים (RAL) מהמפרט", "–"),
    ("בדיקת sanity קצרה", "D"),
    ("הרגרסיה המלאה", "F"),
]


def name(v: int) -> str:
    return NAMES[v]


def names(vs) -> str:
    return " ".join(NAMES[v] for v in vs)


def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


# --- the references -------------------------------------------------------------------------

def valid(n: int, edges, order) -> bool:
    """Every task once, and a before b for every edge (a, b)."""
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in edges)


def all_orders(n: int, edges) -> list[tuple[int, ...]]:
    """Every valid order, by backtracking over the tasks whose predecessors are all placed."""
    preds = [set() for _ in range(n)]
    for a, b in edges:
        preds[b].add(a)
    out, cur, used = [], [], set()

    def go():
        if len(cur) == n:
            out.append(tuple(cur))
            return
        for v in range(n):
            if v not in used and preds[v] <= used:
                used.add(v)
                cur.append(v)
                go()
                cur.pop()
                used.discard(v)

    go()
    return out


def closure(n: int, edges) -> list[list[bool]]:
    r = [[False] * n for _ in range(n)]
    for a, b in edges:
        r[a][b] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    if r[k][j]:
                        r[i][j] = True
    return r


def has_cycle(n: int, edges) -> bool:
    r = closure(n, edges)
    return any(r[v][v] for v in range(n))


def is_cycle(edges, cyc) -> bool:
    """cyc is a cycle of the graph: an edge from every task to the next, and the last to the first."""
    es = set(map(tuple, edges))
    return len(cyc) >= 1 and len(set(cyc)) == len(cyc) and all((cyc[i], cyc[(i + 1) % len(cyc)]) in es for i in range(len(cyc)))


def levels(n: int, edges) -> list[list[int]]:
    """Kahn by rounds: every round takes all the tasks whose in-degree is 0 at once."""
    indeg = [0] * n
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
        indeg[b] += 1
    cur = [v for v in range(n) if indeg[v] == 0]
    out = []
    while cur:
        out.append(cur)
        nxt = []
        for u in cur:
            for v in succ[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        cur = sorted(nxt)
    return out


def find_cycle(n: int, edges, left) -> list[int]:
    """A cycle among the tasks left when Kahn stops: each of them still has a predecessor
    left, so walking back from the smallest one, always to the smallest predecessor left,
    repeats a task; the walk between the two visits, read forward, is a cycle. It is given
    from its smallest task."""
    rest = set(left)
    cur, seen, path = min(rest), {}, []
    while cur not in seen:
        seen[cur] = len(path)
        path.append(cur)
        cur = min(a for a, b in edges if b == cur and a in rest)
    cyc = path[seen[cur]:][::-1]
    k = cyc.index(min(cyc))
    return cyc[k:] + cyc[:k]


def kahn_events(n: int, edges, dur=None) -> list[dict]:
    """Kahn's algorithm event by event, as the box steps it. Successors in the order of the
    edge list; the queue starts with the tasks of in-degree 0 in index order. Every event
    keeps the in-degrees, the queue, the order so far and the earliest starts after it."""
    dur = list(dur) if dur is not None else [1] * n
    succ = [[] for _ in range(n)]
    indeg = [0] * n
    for i, (a, b) in enumerate(edges):
        succ[a].append((b, i))
        indeg[b] += 1
    q = [v for v in range(n) if indeg[v] == 0]
    order, start, ev = [], [0] * n, []

    def rec(**e):
        ev.append({**e, "indeg": indeg[:], "q": q[:], "order": order[:], "start": start[:]})

    while q:
        u = q.pop(0)
        order.append(u)
        rec(kind="pop", u=u)
        for v, i in succ[u]:
            indeg[v] -= 1
            start[v] = max(start[v], start[u] + dur[u])
            zero = indeg[v] == 0
            if zero:
                q.append(v)
            rec(kind="lower", u=u, v=v, i=i, zero=zero)
    left = [v for v in range(n) if v not in order]
    done = {"kind": "done", "left": left, "cycle": find_cycle(n, edges, left) if left else None,
            "total": None, "slack": None}
    if not left:
        total = max((start[v] + dur[v] for v in range(n)), default=0)
        late = [total] * n
        for u in reversed(order):
            for v, _ in succ[u]:
                late[u] = min(late[u], late[v] - dur[v])
        done.update(total=total, slack=[late[v] - dur[v] - start[v] for v in range(n)], late=late)
    ev.append({**done, "indeg": indeg[:], "q": q[:], "order": order[:], "start": start[:]})
    return ev


def dfs_times(n: int, edges):
    """The DFS of part b: starts in index order, successors in edge order; the entry and
    exit times (one clock for every entry and every exit) and the order of the exits."""
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    color, d, f, exits, t = [0] * n, [0] * n, [0] * n, [], [0]

    def visit(u):
        color[u] = 1
        t[0] += 1
        d[u] = t[0]
        for v in succ[u]:
            if color[v] == 0:
                visit(v)
        color[u] = 2
        t[0] += 1
        f[u] = t[0]
        exits.append(u)

    for s in range(n):
        if color[s] == 0:
            visit(s)
    return d, f, exits


def dfs_back(n: int, edges):
    """On a graph with a cycle: the colours at the first back edge, the grey path and the
    edge (u, v) that closes it, by the same DFS."""
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    color, path = [0] * n, []

    def visit(u):
        color[u] = 1
        path.append(u)
        for v in succ[u]:
            if color[v] == 1:
                return (u, v)
            if color[v] == 0:
                hit = visit(v)
                if hit:
                    return hit
        color[u] = 2
        path.pop()
        return None

    for s in range(n):
        if color[s] == 0:
            hit = visit(s)
            if hit:
                return color[:], path[:], hit
    return color[:], [], None


def longest(n: int, edges, dur):
    """The total time with unlimited workers: the heaviest path (sum of durations), by
    walking every path from every task. None on a cycle."""
    if has_cycle(n, edges):
        return None
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    best = [0]

    def walk(u, acc):
        acc += dur[u]
        best[0] = max(best[0], acc)
        for v in succ[u]:
            walk(v, acc)

    for s in range(n):
        walk(s, 0)
    return best[0]


def times(n: int, edges, dur):
    """Earliest start and finish, latest finish and slack of every task (the end of the
    Kahn events), and the total."""
    end = kahn_events(n, edges, dur)[-1]
    es = end["start"]
    ef = [es[v] + dur[v] for v in range(n)]
    return es, ef, end["late"], end["slack"], end["total"]


# --- drawing --------------------------------------------------------------------------------

R = 16
# the example by Kahn rounds: A and E, then B and C, then D, F and G
POS = {A: (44, 52), E: (44, 132), B: (138, 52), C: (138, 132), D: (232, 92), F: (326, 92), G: (420, 92)}
W, H = 464, 184


def edge_line(p, q, curve=None, shrink_end=7):
    """A straight line or a quadratic curve from circle p to circle q, its end short of q by
    the arrowhead, and the arrowhead."""
    (x1, y1), (x2, y2) = p, q
    if curve is None:
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        ax, ay = x1 + ux * R, y1 + uy * R
        tx, ty = x2 - ux * R, y2 - uy * R
        bx, by = tx - ux * shrink_end, ty - uy * shrink_end
        line = f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>'
    else:
        cx, cy = curve
        sx, sy = cx - x1, cy - y1
        L = math.hypot(sx, sy)
        ax, ay = x1 + sx / L * R, y1 + sy / L * R
        ex, ey = x2 - cx, y2 - cy
        L = math.hypot(ex, ey)
        ux, uy = ex / L, ey / L
        tx, ty = x2 - ux * R, y2 - uy * R
        bx, by = tx - ux * shrink_end, ty - uy * shrink_end
        line = f'<path d="M{ax:.1f},{ay:.1f} Q{cx},{cy} {bx:.1f},{by:.1f}" fill="none"/>'
    head = (f'<path class="ts-head" d="M{tx:.1f},{ty:.1f} L{bx - uy * 4.5:.1f},{by + ux * 4.5:.1f} '
            f'L{bx + uy * 4.5:.1f},{by - ux * 4.5:.1f} Z"/>')
    return line + head


def graph_svg(edges, label, node_cls=None, edge_cls=None, badges=None, bands=False, curves=None, hl_text=None):
    """The example's tasks at POS with the given edges; classes per node and per edge, an
    in-degree badge per node, and the Kahn rounds as numbered bands."""
    node_cls = node_cls or {}
    edge_cls = edge_cls or {}
    curves = curves or {}
    o = [f'<svg class="figure ts-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">']
    if bands:
        for k, x in enumerate((44, 138, 232, 326, 420)):
            o.append(f'<rect class="ts-band{" is-alt" if k % 2 else ""}" x="{x - 40}" y="22" width="80" height="{H - 26}" rx="8"/>'
                     f'<g class="ts-round"><circle cx="{x}" cy="12" r="9"/><text x="{x}" y="16" text-anchor="middle">{k + 1}</text></g>')
    for i, (a, b) in enumerate(edges):
        cls = edge_cls.get(i, "")
        o.append(f'<g class="ts-edge{" " + cls if cls else ""}"><title>{name(a)} → {name(b)}: {name(b)} after {name(a)}</title>'
                 f'{edge_line(POS[a], POS[b], curves.get(i))}</g>')
    for v in sorted(POS):
        x, y = POS[v]
        cls = node_cls.get(v, "")
        o.append(f'<g class="ts-node{" " + cls if cls else ""}"><title>task {name(v)}{": " + hl_text[v] if hl_text and v in hl_text else ""}</title>'
                 f'<circle cx="{x}" cy="{y}" r="{R}"/><text x="{x}" y="{y + 5}" text-anchor="middle">{name(v)}</text></g>')
        if badges is not None:
            bx, by = x + 15, y - 22
            o.append(f'<g class="ts-badge{" is-zero" if badges[v] == 0 else ""}"><title>in-degree of {name(v)}: {badges[v]}</title>'
                     f'<rect x="{bx - 10}" y="{by - 9}" width="20" height="17" rx="5"/><text x="{bx}" y="{by + 4}" text-anchor="middle">{badges[v]}</text></g>')
    o.append("</svg>")
    return "".join(o)


def indegrees(n, edges):
    d = [0] * n
    for _, b in edges:
        d[b] += 1
    return d


def statement_figure() -> str:
    return graph_svg(EDGES, "הדוגמה : שבע משימות A עד G. חץ מ-A ל-B אומר ש-B רצה אחרי A. ‏B ו-C אחרי A, ‏C גם אחרי E, ‏D אחרי B ו-C, ‏F אחרי D ו-G אחרי F")


def tasks_table() -> str:
    rows = ["| המשימה | מה היא עושה | רצה אחרי |", "|:-:|---|:-:|"]
    preds = [[a for a, b in EDGES if b == v] for v in range(N)]
    for v, (what, after) in enumerate(TASKS):
        want = ", ".join(name(a) for a in preds[v]) or "–"
        assert want == after, (v, want, after)
        rows.append(f"| {RLM}{name(v)} | {what} | {RLM}{after} |" if after != "–" else f"| {RLM}{name(v)} | {what} | אף אחת |")
    return "\n".join(rows)


def levels_figure() -> str:
    lv = levels(N, EDGES)
    assert lv == [[A, E], [B, C], [D], [F], [G]]
    return graph_svg(EDGES, "הדוגמה לפי הסבבים של Kahn : בסבב 1 המשימות A ו-E, בלי תלות. בסבב 2 B ו-C, בסבב 3 D, בסבב 4 F ובסבב 5 G. ליד כל משימה דרגת הכניסה שלה בהתחלה",
                     node_cls={A: "is-src", E: "is-src"}, badges=indegrees(N, EDGES), bands=True)


def levels_legend() -> str:
    return ('<span class="viz-legend"><span><i class="ts-key-src"></i>דרגת כניסה 0 : אפשר להריץ מיד</span>'
            '<span><i class="ts-key-badge"></i>דרגת הכניסה : כמה משימות עוד צריכות להסתיים לפניה</span>'
            '<span><i class="ts-key-band"></i>סבב : המשימות שהדרגה שלהן מגיעה ל-0 יחד</span></span>')


def kahn_table() -> str:
    """One row per task taken out of the queue: the in-degrees it lowers, the queue after
    them, and the order so far."""
    ev = kahn_events(N, EDGES)
    rows = ["| הצעד | יוצאת מהתור | הדרגות שיורדות | התור אחרי | הסדר עד עכשיו |", "|:-:|:-:|---|:-:|:-:|"]
    step = 0
    i = 0
    while ev[i]["kind"] != "done":
        e = ev[i]
        step += 1
        u = e["u"]
        lows, j = [], i + 1
        while ev[j]["kind"] == "lower":
            x = ev[j]
            v, now = x["v"], x["indeg"][x["v"]]
            lows.append(f"{RLM}{name(v)} : {ltr(f'{now + 1} → {now}')}" + (", נכנסת לתור" if x["zero"] else ""))
            j += 1
        last = ev[j - 1]
        q = last["q"]
        rows.append(f"| {RLM}{step} | {RLM}{name(u)} | {'; '.join(lows) if lows else 'אין לה עוקבות'} | "
                    f"{RLM + ltr(names(q)) if q else 'ריק'} | {RLM}{ltr(names(last['order']))} |")
        i = j
    return "\n".join(rows)


def cycle_figure() -> str:
    ev = kahn_events(N, CYCLE_EDGES)
    end = ev[-1]
    assert end["order"] == [A, B] and end["left"] == [C, D, E, F, G] and end["cycle"] == [C, D, E]
    cyc = end["cycle"]
    on = {(cyc[k], cyc[(k + 1) % len(cyc)]) for k in range(len(cyc))}
    edge_cls = {i: "is-cycle" if (a, b) in on else "is-done" if a in end["order"] else "" for i, (a, b) in enumerate(CYCLE_EDGES)}
    node_cls = {v: "is-out" for v in end["order"]}
    node_cls.update({v: "is-cycle" if v in cyc else "is-stuck" for v in end["left"]})
    return graph_svg(CYCLE_EDGES, "הדוגמה עם עוד חץ, מ-D ל-E : ‏A ו-B יוצאות מהתור, ואז התור ריק. חמש משימות נשארות עם דרגת כניסה 1, וביניהן המעגל C, D, E ובחזרה ל-C",
                     node_cls=node_cls, edge_cls=edge_cls, badges=end["indeg"], curves={7: (150, 222)}).replace(f'viewBox="0 0 {W} {H}"', f'viewBox="0 0 {W} {H + 18}"')


def cycle_legend() -> str:
    return ('<span class="viz-legend"><span><i class="ts-key-out"></i>יצאה מהתור</span>'
            '<span><i class="ts-key-cycle"></i>המעגל</span>'
            '<span><i class="ts-key-stuck"></i>תקועה אחרי המעגל, לא עליו</span>'
            '<span><i class="ts-key-badge"></i>דרגת הכניסה שנשארה</span></span>')


def stuck_table() -> str:
    end = kahn_events(N, CYCLE_EDGES)[-1]
    left = end["left"]
    rows = ["| המשימה | " + " | ".join(RLM + name(v) for v in left) + " |", "|:-:|" + ":-:|" * len(left)]
    rows.append("| דרגת הכניסה שנשארה | " + " | ".join(str(end["indeg"][v]) for v in left) + " |")
    preds = [", ".join(name(a) for a, b in CYCLE_EDGES if b == v and a in left) for v in left]
    rows.append("| מחכה ל | " + " | ".join(f"{RLM}{p}" for p in preds) + " |")
    return "\n".join(rows)


def dfs_table() -> str:
    d, f, exits = dfs_times(N, EDGES)
    rows = ["| המשימה | נכנסים (אפורה) | יוצאים (שחורה) |", "|:-:|:-:|:-:|"]
    for v in range(N):
        rows.append(f"| {RLM}{name(v)} | {d[v]} | {f[v]} |")
    return "\n".join(rows)


def back_figure() -> str:
    color, path, (u, v) = dfs_back(N, CYCLE_EDGES)
    assert path == [A, B, D, E, C] and (u, v) == (C, D)
    node_cls = {x: "is-grey" if color[x] == 1 else "is-black" if color[x] == 2 else "" for x in range(N)}
    edge_cls = {}
    for i, (a, b) in enumerate(CYCLE_EDGES):
        if (a, b) == (u, v):
            edge_cls[i] = "is-back"
        elif a in path and b in path and path.index(b) == path.index(a) + 1:
            edge_cls[i] = "is-path"
    return graph_svg(CYCLE_EDGES, "החיפוש לעומק על הדוגמה עם המעגל : המסלול האפור A, B, D, E, C. ‏F ו-G כבר שחורות. מ-C החץ חוזר ל-D, שעדיין אפורה : קשת אחורה, והמעגל הוא D, E, C",
                     node_cls=node_cls, edge_cls=edge_cls, curves={7: (150, 222)}).replace(f'viewBox="0 0 {W} {H}"', f'viewBox="0 0 {W} {H + 18}"')


def back_legend() -> str:
    return ('<span class="viz-legend"><span><i class="ts-key-white"></i>לבנה : עוד לא נכנסנו</span>'
            '<span><i class="ts-key-grey"></i>אפורה : על המסלול הנוכחי</span>'
            '<span><i class="ts-key-black"></i>שחורה : יצאנו ממנה, כל מה שאחריה סגור</span>'
            '<span><i class="ts-key-path"></i>המסלול האפור</span>'
            '<span><i class="ts-key-back"></i>קשת אחורה, אל משימה אפורה</span></span>')


def diamond_svg() -> str:
    """The diamond A -> B, A -> C, B -> D, C -> D at the moment C looks at D: D is black."""
    pos = {0: (40, 70), 1: (130, 30), 2: (130, 110), 3: (220, 70)}
    w, h = 260, 140
    cls = {0: "is-grey", 1: "is-black", 2: "is-grey", 3: "is-black"}
    o = [f'<svg class="figure ts-fig" viewBox="0 0 {w} {h}" style="max-width:{w / 16:g}rem" role="img" '
         'aria-label="היהלום A, B, C, D ברגע ש-C מסתכלת על D : ‏D כבר שחורה, יצאנו ממנה דרך B. זה לא מעגל, ובדיקה של ביקרנו או לא הייתה מדווחת כאן מעגל בטעות">']
    for a, b in DIAMOND:
        c = " is-now" if (a, b) == (2, 3) else ""
        o.append(f'<g class="ts-edge{c}"><title>{name(a)} → {name(b)}</title>{edge_line(pos[a], pos[b])}</g>')
    for v, (x, y) in pos.items():
        o.append(f'<g class="ts-node {cls[v]}"><title>task {name(v)}</title><circle cx="{x}" cy="{y}" r="{R}"/>'
                 f'<text x="{x}" y="{y + 5}" text-anchor="middle">{name(v)}</text></g>')
    o.append("</svg>")
    return "".join(o)


def gantt_svg() -> str:
    es, ef, late, slack, total = times(N, EDGES, DUR)
    rows = N
    c = Chart(f"לוח הזמנים עם מספר לא מוגבל של מריצים : פס לכל משימה מההתחלה המוקדמת עד הסיום המוקדם. "
              f"הנתיב הקריטי E, C, D, F, G בלי מרווח, והכול נגמר בזמן {total}. ‏A ו-B יכולות להתאחר ב-2 וב-4 דקות",
              w=464, h=40 + rows * 26, x0=30, right=14, top=10, base=14 + rows * 26, x_max=16, y_max=rows, style="max-width:29rem")
    c.grid_x(range(0, 17), labels=[str(x) if x % 2 == 0 or x == total else "" for x in range(17)])
    for v in range(N):
        y = 14 + v * 26
        crit = slack[v] == 0
        c.add(f'<text class="ts-glab" x="{c.x0 - 8}" y="{y + 15}" text-anchor="end">{name(v)}</text>')
        if slack[v]:
            c.add(f'<rect class="ts-slack" x="{c.X(ef[v]):.1f}" y="{y + 5}" width="{c.X(late[v]) - c.X(ef[v]):.1f}" height="12" rx="3">'
                  f'<title>{name(v)}: slack {slack[v]}, may finish as late as {late[v]}</title></rect>')
        c.add(f'<g class="ts-bar{" is-crit" if crit else ""}"><title>{name(v)}: {DUR[v]} minutes, from {es[v]} to {ef[v]}'
              f'{", critical" if crit else f", slack {slack[v]}"}</title>'
              f'<rect x="{c.X(es[v]):.1f}" y="{y + 2}" width="{c.X(ef[v]) - c.X(es[v]):.1f}" height="18" rx="3"/>'
              f'<text x="{(c.X(es[v]) + c.X(ef[v])) / 2:.1f}" y="{y + 15}" text-anchor="middle">{DUR[v]}</text></g>')
    c.add(f'<line class="ts-total" x1="{c.X(total):.1f}" x2="{c.X(total):.1f}" y1="4" y2="{c.base}"/>')
    c.add(f'<line class="axis" x1="{c.x0}" x2="{c.x1}" y1="{c.base}" y2="{c.base}"/>')
    return c.svg().replace('class="perf-chart"', 'class="perf-chart ts-gantt"', 1)


def gantt_legend() -> str:
    return ('<span class="viz-legend"><span><i class="ts-key-crit"></i>על הנתיב הקריטי, בלי מרווח</span>'
            '<span><i class="ts-key-bar"></i>משימה עם מרווח</span>'
            '<span><i class="ts-key-slack"></i>המרווח : כמה אפשר לאחר בלי לאחר את הסוף</span>'
            '<span><i class="ts-key-total"></i>הסוף, הזמן הכולל</span>'
            '<span>המספר בפס : המשך בדקות</span></span>')


def times_table() -> str:
    es, ef, late, slack, total = times(N, EDGES, DUR)
    rows = ["| המשימה | המשך | רצה אחרי | התחלה מוקדמת | סיום מוקדם | סיום מאוחר | המרווח |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for v in range(N):
        preds = ", ".join(name(a) for a, b in EDGES if b == v)
        rows.append(f"| {RLM}{name(v)} | {DUR[v]} | {RLM + preds if preds else '–'} | {es[v]} | {ef[v]} | {late[v]} | "
                    f"{'**0**' if slack[v] == 0 else slack[v]} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    out = [
        statement_figure(),
        tasks_table(),
        levels_figure(),
        levels_legend(),
        kahn_table(),
        cycle_figure(),
        cycle_legend(),
        stuck_table(),
        dfs_table(),
        back_figure(),
        back_legend(),
        diamond_svg(),
        gantt_svg(),
        gantt_legend(),
        times_table(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    print("orders", len(all_orders(N, EDGES)))
    print("levels", levels(N, EDGES))
    print("kahn", [names(e["order"]) for e in kahn_events(N, EDGES)][-1])
    print("dfs", dfs_times(N, EDGES))
    print("back", dfs_back(N, CYCLE_EDGES))
    print("times", times(N, EDGES, DUR), longest(N, EDGES, DUR), sum(DUR))
    print(kahn_table())
