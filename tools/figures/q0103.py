#!/usr/bin/env python3
"""Figures and tables of question 0103, longest prefix match: a scan of the routing table, a
binary trie, a multibit trie with controlled prefix expansion, and a pipelined lookup.

    python tools/figures/fill.py 103        # put the blocks on the page

The references here are independent of the page code: a prefix is a string of bits, and

- best(routes, addr_bits) takes the longest prefix string that addr_bits starts with (the
  later of two equal rows), with no masks and no shifts;
- trie_nodes(routes) is the set of every prefix of every prefix string (the nodes of the
  binary trie), and the lookup path walks that set bit by bit;
- expand(routes, s) expands every prefix to the next multiple of s (at least s), a longer
  original prefix winning an expanded entry; the multibit trie's nodes are the distinct
  multiples of s bits above the expanded strings, and its lookup is best() on them;
- pipe_trace(routes, w, s, inputs) moves the lookups through w / s stages clock by clock,
  each stage reading one level of the multibit trie built by expand().

blocks() returns, in page order: the table of lookups of the 32-bit example, the binary trie
of the 8-bit example with the path of one lookup, its legend, the table of strides, the
expanded root of stride 2, the pipeline diagram and the table of the lookups clock by clock.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

NB = " "
RLM = "‏"

# The example of the page, 32 bits: (prefix, length, next hop); D is the default route.
EXAMPLE = [("10.0.0.0", 8, "A"), ("10.1.0.0", 16, "B"), ("10.1.2.0", 24, "C"),
           ("172.16.0.0", 12, "E"), ("0.0.0.0", 0, "D")]
LOOKUPS = ["10.1.2.3", "10.1.3.4", "10.200.0.1", "172.20.1.1", "172.32.0.1", "8.8.8.8"]

# The 8-bit example of the trie and the box: (bits of the prefix, next hop).
SMALL = [("", "D"), ("1", "A"), ("101", "B"), ("10110", "C"), ("01", "E")]
SMALL_W = 8
SMALL_ADDR = 185            # 1011 1001: the walk passes B, reaches 1011 and stops; the answer is B
PIPE_S = 2
PIPE_IN = [185, 182, None, 64, 3]      # the lookups entering the pipeline, one a clock (None: no lookup)


def quad_bits(quad: str, k: int) -> str:
    """The first k bits of a dotted quad, the first number the high byte."""
    n = 0
    for part in quad.split("."):
        n = n * 256 + int(part)
    return format(n, "032b")[:k]


def example_routes():
    return [(quad_bits(q, k), hop) for q, k, hop in EXAMPLE]


def best(routes, addr_bits):
    """The hop of the longest prefix string that addr_bits starts with; the later of equals."""
    got, got_len = None, -1
    for p, hop in routes:
        if addr_bits.startswith(p) and len(p) >= got_len:
            got, got_len = hop, len(p)
    return got


def matching(routes, addr_bits):
    return [(p, hop) for p, hop in routes if addr_bits.startswith(p)]


def trie_nodes(routes):
    """The nodes of the binary trie: every prefix of every prefix string (the root is '')."""
    return {""} | {p[:i] for p, _ in routes for i in range(len(p) + 1)}


def holder(routes):
    """The hop each node holds: the later row of a prefix given twice."""
    out = {}
    for p, hop in routes:
        out[p] = hop
    return out


def trie_path(routes, addr_bits):
    """The walk of the binary trie: (node, its hop or None, the best so far) per node visited."""
    nodes, held = trie_nodes(routes), holder(routes)
    out, b = [], None
    for i in range(len(addr_bits) + 1):
        node = addr_bits[:i]
        if node not in nodes:
            break
        b = held.get(node, b)
        out.append((node, held.get(node), b))
    return out


def target_len(k, s):
    """A /k prefix is expanded to the next multiple of s, and at least s (a /0 fills the root)."""
    return max(s, -(-k // s) * s)


def expand(routes, s):
    """Controlled prefix expansion: {expanded string: (hop, original length)}, a longer
    original prefix winning an entry, the later row of two equal ones."""
    out = {}
    for p, hop in routes:
        L = target_len(len(p), s)
        for j in range(1 << (L - len(p))):
            x = p + (format(j, f"0{L - len(p)}b") if L > len(p) else "")
            if x not in out or len(p) >= out[x][1]:
                out[x] = (hop, len(p))
    return out


def multibit_nodes(routes, s):
    """The nodes of the multibit trie: the root '' and every multiple of s bits that some
    expanded string goes past."""
    ex = expand(routes, s)
    return {""} | {x[:d] for x in ex for d in range(s, len(x), s)}


def multibit_stats(routes, w, s):
    """(steps of a lookup, nodes, entries = nodes * 2^s, filled entries) of stride s."""
    nodes = multibit_nodes(routes, s)
    return w // s, len(nodes), len(nodes) << s, len(expand(routes, s))


def multibit_lookup(routes, s, addr_bits):
    ex = expand(routes, s)
    return best([(x, hop) for x, (hop, _) in ex.items()], addr_bits)


def multibit_levels(routes, w, s):
    """The memories of the multibit trie level by level, nodes numbered in the order the
    page's insert creates them (the rows of the table in order): levels[d] is a flat list of
    entries (hop or None, child or None), 2^s per node."""
    F = 1 << s
    levels = [[] for _ in range(w // s)]
    index = [{} for _ in range(w // s)]        # node string -> its number in its level
    lens = [[] for _ in range(w // s)]

    def node(d, name):
        if name not in index[d]:
            index[d][name] = len(index[d])
            levels[d] += [[None, None] for _ in range(F)]
            lens[d] += [-1] * F
        return index[d][name]

    node(0, "")
    for p, hop in routes:
        L = target_len(len(p), s)
        n = 0
        for d in range(L // s - 1):
            i = n * F + int(p[d * s:(d + 1) * s], 2)
            child = node(d + 1, p[:(d + 1) * s])
            levels[d][i][1] = child
            n = child
        d = L // s - 1
        free = L - len(p)
        base = n * F + (int(p[d * s:], 2) << free if len(p) > d * s else 0)
        for j in range(1 << free):
            if len(p) >= lens[d][base + j]:
                levels[d][base + j][0] = hop
                lens[d][base + j] = len(p)
    return levels


def pipe_trace(routes, w, s, inputs):
    """The pipeline clock by clock: after clock t (from 1), each stage holds None or
    (address, best so far, still walking); the lookup entering at clock t leaves the last
    stage after clock t + w/s - 1."""
    levels = multibit_levels(routes, w, s)
    L, F = w // s, 1 << s
    stages = [None] * L
    trace = []
    for t in range(len(inputs) + L - 1):
        a = inputs[t] if t < len(inputs) else None
        new = []
        for d in range(L):
            src = ((a, 0, True, None) if a is not None else None) if d == 0 else stages[d - 1]
            if src is None:
                new.append(None)
                continue
            addr, n, go, b = src
            if go:
                chunk = addr >> (w - (d + 1) * s) & (F - 1)
                hop, child = levels[d][n * F + chunk]
                b = hop if hop is not None else b
                go, n = child is not None, child if child is not None else 0
            new.append((addr, n, go, b))
        stages = new
        trace.append((a, [None if x is None else (x[0], x[3], x[2]) for x in stages]))
    return trace


# --- the blocks ------------------------------------------------------------------------------

def ltr(s):
    return f'<span dir="ltr">{s}</span>'


def lookups_table():
    routes = example_routes()
    rows = ["| הכתובת | השורות שמתאימות | הארוכה | הקפיצה הבאה |", "|---|---|:-:|:-:|"]
    for q in LOOKUPS:
        bits = quad_bits(q, 32)
        m = matching(routes, bits)
        names = ", ".join(f"/{len(p)}" for p, _ in sorted(m, key=lambda x: len(x[0])))
        longest = max(len(p) for p, _ in m)
        rows.append(f"| {RLM}{ltr(q)} | {RLM}{ltr(names)} | {RLM}/{longest} | {RLM}{best(routes, bits)} |")
    return "\n".join(rows)


def layout(nodes):
    """x of every node in units: the subtrees of two children side by side, a node with one
    child half a unit off it (to the right of a 0 child, to the left of a 1 child)."""
    pos = {}

    def go(n):
        kids = [n + b for b in "01" if n + b in nodes]
        if not kids:
            pos[n] = 0.0
            return 0.0, 0.0
        if len(kids) == 1:
            lo, hi = go(kids[0])
            pos[n] = pos[kids[0]] + (0.5 if kids[0][-1] == "0" else -0.5)
            return min(lo, pos[n]), max(hi, pos[n])
        lo0, hi0 = go(kids[0])
        lo1, hi1 = go(kids[1])
        shift = hi0 - lo1 + 1
        for x in list(pos):
            if x.startswith(kids[1]):
                pos[x] += shift
        pos[n] = (pos[kids[0]] + pos[kids[1]]) / 2
        return lo0, hi1 + shift

    lo, hi = go("")
    return {n: x - lo for n, x in pos.items()}, hi - lo


def trie_svg(routes, addr, w):
    nodes, held = trie_nodes(routes), holder(routes)
    pos, width = layout(nodes)
    bits = format(addr, f"0{w}b")
    path = trie_path(routes, bits)
    on = {n for n, _, _ in path}
    won = path[-1][2]
    win_node = max((n for n, h, _ in path if h is not None), key=len, default=None)
    U, R, DY, X0, Y0 = 44, 13, 46, 40, 26
    deep = max(len(n) for n in nodes)
    W = int(2 * X0 + width * U)
    H = Y0 + deep * DY + 30
    X = lambda n: X0 + pos[n] * U
    Y = lambda n: Y0 + len(n) * DY
    aria = (f"עץ הביטים של הטבלה הקטנה, כתובות של {w} ביטים{NB}: הקידומות "
            + ", ".join(f"{p or 'הריקה'} אל {h}" for p, h in routes)
            + f". החיפוש של {addr}, הביטים {bits}, עובר בצמתים "
            + ", ".join(n or "השורש" for n in sorted(on, key=len))
            + f" ונעצר, והתשובה {won}")
    s = [f'<svg class="figure lpm-trie" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.3f}rem" '
         f'direction="ltr" role="img" aria-label="{aria}">']
    for n in sorted(nodes, key=lambda x: (len(x), x)):
        if not n:
            continue
        par = n[:-1]
        cls = "lpm-edge is-on" if n in on else "lpm-edge"
        s.append(f'<line class="{cls}" x1="{X(par):.1f}" y1="{Y(par):.1f}" x2="{X(n):.1f}" y2="{Y(n):.1f}"/>')
        mx, my = (X(par) + X(n)) / 2, (Y(par) + Y(n)) / 2
        dx = -9 if n[-1] == "0" else 9
        s.append(f'<text class="lpm-bit" x="{mx + dx:.1f}" y="{my + 4:.1f}" text-anchor="middle">{n[-1]}</text>')
    if len(path) <= w and bits[:len(path)] not in nodes:      # the missing child where the walk stops
        last = path[-1][0]
        nxt = last + bits[len(last)]
        x0, y0 = X(last), Y(last)
        x1 = x0 + (-0.5 if nxt[-1] == "0" else 0.5) * U
        y1 = y0 + DY
        s.append(f'<line class="lpm-edge lpm-miss" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1 - R:.1f}"/>')
        s.append(f'<text class="lpm-miss-t" x="{x1:.1f}" y="{y1 + 4:.1f}" text-anchor="middle">×</text>')
    for n in sorted(nodes, key=lambda x: (len(x), x)):
        h = held.get(n)
        cls = ["lpm-node", "has-hop" if h else "no-hop"]
        if n in on:
            cls.append("is-on")
        if n == win_node:
            cls.append("is-win")
        tip = f"{n or 'השורש'}{NB}: {'הקידומת ' + n + '* אל ' + h if h else 'אין קידומת'}"
        s.append(f'<g class="{" ".join(cls)}"><circle cx="{X(n):.1f}" cy="{Y(n):.1f}" r="{R}"/>'
                 + (f'<text x="{X(n):.1f}" y="{Y(n) + 4:.1f}" text-anchor="middle">{h}</text>' if h else "")
                 + f'<title>{tip}</title></g>')
    for d in range(deep + 1):
        s.append(f'<text class="lpm-depth" x="6" y="{Y0 + d * DY + 4:.1f}">{d}</text>')
    s.append("</svg>")
    return "".join(s)


def trie_legend():
    return ('<span class="viz-legend"><span><i class="lpm-key-hop"></i>צומת שמחזיק קידומת</span>'
            '<span><i class="lpm-key-nohop"></i>צומת בדרך, בלי קידומת</span>'
            '<span><i class="lpm-key-on"></i>הדרך של החיפוש</span>'
            '<span><i class="lpm-key-win"></i>הקידומת הארוכה שנמצאה</span></span>')


def strides_table():
    routes = example_routes()
    rows = ["| ביטים בצעד s | צעדים לחיפוש | צמתים | כניסות בטבלאות | כניסות עם קפיצה |", "|:-:|:-:|:-:|:-:|:-:|"]
    for s in (1, 2, 4, 8):
        steps, n, e, filled = multibit_stats(routes, 32, s)
        rows.append(f"| {s} | {steps} | {n} | {e:,} | {filled} |")
    return "\n".join(rows)


def expansion_table():
    """The 8-bit example with s = 2: every row and the entries it fills."""
    s = PIPE_S
    ex = expand(SMALL, s)
    rows = ["| הקידומת | האורך | מורחבת ל | הכניסות | נשארות לה |", "|---|:-:|:-:|---|---|"]
    for p, hop in SMALL:
        L = target_len(len(p), s)
        mine = [p + format(j, f"0{L - len(p)}b") if L > len(p) else p for j in range(1 << (L - len(p)))]
        kept = [x for x in mine if ex[x] == (hop, len(p))]
        name = (p or "ε") + "*"
        cell = lambda xs: (RLM + ", ".join(f"<code>{x}</code>" for x in xs)) if xs else "אף אחת"
        rows.append(f"| {RLM}<code>{name}</code> אל {hop} | {len(p)} | {L} | {cell(mine)} | {cell(kept)} |")
    return "\n".join(rows)


def pipe_svg():
    """The pipeline: the address enters stage 1, each stage reads its level's memory with s
    bits of the address and the node from the stage before, and passes the address, the node,
    the best hop so far and valid to the next stage."""
    L = SMALL_W // PIPE_S
    BW, BH, GAP, X0, Y0 = 92, 118, 34, 20, 34
    W = X0 * 2 + L * BW + (L - 1) * GAP
    H = Y0 + BH + 34
    aria = (f"צנרת של {L} שלבים לכתובת של {SMALL_W} ביטים, {PIPE_S} ביטים בכל שלב{NB}: כל שלב קורא את הזיכרון "
            "של הרמה שלו, וברגיסטרים שלו עוברים לשלב הבא הכתובת, הצומת, הקפיצה הטובה עד עכשיו ו-valid")
    s = [f'<svg class="figure lpm-pipe" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.3f}rem" direction="ltr" role="img" aria-label="{aria}">']
    for d in range(L):
        x = X0 + d * (BW + GAP)
        hi = SMALL_W - 1 - d * PIPE_S
        s.append(f'<rect class="lpm-stage" x="{x}" y="{Y0}" width="{BW}" height="{BH}" rx="6"/>')
        s.append(f'<text class="lpm-st-name" x="{x + BW / 2}" y="{Y0 - 10}" text-anchor="middle">stage {d + 1}</text>')
        s.append(f'<rect class="lpm-mem" x="{x + 10}" y="{Y0 + 12}" width="{BW - 20}" height="40" rx="3"/>')
        s.append(f'<text class="lpm-mem-t" x="{x + BW / 2}" y="{Y0 + 30}" text-anchor="middle">level {d}</text>')
        s.append(f'<text class="lpm-mem-s" x="{x + BW / 2}" y="{Y0 + 45}" text-anchor="middle">a[{hi}:{hi - PIPE_S + 1}]</text>')
        s.append(f'<rect class="lpm-reg" x="{x + 10}" y="{Y0 + 66}" width="{BW - 20}" height="40" rx="3"/>')
        s.append(f'<text class="lpm-reg-t" x="{x + BW / 2}" y="{Y0 + 83}" text-anchor="middle">v a node</text>')
        s.append(f'<text class="lpm-reg-t" x="{x + BW / 2}" y="{Y0 + 98}" text-anchor="middle">go best</text>')
        s.append(f'<line class="lpm-wire" x1="{x + BW / 2}" y1="{Y0 + 52}" x2="{x + BW / 2}" y2="{Y0 + 66}"/>')
        if d < L - 1:
            s.append(f'<line class="lpm-wire lpm-arrow" x1="{x + BW}" y1="{Y0 + 86}" x2="{x + BW + GAP - 2}" y2="{Y0 + 86}"/>')
            s.append(f'<path class="lpm-head" d="M{x + BW + GAP - 2},{Y0 + 86} l-7,-4 v8 z"/>')
    s.append(f'<text class="lpm-io" x="{X0}" y="{Y0 + BH + 24}">in: valid, addr</text>')
    s.append(f'<text class="lpm-io" x="{W - X0}" y="{Y0 + BH + 24}" text-anchor="end">out: valid, hit, hop</text>')
    s.append("</svg>")
    return "".join(s)


def pipe_table():
    L = SMALL_W // PIPE_S
    tr = pipe_trace(SMALL, SMALL_W, PIPE_S, PIPE_IN)
    head = "| שעון | נכנס | " + " | ".join(f"שלב {d + 1}" for d in range(L)) + " |"
    rows = [head, "|:-:|:-:|" + ":-:|" * L]
    for t, (a, st) in enumerate(tr, 1):
        cells = []
        for d, x in enumerate(st):
            if x is None:
                cells.append("–")
            else:
                addr, b, go = x
                txt = f"{RLM}{ltr(f'{addr} · {b or chr(8211)}')}"
                cells.append(f"**{txt}**" if d == L - 1 else txt)
        rows.append(f"| {t} | {'–' if a is None else a} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    out = [
        lookups_table(),
        trie_svg(SMALL, SMALL_ADDR, SMALL_W),
        trie_legend(),
        expansion_table(),
        strides_table(),
        pipe_svg(),
        pipe_table(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    r = example_routes()
    for q in LOOKUPS:
        print(q, best(r, quad_bits(q, 32)))
    for s in (1, 2, 4, 8):
        print(s, multibit_stats(r, 32, s))
    print(len(trie_nodes(r)))
    print(trie_path(SMALL, format(SMALL_ADDR, "08b")))
    for t, x in enumerate(pipe_trace(SMALL, 8, 2, PIPE_IN), 1):
        print(t, x)
    print(multibit_levels(SMALL, 8, 2))
