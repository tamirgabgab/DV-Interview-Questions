"""The tutorial video of question 0071, the three-wizard duel (script: script.md).

Render with `python videos/render.py 0071` (see notes/VIDEOS.md). The question has no code, so
each part is a proof step by step, as in 0015, 0029 and 0026: one line of the argument at
a time, in LaTeX, under its caption. Every number is recomputed here with exact fractions
against the page's own reference, tools/figures/q0071.py (imported), and asserted.

Part א (I am first against 0.6 and 0.8, only my wand p1 varies): the duel formula
V(x, y) = x / (x + y - xy), the backward induction (wizard 3 must shoot, wizard 2, me),
the weak and the strong option, my chance per wand drawn as a chart, the maximum just under
0.6 (513/805), and the game as a Markov chain drawn in Manim with the chances flowing into
the end states (6/35, 64/575, the cats 2/25); then the page's box (wand 0.599, 0.8, 1).
Part ב (I choose my turn and the order): the six orders filled row by row, the winner
(third behind 0.6 then 0.8, 13101/20125) stage by stage, its chain, why it wins, and the
box's best-choice button. Part ג (any rivals a < b): the two plans (a first-turn sniper,
1 - a; hiding third behind a then b just under a), the hide plan's chance as a sum over
the chain's paths, V substituted to the explicit expression in a and b, the others'
chances, the threshold a* and the box with rivals 0.4 and 0.8, then 0.7 and 0.9.
"""

import sys
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(ROOT / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, T, X  # noqa: E402
import q0071 as ref  # noqa: E402

QID = 71
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – אני ראשון"),
    ("ChapterB", "סעיף ב – אני בוחר גם את התור"),
    ("ChapterC", "סעיף ג – המקרה הכללי"),
    ("Closing", "סיכום"),
]

# The page's wizards box (box 0: me first, rivals 0.6 then 0.8, wand 0.599).
# "a": the wand slider down to the box's chain (the orders table and the chart hidden):
#      as the page opens it, wand 0.8, wand 1, then "just under the weak rival".
# "b": the best-choice button, the chances and the orders table with the chart.
# "bchain": the chain after "best choice" (third behind 0.6 then 0.8).
# "c": the rivals' sliders: 0.4 and 0.8, best choice; 0.7 and 0.9, best choice.
BOXES = {
    "a": {"box": 0, "region": [".ex-summary", ".wz-out", ".wz-chain"],
          "hide": [".wz-duo", ".wz-explain", ".viz-legend"],
          "steps": [[], [["set", ".wz-wand", "0.8"]], [["set", ".wz-wand", "1"]],
                    [["click", ".wz-weak"]]]},
    "b": {"box": 0, "region": [".wz-best", ".ex-summary", ".wz-out", ".wz-duo"],
          "steps": [[], [["click", ".wz-best"]]]},
    "bchain": {"box": 0, "region": [".wz-out", ".wz-chain"], "hide": [".wz-duo", ".wz-explain", ".viz-legend"],
               "steps": [[["click", ".wz-best"]]]},
    "c": {"box": 0, "region": [".ex-controls", ".ex-summary", ".wz-out", ".wz-duo"],
          "steps": [[["set", ".wz-r1", "0.4"]], [["click", ".wz-best"]],
                    [["set", ".wz-r1", "0.7"], ["set", ".wz-r2", "0.9"]], [["click", ".wz-best"]]]},
}

# ---- the numbers, from the page's reference --------------------------------------------

EPS = ref.EPS
RIV = ref.RIVALS                                   # (0.6, 0.8)
P_A = ref.place(1, Fr(6, 10) - EPS, RIV)           # part a: me first, just under 0.6
P_B = ref.place(3, Fr(6, 10) - EPS, RIV)           # part b: me third behind 0.6 then 0.8
F = ref.F


def close(x, y, tol=Fr(1, 10**12)):
    return abs(Fr(x) - Fr(y)) < tol


assert F(Fr(6, 10), Fr(8, 10)) == Fr(15, 23) and F(Fr(8, 10), Fr(6, 10)) == Fr(20, 23)
assert F(Fr(6, 10), Fr(6, 10)) == Fr(5, 7)
# part a: the limit just under 0.6 and the others' chances
wa, ca = ref.round_options(P_A)[0], ref.outcomes(P_A)[1]
assert close(wa[0], Fr(513, 805)) and close(wa[1], Fr(6, 35)) and close(wa[2], Fr(64, 575))
assert ca == Fr(2, 25) and Fr(3, 7) + Fr(24, 115) == Fr(513, 805)
assert Fr(513, 805) + Fr(6, 35) + Fr(64, 575) + Fr(2, 25) == 1
assert ref.win(1, Fr(1), RIV) == Fr(2, 5)          # the sniper
TRACE_A = {w: b for w, _, b in ref.round_options(P_A)[1]}
assert TRACE_A == {3: 2, 2: 3, 1: "air"}
# wizard 3 shoots at me exactly when p1 > 0.6; wizard 2 airs above 0.6
assert {w: b for w, _, b in ref.round_options(ref.place(1, Fr(7, 10), RIV))[1]} == {3: 1, 2: "air", 1: 3}
# part b: the six orders (each best just under 0.6) and the winner
ORDERS = []
for me in (1, 2, 3):
    for rv in ((Fr(6, 10), Fr(8, 10)), (Fr(8, 10), Fr(6, 10))):
        p = ref.place(me, Fr(6, 10) - EPS, rv)
        ch, cats = ref.round_options(p)[0], ref.outcomes(p)[1]
        ORDERS.append((me, rv, ch, cats))
assert [round(float(o[2][o[0] - 1]) * 100, 1) for o in ORDERS] == [63.7, 60.7, 63.7, 60.7, 65.1, 55.6]
wb, cb = ref.round_options(P_B)[0], ref.outcomes(P_B)[1]
assert close(wb[2], Fr(13101, 20125)) and close(wb[0], Fr(36, 175)) and close(wb[1], Fr(64, 575))
assert cb == Fr(4, 125) * (1 + 0) or close(cb, Fr(4, 125))
assert Fr(3, 7) + Fr(24, 115) + Fr(48, 1000) * Fr(2, 7) == Fr(13101, 20125)
assert {w: b for w, _, b in ref.round_options(P_B)[1]} == {3: 2, 2: 1, 1: 2}
# wizard 1 in part b: a hit beats the air while p3 < 5/6
for q in (Fr(1, 2), Fr(8, 10)):
    hit = Fr(6, 10) * (1 - q) / (Fr(6, 10) + Fr(4, 10) * q)
    air = Fr(2, 10) * q * Fr(6, 10) / (Fr(6, 10) + Fr(4, 10) * q)
    assert (hit > air) == (q < Fr(5, 6))
# part c: the closed form, the sniper, the threshold and the box's examples
assert ref.hide_closed(Fr(6, 10), Fr(8, 10)) == (Fr(13101, 20125), Fr(36, 175), Fr(64, 575), Fr(4, 125))
for a, b in ((Fr(4, 10), Fr(8, 10)), (Fr(7, 10), Fr(9, 10)), (Fr(3, 10), Fr(5, 10))):
    assert ref.hide_closed(a, b) == ref.hide_third(a, b) and sum(ref.hide_closed(a, b)) == 1
H48 = ref.hide_closed(Fr(4, 10), Fr(8, 10))[0]
H79 = ref.hide_closed(Fr(7, 10), Fr(9, 10))[0]
assert round(float(H48) * 100, 1) == 48.6 and round(float(H79) * 100, 1) == 73.8
A_STAR = [(b, ref.threshold(b)) for b in ref.THRESHOLD_BS] + [(None, ref.threshold(None))]
assert [round(t, 3) for _, t in A_STAR] == [0.476, 0.469, 0.464, 0.461, 0.458, 0.456, 0.478]


def pct(v) -> str:
    return f"{float(v) * 100:.1f}%"


# ---- the Markov chain --------------------------------------------------------------------

SX, X0 = 0.0300, 239          # the page's chain coordinates (480 x 340) to the frame
YS = {40: 3.0, 176: 0.55, 300: -1.72}
NODE_W = {"top": 2.3, "mid": 2.12, "bot": 2.5}


def cp(key):
    x, y = ref.POS[key]
    return np.array([(x - X0) * SX, YS[y], 0.0])


def short(v) -> str:
    v = Fr(v)
    if v != 1 and ((v + EPS) * 10).denominator == 1 and (v * 10).denominator != 1:
        return f"{float(v + EPS):g}⁻"
    return f"{float(v):g}"


class Chain(VGroup):
    """The duel as a Markov chain: the first round on top (everyone alive, whose turn), the
    duels in the middle (who is left, whose turn), the wins and the cats at the bottom. The
    edges are the best choices of p (in turn order); the end states hold their chances."""

    def __init__(self, p, me):
        super().__init__()
        self.p, self.me = p, me
        st = ref.chain_states(p)
        choice = {w: b for w, _, b in ref.round_options(p)[1]}
        self.nodes, self.edges, self.free = {}, [], []          # edges: (a, b, arrow, label)
        self.orig, self.base = {}, {}
        for key in ref.POS:
            k = ref.skey(key)
            row = "top" if k in ("R1", "R2", "R3", "CATS") else "bot" if k.startswith("W") else "mid"
            if k.startswith("R"):
                lines = ["all alive", f"turn {k[1]}"]
            elif k == "CATS":
                lines = ["cats", pct(st["CATS"]["reach"])]
            elif k.startswith("W"):
                lines = [f"{k[1]} wins", pct(st[k]["reach"])]
            else:
                i, j, s = key
                lines = [f"{i} vs {j}", f"turn {s}"]
            mine = (k.startswith("R") and k[1] == str(me)) or (not k.startswith(("R", "C", "W")) and key[2] == me) \
                or k == f"W{me}"
            color = C.GREEN if k.startswith("W") else C.RED if k == "CATS" else C.MUTED
            box = RoundedRectangle(width=NODE_W[row], height=0.92, corner_radius=0.14,
                                   stroke_color=C.AMBER if mine else color, stroke_width=4 if mine else 2.5,
                                   fill_color=C.NAVY_LIGHT, fill_opacity=1)
            txt = VGroup(*[T(s, 28, C.WHITE) for s in lines]).arrange(DOWN, buff=0.08)
            node = VGroup(box, txt.move_to(box)).move_to(cp(key))
            self.orig[k] = (box.get_stroke_color(), box.get_stroke_width())
            self.base[k] = 1 if st[k]["reach"] else 0.28
            node.set_opacity(self.base[k])
            self.nodes[k] = node
        p_ = [Fr(x) for x in p]
        for w, nxt in ((1, "R2"), (2, "R3"), (3, "CATS")):
            c = choice[w]
            if c != "air":
                d = ref.skey(ref.duel_of(w, c))
                t, sh = ref.LABEL_AT[(w, c)]
                self._edge(f"R{w}", d, short(p_[w - 1]), hit=True, t=t, shift=sh)
            self._edge(f"R{w}", nxt, "air" if c == "air" else short(1 - p_[w - 1]), hit=False)
        for key in [k for k in ref.POS if isinstance(k, tuple)]:
            k = ref.skey(key)
            i, j, s = key
            if not st[k]["reach"]:
                continue
            o = j if s == i else i
            self._edge(k, f"W{s}", short(p_[s - 1]), hit=True)
            self._edge(k, ref.skey((i, j, o)), short(1 - p_[s - 1]), hit=False, arc=(s == i))
        self._place()
        self.arrows = VGroup(*[e[2] for e in self.edges])
        self.labels = VGroup(*[e[3] for e in self.edges])
        self.boxes = VGroup(*self.nodes.values())
        self.add(self.arrows, self.boxes, self.labels)       # the edges behind the states

    def _edge(self, a, b, label, hit, t=0.5, shift=0.0, arc=None):
        na, nb = self.nodes[a], self.nodes[b]
        col = C.WHITE if hit else C.MUTED
        if arc is not None:            # the two directions of a duel: an arc above, one below
            up = 1 if arc else -1
            s = na[0].get_corner(UR if up > 0 else DR) + LEFT * 0.35
            e = nb[0].get_corner(UL if up > 0 else DL) + RIGHT * 0.35
            if not arc:
                s, e = na[0].get_corner(DL) + RIGHT * 0.35, nb[0].get_corner(DR) + LEFT * 0.35
            arrow = CurvedArrow(s, e, angle=-0.9 * up if arc else -0.9, color=col, stroke_width=3,
                                tip_length=0.16)
            mid = arrow.point_from_proportion(0.5) + UP * 0.2 * up
        else:
            s, e = na[0].get_center(), nb[0].get_center()
            if abs(s[1] - e[1]) < 0.1:              # along the top row
                s, e = na[0].get_right(), nb[0].get_left()
            else:
                s, e = na[0].get_bottom(), nb[0].get_top()
            arrow = Arrow(s, e, buff=0.04, color=col, stroke_width=3.5 if hit else 3,
                          max_tip_length_to_length_ratio=0.12, tip_length=0.18)
            mid = s + (e - s) * t + RIGHT * shift * SX
            if abs(s[1] - e[1]) < 0.1:
                mid = (s + e) / 2 + UP * 0.32
        lab = M(label, 28, C.AMBER if hit else C.WHITE)
        bg = BackgroundRectangle(lab, color=C.NAVY, fill_opacity=0.9, buff=0.05)
        g = VGroup(bg, lab).move_to(mid)
        self.edges.append((a, b, arrow, g))
        if arc is None and abs(s[1] - e[1]) >= 0.1:
            self.free.append((g, s, e))

    def _place(self):
        """The labels of the slanted edges, one at a time, where they are farthest from the
        labels already placed and clear of the states (the edges cross, so a fixed share of
        the way puts two labels on top of each other)."""
        free = {id(g) for g, _, _ in self.free}
        placed = [e[3].get_center() for e in self.edges if id(e[3]) not in free]
        rects = [(n[0].get_left()[0] - 0.3, n[0].get_right()[0] + 0.3, n[0].get_bottom()[1] - 0.15,
                  n[0].get_top()[1] + 0.15) for n in self.nodes.values()]
        for g, s, e in self.free:
            best, where = -1.0, None
            for t in np.linspace(0.2, 0.8, 16):
                pt = s + (e - s) * t
                if any(x0 <= pt[0] <= x1 and y0 <= pt[1] <= y1 for x0, x1, y0, y1 in rects):
                    continue
                d = min([np.hypot((pt[0] - q[0]) / 0.9, (pt[1] - q[1]) / 0.45) for q in placed] + [9.0])
                if d > best:
                    best, where = d, pt
            g.move_to(where if where is not None else (s + e) / 2)
            placed.append(g.get_center())

    def around(self, key):
        """The arrows and labels into and out of a state."""
        return [e for e in self.edges if key in (e[0], e[1])]

    def focus(self, key=None):
        """Animations to one look of the chain: with a key, the state framed amber, its
        arrows and neighbours lit and the rest dimmed; without one, everything as built."""
        on = self.around(key) if key else self.edges
        keep = {key} | {e[0] for e in on} | {e[1] for e in on} if key else set(self.nodes)
        anims = []
        for e in self.edges:
            op = 1 if e in on else 0.15
            anims += [e[2].animate.set_opacity(op), e[3].animate.set_opacity(op)]
        for k, n in self.nodes.items():
            op = self.base[k] if k in keep else 0.2
            col, w = (C.AMBER, 6) if k == key else self.orig[k]
            n.generate_target()
            n.target.set_opacity(op)
            n.target[0].set_stroke(col, width=w, opacity=op)
            anims.append(MoveToTarget(n))
        return anims


# ---- smaller pieces ----------------------------------------------------------------------

def wizard(n, label, me=False) -> VGroup:
    ring = Circle(radius=0.55, stroke_color=C.AMBER if me else C.MUTED, stroke_width=5 if me else 3,
                  fill_color=C.NAVY_LIGHT, fill_opacity=1)
    num = M(str(n), 44, C.WHITE).move_to(ring)
    lab = TX(label, size=36, color=C.AMBER if me else C.WHITE).next_to(ring, DOWN, buff=0.25)
    g = VGroup(ring, num, lab)
    if me:
        g.add(T("me", 30, C.AMBER).next_to(ring, UP, buff=0.2))
    return g


def proof(*lines, size=40, buff=0.42) -> VGroup:
    return VGroup(*[TX(s, size=size) for s in lines]).arrange(DOWN, buff=buff, aligned_edge=LEFT)


class Chart(VGroup):
    """My chance against my wand (0..1) at a turn and an order: the page's chart in Manim."""

    def __init__(self, me, rv, w=8.4, h=4.2, ymax=0.7, origin=(-4.2, -1.9)):
        super().__init__()
        self.ox, self.oy, self.w, self.h, self.ymax = origin[0], origin[1], w, h, ymax
        ax = VGroup(Line(self.pt(0, 0), self.pt(1, 0), stroke_color=C.MUTED, stroke_width=3),
                    Line(self.pt(0, 0), self.pt(0, ymax), stroke_color=C.MUTED, stroke_width=3))
        ticks = VGroup()
        for x in (0, 0.2, 0.4, 0.6, 0.8, 1):
            ticks.add(M(f"{x:g}", 28, C.MUTED).next_to(self.pt(x, 0), DOWN, buff=0.15))
        for y in (0.2, 0.4, 0.6):
            ticks.add(M(f"{int(y * 100)}%", 28, C.MUTED).next_to(self.pt(0, y), LEFT, buff=0.15))
            ticks.add(DashedLine(self.pt(0, y), self.pt(1, y), stroke_color=C.FAINT, stroke_width=1.5))
        self.axes = VGroup(ax, ticks, T("wand", 28, C.MUTED).next_to(self.pt(1, 0), RIGHT, buff=0.3))
        lo = [Fr(k, 100) for k in range(1, 60)] + [Fr(6, 10) - EPS]
        hi = [Fr(6, 10) + Fr(1, 10**6)] + [Fr(k, 100) for k in range(61, 101)]
        self.lo = VMobject(stroke_color=C.BLUE, stroke_width=5).set_points_as_corners(
            [self.pt(float(q), float(ref.win(me, q, rv))) for q in lo])
        self.hi = VMobject(stroke_color=C.BLUE, stroke_width=5).set_points_as_corners(
            [self.pt(float(q), float(ref.win(me, q, rv))) for q in hi])
        self.add(self.axes, self.lo, self.hi)

    def pt(self, x, y):
        return np.array([self.ox + self.w * x, self.oy + self.h * y / self.ymax, 0.0])


class Wiz(DVQScene):
    def swap(self, view: BoxView, k: int, run_time: float = 0.6):
        """The box to its picture k with no click marked (the control is outside the region)."""
        new = view._image(k)
        self.play(FadeIn(new), run_time=run_time)
        view.remove(view.image)
        self.remove(view.image)
        view.image = new
        view.submobjects.insert(0, new)
        view.k = k
        self.remove(new)
        self.add(view)

    def chain_in(self, chain: Chain, captions):
        """The chain built row by row under three captions: the top, the duels, the ends."""
        top = [k for k in ("R1", "R2", "R3", "CATS")]
        mid = [k for k in chain.nodes if "," in k]
        bot = ["W1", "W2", "W3"]
        e_top = [e for e in chain.edges if e[0] in top and e[1] in top]
        e_mid = [e for e in chain.edges if (e[0] in top and e[1] in mid) or (e[0] in mid and e[1] in mid)]
        e_bot = [e for e in chain.edges if e[0] in mid and e[1] in bot]
        for keys, edges, cap in ((top, e_top, captions[0]), (mid, e_mid, captions[1]), (bot, e_bot, captions[2])):
            with self.beat(cap):
                nodes = [chain.nodes[k] for k in keys]
                self.play(*[FadeIn(n) for n in nodes], run_time=0.7)
                self.play(*[GrowArrow(e[2]) if isinstance(e[2], Arrow) else Create(e[2]) for e in edges],
                          *[FadeIn(e[3]) for e in edges], run_time=1.0)
        self.clear()
        self.add(chain)


class Opening(Wiz):
    def construct(self):
        self.opening(QID, "סניור", "דו-קרב של שלושה קוסמים",
                     ["א · אני ראשון", "ב · בוחר גם את התור", "ג · המקרה הכללי"],
                     ["שאלה 0071 : דו-קרב של שלושה קוסמים,\nשאלה ברמת סניור.",
                      "שלושה סעיפים : אני ראשון, אני בוחר תור,\nוהמקרה הכללי."])
        self.fade_all()
        ws = VGroup(wizard(1, "p_1"), wizard(2, "p_2"), wizard(3, "p_3")).arrange(RIGHT, buff=2.2).move_to(UP * 1.1)
        turn = VGroup(*[Arrow(ws[i][0].get_right(), ws[i + 1][0].get_left(), buff=0.15, color=C.MUTED,
                              stroke_width=4) for i in range(2)])
        back = CurvedArrow(ws[2][0].get_top() + UP * 0.1, ws[0][0].get_top() + UP * 0.1, angle=0.7,
                           color=C.MUTED, stroke_width=3)
        self.say("שלושה קוסמים מכשפים בתורות :\nקוסם 1, אחריו 2, אחריו 3, וחוזר חלילה.",
                 FadeIn(ws, lag_ratio=0.2), GrowArrow(turn[0]), GrowArrow(turn[1]), Create(back), run_time=1.6)
        zap = Arrow(ws[0][0].get_bottom() + DOWN * 0.9, ws[2][0].get_bottom() + DOWN * 0.9, buff=0,
                    color=C.AMBER, stroke_width=5)
        lab = TX(r"\text{hit with } p_1", size=34, color=C.AMBER).next_to(zap, DOWN, buff=0.2)
        self.say("בתור שלו כל קוסם מכשף על יריב אחד,\nופוגע בהסתברות שלו. מותר גם באוויר.",
                 GrowArrow(zap), FadeIn(lab))
        self.play(FadeOut(zap), FadeOut(lab), run_time=0.5)
        cats = T("all alive after round 1  →  all become cats", 32, C.RED).move_to(DOWN * 1.6)
        self.say("חוק החתולים : אם אחרי הסבב הראשון\nכולם חיים, כולם הופכים לחתולים ומפסידים.",
                 FadeIn(cats, shift=0.2 * UP))
        self.play(FadeOut(cats), run_time=0.5)
        wand = T("my wand: chosen in advance, seen by all", 32, C.AMBER).move_to(DOWN * 1.6)
        self.say("השרביט : אני בוחר מראש את ההסתברות שלי,\nוכולם רואים אותה. כולם משחקים הכי טוב.",
                 FadeIn(wand, shift=0.2 * UP))
        self.fade_all()


class ChapterA(Wiz):
    def construct(self):
        self.chapter_card("סעיף א", "אני ראשון", "סעיף א : אני מכשף ראשון,\nמול קוסמים של 0.6 ו-0.8.")
        self.setup_a()
        self.duel()
        self.induction()
        self.maximum()
        self.chain_a()
        self.box_a()

    def setup_a(self):
        ws = VGroup(wizard(1, "p_1", me=True), wizard(2, "0.6"), wizard(3, "0.8")).arrange(RIGHT, buff=2.4)
        ws.move_to(UP * 1.0)
        self.say("קוסם 2 פוגע ב-0.6 וקוסם 3 ב-0.8.\nהמשתנה היחיד הוא השרביט שלי, p₁.", FadeIn(ws, lag_ratio=0.2))
        steps = T("duel   →   wizard 3   →   wizard 2   →   me", 32, C.AMBER).move_to(DOWN * 1.4)
        self.say("הרעיון : פותרים מהסוף להתחלה. קודם\nהדו-קרב, אחר כך קוסם 3, קוסם 2, ואני.",
                 FadeIn(steps, shift=0.2 * UP))
        self.fade_all()

    def duel(self):
        eq = proof(r"V = x + (1-x)(1-y)\,V", r"V(x,y) = \frac{x}{x+y-xy}", size=46).move_to(UP * 1.3)
        self.say("שלב 1 : כשנשארים שניים, יורים לסירוגין.\nמי שפותח פוגע מיד, או ששניהם מחטיאים,",
                 FadeIn(eq[0]))
        self.say("וחוזרים לאותו מצב. פותרים, ומקבלים\nאת הסיכוי של הפותח לנצח, V(x,y).",
                 FadeIn(eq[1], shift=0.2 * DOWN))
        tab = proof(r"V(0.6,\,0.8) = \tfrac{15}{23} \approx 0.652",
                    r"V(0.8,\,0.6) = \tfrac{20}{23} \approx 0.870", size=40).move_to(DOWN * 1.15)
        self.say("קוסם 2 פותח מול קוסם 3 ומנצח ב-65% :\nהירייה הראשונה שווה הרבה.", FadeIn(tab))
        self.say("ומי שפגע בסבב הראשון הוא השני בדו-קרב,\nכי התור עובר למי שנשאר.")
        self.fade_all()

    def induction(self):
        w3 = proof(r"\text{on me: } 0.8\cdot\tfrac{8}{23}",
                   r"\text{on 2: } 0.8\cdot\frac{0.8\,(1-p_1)}{0.8+0.2\,p_1}",
                   r"\frac{0.8\,(1-p_1)}{0.8+0.2\,p_1} < \frac{8}{23} \iff 18.4 - 18.4\,p_1 < 6.4 + 1.6\,p_1",
                   r"\text{on me} \iff p_1 > 0.6", size=40).move_to(UP * 0.7)
        self.say("שלב 2 : קוסם 3 חייב לכשף,\nאחרת כולם חתולים. על מי?", FadeIn(w3[0]), FadeIn(w3[1]))
        self.say("אם הוא פוגע בי, הוא שני מול קוסם 2.\nאם בקוסם 2, הוא שני מולי.")
        self.say("משווים את שני הסיכויים, וכופלים\nבמכנים. נשאר אי-שוויון פשוט ב-p₁.", FadeIn(w3[2]))
        self.say("הוא מכשף עליי בדיוק כש-p₁ > 0.6,\nכלומר על החזק מביני ומבין קוסם 2.",
                 FadeIn(w3[3]), w3[3].animate.set_color(C.AMBER))
        self.play(FadeOut(w3), run_time=0.5)
        w2 = proof(r"p_1 < 0.6:\ \text{air} = 0 \ \Rightarrow\ \text{on 3}",
                   r"p_1 > 0.6:\ \text{air} = 0.8\cdot\tfrac{15}{23} > \text{hit 3}", size=40).move_to(UP * 0.6)
        self.say("שלב 3 : קוסם 2. כש-p₁ < 0.6 קוסם 3 יכשף\nעליו, ולכן באוויר הוא מפסיד : מכשף על 3.",
                 FadeIn(w2[0]))
        self.say("כש-p₁ > 0.6, באוויר קוסם 3 מכשף עליי,\nוקוסם 2 פותח אחר כך מולו : ‏12/23.",
                 FadeIn(w2[1]))
        w2c = TX(r"\frac{0.6\,(1-p_1)}{0.6+0.4\,p_1} > \frac{12}{23} \iff p_1 < 0.355", size=40,
                 color=C.MUTED).next_to(w2, DOWN, buff=0.5)
        self.say("כדי שפגיעה בקוסם 3 תשתלם לו, צריך\n‏p₁ < 0.355. זה סותר, ולכן הוא באוויר.",
                 FadeIn(w2c))
        self.play(FadeOut(w2), FadeOut(w2c), run_time=0.5)
        weak = proof(r"p_1 < 0.6:", r"W(p_1) = 0.6\,V(p_1, 0.6) + 0.32\,V(p_1, 0.8)", size=40)
        strong = proof(r"p_1 > 0.6:", r"P(p_1) = \frac{0.4\,p_1^2}{0.6+0.4\,p_1} \le 0.4", size=40)
        VGroup(weak, strong).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(UP * 0.6)
        h = proof(r"H_3 = \frac{0.4\,p_1}{0.6+0.4\,p_1} \;>\; H_2 = \frac{0.2\,p_1}{0.8+0.2\,p_1}", size=40).move_to(UP * 0.6)
        self.say("שלב 4 : אני. אם אכשף, אכשף על קוסם 3,\nהחזק. אבל האם כדאי לי לכשף בכלל?", FadeIn(h))
        self.play(FadeOut(h), run_time=0.5)
        self.say("אם p₁ < 0.6, אף אחד לא מכשף עליי.\nאני מכשף באוויר, ופותח מול מי שנשאר.",
                 FadeIn(weak))
        self.say("קוסם 2 פוגע ב-3 בהסתברות 0.6. אחרת קוסם 3\nפוגע ב-2, בהסתברות 0.4 כפול 0.8.",
                 Indicate(weak[1], color=C.AMBER))
        self.say("אם p₁ > 0.6, קוסם 3 מכשף עליי. אני חייב\nלפגוע מיד, ומקבל לכל היותר 0.4.", FadeIn(strong))
        self.fade_all()

    def maximum(self):
        ch = Chart(1, RIV)
        best = Dot(ch.pt(0.6, float(Fr(513, 805))), radius=0.12, color=C.AMBER)
        snip = Dot(ch.pt(1, 0.4), radius=0.1, color=C.WHITE)
        with self.beat("הסיכוי שלי לפי השרביט : עולה עד ממש\nלפני 0.6, וצונח כשאני עובר את קוסם 2."):
            self.play(FadeIn(ch.axes), run_time=0.6)
            self.play(Create(ch.lo), run_time=1.6, rate_func=linear)
            self.play(Create(ch.hi), run_time=1.0, rate_func=linear)
        val = TX(r"W(0.6^-) = \tfrac{3}{7} + \tfrac{24}{115} = \tfrac{513}{805} \approx 0.637", size=40,
                 color=C.AMBER).move_to(UP * 3.0)
        self.say("ב-0.6 מלמטה : ‏513/805, כמעט 64%.\nצלף, שרביט 1, מקבל רק 40%.", FadeIn(best, scale=1.6),
                 FadeIn(snip), FadeIn(val))
        self.say("למה לא 0.6 בדיוק? שם קוסם 3 אדיש,\nועלול לבחור בי. לכן קצת מתחת, למשל 0.59.")
        self.fade_all()
        head = VGroup(*[T(h, 30, C.MUTED) for h in ("wand", "I do", "my chance")])
        xs = [-3.2, 0.0, 3.2]
        for h, x in zip(head, xs):
            h.move_to([x, 2.6, 0])
        rows = VGroup()
        for r, q in enumerate(ref.WANDS):
            p = ref.place(1, q, RIV)
            act = "air" if {w: b for w, _, b in ref.round_options(p)[1]}[1] == "air" else "at 3"
            v = ref.win(1, q, RIV)
            cells = [short(q), act, f"{float(v):.3f}"]
            best = q == Fr(6, 10) - EPS
            rows.add(VGroup(*[M(c, 30, C.AMBER if best else C.WHITE).move_to([x, 1.95 - 0.55 * r, 0])
                              for c, x in zip(cells, xs)]))
        self.say("הטבלה מהעמוד : עד 0.6 אני באוויר,\nומעליו אני חייב לכשף על קוסם 3.",
                 FadeIn(head), FadeIn(rows[:4], lag_ratio=0.2), run_time=1.6)
        self.say("מעל 0.6 הסיכוי קופץ למטה, ל-0.223,\nועולה רק עד 0.4 בצלף.", FadeIn(rows[4:], lag_ratio=0.2))
        self.fade_all()
        rule = VGroup(T("wizard 2: at 3          wizard 3: at 2", 34, C.WHITE),
                      T("kill the stronger, face the weaker at the end", 34, C.AMBER)).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        self.say("העיקרון אצל שניהם : לחסל את החזק,\nכדי להישאר בסוף מול החלש, מולי.", FadeIn(rule, lag_ratio=0.3))
        self.fade_all()

    def chain_a(self):
        chain = Chain(P_A, 1)
        title = T("the game as a Markov chain", 40, C.AMBER).move_to(UP * 0.4)
        sub = T("a state: who is alive, and whose turn it is", 32, C.MUTED).next_to(title, DOWN, buff=0.4)
        self.say("עכשיו כל המשחק כשרשרת מרקוב :\nכל מצב הוא מי חי, ומי מכשף עכשיו.", FadeIn(title), FadeIn(sub))
        self.play(FadeOut(title), FadeOut(sub), run_time=0.5)
        self.chain_in(chain, [
            "בשורה העליונה הסבב הראשון : אני באוויר,\nקוסם 2 על 3, ואם החטיא, קוסם 3 על 2.",
            "פגיעה מעבירה לדו-קרב, שבו מכשפים\nלסירוגין עד שמישהו פוגע.",
            "בשורה התחתונה הניצחונות. הסיכוי לכל סוף\nהוא סכום על המסלולים אליו.",
        ])
        self.say("דו-קרב 1 מול 2, תורי : אני פוגע ב-0.6,\nאחרת קוסם 2 מכשף, ואם החטיא, שוב אני.",
                 *chain.focus("1,2,1"))
        self.say("זו הלולאה של V : מהמצב הזה\nאני מנצח ב-5/7.")
        self.say("ודו-קרב 1 מול 3, תורי : מגיעים אליו\nב-0.32, ואני מנצח בו ב-15/23.",
                 *chain.focus("1,3,1"))
        self.say("כל מסלול הוא מכפלת ההסתברויות\nשעל החצים שלו.", *chain.focus("CATS"))
        self.say("חתולים : שניהם מחטיאים,\n‏0.4 כפול 0.2, כלומר 8%.")
        self.say("אני : ‏0.6 כפול 5/7, ועוד 0.32 כפול 15/23.\nבסך הכול 63.7%.",
                 *chain.focus("W1"))
        self.say("קוסם 2 : פוגע ב-3 ומנצח כשני מולי,\n‏0.6 כפול 2/7, כ-17.1%.", *chain.focus("W2"))
        self.say("קוסם 3 : ‏0.32 כפול 8/23, כ-11.1%.\nהחזק מכולם מקבל הכי מעט.", *chain.focus("W3"))
        self.say("הבדיקה : ‏63.7 ועוד 17.1, 11.1 ו-8,\nבדיוק 100%.", *chain.focus())
        self.fade_all()

    def box_a(self):
        view = BoxView(QID, "a", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד : אני ראשון עם 0.599,\nושרשרת מרקוב של הבחירה.", FadeIn(view))
        for k, cap in [
            (1, "שרביט 0.8 : קוסם 3 מכשף עליי,\nוקוסם 2 מכשף באוויר."),
            (2, "צלף : אני פוגע בקוסם 3 מיד,\nוקוסם 2 פותח מולי. רק 40%."),
            (3, "ובחזרה ממש מתחת ל-0.6 :\nשוב 63.7%."),
        ]:
            with self.beat(cap):
                self.swap(view, k)
        self.fade_all()
        trap = T("trap: the strongest wand is not the best", 36, C.RED).move_to(UP * 0.8)
        nums = TX(r"1 \to 40\% \qquad 0.6^- \to 63.7\%", size=44).move_to(DOWN * 0.4)
        self.say("המלכודת : לחשוב שהשרביט החזק הוא הטוב.\nכאן הוא נותן 40%, מול 63.7% לחלש.",
                 FadeIn(trap), FadeIn(nums))
        self.fade_all()


class ChapterB(Wiz):
    def construct(self):
        self.chapter_card("סעיף ב", "אני בוחר גם את התור",
                          "סעיף ב : עכשיו אני בוחר גם את התור,\nואת הסדר של שני היריבים.")
        self.table()
        self.winner()
        self.chain_b()
        self.box_b()

    def table(self):
        head = ["order", "wand", "me", "0.6", "0.8", "cats"]
        xs = [-4.4, -1.3, 0.6, 2.2, 3.8, 5.4]
        rows = VGroup()
        hr = VGroup(*[T(h, 30, C.MUTED).move_to([x, 2.6, 0]) for h, x in zip(head, xs)])
        for r, (me, rv, ch, cats) in enumerate(ORDERS):
            names = [f"{float(x):g}" for x in rv]
            names.insert(me - 1, "me")
            o6 = [i for i in range(3) if i != me - 1 and ref.place(me, Fr(6, 10) - EPS, rv)[i] == Fr(6, 10)][0]
            o8 = [i for i in range(3) if i != me - 1 and ref.place(me, Fr(6, 10) - EPS, rv)[i] == Fr(8, 10)][0]
            cells = [" → ".join(names), "0.6⁻", pct(ch[me - 1]), pct(ch[o6]), pct(ch[o8]), pct(cats)]
            y = 1.85 - 0.62 * r
            rows.add(VGroup(*[M(c, 28, C.WHITE).move_to([x, y, 0]) for c, x in zip(cells, xs)]))
        self.say("שלושה תורות, ובכל אחד שני סדרים :\nשישה סדרים. כל אחד נפתר כמו סעיף א.", FadeIn(hr))
        self.say("בכל אחד השרביט הטוב יוצא קצת מתחת\nל-0.6 : להיות החלש, שלא יכשפו עליי.",
                 FadeIn(rows[0]), FadeIn(rows[1]))
        self.say("ראשון או שני : ‏63.7% או 60.7%,\nלפי מי מהיריבים מכשף קודם.", FadeIn(rows[2]), FadeIn(rows[3]))
        ring = SurroundingRectangle(rows[4], color=C.AMBER, buff=0.12, corner_radius=0.1)
        self.say("שלישי אחרי 0.6 ואז 0.8 : ‏65.1%, הכי טוב.\nאחרי 0.8 ואז 0.6 רק 55.6%.",
                 FadeIn(rows[4]), FadeIn(rows[5]), Create(ring))
        self.fade_all()

    def winner(self):
        ws = VGroup(wizard(1, "0.6"), wizard(2, "0.8"), wizard(3, "p_3", me=True)).arrange(RIGHT, buff=2.4)
        ws.move_to(UP * 1.6)
        self.say("נפתח את הסדר המנצח. אני קוסם 3, עם p₃.\nקוסם 1 פוגע ב-0.6, וקוסם 2 ב-0.8.",
                 FadeIn(ws, lag_ratio=0.2))
        duels = proof(r"V(p_3, 0.6) = \frac{p_3}{0.6+0.4\,p_3}, \quad V(p_3, 0.8) = \frac{p_3}{0.8+0.2\,p_3}",
                      r"V(0.6, p_3) = \frac{0.6}{0.6+0.4\,p_3}, \quad V(0.8, p_3) = \frac{0.8}{0.8+0.2\,p_3}",
                      size=36).move_to(DOWN * 1.35)
        self.say("הדו-קרבים של הסדר הזה, באותה נוסחה :\nאני פותח, או שהיריב פותח מולי.", FadeIn(duels))
        self.play(FadeOut(duels), run_time=0.5)
        note = T("me (last): must shoot, at 2", 32, C.AMBER).move_to(DOWN * 1.3)
        self.say("אני אחרון בסבב : חייב לכשף, ועל החזק,\nקוסם 2, כדי להישאר מול החלש.", FadeIn(note))
        note2 = T("wizard 2: air = 0, so at the stronger of 1 and me: at 1", 30, C.AMBER).move_to(DOWN * 1.3)
        self.say("קוסם 2 : באוויר אני מחסל אותו. לכן מכשף,\nעל החזק מבין קוסם 1 ואותי : על 1.",
                 ReplacementTransform(note, note2))
        self.fade_all()
        w1 = proof(r"\text{hit 2} = \frac{0.6\,(1-p_3)}{0.6+0.4\,p_3}",
                   r"\text{air} = 0.2\,p_3\cdot\frac{0.6}{0.6+0.4\,p_3}",
                   r"\text{hit} > \text{air} \iff p_3 < \tfrac{5}{6}", size=40).move_to(UP * 0.9)
        self.say("קוסם 1 : פגיעה בקוסם 2 עדיפה על האוויר\nכל עוד p₃ < 5/6. לכן גם הוא מכשף על 2.",
                 FadeIn(w1, lag_ratio=0.3), run_time=1.8)
        self.play(FadeOut(w1), run_time=0.5)
        wsum = proof(r"W(p_3) = 0.6\,V(p_3,0.6) + 0.32\,V(p_3,0.8)",
                     r"\qquad\quad + 0.08\,p_3\,\bigl(1 - V(0.6, p_3)\bigr)",
                     r"W(0.6^-) = \tfrac{3}{7} + \tfrac{24}{115} + 0.048\cdot\tfrac{2}{7}"
                     r" = \tfrac{13101}{20125}", size=38).move_to(UP * 0.8)
        self.say("הסיכוי שלי : שלוש דרכים לדו-קרב.\nהאחרונה, הפגיעה שלי, היא רק גיבוי.",
                 FadeIn(wsum[0]), FadeIn(wsum[1]))
        self.say("בגבול מתחת ל-0.6 : ‏13101/20125,\nכ-65.1%.", FadeIn(wsum[2]), wsum[2].animate.set_color(C.AMBER))
        self.fade_all()

    def chain_b(self):
        chain = Chain(P_B, 3)
        self.chain_in(chain, [
            "השרשרת של הסדר הזה : קוסם 1 על 2,\nאם החטיא קוסם 2 על 1, ואם החטיא אני.",
            "הדו-קרבים : בכולם אני משחק\nמול מי שנשאר.",
            "בסוף : אני 65.1%, קוסם 1 ‏20.6%,\nקוסם 2 ‏11.1%.",
        ])
        self.say("חתולים רק אם שלושתנו מחטיאים :\n‏0.4 כפול 0.2 כפול 0.4, כלומר 3.2%.", *chain.focus("CATS"))
        self.say("וקוסם 1 : פוגע בקוסם 2 ומנצח כשני מולי,\nאו פותח מולי אחרי הפגיעה שלי.",
                 *chain.focus("W1"))
        self.say("ואני : שלוש דרכים לדו-קרב,\nובשתיים הראשונות אני פותח.", *chain.focus("W3"))
        self.say("קוסם 2 : רק אם פגע בקוסם 1, ואז הוא\nשני מולי : ‏0.32 כפול 8/23, כ-11.1%.", *chain.focus("W2"))
        self.play(*chain.focus(), run_time=0.6)
        self.fade_all()
        why = VGroup(T("shoot last: both rivals shoot first, my shot is a backup", 30, C.WHITE),
                     T("the weak rival first: I face 0.6, not 0.8", 30, C.WHITE),
                     TX(r"V(0.6,\,0.6) = \tfrac{5}{7} \;>\; V(0.6,\,0.8) = \tfrac{15}{23}", size=40,
                        color=C.AMBER)).arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        self.say("למה זה מנצח? כשאני אחרון, שני היריבים\nמכשפים לפניי, והחתולים יורדים ל-3.2%.",
                 FadeIn(why[0]))
        self.say("והחלש מכשף ראשון : הוא מכשף על 0.8,\nואני נשאר מול 0.6 ולא מול 0.8.",
                 FadeIn(why[1]), FadeIn(why[2]))
        self.fade_all()

    def box_b(self):
        view = BoxView(QID, "b", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה, הכפתור הבחירה הטובה ביותר\nעובר על ששת הסדרים.", FadeIn(view))
        self.box_beat(view, [
            (1, "הוא בוחר שלישי, אחרי 0.6 ואז 0.8,\nממש מתחת ל-0.6 : ‏65.1%."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        view = BoxView(QID, "bchain", height=5.6).move_to(UP * 0.62)
        self.say("ושרשרת מרקוב של הבחירה הזו,\nעם אותם מספרים.", FadeIn(view))
        self.fade_all()


class ChapterC(Wiz):
    def construct(self):
        self.chapter_card("סעיף ג", "המקרה הכללי", "סעיף ג : יריבים כלשהם, a < b.\nמה הבחירה הכי טובה?")
        self.plans()
        self.closed()
        self.rule()
        self.box_c()

    def plans(self):
        rule = T("everyone shoots at the stronger of the other two", 32, C.WHITE).move_to(UP * 2.0)
        self.say("מה שראינו : כל קוסם מכשף על החזק\nמבין שני האחרים. על החלש מכולם לא מכשפים.", FadeIn(rule))
        a = VGroup(T("sniper first", 34, C.AMBER), TX(r"\text{wand } 1,\ \text{kill } b:\ \ 1-a", size=40))
        b = VGroup(T("hide third", 34, C.AMBER), TX(r"a,\ b,\ \text{me};\ \text{wand } a^-", size=40))
        for g in (a, b):
            g.arrange(DOWN, buff=0.3)
        VGroup(a, b).arrange(RIGHT, buff=2.0).move_to(DOWN * 0.2)
        self.say("לכן יש שתי תוכניות : להסתתר כחלש,\nאו להיות צלף ולהרוג את החזק ראשון.", FadeIn(a), FadeIn(b))
        self.say("צלף ראשון : שרביט 1, ואני הורג את b מיד.\nהיריב a פותח מולי, ומנצח רק אם פגע.",
                 Indicate(a, color=C.AMBER))
        self.say("להסתתר : שלישי, אחרי a ואז b,\nעם שרביט קצת מתחת ל-a, כמו בסעיף ב.", Indicate(b, color=C.AMBER))
        self.say("צלף בתור שני או שלישי לא מקבל יותר :\nמי שמכשף לפניו רואה בו את החזק.")
        self.fade_all()
        dec = proof(r"\text{me (last): at } b",
                    r"b:\ \text{air} = 0 \Rightarrow \text{at } a",
                    r"a:\ \text{hit } b \to \tfrac{1-a}{2-a} \;>\; \text{air} \to \tfrac{(1-b)\,a}{2-a}",
                    size=40).move_to(UP * 0.6)
        self.say("בתוכנית ההסתרה, כמו בסעיף ב : אני\nאחרון ומכשף על b, ו-b מכשף על a.", FadeIn(dec[0]), FadeIn(dec[1]))
        self.say("ו-a מכשף על b, כי 1 − a גדול תמיד\nמ-(1 − b)a.", FadeIn(dec[2]))
        self.fade_all()

    def closed(self):
        paths = proof(r"P_{\text{me}} = a\,V(a,a) + (1-a)\,b\,V(a,b)",
                      r"\qquad\quad + (1-a)(1-b)\,a\,\bigl(1 - V(a,a)\bigr)", size=40).move_to(UP * 2.1)
        self.say("הסיכוי שלי : סכום על שלושת המסלולים\nשל השרשרת, כמו בסעיף ב.", FadeIn(paths))
        subs = VGroup(TX(r"V(a,a) = \frac{a}{2a-a^2} = \frac{1}{2-a}", size=42, color=C.MUTED),
                      TX(r"V(a,b) = \frac{a}{a+b-ab}", size=42, color=C.MUTED)).arrange(RIGHT, buff=1.0).move_to(UP * 0.55)
        self.say("מציבים את V משלב 1. מול יריב שווה לי :\nהשבר מצטמצם ל-1/(2 − a).", FadeIn(subs[0]))
        self.say("ומול b : ‏a חלקי a + b − ab.\nכאן אין מה לצמצם.", FadeIn(subs[1]))
        final = TX(r"P_{\text{me}} = \frac{a\,\bigl(1 + (1-a)^2(1-b)\bigr)}{2-a} + \frac{a\,b\,(1-a)}{a+b-ab}",
                   size=44, color=C.AMBER).move_to(DOWN * 1.0)
        self.say("וזה הביטוי הכללי של הסיכוי שלי,\nב-a וב-b בלבד.", FadeIn(final, shift=0.2 * UP))
        self.play(FadeOut(paths), FadeOut(subs), final.animate.move_to(UP * 2.4), run_time=0.8)
        others = proof(r"P_a = \frac{a\,(1-a)(2-b)}{2-a}", r"P_b = \frac{(1-a)^2\,b^2}{a+b-ab}",
                       r"P_{\text{cats}} = (1-a)^2\,(1-b)", size=40, buff=0.35).move_to(DOWN * 0.15)
        self.say("ובאותה דרך, הסיכויים של שני היריבים\nושל החתולים.", FadeIn(others, lag_ratio=0.3))
        self.say("החתולים : שלושתנו מחטיאים, כי השרביט\nשלי קרוב ל-a : ‏(1 − a)² כפול (1 − b).",
                 Indicate(others[2], color=C.AMBER))
        self.play(FadeOut(others), run_time=0.5)
        check = TX(r"a = 0.6,\ b = 0.8:\quad P_{\text{me}} = \tfrac{13101}{20125} \approx 0.651", size=42,
                   color=C.GREEN).move_to(UP * 0.4)
        self.say("בדיקה : a = 0.6 ו-b = 0.8 נותנים\n‏13101/20125, בדיוק התשובה של סעיף ב.", FadeIn(check))
        self.say("אלה גבולות : שרביט קצת מתחת ל-a\nמתקרב אליהם כמה שרוצים.")
        self.fade_all()

    def rule(self):
        cond = TX(r"P_{\text{me}}(a,b) > 1 - a", size=48, color=C.AMBER).move_to(UP * 2.3)
        self.say("מסתתרים כשהביטוי הזה גדול מ-1 − a,\nהסיכוי של הצלף.", FadeIn(cond))
        cols = VGroup()
        for b, t in A_STAR:
            bl = "a" if b is None else f"{float(b):g}"
            cols.add(VGroup(M(bl, 30, C.MUTED), M(f"{t:.3f}", 30, C.WHITE)).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=0.55)
        heads = VGroup(T("b", 30, C.MUTED), T("a*", 30, C.AMBER)).arrange(DOWN, buff=0.35)
        tab = VGroup(heads, cols).arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        first = TX(r"\frac{a}{2-a} > 1 - a \iff a > 2 - \sqrt{2} \approx 0.586", size=40, color=C.MUTED).move_to(UP * 0.9)
        self.say("האיבר הראשון לבדו עובר את 1 − a\nכש-a > 2 − √2, כ-0.586.", FadeIn(first))
        self.play(FadeOut(first), run_time=0.5)
        self.say("עם שני האיברים האחרים, הסף a* נמוך יותר,\nותלוי מעט ב-b : בין 0.456 ל-0.478.", FadeIn(tab, lag_ratio=0.1))
        verdict = VGroup(TX(r"a < a^*:\ \text{sniper first}", size=40),
                         TX(r"a > a^*:\ \text{hide third}", size=40)).arrange(DOWN, buff=0.35).move_to(DOWN * 1.35)
        self.say("מתחת לסף, צלף ראשון. מעליו, להסתתר.\nבסעיף ב, a = 0.6, ולכן מסתתרים.", FadeIn(verdict))
        self.fade_all()
        head = ["rivals", "hide", "sniper", "choice"]
        xs = [-4.2, -1.2, 1.4, 4.2]
        hr = VGroup(*[T(h, 30, C.MUTED).move_to([x, 2.4, 0]) for h, x in zip(head, xs)])
        rows = VGroup()
        for r, (a, b) in enumerate(ref.EXAMPLES):
            hide, snip = ref.hide_closed(a, b)[0], 1 - a
            cells = [f"{float(a):g} / {float(b):g}", pct(hide), pct(snip), "hide third" if hide > snip else "sniper"]
            row = VGroup(*[M(c, 30, C.AMBER if (k == 1 and hide > snip) or (k == 2 and snip >= hide) else C.WHITE)
                           .move_to([x, 1.6 - 0.62 * r, 0]) for k, (c, x) in enumerate(zip(cells, xs))])
            rows.add(row)
        self.say("הכלל על כמה זוגות יריבים : בכל שורה\nהסיכוי בכל תוכנית, והבחירה.", FadeIn(hr), FadeIn(rows[0]))
        self.say("‏0.4 ו-0.8 מתחת לסף : צלף, 60%.\n‏0.47 ו-0.9 כבר מעליו : להסתתר.", FadeIn(rows[1]), FadeIn(rows[2]))
        self.say("‏0.47 ו-0.55 : הסף עולה כש-b קטן,\nוצלף מנצח בקושי. ו-0.7 ו-0.9 : ‏73.8%.", FadeIn(rows[3]), FadeIn(rows[4]))
        self.fade_all()

    def box_c(self):
        view = BoxView(QID, "c", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה : יריבים 0.4 ו-0.8,\nמתחת לסף.", FadeIn(view))
        self.box_beat(view, [
            (1, "הבחירה הטובה : צלף ראשון, 60%,\nמול 48.6% אם מסתתרים."),
            (2, "ועכשיו יריבים 0.7 ו-0.9,\nמעל הסף."),
            (3, "הבחירה : שלישי, ממש מתחת ל-0.7,\nעם 73.8%."),
        ])
        self.fade_all()


class Closing(Wiz):
    def construct(self):
        self.closing(QID, [("א", TX(r"\text{first: wand } 0.6^-,\ \tfrac{513}{805} \approx 63.7\%", size=40)),
                           ("ב", TX(r"\text{third after } 0.6, 0.8:\ \tfrac{13101}{20125} \approx 65.1\%", size=40)),
                           ("ג", TX(r"\text{hide third if } P_{\text{me}} > 1-a,\ \text{else sniper}", size=40))],
                     ["לסיכום : להיות החלש, לכשף אחרון,\nולתת לחזקים להילחם ביניהם.",
                      "נסו יריבים משלכם בתיבה\nשבעמוד של שאלה 0071 באתר."],
                     holds=(4.0, 4.5))
