#!/usr/bin/env python3
"""Figures and tables of question 0069 (overtakes in a stream of out-of-order responses:
how many later requests overtook each request, how many earlier ones it overtook, and the
total, with a Fenwick tree).

    python tools/figures/fill.py 69        # put the blocks on the page

The references here are independent of the page code: brute_passed(), brute_overtook()
and brute_inversions() count every pair; Fen is a small Fenwick tree that records the
cells each query and update touched; walk_passed(), walk_overtook() and walk_live() replay
the three walks step by step (the rows of the tables and the frames of the overtakes
explorer); lis_length(), min_swaps() and max_distance() are the follow-ups. blocks()
returns, in page order: the crossing-lines figure of the example with its legend, the
Fenwick array of n = 8 with the ranges its cells cover, the table of part a's walk, the
two arrays side by side, the table of part b's walk and the table of part c's stream.
"""

from bisect import bisect_left

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
    for k, i in enumerate(arrival_order(done)):
        q, qpath = ft.prefix(i + 1)
        upath = ft.add(i + 1)
        total += k - q
        rows.append({"k": k, "i": i, "v": done[i], "rank": i + 1, "inserted": k, "arg": i + 1, "q": q,
                     "qpath": qpath, "upath": upath, "count": k - q, "total": total,
                     "disorder": total / pairs if pairs else 0.0, "tree": ft.tree[1:]})
    return rows


def lis_length(done):
    """The longest chain of requests answered in their send order (patience sorting)."""
    tails = []
    for v in done:
        p = bisect_left(tails, v)
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
        cross = sum(1 for j in range(n) if (j > i and done[j] < done[i]) or (j < i and done[j] > done[i]))
        s += (f'<line class="ov-line{" is-cross" if cross else ""}" x1="{cx(i):g}" y1="48" x2="{cx(pos[i]):g}" y2="94">'
              f'<title>request {i}: sent in slot {i}, answered at {done[i]}, slot {pos[i]} of the answers; {cross} overtakes on its line</title></line>')
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
    ]


if __name__ == "__main__":
    print(brute_passed(DONE), brute_overtook(DONE), brute_inversions(DONE))
    print("\n\n".join(blocks()))
