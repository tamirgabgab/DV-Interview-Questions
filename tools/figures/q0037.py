#!/usr/bin/env python3
"""Figures and tables of question 0037, the edit distance between the stream a scoreboard
expected and the stream the DUT sent: the distance (missing, extra and changed packets), the
report read back from the table with a rule for ties, the band of at most d differences, and
two neighbouring packets that swapped places (the optimal string alignment of Damerau).

    python tools/figures/fill.py 37         # put the blocks on the page

The references here: table() is the full table of the distance (with swap=True also the
swap of two neighbours), report() reads it back from the corner; bfs() is independent of the
table, a search over the strings one edit apart (with swaps it is the unrestricted Damerau
distance, which the table of part d may exceed: "CA" and "ABC"). blocks() returns, in page
order: the table of part a with its path and the legend, the two reports of the tie, the
table of the tie with both paths, the band of part c and its table of costs, the table of
the swaps of part d.
"""

from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "
A, B = "ABCDEFGH", "ABDEYGHH"                         # part a: C missing, F changed to Y, H extra
TIE_A, TIE_B = "ABCDEF", "ABDXEF"                     # part b: the tie
BAND_A, BAND_B, BAND_D = "ABCDEFGHIJKL", "ABCEFGHIXJKL", 2   # part c: D missing, X extra
SWAP_A, SWAP_B = "ABCDEFGH", "ABDCEFHG"               # part d: two pairs swapped
NAMES = {"missing": "חסרה", "extra": "מיותרת", "changed": "שובשה", "swapped": "התחלפו"}


# --- the reference ---------------------------------------------------------------------------------

def table(a: str, b: str, swap: bool = False) -> list[list[int]]:
    """d[i][j]: the fewest edits from the first i packets of a to the first j of b."""
    d = [[i + j if i == 0 or j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
            if swap and i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1] and a[i - 1] != b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d


def distance(a: str, b: str, swap: bool = False) -> int:
    return table(a, b, swap)[len(a)][len(b)]


def walk(a: str, b: str, prefer: str = "gaps", swap: bool = False):
    """The path back from the corner: a list of (kind, i, j) from (0, 0), every step ending at
    cell (i, j); kind is same, missing, extra, changed or swapped. At a tie the order of the
    moves decides: "gaps" tries missing and extra before changed, "changed" the other way.
    A swap, when it is allowed and fits, is tried first."""
    d = table(a, b, swap)
    i, j, out = len(a), len(b), []
    order = ["missing", "extra", "changed"] if prefer == "gaps" else ["changed", "missing", "extra"]
    move = {"missing": (1, 0), "extra": (0, 1), "changed": (1, 1), "swapped": (2, 2)}
    while i or j:
        if i and j and a[i - 1] == b[j - 1] and d[i][j] == d[i - 1][j - 1]:
            out.append(("same", i, j))
            i, j = i - 1, j - 1
            continue
        kinds = (["swapped"] if swap else []) + order
        for kind in kinds:
            di, dj = move[kind]
            if i < di or j < dj:
                continue
            if kind == "swapped" and not (a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1] and a[i - 1] != b[j - 1]):
                continue
            if d[i][j] == d[i - di][j - dj] + 1:
                break
        else:
            raise AssertionError("no move")
        out.append((kind, i, j))
        i, j = i - di, j - dj
    return out[::-1]


def report(a: str, b: str, prefer: str = "gaps", swap: bool = False) -> list[tuple]:
    """The differences in stream order: (kind, the expected packets, the actual ones)."""
    out = []
    for kind, i, j in walk(a, b, prefer, swap):
        if kind == "missing":
            out.append((kind, a[i - 1], None))
        elif kind == "extra":
            out.append((kind, None, b[j - 1]))
        elif kind == "changed":
            out.append((kind, a[i - 1], b[j - 1]))
        elif kind == "swapped":
            out.append((kind, a[i - 2:i], b[j - 2:j]))
    return out


def apply(a: str, b: str, path) -> str:
    """b rebuilt from a along the path (the check that a report says what happened)."""
    out = []
    for kind, i, j in path:
        if kind in ("same", "changed", "extra"):
            out.append(b[j - 1])
        elif kind == "swapped":
            out.append(a[i - 1] + a[i - 2])
    return "".join(out)


def bfs(a: str, b: str, swap: bool = False) -> int:
    """The fewest single edits from a to b by a search over the strings themselves: delete a
    packet, insert one, change one, and with swap exchange two neighbours anywhere (the
    unrestricted Damerau distance). Letters from a and b are enough."""
    letters = sorted(set(a + b))
    seen, todo = {a: 0}, deque([a])
    cap = len(a) + len(b) + 1
    while todo:
        s = todo.popleft()
        if s == b:
            return seen[s]
        nxt = set()
        for k in range(len(s) + 1):
            if k < len(s):
                nxt.add(s[:k] + s[k + 1:])
                nxt.update(s[:k] + c + s[k + 1:] for c in letters)
                if swap and k + 1 < len(s):
                    nxt.add(s[:k] + s[k + 1] + s[k] + s[k + 2:])
            if len(s) < cap:
                nxt.update(s[:k] + c + s[k:] for c in letters)
        for t in nxt:
            if t not in seen:
                seen[t] = seen[s] + 1
                todo.append(t)
    raise AssertionError("unreachable")


def within(a: str, b: str, d: int) -> int | None:
    """The distance when it is at most d, else None, from the cells with |i - j| <= d only;
    also the number of cells it computed, for the table of costs."""
    m, n = len(a), len(b)
    if abs(m - n) > d:
        return None
    big = d + 1
    prev = {j: j for j in range(0, min(n, d) + 1)}
    for i in range(1, m + 1):
        cur = {}
        for j in range(max(0, i - d), min(n, i + d) + 1):
            if j == 0:
                cur[j] = i
                continue
            cur[j] = min(prev.get(j, big) + 1, cur.get(j - 1, big) + 1, prev.get(j - 1, big) + (a[i - 1] != b[j - 1]))
        if min(cur.values()) > d:
            return None
        prev = cur
    return prev[n] if prev[n] <= d else None


def band_cells(n: int, d: int) -> int:
    """The cells of an n by n table (without row and column 0) with |i - j| <= d."""
    return n * (2 * d + 1) - d * (d + 1)


# --- drawing ---------------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


CW = 26                                               # a cell
OPS = {"same": "ed-same", "missing": "ed-miss", "extra": "ed-extra", "changed": "ed-chg", "swapped": "ed-swap"}


def table_svg(a: str, b: str, label: str, prefer: str = "gaps", other: str | None = None,
              band: int | None = None, swap: bool = False) -> str:
    """The table, the expected stream down the left, the actual one along the top; the path
    of the report shaded by what each step means, and `other`, a second rule for ties, as a
    dashed line; with band, the cells outside |i - j| <= band left empty."""
    d = table(a, b, swap)
    m, n = len(a), len(b)
    x0, y0 = 2 * CW + 4, 2 * CW + 4
    W, H = x0 + (n + 1) * CW + 34, y0 + (m + 1) * CW + 4   # 30 more on the right for the enlarge button
    path = walk(a, b, prefer, swap)
    kind_at = {(i, j): k for k, i, j in path}
    kind_at[(0, 0)] = "same"
    s = f'<svg class="figure ed-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">'
    # the headers: the packets, and the index row and column (0 is the empty prefix)
    for j in range(n + 1):
        x = x0 + j * CW + CW / 2
        s += f'<text class="ed-idx" x="{x:g}" y="{CW - 8}" text-anchor="middle">{j}</text>'
        if j:
            s += f'<text class="ed-pk" x="{x:g}" y="{2 * CW - 6}" text-anchor="middle">{b[j - 1]}</text>'
    for i in range(m + 1):
        y = y0 + i * CW + CW / 2 + 4
        s += f'<text class="ed-idx" x="{CW / 2:g}" y="{y:g}" text-anchor="middle">{i}</text>'
        if i:
            s += f'<text class="ed-pk" x="{CW + CW / 2 + 2:g}" y="{y:g}" text-anchor="middle">{a[i - 1]}</text>'
    for i in range(m + 1):
        for j in range(n + 1):
            x, y = x0 + j * CW, y0 + i * CW
            out = band is not None and abs(i - j) > band
            cls = "ed-cell" + (" ed-out" if out else "") + (f" {OPS[kind_at[(i, j)]]}" if (i, j) in kind_at else "")
            s += f'<rect class="{cls}" x="{x}" y="{y}" width="{CW}" height="{CW}"/>'
            if not out:
                s += f'<text class="ed-v" x="{x + CW / 2:g}" y="{y + CW / 2 + 4:g}" text-anchor="middle">{d[i][j]}</text>'
    if other:
        pts = [(0, 0)] + [(i, j) for _, i, j in walk(a, b, other, swap)]
        s += '<polyline class="ed-other" points="' + " ".join(f"{x0 + j * CW + CW / 2:g},{y0 + i * CW + CW / 2:g}" for i, j in pts) + '"/>'
    return s + "</svg>"


def legend(other: bool = False, swap: bool = False) -> str:
    keys = ('<span><i class="ed-key-same"></i>אותה חבילה</span><span><i class="ed-key-miss"></i>חסרה, צעד למטה</span>'
            '<span><i class="ed-key-extra"></i>מיותרת, צעד ימינה</span><span><i class="ed-key-chg"></i>שובשה, צעד באלכסון</span>')
    if swap:
        keys += '<span><i class="ed-key-swap"></i>התחלפו, שני צעדים באלכסון</span>'
    if other:
        keys += '<span><i class="ed-key-other"></i>המסלול כשמעדיפים שיבוש</span>'
    return f'<span class="viz-legend">{keys}</span>'


def say(item) -> str:
    """One line of the report, the Hebrew word first."""
    kind, x, y = item
    if kind == "missing":
        return f"חסרה {x}"
    if kind == "extra":
        return f"מיותרת {y}"
    if kind == "changed":
        return f"שובשה {x} ל-{y}"
    return f"התחלפו {ltr(x)} ל-{ltr(y)}"


def table_ties() -> str:
    rows = ["| הכלל בשוויון | הדוח | המרחק |", "|---|---|:-:|"]
    for prefer, name in (("gaps", "קודם חסרה ומיותרת"), ("changed", "קודם שיבוש")):
        rep = report(TIE_A, TIE_B, prefer)
        assert len(rep) == distance(TIE_A, TIE_B)
        rows.append(f"| {name} | {', '.join(say(x) for x in rep)} | {len(rep)} |")
    return "\n".join(rows)


def table_costs() -> str:
    rows = ["| הזרמים | הסף d | תאים בטבלה המלאה | תאים ברצועה |", "|---|:-:|:-:|:-:|"]
    for m, d in ((12, 2), (1000, 3), (10**6, 10)):
        full, band = m * m, band_cells(m, d)
        if m < 2000:
            assert band == sum(1 for i in range(1, m + 1) for j in range(1, m + 1) if abs(i - j) <= d)
        rows.append(f"| שני זרמים של {m:,} חבילות | {d} | {full:,} | {band:,} |")
    return "\n".join(rows)


def table_swaps() -> str:
    rows = ["| הצפוי מול בפועל | בלי החלפה | עם החלפה של שכנות | הדוח עם החלפה |", "|---|:-:|:-:|---|"]
    for a, b in ((SWAP_A, SWAP_B), ("ABCDEF", "ABDCEF"), ("ABCD", "BCDA")):
        lev, osa = distance(a, b), distance(a, b, swap=True)
        if len(a) <= 6:
            assert lev == bfs(a, b) and osa == bfs(a, b, swap=True)
        rep = ", ".join(say(x) for x in report(a, b, swap=True))
        rows.append(f"| {RLM}`{a}` מול `{b}` | {lev} | {osa} | {rep} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    out = [
        table_svg(A, B, f"טבלת המרחקים של {A} מול {B} : הזרם הצפוי בשורות, הזרם בפועל בעמודות, ובפינה 3. "
                  "המסלול מהפינה : C חסרה, F שובשה ל-Y, ו-H מיותרת"),
        legend(),
        table_ties(),
        table_svg(TIE_A, TIE_B, f"טבלת המרחקים של {TIE_A} מול {TIE_B}, ובפינה 2. שני מסלולים באותו אורך : "
                  "C חסרה ו-X מיותרת, או C שובשה ל-D ו-D שובשה ל-X", other="changed"),
        legend(other=True),
        table_svg(BAND_A, BAND_B, f"טבלת המרחקים של {BAND_A} מול {BAND_B} עם d = 2 : רק חמשת האלכסונים "
                  "שסביב האלכסון הראשי מחושבים, ובפינה 2", band=BAND_D),
        table_costs(),
        table_swaps(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    print("a", distance(A, B), bfs(A, B), report(A, B))
    print("b", report(TIE_A, TIE_B, "gaps"), report(TIE_A, TIE_B, "changed"))
    print("c", within(BAND_A, BAND_B, 2), within(BAND_A, BAND_B, 1), distance(BAND_A, BAND_B), band_cells(12, 2))
    print("d", distance(SWAP_A, SWAP_B), distance(SWAP_A, SWAP_B, True), report(SWAP_A, SWAP_B, swap=True),
          distance("CA", "ABC", True), bfs("CA", "ABC", True))
