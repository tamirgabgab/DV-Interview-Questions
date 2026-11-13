#!/usr/bin/env python3
"""Figures and tables of question 0109, car fleets: cars on a one-lane road drive toward a
target; a car that catches the car ahead sticks to it and drives at its speed (a fleet).

    python tools/figures/fill.py 109        # put the blocks on the page

The references here are independent of the page code, and exact (fractions.Fraction):

- simulate(pos, speed, target) moves the fleets from event to event: every fleet drives on
  the free line of its front car, the next event is the first catch between neighbours or
  the first arrival at the target (none on an infinite road, target None); fleets that meet
  merge, a meeting exactly at the target included. It returns the time every car touches
  the car ahead (or None), the arrival time of every car, and the events.
- envelope(pos, speed, target, i, t) is the real place of car i at time t by the page's
  picture: the minimum of the free lines of i and of every car ahead (and of the target).
- by_formula(target, pos, speed) is part a's rule: the cars from the front, T = max(alone,
  T of the car ahead), a new fleet when T grows strictly.
- by_stack(pos, speed) is part b's monotonic stack, with its trace.

Cars are named by their place on the road from the back: car 0 is the furthest from the
target (part b's order). blocks() returns, in page order: the road of the statement's
example and its legend, the position-time graph of the example and its legend, the graph of
the two-car example with a meeting at a fraction of a second, part a's table, the graph of
part b's chain and its legend, and part b's table of the stack.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from charts import Chart  # noqa: E402

RLM = "‏"
NB = " "
MINUS = "−"

# the inputs of the page and of the box: (target, positions, speeds)
EXAMPLE = (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3])    # LeetCode 853: 3 fleets
TWO = (10, [0, 1], [3, 1])                           # A at 0 speed 3, B at 1 speed 1: they meet at 1/2
CHAIN = ([3, 5, 6, 9], [4, 4, 3, 1])                 # LeetCode 1776, example 2: 2, 1, 3/2, -1
CHAIN_TARGET = 12                                    # the chain in the box of part a
THREE = (10, [0, 2, 6], [3, 4, 1])                   # the trap: A never catches B's own line, yet joins
FLOAT = (2, [0, 1], [7, 1])                          # the float trap: 1/6 + 5/6 = 1.0000000000000002


# --- the references --------------------------------------------------------------------------------

def road(pos, speed):
    """The cars in road order, from the back: [(p, s)], and the input index of each."""
    order = sorted(range(len(pos)), key=lambda i: pos[i])
    return [(pos[i], speed[i]) for i in order], order


def lone(target, p, s) -> Fraction:
    return Fraction(target - p, s)


def simulate(pos, speed, target=None):
    """Exact fleets on the road (cars in road order, from the back). Returns (touch, arrive,
    events): touch[r] the time car r touches car r + 1 (None if never, or only past the target),
    arrive[r] its arrival time (None on an infinite road), events a list of
    ("meet", t, x, r, r + 1) and ("arrive", t, [cars])."""
    cars, _ = road(pos, speed)
    n = len(cars)
    touch, arrive, events = [None] * n, [None] * n, []
    fleets = [[r, r] for r in range(n)]                      # [back, front], contiguous, back to front
    line = lambda f: cars[f[1]]                              # noqa: E731 - a fleet drives on its front's free line
    at = lambda f, t: line(f)[0] + line(f)[1] * t            # noqa: E731
    t = Fraction(0)
    while fleets:
        cand = []
        for a, b in zip(fleets, fleets[1:]):
            (pa, sa), (pb, sb) = line(a), line(b)
            if sa > sb:
                tc = Fraction(pb - pa, sa - sb)
                if target is None or pa + sa * tc <= target:
                    cand.append(tc)
        if target is not None:
            cand += [lone(target, *line(f)) for f in fleets]
        if not cand:
            break
        t = min(cand)
        merged = [fleets[0]]
        for f in fleets[1:]:
            g = merged[-1]
            if at(g, t) == at(f, t):
                touch[g[1]] = t
                events.append(("meet", t, at(f, t), g[1], f[0]))
                merged[-1] = [g[0], f[1]]
            else:
                merged.append(f)
        fleets = merged
        if target is not None:
            done = [f for f in fleets if at(f, t) == target]
            for f in done:
                for r in range(f[0], f[1] + 1):
                    arrive[r] = t
                events.append(("arrive", t, list(range(f[0], f[1] + 1))))
            fleets = [f for f in fleets if at(f, t) != target]
    return touch, arrive, events


def envelope(pos, speed, target, r, t) -> Fraction:
    """Car r's place at time t (road order): the lowest free line of r and the cars ahead."""
    cars, _ = road(pos, speed)
    x = min(p + s * Fraction(t) for p, s in cars[r:])
    return x if target is None else min(x, Fraction(target))


def by_formula(target, pos, speed):
    """Part a's rule, front first: rows (r, p, s, alone, T, fleet number, new?) and the count."""
    cars, _ = road(pos, speed)
    rows, ahead, count = [], Fraction(0), 0
    for r in range(len(cars) - 1, -1, -1):
        p, s = cars[r]
        t = lone(target, p, s)
        new = t > ahead
        if new:
            count += 1
            ahead = t
        rows.append((r, p, s, t, ahead, count, new))
    return rows, count


def by_stack(pos, speed):
    """Part b (positions increasing): the time every car hits the car ahead, -1 if never, the
    car whose free line it meets, and the trace: per car, the stack before (top last) and the
    cars popped with the reason ("speed" or "late", with the meeting time)."""
    n = len(pos)
    ans, on, stack, trace = [-1] * n, [None] * n, [], []
    for i in range(n - 1, -1, -1):
        before, popped = stack[:], []
        while stack:
            j = stack[-1]
            if speed[i] <= speed[j]:
                popped.append((j, "speed", None))
            else:
                tc = Fraction(pos[j] - pos[i], speed[i] - speed[j])
                if ans[j] == -1 or tc < ans[j]:
                    ans[i], on[i] = tc, j
                    break
                popped.append((j, "late", tc))
            stack.pop()
        stack.append(i)
        trace.append((i, before, popped, ans[i], on[i]))
    return ans, on, trace


def fleets_at(touch, t) -> int:
    """The fleets on an infinite road at time t: the cars not touching the car ahead yet."""
    return sum(1 for c in touch if c is None or c > t)


# --- formatting ---------------------------------------------------------------------------------------

def frac(v) -> str:
    """A time or a place as a plain fraction for the SVG titles: 3/2, 7, −1."""
    v = Fraction(v)
    s = f"{abs(v.numerator)}" if v.denominator == 1 else f"{abs(v.numerator)}/{v.denominator}"
    return f"{MINUS}{s}" if v < 0 else s


def tex(v) -> str:
    """A fraction for MathJax: \\( \\tfrac{10}{3} \\), or a whole number as it is."""
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return f"\\( {sign}\\tfrac{{{abs(v.numerator)}}}{{{v.denominator}}} \\)"


def cell(v) -> str:
    """A table cell: a whole number as it is, a fraction in math after an RLM."""
    s = tex(v)
    return s if s.lstrip("-").isdigit() else f"{RLM}{s}"


def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def num(v) -> str:
    return f"{MINUS}{-v}" if v < 0 else f"{v:g}"


# --- the road -------------------------------------------------------------------------------------------

def road_svg(target, pos, speed, label) -> str:
    """The road at time 0: the cars at their places, each with its speed, and the target."""
    cars, _ = road(pos, speed)
    W, H, x0, x1, Y = 640, 108, 30, 600, 62
    X = lambda v: x0 + (x1 - x0) * v / target            # noqa: E731
    o = [f'<svg class="figure cf-road" viewBox="0 0 {W} {H}" direction="ltr" role="img" aria-label="{label}">',
         f'<line class="cf-lane" x1="{x0 - 14}" x2="{X(target):.1f}" y1="{Y}" y2="{Y}"/>']
    for v in range(0, target + 1):
        o.append(f'<line class="cf-tickl" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{Y - 4}" y2="{Y + 4}"/>')
        if v % 2 == 0 or v == target:
            o.append(f'<text class="tick" x="{X(v):.1f}" y="{Y + 22}" text-anchor="middle">{v}</text>')
    o.append(f'<line class="cf-goal" x1="{X(target):.1f}" x2="{X(target):.1f}" y1="{Y - 44}" y2="{Y + 8}"/>'
             f'<path class="cf-flag" d="M{X(target):.1f},{Y - 44} l16,6 l-16,6 Z"/>')
    for r, (p, s) in enumerate(cars):
        x = X(p)
        o.append(f'<g class="cf-car"><title>car at {p}, speed {s}</title>'
                 f'<rect x="{x - 13:.1f}" y="{Y - 34}" width="26" height="22" rx="6"/>'
                 f'<text x="{x:.1f}" y="{Y - 18}" text-anchor="middle">{s}</text>'
                 f'<path class="cf-arrow" d="M{x + 16:.1f},{Y - 28} l7,5 l-7,5 Z"/></g>')
    o.append("</svg>")
    return "".join(o)


def road_legend() -> str:
    return ('<span class="viz-legend"><span><i class="cf-key-car"></i>מכונית, ובתוכה המהירות שלה</span>'
            '<span><i class="cf-key-goal"></i>היעד</span></span>')


# --- the position-time graphs ----------------------------------------------------------------------------

def graph(pos, speed, target, label, t_max, y_min, y_max, *, x_step=1, y_step=1, ghosts=(), notes=(), by_car=False):
    """Time along x, the place along y. Every car's free line dashed (to the target, or to
    t_max), its real path bold in the colour of its fleet, the meetings as rings, the target
    as a dashed line. `ghosts` are crossings of free lines that never happen (hollow), `notes`
    short labels (t, x, text, dx, dy). With `by_car` every car has its own colour and number,
    and the paths are drawn from the back, wider under narrower: a stretch the cars share
    shows the colour of the front car, whose free line the fleet drives on."""
    cars, _ = road(pos, speed)
    n = len(cars)
    touch, arrive, events = simulate(pos, speed, target)
    group, g = [0] * n, 0
    for r in range(n - 1, -1, -1):                         # the fleet at the end, numbered from the front
        if r < n - 1 and touch[r] is None:
            g += 1
        group[r] = g
    if by_car:
        group = list(range(n))
    c = Chart(label, w=640, h=300, x0=44, right=16, top=16, base=262, x_min=0, x_max=t_max, y_min=y_min, y_max=y_max)
    c.parts[0] = c.parts[0].replace('class="perf-chart"', 'class="perf-chart cf-graph" direction="ltr"')
    ys = list(range(math.ceil(y_min / y_step) * y_step, int(y_max) + 1, y_step))
    c.grid_y(ys)
    xs = [k * x_step for k in range(int(t_max / x_step) + 1)]
    for x in xs:
        c.add(f'<text class="tick" x="{c.X(x):.1f}" y="{c.base + 18}" text-anchor="middle">{x:g}</text>')
    if target is not None:
        c.add(f'<line class="cf-target" x1="{c.x0}" x2="{c.x1}" y1="{c.Y(target):.1f}" y2="{c.Y(target):.1f}"/>')
    end = lambda p, s: lone(target, p, s) if target is not None else Fraction(y_max - p, s)   # noqa: E731 - to the top
    for r, (p, s) in enumerate(cars):                      # the free lines
        te = min(end(p, s), Fraction(t_max))
        c.add(f'<line class="cf-free cf-c{group[r] % 6}" x1="{c.X(0):.1f}" y1="{c.Y(p):.1f}" x2="{c.X(te):.1f}" y2="{c.Y(p + s * te):.1f}">'
              f'<title>car {r}: free line x = {p} + {s}t</title></line>')
    for r, (p, s) in enumerate(cars):                      # the real paths: the envelope at its kinks
        stop = arrive[r] if target is not None else Fraction(t_max)
        ts = {Fraction(0), stop}
        for k in range(r, n):
            for m in range(k + 1, n):
                (pk, sk), (pm, sm) = cars[k], cars[m]
                if sk != sm:
                    tc = Fraction(pm - pk, sk - sm)
                    if 0 < tc < stop:
                        ts.add(tc)
        pts = [(tt, envelope(pos, speed, target, r, tt)) for tt in sorted(ts)]
        c.path(pts, f"cf-path cf-c{group[r] % 6}", width=round(3 + 1.6 * (n - 1 - r), 1) if by_car else 3.2)
        if by_car:
            c.add(f'<text class="cf-carno cf-c{r % 6}" x="{c.X(0) + 9:.1f}" y="{c.Y(p) - 7:.1f}" text-anchor="middle">{r}</text>')
    for gx, gy in ghosts:
        c.add(f'<circle class="cf-ghost" cx="{c.X(gx):.1f}" cy="{c.Y(gy):.1f}" r="5"><title>t = {frac(gx)}, x = {frac(gy)}: the lines cross, but too late</title></circle>')
    seen = set()
    for ev in events:
        if ev[0] != "meet" or (ev[1], ev[2]) in seen:
            continue
        seen.add((ev[1], ev[2]))
        c.add(f'<circle class="cf-meet" cx="{c.X(ev[1]):.1f}" cy="{c.Y(ev[2]):.1f}" r="5.5"><title>t = {frac(ev[1])}, x = {frac(ev[2])}: car {ev[3]} reaches car {ev[4]}</title></circle>')
    for tx, xv, text, dx, dy in notes:
        c.add(f'<text class="cf-lab" x="{c.X(tx) + dx:.1f}" y="{c.Y(xv) + dy:.1f}" text-anchor="middle">{text}</text>')
    c.axis()
    c.add(f'<line class="axis" x1="{c.x0}" x2="{c.x0}" y1="{c.top}" y2="{c.base}"/>')
    return c.svg()


def graph_legend(target=True, ghost=False, by_car=False) -> str:
    whose = "של המכונית : קטע משותף בצבע של המכונית שבראש" if by_car else "של השיירה"
    parts = ['<span><i class="cf-key-free"></i>הקו החופשי : המקום אילו המכונית נסעה לבד</span>',
             f'<span><i class="cf-key-path"></i>הדרך האמיתית, בצבע {whose}</span>',
             '<span><i class="cf-key-meet"></i>מפגש</span>']
    if ghost:
        parts.append('<span><i class="cf-key-ghost"></i>קווים שנחתכים מאוחר מדי : המכונית שלפנים כבר האטה</span>')
    if target:
        parts.append('<span><i class="cf-key-target"></i>היעד</span>')
    return '<span class="viz-legend">' + "".join(p.replace(" : ", f"{NB}: ") for p in parts) + "</span>"


# --- the tables -------------------------------------------------------------------------------------------

def formula_table() -> str:
    target, pos, speed = EXAMPLE
    rows, _ = by_formula(target, pos, speed)
    out = [f"| המקום \\( p \\) | המהירות \\( s \\) | לבד, \\( t = (12 - p) / s \\) | ‏\\( T \\), המקסימום עד כאן | השיירה |",
           "|:-:|:-:|:-:|:-:|---|"]
    prev = None
    for r, p, s, t, T, k, new in rows:
        if new:
            what = f"שיירה חדשה, {k}"
        elif t == prev:
            what = f"מצטרפת ל-{k}, נפגשות ביעד"
        else:
            what = f"מצטרפת ל-{k}"
        out.append(f"| {p} | {s} | {cell(t)} | {'**' + cell(T) + '**' if new else cell(T)} | {what} |")
        prev = T
    return "\n".join(out)


def stack_table() -> str:
    pos, speed = CHAIN
    ans, on, trace = by_stack(pos, speed)
    out = ["| המכונית | המקום \\( p \\) | המהירות \\( s \\) | המחסנית לפני, מלמעלה | מה קורה | הזמן |", "|:-:|:-:|:-:|:-:|---|:-:|"]
    for i, before, popped, a, j in trace:
        st = ltr(", ".join(str(k) for k in reversed(before))) if before else "ריקה"
        st = f"{RLM}{st}" if before else st
        steps = []
        for k, why, tc in popped:
            if why == "speed":
                steps.append(f"מוציאים את {k} : {i} לא מהירה ממנה ({speed[i]} מול {speed[k]})")
            else:
                steps.append(f"מוציאים את {k} : הקווים נפגשים ב-{tex(tc)}, אבל {k} נבלעת כבר ב-{tex(ans[k])}")
        if j is not None:
            steps.append(f"פוגשת את הקו של {j} ב-{tex(a)}, לפני ש-{j} נבלעת" if ans[j] != -1 else f"פוגשת את הקו של {j} ב-{tex(a)}")
        else:
            steps.append("אין לפניה אף אחת")
        out.append(f"| {i} | {pos[i]} | {speed[i]} | {st} | " + ". ".join(s.replace(" : ", f"{NB}: ") for s in steps)
                   + f" | {cell(a) if a != -1 else RLM + ltr(MINUS + '1')} |")
    return "\n".join(out)


# --- the blocks -------------------------------------------------------------------------------------------

def blocks():
    target, pos, speed = EXAMPLE
    t2, p2, s2 = TWO
    return [
        road_svg(target, pos, speed, f"הדוגמה בזמן 0{NB}: היעד ב-12, והמכוניות במקומות 0, 3, 5, 8 ו-10 עם המהירויות 1, 3, 1, 4 ו-2"),
        road_legend(),
        graph(p2, s2, t2, f"שתי מכוניות והיעד ב-10{NB}: A מ-0 במהירות 3 ו-B מ-1 במהירות 1. A משיגה את B בזמן חצי, במקום 1.5, "
              "ומשם נוסעת במהירות 1 ומגיעה בזמן 9, ולא בזמן 10 חלקי 3 של הקו החופשי שלה", 9.5, 0, 10, x_step=1, y_step=2,
              notes=[(Fraction(1, 2), Fraction(3, 2), "τ = 1/2", 22, 16), (Fraction(10, 3), 10, "10/3", 24, 18), (9, 10, "9", 14, 18)]),
        graph_legend(),
        graph(pos, speed, target, f"המקום מול הזמן בדוגמה{NB}: הקווים החופשיים מקווקווים והדרכים האמיתיות מודגשות. "
              "המכוניות מ-8 ומ-10 נפגשות ביעד בזמן 1, המכונית מ-3 משיגה את זו מ-5 בזמן 1 במקום 6 ומגיעה איתה בזמן 7, "
              "והמכונית מ-0 מגיעה לבד בזמן 12. שלוש שיירות", 12.5, 0, 12, x_step=1, y_step=2),
        graph_legend(),
        formula_table(),
        graph(*CHAIN, None, f"השרשרת של סעיף ב בלי יעד{NB}: מכוניות 0 עד 3 מהמקומות 3, 5, 6 ו-9 במהירויות 4, 4, 3 ו-1. "
              "מכונית 2 משיגה את 3 בזמן 3 חלקי 2, מכונית 1 את 2 בזמן 1, ומכונית 0 את השיירה בזמן 2. "
              "הקו החופשי של 0 חותך את הקו של 2 רק בזמן 3, אחרי ש-2 כבר נבלעה", 3.25, 3, 16, x_step=1, y_step=2,
              ghosts=[(3, 15)], by_car=True),
        graph_legend(target=False, ghost=True, by_car=True),
        stack_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
