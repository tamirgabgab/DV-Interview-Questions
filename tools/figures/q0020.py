#!/usr/bin/env python3
"""Figures and tables of question 0020 (PCIe: all the completion splits of a read).

    python tools/figures/q0020.py > /tmp/q0020.html

Prints, in page order: the parameters figure (one request over the RCB grid, the MPS reach
of the first completion and one legal split); the map of every split of the example
(0x1010, 256 bytes, RCB 64, MPS 256) grouped by the number of completions; the table with
the same splits; the same map with the splits that MPS = 128 rules out faded; and the
table of the MPS = 128 case. The splits come from the page's own Python code (the page is
the single source of truth); tests/0020 checks that the page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extract_code import load_python  # noqa: E402

completion_splits = load_python(20)["completion_splits"]

ADDR, LEN, RCB, MPS = 0x1010, 256, 64, 256
BASE = 0x1000                 # left edge of the figures
SPAN = 320                    # bytes shown: 0x1000 .. 0x1140
RLM = "‏"


def role(i, n):
    return "one" if n == 1 else "first" if i == 0 else "last" if i == n - 1 else "mid"


def plus(split):
    return "+".join(str(s) for s in split)


def segments(split, start=ADDR):
    """(role, start address, size) of every completion of a split."""
    out, pos = [], start
    for i, size in enumerate(split):
        out.append((role(i, len(split)), pos, size))
        pos += size
    return out


# ---------------------------------------------------------------- the parameters figure

def params_svg(mps=128, split=(48, 128, 80)):
    x0, x1 = 40, 600
    sc = (x1 - x0) / SPAN

    def x(addr):
        return x0 + (addr - BASE) * sc

    p = ['<svg class="figure cs-fig" viewBox="0 0 640 196" style="max-width:40rem" role="img" '
         'aria-label="בקשת קריאה של 256 בתים מכתובת 0x1010 על רשת גבולות ה-RCB, טווח ה-MPS של '
         'ה-Completion הראשון, ופיצול חוקי אחד: 48, 128, 80">']
    p.append('<defs><marker id="cs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             'markerHeight="6" orient="auto-start-reverse"><path class="ink-fill" d="M0,0 L10,5 L0,10 z"/>'
             '</marker></defs>')
    # RCB grid
    for off in range(0, SPAN + 1, RCB):
        xx = x(BASE + off)
        p.append(f'<line class="cs-rcb" x1="{xx:.1f}" y1="26" x2="{xx:.1f}" y2="150"/>')
        p.append(f'<text class="coord halo" x="{xx:.1f}" y="18" text-anchor="middle">0x{BASE + off:X}</text>')
    # the request
    rs, re_ = x(ADDR), x(ADDR + LEN)
    p.append(f'<line class="cs-req" x1="{rs:.1f}" y1="30" x2="{rs:.1f}" y2="150"/>')
    p.append(f'<line class="cs-req" x1="{re_:.1f}" y1="30" x2="{re_:.1f}" y2="150"/>')
    # MPS reach of the first completion
    reach = x(ADDR + mps)
    p.append(f'<line class="ink-line" x1="{rs:.1f}" y1="48" x2="{reach - 1:.1f}" y2="48" stroke-width="1.6" '
             f'marker-end="url(#cs-arrow)"/>')
    p.append(f'<text class="legend halo" x="{(rs + reach) / 2:.1f}" y="42" text-anchor="middle">MPS = {mps}</text>')
    for off in (64, 128):          # boundaries the first completion may end at
        p.append(f'<circle class="cs-can" cx="{x(BASE + off):.1f}" cy="48" r="4.5"><title>'
                 f'0x{BASE + off:X}: a legal end of the first completion</title></circle>')
    p.append(f'<text class="cs-no" x="{x(BASE + 192):.1f}" y="52.5" text-anchor="middle">✕</text>')
    # one split
    for r, start, size in segments(split):
        a, b = x(start), x(start + size)
        p.append(f'<rect class="cs-{r}" x="{a:.1f}" y="62" width="{b - a:.1f}" height="30" rx="3">'
                 f'<title>0x{start:X}–0x{start + size - 1:X}: {size} bytes</title></rect>')
        p.append(f'<text class="cs-size" x="{(a + b) / 2:.1f}" y="82" text-anchor="middle">{size}</text>')
        p.append(f'<text class="tick" x="{(a + b) / 2:.1f}" y="108" text-anchor="middle">{r}</text>')
    # RCB bracket
    ya = 128
    p.append(f'<line class="ink-line" x1="{x(BASE + 64) + 1:.1f}" y1="{ya}" x2="{x(BASE + 128) - 1:.1f}" y2="{ya}" '
             f'stroke-width="1.6" marker-start="url(#cs-arrow)" marker-end="url(#cs-arrow)"/>')
    p.append(f'<text class="legend halo" x="{x(BASE + 96):.1f}" y="{ya - 6}" text-anchor="middle">RCB = {RCB}</text>')
    # request bracket
    yb = 160
    p.append(f'<line class="ink-line" x1="{rs + 1:.1f}" y1="{yb}" x2="{re_ - 1:.1f}" y2="{yb}" stroke-width="1.6" '
             f'marker-start="url(#cs-arrow)" marker-end="url(#cs-arrow)"/>')
    p.append(f'<text class="legend halo" x="{(rs + re_) / 2:.1f}" y="{yb + 18}" text-anchor="middle">'
             f'request: {LEN} B from 0x{ADDR:X} (≤ MRRS)</text>')
    p.append("</svg>")
    return "".join(p)


def params_legend():
    return ('<span class="viz-legend">'
            '<span><i class="cs-rcb"></i>גבול RCB: כאן מותר לחתוך</span>'
            '<span><i class="cs-req"></i>תחילת הבקשה וסופה</span>'
            '<span><i class="cs-can"></i>סוף אפשרי ל-Completion הראשון</span>'
            '<span><i class="cs-first"></i>ראשון: עד גבול RCB</span>'
            '<span><i class="cs-mid"></i>אמצעי: כפולה של RCB</span>'
            '<span><i class="cs-last"></i>אחרון: עד סוף הבקשה</span>'
            '</span>')


# ---------------------------------------------------------------- the map of all splits

def splits_map_svg(splits, mps_filter=None):
    """Every split as a row of segments over the address axis, grouped by the number of
    completions. With `mps_filter`, splits that have a completion above it are faded and
    the offending completions are marked."""
    x0, x1 = 128, 612
    sc = (x1 - x0) / SPAN
    row, gap, head = 22, 6, 24

    def x(addr):
        return x0 + (addr - BASE) * sc

    groups = {}
    for s in splits:
        groups.setdefault(len(s), []).append(s)
    height = 30 + sum(head + len(g) * (row + gap) for g in groups.values()) + 4
    label = ("כל הפיצולים החוקיים של הבקשה, שורה לכל פיצול, מקובצים לפי מספר ה-Completions"
             if mps_filter is None else
             f"אותם פיצולים כש-MPS = {mps_filter}: הפיצולים שיש בהם Completion גדול מ-{mps_filter} מסומנים ודהויים")
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 {height}" style="max-width:40rem" role="img" '
         f'aria-label="{label}">']
    for off in range(0, SPAN + 1, RCB):
        xx = x(BASE + off)
        p.append(f'<line class="cs-rcb" x1="{xx:.1f}" y1="24" x2="{xx:.1f}" y2="{height - 4}"/>')
        p.append(f'<text class="coord halo" x="{xx:.1f}" y="16" text-anchor="middle">0x{BASE + off:X}</text>')
    for xx in (x(ADDR), x(ADDR + LEN)):
        p.append(f'<line class="cs-req" x1="{xx:.1f}" y1="24" x2="{xx:.1f}" y2="{height - 4}"/>')
    y = 30
    for n in sorted(groups):
        g = groups[n]
        word = "completion" if n == 1 else "completions"
        p.append(f'<text class="legend halo" x="{x0 + 8}" y="{y + 15}" font-weight="700">{n} {word}: {len(g)} '
                 f'{"split" if len(g) == 1 else "splits"}</text>')
        y += head
        for s in g:
            bad = mps_filter is not None and max(s) > mps_filter
            p.append('<g class="st-faded">' if bad else "<g>")
            p.append(f'<text class="coord halo" x="{x0 - 10}" y="{y + 15}" text-anchor="end">{plus(s)}</text>')
            for r, start, size in segments(s):
                a, b = x(start), x(start + size)
                cls = "cs-bad" if mps_filter is not None and size > mps_filter else f"cs-{r}"
                p.append(f'<rect class="{cls}" x="{a:.1f}" y="{y}" width="{b - a:.1f}" height="{row}" rx="3">'
                         f'<title>0x{start:X}–0x{start + size - 1:X}: {size} bytes ({r})</title></rect>')
                p.append(f'<text class="cs-size" x="{(a + b) / 2:.1f}" y="{y + 15}" text-anchor="middle">{size}</text>')
            p.append("</g>")
            y += row + gap
    p.append("</svg>")
    return "".join(p)


def map_legend(pruned=False):
    items = ['<span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span>',
             '<span><i class="cs-mid"></i>אמצעי</span>',
             '<span><i class="cs-last"></i>אחרון</span>']
    if pruned:
        items.append('<span><i class="cs-bad"></i>גדול מ-MPS, הפיצול נפסל</span>')
    return '<span class="viz-legend">' + "".join(items) + "</span>"


# ---------------------------------------------------------------- tables

def groups_table(splits):
    groups = {}
    for s in splits:
        groups.setdefault(len(s), []).append(s)
    lines = ["| מספר Completions | כמה פיצולים | הפיצולים (בסדר שהאלגוריתם מחזיר) |", "|:-:|:-:|---|"]
    for n in sorted(groups):
        lines.append(f"| {n} | {len(groups[n])} | " + ", ".join(RLM + plus(s) for s in groups[n]) + " |")
    lines.append(f"| **סך הכול** | **{len(splits)}** | |")
    return "\n".join(lines)


def mps_table(splits, mps_filter=128):
    lines = [f"| הפיצול | ה-Completion הגדול ביותר | ‏MPS = {MPS} | ‏MPS = {mps_filter} |", "|---|:-:|:-:|:-:|"]
    for s in splits:
        ok = max(s) <= mps_filter
        lines.append(f"| {RLM}{plus(s)} | {max(s)} | ✓ | {'✓' if ok else '✗'} |")
    kept = sum(max(s) <= mps_filter for s in splits)
    lines.append(f"| **סך הכול** | | **{len(splits)}** | **{kept}** |")
    return "\n".join(lines)


if __name__ == "__main__":
    splits = completion_splits(ADDR, LEN, MPS, RCB)
    print(params_svg(), "\n")
    print(params_legend(), "\n")
    print(splits_map_svg(splits), "\n")
    print(map_legend(), "\n")
    print(groups_table(splits), "\n")
    print(splits_map_svg(splits, mps_filter=128), "\n")
    print(map_legend(pruned=True), "\n")
    print(mps_table(splits), "\n")
