#!/usr/bin/env python3
"""Figures and tables of question 0051 (a poisoned bottle among n, mice that die a day
after drinking, one round, two rounds and b rounds).

    python tools/figures/fill.py 51        # put the blocks on the page

The reference here is independent of the page code: needed(n, b) is the smallest m with
(b + 1)^m >= n found by trying m = 0, 1, ...; outcome(x, m, b) plays the rounds with the
mice that are still alive; decode() reads the digits back. blocks() returns, in page
order: the figure of the ten mice for bottle 613 in one round, its table, the table of
the two rounds for the same bottle, and the table of the mice needed for 1000 bottles
against the number of rounds. tests/0051 checks the page code against these.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

N = 1000
BOTTLE = 613
RLM = "‏"


# --- the model ---------------------------------------------------------------------------

def needed(n, b):
    """The fewest mice for n bottles in b rounds: each mouse ends in one of b + 1 ways
    (dies in round 1, ..., dies in round b, survives)."""
    m = 0
    while (b + 1) ** m < n:
        m += 1
    return m


def digits(x, base, m):
    """The m digits of x in the base, the least significant first (mouse 0 first)."""
    return [x // base ** i % base for i in range(m)]


def outcome(x, m, b):
    """Mouse i drinks from bottle y in round d when the i-th digit of y is d >= 1, and
    never when it is 0; the round each mouse dies in (0: it survives) when x is poisoned.
    A dead mouse drinks no more, which never matters: it already told its digit."""
    death = [0] * m
    for r in range(1, b + 1):
        for i in range(m):
            if not death[i] and digits(x, b + 1, m)[i] == r:
                death[i] = r
    return death


def decode(death, b):
    return sum(d * (b + 1) ** i for i, d in enumerate(death))


# --- blocks ------------------------------------------------------------------------------

def mice_figure():
    """The ten mice of part a for bottle 613: the bit of each mouse, the dead ones dark."""
    m = needed(N, 1)
    bits, death = digits(BOTTLE, 2, m), outcome(BOTTLE, m, 1)
    W, gap = 640, 60
    x0 = W - 40                                   # mouse 0 (the lowest bit) on the right
    s = (f'<svg class="figure mc-fig" viewBox="0 0 {W} 150" style="max-width:40rem" role="img" '
         f'aria-label="עשרה עכברים, ביט לכל אחד : בבקבוק {BOTTLE} מתים העכברים של הביטים שהם 1">')
    for i in range(m):
        x = x0 - i * gap
        dead = death[i] == 1
        s += (f'<g class="mc-mouse{" is-dead" if dead else ""}"><title>mouse {i}: bit {bits[i]}, {"dies" if dead else "lives"}</title>'
              f'<circle cx="{x}" cy="62" r="22"/><text x="{x}" y="68" text-anchor="middle">{bits[i]}</text></g>'
              f'<text class="tick" x="{x}" y="24" text-anchor="middle">2^{i}</text>'
              f'<text class="tick" x="{x}" y="112" text-anchor="middle">{"✗" if dead else "✓"}</text>')
    s += f'<text class="legend" x="{W - 8}" y="142" text-anchor="end">{BOTTLE} = 1001100101 (binary)</text>'
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="mc-key-dead"></i>עכבר שמת : הביט שלו 1</span>'
            '<span><i class="mc-key-live"></i>עכבר ששרד : הביט שלו 0</span></span>')


def one_round_table():
    m = needed(N, 1)
    bits, death = digits(BOTTLE, 2, m), outcome(BOTTLE, m, 1)
    rows = ["| העכבר | ערך הביט | הביט של 613 | התוצאה |", "|:-:|:-:|:-:|:-:|"]
    for i in range(m - 1, -1, -1):
        rows.append(f"| {RLM}{i} | {RLM}{2 ** i} | {RLM}{bits[i]} | {'מת' if death[i] else 'שרד'} |")
    return "\n".join(rows)


def two_rounds_table():
    m, b = needed(N, 2), 2
    ds, death = digits(BOTTLE, 3, m), outcome(BOTTLE, m, b)
    say = {1: "שותה בסבב 1", 2: "שותה בסבב 2", 0: "לא שותה"}
    end = {1: "מת בסבב 1", 2: "מת בסבב 2", 0: "שרד"}
    rows = ["| העכבר | ערך הספרה | הספרה של 613 | מבקבוק 613 | התוצאה |", "|:-:|:-:|:-:|:-:|:-:|"]
    for i in range(m - 1, -1, -1):
        rows.append(f"| {RLM}{i} | {RLM}{3 ** i} | {RLM}{ds[i]} | {say[ds[i]]} | {end[death[i]]} |")
    return "\n".join(rows)


def rounds_table():
    rows = ["| הסבבים b | התוצאות לעכבר | העכברים ל-1000 בקבוקים | כמה בקבוקים הם מכסים |", "|:-:|:-:|:-:|:-:|"]
    for b in range(1, 10):
        m = needed(N, b)
        rows.append(f"| {RLM}{b} | {RLM}{b + 1} | {RLM}{m} | {RLM}{(b + 1) ** m:,} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [mice_figure(), legend(), one_round_table(), two_rounds_table(), rounds_table()]


if __name__ == "__main__":
    print(needed(N, 1), needed(N, 2), digits(BOTTLE, 3, 7), outcome(BOTTLE, 7, 2))
    print("\n\n".join(blocks()))
