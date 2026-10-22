#!/usr/bin/env python3
"""Figures and tables of question 0024 (USB4 Path credits reference model).

    python tools/figures/q0024.py > /tmp/q0024.html

Prints, in page order. Part a: the modulo-256 circle (the same distance without and with
a wrap) and its legend; the stepper of the run without losses, its legend and its table.
Part b: the circle of the Credit Sync correction across the wrap and its legend; the
stepper of the run with one dropped packet, its legend and its table. The runs drive the
page's own Python classes, so the figures show what the published code does; tests/0024
checks that the page copies match.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import load_python  # noqa: E402
from stepper import stepper  # noqa: E402

ns = load_python(24)
Egress, Ingress = ns["EgressSyncModel"], ns["IngressSyncModel"]
TunneledPacket, forward_distance = ns["TunneledPacket"], ns["forward_distance"]

RLM = "‏"
HOP = 3
CREDITS = 5


def legend(items):
    return ('<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{t}</span>' for c, t in items)
            + "</span>")


# ------------------------------------------------------------------ the modulo-256 circle

R = 86


def pt(cx, cy, value, r=R):
    """The point of counter value `value` on a circle: 0 at the top, clockwise."""
    th = value / 256 * 2 * math.pi - math.pi / 2
    return cx + r * math.cos(th), cy + r * math.sin(th)


def arc(cx, cy, a, b, cls, r=R):
    """The clockwise arc from value a to value b."""
    d = (b - a) % 256
    x1, y1 = pt(cx, cy, a, r)
    x2, y2 = pt(cx, cy, b, r)
    return f'<path class="{cls}" d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {1 if d > 128 else 0} 1 {x2:.1f},{y2:.1f}"/>'


def panel(p, cx, cy, a, b, name_a, name_b, head, foot, what):
    d = (b - a) % 256
    p.append(f'<text class="legend halo" x="{cx}" y="22" text-anchor="middle">{head}</text>')
    p.append(f'<circle class="fc-ring" cx="{cx}" cy="{cy}" r="{R}"/>')
    for v in range(0, 256, 32):
        x1, y1 = pt(cx, cy, v, R - 5)
        x2, y2 = pt(cx, cy, v, R + 5)
        tx, ty = pt(cx, cy, v, R + 17)
        p.append(f'<line class="fc-tick" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        p.append(f'<text class="tick" x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle">{v}</text>')
    p.append(arc(cx, cy, a + 1, a + 127, "fc-window"))
    p.append(arc(cx, cy, a, b, "fc-ahead"))
    for v, cls, name, off in ((a, "ink-dot", name_a, -14), (b, "s3-dot", name_b, 14)):
        x, y = pt(cx, cy, v)
        lx, ly = pt(cx, cy, v + off, R + 40)
        p.append(f'<line class="fc-tick" x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly:.1f}"/>')
        p.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="5.5"><title>{name} = {v}</title></circle>')
        p.append(f'<text class="coord halo" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">{name} {v}</text>')
    p.append(f'<text class="st-text" x="{cx}" y="{cy + 1}" text-anchor="middle">{d} {what}</text>')
    p.append(f'<text class="tick" x="{cx}" y="{cy + 20}" text-anchor="middle">{foot}</text>')


def circle_svg(aria, left, right):
    p = [f'<svg class="figure" viewBox="0 0 640 294" style="max-width:40rem" role="img" aria-label="{aria}">']
    panel(p, 160, 156, *left)
    panel(p, 480, 156, *right)
    p.append("</svg>")
    return "".join(p)


def circle_a():
    return circle_svg("שני מצבים עם אותו מרחק קדימה : PCC = 9 ו-PCL = 13 בלי גלישה, PCC = 254 ו-PCL = 2 עם גלישה; "
                      "בשניהם ארבעה קרדיטים",
                      (9, 13, "PCC", "PCL", "no wrap: PCC = 9, PCL = 13", "(13 − 9) mod 256 = 4", "credits"),
                      (254, 2, "PCC", "PCL", "wrap: PCC = 254, PCL = 2", "(2 − 254) mod 256 = 4", "credits"))


def circle_a_legend():
    return legend([("ink", f"{RLM}PCC"), ("s3", f"{RLM}PCL"), ("fc-ahead", "המרחק קדימה : הקרדיטים שנותרו"),
                   ("fc-window", "חלון של 127 צעדים קדימה מ-PCC : רק שם PCL נקרא כ\"לפני\"")])


def circle_b():
    return circle_svg("תיקון ה-Credit Sync מעבר לגלישה : מ-PCR = 253 ל-PCC = 1 המרחק 4, ולכן PCA מתקדם מ-254 ל-2",
                      (253, 1, "PCR", "PCC", "Sync: PCR = 253, received PCC = 1", "(1 − 253) mod 256 = 4", "missing"),
                      (254, 2, "old PCA", "new PCA", "PCA = (254 + 4) mod 256", "then PCR = 1", "credits back"))


def circle_b_legend():
    return legend([("ink", "הערך הישן"), ("s3", "הערך שהגיע, או החדש"),
                   ("fc-ahead", "המרחק קדימה : פקטות שאבדו, והקרדיטים שחוזרים"),
                   ("fc-window", "חלון של 127 צעדים קדימה")])


# ------------------------------------------------------------------ the two runs

class Run:
    """One Path driven step by step; every step records the counters before and after."""

    def __init__(self):
        self.eg, self.ing = Egress(HOP), Ingress(HOP, CREDITS)
        self.frames, self.sent = [], 0

    def state(self):
        return {"pcc": self.eg.pcc, "pcl": self.eg.pcl, "pcr": self.ing.pcr, "pca": self.ing.pca,
                "occ": self.ing.rx_occupancy, "credits": forward_distance(self.eg.pcc, self.eg.pcl)}

    def step(self, kind, label, event, action):
        before = self.state()
        action()
        self.frames.append({"kind": kind, "label": label, "event": event, "before": before, "after": self.state()})

    def setup(self):
        self.step("setup", "Path setup", "הקמת הנתיב", lambda: None)

    def grant(self):
        g = self.ing.build_credit_grant()
        self.step("grant", f"Credit Grant ({g.credits})", f"{RLM}Credit Grant של {g.credits}",
                  lambda: self.eg.consume_credit_grant(g))

    def packet(self, accepted=True):
        self.sent += 1
        n, pkt = self.sent, TunneledPacket(HOP, self.sent)

        def act():
            self.eg.on_packet_transmitted()
            self.ing.on_packet_received(pkt, accepted)
        self.step("packet" if accepted else "drop", f"packet {n}",
                  f"פקטה {n} שודרה {'והתקבלה' if accepted else 'ואבדה'}", act)

    def burst(self, k):
        first, last = self.sent + 1, self.sent + k

        def act():
            for n in range(first, last + 1):
                self.eg.on_packet_transmitted()
                self.ing.on_packet_received(TunneledPacket(HOP, n))
            self.sent = last
        self.step("packet", f"packets {first} … {last}", f"פקטות {first} עד {last} שודרו והתקבלו", act)

    def dequeue(self):
        self.step("dequeue", "dequeue", "פקטה יצאה מה-buffer", self.ing.on_packet_dequeued)

    def sync(self):
        s = self.eg.build_credit_sync()
        self.step("sync", f"Credit Sync (PCC = {s.pcc})", f"{RLM}Credit Sync עם PCC = {s.pcc}",
                  lambda: self.ing.consume_credit_sync(s))


def run_a():
    r = Run()
    r.setup(); r.grant(); r.packet(); r.packet(); r.packet(); r.dequeue(); r.dequeue(); r.grant(); r.burst(4)
    return r.frames


def run_b():
    r = Run()
    r.setup(); r.grant(); r.packet(); r.packet(accepted=False); r.packet(); r.dequeue(); r.dequeue(); r.grant()
    r.sync(); r.grant()
    return r.frames


# ------------------------------------------------------------------ stepper frames

def defs(uid):
    m = []
    for c in ("s1", "s3", "ink"):
        m.append(f'<marker id="{uid}-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto"><path class="{c}-fill" d="M0,0 L10,5 L0,10 z"/></marker>')
    return "<defs>" + "".join(m) + "</defs>"


def adapter(p, x, title, rows, slots=None):
    p.append(f'<rect class="cs-blk" x="{x}" y="36" width="230" height="166" rx="6"/>')
    p.append(f'<text class="coord" x="{x + 115}" y="58" text-anchor="middle" font-weight="700">{title}</text>')
    for i, (name, before, after) in enumerate(rows):
        y = 88 + i * 26
        if before != after:
            p.append(f'<rect class="st-cur" x="{x + 164}" y="{y - 17}" width="56" height="24" rx="4"/>')
        p.append(f'<text class="tick" x="{x + 14}" y="{y}">{name}</text>')
        p.append(f'<text class="st-text" x="{x + 214}" y="{y}" text-anchor="end">{after}</text>')
    if slots is not None:
        occ, size = slots
        p.append(f'<text class="tick" x="{x + 14}" y="{172}">RX buffer</text>')
        for i in range(size):
            cls = "fc-full" if i < occ else "fc-slot"
            p.append(f'<rect class="{cls}" x="{x + 92 + i * 27}" y="{156}" width="22" height="22" rx="3"/>')
        p.append(f'<text class="tick" x="{x + 214}" y="{196}" text-anchor="end">{occ} of {size} slots used</text>')


def middle(p, f, uid):
    """The event between the adapters: an arrow with a label above and up to two short
    lines below (the column is 140 px wide, so every line stays under 20 characters)."""
    kind = f["kind"]
    arrows = {"packet": ("fc-pkt", 252, 384, "s1"), "grant": ("fc-grant", 388, 256, "s3"),
              "sync": ("fc-sync", 252, 384, "ink")}
    notes = {"packet": ("PCC + 1, PCR + 1",), "drop": ("PCC + 1;", "Ingress: no change"),
             "grant": ("credits = PCA", "→ PCL"), "sync": ("PCA + missing,", "then PCR = PCC"),
             "dequeue": ("one slot freed:", "PCA + 1")}
    if kind in arrows:
        cls, x1, x2, m = arrows[kind]
        p.append(f'<line class="{cls}" x1="{x1}" y1="118" x2="{x2}" y2="118" marker-end="url(#{uid}-{m})"/>')
        p.append(f'<text class="tick" x="320" y="104" text-anchor="middle">{f["label"]}</text>')
    elif kind == "drop":
        p.append('<line class="fc-drop" x1="252" y1="118" x2="308" y2="118"/>')
        p.append('<text class="cs-no" x="320" y="123" text-anchor="middle">✕</text>')
        p.append(f'<text class="tick" x="320" y="104" text-anchor="middle">{f["label"]} lost</text>')
    elif kind == "dequeue":
        p.append('<text class="coord" x="320" y="112" text-anchor="middle" font-weight="700">dequeue</text>')
    else:
        p.append('<text class="coord" x="320" y="118" text-anchor="middle" font-weight="700">Path setup</text>')
    for i, line in enumerate(notes.get(kind, ())):
        p.append(f'<text class="tick" x="320" y="{138 + i * 16}" text-anchor="middle">{line}</text>')


def frame_svg(k, f, uid):
    a, b = f["before"], f["after"]
    p = [f'<svg class="figure" viewBox="0 0 640 212" style="max-width:40rem" role="img" '
         f'aria-label="צעד {k} : {f["event"]}; המונים של שני הצדדים ותפוסת ה-buffer">', defs(uid)]
    p.append(f'<text class="coord" x="8" y="20" font-weight="700">step {k} · {f["label"]}</text>')
    adapter(p, 16, "HOST · Egress Adapter",
            [("PCC", a["pcc"], b["pcc"]), ("PCL", a["pcl"], b["pcl"]), ("credits", a["credits"], b["credits"])])
    adapter(p, 394, "DEVICE · Ingress Adapter",
            [("PCR", a["pcr"], b["pcr"]), ("PCA", a["pca"], b["pca"])], slots=(b["occ"], CREDITS))
    middle(p, f, uid)
    p.append("</svg>")
    return "".join(p)


def caption(k, f):
    a, b = f["before"], f["after"]
    kind = f["kind"]
    if kind == "setup":
        return (f"צעד {k} : הקמת הנתיב. ה-Egress מתחיל מ-PCC = 0 ו-PCL = 0; ה-Ingress מ-PCR = 0 ו-PCA = {b['pca']}, "
                f"כמספר התאים ב-buffer. המרחק מ-PCC ל-PCL הוא 0, ולכן עדיין אסור לשדר.")
    if kind == "grant":
        free = CREDITS - b["occ"]
        tail = (f" בדיוק מספר התאים הפנויים, {free}." if b["credits"] == free else
                f" אבל ב-buffer יש {free} תאים פנויים : קרדיט אחד דלף עם הפקטה שאבדה.")
        return (f"צעד {k} : ה-Ingress שולח Credit Grant עם PCA = {b['pcl']}, וה-Egress מחליף : PCL = {b['pcl']}. "
                f"המרחק מ-PCC = {b['pcc']} הוא {b['credits']} קרדיטים.{tail}")
    if kind == "packet":
        n = b["pcc"] - a["pcc"]
        if n == 1:
            return (f"צעד {k} : {f['event']}. ‏PCC = {b['pcc']}, ‏PCR = {b['pcr']}, התפוסה {b['occ']}. "
                    f"נשארו {b['credits']} קרדיטים.")
        return (f"צעד {k} : {f['event']}. ‏PCC = {b['pcc']} = PCL, ‏PCR = {b['pcr']}, התפוסה {b['occ']} "
                f"וה-buffer מלא. המרחק 0, ולכן can_transmit מחזירה 0 עד ה-Credit Grant הבא.")
    if kind == "drop":
        return (f"צעד {k} : {f['event']}. ה-Egress צרך קרדיט, ‏PCC = {b['pcc']}, אבל ה-Ingress לא ראה את הפקטה : "
                f"‏PCR נשאר {b['pcr']}, ‏PCA נשאר {b['pca']} והתפוסה {b['occ']}. הקרדיט הזה לא יחזור מעצמו.")
    if kind == "dequeue":
        return (f"צעד {k} : פקטה יוצאת מה-buffer. התפוסה {b['occ']}, ‏PCA = {b['pca']}. ‏PCR נשאר {b['pcr']} : "
                f"הוא סופר קבלות, לא תפוסה.")
    missing = (b["pcr"] - a["pcr"]) % 256
    return (f"צעד {k} : ה-Egress שולח Credit Sync עם PCC = {b['pcr']}. ה-Ingress מודד מ-PCR = {a['pcr']} עד "
            f"{b['pcr']} : המרחק {missing}, פקטה אחת אבדה. ‏PCA = {a['pca']} + {missing} = {b['pca']}, ואז PCR = {b['pcr']}.")


def run_stepper(frames, part, aria):
    out = [(frame_svg(k, f, f"fc{part}{k}"), caption(k, f)) for k, f in enumerate(frames)]
    return stepper(out, aria)


def stepper_legend():
    return legend([("fc-full", "תא תפוס ב-buffer"), ("fc-slot", "תא פנוי"), ("st-cur", "ערך שהשתנה בצעד הזה"),
                   ("fc-pkt", f"{RLM}Tunneled Packet, מה-HOST ל-DEVICE"), ("fc-grant", f"{RLM}Credit Grant, מה-DEVICE ל-HOST"),
                   ("fc-sync", f"{RLM}Path Credit Sync"), ("fc-drop", "פקטה שאבדה בדרך")])


def run_table(frames):
    rows = ["| צעד | אירוע | ‏PCC | ‏PCL | ‏PCR | ‏PCA | תפוסה | קרדיטים |", "|---|---|---|---|---|---|---|---|"]
    for k, f in enumerate(frames):
        b = f["after"]
        rows.append(f"| {k} | {f['event']} | {b['pcc']} | {b['pcl']} | {b['pcr']} | {b['pca']} | {b['occ']} | {b['credits']} |")
    return "\n".join(rows)


def figures():
    """Everything the page holds, keyed by the placeholder names used while writing it."""
    a, b = run_a(), run_b()
    return {
        "FIG:circle_a": circle_a(), "LEG:circle_a": circle_a_legend(),
        "FIG:stepper_a": run_stepper(a, "a", "הזרימה התקינה, צעד אחרי צעד : Credit Grant, שלוש פקטות, שתי הוצאות ו-Grant נוסף"),
        "LEG:stepper_a": stepper_legend(), "TAB:stepper_a": run_table(a),
        "FIG:circle_b": circle_b(), "LEG:circle_b": circle_b_legend(),
        "FIG:stepper_b": run_stepper(b, "b", "אובדן פקטה, צעד אחרי צעד : הדליפה, ה-Credit Sync והתיקון"),
        "LEG:stepper_b": stepper_legend(), "TAB:stepper_b": run_table(b),
    }


if __name__ == "__main__":
    print("\n\n".join(figures().values()))
