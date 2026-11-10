#!/usr/bin/env python3
"""Figures and tables of question 0069 (overtakes in a stream of out-of-order responses:
how many later requests overtook each request, how many earlier ones it overtook, and the
total, with a Fenwick tree).

    python tools/figures/fill.py 69        # put the blocks on the page

The references here are independent of the page code: brute_passed(), brute_overtook()
and brute_inversions() count every pair; Fen is a small Fenwick tree that records the
cells each query and update touched; walk_passed(), walk_overtook() and walk_live() replay
the three walks step by step (the rows of the tables and the frames of the overtakes
explorer); lis_length(), min_swaps() and max_distance() are the follow-ups. hw_rows() is
the RTL monitor of part c clock by clock (a bit per answered request, a popcount of the bits
above the response's own). blocks() returns, in page order: the crossing-lines figure of the
example with its legend, the Fenwick array of n = 8 with the ranges its cells cover, the
table of part a's walk, the two arrays side by side, the table of part b's walk, the table
of part c's stream, and the monitor's block diagram, its legend and its table per clock.
"""

from bisect import bisect_right
from html import escape

RLM = "‏"
NB = " "
DONE = [5, 2, 6, 1]


# --- references ---------------------------------------------------------------------------

def brute_passed(done):
    """passed[i]: later requests answered strictly before request i, every pair tried."""
    n = len(done)
    return [sum(1 for j in range(i + 1, n) if done[j] < done[i]) for i in range(n)]


def brute_overtook(done):
    """overtook[i]: earlier requests answered strictly after request i."""
    return [sum(1 for j in range(i) if done[j] > done[i]) for i in range(len(done))]


def brute_inversions(done):
    return sum(brute_passed(done))


def ranks(done):
    """Every value to its rank among the distinct values, 1 for the smallest."""
    return {v: r for r, v in enumerate(sorted(set(done)), start=1)}


def arrival_order(done):
    """The requests in the order their responses arrive (an equal time keeps the send order)."""
    return sorted(range(len(done)), key=lambda i: (done[i], i))


def lowbit(i):
    return i & -i


class Fen:
    """A Fenwick tree over 1..n that remembers the cells of its last walk."""

    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i):
        path = []
        while i <= self.n:
            self.tree[i] += 1
            path.append(i)
            i += lowbit(i)
        return path

    def prefix(self, i):
        s, path = 0, []
        while i > 0:
            s += self.tree[i]
            path.append(i)
            i -= lowbit(i)
        return s, path


def walk_passed(done):
    """Part a step by step: from the last request to the first, the query of the ranks below
    the request's rank (the later requests already in the tree that were answered before it)
    and then the insertion of its rank. A row per request."""
    rk = ranks(done)
    ft = Fen(len(rk))
    rows = []
    for k, i in enumerate(range(len(done) - 1, -1, -1)):
        r = rk[done[i]]
        q, qpath = ft.prefix(r - 1)
        upath = ft.add(r)
        rows.append({"k": k, "i": i, "v": done[i], "rank": r, "inserted": k, "arg": r - 1, "q": q,
                     "qpath": qpath, "upath": upath, "count": q, "tree": ft.tree[1:]})
    return rows


def walk_overtook(done):
    """Part b step by step: from the first request to the last, the query of the ranks up
    to the request's rank; the earlier requests not among them were answered after it."""
    rk = ranks(done)
    ft = Fen(len(rk))
    rows = []
    for i, v in enumerate(done):
        r = rk[v]
        q, qpath = ft.prefix(r)
        upath = ft.add(r)
        rows.append({"k": i, "i": i, "v": v, "rank": r, "inserted": i, "arg": r, "q": q,
                     "qpath": qpath, "upath": upath, "count": i - q, "tree": ft.tree[1:]})
    return rows


def walk_live(done):
    """Part c, the stream: the responses in arrival order, a tree over the send indices (no
    compression); when request i arrives, the answered requests sent after it are the
    answered so far minus those sent up to i. The running total and the disorder."""
    n = len(done)
    ft = Fen(n)
    rows, total = [], 0
    pairs = n * (n - 1) // 2
    arrived, head = set(), 0
    for k, i in enumerate(arrival_order(done)):
        q, qpath = ft.prefix(i + 1)
        upath = ft.add(i + 1)
        total += k - q
        # a reorder buffer that delivers in send order: it takes the response and hands on
        # the head while it has it; held is what still waits, for the request `head`
        arrived.add(i)
        while head in arrived:
            arrived.remove(head)
            head += 1
        rows.append({"k": k, "i": i, "v": done[i], "rank": i + 1, "inserted": k, "arg": i + 1, "q": q,
                     "qpath": qpath, "upath": upath, "count": k - q, "total": total,
                     "disorder": total / pairs if pairs else 0.0, "tree": ft.tree[1:],
                     "held": len(arrived), "head": head})
    return rows


def hw_rows(done):
    """The RTL monitor of part c on a trace with one response per clock (distinct times):
    a row per response, with the clock, the request, the vector `answered` before and after
    the edge (bit i is request i), the answered bits above the request (its passed), and
    the registers max_passed and total after the edge."""
    assert len(set(done)) == len(done)
    answered, mx, total, rows = 0, 0, 0, []
    for i in arrival_order(done):
        above = answered >> (i + 1)
        p = bin(above).count("1")
        before, answered = answered, answered | (1 << i)
        mx, total = max(mx, p), total + p
        rows.append({"clk": done[i], "seq": i, "before": before, "above": above << (i + 1), "passed": p,
                     "after": answered, "max": mx, "total": total})
    return rows


def lis_length(done):
    """The longest chain of requests answered in their send order, none overtaking another:
    the longest non-decreasing subsequence, since an equal time is not an overtake (patience
    sorting, the first tail that is larger)."""
    tails = []
    for v in done:
        p = bisect_right(tails, v)
        if p == len(tails):
            tails.append(v)
        else:
            tails[p] = v
    return len(tails)


def min_swaps(done):
    """Fewest swaps that put the responses in send order: n minus the number of cycles of
    the permutation (distinct times)."""
    order = arrival_order(done)
    seen, cycles = [False] * len(done), 0
    for s in range(len(done)):
        if seen[s]:
            continue
        cycles += 1
        j = s
        while not seen[j]:
            seen[j] = True
            j = order[j]
    return len(done) - cycles


def max_distance(done):
    """The largest j - i over the overtakes (done[j] < done[i], j > i): the prefix maximum
    against the suffix minimum with two pointers, O(n)."""
    n = len(done)
    if n == 0:
        return 0
    suf = list(done)
    for i in range(n - 2, -1, -1):
        suf[i] = min(suf[i], suf[i + 1])
    best, i, j = 0, 0, 0
    while i < n and j < n:
        if suf[j] < done[i]:
            best = max(best, j - i)
            j += 1
        else:
            i += 1
    return best


# --- figures ------------------------------------------------------------------------------

def num(v):
    return str(v).replace("-", "−")


CELL, LW = 40, 64


def cross_svg(done, counts, name, label):
    """The requests in send order on the top row (the time of each), the responses in
    arrival order on the bottom row, a line from every request to its response (crossing
    lines are overtakes), and the counts of the array `name` under the top row."""
    n, order = len(done), arrival_order(done)
    pos = {i: p for p, i in enumerate(order)}
    W, H = LW + n * CELL + 8, 190
    cx = lambda p: LW + p * CELL + CELL / 2
    s = (f'<svg class="figure ov-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         f'aria-label="{label}">')
    s += f'<text class="tick" x="{LW - 8}" y="12" text-anchor="end">i</text>'
    s += f'<text class="ov-lab" x="{LW - 8}" y="39" text-anchor="end">done</text>'
    s += f'<text class="ov-lab" x="{LW - 8}" y="111" text-anchor="end">arrive</text>'
    s += f'<text class="tick" x="{LW - 8}" y="138" text-anchor="end">time</text>'
    s += f'<text class="ov-lab" x="{LW - 8}" y="171" text-anchor="end">{name}</text>'
    for i in range(n):
        s += f'<text class="tick" x="{cx(i):g}" y="12" text-anchor="middle">{i}</text>'
    # the lines first, so the cells cover their ends
    for i in range(n):
        p = sum(1 for j in range(i + 1, n) if done[j] < done[i])
        o = sum(1 for j in range(i) if done[j] > done[i])
        s += (f'<line class="ov-line{" is-cross" if p + o else ""}" x1="{cx(i):g}" y1="48" x2="{cx(pos[i]):g}" y2="94">'
              f'<title>request {i}: sent in slot {i}, answered at {done[i]}, slot {pos[i]} of the answers; its line is crossed '
              f'{p + o} times: passed {p} + overtook {o}</title></line>')
    for i, v in enumerate(done):
        s += (f'<g class="ov-cell is-req"><title>request {i}, answered at time {v}</title>'
              f'<rect x="{LW + i * CELL + 4}" y="20" width="{CELL - 8}" height="28" rx="4"/>'
              f'<text x="{cx(i):g}" y="39" text-anchor="middle">{num(v)}</text></g>')
    for p, i in enumerate(order):
        s += (f'<g class="ov-cell is-rsp"><title>answer slot {p}: request {i}, time {done[i]}</title>'
              f'<rect x="{LW + p * CELL + 4}" y="94" width="{CELL - 8}" height="28" rx="4"/>'
              f'<text x="{cx(p):g}" y="113" text-anchor="middle">{i}</text></g>')
        s += f'<text class="tick" x="{cx(p):g}" y="138" text-anchor="middle">{num(done[i])}</text>'
    for i, c in enumerate(counts):
        s += (f'<g class="ov-cnt{" is-zero" if c == 0 else ""}"><title>{name}[{i}] = {c}</title>'
              f'<rect x="{LW + i * CELL + 4}" y="152" width="{CELL - 8}" height="28" rx="4"/>'
              f'<text x="{cx(i):g}" y="171" text-anchor="middle">{c}</text></g>')
    return s + "</svg>"


def cross_legend():
    return (f'<span class="viz-legend"><span><i class="ov-key-req"></i>בקשה, לפי סדר השליחה, עם זמן התשובה</span>'
            '<span><i class="ov-key-rsp"></i>תשובה, לפי סדר ההגעה, עם מספר הבקשה</span>'
            f'<span><i class="ov-key-cross"></i>קו שחוצה קו אחר{NB}: עקיפה</span>'
            '<span><i class="ov-key-cnt"></i>הספירה של הבקשה</span></span>')


def fenwick_svg(n=8, tree=None, qpath=(), upath=(), label=None, under=None, live=False):
    """The Fenwick array of n cells: a bar above each cell over the range it covers,
    (i - lowbit(i), i], stacked by the size of the range; the index and its binary under
    the cell. With tree the values are written in the cells, and the cells of a query path
    and an update path are highlighted."""
    levels = n.bit_length()
    BAR, LVL = 14, 16
    top = 8 + levels * LVL
    H = top + 30 + 40
    W = LW + n * CELL + 8
    cx = lambda i: LW + (i - 1) * CELL + CELL / 2
    label = label or f"מערך Fenwick של {n} תאים{NB}: מעל כל תא הטווח שהוא מכסה, ומתחתיו האינדקס בבינארי"
    size = "" if live else f'style="max-width:{W / 16:g}rem" '
    s = (f'<svg class="figure ov-fig ov-fw{" ov-live" if live else ""}" viewBox="0 0 {W} {H}" '
         f'{size}role="img" aria-label="{label}">')
    s += f'<text class="ov-lab" x="{LW - 8}" y="{top + 19}" text-anchor="end">tree[i]</text>'
    s += f'<text class="tick" x="{LW - 8}" y="{top + 44}" text-anchor="end">i</text>'
    s += f'<text class="tick" x="{LW - 8}" y="{top + 57}" text-anchor="end">binary</text>'
    if under:
        s += f'<text class="tick" x="{LW - 8}" y="{top + 70}" text-anchor="end">{under[0]}</text>'
    for i in range(1, n + 1):
        lb = lowbit(i)
        lvl = lb.bit_length() - 1
        y = top - 4 - (lvl + 1) * LVL + (LVL - BAR)
        x0 = LW + (i - lb) * CELL + 3
        cls = " is-q" if i in qpath else " is-u" if i in upath else ""
        s += (f'<g class="ov-bar{cls}"><title>tree[{i}] covers {i - lb + 1}..{i}: {lb} cell{"s" if lb > 1 else ""}, the lowest set bit of {i}</title>'
              f'<rect x="{x0}" y="{y}" width="{lb * CELL - 6}" height="{BAR}" rx="3"/>'
              f'<text x="{x0 + (lb * CELL - 6) / 2:g}" y="{y + 11}" text-anchor="middle">{f"{i - lb + 1}..{i}" if lb > 1 else i}</text></g>')
        val = "" if tree is None else str(tree[i - 1])
        s += (f'<g class="ov-tc{cls}"><title>tree[{i}]{"" if tree is None else f" = {tree[i - 1]}"}</title>'
              f'<rect x="{LW + (i - 1) * CELL + 4}" y="{top}" width="{CELL - 8}" height="28" rx="4"/>'
              f'<text x="{cx(i):g}" y="{top + 19}" text-anchor="middle">{val}</text></g>')
        s += f'<text class="tick{cls}" x="{cx(i):g}" y="{top + 44}" text-anchor="middle">{i}</text>'
        s += f'<text class="ov-bin" x="{cx(i):g}" y="{top + 57}" text-anchor="middle">{i:0{levels}b}</text>'
        if under:
            s += f'<text class="tick" x="{cx(i):g}" y="{top + 70}" text-anchor="middle">{num(under[1][i - 1])}</text>'
    return s + "</svg>"


def fenwick_legend():
    return ('<span class="viz-legend"><span><i class="ov-key-bar"></i>הטווח שהתא מכסה, באורך הביט הדולק הנמוך של i</span>'
            '<span><i class="ov-key-q"></i>תאים שהשאילתה קוראת</span><span><i class="ov-key-u"></i>תאים שהעדכון מגדיל</span></span>')


# --- the RTL monitor ------------------------------------------------------------------------

HW_W, HW_H = 560, 244
# (x, y, w, h, stage, title, sub): stage 1 is the query (blue), 2 the update (orange)
HW_BLOCKS = [
    (86, 20, 116, 44, 0, "seq_of_tag", "[rsp_tag]"),
    (290, 20, 100, 44, 1, ">> seq+1", "bits above"),
    (418, 20, 110, 44, 1, "popcount", ""),
    (280, 110, 120, 44, 2, "answered", "N bits"),
    (418, 110, 110, 44, 0, "max_passed", "max"),
    (418, 190, 110, 44, 0, "total", "+= passed"),
]
# (points, arrow, label, label x, label y, anchor)
HW_WIRES = [
    ([(6, 42), (86, 42)], True, "rsp_tag", 8, 34, "start"),
    ([(202, 42), (290, 42)], True, "rsp_seq", 210, 34, "start"),
    ([(246, 42), (246, 132), (280, 132)], True, "set bit", 238, 128, "end"),
    ([(340, 110), (340, 64)], True, "", 0, 0, ""),
    ([(390, 42), (418, 42)], True, "", 0, 0, ""),
    ([(528, 42), (556, 42)], True, "passed", 556, 14, "end"),
    ([(542, 42), (542, 212), (528, 212)], True, "", 0, 0, ""),
    ([(542, 132), (528, 132)], True, "", 0, 0, ""),
]
HW_DOTS = [(246, 42), (542, 42), (542, 132)]


def hw_diagram():
    """The block diagram of the monitor ooo_monitor: the tag looked up to the request's send
    number, the vector `answered`, the bits above the request counted, a maximum register
    and a running sum."""
    label = ("תרשים המלבנים של המוניטור" + NB + ": הטבלה seq_of_tag הופכת את ה-tag של התשובה למספר השליחה rsp_seq, "
             "הווקטור answered מוזז ימינה ב-seq + 1 כך שנשארים הביטים שמעל הבקשה, ‏popcount סופר אותם ונותן את passed, "
             "ובאותו מחזור הביט rsp_seq של answered נדלק, max_passed שומר את המקסימום ו-total את הסכום")
    o = [f'<svg class="figure ov-dp" viewBox="0 0 {HW_W} {HW_H}" direction="ltr" style="max-width:{HW_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="ov-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="ov-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for x, y, w, h, stage, title, sub in HW_BLOCKS:
        ty = y + h / 2 + (-3 if sub else 5)
        cls = f" ov-st{stage}" if stage else ""
        o.append(f'<g class="ov-blk{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{escape(title)}</text>'
                 + (f'<text class="ov-sub" x="{x + w / 2:g}" y="{y + h / 2 + 14:g}" text-anchor="middle">{escape(sub)}</text>' if sub else "")
                 + "</g>")
    for pts, arrow, lab, lx, ly, anchor in HW_WIRES:
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        head = ' marker-end="url(#ov-hb)"' if arrow else ""
        o.append(f'<path class="ov-wire" d="{d}"{head}/>')
        if lab:
            o.append(f'<text class="ov-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    o += [f'<circle class="ov-dot" cx="{x}" cy="{y}" r="3.5"/>' for x, y in HW_DOTS]
    return "".join(o) + "</svg>"


def hw_legend():
    return ('<span class="viz-legend"><span><i class="ov-key-q"></i>השאילתה' + NB + ': הביטים שמעל הבקשה, וספירתם</span>'
            '<span><i class="ov-key-u"></i>העדכון' + NB + ': הביט של הבקשה נדלק</span>'
            '<span><i class="ov-key-req"></i>הטבלה מ-tag למספר השליחה, המקסימום והסכום</span></span>')


def hw_table(done):
    """The monitor on the example, a row per response (the clock is the response's time);
    the vectors are written with bit n - 1 on the left."""
    n = len(done)
    bits = lambda v: f"{RLM}`{v:0{n}b}`"
    out = [f"| מחזור | {RLM}rsp_seq | {RLM}answered לפני | הביטים שמעל | {RLM}passed | {RLM}answered אחרי | {RLM}max_passed | {RLM}total |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in hw_rows(done):
        out.append(f"| {RLM}{r['clk']} | {RLM}{r['seq']} | {bits(r['before'])} | {bits(r['above'])} | **{RLM}{r['passed']}** | "
                   f"{bits(r['after'])} | {RLM}{r['max']} | {RLM}{r['total']} |")
    return "\n".join(out)


# --- tables ---------------------------------------------------------------------------------

def tree_text(tree):
    return RLM + '<span dir="ltr">[' + ", ".join(str(t) for t in tree) + "]</span>"


def path_text(path):
    return RLM + '<span dir="ltr">' + " → ".join(f"tree[{i}]" for i in path) + "</span>" if path else "אין"


def table_passed(done):
    rows = walk_passed(done)
    out = ["| הצעד | הבקשה i | הזמן | הדרגה | השאילתה | התאים שנקראו | התוצאה | העדכון | העץ אחרי | ‏passed[i] |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        out.append(f"| {RLM}{r['k'] + 1} | {RLM}{r['i']} | {RLM}{r['v']} | {RLM}{r['rank']} | {RLM}prefix({r['arg']}) | {path_text(r['qpath'])} | "
                   f"{RLM}{r['q']} | {path_text(r['upath'])} | {tree_text(r['tree'])} | **{RLM}{r['count']}** |")
    return "\n".join(out)


def table_overtook(done):
    rows = walk_overtook(done)
    out = ["| הצעד | הבקשה i | הזמן | הדרגה | כבר בעץ | השאילתה | התוצאה | ‏overtook[i] | העדכון | העץ אחרי |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        out.append(f"| {RLM}{r['k'] + 1} | {RLM}{r['i']} | {RLM}{r['v']} | {RLM}{r['rank']} | {RLM}{r['inserted']} | {RLM}prefix({r['arg']}) | "
                   f"{RLM}{r['q']} | **{RLM}<span dir=\"ltr\">{r['inserted']} − {r['q']} = {r['count']}</span>** | {path_text(r['upath'])} | {tree_text(r['tree'])} |")
    return "\n".join(out)


def table_side(done):
    """The two arrays side by side, a row per request, with the pairs behind each count."""
    n = len(done)
    p, o = brute_passed(done), brute_overtook(done)
    out = ["| הבקשה i | הזמן | ‏passed[i] | מי עקף אותה | ‏overtook[i] | את מי היא עקפה |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i in range(n):
        who = [j for j in range(i + 1, n) if done[j] < done[i]]
        whom = [j for j in range(i) if done[j] > done[i]]
        out.append(f"| {RLM}{i} | {RLM}{done[i]} | **{RLM}{p[i]}** | {('הבקשות ' if len(who) > 1 else 'הבקשה ') + RLM + ', '.join(map(str, who)) if who else 'אף אחת'} | "
                   f"**{RLM}{o[i]}** | {('את ' if whom else '') + RLM + ', '.join(map(str, whom)) if whom else 'אף אחת'} |")
    out.append(f"| **סכום** | | **{RLM}{sum(p)}** | | **{RLM}{sum(o)}** | |")
    return "\n".join(out)


def table_live(done):
    rows = walk_live(done)
    n = len(done)
    pairs = n * (n - 1) // 2
    out = ["| ההגעה k | הבקשה i | הזמן | כבר ענו | ‏prefix(i + 1) | עקיפות שספגה | הסכום הרץ | אי-הסדר | העץ אחרי |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        out.append(f"| {RLM}{r['k']} | {RLM}{r['i']} | {RLM}{r['v']} | {RLM}{r['inserted']} | {RLM}{r['q']} | "
                   f"**{RLM}<span dir=\"ltr\">{r['inserted']} − {r['q']} = {r['count']}</span>** | {RLM}{r['total']} | "
                   f"{RLM}<span dir=\"ltr\">{r['total']}/{pairs} ≈ {r['disorder']:.2f}</span> | {tree_text(r['tree'])} |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    p = brute_passed(DONE)
    return [
        cross_svg(DONE, p, "passed", f"הבקשות 0 עד 3 עם זמני התשובה {' '.join(map(str, DONE))}, התשובות לפי סדר ההגעה, הקווים ביניהן, ו-passed של כל בקשה"),
        cross_legend(),
        fenwick_svg(8),
        fenwick_legend(),
        table_passed(DONE),
        table_side(DONE),
        table_overtook(DONE),
        table_live(DONE),
        hw_diagram(),
        hw_legend(),
        hw_table(DONE),
    ]


if __name__ == "__main__":
    print(brute_passed(DONE), brute_overtook(DONE), brute_inversions(DONE))
    print("\n\n".join(blocks()))
