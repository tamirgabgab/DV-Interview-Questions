#!/usr/bin/env python3
"""Figures and tables of question 0107, the largest number from concatenation: arrange
non-negative integers so that writing them one after another gives the largest number (part a
and b), or the smallest one with no leading zero (part c).

    python tools/figures/fill.py 107        # put the blocks on the page

The references here are independent of the page code:

- rho(a) is the exact rational a / (10^|a| - 1) of a digit string a, the number 0.aaaa... whose
  digits are a repeated forever; largest(nums) sorts by it (descending) and joins.
- largest_brute(nums) and smallest_brute(nums) try every order (the smallest skips an order
  that starts with "0" unless every number is 0).
- smallest(nums) is part c's rule: every distinct non-zero value as the first, then the zeros,
  then the rest in ascending rho; the smallest candidate.
- shortcut(nums) is the familiar wrong rule of part c: sort ascending and move the first
  non-zero string to the front; num_sort and str_sort are the naive sorts of part a.

blocks() returns, in page order: part a's table of the three sorts on the example and the table
of its adjacent pairs, part b's table of the values rho, the number line of the example and its
legend, part c's table of the candidates of [0, 2, 21] and the table of the brute force against
the shortcut and the rule.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from functools import cmp_to_key
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "
CAT = "‖"                     # concatenation, as the page writes it

EXAMPLE = [3, 30, 34, 5, 9]          # the statement: 9534330
TIE = [12, 1212]                     # equal rho: 4/33
ZEROS = [0, 0]                       # "0", not "00"
SMALL = [[0, 1, 10], [3, 30, 34, 5, 9], [0, 0, 1], [20, 1, 0], [0, 2, 21]]   # part c, the lead's brute force and the shortcut's failure
SHORT_FAIL = [0, 2, 21]              # the shortcut gives 2102, the answer is 2021


# --- the reference ----------------------------------------------------------------------------------

def rho(a: str) -> Fraction:
    """The rational number of a digit string: a / (10^|a| - 1), that is 0.aaaa..."""
    return Fraction(int(a), 10 ** len(a) - 1)


def strings(nums) -> list[str]:
    return [str(x) for x in nums]


def largest(nums) -> str:
    """Sorted by rho, descending, and joined; all zeros give "0"."""
    out = "".join(sorted(strings(nums), key=rho, reverse=True))
    return "0" if out[0] == "0" else out


def largest_brute(nums) -> str:
    best = max("".join(p) for p in permutations(strings(nums)))
    return "0" if best[0] == "0" else best


def smallest_brute(nums) -> str:
    """The smallest join of an order that does not start with "0" ("0" when every number is 0)."""
    s = strings(nums)
    if all(x == "0" for x in s):
        return "0"
    return min("".join(p) for p in permutations(s) if p[0] != "0")


def ascending(nums) -> list[str]:
    return sorted(strings(nums), key=rho)


def candidates(nums) -> list[tuple[str, str]]:
    """Part c: (first value, candidate) for every distinct non-zero value, the rest after the zeros
    in ascending rho."""
    s = ascending(nums)
    z = s.count("0")
    rest = [x for x in s if x != "0"]
    out, seen = [], set()
    for i, x in enumerate(rest):
        if x in seen:
            continue
        seen.add(x)
        out.append((x, x + "0" * z + "".join(rest[:i] + rest[i + 1:])))
    return out


def smallest(nums) -> str:
    c = candidates(nums)
    return min(v for _, v in c) if c else "0"


def shortcut(nums) -> str:
    """The wrong rule: ascending, then the first non-zero string moved to the front."""
    s = ascending(nums)
    i = next((k for k, x in enumerate(s) if x != "0"), None)
    if i is None:
        return "0"
    return "".join([s[i]] + s[:i] + s[i + 1:])


def block_rule(nums) -> str:
    """The faster rule of the follow-up (checked by the tests, not proved on the page): the first is
    the non-zero x whose block x + 0^z is smallest by rho, the longest x on a tie."""
    s = strings(nums)
    z = s.count("0")
    nz = [x for x in s if x != "0"]
    if not nz:
        return "0"
    x = min(nz, key=lambda t: (rho(t + "0" * z), -len(t)))
    rest = list(nz)
    rest.remove(x)
    return x + "0" * z + "".join(sorted(rest, key=rho))


def num_sort(nums, desc=True) -> list[str]:
    return strings(sorted(nums, reverse=desc))


def str_sort(nums, desc=True) -> list[str]:
    return sorted(strings(nums), reverse=desc)


def bool_cmp_sort(nums) -> str:
    """The trap: a comparator that returns a bool. It is never negative, so the sort sees every pair as
    "not less" and keeps the input order."""
    return "".join(sorted(strings(nums), key=cmp_to_key(lambda a, b: a + b < b + a)))


# --- formatting -----------------------------------------------------------------------------------------

def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def arr(xs) -> str:
    return ltr("[" + ", ".join(str(x) for x in xs) + "]")


def cat(xs) -> str:
    return ltr(f" {CAT} ".join(xs))


def dec(a: str, places: int = 6) -> str:
    """0.aaaa... cut after `places` digits, "1" for 9..9 and "0" for 0."""
    if set(a) == {"9"}:
        return "1"
    if a == "0":
        return "0"
    return "0." + (a * places)[:places] + "…"


def first_diff(a: str, b: str) -> int:
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), -1)


def marked(s: str, want: str) -> str:
    """s with its first digit that differs from want in bold."""
    i = first_diff(s, want)
    if i < 0:
        return s
    return f"{s[:i]}<b>{s[i]}</b>{s[i + 1:]}"


# --- part a ------------------------------------------------------------------------------------------

def sorts_table() -> str:
    want = largest(EXAMPLE)
    rows = [("מיון של המספרים, מהגדול לקטן", num_sort(EXAMPLE)),
            ("מיון של המחרוזות, מהגדולה לקטנה", str_sort(EXAMPLE)),
            (f"{RLM}\\( a \\Vert b \\) מול \\( b \\Vert a \\)", ascending(EXAMPLE)[::-1])]
    out = ["| המיון | הסדר | השרשור | התוצאה |", "|---|:-:|:-:|:-:|"]
    for name, order in rows:
        s = "".join(order)
        ok = "הגדול ביותר" if s == want else ("קטן יותר" if s < want else "גדול יותר")
        out.append(f"| {name} | {RLM}{cat(order)} | {RLM}{ltr(marked(s, want))} | {ok} |")
    return "\n".join(out)


def pairs_table() -> str:
    order = ascending(EXAMPLE)[::-1]
    out = [f"| הזוג | {RLM}\\( a \\Vert b \\) | {RLM}\\( b \\Vert a \\) | ההשוואה |", "|:-:|:-:|:-:|:-:|"]
    for a, b in zip(order, order[1:]):
        ab, ba = a + b, b + a
        sign = ">" if ab > ba else "=" if ab == ba else "<"
        out.append(f"| {RLM}{ltr(f'{a}, {b}')} | {ab} | {ba} | {RLM}{ltr(f'{ab} {sign} {ba}')} |")
    return "\n".join(out)


# --- part b ------------------------------------------------------------------------------------------

def rho_table() -> str:
    order = ascending(EXAMPLE)[::-1]
    out = [f"| המספר \\( a \\) | האורך | {RLM}\\( a / (10^{{\\lvert a \\rvert}} - 1) \\) | בצורה עשרונית | המקום בתשובה |",
           "|:-:|:-:|:-:|:-:|:-:|"]
    for a in sorted(strings(EXAMPLE), key=lambda t: (-rho(t), t)):
        r = rho(a)
        frac = f"{a}/{10 ** len(a) - 1}"
        if r.denominator != 10 ** len(a) - 1:
            frac += f" = {r.numerator}/{r.denominator}" if r.denominator != 1 else f" = {r.numerator}"
        out.append(f"| {a} | {len(a)} | {RLM}{ltr(frac)} | {RLM}{ltr(dec(a))} | {order.index(a) + 1} |")
    return "\n".join(out)


def number_line(nums, label: str, desc: bool = True) -> str:
    """The values rho on [0, 1]: a dot per distinct value, the numbers in a row under the line in
    ascending rho, each joined to its dot, with its place in the answer (from the largest when
    desc, else from the smallest)."""
    s = strings(nums)
    W, H, X0, X1, AY, LY = 640, 150, 34, 606, 46, 112
    X = lambda v: X0 + float(v) * (X1 - X0)  # noqa: E731
    up = sorted(s, key=lambda t: (rho(t), t))
    order = sorted(s, key=rho, reverse=desc)
    n = len(up)
    o = [f'<svg class="figure cc-line" viewBox="0 0 {W} {H}" style="max-width:40rem" direction="ltr" role="img" aria-label="{label}">']
    o.append(f'<line class="cc-axis" x1="{X0}" x2="{X1}" y1="{AY}" y2="{AY}"/>')
    for k in range(11):
        x = X(Fraction(k, 10))
        big = k in (0, 5, 10)
        o.append(f'<line class="cc-tick" x1="{x:.1f}" x2="{x:.1f}" y1="{AY - (7 if big else 4)}" y2="{AY + (7 if big else 4)}"/>')
        if big:
            o.append(f'<text class="cc-tl" x="{x:.1f}" y="{AY - 13}" text-anchor="middle">{["0", "0.5", "1"][k // 5]}</text>')
    slot = (X1 - X0) / n
    for i, a in enumerate(up):
        xd, xl = X(rho(a)), X0 + (i + 0.5) * slot
        o.append(f'<line class="cc-lead" x1="{xd:.1f}" y1="{AY + 6}" x2="{xl:.1f}" y2="{LY - 17}"/>')
    for v in sorted({rho(a) for a in s}):
        o.append(f'<circle class="cc-dot" cx="{X(v):.1f}" cy="{AY}" r="5"><title>{v.numerator}/{v.denominator}</title></circle>')
    for i, a in enumerate(up):
        xl = X0 + (i + 0.5) * slot
        w = 14 + 9 * len(a)
        place = order.index(a) + 1
        o.append(f'<g class="cc-lab"><title>{a}: {int(a)}/{10 ** len(a) - 1}, place {place}</title>'
                 f'<rect x="{xl - w / 2:.1f}" y="{LY - 16}" width="{w}" height="24" rx="5"/>'
                 f'<text class="cc-num" x="{xl:.1f}" y="{LY + 1}" text-anchor="middle">{a}</text>'
                 f'<circle class="cc-place" cx="{xl:.1f}" cy="{LY + 23}" r="9"/>'
                 f'<text class="cc-pl" x="{xl:.1f}" y="{LY + 27}" text-anchor="middle">{place}</text></g>')
    o.append("</svg>")
    return "".join(o)


def line_legend() -> str:
    return ('<span class="viz-legend"><span><i class="cc-key-dot"></i><span>הערך \\( a / (10^{\\lvert a \\rvert} - 1) \\) של מספר, על הקטע מ-0 עד 1</span></span>'
            '<span><i class="cc-key-lab"></i>המספרים לפי הסדר של הערכים, וכל אחד מחובר לנקודה שלו</span>'
            f'<span><i class="cc-key-place"></i>המקום בתשובה{NB}: הגדול ביותר נקרא מימין לשמאל</span></span>')


# --- part c ------------------------------------------------------------------------------------------

def cand_table(nums) -> str:
    c = candidates(nums)
    best = min(v for _, v in c)
    out = ["| הראשון | אחריו | המועמד | הבחירה |", "|:-:|:-:|:-:|:-:|"]
    s = ascending(nums)
    z = s.count("0")
    for x, v in c:
        rest = [t for t in s if t != "0"]
        rest.remove(x)
        after = cat(["0"] * z + rest)
        mark = "הקטן ביותר" if v == best else ""
        out.append(f"| {x} | {RLM}{after} | {RLM}{ltr(marked(v, best)) if v != best else f'**{v}**'} | {mark} |")
    return "\n".join(out)


def brute_table() -> str:
    out = ["| המספרים | מיון עולה | הכוח הגס | הזזת הראשון שאינו 0 | הכלל של סעיף ג |", "|:-:|:-:|:-:|:-:|:-:|"]
    for nums in SMALL:
        b = smallest_brute(nums)
        sc, ru = shortcut(nums), smallest(nums)
        up = "".join(ascending(nums))
        out.append(f"| {RLM}{arr(nums)} | {up} | **{b}** | {sc if sc == b else f'{RLM}{ltr(marked(sc, b))}, שגוי'} | {ru} |")
    return "\n".join(out)


# --- the blocks ----------------------------------------------------------------------------------------

def blocks():
    return [
        sorts_table(),
        pairs_table(),
        rho_table(),
        number_line(EXAMPLE, f"הערכים של הדוגמה על הקטע מ-0 עד 1{NB}: 30 ב-0.3030, 3 ב-0.3333, 34 ב-0.3434, 5 ב-0.5555 ו-9 ב-1. "
                    "בשורה שמתחת המספרים לפי הסדר של הערכים, והמקום של כל אחד בתשובה 9534330 מ-1 עד 5"),
        line_legend(),
        cand_table(SHORT_FAIL),
        brute_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
