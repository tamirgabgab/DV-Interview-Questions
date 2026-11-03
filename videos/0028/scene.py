"""The tutorial video of question 0028, a cake shared by fractions that grow as a geometric
sequence (script: script.md).

Render with `python videos/render.py 0028` (see VIDEOS.md). No code (the page has none):
the proof step by step instead, as in 0026. The cake is a strip, as in the page's figure:
each person cuts a slice of what is left, from the left, and under the strip a bar chart of
each person's share is built bar by bar up to the peak and past it. Part א on the page's
numbers (a = 0.01, q = 1.5): the 13 people, the shares S_k = p_k R_k, the ratio of two
neighbours q (1 - p_k), the threshold 1/3, the logarithm and the tenth person with about
0.170; the page's cake box from person 9 to 11. Part ב: the ratio chart (above 1 up to the
peak, below it after), one peak, the formula, the last person's cut, other q, the tie
(a = 0.25, q = 2) and the box's proof panel; q > 2 in one closing sentence.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, BoxView, DVQScene, M, TX, he, read_palette  # noqa: E402
import cake  # noqa: E402

QID = 28
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – הצבה מספרית"),
    ("ChapterB", "סעיף ב – המקרה הכללי"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="cake-geo", a = 0.01, q = 1.5). "play": the pie and the table,
# eight clicks on "the next person" before the first picture (person 9), then 10 and 11.
# "proof": the proof panel with every person, then a = 0.25 and q = 2 (the tie).
BOXES = {
    "play": {"box": 0, "region": [".ex-play-row", ".cake-box"], "width": 760,
             "steps": [
                 [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]], [["click", ".ex-next"]], [["click", ".ex-next"]],
                 [["click", ".ex-all"]]]},
    "proof": {"box": 0, "region": [".cake-proof"], "steps": [[["click", ".ex-all"]]]},
    "tie": {"box": 0, "region": [".cake-proof"],
            "steps": [[["fill", ".num-a", "0.25"], ["fill", ".num-step", "2"], ["click", ".ex-all"]]]},
}

_S = read_palette()["slate"]
SL1, SL2, PEAK, REST = _S["--viz-s1"], _S["--viz-s3"], _S["--viz-s2"], C.NAVY_LIGHT

# ---- the numbers, all from the page's reference (tools/figures/cake.py) --------------------

A, Q = Fr(1, 100), Fr(3, 2)
ROWS = cake.split(cake.GEO, A, Q)                     # (k, p, R, S), exact
assert len(ROWS) == 13 and ROWS[-1][1] == 1
PEAKS, TOP = cake.best(ROWS)
assert PEAKS == [10] and cake.formula(cake.GEO, A, Q) == 10
P = {k: p for k, p, _, _ in ROWS}
R = {k: r for k, _, r, _ in ROWS}
S = {k: s for k, _, _, s in ROWS}
assert round(float(S[10]), 4) == 0.1697 and round(float(R[10]), 4) == 0.4415
assert round(float(P[10]), 4) == 0.3844 and round(float(P[9]), 4) == 0.2563
assert P[9] < Fr(1, 3) <= P[10] and 1 - Q ** -1 == Fr(1, 3)
assert all(S[k + 1] > S[k] for k in range(1, 10)) and all(S[k + 1] < S[k] for k in range(10, 13))
assert 1 - R[10] < Fr(3, 5)                           # the first nine take less than 60 %
LOG50 = math.log(50) / math.log(1.5)
assert round(LOG50, 2) == 9.65 and math.ceil(LOG50) == 10
assert math.ceil(math.log(100) / math.log(1.5)) + 1 == 13 and round(float(S[13]), 4) == 0.0155
RATIO = {k: Q * (1 - P[k]) for k in range(1, 12)}    # S(k+1) / S(k), k + 1 not the last
assert all(RATIO[k] == S[k + 1] / S[k] for k in RATIO)
assert all(RATIO[k] > 1 for k in range(1, 10)) and all(RATIO[k] < 1 for k in range(10, 12))
assert round(float(RATIO[9]), 3) == 1.116 and round(float(RATIO[10]), 3) == 0.923
# the statement's example: a = 0.1, q = 2, five people, the fifth takes the rest
STATEMENT = cake.split(cake.GEO, Fr(1, 10), Fr(2))
assert [p for _, p, _, _ in STATEMENT] == [Fr(1, 10), Fr(1, 5), Fr(2, 5), Fr(4, 5), 1]
# other q with a = 0.01 (the page's table)
OTHER = {}
for q in (Fr(2), Fr(3, 2), Fr(11, 10)):
    pk, top = cake.best(cake.split(cake.GEO, A, q))
    OTHER[q] = (pk[0], top, math.log(float((q - 1) / A)) / math.log(float(q)))
assert OTHER[Fr(2)][0] == 7 and round(float(OTHER[Fr(2)][1]), 3) == 0.313
assert OTHER[Fr(11, 10)][0] == 25 and round(float(OTHER[Fr(11, 10)][1]), 3) == 0.040
assert round(OTHER[Fr(2)][2], 2) == 6.64 and round(OTHER[Fr(11, 10)][2], 2) == 24.16
# the tie: a = 0.25, q = 2
TIE = cake.split(cake.GEO, Fr(1, 4), Fr(2))
assert [s for _, _, _, s in TIE] == [Fr(1, 4), Fr(3, 8), Fr(3, 8)] and cake.best(TIE)[0] == [2, 3]
assert (Fr(2) - 1) / Fr(1, 4) == 4 == 2 ** 2 and TIE[1][1] == Fr(1, 2) == 1 - Fr(1, 2)


def f4(x) -> str:
    return f"{float(x):.4f}"


# ---- the cake strip and the bar chart -------------------------------------------------------

STRIP_X0, STRIP_W = -5.6, 11.2


class Strip(VGroup):
    """The cake as a strip: the whole cake (what is left) and the slices cut from the left."""

    def __init__(self, rows, y: float = 2.8, h: float = 0.62, peak=()):
        super().__init__()
        self.rows, self.y, self.h, self.peak = rows, y, h, set(peak)
        self.body = Rectangle(width=STRIP_W, height=h, stroke_color=C.MUTED, stroke_width=2,
                              fill_color=REST, fill_opacity=1).move_to([STRIP_X0 + STRIP_W / 2, y, 0])
        self.add(self.body)
        self.slices = {}

    def slice(self, k: int, highlight: bool = True) -> Rectangle:
        _, p, r, s = self.rows[k - 1]
        x0 = STRIP_X0 + STRIP_W * float(1 - r)
        w = max(STRIP_W * float(s), 0.012)
        color = PEAK if (highlight and k in self.peak) else (SL1 if k % 2 else SL2)
        rect = Rectangle(width=w, height=self.h, stroke_color=C.NAVY, stroke_width=1.5 if w > 0.1 else 0,
                         fill_color=color, fill_opacity=0.9).move_to([x0 + w / 2, self.y, 0])
        self.slices[k] = rect
        return rect


class Bars(VGroup):
    """A bar per person: its share (or another value), against a y axis with a few ticks."""

    def __init__(self, values: dict, vmax: float, ticks, origin=(-5.2, -1.85), width=10.6,
                 height=3.05, peak=(), fmt="{:.2f}", label_size=24):
        super().__init__()
        self.values, self.vmax, self.peak = values, vmax, set(peak)
        self.ox, self.oy, self.w, self.h = origin[0], origin[1], width, height
        n = len(values)
        self.slot = width / n
        axis = Line(self.pt(0, 0), self.pt(n, 0), stroke_color=C.MUTED, stroke_width=3)
        yax = Line(self.pt(0, 0), self.pt(0, vmax), stroke_color=C.MUTED, stroke_width=3)
        tk = VGroup()
        for v in ticks:
            tk.add(Line(self.pt(0, v), self.pt(0, v) + LEFT * 0.1, stroke_color=C.MUTED, stroke_width=2))
            tk.add(M(fmt.format(v), 22, C.MUTED).next_to(self.pt(0, v), LEFT, buff=0.18))
        names = VGroup(*[M(str(k), label_size, C.MUTED).move_to(self.center(k) + DOWN * 0.27)
                         for k in values])
        self.axes = VGroup(axis, yax, tk, names)
        self.add(self.axes)
        self.bars = {}

    def pt(self, i: float, v: float) -> np.ndarray:
        return np.array([self.ox + self.slot * i, self.oy + self.h * v / self.vmax, 0.0])

    def center(self, k: int) -> np.ndarray:
        keys = list(self.values)
        return self.pt(keys.index(k) + 0.5, 0)

    def bar(self, k: int, color: str | None = None) -> Rectangle:
        v = float(self.values[k])
        hh = max(self.h * v / self.vmax, 0.02)
        col = color or (PEAK if k in self.peak else SL1)
        rect = Rectangle(width=self.slot * 0.62, height=hh, stroke_width=0, fill_color=col,
                         fill_opacity=0.95)
        rect.move_to(self.center(k) + UP * hh / 2)
        self.bars[k] = rect
        return rect

    def hline(self, v: float, color=C.WHITE) -> DashedLine:
        n = len(self.values)
        return DashedLine(self.pt(0, v), self.pt(n, v), stroke_color=color, stroke_width=2.5,
                          dash_length=0.12)


def readout(k: int, rows) -> Text:
    _, p, r, s = rows[k - 1]
    pp = "1" if p == 1 else f4(p)
    return M(f"k = {k:<2}  p = {pp:<6}  R = {f4(r)}  S = {f4(s)}", 26, C.WHITE)


class CakeScene(DVQScene):
    """Helpers shared by the scenes of 0028."""

    def cut(self, strip: Strip, bars: Bars | None, rows, ks, ro_pos, ro=None, per: float = 0.85):
        """Cut the slices of the people `ks`, one after another, each with its bar."""
        for k in ks:
            sl = strip.slice(k)
            anims = [GrowFromEdge(sl, LEFT)]
            if bars is not None:
                anims.append(GrowFromEdge(bars.bar(k), DOWN))
            new = readout(k, rows).move_to(ro_pos)
            anims.append(FadeIn(new) if ro is None else Transform(ro, new))
            self.play(*anims, run_time=per)
            if ro is None:
                ro = new
        return ro


class Opening(CakeScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "חלוקת עוגה בסדרה הנדסית",
                     ["א · ‏a = 0.01, q = 1.5", "ב · המקרה הכללי"],
                     ["שאלה 0028 : חלוקת עוגה בסדרה הנדסית,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : הצבה מספרית,\nואז המקרה הכללי עם הוכחה."])
        self.fade_all()
        seq = TX(r"p_k = a\,q^{\,k-1}", size=54).move_to(UP * 1.6)
        self.say("כמו בשאלה 0027, אבל עכשיו השבר\nגדל פי q, ולא בתוספת קבועה.", Write(seq))
        strip = Strip(STATEMENT, y=0.2, h=0.8)
        self.say("עוגה בגודל 1. כל אחד בתורו חותך\nשבר p_k ממה שנשאר, לא מהעוגה כולה.",
                 FadeIn(strip), run_time=1.0)
        fracs = VGroup(*[M(("1" if p == 1 else f"{float(p):g}"), 28, SL1 if k % 2 else SL2)
                         for k, p, _, _ in STATEMENT])
        with self.beat("דוגמה עם a = 0.1 ו-q = 2 : השברים\n‏0.1, 0.2, 0.4, 0.8, והחמישי לוקח את השארית."):
            for k, p, r, s in STATEMENT:
                sl = strip.slice(k)
                fracs[k - 1].move_to(sl.get_center() + DOWN * 0.85)
                self.play(GrowFromEdge(sl, LEFT), FadeIn(fracs[k - 1]), run_time=0.7)
        self.say("השבר גדל, אבל מה שנשאר לחתוך ממנו\nקטן. מי מקבל את החלק הגדול ביותר?")
        self.fade_all()


class ChapterA(CakeScene):
    def construct(self):
        self.chapter_card("סעיף א", "הצבה מספרית",
                          "סעיף א : a = 0.01 ו-q = 1.5. השברים\n‏0.01, 0.015, 0.0225, כל אחד פי 1.5.")
        self.shares()
        self.ratio()
        self.threshold()
        self.box()

    def shares(self):
        strip = Strip(ROWS, peak=PEAKS)
        bars = Bars({k: S[k] for k in range(1, 14)}, 0.18, [0, 0.05, 0.10, 0.15], peak=PEAKS)
        ro_pos = [0, 1.85, 0]
        self.say("למעלה העוגה, ולמטה גרף : החלק\nשכל אחד מקבל, עמודה לכל אדם.",
                 FadeIn(strip), FadeIn(bars.axes), run_time=1.0)
        with self.beat("חמשת הראשונים לוקחים פרוסות דקות :\nהשבר קטן, והעוגה כמעט שלמה."):
            ro = self.cut(strip, bars, ROWS, range(1, 6), ro_pos)
        with self.beat("השבר ממשיך לגדול פי 1.5, והעמודות\nעולות. עד האדם התשיעי כל אחד מקבל יותר."):
            self.cut(strip, bars, ROWS, range(6, 10), ro_pos, ro)
        with self.beat("האדם העשירי לוקח 0.3844 ממה שנשאר,\nומקבל 0.1697 : העמודה הגבוהה ביותר."):
            self.cut(strip, bars, ROWS, [10], ro_pos, ro, per=1.0)
        with self.beat("אחריו השבר גדול, אבל נשאר מעט.\nהעמודות יורדות, והאדם ה-13 לוקח את השארית."):
            self.cut(strip, bars, ROWS, range(11, 14), ro_pos, ro)
        self.say("תשעת הראשונים לקחו יחד פחות מ-60%\nמהעוגה, ומשם השבר קופץ מהר.")
        self.say("מלכודת : לאחרון יש השבר הגדול ביותר,\nכל השארית. אבל נשאר לו רק 0.0155.",
                 bars.bars[13].animate.set_fill(C.AMBER), strip.slices[13].animate.set_fill(C.AMBER),
                 FadeIn(M("0.0155", 24, C.AMBER).next_to(bars.bars[13], UP, buff=0.12)), run_time=1.0)
        self.fade_all()

    def ratio(self):
        l1 = TX(r"S_k = p_k\,R_k", r"\qquad", r"R_{k+1} = (1 - p_k)\,R_k", size=46)
        l1.move_to(UP * 2.3)
        self.say("סימון : R_k הוא מה שנשאר לפני האדם ה-k.\nהוא לוקח p_k ממנו, והשאר עובר הלאה.",
                 Write(l1), run_time=1.4)
        l2 = TX(r"\frac{S_{k+1}}{S_k} = \frac{p_{k+1}\,(1 - p_k)}{p_k}", size=46)
        l3 = TX(r"= \frac{q\,p_k\,(1 - p_k)}{p_k} = q\,(1 - p_k)", size=46, color=C.AMBER)
        l2.move_to(UP * 0.85)
        l3.next_to(l2, DOWN, buff=0.3).align_to(l2[0], LEFT).shift(RIGHT * 1.15)
        self.say("משווים שני שכנים : מה שנשאר מצטמצם,\nועם p_{k+1} = q·p_k מצטמצם גם השבר.",
                 FadeIn(l2))
        self.say("נשאר יחס פשוט מאוד : q כפול 1 − p_k.\nהוא לא תלוי בכלל במה שנשאר.", FadeIn(l3))
        l4 = TX(r"S_{k+1} > S_k \iff q\,(1 - p_k) > 1 \iff p_k < 1 - \frac{1}{q} = \frac13",
                size=42).move_to(DOWN * 1.95)
        self.say("האדם הבא מקבל יותר בדיוק כשהיחס\nגדול מ-1, כלומר כשהשבר מתחת לשליש.",
                 FadeIn(l4))
        self.fade_all()

    def threshold(self):
        bars = Bars({k: P[k] for k in range(1, 13)}, 1.0, [0, 0.25, 0.5, 0.75, 1.0],
                    origin=(-5.0, -1.85), width=10.4, height=4.2, fmt="{:.2f}")
        for k in range(1, 13):
            bars.bar(k, PEAK if k == 10 else (SL1 if k < 10 else C.MUTED))
        line = bars.hline(1 / 3, C.WHITE)
        tag = TX(r"T = \tfrac13", size=34).next_to(line, RIGHT, buff=0.15)
        self.say("כאן כל עמודה היא השבר של אדם,\nוהקו המקווקו הוא הסף שליש.",
                 FadeIn(bars.axes), Create(line), FadeIn(tag), run_time=1.0)
        with self.beat("תשעה שברים מתחת לסף : אחרי כל אחד\nמהם בא מישהו שמקבל יותר."):
            self.play(LaggedStart(*[GrowFromEdge(bars.bars[k], DOWN) for k in range(1, 10)],
                                  lag_ratio=0.15), run_time=1.8)
        with self.beat("השבר העשירי הוא הראשון שעובר את הסף.\nאחריו כל השברים מעליו."):
            self.play(GrowFromEdge(bars.bars[10], DOWN), run_time=0.7)
            self.play(*[GrowFromEdge(bars.bars[k], DOWN) for k in (11, 12)], run_time=0.8)
        self.fade_all()

        e1 = TX(r"0.01 \cdot 1.5^{\,k-1} \ge \tfrac13", size=46)
        e2 = TX(r"\iff 1.5^{\,k} \ge 50", size=46)
        e3 = TX(r"\iff k \ge \log_{1.5} 50 \approx 9.65", size=46)
        col = VGroup(e1, e2, e3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 1.6)
        self.say("מי עובר את הסף? כופלים ב-q חלקי a,\nכי 0.5 חלקי 0.01 הוא 50.", FadeIn(e1), FadeIn(e2))
        k10 = TX(r"k = \lceil 9.65 \rceil = 10", size=50, color=C.AMBER).next_to(col, DOWN, buff=0.45)
        self.say("לוקחים לוגריתם בבסיס 1.5 ומעגלים\nלמעלה : האדם העשירי.", FadeIn(e3), FadeIn(k10))
        wrong = TX(r"0.01 \cdot 1.5^{\,k-1} \ge 1 \;\Rightarrow\; k = \lceil \log_{1.5} 100 \rceil + 1 = 13",
                   size=42, color=C.RED).next_to(k10, DOWN, buff=0.45)
        self.say("מלכודת : סף 1 במקום שליש מוצא את\nהאחרון, שלוקח את השארית : 13 במקום 10.",
                 FadeIn(wrong))
        self.play(FadeOut(col), FadeOut(k10), FadeOut(wrong), run_time=0.6)
        c1 = TX(r"p_9 \approx 0.256 < \tfrac13 \;\Rightarrow\; S_{10} > S_9", size=44)
        c2 = TX(r"p_{10} \approx 0.384 \ge \tfrac13 \;\Rightarrow\; S_{11} < S_{10}", size=44)
        c3 = TX(r"S_{10} = p_{10}\,R_{10} \approx 0.3844 \cdot 0.4415 \approx 0.1697", size=46,
                color=C.AMBER)
        VGroup(c1, c2, c3).arrange(DOWN, buff=0.5).move_to(UP * 1.0)
        self.say("בדיקה ישירה : השבר התשיעי מתחת לסף,\nוהעשירי כבר מעליו.", FadeIn(c1), FadeIn(c2))
        self.say("והחלק שלו : 0.3844 מתוך 0.4415\nשנשארו, כלומר בערך 17% מהעוגה.", FadeIn(c3))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "play", height=5.6).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד : העוגה\nועד עכשיו תשעה אנשים בטבלה.", FadeIn(view))
        self.box_beat(view, [
            (1, "האדם הבא : העשירי חותך 0.3844\nממה שנשאר, ומקבל 0.1697."),
            (2, "והאחד-עשר מקבל פחות, 0.1567.\nהפסגה היא האדם העשירי."),
            (3, "וכולם : אחרי העשירי החלקים רק\nיורדים, עד 0.0155 של האחרון."),
        ])
        self.fade_all()


class ChapterB(CakeScene):
    def construct(self):
        self.chapter_card("סעיף ב", "המקרה הכללי",
                          "סעיף ב : a ו-q כלשהם, עם 1 < q ≤ 2.\nמי מקבל הכי הרבה, ולמה יש פסגה אחת?")
        self.one_peak()
        self.formula()
        self.tie()
        self.box()

    def one_peak(self):
        n = 11
        ox, oy, w, h, vmax = -5.0, -1.85, 10.2, 4.0, 1.6
        def pt(i, v):
            return np.array([ox + w * i / (n + 1), oy + h * v / vmax, 0.0])
        axis = Line(pt(0, 0), pt(n + 1, 0), stroke_color=C.MUTED, stroke_width=3)
        yax = Line(pt(0, 0), pt(0, vmax), stroke_color=C.MUTED, stroke_width=3)
        ticks = VGroup()
        for v in (0, 0.5, 1.0, 1.5):
            ticks.add(M(f"{v:.1f}", 22, C.MUTED).next_to(pt(0, v), LEFT, buff=0.18))
        names = VGroup(*[M(str(k), 24, C.MUTED).move_to(pt(k, 0) + DOWN * 0.27) for k in range(1, n + 1)])
        one = DashedLine(pt(0, 1), pt(n + 1, 1), stroke_color=C.WHITE, stroke_width=2.5, dash_length=0.12)
        one_tag = TX(r"y = 1", size=32).next_to(one, RIGHT, buff=0.15)
        head = TX(r"\frac{S_{k+1}}{S_k} = q\,(1 - p_k)", size=44).move_to([2.2, 2.7, 0])
        self.say("היחס בין שכנים, q(1 − p_k), לא תלוי\nבמספרים של סעיף א. כאן הוא בגרף, נקודה לכל k.",
                 FadeIn(VGroup(axis, yax, ticks, names)), Create(one), FadeIn(one_tag), FadeIn(head),
                 run_time=1.2)
        dots = VGroup(*[Dot(pt(k, float(RATIO[k])), radius=0.1,
                            color=PEAK if k == 10 else (SL1 if k < 10 else C.MUTED)) for k in range(1, n + 1)])
        with self.beat("השברים עולים, ולכן היחס רק יורד.\nתשע נקודות מעל הקו : החלקים עולים."):
            self.play(LaggedStart(*[FadeIn(dots[k - 1], scale=1.6) for k in range(1, 10)], lag_ratio=0.2),
                      run_time=2.0)
        with self.beat("הנקודה של האדם העשירי היא הראשונה\nמתחת לקו, וכל מה שאחריה נשאר מתחת."):
            self.play(FadeIn(dots[9], scale=1.8), run_time=0.6)
            self.play(FadeIn(dots[10], scale=1.6), run_time=0.5)
        self.say("לכן יש פסגה אחת : החלקים עולים\nעד האדם הראשון שיורד לקו, ואחריו רק יורדים.")
        self.fade_all()

    def formula(self):
        t = TX(r"q\,(1 - p) = 1 \iff p = T = 1 - \frac{1}{q}", size=46).move_to(UP * 2.3)
        self.say("הסף הוא הנקודה שבה היחס שווה ל-1 :\n‏T = 1 − 1/q. שליש עבור q = 1.5.", FadeIn(t))
        e1 = TX(r"a\,q^{\,k-1} \ge \frac{q - 1}{q} \iff q^{k} \ge \frac{q - 1}{a}", size=44)
        e2 = TX(r"k = \max\left(1,\ \left\lceil \log_q \frac{q - 1}{a} \right\rceil\right)", size=50,
                color=C.AMBER)
        VGroup(e1, e2).arrange(DOWN, buff=0.55).move_to(DOWN * 0.15)
        self.say("מי עובר את הסף : כופלים ב-q חלקי a\nולוקחים לוגריתם בבסיס q.", FadeIn(e1))
        self.say("והנוסחה : האדם הראשון שהשבר שלו\nמגיע לסף. אם a כבר מעליו, זה הראשון.", FadeIn(e2))
        self.fade_all()
        last = TX(r"\frac{S_L}{S_{L-1}} = \frac{1 - p_{L-1}}{p_{L-1}}", size=46).move_to(UP * 1.9)
        self.say("והאחרון? השבר שלו נחתך ל-1, ולכן\nהיחס אליו הוא 1 − p חלקי p, ולא q(1 − p).",
                 FadeIn(last))
        cap = TX(r"T = 1 - \frac{1}{q} \le \frac12 \quad (q \le 2)", size=46).move_to(DOWN * 0.2)
        self.say("כש-q ≤ 2 הסף לכל היותר חצי. מתחת\nלסף היחס הזה גדול מ-1, כמו שהתנאי אומר.",
                 FadeIn(cap))
        self.say("ומעל הסף החיתוך רק מקטין את היחס.\nבשני המקרים התשובה לא משתנה.")
        self.fade_all()
        rows = [("q", "T", "log", "k", "S")]
        for q in (Fr(2), Fr(3, 2), Fr(11, 10)):
            k, top, lg = OTHER[q]
            rows.append((cake.short(q), f"{float(1 - 1 / q):.3f}", f"{lg:.2f}", str(k), f"{float(top):.3f}"))
        table = VGroup()
        widths = [1.6, 2.0, 2.0, 1.4, 1.8]
        for r_i, row in enumerate(rows):
            x = -sum(widths) / 2
            for c_i, cell in enumerate(row):
                col = C.MUTED if r_i == 0 else (C.AMBER if row[0] == "1.5" else C.WHITE)
                txt = M(cell, 32, col).move_to([x + widths[c_i] / 2, 1.6 - 0.85 * r_i, 0])
                table.add(txt)
                x += widths[c_i]
        rule = Line([-4.4, 1.18, 0], [4.4, 1.18, 0], stroke_color=C.FAINT, stroke_width=2)
        self.say("עם a = 0.01 ו-q אחרים : q = 2 נותן\nאת האדם השביעי, עם 0.313 מהעוגה.",
                 FadeIn(table[:10]), Create(rule))
        self.say("ככל ש-q קרוב ל-1, הפסגה מאוחרת יותר,\nנמוכה ושטוחה : עם 1.1, האדם ה-25.",
                 FadeIn(table[10:]))
        self.fade_all()

    def tie(self):
        head = TX(r"a = 0.25,\quad q = 2:\qquad \frac{q - 1}{a} = 4 = 2^2", size=44).move_to(UP * 3.0)
        self.say("ומתי יש תיקו? כש-q^k שווה בדיוק\nל-(q − 1)/a. למשל a = 0.25 ו-q = 2.",
                 FadeIn(head))
        strip = Strip(TIE, y=1.9, h=0.62, peak=[2, 3])
        bars = Bars({k: s for k, _, _, s in TIE}, 0.4, [0, 0.1, 0.2, 0.3, 0.4], origin=(-3.2, -1.85),
                    width=6.4, height=2.9, peak=[2, 3], fmt="{:.1f}")
        self.play(FadeIn(strip), FadeIn(bars.axes), run_time=0.8)
        with self.beat("השבר השני הוא בדיוק חצי, הסף.\nהשני והשלישי מקבלים 0.375 כל אחד."):
            for k in (1, 2, 3):
                self.play(GrowFromEdge(strip.slice(k), LEFT), GrowFromEdge(bars.bar(k), DOWN),
                          run_time=0.7)
        self.play(*[FadeOut(m) for m in (strip, bars, *bars.bars.values(), *strip.slices.values())],
                  run_time=0.6)
        lg = TX(r"\log_2 \frac{q - 1}{a} = \log_2 4 = 2", size=48, color=C.AMBER).move_to(UP * 0.6)
        self.say("כאן הלוגריתם יוצא מספר שלם. מחשבון\nשמחזיר 2.0000001 יעגל ל-3, ויפספס את התיקו.", FadeIn(lg))
        self.say("לכן כשהלוגריתם קרוב לשלם, בודקים\nישירות את q^k מול (q − 1)/a.")
        self.fade_all()

    def box(self):
        view = BoxView(QID, "proof", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד, בשלב ההוכחה, כל אדם\nהוא נקודה על הקו q(1 − p), מול הקו y = 1.",
                 FadeIn(view))
        self.play(FadeOut(view), run_time=0.5)
        view = BoxView(QID, "tie", height=5.6).move_to(UP * 0.62)
        self.say("ועם a = 0.25 ו-q = 2, הנקודה השנייה\nנוגעת בקו בדיוק : תיקו עם השלישי.", FadeIn(view))
        self.say("כש-q גדול מ-2 האחרון יכול לשבור את\nהנוסחה. שאלות ההמשך בעמוד מראות מתי.")
        self.fade_all()


class Closing(CakeScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"k = 10,\quad S_{10} \approx 0.170", size=40)),
                           ("ב", TX(r"k = \max\left(1,\ \left\lceil \log_q \frac{q - 1}{a} \right\rceil\right)",
                                    size=40))],
                     ["לסיכום : היחס בין שכנים הוא q(1 − p_k),\nוהפסגה אצל הראשון שעובר את 1 − 1/q.",
                      "נסו a ו-q משלכם בתיבה\nשבעמוד של שאלה 0028 באתר."])
