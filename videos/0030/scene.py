"""The tutorial video of question 0030, the spider and the fly on a box (script: script.md).

Render with `python videos/render.py 0030` (see VIDEOS.md). Part א has no code: the box is
drawn in 3D (an orthographic projection of the room, turned by a camera of its own), and
its faces unfold into the plane around their shared edges, as cardboard opens, so that a
path on the box becomes a straight line. First the obvious route over the ceiling (42),
then the route over one long wall (43.17), then the stair-shaped net of five faces where
S and F are the corners of a right triangle with legs 32 and 24: 40. The line folds back
onto the box and the route is told face by face, with the page's points. Part ב is the
idea of the code only (the owner's choice: no code typed): the four lateral faces unroll
into one periodic strip, every end wall folds onto it around one of its four edges (four
images of S and four of F), 4 x 4 x 3 = 48 lines with the shift of one period, two checks
per line, and the shortest valid one; then the page's strip box (valid lines, all 48, the
shortest only).

Every number is computed here from the page's figure generator (tools/figures/q0030.py)
and checked with asserts.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, T, chip, cost_chips, he, read_palette  # noqa: E402
import q0030  # noqa: E402

QID = 30
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – המרחק הקצר ביותר והמסלול"),
    ("ChapterB", "סעיף ב – כל הפריסות ברצועה אחת"),
    ("Closing", "סיכום"),
]

# The page's strip box (data-kind="strip", the question's room and points): the strip (its
# summary line left out, so the chart is large enough), with the valid lines (as the page opens it), all 48, then the shortest only.
BOXES = {
    "strip": {"box": 0, "region": [".strip-chart"], "hide": [".viz-legend"],
              "steps": [[], [["set", ".ex-show", "all"]], [["set", ".ex-show", "best"]],
                        [["fill", ".ex-z0", "6"]], [["fill", ".ex-z0", "11"], ["fill", ".ex-y0", "2"]]]},
}

_S = read_palette()["slate"]
S_COL, F_COL, MARK = _S["--viz-s1"], C.ORANGE, C.GREEN
PATH = C.AMBER
# every face its own colour (the owner, 2026-11-02), kept through the unfolding and in the strip
FACE_COL = {"end0": _S["--viz-s4"], "enda": _S["--viz-s5"], "top": _S["--viz-s1"],
            "sideB": _S["--viz-s3"], "bottom": C.CRATE, "side0": C.MUTED}
FACE_OPACITY = 0.3

# ---- the numbers, from the page's generator --------------------------------------------------

A, B, H = q0030.A, q0030.B, q0030.H
SP, FL = q0030.S, q0030.F
assert (A, B, H, SP, FL) == (30, 12, 12, (0, 6, 11), (30, 6, 1))
CANDS = q0030.candidates()
BEST = q0030.best()
assert len(CANDS) == 48 and BEST["length"] == 40 and (BEST["dx"], BEST["dp"]) == (32, -24)
assert BEST["faces"] == ["end0", "top", "sideB", "bottom", "enda"]
assert BEST["p_exit"] == 29.25 and BEST["p_enter"] == 6.75
VALID = [c for c in CANDS if c["valid"]]
assert len(VALID) == 22
# the 16 face orders of the page's table and their lengths
TABLE = {}
for c in VALID:
    if len(set(c["faces"])) == len(c["faces"]):      # no face twice (as the page's table)
        TABLE.setdefault(tuple(c["faces"]), round(c["length"], 2))
assert len(TABLE) == 16
ORDERS = []                      # one candidate per face order, shortest first (the page's table)
for c in VALID:
    if len(set(c["faces"])) == len(c["faces"]) and all(tuple(o["faces"]) != tuple(c["faces"]) for o in ORDERS):
        ORDERS.append(c)
assert len(ORDERS) == 16 and ORDERS[0]["faces"] == BEST["faces"]
COUNTS = {}
for v in TABLE.values():
    COUNTS[v] = COUNTS.get(v, 0) + 1
assert COUNTS == {40.0: 2, 40.72: 4, 42.0: 2, 43.17: 2, 47.52: 4, 57.27: 2}
assert round(math.hypot(42, 10), 2) == 43.17 and math.hypot(32, 24) == 40
assert round(math.hypot(30, 10), 1) == 31.6
# the spider moved in the box: half way down (the floor wins, 37), near the near wall (four faces)
_MID, _NEAR = q0030.best(s=(0, 6, 6)), q0030.best(s=(0, 2, 11))
assert _MID["length"] == 37 and _MID["faces"] == ["end0", "bottom", "enda"]
assert round(_NEAR["length"], 2) == 37.12 and _NEAR["faces"] == ["end0", "side0", "bottom", "enda"]
S_IMG = [(e, -float(d), float(p)) for e, d, p, lo, hi in q0030.images(SP[1], SP[2])]
F_IMG = [(e, A + float(d), float(p)) for e, d, p, lo, hi in q0030.images(FL[1], FL[2])]
assert [(x, p) for _, x, p in S_IMG] == [(-11, 6), (-6, 23), (-1, 30), (-6, 37)]
assert [(x, p) for _, x, p in F_IMG] == [(31, 6), (36, 13), (41, 30), (36, 47)]
RANGES = q0030.bands()
assert RANGES == {"bottom": (0, 12), "sideB": (12, 24), "top": (24, 36), "side0": (36, 48)}
# the route in space (step 6 of the page) and the crossings in the net
ROUTE = [(0, 6, 11), (0, 6.75, 12), (7, 12, 12), (23, 12, 0), (30, 6.75, 0), (30, 6, 1)]
SEGS = [math.dist(a, b) for a, b in zip(ROUTE, ROUTE[1:])]
MIRROR = [(x, B - y, z) for x, y, z in ROUTE]       # the same route over the near wall
assert abs(sum(math.dist(a, b) for a, b in zip(MIRROR, MIRROR[1:])) - 40) < 1e-9
assert [round(s, 2) for s in SEGS] == [1.25, 8.75, 20, 8.75, 1.25] and round(sum(SEGS), 9) == 40
# an invalid line of the strip: S over side0, F over sideB, k = 0
BAD = next(c for c in CANDS if (c["s_edge"], c["f_edge"], c["k"]) == ("side0", "sideB", 0))
assert not BAD["valid"] and round(float(BAD["p_exit"]), 2) == 33.57

# ---- 3D: the faces, the nets and the camera ------------------------------------------------


def rot_about_p(pt, c, th):
    """Rotate (x, p, n) about the line p = c of the plane n = 0 (along x)."""
    x, p, n = pt
    ct, st = math.cos(th), math.sin(th)
    return (x, c + (p - c) * ct - n * st, (p - c) * st + n * ct)


def rot_about_x(pt, c, th):
    """Rotate (x, p, n) about the line x = c of the plane n = 0 (along p)."""
    x, p, n = pt
    ct, st = math.cos(th), math.sin(th)
    return (c + (x - c) * ct - n * st, p, (x - c) * st + n * ct)


class Net:
    """Faces laid flat in the net's plane (x, p), each hinged to its parent along an edge.
    Folded (s = 1) the faces are the box's; flat (s = 0) they lie in the plane. `world`
    maps the root face's frame (x, p, n) to the room (x, y, z)."""

    def __init__(self, faces: dict, world):
        self.faces, self.world = faces, world

    def point(self, face: str, x: float, p: float, s: float) -> np.ndarray:
        pt, f = (x, p, 0.0), face
        while self.faces[f].get("parent"):
            fd = self.faces[f]
            th = fd["sign"] * s * math.pi / 2
            axis, c = fd["hinge"]
            pt = rot_about_p(pt, c, th) if axis == "p" else rot_about_x(pt, c, th)
            f = fd["parent"]
        return np.array(self.world(pt), dtype=float)

    def corners(self, face: str, s: float) -> list:
        x0, x1, p0, p1 = self.faces[face]["rect"]
        return [self.point(face, x, p, s) for x, p in ((x0, p0), (x1, p0), (x1, p1), (x0, p1))]


SIDE_B = lambda pt: (pt[0], B - pt[2], pt[1] - B)          # noqa: E731  root: the far wall
TOP_ROOT = lambda pt: (pt[0], 2 * B + H - pt[1], H - pt[2])   # noqa: E731  root: the ceiling

# The obvious route: the spider's wall, the ceiling and the fly's wall in one row.
NAIVE = Net({"top": {"rect": (0, A, B + H, 2 * B + H), "kind": "side"},
             "end0": {"rect": (-H, 0, B + H, 2 * B + H), "parent": "top", "hinge": ("x", 0), "sign": -1, "kind": "end"},
             "enda": {"rect": (A, A + H, B + H, 2 * B + H), "parent": "top", "hinge": ("x", A), "sign": 1, "kind": "end"}},
            TOP_ROOT)
# Over the far wall: the two end walls hinged to its short edges.
SIDE = Net({"sideB": {"rect": (0, A, B, B + H), "kind": "side"},
            "end0": {"rect": (-B, 0, B, B + H), "parent": "sideB", "hinge": ("x", 0), "sign": -1, "kind": "end"},
            "enda": {"rect": (A, A + B, B, B + H), "parent": "sideB", "hinge": ("x", A), "sign": 1, "kind": "end"}},
           SIDE_B)
# The stairs: the spider's wall on the ceiling, the ceiling on the far wall, the far wall on
# the floor, the floor on the fly's wall (the page's step 3).
STAIRS = Net({"sideB": {"rect": (0, A, B, B + H), "kind": "side"},
              "top": {"rect": (0, A, B + H, 2 * B + H), "parent": "sideB", "hinge": ("p", B + H), "sign": 1, "kind": "side"},
              "bottom": {"rect": (0, A, 0, B), "parent": "sideB", "hinge": ("p", B), "sign": -1, "kind": "side"},
              "end0": {"rect": (-H, 0, B + H, 2 * B + H), "parent": "top", "hinge": ("x", 0), "sign": -1, "kind": "end"},
              "enda": {"rect": (A, A + H, 0, B), "parent": "bottom", "hinge": ("x", A), "sign": 1, "kind": "end"}},
             SIDE_B)
# The hoop of part ב: the four lateral faces, in the strip's order.
HOOP = Net({"sideB": {"rect": (0, A, B, B + H), "kind": "side"},
            "top": {"rect": (0, A, B + H, 2 * B + H), "parent": "sideB", "hinge": ("p", B + H), "sign": 1, "kind": "side"},
            "side0": {"rect": (0, A, 2 * B + H, 2 * (B + H)), "parent": "top", "hinge": ("p", 2 * B + H), "sign": 1, "kind": "side"},
            "bottom": {"rect": (0, A, 0, B), "parent": "sideB", "hinge": ("p", B), "sign": -1, "kind": "side"}},
           SIDE_B)

# the six faces of the room, for the faces a net leaves out
BOX_FACES = {
    "end0": ([0, 0, 0], [0, B, 0], [0, B, H], [0, 0, H]),
    "enda": ([A, 0, 0], [A, B, 0], [A, B, H], [A, 0, H]),
    "bottom": ([0, 0, 0], [A, 0, 0], [A, B, 0], [0, B, 0]),
    "top": ([0, 0, H], [A, 0, H], [A, B, H], [0, B, H]),
    "sideB": ([0, B, 0], [A, B, 0], [A, B, H], [0, B, H]),
    "side0": ([0, 0, 0], [A, 0, 0], [A, 0, H], [0, 0, H]),
}
# every net brings S and F along: (face, x, p)
POINTS = {
    NAIVE: (("end0", -1, 30), ("enda", 41, 30)),
    SIDE: (("end0", -6, 23), ("enda", 36, 13)),
    STAIRS: (("end0", -1, 30), ("enda", 31, 6)),
}
for net, (s_pt, f_pt) in POINTS.items():     # each image folds back onto the real point
    assert np.allclose(net.point(*s_pt, 1.0), SP) and np.allclose(net.point(*f_pt, 1.0), FL)
for net in (NAIVE, SIDE, STAIRS, HOOP):      # and each face onto the room's face
    for name in net.faces:
        got = sorted(map(tuple, np.round(net.corners(name, 1.0), 6)))
        assert got == sorted(map(tuple, np.array(BOX_FACES[name], dtype=float))), name

# the routes as polylines on their faces, in the net's coordinates
NAIVE_PATH = [("end0", [(-1, 30), (0, 30)]), ("top", [(0, 30), (30, 30)]), ("enda", [(30, 30), (41, 30)])]
SIDE_PATH = [("end0", [(-6, 23), (0, 23 - 10 * 6 / 42)]),
             ("sideB", [(0, 23 - 10 * 6 / 42), (30, 23 - 10 * 36 / 42)]),
             ("enda", [(30, 23 - 10 * 36 / 42), (36, 13)])]
BEST_PATH = [("end0", [(-1, 30), (0, 29.25)]), ("top", [(0, 29.25), (7, 24)]),
             ("sideB", [(7, 24), (23, 12)]), ("bottom", [(23, 12), (30, 6.75)]),
             ("enda", [(30, 6.75), (31, 6)])]
assert np.allclose(STAIRS.point("top", 0, 29.25, 1.0), ROUTE[1])
assert np.allclose(STAIRS.point("sideB", 7, 24, 1.0), ROUTE[2])
assert np.allclose(STAIRS.point("bottom", 23, 12, 1.0), ROUTE[3])
assert np.allclose(STAIRS.point("enda", 30, 6.75, 1.0), ROUTE[4])
assert abs(sum(math.dist(*seg) for _, seg in BEST_PATH) - 40) < 1e-9


class Room(VGroup):
    """The room on the screen: an orthographic camera (azimuth, elevation, scale, the screen
    point of the room's centre), the faces of one net folded by `s`, the faces the net leaves
    out (faded by `ghost`), S and F, and a route drawn up to `draw` of its length."""

    def __init__(self, net: Net, phi=28, theta=24, scale=0.23, at=(0.0, 0.75), center=(A / 2, B / 2, H / 2)):
        super().__init__()
        self.net = net
        self.phi, self.theta = ValueTracker(phi), ValueTracker(theta)
        self.scale_t = ValueTracker(scale)
        self.ax, self.ay = ValueTracker(at[0]), ValueTracker(at[1])
        self.cx, self.cy, self.cz = (ValueTracker(v) for v in center)
        self.s = ValueTracker(1.0)
        self.ghost = ValueTracker(1.0)
        self.draw = ValueTracker(0.0)
        self.route: list = []
        self.faces_mob = always_redraw(self._faces)
        self.route_mob = always_redraw(self._route)
        self.s_dot = Dot(radius=0.12, color=S_COL, stroke_color=C.WHITE, stroke_width=2.5)
        self.f_dot = Dot(radius=0.12, color=F_COL, stroke_color=C.WHITE, stroke_width=2.5)
        self.s_lab = TX("S", size=36, color=S_COL)
        self.f_lab = TX("F", size=36, color=F_COL)
        self.s_dot.add_updater(lambda m: m.move_to(self.screen(self.net.point(*POINTS.get(self.net, POINTS[STAIRS])[0], self.s.get_value()))))
        self.f_dot.add_updater(lambda m: m.move_to(self.screen(self.net.point(*POINTS.get(self.net, POINTS[STAIRS])[1], self.s.get_value()))))
        self.s_lab.add_updater(lambda m: m.next_to(self.s_dot, LEFT, buff=0.12))
        self.f_lab.add_updater(lambda m: m.next_to(self.f_dot, RIGHT, buff=0.12))
        self.add(self.faces_mob, self.route_mob, self.s_dot, self.f_dot, self.s_lab, self.f_lab)

    # the camera
    def basis(self):
        ph, th = math.radians(self.phi.get_value()), math.radians(self.theta.get_value())
        r = np.array([math.cos(ph), -math.sin(ph), 0.0])
        f = np.array([math.sin(ph) * math.cos(th), math.cos(ph) * math.cos(th), -math.sin(th)])
        u = np.cross(r, f)
        return r, u, f

    def screen(self, P) -> np.ndarray:
        r, u, _ = self.basis()
        rel = np.asarray(P, dtype=float) - np.array([self.cx.get_value(), self.cy.get_value(), self.cz.get_value()])
        k = self.scale_t.get_value()
        return np.array([self.ax.get_value() + k * rel.dot(r), self.ay.get_value() + k * rel.dot(u), 0.0])

    def depth(self, pts) -> float:
        _, _, f = self.basis()
        c = np.mean(np.asarray(pts, dtype=float), axis=0)
        return float(c.dot(f))

    def flat(self, x: float, p: float) -> np.ndarray:
        """The screen point of the net's (x, p) when the net is flat (any s, the net's frame)."""
        return self.screen(self.net.world((x, p, 0.0)))

    # the pictures
    def _quad(self, pts, name: str, opacity: float) -> Polygon:
        col = FACE_COL[name]
        return Polygon(*[self.screen(p) for p in pts], stroke_color=col, stroke_width=2.5,
                       stroke_opacity=0.95 * opacity, fill_color=col, fill_opacity=FACE_OPACITY * opacity)

    def _faces(self) -> VGroup:
        s = self.s.get_value()
        items = []
        for name, fd in self.net.faces.items():
            pts = self.net.corners(name, s)
            items.append((self.depth(pts), pts, name, 1.0))
        g = self.ghost.get_value()
        if g > 0.01:
            for name, pts in BOX_FACES.items():
                if name not in self.net.faces:
                    items.append((self.depth(pts), pts, name, g * (0.6 if name == "side0" else 1.0)))
        items.sort(key=lambda t: -t[0])          # the farthest first
        return VGroup(*[self._quad(pts, name, op) for _, pts, name, op in items])

    def _route(self) -> VMobject:
        s, d = self.s.get_value(), self.draw.get_value()
        pts3 = []
        for face, seg in self.route:
            for x, p in seg:
                pts3.append(self.net.point(face, x, p, s))
        m = VMobject(stroke_color=PATH, stroke_width=6)
        if len(pts3) < 2 or d <= 0:
            return m.set_points_as_corners([ORIGIN, ORIGIN + RIGHT * 1e-4]).set_stroke(opacity=0)
        scr = [self.screen(p) for p in pts3]
        lens = [np.linalg.norm(b - a) for a, b in zip(pts3, pts3[1:])]
        total, want, out = sum(lens), d * sum(lens), [scr[0]]
        for k, L in enumerate(lens):
            if want >= L:
                out.append(scr[k + 1])
                want -= L
            else:
                t = want / L if L else 0
                out.append(scr[k] + (scr[k + 1] - scr[k]) * t)
                break
        return m.set_points_as_corners(out)

    def set_net(self, net: Net, route=None):
        self.net = net
        self.route = route or []


def stop(room: Room):
    """Freeze the room's updaters before it is faded out."""
    for m in (room.s_dot, room.f_dot, room.s_lab, room.f_lab):
        m.clear_updaters()


def dims(room: Room) -> VGroup:
    """The room's three sizes beside its edges (in the box view)."""
    a = M(str(A), 30, C.MUTED).move_to(room.screen([A / 2, 0, 0]) + DOWN * 0.35)
    b = M(str(B), 30, C.MUTED).move_to(room.screen([A, B / 2, H]) + UP * 0.35 + RIGHT * 0.2)
    h = M(str(H), 30, C.MUTED).move_to(room.screen([A, 0, H / 2]) + RIGHT * 0.4)
    return VGroup(a, b, h)


class SpiderScene(DVQScene):
    """Helpers shared by the scenes of 0030."""

    def turn(self, room: Room, to: float, run_time: float = 2.0):
        self.play(room.phi.animate.set_value(to), run_time=run_time, rate_func=smooth)

    def unfold(self, room: Room, theta: float, phi: float = 0.0, scale=None, at=None, run_time: float = 3.0):
        """Open the net flat while the camera turns to look straight at its plane."""
        anims = [room.s.animate.set_value(0.0), room.theta.animate.set_value(theta),
                 room.phi.animate.set_value(phi), room.ghost.animate.set_value(0.0)]
        if scale is not None:
            anims.append(room.scale_t.animate.set_value(scale))
        if at is not None:
            anims += [room.ax.animate.set_value(at[0]), room.ay.animate.set_value(at[1])]
        self.play(*anims, run_time=run_time, rate_func=smooth)

    def fold(self, room: Room, theta: float = 24, phi: float = 28, scale=0.23, at=(0.0, 0.75), run_time: float = 3.0):
        self.play(room.s.animate.set_value(1.0), room.theta.animate.set_value(theta),
                  room.phi.animate.set_value(phi), room.ghost.animate.set_value(1.0),
                  room.scale_t.animate.set_value(scale), room.ax.animate.set_value(at[0]),
                  room.ay.animate.set_value(at[1]), run_time=run_time, rate_func=smooth)


# ---- the scenes ----------------------------------------------------------------------------


class Opening(SpiderScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "העכביש והזבוב",
                     ["א · הדרך הקצרה ביותר", "ב · כל הפריסות"],
                     ["שאלה 0030 : העכביש והזבוב,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : הדרך הקצרה ביותר על פני התיבה,\nואז רעיון לקוד שבודק את כל הפריסות."])
        self.fade_all()
        room = Room(STAIRS)
        d = dims(room)
        self.say("חדר בצורת תיבה : אורכו 30,\nרוחבו 12 וגובהו 12.",
                 FadeIn(room.faces_mob), FadeIn(d), run_time=1.2)
        self.add(room.route_mob)
        self.say("העכביש S על קיר קצה, באמצע הרוחב,\nיחידה אחת מתחת לתקרה.",
                 FadeIn(room.s_dot, scale=1.6), FadeIn(room.s_lab))
        self.say("הזבוב F על הקיר שממול, באמצע הרוחב,\nיחידה אחת מעל הרצפה.",
                 FadeIn(room.f_dot, scale=1.6), FadeIn(room.f_lab))
        with self.beat("העכביש הולך רק על פני התיבה, לא באוויר.\nמה הדרך הקצרה ביותר אל הזבוב?"):
            self.play(FadeOut(d), run_time=0.4)
            self.turn(room, -28, run_time=1.8)
            self.turn(room, 28, run_time=1.8)
        stop(room)
        self.fade_all()


class ChapterA(SpiderScene):
    def construct(self):
        self.chapter_card("סעיף א", "המרחק הקצר ביותר והמסלול",
                          "סעיף א : מה המרחק הקצר ביותר,\nואיפה העכביש עובר מפאה לפאה?")
        room = Room(NAIVE)
        room.draw.set_value(0)
        self.play(FadeIn(room), run_time=0.8)
        self.naive(room)
        self.side(room)
        self.stairs(room)
        self.back(room)
        self.all_orders()

    def naive(self, room: Room):
        room.set_net(NAIVE, NAIVE_PATH)
        self.say("המסלול שעולה ראשון : למעלה לתקרה,\nלאורך כל התקרה, ולמטה אל הזבוב.",
                 room.draw.animate.set_value(1.0), run_time=2.4)
        total = TX(r"1 + 30 + 11 = 42", size=46).move_to([0, -1.85, 0])
        self.say("האורך : ‏1 + 30 + 11 = 42.\nזו התשובה שעולה ראשונה, והיא לא נכונה.", FadeIn(total))
        self.play(FadeOut(total), run_time=0.4)
        with self.beat("פורסים את שלוש הפאות למישור, כמו קרטון :\nהמסלול הופך לקו ישר באורך 42."):
            self.unfold(room, theta=90, scale=0.17, at=(0.0, 0.9), run_time=3.0)
        self.say("אותו אורך בדיוק דרך הרצפה : ‏11 + 30 + 1.\nאבל אולי פאות אחרות נותנות קו קצר יותר?")
        self.play(room.draw.animate.set_value(0.0), run_time=0.6)
        self.fold(room, run_time=2.4)

    def side(self, room: Room):
        room.set_net(SIDE, SIDE_PATH)
        with self.beat("דרך אחד הקירות הארוכים : פורסים\nאת שני קירות הקצה אל הקיר הרחוק."):
            self.unfold(room, theta=0, scale=0.17, at=(0.0, 0.6), run_time=3.0)
            self.play(room.draw.animate.set_value(1.0), run_time=1.4)
        eq = TX(r"\sqrt{42^2 + 10^2} \approx 43.17", size=44).move_to([0, -1.9, 0])
        self.say("‏S ו-F שניהם 6 מהקפל, בגבהים 11 ו-1 :\nהקו ארוך יותר, 43.17.", FadeIn(eq))
        self.play(FadeOut(eq), room.draw.animate.set_value(0.0), run_time=0.6)
        self.fold(room, run_time=2.4)

    def stairs(self, room: Room):
        room.set_net(STAIRS, BEST_PATH)
        with self.beat("עכשיו חמש פאות, במדרגות : הקיר של העכביש,\nהתקרה, הקיר הרחוק, הרצפה והקיר של הזבוב."):
            self.turn(room, 36, run_time=1.2)
            self.unfold(room, theta=0, scale=0.17, at=(-1.6, 0.68), run_time=3.4)
        self.say("בפריסה הזו הקו הישר מ-S ל-F\nחוצה את כל חמש הפאות.",
                 room.draw.animate.set_value(1.0), run_time=1.8)
        corner = room.flat(31, 30)
        h_leg = DashedLine(room.flat(-1, 30), corner, stroke_color=C.WHITE, stroke_width=3)
        v_leg = DashedLine(corner, room.flat(31, 6), stroke_color=C.WHITE, stroke_width=3)
        h_lab = M("32", 32, C.WHITE).next_to(h_leg, UP, buff=0.12)
        v_lab = M("24", 32, C.WHITE).next_to(v_leg, RIGHT, buff=0.15)
        self.say("‏S ו-F הם קודקודים של משולש ישר-זווית.\nאופקית : ‏1 + 30 + 1 = 32.",
                 Create(h_leg), FadeIn(h_lab))
        self.say("ואנכית : חצי תקרה, הקיר הרחוק וחצי רצפה,\n‏6 + 12 + 6 = 24.", Create(v_leg), FadeIn(v_lab))
        eq = TX(r"d = \sqrt{32^2 + 24^2}", r"= \sqrt{1600}", r"= 40", size=42)
        eq.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45).set_y(1.95)
        eq[2].set_color(C.AMBER)
        self.say("פיתגורס : שורש של 1,024 + 576,\nכלומר שורש של 1,600 : בדיוק 40.", Write(eq), run_time=1.8)
        cross = VGroup(*[Dot(room.flat(x, p), radius=0.08, color=MARK)
                         for x, p in ((0, 29.25), (7, 24), (23, 12), (30, 6.75))])
        self.say("הקו חוקי : הוא חוצה כל קפל בתוך הצלע,\nב-x = 7 וב-x = 23, ויוצא ונכנס דרך הצלעות.",
                 FadeIn(cross, lag_ratio=0.2))
        self.play(FadeOut(VGroup(h_leg, v_leg, h_lab, v_lab, cross)), FadeOut(eq), run_time=0.6)

    def back(self, room: Room):
        with self.beat("מקפלים בחזרה, והקו הישר\nהופך למסלול על פני התיבה."):
            self.fold(room, theta=26, phi=34, run_time=3.4)
        self.say("הוא עולה על הקיר שלו לתקרה, חוצה אותה\nבאלכסון לקיר הרחוק, ויורד עליו עד הרצפה.")
        with self.beat("משם באלכסון על הרצפה לקיר של הזבוב,\nועולה אליו. חמש פאות, ולא שלוש."):
            self.turn(room, -20, run_time=2.6)
        segs = TX(r"1.25 + 8.75 + 20 + 8.75 + 1.25 = 40", size=42).move_to([0, -1.9, 0])
        self.say("האורכים על הפאות : ‏1.25, ‏8.75, ‏20,\n‏8.75 ו-1.25. ביחד 40.", FadeIn(segs))
        mirror = always_redraw(lambda: VMobject(stroke_color=C.WHITE, stroke_width=4, stroke_opacity=0.85)
                               .set_points_as_corners([room.screen(q) for q in MIRROR]))
        with self.beat("ויש תמונת ראי : אותו מסלול דרך הקיר הקרוב,\nגם הוא באורך 40 בדיוק."):
            self.play(FadeOut(segs), Create(mirror), run_time=1.6)
            self.turn(room, 30, run_time=2.4)
        mirror.clear_updaters()
        stop(room)
        self.fade_all()

    def all_orders(self):
        """The page's table of every unfolding, by how many faces it crosses: the middle faces
        (between the two end walls) and the length."""
        cols, cells = VGroup(), {}
        for n in (3, 4, 5):
            rows = [c for c in ORDERS if len(c["faces"]) == n]
            lines = VGroup()
            for c in rows:
                mid = " > ".join(c["faces"][1:-1])
                length = f"{round(c['length'], 2):g}"
                row = VGroup(M(mid, 28, C.WHITE), M(length, 28, C.AMBER if c["length"] == 40 else C.WHITE))
                lines.add(row)
                cells[id(c)] = row
            w = max(r[0].width for r in lines)
            for r in lines:
                r[1].next_to(r[0], RIGHT, buff=0.35).shift(RIGHT * (w - r[0].width))
            lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            head = M(f"{n} faces", 30, C.MUTED)
            col = VGroup(head, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            cols.add(col)
        cols.arrange(RIGHT, aligned_edge=UP, buff=0.8)
        if cols.width > 13.2:
            cols.scale_to_fit_width(13.2)
        cols.move_to([0, 1.0, 0])
        assert [len(c[1]) for c in cols] == [4, 8, 4]
        self.say("כל הפריסות שבעמוד : דרך שלוש פאות,\nארבע או חמש, וכל אחת עם האורך שלה.",
                 *[FadeIn(c, lag_ratio=0.1) for c in cols], run_time=2.0)
        best = VGroup(*[cells[id(c)] for c in ORDERS if c["length"] == 40])
        self.say("הקצר ביותר 40, פעמיים : המסלול שלנו\nותמונת הראי שלו, דרך הקיר הקרוב.",
                 *[Circumscribe(r, color=C.AMBER, buff=0.08) for r in best])
        naive = VGroup(*[cells[id(c)] for c in ORDERS if c["length"] == 42])
        self.say("ו-42, המסלול שעולה ראשון,\nרק במקום השביעי.", *[Indicate(r, color=C.WHITE, scale_factor=1.1) for r in naive])
        low = TX(r"\sqrt{30^2 + 10^2} \approx 31.6", size=40).move_to([0, -1.85, 0])
        self.say("וחסם תחתון : דרך האוויר, 31.6.\nשום מסלול על הפאות לא קצר ממנו.", FadeIn(low))
        self.fade_all()


class ChapterB(SpiderScene):
    K = 0.118                     # the strip's scale on the screen
    AT = (-2.6, 0.55)             # the screen point of the strip's centre (x = 15, p = 24)

    def sp(self, x: float, p: float) -> np.ndarray:
        """The strip's (x, p) on the screen, as the flat hoop lies."""
        return np.array([self.AT[0] + self.K * (x - A / 2), self.AT[1] + self.K * (p - (B + H)), 0.0])

    def construct(self):
        self.chapter_card("סעיף ב", "כל הפריסות ברצועה אחת",
                          "סעיף ב : פונקציה לכל תיבה ולכל שתי נקודות.\nבלי לטפל בכל פריסה בנפרד.")
        self.thumbs()
        self.hoop()
        self.images()
        self.lines()
        self.box()

    # -- the 16 unfoldings as thumbnails, and the idea in three steps ---------------------------

    TH_CELL = (1.97, 1.5)         # a thumbnail's cell in the grid
    TH_K = 0.0306                 # one scale for all of them, so their lengths compare

    def thumb(self, c: dict) -> VGroup:
        """One unfolding of the page's table, flat: the side faces it crosses, the two end walls
        folded onto their edges, and the straight line from S to F, drawn around ORIGIN."""
        P = q0030.period()
        es, ef, k = c["s_edge"], c["f_edge"], c["k"]
        sx, sp_ = next((x, p) for e, x, p in S_IMG if e == es)
        fx, fp = next((x, p) for e, x, p in F_IMG if e == ef)
        fp += k * P
        slo, shi = RANGES[es]
        flo, fhi = RANGES[ef][0] + k * P, RANGES[ef][1] + k * P
        j0, j1 = int(min(slo, flo) // B), int(max(shi, fhi) // B)
        parts = [(q0030.band_of(B * j), 0, A, B * j, B * j + B) for j in range(j0, j1)]
        assert {n for n, *_ in parts} == set(c["faces"][1:-1])
        parts += [("end0", -H, 0, slo, shi), ("enda", A, A + H, flo, fhi)]
        mid = (B * j0 + B * j1) / 2

        def at(x, p):
            return np.array([self.TH_K * (x - A / 2), self.TH_K * (p - mid), 0.0])

        rects = VGroup(*[Polygon(at(x0, lo), at(x1, lo), at(x1, hi), at(x0, hi), stroke_color=FACE_COL[n],
                                 stroke_width=1.5, fill_color=FACE_COL[n], fill_opacity=0.35)
                         for n, x0, x1, lo, hi in parts])
        best = c["length"] == 40
        line = Line(at(sx, sp_), at(fx, fp), stroke_color=PATH if best else C.WHITE, stroke_width=3.5 if best else 2.5)
        assert abs(math.dist((sx, sp_), (fx, fp)) - c["length"]) < 1e-9
        dots = VGroup(Dot(at(sx, sp_), radius=0.045, color=S_COL), Dot(at(fx, fp), radius=0.045, color=F_COL))
        return VGroup(rects, line, dots)

    def thumbs(self):
        cw, ch = self.TH_CELL
        cells = VGroup()
        for i, c in enumerate(ORDERS):
            r, col = divmod(i, 4)
            cx, cy = -6.9 + cw * (col + 0.5), 3.72 - ch * (r + 0.5)
            pic = self.thumb(c).move_to([cx, cy + 0.17, 0])
            lab = M(f"{round(c['length'], 2):g}", 28, C.AMBER if c["length"] == 40 else C.WHITE).move_to([cx, cy - 0.6, 0])
            cells.add(VGroup(pic, lab))
        self.say("כל סדר של פאות, מקיר לקיר, הוא פריסה אחת.\nהנה כל 16 הפריסות שבעמוד.",
                 LaggedStart(*[FadeIn(x, scale=0.8) for x in cells[:8]], lag_ratio=0.4), run_time=3.2)
        self.say("כל אחת עם הקו הישר שלה ועם האורך שלו,\nמהקצרה לארוכה.",
                 LaggedStart(*[FadeIn(x, scale=0.8) for x in cells[8:]], lag_ratio=0.4), run_time=3.2)
        marks = VGroup(*[SurroundingRectangle(cells[i], color=C.AMBER, buff=0.04, corner_radius=0.08)
                         for i, c in enumerate(ORDERS) if c["length"] == 40])
        self.say("הקצרות ביותר, 40, מסומנות : המסלול שלנו\nותמונת הראי שלו.", Create(marks))
        self.say("הארוכה ביותר, 57.27, עוברת דרך הרצפה,\nקיר צדדי והתקרה.",
                 Indicate(cells[-1], color=C.WHITE, scale_factor=1.12))
        steps = []
        for i, text in enumerate(["כל סדר פאות – פריסה אחת", "קו ישר, בתוך הפאות", "לוקחים את הקצר ביותר"], 1):
            num = chip(M(str(i), 30, C.AMBER), color=C.AMBER)
            row = Group(he(text, 30, C.WHITE, 500), num).arrange(RIGHT, buff=0.3)
            steps.append(row)
        col = Group(*steps).arrange(DOWN, aligned_edge=RIGHT, buff=0.55)
        col.move_to([4.3, 1.0, 0]).align_to([6.8, 0, 0], RIGHT)
        self.say("הרעיון בשלושה שלבים. שלב 1 : עוברים\nעל כל סדרי הפאות, ופורסים כל אחד למישור.",
                 FadeIn(steps[0], shift=0.2 * LEFT))
        self.say("שלב 2 : בכל פריסה מותחים קו ישר מ-S ל-F,\nובודקים שהוא נשאר בתוך הפאות.",
                 FadeIn(steps[1], shift=0.2 * LEFT))
        self.say("שלב 3 : לוקחים את הקצר\nמבין הקווים החוקיים. כאן 40.", FadeIn(steps[2], shift=0.2 * LEFT))
        self.say("אבל 16 פריסות שונות הן 16 מקרים בקוד.\nהטריק : כולן הן קווים ברצועה אחת.")
        self.fade_all()

    def hoop(self):
        room = Room(HOOP, center=(A / 2, B / 2, H / 2))
        room.s_dot.set_opacity(0)
        room.s_lab.set_opacity(0)
        room.f_dot.set_opacity(0)
        room.f_lab.set_opacity(0)
        self.play(FadeIn(room.faces_mob), run_time=0.8)
        with self.beat("ארבע הפאות הצדדיות עוטפות את התיבה\nכמו חישוק. פורסים אותן לרצועה אחת."):
            self.play(room.ghost.animate.set_value(0.0), run_time=0.6)
            # the strip's centre (x = 15, p = 24) is the room's (15, 12, 12) in the far wall's frame
            self.play(room.s.animate.set_value(0.0), room.theta.animate.set_value(0), room.phi.animate.set_value(0),
                      room.scale_t.animate.set_value(self.K), room.cy.animate.set_value(B),
                      room.cz.animate.set_value(H), room.ax.animate.set_value(self.AT[0]),
                      room.ay.animate.set_value(self.AT[1]), run_time=3.2, rate_func=smooth)
        stop(room)
        bands = VGroup()
        for name, (lo, hi) in RANGES.items():
            r = Polygon(self.sp(0, lo), self.sp(A, lo), self.sp(A, hi), self.sp(0, hi), stroke_color=FACE_COL[name],
                        stroke_width=2.5, fill_color=FACE_COL[name], fill_opacity=FACE_OPACITY)
            lab = M(name, 28, C.WHITE).move_to(self.sp(A / 2, (lo + hi) / 2))
            bands.add(VGroup(r, lab))
        ticks = VGroup()
        for p in (0, 12, 24, 36, 48):
            ticks.add(M(f"p = {p}" if p in (0, 48) else str(p), 28, C.MUTED).next_to(self.sp(A + 12, p), RIGHT, buff=0.55))
        self.add(bands)
        self.remove(room.faces_mob)
        self.say("קואורדינטה p עוברת סביב ההיקף : רצפה,\nקיר רחוק, תקרה וקיר קרוב. המחזור 48.",
                 FadeIn(ticks, lag_ratio=0.1))
        self.bands, self.ticks = bands, ticks

    def wall(self, x0: float, x1: float, lo: float, hi: float, color: str) -> Polygon:
        return Polygon(self.sp(x0, lo), self.sp(x1, lo), self.sp(x1, hi), self.sp(x0, hi), stroke_color=color,
                       stroke_width=1.5, stroke_opacity=0.8, fill_color=color, fill_opacity=0.22)

    def images(self):
        s_walls, s_dots, f_walls, f_dots = VGroup(), VGroup(), VGroup(), VGroup()
        for e, x, p in S_IMG:
            lo, hi = RANGES[e]
            s_walls.add(self.wall(-H if e in ("bottom", "top") else -B, 0, lo, hi, FACE_COL["end0"]))
            s_dots.add(Dot(self.sp(x, p), radius=0.1, color=S_COL, stroke_color=C.WHITE, stroke_width=2))
        for e, x, p in F_IMG:
            lo, hi = RANGES[e]
            f_walls.add(self.wall(A, A + (H if e in ("bottom", "top") else B), lo, hi, FACE_COL["enda"]))
            f_dots.add(Dot(self.sp(x, p), radius=0.1, color=F_COL, stroke_color=C.WHITE, stroke_width=2))
        self.say("הקיר של העכביש מתקפל על הרצועה סביב\nאחת מארבע הצלעות שלו : ארבע דמויות ל-S.",
                 FadeIn(s_walls, lag_ratio=0.2), FadeIn(s_dots, lag_ratio=0.2), run_time=1.8)
        top_s = M("(-1, 30)", 28, S_COL).next_to(s_dots[2], LEFT, buff=0.15)
        self.say("כל דמות במרחק של S מהצלע, משמאל ל-x = 0.\nדרך התקרה, למשל : ‏x = −1 ו-p = 30.", FadeIn(top_s))
        self.say("ובאותו אופן ארבע דמויות ל-F,\nמימין ל-x = 30.",
                 FadeIn(f_walls, lag_ratio=0.2), FadeIn(f_dots, lag_ratio=0.2), run_time=1.8)
        n = TX(r"4 \cdot 4 \cdot 3 = 48", size=44).move_to([4.6, -1.75, 0])
        arrows = VGroup(*[Arrow(self.sp(x, p), self.sp(x, p) + UP * 0.55 * sgn, buff=0.1, stroke_width=3,
                                max_tip_length_to_length_ratio=0.35, color=F_COL)
                          for _, x, p in F_IMG[1:3] for sgn in (1, -1)])
        self.say("כל דמות של F גם מחזור אחד למעלה או למטה :\nבסך הכול ‏4 · 4 · 3 = 48 קווים.",
                 FadeIn(arrows), FadeIn(n), run_time=1.2)
        self.play(FadeOut(arrows), FadeOut(top_s), run_time=0.5)
        self.s_dots, self.f_dots, self.count = s_dots, f_dots, n

    def lines(self):
        x_s = Line(self.sp(0, 0), self.sp(0, 48), stroke_color=C.WHITE, stroke_width=2)
        x_f = Line(self.sp(A, 0), self.sp(A, 48), stroke_color=C.WHITE, stroke_width=2)
        lo, hi = RANGES["side0"]
        exit_edge = Line(self.sp(0, lo), self.sp(0, hi), stroke_color=MARK, stroke_width=7)
        bad = Line(self.sp(-6, 37), self.sp(36, 13), stroke_color=C.RED, stroke_width=4)
        hit = Dot(self.sp(0, float(BAD["p_exit"])), radius=0.09, color=C.RED)
        self.say("לכל קו שתי בדיקות : הוא חוצה את x = 0\nבתוך הצלע שהעכביש התקפל סביבה,",
                 Create(x_s), Create(x_f), Create(exit_edge), Create(bad), run_time=1.6)
        self.say("ואת x = 30 בתוך הצלע של הזבוב.\nהקו האדום יוצא ב-p = 33.57, מחוץ לצלע : נפסל.",
                 FadeIn(hit, scale=1.8))
        self.play(FadeOut(bad), FadeOut(hit), FadeOut(exit_edge), run_time=0.5)
        valid0 = VGroup()
        for c in VALID:
            if c["k"] != 0:
                continue
            sx = next(x for e, x, _ in S_IMG if e == c["s_edge"])
            sp_ = next(p for e, _, p in S_IMG if e == c["s_edge"])
            fx = next(x for e, x, _ in F_IMG if e == c["f_edge"])
            fp = next(p for e, _, p in F_IMG if e == c["f_edge"])
            valid0.add(Line(self.sp(sx, sp_), self.sp(fx, fp), stroke_color=C.GREEN, stroke_width=2.5,
                            stroke_opacity=0.75))
        self.say("מתוך 48 הקווים, 22 חוקיים.\nאלה מהם שבתוך הרצועה, בלי הזזה.",
                 Create(valid0, lag_ratio=0.1), run_time=2.0)
        best = Line(self.sp(-1, 30), self.sp(31, 6), stroke_color=PATH, stroke_width=6)
        e_lo, e_hi = RANGES["top"]
        s_edge = Line(self.sp(0, e_lo), self.sp(0, e_hi), stroke_color=MARK, stroke_width=7)
        f_lo, f_hi = RANGES["bottom"]
        f_edge = Line(self.sp(A, f_lo), self.sp(A, f_hi), stroke_color=MARK, stroke_width=7)
        self.say("הקצר שבהם : מ-S דרך התקרה אל F דרך הרצפה.\n‏Δx = 32, ‏Δp = −24, האורך 40.",
                 valid0.animate.set_stroke(opacity=0.25), Create(best), FadeIn(s_edge), FadeIn(f_edge),
                 run_time=1.6)
        ex = Dot(self.sp(0, 29.25), radius=0.09, color=MARK)
        eq = TX(r"p_{\text{exit}} = 29.25", r"(0,\ 6.75,\ 12)", size=40)
        eq.arrange(DOWN, buff=0.3).move_to([4.6, 1.6, 0])
        self.say("נקודת היציאה : ‏p = 29.25, בתוך צלע התקרה,\nכלומר הנקודה ‏(0, 6.75, 12), כמו בסעיף א.",
                 FadeIn(ex, scale=1.8), FadeIn(eq))
        cost = cost_chips(("time", "$O(1)$"), ("lines", "48")).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        cost.scale(0.85).move_to([4.9, -0.85, 0])
        self.say("כל הפריסות הן קווים ברצועה אחת : ‏48 קווים,\nשורש ושתי השוואות לכל אחד, בלי מקרים.",
                 FadeOut(self.count), FadeIn(cost))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "strip", height=5.9).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד : הרצועה,\nשמונה הדמויות והקווים החוקיים.", FadeIn(view))
        self.box_beat(view, [
            (1, "בבחירה \"כל 48\" רואים גם את הקווים\nשנפסלו בשתי הבדיקות."),
            (2, "וב\"קצר בלבד\" נשאר המסלול של 40.\nאפשר לגרור את S ואת F ולשנות את המידות."),
            (3, "כשהעכביש יורד לחצי הגובה, z = 6, מנצח\nהמסלול הישר דרך הרצפה : ‏6 + 30 + 1 = 37."),
            (4, "ובנקודה ‏(0, 2, 11), קרוב לקיר הקרוב,\nהקצר עובר דרך ארבע פאות : 37.12."),
        ])
        self.fade_all()


class Closing(SpiderScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"\sqrt{32^2 + 24^2} = 40 \ \text{(not } 42)", size=38)),
                           ("ב", TX(r"4 \cdot 4 \cdot 3 = 48 \ \text{lines, the shortest valid}", size=34))],
                     ["לסיכום : פורסים את הפאות, והמסלול הקצר\nהוא קו ישר דרך חמש פאות, באורך 40.",
                      "גררו את העכביש ואת הזבוב בתיבה\nשבעמוד של שאלה 0030 באתר."],
                     holds=(4.0, 4.5))
