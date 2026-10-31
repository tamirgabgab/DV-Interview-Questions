"""The tutorial video of question 0002, swap two variables (script: script.md).

Render with `python videos/render.py 0002` (see VIDEOS.md). The example is the page's,
a = 5 and b = 3; the code beats run the page's Python on v = [5, 3], i = 0, j = 1.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (BoxView, C, Cell, CodePanel, DVQScene, M, T, X, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 2
# The page's three trace boxes (VIDEOS.md, "The page's box"): picture k after k clicks on
# "next", the box's line k run on a = 5, b = 3.
BOXES = {
    "temp": {"box": 0, "region": [".ex-play-row", ".tr-box", ".tr-step"], "hide": [".ex-scrubwrap"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "arith": {"box": 1, "region": [".ex-play-row", ".tr-box", ".tr-step"], "hide": [".ex-scrubwrap"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "xor": {"box": 2, "region": [".ex-play-row", ".tr-box", ".tr-step"], "hide": [".ex-scrubwrap"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 3}]},
}
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – עם משתנה עזר"),
    ("ChapterB", "סעיף ב – בלי משתנה עזר"),
    ("ChapterC", "סעיף ג – רק אופרטורים על ביטים"),
    ("Closing", "סיכום"),
]

A0, B0 = 5, 3            # the page's example
NUM = {"5": C.AMBER, "3": C.BLUE}


def bits(n: int, w: int = 4) -> str:
    return format(n & ((1 << w) - 1), f"0{w}b")


class SwapScene(DVQScene):
    """Helpers shared by the chapters of 0002."""

    def statement(self, text: str, old=None, color=None):
        """The step's statement above the picture; returns (mobject, animation)."""
        new = M(text, 44, color or C.AMBER).move_to(UP * 2.8)
        return new, (Transform(old, new) if old is not None else FadeIn(new, shift=0.15 * DOWN))

    def travel(self, src: Cell, dst: Cell, run_time: float = 1.4):
        """The value of `src` travels as a card into `dst`; dst's old value fades."""
        card = src.value.copy()
        old = dst.value
        self.add(card)
        self.play(card.animate.move_to(dst.box.get_center()), old.animate.set_opacity(0),
                  run_time=run_time)
        dst.remove(old)
        self.remove(old, card)
        dst.value = card
        dst.add(card)

    def box_idea(self, name: str, intro: str, steps: list):
        """The page's box, alone and large, played on the example: a caption per line."""
        view = BoxView(QID, name, height=5.5).move_to(UP * 0.55)
        self.say(intro, FadeIn(view))
        self.box_beat(view, steps)
        self.fade_all()

    def code(self, marker: str, func: str, box: str, typed, run, groups, intro=None, size=34,
             extra=None, share=None):
        """The code beat: the page's function typed line by line under its captions
        (`typed`), then beside the page's box (`run`, the split screen), its lines lit in
        the order they ran while the box steps with them (`groups`: (lines, caption, k))."""
        code = page_python(QID, marker)
        steps, _ = trace(code, func, ([A0, B0], 0, 1))
        panel = CodePanel(code, font_size=size)
        self.place_code(panel, None, extra)
        self.type_code(panel, typed, intro=intro)
        view = BoxView(QID, box)
        with self.beat(run):
            if extra is not None:
                self.play(FadeOut(extra), run_time=0.5)
            self.split(panel, view, code_share=share)   # share: the code's part of the width
        self.run_code(panel, None, steps, groups, view=view)


class Opening(SwapScene):
    def construct(self):
        self.opening(QID, "סטודנט", "החלפת ערכים בין שני משתנים",
                     ["א · עם משתנה עזר", "ב · בלי משתנה עזר", "ג · רק אופרטורים על ביטים"],
                     ["שאלה 0002 : החלפת ערכים בין שני משתנים,\nשאלה ברמת סטודנט.",
                      "שלושה סעיפים, וכל סעיף מוסיף אילוץ :\nעם משתנה עזר, בלי משתנה עזר, ורק ביטים."])
        a = Cell("a", A0).move_to(LEFT * 2.6 + UP * 1.7)
        b = Cell("b", B0).move_to(RIGHT * 2.6 + UP * 1.7)
        a.value.set_color(C.AMBER)
        b.value.set_color(C.BLUE)
        ba = M(bits(A0), 32, C.MUTED).next_to(a.box, DOWN, buff=0.25)
        bb = M(bits(B0), 32, C.MUTED).next_to(b.box, DOWN, buff=0.25)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)
        self.say("הפונקציה swap מקבלת שני משתנים, a ו-b,\nומחליפה ביניהם במקום.",
                 FadeIn(a), FadeIn(b), FadeIn(ba), FadeIn(bb))
        ga = M(str(B0), 56, C.BLUE).move_to(LEFT * 2.6 + DOWN * 1.7)
        gb = M(str(A0), 56, C.AMBER).move_to(RIGHT * 2.6 + DOWN * 1.7)
        boxes = VGroup(*[DashedVMobject(RoundedRectangle(width=2.2, height=1.3, corner_radius=0.16,
                                                         stroke_color=C.GREEN, stroke_width=3),
                                        num_dashes=28).move_to(g) for g in (ga, gb)])
        arrows = VGroup(
            Arrow(ba.get_bottom() + DOWN * 0.1, boxes[1].get_top(), color=C.AMBER, stroke_width=5,
                  buff=0.12),
            Arrow(bb.get_bottom() + DOWN * 0.1, boxes[0].get_top(), color=C.BLUE, stroke_width=5,
                  buff=0.12))
        self.say("בסוף a מחזיק את הערך המקורי של b,\nו-b את הערך המקורי של a.",
                 GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(boxes), FadeIn(ga), FadeIn(gb))
        self.fade_all()


class ChapterA(SwapScene):
    def construct(self):
        self.chapter_card("סעיף א", "עם משתנה עזר", "סעיף א : הדרך הפשוטה ביותר, עם משתנה עזר.")
        a = Cell("a", A0).move_to(LEFT * 4.0 + DOWN * 0.1)
        b = Cell("b", B0).move_to(DOWN * 0.1)
        self.say("יש לנו שני משתנים : a שווה 5, ו-b שווה 3.", FadeIn(a), FadeIn(b))
        goal = VGroup(M(str(B0), 48, C.GREEN).next_to(a.box, DOWN, buff=1.0),
                      M(str(A0), 48, C.GREEN).next_to(b.box, DOWN, buff=1.0))
        goal_arrows = VGroup(*[Arrow(c.box.get_bottom(), g.get_top(), buff=0.15, color=C.GREEN,
                                     stroke_width=4) for c, g in zip((a, b), goal)])
        self.say("המטרה : ש-a יחזיק 3, ו-b יחזיק 5.", FadeIn(goal), *map(GrowArrow, goal_arrows))
        temp = Cell("temp", "", name_color=C.AMBER).move_to(RIGHT * 4.0 + DOWN * 0.1)
        self.say("הרעיון : משתנה עזר, temp,\nששומר את הערך של a לפני שדורסים אותו.",
                 FadeOut(goal), FadeOut(goal_arrows), FadeIn(temp, shift=0.2 * LEFT))

        with self.beat("שלב 1 : temp = a. הערך 5 נשמר ב-temp."):
            stmt, anim = self.statement("temp = a")
            self.play(anim, run_time=0.8)
            self.travel(a, temp)
        with self.beat("שלב 2 : a = b. עכשיו a מחזיק 3,\nוה-5 המקורי עדיין שמור ב-temp."):
            self.play(self.statement("a = b", stmt)[1], run_time=0.8)
            self.travel(b, a)
        with self.beat("שלב 3 : b = temp, ו-b מקבל 5.\nההחלפה הושלמה."):
            self.play(self.statement("b = temp", stmt)[1], run_time=0.8)
            self.travel(temp, b)
            self.play(a.box.animate.set_stroke(C.GREEN, 5), b.box.animate.set_stroke(C.GREEN, 5),
                      run_time=0.6)
        self.fade_all()
        self.box_idea('temp', 'אותה דוגמה בתיבה שבעמוד\xa0:\nהקוד, ומתחתיו הערך של כל משתנה.',
                      [
                       (1, '\u200ftemp שומר את a0, הערך 5,\nלפני שדורסים את v[i].'),
                       (2, '\u200fv[i] מקבל את b0, והעמודה הסימבולית\nמראה ש-a0 שמור רק ב-temp.'),
                       (3, '\u200fv[j] מקבל את a0 מ-temp.\nבסוף a = b0 ו-b = a0.')])

        extra = VGroup(M("a ≡ v[i]", 34, C.MUTED), M("b ≡ v[j]", 34, C.MUTED)).arrange(RIGHT, buff=1.4)
        self.code("def swap_temp", "swap_temp", "temp",
                  [(1, ["ב-Python אין העברה של int by reference,\nולכן מעבירים רשימה v ושני אינדקסים, i ו-j.",
                        ("כאן v[i] משחק את התפקיד של a,\nו-v[j] את התפקיד של b.", [FadeIn(extra)])]),
                   (2, "שורה 2 : שומרים ב-temp את v[i],\nהערך של a, לפני שדורסים אותו."),
                   (3, "שורה 3 : עכשיו מותר לדרוס את v[i],\nוהוא מקבל את הערך של b."),
                   (4, "שורה 4 : v[j] מקבל את הערך המקורי של a,\nששמור ב-temp.")],
                  'מימין, התיבה מהעמוד מריצה את אותו הקוד\nעל [5, 3], עם i = 0 ו-j = 1.',
                  [([2], 'קודם temp מקבל את v[i], כלומר 5.', 1),
                   ([3], 'אחר כך v[i] מקבל את v[j], כלומר 3.', 2),
                   ([4], 'ובסוף v[j] מקבל את temp,\nוהרשימה היא עכשיו [3, 5].', 3)],
                  intro="עכשיו נכתוב את זה ב-Python, שורה אחרי שורה.", extra=extra)
        self.fade_all()

        # Why it works: where the two values are after every step.
        rows = [("start", A0, B0, None), ("1", A0, B0, A0), ("2", B0, B0, A0), ("3", B0, A0, A0)]
        table, cells = self.value_table(rows)
        self.say("למה זה נכון : נעקוב אחרי 5 ו-3,\nונראה איפה הם נמצאים אחרי כל שלב.",
                 FadeIn(table, lag_ratio=0.05))
        picks = [(1, 2), (1, 2), (3, 1), (2, 1)]          # a column holding 5, one holding 3
        rings = VGroup()
        for r, (c5, c3) in enumerate(picks):
            rings.add(SurroundingRectangle(cells[r][c5], color=C.AMBER, buff=0.2, corner_radius=0.1),
                      SurroundingRectangle(cells[r][c3], color=C.BLUE, buff=0.2, corner_radius=0.1))
        self.say("בכל שורה, כל אחד מהם נמצא לפחות במשתנה אחד.\nשום ערך לא הולך לאיבוד.",
                 LaggedStart(*[Create(x) for x in rings], lag_ratio=0.15), run_time=2.0)
        self.fade_all()

        chips = cost_chips(("time", "O(1)"), ("memory", "1 int"),
                           notes=("three assignments", "temp"))
        self.say("הסיבוכיות : שלוש השמות, כלומר זמן O(1),\nוזיכרון נוסף של משתנה int אחד.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: the first move lost.
        a = Cell("a", A0).move_to(LEFT * 2.6 + DOWN * 0.1)
        b = Cell("b", B0).move_to(RIGHT * 2.6 + DOWN * 0.1)
        stmt, anim = self.statement("a = b", color=C.RED)
        self.say("המלכודת : לכתוב a = b לפני ששמרנו את a.", FadeIn(a), FadeIn(b), anim)
        with self.beat("הערך 5 נמחק.\nעכשיו גם a וגם b מחזיקים 3."):
            self.play(a.value.animate.set_color(C.RED).scale(1.15), run_time=0.6)
            self.travel(b, a)
        with self.beat("ההשמה b = a כבר לא עוזרת :\nשני המשתנים מסתיימים עם 3."):
            self.play(self.statement("b = a", stmt, color=C.RED)[1], run_time=0.8)
            self.travel(a, b)
            cross = M("✗", 80, C.RED).next_to(b, RIGHT, buff=0.8)
            self.play(FadeIn(cross, scale=1.4), run_time=0.6)
        fix = M("temp = a;  a = b;  b = temp", 40, C.GREEN).move_to(DOWN * 2.2)
        self.say("לכן השמירה ב-temp חייבת לבוא\nלפני הדריסה הראשונה.", Write(fix), run_time=1.5)
        self.fade_all()

    def value_table(self, rows):
        """A table of a, b, temp per step; 5 in amber, 3 in blue."""
        heads = ["step", "a", "b", "temp"]
        widths = [2.6, 2.2, 2.2, 2.2]
        h = 1.0
        grid = VGroup()
        cells = []
        x0 = -sum(widths) / 2
        for r, row in enumerate([heads] + [list(x) for x in rows]):
            y = -r * h
            line = []
            x = x0
            for c, (val, w) in enumerate(zip(row, widths)):
                if r == 0 or c == 0:
                    mob = M(val, 34, C.MUTED)
                else:
                    text = "—" if val is None else str(val)
                    mob = M(text, 44, NUM.get(text, C.MUTED))
                mob.move_to([x + w / 2, y, 0])
                line.append(mob)
                grid.add(mob)
                x += w
            if r:
                cells.append(line)
        grid.add(Line([x0, -h / 2, 0], [x0 + sum(widths), -h / 2, 0], stroke_color=C.MUTED,
                      stroke_width=2))
        grid.move_to(ORIGIN)
        return grid, cells


class ChapterB(SwapScene):
    def construct(self):
        self.chapter_card("סעיף ב", "בלי משתנה עזר",
                          "סעיף ב : אותה החלפה, בלי אף משתנה עזר.\nמותר להשתמש בפעולות חשבון.")
        a = Cell("a", A0).move_to(LEFT * 4.0 + DOWN * 0.1)
        b = Cell("b", B0).move_to(DOWN * 0.1)
        a.value.set_color(C.AMBER)
        b.value.set_color(C.BLUE)
        temp = Cell("temp", "").move_to(RIGHT * 4.0 + DOWN * 0.1)
        strike = Line(temp.box.get_corner(DL) + DL * 0.15, temp.box.get_corner(UR) + UR * 0.15,
                      stroke_color=C.RED, stroke_width=7)
        with self.beat("אין temp. לכן הערך הראשון שנכתוב\nצריך לשמור מידע על שני הערכים."):
            self.play(FadeIn(a), FadeIn(b), FadeIn(temp), run_time=0.8)
            self.play(Create(strike), run_time=0.6)
            self.play(FadeOut(temp), FadeOut(strike), a.animate.move_to(LEFT * 3.5 + DOWN * 0.1),
                      b.animate.move_to(RIGHT * 3.5 + DOWN * 0.1), run_time=0.9)

        tc = {"5": C.AMBER, "3": C.BLUE, "8": C.GREEN}
        s = M("5 + 3 = 8", 56, t2c=tc).move_to(UP * 2.7)
        self.say("הרעיון : הסכום 8 מחזיק את שני הערכים ביחד.", Write(s), run_time=1.2)
        d = VGroup(M("8 − 3 = 5", 48, t2c=tc), M("8 − 5 = 3", 48, t2c=tc)).arrange(RIGHT, buff=1.6)
        d.move_to(DOWN * 2.15)
        self.say("כשיודעים את הסכום ואחד הערכים,\nחיסור מחזיר את השני.", FadeIn(d, shift=0.2 * UP))
        self.play(FadeOut(s), FadeOut(d), run_time=0.6)

        def sym(cell, text, old=None):
            new = X(text, 36, C.MUTED).next_to(cell.box, DOWN, buff=0.35)
            return new if old is None else Transform(old, new)

        sa, sb = sym(a, "a₀"), sym(b, "b₀")
        self.play(FadeIn(sa), FadeIn(sb), run_time=0.6)
        with self.beat("שלב 1 : a = a + b, ועכשיו a מחזיק 8,\nהסכום של שניהם."):
            stmt, anim = self.statement("a = a + b")
            self.play(anim, run_time=0.8)
            self.play(a.set_value(8, C.GREEN), sym(a, "a₀ + b₀", sa), run_time=1.0)
        with self.beat("שלב 2 : b = a − b, כלומר 8 פחות 3,\nו-b מקבל 5."):
            self.play(self.statement("b = a - b", stmt)[1], run_time=0.8)
            self.play(b.set_value(5, C.AMBER), sym(b, "(a₀ + b₀) − b₀ = a₀", sb), run_time=1.0)
        with self.beat("שלב 3 : a = a − b, כלומר 8 פחות 5,\nו-a מקבל 3. הערכים הוחלפו."):
            self.play(self.statement("a = a - b", stmt)[1], run_time=0.8)
            self.play(a.set_value(3, C.BLUE), sym(a, "(a₀ + b₀) − a₀ = b₀", sa), run_time=1.0)
        self.fade_all()
        self.box_idea('arith', 'בתיבה שבעמוד, אותן שלוש שורות,\nועמודה סימבולית שעוקבת אחרי a0 ו-b0.',
                      [
                       (1, '\u200fv[i] מקבל את הסכום, 8,\nובסימבולית a0 + b0.'),
                       (2, '\u200fv[j] מקבל את הסכום פחות b0,\nכלומר 8 − 3 = 5, שהוא a0.'),
                       (3, '\u200fv[i] מקבל את הסכום פחות a0,\nכלומר 8 − 5 = 3, שהוא b0.')])

        self.code("def swap_arith", "swap_arith", "arith",
                  [(1, "אותה חתימה כמו בסעיף א :\nרשימה v ושני אינדקסים, בלי temp."),
                   (2, "שורה 2 : v[i] נדרס בסכום של שניהם,\nוההערה רושמת a = a0 + b0."),
                   (3, "שורה 3 : הסכום פחות b0 משאיר את a0,\nוזה הערך החדש של v[j]."),
                   (4, "שורה 4 : הסכום פחות a0 משאיר את b0,\nוזה הערך החדש של v[i].")],
                  'ונריץ ליד התיבה מהעמוד,\nעל אותה דוגמה, v = [5, 3].',
                  [([2], 'קודם v[i] מקבל את הסכום, 8.', 1),
                   ([3], 'אחר כך v[j] מקבל 8 פחות 3, כלומר 5.', 2),
                   ([4], 'ובסוף v[i] מקבל 8 פחות 5, כלומר 3.', 3)],
                  intro="בקוד מהעמוד אותן שלוש שורות, על v[i] ו-v[j].", size=30, share=0.52)
        self.say("ב-Python הסכום אף פעם לא גולש,\nכי מספרים שלמים הם בגודל לא מוגבל.")
        self.fade_all()

        # Why it works: the number line, then the symbolic table.
        nl = NumberLine(x_range=[0, 9, 1], length=12, color=C.MUTED, stroke_width=3,
                        include_tip=False).move_to(UP * 0.4)
        nums = VGroup(*[M(str(k), 32, C.MUTED).next_to(nl.n2p(k), DOWN, buff=0.3) for k in range(10)])
        dots = VGroup(*[Dot(nl.n2p(k), radius=0.16, color=c) for k, c in ((3, C.BLUE), (5, C.AMBER),
                                                                       (8, C.GREEN))])
        back3 = CurvedArrow(nl.n2p(8) + UP * 0.25, nl.n2p(5) + UP * 0.25, angle=PI / 2.2,
                            color=C.AMBER, stroke_width=5)
        l3 = M("− 3", 36, C.AMBER).next_to(back3, UP, buff=0.15)
        self.say("למה זה נכון : על ציר המספרים,\nמ-8 חוזרים 3 צעדים ומגיעים ל-5.",
                 Create(nl), FadeIn(nums), FadeIn(dots), Create(back3), FadeIn(l3), run_time=1.8)
        back5 = CurvedArrow(nl.n2p(8) + DOWN * 0.9, nl.n2p(3) + DOWN * 0.9, angle=-PI / 2.4,
                            color=C.BLUE, stroke_width=5)
        l5 = M("− 5", 36, C.BLUE).next_to(back5, DOWN, buff=0.15)
        self.say("ומ-8 חוזרים 5 צעדים ומגיעים ל-3.\nשום מידע לא אבד.", Create(back5), FadeIn(l5))
        self.fade_all()

        rows = [["step", "a", "b"],
                ["start", "a₀", "b₀"],
                ["1", "a₀ + b₀", "b₀"],
                ["2", "a₀ + b₀", "(a₀ + b₀) − b₀ = a₀"],
                ["3", "(a₀ + b₀) − a₀ = b₀", "a₀"]]
        table = self.text_table(rows, [2.2, 5.0, 5.0])
        self.say("ובאופן כללי, עם a₀ ו-b₀ :\nבסוף a = b₀ ו-b = a₀, לכל שני ערכים.",
                 FadeIn(table, lag_ratio=0.05))
        self.fade_all()

        self.overflow()

        chips = cost_chips(("time", "O(1)"), ("memory", "0"), notes=("three operations", "no temp"))
        self.say("הסיבוכיות : זמן O(1), וזיכרון נוסף אפס,\nוזה כל העניין של הסעיף.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: the same variable twice.
        x = Cell("x", A0).move_to(DOWN * 0.5)
        na = M("a", 40, C.AMBER).move_to(LEFT * 3.0 + UP * 1.1)
        nb = M("b", 40, C.BLUE).move_to(RIGHT * 3.0 + UP * 1.1)
        pa = Arrow(na.get_right(), x.box.get_corner(UL), buff=0.15, color=C.AMBER, stroke_width=5)
        pb = Arrow(nb.get_left(), x.box.get_corner(UR), buff=0.15, color=C.BLUE, stroke_width=5)
        call = M("swap(x, x)", 44, C.RED).move_to(UP * 2.8)
        self.say("המלכודת : לקרוא ל-swap עם אותו משתנה פעמיים,\nלמשל swap(x, x).",
                 FadeIn(x), FadeIn(call))
        with self.beat("כאן a ו-b הם שני שמות לאותו משתנה.\nשלב 1 : x מקבל 5 + 5, כלומר 10."):
            self.play(FadeIn(na), FadeIn(nb), GrowArrow(pa), GrowArrow(pb), run_time=1.0)
            self.play(self.statement("x = x + x", call)[1], run_time=0.6)
            self.play(x.set_value(10, C.GREEN), run_time=0.8)
        with self.beat("שלב 2 : x מקבל x − x, כלומר 0.\nהערך המקורי אבד."):
            self.play(self.statement("x = x - x", call)[1], run_time=0.6)
            self.play(x.set_value(0, C.RED), run_time=0.8)
        with self.beat("שלב 3 משאיר 0.\nהגרסה עם temp לא נפגעת מזה."):
            self.play(Indicate(call, color=C.AMBER), Indicate(x.value, color=C.RED), run_time=1.0)
        guard = M("if i == j: return", 40, C.GREEN).move_to(DOWN * 2.3)
        self.say("ב-Python מגינים על הפונקציה בבדיקה :\nאם i == j, יוצאים מיד.", Write(guard))
        self.fade_all()

    def text_table(self, rows, widths, size=34, h=0.95):
        grid = VGroup()
        x0 = -sum(widths) / 2
        for r, row in enumerate(rows):
            y = -r * h
            x = x0
            for c, (val, w) in enumerate(zip(row, widths)):
                color = C.MUTED if r == 0 or c == 0 else C.WHITE
                if r and c and val.endswith(("= a₀", "= b₀")):
                    color = C.GREEN
                mob = (M if r == 0 or c == 0 else X)(val, size, color).move_to([x + w / 2, y, 0])
                grid.add(mob)
                x += w
        grid.add(Line([x0, -h / 2, 0], [x0 + sum(widths), -h / 2, 0], stroke_color=C.MUTED,
                      stroke_width=2))
        return grid.move_to(ORIGIN)

    def overflow(self):
        """The 32-bit wheel (not to scale): 0 at the top, the seam at the bottom."""
        center = LEFT * 3.3 + UP * 0.55
        R = 2.3
        wheel = Circle(radius=R, color=C.MUTED, stroke_width=3).move_to(center)

        def at(deg, r=R):
            return center + r * np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])

        POS = {"0": 90, "1": 72, "max": -72, "min": -108}
        ticks = VGroup(*[Line(at(d, R - 0.14), at(d, R + 0.14), color=C.MUTED, stroke_width=3)
                         for d in POS.values()])
        labels = VGroup(X("0", 32, C.MUTED).move_to(at(90, R + 0.45)),
                        X("1", 32, C.MUTED).move_to(at(72, R + 0.45)),
                        X("2³¹ − 1", 32, C.MUTED).move_to(at(-72, R + 0.45) + RIGHT * 0.75),
                        X("−2³¹", 32, C.MUTED).move_to(at(-108, R + 0.45) + LEFT * 0.5))
        plus = X("+", 44, C.MUTED).move_to(at(5, R - 0.6))
        minus = X("−", 44, C.MUTED).move_to(at(175, R - 0.6))
        seam = Line(at(-90, R - 0.4), at(-90, R + 0.4), color=C.AMBER, stroke_width=7)
        self.say("ומה עם גלישה? ב-SystemVerilog, int הוא 32 ביט,\nוהחשבון הוא מודולו 2³².",
                 Create(wheel), FadeIn(ticks), FadeIn(labels), FadeIn(plus), FadeIn(minus))
        self.say("הערכים יושבים על גלגל :\nאחרי 2³¹ − 1 בא מיד −2³¹.", Create(seam),
                 Flash(at(-90), color=C.AMBER, line_length=0.35))

        right = RIGHT * 3.6
        rows = VGroup(X("a = 2³¹ − 1", 44, C.AMBER), X("b = 1", 44, C.BLUE))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(right + UP * 0.6)
        da = Dot(at(POS["max"]), radius=0.16, color=C.AMBER)
        db = Dot(at(POS["1"]), radius=0.16, color=C.BLUE)
        la = M("a", 32, C.AMBER).move_to(at(POS["max"], R * 0.8))
        lb = M("b", 32, C.BLUE).move_to(at(POS["1"], R * 0.8))

        def turn(dot, label, frm, to):
            """The dot along the wheel and its name along an inner circle (no updaters, so
            every still is a frozen frame)."""
            def arc(r):
                return Arc(radius=r, start_angle=np.radians(frm), angle=np.radians(to - frm),
                           arc_center=center)
            return MoveAlongPath(dot, arc(R)), MoveAlongPath(label, arc(R * 0.8))

        def row(i, text, color):
            return Transform(rows[i], X(text, 44, color).move_to(rows[i], aligned_edge=LEFT))

        stmt = M("a = a + b", 44, C.AMBER).move_to(right + UP * 2.8)
        with self.beat("נניח a = 2³¹ − 1 ו-b = 1.\nהסכום עובר את התפר ונעטף אל −2³¹."):
            self.play(FadeIn(da), FadeIn(db), FadeIn(la), FadeIn(lb), FadeIn(rows), run_time=0.8)
            self.play(FadeIn(stmt), run_time=0.5)
            self.play(*turn(da, la, POS["max"], POS["min"]), row(0, "a = −2³¹", C.AMBER), run_time=1.4)
        with self.beat("שלב 2 : החיסור מסובב את הגלגל אחורה,\nו-b מקבל 2³¹ − 1."):
            self.play(Transform(stmt, M("b = a - b", 44, C.AMBER).move_to(stmt)), run_time=0.5)
            self.play(FadeOut(db), FadeOut(lb), run_time=0.4)
            db.move_to(at(POS["min"]))
            lb.move_to(at(POS["min"], R * 0.8))
            self.play(FadeIn(db), FadeIn(lb), run_time=0.4)
            self.play(*turn(db, lb, POS["min"], POS["max"]), row(1, "b = 2³¹ − 1", C.BLUE), run_time=1.2)
        with self.beat("שלב 3 : a מקבל 1.\nההחלפה נכונה, למרות שהסכום גלש."):
            self.play(Transform(stmt, M("a = a - b", 44, C.AMBER).move_to(stmt)), run_time=0.5)
            self.play(*turn(da, la, POS["min"] + 360, POS["1"] + 360), row(0, "a = 1", C.AMBER),
                      run_time=1.6)
            ok = M("✓", 56, C.GREEN).next_to(rows, RIGHT, buff=0.5)
            self.play(FadeIn(ok), run_time=0.4)
        ident = VGroup(X("((a₀ + b₀) − b₀) mod 2³²", 34, C.GREEN), X("= a₀ mod 2³²", 34, C.GREEN))
        ident.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(right + DOWN * 1.6)
        self.say("כל השוויונים נכונים גם מודולו 2³²,\nולכן הגלישה לא מזיקה.", Write(ident))
        self.fade_all()


class ChapterC(SwapScene):
    SQ = 1.15

    def bit_row(self, name, value, y, color):
        squares = VGroup(*[RoundedRectangle(width=self.SQ, height=self.SQ, corner_radius=0.12,
                                            stroke_color=C.MUTED, stroke_width=2.5,
                                            fill_color=C.NAVY_LIGHT, fill_opacity=1)
                           for _ in range(4)]).arrange(RIGHT, buff=0.18)
        squares.move_to([0, y, 0])
        digits = VGroup(*[M(ch, 52).move_to(sq) for ch, sq in zip(bits(value), squares)])
        label = M(name, 52, color).next_to(squares, LEFT, buff=0.7)
        dec = M(f"= {value}", 52, color).next_to(squares, RIGHT, buff=0.7)
        return VGroup(label, squares, digits, dec)

    def set_bits(self, row, value, color):
        """Animations: the bits that change flip (in amber), the decimal value updates."""
        anims = []
        for k, ch in enumerate(bits(value)):
            old = row[2][k]
            if old.text != ch:
                anims.append(Transform(old, M(ch, 52, C.AMBER).move_to(row[1][k])))
                old.text = ch
        anims.append(Transform(row[3], M(f"= {value}", 52, color).next_to(row[1], RIGHT, buff=0.7)))
        return anims

    def columns(self, row_a, row_b, mask_row):
        """Amber bands behind the columns where `mask_row` has a 1."""
        bands = VGroup()
        for k in range(4):
            if mask_row[2][k].text == "1":
                top = row_a[1][k].get_top()[1] + 0.15
                bot = row_b[1][k].get_bottom()[1] - 0.15
                bands.add(Rectangle(width=self.SQ + 0.12, height=top - bot, stroke_width=0,
                                    fill_color=C.AMBER, fill_opacity=0.25)
                          .move_to([row_a[1][k].get_x(), (top + bot) / 2, 0]))
        return bands

    def table2(self, op, fn, title_color=C.WHITE, size=44, cell=1.05):
        """The 2×2 table of `op`: rows a = 0, 1; columns b = 0, 1."""
        g = VGroup()
        cells = {}
        for bi in (0, 1):
            g.add(M(f"b={bi}", 26, C.MUTED).move_to([(bi + 1) * cell, 0, 0]))
        for ai in (0, 1):
            g.add(M(f"a={ai}", 26, C.MUTED).move_to([-0.1, -(ai + 1) * cell, 0]))
            for bi in (0, 1):
                box = Square(cell * 0.92, stroke_color=C.FAINT, stroke_width=2, fill_color=C.NAVY_LIGHT,
                             fill_opacity=1).move_to([(bi + 1) * cell, -(ai + 1) * cell, 0])
                cells[(ai, bi)] = VGroup(box, M(str(fn(ai, bi)), size).move_to(box))
                g.add(cells[(ai, bi)])
        g.add(M(op, 52, title_color).move_to([-0.1, 0.05, 0]))
        return g, cells

    def construct(self):
        self.chapter_card("סעיף ג", "רק אופרטורים על ביטים",
                          "סעיף ג : בלי משתנה עזר ובלי חשבון.\nמותר רק &, |, ^ ו-~.")
        ra = self.bit_row("a", A0, 0.65, C.AMBER)
        rb = self.bit_row("b", B0, -0.75, C.BLUE)
        weights = VGroup(*[M(w, 26, C.MUTED).next_to(sq, UP, buff=0.18) for w, sq in zip("8421", ra[1])])
        self.say("נכתוב את שני הערכים בביטים :\nהערך 5 הוא 0101, והערך 3 הוא 0011.",
                 FadeIn(ra), FadeIn(rb), FadeIn(weights))
        pic = VGroup(ra, rb, weights)
        xor, xcells = self.table2("^", lambda x, y: x ^ y, C.AMBER)
        xor.move_to(RIGHT * 3.9 + UP * 0.5)
        for k, c in xcells.items():
            if k[0] != k[1]:
                c[1].set_color(C.AMBER)
        self.say("הרעיון : XOR, שנותן 1 בדיוק כשהביטים שונים.",
                 pic.animate.scale(0.8).move_to(LEFT * 2.9 + UP * 0.2), FadeIn(xor))
        rules = VGroup(M("x ^ x = 0", 40), M("x ^ 0 = x", 40)).arrange(DOWN, buff=0.3)
        rules.next_to(xor, DOWN, buff=0.6)
        self.say("לכן x ^ x = 0 ו-x ^ 0 = x.\nכך XOR הוא גם החיבור וגם החיסור של סעיף ב.",
                 FadeIn(rules, shift=0.2 * UP))
        self.play(FadeOut(xor), FadeOut(rules), pic.animate.scale(1.25).move_to(DOWN * 0.2), run_time=1.0)

        def step(text, stmt_text, target, mask, value, color, old_stmt):
            with self.beat(text):
                stmt, anim = self.statement(stmt_text, old_stmt)
                self.play(anim, run_time=0.6)
                bands = self.columns(ra, rb, mask)
                self.play(FadeIn(bands), run_time=0.6)
                self.play(*self.set_bits(target, value, color), run_time=1.0)
                self.play(FadeOut(bands), run_time=0.5)
            return stmt

        stmt = step("שלב 1 : a = a ^ b. הביט של a מתהפך\nבכל עמודה שבה ב-b יש 1.", "a = a ^ b", ra, rb,
                    A0 ^ B0, C.AMBER, None)
        diff = VGroup(*[SurroundingRectangle(VGroup(ra[1][k], rb[1][k]), color=C.GREEN, buff=0.1)
                        for k in range(4) if bits(A0)[k] != bits(B0)[k]])
        self.say("עכשיו a הוא 0110, כלומר 6 :\nהוא מסמן את העמודות שבהן 5 ו-3 שונים.",
                 *[Create(d) for d in diff], *[r.animate.set_color(C.WHITE) for r in ra[2]])
        self.play(FadeOut(diff), run_time=0.5)
        step("שלב 2 : b = a ^ b, ו-b מתהפך היכן ש-a הוא 1.\nיוצא 0101, כלומר 5.", "b = a ^ b", rb, ra,
             A0, C.BLUE, stmt)
        self.play(*[r.animate.set_color(C.WHITE) for r in rb[2]], run_time=0.4)
        step("שלב 3 : a = a ^ b, ו-a מתהפך היכן ש-b הוא 1.\nיוצא 0011, כלומר 3.", "a = a ^ b", ra, rb,
             B0, C.AMBER, stmt)
        self.fade_all()
        self.box_idea('xor', 'והתיבה שבעמוד, הפעם עם XOR\xa0:\nאותן שלוש שורות, עם ^.',
                      [
                       (1, '\u200fv[i] מקבל 5 ^ 3, כלומר 6,\nובסימבולית a0 ^ b0.'),
                       (2, '\u200fv[j] מקבל 6 ^ 3, כלומר 5\xa0:\nה-b0 מתבטל ונשאר a0.'),
                       (3, '\u200fv[i] מקבל 6 ^ 5, כלומר 3\xa0:\nה-a0 מתבטל ונשאר b0.')])

        self.code("def swap_xor", "swap_xor", "xor",
                  [(1, "שוב אותה חתימה : רשימה v ושני אינדקסים."),
                   (2, "שורה 2 : v[i] מקבל a0 ^ b0,\nהעמודות שבהן שני הערכים שונים."),
                   (3, "שורה 3 : XOR עם b0 מבטל אותו,\nונשאר a0, הערך החדש של v[j]."),
                   (4, "שורה 4 : XOR עם a0 מבטל אותו,\nונשאר b0, הערך החדש של v[i].")],
                  'ועכשיו הריצה על 5 ו-3,\nלצד התיבה מהעמוד.',
                  [([2], 'קודם v[i] מקבל 5 ^ 3, כלומר 6.', 1),
                   ([3], 'אחר כך v[j] מקבל 6 ^ 3, כלומר 5.', 2),
                   ([4], 'ובסוף v[i] מקבל 6 ^ 5, כלומר 3.', 3)],
                  intro="הקוד מהעמוד : אותן שלוש שורות,\nעם ^ במקום + ו-−.", size=30, share=0.52)
        self.fade_all()

        # Why it works: one bit column, all four cases.
        heads = ["a₀", "b₀", "1 · a", "2 · b", "3 · a"]
        subs = ["", "", "a₀ ^ b₀", "a ^ b₀", "a ^ b"]
        widths = [1.8, 1.8, 2.7, 2.7, 2.7]
        x0 = -sum(widths) / 2
        h = 0.78
        top = 3.1
        xs = []
        x = x0
        for w in widths:
            xs.append(x + w / 2)
            x += w
        head = VGroup(*[X(t, 36, C.MUTED).move_to([xs[c], top, 0]) for c, t in enumerate(heads)])
        sub = VGroup(*[X(t, 26, C.MUTED).move_to([xs[c], top - 0.48, 0]) for c, t in enumerate(subs) if t])
        rule = Line([x0, top - 0.8, 0], [x0 + sum(widths), top - 0.8, 0], stroke_color=C.MUTED,
                    stroke_width=2)
        self.say("למה זה נכון : XOR פועל על כל עמודה לבד,\nבלי נשא, אז מספיק לבדוק ביט אחד.",
                 FadeIn(head), FadeIn(sub), Create(rule))
        body = VGroup()
        cols = [VGroup() for _ in heads]
        for r, (x_, y_) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            s1 = x_ ^ y_
            s2 = s1 ^ y_
            s3 = s1 ^ s2
            for c, v in enumerate((x_, y_, s1, s2, s3)):
                m = M(str(v), 40).move_to([xs[c], top - 1.35 - r * h, 0])
                cols[c].add(m)
                body.add(m)
        self.say("יש רק ארבעה צירופים של a₀ ו-b₀.\nנריץ על כל אחד את שלושת השלבים.",
                 LaggedStart(*[FadeIn(m) for m in body], lag_ratio=0.06), run_time=2.0)
        g1 = VGroup(SurroundingRectangle(cols[0], color=C.GREEN, buff=0.15),
                    SurroundingRectangle(cols[3], color=C.GREEN, buff=0.15))
        g2 = VGroup(SurroundingRectangle(cols[1], color=C.BLUE, buff=0.15),
                    SurroundingRectangle(cols[4], color=C.BLUE, buff=0.15))
        self.say("בכל הארבעה, שלב 2 מחזיר את a₀,\nושלב 3 מחזיר את b₀.", Create(g1), Create(g2))
        alg = X("(a₀ ^ b₀) ^ b₀  =  a₀ ^ (b₀ ^ b₀)  =  a₀ ^ 0  =  a₀", 36, C.GREEN).move_to(DOWN * 2.25)
        self.say("ובאלגברה : b₀ ^ b₀ מתבטל ל-0, ונשאר a₀.", Write(alg))
        self.fade_all()

        chips = cost_chips(("time", "O(1)"), ("memory", "0"), notes=("three XORs", "no temp"))
        self.say("הסיבוכיות : זמן O(1) וזיכרון אפס,\nבלי נשא ובלי גלישה.", FadeIn(chips, lag_ratio=0.3))
        chain = VGroup(M("a = a ^ b", 34), M("→", 34, C.MUTED), M("b = a ^ b", 34), M("→", 34, C.MUTED),
                       M("a = a ^ b", 34)).arrange(RIGHT, buff=0.3).move_to(DOWN * 2.2)
        self.say("שלוש הפעולות תלויות זו בזו, ולכן רצות בטור.\nזה טריק, לא אופטימיזציה.",
                 chips.animate.shift(UP * 0.8), FadeIn(chain, lag_ratio=0.3))
        self.fade_all()

        # The traps.
        rx = self.bit_row("x", A0, -0.2, C.AMBER)
        stmt, anim = self.statement("x = x ^ x", color=C.RED)
        with self.beat("מלכודת ראשונה : שוב אותו משתנה.\nכי x ^ x הוא 0, והערך נמחק כבר בשלב 1."):
            self.play(FadeIn(rx), anim, run_time=0.8)
            self.play(*self.set_bits(rx, 0, C.RED), run_time=1.0)
            self.play(*[d.animate.set_color(C.RED) for d in rx[2]], run_time=0.4)
        self.play(FadeOut(rx), FadeOut(stmt), run_time=0.6)

        t_and, c_and = self.table2("&", lambda x, y: x & y)
        t_or, c_or = self.table2("|", lambda x, y: x | y)
        t_xor, c_xor = self.table2("^", lambda x, y: x ^ y, C.AMBER)
        tables = VGroup(t_and, t_or, t_xor).arrange(RIGHT, buff=1.3).move_to(UP * 0.1)
        self.say("מלכודת שנייה : למה לא & או |?\nכי הם מאבדים מידע.", FadeIn(tables, lag_ratio=0.2))
        ring_and = SurroundingRectangle(VGroup(c_and[(0, 0)], c_and[(1, 0)]), color=C.RED, buff=0.1)
        self.say("בעמודה שבה b הוא 0, a & b יוצא 0\nגם כש-a היה 0 וגם כש-a היה 1.", Create(ring_and),
                 *[c_and[k][1].animate.set_color(C.RED) for k in ((0, 0), (1, 0))])
        ring_or = SurroundingRectangle(VGroup(c_or[(0, 1)], c_or[(1, 1)]), color=C.RED, buff=0.1)
        self.say("ב-| אותו דבר כש-b הוא 1.\nאחרי זה כבר אי אפשר לשחזר את a.", Create(ring_or),
                 *[c_or[k][1].animate.set_color(C.RED) for k in ((0, 1), (1, 1))])
        ring_xor = VGroup(*[SurroundingRectangle(VGroup(c_xor[(0, b)], c_xor[(1, b)]), color=C.GREEN,
                                                 buff=0.1) for b in (0, 1)])
        self.say("רק ב-XOR, כש-b ידוע,\nאפשר תמיד לשחזר את a.", Create(ring_xor))
        self.fade_all()


class Closing(SwapScene):
    def construct(self):
        self.closing(QID, [("א", M("temp = a;  a = b;  b = temp", 34)),
                           ("ב", M("a = a + b;  b = a - b;  a = a - b", 34)),
                           ("ג", M("a = a ^ b;  b = a ^ b;  a = a ^ b", 34))],
                     ["לסיכום : משתנה עזר, סכום וחיסור,\nאו שלוש פעולות XOR.",
                      "נסו את שלוש הגרסאות בתיבה\nשבעמוד של שאלה 0002 באתר."])
