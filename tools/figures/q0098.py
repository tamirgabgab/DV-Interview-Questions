#!/usr/bin/env python3
"""Figures and tables of question 0098, check digits: Luhn, the Israeli ID and ISBN-10.

    python tools/figures/fill.py 98        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Every number is computed here from the rules (the question's test checks
them against the page's code). The digit strips are SVG with one cell per digit, read left
to right; the doubled cells are filled (lu-dbl), the colliding columns marked (lu-hit).
Colours come from the site's palette through the lu-* classes of
docs/stylesheets/questions/0098-luhn.css.
"""

NB = " "
RLM = "‏"

CARD = "4111111111111111"          # the standard Visa test number, valid
ISBN = "0306406152"                # a published ISBN-10 (the example of the ISBN article)


def ltr(s):
    return f'<span dir="ltr">{s}</span>'


def doubled(d):
    """Luhn's map of a digit in a doubled place: 2d, minus 9 when that is two digits."""
    return 2 * d - 9 if 2 * d > 9 else 2 * d


def luhn_terms(number):
    """What each digit adds, left to right, and whether its place is doubled (every second
    digit counted from the right; the rightmost, the check digit, is not doubled)."""
    ds = [int(c) for c in number]
    n = len(ds)
    out = []
    for i, d in enumerate(ds):
        dbl = (n - 1 - i) % 2 == 1
        out.append((d, dbl, doubled(d) if dbl else d))
    return out


def luhn_sum(number):
    return sum(t for _, _, t in luhn_terms(number))


def isbn_terms(isbn):
    vals = [10 if c in "Xx" else int(c) for c in isbn]
    return [(c, 10 - i, (10 - i) * v) for i, (c, v) in enumerate(zip(isbn, vals))]


# --- the schemes of part ג: what one place adds for a digit, for the two kinds of places ---

def scheme_maps():
    """name -> (map of an odd place, map of an even place, modulus), counted from the right."""
    return {
        "luhn": (lambda d: d, doubled, 10),
        "w12": (lambda d: d, lambda d: 2 * d, 10),
        "ean": (lambda d: d, lambda d: 3 * d, 10),
        "isbn": (lambda d: d, lambda d: 2 * d, 11),     # two neighbours of ISBN-10 weigh w and w + 1
    }


def single_misses(name):
    """Ordered pairs (a, b), a != b, where a digit a changed to b slips by, in either place."""
    f, g, m = scheme_maps()[name]
    return [(a, b) for a in range(10) for b in range(10) if a != b
            and ((f(a) - f(b)) % m == 0 or (g(a) - g(b)) % m == 0)]


def swap_misses(name):
    """Unordered pairs {a, b} whose swap in two neighbouring places slips by."""
    f, g, m = scheme_maps()[name]
    return [(a, b) for a in range(10) for b in range(a + 1, 10)
            if (f(a) + g(b) - f(b) - g(a)) % m == 0]


SCHEMES = [
    ("luhn", RLM + "Luhn : כפל ב-2 וסכום ספרות".replace(" :", NB + ":")),
    ("w12", "משקלים 1 ו-2, בלי סכום ספרות"),
    ("ean", "ברקוד EAN-13, משקלים 1 ו-3"),
    ("isbn", RLM + "ISBN-10 : משקלים 10 עד 1, מודולו 11".replace(" :", NB + ":")),
]


# --- drawing -----------------------------------------------------------------------------

def strip(cells, rows, label, colw=21, x0=12, hit=()):
    """An SVG of len(cells) columns: rows is a list of (row label or "", values) with one value
    per column; cells[i] True fills column i as doubled; hit marks columns."""
    n = len(cells)
    lab = 0 if all(not r for r, _ in rows) else 58
    width = x0 + lab + n * colw + 8
    rowh = 30
    height = 10 + rowh * len(rows)
    s = (f'<svg class="lu-strip" viewBox="0 0 {width} {height}" role="img" aria-label="{label}">')
    for i in range(n):
        x = x0 + lab + i * colw
        cls = "lu-cell lu-hit" if i in hit else ("lu-cell lu-dbl" if cells[i] else "lu-cell")
        s += f'<rect class="{cls}" x="{x + 1}" y="5" width="{colw - 2}" height="{rowh * len(rows)}" rx="3"/>'
    for r, (name, vals) in enumerate(rows):
        y = 5 + rowh * r + rowh * 0.68
        if name:
            heb = any("\u0590" <= ch <= "\u05ff" for ch in name)
            # the label's right edge 6 to the left of the cells: a Hebrew label is right to
            # left and starts there, a Latin one is left to right and ends there
            way = 'direction="rtl" text-anchor="start"' if heb else 'direction="ltr" text-anchor="end"'
            s += f'<text class="lu-lab" x="{x0 + lab - 6}" y="{y:.1f}" {way}>{name}</text>'
        for i, v in enumerate(vals):
            x = x0 + lab + i * colw + colw / 2
            s += f'<text class="lu-t{" lu-sum" if r == len(rows) - 1 and name else ""}" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{v}</text>'
        if r < len(rows) - 1:
            yl = 5 + rowh * (r + 1)
            s += f'<line class="lu-rule" x1="{x0 + lab}" x2="{x0 + lab + n * colw}" y1="{yl}" y2="{yl}"/>'
    return s + "</svg>"


def card_strip():
    terms = luhn_terms(CARD)
    total = luhn_sum(CARD)
    label = (f"המספר {' '.join(CARD[i:i + 4] for i in range(0, 16, 4))}: ספרה בכל עמודה, והעמודות "
             f"המודגשות הן המקומות שמכפילים, כל ספרה שנייה מימין. השורה התחתונה היא מה שכל ספרה "
             f"מוסיפה. הסכום {total}, מתחלק ב-10, ולכן המספר תקין")
    svg = strip([dbl for _, dbl, _ in terms],
                [("", [d for d, _, _ in terms]), ("", [t for _, _, t in terms])], label)
    legend = (f'<span class="viz-legend"><span><i class="lu-key-dbl"></i><span>מקום שמכפילים</span></span>'
              f'<span><i class="lu-key-cell"></i><span>מקום שלא נוגעים בו</span></span></span>')
    return (f'<div class="lu-fig">{svg}</div>\n\n{legend}\n\n'
            f'{RLM}{ltr("4·2 = 8")} בעמודה הראשונה, ושבע פעמים {ltr("1·2 = 2")}. שאר הספרות נכנסות כמו '
            f'שהן{NB}: {ltr("8 + 7·2 + 8·1 = 30")}.')


def doubling_table():
    ds = list(range(10))
    dd = [doubled(d) for d in ds]
    delta = [(doubled(d) - d) % 10 for d in ds]
    label = ("שלוש שורות לכל ספרה d מ-0 עד 9: הספרה, מה שהיא מוסיפה במקום מוכפל, וההפרש בין השניים מודולו 10. "
             "השורה האמצעית היא כל הספרות מ-0 עד 9 בסדר אחר, ולכן כל טעות בספרה אחת נתפסת. בשורה התחתונה "
             "0 מופיע פעמיים, אצל 0 ואצל 9, ולכן ההחלפה של 09 ו-90 חומקת")
    svg = strip([False] * 10, [("d", ds), ("D(d)", dd), ("D−d", delta)], label, colw=29, x0=6, hit=(0, 9))
    legend = ('<span class="viz-legend"><span><i class="lu-key-hit"></i><span>אותו הפרש אצל {ltr("0")} ו-{ltr("9")}</span></span></span>')
    return f'<div class="lu-fig">{svg}</div>\n\n{legend}'


def isbn_strip():
    terms = isbn_terms(ISBN)
    total = sum(p for _, _, p in terms)
    label = (f"ה-ISBN {ISBN}: הספרות, המשקלים מ-10 עד 1 והמכפלות. הסכום {total}, שהוא {total // 11} כפול 11, "
             f"ולכן המספר תקין")
    svg = strip([False] * 10, [("ספרה", [c for c, _, _ in terms]), ("משקל", [w for _, w, _ in terms]),
                               ("מכפלה", [p for _, _, p in terms])], label, colw=29, x0=6)
    return (f'<div class="lu-fig">{svg}</div>\n\n'
            f'{RLM}{ltr(f"0 + 27 + 0 + 42 + 24 + 0 + 24 + 3 + 10 + 2 = {total} = {total // 11} · 11")}.')


def scheme_table():
    rows = ["| השיטה | טעות בספרה אחת שחומקת | החלפת שכנות שחומקת |", "|---|---|---|"]
    for key, name in SCHEMES:
        s, w = single_misses(key), swap_misses(key)
        s_txt = "אף אחת" if not s else f"{RLM}{len(s)} מתוך 90 (הפרש 5)"
        if not w:
            w_txt = "אף אחת"
        elif key == "luhn":
            w_txt = f"{RLM}1 מתוך 45{NB}: {ltr('09 ↔ 90')}"
        else:
            w_txt = f"{RLM}{len(w)} מתוך 45 (הפרש 5)"
        rows.append(f"| {name} | {s_txt} | {w_txt} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [card_strip(), doubling_table(), isbn_strip(), scheme_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
