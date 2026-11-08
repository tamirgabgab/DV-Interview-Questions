"""The tutorial video of question 0040, the 1011 sequence detector with overlap (script: script.md).

Render with `python videos/render.py 0040` (see notes/VIDEOS.md). The answer is hardware, so the
code beat types the page's SystemVerilog module (the owner, 2026-11-01: SV in both videos
of the round, the 0011 exception) and walks it beside the page's box (`walk_code`, no line
trace for SV). Part א: the state as "how much of the pattern was seen", the Mealy diagram
drawn edge by edge, the stream 1011011 stepped on it, the box played bit by bit, the
module typed then walked, the timing diagram built cycle by cycle (the owner: each rising
edge adds a cycle, the state register shows what it remembers) until it is the page's
WaveDrom diagram, the cost and the trap of going back to S0 on a mismatch. Part ב: the
construction on 10101 (the pattern slid under the input to the longest prefix, the
formula with fail, the table row by row), the page's next_state shown, the box building
10101, then Mealy against Moore on 1011011 (one more state, the output a cycle later).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, cost_chips, page_code)  # noqa: E402

QID = 40
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – התבנית 1011"),
    ("ChapterB", "סעיף ב – כל תבנית : הבנייה השיטתית, ‏Mealy מול Moore"),
    ("Closing", "סיכום"),
]

# The page's part b box (data-kind="seqdet", the second on the page after part a's seqhw). "stream": the pattern 1011 (Mealy) fed 1011011 by
# the bit buttons, picture k after k bits; the graph and the strip of din / state / found.
# "build": the pattern 10101 typed, then 1, 0, 1 (state S3, the build of both edges
# shown), 0 (S4) and 1 (a match: found, back to S3). "mm": 1011011 by the example
# button, Mealy, then the machine switched to Moore.
BOXES = {
    "stream": {"box": 1, "width": 520,
               "region": [".sq-bits", ".sq-sum", ".sq-graph", ".sq-strip"],
               "hide": [".ex-play-row > :not(.sq-bits)", ".sq-next", ".sq-slide",
                        ".sq-build-toggle", ".viz-legend", ".ex-reset", ".ex-keys", ".wv-export"],
               "steps": [[], [["click", ".sq-bit[data-b='1']"]], [["click", ".sq-bit[data-b='0']"]],
                         [["click", ".sq-bit[data-b='1']"]], [["click", ".sq-bit[data-b='1']"]],
                         [["click", ".sq-bit[data-b='0']"]], [["click", ".sq-bit[data-b='1']"]],
                         [["click", ".sq-bit[data-b='1']"]]]},
    "build": {"box": 1,
              "region": [".sq-pat", ".sq-bits", ".sq-sum", ".sq-graph", ".sq-slide"],
              "hide": [".ex-controls:not(.ex-play-row) > :not(label:has(.sq-pat))",
                       ".ex-play-row > :not(.sq-bits)", ".sq-next", ".sq-build-toggle", ".viz-legend",
                       ".ex-keys", ".wv-export"],
              "steps": [[["fill", ".sq-pat", "10101"]],
                        [["click", ".sq-bit[data-b='1']"], ["click", ".sq-bit[data-b='0']"],
                         ["click", ".sq-bit[data-b='1']"]],
                        [["click", ".sq-bit[data-b='0']"]],
                        [["click", ".sq-bit[data-b='1']"]]]},
    "mm": {"box": 1,
           "region": [".sq-kind", ".sq-sum", ".sq-graph", ".sq-strip"],
           "hide": [".ex-controls:not(.ex-play-row) > :not(label:has(.sq-kind))",
                    ".ex-play-row", ".sq-next", ".sq-slide", ".sq-build-toggle", ".viz-legend",
                    ".ex-keys", ".wv-export"],
           "steps": [[["click", ".ex-preset[data-s='1011011']"]],
                     [["set", ".sq-kind", "moore"]]]},
}

STREAM = [1, 0, 1, 1, 0, 1, 1]
SV = page_code(QID, "systemverilog", "module seq_detect_1011")
SV_ANY = page_code(QID, "systemverilog", "module seq_detect #(")


def kmp(pattern: list[int]) -> tuple[list[list[int]], list[int]]:
    """nxt[s][b] of the page's construction, and fail(s) for s = 1..L (index s)."""
    L = len(pattern)
    nxt = [[0, 0] for _ in range(L + 1)]
    nxt[0][pattern[0]] = 1
    fail, fails = 0, [None, 0]
    for s in range(1, L + 1):
        for b in (0, 1):
            nxt[s][b] = s + 1 if s < L and pattern[s] == b else nxt[fail][b]
        if s < L:
            fail = nxt[fail][pattern[s]]
            fails.append(fail)
    return nxt, fails


def mealy(pattern, bits):
    """The states before each bit and the outputs (Mealy: the full state folds back)."""
    nxt, fails = kmp(pattern)
    L = len(pattern)
    rest = next(s for s in range(L) if nxt[s] == nxt[L])
    s, states, out = 0, [], []
    for b in bits:
        states.append(s)
        n = nxt[s][b]
        out.append(int(n == L))
        s = n if n < L else rest
    return states, out, s


NXT_1011, _ = kmp([1, 0, 1, 1])
assert NXT_1011 == [[0, 1], [2, 1], [0, 3], [2, 4], [2, 1]], NXT_1011
assert mealy([1, 0, 1, 1], STREAM)[:2] == ([0, 1, 2, 3, 1, 2, 3], [0, 0, 0, 1, 0, 0, 1])
NXT_5, FAIL_5 = kmp([1, 0, 1, 0, 1])
assert NXT_5 == [[0, 1], [2, 1], [0, 3], [4, 1], [0, 5], [4, 1]], NXT_5
assert FAIL_5 == [None, 0, 0, 1, 2, 3], FAIL_5


# --------------------------------------------------------------------------------------
# Pictures
# --------------------------------------------------------------------------------------

def bit_cell(v, side=0.62, size=34, color=None, fill=None) -> VGroup:
    box = RoundedRectangle(width=side, height=side, corner_radius=0.1, stroke_color=C.MUTED,
                           stroke_width=2.5, fill_color=fill or C.NAVY_LIGHT, fill_opacity=1)
    return VGroup(box, M(str(v), size, color or C.WHITE).move_to(box))


def bit_row(bits, side=0.62, gap=0.1, size=34) -> VGroup:
    return VGroup(*[bit_cell(b, side, size) for b in bits]).arrange(RIGHT, buff=gap)


class FSM(VGroup):
    """A detector's state diagram as on the page's box: the states in a row, the forward
    edges straight, the self loops above, the edges back as arcs below, a label per edge
    ("1", or "1 / 1" on the Mealy edge that detects). Edges are drawn behind the nodes."""

    def __init__(self, n: int, meanings: list[str], y: float = 0.9, pitch: float = 3.0,
                 r: float = 0.5, out_state: int | None = None):
        super().__init__()
        self.r, self.y = r, y
        self.xs = [(k - (n - 1) / 2) * pitch for k in range(n)]
        self.nodes = VGroup()
        for k in range(n):
            ring = Circle(radius=r, stroke_color=C.WHITE, stroke_width=3,
                          fill_color=C.NAVY_DARK, fill_opacity=1)
            g = VGroup(ring, M(f"S{k}", 30)).move_to([self.xs[k], y, 0])
            if out_state == k:
                g.add(Circle(radius=r - 0.08, stroke_color=C.ORANGE, stroke_width=3).move_to(g))
            g.set_z_index(2)
            self.nodes.add(g)
        self.meanings = VGroup(*[M(m, 26, C.MUTED).move_to([self.xs[k], y - 2.5, 0])
                                 for k, m in enumerate(meanings)])
        self.edges = {}
        self.add(self.nodes, self.meanings)

    def edge(self, s: int, t: int, label: str, found: bool = False, depth: float = 1.0) -> VGroup:
        color = C.ORANGE if found else C.BLUE
        a, b = self.nodes[s][0], self.nodes[t][0]
        if t == s + 1:
            arrow = Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=4, color=color,
                          max_tip_length_to_length_ratio=0.12, tip_length=0.22)
            lab = M(label, 28, color).next_to(arrow, UP, buff=0.1)
        elif t == s:
            top = a.get_top()
            arrow = CurvedArrow(top + LEFT * 0.3 + DOWN * 0.05, top + RIGHT * 0.3 + DOWN * 0.05,
                                angle=-1.6 * PI, color=color, stroke_width=4, tip_length=0.2)
            lab = M(label, 28, color).next_to(arrow, UP, buff=0.08)
        else:
            arrow = CurvedArrow(a.get_bottom() + LEFT * 0.12, b.get_bottom() + RIGHT * 0.12,
                                angle=-depth, color=color, stroke_width=4, tip_length=0.22)
            lab = M(label, 28, color).next_to(arrow, DOWN, buff=0.06)
            lab.move_to([lab.get_x(), arrow.get_bottom()[1] - 0.22, 0])
        g = VGroup(arrow, lab)
        g.set_z_index(1)
        self.edges[(s, t)] = g
        return g

    def ring(self, k: int) -> Circle:
        return Circle(radius=self.r + 0.12, stroke_color=C.AMBER, stroke_width=7).move_to(self.nodes[k])


def detector_1011(y=0.45) -> FSM:
    fsm = FSM(4, ["start", "1", "10", "101"], y=y)
    fsm.edge(0, 1, "1"), fsm.edge(1, 2, "0"), fsm.edge(2, 3, "1")
    fsm.edge(0, 0, "0"), fsm.edge(1, 1, "1")
    fsm.edge(2, 0, "0", depth=0.8)
    fsm.edge(3, 2, "0", depth=1.2)
    fsm.edge(3, 1, "1 / 1", found=True, depth=1.45)
    return fsm


class Wave(VGroup):
    """A timing diagram built a cycle at a time: clk, din, state, found, as the page's
    WaveDrom diagram (cycle 0 is after the reset, din unknown)."""

    LANES = ["clk", "din", "state", "found"]

    def __init__(self, din, states, found, x0=-5.0, width=1.32, top=1.55, gap=1.0, h=0.55):
        super().__init__()
        self.din, self.states, self.found = din, states, found
        self.x0, self.w, self.h = x0, width, h
        self.ys = {name: top - k * gap for k, name in enumerate(self.LANES)}
        self.labels = VGroup(*[M(n, 28, C.MUTED).move_to([x0 - 0.85, self.ys[n], 0]) for n in self.LANES])
        self.ticks = VGroup()
        self.add(self.labels)

    def level(self, lane, v):
        return self.ys[lane] + (self.h / 2 if v else -self.h / 2)

    def cycle(self, k: int) -> VGroup:
        """The pieces of cycle k (with the transitions into it)."""
        x, w = self.x0 + k * self.w, self.w
        g = VGroup()
        hi, lo = self.level("clk", 1), self.level("clk", 0)
        g.add(VMobject(stroke_color=C.WHITE, stroke_width=3).set_points_as_corners(
            [[x, lo, 0], [x, hi, 0], [x + w / 2, hi, 0], [x + w / 2, lo, 0], [x + w, lo, 0]]))
        g.add(M(str(k), 24, C.MUTED).move_to([x + w / 2, self.ys["clk"] + 0.62, 0]))
        d = self.din[k]
        if d is None:
            box = Rectangle(width=w, height=self.h, stroke_width=0, fill_color=C.FAINT,
                            fill_opacity=0.5).move_to([x + w / 2, self.ys["din"], 0])
            g.add(box)
        else:
            prev = self.din[k - 1] if k else None
            y = self.level("din", d)
            pts = []
            if prev is not None and prev != d:
                pts.append([x, self.level("din", prev), 0])
            pts += [[x, y, 0], [x + w, y, 0]]
            g.add(VMobject(stroke_color=C.BLUE, stroke_width=4).set_points_as_corners(pts))
        sy = self.ys["state"]
        bus = Polygon([x + 0.08, sy, 0], [x + 0.2, sy + self.h / 2, 0], [x + w - 0.2, sy + self.h / 2, 0],
                      [x + w - 0.08, sy, 0], [x + w - 0.2, sy - self.h / 2, 0], [x + 0.2, sy - self.h / 2, 0],
                      stroke_color=C.WHITE, stroke_width=2.5, fill_color=C.NAVY_LIGHT, fill_opacity=1)
        g.add(bus, M(self.states[k], 24).move_to([x + w / 2, sy, 0]))
        f, prev = self.found[k], self.found[k - 1] if k else 0
        y = self.level("found", f)
        pts = ([[x, self.level("found", prev), 0]] if prev != f else []) + [[x, y, 0], [x + w, y, 0]]
        g.add(VMobject(stroke_color=C.ORANGE, stroke_width=4).set_points_as_corners(pts))
        return g


class Register(VGroup):
    """The two flip-flops of the state: a box with the state's name and its two bits."""

    CODE = {"S0": "00", "S1": "01", "S10": "10", "S101": "11"}

    def __init__(self, state="S0"):
        super().__init__()
        self.box = RoundedRectangle(width=3.4, height=0.95, corner_radius=0.14, stroke_color=C.AMBER,
                                    stroke_width=3, fill_color=C.NAVY_DARK, fill_opacity=1)
        self.tag = M("state", 26, C.MUTED).next_to(self.box, LEFT, buff=0.25)
        self.val = self.text(state)
        self.add(self.box, self.tag, self.val)

    def text(self, state):
        return M(f"{state} = {self.CODE[state]}", 32, C.AMBER).move_to(self.box)

    def set(self, state):
        return Transform(self.val, self.text(state))


def grid(rows: list[list[str]], col_w: float = 0.95, row_h: float = 0.62, size: float = 28,
         first_w: float = 1.8, colors=None) -> VGroup:
    """A small table of monospace texts: the first column the row's name."""
    out = VGroup()
    for i, row in enumerate(rows):
        line = VGroup()
        for j, txt in enumerate(row):
            x = 0 if j == 0 else first_w + (j - 0.5) * col_w
            col = (colors or {}).get((i, j), C.MUTED if j == 0 else C.WHITE)
            t = M(txt, size, col)
            if j == 0:
                t.move_to([x, -i * row_h, 0], aligned_edge=LEFT)
            else:
                t.move_to([x, -i * row_h, 0])
            line.add(t)
        out.add(line)
    return out


# --------------------------------------------------------------------------------------
# The scenes
# --------------------------------------------------------------------------------------


class Opening(DVQScene):
    def construct(self):
        self.opening(QID, "סטודנט", "גלאי רצף 1011 עם חפיפה",
                     ["א · התבנית 1011", "ב · כל תבנית"],
                     ["שאלה 0040 : גלאי רצף 1011 עם חפיפה,\nשאלה ברמת סטודנט.",
                      "שני סעיפים : קודם התבנית 1011,\nואז בנייה שיטתית לכל תבנית."])
        self.fade_all()
        row = bit_row(STREAM, side=0.8, size=40).move_to(UP * 0.9)
        din = M("din", 30, C.MUTED).next_to(row, LEFT, buff=0.45)
        nums = VGroup(*[M(str(k + 1), 24, C.MUTED).next_to(c, UP, buff=0.18) for k, c in enumerate(row)])
        self.say("בכל מחזור שעון מגיע ביט אחד, din.\nהמעגל מוציא found = 1 כשארבעת האחרונים 1011.",
                 FadeIn(din), FadeIn(row, lag_ratio=0.15), FadeIn(nums), run_time=1.6)
        w1 = SurroundingRectangle(row[0:4], color=C.AMBER, buff=0.1, corner_radius=0.12, stroke_width=5)
        w2 = SurroundingRectangle(row[3:7], color=C.ORANGE, buff=0.18, corner_radius=0.14, stroke_width=5)
        f1 = M("found", 30, C.AMBER).next_to(row[3], DOWN, buff=0.45)
        f2 = M("found", 30, C.ORANGE).next_to(row[6], DOWN, buff=0.45)
        with self.beat("בזרם 1011011 המוצא עולה פעמיים :\nבמחזור 4 ובמחזור 7."):
            self.play(Create(w1), FadeIn(f1, shift=0.2 * UP), run_time=1.0)
            self.play(Create(w2), FadeIn(f2, shift=0.2 * UP), run_time=1.0)
        self.say("זו החפיפה : ה-1 האחרון של הזיהוי הראשון\nהוא ה-1 הראשון של השני.",
                 Indicate(row[3], color=C.AMBER, scale_factor=1.25), run_time=1.2)
        self.fade_all()


class ChapterA(DVQScene):
    def construct(self):
        self.chapter_card("סעיף א", "התבנית 1011",
                          "סעיף א : מכונת מצבים שמזהה את 1011,\nכולל חפיפה.")

        # The idea and the diagram, edge by edge.
        fsm = detector_1011()
        e = fsm.edges
        self.say("הרעיון : המצב זוכר כמה מהתבנית כבר ראינו,\nולא רק את הביט האחרון.",
                 FadeIn(fsm.nodes, lag_ratio=0.2), run_time=1.4)
        self.say("לפני שהתבנית נגמרת יש ארבע אפשרויות :\nכלום, 1, 10 ו-101. לכן ארבעה מצבים.",
                 FadeIn(fsm.meanings, lag_ratio=0.2))
        self.say("מתקדמים כשהביט מתאים :\nמ-S0 עם 1, מ-S1 עם 0, ומ-S2 עם 1.",
                 *[Create(e[k]) for k in [(0, 1), (1, 2), (2, 3)]], lag_ratio=0.4, run_time=1.6)
        self.say("‏S0 עם 0 נשאר במקום, וגם S1 עם 1 :\n‏11 מסתיים ב-1, שעדיין פותח את התבנית.",
                 Create(e[(0, 0)]), Create(e[(1, 1)]))
        self.say("‏S2 עם 0 : הקלט 100. שום סיומת שלו\nלא פותחת את התבנית, ולכן חוזרים ל-S0.",
                 Create(e[(2, 0)]))
        self.say("‏S3 עם 0 : הקלט 1010, שמסתיים ב-10.\nלכן לא חוזרים להתחלה, אלא ל-S2.",
                 Create(e[(3, 2)]))
        self.say("‏S3 עם 1 : זיהוי. הפלט 1 על המעבר,\nוממשיכים ל-S1, כי 1011 מסתיים ב-1.",
                 Create(e[(3, 1)]))
        self.say("זו מכונת Mealy : הפלט תלוי במצב ובביט,\nולכן found עולה באותו מחזור.",
                 Indicate(e[(3, 1)][1], color=C.ORANGE, scale_factor=1.3))

        # The stream on the diagram.
        row = bit_row(STREAM, side=0.55, size=30).move_to([0.6, 3.3, 0])
        lab = M("din", 26, C.MUTED).next_to(row, LEFT, buff=0.3)
        ring = fsm.ring(0)
        ptr = SurroundingRectangle(row[0], color=C.AMBER, buff=0.05, corner_radius=0.08, stroke_width=5)
        marks = VGroup()

        def feed(k: int, state_before: int, state_after: int, out: int):
            edge = e[(state_before, state_after)][0]
            moves = [ptr.animate.move_to(row[k])] if k else []
            self.play(*moves, Indicate(row[k], color=C.AMBER, scale_factor=1.15), run_time=0.45)
            self.play(edge.animate.set_color(C.AMBER), run_time=0.3)
            anims = [ring.animate.move_to(fsm.nodes[state_after])]
            if out:
                m = M("1", 30, C.ORANGE, weight="BOLD").next_to(row[k], DOWN, buff=0.12)
                marks.add(m)
                anims.append(FadeIn(m, scale=1.6))
            self.play(*anims, run_time=0.6)
            self.play(edge.animate.set_color(C.ORANGE if (state_before, state_after) == (3, 1) else C.BLUE),
                      run_time=0.25)

        self.say("נריץ את 1011011. מתחילים ב-S0.",
                 FadeIn(lab), FadeIn(row, lag_ratio=0.1), Create(ring), Create(ptr))
        with self.beat("‏1, 0, 1 : שלושה מעברים קדימה,\nוהמכונה ב-S3."):
            feed(0, 0, 1, 0)
            feed(1, 1, 2, 0)
            feed(2, 2, 3, 0)
        with self.beat("הביט הרביעי 1 : הפלט 1 במחזור 4,\nוהמכונה עוברת ל-S1."):
            feed(3, 3, 1, 1)
        with self.beat("‏0 ואחריו 1 מחזירים אותה ל-S3,\nבזכות ה-1 שנשאר מהזיהוי."):
            feed(4, 1, 2, 0)
            feed(5, 2, 3, 0)
        with self.beat("וה-1 האחרון מזהה שוב, במחזור 7 :\nשני זיהויים, כמו שצריך."):
            feed(6, 3, 1, 1)
        self.fade_all()

        # The page's box, alone.
        view = BoxView(QID, "stream", height=5.9).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד : הגרף,\nורצועת תזמון שגדלה ביט אחרי ביט.", FadeIn(view))
        with self.beat("לוחצים 1, 0, 1 : המצב הנוכחי מודגש,\nוהרצועה מראה din, state ו-found."):
            for k in (1, 2, 3):
                self.box_step(view, k)
        self.box_beat(view, [(4, "עוד 1 : המעבר 1 / 1 נלקח,\nו-found עולה במחזור 4.")])
        with self.beat("‏0 ו-1 מחזירים את המכונה ל-S3."):
            for k in (5, 6):
                self.box_step(view, k)
        self.box_beat(view, [(7, "וה-1 האחרון : זיהוי שני, במחזור 7.")])
        self.fade_all()

        # The module, typed.
        panel = CodePanel(SV, font_size=30, drop_comments=True, language="systemverilog", rows=14)
        self.place_code(panel)
        self.type_code(panel, [
            ([1, 2, 3, 4, 5, 6], "המודול : שעון, איפוס שפעיל ב-0,\nביט הקלט din והמוצא found."),
            ([7, 8], ["ארבעה מצבים, בשמות של מה שכבר נראה.\nשני ביטים מספיקים לארבעה.",
                      "בקוד S10 הוא S2 מהגרף,\nו-S101 הוא S3."]),
            ([10, 11, 12], "לוגיקה צירופית. ברירת המחדל :\nהמצב לא משתנה, והמוצא 0."),
            ([13, 14, 15, 16], "‏case על המצב : המעברים של S0,\nשל S1 ושל S10, לפי din."),
            ([17, 18, 19], ["ב-S101 : found = din. זה ה-Mealy,\nהפלט תלוי גם בביט שנכנס.",
                            "ואחר כך : עם 1 ל-S1, בשביל החפיפה,\nועם 0 ל-S10."]),
            ([21, 22, 23, 24], "הפלופים : באיפוס חוזרים ל-S0,\nובכל עליית שעון state מקבל את next."),
        ], intro="עכשיו נכתוב את המודול ב-SystemVerilog.")

        # Walked beside the box.
        view = BoxView(QID, "stream")
        with self.beat("נעבור על הקוד לצד התיבה,\nעל אותו זרם 1011011."):
            self.split(panel, view)
        self.walk_code(panel, view, [
            ([22], "אחרי האיפוס המצב S0, ועוד לא הגיע ביט.", None),
            ([14], "מחזור 1, din = 1 : ב-S0 השורה הזו\nבוחרת next = S1.", 1),
            ([15], "מחזור 2, din = 0 : מ-S1 ל-S10.", 2),
            ([16], "מחזור 3, din = 1 : מ-S10 ל-S101.", 3),
            ([17], "מחזור 4, din = 1 : ב-S101 found = din,\nכלומר 1. והמצב הבא S1.", 4),
            ([23], "בעליית השעון state מקבל את next :\nהמכונה ב-S1, מוכנה לחפיפה.", None),
            ([15, 16], "מחזורים 5 ו-6 : ‏0 ואחריו 1,\nושוב מגיעים ל-S101.", 6),
            ([17], "מחזור 7 : שוב found = 1,\nבאותו מחזור שבו ה-1 על הקו.", 7),
        ])
        self.fade_all()

        # The timing diagram, cycle by cycle.
        din = [None] + STREAM
        names = ["S0", "S1", "S10", "S101"]
        states = ["S0"] + [names[s] for s in mealy([1, 0, 1, 1], STREAM)[0]]
        found = [0] + mealy([1, 0, 1, 1], STREAM)[1]
        assert states == ["S0", "S0", "S1", "S10", "S101", "S1", "S10", "S101"], states
        assert found == [0, 0, 0, 0, 1, 0, 0, 1], found
        wave = Wave(din, states, found, x0=-4.6, width=1.3, top=1.3, gap=1.05)
        reg = Register("S0").move_to([0.9, 3.05, 0])
        cycles = [wave.cycle(k) for k in range(8)]
        after = states[1:] + ["S1"]          # what the flip-flops hold after each cycle's edge

        def add(k):
            self.play(FadeIn(cycles[k], shift=0.1 * RIGHT), run_time=0.6)
            self.play(reg.set(after[k]), Indicate(reg.box, color=C.AMBER, scale_factor=1.05), run_time=0.6)

        with self.beat("נבנה את דיאגרמת התזמון, מחזור אחרי מחזור.\nבמחזור 0, אחרי האיפוס, המצב S0."):
            self.play(FadeIn(wave.labels), FadeIn(reg), run_time=0.8)
            self.play(FadeIn(cycles[0], shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("בכל עליית שעון הפלופים שומרים את next.\nאחרי 1, 0, 1 הם מחזיקים S101."):
            for k in (1, 2, 3):
                add(k)
        with self.beat("במחזור 4 המצב S101 ו-din = 1 :\n‏found עולה מיד, באותו מחזור."):
            self.play(FadeIn(cycles[4], shift=0.1 * RIGHT), run_time=0.6)
            self.play(Indicate(cycles[4][-1], color=C.AMBER), run_time=0.8)
            self.play(reg.set(after[4]), Indicate(reg.box, color=C.AMBER, scale_factor=1.05), run_time=0.6)
        with self.beat("בעלייה הבאה המצב S1, ו-found יורד.\nמחזורים 5 ו-6 מביאים שוב ל-S101."):
            for k in (5, 6):
                add(k)
        with self.beat("ובמחזור 7 found עולה שוב.\nזו בדיוק דיאגרמת התזמון שבעמוד."):
            self.play(FadeIn(cycles[7], shift=0.1 * RIGHT), run_time=0.6)
            self.play(Indicate(cycles[7][-1], color=C.AMBER), run_time=0.8)
        self.fade_all()

        chips = cost_chips(("flip-flops", "2"), ("din → found", "1 gate"),
                           notes=("4 states in 2 bits", "Mealy: combinational"))
        self.say("העלות : שני פלופים לארבעה מצבים, ושער אחד\nמ-din ל-found. בלי רגיסטר הזזה ומשווה.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: back to S0 on every mismatch.
        bits = [1, 0, 1, 0, 1, 1]
        ours, ours_out, _ = mealy([1, 0, 1, 1], bits)
        assert ours == [0, 1, 2, 3, 2, 3] and ours_out == [0, 0, 0, 0, 0, 1]
        naive = [0, 1, 2, 3, 0, 1]
        rows = [["cycle"] + [str(k + 1) for k in range(6)],
                ["din"] + [str(b) for b in bits],
                ["S3 -0-> S0"] + [f"S{s}" for s in naive],
                ["found"] + ["0"] * 6,
                ["S3 -0-> S2"] + [f"S{s}" for s in ours],
                ["found"] + [str(o) for o in ours_out]]
        colors = {(2, 0): C.RED, (4, 0): C.GREEN, (5, 6): C.ORANGE, (2, 5): C.RED, (4, 5): C.GREEN}
        table = grid(rows, col_w=1.15, row_h=0.72, size=30, first_w=3.0, colors=colors).move_to(UP * 0.55)
        self.say("מלכודת : לחזור ל-S0 בכל ביט שלא מתאים.\nנבדוק את הזרם 101011.",
                 FadeIn(table[0:2]), run_time=1.0)
        self.say("אחרי 1010 הגלאי הזה כבר ב-S0, ו-11\nלא מספיקים לו : במחזור 6 אין זיהוי.",
                 FadeIn(table[2:4], lag_ratio=0.2), run_time=1.2)
        self.say("המכונה הנכונה עוברת ל-S2 אחרי 1010,\nכי 10 עוד יכול לפתוח זיהוי, ומזהה במחזור 6.",
                 FadeIn(table[4:6], lag_ratio=0.2), run_time=1.2)
        self.fade_all()


class ChapterB(DVQScene):
    def construct(self):
        self.chapter_card("סעיף ב", "כל תבנית",
                          "סעיף ב : בונים את המכונה לכל תבנית,\nבלי לחשוב על כל מקרה ביד.")

        # The state as a suffix that is a prefix.
        pat = [1, 0, 1, 0, 1]
        prow = bit_row(pat, side=0.7, size=36).move_to(UP * 2.2)
        plab = M("pattern", 28, C.MUTED).next_to(prow, LEFT, buff=0.4)
        self.say("ניקח תבנית אחרת, 10101. המצב s אומר :\nה-s הביטים האחרונים הם ה-s הראשונים שלה.",
                 FadeIn(plab), FadeIn(prow, lag_ratio=0.1))

        text = [1, 0, 1, 1]
        trow = bit_row(text, side=0.7, size=36).move_to(UP * 0.6 + LEFT * 1.2)
        trow[-1][0].set_stroke(C.AMBER, 5)
        tlab = M("input", 28, C.MUTED).next_to(trow, LEFT, buff=0.4)
        self.say("ב-S3 ראינו 101, ומגיע 1.\nהקלט מסתיים עכשיו ב-1011.",
                 FadeIn(tlab), FadeIn(trow, lag_ratio=0.1))

        pitch = trow[1].get_x() - trow[0].get_x()
        slide = bit_row(pat, side=0.7, size=36)
        slide.move_to(trow[0].get_center() + DOWN * 1.0, aligned_edge=LEFT)
        slide.shift(LEFT * 0.35)
        marks = VGroup()

        def compare(shift: int) -> bool:
            ok = True
            res = VGroup()
            for i in range(len(text) - shift):
                good = text[shift + i] == pat[i]
                ok = ok and good
                res.add(SurroundingRectangle(slide[i], color=C.GREEN if good else C.RED,
                                             buff=0.04, corner_radius=0.08, stroke_width=5))
            return ok, res

        with self.beat("מזיזים את התבנית מתחת לקלט. בלי הזזה\nהביט הרביעי לא מתאים : 1 מול 0."):
            self.play(FadeIn(slide, shift=0.2 * DOWN), run_time=0.6)
            ok, marks = compare(0)
            self.play(Create(marks), run_time=0.5)
        with self.beat("מזיזים צעד אחרי צעד, עד שסוף הקלט\nמתחיל את התבנית."):
            for shift in range(1, 4):
                if shift:
                    self.play(FadeOut(marks), slide.animate.shift(RIGHT * pitch), run_time=0.5)
                ok, marks = compare(shift)
                self.play(Create(marks), run_time=0.5)
                if ok:
                    break
                self.wait(0.3)
        self.say("ביט אחד מתאים : המצב הבא S1.\nזו הסיומת הארוכה ביותר שהיא גם התחלה.",
                 Indicate(slide[0], color=C.GREEN, scale_factor=1.25))
        self.fade_all()

        # The formula.
        f1 = TX(r"\mathrm{next}[s][b] = \begin{cases} s + 1 & P[s] = b \\ "
                r"\mathrm{next}[\,\mathrm{fail}(s)\,][b] & \text{otherwise} \end{cases}", size=36)
        f2 = TX(r"\mathrm{fail}(s + 1) = \mathrm{next}[\,\mathrm{fail}(s)\,][\,P[s]\,]", size=36,
                color=C.AMBER)
        VGroup(f1, f2).arrange(DOWN, buff=0.7).move_to(UP * 0.7)
        self.say("אין צורך להזיז ביד. ‏fail(s) הוא המצב\nשל אותה סיומת, בלי הביט הראשון שלה.", FadeIn(f1))
        self.say("ואת fail של המצב הבא מחשבים\nמאותה טבלה, בשורה אחת.", FadeIn(f2))
        self.fade_all()

        # The table of 10101, row by row.
        head = ["s", "seen", "0", "1", "fail"]
        seen = ["start", "1", "10", "101", "1010", "10101"]
        rows = [head] + [[str(s), seen[s], str(NXT_5[s][0]), str(NXT_5[s][1]),
                          "-" if FAIL_5[s] is None else str(FAIL_5[s])] for s in range(6)]
        xs = [-3.6, -1.7, 0.4, 1.9, 3.6]
        table = VGroup()
        for i, row in enumerate(rows):
            line = VGroup(*[M(txt, 30, C.MUTED if i == 0 else C.WHITE).move_to([xs[j], 2.7 - i * 0.68, 0])
                            for j, txt in enumerate(row)])
            table.add(line)
        rule = Line([-4.4, 2.35, 0], [4.4, 2.35, 0], stroke_color=C.FAINT, stroke_width=2)
        for s in range(6):           # the edges that advance in amber
            for b in (0, 1):
                if NXT_5[s][b] == s + 1:
                    table[s + 1][2 + b].set_color(C.AMBER)
        self.say("נבנה את הטבלה של 10101, שורה אחרי שורה.\nבכתום : המעברים שמתקדמים.",
                 FadeIn(table[0]), Create(rule), FadeIn(table[1]))
        self.say("מצב 1 : 0 מתקדם, ו-1 הולך לאן שהולך\nמצב הכישלון 0 עם 1. מצב 2 באותה דרך.",
                 FadeIn(table[2]), FadeIn(table[3]), run_time=1.2)
        self.say("מצב 3 : 0 מתקדם, ו-1 כמו ממצב 1.\nמצב 4 : 1 משלים את התבנית.",
                 FadeIn(table[4]), FadeIn(table[5]), run_time=1.2)
        full = SurroundingRectangle(table[6], color=C.ORANGE, buff=0.1, corner_radius=0.1)
        self.say("המצב המלא 5 מתנהג כמו מצב 3 :\n‏101 הוא גם סוף וגם התחלה של 10101.",
                 FadeIn(table[6]), Create(full), run_time=1.2)
        self.fade_all()

        # The page's next_state, shown whole.
        panel = CodePanel(SV_ANY, font_size=24, language="systemverilog", only=set(range(13, 24)))
        self.place_code(panel)
        self.say("בעמוד, הפונקציה next_state בונה\nבדיוק את הטבלה הזו, בלולאה אחת.", FadeIn(panel))
        for lines, cap in [([19], "בכל שורה : התקדמות על התאמה,\nאחרת המעבר של מצב הכישלון."),
                           ([20], "ושורה אחת מעדכנת את fail\nלמצב הבא, מאותה טבלה.")]:
            band = panel.band(lines)
            panel.code.remove(band)
            band.set_fill(opacity=0.22)
            self.say(cap, FadeIn(band), run_time=0.5)
            self.play(FadeOut(band), run_time=0.3)
        self.fade_all()

        # The box builds 10101.
        view = BoxView(QID, "build", height=5.9).move_to(UP * 0.62)
        self.say("בתיבה מקלידים תבנית, והגרף נבנה לבד.\nמתחתיו : איך נבנה כל מעבר.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי 1, 0, 1 המכונה ב-S3,\nוהתבנית מוזזת לשני הביטים הבאים."),
            (2, "‏0 מתקדם ל-S4. עכשיו 1\nישלים את התבנית."),
            (3, "‏1 משלים את 10101 : הפלט 1,\nוממשיכים מ-S3, לא מההתחלה."),
        ])
        self.fade_all()

        # Mealy against Moore.
        moore = FSM(5, ["start", "1", "10", "101", "1011"], y=0.9, pitch=2.7, out_state=4)
        moore.edge(0, 1, "1"), moore.edge(1, 2, "0"), moore.edge(2, 3, "1"), moore.edge(3, 4, "1")
        moore.edge(0, 0, "0"), moore.edge(1, 1, "1")
        moore.edge(2, 0, "0", depth=0.75)
        moore.edge(3, 2, "0", depth=1.6)
        moore.edge(4, 2, "0", depth=0.6)
        moore.edge(4, 1, "1", depth=1.3)
        out = M("found = 1", 28, C.ORANGE).next_to(moore.nodes[4], UP, buff=0.35)
        self.say("‏Mealy מול Moore. ב-Moore הפלט שייך למצב,\nולכן צריך מצב חמישי, S4, שמוציא 1.",
                 FadeIn(moore.nodes, lag_ratio=0.15), FadeIn(moore.meanings),
                 *[Create(g) for g in moore.edges.values()], FadeIn(out), run_time=2.0)
        rows4 = VGroup(moore.edges[(4, 2)], moore.edges[(4, 1)])
        self.say("מ-S4 : ‏0 ל-S2 ו-1 ל-S1, בדיוק כמו מ-S3\nב-Mealy. לכן Mealy מסתפק בארבעה.",
                 Indicate(rows4, color=C.AMBER, scale_factor=1.05), run_time=1.4)
        self.fade_all()

        # The two outputs on one stream.
        bits = STREAM + [None]
        _, me, _ = mealy([1, 0, 1, 1], STREAM)
        mo = [0] + me                      # Moore: the same detections, a cycle later
        rows = [["cycle"] + [str(k + 1) for k in range(8)],
                ["din"] + ["-" if b is None else str(b) for b in bits],
                ["Mealy"] + [str(v) for v in me + [0]],
                ["Moore"] + [str(v) for v in mo]]
        colors = {(2, 4): C.ORANGE, (2, 7): C.ORANGE, (3, 5): C.ORANGE, (3, 8): C.ORANGE}
        table = grid(rows, col_w=1.0, row_h=0.8, size=32, first_w=2.4, colors=colors).move_to(UP * 0.7)
        self.say("על 1011011 : ‏Mealy מוציא 1 במחזורים 4 ו-7,\nו-Moore מחזור אחד אחריו, ב-5 וב-8.",
                 FadeIn(table, lag_ratio=0.15), run_time=1.4)
        self.say("‏Moore : מצב אחד יותר ומחזור אחד מאוחר,\nאבל המוצא רשום ונקי מגליצ'ים.")
        self.fade_all()

        view = BoxView(QID, "mm", height=5.9).move_to(UP * 0.62)
        self.say("בתיבה : אותו זרם ב-Mealy,\nו-found עולה במחזורים 4 ו-7.", FadeIn(view))
        self.box_beat(view, [(1, "עוברים ל-Moore : חמישה מצבים,\nו-found זז מחזור אחד ימינה.")])
        self.fade_all()

        chips = cost_chips(("flip-flops", r"$\lceil \log_2 (L+1) \rceil$"), ("per bit", "$O(1)$"),
                           notes=("L states, or L+1 for Moore", "one table lookup"))
        self.say("העלות : לוג של L + 1 פלופים,\nומעבר אחד בטבלה לכל ביט.", FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class Closing(DVQScene):
    def construct(self):
        self.closing(QID, [("א", M("4 states; S3 + 1 -> S1, found = 1", 30)),
                           ("ב", M("next[s][b]: s+1, or next[fail(s)][b]", 30))],
                     ["לסיכום : ארבעה מצבים לפי מה שכבר נראה,\nובנייה שיטתית לכל תבנית.",
                      "נסו תבניות משלכם בתיבה\nשבעמוד של שאלה 0040 באתר."],
                     holds=(3.6, 3.6))
