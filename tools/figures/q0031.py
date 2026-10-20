#!/usr/bin/env python3
"""Figures and tables of question 0031 (the bridge and the torch).

    python tools/figures/fill.py 31        # put the blocks on the page

Four people with crossing times 1, 2, 5 and 10 minutes, a bridge that holds two, one
torch. blocks() returns, in page order: the statement figure (everyone on the near bank),
its legend, the step-through figure of the 17-minute plan, the plan as a table, the table
of the three strategies (escort everyone: 19; pair the slowest: 17; the other 17), and for
part b the table of examples where the search and the greedy rule agree. The plan comes
from an independent Dijkstra over (who is across, torch side); tests/0031 checks it
against brute force and against the page code.
"""

import heapq
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

TIMES = [1, 2, 5, 10]
NAMES = "ABCD"


# --- the search -------------------------------------------------------------------------

def plan(times):
    """(total time, crossings) by Dijkstra over (across mask, torch side); ties broken by
    the fewest crossings and then by the smallest indices, so the figure is stable."""
    n = len(times)
    everyone = (1 << n) - 1
    start = (0, 0)
    best = {start: 0}
    queue = [(0, [], start)]
    while queue:
        t, path, (across, side) = heapq.heappop(queue)
        if t > best[(across, side)]:
            continue
        if across == everyone:
            return t, path
        here = [i for i in range(n) if (across >> i) & 1 == side]
        groups = [(i,) for i in here] + list(combinations(here, 2))
        for g in groups:
            mask = sum(1 << i for i in g)
            new = (across ^ mask, 1 - side)
            cost = t + max(times[i] for i in g)
            if cost < best.get(new, float("inf")):
                best[new] = cost
                heapq.heappush(queue, (cost, path + [g], new))
    return None


def escort(times):
    """The fastest person escorts everyone else, one at a time."""
    s = sorted(times)
    return s[-1] if len(s) < 3 else s[0] * (len(s) - 2) + sum(s[1:])


def greedy(times):
    """The rule of part b: for the two slowest, min(t1 + 2 t2 + tn, 2 t1 + t(n-1) + tn)."""
    s = sorted(times)
    total = 0
    while len(s) > 3:
        total += min(s[0] + 2 * s[1] + s[-1], 2 * s[0] + s[-2] + s[-1])
        s = s[:-2]
    return total + (sum(s) if len(s) == 3 else s[-1])


def replay(times, moves):
    """Total time of a crossing sequence, or None when it is not legal."""
    n, across, side, t = len(times), 0, 0, 0
    for g in moves:
        if not 1 <= len(g) <= 2 or any((across >> i) & 1 != side for i in g):
            return None
        across ^= sum(1 << i for i in g)
        side = 1 - side
        t += max(times[i] for i in g)
    return t if across == (1 << n) - 1 else None


# --- the figure --------------------------------------------------------------------------

def frame(times, across, side, moving=(), forward=True, t=0, label=""):
    """The two banks, the bridge, the torch and the people; `moving` are on the bridge."""
    w, h = 640, 190
    p = [f'<svg class="figure bridge-fig" viewBox="0 0 {w} {h}" style="max-width:40rem" role="img" aria-label="{label}">',
         '<rect class="bank" x="0" y="20" width="190" height="150" rx="8"/>',
         '<rect class="bank" x="450" y="20" width="190" height="150" rx="8"/>',
         '<rect class="river" x="190" y="20" width="260" height="150"/>',
         '<rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/>',
         '<text class="legend" x="95" y="160" text-anchor="middle">near</text>',
         '<text class="legend" x="545" y="160" text-anchor="middle">far</text>']
    n = len(times)
    near = [i for i in range(n) if not (across >> i) & 1 and i not in moving]
    far = [i for i in range(n) if (across >> i) & 1 and i not in moving]

    def person(i, x, y, cls):
        p.append(f'<g><circle class="{cls}" cx="{x}" cy="{y}" r="17"/>'
                 f'<text class="st-text" x="{x}" y="{y + 5}" text-anchor="middle">{times[i]}</text>'
                 f'<text class="st-small" x="{x}" y="{y + 30}" text-anchor="middle">{NAMES[i]}</text></g>')

    for k, i in enumerate(near):
        person(i, 40 + 40 * k, 60, "st-cell")
    for k, i in enumerate(far):
        person(i, 490 + 40 * k, 60, "st-ok")
    for k, i in enumerate(moving):
        person(i, 290 + 60 * k, 95, "st-stack")
    if moving:
        x0, x1 = (236, 404) if forward else (404, 236)
        p.append(f'<line class="ink-line" x1="{x0}" y1="128" x2="{x1}" y2="128" stroke-width="2"/>'
                 f'<polygon class="ink-fill" points="{x1},128 {x1 - (9 if forward else -9)},123 {x1 - (9 if forward else -9)},133"/>')
    # the torch: on the bridge with the walkers, else on the bank where it is
    tx = 320 if moving else (150 if side == 0 else 490)
    ty = 150 if moving else 118
    p.append(f'<polygon class="torch" points="{tx},{ty - 14} {tx + 6},{ty - 2} {tx},{ty + 2} {tx - 6},{ty - 2}"/>'
             f'<rect class="ink-fill" x="{tx - 1.5}" y="{ty + 2}" width="3" height="10"/>')
    p.append(f'<text class="legend" x="{w - 10}" y="{h - 8}" text-anchor="end" font-weight="700">t = {t}</text>')
    p.append("</svg>")
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="st-cell"></i>על הגדה הקרובה</span><span><i class="st-stack"></i>חוצים עכשיו</span>'
            '<span><i class="st-ok"></i>כבר על הגדה הרחוקה</span><span><i class="torch"></i>הלפיד</span></span>')


def statement_figure(times=TIMES):
    return frame(times, 0, 0, label="ארבעה אנשים עם הלפיד על הגדה הקרובה של הגשר, עם הזמנים 1, 2, 5 ו-10 דקות")


def heb_group(times, g):
    return " ו-".join(f"{NAMES[i]} ({times[i]})" for i in g)


def crossing_stepper(times=TIMES):
    total, moves = plan(times)
    frames = [(frame(times, 0, 0, label="התחלה: כולם על הגדה הקרובה"), "רגע 0: כולם והלפיד על הגדה הקרובה. הגשר מחזיק שניים, והזוג הולך בקצב האיטי.")]
    across, side, t = 0, 0, 0
    for k, g in enumerate(moves, 1):
        forward = side == 0
        cost = max(times[i] for i in g)
        t += cost
        frames.append((frame(times, across, side, g, forward, t, label=f"חצייה {k}"),
                       f"חצייה {k}: {heb_group(times, g)} {'חוצים' if len(g) > 1 else 'חוזר'} "
                       f"{'קדימה' if forward else 'עם הלפיד חזרה'}, {cost} דקות. עברו {t} דקות."))
        across ^= sum(1 << i for i in g)
        side = 1 - side
    frames.append((frame(times, across, side, t=t, label="סיום"), f"כולם על הגדה הרחוקה אחרי {t} דקות."))
    return stepper(frames, f"התוכנית של {total} דקות, חצייה אחרי חצייה")


def plan_table(times=TIMES):
    total, moves = plan(times)
    lines = ["| חצייה | מי | לאן | הזמן | סה\"כ |", "|:-:|---|---|:-:|:-:|"]
    side, t = 0, 0
    for k, g in enumerate(moves, 1):
        cost = max(times[i] for i in g)
        t += cost
        lines.append(f"| {k} | ‏{heb_group(times, g)} | {'קדימה' if side == 0 else 'חזרה'} | {cost} | {t} |")
        side = 1 - side
    return "\n".join(lines)


def strategies_table(times=TIMES):
    s = sorted(times)
    pair = s[0] + 2 * s[1] + s[-1] + s[1]          # 1+2, 1 back, 5+10, 2 back, 1+2
    esc = escort(s)
    lines = ["| האסטרטגיה | החציות | הזמן |", "|---|---|:-:|",
             f"| המהיר מלווה את כולם | ‏A+D, ‏A, ‏A+C, ‏A, ‏A+B | ‏{esc} |",
             f"| שני האיטיים חוצים יחד | ‏A+B, ‏A, ‏C+D, ‏B, ‏A+B | ‏{pair} |",
             f"| אותו רעיון, בסדר אחר | ‏A+B, ‏B, ‏C+D, ‏A, ‏A+B | ‏{pair} |"]
    return "\n".join(lines)


EXAMPLES = [[1, 2, 5, 10], [1, 2, 3, 4], [1, 3, 4, 6], [1, 1, 1, 1], [2, 2, 2, 2, 2], [1, 2, 5, 10, 20], [1, 4, 5, 6, 7, 8]]


def examples_table():
    lines = ["| הזמנים | המהיר מלווה | החיפוש (Dijkstra) | הכלל החמדני |", "|---|:-:|:-:|:-:|"]
    for ts in EXAMPLES:
        total, _ = plan(ts)
        lines.append(f"| ‏{', '.join(map(str, ts))} | ‏{escort(ts)} | ‏{total} | ‏{greedy(ts)} |")
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [statement_figure(), legend(), crossing_stepper(), plan_table(), strategies_table(), examples_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
