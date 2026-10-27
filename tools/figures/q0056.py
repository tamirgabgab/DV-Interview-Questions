#!/usr/bin/env python3
"""Figures and tables of question 0056 (ants on a pole: when the last one falls, how many
collisions, when a given ant falls).

    python tools/figures/fill.py 56        # put the blocks on the page

The reference here is independent of the page code: simulate() moves the ants in half
seconds on doubled coordinates (every meeting lands on a grid point, since all distances
stay even), turns both ants at a meeting, and records each ant's fall and every
collision. blocks() returns, in page order: the space-time figure of the page's six ants
(the real ants, and the same lines as ghosts that walk through each other), its legend,
the table of who falls where and when, and the count of the collisions. tests/0056 checks
the page code against these.
"""

L = 100
POS = [10, 25, 40, 60, 75, 90]
DIRS = [1, -1, 1, -1, -1, 1]
RLM = "‏"
NAME = {1: "ימינה", -1: "שמאלה"}


# --- the model ---------------------------------------------------------------------------

def simulate(pos, dirs, length=L):
    """Ants at distinct integer positions (cm), speed 1 cm/s, turning at every meeting.
    Returns (fall time and side of each ant in its order along the pole, the number of
    collisions, the path of each ant as (t, x) points where it starts, turns and falls)."""
    order = sorted(range(len(pos)), key=lambda i: pos[i])
    x = [2 * pos[i] for i in order]                        # doubled: one unit per half second
    d = [dirs[i] for i in order]
    alive = set(range(len(x)))
    fall = [None] * len(x)
    paths = [[(0.0, float(pos[i]))] for i in order]
    hits, tick = 0, 0
    while alive:
        for k in sorted(alive):                            # an ant at an end facing out falls now
            if (x[k] <= 0 and d[k] < 0) or (x[k] >= 2 * length and d[k] > 0):
                fall[k] = (tick / 2, "L" if d[k] < 0 else "R")
                paths[k].append((tick / 2, x[k] / 2))
                alive.discard(k)
        if not alive:
            break
        for k in alive:
            x[k] += d[k]
        tick += 1
        at = {}
        for k in alive:
            at.setdefault(x[k], []).append(k)
        for ks in at.values():
            if len(ks) == 2:                               # two ants meet: both turn
                hits += 1
                for k in ks:
                    d[k] = -d[k]
                    paths[k].append((tick / 2, x[k] / 2))
            assert len(ks) <= 2
    return fall, hits, paths


def ghosts(pos, dirs, length=L):
    """The straight lines: ghost i from (0, p) to its end, at time p or length - p."""
    return [(p, 0 if dd < 0 else length, p if dd < 0 else length - p) for p, dd in zip(pos, dirs)]


# --- blocks ------------------------------------------------------------------------------

def spacetime():
    """Two panels on the same axes: the ants that turn (each ant its own colour) and the
    ghosts that walk through (each ghost its own colour): the same set of lines."""
    fall, hits, paths = simulate(POS, DIRS)
    W, H, pw, x0s, top, sy = 640, 372, 280, (330, 30), 46, 2.9
    sx = pw / L
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    s = (f'<svg class="figure an-fig" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
         'aria-label="מקום מול זמן : מימין הנמלים שמסתובבות, משמאל רוחות שעוברות זו דרך זו. אותם קווים בדיוק, רק הצבעים מתחלפים">')
    for x0, title, ghost in ((x0s[0], "הנמלים : מסתובבות", False), (x0s[1], "רוחות : עוברות זו דרך זו", True)):
        s += f'<text class="an-title" x="{x0 + pw / 2}" y="16" text-anchor="middle" direction="rtl">{title}</text>'
        s += f'<line class="an-pole" x1="{x0}" y1="{top}" x2="{x0 + pw}" y2="{top}"/>'
        for v in (0, 50, 100):
            s += f'<text class="tick" x="{x0 + v * sx}" y="{top - 8}" text-anchor="middle">{v}</text>'
        for t in (25, 50, 75, 100):
            y = top + t * sy
            s += f'<line class="an-grid" x1="{x0}" y1="{y}" x2="{x0 + pw}" y2="{y}"/>'
            s += f'<text class="tick" x="{x0 - 4}" y="{y + 4}" text-anchor="end">{t}s</text>'
        if ghost:
            for i, (p, end, t) in enumerate(ghosts(POS, DIRS)):
                s += (f'<line class="an-path an-c{i}" x1="{f(x0 + p * sx)}" y1="{top}" x2="{f(x0 + end * sx)}" y2="{f(top + t * sy)}">'
                      f'<title>ghost from {p}: off at {end} after {t} s</title></line>')
        else:
            for k, pts in enumerate(paths):
                d = " ".join(f"{f(x0 + x * sx)},{f(top + t * sy)}" for t, x in pts)
                s += f'<polyline class="an-path an-c{k}" points="{d}"><title>ant {k + 1}: falls at {fall[k][0]:g} s</title></polyline>'
        for i, p in enumerate(sorted(POS)):
            s += f'<circle class="an-start an-c{i}" cx="{f(x0 + p * sx)}" cy="{top}" r="4.5"/>'
    s += f'<text class="legend" x="{W - 8}" y="{H - 6}" text-anchor="end">x (cm) →   t (s) ↓</text>'
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="an-key-path"></i>קו לכל נמלה : מקום (אופקי) מול זמן (למטה)</span>'
            '<span><i class="an-key-start"></i>המקום בהתחלה</span></span>')


def fall_table():
    fall, hits, paths = simulate(POS, DIRS)
    order = sorted(range(len(POS)), key=lambda i: POS[i])
    rows = ["| הנמלה (משמאל) | מתחילה ב- | הולכת | נופלת מהצד | אחרי (שניות) |", "|:-:|:-:|:-:|:-:|:-:|"]
    for k, i in enumerate(order):
        t, side = fall[k]
        rows.append(f"| {RLM}{k + 1} | {RLM}{POS[i]} | {NAME[DIRS[i]]} | {'השמאלי (0)' if side == 'L' else 'הימני (100)'} | {RLM}{t:g} |")
    return "\n".join(rows)


def pairs_table():
    """Each ant going left meets every ant going right that starts to its left."""
    order = sorted(range(len(POS)), key=lambda i: POS[i])
    rows = ["| נמלה שהולכת שמאלה | הנמלות שהולכות ימינה משמאלה | התנגשויות |", "|:-:|:-:|:-:|"]
    total = 0
    for k, i in enumerate(order):
        if DIRS[i] < 0:
            rs = [POS[j] for j in order[:k] if DIRS[j] > 0]
            total += len(rs)
            rows.append(f"| {RLM}{POS[i]} | {RLM}{', '.join(map(str, rs)) or '—'} | {RLM}{len(rs)} |")
    rows.append(f"| **סך הכול** | | **{RLM}{total}** |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [spacetime(), legend(), pairs_table(), fall_table()]


if __name__ == "__main__":
    print(simulate(POS, DIRS)[:2])
    print("\n\n".join(blocks()))
