#!/usr/bin/env python3
"""Figures and tables of question 0070 (the shortest path in a grid: BFS over the open
cells, BFS over the states (cell, breaks left) when up to k walls may be broken, and
Dijkstra when every cell has an entry cost).

    python tools/figures/fill.py 70        # put the blocks on the page

The references here are independent of the page code: dist_ref() is a BFS over a dict,
breaks_ref() a BFS over every state (cell, breaks left) without the page's pruning,
cost_ref() relaxes every move until nothing changes (Bellman-Ford). trace() replays the
three searches pop by pop exactly as the page's code runs them (the frames of the gridpath
explorer and the rows of the tables); naive_breaks() is the wrong BFS of the trap (one
visit per cell), astar() and zero_one_bfs() are the follow-ups. blocks() returns, in page
order: the example with its BFS distances and path (four and eight directions), its
legend, the table of the layers, the table of the rules of a diagonal step, the
counterexample grid of part b with the two runs, the answer for every k, the terrain of
part c with the two paths, its legend, the table of the two paths and the table of the
pops of Dijkstra.
"""

import heapq
import re
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = "\u00a0"
# the maze of parts a and b: a wall in column 2 open at the bottom, a zigzag wall in
# columns 4 and 5 open at the bottom, a wall in column 7 open at the top
GRID = ["001010000", "001001010", "001010010", "001001010", "001010010", "001001010", "000000010"]
S, T = (3, 0), (3, 8)
CE_GRID, CE_S, CE_T, CE_K = ["001", "101", "010"], (0, 0), (2, 2), 1      # the trap of part b
# the terrain of part c: a road on the border (1), mud (5) and a mountain (9) inside, one
# mud cell on the bottom road
COST = ["1111111", "1559551", "1599951", "1599951", "1559551", "1115111"]
CS, CT = (2, 0), (3, 6)
KMAX = 4
# the self-checks
SC_GRID = ["0000", "1110", "0000", "0111"]
SC_A = (SC_GRID, (3, 0), (0, 0))                                           # part a: 9
SC_B = (SC_GRID, (3, 0), (0, 0), 1)                                        # part b: 3
SC_C = (["191", "151", "111"], (0, 0), (0, 2))                             # part c: 6

DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
DIR_HEB = ["למעלה", "למטה", "שמאלה", "ימינה", "למעלה-שמאלה", "למעלה-ימינה", "למטה-שמאלה", "למטה-ימינה"]


def wall_of(mode):
    return "#" if mode == "c" else "1"


def moves(grid, r, c, diag, wall="1", cut=False):
    """The moves out of (r, c) in the order of the table, as [a, b, k, squeezed]: a diagonal
    between two walls is squeezed (not a move unless cut, the follow-up's rule)."""
    m, n = len(grid), len(grid[0])
    out = []
    for k, (dr, dc) in enumerate(DIRS8 if diag else DIRS4):
        a, b = r + dr, c + dc
        if not (0 <= a < m and 0 <= b < n):
            continue
        sq = bool(dr and dc and grid[r][b] == wall and grid[a][c] == wall)
        out.append([a, b, k, sq and not cut])
    return out


def nbrs(grid, r, c, diag, wall="1", cut=False):
    return [(a, b) for a, b, _, sq in moves(grid, r, c, diag, wall, cut) if not sq]


# --- references -------------------------------------------------------------------------------

def dist_ref(grid, s, diag=False, cut=False):
    """The number of steps from s to every open cell (a dict), by a plain BFS."""
    d, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        for v in nbrs(grid, *u, diag, cut=cut):
            if grid[v[0]][v[1]] == "0" and v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def length_ref(grid, s, t, diag=False, cut=False):
    return dist_ref(grid, s, diag, cut).get(t, -1)


def breaks_ref(grid, s, t, k, diag=False):
    """BFS over every state (cell, breaks left), each state visited once, no pruning."""
    seen, q = {(s, k)}, deque([(s, k, 0)])
    while q:
        u, left, d = q.popleft()
        if u == t:
            return d
        for v in nbrs(grid, *u, diag):
            rest = left - (grid[v[0]][v[1]] == "1")
            if rest >= 0 and (v, rest) not in seen:
                seen.add((v, rest))
                q.append((v, rest, d + 1))
    return -1


def naive_breaks(grid, s, t, k, diag=False):
    """The trap: a BFS that visits every cell once, with the breaks left of its first visit."""
    seen, q = {s}, deque([(s, k, 0)])
    while q:
        u, left, d = q.popleft()
        if u == t:
            return d
        for v in nbrs(grid, *u, diag):
            rest = left - (grid[v[0]][v[1]] == "1")
            if rest >= 0 and v not in seen:
                seen.add(v)
                q.append((v, rest, d + 1))
    return -1


def cost_ref(grid, s, diag=False):
    """The least entry cost from s to every cell, by relaxing every move until nothing
    changes; walls '#' are never entered."""
    m, n = len(grid), len(grid[0])
    inf = float("inf")
    best = {(r, c): inf for r in range(m) for c in range(n)}
    best[s] = 0
    changed = True
    while changed:
        changed = False
        for (r, c), d in list(best.items()):
            if d == inf:
                continue
            for a, b in nbrs(grid, r, c, diag, "#"):
                if grid[a][b] != "#" and d + int(grid[a][b]) < best[(a, b)]:
                    best[(a, b)] = d + int(grid[a][b])
                    changed = True
    return best


def cheapest_ref(grid, s, t, diag=False):
    v = cost_ref(grid, s, diag)[t]
    return -1 if v == float("inf") else v


def path_cost(grid, path):
    return sum(int(grid[r][c]) for r, c in path[1:])


def fewest_steps_costs(grid, s, t, diag=False):
    """The cost of the BFS path (the first one found) and the least cost of any path with
    the fewest steps: a BFS by layers keeps per cell the least cost among the shortest."""
    ones = ["".join("1" if ch == "#" else "0" for ch in row) for row in grid]
    d = dist_ref(ones, s, diag)
    best = {s: 0}
    for u in sorted(d, key=lambda x: d[x]):
        for v in nbrs(ones, *u, diag):
            if v in d and d[v] == d[u] + 1:
                cand = best[u] + int(grid[v[0]][v[1]])
                if cand < best.get(v, float("inf")):
                    best[v] = cand
    return d[t], best[t]


# --- the page's three searches, pop by pop --------------------------------------------------------

def trace(mode, grid, s, t, diag=False, k=0):
    """The search of the mode ("a" BFS, "b" BFS over (cell, breaks left), "c" Dijkstra) pop
    by pop, as the page's code runs it. A frame per pop: kind "pop", "goal" (t popped: the
    end, with the path) or "skip" (a stale heap entry), and a last "none" frame when the
    queue empties without t. Every frame carries the popped cell and its value (d, and left
    in mode b), the moves checked as [a, b, why, value] (why: squeeze, wall, seen, push in
    mode a; squeeze, nobreak, worse, push in b; squeeze, wall, noimp, push in c), the
    frontier after it (cells in a, [r, c, left, d] in b, [d, r, c] sorted in c) and the
    values of every cell (a: the distance, b: the most breaks left and the distance of that
    state, c: the cost; -1 for none)."""
    m, n = len(grid), len(grid[0])
    wall = wall_of(mode)
    frames = []
    val = [[-1] * n for _ in range(m)]
    dst = [[-1] * n for _ in range(m)]
    par = {}

    def snap(kind, cell, d, nb, front, left=None, path=None):
        f = {"kind": kind, "cell": cell, "d": d, "left": left, "nb": nb, "front": front,
             "val": [row[:] for row in val], "dst": [row[:] for row in dst] if mode == "b" else None, "path": path}
        frames.append(f)

    def walk(key, cell_of):
        out = []
        while key is not None:
            out.append(list(cell_of(key)))
            key = par[key]
        return out[::-1]

    if mode == "a":
        val[s[0]][s[1]] = 0
        par[s] = None
        q = deque([s])
        while q:
            r, c = q.popleft()
            if (r, c) == t:
                snap("goal", [r, c], val[r][c], [], [list(x) for x in q], path=walk((r, c), lambda x: x))
                return frames
            nb = []
            for a, b, _, sq in moves(grid, r, c, diag, wall):
                if sq:
                    nb.append([a, b, "squeeze", None])
                elif grid[a][b] != "0":
                    nb.append([a, b, "wall", None])
                elif val[a][b] >= 0:
                    nb.append([a, b, "seen", val[a][b]])
                else:
                    val[a][b] = val[r][c] + 1
                    par[(a, b)] = (r, c)
                    q.append((a, b))
                    nb.append([a, b, "push", val[a][b]])
            snap("pop", [r, c], val[r][c], nb, [list(x) for x in q])
    elif mode == "b":
        val[s[0]][s[1]] = k
        dst[s[0]][s[1]] = 0
        par[(s[0], s[1], k)] = None
        q = deque([(s[0], s[1], k, 0)])
        while q:
            r, c, left, d = q.popleft()
            if (r, c) == t:
                snap("goal", [r, c], d, [], [list(x) for x in q], left, path=walk((r, c, left), lambda x: x[:2]))
                return frames
            nb = []
            for a, b, _, sq in moves(grid, r, c, diag, wall):
                rest = left - (grid[a][b] == "1")
                if sq:
                    nb.append([a, b, "squeeze", None])
                elif rest < 0:
                    nb.append([a, b, "nobreak", rest])
                elif rest <= val[a][b]:
                    nb.append([a, b, "worse", rest])
                else:
                    val[a][b] = rest
                    dst[a][b] = d + 1
                    par[(a, b, rest)] = (r, c, left)
                    q.append((a, b, rest, d + 1))
                    nb.append([a, b, "push", rest])
            snap("pop", [r, c], d, nb, [list(x) for x in q], left)
    else:
        val[s[0]][s[1]] = 0
        par[s] = None
        heap = [(0, s[0], s[1])]
        while heap:
            d, r, c = heapq.heappop(heap)
            if d > val[r][c]:
                snap("skip", [r, c], d, [], [list(x) for x in sorted(heap)])
                continue
            if (r, c) == t:
                snap("goal", [r, c], d, [], [list(x) for x in sorted(heap)], path=walk((r, c), lambda x: x))
                return frames
            nb = []
            for a, b, _, sq in moves(grid, r, c, diag, wall):
                if sq:
                    nb.append([a, b, "squeeze", None])
                elif grid[a][b] == "#":
                    nb.append([a, b, "wall", None])
                else:
                    nd = d + int(grid[a][b])
                    if val[a][b] < 0 or nd < val[a][b]:
                        val[a][b] = nd
                        par[(a, b)] = (r, c)
                        heapq.heappush(heap, (nd, a, b))
                        nb.append([a, b, "push", nd])
                    else:
                        nb.append([a, b, "noimp", nd])
            snap("pop", [r, c], d, nb, [list(x) for x in sorted(heap)])
    snap("none", None, -1, [], [])
    return frames


def answer_of(frames):
    return frames[-1]["d"] if frames[-1]["kind"] == "goal" else -1


# --- follow-ups -------------------------------------------------------------------------------------

def astar(grid, s, t, diag=False):
    """A* with the entry costs: h is the number of steps left (Manhattan, or Chebyshev with
    diagonals) times the least cost of a cell, which never overestimates. Returns the cost
    and the number of pops (stale entries skipped)."""
    m, n = len(grid), len(grid[0])
    cmin = min(int(ch) for row in grid for ch in row if ch != "#")

    def h(r, c):
        dr, dc = abs(r - t[0]), abs(c - t[1])
        return cmin * (max(dr, dc) if diag else dr + dc)

    g = {s: 0}
    heap, pops = [(h(*s), 0, s)], 0
    while heap:
        f, d, u = heapq.heappop(heap)
        if d > g[u]:
            continue
        pops += 1
        if u == t:
            return d, pops
        for a, b in nbrs(grid, *u, diag, "#"):
            if grid[a][b] != "#":
                nd = d + int(grid[a][b])
                if nd < g.get((a, b), float("inf")):
                    g[(a, b)] = nd
                    heapq.heappush(heap, (nd + h(a, b), nd, (a, b)))
    return -1, pops


def dijkstra_pops(grid, s, t, diag=False):
    return sum(1 for f in trace("c", grid, s, t, diag) if f["kind"] in ("pop", "goal"))


def zero_one_bfs(grid, s, t, diag=False):
    """Costs 0 and 1 ('0' and '1' entry costs): a deque, a 0 move to the front and a 1 move
    to the back; returns the least cost."""
    m, n = len(grid), len(grid[0])
    best = {s: 0}
    dq = deque([s])
    done = set()
    while dq:
        u = dq.popleft()
        if u in done:
            continue
        done.add(u)
        for a, b in nbrs(grid, *u, diag, "#"):
            w = int(grid[a][b])
            if best[u] + w < best.get((a, b), float("inf")):
                best[(a, b)] = best[u] + w
                (dq.appendleft if w == 0 else dq.append)((a, b))
    return best.get(t, -1)


def multi_target(grid, s, targets, diag=False):
    """The steps to the nearest of several targets: one BFS, stopped at the first target
    that leaves the queue."""
    d, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        if u in targets:
            return d[u], u
        for v in nbrs(grid, *u, diag):
            if grid[v[0]][v[1]] == "0" and v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return -1, None


# --- blocks -----------------------------------------------------------------------------------------

def cell_name(r, c):
    return f"({r}, {c})"


def ltr(x):
    return f'<span dir="ltr">{x}</span>'


def grid_svg(grid, s, t, label, values=None, path=None, ghost=None, mode="a", squeeze=(), broken=()):
    """A grid: walls dark, the start S and the target T, a value per cell (the BFS distance
    or the cost so far), the terrain cost in the corner of every cell in mode c, the path
    as a line from centre to centre, a second path dashed (ghost), the squeezed diagonals
    as crossed marks and the broken walls of part b."""
    m, n = len(grid), len(grid[0])
    cs, lw, top = 34, 24, 22
    W, H = lw + n * cs + 6, top + m * cs + 6
    wall = wall_of(mode)
    s_ = (f'<svg class="figure gx-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">')
    for c in range(n):
        s_ += f'<text class="tick" x="{lw + c * cs + cs / 2:g}" y="14" text-anchor="middle">{c}</text>'
    for r in range(m):
        s_ += f'<text class="tick" x="{lw - 7}" y="{top + r * cs + cs / 2 + 4:g}" text-anchor="end">{r}</text>'
    texts = ""                                 # the text goes over the path lines
    for r in range(m):
        for c in range(n):
            x, y = lw + c * cs, top + r * cs
            ch = grid[r][c]
            v = values.get((r, c)) if values is not None else None
            if ch == wall:
                cls, what = "is-wall", "wall"
                if (r, c) in broken:
                    cls, what = "is-broken", "a wall broken on the way"
            else:
                cls, what = "is-open", "open"
                if mode == "c":
                    cls += f" gx-t{(int(ch) - 1) // 3 + 1}"
                    what = f"entry cost {ch}"
                if v is not None:
                    cls += " is-seen"
            tag = "S" if (r, c) == s else "T" if (r, c) == t else ""
            tip = f"cell {cell_name(r, c)}: {what}" + (f", {'cost' if mode == 'c' else 'distance'} {v}" if v is not None else "") + \
                (", the start" if tag == "S" else ", the target" if tag == "T" else "")
            s_ += (f'<g class="gx-cell {cls}"><title>{tip}</title>'
                   f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{cs - 3}" height="{cs - 3}" rx="3"/>')
            s_ += "</g>"
            if tag:
                texts += f'<text class="gx-tag" x="{x + 4}" y="{y + 12}">{tag}</text>'
            if mode == "c" and ch != "#":
                texts += f'<text class="gx-cost" x="{x + cs - 4}" y="{y + 12}" text-anchor="end">{ch}</text>'
            if v is not None:
                texts += f'<text class="gx-val" x="{x + cs / 2:g}" y="{y + cs / 2 + (8 if mode == "c" or tag else 5):g}" text-anchor="middle">{v}</text>'

    cx = lambda c: lw + c * cs + cs / 2   # noqa: E731
    cy = lambda r: top + r * cs + cs / 2  # noqa: E731
    for (r, c), (a, b) in squeeze:
        mx, my = (cx(c) + cx(b)) / 2, (cy(r) + cy(a)) / 2
        s_ += (f'<g class="gx-squeeze"><title>a diagonal between two walls: {cell_name(r, c)} to {cell_name(a, b)} is not a move</title>'
               f'<line x1="{mx - 5:g}" y1="{my - 5:g}" x2="{mx + 5:g}" y2="{my + 5:g}"/><line x1="{mx - 5:g}" y1="{my + 5:g}" x2="{mx + 5:g}" y2="{my - 5:g}"/></g>')
    for p, cls in ((ghost, "gx-path is-ghost"), (path, "gx-path")):
        if p:
            pts = " ".join(f"{cx(c):g},{cy(r):g}" for r, c in p)
            s_ += f'<polyline class="{cls}" points="{pts}"><title>{"the fewest steps (BFS)" if "ghost" in cls else "the path"}: {len(p) - 1} steps</title></polyline>'
    return s_ + texts + "</svg>"


def legend(mode="a", ghost=False, squeeze=False, broken=False):
    keys = '<span><i class="gx-key-s"></i>S ההתחלה, T היעד</span>'
    if mode == "c":
        keys += ('<span><i class="gx-key gx-t1"></i>כביש, 1 עד 3</span><span><i class="gx-key gx-t2"></i>בוץ, 4 עד 6</span>'
                 '<span><i class="gx-key gx-t3"></i>הר, 7 עד 9</span>')
    else:
        keys += '<span><i class="gx-key is-open"></i>תא פתוח</span><span><i class="gx-key is-wall"></i>קיר</span>'
    if broken:
        keys += '<span><i class="gx-key is-broken"></i>קיר שנשבר בדרך</span>'
    keys += '<span><i class="gx-key-path"></i>המסלול</span>'
    if ghost:
        keys += '<span><i class="gx-key-ghost"></i>המסלול עם הכי מעט צעדים (BFS)</span>'
    if squeeze:
        keys += '<span><i class="gx-key-squeeze"></i>אלכסון בין שני קירות : אסור</span>'
    return f'<span class="viz-legend">{keys}</span>'


def squeezes(grid, wall="1"):
    """Every diagonal between two open cells whose two side cells are walls."""
    m, n = len(grid), len(grid[0])
    out = []
    for r in range(m - 1):
        for c in range(n):
            for dc in (-1, 1):
                b = c + dc
                if 0 <= b < n and grid[r][c] != wall and grid[r + 1][b] != wall and grid[r][b] == wall and grid[r + 1][c] == wall:
                    out.append(((r, c), (r + 1, b)))
    return out


def qtext(cells):
    return ltr(" ".join(f"({r},{c})" for r, c in cells)) if cells else "ריק"


def table_layers(grid, s, t, diag=False):
    """The BFS layers of the example: the distance, the cells at that distance (the order
    they enter the queue), and how many."""
    fr = trace("a", grid, s, t, diag)
    order = []
    for f in fr:
        for a, b, why, v in f["nb"]:
            if why == "push":
                order.append(((a, b), v))
    by = {}
    for cell, v in [((s[0], s[1]), 0)] + order:
        by.setdefault(v, []).append(cell)
    rows = ["| המרחק | התאים במרחק הזה, בסדר הכניסה לתור | כמה |", "|:-:|:--|:-:|"]
    for v in sorted(by):
        cells = by[v]
        mark = " (**T**)" if tuple(t) in cells else ""
        rows.append(f"| {RLM}{v} | {RLM}{qtext(cells)}{mark} | {RLM}{len(cells)} |")
    return "\n".join(rows)


def table_rules(grid, s, t):
    """The length of the example under the three rules of a diagonal step."""
    rows = ["| הצעדים המותרים | אורך המסלול הקצר | מה קובע |", "|:--|:-:|:--|"]
    rows.append(f"| ארבעה כיוונים | {RLM}{length_ref(grid, s, t)} | שלושת הקירות, כל אחד עוקפים דרך הפתח שלו |")
    rows.append(f"| שמונה כיוונים, בלי לעבור בין שני קירות (הכלל שלנו) | {RLM}{length_ref(grid, s, t, True)} | צעד באלכסון חוסך בפינות, אבל קיר הזיגזג עדיין סגור |")
    rows.append(f"| שמונה כיוונים, גם בין שני קירות (שאלת המשך) | {RLM}{length_ref(grid, s, t, True, cut=True)} | המסלול חוצה את קיר הזיגזג באלכסון, בין שתי פינות של קירות |")
    return "\n".join(rows)


def table_run_b(grid, s, t, k, naive):
    """Part b's trap and fix on the small grid, pop by pop: the state, the moves checked,
    the queue after."""
    rows = ["| הצעד | יוצא מהתור | המהלכים שנבדקים | התור אחרי |", "|:-:|:-:|:--|:--|"]
    seen, q, step = {s}, deque([(s, k, 0)]), 0
    best = {s: k}

    def state(u, left, d):
        return ltr(f"({u[0]},{u[1]},{left},{d})")

    def queue():
        return ltr(" ".join(f"({v[0]},{v[1]},{lf},{dd})" for v, lf, dd in q)) if q else "ריק"

    while q:
        u, left, d = q.popleft()
        step += 1
        if u == t:
            rows.append(f"| {RLM}{step} | {RLM}{state(u, left, d)} | **היעד** : התשובה {d} | {RLM}{queue()} |")
            return "\n".join(rows)
        parts = []
        for a, b, kk, sq in moves(grid, *u, False):
            v = (a, b)
            wallc = grid[a][b] == "1"
            rest = left - wallc
            name = f"{DIR_HEB[kk]} {ltr(cell_name(a, b))}{' קיר' if wallc else ''}"
            if rest < 0:
                parts.append(f"{name} : אין שבירות")
            elif naive and v in seen:
                parts.append(f"{name} : כבר סומן")
            elif not naive and rest <= best.get(v, -1):
                parts.append(f"{name} : {rest} לא יותר מ-{best[v]}")
            else:
                if naive:
                    seen.add(v)
                else:
                    best[v] = rest
                q.append((v, rest, d + 1))
                parts.append(f"{name} : **נכנס עם {rest}**")
        rows.append(f"| {RLM}{step} | {RLM}{state(u, left, d)} | {'; '.join(parts)} | {RLM}{queue()} |")
    rows.append(f"| {RLM}{step + 1} | — | התור ריק : התשובה <span dir=\"ltr\">−1</span> | ריק |")
    return "\n".join(rows)


def sval(v):
    return ltr("−1") if v < 0 else f"{RLM}{v}"


def table_k(grid, s, t):
    """The answer of part b for every k, four and eight directions."""
    head = "| הצעדים | " + " | ".join(f"‏k = {k}" for k in range(KMAX + 1)) + " |"
    rows = [head, "|:--|" + ":-:|" * (KMAX + 1)]
    for diag, name in ((False, "ארבעה כיוונים"), (True, "שמונה כיוונים")):
        rows.append(f"| {name} | " + " | ".join(sval(breaks_ref(grid, s, t, k, diag)) for k in range(KMAX + 1)) + " |")
    return "\n".join(rows)


def table_paths(grid, s, t):
    """Part c: the BFS path (fewest steps) against Dijkstra's (cheapest)."""
    fb = trace("a", ["".join("1" if ch == "#" else "0" for ch in row) for row in grid], s, t)
    bp = fb[-1]["path"]
    cp = trace("c", grid, s, t)[-1]["path"]
    steps, best_short = fewest_steps_costs(grid, s, t)
    rows = ["| המסלול | צעדים | העלויות של התאים שנכנסים אליהם | העלות |", "|:--|:-:|:--|:-:|"]
    rows.append(f"| ‏BFS : הכי מעט צעדים | {RLM}{len(bp) - 1} | {RLM}{ltr(' + '.join(grid[r][c] for r, c in bp[1:]))} | {RLM}{path_cost(grid, bp)} |")
    rows.append(f"| ‏Dijkstra : הכי זול | {RLM}{len(cp) - 1} | {RLM}{ltr(' + '.join(grid[r][c] for r, c in cp[1:]))} | {RLM}{path_cost(grid, cp)} |")
    rows.append(f"| הזול ביותר מבין המסלולים של {steps} צעדים | {RLM}{steps} | — | {RLM}{best_short} |")
    return "\n".join(rows)


def table_pops(grid, s, t):
    """Part c: every pop of Dijkstra on the terrain, with the cells pushed, as cell=cost."""
    rows = ["| הצעד | יוצא מהערימה (תא=עלות) | נכנסים לערימה (תא=עלות) | בערימה אחרי |", "|:-:|:-:|:--|:-:|"]
    for i, f in enumerate(trace("c", grid, s, t)):
        r, c = f["cell"]
        out = ltr(f"({r},{c})={f['d']}")
        if f["kind"] == "goal":
            pushed = "**היעד** : העלות הסופית"
        else:
            p = [f"({a},{b})={v}" for a, b, why, v in f["nb"] if why == "push"]
            pushed = RLM + ltr("&nbsp; ".join(p)) if p else "אף תא : לכל השכנים כבר יש עלות קטנה או שווה"
        rows.append(f"| {RLM}{i + 1} | {RLM}{out} | {pushed} | {RLM}{len(f['front'])} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    fa = trace("a", GRID, S, T)
    da = {(r, c): v for r, row in enumerate(fa[-1]["val"]) for c, v in enumerate(row) if v >= 0}
    f8 = trace("a", GRID, S, T, True)
    d8 = {(r, c): v for r, row in enumerate(f8[-1]["val"]) for c, v in enumerate(row) if v >= 0}
    fb = trace("b", GRID, S, T, False, 1)
    broken = {tuple(x) for x in fb[-1]["path"] if GRID[x[0]][x[1]] == "1"}
    fc = trace("c", COST, CS, CT)
    dc = {(r, c): v for r, row in enumerate(fc[-1]["val"]) for c, v in enumerate(row) if v >= 0}
    ghost = trace("a", ["0" * len(COST[0])] * len(COST), CS, CT)[-1]["path"]
    out = [
        grid_svg(GRID, S, T, "הדוגמה : לוח 7 על 9 עם שלושה קירות, ההתחלה S משמאל והיעד T מימין ; בכל תא המרחק שלו מ-S ב-BFS של ארבעה כיוונים, והמסלול הקצר מסומן",
                 values=da, path=fa[-1]["path"]),
        legend(),
        table_layers(GRID, S, T),
        grid_svg(GRID, S, T, "אותו לוח עם שמונה כיוונים : המרחקים והמסלול הקצר, והאלכסונים בין שני קירות מסומנים באיקס",
                 values=d8, path=f8[-1]["path"], squeeze=squeezes(GRID)),
        legend(squeeze=True),
        table_rules(GRID, S, T),
        grid_svg(CE_GRID, CE_S, CE_T, "הלוח הקטן של המלכודת : 3 על 3, ההתחלה בפינה השמאלית העליונה והיעד בפינה הימנית התחתונה"),
        table_run_b(CE_GRID, CE_S, CE_T, CE_K, naive=True),
        table_run_b(CE_GRID, CE_S, CE_T, CE_K, naive=False),
        grid_svg(GRID, S, T, "הדוגמה עם k = 1 : המסלול של 14 צעדים שובר את הקיר של עמודה 7", values=None, path=fb[-1]["path"], broken=broken),
        legend(broken=True),
        table_k(GRID, S, T),
        grid_svg(COST, CS, CT, "השטח של סעיף ג : כביש מסביב, בוץ והר באמצע ; בכל תא העלות הקטנה ביותר להגיע אליו (בפינה עלות הכניסה), המסלול הזול רציף ומסלול ה-BFS מקווקו",
                 values=dc, path=fc[-1]["path"], ghost=ghost, mode="c"),
        legend("c", ghost=True),
        table_paths(COST, CS, CT),
        table_pops(COST, CS, CT),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", b) for b in out]   # the colon rule of the Hebrew text


if __name__ == "__main__":
    print("a", length_ref(GRID, S, T), length_ref(GRID, S, T, True), length_ref(GRID, S, T, True, cut=True))
    print("b", [breaks_ref(GRID, S, T, k) for k in range(5)], [breaks_ref(GRID, S, T, k, True) for k in range(5)])
    print("ce", naive_breaks(CE_GRID, CE_S, CE_T, 1), breaks_ref(CE_GRID, CE_S, CE_T, 1))
    print("c", cheapest_ref(COST, CS, CT), cheapest_ref(COST, CS, CT, True), fewest_steps_costs(COST, CS, CT))
    print("sc", length_ref(*SC_A), breaks_ref(*SC_B), cheapest_ref(*SC_C))
    print("astar", astar(COST, CS, CT), dijkstra_pops(COST, CS, CT), astar(COST, CS, CT, True), dijkstra_pops(COST, CS, CT, True))
    print("pops", len(trace("a", GRID, S, T)), len(trace("a", GRID, S, T, True)), len(trace("b", GRID, S, T, False, 1)), len(trace("c", COST, CS, CT)))
