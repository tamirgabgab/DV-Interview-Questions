"""The tutorial video of question 0029, three clock hands: how many meetings a day (script:
script.md).

Render with `python videos/render.py 0029` (see VIDEOS.md). The question has no code, so
each part is a proof step by step (the owner, 2026-10-31): one line of the argument at a
time under its caption, the earlier lines dimmed, the key numbers in amber.

Part א counts each pair of hands on its own (the fast hand laps the slow one, so a pair
meets as often as their turns a day differ: 1,416, 1,438 and 22), then removes what was
counted three times (all three hands meet only at 00:00 and 12:00): 2,876 − 2 · 2 = 2,872.
The page's clock box is played pair after pair (one pair checked, "next meeting" a few
times, so the constant gap shows), then all pairs and "next triple" to 12:00.

Part ב is the bonus: the gap θi − θj in turns grows linearly, so the meetings are every
T = ti tj / (tj − ti); the count on a closed, an open and a half-open interval (the page's
gapline box: 3T and 2.75T); and the proof that all three meet only every 43,200 s
(11a = 708b with gcd(11, 708) = 1), which gives 2,872 again.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import C, BoxView, DVQScene, M, X, read_palette  # noqa: E402

QID = 29
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – כמה פגישות ביממה"),
    ("ChapterB", "סעיף ב – הנוסחה הכללית וההוכחה"),
    ("Closing", "סיכום"),
]

# The page's boxes. "pairs": the clock box (box 0), 720 CSS px wide so the face and the
# counters sit side by side (the day bar and the time lines hidden). Picture 0 at 00:00,
# all pairs on; 1 only seconds and minutes; 2-4 "next meeting" three times; 5 only seconds
# and hours, back to 00:00; 6-8 three jumps; 9 only minutes and hours, back to 00:00;
# 10-11 two jumps; 12 every pair on again; 13 "next triple", to 12:00:00.
# "gap": the gapline box (box 1) as the page opens it (minutes and hours, L = 3T, closed),
# then open, half-open, L = 2.75T (half-open), closed and open again; its legend and the
# summary under the table hidden (the captions say what a filled and a hollow dot are).
BOXES = {
    "pairs": {"box": 0, "width": 720, "region": [".ex-controls", ".clock-box", ".ex-summary"],
              "hide": [".clock-day", ".clock-timeline", ".clock-hour-title"],
              "steps": [[],
                        [["check", ".ex-pair[value='1']", False], ["check", ".ex-pair[value='2']", False]],
                        {"do": [["click", ".ex-next"]], "repeat": 3},
                        [["check", ".ex-pair[value='1']", True], ["check", ".ex-pair[value='0']", False],
                         ["click", ".ex-reset"]],
                        {"do": [["click", ".ex-next"]], "repeat": 3},
                        [["check", ".ex-pair[value='2']", True], ["check", ".ex-pair[value='1']", False],
                         ["click", ".ex-reset"]],
                        {"do": [["click", ".ex-next"]], "repeat": 2},
                        [["check", ".ex-pair[value='0']", True], ["check", ".ex-pair[value='1']", True]],
                        [["click", ".ex-triple"]]]},
    "gap": {"box": 1, "region": [".ex-controls", ".gl-chart", ".gl-table"],
            "hide": [".gl-T", ".ex-reset", ".viz-legend", ".gl-sum"],
            "steps": [[], [["set", ".gl-mode", "open"]], [["set", ".gl-mode", "half"]],
                      [["set", ".gl-q", "11"]], [["set", ".gl-mode", "closed"]],
                      [["set", ".gl-mode", "open"]]]},
}

# The hands' colours on the page: hours ink, minutes s1, seconds s3, a meeting s2.
_S = read_palette()["slate"]
HOUR, MINUTE, SECOND, MEET = C.WHITE, _S["--viz-s1"], _S["--viz-s3"], _S["--viz-s2"]
PERIOD = {"s": 60, "m": 3600, "h": 43200}
DAY, HALF = 86400, 43200
NB = " "


# ---- the numbers of the captions, checked with exact fractions ---------------------------

def gap(i: str, j: str) -> Fr:
    """The time between two meetings of hands i (fast) and j (slow): ti tj / (tj − ti)."""
    ti, tj = PERIOD[i], PERIOD[j]
    return Fr(ti * tj, tj - ti)


def label(t: Fr) -> str:
    """H:MM:SS.ss as the page writes it (hundredths rounded, at most .99)."""
    sec = math.floor(t)
    base = f"{sec // 3600}:{sec // 60 % 60:02d}:{sec % 60:02d}"
    if t == sec:
        return base
    return f"{base}.{min(math.floor((t - sec) * 100 + Fr(1, 2)), 99):02d}"


PAIRS = [("s", "m"), ("s", "h"), ("m", "h")]
TURNS = {k: DAY // v for k, v in PERIOD.items()}
COUNT = {p: math.ceil(Fr(DAY) / gap(*p)) for p in PAIRS}          # [0, day)
assert TURNS == {"s": 1440, "m": 24, "h": 2}
assert [COUNT[p] for p in PAIRS] == [1416, 1438, 22]
assert all(COUNT[(i, j)] == TURNS[i] - TURNS[j] for i, j in PAIRS)
assert sum(COUNT.values()) == 2876 and sum(COUNT.values()) - 2 * 2 == 2872
assert gap("s", "m") == Fr(3600, 59) and gap("s", "h") == Fr(43200, 719) and gap("m", "h") == Fr(43200, 11)
assert [label(k * gap("s", "m")) for k in (1, 2, 3)] == ["0:01:01.02", "0:02:02.03", "0:03:03.05"]
assert [label(k * gap("s", "h")) for k in (1, 2, 3)] == ["0:01:00.08", "0:02:00.17", "0:03:00.25"]
assert [label(k * gap("m", "h")) for k in (1, 2)] == ["1:05:27.27", "2:10:54.55"]
assert label(gap("m", "h")) == "1:05:27.27" and round(float(gap("m", "h")), 2) == 3927.27
# On a dial of 60 ticks: minutes and hours at meeting k, and the seconds hand then.
TICKS = [(k, label(k * gap("m", "h")), Fr(60 * k, 11) % 60, (k * gap("m", "h")) % 60) for k in range(12)]
assert [k for k, _, a, b in TICKS if a == b] == [0, 11] and TICKS[11][1] == "12:00:00"
assert (round(float(TICKS[1][2]), 2), round(float(TICKS[1][3]), 2)) == (5.45, 27.27)
# Formula 3 on 12 hours (L = 43,200): L / T = 708, 719, 11.
RATIO = {p: Fr(HALF) / gap(*p) for p in PAIRS}
assert [RATIO[p] for p in PAIRS] == [708, 719, 11]
CLOSED = {p: math.floor(RATIO[p]) + 1 for p in PAIRS}
OPEN = {p: math.ceil(RATIO[p]) - 1 for p in PAIRS}
HALFOPEN = {p: math.ceil(RATIO[p]) for p in PAIRS}
assert [CLOSED[p] for p in PAIRS] == [709, 720, 12] and [OPEN[p] for p in PAIRS] == [707, 718, 10]
assert sum(OPEN.values()) == 1435 and 2 * 1435 + 2 == 2872 and 2 * 1435 == 2870
# The box: L = 3T gives 4, 2, 3; L = 2.75T gives 3, 2, 3.
for q, want in ((Fr(3), (4, 2, 3)), (Fr(11, 4), (3, 2, 3))):
    assert (math.floor(q) + 1, math.ceil(q) - 1, math.ceil(q)) == want
# The triple meeting: 3600 a / 59 = 43200 b / 11  <=>  11 a = 708 b, gcd(11, 708) = 1.
assert 708 == 2 ** 2 * 3 * 59 and math.gcd(11, 708) == 1
assert all((11 * a == 708 * b) == (Fr(3600 * a, 59) == Fr(43200 * b, 11))
           for a in range(0, 1500, 59) for b in range(0, 25))


# ---- drawing helpers ----------------------------------------------------------------------

def hand_point(centre, turn: float, length: float) -> np.ndarray:
    a = 2 * math.pi * turn
    return centre + length * np.array([math.sin(a), math.cos(a), 0.0])


class Clock(VGroup):
    """A clock face with three hands that follow the tracker `t` (seconds from 00:00)."""

    def __init__(self, radius: float = 2.0, t: float = 0.0, hands: str = "hms"):
        super().__init__()
        self.r = radius
        self.t = ValueTracker(t)
        self.face = Circle(radius=radius, stroke_color=C.WHITE, stroke_width=4,
                           fill_color=C.NAVY_DARK, fill_opacity=1)
        ticks = VGroup()
        for n in range(60):
            big = n % 5 == 0
            a = hand_point(ORIGIN, n / 60, radius * (0.86 if big else 0.92))
            b = hand_point(ORIGIN, n / 60, radius * 0.97)
            ticks.add(Line(a, b, stroke_color=C.WHITE if big else C.MUTED, stroke_width=3 if big else 1.5))
        nums = VGroup(*[M(str(n), 24 * radius / 2, C.MUTED).move_to(hand_point(ORIGIN, n / 12, radius * 0.72))
                        for n in range(1, 13)])
        self.add(self.face, ticks, nums)
        spec = {"h": (0.5, 9, HOUR), "m": (0.78, 6, MINUTE), "s": (0.9, 3, SECOND)}
        self.hands = {}
        for k in hands:
            frac, width, colour = spec[k]
            hand = Line(ORIGIN, UP * radius * frac, stroke_color=colour, stroke_width=width * radius / 2)
            hand.cap_style = CapStyleType.ROUND
            hand.add_updater(lambda m, k=k, frac=frac: m.put_start_and_end_on(
                self.face.get_center(),
                hand_point(self.face.get_center(), self.t.get_value() / PERIOD[k], self.r * frac)))
            self.hands[k] = hand
            self.add(hand)
        self.add(Dot(ORIGIN, radius=0.07 * radius / 2, color=C.WHITE))

    def paint(self, keys: str, colour: str | None = None):
        return [self.hands[k].animate.set_stroke(color=colour or MEET) for k in keys]

    def unpaint(self):
        base = {"h": HOUR, "m": MINUTE, "s": SECOND}
        return [h.animate.set_stroke(color=base[k]) for k, h in self.hands.items()]


def line(s: str, size: float = 40, color: str | None = None, amber: tuple = (), **kw) -> Text:
    """One line of a proof: math in Inter, the substrings in `amber` coloured."""
    return X(s, size, color, t2c={a: C.AMBER for a in amber}, disable_ligatures=True, **kw)


def lines(*specs, size: float = 40, buff: float = 0.32, align_eq: bool = True) -> VGroup:
    """The lines of a proof screen, top to bottom, their "=" signs one under the other."""
    group = VGroup(*[line(s, size, amber=amber) for s, amber in specs])
    group.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if align_eq:
        xs = []
        for (s, _), ln in zip(specs, group):
            glyphs = [c for c in s if not c.isspace()]
            xs.append(ln[glyphs.index("=")].get_center()[0] if "=" in glyphs else None)
        target = max(x for x in xs if x is not None)
        for x, ln in zip(xs, group):
            if x is not None:
                ln.shift(RIGHT * (target - x))
    if group.width > 13.0:
        group.scale_to_fit_width(13.0)
    return group


def grid(rows: list[list[str]], size: float = 30, head: bool = True, hbuff: float = 0.6,
         vbuff: float = 0.22, colors: dict | None = None, align: str | None = None) -> VGroup:
    """A table of Latin cells; the first row muted (a header)."""
    cells = VGroup()
    for r, row in enumerate(rows):
        for c, s in enumerate(row):
            col = C.MUTED if head and r == 0 else (colors or {}).get((r, c), C.WHITE)
            cells.add(X(s, size, col, disable_ligatures=True))
    cells.arrange_in_grid(rows=len(rows), cols=len(rows[0]), buff=(hbuff, vbuff), col_alignments=align or "r" * len(rows[0]))
    return cells


def row_of(table: VGroup, r: int, cols: int) -> VGroup:
    return VGroup(*table[r * cols:(r + 1) * cols])


CENTRE = UP * (3.75 - 2.5) / 2       # between the top and the captions


class S29(DVQScene):
    """The scenes of 0029 (the captions' colons have their no-break space in the source)."""

    def reveal(self, group: VGroup, k: int, caption: str, *anims, run_time: float = 1.0):
        """Line k of a proof screen appears under its caption; the earlier lines dim."""
        dim = [group[j].animate.set_opacity(0.4) for j in range(k) if group[j].get_fill_opacity() > 0.5]
        self.say(caption, FadeIn(group[k], shift=0.15 * UP), *dim, *anims, run_time=run_time)


# ---- the scenes ---------------------------------------------------------------------------

class Opening(S29):
    def construct(self):
        self.opening(QID, "ג'וניור", "שלושה מחוגים – כמה פגישות ביממה?",
                     ["כמה פגישות ביממה", "הנוסחה הכללית וההוכחה"],
                     ["שאלה 0029 : שלושה מחוגים של שעון.\nשאלה ברמת ג'וניור.",
                      "שני סעיפים : כמה פגישות ביממה,\nואז הנוסחה הכללית וההוכחה."])
        self.fade_all()
        clock = Clock(2.3).move_to(LEFT * 2.6 + CENTRE)
        keys = VGroup()
        for k, name, per in (("s", "seconds", "60 s"), ("m", "minutes", "3,600 s"), ("h", "hours", "43,200 s")):
            colour = {"s": SECOND, "m": MINUTE, "h": HOUR}[k]
            keys.add(VGroup(Line(ORIGIN, RIGHT * 0.6, stroke_color=colour, stroke_width=8),
                            X(name, 32, C.WHITE), X("1 turn = " + per, 30, C.MUTED)).arrange(RIGHT, buff=0.3))
        keys.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.3 + CENTRE)
        with self.beat("לשעון שלושה מחוגים, וכולם זזים ברציפות.\nגם מחוג השניות מחליק ולא קופץ."):
            self.play(FadeIn(clock), run_time=0.8)
            self.play(clock.t.animate.set_value(50), run_time=3.0, rate_func=linear)
        self.say("מחוג השניות מסיים סיבוב בדקה,\nהדקות בשעה, והשעות ב-12 שעות.",
                 LaggedStart(*[FadeIn(k, shift=0.2 * LEFT) for k in keys], lag_ratio=0.3), run_time=1.5)
        meet = float(gap("s", "m"))
        with self.beat("פגישה : רגע ששני מחוגים או יותר\nמצביעים בדיוק לאותו כיוון."):
            self.play(clock.t.animate.set_value(meet), run_time=2.0, rate_func=smooth)
            self.play(*clock.paint("sm"), run_time=0.5)
        self.say("כאן השניות והדקות נפגשים,\nב-0:01:01.02. בהמשך נראה למה דווקא שם.")
        self.fade_all()


class ChapterA(S29):
    def construct(self):
        self.chapter_card("סעיף א", "כמה פגישות ביממה",
                          "סעיף א : כמה פעמים ביממה\nנפגשים לפחות שני מחוגים?")

        rules = lines(("day:  00:00:00 ≤ t ≤ 23:59:59", ()), ("24:00:00  →  the next day", ()),
                      ("all three at once  =  1 meeting", ()), size=38, align_eq=False)
        rules.move_to(CENTRE)
        rules[1].set_color(C.MUTED)
        self.say("היממה : מ-00:00:00 ועד 23:59:59, כולל.\nחצות של סוף היממה שייכת ליממה הבאה.",
                 FadeIn(rules[0]), FadeIn(rules[1]))
        self.say("ורגע שבו שלושתם נפגשים\nנספר פעם אחת בלבד.", FadeIn(rules[2]))
        self.fade_all()

        chips = VGroup()
        for i, j in PAIRS:
            dots = VGroup(Dot(color={"s": SECOND, "m": MINUTE, "h": HOUR}[i], radius=0.12),
                          Dot(color={"s": SECOND, "m": MINUTE, "h": HOUR}[j], radius=0.12)).arrange(RIGHT, buff=0.12)
            name = X({"s": "seconds", "m": "minutes", "h": "hours"}[i] + " & "
                     + {"s": "seconds", "m": "minutes", "h": "hours"}[j], 32)
            box = VGroup(dots, name).arrange(RIGHT, buff=0.3)
            chips.add(VGroup(SurroundingRectangle(box, color=C.FAINT, buff=0.22, corner_radius=0.2), box))
        chips.arrange(DOWN, buff=0.4).move_to(CENTRE)
        self.say("הרעיון : לספור כל זוג מחוגים לחוד,\nואז לתקן את מה שנספר יותר מפעם אחת.",
                 LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in chips], lag_ratio=0.3), run_time=1.6)
        self.fade_all()

        # Step 1: turns a day.
        s1 = lines(("day = 86,400 s", ("86,400",)),
                   ("nₛ = 86,400 / 60 = 1,440", ("1,440",)),
                   ("nₘ = 86,400 / 3,600 = 24", ("24",)),
                   ("nₕ = 86,400 / 43,200 = 2", ("= 2",)), size=48).move_to(CENTRE)
        self.reveal(s1, 0, "שלב 1 : ביממה יש 86,400 שניות.\nכמה סיבובים מסיים בה כל מחוג?")
        self.reveal(s1, 1, "מחוג השניות : 86,400 חלקי 60,\nכלומר 1,440 סיבובים ביממה.")
        with self.beat("מחוג הדקות מסיים 24 סיבובים,\nומחוג השעות רק 2."):
            self.play(FadeIn(s1[2], shift=0.15 * UP), s1[0].animate.set_opacity(0.4),
                      s1[1].animate.set_opacity(0.4), run_time=0.8)
            self.play(FadeIn(s1[3], shift=0.15 * UP), run_time=0.8)
        self.fade_all()

        # Step 2: the fast hand laps the slow one (minutes and hours over 12 hours).
        T = float(gap("m", "h"))
        t = ValueTracker(0.0)
        centre = LEFT * 3.0 + CENTRE
        R = 2.2
        track = Circle(radius=R, stroke_color=C.FAINT, stroke_width=10).move_to(centre)
        top = M("12", 26, C.MUTED).next_to(track, UP, buff=0.32)
        marks = VGroup()
        for k in range(11):
            ring = Circle(radius=0.2, stroke_color=MEET, stroke_width=5).move_to(hand_point(centre, k / 11, R))
            ring.add_updater(lambda m, k=k: m.set_stroke(opacity=1.0 if t.get_value() >= k * T - 1 else 0.0))
            marks.add(ring)
        fast = Dot(radius=0.17, color=MINUTE).add_updater(
            lambda m: m.move_to(hand_point(centre, t.get_value() / 3600, R)))
        slow = Dot(radius=0.17, color=HOUR).add_updater(
            lambda m: m.move_to(hand_point(centre, t.get_value() / 43200, R)))
        anchor = M("12:00", 44).set_opacity(0)
        slot = M("12", 52).set_opacity(0)
        side = VGroup(
            VGroup(Dot(radius=0.14, color=MINUTE), X("minutes: 1 turn / hour", 30)).arrange(RIGHT, buff=0.25),
            VGroup(Dot(radius=0.14, color=HOUR), X("hours: 1 turn / 12 h", 30)).arrange(RIGHT, buff=0.25),
            VGroup(X("t =", 34, C.MUTED), anchor).arrange(RIGHT, buff=0.25),
            VGroup(X("meetings in [0, t]:", 34, C.MUTED), slot).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.4 + CENTRE)
        count = always_redraw(lambda: M(str(math.floor(t.get_value() / T + 1e-6) + 1), 52, C.AMBER)
                              .move_to(slot, aligned_edge=LEFT))
        clock_txt = always_redraw(lambda: M(
            f"{int(t.get_value() // 3600)}:{int(t.get_value() // 60 % 60):02d}", 44, C.WHITE)
            .move_to(anchor, aligned_edge=LEFT))
        self.say("שלב 2 : בכל זוג, המחוג המהיר מקיף\nאת האיטי, כמו רץ מהיר במסלול.",
                 FadeIn(track), FadeIn(top), FadeIn(fast), FadeIn(slow), FadeIn(side), FadeIn(clock_txt),
                 FadeIn(count), FadeIn(marks))
        self.say("בכל פעם שהוא מרוויח עליו סיבוב שלם,\nהם נפגשים. כאן הדקות והשעות.",
                 t.animate.set_value(3.3 * T), run_time=4.0, rate_func=linear)
        self.say("ב-12 שעות מחוג הדקות מסיים 12 סיבובים,\nומחוג השעות אחד. הוא מרוויח 11.",
                 t.animate.set_value(HALF), run_time=4.0, rate_func=linear)
        self.say("הפגישה ב-12:00 היא כבר ה-12,\nכי גם 00:00 נספרה.", Indicate(count, color=C.AMBER))
        for m in (fast, slow, count, clock_txt, *marks):
            m.clear_updaters()
        self.fade_all()

        s2 = lines(("gap:  0  →  n(fast) − n(slow)  turns", ()),
                   ("meet at gap 0, 1, 2, …, n(fast) − n(slow) − 1", ()),
                   ("N = n(fast) − n(slow)", ()),
                   ("Nₛₘ = 1,440 − 24 = 1,416", ("1,416",)),
                   ("Nₛₕ = 1,440 − 2 = 1,438", ("1,438",)),
                   ("Nₘₕ = 24 − 2 = 22", ("22",)), size=42).move_to(CENTRE)
        self.reveal(s2, 0, "ביממה הפער בין שני מחוגים גדל\nבקצב קבוע, מ-0 עד הפרש הסיבובים.")
        self.reveal(s2, 1, "הם נפגשים בכל פעם שהפער שלם.\nהפער הסופי מגיע רק בחצות של סוף היממה.")
        self.reveal(s2, 2, "ולכן לכל זוג : מספר הפגישות ביממה\nהוא ההפרש בין מספרי הסיבובים.")
        self.reveal(s2, 3, "השניות והדקות : 1,440 פחות 24,\nכלומר 1,416 פגישות.")
        with self.beat("השניות והשעות : 1,438.\nהדקות והשעות : 22."):
            self.play(FadeIn(s2[4], shift=0.15 * UP), s2[3].animate.set_opacity(0.4),
                      s2[2].animate.set_opacity(0.4), run_time=0.8)
            self.play(FadeIn(s2[5], shift=0.15 * UP), run_time=0.8)
        self.fade_all()

        # Step 3: the page's box, pair after pair: a constant time between meetings.
        view = BoxView(QID, "pairs", height=6.0).move_to(CENTRE)
        self.say("בתיבה שבעמוד : שעון שקופצים בו\nמפגישה לפגישה. מתחילים ב-00:00.", FadeIn(view))
        self.box_beat(view, [
            (1, "משאירים מסומן רק את הזוג של השניות\nוהדקות, כדי שהקפיצות יהיו רק שלו."),
            (2, "הפגישה הראשונה : 0:01:01.02, קצת אחרי\nדקה, כי מחוג הדקות התקדם בינתיים."),
            (3, "הבאה ב-0:02:02.03,\nשוב אחרי 61.02 שניות."),
            (4, "ו-0:03:03.05. המרווח קבוע, 3,600\nחלקי 59 : כ-61.02 שניות."),
            (5, "עכשיו השניות והשעות, מ-00:00.\nמחוג השעות כמעט עומד במקום."),
            (6, "פגישה ב-0:01:00.08 : אחרי דקה\nועוד קצת, כי מחוג השעות זז מעט."),
        ])
        with self.beat("ואז 0:02:00.17 ו-0:03:00.25 :\nכל 43,200 חלקי 719, כ-60.08 שניות."):
            self.box_step(view, 7)
            self.box_step(view, 8)
        self.box_beat(view, [
            (9, "והזוג האיטי, הדקות והשעות.\nשוב מ-00:00."),
            (10, "הפגישה הראשונה : 1:05:27.27, ולא 1:05.\nמחוג השעות כבר עבר את ה-1."),
            (11, "השנייה ב-2:10:54.55. המרווח קבוע :\nשעה, 5 דקות ו-27.27 שניות."),
        ])
        self.say("המרווח קבוע כי הפער גדל בקצב קבוע.\nלכן הפגישות במרווחים שווים.")

        # Steps 4-5: the sum counts pairs, not moments; all three meet at 00:00 and 12:00.
        self.box_beat(view, [
            (12, "עכשיו כל הזוגות יחד. ביממה הסכום\nהוא 1,416 ועוד 1,438 ועוד 22 : 2,876."),
        ])
        self.say("אבל זה מספר הפגישות של זוגות,\nולא מספר הרגעים.")
        self.box_beat(view, [
            (13, "הכפתור \"למשולשת הבאה\" קופץ ל-12:00 :\nשלושת המחוגים על ה-12."),
        ])
        self.say("רגע כזה נספר בשלושת הזוגות,\nבמקום פעם אחת. עודף של 2.")
        self.say("ביממה יש שני רגעים כאלה, 00:00 ו-12:00.\nמורידים 2 על כל אחד.")
        self.fade_all()

        s4 = lines(("Nₛₘ + Nₛₕ + Nₘₕ = 1,416 + 1,438 + 22 = 2,876", ("2,876",)),
                   ("N = 2,876 − 2 · 2 = 2,872", ("2,872",)), size=46).move_to(CENTRE)
        self.reveal(s4, 0, "סכום הזוגות : 2,876.")
        self.reveal(s4, 1, "התשובה : 2,876 פחות 2 כפול 2,\nכלומר 2,872 פגישות ביממה.")
        self.fade_all()

        # Why only 00:00 and 12:00: the seconds hand at every meeting of minutes and hours.
        head = ["k", "time", "m & h", "s"]
        body = [[str(k), lab, f"{float(a):.2f}", f"{float(b):.2f}"] for k, lab, a, b in TICKS]
        left = grid([head] + body[:6], size=28, hbuff=0.45)
        right = grid([head] + body[6:], size=28, hbuff=0.45)
        tables = VGroup(left, right).arrange(RIGHT, buff=1.3, aligned_edge=UP)
        if tables.width > 12.6:
            tables.scale_to_fit_width(12.6)
        note = X("dial of 60 ticks", 28, C.MUTED)
        VGroup(note, tables).arrange(DOWN, buff=0.3).move_to(CENTRE)
        hits = VGroup(SurroundingRectangle(row_of(left, 1, 4), color=C.GREEN, buff=0.1, corner_radius=0.08),
                      SurroundingRectangle(row_of(right, 6, 4), color=C.GREEN, buff=0.1, corner_radius=0.08))
        one = SurroundingRectangle(row_of(left, 2, 4), color=C.AMBER, buff=0.1, corner_radius=0.08)
        self.say("למה רק שני רגעים? כל פגישה של שלושה\nהיא גם פגישה של הדקות והשעות.")
        self.say("ב-12 שעות יש רק 11 כאלה. בודקים\nאיפה מחוג השניות בכל אחת.",
                 FadeIn(note), FadeIn(tables, lag_ratio=0.02), run_time=1.5)
        self.say("בפגישה 1 הדקות והשעות בשנתה 5.45,\nומחוג השניות בשנתה 27.27. לא יחד.", Create(one))
        self.say("כך בכל השורות, חוץ מ-0:00:00 ו-12:00:00.\nרק שם מחוג השניות באותה שנתה.",
                 FadeOut(one), Create(hits))
        self.fade_all()

        # The trap.
        trap = lines(("12 h, no ends:  N = 707 + 718 + 10 = 1,435", ()),
                     ("2 · 1,435 = 2,870", ()),
                     ("2 · 1,435 + 2 = 2,872", ("2,872",)), size=44).move_to(CENTRE)
        trap[1].set_color(C.RED)
        self.reveal(trap, 0, "המלכודת : לספור 12 שעות ולהכפיל.\nבלי הקצוות, ב-12 שעות יש 1,435 פגישות.")
        self.reveal(trap, 1, "פי 2 זה 2,870, וחסרים\nהרגעים 00:00 ו-12:00 עצמם.")
        self.reveal(trap, 2, "עם שניהם : 2,872.\nאותה תשובה.")
        self.fade_all()


class ChapterB(S29):
    def construct(self):
        self.chapter_card("סעיף ב", "הנוסחה הכללית וההוכחה",
                          "סעיף ב, בונוס : נוסחה לכל שני מחוגים,\nוהוכחה מתי שלושתם נפגשים.")

        # Steps 1-2: the gap grows linearly; it crosses an integer every T.
        s1 = lines(("two hands:  tᵢ < tⱼ   (seconds a turn)", ()),
                   ("θᵢ(t) = t / tᵢ   (turns)", ()),
                   ("ωᵢ − ωⱼ = 1/tᵢ − 1/tⱼ = (tⱼ − tᵢ) / (tᵢ tⱼ)", ("(tⱼ − tᵢ) / (tᵢ tⱼ)",)),
                   size=44, align_eq=False).move_to(CENTRE)
        self.reveal(s1, 0, "שני מחוגים, עם זמני סיבוב t_i < t_j.\nכל כמה זמן הם נפגשים?")
        self.reveal(s1, 1, "מודדים זוויות בסיבובים. מחוג עם זמן\nסיבוב t_i עושה 1/t_i סיבובים בשנייה.")
        self.reveal(s1, 2, "שלב 1 : המהיר מתרחק מהאיטי\nבקצב ההפרש של המהירויות.")
        self.fade_all()

        ax = Axes(x_range=[0, 3.6, 1], y_range=[0, 3.6, 1], x_length=8.0, y_length=4.6, tips=False,
                  axis_config={"color": C.MUTED, "stroke_width": 3, "include_ticks": True})
        ax.move_to(CENTRE + DOWN * 0.15)
        dashes = VGroup(*[DashedLine(ax.c2p(0, k), ax.c2p(3.6, k), color=C.MUTED, stroke_width=2.5,
                                     stroke_opacity=0.7)
                          for k in (1, 2, 3)])
        ylab = VGroup(*[X(str(k), 28, C.MUTED).next_to(ax.c2p(0, k), LEFT, buff=0.2) for k in range(4)])
        xlab = VGroup(*[X(s, 28, C.MUTED).next_to(ax.c2p(k, 0), DOWN, buff=0.2)
                        for k, s in ((1, "T"), (2, "2T"), (3, "3T"))])
        yname = X("θᵢ − θⱼ  (turns)", 30, C.WHITE).next_to(ax.c2p(0, 3.6), UP, buff=0.15).shift(RIGHT * 0.6)
        xname = X("t", 30, C.WHITE).next_to(ax.c2p(3.6, 0), RIGHT, buff=0.15)
        graph = ax.plot(lambda x: x, x_range=[0, 3.5], color=MINUTE, stroke_width=5)
        dots = VGroup(*[Dot(ax.c2p(k, k), radius=0.12, color=MEET) for k in range(4)])
        drops = VGroup(*[DashedLine(ax.c2p(k, k), ax.c2p(k, 0), color=MEET, stroke_width=2) for k in (1, 2, 3)])
        self.say("בגרף : הפער בסיבובים מול הזמן\nהוא קו ישר שעולה בקצב קבוע.",
                 Create(ax), FadeIn(ylab), FadeIn(yname), FadeIn(xname), Create(graph), run_time=2.0)
        self.say("הקווים המקווקווים הם המספרים השלמים.\nכל חיתוך הוא פגישה.",
                 Create(dashes), LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.3),
                 run_time=1.6)
        self.say("שלב 2 : החיתוכים במרווחים שווים, T.\nהפער עולה בסיבוב שלם בכל T.",
                 Create(drops), FadeIn(xlab), run_time=1.4)
        self.fade_all()

        s2 = lines(("T · (ωᵢ − ωⱼ) = 1", ()),
                   ("Tᵢⱼ = tᵢ tⱼ / (tⱼ − tᵢ)", ("tᵢ tⱼ / (tⱼ − tᵢ)",)),
                   ("Tₛₘ = 60 · 3,600 / 3,540 = 3,600/59 ≈ 61.02 s", ("61.02",)),
                   ("Tₛₕ = 60 · 43,200 / 43,140 = 43,200/719 ≈ 60.08 s", ("60.08",)),
                   ("Tₘₕ = 3,600 · 43,200 / 39,600 = 43,200/11 ≈ 3,927.27 s", ("3,927.27",)),
                   size=38).move_to(CENTRE)
        self.reveal(s2, 0, "ב-T אחד הפער עולה בסיבוב אחד :\nהקצב כפול T שווה 1.")
        self.reveal(s2, 1, "ולכן T הוא מכפלת זמני הסיבוב\nחלקי ההפרש ביניהם.")
        self.reveal(s2, 2, "מציבים את השעון : לשניות והדקות\nיוצא 3,600 חלקי 59, כ-61.02 שניות.")
        with self.beat("לשניות והשעות כ-60.08 שניות, ולדקות\nוהשעות כ-3,927.27. כמו בתיבה של סעיף א."):
            self.play(FadeIn(s2[3], shift=0.15 * UP), s2[2].animate.set_opacity(0.4),
                      s2[1].animate.set_opacity(0.4), s2[0].animate.set_opacity(0.4), run_time=0.8)
            self.play(FadeIn(s2[4], shift=0.15 * UP), run_time=0.8)
        self.fade_all()

        # Step 3: the count on an interval, and the page's gapline box.
        g3 = grid([["[0, L]", "closed", "⌊L/T⌋ + 1"], ["(0, L)", "open", "⌈L/T⌉ − 1"],
                   ["[0, L)", "half-open", "⌈L/T⌉"]], size=40, head=False, hbuff=0.7, vbuff=0.4,
                  align="lll", colors={(r, 2): C.AMBER for r in range(3)})
        title = X("meetings at  0, T, 2T, 3T, …", 40, C.MUTED, disable_ligatures=True)
        title.next_to(g3, UP, buff=0.55).align_to(g3, LEFT)
        s3 = VGroup(title, *[row_of(g3, r, 3) for r in range(3)]).move_to(CENTRE)
        self.reveal(s3, 0, "שלב 3 : כמה פגישות יש בקטע באורך L\nשמתחיל בפגישה? תלוי בקצוות.")
        self.say("הפגישות בזמנים 0, T, 2T וכן הלאה.\nסופרים כמה מהן נכנסות לקטע.",
                 Indicate(s3[0], color=C.AMBER, scale_factor=1.05), run_time=1.2)
        self.reveal(s3, 1, "בקטע סגור : כל k מ-0 עד L/T,\nכלומר L/T מעוגל למטה, ועוד 1.")
        with self.beat("בקטע פתוח מוותרים על 0 ועל L,\nובקטע חצי פתוח רק על L."):
            self.play(FadeIn(s3[2], shift=0.15 * UP), s3[1].animate.set_opacity(0.4), run_time=0.8)
            self.play(FadeIn(s3[3], shift=0.15 * UP), run_time=0.8)
        self.fade_all()
        view = BoxView(QID, "gap", height=6.2).move_to(CENTRE)
        self.say("בתיבה שבעמוד : הדקות והשעות, עם\nקטע באורך 3T. בקטע סגור : 4 פגישות.", FadeIn(view))
        self.box_beat(view, [
            (1, "קטע פתוח : נקודה ריקה לא נספרת.\nשני הקצוות בחוץ, ונשארות 2 פגישות."),
            (2, "חצי פתוח : 0 בפנים ו-L בחוץ,\nולכן 3 פגישות."),
            (3, "כש-L הוא 2.75T, הקצה L אינו פגישה.\nבקטע חצי פתוח : עדיין 3."),
            (4, "ואז רק הקצה 0 משנה : בקטע סגור\nיש 3, כמו בחצי פתוח."),
            (5, "ובקטע פתוח 2,\nבלי הקצה 0."),
        ])
        self.fade_all()

        heads = ["", "s & m", "s & h", "m & h"]
        rows = [heads,
                ["L / T  (12 h)"] + [str(RATIO[p]) for p in PAIRS],
                ["[0, L]"] + [str(CLOSED[p]) for p in PAIRS],
                ["(0, L)"] + [str(OPEN[p]) for p in PAIRS],
                ["[0, L)"] + [str(HALFOPEN[p]) for p in PAIRS],
                ["day  [0, 2L)"] + [f"{COUNT[p]:,}" for p in PAIRS]]
        table = grid(rows, size=34, hbuff=0.9, vbuff=0.3).move_to(CENTRE)
        ratio = SurroundingRectangle(row_of(table, 1, 4), color=C.AMBER, buff=0.12, corner_radius=0.08)
        day = SurroundingRectangle(row_of(table, 5, 4), color=C.GREEN, buff=0.12, corner_radius=0.08)
        self.say("ב-12 שעות, L/T הוא 708, 719 ו-11 :\nבדיוק הפרשי הסיבובים, כמו בסעיף א.",
                 FadeIn(table, lag_ratio=0.02), Create(ratio), run_time=1.5)
        self.say("וביממה, בקטע חצי פתוח : 1,416, 1,438\nו-22. אותם מספרים כמו בסעיף א.", Create(day))
        self.fade_all()

        # Step 4: the triple meeting, as an equation in integers.
        s4 = lines(("3,600 · a / 59 = 43,200 · b / 11", ()),
                   ("a / 59 = 12 · b / 11", ()),
                   ("11 · a = 708 · b", ("708",)),
                   ("708 = 2² · 3 · 59,   gcd(11, 708) = 1", ("gcd(11, 708) = 1",)),
                   ("b = 11c,   a = 708c", ("b = 11c",)),
                   ("t = 43,200 · 11c / 11 = 43,200 · c", ("43,200 · c",)), size=38).move_to(CENTRE)
        self.say("שלב 4 : פגישה של שלושה היא שתי\nפגישות של זוגות באותו רגע.")
        self.reveal(s4, 0, "השניות והדקות בפגישה a, והדקות\nוהשעות בפגישה b, באותו זמן.")
        self.reveal(s4, 1, "מחלקים את שני הצדדים ב-3,600.")
        self.reveal(s4, 2, "מכפילים ב-59 וב-11, ומקבלים\nמשוואה במספרים שלמים.")
        self.reveal(s4, 3, "אבל 708 הוא 4 כפול 3 כפול 59,\nואין לו מחלק משותף עם 11.")
        self.reveal(s4, 4, "לכן 11 מחלק את b : b = 11c,\nו-a = 708c.")
        self.reveal(s4, 5, "והזמן הוא 43,200 כפול c :\nרק כפולות של 12 שעות.")
        self.say("ביממה אלה c = 0 ו-c = 1,\nכלומר 00:00 ו-12:00 בלבד.")
        self.fade_all()

        # Steps 5-6: inclusion and exclusion, and 2,872 again.
        s5 = lines(("N = Nₛₘ + Nₛₕ + Nₘₕ − 2 · Nₛₘₕ", ("− 2 · Nₛₘₕ",)),
                   ("N = 1,416 + 1,438 + 22 − 2 · 2 = 2,872", ("2,872",)),
                   ("12 h, open:  N = 707 + 718 + 10 = 1,435", ("1,435",)), size=42).move_to(CENTRE)
        self.reveal(s5, 0, "שלב 5 : רגע של שני מחוגים שייך לזוג\nאחד, ורגע של שלושה לשלושת הזוגות.")
        self.say("ולכן מורידים פעמיים את מספר\nהפגישות של שלושה.",
                 Circumscribe(s5[0][-7:], color=C.AMBER), run_time=1.2)
        self.reveal(s5, 1, "ביממה : 1,416 ועוד 1,438 ועוד 22,\nפחות 2 כפול 2. שוב 2,872.")
        self.reveal(s5, 2, "ובקטע הפתוח של 12 שעות אין פגישה\nשל שלושה : 1,435, כמו בבדיקה של סעיף א.")
        self.fade_all()


class Closing(S29):
    def construct(self):
        self.closing(QID, [("סעיף א", X("1,416 + 1,438 + 22 − 2 · 2 = 2,872", 36, disable_ligatures=True)),
                           ("סעיף ב", X("Tᵢⱼ = tᵢ tⱼ / (tⱼ − tᵢ)", 36, disable_ligatures=True))],
                     ["לסיכום : כל זוג לחוד, ואז מורידים את\nהרגעים של שלושה. 2,872 פגישות ביממה.",
                      "נסו את השעון ואת הגרף בתיבות\nשבעמוד של שאלה 0029 באתר."],
                     holds=(4.0, 4.0))
