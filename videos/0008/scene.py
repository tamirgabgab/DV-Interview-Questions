"""The tutorial video of question 0008, Eurovision 2026: when was Israel's loss certain
(script: script.md).

Render with `python videos/render.py 0008` (see notes/VIDEOS.md). The owner's choices
(2026-11-03): part א as a live scoreboard, the eight countries at the top after the jury as
bars, the public announcements one after another (from last after the jury to first), the
countries still to come as cups up to Israel's 343, and two counters, the points left
against the room in the cups, until the moment of France (the fourth announcement after
Israel); no trap section, straight to the solution; the site's Eurovision box at the end of
part א. Part ב: the page's two Python functions typed and traced on the 2026 data, reaching
4 (France). About 5-6 minutes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "figures"))

from manim import *  # noqa: E402,F403
from dvq import (C, TX, BoxView, CodePanel, DVQScene, M, VarPanel,  # noqa: E402
                 cost_chips, page_python, trace)

import q0008  # noqa: E402

QID = 8
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – הרגע המוקדם ביותר"),
    ("ChapterB", "סעיף ב – כתבו את הקוד"),
    ("Closing", "סיכום"),
]

# The page's box: "live" the slider, the cups and the line under them, from Israel's own
# announcement to France's (four clicks on "the next announcement"); "pour" the proof
# panel after France: the points left poured into the three cups still to come, 17 spilt.
BOXES = {
    "live": {"box": 0, "region": [":scope > .ex-controls:not(.eu-what)", ".eu-chart", ".eu-step"],
             "hide": [".eu-what", ".eu-sum", ".eu-proof"],
             "steps": [[], {"do": [["click", ".ex-next"]], "repeat": 4}]},
    "pour": {"box": 0, "region": [".eu-proof"], "hide": [".eu-what", ".eu-sum"],
             "steps": [[["click", ".ex-next"], ["click", ".ex-next"], ["click", ".ex-next"],
                        ["click", ".ex-next"]],
                       [["click", ".ex-pour"], ["wait", 1800]]]},
}

# ---- the numbers (from tools/figures/q0008.py, checked) --------------------------------

PUBLIC_TOTAL = q0008.PUBLIC_TOTAL
ISRAEL_TOTAL = q0008.ISRAEL_TOTAL
ABOVE = q0008.ABOVE                         # (country, jury, public), in announcement order
LEFT0 = q0008.LEFT_AFTER_ISRAEL
assert PUBLIC_TOTAL == 2088 and 35 * 58 == 2030 and sum(range(1, 9)) + 10 + 12 == 58
assert ISRAEL_TOTAL == 343 and LEFT0 == 828
assert [r[0] for r in ABOVE] == ["Poland", "Italy", "Finland", "France", "Denmark", "Australia", "Bulgaria"]
BELOW_PUBLIC = PUBLIC_TOTAL - LEFT0 - 220
assert BELOW_PUBLIC == 1040 and q0008.ISRAEL == 17          # 17 countries announced before Israel

STEPS = q0008.steps()                       # (label, left, room, lost)
assert [(s[1], s[2]) for s in STEPS] == [(828, 1315), (811, 1105), (664, 896), (526, 694),
                                         (512, 495), (434, 317), (312, 139), (0, 0)]
FIRST = next(i for i, s in enumerate(STEPS) if s[3])
assert FIRST == 4 and STEPS[4][0] == "France"
ROOM = {c: ISRAEL_TOTAL - j for c, j, _ in ABOVE}
assert ROOM == {"Poland": 210, "Italy": 209, "Finland": 202, "France": 199, "Denmark": 178,
                "Australia": 178, "Bulgaria": 139}
assert max(ROOM.values()) == 210 < 220                      # every tie goes to Israel
GAPS = [s[2] - s[1] for s in STEPS[:5]]
assert GAPS == [487, 294, 232, 168, -17]
assert [ISRAEL_TOTAL - (j + p) for _, j, p in ABOVE[:4]] == [193, 62, 64, 185]

# The scoreboard after the jury, top to bottom (the jury table ranks Australia above Denmark).
BOARD = [("Bulgaria", 204, 312), ("Australia", 165, 122), ("Denmark", 165, 78), ("France", 144, 14),
         ("Finland", 141, 138), ("Italy", 134, 147), ("Poland", 133, 17), ("Israel", 123, 220)]
assert sorted(BOARD[:-1], key=lambda r: r[0]) == sorted(ABOVE, key=lambda r: r[0])

X0, SCALE = -4.25, 6.3 / 520                # the bars: x of 0 points, units per point
ROW0, ROW_GAP, BAR_H = 2.85, 0.6, 0.4


def X(v: float) -> float:
    return X0 + v * SCALE


def num(v: int) -> str:
    return f"{v:,}"


class Board:
    """The scoreboard: per country its name, the jury bar, the cup up to 343 or the public
    bar, and its score at the bar's end."""

    def __init__(self):
        self.rows = {}
        for i, (c, j, p) in enumerate(BOARD):
            y = ROW0 - i * ROW_GAP
            name = M(c, 24, C.AMBER if c == "Israel" else C.WHITE).move_to([X0 - 0.2, y, 0], aligned_edge=RIGHT)
            jury = Rectangle(width=j * SCALE, height=BAR_H, stroke_width=0, fill_color=C.BLUE,
                             fill_opacity=0.85).move_to([X(j / 2), y, 0])
            score = M(str(j), 22, C.WHITE).move_to([X(j) - 0.08, y, 0], aligned_edge=RIGHT)
            self.rows[c] = {"y": y, "jury": j, "pub": p, "name": name, "bar": jury, "score": score}

    def jury_group(self) -> VGroup:
        return VGroup(*[VGroup(r["name"], r["bar"], r["score"]) for r in self.rows.values()])

    def cup(self, c: str) -> VGroup:
        r = self.rows[c]
        w = (ISRAEL_TOTAL - r["jury"]) * SCALE
        box = Rectangle(width=w, height=BAR_H, stroke_color=C.AMBER, stroke_width=2,
                        fill_color=C.AMBER, fill_opacity=0.14).move_to([X(r["jury"]) + w / 2, r["y"], 0])
        label = M(str(ISRAEL_TOTAL - r["jury"]), 20, C.AMBER).move_to(box)
        r["cup"] = VGroup(box, label)
        return r["cup"]

    def public(self, c: str, color: str = C.GREEN) -> tuple[Rectangle, Text]:
        r = self.rows[c]
        total = r["jury"] + r["pub"]
        w = max(r["pub"], 0.5) * SCALE
        bar = Rectangle(width=w, height=BAR_H, stroke_width=0, fill_color=color,
                        fill_opacity=0.9).move_to([X(r["jury"]) + w / 2, r["y"], 0])
        score = M(str(total), 22, C.WHITE).move_to([X(total) + 0.12, r["y"], 0], aligned_edge=LEFT)
        return bar, score


class Counters(VGroup):
    """Points left against the room in the cups, and their comparison."""

    def __init__(self, left: int, room: int | None):
        super().__init__()
        self.lab_l = M("points left", 24, C.MUTED)
        self.val_l = M(num(left), 44, C.WHITE)
        self.lab_r = M("room under 343", 24, C.MUTED)
        self.val_r = M(num(room if room is not None else 0), 44, C.AMBER)
        col = VGroup(self.lab_l, self.val_l, self.lab_r, self.val_r).arrange(DOWN, buff=0.18)
        col[2].shift(DOWN * 0.25)
        col[3].shift(DOWN * 0.25)
        self.add(col)
        self.move_to([5.0, 1.4, 0])

    def left_to(self, v: int):
        new = M(num(v), 44, C.WHITE).move_to(self.val_l)
        return Transform(self.val_l, new)

    def room_to(self, v: int):
        new = M(num(v), 44, C.AMBER).move_to(self.val_r)
        return Transform(self.val_r, new)


def verdict(left: int, room: int) -> VGroup:
    ok = left <= room
    s = f"{num(left)} {'≤' if ok else '>'} {num(room)}"
    text = M(s, 34, C.GREEN if ok else C.RED)
    mark = M("✓" if ok else "✗", 40, C.GREEN if ok else C.RED, weight="BOLD")
    return VGroup(text, mark).arrange(RIGHT, buff=0.3).move_to([5.0, -1.25, 0])


class Opening(DVQScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "אירוויזיון 2026 – מתי היה ברור שישראל לא תנצח?",
                     ["א · הרגע המוקדם ביותר", "ב · כתבו את הקוד"],
                     ["שאלה 0008 : אירוויזיון 2026, ומתי כבר\nהיה ברור שישראל לא תנצח. רמת ג'וניור.",
                      "שני סעיפים : הרגע המוקדם ביותר,\nואז הקוד שמוצא אותו."])
        self.fade_all()
        sets = TX(r"12 + 10 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 = 58", size=40).move_to(UP * 2.3)
        self.say("כל מצביע נותן 12, 10, 8 ועד 1\nלעשר מדינות שונות : 58 נקודות.", FadeIn(sets))
        jury = TX(r"\text{jury: } 35 \times 58 = 2030", size=40).next_to(sets, DOWN, buff=0.6)
        pub = TX(r"\text{public: } 36 \times 58 = 2088", size=40).next_to(jury, DOWN, buff=0.35)
        self.say("השופטים, 35 מדינות, נותנים 2,030 נקודות.\nהקהל, 36 הצבעות, נותן 2,088.",
                 FadeIn(jury), FadeIn(pub))
        self.say("קודם מכריזים את כל השופטים. אחר כך\nכל מדינה מקבלת את הקהל שלה בבת אחת.",
                 sets.animate.set_opacity(0.4), jury.animate.set_opacity(0.4), pub.animate.set_opacity(0.4))
        order = M("last after the jury  →  ...  →  first", 34, C.AMBER).next_to(pub, DOWN, buff=0.7)
        self.say("הסדר : מהמקום האחרון אחרי השופטים\nועד הראשון. מי שקיבלה, הניקוד שלה סופי.",
                 FadeIn(order, shift=0.2 * RIGHT))
        tie = M("tie  →  more public points wins", 32, C.MUTED).next_to(order, DOWN, buff=0.45)
        self.say("שובר שוויון : בתיקו מנצחת המדינה\nשקיבלה יותר נקודות מהקהל.", FadeIn(tie))
        self.fade_all()


class ChapterA(DVQScene):
    def construct(self):
        self.chapter_card("סעיף א", "הרגע המוקדם ביותר",
                          "סעיף א : מהו הרגע המוקדם ביותר שבו\nאפשר היה לדעת שישראל לא תנצח?")

        board = Board()
        rows = board.rows
        axis = Line([X0, ROW0 + 0.4, 0], [X0, ROW0 - 7 * ROW_GAP - 0.4, 0], stroke_color=C.FAINT, stroke_width=2)
        self.say("לוח התוצאות אחרי השופטים : ישראל\nבמקום 8, ושבע מדינות מעליה.",
                 Create(axis), LaggedStart(*[FadeIn(g, shift=0.2 * RIGHT) for g in board.jury_group()],
                                           lag_ratio=0.12), run_time=2.0)
        below = M("+ 17 countries below Israel", 22, C.MUTED).move_to([X0 + 1.5, ROW0 - 8 * ROW_GAP + 0.05, 0],
                                                                       aligned_edge=LEFT)
        below.align_to(rows["Israel"]["name"], LEFT)
        cnt = Counters(PUBLIC_TOTAL, None)
        self.say("הקהל מכריז מלמטה למעלה. כל הנקודות\nשלו, 2,088, עוד לא חולקו.",
                 FadeIn(cnt.lab_l), FadeIn(cnt.val_l))
        self.say("‏17 המדינות שמתחת לישראל מקבלות\nקודם : 1,040 נקודות. נותרו 1,048.",
                 FadeIn(below), cnt.left_to(PUBLIC_TOTAL - BELOW_PUBLIC))

        isr = rows["Israel"]
        bar, score = board.public("Israel", C.GREEN)
        self.say("ישראל מקבלת 220 נקודות קהל : 123\nועוד 220 הם 343, והיא עולה לראש.",
                 GrowFromEdge(bar, LEFT), Transform(isr["score"], score), cnt.left_to(LEFT0))
        line = DashedLine([X(ISRAEL_TOTAL), ROW0 + 0.45, 0], [X(ISRAEL_TOTAL), ROW0 - 7 * ROW_GAP - 0.35, 0],
                          stroke_color=C.AMBER, stroke_width=3, dash_length=0.12)
        tag = M("Israel 343", 24, C.AMBER).next_to(line, UP, buff=0.08)
        self.say("הניקוד של ישראל סופי. שבע המדינות\nשמעליה עוד מחכות לנקודות הקהל שלהן.",
                 Create(line), FadeIn(tag))

        # The cups.
        cups = [board.cup(c) for c, _, _ in ABOVE]
        self.say("כל אחת מהן היא כוס : מניקוד השופטים\nשלה ועד 343. זה המקום הפנוי שלה.",
                 LaggedStart(*[FadeIn(cp) for cp in cups], lag_ratio=0.15), run_time=1.8)
        self.say("המים הם נקודות הקהל שנותרו, 828.\nכולם חייבים להישפך לשבע הכוסות.",
                 Indicate(cnt.val_l, color=C.AMBER))
        cnt.val_r.become(M(num(STEPS[0][2]), 44, C.AMBER).move_to(cnt.lab_r.get_center() + DOWN * 0.62))
        v = verdict(LEFT0, STEPS[0][2])
        self.say("המקום בכל הכוסות יחד : 1,315.\n‏828 נכנסים, וישראל עוד יכולה לנצח.",
                 FadeIn(cnt.lab_r), FadeIn(cnt.val_r), FadeIn(v))

        # Why the cup's brim is allowed (the tie), and the two directions.
        tie = TX(r"\max\ \mathit{room} = 343 - 133 = 210 < 220", size=30).move_to([4.6, -2.05, 0])
        self.say("כוס מלאה עד השפה היא תיקו. היא מקבלת\nמהקהל לכל היותר 210, וישראל קיבלה 220.",
                 FadeIn(tie))
        self.say("לכן בכל תיקו ישראל מנצחת,\nומותר למלא כוס עד השפה.", Indicate(rows["Poland"]["cup"], color=C.AMBER))
        self.play(FadeOut(tie), run_time=0.5)
        self.say("כל עוד המים נכנסים, יש חלוקה שבה אף\nמדינה לא עוברת את 343 : ישראל בחיים.")
        self.say("וכשיש יותר מים מנפח, לפי שובך היונים\nכוס אחת לפחות עולה על גדותיה.")

        # The announcements, one by one.
        texts = {
            "Poland": "פולין מקבלת 17 : המים יורדים ב-17,\nאבל הנפח יורד בכוס שלמה, 210.",
            "Italy": "איטליה מקבלת 147 ומגיעה ל-281.\nנותרו 664, והמקום 896 : עוד נכנס.",
            "Finland": "פינלנד מקבלת 138 ומגיעה ל-279.\nנותרו 526, והמקום 694 : עוד נכנס.",
        }
        for k, (c, j, p) in enumerate(ABOVE[:3], start=1):
            r = rows[c]
            bar, score = board.public(c)
            nv = verdict(STEPS[k][1], STEPS[k][2])
            self.say(texts[c], FadeOut(r["cup"]), GrowFromEdge(bar, LEFT), Transform(r["score"], score),
                     cnt.left_to(STEPS[k][1]), cnt.room_to(STEPS[k][2]), Transform(v, nv))

        r = rows["France"]
        bar, score = board.public("France")
        self.say("צרפת מקבלת רק 14, ומגיעה ל-158.\nהמים יורדים רק ב-14 : נותרו 512.",
                 GrowFromEdge(bar, LEFT), Transform(r["score"], score), cnt.left_to(STEPS[4][1]),
                 r["cup"][0].animate.set_opacity(0.5), r["cup"][1].animate.set_opacity(0))
        self.say("אבל הכוס שלה, 199, יוצאת כולה. לשלוש\nהכוסות שנותרו יש מקום רק ל-495.",
                 FadeOut(r["cup"]), cnt.room_to(STEPS[4][2]))
        nv = verdict(STEPS[4][1], STEPS[4][2])
        spill = M("512 − 495 = 17", 30, C.RED).next_to(nv, DOWN, buff=0.3)
        self.say("‏512 גדול מ-495 : גם בחלוקה הכי טובה\nלישראל, 17 נקודות נשפכות.",
                 Transform(v, nv), FadeIn(spill))
        ring = SurroundingRectangle(VGroup(r["name"], r["bar"]), color=C.RED, buff=0.08, stroke_width=4)
        self.say("זה הרגע : מיד אחרי צרפת, ההכרזה\nהרביעית אחרי ישראל, ההפסד ודאי.", Create(ring))

        # Why France: the gap between room and left drops by 343 - total.
        self.play(FadeOut(spill), FadeOut(ring), run_time=0.5)
        gap = VGroup(*[M(str(g), 30, C.RED if g < 0 else C.WHITE) for g in GAPS])
        names = VGroup(*[M(n, 24, C.MUTED) for n in ("Israel", "Poland", "Italy", "Finland", "France")])
        tbl = VGroup(*[VGroup(n, g) for n, g in zip(names, gap)])
        for i, (n, g) in enumerate(zip(names, gap)):
            n.move_to([4.0, 1.7 - i * 0.55, 0], aligned_edge=RIGHT)
            g.move_to([4.5, 1.7 - i * 0.55, 0], aligned_edge=LEFT)
        head = M("room − left", 28, C.AMBER).move_to([4.6, 2.45, 0])
        whole = VGroup(head, tbl)
        self.play(FadeOut(cnt), FadeOut(v), run_time=0.5)
        self.say("למה דווקא צרפת? אחרי כל הכרזה הפער\nבין המקום למים קטן ב-343 פחות הסך שלה.",
                 FadeIn(whole))
        self.say("צרפת סיימה עם 158 בלבד, ולכן בזבזה\n‏185 מקומות בבת אחת : מ-168 למינוס 17.",
                 Indicate(gap[4], color=C.RED), Indicate(gap[3]))
        self.play(FadeOut(whole), FadeIn(cnt), FadeIn(v), run_time=0.6)

        # The rest of the evening.
        anims = []
        for k, (c, j, p) in enumerate(ABOVE[4:], start=5):
            r = rows[c]
            bar, score = board.public(c, C.RED if j + p > ISRAEL_TOTAL else C.GREEN)
            anims.append(AnimationGroup(FadeOut(r["cup"]), GrowFromEdge(bar, LEFT), Transform(r["score"], score)))
        with self.beat("אחר כך דנמרק, אוסטרליה ובולגריה.\nבולגריה מגיעה ל-516 ומנצחת."):
            self.play(LaggedStart(*anims, lag_ratio=0.6), cnt.left_to(0), cnt.room_to(0), run_time=3.0)
        self.fade_all()

        # The page's box.
        view = BoxView(QID, "live", height=5.7).move_to(UP * 0.62)
        self.say("בתיבה שבעמוד : אותו לוח, הכרזה\nאחרי הכרזה, עם הכוסות שנותרו.", FadeIn(view))
        self.box_beat(view, [
            (1, "פולין : 811 נקודות נכנסות\nבמקום של 1,105."),
            (2, "איטליה : 664 מול 896."),
            (3, "פינלנד : 526 מול 694."),
            (4, "צרפת : 512 מול 495,\nוהשורה למטה הופכת לאדומה."),
        ])
        self.play(FadeOut(view), run_time=0.6)
        pour = BoxView(QID, "pour", height=5.4).move_to(UP * 0.62)
        self.say("ובשלב ההוכחה שבתיבה, מוזגים את\nהנקודות לשלוש הכוסות שנותרו.", FadeIn(pour))
        self.box_beat(pour, [(1, "כל כוס מתמלאת עד 343,\nו-17 נקודות נשפכות החוצה.")])
        self.fade_all()


class ChapterB(DVQScene):
    def construct(self):
        self.chapter_card("סעיף ב", "כתבו את הקוד",
                          "סעיף ב : פונקציה שבודקת רגע אחד,\nופונקציה שעוברת על ההכרזות.")

        # The check at one moment.
        code = page_python(QID, "def israel_cannot_win")
        only = [n for n in range(1, len(code.rstrip().split("\n")) + 1) if n not in (2, 3)]
        panel = CodePanel(code, font_size=32, drop_trailing_comments=True, only=only)
        vp = VarPanel(["jury", "room"], size=32).set_state({})
        self.place_code(panel, vp, vp_width=3.4)
        self.type_code(panel, [
            (1, "היא מקבלת את הניקוד של ישראל, את\nניקוד השופטים של מי שמחכה, ואת המים."),
            (4, "‏room יסכום את המקום הפנוי בכוסות."),
            ([5, 6, 7], "מדינה שכבר מעל ישראל רק עם השופטים :\nההפסד ודאי מיד."),
            (8, "אחרת מוסיפים את הכוס שלה : ניקוד\nישראל פחות ניקוד השופטים."),
            (9, "בסוף : יותר מים מנפח? הסימן > ולא ≥,\nכי בתיקו ישראל מנצחת."),
        ], intro="קודם הבדיקה ברגע אחד : בדיוק\nהנימוק של הכוסות.")
        juries = [j for _, j, _ in ABOVE]
        self.play(FadeIn(vp), run_time=0.6)
        steps, result = trace(code, "israel_cannot_win", (ISRAEL_TOTAL, juries, LEFT0))
        assert result is False and [s.line for s in steps] == [4] + [5, 6, 8] * 7 + [5, 9]
        self.run_code(panel, vp, steps, [
            ([4], "נריץ מיד אחרי ההכרזה של ישראל :\nשבע כוסות, ו-828 נקודות שנותרו."),
            ([5, 6, 8], "פולין : 133 שופטים, כוס של 210."),
            ([5, 6, 8] * 6, "וכך לכל השבע : המקום הפנוי\nמצטבר ל-1,315."),
            ([5, 9], "‏828 לא גדול מ-1,315 :\nהפונקציה מחזירה False."),
        ])
        later = [j for _, j, _ in ABOVE[4:]]
        assert later == [165, 165, 204]
        call = M("israel_cannot_win(343, [165, 165, 204], 512)", 28)
        res = M("True", 30, C.RED)
        VGroup(call, res).arrange(RIGHT, buff=0.35).move_to([0, -2.05, 0])
        _, r2 = trace(code, "israel_cannot_win", (ISRAEL_TOTAL, later, STEPS[4][1]))
        assert r2 is True
        self.say("ואחרי צרפת : שלוש כוסות ו-512 נקודות.\nהמקום 495, והתשובה True.", FadeIn(call), FadeIn(res))
        self.fade_all()

        # The scan.
        code = page_python(QID, "def earliest_certain_loss")
        only = [n for n in range(1, len(code.rstrip().split("\n")) + 1) if n not in (2, 3, 4, 12)]
        panel = CodePanel(code, font_size=32, drop_trailing_comments=True, only=only, rows=11)

        def fmt(n, s):
            return str(s[n]) if n in s else ""

        vp = VarPanel(["k", "jury", "public", "points_left", "room"], fmt=fmt, size=28).set_state({})
        self.place_code(panel, vp, vp_width=3.6)
        self.type_code(panel, [
            (1, "היא מקבלת את המדינות שמעל ישראל, לפי\nסדר ההכרזות, ואת הנקודות שנותרו."),
            ([5, 6, 7, 8, 9], "קודם אותו חישוב של המקום הפנוי,\nכמו בפונקציה הראשונה."),
            ([10, 11], "אם ההפסד ודאי כבר ברגע הזה,\nמחזירים 0."),
            (13, "עכשיו ההכרזות לפי הסדר,\nו-k סופר אותן מ-1."),
            ([14, 15], "המים יורדים בנקודות שהמדינה קיבלה,\nוהנפח יורד בכוס שלה כולה."),
            ([16, 17], "שני תנאים : המדינה עברה את ישראל,\nאו שיש יותר מים מנפח. מחזירים k."),
            (18, "אם זה לא קרה אף פעם,\nישראל ניצחה : None."),
        ], intro="אפשר לקרוא לה אחרי כל הכרזה, אבל\nזה O(k²). עדיף לעדכן שני סכומים.")
        steps, result = trace(code, "earliest_certain_loss", (ISRAEL_TOTAL, list(ABOVE), LEFT0))
        loop = [13, 14, 15, 16]
        self.play(FadeIn(vp), run_time=0.6)
        assert result == 4 and [s.line for s in steps] == [5] + [6, 7, 9] * 7 + [6, 10] + loop * 4 + [17]
        self.run_code(panel, vp, steps, [
            ([5] + [6, 7, 9] * 7 + [6], "נריץ על נתוני 2026 : המקום הפנוי\nבהתחלה הוא שוב 1,315."),
            ([10], "‏828 לא גדול מ-1,315 : ממשיכים."),
            (loop, "‏k = 1, פולין : נותרו 811,\nוהמקום 1,105."),
            (loop * 2, "איטליה ופינלנד : 664 מול 896,\nואז 526 מול 694."),
            (loop, "‏k = 4, צרפת : נותרו 512,\nוהמקום 495. ‏512 > 495."),
            ([17], "הפונקציה מחזירה 4 : ההפסד ודאי\nאחרי צרפת, ההכרזה הרביעית."),
        ])
        self.fade_all()
        chips = cost_chips(("time", "$O(k)$"), ("memory", "$O(1)$"),
                           notes=("one pass", "room, points_left"))
        self.say("מעבר אחד : זמן O(k), וזיכרון O(1),\nשני משתנים בלבד.", FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class Closing(DVQScene):
    def construct(self):
        self.closing(QID, [("א", TX(r"\mathit{left} > \sum_c \left(343 - \mathit{jury}_c\right)", size=34)),
                           ("ב", M("earliest_certain_loss(...) = 4   # France", 28))],
                     ["לסיכום : ההפסד ודאי ברגע שהנקודות\nשנותרו לא נכנסות בכוסות : אחרי צרפת.",
                      "נסו את תיבת מה אם בעמוד של\nשאלה 0008 באתר."],
                     holds=(3.5, 3.5))
