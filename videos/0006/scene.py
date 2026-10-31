"""The tutorial video of question 0006, the best single trade of a stock (script: script.md).

Render with `python videos/render.py 0006` (see VIDEOS.md). The example is the page's,
prices = [5, 8, 3, 9, 2, 6]: the best long earns 6 (days 2 and 3), the best short 7
(days 3 and 4). Only the efficient O(n) code of each part is typed (the owner,
2026-10-31); the O(n²) check of every pair is named in the idea. The page's box is shown
twice in each chapter: alone, played day by day on the example, and beside the code while
the code runs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 6
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – קנייה ואחר כך מכירה"),
    ("ChapterB", "סעיף ב – מותר גם שורט"),
    ("Closing", "סיכום"),
]

PRICES = [5, 8, 3, 9, 2, 6]          # the page's example

# The page's two boxes: the scan of part א (long only) and of part ב (long and short),
# reset to the start and stepped one day at a time. Picture 0 is the box as the page opens
# it, 1 the start (before day 0), 2 + d after day d.
BOXES = {
    "long": {"box": 0, "region": [".ex-play-row", ".st-chart", ".wv-step", ".wv-sum"], "hide": [".wv-hint", ".ex-scrubwrap"],
             "steps": [[], [["click", ".ex-start"]], {"do": [["click", ".ex-next"]], "repeat": 6}]},
    "both": {"box": 1, "region": [".ex-play-row", ".st-chart", ".wv-step", ".wv-sum"], "hide": [".wv-hint", ".ex-scrubwrap"],
             "steps": [[], [["click", ".ex-start"]], {"do": [["click", ".ex-next"]], "repeat": 6}]},
}
START = 1


def day(d: int) -> int:
    """The box's picture after day d."""
    return 2 + d


class PriceChart(VGroup):
    """The prices as dots joined by a line, the price over each dot and the day under it."""

    def __init__(self, prices, width: float = 9.6, height: float = 3.7, top: float = 10,
                 base: float = -1.55):
        super().__init__()
        self.prices, self.n = list(prices), len(prices)
        self.dx = width / max(1, self.n - 1)
        self.x0, self.y0, self.k = -width / 2, base, height / top
        self.axis = Line([self.x0 - 0.5, base, 0], [self.x0 + width + 0.5, base, 0],
                         stroke_color=C.FAINT, stroke_width=2)
        self.line = VMobject(stroke_color=C.MUTED, stroke_width=3)
        self.line.set_points_as_corners([self.pt(d) for d in range(self.n)])
        self.dots = VGroup(*[Circle(radius=0.13, stroke_color=C.WHITE, stroke_width=3,
                                    fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to(self.pt(d))
                             for d in range(self.n)])
        self.vals = VGroup(*[M(str(p), 30).next_to(self.dots[d], UP, buff=0.14)
                             for d, p in enumerate(self.prices)])
        self.days = VGroup(*[M(str(d), 26, C.MUTED).move_to([self.x(d), base - 0.38, 0])
                             for d in range(self.n)])
        self.add(self.axis, self.line, self.dots, self.vals, self.days)

    def x(self, d: float) -> float:
        return self.x0 + d * self.dx

    def y(self, p: float) -> float:
        return self.y0 + p * self.k

    def pt(self, d: int) -> np.ndarray:
        return np.array([self.x(d), self.y(self.prices[d]), 0.0])

    def running(self, pick, color: str) -> VMobject:
        """A dashed step line: over each day, `pick` (min or max) of the prices so far."""
        pts = []
        for d in range(self.n):
            v = pick(self.prices[:d + 1])
            pts += [[self.x(d - 0.5) if d else self.x(0) - 0.3, self.y(v), 0],
                    [self.x(d + 0.5) if d < self.n - 1 else self.x(d) + 0.3, self.y(v), 0]]
        path = VMobject(stroke_color=color, stroke_width=4)
        path.set_points_as_corners(pts)
        return DashedVMobject(path, num_dashes=60)

    def seg(self, i: int, j: int, color: str, width: float = 9) -> Line:
        return Line(self.pt(i), self.pt(j), stroke_color=color, stroke_width=width)

    def gap(self, d: int, level: float, color: str) -> VGroup:
        """A vertical bar from `level` up (or down) to the price of day d."""
        a, b = [self.x(d), self.y(level), 0], self.pt(d)
        return Line(a, b, stroke_color=color, stroke_width=6)


class StockScene(DVQScene):
    """Helpers shared by the chapters of 0006."""

    def chart(self) -> PriceChart:
        return PriceChart(PRICES)

    def note(self, text: str, color: str | None = None, size: float = 40) -> Text:
        return M(text, size, color or C.AMBER).move_to(UP * 3.05)


class Opening(StockScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "רווח מקסימלי ממניה – לונג או שורט",
                     ["א · קנייה ואחר כך מכירה", "ב · מותר גם שורט"],
                     ["שאלה 0006 : רווח מקסימלי ממניה,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : קודם רק לונג,\nואז גם שורט."])
        self.fade_all()
        ch = self.chart()
        self.say("נתון מערך prices : המחיר של המניה בכל יום.\nמותר לבצע עסקה אחת.",
                 FadeIn(ch, lag_ratio=0.05), run_time=1.6)
        self.fade_all()


class ChapterA(StockScene):
    def construct(self):
        self.chapter_card("סעיף א", "קנייה ואחר כך מכירה",
                          "סעיף א : קונים ביום אחד,\nומוכרים ביום מאוחר יותר. עסקת לונג.")
        ch = self.chart()
        self.say("המחירים מהעמוד : 5, 8, 3, 9, 2, 6,\nמחיר אחד לכל יום.",
                 FadeIn(ch, lag_ratio=0.05), run_time=1.4)
        trade = ch.seg(2, 3, C.BLUE)
        lab = M("9 − 3 = 6", 36, C.BLUE).move_to(UP * 3.05)
        self.say("קונים ביום i ומוכרים ביום j > i.\nהרווח : prices[j] − prices[i].",
                 Create(trade), FadeIn(lab))
        pairs = VGroup(*[Line(ch.pt(i), ch.pt(j), stroke_color=C.FAINT, stroke_width=2)
                         for i in range(6) for j in range(i + 1, 6)])
        self.say("הדרך הישירה בודקת כל זוג ימים :\nכאן 15 זוגות, ובכלל זמן O(n²).",
                 FadeOut(trade), FadeOut(lab), Create(pairs, lag_ratio=0.05), run_time=1.6)
        low = ch.running(min, C.BLUE)
        self.say("הרעיון : אם מוכרים ביום j, הכי טוב לקנות\nבמחיר הנמוך ביותר עד אותו יום.",
                 FadeOut(pairs), Create(low), run_time=1.6)
        gaps = VGroup(*[ch.gap(d, min(PRICES[:d]), C.GREEN if PRICES[d] > min(PRICES[:d]) else C.RED)
                        for d in range(1, 6)])
        self.say("לכן מספיק לזכור את המינימום עד כה,\nולעבור על המערך פעם אחת.",
                 Create(gaps, lag_ratio=0.2), run_time=1.6)
        self.fade_all()

        # The page's box, played day by day on the same prices.
        view = BoxView(QID, "long", height=5.7, start=START).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד, על אותם מחירים.\nהקו הכחול הוא המינימום עד כה.",
                 FadeIn(view))
        self.box_beat(view, [
            (day(0), "יום 0 : המחיר 5. אין יום קודם,\nולכן 5 הוא המינימום."),
            (day(1), "יום 1 : 8 − 5 = 3.\nהלונג הטוב ביותר עד כה מרוויח 3."),
            (day(2), "יום 2 : 3 − 5 שלילי, אין רווח.\nאבל 3 הוא המינימום החדש."),
            (day(3), "יום 3 : 9 − 3 = 6. לונג חדש :\nקנייה ביום 2 ומכירה ביום 3."),
            (day(4), "יום 4 : 2 − 3 שלילי.\nהמינימום החדש הוא 2."),
            (day(5), "יום 5 : 6 − 2 = 4, פחות מ-6.\nהתשובה : רווח 6, ימים 2 ו-3."),
        ])
        self.fade_all()

        # The code: typed, then run beside the box.
        code = page_python(QID, "def max_long_fast")
        steps, result = trace(code, "max_long_fast", (PRICES,))
        assert result == (6, 2, 3), result
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True)
        names = ["i", "p", "min_p", "best", "buy", "sell"]
        vp = VarPanel(names, fmt=lambda n, s: str(s[n]) if n in s else "", size=30, cols=3,
                      slot=3.0).set_state({})
        self.place_code(panel)
        self.type_code(panel, [
            (1, "‏max_long_fast מקבלת את רשימת המחירים,\nומחזירה רווח, יום קנייה ויום מכירה."),
            (2, "שורה 2 : עוד אין עסקה.\nרווח 0, ובלי ימים."),
            ([3, 4], "שורות 3–4 : רשימה ריקה מחזירה מיד\nאת התשובה \"אין עסקה\"."),
            (5, "שורה 5 : המינימום עד כה מתחיל\nבמחיר של היום הראשון, יום 0."),
            (6, "שורה 6 : עוברים על הימים לפי הסדר.\n‏i הוא היום, ו-p המחיר שלו."),
            ([7, 8], "שורות 7–8 : מוכרים היום, וקנינו במינימום.\nרווח גדול יותר נשמר עם שני הימים."),
            ([9, 10], "שורות 9–10 : רק אחרי הבדיקה מעדכנים\nאת המינימום, כדי לא לקנות ולמכור באותו יום."),
            (11, "שורה 11 : מחזירים את העסקה הטובה ביותר."),
        ], intro="עכשיו נכתוב את זה ב-Python, שורה אחרי שורה.")
        view = BoxView(QID, "long", start=START)
        with self.beat("נריץ את הקוד על הדוגמה,\nוהתיבה מהעמוד מתקדמת יחד איתו."):
            self.split(panel, view, vp)
        self.run_code(panel, vp, steps, [
            ([2, 3, 5], "שורות 2–5 : אין עסקה עדיין,\nוהמינימום הוא 5, מיום 0.", None),
            ([6, 7, 9], "יום 0 : 5 − 5 = 0, לא יותר מ-0.\nהמינימום נשאר 5.", day(0)),
            ([6, 7, 8, 9], "יום 1 : 8 − 5 = 3. שורה 8 שומרת\nרווח 3, קנייה ביום 0 ומכירה ביום 1.", day(1)),
            ([6, 7, 9, 10], "יום 2 : 3 − 5 שלילי, ושורה 10\nמעדכנת את המינימום ל-3, ביום 2.", day(2)),
            ([6, 7, 8, 9], "יום 3 : 9 − 3 = 6, יותר מ-3.\nהעסקה החדשה : ימים 2 ו-3.", day(3)),
            ([6, 7, 9, 10], "יום 4 : 2 − 3 שלילי.\nהמינימום יורד ל-2, ביום 4.", day(4)),
            ([6, 7, 9], "יום 5 : 6 − 2 = 4, פחות מ-6.\nשום דבר לא משתנה.", day(5)),
            ([6, 11], "הלולאה נגמרה. התשובה :\nרווח 6, קנייה ביום 2 ומכירה ביום 3.", None),
        ], view=view)
        self.fade_all()

        # Why it works: every sell day against the minimum of the days before it.
        ch = self.chart()
        low = ch.running(min, C.BLUE)
        self.say("למה זה נכון : לכל יום מכירה j, הקנייה\nהטובה ביותר היא במינימום של הימים שלפניו.",
                 FadeIn(ch), Create(low), run_time=1.4)
        gaps, labels = VGroup(), VGroup()
        for d in range(1, 6):
            m = min(PRICES[:d])
            g = PRICES[d] - m
            gaps.add(ch.gap(d, m, C.GREEN if g > 0 else C.RED))
            labels.add(M(f"{g:+d}", 30, C.GREEN if g > 0 else C.RED)
                       .next_to(ch.dots[d], RIGHT, buff=0.12))
        best = SurroundingRectangle(labels[2], color=C.AMBER, buff=0.1, corner_radius=0.08)
        self.say("הלולאה בודקת בדיוק את הערך הזה לכל יום,\nולכן המקסימום שלה הוא המקסימום על כל הזוגות.",
                 Create(gaps, lag_ratio=0.2), FadeIn(labels, lag_ratio=0.2), Create(best), run_time=1.8)
        self.fade_all()

        # The trap: the highest price minus the lowest one.
        tr = PriceChart([9, 1], width=4.0, height=3.4)
        wrong = M("max − min = 9 − 1 = 8", 38, C.RED).move_to(UP * 3.05)
        self.say("המלכודת : לחשב את המחיר הגבוה ביותר\nפחות הנמוך ביותר, בכל המערך.",
                 FadeIn(tr), FadeIn(wrong))
        cross = Cross(wrong, stroke_color=C.RED, stroke_width=5)
        fix = M("best long = 0", 38, C.GREEN).move_to(DOWN * 2.15 + RIGHT * 4.2)
        self.say("עבור 9, 1 ההפרש הוא 8, אבל הקנייה חייבת\nלבוא לפני המכירה : אין לונג שמרוויח.",
                 Create(cross), FadeIn(fix))
        self.fade_all()

        chips = cost_chips(("time", "O(n)"), ("memory", "O(1)"),
                           notes=("one pass", "min_p, min_i"))
        self.say("הסיבוכיות : מעבר אחד, זמן O(n),\nוזיכרון O(1), במקום O(n²) של כל הזוגות.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterB(StockScene):
    def construct(self):
        self.chapter_card("סעיף ב", "מותר גם שורט",
                          "סעיף ב : הטוויסט. מותר גם שורט.")
        ch = self.chart()
        self.play(FadeIn(ch), run_time=0.8)
        short = ch.seg(3, 4, C.ORANGE)
        lab = M("9 − 2 = 7", 36, C.ORANGE).move_to(UP * 3.05)
        self.say("שורט : מוכרים ביום i, וקונים בחזרה\nביום מאוחר יותר j.",
                 Create(short), FadeIn(lab))
        self.say("הרווח בשורט : prices[i] − prices[j].\nמרוויחים כשהמחיר יורד.")
        long_ = ch.seg(2, 3, C.BLUE)
        lab2 = VGroup(M("long +6", 34, C.BLUE), M("short +7", 34, C.ORANGE)).arrange(RIGHT, buff=1.2)
        lab2.move_to(UP * 3.05)
        self.say("בדוגמה, הלונג הטוב ביותר מרוויח 6,\nוהשורט הטוב ביותר מרוויח 7.",
                 Create(long_), Transform(lab, lab2))
        ans = M("short, 7, days 3 → 4", 34, C.AMBER).move_to(DOWN * 2.2 + RIGHT * 3.4)
        self.say("לכן התשובה : שורט, רווח 7, ימים 3 ו-4.", FadeIn(ans))
        self.play(FadeOut(long_), FadeOut(short), FadeOut(lab), FadeOut(ans), run_time=0.6)

        low, high = ch.running(min, C.BLUE), ch.running(max, C.ORANGE)
        self.say("הרעיון : רווח השורט הוא מינוס רווח הלונג\nבאותם ימים.", Create(low))
        self.say("לכן בשורט זוכרים את המקסימום עד כה,\nושני החישובים רצים באותה לולאה.",
                 Create(high), run_time=1.4)
        self.fade_all()

        view = BoxView(QID, "both", height=5.7, start=START).move_to(UP * 0.62)
        self.say("בתיבה : הקו הכחול הוא המינימום עד כה,\nוהכתום הוא המקסימום עד כה.",
                 FadeIn(view))
        self.box_beat(view, [
            (day(0), "יום 0 : המינימום והמקסימום הם 5."),
            (day(1), "יום 1 : לונג 8 − 5 = 3.\nהמקסימום עולה ל-8."),
            (day(2), "יום 2 : שורט 8 − 3 = 5.\nהמינימום יורד ל-3."),
            (day(3), "יום 3 : לונג 9 − 3 = 6.\nהמקסימום עולה ל-9."),
            (day(4), "יום 4 : שורט 9 − 2 = 7.\nהמינימום יורד ל-2."),
            (day(5), "יום 5 : לונג 4 ושורט 3, בלי שיפור.\nהשורט, 7, מנצח את הלונג, 6."),
        ])
        self.fade_all()

        code = page_python(QID, "def max_profit_fast")
        steps, result = trace(code, "max_profit_fast", (PRICES,))
        assert result == (7, "short", 3, 4), result
        panel = CodePanel(code, font_size=34, drop_comments=True, drop_trailing_comments=True,
                          rows=14)
        vp = VarPanel(["i", "p", "min_p", "max_p", "long_best", "short_best"],
                      fmt=lambda n, s: str(s[n]) if n in s else "", size=30, cols=2,
                      slot=4.2).set_state({})
        self.place_code(panel)
        self.type_code(panel, [
            (1, "‏max_profit_fast מחזירה רווח, סוג העסקה,\nויום הפתיחה ויום הסגירה שלה."),
            ([2, 3], "שורות 2–3 : עסקה צריכה שני ימים.\nעם פחות משני מחירים אין עסקה."),
            ([5, 6], "שורות 5–6 : המינימום והמקסימום עד כה,\nשניהם מתחילים במחיר של יום 0."),
            ([8, 9], "שורות 8–9 : שני מועמדים, לונג ושורט,\nכל אחד עם רווח 0 ובלי ימים."),
            (11, "שורה 11 : לולאה אחת על כל הימים."),
            ([12, 13, 14], "שורות 12–14 : בדיקת הלונג, כמו בסעיף א,\nמול המינימום של הימים הקודמים."),
            ([16, 17, 18], "שורות 16–18 : תמונת הראי בשביל השורט :\nהמקסימום עד כה פחות מחיר היום."),
            ([20, 21, 22, 23], "שורות 20–23 : רק אחרי שתי הבדיקות\nמעדכנים את המינימום ואת המקסימום."),
            ([25, 26], "שורות 25–26 : אם השורט טוב יותר מהלונג,\nמחזירים אותו."),
            ([27, 28, 29], "שורות 27–29 : אחרת את הלונג, אם הוא מרוויח.\nואם לא, אין עסקה."),
        ], intro="ב-Python זו אותה לולאה, עם שני מועמדים.")
        view = BoxView(QID, "both", start=START)
        with self.beat("נריץ על הדוגמה, יום אחרי יום,\nלצד התיבה מהעמוד."):
            self.split(panel, view, vp)
        loop_a = [11, 12, 16, 20, 22]
        long_up = [11, 12, 13, 14, 16, 20, 22, 23]
        short_dn = [11, 12, 16, 17, 18, 20, 21, 22]
        self.run_code(panel, vp, steps, [
            ([2, 5, 6, 8, 9], "שורות 2–9 : המינימום והמקסימום הם 5,\nושני המועמדים ברווח 0.", None),
            (loop_a, "יום 0 : אין רווח לאף כיוון.", day(0)),
            (long_up, "יום 1 : לונג 8 − 5 = 3, ושורה 23\nמעלה את המקסימום ל-8.", day(1)),
            (short_dn, "יום 2 : שורט 8 − 3 = 5, ושורה 21\nמורידה את המינימום ל-3.", day(2)),
            (long_up, "יום 3 : לונג 9 − 3 = 6,\nוהמקסימום עולה ל-9.", day(3)),
            (short_dn, "יום 4 : שורט 9 − 2 = 7,\nוהמינימום יורד ל-2.", day(4)),
            (loop_a, "יום 5 : לונג 4 ושורט 3, בלי שיפור.", day(5)),
            ([11], "הלולאה נגמרה : הלונג הטוב ביותר 6,\nוהשורט הטוב ביותר 7.", None),
            ([25, 26], "שורה 25 : 7 גדול מ-6, ולכן מוחזר\nשורט, רווח 7, ימים 3 ו-4.", None),
        ], view=view)
        self.fade_all()

        chips = cost_chips(("time", "O(n)"), ("memory", "O(1)"),
                           notes=("one pass", "min, max, two trades"))
        self.say("הסיבוכיות : עדיין מעבר אחד, זמן O(n),\nוזיכרון נוסף קבוע, O(1).",
                 FadeIn(chips, lag_ratio=0.3))
        scale = VGroup(M("n = 10⁶", 34, C.MUTED),
                       M("all pairs ≈ 5·10¹¹", 34, C.RED),
                       M("one pass = 10⁶", 34, C.GREEN)).arrange(RIGHT, buff=0.8).move_to(DOWN * 2.0)
        self.say("עבור מיליון ימים : כחמש מאות מיליארד זוגות,\nמול מיליון צעדים בלבד.",
                 FadeIn(scale, lag_ratio=0.3))
        self.fade_all()

        # The trap: a tie between the best long and the best short.
        tie = PriceChart([1, 4, 1], width=5.0, height=3.2, top=5)
        l2, s2 = tie.seg(0, 1, C.BLUE), tie.seg(1, 2, C.ORANGE)
        lab = VGroup(M("long +3", 34, C.BLUE), M("short +3", 34, C.ORANGE)).arrange(RIGHT, buff=1.2)
        lab.move_to(UP * 3.05)
        self.say("מלכודת : תיקו בין לונג לשורט.\nלמשל 1, 4, 1 : לונג 3 ושורט 3.",
                 FadeIn(tie), Create(l2), Create(s2), FadeIn(lab))
        res = M('(3, "long", 0, 1)', 36, C.GREEN).move_to(DOWN * 2.15 + RIGHT * 3.8)
        self.say("ההשוואה החדה בשורה 25 מחזירה את הלונג.\nכל זוג עם הרווח המקסימלי הוא תשובה נכונה.",
                 FadeIn(res))
        self.fade_all()


class Closing(StockScene):
    def construct(self):
        self.closing(QID, [("א", M("min so far  →  best long", 34)),
                           ("ב", M("min and max so far  →  long or short", 34))],
                     ["לסיכום : המינימום עד כה נותן את הלונג,\nוהמקסימום עד כה נותן את השורט.",
                      "נסו מחירים משלכם בתיבה\nשבעמוד של שאלה 0006 באתר."])
