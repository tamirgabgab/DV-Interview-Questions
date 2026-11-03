"""The tutorial video of question 0048, the farmer, the food and the water (script: script.md).

Render with `python videos/render.py 0048` (see VIDEOS.md). No code in this question's video
(the owner, 2026-11-02): every part is the reflection, drawn.

Part א works with the page's numbers L = 7, H = 3, a = 1, b = 2. First three routes that are
not the shortest, with their lengths (10.04, 10.30, 11.08), then the double reflection: the
cow through the water line (B' = (7, -2)), then B' through the food line (B'' = (7, 8)), the
first route unfolded leg by leg into a broken line from A to B'' of the same length, and the
straight line A -> B'' (D = 7, z = sqrt(98) = 9.90). Folding it back gives the stops: it
rises 2, 3 and 2, so x = 2, y = 3, w = 2.

Part ב runs the same picture backwards: the straight line through the food stop at L/3 and
the image of the water stop at 2L/3 rises H on every third, so it starts at height 0 and
ends at 3H = 2H + b: a = 0, b = H; folded back, three congruent legs.

Part ג tilts the food line by theta about (0, H). The two reflections are a rotation about
the meeting point O by 2 theta (the page's example theta = 15: B2 = (3.56, 10.83), z =
10.456, P = (0.80, 3.22), Q = (4.62, 0)). Then theta rises from 0 to 60 with the route and
its length updating, the turn 2 theta + beta - alpha <= 3 theta <= 180 beside it, and the
page's box in mode c. Every number is the page generator's (tools/figures/q0048.py).
"""

import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, BoxView, DVQScene, M, TX, he, read_palette  # noqa: E402

import q0048  # noqa: E402

QID = 48
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – החוואי בשליש הגובה והפרה בשני שלישים"),
    ("ChapterB", "סעיף ב – העצירות בשליש ובשני שלישים"),
    ("ChapterC", "סעיף ג – קו האוכל נוטה בזווית"),
    ("Closing", "סיכום"),
]

# The page's second box (mode c, theta = 15): the reflection shown, then theta at 30 and 45.
BOXES = {
    "tilt": {"box": 1, "region": [".farm-th", ".ex-summary", ".farm-live"],
             "hide": [".farm-note", ".farm-drag", ".farm-table", ".viz-legend"],
             "steps": [[["check", ".ex-refl", True]], [["set", ".ex-trange", "30"]],
                       [["set", ".ex-trange", "45"]]]},
}

_S = read_palette()["slate"]
FOOD, WATER = _S["--viz-s3"], _S["--viz-s1"]
COW, FARMER, PATH = C.ORANGE, C.WHITE, C.AMBER
FACE = C.NAVY_LIGHT

# ---- the numbers, from the page's generator ----------------------------------------------

L, H, A_H, B_H = 7, 3, 1, 2
SH = q0048.shortest(L, H, A_H, B_H)
assert (SH["x"], SH["y"], SH["w"], SH["D"]) == (2, 3, 2, 7)
assert round(SH["z"], 2) == 9.90 and SH["z"] ** 2 - 98 < 1e-9
ROUTES = [(3, 5), (1, 6), (4, 4)]
LENS = [q0048.length(L, H, A_H, B_H, p1, p2) for p1, p2 in ROUTES]
assert [f"{v:.2f}" for v in LENS] == ["10.04", "10.30", "11.08"]
assert all(v > SH["z"] for v in LENS)
# part ב: stops at L/3 and 2L/3
assert q0048.heights(L, H, F(L, 3), F(L, 3)) == (0, 3)
SB = q0048.shortest(L, H, 0, 3)
assert (SB["x"], SB["y"], SB["w"], SB["D"]) == (F(7, 3), F(7, 3), F(7, 3), 9)
# part ג: the page's example, theta = 15
T15 = q0048.tilted(L, H, A_H, B_H, 15)
assert [f"{v:.2f}" for v in T15["B2"]] == ["3.56", "10.83"] and f"{T15['z']:.3f}" == "10.456"
assert [f"{v:.2f}" for v in T15["P"]] == ["0.80", "3.22"] and f"{T15['Q'][0]:.2f}" == "4.62"
assert f"{T15['O'][0]:.2f}" == "-11.20" and f"{T15['turn']:.2f}" == "31.17"
THETAS = {t: q0048.tilted(L, H, A_H, B_H, t) for t in (0, 15, 27, 28, 45, 60)}
assert f"{THETAS[0]['z']:.2f}" == "9.90" and f"{THETAS[45]['z']:.2f}" == "10.30"
assert f"{THETAS[60]['z']:.2f}" == "9.60" and f"{THETAS[60]['turn']:.1f}" == "102.9"
assert THETAS[27]["sf"] > 0 > THETAS[28]["sf"]          # the food stop passes left of A near 27.2
ZMAX = max(q0048.tilted(L, H, A_H, B_H, t / 10)["z"] for t in range(0, 601))
assert f"{ZMAX:.1f}" == "10.6"
assert all(q0048.tilted(L, H, A_H, B_H, t)["turn"] <= 3 * t + 1e-9 for t in range(1, 61))


# ---- drawing helpers -------------------------------------------------------------------------

class Plane:
    """Model coordinates (the page's x, y) to the frame: origin at (ox, oy), k units each."""

    def __init__(self, ox: float, oy: float, k: float):
        self.ox, self.oy, self.k = ox, oy, k

    def p(self, x, y) -> np.ndarray:
        return np.array([self.ox + self.k * float(x), self.oy + self.k * float(y), 0.0])


def dashed(pl: Plane, x0, y0, x1, y1, color, width=4, opacity=1.0) -> DashedLine:
    return DashedLine(pl.p(x0, y0), pl.p(x1, y1), dash_length=0.16, dashed_ratio=0.6,
                      stroke_color=color, stroke_width=width, stroke_opacity=opacity)


def band(pl: Plane, y0, y1, x0=0, x1=L, opacity=0.55) -> Polygon:
    return Polygon(pl.p(x0, y0), pl.p(x1, y0), pl.p(x1, y1), pl.p(x0, y1), stroke_width=0,
                   fill_color=FACE, fill_opacity=opacity)


def dot(pl: Plane, x, y, color, r=0.1) -> Dot:
    return Dot(pl.p(x, y), radius=r, color=color)


def label(tex: str, at: np.ndarray, direction, color=C.WHITE, size=34, buff=0.12) -> MathTex:
    return TX(tex, size=size, color=color).next_to(at, direction, buff=buff)


def poly(pl: Plane, pts, color=PATH, width=6) -> VMobject:
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([pl.p(*q) for q in pts])


def strip(pl: Plane, x0=-0.6, x1=L + 0.6, names=True) -> Group:
    """The field between the water line (y = 0) and the food line (y = H)."""
    g = Group(band(pl, 0, H, x0, x1), dashed(pl, x0, H, x1, H, FOOD), dashed(pl, x0, 0, x1, 0, WATER))
    if names:
        g.add(he("קו האוכל", 28, FOOD, 600).next_to(pl.p(x1, H), RIGHT, buff=0.15),
              he("קו המים", 28, WATER, 600).next_to(pl.p(x1, 0), RIGHT, buff=0.15))
    return g


def route(p1, p2, a=A_H, b=B_H):
    return [(0, a), (p1, H), (p2, 0), (L, b)]


class FarmScene(DVQScene):
    """Helpers shared by the chapters of 0048."""

    def people(self, pl: Plane, a=A_H, b=B_H, size=34):
        fa, cb = dot(pl, 0, a, FARMER, 0.11), dot(pl, L, b, COW, 0.11)
        la = label("A", fa.get_center(), LEFT, FARMER, size)
        lb = label("B", cb.get_center(), RIGHT, COW, size)
        return VGroup(fa, la), VGroup(cb, lb)


# ---- the scenes ------------------------------------------------------------------------------

class Opening(FarmScene):
    def construct(self):
        self.opening(QID, "סטודנט", "החוואי, האוכל והמים",
                     ["א · שליש ושני שלישים", "ב · הבעיה ההפוכה", "ג · קו אוכל נטוי"],
                     ["שאלה 0048 : החוואי, האוכל והמים,\nשאלה ברמת סטודנט.",
                      "שלושה סעיפים : הגבהים נתונים,\nהבעיה ההפוכה, וקו אוכל נטוי."])
        self.fade_all()
        pl = Plane(-4.2, -1.5, 1.0)
        field = strip(pl)
        hh = VGroup(Line(pl.p(-1.0, 0), pl.p(-1.0, H), stroke_color=C.MUTED, stroke_width=2),
                    TX("H", size=34, color=C.MUTED).next_to(pl.p(-1.0, H / 2), LEFT, buff=0.12))
        self.say("שני קווים מקבילים : למעלה אוכל,\nלמטה מים, והמרחק ביניהם H.",
                 FadeIn(field), FadeIn(hh), run_time=1.2)
        a, b = self.people(pl)
        ha = VGroup(Line(pl.p(0.35, 0), pl.p(0.35, A_H), stroke_color=FARMER, stroke_width=2),
                    TX("a", size=32).next_to(pl.p(0.35, A_H / 2), RIGHT, buff=0.08))
        hb = VGroup(Line(pl.p(L - 0.35, 0), pl.p(L - 0.35, B_H), stroke_color=COW, stroke_width=2),
                    TX("b", size=32, color=COW).next_to(pl.p(L - 0.35, B_H / 2), LEFT, buff=0.08))
        ll = VGroup(Line(pl.p(0, -0.45), pl.p(L, -0.45), stroke_color=C.MUTED, stroke_width=2),
                    TX("L", size=34, color=C.MUTED).next_to(pl.p(L / 2, -0.45), DOWN, buff=0.1))
        self.say("החוואי A בגובה a, הפרה B בגובה b,\nוהמרחק האופקי ביניהם L.",
                 FadeIn(a), FadeIn(b), FadeIn(ha), FadeIn(hb), FadeIn(ll))
        path = poly(pl, route(3, 5))
        self.say("בדרך לפרה הוא לוקח קודם אוכל,\nאחר כך מים, ומשם ישר אל הפרה.", Create(path),
                 run_time=1.6)
        self.say("כל קטע הוא קו ישר. מה הדרך\nהקצרה ביותר, ואיפה עוצרים?")
        self.fade_all()


class ChapterA(FarmScene):
    def construct(self):
        self.chapter_card("סעיף א", "החוואי בשליש הגובה והפרה בשני שלישים",
                          "סעיף א : החוואי בשליש הגובה, והפרה\nבשני שלישים. מה המסלול הקצר ביותר?")
        self.routes()
        self.reflect()
        self.fold()
        self.close()

    # -- three routes, none the shortest -------------------------------------------------------

    def routes(self):
        self.pl = pl = Plane(-4.6, -1.2, 0.85)
        self.field = strip(pl, names=False)
        self.a, self.b = self.people(pl)
        nums = TX(r"L = 7,\quad H = 3,\quad a = 1,\quad b = 2", size=40).move_to([2.6, 3.2, 0])
        self.say("נעבוד עם מספרים : L = 7 ו-H = 3,\nולכן a = 1 ו-b = 2.",
                 FadeIn(self.field), FadeIn(self.a), FadeIn(self.b), FadeIn(nums), run_time=1.2)
        self.nums = nums
        rows = VGroup()
        self.paths = []
        cols = [PATH, C.PURPLE, C.MUTED]

        def show(i):
            (p1, p2), ln, col = ROUTES[i], LENS[i], cols[i]
            path = poly(pl, route(p1, p2), col, 6 if i == 0 else 4)
            row = TX(rf"P = {p1},\ Q = {p2} \;\rightarrow\; {ln:.2f}", size=34, color=col)
            row.move_to([4.7, 1.6 - 0.8 * i, 0])
            rows.add(row)
            dim = [q.animate.set_stroke(opacity=0.35) for q in self.paths]
            self.paths.append(path)
            return [Create(path), FadeIn(row), *dim]

        self.say("מסלול ראשון : אוכל ב-3, מים ב-5.\nהאורך בערך 10.04.", *show(0), run_time=1.4)
        self.say("מסלול שני : אוכל ב-1, מים ב-6.\nארוך יותר, 10.30.", *show(1), run_time=1.4)
        self.say("ומסלול שיורד ישר באמצע : 11.08.\nאיך מוצאים את הקצר ביותר בלי לנחש?", *show(2),
                 run_time=1.4)
        self.rows = rows
        self.say("אפשר לכתוב את האורך כפונקציה של שתי\nנקודות העצירה ולגזור, אבל זה מסורבל.")
        self.say("יש דרך יפה יותר : שיקוף.\nנשקף את הפרה, פעמיים.")
        self.play(FadeOut(rows), FadeOut(self.nums), FadeOut(self.paths[1]), FadeOut(self.paths[2]),
                  self.paths[0].animate.set_stroke(opacity=1), run_time=0.7)

    # -- the double reflection --------------------------------------------------------------------

    def reflect(self):
        old = self.pl
        k = 0.6
        new = Plane(old.ox, old.oy, k)
        moving = Group(self.field, self.a, self.b, self.paths[0])
        self.play(moving.animate.scale(k / old.k, about_point=old.p(0, 0)), run_time=1.0)
        # rebuild in the new plane (the same picture, exact coordinates)
        self.remove(*moving)
        self.pl = pl = new
        self.field = strip(pl, names=False)
        self.a, self.b = self.people(pl, size=30)
        self.path = poly(pl, route(3, 5))
        self.add(self.field, self.a, self.b, self.path)

        below = Group(band(pl, -2.0, 0, -0.6, L + 0.6, 0.25))
        bp = dot(pl, L, -B_H, COW, 0.09)
        bpl = label("B'", bp.get_center(), RIGHT, COW, 30)
        self.say("שיקוף ראשון : משקפים את הפרה דרך\nקו המים, ומקבלים את B' בעומק 2.",
                 FadeIn(below), TransformFromCopy(self.b[0], bp), FadeIn(bpl))
        q = pl.p(5, 0)
        leg = Line(q, pl.p(L, B_H), stroke_color=C.WHITE, stroke_width=5)
        legp = DashedLine(q, pl.p(L, -B_H), stroke_color=C.WHITE, stroke_width=5)
        self.say("לכל נקודה על קו המים, המרחק לפרה\nשווה למרחק ל-B'. הקטע האחרון לא משתנה.",
                 Create(leg), Create(legp))
        self.play(FadeOut(leg), FadeOut(legp), run_time=0.4)
        above = Group(band(pl, H, 2 * H, -0.6, L + 0.6, 0.25), band(pl, 2 * H, 8.3, -0.6, L + 0.6, 0.25),
                      dashed(pl, -0.6, 2 * H, L + 0.6, 2 * H, WATER, 3, 0.7))
        bpp = dot(pl, L, 2 * H + B_H, COW, 0.09)
        bppl = label("B''", bpp.get_center(), RIGHT, COW, 30)
        dist = TX(r"H + b = 5", size=38).move_to([3.0, 2.2, 0])
        self.say("שיקוף שני : את B' משקפים דרך קו האוכל.\nהמרחק שלה מהקו הוא H + b = 5.",
                 FadeIn(above), FadeIn(dist))
        high = TX(r"B'' = (7,\ 2H + b) = (7,\ 8)", size=38, color=COW).next_to(dist, DOWN, buff=0.4)
        self.say("לכן B'' בגובה 2H + b = 8 מעל\nקו המים, מעל השיקוף של הרצועה.",
                 TransformFromCopy(bp, bpp), FadeIn(bppl), FadeIn(high))
        self.below, self.above, self.bp, self.bpl, self.bpp, self.bppl = below, above, bp, bpl, bpp, bppl
        self.texts = VGroup(dist, high)

        # route 1 unfolded: the last leg through the water line, then the last two through the food line
        step1 = poly(pl, [(0, A_H), (3, H), (5, 0), (L, -B_H)])
        step2 = poly(pl, [(0, A_H), (3, H), (5, 2 * H), (L, 2 * H + B_H)])
        with self.beat("עכשיו נפרוש את המסלול הראשון : הקטע\nהאחרון עובר אל B', והשניים אחריו מתקפלים."):
            self.play(Transform(self.path, step1), run_time=1.2)
            self.play(Transform(self.path, step2), run_time=1.2)
        self.say("כל מסלול שווה באורכו לקו שבור\nמ-A אל B'', באותו אורך בדיוק.")
        line = Line(pl.p(0, A_H), pl.p(L, 2 * H + B_H), stroke_color=C.GREEN, stroke_width=6)
        self.say("והקו השבור הקצר ביותר הוא קו ישר.\nהוא המסלול הקצר ביותר אחרי הפרישה.", Create(line))
        self.line = line
        dd = TX(r"D = 2H + b - a = 7", size=40).move_to([3.4, 0.6, 0])
        self.say("ההפרש האנכי : D = 2H + b − a = 7,\nוההפרש האופקי L = 7.",
                 FadeOut(self.texts), FadeIn(dd))
        z = TX(r"z = \sqrt{L^2 + D^2} = \sqrt{98} \approx 9.90", size=40, color=C.GREEN)
        z.next_to(dd, DOWN, buff=0.45)
        self.say("לפי פיתגורס : שורש של 49 ועוד 49,\nכלומר שורש 98, בערך 9.90.", FadeIn(z))
        gen = TX(r"z_{\min} = \sqrt{L^2 + (2H + b - a)^2}", size=40, color=C.AMBER).next_to(z, DOWN, buff=0.45)
        self.say("ובכלל : שורש של L² ועוד (2H + b − a)²,\nבשורה אחת.", FadeIn(gen))
        self.formulas = VGroup(dd, z, gen)

    # -- folding back: the stops ---------------------------------------------------------------------

    def fold(self):
        pl = self.pl
        self.play(FadeOut(self.path), run_time=0.5)
        p = dot(pl, 2, H, FOOD, 0.1)
        qq = dot(pl, 5, 2 * H, WATER, 0.1)
        self.say("איפה הקו הישר חוצה את קו האוכל?\nשם עוצרים לאוכל : ב-x = 2.", FadeIn(p, scale=1.6))
        self.say("ואיפה הוא חוצה את השיקוף של קו המים?\nשם עוצרים למים : ב-5.", FadeIn(qq, scale=1.6))
        ticks = VGroup()
        for (y0, y1), t in zip([(A_H, H), (H, 2 * H), (2 * H, 2 * H + B_H)], ["2", "3", "2"]):
            x0 = (y0 - A_H) * L / SH["D"]
            x1 = (y1 - A_H) * L / SH["D"]
            ticks.add(VGroup(Line(pl.p(x1 + 0.25, y0), pl.p(x1 + 0.25, y1), stroke_color=C.AMBER, stroke_width=4),
                             TX(t, size=30, color=C.AMBER).next_to(pl.p(x1 + 0.25, (y0 + y1) / 2), RIGHT, buff=0.08)))
        self.say("הקו עולה 2 עד קו האוכל, עוד 3\nעד השיקוף, ועוד 2 עד B''.",
                 LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.4), FadeOut(self.formulas))
        ratio = VGroup(TX(r"x : y : w = (H - a) : H : b", size=38), TX(r"= 2 : 3 : 2", size=38, color=C.AMBER))
        ratio.arrange(DOWN, buff=0.25).move_to([3.6, 1.0, 0])
        self.say("ההתקדמות האופקית באותו יחס, כי השיפוע\nקבוע : x = 2, y = 3 ו-w = 2.", FadeIn(ratio))
        stops = VGroup(TX(r"x = \frac{L(H - a)}{D}", size=36),
                       TX(r"y = \frac{LH}{D}, \quad w = \frac{Lb}{D}", size=36)).arrange(DOWN, buff=0.3)
        stops.move_to([3.6, -1.0, 0])
        self.say("ובכלל : x = L(H − a)/D, y = LH/D\nו-w = Lb/D, כל אחד לפי מה שהקו עולה.", FadeIn(stops))
        self.say("בשברים של L : 2L/7, 3L/7 ו-2L/7.\nבדיקה : 2 + 3 + 2 = 7.")
        self.play(FadeOut(ticks), FadeOut(qq), FadeOut(ratio), FadeOut(stops), run_time=0.6)
        folded = poly(pl, [(0, A_H), (2, H), (5, 2 * H), (L, 2 * H + B_H)], C.GREEN)
        self.remove(self.line)
        self.add(folded)
        f1 = poly(pl, [(0, A_H), (2, H), (5, 0), (L, -B_H)], C.GREEN)
        f2 = poly(pl, [(0, A_H), (2, H), (5, 0), (L, B_H)], C.GREEN)
        q = dot(pl, 5, 0, WATER, 0.1)
        with self.beat("מקפלים חזרה : קודם דרך קו האוכל,\nואחר כך דרך קו המים."):
            self.play(Transform(folded, f1), run_time=1.2)
            self.play(Transform(folded, f2), FadeIn(q, scale=1.6), run_time=1.2)
        self.play(FadeOut(self.below), FadeOut(self.above), FadeOut(self.bp), FadeOut(self.bpl),
                  FadeOut(self.bpp), FadeOut(self.bppl), run_time=0.6)
        legs = TX(r"z_1 = \tfrac{2}{7}z,\quad z_2 = \tfrac{3}{7}z,\quad z_3 = \tfrac{2}{7}z", size=38)
        legs.move_to([3.0, 1.2, 0])
        self.say("שלושת המשולשים דומים למשולש הגדול :\nהקטעים הם 2/7, 3/7 ו-2/7 של 9.90.", FadeIn(legs))
        self.say("עם המספרים שלנו הקו עולה ב-45 מעלות,\nכי D = L = 7.")
        self.legs = legs

    def close(self):
        proof = VGroup(TX(r"|AP| + |PQ| + |QB|", size=36), TX(r"= |AP| + |PQ''| + |Q''B''|", size=36),
                       TX(r"\ge |AB''|", size=36, color=C.GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        proof.move_to([3.4, -0.9, 0])
        self.say("ולמה זה המינימום? כל מסלול שווה לקו\nשבור מ-A אל B'', ולפחות כמו הקו הישר.",
                 FadeIn(proof))
        self.fade_all()
        trap = TX(r"2H - b \;\ne\; 2H + b", size=48, color=C.RED).move_to(UP * 1.0)
        self.say("מלכודת : לשקף את הפרה ישר דרך קו\nהאוכל, בלי קו המים, נותן גובה 2H − b.",
                 FadeIn(trap))
        self.say("יש שתי עצירות, ולכן שני שיקופים :\nקודם דרך קו המים, ואז דרך קו האוכל.")
        self.fade_all()


class ChapterB(FarmScene):
    def construct(self):
        self.chapter_card("סעיף ב", "העצירות בשליש ובשני שלישים",
                          "סעיף ב : הבעיה ההפוכה. העצירות בשליש\nובשני שלישים מהדרך. מה a ו-b?")
        pl = Plane(-4.6, -1.0, 0.5)
        lines = Group(band(pl, -2.8, 0, -0.5, L + 0.5, 0.25), band(pl, 0, H, -0.5, L + 0.5),
                      band(pl, H, 2 * H, -0.5, L + 0.5, 0.25), band(pl, 2 * H, 9.4, -0.5, L + 0.5, 0.25),
                      dashed(pl, -0.5, 0, L + 0.5, 0, WATER), dashed(pl, -0.5, H, L + 0.5, H, FOOD),
                      dashed(pl, -0.5, 2 * H, L + 0.5, 2 * H, WATER, 3, 0.7))
        names = Group(he("קו האוכל", 26, FOOD, 600).next_to(pl.p(L + 0.5, H), RIGHT, buff=0.12),
                      he("קו המים", 26, WATER, 600).next_to(pl.p(L + 0.5, 0), RIGHT, buff=0.12),
                      he("השיקוף של קו המים", 26, WATER, 500).next_to(pl.p(L + 0.5, 2 * H), RIGHT, buff=0.12))
        self.say("אותו שיקוף, בכיוון ההפוך : מתחילים\nמהקו הישר, ולא מהגבהים.", FadeIn(lines), FadeIn(names))
        p1, p2 = F(L, 3), F(2 * L, 3)
        p = dot(pl, p1, H, FOOD, 0.1)
        q = dot(pl, p2, 2 * H, WATER, 0.1)
        thirds = VGroup(*[DashedLine(pl.p(x, -0.3), pl.p(x, 9.2), stroke_color=C.FAINT, stroke_width=2)
                          for x in (p1, p2)])
        tl = VGroup(TX(r"\tfrac{L}{3}", size=32, color=C.MUTED).next_to(pl.p(p1, -0.3), DOWN, buff=0.08),
                    TX(r"\tfrac{2L}{3}", size=32, color=C.MUTED).next_to(pl.p(p2, -0.3), DOWN, buff=0.08))
        self.say("הקו חוצה את קו האוכל בשליש,\nואת השיקוף של קו המים בשני שלישים.",
                 FadeIn(thirds), FadeIn(tl), FadeIn(p, scale=1.6), FadeIn(q, scale=1.6))
        mid = Line(pl.p(p1, H), pl.p(p2, 2 * H), stroke_color=C.GREEN, stroke_width=6)
        rise = VGroup(Line(pl.p(p2 + 0.3, H), pl.p(p2 + 0.3, 2 * H), stroke_color=C.AMBER, stroke_width=4),
                      TX("H", size=30, color=C.AMBER).next_to(pl.p(p2 + 0.3, 1.5 * H), RIGHT, buff=0.08))
        self.say("שתי נקודות קובעות קו ישר : בין שתיהן\nהוא עולה H על פני שליש מהדרך.", Create(mid), FadeIn(rise))
        first = Line(pl.p(0, 0), pl.p(p1, H), stroke_color=C.GREEN, stroke_width=6)
        a0 = dot(pl, 0, 0, FARMER, 0.11)
        al = label("A", a0.get_center(), LEFT, FARMER, 30)
        res_a = TX(r"a = 0", size=42).move_to([4.5, 2.6, 0])
        self.say("אותו שיפוע בשליש הראשון : הקו יורד\nעוד H, ומתחיל בגובה 0. לכן a = 0.",
                 Create(first), FadeIn(a0), FadeIn(al), FadeIn(res_a))
        last = Line(pl.p(p2, 2 * H), pl.p(L, 3 * H), stroke_color=C.GREEN, stroke_width=6)
        bpp = dot(pl, L, 3 * H, COW, 0.1)
        bl = label("B''", bpp.get_center(), UP, COW, 30)
        res_b = VGroup(TX(r"2H + b = 3H", size=42), TX(r"b = H", size=42)).arrange(DOWN, buff=0.3)
        res_b.next_to(res_a, DOWN, buff=0.4)
        self.say("ובשליש האחרון עוד H, עד 3H. הגובה\nשל B'' הוא 2H + b, ולכן b = H.",
                 Create(last), FadeIn(bpp), FadeIn(bl), FadeIn(res_b))
        self.say("התשובה : a = 0 ו-b = H. החוואי עומד\nעל קו המים, והפרה על קו האוכל.")
        whole = poly(pl, [(0, 0), (p1, H), (p2, 2 * H), (L, 3 * H)], C.GREEN)
        self.remove(first, mid, last)
        self.add(whole)
        f1 = poly(pl, [(0, 0), (p1, H), (p2, 0), (L, -H)], C.GREEN)
        f2 = poly(pl, [(0, 0), (p1, H), (p2, 0), (L, H)], C.GREEN)
        b_real = dot(pl, L, H, COW, 0.11)
        b_l = label("B", b_real.get_center(), UP, COW, 30)
        with self.beat("מקפלים חזרה : שלושה קטעים חופפים,\nכל אחד עם ניצבים L/3 ו-H."):
            self.play(FadeOut(rise), FadeOut(bl), run_time=0.4)
            self.play(Transform(whole, f1), run_time=1.1)
            self.play(Transform(whole, f2), ReplacementTransform(bpp, b_real), FadeIn(b_l), run_time=1.1)
        chk = VGroup(TX(r"D = 2H + H - 0 = 3H", size=36), TX(r"x = y = w = \tfrac{L}{3}", size=36, color=C.AMBER))
        chk.arrange(DOWN, buff=0.25).move_to([4.5, -1.3, 0])
        self.say("בדיקה בנוסחאות של סעיף א : D = 3H,\nולכן x = y = w = L/3, כמו שרצינו.", FadeIn(chk))
        self.play(FadeOut(res_a), FadeOut(res_b), FadeOut(chk), run_time=0.5)
        gen = VGroup(TX(r"D = \frac{LH}{y}", size=36),
                     TX(r"a = H\left(1 - \frac{x}{y}\right)", size=36),
                     TX(r"b = \frac{H w}{y}", size=36),
                     TX(r"x \le y, \quad w \le y", size=36, color=C.AMBER)).arrange(DOWN, buff=0.3)
        gen.move_to([4.5, 0.9, 0])
        self.say("בכלל : הקטע האמצעי עולה H על פני y,\nומזה יוצאים a ו-b.", FadeIn(gen[0]), FadeIn(gen[1]), FadeIn(gen[2]))
        self.say("וכדי שהגבהים יהיו בין הקווים צריך x ≤ y\nו-w ≤ y : הקטע האמצעי הוא הארוך.", FadeIn(gen[3]))
        self.say("כאן x = y = w, בדיוק על הגבול. לכן\nהחוואי והפרה עומדים על הקווים עצמם.")
        self.say("מלכודת : לבדוק רק ש-b ≥ 0. צריך\nגם b ≤ H, אחרת הפרה מעל קו האוכל.")
        self.fade_all()


class ChapterC(FarmScene):
    def construct(self):
        self.chapter_card("סעיף ג", "קו האוכל נוטה בזווית",
                          "סעיף ג : קו האוכל נוטה בזווית θ,\nוהקווים נפגשים משמאל, בנקודה O.")
        self.rotation()
        self.sweep()
        self.box()

    # -- the example theta = 15: two reflections are a rotation -----------------------------------------

    def rotation(self):
        r = T15
        t = math.radians(15)
        pl = Plane(-2.0, -1.4, 0.42)
        ox = r["O"][0]
        o = pl.p(ox, 0)
        far = 19.5

        def ray(ang, length, color, width=4, opacity=1.0):
            end = (ox + length * math.cos(ang), length * math.sin(ang))
            return DashedLine(o, pl.p(*end), dash_length=0.16, dashed_ratio=0.6, stroke_color=color,
                              stroke_width=width, stroke_opacity=opacity)

        xe = ox + far * math.cos(t)
        face = Polygon(o, pl.p(xe, 0), pl.p(xe, far * math.sin(t)), stroke_width=0, fill_color=FACE,
                       fill_opacity=0.55)
        water, food = ray(0, far * math.cos(t), WATER), ray(t, far, FOOD)
        od = Dot(o, radius=0.08, color=C.WHITE)
        ol = label("O", o, DOWN, C.WHITE, 30)
        a, b = self.people(pl, size=30)
        th = Arc(radius=1.3, start_angle=0, angle=t, arc_center=o, stroke_color=C.WHITE, stroke_width=2)
        thl = TX(r"\theta", size=30).move_to(o + 1.6 * np.array([math.cos(t / 2), math.sin(t / 2), 0]))
        ex = VGroup(TX(r"\theta = 15^\circ", size=34), TX(r"O \approx (-11.20,\ 0)", size=34)).arrange(DOWN, buff=0.15)
        ex.move_to([4.7, 3.3, 0])
        self.say("קו המים נשאר אופקי, וקו האוכל עובר\nדרך (0, 3) בזווית θ. בדוגמה : 15 מעלות.",
                 FadeIn(face), Create(water), Create(food), FadeIn(od), FadeIn(ol), FadeIn(a), FadeIn(b),
                 FadeIn(th), FadeIn(thl), FadeIn(ex), run_time=1.4)
        b1 = dot(pl, L, -B_H, COW, 0.08)
        b1l = label("B_1", b1.get_center(), RIGHT, COW, 28)
        self.say("השיקוף הראשון כמו קודם, דרך קו המים :\nהתמונה B1 = (7, −2).", TransformFromCopy(b[0], b1),
                 FadeIn(b1l))
        self.say("השיקוף השני דרך קו האוכל הנטוי,\nבניצב לקו, לא בניצב לציר.")
        self.say("מלכודת : לשקף בקו אנכי, כאילו קו האוכל\nאופקי בגובה H + L tan θ. זה לא נכון.")
        rot = TX(r"R_{\text{food}} \circ R_{\text{water}} = \mathrm{Rot}_O(2\theta)", size=32).move_to([4.5, 2.25, 0])
        self.say("והפתעה : שני שיקופים דרך קווים\nשנחתכים ב-O הם סיבוב סביב O.", FadeIn(rot))
        img = ray(2 * t, far, WATER, 3, 0.6)
        b2 = dot(pl, *r["B2"], COW, 0.09)
        b2l = label("B_2", b2.get_center(), UP, COW, 28)
        radius = math.dist(r["O"], (L, B_H)) * pl.k
        beta = math.atan2(B_H, L - ox)
        arc = DashedVMobject(Arc(radius=radius, start_angle=beta, angle=2 * t, arc_center=o,
                                 stroke_color=COW, stroke_width=3), num_dashes=18)
        self.say("כל שיקוף שומר על המרחק מ-O, ולכן\nהפרה בזווית β עוברת אל 2θ + β.", Create(arc), Create(img),
                 run_time=1.6)
        b2t = TX(r"B_2 \approx (3.56,\ 10.83)", size=34, color=COW).move_to([4.6, 1.45, 0])
        self.say("לכן B2 הוא B מסובב ב-30 מעלות\nסביב O : בערך (3.56, 10.83).", FadeIn(b2), FadeIn(b2l),
                 FadeIn(b2t))
        line = Line(pl.p(0, A_H), pl.p(*r["B2"]), stroke_color=C.GREEN, stroke_width=5)
        zt = TX(r"z = |AB_2| \approx 10.456", size=36, color=C.GREEN).move_to([4.6, 0.65, 0])
        self.say("והמסלול הקצר ביותר שוב קו ישר,\nמ-A אל B2 : באורך 10.456 בערך.", Create(line), FadeIn(zt))
        pd = dot(pl, *r["P"], FOOD, 0.08)
        qs = dot(pl, *r["Qs"], WATER, 0.08)
        self.say("הוא חוצה את קו האוכל, ואחר כך את\nהשיקוף של קו המים, בסדר הנכון.", FadeIn(pd, scale=1.6),
                 FadeIn(qs, scale=1.6))
        back = poly(pl, [(0, A_H), r["P"], r["Q"], (L, B_H)], C.GREEN, 5)
        qd = dot(pl, *r["Q"], WATER, 0.08)
        stops = VGroup(TX(r"P \approx (0.80,\ 3.22)", size=34), TX(r"Q \approx (4.62,\ 0)", size=34))
        stops.arrange(DOWN, buff=0.15).move_to([4.6, -0.45, 0])
        with self.beat("מקפלים חזרה : אוכל ב-(0.80, 3.22)\nבערך, ומים ב-(4.62, 0)."):
            self.play(FadeOut(line), FadeOut(qs), FadeOut(arc), FadeOut(img), Create(back), FadeIn(qd),
                      FadeIn(stops), run_time=1.4)
        self.fade_all()
        zz = VGroup(TX(r"z^2 = L^2 + (H + b)^2 + (H - a)^2", size=40),
                    TX(r"+\, 2(H - a)\big(L\sin 2\theta + (H + b)\cos 2\theta\big)", size=40),
                    TX(r"\theta = 0:\quad z^2 = L^2 + (2H + b - a)^2", size=40, color=C.AMBER))
        zz[1].next_to(zz[0], DOWN, buff=0.3).align_to(zz[0], LEFT).shift(RIGHT * 0.6)
        zz[2].next_to(zz[1], DOWN, buff=0.7)
        zz[2].set_x(0)
        zz.move_to(UP * 1.0)
        self.say("הנוסחה : מפתחים את |AB2|².\nבזווית 0 היא חוזרת בדיוק לסעיף א.", FadeIn(zz))
        self.fade_all()

    # -- theta from 0 to 60 -------------------------------------------------------------------------

    def sweep(self):
        pl = Plane(-4.5, -1.6, 0.66)
        X0, X1, YMAX = -1.5, 8.2, 6.0
        th = ValueTracker(0.0)

        def food_end(t):
            """The food line from x = max(X0, O) to the box edge (x = X1 or y = YMAX)."""
            tn = math.tan(t)
            x0 = X0 if t == 0 else max(X0, -H / tn)
            x1 = X1 if tn == 0 else min(X1, (YMAX - H) / tn)
            return (x0, H + x0 * tn), (x1, H + x1 * tn)

        def picture():
            deg = th.get_value()
            t = math.radians(deg)
            (fx0, fy0), (fx1, fy1) = food_end(t)
            wx0 = fx0
            pts = [pl.p(wx0, 0), pl.p(X1, 0)]
            if fx1 < X1 - 1e-9:
                pts += [pl.p(X1, YMAX), pl.p(fx1, fy1)]
            else:
                pts += [pl.p(X1, fy1)]
            pts += [pl.p(fx0, fy0)]
            face = Polygon(*pts, stroke_width=0, fill_color=FACE, fill_opacity=0.55)
            water = DashedLine(pl.p(wx0, 0), pl.p(X1, 0), dash_length=0.16, dashed_ratio=0.6,
                               stroke_color=WATER, stroke_width=4)
            food = DashedLine(pl.p(fx0, fy0), pl.p(fx1, fy1), dash_length=0.16, dashed_ratio=0.6,
                              stroke_color=FOOD, stroke_width=4)
            r = q0048.tilted(L, H, A_H, B_H, deg)
            path = poly(pl, [(0, A_H), r["P"], r["Q"], (L, B_H)], C.GREEN, 5)
            pd, qd = dot(pl, *r["P"], FOOD, 0.08), dot(pl, *r["Q"], WATER, 0.08)
            fence = DashedLine(pl.p(0, -0.2), pl.p(0, YMAX), stroke_color=C.FAINT, stroke_width=1.5)
            return VGroup(face, fence, water, food, path, pd, qd)

        pic = always_redraw(picture)
        a, b = self.people(pl, size=30)

        def readout():
            deg = th.get_value()
            r = q0048.tilted(L, H, A_H, B_H, deg)
            rows = VGroup(M(f"θ    = {deg:5.1f}°", 32, C.WHITE),
                          M(f"z    = {r['z']:6.3f}", 32, C.GREEN),
                          M(f"food x = {r['P'][0]:5.2f}", 28, FOOD),
                          M(f"turn = {r['turn']:5.1f}°", 28, C.AMBER),
                          M(f"3θ   = {3 * deg:5.1f}°", 28, C.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            return rows.move_to([4.3, 1.0, 0])

        read = always_redraw(readout)
        self.say("עכשיו מעלים את θ מ-0 : קו האוכל\nמסתובב, והמסלול מתעדכן איתו.", FadeIn(pic), FadeIn(a),
                 FadeIn(b), FadeIn(read), run_time=1.2)
        self.say("בזווית 0 זה סעיף א : 9.90.\nב-15 מעלות 10.456, קו האוכל התרחק.",
                 th.animate.set_value(15), run_time=3.5, rate_func=linear)
        self.say("סביב 27 מעלות נקודת האוכל עוברת\nמשמאל לחוואי. זה מותר : הקווים ממשיכים.",
                 th.animate.set_value(30), run_time=4.0, rate_func=linear)
        self.say("האורך מגיע לבערך 10.6 ואז יורד :\nב-45 מעלות 10.30.", th.animate.set_value(45),
                 run_time=4.0, rate_func=linear)
        self.say("וב-60 מעלות 9.60. בכל הדרך הזו\nהשיקוף נותן את התשובה, בלי מקרי קצה.",
                 th.animate.set_value(60), run_time=4.0, rate_func=linear)
        self.play(FadeOut(pic), FadeOut(a), FadeOut(b), FadeOut(read), run_time=0.7)
        why = VGroup(TX(r"0 \le \alpha,\ \beta \le \theta", size=40),
                     TX(r"2\theta + \beta - \alpha \;\le\; 3\theta \;\le\; 180^\circ", size=44, color=C.AMBER),
                     TX(r"\theta = 60^\circ:\quad 102.9^\circ < 180^\circ", size=40)).arrange(DOWN, buff=0.55)
        why.move_to(UP * 1.0)
        self.say("למה? מ-O רואים את A בזווית α ואת B\nבזווית β, שתיהן בין 0 ל-θ.", FadeIn(why[0]))
        self.say("הקו הישר מסתובב סביב O ב-2θ + β − α,\nוזה לכל היותר 3θ.", FadeIn(why[1]))
        self.say("שלוש פעמים 60 הן 180 : עד 60 מעלות\nהקו חוצה את הקווים בסדר הנכון.")
        self.say("בדוגמה, ב-60 מעלות הסיבוב 102.9 מעלות,\nרחוק מ-180.", FadeIn(why[2]))
        self.say("רק מעל 60 מעלות זה יכול להישבר,\nואז המסלול הקצר עובר דרך O עצמה.")
        self.fade_all()

    def box(self):
        view = BoxView(QID, "tilt", height=6.3).move_to(UP * 0.7)
        self.say("כך זה נראה בתיבה שבעמוד, עם השיקוף :\nהרצועות המשוקפות, B2, וקשת הסיבוב.", FadeIn(view))
        self.box_beat(view, [
            (1, "ב-30 מעלות B2 כבר משמאל לציר,\nונקודת האוכל משמאל לחוואי."),
            (2, "וב-45 מעלות : האורך כבר יורד,\nבערך 10.30."),
        ])
        self.fade_all()


class Closing(FarmScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"z = \sqrt{L^2 + (2H + b - a)^2}", size=40)),
                           ("ב", TX(r"a = 0,\quad b = H", size=40)),
                           ("ג", TX(r"B_2 = \mathrm{rot}_O(2\theta)\,B,\quad z = |AB_2|", size=40))],
                     ["לסיכום : שני שיקופים הופכים את המסלול\nלקו ישר, גם כשקו האוכל נוטה.",
                      "נסו גבהים וזוויות משלכם בתיבה\nשבעמוד של שאלה 0048 באתר."])
