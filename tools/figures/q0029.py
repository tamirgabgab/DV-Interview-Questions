#!/usr/bin/env python3
"""Figures and tables of question 0029 (second, minute and hour hands: how many meetings in a day).

    python tools/figures/fill.py 29        # put the blocks on the page

Time is in seconds from 00:00:00. The hands turn continuously: the second hand once in 60 s,
the minute hand once in 3600 s, the hour hand once in 43200 s (12 hours). A meeting of two
hands is a moment when they point the same way; the day is [0, 86400), so 00:00 counts once.

blocks() returns, in page order: the pairs table, the clock at the first minute-hour meeting
with the 11 meeting places, the minute-hour angle chart over 12 hours, the zoom on the
second hand around 00:01:00, the seconds-past-the-minute chart of the first hour, the table
of the minute-hour meetings, and the interval-count table of part b. tests/0029 checks the
numbers and that the page copies match.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

PERIOD = {"s": 60, "m": 3600, "h": 43200}
HALF, DAY = 43200, 86400
PAIRS = (("s", "m"), ("s", "h"), ("m", "h"))
NAME = {"s": "השניות", "m": "הדקות", "h": "השעות"}
CLS = {"s": "s3", "m": "s1", "h": "ink"}          # the colour of each hand, here and in the explorer


# --- the math ------------------------------------------------------------------------------

def gap(i, j):
    """Time between two meetings of hands i and j: one lap of the faster one, t_i t_j / (t_j - t_i)."""
    ti, tj = PERIOD[i], PERIOD[j]
    return Fr(ti * tj, abs(tj - ti))


def turns(i, L=DAY):
    return Fr(L, PERIOD[i])


def meetings(i, j, L=DAY):
    """The meeting times of hands i and j in [0, L)."""
    T, out, n = gap(i, j), [], 0
    while n * T < L:
        out.append(n * T)
        n += 1
    return out


def angle(i, t):
    """The position of hand i at time t, in turns from 12, in [0, 1)."""
    v = Fr(t) / PERIOD[i]
    return v - math.floor(v)


def events(L=DAY):
    """Every moment in [0, L) when at least two hands meet, with the set of hands there."""
    out = {}
    for i, j in PAIRS:
        for t in meetings(i, j, L):
            out.setdefault(t, set()).update((i, j))
    return dict(sorted(out.items()))


def count(lo_closed, hi_closed, L, i, j):
    """Meetings of i and j on the interval from 0 to L, each end included or not."""
    n = L / gap(i, j)
    inside = math.ceil(n) - 1                       # 0 < t < L
    return inside + lo_closed + (hi_closed and n.denominator == 1)


def dec(v, n=2):
    """A decimal with n digits, rounded half up."""
    q = Fr(v) * 10 ** n
    r = math.floor(q + Fr(1, 2))
    s = f"{r // 10 ** n}.{r % 10 ** n:0{n}d}" if n else f"{r}"
    return s


def clock(t, digits=2):
    """'H:MM:SS.ss' of a time in seconds; the hundredths are rounded but stay inside the
    second (at most .99), so the label and the highlighted second agree (explorer.js too)."""
    t = Fr(t)
    sec = math.floor(t)
    hund = min(math.floor((t - sec) * 100 + Fr(1, 2)), 99)
    h, m, s = sec // 3600, sec // 60 % 60, sec % 60
    base = f"{h}:{m:02d}:{s:02d}"
    return base + (f".{hund:02d}" if digits and (t != sec) else "")


# --- tables --------------------------------------------------------------------------------

def big(n):
    return f"{n:,}"


def pairs_table():
    lines = ["| הזוג | הקפות ביממה | פגישות ביממה | הזמן בין שתי פגישות |", "|---|---|---|---|"]
    for i, j in PAIRS:
        T = gap(i, j)
        n = len(meetings(i, j))
        exact = f"\\tfrac{{{big(T.numerator).replace(',', '{,}')}}}{{{T.denominator}}}"
        lines.append(f"| {NAME[i]} ו{NAME[j]} | ‏{big(int(turns(i)))} ו-{int(turns(j))} | ‏{big(n)} | "
                     f"‏\\( {exact} \\approx {dec(T)} \\) שניות |")
    return "\n".join(lines)


def mh_table():
    T = gap("m", "h")
    lines = ["| ‏\\( k \\) | השעה | הדקות והשעות על השנתה | מחוג השניות על השנתה |", "|---|---|---|---|"]
    for k in range(12):
        t = k * T
        hm = 60 * angle("m", t)
        s = 60 * angle("s", t)
        same = " (שלושתם)" if hm == s else ""
        lines.append(f"| ‏{k} | ‏{clock(t)} | ‏{dec(hm)} | ‏{dec(s)}{same} |")
    return "\n".join(lines)


def counts_table():
    rows = [("סגור, \\( 0 \\le t \\le L \\)", 1, 1, HALF), ("פתוח, \\( 0 < t < L \\)", 0, 0, HALF),
            ("חצי פתוח, \\( 0 \\le t < L \\)", 1, 0, HALF), ("יממה, \\( 0 \\le t < 2L \\)", 1, 0, DAY)]
    lines = ["| הקטע | השניות והדקות | השניות והשעות | הדקות והשעות |", "|---|---|---|---|"]
    for name, lo, hi, L in rows:
        cells = " | ".join(f"‏{big(count(lo, hi, L, i, j))}" for i, j in PAIRS)
        lines.append(f"| {name} | {cells} |")
    return "\n".join(lines)


# --- the clock face ------------------------------------------------------------------------

def face_svg(k=1):
    """The clock at the k-th minute-hour meeting, with the 11 places where they meet."""
    t = k * gap("m", "h")
    size, c, R = 280, 140, 124
    pt = lambda turn, r: (c + r * math.sin(2 * math.pi * turn), c - r * math.cos(2 * math.pi * turn))
    p = [f'<svg class="figure" viewBox="0 0 {size} {size}" style="max-width:17rem" role="img" '
         f'aria-label="שעון בשעה {clock(t)} : מחוג הדקות ומחוג השעות אחד על השני, ומחוג השניות במקום אחר. '
         'הנקודות הן 11 המקומות שבהם הדקות והשעות נפגשים">',
         f'<circle class="clock-face" cx="{c}" cy="{c}" r="{R}"/>']
    for n in range(60):
        r0 = R - (11 if n % 5 == 0 else 5)
        (x0, y0), (x1, y1) = pt(n / 60, r0), pt(n / 60, R)
        cls = "clock-tick5" if n % 5 == 0 else "clock-tick"
        p.append(f'<line class="{cls}" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    for n in range(1, 13):
        x, y = pt(n / 12, R - 26)
        p.append(f'<text class="legend" x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle">{n}</text>')
    for j in range(11):
        x, y = pt(Fr(j, 11), R - 42)
        tj = j * gap("m", "h")
        p.append(f'<circle class="s2-dot" cx="{x:.1f}" cy="{y:.1f}" r="4.5"><title>{clock(tj)}</title></circle>')
    for hand, length, width in (("h", 62, 7), ("m", 96, 4.5), ("s", 108, 2)):
        x, y = pt(angle(hand, t), length)
        p.append(f'<line class="{CLS[hand]}-line" x1="{c}" y1="{c}" x2="{x:.1f}" y2="{y:.1f}" '
                 f'stroke-width="{width}" stroke-linecap="round"/>')
    p.append(f'<circle class="ink-dot" cx="{c}" cy="{c}" r="5"/></svg>')
    return "".join(p)


HANDS = [(CLS["h"], "מחוג השעות"), (CLS["m"], "מחוג הדקות"), (CLS["s"], "מחוג השניות")]


def legend(items):
    return '<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{n}</span>' for c, n in items) + "</span>"


# --- charts --------------------------------------------------------------------------------

def deg(i, t):
    return float(angle(i, t)) * 360


def mh_chart():
    """Minute and hour angle over 12 hours: the minute hand is a saw with 12 teeth, the hour
    hand one slow line, and every crossing is a meeting."""
    c = Chart("זווית מחוג הדקות ומחוג השעות לאורך 12 שעות : 12 נקודות מפגש, הראשונה והאחרונה עם מחוג השניות",
              w=480, h=260, base=226, x_max=12, y_max=360, style="max-width:36rem")
    c.grid_y([0, 90, 180, 270, 360], fmt="{:g}°")
    c.grid_x(range(13))
    for hr in range(12):
        c.segment((hr, 0), (hr + 1, 360), "s1-line", width=2)
    c.segment((0, 0), (12, 360), "ink-line", width=3)
    T = gap("m", "h")
    for k in range(12):
        t = k * T
        triple = k in (0, 11)
        c.dot(float(t) / 3600, float(Fr(360) * k / 11), "s3" if triple else "s2", r=5.5 if triple else 4.5,
              title=f"{clock(t)}" + (" – שלושתם" if triple else ""))
    c.axis()
    return c.svg()


def zoom_chart():
    """The second hand around 00:01:00: it passes the hour hand, then the minute hand."""
    lo, hi = Fr(598, 10), Fr(616, 10)
    c = Chart("הזווית של שלושת המחוגים בין 0:00:59.8 ל-0:01:01.6 : מחוג השניות פוגש את מחוג השעות "
              "ב-60.08 שניות ואת מחוג הדקות ב-61.02 שניות", w=480, h=260, base=226, x_min=float(lo), x_max=float(hi),
              style="max-width:36rem",
              y_max=10)
    c.grid_y([0, 2, 4, 6, 8, 10], fmt="{:g}°")
    c.grid_x([60, 60.5, 61, 61.5])
    c.segment((60, 0), (float(hi), deg("s", hi)), "s3-line", width=2.5)
    c.segment((float(lo), deg("m", lo)), (float(hi), deg("m", hi)), "s1-line", width=3)
    c.segment((float(lo), deg("h", lo)), (float(hi), deg("h", hi)), "ink-line", width=3)
    for i, j, dx, dy in (("s", "h", -24, -12), ("s", "m", -30, -10)):
        t = gap(i, j)
        c.dot(float(t), deg(i, t), "s2", r=5.5, title=f"{clock(t)} : {NAME[i]} ו{NAME[j]}",
              label=f"{dec(t)}", dx=dx, dy=dy)
    c.axis()
    return c.svg()


def offsets_chart():
    """For every minute of the first hour, the second within it at which the second hand
    meets the minute hand and the hour hand."""
    c = Chart("בכל דקה בשעה הראשונה : באיזו שנייה מחוג השניות פוגש את מחוג הדקות ואת מחוג השעות. "
              "בדקה 59 אין פגישה עם מחוג הדקות", w=480, h=260, base=226, x_min=-1, x_max=60, y_max=60,
              style="max-width:36rem")
    c.grid_y([0, 15, 30, 45, 60])
    c.grid_x([0, 10, 20, 30, 40, 50, 59])
    for i, j in (("s", "h"), ("s", "m")):
        for t in meetings(i, j, 3600):
            minute, sec = int(t // 60), t - 60 * (t // 60)
            c.dot(minute, float(sec), CLS[j], r=3.2, title=f"{clock(t)} : {NAME[i]} ו{NAME[j]}")
    c.text(58.6, 40, "בדקה 59 אין", anchor="start", rtl=True)
    c.axis()
    return c.svg()


def blocks():
    """The generated blocks, in page order."""
    return [
        pairs_table(),
        face_svg(),
        legend(HANDS + [("s2", "המקומות שבהם הדקות והשעות נפגשים")]),
        mh_chart(),
        legend(HANDS[:2] + [("s2", "הדקות והשעות נפגשים"), ("s3", "שלושתם, גם עם מחוג השניות")]),
        zoom_chart(),
        legend(HANDS + [("s2", "פגישה")]),
        offsets_chart(),
        legend([("s1", "פגישה עם מחוג הדקות"), ("ink", "פגישה עם מחוג השעות")]),
        mh_table(),
        counts_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
