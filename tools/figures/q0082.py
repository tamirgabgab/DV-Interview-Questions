#!/usr/bin/env python3
"""Figures and tables of question 0082 (Nim: normal play, misère, and the subtraction game
{1, 3, 4} with Grundy numbers).

    python tools/figures/fill.py 82        # put the blocks on the page

blocks() returns them in page order: for part a the heaps 3, 4, 5 in binary with their XOR
row (the column of the XOR's highest bit marked, and the one heap that has it), the same
table after the winning move, their legend, and a table of positions with every winning
move; for part b the endgame (1, 1, 4) under the two rules; for part c the Grundy numbers of
{1, 3, 4} from 0 to 13 with the period of 7 tinted, its legend, and a table of positions in
the subtraction game (the XOR of the Grundy numbers against the XOR of the sizes).
tests/0082 checks that the page copies match and solves every position by brute force.
"""

from __future__ import annotations

import sys
from functools import reduce
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
        moves = "אין" if not mv else "; ".join(f"{h[i]} → {new}" for i, new in mv)
        lines.append(f'| {heaps_txt(h)} | <span dir="ltr">{x} = {bits(x, 4)}</span> | {verdict} | '
                     f'{"אין" if not mv else f"<span dir=\"ltr\">{moves}</span>"} |')
    return "\n".join(lines)


# --- part b --------------------------------------------------------------------------------

END = (1, 1, 4)


def table_misere() -> str:
    lines = ["| המהלך מ-‏(1, 1, 4) | המצב שנשאר | ‏XOR | כשהאחרון מנצח | כשהאחרון מפסיד |", "|:-:|:-:|:-:|:-:|:-:|"]
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
    lines = ["| הערימות | מספרי גרנדי | ‏XOR של גרנדי | מי שתורו | מהלך מנצח | ‏XOR של הגדלים |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for h in SUB_EXAMPLES:
        g = grundy(max(h))
        gs = [g[v] for v in h]
        x = reduce(xor, gs, 0)
        mv = sub_moves(h)
        win = "מנצח" if x else "מפסיד"
        first = "אין" if not mv else f'<span dir="ltr">{h[mv[0][0]]} → {mv[0][1]}</span>'
        lines.append(f'| {heaps_txt(h)} | <span dir="ltr">{", ".join(map(str, gs))}</span> | ‏{x} | {win} | {first} | ‏{nim_xor(h)} |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [table_before(), table_after(), legend_a(), table_examples(), table_misere(),
            table_grundy(), legend_grundy(), table_sub()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
