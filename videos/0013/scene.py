"""The tutorial video of question 0013, sort four digits and subtract (script: script.md).

Render with `python videos/render.py 0013` (see VIDEOS.md). The owner's choices
(2026-11-02): one sentence linking to video 0012 (three digits, 495), the video standing on
its own; part א with the page's code typed and run with its trace on 6174 and on 3524 (not
special), beside the page's column subtraction; part ב the proof through the grid of the
pairs (p, q): the difference is 999p + 90q, a grid of the 54 pairs with p >= 1 checked one by
one, only (6, 2) = 6174 returns to itself, why (the digits of the difference and the cases),
`find_special_4` typed and its run jumping 0, 6174, end, and the site's pairs box following
the arrows from (9, 5) to 6174, then the histogram; part ג short: the formula in base B, the
family B = 5k with its digits, the two exceptions, existence is not convergence (base 15),
and the site's base box.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 13
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – לבדוק מספר אחד"),
    ("ChapterB", "סעיף ב – לבדוק את כל המספרים"),
    ("ChapterC", "סעיף ג – ארבע ספרות בבסיס B"),
    ("Closing", "סיכום"),
]

# The page's boxes. Box 0 (kappairs, from (9, 5)): "pairs" the grid and its text, then the
# arrow followed six times to (6, 2) = 6174. Box 1 (kaprekar, four digits): "cols_n" the
# column subtraction of 3524, 440 CSS px wide for beside the code; "hist"
# the histogram over all 10,000 numbers. Box 2 (kap4base, base 15, 1234): "base" the
# summary, the step line and the map of the pairs; to the end (a cycle of four), then base
# 10 (the same digits, 1234) and to the end (6174).
BOXES = {
    "pairs": {"box": 0, "region": [":scope > .ex-controls", ".kpp-grid", ".kpp-text"],
              "hide": [".ex-title", ".viz-legend"],
              "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 6}]},
    "cols_n": {"box": 1, "width": 440, "region": [".kp-cols"],
               "hide": [".kp-table", ".kp-chain"],
               "steps": [[]]},
    "hist": {"box": 1, "region": [".kp-chart", ".kp-sum"], "hide": [".ex-title"], "steps": [[]]},
    "base": {"box": 2, "region": [".k4-sum", ".k4-map"],
             "hide": [".k4-table", ".ex-fold", ".viz-legend", ".ex-title", ".k4-step"],
             "steps": [[], [["click", ".ex-end"]], [["set", ".k4-b", "10"]], [["click", ".ex-end"]]]},
}


# The reference, independent of the page code.
def step(x: int) -> tuple[int, int, int]:
    """(largest, smallest, difference) of x written with four digits."""
    ds = sorted(f"{x:04d}")
    lo, hi = int("".join(ds)), int("".join(reversed(ds)))
    return hi, lo, hi - lo


def pair(x: int) -> tuple[int, int]:
    """(p, q) of x: the largest digit minus the smallest, the two middle ones' distance."""
    d = sorted((int(c) for c in f"{x:04d}"), reverse=True)
    return d[0] - d[3], d[1] - d[2]


def chain(x: int) -> list[int]:
    out = [x]
    while step(out[-1])[2] != out[-1]:
        out.append(step(out[-1])[2])
    return out


SPECIAL = [x for x in range(10000) if step(x)[2] == x]
assert SPECIAL == [0, 6174]
assert step(3524) == (5432, 2345, 3087) and step(95) == (9500, 59, 9441) and step(6174) == (7641, 1467, 6174)
CHAIN_3524 = [3524, 3087, 8352, 6174]
assert chain(3524) == CHAIN_3524 and step(7777)[2] == 0 and step(0)[2] == 0
PAIRS = [(p, q) for p in range(1, 10) for q in range(p + 1)]
assert len(PAIRS) == 54
for p, q in PAIRS:     # the difference depends only on (p, q): 999p + 90q, digits by step 3
    v = 999 * p + 90 * q
    want = [p, q - 1, 9 - q, 10 - p] if q >= 1 else [p - 1, 9, 9, 10 - p]
    assert [int(c) for c in f"{v:04d}"] == want
FIXED = [(p, q) for p, q in PAIRS if step(999 * p + 90 * q)[2] == 999 * p + 90 * q]
assert FIXED == [(6, 2)] and 999 * 6 + 90 * 2 == 6174
assert pair(9441) == (8, 0)
PATH = [9441, 7992, 7173, 6354, 3087, 8352, 6174]          # the pairs box from (9, 5)
assert chain(999 * 9 + 90 * 5) == PATH
assert [pair(x) for x in PATH] == [(8, 0), (7, 2), (6, 4), (3, 1), (8, 4), (6, 2), (6, 2)]
STEPS = {x: len(chain(x)) - 1 for x in range(10000) if pair(x)[0] > 0}
assert len(STEPS) == 9990 and max(STEPS.values()) == 7


# Base B (part ג).
DIG = "0123456789ABCDEF"


def b_digits(x: int, B: int) -> list[int]:
    return [x // B ** 3, x // B ** 2 % B, x // B % B, x % B]


def b_text(x: int, B: int) -> str:
    return "".join(DIG[v] for v in b_digits(x, B))


def b_step(x: int, B: int) -> int:
    a, b, c, d = sorted(b_digits(x, B), reverse=True)
    return (a * B ** 3 + b * B ** 2 + c * B + d) - (d * B ** 3 + c * B ** 2 + b * B + a)


def b_fixed(B: int) -> list[int]:
    return [x for x in range(B ** 4) if len(set(b_digits(x, B))) > 1 and b_step(x, B) == x]


FAMILY = {B: b_fixed(B) for B in range(2, 17)}
assert [B for B in FAMILY if FAMILY[B]] == [2, 4, 5, 10, 15]
assert [b_text(x, 2) for x in FAMILY[2]] == ["0111", "1001"] and [b_text(x, 4) for x in FAMILY[4]] == ["3021"]
for k, B in ((1, 5), (2, 10), (3, 15)):
    (x,) = FAMILY[B]
    assert b_digits(x, B) == [3 * k, k - 1, 4 * k - 1, 2 * k]
    assert x == B * (B - 1) * (3 * B * B + 4 * B + 3) // 5
assert [b_text(FAMILY[B][0], B) for B in (5, 10, 15)] == ["3032", "6174", "92B6"]
X15 = 1 * 15 ** 3 + 2 * 15 ** 2 + 3 * 15 + 4
ORBIT15 = [X15]
for _ in range(5):
    ORBIT15.append(b_step(ORBIT15[-1], 15))
assert [b_text(x, 15) for x in ORBIT15] == ["1234", "30DC", "D852", "B2B4", "9676", "30DC"]


class Digits(VGroup):
    """A four-digit number as a row of cells, centred on `centre`."""

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
    """Helpers shared by the chapters of 0013."""

    def sort_demo(self, s: str, y: float = 1.7):
        """The number's cells, then sorted ascending (the smallest), left; returns
        (x row, small row, large row), the large row not shown yet."""
        top = Digits(s, UP * y)
        name = M("x", 40, C.MUTED).next_to(top, LEFT, buff=0.5)
        self.play(FadeIn(name), FadeIn(top, lag_ratio=0.15), run_time=0.9)
        order = sorted(range(len(s)), key=lambda i: s[i])
        small = top.copy()
        target = VGroup(*[small.cells[i].copy() for i in order]).arrange(RIGHT, buff=0.12)
        target.move_to([-3.0, y - 1.9, 0])
        self.play(*[small.cells[i].animate.move_to(target[k]) for k, i in enumerate(order)], run_time=1.1)
        large = VGroup(*[small.cells[i].copy() for i in reversed(order)])
        large.arrange(RIGHT, buff=0.12).move_to([3.0, y - 1.9, 0])
        return VGroup(name, top), small, large


class Opening(KScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "ממיינים ספרות ומחסרים – ארבע ספרות",
                     ["א · לבדוק מספר אחד", "ב · לבדוק את כל המספרים", "ג · ארבע ספרות בבסיס B"],
                     ["שאלה 0013 : ממיינים ספרות ומחסרים,\nהפעם עם ארבע ספרות. רמת ג'וניור.",
                      "שלושה סעיפים : לבדוק מספר אחד,\nלבדוק את כל המספרים, ובסיס B."])
        self.say("בסרטון של שאלה 0012, עם שלוש ספרות,\nקיבלנו 495. עכשיו ארבע ספרות.")
        self.fade_all()
        top = Digits("3524", UP * 1.7)
        name = M("x", 40, C.MUTED).next_to(top, LEFT, buff=0.5)
        self.say("לוקחים מספר בין 0 ל-9999, למשל 3524,\nוכותבים אותו בארבע ספרות.",
                 FadeIn(name), FadeIn(top, lag_ratio=0.15))
        desc = Digits("5432", [3.0, -0.2, 0], side=0.8)
        asc = Digits("2345", [-3.0, -0.2, 0], side=0.8)
        dl = M("desc", 32, C.MUTED).next_to(desc, UP, buff=0.25)
        al = M("asc", 32, C.MUTED).next_to(asc, UP, buff=0.25)
        self.say("ממיינים את הספרות מהגדול לקטן, 5432,\nומהקטן לגדול, 2345.",
                 FadeIn(desc, shift=0.2 * DOWN), FadeIn(asc, shift=0.2 * DOWN), FadeIn(dl), FadeIn(al))
        diff = M("5432 − 2345 = 3087", 44).move_to(DOWN * 1.6 + LEFT * 0.8)
        self.say("מחסרים את הקטן מהגדול,\nומקבלים 3087.", FadeIn(diff, shift=0.2 * UP))
        rule = M("3087 = x ?", 40, C.AMBER).next_to(diff, RIGHT, buff=0.7)
        self.say("אם ההפרש שווה למספר עצמו,\nהמספר נקרא מיוחד.", FadeIn(rule))
        no = mark(False, rule.get_right() + RIGHT * 0.5)
        self.say("כאן 3087 שונה מ-3524,\nולכן 3524 לא מיוחד.", FadeIn(no, scale=1.4))
        self.fade_all()


class ChapterA(KScene):
    def construct(self):
        self.chapter_card("סעיף א", "לבדוק מספר אחד",
                          "סעיף א : פונקציה שמקבלת מספר x,\nומחזירה 1 אם הוא מיוחד, ו-0 אחרת.")

        # The idea: one sort, read both ways.
        with self.beat("הרעיון : שני המספרים בנויים\nמאותן ארבע ספרות."):
            x_row, small, large = self.sort_demo("3524")
        sl = M("smallest = 2345", 34, C.GREEN).next_to(small, DOWN, buff=0.35)
        self.say("ממיינים פעם אחת בסדר עולה :\nזה המספר הקטן, 2345.", FadeIn(sl))
        arrow = Arrow(small.get_right(), large.get_left(), buff=0.25, color=C.AMBER, stroke_width=5)
        rev = M("reversed", 30, C.AMBER).next_to(arrow, UP, buff=0.12)
        ll = M("largest = 5432", 34, C.GREEN).next_to(large, DOWN, buff=0.35)
        self.say("אותן ספרות בסדר הפוך הן הגדול,\n‏5432. אין צורך במיון שני.",
                 GrowArrow(arrow), FadeIn(rev), FadeIn(large, shift=0.2 * RIGHT), FadeIn(ll))
        self.fade_all()

        # The code: typed, then traced on 3524 and on 6174 beside the box.
        code = page_python(QID, "def is_special_4")
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True)

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            return "[" + ", ".join(repr(c) for c in v) + "]" if n == "digits" else str(v)

        vp = VarPanel(["x", "digits", "smallest", "largest"], fmt=fmt, size=26, cols=2,
                      slot=4.6).set_state({})
        self.place_code(panel, vp_width=9.4)
        self.type_code(panel, [
            (1, "הפונקציה is_special_4 מקבלת את x,\nומחזירה 1 או 0."),
            (2, ["הפורמט 04d כותב את x בארבע ספרות,\nעם אפסים משמאל : 95 הופך ל-0095.",
                 "‏sorted ממיינת את ארבעת התווים\nבסדר עולה, לרשימה."]),
            (3, "החיבור של התווים בסדר עולה\nנותן את המספר הקטן."),
            (4, "אותם תווים בסדר הפוך נותנים\nאת הגדול, בלי מיון שני."),
            (5, "בסוף משווים את ההפרש ל-x,\nומחזירים 1 או 0."),
        ], intro="עכשיו נכתוב את זה ב-Python : כמעט\nאותו קוד כמו בשלוש ספרות.")

        steps, result = trace(code, "is_special_4", (3524,))
        assert result == 0 and [s.line for s in steps] == [2, 3, 4, 5]
        view = BoxView(QID, "cols_n")
        with self.beat("נריץ את הקוד על 3524,\nלצד החיסור במאונך מהתיבה שבעמוד."):
            self.split(panel, view, vp)
        self.run_code(panel, vp, steps, [
            ([2], "‏x = 3524 : הספרות בסדר עולה\nהן 2, 3, 4 ו-5.", None),
            ([3], "המספר הקטן הוא 2345.", None),
            ([4], "והגדול הוא 5432.", None),
            ([5], "‏5432 פחות 2345 הם 3087, לא 3524 :\nהפונקציה מחזירה 0.", None),
        ], view=view)

        self.fade_all()

        # The step again and again: 3524 reaches 6174, where the function returns 1.
        nums = [Digits(f"{x:04d}", side=0.55) for x in CHAIN_3524]
        row = VGroup(*nums).arrange(RIGHT, buff=0.9).move_to(UP * 1.4)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.12, color=C.AMBER, stroke_width=4)
                          for a, b in zip(nums, nums[1:])])
        self.say("ומה אם מפעילים את אותו צעד שוב ושוב,\nכל פעם על ההפרש?", FadeIn(nums[0]))
        with self.beat("‏3524 נותן 3087, ‏3087 נותן 8352,\nו-8352 נותן 6174."):
            for k in range(3):
                self.play(GrowArrow(arrows[k]), FadeIn(nums[k + 1], shift=0.2 * RIGHT), run_time=0.8)
        fix = M("7641 − 1467 = 6174", 40, C.GREEN).next_to(row, DOWN, buff=0.8)
        ok = mark(True, fix.get_right() + RIGHT * 0.5)
        ret = M("is_special_4(6174) = 1", 34, C.MUTED).next_to(fix, DOWN, buff=0.45)
        self.say("ושם הוא נעצר : 7641 פחות 1467 הם\n‏6174 בדיוק. על 6174 הפונקציה מחזירה 1.",
                 FadeIn(fix), FadeIn(ok, scale=1.4), FadeIn(ret))
        self.fade_all()

        # The traps: all digits equal, and the zeros on the left.
        same = VGroup(M("7777:", 40, C.MUTED), M("7777 − 7777 = 0", 44, C.RED)).arrange(RIGHT, buff=0.5)
        zero = VGroup(M("0:", 40, C.MUTED), M("0000 − 0000 = 0", 44, C.GREEN)).arrange(RIGHT, buff=0.5)
        VGroup(same, zero).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(UP * 0.9)
        self.say("מלכודת ראשונה : כל הספרות שוות, כמו\n‏7777. ההפרש 0, ולכן 7777 לא מיוחד.",
                 FadeIn(same, shift=0.2 * RIGHT))
        self.say("אבל 0 עצמו כן מיוחד : 0000 פחות 0000\nהם 0, בדיוק המספר. כך גם בטבלה שבעמוד.",
                 FadeIn(zero, shift=0.2 * RIGHT))
        self.fade_all()
        bad = VGroup(M("\"95\":", 40, C.MUTED), M("95 − 59 = 36", 44, C.RED)).arrange(RIGHT, buff=0.5)
        good = VGroup(M("\"0095\":", 40, C.MUTED), M("9500 − 0059 = 9441", 44, C.GREEN)).arrange(RIGHT, buff=0.5)
        VGroup(bad, good).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(UP * 0.9)
        self.say("מלכודת שנייה : מספר קצר. בלי אפסים\nמשמאל, 95 נותן 95 פחות 59, כלומר 36.",
                 FadeIn(bad, shift=0.2 * RIGHT))
        self.say("עם ריפוד לארבע ספרות זה 0095 :\n‏9500 פחות 0059, כלומר 9441.",
                 FadeIn(good, shift=0.2 * RIGHT))
        self.fade_all()

        chips = cost_chips(("time", "$O(1)$"), ("memory", "$O(1)$"),
                           notes=("always 4 digits", "4 digits, 2 numbers"))
        self.say("הסיבוכיות : תמיד ארבע ספרות,\nולכן זמן O(1) וזיכרון O(1).",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterB(KScene):
    def construct(self):
        self.chapter_card("סעיף ב", "לבדוק את כל המספרים",
                          "סעיף ב : מריצים את הפונקציה על 0 עד 9999.\nאילו מספרים מיוחדים, ולמה?")

        # The difference is 999p + 90q.
        abcd = TX(r"a \ge b \ge c \ge d", size=44, color=C.AMBER).move_to(UP * 2.4)
        self.say("נסמן את הספרות הממוינות,\nמהגדולה a עד הקטנה d.", FadeIn(abcd))
        diff = TX(r"(1000a + 100b + 10c + d)", r"-", r"(1000d + 100c + 10b + a)", size=38).move_to(UP * 1.2)
        self.say("הגדול פחות הקטן : אותן ספרות,\nפעם בסדר אחד ופעם בסדר ההפוך.", FadeIn(diff))
        res = TX(r"= 999\,(a - d) + 90\,(b - c)", size=42).next_to(diff, DOWN, buff=0.5)
        self.say("הפעם ספרות האמצע לא מתבטלות,\nאבל הכול מתקבץ לשני הפרשים.", FadeIn(res))
        pq = TX(r"p = a - d,\quad q = b - c", r"\quad\Rightarrow\quad 999p + 90q", size=42)
        pq[1].set_color(C.AMBER)
        pq.next_to(res, DOWN, buff=0.5)
        self.say("‏p הוא המרחק בין הגדולה לקטנה,\nו-q המרחק בין שתי האמצעיות.", FadeIn(pq[0]))
        self.say("ההפרש הוא 999p ועוד 90q :\nהוא תלוי רק בזוג p, q.", FadeIn(pq[1]))
        rng = TX(r"0 \le q \le p \le 9 \;\Rightarrow\; 55 \text{ pairs}", size=40, color=C.MUTED)
        rng.next_to(pq, DOWN, buff=0.5)
        self.say("כי b ו-c בין a ל-d, מתקיים q ≤ p ≤ 9 :\nיש רק 55 זוגות, ולכן 55 הפרשים.", FadeIn(rng))
        self.fade_all()

        # The grid of the 54 pairs with p >= 1 (the 55th, p = 0, is 0): each cell the
        # difference of its pair, then a mark: do the difference's digits give the same pair?
        cw, ch = 1.2, 0.6
        x0, y0 = -5.55, 2.75
        cells, nums, marks = {}, {}, {}
        for p, q in PAIRS:
            x, y = x0 + q * cw, y0 - (p - 1) * ch
            r = Rectangle(width=cw - 0.06, height=ch - 0.06, stroke_color=C.FAINT, stroke_width=1.5,
                          fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to([x, y, 0])
            cells[p, q] = r
            nums[p, q] = M(f"{999 * p + 90 * q:04d}", 21).move_to(r).shift(LEFT * 0.16)
            ok = pair(999 * p + 90 * q) == (p, q)
            marks[p, q] = M("✓" if ok else "✗", 20, C.GREEN if ok else C.RED, weight="BOLD") \
                .move_to(r).shift(RIGHT * 0.4)
        qlab = VGroup(*[M(f"q={q}", 20, C.MUTED).move_to([x0 + q * cw, y0 + 0.5, 0]) for q in range(10)])
        plab = VGroup(*[M(f"p={p}", 20, C.MUTED).move_to([x0 - 0.85, y0 - (p - 1) * ch, 0]) for p in range(1, 10)])
        grid = VGroup(*[VGroup(cells[k], nums[k]) for k in PAIRS])
        self.say("כל משבצת היא זוג אחד, ובתוכה ההפרש\nשהוא נותן, 999p + 90q. ‏p = 0 נותן רק 0.",
                 FadeIn(qlab), FadeIn(plab),
                 LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.03), run_time=2.4)

        # Checked one by one: the pair of each difference against the cell's own pair.
        probe = M("", 30)
        probe_pos = [3.6, 0.9, 0]
        with self.beat("בודקים כל משבצת : האם לספרות של\nההפרש יש שוב אותו p ואותו q?"):
            for p, q in PAIRS[:5]:
                v = 999 * p + 90 * q
                np_, nq = pair(v)
                new = VGroup(M(f"{v:04d}  ->  (p, q) = ({np_}, {nq})", 26),
                             M(f"cell ({p}, {q})", 26, C.MUTED)).arrange(DOWN, buff=0.15).move_to(probe_pos)
                self.play(Transform(probe, new), FadeIn(marks[p, q], scale=1.4),
                          cells[p, q].animate.set_fill(C.RED, 0.25), run_time=0.6)
        with self.beat("‏53 משבצות נכשלות : הספרות של\nההפרש שלהן נותנות זוג אחר."):
            rest = [k for k in PAIRS[5:] if k != (6, 2)]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(marks[k]), cells[k].animate.set_fill(C.RED, 0.25))
                                    for k in rest], lag_ratio=0.04),
                      FadeOut(probe), run_time=2.6)
        good = cells[6, 2]
        ring = SurroundingRectangle(good, color=C.GREEN, buff=0.04, stroke_width=5)
        check = M("7641 − 1467 = 6174", 30, C.GREEN).move_to([3.6, 0.9, 0])
        self.say("רק משבצת אחת עוברת :\n‏p = 6, ‏q = 2, כלומר 6174.",
                 FadeIn(marks[6, 2], scale=1.6), good.animate.set_fill(C.GREEN, 0.4), Create(ring), FadeIn(check))
        self.say("יחד עם 0, יש בדיוק שני מספרים\nמיוחדים : 0 ו-6174.", Indicate(nums[6, 2], color=C.AMBER))
        self.fade_all()

        # Why: the digits of the difference, conditions a and b, the cases.
        l1 = TX(r"q \ge 1:\quad (p,\; q-1,\; 9-q,\; 10-p)", size=40).move_to(UP * 2.3)
        l0 = TX(r"q = 0:\quad (p-1,\; 9,\; 9,\; 10-p)", size=40, color=C.BLUE).next_to(l1, DOWN, buff=0.4)
        self.say("ולמה? חיסור במאונך נותן את ספרות ההפרש\nישר מ-p ו-q, עם לווה בעמודות הנמוכות.",
                 FadeIn(l1), FadeIn(l0))
        cond = VGroup(TX(r"\text{(a)}\ \max - \min = p", size=36),
                      TX(r"\text{(b)}\ \text{middle two differ by } q", size=36)).arrange(DOWN, buff=0.25)
        cond.next_to(l0, DOWN, buff=0.5)
        self.say("מספר מיוחד שווה להפרש, ולכן לספרות\nההפרש יש אותו p ואותו q : שני תנאים.", FadeIn(cond))
        no0 = TX(r"q = 0:\ \text{three 9s} \;\Rightarrow\; \text{impossible}", size=36, color=C.RED)
        no0.next_to(cond, DOWN, buff=0.45)
        self.say("כש-q = 0 יש בהפרש שתי ספרות 9, ואז\nצריך שלוש. זה לא מסתדר : העמודה נפסלת.",
                 FadeIn(no0))
        self.fade_all()
        c1 = TX(r"q \ge 1:\ 7 \text{ cases (largest, smallest)}", size=38).move_to(UP * 2.2)
        self.say("כש-q ≥ 1 בודקים מי הספרה הגדולה\nומי הקטנה : יש רק שבעה מקרים.", FadeIn(c1))
        c4 = TX(r"\max = 9-q,\ \min = q-1:\quad p = 10 - 2q", size=38).next_to(c1, DOWN, buff=0.5)
        c5 = TX(r"|10 - 4q| = q \;\Rightarrow\; q = 2,\ p = 6", size=40, color=C.AMBER).next_to(c4, DOWN, buff=0.45)
        self.say("שישה מקרים נפסלים. במקרה היחיד\nשנשאר, הגדולה 9 − q והקטנה q − 1.", FadeIn(c4))
        self.say("התנאי השני נותן q = 2, ולכן p = 6 :\n‏999 · 6 + 90 · 2 = 6174.", FadeIn(c5))
        self.fade_all()

        # The code: typed, then its run, jumping over the numbers that are not special.
        code = page_python(QID, "def find_special_4")
        panel = CodePanel(code, font_size=34)
        env = {}
        exec(page_python(QID, "def is_special_4"), env)
        steps, result = trace(code, "find_special_4", (), env=env)
        assert result == [0, 6174] and set(s.line for s in steps) == {2}
        self.place_code(panel)
        panel.shift(UP * 1.2)
        self.type_code(panel, [
            (1, "‏find_special_4 לא מקבלת כלום,\nומחזירה רשימה."),
            (2, "היא עוברת על x מ-0 עד 9999, ושומרת\nכל x ש-is_special_4 מחזירה עבורו 1."),
        ], intro="ובקוד : בלי ההוכחה, פשוט בודקים הכול.")
        xv = M("x = 0", 40).move_to(LEFT * 3.2 + DOWN * 1.0)
        out = M("[0]", 40, C.GREEN).move_to(RIGHT * 2.4 + DOWN * 1.0)
        out_name = M("result:", 32, C.MUTED).next_to(out, LEFT, buff=0.3)
        bar = panel.bar(2)
        self.say("‏x = 0 : כל הספרות 0, וההפרש 0.\nהוא מיוחד, ונכנס לרשימה.",
                 FadeIn(bar), FadeIn(xv), FadeIn(out_name), FadeIn(out))
        with self.beat("מ-1 עד 6173 אין אף מספר מיוחד,\nולכן קופצים קדימה."):
            for v in (1000, 2000, 3000, 4000, 5000, 6000, 6173):
                self.play(Transform(xv, M(f"x = {v}", 40).move_to(xv)), run_time=0.3)
        new = M("[0, 6174]", 40, C.GREEN).move_to(out).align_to(out, LEFT)
        self.say("‏x = 6174 : ‏7641 פחות 1467 הם 6174.\nמיוחד, ונכנס לרשימה.",
                 Transform(xv, M("x = 6174", 40, C.AMBER).move_to(xv)), Transform(out, new))
        with self.beat("ומ-6175 עד 9999 שוב אין אף אחד :\nהתוצאה היא 0 ו-6174."):
            for v in (7000, 8000, 9000, 9999):
                self.play(Transform(xv, M(f"x = {v}", 40).move_to(xv)), run_time=0.3)
            self.play(Indicate(out, color=C.AMBER), run_time=0.8)
        self.fade_all()

        # The page's pairs box: the arrows from (9, 5) to 6174.
        view = BoxView(QID, "pairs", height=5.9).move_to(UP * 0.6)
        self.say("בתיבה שבעמוד לוחצים על זוג, והחץ\nמוביל לזוג של ההפרש הבא. מתחילים מ-9441.",
                 FadeIn(view))
        self.box_beat(view, [
            (1, "‏9441 נותן את הזוג p = 8, ‏q = 0,\nכלומר 7992."),
            (2, "‏7992 מוביל ל-7173,"),
            (3, "‏7173 ל-6354,"),
            (4, "‏6354 ל-3087,"),
            (5, "ו-3087 ל-8352."),
            (6, "‏8352 מוביל ל-6174, והזוג (6, 2)\nמצביע על עצמו : המסלול נעצר."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        hist = BoxView(QID, "hist", height=5.6).move_to(UP * 0.62)
        self.say("על כל 10,000 המספרים : ‏9,990 מגיעים\nל-6174 תוך שבעה צעדים לכל היותר.", FadeIn(hist))
        self.say("ועשרת המספרים שכל הספרות שלהם שוות,\nכמו 7777, נופלים ל-0.")
        self.fade_all()

        chips = cost_chips(("loop", "10000"), ("by the proof", "55"),
                           notes=("each check O(1)", "the pairs (p, q)"))
        self.say("הלולאה בודקת 10,000 מספרים, כל אחד\nב-O(1). לפי ההוכחה מספיק לבדוק 55.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterC(KScene):
    def construct(self):
        self.chapter_card("סעיף ג", "ארבע ספרות בבסיס B",
                          "סעיף ג, בקצרה : אותו תהליך,\nאבל המספר כתוב בבסיס B.")
        l1 = TX(r"F = p\,(B^3 - 1) + q\,(B^2 - B)", size=44).move_to(UP * 2.3)
        self.say("אותו חישוב, עם B במקום 10 :\nההפרש תלוי שוב רק ב-p וב-q.", FadeIn(l1))
        l2 = TX(r"q \ge 1:\quad (p,\; q-1,\; B-q-1,\; B-p)", size=40).next_to(l1, DOWN, buff=0.5)
        self.say("והספרות שלו, כש-q ≥ 1, הן p, ‏q − 1,\n‏B − q − 1 ו-B − p.",
                 l1.animate.set_opacity(0.45), FadeIn(l2))
        l3 = TX(r"p = 3q,\quad B = 5q", size=46, color=C.AMBER).next_to(l2, DOWN, buff=0.55)
        self.say("אותם שני תנאים. רק חלוקה אחת של\nהספרות נותנת משפחה : p = 3q ו-B = 5q.",
                 l2.animate.set_opacity(0.45), FadeIn(l3))
        self.fade_all()

        head = TX(r"B = 5k:\quad (3k,\; k-1,\; 4k-1,\; 2k)", size=44, color=C.AMBER).move_to(UP * 2.4)
        self.say("התשובה : נקודת שבת קיימת כש-B מתחלק\nב-5, והספרות שלה 3k, ‏k − 1, ‏4k − 1, ‏2k.",
                 FadeIn(head))
        rows = VGroup(*[VGroup(M(f"B = {B}", 34, C.MUTED), M(f"k = {B // 5}", 34, C.MUTED),
                               M(b_text(FAMILY[B][0], B), 40, C.GREEN if B == 10 else C.WHITE))
                        .arrange(RIGHT, buff=0.9) for B in (5, 10, 15)]).arrange(DOWN, buff=0.4)
        rows.next_to(head, DOWN, buff=0.6)
        self.say("בסיס 5 נותן 3032, בסיס 15 נותן 92B6,\nובבסיס 10, עם k = 2, זה 6174.",
                 LaggedStart(*[FadeIn(r, shift=0.15 * DOWN) for r in rows], lag_ratio=0.3), run_time=1.6)
        exc = M("B = 2: 0111, 1001     B = 4: 3021", 32, C.BLUE).next_to(rows, DOWN, buff=0.55)
        self.say("ועוד שני חריגים : 0111 ו-1001 בבסיס 2,\nו-3021 בבסיס 4. בכל בסיס אחר אין.", FadeIn(exc))
        self.fade_all()

        view = BoxView(QID, "base", height=5.9).move_to(UP * 0.6)
        self.say("אבל קיום אינו התכנסות. בתיבה שבעמוד :\nבסיס 15, ונקודת השבת שלו 92B6.", FadeIn(view))
        self.box_beat(view, [
            (1, "‏1234 בבסיס 15 לא מגיע אליה : הוא נכנס\nלמחזור של ארבעה, 30DC עד 9676."),
            (2, "אותן ספרות בבסיס 10 :\n‏1234, עם p = 3 ו-q = 1."),
            (3, "שלושה צעדים, דרך 3087 ו-8352,\nוהוא נעצר ב-6174."),
        ])
        self.fade_all()


class Closing(KScene):
    def construct(self):
        self.closing(QID, [("א", M("sort once: largest − smallest == x", 30)),
                           ("ב", TX(r"999p + 90q \;\Rightarrow\; \{0,\ 6174\}", size=34)),
                           ("ג", TX(r"B = 5k:\ (3k,\ k-1,\ 4k-1,\ 2k)", size=34))],
                     ["לסיכום : ההפרש תלוי רק ב-p וב-q,\nורק הזוג (6, 2) חוזר לעצמו : 6174.",
                      "נסו מספרים ובסיסים משלכם בתיבות\nשבעמוד של שאלה 0013 באתר."],
                     holds=(3.5, 3.5))
