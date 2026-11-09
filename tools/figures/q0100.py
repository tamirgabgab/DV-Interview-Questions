#!/usr/bin/env python3
"""Figures and tables of question 0100, the number of ways to climb n stairs when every jump
is a number of stairs from a set S: the order matters (a sum over the jumps), broken stairs
(a zero in the table), the order does not matter (the loops swapped), and exactly t jumps (a
table over the jumps).

    python tools/figures/fill.py 100        # put the blocks on the page

The references here are independent of the page code: ways() lists every climb as the set
of stairs it lands on (each subset of 1..n-1 with n added, kept when every gap is in S and
no stair is broken), multisets() lists the counts of every jump size, and the closed forms
come from math.comb. blocks() returns, in page order: the staircase of S = {1, 2}, n = 10
with the count on every stair and the two stairs that make the last one, the table of
several sets S, the staircase with stair 5 broken, the table of the climbs of n = 10 by the
number of 2's (orders and multisets), the table of the swapped loops for S = {1, 2, 3}, and
the table of the ways in exactly t jumps.

The cycle table of the module stairs_ways (part b) comes from module_trace(), a clock-by-clock
model of the page's RTL: the combinational sum of the window, then the edge that shifts it.
tests/0100/tb.sv checks the same numbers on the module itself.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "
N, S = 10, (1, 2)                                     # the example of part a
BROKEN = (5,)                                         # the broken stair of part b


# --- the reference ---------------------------------------------------------------------------------

def table(n: int, steps, broken=()) -> list[int]:
    """ways[i]: the climbs to stair i (the order matters), stair 0 the ground."""
    bad = set(broken)
    w = [1] + [0] * n
    for i in range(1, n + 1):
        if i not in bad:
            w[i] = sum(w[i - s] for s in steps if s <= i)
    return w


def climbs(n: int, steps, broken=()) -> list[tuple[int, ...]]:
    """Every climb as its list of jumps, from the sets of stairs it lands on."""
    bad, out = set(broken), []
    if n in bad:
        return out
    if n == 0:
        return [()]                                   # the empty climb: stay on the ground
    for k in range(n):
        for mid in itertools.combinations(range(1, n), k):
            stops = (0,) + mid + (n,)
            jumps = tuple(b - a for a, b in zip(stops, stops[1:]))
            if all(j in steps for j in jumps) and not bad & set(mid):
                out.append(jumps)
    return sorted(out)


def ways(n: int, steps, broken=()) -> int:
    return len(climbs(n, steps, broken))


def multisets(n: int, steps) -> list[dict[int, int]]:
    """Every way when the order does not matter: how many jumps of each size."""
    steps = sorted(set(steps))
    out = []
    for counts in itertools.product(*[range(n // s + 1) for s in steps]):
        if sum(c * s for c, s in zip(counts, steps)) == n:
            out.append(dict(zip(steps, counts)))
    return out


def unordered_rows(n: int, steps) -> list[list[int]]:
    """The table of the swapped loops after each jump size."""
    w = [1] + [0] * n
    rows = []
    for s in steps:
        for i in range(s, n + 1):
            w[i] += w[i - s]
        rows.append(w.copy())
    return rows


def exact(n: int, steps, t: int) -> int:
    """The climbs of n in exactly t jumps."""
    return sum(1 for c in climbs(n, steps) if len(c) == t)


def exact_table(n: int, steps, tmax: int) -> list[list[int]]:
    row, rows = [1] + [0] * n, []
    rows.append(row)
    for _ in range(tmax):
        row = [sum(row[i - s] for s in steps if s <= i) for i in range(n + 1)]
        rows.append(row)
    return rows


def module_trace(n: int, steps, broken=(), k: int = 6) -> list[dict]:
    """stairs_ways clock by clock: cycle 0 start, cycles 1..n the stairs (valid, no idle clock),
    cycle n + 1 idle. Each row is the inputs of its cycle, the combinational sum and the
    registers inside the cycle; the edge at its end writes the next row's registers."""
    below, ways_reg, rows = [0] * (k + 1), 0, []                # after reset
    bad = set(broken)
    for c in range(n + 2):
        start, valid = c == 0, 1 <= c <= n
        brk = valid and c in bad
        total = sum(below[s] for s in steps)
        rows.append({"cycle": c, "start": int(start), "valid": int(valid), "stair": c if valid else None,
                     "broken": int(brk), "b1": below[1], "b2": below[2], "sum": total, "ways": ways_reg})
        if start:
            below = [0] * (k + 1)
            below[1] = ways_reg = 1
        elif valid:
            below = [0, 0 if brk else total] + below[1:k]
            ways_reg = 0 if brk else total
    return rows


# --- drawing ---------------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def sset(steps) -> str:
    return "{" + ", ".join(map(str, steps)) + "}"


def staircase_svg(n, steps, broken, label, focus=None) -> str:
    """The stairs 0 (the ground) to n rising to the right, the count on every stair, a broken
    stair crossed, and arrows into the focus stair from the stairs that make it."""
    w = table(n, steps, broken)
    cw, rise, base, top = 30, 9, 26, 40
    W = (n + 1) * cw + 12 + (30 if focus is not None else 0)   # room on the right for the enlarge button
    H = top + n * rise + base + 18
    floor = H - 18
    s = f'<svg class="figure sw-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">'
    for i in range(n + 1):
        x, h = 6 + i * cw, base + i * rise
        y = floor - h
        cls = "sw-stair" + (" sw-broken" if i in broken else "") + (" sw-focus" if i == focus else "") + \
            (" sw-from" if focus is not None and i not in broken and 0 < focus - i in steps else "")
        tip = f"stair {i}: " + ("broken" if i in broken else f"{w[i]} way{'' if w[i] == 1 else 's'}")
        s += f'<g class="{cls}"><title>{tip}</title><rect x="{x}" y="{y}" width="{cw - 2}" height="{h}" rx="2"/></g>'
        s += f'<text class="tick" x="{x + (cw - 2) / 2:g}" y="{floor + 13}" text-anchor="middle">{i}</text>'
        if i in broken:
            s += (f'<path class="sw-x" d="M{x + 7},{y + 5} l{cw - 16},{cw - 16} M{x + cw - 9},{y + 5} l{-(cw - 16)},{cw - 16}"/>')
        else:
            s += f'<text class="sw-val" x="{x + (cw - 2) / 2:g}" y="{y + 15}" text-anchor="middle">{w[i]}</text>'
    if focus is not None:
        fx = 6 + focus * cw + (cw - 2) / 2
        fy = floor - (base + focus * rise) - 4
        for d in steps:
            j = focus - d
            if j < 0 or j in broken:
                continue
            jx = 6 + j * cw + (cw - 2) / 2
            jy = floor - (base + j * rise) - 4
            my = min(jy, fy) - 14 - 8 * d
            s += f'<path class="sw-arc" d="M{jx:g},{jy:g} Q{(jx + fx) / 2:g},{my:g} {fx:g},{fy:g}" marker-end="url(#sw-head)"/>'
        s += ('<defs><marker id="sw-head" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">'
              '<path class="sw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>')
    return s + "</svg>"


def legend(focus=False, broken=False) -> str:
    keys = '<span><i class="sw-key"></i>מדרגה, ומעליה מספר הדרכים להגיע אליה</span>'
    if focus:
        keys += '<span><i class="sw-key-focus"></i>המדרגה האחרונה</span><span><i class="sw-key-from"></i>המדרגות שקופצים מהן אליה</span>'
    if broken:
        keys += '<span><i class="sw-key-broken"></i>מדרגה שבורה</span>'
    return f'<span class="viz-legend">{keys}</span>'


def table_sets() -> str:
    rows = ["| הקפיצות S | הנוסחה | הדרכים למדרגות 0 עד 10 | למדרגה 10 |", "|---|---|---|:-:|"]
    for steps in ((1, 2), (1, 2, 3), (1, 3, 5), (2, 3), (1, 2, 3, 4, 5, 6)):
        w = table(10, steps)
        assert w[10] == ways(10, steps)
        rec = " + ".join(f"w(i−{s})" for s in steps)
        rows.append(f"| {RLM}{ltr(sset(steps))} | {RLM}{ltr(f'w(i) = {rec}')} | {RLM}{ltr(', '.join(map(str, w)))} | {w[10]} |")
    return "\n".join(rows)


def table_by_twos() -> str:
    rows = ["| קפיצות של 2 | קפיצות של 1 | קפיצות בסך הכול, t | סדרים שונים | בלי סדר |", "|:-:|:-:|:-:|:-:|:-:|"]
    total = 0
    for k in range(N // 2 + 1):
        t = N - k
        orders = math.comb(t, k)
        assert orders == exact(N, S, t)
        total += orders
        rows.append(f"| {k} | {N - 2 * k} | {t} | {RLM}{ltr(f'C({t}, {k}) = {orders}')} | 1 |")
    rows.append(f"| **סך הכול** | | | **{total}** | **{N // 2 + 1}** |")
    return "\n".join(rows)


def table_loops() -> str:
    steps, n = (1, 2, 3), 6
    rows = ["| אחרי הלולאה של | הטבלה, מדרגות 0 עד 6 | מה נספר |", "|---|---|---|"]
    says = {1: "רק קפיצות של 1 : דרך אחת לכל מדרגה", 2: "קפיצות של 1 ושל 2, כל ה-2 אחרי כל ה-1",
            3: "גם קפיצות של 3, אחרי כל השאר"}
    for s, w in zip(steps, unordered_rows(n, steps)):
        rows.append(f"| {s} | {RLM}{ltr(', '.join(map(str, w)))} | {says[s]} |")
    rows.append(f"| בסדר הרגיל | {RLM}{ltr(', '.join(map(str, table(n, steps))))} | כל הסדרים |")
    return "\n".join(rows)


def table_cycles() -> str:
    """The module stairs_ways on the broken-5 run: a row a clock."""
    rows = ["| מחזור | ‏start | ‏valid | המדרגה | ‏broken | ‏below[1] | ‏below[2] | ‏sum | ‏ways |",
            "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    w = table(N, S, BROKEN)
    for r in module_trace(N, S, BROKEN):
        c = r["cycle"]
        if 1 <= c <= N + 1:                                     # the window and ways lag by a clock
            assert r["b1"] == w[c - 1] == r["ways"] and r["b2"] == (w[c - 2] if c >= 2 else 0)
        bold = lambda v, on: f"**{v}**" if on else str(v)       # noqa: E731
        cells = [bold(c, c in BROKEN or c == N + 1), str(r["start"]), str(r["valid"]),
                 "–" if r["stair"] is None else str(r["stair"]), bold(r["broken"], r["broken"]),
                 bold(r["b1"], c - 1 in BROKEN), str(r["b2"]), str(r["sum"]),
                 bold(r["ways"], c - 1 in BROKEN or c == N + 1)]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def table_exact() -> str:
    """The ways in exactly t jumps, a row per t and a column per stair, n = 10; the last row
    sums every column, which is part a's table."""
    n, t_ask = N, 7
    rows = ["| הקפיצות t | " + " | ".join(str(i) for i in range(n + 1)) + " |", "|:-:|" + ":-:|" * (n + 1)]
    table_ = exact_table(n, S, n)
    for t, row in enumerate(table_):
        cells = [("**%d**" % v if (t, i) == (t_ask, n) else str(v)) if v else "·" for i, v in enumerate(row)]
        rows.append(f"| {t} | " + " | ".join(cells) + " |")
    sums = [sum(r[i] for r in table_) for i in range(n + 1)]
    assert sums == table(n, S)
    rows.append("| **סך הכול** | " + " | ".join(f"**{v}**" if i == n else str(v) for i, v in enumerate(sums)) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    out = [
        staircase_svg(N, S, (), "גרם מדרגות 0 עד 10 עם קפיצות של 1 ושל 2 : על כל מדרגה מספר הדרכים להגיע אליה, 1, 1, 2, 3, 5 ועד 89 במדרגה 10. חיצים מהמדרגות 9 ו-8 אל מדרגה 10", focus=N),
        legend(focus=True),
        table_sets(),
        staircase_svg(N, S, BROKEN, "אותו גרם מדרגות כשמדרגה 5 שבורה : עליה 0, מדרגה 6 מקבלת רק ממדרגה 4, ובמדרגה 10 יש 25 דרכים", focus=6),
        legend(focus=True, broken=True),
        table_cycles(),
        table_by_twos(),
        table_loops(),
        table_exact(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    print("a", table(N, S), ways(10, (1, 3, 5)), ways(10, (1, 2, 3)))
    print("b", table(N, S, BROKEN), ways(N, S, (5, 6)), ways(N, (1, 3), (5, 6)))
    print("c", len(multisets(N, S)), len(multisets(10, (1, 2, 3))), unordered_rows(6, (1, 2, 3)))
    print("d", [exact(N, S, t) for t in range(5, 11)], exact_table(6, S, 6))
