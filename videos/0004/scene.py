"""The tutorial video of question 0004, three mislabeled boxes (script: script.md).

Render with `python videos/render.py 0004` (see VIDEOS.md). The example is the page's: the
labels RED, BLACK, MIXED on boxes 0, 1, 2 and the contents of arrangement 1, so the ball
drawn from box 2 is red. The Hebrew in the frame comes from he() (browser-drawn PNGs).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, CodePanel, DVQScene, M, T, VarPanel, chip, cost_chips, he,  # noqa: E402
                 page_python, trace)

QID = 4
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – מספר הדגימות המינימלי"),
    ("ChapterB", "סעיף ב – הקוד"),
    ("Closing", "סיכום"),
]

HE = {"R": "אדום", "B": "שחור", "M": "אדום ושחור"}
EN = {"R": "RED", "B": "BLACK", "M": "MIXED"}
LABELS = ["R", "B", "M"]          # the labels on boxes 0, 1, 2 (the page's example)
ARR1 = ["B", "M", "R"]            # arrangement 1: the true contents (a red ball from box 2)
ARR2 = ["M", "R", "B"]            # arrangement 2 (a black ball from box 2)
XS = [-4.3, 0.0, 4.3]


def ball(kind: str, r: float = 0.2) -> Circle:
    fill = C.BALL_RED if kind == "R" else C.BALL_BLACK
    return Circle(radius=r, fill_color=fill, fill_opacity=1, stroke_color=C.MUTED, stroke_width=2)


def content(kind: str, r: float = 0.2) -> VGroup:
    """The content of a box as balls: red, black, or one of each (mixed)."""
    if kind == "M":
        return VGroup(ball("R", r), ball("B", r)).arrange(RIGHT, buff=0.06)
    return VGroup(ball(kind, r))


class Crate(Group):
    """A wooden crate as in the page's figure (tools/figures/q0004.py), its label on the front."""

    def __init__(self, label: Mobject | None = None, w: float = 2.7, h: float = 1.75, d: float = 0.45):
        super().__init__()
        front = Rectangle(width=w, height=h, fill_color=C.CRATE, fill_opacity=1,
                          stroke_color=C.CRATE_EDGE, stroke_width=3)
        ul, ur, dr = front.get_corner(UL), front.get_corner(UR), front.get_corner(DR)
        off = np.array([d, d, 0])
        top = Polygon(ul, ul + off, ur + off, ur, fill_color=C.CRATE_TOP, fill_opacity=1,
                      stroke_color=C.CRATE_EDGE, stroke_width=3)
        side = Polygon(ur, ur + off, dr + off, dr, fill_color=C.CRATE_SIDE, fill_opacity=1,
                       stroke_color=C.CRATE_EDGE, stroke_width=3)
        self.front, self.top = front, top
        self.add(top, side, front)
        self.label = None
        if label is not None:
            self.set_label(label)

    def set_label(self, label: Mobject):
        label.move_to(self.front)
        self.label = label
        self.add(label)
        return label

    def mouth(self):
        return self.top.get_center()


def crates(labels=None, en=False, scale=1.0):
    row = Group()
    for k, x in enumerate(XS):
        lab = None
        if labels is not None:
            lab = M(EN[labels[k]], 34, C.WHITE, weight="BOLD") if en else he(HE[labels[k]], 40, C.WHITE, 600)
        c = Crate(lab).scale(scale).move_to([x, 0, 0])
        row.add(c)
    return row


class BoxScene(DVQScene):
    def rise(self, crate: Crate, kind: str, height: float = 1.3):
        """A ball rises out of the crate's mouth; returns the ball."""
        b = ball(kind, 0.26).move_to(crate.mouth())
        self.add_foreground_mobject(b)
        self.play(FadeIn(b, scale=0.5), run_time=0.3)
        self.play(b.animate.shift(UP * height), run_time=0.9)
        return b

    def pin(self, crate: Crate, kind: str, color=None):
        """The true content of `crate`, pinned under it as a chip."""
        c = chip(content(kind, 0.22), color=color or C.GREEN, buff=0.16)
        c.next_to(crate, DOWN, buff=0.35)
        return c


class Opening(BoxScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "שלוש קופסאות עם תוויות שגויות",
                     ["א · מספר הדגימות המינימלי", "ב · הקוד"],
                     ["שאלה 0004 : שלוש קופסאות עם תוויות שגויות,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : כמה דגימות צריך,\nואיך כותבים את זה בקוד."])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)
        row = crates().move_to(DOWN * 0.4)
        piles = VGroup()
        for k, crate in enumerate(row):
            kinds = {"R": "RRR", "B": "BBB", "M": "RBR"}[ARR1[k]]
            pile = VGroup(*[ball(t, 0.24) for t in kinds]).arrange(RIGHT, buff=0.08)
            pile.next_to(crate.top, UP, buff=0.15)
            piles.add(pile)
        self.say("באחת הקופסאות רק כדורים אדומים, באחרת רק שחורים,\nובשלישית גם וגם.",
                 FadeIn(row, lag_ratio=0.2), FadeIn(piles, shift=0.3 * DOWN, lag_ratio=0.2), run_time=1.6)
        labels = Group(*[he(HE[k], 40, C.WHITE, 600) for k in LABELS])
        for crate, lab in zip(row, labels):
            lab.move_to(crate.front)
        self.say("על כל קופסה מודבקת תווית :\nאדום, שחור, ואדום ושחור.",
                 *[p.animate.shift(DOWN * 0.6).set_opacity(0) for p in piles],
                 *[FadeIn(lab, shift=0.15 * DOWN) for lab in labels], run_time=1.5)
        text = he("כל התוויות שגויות", 52, C.RED, 700)
        frame = RoundedRectangle(width=text.width + 0.6, height=text.height + 0.4, corner_radius=0.12,
                                 stroke_color=C.RED, stroke_width=6, fill_color=C.NAVY_DARK,
                                 fill_opacity=0.85)
        stamp = Group(frame, text).rotate(8 * DEGREES).move_to(UP * 2.4)
        self.say("והחוק היחיד : כל התוויות שגויות.", FadeIn(stamp, scale=1.8), run_time=0.6)
        self.fade_all()


class ChapterA(BoxScene):
    def construct(self):
        self.chapter_card("סעיף א", "מספר הדגימות המינימלי",
                          "סעיף א : מהו המספר המינימלי של דגימות\nשמבטיח שנוכל לתקן את כל התוויות?")
        row = crates(LABELS).move_to(DOWN * 0.3)
        with self.beat("דגימה : מצביעים על קופסה,\nומקבלים ממנה כדור אחד אקראי."):
            self.play(FadeIn(row, lag_ratio=0.2), run_time=1.0)
            b = self.rise(row[0], "B")
        self.play(FadeOut(row), FadeOut(b), run_time=0.6)

        # The six ways, and the two in which every label is wrong.
        import itertools
        perms = list(itertools.permutations("RBM"))
        xs = [-2.8, 0.6, 4.0]
        head = Group(*[he(HE[k], 40, C.AMBER, 600).move_to([x, 3.4, 0]) for k, x in zip(LABELS, xs)])
        rule = Line([-5.0, 2.95, 0], [5.6, 2.95, 0], stroke_color=C.MUTED, stroke_width=2)
        ys = [2.4 - r * 0.88 for r in range(6)]
        rows = []
        for p, y in zip(perms, ys):
            rows.append(VGroup(*[content(k, 0.27).move_to([x, y, 0]) for k, x in zip(p, xs)]))
        self.say("יש שש דרכים לחלק את שלושת סוגי התוכן\nבין שלוש הקופסאות.",
                 FadeIn(head), Create(rule), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15),
                 run_time=2.0)
        crosses = VGroup()
        bad = []
        for r, p in enumerate(perms):
            hit = [c for c in range(3) if p[c] == LABELS[c]]
            if hit:
                bad.append(r)
            for c in hit:
                crosses.add(Cross(rows[r][c], stroke_color=C.RED, stroke_width=5, scale_factor=1.3))
        self.say("אבל כל התוויות שגויות, ולכן נפסל\nכל סידור שבו תוכן תואם לתווית שלו.",
                 LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.15), run_time=2.0)
        good = [r for r in range(6) if r not in bad]
        assert [list(perms[r]) for r in good] == [ARR1, ARR2] or [list(perms[r]) for r in good] == [ARR2, ARR1]
        r1 = good[[list(perms[r]) for r in good].index(ARR1)]
        r2 = good[[list(perms[r]) for r in good].index(ARR2)]
        num1 = M("1", 44, C.MUTED).move_to([-5.0, 0.9, 0])
        num2 = M("2", 44, C.MUTED).move_to([-5.0, -0.5, 0])
        self.say("נשארים רק שני סידורים אפשריים,\nוצריך להכריע ביניהם.",
                 *[FadeOut(rows[r]) for r in bad], FadeOut(crosses),
                 rows[r1].animate.move_to([rows[r1].get_x(), 0.9, 0]),
                 rows[r2].animate.move_to([rows[r2].get_x(), -0.5, 0]), FadeIn(num1), FadeIn(num2))

        def ring(c, color):
            return SurroundingRectangle(VGroup(rows[r1][c], rows[r2][c]), color=color, buff=0.25,
                                        corner_radius=0.12)

        def above(kind, c):
            return content(kind, 0.3).move_to([xs[c], -2.0, 0])

        ring0, b0 = ring(0, C.BLUE), above("B", 0)
        self.say("בקופסה \"אדום\" יש שחור או תערובת.\nכדור שחור מתאים לשני הסידורים.",
                 Create(ring0), FadeIn(b0, shift=0.2 * UP))
        ring1, b1 = ring(1, C.BLUE), above("R", 1)
        self.say("בקופסה \"שחור\" יש תערובת או אדום,\nוכדור אדום מתאים לשניהם.",
                 ReplacementTransform(ring0, ring1), FadeOut(b0), FadeIn(b1, shift=0.2 * UP))
        ring2 = ring(2, C.AMBER)
        self.say("רק בקופסה \"אדום ושחור\"\nשני הסידורים נבדלים בצבע אחד וברור.",
                 ReplacementTransform(ring1, ring2), FadeOut(b1), Indicate(head[2], color=C.AMBER))
        self.say("הרעיון : התווית \"אדום ושחור\" שגויה,\nולכן בקופסה הזו יש צבע אחד בלבד.",
                 ring2.animate.set_stroke(width=6))
        self.fade_all()

        # The two cases.
        row = crates(LABELS).move_to(UP * 0.2)
        self.play(FadeIn(row), run_time=0.8)
        with self.beat("מקרה ראשון : מהקופסה \"אדום ושחור\" יוצא כדור אדום.\nזו הקופסה האדומה."):
            b = self.rise(row[2], "R")
            p2 = self.pin(row[2], "R")
            self.play(FadeIn(p2, shift=0.2 * UP), run_time=0.7)
        p1 = self.pin(row[1], "M")
        self.say("הקופסה \"שחור\" לא שחורה, כי התווית שגויה,\nוגם לא אדומה. לכן היא התערובת.",
                 FadeIn(p1, shift=0.2 * UP), Indicate(row[1].label, color=C.AMBER))
        p0 = self.pin(row[0], "B")
        self.say("ולקופסה \"אדום\" נשאר השחור.", FadeIn(p0, shift=0.2 * UP))
        with self.beat("מקרה שני : יוצא כדור שחור.\nאז זו הקופסה השחורה."):
            self.play(FadeOut(b), FadeOut(p0), FadeOut(p1), FadeOut(p2), run_time=0.6)
            self.remove_foreground_mobject(b)
            b = self.rise(row[2], "B")
            p2 = self.pin(row[2], "B")
            self.play(FadeIn(p2, shift=0.2 * UP), run_time=0.7)
        p0, p1 = self.pin(row[0], "M"), self.pin(row[1], "R")
        self.say("הקופסה \"אדום\" לא אדומה וגם לא שחורה,\nלכן היא התערובת, ול\"שחור\" נשאר האדום.",
                 FadeIn(p0, shift=0.2 * UP), FadeIn(p1, shift=0.2 * UP))
        self.remove_foreground_mobject(b)
        self.fade_all()

        # The rule, on the two arrangements.
        head, mini, marks = self.mini_table()
        deciders = VGroup(content("R", 0.32).move_to(marks[0]), content("B", 0.32).move_to(marks[1]))
        self.say("הכלל : יצא צבע c? הקופסה שתוויתה c\nמכילה את הצבע השני, והשלישית את התערובת.",
                 FadeIn(head), FadeIn(mini), FadeIn(deciders))
        q = VGroup(*[M("?", 64, C.AMBER).move_to(m) for m in marks])
        self.say("ולמה לא אפס? בלי דגימה נשארים שני סידורים,\nואין דרך לבחור ביניהם.",
                 FadeOut(deciders), FadeIn(q))
        self.play(FadeOut(head), FadeOut(mini), FadeOut(q), run_time=0.6)
        answer = chip(VGroup(M("1", 140, C.AMBER, weight="BOLD"), T("draw", 60, C.WHITE)).arrange(RIGHT, buff=0.4),
                      color=C.AMBER, buff=0.45, stroke=4)
        under = Group(Crate(he(HE["M"], 40, C.WHITE, 600)))
        Group(answer, under).arrange(RIGHT, buff=1.2).move_to(ORIGIN)
        self.say("לכן התשובה : דגימה אחת,\nודווקא מהקופסה \"אדום ושחור\".",
                 FadeIn(answer, scale=1.2), FadeIn(under))
        self.fade_all()

        # The trap.
        row = crates(LABELS).move_to(UP * 0.4)
        self.play(FadeIn(row), run_time=0.8)
        with self.beat("המלכודת : לדגום מהקופסה \"אדום\".\nכדור שחור משם משאיר את שני הסידורים פתוחים."):
            b = self.rise(row[0], "B")
            maybe = VGroup(chip(content("B", 0.22), color=C.MUTED, buff=0.14), M("?", 44, C.AMBER),
                           chip(content("M", 0.22), color=C.MUTED, buff=0.14)).arrange(RIGHT, buff=0.25)
            maybe.next_to(row[0], DOWN, buff=0.4)
            self.play(FadeIn(maybe, shift=0.2 * UP), run_time=0.8)
        ring = SurroundingRectangle(row[2], color=C.AMBER, buff=0.2, corner_radius=0.15)
        maybe1 = VGroup(chip(content("M", 0.22), color=C.MUTED, buff=0.14), M("?", 44, C.AMBER),
                        chip(content("R", 0.22), color=C.MUTED, buff=0.14)).arrange(RIGHT, buff=0.25)
        maybe1.next_to(row[1], DOWN, buff=0.4)
        self.say("אותו דבר בקופסה \"שחור\".\nרק \"אדום ושחור\" ידועה מראש כחד-צבעית.",
                 FadeIn(maybe1, shift=0.2 * UP), Create(ring))
        self.remove_foreground_mobject(b)
        self.fade_all()

    def mini_table(self):
        """The two arrangements under the three labels, a slot at the left of each row."""
        xs = [-1.4, 1.7, 4.8]
        head = Group(*[he(HE[k], 40, C.AMBER, 600).move_to([x, 1.9, 0]) for k, x in zip(LABELS, xs)])
        rows = VGroup()
        marks = []
        for arr, y in ((ARR1, 0.55), (ARR2, -1.0)):
            rows.add(VGroup(*[content(k, 0.3).move_to([x, y, 0]) for k, x in zip(arr, xs)]))
            marks.append(np.array([-4.4, y, 0]))
        rows.add(Line([-5.4, 1.3, 0], [6.0, 1.3, 0], stroke_color=C.MUTED, stroke_width=2))
        rows.add(Line([-3.2, 1.2, 0], [-3.2, -1.7, 0], stroke_color=C.MUTED, stroke_width=2))
        return head, rows, marks


class ChapterB(BoxScene):
    def construct(self):
        self.chapter_card("סעיף ב", "הקוד", "סעיף ב : מתרגמים את הפתרון לפונקציה.")

        cells = VGroup()
        for k, x in enumerate(XS):
            box = RoundedRectangle(width=2.9, height=1.0, corner_radius=0.14, stroke_color=C.MUTED,
                                   stroke_width=2.5, fill_color=C.NAVY_LIGHT, fill_opacity=1)
            cells.add(VGroup(box, M(f'"{EN[LABELS[k]]}"', 34).move_to(box),
                             M(str(k), 28, C.MUTED).next_to(box, DOWN, buff=0.2)))
        cells.arrange(RIGHT, buff=0.35).move_to(DOWN * 1.65)
        name = M("labels", 34, C.MUTED).next_to(cells, UP, buff=0.3).align_to(cells, LEFT)
        self.say("הקלט : מערך labels של שלוש תוויות,\nכלומר RED, BLACK ו-MIXED, בסדר כלשהו.",
                 FadeIn(cells, lag_ratio=0.2), FadeIn(name))
        row = crates(LABELS, en=True, scale=0.8)
        for crate, cell in zip(row, cells):
            crate.move_to([cell.get_x() - 0.15, 0.9, 0])
        arrow = Arrow(row[2].mouth() + UP * 1.7 + LEFT * 1.1, row[2].mouth() + UP * 0.25, color=C.AMBER,
                      stroke_width=5, buff=0)
        call = M("draw(2)", 36, C.AMBER).next_to(arrow.get_start(), LEFT, buff=0.2)
        with self.beat("ה-API : draw(i) שולף כדור אקראי מקופסה i,\nומחזיר RED או BLACK."):
            self.play(FadeIn(row, lag_ratio=0.2), run_time=0.8)
            self.play(GrowArrow(arrow), FadeIn(call), run_time=0.8)
            b = self.rise(row[2], "R", height=1.0)
            got = M('"RED"', 36, C.RED).next_to(b, RIGHT, buff=0.3)
            self.play(FadeIn(got), run_time=0.4)
        truth = VGroup(*[content(k, 0.18).set_opacity(0.6).next_to(c.front, DOWN, buff=0.12)
                         .shift(UP * 0.62) for k, c in zip(ARR1, row)])
        self.say("בדוגמה מהעמוד, התוכן האמיתי הוא סידור 1 מסעיף א,\nולכן הכדור מקופסה 2 אדום.",
                 FadeIn(truth))
        self.remove_foreground_mobject(b)
        self.fade_all()

        self.solution1()
        self.rotation()
        self.solution2()
        self.modulo()
        self.cost()

    def solution1(self):
        code = page_python(QID, "def fix_labels_simple")
        panel = CodePanel(code, font_size=24, drop_comments=True, line_spacing=0.5)

        def fmt(n, s):
            if n.startswith("fixed"):
                return repr(s["fixed"][int(n[6])]) if "fixed" in s else ""
            return repr(s[n]) if n in s else ""

        vp = VarPanel(["i", "k", "ball", "other", "fixed[0]", "fixed[1]", "fixed[2]"], fmt=fmt,
                      size=32, buff=0.35).set_state({})
        self.place_code(panel, vp, vp_width=vp.keys["fixed[0]"].width + 2.2)
        self.type_code(panel, [
            (1, "הפונקציה מקבלת את מערך התוויות,\nומחזירה את התוויות הנכונות."),
            (2, "המערך fixed יקבל את התוויות המתוקנות.\nבינתיים שלוש מחרוזות ריקות."),
            (range(5, 8), "לולאה ראשונה : מחפשים את הקופסה\nשתוויתה MIXED, ושומרים את האינדקס שלה ב-k."),
            (8, "הדגימה היחידה בפונקציה, מקופסה k.\nהיא חד-צבעית, ולכן ball הוא הצבע שלה."),
            (range(11, 15), "התנאי קובע את הצבע השני, other :\nאם ball הוא RED אז BLACK, ואחרת RED."),
            (15, "קופסה k מקבלת את התווית ball,\nכי זה הצבע היחיד שבה."),
            (range(18, 21), "לולאה שנייה : הקופסה שתוויתה ball\nמקבלת other, לפי הכלל של סעיף א."),
            (range(23, 26), "לולאה שלישית : בקופסה שתוויתה other\nאין other ואין ball, ולכן היא MIXED."),
            (27, "ומחזירים את fixed.\nהמערך labels עצמו לא השתנה."),
        ], intro="הפתרון הראשון מתרגם את סעיף א כמעט מילה במילה,\nובונה מערך fixed חדש.")
        self.say("נריץ על הדוגמה מהעמוד,\nכש-draw מחזיר RED.", FadeIn(vp))
        steps, result = trace(code, "fix_labels_simple", ([EN[k] for k in LABELS],),
                              {"draw": lambda i: "RED"})
        assert result == [EN[k] for k in ARR1]
        cursor = self.run_code(panel, vp, steps, [
            ([2, 5, 6, 5, 6, 5, 6, 7, 5], "המעבר הראשון מחפש את MIXED.\nהוא בקופסה 2, ולכן k = 2."),
            ([8], "דגימה אחת מקופסה 2 : יוצא RED."),
            ([11, 12, 15], "הצבע השני, other, הוא BLACK,\nוקופסה 2 מקבלת RED."),
            ([18, 19, 20, 18, 19, 18, 19, 18], "המעבר השני : הקופסה שתוויתה RED\nמקבלת את other, כלומר BLACK."),
            ([23, 24, 23, 24, 25, 23, 24, 23], "המעבר השלישי : הקופסה שתוויתה BLACK\nמקבלת MIXED."),
            ([27], "התוצאה : BLACK, MIXED, RED.\nבדיוק סידור 1."),
        ], step_time=3.0)
        self.play(FadeOut(cursor), *vp.show({}, flash=False), run_time=0.6)
        steps, result = trace(code, "fix_labels_simple", ([EN[k] for k in LABELS],),
                              {"draw": lambda i: "BLACK"})
        assert result == [EN[k] for k in ARR2]
        cursor = self.run_code(panel, vp, steps, [
            ([2, 5, 6, 5, 6, 5, 6, 7, 5, 8, 11, 14, 15], "ואם הכדור שחור? other הוא RED,\nוקופסה 2 מקבלת BLACK."),
            ([18, 19, 18, 19, 20, 18, 19, 18, 23, 24, 25, 23, 24, 23, 24, 23, 27],
             "קופסה 1 מקבלת RED, וקופסה 0 מקבלת MIXED.\nזה סידור 2."),
        ], step_time=3.4)
        self.fade_all()
        chips = cost_chips(("passes", "3"), ("memory", "new array"),
                           notes=("three loops over labels", "fixed"))
        self.say("הפתרון נכון וקריא, אבל עובר על המערך שלוש פעמים\nומחזיק מערך נוסף.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

    def rotation(self):
        cells, texts = VGroup(), []
        for k, x in enumerate(XS):
            box = RoundedRectangle(width=2.9, height=1.1, corner_radius=0.14, stroke_color=C.MUTED,
                                   stroke_width=2.5, fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to([x, 0, 0])
            t = M(f'"{EN[LABELS[k]]}"', 36).move_to(box)
            texts.append(t)
            cells.add(box)
        idx = VGroup(*[M(str(k), 28, C.MUTED).next_to(cells[k], DOWN, buff=0.2) for k in range(3)])
        tags = VGroup(M("same", 34, C.BLUE).next_to(cells[0], UP, buff=0.3),
                      M("other", 34, C.PURPLE).next_to(cells[1], UP, buff=0.3),
                      M("k", 34, C.AMBER).next_to(cells[2], UP, buff=0.3))
        big = CurvedArrow(cells[0].get_top() + UP * 0.85, cells[2].get_top() + UP * 0.85, angle=-PI / 3,
                          color=C.AMBER, stroke_width=5)
        low1 = CurvedArrow(cells[2].get_bottom() + DOWN * 0.6, cells[1].get_bottom() + DOWN * 0.6,
                           angle=-PI / 2.5, color=C.AMBER, stroke_width=5)
        low2 = CurvedArrow(cells[1].get_bottom() + DOWN * 0.6, cells[0].get_bottom() + DOWN * 0.6,
                           angle=-PI / 2.5, color=C.AMBER, stroke_width=5)
        self.say("הפתרון השני מתחיל מתצפית :\nהתיקון הוא סיבוב של שלוש התוויות.",
                 FadeIn(cells), *[FadeIn(t) for t in texts], FadeIn(idx), Create(big), Create(low1),
                 Create(low2), run_time=1.8)
        self.say("נקרא same לקופסה שתוויתה כצבע הכדור,\nו-other לקופסה השלישית.",
                 FadeIn(tags, shift=0.2 * DOWN))
        self.say("צבע הכדור עובר ל-k, MIXED עובר ל-other,\nוהצבע השני עובר ל-same.",
                 texts[0].animate(path_arc=-PI / 1.6).move_to(cells[2]),
                 texts[2].animate(path_arc=-PI / 1.6).move_to(cells[1]),
                 texts[1].animate(path_arc=-PI / 1.6).move_to(cells[0]), run_time=2.0)
        swaps = M("rotation of 3 = 2 swaps", 36, C.GREEN).move_to(DOWN * 2.3)
        self.say("וסיבוב של שלושה איברים\nהוא בדיוק שתי החלפות.", FadeIn(swaps, shift=0.2 * UP))
        self.fade_all()

    def solution2(self):
        code = page_python(QID, "def fix_labels(")
        panel = CodePanel(code, font_size=26, drop_comments=True, drop_trailing_comments=True,
                          line_spacing=0.6)          # place_code scales it to the frame

        def fmt(n, s):
            return repr(s[n]) if n in s else ""

        vp = VarPanel(["k", "ball", "n1", "n2", "same", "other", "labels"], fmt=fmt, size=30,
                      cols=3, slot=3.7)
        vp.set_state({"labels": [EN[k] for k in LABELS]})
        self.place_code(panel, vp)
        self.type_code(panel, [
            (1, "הפעם הפונקציה מתקנת את labels במקום,\nומחזירה את אותו מערך."),
            ([2, 3], "המתודה index מוצאת את MIXED בשורה אחת,\nוהדגימה היחידה היא שוב מקופסה k."),
            (5, "השכנים של k במעגל, n1 ו-n2,\nבלי לולאה ובלי חיפוש."),
            ([6, 7], "בדיקה אחת : השכן שתוויתו כצבע הכדור\nהוא same, והשני הוא other."),
            (10, "החלפה ראשונה, בהשמה מרובה ובלי tmp :\nקופסה k מקבלת את צבע הכדור."),
            (11, "החלפה שנייה, בין same ל-other.\nשתי ההחלפות יחד הן הסיבוב."),
            (12, "ומחזירים את labels, מתוקן במקום."),
        ], intro="הקוד : אחרי הדגימה לא מחפשים שוב,\nולא בונים מערך חדש.")
        self.say("ועכשיו הריצה, שוב עם כדור אדום.", FadeIn(vp))
        steps, result = trace(code, "fix_labels", ([EN[k] for k in LABELS],), {"draw": lambda i: "RED"})
        assert result == [EN[k] for k in ARR1]
        self.run_code(panel, vp, steps, [
            ([2, 3], "שוב k = 2, והכדור שיוצא אדום."),
            ([5], "השכנים של k : ‏(k + 1) % 3, כלומר 0,\nו-(k + 2) % 3, כלומר 1."),
            ([6, 7], "בקופסה 0 כתוב RED, כמו הכדור,\nולכן same = 0 ו-other = 1."),
            ([10], "החלפה ראשונה, בין k ל-same : קופסה 2 כבר נכונה,\nו-MIXED עובר זמנית ל-0."),
            ([11, 12], "החלפה שנייה, בין same ל-other :\nמתקבל BLACK, MIXED, RED."),
        ])
        self.say("אותה תוצאה כמו בפתרון הראשון,\nבשתי החלפות במקום.")
        self.fade_all()

    def modulo(self):
        k0 = M("k = 0", 44, C.AMBER).move_to(UP * 3.0)
        heads = VGroup(T("Python", 44, C.BLUE).move_to(LEFT * 3.4 + UP * 1.8),
                       T("SystemVerilog", 44, C.PURPLE).move_to(RIGHT * 3.4 + UP * 1.8))
        rule = Line(UP * 2.3, DOWN * 2.3, stroke_color=C.MUTED, stroke_width=2)
        self.say("ולמה (k + 2) % 3 ולא (k − 1) % 3?\nשניהם אמורים לתת את השכן הקודם במעגל.",
                 FadeIn(k0), FadeIn(heads), Create(rule))

        def line(expr, result, color, x, y, mark=""):
            g = VGroup(M(expr, 38), M("=", 38, C.MUTED), M(result, 38, color))
            if mark:
                g.add(M(mark, 38, color))
            return g.arrange(RIGHT, buff=0.3).move_to([x, y, 0])

        py = line("(0 - 1) % 3", "2", C.GREEN, -3.4, 0.5)
        self.say("ב-Python, ‏(0 − 1) % 3 הוא 2,\nכי שם התוצאה של % אף פעם לא שלילית.", FadeIn(py))
        sv = line("(0 - 1) % 3", "-1", C.RED, 3.4, 0.5, "✗")
        self.say("ב-SystemVerilog וב-C, % שומר על סימן המחולק :\nיוצא −1, אינדקס לא חוקי.", FadeIn(sv))
        both = VGroup(line("(0 + 2) % 3", "2", C.GREEN, -3.4, -1.4, "✓"),
                      line("(0 + 2) % 3", "2", C.GREEN, 3.4, -1.4, "✓"))
        self.say("חיבור 2 שקול לחיסור 1 מודולו 3, ונשאר חיובי.\nלכן הקוד זהה בשתי השפות.", FadeIn(both))
        self.fade_all()

    def cost(self):
        rows = [("", "fix_labels_simple", "fix_labels"),
                ("passes", "3", "1"),
                ("extra memory", "new array", "2 indices"),
                ("label writes", "3 writes", "2 swaps"),
                ("draws", "1", "1"),
                ("time", "O(1)", "O(1)")]
        xs = [-4.3, -0.2, 4.0]
        grid = VGroup()
        right = VGroup()
        for r, row in enumerate(rows):
            y = 2.6 - r * 0.85
            for c, (val, x) in enumerate(zip(row, xs)):
                if r == 0:
                    m = M(val, 32, C.GREEN)
                elif c == 0:
                    m = T(val, 32, C.MUTED)
                else:
                    m = M(val, 34, C.WHITE)
                m.move_to([x, y, 0])
                grid.add(m)
                if c == 2:
                    right.add(m)
        grid.add(Line([-6.2, 2.17, 0], [6.0, 2.17, 0], stroke_color=C.MUTED, stroke_width=2))
        self.say("הסיבוכיות : שני הפתרונות O(1),\nעם דגימה אחת.", FadeIn(grid, lag_ratio=0.03))
        box = SurroundingRectangle(right, color=C.AMBER, buff=0.25, corner_radius=0.12)
        self.say("השני עושה מעבר אחד ושתי החלפות במקום,\nבלי מערך נוסף.", Create(box))
        self.fade_all()


class Closing(BoxScene):
    def construct(self):
        self.closing(QID, [("א", M("1 draw, from the box labelled MIXED", 32)),
                           ("ב", M("fix: rotate the labels, 2 swaps", 32))],
                     ["לסיכום : דגימה אחת מהקופסה \"אדום ושחור\"\nמתקנת את שלוש התוויות.",
                      "ובקוד התיקון הוא סיבוב, שתי החלפות במקום.\nנסו בתיבה שבעמוד של שאלה 0004."])
