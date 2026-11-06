"""The tutorial video of question 0026, three friends and one motorcycle (script: script.md).

Render with `python videos/render.py 0026` (see notes/VIDEOS.md). One part and no code: the
proof step by step instead (as in 0015 and 0029). The road from A to B is drawn as a line,
the motorcycle with its driver and the two others move on it, and a distance-time chart
under it is drawn in step (a line per traveller and one for the motorcycle): first the two
simple plans (the second friend waits at A: 3 h; he walks meanwhile: 19/7 h, and now the
passenger waits at B), then the plan in which the passenger gets off on the way and all
three arrive together after 2.5 h. Then the formula, derived in LaTeX stage by stage as
the page does it (y, x, z, x, r and alpha = t0 / t1), checked on 13 and 1, its edge cases,
and the page's motorcycle box: the plan played, other values (t0 = 4; three riders), and
the proof panel (the drop point D against both arrival times).
"""

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, T, he, read_palette  # noqa: E402

QID = 26
SCENES = [
    ("Opening", "פתיחה"),
    ("Chapter", "שלושה אנשים ואופנוע – התוכנית והנוסחה"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="motorcycle", t0 = 13, t1 = 1). Its time slider is in units of
# t1, so 0.875, 1.625 and 2.5 are the ends of the three stages; a value past the end is
# clamped to the plan's T by the browser.
BOXES = {
    "play": {"box": 0, "region": [".ex-play-row", ".road-box", ".ex-summary", ".road-chart"],
             "hide": [".ex-speed"],
             "steps": [[], [["set", ".ex-t", "0.875"]], [["set", ".ex-t", "1.625"]],
                       [["set", ".ex-t", "2.5"]]]},
    "values": {"box": 0, "region": [".ex-t0", ".ex-k", ".road-box", ".ex-summary", ".road-chart"],
               "hide": ["label:has(.ex-km)", "label:has(.ex-strategy)", "label:has(.ex-cmp)",
                        ".ex-controls .ex-reset", "label:has(.ex-speed)", ".road-title"],
               "steps": [[["set", ".ex-t", "9"]],
                         [["set", ".ex-t0", "4"], ["set", ".ex-t", "9"]],
                         [["set", ".ex-t0", "13"], ["set", ".ex-k", "3"], ["set", ".ex-t", "9"]]]},
    "drop": {"box": 0, "region": [".road-proof"],
             "steps": [[], [["set", ".ex-drop", "0.5"]], [["set", ".ex-drop", "0.97"]],
                       [["click", ".ex-drop-best"]]]},
}

_S = read_palette()["slate"]
P_COL, W_COL, BIKE = _S["--viz-s1"], _S["--viz-s2"], C.AMBER

# ---- the plans, checked with exact fractions (AB = 1, t1 = 1, alpha = 13) ----------------

ALPHA = 13
V0 = Fr(1, ALPHA)


def T_formula(t0, t1):
    return Fr(3 * t0 + t1, t0 + 3 * t1) * t1


assert T_formula(13, 1) == Fr(5, 2) and Fr(3 * ALPHA + 1, ALPHA + 3) == Fr(40, 16)
assert Fr(3 * ALPHA - 1, ALPHA + 1) == Fr(19, 7)
D_DROP = Fr(ALPHA + 1, ALPHA + 3)                     # 7/8
assert D_DROP == Fr(7, 8)
Q = D_DROP * V0                                       # the walker when the passenger gets off
MEET_T = D_DROP + (D_DROP - Q) / (1 + V0)              # the motorcycle meets the walker
C_POS = Q + (MEET_T - D_DROP) * V0
E_POS = D_DROP + (MEET_T - D_DROP) * V0
assert (Q, MEET_T, C_POS, E_POS) == (Fr(7, 104), Fr(13, 8), Fr(1, 8), Fr(97, 104))
assert C_POS + (1 - C_POS) == 1 and MEET_T + (1 - C_POS) == Fr(5, 2)
assert E_POS + (Fr(5, 2) - MEET_T) * V0 == 1
# the segments y, x, z, x, r as parts of AB
x = Fr(ALPHA - 1, ALPHA * (ALPHA + 3))
y = r = Fr(ALPHA + 1, ALPHA * (ALPHA + 3))
z = Fr(ALPHA - 1, ALPHA + 3)
assert y + x + z + x + r == 1 and (y, y + x, y + x + z) == (Q, C_POS, D_DROP)
assert ALPHA * y == y + x + z and z == ALPHA * x and ALPHA * r == z + x + r
assert y + x == Fr(2, ALPHA + 3) and (y + x) * ALPHA + (1 - y - x) == Fr(5, 2)
# the simple plans
MW_MEET = 1 + (1 - V0) / (1 + V0)                     # 13/7: the motorcycle back to the walker
assert MW_MEET == Fr(13, 7) and MW_MEET * V0 == Fr(1, 7) and MW_MEET + (1 - Fr(1, 7)) == Fr(19, 7)
# other values in the box: t0 = 4, t1 = 1; three riders at alpha = 13
assert T_formula(4, 1) == Fr(13, 7) and Fr(5 * ALPHA + 1, ALPHA + 5) == Fr(11, 3)

# Each plan: the breakpoints (time, place) of the motorcycle, the passenger and the walker,
# and when each of the two rides.
PLANS = {
    "wait": {"bike": [(0, 0), (1, 1), (2, 0), (3, 1)],
             "p": [(0, 0), (1, 1), (3, 1)], "w": [(0, 0), (2, 0), (3, 1)],
             "ride_p": (0, 1), "ride_w": (2, 3), "T": Fr(3)},
    "meanwhile": {"bike": [(0, 0), (1, 1), (MW_MEET, Fr(1, 7)), (Fr(19, 7), 1)],
                  "p": [(0, 0), (1, 1), (Fr(19, 7), 1)],
                  "w": [(0, 0), (MW_MEET, Fr(1, 7)), (Fr(19, 7), 1)],
                  "ride_p": (0, 1), "ride_w": (MW_MEET, Fr(19, 7)), "T": Fr(19, 7)},
    "best": {"bike": [(0, 0), (D_DROP, D_DROP), (MEET_T, C_POS), (Fr(5, 2), 1)],
             "p": [(0, 0), (D_DROP, D_DROP), (Fr(5, 2), 1)],
             "w": [(0, 0), (MEET_T, C_POS), (Fr(5, 2), 1)],
             "ride_p": (0, D_DROP), "ride_w": (MEET_T, Fr(5, 2)), "T": Fr(5, 2)},
}
for plan in PLANS.values():            # every line ends at B at the plan's end
    assert all(pts[-1] == (plan["T"], 1) for pts in (plan["bike"], plan["p"], plan["w"]))


def at(points, t: float) -> float:
    """The place on a piecewise-linear line at time t."""
    t0, p0 = points[0]
    for t1, p1 in points[1:]:
        if t <= t1:
            return float(p0) + (float(p1) - float(p0)) * (t - float(t0)) / (float(t1) - float(t0))
        t0, p0 = t1, p1
    return float(points[-1][1])


def upto(points, t: float):
    """The breakpoints before t, then the point at t: the line drawn so far."""
    out = [(float(a), float(b)) for a, b in points if float(a) < t]
    out.append((t, at(points, t)))
    return out


# ---- the road and the chart ---------------------------------------------------------------

ROAD_Y, ROAD_X0, ROAD_X1 = 2.75, -5.6, 5.6


def road_x(p: float) -> float:
    return ROAD_X0 + (ROAD_X1 - ROAD_X0) * p


def bike_icon() -> VGroup:
    """The motorcycle with its driver: two wheels, a frame and the driver (amber)."""
    w1 = Circle(radius=0.11, stroke_color=BIKE, stroke_width=4)
    w2 = w1.copy().shift(RIGHT * 0.42)
    frame = Polygon([0, 0, 0], [0.21, 0.2, 0], [0.42, 0, 0], stroke_color=BIKE, stroke_width=4)
    driver = Circle(radius=0.11, stroke_width=0, fill_color=BIKE, fill_opacity=1).move_to([0.21, 0.38, 0])
    g = VGroup(w1, w2, frame, driver)
    return g


def person(color: str) -> Circle:
    return Circle(radius=0.15, stroke_color=C.NAVY, stroke_width=3, fill_color=color, fill_opacity=1)


class Road(VGroup):
    """The road A to B; the motorcycle (with a rider on it) above the line, walkers under it."""

    def __init__(self, tt: ValueTracker, plan: dict, y0: float = ROAD_Y):
        super().__init__()
        self.tt, self.plan, self.y0 = tt, plan, y0
        line = Line([ROAD_X0, y0, 0], [ROAD_X1, y0, 0], stroke_color=C.MUTED, stroke_width=4)
        ends = VGroup(*[Line([xx, y0 - 0.14, 0], [xx, y0 + 0.14, 0], stroke_color=C.MUTED, stroke_width=4)
                        for xx in (ROAD_X0, ROAD_X1)])
        a = TX("A", size=36).next_to(line.get_start(), LEFT, buff=0.45)
        b = TX("B", size=36).next_to(line.get_end(), RIGHT, buff=0.45)
        self.base = VGroup(line, ends, a, b)
        self.bike = bike_icon()
        self.p, self.w = person(P_COL), person(W_COL)
        self.add(self.base, self.bike, self.p, self.w)
        self.update_all()
        for m in (self.bike, self.p, self.w):
            m.add_updater(lambda _m: self.update_all())

    def set_plan(self, plan: dict):
        self.plan = plan
        self.update_all()

    def update_all(self):
        t, pl = self.tt.get_value(), self.plan
        xb = road_x(at(pl["bike"], t))
        self.bike.move_to([xb, self.y0 + 0.3, 0])
        for dot, key, ride in ((self.p, "p", pl["ride_p"]), (self.w, "w", pl["ride_w"])):
            xp = road_x(at(pl[key], t))
            riding = float(ride[0]) <= t <= float(ride[1]) and t > 0
            if riding:
                dot.move_to([xb + 0.36, self.y0 + 0.75, 0])
            else:
                dot.move_to([xp, self.y0 - 0.32, 0])
        # at the start both stand at A: the walker a little apart from the passenger
        if t == 0:
            self.p.move_to([road_x(0), self.y0 - 0.32, 0])
            self.w.move_to([road_x(0) + 0.36, self.y0 - 0.32, 0])

    def mark(self, p: float, name: str) -> VGroup:
        """A point of the road: a tick and its name under the walkers' row."""
        tick = Line([road_x(p), self.y0 - 0.1, 0], [road_x(p), self.y0 + 0.1, 0],
                    stroke_color=C.AMBER, stroke_width=4)
        lab = TX(name, size=32, color=C.AMBER).move_to([road_x(p), self.y0 - 0.78, 0])
        return VGroup(tick, lab)


class Chart(VGroup):
    """The distance-time chart: time in hours across, the place on the road up (0 = A, 1 = B)."""

    def __init__(self, tt: ValueTracker, plan: dict, tmax: float = 3.0, origin=(-5.0, -1.85),
                 width: float = 8.4, height: float = 2.85):
        super().__init__()
        self.tt, self.plan, self.tmax = tt, plan, tmax
        self.ox, self.oy, self.w, self.h = origin[0], origin[1], width, height
        ax = Line(self.pt(0, 0), self.pt(tmax, 0), stroke_color=C.MUTED, stroke_width=3)
        ay = Line(self.pt(0, 0), self.pt(0, 1.0), stroke_color=C.MUTED, stroke_width=3)
        top = DashedLine(self.pt(0, 1), self.pt(tmax, 1), stroke_color=C.FAINT, stroke_width=2)
        lab_a = TX("A", size=30, color=C.MUTED).next_to(self.pt(0, 0), LEFT, buff=0.2)
        lab_b = TX("B", size=30, color=C.MUTED).next_to(self.pt(0, 1), LEFT, buff=0.2)
        ticks = VGroup()
        for k in range(int(tmax) + 1):
            ticks.add(Line(self.pt(k, 0), self.pt(k, 0) + DOWN * 0.1, stroke_color=C.MUTED, stroke_width=3))
            ticks.add(M(str(k), 28, C.MUTED).next_to(self.pt(k, 0), DOWN, buff=0.18))
        unit = T("h", 28, C.MUTED).next_to(self.pt(tmax, 0), RIGHT, buff=0.2)
        self.axes = VGroup(top, ax, ay, lab_a, lab_b, ticks, unit)
        self.add(self.axes)
        self.lines = VGroup(
            always_redraw(lambda: self.trace("bike", BIKE, 9, 0.45)),
            always_redraw(lambda: self.trace("w", W_COL, 4, 1.0)),
            always_redraw(lambda: self.trace("p", P_COL, 4, 1.0)),
        )
        self.add(self.lines)

    def pt(self, t: float, p: float) -> np.ndarray:
        return np.array([self.ox + self.w * t / self.tmax, self.oy + self.h * p, 0.0])

    def trace(self, key: str, color: str, width: float, opacity: float) -> VMobject:
        t = self.tt.get_value()
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
        pts = [self.pt(a, b) for a, b in upto(self.plan[key], t)]
        if len(pts) < 2:
            pts = [pts[0], pts[0] + RIGHT * 1e-4]
        m.set_points_as_corners(pts)
        return m


def legend() -> Group:
    rows = []
    for icon, name in ((bike_icon().scale(0.9), "הנהג והאופנוע"), (person(P_COL), "הנוסע"),
                       (person(W_COL), "ההולך")):
        rows.append(Group(he(name, 30), icon).arrange(RIGHT, buff=0.25))
    g = Group(*rows).arrange(DOWN, buff=0.3, aligned_edge=RIGHT)
    return g


class MotoScene(DVQScene):
    """Helpers shared by the scenes of 0026."""

    def clock(self, tt: ValueTracker, where) -> Mobject:
        return always_redraw(lambda: M(f"t = {tt.get_value():.3f} h", 32, C.WHITE).move_to(where))

    def run(self, tt: ValueTracker, to, per_hour: float = 3.2):
        to = float(to)
        self.play(tt.animate.set_value(to), run_time=max(0.6, abs(to - tt.get_value()) * per_hour),
                  rate_func=linear)


class Opening(MotoScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "שלושה אנשים ואופנוע אחד",
                     ["תוכנית, ואז נוסחה כללית"],
                     ["שאלה 0026 : שלושה אנשים ואופנוע אחד,\nשאלה ברמת ג'וניור.",
                      "סעיף אחד : הזמן הקצר ביותר,\nהתוכנית, ונוסחה כללית."])
        self.fade_all()
        tt = ValueTracker(0)
        road = Road(tt, PLANS["best"], y0=1.2)
        self.say("שלושה חברים ב-A צריכים להגיע ל-B.\nיש להם אופנוע אחד, לנהג ולנוסע אחד.",
                 FadeIn(road.base), FadeIn(road.bike), FadeIn(road.p), FadeIn(road.w), run_time=1.2)
        walk = Group(person(W_COL), TX(r"t_0 = 13\ \text{h}", size=40)).arrange(RIGHT, buff=0.4)
        ride = Group(bike_icon(), TX(r"t_1 = 1\ \text{h}", size=40)).arrange(RIGHT, buff=0.4)
        Group(walk, ride).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.6)
        self.say("הליכה של כל הדרך : 13 שעות.\nנסיעה באופנוע של כל הדרך : שעה אחת.",
                 FadeIn(walk), FadeIn(ride))
        self.say("מה הזמן הקצר ביותר עד ששלושתם ב-B?\nהמרחק עצמו לא ידוע.")
        road.clear_updaters()
        for m in (road.bike, road.p, road.w):
            m.clear_updaters()
        self.fade_all()


class Chapter(MotoScene):
    def construct(self):
        self.simple_plans()
        self.best_plan()
        self.formula()
        self.edges()
        self.box()

    # -- the plans on the road and the chart ------------------------------------------------

    def stage(self, plan_key: str, tmax: float = 3.0):
        tt = ValueTracker(0)
        road = Road(tt, PLANS[plan_key])
        chart = Chart(tt, PLANS[plan_key], tmax=tmax)
        lg = legend().move_to([5.25, -0.5, 0])
        clk = self.clock(tt, [5.25, 1.25, 0])
        return tt, road, chart, lg, clk

    def simple_plans(self):
        tt, road, chart, lg, clk = self.stage("wait")
        self.say("נתחיל מהתוכנית שעולה ראשונה. למעלה הדרך,\nולמטה גרף : המקום על הדרך מול הזמן.",
                 FadeIn(road), FadeIn(chart.axes), FadeIn(lg), FadeIn(clk), run_time=1.2)
        self.add(chart.lines)
        with self.beat("הנהג מסיע את הנוסע עד B,\nבשעה אחת. בגרף זה קו תלול."):
            self.run(tt, 1)
        with self.beat("הוא חוזר ריק ל-A, עוד שעה,\nוההולך מחכה שם כל הזמן הזה."):
            self.run(tt, 2)
        with self.beat("ואז מסיע את ההולך. סך הכול 3 שעות,\nוההולך בזבז שעתיים בהמתנה."):
            self.run(tt, 3)
        self.fade_all()

        tt, road, chart, lg, clk = self.stage("meanwhile")
        self.play(FadeIn(road), FadeIn(chart.axes), FadeIn(lg), FadeIn(clk), run_time=0.8)
        self.add(chart.lines)
        with self.beat("שיפור : ההולך יוצא לדרך מיד.\nבגרף זה קו כמעט שטוח, הליכה איטית."):
            self.run(tt, 1)
        with self.beat("האופנוע חוזר ופוגש אותו מוקדם יותר,\nכי שניהם נעים זה לקראת זה."):
            self.run(tt, MW_MEET)
        with self.beat("ככה מגיעים אחרי 19/7 שעות,\nבערך 2.71. אבל עכשיו הנוסע מחכה ב-B."):
            self.run(tt, Fr(19, 7))
        wait_band = Line(chart.pt(1, 1), chart.pt(float(Fr(19, 7)), 1), stroke_color=P_COL, stroke_width=12,
                         stroke_opacity=0.5)
        self.say("הקו של הנוסע שטוח ב-B כמעט שעתיים :\nזה זמן שהוא יכול היה ללכת בו.", Create(wait_band))
        self.fade_all()

    def best_plan(self):
        tt, road, chart, lg, clk = self.stage("best")
        self.say("הרעיון : אף אחד לא צריך לחכות.\nהנוסע יורד לפני B וממשיך ברגל.",
                 FadeIn(road), FadeIn(chart.axes), FadeIn(lg), FadeIn(clk), run_time=0.8)
        self.add(chart.lines)
        d_mark = road.mark(float(D_DROP), "D")
        q_mark = road.mark(float(Q), "Q")
        with self.beat("שלב 1 : הנהג והנוסע נוסעים עד D,\nשבע שמיניות מהדרך. ההולך מגיע ל-Q."):
            self.run(tt, D_DROP)
            self.play(FadeIn(d_mark), FadeIn(q_mark), run_time=0.5)
        c_mark = road.mark(float(C_POS), "C")
        e_mark = road.mark(float(E_POS), "E")
        with self.beat("שלב 2 : הנוסע הולך מ-D, והאופנוע חוזר\nופוגש את ההולך ב-C, שמינית מהדרך."):
            self.run(tt, MEET_T)
            self.play(FadeIn(c_mark), FadeIn(e_mark), run_time=0.5)
        with self.beat("שלב 3 : הנהג מסיע את ההולך ל-B,\nוהנוסע מגיע ברגל בדיוק באותו רגע."):
            self.run(tt, Fr(5, 2))
        dot = Dot(chart.pt(2.5, 1), radius=0.12, color=C.WHITE)
        self.say("שלושתם ב-B אחרי שעתיים וחצי,\nולאף אחד לא היה רגע של המתנה.", FadeIn(dot, scale=1.6))
        flat_w = Line(chart.pt(0, 0), chart.pt(float(MEET_T), float(C_POS)), stroke_color=W_COL, stroke_width=12,
                      stroke_opacity=0.45)
        flat_p = Line(chart.pt(float(D_DROP), float(D_DROP)), chart.pt(2.5, 1), stroke_color=P_COL,
                      stroke_width=12, stroke_opacity=0.45)
        self.say("שני הקטעים השטוחים מקבילים ושווים :\nכל אחד הולך שמינית ונוסע שבע שמיניות.",
                 Create(flat_w), Create(flat_p))
        self.fade_all()

    # -- the formula ---------------------------------------------------------------------------

    def segments(self) -> VGroup:
        """The road cut into y, x, z, x, r with the points Q, C, D, E (schematic lengths)."""
        lengths = [1.6, 1.3, 4.6, 1.3, 1.6]
        names = ["y", "x", "z", "x", "r"]
        xs = [-5.2]
        for L in lengths:
            xs.append(xs[-1] + L)
        yy = 2.85
        line = Line([xs[0], yy, 0], [xs[-1], yy, 0], stroke_color=C.MUTED, stroke_width=4)
        ticks = VGroup(*[Line([xx, yy - 0.15, 0], [xx, yy + 0.15, 0], stroke_color=C.MUTED, stroke_width=4)
                         for xx in xs])
        segs = VGroup(*[TX(n, size=36, color=C.AMBER).move_to([(a + b) / 2, yy + 0.4, 0])
                        for n, a, b in zip(names, xs, xs[1:])])
        pts = VGroup(*[TX(n, size=32, color=C.MUTED).move_to([xx, yy - 0.45, 0])
                       for n, xx in zip(["A", "Q", "C", "D", "E", "B"], xs)])
        return VGroup(line, ticks, segs, pts)

    def formula(self):
        alpha = TX(r"\alpha = \frac{v_1}{v_0} = \frac{t_0}{t_1} = 13", size=46).move_to(UP * 0.6)
        self.say("עכשיו הנוסחה. מסמנים את יחס המהירויות\nב-α : כמה פעמים האופנוע מהיר מההליכה.",
                 Write(alpha), run_time=1.4)
        self.play(FadeOut(alpha), run_time=0.5)
        seg = self.segments()
        self.say("הנקודות מחלקות את הדרך לחמישה קטעים :\n‏y, x, z, x ו-r, לפי הסדר מ-A.",
                 FadeIn(seg, lag_ratio=0.1), run_time=1.4)
        col_x = -4.8
        eq1 = TX(r"\alpha\, y = y + x + z", size=46)
        eq2 = TX(r"z = \alpha\, x", size=46)
        eq3 = TX(r"\alpha\, r = z + x + r", size=46)
        tags = [TX(r"(1)", size=34, color=C.MUTED), TX(r"(2)", size=34, color=C.MUTED),
                TX(r"(3)", size=34, color=C.MUTED)]
        rows = VGroup()
        for k, e in enumerate((eq1, eq2, eq3)):
            row = VGroup(tags[k], e).arrange(RIGHT, buff=0.4)
            row.move_to([0, 1.05 - 1.15 * k, 0]).align_to([col_x, 0, 0], LEFT)
            rows.add(row)
        self.say("שלב 1 : באותו זמן האופנוע עובר y + x + z,\nוההולך רק y. מהירות פי α, ולכן משוואה 1.",
                 FadeIn(rows[0]))
        self.say("שלב 2 : האופנוע חוזר z וההולך מתקדם x,\nבאותו זמן. לכן z = αx.", FadeIn(rows[1]))
        self.say("שימו לב : ההולך לא עומד במקום.\nהם מתקרבים במהירות v₁ + v₀, לא v₁.")
        self.say("שלב 3 : האופנוע עובר z + x + r\nבזמן שהנוסע הולך r. זו משוואה 3.", FadeIn(rows[2]))
        sym = TX(r"y = r = \frac{\alpha + 1}{\alpha - 1}\, x", size=46, color=C.AMBER)
        sym.move_to([3.3, -0.1, 0])
        self.say("מציבים z = αx במשוואות 1 ו-3,\nושתיהן נותנות את אותה תוצאה : y = r.",
                 FadeIn(sym, shift=0.2 * LEFT))
        self.say("הסימטריה יוצאת לבד : ההולך הולך y + x\nבהתחלה, והנוסע הולך x + r בסוף.")
        self.play(FadeOut(rows), FadeOut(sym), run_time=0.6)

        ab = TX(r"AB = 2x + 2y + \alpha x = \frac{\alpha(\alpha + 3)}{\alpha - 1}\, x", size=44)
        walk = TX(r"y + x = \frac{2}{\alpha + 3}\, AB", size=44)
        tline = TX(r"T = \frac{2}{\alpha + 3}\, t_0 + \frac{\alpha + 1}{\alpha + 3}\, t_1"
                   r" = \frac{3\alpha + 1}{\alpha + 3}\, t_1", size=44)
        block = VGroup(ab, walk, tline).arrange(DOWN, buff=0.6).move_to(DOWN * 0.25)
        self.say("מחברים את חמשת הקטעים, ומבטאים\nאת אורך הדרך כולה דרך x.", FadeIn(ab))
        self.say("מכאן ההולך הולך y + x, כלומר\nשתיים חלקי α + 3 מהדרך.", FadeIn(walk))
        self.say("ואת השאר הוא נוסע. הזמן הכולל שלו,\nוהוא גם הזמן של כולם : T.", FadeIn(tline))
        final = TX(r"T = \frac{3t_0 + t_1}{t_0 + 3t_1}\, t_1", size=56, color=C.AMBER)
        self.play(FadeOut(seg), FadeOut(ab), FadeOut(walk), tline.animate.move_to(UP * 2.0), run_time=0.8)
        final.move_to(UP * 0.45)
        self.say("מציבים α = t₀ / t₁, והמרחק נעלם :\nהנוסחה תלויה רק בשני הזמנים.", FadeIn(final, shift=0.2 * UP))
        check = TX(r"T = \frac{3 \cdot 13 + 1}{13 + 3 \cdot 1} = \frac{40}{16} = 2.5", size=44)
        check.move_to(DOWN * 1.25)
        self.say("בדיקה עם 13 ו-1 : ארבעים חלקי שש עשרה,\nכלומר שעתיים וחצי, כמו בגרף.", FadeIn(check))
        self.fade_all()

    def edges(self):
        title = TX(r"T = \frac{3\alpha + 1}{\alpha + 3}\, t_1", size=48, color=C.AMBER).move_to(UP * 1.9)
        slow = TX(r"\alpha \to 1 \;\Longrightarrow\; T \to t_1 = t_0", size=42).move_to(UP * 0.4)
        fast = TX(r"\alpha \to \infty \;\Longrightarrow\; T \to 3\, t_1", size=42).move_to(DOWN * 0.7)
        self.say("בדיקת שפיות במקרי הקצה :\nאופנוע איטי כמו הליכה לא עוזר בכלום.",
                 FadeIn(title), FadeIn(slow))
        self.say("ואופנוע מהיר מאוד עובר את הדרך שלוש פעמים :\nקדימה, אחורה וקדימה.", FadeIn(fast))
        self.fade_all()

    # -- the page's box -----------------------------------------------------------------------

    def box(self):
        view = BoxView(QID, "play", height=5.7).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד :\nהדרך, ומתחתיה אותו גרף בדיוק.", FadeIn(view))
        self.box_beat(view, [
            (1, "בסוף שלב 1 : הנוסע יורד ב-D,\nוההולך ב-Q, אחרי 0.875 שעות."),
            (2, "בסוף שלב 2 : האופנוע אוסף את ההולך ב-C,\nאחרי 1.625 שעות."),
            (3, "ובסוף שלב 3 שלושתם ב-B,\nאחרי 2.5 שעות."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        view = BoxView(QID, "values", height=5.7).move_to(UP * 0.62)
        self.say("בתיבה אפשר לשנות את הזמנים.\nזו התוכנית עם 13 ו-1.", FadeIn(view))
        self.box_beat(view, [
            (1, "עם הליכה של 4 שעות הנוסע יורד מוקדם יותר,\nוהזמן 13/7, בערך 1.86 שעות."),
            (2, "ועם שלושה שצריכים הסעה, כל אחד נוסע\nאותו מרחק : שלוש שעות ו-40 דקות."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        view = BoxView(QID, "drop", height=5.6).move_to(UP * 0.62)
        self.say("ולמה דווקא D? בשלב ההוכחה מזיזים\nאת נקודת הירידה, ורואים שני זמני הגעה.",
                 FadeIn(view))
        self.box_beat(view, [
            (1, "ירידה מוקדמת : הנוסע הולך הרבה\nומגיע אחרון."),
            (2, "ירידה מאוחרת : האופנוע חוזר מרחוק,\nוההולך מגיע אחרון."),
            (3, "המאוחר מהשניים הכי מוקדם כשהם שווים :\nבנקודה D, שבע שמיניות מהדרך."),
        ])
        self.fade_all()


class Closing(MotoScene):
    def construct(self):
        self.closing(QID, [("התוכנית", M("drop at 7/8, pick up at 1/8", 34)),
                           ("הזמן", TX(r"T = \frac{3t_0 + t_1}{t_0 + 3t_1}\, t_1 = 2.5\ \text{h}", size=40))],
                     ["לסיכום : הנוסע יורד בדרך, ושלושתם\nמגיעים יחד אחרי שעתיים וחצי.",
                      "נסו זמנים אחרים בתיבה\nשבעמוד של שאלה 0026 באתר."],
                     holds=(4.0, 4.5))
