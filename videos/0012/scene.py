"""The tutorial video of question 0012, sort the digits and subtract (script: script.md).

Render with `python videos/render.py 0012` (see notes/VIDEOS.md). The owner's choice
(2026-11-01): parts א and ב in full, part ג briefly. Part א: the step on 352 drawn as digit
cells (sort once: ascending is the smallest, reversed the largest), the box's column
subtraction on the page's examples, `is_special` typed and traced on 352 and 495 beside
the box, the cost and the leading-zero trap. Part ב: the difference is 99(a − c), so only
ten candidates; the table of the nine non-zero ones (only 495 returns to itself); the
digit proof; `find_special` typed, its run jumping from 0 to 495 to the end; the box's
chain and histogram; the map of d (3 → 7 → 6 → 5); the cost. Part ג: d(b² − 1), the
digits (d − 1, b − 1, b − d), the map d' = max(b − d, d − 1), even base a fixed point,
odd base a 2-cycle, and the page's base-7 box from 610; no code and no full proof.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 12
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – לבדוק מספר אחד"),
    ("ChapterB", "סעיף ב – לבדוק את כל המספרים"),
    ("ChapterC", "סעיף ג – שלוש ספרות בבסיס b"),
    ("Closing", "סיכום"),
]

# The page's boxes. Box 0 (kaprekar): "cols" the column subtraction of the first step on
# 352, then the presets 7 and 45, then 495 typed (the chain table hidden); "chain" the
# chain table of 352, then of 100 (the longest, six steps); "hist" the histogram over all
# 1,000 numbers; "cols_n" the pictures of "cols" 440 CSS px wide, for beside the code.
# Box 1 (kapbase, base 10, from 352): "dmap" the map of d, a step a click
# (3 -> 7 -> 6 -> 5). Box 2 (kapbase, base 7, from 610): "base7" the same, three steps to
# the cycle 363 <-> 264.
BOXES = {
    "cols": {"box": 0, "region": [":scope > .ex-controls", ".kp-cols"],
             "hide": [".kp-table", ".kp-chain"],
             "steps": [[], [["click", ".ex-preset[data-x='7']"]], [["click", ".ex-preset[data-x='45']"]],
                       [["fill", ".ex-x", "495"]]]},
    "cols_n": {"box": 0, "width": 440, "region": [":scope > .ex-controls", ".kp-cols"],
               "hide": [".kp-table", ".kp-chain"],
               "steps": [[], [["click", ".ex-preset[data-x='7']"]], [["click", ".ex-preset[data-x='45']"]],
                         [["fill", ".ex-x", "495"]]]},
    "chain": {"box": 0, "region": [":scope > .ex-controls", ".kp-table", ".kp-chain"],
              "steps": [[], [["fill", ".ex-x", "100"]]]},
    "hist": {"box": 0, "region": [".kp-chart", ".kp-sum"], "steps": [[]]},
    "dmap": {"box": 1, "region": [".ex-play-row", ".kb-step", ".kb-map"],
             "hide": [".kb-chart", ".kb-hist-title", ".kb-table", ".kb-sum", ".ex-title"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 4}]},
    "base7": {"box": 2, "region": [".ex-play-row", ".kb-step", ".kb-map"],
              "hide": [".kb-chart", ".kb-hist-title", ".kb-table", ".kb-sum", ".ex-title"],
              "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 3}]},
}


# The reference, independent of the page code: the step, the special numbers, the d-map.
def step(x: int) -> tuple[int, int, int]:
    """(largest, smallest, difference) of x written with three digits."""
    ds = sorted(f"{x:03d}")
    lo, hi = int("".join(ds)), int("".join(reversed(ds)))
    return hi, lo, hi - lo


SPECIAL = [x for x in range(1000) if step(x)[2] == x]
assert SPECIAL == [0, 495]
assert step(352) == (532, 235, 297) and step(7) == (700, 7, 693) and step(45) == (540, 45, 495)
CHAIN_352 = [352, 297, 693, 594, 495]
assert all(step(a)[2] == b for a, b in zip(CHAIN_352, CHAIN_352[1:]))
assert [max(int(c) for c in f"{x:03d}") - min(int(c) for c in f"{x:03d}") for x in CHAIN_352] == [3, 7, 6, 5, 5]
CANDIDATES = [(d, 99 * d) + step(99 * d) for d in range(1, 10)]
assert [r[1] for r in CANDIDATES if r[4] == r[1]] == [495]


def base_step(x: int, b: int) -> int:
    lo, mid, hi = sorted((x // (b * b), x // b % b, x % b))
    return (hi * b * b + mid * b + lo) - (lo * b * b + mid * b + hi)


def in_base(x: int, b: int) -> str:
    return "".join(str(v) for v in (x // (b * b), x // b % b, x % b))


B7 = [6 * 49 + 1 * 7 + 0]
for _ in range(4):
    B7.append(base_step(B7[-1], 7))
assert [in_base(x, 7) for x in B7] == ["610", "561", "462", "363", "264"]


class Digits(VGroup):
    """A three-digit number as a row of cells, centred on `centre`."""

    def __init__(self, s: str, centre=ORIGIN, side: float = 0.95, color: str | None = None):
        super().__init__()
        self.side = side
        self.cells = VGroup(*[self.cell(ch, color) for ch in s])
        self.cells.arrange(RIGHT, buff=0.12).move_to(centre)
        self.add(self.cells)

    def cell(self, ch: str, color: str | None) -> VGroup:
        box = RoundedRectangle(width=self.side, height=self.side, corner_radius=0.12,
                               stroke_color=color or C.MUTED, stroke_width=2.5,
                               fill_color=C.NAVY_LIGHT, fill_opacity=1)
        return VGroup(box, M(ch, 56 * self.side / 0.95, color or C.WHITE).move_to(box))


def mark(ok: bool, where) -> Text:
    return M("✓" if ok else "✗", 48, C.GREEN if ok else C.RED, weight="BOLD").move_to(where)


class KScene(DVQScene):
    """Helpers shared by the chapters of 0012."""

    def sort_demo(self, s: str, y: float = 1.7):
        """The number's cells, then sorted ascending (the smallest) and reversed (the
        largest), each a row with its Latin name. Returns (x row, small row, large row)."""
        top = Digits(s, UP * y)
        name = M("x", 40, C.MUTED).next_to(top, LEFT, buff=0.5)
        self.play(FadeIn(name), FadeIn(top, lag_ratio=0.15), run_time=0.9)
        order = sorted(range(3), key=lambda i: s[i])
        small = top.copy()
        target = VGroup(*[small.cells[i].copy() for i in order]).arrange(RIGHT, buff=0.12)
        target.move_to([-2.6, y - 1.9, 0])
        self.play(*[small.cells[i].animate.move_to(target[k]) for k, i in enumerate(order)], run_time=1.1)
        large = VGroup(*[small.cells[i].copy() for i in reversed(order)])
        large.arrange(RIGHT, buff=0.12).move_to([2.6, y - 1.9, 0])
        return VGroup(name, top), small, large


class Opening(KScene):
    def construct(self):
        self.opening(QID, "סטודנט", "ממיינים ספרות ומחסרים",
                     ["א · לבדוק מספר אחד", "ב · לבדוק את כל המספרים", "ג · שלוש ספרות בבסיס b"],
                     ["שאלה 0012 : ממיינים ספרות ומחסרים,\nשאלה ברמת סטודנט.",
                      "שלושה סעיפים : לבדוק מספר אחד,\nלבדוק את כל המספרים, ובסיס אחר."])
        self.fade_all()
        top = Digits("352", UP * 1.7)
        name = M("x", 40, C.MUTED).next_to(top, LEFT, buff=0.5)
        self.say("לוקחים מספר בין 0 ל-999, למשל 352,\nוכותבים אותו בשלוש ספרות.",
                 FadeIn(name), FadeIn(top, lag_ratio=0.15))
        desc = Digits("532", [2.6, -0.2, 0])
        asc = Digits("235", [-2.6, -0.2, 0])
        dl = M("desc", 32, C.MUTED).next_to(desc, UP, buff=0.25)
        al = M("asc", 32, C.MUTED).next_to(asc, UP, buff=0.25)
        self.say("ממיינים את הספרות מהגדול לקטן, 532,\nומהקטן לגדול, 235.",
                 FadeIn(desc, shift=0.2 * DOWN), FadeIn(asc, shift=0.2 * DOWN), FadeIn(dl), FadeIn(al))
        diff = M("532 − 235 = 297", 44).move_to(DOWN * 1.6)
        self.say("מחסרים את הקטן מהגדול,\nומקבלים 297.", FadeIn(diff, shift=0.2 * UP))
        rule = M("297 = x ?", 40, C.AMBER).next_to(diff, RIGHT, buff=0.7)
        self.say("אם ההפרש שווה למספר עצמו,\nהמספר נקרא מיוחד.", FadeIn(rule))
        no = mark(False, rule.get_right() + RIGHT * 0.5)
        self.say("כאן 297 שונה מ-352,\nולכן 352 לא מיוחד.", FadeIn(no, scale=1.4))
        self.fade_all()


class ChapterA(KScene):
    def construct(self):
        self.chapter_card("סעיף א", "לבדוק מספר אחד",
                          "סעיף א : פונקציה שמקבלת מספר x,\nומחזירה 1 אם הוא מיוחד, ו-0 אחרת.")

        # The leading zeros: 7 is 007.
        seven = Digits("007", UP * 1.2)
        name = M("x = 7", 40, C.MUTED).next_to(seven, LEFT, buff=0.6)
        zeros = SurroundingRectangle(VGroup(seven.cells[0], seven.cells[1]), color=C.AMBER,
                                     buff=0.08, corner_radius=0.12, stroke_width=5)
        self.say("קודם כול : מספר קטן מ-100 מקבל\nאפסים משמאל. ‏7 נכתב 007.",
                 FadeIn(name), FadeIn(seven, lag_ratio=0.15), Create(zeros), run_time=1.4)
        calc = M("700 − 007 = 693", 44).move_to(DOWN * 0.6)
        self.say("מהגדול לקטן זה 700, ומהקטן לגדול 007 :\nההפרש 693.", FadeIn(calc, shift=0.2 * UP))
        self.fade_all()

        # The idea: one sort, read both ways.
        with self.beat("הרעיון : שני המספרים בנויים\nמאותן שלוש ספרות."):
            x_row, small, large = self.sort_demo("352")
        sl = M("smallest = 235", 34, C.GREEN).next_to(small, DOWN, buff=0.35)
        self.say("ממיינים פעם אחת בסדר עולה :\nזה המספר הקטן, 235.", FadeIn(sl))
        arrow = Arrow(small.get_right(), large.get_left(), buff=0.25, color=C.AMBER, stroke_width=5)
        rev = M("reversed", 30, C.AMBER).next_to(arrow, UP, buff=0.12)
        ll = M("largest = 532", 34, C.GREEN).next_to(large, DOWN, buff=0.35)
        self.say("אותן ספרות בסדר הפוך הן הגדול,\n‏532. אין צורך במיון שני.",
                 GrowArrow(arrow), FadeIn(rev), FadeIn(large, shift=0.2 * RIGHT), FadeIn(ll))
        self.fade_all()

        # The page's box: the column subtraction of the page's examples.
        view = BoxView(QID, "cols", width=10.6).move_to(UP * 0.6)
        self.say("כך זה נראה בתיבה שבעמוד :\nהחיסור במאונך, עמודה אחרי עמודה.", FadeIn(view))
        self.say("‏532 פחות 235, עם שני לווים :\nההפרש 297, ולכן 352 לא מיוחד.")
        self.box_beat(view, [
            (1, "הדוגמה 7 : ‏700 פחות 007 הם 693."),
            (2, "הדוגמה 45 : ‏540 פחות 045 הם 495.\nההפרש שונה מ-45, ולכן 45 לא מיוחד."),
            (3, "ועכשיו 495 : ‏954 פחות 459\nהם 495 בדיוק. הוא מיוחד."),
        ])
        self.fade_all()

        # The code: typed, then traced on 352 and 495 beside the box.
        code = page_python(QID, "def is_special")
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True)

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            return "[" + ", ".join(repr(c) for c in v) + "]" if n == "digits" else str(v)

        vp = VarPanel(["x", "digits", "smallest", "largest"], fmt=fmt, size=28, cols=2,
                      slot=4.6).set_state({})
        self.place_code(panel, vp_width=9.5)
        self.type_code(panel, [
            (1, "הפונקציה is_special מקבלת את x,\nומחזירה 1 או 0."),
            (2, ["הפורמט 03d כותב את x בשלוש ספרות,\nעם אפסים משמאל : 7 הופך ל-007.",
                 "‏sorted ממיינת את שלושת התווים\nבסדר עולה, לרשימה."]),
            (3, "החיבור של התווים בסדר עולה\nנותן את המספר הקטן."),
            (4, "אותם תווים בסדר הפוך נותנים\nאת הגדול, בלי מיון שני."),
            (5, "בסוף משווים את ההפרש ל-x,\nומחזירים 1 או 0."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        steps, result = trace(code, "is_special", (352,))
        assert result == 0 and [s.line for s in steps] == [2, 3, 4, 5]
        view = BoxView(QID, "cols_n")
        with self.beat("נריץ את הקוד על 352,\nלצד התיבה מהעמוד."):
            self.split(panel, view, vp)
        cursor = self.run_code(panel, vp, steps, [
            ([2], "‏x = 352 : הספרות בסדר עולה\nהן 2, 3 ו-5.", None),
            ([3], "המספר הקטן הוא 235.", None),
            ([4], "והגדול הוא 532.", None),
            ([5], "‏532 פחות 235 הם 297, לא 352 :\nהפונקציה מחזירה 0.", None),
        ], view=view)

        steps, result = trace(code, "is_special", (495,))
        assert result == 1 and [s.line for s in steps] == [2, 3, 4, 5]
        self.play(FadeOut(cursor), *vp.show({}, flash=False), run_time=0.4)
        self.run_code(panel, vp, steps, [
            ([2], "עכשיו x = 495 : הספרות\nבסדר עולה הן 4, 5 ו-9.", 3),
            ([3, 4], "הקטן הוא 459, והגדול 954.", None),
            ([5], "ההפרש 495, בדיוק x :\nהפונקציה מחזירה 1.", None),
        ], view=view)
        self.fade_all()

        chips = cost_chips(("time", "$O(1)$"), ("memory", "$O(1)$"),
                           notes=("always 3 digits", "3 digits, 2 numbers"))
        self.say("הסיבוכיות : תמיד שלוש ספרות,\nולכן זמן O(1) וזיכרון O(1).",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: no padding.
        bad = VGroup(M("\"45\":", 40, C.MUTED), M("54 − 45 = 9", 44, C.RED)).arrange(RIGHT, buff=0.5)
        good = VGroup(M("\"045\":", 40, C.MUTED), M("540 − 045 = 495", 44, C.GREEN)).arrange(RIGHT, buff=0.5)
        VGroup(bad, good).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(UP * 0.7)
        self.say("מלכודת : לשכוח את האפסים. בלי ריפוד,\n‏45 נותן 54 פחות 45, כלומר 9.",
                 FadeIn(bad, shift=0.2 * RIGHT))
        self.say("עם ריפוד זה 540 פחות 045, כלומר 495.\nמספר קטן הוא עדיין מספר בן שלוש ספרות.",
                 FadeIn(good, shift=0.2 * RIGHT))
        self.fade_all()


class ChapterB(KScene):
    def construct(self):
        self.chapter_card("סעיף ב", "לבדוק את כל המספרים",
                          "סעיף ב : מריצים את הפונקציה על 0 עד 999.\nאילו מספרים מיוחדים, ולמה?")

        # The difference is 99 (a - c).
        abc = TX(r"a \ge b \ge c", size=44, color=C.AMBER).move_to(UP * 2.2)
        self.say("נסמן את הספרות הממוינות :\nהגדולה a, האמצעית b, והקטנה c.", FadeIn(abc))
        diff = TX(r"(100a + 10b + c)", r"-", r"(100c + 10b + a)", size=40).move_to(UP * 0.9)
        self.say("הגדול פחות הקטן : מאות, עשרות ואחדות,\nפעם בסדר אחד ופעם בסדר ההפוך.", FadeIn(diff))
        mids = VGroup(diff[0][6:9], diff[2][6:9])
        cross = VGroup(*[Line(m.get_corner(DL), m.get_corner(UR), color=C.RED, stroke_width=5) for m in mids])
        self.say("ספרת האמצע b מופיעה פעמיים, 10b,\nומתבטלת בחיסור.", Create(cross))
        res = TX(r"= 99a - 99c", r"= 99\,(a - c)", size=44).next_to(diff, DOWN, buff=0.55)
        res[1].set_color(C.AMBER)
        self.say("נשאר 99 כפול a פחות c :\nההפרש תמיד כפולה של 99.", FadeIn(res))
        dd = TX(r"d = a - c,\quad 0 \le d \le 9", size=40, color=C.MUTED).next_to(res, DOWN, buff=0.55)
        self.say("נסמן d = a − c. הוא בין 0 ל-9,\nולכן יש רק עשרה הפרשים אפשריים.", FadeIn(dd))
        self.fade_all()

        cands = VGroup(*[M(f"{99 * d:03d}", 34, C.AMBER if d == 5 else C.WHITE) for d in range(10)])
        cands.arrange(RIGHT, buff=0.32).move_to(UP * 0.8)
        dl = VGroup(*[M(f"d={d}", 24, C.MUTED).next_to(c, DOWN, buff=0.25) for d, c in zip(range(10), cands)])
        self.say("מספר מיוחד שווה להפרש שלו,\nולכן הוא אחד מעשרת המועמדים האלה.",
                 LaggedStart(*[FadeIn(c, shift=0.15 * DOWN) for c in cands], lag_ratio=0.1),
                 FadeIn(dl), run_time=1.8)
        self.fade_all()

        # The table of the nine non-zero candidates.
        head = ["d", "99d", "desc", "asc", "desc − asc", ""]
        xs = [-5.0, -3.4, -1.4, 0.6, 3.0, 5.0]
        y0, dy = 3.0, 0.56
        hrow = VGroup(*[M(h, 28, C.MUTED).move_to([x, y0, 0]) for h, x in zip(head, xs)])
        rule = Line([-5.6, y0 - 0.3, 0], [5.6, y0 - 0.3, 0], color=C.FAINT, stroke_width=2)
        rows = []
        for k, (d, v, hi, lo, df) in enumerate(CANDIDATES):
            y = y0 - (k + 1) * dy - 0.05
            ok = df == v
            cells = [f"{d}", f"{v:03d}", f"{hi:03d}", f"{lo:03d}", f"{df:03d}"]
            row = VGroup(*[M(t, 30, C.GREEN if ok and i == 4 else C.WHITE).move_to([x, y, 0])
                           for i, (t, x) in enumerate(zip(cells, xs))])
            row.add(mark(ok, [xs[5], y, 0]).scale(0.7))
            rows.append(row)
        with self.beat("בודקים את תשעת המועמדים שאינם 0 :\nממיינים, מחסרים ומשווים."):
            self.play(FadeIn(hrow), Create(rule), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=0.1 * DOWN) for r in rows], lag_ratio=0.25), run_time=2.6)
        hl = SurroundingRectangle(rows[4], color=C.GREEN, buff=0.1, corner_radius=0.1, stroke_width=4)
        self.say("רק 495 חוזר לעצמו : ‏954 פחות 459.\nיחד עם 0, אלה שני המספרים המיוחדים.", Create(hl))
        pair = VGroup(SurroundingRectangle(rows[2], color=C.BLUE, buff=0.08, corner_radius=0.1, stroke_width=3),
                      SurroundingRectangle(rows[6], color=C.BLUE, buff=0.08, corner_radius=0.1, stroke_width=3))
        self.say("שימו לב : d ו-10 פחות d בנויים\nמאותן ספרות, ונותנים אותו הפרש.", Create(pair))
        self.fade_all()

        # The proof by the digits, without the table.
        l1 = TX(r"99d = 100\,(d-1) + 10 \cdot 9 + (10-d)", size=40).move_to(UP * 2.1)
        self.say("ההוכחה בלי טבלה : ל-99d יש תמיד\nאת הספרות d − 1, ‏9 ו-10 − d.", FadeIn(l1))
        l2 = TX(r"x = 99d \;\Rightarrow\; a = 9,\quad c = 9 - d", size=40).next_to(l1, DOWN, buff=0.55)
        self.say("אם x שווה להפרש, יש בו 9, הספרה\nהגדולה ביותר : לכן a = 9, ו-c = 9 − d.",
                 l1.animate.set_opacity(0.45), FadeIn(l2))
        l3 = TX(r"\{\, b,\; 9-d \,\} = \{\, d-1,\; 10-d \,\}", size=40).next_to(l2, DOWN, buff=0.55)
        self.say("שתי הספרות האחרות שוות לשתיים מימין,\nו-9 − d לא יכול להיות 10 − d.",
                 l2.animate.set_opacity(0.45), FadeIn(l3))
        l4 = TX(r"9-d = d-1 \;\Rightarrow\; d = 5 \;\Rightarrow\; x = 495", size=42, color=C.AMBER)
        l4.next_to(l3, DOWN, buff=0.55)
        self.say("לכן 9 − d = d − 1, כלומר d = 5,\nוהמספר הוא 99 כפול 5 : ‏495.",
                 l3.animate.set_opacity(0.45), FadeIn(l4))
        self.fade_all()

        # The code: typed, then its run, jumping over the numbers that are not special.
        code = page_python(QID, "def find_special")
        panel = CodePanel(code, font_size=34)
        env = {}
        exec(page_python(QID, "def is_special"), env)
        steps, result = trace(code, "find_special", (), env=env)
        assert result == [0, 495] and set(s.line for s in steps) == {2}
        self.place_code(panel)
        panel.shift(UP * 1.2)
        self.type_code(panel, [
            (1, "‏find_special לא מקבלת כלום,\nומחזירה רשימה."),
            (2, "היא עוברת על x מ-0 עד 999, ושומרת\nכל x ש-is_special מחזירה עבורו 1."),
        ], intro="ובקוד : בלי ההוכחה, פשוט בודקים הכול.")
        xv = M("x = 0", 40).move_to(LEFT * 3.2 + DOWN * 1.0)
        out = M("[0]", 40, C.GREEN).move_to(RIGHT * 2.4 + DOWN * 1.0)
        out_name = M("result:", 32, C.MUTED).next_to(out, LEFT, buff=0.3)
        bar = panel.bar(2)
        self.say("‏x = 0 : כל הספרות 0, וההפרש 0.\nהוא מיוחד, ונכנס לרשימה.",
                 FadeIn(bar), FadeIn(xv), FadeIn(out_name), FadeIn(out))
        with self.beat("מ-1 עד 494 אין אף מספר מיוחד,\nולכן קופצים קדימה."):
            for v in (100, 200, 300, 400, 494):
                self.play(Transform(xv, M(f"x = {v}", 40).move_to(xv)), run_time=0.35)
        new = M("[0, 495]", 40, C.GREEN).move_to(out).align_to(out, LEFT)
        self.say("‏x = 495 : ‏954 פחות 459 הם 495.\nמיוחד, ונכנס לרשימה.",
                 Transform(xv, M("x = 495", 40, C.AMBER).move_to(xv)), Transform(out, new))
        with self.beat("ומ-496 עד 999 שוב אין אף אחד :\nהתוצאה היא 0 ו-495."):
            for v in (600, 800, 999):
                self.play(Transform(xv, M(f"x = {v}", 40).move_to(xv)), run_time=0.35)
            self.play(Indicate(out, color=C.AMBER), run_time=0.8)
        self.fade_all()

        # The page's boxes: the chain to 495, the histogram, the map of d.
        view = BoxView(QID, "chain", height=5.7).move_to(UP * 0.62)
        self.say("התיבה שבעמוד מפעילה את הצעד שוב ושוב\nעל ההפרש : ‏352 מגיע ל-495.", FadeIn(view))
        self.box_beat(view, [
            (1, "‏100 הוא הארוך ביותר : שישה צעדים\nעד 495, ושם הוא נעצר."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        hist = BoxView(QID, "hist", width=11.0).move_to(UP * 0.6)
        self.say("על כל 1,000 המספרים : ‏990 מגיעים ל-495\nתוך שישה צעדים לכל היותר, ו-10 ל-0.", FadeIn(hist))
        self.play(FadeOut(hist), run_time=0.6)
        dmap = BoxView(QID, "dmap", height=5.7).move_to(UP * 0.62)
        self.say("והמפה של d : ‏352 נותן d = 3.\nכל צעד מעביר את d לערך הבא.", FadeIn(dmap))
        self.box_beat(dmap, [
            (1, "צעד 1 : ‏352 הופך ל-297,\nו-d קופץ מ-3 ל-7."),
            (2, "צעד 2 : ‏297 הופך ל-693, ו-d = 6."),
            (3, "צעד 3 : ‏693 הופך ל-594, ו-d = 5."),
            (4, "צעד 4 : ‏594 הופך ל-495. רק 5\nמצביע על עצמו : נקודת השבת."),
        ])
        self.fade_all()

        chips = cost_chips(("loop", "1000"), ("by the proof", "10"),
                           notes=("each check O(1)", "the multiples of 99"))
        self.say("הלולאה בודקת 1,000 מספרים, כל אחד ב-O(1).\nלפי ההוכחה מספיק לבדוק עשרה.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterC(KScene):
    def construct(self):
        self.chapter_card("סעיף ג", "שלוש ספרות בבסיס b",
                          "סעיף ג, בקצרה : אותו תהליך,\nאבל המספר כתוב בבסיס b.")
        l1 = TX(r"F(X) = d\,(b^2 - 1)", size=44).move_to(UP * 2.2)
        self.say("אותו חישוב : ספרת האמצע מתבטלת,\nוההפרש הוא d כפול b² − 1.", FadeIn(l1))
        l2 = TX(r"d\,(b^2-1) = (d-1)\,b^2 + (b-1)\,b + (b-d)", size=40).next_to(l1, DOWN, buff=0.55)
        self.say("הספרות שלו תמיד d − 1, ‏b − 1 ו-b − d,\nולכן ה-d הבא תלוי רק ב-d.",
                 l1.animate.set_opacity(0.45), FadeIn(l2))
        l3 = TX(r"d' = \max(b-d,\; d-1)", size=44, color=C.AMBER).next_to(l2, DOWN, buff=0.55)
        self.say("ה-d הבא הוא המקסימום של b − d ו-d − 1 :\nהמפה דוחפת את d לאמצע, b/2.",
                 l2.animate.set_opacity(0.45), FadeIn(l3))
        even = TX(r"b \text{ even}:\ d = b/2 \ \text{stays}", size=38, color=C.GREEN)
        odd = TX(r"b \text{ odd}:\ d \leftrightarrow d+1", size=38, color=C.BLUE)
        VGroup(even, odd).arrange(RIGHT, buff=1.2).next_to(l3, DOWN, buff=0.6)
        self.say("בסיס זוגי : d = b/2 נשאר במקום.\nנקודת שבת יחידה, ובבסיס 10 זה 495.", FadeIn(even))
        self.say("בסיס אי-זוגי : אין אמצע שלם, ו-d\nמתנדנד בין שני שלמים : מחזור באורך 2.", FadeIn(odd))
        self.fade_all()

        view = BoxView(QID, "base7", height=5.7).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד : בסיס 7, מתחילים מ-610.\nה-d שלו הוא 6 פחות 0, כלומר 6.", FadeIn(view))
        self.box_beat(view, [
            (1, "צעד 1 : ‏610 הופך ל-561, ו-d = 5."),
            (2, "צעד 2 : ‏561 הופך ל-462, ו-d = 4."),
            (3, "צעד 3 : ‏462 הופך ל-363, ו-d = 3.\nמכאן 363 ו-264 מתחלפים לנצח."),
        ])
        self.say("התשובה : בבסיס זוגי נקודת שבת אחת,\nובבסיס אי-זוגי מחזור של שני מספרים.")
        self.fade_all()


class Closing(KScene):
    def construct(self):
        self.closing(QID, [("א", M("sort once: largest − smallest == x", 30)),
                           ("ב", TX(r"99\,(a - c) \;\Rightarrow\; \{0,\ 495\}", size=34)),
                           ("ג", TX(r"b \text{ even: a fixed point};\ \ b \text{ odd: a 2-cycle}", size=34))],
                     ["לסיכום : ממיינים פעם אחת ומחסרים,\nוההפרש תמיד כפולה של 99.",
                      "נסו מספרים ובסיסים משלכם בתיבות\nשבעמוד של שאלה 0012 באתר."],
                     holds=(3.5, 3.5))
