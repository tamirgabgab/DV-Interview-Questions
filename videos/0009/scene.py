"""The tutorial video of question 0009, 16 people, 16 boxes and one helper (script: script.md).

Render with `python videos/render.py 0009` (see VIDEOS.md). The owner's choices
(2026-11-02): part א drawn with the 16 boxes and their notes, a person's walk from his own
box along the notes, the arrows that close into coloured cycles, a cycle longer than 8 that
fails, and person 0 who cuts it with a swap; the main example one cycle of all 16 boxes,
cut by one swap into two cycles of 8, then a second arrangement (the page's example: 11, 3
and 2, cut into 6 and 5); the page's wording on the swaps (one swap is enough, the other
three are not needed); the site's boxes box after part א. Part ב: only the strategy typed
in Python (cycle_from, helper, find_my_note) with its traced runs; the Room class shown
briefly, not typed. About 6-7 minutes.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, T, VarPanel, chip,  # noqa: E402
                 cost_chips, he, page_python, trace)

import q0009  # noqa: E402

QID = 9
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – האסטרטגיה"),
    ("ChapterB", "סעיף ב – כתבו את הקוד"),
    ("Closing", "סיכום"),
]

# The page's box (the page's example, person 0 on, person 13 chosen): the picture as the
# page opens it, then person 13's walk opening by opening (six), then person 0 off and
# the walk to its end (eight boxes, not found). The cycle list and the line without person 0
# are hidden, so the box keeps its size on the page.
BOXES = {
    "walk": {"box": 0, "region": [".bx-box"], "hide": [".bx-cycles", ".bx-alone"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 6},
                       [["check", ".ex-helper", False], ["click", ".ex-all"]]]},
}

N, MAX_OPENS = 16, 8

# ---- the numbers ----------------------------------------------------------------------


def notes_of(cycles: list[list[int]]) -> list[int]:
    """notes[b] for boxes on the given cycles (index 0 unused)."""
    notes = [0] * (N + 1)
    for cyc in cycles:
        for i, b in enumerate(cyc):
            notes[b] = cyc[(i + 1) % len(cyc)]
    assert sorted(notes[1:]) == list(range(1, N + 1))
    return notes


def walk(notes: list[int], me: int) -> tuple[list[int], bool]:
    """The boxes person `me` opens (at most MAX_OPENS) and whether he finds his note."""
    opened, box = [], me
    for _ in range(MAX_OPENS):
        opened.append(box)
        if notes[box] == me:
            return opened, True
        box = notes[box]
    return opened, False


def swapped(notes: list[int], a: int, b: int) -> list[int]:
    out = list(notes)
    out[a], out[b] = out[b], out[a]
    return out


# The main example: one cycle of all 16 boxes.
BIG = [1, 6, 11, 3, 14, 9, 16, 4, 12, 7, 2, 15, 5, 10, 13, 8]
BIG_NOTES = notes_of([BIG])
assert q0009.cycles(BIG_NOTES) == [BIG]
WALK1 = walk(BIG_NOTES, 1)
assert WALK1 == ([1, 6, 11, 3, 14, 9, 16, 4], False) and BIG_NOTES.index(1) == 8 == BIG[15]
H16 = len(BIG) // 2
BIG_CUT = (BIG[0], BIG[H16])                       # boxes 1 and 12
assert BIG_CUT == (1, 12) and (BIG_NOTES[1], BIG_NOTES[12]) == (6, 7)
BIG_AFTER = swapped(BIG_NOTES, *BIG_CUT)
HALF_A = BIG[:1] + BIG[H16 + 1:]                   # 1, 7, 2, 15, 5, 10, 13, 8
HALF_B = BIG[1:H16 + 1]                            # 6, 11, 3, 14, 9, 16, 4, 12
assert sorted(map(sorted, q0009.cycles(BIG_AFTER))) == sorted(map(sorted, [HALF_A, HALF_B]))
assert len(HALF_A) == len(HALF_B) == 8
assert walk(BIG_AFTER, 1) == (HALF_A, True)
assert all(walk(BIG_NOTES, me)[1] is False for me in range(1, N + 1))
assert all(len(walk(BIG_AFTER, me)[0]) == 8 and walk(BIG_AFTER, me)[1] for me in range(1, N + 1))

# The second example: the page's (tools/figures/q0009.py).
NOTES, AFTER, LONG = q0009.NOTES, q0009.AFTER, q0009.LONG
assert q0009.cycles(NOTES) == [LONG, [2, 11, 6], [8, 14]] and len(LONG) == 11
assert q0009.SWAP == (1, 9) == (LONG[0], LONG[len(LONG) // 2]) and len(LONG) // 2 == 5
SIX, FIVE = [1, 4, 16, 10, 5, 13], [3, 15, 9, 7, 12]
assert q0009.cycles(AFTER) == [SIX, [2, 11, 6], FIVE, [8, 14]]
W13 = walk(NOTES, 13)
assert W13 == ([13, 1, 7, 12, 3, 15, 9, 4], False) and NOTES.index(13) == 5 and LONG.index(5) == 9
W13B = walk(AFTER, 13)
assert W13B == ([13, 1, 4, 16, 10, 5], True)
assert max(len(walk(AFTER, me)[0]) for me in range(1, N + 1)) == 6
assert all(walk(AFTER, me)[1] for me in range(1, N + 1))

# Without person 0 (the page's follow-up): 1 - sum 1/L for L = 9..16, about a third.
P_ALONE = 1 - sum(Fraction(1, L) for L in range(9, N + 1))
assert round(float(P_ALONE), 3) == 0.337

# ---- the drawings ---------------------------------------------------------------------

GRID_X = [-5.6 + 1.6 * i for i in range(8)]
GRID_Y = [2.25, 0.55]
CELL = 1.3
NODE_R = 0.3


def grid_pos(b: int) -> np.ndarray:
    return np.array([GRID_X[(b - 1) % 8], GRID_Y[(b - 1) // 8], 0.0])


class BoxCell(VGroup):
    """A box of the grid: its number small at the top left, the note big in the middle."""

    def __init__(self, b: int, note: int):
        super().__init__()
        self.b = b
        self.sq = RoundedRectangle(width=CELL, height=CELL, corner_radius=0.14, stroke_color=C.FAINT,
                                   stroke_width=2.5, fill_color=C.NAVY_LIGHT, fill_opacity=1)
        self.num = M(str(b), 22, C.MUTED).move_to(self.sq.get_corner(UL) + np.array([0.24, -0.2, 0]))
        self.note = M(str(note), 46, C.WHITE, weight="BOLD").move_to(self.sq.get_center() + DOWN * 0.08)
        self.add(self.sq, self.num, self.note)
        self.move_to(grid_pos(b))


def node(b: int, at, color: str = C.FAINT) -> VGroup:
    c = Circle(radius=NODE_R, stroke_color=color, stroke_width=3, fill_color=C.NAVY_LIGHT,
               fill_opacity=1).move_to(at)
    return VGroup(c, M(str(b), 24, C.WHITE).move_to(at))


def ring(cycle: list[int], centre, radius: float) -> dict[int, np.ndarray]:
    """The positions of a cycle's boxes on a circle, clockwise from the top."""
    centre = np.array([*centre, 0.0][:3]) if len(centre) == 2 else np.array(centre)
    n = len(cycle)
    return {b: centre + radius * np.array([np.cos(PI / 2 - TAU * i / n), np.sin(PI / 2 - TAU * i / n), 0])
            for i, b in enumerate(cycle)}


def arcs(cycle: list[int], centre, radius: float, color: str, special: dict | None = None) -> VGroup:
    """The arrows of a cycle along its circle, clockwise; `special` colours single edges."""
    n = len(cycle)
    d = (NODE_R + 0.07) / radius
    out = VGroup()
    for i, b in enumerate(cycle):
        a0 = PI / 2 - TAU * i / n
        col = (special or {}).get(b, color)
        arc = Arc(radius=radius, start_angle=a0 - d, angle=-(TAU / n - 2 * d),
                  arc_center=np.array([centre[0], centre[1], 0.0]), stroke_color=col, stroke_width=4)
        arc.add_tip(tip_length=0.17, tip_width=0.17)
        arc.get_tip().set_color(col)
        out.add(arc)
    return out


class BScene(DVQScene):
    """Helpers shared by the chapters of 0009."""

    def grid(self, notes: list[int]) -> dict[int, BoxCell]:
        return {b: BoxCell(b, notes[b]) for b in range(1, N + 1)}

    def to_rings(self, cells: dict, layout: list[tuple[list[int], tuple, float, str]], run_time=1.6):
        """The grid's boxes fly to their places on the cycles' circles; returns (nodes, arrows, labels)."""
        nodes, anims = {}, []
        for cyc, centre, radius, color in layout:
            for b, p in ring(cyc, centre, radius).items():
                nodes[b] = node(b, p, color)
                anims.append(ReplacementTransform(cells[b], nodes[b]))
        self.play(*anims, run_time=run_time)
        arrows = VGroup(*[arcs(cyc, centre, radius, color) for cyc, centre, radius, color in layout])
        labels = VGroup(*[M(f"L = {len(cyc)}", 30 if radius > 1.2 else 24, color).move_to([centre[0], centre[1], 0])
                          for cyc, centre, radius, color in layout])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15), FadeIn(labels), run_time=1.6)
        return nodes, arrows, labels

    def walk_ring(self, nodes: dict, path: list[int], found: bool, y: float = 3.62, per: float = 0.4):
        """A person's walk on the circles: a ring moves box to box, the boxes opened so far
        and their count at the top. Returns the drawn group."""
        items = [M(str(b) if k == 0 else f"→ {b}", 30, C.WHITE) for k, b in enumerate(path)]
        row = VGroup(*items).arrange(RIGHT, buff=0.18)
        counts = [M(f"{k + 1}/{MAX_OPENS}", 30, C.AMBER) for k in range(len(path))]
        whole = VGroup(row, counts[-1].copy()).arrange(RIGHT, buff=0.5).move_to([0, y, 0])
        for c in counts:
            c.move_to(whole[1]).align_to(whole[1], LEFT)
        ringm = Circle(radius=NODE_R + 0.1, stroke_color=C.AMBER, stroke_width=6).move_to(nodes[path[0]])
        count = counts[0]
        self.play(Create(ringm), FadeIn(items[0]), FadeIn(count), nodes[path[0]][0].animate.set_fill(C.AMBER, 0.35),
                  run_time=per)
        for k, b in enumerate(path[1:], start=1):
            self.play(ringm.animate.move_to(nodes[b]), FadeIn(items[k]), Transform(count, counts[k]),
                      nodes[b][0].animate.set_fill(C.AMBER, 0.35), run_time=per)
        mark = M("✓" if found else "✗", 44, C.GREEN if found else C.RED, weight="BOLD").next_to(count, RIGHT, buff=0.35)
        self.play(FadeIn(mark, scale=1.5), run_time=0.4)
        return VGroup(row, count, mark, ringm)

    def clear_walk(self, nodes: dict, drawn: VGroup, path: list[int]):
        self.play(FadeOut(drawn), *[nodes[b][0].animate.set_fill(C.NAVY_LIGHT, 1) for b in path], run_time=0.6)


# ---- the scenes ------------------------------------------------------------------------


class Opening(BScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "16 אנשים, 16 קופסאות ועוזר אחד",
                     ["א · האסטרטגיה", "ב · כתבו את הקוד"],
                     ["שאלה 0009 : ‏16 אנשים, 16 קופסאות\nועוזר אחד. רמת ג'וניור.",
                      "שני סעיפים : האסטרטגיה,\nואז הקוד שמממש אותה."])
        self.fade_all()
        cells = self.grid(BIG_NOTES)
        self.say("בחדר 16 קופסאות, ובכל אחת פתק עם\nמספר מ-1 עד 16, כל מספר פעם אחת.",
                 LaggedStart(*[FadeIn(c, shift=0.15 * DOWN) for c in cells.values()], lag_ratio=0.05),
                 run_time=1.8)
        big1 = cells[1].copy().scale(1.3).move_to([0, -1.25, 0])
        box_l = he("קופסה", 40, C.MUTED).next_to(big1, LEFT, buff=1.0).align_to(big1.num, UP)
        note_l = he("פתק", 40, C.WHITE).next_to(big1, RIGHT, buff=1.0)
        a1 = Arrow(box_l.get_right(), big1.num.get_left(), buff=0.12, color=C.MUTED, stroke_width=3)
        a2 = Arrow(note_l.get_left(), big1.note.get_right(), buff=0.12, color=C.WHITE, stroke_width=3)
        self.say("המספר הקטן הוא הקופסה, והגדול\nהוא הפתק שבתוכה : בקופסה 1 הפתק 6.",
                 TransformFromCopy(cells[1], big1), FadeIn(box_l), FadeIn(note_l), GrowArrow(a1), GrowArrow(a2))
        self.play(FadeOut(big1), FadeOut(box_l), FadeOut(note_l), FadeOut(a1), FadeOut(a2), run_time=0.5)
        p0 = chip(M("person 0: sees every box, at most 4 swaps", 28), color=C.AMBER).move_to([0, -1.05, 0])
        self.say("אדם 0 נכנס ראשון : מציץ בכל הקופסאות,\nומחליף פתקים עד 4 פעמים.", FadeIn(p0, shift=0.2 * UP))
        p1 = chip(M("persons 1..16: one by one, at most 8 boxes each", 28), color=C.BLUE).move_to([0, -1.85, 0])
        self.say("אחריו אנשים 1 עד 16, אחד אחד : כל\nאחד פותח עד 8 קופסאות, בלי להזיז.",
                 FadeIn(p1, shift=0.2 * UP))
        self.say("המטרה : כולם צריכים למצוא את הפתק\nשלהם. אם אחד נכשל, כולם מפסידים.",
                 Indicate(p1, color=C.AMBER))
        self.fade_all()


class ChapterA(BScene):
    def construct(self):
        self.chapter_card("סעיף א", "האסטרטגיה",
                          "סעיף א : איזו אסטרטגיה מבטיחה\nשכולם ינצחו, בכל סידור של הפתקים?")

        # The walk of person 1 on the grid of the main example.
        cells = self.grid(BIG_NOTES)
        self.play(FadeIn(VGroup(*cells.values())), run_time=0.8)
        ringm = SurroundingRectangle(cells[1], color=C.AMBER, buff=0.06, stroke_width=6, corner_radius=0.16)
        self.say("הרעיון : כל אדם פותח קודם את\nהקופסה עם המספר שלו.", Create(ringm))
        seq = VGroup(M("1", 34))
        seq.move_to([-5.4, -1.2, 0])
        count = M(f"1/{MAX_OPENS}", 34, C.AMBER).move_to([5.0, -1.2, 0])
        self.say("ואז את הקופסה שהמספר שלה כתוב\nעל הפתק שמצא, וכן הלאה.",
                 FadeIn(seq), FadeIn(count), cells[1].sq.animate.set_fill(C.AMBER, 0.3))
        with self.beat("נעקוב אחרי אדם 1 : קופסה 1, בה פתק 6,\nואז 11, 3, 14, 9, 16 ו-4."):
            for k, b in enumerate(WALK1[0][1:], start=2):
                item = M(f"→ {b}", 34).next_to(seq, RIGHT, buff=0.2)
                seq.add(item)
                self.play(ringm.animate.move_to(cells[b]), FadeIn(item),
                          count.animate.become(M(f"{k}/{MAX_OPENS}", 34, C.AMBER).move_to(count)),
                          cells[b].sq.animate.set_fill(C.AMBER, 0.3), run_time=0.45)
        miss = M("✗", 48, C.RED, weight="BOLD").next_to(count, RIGHT, buff=0.3)
        self.say("‏8 פתיחות נגמרו, והפתק 1 עוד לא נמצא.\nהוא בקופסה 8, ה-16 בשרשרת.",
                 FadeIn(miss, scale=1.5), Indicate(cells[8], color=C.RED))
        self.play(FadeOut(VGroup(seq, count, miss, ringm)),
                  *[c.sq.animate.set_fill(C.NAVY_LIGHT, 1) for c in cells.values()], run_time=0.6)

        # The arrows close into a cycle: here all 16 boxes on one circle.
        big = (BIG, (0.0, 0.42), 2.45, C.RED)
        with self.beat("אם ממשיכים מכל קופסה לפי הפתקים,\nהחצים תמיד נסגרים למעגלים."):
            nodes, arrows, labels = self.to_rings(cells, [big])
        self.say("כאן כל 16 הקופסאות על מעגל אחד :\nקופסה 1 שולחת ל-6, ‏6 ל-11, וכן הלאה.",
                 Indicate(nodes[1], color=C.AMBER), Indicate(nodes[6], color=C.AMBER))
        self.say("למה מעגלים? מכל קופסה יוצא חץ אחד,\nואליה נכנס חץ אחד : כל פתק פעם אחת.",
                 Indicate(arrows, color=C.AMBER, scale_factor=1.03))
        self.say("אדם i מתחיל בקופסה i, ולכן\nהוא הולך על המעגל שלה.", Indicate(nodes[1], color=C.AMBER))
        back = nodes[8]
        self.say("הפתק i נמצא בקופסה שמצביעה חזרה\nלקופסה i : האחרונה במעגל.",
                 back[0].animate.set_stroke(C.AMBER, 6), arrows[0][15].animate.set_color(C.AMBER))
        rule = TX(r"\text{cycle of length } L \;\Rightarrow\; \text{note found at open } L",
                  size=34).move_to([0, 3.62, 0])
        self.say("לכן מי שעל מעגל באורך L מוצא את\nהפתק שלו בדיוק בפתיחה ה-L.", FadeIn(rule))
        self.say("מעגל עד 8 : כולם בו מצליחים.\nכאן L = 16 : כל 16 האנשים נכשלים.",
                 Indicate(labels, color=C.RED, scale_factor=1.4))
        self.play(FadeOut(rule), back[0].animate.set_stroke(C.RED, 3), arrows[0][15].animate.set_color(C.RED),
                  run_time=0.5)
        alone = TX(r"1 - \sum_{L=9}^{16} \frac{1}{L} \approx 0.337", size=34, color=C.MUTED).move_to([4.7, 2.9, 0])
        self.say("בלי אדם 0 זה קורה הרבה : האסטרטגיה\nמצליחה רק בכשליש מהסידורים.", FadeIn(alone))
        rnd = TX(r"\text{random: } \left(\tfrac{1}{2}\right)^{16}", size=34, color=C.MUTED).next_to(alone, DOWN, buff=0.45)
        self.say("ובחירה אקראית של 8 קופסאות גרועה\nבהרבה : כמעט אף פעם.", FadeIn(rnd))
        self.play(FadeOut(alone), FadeOut(rnd), run_time=0.5)

        # Person 0 cuts the cycle in the middle: boxes 1 and 12, the notes 6 and 7.
        n6 = M("6", 30, C.AMBER, weight="BOLD")
        n7 = M("7", 30, C.AMBER, weight="BOLD")
        out1 = nodes[1].get_center() + UP * 0.62
        out12 = nodes[12].get_center() + DOWN * 0.62
        n6.move_to(out1)
        n7.move_to(out12)
        self.say("כאן נכנס אדם 0. הוא רואה את כל\nהקופסאות, ולכן רואה את המעגל.",
                 nodes[1][0].animate.set_stroke(C.AMBER, 6), nodes[12][0].animate.set_stroke(C.AMBER, 6))
        self.say("הוא מחליף בין הפתק של קופסה 1,\nתחילת המעגל, לפתק של קופסה 12, באמצע.",
                 FadeIn(n6), FadeIn(n7))
        self.say("פתק 6 עובר לקופסה 12,\nופתק 7 עובר לקופסה 1.",
                 n6.animate(path_arc=PI / 2).move_to(out12), n7.animate(path_arc=PI / 2).move_to(out1),
                 run_time=1.4)
        # The circle splits into two circles of 8.
        left = (HALF_A, (-3.4, 0.42), 1.95, C.GREEN)
        right = (HALF_B, (3.4, 0.42), 1.95, C.BLUE)
        with self.beat("רק שני חצים משתנים, והמעגל מתפצל\nלשני מעגלים, כל אחד באורך 8."):
            self.play(FadeOut(arrows), FadeOut(labels), FadeOut(n6), FadeOut(n7), run_time=0.6)
            moves = []
            new_nodes = {}
            for cyc, centre, radius, color in (left, right):
                for b, p in ring(cyc, centre, radius).items():
                    new_nodes[b] = node(b, p, color)
                    moves.append(Transform(nodes[b], new_nodes[b]))
            self.play(*moves, run_time=1.4)
            special = {1: C.AMBER}
            a_left = arcs(HALF_A, left[1], left[2], C.GREEN, special)
            a_right = arcs(HALF_B, right[1], right[2], C.BLUE, {12: C.AMBER})
            l_lab = VGroup(M("L = 8", 30, C.GREEN).move_to([left[1][0], left[1][1], 0]),
                           M("L = 8", 30, C.BLUE).move_to([right[1][0], right[1][1], 0]))
            self.play(Create(a_left), Create(a_right), FadeIn(l_lab), run_time=1.4)
        with self.beat("אדם 1 עכשיו : ‏1, 7, 2, 15, 5, 10, 13 ו-8.\nבפתיחה השמינית הפתק שלו."):
            drawn = self.walk_ring(nodes, HALF_A, True)
        self.say("כך כל אחד מוצא את הפתק שלו בדיוק\nבפתיחה ה-8 : כולם מנצחים.",
                 Indicate(l_lab, color=C.AMBER, scale_factor=1.3))
        self.fade_all()

        # The proof: at most one long cycle, and one swap cuts it.
        f1 = TX(r"9 + 9 = 18 > 16", size=44).move_to(UP * 2.4)
        self.say("למה זה עובד בכל סידור? עובדה ראשונה :\nיש לכל היותר מעגל ארוך אחד.", FadeIn(f1))
        self.say("סכום אורכי המעגלים הוא 16, ושני\nמעגלים מעל 8 כבר צריכים 18 קופסאות.",
                 Indicate(f1, color=C.AMBER))
        f2 = VGroup(TX(r"c_0 \to c_1 \to \dots \to c_{L-1} \to c_0", size=38),
                    TX(r"\text{swap}(c_0,\, c_h):", size=36, color=C.AMBER),
                    TX(r"c_0 \to c_{h+1} \to \dots \to c_{L-1} \to c_0 \quad (L-h)", size=36, color=C.GREEN),
                    TX(r"c_1 \to c_2 \to \dots \to c_h \to c_1 \quad (h)", size=36, color=C.BLUE)) \
            .arrange(DOWN, buff=0.28).next_to(f1, DOWN, buff=0.5)
        self.say("עובדה שנייה : החלפה בין הפתקים של c0\nושל ch חותכת את המעגל לשני מעגלים.",
                 FadeIn(f2[0]), FadeIn(f2[1]))
        self.say("אחד באורך L − h, והשני באורך h.", FadeIn(f2[2]), FadeIn(f2[3]))
        self.play(FadeOut(f1), f2.animate.shift(UP * 1.1), run_time=0.6)
        f3 = TX(r"h = \lfloor L/2 \rfloor,\quad L \le 16 \;\Rightarrow\; h,\ L-h \le 8", size=40,
                color=C.AMBER).next_to(f2, DOWN, buff=0.5)
        self.say("בוחרים את האמצע, h = ⌊L/2⌋. כי L ≤ 16,\nשני החלקים באורך 8 לכל היותר.", FadeIn(f3))
        f4 = M("1 swap is enough", 36, C.GREEN).next_to(f3, DOWN, buff=0.45)
        self.say("לכן החלפה אחת תמיד מספיקה,\nושלוש ההחלפות הנוספות מיותרות.", FadeIn(f4, shift=0.2 * UP))
        self.fade_all()

        # The second example: the page's.
        cells = self.grid(NOTES)
        self.say("סידור שני, הדוגמה מהעמוד :\nהפתקים בקופסאות 1 עד 16.",
                 LaggedStart(*[FadeIn(c, shift=0.15 * DOWN) for c in cells.values()], lag_ratio=0.04),
                 run_time=1.6)
        long_ = (LONG, (-2.8, 0.42), 2.4, C.RED)
        three = ([2, 11, 6], (3.4, 1.55), 0.9, C.MUTED)
        two = ([8, 14], (3.4, -1.05), 0.75, C.MUTED)
        with self.beat("בעקבות החצים יש שלושה מעגלים :\nבאורך 11, באורך 3 ובאורך 2."):
            nodes, arrows, labels = self.to_rings(cells, [long_, three, two])
        with self.beat("אדם 13 על המעגל הארוך : ‏13, 1, 7, 12,\n\u200f3, 15, 9 ו-4. נגמרו 8 פתיחות."):
            drawn = self.walk_ring(nodes, W13[0], False)
        self.say("הפתק 13 בקופסה 5,\nה-11 במעגל : רחוק מדי.", Indicate(nodes[5], color=C.RED))
        self.clear_walk(nodes, drawn, W13[0])
        n7 = M("7", 30, C.AMBER, weight="BOLD").move_to(nodes[1].get_center() + UP * 0.62)
        n4 = M("4", 30, C.AMBER, weight="BOLD").move_to(nodes[9].get_center() + DOWN * 0.62 + LEFT * 0.2)
        self.say("אדם 0 מחליף בין קופסה 1 לקופסה 9 :\nהן c0 ו-c5, כי ⌊11/2⌋ = 5.",
                 nodes[1][0].animate.set_stroke(C.AMBER, 6), nodes[9][0].animate.set_stroke(C.AMBER, 6),
                 FadeIn(n7), FadeIn(n4))
        six = (SIX, (-4.2, 0.42), 1.6, C.GREEN)
        five = (FIVE, (0.0, 0.42), 1.5, C.BLUE)
        with self.beat("פתק 7 עובר לקופסה 9, ופתק 4 לקופסה 1.\nהמעגל של 11 מתפצל ל-6 ול-5."):
            self.play(n7.animate(path_arc=PI / 2).move_to(n4), n4.animate(path_arc=PI / 2).move_to(n7), run_time=1.1)
            self.play(FadeOut(arrows[0]), FadeOut(labels[0]), FadeOut(n7), FadeOut(n4), run_time=0.5)
            moves = []
            for cyc, centre, radius, color in (six, five):
                for b, p in ring(cyc, centre, radius).items():
                    moves.append(Transform(nodes[b], node(b, p, color)))
            self.play(*moves, run_time=1.2)
            a6 = arcs(SIX, six[1], six[2], C.GREEN, {1: C.AMBER})
            a5 = arcs(FIVE, five[1], five[2], C.BLUE, {9: C.AMBER})
            labs = VGroup(M("L = 6", 26, C.GREEN).move_to([six[1][0], six[1][1], 0]),
                          M("L = 5", 26, C.BLUE).move_to([five[1][0], five[1][1], 0]))
            self.play(Create(a6), Create(a5), FadeIn(labs), run_time=1.2)
        with self.beat("ועכשיו אדם 13 : ‏13, 1, 4, 16, 10 ו-5.\nבקופסה 5 הפתק שלו, בפתיחה השישית."):
            drawn = self.walk_ring(nodes, W13B[0], True)
        self.say("כך כל 16 האנשים : לכל אחד\nמספיקות 6 פתיחות לכל היותר.", Indicate(labs, color=C.AMBER))
        self.fade_all()

        # The page's box.
        view = BoxView(QID, "walk", height=6.2).move_to(UP * 0.62)
        if view.css_scale() < 0.8:
            self.problems.append(f"box at {view.css_scale():.2f} of its page size")
        self.say("בתיבה שבעמוד אותו סידור. החצים\nהמקווקווים הם ההחלפה של אדם 0.", FadeIn(view))
        self.box_beat(view, [
            (1, "בכל לחיצה אדם 13 פותח קופסה :\nקודם קופסה 13, ובה הפתק 1."),
            (3, "ממשיך לפי הפתקים :\nקופסה 1, ואז קופסה 4."),
            (6, "ובפתיחה השישית, בקופסה 5,\nהוא מוצא את הפתק שלו."),
            (7, "בלי אדם 0 המעגל של 11 חוזר באדום,\nואדם 13 נכשל אחרי 8 פתיחות."),
        ])
        self.fade_all()


class ChapterB(BScene):
    def construct(self):
        self.chapter_card("סעיף ב", "כתבו את הקוד",
                          "סעיף ב : לממש את החדר עם המגבלות,\nאת אדם 0, את כל השאר ומשחק שלם.")

        # The room, shown briefly (not typed).
        room = page_python(QID, "class Room")
        rl = room.rstrip("\n").split("\n")

        def ln(s: str) -> int:
            return next(i for i, line in enumerate(rl, start=1) if s in line)

        keep = [i for i, line in enumerate(rl, start=1)
                if line.strip() and not line.strip().startswith("#") and '"""' not in line]
        panel = CodePanel(room, font_size=30, drop_trailing_comments=True, only=keep, rows=12)
        self.place_code(panel)
        groups = [
            ([ln("N = 16"), ln("MAX_OPENS ="), ln("MAX_SWAPS ="), ln("class Room"), ln("def __init__"),
              ln("self._notes ="), ln("self.swaps_left ="), ln("self.opens_left = 0"), ln("self.helper_done = False")],
             "המגבלות : 8 פתיחות ו-4 החלפות. החדר\nשומר עותק פרטי של הפתקים.", None),
            ([ln("def look_all"), ln("only person 0 may look"), ln("return list(self._notes)"), ln("def swap"),
              ln("no swaps allowed"), ln("self.swaps_left -= 1"), ln("self._notes[a], self._notes[b]")],
             "‏look_all ו-swap רק לאדם 0, לפני\nשמישהו נכנס, ועד 4 החלפות.", None),
            ([ln("def enter"), ln("self.helper_done = True"), ln("self.opens_left = MAX_OPENS"), ln("def open_box"),
              ln("no opens left"), ln("self.opens_left -= 1"), ln("return self._notes[box]")],
             "‏enter נותן לכל נכנס 8 פתיחות, ו-open_box\nסופרת אותן : הכללים נאכפים בחדר.", None),
        ]
        with self.beat("קודם החדר, בקצרה ובלי להקליד :\nהמחלקה Room שאוכפת את הכללים."):
            self.play(FadeIn(panel), run_time=0.9)
        self.walk_code(panel, None, groups)
        self.fade_all()

        # The strategy, typed: cycle_from, helper, find_my_note.
        code = page_python(QID, "def cycle_from")
        env = {}
        exec(room, env)
        lines = code.rstrip("\n").split("\n")

        def body(first: str, last: str) -> list[int]:
            a = next(i for i, line in enumerate(lines, start=1) if line.startswith(first))
            b = next(i for i, line in enumerate(lines, start=1) if i > a and last in line)
            return [i for i in range(a, b + 1) if lines[i - 1].strip() and '"""' not in lines[i - 1]]

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            return "[" + ", ".join(map(str, v)) + "]" if isinstance(v, list) else str(v)

        # cycle_from
        only = body("def cycle_from", "return cycle")
        assert only == [1, 3, 4, 5, 6, 7, 8]
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=only)
        steps, result = trace(code, "cycle_from", (NOTES, 2), env)
        assert result == [2, 11, 6]
        example = M("cycle_from(notes, 2) = [2, 11, 6]", 32, C.GREEN)
        self.place_code(panel, extra=example)
        self.type_code(panel, [
            (1, "‏cycle_from מקבלת את הפתקים\nוקופסת התחלה."),
            ([3, 4], "מתחילים רשימה עם קופסת ההתחלה,\nועוברים לקופסה שהפתק שלה מראה."),
            ([5, 6, 7], "כל עוד לא חזרנו להתחלה : מוסיפים\nאת הקופסה, והולכים לפי הפתק שבה."),
            (8, ["בסוף מחזירים את כל המעגל.",
                 ("בדוגמה מהעמוד, מקופסה 2 :\n‏2, 11, 6, וחזרה ל-2.", [FadeIn(example, shift=0.2 * UP)])]),
        ], intro="עכשיו האסטרטגיה. קודם פונקציית עזר,\nמשותפת לאדם 0 ולכל השאר.")
        self.fade_all()

        # helper, and its run on the page's example
        only = body("def helper", "return")
        assert only == [11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=only)
        vp = VarPanel(["start", "cycle"], fmt=fmt, size=32).set_state({})
        self.place_code(panel, vp, vp_width=9.0)
        self.type_code(panel, [
            (11, "אדם 0 הוא הפונקציה helper,\nשמקבלת את החדר."),
            ([13, 14], "הוא קורא את כל הפתקים בבת אחת,\nוזוכר באילו קופסאות כבר ביקר."),
            ([15, 16, 17, 18, 19], "עובר על הקופסאות, מדלג על מי שכבר\nבמעגל, ומוצא את המעגל של כל קופסה חדשה."),
            ([20, 21, 22], "מעגל ארוך מ-8 : החלפה בין הראשונה\nלאמצעית, ויציאה. אין מעגל ארוך שני."),
        ])
        r = env["Room"](NOTES)
        steps, result = trace(code, "helper", (r,), env)
        assert [s.line for s in steps] == [13, 14, 15, 16, 18, 19, 20, 21, 22] and r._notes == AFTER
        assert r.swaps_left == 3
        with self.beat("נריץ את אדם 0 על הדוגמה מהעמוד."):
            self.play(FadeIn(vp), run_time=0.6)
        self.run_code(panel, vp, steps, [
            ([13, 14, 15, 16, 18, 19], "המעגל של קופסה 1 הוא המעגל הארוך,\nעם 11 קופסאות."),
            ([20, 21, 22], "‏11 ארוך מ-8 : מחליף בין cycle[0] = 1\nל-cycle[5] = 9, ויוצא. החלפה אחת."),
        ], step_time=2.8)
        self.fade_all()

        # find_my_note, and person 13's run after the swap
        only = body("def find_my_note", "return False")
        assert only == [25, 27, 28, 29, 30, 31, 32, 33, 34]
        panel = CodePanel(code, font_size=34, drop_trailing_comments=True, only=only)
        vp = VarPanel(["me", "box", "note"], fmt=fmt, size=30).set_state({})
        self.place_code(panel, vp, vp_width=3.6)
        self.type_code(panel, [
            (25, "כל אחד מהאחרים הוא find_my_note :\nמקבל את החדר ואת המספר שלו."),
            ([27, 28], "נכנס, ומתחיל בקופסה שלו : כך הוא\nבטוח על המעגל של הפתק שלו."),
            ([29, 30, 31, 32], "עד 8 פעמים פותח קופסה,\nואם הפתק שלו, הוא מצא."),
            ([33, 34], "אחרת עובר לקופסה שעל הפתק. אחרי\n‏8 פתיחות בלי הפתק : נכשל."),
        ])
        steps, result = trace(code, "find_my_note", (r, 13), env)
        lines_ran = [s.line for s in steps]
        assert result is True and lines_ran == [27, 28] + [29, 30, 31, 33] * 5 + [29, 30, 31, 32]
        with self.beat("אדם 13, אחרי ההחלפה של אדם 0."):
            self.play(FadeIn(vp), run_time=0.6)
        self.run_code(panel, vp, steps, [
            ([27, 28, 29, 30, 31, 33], "הוא מתחיל בקופסה 13, ובה הפתק 1 :\nלא שלו, ולכן עובר לקופסה 1."),
            ([29, 30, 31, 33] * 4, "אחר כך קופסאות 1, 4, 16 ו-10,\nעם הפתקים 4, 16, 10 ו-5."),
            ([29, 30, 31, 32], "בקופסה 5 הפתק 13 : הוא מצא,\nבפתיחה השישית."),
        ], step_time=2.6)
        self.fade_all()

        # play, the tests on the page, the cost.
        play = VGroup(M("play(notes):", 34, C.GREEN),
                      M("Room → helper → find_my_note for 1..16", 32)).arrange(DOWN, buff=0.25)
        play.move_to(UP * 2.4)
        tests = VGroup(M("231 cycle structures  ✓", 34, C.GREEN),
                       M("20,000 random arrangements  ✓", 34, C.GREEN),
                       M("at most 1 swap", 34, C.AMBER)).arrange(DOWN, buff=0.3).next_to(play, DOWN, buff=0.7)
        self.say("‏play בונה חדר, מריץ את אדם 0, ואז\nאת כולם, ובודק שכל 16 מצאו.", FadeIn(play))
        self.say("הקוד נבדק על 231 מבני המעגלים\nועל 20,000 סידורים אקראיים.", FadeIn(tests[0]), FadeIn(tests[1]))
        self.say("בכולם כל 16 האנשים ניצחו,\nעם החלפה אחת לכל היותר.", FadeIn(tests[2]))
        self.fade_all()
        chips = cost_chips(("time", "$O(N)$"), ("memory", "$O(N)$"),
                           notes=("person 0: every box once", "the others: O(1) each"))
        self.say("הסיבוכיות : אדם 0 בזמן ובזיכרון O(N),\nוכל אחד מהאחרים בזיכרון O(1).",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class Closing(BScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"L > 8:\ \text{swap}(c_0,\, c_{\lfloor L/2 \rfloor})", size=36)),
                           ("ב", M("cycle_from · helper · find_my_note", 30))],
                     ["לסיכום : הפתקים יוצרים מעגלים, ואדם 0\nחותך את המעגל הארוך בהחלפה אחת.",
                      "נסו סידורים משלכם בתיבה שבעמוד\nשל שאלה 0009 באתר."],
                     holds=(3.5, 3.5))
