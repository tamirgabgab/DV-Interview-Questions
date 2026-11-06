#!/usr/bin/env python3
"""Figures and tables of question 0088: differences in a circle (the Ducci sequence).

    python tools/figures/fill.py 88        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the tests compare the
two): a step replaces x_i by |x_i - x_{i+1}| (indices around the circle), and an orbit is
followed with a dict of the states already seen. Mod 2 a step is x_i XOR x_{i+1}; on n-bit
integers that is b ^ rotate(b). The same model is in the box (docs/javascripts/explorer/ducci.js).
"""

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401

START = (2, 6, 11, 4)          # the statement and part a
TRIB = (0, 7, 20, 44)          # a long start for n = 4 (built from Tribonacci numbers)
TRIB_BIG = (0, 1705, 4841, 10609)
N3 = (1, 2, 3)                 # part c: enters a cycle of length 3


# --- the model -----------------------------------------------------------------------------------

def step(v):
    n = len(v)
    return tuple(abs(v[i] - v[(i + 1) % n]) for i in range(n))


def orbit(v):
    """(tail, period, states): the steps before the cycle, its length, and every state from
    the start to the last one before the cycle closes."""
    seen, seq = {}, []
    v = tuple(v)
    while v not in seen:
        seen[v] = len(seq)
        seq.append(v)
        v = step(v)
    return seen[v], len(seq) - seen[v], seq


def steps_to_zero(v):
    """The steps until all are zero, or None if the orbit never gets there."""
    tail, period, seq = orbit(v)
    return tail if period == 1 and not any(seq[tail]) else None


def power_of_two(n):
    return n > 0 and n & (n - 1) == 0


def bound(v):
    """The bound of part b: n steps make every entry even, and log2 of the max halvings."""
    return len(v) * max(v).bit_length()


def parity_step(b, n):
    """One step mod 2 on an n-bit integer: bit i is x_i XOR x_{i+1}."""
    mask = (1 << n) - 1
    return (b ^ ((b >> 1) | (b << (n - 1)))) & mask


def single_one_rows(n, t):
    """The parity pattern of a single 1 (at x_n) after 0..t rounds, as lists of bits x_1..x_n:
    row t is row t of Pascal's triangle mod 2, growing to the left and wrapping around."""
    rows, v = [], tuple(1 if i == n - 1 else 0 for i in range(n))   # the 1 on the right: x_n
    for _ in range(t + 1):
        rows.append(list(v))
        v = step(v)
    return rows


def cycle_lengths(n):
    """Every cycle length of the n-number game (from the 0/1 starts, which give all of them)."""
    return sorted({orbit(v)[1] for v in itertools.product((0, 1), repeat=n)})


# --- the statement: four numbers on a circle, the differences on the edges -----------------------

def statement_figure():
    W, H, cx, cy, R = 300, 236, 150, 116, 84
    pts = [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)]   # clockwise from the top
    nxt = step(START)
    out = [f'<svg class="figure du-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
           f'aria-label="ארבעה מספרים על מעגל, בכיוון השעון מלמעלה : {", ".join(map(str, START))}. '
           f'על כל צלע ההפרש בין שני המספרים שבקצותיה : {", ".join(map(str, nxt))}. אלה המספרים של הסיבוב הבא">']
    out.append(f'<circle class="du-ring" cx="{cx}" cy="{cy}" r="{R}"/>')
    for i in range(4):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 4]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        out.append(f'<line class="du-chord" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        out.append(f'<rect class="du-diff-bg" x="{mx - 15:.1f}" y="{my - 12:.1f}" width="30" height="24" rx="6"/>')
        out.append(f'<text class="du-diff" x="{mx:.1f}" y="{my + 5:.1f}" text-anchor="middle">{nxt[i]}</text>')
    for (x, y), v in zip(pts, START):
        out.append(f'<circle class="du-node" cx="{x}" cy="{y}" r="20"/>')
        out.append(f'<text class="du-val" x="{x}" y="{y + 6}" text-anchor="middle">{v}</text>')
    out.append("</svg>")
    return "".join(out)


def statement_legend():
    return ('<span class="viz-legend"><span><i class="du-key-node"></i>מספר על המעגל</span>'
            '<span><i class="du-key-diff"></i>ההפרש בין שני שכנים : המספר שיחליף אותם בסיבוב הבא</span></span>')


# --- part a: the run of 2, 6, 11, 4 ----------------------------------------------------------------

def trace_table(v=START):
    _, _, seq = orbit(v)
    rows = ["| סיבוב | מספר 1 | מספר 2 | מספר 3 | מספר 4 | הכי גדול | כמה אי-זוגיים |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for t, s in enumerate(seq):
        rows.append(f"| {t} | " + " | ".join(str(x) for x in s) + f" | {max(s)} | {sum(x % 2 for x in s)} |")
    return "\n".join(rows)


# --- part b: a single 1 mod 2, on 8 numbers and on 6 ---------------------------------------------

def bits_panel(n, t, x0, y0, cell, title):
    rows = single_one_rows(n, t)
    out = [f'<text class="du-panel" x="{x0 + n * cell / 2:.1f}" y="{y0 - 10}" text-anchor="middle">{title}</text>']
    for r, row in enumerate(rows):
        y = y0 + r * cell
        out.append(f'<text class="du-tick" x="{x0 - 8}" y="{y + cell * 0.68:.1f}" text-anchor="end">{r}</text>')
        for i, b in enumerate(row):
            cls = "du-one" if b else "du-zero"
            out.append(f'<rect class="{cls}" x="{x0 + i * cell + 1}" y="{y + 1}" width="{cell - 2}" height="{cell - 2}" rx="2"/>')
        if not any(row):
            out.append(f'<rect class="du-dead" x="{x0 - 1}" y="{y}" width="{n * cell + 2}" height="{cell}" rx="3"/>')
    return out


def bits_figure():
    t, cell = 8, 18
    W, H = 400, 50 + (t + 1) * cell + 10
    out = [f'<svg class="figure du-bits" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
           f'aria-label="הזוגיות של 1 בודד בין אפסים, סיבוב אחרי סיבוב. מימין 8 מספרים : אחרי 8 סיבובים הכל זוגי. '
           f'משמאל 6 מספרים : אף פעם לא הכל זוגי">']
    out += bits_panel(8, t, 230, 40, cell, "n = 8")
    out += bits_panel(6, t, 50, 40, cell, "n = 6")
    out.append("</svg>")
    return "".join(out)


def bits_legend():
    return ('<span class="viz-legend"><span><i class="du-key-one"></i>מספר אי-זוגי</span>'
            '<span><i class="du-key-zero"></i>מספר זוגי</span><span><i class="du-key-dead"></i>שורה שכולה זוגית</span>'
            '<span>בכל שורה הזוגיות אחרי עוד סיבוב, והמספר ליד השורה הוא מספר הסיבובים. מימין 8 מספרים, משמאל 6</span></span>')


# --- part c: a cycle, and the table of cycle lengths ------------------------------------------------

def cycle_table(v=N3):
    tail, period, seq = orbit(v)
    rows = ["| סיבוב | מספר 1 | מספר 2 | מספר 3 | הערה |", "|:-:|:-:|:-:|:-:|---|"]
    for t, s in enumerate(seq + [step(seq[-1])]):
        note = "התחלה" if t == 0 else "נכנסים למחזור" if t == tail else f"חוזר למצב של סיבוב {tail}" if t == len(seq) else ""
        rows.append(f"| {t} | " + " | ".join(str(x) for x in s) + f" | {note} |")
    return "\n".join(rows)


def lengths_table(lo=3, hi=10):
    rows = ["| ‏n | חזקה של 2 | אורכי המחזורים, חוץ מהאפסים | ההתחלה של 1 אחד ואפסים |", "|:-:|:-:|---|---|"]
    for n in range(lo, hi + 1):
        lens = [x for x in cycle_lengths(n) if x > 1]
        one = orbit(tuple(1 if i == 0 else 0 for i in range(n)))
        single = "מגיעים לאפסים" if power_of_two(n) else f"מחזור באורך {one[1]}"
        cyc = "אין, תמיד מגיעים לאפסים" if not lens else " ו-".join(str(x) for x in lens)
        rows.append(f"| {n} | {'כן' if power_of_two(n) else 'לא'} | {cyc} | {single} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        statement_figure(),
        statement_legend(),
        trace_table(),
        bits_figure(),
        bits_legend(),
        cycle_table(),
        lengths_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
