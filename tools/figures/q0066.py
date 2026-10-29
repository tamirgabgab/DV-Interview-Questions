#!/usr/bin/env python3
"""Figures and tables of question 0066 (merge overlapping intervals; the total height at
every point of weighted half-open intervals, as pieces of constant total; the peak and the
ranges at or above a threshold).

    python tools/figures/fill.py 66        # put the blocks on the page

The references here are independent of the page code: brute_merge() joins intervals by
their overlap graph, brute_skyline() and brute_above() read the total height at every
integer point, and trace_merge(), trace_skyline() and trace_above() replay the three
solutions step by step (the rows of the tables and the frames of the intervals explorer).
blocks() returns, in page order: the figure of part a's example with its legend and the
table of its walk, the figure of part b's example with its legend and the table of its
events, and the table of part c's example.
"""

RLM = "‏"
IVS = [(1, 3), (2, 6), (8, 10), (15, 18)]                  # part a, closed intervals
TRIPLES = [(1, 7, 7), (2, 6, 4)]                            # part b, the owner's example
TRIPLES_C = [(0, 4, 2), (1, 3, 3), (2, 6, 1), (5, 8, 4)]    # part c, with the threshold T_C
T_C = 4


# --- references --------------------------------------------------------------------------

def brute_merge(intervals):
    """The merged closed intervals by the overlap graph: two intervals are joined when they
    share a point (touching ones included), and a merged interval is a connected set."""
    ivs = [tuple(x) for x in intervals]
    comp = list(range(len(ivs)))

    def find(i):
        while comp[i] != i:
            i = comp[i]
        return i

    for i, (s1, e1) in enumerate(ivs):
        for j, (s2, e2) in enumerate(ivs):
            if i < j and s1 <= e2 and s2 <= e1:
                comp[find(i)] = find(j)
    groups = {}
    for i, iv in enumerate(ivs):
        groups.setdefault(find(i), []).append(iv)
    return sorted((min(s for s, _ in g), max(e for _, e in g)) for g in groups.values())


def heights(triples):
    """The total height at every integer point x of [lo, hi): a dict x -> total (the total
    is constant on [x, x + 1) because every end is an integer)."""
    if not triples:
        return {}
    lo, hi = min(s for s, _, _ in triples), max(e for _, e, _ in triples)
    return {x: sum(h for s, e, h in triples if s <= x < e) for x in range(lo, hi)}


def runs(points, keep):
    """Maximal runs of consecutive integer points x with keep(total(x)), as (start, end)."""
    out = []
    for x in sorted(points):
        if not keep(points[x]):
            continue
        if out and out[-1][1] == x and keep(points[x - 1]) and points[x - 1] == points[x]:
            out[-1][1] = x + 1
        else:
            out.append([x, x + 1])
    return out


def brute_skyline(triples):
    """The pieces (start, end, total) of constant non-zero total, read point by point."""
    pts = heights(triples)
    out = []
    for x in sorted(pts):
        t = pts[x]
        if t == 0:
            continue
        if out and out[-1][1] == x and out[-1][2] == t:
            out[-1][1] = x + 1
        else:
            out.append([x, x + 1, t])
    return [tuple(p) for p in out]


def brute_above(triples, t):
    """The ranges where the total is at least t (t >= 1), read point by point."""
    pts = heights(triples)
    out = []
    for x in sorted(pts):
        if pts[x] < t:
            continue
        if out and out[-1][1] == x:
            out[-1][1] = x + 1
        else:
            out.append([x, x + 1])
    return [tuple(r) for r in out]


# --- traces --------------------------------------------------------------------------------

def trace_merge(intervals):
    """Part a interval by interval, in sorted order: the merged list before and after, and
    the decision (new: opens a merged interval; extend: the end grows; inside: it is within
    the last merged one, so nothing changes)."""
    ev, out = [], []
    for i, (s, e) in enumerate(sorted(tuple(x) for x in intervals)):
        before = [list(x) for x in out]
        if out and s <= out[-1][1]:
            kind = "extend" if e > out[-1][1] else "inside"
            out[-1][1] = max(out[-1][1], e)
        else:
            kind = "new"
            out.append([s, e])
        ev.append({"i": i, "s": s, "e": e, "kind": kind, "prev_end": before[-1][1] if before else None,
                   "before": before, "after": [list(x) for x in out]})
    return ev


def trace_skyline(triples):
    """Part b position by position: the events at the position (the ends, −h, before the
    starts, +h; each with the index of its interval), the running total before and after
    them, the piece emitted for the gap since the previous position (None when the total was
    0, or at the first position), whether it was joined to the previous piece, and the
    pieces so far."""
    events = sorted((p, d, i) for i, (s, e, h) in enumerate(triples) for p, d in ((s, h), (e, -h)))
    ev, out, total, prev = [], [], 0, None
    k = 0
    while k < len(events):
        p = events[k][0]
        mine = []
        while k < len(events) and events[k][0] == p:
            mine.append({"i": events[k][2], "d": events[k][1]})
            k += 1
        piece, joined = None, False
        if prev is not None and total != 0:
            if out and out[-1][1] == prev and out[-1][2] == total:
                out[-1][1] = p
                joined = True
            else:
                out.append([prev, p, total])
            piece = [prev, p, total]
        before = total
        total += sum(m["d"] for m in mine)
        ev.append({"p": p, "events": mine, "before": before, "after": total, "prev": prev,
                   "piece": piece, "joined": joined, "pieces": [list(x) for x in out]})
        prev = p
    return ev


def skyline_ref(triples):
    """The pieces of part b from the trace."""
    ev = trace_skyline(triples)
    return [tuple(p) for p in ev[-1]["pieces"]] if ev else []


def trace_above(pieces, t):
    """Part c piece by piece: whether the piece reaches t, whether it was joined to the
    previous range, the ranges so far, and the peak so far with the pieces that hold it."""
    ev, ranges, peak, where = [], [], 0, []
    for j, (s, e, h) in enumerate(pieces):
        ok, joined = h >= t, False
        if ok:
            if ranges and ranges[-1][1] == s:
                ranges[-1][1] = e
                joined = True
            else:
                ranges.append([s, e])
        if h > peak:
            peak, where = h, [[s, e]]
        elif h == peak:
            if where and where[-1][1] == s:
                where[-1][1] = e
            else:
                where.append([s, e])
        ev.append({"j": j, "s": s, "e": e, "h": h, "ok": ok, "joined": joined,
                   "ranges": [list(r) for r in ranges], "peak": peak, "where": [list(w) for w in where]})
    return ev


# --- blocks ------------------------------------------------------------------------------

def num(v):
    """A number as the page writes it: the minus sign, not a hyphen."""
    return str(v).replace("-", "−")


def sval(v):
    """A value for a table cell: a negative one in an LTR span, or the RLM before it puts the
    minus after the digits."""
    return f'<span dir="ltr">{num(v)}</span>' if v < 0 else num(v)


def axis(T, lo, L, R, W, top, bottom):
    """Vertical grid lines with their tick labels under `bottom`, every 1, 2 or 5 units."""
    span = max(T - lo, 1)
    x = lambda t: L + (W - L - R) * (t - lo) / span
    step = 1 if span <= 12 else 2 if span <= 24 else 5
    s = ""
    for t in range(lo, T + 1, step):
        s += f'<line class="grid" x1="{x(t):g}" x2="{x(t):g}" y1="{top}" y2="{bottom}"/>'
        s += f'<text class="tick" x="{x(t):g}" y="{bottom + 14}" text-anchor="middle">{t}</text>'
    return s, x


def merge_svg(intervals, label):
    """Part a: the intervals sorted by start as bars, a row each, and under the axis one row
    of the merged result, every merged interval marked with its ends."""
    ivs = sorted(tuple(v) for v in intervals)
    lo, T = min(0, min(s for s, _ in ivs)), max(e for _, e in ivs)
    L, R, W, bar, gap, top = 64, 16, 640, 16, 8, 14
    y_axis = top + len(ivs) * (bar + gap) + 6
    y_res = y_axis + 34
    H = y_res + bar + 10
    s = f'<svg class="figure iv-fig" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
    g, x = axis(T, lo, L, R, W, top - 4, y_axis)
    s += g
    for i, (a, b) in enumerate(ivs):
        y = top + i * (bar + gap)
        s += (f'<text class="iv-name" x="{L - 8}" y="{y + bar - 3}" text-anchor="end">{i + 1}</text>'
              f'<rect class="iv-bar" x="{x(a):g}" y="{y}" width="{x(b) - x(a):g}" height="{bar}" rx="3"><title>[{a}, {b}]</title></rect>')
    s += f'<line class="axis" x1="{L}" x2="{W - R}" y1="{y_axis}" y2="{y_axis}"/>'
    s += f'<text class="iv-name" x="{L - 8}" y="{y_res + bar - 3}" text-anchor="end">merged</text>'
    for a, b in brute_merge(ivs):
        s += f'<rect class="iv-merged" x="{x(a):g}" y="{y_res}" width="{x(b) - x(a):g}" height="{bar}" rx="3"><title>merged: [{a}, {b}]</title></rect>'
    return s + "</svg>"


def legend_a():
    return ('<span class="viz-legend"><span><i class="iv-key-bar"></i>קטע מהקלט, ממוין לפי ההתחלה</span>'
            '<span><i class="iv-key-merged"></i>קטע ממוזג בפלט</span></span>')


def table_merge(intervals):
    out = ["| הקטע (ממוין) | הסוף של הקטע הממוזג האחרון | ההחלטה | הפלט אחרי הצעד |", "|:-:|:-:|:-:|:-:|"]
    for r in trace_merge(intervals):
        s, e = r["s"], r["e"]
        pe = "אין עדיין" if r["prev_end"] is None else f"{RLM}{num(r['prev_end'])}"
        if r["kind"] == "new":
            why = "אין קטע פתוח" if r["prev_end"] is None else f"{RLM}<span dir=\"ltr\">{num(s)} &gt; {num(r['prev_end'])}</span>, קטע חדש"
        elif r["kind"] == "extend":
            why = f"{RLM}<span dir=\"ltr\">{num(s)} ≤ {num(r['prev_end'])}</span>, הסוף גדל ל-{num(e)}"
        else:
            why = f"{RLM}<span dir=\"ltr\">{num(s)} ≤ {num(r['prev_end'])}</span>, כולו בפנים"
        after = RLM + '<span dir="ltr">' + " ".join(f"[{num(a)}, {num(b)}]" for a, b in r["after"]) + "</span>"
        out.append(f"| {RLM}<span dir=\"ltr\">[{num(s)}, {num(e)}]</span> | {pe} | {why} | {after} |")
    return "\n".join(out)


def stacks(triples):
    """For every gap between consecutive event positions: (start, end, [indices of the
    intervals covering it, in input order])."""
    pos = sorted({p for s, e, _ in triples for p in (s, e)})
    return [(a, b, [i for i, (s, e, _) in enumerate(triples) if s <= a and b <= e]) for a, b in zip(pos, pos[1:])]


def skyline_svg(triples, label, upto=None, threshold=None, peak_mark=False):
    """Part b: the intervals as bars with their heights, a row each, and under the axis the
    total height as stacked blocks (one colour per interval) with the skyline line over
    them. `upto` draws the stacks only up to that position (the explorer's steps)."""
    lo, T = min(0, min(s for s, _, _ in triples)), max(e for _, e, _ in triples)
    L, R, W, bar, gap, top = 64, 44, 640, 16, 8, 14
    n = len(triples)
    y_axis = top + n * (bar + gap) + 6
    peak = max(heights(triples).values(), default=0)
    unit = max(10, min(22, 120 // max(peak, 1)))
    ch, cy0 = unit * max(peak, 1), y_axis + 30
    H = cy0 + ch + 10
    s = f'<svg class="figure iv-fig" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
    g, x = axis(T, lo, L, R, W, top - 4, y_axis)
    s += g
    yc = lambda c: cy0 + ch - ch * c / max(peak, 1)
    for i, (a, b, h) in enumerate(triples):
        y = top + i * (bar + gap)
        s += (f'<text class="iv-name" x="{L - 8}" y="{y + bar - 3}" text-anchor="end">{i + 1}</text>'
              f'<rect class="iv-bar iv-c{i % 4}" x="{x(a):g}" y="{y}" width="{x(b) - x(a):g}" height="{bar}" rx="3"><title>[{a}, {b}) height {h}</title></rect>'
              f'<text class="iv-h" x="{x(b) + 6:g}" y="{y + bar - 3}">h = {h}</text>')
    s += f'<line class="axis" x1="{L}" x2="{W - R}" y1="{y_axis}" y2="{y_axis}"/>'
    tick = 1 if peak <= 8 else 2 if peak <= 16 else 5
    for c in range(0, peak + 1, tick):
        s += f'<text class="tick" x="{L - 8}" y="{yc(c) + 4:g}" text-anchor="end">{c}</text>'
    pts = [f"M{x(lo):g},{yc(0):g}"]
    for a, b, idx in stacks(triples):
        if upto is not None and a >= upto:
            break
        level = 0
        for i in idx:
            h = triples[i][2]
            s += (f'<rect class="iv-blk iv-c{i % 4}" x="{x(a):g}" y="{yc(level + h):g}" width="{x(b) - x(a):g}" height="{yc(level) - yc(level + h):g}">'
                  f'<title>[{a}, {b}): interval {i + 1} adds {h}, total {sum(triples[j][2] for j in idx)}</title></rect>')
            level += h
        pts.append(f"H{x(a):g} V{yc(level):g} H{x(b):g}")
    pts.append(f"V{yc(0):g}")
    s += f'<path class="iv-line" d="{" ".join(pts)}"/>'
    if threshold is not None:
        s += f'<line class="iv-thr" x1="{L}" x2="{W - R}" y1="{yc(threshold):g}" y2="{yc(threshold):g}"/><text class="legend" x="{W - R + 4}" y="{yc(threshold) + 4:g}">T = {threshold}</text>'
    if peak_mark:
        s += f'<line class="iv-peak" x1="{L}" x2="{W - R}" y1="{yc(peak):g}" y2="{yc(peak):g}"/><text class="legend" x="{W - R + 4}" y="{yc(peak) + 4:g}">max</text>'
    s += f'<text class="iv-name" x="{L - 8}" y="{cy0 - 8}" text-anchor="end">total</text>'
    return s + "</svg>"


def legend_b():
    return ('<span class="viz-legend"><span><i class="iv-key-blk"></i>הגובה של קטע אחד, בצבע שלו</span>'
            '<span><i class="iv-key-line"></i>הגובה הכולל, סכום הבלוקים</span></span>')


def legend_c():
    return ('<span class="viz-legend"><span><i class="iv-key-line"></i>הגובה הכולל</span>'
            '<span><i class="iv-key-thr"></i>הסף T</span><span><i class="iv-key-peak"></i>השיא</span></span>')


def table_skyline(triples):
    out = ["| המיקום | האירועים | הסכום לפני | הסכום אחרי | החתיכה שנפלטת |", "|:-:|:-:|:-:|:-:|:-:|"]
    for r in trace_skyline(triples):
        evs = ", ".join(f"<span dir=\"ltr\">{'+' if m['d'] > 0 else '−'}{abs(m['d'])}</span> (קטע {m['i'] + 1})" for m in r["events"])
        if r["piece"] is None:
            piece = "אין" if r["prev"] is None else "רווח, הסכום 0"
        else:
            a, b, t = r["piece"]
            piece = f"{RLM}<span dir=\"ltr\">[{num(a)}, {num(b)})</span> בגובה **{num(t)}**" + (" (מצטרפת לקודמת)" if r["joined"] else "")
        out.append(f"| {RLM}{num(r['p'])} | {RLM}{evs} | {RLM}{sval(r['before'])} | {RLM}{sval(r['after'])} | {piece} |")
    return "\n".join(out)


def table_above(triples, t):
    pieces = skyline_ref(triples)
    out = [f"| החתיכה | הגובה | לפחות {t}? | הטווחים עד עכשיו | השיא עד עכשיו |", "|:-:|:-:|:-:|:-:|:-:|"]
    for r in trace_above(pieces, t):
        ok = ("כן, מצטרפת לטווח הקודם" if r["joined"] else "כן, טווח חדש") if r["ok"] else "לא"
        rng = (RLM + '<span dir="ltr">' + " ".join(f"[{num(a)}, {num(b)})" for a, b in r["ranges"]) + "</span>") if r["ranges"] else "אין"
        where = " ".join(f"[{num(a)}, {num(b)})" for a, b in r["where"])
        out.append(f"| {RLM}<span dir=\"ltr\">[{num(r['s'])}, {num(r['e'])})</span> | {RLM}{num(r['h'])} | {ok} | {rng} | **{RLM}{num(r['peak'])}** ב-<span dir=\"ltr\">{where}</span> |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [merge_svg(IVS, "ארבעה קטעים סגורים : [1, 3], [2, 6], [8, 10] ו-[15, 18], ומתחתם התוצאה הממוזגת [1, 6], [8, 10], [15, 18]"),
            legend_a(), table_merge(IVS),
            skyline_svg(TRIPLES, "שני קטעים, [1, 7) בגובה 7 ו-[2, 6) בגובה 4, ומתחתם הגובה הכולל : 7 ב-[1, 2), 11 ב-[2, 6) ו-7 ב-[6, 7)"),
            legend_b(), table_skyline(TRIPLES),
            skyline_svg(TRIPLES_C, "ארבעה קטעים עם גבהים, הגובה הכולל שלהם, הסף T = 4 והשיא 6 ב-[2, 3)", threshold=T_C, peak_mark=True),
            legend_c(), table_above(TRIPLES_C, T_C)]


if __name__ == "__main__":
    print(brute_merge(IVS), [r["after"] for r in trace_merge(IVS)][-1])
    print(brute_skyline(TRIPLES), skyline_ref(TRIPLES))
    print(brute_skyline(TRIPLES_C), brute_above(TRIPLES_C, T_C), trace_above(skyline_ref(TRIPLES_C), T_C)[-1])
    print("\n\n".join(blocks()))
