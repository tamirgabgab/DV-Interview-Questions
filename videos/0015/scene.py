"""The tutorial video of question 0015, two children, at least one a boy (script: script.md).

Render with `python videos/render.py 0015` (see VIDEOS.md). The question has no code, so
every part is a proof step by step (the owner, 2026-10-31): one equation line at a time,
its caption saying why it holds, the earlier lines dimmed and the key numbers in amber.
Part א draws the four ordered families (the page has no box for it) and crosses out two
girls: 1/3. Part ב draws the 14 × 14 grid of (sex, weekday) pairs and counts the cross of
"a boy born on Tuesday" with inclusion-exclusion: 27 families, 13 with two boys, 13/27;
then the page's tuesday box counts the same cross in its four steps, and its table puts
the three kinds of information side by side. Part ג derives the general formula through
the complements, checks it against 1/3 and 13/27 and its limit p^(C−1), and shows the
page's probability box (the square of two children, and the curve against q).
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import MIN_BOX_SCALE, C, BoxView, DVQScene, M, X, he  # noqa: E402

QID = 15
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – לפחות אחד בן"),
    ("ChapterB", "סעיף ב – בן שנולד ביום שלישי"),
    ("ChapterC", "סעיף ג – הנוסחה הכללית"),
    ("Closing", "סיכום"),
]

# The page's boxes: the tuesday box (box 0, part ב) and the probability box (box 1, part
# ג). "tue": the box opens on step 1 (the first child's row lit); picture k is step k + 1,
# a click on "the next step" each, its scrubber and legend hidden and its width 500 CSS
# px, so the 14 × 14 grid fits the frame at its page size. "infos": the box's table of the
# three kinds of information. "square": the probability box on the page's values (p = 1/2,
# q = 1/7, C = 2), its summary and the square of two children. "curve": the summary and
# the curve against q, on the page's values and then with three children (the slider of C
# set to 3); the square is hidden there, so nothing moves when it gives way to a line.
BOXES = {
    "tue": {"box": 0, "width": 500, "region": [".ex-play-row", ".tu-step", ".tu-grid"],
            "hide": [".ex-scrubwrap", ".viz-legend", ".ex-controls:not(.ex-play-row)"],
            "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "infos": {"box": 0, "width": 470, "region": [".tu-infos"], "hide": [".viz-legend"],
              "steps": [[]]},
    "square": {"box": 1, "region": [".ex-summary", ".prob-grid"],
               "hide": [".prob-grid .viz-legend"], "steps": [[]]},
    "curve": {"box": 1, "region": [".ex-controls", ".ex-summary", ".prob-chart"],
              "hide": [".prob-grid", ".ex-reset"],
              "steps": [[], [["fill", ".ex-C", "3"]]]},
}

F = Fraction
HALF = F(1, 2)


def answer(C_: int, p: Fraction, q: Fraction) -> Fraction:
    """The page's formula: P(all C children are boys | one at least is a boy with the trait)."""
    return p ** C_ * (1 - (1 - q) ** C_) / (1 - (1 - p * q) ** C_)


# Every number the captions say, checked exactly.
KINDS = [(s, d) for s in "BG" for d in range(7)]
CROSS = [(a, b) for a in KINDS for b in KINDS if a == ("B", 2) or b == ("B", 2)]
TWO_BOYS = [(a, b) for a, b in CROSS if a[0] == b[0] == "B"]
assert (len(KINDS) ** 2, len(CROSS), len(TWO_BOYS)) == (196, 27, 13)
assert F(1, 4) / F(3, 4) == F(1, 3)
assert 1 - F(6, 7) ** 2 == F(13, 49) and 1 - F(13, 14) ** 2 == F(27, 196)
assert F(13, 49) * F(1, 4) / F(27, 196) == F(13, 27)
assert answer(2, HALF, F(1)) == F(1, 3) and answer(2, HALF, F(1, 7)) == F(13, 27)
assert answer(2, HALF, F(1, 2)) == F(3, 7) and answer(2, HALF, F(1, 365)) == F(729, 1459)
assert answer(3, HALF, F(1, 7)) == F(127, 547) and round(float(F(127, 547)), 4) == 0.2322
assert round(float(F(13, 27)), 4) == 0.4815

RLM = "‏"
DIM = 0.35            # the opacity of a proof's earlier lines


# --------------------------------------------------------------------------------------
# Math from text pieces (no LaTeX here): fractions, powers, equation rows
# --------------------------------------------------------------------------------------


def frac(a, b, size: float = 38, color: str | None = None) -> VGroup:
    """a over b, a rule between them."""
    n = a if isinstance(a, Mobject) else X(a, size, color)
    d = b if isinstance(b, Mobject) else X(b, size, color)
    w = max(n.width, d.width) + 0.14
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=2.6, color=color or C.WHITE)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.1)


def pw(base, exp: str, size: float = 34, color: str | None = None) -> VGroup:
    """base to the power exp, the exponent small and raised."""
    b = base if isinstance(base, Mobject) else X(base, size, color)
    e = X(exp, size * 0.62, color)
    e.next_to(b, RIGHT, buff=0.04).align_to(b, UP).shift(UP * 0.12)
    return VGroup(b, e)


def fade_to(group: Mobject, op: float) -> list:
    """Animations taking every part of a Group (shapes and labels) to opacity op."""
    return [m.animate.set_opacity(op) for m in group.submobjects]


def formula(size: float = 40, color: str | None = None) -> VGroup:
    """The answer of part ג: p^C (1 − (1 − q)^C) over 1 − (1 − pq)^C."""
    top = eq(pw(X("p", size, color), "C", size, color), X("(1 −", size, color),
             pw(X("(1 − q)", size, color), "C", size, color), X(")", size, color), buff=0.14)
    bottom = eq(X("1 −", size, color), pw(X("(1 − pq)", size, color), "C", size, color), buff=0.14)
    return frac(top, bottom, color=color)


def eq(*parts, size: float = 38, buff: float = 0.16) -> VGroup:
    """A row of math: a str is text, (str, colour) coloured text, a Mobject itself."""
    mobs = []
    for p in parts:
        if isinstance(p, str):
            mobs.append(X(p, size))
        elif isinstance(p, tuple):
            mobs.append(X(p[0], size, p[1]))
        else:
            mobs.append(p)
    return VGroup(*mobs).arrange(RIGHT, buff=buff)


class ProofScene(DVQScene):
    """The proof beat: a column of equation lines, one at a time, the earlier ones dimmed."""

    def proof_start(self, corner: np.ndarray, gap: float = 0.34):
        self.proof_lines = VGroup()
        self.proof_corner = corner
        self.proof_gap = gap

    def proof_line(self, line: Mobject, caption: str, *anims, dim: bool = True,
                   beside: bool = False, **kw):
        if beside:          # the line goes on at the right of the last one (a last "= x")
            line.next_to(self.proof_lines[-1], RIGHT, buff=0.25)
        elif len(self.proof_lines):
            line.next_to(self.proof_lines[-1], DOWN, buff=self.proof_gap, aligned_edge=LEFT)
        else:
            line.move_to(self.proof_corner, aligned_edge=UL)
        olds = [m.animate.set_opacity(DIM) for m in self.proof_lines] if dim else []
        self.say(caption, *olds, FadeIn(line, shift=0.15 * UP), *anims, **kw)
        self.proof_lines.add(line)
        return line

    def check_box(self, view: BoxView):
        if view.css_scale() < MIN_BOX_SCALE:
            self.problems.append(f"box at {view.css_scale():.2f} of its page size "
                                 f"(at least {MIN_BOX_SCALE})")


# --------------------------------------------------------------------------------------
# Part א: the four ordered families
# --------------------------------------------------------------------------------------

SEX = {"B": "בן", "G": "בת"}


class Families(Group):
    """The four families as a 2 × 2 grid: the first child the rows (a boy on top), the
    second child the columns (a boy on the right), as on the page."""

    def __init__(self, w: float = 2.7, h: float = 1.3):
        super().__init__()
        self.cells = {}
        for r, s1 in enumerate("BG"):
            for c, s2 in enumerate("BG"):
                box = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=C.FAINT,
                                       stroke_width=3, fill_color=C.NAVY_LIGHT, fill_opacity=1)
                box.move_to([-(c * (w + 0.18)), -r * (h + 0.18), 0])
                name = he(f"{SEX[s1]}, {SEX[s2]}", 38, C.WHITE, 500).move_to(box).shift(UP * 0.18)
                prob = M("1/4", 26, C.MUTED).next_to(name, DOWN, buff=0.12)
                cell = Group(box, name, prob)
                self.cells[s1 + s2] = cell
                self.add(cell)
        self.col_heads = Group(he("בן", 34, C.AMBER, 600).next_to(self.cells["BB"], UP, buff=0.2),
                               he("בת", 34, C.AMBER, 600).next_to(self.cells["BG"], UP, buff=0.2))
        self.row_heads = Group(he("בן", 34, C.AMBER, 600).next_to(self.cells["BB"], RIGHT, buff=0.25),
                               he("בת", 34, C.AMBER, 600).next_to(self.cells["GB"], RIGHT, buff=0.25))
        self.col_title = he("הילד השני", 28, C.MUTED).next_to(self.col_heads, UP, buff=0.18)
        self.row_title = he("הילד הראשון", 28, C.MUTED).next_to(self.row_heads, RIGHT, buff=0.3)
        self.add(self.col_heads, self.row_heads, self.col_title, self.row_title)

    def box(self, key: str) -> RoundedRectangle:
        return self.cells[key][0]


# --------------------------------------------------------------------------------------
# Part ב: the 14 × 14 grid
# --------------------------------------------------------------------------------------

LETTER = "אבגדהוש"
TUE = 2


class Grid14(Group):
    """196 families: the first child the rows (boys Sunday to Saturday, then girls), the
    second child the columns, right to left as on the page (a boy's columns on the right).
    A kind is 0..6 a boy born on day 0..6, 7..13 a girl."""

    def __init__(self, side: float = 0.29, gap: float = 0.05):
        super().__init__()
        p = side + gap
        self.p = p
        self.sq = {}
        squares = VGroup()
        for c1 in range(14):
            for c2 in range(14):
                s = RoundedRectangle(width=side, height=side, corner_radius=0.04,
                                     stroke_color=C.FAINT, stroke_width=1.5,
                                     fill_color=C.NAVY_LIGHT, fill_opacity=1)
                s.move_to([-c2 * p - (0.12 if c2 >= 7 else 0), -c1 * p - (0.12 if c1 >= 7 else 0), 0])
                self.sq[(c1, c2)] = s
                squares.add(s)
        self.squares = squares
        self.add(squares)
        letters = Group()
        for c in range(14):
            color = C.AMBER if c == TUE else C.MUTED
            top = he(LETTER[c % 7], 20, color, 600).next_to(self.sq[(0, c)], UP, buff=0.1)
            side_l = he(LETTER[c % 7], 20, color, 600).next_to(self.sq[(c, 0)], RIGHT, buff=0.12)
            letters.add(top, side_l)
        self.letters = letters
        self.add(letters)
        self.heads = Group(
            he("בן", 28, C.WHITE, 600).next_to(Group(self.sq[(0, 0)], self.sq[(0, 6)]), UP, buff=0.42),
            he("בת", 28, C.WHITE, 600).next_to(Group(self.sq[(0, 7)], self.sq[(0, 13)]), UP, buff=0.42),
            he("בן", 28, C.WHITE, 600).next_to(Group(self.sq[(0, 0)], self.sq[(6, 0)]), RIGHT, buff=0.5),
            he("בת", 28, C.WHITE, 600).next_to(Group(self.sq[(7, 0)], self.sq[(13, 0)]), RIGHT, buff=0.5))
        self.add(self.heads)

    def row(self, c1: int) -> VGroup:
        return VGroup(*[self.sq[(c1, c2)] for c2 in range(14)])

    def col(self, c2: int) -> VGroup:
        return VGroup(*[self.sq[(c1, c2)] for c1 in range(14)])

    def cells(self, keys) -> VGroup:
        return VGroup(*[self.sq[k] for k in keys])

    def quad(self) -> VMobject:
        """The dashed square round the families with two boys (rows and columns 0..6)."""
        g = VGroup(*[self.sq[(a, b)] for a in range(7) for b in range(7)])
        r = Rectangle(width=g.width + 0.12, height=g.height + 0.12, stroke_color=C.WHITE,
                      stroke_width=3).move_to(g)
        return DashedVMobject(r, num_dashes=40)


def kind_of(k: tuple) -> int:
    s, d = k
    return d if s == "B" else 7 + d


# --------------------------------------------------------------------------------------
# The scenes
# --------------------------------------------------------------------------------------


class Opening(ProofScene):
    def construct(self):
        self.opening(QID, "סטודנט", "שני ילדים, ולפחות אחד מהם בן",
                     ["לפחות אחד בן", "בן שנולד ביום שלישי", "הנוסחה הכללית"],
                     ["שאלה 0015 : שני ילדים, ולפחות אחד בן.\nשאלה ברמת סטודנט.",
                      "שלושה סעיפים, וכולם הוכחה צעד אחרי\nצעד : אין כאן קוד, רק ספירה."])
        self.fade_all()
        kids = Group()
        for _ in range(2):
            c = Circle(radius=0.75, stroke_color=C.MUTED, stroke_width=4, fill_color=C.NAVY_LIGHT,
                       fill_opacity=1)
            c.add(M("?", 60, C.AMBER).move_to(c))
            kids.add(c)
        kids.arrange(RIGHT, buff=1.0).move_to(UP * 1.3)
        yes = he("כן", 40, C.GREEN, 700)
        yes_chip = Group(RoundedRectangle(width=yes.width + 0.6, height=yes.height + 0.35,
                                          corner_radius=0.2, stroke_color=C.GREEN, stroke_width=3,
                                          fill_color=C.NAVY_DARK, fill_opacity=1), yes)
        yes_chip.next_to(kids, DOWN, buff=0.6)
        self.say("ליוסי יש שני ילדים. שאלנו אותו : האם\nלפחות אחד מהם בן? והוא ענה כן.",
                 FadeIn(kids, lag_ratio=0.3), run_time=1.4)
        self.say("מה ההסתברות ששני הילדים בנים?", FadeIn(yes_chip, shift=0.2 * UP))
        rules = VGroup(eq("P(boy) = P(girl) =", ("1/2", C.AMBER), size=34),
                       eq("P(any weekday) =", ("1/7", C.AMBER), size=34)) \
            .arrange(DOWN, buff=0.35).next_to(yes_chip, DOWN, buff=0.6)
        self.say("ההנחות : כל ילד בן או בת בחצי, וכל\nיום בשבוע שווה הסתברות, בלי תלות.",
                 FadeIn(rules, lag_ratio=0.3))
        self.fade_all()


class ChapterA(ProofScene):
    def construct(self):
        self.chapter_card("סעיף א", "לפחות אחד בן",
                          "מה ההסתברות ששני הילדים בנים?\nהתשובה המהירה היא חצי. האם היא נכונה?")
        guess = eq("P = ", ("1/2 ?", C.RED), size=52).move_to(UP * 1.0)
        self.say("הניחוש : יש בן אחד, והילד השני הוא\nבן או בת בחצי. אז חצי?", FadeIn(guess))
        self.play(FadeOut(guess), run_time=0.6)

        fam = Families().scale(1.15).move_to(UP * 0.85)
        self.say("מסדרים את הילדים לפי סדר הלידה :\nארבע משפחות, כל אחת בהסתברות 1/4.",
                 FadeIn(fam, lag_ratio=0.1), run_time=1.6)
        rings = VGroup(*[SurroundingRectangle(fam.box(k), color=C.ORANGE, buff=0.06,
                                              corner_radius=0.16, stroke_width=5) for k in ("BG", "GB")])
        self.say("בן ובת, ובת ובן, הן שתי משפחות\nשונות, ולא תוצאה אחת.",
                 Create(rings))
        self.play(FadeOut(rings), run_time=0.5)
        gg = fam.box("GG")
        strike = Line(gg.get_corner(DL) + 0.1 * UR, gg.get_corner(UR) - 0.1 * UR,
                      stroke_color=C.RED, stroke_width=6)
        self.say("התשובה כן פוסלת רק משפחה אחת :\nשתי בנות.",
                 Create(strike), *fade_to(fam.cells["GG"], 0.3))
        cond = [fam.box(k) for k in ("BB", "BG", "GB")]
        self.say("נשארות שלוש משפחות שוות הסתברות,\nבהסתברות כוללת של 3/4.",
                 *[b.animate.set_stroke(C.BLUE, width=5) for b in cond])
        self.say("רק באחת מהן שני בנים :\nבן ובן, בהסתברות 1/4.",
                 fam.box("BB").animate.set_stroke(C.GREEN, width=6).set_fill(C.GREEN, opacity=0.28))

        # The proof: the grid to the left, the lines to the right.
        self.play(Group(fam, strike).animate.scale(0.68).to_edge(LEFT, buff=0.5).shift(UP * 0.35),
                  run_time=1.0)
        self.proof_start(np.array([0.3, 3.3, 0]))
        self.proof_line(VGroup(eq(("A", C.GREEN), "= both boys", size=36),
                               eq(("B", C.BLUE), "= at least one boy", size=36))
                        .arrange(DOWN, buff=0.2, aligned_edge=LEFT),
                        "נסמן : A הוא שני הילדים בנים,\nו-B הוא לפחות אחד בן.")
        self.proof_line(eq("A ∩ B = A", size=40),
                        "כל משפחה עם שני בנים מקיימת גם את B,\nולכן החיתוך הוא A עצמו.")
        self.proof_line(eq("P(A | B) =", frac("P(A ∩ B)", "P(B)", 40), size=40),
                        "ההסתברות המותנית : ההסתברות של\nהחיתוך, חלקי ההסתברות של התנאי.")
        self.proof_line(eq("=", frac("1/4", "3/4", 40), size=40),
                        "מציבים : 1/4 בשביל שני בנים,\nו-3/4 בשביל שלוש המשפחות שנשארו.")
        self.proof_line(eq("=", frac(X("1", 40, C.AMBER), X("3", 40, C.AMBER), color=C.AMBER), size=40),
                        "ומקבלים שליש, ולא חצי.", beside=True)
        self.fade_all()

        # Where the guess went wrong: "the elder is a boy" names one child.
        fam2 = Families().scale(1.15).move_to(UP * 0.85)
        self.say("איפה הניחוש טעה? \"לפחות אחד בן\"\nלא אומר איזה מהשניים הוא הבן.", FadeIn(fam2))
        elder = SurroundingRectangle(Group(fam2.cells["BB"], fam2.cells["BG"]), color=C.AMBER,
                                     buff=0.1, corner_radius=0.18, stroke_width=6)
        self.say("אם המידע היה \"הבכור הוא בן\", נשארת\nרק השורה העליונה : בן ובן, ובן ובת.",
                 Create(elder), *fade_to(fam2.cells["GB"], 0.3), *fade_to(fam2.cells["GG"], 0.3))
        half = eq("P =", frac("1", "2", color=C.AMBER), size=40).next_to(fam2, LEFT, buff=0.5)
        self.say("אז התשובה הייתה חצי : המידע\nמצביע על ילד מסוים.", FadeIn(half))
        self.play(FadeOut(elder), FadeOut(half), *fade_to(fam2.cells["GB"], 1), run_time=0.8)
        both = [fam2.box(k) for k in ("BG", "GB")]
        self.say("ב\"לפחות אחד\" הבן יכול להיות כל אחד :\nשתי משפחות של בן ובת, מול אחת של שני בנים.",
                 *[b.animate.set_stroke(C.BLUE, width=5) for b in both],
                 fam2.box("BB").animate.set_stroke(C.GREEN, width=6))
        self.say("מלכודת : לספור בן ובת כתוצאה אחת.\nהיא קורית בשני סדרים, ולכן ההסתברות שלה חצי.")
        self.fade_all()


class ChapterB(ProofScene):
    def construct(self):
        self.chapter_card("סעיף ב", "בן שנולד ביום שלישי",
                          "עכשיו יוסי עונה כן לשאלה : יש לך בן\nשנולד ביום שלישי? מה ההסתברות עכשיו?")
        ask = eq("P( both boys  |  a boy born on Tuesday ) =", ("?", C.AMBER), size=40).move_to(UP * 0.9)
        self.say("נראה שיום הלידה לא אמור לשנות כלום.\nבואו נספור.", FadeIn(ask))
        self.play(FadeOut(ask), run_time=0.5)

        # The 14 kinds of a child.
        strip = Group()
        for c in range(14):
            boy = c < 7
            s = RoundedRectangle(width=0.76, height=0.76, corner_radius=0.08,
                                 stroke_color=C.AMBER if c == TUE else (C.BLUE if boy else C.ORANGE),
                                 stroke_width=4 if c == TUE else 2.5, fill_color=C.NAVY_LIGHT,
                                 fill_opacity=1)
            strip.add(Group(s, he(LETTER[c % 7], 30, C.AMBER if c == TUE else C.WHITE, 600).move_to(s)))
        strip.arrange(LEFT, buff=0.1)
        for s in strip[7:]:
            s.shift(LEFT * 0.35)
        strip.move_to(UP * 1.2)
        heads = Group(he("בן", 34, C.BLUE, 600).next_to(Group(*strip[:7]), UP, buff=0.3),
                      he("בת", 34, C.ORANGE, 600).next_to(Group(*strip[7:]), UP, buff=0.3))
        self.say("כל ילד הוא אחד מ-14 סוגים שווי הסתברות :\nבן או בת, כפול שבעה ימים.",
                 FadeIn(strip, lag_ratio=0.06), FadeIn(heads), run_time=1.8)
        tue = M("1/14", 34, C.AMBER).next_to(strip[TUE], DOWN, buff=0.3)
        self.say("בן שנולד ביום שלישי הוא סוג אחד מהם,\nבהסתברות 1/14.", FadeIn(tue))
        self.fade_all()

        grid = Grid14()
        grid.move_to([-3.2, 0.5, 0])
        self.say("לשני ילדים יש 14 × 14 = 196 זוגות\nמסודרים, כל אחד בהסתברות 1/196.",
                 FadeIn(grid, lag_ratio=0.002), run_time=2.0)
        marks = VGroup(*[SurroundingRectangle(m, color=C.AMBER, buff=0.06, corner_radius=0.06,
                                              stroke_width=3) for m in grid.letters[TUE * 2:TUE * 2 + 2]])
        self.say("השורות הן הילד הראשון, והעמודות השני.\nהאות ג היא יום שלישי.", Create(marks))
        self.play(FadeOut(marks), run_time=0.4)

        row = grid.row(TUE)
        self.proof_start(np.array([0.6, 3.4, 0]), gap=0.3)
        self.proof_line(eq("first child:", ("14", C.AMBER), size=36),
                        "הילד הראשון בן מיום שלישי : זו שורה\nאחת של 14 זוגות, השני הוא כל סוג.",
                        row.animate.set_fill(C.AMBER, opacity=0.55))
        col = grid.col(TUE)
        self.proof_line(eq("second child:", ("14", C.AMBER), size=36),
                        "גם הילד השני יכול להיות בן מיום שלישי :\nעמודה אחת, עוד 14 זוגות.",
                        col.animate.set_fill(C.AMBER, opacity=0.55))
        both = Circle(radius=0.12, stroke_color=C.RED, stroke_width=5).move_to(grid.sq[(TUE, TUE)])
        self.proof_line(eq("counted twice:", ("1", C.RED), size=36),
                        "המשבצת שבהצטלבות, שני בנים מיום שלישי,\nנספרה פעמיים. מורידים אותה פעם אחת.",
                        Create(both))
        cross = grid.cells(CROSS_KEYS)
        self.proof_line(eq("|T| = 14 + 14 − 1 =", ("27", C.AMBER), size=38),
                        "לכן התנאי מתקיים ב-27 זוגות,\nולא ב-28.",
                        cross.animate.set_fill(C.BLUE, opacity=0.6))
        quad = grid.quad()
        hit = grid.cells(HIT_KEYS)
        self.proof_line(eq("|A ∩ T| = 7 + 7 − 1 =", ("13", C.GREEN), size=38),
                        "מתוכם, שני בנים : הריבוע המקווקו.\nשבעה בשורה, שבעה בעמודה, פחות הכפולה.",
                        Create(quad), hit.animate.set_fill(C.GREEN, opacity=0.75))
        self.proof_line(eq("P(A | T) =", frac("13", "27", color=C.AMBER), "≈ 0.481", size=36),
                        "כל הזוגות שווי הסתברות, ולכן ההסתברות\nהיא 13 חלקי 27, בערך 0.481.")
        self.say("כמעט חצי, ורחוק מהשליש של סעיף א.\nהמידע הספציפי שינה את התשובה.")
        self.say("בלי ההורדה של המשבצת הכפולה היינו\nמקבלים 14 חלקי 28, כלומר חצי. וזו טעות.",
                 Indicate(both, color=C.RED, scale_factor=1.6))
        self.say("למה? יום שלישי הוא מידע כמעט על ילד\nמסוים, כמו \"הבכור הוא בן\", שנותן חצי.")
        self.play(*[FadeOut(m) for m in self.proof_lines], run_time=0.7)

        # The same through Bayes, read off the grid.
        self.proof_start(np.array([0.6, 3.4, 0]), gap=0.42)
        self.proof_line(eq("P(A) =", frac("49", "196", 34), "=", frac("1", "4", 34), size=34),
                        "אותה תשובה דרך בייס. הריבוע של שני\nבנים : 49 משבצות מתוך 196, רבע.",
                        Indicate(quad, color=C.WHITE, scale_factor=1.03))
        self.proof_line(eq("P(T | A) = 1 −", pw(X("(6/7)", 34), "2", 34), "=", frac("13", "49", 34), size=34),
                        "בתוך הריבוע, אף בן לא נולד ביום\nשלישי בהסתברות (6/7)². המשלים 13/49.")
        self.proof_line(eq("P(T) = 1 −", pw(X("(13/14)", 34), "2", 34), "=", frac("27", "196", 34), size=34),
                        "כל ילד הוא בן מיום שלישי ב-1/14,\nולכן התנאי קורה ב-1 פחות (13/14)².")
        self.proof_line(eq("P(A | T) =", frac("(13/49) · (1/4)", "27/196", 30), "=",
                           frac(X("13", 36, C.AMBER), X("27", 36, C.AMBER), color=C.AMBER), size=30),
                        "מציבים בנוסחת בייס :\n‏13/196 חלקי 27/196, שוב 13/27.")
        self.fade_all()

        # The page's box counts the same cross, step by step.
        view = BoxView(QID, "tue", height=6.15).move_to(UP * 0.72)
        self.check_box(view)
        self.say("התיבה שבעמוד סופרת את אותו צלב, צעד\nאחרי צעד. צעד 1 : השורה, 14 משפחות.",
                 FadeIn(view))
        self.box_beat(view, [
            (1, "צעד 2 : העמודה של הילד השני, עוד 14.\nהמשבצת שבהצטלבות נספרה פעמיים."),
            (2, "צעד 3 : כל משפחה נספרת פעם אחת,\n‏14 + 14 − 1 = 27 משפחות."),
            (3, "צעד 4 : מתוכן שני בנים,\n‏7 + 7 − 1 = 13. ההסתברות 13/27."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        table = BoxView(QID, "infos", width=10.5).move_to(UP * 0.6)
        self.check_box(table)
        self.say("הטבלה שבתיבה משווה שלושה סוגי מידע,\nכל אחד על אותן 196 משפחות.", FadeIn(table))
        self.say("לפחות אחד בן נותן שליש, בן מיום שלישי\n‏13/27, והבכור הוא בן נותן חצי.")
        self.say("יום שלישי נמצא ביניהם : ככל שהמידע\nספציפי יותר, התשובה קרובה יותר לחצי.")
        self.fade_all()


CROSS_KEYS = sorted({(kind_of(a), kind_of(b)) for a, b in CROSS})
HIT_KEYS = sorted({(kind_of(a), kind_of(b)) for a, b in TWO_BOYS})
assert len(CROSS_KEYS) == 27 and len(HIT_KEYS) == 13


class ChapterC(ProofScene):
    def construct(self):
        self.chapter_card("סעיף ג", "הנוסחה הכללית",
                          "עכשיו בכלליות : C ילדים, כל אחד בן\nבהסתברות p, ועם התכונה בהסתברות q.")
        self.proof_start(np.array([-6.4, 3.45, 0]), gap=0.36)
        self.proof_line(eq(("A", C.GREEN), "= all C children are boys", size=36),
                        "נסמן : A הוא כל הילדים בנים, ו-T הוא\nלפחות ילד אחד שהוא בן עם התכונה.")
        self.proof_line(eq(("T", C.BLUE), "= at least one is a boy with the trait", size=36),
                        "שניהם מאורעות של \"לפחות אחד\", ואת\nשניהם הכי קל לחשב דרך המשלים : \"אף אחד\".",
                        dim=False)
        self.proof_line(eq("P(a child is a boy with the trait) = pq", size=36),
                        "ילד אחד הוא בן עם התכונה בהסתברות pq,\nואיננו כזה בהסתברות 1 − pq.")
        self.proof_line(eq("P(no child is) =", pw(X("(1 − pq)", 36), "C", 36), size=36),
                        "הילדים בלתי תלויים, ולכן אף אחד מהם\nאיננו כזה בהסתברות (1 − pq) בחזקת C.")
        den = self.proof_line(eq("P(T) = 1 −", pw(X("(1 − pq)", 36, C.AMBER), "C", 36, C.AMBER), size=36),
                              "המכנה הוא המשלים : 1 פחות\nהחזקה הזו. זו ההסתברות של T.")
        self.play(*[FadeOut(m) for m in self.proof_lines[:-1]],
                  den.animate.move_to(self.proof_corner, aligned_edge=UL), run_time=0.9)
        self.proof_lines = VGroup(den)
        self.proof_line(eq("P(A) =", pw(X("p", 36), "C", 36), size=36),
                        "המונה : כל הילדים בנים\nבהסתברות p בחזקת C.")
        self.proof_line(eq("P(T | A) = 1 −", pw(X("(1 − q)", 36), "C", 36), size=36),
                        "אם כולם בנים, T אומר רק שלפחות לאחד\nיש את התכונה : אחד פחות (1 − q) בחזקת C.")
        num = self.proof_line(eq("P(A ∩ T) =", pw(X("p", 36, C.AMBER), "C", 36, C.AMBER),
                                 X("·", 36, C.AMBER), X("(1 −", 36, C.AMBER),
                                 pw(X("(1 − q)", 36, C.AMBER), "C", 36, C.AMBER), X(")", 36, C.AMBER),
                                 size=36),
                              "לכן החיתוך הוא המכפלה : ההסתברות\nשכולם בנים, כפול זו של התכונה.")
        self.fade_all()
        del num

        big = eq("P(A | T) =", formula(40), size=40)
        big.move_to(UP * 1.4)
        box = SurroundingRectangle(big, color=C.AMBER, buff=0.3, corner_radius=0.15, stroke_width=4)
        self.say("מחלקים את המונה במכנה,\nומקבלים את הנוסחה הכללית.", FadeIn(big), Create(box))
        self.play(VGroup(big, box).animate.scale(0.75).move_to(UP * 2.75), run_time=0.9)

        self.proof_start(np.array([-6.0, 1.45, 0]), gap=0.42)
        self.proof_line(eq("C = 2, p = 1/2, q = 1:", frac("1/4", "1 − 1/4", 34), "=", ("1/3", C.AMBER), size=34),
                        "בדיקה : בלי תכונה, q = 1, הנוסחה\nנותנת רבע חלקי שלושה רבעים, שליש.")
        self.proof_line(eq("q = 1/7:", frac("(1/4) · (13/49)", "27/196", 34), "=", ("13/27", C.AMBER), size=34),
                        "יום בשבוע, q = 1/7 : המונה 13/196,\nהמכנה 27/196, ושוב 13/27.")
        self.proof_line(eq("q → 0:", "P(A | T) →", pw(X("p", 34, C.AMBER), "C − 1", 34, C.AMBER), "=",
                           ("1/2", C.AMBER), size=34),
                        "תכונה נדירה מאוד, q שואף ל-0 :\nהתשובה שואפת ל-p בחזקת C − 1.")
        self.say("עם שני ילדים זה חצי : המידע מצביע\nכמעט בוודאות על בן אחד מסוים.")
        self.fade_all()

        # The table of the page: the answer rises from 1/3 towards 1/2 as q shrinks.
        rows = [("q = 1", "1/3", "0.333", "1/7", "0.143"), ("q = 1/2", "3/7", "0.429", "7/37", "0.189"),
                ("q = 1/7", "13/27", "0.481", "127/547", "0.232"),
                ("q = 1/365", "729/1459", "0.500", "398581/1596511", "0.250")]
        for q, v2, d2, v3, d3 in rows:
            qq = Fraction(q.split("= ")[1])
            assert answer(2, HALF, qq) == Fraction(v2) and f"{float(Fraction(v2)):.3f}" == d2
            assert answer(3, HALF, qq) == Fraction(v3) and f"{float(Fraction(v3)):.3f}" == d3
        xs = (-4.6, -0.9, 3.6)
        tbl = VGroup()
        head = VGroup(X("p = 1/2", 32, C.MUTED), X("C = 2", 32, C.MUTED), X("C = 3", 32, C.MUTED))
        tbl.add(head)
        for q, v2, d2, v3, d3 in rows:
            tbl.add(VGroup(X(q, 34), X(f"{v2} ≈ {d2}", 34, C.AMBER), X(f"≈ {d3}", 34, C.BLUE)))
        tbl.arrange(DOWN, buff=0.42).move_to(UP * 0.9)
        for r in tbl:
            for m, x in zip(r, xs):
                m.set_x(x)
        rule = Line(LEFT * 6.0, RIGHT * 5.6, stroke_color=C.FAINT).next_to(head, DOWN, buff=0.2)
        self.say("ככל ש-q קטן, המידע ספציפי יותר,\nוהתשובה עולה מהשליש לכיוון החצי.",
                 FadeIn(VGroup(head[0], head[1])), Create(rule),
                 LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in tbl[1:]], lag_ratio=0.3),
                 run_time=2.0)
        self.say("עם שלושה ילדים, מאותה נוסחה : מהשביעית\nשל \"לפחות אחד בן\" ועד רבע.",
                 FadeIn(head[2]), LaggedStart(*[FadeIn(r[2]) for r in tbl[1:]], lag_ratio=0.3),
                 run_time=1.6)
        self.fade_all()

        # The page's probability box.
        sq = BoxView(QID, "square", height=5.8).move_to(UP * 0.8)
        self.check_box(sq)
        self.say("התיבה שבעמוד מחשבת את הנוסחה. בערכי\nהעמוד, p = 1/2 ו-q = 1/7, התשובה 0.4815.",
                 FadeIn(sq))
        self.say("בריבוע, השטח של כל משבצת הוא ההסתברות\nשל הזוג. הצלב הצבעוני הוא התנאי.")
        self.say("החלק הירוק, בתוך הריבוע המקווקו של\nשני בנים, הוא המטרה.")
        self.play(FadeOut(sq), run_time=0.6)
        cv = BoxView(QID, "curve", height=5.9).move_to(UP * 0.8)
        self.check_box(cv)
        self.say("העקומה : התשובה לכל q. מימין, q = 1\nוהשליש. משמאל, q קטן והקו של החצי.",
                 FadeIn(cv))
        self.box_beat(cv, [(1, "עם שלושה ילדים, C = 3 : התשובה 0.2322,\nכלומר 127/547, והגבול הוא רבע.")])
        self.fade_all()

        asked = VGroup(X("we asked: \"a Tuesday boy?\"  yes", 36),
                       eq("P =", ("13/27", C.AMBER), size=40)).arrange(DOWN, buff=0.3)
        told = VGroup(X("he picked a child and told us about it", 36),
                      eq("P =", ("1/2", C.AMBER), size=40)).arrange(DOWN, buff=0.3)
        VGroup(asked, told).arrange(DOWN, buff=0.9).move_to(UP * 0.8)
        self.say("מלכודת אחרונה : התשובה תלויה בדרך\nשבה התקבל המידע. שאלנו שאלה של כן או לא.",
                 FadeIn(asked))
        self.say("אם יוסי היה בוחר ילד באקראי ומספר עליו,\nהמידע היה על ילד מסוים, והתשובה חצי.",
                 FadeIn(told))
        self.fade_all()


class Closing(ProofScene):
    def construct(self):
        self.closing(QID, [("א", X("1/3", 36)),
                           ("ב", X("13/27 ≈ 0.481", 36)),
                           ("ג", formula(28))],
                     ["לסיכום : שליש, 13/27, ונוסחה אחת\nשמחזירה את שניהם.",
                      "נסו ערכים משלכם בתיבות\nשבעמוד של שאלה 0015 באתר."],
                     holds=(3.4, 3.6))
