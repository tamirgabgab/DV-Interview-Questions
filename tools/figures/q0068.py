#!/usr/bin/env python3
"""Figures and tables of question 0068 (the median of a stream with two heaps, the
p-quantile of a stream by the nearest rank, and the quantile over a sliding window with lazy
deletion).

    python tools/figures/fill.py 68        # put the blocks on the page

The references here are independent of the page code: brute_median() and brute_quantile()
sort the prefix (or the window), Heap is a binary heap with the same sift algorithm as the
twoheaps explorer (so the array layouts match), and trace_median(), trace_quantile() and
trace_window() replay the two heaps frame by frame (the rows of the tables and the frames of
the explorer). blocks() returns, in page order: the heap definition figure, the two heaps at
the end of part a's example with their legend, the table of part a, the two tables of part b
(p = 9/10 and p = 1/4) and the table of part c (W = 4, p = 1/2).
"""

from fractions import Fraction

RLM = "‏"
STREAM = [5, 15, 1, 3, 8, 7, 9, 10, 20, 2]
P_HIGH = (9, 10)
P_LOW = (1, 4)
W = 4
P_WIN = (1, 2)
HEAP_DEF = [1, 3, 2, 7, 4, 9, 5]


# --- references ----------------------------------------------------------------------------

def brute_median(values):
    """The median of the values: the middle one, or the mean of the two middle ones."""
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def rank_of(n, num, den):
    """The nearest rank of the p-quantile, p = num / den: ceil(p n), and 1 when p = 0."""
    return max(1, -(-num * n // den))


def brute_quantile(values, num, den):
    """The p-quantile by the nearest rank: the value at position ceil(p n) of the sorted
    values, 1-based."""
    return sorted(values)[rank_of(len(values), num, den) - 1]


class Heap:
    """A binary heap of (value, id) items, the smallest on top (or the largest, with
    is_max); ties by the smaller id. The same sift algorithm as the explorer's, so the
    array layouts are the same."""

    def __init__(self, is_max=False):
        self.a, self.is_max = [], is_max

    def before(self, x, y):
        if x[0] != y[0]:
            return x[0] > y[0] if self.is_max else x[0] < y[0]
        return x[1] < y[1]

    def push(self, x):
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and self.before(a[i], a[(i - 1) // 2]):
            a[i], a[(i - 1) // 2] = a[(i - 1) // 2], a[i]
            i = (i - 1) // 2

    def pop(self):
        a = self.a
        top, last = a[0], a.pop()
        if a:
            a[0] = last
            i = 0
            while True:
                k = i
                for c in (2 * i + 1, 2 * i + 2):
                    if c < len(a) and self.before(a[c], a[k]):
                        k = c
                if k == i:
                    break
                a[i], a[k] = a[k], a[i]
                i = k
        return top

    def top(self):
        return self.a[0]

    def __len__(self):
        return len(self.a)


def snap(low, high, **more):
    d = {"low": [list(x) for x in low.a], "high": [list(x) for x in high.a]}
    d.update(more)
    return d


def trace_median(nums):
    """Part a frame by frame: for every value, the push into low, the move of low's top to
    high, and the balance (the move back when high got bigger) with the median. Every frame
    keeps both heaps as arrays of [value, id]."""
    low, high, frames = Heap(True), Heap(False), []
    for i, x in enumerate(nums):
        low.push((x, i))
        frames.append(snap(low, high, kind="push", i=i, x=x))
        t = low.pop()
        high.push(t)
        frames.append(snap(low, high, kind="through", i=i, x=x, moved=list(t)))
        back = None
        if len(high) > len(low):
            back = high.pop()
            low.push(back)
        med = low.top()[0] if len(low) > len(high) else Fraction(low.top()[0] + high.top()[0], 2)
        frames.append(snap(low, high, kind="balance", i=i, x=x, moved=list(back) if back else None, ans=med))
    return frames


def trace_quantile(nums, num, den):
    """Part b frame by frame: the push into low, the move through to high, and the move
    back when the target size ceil(p n) grew, with the quantile (low's top)."""
    low, high, frames = Heap(True), Heap(False), []
    for i, x in enumerate(nums):
        low.push((x, i))
        frames.append(snap(low, high, kind="push", i=i, x=x, t=rank_of(i, num, den) if i else 0))
        t = low.pop()
        high.push(t)
        frames.append(snap(low, high, kind="through", i=i, x=x, moved=list(t), t=rank_of(i, num, den) if i else 0))
        target = rank_of(i + 1, num, den)
        back = None
        if len(low) < target:
            back = high.pop()
            low.push(back)
        frames.append(snap(low, high, kind="target", i=i, x=x, moved=list(back) if back else None, t=target, ans=low.top()[0]))
    return frames


def trace_window(nums, w, num, den):
    """Part c frame by frame: the oldest value leaves the window (marked dead, its heap's
    live count down), the push into low, the move through to high, and the move to the
    target size with the quantile. A dead value on top is thrown away before a top is
    read (pruned), and a heap with more dead than live values is rebuilt from its live
    ones; both are recorded on the frame they happened in."""
    low, high, frames = Heap(True), Heap(False), []
    side, live = {}, {"low": 0, "high": 0}
    heaps = {"low": low, "high": high}
    log = {"pruned": [], "rebuilt": []}

    def prune(s):
        h = heaps[s]
        while len(h) and h.top()[1] not in side:
            log["pruned"].append([s, list(h.pop())])

    def move(src, dst):
        prune(src)
        x = heaps[src].pop()
        heaps[dst].push(x)
        side[x[1]] = dst
        live[src] -= 1
        live[dst] += 1
        return list(x)

    def rebuild():
        for s, h in heaps.items():
            if len(h) > 2 * live[s]:
                keep = [x for x in h.a if x[1] in side]
                h.a = []
                for x in keep:
                    h.push(x)
                log["rebuilt"].append(s)

    def frame(kind, i, x, **more):
        dead = sorted(x[1] for h in heaps.values() for x in h.a if x[1] not in side)
        d = snap(low, high, kind=kind, i=i, x=x, left=max(0, i - w + 1), live=dict(live), dead=dead,
                 pruned=log["pruned"], rebuilt=log["rebuilt"], **more)
        log["pruned"], log["rebuilt"] = [], []
        frames.append(d)

    for i, x in enumerate(nums):
        if i >= w:
            gone = side.pop(i - w)
            live[gone] -= 1
            frame("leave", i, x, gone=[nums[i - w], i - w], gone_side=gone, t=rank_of(w, num, den))
        low.push((x, i))
        side[i] = "low"
        live["low"] += 1
        frame("push", i, x, t=rank_of(min(i, w), num, den) if i else 0)
        moved = move("low", "high")
        frame("through", i, x, moved=moved, t=rank_of(min(i, w), num, den) if i else 0)
        m = min(i + 1, w)
        target = rank_of(m, num, den)
        back = None
        if live["low"] < target:
            back = move("high", "low")
        elif live["low"] > target:
            back = move("low", "high")
        prune("low")
        rebuild()
        frame("target", i, x, moved=back, t=target, ans=low.top()[0])
    return frames


def levels(n):
    """The depth of a heap of n items: 1 + floor(log2 n), and 1 for an empty one."""
    d = 1
    while (1 << d) - 1 < max(n, 1):
        d += 1
    return d


# --- drawing ----------------------------------------------------------------------------

def num(v):
    """A number as the page writes it: the minus sign, not a hyphen."""
    return str(v).replace("-", "−")


def sval(v):
    """A value for a table cell: a negative one in an LTR span, or the RLM before it puts the
    minus after the digits."""
    return f'<span dir="ltr">{num(v)}</span>' if v < 0 else num(v)


def heap_def_svg(values):
    """The heap of the definition: the array as cells with their indices, and the same
    array as a tree, item k over its children 2k + 1 and 2k + 2."""
    n, cell, W = len(values), 36, 320
    L = levels(n)
    LH, top, R = 44, 22, 14
    H = top + L * LH + 26 + cell + 8
    h = Heap(False)
    for i, v in enumerate(values):
        h.push((v, i))
    a = [x[0] for x in h.a]
    s = (f'<svg class="figure th-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         f'aria-label="ערימת מינימום של {" ".join(map(num, values))} : המערך עם האינדקסים, ואותו מערך כעץ, כל איבר מעל שני ילדיו">')
    pos = {}
    for k in range(len(a)):
        d = levels(k + 1) - 1
        j = k + 1 - (1 << d)
        slot = (W - 16) / (1 << d)
        pos[k] = (8 + (j + 0.5) * slot, top + d * LH + R)
    for k in range(1, len(a)):
        (x1, y1), (x2, y2) = pos[(k - 1) // 2], pos[k]
        s += f'<line class="th-edge" x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}"/>'
    for k, v in enumerate(a):
        x, y = pos[k]
        s += (f'<g class="th-node{" is-top" if k == 0 else ""}"><title>a[{k}] = {v}</title><circle cx="{x:g}" cy="{y:g}" r="{R}"/>'
              f'<text x="{x:g}" y="{y + 4:g}" text-anchor="middle">{num(v)}</text></g>'
              f'<text class="tick" x="{x + R + 2:g}" y="{y - R + 4:g}">{k}</text>')
    y0 = top + L * LH + 18
    x0 = (W - n * cell) / 2
    s += f'<text class="th-lab" x="{x0 - 6:g}" y="{y0 + cell / 2 + 4:g}" text-anchor="end">a</text>'
    for k, v in enumerate(a):
        x = x0 + k * cell
        s += (f'<g class="th-cell{" is-top" if k == 0 else ""}"><title>a[{k}] = {v}</title><rect x="{x + 2:g}" y="{y0}" width="{cell - 4}" height="{cell - 8}" rx="4"/>'
              f'<text x="{x + cell / 2:g}" y="{y0 + cell / 2 - 1:g}" text-anchor="middle">{num(v)}</text></g>'
              f'<text class="tick" x="{x + cell / 2:g}" y="{y0 + cell + 4}" text-anchor="middle">{k}</text>')
    return s + "</svg>"


def heaps_svg(low, high, L, label, *, top=None, new=None, moved=None, dead=(), line="", lab_hi="high", lab_lo="low", live=None):
    """The two heaps facing each other: high as a tree with its root at the bottom, low as a
    tree with its root at the top, and the answer's line between them. Both trees are drawn
    for a depth L, so the figure keeps its size while the heaps grow. Each heap is an array
    of [value, id]."""
    W, LH, R, MID = 320, 40, 14, 44
    H = 2 * L * LH + MID + 16
    ymid = 8 + L * LH + MID / 2
    s = f'<svg class="figure th-fig th-two" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">'
    dead = set(dead)

    def tree(a, up, name):
        nonlocal s
        pos = {}
        for k in range(len(a)):
            d = levels(k + 1) - 1
            j = k + 1 - (1 << d)
            slot = min(64, (W - 16) / (1 << d))
            x = W / 2 + (j + 0.5 - (1 << d) / 2) * slot
            y = ymid - MID / 2 - 8 - R - d * LH if up else ymid + MID / 2 + 8 + R + d * LH
            pos[k] = (x, y)
        for k in range(1, len(a)):
            (x1, y1), (x2, y2) = pos[(k - 1) // 2], pos[k]
            s += f'<line class="th-edge" x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}"/>'
        for k, (v, i) in enumerate(a):
            x, y = pos[k]
            cls = " is-dead" if i in dead else ""
            if k == 0 and i not in dead:
                cls += " is-top"
            if new is not None and i == new:
                cls += " is-new"
            if moved is not None and i == moved:
                cls += " is-moved"
            what = "left the window, not thrown away yet" if i in dead else "the top" if k == 0 else "in the heap"
            s += (f'<g class="th-node{cls}"><title>{name}[{k}]: value {v}, arrival {i}, {what}</title><circle cx="{x:g}" cy="{y:g}" r="{R}"/>'
                  f'<text x="{x:g}" y="{y + 4:g}" text-anchor="middle">{num(v)}</text></g>')
            if i in dead:
                s += f'<line class="th-strike" x1="{x - 9:g}" y1="{y + 9:g}" x2="{x + 9:g}" y2="{y - 9:g}"/>'

    tree(high, True, "high")
    tree(low, False, "low")
    s += f'<line class="th-mid" x1="8" y1="{ymid:g}" x2="{W - 8}" y2="{ymid:g}"/>'
    nh = live["high"] if live else len(high)
    nl = live["low"] if live else len(low)
    s += (f'<text class="th-lab" x="10" y="{ymid - 8:g}">{lab_hi} ↑ {nh}</text>'
          f'<text class="th-lab" x="10" y="{ymid + 16:g}">{lab_lo} ↓ {nl}</text>')
    if line:
        s += f'<rect class="th-ans-bg" x="{W / 2 - 60:g}" y="{ymid - 11:g}" width="120" height="22" rx="11"/><text class="th-ans" x="{W / 2:g}" y="{ymid + 5:g}" text-anchor="middle">{line}</text>'
    return s + "</svg>"


def heaps_legend():
    return ('<span class="viz-legend"><span><i class="th-key-in"></i>בערימה</span><span><i class="th-key-top"></i>הראש</span>'
            '<span><i class="th-key-new"></i>הערך החדש</span><span><i class="th-key-moved"></i>עבר בצעד הזה</span>'
            '<span><i class="th-key-dead"></i>יצא מהחלון, עוד בערימה</span></span>')


def final_svg(nums):
    """The two heaps after the whole stream of part a, the median on the line."""
    f = trace_median(nums)[-1]
    med = f["ans"]
    return heaps_svg(f["low"], f["high"], levels(max(len(f["low"]), len(f["high"]))),
                     f"שתי הערימות אחרי כל הזרם {' '.join(map(num, nums))} : high למעלה, low למטה, והחציון על הקו ביניהן",
                     line=f"median = {fmt(med)}")


# --- tables --------------------------------------------------------------------------------

def fmt(v):
    """A median as the page writes it: a whole number, or a decimal with a half."""
    if isinstance(v, Fraction):
        return num(v.numerator) if v.denominator == 1 else num(f"{float(v):g}")
    return num(v)


def heap_cell(a, is_max, dead=()):
    """A heap's values as a cell: from the top, the top in bold, a dead value struck."""
    if not a:
        return "ריקה"
    items = sorted(a, key=lambda x: (-x[0] if is_max else x[0], x[1]))
    parts = []
    for k, (v, i) in enumerate(items):
        t = num(v)
        if i in dead:
            t = f"<s>{t}</s>"
        elif k == 0:
            t = f"<b>{t}</b>"
        parts.append(t)
    return RLM + '<span dir="ltr">' + " ".join(parts) + "</span>"


def table_median(nums):
    out = ["| ‏i | ‏x | עובר ל-high | חוזר ל-low | ‏low (הראש ראשון) | ‏high (הראש ראשון) | הגדלים | החציון |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    fr = trace_median(nums)
    for i, x in enumerate(nums):
        th, ba = fr[3 * i + 1], fr[3 * i + 2]
        back = f"{RLM}{sval(ba['moved'][0])}" if ba["moved"] else "אין צורך"
        out.append(f"| {RLM}{i + 1} | {RLM}{sval(x)} | {RLM}{sval(th['moved'][0])} | {back} | {heap_cell(ba['low'], True)} | "
                   f"{heap_cell(ba['high'], False)} | {RLM}{len(ba['low'])}, {len(ba['high'])} | **{RLM}{fmt(ba['ans'])}** |")
    return "\n".join(out)


def table_quantile(nums, num_, den):
    out = [f"| ‏n | ‏x | היעד ⌈{num_}n/{den}⌉ | חוזר ל-low | ‏low (הראש ראשון) | ‏high (הראש ראשון) | האחוזון | הרשימה הממוינת |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    fr = trace_quantile(nums, num_, den)
    for i, x in enumerate(nums):
        tg = fr[3 * i + 2]
        back = f"{RLM}{sval(tg['moved'][0])}" if tg["moved"] else "אין צורך"
        srt = sorted(nums[:i + 1])
        r = tg["t"]
        lst = " ".join(f"<b>{num(v)}</b>" if k == r - 1 else num(v) for k, v in enumerate(srt))
        out.append(f"| {RLM}{i + 1} | {RLM}{sval(x)} | {RLM}{r} | {back} | {heap_cell(tg['low'], True)} | {heap_cell(tg['high'], False)} | "
                   f"**{RLM}{sval(tg['ans'])}** | {RLM}<span dir=\"ltr\">{lst}</span> |")
    return "\n".join(out)


def table_window(nums, w, num_, den):
    out = ["| ‏i | ‏x | יוצא מהחלון | החלון | היעד | ‏low (הראש ראשון) | ‏high (הראש ראשון) | נזרקו / נבנתה מחדש | האחוזון |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    fr = trace_window(nums, w, num_, den)
    rows = {}
    for f in fr:
        rows.setdefault(f["i"], []).append(f)
    for i, x in enumerate(nums):
        mine = rows[i]
        tg = mine[-1]
        gone = next((f for f in mine if f["kind"] == "leave"), None)
        left = f"{RLM}{sval(gone['gone'][0])} (מ-{gone['gone_side']})" if gone else "אין"
        pruned = [f"{s}: {num(v)}" for f in mine for s, (v, _) in f["pruned"]]
        rebuilt = [s for f in mine for s in f["rebuilt"]]
        parts = ([f"נזרק מ-{RLM}" + '<span dir="ltr">' + "; ".join(pruned) + "</span>"] if pruned else []) + \
            ([f"נבנתה מחדש : {', '.join(rebuilt)}"] if rebuilt else [])
        note = "; ".join(parts) or "לא"
        win = " ".join(map(num, nums[tg["left"]:i + 1]))
        out.append(f"| {RLM}{i} | {RLM}{sval(x)} | {left} | {RLM}<span dir=\"ltr\">{win}</span> | {RLM}{tg['t']} | {heap_cell(tg['low'], True, tg['dead'])} | "
                   f"{heap_cell(tg['high'], False, tg['dead'])} | {note} | **{RLM}{sval(tg['ans'])}** |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [heap_def_svg(HEAP_DEF), final_svg(STREAM), heaps_legend(), table_median(STREAM),
            table_quantile(STREAM, *P_HIGH), table_quantile(STREAM, *P_LOW), table_window(STREAM, W, *P_WIN)]


if __name__ == "__main__":
    print([fmt(f["ans"]) for f in trace_median(STREAM) if f["kind"] == "balance"])
    print([f["ans"] for f in trace_quantile(STREAM, *P_HIGH) if f["kind"] == "target"])
    print([f["ans"] for f in trace_quantile(STREAM, *P_LOW) if f["kind"] == "target"])
    print([f["ans"] for f in trace_window(STREAM, W, *P_WIN) if f["kind"] == "target"])
    print("\n\n".join(blocks()))
