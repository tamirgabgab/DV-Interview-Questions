#!/usr/bin/env python3
"""Figures and tables of question 0017 (find the duplicate number).

    python tools/figures/q0017.py > /tmp/q0017.html

Prints, in page order: the example array; the graph i -> nums[i] of the example (the rho
shape); the binary-search table; the step-through of Floyd's two phases. Paste them into
the page; tests/0017 checks that the page copies match.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

# n = 9: ten numbers between 1 and 9. From index 0: tail 0 -> 3 -> 6, then the cycle
# 1 -> 9 -> 4 -> 7 -> 1. The value 1 sits at indices 6 and 7. 2 -> 5 -> 8 is a second
# cycle that the walk from 0 never reaches.
NUMS = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4]
DUP = 1

R = 17
POS = {0: (40, 90), 3: (120, 90), 6: (200, 90)}
for i, node in enumerate([1, 9, 4, 7]):              # the cycle, 1 on its left
    a = math.pi - i * math.pi / 2
    POS[node] = (350 + 70 * math.cos(a), 90 - 70 * math.sin(a))
for i, node in enumerate([2, 5, 8]):                 # the unreachable cycle, bottom left
    a = math.pi / 2 + i * 2 * math.pi / 3
    POS[node] = (110 + 40 * math.cos(a), 230 - 40 * math.sin(a))


def array_table(nums=NUMS):
    """The example as a row of cells: small number = index, big number = value."""
    cells = "".join(f'<span{" class=\"hl\"" if v == DUP else ""}><small>{i}</small><b>{v}</b></span>'
                    for i, v in enumerate(nums))
    return f'<div class="box-grid bg-10" dir="ltr">{cells}</div>'


def walk(nums, start=0, steps=12):
    x, out = start, [start]
    for _ in range(steps):
        x = nums[x]
        out.append(x)
    return out


def edge(i, j, cls, uid):
    (x0, y0), (x1, y1) = POS[i], POS[j]
    d = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    a = (x0 + ux * (R + 2), y0 + uy * (R + 2))
    b = (x1 - ux * (R + 5), y1 - uy * (R + 5))
    color = cls.split("-")[0]
    return (f'<line class="{cls}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            f'stroke-width="2.2" marker-end="url(#{uid}-{color})"><title>nums[{i}] = {j}</title></line>')


def rho_svg(uid, slow=None, fast=None, mark_entry=False, faded_other=True, hot=()):
    """The graph i -> nums[i]. `slow` / `fast` get a ring; `hot` edges are drawn orange."""
    heads = "".join(
        f'<marker id="{uid}-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path class="{c}-fill" d="M0,0 L10,5 L0,10 z"/></marker>' for c in ("ink", "s2"))
    p = [f'<svg class="figure" viewBox="0 0 450 290" style="max-width:28rem" role="img" '
         f'aria-label="הגרף שבו כל אינדקס מצביע על הערך שבו: זנב, מעגל, ומעגל נפרד"><defs>{heads}</defs>']
    other = {2, 5, 8}
    for i, j in enumerate(NUMS):
        cls = "s2-line" if (i, j) in hot else "ink-line"
        line = edge(i, j, cls, uid)
        p.append(f'<g class="st-faded">{line}</g>' if faded_other and i in other else line)
    for node, (x, y) in POS.items():
        cls = "st-ok" if mark_entry and node == DUP else "st-cell"
        g = ' class="st-faded"' if faded_other and node in other else ""
        p.append(f'<g{g}><circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>'
                 f'<text class="st-text" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{node}</text></g>')
    if slow is not None:
        x, y = POS[slow]
        p.append(f'<circle class="fl-slow" cx="{x:.1f}" cy="{y:.1f}" r="{R + 5}"/>')
    if fast is not None:
        x, y = POS[fast]
        p.append(f'<circle class="fl-fast" cx="{x:.1f}" cy="{y:.1f}" r="{R + 10}"/>')
    p.append("</svg>")
    return "".join(p)


def floyd_trace(nums=NUMS):
    """Frames of the page's algorithm: (phase, step, slow, fast)."""
    frames = [(1, 0, 0, 0)]
    slow = fast = 0
    step = 0
    while True:
        slow, fast, step = nums[slow], nums[nums[fast]], step + 1
        frames.append((1, step, slow, fast))
        if slow == fast:
            break
    meet = slow
    slow, step = 0, 0
    frames.append((2, 0, slow, fast))
    while slow != fast:
        slow, fast, step = nums[slow], nums[fast], step + 1
        frames.append((2, step, slow, fast))
    return frames, meet


def floyd_stepper():
    frames, meet = floyd_trace()
    out = []
    for n, (phase, step, slow, fast) in enumerate(frames):
        uid = f"q17s{n}"
        if phase == 1 and step == 0:
            text = "שלב 1: הצב והארנב מתחילים באינדקס 0, שאף ערך לא מצביע עליו."
        elif phase == 1 and slow != fast:
            text = f"שלב 1, איטרציה {step}: הצב מתקדם צעד אחד ל-{slow}, והארנב שני צעדים ל-{fast}."
        elif phase == 1:
            text = (f"שלב 1, איטרציה {step}: שניהם ב-{slow}. נפגשו בתוך המעגל, ומספר האיטרציות {step} "
                    "הוא כפולה של אורך המעגל.")
        elif step == 0:
            text = f"שלב 2: מחזירים את הצב ל-0. הארנב נשאר בנקודת המפגש {meet}, ומעכשיו שניהם צועדים צעד אחד."
        elif slow != fast:
            text = f"שלב 2, איטרציה {step}: הצב ב-{slow}, הארנב ב-{fast}."
        else:
            text = (f"שלב 2, איטרציה {step}: שניהם ב-{slow}, הכניסה למעגל. שני חצים נכנסים אליה, מאינדקס 6 "
                    f"ומאינדקס 7, ולכן {slow} הוא הערך הכפול.")
        entry = phase == 2 and slow == fast
        hot = {(6, DUP), (7, DUP)} if entry else set()
        out.append((rho_svg(uid, slow, fast, mark_entry=entry, hot=hot), text))
    return stepper(out, "האלגוריתם של Floyd על הדוגמה: שלב המפגש ושלב הכניסה למעגל")


def legend():
    return ('<span class="viz-legend"><span><i class="fl-slow"></i>הצב: צעד אחד בכל פעם</span>'
            '<span><i class="fl-fast"></i>הארנב: שני צעדים בכל פעם</span>'
            '<span><i class="s3"></i>הכניסה למעגל, הערך הכפול</span></span>')


def binary_rows(nums=NUMS):
    rows = []
    lo, hi = 1, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(v <= mid for v in nums)
        rows.append((lo, hi, mid, count))
        if count > mid:
            hi = mid
        else:
            lo = mid + 1
    return rows, lo


def binary_search_table(nums=NUMS):
    rows, found = binary_rows(nums)
    lines = ["| הטווח | ‏\\( mid \\) | כמה \\( \\le mid \\) | הכפול נמצא |", "|---|---|---|---|"]
    for lo, hi, mid, count in rows:
        if count > mid:
            dec = f"‏\\( {count} > {mid} \\): " + (f"הוא {lo}" if lo == mid else f"בין {lo} ל-{mid}")
        else:
            dec = f"‏\\( {count} \\le {mid} \\): " + (f"הוא {hi}" if mid + 1 == hi else f"בין {mid + 1} ל-{hi}")
        lines.append(f"| {lo} עד {hi} | {mid} | {count} | {dec} |")
    lines.append(f"| {found} עד {found} | | | **{found}** |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(array_table(), "\n")
    print(rho_svg("q17a", mark_entry=True, hot={(6, DUP), (7, DUP)}), "\n")
    print(binary_search_table(), "\n")
    print(legend(), "\n")
    print(floyd_stepper())
