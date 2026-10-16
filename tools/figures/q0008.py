#!/usr/bin/env python3
"""Inline SVG figures of question 0008 (Eurovision 2026: when could Israel no longer win?).

    python tools/figures/q0008.py > /tmp/q0008.html

Prints the step table and three figures; paste them into the question page.
"""

# Grand final results: (country, jury, public)
RESULTS = [
    ("Bulgaria", 204, 312), ("Israel", 123, 220), ("Romania", 64, 232),
    ("Australia", 165, 122), ("Italy", 134, 147), ("Finland", 141, 138),
    ("Denmark", 165, 78), ("Moldova", 43, 183), ("Ukraine", 54, 167),
    ("Greece", 73, 147), ("France", 144, 14), ("Poland", 133, 17),
    ("Albania", 60, 85), ("Norway", 115, 19), ("Croatia", 53, 71),
    ("Czechia", 104, 9), ("Serbia", 38, 52), ("Malta", 81, 8),
    ("Cyprus", 41, 34), ("Sweden", 35, 16), ("Belgium", 36, 0),
    ("Lithuania", 10, 12), ("Germany", 12, 0), ("Austria", 1, 5),
    ("United Kingdom", 1, 0),
]
PUBLIC_TOTAL = 36 * 58
assert sum(r[1] for r in RESULTS) == 35 * 58
assert sum(r[2] for r in RESULTS) == PUBLIC_TOTAL

ORDER = sorted(RESULTS, key=lambda r: r[1])          # lowest jury score is announced first
ISRAEL = next(i for i, r in enumerate(ORDER) if r[0] == "Israel")
ISRAEL_TOTAL = ORDER[ISRAEL][1] + ORDER[ISRAEL][2]
ABOVE = ORDER[ISRAEL + 1:]
LEFT_AFTER_ISRAEL = PUBLIC_TOTAL - sum(r[2] for r in ORDER[:ISRAEL + 1])


def steps():
    """(label, points left, room, lost) right after Israel and after each country above it."""
    left, room = LEFT_AFTER_ISRAEL, sum(ISRAEL_TOTAL - j for _, j, _ in ABOVE)
    out, passed = [("Israel", left, room, left > room)], False
    for country, jury, public in ABOVE:
        left -= public
        room -= ISRAEL_TOTAL - jury
        passed = passed or jury + public > ISRAEL_TOTAL
        out.append((country, left, room, passed or left > room))
    return out


def cups(announced: int, aria: str) -> str:
    """Bars of the countries above Israel after `announced` of them got their public points."""
    w, h, x0, top, base = 640, 330, 48, 16, 230
    ymax = 400
    y = lambda v: base - (base - top) * min(v, ymax) / ymax
    slot = (w - x0 - 10) / len(ABOVE)
    bw = slot * 0.56
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">']
    for v in range(0, ymax + 1, 100):
        p.append(f'<line class="grid" x1="{x0}" x2="{w - 10}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                 f'<text class="tick" x="{x0 - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    room_total = 0
    for i, (country, jury, public) in enumerate(ABOVE):
        x = x0 + i * slot + (slot - bw) / 2
        cx = x + bw / 2
        p.append(f'<rect class="bar by-multiples" x="{x:.1f}" y="{y(jury):.1f}" width="{bw:.1f}" '
                 f'height="{base - y(jury):.1f}"><title>{country}: jury {jury}</title></rect>')
        if i < announced:
            total = jury + public
            p.append(f'<rect class="bar by-bfs" x="{x:.1f}" y="{y(total):.1f}" width="{bw:.1f}" '
                     f'height="{y(jury) - y(total):.1f}"><title>{country}: public {public}, '
                     f'total {total}</title></rect>'
                     f'<text class="tick" x="{cx:.1f}" y="{y(total) - 6:.1f}" text-anchor="middle">{total}</text>')
        else:
            room = ISRAEL_TOTAL - jury
            room_total += room
            p.append(f'<rect class="cup-room" x="{x:.1f}" y="{y(ISRAEL_TOTAL):.1f}" width="{bw:.1f}" '
                     f'height="{y(jury) - y(ISRAEL_TOTAL):.1f}"><title>{country}: room {room}</title></rect>'
                     f'<text class="tick" x="{cx:.1f}" y="{(y(jury) + y(ISRAEL_TOTAL)) / 2 + 4:.1f}" '
                     f'text-anchor="middle">{room}</text>')
        p.append(f'<text class="tick" x="{cx:.1f}" y="{base + 16}" text-anchor="middle">{country}</text>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - 10}" y1="{base}" y2="{base}"/>'
             f'<line class="israel-line" x1="{x0}" x2="{w - 10}" y1="{y(ISRAEL_TOTAL):.1f}" '
             f'y2="{y(ISRAEL_TOTAL):.1f}"/><text class="legend" x="{x0 + 4}" '
             f'y="{y(ISRAEL_TOTAL) - 6:.1f}">Israel {ISRAEL_TOTAL}</text>')

    # Bottom: total room against the points still to be given, on one scale
    left = LEFT_AFTER_ISRAEL - sum(r[2] for r in ABOVE[:announced])
    scale = (w - x0 - 120) / 1400
    left_label = f"{left} = {room_total} + {left - room_total}" if left > room_total else f"{left}"
    for row, (value, cls, name, label) in enumerate([(room_total, "cup-room", "room", f"{room_total}"),
                                                     (left, "left-bar", "left", left_label)]):
        by = 262 + row * 30
        p.append(f'<rect class="{cls}" x="{x0}" y="{by}" width="{value * scale:.1f}" height="20">'
                 f'<title>{name}: {value}</title></rect>'
                 f'<text class="legend" x="{x0 + value * scale + 8:.1f}" y="{by + 15}">{label}</text>')
    if left > room_total:
        x1, x2 = x0 + room_total * scale, x0 + left * scale
        p.append(f'<rect class="overflow" x="{x1:.1f}" y="292" width="{x2 - x1:.1f}" height="20">'
                 f'<title>overflow: {left - room_total}</title></rect>'
                 f'<line class="israel-line" x1="{x1:.1f}" x2="{x1:.1f}" y1="256" y2="318"/>')
    p.append("</svg>")
    return "".join(p)


def crossing_chart() -> str:
    """Room and points left after each announcement; Israel is out once left > room."""
    data = steps()
    w, h, x0, top, base = 640, 290, 56, 16, 250
    ymax = 1400
    y = lambda v: base - (base - top) * v / ymax
    dx = (w - x0 - 80) / (len(data) - 1)
    x = lambda i: x0 + 20 + i * dx
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" role="img" '
         f'aria-label="המקום הפנוי מול הנקודות שנותרו אחרי כל הכרזה">']
    for v in range(0, ymax + 1, 200):
        p.append(f'<line class="grid" x1="{x0}" x2="{w - 10}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                 f'<text class="tick" x="{x0 - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    first_out = next(i for i, d in enumerate(data) if d[3])
    p.append(f'<rect class="lost-zone" x="{x(first_out) - dx / 2:.1f}" y="{top}" '
             f'width="{w - 10 - x(first_out) + dx / 2:.1f}" height="{base - top}"/>')
    _, left, room, _ = data[first_out]
    p.append(f'<text class="legend" x="{x(first_out) + 8:.1f}" y="{top + 18}">{data[first_out][0]}: '
             f'{left} &gt; {room}</text>')
    for i, (label, *_) in enumerate(data):
        p.append(f'<text class="tick" x="{x(i):.1f}" y="{base + 18}" text-anchor="middle">{label}</text>')
    for key, line, dot in [(2, "s2-line", "s2-dot"), (1, "ink-line", "ink-dot")]:
        pts = " L".join(f"{x(i):.1f},{y(d[key]):.1f}" for i, d in enumerate(data))
        p.append(f'<path class="{line}" d="M{pts}" fill="none" stroke-width="2"/>')
        name = "room" if key == 2 else "points left"
        for i, d in enumerate(data):
            p.append(f'<circle class="{dot}" cx="{x(i):.1f}" cy="{y(d[key]):.1f}" r="4">'
                     f'<title>after {d[0]}: {name} {d[key]}</title></circle>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - 10}" y1="{base}" y2="{base}"/></svg>')
    return "".join(p)


def step_table() -> str:
    rows = ["| אחרי ההכרזה של | ניקוד הקהל | סך הכול | נקודות שנותרו | מקום פנוי עד 343 | ישראל עדיין יכולה לנצח? |",
            "|---|---|---|---|---|---|"]
    publics = {c: (j, pub) for c, j, pub in ABOVE}
    for label, left, room, lost in steps():
        jury, public = publics.get(label, (ORDER[ISRAEL][1], ORDER[ISRAEL][2]))
        verdict = "**לא**" if lost else "כן"
        rows.append(f"| {label} | {public} | {jury + public} | {left} | {room} | {verdict} |")
    return "\n".join(rows)


if __name__ == "__main__":
    print(step_table(), "\n")
    print(cups(0, "המקום הפנוי של כל מדינה עד 343 נקודות, מיד אחרי ההכרזה של ישראל"), "\n")
    print(cups(4, "המקום הפנוי של כל מדינה עד 343 נקודות, אחרי ההכרזה של צרפת"), "\n")
    print(crossing_chart())
