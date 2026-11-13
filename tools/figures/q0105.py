#!/usr/bin/env python3
"""Figures and tables of question 0105, counting distinct addresses with HyperLogLog: the
exact count, one register of leading zeros, HyperLogLog with m registers, and a pipelined
register update unit in hardware.

    python tools/figures/fill.py 105        # put the blocks on the page

The references here are independent of the page code. The hash is the page's (splitmix64's
finalizer, the same constants), but a hash value is handled as a string of 64 bits:

- split(h, p, kind) takes the register from the first p characters and the rank from the
  position of the first "1" in the others (kind "same": in the whole string, the trap);
- registers(addrs, p, kind) keeps the max rank per register, estimate(R) is the harmonic
  formula with the small-range correction, single(addrs) the max rank of the whole hash;
- the streams of the page and of the box: distinct(t) is the t-th of a sequence of distinct
  line addresses (an odd multiplier modulo 2^26, times 64), dup(t) draws from the first
  2,000 of them with repeats, seq(t) is one line after the other;
- pipe_trace(inputs, p, forward) moves updates through the three stages of part d clock by
  clock, the register read in stage 2 returning the value before that clock's write.

blocks() returns, in page order: the hash of the example with its rank (part b), the single
register on growing streams, the distribution of its estimate for 1,000 addresses, the same
hash split into register and rank (part c), its legend, the 16 registers of a small example,
the estimate of that example step by step, HyperLogLog on the growing streams, the error
against m over 200 runs, the pipeline diagram and the per-clock table of part d.
"""

from __future__ import annotations

import functools
import math
import re
from fractions import Fraction

NB = "\u00a0"
RLM = "‏"

MASK = (1 << 64) - 1
GOLD = 2654435761              # odd: t -> t * GOLD mod 2^26 is a bijection on the line numbers
LINES = 1 << 26                # 2^26 lines of 64 bytes: a 4 GB address space
N_BOX = 20000                  # the length of the box's streams
DUP_SET = 2000                 # the working set of the stream with repeats
SEQ_BASE = 0x80000000
CHECKPOINTS = [10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000, 1500, 2000, 3000,
               5000, 7000, 10000, 15000, 20000]
GROW = [10, 100, 1000, 10000, 100000, 1000000]       # the growing streams of parts b and c
EXAMPLE_T = 13                 # the address of the hash figures: distinct(EXAMPLE_T)
SMALL_P, SMALL_N = 4, 50       # the register figure: 16 registers, the first 50 addresses
RUNS, RUN_N = 200, 5000        # the error table: 200 runs of 5,000 distinct addresses
PIPE_P = 4                     # the per-clock table: 16 registers


def ltr(s) -> str:
    return f'<span dir="ltr">{s}</span>'


def num(n) -> str:
    return f"{n:,}"


def pct(x) -> str:
    """A signed percent with a minus sign, one decimal."""
    return ("+" if x >= 0 else "−") + f"{abs(x) * 100:.1f}%"


# --- the hash and the streams -----------------------------------------------------------------

def mix64(x: int) -> int:
    x = (x + 0x9E3779B97F4A7C15) & MASK
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & MASK
    return x ^ (x >> 31)


def hash_of(addr: int, kind: str = "mix") -> int:
    """kind "mix": the mixer; "ident": the 32-bit address itself, at the top of the word."""
    return (addr << 32) & MASK if kind == "ident" else mix64(addr)


def first_one(bits: str) -> int:
    """The rank of a string of bits: where its first 1 is, from 1; len + 1 when there is none."""
    i = bits.find("1")
    return len(bits) + 1 if i < 0 else i + 1


def split(h: int, p: int, kind: str = "mix"):
    s = format(h, "064b")
    j = int(s[:p], 2) if p else 0
    return j, first_one(s if kind == "same" else s[p:])


def distinct(t: int) -> int:
    return 64 * ((t * GOLD) % LINES)


def stream(name: str, n: int = N_BOX) -> list[int]:
    if name == "rand":
        return [distinct(t) for t in range(1, n + 1)]
    if name == "dup":
        return [distinct(1 + (t * GOLD) % LINES % DUP_SET) for t in range(1, n + 1)]
    if name == "seq":
        return [SEQ_BASE + 64 * t for t in range(1, n + 1)]
    raise ValueError(name)


# --- the estimators ---------------------------------------------------------------------------

def registers(addrs, p: int, kind: str = "mix") -> list[int]:
    R = [0] * (1 << p)
    for a in addrs:
        j, r = split(hash_of(a, kind), p, kind)
        R[j] = max(R[j], r)
    return R


def alpha(m: int) -> float:
    return 0.7213 / (1 + 1.079 / m)


def raw_estimate(R) -> float:
    m = len(R)
    return alpha(m) * m * m / sum(2.0 ** -r for r in R)


def estimate(R) -> float:
    m, e, zeros = len(R), raw_estimate(R), R.count(0)
    if e <= 2.5 * m and zeros > 0:
        return m * math.log(m / zeros)
    return e


def arith_estimate(R) -> float:
    """The trap: the same formula with the arithmetic mean of 2^R in place of the harmonic one."""
    m = len(R)
    return alpha(m) * m * sum(2.0 ** r for r in R) / m


def single(addrs, kind: str = "mix") -> int:
    return max((first_one(format(hash_of(a, kind), "064b")) for a in addrs), default=0)


def single_dist(n: int, r: int) -> Fraction:
    """P(the max rank of n random hashes is exactly r): every rank is <= r, not every one < r."""
    le = lambda k: (1 - Fraction(1, 2 ** k)) ** n if k > 0 else Fraction(0)   # noqa: E731
    return le(r) - le(r - 1)


def std_error(m: int) -> float:
    return 1.04 / math.sqrt(m)


@functools.lru_cache(maxsize=None)
def grow_rows():
    """Per n of GROW: the single register's rank and HyperLogLog with 1,024 registers, on
    distinct(1..n)."""
    out, R, r1, t = [], [0] * 1024, 0, 0
    for n in GROW:
        while t < n:
            t += 1
            h = mix64(distinct(t))
            j, r = split(h, 10)
            R[j] = max(R[j], r)
            r1 = max(r1, first_one(format(h, "064b")))
        out.append((n, r1, estimate(R)))
    return tuple(out)


@functools.lru_cache(maxsize=None)
def error_rows():
    """Per p in 4, 6, 8, 10: the rms relative error of the estimate (and of the arithmetic mean)
    over RUNS runs of RUN_N distinct addresses, run k taking distinct(k * RUN_N + 1 ...)."""
    ps = (4, 6, 8, 10)
    errs = {p: [] for p in ps}
    arith = {p: [] for p in ps}
    for k in range(RUNS):
        regs = {p: [0] * (1 << p) for p in ps}
        for t in range(k * RUN_N + 1, (k + 1) * RUN_N + 1):
            s = format(mix64(distinct(t)), "064b")
            for p in ps:
                j, r = int(s[:p], 2), first_one(s[p:])
                if r > regs[p][j]:
                    regs[p][j] = r
        for p in ps:
            errs[p].append(estimate(regs[p]) / RUN_N - 1)
            arith[p].append(arith_estimate(regs[p]) / RUN_N - 1)
    rms = lambda v: math.sqrt(sum(x * x for x in v) / len(v))   # noqa: E731
    return tuple((p, rms(errs[p]), rms(arith[p]), max(arith[p]),
                  sum(1 for x in errs[p] if abs(x) > 2 * std_error(1 << p))) for p in ps)


def merge_example():
    """Two monitors: distinct(1..60,000) and distinct(30,001..90,000), 1,024 registers each."""
    a = registers([distinct(t) for t in range(1, 60001)], 10)
    b = registers([distinct(t) for t in range(30001, 90001)], 10)
    u = [max(x, y) for x, y in zip(a, b)]
    return estimate(a), estimate(b), estimate(u), u


def dup_example():
    """15,000 transactions over 5,000 distinct addresses, 1,024 registers."""
    s = [distinct(1 + (t * GOLD) % LINES % 5000) for t in range(1, 15001)]
    return len(set(s)), estimate(registers(s, 10))


def small_range_example():
    """100 distinct addresses in 1,024 registers: the raw estimate and the corrected one."""
    R = registers(stream("rand", 100), 10)
    return raw_estimate(R), estimate(R), R.count(0)


def box_series(name: str, kind: str, p: int):
    """The box at every checkpoint: (transactions, distinct so far, estimate, single rank,
    registers)."""
    s = stream(name)
    R, seen, r1, out, t = [0] * (1 << p), set(), 0, [], 0
    for c in CHECKPOINTS:
        while t < c:
            a = s[t]
            t += 1
            seen.add(a)
            h = hash_of(a, kind)
            j, r = split(h, p, kind)
            R[j] = max(R[j], r)
            r1 = max(r1, first_one(format(h, "064b")))
        out.append((c, len(seen), estimate(R), r1, R[:]))
    return out


# --- part d: the pipeline ---------------------------------------------------------------------

def find_pipe_addrs():
    """Three line addresses in one register of 16, with ranks 4, 1 and 2: A and B back to back
    lose A's update without forwarding, C two clocks later reads after the write."""
    want, found = {4: None, 1: None, 2: None}, {}
    for k in range(1, 100000):
        j, r = split(mix64(64 * k), PIPE_P)
        found.setdefault(j, {}).setdefault(r, 64 * k)
        got = found[j]
        if all(x in got for x in want):
            return j, got[4], got[1], got[2]
    raise RuntimeError("no three addresses")


PIPE_J, PIPE_A, PIPE_B, PIPE_C = find_pipe_addrs()
PIPE_IN = [PIPE_A, PIPE_B, None, PIPE_C]
PIPE_NAMES = {PIPE_A: "A", PIPE_B: "B", PIPE_C: "C"}


def pipe_trace(inputs, p: int, forward: bool = True):
    """Per clock: (stage 1, stage 2, stage 3, the registers after the clock's edge). Stage 1 holds
    the address being hashed, stage 2 (address, j, r, q) the split and the register as read,
    stage 3 (address, j, r, old, new) the max being written, old the forwarded value when the
    previous clock wrote the same register."""
    R = [0] * (1 << p)
    s1 = s2 = None             # the pipeline registers: the address in stage 2, and in stage 3
    last = None                # the previous clock's write: (j, value)
    out = []
    for c in range(len(inputs) + 2):
        a = inputs[c] if c < len(inputs) else None
        st3 = None
        if s2 is not None:
            addr, j, r, q = s2
            old = last[1] if forward and last is not None and last[0] == j else q
            st3 = (addr, j, r, old, max(old, r), old != q)
        st2 = None
        if s1 is not None:
            j, r = split(mix64(s1), p)
            st2 = (s1, j, r, R[j])                     # read before this edge's write
        if st3 is not None:
            R[st3[1]] = st3[4]
        out.append((a, st2, st3, R[:]))
        s1, s2, last = a, (None if st2 is None else st2), (None if st3 is None else (st3[1], st3[4]))
    return out


# --- the figures ------------------------------------------------------------------------------

def hash_svg(addr: int, p: int) -> str:
    """The 64 bits of mix64(addr) in four rows of 16, the top bit first: the register's p bits,
    the leading zeros of the rest and its first 1."""
    s = format(mix64(addr), "064b")
    j, r = split(mix64(addr), p)
    CW, CH, GAP, X0, Y0, RG = 19, 24, 5, 30, 8, 8
    W = X0 + 16 * CW + 3 * GAP + 6
    H = Y0 + 4 * CH + 3 * RG + 6
    parts = []
    for i, b in enumerate(s):
        row, col = divmod(i, 16)
        x = X0 + col * CW + (col // 4) * GAP
        y = Y0 + row * (CH + RG)
        if i < p:
            cls = "is-idx"
        elif i < p + r - 1:
            cls = "is-zero"
        elif i == p + r - 1:
            cls = "is-one"
        else:
            cls = "is-rest"
        parts.append(f'<rect class="hll-bit {cls}" x="{x}" y="{y}" width="{CW - 2}" height="{CH}" rx="2"/>'
                     f'<text class="hll-bit-t {cls}" x="{x + (CW - 2) / 2:.1f}" y="{y + CH / 2 + 5}" text-anchor="middle">{b}</text>')
    for row in range(4):
        y = Y0 + row * (CH + RG) + CH / 2 + 4
        parts.append(f'<text class="hll-bitno" x="{X0 - 5}" y="{y:.1f}" text-anchor="end">{63 - 16 * row}</text>')
    who = (f"הביטים {p} הראשונים, {s[:p]}, בוחרים את רגיסטר {j}, ואחריהם {r - 1} אפסים ו-1 : הדרגה {r}" if p
           else f"{r - 1} אפסים מובילים ואחריהם 1 : הדרגה {r}")
    label = f"64 הביטים של ה-hash של הכתובת {addr}, בארבע שורות של 16, הביט העליון ראשון. {who}"
    return (f'<svg class="figure hll-hash" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.3f}rem" direction="ltr" '
            f'role="img" aria-label="{label}">' + "".join(parts) + "</svg>")


def hash_legend(p: int) -> str:
    items = [("hll-key-idx", "הביטים שבוחרים את הרגיסטר")] if p else []
    items += [("hll-key-zero", "האפסים המובילים"), ("hll-key-one", "ה-1 הראשון : הדרגה")]
    return '<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{t}</span>' for c, t in items) + "</span>"


def level(v: int, vmax: int) -> int:
    """The tint of a register: 0 empty, then 1 to 6 by its share of the largest value."""
    return 0 if v == 0 else min(6, max(1, math.ceil(6 * v / max(vmax, 1))))


def registers_svg() -> str:
    R = registers(stream("rand", SMALL_N), SMALL_P)
    m, vmax = len(R), max(R)
    C, GAP, X0, Y0 = 40, 4, 4, 4
    W = X0 * 2 + 8 * C + 7 * GAP
    H = Y0 + 2 * (C + 18) + 2
    parts = []
    for j, v in enumerate(R):
        row, col = divmod(j, 8)
        x, y = X0 + col * (C + GAP), Y0 + row * (C + 18)
        parts.append(f'<g class="hll-reg hll-c{level(v, vmax)}"><rect x="{x}" y="{y}" width="{C}" height="{C}" rx="3"/>'
                     + (f'<text x="{x + C / 2:.1f}" y="{y + C / 2 + 6}" text-anchor="middle">{v}</text>' if v else "")
                     + f'<title>רגיסטר {j} : {v if v else "ריק"}</title></g>'
                     f'<text class="hll-regno" x="{x + C / 2:.1f}" y="{y + C + 13}" text-anchor="middle">{j}</text>')
    label = (f"16 הרגיסטרים אחרי {SMALL_N} הכתובות הראשונות של הזרם האקראי, לפי הסדר : "
             + ", ".join(str(v) for v in R) + f". {R.count(0)} ריקים")
    return (f'<svg class="figure hll-regs" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.3f}rem" direction="ltr" '
            f'role="img" aria-label="{label}">' + "".join(parts) + "</svg>")


def registers_table() -> str:
    R = registers(stream("rand", SMALL_N), SMALL_P)
    m = len(R)
    s = sum(Fraction(1, 2 ** r) for r in R)
    e = raw_estimate(R)
    rows = ["| הגודל | הערך |", "|---|:-:|",
            f"| הסכום {ltr('Σ 2<sup>−R[j]</sup>')} | {RLM}{ltr(f'{float(s):.4f}')} |",
            f"| הקבוע ‏α<sub>16</sub> | {RLM}{ltr(f'{alpha(m):.4f}')} |",
            f"| האומדן {ltr('α m² / Σ')} | {RLM}{ltr(f'{e:.1f}')} |",
            f"| רגיסטרים ריקים V | {R.count(0)} |",
            f"| הסף של התיקון {ltr('2.5 m')} | {RLM}{ltr(f'{2.5 * m:g}')} |"]
    return "\n".join(rows)


def grow_table() -> str:
    rows = ["| כתובות שונות | רגיסטר אחד R | האומדן 2<sup>R</sup> | פי |", "|:-:|:-:|:-:|:-:|"]
    for n, r, _ in grow_rows():
        rows.append(f"| {num(n)} | {r} | {num(2 ** r)} | {RLM}{ltr(f'{2 ** r / n:.2f}')} |")
    return "\n".join(rows)


def dist_table(n: int = 1000) -> str:
    rows = ["| האומדן 2<sup>R</sup> | פי | ההסתברות |", "|:-:|:-:|:-:|"]
    lo = Fraction(0)
    for r in range(1, 9):
        lo += single_dist(n, r)
    rows.append(f"| עד {num(2 ** 8)} | {RLM}{ltr('≤ 0.26')} | {RLM}{ltr(f'{float(lo) * 100:.1f}%')} |")
    for r in range(9, 14):
        rows.append(f"| {num(2 ** r)} | {RLM}{ltr(f'{2 ** r / n:.2f}')} | {RLM}{ltr(f'{float(single_dist(n, r)) * 100:.1f}%')} |")
    hi = 1 - (1 - Fraction(1, 2 ** 13)) ** n
    rows.append(f"| {num(2 ** 14)} ומעלה | {RLM}{ltr('≥ 16.38')} | {RLM}{ltr(f'{float(hi) * 100:.1f}%')} |")
    return "\n".join(rows)


def hll_table() -> str:
    rows = ["| כתובות שונות | האומדן, 1,024 רגיסטרים | השגיאה | רגיסטר אחד |", "|:-:|:-:|:-:|:-:|"]
    for n, r, e in grow_rows():
        rows.append(f"| {num(n)} | {num(round(e))} | {RLM}{ltr(pct(e / n - 1))} | {num(2 ** r)} |")
    return "\n".join(rows)


def error_table() -> str:
    rows = ["| רגיסטרים m | הזיכרון | ‏1.04/√m | השגיאה שנמדדה | מחוץ ל-2σ |", "|:-:|:-:|:-:|:-:|:-:|"]
    for p, rms, _, _, out in error_rows():
        m = 1 << p
        rows.append(f"| {num(m)} | {num(m * 6 // 8)} בתים | {RLM}{ltr(f'{std_error(m) * 100:.2f}%')} | "
                    f"{RLM}{ltr(f'{rms * 100:.2f}%')} | {out} מתוך {RUNS} |")
    return "\n".join(rows)


def pipe_svg() -> str:
    """The update unit: stage 1 hashes, stage 2 splits, counts and reads, stage 3 takes the max
    and writes; the forwarding path takes the previous write back to stage 3's multiplexer."""
    p = []
    box = lambda x, y, w, h, cls: f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'   # noqa: E731
    txt = lambda x, y, s, cls="hll-pt", a="middle": f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{a}">{s}</text>'   # noqa: E731
    wire = lambda x1, y1, x2, y2, cls="hll-wire": f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'   # noqa: E731
    head = lambda x, y, cls="hll-head": f'<path class="{cls}" d="M{x},{y} l-7,-4 v8 z"/>'   # noqa: E731
    # stage frames and names
    for i, (x, w) in enumerate([(14, 104), (150, 150), (332, 162)]):
        p.append(box(x, 26, w, 112, "hll-stage"))
        p.append(txt(x + w / 2, 18, f"stage {i + 1}", "hll-st-name"))
    p.append(txt(14, 160, "in: valid, addr", "hll-io", "start"))
    # stage 1: the hash
    p.append(box(26, 42, 80, 34, "hll-op") + txt(66, 64, "mix64"))
    p.append(box(26, 92, 80, 34, "hll-reg") + txt(66, 114, "v1  h1"))
    p.append(wire(66, 76, 66, 92))
    p.append(wire(106, 109, 160, 109) + head(160, 109))
    # stage 2: split, count, read
    p.append(box(162, 42, 126, 34, "hll-op") + txt(225, 57, "j = h[63:64-P]") + txt(225, 71, "r = clz + 1"))
    p.append(box(162, 92, 126, 34, "hll-reg") + txt(225, 114, "v2 j2 r2 q2"))
    p.append(wire(225, 76, 225, 92))
    p.append(wire(288, 109, 344, 109) + head(344, 109))
    # stage 3: forward mux, max, write
    p.append(box(346, 42, 72, 34, "hll-op") + txt(382, 57, "old =") + txt(382, 71, "q2 / wq"))
    p.append(box(428, 42, 54, 34, "hll-op") + txt(455, 64, "max"))
    p.append(wire(418, 59, 428, 59) + head(428, 59))
    p.append(box(346, 92, 136, 34, "hll-fwd") + txt(414, 106, "wv wj wq", "hll-pt") + txt(414, 120, "previous write", "hll-pt-s"))
    p.append(wire(382, 92, 382, 76, "hll-wire hll-fwd-w") + f'<path class="hll-head hll-fwd-h" d="M382,77 l-4,7 h8 z"/>')
    # the register RAM under stages 2 and 3
    p.append(box(162, 180, 320, 36, "hll-ram") + txt(322, 203, "regs [M] : 6 bits each"))
    p.append(wire(225, 180, 225, 128, "hll-wire") + f'<path class="hll-head" d="M225,128 l-4,7 h8 z"/>')
    p.append(txt(231, 160, "read j1", "hll-pt-s", "start"))
    p.append(wire(455, 76, 455, 92, "hll-wire hll-dim"))
    p.append(f'<path class="hll-wire" d="M482,59 h8 v135 h-8" fill="none"/>' + head(482, 194))
    p.append(txt(490, 230, "write regs[j2]", "hll-pt-s", "end"))
    W, H = 508, 240
    label = ("יחידת העדכון בשלושה שלבים : שלב 1 מחשב את ה-hash, שלב 2 מפצל אותו לרגיסטר ולדרגה וקורא את הרגיסטר, "
             "שלב 3 לוקח את המקסימום וכותב. דרך הקידום מחזירה את הכתיבה של השעון הקודם לבורר של שלב 3")
    return (f'<svg class="figure hll-pipe" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.3f}rem" direction="ltr" '
            f'role="img" aria-label="{label}">' + "".join(p) + "</svg>")


def pipe_rows(forward: bool):
    return pipe_trace(PIPE_IN, PIPE_P, forward)


def pipe_table() -> str:
    good, bad = pipe_rows(True), pipe_rows(False)
    J = PIPE_J
    rows = [f"| שעון | שלב 1 | שלב 2 | שלב 3 | ‏R[{J}] | ‏R[{J}] בלי קידום |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    name = lambda a: PIPE_NAMES[a]   # noqa: E731
    for c, ((a, st2, st3, R), (_, _, _, Rb)) in enumerate(zip(good, bad), 1):
        c1 = "–" if a is None else RLM + name(a)
        c2 = "–" if st2 is None else f"{RLM}{ltr(f'{name(st2[0])}: r={st2[2]}, q={st2[3]}')}"
        if st3 is None:
            c3 = "–"
        else:
            addr, j, r, old, new, fwd = st3
            o = f"<b>{old}</b>" if fwd else str(old)
            c3 = f"{RLM}{ltr(f'{name(addr)}: max({o}, {r})')}"
        rows.append(f"| {c} | {c1} | {c2} | {c3} | {R[J]} | {Rb[J]} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    ex = distinct(EXAMPLE_T)
    out = [
        hash_svg(ex, 0),
        hash_legend(0),
        grow_table(),
        dist_table(),
        hash_svg(ex, SMALL_P),
        hash_legend(SMALL_P),
        registers_svg(),
        registers_table(),
        hll_table(),
        error_table(),
        pipe_svg(),
        pipe_table(),
    ]
    return [re.sub(r"(?<=\S) :(?=[\s*]|$)", NB + ":", blk) for blk in out]


if __name__ == "__main__":
    ex = distinct(EXAMPLE_T)
    print("example", ex, format(mix64(ex), "064b"), split(mix64(ex), 0), split(mix64(ex), SMALL_P))
    print("grow", grow_rows())
    print("small regs", registers(stream("rand", SMALL_N), SMALL_P), raw_estimate(registers(stream("rand", SMALL_N), SMALL_P)),
          estimate(registers(stream("rand", SMALL_N), SMALL_P)))
    print("pipe", PIPE_J, PIPE_A, PIPE_B, PIPE_C)
    for row in pipe_rows(True):
        print(row[:3], row[3][PIPE_J])
    for row in pipe_rows(False):
        print(row[:3], row[3][PIPE_J])
    print("merge", merge_example()[:3])
    print("dup", dup_example())
    print("small range", small_range_example())
    print("errors", error_rows())
    for r in range(8, 15):
        print(r, float(single_dist(1000, r)))
