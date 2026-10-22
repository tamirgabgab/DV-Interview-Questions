#!/usr/bin/env python3
"""Work table and log-scale chart of question 0010 (valid parentheses).

    python tools/figures/q0010.py > /tmp/q0010.html

Work = characters read. The pair-removal solution reads the whole remaining string on
every pass; the stack reads every character once. Input: n/2 times "(" then n/2 times ")".
"""

import html
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepper import stepper  # noqa: E402

SIZES = [10, 100, 1_000, 10_000, 100_000]
PAIRS = {")": "(", "]": "[", "}": "{"}
# Hebrew names of the bracket kinds for the captions: a lone bracket glyph inside Hebrew text
# is mirrored by the bidi algorithm, so the captions name the brackets instead of showing them
KIND = {"(": "עגול", ")": "עגול", "[": "מרובע", "]": "מרובע", "{": "מסולסל", "}": "מסולסל"}


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
    lines = ["| אורך \\( n \\) | מעברים בפתרון הפשוט | תווים שנקראו : פשוט | תווים שנקראו : מחסנית | פי כמה |",
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


def stack_frame(text, pos, stack, status=None):
    """One frame: the input with the character at `pos` marked, and the stack on the right.
    status: None (reading), "ok" (valid at the end), "bad" (mismatch at `pos`)."""
    cell, gap, x0, y0 = 40, 6, 16, 36
    w = max(360, x0 + len(text) * (cell + gap) + 150)
    p = [f'<svg class="figure" viewBox="0 0 {w} 190" style="max-width:{w / 16:.0f}rem" role="img" aria-label="מצב המחסנית">']
    for i, ch in enumerate(text):
        x = x0 + i * (cell + gap)
        cls = "st-done" if i < pos else ("st-bad" if status == "bad" and i == pos else "st-cur" if i == pos and status is None else "st-cell")
        p.append(f'<rect class="{cls}" x="{x}" y="{y0}" width="{cell}" height="{cell}" rx="5"/>'
                 f'<text class="st-text" x="{x + cell / 2}" y="{y0 + 27}" text-anchor="middle">{html.escape(ch)}</text>')
        if i == pos and status != "ok":
            p.append(f'<path class="s2-fill" d="M{x + cell / 2 - 7},{y0 + cell + 16} L{x + cell / 2 + 7},{y0 + cell + 16} L{x + cell / 2},{y0 + cell + 6} z"/>')
    p.append(f'<text class="st-small" x="{x0}" y="{y0 - 12}">input</text>')
    sx, sb, sh = w - 70, 176, 34
    p.append(f'<text class="st-small" x="{sx + 22}" y="{y0 - 12}" text-anchor="middle">stack</text>')
    p.append(f'<line class="ink-line" x1="{sx - 6}" x2="{sx + 50}" y1="{sb}" y2="{sb}" stroke-width="2"/>')
    for j, ch in enumerate(stack):
        y = sb - (j + 1) * (sh + 4)
        top = j == len(stack) - 1
        cls = ("st-bad" if status == "bad" else "st-top") if top else "st-stack"
        p.append(f'<rect class="{cls}" x="{sx}" y="{y}" width="44" height="{sh}" rx="5"/>'
                 f'<text class="st-text" x="{sx + 22}" y="{y + 24}" text-anchor="middle">{html.escape(ch)}</text>')
    if not stack:
        p.append(f'<text class="st-small" x="{sx + 22}" y="{sb - 14}" text-anchor="middle">empty</text>')
    p.append("</svg>")
    return "".join(p)


def stack_stepper(text):
    """Frames of the stack solution on `text`, one per character, plus start and verdict."""
    name = lambda ch: f"{'סוגר' if ch in PAIRS else 'פותח'} {KIND[ch]}"
    frames = [(stack_frame(text, -1, []), "לפני הקריאה : המחרוזת שבאיור, והמחסנית ריקה.")]
    stack = []
    for i, ch in enumerate(text):
        if ch in PAIRS:
            if not stack:
                frames.append((stack_frame(text, i, stack, "bad"),
                               f"תו {i + 1} הוא {name(ch)}, אבל המחסנית ריקה. אין מה לסגור : המחרוזת לא תקינה ✗"))
                return stepper(frames, f"המחסנית תו אחרי תו על {text}")
            if stack[-1] != PAIRS[ch]:
                frames.append((stack_frame(text, i, stack, "bad"),
                               f"תו {i + 1} הוא {name(ch)}, אבל בראש המחסנית {name(stack[-1])} ולא {name(PAIRS[ch])}. "
                               f"סדר הסגירה שגוי : המחרוזת לא תקינה ✗"))
                return stepper(frames, f"המחסנית תו אחרי תו על {text}")
            stack.pop()
            frames.append((stack_frame(text, i, stack),
                           f"תו {i + 1} הוא {name(ch)}. בראש המחסנית {name(PAIRS[ch])}, מתאים, ולכן הוא מוצא מהמחסנית."))
        else:
            stack.append(ch)
            frames.append((stack_frame(text, i, stack),
                           f"תו {i + 1} הוא {name(ch)}, ולכן נדחף למחסנית."))
    verdict = ("סוף המחרוזת והמחסנית ריקה : כל פותח נסגר, המחרוזת תקינה ✓" if not stack
               else f"סוף המחרוזת, אבל במחסנית נשארו {len(stack)} פותחים שלא נסגרו : המחרוזת לא תקינה ✗")
    frames.append((stack_frame(text, len(text), stack, "ok" if not stack else "bad"), verdict))
    return stepper(frames, f"המחסנית תו אחרי תו על {text}")


if __name__ == "__main__":
    print(table(), "\n")
    print(chart(), "\n")
    print(stack_stepper("{[()]}"), "\n")
    print(stack_stepper("([)]"))
