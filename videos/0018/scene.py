"""The tutorial video of question 0018, two hourglasses measuring D minutes from time 0
(script: script.md).

Render with `python videos/render.py 0018` (see notes/VIDEOS.md). Part א draws the two hourglasses
(7 and 11 minutes) in Manim with a clock and a time line: the sand flows, each flip turns the
glass over, and the page's plan (both at 0, A at 7, A again at 11) ends at 15; then the page's
box plays the plan event by event, the values of D that can be measured from 0, and the trap
of flipping only an empty glass. Part ב: decisions only at events, the state (t, a, b), four
options, the wait and the pruning, the children of (7, 0, 4); the page's `solve` typed in a
scrolling window and traced on 7, 11, 15 pop by pop (the first pop line by line, then from
pop to pop, a log of the popped states beside the code), the box's search panel, the cost,
and the trap of a search without `seen`.
"""

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, SAFE_BOTTOM, TX, BoxView, CodePanel, DVQScene, M, T,  # noqa: E402
                 VarPanel, baseline_text, cost_chips, page_python, trace)

QID = 18
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – דוגמה : A = 7, B = 11, D = 15"),
    ("ChapterB", "סעיף ב – האלגוריתם הכללי"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="hourglass", data-mode="zero", 7, 11, 15). "plan": the time line,
# the player and the scene, picture k after k events (a click on "next event" each).
# "search": the proof panel, picture k after k pops from the queue.
BOXES = {
    "plan": {"box": 0, "region": [".hg-axis", ".ex-play-row", ".hg-frame", ".hg-caption"],
             "hide": [".ex-play", ".ex-speed", ".hg-compare"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 4}]},
    "search": {"box": 0, "region": [".hg-proof > .ex-controls", ".hg-q-now", ".hg-q-kids", ".hg-q-tree"],
               "hide": [".ex-q-end", ".ex-q-start"],
               "steps": [[], {"do": [["click", ".ex-q-next"]], "repeat": 9}]},
}

A_CAP, B_CAP, D_GOAL = 7, 11, 15


def bfs(A: int, B: int, D: int, use_seen: bool = True):
    """The page's search, independently: (pops, children of each pop, plan)."""
    start = (0, 0, 0)
    queue, seen, pops, kids = deque([(start, {})]), {start}, [], []
    while queue:
        (t, a, b), plan = queue.popleft()
        pops.append((t, a, b))
        kids.append([])
        if t == D:
            return pops, kids, plan
        for fa in (False, True):
            for fb in (False, True):
                a2, b2 = (A - a if fa else a), (B - b if fb else b)
                run = [s for s in (a2, b2) if s > 0]
                if not run:
                    continue
                w = min(run)
                if t + w > D:
                    continue
                n = (t + w, max(a2 - w, 0), max(b2 - w, 0))
                if not use_seen or n not in seen:
                    seen.add(n)
                    kids[-1].append(n)
                    queue.append((n, {**plan, t: ("A" if fa else "") + ("B" if fb else "")}))
    return pops, kids, None


POPS, KIDS, PLAN = bfs(A_CAP, B_CAP, D_GOAL)
assert PLAN == {0: "AB", 7: "A", 11: "A"}, PLAN
assert POPS == [(0, 0, 0), (11, 0, 0), (7, 0, 0), (7, 0, 4), (14, 0, 0), (14, 0, 4),
                (11, 3, 0), (14, 0, 8), (15, 0, 0)], POPS
assert KIDS[:8] == [[(11, 0, 0), (7, 0, 0), (7, 0, 4)], [], [(14, 0, 0), (14, 0, 4)], [(11, 3, 0)],
                    [], [], [(14, 0, 8), (15, 0, 0), (15, 0, 7)], []], KIDS
MEASURABLE = [D for D in range(1, 40) if bfs(A_CAP, B_CAP, D)[2] is not None]
assert MEASURABLE[:5] == [7, 11, 14, 15, 17] and MEASURABLE[4:] == list(range(17, 40)), MEASURABLE
assert all(15 != 7 * i + 11 * j for i in range(3) for j in range(2))
# the trap: without `seen` the search still ends, but at D = 60 it pops 5,403 states, not 244
assert len(bfs(7, 11, 60)[0]) == 244 and len(bfs(7, 11, 60, use_seen=False)[0]) == 5403


# --- the hourglasses ------------------------------------------------------------------------

GW, GH = 1.5, 1.0            # a glass's width and the height of each chamber


def glass_body(cap: float, top: float, centre, colour: str) -> VGroup:
    """The frame and the sand: `top` minutes up (at the wide end, as just turned over), the
    rest down; the sand under the frame."""
    c = np.array(centre, dtype=float)
    frame = VGroup(
        Polygon(c + [-GW / 2, GH, 0], c + [GW / 2, GH, 0], c + [0, 0, 0],
                stroke_color=C.WHITE, stroke_width=4, fill_opacity=0),
        Polygon(c + [-GW / 2, -GH, 0], c + [GW / 2, -GH, 0], c + [0, 0, 0],
                stroke_color=C.WHITE, stroke_width=4, fill_opacity=0),
        Line(c + [-GW / 2 - 0.14, GH, 0], c + [GW / 2 + 0.14, GH, 0], stroke_width=8, color=C.WHITE),
        Line(c + [-GW / 2 - 0.14, -GH, 0], c + [GW / 2 + 0.14, -GH, 0], stroke_width=8, color=C.WHITE),
    )
    sand = VGroup()
    ft = max(0.0, min(1.0, top / cap))
    if ft > 1e-6:
        h = GH * ft
        w1 = GW / 2 * (GH - h) / GH
        sand.add(Polygon(c + [-GW / 2, GH, 0], c + [GW / 2, GH, 0], c + [w1, GH - h, 0],
                         c + [-w1, GH - h, 0], stroke_width=0, fill_color=colour, fill_opacity=1))
    fb = 1 - ft
    if fb > 1e-6:
        h = GH * fb
        w1 = GW / 2 * (GH - h) / GH
        sand.add(Polygon(c + [-GW / 2, -GH, 0], c + [GW / 2, -GH, 0], c + [w1, -GH + h, 0],
                         c + [-w1, -GH + h, 0], stroke_width=0, fill_color=colour, fill_opacity=1))
    return VGroup(sand, frame)


def glass_nums(cap: float, top: float, centre) -> VGroup:
    """The minutes up and down, beside the glass."""
    c = np.array(centre, dtype=float)
    up, down = int(round(top)), int(round(cap - top))
    return VGroup(M(str(up), 36, C.WHITE).move_to(c + [GW / 2 + 0.5, GH * 0.6, 0]),
                  M(str(down), 36, C.WHITE).move_to(c + [GW / 2 + 0.5, -GH * 0.6, 0]))


class Glass:
    """An hourglass on the screen: its sand up is a ValueTracker, redrawn every frame."""

    def __init__(self, cap: int, centre, colour: str, name: str):
        self.cap, self.c, self.colour = cap, np.array(centre, dtype=float), colour
        self.top = ValueTracker(0)
        self.body = always_redraw(lambda: glass_body(cap, self.top.get_value(), self.c, colour))
        self.nums = always_redraw(lambda: glass_nums(cap, self.top.get_value(), self.c))
        self.label = T(f"{name} = {cap}", 32, colour).move_to(self.c + DOWN * (GH + 0.45))

    def mobs(self):
        return [self.body, self.nums, self.label]

    def flip(self, scene: Scene, others: list | None = None, run_time: float = 0.8):
        """Turn the glass over (with `others` at the same time): the sand up and down swap."""
        flips = [self] + (others or [])
        stills = []
        for g in flips:
            top = g.top.get_value()
            body, nums = glass_body(g.cap, top, g.c, g.colour), glass_nums(g.cap, top, g.c)
            scene.remove(g.body, g.nums)
            scene.add(body, nums)
            stills.append((g, body, nums))
        scene.play(*[Rotate(b, PI, about_point=g.c) for g, b, _ in stills],
                   *[FadeOut(n) for _, _, n in stills], run_time=run_time)
        for g, body, _ in stills:
            g.top.set_value(g.cap - g.top.get_value())
            g.body.update()
            g.nums.update()
            scene.remove(body)
            scene.add(g.body)
        news = [glass_nums(g.cap, g.top.get_value(), g.c) for g in flips]
        scene.play(*[FadeIn(n) for n in news], run_time=0.3)
        for g, n in zip(flips, news):
            scene.remove(n)
            scene.add(g.nums)


class Clock:
    """The time line from 0 to D with a marker, and the clock text."""

    def __init__(self, d: int = D_GOAL):
        self.t = ValueTracker(0)
        self.line = NumberLine(x_range=[0, d, 1], length=11.0, color=C.MUTED, stroke_width=3,
                               include_tip=False, tick_size=0.06).move_to(DOWN * 1.75)
        self.ticks = VGroup(*[M(str(v), 28, C.MUTED).next_to(self.line.n2p(v), DOWN, buff=0.22)
                              for v in (0, 7, 11, 15)])
        self.marker = always_redraw(lambda: Triangle(fill_color=C.AMBER, fill_opacity=1, stroke_width=0)
                                    .scale(0.13).rotate(PI).next_to(self.line.n2p(self.t.get_value()), UP, buff=0.02))
        self.text = always_redraw(lambda: M(f"t = {int(round(self.t.get_value()))}", 48, C.AMBER)
                                  .move_to([3.9, 1.6, 0]))

    def mobs(self):
        return [self.line, self.ticks, self.marker, self.text]

    def tag(self, at: int, text: str, colour: str = C.WHITE) -> Text:
        return M(text, 28, colour).next_to(self.line.n2p(at), UP, buff=0.42)


class HourglassScene(DVQScene):
    """Helpers shared by the chapters of 0018."""

    def fade_all(self, run_time: float = 0.8):
        """Fade everything out, the redrawn glasses and clock frozen first (a redraw during
        the fade would change the family the fade interpolates)."""
        for m in self.mobjects:
            m.clear_updaters()
        super().fade_all(run_time)

    def run(self, clock: Clock, glasses: list, minutes: float, per_minute: float = 0.32):
        """Let the sand flow `minutes`: every glass with sand up loses it, the clock moves."""
        anims = [clock.t.animate.increment_value(minutes)]
        for g in glasses:
            top = g.top.get_value()
            if top > 0:
                anims.append(g.top.animate.set_value(max(top - minutes, 0)))
        self.play(*anims, run_time=minutes * per_minute, rate_func=linear)

    def swap_box(self, view: BoxView, name: str, start: int = 0, height: float | None = None) -> BoxView:
        new = BoxView(QID, name, start=start, height=height or view.height)
        new.move_to(view)
        self.play(FadeOut(view), FadeIn(new), run_time=0.8)
        return new


class Opening(HourglassScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "שני שעוני חול",
                     ["א · 7, 11 ו-15", "ב · האלגוריתם הכללי"],
                     ["שאלה 0018 : שני שעוני חול,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : דוגמה ביד,\nואז קוד שמוצא תוכנית לכל מטרה."])
        self.fade_all()
        a = Glass(A_CAP, [-2.2, 0.5, 0], C.BLUE, "A")
        b = Glass(B_CAP, [2.2, 0.5, 0], C.ORANGE, "B")
        self.say("שני שעוני חול : A מודד 7 דקות,\nו-B מודד 11. ברגע 0 כל החול למטה.",
                 *[FadeIn(m) for m in a.mobs() + b.mobs()], run_time=1.2)
        with self.beat("מותר להפוך שעון בכל רגע, גם באמצע :\nמה שלמטה עולה, וממשיך לרדת."):
            a.flip(self, [b])
        self.say("צריך שבדיוק ברגע D\nאיזשהו שעון חול ייגמר.")
        self.fade_all()


class ChapterA(HourglassScene):
    def construct(self):
        self.chapter_card("סעיף א", "דוגמה : 7, 11 ו-15",
                          "סעיף א : שעונים של 7 ו-11 דקות.\nצריך למדוד בדיוק 15 דקות מרגע 0.")

        a = Glass(A_CAP, [-4.4, 0.9, 0], C.BLUE, "A")
        b = Glass(B_CAP, [-0.9, 0.9, 0], C.ORANGE, "B")
        clock = Clock()
        goal = clock.tag(15, "D = 15", C.GREEN)
        self.say("שני השעונים, כל החול למטה,\nושעון שמראה כמה זמן עבר.",
                 *[FadeIn(m) for m in a.mobs() + b.mobs()], FadeIn(clock.text), run_time=1.2)
        self.say("אין שעון אחר : רק רגע שבו שעון חול\nנגמר אומר לנו כמה זמן עבר.",
                 *[FadeIn(m) for m in clock.mobs()[:3]], FadeIn(goal))
        idea = VGroup(TX(r"15 = 11 + 4", size=44, color=C.AMBER), TX(r"4 = 11 - 7", size=44, color=C.AMBER))
        idea.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.1, 0.2, 0])
        self.say("הרעיון : 15 = 11 + 4,\nואת ה-4 נקבל מההפרש 11 − 7.", FadeIn(idea))
        self.play(FadeOut(idea), run_time=0.5)

        tags = []
        with self.beat("רגע 0 : הופכים את שני השעונים,\nושניהם מתחילים לרוץ."):
            a.flip(self, [b])
            tags.append(clock.tag(0, "A+B", C.AMBER))
            self.play(FadeIn(tags[-1]), run_time=0.4)
        with self.beat("אחרי 7 דקות A נגמר.\nב-B נשארו 4 דקות למעלה."):
            self.run(clock, [a, b], 7)
        with self.beat("רגע 7 : הופכים את A מיד,\nוהוא מתחיל עוד 7 דקות."):
            a.flip(self)
            tags.append(clock.tag(7, "A", C.AMBER))
            self.play(FadeIn(tags[-1]), run_time=0.4)
        with self.beat("ברגע 11 B נגמר. ב-A ירדו בינתיים\n‏4 דקות, ונשארו 3 למעלה."):
            self.run(clock, [a, b], 4)
        ring = SurroundingRectangle(a.nums[1], color=C.AMBER, buff=0.12, corner_radius=0.1)
        self.say("‏4 הדקות שלמטה ב-A הן בדיוק\nההפרש 11 − 7 שחיפשנו.", Create(ring))
        self.play(FadeOut(ring), run_time=0.3)
        with self.beat("רגע 11 : הופכים את A באמצע הריצה,\nוה-4 שלמטה עולות למעלה."):
            a.flip(self)
            tags.append(clock.tag(11, "A", C.AMBER))
            self.play(FadeIn(tags[-1]), run_time=0.4)
        with self.beat("‏A נגמר ברגע 11 + 4 = 15 :\nמדדנו בדיוק 15 דקות."):
            self.run(clock, [a, b], 4)
            self.play(goal.animate.scale(1.15), Flash(clock.line.n2p(15), color=C.GREEN), run_time=0.6)
        self.say("התוכנית : שניהם ב-0, A ב-7,\nושוב A ב-11. ההיפוך באמצע הוא המפתח.")
        self.fade_all()

        # The page's box, the same plan event by event.
        view = BoxView(QID, "plan", height=5.6).move_to(UP * 0.6)
        self.say("כך זה נראה בתיבה שבעמוד :\nציר הזמן, השעון ושני השעונים.", FadeIn(view))
        self.box_beat(view, [
            (1, "אירוע 1, רגע 0 : הופכים את שניהם."),
            (2, "אירוע 2, רגע 7 : A נגמר,\nוהופכים אותו."),
            (3, "אירוע 3, רגע 11 : B נגמר. ב-A\n‏3 למעלה ו-4 למטה, והופכים."),
            (4, "אירוע 4, רגע 15 : A נגמר.\nמדדנו 15 דקות."),
        ])
        self.fade_all()

        # Which D can be measured from 0.
        ok = VGroup(*[M(str(v), 40, C.GREEN) for v in (7, 11, 14, 15)],
                    M("17, 18, 19, ...", 40, C.GREEN)).arrange(RIGHT, buff=0.55).move_to(UP * 1.2)
        no = M("1–6, 8–10, 12, 13, 16", 40, C.RED).move_to(DOWN * 0.3)
        self.say("לא כל D אפשרי מרגע 0. עם 7 ו-11\nאפשר רק 7, 11, 14, 15, ומ-17 כל מספר.",
                 FadeIn(ok, lag_ratio=0.15), run_time=1.4)
        self.say("גם לא 4 : ההפרש 11 − 7 הוא מדידה\nשמתחילה ברגע 7, לא ברגע 0.", FadeIn(no))
        self.fade_all()

        # The trap: flipping only an empty glass.
        sums = M("7i + 11j:  7, 11, 14, 18, 21, 22, ...", 40, C.MUTED).move_to(UP * 0.9)
        miss = M("15 ?", 48, C.RED).next_to(sums, DOWN, buff=0.6)
        self.say("מלכודת : להפוך רק שעון שנגמר.\nאז מודדים רק סכומים של ריצות שלמות.",
                 FadeIn(sums))
        self.say("‏15 אינו 7i + 11j לשום i ו-j,\nולכן בלי היפוך באמצע אין פתרון.", FadeIn(miss))
        self.fade_all()


class ChapterB(HourglassScene):
    def construct(self):
        self.chapter_card("סעיף ב", "האלגוריתם הכללי",
                          "סעיף ב : פונקציה שמקבלת A, B ו-D\nומחזירה תוכנית, או שאין פתרון.")

        # Events and the state.
        clock = Clock()
        dots = VGroup(*[Dot(clock.line.n2p(v), radius=0.11, color=C.AMBER) for v in (0, 7, 11, 15)])
        self.say("אין שעון אחר, ולכן מחליטים רק ברגע\nששעון חול נגמר. רגע כזה הוא אירוע.",
                 FadeIn(clock.line), FadeIn(clock.ticks), FadeIn(dots, lag_ratio=0.2), run_time=1.4)
        state = TX(r"(t,\ a,\ b)", size=64, color=C.AMBER).move_to(UP * 1.6)
        notes = VGroup(T("t: the time", 30, C.MUTED), T("a: sand on top of A", 30, C.MUTED),
                       T("b: sand on top of B", 30, C.MUTED)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        notes.next_to(state, DOWN, buff=0.4)
        self.say("המצב באירוע : הזמן t, והחול שלמעלה\nבכל שעון, a ו-b.", FadeIn(state), FadeIn(notes))
        self.fade_all()

        opts = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=0.9, corner_radius=0.14, stroke_color=C.MUTED,
                                                stroke_width=3, fill_color=C.NAVY_LIGHT, fill_opacity=1),
                               M(s, 36)) for s in ("wait", "A", "B", "AB")]).arrange(RIGHT, buff=0.35)
        for o in opts:
            o[1].move_to(o[0])
        opts.move_to(UP * 2.0)
        self.say("מכל מצב ארבע אפשרויות : לא להפוך,\nלהפוך את A, את B, או את שניהם.",
                 FadeIn(opts, lag_ratio=0.2), run_time=1.2)
        f1 = TX(r"a' = A - a \ \text{(flipped)},\qquad w = \min\{\,a',\ b' > 0\,\}", size=40).move_to(UP * 0.5)
        f2 = TX(r"(t + w,\ \max(a' - w, 0),\ \max(b' - w, 0))", size=40, color=C.AMBER).move_to(DOWN * 0.5)
        self.say("היפוך משאיר A − a למעלה. מחכים\nלשעון הראשון שנגמר : הקטן מביניהם.", FadeIn(f1))
        self.say("ומגיעים למצב הבא, באירוע הבא.", FadeIn(f2))
        cut = T("nothing flows  ✗      t + w > D  ✗", 32, C.RED).move_to(DOWN * 1.6)
        self.say("פוסלים אפשרות שבה שום שעון לא רץ,\nואפשרות שעוברת את D.", FadeIn(cut))
        self.fade_all()

        # The children of (7, 0, 4).
        def node(s, colour=C.WHITE):
            box = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.14, stroke_color=colour,
                                   stroke_width=3, fill_color=C.NAVY_LIGHT, fill_opacity=1)
            return VGroup(box, M(str(s).replace(" ", ""), 32, colour).move_to(box))

        parent = node((7, 0, 4), C.AMBER).move_to(UP * 2.2)
        kids = [((11, 0, 0), "wait", False), ((14, 0, 0), "B", False),
                ((11, 3, 0), "A", True), ((14, 0, 0), "AB", False)]
        found = {(0, 0, 0), *[k for ks in KIDS[:3] for k in ks]}        # seen before pop 4
        assert [k in found for k, _, _ in kids] == [True, True, False, True]
        row = VGroup(*[node(k, C.GREEN if new else C.MUTED) for k, _, new in kids]).arrange(RIGHT, buff=0.45)
        row.move_to(DOWN * 0.3)
        edges, labels, marks = VGroup(), VGroup(), VGroup()
        for n, (k, act, new) in zip(row, kids):
            e = Line(parent.get_bottom(), n.get_top(), stroke_color=C.MUTED, stroke_width=3)
            edges.add(e)
            labels.add(M(act, 28, C.AMBER).next_to(e.point_from_proportion(0.62), LEFT, buff=0.12))
            marks.add(T("new" if new else "seen", 28, C.GREEN if new else C.MUTED).next_to(n, DOWN, buff=0.2))
        self.add(edges)                       # the lines under the boxes
        self.say("למשל מ-(7, 0, 4) יוצאים ארבעה מצבים.\nשלושה כבר נמצאו קודם.",
                 FadeIn(parent), Create(edges), FadeIn(row, lag_ratio=0.15), FadeIn(labels), run_time=1.4)
        self.say("רק (11, 3, 0) חדש, והוא זה\nשמוביל לפתרון.", FadeIn(marks))
        self.say("‏BFS עובר על המצבים לפי הסדר,\nומצב שכבר נראה לא נכנס שוב לתור.")
        self.fade_all()

        # The code: typed.
        code = page_python(QID, "def solve")
        keep = [n for n in range(1, len(code.splitlines()) + 1) if n != 5]     # the docstring
        panel = CodePanel(code, font_size=30, drop_comments=True, drop_trailing_comments=True,
                          only=keep, rows=13)
        self.place_code(panel)
        self.type_code(panel, [
            (1, "‏deque הוא תור : מוסיפים בסוף,\nושולפים מההתחלה."),
            (4, "‏solve מקבלת את שני השעונים\nואת המטרה D."),
            ([7, 8, 9], "ההתחלה (0, 0, 0) בתור, עם תוכנית ריקה,\nוהיא גם בקבוצה seen."),
            ([11, 12], "כל עוד התור לא ריק, שולפים מצב\nואת התוכנית שהביאה אליו."),
            ([13, 14], "אם הזמן שלו בדיוק D,\nהתוכנית שלו היא התשובה."),
            ([16, 17], "שתי לולאות : להפוך את A או לא,\nולהפוך את B או לא."),
            ([18, 19], "היפוך משאיר A − a למעלה.\nבלי היפוך הכמות נשארת."),
            ([20, 21, 22], "השעונים שעוד רצים. אם אין כאלה,\nשום דבר לא יקרה : continue."),
            (23, "מחכים לשעון הראשון שנגמר :\nהקטנה בין הכמויות החיוביות."),
            ([24, 25], "אם זה עובר את D, פוסלים."),
            (27, "המצב הבא : הזמן גדל ב-wait,\nוהחול שלמעלה ירד ב-wait."),
            ([28, 29], "מצב שכבר נראה לא נכנס שוב.\nחדש נכנס ל-seen."),
            ([30, 31], "הפעולה : מה הפכנו ברגע t.\nהמצב נכנס לתור עם התוכנית המורחבת."),
            (32, "אם התור התרוקן, אין פתרון :\nמחזירים None."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        # The run on 7, 11, 15: pop by pop, a log of the popped states beside the code.
        steps, result = trace(code, "solve", (A_CAP, B_CAP, D_GOAL))
        assert result == PLAN, result
        lines = [s.line for s in steps]
        starts = [k for k, n in enumerate(lines) if n == 11]
        assert len(starts) == 9 and lines[-1] == 14, (len(starts), lines[-1])
        prologue = list(range(starts[0]))
        segs = [list(range(starts[i], starts[i + 1] if i + 1 < len(starts) else len(steps)))
                for i in range(len(starts))]
        for i, seg in enumerate(segs):
            s = steps[seg[1]].state                                   # after line 12
            assert (s["t"], s["a"], s["b"]) == POPS[i], (i, s)
        kid_at = [i for i in segs[0] if lines[i] == 18]               # the four options of pop 1
        assert len(kid_at) == 4
        head0 = [i for i in segs[0] if i < kid_at[0]]
        cuts = []                       # an option starts with the loop heads just before it
        for j in range(1, 4):
            c = kid_at[j]
            while lines[c - 1] in (16, 17):
                c -= 1
            cuts.append(c)
        bounds = [kid_at[0], *cuts, segs[0][-1] + 1]
        child = [list(range(bounds[j], bounds[j + 1])) for j in range(4)]

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            if n == "plan":
                return " ".join(f"{k}:{a}" for k, a in v.items()) or "{}"
            return str(v)

        vp = VarPanel(["t", "a", "b", "plan"], fmt=fmt, size=28, cols=3, slot=2.1).set_state({})
        target = panel.copy()
        target.scale(19.4 / panel.em_px())
        margin, top = 0.25, 3.55
        target.move_to([-config.frame_width / 2 + margin + target.width / 2, top - target.height / 2, 0])
        vp.next_to(target, DOWN, buff=0.35).align_to(target, LEFT).shift(RIGHT * 0.3)
        right_x = target.get_right()[0] + 0.45
        room = config.frame_width / 2 - 0.2 - right_x
        log_title = T("popped", 28, C.MUTED)
        log_title.move_to([right_x + log_title.width / 2, top - 0.25, 0])
        log = VGroup()
        log_top = log_title.get_bottom()[1] - 0.15
        row_h = 0.46

        def add_rows(ks):
            """The pops `ks` into the log, the newest amber."""
            anims = []
            for kk in ks:
                t, a, b = POPS[kk]
                row = baseline_text(f"({t}, {a}, {b})", 28, C.WHITE)
                if row.width > room:
                    row.scale(room / row.width)
                log.add(row)
            for idx, row in enumerate(log):
                at = np.array([right_x + row.width / 2, log_top - row_h * (idx + 0.5), 0])
                colour = C.GREEN if POPS[idx][0] == D_GOAL else (C.AMBER if idx >= len(log) - len(ks) else C.WHITE)
                if row in self.mobjects:
                    anims.append(row.animate.move_to(at).set_color(colour))
                else:
                    row.move_to(at).set_color(colour)
                    anims.append(FadeIn(row))
            self.play(*anims, run_time=0.5)

        with self.beat("נריץ על 7, 11, 15. מתחת לקוד המשתנים,\nומימין כל מצב שנשלף מהתור."):
            self.play(Transform(panel, target), run_time=1.2)
            vp.set_state({})
            self.play(FadeIn(vp), FadeIn(log_title), run_time=0.6)
        if panel.em_px() < 19.0:
            self.problems.append(f"code beside the log {panel.em_px():.1f} px high at 720p")
        if vp.get_bottom()[1] < SAFE_BOTTOM + 0.05:
            self.problems.append(f"variables at {vp.get_bottom()[1]:.2f}, under the captions' line")

        plan = [
            (prologue, "full", "‏(0, 0, 0) בתור ובקבוצה seen,\nעם תוכנית ריקה.", None),
            (head0, "full", "שולפים את (0, 0, 0). הזמן 0, לא 15,\nועוברים על ארבע האפשרויות.", [0]),
            (child[0], "full", "לא להפוך : אין חול למעלה, שום שעון\nלא רץ, ולכן continue.", None),
            (child[1], "jump", "להפוך את B : מחכים 11 דקות.\n‏(11, 0, 0) חדש, ונכנס לתור.", None),
            (child[2] + child[3], "jump", "‏A לבד נותן (7, 0, 0), ושניהם\n‏(7, 0, 4). שלושה מצבים בתור.", None),
            (segs[1], "jump", "שולפים את (11, 0, 0). כל אפשרות\nעוברת את 15, ולא נכנס כלום.", [1]),
            (segs[2], "jump", "‏(7, 0, 0) מוסיף את (14, 0, 0)\nואת (14, 0, 4).", [2]),
            (segs[3], "jump", "‏(7, 0, 4) : רק להפוך את A\nנותן מצב חדש, (11, 3, 0).", [3]),
            (segs[4] + segs[5], "jump", "‏(14, 0, 0) ו-(14, 0, 4) :\nכל המשך עובר את 15.", [4, 5]),
            (segs[6], "jump", "‏(11, 3, 0) מכניס את (14, 0, 8),\n‏(15, 0, 0) ו-(15, 0, 7).", [6]),
            (segs[7], "jump", "‏(14, 0, 8) לא מוסיף כלום.", [7]),
            (segs[8], "full", "שולפים את (15, 0, 0) : t = D,\nומחזירים את התוכנית שלו.", [8]),
        ]
        planned = [i for g in plan for i in g[0]]
        if planned != list(range(len(steps))):
            raise RuntimeError("the plan does not cover the trace in order")
        cursor = None
        for idx, mode, caption, rows in plan:
            with self.beat(caption):
                if mode == "full":
                    todo = idx
                else:      # the last line that says what the pop did: a push, an overshoot
                    key = [i for i in idx if lines[i] in (31, 25, 22, 14)]
                    todo = key[-1:] or idx[-1:]
                rows_at = [panel.index[steps[i].line] for i in todo]
                if not all(panel.visible(steps[i].line) for i in todo):
                    lo, hi = min(rows_at), max(rows_at)
                    first = lo if lo < panel.scroll else hi - panel.rows + 1
                    anims = panel.scroll_to(first)
                    if cursor is not None:
                        anims.append(FadeOut(cursor))
                        cursor = None
                    self.play(*anims, run_time=0.7)
                per = min(0.5, 2.4 / len(todo))
                for i in todo:
                    bar = panel.bar(steps[i].line)
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar),
                              *vp.show(steps[i].state), run_time=per)
                    cursor = cursor or bar
                if rows:
                    add_rows(rows)
        self.say("התוכנית שחזרה : שניהם ב-0, A ב-7,\nושוב A ב-11. התוכנית של סעיף א.")
        self.fade_all()

        # The box's search panel, pop by pop.
        view = BoxView(QID, "search", height=5.7).move_to(UP * 0.55)
        self.say("בתיבה שבעמוד, אותו חיפוש שליפה\nאחרי שליפה : הילדים, התור והעץ.", FadeIn(view))
        with self.beat("השליפה הראשונה : שלושה מצבים\nחדשים בתור, והעץ מתחיל לגדול."):
            self.box_step(view, 1)
        with self.beat("השליפה הרביעית, (7, 0, 4) :\nרק (11, 3, 0) חדש."):
            for k in (2, 3, 4):
                self.box_step(view, k, run_time=0.35)
        with self.beat("השליפה השביעית, (11, 3, 0),\nמכניסה את (15, 0, 0) לתור."):
            for k in (5, 6, 7):
                self.box_step(view, k, run_time=0.35)
        with self.beat("בשליפה התשיעית יוצא (15, 0, 0),\nוהדרך אליו מסומנת בעץ."):
            for k in (8, 9):
                self.box_step(view, k, run_time=0.35)
        self.fade_all()

        # The cost.
        chips = cost_chips(("time", "$O\\big((D+1)(A+B+1)\\big)$"), ("memory", "$O\\big((D+1)(A+B+1)\\big)$"),
                           notes=("a = 0 or b = 0 at an event", "seen and the queue"))
        chips.arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        self.say("בכל אירוע לפחות שעון אחד ריק, ולכן\nיש לכל היותר (D+1)(A+B+1) מצבים.",
                 FadeIn(chips, lag_ratio=0.3))
        self.say("כל מצב נכנס לתור פעם אחת, עם ארבע\nבדיקות. בדוגמה נשלפו רק 9 מצבים.")
        self.fade_all()

        # The trap: no `seen`.
        with_seen = M("seen:     244 pops", 40, C.GREEN)
        without = M("no seen:  5403 pops", 40, C.RED)
        both = VGroup(T("A = 7, B = 11, D = 60", 34, C.MUTED), with_seen, without).arrange(DOWN, buff=0.45)
        both.move_to(UP * 0.8)
        self.say("מלכודת : לוותר על seen. החיפוש\nעדיין נגמר, כי הזמן גדל בכל צעד.",
                 FadeIn(both[0]), FadeIn(without))
        self.say("אבל ב-D = 60 נשלפים 5,403 מצבים,\nבמקום 244 עם seen.", FadeIn(with_seen))
        self.fade_all()


class Closing(HourglassScene):
    def construct(self):
        self.closing(QID, [("א", M("0: A+B    7: A    11: A    → 15", 30)),
                           ("ב", M("BFS over (t, a, b), four options an event", 30))],
                     ["לסיכום : היפוך באמצע הריצה נותן 4 דקות,\nו-BFS על (t, a, b) מוצא תוכנית לכל D.",
                      "נסו שעונים ומטרות משלכם בתיבה\nשבעמוד של שאלה 0018 באתר."],
                     holds=(4.0, 4.0))
