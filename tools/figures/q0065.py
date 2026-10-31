#!/usr/bin/env python3
"""Figures and tables of question 0065 (the number of islands in a grid of land and water
with four neighbours, with eight, and the size of every island).

    python tools/figures/fill.py 65        # put the blocks on the page

The references here are independent of the page code: components() finds the islands by
union-find (the brute force of the tests), trace() replays the flood fill frame by frame
(the rows of the table and the frames of the islands explorer), water_pieces() counts the
pieces of water for the digital topology paradox, and queue_stats() measures the queue and
the stack on an all-land grid. blocks() returns, in page order: the example grid coloured
by its islands with four neighbours and its legend, the table of the flood cell by cell,
the same grid with eight neighbours, the diagonal line of land and its table, and the
table of the island sizes.
"""

from collections import deque

RLM = "‏"
GRID = ["110000", "110011", "000010", "000100", "000100"]
SC_GRID = ["101", "010", "101"]                  # the X of the self-checks of parts a and b
SC_GRID_C = ["1101", "1001", "0111"]             # the self-check of part c
DIAG_GRID = ["0001", "0010", "0100", "1000"]     # the diagonal line of land of part b
DIRS4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS8 = DIRS4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
DIR_NAMES = ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]
DIR_HEB = ["למעלה", "למטה", "שמאלה", "ימינה", "למעלה-שמאלה", "למעלה-ימינה", "למטה-שמאלה", "למטה-ימינה"]


def dirs_of(diag):
    return DIRS8 if diag else DIRS4


# --- references ---------------------------------------------------------------------------

def components(grid, diag=False, land="1"):
    """The islands by union-find, the brute force of the tests: a list of sets of cells, in
    the order of their smallest cell (row-major)."""
    m, n = len(grid), len(grid[0]) if grid else 0
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r in range(m):
        for c in range(n):
            if grid[r][c] == land:
                parent[(r, c)] = (r, c)
    for (r, c) in list(parent):
        for dr, dc in dirs_of(diag):
            a, b = r + dr, c + dc
            if (a, b) in parent:
                ra, rb = find((r, c)), find((a, b))
                if ra != rb:
                    parent[max(ra, rb)] = min(ra, rb)
    groups = {}
    for cell in parent:
        groups.setdefault(find(cell), set()).add(cell)
    return [groups[k] for k in sorted(groups)]


def sizes_brute(grid, diag=False):
    return sorted((len(s) for s in components(grid, diag)), reverse=True)


def water_pieces(grid, diag=False):
    """How many pieces the water forms, with the same neighbourhood."""
    return len(components(grid, diag, land="0"))


def trace(grid, diag=False):
    """The flood fill frame by frame, as the page's code runs it: a "start" frame when the
    scan meets a land cell not seen yet (a new island, the cell pushed), a "pop" frame for
    every cell that leaves the queue (its neighbours checked in the order of the directions,
    the land cells not seen yet pushed and marked), and an "end" frame when the scan is
    over. Every frame carries the queue after it, the island labels of the cells (0 for
    water or not reached yet), the count and the sizes so far (the running island last)."""
    m, n = len(grid), len(grid[0]) if grid else 0
    dirs = dirs_of(diag)
    labels = [[0] * n for _ in range(m)]
    frames, sizes, skipped, count = [], [], 0, 0

    def snap(kind, **more):
        f = {"kind": kind, "count": count, "sizes": list(sizes), "labels": [row[:] for row in labels]}
        f.update(more)
        frames.append(f)

    for r in range(m):
        for c in range(n):
            if grid[r][c] != "1" or labels[r][c]:
                skipped += 1
                continue
            count += 1
            labels[r][c] = count
            sizes.append(0)
            q = deque([(r, c)])
            snap("start", cell=[r, c], isle=count, skipped=skipped, q=[[r, c]], pushed=[[r, c]], nb=[])
            skipped = 0
            while q:
                i, j = q.popleft()
                sizes[-1] += 1
                nb, pushed = [], []
                for k, (di, dj) in enumerate(dirs):
                    a, b = i + di, j + dj
                    if not (0 <= a < m and 0 <= b < n):
                        why = "out"
                    elif grid[a][b] != "1":
                        why = "water"
                    elif labels[a][b]:
                        why = "seen"
                    else:
                        why = "push"
                        labels[a][b] = count
                        q.append((a, b))
                        pushed.append([a, b])
                    nb.append([a, b, why, k])
                snap("pop", cell=[i, j], isle=count, q=[list(x) for x in q], pushed=pushed, nb=nb, skipped=0)
    snap("end", cell=None, isle=count, skipped=skipped, q=[], pushed=[], nb=[])
    return frames


def flood_sizes(grid, diag=False):
    """The sizes in the order the islands are found, from the trace."""
    return trace(grid, diag)[-1]["sizes"]


def queue_stats(m, n, diag=False):
    """On an all-land m x n grid: the longest the BFS queue gets (marking at the push), the
    deepest an explicit DFS stack gets (marking at the push), the depth of a recursive DFS
    (marking at the entry, the path it follows), and the pushes a BFS that marks at the
    pop makes (cells pushed more than once)."""
    grid = ["1" * n] * m
    dirs = dirs_of(diag)
    inside = lambda a, b: 0 <= a < m and 0 <= b < n

    def run(lifo):
        seen = [[False] * n for _ in range(m)]
        seen[0][0] = True
        q, longest = deque([(0, 0)]), 1
        while q:
            i, j = q.pop() if lifo else q.popleft()
            for di, dj in dirs:
                a, b = i + di, j + dj
                if inside(a, b) and not seen[a][b]:
                    seen[a][b] = True
                    q.append((a, b))
            longest = max(longest, len(q))
        return longest

    def rec_depth():
        seen = [[False] * n for _ in range(m)]
        stack, deepest = [((0, 0), 0)], 1          # a recursion simulated: (cell, next direction)
        seen[0][0] = True
        while stack:
            (i, j), k = stack[-1]
            if k == len(dirs):
                stack.pop()
                continue
            stack[-1] = ((i, j), k + 1)
            a, b = i + dirs[k][0], j + dirs[k][1]
            if inside(a, b) and not seen[a][b]:
                seen[a][b] = True
                stack.append(((a, b), 0))
                deepest = max(deepest, len(stack))
        return deepest

    def pushes_mark_at_pop():
        seen = [[False] * n for _ in range(m)]
        q, pushes, longest = deque([(0, 0)]), 1, 1
        while q:
            i, j = q.popleft()
            if seen[i][j]:
                continue
            seen[i][j] = True
            for di, dj in dirs:
                a, b = i + di, j + dj
                if inside(a, b) and not seen[a][b]:
                    q.append((a, b))
                    pushes += 1
            longest = max(longest, len(q))
        return pushes, longest

    pushes, longest = pushes_mark_at_pop()
    return {"queue": run(False), "stack": run(True), "recursion": rec_depth(), "pushes_late": pushes, "queue_late": longest}


# --- follow-ups -----------------------------------------------------------------------------

def perimeter(grid, diag=False):
    """The perimeter of every island, largest island first: 4 per cell minus 2 per pair of
    cells that share an edge (an edge is shared with an up / down / left / right neighbour
    only, whatever the connectivity)."""
    out = []
    for comp in components(grid, diag):
        shared = sum(1 for (r, c) in comp for (dr, dc) in DIRS4 if (r + dr, c + dc) in comp) // 2
        out.append((len(comp), 4 * len(comp) - 2 * shared))
    return sorted(out, reverse=True)


def distinct_shapes(grid, diag=False):
    """The number of islands of different shapes (LC 694): a shape is the set of cells moved
    so that its smallest cell is (0, 0)."""
    shapes = set()
    for comp in components(grid, diag):
        r0, c0 = min(comp)
        shapes.add(frozenset((r - r0, c - c0) for r, c in comp))
    return len(shapes)


def count_online(m, n, adds, diag=False):
    """LC 305: the number of islands after every cell added, by union-find with a count."""
    parent, count, out = {}, 0, []
    dirs = dirs_of(diag)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (r, c) in adds:
        if (r, c) in parent:
            out.append(count)
            continue
        parent[(r, c)] = (r, c)
        count += 1
        for dr, dc in dirs:
            nb = (r + dr, c + dc)
            if nb in parent:
                ra, rb = find((r, c)), find(nb)
                if ra != rb:
                    parent[ra] = rb
                    count -= 1
        out.append(count)
    return out


# --- blocks ---------------------------------------------------------------------------------

def cell_name(r, c):
    return f"({r}, {c})"


def grid_svg(grid, diag, label, show="isle"):
    """The grid with every land cell coloured by its island (the colour cycles over the five
    series, the island's number, or its size with show="size", written in the cell); with
    eight neighbours the diagonal links between cells of one island are drawn."""
    m, n = len(grid), len(grid[0])
    comps = components(grid, diag)
    cell_of = {cell: k + 1 for k, comp in enumerate(comps) for cell in comp}
    size_of = {k + 1: len(comp) for k, comp in enumerate(comps)}
    cs, lw, top = 36, 26, 22
    W, H = lw + n * cs + 6, top + m * cs + 6
    s = (f'<svg class="figure il-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">')
    for c in range(n):
        s += f'<text class="tick" x="{lw + c * cs + cs / 2:g}" y="14" text-anchor="middle">{c}</text>'
    for r in range(m):
        s += f'<text class="tick" x="{lw - 8}" y="{top + r * cs + cs / 2 + 4:g}" text-anchor="end">{r}</text>'
    for r in range(m):
        for c in range(n):
            x, y = lw + c * cs, top + r * cs
            if grid[r][c] == "1":
                k = cell_of[(r, c)]
                txt = k if show == "isle" else size_of[k]
                s += (f'<g class="il-cell is-land il-i{(k - 1) % 5 + 1}"><title>cell {cell_name(r, c)}: land, island {k} of {size_of[k]} cells</title>'
                      f'<rect x="{x + 2}" y="{y + 2}" width="{cs - 4}" height="{cs - 4}" rx="4"/>'
                      f'<text x="{x + cs / 2:g}" y="{y + cs / 2 + 5:g}" text-anchor="middle">{txt}</text></g>')
            else:
                s += (f'<g class="il-cell is-water"><title>cell {cell_name(r, c)}: water</title>'
                      f'<rect x="{x + 2}" y="{y + 2}" width="{cs - 4}" height="{cs - 4}" rx="4"/></g>')
    if diag:                                   # the corner links that only eight neighbours give
        for r in range(m):
            for c in range(n):
                if grid[r][c] != "1":
                    continue
                for dr, dc in ((1, -1), (1, 1)):
                    a, b = r + dr, c + dc
                    if 0 <= a < m and 0 <= b < n and grid[a][b] == "1":
                        s += (f'<line class="il-link" x1="{lw + c * cs + cs / 2:g}" y1="{top + r * cs + cs / 2:g}" '
                              f'x2="{lw + b * cs + cs / 2:g}" y2="{top + a * cs + cs / 2:g}"><title>a corner link: {cell_name(r, c)} and {cell_name(a, b)}</title></line>')
    return s + "</svg>"


def legend(show="isle", diag=False):
    keys = "".join(f'<span><i class="il-key il-i{k}"></i>אי {k}</span>' for k in range(1, 4)) if show == "isle" else \
        '<span><i class="il-key il-i1"></i>יבשה, צבע לכל אי, הגודל כתוב בתא</span>'
    link = '<span><i class="il-key-link"></i>חיבור דרך פינה (שמונה כיוונים בלבד)</span>' if diag else ""
    return f'<span class="viz-legend">{keys}<span><i class="il-key is-water"></i>מים</span>{link}</span>'


def qtext(q):
    if not q:
        return "ריק"
    return '<span dir="ltr">' + " ".join(f"({r},{c})" for r, c in q) + "</span>"


def table_flood(grid, diag=False):
    """A row per frame of the flood on the example: what the scan met, the cell that left
    the queue, its neighbours, the queue after, the count and the size so far."""
    out = ["| הצעד | מה קרה | התא | השכנים שנבדקו | התור אחרי הצעד | איים | הגודל |",
           "|:-:|:--|:-:|:--|:--|:-:|:-:|"]
    for t, f in enumerate(trace(grid, diag)):
        if f["kind"] == "start":
            what = (f"הסריקה עברה {f['skipped']} תאים של מים או תאים שכבר סומנו, ופגשה" if f["skipped"] else "הסריקה פגשה") + \
                f" יבשה שלא סומנה : **אי חדש {f['isle']}**, התא מסומן ונכנס לתור"
            nb = "—"
        elif f["kind"] == "pop":
            what = "התא יוצא מהתור, הגודל גדל ב-1"
            parts = []
            for a, b, why, k in f["nb"]:
                word = {"out": "מחוץ ללוח", "water": "מים", "seen": "כבר סומן", "push": "**מסומן ונכנס לתור**"}[why]
                where = "" if why == "out" else f' <span dir="ltr">{cell_name(a, b)}</span>'
                parts.append(f"{DIR_HEB[k]}{where} {word}")
            nb = "; ".join(parts)
        else:
            what = f"הסריקה עברה את {f['skipped']} התאים האחרונים (מים או מסומנים) ונגמרה"
            nb = "—"
        cell = f"{RLM}{qtext([f['cell']])}" if f["cell"] else "—"
        size = f"{RLM}{f['sizes'][-1]}" if f["sizes"] and f["kind"] != "end" else "—"
        out.append(f"| {RLM}{t + 1} | {what} | {cell} | {nb} | {RLM}{qtext(f['q'])} | {RLM}{f['count']} | {size} |")
    return "\n".join(out)


def table_paradox(grid):
    """The diagonal line of land: the islands and the pieces of water with four and with
    eight neighbours."""
    rows = ["| השכנות | איים של יבשה | חלקים של מים | מה זה אומר |", "|:--|:-:|:-:|:--|"]
    for diag, name, meaning in ((False, "ארבעה כיוונים", "ארבעה תאים בודדים, והמים משני צידי האלכסון מופרדים"),
                                (True, "שמונה כיוונים", "אי אחד, אבל גם המים חוצים את האלכסון דרך אותן פינות : הקו לא מפריד")):
        rows.append(f"| {name} | {RLM}{len(components(grid, diag))} | {RLM}{water_pieces(grid, diag)} | {meaning} |")
    return "\n".join(rows)


def table_sizes(grid):
    """The islands of the example with their cells and sizes, with four and with eight
    neighbours, and the sorted lists."""
    out = ["| השכנות | האי | התאים | הגודל | הרשימה הממוינת |", "|:--|:-:|:--|:-:|:--|"]
    for diag, name in ((False, "ארבעה כיוונים"), (True, "שמונה כיוונים")):
        comps = components(grid, diag)
        found = flood_sizes(grid, diag)
        sizes = sorted(found, reverse=True)
        for k, comp in enumerate(comps):
            cells = qtext(sorted(comp))
            lst = f"{RLM}<span dir=\"ltr\">[{', '.join(map(str, sizes))}]</span>" if k == 0 else f"{RLM}—"
            out.append(f"| {name if k == 0 else RLM + '—'} | {RLM}{k + 1} | {RLM}{cells} | {RLM}{len(comp)} | {lst} |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [
        grid_svg(GRID, False, "הלוח 5 על 6 של הדוגמה : שלושה איים עם ארבעה כיוונים, כל אי בצבע שלו והמספר שלו בתא"),
        legend(),
        table_flood(GRID, False),
        grid_svg(GRID, True, "אותו לוח עם שמונה כיוונים : שני איים, הפינה בין (2, 4) ל-(3, 3) מחברת"),
        legend(diag=True),
        grid_svg(DIAG_GRID, True, "קו אלכסוני של יבשה על לוח 4 על 4 : עם שמונה כיוונים הוא אי אחד, והמים משני הצדדים גם הם מחוברים דרך אותן פינות"),
        table_paradox(DIAG_GRID),
        grid_svg(GRID, False, "הלוח של הדוגמה, הגודל של האי כתוב בכל תא שלו", show="size"),
        legend(show="size"),
        table_sizes(GRID),
    ]


if __name__ == "__main__":
    print(sizes_brute(GRID), sizes_brute(GRID, True), flood_sizes(GRID), flood_sizes(GRID, True))
    print(sizes_brute(SC_GRID), sizes_brute(SC_GRID, True), sizes_brute(SC_GRID_C))
    print(queue_stats(20, 20), queue_stats(8, 10))
    print(perimeter(GRID), distinct_shapes(GRID))
    print("\n\n".join(blocks()))
