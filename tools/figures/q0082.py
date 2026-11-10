#!/usr/bin/env python3
"""Figures and tables of question 0082 (Nim: normal play, misère, and the subtraction game
{1, 3, 4} with Grundy numbers).

    python tools/figures/fill.py 82        # put the blocks on the page

blocks() returns them in page order: for part a the heaps 3, 4, 5 in binary with their XOR
row (the column of the XOR's highest bit marked, and the one heap that has it), the same
table after the winning move, their legend, the block diagram of the combinational
nim_move_hw, and a table of positions with every winning move; for part b the endgame (1, 1, 4) under the two rules; for part c the Grundy numbers of
{1, 3, 4} from 0 to 13 with the period of 7 tinted, its legend, and a table of positions in
the subtraction game with every winning move (the XOR of the Grundy numbers against the
XOR of the sizes).
tests/0082 checks that the page copies match and solves every position by brute force.
"""

from __future__ import annotations

import sys
from functools import reduce
from html import escape
from operator import xor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cells import legend, table  # noqa: E402

MOVES = (1, 3, 4)
BITS = 3


# --- the theory ----------------------------------------------------------------------------


def nim_xor(heaps) -> int:
    return reduce(xor, heaps, 0)


def nim_moves(heaps):
    """Every winning move of normal Nim: (heap index, new size); empty when lost."""
    x = nim_xor(heaps)
    return [(i, h ^ x) for i, h in enumerate(heaps) if x and h ^ x < h]


def misere_lost(heaps) -> bool:
    """The player to move loses misère Nim (at least one token on the table)."""
    x = nim_xor(heaps)
    if max(heaps) > 1:
        return x == 0
    return sum(heaps) % 2 == 1


def grundy(n: int, moves=MOVES) -> list[int]:
    g = [0] * (n + 1)
    for k in range(1, n + 1):
        seen = {g[k - m] for m in moves if m <= k}
        g[k] = min(set(range(len(seen) + 1)) - seen)
    return g


def sub_moves(heaps, moves=MOVES):
    """Every winning move of the sum of subtraction games: (heap index, new size)."""
    g = grundy(max(heaps), moves)
    x = reduce(xor, (g[h] for h in heaps), 0)
    if x == 0:
        return []
    return [(i, h - m) for i, h in enumerate(heaps) for m in moves if m <= h and g[h - m] == g[h] ^ x]


# --- helpers -------------------------------------------------------------------------------


def bits(v: int, n: int = BITS) -> str:
    return format(v, f"0{n}b")


def heaps_txt(h) -> str:
    return f'<span dir="ltr">({", ".join(map(str, h))})</span>'


def arrow(a, b) -> str:
    """One move "a → b", never split at the end of a line (non-breaking spaces)."""
    return f"{a}\u00a0→\u00a0{b}"


def move_txt(heaps, mv) -> str:
    i, new = mv
    return f"מהערימה של {heaps[i]} לוקחים {heaps[i] - new}"


# --- part a --------------------------------------------------------------------------------

START = (3, 4, 5)


def xor_table(heaps, aria: str) -> str:
    """The heaps in binary, a row each, and the XOR row; the column of the XOR's highest bit
    framed, and the bit of the heaps that have it tinted."""
    x = nim_xor(heaps)
    top = x.bit_length() - 1 if x else None
    rows = []
    for h in heaps:
        cells = []
        for b in range(BITS - 1, -1, -1):
            v = (h >> b) & 1
            cls = "c2 is-hl" if b == top and v else ("is-hl" if b == top else ("c1" if v else ""))
            cells.append((str(v), cls) if cls else str(v))
        rows.append((f"ערימה {h}", cells, f"= {h}"))
    xc = []
    for b in range(BITS - 1, -1, -1):
        v = (x >> b) & 1
        cls = "c3" if not x else ("c1" if v else "") + (" is-hl" if b == top else "")
        xc.append((str(v), cls.strip()) if cls.strip() else str(v))
    rows.append(("‏XOR", xc, f"= {x}"))
    return table(rows, aria, head=[str(1 << b) for b in range(BITS - 1, -1, -1)])


def table_before() -> str:
    return xor_table(START, "סעיף א : הערימות 3, 4 ו-5 בבינארי ושורת ה-XOR שלהן, 010 = 2. "
                            "הביט הגבוה של ה-XOR הוא ביט ה-2, ורק לערימה 3 יש אותו")


def table_after() -> str:
    after = list(START)
    i, new = nim_moves(START)[0]
    after[i] = new
    return xor_table(after, "סעיף א : אחרי המהלך, הערימות 1, 4 ו-5, וה-XOR שלהן 000 = 0")


def legend_a() -> str:
    return legend([("pm-key-c1", "ביט 1 בערימה"), ("pm-key-hl", "העמודה של הביט הגבוה של ה-XOR"),
                   ("pm-key-c2", "הערימה שיש לה את הביט הזה : ממנה לוקחים"), ("pm-key-c3", "‏XOR = 0 : מי שתורו מפסיד")])


EXAMPLES = [(3, 4, 5), (1, 2, 3), (1, 1, 2), (2, 5, 6), (7, 9, 12), (5, 6, 7, 8)]


def table_examples() -> str:
    lines = ["| הערימות | ‏XOR | מי שתורו | המהלכים המנצחים |", "|:-:|:-:|:-:|:-:|"]
    for h in EXAMPLES:
        x = nim_xor(h)
        mv = nim_moves(h)
        verdict = "מפסיד" if not x else "מנצח"
        moves = "; ".join(arrow(h[i], new) for i, new in mv)
        moves = f'<span dir="ltr">{moves}</span>' if mv else "אין"
        lines.append(f'| {heaps_txt(h)} | <span dir="ltr">{x} = {bits(x, 4)}</span> | {verdict} | {moves} |')
    return "\n".join(lines)


# --- part a in hardware: the block diagram of nim_move_hw ----------------------------------

NB = "\u00a0"
DP_W, DP_H = 400, 440
# (x, y, w, h, kind, title, sub): one column of blocks, the data flowing down
DP_BLOCKS = (
    (50, 40, 270, 46, "tree", "XOR tree", "x = heap[0] ^ ... ^ heap[n-1]"),
    (50, 116, 270, 46, "logic", "leading one", "top = the highest 1 of x"),
    (50, 192, 270, 46, "logic", "candidates", "cand[i] = |(heap[i] & top)"),
    (50, 268, 270, 46, "logic", "priority encoder", "idx = the first 1 of cand"),
    (50, 344, 270, 46, "out", "mux + XOR", "new_size = heap[idx] ^ x"),
)
# (points, arrow head, label, label x, label y, anchor)
DP_WIRES = (
    (((185, 4), (185, 40)), True, "heap[0..n-1]", 179, 16, "end"),
    (((185, 22), (350, 22), (350, 215), (320, 215)), True, "", 0, 0, ""),
    (((350, 215), (350, 367), (320, 367)), True, "heap", 355, 335, "start"),
    (((185, 86), (185, 116)), True, "x", 191, 106, "start"),
    (((185, 100), (22, 100), (22, 367), (50, 367)), True, "x", 28, 300, "start"),
    (((185, 162), (185, 192)), True, "top", 191, 182, "start"),
    (((185, 238), (185, 268)), True, "cand", 191, 258, "start"),
    (((185, 314), (185, 344)), True, "idx", 191, 334, "start"),
    (((320, 291), (396, 291)), True, "valid", 394, 284, "end"),
    (((185, 390), (185, 420)), True, "new_size", 191, 414, "start"),
)
DP_DOTS = ((185, 22), (350, 215), (185, 100))


def dp_wire(pts, arrow=True):
    d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
    return f'<path class="nm-wire" d="{d}"' + (' marker-end="url(#nm-hb)"' if arrow else "") + "/>"


def diagram_svg() -> str:
    """Part a in hardware: nim_move as a combinational block. The XOR tree gives x, the
    leading-one detector its top bit as a one-hot top, an AND per heap the candidates, a
    priority encoder the first of them, and a mux with an XOR the new size."""
    label = ("תרשים המלבנים של nim_move_hw, מעגל צירופי בלי שעון" + NB + ": עץ XOR מחשב את x מכל הערימות. "
             "גלאי האחד המוביל מוציא את top, עם ביט דלוק אחד במקום הביט הגבוה של x. "
             "לכל ערימה, AND עם top ואחריו OR של הביטים אומר אם היא מועמדת, ו-valid הוא OR של המועמדות. "
             "מקודד עדיפות בוחר את המועמדת הראשונה, idx, ומרבב בוחר את heap[idx], וה-XOR שלו עם x הוא new_size")
    o = [f'<svg class="figure nm-fig nm-dp" viewBox="0 0 {DP_W} {DP_H}" direction="ltr" style="max-width:{DP_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="nm-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="nm-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for x, y, w, h, cls, title, sub in DP_BLOCKS:
        o.append(f'<g class="nm-blk nm-{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{y + h / 2 - 3:g}" text-anchor="middle">{escape(title)}</text>'
                 f'<text class="nm-sub" x="{x + w / 2:g}" y="{y + h / 2 + 13:g}" text-anchor="middle">{escape(sub)}</text></g>')
    for pts, arrow, lab, lx, ly, anchor in DP_WIRES:
        o.append(dp_wire(pts, arrow))
        if lab:
            o.append(f'<text class="nm-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    o += [f'<circle class="nm-dot" cx="{x}" cy="{y}" r="3"/>' for x, y in DP_DOTS]
    return "".join(o) + "</svg>"


# --- part b --------------------------------------------------------------------------------

END = (1, 1, 4)


def table_misere() -> str:
    lines = ["| המהלך מ-<span dir=\"ltr\">(1, 1, 4)</span> | המצב שנשאר | ‏XOR | כשהאחרון מנצח | כשהאחרון מפסיד |", "|:-:|:-:|:-:|:-:|:-:|"]
    for new, name in [(0, 'הורדה ל-0, כמו ב-Nim רגיל : <span dir="ltr">4 → 0</span>'),
                      (1, 'הורדה ל-1 : <span dir="ltr">4 → 1</span>')]:
        h = (1, 1, new)
        x = nim_xor(h)
        normal = "היריב מפסיד" if x == 0 else "היריב מנצח"
        mis = "היריב מפסיד" if misere_lost(h) else "היריב מנצח"
        lines.append(f'| {name} | {heaps_txt(h)} | ‏{x} | {normal} | {mis} |')
    return "\n".join(lines)


# --- part c --------------------------------------------------------------------------------

GN = 14


def table_grundy() -> str:
    g = grundy(GN - 1)
    row_n = [str(n) for n in range(GN)]
    row_g = [(str(g[n]), ("c1" if n < 7 else "c4") + (" is-hl" if n in (7, 8, 9, 10) else "")) for n in range(GN)]
    return table([("‏g(n)", row_g, None)],
                 "סעיף ג : מספרי גרנדי של המשחק שבו לוקחים 1, 3 או 4, מ-n = 0 עד 13 : "
                 "0, 1, 0, 1, 2, 3, 2 ושוב 0, 1, 0, 1, 2, 3, 2. ארבעת הערכים ב-7 עד 10 שווים לאלה ב-0 עד 3, "
                 "ולכן הסדרה מחזורית במחזור 7",
                 head=row_n)


def legend_grundy() -> str:
    return legend([("pm-key-c1", "המחזור הראשון, n = 0 עד 6"), ("pm-key-c4", "המחזור השני, n = 7 עד 13"),
                   ("pm-key-hl", "ארבעה ערכים שחוזרים : מכאן הסדרה חוזרת")])


SUB_EXAMPLES = [(3, 4, 5), (5, 6, 7), (10, 11, 6), (2, 9, 16)]


def table_sub() -> str:
    lines = ["| הערימות | מספרי גרנדי | ‏XOR של גרנדי | מי שתורו | המהלכים המנצחים | ‏XOR של הגדלים |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for h in SUB_EXAMPLES:
        g = grundy(max(h))
        gs = [g[v] for v in h]
        x = reduce(xor, gs, 0)
        mv = sub_moves(h)
        win = "מנצח" if x else "מפסיד"
        moves = "אין" if not mv else '<span dir="ltr">' + "; ".join(arrow(h[i], new) for i, new in mv) + "</span>"
        lines.append(f'| {heaps_txt(h)} | <span dir="ltr">{", ".join(map(str, gs))}</span> | ‏{x} | {win} | {moves} | ‏{nim_xor(h)} |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [table_before(), table_after(), legend_a(), diagram_svg(), table_examples(), table_misere(),
            table_grundy(), legend_grundy(), table_sub()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
