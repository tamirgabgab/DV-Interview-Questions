#!/usr/bin/env python3
"""Figures and tables of question 0021 (PCIe: how many completion splits, and the proof).

    python tools/figures/q0021.py > /tmp/q0021.html

The page has no code, so the counting lives here: the splits by the recursion of question
0020, the count by a dynamic program, the compositions C_m(N), the closed form S(n) and the
count by number of completions T(N, k). Prints, in page order: the block structure and the
map of all splits for the two 256-byte requests; the block structures of the two 512-byte
requests, the first-completion branching for N = 8 and the C(N) / T(N, k) tables; the
three cases of lemma 2, the block structure and the map of the delta example, the S(n)
table. tests/0021 checks every number independently and that the page copies match.
"""

from math import comb

RLM = "‏"
RCB, MPS = 64, 256
M = MPS // RCB
BASE = 0x1000
CASES = {"a1": (0x1000, 256), "a2": (0x1010, 256), "b1": (0x1000, 512), "b2": (0x1010, 512)}
DELTA_CASE = (0x1020, 128, 128, 64)          # addr, length, MPS, RCB: the file's delta example


# ---------------------------------------------------------------- counting

def boundaries(addr, length, rcb):
    """The RCB boundaries strictly inside the request (the set B of the proof)."""
    return list(range((addr // rcb + 1) * rcb, addr + length, rcb))


def blocks(addr, length, rcb):
    """Sizes of the N blocks the request touches: f, RCB, ..., RCB, e."""
    pts = [addr, *boundaries(addr, length, rcb), addr + length]
    return [b - a for a, b in zip(pts, pts[1:])]


def splits(addr, length, mps, rcb):
    """Every legal split as a list of sizes, in the order of question 0020 (largest cut first)."""
    end = addr + length
    out = []

    def extend(pos, sizes):
        if pos == end:
            out.append(sizes)
            return
        cuts = [end] if pos + mps >= end else []
        b = (pos // rcb + 1) * rcb
        while b < end and b <= pos + mps:
            cuts.append(b)
            b += rcb
        for cut in sorted(cuts, reverse=True):
            extend(cut, sizes + [cut - pos])

    extend(addr, [])
    return out


def count(addr, length, mps, rcb):
    """Number of legal splits by a dynamic program over the cut points (no enumeration)."""
    end = addr + length
    pts = [addr, *boundaries(addr, length, rcb), end]
    ways = {end: 1}
    for i in range(len(pts) - 2, -1, -1):
        ways[pts[i]] = sum(ways[q] for q in pts[i + 1:] if q - pts[i] <= mps)
    return ways[addr]


def compositions(n, m):
    """C_m(n): ordered sums of n with parts in 1..m (C_m(0) = 1)."""
    c = [1] + [0] * n
    for i in range(1, n + 1):
        c[i] = sum(c[i - j] for j in range(1, min(m, i) + 1))
    return c[n]


def S(n, m):
    """[x^n] 1 / (1 - 2x + x^(m+1)); S(-1) = 0."""
    if n < 0:
        return 0
    return sum((-1) ** j * comb(n - m * j, j) * 2 ** (n - (m + 1) * j) for j in range(n // (m + 1) + 1))


def delta(addr, length, mps, rcb):
    N = len(blocks(addr, length, rcb))
    return 1 if N == mps // rcb + 1 and length <= mps else 0


def formula(addr, length, mps, rcb):
    """The theorem: S(N) - S(N - 1) + delta."""
    m = mps // rcb
    N = len(blocks(addr, length, rcb))
    return S(N, m) - S(N - 1, m) + delta(addr, length, mps, rcb)


def T(N, k, m):
    """Compositions of N into exactly k parts, each at most m (inclusion-exclusion)."""
    return sum((-1) ** j * comb(k, j) * comb(N - j * m - 1, k - 1)
               for j in range((N - k) // m + 1) if N - j * m - 1 >= k - 1)


# ---------------------------------------------------------------- drawing helpers

def plus(split):
    return "+".join(str(s) for s in split)


def role(i, n):
    return "one" if n == 1 else "first" if i == 0 else "last" if i == n - 1 else "mid"


class Axis:
    """Address axis of a figure: `base` .. `base + span` bytes mapped to x0 .. x1."""

    def __init__(self, addr, length, rcb, x0, x1):
        self.base = (addr // rcb) * rcb
        end_block = -(-(addr + length) // rcb) * rcb
        self.span = end_block + rcb - self.base
        self.rcb, self.x0, self.x1 = rcb, x0, x1
        self.sc = (x1 - x0) / self.span

    def x(self, addr):
        return self.x0 + (addr - self.base) * self.sc

    def grid(self, y0, y1, addr, length, labels_y=16):
        """Dashed RCB lines with hex labels (every other one on a wide span) and the two
        request limits."""
        p = []
        step = self.rcb if self.span <= 400 else 2 * self.rcb
        for off in range(0, self.span + 1, self.rcb):
            xx = self.x(self.base + off)
            p.append(f'<line class="cs-rcb" x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y1}"/>')
            if off % step == 0:
                p.append(f'<text class="coord halo" x="{xx:.1f}" y="{labels_y}" text-anchor="middle">'
                         f'0x{self.base + off:X}</text>')
        for a in (addr, addr + length):
            xx = self.x(a)
            p.append(f'<line class="cs-req" x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y1}"/>')
        return "".join(p)


def segment(ax, cls, start, size, y, h, title, label=None, label_cls="cs-size"):
    a, b = ax.x(start), ax.x(start + size)
    p = [f'<rect class="{cls}" x="{a:.1f}" y="{y}" width="{b - a:.1f}" height="{h}" rx="3"><title>{title}</title></rect>']
    text = str(size) if label is None else label
    if b - a >= 22:
        p.append(f'<text class="{label_cls}" x="{(a + b) / 2:.1f}" y="{y + h / 2 + 4.5:.1f}" text-anchor="middle">{text}</text>')
    else:                                           # too narrow: the label sits above the bar
        p.append(f'<text class="{label_cls} halo" x="{(a + b) / 2:.1f}" y="{y - 5}" text-anchor="middle">{text}</text>')
    return "".join(p)


# ---------------------------------------------------------------- figures

def blocks_svg(addr, length, mps=MPS, rcb=RCB):
    """The request on the RCB grid, cut into its N blocks: f, full blocks, e; the interior
    boundaries marked; N, |B|, m and delta written under the bar."""
    ax = Axis(addr, length, rcb, 40, 600)
    sizes = blocks(addr, length, rcb)
    N, m = len(sizes), mps // rcb
    d = delta(addr, length, mps, rcb)
    label = (f"בקשה של {length} בתים מכתובת 0x{addr:X} על רשת RCB של {rcb}: {N} בלוקים, "
             f"{N - 1} גבולות פנימיים")
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 132" style="max-width:40rem" role="img" aria-label="{label}">',
         ax.grid(26, 96, addr, length)]
    pos = addr
    for i, s in enumerate(sizes):
        cls = "cs-first" if i == 0 else "cs-last" if i == N - 1 else "cs-mid"
        p.append(segment(ax, cls, pos, s, 50, 28, f"block {i + 1}: 0x{pos:X}–0x{pos + s - 1:X}, {s} bytes"))
        pos += s
    for b in boundaries(addr, length, rcb):
        p.append(f'<circle class="cs-can" cx="{ax.x(b):.1f}" cy="50" r="4"><title>boundary 0x{b:X}</title></circle>')
    f, e = sizes[0], sizes[-1]
    p.append(f'<text class="legend" x="40" y="118">N = {N}, |B| = {N - 1}, f = {f}, e = {e}, m = MPS / RCB = {m}, '
             f'δ = {d}{" (N = m + 1 and L ≤ MPS)" if d else ""}</text>')
    p.append("</svg>")
    return "".join(p)


def splits_map_svg(addr, length, mps=MPS, rcb=RCB):
    """Every legal split as a row of segments over the address axis, grouped by the number
    of completions (the map of question 0020)."""
    ax = Axis(addr, length, rcb, 128, 612)
    all_splits = splits(addr, length, mps, rcb)
    row, gap, head = 22, 6, 24
    groups = {}
    for s in all_splits:
        groups.setdefault(len(s), []).append(s)
    height = 30 + sum(head + len(g) * (row + gap) for g in groups.values()) + 4
    label = (f"כל {len(all_splits)} הפיצולים החוקיים של בקשה של {length} בתים מכתובת 0x{addr:X} "
             f"עם MPS = {mps} ו-RCB = {rcb}, שורה לכל פיצול")
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 {height}" style="max-width:40rem" role="img" aria-label="{label}">',
         ax.grid(24, height - 4, addr, length)]
    y = 30
    for n in sorted(groups):
        g = groups[n]
        word = "completion" if n == 1 else "completions"
        p.append(f'<text class="legend halo" x="{ax.x0 + 8}" y="{y + 15}" font-weight="700">{n} {word}: {len(g)} '
                 f'{"split" if len(g) == 1 else "splits"}</text>')
        y += head
        for s in g:
            p.append(f'<text class="coord halo" x="{ax.x0 - 10}" y="{y + 15}" text-anchor="end">{plus(s)}</text>')
            pos = addr
            for i, size in enumerate(s):
                r = role(i, len(s))
                p.append(segment(ax, f"cs-{r}", pos, size, y, row, f"0x{pos:X}–0x{pos + size - 1:X}: {size} bytes ({r})"))
                pos += size
            y += row + gap
    p.append("</svg>")
    return "".join(p)


def branch_svg(N=8, m=M):
    """The first step of the recursion C(N) = C(N-1) + ... + C(N-m): the first completion
    covers i blocks, what is left is a smaller instance."""
    bw, x0, y0, rh = 44, 150, 34, 30
    label = f"הפיצול לפי מספר הבלוקים של ה-Completion הראשון: C({N}) כסכום של C({N - 1}) עד C({N - m})"
    height = y0 + m * (rh + 14) + 30
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 {height}" style="max-width:40rem" role="img" aria-label="{label}">']
    for j in range(N + 1):
        xx = x0 + j * bw
        p.append(f'<line class="cs-rcb" x1="{xx}" y1="{y0 - 10}" x2="{xx}" y2="{height - 26}"/>')
    for j in range(N):
        p.append(f'<text class="tick" x="{x0 + j * bw + bw / 2:.1f}" y="{y0 - 14}" text-anchor="middle">β{j + 1}</text>')
    total = []
    for i in range(1, m + 1):
        y = y0 + (i - 1) * (rh + 14)
        rest = compositions(N - i, m)
        total.append(rest)
        p.append(f'<text class="legend halo" x="{x0 - 10}" y="{y + 19}" text-anchor="end">first covers {i}</text>')
        p.append(f'<rect class="cs-first" x="{x0}" y="{y}" width="{i * bw}" height="{rh}" rx="3">'
                 f'<title>the first completion: {i} block{"s" if i > 1 else ""}</title></rect>')
        p.append(f'<text class="cs-size" x="{x0 + i * bw / 2:.1f}" y="{y + 19}" text-anchor="middle">{i}</text>')
        p.append(f'<rect class="cs-mid" x="{x0 + i * bw}" y="{y}" width="{(N - i) * bw}" height="{rh}" rx="3">'
                 f'<title>what is left: {N - i} blocks, C({N - i}) = {rest} ways</title></rect>')
        p.append(f'<text class="cs-size" x="{x0 + i * bw + (N - i) * bw / 2:.1f}" y="{y + 19}" text-anchor="middle">'
                 f'C({N - i}) = {rest}</text>')
    p.append(f'<text class="legend" x="{x0}" y="{height - 8}" font-weight="700">C({N}) = '
             f'{" + ".join(str(t) for t in total)} = {sum(total)}</text>')
    p.append("</svg>")
    return "".join(p)


def lemma2_svg(m=M):
    """The three cases of lemma 2 on a request of six blocks with short end blocks: an
    interior completion, a completion holding one end, and the single completion."""
    N, bw, x0, y0, rh = 6, 64, 30, 40, 28
    f, e = 0.45, 0.3                                    # end blocks as a fraction of RCB
    edges = [x0, x0 + f * bw] + [x0 + f * bw + j * bw for j in range(1, N - 1)] + [x0 + f * bw + (N - 2) * bw + e * bw]
    label = "שלושת המקרים של למה 2: Completion פנימי, Completion עם קצה אחד, ו-Completion יחיד שמכיל את שני הקצוות"
    rows = [("(a) interior, r = 3", 1, 4, f"3·RCB ≤ MPS ⇔ r ≤ {m}"),
            ("(b) one end, r = 4", 0, 4, f"f + 3·RCB ≤ MPS ⇔ r ≤ {m}"),
            ("(c) both ends, r = N", 0, N, "L ≤ MPS ? (the δ case)")]
    height = y0 + len(rows) * (rh + 30) + 6
    p = [f'<svg class="figure cs-fig" viewBox="0 0 640 {height}" style="max-width:40rem" role="img" aria-label="{label}">']
    for j, xx in enumerate(edges):
        cls = "cs-req" if j in (0, N) else "cs-rcb"
        p.append(f'<line class="{cls}" x1="{xx:.1f}" y1="{y0 - 12}" x2="{xx:.1f}" y2="{height - 4}"/>')
    names = ["f"] + ["RCB"] * (N - 2) + ["e"]
    for j in range(N):
        p.append(f'<text class="tick" x="{(edges[j] + edges[j + 1]) / 2:.1f}" y="{y0 - 16}" text-anchor="middle">{names[j]}</text>')
    for k, (title, i0, i1, rule) in enumerate(rows):
        y = y0 + k * (rh + 30)
        for j in range(N):
            cls = "cs-mid"
            if i0 <= j < i1:
                cls = "cs-one" if (i0, i1) == (0, N) else "cs-first"
            p.append(f'<rect class="{cls}" x="{edges[j]:.1f}" y="{y}" width="{edges[j + 1] - edges[j]:.1f}" height="{rh}" rx="2"/>')
        a, b = edges[i0], edges[i1]
        p.append(f'<line class="ink-line" x1="{a + 2:.1f}" y1="{y + rh + 8}" x2="{b - 2:.1f}" y2="{y + rh + 8}" stroke-width="1.6"/>')
        p.append(f'<text class="legend" x="{edges[N] + 14:.1f}" y="{y + 11}" font-weight="700">{title}</text>')
        p.append(f'<text class="tick" x="{edges[N] + 14:.1f}" y="{y + 28}">{rule}</text>')
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------- legends and tables

def blocks_legend():
    return ('<span class="viz-legend">'
            '<span><i class="cs-first"></i>הבלוק הראשון, f בתים</span>'
            '<span><i class="cs-mid"></i>בלוק מלא, RCB בתים</span>'
            '<span><i class="cs-last"></i>הבלוק האחרון, e בתים</span>'
            '<span><i class="cs-can"></i>גבול פנימי: כאן מותר לחתוך</span>'
            '</span>')


def map_legend():
    return ('<span class="viz-legend">'
            '<span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span>'
            '<span><i class="cs-mid"></i>אמצעי</span>'
            '<span><i class="cs-last"></i>אחרון</span>'
            '</span>')


def c_table(n_max=9, m=M):
    lines = [f"| ‏\\( N \\) | החישוב | ‏\\( C_{m}(N) \\) |", "|:-:|---|:-:|"]
    for n in range(1, n_max + 1):
        terms = [compositions(n - j, m) for j in range(1, min(m, n) + 1)]
        calc = RLM + "\\( " + " + ".join(str(t) for t in terms) + " \\)" if n > 1 else "בלוק אחד, Completion אחד"
        lines.append(f"| {n} | {calc} | **{compositions(n, m)}** |")
    return "\n".join(lines)


def t_table(N, m=M):
    k_min = -(-N // m)
    lines = [f"| מספר Completions ‏\\( k \\) | ‏\\( T({N}, k) \\) |", "|:-:|:-:|"]
    for k in range(k_min, N + 1):
        lines.append(f"| {k} | {T(N, k, m)} |")
    lines.append(f"| **סך הכול** | **{sum(T(N, k, m) for k in range(k_min, N + 1))}** |")
    return "\n".join(lines)


def s_table(n_max=9, m=M):
    lines = [f"| ‏\\( n \\) | האיברים של \\( S(n) \\) | ‏\\( S(n) \\) | ‏\\( S(n) - S(n-1) \\) | ‏\\( C_{m}(n) \\) |",
             "|:-:|---|:-:|:-:|:-:|"]
    for n in range(0, n_max + 1):
        terms = []
        for j in range(n // (m + 1) + 1):
            t = comb(n - m * j, j) * 2 ** (n - (m + 1) * j)
            terms.append(("- " if j % 2 else ("+ " if j else "")) + str(t))
        lines.append(f"| {n} | {RLM}\\( {' '.join(terms)} \\) | {S(n, m)} | {S(n, m) - S(n - 1, m)} | {compositions(n, m)} |")
    return "\n".join(lines)


def cases_table():
    lines = ["| הבקשה | ‏\\( a \\) | ‏\\( N \\) | ‏\\( \\delta \\) | ‏\\( S(N) - S(N-1) + \\delta \\) | במנייה |", "|---|:-:|:-:|:-:|:-:|:-:|"]
    for key, (addr, length) in CASES.items():
        N = len(blocks(addr, length, RCB))
        d = delta(addr, length, MPS, RCB)
        lines.append(f"| {RLM}0x{addr:X}, {length} B | {addr % RCB} | {N} | {d} | "
                     f"{RLM}\\( {S(N, M)} - {S(N - 1, M)} + {d} = \\mathbf{{{formula(addr, length, MPS, RCB)}}} \\) | {count(addr, length, MPS, RCB)} |")
    return "\n".join(lines)


if __name__ == "__main__":
    for key in ("a1", "a2"):
        print(blocks_svg(*CASES[key]), "\n")
    print(blocks_legend(), "\n")
    for key in ("a1", "a2"):
        print(splits_map_svg(*CASES[key]), "\n")
    print(map_legend(), "\n")
    for key in ("b1", "b2"):
        addr, length = CASES[key]
        print(blocks_svg(addr, length), "\n")
    print(branch_svg(8), "\n")
    print(c_table(), "\n")
    print(t_table(8), "\n")
    print(t_table(9), "\n")
    print(lemma2_svg(), "\n")
    print(blocks_svg(*DELTA_CASE), "\n")
    print(splits_map_svg(*DELTA_CASE), "\n")
    print(s_table(), "\n")
    print(cases_table(), "\n")
