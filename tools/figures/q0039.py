#!/usr/bin/env python3
"""Figures and tables of question 0039 (egg drop: three eggs and 100 floors, then k eggs
and n floors).

    python tools/figures/fill.py 39        # put the blocks on the page

The reference here is independent of the page code: covered(k, t) is the binomial sum
C(t, 1) + ... + C(t, k), the plan drops from low + covered(k - 1, t - 1) + 1, and run()
plays it against a threshold. blocks() returns, in page order: the table of floors
covered by 1, 2 and 3 eggs per number of drops, the building figure of the plan for
three eggs and 100 floors, the plan table (the first egg's floors with what each
outcome leaves), the chart of drops used against every threshold, the table of the
answer for k eggs on 100 and 1,000 floors, and the examples table of part b.
tests/0039 checks every number against the page code and against brute force.
"""

from math import comb

K, N = 3, 100
RLM = "‏"


# --- the model --------------------------------------------------------------------------

def covered(k, t):
    """The most floors k eggs settle in t drops: C(t, 1) + ... + C(t, k)."""
    return sum(comb(t, i) for i in range(1, k + 1))


def min_drops(k, n):
    t = 0
    while covered(k, t) < n:
        t += 1
    return t


def run(k, n, threshold):
    """The plan against a threshold (the egg breaks from floor threshold + 1): the drops
    as (floor, broke), from the first egg's floor low + covered(k - 1, t - 1) + 1."""
    t, low, high, eggs, drops = min_drops(k, n), 0, n + 1, k, []
    while high - low > 1:
        floor = min(low + covered(eggs - 1, t - 1) + 1, high - 1)
        broke = floor > threshold
        drops.append((floor, broke))
        t -= 1
        if broke:
            high, eggs = floor, eggs - 1
        else:
            low = floor
    assert low == threshold
    return drops


def first_egg_floors(k, n):
    """The floors the first egg is dropped from while it survives (the worst case for it)."""
    return [fl for fl, _ in run(k, n, n)]


def drops_per_threshold(k, n):
    return [len(run(k, n, T)) for T in range(n + 1)]


# --- tables ------------------------------------------------------------------------------

def covered_table(tmax=9, ks=(1, 2, 3), n=N):
    lines = ["| הטלות t | ביצה אחת | שתי ביצים | שלוש ביצים |", "|:-:|:-:|:-:|:-:|"]
    for t in range(1, tmax + 1):
        cells = []
        for k in ks:
            v = covered(k, t)
            cells.append(f"{RLM}**{v}** ✓" if v >= n and covered(k, t - 1) < n else f"{RLM}{v}")
        lines.append(f"| {RLM}{t} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def plan_table(k=K, n=N):
    t = min_drops(k, n)
    lines = ["| הטלה | הקומה | אם נשברה : נשארו | אם לא נשברה : נשארו |", "|:-:|:-:|---|---|"]
    low = 0
    for i, fl in enumerate(first_egg_floors(k, n), 1):
        left = t - i
        below = fl - low - 1
        above = n - fl
        lines.append(f"| {RLM}{i} | {RLM}{fl} | {RLM}{k - 1} ביצים ו-{left} הטלות ל-{below} קומות ({low + 1} עד {fl - 1}) | "
                     + (f"{RLM}{k} ביצים ו-{left} הטלות ל-{above} קומות ({fl + 1} עד {n}) |" if above else "הכול ידוע : הסף הוא 100 |"))
        low = fl
    return "\n".join(lines)


def answers_table(ks=range(1, 11), ns=(100, 1000)):
    lines = ["| ביצים k | " + " | ".join(f"הטלות ל-{n} קומות" for n in ns) + " |", "|:-:|" + ":-:|" * len(ns)]
    for k in ks:
        lines.append(f"| {RLM}{k} | " + " | ".join(f"{RLM}{min_drops(k, n)}" for n in ns) + " |")
    return "\n".join(lines)


EXAMPLES = [(1, 100), (2, 100), (3, 100), (2, 36), (3, 14), (4, 1000), (10, 1000)]


def examples_table():
    lines = ["| ביצים | קומות | הטלות | הקומות של הביצה הראשונה |", "|:-:|:-:|:-:|---|"]
    for k, n in EXAMPLES:
        fl = first_egg_floors(k, n)
        shown = ", ".join(map(str, fl)) if len(fl) <= 12 else ", ".join(map(str, fl[:10])) + ", …"
        lines.append(f"| {RLM}{k} | {RLM}{n} | {RLM}{min_drops(k, n)} | {RLM}{shown} |")
    return "\n".join(lines)


# --- the figures --------------------------------------------------------------------------

def building_svg(k=K, n=N):
    """The building with the first egg's floors on the right, the second egg's floors of
    the first gap on the left, and the third egg's single steps in the first sub-gap."""
    W, H, X0, X1, TOP, BOT = 640, 380, 250, 390, 20, 360
    pitch = (BOT - TOP) / n
    y = lambda fl: BOT - fl * pitch                     # the top edge of floor fl
    first = first_egg_floors(k, n)
    second = [fl for fl, broke in run(k, n, first[0] - 1) if not broke and fl < first[0]]
    third = list(range(1, second[0]))
    p = [f'<svg class="figure egg-fig" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
         f'aria-label="בניין של {n} קומות : הקומות של הביצה הראשונה {", ".join(map(str, first))}, של השנייה {", ".join(map(str, second))} ושל השלישית {third[0]} עד {third[-1]}">',
         f'<rect class="egg-wall" x="{X0}" y="{TOP}" width="{X1 - X0}" height="{BOT - TOP}" rx="4"/>']
    for fl in range(10, n, 10):
        p.append(f'<line class="egg-floor" x1="{X0}" x2="{X1}" y1="{y(fl):.1f}" y2="{y(fl):.1f}"/>')
    # the first egg: bands between its floors, a mark and a label on the right
    low = 0
    for i, fl in enumerate(first):
        p.append(f'<rect class="egg-band{i % 2}" x="{X0 + 2}" y="{y(fl):.1f}" width="{X1 - X0 - 4}" height="{(fl - low) * pitch:.1f}"/>')
        p.append(f'<line class="egg-drop1" x1="{X0}" x2="{X1 + 10}" y1="{y(fl):.1f}" y2="{y(fl):.1f}"/>'
                 f'<text class="egg-lbl1" x="{X1 + 16}" y="{y(fl) + 4:.1f}">{fl}</text>')
        low = fl
    p.append(f'<text class="legend" x="{X1 + 16}" y="{TOP - 6}">הביצה הראשונה</text>')
    last_label = None                                    # labels only where they do not overlap
    for fl in reversed(second):
        p.append(f'<line class="egg-drop2" x1="{X0 - 10}" x2="{X1}" y1="{y(fl):.1f}" y2="{y(fl):.1f}"/>')
        if last_label is None or y(fl) - last_label >= 11:
            p.append(f'<text class="egg-lbl2" x="{X0 - 16}" y="{y(fl) + 4:.1f}" text-anchor="end">{fl}</text>')
            last_label = y(fl)
    p.append(f'<text class="legend" x="{X0 - 16}" y="{y(second[-1]) - 8:.1f}" text-anchor="end">הביצה השנייה</text>')
    for fl in third:
        p.append(f'<line class="egg-drop3" x1="{X0 - 60}" x2="{X0 - 40}" y1="{y(fl):.1f}" y2="{y(fl):.1f}"/>')
    p.append(f'<text class="egg-lbl3" x="{X0 - 66}" y="{y(third[-1]) + 10:.1f}" text-anchor="end">{third[0]}–{third[-1]}</text>'
             f'<text class="legend" x="{X0 - 66}" y="{y(third[-1]) - 6:.1f}" text-anchor="end">השלישית</text>')
    p.append(f'<text class="tick" x="{X0 - 6}" y="{BOT + 14}" text-anchor="end">קומה 0</text>'
             f'<text class="tick" x="{X1 + 16}" y="{BOT + 14}">{n} קומות, {min_drops(k, n)} הטלות</text></svg>')
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="egg-key1"></i>הקומות של הביצה הראשונה (כל עוד היא לא נשברת)</span>'
            '<span><i class="egg-key2"></i>הביצה השנייה, אחרי שבירה ב-37</span>'
            '<span><i class="egg-key3"></i>הביצה השלישית, קומה אחר קומה</span></span>')


def threshold_chart(k=K, n=N):
    """Drops used against every threshold, a step line under the worst case."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from charts import Chart

    used = drops_per_threshold(k, n)
    t = min_drops(k, n)
    c = Chart(f"מספר ההטלות לכל סף מ-0 עד {n} : לעולם לא יותר מ-{t}", x_max=n, y_max=t + 1, h=230, base=196)
    c.grid_y(list(range(0, t + 2, 3)))
    c.grid_x([0, 25, 50, 75, 100], dashed=True)
    c.hline(t, f"{t} = המקרה הגרוע", label_at="end")
    pts = []
    for T, d in enumerate(used):
        pts.append((T, d))
    # a step line: hold each value over its threshold
    path = " ".join(f"{c.X(T):.1f},{c.Y(d):.1f} {c.X(T + 1):.1f},{c.Y(d):.1f}" for T, d in pts)
    c.add(f'<polyline class="s1-line" points="{path}" fill="none" stroke-width="2"/>')
    worst = [T for T, d in enumerate(used) if d == t]
    for T in worst[:1] + worst[-1:]:
        c.dot(T + 0.5, used[T], "s2", r=4, title=f"סף {T} : {used[T]} הטלות")
    c.axis("הסף")
    return c.svg()


def chart_legend(k=K, n=N):
    used = drops_per_threshold(k, n)
    t = min_drops(k, n)
    worst = sum(1 for d in used if d == t)
    return (f'<span class="viz-legend"><span><i class="by-multiples"></i>ההטלות שהתוכנית משתמשת בהן לסף הזה</span>'
            f'<span><i class="by-enum"></i>ספים שמגיעים ל-{t} : {worst} מתוך {n + 1}</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [covered_table(), building_svg(), legend(), plan_table(), threshold_chart(), chart_legend(),
            answers_table(), examples_table()]


if __name__ == "__main__":
    print(min_drops(3, 100), first_egg_floors(3, 100), run(3, 100, 36))
    print("\n\n".join(blocks()))
