"""The tutorial video of question 0057, ants on a rod (script: script.md).

Render with `python videos/render.py 0057` (see VIDEOS.md). The owner's choice
(2026-11-01): parts א, ב and ג in full, part ד briefly. The ants are drawn in Manim on a
rod of 100 cm, with the space-time chart under it (place across, time down): two ants that
meet and turn look exactly like two ghosts that walk through each other, only the colours
swap. Part א: every ghost leaves after p or 100 - p seconds, `last_fall` typed and run on
the page's six ants (90 s), the page's box drawing the ants' lines and then the ghosts'.
Part ב: a collision is a crossing of two ghost lines, the pairs going toward each other
(5 in the example), at most 50 · 50 = 2500, `collisions` typed and traced ant by ant. Part
ג: the order along the rod never changes, so the leftmost ants fall left, `fall_times`
typed and traced, the page's box stepping to each fall; the ant at 60 faces left and falls
right, last, at 90 s. Part ד, briefly: on a ring the ghosts are home after 100 s and the
labels turn by s = R - L, home after n / gcd(n, s) laps (300 s); no code.
"""

import sys
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, read_palette, trace)

QID = 57
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – מתי הנמלה האחרונה נופלת"),
    ("ChapterB", "סעיף ב – כמה התנגשויות"),
    ("ChapterC", "סעיף ג – מתי נופלת נמלה מסוימת"),
    ("ChapterD", "סעיף ד – מסלול מעגלי"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="ants", the six ants 10R 25L 40R 60L 75L 90R). "pole": the rod,
# the summary and the chips of when each ant falls, at 0, 10, 25, 60 and 75 s,
# half a second a click (75 s, not the end: the answer line that appears at the end would
# move the picture). "chart": the space-time chart at 0 and 25 s, at 89.5 s (the same
# reason), then with the ghosts switched on (the controls are out of the picture).
BOXES = {
    "pole": {"box": 0, "region": [".ex-play-row", ".an-sum", ".an-pole-wrap", ".an-falls"],
             "hide": [".an-hint", ".an-st-wrap", ".viz-legend", ".ex-keys"],
             "steps": [[], [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
               [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
               [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
               [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]]]},
    "chart": {"box": 0, "region": [".an-st-wrap"], "hide": [".an-hint", ".viz-legend", ".an-falls", ".ex-keys"],
              "steps": [[], [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
                [["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"]],
                [["check", ".an-ghost", True]]]},
}

POS = [10, 25, 40, 60, 75, 90]
DIRS = [1, -1, 1, -1, -1, 1]
LEN = 100


# --- the reference, independent of the page code ----------------------------------------

def ghost(p: int, d: int, t: float):
    """Ghost of an ant from p, direction d, at time t: its place, or None once off."""
    off = p if d < 0 else LEN - p
    return None if t >= off else p + d * t


def ants_at(pos, dirs, t):
    """Each ant (in order along the rod) at time t: (x or None, direction, ghost index).
    The leftmost ants fall left, one for each ghost off on the left; at a meeting the
    ghost going left belongs to the left ant."""
    n = len(pos)
    gs = [(ghost(p, d, t), d, i) for i, (p, d) in enumerate(zip(pos, dirs))]
    fl = sum(1 for x, d, _ in gs if x is None and d < 0)
    fr = sum(1 for x, d, _ in gs if x is None and d > 0)
    on = sorted((g for g in gs if g[0] is not None), key=lambda g: (g[0], g[1]))
    out = []
    for k in range(n):
        if k < fl or k >= n - fr:
            out.append((None, 0, None))
        else:
            out.append(on[k - fl])
    return out


def fall_ref(pos, dirs):
    left = sorted(p for p, d in zip(pos, dirs) if d < 0)
    right = sorted(LEN - p for p, d in zip(pos, dirs) if d > 0)
    return [(t, "L") for t in left] + [(t, "R") for t in right[::-1]]


def collisions_ref(pos, dirs):
    return sum(1 for a, da in zip(pos, dirs) for b, db in zip(pos, dirs) if da > 0 and db < 0 and a < b)


def meetings(pos, dirs):
    """(time, place) of every crossing of two ghost lines."""
    out = []
    for a, da in zip(pos, dirs):
        for b, db in zip(pos, dirs):
            if da > 0 and db < 0 and a < b:
                out.append(((b - a) / 2, (a + b) / 2))
    return sorted(out)


FALL = fall_ref(POS, DIRS)
assert FALL == [(25, "L"), (60, "L"), (75, "L"), (90, "R"), (60, "R"), (10, "R")]
assert max(t for t, _ in FALL) == 90
assert collisions_ref(POS, DIRS) == 5 and len(meetings(POS, DIRS)) == 5
assert [m[0] for m in meetings(POS, DIRS)] == [7.5, 10.0, 17.5, 25.0, 32.5]
# a brute-force check of the ghost picture: step the ants a quarter second at a time
def _simulate(pos, dirs):
    xs, ds, alive, fall = [4 * p for p in pos], list(dirs), [True] * len(pos), [None] * len(pos)
    t = 0
    while any(alive):
        t += 1
        for i in range(len(xs)):
            if alive[i]:
                xs[i] += ds[i]
        for i in range(len(xs)):
            if alive[i] and (xs[i] <= 0 or xs[i] >= 4 * LEN):
                alive[i] = False
                fall[i] = (t / 4, "L" if xs[i] <= 0 else "R")
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                if alive[i] and alive[j] and xs[i] == xs[j]:
                    ds[i], ds[j] = -ds[i], -ds[j]
    return fall
assert _simulate(POS, DIRS) == FALL
assert 50 * 50 == 2500 and max(k * (100 - k) for k in range(101)) == 2500
RING = [1, 1, 1, -1, -1, 1]
S = (RING.count(1) - RING.count(-1)) % 6
assert S == 2 and 6 // gcd(6, S) == 3

_S = read_palette()["slate"]
COLS = [_S["--viz-s1"], _S["--viz-s2"], _S["--viz-s3"], _S["--viz-s4"], _S["--viz-s5"], C.WHITE]


# --- the drawings ---------------------------------------------------------------------------

class Rod:
    """A rod of 100 cm from x0 to x0 + w at height y, with its ticks."""

    def __init__(self, y: float = 2.4, x0: float = -5.5, w: float = 11.0):
        self.y, self.x0, self.w = y, x0, w

    def X(self, p: float) -> float:
        return self.x0 + p * self.w / LEN

    def mob(self, ticks: bool = True) -> VGroup:
        line = Line([self.X(0), self.y, 0], [self.X(LEN), self.y, 0], color=C.WHITE, stroke_width=6)
        g = VGroup(line)
        if ticks:
            for v in (0, 25, 50, 75, 100):
                g.add(M(str(v), 28, C.MUTED).move_to([self.X(v), self.y - 0.38, 0]))
        return g


def ant(label: str, color: str, d: int, at, r: float = 0.27) -> VGroup:
    """An ant (or a ghost): a disc with its number, a small triangle on the side it walks."""
    disc = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(at)
    num = M(label, 28, C.NAVY, weight="BOLD").move_to(disc)
    g = VGroup(disc, num)
    if d:
        tip = np.array(at) + RIGHT * d * (r + 0.2)
        tri = Polygon(tip, tip - RIGHT * d * 0.17 + UP * 0.11, tip - RIGHT * d * 0.17 + DOWN * 0.11,
                      stroke_width=0, fill_color=color, fill_opacity=1)
        g.add(tri)
    return g


def ants_on(rod: Rod, tt: ValueTracker, pos, dirs, ghosts: bool = False, labels=None):
    """The ants (or the ghosts) on the rod at the tracker's time, redrawn every frame. An
    ant keeps its colour; with `ghosts` the colour follows the ghost."""
    def draw():
        t = tt.get_value()
        g = VGroup()
        y = rod.y + 0.42
        if ghosts:
            for i, (p, d) in enumerate(zip(pos, dirs)):
                x = ghost(p, d, t)
                if x is not None:
                    g.add(ant(str(i + 1) if labels is None else labels[i], COLS[i % 6], d, [rod.X(x), y, 0]))
        else:
            for k, (x, d, _) in enumerate(ants_at(pos, dirs, t)):
                if x is not None:
                    g.add(ant(str(k + 1) if labels is None else labels[k], COLS[k % 6], d, [rod.X(x), y, 0]))
        return g
    return always_redraw(draw)


class Chart:
    """The space-time chart under a rod: place across (the rod's x), time down."""

    def __init__(self, rod: Rod, top: float = 1.75, sy: float = 0.04, tmax: float = 100):
        self.rod, self.top, self.sy, self.tmax = rod, top, sy, tmax

    def Y(self, t: float) -> float:
        return self.top - t * self.sy

    def axes(self) -> VGroup:
        r = self.rod
        g = VGroup()
        for v in (25, 50, 75, 100):
            if v > self.tmax:
                continue
            g.add(DashedLine([r.X(0), self.Y(v), 0], [r.X(LEN), self.Y(v), 0], color=C.FAINT,
                             stroke_width=1.5, dash_length=0.08))
            g.add(M(str(v), 28, C.MUTED).move_to([r.X(0) - 0.45, self.Y(v), 0]))
        g.add(Line([r.X(0), self.top, 0], [r.X(LEN), self.top, 0], color=C.FAINT, stroke_width=2))
        g.add(M("t", 30, C.MUTED).move_to([r.X(0) - 0.45, self.top, 0]))
        return g

    def lines(self, tt: ValueTracker, pos, dirs, ghosts: bool = False):
        """Every ant's broken line (or every ghost's straight one) up to the tracker's time."""
        r = self.rod
        falls = fall_ref(pos, dirs)

        def draw():
            t = tt.get_value()
            g = VGroup()
            if ghosts:
                for i, (p, d) in enumerate(zip(pos, dirs)):
                    stop = min(t, p if d < 0 else LEN - p)
                    if stop > 0:
                        g.add(Line([r.X(p), self.Y(0), 0], [r.X(p + d * stop), self.Y(stop), 0],
                                   color=COLS[i % 6], stroke_width=4))
                return g
            for k in range(len(pos)):
                end = min(t, falls[k][0])
                pts, s = [], 0.0
                while s < end:
                    x = ants_at(pos, dirs, s)[k][0]
                    pts.append([r.X(x), self.Y(s), 0])
                    s += 0.5
                if t >= falls[k][0]:
                    pts.append([r.X(0 if falls[k][1] == "L" else LEN), self.Y(falls[k][0]), 0])
                elif end > 0:
                    pts.append([r.X(ants_at(pos, dirs, end)[k][0]), self.Y(end), 0])
                if len(pts) > 1:
                    g.add(VMobject(stroke_color=COLS[k % 6], stroke_width=4).set_points_as_corners(pts))
            return g
        return always_redraw(draw)


def clock(tt: ValueTracker, where) -> Mobject:
    return always_redraw(lambda: M(f"t = {tt.get_value():g} s", 32, C.AMBER).move_to(where))


class AntScene(DVQScene):
    """Helpers shared by the chapters of 0057."""

    def run_to(self, tt: ValueTracker, to: float, speed: float = 18.0):
        """Advance the time to `to` at `speed` seconds of the ants per second of video."""
        dt = abs(to - tt.get_value())
        if dt:
            self.play(tt.animate.set_value(to), run_time=max(0.4, dt / speed), rate_func=linear)

    def box(self, name: str, **kw) -> BoxView:
        """The page's box, the clicks of a step marked once (a step of many clicks on the
        same button rings it once)."""
        view = BoxView(QID, name, **kw)
        for shot in view.data["shots"]:
            seen, keep = set(), []
            for c in shot["clicks"]:
                if tuple(c) not in seen:
                    seen.add(tuple(c))
                    keep.append(c)
            shot["clicks"] = keep
        return view

    def run_with(self, panel: CodePanel, vp, steps: list, groups: list, cursor=None):
        """Light the traced lines in the order they ran, the variables beside them, and after
        each group's lines play its own picture (a callable, or None)."""
        planned = [n for g in groups for n in g[0]]
        ran = [s.line for s in steps]
        if planned != ran:
            raise RuntimeError(f"the code ran lines {ran}, the script lights {planned}")
        k = 0
        for lines, caption, then in groups:
            with self.beat(caption):
                per = min(0.8, 2.0 / len(lines))
                for _ in lines:
                    step = steps[k]
                    k += 1
                    bar = panel.bar(step.line)
                    anims = vp.show(step.state) if vp is not None else []
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar), *anims, run_time=per)
                    cursor = cursor or bar
                if then is not None:
                    then()
        return cursor


def strip(pos, dirs, size: float = 32) -> VGroup:
    """The ants as text, "10→ 25← ...", one chip each, in their order along the rod."""
    return VGroup(*[M(f"{p}{'→' if d > 0 else '←'}", size, COLS[k % 6]) for k, (p, d) in enumerate(zip(pos, dirs))]
                  ).arrange(RIGHT, buff=0.55)


# --- the scenes -----------------------------------------------------------------------------

class Opening(AntScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "נמלים על מוט",
                     ["א · הנמלה האחרונה", "ב · התנגשויות", "ג · נמלה מסוימת", "ד · מסלול מעגלי"],
                     ["שאלה 0057 : נמלים על מוט,\nשאלה ברמת ג'וניור.",
                      "ארבעה סעיפים : מתי הכול נגמר, כמה התנגשויות,\nמתי נופלת נמלה מסוימת, ומעגל."])
        self.fade_all()
        rod = Rod(y=0.6)
        tt = ValueTracker(0)
        ants = ants_on(rod, tt, POS, DIRS)
        self.say("על מוט באורך 100 ס\"מ עומדות נמלים,\nכל אחת בנקודה אחרת.",
                 Create(rod.mob()), FadeIn(ants), run_time=1.4)
        self.say("כל נמלה פונה ימינה או שמאלה,\nוהולכת סנטימטר אחד בשנייה.")
        clk = clock(tt, [-5.0, 2.4, 0])
        with self.beat("כששתי נמלים נפגשות, שתיהן מסתובבות\nמיד. נמלה שמגיעה לקצה נופלת."):
            self.play(FadeIn(clk), run_time=0.4)
            self.run_to(tt, 12, speed=6)
        with self.beat("זו הדוגמה מהעמוד : שש נמלים,\nבמקומות 10, 25, 40, 60, 75 ו-90."):
            self.run_to(tt, 0, speed=30)
        self.fade_all()


class ChapterA(AntScene):
    def construct(self):
        self.chapter_card("סעיף א", "מתי הנמלה האחרונה נופלת",
                          "סעיף א : על המוט 100 נמלים, בכל סידור.\nמה הזמן הארוך ביותר עד שכולן נופלות?")

        # The idea: two ants that turn look like two ghosts that pass.
        top, bot = Rod(y=1.7, x0=-4.5, w=9.0), Rod(y=-1.1, x0=-4.5, w=9.0)
        tt = ValueTracker(0)
        two_p, two_d = [30, 70], [1, -1]
        a_row = ants_on(top, tt, two_p, two_d, labels=["A", "B"])
        g_row = ants_on(bot, tt, two_p, two_d, ghosts=True, labels=["A", "B"])
        lab_a = M("ants: turn", 30, C.MUTED).move_to([-4.5, 2.75, 0], aligned_edge=LEFT)
        lab_g = M("ghosts: pass through", 30, C.MUTED).move_to([-4.5, -0.05, 0], aligned_edge=LEFT)
        self.say("שתי נמלים, A ו-B, הולכות זו לקראת זו.\nלמעלה הן מסתובבות במפגש, כמו בשאלה.",
                 Create(top.mob()), FadeIn(a_row), FadeIn(lab_a), run_time=1.2)
        self.say("למטה אותן שתיים, אבל כאן הן עוברות\nזו דרך זו, כמו רוחות.",
                 Create(bot.mob()), FadeIn(g_row), FadeIn(lab_g), run_time=1.2)
        with self.beat("מריצים את שתיהן יחד.\nהן נפגשות באמצע, ב-50."):
            self.run_to(tt, 20, speed=10)
        with self.beat("אחרי המפגש : למעלה A חוזרת שמאלה,\nלמטה A ממשיכה ימינה."):
            self.run_to(tt, 32, speed=8)
        self.say("אבל המקומות זהים לגמרי : נקודה אחת שמאלה\nונקודה אחת ימינה. רק הצבעים התחלפו.")
        self.say("מי שלא רואה שמות לא יכול להבדיל.\nזה כל הטריק : לחשוב על רוחות.")
        self.fade_all()

        # The six ants, then their ghosts: the same lines.
        rod = Rod(y=2.55)
        ch = Chart(rod, top=1.85, sy=0.042)
        tt = ValueTracker(0)
        ants = ants_on(rod, tt, POS, DIRS)
        lines = ch.lines(tt, POS, DIRS)
        clk = clock(tt, [5.3, 3.55, 0])
        self.say("עכשיו שש הנמלים מהעמוד. מתחת למוט,\nכל נמלה מציירת קו : מקום מול זמן.",
                 Create(rod.mob()), FadeIn(ch.axes()), FadeIn(ants), FadeIn(clk), run_time=1.4)
        self.add(lines)
        with self.beat("הזמן יורד למטה. בכל מפגש\nהקווים של הנמלים נשברים."):
            self.run_to(tt, 40, speed=12)
        with self.beat("ממשיכים עד שהמוט מתרוקן :\nהאחרונה נופלת אחרי 90 שניות."):
            self.run_to(tt, 90, speed=14)
        self.wait(0.3)
        tg = ValueTracker(0)
        gants = ants_on(rod, tg, POS, DIRS, ghosts=True)
        glines = ch.lines(tg, POS, DIRS, ghosts=True)
        clk2 = clock(tg, [5.3, 3.55, 0])
        self.say("ועכשיו אותה ריצה עם רוחות,\nשהולכות ישר ולא מסתובבות.",
                 FadeOut(lines), FadeOut(ants), FadeOut(clk), FadeIn(gants), FadeIn(clk2), run_time=0.8)
        self.add(glines)
        with self.beat("כל רוח היא קו ישר. אלה בדיוק\nאותם קווים, רק בצבעים אחרים."):
            self.run_to(tg, 90, speed=24)
        self.fade_all()

        # Each ghost leaves after p or 100 - p.
        f1 = TX(r"\text{left: } p", r"\qquad", r"\text{right: } 100 - p", size=44).move_to(UP * 2.0)
        self.say("רוח שהולכת שמאלה מ-p יוצאת אחרי p שניות,\nורוח שהולכת ימינה אחרי 100 פחות p.", FadeIn(f1))
        times = [p if d < 0 else LEN - p for p, d in zip(POS, DIRS)]
        row = VGroup(*[M(str(t), 40, COLS[k]) for k, t in enumerate(times)]).arrange(RIGHT, buff=0.75)
        heads = VGroup(*[M(f"{p}{'→' if d > 0 else '←'}", 30, C.MUTED).next_to(n, UP, buff=0.3)
                         for n, (p, d) in zip(row, zip(POS, DIRS))])
        VGroup(heads, row).move_to(UP * 0.15)
        self.say("בדוגמה : הזמנים של שש הרוחות\nהם 90, 25, 60, 60, 75 ו-10.",
                 FadeIn(heads), LaggedStart(*[FadeIn(n, shift=0.15 * DOWN) for n in row], lag_ratio=0.15))
        mx = TX(r"\max = 90", size=46, color=C.AMBER).next_to(row, DOWN, buff=0.6)
        ring = SurroundingRectangle(row[0], color=C.AMBER, buff=0.12, corner_radius=0.1, stroke_width=4)
        self.say("המוט מתרוקן כשהרוח האחרונה יוצאת :\nהמקסימום, 90 שניות.", Create(ring), FadeIn(mx))
        worst = TX(r"p = 0,\ \rightarrow \quad\Rightarrow\quad 100", size=44, color=C.GREEN)
        worst.next_to(mx, DOWN, buff=0.5)
        self.say("כל זמן הוא לכל היותר 100, ו-100 מתקבל\nכשנמלה עומדת בקצה ופונה פנימה.", FadeIn(worst))
        self.say("וזה לא תלוי בכמה נמלים יש :\nעם אחת או עם 100, התשובה 100 שניות.")
        self.fade_all()

        # The code: typed, then run on the example.
        code = page_python(QID, "def last_fall")
        steps, result = trace(code, "last_fall", (POS, DIRS))
        assert result == 90 and [s.line for s in steps] == [3]
        panel = CodePanel(code, font_size=30, only=[1, 3])
        self.place_code(panel)
        panel.shift(UP * 0.8)
        self.type_code(panel, [
            (1, "‏last_fall מקבלת את המקומות והכיוונים :\n‏+1 ימינה, ‏-1 שמאלה."),
            (3, ["לכל נמלה, הזמן של הרוח שלה :\n‏p אם היא הולכת שמאלה, אחרת 100 פחות p.",
                 "ומחזירים את המקסימום. אין כאן\nשום סימולציה של התנגשויות."]),
        ], intro="עכשיו נכתוב את זה ב-Python.")
        call = M("last_fall([10, 25, 40, 60, 75, 90], [1, -1, 1, -1, -1, 1])", 26, C.MUTED)
        call.next_to(panel, DOWN, buff=0.6)
        res = M("90", 48, C.AMBER, weight="BOLD").next_to(call, DOWN, buff=0.4)
        self.say("נריץ על שש הנמלים מהעמוד.", FadeIn(call))
        self.run_with(panel, None, steps, [
            ([3], "הזמנים 90, 25, 60, 60, 75 ו-10,\nוהמקסימום 90.", lambda: self.play(FadeIn(res), run_time=0.5)),
        ])
        self.fade_all()

        # The page's box: the lines of the ants, then of the ghosts.
        view = self.box("chart", height=5.6).move_to(UP * 0.62)
        self.say("גם התיבה שבעמוד מציירת את הקווים :\nמקום לרוחב, וזמן כלפי מטה.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי 25 שניות : ארבע התנגשויות\nכבר קרו, ושתי נמלים נפלו."),
            (2, "כמעט בסוף, אחרי 89.5 שניות, נשארה\nרק נמלה 4. הקווים שבורים בכל מפגש."),
            (3, "המתג \"רוחות\" מחליף לקווים ישרים :\nאותם קווים בדיוק, רק הצבעים מתחלפים."),
        ])
        self.fade_all()

        chips = cost_chips(("time", "$O(n)$"), ("memory", "$O(1)$"),
                           notes=("one pass", "the maximum so far"))
        self.say("הסיבוכיות : מעבר אחד על הנמלים,\nזמן O(n) וזיכרון O(1).", FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        trap = TX(r"100 \text{ ants} \;\Rightarrow\; \text{up to } 2500 \text{ collisions}", size=42)
        trap.move_to(UP * 0.8)
        self.say("מלכודת : לסמלץ התנגשות אחרי התנגשות.\nעם 100 נמלים יכולות להיות 2500.", FadeIn(trap))
        ok = TX(r"T = \max_i \,(p_i \ \text{or}\ 100 - p_i)", size=42, color=C.GREEN).next_to(trap, DOWN, buff=0.7)
        self.say("הרוחות חוסכות את כל זה : הזמן תלוי\nרק במקום ובכיוון של כל נמלה לבד.", FadeIn(ok))
        self.fade_all()


class ChapterB(AntScene):
    def construct(self):
        self.chapter_card("סעיף ב", "כמה התנגשויות",
                          "סעיף ב : כמה התנגשויות יהיו בסידור נתון?\nומה המספר הגדול ביותר עם 100 נמלים?")

        # A collision is a crossing of two ghost lines.
        rod = Rod(y=2.55)
        ch = Chart(rod, top=1.85, sy=0.042)
        tt = ValueTracker(90)
        self.say("כל התנגשות היא נקודה שבה שני קווים\nנחתכים. נסתכל על הקווים הישרים של הרוחות.",
                 Create(rod.mob()), FadeIn(ch.axes()), FadeIn(ch.lines(tt, POS, DIRS, ghosts=True)), run_time=1.4)
        dots = VGroup(*[Dot([rod.X(x), ch.Y(t), 0], radius=0.11, color=C.AMBER) for t, x in meetings(POS, DIRS)])
        self.say("בדוגמה יש חמישה חיתוכים, ולכן\nחמש התנגשויות של נמלים.",
                 LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=1.6)
        self.say("שני קווים ישרים נחתכים רק אם\nהם הולכים זה לקראת זה.")
        self.fade_all()

        # Which pairs meet.
        pair = TX(r"a < b,\quad a \rightarrow,\ \ b \leftarrow", size=44).move_to(UP * 2.1)
        self.say("זוג נפגש אם השמאלית הולכת ימינה\nוהימנית שמאלה. זוגות אחרים אף פעם.", FadeIn(pair))
        when = TX(r"t = \frac{b - a}{2} \;<\; \min(b,\ 100 - a)", size=44).next_to(pair, DOWN, buff=0.55)
        self.say("והם תמיד נפגשים בזמן, באמצע הדרך,\nלפני שאחת מהן יוצאת מהמוט.",
                 pair.animate.set_opacity(0.45), FadeIn(when))
        self.fade_all()

        # Count: for each ant going left, the ants going right on its left.
        s = strip(POS, DIRS, 36).move_to(UP * 2.3)
        self.say("סופרים : לכל נמלה שהולכת שמאלה,\nכמה הולכות ימינה ונמצאות משמאלה.", FadeIn(s))
        rows = VGroup(
            M("25←  meets 10→           1", 34),
            M("60←  meets 10→, 40→      2", 34),
            M("75←  meets 10→, 40→      2", 34),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.3)
        with self.beat("‏25 פוגשת את 10. ‏60 ו-75 פוגשות\nכל אחת את 10 ואת 40."):
            for r in rows:
                self.play(FadeIn(r, shift=0.15 * DOWN), run_time=0.6)
        tot = M("total = 5", 40, C.AMBER, weight="BOLD").next_to(rows, DOWN, buff=0.5)
        self.say("סך הכול 1 ועוד 2 ועוד 2 :\nחמש התנגשויות.", FadeIn(tot))
        self.fade_all()

        # The most: k going right, all on the left.
        k = TX(r"k \text{ right},\ \ n - k \text{ left} \;\Rightarrow\; k\,(n - k)", size=44).move_to(UP * 2.1)
        self.say("עם k נמלים שהולכות ימינה,\nיש לכל היותר k כפול n פחות k זוגות.", FadeIn(k))
        demo_p, demo_d = [8, 20, 32, 44, 56, 68, 80, 92], [1, 1, 1, 1, -1, -1, -1, -1]
        r2 = Rod(y=0.5)
        g = VGroup(*[ant("", C.BLUE if d > 0 else C.ORANGE, d, [r2.X(p), r2.y + 0.42, 0])
                     for p, d in zip(demo_p, demo_d)])
        self.say("והמקסימום כשכל ההולכות ימינה\nמשמאל לכל ההולכות שמאלה.",
                 k.animate.set_opacity(0.45), Create(r2.mob(ticks=False)), FadeIn(g, lag_ratio=0.1))
        best = TX(r"k = \frac{n}{2}:\quad 50 \cdot 50 = 2500", size=46, color=C.AMBER).move_to(DOWN * 1.2)
        self.say("‏k(n − k) הכי גדול ב-k = n/2 :\nעם 100 נמלים, 50 כפול 50, ‏2500.", FadeIn(best))
        self.fade_all()

        # The code: typed, then traced ant by ant.
        code = page_python(QID, "def collisions")
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=[1, 3, 4, 5, 6, 7, 8, 9])
        vp = VarPanel(["p", "d", "right", "count"], fmt=lambda n, st: str(st[n]) if n in st else "",
                      size=32).set_state({})
        bar = strip(POS, DIRS, 34)
        self.place_code(panel, vp, extra=bar)
        self.type_code(panel, [
            (1, "‏collisions מקבלת את המקומות והכיוונים,\nומחזירה את מספר ההתנגשויות."),
            (3, "שני מונים : count להתנגשויות,\nו-right לנמלים שהולכות ימינה שעברנו."),
            (4, "עוברים על הנמלים משמאל לימין,\nאחרי מיון לפי המקום."),
            ([5, 6], "נמלה שהולכת ימינה : מוסיפים אחת\nל-right. היא תפגוש את מי שמימינה."),
            ([7, 8], "נמלה שהולכת שמאלה פוגשת את כל\nההולכות ימינה שמשמאלה : מוסיפים right."),
            (9, "בסוף מחזירים את count."),
        ], intro="עכשיו נכתוב את זה ב-Python.")
        self.play(FadeIn(vp), FadeIn(bar), run_time=0.6)
        steps, result = trace(code, "collisions", (POS, DIRS))
        assert result == 5
        mark = [None]

        def at(i):
            def go():
                box = SurroundingRectangle(bar[i], color=C.AMBER, buff=0.1, corner_radius=0.1, stroke_width=4)
                if mark[0] is None:
                    self.play(Create(box), run_time=0.4)
                    mark[0] = box
                else:
                    self.play(Transform(mark[0], box), run_time=0.4)
            return go

        R, L, E = [4, 5, 6], [4, 5, 8], [4, 9]
        self.run_with(panel, vp, steps, [
            ([3], "נריץ על שש הנמלים מהעמוד.\nשני המונים מתחילים ב-0.", None),
            (R, "‏10 הולכת ימינה : right = 1.", at(0)),
            (L, "‏25 הולכת שמאלה, ופוגשת את 10 :\n‏count = 1.", at(1)),
            (R, "‏40 הולכת ימינה : right = 2.", at(2)),
            (L, "‏60 הולכת שמאלה, ופוגשת את 10 ואת 40 :\n‏count = 3.", at(3)),
            (L, "‏75 גם הולכת שמאלה, ופוגשת את שתיהן :\n‏count = 5.", at(4)),
            (R, "‏90 הולכת ימינה, ואין אף אחת מימינה\nשתפגוש אותה : right = 3.", at(5)),
            (E, "הלולאה נגמרה : הפונקציה מחזירה 5.", None),
        ])
        self.fade_all()

        chips = cost_chips(("time", "$O(n \\log n)$"), ("memory", "$O(n)$"),
                           notes=("the sort, then one pass", "the sorted pairs"))
        self.say("הסיבוכיות : המיון עולה O(n log n),\nוהמעבר עצמו O(n). זיכרון O(n) לרשימה.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: a pair that faces apart never meets.
        r3 = Rod(y=0.6)
        tt = ValueTracker(0)
        two = ants_on(r3, tt, [25, 40], [-1, 1], ghosts=True, labels=["1", "2"])
        self.say("מלכודת : לספור כל זוג שהולך בכיוונים\nשונים. כאן 25 שמאלה ו-40 ימינה.",
                 Create(r3.mob()), FadeIn(two), run_time=1.0)
        with self.beat("הן מתרחקות זו מזו, ולא נפגשות אף פעם.\nסופרים רק זוגות שפונים זה לזה."):
            self.run_to(tt, 20, speed=10)
        self.fade_all()


class ChapterC(AntScene):
    def construct(self):
        self.chapter_card("סעיף ג", "מתי נופלת נמלה מסוימת",
                          "סעיף ג : מתי, ומאיזה צד, נופלת\nהנמלה ה-k משמאל? ואיזו נופלת אחרונה?")

        # The order never changes.
        rod = Rod(y=0.9)
        tt = ValueTracker(0)
        ants = ants_on(rod, tt, POS, DIRS)
        self.say("הרעיון הראשון : נמלים לא עוברות זו את זו.\nהן רק נפגשות ומסתובבות.",
                 Create(rod.mob()), FadeIn(ants), run_time=1.2)
        clk = clock(tt, [-5.0, 2.6, 0])
        self.add(clk)
        with self.beat("לכן הסדר לאורך המוט לא משתנה :\nנמלה 1 תמיד הכי שמאלית."):
            self.run_to(tt, 28, speed=10)
        self.say("הנמלה שנופלת משמאל היא תמיד\nהשמאלית ביותר שעוד על המוט.")
        self.fade_all()

        # Who falls on which side.
        f1 = TX(r"\text{left ghosts: } 25,\ 60,\ 75", size=42).move_to(UP * 2.2)
        self.say("הרעיון השני : כל רוח שיוצאת משמאל\nמפילה נמלה משמאל. שלוש רוחות הולכות שמאלה.",
                 FadeIn(f1))
        self.say("לכן נמלים 1, 2 ו-3 נופלות שמאלה,\nאחרי 25, 60 ו-75 שניות, לפי הסדר.")
        f2 = TX(r"\text{right ghosts: } 100-10,\ 100-40,\ 100-90 \;=\; 90,\ 60,\ 10", size=40)
        f2.next_to(f1, DOWN, buff=0.5)
        self.say("הרוחות שהולכות ימינה יוצאות\nאחרי 90, 60 ו-10 שניות.", f1.animate.set_opacity(0.5), FadeIn(f2))
        self.say("מימין הנמלה הימנית ביותר נופלת ראשונה :\nנמלה 6 ב-10, נמלה 5 ב-60, ונמלה 4 ב-90.")
        self.fade_all()

        head = VGroup(*[M(h, 30, C.MUTED) for h in ("ant", "start", "walks", "falls", "at")])
        xs = [-4.4, -2.4, -0.4, 1.8, 4.0]
        for h, x in zip(head, xs):
            h.move_to([x, 2.6, 0])
        rows = VGroup()
        for k, ((p, d), (t, side)) in enumerate(zip(zip(POS, DIRS), FALL)):
            y = 2.0 - k * 0.6
            cells = [str(k + 1), str(p), "→" if d > 0 else "←", "left" if side == "L" else "right", str(t)]
            r = VGroup(*[M(c, 32, COLS[k] if i == 0 else C.WHITE).move_to([x, y, 0]) for i, (c, x) in enumerate(zip(cells, xs))])
            rows.add(r)
        rule = Line([-5.2, 2.3, 0], [4.8, 2.3, 0], color=C.FAINT, stroke_width=2)
        with self.beat("הטבלה : לכל נמלה, מאיזה צד\nהיא נופלת ומתי."):
            self.play(FadeIn(head), Create(rule), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=0.1 * DOWN) for r in rows], lag_ratio=0.2), run_time=2.0)
        ring = SurroundingRectangle(rows[3], color=C.AMBER, buff=0.1, corner_radius=0.1, stroke_width=4)
        self.say("נמלה 4 התחילה ב-60 והלכה שמאלה,\nאבל היא נופלת מימין, אחרונה, ב-90.", Create(ring))
        self.fade_all()

        # The code: typed, then run.
        code = page_python(QID, "def fall_times")
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=[1, 3, 4, 5])
        vp = VarPanel(["left", "right"], fmt=lambda n, st: str(st[n]) if n in st else "", size=32).set_state({})
        self.place_code(panel, vp, vp_width=4.5)
        self.type_code(panel, [
            (1, "‏fall_times מחזירה את זמן הנפילה\nשל כל נמלה, לפי הסדר משמאל."),
            (3, "הזמנים של הרוחות שיוצאות משמאל :\n‏p של ההולכות שמאלה, מהקטן לגדול."),
            (4, "הזמנים של הרוחות שיוצאות מימין :\n‏100 פחות p של ההולכות ימינה."),
            (5, "השמאליות קודם, ואחריהן הימניות\nבסדר הפוך : הימנית ביותר נופלת ראשונה."),
        ], intro="עכשיו נכתוב את זה ב-Python.")
        self.play(FadeIn(vp), run_time=0.4)
        steps, result = trace(code, "fall_times", (POS, DIRS))
        assert result == [t for t, _ in FALL]
        res = M("[25, 60, 75, 90, 60, 10]", 34, C.AMBER).next_to(VGroup(panel, vp), DOWN, buff=0.45)
        self.run_with(panel, vp, steps, [
            ([3], "נריץ על הדוגמה : משמאל יוצאות\nהרוחות של 25, 60 ו-75.", None),
            ([4], "מימין : ‏100 פחות 10, 40 ו-90,\nממוינים : 10, 60 ו-90.", None),
            ([5], "והתוצאה : 25, 60, 75, ואז 90, 60 ו-10.\nהמקסימום של נמלה 4, ‏90.", lambda: self.play(FadeIn(res), run_time=0.5)),
        ])
        self.fade_all()

        # The page's box: the falls one by one.
        view = self.box("pole", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד : המוט, ומתחתיו\nמתי נופלת כל נמלה.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי 10 שניות נמלה 6 נופלת מימין,\nהראשונה."),
            (2, "אחרי 25 שניות נמלה 1 נופלת משמאל."),
            (3, "אחרי 60 שניות שתיים נופלות יחד :\nנמלה 2 משמאל, ונמלה 5 מימין."),
            (4, "ב-75 נמלה 3 נופלת משמאל. נשארה רק\nנמלה 4, והיא תיפול מימין ב-90."),
        ])
        self.fade_all()

        chips = cost_chips(("time", "$O(n \\log n)$"), ("memory", "$O(n)$"),
                           notes=("two sorts", "two lists of times"))
        self.say("הסיבוכיות : שני מיונים, O(n log n),\nושתי רשימות של זמנים, O(n).", FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        r4 = Rod(y=0.6)
        a4 = ant("4", COLS[3], -1, [r4.X(60), r4.y + 0.42, 0])
        arrow = Arrow([r4.X(60), -0.4, 0], [r4.X(100), -0.4, 0], color=C.AMBER, buff=0, stroke_width=5)
        self.say("מלכודת : \"הנמלה נופלת מהצד שאליו\nהיא פונה\". נמלה 4 פונה שמאלה.",
                 Create(r4.mob()), FadeIn(a4), run_time=1.0)
        self.say("אבל היא נופלת מימין. מה שהולך ישר\nהוא הרוח, לא הנמלה.", GrowArrow(arrow))
        self.fade_all()


class ChapterD(AntScene):
    def construct(self):
        self.chapter_card("סעיף ד", "מסלול מעגלי",
                          "סעיף ד, בקצרה : המוט מתעקם למעגל,\nבלי קצוות, ואף נמלה לא נופלת.")
        centre, rad = np.array([-3.3, 0.55, 0]), 2.45

        def ang(p):
            return PI / 2 - p / LEN * TAU          # clockwise from the top, 0 at the top

        def pt(p, r=rad):
            a = ang(p)
            return centre + r * np.array([np.cos(a), np.sin(a), 0])

        circ = Circle(radius=rad, color=C.WHITE, stroke_width=5).move_to(centre)
        places = VGroup()
        for p, d in zip(POS, RING):
            a0, a1 = ang(p) + 0.16 * d, ang(p) - 0.2 * d       # clockwise: the angle falls
            r = rad + 0.55
            arc = Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=centre, color=C.MUTED,
                      stroke_width=5).add_tip(tip_length=0.18, tip_width=0.18)
            places.add(VGroup(arc, M(str(p), 26, C.MUTED).move_to(centre + (rad + 1.05) * np.array([np.cos(ang(p)), np.sin(ang(p)), 0]))))
        labels = [ant(str(i), COLS[i], 0, pt(p)) for i, p in enumerate(POS)]
        self.say("אותן שש נמלים, אבל ארבע הולכות\nעם כיוון השעון, ורק 60 ו-75 נגדו.",
                 Create(circ), FadeIn(places), *[FadeIn(l) for l in labels], run_time=1.4)
        f1 = TX(r"t = 100:\ \text{every ghost is home}", size=34).move_to([3.0, 2.3, 0])
        self.say("כל רוח משלימה סיבוב ב-100 שניות :\nקבוצת המקומות והכיוונים חוזרת.", FadeIn(f1))
        f2 = TX(r"s = R - L = 4 - 2 = 2", size=40, color=C.AMBER).next_to(f1, DOWN, buff=0.55)
        self.say("אבל הסדר המעגלי מסתובב : כל נמלה\nזזה s = R − L מקומות, כאן 2.", FadeIn(f2))
        lap = M("lap 0", 34, C.MUTED).next_to(f2, DOWN, buff=0.6)
        self.add(lap)
        cur = list(range(6))          # cur[j]: the ant standing at place j
        for k in (1, 2, 3):
            cur = [cur[(j - S) % 6] for j in range(6)]
            new = [None] * 6
            for j, i in enumerate(cur):
                new[i] = ant(str(i), COLS[i], 0, pt(POS[j]))
            cap = {1: "אחרי 100 שניות : נמלה 0 עומדת\nבמקום של נמלה 2, וכך כולן.",
                   2: "אחרי 200 שניות : עוד שני מקומות.",
                   3: "אחרי 300 שניות כולן בבית,\nבאותו מקום ובאותו כיוון."}[k]
            self.say(cap, *[Transform(labels[i], new[i], path_arc=-PI / 3) for i in range(6)],
                     Transform(lap, M(f"lap {k}", 34, C.MUTED).move_to(lap)), run_time=1.2)
        assert cur == list(range(6))
        f3 = VGroup(TX(r"\frac{n}{\gcd(n,\, s)} = \frac{6}{2} = 3 \ \text{laps}", size=36, color=C.GREEN),
                    TX(r"3 \cdot 100 = 300\ \text{s}", size=36, color=C.GREEN)).arrange(DOWN, buff=0.3)
        f3.next_to(lap, DOWN, buff=0.45)
        self.say("בכלל : n חלקי gcd של n ו-s סיבובים.\nכאן 6 חלקי 2, שלושה סיבובים : ‏300 שניות.", FadeIn(f3))
        self.fade_all()


class Closing(AntScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"\max_i\,(p_i \ \text{or}\ 100 - p_i) \le 100", size=34)),
                           ("ב", TX(r"\#\{a \rightarrow\ \ b \leftarrow,\ a < b\} \le 50 \cdot 50", size=34)),
                           ("ג", M("order kept: left times, then right ones", 30)),
                           ("ד", TX(r"s = R - L,\quad n / \gcd(n, s) \ \text{laps}", size=34))],
                     ["לסיכום : רוחות שעוברות זו דרך זו\nפותרות את כל ארבעת הסעיפים.",
                      "נסו סידורים משלכם בתיבה\nשבעמוד של שאלה 0057 באתר."],
                     holds=(3.5, 3.5))
