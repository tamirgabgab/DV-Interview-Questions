#!/usr/bin/env python3
"""Figures and tables of question 0025 (PCIe Ack/Nak reference model).

    python tools/figures/q0025.py > /tmp/q0025.html

blocks(), in page order: the table of the error-free run (part a) and the table of the
run with a corrupt TLP, a corrupt Ack, a replay timeout and an Ack whose number the link
changed (part b), a row per step with the model's method the environment called and, under
it, what went out on the link. NEXT_TRANSMIT_SEQ is left out (the transmitter's invariant gives it:
one past the last entry of the Retry Buffer, or ACKD_SEQ + 1 when it is empty), the other
state columns are named short (NRS, NAK, as on the box's event axis) and the step's number
opens its event cell, so the seven columns fit the page's column. Both runs drive the page's own Python classes through a scripted
"random" source, so the Ack thresholds are the ones the page names; tests/0025 checks
that the page copies match (python tools/figures/fill.py 25 rewrites them).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import load_python  # noqa: E402

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

    def step(self, kind, label, event, action, call, **extra):
        before = self.state()
        action()
        after = self.state()
        self.frames.append({"kind": kind, "label": label, "event": event, "call": call,
                            "before": before, "after": after, **extra})

    def start(self):
        self.step("start", "initial state", "מצב התחלתי", lambda: None, "הבנאים")

    def send(self, n):
        seqs = [(self.rc.next_transmit_seq + i) % 4096 for i in range(n)]

        def act():
            for _ in range(n):
                self.rc.send_tlp(Tlp(self.payload))
                self.payload += 1
        self.step("send", f"send TLP {seqs[0]}" if n == 1 else f"send TLPs · {', '.join(map(str, seqs))}",
                  f"ה-RC שולח {'TLP' if n == 1 else 'TLPs'} {', '.join(map(str, seqs))}", act, times("send_tlp", n))

    def deliver_tlp(self, corrupt=False, kind=None, count=1):
        """The next `count` TLPs on the link reach the EP; `kind` names the frame for the page."""
        tlps = [self.rc.tx_tlps.pop(0) for _ in range(count)]
        if corrupt:
            tlps[0].crc_ok = False
        seqs = ", ".join(str(t.seq) for t in tlps)
        replay = tlps[0].is_replay
        label = ("TLP %s · bad LCRC" % seqs if corrupt else
                 ("replayed " if replay else "") + ("TLPs · " if count > 1 else "TLP ") + seqs)
        tlp, arrive = ("TLPs", "מגיעים") if count > 1 else ("TLP", "מגיע")
        events = {"bad": f"{RLM}{tlp} {seqs} {arrive} עם LCRC שגוי", "future": f"{RLM}{tlp} {seqs} {arrive} לפני זמנו",
                  "dup": f"{RLM}{tlp} {seqs} {arrive} שוב (כפולים)" if count > 1 else f"{RLM}TLP {seqs} מגיע שוב (כפול)",
                  None: f"{RLM}{tlp} {seqs} {arrive}"}
        self.step(kind or ("replay" if replay else "tlp"), label,
                  events[kind] + (" (Replay)" if replay and kind != "dup" else ""),
                  lambda: [self.ep.receive_tlp(t) for t in tlps], times("receive_tlp", count), replay=replay)

    def deliver_dllp(self, corrupt=False, tamper=None, count=1, which=""):
        """The next `count` DLLPs reach the RC; `which` ("הראשון", ...) tells apart equal ones."""
        dllps = [self.ep.tx_dllps.pop(0) for _ in range(count)]
        names = ", ".join(f"{d.kind.name.title()} {d.seq}" for d in dllps)
        if corrupt:
            dllps[0].crc_ok = False
        if tamper is not None:
            dllps[0].seq = tamper
        kind = "bad_dllp" if corrupt else "illegal" if tamper is not None else dllps[0].kind.name.lower()
        label = names + (" · bad CRC" if corrupt else f" · seq changed to {tamper}" if tamper is not None else "")
        names += f" {which}" if which else ""
        event = (f"{RLM}{names} מגיע עם CRC שגוי" if corrupt else
                 f"{RLM}{names} מגיע, המספר שונה ל-{tamper}" if tamper is not None else f"{RLM}{names} מגיע")
        self.step(kind, label, event, lambda: [self.rc.receive_dllp(d) for d in dllps], times("receive_dllp", count))

    def timeout(self):
        self.step("timeout", "replay timer expired", "ה-REPLAY_TIMER פג", self.rc.on_replay_timeout,
                  times("on_replay_timeout", 1))


def times(method, n):
    """The table's call cell: the method the environment called (once a packet; the event
    cell says how many packets)."""
    return f"{RLM}`{method}`"


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
    r.deliver_dllp(which="הראשון")                   # the first Ack 1: purge everything
    r.deliver_dllp(which="השני")                     # the second: no progress, no effect
    r.deliver_dllp(tamper=9, which="השלישי")         # the third, its number changed to 9: protocol error
    r.script.done()
    assert not r.rc.tx_tlps and not r.ep.tx_dllps and not r.rc.retry_buffer
    return r.frames


# ------------------------------------------------------------------ the tables

def fmt(seqs):
    return ", ".join(map(str, seqs)) if seqs else "ריק"


def went_out(f):
    """What the step put on the link, as a second line under the call: the TLPs the RC sent
    or replayed, the DLLPs the EP sent."""
    a, b = f["before"], f["after"]
    tlps = b["tx_tlps"][len(a["tx_tlps"]):]
    dllps = b["tx_dllps"][len(a["tx_dllps"]):]
    if tlps:
        seqs = ", ".join(str(q) for q, _ in tlps)
        many = len(tlps) > 1
        if tlps[0][1]:
            return f"<br>{RLM}Replay של {seqs}"
        return f"<br>{'יוצאים' if many else 'יוצא'} TLP {seqs}"
    names = [f"{k.title()} {q}" for k, q in dllps]
    if len(names) > 1 and len(set(names)) == 1:                  # three equal Acks: say "three"
        return f"<br>יוצאים {COUNT[len(names)]} {names[0]}"
    if names:
        return f"<br>{'יוצאים' if len(names) > 1 else 'יוצא'} " + ", ".join(names)
    return ""


COUNT = {2: "שני", 3: "שלושה", 4: "ארבעה"}


def ltr(text):
    """Numbers read left to right in a right-to-left cell (the RLM keeps the cell RTL)."""
    return RLM + '<span dir="ltr">' + text + "</span>"


def run_table(frames):
    rows = [f"| צעד | קריאה ומה שיצא לקישור | {RLM}ACKD_SEQ | {RLM}Retry Buffer "
            f"| {RLM}NRS | ממתינים / סף | {RLM}NAK |",
            "|---|---|---|---|---|---|---|"]
    for k, f in enumerate(frames):
        b = f["after"]
        counts = ltr(f"{b['pending']} / {b['threshold']}")
        rows.append(f"| **{k}** · {f['event']} | {f['call']}{went_out(f)} | {b['ackd']} | {fmt(b['retry'])} "
                    f"| {b['nrs']} | {counts} | {int(b['nak'])} |")
    return "\n".join(rows)


def blocks():
    return [run_table(run_a()), run_table(run_b())]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
