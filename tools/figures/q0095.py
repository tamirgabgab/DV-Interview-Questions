#!/usr/bin/env python3
"""Figures and tables of question 0095 (Conway's soldiers).

    python tools/figures/fill.py 95        # put the blocks on the page

Soldiers stand on the cells of the grid below a line: cell (x, y) with y <= 0. A move is a
jump of peg solitaire: a soldier jumps over a neighbour (up, down, left or right) into the
empty cell behind it, and the soldier jumped over leaves the board. Row n is the row y = n
above the line, and the target of row n is the cell (0, n).

A soldier is a blue dot, the soldier that just landed an orange dot, the two cells a jump
emptied dashed circles, the target a magenta frame. Frames of a play run right to left,
the start on the right, as the page reads.

blocks() returns them in page order: the statement's jump (with the legend); part a's
plays to rows 1 and 2, and the play to row 3 in two rows of frames; part b's three boards
of the 20 soldiers (the start, the army of row 3 one row up, the end) and the table of the
19 moves; part c's weights to the target of row 5 and the table of the half plane's
weight and the fewest soldiers for each row. tests/0095 checks that the page copies match,
replays every play and recomputes every number exactly.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

NB = " "
RLM = "‏"

# --- the reference -------------------------------------------------------------------------

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))

SOLUTIONS = {
    1: ([(0, 0), (0, -1)],
        [((0, -1), (0, 0), (0, 1))]),
    2: ([(-2, 0), (-1, 0), (0, 0), (0, -1)],
        [((0, -1), (0, 0), (0, 1)), ((-2, 0), (-1, 0), (0, 0)), ((0, 0), (0, 1), (0, 2))]),
    3: ([(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, -1), (1, -1), (2, -1)],
        [((2, -1), (2, 0), (2, 1)), ((1, -1), (1, 0), (1, 1)), ((2, 1), (1, 1), (0, 1)),
         ((0, 0), (0, 1), (0, 2)), ((-2, 0), (-1, 0), (0, 0)), ((0, -1), (0, 0), (0, 1)),
         ((0, 1), (0, 2), (0, 3))]),
    4: ([(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
         (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
         (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (0, -3), (2, -3)],
        [((0, -1), (0, 0), (0, 1)), ((0, -3), (0, -2), (0, -1)), ((-2, -2), (-1, -2), (0, -2)),
         ((1, -1), (1, 0), (1, 1)), ((3, -1), (2, -1), (1, -1)), ((2, -3), (2, -2), (2, -1)),
         ((2, -1), (2, 0), (2, 1)), ((4, 0), (3, 0), (2, 0)), ((1, -2), (1, -1), (1, 0)),
         ((0, -2), (0, -1), (0, 0)), ((-2, -1), (-2, 0), (-2, 1)), ((-1, -1), (-1, 0), (-1, 1)),
         ((2, 0), (2, 1), (2, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 2), (1, 2), (0, 2)),
         ((0, 1), (0, 2), (0, 3)), ((-2, 1), (-1, 1), (0, 1)), ((0, 0), (0, 1), (0, 2)),
         ((0, 2), (0, 3), (0, 4))]),
}
PHASE = 12      # the first 12 moves of row 4 build the army of row 3 one row up


def jump(army: frozenset, src, over, dst) -> frozenset:
    step = (over[0] - src[0], over[1] - src[1])
    assert step in DIRS and (dst[0] - over[0], dst[1] - over[1]) == step, (src, over, dst)
    assert src in army and over in army and dst not in army, (src, over, dst)
    return (army - {src, over}) | {dst}


def boards(n: int) -> list[frozenset]:
    army, moves = SOLUTIONS[n]
    out = [frozenset(army)]
    assert all(y <= 0 for _, y in army)
    for mv in moves:
        out.append(jump(out[-1], *mv))
    assert (0, n) in out[-1]
    return out


# Exact weights: p + q·σ with integers p and q, where σ = (√5 − 1)/2 and σ² = 1 − σ.

def zmul(u, v):
    (p, q), (r, s) = u, v
    return p * r + q * s, p * s + q * r - q * s


def zpow(d: int):
    out = (1, 0)
    for _ in range(d):
        out = zmul(out, (0, 1))
    return out


def zadd(u, v):
    return u[0] + v[0], u[1] + v[1]


def zsign(u) -> int:
    """The sign of p + q·σ = (2p − q + q√5)/2, exactly."""
    a, b = 2 * u[0] - u[1], u[1]
    if a >= 0 and b >= 0:
        return int(a > 0 or b > 0)
    if a <= 0 and b <= 0:
        return -1
    return 1 if (a * a > 5 * b * b) == (a > 0) else -1


def zfloat(u) -> float:
    return u[0] + u[1] * (5 ** 0.5 - 1) / 2


def dist(c, n: int) -> int:
    return abs(c[0]) + abs(n - c[1])


def top(n: int, k: int):
    """The k heaviest cells below the line together, for the target of row n."""
    ds = sorted(abs(x) + n - y for x in range(-k, k + 1) for y in range(-k, 1))[:k]
    out = (0, 0)
    for d in ds:
        out = zadd(out, zpow(d))
    return out


def fewest_by_weight(n: int) -> int:
    """The fewest soldiers whose cells can weigh 1 together: the potential's lower bound."""
    k = 1
    while zsign(zadd(top(n, k), (-1, 0))) < 0:
        k += 1
    return k


FEWEST = {1: 2, 2: 4, 3: 8, 4: 20}

# --- drawing --------------------------------------------------------------------------------

S = 18          # the side of a cell
LM = 14         # the row numbers on the left
TOPM = 22       # room above for the enlarge button of the figure


def frame(army, x0: float, y0: float, xr, yr, s: int = S, n: int | None = None, move=None,
          caption: str = "", labels: bool = True) -> str:
    """One board: the cells of xr x yr, the line, the soldiers, the last move marked."""
    out = []
    bx = x0 + (LM if labels else 0)
    xs, ys = range(xr[0], xr[1] + 1), range(yr[1], yr[0] - 1, -1)

    def px(x, y):
        return bx + (x - xr[0]) * s, y0 + (yr[1] - y) * s

    for y in ys:
        for x in xs:
            cx, cy = px(x, y)
            cls = "cy-ground" if y <= 0 else "cy-sky"
            out.append(f'<rect class="{cls}" x="{cx + 0.5:g}" y="{cy + 0.5:g}" width="{s - 1}" height="{s - 1}"/>')
    lx0, ly = px(xr[0], 0)
    out.append(f'<line class="cy-line" x1="{lx0 - 2:g}" y1="{ly:g}" x2="{lx0 + len(xs) * s + 2:g}" y2="{ly:g}"/>')
    if n is not None and yr[0] <= n <= yr[1]:
        tx, ty = px(0, n)
        out.append(f'<rect class="cy-target" x="{tx + 1.5:g}" y="{ty + 1.5:g}" width="{s - 3}" height="{s - 3}" rx="2"/>')
    r = s * 0.32
    if move is not None:
        src, over, dst = move
        for c in (src, over):
            cx, cy = px(*c)
            out.append(f'<circle class="cy-gone" cx="{cx + s / 2:g}" cy="{cy + s / 2:g}" r="{r:g}"/>')
        (ax, ay), (bx2, by2) = px(*src), px(*dst)
        out.append(f'<path class="cy-arrow" d="M{ax + s / 2:g},{ay + s / 2:g} L{bx2 + s / 2:g},{by2 + s / 2:g}"/>')
    for c in sorted(army):
        if xr[0] <= c[0] <= xr[1] and yr[0] <= c[1] <= yr[1]:
            cx, cy = px(*c)
            cls = "cy-new" if move is not None and c == move[2] else "cy-man"
            out.append(f'<circle class="{cls}" cx="{cx + s / 2:g}" cy="{cy + s / 2:g}" r="{r:g}"/>')
    if labels:
        for y in ys:
            if y > 0:
                _, cy = px(xr[0], y)
                out.append(f'<text class="cy-lab" x="{x0 + LM / 2:g}" y="{cy + s / 2 + 4:g}" text-anchor="middle">{y}</text>')
    if caption:
        cx = bx + len(xs) * s / 2
        out.append(f'<text class="cy-cap" x="{cx:g}" y="{y0 + len(ys) * s + 15:g}" text-anchor="middle" direction="rtl">{caption}</text>')
    return "".join(out)


def row_of_frames(items: list[dict], xr, yr, label: str, s: int = S, gap: int = 14) -> str:
    """Frames side by side, the first one on the right."""
    w1 = LM + (xr[1] - xr[0] + 1) * s
    hgt = TOPM + (yr[1] - yr[0] + 1) * s + 22
    width = len(items) * w1 + (len(items) - 1) * gap + 4
    parts = []
    for i, it in enumerate(items):
        x0 = width - 2 - (i + 1) * w1 - i * gap
        parts.append(frame(it["army"], x0, TOPM, xr, yr, s=s, n=it.get("n"), move=it.get("move"),
                           caption=it.get("caption", "")))
    rem = min(width * 1.25, 46 * 16) / 16
    return (f'<svg class="figure cy-fig" viewBox="0 0 {width:g} {hgt:g}" style="max-width:{rem:.1f}rem" role="img" '
            f'aria-label="{label}">' + "".join(parts) + "</svg>")


def legend(*keys: tuple[str, str]) -> str:
    return '<span class="viz-legend">' + "".join(f'<span><i class="{k}"></i>{t}</span>' for k, t in keys) + "</span>"


KEY_MAN = ("cy-key-man", "חייל")
KEY_NEW = ("cy-key-new", "החייל שקפץ")
KEY_GONE = ("cy-key-gone", "המשבצות שהקפיצה פינתה")
KEY_TARGET = ("cy-key-target", "היעד")
KEY_LINE = ("cy-key-line", "הקו")


def coord(c) -> str:
    return f"({c[0]}, {c[1]})"


def play(n: int, lo: int, hi: int) -> list[dict]:
    bs = boards(n)
    _, moves = SOLUTIONS[n]
    items = []
    for k in range(lo, hi + 1):
        cap = f"ההתחלה, {len(bs[0])} חיילים" if k == 0 else f"מהלך {k}"
        items.append({"army": bs[k], "n": n, "move": moves[k - 1] if k else None, "caption": cap})
    return items


def describe(n: int, lo: int, hi: int) -> str:
    bs = boards(n)
    _, moves = SOLUTIONS[n]
    out = []
    for k in range(lo, hi + 1):
        if k == 0:
            out.append(f"ההתחלה{NB}: {len(bs[0])} חיילים, " + ", ".join(coord(c) for c in sorted(bs[0], key=lambda c: (-c[1], c[0]))))
        else:
            a, b, c = moves[k - 1]
            out.append(f"מהלך {k}{NB}: החייל ב-{coord(a)} קופץ מעל {coord(b)} אל {coord(c)}")
    return "; ".join(out)


# --- the statement ---------------------------------------------------------------------------

def statement() -> str:
    xr, yr = (-3, 3), (-3, 3)
    army = frozenset((x, y) for x in range(xr[0], xr[1] + 1) for y in range(yr[0], 1))
    mv = ((1, -1), (1, 0), (1, 1))
    after = jump(army, *mv)
    items = [{"army": army, "caption": "חיילים מתחת לקו"},
             {"army": after, "move": mv, "caption": "קפיצה לשורה 1"}]
    label = ("שני לוחות. בימני חיילים בכל משבצת מתחת לקו, בשורות 0 ומטה, והשורות מעל הקו ממוספרות 1, 2, 3. "
             "בשמאלי קפיצה אחת : החייל במשבצת (1, -1) קופץ מעל השכן שלו ב-(1, 0) אל המשבצת הריקה (1, 1) בשורה 1, "
             "והחייל שבאמצע יוצא מהלוח")
    return row_of_frames(items, xr, yr, label, s=17, gap=20) + "\n\n" + legend(KEY_MAN, KEY_NEW, KEY_GONE, KEY_LINE)


# --- part a: rows 1, 2 and 3 -------------------------------------------------------------------

def rows_1_2() -> str:
    f1 = row_of_frames(play(1, 0, 1), (-1, 1), (-1, 1),
                       "שורה 1 בשני חיילים. " + describe(1, 0, 1), s=20, gap=18)
    f2 = row_of_frames(play(2, 0, 3), (-2, 1), (-1, 2),
                       "שורה 2 בארבעה חיילים. " + describe(2, 0, 3), s=18, gap=12)
    return f1 + "\n\n" + f2 + "\n\n" + legend(KEY_MAN, KEY_NEW, KEY_GONE, KEY_TARGET)


def row_3(lo: int, hi: int) -> str:
    part = "חלק ראשון" if lo == 0 else "חלק שני"
    return row_of_frames(play(3, lo, hi), (-2, 2), (-1, 3),
                         f"שורה 3 בשמונה חיילים, {part}. " + describe(3, lo, hi), s=15, gap=10)


# --- part b: row 4 -------------------------------------------------------------------------------

def row_4() -> str:
    bs = boards(4)
    items = [{"army": bs[0], "n": 4, "caption": "ההתחלה, 20 חיילים"},
             {"army": bs[PHASE], "n": 4, "caption": f"אחרי {PHASE} מהלכים"},
             {"army": bs[-1], "n": 4, "caption": "אחרי 19 מהלכים"}]
    label = ("שורה 4 בעשרים חיילים, שלושה לוחות. בימני ההתחלה : שבעה חיילים בשורה 0 מ-x = -2 עד 4, שישה בשורה -1 "
             "מ-x = -2 עד 3, חמישה בשורה -2 מ-x = -2 עד 2, ושניים בשורה -3 ב-x = 0 וב-x = 2. באמצעי, אחרי 12 מהלכים, "
             "נשארו שמונה : חמישה בשורה 1 מ-x = -2 עד 2 ושלושה בשורה 0 מ-x = 0 עד 2, הצבא של שורה 3 שורה אחת למעלה. "
             "בשמאלי, אחרי 19 מהלכים, חייל אחד ביעד (0, 4)")
    return row_of_frames(items, (-2, 4), (-3, 4), label, s=15, gap=16) + "\n\n" + legend(KEY_MAN, KEY_TARGET)


def moves_table() -> str:
    _, moves = SOLUTIONS[4]
    rows = ["| מהלך | שלב | החייל קופץ מ- | מעל | אל |", "|:-:|:-:|:-:|:-:|:-:|"]
    for k, (a, b, c) in enumerate(moves, 1):
        stage = "בונים את הצבא של שורה 3" if k <= PHASE else "הפתרון של שורה 3, שורה אחת למעלה"
        cells = " | ".join(f"{RLM}\\( {coord(p)} \\)" for p in (a, b, c))
        rows.append(f"| {RLM}{k} | {stage} | {cells} |")
    return "\n".join(rows)


# --- part c: the weights and the table -------------------------------------------------------------

def weights() -> str:
    n, xr, yr, s = 5, (-4, 4), (-3, 5), 24
    w = LM + (xr[1] - xr[0] + 1) * s + 4
    hgt = TOPM + (yr[1] - yr[0] + 1) * s + 8
    out = []
    bx = LM

    def px(x, y):
        return bx + (x - xr[0]) * s, TOPM + (yr[1] - y) * s

    for y in range(yr[1], yr[0] - 1, -1):
        for x in range(xr[0], xr[1] + 1):
            d = dist((x, y), n)
            cx, cy = px(x, y)
            shade = min(max(d - 4, 0), 6) if y <= 0 else 0
            cls = f"cy-w{shade}" if y <= 0 else "cy-sky"
            out.append(f'<rect class="{cls}" x="{cx + 0.5:g}" y="{cy + 0.5:g}" width="{s - 1}" height="{s - 1}"/>')
            tcls = "cy-wnum" if y <= 0 else "cy-wsky"
            out.append(f'<text class="{tcls}" x="{cx + s / 2:g}" y="{cy + s / 2 + 4:g}" text-anchor="middle">{d}</text>')
        if y > 0:
            _, cy = px(xr[0], y)
            out.append(f'<text class="cy-lab" x="{LM / 2:g}" y="{cy + s / 2 + 4:g}" text-anchor="middle">{y}</text>')
    tx, ty = px(0, n)
    out.append(f'<rect class="cy-target" x="{tx + 1.5:g}" y="{ty + 1.5:g}" width="{s - 3}" height="{s - 3}" rx="2"/>')
    lx, ly = px(xr[0], 0)
    out.append(f'<line class="cy-line" x1="{lx - 2:g}" y1="{ly:g}" x2="{lx + (xr[1] - xr[0] + 1) * s + 2:g}" y2="{ly:g}"/>')
    label = ("המרחק של כל משבצת מהיעד (0, 5), צעדים למעלה, למטה ולצדדים. ביעד עצמו 0, ובמשבצת (0, 0), "
             "הקרובה ביותר מתחת לקו, 5. בכל שורה המרחק גדל ב-1 לכל צעד הצידה, ובכל עמודה ב-1 לכל שורה למטה. "
             "המשקל של משבצת במרחק d הוא סיגמא בחזקת d, ומתחת לקו המשבצות כהות יותר ככל שהן קרובות")
    return (f'<svg class="figure cy-fig" viewBox="0 0 {w:g} {hgt:g}" style="max-width:{w * 1.25 / 16:.1f}rem" role="img" '
            f'aria-label="{label}">' + "".join(out) + "</svg>\n\n"
            + legend(("cy-key-w", f"מתחת לקו{NB}: כהה יותר, כבד יותר"), KEY_TARGET, KEY_LINE))


PHI_POW = {1: r"\varphi^{4} \approx 6.854", 2: r"\varphi^{3} \approx 4.236", 3: r"\varphi^{2} \approx 2.618",
           4: r"\varphi \approx 1.618", 5: r"1"}


def table_c() -> str:
    rows = [f"| שורה | המשקל של כל חצי המישור | הפוטנציאל אומר{NB}: לפחות | הכי מעט חיילים |", "|:-:|:-:|:-:|:-:|"]
    for n in range(1, 6):
        if n < 5:
            low, best = str(fewest_by_weight(n)), str(FEWEST[n])
        else:
            low, best = "אי אפשר", "אי אפשר"
        rows.append(f"| {RLM}{n} | {RLM}\\( {PHI_POW[n]} \\) | {RLM}{low} | {RLM}{best} |".replace(f"{RLM}אי", "אי"))
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        statement(),
        rows_1_2(),
        row_3(0, 3),
        row_3(4, 7) + "\n\n" + legend(KEY_MAN, KEY_NEW, KEY_GONE, KEY_TARGET),
        row_4(),
        moves_table(),
        weights(),
        table_c(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
