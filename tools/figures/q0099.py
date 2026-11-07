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


def run_final(digits) -> tuple[bool, int, int]:
    """The page's checker with blocks of at most 10 bits: 17 flip-flops (h, r, and n, a counter
    of the tail). The head goes to h while r counts it in 97..102; the rest goes to r; after
    the last digit six clocks feed the digit 0, which multiplies r by 10^6; then
    r + h is 1 or 98 exactly when (R 10^6 + H) mod 97 = 1."""
    h, r = 0, 97
    for d in digits:
        if r >= 97:
            h = (10 * h + d) % 97
            r = 0 if r == 97 + HEAD - 1 else r + 1
        else:
            r = (10 * r + d) % 97
    if r >= 97:
        return False, len(digits), 17
    for _ in range(6):                          # the tail: n = 1..6
        r = (10 * r) % 97
    return r + h in (1, 98), len(digits) + 6, 7 + 7 + 3


VERSIONS = (("buffer", run_buffer), ("final", run_final))     # the two of the page and its box


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


def datapath_svg() -> str:
    """The block diagram of the checker (blocks of at most 10 bits and a mod 97 block): the
    registers h and r, the counter n of the tail; the control (head = r >= 97, tail = n > 0)
    drives the two multiplexers; one multiply-add and one mod 97; at the end y + h against 1
    and 98."""
    W, H = 400, 520
    def box(x, y, w, h, text, cls="ih-blk", sub=""):
        t = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
        t += f'<text x="{x + w / 2:g}" y="{y + h / 2 + (-2 if sub else 5):g}" text-anchor="middle">{text}</text>'
        if sub:
            t += f'<text class="ih-sub" x="{x + w / 2:g}" y="{y + h / 2 + 13:g}" text-anchor="middle">{sub}</text>'
        return t + "</g>"
    def line(pts, arrow=True, cls="ih-wire"):
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        return f'<path class="{cls}" d="{d}"' + (' marker-end="url(#ih-hb)"' if arrow else "") + "/>"
    def lab(x, y, t, anchor="middle"):
        return f'<text class="ih-wlab" x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'
    o = [f'<svg class="figure ih-fig ih-dp" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" '
         'aria-label="תרשים המלבנים של הבודק : שלושה רגיסטרים, h ו-r של 7 ביטים ומונה n של 3 ביטים. הבקרה מחשבת head כש-r לפחות 97 '
         'ו-tail כש-n גדול מ-0. מרבב בוחר את h בזמן הראש ואת r אחריו, מרבב שני מכניס 0 במקום הספרה בזמן הזנב, '
         'בלוק אחד מחשב 10x ועוד הספרה ובלוק אחד mod 97. התוצאה נכתבת ל-h בזמן הראש ול-r אחריו. בסוף בודקים אם y ועוד h '
         'שווה 1 או 98">', _arrow_defs("ih-hb")]
    # the registers and the control
    o.append(box(20, 14, 104, 44, "h", "ih-blk ih-reg", "7 flip-flops"))
    o.append(box(148, 14, 104, 44, "r", "ih-blk ih-reg", "7 flip-flops"))
    o.append(box(276, 14, 104, 44, "n", "ih-blk ih-reg", "3 flip-flops"))
    o.append(box(148, 84, 104, 30, "r ≥ 97 ?", "ih-blk ih-ctl"))
    o.append(box(276, 84, 104, 30, "n > 0 ?", "ih-blk ih-ctl"))
    o.append(line([(200, 58), (200, 84)]))
    o.append(line([(328, 58), (328, 84)]))
    o.append(lab(144, 128, "head", "end"))
    o.append(lab(326, 128, "tail", "end"))
    # the two multiplexers
    o.append(box(40, 150, 150, 36, "x = head ? h : r", "ih-blk ih-mux"))
    o.append(box(220, 150, 150, 36, "e = tail ? 0 : d", "ih-blk ih-mux"))
    o.append(line([(72, 58), (72, 150)]))
    o.append(line([(170, 58), (170, 70), (134, 70), (134, 150)]))
    o.append(line([(148, 114), (148, 132), (115, 132), (115, 150)]))
    o.append(line([(330, 114), (330, 132), (295, 132), (295, 150)]))
    o.append(lab(352, 134, "d[3:0]", "start"))
    o.append(line([(350, 138), (350, 150)]))
    # the arithmetic: one multiply-add, one mod 97
    o.append(box(90, 214, 220, 44, "s = 10x + e", "ih-blk ih-add", "≤ 969, 10 bits"))
    o.append(line([(115, 186), (115, 214)]))
    o.append(line([(295, 186), (295, 214)]))
    o.append(box(90, 284, 220, 44, "y = s mod 97", "ih-blk ih-stage", "0 .. 96"))
    o.append(line([(200, 258), (200, 284)]))
    # the write back
    o.append(box(40, 356, 320, 44, "head: h ← y, r ← r + 1 (0 after 102)", "ih-blk ih-mux", "rest and tail: r ← y; tail: n ← n + 1"))
    o.append(line([(200, 328), (200, 356)]))
    o.append(line([(40, 378), (8, 378), (8, 36), (20, 36)]))
    o.append(line([(360, 378), (392, 378), (392, 6), (200, 6), (200, 14)]))
    o.append(line([(328, 6), (328, 14)]))
    # the end: y + h against 1 and 98
    o.append(box(40, 432, 140, 44, "y + h", "ih-blk ih-add", "≤ 192"))
    o.append(box(220, 432, 140, 44, "= 1 or 98 ?", "ih-blk ih-out", "ok, n = 6"))
    o.append(line([(110, 400), (110, 432)]))
    o.append(line([(180, 454), (220, 454)]))
    o.append(f'<text class="ih-sub" x="200" y="506" text-anchor="middle">one clock: a mux, 10x + e, mod 97</text>')
    return "".join(o) + "</svg>"


def trace_rows(iban: str = IL):
    """The checker clock by clock: (clock, digit or 0, the register that goes in, 10x + e,
    mod 97, h, r, n)."""
    h, r, n, out = 0, 97, 0, []
    for k, d in enumerate(stream(iban), 1):
        if r >= 97:
            s = 10 * h + d
            h, r, reg = s % 97, (0 if r == 97 + HEAD - 1 else r + 1), "h"
        else:
            s = 10 * r + d
            r, reg = s % 97, "r"
        out.append((k, d, reg, s, s % 97, h, r, n))
    for _ in range(6):
        n += 1
        s = 10 * r
        r = s % 97
        out.append((out[-1][0] + 1, 0, "r", s, r, h, r, n))
    return out


def trace_table() -> str:
    rows = ["| שעון | נכנס | מה נכנס לבלוקים | ‏10x + e | ‏mod 97 | אחרי השעון |", "|:-:|:-:|---|:-:|:-:|---|"]
    tr = trace_rows()
    show = list(range(0, 10)) + [None] + [24] + list(range(25, 31))
    for i in show:
        if i is None:
            rows.append("| … | | | | | |")
            continue
        k, d, reg, s, y, h, r, n = tr[i]
        what = (f"ספרת ראש, ‏{L(f'x = h = {tr[i - 1][5] if i else 0}')}" if i < HEAD else
                f"ספרה, ‏{L(f'x = r = {tr[i - 1][6]}')}" if n == 0 else f"‏0 של הזנב, ‏{L(f'x = r = {tr[i - 1][6]}')}")
        after = L(f"h = {h}, r = {r}" + (f", n = {n}" if n else ""))
        rows.append(f"| {k} | {d} | {what} | {s} | {y} | {RLM}{after} |")
    k, d, reg, s, y, h, r, n = tr[-1]
    assert r + h == 98
    rows.append(f"| סוף | | ‏{L('y + h')} | | | {RLM}{L(f'{r} + {h} = {r + h}')}, תקין |")
    return "\n".join(rows)


def versions_table() -> str:
    """The way in and the way out, and the least with a wider multiplier."""
    il = stream(IL)
    ok1, c1, f1 = run_buffer(il)
    ok2, c2, f2 = run_final(il)
    ok3, c3, f3 = run_codes(il)
    assert ok1 and ok2 and ok3 and (f1, c1, f2, c2, f3, c3) == (34, 31, 17, 31, 14, 25)
    rows = ["| הבודק | פליפ-פלופים | שעונים ל-IBAN הישראלי |", "|---|:-:|:-:|",
            f"| שומרים את 6 ספרות הראש ומכניסים אותן שוב בסוף | {RLM}{L('24 + 7 + 3 = 34')} | {c1} |",
            f"| שארית לראש, שש ספרות 0 בסוף (הפתרון) | {RLM}{L('7 + 7 + 3 = 17')} | {c2} |",
            f"| עם מכפל של 12 ביטים, ‏{L('(27r + h) mod 97')} | {RLM}{L('7 + 7 = 14')} | {c3} |"]
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        moved_table(),
        running_grid(),
        datapath_svg(),
        trace_table(),
        versions_table(),
        check_table(),
        moduli_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
