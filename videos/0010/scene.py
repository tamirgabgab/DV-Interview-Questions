"""The tutorial video of question 0010, valid parentheses (script: script.md).

Render with `python videos/render.py 0010` (see VIDEOS.md). Part א deletes adjacent
pairs, pass after pass: the page has no box for it, so the string is drawn here as a row
of cells and its pairs are deleted as the page's code does (every "()", then every "[]",
then every "{}" in one pass); the box's table of passes for (((()))) shows the O(n²).
Part ב reads the string once with a stack: the page's box is played alone on {[()]},
([)] and (((, then beside the typed code on the same strings, and on (([], an even
string whose openers are left over ((( is caught earlier, by its odd length).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel, cost_chips,  # noqa: E402
                 page_python, trace)

QID = 10
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – פתרון פשוט"),
    ("ChapterB", "סעיף ב – פתרון יעיל"),
    ("Closing", "סיכום"),
]

# The page's box, captured narrower than the page (540 CSS px) so it is compact beside the
# code. Each string is typed into the box's field, then read one character a click:
# picture 0 is the string before its first character, picture k after character k. The
# last box is part א's table of passes (the box's fold under the stack) for (((()))).
BOXES = {
    "nested": {"box": 0, "width": 540, "region": [".ex-play-row", ".br-box", ".br-step", ".br-sum"],
               "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 6}]},
    "mismatch": {"box": 0, "width": 540, "region": [".ex-play-row", ".br-box", ".br-step", ".br-sum"],
                 "steps": [[["fill", ".ex-s", "([)]"]], {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "open": {"box": 0, "width": 540, "region": [".ex-play-row", ".br-box", ".br-step", ".br-sum"],
             "steps": [[["fill", ".ex-s", "((("]], {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "even": {"box": 0, "width": 540, "region": [".ex-play-row", ".br-box", ".br-step", ".br-sum"],
             "steps": [[["fill", ".ex-s", "(([]"]], {"do": [["click", ".ex-next"]], "repeat": 4}]},
    "passes": {"box": 0, "width": 640, "region": [".br-passes"],
               "steps": [[["fill", ".ex-s", "(((())))"]]]},
}

PAIRS = ["()", "[]", "{}"]


def occurrences(s: str, pat: str) -> list[int]:
    """The indices str.replace(pat, "") deletes: every non-overlapping occurrence, left to
    right."""
    out, i = [], 0
    while True:
        i = s.find(pat, i)
        if i < 0:
            return out
        out += [i, i + 1]
        i += 2


class Row(VGroup):
    """A bracket string as a row of cells, centred on `centre`; pairs are deleted in place
    and the cells left close the gap."""

    def __init__(self, s: str, centre=ORIGIN, side: float = 0.95, font: float | None = None):
        super().__init__()
        self.s, self.centre, self.side = s, np.array(centre, dtype=float), side
        self.font = font or 56 * side / 0.95
        self.cells = [self.cell(ch) for ch in s]
        for c, x in zip(self.cells, self.xs(len(s))):
            c.move_to(self.centre + RIGHT * x)
        self.add(*self.cells)

    def cell(self, ch: str) -> VGroup:
        box = RoundedRectangle(width=self.side, height=self.side, corner_radius=0.12,
                               stroke_color=C.MUTED, stroke_width=2.5,
                               fill_color=C.NAVY_LIGHT, fill_opacity=1)
        return VGroup(box, M(ch, self.font).move_to(box))

    def xs(self, n: int) -> list[float]:
        pitch = self.side + 0.14
        return [(i - (n - 1) / 2) * pitch for i in range(n)]

    def rings(self, idx: list[int], color: str = C.AMBER) -> VGroup:
        return VGroup(*[SurroundingRectangle(VGroup(self.cells[i], self.cells[i + 1]), color=color,
                                             buff=0.08, corner_radius=0.12, stroke_width=5)
                        for i in idx[::2]])

    def delete(self, scene: "DVQScene", idx: list[int]) -> None:
        """Mark the cells `idx` (pairs), then delete them; the others close up."""
        rings = self.rings(idx)
        scene.play(Create(rings), *[c[1].animate.set_color(C.AMBER) for i, c in enumerate(self.cells)
                                    if i in idx], run_time=0.6)
        keep = [c for i, c in enumerate(self.cells) if i not in idx]
        gone = [c for i, c in enumerate(self.cells) if i in idx]
        moves = [c.animate.move_to(self.centre + RIGHT * x) for c, x in zip(keep, self.xs(len(keep)))]
        scene.play(*[FadeOut(c, scale=0.6) for c in gone], FadeOut(rings), *moves, run_time=0.7)
        for c in gone:
            self.remove(c)
        self.cells = keep
        self.s = "".join(ch for i, ch in enumerate(self.s) if i not in idx)

    def one_pass(self, scene: "DVQScene") -> None:
        """One pass of the page's line 3: replace every "()", then "[]", then "{}"."""
        for pat in PAIRS:
            idx = occurrences(self.s, pat)
            if idx:
                self.delete(scene, idx)


class BracketScene(DVQScene):
    """Helpers shared by the chapters of 0010."""

    def verdict(self, ok: bool, where) -> Text:
        return M("True" if ok else "False", 44, C.GREEN if ok else C.RED, weight="BOLD").move_to(where)

    def run_with(self, panel: CodePanel, steps: list, groups: list, cursor=None):
        """Light the traced lines as run_code does, and after each group's lines play its
        own pictures (a callable, or None): [(lines, caption, then), ...]."""
        planned = [n for g in groups for n in g[0]]
        ran = [s.line for s in steps]
        if planned != ran:
            raise RuntimeError(f"the code ran lines {ran}, the script lights {planned}")
        k = 0
        for lines, caption, then in groups:
            with self.beat(caption):
                per = min(1.0, 2.4 / len(lines))
                for _ in lines:
                    bar = panel.bar(steps[k].line)
                    k += 1
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar), run_time=per)
                    cursor = cursor or bar
                if then is not None:
                    then()
        return cursor

    def swap_box(self, view: BoxView, name: str, start: int = 0) -> BoxView:
        """Another of the box's strings in the same place and width."""
        new = BoxView(QID, name, start=start)
        new.scale_to_fit_width(view.width)
        new.move_to(view).align_to(view, UP)
        self.play(FadeOut(view), FadeIn(new), run_time=0.8)
        return new


class Opening(BracketScene):
    def construct(self):
        self.opening(QID, "סטודנט", "סוגריים תקינים",
                     ["א · פתרון פשוט", "ב · פתרון יעיל"],
                     ["שאלה 0010 : סוגריים תקינים,\nשאלה ברמת סטודנט.",
                      "שני סעיפים : קודם פתרון פשוט,\nואז פתרון שעובר על המחרוזת פעם אחת."])
        self.fade_all()
        good = VGroup(*[M(s, 48) for s in ["()", "()[]{}", "{[()]}"]]).arrange(DOWN, buff=0.45)
        bad = VGroup(*[M(s, 48) for s in ["(]", "([)]", "((("]]).arrange(DOWN, buff=0.45)
        good.add(self.verdict(True, ORIGIN)).arrange(DOWN, buff=0.45)
        bad.add(self.verdict(False, ORIGIN)).arrange(DOWN, buff=0.45)
        cols = VGroup(good, bad).arrange(RIGHT, buff=3.2, aligned_edge=UP).move_to(UP * 0.7)
        self.say("נתונה מחרוזת של סוגריים משלושה סוגים :\nעגולים, מרובעים ומסולסלים.",
                 FadeIn(good[:-1], lag_ratio=0.2), FadeIn(bad[:-1], lag_ratio=0.2), run_time=1.4)
        self.say("היא תקינה אם כל פותח נסגר בסוגר מאותו סוג,\nוהאחרון שנפתח נסגר ראשון.",
                 FadeIn(good[-1]), FadeIn(bad[-1]))
        self.fade_all()


class ChapterA(BracketScene):
    def construct(self):
        self.chapter_card("סעיף א", "פתרון פשוט",
                          "סעיף א : פתרון פשוט,\nגם אם הוא לא יעיל.")

        # The idea: a valid string always has an adjacent pair, and deleting it keeps the answer.
        row = Row("{[()]}", UP * 0.6)
        self.say("המחרוזת מהעמוד : {[()]}.", FadeIn(row, lag_ratio=0.1), run_time=1.0)
        rings = row.rings([2, 3])
        self.say("הרעיון : במחרוזת תקינה ולא ריקה\nתמיד יש זוג צמוד, כמו () או [].", Create(rings))
        self.remove(rings)
        with self.beat("מוחקים אותו. מה שנשאר תקין\nאם ורק אם המחרוזת המקורית תקינה."):
            row.delete(self, [2, 3])
        with self.beat("עכשיו [] צמוד, ואחריו {}.\nמוחקים גם אותם."):
            row.delete(self, [1, 2])
            row.delete(self, [0, 1])
        ok = self.verdict(True, DOWN * 0.9)
        self.say("לא נשאר כלום : המחרוזת תקינה.", FadeIn(ok))
        self.fade_all()

        row = Row("(())", UP * 0.6)
        self.play(FadeIn(row, lag_ratio=0.1), run_time=0.8)
        with self.beat("מחיקה יכולה ליצור זוג צמוד חדש :\nב-(()) מוחקים את הזוג הפנימי,"):
            row.delete(self, [1, 2])
        with self.beat("ורק אז הזוג החיצוני נהיה צמוד.\nלכן חוזרים על המחיקה, מעבר אחרי מעבר."):
            row.delete(self, [0, 1])
        self.fade_all()

        row = Row("([)]", UP * 0.6)
        self.say("ובמחרוזת ([)] אין אף זוג צמוד :\nאין מה למחוק, והיא לא ריקה.", FadeIn(row, lag_ratio=0.1))
        bad = self.verdict(False, DOWN * 0.9)
        self.say("לכן היא לא תקינה : הסוגר העגול נסגר\nלפני המרובע, שנפתח אחריו.", FadeIn(bad))
        self.fade_all()

        # The code: typed, then run under the row of cells.
        code = page_python(QID, "def isValid_brute")
        steps, result = trace(code, "isValid_brute", ("(())",))
        assert result is True and [s.line for s in steps] == [2, 3, 2, 3, 2, 4], steps
        panel = CodePanel(code, font_size=34)
        self.place_code(panel)
        panel.shift(UP * 0.5)
        centre = np.array([0.0, panel.get_bottom()[1] - 1.0, 0.0])   # the rows, under the code
        self.type_code(panel, [
            (1, "‏isValid_brute מקבלת את המחרוזת s,\nומחזירה True אם היא תקינה."),
            (2, "שורה 2 : הלולאה רצה כל עוד יש במחרוזת\nזוג צמוד, מאחד משלושת הסוגים."),
            (3, "שורה 3 : מעבר אחד מוחק את כל ה-(),\nאחר כך את כל ה-[], ואז את כל ה-{}."),
            (4, "שורה 4 : כשאין יותר זוג צמוד,\nהמחרוזת תקינה רק אם לא נשאר בה כלום."),
        ], intro="עכשיו נכתוב את זה ב-Python.")
        row = Row("(())", centre)
        self.say("נריץ את הקוד על (()).", FadeIn(row, lag_ratio=0.1), run_time=0.8)
        res = self.verdict(True, centre + RIGHT * 3.6)
        cursor = self.run_with(panel, steps, [
            ([2], "יש בה זוג צמוד, ולכן נכנסים ללולאה.", None),
            ([3], "שורה 3 : המעבר הראשון מוחק\nאת הזוג הפנימי, ונשאר ().", lambda: row.one_pass(self)),
            ([2], "המחיקה יצרה זוג צמוד חדש,\nולכן הלולאה ממשיכה.", None),
            ([3], "המעבר השני מוחק אותו,\nונשארת מחרוזת ריקה.", lambda: row.one_pass(self)),
            ([2], "אין יותר זוג צמוד,\nוהלולאה נגמרת.", None),
            ([4], "שורה 4 : המחרוזת ריקה,\nולכן מוחזר True.", lambda: self.play(FadeIn(res))),
        ])
        self.play(FadeOut(res), FadeOut(row), run_time=0.5)

        steps, result = trace(code, "isValid_brute", ("([)]",))
        assert result is False and [s.line for s in steps] == [2, 4], steps
        row = Row("([)]", centre)
        res = self.verdict(False, centre + RIGHT * 3.6)
        self.play(FadeIn(row, lag_ratio=0.1), run_time=0.8)
        cursor = self.run_with(panel, steps, [
            ([2], "על ([)] אין אף זוג צמוד,\nולכן הלולאה לא מתחילה בכלל.", None),
            ([4], "שורה 4 : נשארו ארבעה תווים,\nולכן מוחזר False.", lambda: self.play(FadeIn(res))),
        ], cursor=cursor)
        self.say("שימו לב לתנאי של הלולאה : יש זוג צמוד.\nעם \"המחרוזת לא ריקה\" היא הייתה אינסופית.",
                 Indicate(VGroup(*panel.code.code_lines[1]), color=C.AMBER))
        self.fade_all()

        # The cost: a nested string loses one pair a pass.
        row = Row("(((())))", UP * 1.2, side=0.85, font=50)
        reads = VGroup(M("read:", 34, C.MUTED), M("0", 40, C.AMBER)).arrange(RIGHT, buff=0.3)
        reads.move_to(DOWN * 0.6)
        self.say("כמה זה עולה? ניקח מחרוזת מקוננת,\n‏(((()))), באורך 8.", FadeIn(row, lag_ratio=0.1))
        total = 0
        counts = []
        s = row.s
        while any(p in s for p in PAIRS):
            n = 0
            for p in PAIRS:
                n += len(s)
                s = s.replace(p, "")
            counts.append(n)
        assert counts == [20, 14, 8, 2], counts

        def passes(ns):
            nonlocal total
            for n in ns:
                row.one_pass(self)
                total += n
                self.play(Transform(reads[1], M(str(total), 40, C.AMBER).move_to(reads[1], LEFT)),
                          run_time=0.4)

        with self.beat("כל מעבר מוחק רק את הזוג הפנימי :\nאחרי שני מעברים נשארה (())."):
            self.play(FadeIn(reads), run_time=0.5)
            passes(counts[:2])
        with self.beat("עוד שני מעברים, ורק אז המחרוזת ריקה :\nארבעה מעברים בסך הכול."):
            passes(counts[2:])
        stack = M("stack: 8", 34, C.GREEN).next_to(reads, DOWN, buff=0.45)
        self.say("כל מעבר קורא את המחרוזת שלוש פעמים,\nפעם לכל replace : 44 תווים, לעומת 8.",
                 FadeIn(stack))
        self.fade_all()

        view = BoxView(QID, "passes", width=11.0).move_to(UP * 0.6)
        self.say("גם התיבה שבעמוד מראה את המעברים,\nואת מספר התווים שנקראו בכל אחד.", FadeIn(view))
        self.say("במחרוזת מקוננת באורך n יש n/2 מעברים,\nוכל מעבר עולה O(n) : בסך הכול O(n²).")
        self.fade_all()

        chips = cost_chips(("time", "$O(n^2)$"), ("memory", "$O(n)$"),
                           notes=("a pass per pair", "a new string each pass"))
        self.say("הסיבוכיות : זמן O(n²), וזיכרון O(n)\nלמחרוזות החדשות. אפשר לעשות יותר טוב.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterB(BracketScene):
    def construct(self):
        self.chapter_card("סעיף ב", "פתרון יעיל",
                          "סעיף ב : פתרון שעובר על המחרוזת\nפעם אחת בלבד.")

        # The idea: the last opener is closed first, a stack.
        row = Row("{[()]}", UP * 0.2)
        arcs = VGroup()
        for a, b in [(0, 5), (1, 4), (2, 3)]:
            p, q = row.cells[a].get_top() + UP * 0.1, row.cells[b].get_top() + UP * 0.1
            arcs.add(ArcBetweenPoints(q, p, angle=PI * 0.8, color=C.BLUE, stroke_width=4))
        self.say("הרעיון : הסוגר שנפתח אחרון\nנסגר ראשון.", FadeIn(row, lag_ratio=0.1),
                 Create(arcs, lag_ratio=0.4), run_time=1.6)
        last = VGroup(row.cells[2], row.cells[3])
        ring = SurroundingRectangle(last, color=C.AMBER, buff=0.08, corner_radius=0.12, stroke_width=5)
        self.say("כשמגיע סוגר סוגר, רק הפותח האחרון\nשעוד לא נסגר יכול להתאים לו.", Create(ring))
        lifo = M("last in, first out  →  stack", 38, C.AMBER).move_to(DOWN * 1.5)
        self.say("זו בדיוק מחסנית :\nנכנס אחרון, יוצא ראשון.", FadeIn(lifo))
        self.fade_all()

        # The page's box, alone, on the three strings.
        view = BoxView(QID, "nested", height=5.7).move_to(UP * 0.62)
        self.say("כך זה נראה בתיבה שבעמוד. המחסנית\nמשמאל, ועומק המחסנית בגרף.", FadeIn(view))
        self.box_beat(view, [
            (1, "התו { פותח, ולכן נדחף למחסנית."),
            (2, "גם [ פותח, ונדחף מעליו."),
            (3, "גם ( נדחף, ועכשיו הוא\nבראש המחסנית."),
            (4, "התו ) סוגר. בראש המחסנית ( מאותו סוג,\nולכן מוציאים אותו."),
            (5, "התו ] סוגר את ה-[ שבראש המחסנית."),
            (6, "התו } סוגר את ה-{. המחסנית ריקה :\nהמחרוזת תקינה."),
        ])
        view = self.swap_box(view, "mismatch")
        self.say("עכשיו ([)], שאין בה אף זוג צמוד.")
        with self.beat("‏( ואחריו [ נדחפים למחסנית."):
            self.box_step(view, 1)
            self.box_step(view, 2)
        self.box_beat(view, [
            (3, "התו ) סוגר עגול, אבל בראש המחסנית [ :\nלא תקינה, ועוצרים מיד."),
        ])
        view = self.swap_box(view, "open")
        with self.beat("ובמחרוזת ((( כל תו פותח,\nוכולם נדחפים למחסנית."):
            for k in (1, 2, 3):
                self.box_step(view, k)
        self.say("המחרוזת נגמרה, והמחסנית לא ריקה :\nשלושה פותחים לא נסגרו.")
        self.say("אלה שלושת הכישלונות : סוג לא מתאים,\nסוגר בלי פותח, ופותחים שנשארו.")
        self.fade_all()

        # The code: typed, then run beside the box.
        code = page_python(QID, "def isValid(")
        panel = CodePanel(code, font_size=34, drop_comments=True, drop_trailing_comments=True)

        def fmt(n, s):
            if n not in s:
                return ""
            return s[n] if n == "ch" else "[" + ", ".join(repr(c) for c in s[n]) + "]"

        vp = VarPanel(["ch", "stack"], fmt=fmt, size=30, cols=2, slot=3.2).set_state({})
        self.place_code(panel, vp_width=6.0)
        self.type_code(panel, [
            (1, "‏isValid מקבלת מחרוזת,\nומחזירה True אם היא תקינה."),
            ([2, 3], "שורות 2–3 : אורך אי-זוגי אף פעם לא תקין,\nכי סוגריים באים בזוגות."),
            (5, "שורה 5 : מילון מכל סוגר סוגר\nלפותח מאותו סוג."),
            (6, "שורה 6 : המחסנית, בהתחלה רשימה ריקה."),
            (8, "שורה 8 : עוברים על התווים,\nאחד אחרי השני."),
            ([9, 10, 11, 12], ["שורות 9–11 : לסוגר סוגר צריך את הפותח שלו\nבראש המחסנית. אם אין, מחזירים False.",
                               "שורה 12 : אם הוא שם,\nמוציאים אותו מהמחסנית."]),
            ([13, 14], "שורות 13–14 : סוגר פותח\nנדחף למחסנית."),
            (16, "שורה 16 : בסוף, תקינה רק אם המחסנית ריקה,\nכלומר כל הפותחים נסגרו."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        steps, result = trace(code, "isValid", ("{[()]}",))
        assert result is True, result
        view = BoxView(QID, "nested")
        with self.beat("נריץ על {[()]},\nלצד התיבה מהעמוד."):
            self.split(panel, view, vp)
        push, pop = [8, 9, 14], [8, 9, 10, 12]
        cursor = self.run_code(panel, vp, steps, [
            ([2, 5, 6], "האורך 6, זוגי. המילון מוכן,\nוהמחסנית ריקה.", None),
            (push, "התו { פותח : שורה 14 דוחפת אותו.", 1),
            (push, "גם [ נדחף.", 2),
            (push, "גם ( נדחף. עכשיו במחסנית\nשלושה פותחים.", 3),
            (pop, "התו ) סוגר, ובראש המחסנית ( :\nשורה 12 מוציאה אותו.", 4),
            (pop, "התו ] סוגר את ה-[.", 5),
            (pop, "התו } סוגר את ה-{.", 6),
            ([8, 16], "הלולאה נגמרה והמחסנית ריקה :\nשורה 16 מחזירה True.", None),
        ], view=view)

        steps, result = trace(code, "isValid", ("([)]",))
        assert result is False, result
        self.play(FadeOut(cursor), *vp.show({}, flash=False), run_time=0.4)
        view = self.swap_box(view, "mismatch")
        cursor = self.run_code(panel, vp, steps, [
            ([2, 5, 6], "עכשיו ([)] : האורך 4, זוגי.", None),
            (push, "התו ( נדחף.", 1),
            (push, "התו [ נדחף מעליו.", 2),
            ([8, 9, 10, 11], "התו ) סוגר, ובראש המחסנית [ :\nשורה 11 מחזירה False.", 3),
        ], view=view)

        steps, result = trace(code, "isValid", ("(((",))
        assert result is False and [s.line for s in steps] == [2, 3], steps
        self.play(FadeOut(cursor), *vp.show({}, flash=False), run_time=0.4)
        view = self.swap_box(view, "open", start=3)
        cursor = self.run_code(panel, vp, steps, [
            ([2, 3], "ועל ((( הקוד עוצר כבר בשורה 3 :\nהאורך 3, אי-זוגי, בלי לקרוא אף תו.", None),
        ], view=view)
        self.say("התיבה קוראת עד הסוף ומראה את הפותחים\nשנשארו. הקוד יודע את זה קודם, מהאורך.")

        steps, result = trace(code, "isValid", ("(([]",))
        assert result is False, result
        self.play(FadeOut(cursor), *vp.show({}, flash=False), run_time=0.4)
        view = self.swap_box(view, "even")
        cursor = self.run_code(panel, vp, steps, [
            ([2, 5, 6], "ופותחים שנשארו באורך זוגי? למשל (([] :\nהאורך 4, ולכן הלולאה רצה.", None),
            (push * 3, "שלושת הפותחים נדחפים למחסנית.", 3),
            (pop, "התו ] סוגר את ה-[, ושורה 12 מוציאה אותו.", 4),
            ([8, 16], "הלולאה נגמרה, ונשארו במחסנית (( :\nשורה 16 מחזירה False.", None),
        ], view=view)
        self.fade_all()

        chips = cost_chips(("time", "$O(n)$"), ("memory", "$O(n)$"),
                           notes=("each character once", "the stack, at worst"))
        self.say("הסיבוכיות : כל תו נקרא פעם אחת, זמן O(n),\nוזיכרון O(n) למחסנית במקרה הגרוע.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: counting is not enough.
        steps, result = trace(code, "isValid", (")(",))
        assert result is False and [s.line for s in steps] == [2, 5, 6, 8, 9, 10, 11], steps
        row = Row(")(", UP * 1.0)
        counts = TX(r"\text{opened} = 1,\quad \text{closed} = 1", size=40, color=C.MUTED).move_to(DOWN * 0.5)
        self.say("מלכודת : לא מספיק לספור פותחים וסוגרים.\nב-)( יש אחד מכל סוג.",
                 FadeIn(row, lag_ratio=0.2), FadeIn(counts))
        bad = self.verdict(False, DOWN * 1.5)
        self.say("אבל הסוגר מגיע כשהמחסנית ריקה,\nושורות 10–11 מחזירות False.", FadeIn(bad))
        self.fade_all()


class Closing(BracketScene):
    def construct(self):
        self.closing(QID, [("א", M("delete (), [], {} until none is left", 32)),
                           ("ב", M("a stack: push openers, pop on a match", 32))],
                     ["לסיכום : מחיקת זוגות צמודים, O(n²),\nאו מחסנית במעבר אחד, O(n).",
                      "נסו מחרוזות משלכם בתיבה\nשבעמוד של שאלה 0010 באתר."])
