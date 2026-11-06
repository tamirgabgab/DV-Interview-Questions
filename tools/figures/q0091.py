#!/usr/bin/env python3
"""Figures and tables of question 0091 (Chomp: the poisoned chocolate bar).

    python tools/figures/fill.py 91        # put the blocks on the page

A bar of m rows and n columns, the poisoned square at the bottom left. Squares are named
like a chessboard: the columns a, b, c, ... from the left, the rows 1, 2, 3, ... from the
bottom, so the poison is a1. Eating a square eats it and every square above it and to its
right. A position is a staircase: the heights of the columns, column a first, never rising
to the right. A square of chocolate is a warm tile, the poison a magenta tile with a cross,
the squares a move eats are dashed, and the square chosen is framed in blue.

blocks() returns them in page order: the statement's move c3 on 4 x 4 (with the legend);
part a's game on 4 x 4 in two rows of boards (b2, then the mirror); part b's table of the
square boards 2 to 8 (staircases, the winning first moves, the mirror against every
answer); part c's strategy-stealing boards on 3 x 5, the 2 x 6 game, and the table of the
winning first moves for 1 to 7 rows and 1 to 8 columns. tests/0091 checks that the page
copies match and recomputes every value.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

COLS = "abcdefgh"

# --- the reference -------------------------------------------------------------------------


def eat(h: tuple, c: int, r: int) -> tuple:
    """The staircase after eating column c, row r (0-based): every column from c on keeps
    at most r squares."""
    return tuple(min(x, r) if i >= c else x for i, x in enumerate(h))


def moves(h: tuple):
    """Every move but the poison (column 0, row 0), with the staircase after it."""
    for c, height in enumerate(h):
        for r in range(height):
            if (c, r) != (0, 0):
                yield (c, r), eat(h, c, r)


@lru_cache(maxsize=None)
def wins(h: tuple) -> bool:
    """The player to move wins from h. With the poison alone there is no move but the
    poison, and the player to move loses."""
    return any(not wins(t) for _, t in moves(h))


def winning_moves(h: tuple) -> list:
    return [mv for mv, t in moves(h) if not wins(t)]


def first_moves(m: int, n: int) -> list:
    return winning_moves((m,) * n)


def name(c: int, r: int) -> str:
    return f"{COLS[c]}{r + 1}"


def staircases(m: int, n: int) -> int:
    """The staircases that fit in m x n, the empty one included."""
    return comb(m + n, n)


def reachable(m: int, n: int) -> int:
    seen, todo = set(), [(m,) * n]
    while todo:
        h = todo.pop()
        if h not in seen:
            seen.add(h)
            todo.extend(t for _, t in moves(h))
    return len(seen)


def mirror_move(h: tuple):
    """The mirror strategy on a square board: b2 first, then keep the two arms of the L
    equal. None when the arms are already equal (the player to move loses)."""
    if len(h) > 1 and h[1] > 1:
        return 1, 1
    up, right = h[0] - 1, sum(1 for x in h if x > 0) - 1
    if up > right:
        return 0, right + 1
    if right > up:
        return up + 1, 0
    return None


def mirror_always_wins(n: int) -> bool:
    """The mirror strategy, first on n x n, against every possible answer."""
    def ours(h):
        mv = mirror_move(h)
        return mv is not None and theirs(eat(h, *mv))

    def theirs(h):
        return all(ours(t) for _, t in moves(h))
    return ours((n,) * n)


def two_rows_move(bottom: int, top: int):
    """2 x n: keep the bottom row exactly one longer than the top row. None when it
    already is (the player to move loses)."""
    if top == bottom - 1:
        return None
    if top >= bottom:
        return bottom - 1, 1          # eat the top row back to bottom - 1 squares
    return top + 1, 0                 # eat the bottom row back to top + 1 squares


# --- drawing --------------------------------------------------------------------------------

S = 24          # the side of a square
LM, BM = 14, 16  # the margins of the row numbers (left) and the column letters (below)
TOPM = 20        # room above the boards for the enlarge button of the figure


def board(m: int, n: int, h: tuple, x0: float, y0: float, s: int = S, prev: tuple | None = None,
          pick=None, caption: str = "", labels: bool = True) -> str:
    """One bar: the squares left (h), the squares the last move ate (prev minus h) dashed,
    the square chosen framed, the letters and numbers, a caption under it."""
    out = []
    bx = x0 + (LM if labels else 0)
    for c in range(n):
        for r in range(m):
            x, y = bx + c * s, y0 + (m - 1 - r) * s
            if r < h[c]:
                cls = "cp-poison" if (c, r) == (0, 0) else "cp-sq"
                out.append(f'<rect class="{cls}" x="{x + 1}" y="{y + 1}" width="{s - 2}" height="{s - 2}" rx="3"/>')
                if (c, r) == (0, 0):
                    d = s * 0.28
                    cx, cy = x + s / 2, y + s / 2
                    out.append(f'<path class="cp-cross" d="M{cx - d:g},{cy - d:g} L{cx + d:g},{cy + d:g} M{cx - d:g},{cy + d:g} L{cx + d:g},{cy - d:g}"/>')
            elif prev is not None and r < prev[c]:
                out.append(f'<rect class="cp-gone" x="{x + 2}" y="{y + 2}" width="{s - 4}" height="{s - 4}" rx="3"/>')
            else:
                out.append(f'<rect class="cp-empty" x="{x + 1}" y="{y + 1}" width="{s - 2}" height="{s - 2}" rx="3"/>')
    if pick is not None:
        c, r = pick
        x, y = bx + c * s, y0 + (m - 1 - r) * s
        out.append(f'<rect class="cp-pick" x="{x + 1}" y="{y + 1}" width="{s - 2}" height="{s - 2}" rx="3"/>')
    if labels:
        for c in range(n):
            out.append(f'<text class="cp-lab" x="{bx + c * s + s / 2:g}" y="{y0 + m * s + 13}" text-anchor="middle">{COLS[c]}</text>')
        for r in range(m):
            out.append(f'<text class="cp-lab" x="{x0 + 5}" y="{y0 + (m - 1 - r) * s + s / 2 + 4:g}" text-anchor="middle">{r + 1}</text>')
    if caption:
        out.append(f'<text class="cp-cap" x="{bx + n * s / 2:g}" y="{y0 + m * s + BM + 16}" text-anchor="middle" direction="rtl">{caption}</text>')
    return "".join(out)


def row_of_boards(m: int, n: int, items: list[dict], label: str, gap: int = 22, s: int = S) -> str:
    """Boards side by side, the first on the right, as the page reads."""
    bw = LM + n * s
    w = len(items) * bw + (len(items) - 1) * gap + 4
    h = TOPM + m * s + BM + (24 if any(i.get("caption") for i in items) else 2) + 4
    out = [f'<svg class="figure cp-fig" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.1f}rem" role="img" aria-label="{label}">']
    for j, it in enumerate(items):
        out.append(board(m, n, it["h"], 2 + (len(items) - 1 - j) * (bw + gap), TOPM + 2, s, it.get("prev"), it.get("pick"),
                         it.get("caption", "")))
    return "".join(out) + "</svg>"


def legend(*keys: tuple[str, str]) -> str:
    return '<span class="viz-legend">' + "".join(f'<span><i class="{k}"></i>{t}</span>' for k, t in keys) + "</span>"


KEY_SQ = ("cp-key-sq", "שוקולד")
KEY_POISON = ("cp-key-poison", "המשבצת המורעלת, a1")
KEY_PICK = ("cp-key-pick", "המשבצת שנבחרה")
KEY_GONE = ("cp-key-gone", "מה שהמהלך אכל")


def game(m: int, n: int, plays: list[tuple[str, tuple]], start=None) -> list[dict]:
    """The boards of a game: the start, then one board after each move (who, square)."""
    h = start or (m,) * n
    items = [{"h": h, "caption": "ההתחלה"}]
    for who, sq in plays:
        t = eat(h, *sq)
        items.append({"h": t, "prev": h, "pick": sq, "caption": f"{who} : {name(*sq)}"})
        h = t
    return items


# --- the statement ---------------------------------------------------------------------------

def statement() -> str:
    h0 = (4,) * 4
    items = [{"h": h0, "caption": "לפני"}, {"h": eat(h0, 2, 2), "prev": h0, "pick": (2, 2), "caption": "אחרי c3"}]
    svg = row_of_boards(4, 4, items, gap=40, label=(
        "טבלת שוקולד של 4 על 4. העמודות a עד d משמאל לימין, השורות 1 עד 4 מלמטה למעלה, והמשבצת המורעלת "
        "a1 בפינה השמאלית התחתונה. מימין הטבלה לפני המהלך, משמאל אחריו : מי שבוחר את c3 אוכל אותה ואת כל "
        "מה שמעליה ומימינה, c3, d3, c4 ו-d4, ונשארות 12 משבצות"))
    return svg + "\n\n" + legend(KEY_SQ, KEY_POISON, KEY_PICK, KEY_GONE)


# --- part a: 4 x 4 ----------------------------------------------------------------------------

GAME_A = [("אתם", (1, 1)), ("היריב", (3, 0)), ("אתם", (0, 3)), ("היריב", (1, 0)), ("אתם", (0, 1))]


def game_a() -> tuple[str, str]:
    items = game(4, 4, GAME_A)
    one = row_of_boards(4, 4, items[:3], label=(
        "משחק על 4 על 4, חלק ראשון. ההתחלה; אתם אוכלים את b2, ונשארת צורת L : הזרוע העליונה a2, a3, a4 "
        "והזרוע הימנית b1, c1, d1, שלוש משבצות בכל אחת; היריב אוכל את d1, ונשארות שתיים בזרוע הימנית"))
    two = row_of_boards(4, 4, items[3:], label=(
        "משחק על 4 על 4, חלק שני. אתם עונים ב-a4, ושוב שתי הזרועות שוות, שתיים בכל אחת; היריב אוכל את b1, "
        "והזרוע הימנית נעלמת; אתם אוכלים את a2, והזרוע העליונה נעלמת. נשארה רק a1 המורעלת, והיריב חייב לאכול אותה"))
    return one, two


# --- part b: the square boards ---------------------------------------------------------------

def table_b() -> str:
    rows = ["| הלוח | מצבים עם המשבצת המורעלת | המהלכים הראשונים המנצחים | המראה מנצחת כל תשובה |",
            "|:-:|:-:|:-:|:-:|"]
    for n in range(2, 9):
        fm = ", ".join(name(*mv) for mv in first_moves(n, n))
        rows.append(f"| ‏{n} × {n} | ‏{staircases(n, n) - 1:,} | ‏{fm} | כן |")
    return "\n".join(rows)


# --- part c: strategy stealing, 2 x n, the table -----------------------------------------------

def stealing() -> str:
    h0 = (3,) * 5
    corner = eat(h0, 4, 2)
    x = (2, 1)
    items = [{"h": corner, "prev": h0, "pick": (4, 2), "caption": "הראשון : e3"},
             {"h": eat(corner, *x), "prev": corner, "pick": x, "caption": "התשובה X"},
             {"h": eat(h0, *x), "prev": h0, "pick": x, "caption": "רק X"}]
    return row_of_boards(3, 5, items, gap=24, s=22, label=(
        "גניבת אסטרטגיה על 3 על 5. בלוח הימני הראשון אוכל רק את הפינה הימנית העליונה, e3. באמצעי השני עונה "
        "במהלך X, כאן c2, שאוכל את c2, d2, e2, c3 ו-d3. בשמאלי הראשון אוכל את X כבר במהלך הראשון, ומקבל "
        "בדיוק אותו מצב, כי X אוכל גם את e3"))


GAME_2 = [("אתם", (5, 1)), ("היריב", (3, 0)), ("אתם", (2, 1)), ("היריב", (0, 1)), ("אתם", (1, 0))]


def game_2() -> tuple[str, str]:
    items = game(2, 6, GAME_2)[1:]
    one = row_of_boards(2, 6, items[:3], s=20, label=(
        "משחק על 2 על 6. אתם אוכלים את f2, והשורה העליונה קצרה באחת מהתחתונה, 5 מול 6; היריב אוכל את d1 "
        "ואת כל מה שמימינה ומעליה, ונשארות 3 בכל שורה; אתם אוכלים את c2, ושוב 2 מול 3"))
    two = row_of_boards(2, 6, items[3:], s=20, label=(
        "המשך המשחק על 2 על 6. היריב אוכל את a2, וכל השורה העליונה נעלמת; אתם אוכלים את b1, ונשארת רק a1 "
        "המורעלת, והיריב חייב לאכול אותה"))
    return one, two


def table_c() -> str:
    head = "| שורות \\ עמודות | " + " | ".join(f"‏{n}" for n in range(1, 9)) + " |"
    rows = [head, "|:-:|" + ":-:|" * 8]
    for m in range(1, 8):
        cells = []
        for n in range(1, 9):
            fm = first_moves(m, n)
            cells.append("אין" if not fm else "‏" + ", ".join(name(*mv) for mv in fm))
        rows.append(f"| ‏{m} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    a1, a2 = game_a()
    g1, g2 = game_2()
    return [
        statement(),
        a1,
        a2 + "\n\n" + legend(KEY_PICK, KEY_GONE, KEY_POISON),
        table_b(),
        stealing(),
        g1,
        g2,
        table_c(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
