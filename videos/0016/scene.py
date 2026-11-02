"""The tutorial video of question 0016, the Josephus problem (script: script.md).

Render with `python videos/render.py 0016` (see VIDEOS.md). No code in this question's
video (the owner, 2026-11-02): parts א and ב get their formula and its proof, part ג is a
short chapter with the general formula and its check against parts א and ב.

The circle: numbered people on a ring, an amber pointer that goes around clockwise, the
one who stays lit blue, each one who leaves lit red and then greyed out and faded, the
number still in the circle at the centre, the survivor green. Every step is the page's
reference (tools/figures/q0016.py's run()).

Part א: the page's example N = 5 step by step; the survivors for N = 1 to 32 in rows that
start at the powers of 2 (a zero at each, a climb of 2 in between); the proof through the
power of 2 (the owner's choice): with 2^m people the one who starts survives (every round
halves the circle and the count comes back to the starter: N = 8), and with N = 2^m + r
people, after r eliminations 2^m are left and person 2r starts, so F(N) = 2r. It is
played on 41 people (the number of the story, where the rule was another one: the page's
trap), stopping after 9 eliminations at person 18, then to the end. The bits: N as a row
of bit cells, the top bit moves to the end and arrives as 0 (numbering from 0; from 1 it
would stay 1, the page's trap), on 20 and 41. Then the page's box, round by round.

Part ב, in the same order and faster: N = 7 step by step, the survivors up to 30 in two
chains by parity (the zero points 1, 3, 9, 27 and 2, 6, 18, the climb of 3 per step of 2),
the zero points from a full round (F3(3k) = 3 F3(k)), and the same stop: on 30 people,
after 6 steps 18 are left (a zero point) and person 18 starts, so F3 = 3j = 3/2 (N - M).
Part ג: the recurrence of one step, the L - 1 chains, the zero points b L^m and the
formula, checked with L = 2, 3 and F4(20) = 16.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, he  # noqa: E402

import q0016  # noqa: E402

QID = 16
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – אחד נשאר, אחד יוצא"),
    ("ChapterB", "סעיף ב – אחד נשאר, שניים יוצאים"),
    ("ChapterC", "סעיף ג – בונוס : אחד נשאר, L − 1 יוצאים"),
    ("Closing", "סיכום"),
]

# The page's first box (N = 20, L = 2): the picture after 0, 10, 15 and 19 steps, the
# ends of the rounds (the scrub slider of the player).
BOXES = {
    "rounds": {"box": 0, "region": [".ex-play-row", ".jos-box"],
               "steps": [[], [["set", ".ex-scrub", "10"]], [["set", ".ex-scrub", "15"]],
                         [["set", ".ex-scrub", "19"]]]},
    "rounds3": {"box": 1, "region": [".ex-play-row", ".jos-box"],
                "steps": [[], [["set", ".ex-scrub", "10"]], [["set", ".ex-scrub", "14"]], [["set", ".ex-scrub", "15"]]]},
}

# ---- the numbers, all from the page's reference ------------------------------------------

F2 = [q0016.survivor(n) for n in range(1, 33)]
F3 = [q0016.survivor(n, 3) for n in range(1, 31)]
assert q0016.run(5) == ([(0, [1]), (2, [3]), (4, [0]), (2, [4])], 2)
assert q0016.run(7, 3) == ([(0, [1, 2]), (3, [4, 5]), (6, [0, 3])], 6)
assert q0016.rounds(8)[0] == [[(0, [1]), (2, [3]), (4, [5]), (6, [7])], [(0, [2]), (4, [6])], [(0, [4])]]
assert all(F2[n - 1] == q0016.formula(n) == 2 * (n - 2 ** (n.bit_length() - 1)) for n in range(1, 33))
assert [n for n in range(1, 33) if F2[n - 1] == 0] == [1, 2, 4, 8, 16, 32]
STEPS41, WIN41 = q0016.run(41)
assert WIN41 == 18 == q0016.formula(41) and 41 == 32 + 9
assert [s for s, _ in STEPS41[:9]] == list(range(0, 17, 2)) and STEPS41[9][0] == 18
assert [len(r) for r in q0016.rounds(41)[0]] == [21, 10, 5, 3, 1]
assert F2[11] == 8 and F2[30] == 30 and q0016.survivor(10) == 4
assert q0016.survivor(20) == 8 and format(20, "b") == "10100" and format(41, "b") == "101001"
assert int("01000", 2) == 8 and int("010010", 2) == 18
assert [n for n in range(1, 31) if F3[n - 1] == 0] == [1, 2, 3, 6, 9, 18, 27]
assert all(F3[n - 1] == q0016.formula(n, 3) for n in range(1, 31))
STEPS30, WIN30 = q0016.run(30, 3)
assert WIN30 == 18 and [s for s, _ in STEPS30[:6]] == [0, 3, 6, 9, 12, 15] and STEPS30[6][0] == 18
assert (int('120', 3), int('20', 3), int('200', 3), int('101', 3), int('11', 3)) == (15, 6, 18, 10, 4)
assert q0016.zero_below(30, 3) == 18 and q0016.zero_below(21, 3) == 9 and q0016.survivor(21, 3) == 18
assert [len(r) for r in q0016.rounds(30, 3)[0]] == [10, 4, 1] and len(STEPS30) == 15
assert q0016.survivor(10, 3) == 6 and q0016.survivor(9, 3) == 0
assert q0016.residue(20, 4) == 2 and q0016.zero_below(20, 4) == 8 and q0016.survivor(20, 4) == 16 == q0016.formula(20, 4)
assert all(q0016.survivor(n, L) == q0016.formula(n, L) for L in (2, 3, 4, 5) for n in range(1, 80))

# ---- the circle --------------------------------------------------------------------------


class Ring(VGroup):
    """People 0 .. n - 1 on a ring, clockwise from the top; the pointer outside the ring,
    the number still in the circle at the centre."""

    def __init__(self, n, center=ORIGIN, radius=2.0, dot=0.32, size=28):
        super().__init__()
        self.n, self.c, self.R, self.d, self.size = n, np.array(center, dtype=float), radius, dot, size
        self.people = []
        for i in range(n):
            p = self.pos(i)
            disc = Circle(radius=dot, stroke_color=C.MUTED, stroke_width=3, fill_color=C.NAVY_LIGHT,
                          fill_opacity=1).move_to(p)
            self.people.append(VGroup(disc, M(str(i), size, C.WHITE).move_to(p)))
        self.ppl = VGroup(*self.people)
        self.alive = n
        self.num = M(str(n), size * 1.5, C.MUTED).move_to(self.c)
        tip = self.c + (radius + dot + 0.12) * UP
        self.ptr = Triangle(fill_color=C.AMBER, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI)
        self.ptr.next_to(tip, UP, buff=0)
        self.ang = PI / 2
        self.stay = None
        self.add(self.ppl, self.num, self.ptr)

    def angle(self, i):
        return PI / 2 - TAU * i / self.n

    def pos(self, i, r=None):
        a = self.angle(i)
        return self.c + (self.R if r is None else r) * np.array([np.cos(a), np.sin(a), 0])

    def to(self, i):
        """The pointer to person i, clockwise."""
        target = self.angle(i)
        delta = -((self.ang - target) % TAU)
        self.ang = target
        if abs(delta) < 1e-9:
            return []
        return [Rotate(self.ptr, angle=delta, about_point=self.c)]

    def lit(self, i, color, width=6, fill=0.35):
        disc = self.people[i][0]
        return disc.animate.set_stroke(color, width).set_fill(interpolate_color(ManimColor(C.NAVY_LIGHT), ManimColor(color), fill), 1)

    def calm(self, i):
        return self.people[i][0].animate.set_stroke(C.MUTED, 3).set_fill(C.NAVY_LIGHT, 1)

    def gone(self, i):
        disc, lab = self.people[i]
        return [disc.animate.set_stroke(C.FAINT, 2).set_fill(C.NAVY_LIGHT, 0.2),
                lab.animate.set_color(C.MUTED).set_opacity(0.3)]

    def count(self, k):
        self.alive -= k
        new = M(str(self.alive), self.size * 1.5, C.MUTED).move_to(self.c)
        return Transform(self.num, new)

    def label(self, i, text, color=None, r=None):
        """A small label outside person i (a new number)."""
        return M(text, self.size * 0.9, color or C.GREEN).move_to(self.pos(i, (r or self.R + self.d + 0.32)))


class JScene(DVQScene):
    """The steps of a circle: slow (stay, then each one who leaves) or fast."""

    def slow_step(self, ring, stays, leaves):
        anims = ring.to(stays) + [ring.lit(stays, C.BLUE)]
        if ring.stay is not None and ring.stay != stays:
            anims.append(ring.calm(ring.stay))
        ring.stay = stays
        self.play(*anims, run_time=0.7)
        for i in leaves:
            self.play(*ring.to(i), ring.lit(i, C.RED, fill=0.5), run_time=0.6)
            self.play(*ring.gone(i), ring.count(1), run_time=0.45)

    def fast_steps(self, ring, steps, t=0.3):
        for stays, leaves in steps:
            anims = ring.to(leaves[-1])
            for i in leaves:
                anims += ring.gone(i)
            if ring.stay is not None:
                anims.append(ring.calm(ring.stay))
                ring.stay = None
            self.play(*anims, ring.count(len(leaves)), run_time=t)

    def win(self, ring, i):
        return ring.lit(i, C.GREEN, width=7, fill=0.45)


class Opening(JScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "בעיית יוספוס",
                     ["א · אחד יוצא", "ב · שניים יוצאים", "ג · L − 1 יוצאים"],
                     ["שאלה 0016 : בעיית יוספוס,\nשאלה ברמת ג'וניור.",
                      "שלושה סעיפים : אחד יוצא, שניים יוצאים,\nובבונוס L − 1 יוצאים."])
        self.fade_all()
        ring = Ring(8, center=UP * 0.45, radius=2.0, dot=0.34, size=30)
        self.say("במעגל עומדים N אנשים, ממוספרים\nמ-0 עד N − 1 עם כיוון השעון.",
                 LaggedStart(*[FadeIn(p, scale=0.6) for p in ring.people], lag_ratio=0.08), FadeIn(ring.num),
                 run_time=1.6)
        self.say("אדם 0 נשאר, הבאים אחריו יוצאים,\nהבא נשאר, וכך שוב ושוב סביב המעגל.",
                 FadeIn(ring.ptr), ring.lit(0, C.BLUE))
        self.say("עד שנשאר אדם אחד : השורד.\nמי הוא, ומה הנוסחה לכל N?")
        self.fade_all()


class ChapterA(JScene):
    def construct(self):
        self.chapter_card("סעיף א", "אחד נשאר, אחד יוצא",
                          "סעיף א : אדם 0 נשאר ואדם 1 יוצא,\nכלומר כל שני יוצא. השורד הוא F(N).")
        self.five()
        self.table()
        self.power()
        self.forty_one()
        self.bits()
        self.box()

    def five(self):
        ring = Ring(5, center=UP * 0.45, radius=1.8, dot=0.38, size=32)
        self.play(FadeIn(ring), run_time=0.8)
        steps = q0016.run(5)[0]
        caps = ["נתחיל ב-5 אנשים. אדם 0 נשאר,\nואדם 1 יוצא.",
                "אדם 2 נשאר, ואדם 3 יוצא.",
                "אדם 4 נשאר, והספירה ממשיכה סביב\nהמעגל : אדם 0 יוצא.",
                "אדם 2 נשאר, ואדם 4 יוצא.\nהשורד הוא אדם 2 : F(5) = 2."]
        for (stays, leaves), cap in zip(steps, caps):
            with self.beat(cap):
                self.slow_step(ring, stays, leaves)
                if cap is caps[-1]:
                    self.play(self.win(ring, 2), run_time=0.5)
        self.fade_all()

    def table(self):
        rows = [(1, 1), (2, 3), (4, 7), (8, 15), (16, 31), (32, 32)]
        x0, dx, y0, dy = -5.4, 0.72, 2.85, 0.9
        cells, zeros, ns = [], VGroup(), VGroup()
        for r, (a, b) in enumerate(rows):
            row = VGroup()
            for j, n in enumerate(range(a, b + 1)):
                x, y = x0 + j * dx, y0 - r * dy
                f = F2[n - 1]
                top = M(str(n), 18, C.MUTED).move_to([x, y + 0.24, 0])
                val = M(str(f), 28, C.AMBER if f == 0 else C.WHITE).move_to([x, y - 0.12, 0])
                row.add(VGroup(top, val))
                ns.add(top)
                if f == 0:
                    zeros.add(val)
            cells.append(row)
        head = VGroup(TX(r"N", size=26, color=C.MUTED), TX(r"F(N)", size=26)).arrange(DOWN, buff=0.12)
        head.next_to(cells[0][0], LEFT, buff=0.45)
        self.say("נחשב את השורד לכל N עד 32,\nושורה חדשה בכל חזקה של 2.", FadeIn(head),
                 LaggedStart(*[FadeIn(row, shift=0.15 * RIGHT) for row in cells], lag_ratio=0.35), run_time=2.4)
        boxz = SurroundingRectangle(VGroup(*[row[0] for row in cells]), color=C.AMBER, buff=0.1, corner_radius=0.1)
        y = y0 - 4 * dy - 0.42
        climb = Arrow([x0 - 0.1, y, 0], [x0 + 15 * dx + 0.1, y, 0], buff=0, color=C.GREEN, stroke_width=4,
                      max_tip_length_to_length_ratio=0.03)
        plus = TX(r"+2", size=26, color=C.GREEN).next_to(climb, RIGHT, buff=0.15)
        self.say("בכל חזקה של 2 השורד הוא 0, ומשם\nהוא עולה ב-2 עם כל אדם נוסף.", Create(boxz), GrowArrow(climb),
                 FadeIn(plus))
        self.say("למשל 12 = 8 + 4 נותן 8, ו-31 = 16 + 15\nנותן 30, התא האחרון של השורה של 16.")
        guess = TX(r"N = 2^m + r,\ \ 0 \le r < 2^m \;\Longrightarrow\; F(N) = 2r", size=36, color=C.AMBER)
        guess.move_to(DOWN * 2.15)
        self.say("ההשערה : אם N = 2ᵐ + r עם r < 2ᵐ,\nאז F(N) = 2r. עכשיו נוכיח.", FadeIn(guess))
        self.fade_all()

    def power(self):
        ring = Ring(8, center=[-3.3, 0.45, 0], radius=2.0, dot=0.34, size=30)
        claim = TX(r"F(2^m) = 0", size=44, color=C.AMBER).move_to([3.3, 2.2, 0])
        self.say("קודם חזקה של 2 : עם 8 אנשים,\nמי שמתחיל את הספירה הוא השורד.", FadeIn(ring), FadeIn(claim))
        rounds = q0016.rounds(8)[0]
        with self.beat("סיבוב 1 : יוצאים כל האי-זוגיים, נשארו 4,\nוהספירה חוזרת בדיוק לאדם 0."):
            self.play(ring.lit(0, C.BLUE), run_time=0.4)
            ring.stay = None
            self.fast_steps(ring, rounds[0], t=0.45)
            self.play(*ring.to(0), ring.lit(0, C.BLUE), run_time=0.5)
        with self.beat("כל סיבוב חוצה את המעגל, וחוזר למי\nשהתחיל. אחרי 3 סיבובים נשאר רק אדם 0."):
            self.fast_steps(ring, rounds[1], t=0.45)
            self.play(*ring.to(0), run_time=0.4)
            self.fast_steps(ring, rounds[2], t=0.45)
            self.play(*ring.to(0), self.win(ring, 0), run_time=0.5)
        why = TX(r"2^m \to 2^{m-1} \to \cdots \to 1", size=40).move_to([3.3, 0.9, 0])
        self.say("עם 2ᵐ אנשים כל סיבוב משאיר חצי, שוב\nחזקה של 2, ולכן מי שמתחיל שורד.", FadeIn(why))
        half = TX(r"F(2k) = 2\,F(k)", size=44).move_to([3.3, -0.3, 0])
        self.say("ובכלל, כש-N זוגי סיבוב שלם משאיר את\nהזוגיים ומתחיל שוב מ-0 : F(2k) = 2F(k).", FadeIn(half))
        ex = TX(r"F(20) = 2F(10) = 4F(5) = 8", size=40, color=C.AMBER).move_to([3.3, -1.4, 0])
        self.say("למשל F(20) = 2F(10) = 4F(5) = 8,\nואת F(5) = 2 כבר ראינו.", FadeIn(ex))
        self.fade_all()

    def forty_one(self):
        ring = Ring(41, center=[-3.15, 0.35, 0], radius=2.5, dot=0.165, size=14)
        story = he("יוסף בן מתתיהו, יודפת", 34, C.MUTED).move_to([3.4, 2.9, 0])
        self.say("לפי הסיפור, ביודפת עמדו 41 אנשים\nבמעגל, אבל שם כל שלישי יצא, כלל אחר.",
                 FadeIn(story), LaggedStart(*[FadeIn(p) for p in ring.people], lag_ratio=0.02), FadeIn(ring.num),
                 FadeIn(ring.ptr), run_time=2.0)
        split = TX(r"41 = 32 + 9", size=44).move_to([3.4, 1.7, 0])
        self.say("נריץ את הכלל שלנו על 41 = 32 + 9 :\nחזקה של 2, ועוד 9 אנשים.", FadeIn(split))
        with self.beat("מוציאים 9 אנשים, 1, 3 עד 17,\nעד שנשארים בדיוק 32 : חזקה של 2."):
            self.fast_steps(ring, STEPS41[:9], t=0.42)
        stop = Circle(radius=ring.d + 0.13, stroke_color=C.AMBER, stroke_width=6).move_to(ring.pos(18))
        lab = M("18", 26, C.AMBER).move_to(ring.pos(18, ring.R + ring.d + 0.42))
        rule = TX(r"F(N) = 2r = 2 \cdot 9 = 18", size=44, color=C.AMBER).move_to([3.4, 0.5, 0])
        self.say("ועכשיו הספירה מתחילה מאדם 18.\nמעגל של 32, ולכן 18 הוא השורד.",
                 *ring.to(18), Create(stop), FadeIn(lab), FadeIn(rule))
        self.say("באופן כללי : אחרי r יציאות יצאו כל\nהאי-זוגיים עד 2r − 1, ומתחיל אדם 2r.")
        self.say("כל אדם נוסף מוסיף יציאה אחת לפני\nהחזקה של 2, ולכן השורד זז ב-2.")
        rest = STEPS41[9:]
        groups = [rest[:12], rest[12:24], rest[24:]]
        with self.beat("נמשיך עד הסוף, כדי לבדוק :\nכולם יוצאים, חוץ מאדם 18."):
            self.play(FadeOut(stop), run_time=0.3)
            for g in groups:
                self.fast_steps(ring, g, t=0.11)
            self.play(self.win(ring, 18), run_time=0.5)
        check = TX(r"20 = 16 + 4 \;\Rightarrow\; F(20) = 8", size=40).move_to([3.4, -0.7, 0])
        self.say("השורד הוא 18 : F(41) = 18. ובאותה\nדרך, 20 = 16 + 4 נותן F(20) = 8.", FadeIn(check))
        self.fade_all()

    def bit_row(self, bits, y, label):
        cells = VGroup()
        for k, b in enumerate(bits):
            sq = Square(side_length=0.72, stroke_color=C.MUTED, stroke_width=3, fill_color=C.NAVY_LIGHT, fill_opacity=1)
            cells.add(VGroup(sq, M(b, 34, C.AMBER if k == 0 else C.WHITE)))
        cells.arrange(RIGHT, buff=0.08).move_to([0.2, y, 0])
        name = M(label, 34, C.MUTED).next_to(cells, LEFT, buff=0.5)
        return name, cells

    def rotate_bits(self, cells, name=None, n=0):
        """The top bit moves to the end and arrives as 0: the others shift one cell left;
        the row's label N = becomes F(N) =."""
        top = cells[0]
        step = cells[1].get_center() - cells[0].get_center()
        end = cells[-1].get_center()
        anims = [c.animate.shift(-step) for c in cells[1:]]
        anims.append(top.animate(path_arc=-PI * 0.75).move_to(end))
        if name is not None:
            anims.append(Transform(name, M(f"F({n}) =", 34, C.MUTED).next_to(cells, LEFT, buff=0.5)
                                   .shift(LEFT * 0)))
        self.play(*anims, run_time=1.2)
        zero = M("0", 34, C.AMBER).move_to(top[1])
        self.play(Transform(top[1], zero), run_time=0.5)

    def bits(self):
        name20, row20 = self.bit_row("10100", 1.6, "20 =")
        self.say("בבינארי : 20 הוא 10100. הביט העליון\nהוא 16, והביטים שאחריו הם r = 4.", FadeIn(name20),
                 FadeIn(row20))
        out20 = M("= 8", 34, C.GREEN).next_to(row20, RIGHT, buff=0.5)
        with self.beat("הביט העליון עובר לסוף והופך ל-0 :\nמקבלים 01000, כלומר 2r = 8, השורד."):
            self.rotate_bits(row20, name20, 20)
            self.play(FadeIn(out20), run_time=0.5)
        name41, row41 = self.bit_row("101001", -0.5, "41 =")
        out41 = M("= 18", 34, C.GREEN).next_to(row41, RIGHT, buff=0.5)
        with self.beat("ועם 41, כלומר 101001 : מקבלים 010010,\nכלומר 18, כמו בסימולציה."):
            self.play(FadeIn(name41), FadeIn(row41), run_time=0.6)
            self.rotate_bits(row41, name41, 41)
            self.play(FadeIn(out41), run_time=0.5)
        self.say("במספור מ-0 הביט מגיע לסוף כ-0.\nבמספור מ-1 הוא נשאר 1, והשורד הוא 2r + 1.")
        hw = M("leading-one detector + shift", 30, C.MUTED).move_to(DOWN * 1.9)
        self.say("בחומרה זה גלאי של ה-1 העליון והזזה :\nתשובה במחזור שעון אחד, לכל N.", FadeIn(hw))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "rounds", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד : 20 אנשים במעגל,\nצעד אחרי צעד.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי 10 צעדים, סוף סיבוב 1 :\nנשארו רק הזוגיים."),
            (2, "אחרי 15 צעדים, סוף סיבוב 2 :\nנשארו 0, 4, 8, 12 ו-16."),
            (3, "ואחרי 19 צעדים : השורד הוא אדם 8."),
        ])
        self.fade_all()


class ChapterB(JScene):
    def construct(self):
        self.chapter_card("סעיף ב", "אחד נשאר, שניים יוצאים",
                          "סעיף ב : אדם 0 נשאר, ו-1 ו-2 יוצאים,\nוכך הלאה. השורד הוא F₃(N).")
        self.seven()
        self.table()
        self.zeros()
        self.thirty()
        self.base3()
        self.box()

    def seven(self):
        ring = Ring(7, center=UP * 0.45, radius=1.9, dot=0.36, size=30)
        self.play(FadeIn(ring), run_time=0.8)
        caps = ["שבעה אנשים. אדם 0 נשאר,\nואנשים 1 ו-2 יוצאים.",
                "אדם 3 נשאר, ו-4 ו-5 יוצאים.",
                "אדם 6 נשאר, ו-0 ו-3 יוצאים.\nהשורד הוא 6 : F₃(7) = 6."]
        for (stays, leaves), cap in zip(q0016.run(7, 3)[0], caps):
            with self.beat(cap):
                self.slow_step(ring, stays, leaves)
                if cap is caps[-1]:
                    self.play(self.win(ring, 6), run_time=0.5)
        self.fade_all()

    def chain(self, start, blocks, x0, y0):
        """The rows of one chain: N from each zero point to the next, every second N."""
        dx, dy = 0.62, 0.9
        rows = VGroup()
        for r, (a, b) in enumerate(blocks):
            row = VGroup()
            for j, n in enumerate(range(a, b + 1, 2)):
                x, y = x0 + j * dx, y0 - r * dy
                f = F3[n - 1]
                row.add(VGroup(M(str(n), 17, C.MUTED).move_to([x, y + 0.24, 0]),
                               M(str(f), 26, C.AMBER if f == 0 else C.WHITE).move_to([x, y - 0.12, 0])))
            rows.add(row)
        return rows

    def table(self):
        odd = self.chain(1, [(1, 1), (3, 7), (9, 25), (27, 29)], -6.3, 2.35)
        even = self.chain(2, [(2, 4), (6, 16), (18, 30)], 1.0, 2.35)
        h_odd = he("N אי-זוגי", 32, C.BLUE).next_to(odd, UP, buff=0.3).align_to(odd, LEFT)
        h_even = he("N זוגי", 32, C.ORANGE).next_to(even, UP, buff=0.3).align_to(even, LEFT)
        h_even.align_to(h_odd, UP)
        self.say("השורד לכל N עד 30. צעד מוריד שניים,\nולכן מסדרים לפי זוגיות : שתי שרשראות.",
                 FadeIn(h_odd), FadeIn(h_even),
                 LaggedStart(*[FadeIn(r, shift=0.15 * RIGHT) for r in [*odd, *even]], lag_ratio=0.3), run_time=2.4)
        zs = VGroup(*[c for r in [*odd, *even] for c in r if F3[int(c[0].text) - 1] == 0])
        rings = VGroup(*[SurroundingRectangle(z, color=C.AMBER, buff=0.06, corner_radius=0.08) for z in zs])
        self.say("השורד נופל לאפס ב-1, 3, 9 ו-27,\nובזוגיים ב-2, 6 ו-18.", Create(rings))
        self.say("ובין שתי נקודות אפס בשרשרת, השורד\nעולה ב-3 בכל צעד של 2.")
        self.say("מה שהשתנה : שתי שרשראות, נקודות אפס\nב-3ᵐ וב-2 · 3ᵐ, ועלייה של 3.")
        self.fade_all()

    def zeros(self):
        ring = Ring(9, center=[-3.3, 0.45, 0], radius=2.0, dot=0.34, size=30)
        rule = TX(r"F_3(3k) = 3\,F_3(k)", size=44).move_to([3.3, 2.3, 0])
        self.say("סיבוב שלם על כפולה של 3 משאיר את\nהכפולות של 3, והספירה חוזרת לאדם 0.", FadeIn(ring), FadeIn(rule))
        with self.beat("עם 9 אנשים : נשארים 0, 3 ו-6,\nושוב מאדם 0. ואז נשאר רק 0."):
            steps = q0016.run(9, 3)[0]
            self.fast_steps(ring, steps[:3], t=0.5)
            self.play(*ring.to(0), run_time=0.4)
            self.fast_steps(ring, steps[3:], t=0.5)
            self.play(*ring.to(0), self.win(ring, 0), run_time=0.5)
        zs = TX(r"F_3(1) = F_3(2) = 0 \;\Rightarrow\; F_3(3^m) = F_3(2 \cdot 3^m) = 0", size=34, color=C.AMBER)
        zs.move_to([2.6, 1.0, 0])
        self.say("ומכיוון ש-F₃(1) = F₃(2) = 0, בכל נקודת\nאפס, 3ᵐ או 2 · 3ᵐ, מי שמתחיל שורד.",
                 FadeIn(zs))
        self.fade_all()

    def thirty(self):
        ring = Ring(30, center=[-3.2, 0.35, 0], radius=2.4, dot=0.2, size=17)
        split = TX(r"30 = 18 + 2 \cdot 6", size=44).move_to([3.4, 2.4, 0])
        self.say("אותו רעיון עם 30 אנשים. נקודת האפס\nהזוגית שמתחת ל-30 היא 18.", FadeIn(ring), FadeIn(split))
        with self.beat("כל צעד מוציא שניים. אחרי 6 צעדים\nנשארים בדיוק 18 : נקודת אפס."):
            self.fast_steps(ring, STEPS30[:6], t=0.55)
        stop = Circle(radius=ring.d + 0.13, stroke_color=C.AMBER, stroke_width=6).move_to(ring.pos(18))
        lab = M("18", 26, C.AMBER).move_to(ring.pos(18, ring.R + ring.d + 0.42))
        rule = TX(r"F_3(30) = 3 \cdot 6 = 18", size=44, color=C.AMBER).move_to([3.4, 1.2, 0])
        self.say("והספירה מתחילה מאדם 18, שלושה\nלכל צעד : 3 · 6 = 18. הוא השורד.",
                 *ring.to(18), Create(stop), FadeIn(lab), FadeIn(rule))
        with self.beat("נמשיך עד הסוף : כולם יוצאים,\nחוץ מאדם 18."):
            self.play(FadeOut(stop), run_time=0.3)
            self.fast_steps(ring, STEPS30[6:], t=0.3)
            self.play(self.win(ring, 18), run_time=0.5)
        gen = TX(r"F_3(N) = 3j = \tfrac{3}{2}\,(N - M)", size=44, color=C.AMBER).move_to([3.4, -0.1, 0])
        self.say("כללית : מ-N יורדים ב-j צעדים לנקודת\nהאפס M באותה זוגיות, והשורד הוא 3j.", FadeIn(gen))
        chk = TX(r"21:\ M = 9,\ \ \tfrac{3}{2} \cdot 12 = 18", size=38).move_to([3.4, -1.3, 0])
        self.say("זהירות מהשרשרת : 21 אי-זוגי, ולכן M = 9\nולא 18, והשורד שוב 18.", FadeIn(chk))
        self.fade_all()


    def base3(self):
        r30 = TX(r"30:\quad 15 = 120_3,\quad 120_3 - 100_3 = 20_3 \;\to\; 200_3 = 18", size=38).move_to(UP * 1.6)
        r21 = TX(r"21:\quad 10 = 101_3,\quad 101_3 - 11_3 = 20_3 \;\to\; 200_3 = 18", size=38).move_to(UP * 0.2)
        self.say("גם כאן יש כלל בספרות, בבסיס 3 : כותבים\nאת חצי N, מחסרים 10…0 או 11…1, ומוסיפים 0.")
        self.say("עם 30 : 15 הוא 120 בבסיס 3, פחות 100\nנותן 20, ועם 0 בסוף 200, כלומר 18.", FadeIn(r30))
        self.say("עם 21, אי-זוגי : 10 הוא 101, פחות 11\nנותן 20, ושוב 200, כלומר 18.", FadeIn(r21))
        self.fade_all()

    def box(self):
        view = BoxView(QID, "rounds3", height=5.6).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד, עם הכלל של סעיף ב :\nשלושים אנשים במעגל.", FadeIn(view))
        self.box_beat(view, [
            (1, "אחרי 10 צעדים נשארו רק הכפולות\nשל 3, והספירה שוב מאדם 0."),
            (2, "אחרי 14 צעדים נשארו 18 ו-27."),
            (3, "ובצעד ה-15 אדם 27 יוצא :\nהשורד הוא אדם 18."),
        ])
        self.fade_all()


class ChapterC(JScene):
    def construct(self):
        self.chapter_card("סעיף ג", "בונוס : אחד נשאר, L − 1 יוצאים",
                          "סעיף ג, בונוס : אחד נשאר ו-L − 1 יוצאים,\nלכל L. נוסחה אחת לכל המקרים.")
        rec = TX(r"F_L(N) = \bigl(F_L(N - L + 1) + L\bigr) \bmod N", size=40).move_to(UP * 2.6)
        self.say("צעד אחד מוריד L − 1 אנשים, ומזיז\nאת המספור ב-L.", FadeIn(rec))
        r = TX(r"r = 1 + \bigl((N - 1) \bmod (L - 1)\bigr)", size=40).move_to(UP * 1.45)
        self.say("לכן יש L − 1 שרשראות, לפי השארית\nשל N בחלוקה ב-L − 1.", FadeIn(r))
        z = TX(r"F_L(N) = 0 \iff N = b \cdot L^m,\ \ 1 \le b < L", size=40).move_to(UP * 0.3)
        self.say("נקודות האפס הן b · Lᵐ עם 1 ≤ b < L,\nוביניהן השורד עולה ב-L בכל צעד.", FadeIn(z))
        self.say("והבסיס : עם פחות מ-L אנשים, אדם 0\nנשאר וכל השאר יוצאים מיד.")
        f = TX(r"F_L(N) = \frac{L}{L - 1}\,(N - M), \qquad M = r \cdot L^{\lfloor \log_L (N / r) \rfloor}",
               size=40, color=C.AMBER).move_to(DOWN * 1.05)
        self.say("הנוסחה : M היא נקודת האפס של השרשרת\nשמתחת ל-N, והשורד הוא L/(L − 1) · (N − M).",
                 FadeIn(f))
        self.fade_all()
        l2 = TX(r"L = 2:\quad r = 1,\ \ M = 2^m,\ \ F = 2\,(N - 2^m)", size=40).move_to(UP * 2.0)
        self.say("עם L = 2 : שרשרת אחת, M = 2ᵐ,\nו-F = 2(N − 2ᵐ). זה סעיף א.", FadeIn(l2))
        l3 = TX(r"L = 3:\quad r \in \{1, 2\},\ \ F = \tfrac{3}{2}\,(N - M)", size=40).move_to(UP * 0.7)
        self.say("עם L = 3 : שתי שרשראות לפי הזוגיות,\nו-F = 3/2 · (N − M). זה סעיף ב.", FadeIn(l3))
        self.say("עם L = 4 יש שלוש שרשראות, לפי\nהשארית של N בחלוקה ב-3.")
        l4 = TX(r"L = 4,\ N = 20:\quad r = 2,\ \ M = 8,\ \ F_4(20) = \tfrac{4}{3} \cdot 12 = 16", size=40,
                color=C.AMBER).move_to(DOWN * 0.6)
        self.say("ועם L = 4 ו-N = 20 : r = 2 ו-M = 8,\nוהשורד הוא 4/3 · 12 = 16.", FadeIn(l4))
        self.fade_all()


class Closing(JScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"F(N) = 2\,(N - 2^m)", size=40)),
                           ("ב", TX(r"F_3(N) = \tfrac{3}{2}\,(N - M)", size=40)),
                           ("ג", TX(r"F_L(N) = \tfrac{L}{L - 1}\,(N - M)", size=40))],
                     ["לסיכום : יורדים לנקודת אפס, שבה מי\nשמתחיל שורד, וסופרים כמה צעדים עברו.",
                      "נסו כל N וכל L בתיבה שבעמוד\nשל שאלה 0016 באתר."])
