"""The tutorial video of question 0043, horse races without a stopwatch (script: script.md).

Render with `python videos/render.py 0043` (see VIDEOS.md). Part א draws the 36 horses as a
grid in Manim, a row per group and a column per place in the group, on the page's example
(seed 3, the same hidden speeds as the page's first box): the group races put each row in
order, the winners' race sorts the rows, every horse shows how many horses are known to be
faster, the staircase of nine candidates, races 8 and 9; then the page's box plays the same
races, and the proof that 8 races are not enough. Part ב: 30 horses for the top 3 (seed 11,
the page's second box), the free lane in the winners' race, the general count, then
horses_plan typed in a scrolling window and traced race by race with the variables under
it (the box is too narrow beside 81-character lines), then the box.

The page's code is shown whole, but three long lines are wrapped in the picture: line 1
and line 35 break inside their brackets (still valid Python), and line 23, which has no
bracket to break in, wraps with a ↪ mark, as an editor's soft wrap. The code that runs is
the page's, unchanged.
"""

import sys
from math import ceil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "videos" / "lib"))
sys.path.insert(0, str(ROOT / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, T, VarPanel, chip,  # noqa: E402
                 cost_chips, he, page_python, trace)
import q0043  # noqa: E402  (the page's figures: an independent reference of the plan)

QID = 43
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – 36 סוסים, 6 במסלול, ארבעת הראשונים"),
    ("ChapterB", "סעיף ב – 30 סוסים, שלושת הראשונים, והתוכנית הכללית"),
    ("Closing", "סיכום"),
]

# The page's two boxes, a picture after every race: box 0 is part א's (36 / 6 / 4, seed 3,
# fixed), box 1 part ב's (30 / 6 / 3, seed 11). The summary line above the grid is hidden.
BOXES = {
    "fixed": {"box": 0, "region": [".ex-play-row", ".hr-gridbox", ".hr-step"], "hide": [".hr-sum"],
              "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 9}]},
    "thirty": {"box": 1, "region": [".ex-play-row", ".hr-gridbox", ".hr-step"], "hide": [".hr-sum"],
               "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 7}]},
}


# --- the examples, from the reference model of tools/figures/q0043.py ----------------------

def example(a: int, b: int, c: int, seed: int) -> dict:
    speed = q0043.speeds(a, seed)
    ranking, log = q0043.plan(a, b, c, speed)
    return dict(a=a, b=b, c=c, speed=speed, ranking=ranking, log=log,
                names=q0043.names(a, b, log))


EX_A = example(36, 6, 4, q0043.SEED_A)
EX_B = example(30, 6, 3, q0043.SEED_B)


def nm(ex: dict, xs) -> str:
    return " > ".join(ex["names"][x] for x in xs)


def known_faster(ex: dict, k: int) -> list[set]:
    """Every horse's set of horses known to be faster after the first k races."""
    a = ex["a"]
    faster = [set() for _ in range(a)]
    slower = [set() for _ in range(a)]
    for entry in ex["log"][:k]:
        order = entry["order"]
        for i, x in enumerate(order):
            for y in order[i + 1:]:
                if y in slower[x]:
                    continue
                for u in faster[x] | {x}:
                    for v in slower[y] | {y}:
                        slower[u].add(v)
                        faster[v].add(u)
    return faster


def state_after(ex: dict, k: int) -> tuple[set, dict]:
    """The horses out and the settled ranks after the first k races."""
    out, placed = set(), {}
    faster = known_faster(ex, k)
    for entry in ex["log"][:k]:
        out |= set(entry["gone"])
    for entry in ex["log"][:k]:
        for x in entry["placed"]:
            placed[x] = len(faster[x]) + 1
    return out, placed


# The numbers the captions quote, checked against the reference (and the page's box).
assert [len(e["order"]) for e in EX_A["log"]] == [6] * 7 + [6, 2]
assert nm(EX_A, EX_A["log"][6]["order"]) == "C1 > F1 > B1 > E1 > D1 > A1"
assert nm(EX_A, EX_A["log"][7]["order"]) == "F1 > F2 > B1 > E1 > C2 > C3"
assert nm(EX_A, EX_A["log"][8]["order"]) == "B1 > F3"
assert [EX_A["names"][x] for x in EX_A["ranking"]] == ["C1", "F1", "F2", "B1"]
assert len(EX_A["log"][6]["gone"]) == 14 and len(EX_A["log"][6]["open"]) == 9
assert len(EX_A["log"][7]["open"]) == 2
assert len(EX_B["log"]) == 7
assert nm(EX_B, EX_B["log"][5]["order"]) == "A1 > D1 > C1 > B1 > E1"
assert nm(EX_B, EX_B["log"][6]["horses"]) == "D1 > A2 > C1 > D2 > A3"
assert nm(EX_B, EX_B["log"][6]["order"]) == "D1 > C1 > A2 > A3 > D2"
assert [EX_B["names"][x] for x in EX_B["ranking"]] == ["A1", "D1", "C1"]
assert 36 * 35 * 34 * 33 == 1413720 and 720 ** 2 < 1413720 < 720 ** 3


# --- the grid of horses -----------------------------------------------------------------

CELL_W, CELL_H, GAP = 0.92, 0.6, 0.1


class Grid(VGroup):
    """The horses as a grid: a row per group, a column per place in the group's race.
    Before its race a group's horses are blank, in stable order; the race moves each to
    its place and names it. Rows move when the winners' race sorts the groups."""

    def __init__(self, ex: dict, centre=ORIGIN):
        super().__init__()
        self.ex = ex
        a, b = ex["a"], ex["b"]
        self.rows_n = ceil(a / b)
        self.centre = np.array(centre, dtype=float)
        self.row_at = list(range(self.rows_n))      # group g sits at screen row row_at[g]
        self.col_of = {x: x % b for x in range(a)}   # before its race: stable order
        self.cells = {}
        for x in range(a):
            rect = RoundedRectangle(width=CELL_W, height=CELL_H, corner_radius=0.1,
                                    stroke_color=C.MUTED, stroke_width=2,
                                    fill_color=C.NAVY_LIGHT, fill_opacity=1)
            dot = Dot(radius=0.07, color=C.MUTED)
            cell = VGroup(rect, dot)
            cell.move_to(self.pos(x))
            self.cells[x] = cell
            self.add(cell)
        self.heads = VGroup(*[M(str(i + 1), 28, C.MUTED) for i in range(b)])
        for i, h in enumerate(self.heads):
            h.move_to(self.point(0, i) + UP * (CELL_H / 2 + 0.32))
        self.letters = VGroup(*[M("ABCDEF"[g], 28, C.MUTED) for g in range(self.rows_n)])
        for g, t in enumerate(self.letters):
            t.move_to(self.point(g, 0) + LEFT * (CELL_W / 2 + 0.35))
        self.add(self.heads, self.letters)

    def point(self, row: int, col: int) -> np.ndarray:
        b = self.ex["b"]
        x = (col - (b - 1) / 2) * (CELL_W + GAP)
        y = ((self.rows_n - 1) / 2 - row) * (CELL_H + GAP)
        return self.centre + np.array([x, y, 0.0])

    def pos(self, x: int) -> np.ndarray:
        return self.point(self.row_at[x // self.ex["b"]], self.col_of[x])

    def label(self, x: int, text: str | None = None, color=None) -> Text:
        return M(text or self.ex["names"][x], 28, color or C.WHITE).move_to(self.cells[x][0])

    def race_group(self, scene, g: int, run_time: float = 0.9):
        """A group race: its horses move to their places and get their names."""
        b = self.ex["b"]
        order = self.ex["log"][g]["order"]
        anims = []
        for i, x in enumerate(order):
            self.col_of[x] = i
            target = self.pos(x)
            new = VGroup(self.cells[x][0].copy().move_to(target), self.label(x).move_to(target))
            anims.append(Transform(self.cells[x], new))
        scene.play(*anims, run_time=run_time)
        del b

    def sort_rows(self, scene, winners: list[int], run_time: float = 1.4):
        """The winners' race: the groups move to the rows of their winners' places."""
        b = self.ex["b"]
        for j, w in enumerate(winners):
            self.row_at[w // b] = j
        anims = [self.cells[x].animate.move_to(self.pos(x)) for x in self.cells]
        anims += [t.animate.move_to(self.point(self.row_at[g], 0) + LEFT * (CELL_W / 2 + 0.35))
                  for g, t in enumerate(self.letters)]
        scene.play(*anims, run_time=run_time)

    def style(self, x: int, kind: str) -> list:
        """Animations to a cell's look: plain, cand(idate), out, placed."""
        rect, lab = self.cells[x][0], self.cells[x][1]
        if kind == "out":
            return [rect.animate.set_fill(C.NAVY, opacity=1).set_stroke(C.FAINT, width=2),
                    lab.animate.set_color(C.FAINT)]
        if kind == "cand":
            return [rect.animate.set_fill(C.NAVY_LIGHT, opacity=1).set_stroke(C.BLUE, width=4),
                    lab.animate.set_color(C.WHITE)]
        if kind == "placed":
            return [rect.animate.set_fill(C.GREEN, opacity=0.55).set_stroke(C.GREEN, width=4),
                    lab.animate.set_color(C.WHITE)]
        return [rect.animate.set_fill(C.NAVY_LIGHT, opacity=1).set_stroke(C.MUTED, width=2),
                lab.animate.set_color(C.WHITE)]

    def rings(self, xs, color=C.AMBER) -> VGroup:
        return VGroup(*[SurroundingRectangle(self.cells[x][0], color=color, buff=0.05,
                                             corner_radius=0.12, stroke_width=5) for x in xs])

    def show_counts(self, scene, faster: list[set], xs) -> list:
        """Each horse's label becomes its number of known-faster horses."""
        olds = []
        anims = []
        for x in xs:
            lab = self.cells[x][1]
            olds.append(lab.copy())
            n = len(faster[x])
            anims.append(Transform(lab, M(str(n), 30, C.AMBER if n < self.ex["c"] else C.MUTED)
                                   .move_to(lab)))
        scene.play(*anims, run_time=0.8)
        return olds

    def show_names(self, scene, xs, colors: dict) -> None:
        scene.play(*[Transform(self.cells[x][1], self.label(x, color=colors.get(x, C.WHITE)))
                     for x in xs], run_time=0.8)


def legend() -> Group:
    rows = []
    for color, fill, opacity, text in ((C.GREEN, C.GREEN, 0.55, "נקבע"), (C.BLUE, C.NAVY_LIGHT, 1, "מועמד"),
                                       (C.FAINT, C.NAVY, 1, "נפסל")):
        sw = RoundedRectangle(width=0.5, height=0.36, corner_radius=0.08, stroke_color=color,
                              stroke_width=4, fill_color=fill, fill_opacity=opacity)
        rows.append(Group(he(text, 30, C.WHITE), sw).arrange(RIGHT, buff=0.25))
    g = Group(*rows).arrange(DOWN, buff=0.3, aligned_edge=RIGHT)
    return g


class HorseScene(DVQScene):
    """Helpers shared by the chapters of 0043."""

    def race_line(self, text: str, where=UP * 3.25, color=None) -> Text:
        return M(text, 32, color or C.AMBER).move_to(where)

    def set_line(self, old, text: str, color=None):
        new = self.race_line(text, color=color)
        if old is None:
            self.play(FadeIn(new), run_time=0.4)
            return new
        self.play(Transform(old, new), run_time=0.4)
        return old


# --- the wrapped code panel (three long lines broken in the picture only) -------------------

WRAP = {1: ("def horses_plan(a: int, b: int, c: int,", 16, ""),
        23: ("        return len(faster[x]) + 1 if len(faster[x]) + len(slower[x]) == a - 1", 12, "↪ "),
        35: ("            best = max(pool, key=lambda x: (sum(1 for y in chosen", 20, "")}


class WrapPanel(CodePanel):
    """The page's code with its docstring out of the picture and the lines of WRAP broken in
    two rows: page line n keeps its row, the rest goes to a row named n + 0.5 (typed and lit
    with it)."""

    def __init__(self, code: str, **kw):
        page = code.rstrip("\n").split("\n")
        disp, where = [], []
        for n, line in enumerate(page, 1):
            if n in (2, 3):                       # the docstring
                continue
            if n in WRAP:
                head, indent, mark = WRAP[n]
                if not line.startswith(head):
                    raise RuntimeError(f"line {n} changed on the page: {line!r}")
                disp += [head, " " * indent + mark + line[len(head):].lstrip()]
                where += [n, n + 0.5]
            else:
                disp.append(line)
                where.append(n)
        super().__init__("\n".join(disp) + "\n", **kw)
        self.index = {where[d - 1]: r for d, r in self.index.items()}
        for n, (_, _, mark) in WRAP.items():
            if mark:                              # the soft-wrap mark, muted
                self.code.code_lines[self.index[n + 0.5]][0].set_color(C.MUTED)

    def bar(self, page_line):
        if page_line in WRAP:                     # a wrapped line: the cursor covers both rows
            a, b = super().bar(page_line), super().bar(page_line + 0.5)
            top, bottom = a.get_top()[1], b.get_bottom()[1]
            for part in a:
                part.stretch_to_fit_height(top - bottom).move_to(
                    [part.get_center()[0], (top + bottom) / 2, 0])
            return a
        return super().bar(page_line)


# --- the scenes -------------------------------------------------------------------------


class Opening(HorseScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "מרוצי סוסים בלי שעון",
                     ["א · 36 סוסים, ארבעה ראשונים", "ב · 30 סוסים, והתוכנית הכללית"],
                     ["שאלה 0043 : מרוצי סוסים בלי שעון,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : 36 סוסים וארבעת הראשונים,\nואז 30 סוסים ותוכנית לכל מקרה."])
        self.fade_all()


class ChapterA(HorseScene):
    def construct(self):
        ex = EX_A
        log = ex["log"]
        self.chapter_card("סעיף א", "36 סוסים, ארבעת הראשונים",
                          "סעיף א : 36 סוסים, שישה בכל תחרות,\nואנחנו רוצים את ארבעת המהירים, לפי הסדר.")

        # The problem: 36 blank horses, a race gives only an order.
        grid = Grid(ex, centre=LEFT * 1.3 + DOWN * 0.35)
        self.say("באורווה 36 סוסים, לכל אחד מהירות קבועה.\nבכל תחרות רצים שישה.",
                 FadeIn(VGroup(*grid.cells.values()), lag_ratio=0.02), run_time=1.6)
        self.say("אין שעון : בסוף התחרות רואים\nרק את סדר ההגעה, בלי זמנים.")
        line = None
        with self.beat("השאלה : כמה תחרויות צריך לכל הפחות,\nכדי לדעת בוודאות את ארבעת הראשונים?"):
            line = self.set_line(line, "36 horses · 6 a race · top 4 in order", C.WHITE)

        # The idea: count the horses known to be faster.
        self.say("הרעיון : לכל סוס נספור כמה סוסים\nידוע בוודאות שהם מהירים ממנו.")
        self.say("גם בעקיפין : אם x ניצח את y, ו-y ניצח את z,\nאז x מהיר מ-z, גם אם לא רצו יחד.")
        self.say("סוס שידועים לו ארבעה מהירים או יותר\nלא יכול להיות בארבעת הראשונים. הוא נפסל.")

        # Races 1 to 6: the groups.
        key = legend().move_to(RIGHT * 4.9 + DOWN * 0.35)
        self.play(FadeIn(grid.heads), FadeIn(grid.letters), FadeIn(key), run_time=0.6)
        with self.beat("תחרויות 1 עד 6 : כל סוס חייב לרוץ,\nאז מריצים שש קבוצות של שישה."):
            line = self.set_line(line, "race 1:  " + nm(ex, log[0]["order"]))
            grid.race_group(self, 0)
        with self.beat("כל שורה היא קבוצה, וכל עמודה מקום בה.\n‏A1 ניצח בקבוצה A, ‏A2 הגיע שני."):
            self.play(Indicate(grid.cells[log[0]["order"][0]], color=C.AMBER), run_time=0.8)
        with self.beat("כך גם חמש הקבוצות האחרות."):
            line = self.set_line(line, "races 2-6:  every group in order")
            for g in range(1, 6):
                grid.race_group(self, g, run_time=0.5)
        out6, _ = state_after(ex, 6)
        self.say("בכל קבוצה המקומות 5 ו-6 נפסלים מיד :\nלכל אחד ארבעה מהירים ידועים בקבוצה שלו.",
                 *[a for x in sorted(out6) for a in grid.style(x, "out")], run_time=1.0)

        # Race 7: the winners.
        winners = log[6]["order"]
        rings = grid.rings(winners)
        with self.beat("תחרות 7 : ששת המנצחים של הקבוצות.\nמי שמנצח כאן הוא הסוס המהיר ביותר."):
            line = self.set_line(line, "race 7:  " + nm(ex, winners))
            self.play(Create(rings), run_time=0.8)
        with self.beat("‏C1 ניצח, והוא מקום 1. מסדרים את השורות\nלפי תחרות המנצחים : הקבוצה של C1 למעלה."):
            self.play(FadeOut(rings), run_time=0.4)
            grid.sort_rows(self, winners)
            self.play(*grid.style(winners[0], "placed"), run_time=0.6)

        # The counts after race 7.
        faster7 = known_faster(ex, 7)
        alive = [x for x in range(ex["a"]) if x not in out6]
        olds = None
        with self.beat("עכשיו נספור לכל סוס את המהירים הידועים\nשלו. המספר מופיע במקום השם."):
            olds = grid.show_counts(self, faster7, range(ex["a"]))
        self.say("סוס במקום i בשורה j : ‏i − 1 מהירים בקבוצה,\nועוד j − 1 מנצחים שמהירים מהמנצח שלו.")
        out7, placed7 = state_after(ex, 7)
        gone7 = sorted(out7 - out6)
        self.say("כל מי שהמספר שלו 4 או יותר נפסל :\nעוד 14 סוסים יוצאים בתחרות הזו.",
                 *[a for x in gone7 for a in grid.style(x, "out")], run_time=1.0)
        cands = log[6]["open"]
        with self.beat("נשארו בדיוק תשעה מועמדים, במדרגות :\nמספרים 1, 2 ו-3."):
            grid.show_names(self, range(ex["a"]), {x: C.FAINT for x in out7})
            self.play(*[a for x in cands for a in grid.style(x, "cand")], run_time=0.8)
        del olds, alive

        # The staircase.
        by_count = {k: [x for x in cands if len(faster7[x]) == k] for k in (1, 2, 3)}
        r1 = grid.rings(by_count[1])
        self.say("למקום 2 יש רק שני מועמדים, C2 ו-F1 :\nלכל אחד מהם מהיר ידוע אחד, C1.", Create(r1))
        r2 = grid.rings(by_count[2])
        self.say("למקום 3 מצטרפים C3, F2 ו-B1,\nעם שני מהירים ידועים.", Create(r2))
        r3 = grid.rings(by_count[3])
        self.say("ולמקום 4 עוד ארבעה : C4, F3, B2 ו-E1,\nעם שלושה מהירים ידועים.", Create(r3))
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(r3), run_time=0.5)
        assert [ex["names"][x] for x in by_count[1]] == ["C2", "F1"] or \
            sorted(ex["names"][x] for x in by_count[1]) == ["C2", "F1"]

        # Race 8.
        race8 = log[7]["horses"]
        rings = grid.rings(race8)
        self.say("תחרות 8 : כל חמשת המועמדים למקומות 2 ו-3,\nועוד E1, מועמד למקום 4.", Create(rings))
        with self.beat("‏F1 > F2 > B1 > E1 > C2 > C3.\nכולם רצו יחד, אז הסדר ביניהם ידוע."):
            line = self.set_line(line, "race 8:  " + nm(ex, log[7]["order"]))
        out8, placed8 = state_after(ex, 8)
        new_placed = [x for x in placed8 if x not in placed7]
        self.say("לכן F1 הוא מקום 2, ו-F2 מקום 3 :\nאין אף מועמד אחר למקומות האלה.",
                 FadeOut(rings), *[a for x in new_placed for a in grid.style(x, "placed")], run_time=1.0)
        gone8 = sorted(out8 - out7)
        self.say("ועכשיו ל-C2, ‏C3, ‏C4, ‏B2 ו-E1 יש ארבעה\nמהירים ידועים, והם נפסלים.",
                 *[a for x in gone8 for a in grid.style(x, "out")], run_time=1.0)
        last = log[7]["open"]
        ring9 = grid.rings(last)
        self.say("נשארו שני מועמדים למקום 4 :\n‏B1, השלישי בתחרות 8, ו-F3.",
                 Create(ring9), run_time=0.8)

        # Race 9.
        with self.beat("תחרות 9 : ‏B1 נגד F3. ‏B1 מנצח, והוא מקום 4.\nסיימנו אחרי 9 תחרויות."):
            line = self.set_line(line, "race 9:  " + nm(ex, log[8]["order"]))
            out9, placed9 = state_after(ex, 9)
            anims = [a for x in placed9 if x not in placed8 for a in grid.style(x, "placed")]
            anims += [a for x in out9 - out8 for a in grid.style(x, "out")]
            self.play(*anims, FadeOut(ring9), run_time=0.8)
        top4 = self.race_line("top 4:  " + "  ".join(f"{i + 1}. {ex['names'][x]}"
                                                   for i, x in enumerate(ex["ranking"])), color=C.GREEN)
        self.say("ארבעת הראשונים, לפי הסדר :\n‏C1, ‏F1, ‏F2 ו-B1.", Transform(line, top4))
        self.fade_all()

        # The page's box on the same example.
        view = BoxView(QID, "fixed", height=6.0).move_to(UP * 0.62)
        self.say("התיבה שבעמוד מריצה את אותה דוגמה,\nעם מהירויות נסתרות, תחרות אחרי תחרות.", FadeIn(view))
        self.box_beat(view, [
            (6, "אחרי שש תחרויות הקבוצות :\nבכל שורה, המקומות 5 ו-6 כבר בחוץ."),
            (7, "תחרות 7, המנצחים : השורות מסודרות,\nובכל תא המספר הוא המהירים הידועים."),
            (8, "תחרות 8 : ‏F1 מקום 2 ו-F2 מקום 3,\nונשארו שני מועמדים."),
            (9, "ותחרות 9 קובעת את מקום 4, ‏B1.\nבעמוד אפשר גם להגריל מהירויות אחרות."),
        ])
        self.fade_all()

        # Why 8 races are not enough.
        chips = VGroup(*[RoundedRectangle(width=0.62, height=0.62, corner_radius=0.1,
                                          stroke_color=C.MUTED, stroke_width=2,
                                          fill_color=C.NAVY_LIGHT, fill_opacity=1) for _ in range(9)])
        chips.arrange(RIGHT, buff=0.18).move_to(UP * 1.9)
        nums = VGroup(*[M(str(i + 1), 28).move_to(chips[i]) for i in range(9)])
        self.say("למה אי אפשר בפחות מ-9?\nנעבור על זה שלב אחרי שלב.", FadeIn(chips), FadeIn(nums))
        self.say("כל סוס חייב לרוץ לפחות פעם אחת :\nאחרת הוא אולי המהיר ביותר. שש תחרויות.",
                 *[chips[i].animate.set_stroke(C.BLUE, width=4) for i in range(6)])
        self.say("כדי לדעת מי מקום 1, המנצחים חייבים\nלהיפגש : תחרות 7.",
                 chips[6].animate.set_stroke(C.GREEN, width=4))
        dots = VGroup(*[Dot(radius=0.2, color=C.BLUE) for _ in range(9)]).arrange(RIGHT, buff=0.42)
        dots.move_to(DOWN * 0.4)
        nine = TX(r"9 \text{ candidates},\ \le 3 \text{ known faster each}", size=34, color=C.MUTED)
        nine.next_to(dots, DOWN, buff=0.4)
        self.say("אחרי שבע תחרויות, בכל תוכנית, נשארים\nלפחות תשעה מועמדים למקומות 2 עד 4.",
                 FadeIn(dots, lag_ratio=0.1), FadeIn(nine))
        lane = SurroundingRectangle(VGroup(*dots[:6]), color=C.AMBER, buff=0.18, corner_radius=0.15,
                                    stroke_width=4)
        self.say("תחרות אחת מריצה רק שישה מהם,\nושלושה נשארים בחוץ.", Create(lane),
                 chips[7].animate.set_stroke(C.AMBER, width=4))
        q = M("?", 40, C.RED).next_to(dots[8], UP, buff=0.2)
        self.say("היריב בוחר את התוצאה כך שאחד מאלה\nשבחוץ עדיין יכול להיות מקום 4.", FadeIn(q),
                 dots[8].animate.set_color(C.RED))
        self.say("לכן אחרי 8 תחרויות מקום 4 לא ידוע,\nוצריך תחרות תשיעית.",
                 chips[8].animate.set_stroke(C.RED, width=4))
        self.fade_all()

        # The cost.
        info = TX(r"36\cdot 35\cdot 34\cdot 33 \approx 1.4\cdot 10^{6}", size=40).move_to(UP * 1.1)
        per = TX(r"6! = 720 \text{ results a race}", size=40, color=C.MUTED).next_to(info, DOWN, buff=0.45)
        self.say("במונחי מידע : יש כ-1.4 מיליון תשובות\nאפשריות, ותחרות נותנת רק 720 תוצאות.",
                 FadeIn(info), FadeIn(per))
        low = TX(r"\Rightarrow\ \ge 3 \text{ races, even with a stopwatch}", size=40, color=C.AMBER)
        low.next_to(per, DOWN, buff=0.45)
        self.say("זה חסם של שלוש תחרויות בלבד, גם עם שעון.\nבלי שעון, המבנה מעלה אותו ל-9.", FadeIn(low))
        self.fade_all()
        chips_cost = cost_chips(("races", "9"), notes=("6 groups, the winners, 2 more",))
        self.say("התשובה : 9 תחרויות, ואין פחות.", FadeIn(chips_cost, lag_ratio=0.3))
        self.fade_all()

        # The trap: the winner of the second group is not place 2.
        c2 = VGroup(RoundedRectangle(width=1.4, height=0.9, corner_radius=0.12, stroke_color=C.BLUE,
                                     stroke_width=4, fill_color=C.NAVY_LIGHT, fill_opacity=1),
                    M("C2", 40))
        f1 = c2.copy()
        f1[1].become(M("F1", 40).move_to(f1[0]))
        pair = VGroup(c2, M("?", 48, C.RED), f1).arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        self.say("מלכודת : לחשוב שהמנצח של הקבוצה השנייה,\nכאן F1, הוא בטוח מקום 2.", FadeIn(pair))
        self.say("אבל C2, השני בקבוצה של המנצח, מעולם\nלא רץ נגדו, ואולי הוא מהיר ממנו.",
                 Indicate(pair[1], color=C.RED))
        self.say("תחרות המנצחים מדרגת קבוצות, לא סוסים.\nלכן יש שני מועמדים למקום 2.")
        self.fade_all()


class ChapterB(HorseScene):
    def construct(self):
        ex = EX_B
        log = ex["log"]
        self.chapter_card("סעיף ב", "30 סוסים, והתוכנית הכללית",
                          "סעיף ב : 30 סוסים, שישה במסלול,\nושלושת הראשונים. ואז תוכנית לכל מקרה.")

        grid = Grid(ex, centre=LEFT * 1.3 + DOWN * 0.35)
        line = None
        with self.beat("חמש תחרויות של קבוצות,\nכדי שכל סוס ירוץ פעם אחת."):
            self.play(FadeIn(grid), FadeIn(legend().move_to(RIGHT * 4.9 + DOWN * 0.35)), run_time=0.8)
            line = self.set_line(line, "races 1-5:  the groups")
            for g in range(5):
                grid.race_group(self, g, run_time=0.45)
        out5, _ = state_after(ex, 5)
        self.say("עם שלושה ראשונים, נפסל מי שיש לו\nשלושה מהירים ידועים : המקומות 4 עד 6.",
                 *[a for x in sorted(out5) for a in grid.style(x, "out")], run_time=1.0)

        winners = log[5]["order"]
        rings = grid.rings(winners)
        with self.beat("תחרות 6 : חמשת המנצחים.\nבמסלול יש שישה מקומות, ואחד נשאר פנוי."):
            line = self.set_line(line, "race 6:  " + nm(ex, winners))
            self.play(Create(rings), run_time=0.8)
        self.say("מפתה להוסיף את השני של הקבוצה הטובה,\nאבל איזו קבוצה טובה עוד לא יודעים.")
        self.say("כל סוס שנוסיף, היריב יקבע שהקבוצה שלו\nלא תהיה הטובה. המקום הפנוי לא עוזר.")
        with self.beat("‏A1 ניצח, והוא מקום 1.\nמסדרים את השורות לפי התחרות."):
            self.play(FadeOut(rings), run_time=0.4)
            grid.sort_rows(self, winners)
            self.play(*grid.style(winners[0], "placed"), run_time=0.6)
        out6, placed6 = state_after(ex, 6)
        cands = log[5]["open"]
        self.say("אותן מדרגות, עם i − 1 + j − 1 ≤ 2 :\nחמישה מועמדים, A2, ‏D1, ‏A3, ‏D2 ו-C1.",
                 *[a for x in sorted(out6 - out5) for a in grid.style(x, "out")],
                 *[a for x in cands for a in grid.style(x, "cand")], run_time=1.0)
        rings = grid.rings(log[6]["horses"])
        with self.beat("חמישה נכנסים לתחרות אחת. תחרות 7 :\n‏D1 > C1 > A2 > A3 > D2."):
            self.play(Create(rings), run_time=0.6)
            line = self.set_line(line, "race 7:  " + nm(ex, log[6]["order"]))
        out7, placed7 = state_after(ex, 7)
        self.say("‏D1 מקום 2, ו-C1 מקום 3.\nשבע תחרויות, ולא שש.", FadeOut(rings),
                 *[a for x in placed7 if x not in placed6 for a in grid.style(x, "placed")],
                 *[a for x in out7 - out6 for a in grid.style(x, "out")], run_time=1.0)
        self.fade_all()

        # The general count.
        f1 = VGroup(TX(r"\left\lceil a/b \right\rceil", size=46), TX(r"+\ 1", size=46),
                    TX(r"+\ 1", size=46)).arrange(RIGHT, buff=1.2).move_to(UP * 1.5)
        notes = VGroup(T("groups", 30, C.MUTED), T("winners", 30, C.MUTED), T("staircase", 30, C.MUTED))
        for part, n in zip(f1, notes):
            n.next_to(part, DOWN, buff=0.3)
        self.say("בכלל : ‏a חלקי b תחרויות של קבוצות,\nועוד אחת של המנצחים.", FadeIn(f1[:2]), FadeIn(notes[:2]))
        cond = TX(r"\frac{c(c+1)}{2} - 1 \le b", size=46, color=C.AMBER).move_to(DOWN * 0.9)
        self.say("אחריהן יש c(c + 1)/2 − 1 מועמדים.\nאם הם נכנסים בתחרות אחת, עוד אחת מספיקה.",
                 FadeIn(f1[2]), FadeIn(notes[2]), FadeIn(cond))
        ex36 = TX(r"c = 4:\ 9 > 6 \ \Rightarrow\ \text{two more races}", size=38, color=C.MUTED)
        ex36.next_to(cond, DOWN, buff=0.45)
        self.say("עם ארבעה ראשונים יש תשעה מועמדים,\nיותר משישה, ולכן בסעיף א שתיים.", FadeIn(ex36))
        self.fade_all()

        # The code: typed in a scrolling window.
        code = page_python(QID, "def horses_plan")
        panel = WrapPanel(code, font_size=30, drop_comments=True, drop_trailing_comments=True, rows=11)
        names = ex["names"]

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            if n == "log":
                if not v:
                    return "[]"
                return f"{len(v)} race{'s' if len(v) > 1 else ''}, last: " + " > ".join(names[x] for x in v[-1])
            return "[" + ", ".join(names[x] for x in v) + "]"

        vp = VarPanel(["log", "pool", "chosen"], fmt=fmt, size=28).set_state({})
        self.place_code(panel, vp, max_width=13.6, vp_width=9.5)
        self.type_code(panel, [
            ([1, 1.5], "‏horses_plan מקבלת a סוסים, b במסלול\nו-c ראשונים, ו-race שמחזירה סדר הגעה."),
            ([4, 5, 6], "לכל סוס שתי קבוצות : מי ידוע מהיר ממנו,\nומי ידוע איטי ממנו. ‏log שומר את התחרויות."),
            ([8, 9, 10], "‏beats רושמת ש-x ניצח את y.\nאם זה כבר ידוע, אין מה לעשות."),
            ([11, 12, 13], "הסגירות : כל מי שמעל x, כולל x,\nמנצח את כל מי שמתחת ל-y, כולל y."),
            ([15, 16, 17, 18, 19, 20], "‏run מריצה תחרות, שומרת את הסדר,\nורושמת כל זוג : מי שהגיע קודם ניצח."),
            ([22, 23, 23.5], ["‏rank : הדירוג ידוע כשכל סוס אחר\nידוע כמהיר ממנו או כאיטי ממנו.",
                              "השורה הארוכה שבורה כאן לשתיים,\nרק בתמונה. בעמוד היא שורה אחת."]),
            ([25, 26, 27], "קודם הקבוצות : קבוצות של b,\nוכל קבוצה רצה."),
            ([28, 29], "אם יש יותר מקבוצה אחת,\nתחרות של כל המנצחים."),
            (30, "ממשיכים כל עוד אחד המקומות\nמ-1 עד c עוד לא נקבע."),
            ([31, 32], "‏pool : המועמדים הפתוחים, פחות מ-c מהירים\nידועים. קודם מי שיש לו הכי מעט."),
            ([33, 34, 35, 35.5, 36, 37, 38], "בוחרים עד b סוסים בחמדנות : בכל פעם מי\nשמוסיף הכי הרבה זוגות שעוד לא הושוו."),
            (39, "ומריצים אותם. כל תחרות כזו\nמוסיפה השוואות שחסרו."),
            (40, "בסוף מחזירים את c הראשונים לפי הדירוג,\nואת כל התחרויות."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        # The run on the page's example: race by race.
        speed = ex["speed"]
        steps, result = trace(code, "horses_plan", (30, 6, 3, lambda g: sorted(g, key=lambda x: speed[x])))
        ranking, page_log = result
        assert ranking == ex["ranking"] and page_log == [e["order"] for e in log], result
        lines = [s.line for s in steps]

        def segments(ends):
            """Cut the trace after the run of each line in `ends`, in order."""
            out, k = [], 0
            for m in ends:
                j = k
                while not (lines[j] == m and (j + 1 == len(lines) or lines[j + 1] != m)):
                    j += 1
                out.append(list(range(k, j + 1)))
                k = j + 1
            if k != len(lines):
                raise RuntimeError(f"the trace goes on after the plan: {lines[k:]}")
            return out

        segs = segments([22, 25, 27, 27, 27, 27, 27, 29, 32, 38, 38, 38, 38, 38, 39, 40])
        plan = [
            ([segs[0]], "full", "נריץ על הדוגמה שבעמוד : 30 סוסים,\nשישה במסלול, שלושה ראשונים."),
            ([segs[1]], "full", "חמש קבוצות של שישה :\nסוסים 0 עד 5, ‏6 עד 11, וכן הלאה."),
            ([segs[2]], "full", "תחרות 1 : קבוצה A. הסדר נשמר ב-log,\nוכל זוג בה נרשם."),
            (segs[3:7], "jump", "וכך כל חמש הקבוצות :\nחמש תחרויות ב-log."),
            ([segs[7]], "full", "יותר מקבוצה אחת, ולכן תחרות 6 :\nהמנצחים, ‏A1 > D1 > C1 > B1 > E1."),
            ([segs[8]], "full", "מקום 2 עוד לא נקבע, ונכנסים ללולאה.\n‏pool : חמשת המועמדים, ממוינים."),
            ([segs[9][:3]], "full", "‏chosen ריק, ומתחילים לבחור.\nבהתחלה אף סוס לא מוסיף זוגות חסרים."),
            ([segs[9][3:]], "full", "לכן קובע השוויון : D1, עם מהיר ידוע אחד\nוהכי הרבה איטיים ידועים."),
            (segs[10:14], "jump", "וכך עוד ארבעה : A2, ‏C1, ‏D2 ו-A3.\nכל אחד מוסיף זוגות שלא הושוו."),
            ([segs[14]], "full", "‏pool ריק, ורצה תחרות 7 :\n‏D1 > C1 > A2 > A3 > D2."),
            ([segs[15]], "full", "מקומות 1 עד 3 נקבעו, והלולאה נגמרת :\n‏A1, ‏D1, ‏C1, אחרי שבע תחרויות."),
        ]
        self.play(FadeIn(vp), run_time=0.5)
        cursor = None
        for parts, mode, caption in plan:
            idx = [i for p in parts for i in p]
            with self.beat(caption):
                if mode == "full":          # each line once, the locals after its last repeat
                    todo = [i for i in idx if i + 1 not in idx or lines[i + 1] != lines[i]]
                else:
                    todo = idx[-1:]
                for i in todo:
                    n = lines[i]
                    if not panel.visible(n) or (n in WRAP and not panel.visible(n + 0.5)):
                        row = panel.index[n]
                        first = row if row < panel.scroll else row - panel.rows + 1 + (1 if n in WRAP else 0)
                        anims = panel.scroll_to(max(0, min(first, len(panel.lines_text) - panel.rows)))
                        if cursor is not None:
                            anims.append(FadeOut(cursor))
                            cursor = None
                        self.play(*anims, run_time=0.6)
                    bar = panel.bar(n)
                    per = min(0.6, 2.4 / len(todo))
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar),
                              *vp.show(steps[i].state), run_time=per)
                    cursor = cursor or bar
        self.fade_all()

        # The box.
        view = BoxView(QID, "thirty", height=6.0, start=5).move_to(UP * 0.62)
        self.say("התיבה שבעמוד מריצה את אותה דוגמה.\nאחרי חמש תחרויות הקבוצות :", FadeIn(view))
        with self.beat("תחרות 6, המנצחים. ‏A1 מקום 1,\nוחמישה מועמדים נשארו."):
            self.box_step(view, 6)
        self.box_beat(view, [
            (7, "ותחרות 7 קובעת את מקומות 2 ו-3.\nבעמוד אפשר לבחור a, ‏b ו-c אחרים."),
        ])
        self.fade_all()

        chips = cost_chips(("time", "$O(a^2)$"), ("memory", "$O(a^2)$"),
                           notes=("per result: the closure", "two sets a horse"))
        self.say("הסיבוכיות : כל תוצאה עולה O(a²) בסגירות,\nוהזיכרון O(a²), שתי קבוצות לכל סוס.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: the classic answer of 7.
        classic = TX(r"25,\ 5,\ 3:\ \ 7 \text{ races}", size=44).move_to(UP * 0.8)
        ours = TX(r"36,\ 6,\ 4:\ \ 9 \text{ races}", size=44, color=C.AMBER).next_to(classic, DOWN, buff=0.5)
        self.say("מלכודת : לזכור שהחידה הקלאסית נגמרת\nב-7, ולענות 7 גם ל-36 סוסים.", FadeIn(classic))
        self.say("שם חמישה מועמדים נכנסים בתחרות אחת.\nעם ארבעה ראשונים יש תשעה, וצריך שתיים.",
                 FadeIn(ours))
        self.fade_all()


class Closing(HorseScene):
    def construct(self):
        self.closing(QID, [("א", M("36 / 6 / top 4:  groups, winners, 2 more = 9", 30)),
                           ("ב", M("30 / 6 / top 3: 7;  any a, b, c: horses_plan", 30))],
                     ["לסיכום : לספור לכל סוס מהירים ידועים,\nולהריץ רק את המועמדים.",
                      "נסו מספרים משלכם בתיבה\nשבעמוד של שאלה 0043 באתר."],
                     holds=(None, 4.0))
