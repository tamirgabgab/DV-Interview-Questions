"""The tutorial video of question 0032, wolf, goat and cabbage (script: script.md).

Render with `python videos/render.py 0032` (see notes/VIDEOS.md). The river is drawn in Manim
with simple icons (the owner, 2026-11-01: a farmer with a hat, a wolf, a goat and a
cabbage, no Hebrew in the picture), the near bank on the left as in the page's box. Part א
plays the seven crossings, then the page's box crossing by crossing (two forbidden tries
included), the step-by-step proof that seven is the least, and the trap after crossing 3.
Part ב: the state as four bits, the 16 states with the six unsafe ones struck, the ten
safe ones as a graph that the BFS fills layer by layer, the page's code typed (river_safe
with the constants, then river_plan), and its run beside the box's proof panel, the trace
jumping from the end of one layer to the end of the next (the owner, 2026-11-01).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 32
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – התוכנית"),
    ("ChapterB", "סעיף ב – קוד : מציאת התוכנית בחיפוש"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="river"). "plan": the crossing buttons clicked as a reader
# would: picture 0 the start, 1 a try with the wolf (the box refuses it: the goat is left
# with the cabbage), 2-4 goat, alone, wolf, 5 a try to go back alone (refused: the wolf
# with the goat), 6-9 the goat back, the cabbage, alone, the goat: everyone across in 7.
# "bfs": the proof panel, picture k after k clicks on "next layer" (layers 0 to 7).
BOXES = {
    "plan": {"box": 0, "region": [":scope > .ex-controls", ".river-frame", ".ex-summary"],
             "steps": [[], [["click", ".ex-go[data-item='wolf']"]],
                       [["click", ".ex-go[data-item='goat']"]],
                       [["click", ".ex-go[data-item='']"]],
                       [["click", ".ex-go[data-item='wolf']"]],
                       [["click", ".ex-go[data-item='']"]],
                       [["click", ".ex-go[data-item='goat']"]],
                       [["click", ".ex-go[data-item='cabbage']"]],
                       [["click", ".ex-go[data-item='']"]],
                       [["click", ".ex-go[data-item='goat']"]]]},
    "bfs": {"box": 0, "width": 480, "region": [".river-proof"], "hide": [".ex-proof-title"],
            "steps": [[], {"do": [["click", ".ex-bfs-next"]], "repeat": 7}]},
}

NAMES = ["farmer", "wolf", "goat", "cabbage"]
LETTER = {"farmer": "F", "wolf": "W", "goat": "G", "cabbage": "C"}
BIT = {"farmer": 1, "wolf": 2, "goat": 4, "cabbage": 8}
PLAN = ["goat", None, "wolf", "goat", "cabbage", None, "goat"]


def safe(s: int) -> bool:
    f, w, g, c = (bool(s & b) for b in (1, 2, 4, 8))
    return g == f or (g != w and g != c)


def layers() -> tuple[list[list[int]], dict]:
    """The BFS layers from 0 and every state's parents one layer up."""
    depth, parents, out = {0: 0}, {0: []}, [[0]]
    while True:
        d, nxt = len(out), []
        for s in out[-1]:
            for item in [None, "wolf", "goat", "cabbage"]:
                if item and bool(s & BIT[item]) != bool(s & 1):
                    continue
                t = s ^ 1 ^ (BIT[item] if item else 0)
                if not safe(t):
                    continue
                if t not in depth:
                    depth[t], parents[t] = d, []
                    nxt.append(t)
                if depth[t] == d:
                    parents[t].append(s)
        if not nxt:
            return out, parents
        out.append(nxt)


LAYERS, PARENTS = layers()
assert LAYERS == [[0], [5], [4], [7, 13], [2, 8], [11], [10], [15]], LAYERS
assert [s for s in range(16) if safe(s)] == [0, 2, 4, 5, 7, 8, 10, 11, 13, 15]


def banks(s: int) -> tuple[str, str]:
    near = "".join(LETTER[n] for n in NAMES if not s & BIT[n]) or "–"
    far = "".join(LETTER[n] for n in NAMES if s & BIT[n]) or "–"
    return near, far


# --------------------------------------------------------------------------------------
# The icons: simple shapes in the site's palette, about one unit high
# --------------------------------------------------------------------------------------

def _dot(x, y, r=0.035, color=None):
    return Circle(radius=r, fill_color=color or C.NAVY_DARK, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def farmer_icon() -> VGroup:
    shirt = RoundedRectangle(width=0.8, height=0.46, corner_radius=0.2, fill_color=C.BLUE,
                             fill_opacity=1, stroke_width=0).move_to(DOWN * 0.3)
    strap = VGroup(Line([-0.16, -0.08, 0], [-0.16, -0.5, 0]), Line([0.16, -0.08, 0], [0.16, -0.5, 0]))
    strap.set_stroke(C.NAVY_DARK, 4)
    head = Circle(radius=0.2, fill_color=C.CRATE_TOP, fill_opacity=1, stroke_width=0).move_to(UP * 0.08)
    brim = RoundedRectangle(width=0.66, height=0.08, corner_radius=0.04, fill_color=C.AMBER,
                            fill_opacity=1, stroke_width=0).move_to(UP * 0.25)
    crown = RoundedRectangle(width=0.36, height=0.22, corner_radius=0.07, fill_color=C.AMBER,
                             fill_opacity=1, stroke_width=0).move_to(UP * 0.37)
    eyes = VGroup(_dot(-0.07, 0.09), _dot(0.07, 0.09))
    return VGroup(shirt, strap, head, brim, crown, eyes)


def wolf_icon() -> VGroup:
    head = Polygon([-0.4, 0.46, 0], [-0.14, 0.2, 0], [0.14, 0.2, 0], [0.4, 0.46, 0], [0.38, 0.0, 0],
                   [0.14, -0.36, 0], [0.0, -0.46, 0], [-0.14, -0.36, 0], [-0.38, 0.0, 0],
                   fill_color=C.MUTED, fill_opacity=1, stroke_width=0)
    ears = VGroup(Polygon([-0.33, 0.36, 0], [-0.2, 0.2, 0], [-0.32, 0.12, 0]),
                  Polygon([0.33, 0.36, 0], [0.2, 0.2, 0], [0.32, 0.12, 0]))
    ears.set_fill(C.FAINT, 1).set_stroke(width=0)
    muzzle = Polygon([-0.14, -0.12, 0], [0.14, -0.12, 0], [0.0, -0.42, 0],
                     fill_color=C.WHITE, fill_opacity=0.85, stroke_width=0)
    nose = Polygon([-0.07, -0.33, 0], [0.07, -0.33, 0], [0.0, -0.42, 0],
                   fill_color=C.NAVY_DARK, fill_opacity=1, stroke_width=0)
    eyes = VGroup(_dot(-0.14, 0.03, 0.045, C.AMBER), _dot(0.14, 0.03, 0.045, C.AMBER))
    return VGroup(head, ears, muzzle, nose, eyes)


def goat_icon() -> VGroup:
    horns = VGroup(ArcBetweenPoints([-0.1, 0.28, 0], [-0.32, 0.5, 0], angle=-PI / 2.2),
                   ArcBetweenPoints([0.1, 0.28, 0], [0.32, 0.5, 0], angle=PI / 2.2))
    horns.set_stroke(C.CRATE_TOP, 7)
    ears = VGroup(Ellipse(width=0.3, height=0.12).move_to([-0.3, 0.12, 0]).rotate(-0.4),
                  Ellipse(width=0.3, height=0.12).move_to([0.3, 0.12, 0]).rotate(0.4))
    ears.set_fill(C.WHITE, 1).set_stroke(width=0)
    head = Ellipse(width=0.42, height=0.66, fill_color=C.WHITE, fill_opacity=1,
                   stroke_width=0).move_to(DOWN * 0.02)
    beard = Polygon([-0.08, -0.3, 0], [0.08, -0.3, 0], [0.0, -0.52, 0],
                    fill_color=C.MUTED, fill_opacity=1, stroke_width=0)
    eyes = VGroup(_dot(-0.09, 0.06), _dot(0.09, 0.06))
    nose = VGroup(_dot(-0.04, -0.2, 0.022), _dot(0.04, -0.2, 0.022))
    return VGroup(horns, ears, head, beard, eyes, nose)


def cabbage_icon() -> VGroup:
    outer = Circle(radius=0.42, fill_color=C.GREEN, fill_opacity=1, stroke_width=0)
    inner = Circle(radius=0.25, fill_color=C.GREEN, fill_opacity=1,
                   stroke_color=C.NAVY_DARK, stroke_width=3, stroke_opacity=0.45).shift(UP * 0.04)
    veins = VGroup(ArcBetweenPoints([-0.36, -0.2, 0], [-0.05, 0.3, 0], angle=-0.6),
                   ArcBetweenPoints([0.36, -0.2, 0], [0.05, 0.3, 0], angle=0.6),
                   ArcBetweenPoints([-0.3, 0.25, 0], [0.3, 0.25, 0], angle=-0.8))
    veins.set_stroke(C.NAVY_DARK, 3, opacity=0.45)
    return VGroup(outer, veins, inner)


ICON = {"farmer": farmer_icon, "wolf": wolf_icon, "goat": goat_icon, "cabbage": cabbage_icon}


def icon(name: str, height: float = 1.0) -> VGroup:
    g = ICON[name]()
    g.scale_to_fit_height(height)
    return g


# --------------------------------------------------------------------------------------
# The river
# --------------------------------------------------------------------------------------

NEAR_X, FAR_X = -4.95, 4.95
SLOTS = {"farmer": (-0.8, 1.55), "wolf": (0.8, 1.55), "goat": (-0.8, -0.05), "cabbage": (0.8, -0.05)}
DOCK = {0: -2.15, 1: 2.15}
BOAT_Y = -1.45


class River(VGroup):
    """The two banks, the river, the boat and the four icons; `side[name]` 0 near, 1 far."""

    def __init__(self, scale: float = 1.0):
        super().__init__()
        self.near = RoundedRectangle(width=3.3, height=5.0, corner_radius=0.25, fill_color=C.NAVY_LIGHT,
                                     fill_opacity=1, stroke_width=0).move_to([NEAR_X, 0.55, 0])
        self.far = self.near.copy().move_to([FAR_X, 0.55, 0])
        water = Rectangle(width=6.6, height=5.0, fill_color=C.BLUE, fill_opacity=0.16,
                          stroke_width=0).move_to([0, 0.55, 0])
        waves = VGroup(*[FunctionGraph(lambda x, k=k: 0.06 * np.sin(4 * x + k), x_range=[-2.6, 2.6])
                         .shift(UP * (2.4 - 0.75 * k)) for k in range(5)])
        waves.set_stroke(C.BLUE, 2, opacity=0.35)
        self.labels = VGroup(M("near", 28, C.MUTED).move_to([NEAR_X, -1.6, 0]),
                             M("far", 28, C.MUTED).move_to([FAR_X, -1.6, 0]))
        self.boat = VGroup(
            Polygon([-1.2, 0.2, 0], [1.2, 0.2, 0], [0.95, -0.22, 0], [-0.95, -0.22, 0],
                    fill_color=C.CRATE, fill_opacity=1, stroke_color=C.CRATE_EDGE, stroke_width=3),
        ).move_to([DOCK[0], BOAT_Y, 0])
        self.side = {n: 0 for n in NAMES}
        self.icons = {n: icon(n, 1.05).move_to(self.slot(n, 0)) for n in NAMES}
        self.add(water, waves, self.near, self.far, self.labels, self.boat, *self.icons.values())
        self.count = 0
        self.counter = VGroup(M("crossings:", 30, C.MUTED), M("0", 34, C.AMBER)).arrange(RIGHT, buff=0.2)
        self.counter.move_to([0, 2.75, 0])

    @staticmethod
    def slot(name: str, side: int) -> np.ndarray:
        x0 = NEAR_X if side == 0 else FAR_X
        dx, y = SLOTS[name]
        return np.array([x0 + dx, y, 0.0])

    def seat(self, k: int, side: int) -> np.ndarray:
        return np.array([DOCK[side] + (-0.5 if k == 0 else 0.5), BOAT_Y + 0.62, 0.0])

    def state(self) -> int:
        return sum(BIT[n] for n in NAMES if self.side[n])

    def cross(self, scene: DVQScene, item: str | None, count: bool = True) -> None:
        """One crossing: the farmer (and the item) board, the boat crosses, they step off."""
        a = self.side["farmer"]
        b = 1 - a
        who = ["farmer"] + ([item] if item else [])
        scene.play(*[self.icons[n].animate.move_to(self.seat(k, a)) for k, n in enumerate(who)],
                   run_time=0.6)
        shift = RIGHT * (DOCK[b] - DOCK[a])
        scene.play(self.boat.animate.shift(shift), *[self.icons[n].animate.shift(shift) for n in who],
                   run_time=1.1)
        for n in who:
            self.side[n] = b
        anims = [self.icons[n].animate.move_to(self.slot(n, b)) for n in who]
        if count:
            self.count += 1
            anims.append(Transform(self.counter[1], M(str(self.count), 34, C.AMBER).move_to(self.counter[1])))
        scene.play(*anims, run_time=0.6)

    def board(self, scene: DVQScene, item: str) -> None:
        """A try: the farmer and the item step onto the boat (not crossing yet)."""
        a = self.side["farmer"]
        scene.play(*[self.icons[n].animate.move_to(self.seat(k, a)) for k, n in enumerate(["farmer", item])],
                   run_time=0.6)

    def unboard(self, scene: DVQScene, item: str) -> None:
        scene.play(*[self.icons[n].animate.move_to(self.slot(n, self.side[n])) for n in ["farmer", item]],
                   run_time=0.6)

    def eats(self, a: str, b: str) -> Arrow:
        """A red arrow from the eater to the eaten."""
        p, q = self.icons[a].get_center(), self.icons[b].get_center()
        return Arrow(p, q, buff=0.45, color=C.RED, stroke_width=7, max_tip_length_to_length_ratio=0.3)


def crossing_chip(forward: bool, item: str | None, color: str | None = None) -> VGroup:
    """A crossing in a row: an arrow (right: forward, left: back) and the icon it carries."""
    color = color or (C.AMBER if forward else C.MUTED)
    arrow = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=color, stroke_width=6,
                  max_tip_length_to_length_ratio=0.3)
    if not forward:
        arrow.rotate(PI)
    top = icon(item, 0.62) if item else Circle(radius=0.08, fill_color=C.FAINT, fill_opacity=1,
                                                stroke_width=0)
    if item is None:
        top = VGroup(top, Rectangle(width=0.62, height=0.62, stroke_width=0, fill_opacity=0))
    return VGroup(top, arrow).arrange(DOWN, buff=0.18)


# --------------------------------------------------------------------------------------
# The state graph of part ב
# --------------------------------------------------------------------------------------

def tile(s: int, color: str | None = None) -> VGroup:
    near, far = banks(s)
    box = RoundedRectangle(width=1.3, height=1.0, corner_radius=0.12, fill_color=C.NAVY_LIGHT,
                           fill_opacity=1, stroke_color=color or C.FAINT, stroke_width=3)
    top = M(near, 28).move_to(box.get_center() + UP * 0.21)
    bot = M(far, 28, C.MUTED).move_to(box.get_center() + DOWN * 0.21)
    rule = Line(box.get_left() + RIGHT * 0.12, box.get_right() + LEFT * 0.12, stroke_color=C.FAINT,
                stroke_width=2)
    return VGroup(box, rule, top, bot)


def graph_positions(x_pitch: float = 1.72, y_gap: float = 2.1, y0: float = 0.55) -> dict:
    pos = {}
    for d, layer in enumerate(LAYERS):
        for k, s in enumerate(layer):
            y = y0 + (len(layer) - 1) * y_gap / 2 - k * y_gap
            pos[s] = np.array([(d - 3.5) * x_pitch, y, 0.0])
    return pos


def state_fmt(name: str, st: dict) -> str:
    if name not in st:
        return ""
    v = st[name]
    if name == "s":
        return f"{v} = {v:04b}"
    if name == "queue":
        return "[" + ", ".join(str(x) for x in v) + "]"
    return repr(v)


# --------------------------------------------------------------------------------------
# The scenes
# --------------------------------------------------------------------------------------


class Opening(DVQScene):
    def construct(self):
        self.opening(QID, "סטודנט", "זאב, עז וכרוב",
                     ["א · התוכנית", "ב · חיפוש בקוד"],
                     ["שאלה 0032 : זאב, עז וכרוב,\nשאלה ברמת סטודנט.",
                      "שני סעיפים : קודם התוכנית ביד,\nואז קוד שמוצא אותה לבד."])
        self.fade_all()
        river = River()
        self.say("איכר צריך להעביר זאב, עז וכרוב\nלגדה הרחוקה של הנהר.",
                 FadeIn(river, lag_ratio=0.05), run_time=1.6)
        seats = [river.seat(0, 0), river.seat(1, 0)]
        rings = VGroup(*[Circle(radius=0.5, color=C.AMBER, stroke_width=4).move_to(p) for p in seats])
        self.say("בסירה יש מקום לאיכר ועוד אחד בלבד,\nורק האיכר יודע לחתור.", Create(rings))
        self.play(FadeOut(rings), run_time=0.4)
        a1, a2 = river.eats("wolf", "goat"), river.eats("goat", "cabbage")
        self.say("בלי האיכר, הזאב אוכל את העז,\nוהעז אוכלת את הכרוב.", GrowArrow(a1), GrowArrow(a2))
        self.say("כמה חציות צריך לכל הפחות\nכדי להעביר את שלושתם בשלום?", FadeOut(a1), FadeOut(a2),
                 run_time=0.6)
        self.fade_all()


class ChapterA(DVQScene):
    def construct(self):
        self.chapter_card("סעיף א", "התוכנית",
                          "סעיף א : למצוא סדר חציות,\nולהראות שאין קצר ממנו.")

        # The idea: the only safe pair, so the goat goes first.
        river = River()
        self.play(FadeIn(river), run_time=0.8)
        ok = DashedLine(river.icons["wolf"].get_center(), river.icons["cabbage"].get_center(),
                        buff=0.55, color=C.GREEN, stroke_width=6)
        check = M("ok", 30, C.GREEN).next_to(ok, RIGHT, buff=0.15)
        self.say("הרעיון : הזוג היחיד שבטוח להשאיר לבד\nהוא הזאב והכרוב.", Create(ok), FadeIn(check))
        self.play(FadeOut(ok), FadeOut(check), run_time=0.4)
        with self.beat("אם האיכר לוקח קודם את הזאב,\nהעז נשארת עם הכרוב."):
            river.board(self, "wolf")
            bad = river.eats("goat", "cabbage")
            self.play(GrowArrow(bad), run_time=0.6)
        with self.beat("ואם הוא לוקח את הכרוב,\nהעז נשארת עם הזאב."):
            self.play(FadeOut(bad), run_time=0.3)
            river.unboard(self, "wolf")
            river.board(self, "cabbage")
            bad = river.eats("wolf", "goat")
            self.play(GrowArrow(bad), run_time=0.6)
        with self.beat("לכן בחצייה הראשונה האיכר\nחייב לקחת את העז."):
            self.play(FadeOut(bad), run_time=0.3)
            river.unboard(self, "cabbage")
            self.play(Indicate(river.icons["goat"], color=C.AMBER, scale_factor=1.25), run_time=1.0)

        # The steps: the seven crossings.
        self.play(FadeIn(river.counter), run_time=0.5)
        with self.beat("חצייה 1 : האיכר לוקח את העז.\nהזאב והכרוב נשארים יחד, וזה בטוח."):
            river.cross(self, "goat")
        with self.beat("חצייה 2 : האיכר חוזר לבד.\nהעז לבד בצד הרחוק."):
            river.cross(self, None)
        with self.beat("חצייה 3 : האיכר לוקח את הזאב.\nעכשיו הזאב והעז בצד הרחוק."):
            river.cross(self, "wolf")
        bad = river.eats("wolf", "goat")
        self.say("אם הוא יחזור עכשיו לבד,\nהזאב יאכל את העז.", GrowArrow(bad))
        with self.beat("חצייה 4 : הצעד שמפספסים.\nהאיכר מחזיר את העז לגדה הקרובה."):
            self.play(FadeOut(bad), run_time=0.3)
            river.cross(self, "goat")
        self.say("זה נראה כמו בזבוז של חצייה,\nאבל בלי הצעד הזה אין פתרון.",
                 Indicate(river.icons["goat"], color=C.AMBER, scale_factor=1.25), run_time=1.0)
        with self.beat("חצייה 5 : האיכר לוקח את הכרוב.\nבצד הרחוק הזאב והכרוב, וזה בטוח."):
            river.cross(self, "cabbage")
        with self.beat("חצייה 6 : האיכר חוזר לבד.\nהעז לבד על הגדה הקרובה."):
            river.cross(self, None)
        with self.beat("חצייה 7 : האיכר לוקח את העז.\nכולם בצד הרחוק, אחרי שבע חציות."):
            river.cross(self, "goat")
        self.say("אפשר גם להחליף את התפקידים :\nהכרוב בחצייה 3, והזאב בחצייה 5.",
                 Indicate(VGroup(river.icons["wolf"], river.icons["cabbage"]), color=C.AMBER),
                 run_time=1.0)
        self.fade_all()

        # The page's box, alone: the same plan by its buttons, two refused tries included.
        view = BoxView(QID, "plan", width=12.4, height=5.6).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד :\nבוחרים מי עולה לסירה עם האיכר.", FadeIn(view))
        self.box_beat(view, [
            (1, "ניסיון עם הזאב : התיבה מבטלת אותו,\nכי העז והכרוב נשארים לבד."),
        ])
        with self.beat("עם העז, חזרה לבד, ועם הזאב :\nשלוש החציות הראשונות."):
            for k in (2, 3, 4):
                self.box_step(view, k)
        self.box_beat(view, [
            (5, "ועכשיו חזרה לבד? גם היא מבוטלת :\nהזאב והעז נשארים יחד."),
        ])
        with self.beat("לכן מחזירים את העז, ואז הכרוב,\nחזרה לבד, והעז : שבע חציות."):
            for k in (6, 7, 8, 9):
                self.box_step(view, k)
        self.fade_all()

        # Why it works: seven is the least, step by step.
        def row(spec, y):
            r = VGroup(*[crossing_chip(f, it) for f, it in spec]).arrange(RIGHT, buff=0.35)
            return r.scale(1.45).move_to(UP * y)

        three = row([(True, None)] * 3, 1.8)
        q3 = VGroup(*[M("?", 34, C.AMBER).move_to(c[0]) for c in three])
        self.say("למה אי אפשר פחות משבע? כל חצייה קדימה\nמעבירה לכל היותר פריט אחד.",
                 FadeIn(three, lag_ratio=0.2), FadeIn(q3), run_time=1.2)
        five = row([(True, None), (False, None), (True, None), (False, None), (True, None)], 1.8)
        n5 = TX(r"3 + 2 = 5", size=40, color=C.AMBER).next_to(five, DOWN, buff=0.4)
        self.say("לכן לפחות שלוש חציות קדימה, וביניהן\nשתי חזרות : חמש חציות לפחות.",
                 ReplacementTransform(three, five), FadeOut(q3), FadeIn(n5))
        tight = row([(True, "goat"), (False, None), (True, "wolf"), (False, None), (True, None)], 1.8)
        self.say("בחמש בדיוק, כל קדימה מעבירה פריט,\nוכל חזרה היא לבד. הראשון חייב להיות העז.",
                 ReplacementTransform(five, tight))
        cross = Cross(tight[3], stroke_color=C.RED, stroke_width=10, scale_factor=0.9)
        why = VGroup(icon("wolf", 0.9), M("+", 40, C.RED), icon("goat", 0.9)).arrange(RIGHT, buff=0.25)
        why.next_to(tight[3], DOWN, buff=1.0)
        self.say("אבל בחזרה השנייה, הפריט השני נשאר\nבצד הרחוק עם העז, בלי האיכר.",
                 Create(cross), FadeIn(why), FadeOut(n5))
        seven = row([(True, "goat"), (False, None), (True, "wolf"), (False, "goat"),
                     (True, "cabbage"), (False, None), (True, "goat")], 1.8)
        n7 = TX(r"5 + 2 = 7", size=40, color=C.AMBER).next_to(seven, DOWN, buff=0.4)
        self.say("לכן אחת החזרות לוקחת פריט, והוא צריך\nעוד חצייה קדימה : שבע לפחות.",
                 FadeOut(cross), FadeOut(why), ReplacementTransform(tight, seven), FadeIn(n7))
        self.say("והתוכנית שראינו עושה את זה בדיוק\nבשבע : המספר הקטן ביותר.",
                 Indicate(seven[3], color=C.AMBER, scale_factor=1.2), run_time=1.0)
        self.fade_all()

        # The cost: few states.
        chips = cost_chips(("states", "$2^4 = 16$"), ("safe", "$10$"),
                           notes=("4 things, 2 banks", "nobody eaten"))
        self.say("ארבעה דברים, כל אחד באחת משתי גדות :\n‏16 מצבים, ורק עשרה מהם בטוחים.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: stuck after crossing 3.
        river = River()
        for item in ("goat", None, "wolf"):
            for n in ["farmer"] + ([item] if item else []):
                river.side[n] = 1 - river.side[n]
        for n in NAMES:
            river.icons[n].move_to(river.slot(n, river.side[n]))
        river.boat.move_to([DOCK[1], BOAT_Y, 0])
        bad = river.eats("wolf", "goat")
        self.say("מלכודת : אחרי חצייה 3 נדמה שאין מהלך.\nחזרה לבד משאירה את הזאב עם העז.",
                 FadeIn(river), GrowArrow(bad), run_time=1.2)
        with self.beat("חזרה עם הזאב מבטלת את חצייה 3 :\nחוזרים למצב שאחרי חצייה 2."):
            self.play(FadeOut(bad), run_time=0.3)
            river.cross(self, "wolf", count=False)
            back = M("= after crossing 2", 32, C.RED).move_to([0, 2.75, 0])
            self.play(FadeIn(back), run_time=0.5)
        with self.beat("נשארת רק העז : להחזיר משהו\nלגדה הקרובה, ולא להיתקע."):
            self.play(FadeOut(back), run_time=0.3)
            river.cross(self, "wolf", count=False)
            river.cross(self, "goat", count=False)
        self.fade_all()


class ChapterB(DVQScene):
    def construct(self):
        self.chapter_card("סעיף ב", "קוד : מציאת התוכנית בחיפוש",
                          "סעיף ב : קוד שמוצא את התוכנית\nבעצמו, בלי לדעת אותה מראש.")

        # The idea: a state is four bits.
        icons = VGroup(*[icon(n, 0.9) for n in reversed(NAMES)]).arrange(RIGHT, buff=0.9).move_to(UP * 2.2)
        letters = VGroup(*[M(LETTER[n], 36, C.AMBER).next_to(ic, DOWN, buff=0.25)
                           for n, ic in zip(reversed(NAMES), icons)])
        weights = VGroup(*[M(str(BIT[n]), 30, C.MUTED).next_to(l, DOWN, buff=0.2)
                           for n, l in zip(reversed(NAMES), letters)])
        self.say("המצב : ביט לכל אחד מהארבעה.\n‏0 בגדה הקרובה, 1 בגדה הרחוקה.",
                 FadeIn(icons, lag_ratio=0.15), FadeIn(letters), FadeIn(weights), run_time=1.4)
        bits = VGroup(*[M(b, 44) .next_to(w, DOWN, buff=0.35) for b, w in zip("0101", weights)])
        bits[1].set_color(C.AMBER)
        bits[3].set_color(C.AMBER)
        val = M("= 5", 44, C.AMBER).next_to(bits, RIGHT, buff=0.4)
        self.say("למשל אחרי החצייה הראשונה, האיכר והעז\nרחוקים : 0101 = 5.", FadeIn(bits), FadeIn(val))
        ends = VGroup(M("start 0000 = 0", 34), M("goal  1111 = 15", 34, C.GREEN)).arrange(DOWN, buff=0.25,
                                                                                            aligned_edge=LEFT)
        ends.next_to(bits, DOWN, buff=0.55)
        self.say("ההתחלה 0000, כולם קרובים,\nוהסיום 1111, כולם רחוקים.", FadeIn(ends))
        self.fade_all()

        # The check: the 16 states, the six unsafe ones struck.
        tiles = {s: tile(s) for s in range(16)}
        grid = VGroup(*[tiles[s] for s in range(16)]).arrange_in_grid(rows=2, cols=8, buff=(0.2, 0.45))
        grid.move_to(UP * 0.6 + RIGHT * 0.65)
        legend = VGroup(M("near", 26, C.WHITE), M("far", 26, C.MUTED)).arrange(DOWN, buff=0.12)
        legend.next_to(grid, LEFT, buff=0.3)
        self.say("כל 16 המצבים : למעלה מי בגדה הקרובה,\nולמטה מי בגדה הרחוקה.",
                 FadeIn(grid, lag_ratio=0.04), FadeIn(legend), run_time=1.4)
        rule = TX(r"\text{safe} \iff g = f \ \ \text{or} \ \ (g \ne w \ \text{and} \ g \ne c)",
                  size=34, color=C.AMBER).next_to(grid, DOWN, buff=0.5)
        self.say("מצב בטוח : העז עם האיכר, או שהעז\nרחוקה גם מהזאב וגם מהכרוב.", FadeIn(rule))
        bad = [s for s in range(16) if not safe(s)]
        strikes = VGroup(*[Line(tiles[s].get_corner(DL), tiles[s].get_corner(UR), color=C.RED, stroke_width=6)
                           for s in bad])
        self.say("ששה מצבים נפסלים, ונשארים עשרה.\nבכל ששת הפסולים העז בלי האיכר.",
                 Create(strikes, lag_ratio=0.15), *[tiles[s].animate.set_opacity(0.4) for s in bad],
                 run_time=1.4)

        # The edges, and the graph by layers.
        pos = graph_positions()
        self.play(FadeOut(strikes), FadeOut(rule), FadeOut(legend),
                  *[FadeOut(tiles[s]) for s in bad], run_time=0.6)
        edges = VGroup()
        edge_of = {}
        for t, ps in PARENTS.items():
            for p in ps:
                e = Line(pos[p], pos[t], stroke_color=C.FAINT, stroke_width=3)
                edge_of[(p, t)] = e
                edges.add(e)
        heads = VGroup(*[M(str(d), 28, C.MUTED).move_to([pos[layer[0]][0], 2.95, 0])
                         for d, layer in enumerate(LAYERS)])
        layer_word = M("layer", 28, C.MUTED).next_to(heads[0], UP, buff=0.12)
        with self.beat("קשת : האיכר חוצה, ואיתו לכל היותר\nפריט אחד מהצד שלו. כל חצייה שווה."):
            for s in pos:
                tiles[s].set_z_index(2)
            self.play(*[tiles[s].animate.move_to(pos[s]) for s in pos], run_time=1.4)
            self.add(edges)
            self.bring_to_front(*[tiles[s] for s in pos])
            self.play(Create(edges, lag_ratio=0.1), run_time=1.0)
        self.say("לכן מחפשים לרוחב, BFS : שכבה אחרי\nשכבה, לפי המרחק מההתחלה.",
                 FadeIn(heads, lag_ratio=0.1), FadeIn(layer_word))

        def light(d):
            anims = []
            for s in LAYERS[d]:
                anims.append(tiles[s][0].animate.set_stroke(C.AMBER, 5))
                for p in PARENTS[s]:
                    anims.append(edge_of[(p, s)].animate.set_stroke(C.BLUE, 5))
            if d > 0:
                for s in LAYERS[d - 1]:
                    anims.append(tiles[s][0].animate.set_stroke(C.GREEN, 4))
            anims.append(heads[d].animate.set_color(C.AMBER))
            return anims

        self.say("שכבה 0 : מצב ההתחלה, 0000.", *light(0), run_time=0.8)
        self.say("שכבה 1 : רק חצייה אחת בטוחה,\nעם העז.", *light(1), run_time=0.8)
        self.say("שכבה 2 : האיכר חוזר לבד. חזרה עם העז\nמובילה ל-0000, שכבר נמצא.", *light(2), run_time=0.8)
        self.say("שכבה 3 : שני מצבים חדשים,\nעם הזאב או עם הכרוב.", *light(3), run_time=0.8)
        with self.beat("שכבות 4 ו-5 : מחזירים את העז,\nומביאים את הפריט השני."):
            self.play(*light(4), run_time=0.8)
            self.play(*light(5), run_time=0.8)
        with self.beat("שכבה 6 : חזרה לבד. שכבה 7 : הסיום,\n‏1111, במרחק שבע מההתחלה."):
            self.play(*light(6), run_time=0.8)
            self.play(*light(7), run_time=0.8)
        paths = VGroup(*[edge_of[k].copy().set_stroke(C.AMBER, 7) for k in edge_of]).set_z_index(1)
        self.say("שני מסלולים באורך שבע : הזאב לפני\nהכרוב, או הכרוב לפני הזאב.",
                 Create(paths, lag_ratio=0.05), run_time=1.4)
        self.fade_all()

        # The code: the constants and river_safe, then river_plan.
        code = page_python(QID, "def river_plan")
        pa = CodePanel(code, font_size=34, drop_trailing_comments=True, only=[1, 3, 4, 5, 8, 10, 11])
        self.place_code(pa)
        self.type_code(pa, [
            (1, "התור של BFS : deque\nמהספרייה הסטנדרטית."),
            ([3, 4], "הביט של כל אחד, ו-EVERYONE = 15,\nכולם רחוקים."),
            (5, "‏CARGO : מה האיכר יכול לקחת :\nכלום, את הזאב, את העז או את הכרוב."),
            ([8, 10, 11], "‏river_safe : ארבעת הביטים, והתנאי\nשראינו : העז עם האיכר, או רחוקה משניהם."),
        ], intro="עכשיו נכתוב את זה ב-Python.\nקודם הקבועים ובדיקת הבטיחות.")
        self.play(FadeOut(pa), run_time=0.6)

        plan_lines = [14] + list(range(16, 34))
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=plan_lines, rows=15)
        vp = VarPanel(["s", "item", "queue"], fmt=state_fmt, size=28, cols=2, slot=4.3).set_state({})
        self.place_code(panel, vp_width=8.0)
        self.type_code(panel, [
            ([14, 16, 17], "‏river_plan : ההורה של 0 הוא None,\nוהתור מתחיל עם 0."),
            ([18, 19, 20, 21], "שולפים מצב מהתור.\nאם הוא 15, הגענו לסיום."),
            ([22, 23, 24], "לכל פריט : אם הוא בצד השני\nמהאיכר, הוא לא יכול לעלות לסירה."),
            (25, "החצייה הופכת את הביט של האיכר\nואת הביט של מה שהוא לוקח."),
            ([26, 27, 28], "מצב בטוח שעוד לא ראינו : רושמים\nמאיפה באנו ומה נלקח, ומכניסים לתור."),
            ([29, 30, 31, 32, 33], "השחזור : מ-15 אחורה לפי ההורים,\nואז הופכים את הרשימה."),
        ])

        # The run beside the box's BFS panel, a layer at a time.
        steps, result = trace(code, "river_plan", ())
        assert result == PLAN, result
        ran = [s.line for s in steps]
        cut = [i for i, n in enumerate(ran) if n == 18]                   # each `while queue`
        pops = [steps[i + 1].state["s"] for i in cut]
        assert pops == [s for layer in LAYERS for s in layer], pops
        brk = ran.index(21)
        chunks = [ran[:cut[0]]]
        k = 0
        for layer in LAYERS[:-1]:
            a = cut[k]
            k += len(layer)
            chunks.append(ran[a:cut[k]])
        chunks.append(ran[cut[k]:brk + 1])
        chunks.append(ran[brk + 1:])
        assert sum(chunks, []) == ran
        view = BoxView(QID, "bfs")
        with self.beat("נריץ את river_plan, לצד השכבות\nשל ה-BFS בתיבה מהעמוד."):
            self.split(panel, view, vp)
        caps = [
            "בהתחלה בתור רק 0,\nוההורה שלו None.",
            "שולפים את 0. רק החצייה עם העז\nבטוחה : 5 נכנס לתור.",
            "שולפים את 5. חזרה לבד נותנת 4.\nחזרה עם העז היא 0, שכבר נמצא.",
            "שולפים את 4 : עם הזאב 7,\nועם הכרוב 13. שניהם נכנסים לתור.",
            "שולפים את 7 ואת 13.\nמכל אחד העז חוזרת : 2 ו-8.",
            "מ-2 ומ-8 מגיעים ל-11. הוא נכנס פעם אחת,\nמ-2, שנשלף קודם.",
            "שולפים את 11 : האיכר חוזר לבד,\nו-10 נכנס לתור.",
            "שולפים את 10 : עם העז מגיעים ל-15,\nהסיום, והוא נכנס לתור.",
            "שולפים את 15, וה-break\nעוצר את הלולאה.",
            "השחזור הולך מ-15 אחורה עד 0,\nואוסף את מה שנלקח בכל חצייה.",
        ]
        frames = [0, 1, 2, 3, 4, 5, 6, 7, None, None]
        self.run_code(panel, vp, steps, list(zip(chunks, caps, frames)), view=view)
        self.fade_all()
        seven = VGroup(*[crossing_chip(f, it) for f, it in
                         zip([True, False] * 3 + [True], PLAN)]).arrange(RIGHT, buff=0.35)
        seven.move_to(UP * 1.6)
        listed = M("['goat', None, 'wolf', 'goat', 'cabbage', None, 'goat']", 26, C.AMBER)
        listed.next_to(seven, DOWN, buff=0.5)
        self.say("ההפוך הוא התוכנית של סעיף א :\nעז, לבד, זאב, עז, כרוב, לבד, עז.",
                 FadeIn(seven, lag_ratio=0.15), FadeIn(listed), run_time=1.4)
        depth = TX(r"\text{depth}(15) = 7", size=40, color=C.GREEN).next_to(listed, DOWN, buff=0.5)
        self.say("למה זה נכון? BFS מגיע למצבים לפי\nהמרחק מההתחלה, ו-15 נכנס בשכבה 7.", FadeIn(depth))
        self.say("לכן אין מסלול קצר משבע, והשחזור\nמחזיר את אחד משני המסלולים הקצרים.",
                 Indicate(seven, color=C.AMBER, scale_factor=1.05), run_time=1.0)
        self.fade_all()

        chips = cost_chips(("time", "$O(1)$"), ("memory", "$O(1)$"),
                           notes=("16 states, at most 4 edges each", "parent and queue: 16 at most"))
        self.say("הסיבוכיות : 16 מצבים, מכל אחד עד ארבע\nקשתות. זמן וזיכרון קבועים בפועל.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: a state without the farmer.
        three = VGroup(*[icon(n, 0.8) for n in ("cabbage", "goat", "wolf")]).arrange(RIGHT, buff=0.7)
        three.move_to(UP * 1.8)
        b3 = M("3 bits: 8 states", 34, C.RED).next_to(three, DOWN, buff=0.4)
        self.say("מלכודת : לתאר את המצב רק לפי שלושת\nהפריטים. יש אז שמונה מצבים.",
                 FadeIn(three, lag_ratio=0.2), FadeIn(b3))
        four = VGroup(*[icon(n, 0.8) for n in reversed(NAMES)]).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.6)
        b4 = M("4 bits: 16 states", 34, C.GREEN).next_to(four, DOWN, buff=0.4)
        self.say("אבל בלי הביט של האיכר לא יודעים\nמאיזה צד הוא יכול לקחת. הוא חלק מהמצב.",
                 FadeIn(four, lag_ratio=0.2), FadeIn(b4))
        self.fade_all()


class Closing(DVQScene):
    def construct(self):
        self.closing(QID, [("א", M("goat, back, wolf, goat, cabbage, back, goat", 28)),
                           ("ב", M("BFS on 4-bit states: 7 crossings", 28))],
                     ["לסיכום : שבע חציות, והצעד המפתיע\nהוא להחזיר את העז.",
                      "נסו לחצות בעצמכם בתיבה\nשבעמוד של שאלה 0032 באתר."],
                     holds=(3.2, 3.5))
