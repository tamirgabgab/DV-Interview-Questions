"""The tutorial video of question 0011, a random final tic-tac-toe board (script: script.md).

Render with `python videos/render.py 0011` (see VIDEOS.md). The answer is the page's
SystemVerilog class `ttt_end` (the owner, 2026-10-31: a DV question whose answer is SV
constraints types the SV class); it is typed into a scrolling window, then each constraint
stands above the page's box, which shows a board that the constraint keeps or rejects. The
boxes are captured from the built site (BOXES, lib/box_shots.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, MIN_BOX_SCALE, MIN_SPLIT_EM, SAFE_BOTTOM, BoxView, CodePanel,  # noqa: E402
                 DVQScene, M, T, TX, cost_chips, he, page_code)

QID = 11
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – הלוח הרגיל"),
    ("ChapterB", "סעיף ב – אלכסונים מסביב"),
    ("Closing", "סיכום"),
]

PAGE_BOARD = "XXXOXOOOX"

# The page's boxes, captured step by step (lib/box_shots.py). A click on a cell cycles it
# empty -> X -> O; "ex-clear" empties the board; a seed typed into "ex-seed" draws the
# board that "לוח חוקי אקראי" would draw with it (seed 7: X wins, 1: O wins, 2: a draw).
BOXES = {
    "rules": {
        "box": 0,
        "width": 400,
        "region": [".ttt-board svg", ".ttt-panel"],
        "hide": [".ttt-sum"],
        "steps": [
            [],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='2']"]],
            [["click", ".ttt-cell[data-i='3']"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='4']"],
             ["click", ".ttt-cell[data-i='5']"], ["click", ".ttt-cell[data-i='5']"]],
            [["click", ".ttt-cell[data-i='5']"], ["click", ".ttt-cell[data-i='6']"],
             ["click", ".ttt-cell[data-i='6']"]],
            [["click", ".ttt-cell[data-i='6']"]],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='8']"],
             ["click", ".ttt-cell[data-i='0']"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='1']"],
             ["click", ".ttt-cell[data-i='2']"], ["click", ".ttt-cell[data-i='2']"]],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='2']"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='7']"], ["click", ".ttt-cell[data-i='8']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='1']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='4']"],
             ["click", ".ttt-cell[data-i='5']"], ["click", ".ttt-cell[data-i='5']"],
             ["click", ".ttt-cell[data-i='6']"], ["click", ".ttt-cell[data-i='6']"]],
        ],
    },
    "walk": {
        "box": 0,
        "width": 400,
        "region": [".ttt-board svg", ".ttt-panel"],
        "hide": [".ttt-sum"],
        "steps": [
            [],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='2']"]],
            [["click", ".ex-reset"]],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='2']"],
             ["click", ".ttt-cell[data-i='3']"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='4']"],
             ["click", ".ttt-cell[data-i='6']"], ["click", ".ttt-cell[data-i='6']"]],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='8']"],
             ["click", ".ttt-cell[data-i='0']"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='1']"],
             ["click", ".ttt-cell[data-i='2']"], ["click", ".ttt-cell[data-i='2']"]],
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='2']"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='7']"], ["click", ".ttt-cell[data-i='8']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='1']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='4']"],
             ["click", ".ttt-cell[data-i='5']"], ["click", ".ttt-cell[data-i='5']"],
             ["click", ".ttt-cell[data-i='6']"], ["click", ".ttt-cell[data-i='6']"]],
            [["fill", ".ex-seed", 7]],
            [["fill", ".ex-seed", 1]],
            [["fill", ".ex-seed", 2]],
        ],
    },
    "wrap": {
        "box": 0,
        "width": 400,
        "region": ["label:has(.ex-wrap)", ".ttt-board svg", ".ttt-panel"],
        "hide": [".ttt-sum", ".ex-random", ".ex-clear", ".ex-reset", ".ex-seedlab"],
        "steps": [
            [["click", ".ex-clear"], ["click", ".ttt-cell[data-i='0']"],
             ["click", ".ttt-cell[data-i='2']"], ["click", ".ttt-cell[data-i='3']"],
             ["click", ".ttt-cell[data-i='7']"], ["click", ".ttt-cell[data-i='8']"],
             ["click", ".ttt-cell[data-i='1']"], ["click", ".ttt-cell[data-i='1']"],
             ["click", ".ttt-cell[data-i='4']"], ["click", ".ttt-cell[data-i='4']"],
             ["click", ".ttt-cell[data-i='5']"], ["click", ".ttt-cell[data-i='5']"],
             ["click", ".ttt-cell[data-i='6']"], ["click", ".ttt-cell[data-i='6']"]],
            [["check", ".ex-wrap", True]],
        ],
    },
    "five": {
        "box": 1,
        "region": [".ttt-box"],
        "hide": [".tf-sum"],
        "steps": [
            [],
            [["click", ".tf-cell[data-c='8']"]],
            [["click", ".tf-cell[data-c='8']"], ["click", ".tf-cell[data-c='2']"]],
        ],
    },
}

SV_CLASS = page_code(QID, "systemverilog", "class ttt_end")
SV_SHOW = set(range(44, 50))          # show(): it only prints the board, left out of the picture

# The 12 lines in their four directions (part b): each direction, three parallel lines.
DIRECTIONS = [
    ("rows", [(0, 1, 2), (3, 4, 5), (6, 7, 8)]),
    ("columns", [(0, 3, 6), (1, 4, 7), (2, 5, 8)]),
    ("↘ wrap", [(0, 4, 8), (1, 5, 6), (2, 3, 7)]),
    ("↙ wrap", [(2, 4, 6), (0, 5, 7), (1, 3, 8)]),
]


def mini_board(marks: str = ".........", cell: float = 0.8, tint: dict | None = None,
               numbers: bool = True) -> VGroup:
    """A 3x3 board: X and O drawn as marks, empty cells with their number (muted)."""
    tint = tint or {}
    g = VGroup()
    for i, m in enumerate(marks):
        x, y = (i % 3 - 1) * cell, (1 - i // 3) * cell
        sq = Square(cell, stroke_color=C.FAINT, stroke_width=2,
                    fill_color=tint.get(i, C.NAVY_LIGHT), fill_opacity=0.9 if i in tint else 1)
        sq.move_to([x, y, 0])
        g.add(sq)
        if m == "X":
            d = cell * 0.27
            g.add(VGroup(Line([x - d, y - d, 0], [x + d, y + d, 0]),
                         Line([x - d, y + d, 0], [x + d, y - d, 0])).set_stroke(C.WHITE, 5))
        elif m == "O":
            g.add(Circle(radius=cell * 0.29, stroke_color=C.WHITE, stroke_width=5).move_to([x, y, 0]))
        elif numbers:
            g.add(M(str(i), 22 * cell / 0.8, C.MUTED).move_to([x, y, 0]))
    return g


def dedent(code: str, lines) -> str:
    """`code` with the common indentation of its page lines `lines` taken off them (the
    other lines as they are), so a panel of those lines starts at its left edge."""
    rows = code.split("\n")
    shown = [rows[n - 1] for n in lines if rows[n - 1].strip()]
    cut = min(len(r) - len(r.lstrip()) for r in shown)
    return "\n".join(r[cut:] if n in lines else r for n, r in enumerate(rows, start=1))


def cell_center(board: VGroup, i: int, cell: float = 0.8):
    return board.get_center() + np.array([(i % 3 - 1) * cell, (1 - i // 3) * cell, 0])


class TTTScene(DVQScene):
    """Helpers shared by the chapters of 0011."""

    def box_step(self, view, k, run_time: float = 0.5, ring_time: float = 0.18):
        """dvq's box_step with one ring per clicked control (a cell clicked twice, for an O,
        is one ring) and quicker rings, since a board is built with many clicks."""
        if k == view.k:
            return
        rings, seen = [], set()
        for centre, w, h in view.clicks(k):
            key = (round(centre[0], 2), round(centre[1], 2))
            if key in seen:
                continue
            seen.add(key)
            ring = RoundedRectangle(width=w + 0.12, height=h + 0.12,
                                    corner_radius=min(0.2, (h + 0.12) / 2),
                                    stroke_color=C.AMBER, stroke_width=5, fill_opacity=0)
            ring.move_to(centre)
            self.play(FadeIn(ring, scale=1.6), run_time=ring_time)
            rings.append(ring)
        new = view._image(k)
        self.play(FadeIn(new), run_time=run_time)
        view.remove(view.image)
        self.remove(view.image)
        view.image = new
        view.submobjects.insert(0, new)
        view.k = k
        if rings:
            self.play(*[FadeOut(r) for r in rings], run_time=0.3)
        self.remove(new)
        self.add(view)

    def stack(self, view_name: str, groups: list):
        """The constraints above the page's box: `groups` is [(page lines, [(k, caption),
        ...]), ...]. The SV lines of a group stand at the top, full width (they are too wide
        to share the frame side by side), and the box under them steps to picture k under
        each caption."""
        top, bottom = 3.65, SAFE_BOTTOM + 0.12
        panels = []
        for lines, _ in groups:
            p = CodePanel(dedent(SV_CLASS, lines), font_size=24, drop_trailing_comments=True,
                          language="systemverilog", only=set(lines))
            if p.width > 13.4:
                p.scale(13.4 / p.width)
            p.move_to([0, top - p.height / 2, 0])
            panels.append(p)
        room = top - max(p.height for p in panels) - 0.12 - bottom
        view = BoxView(QID, view_name, height=room)
        view.move_to([0, bottom + room / 2, 0])
        for p in panels:
            em = p.em_px()
            if em < MIN_SPLIT_EM:
                self.problems.append(f"code above the box {em:.1f} px high (at least {MIN_SPLIT_EM})")
        if view.css_scale() < MIN_BOX_SCALE:
            self.problems.append(f"box at {view.css_scale():.2f} of its page size (at least {MIN_BOX_SCALE})")
        self.code_ems.append(min(p.em_px() for p in panels))
        print(f"stack: box at {view.css_scale():.2f} of its page size, code {min(p.em_px() for p in panels):.1f} px")
        current = None
        for (lines, steps), panel in zip(groups, panels):
            for j, (k, caption) in enumerate(steps):
                with self.beat(caption):
                    if j == 0:
                        if current is None:
                            self.play(FadeIn(panel), FadeIn(view), run_time=0.8)
                        else:
                            self.play(FadeOut(current), FadeIn(panel), run_time=0.6)
                        current = panel
                    self.box_step(view, k)
        return view

    def bars(self, title: str, values: list, labels=("X", "O", "draw"), maxh: float = 3.0):
        """Three bars with their share in %, a Latin title over them."""
        colors = [C.AMBER, C.BLUE, C.GREEN]
        g = VGroup()
        for v, lab, col in zip(values, labels, colors):
            h = max(0.04, maxh * v / 100)
            bar = Rectangle(width=0.9, height=h, fill_color=col, fill_opacity=0.9, stroke_width=0)
            num = M(f"{v:g}%", 28, col).next_to(bar, UP, buff=0.15)
            name = M(lab, 28, C.MUTED).next_to(bar, DOWN, buff=0.2)
            g.add(VGroup(bar, num, name))
        g.arrange(RIGHT, buff=0.7, aligned_edge=DOWN)
        head = T(title, 28, C.WHITE).next_to(g, UP, buff=0.5)
        return VGroup(head, g)


class Opening(TTTScene):
    def construct(self):
        self.opening(QID, "סניור", "לוח סיום אקראי של איקס-עיגול",
                     ["א · הלוח הרגיל", "ב · אלכסונים מסביב"],
                     ["שאלה 0011 : לוח סיום אקראי של איקס-עיגול,\nשאלה ברמת סניור.",
                      "שני סעיפים : הלוח הרגיל,\nואלכסונים שממשיכים מהצד השני."])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.8)
        board = mini_board(PAGE_BOARD, cell=1.1).move_to(LEFT * 2.6 + UP * 0.6)
        results = VGroup(*[M(r, 36, c) for r, c in (("X_WINS", C.AMBER), ("O_WINS", C.BLUE),
                                                    ("DRAW", C.GREEN))]).arrange(DOWN, buff=0.45)
        results.move_to(RIGHT * 3.0 + UP * 0.6)
        ring = SurroundingRectangle(results[0], color=C.AMBER, buff=0.15, corner_radius=0.1)
        self.say("צריך לייצר לוח שבו נגמר משחק,\nויחד איתו את התוצאה : X, O או תיקו.",
                 FadeIn(board), FadeIn(results, lag_ratio=0.2), Create(ring), run_time=1.6)
        self.fade_all()


class ChapterA(TTTScene):
    def construct(self):
        self.chapter_card("סעיף א", "הלוח הרגיל", "סעיף א : מהם כל התנאים של לוח סיום,\nואיך כותבים אותם כ-constraints?")

        # The problem: the numbering, X starts, the players alternate.
        empty = mini_board(cell=1.1).move_to(UP * 0.7)
        self.say("המשבצות ממוספרות מ-0 עד 8, שורה אחרי שורה.\n‏X תמיד מתחיל, והשחקנים משחקים לסירוגין.",
                 FadeIn(empty, lag_ratio=0.05))
        self.fade_all()

        # The conditions, on the page's box.
        view = BoxView(QID, "rules", height=5.8).move_to(UP * 0.62)
        self.say("זו התיבה מהעמוד, עם הלוח של השאלה :\nל-X שתי שלישיות, והוא ניצח.", FadeIn(view))
        self.box_beat(view, [
            (1, "תנאי 1, הספירה : X מתחיל ומשחקים לסירוגין.\nשלושה X בלי אף O לא קורה במשחק."),
            (2, "תנאי 2 : אין שני מנצחים.\nהמשחק נעצר ברגע שמישהו השלים שלישייה."),
            (3, "והתנאי שרוב המועמדים שוכחים : ל-X שלישייה,\nאבל n_X = n_O. כלומר O שיחק אחרי הניצחון."),
            (4, "בלי ה-O האחרון יש n_X = n_O + 1.\nמי שניצח הוא זה ששיחק אחרון."),
            (5, "ובאותו אופן ל-O : שלישייה של O,\nאין שלישייה של X, ו-n_X = n_O."),
            (6, "ותיקו : לוח מלא, חמישה X וארבעה O,\nבלי אף שלישייה."),
        ])
        self.fade_all()

        rules = VGroup(
            TX(r"n_X \in \{\, n_O,\ n_O + 1 \,\}", size=36, color=C.WHITE),
            TX(r"\texttt{X\_WINS}:\ \ \texttt{x\_lines} > 0,\ \ \texttt{o\_lines} = 0,\ \ n_X = n_O + 1", size=34, color=C.AMBER),
            TX(r"\texttt{O\_WINS}:\ \ \texttt{o\_lines} > 0,\ \ \texttt{x\_lines} = 0,\ \ n_X = n_O", size=34, color=C.BLUE),
            TX(r"\texttt{DRAW}:\ \ \texttt{x\_lines} = 0,\ \ \texttt{o\_lines} = 0,\ \ n_X + n_O = 9", size=34, color=C.GREEN),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.6)
        self.say("ארבעה תנאים : הספירה, ותנאי לכל תוצאה.\nכל אחד מהם יהפוך ל-constraint.",
                 FadeIn(rules, lag_ratio=0.25), run_time=2.0)
        self.fade_all()

        # The class, typed into a scrolling window.
        panel = CodePanel(SV_CLASS, font_size=30, drop_comments=True, drop_trailing_comments=True,
                          language="systemverilog", rows=14, only=set(range(1, 51)) - SV_SHOW)
        self.place_code(panel)
        self.type_code(panel, [
            ([1, 2, 3], ["שלושה טיפוסים : משבצת היא EMPTY, X או O,\nוהתוצאה היא אחת משלוש.",
                         "הלוח הוא מערך של 9 משבצות,\nממוספרות מ-0 עד 8."]),
            (5, "המחלקה ttt_end. כל קריאה ל-randomize()\nתיתן לוח סיום ותוצאה שמתאימה לו."),
            ([7, 8, 9, 10, 11], "טבלת הקווים : שורות, טורים ושני אלכסונים.\nארבעת האחרונים שמורים לסעיף ב."),
            (12, "‏n_lines = 8 בלוח הרגיל. הוא לא rand,\nולכן בעיני ה-solver הוא קבוע."),
            ([14, 15], "הלוח והתוצאה הם rand :\nה-solver בוחר את שניהם יחד."),
            ([16, 17, 18], "ועוד משתני עזר, גם הם rand :\nכמה X וכמה O, ואילו קווים שלמים."),
            ([20, 21, 22, 23, 24], "‏c_count : משתני העזר שווים לספירה על הלוח,\nו-n_x הוא n_o או n_o + 1."),
            ([26, 27, 28, 29, 30, 31, 32],
             "‏c_lines : x_line[l] הוא 1 בדיוק כשהקו פעיל\nוכל שלוש המשבצות שלו X."),
            ([33, 34, 35], "‏x_lines ו-o_lines סופרים את הקווים השלמים.\nה-int' מרחיב את הסכום מעבר לביט אחד."),
            ([37, 38, 39, 40], ["‏c_result : כל תוצאה גוררת את התנאים שלה,\nבדיוק התנאים מהתיבה.",
                                "חץ ולא שוויון : התנאים זרים זה לזה,\nולכן כל לוח קובע תוצאה אחת."]),
            ([41, 42], "‏solve result before board : קודם תוצאה\nבהסתברות שווה, ורק אחר כך לוח."),
            (50, "והמחלקה נסגרת. בעמוד יש גם show(),\nשרק מדפיסה את הלוח, ולכן היא לא כאן."),
        ], intro="עכשיו נכתוב את המחלקה ב-SystemVerilog,\nחלק אחרי חלק.")
        self.fade_all()

        # Each constraint above the box.
        self.stack("walk", [
            ([23], [(1, "ב-c_count : שלושה X ואפס O.\nאין n_o שמקיים את זה, והלוח נפסל.")]),
            ([33], [(2, "ב-c_lines : בלוח של השאלה שני קווים של X שלמים,\nולכן x_lines = 2.")]),
            ([38], [(3, "‏X_WINS דורש n_x == n_o + 1.\nכאן n_x == n_o : O שיחק אחרי הניצחון.")]),
            ([39], [(4, "‏O_WINS : שלישייה של O, אין של X,\nו-n_x == n_o, כי O שיחק אחרון.")]),
            ([40], [(5, "‏DRAW : לוח מלא בלי שלישיות. בלי n_x + n_o == 9\nגם לוח באמצע משחק היה תיקו.")]),
            ([41], [(6, "עם solve before, ה-solver בוחר קודם תוצאה.\nבהגרלה הזו יצא X_WINS."),
                    (7, "בהגרלה הבאה יצא O_WINS."),
                    (8, "ובשלישית תיקו, שיוצא בשליש מההגרלות.")]),
        ])
        self.fade_all()

        # The distribution, with and without solve ... before.
        plain = self.bars("randomize()", [65.3, 33.0, 1.7]).move_to(LEFT * 3.4 + UP * 0.4)
        self.say("יש 958 לוחות סיום : 626 של X, 316 של O, ו-16 תיקו.\nבלי solve before, כל לוח מוגרל באותה הסתברות.",
                 FadeIn(plain[0]), *[GrowFromEdge(b[0], DOWN) for b in plain[1]],
                 *[FadeIn(b[1:]) for b in plain[1]], run_time=1.6)
        solved = self.bars("solve result before board", [33.3, 33.3, 33.3]).move_to(RIGHT * 3.4 + UP * 0.4)
        self.say("אז X מנצח ב-65% מההגרלות, ותיקו רק ב-1.7%.\nעם solve before, כל תוצאה מקבלת שליש.",
                 FadeIn(solved[0]), *[GrowFromEdge(b[0], DOWN) for b in solved[1]],
                 *[FadeIn(b[1:]) for b in solved[1]], run_time=1.6)
        self.say("אותם 958 לוחות, בהתפלגות אחרת :\nהמקרה הנדיר, התיקו, נבדק הרבה יותר.")
        self.fade_all()

        chips = cost_chips(("fillings", "$3^9 = 19{,}683$"), ("final", "958"),
                           notes=("every board of 9 cells", "626 X · 316 O · 16 draw"))
        self.say("מרחב הפתרונות קטן : 3 בחזקת 9 מילויים,\nומהם רק 958 הם לוחות סיום.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()

        # The trap: exactly one line for the winner.
        board = mini_board(PAGE_BOARD, cell=1.1, numbers=False).move_to(UP * 0.6)
        l1 = Line(cell_center(board, 0, 1.1), cell_center(board, 2, 1.1), color=C.AMBER, stroke_width=8)
        l2 = Line(cell_center(board, 0, 1.1), cell_center(board, 8, 1.1), color=C.AMBER, stroke_width=8)
        self.say("מלכודת : לדרוש שלמנצח שלישייה אחת בלבד.\nכאן X סגר שתיים במהלך אחד, במשבצת 0.",
                 FadeIn(board), Create(l1), Create(l2))
        self.say("‏constraint חזק מדי מסתיר לוחות חוקיים,\nואף בדיקה לא תתריע עליו.")
        self.fade_all()


class ChapterB(TTTScene):
    def construct(self):
        self.chapter_card("סעיף ב", "אלכסונים מסביב", "סעיף ב : אלכסון ממשיך מהצד השני של הלוח,\nכאילו הלוח מודבק לעצמו.")

        ex = mini_board(cell=1.0).move_to(UP * 0.6)
        tint = {i: C.AMBER for i in (0, 5, 7)}
        ex2 = mini_board(cell=1.0, tint=tint).move_to(UP * 0.6)
        self.say("למשל המשבצות 0, 5 ו-7 :\nיורדים שמאלה, יוצאים מהלוח וחוזרים מימין.",
                 FadeIn(ex), Transform(ex, ex2))
        self.fade_all()

        colors = [C.BLUE, C.ORANGE, C.GREEN]
        boards = VGroup()
        for name, lines in DIRECTIONS:
            tint = {c: colors[j] for j, line in enumerate(lines) for c in line}
            b = mini_board(cell=0.62, tint=tint)
            boards.add(VGroup(b, M(name, 26, C.MUTED).next_to(b, DOWN, buff=0.25)))
        boards.arrange(RIGHT, buff=0.8).move_to(UP * 0.6)
        self.say("ארבעה קווים חדשים, ובסך הכול 12 קווים :\nארבעה כיוונים, בכל אחד שלושה קווים מקבילים.",
                 FadeIn(boards, lag_ratio=0.25), run_time=2.0)
        self.say("התנאים לא משתנים, רק קבוצת הקווים.\nבמחלקה זה משתנה אחד : n_lines.")
        self.fade_all()

        snippet = page_code(QID, "systemverilog", "t.n_lines = 12")
        panel = CodePanel(snippet, font_size=30, drop_trailing_comments=True, language="systemverilog")
        self.place_code(panel)
        self.type_code(panel, [
            (1, "יוצרים אובייקט של המחלקה מסעיף א."),
            (2, "‏n_lines = 12 מדליק את ארבעת הקווים החדשים.\nאף שורה ב-constraints לא משתנה."),
            (3, "הגרלה רגילה : X או O,\nכל אחד בחצי מההגרלות."),
            ([4, 5], "‏randomize() with מוסיף constraint זמני.\nכאן הוא תמיד נכשל, כי אין תיקו."),
        ], intro="כך משתמשים במחלקה עם 12 הקווים.")
        self.fade_all()

        view = BoxView(QID, "wrap", height=5.8).move_to(UP * 0.62)
        self.say("בתיבה : לוח מלא בלי שלישייה,\nתיקו עם 8 הקווים.", FadeIn(view))
        self.box_beat(view, [
            (1, "מדליקים את האלכסונים מסביב :\nעכשיו גם ל-X וגם ל-O יש שלישייה."),
        ])
        self.fade_all()

        # The proof: every 5 cells contain a line.
        steps = VGroup(
            TX(r"\text{5 cells, no line: every direction splits them } 2 + 2 + 1", size=34),
            TX(r"2 + 2 + 1 \;\to\; 2 \text{ pairs on a line per direction}", size=34),
            TX(r"4 \text{ directions} \times 2 = 8 \text{ pairs}", size=34, color=C.AMBER),
            TX(r"5 \text{ cells: } \binom{5}{2} = 10 \text{ pairs, each on exactly one line}", size=34, color=C.BLUE),
            TX(r"8 \neq 10", size=46, color=C.RED),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.6)
        self.say("תיקו דורש לוח מלא : חמישה X בלי שלישייה.\nנראה שכל 5 משבצות מכילות קו.")
        self.say("נניח שאין קו. בכל כיוון המשבצות מתחלקות 2, 2, 1,\nולכן יש בו 2 זוגות על קו.",
                 FadeIn(steps[0]), FadeIn(steps[1]))
        self.say("בארבעת הכיוונים : 8 זוגות.\nאבל ל-5 משבצות יש 10 זוגות.",
                 FadeIn(steps[2]), FadeIn(steps[3]))
        self.say("וכל זוג משבצות נמצא על קו אחד בדיוק.\nסתירה : אין 5 משבצות בלי קו.", FadeIn(steps[4], scale=1.3))
        self.fade_all()

        five = BoxView(QID, "five", height=5.85).move_to(UP * 0.6)
        self.say("בתיבה : ריבוע של 4 משבצות בלי קו.\nהכוכבים : כל משבצת ריקה משלימה קו.", FadeIn(five))
        self.box_beat(five, [
            (1, "משבצת 8 משלימה שני קווים : האלכסון 0, 4, 8,\nוגם 1, 3, 8, שממשיך מהצד השני."),
            (2, "ומשבצת 2 משלימה את השורה העליונה."),
        ])
        self.fade_all()

        bars = self.bars("12 lines: 1,314 final boards", [882 / 13.14, 432 / 13.14, 0.0])
        for b, n in zip(bars[1], ("882", "432", "0")):
            b[1].become(M(n, 28, b[1].get_color()).move_to(b[1]))
        bars.move_to(UP * 0.4)
        self.say("עם 12 הקווים יש 1,314 לוחות סיום :\n‏882 של X, 432 של O, ואף תיקו.",
                 FadeIn(bars[0]), *[GrowFromEdge(b[0], DOWN) for b in bars[1]],
                 *[FadeIn(b[1:]) for b in bars[1]], run_time=1.6)
        self.say("ה-solver לא מוצא אף פתרון עם DRAW :\nהוא מוכיח את המשפט בשבילנו.")
        self.fade_all()


class Closing(TTTScene):
    def construct(self):
        self.closing(QID, [("א", M("4 conditions -> 958 boards: 626 X, 316 O, 16 draw", 28)),
                           ("ב", M("12 lines -> 1,314 boards, and no draw", 28))],
                     ["לסיכום : ארבעה תנאים, וכל תנאי הופך ל-constraint.\nמי שניצח הוא זה ששיחק אחרון.",
                      "ועם האלכסונים מסביב אין תיקו.\nנסו בתיבה שבעמוד של שאלה 0011."])
