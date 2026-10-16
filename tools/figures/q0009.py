#!/usr/bin/env python3
"""Inline SVG figures and tables of question 0009 (16 boxes, 16 people and a helper).

    python tools/figures/q0009.py > /tmp/q0009.html

Prints the before / after box tables, the two cycle figures and the trace table; paste
them into the question page.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

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


def walk(notes, me):
    """The boxes person `me` opens, in order (at most MAX_OPENS)."""
    box, path = me, []
    for _ in range(MAX_OPENS):
        path.append(box)
        if notes[box] == me:
            break
        box = notes[box]
    return path


def boxes_frame(notes, marked=(), path=(), found=None, faded=False):
    """16 boxes in two rows (small number = box, big number = note). `path` boxes are numbered
    in opening order and joined by lines; `found` is drawn green; `marked` orange."""
    cell, gap, x0, y0 = 50, 10, 14, 22
    centre = {}
    p = ['<svg class="figure" viewBox="0 0 500 180" style="max-width:31rem" role="img" aria-label="16 הקופסאות והפתקים שבהן">']
    for b in range(1, N + 1):
        r, c = divmod(b - 1, 8)
        x, y = x0 + c * (cell + gap), y0 + r * 80
        centre[b] = (x + cell / 2, y + 22)
        if b == found:
            cls = "st-ok"
        elif b in path:
            cls = "st-stack"
        elif b in marked:
            cls = "st-cur"
        else:
            cls = "st-cell"
        extra = " st-faded" if faded and b not in path and b != found and b not in marked else ""
        p.append(f'<g class="{extra.strip()}"><rect class="{cls}" x="{x}" y="{y}" width="{cell}" height="44" rx="6"/>'
                 f'<text class="st-small" x="{x + 6}" y="{y + 12}">{b}</text>'
                 f'<text class="st-text" x="{x + cell / 2}" y="{y + 33}" text-anchor="middle">{notes[b]}</text></g>')
    for i in range(len(path) - 1):
        (xa, ya), (xb, yb) = centre[path[i]], centre[path[i + 1]]
        p.append(f'<line class="st-path" x1="{xa:.0f}" y1="{ya:.0f}" x2="{xb:.0f}" y2="{yb:.0f}" stroke-dasharray="5 4"/>')
    for i, b in enumerate(path):
        x, y = centre[b]
        p.append(f'<circle class="st-order-bg" cx="{x + 18:.0f}" cy="{y - 18:.0f}" r="8"/>'
                 f'<text class="st-order" x="{x + 18:.0f}" y="{y - 14.5:.0f}" text-anchor="middle">{i + 1}</text>')
    p.append("</svg>")
    return "".join(p)


def walk_stepper():
    """Frame 0: the helper's swap. Frames 1..16: each person's walk after the swap."""
    frames = [(boxes_frame(NOTES, marked=SWAP),
               f"לפני ההחלפה. אדם 0 מצא מעגל באורך 11 ומחליף בין הפתקים של קופסה {SWAP[0]} "
               f"(פתק {NOTES[SWAP[0]]}) וקופסה {SWAP[1]} (פתק {NOTES[SWAP[1]]})."),
              (boxes_frame(AFTER, marked=SWAP),
               f"אחרי ההחלפה: בקופסה {SWAP[0]} עכשיו הפתק {AFTER[SWAP[0]]}, ובקופסה {SWAP[1]} הפתק "
               f"{AFTER[SWAP[1]]}. מכאן כל אחד הולך לפי הפתקים, מתחיל בקופסה עם המספר שלו.")]
    for me in range(1, N + 1):
        path = walk(AFTER, me)
        chain = " ← ".join(str(b) for b in path)
        frames.append((boxes_frame(AFTER, path=path, found=path[-1], faded=True),
                       f"אדם {me} פותח <span dir=\"ltr\">{chain.replace(' ← ', ' → ')}</span>: הפתק {me} נמצא "
                       f"בקופסה {path[-1]} אחרי {len(path)} פתיחות מתוך {MAX_OPENS} מותרות ✓"))
    return stepper(frames, "ההחלפה של העוזר ואז המסלול של כל אחד מ-16 האנשים")


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
    print(trace_table(AFTER), "\n")
    print(walk_stepper())
