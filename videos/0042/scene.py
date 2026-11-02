"""The tutorial video of question 0042, the camel and the water depots (script: script.md).

Render with `python videos/render.py 0042` (see VIDEOS.md). No code in this question's
video (the owner, 2026-11-02): part ב gets its formula and the reasoning behind it.

Part א draws the road from 0 to 400 km with the depots as water bars (a thin line at
every full load of 150) and the camel under the road with the litres on it, a running
count of the litres burned at the top. First the trap: three loads, three walks, 1.5
litres a km, which forgets the way back (five crossings, 2.5 litres; with 1.5 the answer
would be 440). Then the price list (j loads: 2j - 1 crossings), litres turned into km
(150 / 2.5 + 150 / 1.5 + 150 / 0.5 = 460, minus the 60 km the 30 delivered litres are
worth: 400), the stops where a whole load ends (60 and 160), and the plan played pass by
pass from tools/figures/q0042.py's passes(): every number on the screen is the
reference's. The water still in motion against the road (450 down to 30, its slopes the
price list) gives the bound, and the page's box plays the passes.

Part ב: the general price list g(N) = (2 ceil(N / c) - 1) a as a staircase, its reciprocal
1 / g as the km a litre buys, the range Phi as the area under it (300 + 100 + 60 = 460;
the 30 litres that must arrive are 60 of it), the closed form of d_max with k and r, the
bound (d/dx Phi(N(x)) <= -1), the stops, the check against part א, and the general box
with 250 litres. The bonus: one load, a target over one load (200 litres: 126.7 km), and
the logarithmic growth (the general box's chart with 1,500 and 3,000 litres).
"""

import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, SAFE_BOTTOM, TX, BoxView, DVQScene, M, he  # noqa: E402

import q0042  # noqa: E402

QID = 42
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – 450 ליטר, 150 על הגמל, 30 ליטר ליעד"),
    ("ChapterB", "סעיף ב – צריכה a, קיבולת c, מים w ויעד T"),
    ("Bonus", "בונוס – מקרים מיוחדים וכמה רחוק אפשר להגיע"),
    ("Closing", "סיכום"),
]

# The page's boxes: 0 is part א's (data-fixed: the page's numbers), 1 the general one.
# "plan": the passes one at a time (picture k after k passes, 9 in all). "general": 250
# litres instead of 450. "far": the chart of the distance against the water, at 1,500
# and at 3,000 litres.
BOXES = {
    "plan": {"box": 0, "region": [".ex-play-row", ".cm-sum", ".cm-road", ".cm-step"],
             "hide": [".viz-legend", ".cm-price-text"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 9}]},
    "general": {"box": 1, "region": [".cm-w", ".cm-sum", ".cm-road", ".cm-step"],
                "hide": [".ex-play-row", ".viz-legend", ".cm-price-text"],
                "steps": [[], [["fill", ".cm-w", "250"]]]},
    "far": {"box": 1, "region": [".cm-w", ".cm-sum", ".ex-title", ".cm-chart"],
            "hide": [".ex-play-row", ".viz-legend", ".cm-road", ".cm-step", ".cm-price-text"],
            "steps": [[], [["fill", ".cm-w", "1500"]], [["fill", ".cm-w", "3000"]]]},
}

# ---- the numbers, all from the page's reference (exact fractions) ------------------------

A, CAP, W, TGT = q0042.A, q0042.C, q0042.W, q0042.T
SEGS = q0042.segments(A, CAP, W, TGT)
PASSES = q0042.passes(A, CAP, W, TGT)
assert [(x0, x1, j) for x0, x1, j, _, _ in SEGS] == [(0, 60, 3), (60, 160, 2), (160, 400, 1)]
assert q0042.distance(A, CAP, W, TGT) == 400 == q0042.formula(A, CAP, W, TGT)
assert q0042.range_of(A, CAP, W) == 460 and TGT / A == 60
assert [q0042.price(j, A) for j in (3, 2, 1)] == [F(5, 2), F(3, 2), F(1, 2)]
assert [CAP / q0042.price(j, A) for j in (3, 2, 1)] == [60, 100, 300]
assert len(PASSES) == 9 and q0042.walked(A, CAP, W, TGT) == 840
# the passes of part א as the page's tables give them
assert [(p["carry0"], p["carry1"], p["drop"]) for p in PASSES if not p["back"]] == \
    [(150, 120, 90), (150, 120, 90), (150, 120, 120), (150, 100, 50), (150, 100, 100), (150, 30, 30)]
assert PASSES[4]["depots"][:2] == [0, 300] and PASSES[7]["depots"][1:3] == [0, 150]
assert PASSES[-1]["depots"] == [0, 0, 0, 30]
# the trap: three loads at 1.5 a km gives a first segment of 100 and 440 in all
assert CAP / (3 * A) == 100 and 100 + 100 + 300 - 60 == 440
# part ב: 250 litres (k = 2, r = 100), and the stops; the bonus
assert q0042.distance(A, CAP, 250, TGT) == F(920, 3) and q0042.stops(A, CAP, 250, TGT) == [F(200, 3)]
assert q0042.distance(A, CAP, 150, TGT) == 240
assert q0042.distance(A, CAP, W, 200) == F(380, 3) == 460 - q0042.range_of(A, CAP, 200)
assert q0042.range_of(A, CAP, 200) == F(1000, 3)
assert round(float(q0042.distance(A, CAP, 1500, TGT)), 1) == 580.0
assert round(float(q0042.distance(A, CAP, 3000, TGT)), 1) == 683.9
assert round(q0042.approx(A, CAP, W, TGT), 1) == 399.3 and CAP / (2 * A) == 150

# ---- the road ----------------------------------------------------------------------------

ROAD_Y, X0, X1 = -0.55, -5.3, 5.3
STOPS = [0, 60, 160, 400]
LITRE_H = 0.0062            # a depot bar's height per litre: 450 litres is 2.8 units
WATER = C.BLUE
CAMEL = C.ORANGE


def kx(km: float) -> float:
    return X0 + (X1 - X0) * float(km) / 400


def camel_icon() -> VGroup:
    """A camel facing right: the body, the hump, the neck and the head, four legs."""
    kw = dict(stroke_width=0, fill_color=CAMEL, fill_opacity=1)
    body = Ellipse(width=0.66, height=0.3, **kw)
    hump = Ellipse(width=0.34, height=0.3, **kw).move_to([-0.04, 0.13, 0])
    neck = Line([0.24, 0.02, 0], [0.38, 0.3, 0], stroke_color=CAMEL, stroke_width=9)
    head = Ellipse(width=0.2, height=0.11, **kw).move_to([0.45, 0.31, 0])
    legs = VGroup(*[Line([x, -0.06, 0], [x, -0.4, 0], stroke_color=CAMEL, stroke_width=6)
                    for x in (-0.22, -0.12, 0.12, 0.22)])
    return VGroup(legs, body, hump, neck, head)


def water_bar(litres: float, x: float, base: float, width: float = 0.36) -> VGroup:
    """A depot: a bar of water standing on the road, a thin line at every full load."""
    h = max(1e-3, float(litres) * LITRE_H)
    bar = Rectangle(width=width, height=h, stroke_width=0, fill_color=WATER, fill_opacity=0.85)
    bar.move_to([x, base + h / 2, 0])
    g = VGroup(bar)
    n = 1
    while n * 150 < litres - 1e-6:
        y = base + n * 150 * LITRE_H
        g.add(Line([x - width / 2, y, 0], [x + width / 2, y, 0], stroke_color=C.NAVY, stroke_width=3))
        n += 1
    return g


class Road(Group):
    """The road with its stops, the depots, the camel under the road with its load, and
    the litres burned so far. Trackers: pos (km), carry, face (+1 right, -1 left), burned,
    and one per depot."""

    def __init__(self, labels=(0, 60, 160, 400), ticks=STOPS, depots=None):
        super().__init__()
        self.pos, self.carry, self.face = ValueTracker(0), ValueTracker(0), ValueTracker(1)
        self.burned = ValueTracker(0)
        start = {0: W, 60: 0, 160: 0, 400: 0} if depots is None else depots
        self.dep = {s: ValueTracker(float(start[s])) for s in STOPS}
        line = Line([X0, ROAD_Y, 0], [X1, ROAD_Y, 0], stroke_color=C.MUTED, stroke_width=4)
        self.ticks = VGroup()
        for s in ticks:
            tick = Line([kx(s), ROAD_Y - 0.12, 0], [kx(s), ROAD_Y + 0.12, 0], stroke_color=C.MUTED, stroke_width=4)
            lab = M(str(s), 28, C.MUTED).move_to([kx(s), ROAD_Y - 0.36, 0])
            self.ticks.add(VGroup(tick, lab) if s in labels else VGroup(tick))
        unit = M("km", 26, C.MUTED).move_to([X1 + 0.62, ROAD_Y - 0.36, 0])
        self.base = VGroup(line, self.ticks, unit)
        self.bars = always_redraw(self._bars)
        self.camel = always_redraw(self._camel)
        self.add(self.base, self.bars)

    def _bars(self) -> VGroup:
        g = VGroup()
        for s in STOPS:
            v = self.dep[s].get_value()
            if v < 0.5:
                continue
            bar = water_bar(v, kx(s), ROAD_Y + 0.05)
            num = M(f"{v:.0f}", 28, WATER).next_to(bar, UP, buff=0.12)
            g.add(bar, num)
        return g

    def _camel(self) -> VGroup:
        x = kx(self.pos.get_value())
        icon = camel_icon()
        if self.face.get_value() < 0:
            icon.flip(UP)
        icon.move_to([x, ROAD_Y - 1.25, 0])
        c = self.carry.get_value()
        load = Rectangle(width=0.16, height=max(1e-3, c * 0.0042), stroke_width=0, fill_color=WATER,
                         fill_opacity=0.9)
        side = 0.6 if self.face.get_value() > 0 else -0.6
        load.move_to([x + side, ROAD_Y - 1.65 + load.height / 2, 0])
        num = M(f"{c:.0f}", 28, WATER)
        num.next_to(load, RIGHT if side > 0 else LEFT, buff=0.1).align_to(load, DOWN)
        return VGroup(icon, load, num)

    def counter(self) -> Mobject:
        return always_redraw(lambda: M(f"burned {self.burned.get_value():.0f} L", 30, C.MUTED)
                             .move_to([X0 + 1.4, 3.45, 0]))

    def mark(self, km: float) -> Line:
        """A stop lit amber."""
        return Line([kx(km), ROAD_Y - 0.16, 0], [kx(km), ROAD_Y + 0.16, 0], stroke_color=C.AMBER, stroke_width=7)


class CamelScene(DVQScene):
    """Helpers shared by the chapters of 0042: the camel's moves on the road."""

    fast = False      # the later segments: the camel runs, only the numbers update

    def walk(self, road: Road, to: float):
        d = abs(float(to) - road.pos.get_value())
        road.face.set_value(1 if float(to) > road.pos.get_value() else -1)
        self.play(road.pos.animate.set_value(float(to)),
                  road.carry.animate.set_value(road.carry.get_value() - float(A) * d),
                  road.burned.animate.set_value(road.burned.get_value() + float(A) * d),
                  run_time=0.5 if self.fast else max(0.8, d / 75), rate_func=linear)

    def take(self, road: Road, at: int, litres: float):
        self.play(road.dep[at].animate.set_value(road.dep[at].get_value() - float(litres)),
                  road.carry.animate.set_value(road.carry.get_value() + float(litres)), run_time=0.25 if self.fast else 0.45)

    def drop(self, road: Road, at: int, litres: float):
        self.play(road.dep[at].animate.set_value(road.dep[at].get_value() + float(litres)),
                  road.carry.animate.set_value(road.carry.get_value() - float(litres)), run_time=0.25 if self.fast else 0.45)

    def one_pass(self, road: Road, p: dict):
        """A pass of the reference's plan: out (take, walk, drop) or back (walk)."""
        x0, x1 = SEGS[p["seg"]][0], SEGS[p["seg"]][1]
        if p["back"]:
            self.walk(road, x0)
            return
        self.take(road, int(x0), p["carry0"])
        self.walk(road, x1)
        self.drop(road, int(x1), p["drop"])
        if p["drop"] == p["carry1"]:
            road.face.set_value(1)


class Opening(CamelScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "הגמל והמים",
                     ["א · 450 ליטר, 30 ליעד", "ב · צריכה, קיבולת, מים ויעד", "בונוס · מקרים מיוחדים"],
                     ["שאלה 0042 : הגמל והמים,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים ובונוס : המספרים של השאלה,\nהנוסחה הכללית, ומקרים מיוחדים."])
        self.fade_all()
        road = Road(labels=(0,), ticks=(0,))
        self.say("בהתחלה יש 450 ליטר מים,\nושלושה מטענים מלאים של 150.",
                 FadeIn(road.base), FadeIn(road.bars), run_time=1.2)
        self.say('הגמל נושא עד 150 ליטר, ושותה\nחצי ליטר לכל ק"מ, עם מטען או בלי.', FadeIn(road.camel))
        self.say('אפשר להשאיר מים במחסנים בדרך\nולחזור לקחת עוד. כמה רחוק מגיעים?')
        self.fade_all()


class ChapterA(CamelScene):
    def construct(self):
        self.chapter_card("סעיף א", "450 ליטר, 150 על הגמל, 30 ליטר ליעד",
                          'סעיף א : מה המרחק הגדול ביותר\nשאליו הגמל יכול להביא 30 ליטר?')
        self.trap()
        self.price_list()
        self.plan()
        self.bound()
        self.box()

    # -- the trap: forgetting the way back ------------------------------------------------------

    def trap(self):
        y0, xa, xb = 1.6, -3.0, 3.0
        seg = VGroup(Line([xa, y0, 0], [xb, y0, 0], stroke_color=C.MUTED, stroke_width=4),
                     Line([xa, y0 - 0.12, 0], [xa, y0 + 0.12, 0], stroke_color=C.MUTED, stroke_width=4),
                     Line([xb, y0 - 0.12, 0], [xb, y0 + 0.12, 0], stroke_color=C.MUTED, stroke_width=4))
        km = TX(r"1\ \text{km}", size=34, color=C.MUTED).next_to(seg, UP, buff=0.2)
        ys = [1.0, 0.25, -0.5]
        outs = VGroup(*[Arrow([xa, y, 0], [xb, y, 0], buff=0, color=C.AMBER, stroke_width=6) for y in ys])
        backs = VGroup(*[Arrow([xb, y, 0], [xa, y, 0], buff=0, color=C.RED, stroke_width=6)
                         for y in (0.625, -0.125)])
        naive = TX(r"3 \times 0.5 = 1.5", size=40).move_to([5.0, 0.25, 0])
        self.say('הניסיון הראשון : שלושה מטענים, שלוש הליכות,\nולכן כל ק"מ עולה 1.5 ליטר.',
                 FadeIn(seg), FadeIn(km), LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.3),
                 FadeIn(naive))
        self.say('אבל בין הליכה להליכה הגמל חוזר\nלקחת את המטען הבא, וגם זה שורף מים.',
                 LaggedStart(*[GrowArrow(a) for a in backs], lag_ratio=0.3))
        right = TX(r"5 \times 0.5 = 2.5", size=40, color=C.AMBER).move_to([5.0, -0.6, 0])
        cross = Line(naive.get_left() + LEFT * 0.1, naive.get_right() + RIGHT * 0.1, stroke_color=C.RED,
                     stroke_width=5)
        self.say('חמישה מעברים, לא שלושה :\nבהתחלה כל ק"מ עולה 2.5 ליטר.', Create(cross), FadeIn(right))
        wrong = TX(r"\frac{150}{1.5} + \frac{150}{1.5} + \frac{150}{0.5} - 60 = 440", size=40, color=C.MUTED)
        wrong.move_to([-1.2, -1.75, 0])
        wcross = Line(wrong.get_left() + LEFT * 0.1, wrong.get_right() + RIGHT * 0.1, stroke_color=C.RED,
                      stroke_width=5)
        self.say('חישוב שסופר רק הליכות קדימה : קטע ראשון\nשל 100 ק"מ, ותשובה של 440 ק"מ.', FadeIn(wrong))
        self.say('אבל לשם אי אפשר להגיע : הגמל\nלא יכול לדלג על הדרך חזרה.', Create(wcross))
        self.say('זו הטעות הנפוצה ביותר בחידה הזו :\nלספור רק את הדרך קדימה.')
        self.fade_all()

    # -- the price list, litres into km, the stops ------------------------------------------------

    def price_list(self):
        head = [TX(r"j", size=40, color=C.MUTED), TX(r"2j - 1", size=40, color=C.MUTED),
                TX(r"(2j - 1) \cdot 0.5", size=40, color=C.MUTED)]
        rows = [[TX(str(j), size=40), TX(str(2 * j - 1), size=40), TX(f"{(2 * j - 1) * 0.5:g}", size=40, color=C.AMBER)]
                for j in (3, 2, 1)]
        xs, y0 = [-3.0, 0.0, 3.4], 2.4
        table = VGroup()
        for r, cells in enumerate([head] + rows):
            for x, cell in zip(xs, cells):
                cell.move_to([x, y0 - 0.85 * r, 0])
                table.add(cell)
        rule = Line([-4.2, y0 - 0.45, 0], [4.8, y0 - 0.45, 0], stroke_color=C.FAINT, stroke_width=2)
        self.say('המחירון : עם j מטענים, j הליכות קדימה\nו-j − 1 חזרה, כלומר 2j − 1 מעברים.',
                 FadeIn(VGroup(*table[:3])), Create(rule))
        self.say('שלושה מטענים : 2.5 ליטר לק"מ.\nשניים : 1.5. מטען אחד : 0.5.',
                 LaggedStart(*[FadeIn(VGroup(*table[3 * r:3 * r + 3])) for r in (1, 2, 3)], lag_ratio=0.4))
        self.play(FadeOut(table), FadeOut(rule), run_time=0.6)

        phi = TX(r"\Phi(450) = \frac{150}{2.5} + \frac{150}{1.5} + \frac{150}{0.5}", size=42).move_to(UP * 2.0)
        phi2 = TX(r"= 60 + 100 + 300 = 460", size=42).next_to(phi, DOWN, buff=0.45).shift(RIGHT * 0.9)
        self.say('ליטר במחיר 2.5 לק"מ מקדם את המים\nרק 1/2.5 ק"מ. כך ליטרים הופכים לק"מ.', FadeIn(phi))
        self.say('המטען העליון שווה 60 ק"מ, הבא 100,\nוהאחרון 300 : ביחד 460.', FadeIn(phi2))
        keep = TX(r"\frac{30}{0.5} = 60", size=42).move_to(DOWN * 0.55)
        res = TX(r"d_{\max} = 460 - 60 = 400", size=50, color=C.AMBER).move_to(DOWN * 1.75)
        self.say('אבל 30 ליטר חייבים להגיע. במטען האחרון\nהם שווים 60 ק"מ שאסור לשרוף.', FadeIn(keep))
        self.say('נשארים 460 − 60 = 400 ק"מ.\nזו התשובה, ועכשיו התוכנית.', FadeIn(res, shift=0.2 * UP))
        self.fade_all()
        at50 = TX(r"450 - 50 \cdot 2.5 = 325 > 300", size=46).move_to(UP * 1.4)
        self.say('איפה לעצור? נניח ב-50 ק"מ, כי זה עגול.\nאחרי 50 ק"מ במחיר 2.5 נשארו 325 ליטר.', FadeIn(at50))
        loss = TX(r"10\ \text{km} \times 2.5 \quad \text{or} \quad 25\ \text{L spilled}", size=42,
                  color=C.RED).move_to(DOWN * 0.2)
        self.say('יותר משני מטענים : הקטע הבא עדיין\nמשלם 2.5 על עוד 10 ק"מ, או ששופכים 25.', FadeIn(loss))
        self.say('לכן עוצרים רק כשמטען שלם נגמר בדיוק :\nשם, ולא לפני, המחיר יורד.')
        self.fade_all()

    # -- the plan, pass by pass --------------------------------------------------------------

    def plan(self):
        road = Road()
        self.road = road
        cnt = road.counter()
        self.say('עוצרים בדיוק כשמטען שלם נגמר :\nב-60 ק"מ נשארו 300, וב-160 נשארו 150.',
                 FadeIn(road.base), FadeIn(road.bars), FadeIn(road.camel), FadeIn(cnt),
                 Create(road.mark(60)), Create(road.mark(160)), run_time=1.4)
        p = PASSES
        with self.beat('קטע 1, מ-0 ל-60 : כל הליכה שורפת 30.\nלוקח 150, מגיע עם 120, ומוריד 90.'):
            self.one_pass(road, p[0])
        with self.beat('חוזר עם 30, בדיוק מה שהדרך חזרה שורפת,\nומגיע להתחלה ריק.'):
            self.one_pass(road, p[1])
        with self.beat('לוקח עוד 150, ושוב מגיע עם 120\nומוריד 90. במחסן 60 יש 180.'):
            self.one_pass(road, p[2])
        with self.beat('חוזר שוב עם 30. בהתחלה נשאר\nמטען אחד אחרון, 150 ליטר.'):
            self.one_pass(road, p[3])
        with self.beat('בפעם השלישית הוא לא חוזר ומוריד הכול :\nבמחסן 60 יש 300 ליטר, שני מטענים.'):
            self.one_pass(road, p[4])
        self.say('חמישה מעברים של 60 ק"מ שרפו 150 ליטר,\nבדיוק מטען אחד. מכאן המחיר 1.5.')
        self.fast = True
        with self.beat('קטע 2, מ-60 ל-160, באותה שיטה : כל הליכה\nשורפת 50, הליכה, חזרה והליכה.'):
            self.one_pass(road, p[5])
            self.one_pass(road, p[6])
            self.one_pass(road, p[7])
        self.say('שלושה מעברים של 100 ק"מ שרפו 150 :\nבמחסן 160 יש 150 ליטר, מטען אחד.')
        with self.beat('קטע 3 : מטען אחד, בלי חזרות.\nהולך 240 ק"מ, שורף 120, ומגיע עם 30.'):
            self.one_pass(road, p[8])
        self.fast = False
        check = TX(r"150 + 150 + 120 + 30 = 450", size=40).move_to([1.4, 3.45, 0])
        self.say('‏400 ק"מ, עם 30 ליטר ביעד. בדיקה :\nכל ליטר נשרף בדרך או הגיע.', FadeIn(check))
        bands = VGroup()
        for (x0, x1, j, _, _), col in zip(SEGS, (C.RED, C.ORANGE, C.GREEN)):
            band = Line([kx(x0) + 0.06, ROAD_Y - 0.75, 0], [kx(x1) - 0.06, ROAD_Y - 0.75, 0], stroke_color=col,
                        stroke_width=8)
            times = M(f"x{2 * j - 1}", 28, col).next_to(band, DOWN, buff=0.15)
            price = M(f"{float(q0042.price(j, A)):g}", 28, col).next_to(times, DOWN, buff=0.1)
            bands.add(VGroup(band, times, price))
        self.play(FadeOut(road.camel), run_time=0.5)
        self.say('הגמל עבר את הקטע הראשון 5 פעמים,\nאת השני 3, ואת האחרון פעם אחת.',
                 LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.3))
        self.say('‏840 ק"מ הליכה בסך הכול,\nכדי להתקדם 400.')
        self.fade_all()

    # -- why no plan goes further ---------------------------------------------------------------

    def bound(self):
        ox, oy, w, h = -5.2, -1.9, 9.6, 4.6

        def pt(x, n):
            return np.array([ox + w * float(x) / 400, oy + h * float(n) / 450, 0])

        axes = VGroup(Line(pt(0, 0), pt(400, 0), stroke_color=C.MUTED, stroke_width=3),
                      Line(pt(0, 0), pt(0, 450), stroke_color=C.MUTED, stroke_width=3))
        for x in (0, 60, 160, 400):
            axes.add(M(str(x), 26, C.MUTED).next_to(pt(x, 0), DOWN, buff=0.15))
        for n in (30, 150, 300, 450):
            axes.add(DashedLine(pt(0, n), pt(400, n), stroke_color=C.FAINT, stroke_width=1.5))
            axes.add(M(str(n), 26, C.MUTED).next_to(pt(0, n), LEFT, buff=0.15))
        axes.add(M("km", 26, C.MUTED).next_to(pt(400, 0), RIGHT, buff=0.2))
        pts = [(0, 450), (60, 300), (160, 150), (400, 30)]
        curve = VMobject(stroke_color=WATER, stroke_width=6).set_points_as_corners([pt(*q) for q in pts])
        slopes = VGroup(TX(r"-2.5", size=34, color=C.AMBER).move_to(pt(20, 390) + RIGHT * 0.2),
                        TX(r"-1.5", size=34, color=C.AMBER).move_to(pt(115, 255)),
                        TX(r"-0.5", size=34, color=C.AMBER).move_to(pt(280, 120)))
        self.say('למה אי אפשר יותר? המים שעוד בתנועה\nיורדים מ-450 ל-30 לאורך הדרך.', FadeIn(axes), Create(curve),
                 run_time=1.6)
        self.say('השיפוע בכל קטע הוא המחירון :\nאין דרך להזיז מים בזול יותר.', FadeIn(slopes))
        self.say('כל ק"מ שורף לפחות ק"מ אחד מהטווח של 460,\nולכן 400 הוא המקסימום. ההוכחה בסעיף ב.')
        self.fade_all()

    # -- the page's box ------------------------------------------------------------------------

    def box(self):
        view = BoxView(QID, "plan", height=5.6).move_to(UP * 0.62)
        self.say('כך זה נראה בתיבה שבעמוד :\nהמעברים אחד אחרי השני.', FadeIn(view))
        self.box_beat(view, [
            (5, 'אחרי חמישה מעברים כל המים\nב-60 ק"מ : 300 ליטר.'),
            (9, 'והמעבר האחרון : 30 ליטר מגיעים\nל-400 ק"מ, והמחירון מתחת לכל קטע.'),
        ])
        self.fade_all()


class ChapterB(CamelScene):
    def construct(self):
        self.chapter_card("סעיף ב", "צריכה a, קיבולת c, מים w ויעד T",
                          'סעיף ב : הגמל שותה a לק"מ, נושא c,\nיש w ליטר, וצריך להביא T.')
        self.staircase()
        self.levels()
        self.formula()
        self.proof()
        self.box()

    def chart(self, top: float):
        """Axes for the water in motion N (0 to 450) across and a value up to `top`."""
        ox, oy, w, h = -5.6, -1.75, 6.6, 4.1

        def pt(n, v):
            return np.array([ox + w * float(n) / 450, oy + h * float(v) / top, 0])

        axes = VGroup(Line(pt(0, 0), pt(450, 0), stroke_color=C.MUTED, stroke_width=3),
                      Line(pt(0, 0), pt(0, top), stroke_color=C.MUTED, stroke_width=3))
        for n in (0, 150, 300, 450):
            axes.add(M(str(n), 26, C.MUTED).next_to(pt(n, 0), DOWN, buff=0.15))
        axes.add(TX(r"N", size=34, color=C.MUTED).next_to(pt(450, 0), RIGHT, buff=0.2))
        return pt, axes

    def staircase(self):
        pt, axes = self.chart(3.0)
        g = TX(r"g(N) = \left(2 \left\lceil \tfrac{N}{c} \right\rceil - 1\right) a", size=40).move_to([3.6, 2.6, 0])
        steps = VGroup(*[Line(pt(150 * i, (2 * i + 1) * 0.5), pt(150 * (i + 1), (2 * i + 1) * 0.5),
                              stroke_color=C.AMBER, stroke_width=6) for i in range(3)])
        vals = VGroup(*[M(f"{(2 * i + 1) * 0.5:g}", 28, C.AMBER).next_to(steps[i], UP, buff=0.12) for i in range(3)])
        self.say('המחירון הכללי : עם N ליטר בתנועה\nצריך ⌈N / c⌉ מטענים, וכל ק"מ עולה g(N).',
                 FadeIn(axes), FadeIn(g))
        self.say('המחיר הוא מדרגות, ויורד בכל כפולה של c.\nבדיוק שם כדאי לעצור.', Create(steps), FadeIn(vals))
        self.play(FadeOut(steps), FadeOut(vals), FadeOut(axes), run_time=0.6)

        pt, axes = self.chart(2.4)
        inv = [(0, 150, 2.0), (150, 300, 2 / 3), (300, 450, 0.4)]
        blocks = VGroup(*[Polygon(pt(a, 0), pt(b, 0), pt(b, v), pt(a, v), stroke_color=WATER, stroke_width=3,
                                  fill_color=WATER, fill_opacity=0.35) for a, b, v in inv])
        areas = VGroup(*[M(s, 30, C.WHITE).move_to(blk) for s, blk in zip(("300", "100", "60"), blocks)])
        areas[2].next_to(blocks[2], UP, buff=0.12)
        areas[1].next_to(blocks[1], UP, buff=0.12)
        phi = TX(r"\Phi(N) = \int_0^N \frac{dn}{g(n)}", size=40).move_to([3.6, 1.2, 0])
        self.say('ליטר במחיר g קונה 1/g ק"מ. הטווח של\nהמים הוא השטח מתחת ל-1/g.', FadeIn(axes), FadeIn(blocks),
                 FadeIn(phi))
        self.say('בנתוני סעיף א : 300 + 100 + 60 = 460,\nהמטענים מלמטה למעלה.', FadeIn(areas))
        self.say('המטען העליון שווה הכי מעט, 60 ק"מ,\nכי הוא נישא הכי הרבה פעמים.')
        strip = Polygon(pt(0, 0), pt(30, 0), pt(30, 2.0), pt(0, 2.0), stroke_width=0, fill_color=C.RED,
                        fill_opacity=0.75)
        t60 = M("60", 30, C.RED).next_to(strip, RIGHT, buff=0.12).align_to(strip, UP).shift(DOWN * 0.15)
        self.say('‏30 הליטרים שחייבים להגיע הם 60\nמהשטח : אותם לא שורפים.', FadeIn(strip), FadeIn(t60))
        d = TX(r"d_{\max} = \Phi(w) - \Phi(T) = 400", size=40, color=C.AMBER).move_to([3.6, -0.2, 0])
        self.say('המרחק המקסימלי הוא השטח שבין T ל-w :\nהטווח של המים פחות מה שחייב להגיע.', FadeIn(d))
        self.fade_all()

    def levels(self):
        lv = TX(r"w,\; (k-1)c,\; \dots,\; c,\; T \qquad 450,\; 300,\; 150,\; 30", size=42).move_to(UP * 2.4)
        self.say('הרמות : w, הכפולות של c שבין T ל-w,\nו-T. כל שתי רמות סמוכות הן קטע.', FadeIn(lv))
        seg = TX(r"L = \frac{N_0 - N_1}{(2j - 1)\, a}, \qquad j = \left\lceil \frac{N_0}{c} \right\rceil",
                 size=42).move_to(UP * 0.85)
        self.say('אורך הקטע : הירידה במים\nחלקי המחיר של המטענים שבו.', FadeIn(seg))
        ex = TX(r"\frac{150}{2.5} = 60, \quad \frac{150}{1.5} = 100, \quad \frac{120}{0.5} = 240", size=40,
                color=C.AMBER).move_to(DOWN * 0.55)
        self.say('בסעיף א : 60, 100 ו-240 ק"מ,\nשלושת הקטעים של התוכנית.', FadeIn(ex))
        self.fade_all()
        keep = TX(r"c - 2aL", size=46).move_to(UP * 2.3)
        self.say('בכל קטע j הליכות קדימה. בכל הליכה\nחוץ מהאחרונה הגמל לוקח מטען מלא.', FadeIn(keep))
        self.say('הוא שורף aL בדרך, שומר aL לחזרה,\nומשאיר c − 2aL במחסן הרחוק.')
        bal = TX(r"(2j - 1)\, a L = N_0 - N_1", size=46, color=C.AMBER).move_to(UP * 0.7)
        self.say('בהליכה האחרונה לוקח את השארית,\nהמטען החלקי, ומשאיר הכול.', FadeIn(bal))
        self.say('‏2j − 1 מעברים של L שורפים בדיוק\nאת הירידה : המחסן הרחוק מגיע לרמה הבאה.')
        self.fade_all()

    def formula(self):
        k = TX(r"k = \left\lceil \frac{w}{c} \right\rceil, \qquad r = w - (k - 1)\, c", size=42).move_to(UP * 2.3)
        self.say('נסמן k מטענים, שהעליון בהם חלקי,\nבגודל r : מה שנשאר מעל k − 1 מלאים.', FadeIn(k))
        dmax = TX(r"d_{\max} = \frac{1}{a} \left[ c \sum_{j=1}^{k-1} \frac{1}{2j - 1} + \frac{r}{2k - 1} - T \right]",
                  size=44, color=C.AMBER).move_to(UP * 0.4)
        self.say('כל מטען מלא מלמטה שווה c / (2j − 1)a,\nהחלקי שבראש שווה r / (2k − 1)a.', FadeIn(dmax))
        self.say('ומחסרים T / a : הק"מ ששווים\nהמים שצריכים להגיע.')
        self.say('עם T = 0 זה בדיוק Φ(w) : הגמל מגיע\nלכל היותר ל-460 ק"מ, ריק.')
        check = TX(r"\frac{1}{0.5}\left[150\left(1 + \tfrac{1}{3}\right) + \tfrac{150}{5} - 30\right] = 400",
                   size=40).move_to(DOWN * 1.5)
        self.say('בדיקה מול סעיף א : k = 3 ו-r = 150,\nוהנוסחה נותנת 400.', FadeIn(check))
        self.fade_all()

    def proof(self):
        intro = TX(r"\text{any plan} \;\Longrightarrow\; d \le 400\,?", size=46).move_to(UP * 1.2)
        self.say('נשאר להוכיח שאף תוכנית, גם תוכנית\nחכמה שלא חשבנו עליה, לא עוברת את זה.', FadeIn(intro))
        self.say('הרעיון : לספור כמה טווח כל ק"מ\nשל דרך שורף, בכל תוכנית שהיא.')
        self.fade_all()
        lines = [
            (r"\left\lceil \tfrac{N}{c} \right\rceil\ \text{forward} \;+\; \left(\left\lceil \tfrac{N}{c} \right\rceil - 1\right)\ \text{back}",
             'כל מעבר קדימה נושא לכל היותר c, אז N ליטר\nצריכים לפחות ⌈N / c⌉ מעברים, וחזרות ביניהם.'),
            (r"g(N) = \left(2 \left\lceil \tfrac{N}{c} \right\rceil - 1\right) a",
             'לכן כל ק"מ עולה לפחות g(N) :\nהמחירון הוא חסם תחתון על המחיר.'),
            (r"N'(x) \le -\,g\big(N(x)\big)",
             'לכן בכל תוכנית המים בתנועה יורדים\nלפחות בקצב g, בכל ק"מ.'),
            (r"\frac{d}{dx}\,\Phi\big(N(x)\big) = \frac{N'(x)}{g\big(N(x)\big)} \le -1",
             'ולפי כלל השרשרת, כל ק"מ של דרך\nשורף לפחות ק"מ אחד של טווח.'),
            (None, 'מסכמים לאורך הדרך : אחרי d ק"מ\nנשאר טווח של לכל היותר Φ(w) − d.'),
            (r"\Phi(T) \le \Phi\big(N(d)\big) \le \Phi(w) - d \;\Longrightarrow\; d \le \Phi(w) - \Phi(T)",
             'כדי ש-T ליטר יגיעו, d לא יכול לעבור\nאת Φ(w) − Φ(T). זו בדיוק הנוסחה.'),
        ]
        shown = []
        i = 0
        for tex, cap in lines:
            if tex is None:              # a caption on the same picture
                self.say(cap)
                continue
            m = TX(tex, size=38).move_to([0, 2.8 - 1.08 * i, 0])
            dim = [s.animate.set_opacity(0.45) for s in shown]
            self.say(cap, FadeIn(m), *dim)
            shown.append(m)
            i += 1
        self.fade_all()
        tight = TX(r"N'(x) = -\,g\big(N(x)\big)", size=46, color=C.AMBER).move_to(UP * 1.6)
        self.say('והתוכנית שעוצרת בכל כפולה של c\nמשלמת בדיוק לפי המחירון : היא מגיעה לחסם.', FadeIn(tight))
        self.say('עצירה במקום אחר : הגמל ממשיך לשלם\nעל מטען שכבר לא צריך, או שופך מים.')
        self.fade_all()
        stops = TX(r"Y_1 = \frac{r}{(2k - 1)\, a}, \qquad Y_i = Y_{i-1} + \frac{c}{(2k - 2i + 1)\, a}",
                   size=42).move_to(UP * 1.6)
        self.say('העצירה הראשונה כשהמטען החלקי נגמר,\nוכל עצירה אחריה כשנגמר מטען שלם.', FadeIn(stops))
        ex = TX(r"Y_1 = \frac{150}{5 \cdot 0.5} = 60, \qquad Y_2 = 60 + \frac{150}{3 \cdot 0.5} = 160",
                size=40, color=C.AMBER).move_to(DOWN * 0.3)
        self.say('בסעיף א : עצירות ב-60 וב-160 ק"מ,\nבדיוק כמו בתוכנית.', FadeIn(ex))
        last = TX(r"\frac{c - T}{a} = \frac{150 - 30}{0.5} = 240", size=40).move_to(DOWN * 1.75)
        self.say('ובעצירה ה-i נשארים (k − i)c ליטר. הקטע\nהאחרון, עם מטען אחד, באורך (c − T) / a.', FadeIn(last))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "general", height=5.6).move_to(UP * 0.62)
        self.say('בתיבה הכללית בוחרים צריכה, קיבולת,\nמים ויעד. אלה הנתונים של סעיף א.', FadeIn(view))
        self.box_beat(view, [
            (1, 'עם 250 ליטר : מטען חלקי של 100 למעלה,\nעצירה ב-66.7 ק"מ, ומרחק של 306.7.'),
        ])
        self.fade_all()


class Bonus(CamelScene):
    def construct(self):
        self.chapter_card("בונוס", "מקרים מיוחדים וכמה רחוק אפשר להגיע",
                          'בונוס : שלוש שאלות קצרות\nשבודקות שהנוסחה באמת מובנת.')
        one = TX(r"w \le c: \quad d_{\max} = \frac{w - T}{a} = \frac{150 - 30}{0.5} = 240", size=40)
        one.move_to(UP * 2.2)
        self.say('מטען אחד : אין עצירות, והגמל פשוט\nהולך עד שנשארים T ליטר. 150 ליטר : 240.',
                 FadeIn(one))
        big = TX(r"T = 200: \quad \Phi(450) - \Phi(200) = 460 - 333.3 = 126.7", size=40).move_to(UP * 0.6)
        self.say('יעד גדול ממטען : אותו עיקרון. 200 ליטר\nליעד מגיעים רק ל-126.7 ק"מ.', FadeIn(big))
        far = TX(r"d_{\max} \approx \frac{c}{2a}\left(\ln n + 1.96\right) - \frac{T}{a}", size=44,
                 color=C.AMBER).move_to(DOWN * 1.1)
        self.say('והרבה מים : הטור 1 + 1/3 + 1/5 ...\nמתבדר, אז אפשר להגיע לכל מרחק.', FadeIn(far))
        self.say('אבל לאט : כל הכפלה של המים פי e\nמוסיפה רק c / 2a, כאן 150 ק"מ.')
        self.fade_all()
        view = BoxView(QID, "far", height=5.6).move_to(UP * 0.62)
        self.say('בתיבה : המרחק המדויק מול כמות המים,\nוהקירוב מקווקו. ב-450 ליטר, 400 ק"מ.', FadeIn(view))
        self.box_beat(view, [
            (1, 'עם 1,500 ליטר, פי שלושה ויותר,\nרק 580 ק"מ.'),
            (2, 'ועם 3,000 ליטר : 683.9 ק"מ.\nהגידול לוגריתמי.'),
        ])
        self.fade_all()


class Closing(CamelScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"60,\ 160 \;\rightarrow\; 400\ \text{km}", size=40)),
                           ("ב", TX(r"d_{\max} = \Phi(w) - \Phi(T)", size=40)),
                           ("בונוס", TX(r"\approx \frac{c}{2a}(\ln n + 1.96) - \frac{T}{a}", size=40))],
                     ['לסיכום : עוצרים כשמטען שלם נגמר,\nומגיעים ל-400 ק"מ עם 30 ליטר.',
                      "נסו מים וקיבולת משלכם בתיבה\nשבעמוד של שאלה 0042 באתר."])
