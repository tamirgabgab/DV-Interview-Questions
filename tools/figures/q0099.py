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
# the made-up Israeli account of part d
BANK, BRANCH, ACCOUNT = 12, 345, 6789012


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


def israeli(bank: int, branch: int, account: int) -> str:
    bban = f"{bank:03d}{branch:03d}{account:013d}"
    return "IL" + check_digits("IL00" + bban) + bban


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


def structure_table() -> str:
    """The Israeli IBAN as a strip of its five parts, each with its own tint, and a table of
    what each part holds."""
    s = norm(IL)
    parts = [("ib-cc", s[:2], "קוד המדינה"), ("ib-ck", s[2:4], "ספרות ביקורת"), ("ib-bk", s[4:7], "בנק"),
             ("ib-br", s[7:10], "סניף"), ("ib-ac", s[10:], "חשבון")]
    strip = "".join(f'<td class="gs-b ib-seg {c}">{v}</td>' for c, v, _ in parts)
    label = "המבנה של IBAN ישראלי : קוד המדינה IL, שתי ספרות ביקורת, 3 ספרות בנק, 3 ספרות סניף ו-13 ספרות חשבון, 23 תווים"
    rows = ["| החלק | תווים | ב-IBAN לדוגמה |", "|---|:-:|:-:|"]
    for c, v, name in parts:
        rows.append(f'| <i class="ib-sw {c}"></i>{name} | {len(v)} | {RLM}{L(v)} |')
    rows.append(f"| סך הכול | {len(s)} | |")
    return (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
            f'<table class="gs-bits ib-tab ib-struct" dir="ltr" aria-label="{escape(label)}"><tbody>'
            f"<tr>{strip}</tr></tbody></table></div>\n\n" + "\n".join(rows))


def build_table() -> str:
    bban = f"{BANK:03d}{BRANCH:03d}{ACCOUNT:013d}"
    m = mod97("IL00" + bban)
    ib = israeli(BANK, BRANCH, ACCOUNT)
    rows = ["| השלב | התוצאה |", "|---|---|",
            f"| בנק, סניף וחשבון (מומצאים) | {RLM}{L(f'{BANK:03d}')}, {L(f'{BRANCH:03d}')}, {L(ACCOUNT)} |",
            f"| החשבון באפסים מקדימים ל-13 ספרות | {RLM}{L(f'{ACCOUNT:013d}')} |",
            f"| ‏{L('IL00')} ואחריו 19 הספרות | {RLM}{L(grouped('IL00' + bban))} |",
            f"| השארית בחלוקה ל-97 אחרי ההעברה | {m} |",
            f"| ספרות הביקורת, 98 פחות השארית | {98 - m:02d} |",
            f"| ה-IBAN | {RLM}{L(grouped(ib))} |"]
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        moved_table(),
        running_grid(),
        check_table(),
        moduli_table(),
        structure_table(),
        build_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
