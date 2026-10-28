#!/usr/bin/env python3
"""Figures and tables of question 0062 (how many tags a list of transactions needs: the
most open at once, with one pool and with a pool for reads and one for writes).

    python tools/figures/fill.py 62        # put the blocks on the page

The reference here is independent of the page code: brute_tags() counts the open
transactions at every send time, sweep() replays the sorted events with the counters (the
rows of the table and what the tagpool explorer draws). blocks() returns, in page order:
the timeline of part a with its counter, its legend, the table of its events, the timeline
of part b with reads and writes, and its legend.
"""

RLM = "‏"
TXNS = [(0, 30), (5, 10), (15, 20)]
# part b: reads and writes whose peaks are apart (a shared pool saves two tags)
TXNS_B = [(0, 10, "R"), (2, 12, "R"), (20, 30, "W"), (22, 32, "W")]
# and whose peaks coincide (no saving)
TXNS_C = [(0, 10, "R"), (2, 12, "R"), (3, 13, "W"), (5, 15, "W")]


def brute_tags(txns):
    """The most transactions open at once: a transaction is open from its send up to, not
    including, its response, so the count is checked at every send time."""
    return max((sum(1 for s, e, *_ in txns if s <= t < e) for t, *_ in txns), default=0)


def sweep(txns):
    """The sorted events of the transactions (a response before a send at the same time)
    with the counters after each: the open reads, the open writes, the open total and the
    maxima so far. A transaction without a kind counts as a read; i is its place in the list."""
    events = []
    for i, (s, e, *kind) in enumerate(txns):
        kind = kind[0] if kind else "R"
        events.append((s, 1, kind, i))
        events.append((e, -1, kind, i))
    events.sort()                     # the time, then the responses, then the reads, then the list order
    rows, open_, best = [], {"R": 0, "W": 0}, {"R": 0, "W": 0, "all": 0}
    for t, d, kind, i in events:
        open_[kind] += d
        best[kind] = max(best[kind], open_[kind])
        best["all"] = max(best["all"], open_["R"] + open_["W"])
        rows.append({"t": t, "d": d, "kind": kind, "i": i, "open": dict(open_), "total": open_["R"] + open_["W"], "best": dict(best)})
    return rows


def pools(txns):
    """(reads alone, writes alone, one shared pool)."""
    last = sweep(txns)[-1]["best"]
    return last["R"], last["W"], last["all"]


# --- blocks ------------------------------------------------------------------------------

def timeline_svg(txns, label, kinds=False):
    """The transactions as bars over time (a row each, top to bottom in list order), the
    time axis, and under them the number open at every moment as a step line with its
    maximum marked."""
    T = max(e for _, e, *_ in txns)
    L, R, W = 64, 16, 640
    bar, gap, top = 16, 8, 14
    x = lambda t: L + (W - L - R) * t / T
    rows = sweep(txns)
    peak = rows[-1]["best"]["all"]
    y_axis = top + len(txns) * (bar + gap) + 6
    ch, cy0 = 22 * max(peak, 1), y_axis + 42
    H = cy0 + ch + 30
    s = f'<svg class="figure tp-fig" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
    step = 5 if T <= 40 else 10
    for t in range(0, T + 1, step):
        s += f'<line class="grid" x1="{x(t):g}" x2="{x(t):g}" y1="{top - 4}" y2="{cy0 + ch}"/>'
        s += f'<text class="tick" x="{x(t):g}" y="{y_axis + 14}" text-anchor="middle">{t}</text>'
    for i, (a, e, *kind) in enumerate(txns):
        y = top + i * (bar + gap)
        cls = f" is-{kind[0].lower()}" if kinds and kind else ""
        name = f"{kind[0]}{i + 1}" if kinds and kind else f"T{i + 1}"
        s += (f'<text class="tp-name" x="{L - 8}" y="{y + bar - 3}" text-anchor="end">{name}</text>'
              f'<rect class="tp-bar{cls}" x="{x(a):g}" y="{y}" width="{x(e) - x(a):g}" height="{bar}" rx="3"><title>{name}: {a}–{e}</title></rect>')
    s += f'<line class="axis" x1="{L}" x2="{W - R}" y1="{y_axis}" y2="{y_axis}"/>'
    # the count as a step line: level 0 before the first event, then the total after each
    yc = lambda c: cy0 + ch - ch * c / max(peak, 1)
    pts, level = [f"M{L},{yc(0):g}"], 0
    for r in rows:
        pts.append(f"H{x(r['t']):g} V{yc(r['total']):g}")
        level = r["total"]
    pts.append(f"H{W - R}")
    for c in range(peak + 1):
        s += f'<text class="tick" x="{L - 8}" y="{yc(c) + 4:g}" text-anchor="end">{c}</text>'
    s += f'<line class="tp-max" x1="{L}" x2="{W - R}" y1="{yc(peak):g}" y2="{yc(peak):g}"/>'
    s += f'<path class="tp-count" d="{" ".join(pts)}"/>'
    s += f'<text class="legend" x="{W - R}" y="{yc(peak) - 7:g}" text-anchor="end">max = {peak}</text>'
    s += f'<text class="tp-name" x="{L - 8}" y="{cy0 - 10}" text-anchor="end">open</text>'
    return s + "</svg>"


def legend_a():
    return ('<span class="viz-legend"><span><i class="tp-key-bar"></i>טרנזקציה פתוחה, מהשליחה עד התשובה</span>'
            '<span><i class="tp-key-count"></i>כמה פתוחות בכל רגע</span><span><i class="tp-key-max"></i>המקסימום, מספר ה-tags</span></span>')


def legend_b():
    return ('<span class="viz-legend"><span><i class="tp-key-r"></i>קריאה</span><span><i class="tp-key-w"></i>כתיבה</span>'
            '<span><i class="tp-key-count"></i>כמה פתוחות יחד</span><span><i class="tp-key-max"></i>המקסימום של המאגר המשותף</span></span>')


def events_table(txns):
    rows = sweep(txns)
    out = ["| הזמן | האירוע | פתוחות אחריו | המקסימום עד עכשיו |", "|:-:|:-:|:-:|:-:|"]
    for r in rows:
        what = "שליחה, ‏+1" if r["d"] > 0 else "תשובה, ‏−1"
        out.append(f"| {RLM}{r['t']} | {what} | {RLM}{r['total']} | **{RLM}{r['best']['all']}** |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [timeline_svg(TXNS, "שלוש טרנזקציות : 0 עד 30, 5 עד 10 ו-15 עד 20, ומתחתן כמה פתוחות בכל רגע, לכל היותר 2"),
            legend_a(), events_table(TXNS),
            timeline_svg(TXNS_B, "שתי קריאות ב-0 עד 12 ושתי כתיבות ב-20 עד 32 : שני מאגרים צריכים 4 tags, מאגר משותף 2", kinds=True),
            legend_b()]


if __name__ == "__main__":
    print(brute_tags(TXNS), pools(TXNS), pools(TXNS_B), pools(TXNS_C))
    print("\n\n".join(blocks()))
