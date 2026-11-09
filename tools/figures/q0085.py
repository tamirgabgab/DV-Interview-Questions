#!/usr/bin/env python3
"""Figures and tables of question 0085: the self-describing number.

    python tools/figures/fill.py 85        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the test compares the
two): a number of b digits in base b is a list d[0..b-1], self-describing when d[i] is how
many times the digit i appears in it. The search fills the digits from position 0, each
value from 0 up, and cuts a value (and every larger one) when the digits so far add up to
more than b or the weighted sum sum(i * d[i]) does. The box (docs/javascripts/explorer/
selfdesc.js) steps through the same events: a cut or a full candidate checked.
"""

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

NB = " "
RLM = "‏"
DIGITS = "0123456789ABCDEFG"
BASES = range(2, 17)


# --- the model -----------------------------------------------------------------------------------

def counts(d):
    """counts[i]: how many times the digit i appears in d."""
    return [sum(1 for x in d if x == i) for i in range(len(d))]


def is_self(d):
    return counts(d) == list(d)


def text(d):
    return "".join(DIGITS[x] for x in d)


def events(b):
    """The search in order: ("cut", prefix, value) when value at position len(prefix) makes
    a sum pass b (the larger values are cut with it), ("check", digits, ok) for every full
    candidate. Returns the events."""
    out = []

    def rec(pre, total, weight):
        i = len(pre)
        if i == b:
            out.append(("check", tuple(pre), is_self(pre)))
            return
        for v in range(b):
            if total + v > b or weight + i * v > b:
                out.append(("cut", tuple(pre), v))
                return
            rec(pre + [v], total + v, weight + i * v)

    rec([], 0, 0)
    return out


def search(b):
    """(the solutions in search order, full candidates checked, cuts)."""
    ev = events(b)
    sols = [list(d) for kind, d, ok in ev if kind == "check" and ok]
    return sols, sum(1 for e in ev if e[0] == "check"), sum(1 for e in ev if e[0] == "cut")


def family(b):
    """The classification of part c: b >= 7 one number, (b - 4) 2 1 0 ... 0 1 0 0 0; base 4
    two, base 5 one; bases 2, 3 and 6 none."""
    if b >= 7:
        d = [0] * b
        d[0], d[1], d[2], d[b - 4] = b - 4, 2, 1, 1
        return [d]
    return {4: [[1, 2, 1, 0], [2, 0, 2, 0]], 5: [[2, 1, 2, 0, 0]]}.get(b, [])


def cases(b):
    """Part b's case analysis for base b, by z = d[0], the number of zeros: (z, the count of
    ones d[1] the case forces, whether a number of that case exists in base b)."""
    sols = family(b)
    return [(1, b - 2, any(d[0] == 1 for d in sols)), (2, b - 4, any(d[0] == 2 for d in sols)),
            ("≥ 3", 2, any(d[0] >= 3 for d in sols))]


# --- the blocks ----------------------------------------------------------------------------------

def digit_table(d, label, marks=(), cls="sd-tab"):
    """A left-to-right table: the positions i, the digits d[i], and the real count of each i;
    a count that differs from d[i] is marked, marks are positions to frame."""
    c = counts(d)
    head = "".join(f'<td class="gs-b sd-ix">{i}</td>' for i in range(len(d)))
    dig = "".join(f'<td class="gs-b is-one{" is-mark" if i in marks else ""}">{DIGITS[x]}</td>' for i, x in enumerate(d))
    cnt = "".join(f'<td class="gs-b{" sd-bad" if c[i] != d[i] else " sd-ok"}">{DIGITS[c[i]] if c[i] < len(DIGITS) else c[i]}</td>'
                  for i in range(len(d)))
    return (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
            f'<table class="gs-bits {cls}" dir="ltr" aria-label="{escape(label)}"><tbody>'
            f'<tr class="sd-ixrow"><th>i</th>{head}</tr><tr><th>d[i]</th>{dig}</tr><tr><th>count(i)</th>{cnt}</tr>'
            "</tbody></table></div>")


def legend(extra=""):
    return ('<span class="viz-legend"><span><i class="gs-key-one"></i><span>הספרה <code>d[i]</code> במקום <code>i</code></span></span>'
            '<span><i class="sd-key-ok"></i><span>כמה פעמים הספרה <code>i</code> באמת מופיעה, ומתאים</span></span>'
            + extra + "</span>")


def statement_table():
    return digit_table([1, 2, 1, 0], "המספר 1210 בבסיס 4 : במקום 0 הספרה 1 ובאמת יש אפס אחד, במקום 1 הספרה 2 "
                       "ויש שני אחדים, במקום 2 הספרה 1 ויש שתיים אחת, במקום 3 הספרה 0 ואין אף שלוש")


def answer_table():
    d = family(10)[0]
    return digit_table(d, f"המספר {text(d)} : שישה אפסים, שני אחדים, שתיים אחת, אפס שלשות, חמישיות ושביעיות, ושש אחת")


def cases_table():
    b = 10
    rows = [f"| {RLM}\\( z = d_0 \\) | מה (*) מכריח | כמה אחדים | אפשר? |", "|:-:|---|---|:-:|"]
    forced = {1: "שתיים אחת, ואין ספרה גדולה מ-2", 2: "שתי ספרות 2, ואין ספרה גדולה מ-2",
              "≥ 3": f"הספרה {RLM}\\( z \\) מופיעה פעם אחת, יש שתיים אחת, ואין עוד ספרה גדולה מ-2"}
    for z, ones, ok in cases(b):
        if z == "≥ 3":
            zz = f"{RLM}\\( z \\ge 3 \\)"
            need = f"{RLM}\\( d_1 = 2 \\), ואז \\( z = {b} - 4 = {b - 4} \\)"
        else:
            zz = f"{RLM}\\( z = {z} \\)"
            need = f"{RLM}\\( d_1 = {ones} \\) : ספרה גדולה מ-2, שאסור שתופיע"
        rows.append(f"| {zz} | {forced[z]} | {need} | {'כן' if ok else 'לא'} |")
    return "\n".join(rows)


def bases_table():
    rows = ["| בסיס | המספרים | לפי התבנית | מועמדים מלאים שנבדקו |", "|:-:|:-:|:-:|:-:|"]
    for b in BASES:
        sols, checked, _ = search(b)
        nums = ", ".join(text(d) for d in sols) or "אין"
        if len(sols) > 1:
            nums = f'{RLM}<span dir="ltr">{nums}</span>'      # two numbers, in reading order
        elif sols:
            nums = RLM + nums          # a cell that starts with a digit or a Latin letter
        pattern = "כן" if b >= 7 else "‏–"
        rows.append(f"| {RLM}{b} | {nums} | {pattern} | {RLM}{checked:,} |")
    return "\n".join(rows)


def pattern_table():
    b = 12
    d = family(b)[0]
    return digit_table(d, f"המספר בבסיס {b} : במקום 0 הספרה {b - 4}, במקום 1 הספרה 2, במקום 2 הספרה 1, "
                       f"ובמקום {b - 4} הספרה 1. כל השאר אפסים",
                       marks=(0, 1, 2, b - 4))


def pattern_legend():
    return legend('<span><i class="sd-key-mark"></i><span>ארבעת המקומות שאינם אפס : '
                  '<code>b − 4</code>, <code>2</code>, <code>1</code> ו-<code>1</code></span></span>')


def search_table():
    rows = ["| בסיס b | מחרוזות של b ספרות | מועמדים מלאים שנבדקו | חיתוכים | פתרונות |", "|:-:|:-:|:-:|:-:|:-:|"]
    for b in (4, 5, 6, 7, 8, 9, 10):
        sols, checked, cuts = search(b)
        rows.append(f"| {RLM}{b} | {RLM}{b ** b:,} | {RLM}{checked:,} | {RLM}{cuts:,} | {RLM}{len(sols)} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        statement_table() + "\n\n" + legend(),
        answer_table() + "\n\n" + legend(),
        search_table(),
        cases_table(),
        pattern_table() + "\n\n" + pattern_legend(),
        bases_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
