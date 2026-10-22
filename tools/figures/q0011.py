#!/usr/bin/env python3
"""Inline SVG figures of question 0011 (random final board of tic-tac-toe).

    python tools/figures/q0011.py > /tmp/q0011.html

Prints five figures separated by blank lines: numbering, examples, wrap-around examples,
the four directions of the 12 lines, and "every fifth cell completes a line".
"""

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
WRAP = LINES + [(1, 5, 6), (2, 3, 7), (0, 5, 7), (1, 3, 8)]
C = 34                                         # cell size


def mark(kind, x, y, cls="mark"):
    """An X or an O centred in the cell whose top-left corner is (x, y)."""
    m, cx, cy = 9, x + C / 2, y + C / 2
    if kind == "X":
        return (f'<path class="{cls}" d="M{x + m},{y + m} L{x + C - m},{y + C - m} '
                f'M{x + C - m},{y + m} L{x + m},{y + C - m}"/>')
    if kind == "O":
        return f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{C / 2 - m + 1}"/>'
    return ""


def board(x0, y0, cells="." * 9, fills=None, caption="", ghost=False, numbers=False, new=()):
    """A 3x3 board. fills: {cell: css class}. new: cells whose mark is highlighted."""
    fills = fills or {}
    g = [f'<g class="ttt-ghost">' if ghost else "<g>"]
    for i in range(9):
        x, y = x0 + (i % 3) * C, y0 + (i // 3) * C
        if i in fills:
            g.append(f'<rect class="{fills[i]}" x="{x}" y="{y}" width="{C}" height="{C}"/>')
        g.append(mark(cells[i], x, y, "mark mark-new" if i in new else "mark"))
        if numbers:
            g.append(f'<text class="box-num" x="{x + C / 2}" y="{y + C / 2 + 5}" text-anchor="middle">{i}</text>')
    for k in (1, 2):
        g.append(f'<line class="ttt-grid" x1="{x0 + k * C}" x2="{x0 + k * C}" y1="{y0}" y2="{y0 + 3 * C}"/>'
                 f'<line class="ttt-grid" x1="{x0}" x2="{x0 + 3 * C}" y1="{y0 + k * C}" y2="{y0 + k * C}"/>')
    if caption:
        g.append(f'<text class="legend" x="{x0 + 1.5 * C}" y="{y0 + 3 * C + 20}" text-anchor="middle" '
                 f'direction="rtl">{caption}</text>')
    g.append("</g>")
    return "".join(g)


def svg(width, height, aria, body, max_w=None):
    style = f' style="max-width:{max_w}rem"' if max_w else ""
    return f'<svg class="figure" viewBox="0 0 {width} {height}"{style} role="img" aria-label="{aria}">{body}</svg>'


def won_cells(cells, player, lines):
    return {i for line in lines if all(cells[i] == player for i in line) for i in line}


def numbering():
    return svg(3 * C + 8, 3 * C + 8, "מספור המשבצות 0 עד 8, שורה אחרי שורה",
               board(4, 4, numbers=True), max_w=8)


def examples():
    boards = [("XXXOXOOOX", "X ניצח : 2 שלישיות"), ("XXOXO.O..", "O ניצח"),
              ("XOXXOOOXX", "תיקו"), ("XXXOOO...", "✗ שניהם ניצחו"),
              ("XXXOO.O..", "✗ O שיחק אחרי הניצחון")]
    body, x = [], 6
    for cells, caption in boards:
        fills = {i: "cell-s2" for i in won_cells(cells, "X", LINES)}
        fills.update({i: "cell-s1" for i in won_cells(cells, "O", LINES)})
        body.append(board(x, 6, cells, fills, caption))
        x += 3 * C + 40
    return svg(x - 20, 3 * C + 34, "דוגמאות ללוחות סיום חוקיים ולא חוקיים", "".join(body))


def wrap_examples():
    """Each wrap-around line drawn straight across the board and a faded copy beside it."""
    body = []
    # (line, ghost on the left?, path in board coordinates: (row, col) with col possibly outside 0..2)
    panels = [((0, 5, 7), True, [(0, 0), (1, -1), (2, -2)]),
              ((2, 3, 7), False, [(0, 2), (1, 3), (2, 4)])]
    x = 6
    for line, left, path in panels:
        cells = "".join("X" if i in line else "." for i in range(9))
        real_x = x + (3 * C + 4 if left else 0)
        ghost_x = x if left else x + 3 * C + 4
        fills = {i: "cell-s2" for i in line}
        body.append(board(ghost_x, 6, cells, fills, ghost=True))
        body.append(board(real_x, 6, cells, fills, "המשבצות " + ", ".join(map(str, line))))
        pts = []
        for r, c in path:
            px = real_x + c * C + C / 2 + (4 if c > 2 else -4 if c < 0 else 0)
            pts.append(f"{px:.1f},{6 + r * C + C / 2:.1f}")
        body.append(f'<polyline class="s2-line" points="{" ".join(pts)}" fill="none" stroke-width="3"/>')
        x += 2 * (3 * C + 4) + 40
    return svg(x - 34, 3 * C + 34, "אלכסונים שממשיכים מהצד השני של הלוח", "".join(body))


def directions():
    groups = [("שורות", lambda r, c: r), ("טורים", lambda r, c: c),
              ("אלכסונים ↘", lambda r, c: (c - r) % 3), ("אלכסונים ↙", lambda r, c: (r + c) % 3)]
    body, x = [], 6
    for caption, key in groups:
        fills = {i: f"cell-s{key(i // 3, i % 3) + 1}" for i in range(9)}
        body.append(board(x, 6, fills=fills, caption=caption, numbers=True))
        x += 3 * C + 36
    return svg(x - 30, 3 * C + 34, "ארבעת הכיוונים : כל כיוון מחלק את הלוח לשלושה קווים מקבילים",
               "".join(body))


def fifth():
    base = {0, 1, 3, 4}
    assert not any(set(line) <= base for line in WRAP)            # 4 cells, no line
    body, x = [], 6
    for extra in sorted(set(range(9)) - base):
        cells = "".join("X" if i in base | {extra} else "." for i in range(9))
        done = [line for line in WRAP if set(line) <= base | {extra}]
        assert done                                               # the fifth cell completes a line
        fills = {i: "cell-s2" for line in done for i in line}
        body.append(board(x, 6, cells, fills, f"משבצת {extra}", new=(extra,)))
        x += 3 * C + 22
    return svg(x - 16, 3 * C + 34, "ריבוע של 4 משבצות בלי קו, וכל משבצת חמישית משלימה קו", "".join(body))


if __name__ == "__main__":
    for fig in (numbering, examples, wrap_examples, directions, fifth):
        print(fig(), "\n")
