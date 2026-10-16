#!/usr/bin/env python3
"""Inline SVG figures and tables of question 0009 (16 boxes, 16 people and a helper).

    python tools/figures/q0009.py > /tmp/q0009.html

Prints the before / after box tables, the two cycle figures and the trace table; paste
them into the question page.
"""

import math

N, MAX_OPENS = 16, 8

# The example: box b holds the note NOTES[b] (index 0 unused). One cycle of 11, plus 3 and 2.
LONG = [1, 7, 12, 3, 15, 9, 4, 16, 10, 5, 13]
SHORT = [[2, 11, 6], [8, 14]]
NOTES = [0] * (N + 1)
for cyc in [LONG, *SHORT]:
    for i, box in enumerate(cyc):
        NOTES[box] = cyc[(i + 1) % len(cyc)]
assert sorted(NOTES[1:]) == list(range(1, N + 1))

HALF = len(LONG) // 2
SWAP = (LONG[0], LONG[HALF])                   # boxes 1 and 9
AFTER = list(NOTES)
AFTER[SWAP[0]], AFTER[SWAP[1]] = AFTER[SWAP[1]], AFTER[SWAP[0]]
NEW_EDGES = {(SWAP[0], AFTER[SWAP[0]]), (SWAP[1], AFTER[SWAP[1]])}


def cycles(notes):
    seen, out = set(), []
    for start in range(1, N + 1):
        if start in seen:
            continue
        cyc, box = [start], notes[start]
        while box != start:
            cyc.append(box)
            box = notes[box]
        seen.update(cyc)
        out.append(cyc)
    return out


def cycle_svg(layout, notes, uid, aria, edge_class, highlight=()):
    """layout: list of (cycle, cx, cy, R). Edges are arcs on each cycle's circle, clockwise."""
    r = 15
    heads = "".join(
        f'<marker id="{uid}-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse"><path class="{c}-fill" d="M0,0 L10,5 L0,10 z"/></marker>'
        for c in ("ink", "s1", "s2", "s3"))
    p = [f'<svg class="figure" viewBox="0 0 640 300" role="img" aria-label="{aria}"><defs>{heads}</defs>']
    nodes = []
    for cyc, cx, cy, R in layout:
        n = len(cyc)
        ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
        pos = {b: (cx + R * math.cos(a), cy + R * math.sin(a)) for b, a in zip(cyc, ang)}
        d = (r + 4) / R
        for i, b in enumerate(cyc):
            nxt = notes[b]
            a0, a1 = ang[i] + d, ang[i] + 2 * math.pi / n - d
            x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
            x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
            large = 1 if (a1 - a0) > math.pi else 0
            cls = edge_class(cyc, b, nxt)
            dash = ' stroke-dasharray="6 4"' if (b, nxt) in NEW_EDGES else ""
            color = cls.split("-")[0]
            p.append(f'<path class="{cls}" d="M{x0:.1f},{y0:.1f} A{R},{R} 0 {large} 1 {x1:.1f},{y1:.1f}" '
                     f'fill="none" stroke-width="2.5"{dash} marker-end="url(#{uid}-{color})">'
                     f'<title>box {b} holds note {nxt}</title></path>')
        for b in cyc:
            x, y = pos[b]
            ring = " box-hl" if b in highlight else ""
            nodes.append(f'<circle class="box-node{ring}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"><title>box {b}</title></circle>'
                         f'<text class="box-num" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{b}</text>')
        p.append(f'<text class="legend" x="{cx}" y="{cy + 4}" text-anchor="middle">L = {n}</text>')
    p.extend(nodes)
    p.append("</svg>")
    return "".join(p)


def boxes_table(notes, marks=()):
    """A compact grid: the small number is the box, the big one is the note inside it."""
    cells = "".join(f'<span{" class=\"hl\"" if b in marks else ""}><small>{b}</small><b>{notes[b]}</b></span>'
                    for b in range(1, N + 1))
    return f'<div class="box-grid" dir="ltr">{cells}</div>'


def trace_table(notes):
    rows = ["| אדם | הקופסאות שהוא פותח, לפי הסדר | פתיחות | הצליח? |", "|---|---|---|---|"]
    for me in range(1, N + 1):
        box, path = me, []
        for _ in range(MAX_OPENS):
            path.append(box)
            if notes[box] == me:
                break
            box = notes[box]
        ok = notes[box] == me
        boxes = " → ".join(str(b) for b in path)
        rows.append(f'| {me} | <span dir="ltr">{boxes}</span> | {len(path)} | {"✓" if ok else "✗"} |')
    return "\n".join(rows)


if __name__ == "__main__":
    print(boxes_table(NOTES, SWAP), "\n")
    before = [(LONG, 175, 150, 120), (SHORT[0], 430, 150, 60), (SHORT[1], 565, 150, 45)]
    print(cycle_svg(before, NOTES, "q9b", "המעגלים לפני ההחלפה: מעגל באורך 11, מעגל באורך 3 ומעגל באורך 2",
                    lambda cyc, b, n: "s2-line" if len(cyc) > MAX_OPENS else "ink-line", SWAP), "\n")
    print(boxes_table(AFTER, SWAP), "\n")
    after_cycles = cycles(AFTER)
    a, b = [c for c in after_cycles if SWAP[0] in c or SWAP[1] in c]
    after = [(a, 110, 150, 85), (b, 300, 150, 80), (SHORT[0], 465, 150, 55), (SHORT[1], 580, 150, 40)]
    print(cycle_svg(after, AFTER, "q9a", "המעגלים אחרי ההחלפה: מעגלים באורך 6, 5, 3 ו-2",
                    lambda cyc, b, n: ("s1-line" if SWAP[0] in cyc else "s3-line") if len(cyc) > 3 else "ink-line",
                    SWAP), "\n")
    print([len(c) for c in after_cycles], "\n")
    print(trace_table(NOTES), "\n")
    print(trace_table(AFTER))
