#!/usr/bin/env python3
"""Figures of question 0076 (a strictly increasing f on the positive integers with
f(f(n)) = 3n).

    python tools/figures/fill.py 76        # put the blocks on the page

blocks() returns them in page order: for part a the ladder 9..18 -> 18..27 (nine steps,
a rise of nine, so f rises by one at each step) and its legend; for part b the graph of f
up to 27 (slope 1 on [3^k, 2*3^k], slope 3 on [2*3^k, 3^(k+1)], the anchors and the line
sqrt(3) n) and its legend, and the table of the base-3 rule. tests/0076 checks that the
page copies match and recomputes every value.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402


def f(n: int) -> int:
    """The unique strictly increasing f with f(f(n)) = 3n (part b)."""
    p = 1
    while 3 * p <= n:
        p *= 3
    return n + p if n <= 2 * p else 3 * n - 3 * p


def base3(n: int) -> str:
    s = ""
    while n:
        s = str(n % 3) + s
        n //= 3
    return s or "0"


def anchors(top: int) -> list[int]:
    """3^k and 2*3^k up to top: 1, 2, 3, 6, 9, 18, 27, ..."""
    out, p = [], 1
    while p <= top:
        out += [p] + ([2 * p] if 2 * p <= top else [])
        p *= 3
    return out


LADDER = range(9, 19)        # part a: f(9) = 18 to f(18) = 27
PICK = 14


def ladder() -> str:
    """Two rows: n = 9..18 above, f(n) = 18..27 below, a line from each n to its value.
    The ends are known from the chain, the line of 14 is the answer."""
    w, h, x0, dx, yt, yb = 640, 168, 92, 54, 34, 136
    s = [f'<svg class="figure" viewBox="0 0 {w} {h}" style="max-width:40rem" role="img" '
         'aria-label="סעיף א : המספרים 9 עד 18 למעלה, והערכים 18 עד 27 למטה. הקצוות ידועים מהשרשרת, '
         'תשעה צעדים ועלייה של תשע, ולכן כל n עולה ל-n + 9, ו-14 עולה ל-23">']
    s.append(f'<text class="legend" x="{x0 - 30}" y="{yt + 6}" text-anchor="end" style="font-size:17px">n</text>')
    s.append(f'<text class="legend" x="{x0 - 30}" y="{yb + 6}" text-anchor="end" style="font-size:17px">f(n)</text>')
    for i, n in enumerate(LADDER):
        x = x0 + i * dx
        end = n in (LADDER[0], LADDER[-1])
        cls = "s2" if n == PICK else "s1" if end else "ink"
        width = 3 if n == PICK or end else 1.4
        s.append(f'<line class="{cls}-line" x1="{x}" y1="{yt + 14}" x2="{x}" y2="{yb - 20}" stroke-width="{width}"/>')
        s.append(f'<circle class="{cls}-dot" cx="{x}" cy="{yt}" r="{6 if cls != "ink" else 4.5}">'
                 f'<title>n = {n}</title></circle>')
        s.append(f'<circle class="{cls}-dot" cx="{x}" cy="{yb}" r="{6 if cls != "ink" else 4.5}">'
                 f'<title>f({n}) = {f(n)}</title></circle>')
        s.append(f'<text class="tick" x="{x}" y="{yt - 13}" text-anchor="middle" style="font-size:16px">{n}</text>')
        s.append(f'<text class="tick" x="{x}" y="{yb + 26}" text-anchor="middle" style="font-size:16px">{f(n)}</text>')
    return "".join(s) + "</svg>"


def ladder_legend() -> str:
    return ('<span class="viz-legend"><span><i class="s1"></i>ידוע מהשרשרת : '
            '‏\\( f(9) = 18 \\), ‏\\( f(18) = 27 \\)</span><span><i class="ink"></i>נקבע בספירה : כל צעד עולה ב-1</span>'
            '<span><i class="s2"></i>‏\\( f(14) = 23 \\)</span></span>')


TOP = 27


def graph() -> str:
    """f(n) for n = 1..27: the slope-1 pieces, the slope-3 pieces, the anchors, sqrt(3) n."""
    c = Chart("סעיף ב : הגרף של f עד 27. מ-3 בחזקת k עד פעמיים 3 בחזקת k הגרף עולה בשיפוע 1, "
              "ומשם עד 3 בחזקת k + 1 בשיפוע 3; העוגנים מסומנים, והקו המקווקו הוא שורש 3 כפול n",
              w=640, h=300, x0=46, base=262, top=14, x_max=TOP + 0.6, x_min=0, y_max=2 * TOP, y_min=0,
              style="max-width:40rem")
    c.grid_y([0, 9, 18, 27, 36, 45, 54])
    c.grid_x(anchors(TOP))
    c.axis()
    c.path([(0, 0), (TOP + 0.6, math.sqrt(3) * (TOP + 0.6))], "ink-line", width=1.5, extra=' stroke-dasharray="6 4"')
    a = anchors(TOP)
    for lo, hi in zip(a, a[1:]):
        slope = (f(hi) - f(lo)) // (hi - lo)
        c.segment((lo, f(lo)), (hi, f(hi)), "s1-line" if slope == 1 else "s3-line", width=2.5)
    for n in range(1, TOP + 1):
        if n in a:
            continue
        p = 1
        while 3 * p <= n:
            p *= 3
        c.dot(n, f(n), "s1" if n <= 2 * p else "s3", r=3.2, title=f"f({n}) = {f(n)}")
    for n in a:
        c.dot(n, f(n), "s2", r=5, title=f"f({n}) = {f(n)}")
    c.text(TOP - 2.2, math.sqrt(3) * (TOP - 2.2) + 2.2, "√3 · n", cls="legend", anchor="end", dy=-6)
    return c.svg()


def graph_legend() -> str:
    return ('<span class="viz-legend"><span><i class="s1"></i>‏\\( 3^k \\le n \\le 2 \\cdot 3^k \\) : שיפוע 1</span>'
            '<span><i class="by-bfs"></i>‏\\( 2 \\cdot 3^k \\le n \\le 3^{k+1} \\) : שיפוע 3</span>'
            '<span><i class="s2"></i>העוגנים \\( 3^k \\) ו-\\( 2 \\cdot 3^k \\)</span>'
            '<span><i class="ink-dash"></i>‏\\( \\sqrt{3}\\,n \\), להשוואה</span></span>')


BASE3_EXAMPLES = [5, 7, 14, 23, 2027]


def base3_table() -> str:
    lines = ["| ‏\\( n \\) | בבסיס 3 | הספרה המובילה | ‏\\( f(n) \\) בבסיס 3 | ‏\\( f(n) \\) |", "|---|---|---|---|---|"]
    for n in BASE3_EXAMPLES:
        b, fb = base3(n), base3(f(n))
        rule = "1 הופכת ל-2" if b[0] == "1" else "2 הופכת ל-1, ו-0 בסוף"
        lines.append(f'| {n} | <span dir="ltr">{b}</span> | {rule} | <span dir="ltr">{fb}</span> | {f(n)} |')
    return "\n".join(lines)


def blocks():
    """The generated blocks, in page order."""
    return [ladder(), ladder_legend(), graph(), graph_legend(), base3_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
