#!/usr/bin/env python3
"""Figures and tables of questions 0016 and 0018: the Josephus problem with the rule
"one stays, the next L - 1 leave", people numbered 0 .. N - 1.

    python tools/figures/q0016.py > /tmp/q0016.html

Prints the figures of 0016 (L = 2) in page order: the step-through circle for N = 20, the
round-by-round table for N = 20, the table of survivors for N = 1..16, the survivor chart
for N = 1..40, the relabelling figure after one elimination, the one-round figure for
N = 8, and the binary figure. tools/figures/q0018.py imports this module for L = 3 and
the general L. tests/0016 and tests/0018 check that the page copies match.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

HEB_ORD = {2: "שני", 3: "שני ושלישי"}


def run(n, L=2):
    """People 0..n-1 in a circle. Person 0 stays, the next L - 1 leave, the next stays, and
    so on around the circle until one is left. Returns the list of (stays, [leave, ...]) per
    step and the survivor."""
    circle = list(range(n))
    steps, i = [], 0
    while len(circle) > 1:
        stays, leave = circle[i], []
        for _ in range(min(L - 1, len(circle) - 1)):
            j = (i + 1) % len(circle)
            leave.append(circle.pop(j))
            if j < i:
                i -= 1                      # the element left of i is gone
        steps.append((stays, leave))
        i = (i + 1) % len(circle)
    return steps, circle[0]


def survivor(n, L=2):
    return run(n, L)[1]


def residue(n, L):
    """r(N) = 1 + ((N - 1) mod (L - 1)): the chain of N (its residue mod L - 1, as 1..L-1)."""
    return 1 + (n - 1) % (L - 1)


def zero_below(n, L):
    """M(N): the largest r L^m that does not exceed N, where r is the residue of N."""
    m = residue(n, L)
    while m * L <= n:
        m *= L
    return m


def formula(n, L=2):
    """The closed form F_L(N) = L (N - M(N)) / (L - 1)."""
    return L * (n - zero_below(n, L)) // (L - 1)


def rounds(n, L=2):
    """Group the steps into rounds: a new round starts when the count wraps past person 0,
    i.e. when the person who stays has a smaller number than the previous one."""
    steps, win = run(n, L)
    groups, prev = [], None
    for stays, leave in steps:
        if prev is None or stays <= prev:
            groups.append([])
        groups[-1].append((stays, leave))
        prev = stays
    return groups, win


# --- the circle ----------------------------------------------------------------------

def circle_frame(n, out, stays=None, leave=(), winner=None):
    """n people on a circle, person 0 at the top, numbered clockwise."""
    if n <= 12:
        w, R, r, small = 300, 105, 17, ""
    elif n <= 20:
        w, R, r, small = 300, 118, 15, ""
    else:
        w, R, r, small = 340, 140, 13, " st-sm"
    cx = cy = w // 2
    h = w - 20
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         f'aria-label="{n} אנשים במעגל">']
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" class="ink-line" stroke-width="1" '
             'stroke-dasharray="3 5" opacity="0.5"/>')
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        if i == winner:
            cls = "st-ok"
        elif i in leave:
            cls = "st-bad"
        elif i == stays:
            cls = "st-stack"
        elif i in out:
            cls = "st-done"
        else:
            cls = "st-cell"
        faded = ' class="st-faded"' if i in out and i not in leave else ""
        p.append(f'<g{faded}><circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
                 f'<text class="st-text{small}" x="{x:.1f}" y="{y + (4 if small else 5):.1f}" text-anchor="middle">{i}</text>')
        if i in out:
            d = r - 3
            p.append(f'<line class="pg-strike" x1="{x - d:.1f}" y1="{y + d:.1f}" x2="{x + d:.1f}" y2="{y - d:.1f}"/>')
        p.append("</g>")
    p.append(f'<text class="st-text" x="{cx}" y="{cy + 6}" text-anchor="middle">{n - len(out)}</text>')
    p.append("</svg>")
    return "".join(p)


def _people(nums):
    nums = list(map(str, nums))
    return nums[0] if len(nums) == 1 else " ו-".join([", ".join(nums[:-1]), nums[-1]])


def circle_stepper(n, L=2):
    steps, win = run(n, L)
    rule = "נשאר, והבא אחריו יוצא" if L == 2 else f"נשאר, ו-{L - 1} הבאים אחריו יוצאים"
    frames = [(circle_frame(n, set()),
               f"{n} אנשים במעגל. מתחילים מאדם 0: הוא {rule}. המספר במרכז הוא כמה אנשים נשארו.")]
    out = set()
    for s, (stays, leave) in enumerate(steps, 1):
        who = f"ואדם {leave[0]} יוצא" if len(leave) == 1 else f"ואנשים {_people(leave)} יוצאים"
        frames.append((circle_frame(n, out | set(leave), stays, leave),
                       f"צעד {s}: אדם {stays} נשאר, {who}."))
        out |= set(leave)
    frames.append((circle_frame(n, out, winner=win), f"נשאר אדם {win}. הוא השורד: \\( F_{L}({n}) = {win} \\)."))
    return stepper(frames, f"יוספוס עם {n} אנשים, כל {HEB_ORD.get(L, str(L))} יוצא")


def rounds_table(n, L=2):
    groups, win = rounds(n, L)
    lines = ["| סיבוב | יוצאים | נשארים, לפי סדר הספירה |", "|---|---|---|"]
    for g, group in enumerate(groups, 1):
        gone = [v for _, leave in group for v in leave]
        stayed = [s for s, _ in group if s not in gone]   # 0 may stay early in a round and leave at its end
        # order the remaining people from the one the count continues with
        nxt = groups[g][0][0] if g < len(groups) else win
        k = stayed.index(nxt)
        left = ", ".join(map(str, stayed[k:] + stayed[:k]))
        lines.append(f"| {g} | {', '.join(map(str, gone))} | {left} |")
    return "\n".join(lines)


# --- tables ------------------------------------------------------------------------------

def survivors_table(N=16):
    """L = 2: N, its binary form, N = 2^m + r and the survivor."""
    lines = ["| ‏\\( N \\) | בבינארי | ‏\\( 2^m + r \\) | ‏\\( F(N) \\) |", "|---|---|---|---|"]
    for n in range(1, N + 1):
        top = 1 << (n.bit_length() - 1)
        lines.append(f"| {n} | ‏`{n:b}` | ‏\\( {top} + {n - top} \\) | **{survivor(n)}** |")
    return "\n".join(lines)


def values_table(L, N, with_residue=False):
    """L >= 3: N, (its residue,) the zero point M below it, the formula and the simulation."""
    frac = f"\\tfrac{{{L}}}{{{L - 1}}}"
    head = ["‏\\( N \\)"] + (["‏\\( r \\)"] if with_residue else []) + ["‏\\( M \\)", f"‏\\( {frac}(N - M) \\)", "השורד"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for n in range(1, N + 1):
        M = zero_below(n, L)
        cells = [str(n)] + ([str(residue(n, L))] if with_residue else []) + \
                [str(M), f"‏\\( {frac} \\cdot {n - M} = {formula(n, L)} \\)", f"**{survivor(n, L)}**"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def zeros_table(Ls=(2, 3, 4, 5), limit=100):
    lines = ["| ‏\\( L \\) | ‏\\( r \\) | נקודות האפס עד 100 |", "|---|---|---|"]
    for L in Ls:
        rs = ", ".join(str(b) for b in range(1, L))
        zeros = sorted(b * L ** m for b in range(1, L) for m in range(8) if b * L ** m <= limit)
        lines.append(f"| {L} | {rs} | {', '.join(map(str, zeros))} |")
    return "\n".join(lines)




# --- charts ------------------------------------------------------------------------------

def chart(L=2, N=40, step=4):
    """The survivor as a function of N; one line per chain (residue mod L - 1), zero points
    as ink dots, and the dashed line F = N."""
    w, h, x0, top, base = 640, 290, 44, 14, 250
    sx = (w - x0 - 16) / N
    sy = (base - top) / N
    X = lambda n: x0 + (n - 0.5) * sx
    Y = lambda v: base - v * sy
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" role="img" '
         f'aria-label="השורד כפונקציה של מספר האנשים, מ-1 עד {N}, כש-{L - 1} יוצאים אחרי כל אחד שנשאר">']
    for v in range(0, N + 1, 2 * step):
        p.append(f'<line class="grid" x1="{x0}" x2="{w - 16}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                 f'<text class="tick" x="{x0 - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    p.append(f'<line class="ink-line" x1="{X(0.5):.1f}" y1="{Y(0):.1f}" x2="{X(N + 0.5):.1f}" y2="{Y(N):.1f}" '
             'stroke-width="1.2" stroke-dasharray="5 4"/>')
    vals = {n: survivor(n, L) for n in range(1, N + 1)}
    for n in range(L, N + 1):                 # segments along a chain, except the drops
        m = n - (L - 1)
        if vals[n] > vals[m]:
            cls = f"s{residue(n, L)}-line"
            p.append(f'<line class="{cls}" x1="{X(m):.1f}" y1="{Y(vals[m]):.1f}" '
                     f'x2="{X(n):.1f}" y2="{Y(vals[n]):.1f}" stroke-width="1.5"/>')
    for n in range(1, N + 1):
        cls = "ink-dot" if vals[n] == 0 else f"s{residue(n, L)}-dot"
        p.append(f'<circle class="{cls}" cx="{X(n):.1f}" cy="{Y(vals[n]):.1f}" r="4.5"><title>N = {n}: {vals[n]}</title></circle>')
        if n % step == 0 or n == 1:
            p.append(f'<text class="tick" x="{X(n):.1f}" y="{base + 18}" text-anchor="middle">{n}</text>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - 16}" y1="{base}" y2="{base}"/>')
    p.append(f'<text class="tick" x="{(x0 + w) / 2:.0f}" y="{h - 4}" text-anchor="middle">N</text></svg>')
    return "".join(p)


def chart_legend(L=2):
    if L == 2:
        chains = '<span><i class="s1"></i>השורד \\( F(N) \\)</span>'
        zeros = "חזקה של 2: השורד הוא 0"
    else:
        if L == 3:
            chains = ('<span><i class="s1"></i>‏\\( N \\) אי-זוגי</span>'
                      '<span><i class="s2"></i>‏\\( N \\) זוגי</span>')
        else:
            chains = "".join(f'<span><i class="s{r}"></i>‏\\( N \\equiv {r % (L - 1)} \\pmod{{{L - 1}}} \\)</span>'
                             for r in range(1, L))
        zeros = "נקודת אפס: השורד הוא 0"
    return (f'<span class="viz-legend">{chains}<span><i class="ink"></i>{zeros}</span>'
            '<span><i class="ink-dash"></i>הקו \\( F = N \\)</span></span>')


# --- rows of boxes -----------------------------------------------------------------------

CELL, GAP = 30, 4


def _row(p, x, y, labels, classes, small=False):
    for i, (lab, cls) in enumerate(zip(labels, classes)):
        bx = x + i * (CELL + GAP)
        p.append(f'<rect class="{cls}" x="{bx}" y="{y}" width="{CELL}" height="{CELL}" rx="4"/>'
                 f'<text class="st-text{" st-sm" if small else ""}" x="{bx + CELL / 2}" y="{y + 21}" text-anchor="middle">{lab}</text>')


def _arrow(p, x, y1, y2, cls="ink-line", marker="q16-ink"):
    p.append(f'<line class="{cls}" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="1.5" marker-end="url(#{marker})"/>')


DEFS = ('<defs><marker id="q16-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/></marker>'
        '<marker id="q16-s2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path class="s2-fill" d="M0,0 L10,5 L0,10 z"/></marker></defs>')


def round_svg(n=8, L=2):
    """One full round over n = L k people: the multiples of L stay, dividing by L gives the
    same problem with k people."""
    k = n // L
    x0, w = 70, 70 + n * (CELL + GAP) + 20
    h = 3 * CELL + 2 * 34 + 20
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         f'aria-label="סיבוב אחד שלם עם {n} אנשים: נשארים הכפולות של {L}, ואחרי חלוקה ב-{L} זו אותה בעיה עם {k} אנשים">', DEFS]
    y = 10
    labels = list(range(n))
    _row(p, x0, y, labels, ["st-stack" if i % L == 0 else "st-bad" for i in labels])
    for i in labels:
        if i % L:
            bx = x0 + i * (CELL + GAP)
            p.append(f'<line class="pg-strike" x1="{bx + 5}" y1="{y + CELL - 5}" x2="{bx + CELL - 5}" y2="{y + 5}"/>')
    p.append(f'<text class="legend" x="{x0 - 10}" y="{y + 20}" text-anchor="end">{n}</text>')
    y2 = y + CELL + 34
    stay = [i for i in labels if i % L == 0]
    _row(p, x0, y2, [i if i in stay else "" for i in labels],
         ["st-stack" if i in stay else "st-cell st-faded" for i in labels])
    for i in stay:
        _arrow(p, x0 + i * (CELL + GAP) + CELL / 2, y + CELL + 3, y2 - 3)
    y3 = y2 + CELL + 34
    _row(p, x0, y3, list(range(k)), ["st-ok"] * k)
    for j, i in enumerate(stay):
        xa, xb = x0 + i * (CELL + GAP) + CELL / 2, x0 + j * (CELL + GAP) + CELL / 2
        p.append(f'<line class="s2-line" x1="{xa}" y1="{y2 + CELL + 3}" x2="{xb}" y2="{y3 - 3}" '
                 'stroke-width="1.5" marker-end="url(#q16-s2)"/>')
    p.append(f'<text class="legend" x="{x0 - 10}" y="{y3 + 20}" text-anchor="end">{k}</text>')
    p.append(f'<text class="legend" x="{x0 + k * (CELL + GAP) + 10}" y="{y3 + 20}">÷ {L}</text>')
    p.append("</svg>")
    return "".join(p)


def relabel_svg(n=7, L=2):
    """After person 0 stays and 1 .. L-1 leave: the count goes on from person L, which gets
    the new number 0. Old number = (new number + L) mod n."""
    x0, w = 70, 70 + n * (CELL + GAP) + 20
    h = 2 * CELL + 34 + 20
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         f'aria-label="אחרי שאדם 0 נשאר ו-{L - 1} הבאים יוצאים, {n - L + 1} האנשים שנשארו מקבלים מספרים חדשים מ-0, החל מאדם {L}">', DEFS]
    y = 10
    old = list(range(n))
    _row(p, x0, y, old, ["st-stack" if i == 0 else "st-bad" if i < L else "st-cell" for i in old])
    for i in range(1, L):
        bx = x0 + i * (CELL + GAP)
        p.append(f'<line class="pg-strike" x1="{bx + 5}" y1="{y + CELL - 5}" x2="{bx + CELL - 5}" y2="{y + 5}"/>')
    p.append(f'<text class="legend" x="{x0 - 10}" y="{y + 20}" text-anchor="end">ישן</text>')
    y2 = y + CELL + 34
    new = {i: (i - L) % n for i in old if i == 0 or i >= L}
    _row(p, x0, y2, [new.get(i, "") for i in old],
         ["st-ok" if i in new else "st-cell st-faded" for i in old])
    for i in new:
        _arrow(p, x0 + i * (CELL + GAP) + CELL / 2, y + CELL + 3, y2 - 3)
    p.append(f'<text class="legend" x="{x0 - 10}" y="{y2 + 20}" text-anchor="end">חדש</text>')
    p.append("</svg>")
    return "".join(p)


def bits_svg(examples=(20, 41)):
    """L = 2: drop the leading 1 of N and append a 0; the result is F(N) = 2r."""
    longest = max(len(f"{n:b}") for n in examples)
    w, h = 70 + 2 * longest * (CELL + GAP) + 90 + 50, 24 + 86 * len(examples)
    p = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:{w / 16:.0f}rem" role="img" '
         'aria-label="הביט העליון של N נמחק ובסוף נוסף 0, והתוצאה היא השורד">', DEFS]
    y = 14
    for n in examples:
        b = f"{n:b}"
        res = b[1:] + "0"
        xa, xb = 70, 70 + len(b) * (CELL + GAP) + 90
        p.append(f'<text class="legend" x="{xa - 12}" y="{y + 20}" text-anchor="end">{n}</text>')
        _row(p, xa, y, b, ["st-bad" if i == 0 else "st-cell" for i in range(len(b))])
        bx = xa
        p.append(f'<line class="pg-strike" x1="{bx + 5}" y1="{y + CELL - 5}" x2="{bx + CELL - 5}" y2="{y + 5}"/>')
        _row(p, xb, y, res, ["st-cell"] * (len(res) - 1) + ["st-ok"])
        x_end = xb + len(res) * (CELL + GAP)
        p.append(f'<text class="legend" x="{x_end + 8}" y="{y + 20}">{int(res, 2)}</text>')
        p.append(f'<line class="ink-line" x1="{xa + len(b) * (CELL + GAP) + 12}" y1="{y + CELL / 2}" '
                 f'x2="{xb - 14}" y2="{y + CELL / 2}" stroke-width="1.5" marker-end="url(#q16-ink)"/>')
        # the bits of r slide one place to the left
        xs, xe = xa + (CELL + GAP) + CELL / 2, xb + CELL / 2
        p.append(f'<path class="s2-line" d="M{xs},{y + CELL + 4} C{xs},{y + CELL + 40} {xe},{y + CELL + 40} {xe},{y + CELL + 6}" '
                 f'fill="none" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#q16-s2)"/>')
        y += 86
    p.append("</svg>")
    return "".join(p)


if __name__ == "__main__":
    print(circle_stepper(20), "\n")
    print(rounds_table(20), "\n")
    print(survivors_table(), "\n")
    print(chart_legend(), "\n")
    print(chart(), "\n")
    print(relabel_svg(7), "\n")
    print(round_svg(8), "\n")
    print(bits_svg())
