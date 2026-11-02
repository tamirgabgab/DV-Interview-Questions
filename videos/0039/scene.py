"""The tutorial video of question 0039, eggs and floors (script: script.md).

Render with `python videos/render.py 0039` (see VIDEOS.md). Part א draws the 100-floor
building in Manim: one egg goes floor by floor, two eggs jump in decreasing steps (14, 27,
39, ...), then the question turned around (how many floors t drops settle), the recurrence
as two bands around a drop, the table f(k, t) to 129, the three-egg plan (37, 66, 88, 100),
and the page's example run against threshold 36 (nine drops), then the page's box on the
same run, why 8 drops are not enough, the cost and the binary-search trap. Part ב: the
closed form by Pascal's rule, the decision tree that proves no plan does better, then
egg_table, min_drops and egg_run typed in a scrolling window and egg_run traced on the
page's example (3 eggs, 100 floors, threshold 36) drop by drop, the middle drops in one
jump, with the variables under the code (the box is too narrow beside 70-character lines),
then the box's check against every threshold, the cost and the trap of 100 thresholds.

Every number the captions quote is computed here (the reference below) and checked against
the page's own code.
"""

import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "videos" / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, T, VarPanel,  # noqa: E402
                 cost_chips, page_python, trace)

QID = 39
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – שלוש ביצים ומאה קומות"),
    ("ChapterB", "סעיף ב – k ביצים ו-n קומות : הנוסחה והקוד"),
    ("Closing", "סיכום"),
]

# The page's box (3 eggs, 100 floors, threshold 36): the player and the building only (the
# zoom, the legend and the text lines hidden), 400 CSS px wide; a picture after every drop
# up to the eighth, the ninth with the answer as its own picture ("done"), and the chart of
# the drops for every threshold.
BOXES = {
    "plan": {"box": 0, "width": 400, "region": [".ex-play-row", ".eg-box"],
             "hide": [".eg-sum", ".eg-rec-text", ".eg-zoomwrap", ".viz-legend", ".eg-step"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 8}]},
    "done": {"box": 0, "width": 400, "region": [".ex-play-row", ".eg-box"],
             "hide": [".eg-sum", ".eg-rec-text", ".eg-zoomwrap", ".viz-legend", ".eg-step"],
             "steps": [[["click", ".ex-end"]]]},
    "chart": {"box": 0, "region": [".ex-title:not(.eg-zoomtitle)", ".eg-chart"], "steps": [[]]},
}


# --- the reference ------------------------------------------------------------------------

def f(k: int, t: int) -> int:
    """How many floors k eggs settle in t drops: the recurrence, uncapped."""
    if k == 0 or t == 0:
        return 0
    return f(k - 1, t - 1) + 1 + f(k, t - 1)


def least_t(k: int, n: int) -> int:
    return next(t for t in range(n + 1) if f(k, t) >= n)


def run(k: int, n: int, thr: int) -> list[tuple[int, bool]]:
    """The plan of the page against threshold thr, from the uncapped recurrence."""
    t, low, high, eggs, out = least_t(k, n), 0, n + 1, k, []
    while high - low > 1:
        fl = min(low + f(eggs - 1, t - 1) + 1, high - 1)
        out.append((fl, fl > thr))
        t -= 1
        if fl > thr:
            high, eggs = fl, eggs - 1
        else:
            low = fl
    return out


N = 100
TABLE = {(k, t): f(k, t) for k in (1, 2, 3) for t in range(1, 10)}
assert [TABLE[3, t] for t in range(1, 10)] == [1, 3, 7, 14, 25, 41, 63, 92, 129]
assert [TABLE[2, t] for t in range(1, 10)] == [1, 3, 6, 10, 15, 21, 28, 36, 45]
assert least_t(3, N) == 9 and least_t(2, N) == 14 and least_t(1, N) == 100
assert all(f(k, t) == sum(comb(t, i) for i in range(1, k + 1)) for k in range(1, 6) for t in range(12))
TWO = [fl for fl, _ in run(2, N, N)]
assert TWO == [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100]
THREE = [fl for fl, _ in run(3, N, N)]
assert THREE == [37, 66, 88, 100]
RUN36 = run(3, N, 36)
assert RUN36 == [(37, True), (8, False), (15, False), (21, False), (26, False), (30, False),
                 (33, False), (35, False), (36, False)]
WORST = [len(run(3, N, thr)) for thr in range(N + 1)]
assert max(WORST) == 9 and WORST.count(9) == 46
assert len(run(2, N, 26)) == 14                     # breaks at 27, then 15..26
assert f(2, 9) == 45 < 49 and least_t(2, 49) == 10  # binary search from 50: 1 + 10
assert f(2, 3) == 6 and sum(comb(3, i) for i in range(3)) == 7
assert f(3, 8) + 1 == 93 < 101
assert least_t(3, 1000) == 19 and least_t(3, 10000) == 40
CODE = page_python(QID, "def egg_table")
_ns = {}
exec(CODE, _ns)
assert _ns["egg_run"](3, N, 36) == RUN36 and _ns["min_drops"](3, N) == 9
assert all(_ns["egg_run"](3, N, thr) == run(3, N, thr) for thr in range(N + 1))


# --- the building ---------------------------------------------------------------------------

class Building(VGroup):
    """A building of n floors as a tall column: floor x is the slab between heights x - 1
    and x; a tick and a number every 20 floors on the left."""

    def __init__(self, n: int = N, x: float = -4.6, y0: float = -2.2, height: float = 5.55,
                 width: float = 1.5):
        super().__init__()
        self.n, self.x, self.y0, self.h, self.w = n, x, y0, height, width
        self.body = Rectangle(width=width, height=height, stroke_color=C.MUTED, stroke_width=2.5,
                              fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to([x, y0 + height / 2, 0])
        self.lines = VGroup(*[Line([x - width / 2, self.y(v), 0], [x + width / 2, self.y(v), 0],
                                   stroke_color=C.FAINT, stroke_width=1.5) for v in range(10, n, 10)])
        self.labels = VGroup(*[M(str(v), 28, C.MUTED).move_to([x - width / 2 - 0.45, self.y(v), 0])
                               for v in range(0, n + 1, 20)])
        self.add(self.body, self.lines, self.labels)

    def y(self, v: float) -> float:
        return self.y0 + v / self.n * self.h

    def slab(self, a: int, b: int, color: str, opacity: float = 0.55) -> Rectangle:
        """The floors a..b (inclusive) filled."""
        r = Rectangle(width=self.w - 0.06, height=max(self.y(b) - self.y(a - 1), 0.02), stroke_width=0,
                      fill_color=color, fill_opacity=opacity)
        return r.move_to([self.x, (self.y(b) + self.y(a - 1)) / 2, 0])

    def tick(self, v: int, color: str = C.AMBER, label: bool = True, side: float = 1.0,
             size: float = 28) -> VGroup:
        """A drop from floor v: a line across the building at the floor's middle, its number
        beside it."""
        yy = self.y(v - 0.5)
        line = Line([self.x - self.w / 2 - 0.08, yy, 0], [self.x + self.w / 2 + 0.08, yy, 0],
                    stroke_color=color, stroke_width=5)
        g = VGroup(line)
        if label:
            g.add(M(str(v), size, color).next_to(line, RIGHT if side > 0 else LEFT, buff=0.15))
        return g


class EggScene(DVQScene):
    """Helpers shared by the chapters of 0039."""

    def log_rows(self, rows: list[tuple[str, str, str]], where, size: float = 30) -> VGroup:
        """A drop log: (number, floor, result) a row, monospace, aligned in columns."""
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            col = C.RED if c == "broke" else C.GREEN
            r = VGroup(M(a, size, C.MUTED), M(b, size), M(c, size, col))
            r[0].move_to([0, -i * 0.5, 0], aligned_edge=LEFT)
            r[1].move_to([0.8, -i * 0.5, 0], aligned_edge=LEFT)
            r[2].move_to([1.9, -i * 0.5, 0], aligned_edge=LEFT)
            g.add(r)
        return g.move_to(where, aligned_edge=UL)


def table_mob(rows: int = 9, size: float = 30) -> tuple[VGroup, dict]:
    """The table f(k, t), t = 1..rows, k = 1..3: the header and a dict (k, t) -> cell."""
    xs = {0: 0.0, 1: 1.3, 2: 2.6, 3: 3.9}
    head = VGroup(M("t", size, C.MUTED).move_to([xs[0], 0, 0]),
                  *[M(f"k={k}", size, C.MUTED).move_to([xs[k], 0, 0]) for k in (1, 2, 3)])
    cells, tlabels = {}, VGroup()
    for t in range(1, rows + 1):
        y = -0.5 * t
        tlabels.add(M(str(t), size, C.MUTED).move_to([xs[0], y, 0]))
        for k in (1, 2, 3):
            cells[k, t] = M(str(TABLE[k, t]), size).move_to([xs[k], y, 0])
    rule = Line([-0.4, -0.25, 0], [4.4, -0.25, 0], stroke_color=C.FAINT, stroke_width=2)
    return VGroup(head, rule, tlabels, *cells.values()), cells, head, tlabels, rule


# --- the scenes ---------------------------------------------------------------------------

class Opening(EggScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "ביצים וקומות",
                     ["א · שלוש ביצים, 100 קומות", "ב · k ביצים ו-n קומות"],
                     ["שאלה 0039 : ביצים וקומות,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : שלוש ביצים ומאה קומות,\nואז k ביצים ו-n קומות, עם קוד."])
        self.fade_all()
        b = Building(x=0.0)
        thr = b.slab(1, 36, C.GREEN, 0.45)
        above = b.slab(37, 100, C.RED, 0.35)
        mark = VGroup(Line([-0.95, b.y(36), 0], [0.95, b.y(36), 0], stroke_color=C.AMBER, stroke_width=5),
                      M("T", 34, C.AMBER).move_to([1.3, b.y(36), 0]))
        self.say("בניין של 100 קומות, ושלוש ביצים זהות.\nבבניין יש קומת סף.", FadeIn(b), run_time=1.2)
        self.say("ביצה שמטילים מעל הסף נשברת,\nומהסף ומתחתיו היא לא נשברת.",
                 FadeIn(above), FadeIn(thr), Create(mark), run_time=1.2)
        self.say("הסף יכול להיות כל מספר מ-0 עד 100.\nצריך למצוא אותו במקרה הגרוע.")
        self.fade_all()


class ChapterA(EggScene):
    def construct(self):
        self.chapter_card("סעיף א", "שלוש ביצים ומאה קומות",
                          "סעיף א : כמה הטלות צריך במקרה הגרוע,\nומאילו קומות מטילים?")

        # One egg: floor by floor.
        b = Building()
        self.play(FadeIn(b), run_time=0.8)
        count = VGroup(M("drops:", 34, C.MUTED), M("0", 40, C.AMBER)).arrange(RIGHT, buff=0.3)
        count.move_to([1.5, 2.6, 0])
        ticks = VGroup()
        with self.beat("עם ביצה אחת אין ברירה :\nמטילים מקומה 1, ‏2, ‏3, וכן הלאה."):
            self.play(FadeIn(count), run_time=0.4)
            for v in range(1, 9):
                tk = b.tick(v, label=False)
                ticks.add(tk)
                self.play(FadeIn(tk), Transform(count[1], M(str(v), 40, C.AMBER).move_to(count[1], LEFT)),
                          run_time=0.25)
        worst1 = M("worst case: 100 drops", 36, C.AMBER).next_to(count, DOWN, buff=0.5, aligned_edge=LEFT)
        self.say("אם היא נשברת באמצע, אין ביצה נוספת.\nלכן במקרה הגרוע : ‏100 הטלות.", FadeIn(worst1))
        self.play(FadeOut(ticks), FadeOut(count), FadeOut(worst1), run_time=0.5)

        # Two eggs: decreasing steps.
        marks = VGroup()
        with self.beat("עם שתי ביצים, הראשונה קופצת,\nוהשנייה עוברת קומה אחר קומה מתחתיה."):
            for v in TWO[:3]:
                tk = b.tick(v)
                marks.add(tk)
                self.play(FadeIn(tk), run_time=0.4)
        gaps = M("14 + 13 + 12 + ... + 1 = 105", 34).move_to([1.6, 2.6, 0])
        with self.beat("הקפיצות קטנות באחת : ‏14, ‏27, ‏39.\nכל קפיצה עולה הטלה לביצה הראשונה."):
            for v in TWO[3:]:
                tk = b.tick(v, label=v in (50, 69, 84, 95, 100))
                marks.add(tk)
                self.play(FadeIn(tk), run_time=0.22)
            self.play(FadeIn(gaps), run_time=0.6)
        ex = VGroup(b.slab(15, 26, C.BLUE, 0.6))
        sum2 = M("2 + 12 = 14", 34, C.AMBER).next_to(gaps, DOWN, buff=0.5, aligned_edge=LEFT)
        self.say("אם הראשונה נשברת ב-27, השנייה בודקת\nאת 15 עד 26 : ‏2 + 12 = 14 הטלות.", FadeIn(ex), FadeIn(sum2))
        self.say("בכל מקום שהראשונה נשברת יוצא 14.\nזה המקרה הגרוע עם שתי ביצים.")
        self.play(FadeOut(marks), FadeOut(gaps), FadeOut(ex), FadeOut(sum2), run_time=0.5)

        # The question turned around: how many floors t drops settle.
        q = TX(r"f(k,\,t)", size=48, color=C.AMBER).move_to([1.6, 2.5, 0])
        self.say("הרעיון : להפוך את השאלה. כמה קומות\nאפשר לסדר עם k ביצים ו-t הטלות?", FadeIn(q))
        x = 37
        drop = b.tick(x)
        below = b.slab(1, x - 1, C.GREEN, 0.5)
        above = b.slab(x + 1, 100, C.BLUE, 0.45)
        lb = TX(r"f(k-1,\,t-1)", size=36, color=C.GREEN).move_to([-1.6, b.y(18), 0])
        la = TX(r"f(k,\,t-1)", size=36, color=C.BLUE).move_to([-1.6, b.y(70), 0])
        self.say("מטילים מקומה אחת. אם נשברה, הסף מתחת,\nונשארו ביצה אחת פחות והטלה אחת פחות.",
                 FadeIn(drop), FadeIn(below), FadeIn(lb))
        self.say("אם לא נשברה, הסף מעל : אותן ביצים,\nוהטלה אחת פחות.", FadeIn(above), FadeIn(la))
        rec = TX(r"f(k,t) = f(k-1,\,t-1) + 1 + f(k,\,t-1)", size=40).move_to([1.4, -2.05, 0])
        self.say("ועוד הקומה עצמה. זו נוסחת הנסיגה,\nעם אפס כשאין ביצים או אין הטלות.", FadeIn(rec))
        self.fade_all()

        # The table.
        tab, cells, head, tlabels, rule = table_mob()
        tab.scale(1.2).move_to([-0.6, 0.6, 0])
        with self.beat("ממלאים טבלה : ביצה אחת מסדרת t קומות,\nושתיים t(t + 1)/2."):
            self.play(FadeIn(head), Create(rule), FadeIn(tlabels), run_time=0.8)
            self.play(*[FadeIn(cells[k, t]) for k in (1, 2) for t in range(1, 10)], lag_ratio=0.03, run_time=1.4)
        with self.beat("עמודת שלוש הביצים : כל תא הוא\nהתא שמשמאל למעלה, ועוד 1, ועוד התא שמעליו."):
            for t in range(1, 10):
                self.play(FadeIn(cells[3, t]), run_time=0.25)
        rings = VGroup(*[SurroundingRectangle(cells[k, t], color=c, buff=0.1, stroke_width=4)
                         for (k, t), c in (((2, 8), C.GREEN), ((3, 8), C.BLUE), ((3, 9), C.AMBER))])
        eq = TX(r"36 + 1 + 92 = 129", size=40, color=C.AMBER).next_to(tab, RIGHT, buff=0.7).shift(DOWN * 1.6)
        self.say("למשל ‏129 = 36 + 1 + 92.\nעם 8 הטלות רק 92 קומות, פחות מ-100.", Create(rings), FadeIn(eq))
        self.say("ועם 9 הטלות כבר 129 קומות.\nלכן התשובה היא 9 הטלות.")
        self.fade_all()

        # The three-egg plan on the building.
        b = Building()
        self.play(FadeIn(b), run_time=0.6)
        t1 = b.tick(37)
        band = b.slab(1, 36, C.GREEN, 0.5)
        note = TX(r"f(2,\,8) + 1 = 37", size=40, color=C.AMBER).move_to([1.6, 2.4, 0])
        self.say("ההטלה הראשונה : אם נשברה, נשארו שתי ביצים\nו-8 הטלות, ל-36 קומות. לכן מקומה 37.",
                 FadeIn(band), FadeIn(t1), FadeIn(note))
        rest = VGroup(b.tick(66), b.tick(88), b.tick(100))
        jumps = VGroup(TX(r"37 + f(2,\,7) + 1 = 66", size=36), TX(r"66 + f(2,\,6) + 1 = 88", size=36),
                       TX(r"88 + f(2,\,5) + 1 > 100", size=36)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        jumps.next_to(note, DOWN, buff=0.5, aligned_edge=LEFT)
        self.say("אם לא נשברה, הקפיצה הבאה קטנה :\nלקומה 66, אחר כך 88, ואז 100.",
                 FadeOut(band), FadeIn(rest, lag_ratio=0.3), FadeIn(jumps, lag_ratio=0.3), run_time=1.6)
        self.fade_all()

        # The run against threshold 36.
        b = Building()
        thr = VGroup(Line([b.x - 0.95, b.y(36), 0], [b.x + 0.95, b.y(36), 0], stroke_color=C.WHITE,
                          stroke_width=3), M("T = 36", 34).move_to([1.2, 3.35, 0]))
        self.play(FadeIn(b), run_time=0.6)
        self.say("נריץ את התוכנית על הדוגמה שבעמוד,\nכשהסף הוא קומה 36.", Create(thr))
        rows = [(str(i + 1), str(fl), "broke" if br else "safe") for i, (fl, br) in enumerate(RUN36)]
        log = self.log_rows(rows, [0.2, 2.75, 0])
        known = b.slab(37, 100, C.RED, 0.35)
        with self.beat("‏37 גבוהה מהסף : הביצה נשברת.\nנשארו שתי ביצים ושמונה הטלות ל-1 עד 36."):
            self.play(FadeIn(b.tick(37, C.RED, side=1)), FadeIn(log[0]), FadeIn(known), run_time=0.8)
        ticks = VGroup()
        with self.beat("השנייה בקפיצות יורדות : ‏8, ‏15, ‏21, ‏26,\n‏30, ‏33, ‏35. אף אחת לא נשברת."):
            for i in range(1, 8):
                fl = RUN36[i][0]
                tk = b.tick(fl, C.GREEN, label=fl in (8, 15, 21, 26))
                ticks.add(tk)
                self.play(FadeIn(tk), FadeIn(log[i]), run_time=0.35)
        safe = b.slab(1, 36, C.GREEN, 0.35)
        self.say("ההטלה התשיעית, מקומה 36, לא נשברת.\n‏36 בטוחה ו-37 שוברת : הסף 36.",
                 FadeIn(b.tick(36, C.GREEN, label=False)), FadeIn(log[8]), FadeIn(safe))
        self.fade_all()

        # The page's box on the same run, with the drops logged beside it.
        view = BoxView(QID, "plan", height=6.0).move_to([2.8, 0.62, 0])
        head = M("k = 3   n = 100   T = 36", 32, C.AMBER).move_to([-3.6, 3.2, 0])
        rows = [(str(i + 1), str(fl), "broke" if br else "safe") for i, (fl, br) in enumerate(RUN36)]
        log = self.log_rows(rows, [-5.6, 2.5, 0], size=30)
        self.say("התיבה שבעמוד מריצה את אותה דוגמה,\nהטלה אחרי הטלה.", FadeIn(view), FadeIn(head))
        with self.beat("הטלה 1 מקומה 37 : נשברה.\nהחלק שמעל 36 ידוע כשובר."):
            self.box_step(view, 1)
            self.play(FadeIn(log[0]), run_time=0.4)
        with self.beat("הטלה 2 מקומה 8 : לא נשברה.\nהטווח הלא ידוע הוא 9 עד 36."):
            self.box_step(view, 2)
            self.play(FadeIn(log[1]), run_time=0.4)
        with self.beat("וכך 15, ‏21 ו-26 : הטווח הלא ידוע\nקטן בכל הטלה, מלמטה."):
            for k in range(3, 6):
                self.box_step(view, k, run_time=0.35)
                self.play(FadeIn(log[k - 1]), run_time=0.3)
        with self.beat("ואחריהן 30, ‏33 ו-35.\nאף אחת לא נשברת."):
            for k in range(6, 9):
                self.box_step(view, k, run_time=0.35)
                self.play(FadeIn(log[k - 1]), run_time=0.3)
        done = BoxView(QID, "done", height=6.0).move_to(view)
        self.say("ובהטלה התשיעית, מקומה 36 : הסף הוא 36.\nתשע הטלות, כמו בחישוב.",
                 FadeOut(view), FadeIn(done), FadeIn(log[8]), run_time=0.8)
        self.fade_all()

        # Why 8 drops are not enough.
        a = TX(r"f(3,\,8) + 1 = 93", size=48).move_to(UP * 1.2)
        bnd = TX(r"93 < 101", size=48, color=C.AMBER).next_to(a, DOWN, buff=0.6)
        self.say("ולמה לא 8? שמונה הטלות ושלוש ביצים\nמבדילות בין 93 ספים לכל היותר.", FadeIn(a))
        self.say("ויש 101 ספים אפשריים, מ-0 עד 100.\nההוכחה המלאה בסעיף ב.", FadeIn(bnd))
        self.fade_all()

        chips = cost_chips(("drops", r"$\approx\sqrt[3]{6n}$"), notes=("f(3, t) is about t^3/6",))
        self.say("מספר ההטלות גדל כמו שורש שלישי של 6n :\n‏19 ל-1,000 קומות, ו-40 ל-10,000.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: binary search.
        b = Building()
        t50 = b.tick(50, C.RED)
        self.play(FadeIn(b), run_time=0.5)
        l1 = TX(r"f(2,\,9) = 45 < 49", size=42).move_to([1.6, 1.2, 0])
        l2 = TX(r"1 + 10 = 11", size=42, color=C.RED).next_to(l1, DOWN, buff=0.5, aligned_edge=LEFT)
        self.say("מלכודת : חיפוש בינארי. מקומה 50,\nוהביצה נשברת.", FadeIn(t50), FadeIn(b.slab(1, 49, C.BLUE, 0.4)))
        self.say("נשארו שתי ביצים ל-49 קומות, שדורשות\n‏10 הטלות. בסך הכול 11, ולא 9.", FadeIn(l1), FadeIn(l2))
        self.fade_all()


class ChapterB(EggScene):
    def construct(self):
        self.chapter_card("סעיף ב", "‏k ביצים ו-n קומות",
                          "סעיף ב : כל מספר ביצים וכל מספר קומות.\nנוסחה, הוכחה וקוד.")

        # The closed form.
        rec = TX(r"f(k,t) = f(k-1,\,t-1) + 1 + f(k,\,t-1)", size=40).move_to(UP * 2.2)
        closed = TX(r"f(k,t) = \sum_{i=1}^{k} \binom{t}{i}", size=48, color=C.AMBER).move_to(UP * 0.5)
        self.say("לנוסחת הנסיגה יש פתרון סגור :\nסכום של מקדמים בינומיים.", FadeIn(rec), FadeIn(closed))
        check = TX(r"f(3,9) = 9 + 36 + 84 = 129", size=42).move_to(DOWN * 1.2)
        self.say("ההוכחה באינדוקציה, עם הזהות של פסקל.\nלשלוש ביצים ו-9 הטלות : ‏129.", FadeIn(check))
        self.fade_all()

        # The decision tree: no plan does better.
        levels = 3
        nodes, edges, leaves = VGroup(), VGroup(), []
        pos = {}
        for d in range(levels + 1):
            for i in range(2 ** d):
                x = (i + 0.5) * 12.0 / 2 ** d - 6.0
                y = 3.2 - d * 1.25
                pos[d, i] = np.array([x, y, 0])
        for d in range(levels):
            for i in range(2 ** d):
                for c in (0, 1):
                    j = 2 * i + c
                    e = Line(pos[d, i], pos[d + 1, j], stroke_color=C.RED if c == 0 else C.GREEN, stroke_width=3)
                    edges.add(e)
        for d in range(levels + 1):
            for i in range(2 ** d):
                nodes.add(Dot(pos[d, i], radius=0.11, color=C.WHITE))
        for i in range(8):
            word = format(i, "03b")
            leaves.append(M(word, 30, C.MUTED if word == "000" else C.WHITE).next_to(pos[3, i], DOWN, buff=0.2))
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.6, stroke_color=C.RED, stroke_width=4), M("0 broke", 28)).arrange(RIGHT),
                     VGroup(Line(ORIGIN, RIGHT * 0.6, stroke_color=C.GREEN, stroke_width=4), M("1 safe", 28)).arrange(RIGHT)
                     ).arrange(RIGHT, buff=0.8).move_to([-3.9, 3.3, 0])
        self.say("כל תוכנית היא עץ החלטות : בכל צומת\nהטלה, שמאלה נשברה וימינה לא נשברה.",
                 Create(edges), FadeIn(nodes), FadeIn(key), run_time=1.6)
        cross = Cross(leaves[0], stroke_color=C.RED, stroke_width=4)
        self.say("בכל מסלול לכל היותר k שבירות.\nעם שתי ביצים ושלוש הטלות, 000 אסור.",
                 FadeIn(VGroup(*leaves)), Create(cross))
        cnt = TX(r"\binom{3}{0}+\binom{3}{1}+\binom{3}{2} = 7 = f(2,3)+1", size=38).move_to(DOWN * 1.95)
        self.say("לכן לכל היותר 7 עלים, ו-7 ספים :\nבדיוק 6 קומות, ‏f(2, 3).", FadeIn(cnt))
        self.fade_all()
        gen = TX(r"\sum_{i=0}^{k}\binom{t}{i} = f(k,t)+1 \;\ge\; n+1", size=46).move_to(UP * 1.0)
        ex = TX(r"k=3,\ t=8:\quad 93 < 101", size=42, color=C.AMBER).move_to(DOWN * 0.7)
        self.say("בכלל : עלה לכל סף, ולכן צריך\n‏f(k, t) ≥ n. התנאי שהקוד מחפש.", FadeIn(gen))
        self.say("עם שלוש ביצים ו-8 הטלות : ‏93 עלים,\nויש 101 ספים. לכן 8 לא מספיקות.", FadeIn(ex))
        self.fade_all()

        # The code: typed in a scrolling window.
        only = [1, 3, 4, 5, 6, 7, 10, 11, 12, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        panel = CodePanel(CODE, font_size=30, only=only, rows=11)

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            if n == "drops":
                return " ".join(f"{fl}{'✗' if br else ''}" for fl, br in v) if v else "[]"
            return str(v)

        vp = VarPanel(["t", "low", "high", "eggs", "floor", "broke", "drops"], fmt=fmt, size=28,
                      cols=3, slot=3.3).set_state({})
        self.place_code(panel, vp, max_width=13.6, vp_width=9.9)
        self.type_code(panel, [
            (1, "‏egg_table בונה את הטבלה F : כמה קומות\nמסדרות e ביצים ב-t הטלות."),
            (3, "בהתחלה הכול אפס : בלי ביצים\nאו בלי הטלות לא מסדרים אף קומה."),
            ([4, 5, 6], "לכל e ולכל t, נוסחת הנסיגה מסעיף א,\nעם תקרה n : מעל n הערך לא משנה."),
            (7, "ומחזירה את הטבלה."),
            ([10, 11, 12], "‏min_drops : ה-t הראשון\nשבו הטבלה מכסה את כל n הקומות."),
            (15, "‏egg_run מריצה את התוכנית מול סף נתון,\nומחזירה את ההטלות."),
            ([17, 18], "‏low : הקומה הבטוחה הידועה. ‏high :\nהקומה השוברת הידועה. ועוד eggs ו-t."),
            (19, "כל עוד יש קומה לא ידועה\nבין low ל-high, מטילים."),
            (20, "הקומה הבאה : מעל low בדיוק מה\nשהביצים שיישארו מסדרות, ועוד אחת."),
            ([21, 22], "מעל הסף הביצה נשברת.\nרושמים את ההטלה ואת התוצאה."),
            (23, "בכל מקרה נשארת הטלה אחת פחות."),
            ([24, 25, 26, 27], "נשברה : high יורד לקומה, וביצה פחות.\nלא נשברה : low עולה לקומה."),
            (28, "כש-high = low + 1 אין קומה לא ידועה,\nומחזירים את ההטלות."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        # The run on the page's example: drop by drop, the middle ones in one jump.
        steps, result = trace(CODE, "egg_run", (3, N, 36))
        assert result == RUN36, result
        lines = [s.line for s in steps]
        it = [i for i, ln in enumerate(lines) if ln == 19]          # the loop's tests
        assert len(it) == 10 and lines[:2] == [17, 18] and lines[-1] == 28, lines
        plan = [
            (list(range(0, 2)), "full", "נריץ על הדוגמה שבעמוד : שלוש ביצים,\n‏100 קומות, והסף 36."),
            (list(range(it[0], it[1])), "full", "ההטלה הראשונה מקומה 37, מעל הסף :\nנשברה. ‏high = 37, ונשארו שתי ביצים."),
            (list(range(it[1], it[2])), "full", "השנייה : ‏0 + F[1][7] + 1 = 8.\nלא נשברה, ולכן low = 8."),
            (list(range(it[2], it[8])), "jump", "וכך שש הטלות שלא נשברות :\n‏15, ‏21, ‏26, ‏30, ‏33 ו-35."),
            (list(range(it[8], it[9])), "full", "התשיעית מקומה 36 : לא נשברה.\n‏low = 36, ו-high = 37."),
            (list(range(it[9], len(lines))), "full", "אין יותר קומה לא ידועה : הסף 36,\nאחרי תשע הטלות, כמו בסעיף א."),
        ]
        assert sorted(i for p in plan for i in p[0]) == list(range(len(lines)))
        self.play(FadeIn(vp), run_time=0.5)
        cursor = None
        for idx, mode, caption in plan:
            with self.beat(caption):
                todo = idx if mode == "full" else idx[-1:]
                for i in todo:
                    n = lines[i]
                    if not panel.visible(n):
                        row = panel.index[n]
                        first = row if row < panel.scroll else row - panel.rows + 1
                        anims = panel.scroll_to(max(0, min(first, len(panel.lines_text) - panel.rows)))
                        if cursor is not None:
                            anims.append(FadeOut(cursor))
                            cursor = None
                        self.play(*anims, run_time=0.6)
                    bar = panel.bar(n)
                    per = min(0.5, 2.6 / len(todo))
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar),
                              *vp.show(steps[i].state), run_time=per)
                    cursor = cursor or bar
        self.fade_all()

        # The box's check against every threshold.
        view = BoxView(QID, "chart", width=12.0).move_to(UP * 0.7)
        self.say("התיבה מריצה את התוכנית מול כל סף,\nמ-0 עד 100, וסופרת את ההטלות.", FadeIn(view))
        self.say("אף סף לא עובר 9, ו-46 ספים\nמגיעים בדיוק ל-9 : זה המקרה הגרוע.")
        self.fade_all()

        chips = cost_chips(("table", "$O(kn)$"), ("check", "$O(nt)$"),
                           notes=("k rows, up to n drops", "n + 1 runs of t drops"))
        self.say("הסיבוכיות : הטבלה O(kn), ריצה אחת O(t),\nוהבדיקה מול כל הספים O(nt).",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: 100 thresholds instead of 101.
        a = TX(r"0,\,1,\,2,\,\dots,\,100 \;\Rightarrow\; n+1 = 101", size=44).move_to(UP * 1.0)
        bnd = TX(r"f(k,t) \ge n", size=46, color=C.AMBER).next_to(a, DOWN, buff=0.6)
        self.say("מלכודת : לספור 100 ספים. הסף יכול\nלהיות גם 0 וגם 100 : יש n + 1 ספים.", FadeIn(a))
        self.say("מי שסופר n מקבל חסם תחתון\nשטועה באחת.", FadeIn(bnd))
        self.fade_all()


class Closing(EggScene):
    def construct(self):
        self.closing(QID, [("א", M("3 eggs, 100 floors: 9 drops (37, 66, 88, 100)", 30)),
                           ("ב", M("f(k, t) = sum C(t, i) >= n;  egg_run", 30))],
                     ["לסיכום : במקום כמה הטלות, כמה קומות\nמסדרות t הטלות.",
                      "נסו מספרים משלכם בתיבה\nשבעמוד של שאלה 0039 באתר."],
                     holds=(None, 4.0))
