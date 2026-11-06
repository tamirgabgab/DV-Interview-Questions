#!/usr/bin/env python3
"""Figures and tables of question 0090: pancake sorting.

    python tools/figures/fill.py 90        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the tests compare the
two): a stack is a tuple, its first item the top pancake; flip(s, k) turns the top k
over; a burnt pancake is a signed size, positive when its burnt side faces down. The
breadth-first searches start at the sorted stack: a flip is its own inverse, so the fewest
flips from the sorted stack to s are the fewest flips that sort s. The explorer box
(docs/javascripts/explorer/pancake.js) uses the same model and the same order of flips.
"""

import html
import sys
from collections import deque
from itertools import permutations, product
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402
from stepper import stepper  # noqa: E402

NB = "\u00a0"
RLM = "‏"

EXAMPLE = (3, 1, 5, 4, 2)          # the page's stack, top first
BURNT = (-1, -2, -3)               # sorted, every burnt side up
PLAIN_MAX = 8                       # the exact worst case, plain stacks
BURNT_MAX = 7                       # and burnt ones (2^7 * 7! = 645,120 stacks)


# --- the model -----------------------------------------------------------------------------------

def flip(s, k):
    """Turn the top k pancakes over (the order of the top k reverses)."""
    return tuple(s[:k][::-1]) + tuple(s[k:])


def burnt_flip(s, k):
    """The same, and every pancake turned over shows its other side."""
    return tuple(-x for x in s[:k][::-1]) + tuple(s[k:])


def simple(s, kinds=False):
    """The simple algorithm: for k = n, ..., 2, bring pancake k to the top (unless it is
    there or already in place) and flip it down to place k. Returns [(k, stack after)],
    with kinds=True [(k, stack after, "up" or "down", the pancake moved)]."""
    s, out = tuple(s), []
    for k in range(len(s), 1, -1):
        p = s.index(k)
        if p == k - 1:
            continue
        if p:
            s = flip(s, p + 1)
            out.append((p + 1, s, "up", k))
        s = flip(s, k)
        out.append((k, s, "down", k))
    return out if kinds else [(f, t) for f, t, *_ in out]


def burnt_simple(s):
    """The same with burnt sides: bring k to the top, turn it burnt side up if needed (a
    flip of one), flip it down. At most three flips for each k, one for the last."""
    s, out = tuple(s), []
    for k in range(len(s), 0, -1):
        p = [abs(x) for x in s].index(k)
        if p == k - 1 and s[p] > 0:
            continue
        if p:
            s = burnt_flip(s, p + 1)
            out.append((p + 1, s))
        if s[0] > 0:
            s = burnt_flip(s, 1)
            out.append((1, s))
        s = burnt_flip(s, k)
        out.append((k, s))
    return out


def distances(n, burnt=False):
    """The fewest flips that sort every stack of n (BFS from the sorted stack)."""
    start = tuple(range(1, n + 1))
    op, k0 = (burnt_flip, 1) if burnt else (flip, 2)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        d = dist[s] + 1
        for k in range(k0, n + 1):
            t = op(s, k)
            if t not in dist:
                dist[t] = d
                queue.append(t)
    return dist


def best_path(s, dist, burnt=False):
    """A shortest sorting: at each stack the smallest k whose flip is one closer."""
    op, k0 = (burnt_flip, 1) if burnt else (flip, 2)
    s, out = tuple(s), []
    while dist[s]:
        k = next(k for k in range(k0, len(s) + 1) if dist[op(s, k)] == dist[s] - 1)
        s = op(s, k)
        out.append((k, s))
    return out


def breakpoints(s):
    """Neighbours that are not consecutive sizes, the plate counted as n + 1 under the
    stack: a flip changes only the pair at its cut, so this is a lower bound."""
    t = tuple(s) + (len(s) + 1,)
    return sum(1 for a, b in zip(t, t[1:]) if abs(a - b) != 1)


def plain_table():
    rows = []
    for n in range(1, PLAIN_MAX + 1):
        d = distances(n)
        worst = max(d.values())
        hardest = sorted(p for p, v in d.items() if v == worst)
        rows.append({"n": n, "stacks": factorial(n), "worst": worst, "count": len(hardest), "hardest": hardest,
                     "simple": max(len(simple(p)) for p in permutations(range(1, n + 1)))})
    return rows


def burnt_table():
    rows = []
    for n in range(1, BURNT_MAX + 1):
        d = distances(n, burnt=True)
        worst = max(d.values())
        hardest = sorted(p for p, v in d.items() if v == worst)
        row = {"n": n, "stacks": len(d), "worst": worst, "count": len(hardest), "hardest": hardest,
               "neg": d[tuple(-x for x in range(1, n + 1))]}
        if n <= 6:   # the simple algorithm over every stack (7: 645,120 runs, left to the test of 6)
            row["simple"] = max(len(burnt_simple(tuple(sg * v for sg, v in zip(signs, p))))
                                for p in permutations(range(1, n + 1)) for signs in product((1, -1), repeat=n))
        rows.append(row)
    return rows


# --- drawings ------------------------------------------------------------------------------------

UNIT_H, GAP = 20, 4


def stack_svg(s, n=None, flip_k=0, done=0, aria="", burnt=False, x0=0, solo=True, width=150):
    """A stack, top first: a pancake k is a rounded slab as wide as its size, its number in
    the middle; burnt pancakes show their burnt side as a thick edge. flip_k > 0 frames
    the top flip_k (the flip that made this stack); done marks the bottom `done` pancakes
    that are in their final place."""
    n = n or len(s)
    h = len(s) * (UNIT_H + GAP) + 18
    parts = []
    cx = x0 + width / 2
    for i, v in enumerate(s):
        size = abs(v)
        w = 26 + (width - 34) * size / n
        y = 6 + i * (UNIT_H + GAP)
        cls = "pk-cake pk-done" if i >= len(s) - done else "pk-cake"
        parts.append(f'<rect class="{cls}" x="{cx - w / 2:.1f}" y="{y}" width="{w:.1f}" height="{UNIT_H}" rx="9"/>')
        if burnt:
            yb = y + UNIT_H - 4 if v > 0 else y
            parts.append(f'<rect class="pk-burnt" x="{cx - w / 2 + 5:.1f}" y="{yb}" width="{w - 10:.1f}" height="4" rx="2"/>')
        parts.append(f'<text class="pk-num" x="{cx:.1f}" y="{y + 15}" text-anchor="middle">{size}</text>')
    yp = 6 + len(s) * (UNIT_H + GAP) + 2
    parts.append(f'<line class="pk-plate" x1="{x0 + 4}" x2="{x0 + width - 4}" y1="{yp}" y2="{yp}"/>')
    if flip_k:
        yb = 6 + flip_k * (UNIT_H + GAP) - GAP / 2
        parts.append(f'<rect class="pk-flipbox" x="{x0 + 2}" y="2" width="{width - 4}" height="{yb - 2:.1f}" rx="6"/>')
    body = "".join(parts)
    if not solo:
        return body, h
    return (f'<svg class="figure pk-fig" viewBox="0 0 {width} {h}" style="max-width:{width / 16:.1f}rem" role="img" '
            f'aria-label="{html.escape(aria)}">{body}</svg>')


def code(s):
    """A stack as code; no-break spaces, so it never wraps in a right-to-left line."""
    return "<code>[" + f",{NB}".join(str(v) for v in s) + "]</code>"


def statement_svg():
    left, h = stack_svg(EXAMPLE, solo=False)
    after = flip(EXAMPLE, 3)
    right, _ = stack_svg(after, flip_k=3, x0=210, solo=False)
    arrow = ('<path class="pk-arrow" d="M156,40 Q183,18 206,40"/>'
             '<polygon class="pk-head" points="200,34 210,42 199,45"/>')
    aria = (f"הערימה {', '.join(map(str, EXAMPLE))} מלמעלה למטה, ואחרי הפיכה של 3 העליונים{NB}: "
            f"{', '.join(map(str, after))}")
    return (f'<svg class="figure pk-fig" viewBox="0 0 360 {h}" style="max-width:22.5rem" role="img" '
            f'aria-label="{html.escape(aria)}">{left}{arrow}{right}</svg>')


def legend(burnt=False):
    items = ['<span><i class="pk-key-cake"></i>פנקייק, רחב כמו הגודל שלו</span>',
             '<span><i class="pk-key-flip"></i>הפנקייקים שההפיכה הפכה</span>',
             '<span><i class="pk-key-done"></i>במקום הסופי</span>',
             '<span><i class="pk-key-plate"></i>הצלחת</span>']
    if burnt:
        items.insert(1, '<span><i class="pk-key-burnt"></i>הצד השרוף</span>')
    return '<span class="viz-legend">' + "".join(items) + "</span>"


def done_count(s):
    """How many pancakes at the bottom are in their final place (plain stacks)."""
    n, c = len(s), 0
    while c < n and abs(s[n - 1 - c]) == n - c and s[n - 1 - c] > 0:
        c += 1
    return c


def simple_stepper():
    steps = simple(EXAMPLE, kinds=True)
    frames = [(stack_svg(EXAMPLE, done=done_count(EXAMPLE), aria="התחלה"),
               f"התחלה{NB}: הערימה {code(EXAMPLE)}, מלמעלה למטה.")]
    for i, (k, s, kind, moved) in enumerate(steps, 1):
        if kind == "down":
            why = f"והפנקייק {moved} יורד למקום הסופי שלו"
        else:
            why = f"כדי להעלות את {moved} לראש הערימה"
        last = f" <strong>ממוין אחרי {len(steps)} הפיכות.</strong>" if i == len(steps) else ""
        frames.append((stack_svg(s, flip_k=k, done=done_count(s), aria=f"הפיכה {i}"),
                       f"הפיכה {i}{NB}: הופכים את {k} העליונים, {why}. עכשיו {code(s)}.{last}"))
    return stepper(frames, aria="האלגוריתם הפשוט על הערימה של השאלה, הפיכה אחרי הפיכה")


def best_stepper():
    d = distances(len(EXAMPLE))
    steps = best_path(EXAMPLE, d)
    frames = [(stack_svg(EXAMPLE, done=done_count(EXAMPLE), aria="התחלה"),
               f"התחלה{NB}: {code(EXAMPLE)}. ‏BFS אומר שמכאן צריך {d[EXAMPLE]} הפיכות.")]
    for i, (k, s) in enumerate(steps, 1):
        left = d[s]
        tail = f"נשארו {left} הפיכות." if left > 1 else ("נשארה הפיכה אחת." if left == 1 else "<strong>ממוין, בחמש הפיכות במקום שבע.</strong>")
        frames.append((stack_svg(s, flip_k=k, done=done_count(s), aria=f"הפיכה {i}"),
                       f"הפיכה {i}{NB}: הופכים את {k} העליונים. עכשיו {code(s)}. {tail}"))
    return stepper(frames, aria="הדרך הקצרה ביותר לאותה ערימה, חמש הפיכות")


def burnt_stepper():
    d = distances(len(BURNT), burnt=True)
    steps = best_path(BURNT, d, burnt=True)
    frames = [(stack_svg(BURNT, burnt=True, aria="התחלה"),
               f"התחלה{NB}: הערימה ממוינת, אבל כל הצדדים השרופים למעלה. ברשימה {code(BURNT)}{NB}: "
               f"מספר שלילי הוא פנקייק שהצד השרוף שלו למעלה.")]
    for i, (k, s) in enumerate(steps, 1):
        what = "הופכים רק את העליון" if k == 1 else f"הופכים את {k} העליונים"
        last = f" <strong>ממוין, וכל הצדדים השרופים למטה, אחרי {len(steps)} הפיכות.</strong>" if i == len(steps) else ""
        frames.append((stack_svg(s, flip_k=k, burnt=True, done=done_count(s), aria=f"הפיכה {i}"),
                       f"הפיכה {i}{NB}: {what}. עכשיו {code(s)}.{last}"))
    return stepper(frames, aria="ערימה ממוינת עם כל הצדדים השרופים למעלה, והדרך הקצרה ביותר שלה")


def plain_table_md(rows):
    lines = ["| ‏n | ערימות | המקרה הגרוע | ערימות קשות | האלגוריתם הפשוט | ‏\\( 2n - 3 \\) |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        n = r["n"]
        bound = str(2 * n - 3) if n >= 2 else "‏–"
        lines.append(f"| {n} | {r['stacks']:,} | {r['worst']} | {r['count']:,} | {r['simple']} | {bound} |")
    return "\n".join(lines)


def burnt_table_md(rows):
    lines = ["| ‏n | המקרה הגרוע | ערימות קשות | ממוינת והפוכה | האלגוריתם הפשוט | ‏\\( 3n - 2 \\) |",
             "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        n = r["n"]
        lines.append(f"| {n} | {r['worst']} | {r['count']} | {r['neg']} | "
                     f"{r.get('simple', '‏–')} | {3 * n - 2} |")
    return "\n".join(lines)


def worst_chart(rows):
    ns = [r["n"] for r in rows if r["n"] >= 2]
    c = Chart(f"המקרה הגרוע לכל n מ-2 עד 8{NB}: הנקודות הן הכי מעט הפיכות לערימה הקשה ביותר, והקו הוא 2n − 3 "
              "של האלגוריתם הפשוט", w=520, h=230, x0=42, top=14, base=190, slots=len(ns), y_max=14)
    c.grid_y([0, 2, 4, 6, 8, 10, 12, 14])
    c.x_ticks(range(1, len(ns) + 1), labels=[str(n) for n in ns])
    c.path([(i + 1, 2 * n - 3) for i, n in enumerate(ns)], "s2-line", width=2.5)
    for i, n in enumerate(ns):
        c.dot(i + 1, 2 * n - 3, "s2", r=3.5, title=f"n = {n}{NB}: 2n − 3 = {2 * n - 3}")
        w = next(r["worst"] for r in rows if r["n"] == n)
        c.dot(i + 1, w, "s1", r=5, title=f"n = {n}{NB}: {w} הפיכות", label=str(w), dy=14)
    c.add(f'<text class="tick" x="{c.x1}" y="{c.base + 34}" text-anchor="end">n</text>')
    return c.svg()


def chart_legend():
    return ('<span class="viz-legend"><span><i class="pk-key-best"></i>המקרה הגרוע האמיתי (BFS)</span>'
            '<span><i class="pk-key-bound"></i>החסם של האלגוריתם הפשוט, <span dir="ltr">2n − 3</span></span></span>')


def blocks():
    """The generated blocks, in page order."""
    plain, burnt = plain_table(), burnt_table()
    return [
        statement_svg(),
        legend(),
        simple_stepper(),
        plain_table_md(plain),
        worst_chart(plain),
        chart_legend(),
        best_stepper(),
        burnt_stepper(),
        legend(burnt=True),
        burnt_table_md(burnt),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
