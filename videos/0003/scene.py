"""The tutorial video of question 0003, what does this code do (script: script.md).

Render with `python videos/render.py 0003` (see VIDEOS.md). The code is the question
itself (the page's `mystery`), so it is shown whole, not typed (the owner, 2026-10-31);
its lines are explained one by one, then it runs on the page's example A = [3, 1, 4, 2]
beside the page's box. The box is shown twice: alone, i = 0 comparison by comparison and
then "until the end of i" for i = 1, 2, 3; and beside the code, where the run stops on
every swap. The page's answer: an ascending sort, always n² comparisons (16 here, 5 swaps).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import C, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips, page_python, trace  # noqa: E402

QID = 3
SCENES = [
    ("Opening", "פתיחה"),
    ("Chapter", "מה הקוד עושה – לולאה כפולה עם swap"),
    ("Closing", "סיכום"),
]

A0 = [3, 1, 4, 2]          # the page's example

# The page's box (data-kind="trace", data-mode="loop"), as the page opens it on [3, 1, 4, 2].
# "endi": picture 0 before the run, 1-4 the four comparisons of i = 0 (a click on "next"
# each), 5-7 the end of i = 1, 2, 3 (a click on "until the end of i" each).
# "all": picture k after k comparisons (k clicks on "next"), for the run beside the code;
# the box's own copy of the code is hidden there, the code panel beside it has the code.
BOXES = {
    "endi": {"box": 0, "region": [".ex-play-row", ".tr-box", ".tr-step"], "hide": [".ex-scrubwrap"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 4},
                       {"do": [["click", ".ex-endi"]], "repeat": 3}]},
    "all": {"box": 0, "region": [".ex-play-row", ".tr-right", ".tr-step", ".tr-sum"],
            "hide": [".ex-scrubwrap", ".tr-left"],
            "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 16}]},
}


def mystery_trace(A, from_next=False):
    """The arrays after each i (and the comparisons and swaps) of the page's code, or of the
    trap's inner loop from j = i + 1."""
    A = list(A)
    n = len(A)
    rows, comps, swaps = [], 0, 0
    for i in range(n):
        for j in range(i + 1 if from_next else 0, n):
            comps += 1
            if A[i] < A[j]:
                A[i], A[j] = A[j], A[i]
                swaps += 1
        rows.append(list(A))
    return rows, comps, swaps


ROWS, COMPS, SWAPS = mystery_trace(A0)
assert (COMPS, SWAPS) == (16, 5) and ROWS[-1] == [1, 2, 3, 4], (COMPS, SWAPS, ROWS)
assert mystery_trace(A0, True)[0][-1] == [4, 3, 2, 1]


class Arr(VGroup):
    """An array as a row of square cells, the index over each cell."""

    def __init__(self, values, side: float = 0.78, done: int = -1, size: float = 34,
                 idx: bool = False):
        super().__init__()
        self.cells = VGroup()
        for x, v in enumerate(values):
            ok = x <= done
            sq = RoundedRectangle(width=side, height=side, corner_radius=0.08,
                                  stroke_color=C.GREEN if ok else C.FAINT, stroke_width=3,
                                  fill_color=C.GREEN if ok else C.NAVY_LIGHT,
                                  fill_opacity=0.22 if ok else 1)
            sq.move_to(RIGHT * x * (side + 0.12))
            sq.add(M(str(v), size).move_to(sq))
            self.cells.add(sq)
        self.add(self.cells)
        if idx:
            self.idx = VGroup(*[M(str(x), 22, C.MUTED).next_to(c, UP, buff=0.1)
                                for x, c in enumerate(self.cells)])
            self.add(self.idx)

    def ring(self, x: int, color: str = C.AMBER) -> SurroundingRectangle:
        return SurroundingRectangle(self.cells[x], color=color, buff=0.06, corner_radius=0.1,
                                    stroke_width=5)


def name_of(n: int, s: dict) -> str:
    if n not in s:
        return ""
    v = s[n]
    return "[" + ", ".join(map(str, v)) + "]" if isinstance(v, list) else str(v)


class Opening(DVQScene):
    def construct(self):
        self.opening(QID, "סטודנט", "מה עושה הקוד?",
                     ["לולאה כפולה עם swap"],
                     ["שאלה 0003 : מה עושה הקוד?\nשאלה ברמת סטודנט.",
                      "סעיף אחד : לקרוא קוד קצר,\nלהריץ אותו על דוגמה, ולהסביר מה הוא עושה."])
        self.fade_all()
        arr = Arr(A0, idx=True)
        q = M("?", 64, C.AMBER)
        row = VGroup(M("mystery(", 40), arr, M(")", 40), M("→", 44, C.MUTED), q).arrange(RIGHT, buff=0.3)
        row.move_to(UP * 0.6)
        self.say("נתונה פונקציה קצרה שמקבלת רשימה\nשל מספרים. מה היא עושה לרשימה?",
                 FadeIn(row, lag_ratio=0.15), run_time=1.6)
        self.fade_all()


class Chapter(DVQScene):
    def construct(self):
        self.chapter_card("השאלה", "לולאה כפולה עם swap",
                          "הנה הקוד של השאלה, ב-Python.\nננסה להבין מה הוא עושה.")

        # The problem: the page's code, shown whole (it is the question, not the answer).
        code = page_python(QID, "def mystery")
        panel = CodePanel(code, font_size=44, drop_trailing_comments=True)
        self.place_code(panel)
        self.say("הפונקציה mystery מקבלת רשימה A\nשל מספרים שלמים, ומשנה אותה במקום.",
                 FadeIn(panel))
        self.walk_code(panel, None, [
            ([2], "קודם n, מספר האיברים ב-A.", None),
            ([3], "הלולאה החיצונית : i עובר\nעל כל האינדקסים, מ-0 עד n − 1.", None),
            ([4], "הלולאה הפנימית : גם j עובר על כולם,\nמ-0, ולא רק על אלה שאחרי i.", None),
            ([5, 6], "אם A[i] קטן מ-A[j],\nמחליפים ביניהם.", None),
        ])
        self.say("במבט ראשון זה נראה כמו מיון יורד :\nאיבר קטן ב-i מתחלף עם איבר גדול ממנו.")
        self.say("אבל לפני שעונים, מריצים דוגמה קטנה.\nהשאלה מבקשת מערך בגודל 4.")
        self.play(FadeOut(panel), run_time=0.6)

        # The steps: the page's box, alone and large.
        view = BoxView(QID, "endi", height=5.8).move_to(UP * 0.62)
        self.say("התיבה שבעמוד מריצה את הקוד\nעל המערך של העמוד : 3, 1, 4, 2.", FadeIn(view))
        self.box_beat(view, [
            (1, "השוואה 1 : i = 0 ו-j = 0.\nהאם 3 < 3? לא, אין החלפה."),
            (2, "השוואה 2 : j = 1.\nהאם 3 < 1? לא."),
            (3, "השוואה 3 : j = 2. האם 3 < 4? כן.\nמחליפים, ו-A הוא 4, 1, 3, 2."),
            (4, "השוואה 4 : האם 4 < 2? לא.\nבסוף i = 0, המקסימום 4 יושב ב-A[0]."),
            (5, "הכפתור \"עד סוף i\" משלים את i = 1 :\nהחלפה אחת, ב-j = 0, של 1 עם 4."),
            (6, "סוף i = 2 : החלפה אחת, ב-j = 1.\nה-3 נכנס לפני ה-4 : 1, 3, 4, 2."),
            (7, "סוף i = 3 : שתי החלפות, ב-j = 1 וב-j = 2.\nהמערך 1, 2, 3, 4."),
        ])
        self.say("התשובה : הקוד ממיין בסדר עולה,\nמהקטן לגדול. לא יורד!")
        self.fade_all()

        # The code beside the box: the run stops on every swap.
        steps, _ = trace(code, "mystery", (list(A0),))
        assert [s.line for s in steps].count(6) == SWAPS
        vp = VarPanel(["i", "j", "n", "A"], fmt=lambda n, s: name_of(n, s), size=30, cols=2,
                      slot=2.4).set_state({})
        vp.next_to(panel, DOWN, buff=0.35).align_to(panel, LEFT)
        view = BoxView(QID, "all")
        with self.beat("נחזור לקוד ונריץ אותו על הדוגמה,\nלצד התיבה, ונעצור על כל החלפה."):
            self.play(FadeIn(panel), run_time=0.6)
            self.split(panel, view, vp)
        self.run_code(panel, vp, steps, [
            ([2], "בהתחלה n = 4,\nו-A הוא 3, 1, 4, 2.", None),
            ([3, 4, 5], "השוואה 1 : i = 0, j = 0.\n‏3 < 3 לא מתקיים.", 1),
            ([4, 5], "השוואה 2 : 3 < 1. לא.", 2),
            ([4, 5, 6], "השוואה 3 : 3 < 4. כן,\nוההחלפה מביאה את 4 ל-A[0].", 3),
            ([4, 5, 4], "השוואה 4 : 4 < 2. לא. הלולאה הפנימית\nנגמרה, והמקסימום ב-A[0].", 4),
            ([3, 4, 5, 6], "ב-i = 1 כבר ההשוואה הראשונה מחליפה :\n‏1 < 4, וה-1 עובר להתחלה.", 5),
            ([4, 5, 4, 5, 4, 5, 4], "עכשיו A[1] הוא 4, המקסימום,\nולכן בשאר ה-j של i = 1 אין החלפות.", 8),
            ([3, 4, 5, 4, 5, 6], "ב-i = 2 : 3 < 1 לא, אבל 3 < 4 כן.\nה-3 נכנס לפני ה-4 : 1, 3, 4, 2.", 10),
            ([4, 5, 4, 5, 4], "ב-j = 2 וב-j = 3, A[2] הוא 4,\nהמקסימום, ואין החלפות.", 12),
            ([3, 4, 5, 4, 5, 6], "ב-i = 3 : 2 < 3, וה-2 מתחלף עם ה-3.\nהמערך 1, 2, 4, 3.", 14),
            ([4, 5, 6], "ב-j = 2 : 3 < 4, עוד החלפה,\nוהמערך 1, 2, 3, 4.", 15),
            ([4, 5, 4, 3], "ההשוואה האחרונה, 4 < 4, לא מתקיימת.\n‏16 השוואות, 5 החלפות, ומיון עולה.", 16),
        ], view=view)
        self.fade_all()

        # Why it works: the array at the end of every i, and the invariant.
        labels = ["start"] + [f"i = {i}" for i in range(4)]
        arrays = [A0] + ROWS
        rows = VGroup()
        for r, (lab, vals) in enumerate(zip(labels, arrays)):
            arr = Arr(vals, side=0.72, done=r - 1, size=32)
            tag = M(lab, 28, C.MUTED)
            rows.add(VGroup(tag, arr).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.22, aligned_edge=RIGHT).move_to(UP * 0.62)
        self.say("למה זה עובד תמיד? נסתכל על המערך\nבסוף כל איטרציה של i.",
                 LaggedStart(*[FadeIn(r, shift=0.15 * DOWN) for r in rows], lag_ratio=0.25),
                 run_time=2.0)
        claim = M("end of i:  A[0..i] sorted,  A[i] = max(A)", 30, C.AMBER).move_to(UP * 3.2)
        self.say("הטענה : בסוף איטרציה i, החלק A[0..i]\nממוין, ו-A[i] הוא המקסימום של כל המערך.",
                 FadeIn(claim))
        ring = rows[1][1].ring(0)
        self.say("שלב 1, i = 0 : כל איבר גדול יותר מתחלף\nעם A[0], ולכן בסוף A[0] הוא המקסימום.",
                 Create(ring))
        ring2 = rows[3][1].ring(1, C.BLUE)
        arrow = Arrow(rows[2][1].cells[2].get_bottom(), rows[3][1].cells[1].get_top(),
                      color=C.BLUE, buff=0.02, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        self.say("שלב 2, j < i : A[i] נכנס למקומו בחלק\nהממוין, כמו ב-insertion sort.",
                 Transform(ring, ring2), Create(arrow))
        ring3 = rows[3][1].ring(2)
        self.say("הגדולים ממנו זזים מקום אחד ימינה,\nוהמקסימום מגיע בדיוק ל-A[i].",
                 Transform(ring, ring3))
        never = M("j ≥ i:  A[i] < A[j]  never", 30, C.RED).next_to(rows, DOWN, buff=0.28)
        self.say("שלב 3, j ≥ i : A[i] הוא כבר המקסימום,\nולכן התנאי לא מתקיים ואין החלפות.",
                 FadeIn(never))
        last = SurroundingRectangle(rows[4][1], color=C.GREEN, buff=0.08, corner_radius=0.1,
                                    stroke_width=5)
        self.say("שלב 4 : אחרי i = n − 1, החלק הממוין\nהוא כל המערך. מיון עולה.",
                 FadeOut(arrow), FadeOut(never), Transform(ring, last))
        self.fade_all()

        chips = cost_chips(("time", "Θ(n²)"), ("memory", "O(1)"),
                           notes=("n · n comparisons", "in place"))
        self.say("הסיבוכיות : תמיד n² השוואות, גם\nכשהמערך כבר ממוין. זמן Θ(n²).",
                 FadeIn(chips, lag_ratio=0.3))
        self.say("אין יציאה מוקדמת, והמיון במקום :\nזיכרון נוסף O(1).")
        self.say("על 4 איברים, 16 השוואות.\nעל 1,000 איברים, מיליון השוואות.")
        self.fade_all()

        # The trap: guessing the direction from the condition.
        top = M("for j in range(n):", 32, C.GREEN)
        bot = M("for j in range(i + 1, n):", 32, C.RED)
        up = Arr(mystery_trace(A0)[0][-1], side=0.72, size=32, done=3)
        down = Arr(mystery_trace(A0, True)[0][-1], side=0.72, size=32)
        down.cells.set_stroke(C.RED)
        r1 = VGroup(top, up).arrange(RIGHT, buff=0.7)
        r2 = VGroup(bot, down).arrange(RIGHT, buff=0.7)
        both = VGroup(r1, r2).arrange(DOWN, buff=0.7, aligned_edge=RIGHT).move_to(UP * 0.7)
        self.say("המלכודת : לנחש את הכיוון מהתנאי.\nהניחוש \"יורד\" נכון רק אם j מתחיל מ-i + 1.",
                 FadeIn(r1), FadeIn(r2))
        self.say("אז זה selection sort, והתוצאה 4, 3, 2, 1.\nאותו תנאי, כיוון הפוך.",
                 Indicate(down, color=C.RED, scale_factor=1.08), run_time=1.2)
        self.say("שם כל i מביא ל-A[i] את המקסימום\nשל A[i..n − 1], ולכן הגדולים בהתחלה.")
        self.fade_all()


class Closing(DVQScene):
    def construct(self):
        self.closing(QID, [("התשובה", M("ascending sort,  n² comparisons", 34))],
                     ["לסיכום : הקוד ממיין בסדר עולה,\nתמיד ב-n² השוואות.",
                      "נסו מערך משלכם בתיבה\nשבעמוד של שאלה 0003 באתר."],
                     holds=(3.2, 3.5))
