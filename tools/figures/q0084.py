#!/usr/bin/env python3
"""Figures and tables of question 0084 (the longest increasing subsequence).

    python tools/figures/fill.py 84        # put the blocks on the page

Every number comes from the page's own code (its Python blocks, loaded with
load_python): part a's dp and prev arcs over the example, part b's tails after every element
and the parent arcs of the reconstruction, part c's (length, count) tables. The arrays are
drawn left to right (index 0 on the left), with Latin labels only.
"""

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extract_code import load_python  # noqa: E402

EXAMPLE = [10, 9, 2, 5, 3, 7, 101, 18]
COUNT_EXAMPLE = [1, 3, 5, 4, 7]
C, G, LW, PAD = 36, 6, 46, 8          # cell, gap, the label column, the right margin
CY = 52                               # the top of the array's cells (the arcs sit above them)


def page():
    return load_python(84)


def tails_trace(a):
    """[(i, x, k, append, the value replaced or None, tails after)] by the page's search rule."""
    tails, out = [], []
    for i, x in enumerate(a):
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
            out.append((i, x, lo, True, None, list(tails)))
        else:
            old, tails[lo] = tails[lo], x
            out.append((i, x, lo, False, old, list(tails)))
    return out


def parents(a):
    """parent[i] as the page's lis sets it, and the index the reconstruction starts at."""
    tails, tail_at, parent = [], [], [-1] * len(a)
    for i, x in enumerate(a):
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
            tail_at.append(i)
        else:
            tails[lo], tail_at[lo] = x, i
        parent[i] = tail_at[lo - 1] if lo else -1
    return parent, (tail_at[-1] if tail_at else -1)


def probes(a):
    """The comparisons of the binary search over the whole array."""
    tails, n = [], 0
    for x in a:
        lo, hi = 0, len(tails)
        while lo < hi:
            n += 1
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return n


def cx(i):
    return LW + i * (C + G) + C / 2


def arc(p, i, cls):
    h = min(30, 6 + 6 * (i - p))
    x1, x2 = cx(p), cx(i)
    return f'<path class="{cls}" d="M{x1:g},{CY - 2} Q{(x1 + x2) / 2:g},{CY - 2 - 2 * h} {x2:g},{CY - 2}"/>'


def array_row(a, lit=()):
    s = []
    for i, v in enumerate(a):
        x = LW + i * (C + G)
        s.append(f'<text class="lis-idx" x="{cx(i):g}" y="14" text-anchor="middle">{i}</text>')
        s.append(f'<rect class="{"fig-one" if i in lit else "st-cell"}" x="{x}" y="{CY}" width="{C}" height="{C}" rx="3"/>'
                 f'<text class="st-text" x="{cx(i):g}" y="{CY + C / 2 + 5:g}" text-anchor="middle">{v}</text>')
    s.append(f'<text class="lis-lab" x="{LW - 10}" y="{CY + C / 2 + 5:g}" text-anchor="end">a</text>')
    return s


def value_row(name, vals, y, lit=()):
    s = [f'<text class="lis-lab" x="{LW - 10}" y="{y + 20}" text-anchor="end">{name}</text>']
    for i, v in enumerate(vals):
        x = LW + i * (C + G)
        s.append(f'<rect class="lis-val{" is-lit" if i in lit else ""}" x="{x}" y="{y}" width="{C}" height="28" rx="3"/>'
                 f'<text class="lis-num" x="{cx(i):g}" y="{y + 19}" text-anchor="middle">{"–" if v == -1 else v}</text>')
    return s


def svg(width, height, label, body):
    return (f'<svg class="figure lis-fig" viewBox="0 0 {width:g} {height}" style="max-width:{width / 16:.1f}rem" role="img" '
            f'aria-label="{escape(label)}">' + "".join(body) + "</svg>")


def chain(prev, end):
    out = []
    while end >= 0:
        out.append(end)
        end = prev[end]
    return out[::-1]


def part_a(a=EXAMPLE):
    ns = page()
    best, dp, prev = ns["lis_dp"](a)
    seq = ns["lis_from_dp"](a, dp, prev)
    idx = chain(prev, dp.index(best))
    assert [a[i] for i in idx] == seq
    n = len(a)
    body = []
    for i, p in enumerate(prev):
        if p >= 0 and not (i in idx and p in idx):
            body.append(arc(p, i, "lis-link"))
    for p, i in zip(idx, idx[1:]):
        body.append(arc(p, i, "lis-link is-chain"))
    body += array_row(a, idx)
    body += value_row("dp", dp, 100, idx)
    W = LW + n * (C + G) - G + PAD
    label = (f"סעיף א : המערך {' '.join(map(str, a))}. מתחת לכל איבר dp, האורך של תת-הסדרה העולה הארוכה ביותר שנגמרת בו : "
             f"{' '.join(map(str, dp))}. קשת מכל איבר לאיבר prev שלפניו. האורך {best}, והסדרה {' '.join(map(str, seq))} מודגשת")
    return svg(W, 136, label, body)


def legend_a():
    return ('<span class="viz-legend"><span><i class="fc-key-sorted"></i>תת-סדרה עולה ארוכה ביותר</span>'
            '<span><i class="lis-key-chain"></i>הקשת מ-<code>prev[i]</code> ל-<code>i</code> שלה</span>'
            '<span><i class="lis-key-link"></i>קשת <code>prev</code> של איבר אחר</span></span>')


def part_b(a=EXAMPLE):
    trace = tails_trace(a)
    L = max(len(t[5]) for t in trace)
    XL = 104                                # the row labels, left of the cells
    RH = 40
    xs = lambda k: XL + k * (C + G)
    W = XL + L * (C + G) - G + 136
    body = []
    for k in range(L):
        body.append(f'<text class="lis-idx" x="{xs(k) + C / 2:g}" y="14" text-anchor="middle">{k}</text>')
    body.append(f'<text class="lis-lab" x="{XL - 10}" y="14" text-anchor="end">k</text>')
    for r, (i, x, k, app, old, tails) in enumerate(trace):
        y = 24 + r * RH
        body.append(f'<text class="lis-lab" x="{XL - 10}" y="{y + 23}" text-anchor="end">x = {x}</text>')
        for j, v in enumerate(tails):
            cls = "lis-cell" + ((" is-new" if app else " is-rep") if j == k else "")
            body.append(f'<rect class="{cls}" x="{xs(j)}" y="{y}" width="{C}" height="32" rx="3"/>'
                        f'<text class="lis-num" x="{xs(j) + C / 2:g}" y="{y + 21}" text-anchor="middle">{v}</text>')
        note = f"k = {k}, append" if app else f"k = {k}, {old} → {x}"
        body.append(f'<text class="lis-side" x="{xs(L) + 4}" y="{y + 21}">{escape(note)}</text>')
    H = 24 + len(trace) * RH - 4
    rows = "; ".join(f"x = {x} : {'מאריך' if app else f'מחליף את {old}'} במקום {k}, tails = {' '.join(map(str, t))}"
                     for i, x, k, app, old, t in trace)
    label = f"סעיף ב : מערך tails אחרי כל איבר של {' '.join(map(str, a))}. {rows}"
    return svg(W, H, label, body)


def legend_b():
    return ('<span class="viz-legend"><span><i class="lis-key-new"></i>\\( x \\) מאריך את <code>tails</code></span>'
            '<span><i class="fc-key-chg"></i>\\( x \\) מחליף ערך גדול ממנו או שווה לו</span></span>')


def part_b_chain(a=EXAMPLE):
    parent, end = parents(a)
    seq = page()["lis"](a)
    idx = chain(parent, end)
    assert [a[i] for i in idx] == seq
    n = len(a)
    body = []
    for i, p in enumerate(parent):
        if p >= 0 and not (i in idx and p in idx):
            body.append(arc(p, i, "lis-link"))
    for p, i in zip(idx, idx[1:]):
        body.append(arc(p, i, "lis-link is-chain"))
    body += array_row(a, idx)
    body += value_row("parent", parent, 100, idx)
    W = LW + 18 + n * (C + G) - G + PAD
    body = [f'<g transform="translate(18 0)">'] + body + ["</g>"]
    label = (f"סעיף ב, השחזור : parent של כל איבר, {' '.join('–' if p < 0 else str(p) for p in parent)}. "
             f"מהאיבר האחרון שנכנס לסוף tails, האינדקס {end}, אחורה לפי parent : {' '.join(map(str, seq))}")
    return svg(W, 136, label, body)


def legend_b_chain():
    return ('<span class="viz-legend"><span><i class="fc-key-sorted"></i>הסדרה שהשחזור מחזיר</span>'
            '<span><i class="lis-key-chain"></i>הקשת מ-<code>parent[i]</code> ל-<code>i</code> שלה</span>'
            '<span><i class="lis-key-link"></i>קשת <code>parent</code> של איבר אחר</span><span>הסימן – הוא \\( -1 \\)</span></span>')


def pairs(a):
    """length and count per index, as the page's count_lis builds them."""
    n = len(a)
    length, count = [1] * n, [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i]:
                if length[j] + 1 > length[i]:
                    length[i], count[i] = length[j] + 1, count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    return length, count


def count_table(a, what):
    length, count = pairs(a)
    best = max(length)
    total = page()["count_lis"](a)
    assert total == sum(c for n, c in zip(length, count) if n == best)
    lit = {i for i in range(len(a)) if length[i] == best}

    def row(name, vals, cls=""):
        cells = "".join(f'<td class="gs-b{" is-one" if i in lit else ""}">{v}</td>' for i, v in enumerate(vals))
        return f'<tr{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><th>{name}</th>{cells}</tr>'

    label = (f"{what} : לכל אינדקס האורך length ומספר הסדרות count. האורך המקסימלי {best}, "
             f"והסכום של count בעמודות שלו הוא {total}")
    return (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
            f'<table class="gs-bits lis-tab" dir="ltr" aria-label="{escape(label)}"><tbody>'
            + row("i", range(len(a)), "lis-ix") + row("a[i]", a) + row("length", length) + row("count", count)
            + "</tbody></table></div>")


def legend_c(a):
    length, count = pairs(a)
    best = max(length)
    total = sum(c for n, c in zip(length, count) if n == best)
    return (f'<span class="viz-legend"><span><i class="gs-key-one"></i>אורך מקסימלי, {best} : הסכום של <code>count</code> בעמודות '
            f'האלה הוא {total}</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [
        part_a() + "\n\n" + legend_a(),
        part_b() + "\n\n" + legend_b(),
        part_b_chain() + "\n\n" + legend_b_chain(),
        count_table(COUNT_EXAMPLE, "סעיף ג, המערך 1 3 5 4 7") + "\n\n" + legend_c(COUNT_EXAMPLE),
        count_table(EXAMPLE, "סעיף ג, הדוגמה של סעיף א") + "\n\n" + legend_c(EXAMPLE),
    ]


if __name__ == "__main__":
    print(tails_trace(EXAMPLE), parents(EXAMPLE), probes(EXAMPLE))
    print("\n\n".join(blocks()))
