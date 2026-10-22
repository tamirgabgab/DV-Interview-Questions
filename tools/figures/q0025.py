#!/usr/bin/env python3
"""Figures and tables of question 0025 (PCIe Ack/Nak reference model).

    python tools/figures/q0025.py > /tmp/q0025.html

Prints, in page order: the stepper of the error-free run (part a), its legend and its
table; the stepper of the run with a corrupt TLP, a corrupt Ack, a replay timeout and an
illegal Ack (part b), its legend and its table. Both runs drive the page's own Python
classes through a scripted "random" source, so the Ack thresholds are the ones the page
names; tests/0025 checks that the page copies match.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import load_python  # noqa: E402
from stepper import stepper  # noqa: E402

ns = load_python(25)
Tlp, Dllp, DllpKind = ns["Tlp"], ns["Dllp"], ns["DllpKind"]
Transmitter, Receiver = ns["TransmitterWithReplay"], ns["ReceiverWithNak"]

RLM = "‏"
START = 4094


class Script:
    """Stand-in for random.Random: the Ack thresholds of a run, in order."""

    def __init__(self, *values):
        self.values = list(values)

    def randint(self, a, b):
        v = self.values.pop(0)
        assert a <= v <= b, (a, v, b)
        return v

    def done(self):
        assert not self.values, self.values


def legend(items):
    return ('<span class="viz-legend">' + "".join(f'<span><i class="{c}"></i>{t}</span>' for c, t in items)
            + "</span>")


# ------------------------------------------------------------------ the runs

class Run:
    """RC transmitter and EP receiver joined by a link the script controls; every step
    records both states before and after."""

    def __init__(self, thresholds):
        self.script = Script(*thresholds)
        self.rc = Transmitter(START)
        self.ep = Receiver(START, self.script)
        self.frames = []
        self.payload = 0xA0

    def state(self):
        return {"nts": self.rc.next_transmit_seq, "ackd": self.rc.ackd_seq,
                "retry": [t.seq for t in self.rc.retry_buffer],
                "bad_dllp": self.rc.bad_dllp_count, "proto": self.rc.protocol_error_count,
                "replays": self.rc.replay_count,
                "nrs": self.ep.next_rcv_seq, "pending": self.ep.accepted_since_ack,
                "threshold": self.ep.ack_threshold, "nak": self.ep.nak_scheduled,
                "delivered": [t.seq for t in self.ep.received_tlps],
                "bad_tlp": self.ep.bad_tlp_count, "dups": self.ep.duplicate_count,
                "tx_dllps": [(d.kind.name, d.seq) for d in self.ep.tx_dllps],
                "tx_tlps": [(t.seq, t.is_replay) for t in self.rc.tx_tlps]}

    def step(self, kind, label, event, action):
        before = self.state()
        action()
        after = self.state()
        self.frames.append({"kind": kind, "label": label, "event": event, "before": before, "after": after})

    def start(self):
        self.step("start", "initial state", "מצב התחלתי", lambda: None)

    def send(self, n):
        seqs = [(self.rc.next_transmit_seq + i) % 4096 for i in range(n)]

        def act():
            for _ in range(n):
                self.rc.send_tlp(Tlp(self.payload))
                self.payload += 1
        self.step("send", f"send TLP {seqs[0]}" if n == 1 else f"send TLPs · {', '.join(map(str, seqs))}",
                  f"ה-RC שולח {'TLP' if n == 1 else 'TLPs'} {', '.join(map(str, seqs))}", act)

    def deliver_tlp(self, corrupt=False, kind=None, count=1):
        """The next `count` TLPs on the link reach the EP; `kind` names the frame for the page."""
        tlps = [self.rc.tx_tlps.pop(0) for _ in range(count)]
        if corrupt:
            tlps[0].crc_ok = False
        seqs = ", ".join(str(t.seq) for t in tlps)
        replay = tlps[0].is_replay
        label = ("TLP %s · bad LCRC" % seqs if corrupt else
                 ("replayed " if replay else "") + ("TLPs · " if count > 1 else "TLP ") + seqs)
        events = {"bad": f"{RLM}TLP {seqs} מגיע עם LCRC שגוי", "future": f"{RLM}TLP {seqs} מגיע לפני זמנו",
                  "dup": f"{RLM}TLP {seqs} מגיע שוב (כפול)", None: f"{RLM}TLP {seqs} מגיע"}
        self.step(kind or ("replay" if replay else "tlp"), label,
                  events[kind] + (" (Replay)" if replay and kind != "dup" else ""),
                  lambda: [self.ep.receive_tlp(t) for t in tlps])

    def deliver_dllp(self, corrupt=False, tamper=None, count=1):
        dllps = [self.ep.tx_dllps.pop(0) for _ in range(count)]
        if corrupt:
            dllps[0].crc_ok = False
        if tamper is not None:
            dllps[0].seq = tamper
        names = ", ".join(f"{d.kind.name.title()} {d.seq}" for d in dllps)
        kind = "bad_dllp" if corrupt else "illegal" if tamper is not None else dllps[0].kind.name.lower()
        label = names + (" · bad CRC" if corrupt else " · unknown seq" if tamper is not None else "")
        event = (f"{RLM}{names} מגיע עם CRC שגוי" if corrupt else
                 f"{RLM}{names} מגיע עם מספר לא מוכר" if tamper is not None else f"{RLM}{names} מגיע")
        self.step(kind, label, event, lambda: [self.rc.receive_dllp(d) for d in dllps])

    def timeout(self):
        self.step("timeout", "replay timer expired", "ה-REPLAY_TIMER פג", self.rc.on_replay_timeout)


def run_a():
    r = Run([2, 3, 1])
    r.start()
    r.send(2)
    r.deliver_tlp()
    r.deliver_tlp()
    r.deliver_dllp()
    r.send(3)
    r.deliver_tlp()
    r.deliver_tlp()
    r.deliver_tlp()
    r.deliver_dllp()
    r.script.done()
    assert not r.rc.tx_tlps and not r.ep.tx_dllps and not r.rc.retry_buffer
    return r.frames


def run_b():
    r = Run([3, 1, 1, 1, 1])
    r.start()
    r.send(4)
    r.deliver_tlp()                                  # 4094 accepted
    r.deliver_tlp(corrupt=True, kind="bad")          # 4095: Nak 4094
    r.deliver_tlp(kind="future")                     # 0: discarded, no second Nak
    r.deliver_tlp(kind="future")                     # 1: discarded
    r.deliver_dllp()                                 # Nak 4094: purge 4094, replay 4095 0 1
    r.deliver_tlp()                                  # replayed 4095 accepted, NAK_SCHEDULED off
    r.deliver_tlp(count=2)                           # 0, 1 accepted: Ack 1
    r.deliver_dllp(corrupt=True)                     # Ack 1 corrupt: ignored
    r.timeout()                                      # replay 4095 0 1 again
    r.deliver_tlp(kind="dup", count=3)               # three duplicates: three Ack 1
    r.deliver_dllp()                                 # Ack 1: purge everything
    r.deliver_dllp()                                 # Ack 1 again: no progress, no effect
    r.deliver_dllp(tamper=9)                         # Ack 9 (the link damaged the number): protocol error
    r.script.done()
    assert not r.rc.tx_tlps and not r.ep.tx_dllps and not r.rc.retry_buffer
    return r.frames


# ------------------------------------------------------------------ stepper frames

def defs(uid):
    m = []
    for c in ("s1", "s2", "s3"):
        m.append(f'<marker id="{uid}-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto"><path class="{c}-fill" d="M0,0 L10,5 L0,10 z"/></marker>')
    return "<defs>" + "".join(m) + "</defs>"


def row(p, x, y, name, before, after, text=None):
    if before != after:
        p.append(f'<rect class="st-cur" x="{x + 150}" y="{y - 17}" width="70" height="24" rx="4"/>')
    p.append(f'<text class="tick" x="{x + 14}" y="{y}">{name}</text>')
    p.append(f'<text class="st-text" x="{x + 214}" y="{y}" text-anchor="end">{text if text is not None else after}</text>')


def seq_boxes(p, x, y, seqs, cls, faded=()):
    for i, s in enumerate(seqs[-5:]):
        bx = x + 30 + i * 42
        extra = " st-faded" if s in faded else ""
        p.append(f'<rect class="{cls}{extra}" x="{bx}" y="{y}" width="38" height="24" rx="3"/>')
        p.append(f'<text class="st-text st-sm{extra}" x="{bx + 19}" y="{y + 16.5}" text-anchor="middle">{s}</text>')
    if not seqs:
        p.append(f'<text class="tick" x="{x + 30}" y="{y + 16}">empty</text>')


def rc_box(p, a, b):
    x = 16
    p.append(f'<rect class="cs-blk" x="{x}" y="36" width="230" height="204" rx="6"/>')
    p.append(f'<text class="coord" x="{x + 115}" y="58" text-anchor="middle" font-weight="700">RC · dll_transmitter</text>')
    row(p, x, 86, "NEXT_TRANSMIT_SEQ", a["nts"], b["nts"])
    row(p, x, 110, "ACKD_SEQ", a["ackd"], b["ackd"])
    p.append(f'<text class="tick" x="{x + 14}" y="136">retry buffer</text>')
    seq_boxes(p, x, 144, b["retry"], "fc-full")
    purged = [s for s in a["retry"] if s not in b["retry"]]
    replayed = [s for s, is_replay in b["tx_tlps"][len(a["tx_tlps"]):] if is_replay]
    note = (f"purged {', '.join(map(str, purged))}" if purged else "") + \
           (("; " if purged else "") + f"replay {', '.join(map(str, replayed))}" if replayed else "")
    if note:
        p.append(f'<text class="tick" x="{x + 14}" y="190">{note}</text>')
    counters = f"bad DLLP {b['bad_dllp']} · protocol err {b['proto']} · replays {b['replays']}"
    cls = "cs-no" if (a["bad_dllp"], a["proto"]) != (b["bad_dllp"], b["proto"]) else "tick"
    p.append(f'<text class="{cls}" x="{x + 14}" y="226" font-size="11">{counters}</text>')


def ep_box(p, a, b):
    x = 394
    p.append(f'<rect class="cs-blk" x="{x}" y="36" width="230" height="204" rx="6"/>')
    p.append(f'<text class="coord" x="{x + 115}" y="58" text-anchor="middle" font-weight="700">EP · dll_receiver</text>')
    row(p, x, 86, "NEXT_RCV_SEQ", a["nrs"], b["nrs"])
    row(p, x, 110, "pending / threshold", (a["pending"], a["threshold"]), (b["pending"], b["threshold"]),
        f"{b['pending']} / {b['threshold']}")
    row(p, x, 134, "NAK_SCHEDULED", a["nak"], b["nak"], int(b["nak"]))
    p.append(f'<text class="tick" x="{x + 14}" y="160">delivered to TL</text>')
    seq_boxes(p, x, 168, b["delivered"], "fc-slot")
    sent = [f"{k.title()} {s}" for k, s in b["tx_dllps"][len(a["tx_dllps"]):]]
    if sent:
        p.append(f'<text class="tick" x="{x + 14}" y="212">sent {", ".join(sent)}</text>')
    counters = f"bad TLP {b['bad_tlp']} · duplicates {b['dups']}"
    cls = "cs-no" if (a["bad_tlp"], a["dups"]) != (b["bad_tlp"], b["dups"]) else "tick"
    p.append(f'<text class="{cls}" x="{x + 14}" y="232" font-size="11">{counters}</text>')


def middle(p, f, uid):
    """The event between the two boxes: at most 20 characters per line."""
    kind, label = f["kind"], f["label"]
    right = {"tlp": ("fc-pkt", "s1"), "replay": ("fc-replay", "s1"), "future": ("fc-pkt", "s1"), "dup": ("fc-pkt", "s1")}
    left = {"ack": ("fc-grant", "s3"), "nak": ("fc-nak", "s2"), "illegal": ("fc-grant", "s3")}
    notes = {"tlp": ("accepted",), "replay": ("accepted",), "future": ("future:", "discarded, no Nak"),
             "dup": ("old: discarded,", "Ack again"), "ack": ("purge through it",), "nak": ("purge, then", "replay the rest"),
             "bad": ("discarded;", "Nak once"), "bad_dllp": ("discarded,", "nothing changes"),
             "illegal": ("protocol error,", "nothing changes"), "send": ("copies kept in the", "retry buffer"),
             "timeout": ("replay everything", "unacknowledged")}
    if kind in right:
        cls, m = right[kind]
        p.append(f'<line class="{cls}" x1="252" y1="118" x2="384" y2="118" marker-end="url(#{uid}-{m})"/>')
    elif kind in left:
        cls, m = left[kind]
        p.append(f'<line class="{cls}" x1="388" y1="118" x2="256" y2="118" marker-end="url(#{uid}-{m})"/>')
    elif kind == "bad":
        p.append('<line class="fc-drop" x1="252" y1="118" x2="308" y2="118"/>')
        p.append('<text class="cs-no" x="320" y="123" text-anchor="middle">✕</text>')
    elif kind == "bad_dllp":
        p.append('<line class="fc-drop" x1="388" y1="118" x2="332" y2="118"/>')
        p.append('<text class="cs-no" x="320" y="123" text-anchor="middle">✕</text>')
    if kind == "illegal":
        p.append('<text class="cs-no" x="320" y="123" text-anchor="middle">?</text>')
    words = label.split(" · ")
    for i, w in enumerate(words):
        p.append(f'<text class="tick" x="320" y="{88 + i * 16}" text-anchor="middle">{w}</text>')
    for i, line in enumerate(notes.get(kind, ())):
        p.append(f'<text class="tick" x="320" y="{140 + i * 16}" text-anchor="middle">{line}</text>')


def frame_svg(k, f, uid):
    p = [f'<svg class="figure" viewBox="0 0 640 250" style="max-width:40rem" role="img" '
         f'aria-label="צעד {k} : {f["event"]}; מצב המשדר והמקבל">', defs(uid)]
    p.append(f'<text class="coord" x="8" y="20" font-weight="700">step {k} · {f["label"].replace(" · ", " ")}</text>')
    rc_box(p, f["before"], f["after"])
    ep_box(p, f["before"], f["after"])
    middle(p, f, uid)
    p.append("</svg>")
    return "".join(p)


def fmt(seqs):
    return ", ".join(map(str, seqs)) if seqs else "ריק"


def caption(k, f):
    a, b, kind = f["before"], f["after"], f["kind"]
    sent = [f"{kd.title()} {s}" for kd, s in b["tx_dllps"][len(a["tx_dllps"]):]]
    purged = [s for s in a["retry"] if s not in b["retry"]]
    replayed = [s for s, r in b["tx_tlps"][len(a["tx_tlps"]):] if r]
    if kind == "start":
        return (f"צעד {k} : הקישור פעיל כבר זמן מה. ה-RC עומד על NEXT_TRANSMIT_SEQ = {b['nts']} ו-ACKD_SEQ = "
                f"{b['ackd']}, ה-Retry Buffer ריק; ה-EP מצפה ל-{b['nrs']} והסף הראשון שהגריל הוא {b['threshold']}.")
    if kind == "send":
        return (f"צעד {k} : {f['event']}. כל אחד מקבל את NEXT_TRANSMIT_SEQ ומקדם אותו; ה-Retry Buffer מחזיק "
                f"{fmt(b['retry'])}, ועותקים נפרדים יצאו לקישור. ‏NEXT_TRANSMIT_SEQ = {b['nts']}.")
    if kind in ("tlp", "replay"):
        n = len(b["delivered"]) - len(a["delivered"])
        head = f"צעד {k} : {f['event']} : {'המספר הצפוי' if n == 1 else 'המספרים הצפויים'}, {'נמסר' if n == 1 else 'נמסרים'} ל-TL"
        nak = " ו-NAK_SCHEDULED כבה" if a["nak"] and not b["nak"] else ""
        if sent:
            return (f"{head}{nak}. ‏NEXT_RCV_SEQ = {b['nrs']}; הספירה הגיעה לסף {a['threshold']}, ולכן יוצא "
                    f"{sent[0]} והסף הבא הוא {b['threshold']}.")
        return f"{head}{nak}. ‏NEXT_RCV_SEQ = {b['nrs']}, {b['pending']} ממתינים ל-Ack מול סף {b['threshold']}."
    if kind == "ack":
        if purged:
            return (f"צעד {k} : {f['event']}. ה-RC מוצא את {a['tx_dllps'][len(a['tx_dllps']) - 1][1] if False else purged[-1]} "
                    f"ב-Retry Buffer ומוחק מהראש עד אליו : {fmt(purged)}. נשאר {fmt(b['retry'])}, ‏ACKD_SEQ = {b['ackd']}.")
        return (f"צעד {k} : {f['event']}. המספר הוא ACKD_SEQ עצמו : Ack חוזר בלי התקדמות, שום דבר לא משתנה.")
    if kind == "bad":
        return (f"צעד {k} : {f['event']}. ה-EP זורק אותו ושולח {sent[0]} (האחרון שנמסר); NAK_SCHEDULED נדלק "
                f"והספירה ל-Ack מתאפסת. ‏NEXT_RCV_SEQ נשאר {b['nrs']}.")
    if kind == "future":
        return (f"צעד {k} : {f['event']} : ה-EP עדיין מצפה ל-{b['nrs']}, ולכן זה TLP \"מהעתיד\". נזרק, ובלי Nak נוסף "
                f"כי NAK_SCHEDULED דולק.")
    if kind == "nak":
        return (f"צעד {k} : {f['event']}. קודם כמו Ack : {fmt(purged)} נמחק ו-ACKD_SEQ = {b['ackd']}; ואז Replay של כל "
                f"מה שנשאר, בסדר ועם המספרים המקוריים : {fmt(replayed)}.")
    if kind == "bad_dllp":
        return (f"צעד {k} : {f['event']}. אי אפשר לסמוך על הסוג ולא על המספר : ה-RC סופר DLLP פגום ולא נוגע "
                f"ב-Retry Buffer ({fmt(b['retry'])}) ולא ב-ACKD_SEQ.")
    if kind == "timeout":
        return (f"צעד {k} : {f['event']} וב-Retry Buffer עוד {fmt(b['retry'])}. ה-RC משדר מחדש את כולם מהעותקים "
                f"השמורים : {fmt(replayed)}.")
    if kind == "dup":
        return (f"צעד {k} : {f['event']}. ה-EP כבר מסר אותם (NEXT_RCV_SEQ = {b['nrs']}), ולכן כל אחד נזרק ועונה "
                f"ב-Ack חוזר : {', '.join(sent)}. ‏Nak אין, כי שום דבר לא חסר.")
    return (f"צעד {k} : {f['event']}. המספר אינו ב-Retry Buffer ואינו ACKD_SEQ ({b['ackd']}) : Data Link Protocol "
            f"Error, נספר ונזרק בלי שינוי.")


def run_stepper(frames, part, aria):
    return stepper([(frame_svg(k, f, f"an{part}{k}"), caption(k, f)) for k, f in enumerate(frames)], aria)


def stepper_legend():
    return legend([("fc-full", "רשומה ב-Retry Buffer"), ("fc-slot", "‏TLP שנמסר ל-Transaction Layer"),
                   ("st-cur", "ערך שהשתנה בצעד הזה"), ("fc-pkt", "‏TLP מה-RC ל-EP"), ("fc-replay", "‏TLP משודר מחדש"),
                   ("fc-grant", "‏Ack מה-EP ל-RC"), ("fc-nak", "‏Nak"), ("fc-drop", "פקט שנפגע על הקו")])


def run_table(frames):
    rows = [f"| צעד | אירוע | {RLM}NEXT_TRANSMIT_SEQ | {RLM}ACKD_SEQ | {RLM}Retry Buffer | {RLM}NEXT_RCV_SEQ | ממתינים / סף | {RLM}NAK_SCHEDULED |",
            "|---|---|---|---|---|---|---|---|"]
    for k, f in enumerate(frames):
        b = f["after"]
        rows.append(f"| {k} | {f['event']} | {b['nts']} | {b['ackd']} | {fmt(b['retry'])} | {b['nrs']} | "
                    f"{b['pending']} / {b['threshold']} | {int(b['nak'])} |")
    return "\n".join(rows)


def figures():
    a, b = run_a(), run_b()
    return {
        "FIG:stepper_a": run_stepper(a, "a", "הזרימה התקינה, צעד אחרי צעד : חמישה TLPs דרך הגלישה ושני Ack-ים מצטברים"),
        "LEG:stepper_a": stepper_legend(), "TAB:stepper_a": run_table(a),
        "FIG:stepper_b": run_stepper(b, "b", "שגיאות, צעד אחרי צעד : TLP פגום, Nak ו-Replay, Ack פגום, טיימר, כפילויות ו-Ack לא חוקי"),
        "LEG:stepper_b": stepper_legend(), "TAB:stepper_b": run_table(b),
    }


if __name__ == "__main__":
    print("\n\n".join(figures().values()))
