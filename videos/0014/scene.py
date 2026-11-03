"""The tutorial video of question 0014, random squares and rectangles without overlap
(script: script.md).

Render with `python videos/render.py 0014` (see VIDEOS.md). The owner's choices
(2026-11-03): part א with squares drawn on the 10 x 8 grid one after another, an overlap
rejected in red and touching (a whole edge, part of an edge, only a corner) allowed in
green, then the condition (the four zones with <=, and its "and" form), then the page's
SystemVerilog class square_set typed, and walked beside a grid with one of the page's
draws (the solver's answer, constraint by constraint) and the two traps (i < j, < instead
of <=); the checker shapes_ok shown briefly; the site's shapes box drawing three seeds.
Part ב only what changes: the square constraint out, rect_set and constraint_mode typed
(short), a draw of rectangles, the cross that a corner test misses, and the box on
rectangles. About 6-7 minutes.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import (C, MIN_SPLIT_EM, TX, Bounded, BoxView, CodePanel, DVQScene, M, T,  # noqa: E402
                 _lines_of, chip, he, page_code)

import q0014  # noqa: E402

QID = 14
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – ריבועים"),
    ("ChapterB", "סעיף ב – מלבנים"),
    ("Closing", "סיכום"),
]

# The page's box (shapes), its controls row, the grid and the step line; the dragging
# sandbox, the projections switch and the summary hidden. Seeds give fixed draws: 7 (one
# square), 12 (two), 25 (four, three of them touching); on rectangles, 5 (five, three
# touching) and 9 (two).
BOXES = {
    "squares": {"box": 0, "region": [":scope > .ex-controls", ".sh-box", ".sh-step"],
                "hide": ["label:has(.ex-proj)", ".sh-sand", ".sh-sum"],
                "steps": [[], [["fill", ".ex-seed", "7"]], [["fill", ".ex-seed", "12"]],
                          [["fill", ".ex-seed", "25"]]]},
    "rects": {"box": 0, "region": [":scope > .ex-controls", ".sh-box", ".sh-step"],
              "hide": ["label:has(.ex-proj)", ".sh-sand", ".sh-sum"],
              "steps": [[["set", ".ex-kind", "rects"]], [["fill", ".ex-seed", "5"]],
                        [["fill", ".ex-seed", "9"]]]},
}

# ---- the numbers (the page's own Python code, through tools/figures/q0014.py) -----------

NS = q0014.ns
OVERLAP = NS["overlap"]
N_, M_ = 10, 8


def ok_set(shapes, squares=True):
    return NS["shapes_ok"](N_, M_, shapes, squares)


# Part א's walk on the grid: each try against the shapes placed so far.
FIRST = (2, 2, 5, 5)
TRIES = [((4, 3, 7, 6), False), ((5, 2, 7, 4), True), ((5, 5, 7, 7), True),
         ((6, 3, 8, 5), False), ((3, 3, 4, 4), False), ((7, 2, 9, 4), True)]
_placed = [FIRST]
for _s, _ok in TRIES:
    assert _s[2] - _s[0] == _s[3] - _s[1]
    assert (not any(OVERLAP(_s, p) for p in _placed)) == _ok, _s
    if _ok:
        _placed.append(_s)
PLACED = list(_placed)
assert ok_set(PLACED) and len(PLACED) == 4
# what each legal one touches: part of an edge, only a corner, a whole edge
assert FIRST[2] == 5 == TRIES[1][0][0] and TRIES[1][0][3] < FIRST[3]          # x = 5, y 2..4 of 2..5
assert (TRIES[2][0][0], TRIES[2][0][1]) == (FIRST[2], FIRST[3])                # the corner (5, 5)
assert TRIES[5][0][0] == TRIES[1][0][2] and TRIES[5][0][1::2] == TRIES[1][0][1::2]   # x = 7, y 2..4

# The zones around i, and a j that shares its left edge.
ZI = (4, 3, 7, 6)
ZJ = (2, 3, 4, 5)
assert not OVERLAP(ZI, ZJ) and ZJ[2] == ZI[0]

# The solver's answer walked beside the code: the page's third draw of squares (seed 26).
SOL = NS["random_shapes"](N_, M_, 6, squares=True, rng=random.Random(26))
assert SOL == [(2, 2, 7, 7), (8, 1, 10, 3), (5, 1, 6, 2), (7, 3, 10, 6), (7, 7, 8, 8), (7, 2, 8, 3)]
assert ok_set(SOL) and len(SOL) * (len(SOL) - 1) // 2 == 15
TOUCH = [(i, j) for i in range(len(SOL)) for j in range(i + 1, len(SOL))
         if not OVERLAP(SOL[i], SOL[j]) and not (SOL[j][2] < SOL[i][0] or SOL[i][2] < SOL[j][0]
                                                 or SOL[j][3] < SOL[i][1] or SOL[i][3] < SOL[j][1])]
assert len(TOUCH) == 7 and (0, 4) in TOUCH and SOL[0][2:] == SOL[4][:2]   # 1 and 5: the corner (7, 7)

# Part ב: the page's first draw of rectangles that is not all squares (seed 19), the cross.
RECTS = NS["random_shapes"](N_, M_, 6, squares=False, rng=random.Random(19))
assert RECTS == [(1, 1, 5, 6), (7, 1, 10, 5), (8, 5, 9, 7), (5, 6, 8, 7), (1, 7, 9, 8), (5, 1, 7, 2)]
assert ok_set(RECTS, squares=False) and not ok_set(RECTS, squares=True)
CROSS_A, CROSS_B = (1, 4, 9, 6), (4, 1, 6, 8)
assert OVERLAP(CROSS_A, CROSS_B)


def inside(p, s):
    return s[0] < p[0] < s[2] and s[1] < p[1] < s[3]


def corners(s):
    return [(x, y) for x in (s[0], s[2]) for y in (s[1], s[3])]


assert not any(inside(p, CROSS_B) for p in corners(CROSS_A))
assert not any(inside(p, CROSS_A) for p in corners(CROSS_B))
N_SQ = len(list(NS["candidates"](N_, M_, True)))
N_RECT = len(list(NS["candidates"](N_, M_, False)))
assert (N_SQ, N_RECT) == (196, 1260)

SQ_CLASS = page_code(QID, "systemverilog", "class square_set")
CHECKER = page_code(QID, "systemverilog", "function automatic bit shapes_ok")
RECT_CLASS = page_code(QID, "systemverilog", "class rect_set")
MODE = page_code(QID, "systemverilog", "s.c_square.constraint_mode")

COLORS = [C.BLUE, C.GREEN, C.PURPLE]

# ---- the drawings ---------------------------------------------------------------------


class Grid(VGroup):
    """The grid of points (1,1)..(n,m), cell `c`, its point (1, 1) at `origin`."""

    def __init__(self, n=N_, m=M_, c=0.62, ticks=True, tick_size=22):
        super().__init__()
        self.n, self.m, self.c = n, m, c
        self.lines = VGroup()
        for x in range(1, n + 1):
            self.lines.add(Line(self.p(x, 1), self.p(x, m), stroke_color=C.FAINT, stroke_width=2))
        for y in range(1, m + 1):
            self.lines.add(Line(self.p(1, y), self.p(n, y), stroke_color=C.FAINT, stroke_width=2))
        self.add(self.lines)
        self.ticks = VGroup()
        if ticks:
            for x in range(1, n + 1):
                self.ticks.add(M(str(x), tick_size, C.MUTED).move_to(self.p(x, 1) + DOWN * 0.3))
            for y in range(1, m + 1):
                self.ticks.add(M(str(y), tick_size, C.MUTED).move_to(self.p(1, y) + LEFT * 0.3))
            self.add(self.ticks)

    def p(self, x, y):
        """The frame point of grid point (x, y), relative to the lines' first corner."""
        base = self.lines[0].get_start() if len(self.submobjects) else ORIGIN
        return base + np.array([(x - 1) * self.c, (y - 1) * self.c, 0.0])

    def shape(self, s, color, opacity=0.32, label=None, width=4):
        x1, y1, x2, y2 = s
        r = Rectangle(width=(x2 - x1) * self.c, height=(y2 - y1) * self.c, stroke_color=color,
                      stroke_width=width, fill_color=color, fill_opacity=opacity)
        r.move_to((self.p(x1, y1) + self.p(x2, y2)) / 2)
        if label is None:
            return r
        return VGroup(r, M(str(label), 26 if self.c > 0.5 else 20, C.WHITE, weight="BOLD").move_to(r))

    def overlap_area(self, a, b):
        cut = (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))
        return self.shape(cut, C.RED, opacity=0.75, width=0)


def coord(s):
    return f"({s[0]}, {s[1]}) → ({s[2]}, {s[3]})"


class SScene(DVQScene):
    """Helpers shared by the chapters of 0014."""

    def walk(self, panel: CodePanel, groups: list):
        """The code lit group by group (no trace: SystemVerilog), each group with the
        animations of its picture: `groups` is [(lines, caption, [anims] or None), ...]."""
        cursor = None
        for lines, caption, anims in groups:
            lines = _lines_of(lines)
            with self.beat(caption):
                if panel.rows:
                    first, last = panel.index[lines[0]], panel.index[lines[-1]]
                    if first < panel.scroll or last >= panel.scroll + panel.rows:
                        moves = panel.scroll_to(max(0, min(first, len(panel.lines_text) - panel.rows)))
                        if cursor is not None:
                            moves.append(FadeOut(cursor))
                            cursor = None
                        self.play(*moves, run_time=0.7)
                band = panel.band(lines)
                panel.code.remove(band)
                band.set_fill(opacity=0.2)
                if cursor is None:
                    self.play(FadeIn(band), run_time=0.4)
                else:
                    self.play(Transform(cursor, band), run_time=0.4)
                    band = cursor
                cursor = band
                for a in anims or []:
                    self.play(*a if isinstance(a, list) else [a], run_time=0.9)
        if cursor is not None:
            self.play(FadeOut(cursor), run_time=0.3)


# ---- the scenes ------------------------------------------------------------------------


class Opening(SScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "ריבועים ומלבנים אקראיים בלי חפיפה",
                     ["א · ריבועים", "ב · מלבנים"],
                     ["שאלה 0014 : ריבועים ומלבנים אקראיים\nבלי חפיפה. רמת ג'וניור.",
                      "שני סעיפים : ריבועים, ואז\nמלבנים באורכים שונים."])
        self.fade_all()
        g = Grid(c=0.62)
        g.move_to(LEFT * 2.4 + UP * 0.55)
        self.say("נתון grid של 10 על 8 נקודות : ‏x\nמ-1 עד 10, ו-y מ-1 עד 8.",
                 Create(g.lines, lag_ratio=0.05), FadeIn(g.ticks), run_time=1.8)
        sq, rc = (2, 2, 5, 5), (7, 2, 10, 6)
        a = g.shape(sq, C.BLUE)
        d1 = Dot(g.p(2, 2), color=C.AMBER, radius=0.09)
        d2 = Dot(g.p(5, 5), color=C.AMBER, radius=0.09)
        l1 = M("(x1, y1)", 24, C.AMBER).next_to(d1, DR, buff=0.08)
        l2 = M("(x2, y2)", 24, C.AMBER).next_to(d2, UL, buff=0.08)
        self.say("כל צורה מתוארת בשתי נקודות : הפינה\nהשמאלית התחתונה והימנית העליונה.",
                 FadeIn(a), FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2))
        b = g.shape(rc, C.GREEN)
        info = VGroup(M("(2, 2) → (5, 5)", 28, C.BLUE), M("width 3, height 3", 26, C.MUTED),
                      M("(7, 2) → (10, 6)", 28, C.GREEN), M("width 3, height 4", 26, C.MUTED)) \
            .arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * 4.6 + UP * 0.9)
        info[2].shift(DOWN * 0.25)
        info[3].shift(DOWN * 0.25)
        self.say("הריבוע מ-(2, 2) עד (5, 5) : רוחב 3\nוגובה 3. המלבן : רוחב 3 וגובה 4.",
                 FadeIn(b), FadeIn(info))
        self.play(FadeOut(VGroup(d1, d2, l1, l2)), run_time=0.4)
        goal = he("בלי חפיפה", 38, C.AMBER, 600).move_to(RIGHT * 4.6 + DOWN * 1.2)
        self.say("המטרה : להגריל מספר אקראי של צורות,\nכך שאף שתיים לא חופפות.",
                 FadeIn(goal, shift=0.2 * UP))
        self.say("מותר שיהיו צמודות : צלע משותפת,\nחלק מצלע, או רק פינה משותפת.",
                 b.animate.shift(LEFT * 2 * g.c), run_time=1.2)
        self.fade_all()


class ChapterA(SScene):
    def construct(self):
        self.chapter_card("סעיף א", "ריבועים",
                          "סעיף א : להגריל מספר אקראי של\nריבועים על ה-grid, בלי חפיפה.")

        # Squares one after another: red rejected, green allowed.
        g = Grid(c=0.62)
        g.move_to(LEFT * 2.6 + UP * 0.55)
        self.play(FadeIn(g), run_time=0.7)
        placed = [g.shape(FIRST, COLORS[0], label=1)]
        log = VGroup()
        log_x = 3.0

        def log_line(s, ok):
            row = VGroup(M(coord(s), 26, C.WHITE), M("✓" if ok else "✗", 30, C.GREEN if ok else C.RED,
                                                    weight="BOLD")).arrange(RIGHT, buff=0.3)
            row.move_to([log_x, 2.9 - 0.62 * len(log), 0]).align_to([log_x - 1.6, 0, 0], LEFT)
            log.add(row)
            return row

        r0 = log_line(FIRST, True)
        self.say("נוסיף ריבועים אחד אחד.\nהראשון : מ-(2, 2) עד (5, 5).",
                 FadeIn(placed[0]), FadeIn(r0))
        captions = {
            0: "הבא, מ-(4, 3) עד (7, 6), נכנס לתוך\nהראשון : יש שטח משותף. נדחה.",
            1: "מ-(5, 2) עד (7, 4) : נוגע בראשון\nלאורך חלק מהצלע. מותר.",
            2: "מ-(5, 5) עד (7, 7) : נוגע בראשון\nרק בפינה אחת. גם זה מותר.",
            3: "מ-(6, 3) עד (8, 5) : חופף את השני.\nנדחה.",
            4: "ריבוע קטן בתוך הראשון, מ-(3, 3)\nעד (4, 4) : גם הוא חופף. נדחה.",
            5: "מ-(7, 2) עד (9, 4) : צלע משותפת\nשלמה עם השני. מותר.",
        }
        placed_s = [FIRST]
        for k, (s, ok) in enumerate(TRIES):
            with self.beat(captions[k]):
                cand = g.shape(s, C.AMBER, opacity=0.15)
                cand.set_stroke(C.AMBER, 4)
                self.play(FadeIn(cand), run_time=0.5)
                row = log_line(s, ok)
                if ok:
                    keep = g.shape(s, COLORS[len(placed_s) % 3], label=len(placed_s) + 1)
                    self.play(ReplacementTransform(cand, keep), FadeIn(row), run_time=0.8)
                    placed.append(keep)
                    placed_s.append(s)
                else:
                    hits = [p for p in placed_s if OVERLAP(s, p)]
                    bad = VGroup(*[g.overlap_area(s, p) for p in hits])
                    self.play(FadeIn(bad), cand.animate.set_stroke(C.RED, 5), FadeIn(row), run_time=0.7)
                    self.play(FadeOut(bad), FadeOut(cand), run_time=0.6)
        self.say("אז מה אסור? רק שטח משותף.\nנגיעה בקו או בנקודה מותרת.",
                 Indicate(log, color=C.AMBER, scale_factor=1.03))
        self.fade_all()

        # The four zones around i, and <=.
        g = Grid(c=0.62)
        g.move_to(LEFT * 2.6 + UP * 0.55)
        si = g.shape(ZI, C.BLUE, label="i")
        self.say("קשה לתאר ישירות מתי שני ריבועים\nחופפים. קל יותר לתאר מתי לא.", FadeIn(g), FadeIn(si))
        x1, y1, x2, y2 = ZI
        zones = [((1, 1, x1, M_), "משמאל"), ((x2, 1, N_, M_), "מימין"),
                 ((1, 1, N_, y1), "מתחת"), ((1, y2, N_, M_), "מעל")]
        zmobs = VGroup(*[g.shape(z, C.GREEN, opacity=0.12, width=0) for z, _ in zones])
        zl = Group(*[he(name, 30, C.GREEN, 600).move_to(g.p(*pt))
                     for (_, name), pt in zip(zones, [(2.5, 4.5), (8.5, 4.5), (5.5, 2), (5.5, 7)])])
        self.say("ריבוע j לא חופף את i אם הוא\nכולו באחד מארבעת האזורים סביבו.",
                 FadeIn(zmobs), FadeIn(zl))
        ineq = [r"x_2[j] \le x_1[i]", r"x_2[i] \le x_1[j]", r"y_2[j] \le y_1[i]", r"y_2[i] \le y_1[j]"]
        rows = Group()
        for tex, (_, name) in zip(ineq, zones):
            rows.add(Group(TX(tex, size=34), he(name, 30, C.GREEN, 500)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to(RIGHT * 4.5 + UP * 1.3)
        ors = VGroup(*[M("||", 30, C.AMBER).next_to(rows[k + 1][0], LEFT, buff=0.3) for k in range(3)])
        self.say("משמאל : x2 של j לכל היותר x1 של i.\nכך גם מימין, מתחת ומעל.",
                 LaggedStart(*[FadeIn(r, shift=0.15 * LEFT) for r in rows], lag_ratio=0.3), run_time=1.8)
        self.say("מספיק שאחד מהם מתקיים,\nולכן מחברים אותם ב-\"או\".", FadeIn(ors))
        sj = g.shape(ZJ, C.GREEN, label="j")
        eq = TX(r"x_2[j] = x_1[i] = 4", size=34, color=C.AMBER).next_to(rows, DOWN, buff=0.45)
        self.say("הסימן ≤ ולא < : כש-x2 של j שווה\nל-x1 של i, יש צלע משותפת. מותר.",
                 FadeIn(sj), FadeIn(eq), Indicate(rows[0], color=C.AMBER))
        self.fade_all()

        # The "and" form.
        andf = VGroup(TX(r"x_1[i] < x_2[j] \;\wedge\; x_1[j] < x_2[i]", size=40),
                      TX(r"\wedge\;\; y_1[i] < y_2[j] \;\wedge\; y_1[j] < y_2[i]", size=40)) \
            .arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to(UP * 1.6)
        lab = VGroup(M("overlap on x", 28, C.BLUE).next_to(andf[0], LEFT, buff=0.5),
                     M("overlap on y", 28, C.BLUE).next_to(andf[1], LEFT, buff=0.5))
        self.say("ובצורה ההפוכה : חופפים אם ורק אם\nההטלות נפגשות על x וגם על y.",
                 FadeIn(andf), FadeIn(lab))
        dm = M("not (A || B || C || D)  ==  !A && !B && !C && !D", 28, C.MUTED).next_to(andf, DOWN, buff=0.6)
        self.say("זו השלילה של ה-\"או\", לפי דה-מורגן.\nנשתמש בה בבודק, בהמשך.", FadeIn(dm))
        self.fade_all()

        # All the rules.
        rules = VGroup(
            M("c_count      1 <= n <= MAX_SHAPES", 30),
            M("c_on_grid    1 <= x1 < x2 <= N,  1 <= y1 < y2 <= M", 30),
            M("c_square     x2 - x1 == y2 - y1", 30),
            M("c_no_overlap every pair i < j: one of the four zones", 30),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.7)
        if rules.width > 13.2:
            rules.scale(13.2 / rules.width)
        self.say("כל התנאים יחד. כמות : n בין 1\nל-MAX_SHAPES.", FadeIn(rules[0], shift=0.15 * LEFT))
        self.say("כל צורה בתוך ה-grid, והסוף מימין\nומעל להתחלה : צלע באורך 1 לפחות.",
                 FadeIn(rules[1], shift=0.15 * LEFT))
        self.say("ריבוע : הרוחב שווה לגובה. ולכל\nזוג i < j : אחד מארבעת האזורים.",
                 FadeIn(rules[2], shift=0.15 * LEFT), FadeIn(rules[3], shift=0.15 * LEFT))
        self.fade_all()

        # The class, typed.
        panel = CodePanel(SQ_CLASS, font_size=30, drop_comments=True, drop_trailing_comments=True,
                          language="systemverilog", rows=14)
        self.place_code(panel)
        self.type_code(panel, [
            ([1, 2, 3], "המחלקה : גודל ה-grid,\nומספר הצורות המרבי, 6."),
            ([5, 6], "המשתנים האקראיים : n, ומערכים\nדינמיים לפינות של כל צורה."),
            ([9, 10, 11, 12], "התנאי הראשון : n בין 1 ל-6,\nוגודל כל מערך שווה ל-n."),
            ([15, 16, 17, 18, 19, 20], "השני : לכל צורה, בתוך ה-grid,\nוהסוף מימין ומעל להתחלה."),
            ([23, 24, 25], "השלישי : הרוחב שווה לגובה. הוא\nלבד בכוונה, בשביל סעיף ב."),
            ([29, 30, 31, 32, 33, 34, 35], "והרביעי : לכל זוג i < j, ארבעת\nהאזורים מחוברים ב-\"או\", עם ≤."),
        ], intro="עכשיו נכתוב את המחלקה\nב-SystemVerilog, עם constraints.")

        # Walked beside a grid with the solver's answer.
        sg = Grid(c=0.37, tick_size=17)
        left = Bounded(panel)
        room_w = config.frame_width - 0.5 - 0.4
        gw = sg.width + 0.2
        k = min((room_w - gw) / left.width, (3.55 - (-2.38)) / left.height, 1.4)
        target = left.copy().scale(k)
        target.move_to([-config.frame_width / 2 + 0.25 + target.width / 2, (3.55 - 2.38) / 2, 0])
        em = panel.em_px() * k
        if em < MIN_SPLIT_EM:
            self.problems.append(f"code beside the grid {em:.1f} px high at 720p")
        sg.move_to([config.frame_width / 2 - 0.3 - sg.width / 2, 0.75, 0])
        shapes = VGroup(*[sg.shape(s, COLORS[i % 3], label=i + 1) for i, s in enumerate(SOL)])
        outl = VGroup(*[sg.shape(s, C.MUTED, opacity=0.0, width=3) for s in SOL])
        nval = M("n = 6", 30, C.AMBER).next_to(sg, UP, buff=0.25)
        pairs = M("15 pairs  ✓", 28, C.GREEN).next_to(sg, DOWN, buff=0.55)
        with self.beat("‏randomize() פותר את כל התנאים יחד.\nהנה פתרון אחד, מהדוגמאות שבעמוד."):
            self.play(Transform(left, target), FadeIn(sg), run_time=1.2)
        self.walk(panel, [
            ([10, 11], "‏c_count : ה-solver בוחר n = 6,\nוארבעת המערכים בגודל 6.", [FadeIn(nval)]),
            ([16, 17, 18], "‏c_on_grid : כל צורה בתוך ה-grid,\nוהפינה השנייה מימין ומעל.",
             [LaggedStart(*[Create(o) for o in outl], lag_ratio=0.15)]),
            ([24], "‏c_square : הרוחב של כל אחת שווה\nלגובה שלה. כולן ריבועים.",
             [[ReplacementTransform(o, s) for o, s in zip(outl, shapes)]]),
            ([30, 31, 32, 33], "‏c_no_overlap : ‏6 צורות, ‏15 זוגות.\nבכל זוג אחד מארבעת המקרים.",
             [FadeIn(pairs)]),
        ])
        self.say("שימו לב לזוגות הצמודים : ‏1 ו-5, למשל,\nנוגעים בפינה. ה-≤ מאפשר אותם.",
                 Indicate(VGroup(shapes[0], shapes[4]), color=C.AMBER, scale_factor=1.05))

        # The two traps.
        self.play(FadeOut(pairs), FadeOut(nval), run_time=0.4)
        trap1 = VGroup(M("i == j:", 28, C.RED),
                       TX(r"x_2[i] \le x_1[i]\ ?\ \text{no}", size=30, color=C.RED)).arrange(RIGHT, buff=0.3)
        trap1.to_edge(RIGHT, buff=0.35).set_y(-1.95)
        self.walk(panel, [
            ([31], "מלכודת : בלי i < j הלולאה בודקת\nגם צורה מול עצמה.", [FadeIn(trap1)]),
        ])
        self.say("שם אף מקרה לא מתקיים, ולכן\n‏randomize() נכשל תמיד.", Indicate(trap1, color=C.RED))
        self.play(FadeOut(trap1), run_time=0.4)
        trap2 = M("<  instead of <=:  7 touching pairs refused", 28, C.RED).to_edge(RIGHT, buff=0.35).set_y(-1.95)
        self.walk(panel, [
            ([32, 33], "מלכודת שנייה : < במקום ≤. אז\nצורות צמודות נחשבות חופפות.", [FadeIn(trap2)]),
        ])
        self.say("בפתרון הזה 7 זוגות צמודים, וכולם\nהיו נפסלים, בניגוד לדרישה.", Indicate(trap2, color=C.RED))
        self.fade_all()

        # The checker, shown, not typed.
        chk = CodePanel(CHECKER, font_size=26, drop_comments=True, drop_trailing_comments=True,
                        language="systemverilog", only=set(range(2, 14)))
        use = VGroup(M('if (!s.randomize()) $fatal(1, "randomize failed");', 24, C.MUTED),
                     M('if (!shapes_ok(...)) $error("illegal shapes");', 24, C.MUTED)) \
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        grp = self.place_code(chk, extra=use)
        with self.beat("ב-DV לא סומכים על randomize() בלי\nלבדוק : קודם, שהוא החזיר 1."):
            self.play(FadeIn(chk), FadeIn(use[0]), run_time=1.0)
        self.walk(chk, [
            ([8, 9, 10], "ואחר כך בודק נפרד, shapes_ok, שכתוב\nבצורת ה-\"וגם\" : חפיפה על שני הצירים.",
             [FadeIn(use[1])]),
        ])
        self.say("שני ניסוחים של אותו תנאי : טעות\nבאחד לא תעבור בשני.", Indicate(grp, color=C.AMBER,
                                                                                 scale_factor=1.02))
        self.fade_all()

        # The page's box.
        view = BoxView(QID, "squares", height=6.2).move_to(UP * 0.63)
        if view.css_scale() < 0.8:
            self.problems.append(f"box at {view.css_scale():.2f} of its page size")
        self.say("בתיבה שבעמוד : ה-grid של 10 על 8,\nועד 6 צורות בכל הגרלה.", FadeIn(view))
        self.box_beat(view, [
            (1, "ערך אתחול 7 : הגרלה של צורה אחת.\nגם 1 הוא מספר חוקי."),
            (2, "ערך אתחול 12 : שני ריבועים."),
            (3, "ערך אתחול 25 : ארבעה ריבועים,\nושלושה מהם צמודים זה לזה."),
        ])
        self.fade_all()
        cost = VGroup(TX(r"\frac{n(n-1)}{2}", size=48, color=C.AMBER), M("n = 6:  15", 34, C.WHITE)) \
            .arrange(RIGHT, buff=0.8).move_to(UP * 0.8)
        self.say("הסיבוכיות : n(n−1)/2 תנאי זוגות.\nעם 6 צורות, 15 שה-solver פותר יחד.", FadeIn(cost))
        self.fade_all()


class ChapterB(SScene):
    def construct(self):
        self.chapter_card("סעיף ב", "מלבנים",
                          "סעיף ב : מלבנים באורכים שונים.\nעדיין בלי חפיפה, ומותר צמוד.")
        rules = VGroup(M("c_count", 34), M("c_on_grid", 34), M("c_square", 34), M("c_no_overlap", 34)) \
            .arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.8)
        self.say("איזה תנאי שייך רק לריבועים?\nרק אחד : הרוחב שווה לגובה.", FadeIn(rules))
        cross = Line(rules[2].get_left() + LEFT * 0.15, rules[2].get_right() + RIGHT * 0.15,
                     stroke_color=C.RED, stroke_width=6)
        self.say("אותו מוציאים. וכל השאר נשארים,\nגם תנאי החפיפה, כמו שהוא.",
                 Create(cross), rules[2].animate.set_color(C.RED), Indicate(rules[3], color=C.GREEN))
        self.fade_all()

        panel = CodePanel(RECT_CLASS, font_size=34, drop_comments=True, language="systemverilog")
        self.place_code(panel)
        self.type_code(panel, [
            (1, "מחלקה יורשת : rect_set מקבלת את\nכל התנאים של square_set."),
            ([3, 4], "‏constraint באותו שם מחליף את זה\nשל מחלקת הבסיס. גוף ריק : בלי תנאי."),
        ])
        self.fade_all()
        panel = CodePanel(MODE, font_size=34, drop_trailing_comments=True, language="systemverilog")
        self.place_code(panel)
        self.type_code(panel, [
            (1, "יוצרים square_set רגיל."),
            (2, "‏constraint_mode(0) מכבה את c_square\nבאובייקט הזה : עכשיו הוא מגריל מלבנים."),
            (3, "ומגרילים כרגיל."),
        ], intro="דרך שנייה, בלי מחלקה חדשה : לכבות\nאת התנאי באובייקט קיים.")
        self.fade_all()

        # A draw of rectangles.
        g = Grid(c=0.62)
        g.move_to(UP * 0.55)
        shapes = VGroup(*[g.shape(s, COLORS[i % 3], label=i + 1) for i, s in enumerate(RECTS)])
        self.say("הגרלה של מלבנים, מהדוגמאות שבעמוד :\nשש צורות, רובן צמודות, בלי שטח משותף.",
                 FadeIn(g), LaggedStart(*[FadeIn(s) for s in shapes], lag_ratio=0.2), run_time=2.0)
        self.fade_all()

        # The cross.
        g = Grid(n=9, m=8, c=0.62)
        g.move_to(LEFT * 1.6 + UP * 0.55)
        a = g.shape(CROSS_A, C.BLUE)
        b = g.shape(CROSS_B, C.GREEN)
        self.say("למה לא לבדוק לפי פינות? הנה שני\nמלבנים בצורת צלב.", FadeIn(g), FadeIn(a), FadeIn(b))
        dots = VGroup(*[Dot(g.p(*p), radius=0.09, color=C.BLUE) for p in corners(CROSS_A)],
                      *[Dot(g.p(*p), radius=0.09, color=C.GREEN) for p in corners(CROSS_B)])
        bad = g.overlap_area(CROSS_A, CROSS_B)
        self.say("אף פינה של אחד לא בתוך השני,\nובכל זאת יש שטח משותף.", FadeIn(dots), FadeIn(bad))
        y0 = g.p(1, 1)[1] - 0.6
        x0 = g.p(1, 1)[0] - 0.55
        px = VGroup(Line([g.p(CROSS_A[0], 1)[0], y0, 0], [g.p(CROSS_A[2], 1)[0], y0, 0], stroke_color=C.BLUE, stroke_width=8),
                    Line([g.p(CROSS_B[0], 1)[0], y0 - 0.2, 0], [g.p(CROSS_B[2], 1)[0], y0 - 0.2, 0], stroke_color=C.GREEN, stroke_width=8))
        py = VGroup(Line([x0, g.p(1, CROSS_A[1])[1], 0], [x0, g.p(1, CROSS_A[3])[1], 0], stroke_color=C.BLUE, stroke_width=8),
                    Line([x0 - 0.2, g.p(1, CROSS_B[1])[1], 0], [x0 - 0.2, g.p(1, CROSS_B[3])[1], 0], stroke_color=C.GREEN, stroke_width=8))
        g.ticks.set_opacity(0.0)
        self.say("התנאי שלנו בודק את ההטלות : הן\nנפגשות על x וגם על y. חופפים.", Create(px), Create(py))
        self.say("בריבועים צלב לא ייתכן, ולכן רק\nהתנאי על הצירים נכון לשני הסעיפים.",
                 Indicate(VGroup(px, py), color=C.AMBER))
        self.fade_all()

        view = BoxView(QID, "rects", height=6.2).move_to(UP * 0.63)
        if view.css_scale() < 0.8:
            self.problems.append(f"box at {view.css_scale():.2f} of its page size")
        self.say("בתיבה שבעמוד : עוברים למלבנים,\nסעיף ב.", FadeIn(view))
        self.box_beat(view, [
            (1, "ערך אתחול 5 : חמישה מלבנים,\nושלושה מהם צמודים."),
            (2, "ערך אתחול 9 : שני מלבנים."),
        ])
        self.fade_all()
        nums = VGroup(M(f"squares     {N_SQ}", 34, C.BLUE), M(f"rectangles  {N_RECT:,}", 34, C.GREEN)) \
            .arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 1.0)
        self.say("בפתרון ב-Python שבעמוד : ‏196 ריבועים\nאפשריים ב-grid, ו-1,260 מלבנים.", FadeIn(nums))
        self.say("וב-SystemVerilog אותה סיבוכיות :\nתנאי זוגות, n(n−1)/2.", Indicate(nums, color=C.AMBER))
        self.fade_all()


class Closing(SScene):
    def construct(self):
        self.closing(QID, [("א", M("x2[j] <= x1[i] || x2[i] <= x1[j] ||\ny2[j] <= y1[i] || y2[i] <= y1[j]", 26)),
                           ("ב", M("rect_set: constraint c_square { }", 28))],
                     ["לסיכום : ארבעה אזורים ב-\"או\", עם ≤\nכדי שצורות צמודות יהיו מותרות.",
                      "נסו הגרלות משלכם בתיבה שבעמוד\nשל שאלה 0014 באתר."],
                     holds=(3.5, 3.5))
