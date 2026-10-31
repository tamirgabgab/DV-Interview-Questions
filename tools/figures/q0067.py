#!/usr/bin/env python3
"""Figures and tables of question 0067 (the time a signal needs to reach every node of a
network: BFS when every link takes one time unit, Dijkstra with weighted links, and the
same Dijkstra on one-directional links).

    python tools/figures/fill.py 67        # put the blocks on the page

The references here are independent of the page code: brute_times() tries every simple
path from the source, bfs_trace() and dijkstra_trace() replay the two searches event by
event (the rows of the tables and the frames of the netdelay explorer), and
bfs_with_weights() is the trap of part b (BFS that adds up the weights of the first path
it finds). blocks() returns, in page order: the example graph of part a with its BFS tree
and its legend, the table of part a's steps, the weighted graph of part b with its
shortest-path tree, the table of part b's steps, the table of BFS against Dijkstra on the
weighted example, the directed graph of part c, and the table of part c's steps.
"""

import heapq
import math

RLM = "‏"
N = 6
K = 1
EDGES = [[1, 2, 1], [1, 3, 5], [3, 2, 1], [3, 4, 2], [2, 5, 6], [4, 5, 1], [6, 5, 1]]
EDGES_A = [[u, v] for u, v, _ in EDGES]


# --- references ---------------------------------------------------------------------------

def adjacency(n, edges, directed=False, weighted=True):
    """adj[u] = [(v, w, i), ...] in the order of the edge list (i the edge's index); an
    undirected edge is entered from both ends, and an unweighted edge weighs 1."""
    adj = [[] for _ in range(n + 1)]
    for i, e in enumerate(edges):
        u, v = e[0], e[1]
        w = e[2] if weighted else 1
        adj[u].append((v, w, i))
        if not directed:
            adj[v].append((u, w, i))
    return adj


def brute_times(n, edges, k, directed=False, weighted=True):
    """The least total weight of a path from k to every node, by trying every simple path
    (a depth-first walk that never revisits a node). None for a node no path reaches."""
    adj = adjacency(n, edges, directed, weighted)
    best = [None] * (n + 1)

    def walk(u, d, seen):
        if best[u] is None or d < best[u]:
            best[u] = d
        for v, w, _ in adj[u]:
            if v not in seen:
                walk(v, d + w, seen | {v})

    walk(k, 0, {k})
    return best[1:]


def answer_of(times):
    """The page's answer: the largest time, or -1 when some node has none."""
    return -1 if any(t is None for t in times) else max(times)


def bfs_trace(n, edges, k):
    """Part a event by event: a pop takes the front of the queue (the node is settled), a
    relax checks one link out of it (the neighbour gets t[u] + 1 and enters the queue if it
    had no time yet), and done gives the answer. Every event keeps the times after it (None
    for a node without one), the queue and the settled order."""
    adj = adjacency(n, edges, False, False)
    t = [None] * (n + 1)
    t[k] = 0
    q, order, ev = [k], [], []

    def rec(**kw):
        ev.append({**kw, "t": t[1:], "q": list(q), "order": list(order)})

    while q:
        u = q.pop(0)
        order.append(u)
        rec(kind="pop", u=u, d=t[u])
        for v, _, i in adj[u]:
            improved = t[v] is None
            if improved:
                t[v] = t[u] + 1
                q.append(v)
            rec(kind="relax", u=u, v=v, w=1, i=i, nd=t[u] + 1, improved=improved)
    rec(kind="done", ans=answer_of(t[1:]))
    return ev


def dijkstra_trace(n, edges, k, directed=False):
    """Parts b and c event by event: a pop takes the smallest (time, node) of the heap and
    settles the node, a skip drops an entry whose node is already settled with a smaller
    time (lazy deletion), a relax checks one link out of the settled node (a smaller time
    is written and pushed), and done gives the answer. Every event keeps the times, the
    heap sorted and the settled order."""
    adj = adjacency(n, edges, directed, True)
    t = [None] * (n + 1)
    t[k] = 0
    heap, settled, ev = [(0, k)], [], []

    def rec(**kw):
        ev.append({**kw, "t": t[1:], "heap": sorted(heap), "settled": list(settled)})

    while heap:
        d, u = heapq.heappop(heap)
        if d > t[u]:
            rec(kind="skip", u=u, d=d)
            continue
        settled.append(u)
        rec(kind="pop", u=u, d=d)
        for v, w, i in adj[u]:
            nd, old = d + w, t[v]
            improved = old is None or nd < old
            if improved:
                t[v] = nd
                heapq.heappush(heap, (nd, v))
            rec(kind="relax", u=u, v=v, w=w, i=i, nd=nd, old=old, improved=improved)
    rec(kind="done", ans=-1 if len(settled) < n else max(t[1:]))
    return ev


def bfs_with_weights(n, edges, k, directed=False):
    """The trap of part b: BFS that gives a node the weight of the first path that finds it
    (right only when every weight is the same)."""
    adj = adjacency(n, edges, directed, True)
    t = [None] * (n + 1)
    t[k] = 0
    q = [k]
    while q:
        u = q.pop(0)
        for v, w, _ in adj[u]:
            if t[v] is None:
                t[v] = t[u] + w
                q.append(v)
    return t[1:]


def parents(ev):
    """The link by which every node got its final time (the shortest-path tree): the last
    improving relax of each node, as {v: u}."""
    par = {}
    for e in ev:
        if e["kind"] == "relax" and e["improved"]:
            par[e["v"]] = e["u"]
    return par


# --- figures ------------------------------------------------------------------------------

W, H, CX, CY, R, NR = 300, 268, 150, 136, 82, 16


def pos(i, n):
    a = -math.pi / 2 + (i - 1) * 2 * math.pi / n
    return CX + R * math.cos(a), CY + R * math.sin(a), a


def num(v):
    return "–" if v is None else str(v).replace("-", "−")


def graph_svg(n, edges, k, times, tree, label, directed=False, weighted=True, cls=""):
    """The nodes on a circle, the links between them with their weights (an arrowhead when
    directed), the links of the shortest-path tree thick, the source marked, and the time of
    every node in a badge outside the circle (a dashed node with "−1" when no path reaches
    it)."""
    s = (f'<svg class="figure nd-fig{" " + cls if cls else ""}" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         f'aria-label="{label}">')
    P = {i: pos(i, n) for i in range(1, n + 1)}
    for u, v, *rest in edges:
        w = rest[0] if (rest and weighted) else 1
        x1, y1, _ = P[u]
        x2, y2, _ = P[v]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        ax, ay = x1 + ux * NR, y1 + uy * NR
        bx, by = x2 - ux * (NR + (7 if directed else 0)), y2 - uy * (NR + (7 if directed else 0))
        is_tree = tree.get(v) == u or (not directed and tree.get(u) == v)
        title = f"link {u} {'→' if directed else '–'} {v}" + (f", weight {w}" if weighted else "")
        s += f'<g class="nd-edge{" is-tree" if is_tree else ""}"><title>{title}</title><line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>'
        if directed:
            px, py = -uy, ux
            s += (f'<path class="nd-head" d="M{bx + ux * 7:.1f},{by + uy * 7:.1f} L{bx + px * 4.5:.1f},{by + py * 4.5:.1f} '
                  f'L{bx - px * 4.5:.1f},{by - py * 4.5:.1f} Z"/>')
        if weighted:
            mx, my = (x1 + x2) / 2 - uy * 9, (y1 + y2) / 2 + ux * 9
            s += f'<rect class="nd-wbox" x="{mx - 8:.1f}" y="{my - 8:.1f}" width="16" height="16" rx="4"/><text class="nd-w" x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle">{w}</text>'
        s += "</g>"
    for i in range(1, n + 1):
        x, y, a = P[i]
        t = times[i - 1]
        kind = "is-src" if i == k else "is-far" if t is None else "is-set"
        what = "the source" if i == k else "no path reaches it" if t is None else f"time {t}"
        s += (f'<g class="nd-node {kind}"><title>node {i}: {what}</title><circle cx="{x:.1f}" cy="{y:.1f}" r="{NR}"/>'
              f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{i}</text></g>')
        bx, by = CX + (R + 34) * math.cos(a), CY + (R + 34) * math.sin(a)
        s += (f'<g class="nd-time{" is-far" if t is None else ""}"><rect x="{bx - 15:.1f}" y="{by - 9:.1f}" width="30" height="18" rx="5"/>'
              f'<text x="{bx:.1f}" y="{by + 4:.1f}" text-anchor="middle">{"−1" if t is None else t}</text></g>')
    return s + "</svg>"


def legend(directed=False, weighted=True):
    items = [('nd-key-src', 'המקור k'), ('nd-key-node', 'צומת עם הזמן שלו בתווית'), ('nd-key-tree', 'הקשת שדרכה הגיע הזמן הסופי (עץ המסלולים הקצרים)')]
    if weighted:
        items.append(('nd-key-w', 'המשקל של הקשת, הזמן שהיא לוקחת'))
    if directed:
        items.append(('nd-key-far', 'צומת שאף מסלול לא מגיע אליו : −1'))
    return '<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{t}</span>' for c, t in items) + '</span>'


# --- tables -------------------------------------------------------------------------------

def tl(items):
    return RLM + '<span dir="ltr">' + " ".join(items) + "</span>"


def times_cell(t):
    return tl([num(x) for x in t])


def table_bfs(n, edges, k):
    """A row per pop of part a: the node taken from the queue, every link checked out of it
    and what it did, the queue after the pop's links, and the times."""
    ev = bfs_trace(n, edges, k)
    out = ["| הצעד | יוצא מהתור | הקשתות שנבדקות | התור אחרי | הזמנים של 1..6 |", "|:-:|:-:|---|:-:|:-:|"]
    step = 0
    for i, e in enumerate(ev):
        if e["kind"] != "pop":
            continue
        step += 1
        rel = []
        j = i + 1
        while j < len(ev) and ev[j]["kind"] == "relax":
            r = ev[j]
            rel.append(f"{RLM}{r['v']} : " + (f"מקבל את הזמן {r['nd']}, נכנס לתור" if r["improved"] else "כבר יש לו זמן"))
            j += 1
        last = ev[j - 1]
        q = tl([str(x) for x in last["q"]]) if last["q"] else "ריק"
        out.append(f"| {RLM}{step} | {RLM}{e['u']} (הזמן {e['d']}) | {'; '.join(rel) if rel else 'אין'} | {q} | {times_cell(last['t'])} |")
    return "\n".join(out)


def heap_cell(h):
    return tl([f"({d},{v})" for d, v in h]) if h else "ריקה"


def table_dijkstra(n, edges, k, directed=False):
    """A row per pop of parts b and c: the entry taken from the heap (settled, or skipped as
    stale), every link relaxed with the sum against the old time, the heap after, the
    settled set and the times."""
    ev = dijkstra_trace(n, edges, k, directed)
    out = ["| הצעד | יוצא מהערימה | הקשתות שנבדקות (הזמן החדש מול הישן) | הערימה אחרי | הסתיימו | הזמנים של 1..6 |",
           "|:-:|:-:|---|:-:|:-:|:-:|"]
    step = 0
    for i, e in enumerate(ev):
        if e["kind"] not in ("pop", "skip"):
            continue
        step += 1
        if e["kind"] == "skip":
            out.append(f"| {RLM}{step} | {tl([f'({e['d']},{e['u']})'])} ישנה : {e['u']} כבר הסתיים בזמן {e['t'][e['u'] - 1]}, מדלגים | אין | "
                       f"{heap_cell(e['heap'])} | {tl([str(x) for x in e['settled']])} | {times_cell(e['t'])} |")
            continue
        rel = []
        j = i + 1
        while j < len(ev) and ev[j]["kind"] == "relax":
            r = ev[j]
            old = "∞" if r["old"] is None else str(r["old"])
            rel.append(f"{RLM}{r['v']} : {RLM}<span dir=\"ltr\">{e['d']} + {r['w']} = {r['nd']}</span> " +
                       (f"מול {old}, משתפר ונכנס" if r["improved"] else f"מול {old}, לא משתפר"))
            j += 1
        last = ev[j - 1]
        out.append(f"| {RLM}{step} | {tl([f'({e['d']},{e['u']})'])} הצומת {e['u']} מסתיים | {'; '.join(rel) if rel else 'אין קשתות יוצאות'} | "
                   f"{heap_cell(last['heap'])} | {tl([str(x) for x in last['settled']])} | {times_cell(last['t'])} |")
    return "\n".join(out)


def table_bfs_vs_dijkstra(n, edges, k):
    """The trap of part b on the example: the time BFS gives every node when it adds up the
    weights of the first path, against the true shortest time."""
    wrong = bfs_with_weights(n, edges, k)
    right = brute_times(n, edges, k)
    out = ["| הצומת | ‏BFS עם משקלים (המסלול הראשון שנמצא) | הזמן הנכון (Dijkstra) | |", "|:-:|:-:|:-:|:--|"]
    for v in range(1, n + 1):
        a, b = wrong[v - 1], right[v - 1]
        note = "נכון" if a == b else f"שגוי, גדול ב-{a - b}"
        out.append(f"| {RLM}{v} | {RLM}{num(a)} | {RLM}{num(b)} | {note} |")
    out.append(f"| **המקסימום** | **{RLM}{num(answer_of(wrong))}** | **{RLM}{num(answer_of(right))}** | |")
    return "\n".join(out)


# --- blocks -------------------------------------------------------------------------------

def blocks():
    """The generated blocks, in page order."""
    ev_a = bfs_trace(N, EDGES_A, K)
    ev_b = dijkstra_trace(N, EDGES, K)
    ev_c = dijkstra_trace(N, EDGES, K, directed=True)
    fig_a = graph_svg(N, EDGES_A, K, ev_a[-1]["t"], parents(ev_a),
                      "הדוגמה : שישה צמתים על מעגל, שבע קשתות ללא משקל, המקור 1 ; ליד כל צומת הזמן שבו האות מגיע אליו, וקשתות עץ ה-BFS מודגשות",
                      weighted=False, cls="nd-a")
    fig_b = graph_svg(N, EDGES, K, ev_b[-1]["t"], parents(ev_b),
                      "הדוגמה עם משקלים : ליד כל צומת הזמן הקצר ביותר מהמקור 1, וקשתות עץ המסלולים הקצרים מודגשות", cls="nd-b")
    fig_c = graph_svg(N, EDGES, K, ev_c[-1]["t"], parents(ev_c),
                      "הדוגמה עם קשתות חד-כיווניות : הצומת 6 לא מושג, והצומת 3 מקבל את האות רק בזמן 5 דרך הקשת הישירה", directed=True, cls="nd-c")
    return [fig_a, legend(weighted=False), table_bfs(N, EDGES_A, K),
            fig_b, legend(), table_dijkstra(N, EDGES, K), table_bfs_vs_dijkstra(N, EDGES, K),
            fig_c, legend(directed=True), table_dijkstra(N, EDGES, K, directed=True)]


if __name__ == "__main__":
    print(brute_times(N, EDGES_A, K, weighted=False), brute_times(N, EDGES, K), brute_times(N, EDGES, K, directed=True))
    print("\n\n".join(blocks()))
