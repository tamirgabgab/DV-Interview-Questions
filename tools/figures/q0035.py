#!/usr/bin/env python3
"""Figures of question 0035 (divide the clock by 3, or by an odd N, with a 50% duty cycle).

    python tools/figures/fill.py 35        # put the blocks on the page

blocks() returns, in page order: the schematic of part a (the counter modulo 3, the flop
a on the rising edge, the flop b on the falling edge, the OR gate) and its legend.
tests/0035 checks that the page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from q0030 import text  # noqa: E402


def wire(pts, cls="ink-line", width=1.8):
    d = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline class="{cls}" points="{d}" fill="none" stroke-width="{width}"/>'


def flop(x, y, name, falling=False, title=""):
    """A D flip-flop: a box 70 x 80 at (x, y), D at the top left, Q at the top right, the
    clock triangle at the bottom left (with a bubble for the falling edge)."""
    s = (f'<rect class="box-face" x="{x}" y="{y}" width="70" height="80" rx="4"><title>{title}</title></rect>'
         + text(x + 10, y + 22, "D", anchor="start", size=14) + text(x + 60, y + 22, "Q", anchor="end", size=14)
         + f'<polyline class="ink-line" points="{x},{y + 52} {x + 12},{y + 60} {x},{y + 68}" fill="none" stroke-width="1.5"/>'
         + text(x + 35, y + 100, name, size=15))
    if falling:
        s += f'<circle class="sch-bubble" cx="{x - 5}" cy="{y + 60}" r="5"/>'
    return s


def schematic_svg():
    W, H = 640, 210
    parts = [f'<svg class="figure" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
             f'aria-label="המעגל של סעיף א : מונה מודולו 3 בעליית השעון, השוואה cnt == 2 שנרשמת בפלופ a בעליית '
             f'השעון, פלופ b שדוגם את a בירידת השעון, ושער OR של a ו-b שמוציא את clk_out">']
    # the counter
    parts.append('<rect class="box-face" x="30" y="30" width="110" height="80" rx="4"><title>מונה מודולו 3 : 0, 1, 2, 0, ...</title></rect>')
    parts.append(text(85, 64, "cnt", size=15) + text(85, 86, "mod 3", size=13))
    # the compare
    parts.append('<rect class="box-face" x="175" y="45" width="80" height="34" rx="17"><title>השוואה צירופית</title></rect>')
    parts.append(text(215, 67, "cnt == 2", size=13))
    parts.append(wire([(140, 62), (175, 62)]))
    # flop a (rising) and flop b (falling)
    parts.append(flop(290, 30, "a", title="פלופ בעליית השעון"))
    parts.append(wire([(255, 62), (272, 62), (272, 52), (290, 52)]))
    parts.append(flop(420, 30, "b", falling=True, title="פלופ בירידת השעון"))
    parts.append(wire([(360, 52), (420, 52)]))
    # the OR gate
    gx, gy = 518, 70
    parts.append(f'<path class="box-face" d="M{gx},{gy} Q{gx + 12},{gy + 22} {gx},{gy + 44} Q{gx + 34},{gy + 44} {gx + 46},{gy + 22} '
                 f'Q{gx + 34},{gy} {gx},{gy} Z"><title>שער OR</title></path>')
    parts.append(text(gx + 20, gy + 27, "OR", size=12))
    parts.append(wire([(390, 52), (390, 20), (508, 20), (508, gy + 12), (gx + 5, gy + 12)]))   # a to the gate
    parts.append('<circle class="ink-dot" cx="390" cy="52" r="3.5"/>')
    parts.append(wire([(490, 52), (498, 52), (498, gy + 32), (gx + 5, gy + 32)]))                       # b to the gate
    parts.append(wire([(gx + 46, gy + 22), (W - 6, gy + 22)], "box-path", 3))
    parts.append(text(W - 6, gy + 12, "clk_out", anchor="end", size=14))
    # the clock
    parts.append(wire([(10, 180), (430, 180)], "s1-line", 2))
    parts.append(wire([(85, 180), (85, 110)], "s1-line", 2))
    parts.append(wire([(276, 180), (276, 90), (290, 90)], "s1-line", 2))
    parts.append(wire([(406, 180), (406, 90), (410, 90)], "s1-line", 2))
    parts.append(text(12, 172, "clk", anchor="start", size=14))
    parts.append(text(325, 154, "↑", size=15) + text(455, 154, "↓", size=15))
    return "".join(parts) + "</svg>"


def schematic_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>השעון clk</span><span><i class="box-face"></i>פלופים ולוגיקה</span>'
            '<span><i class="ink"></i>עיגול בכניסת השעון : הפלופ מתעדכן בירידה</span><span><i class="box-path"></i>המוצא clk_out</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [schematic_svg(), schematic_legend()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
