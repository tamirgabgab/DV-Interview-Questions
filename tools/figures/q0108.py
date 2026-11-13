#!/usr/bin/env python3
"""Figures and tables of question 0108, the fewest flips of k consecutive bits that make every
bit 1 (a row of bits, then a grid of bits with k x k squares).

    python tools/figures/fill.py 108        # put the blocks on the page

The references here are independent of the page code:

- brute(a, k) tries every set of window starts (2^(n-k+1) of them) and returns the sets that
  make every bit 1; brute2(g, k, kc) does the same for a grid with kr x kc rectangles.
- scan(a, k) is the forced scan written with a list of the covering windows of every bit (no
  queue, no parity trick): it returns the starts, or None when a bit is left 0; events(a, k)
  is the same scan as the rows of the page's trace table and of the box.
- scan2(g, k, kc) is the forced scan of a grid, cell by cell in row-major order, counting the
  rectangles over every cell one by one.
- ring_brute(a, k) and ring_solve(a, k) are the circular follow-up: every window start on a
  ring, by brute force and by the cycles of p -> p + k.

blocks() returns, in page order: the windows that cover a bit (the forcing figure) and its
legend, the table of the example's scan and its legend, the trace of the queue of open windows,
the grid example (before and after) and its legend, and the corners of one square in the
difference array and its legend.
"""

from __future__ import annotations

import math
from itertools import product

RLM = "‏"
NB = " "

# the arrays and grids of the page and of the boxes
EXAMPLE = [0, 0, 0, 1, 0, 1, 1, 0]                        # k = 3: windows at 0, 4, 5
EXAMPLE_K = 3
ONE_ZERO = ([0, 1, 0], 1)                                  # 2
STUCK = ([1, 1, 0], 2)                                     # -1
LONG = ([int(c) for c in "00011110000101101000"], 4)       # the box: 7 windows
LONG_BAD = ([int(c) for c in "00011110000101101001"], 4)   # the box: the last bit is left 0
GRID = [[int(c) for c in row] for row in ("10011", "10101", "00010", "00100")]   # k = 2
GRID_K = 2
GRID_STARTS = [(0, 1), (1, 2), (2, 0), (2, 3)]
GRID_BAD = [[int(c) for c in row] for row in ("10011", "10101", "00010", "00101")]   # (3, 4) flipped
CORNER = (1, 2)                                            # the square of the corners figure


# --- the references ------------------------------------------------------------------------------

def covers(i: int, n: int, k: int) -> list[int]:
    """The starts of the windows that cover bit i: p from i - k + 1 to i, and 0 <= p <= n - k."""
    return [p for p in range(max(0, i - k + 1), min(i, n - k) + 1)]


def apply(a, k, starts):
    out = list(a)
    for p in starts:
        for j in range(p, p + k):
            out[j] ^= 1
    return out


def brute(a, k) -> list[tuple[int, ...]]:
    """Every set of starts (each window once at most) that makes every bit 1."""
    n = len(a)
    m = max(0, n - k + 1)
    sols = []
    for mask in range(1 << m):
        starts = tuple(p for p in range(m) if mask >> p & 1)
        if all(apply(a, k, starts)):
            sols.append(starts)
    return sols


def table(n, k) -> dict:
    """Every set of starts at once: the array each set fixes (bit j of the key is a_j) -> the sets.
    The same brute force as brute(), for all 2^n arrays of n bits in one pass."""
    m = max(0, n - k + 1)
    full = (1 << n) - 1
    win = [((1 << k) - 1) << p for p in range(m)]
    out: dict = {}
    for mask in range(1 << m):
        cover = 0
        for p in range(m):
            if mask >> p & 1:
                cover ^= win[p]
        out.setdefault(full ^ cover, []).append(tuple(p for p in range(m) if mask >> p & 1))
    return out


def table2(R, C, kr, kc=None) -> dict:
    """The same for every R x C grid (cell (r, c) is bit r * C + c of the key)."""
    kc = kr if kc is None else kc
    pos = [(r, c) for r in range(R - kr + 1) for c in range(C - kc + 1)]
    sq = [sum(1 << ((r + i) * C + c + j) for i in range(kr) for j in range(kc)) for r, c in pos]
    full = (1 << (R * C)) - 1
    out: dict = {}
    for mask in range(1 << len(pos)):
        cover = 0
        for t in range(len(pos)):
            if mask >> t & 1:
                cover ^= sq[t]
        out.setdefault(full ^ cover, []).append([pos[t] for t in range(len(pos)) if mask >> t & 1])
    return out


def scan(a, k):
    """The forced scan: the window at i is chosen when the windows chosen so far leave bit i 0."""
    n, chosen = len(a), set()
    for i in range(n):
        now = a[i] ^ (sum(p in chosen for p in covers(i, n, k)) % 2)
        if now == 0:
            if i > n - k:
                return None
            chosen.add(i)
    return sorted(chosen)


def answer(a, k) -> int:
    s = scan(a, k)
    return -1 if s is None else len(s)


def events(a, k) -> list[dict]:
    """A row per bit until the scan stops: the windows open over i (started at i - k + 1 .. i - 1),
    their parity, the bit now, and what the scan does (start, skip, check, fail)."""
    n, chosen, rows = len(a), [], []
    for i in range(n):
        open_ = [p for p in chosen if p > i - k]
        par = len(open_) % 2
        now = a[i] ^ par
        can = i <= n - k
        act = ("start" if now == 0 else "skip") if can else ("check" if now == 1 else "fail")
        rows.append({"i": i, "a": a[i], "open": open_, "par": par, "now": now, "act": act})
        if act == "start":
            chosen.append(i)
        if act == "fail":
            break
    return rows


def cover2(g, kr, kc, starts):
    out = [list(row) for row in g]
    for r, c in starts:
        for rr in range(r, r + kr):
            for cc in range(c, c + kc):
                out[rr][cc] ^= 1
    return out


def brute2(g, kr, kc=None):
    kc = kr if kc is None else kc
    R, C = len(g), len(g[0])
    pos = [(r, c) for r in range(R - kr + 1) for c in range(C - kc + 1)]
    sols = []
    for mask in range(1 << len(pos)):
        starts = [pos[j] for j in range(len(pos)) if mask >> j & 1]
        if all(all(row) for row in cover2(g, kr, kc, starts)):
            sols.append(starts)
    return sols


def scan2(g, kr, kc=None):
    """Row-major forced scan of a grid: the rectangles over (r, c) counted one by one."""
    kc = kr if kc is None else kc
    R, C, chosen = len(g), len(g[0]), []
    for r in range(R):
        for c in range(C):
            over = sum(1 for (pr, pc) in chosen if pr <= r < pr + kr and pc <= c < pc + kc)
            if (g[r][c] ^ over % 2) == 0:
                if r + kr > R or c + kc > C:
                    return None
                chosen.append((r, c))
    return chosen


def events2(g, k) -> list[dict]:
    """A row per cell, row by row, until the scan stops: the parity of the squares over the cell
    (counted one by one), the cell now, and what the scan does (start, skip, check, fail)."""
    R, C, chosen, rows = len(g), len(g[0]), [], []
    for r in range(R):
        for c in range(C):
            par = sum(1 for (pr, pc) in chosen if pr <= r < pr + k and pc <= c < pc + k) % 2
            now = g[r][c] ^ par
            can = r + k <= R and c + k <= C
            act = ("start" if now == 0 else "skip") if can else ("check" if now == 1 else "fail")
            rows.append({"r": r, "c": c, "par": par, "now": now, "act": act})
            if act == "start":
                chosen.append((r, c))
            if act == "fail":
                return rows
    return rows


def dp_after(g, k, steps):
    """The page's d and p after the first `steps` cells of the scan: d holds three corners of every
    square (the fourth, the square's own cell, is already read), p the parity of the scanned cells."""
    R, C = len(g), len(g[0])
    ev = events2(g, k)[:steps]
    chosen = [(e["r"], e["c"]) for e in ev if e["act"] == "start"]
    d = [[0] * (C + 1) for _ in range(R + 1)]
    for r, c in chosen:
        for rr, cc in ((r, c + k), (r + k, c), (r + k, c + k)):
            d[rr][cc] ^= 1
    p = [[None] * C for _ in range(R)]
    for e in ev:
        r, c = e["r"], e["c"]
        p[r][c] = sum(1 for (pr, pc) in chosen if pr <= r < pr + k and pc <= c < pc + k) % 2
    return d, p


def answer2(g, kr, kc=None) -> int:
    s = scan2(g, kr, kc)
    return -1 if s is None else len(s)


def ring_cover(a, k, starts):
    n, out = len(a), list(a)
    for p in starts:
        for j in range(k):
            out[(p + j) % n] ^= 1
    return out


def ring_brute(a, k) -> list[tuple[int, ...]]:
    """On a ring a window may start at any of the n places (1 <= k <= n)."""
    n = len(a)
    return [tuple(p for p in range(n) if mask >> p & 1) for mask in range(1 << n)
            if all(ring_cover(a, k, [p for p in range(n) if mask >> p & 1]))]


def ring_solve(a, k):
    """The cycles of p -> p + k: x_p ^ x_(p-k) = a_p ^ a_(p-1) fixes each cycle from one bit; then
    one equation of the ring. Returns (number of solutions, the fewest windows) or (0, -1)."""
    n = len(a)
    g = math.gcd(n, k)
    x = [0] * n
    for s in range(g):            # each cycle from x_s = 0
        p = s
        for _ in range(n // g - 1):
            q = (p + k) % n
            x[q] = x[p] ^ a[q] ^ a[q - 1]
            p = q
        if x[s] != x[(s - k) % n] ^ a[s] ^ a[s - 1]:     # around the cycle
            return 0, -1
    flip = (k // g) % 2           # complementing one cycle changes every window sum by k / g
    cover0 = sum(x[(0 - j) % n] for j in range(k)) % 2
    if (a[0] ^ cover0) != 1:      # the base choice misses: complement an odd number of cycles
        if not flip:
            return 0, -1
        need = 1
    else:
        need = 0
    cyc = [[(s + j * k) % n for j in range(n // g)] for s in range(g)]
    ones = [sum(x[p] for p in c) for c in cyc]
    size = n // g
    if not flip:                  # any cycle can be complemented: 2^g solutions
        return 2 ** g, sum(min(o, size - o) for o in ones)
    best = None                   # complement a set of cycles with the parity `need`
    for mask in range(1 << g):
        if bin(mask).count("1") % 2 != need:
            continue
        cost = sum(size - ones[s] if mask >> s & 1 else ones[s] for s in range(g))
        best = cost if best is None else min(best, cost)
    return 2 ** (g - 1), best


def ring_min_by_switch(a, k) -> int:
    """The page's rule for the fewest windows on a ring: the cheaper side of every cycle, and when
    k / g is odd and the parity is wrong, switch the cycle with the smallest difference."""
    n = len(a)
    g = math.gcd(n, k)
    sols = ring_brute(a, k)
    if not sols:
        return -1
    base = set(sols[0])
    cyc = [[(s + j * k) % n for j in range(n // g)] for s in range(g)]
    ones = [sum(p in base for p in c) for c in cyc]
    size = n // g
    pick = [size - o < o for o in ones]               # complement a cycle when it is cheaper
    cost = sum(min(o, size - o) for o in ones)
    if (k // g) % 2 == 1 and sum(pick) % 2 == 1:      # an odd number of complements breaks the ring
        cost += min(abs(size - 2 * o) for o in ones)
    return cost


# --- drawing helpers -------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def bitrow(bits, cls_of=lambda j: "") -> str:
    """A row of bit cells, bit 0 on the left; a 1 tinted, extra classes per place."""
    cells = []
    for j, b in enumerate(bits):
        cls = "kf-b" + (" kf-one" if b else "") + (f" {cls_of(j)}" if cls_of(j) else "")
        cells.append(f'<span class="{cls}">{b}</span>')
    return f'<span class="kf-w" dir="ltr">{"".join(cells)}</span>'


# --- part a: the scan of the example -----------------------------------------------------------------

def scan_table(a=EXAMPLE, k=EXAMPLE_K) -> str:
    starts = scan(a, k)
    rows = ["| הצעד | הביטים | מה הפכנו |", "|:-:|:-:|:-:|",
            f"| 0 | {bitrow(a, lambda j: 'kf-first' if j == starts[0] else '')} | {RLM}– |"]
    cur = list(a)
    for s, p in enumerate(starts, 1):
        cur = apply(cur, k, [p])
        nxt = next((j for j, b in enumerate(cur) if b == 0), None)
        mark = lambda j, p=p, nxt=nxt: ("kf-flip" if p <= j < p + k else "") + (" kf-first" if j == nxt else "")  # noqa: E731
        rows.append(f"| {s} | {bitrow(cur, lambda j: mark(j).strip())} | החלון שמתחיל ב-{p} |")
    return "\n".join(rows)


def scan_legend() -> str:
    return ('<span class="viz-legend"><span><i class="kf-key-one"></i>ביט 1</span>'
            '<span><i class="kf-key-first"></i>הביט הראשון שהוא 0 : החלון שמתחיל בו כפוי</span>'
            '<span><i class="kf-key-flip"></i>שלושת הביטים שהצעד הפך</span></span>')


# --- part a: which windows cover bit i ---------------------------------------------------------------

def forcing_svg(a=EXAMPLE, k=EXAMPLE_K, i=4) -> str:
    n = len(a)
    m = n - k + 1
    CW, L, T = 30, 34, 22          # cell width, the label column, the top of the bits row
    BH, BG = 15, 7                 # a window's bar and the gap between bars
    top_bars = T + CW + 10
    H = top_bars + m * (BH + BG) + 4
    W = L + n * CW + 4
    decided = [p for p in covers(i, n, k) if p < i]
    o = [f'<svg class="figure kf-cover" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.2f}rem" direction="ltr" role="img" '
         f'aria-label="שמונת הביטים של הדוגמה, ומתחתם {m} החלונות האפשריים, חלון לכל התחלה מ-0 עד {n - k}. '
         f'את ביט {i} מכסים החלונות שמתחילים ב-{decided[0]}, ב-{decided[1]} וב-{i}. כשהסריקה מגיעה לביט {i} '
         f'שני הראשונים כבר הוחלטו, והחלון שמתחיל ב-{i} הוא היחיד שנשאר. בביטים {n - k + 1} ו-{n - 1} לא מתחיל אף חלון">']
    # the column of bit i and the bits where no window starts
    o.append(f'<rect class="kf-col" x="{L + i * CW}" y="{T - 18}" width="{CW}" height="{H - T + 16}" rx="3"/>')
    for j in range(n - k + 1, n):
        o.append(f'<rect class="kf-nostart" x="{L + j * CW + 2}" y="{top_bars - 4}" width="{CW - 4}" height="{H - top_bars}" rx="3"/>')
    for j in range(n):
        x = L + j * CW + CW / 2
        o.append(f'<text class="kf-idx" x="{x:.0f}" y="{T - 6}" text-anchor="middle">{j}</text>')
        o.append(f'<rect class="kf-cell{" kf-one" if a[j] else ""}" x="{L + j * CW + 2}" y="{T}" width="{CW - 4}" height="{CW - 4}" rx="3"/>'
                 f'<text class="kf-bit" x="{x:.0f}" y="{T + CW / 2 + 3:.0f}" text-anchor="middle">{a[j]}</text>')
    o.append(f'<text class="kf-lab" x="{L - 8}" y="{T + CW / 2 + 3:.0f}" text-anchor="end">a</text>')
    for p in range(m):
        y = top_bars + p * (BH + BG)
        cls = "kf-new" if p == i else "kf-old" if p in decided else "kf-other"
        title = (f"x{p}: the only window over bit {i} not decided yet" if p == i else
                 f"x{p}: decided before bit {i}, covers it" if p in decided else f"x{p}: does not cover bit {i}")
        o.append(f'<g class="kf-bar {cls}"><title>{title}</title><rect x="{L + p * CW + 3}" y="{y}" width="{k * CW - 6}" height="{BH}" rx="4"/></g>')
        o.append(f'<text class="kf-lab" x="{L - 8}" y="{y + BH - 3}" text-anchor="end">x{p}</text>')
    o.append("</svg>")
    return "".join(o)


def forcing_legend(i=4) -> str:
    return ('<span class="viz-legend"><span><i class="kf-key-old"></i>חלונות שכבר הוחלטו ומכסים את ביט 4</span>'
            '<span><i class="kf-key-new"></i>החלון היחיד שעוד לא הוחלט : מתחיל ב-4</span>'
            '<span><i class="kf-key-other"></i>חלון שלא מכסה את ביט 4</span>'
            '<span><i class="kf-key-nostart"></i>שום חלון לא מתחיל כאן : רק בדיקה</span></span>')


# --- part a: the queue of the open windows -----------------------------------------------------------

ACT = {"start": "פותחים חלון", "skip": "כלום", "check": "בדיקה : 1", "fail": "בדיקה : 0, אין פתרון"}


def trace_table(a=EXAMPLE, k=EXAMPLE_K) -> str:
    rows = ["| ‏i | ‏a[i] | החלונות הפתוחים | הזוגיות | הביט עכשיו | מה עושים |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for e in events(a, k):
        q = ltr("[" + ", ".join(map(str, e["open"])) + "]") if e["open"] else "אין"
        act = ACT[e["act"]] + (f" ב-{e['i']}" if e["act"] == "start" else "")
        rows.append(f"| {e['i']} | {e['a']} | {q} | {e['par']} | {e['now']} | {act} |")
    return "\n".join(rows)


# --- part b: the grid example ------------------------------------------------------------------------

def grid_svg(g=GRID, k=GRID_K) -> str:
    R, C = len(g), len(g[0])
    S, GAP, PAD = 26, 34, 3
    starts = scan2(g, k)
    end = cover2(g, k, k, starts)
    W = 2 * C * S + GAP + 2 * PAD
    H = R * S + 2 * PAD
    o = [f'<svg class="figure kf-grid" viewBox="0 0 {W} {H}" style="max-width:{W * 1.25 / 16:.2f}rem" direction="ltr" role="img" '
         f'aria-label="לוח של {R} על {C} עם ריבועים של {k} על {k}. משמאל הלוח בהתחלה, עם {len(starts)} הריבועים שהסריקה בוחרת, '
         f'הפינה של כל אחד מסומנת. השורה האחרונה והעמודה האחרונה, שאין ריבוע שמתחיל בהן, מוצללות. מימין הלוח אחרי {len(starts)} '
         f'ההיפוכים : כל התאים 1">']
    for side, grid in ((0, g), (1, end)):
        x0 = PAD + side * (C * S + GAP)
        for r in range(R):
            for c in range(C):
                band = r > R - k or c > C - k
                cls = "kf-cell" + (" kf-one" if grid[r][c] else "") + (" kf-band" if band and side == 0 else "")
                x, y = x0 + c * S, PAD + r * S
                o.append(f'<rect class="{cls}" x="{x + 1}" y="{y + 1}" width="{S - 2}" height="{S - 2}" rx="3"/>'
                         f'<text class="kf-bit" x="{x + S / 2:.0f}" y="{y + S / 2 + 4:.0f}" text-anchor="middle">{grid[r][c]}</text>')
        if side == 0:
            for r, c in starts:
                x, y = x0 + c * S, PAD + r * S
                o.append(f'<g class="kf-sq"><title>square from ({r}, {c})</title><rect x="{x + 3.5}" y="{y + 3.5}" width="{k * S - 7}" height="{k * S - 7}" rx="5"/>'
                         f'<circle cx="{x + 8}" cy="{y + 8}" r="3"/></g>')
    arrow_x = PAD + C * S + GAP / 2
    o.append(f'<path class="kf-arrow" d="M{arrow_x - 9},{H / 2:.0f} h16 m-5,-5 l5,5 l-5,5" fill="none"/>')
    o.append("</svg>")
    return "".join(o)


def grid_legend() -> str:
    return ('<span class="viz-legend"><span><i class="kf-key-one"></i>תא 1</span>'
            '<span><i class="kf-key-sqv"></i>ריבוע שהסריקה בוחרת, הנקודה בפינה שלו</span>'
            '<span><i class="kf-key-band"></i>שורה או עמודה שאין ריבוע שמתחיל בה : רק בדיקה</span></span>')


def corners_svg(R=4, C=5, k=GRID_K, sq=CORNER) -> str:
    """One square in the difference array d (its four corners) and the prefix XOR of d."""
    r0, c0 = sq
    S, GAP, PAD = 26, 34, 3
    d = [[0] * (C + 1) for _ in range(R + 1)]
    for rr, cc in ((r0, c0), (r0, c0 + k), (r0 + k, c0), (r0 + k, c0 + k)):
        d[rr][cc] ^= 1
    p = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            p[r][c] = d[r][c] ^ (p[r - 1][c] if r else 0) ^ (p[r][c - 1] if c else 0) ^ (p[r - 1][c - 1] if r and c else 0)
    W = 2 * C * S + GAP + 2 * PAD
    H = R * S + 2 * PAD
    o = [f'<svg class="figure kf-grid kf-corners" viewBox="0 0 {W} {H}" style="max-width:{W * 1.25 / 16:.2f}rem" direction="ltr" role="img" '
         f'aria-label="ריבוע של {k} על {k} שמתחיל בתא ({r0}, {c0}). משמאל מערך ההפרשים d : ארבע פינות הופכות ל-1, בתאים '
         f'({r0}, {c0}), ({r0}, {c0 + k}), ({r0 + k}, {c0}) ו-({r0 + k}, {c0 + k}). מימין ה-XOR המצטבר של d, מכל התאים שמעל ומשמאל : '
         f'1 בדיוק בארבעת התאים של הריבוע">']
    for side, grid in ((0, d), (1, p)):
        x0 = PAD + side * (C * S + GAP)
        for r in range(R):
            for c in range(C):
                v = grid[r][c]
                cls = "kf-cell" + ((" kf-corner" if side == 0 else " kf-one") if v else "")
                x, y = x0 + c * S, PAD + r * S
                o.append(f'<rect class="{cls}" x="{x + 1}" y="{y + 1}" width="{S - 2}" height="{S - 2}" rx="3"/>'
                         f'<text class="kf-bit" x="{x + S / 2:.0f}" y="{y + S / 2 + 4:.0f}" text-anchor="middle">{v}</text>')
        if side == 1:
            x, y = x0 + c0 * S, PAD + r0 * S
            o.append(f'<g class="kf-sq"><rect x="{x + 3.5}" y="{y + 3.5}" width="{k * S - 7}" height="{k * S - 7}" rx="5"/></g>')
    arrow_x = PAD + C * S + GAP / 2
    o.append(f'<path class="kf-arrow" d="M{arrow_x - 9},{H / 2:.0f} h16 m-5,-5 l5,5 l-5,5" fill="none"/>')
    o.append("</svg>")
    return "".join(o)


def corners_legend() -> str:
    return ('<span class="viz-legend"><span><i class="kf-key-corner"></i>פינה שהריבוע הפך ב-d</span>'
            '<span><i class="kf-key-one"></i>‏1 ב-XOR המצטבר : התא מתחת לריבוע</span></span>')


def blocks():
    return [
        forcing_svg(),
        forcing_legend(),
        scan_table(),
        scan_legend(),
        trace_table(),
        grid_svg(),
        grid_legend(),
        corners_svg(),
        corners_legend(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
