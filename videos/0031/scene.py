"""The tutorial video of question 0031, the bridge and the torch (script: script.md).

Render with `python videos/render.py 0031` (see VIDEOS.md). Part א draws the four people
(1, 2, 5 and 10 minutes), the bridge and the torch in Manim with a running clock: first the
plan that comes to mind, the fastest escorts everyone (19 minutes), then the two slow ones
together (17); the page's box plays the 17 plan and compares the plans; then the proof that
17 is the least, by cases (C not with D: 10 + 5 + 3 = 18 at least; C with D: 2 + 1 + 10 +
2 + 2 = 17 at least), a time axis per case. Part ב: the state (who is across, the torch's
side), why BFS is not enough, the page's `bridge` typed, and its run on 1, 2, 5, 10 traced
pop by pop from the heap (the first pops line by line, then from pop to pop, a log of the
popped states beside the code), the walk back by the parents, and the box playing the plan.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, PX, SAFE_BOTTOM, TX, BoxView, Bounded, CodePanel, DVQScene, M, T,  # noqa: E402
                 VarPanel, baseline_text, cost_chips, he, page_python, trace)

QID = 31
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – ארבעה אנשים : 1, 2, 5 ו-10"),
    ("ChapterB", "סעיף ב – קוד : כל מספר אנשים"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="bridge", times 1 2 5 10). "plans": the table of the three plans
# (the search, the fastest escorts everyone, the two slow ones together). "best": the
# search's plan, picture k after k crossings (a click on "next crossing" each).
BOXES = {
    "plans": {"box": 0, "region": [".bridge-plans"], "steps": [[["check", ".ex-greedy", False]]]},
    "best": {"box": 0, "region": [".ex-play-row", ".bridge-frame", ".bridge-caption"],
             "steps": [[["check", ".ex-greedy", False]], {"do": [["click", ".ex-next"]], "repeat": 5}]},
}

TIMES = [1, 2, 5, 10]
NAMES = "ABCD"
ESCORT = [((0, 3), 10), ((0,), 1), ((0, 2), 5), ((0,), 1), ((0, 1), 2)]
PAIR = [((0, 1), 2), ((0,), 1), ((2, 3), 10), ((1,), 2), ((0, 1), 2)]

# The stage: two banks, the river and the bridge between them.
NEAR_SLOTS = [(-5.6, 1.35), (-4.0, 1.35), (-5.6, -0.15), (-4.0, -0.15)]
FAR_SLOTS = [(4.0, 1.35), (5.6, 1.35), (4.0, -0.15), (5.6, -0.15)]
BRIDGE_Y = 0.55
TORCH_AT = {0: np.array([-4.8, -1.05, 0]), 1: np.array([4.8, -1.05, 0])}


def state_name(across: int, side: int) -> str:
    who = "".join(NAMES[i] for i in range(4) if across >> i & 1) or "-"
    return f"({who}, {'far' if side else 'near'})"


class Person(VGroup):
    """One of the four: a disc with the minutes in it and the letter under it."""

    def __init__(self, i: int):
        super().__init__()
        self.i = i
        self.disc = Circle(radius=0.42, stroke_color=C.MUTED, stroke_width=4,
                           fill_color=C.NAVY_LIGHT, fill_opacity=1)
        self.num = M(str(TIMES[i]), 36).move_to(self.disc)
        self.letter = T(NAMES[i], 28, C.MUTED).next_to(self.disc, DOWN, buff=0.1)
        self.add(self.disc, self.num, self.letter)


def torch() -> VGroup:
    flame = Polygon([0, 0.32, 0], [0.13, 0.05, 0], [0, -0.04, 0], [-0.13, 0.05, 0],
                    stroke_width=0, fill_color=C.AMBER, fill_opacity=1)
    stick = Rectangle(width=0.07, height=0.32, stroke_width=0, fill_color=C.WHITE,
                      fill_opacity=1).next_to(flame, DOWN, buff=0)
    return VGroup(flame, stick)


class Stage(Group):
    """The banks, the river, the bridge, the people, the torch and the clock."""

    def __init__(self):
        super().__init__()
        self.near_bank = RoundedRectangle(width=3.6, height=3.9, corner_radius=0.15, stroke_width=0,
                                          fill_color=C.NAVY_LIGHT, fill_opacity=0.55).move_to([-4.8, 0.45, 0])
        self.far_bank = self.near_bank.copy().move_to([4.8, 0.45, 0])
        river = Rectangle(width=6.0, height=3.9, stroke_width=0, fill_color=C.BLUE,
                          fill_opacity=0.14).move_to([0, 0.45, 0])
        plank = Rectangle(width=6.0, height=0.8, stroke_color=C.MUTED, stroke_width=2,
                          fill_color=C.NAVY_DARK, fill_opacity=1).move_to([0, BRIDGE_Y, 0])
        self.labels = Group(he("הגדה הקרובה", 28, C.MUTED).move_to([-4.8, 2.1, 0]),
                            he("הגדה הרחוקה", 28, C.MUTED).move_to([4.8, 2.1, 0]))
        self.people = [Person(i).move_to([*NEAR_SLOTS[i], 0]) for i in range(4)]
        self.torch = torch().move_to(TORCH_AT[0])
        self.tv = ValueTracker(0)
        self.clock = always_redraw(lambda: M(f"t = {round(self.tv.get_value())}", 44, C.AMBER,
                                             weight="BOLD").move_to([0, 3.15, 0]))
        self.far = set()
        self.side = 0
        self.add(self.near_bank, self.far_bank, river, plank, self.labels, *self.people,
                 self.torch, self.clock)

    def slot(self, i: int, far: bool):
        return np.array([*(FAR_SLOTS if far else NEAR_SLOTS)[i], 0])

    def cross(self, scene: DVQScene, group: tuple, minutes: int):
        """One crossing: the group walks over the bridge with the torch, the clock runs."""
        forward = self.side == 0
        movers = [self.people[i] for i in group]
        sgn = 1 if forward else -1
        xs = [-0.55, 0.55] if len(group) == 2 else [0.0]
        start = [np.array([-2.4 * sgn + x, BRIDGE_Y, 0]) for x in xs]
        end = [np.array([2.4 * sgn + x, BRIDGE_Y, 0]) for x in xs]
        for p, s in zip(movers, start):
            p.generate_target()
            p.target.move_to(s)
            p.target.disc.set_stroke(C.AMBER)
        scene.play(*[MoveToTarget(p) for p in movers],
                   self.torch.animate.move_to([-1.6 * sgn, BRIDGE_Y + 0.9, 0]), run_time=0.6)
        t0 = self.tv.get_value()
        scene.play(*[p.animate.move_to(e) for p, e in zip(movers, end)],
                   self.torch.animate.move_to([1.6 * sgn, BRIDGE_Y + 0.9, 0]),
                   self.tv.animate.set_value(t0 + minutes), run_time=1.4,
                   rate_func=rate_functions.linear)
        for i in group:
            if forward:
                self.far.add(i)
            else:
                self.far.discard(i)
        self.side = 1 - self.side
        for p in movers:
            p.generate_target()
            p.target.move_to(self.slot(p.i, forward))
            p.target.disc.set_stroke(C.GREEN if forward else C.MUTED)
        scene.play(*[MoveToTarget(p) for p in movers],
                   self.torch.animate.move_to(TORCH_AT[self.side]), run_time=0.6)


class Tally(VGroup):
    """The sum of the crossings so far, under the stage: "10 + 1 + 5 ..."."""

    def __init__(self, y: float = -1.95):
        super().__init__()
        self.y, self.terms = y, []
        self.text = M("", 38).move_to([0, y, 0])
        self.add(self.text)

    def push(self, minutes: int, total: int | None = None):
        self.terms.append(str(minutes))
        s = " + ".join(self.terms) + (f" = {total}" if total is not None else "")
        new = M(s, 38, C.AMBER if total is not None else C.WHITE).move_to([0, self.y, 0])
        return Transform(self.text, new)


class BridgeScene(DVQScene):
    """Helpers shared by the chapters of 0031."""

    def time_bar(self, parts: list, y: float, unit: float = 0.5, x0: float = -5.4) -> VGroup:
        """A time axis: one block per crossing, `unit` per minute, its minutes in it."""
        bar = VGroup()
        x = x0
        for minutes, color in parts:
            w = minutes * unit
            r = Rectangle(width=w, height=0.62, stroke_color=C.NAVY, stroke_width=3,
                          fill_color=color, fill_opacity=0.85).move_to([x + w / 2, y, 0])
            n = M(str(minutes), 30, C.NAVY, weight="BOLD").move_to(r)
            bar.add(VGroup(r, n))
            x += w
        return bar


class Opening(BridgeScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "הגשר והלפיד",
                     ["א · ארבעה אנשים", "ב · כל מספר אנשים"],
                     ["שאלה 0031 : הגשר והלפיד,\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : ארבעה אנשים ביד,\nואז קוד שמוצא את המינימום לכל מספר."])
        self.fade_all()


class ChapterA(BridgeScene):
    def construct(self):
        self.chapter_card("סעיף א", "ארבעה אנשים : 1, 2, 5 ו-10",
                          "סעיף א : מה הזמן הקצר ביותר\nשבו ארבעתם עוברים את הגשר?")

        # The problem.
        st = Stage()
        rest = [m for m in st.submobjects if m not in (*st.people, st.torch, st.clock)]
        self.say("ארבעה אנשים מגיעים בלילה לגשר צר.\nהזמנים שלהם : 1, 2, 5 ו-10 דקות.",
                 FadeIn(Group(*rest)), LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in st.people],
                                                   lag_ratio=0.2), run_time=1.6)
        self.say("יש להם לפיד אחד, ובלי לפיד\nאי אפשר לחצות.", FadeIn(st.torch, scale=1.5),
                 FadeIn(st.clock))
        self.say("על הגשר לכל היותר שניים בבת אחת,\nוזוג הולך בקצב של האיטי מביניהם.")
        self.say("והלפיד צריך לחזור עם מישהו,\nכדי שהבאים יוכלו לחצות.")

        # The trap: the fastest escorts everyone.
        tally = Tally()
        self.add(tally)
        self.say("התוכנית הראשונה שעולה : A, המהיר ביותר,\nמלווה כל אחד ומחזיר את הלפיד.")
        captions = [
            "‏A ו-D חוצים יחד : 10 דקות,\nהקצב של D.",
            "‏A חוזר עם הלפיד : עוד דקה.",
            "‏A ו-C חוצים : 5 דקות.\nעברו 16.",
            "‏A חוזר שוב : דקה אחת.",
            "‏A ו-B חוצים : 2 דקות.\nכולם בצד הרחוק אחרי 19 דקות.",
        ]
        total = 0
        for (group, minutes), cap in zip(ESCORT, captions):
            total += minutes
            with self.beat(cap):
                st.cross(self, group, minutes)
                self.play(tally.push(minutes, total if total == 19 else None), run_time=0.5)
        self.say("‏19 נראה סביר : המהיר תמיד מחזיר.\nאבל אפשר פחות.",
                 Indicate(tally, color=C.RED, scale_factor=1.06))
        self.fade_all()

        # The idea: the two slow ones together.
        a = self.time_bar([(10, C.AMBER), (1, C.BLUE), (5, C.ORANGE), (1, C.BLUE), (2, C.BLUE)], 1.4)
        b = self.time_bar([(2, C.BLUE), (1, C.BLUE), (10, C.AMBER), (2, C.BLUE), (2, C.BLUE)], -0.4)
        la = TX("= 19", size=40, color=C.RED).next_to(a, RIGHT, buff=0.35)
        lb = TX("= 17", size=40, color=C.GREEN).next_to(b, RIGHT, buff=0.35)
        ta = T("A escorts everyone", 30, C.MUTED).next_to(a, UP, buff=0.25).align_to(a, LEFT)
        tb = T("C and D together", 30, C.MUTED).next_to(b, UP, buff=0.25).align_to(b, LEFT)
        self.say("הבעיה : התוכנית משלמת גם את ה-10\nוגם את ה-5, בשתי חציות שונות.",
                 FadeIn(a, lag_ratio=0.2), FadeIn(ta), FadeIn(la), run_time=1.4)
        self.say("הרעיון : אם C ו-D חוצים באותו זוג,\nה-5 נבלע ב-10, ומשלמים רק 10.",
                 Indicate(a[2], color=C.RED))
        self.say("המחיר : מישהו מהיר צריך כבר לחכות\nבצד הרחוק, כדי להחזיר את הלפיד.",
                 FadeIn(b, lag_ratio=0.2), FadeIn(tb), FadeIn(lb), run_time=1.4)
        self.say("לכן שולחים את שני המהירים ראשונים.\nנראה את זה על הגשר.")
        self.fade_all()

        # The 17 plan.
        st = Stage()
        tally = Tally()
        self.play(FadeIn(st), run_time=0.8)
        self.add(tally)
        captions = [
            "שלב 1 : A ו-B חוצים, 2 דקות.\n‏B יחכה בצד הרחוק.",
            "שלב 2 : A חוזר עם הלפיד, דקה.\nעברו 3 דקות.",
            "שלב 3 : C ו-D חוצים יחד, 10 דקות.\nהזמן של C נבלע. עברו 13.",
            "שלב 4 : B, שחיכה, מחזיר את הלפיד.\n‏2 דקות, עברו 15.",
            "שלב 5 : A ו-B חוצים, 2 דקות.\nכולם בצד הרחוק אחרי 17 דקות.",
        ]
        total = 0
        for (group, minutes), cap in zip(PAIR, captions):
            total += minutes
            with self.beat(cap):
                st.cross(self, group, minutes)
                self.play(tally.push(minutes, total if total == 17 else None), run_time=0.5)
        self.say("‏17 ולא 19 : במקום ה-5 משלמים פעמיים 2\nועוד דקה, ארבע דקות בלבד.",
                 Indicate(tally, color=C.GREEN, scale_factor=1.06))
        self.fade_all()

        # The page's box: the table of the plans, then the plan crossing by crossing.
        view = BoxView(QID, "plans", width=11.5).move_to(UP * 0.6)
        self.say("התיבה שבעמוד משווה את התוכניות :\nהחיפוש, המהיר מלווה, ושני האיטיים יחד.",
                 FadeIn(view))
        self.say("החיפוש מוצא 17, כמו שני האיטיים יחד.\nהמהיר מלווה נותן 19.")
        self.play(FadeOut(view), run_time=0.6)
        view = BoxView(QID, "best", height=5.6).move_to(UP * 0.62)
        self.say("והיא מריצה את התוכנית של החיפוש,\nחצייה אחרי חצייה.", FadeIn(view))
        self.box_beat(view, [
            (1, "‏A ו-B חוצים, והלפיד איתם."),
            (2, "‏A מחזיר את הלפיד."),
            (3, "‏C ו-D חוצים יחד : t = 13."),
            (4, "‏B מחזיר את הלפיד : t = 15."),
            (5, "‏A ו-B חוצים : t = 17,\nוכולם בצד הרחוק."),
        ])
        self.fade_all()

        # Why 17 is the least: the cases.
        arrows = VGroup(*[M(a, 52, C.AMBER if a == "→" else C.BLUE) for a in "→←→←→"]).arrange(RIGHT, buff=0.6)
        arrows.move_to(UP * 2.4)
        self.say("למה אי אפשר פחות מ-17? קודם :\nכמה חציות צריך לכל הפחות?", FadeIn(arrows, lag_ratio=0.2))
        self.say("כל חצייה קדימה מעבירה עד שניים :\nשלוש קדימה, ושתיים חזרה ביניהן. חמש.")
        line1 = TX(r"D \text{ crosses once at least: } 10", size=36).move_to(UP * 1.3)
        self.say("‏D חוצה קדימה לפחות פעם אחת :\n‏10 דקות.", FadeIn(line1))
        line2 = TX(r"\text{every other crossing} \ge \text{its fastest}", size=36).move_to(UP * 0.4)
        self.say("כל אחת מארבע החציות האחרות לוקחת\nלפחות את הזמן של המהיר שבה.", FadeIn(line2))
        self.play(FadeOut(arrows), FadeOut(line1), FadeOut(line2), run_time=0.6)

        ref = DashedLine([-5.4 + 17 * 0.5, 2.2, 0], [-5.4 + 17 * 0.5, -2.2, 0], color=C.GREEN,
                         stroke_width=3)
        ref_lab = TX("17", size=30, color=C.GREEN).next_to(ref, UP, buff=0.1)
        c1 = self.time_bar([(10, C.AMBER), (5, C.ORANGE), (1, C.BLUE), (1, C.BLUE), (1, C.BLUE)], 1.0)
        t1 = T("case 1: C not with D", 30, C.MUTED).next_to(c1, UP, buff=0.25).align_to(c1, LEFT)
        s1 = TX(r"\ge 18", size=40, color=C.WHITE).next_to(c1, RIGHT, buff=0.35)
        self.say("מקרה 1 : C לא חוצה עם D.\nאז יש עוד חצייה של C, של 5 לפחות.",
                 FadeIn(t1), FadeIn(c1[:2], lag_ratio=0.3), FadeIn(ref), FadeIn(ref_lab), run_time=1.4)
        self.say("ועוד שלוש חציות של דקה לפחות :\n‏10 + 5 + 3 = 18. יותר מ-17.",
                 FadeIn(c1[2:], lag_ratio=0.3), FadeIn(s1), run_time=1.2)
        c2 = self.time_bar([(2, C.BLUE), (1, C.BLUE), (10, C.AMBER), (2, C.BLUE), (2, C.BLUE)], -1.2)
        t2 = T("case 2: C with D", 30, C.MUTED).next_to(c2, UP, buff=0.25).align_to(c2, LEFT)
        s2 = TX(r"\ge 17", size=40, color=C.GREEN).next_to(c2, RIGHT, buff=0.35)
        self.say("מקרה 2 : C חוצה עם D, 10 דקות.\nלפני כן מישהו עבר וחיכה בצד הרחוק :",
                 FadeIn(t2), FadeIn(c2[2]), run_time=1.0)
        self.say("חצייה קדימה של 2 לפחות, כי A לבד\nלא יכול גם לחכות שם וגם לחזור.",
                 FadeIn(c2[0]))
        self.say("הלפיד חוזר פעמיים : 1 ועוד 2 לפחות,\nכי אותו אדם לא יכול להיות בשני הצדדים.",
                 FadeIn(c2[1]), FadeIn(c2[3]))
        self.say("ועוד החצייה האחרונה, 2 לפחות :\n‏2 + 1 + 10 + 2 + 2 = 17.",
                 FadeIn(c2[4]), FadeIn(s2))
        self.say("בשני המקרים לפחות 17, והתוכנית שלנו\nמשיגה בדיוק 17. זה המינימום.",
                 Indicate(s2, color=C.GREEN))
        self.fade_all()

        chips = cost_chips(("crossings", "5"), ("plans", "dozens"),
                           notes=("3 forward, 2 back", "few enough to search"))
        self.say("הסיבוכיות : כל תוכנית לארבעה היא\nחמש חציות, ויש רק כמה עשרות תוכניות.",
                 FadeIn(chips, lag_ratio=0.3))
        self.say("בסעיף ב קוד יעבור על כולן,\nלכל מספר של אנשים.")
        self.fade_all()


class ChapterB(BridgeScene):
    def construct(self):
        self.chapter_card("סעיף ב", "קוד : כל מספר אנשים",
                          "סעיף ב : פונקציה שמקבלת זמנים ומחזירה\nאת הזמן הקצר ביותר ואת החציות.")

        # The state.
        bits = VGroup(*[VGroup(Square(0.9, stroke_color=C.MUTED, stroke_width=3, fill_color=C.NAVY_LIGHT,
                                      fill_opacity=1), M(b, 44)) for b in "0011"]).arrange(RIGHT, buff=0.12)
        for sq in bits:
            sq[1].move_to(sq[0])
        tags = VGroup(*[T(n, 28, C.MUTED).next_to(bits[k], UP, buff=0.15) for k, n in enumerate("DCBA")])
        across = VGroup(M("across =", 36, C.MUTED).next_to(bits, LEFT, buff=0.4), bits, tags)
        side = VGroup(M("side =", 36, C.MUTED), M("1", 44, C.AMBER), T("(far)", 30, C.MUTED)).arrange(RIGHT, buff=0.3)
        state = VGroup(across, side).arrange(DOWN, buff=0.6).move_to(UP * 1.2)
        self.say("המצב באמצע : מי כבר בצד הרחוק,\nביט לכל אדם, ואיפה הלפיד.",
                 FadeIn(across), FadeIn(side), run_time=1.2)
        self.say("כאן A ו-B בצד הרחוק, והלפיד שם.\nמה שקרה קודם לא משנה את ההמשך.",
                 *[Indicate(bits[k], color=C.AMBER) for k in (2, 3)])
        count = TX(r"2^N \cdot 2 \text{ states}: \quad 2^4 \cdot 2 = 32", size=40,
                   color=C.AMBER).move_to(DOWN * 1.3)
        self.say("עם N אנשים יש 2^N · 2 מצבים.\nלארבעה, 32.", FadeIn(count))
        self.say("הזמן שעבר לא חלק מהמצב :\nהוא המחיר של המסלול אליו.")
        self.fade_all()

        # Why not BFS.
        a = self.time_bar([(10, C.AMBER), (1, C.BLUE), (5, C.ORANGE), (1, C.BLUE), (2, C.BLUE)], 1.0)
        b = self.time_bar([(2, C.BLUE), (1, C.BLUE), (10, C.AMBER), (2, C.BLUE), (2, C.BLUE)], -1.0)
        la = TX(r"5 \text{ edges},\ 19", size=36, color=C.RED).next_to(a, RIGHT, buff=0.3)
        lb = TX(r"5 \text{ edges},\ 17", size=36, color=C.GREEN).next_to(b, RIGHT, buff=0.3)
        self.say("חצייה היא קשת בין שני מצבים,\nוהמחיר שלה הוא הזמן של האיטי.",
                 FadeIn(a, lag_ratio=0.2), FadeIn(b, lag_ratio=0.2), run_time=1.4)
        self.say("‏BFS סופר קשתות : לשתי התוכניות\nיש חמש, ו-BFS לא מבדיל ביניהן.",
                 FadeIn(la), FadeIn(lb))
        dij = T("positive costs  →  Dijkstra: pop the least time first", 32, C.AMBER).move_to(DOWN * 2.05)
        self.say("עם מחירים חיוביים צריך Dijkstra :\nתמיד מוציאים את המצב עם הזמן הקטן ביותר.",
                 FadeIn(dij))
        self.fade_all()

        # The code: typed.
        code = page_python(QID, "def bridge")
        keep = [n for n in range(1, len(code.splitlines()) + 1) if n != 6]     # the docstring
        panel = CodePanel(code, font_size=30, drop_comments=True, drop_trailing_comments=True,
                          only=keep, rows=13)
        self.place_code(panel)
        self.type_code(panel, [
            ([1, 2], "‏heapq היא ערימה : הקטן ביותר יוצא ראשון.\n‏combinations נותנת את כל הזוגות."),
            (5, "‏bridge מקבלת את רשימת הזמנים."),
            ([7, 8], "‏n אנשים, ו-everyone היא המסכה\nשבה כולם בצד הרחוק : 1111."),
            (9, "המצב ההתחלתי : אף אחד לא עבר,\nוהלפיד בצד הקרוב."),
            ([10, 11, 12], "‏best : הזמן הטוב ביותר לכל מצב.\n‏parent : מאיפה הגענו. ובערימה, ההתחלה."),
            ([13, 14], "כל עוד הערימה לא ריקה, מוציאים\nאת המצב עם הזמן הקטן ביותר."),
            ([15, 16], "רשומה ישנה, של מצב שכבר הושג\nמהר יותר, זורקים."),
            ([17, 18, 19], "אם כולם בצד הרחוק, סיימנו :\nהמצב יצא עם הזמן הקטן ביותר."),
            (20, "‏bank : מי נמצא בגדה של הלפיד.\nהביט שלו שווה לצד של הלפיד."),
            (21, "כל קבוצה של אחד או שניים\nמהגדה הזאת יכולה לחצות."),
            ([22, 23], "המחיר : t ועוד הזמן של האיטי בקבוצה.\nהביטים שלהם מתהפכים, והלפיד עובר צד."),
            ([24, 25, 26, 27], "אם זו דרך זולה יותר למצב החדש,\nמעדכנים זמן והורה, ודוחפים לערימה."),
            ([28, 29, 30, 31], "בסוף הולכים מהמצב הסופי אחורה\nלפי ההורים, ואוספים את החציות."),
            (32, "ומחזירים את הזמן, ואת החציות\nבסדר הנכון, מההתחלה."),
        ], intro="עכשיו נכתוב את זה ב-Python.")

        # The run on 1, 2, 5, 10: pop by pop, a log of the popped states beside the code.
        steps, result = trace(code, "bridge", (list(TIMES),))
        assert result == (17, [(0, 1), (0,), (2, 3), (1,), (0, 1)]), result
        lines = [s.line for s in steps]
        segs, cur = [], []                     # the prologue, then one segment per pop
        for k, n in enumerate(lines):
            if n in (13, 28) and cur:
                segs.append(cur)
                cur = []
            cur.append(k)
        segs.append(cur)
        pops = segs[1:-1]                      # the last segment is the walk back and return
        assert len(pops) == 26 and lines[pops[-1][-1]] == 19, (len(pops), lines[pops[-1][-1]])

        def popped(k):
            s = steps[pops[k][1]].state        # after line 14
            return s["t"], s["state"]

        def fmt(n, s):
            if n not in s:
                return ""
            v = s[n]
            if n == "state":
                return state_name(*v)
            if n == "group":
                return "+".join(NAMES[i] for i in v)
            return str(v)

        vp = VarPanel(["t", "group", "state", "cost"], fmt=fmt, size=28, cols=2, slot=5.2).set_state({})
        target = panel.copy()
        target.scale(19.3 / panel.em_px())
        margin, top = 0.25, 3.55
        target.move_to([-config.frame_width / 2 + margin + target.width / 2, top - target.height / 2, 0])
        vp.next_to(target, DOWN, buff=0.4).align_to(target, LEFT).shift(RIGHT * 0.3)
        right_x = target.get_right()[0] + 0.4
        room = config.frame_width / 2 - 0.15 - right_x
        log_title = T("popped:  t   state", 28, C.MUTED)
        log_title.move_to([right_x + log_title.width / 2, top - 0.25, 0])
        log = VGroup()
        log_top = log_title.get_bottom()[1] - 0.15
        row_h = 0.44
        w00 = M("00", 28).width

        def add_rows(ks):
            """The pops `ks` into the log (the last 11 rows kept, the newest amber)."""
            anims = []
            for kk in ks:
                t, s = popped(kk)
                num = baseline_text(str(t), 28, C.WHITE)
                name = baseline_text(state_name(*s), 28, C.WHITE)
                num.move_to(ORIGIN, aligned_edge=RIGHT)
                name.next_to(num, RIGHT, buff=0.05).align_to(num, UP)
                row = VGroup(num, name)
                if row.width > room:
                    row.scale(room / row.width)
                log.add(row)
            while len(log) > 11:
                old = log[0]
                log.remove(old)
                anims.append(FadeOut(old))
            for idx, row in enumerate(log):
                at = np.array([right_x + w00, log_top - row_h * (idx + 0.5), 0])
                delta = at - np.array([row[0].get_right()[0], row.get_center()[1], 0])
                color = C.AMBER if idx >= len(log) - len(ks) else C.WHITE
                if row in self.mobjects:
                    anims.append(row.animate.shift(delta).set_color(color))
                else:
                    row.shift(delta).set_color(color)
                    anims.append(FadeIn(row))
            self.play(*anims, run_time=0.5)

        with self.beat("נריץ על 1, 2, 5, 10. מתחת לקוד המשתנים,\nומימין כל מצב שיוצא מהערימה."):
            self.play(Transform(panel, target), run_time=1.2)
            vp.set_state({})
            self.play(FadeIn(vp), FadeIn(log_title), run_time=0.6)
        if panel.em_px() < 19.0:
            self.problems.append(f"code beside the log {panel.em_px():.1f} px high at 720p")

        def span(a, b=None):
            """The trace steps of the segments a..b (pop indices, inclusive)."""
            b = a if b is None else b
            return [i for p in pops[a:b + 1] for i in p]

        p0 = pops[0]
        plan = [
            (segs[0], "full", "‏n = 4. ההתחלה : אף אחד לא עבר,\nהלפיד קרוב, הזמן 0, והיא בערימה.", None),
            (p0[:6], "full", "מוציאים את ההתחלה, t = 0.\nבגדה של הלפיד כל הארבעה.", [0]),
            (p0[6:13], "full", "הקבוצה הראשונה, A לבד : מחיר 1.\nזה פחות מאינסוף, ולכן נדחף לערימה.", None),
            (p0[13:], "jump", "כך כל עשר הקבוצות : עשרה מצבים\nנכנסים לערימה, כל אחד עם הזמן שלו.", None),
            (pops[1], "full", "יוצא (A, far) בזמן 1. רק A ליד הלפיד,\nוהחזרה שלו לא משפרת את ההתחלה.", [1]),
            (span(2), "jump", "גם (B, far) בזמן 2\nלא מוסיף שום מצב חדש.", [2]),
            (span(3), "jump", "‏(AB, far) בזמן 2 : A חוזר, מצב חדש ב-3.\n‏B חוזר, מצב חדש ב-4.", [3]),
            (span(4, 9), "jump", "הערימה מוציאה את המצבים לפי הזמן :\n‏3, 4, 5, 5, 5, 6.", list(range(4, 10))),
            (span(10, 11), "jump", "ב-9 יוצא (BC, near) : A ו-D חוצים,\nוכולם בצד הרחוק בפעם הראשונה, ב-19.", [10, 11]),
            (span(12, 23), "jump", "ה-19 מחכה בערימה. קודם יוצאים\nכל המצבים של 10 עד 15.", list(range(12, 24))),
            (span(24), "jump", "‏(CD, near) בזמן 15 : A ו-B חוצים.\n‏15 + 2 = 17, פחות מ-19 : מעדכנים.", [24]),
            (pops[25], "full", "המצב הסופי יוצא ב-17, לפני ה-19 הישן.\nכולם בצד הרחוק : break.", [25]),
            (segs[-1], "jump", "השחזור : מהסוף אחורה לפי ההורים,\nחמש חציות, ומחזירים 17.", None),
        ]
        planned = [i for g in plan for i in g[0]]
        if planned != list(range(len(steps))):
            raise RuntimeError("the plan does not cover the trace in order")
        cursor = None
        for idx, mode, caption, rows in plan:
            with self.beat(caption):
                todo = idx if mode == "full" else idx[-1:]
                rows_at = [panel.index[steps[i].line] for i in todo]
                if not all(panel.visible(steps[i].line) for i in todo):
                    lo, hi = min(rows_at), max(rows_at)
                    first = lo if lo < panel.scroll else hi - panel.rows + 1
                    anims = panel.scroll_to(first)
                    if cursor is not None:
                        anims.append(FadeOut(cursor))
                        cursor = None
                    self.play(*anims, run_time=0.7)
                per = min(0.5, 2.4 / len(todo))
                for i in todo:
                    bar = panel.bar(steps[i].line)
                    self.play(FadeIn(bar) if cursor is None else Transform(cursor, bar),
                              *vp.show(steps[i].state), run_time=per)
                    cursor = cursor or bar
                if rows:
                    add_rows(rows)
        self.fade_all()

        # The plan in the box: the walk back gives the crossings in reverse.
        moves = TX(r"(A,B)\ \ (A)\ \ (C,D)\ \ (B)\ \ (A,B)", size=40, color=C.AMBER).move_to(UP * 3.0)
        view = BoxView(QID, "best", height=4.9).move_to(UP * 0.1)
        self.say("ההורים נותנים את החציות מהסוף להתחלה.\nהפוכות, הן התוכנית של 17 מסעיף א.",
                 FadeIn(moves), FadeIn(view))
        self.box_beat(view, [
            (1, "‏A ו-B קדימה : 2 דקות."),
            (2, "‏A חוזר עם הלפיד : עברו 3 דקות."),
            (3, "‏C ו-D קדימה : עברו 13 דקות."),
            (5, "‏B חוזר, ואז A ו-B קדימה :\nעברו 17 דקות."),
        ])
        self.fade_all()

        chips = cost_chips(("time", "$O(S N^2 \\log S)$"), ("memory", "$O(S)$"),
                           notes=("S = 2^N · 2 states, O(N²) groups each", "best, parent"))
        self.say("הסיבוכיות : S = 2^N · 2 מצבים, 512 לשמונה.\nמכל מצב O(N²) קבוצות.",
                 FadeIn(chips, lag_ratio=0.3))
        self.say("עם ערימה, זמן O(S N² log S),\nוזיכרון O(S) לזמנים ולהורים.")
        self.fade_all()

        # The trap: the time inside the state.
        good = VGroup(M("state = (across, side)", 36, C.GREEN), M("32 states", 32, C.MUTED)).arrange(DOWN, buff=0.25)
        bad = VGroup(M("state = (across, side, t)", 36, C.RED), M("a new state every time", 32, C.MUTED)).arrange(DOWN, buff=0.25)
        both = VGroup(good, bad).arrange(DOWN, buff=0.9).move_to(UP * 0.7)
        self.say("מלכודת : להכניס לתוך המצב\nגם את הזמן שעבר.", FadeIn(bad))
        self.say("אז כל מצב \"חדש\", הבדיקה של best\nלא גוזמת כלום, והחיפוש מתפוצץ.",
                 Indicate(bad[1], color=C.RED))
        self.say("הזמן הוא המחיר של המסלול, לא חלק\nמהמצב. ואז יש רק 32 מצבים.", FadeIn(good))
        self.fade_all()


class Closing(BridgeScene):
    def construct(self):
        self.closing(QID, [("א", M("A+B →  ← A  C+D →  ← B  A+B →  = 17", 30)),
                           ("ב", M("Dijkstra over (who is across, torch side)", 30))],
                     ["לסיכום : שני האיטיים חוצים יחד, 17 דקות,\nו-Dijkstra על המצבים לכל מספר.",
                      "נסו זמנים משלכם בתיבה\nשבעמוד של שאלה 0031 באתר."])
