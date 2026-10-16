#!/usr/bin/env python3
"""Work table and log-scale chart of question 0010 (valid parentheses).

    python tools/figures/q0010.py > /tmp/q0010.html

Work = characters read. The pair-removal solution reads the whole remaining string on
every pass; the stack reads every character once. Input: n/2 times "(" then n/2 times ")".
"""

import math

SIZES = [10, 100, 1_000, 10_000, 100_000]


def brute_work(s):
    passes = work = 0
    while "()" in s or "[]" in s or "{}" in s:
        passes += 1
        work += len(s)
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return passes, work


def rows():
    out = []
    for n in SIZES:
        passes, work = brute_work("(" * (n // 2) + ")" * (n // 2))
        out.append((n, passes, work, n))
    return out


def table():
    lines = ["| אורך \\( n \\) | מעברים בפתרון הפשוט | תווים שנקראו: פשוט | תווים שנקראו: מחסנית | פי כמה |",
             "|---|---|---|---|---|"]
    for n, passes, work, stack in rows():
        lines.append(f"| {n:,} | {passes:,} | {work:,} | {stack:,} | {work // stack:,} |")
    return "\n".join(lines)


def chart():
    w, h, x0, top, base = 640, 280, 64, 16, 240
    lo, hi = 0, 10                                   # 10^0 .. 10^10
    y = lambda v: base - (base - top) * (math.log10(v) - lo) / (hi - lo)
    data = rows()
    slot = (w - x0 - 10) / len(data)
    bw = slot * 0.3
    p = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}" role="img" '
         f'aria-label="מספר התווים שכל פתרון קורא, בסקאלה לוגריתמית">']
    for e in range(lo, hi + 1):
        p.append(f'<line class="grid" x1="{x0}" x2="{w - 10}" y1="{y(10 ** e):.1f}" y2="{y(10 ** e):.1f}"/>'
                 f'<text class="tick" x="{x0 - 8}" y="{y(10 ** e) + 4:.1f}" text-anchor="end">10<tspan dy="-5" font-size="9">{e}</tspan></text>')
    for i, (n, _, work, stack) in enumerate(data):
        cx = x0 + slot * (i + 0.5)
        for value, dx, cls, name in [(work, -bw, "by-enum", "pair removal"), (stack, 0, "by-multiples", "stack")]:
            p.append(f'<rect class="bar {cls}" x="{cx + dx:.1f}" y="{y(value):.1f}" width="{bw:.1f}" '
                     f'height="{base - y(value):.1f}"><title>n = {n:,}: {name} reads {value:,}</title></rect>')
        p.append(f'<text class="tick" x="{cx:.1f}" y="{base + 18}" text-anchor="middle">n = {n:,}</text>')
    p.append(f'<line class="axis" x1="{x0}" x2="{w - 10}" y1="{base}" y2="{base}"/></svg>')
    return "".join(p)


if __name__ == "__main__":
    print(table(), "\n")
    print(chart())
