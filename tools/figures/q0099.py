#!/usr/bin/env python3
"""Figures and tables of question 0099, the two check digits of an IBAN (mod 97).

    python tools/figures/fill.py 99        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The functions above blocks() are the reference the question's tests use: the
IBAN moved and turned into digits, the remainder mod 97 digit by digit, the check digits,
the Israeli IBAN built from a bank, a branch and an account, and the errors of each kind
with the share of them a modulus catches.

Only published registry examples are used (the ISO 13616 registry's IL62 0108 0000 0009
9999 999, GB82 WEST 1234 5698 7654 32, DE89 3704 0044 0532 0130 00) and made-up numbers.
"""

from __future__ import annotations

import itertools
import math as _m
import random
import re
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "

IL = "IL62 0108 0000 0009 9999 999"
EXAMPLES = (IL, "GB82 WEST 1234 5698 7654 32", "DE89 3704 0044 0532 0130 00")
# the double error of part c: the last two digits 99 become 02, 97 less, and it slips
SLIP = "IL62 0108 0000 0009 9999 902"


# --- the reference ---------------------------------------------------------------------------------

def norm(iban: str) -> str:
    return iban.replace(" ", "").upper()


def well_formed(iban: str) -> bool:
    """Two letters, two digits, then letters and digits (A-Z, 0-9 only)."""
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+", norm(iban)) is not None


def moved(iban: str) -> str:
    s = norm(iban)
    return s[4:] + s[:4]


def char_digits(c: str) -> str:
    """A digit stays, a letter becomes two digits: A = 10 ... Z = 35."""
    return str(int(c, 36))


def to_digits(iban: str) -> str:
    return "".join(char_digits(c) for c in moved(iban))


def running(digits: str) -> list[int]:
    """The remainder mod 97 after each digit: r = (10 r + d) mod 97."""
    r, out = 0, []
    for d in digits:
        r = (10 * r + int(d)) % 97
        out.append(r)
    return out


def mod97(iban: str) -> int:
    return int(to_digits(iban)) % 97


def valid(iban: str) -> bool:
    return well_formed(iban) and mod97(iban) == 1


def check_digits(iban: str) -> str:
    """98 - m, m the remainder with 00 in place of the check digits."""
    s = norm(iban)
    return f"{98 - mod97(s[:2] + '00' + s[4:]):02d}"


def grouped(iban: str) -> str:
    s = norm(iban)
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


# --- the hardware of part b ----------------------------------------------------------------------
# One digit (4 bits) a clock: the IBAN as written, a letter already split into its two digits,
# so the head (two letters and two check digits) is the first 6 digits of the stream.

HEAD = 6                                      # digits of the first four characters
STAGES = (776, 388, 194, 97)                  # 8, 4, 2, 1 times 97
FINAL_STAGES = (1552, 776, 388, 194, 97)      # 16 .. 1 times 97, for 27 r + h < 2716


def reduce(s: int, stages=STAGES) -> int:
    """s mod 97 by compare-and-subtract, largest multiple first (s < 2 * stages[0])."""
    assert 0 <= s < 2 * stages[0]
    for m in stages:
        if s >= m:
            s -= m
    return s


def step_hw(r: int, d: int) -> int:
    """(10 r + d) mod 97 as the datapath does it: 8r + 2r + d (shifts and adders, at most
    969), then the four stages."""
    return reduce((r << 3) + (r << 1) + d)


def step2_hw(r: int, a: int, b: int) -> int:
    """Two digits a clock: (100 r + 10 a + b) mod 97 = (3 r + 10 a + b) mod 97, at most 387,
    two stages."""
    return reduce(3 * r + 10 * a + b, (194, 97))


def step_letter(r: int, v: int) -> int:
    """A letter in one clock: (100 r + v) mod 97 = (3 r + v) mod 97, at most 323."""
    return reduce(3 * r + v, (194, 97))


def final_hw(r: int, h: int) -> int:
    """(27 r + h) mod 97: the head's 6 digits belong after the rest, 10^6 = 27 mod 97."""
    return reduce(27 * r + h, FINAL_STAGES)


def stream(iban: str) -> list[int]:
    """The digits as they arrive: the IBAN as written, every letter as two digits."""
    return [int(c) for c in "".join(char_digits(c) for c in norm(iban))]


def run_buffer(digits) -> tuple[bool, int, int]:
    """34 flip-flops: the 6 head digits kept (24), a counter (3) and r (7); the head is fed
    again after the rest. (valid, clocks, flip-flops)."""
    buf, r, clocks = [], 0, 0
    for k, d in enumerate(digits):
        clocks += 1
        if k < HEAD:
            buf.append(d)
        else:
            r = step_hw(r, d)
    for d in buf:                               # the replay: 6 more clocks
        clocks += 1
        r = step_hw(r, d)
    return r == 1, clocks, 6 * 4 + 3 + 7


def run_two(digits) -> tuple[bool, int, int]:
    """17 flip-flops: h and r (7 each) and a counter of the head (3)."""
    h = r = n = 0
    for d in digits:
        if n < HEAD:
            h, n = step_hw(h, d), n + 1
        else:
            r = step_hw(r, d)
    return final_hw(r, h) == 1, len(digits), 7 + 7 + 3


def run_shared(digits) -> tuple[bool, int, int]:
    """15 flip-flops: during the head r counts its digits, a phase bit tells the two apart."""
    h, r, head = 0, 0, 1
    for d in digits:
        if head:
            h = step_hw(h, d)
            r, head = (0, 0) if r == HEAD - 1 else (r + 1, 1)
        else:
            r = step_hw(r, d)
    return final_hw(r, h) == 1, len(digits), 7 + 7 + 1


def run_codes(digits) -> tuple[bool, int, int]:
    """14 flip-flops: r never holds 97..127 as a remainder, so 97 + k means "head digit k";
    after the sixth head digit r becomes 0. No other state."""
    h, r = 0, 97
    for d in digits:
        if r >= 97:
            h = step_hw(h, d)
            r = 0 if r == 97 + HEAD - 1 else r + 1
        else:
            r = step_hw(r, d)
    return r < 97 and final_hw(r, h) == 1, len(digits), 7 + 7


VERSIONS = (("buffer", run_buffer), ("two", run_two), ("shared", run_shared), ("codes", run_codes))


def states_needed() -> int:
    """The states the checker must tell apart: the start, the head after 1..5 digits (h
    only), and every pair (h, r) after it."""
    return 1 + (HEAD - 1) * 97 + 97 * 97


def order10(m: int) -> int:
    """The order of 10 mod m (gcd(10, m) = 1): the least d > 0 with 10^d = 1 mod m."""
    d, x = 1, 10 % m
    while x != 1:
        x, d = x * 10 % m, d + 1
    return d


def random_ibans(n: int = 30, seed: int = 99) -> list[str]:
    """n made-up Israeli IBANs: 19 random digits and their check digits."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        bban = "".join(rng.choice("0123456789") for _ in range(19))
        out.append("IL" + check_digits("IL00" + bban) + bban)
    return out


def errors(iban: str) -> dict[str, list[str]]:
    """Every error of four kinds among the digits of the BBAN (the account part, after the
    check digits): one digit changed, two neighbours swapped, two digits one apart swapped
    (abc -> cba), two digits changed."""
    s = norm(iban)
    pos = range(4, len(s))
    d = "0123456789"
    return {
        "single": [s[:i] + a + s[i + 1:] for i in pos for a in d if a != s[i]],
        "adjacent": [s[:i] + s[i + 1] + s[i] + s[i + 2:] for i in pos if i + 1 < len(s) and s[i] != s[i + 1]],
        "jump": [s[:i] + s[i + 2] + s[i + 1] + s[i] + s[i + 3:] for i in pos if i + 2 < len(s) and s[i] != s[i + 2]],
        "double": [s[:i] + a + s[i + 1:j] + b + s[j + 1:]
                   for i, j in itertools.combinations(pos, 2) for a in d if a != s[i] for b in d if b != s[j]],
    }


KINDS = ("single", "adjacent", "jump", "double")
MODULI = (100, 99, 98, 97)


def caught(moduli=MODULI, ibans=None) -> dict[int, dict[str, tuple[int, int]]]:
    """For each modulus M and kind of error: (errors caught, errors), where an error is caught
    when it changes the number by something that is not a multiple of M."""
    ibans = random_ibans() if ibans is None else ibans
    out = {m: {k: [0, 0] for k in KINDS} for m in moduli}
    for s in ibans:
        n0 = int(to_digits(s))
        for k, lst in errors(s).items():
            for t in lst:
                delta = int(to_digits(t)) - n0
                for m in moduli:
                    out[m][k][1] += 1
                    out[m][k][0] += delta % m != 0
    return {m: {k: tuple(v) for k, v in row.items()} for m, row in out.items()}


# --- the blocks ----------------------------------------------------------------------------------

def L(text) -> str:
    return f'<span dir="ltr">{text}</span>'


def moved_table() -> str:
    s = norm(IL)
    rows = ["| השלב | המחרוזת |", "|---|---|",
            f"| כפי שנכתב | {RLM}{L(grouped(IL))} |",
            f"| ‏4 התווים הראשונים לסוף | {RLM}{L(s[4:] + ' ' + s[:4])} |",
            f"| כל אות לשתי ספרות, ‏{L('I = 18')} ו-{L('L = 21')} | {RLM}{L(to_digits(IL)[:-6] + ' ' + to_digits(IL)[-6:])} |"]
    return "\n".join(rows)


def running_grid(iban: str = IL, label: str = "") -> str:
    """The digits of the moved IBAN in rows of ten, each with the remainder after it under it:
    the digits that came from letters and the two check digits marked."""
    s = moved(iban)
    digits, owner = "", []
    for k, c in enumerate(s):
        ds = char_digits(c)
        digits += ds
        kind = "let" if c.isalpha() else "chk" if k >= len(s) - 2 else "num"
        owner += [kind] * len(ds)
    rs = running(digits)
    rows = []
    for t in range(0, len(digits), 10):
        top, bot = [], []
        for i in range(t, t + 10):
            if i < len(digits):
                cls = {"let": " ib-let", "chk": " ib-chk", "num": ""}[owner[i]]
                last = " ib-last" if i == len(digits) - 1 else ""
                top.append(f'<td class="gs-b ib-d{cls}">{digits[i]}</td>')
                bot.append(f'<td class="gs-b ib-r{last}">{rs[i]}</td>')
            else:
                top.append('<td class="gs-b ib-pad"></td>')
                bot.append('<td class="gs-b ib-pad"></td>')
        rows.append(f"<tr><th>d</th>{''.join(top)}</tr>")
        rows.append(f'<tr class="ib-rrow"><th>r</th>{"".join(bot)}</tr>')
    label = label or (f"הספרות של {grouped(iban)} אחרי ההעברה, ומתחת לכל ספרה השארית בחלוקה ל-97 עד אליה. "
                      f"השארית בסוף היא {rs[-1]}")
    table = (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
             f'<table class="gs-bits ib-tab" dir="ltr" aria-label="{escape(label)}"><tbody>' + "".join(rows) + "</tbody></table></div>")
    legend = ('<span class="viz-legend">'
              f'<span><i class="ib-key-let"></i><span>ספרות של אות ({L("I = 18, L = 21")})</span></span>'
              '<span><i class="ib-key-chk"></i><span>ספרות הביקורת</span></span>'
              f'<span><i class="ib-key-last"></i><span>השארית בסוף, {rs[-1]}</span></span></span>')
    return table + "\n\n" + legend


def check_table() -> str:
    rows = ["| ה-IBAN | השארית עם 00 | ‏98 פחות השארית | ספרות הביקורת שבו |", "|---|:-:|:-:|:-:|"]
    for ib in EXAMPLES:
        s = norm(ib)
        m = mod97(s[:2] + "00" + s[4:])
        rows.append(f"| {RLM}{L(grouped(s[:2] + '00' + s[4:]))} | {m} | {98 - m:02d} | {s[2:4]} |")
    return "\n".join(rows)


NAMES = {"single": "ספרה אחת שגויה", "adjacent": "שתי שכנות הוחלפו", "jump": "החלפה בדילוג, abc ל-cba",
         "double": "שתי ספרות שגויות"}


def moduli_table() -> str:
    res = caught()
    rows = ["| סוג הטעות | ‏מודולו 100 | ‏מודולו 99 | ‏מודולו 98 | ‏מודולו 97 |", "|---|:-:|:-:|:-:|:-:|"]
    for k in KINDS:
        cells = []
        for m in MODULI:
            c, n = res[m][k]
            cells.append(f"{100 * c / n:.1f}%" if c != n else "100%")
        name = NAMES[k].replace("abc ל-cba", f"{L('abc')} ל-{L('cba')}")
        rows.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


# --- the figures of part b -----------------------------------------------------------------------

def _arrow_defs(idn: str) -> str:
    return (f'<defs><marker id="{idn}" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto">'
            '<path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>')


def mod3_svg() -> str:
    """The whole machine for a small modulus: 3 states, (10 r + d) mod 3 = (r + d) mod 3, so
    the digits fall into three groups by d mod 3; state 0 is the start and the accepting one.
    Between two states the two edges bend to opposite sides; a state's own group is a loop."""
    W, H, R = 380, 350, 26
    pos = {0: (190, 104), 1: (310, 262), 2: (70, 262)}
    groups = {0: "0,3,6,9", 1: "1,4,7", 2: "2,5,8"}
    out = [f'<svg class="figure ih-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
           'aria-label="מכונת המצבים של השארית בחלוקה ל-3 : שלושה מצבים, 0, 1 ו-2. מכל מצב ספרה מקבוצה 0, 3, 6, 9 '
           'משאירה במקום, ספרה מקבוצה 1, 4, 7 מוסיפה 1, וספרה מקבוצה 2, 5, 8 מוסיפה 2, מודולו 3. ההתחלה ב-0, '
           'ו-0 הוא גם המצב שבו המספר מתחלק ב-3">', _arrow_defs("ih-h3")]
    for r in range(3):
        for step, cls in ((1, "ih-e1"), (2, "ih-e2")):
            t = (r + step) % 3
            a, b = min(r, t), max(r, t)
            (ax, ay), (bx, by) = pos[a], pos[b]
            ln = _m.hypot(bx - ax, by - ay)
            nx, ny = -(by - ay) / ln, (bx - ax) / ln         # one normal for the pair
            side = 1 if r < t else -1
            (x1, y1), (x2, y2) = pos[r], pos[t]
            ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
            off = 9 * side
            sx, sy = x1 + ux * R + nx * off, y1 + uy * R + ny * off
            ex, ey = x2 - ux * (R + 3) + nx * off, y2 - uy * (R + 3) + ny * off
            mx, my = (x1 + x2) / 2 + nx * 34 * side, (y1 + y2) / 2 + ny * 34 * side
            out.append(f'<path class="ih-edge {cls}" d="M{sx:.1f},{sy:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}" marker-end="url(#ih-h3)"/>')
            lx, ly = (x1 + x2) / 2 + nx * 34 * side, (y1 + y2) / 2 + ny * 34 * side
            out.append(f'<text class="ih-lab {cls}" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">{groups[step]}</text>')
    for r, (x, y) in pos.items():
        up = -1 if r == 0 else 1
        out.append(f'<path class="ih-edge ih-e0" d="M{x - 12},{y + up * (R - 4)} C{x - 30},{y + up * (R + 36)} {x + 30},{y + up * (R + 36)} {x + 12},{y + up * (R - 2)}" marker-end="url(#ih-h3)"/>')
        out.append(f'<text class="ih-lab" x="{x}" y="{y + up * (R + 40) + (0 if up < 0 else 10)}" text-anchor="middle">{groups[0]}</text>')
        cls = "ih-state ih-start" if r == 0 else "ih-state"
        out.append(f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="{R}"/><text x="{x}" y="{y + 6}" text-anchor="middle">{r}</text></g>')
    return "".join(out) + "</svg>"


def fan_svg() -> str:
    """Two states of the mod 97 machine and their 10 edges: 1 goes to 10..19, and 96 to
    (960 + d) mod 97 = 87..96, which wraps around."""
    W, H = 420, 330
    out = [f'<svg class="figure ih-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
           'aria-label="שני מצבים של מכונת השארית מודולו 97 : ממצב 1 עשר קשתות, לספרות 0 עד 9, אל המצבים 10 עד 19. '
           'ממצב 96 עשר קשתות אל המצבים 87 עד 96, כי 960 מודולו 97 הוא 87">', _arrow_defs("ih-hf")]
    for col, (src, x0) in enumerate(((1, 40), (96, 236))):
        sy = 160
        out.append(f'<g class="ih-state ih-src"><circle cx="{x0}" cy="{sy}" r="22"/><text x="{x0}" y="{sy + 6}" text-anchor="middle">{src}</text></g>')
        for d in range(10):
            ty = 18 + d * 32
            tx = x0 + 132
            t = step_hw(src, d)
            out.append(f'<path class="ih-edge" d="M{x0 + 22},{sy} C{x0 + 70},{sy} {x0 + 70},{ty} {tx - 20},{ty}" marker-end="url(#ih-hf)"/>')
            out.append(f'<text class="ih-lab" x="{x0 + 92}" y="{ty - 4}" text-anchor="middle">{d}</text>')
            out.append(f'<g class="ih-state ih-small"><circle cx="{tx}" cy="{ty}" r="15"/><text x="{tx}" y="{ty + 5}" text-anchor="middle">{t}</text></g>')
    return "".join(out) + "</svg>"


def datapath_svg() -> str:
    """The block diagram of the 14 flip-flop checker: the two registers, the multiplexer that
    picks h in the head and r after it, 8x + 2x + d, the four compare-and-subtract stages,
    the head's count kept in r (97 + k), and at the last digit (27 r + h) mod 97 = 1."""
    W, H = 400, 470
    def box(x, y, w, h, text, cls="ih-blk", sub=""):
        t = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
        t += f'<text x="{x + w / 2:g}" y="{y + h / 2 + (0 if sub else 5):g}" text-anchor="middle">{text}</text>'
        if sub:
            t += f'<text class="ih-sub" x="{x + w / 2:g}" y="{y + h / 2 + 15:g}" text-anchor="middle">{sub}</text>'
        return t + "</g>"
    def line(pts, arrow=True, cls="ih-wire"):
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        return f'<path class="{cls}" d="{d}"' + (' marker-end="url(#ih-hb)"' if arrow else "") + "/>"
    o = [f'<svg class="figure ih-fig ih-dp" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         'aria-label="תרשים המלבנים של הבודק עם 14 פליפ-פלופים : שני רגיסטרים של 7 ביטים, h ו-r. מרבב בוחר את h בזמן הראש '
         'ואת r אחריו, מחשבים 8x ועוד 2x ועוד d, ואז ארבעה שלבים של השוואה וחיסור של 776, 388, 194 ו-97. בזמן הראש r סופר '
         '97 ועוד k. בספרה האחרונה מחשבים 27r ועוד h מודולו 97 ובודקים שזה 1">', _arrow_defs("ih-hb")]
    o.append(box(150, 10, 100, 30, "d[3:0]", "ih-blk ih-in"))
    o.append(box(30, 60, 110, 40, "h", "ih-blk ih-reg", "7 D flip-flops"))
    o.append(box(260, 60, 110, 40, "r", "ih-blk ih-reg", "7 D flip-flops"))
    o.append(box(150, 128, 100, 34, "mux: r ≥ 97 ?", "ih-blk ih-mux"))
    o.append(line([(85, 100), (85, 145), (150, 145)]))
    o.append(line([(315, 100), (315, 145), (250, 145)]))
    o.append(box(110, 186, 180, 40, "8x + 2x + d", "ih-blk ih-add", "two adders, ≤ 969"))
    o.append(line([(200, 162), (200, 186)]))
    o.append(line([(200, 40), (200, 52), (380, 52), (380, 206), (290, 206)]))
    for k, m in enumerate((776, 388, 194, 97)):
        x = 16 + k * 94
        o.append(box(x, 250, 86, 40, f"≥ {m} ?", "ih-blk ih-stage", f"− {m}"))
        if k:
            o.append(line([(x - 8, 270), (x, 270)]))
    o.append(line([(200, 226), (200, 238), (59, 238), (59, 250)]))
    o.append(box(110, 314, 180, 40, "write h or r", "ih-blk ih-mux", "head: r ← r + 1"))
    o.append(line([(345, 290), (345, 304), (290, 324)]))
    o.append(line([(110, 334), (14, 334), (14, 80), (30, 80)]))
    o.append(line([(290, 334), (392, 334), (392, 80), (370, 80)]))
    o.append(box(30, 380, 150, 40, "27r + h", "ih-blk ih-add", "at the last digit"))
    o.append(box(200, 380, 90, 40, "5 stages", "ih-blk ih-stage", "mod 97"))
    o.append(box(310, 380, 70, 40, "= 1 ?", "ih-blk ih-out", "ok"))
    o.append(line([(180, 400), (200, 400)]))
    o.append(line([(290, 400), (310, 400)]))
    o.append(f'<text class="ih-sub" x="200" y="452" text-anchor="middle">critical path: mux, two adders, four stages</text>')
    return "".join(o) + "</svg>"


def legend_mod3() -> str:
    return ('<span class="viz-legend"><span><i class="ih-key-start"></i>ההתחלה, ומתחלק ב-3</span>'
            '<span><i class="ih-key-e0"></i>ספרות שלא משנות את השארית</span><span><i class="ih-key-e1"></i>מוסיפות 1</span>'
            '<span><i class="ih-key-e2"></i>מוסיפות 2</span></span>')


VERSION_ROWS = (
    ("buffer", "שומרים את 6 ספרות הראש ומכניסים אותן שוב בסוף", "24 + 3 + 7"),
    ("two", "שתי שאריות, h לראש ו-r לשאר, ומונה לראש", "7 + 7 + 3"),
    ("shared", "המונה בתוך r, שלא בשימוש בזמן הראש, ועוד ביט של שלב", "7 + 7 + 1"),
    ("codes", "הערכים 97 עד 102 של r הם שלבי הראש", "7 + 7"),
)


def versions_table() -> str:
    il = stream(IL)
    rows = ["| הגרסה | פליפ-פלופים | שעונים ל-IBAN הישראלי |", "|---|:-:|:-:|"]
    for (key, text, parts), (_, run) in zip(VERSION_ROWS, VERSIONS):
        ok, clocks, ff = run(il)
        assert ok and ff == sum(int(x) for x in parts.split(" + "))
        rows.append(f"| {text} | {RLM}{L(f'{parts} = {ff}')} | {clocks} |")
    return "\n".join(rows)


def faster_table() -> str:
    il = norm(IL)
    digits = len(stream(IL))
    rest = digits - HEAD
    pairs = HEAD // 2 + (rest + 1) // 2
    rows = ["| בכל שעון | הצעד | השלבים | שעונים ל-IBAN הישראלי |", "|---|---|:-:|:-:|",
            f"| ספרה, 4 ביטים | {RLM}{L('(10r + d) mod 97')} | 4 | {digits} |",
            f"| תו, 6 ביטים, אות כערך אחד | {RLM}{L('(3r + v) mod 97')} לאות | 4 | {len(il)} |",
            f"| שתי ספרות, 8 ביטים | {RLM}{L('(3r + 10a + b) mod 97')} | 2 | {pairs} |"]
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        moved_table(),
        running_grid(),
        mod3_svg(),
        legend_mod3(),
        fan_svg(),
        datapath_svg(),
        versions_table(),
        faster_table(),
        check_table(),
        moduli_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
