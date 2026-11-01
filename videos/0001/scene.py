"""The tutorial video of question 0001, the rising edge detector (script: script.md).

Render with `python videos/render.py 0001` (see VIDEOS.md). One part: the problem on the
page's sig (0 0 1 1 1 1 0 0 1 1), why a combinational circuit cannot tell "rose now" from
"high for long", the circuit drawn in Manim (a D flip-flop, NOT and AND), then the timing
diagram built cycle by cycle under the circuit, the flip-flop showing the sig it remembers
and the wires their values; the page's WaveDrom diagram whole (`wave_shot.py` takes it from
the built site); the page's edge box drawn click by click, the reset trap and the falling
and any-edge follow-ups; the page's SystemVerilog module typed (the answer is hardware, as
in 0011) and walked beside the box; the cost and the two traps of the page.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import (C, LABEL_PYTHON, TX, BoxView, CodePanel, DVQScene, M, T,  # noqa: E402
                 cost_chips, he, page_code)

QID = 1
SCENES = [
    ("Opening", "פתיחה"),
    ("Chapter", "גלאי עליית שפה – מעגל, קוד ותזמון"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="edge"): picture 0 cleared (every cycle of sig low), then a
# click on a cell of sig per picture (cycles 2, 3, 4 and 5 as one step, 8, 9: the page's
# diagram), the reset trap (sig high in cycle 0), and the falling and any-edge modes.
BOXES = {
    "draw": {"box": 0, "region": [".wv-wrap", ".wv-step", ".wv-sum"], "hide": [".wv-export"],
             "steps": [[["click", ".ex-preset[data-p='clear']"]],
                       [["click", ".wv-cell[data-k='2']"]],
                       [["click", ".wv-cell[data-k='3']"]],
                       [["click", ".wv-cell[data-k='4']"], ["click", ".wv-cell[data-k='5']"]],
                       [["click", ".wv-cell[data-k='8']"]],
                       [["click", ".wv-cell[data-k='9']"]],
                       [["check", ".ex-hi", True]],
                       [["check", ".ex-hi", False], ["set", ".ex-mode", "fall"]],
                       [["set", ".ex-mode", "both"]]]},
}

SIG = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1]                     # the page's diagram
SIG_Q = [0] + SIG[:-1]                                  # reset in cycle 0, then the last sig
PULSE = [s & (1 - q) for s, q in zip(SIG, SIG_Q)]
assert PULSE == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0]

WAVE = Path(__file__).resolve().parent / "out" / "wavedrom.png"


def wavedrom_picture() -> ImageMobject:
    """The page's WaveDrom diagram (taken from the built site by wave_shot.py)."""
    if not WAVE.exists():
        subprocess.run([LABEL_PYTHON, str(Path(__file__).resolve().parent / "wave_shot.py")],
                       check=True)
    return ImageMobject(str(WAVE))


# --------------------------------------------------------------------------------------
# The circuit: sig to a D flip-flop and to an AND; the flip-flop's Q through a NOT to the
# AND's other input. The wires are drawn first, so the shapes sit over their ends.
# --------------------------------------------------------------------------------------


def and_gate(x0: float, y: float, h: float = 1.3) -> VGroup:
    body = VGroup(Line([x0, y + h / 2, 0], [x0 + 0.55, y + h / 2, 0]),
                  ArcBetweenPoints([x0 + 0.55, y + h / 2, 0], [x0 + 0.55, y - h / 2, 0], angle=-PI),
                  Line([x0 + 0.55, y - h / 2, 0], [x0, y - h / 2, 0]),
                  Line([x0, y - h / 2, 0], [x0, y + h / 2, 0]))
    return body.set_stroke(C.WHITE, 4)


def not_gate(x0: float, y: float) -> VGroup:
    tri = Polygon([x0, y + 0.32, 0], [x0, y - 0.32, 0], [x0 + 0.6, y, 0],
                  stroke_color=C.WHITE, stroke_width=4, fill_color=C.NAVY, fill_opacity=1)
    bubble = Circle(radius=0.1, stroke_color=C.WHITE, stroke_width=4, fill_color=C.NAVY,
                    fill_opacity=1).move_to([x0 + 0.7, y, 0])
    return VGroup(tri, bubble)


class Circuit(VGroup):
    """The page's circuit, about 11.6 wide and 2.6 high, centred on the origin."""

    def __init__(self):
        super().__init__()
        top, low, clk_y = 0.75, -0.25, -0.85
        w = dict(stroke_color=C.MUTED, stroke_width=4)
        self.sig_label = M("sig", 46, C.BLUE).move_to([-5.4, top, 0])
        self.clk_label = M("clk", 46, C.MUTED).move_to([-4.4, clk_y, 0])
        self.pulse_label = M("pulse", 46, C.ORANGE).move_to([5.35, 0.45, 0])
        self.w_sig = VGroup(Line([-4.85, top, 0], [2.3, top, 0], **w),
                            Line([-3.7, top, 0], [-3.7, low, 0], **w),
                            Line([-3.7, low, 0], [-2.6, low, 0], **w))
        self.junction = Dot([-3.7, top, 0], radius=0.08, color=C.MUTED)
        self.w_clk = Line([-3.85, clk_y, 0], [-2.6, clk_y, 0], **w)
        self.ff = Rectangle(width=1.7, height=1.9, stroke_color=C.WHITE, stroke_width=4,
                            fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to([-1.75, -0.45, 0])
        self.ff_name = M("D-FF", 34, C.MUTED).next_to(self.ff, DOWN, buff=0.12)
        self.pin_d = M("D", 34, C.MUTED).move_to([-2.4, low, 0])
        self.pin_q = M("Q", 34, C.MUTED).move_to([-1.1, low, 0])
        notch = self.ff.get_left()[0]
        self.clk_mark = Polygon([notch, clk_y + 0.18, 0], [notch, clk_y - 0.18, 0],
                                [notch + 0.26, clk_y, 0], stroke_color=C.MUTED, stroke_width=3)
        self.w_q = Line([-0.9, low, 0], [0.0, low, 0], **w)
        self.q_label = M("sig_q", 40, C.GREEN).move_to([-0.05, low - 0.55, 0])
        self.inv = not_gate(0.0, low)
        self.w_inv = VGroup(Line([0.8, low, 0], [1.5, low, 0], **w),
                            Line([1.5, low, 0], [1.5, 0.15, 0], **w),
                            Line([1.5, 0.15, 0], [2.3, 0.15, 0], **w))
        self.gate = and_gate(2.3, 0.45)
        self.w_out = Line([3.5, 0.45, 0], [4.45, 0.45, 0], **w)
        self.ff_value = M("", 56, C.AMBER, weight="BOLD").move_to(self.ff)
        self.add(self.w_sig, self.w_clk, self.w_q, self.w_inv, self.w_out, self.junction,
                 self.ff, self.ff_name, self.pin_d, self.pin_q, self.clk_mark, self.inv,
                 self.gate, self.sig_label, self.clk_label, self.pulse_label, self.q_label)
        # anchors for the values on the wires (they move with the circuit)
        self.at_sig = Dot([-4.3, top - 0.38, 0], radius=0.001, fill_opacity=0)
        self.at_q = Dot([-0.45, low + 0.35, 0], radius=0.001, fill_opacity=0)
        self.at_out = Dot([4.0, 0.07, 0], radius=0.001, fill_opacity=0)
        self.at_ff = Dot(self.ff.get_center() + DOWN * 0.45, radius=0.001, fill_opacity=0)
        self.add(self.at_sig, self.at_q, self.at_out, self.at_ff)

    def parts_memory(self):
        return VGroup(self.sig_label, self.clk_label, self.w_sig, self.junction, self.w_clk,
                      self.ff, self.ff_name, self.pin_d, self.pin_q, self.clk_mark)

    def parts_q(self):
        return VGroup(self.w_q, self.q_label)

    def parts_logic(self):
        return VGroup(self.inv, self.w_inv, self.gate, self.w_out, self.pulse_label)


# --------------------------------------------------------------------------------------
# The timing diagram, drawn cycle by cycle
# --------------------------------------------------------------------------------------

ROW_NAMES = ["clk", "sig", "sig_q", "pulse"]


class Timing(VGroup):
    """clk, sig, sig_q and pulse over the cycles: each cycle's piece drawn on demand."""

    def __init__(self, n: int = 10, x0: float = -4.4, width: float = 0.98, y0: float = 1.25,
                 pitch: float = 1.0, amp: float = 0.5, numbers: bool = True):
        super().__init__()
        self.n, self.x0, self.w, self.amp = n, x0, width, amp
        colors = [C.WHITE, C.BLUE, C.GREEN, C.ORANGE]
        self.ys = {name: y0 - i * pitch for i, name in enumerate(ROW_NAMES)}
        self.colors = dict(zip(ROW_NAMES, colors))
        self.labels = VGroup(*[M(name, 30, self.colors[name]).move_to([x0 - 0.35, self.ys[name], 0],
                                                                      aligned_edge=RIGHT)
                               for name in ROW_NAMES])
        for lab, name in zip(self.labels, ROW_NAMES):
            lab.align_to([x0 - 0.35, 0, 0], RIGHT)
        self.add(self.labels)
        self.grid = VGroup(*[DashedLine([self.x(k), y0 + amp / 2 + 0.15, 0],
                                        [self.x(k), self.ys["pulse"] - amp / 2 - 0.1, 0],
                                        dash_length=0.06, stroke_color=C.FAINT, stroke_width=1.5)
                             for k in range(n + 1)])
        self.numbers = VGroup(*[M(str(k), 24, C.MUTED).move_to([self.x(k) + width / 2, y0 + amp / 2 + 0.4, 0])
                                for k in range(n)]) if numbers else VGroup()

    def x(self, k: int) -> float:
        return self.x0 + k * self.w

    def level(self, name: str, v: int) -> float:
        return self.ys[name] + (self.amp / 2 if v else -self.amp / 2)

    def clock(self, k: int) -> VMobject:
        lo, hi = self.level("clk", 0), self.level("clk", 1)
        x, m, e = self.x(k), self.x(k) + self.w / 2, self.x(k + 1)
        pts = [[x, lo, 0], [x, hi, 0], [m, hi, 0], [m, lo, 0], [e, lo, 0]]
        return VMobject(stroke_color=C.WHITE, stroke_width=4).set_points_as_corners([np.array(p) for p in pts])

    def bit(self, name: str, values: list, k: int, dashed: bool = False) -> VGroup:
        """Cycle k of a bit row: the step from the previous cycle's level, then the level;
        a soft fill under a high cycle."""
        v = values[k]
        prev = values[k - 1] if k > 0 else v
        x, e = self.x(k), self.x(k + 1)
        pts = [[x, self.level(name, prev), 0], [x, self.level(name, v), 0], [e, self.level(name, v), 0]]
        line = VMobject(stroke_color=self.colors[name], stroke_width=5)
        line.set_points_as_corners([np.array(p) for p in pts])
        if dashed:
            line = DashedVMobject(line, num_dashes=10)
        group = VGroup()
        if v:
            group.add(Rectangle(width=self.w, height=self.amp, stroke_width=0,
                                fill_color=self.colors[name], fill_opacity=0.16)
                      .move_to([x + self.w / 2, self.ys[name], 0]))
        group.add(line)
        return group

    def cell(self, name: str, k: int, color: str = C.AMBER) -> Rectangle:
        return Rectangle(width=self.w, height=self.amp + 0.3, stroke_color=color, stroke_width=4) \
            .move_to([self.x(k) + self.w / 2, self.ys[name], 0])


class EdgeScene(DVQScene):
    """Helpers shared by the scenes of 0001."""

    def show_value(self, old: Mobject | None, value, anchor: Mobject, size: float = 34,
                   color: str = C.AMBER):
        new = M(str(value), size, color, weight="BOLD").move_to(anchor.get_center())
        if old is None:
            return new, FadeIn(new, scale=1.3)
        return old, Transform(old, new)


class Opening(EdgeScene):
    def construct(self):
        self.opening(QID, "סטודנט", "גלאי עליית שפה",
                     ["מעגל · קוד · תזמון"],
                     ["שאלה 0001 : גלאי עליית שפה,\nשאלה ברמת סטודנט.",
                      "סעיף אחד : לשרטט את המעגל, לכתוב אותו\nב-SystemVerilog, ולצייר דיאגרמת תזמון."])
        self.fade_all()
        black = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.15, stroke_color=C.WHITE,
                                 stroke_width=4, fill_color=C.NAVY_LIGHT, fill_opacity=1)
        q = M("?", 80, C.AMBER, weight="BOLD").move_to(black)
        ins = VGroup(Line(LEFT * 3.6 + UP * 0.45, black.get_left() + UP * 0.45),
                     Line(LEFT * 3.6 + DOWN * 0.45, black.get_left() + DOWN * 0.45),
                     Line(black.get_right(), RIGHT * 3.6)).set_stroke(C.MUTED, 4)
        labels = VGroup(M("sig", 40, C.BLUE).next_to(LEFT * 3.6 + UP * 0.45, LEFT, buff=0.25),
                        M("clk", 40, C.MUTED).next_to(LEFT * 3.6 + DOWN * 0.45, LEFT, buff=0.25),
                        M("pulse", 40, C.ORANGE).next_to(RIGHT * 3.6, RIGHT, buff=0.25))
        block = VGroup(ins, black, q, labels).move_to(UP * 0.6)
        self.say("נתון אות sig שמסונכרן לשעון clk.\nמה צריך להיות בתוך הקופסה?",
                 Create(ins), FadeIn(black), FadeIn(q), FadeIn(labels), run_time=1.4, hold=3.0)
        self.fade_all()


class Chapter(EdgeScene):
    def construct(self):
        self.chapter_card("השאלה", "גלאי עליית שפה",
                          "המטרה : פולס ברוחב מחזור שעון אחד\nבכל פעם ש-sig עולה מ-0 ל-1.")
        self.problem()
        self.idea()
        circuit = self.circuit()
        self.timing(circuit)
        self.box()
        self.code()
        self.cost_and_traps()

    # -- the problem and the idea --------------------------------------------------------

    def problem(self):
        tm = Timing(y0=1.6, pitch=1.15)
        clk = VGroup(*[tm.clock(k) for k in range(tm.n)])
        sig = VGroup(*[tm.bit("sig", SIG, k) for k in range(tm.n)])
        want = VGroup(*[tm.bit("pulse", PULSE, k, dashed=True) for k in range(tm.n)])
        labels = VGroup(tm.labels[0], tm.labels[1], tm.labels[3])
        self.say("הנה sig מהדיאגרמה שבעמוד,\nעשרה מחזורים של השעון.",
                 FadeIn(labels), FadeIn(tm.numbers), Create(clk, lag_ratio=0.1),
                 Create(sig, lag_ratio=0.1), run_time=2.2)
        self.say("‏sig עולה פעמיים, ולכן רוצים שני פולסים,\nכל אחד ברוחב מחזור אחד בדיוק.",
                 Create(want, lag_ratio=0.1), run_time=1.6)
        span = Rectangle(width=4 * tm.w, height=tm.amp + 0.35, stroke_color=C.AMBER, stroke_width=4) \
            .move_to([tm.x(2) + 2 * tm.w, tm.ys["sig"], 0])
        self.say("גם כש-sig נשאר גבוה ארבעה מחזורים,\nהפולס לא מתארך.", Create(span))
        self.play(FadeOut(span), run_time=0.4)
        self.tm_problem = (tm, labels, clk, sig, want)

    def idea(self):
        tm, labels, clk, sig, want = self.tm_problem
        c2, c4 = tm.cell("sig", 2), tm.cell("sig", 4)
        self.say("מעגל צירופי רואה רק את sig של עכשיו.\nבמחזור 2 ובמחזור 4 הוא רואה 1.",
                 Create(c2), Create(c4))
        p1, p3 = tm.cell("sig", 1, C.GREEN), tm.cell("sig", 3, C.GREEN)
        b1 = M("0", 34, C.GREEN, weight="BOLD").next_to(p1, DOWN, buff=0.12)
        b3 = M("1", 34, C.GREEN, weight="BOLD").next_to(p3, DOWN, buff=0.12)
        self.say("ההבדל הוא במחזור הקודם : לפני מחזור 2\n‏sig היה 0, ולפני מחזור 4 הוא היה 1.",
                 Create(p1), Create(p3), FadeIn(b1), FadeIn(b3))
        self.say("שינוי הוא השוואה בין שני מחזורים,\nולכן המעגל צריך לזכור את sig הקודם.")
        self.fade_all()

    # -- the circuit -------------------------------------------------------------------------

    def circuit(self) -> Circuit:
        cc = Circuit().move_to(UP * 0.55)
        self.say("את הערך הקודם זוכר Flip-Flop מסוג D :\nבכל עליית שעון הוא דוגם את sig.",
                 Create(VGroup(cc.w_sig, cc.w_clk)), FadeIn(cc.junction), FadeIn(cc.sig_label),
                 FadeIn(cc.clk_label), FadeIn(VGroup(cc.ff, cc.ff_name, cc.pin_d, cc.pin_q, cc.clk_mark)),
                 run_time=1.6)
        self.say("המוצא שלו, sig_q, הוא הערך של sig\nבמחזור הקודם.",
                 Create(cc.w_q), FadeIn(cc.q_label))
        self.say("עליית שפה : עכשיו 1, וקודם 0.\nכלומר sig, וגם ההיפוך של sig_q.",
                 FadeIn(cc.inv), Create(cc.w_inv), Create(cc.gate), Create(cc.w_out),
                 FadeIn(cc.pulse_label), run_time=1.6)
        formula = TX(r"\texttt{pulse} = \texttt{sig} \land \lnot\,\texttt{sig\_q}", size=44,
                     color=C.AMBER).move_to(DOWN * 1.75)
        self.say("המוצא : pulse = sig & ~sig_q.\nזה כל המעגל : זיכרון אחד ושני שערים.",
                 Write(formula), run_time=1.4)
        self.play(FadeOut(formula), cc.animate.scale(0.7).move_to(UP * 2.82), run_time=1.0)
        return cc

    # -- the timing, cycle by cycle -----------------------------------------------------------

    def timing(self, cc: Circuit):
        tm = Timing(y0=0.95, pitch=0.95, amp=0.46)
        self.say("עכשיו נבנה את דיאגרמת התזמון,\nמחזור אחרי מחזור, עם אותו sig.",
                 FadeIn(tm.labels), FadeIn(tm.grid), FadeIn(tm.numbers), run_time=1.0)
        vals = {"sig": None, "ff": None, "out": None}
        edge = [None]

        def cycle(k: int):
            mark = DashedLine([tm.x(k), tm.ys["clk"] + 0.45, 0], [tm.x(k), tm.ys["pulse"] - 0.4, 0],
                              dash_length=0.1, stroke_color=C.AMBER, stroke_width=4)
            anims = [Create(mark)] if edge[0] is None else [Transform(edge[0], mark)]
            vals["ff"], a1 = self.show_value(vals["ff"], SIG_Q[k], cc.at_ff, 40)
            self.play(*anims, a1, Create(tm.clock(k)), run_time=0.6)
            if edge[0] is None:
                edge[0] = mark
            vals["sig"], a2 = self.show_value(vals["sig"], SIG[k], cc.at_sig, 36, C.BLUE)
            vals["out"], a3 = self.show_value(vals["out"], PULSE[k], cc.at_out, 36, C.ORANGE)
            self.play(a2, a3, Create(tm.bit("sig", SIG, k)), Create(tm.bit("sig_q", SIG_Q, k)),
                      Create(tm.bit("pulse", PULSE, k)), run_time=0.7)

        def cycles(ks, caption):
            with self.beat(caption):
                for k in ks:
                    cycle(k)

        cycles([0, 1], "במחזורים 0 ו-1 sig נמוך. האיפוס\nמתחיל את sig_q ב-0, וגם pulse הוא 0.")
        cycles([2], "במחזור 2 sig עולה. ה-Flip-Flop עדיין\nזוכר 0, ולכן pulse = 1 & ~0 = 1.")
        cycles([3], "בעליית השעון הבאה sig_q תופס את ה-1,\nו-~sig_q = 0 מאפס את pulse.")
        cycles([4, 5], "במחזורים 4 ו-5 sig עדיין גבוה,\nאבל גם sig_q : הפולס לא מתארך.")
        cycles([6], "במחזור 6 sig יורד, וה-AND מתאפס מיד :\nירידה לא מייצרת פולס.")
        cycles([7], "במחזור 7 גם sig_q יורד ל-0,\nמחזור אחד אחרי sig.")
        cycles([8], "במחזור 8 sig עולה שוב. ‏sig_q הוא 0,\nולכן יוצא פולס שני.")
        cycles([9], "ובמחזור 9 sig_q תופס את ה-1,\nוהפולס נגמר אחרי מחזור אחד.")
        self.play(FadeOut(edge[0]), run_time=0.4)
        self.say("‏sig_q הוא העתק של sig, מאוחר במחזור אחד.\nהפולס : המחזורים שבהם sig = 1 ו-sig_q = 0.")
        self.fade_all()

        pic = wavedrom_picture()
        pic.scale_to_fit_width(11.6)
        card = RoundedRectangle(width=pic.width + 0.4, height=pic.height + 0.4, corner_radius=0.15,
                                stroke_width=0, fill_color="#ffffff", fill_opacity=1)
        page = Group(card, pic).move_to(UP * 0.55)
        pic.move_to(card)
        self.say("וזו הדיאגרמה שבעמוד, ב-WaveDrom :\nאותם ארבעה אותות, אותם מחזורים.",
                 FadeIn(page), run_time=1.0, hold=3.5)
        self.fade_all()

    # -- the page's box ----------------------------------------------------------------------

    def box(self):
        view = BoxView(QID, "draw", height=5.7).move_to(UP * 0.6)
        self.say("בתיבה שבעמוד מציירים את sig בלחיצות,\nוהמעגל מצייר את sig_q ואת pulse.", FadeIn(view))
        self.box_beat(view, [
            (1, "לוחצים על מחזור 2 : sig עולה,\nו-pulse גבוה במחזור 2 בלבד."),
            (2, "מחזור 3 : sig עדיין גבוה, אבל sig_q כבר 1,\nולכן אין פולס."),
            (3, "גם עם מחזורים 4 ו-5 :\nפולס אחד, ברוחב מחזור אחד."),
            (4, "עלייה שנייה במחזור 8 :\nעוד פולס, שוב מחזור אחד."),
            (5, "ומחזור 9 משלים את הדיאגרמה שבעמוד."),
            (6, "המלכודת של האיפוס : sig כבר גבוה\nכשהאיפוס משתחרר, במחזור 0."),
        ])
        self.say("‏sig_q מתחיל מ-0, ולכן יוצא פולס\nבמחזור 0, בלי עליית שפה.")
        self.say("אם זה לא רצוי, מאפסים את sig_q ל-1,\nאו מסננים את המחזור הראשון.")
        self.box_beat(view, [
            (7, "שאלת המשך : ירידת שפה היא ~sig & sig_q,\nעכשיו 0 וקודם 1."),
            (8, "וכל שינוי, עלייה או ירידה,\nהוא sig ^ sig_q."),
        ])
        self.fade_all()

    # -- the code ----------------------------------------------------------------------------

    def code(self):
        sv = page_code(QID, "systemverilog", "module rise_detect")
        panel = CodePanel(sv, font_size=34, drop_comments=True, drop_trailing_comments=True,
                          language="systemverilog")
        self.place_code(panel)
        self.type_code(panel, [
            ([1, 2, 3, 4, 5, 6], "המודול rise_detect : שעון, איפוס בפעיל נמוך,\nהכניסה sig והמוצא pulse."),
            (7, "‏sig_q : כל הזיכרון של המעגל,\nביט אחד, ה-sig של המחזור הקודם."),
            ([9, 10, 11], ["‏always_ff : לוגיקה רשומה, שמתעדכנת\nבעליית clk או בירידה של rst_n.",
                           "באיפוס sig_q מתאפס ל-0,\nובכל מחזור אחר הוא דוגם את sig."]),
            (13, "‏assign : המוצא צירופי,\nבדיוק pulse = sig & ~sig_q."),
            (14, "וזה כל המודול : Flip-Flop אחד,\nשער NOT ושער AND."),
        ], intro="עכשיו נכתוב את זה ב-SystemVerilog.")

        view = BoxView(QID, "draw")
        with self.beat("נעבור על הקוד לצד התיבה,\nמהדיאגרמה הריקה."):
            self.split(panel, view)
        self.walk_code(panel, view, [
            ([13], "במחזור 2 sig = 1 ו-sig_q = 0,\nולכן ה-assign מוציא pulse = 1.", 1),
            ([9, 10, 11], "בעליית השעון הבאה : sig_q <= sig.\nעכשיו sig_q = 1.", 2),
            ([13], "ה-assign מחשב מחדש : ~sig_q = 0,\nו-pulse יורד אחרי מחזור אחד.", None),
            ([9, 10, 11], "כל עוד sig גבוה, sig_q נשאר 1\nוהפולס לא חוזר.", 3),
            ([10], "ובאיפוס sig_q <= 0 גם כש-sig כבר גבוה :\nזה הפולס של המלכודת.", 6),
        ])
        self.fade_all()

    # -- the cost and the traps -----------------------------------------------------------------

    def cost_and_traps(self):
        chips = cost_chips(("flip-flops", "1"), ("gates", "2"),
                           notes=("sig_q, one bit", "NOT and AND"))
        self.say("העלות : Flip-Flop אחד ושני שערים.\nמהכניסה sig למוצא יש שער אחד בלבד.",
                 FadeIn(chips, lag_ratio=0.3))
        self.say("לכן המעגל לא מגביל את תדר השעון,\nואין בו מונה או מכונת מצבים.")
        self.fade_all()

        bad = M("always @(posedge sig)", 44, C.WHITE).move_to(UP * 1.2)
        cross = Cross(bad, stroke_color=C.RED, stroke_width=6)
        good = M("always_ff @(posedge clk)", 44, C.GREEN).move_to(DOWN * 0.4)
        self.say("מלכודת : לזהות שפה עם always @(posedge sig).\nזה הופך את sig לשעון נוסף.",
                 FadeIn(bad), Create(cross))
        self.say("אין ממנו דרך פשוטה לפולס ברוחב מחזור\nשל clk. במקום זה דוגמים את sig עם clk.",
                 FadeIn(good))
        self.fade_all()

        def block(text, width=1.9):
            b = RoundedRectangle(width=width, height=1.2, corner_radius=0.12, stroke_color=C.WHITE,
                                 stroke_width=4, fill_color=C.NAVY_LIGHT, fill_opacity=1)
            return VGroup(b, M(text, 32).move_to(b))

        chain = VGroup(block("FF"), block("FF"), block("edge", 2.2)).arrange(RIGHT, buff=0.8)
        src = M("sig", 40, C.BLUE).next_to(chain, LEFT, buff=0.8)
        out = M("pulse", 40, C.ORANGE).next_to(chain, RIGHT, buff=0.8)
        VGroup(src, chain, out).move_to(UP * 0.7)
        wires = VGroup(Line(src.get_right() + RIGHT * 0.15, chain[0].get_left()),
                       Line(chain[0].get_right(), chain[1].get_left()),
                       Line(chain[1].get_right(), chain[2].get_left()),
                       Line(chain[2].get_right(), out.get_left() + LEFT * 0.15)).set_stroke(C.MUTED, 4)
        sync = Brace(VGroup(chain[0], chain[1]), DOWN, color=C.AMBER)
        sync_t = T("2-FF synchronizer", 30, C.AMBER).next_to(sync, DOWN, buff=0.15)
        self.say("מלכודת : sig שמגיע מדומיין שעון אחר.\nקודם מסנכרנים אותו בשני Flip-Flops,",
                 Create(wires[:2]), FadeIn(src), FadeIn(chain[:2]), FadeIn(sync), FadeIn(sync_t),
                 run_time=1.4)
        self.say("ורק אז מזהים את השפה. אחרת metastability\nעלול לייצר פולסים כפולים או חסרים.",
                 Create(wires[2:]), FadeIn(chain[2]), FadeIn(out))
        self.fade_all()


class Closing(EdgeScene):
    def construct(self):
        self.closing(QID, [("התשובה", M("pulse = sig & ~sig_q", 40))],
                     ["לסיכום : Flip-Flop אחד זוכר את sig,\nו-pulse = sig & ~sig_q.",
                      "נסו לצייר את sig בעצמכם בתיבה\nשבעמוד של שאלה 0001 באתר."],
                     holds=(4.0, 4.5))
