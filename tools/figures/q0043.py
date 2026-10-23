#!/usr/bin/env python3
"""Figures and tables of question 0043 (horse races without a stopwatch: 36 horses, 6 per
race, the 4 fastest in order; then 30 horses, 6 per race, the 3 fastest, and the general
plan for a horses, b per race, the c fastest).

    python tools/figures/fill.py 43        # put the blocks on the page

The reference here is independent of the page code: plan() keeps, for every horse, the
set of horses known to be faster and the set known to be slower (transitively closed),
races the groups, then the group winners, then, while the first c ranks are not settled,
the b most promising unsettled candidates with the most comparisons still missing between
them (the same rule as the page code, so the race logs are comparable). blocks() returns,
in page order: the staircase table of part a, the grid figure after the winners' race
with its legend, the race log of the page's example of part a, the grid and the log of
part b, and the examples table of the general plan. tests/0043 checks every number against
the page code, brute force over every ordering of the staircase, and the explorer.
"""

import random
import sys
from math import ceil
from pathlib import Path

A, B, C = 36, 6, 4
A2, B2, C2 = 30, 6, 3
RLM = "‏"
LETTERS = "ABCDEFGHIJ"


# --- the model --------------------------------------------------------------------------

def plan(a, b, c, speed):
    """The plan against hidden speeds (lower is faster): the ranking of the c fastest and a
    log with, per race, the horses, the result, the horses newly known to be out of the
    top c (with c horses known faster), the horses newly settled at an exact rank, and
    how many candidates are still open."""
    assert a <= b * b, "more groups than a race holds: the winners would need a tournament"
    faster = [set() for _ in range(a)]
    slower = [set() for _ in range(a)]
    log = []
    out = set()
    settled = {}

    def add(x, y):                                   # x beats y, closed transitively
        if y in slower[x]:
            return
        for u in faster[x] | {x}:
            for v in slower[y] | {y}:
                slower[u].add(v)
                faster[v].add(u)

    def run(group, what):
        order = sorted(group, key=lambda x: speed[x])
        for i, x in enumerate(order):
            for y in order[i + 1:]:
                add(x, y)
        gone, placed = [], []
        for x in range(a):
            if x not in out and len(faster[x]) >= c:
                out.add(x)
                gone.append(x)
            if x not in settled and len(faster[x]) + len(slower[x]) == a - 1 and len(faster[x]) < c:
                settled[x] = len(faster[x]) + 1
                placed.append(x)
        open_ = [x for x in range(a) if x not in out and x not in settled]
        log.append(dict(what=what, horses=list(group), order=order, gone=gone, placed=placed, open=open_,
                        faster={x: sorted(faster[x]) for x in gone}))

    groups = [list(range(k, min(k + b, a))) for k in range(0, a, b)]
    for k, g in enumerate(groups):
        run(g, ("group", k))
    if len(groups) > 1:
        run([min(g, key=lambda x: speed[x]) for g in groups], ("winners", None))
    while any(r not in settled.values() for r in range(1, c + 1)):
        pool = [x for x in range(a) if x not in out and x not in settled]
        pool.sort(key=lambda x: (len(faster[x]), -len(slower[x]), x))
        chosen = []
        while len(chosen) < b and pool:
            best = max(pool, key=lambda x: (sum(1 for y in chosen if y not in faster[x] and y not in slower[x]),
                                            -len(faster[x]), len(slower[x]), -x))
            pool.remove(best)
            chosen.append(best)
        run(chosen, ("final", None))
    ranking = [x for r in range(1, c + 1) for x in range(a) if settled.get(x) == r]
    return ranking, log


def names(a, b, log):
    """Horse x is named by its group letter and its place in the group race."""
    out = {}
    for entry in log:
        if entry["what"][0] == "group":
            for i, x in enumerate(entry["order"]):
                out[x] = f"{LETTERS[x // b]}{i + 1}"
    return out


def mulberry32(seed):
    """The explorer's seeded generator (docs/javascripts/explorer.js), so a seed gives the
    same hidden speeds on the page and in the box."""
    state = seed & 0xFFFFFFFF

    def rnd():
        nonlocal state
        state = (state + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((state ^ (state >> 15)) * (1 | state)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) ^ t
        t &= 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def speeds(a, seed):
    """The hidden speeds of the page's examples: 0..a-1 shuffled (Fisher-Yates) with mulberry32."""
    rnd = mulberry32(seed)
    p = list(range(a))
    for i in range(a - 1, 0, -1):
        j = int(rnd() * (i + 1))
        p[i], p[j] = p[j], p[i]
    return p


def race_count(a, b, c, trials=60, seed=43):
    """The most races the plan needed over seeded random speeds."""
    rng = random.Random(seed)
    worst = 0
    for _ in range(trials):
        sp = list(range(a))
        rng.shuffle(sp)
        worst = max(worst, len(plan(a, b, c, sp)[1]))
    return worst


SEED_A, SEED_B = 3, 11


# --- tables ------------------------------------------------------------------------------

def staircase_table(b=B, c=C):
    """Position i in the group whose winner came j-th: i + j horses known faster."""
    lines = ["| מקום בקבוצה \\ המנצח הגיע | " + " | ".join(f"{j + 1}" for j in range(b)) + " |", "|:-:|" + ":-:|" * b]
    for i in range(b):
        cells = []
        for j in range(b):
            n = i + j
            cells.append(f"{RLM}**{n}** ✓" if n < c and n > 0 else f"{RLM}{n} ✗" if n >= c else f"{RLM}0 (מקום 1)")
        lines.append(f"| {RLM}{i + 1} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def what_text(what, b, k_groups):
    kind, k = what
    if kind == "group":
        return f"קבוצה {LETTERS[k]}"
    if kind == "winners":
        return "המנצחים"
    return "המועמדים"


def log_table(a, b, c, seed):
    sp = speeds(a, seed)
    ranking, log = plan(a, b, c, sp)
    nm = names(a, b, log)
    lines = ["| תחרות | מי רץ | התוצאה | נפסלו (ולמה) | נקבעו | עוד פתוחים |", "|:-:|---|---|---|---|:-:|"]
    for r, e in enumerate(log, 1):
        horses = what_text(e["what"], b, ceil(a / b)) + (f" ({len(e['horses'])})" if e["what"][0] != "group" else "")
        if e["what"][0] != "group":
            horses = ", ".join(nm[x] for x in e["horses"])
        result = " > ".join(nm[x] for x in e["order"])
        gone_sorted = sorted(e["gone"], key=lambda x: nm[x])
        if e["what"][0] == "final":
            gone = "; ".join(f"{nm[x]} ({', '.join(nm[y] for y in sorted(e['faster'][x][:c], key=lambda y: nm[y]))}"
                             f"{' ועוד ' + str(len(e['faster'][x]) - c) if len(e['faster'][x]) > c else ''})" for x in gone_sorted)
        else:
            gone = f"{len(gone_sorted)} : " + ", ".join(nm[x] for x in gone_sorted) if gone_sorted else "—"
        rank_of = {x: r + 1 for r, x in enumerate(sorted(range(a), key=lambda z: sp[z]))}
        placed = ", ".join(f"{nm[x]} מקום {rank_of[x]}" for x in sorted(e["placed"], key=lambda x: rank_of[x])) or "—"
        lines.append(f"| {RLM}{r} | {RLM}{horses} | {RLM}{result} | {RLM}{gone or '—'} | {RLM}{placed} | {RLM}{len(e['open'])} |")
    return "\n".join(lines)


EXAMPLES = [(25, 5, 3), (25, 5, 1), (36, 6, 4), (30, 6, 3), (16, 4, 3), (49, 7, 5), (64, 8, 4), (20, 5, 2), (12, 4, 3)]


def examples_table():
    lines = ["| ‏a | ‏b | ‏c | קבוצות | מועמדי המדרגות | תחרויות |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for a, b, c in EXAMPLES:
        n = c * (c + 1) // 2 - 1
        lines.append(f"| {RLM}{a} | {RLM}{b} | {RLM}{c} | {RLM}{ceil(a / b)} | {RLM}{n} | {RLM}**{race_count(a, b, c)}** |")
    return "\n".join(lines)


# --- the figures --------------------------------------------------------------------------

def grid_svg(a, b, c, seed, upto):
    """The horses as a grid after race `upto`: a row per group, ordered by the winners'
    race once it ran, the cells coloured out / candidate / settled, with the number of
    horses known faster in the corner."""
    sp = speeds(a, seed)
    ranking, log = plan(a, b, c, sp)
    nm = names(a, b, log)
    # replay the known-faster counts up to race `upto`
    faster = [set() for _ in range(a)]
    slower = [set() for _ in range(a)]
    for e in log[:upto]:
        o = e["order"]
        for i, x in enumerate(o):
            for y in o[i + 1:]:
                for u in faster[x] | {x}:
                    for v in slower[y] | {y}:
                        slower[u].add(v)
                        faster[v].add(u)
    groups = [list(range(k, min(k + b, a))) for k in range(0, a, b)]
    rows = [sorted(g, key=lambda x: sp[x]) for g in groups]
    winners = [e for e in log[:upto] if e["what"][0] == "winners"]
    if winners:
        rows.sort(key=lambda row: winners[0]["order"].index(row[0]))
    CW, CH, X0, Y0 = 64, 40, 70, 30
    W, H = X0 + b * CW + 10, Y0 + len(rows) * CH + 10
    p = [f'<svg class="figure hr-grid" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.0f}rem" role="img" '
         f'aria-label="הסוסים אחרי {upto} תחרויות : שורה לכל קבוצה לפי סדר המנצחים, תא ירוק נקבע, כחול מועמד, אפור נפסל">']
    for i in range(b):
        p.append(f'<text class="tick" x="{X0 + i * CW + CW / 2:.0f}" y="{Y0 - 10}" text-anchor="middle">{i + 1}</text>')
    for j, row in enumerate(rows):
        label = f"{LETTERS[row[0] // b]}" + (f" ({j + 1})" if winners else "")
        p.append(f'<text class="tick" x="{X0 - 8}" y="{Y0 + j * CH + CH / 2 + 4:.0f}" text-anchor="end">{label}</text>')
        for i, x in enumerate(row):
            nf = len(faster[x])
            cls = "is-placed" if len(faster[x]) + len(slower[x]) == a - 1 and nf < c else "is-out" if nf >= c else "is-cand"
            X, Y = X0 + i * CW, Y0 + j * CH
            p.append(f'<g class="hr-cell {cls}"><rect x="{X + 2}" y="{Y + 2}" width="{CW - 4}" height="{CH - 4}" rx="4"/>'
                     f'<text class="hr-name" x="{X + CW / 2:.0f}" y="{Y + CH / 2 + 5:.0f}" text-anchor="middle">{nm[x]}</text>'
                     f'<text class="hr-count" x="{X + CW - 6}" y="{Y + 13}" text-anchor="end">{nf}</text></g>')
    p.append("</svg>")
    return "".join(p)


def grid_legend():
    return ('<span class="viz-legend"><span><i class="hr-key-placed"></i>נקבע : הדירוג המדויק ידוע</span>'
            '<span><i class="hr-key-cand"></i>מועמד : פחות מ-c מהירים ידועים</span>'
            '<span><i class="hr-key-out"></i>נפסל : לפחות c מהירים ידועים (המספר בפינה)</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [staircase_table(), grid_svg(A, B, C, SEED_A, 7), grid_legend(), log_table(A, B, C, SEED_A),
            grid_svg(A2, B2, C2, SEED_B, 6), log_table(A2, B2, C2, SEED_B), examples_table()]


if __name__ == "__main__":
    print(len(plan(A, B, C, speeds(A, SEED_A))[1]), len(plan(A2, B2, C2, speeds(A2, SEED_B))[1]))
    print("\n\n".join(blocks()))
