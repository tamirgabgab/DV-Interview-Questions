"""The tutorial video of question 0027, a cake split by fractions that grow as an arithmetic
sequence (script: script.md).

Render with `python videos/render.py 0027` (see notes/VIDEOS.md). No code (the page has none).
The division (the owner, 2026-11-03): a cake strip, as in the page's figure, from which each
person cuts a slice of what is left (the slices taken before stay faint in place, the
peak's slice orange), and under it a bar chart of each person's share, built bar by bar.

Part א: the page's numbers, a = 0.01 and d = 0.1, person by person (the first five slowly,
the rest at once, the last one taking the rest); the peak, person 4 with 0.2158; then the
page's proof: R_k and S_k, the ratio of two neighbours, the quadratic condition and its
root T = 0.2702, the fractions against T (three under it, the fourth the first above), and
S_4 = 0.31 x 0.6961. Then the page's box, person by person.

Part ב: the general condition f(p_k) = p_k^2 / (1 - p_k) < d, f increasing, the people as
points climbing the curve against the line y = d (one peak: once the condition fails it
fails for good), the threshold T and the person's formula checked on part א, the last
person (capped) in one line, the tie on a = d = 1/12 (T = 1/4 = p_3: persons 3 and 4 get
55/288 each), the exceptional d > 1/2 in one closing sentence pointing to the page's
follow-ups, and the box's proof panel (d = 0.1, then 0.25: the peak moves to person 3).
Every number is the page's reference (tools/figures/cake.py, exact fractions).
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, he, read_palette  # noqa: E402

import cake  # noqa: E402

QID = 27
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – הצבה מספרית"),
    ("ChapterB", "סעיף ב – המקרה הכללי"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="cake-arith", a = 0.01, d = 0.1): the stepper person by person,
# and the proof panel (all the people shown), then with d = 0.25.
BOXES = {
    "people": {"box": 0, "region": [".ex-play-row", ".cake-box"],
               "hide": [".ex-speed", ".ex-play"],
               "steps": [[], [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
                         [["click", ".ex-next"]], [["click", ".ex-all"]]]},
    "proof": {"box": 0, "region": [".cake-proof"],
              "hide": [".cake-box", ".ex-summary", ".ex-note", ".cake-charts"],
              "steps": [[["click", ".ex-all"]], [["fill", ".num-step", "0.25"], ["click", ".ex-all"]]]},
}

_S = read_palette()["slate"]
S1, S2, S3 = _S["--viz-s1"], _S["--viz-s2"], _S["--viz-s3"]
GRID, VTEXT = _S["--viz-grid"], _S["--viz-text"]

# ---- the numbers, from the page's reference (exact fractions) ----------------------------

A, D = Fr(1, 100), Fr(1, 10)
ROWS = cake.split(cake.ARITH, A, D)                     # (k, p, R, S)
PEAK, TOP = cake.best(ROWS)
T_A = cake.threshold(cake.ARITH, D)
assert len(ROWS) == 11 and PEAK == [4]
assert [float(p) for _, p, _, _ in ROWS] == [0.01, 0.11, 0.21, 0.31, 0.41, 0.51, 0.61, 0.71, 0.81, 0.91, 1.0]
assert [round(float(S), 4) for *_, S in ROWS] == [0.01, 0.1089, 0.185, 0.2158, 0.1969, 0.1445, 0.0847,
                                                  0.0384, 0.0127, 0.0027, 0.0003]
assert [round(float(R), 4) for _, _, R, _ in ROWS[:5]] == [1.0, 0.99, 0.8811, 0.6961, 0.4803]
assert round(float(ROWS[-1][2]), 4) == 0.0003 and A + 10 * D == Fr(101, 100)   # the 11th would take 1.01
assert round(T_A, 4) == 0.2702 and abs(T_A - (math.sqrt(0.41) - 0.1) / 2) < 1e-12
assert all(float(p) < T_A for _, p, _, _ in ROWS[:3]) and float(ROWS[3][1]) >= T_A
RATIOS = [ROWS[i + 1][3] / ROWS[i][3] for i in range(len(ROWS) - 1)]
assert all(r > 1 for r in RATIOS[:3]) and all(r < 1 for r in RATIOS[3:])
assert round(float(RATIOS[0]), 2) == 10.89


def f(p: float) -> float:
    return p * p / (1 - p)


# the general case: part א by the formula; the box's second picture (d = 0.25)
def k_star(a, d) -> int:
    t = cake.threshold(cake.ARITH, d)
    return max(1, math.ceil((t - float(a)) / float(d)) + 1)


assert k_star(A, D) == 4 and round((T_A - 0.01) / 0.1, 2) == 2.6
R25 = cake.split(cake.ARITH, A, Fr(1, 4))
assert cake.best(R25)[0] == [3] == [k_star(A, Fr(1, 4))] and round(cake.threshold(cake.ARITH, 0.25), 3) == 0.390
# the tie: a = d = 1/12, T = 1/4 = p_3, persons 3 and 4 get 55/288 each
TIE = cake.split(cake.ARITH, Fr(1, 12), Fr(1, 12))
assert cake.best(TIE) == ([3, 4], Fr(55, 288)) and len(TIE) == 12
assert Fr(1, 144) + 4 * Fr(1, 12) == Fr(49, 144) and (Fr(7, 12) - Fr(1, 12)) / 2 == Fr(1, 4) == TIE[2][1]
assert abs(cake.threshold(cake.ARITH, 1 / 12) - 0.25) < 1e-12
# the opening's example, a = d = 0.2: the fifth person (p = 1) takes the rest
OPEN = cake.split(cake.ARITH, Fr(1, 5), Fr(1, 5))
assert [S for *_, S in OPEN] == [Fr(1, 5), Fr(8, 25), Fr(36, 125), Fr(96, 625), Fr(24, 625)]


# ---- the cake strip and the bars ----------------------------------------------------------

class Strip(VGroup):
    """The cake as one strip (size 1 = its width): each person's slice cut, in order, from the
    left of what is left; the slices taken before stay in place, faint."""

    def __init__(self, rows, y: float = 2.65, x0: float = -5.6, width: float = 11.2, h: float = 0.62):
        super().__init__()
        self.rows, self.y, self.x0, self.w, self.h = rows, y, x0, width, h
        self.base = Rectangle(width=width, height=h, fill_color=GRID, fill_opacity=1, stroke_width=0)
        self.base.move_to([x0 + width / 2, y, 0])
        self.edge = Rectangle(width=width, height=h, stroke_color=VTEXT, stroke_width=2, fill_opacity=0)
        self.edge.move_to(self.base)
        self.add(self.base, self.edge)

    def left(self, k: int) -> float:
        return self.x0 + self.w * float(sum(S for kk, _, _, S in self.rows if kk < k))

    def slice(self, k: int, color: str) -> Rectangle:
        S = float(self.rows[k - 1][3])
        w = max(self.w * S, 0.025)
        r = Rectangle(width=w, height=self.h, fill_color=color, fill_opacity=0.9, stroke_color=C.NAVY,
                      stroke_width=1.5)
        r.move_to([self.left(k) + w / 2, self.y, 0])
        return r

    def rest_brace(self, k: int) -> VGroup:
        """The part left before person k, marked under the strip."""
        a, b = self.left(k), self.x0 + self.w
        line = Line([a, self.y - self.h / 2 - 0.16, 0], [b, self.y - self.h / 2 - 0.16, 0],
                    stroke_color=C.AMBER, stroke_width=4)
        ticks = VGroup(*[Line([x, self.y - self.h / 2 - 0.06, 0], [x, self.y - self.h / 2 - 0.26, 0],
                              stroke_color=C.AMBER, stroke_width=4) for x in (a, b)])
        return VGroup(line, ticks)


def slice_color(k: int, peak: list[int] | None = None) -> str:
    if peak and k in peak:
        return S2
    return S1 if k % 2 else S3


class Bars(VGroup):
    """The shares S_k as bars, person k under each."""

    def __init__(self, rows, x0: float = -4.9, gap: float = 0.95, base: float = -1.95,
                 scale: float = 11.0, bw: float = 0.62, label_size: int = 26):
        super().__init__()
        self.rows, self.x0, self.gap, self.base_y, self.scale, self.bw = rows, x0, gap, base, scale, bw
        n = len(rows)
        axis = Line([x0 - 0.6, base, 0], [x0 + gap * (n - 1) + 0.6, base, 0], stroke_color=C.MUTED, stroke_width=3)
        labels = VGroup(*[M(str(k), label_size, C.MUTED).move_to([self.x(k), base - 0.27, 0]) for k, *_ in rows])
        self.axis = VGroup(axis, labels)
        self.add(self.axis)

    def x(self, k: int) -> float:
        return self.x0 + self.gap * (k - 1)

    def bar(self, k: int, color: str) -> Rectangle:
        S = float(self.rows[k - 1][3])
        h = max(self.scale * S, 0.02)
        r = Rectangle(width=self.bw, height=h, fill_color=color, fill_opacity=0.9, stroke_width=0)
        r.move_to([self.x(k), self.base_y + h / 2, 0])
        return r

    def value(self, k: int, text: str, size: int = 21, color: str | None = None) -> Mobject:
        b = self.bar(k, C.WHITE)
        return M(text, size, color or C.WHITE).next_to(b, UP, buff=0.12)


def now_line(k: int, p: str, R: str, S: str) -> VGroup:
    """The step under the strip: the fraction, what is left, and the share."""
    return VGroup(TX(rf"p_{{{k}}} = {p}", size=38), TX(rf"R_{{{k}}} = {R}", size=38),
                  TX(rf"S_{{{k}}} = p_{{{k}}} R_{{{k}}} = {S}", size=38, color=C.AMBER)).arrange(RIGHT, buff=0.8)


class CakeScene(DVQScene):
    """Helpers shared by the scenes of 0027."""

    def cut(self, strip: Strip, bars: Bars, k: int, peak=None, run_time: float = 1.0, prev=None):
        """Person k cuts a slice: the slice appears on the strip, its bar grows; the slices
        before dim."""
        sl = strip.slice(k, slice_color(k, peak))
        bar = bars.bar(k, slice_color(k, peak))
        anims = [FadeIn(sl, scale=0.9), GrowFromEdge(bar, DOWN)]
        if prev is not None:
            anims.append(prev.animate.set_fill(opacity=0.35))
        self.play(*anims, run_time=run_time)
        return sl, bar


class Opening(CakeScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "חלוקת עוגה בסדרה חשבונית",
                     ["א · הצבה מספרית", "ב · המקרה הכללי"],
                     ["שאלה 0027 : חלוקת עוגה בסדרה חשבונית,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : הצבה מספרית,\nואז המקרה הכללי, עם פסגה אחת."])
        self.fade_all()
        strip = Strip(OPEN, y=2.2)
        self.say("עוגה שלמה, בגודל 1. אנשים ניגשים בתור,\nוכל אחד חותך פרוסה ממה שנשאר.",
                 FadeIn(strip))
        rule = TX(r"p_k = a + (k - 1)\,d", size=50).move_to(UP * 0.9)
        self.say("האדם ה-k לוקח את השבר a + (k − 1)d\nממה שנשאר : השברים בסדרה חשבונית.",
                 Write(rule))
        bars = Bars(OPEN, x0=-1.9, gap=0.95, base=-1.9, scale=7.5)
        self.play(rule.animate.scale(0.75).move_to([-4.3, 0.9, 0]), FadeIn(bars.axis), run_time=0.8)
        fracs = ["0.2", "0.4", "0.6", "0.8", "1"]
        lab = None
        prev = None
        with self.beat("למשל a = d = 0.2 : השברים 0.2, 0.4, 0.6\nו-0.8, והחמישי, עם 1, לוקח את השארית."):
            for k in range(1, 6):
                new = TX(rf"p_{{{k}}} = {fracs[k - 1]}", size=40, color=C.AMBER).move_to([4.3, 0.9, 0])
                sl, _ = self.cut(strip, bars, k, run_time=0.45, prev=prev)
                self.play(*([FadeOut(lab)] if lab else []), FadeIn(new), run_time=0.3)
                prev, lab = sl, new
        self.say("השבר גדל, אבל מה שנשאר קטן.\nמי מקבל את החלק הגדול ביותר?")
        self.fade_all()


class ChapterA(CakeScene):
    def construct(self):
        self.chapter_card("סעיף א", "הצבה מספרית",
                          "סעיף א : כאן a = 0.01 ו-d = 0.1, ולכן\nהשברים הם 0.01, 0.11, 0.21, 0.31 וכן הלאה.")
        self.people()
        self.why()
        self.over_t()
        self.box()

    # -- person by person ---------------------------------------------------------------------

    def people(self):
        strip, bars = Strip(ROWS), Bars(ROWS)
        self.play(FadeIn(strip), FadeIn(bars.axis), run_time=0.8)
        share = he("החלק של כל אדם", 30, C.MUTED).move_to([4.6, 0.7, 0])
        self.add(share)
        texts = [("0.01", "1", "0.0100"), ("0.11", "0.99", "0.1089"), ("0.21", "0.8811", "0.1850"),
                 ("0.31", "0.6961", "0.2158"), ("0.41", "0.4803", "0.1969")]
        prev, line, brace, vals, slices = None, None, None, VGroup(), []
        for k in range(1, 6):
            p, R, S = texts[k - 1]
            new_line = now_line(k, p, R, S).move_to([0, 1.55, 0])
            new_brace = strip.rest_brace(k)
            val = bars.value(k, S)
            # the captions are literal for render.py: one say() per person
            anims_out = [FadeOut(line), FadeOut(brace)] if line else []
            if anims_out:
                self.play(*anims_out, run_time=0.3)
            self.play(Create(new_brace), FadeIn(new_line), run_time=0.6)
            sl, bar = self.cut(strip, bars, k, prev=prev)
            slices.append(sl)
            if k == 1:
                self.say("האדם הראשון לוקח 0.01 מכל העוגה,\nפרוסה דקיקה.", FadeIn(val))
            elif k == 2:
                self.say("השני לוקח 0.11 ממה שנשאר, 0.99,\nומקבל 0.1089 : פי עשרה ויותר.", FadeIn(val))
            elif k == 3:
                self.say("השלישי לוקח 0.21 מ-0.8811,\nומקבל 0.1850.", FadeIn(val))
            elif k == 4:
                self.say("הרביעי לוקח 0.31 מ-0.6961,\nומקבל 0.2158. עוד עלייה.", FadeIn(val))
            else:
                self.say("החמישי לוקח 0.41, אבל רק מ-0.4803,\nומקבל 0.1969 : בפעם הראשונה ירידה.", FadeIn(val))
            vals.add(val)
            prev, line, brace = sl, new_line, new_brace
        self.play(FadeOut(line), FadeOut(brace), run_time=0.3)
        with self.beat("מכאן החלקים רק יורדים : השבר גדל,\nאבל כמעט לא נשאר ממה לחתוך."):
            for k in range(6, 11):
                sl, _ = self.cut(strip, bars, k, prev=prev, run_time=0.45)
                prev = sl
                slices.append(sl)
        last = TX(r"p_{11} = 1.01 \;\to\; 1", size=40).move_to([0, 1.55, 0])
        with self.beat("האחד-עשר היה אמור לקחת 1.01, ולכן\nלוקח את כל השארית : 0.0003 בלבד."):
            self.play(FadeIn(last), run_time=0.5)
            sl, _ = self.cut(strip, bars, 11, prev=prev, run_time=0.6)
            slices.append(sl)
        peak_bar = bars.bar(4, S2)
        peak_sl = strip.slice(4, S2)
        ring = SurroundingRectangle(peak_bar, color=C.AMBER, buff=0.08, stroke_width=4)
        self.say("הפסגה : האדם הרביעי, עם 0.2158 מהעוגה,\nכלומר בערך 21.6 אחוז.",
                 FadeOut(last), FadeIn(peak_bar), FadeIn(peak_sl), Create(ring),
                 vals[3].animate.set_color(C.AMBER))
        self.fade_all()

    # -- the proof ----------------------------------------------------------------------------

    def why(self):
        self.say("למה דווקא הרביעי? שני כוחות הפוכים :\nהשבר גדל, ומה שנשאר לחתוך ממנו קטן.")
        e1 = TX(r"S_k = p_k R_k, \qquad R_{k+1} = (1 - p_k)\, R_k", size=46).move_to(UP * 2.2)
        self.say("נסמן ב-Rₖ את מה שנשאר לפני האדם ה-k.\nהוא לוקח pₖ ממנו, והשאר עובר הלאה.", FadeIn(e1))
        e2 = TX(r"\frac{S_{k+1}}{S_k} = \frac{p_{k+1} R_{k+1}}{p_k R_k} = \frac{p_{k+1}(1 - p_k)}{p_k}",
                size=46).move_to(UP * 0.75)
        self.say("משווים כל אדם לבא אחריו : ביחס\nמה שנשאר מצטמצם, ונשארים רק השברים.", FadeIn(e2))
        e3 = TX(r"S_{k+1} > S_k", r"\iff", r"(p_k + d)(1 - p_k) > p_k", size=44)
        e4 = TX(r"\iff", r"p_k^2 + d\, p_k - d < 0", size=44)
        e3.move_to(DOWN * 0.7)
        e4.next_to(e3, DOWN, buff=0.35).align_to(e3[1], LEFT)
        self.say("הבא מקבל יותר כשהיחס גדול מ-1.\nמציבים pₖ₊₁ = pₖ + d ופותחים סוגריים.", FadeIn(e3))
        self.say("יוצא תנאי ריבועי על pₖ בלבד,\nבלי מה שנשאר מהעוגה.", FadeIn(e4))
        self.play(FadeOut(e1), FadeOut(e2), FadeOut(e3), e4.animate.move_to(UP * 2.2), run_time=0.8)
        t = TX(r"T = \frac{\sqrt{0.41} - 0.1}{2} \approx 0.2702", size=50, color=C.AMBER).move_to(UP * 0.6)
        self.say("השורש החיובי של p² + 0.1p − 0.1\nהוא הסף T, בערך 0.2702.", FadeIn(t))
        self.say("מתחת לסף הבא אחריך מקבל יותר,\nומעליו הוא מקבל פחות.")
        self.fade_all()

    def over_t(self):
        bars = Bars(ROWS, x0=-4.9, gap=0.95, base=-1.95, scale=9.5)
        # the fractions p_k as bars, against the dashed threshold
        fr = [bars.bar(k, C.WHITE) for k, *_ in ROWS]
        for k, (b, (_, p, _, _)) in enumerate(zip(fr, ROWS), 1):
            h = 4.0 * float(p)
            b.stretch_to_fit_height(h).move_to([bars.x(k), bars.base_y + h / 2, 0])
            b.set_fill(S1 if float(p) < T_A else (S2 if k == 4 else VTEXT), opacity=0.9)
        y_t = bars.base_y + 4.0 * T_A
        line = DashedLine([bars.x0 - 0.6, y_t, 0], [bars.x(11) + 0.6, y_t, 0], stroke_color=C.AMBER, stroke_width=3)
        lab = TX(r"T \approx 0.270", size=34, color=C.AMBER).next_to(line, RIGHT, buff=0.15).shift(UP * 0.3 + LEFT * 1.2)
        title = he("השבר של כל אדם מול הסף", 32, C.MUTED).move_to([0, 2.95, 0])
        self.say("עכשיו השברים עצמם, עמוד לכל אדם,\nוהקו המקווקו הוא הסף.",
                 FadeIn(bars.axis), FadeIn(title), Create(line), FadeIn(lab))
        self.say("‏0.01, 0.11 ו-0.21 מתחת לסף :\nולכן החלקים עולים עד הרביעי.",
                 *[GrowFromEdge(b, DOWN) for b in fr[:3]], lag_ratio=0.2)
        self.say("‏0.31 הוא הראשון שמגיע לסף, ומכאן כולם\nמעליו : מהרביעי והלאה החלקים רק יורדים.",
                 *[GrowFromEdge(b, DOWN) for b in fr[3:]], lag_ratio=0.12)
        self.fade_all()
        r4 = TX(r"R_4 = 0.99 \cdot 0.89 \cdot 0.79 \approx 0.6961", size=48).move_to(UP * 1.3)
        s4 = TX(r"S_4 = 0.31 \cdot 0.6961 \approx 0.2158", size=52, color=C.AMBER).move_to(DOWN * 0.1)
        self.say("והחלק שלו : לפני הרביעי נשארו\n‏0.99 כפול 0.89 כפול 0.79 מהעוגה.", FadeIn(r4))
        self.say("הוא לוקח 0.31 מזה, ומקבל 0.2158 :\nבערך 21.6 אחוז מהעוגה.", FadeIn(s4))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "people", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד מוסיפים אדם אחרי אדם,\nוהפרוסה שלו נחתכת מהעוגה.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי שלושה אנשים נוספים : הרביעי,\nעם החלק הגדול ביותר עד כה."),
            (2, "החמישי כבר מקבל פחות : היחס\nמול הקודם יורד מתחת ל-1."),
            (3, "וכל האחד-עשר : הפסגה אצל הרביעי,\nכמו בחישוב."),
        ])
        self.fade_all()


class ChapterB(CakeScene):
    def construct(self):
        self.chapter_card("סעיף ב", "המקרה הכללי",
                          "סעיף ב : עכשיו a ו-d כלליים,\nעם d לכל היותר חצי.")
        self.condition()
        self.curve()
        self.formula()
        self.tie()
        self.box()

    def condition(self):
        e1 = TX(r"S_{k+1} > S_k", r"\iff", r"d\,(1 - p_k) > p_k^2", size=46).move_to(UP * 1.9)
        e2 = TX(r"\iff", r"f(p_k) = \frac{p_k^2}{1 - p_k} < d", size=46)
        e2.next_to(e1, DOWN, buff=0.5).align_to(e1[1], LEFT)
        self.say("אותו פיתוח כמו בסעיף א, בלי להציב :\nהבא מקבל יותר כש-d(1 − pₖ) > pₖ².", FadeIn(e1))
        self.say("מחלקים ב-1 − pₖ, שהוא חיובי לכל\nמי שאינו האחרון, ומקבלים פונקציה f.", FadeIn(e2))
        der = TX(r"f'(p) = \frac{p\,(2 - p)}{(1 - p)^2} > 0", size=44, color=C.AMBER).move_to(DOWN * 1.2)
        self.say("‏f עולה : המונה p² גדל, המכנה 1 − p קטן,\nושניהם חיוביים. גם הנגזרת אומרת את זה.",
                 FadeIn(der))
        self.fade_all()

    def curve(self):
        ox, oy, W, H = -4.6, -1.95, 8.6, 4.4
        pmax, ymax = 0.45, 0.32

        def pt(p, y):
            return np.array([ox + W * p / pmax, oy + H * y / ymax, 0.0])

        ax = VGroup(Line(pt(0, 0), pt(pmax, 0), stroke_color=C.MUTED, stroke_width=3),
                    Line(pt(0, 0), pt(0, ymax), stroke_color=C.MUTED, stroke_width=3))
        ticks = VGroup()
        for p in (0.1, 0.2, 0.3, 0.4):
            ticks.add(M(f"{p:.1f}", 24, C.MUTED).next_to(pt(p, 0), DOWN, buff=0.15))
        for y in (0.1, 0.2, 0.3):
            ticks.add(M(f"{y:.1f}", 24, C.MUTED).next_to(pt(0, y), LEFT, buff=0.15))
        pl = TX("p", size=34, color=C.MUTED).next_to(pt(pmax, 0), RIGHT, buff=0.2)
        curve = VMobject(stroke_color=S1, stroke_width=5)
        ps = np.linspace(0, 0.43, 80)
        curve.set_points_smoothly([pt(p, f(p)) for p in ps])
        dline = DashedLine(pt(0, 0.1), pt(pmax, 0.1), stroke_color=C.AMBER, stroke_width=3)
        dlab = TX(r"y = d = 0.1", size=32, color=C.AMBER).next_to(pt(pmax, 0.1), UP, buff=0.15).shift(LEFT * 0.9)
        flab = TX(r"f(p) = \frac{p^2}{1 - p}", size=34, color=S1).move_to(pt(0.37, 0.28)).shift(LEFT * 1.6)
        self.say("כאן העקומה f(p), והקו המקווקו\nהוא y = d, כלומר 0.1 של סעיף א.",
                 FadeIn(ax), FadeIn(ticks), FadeIn(pl), Create(curve), Create(dline), FadeIn(dlab), FadeIn(flab),
                 run_time=1.8)
        dots = VGroup()
        for k, p, _, _ in ROWS[:5]:
            p = float(p)
            col = S1 if f(p) < 0.1 else (S2 if k == 4 else VTEXT)
            d = Dot(pt(p, f(p)), radius=0.11, color=col)
            lab = M(str(k), 24, col).next_to(d, LEFT if k < 4 else RIGHT, buff=0.12)
            dots.add(VGroup(d, lab))
        self.say("כל אדם הוא נקודה על העקומה, ב-pₖ שלו.\nהשברים עולים, ולכן הנקודות מטפסות.",
                 *[FadeIn(g, scale=1.5) for g in dots[:3]], lag_ratio=0.3)
        self.say("שלוש הראשונות מתחת לקו : החלקים עולים.\nהרביעית מעליו, וכל שאחריה גם.",
                 *[FadeIn(g, scale=1.5) for g in dots[3:]], lag_ratio=0.3)
        tdot = Dot(pt(T_A, 0.1), radius=0.09, color=C.AMBER)
        tlab = TX(r"T", size=34, color=C.AMBER).next_to(tdot, DOWN, buff=0.2)
        self.say("ברגע שהתנאי נכשל הוא נכשל לתמיד :\nפסגה אחת, בחיתוך T של העקומה והקו.",
                 FadeIn(tdot, scale=1.6), FadeIn(tlab))
        self.fade_all()

    def formula(self):
        t = TX(r"T = \frac{\sqrt{d^2 + 4d} - d}{2}", size=52, color=C.AMBER).move_to(UP * 2.0)
        self.say("החיתוך הוא השורש החיובי של\n‏p² + dp − d : הסף הכללי T.", FadeIn(t))
        k = TX(r"k = \max\left(1,\ \left\lceil \frac{T - a}{d} \right\rceil + 1\right)", size=48).move_to(UP * 0.2)
        self.say("הגדול הוא האדם הראשון שהשבר שלו\nמגיע לסף, ומזה יוצאת נוסחה ל-k.", FadeIn(k))
        chk = TX(r"\frac{0.2702 - 0.01}{0.1} = 2.60 \;\Rightarrow\; k = 3 + 1 = 4", size=42).move_to(DOWN * 1.4)
        self.say("בדיקה עם סעיף א : 2.60 מעוגל ל-3,\nועוד 1 : האדם הרביעי.", FadeIn(chk))
        self.say("האדם האחרון לוקח רק את השארית,\nאבל כש-d ≤ ½ זה לא משנה את התשובה.")
        self.fade_all()

    def tie(self):
        head = TX(r"a = d = \tfrac{1}{12}: \quad T = \frac{\tfrac{7}{12} - \tfrac{1}{12}}{2} = \tfrac14 = p_3",
                  size=44).move_to(UP * 2.75)
        self.say("ומתי יש תיקו? כשהשבר של מישהו\nשווה לסף בדיוק.")
        self.say("דוגמה : a = d = 1/12. הסף יוצא\nבדיוק רבע, וזה בדיוק p₃ = 3/12.", FadeIn(head))
        bars = Bars(TIE, x0=-5.2, gap=0.9, base=-1.95, scale=17.0, bw=0.56, label_size=24)
        cols = [S2 if k in (3, 4) else (S1 if k % 2 else S3) for k, *_ in TIE]
        bs = [bars.bar(k, c) for (k, *_), c in zip(TIE, cols)]
        both = M("55/288", 26, C.AMBER).next_to(VGroup(bs[2], bs[3]), UP, buff=0.14)
        self.say("ולכן השלישי והרביעי מקבלים בדיוק\nאותו חלק : 55/288 מהעוגה.",
                 FadeIn(bars.axis), *[GrowFromEdge(b, DOWN) for b in bs], FadeIn(both), run_time=1.8)
        self.fade_all()
        self.say("ומה אם d גדול מחצי? שם החיתוך של השבר\nהאחרון משנה את התמונה : בשאלות ההמשך.")

    def box(self):
        view = BoxView(QID, "proof", height=5.4).move_to(UP * 0.62)
        self.say("בתיבה, בשלב ההוכחה : כל אדם הוא נקודה\nעל העקומה, והפסגה היא הראשונה מעל הקו.", FadeIn(view))
        self.box_beat(view, [
            (1, "עם d = 0.25 הסף עולה ל-0.390,\nוהפסגה זזה לאדם השלישי."),
        ])
        self.fade_all()


class Closing(CakeScene):
    def construct(self):
        self.closing(QID, [("סעיף א", TX(r"k = 4, \quad S_4 \approx 0.2158", size=44)),
                           ("סעיף ב", TX(r"T = \frac{\sqrt{d^2 + 4d} - d}{2}", size=44))],
                     ["לסיכום : משווים כל אדם לבא אחריו,\nוהגדול הוא הראשון שמגיע לסף.",
                      "נסו a ו-d אחרים בתיבה\nשבעמוד של שאלה 0027 באתר."],
                     holds=(4.0, 4.5))
