"""Question 0025: the PCIe Ack/Nak reference model. The page's Python classes run through
the numerical examples of the reference document, the duplicate / future classification
over the whole sequence space, the two run stories of the page, and random traffic over
a link that corrupts, drops and tampers with packets, checked against the one property
the Data Link Layer promises: every TLP is delivered once, in order. The SystemVerilog
classes run the same way in tests/0025/tb.sv."""

import random
import re
import subprocess
import sys

import pytest

from extract_code import ROOT, load_python, question_path

ns = load_python(25)
Tlp, Dllp, DllpKind, SEQ_MOD = ns["Tlp"], ns["Dllp"], ns["DllpKind"], ns["SEQ_MOD"]
PlainTx, PlainRx = ns["DllTransmitter"], ns["DllReceiver"]
Tx, Rx = ns["TransmitterWithReplay"], ns["ReceiverWithNak"]


def seqs(tlps):
    return [t.seq for t in tlps]


def dllps(rx):
    return [(d.kind, d.seq) for d in rx.tx_dllps]


def send(tx, n, payload=0):
    for i in range(n):
        tx.send_tlp(Tlp(payload + i))


def pass_tlps(tx, rx, n=None):
    """Deliver the next n TLPs on the link (all of them by default)."""
    n = len(tx.tx_tlps) if n is None else n
    for _ in range(n):
        rx.receive_tlp(tx.tx_tlps.pop(0))


def pass_dllps(tx, rx):
    while rx.tx_dllps:
        tx.receive_dllp(rx.tx_dllps.pop(0))


# ------------------------------------------------------------------ the examples of the reference

def test_example_1_cumulative_ack():
    tx, rx = Tx(3), Rx(3, random.Random(0))
    assert (tx.next_transmit_seq, tx.ackd_seq, rx.next_rcv_seq) == (3, 2, 3)
    send(tx, 5)
    assert tx.next_transmit_seq == 8 and seqs(tx.retry_buffer) == [3, 4, 5, 6, 7]
    rx.ack_threshold = 99                                  # no automatic Ack in this example
    pass_tlps(tx, rx, 3)
    assert rx.next_rcv_seq == 6 and rx.accepted_since_ack == 3
    rx.flush_ack()
    assert dllps(rx) == [(DllpKind.ACK, 5)]
    pass_dllps(tx, rx)
    assert seqs(tx.retry_buffer) == [6, 7] and tx.ackd_seq == 5


def test_example_2_rollover_purge_by_position():
    for cls in (PlainTx, Tx):
        tx = cls(4094)
        send(tx, 5)
        assert tx.next_transmit_seq == 3 and seqs(tx.retry_buffer) == [4094, 4095, 0, 1, 2]
        tx.receive_dllp(Dllp(DllpKind.ACK, 1))
        assert seqs(tx.retry_buffer) == [2] and tx.ackd_seq == 1


def test_example_3_nak_after_bad_lcrc():
    tx, rx = Tx(4094), Rx(4094, random.Random(0))
    rx.ack_threshold = 99
    send(tx, 5)
    pass_tlps(tx, rx, 1)
    assert rx.next_rcv_seq == 4095
    bad = tx.tx_tlps.pop(0)
    bad.crc_ok = False
    rx.receive_tlp(bad)
    assert dllps(rx) == [(DllpKind.NAK, 4094)] and rx.nak_scheduled and rx.bad_tlp_count == 1
    pass_tlps(tx, rx, 2)                                   # 0 and 1: out of sequence, no second Nak
    assert dllps(rx) == [(DllpKind.NAK, 4094)] and rx.next_rcv_seq == 4095 and rx.bad_tlp_count == 3
    pass_dllps(tx, rx)
    assert seqs(tx.retry_buffer) == [4095, 0, 1, 2] and tx.ackd_seq == 4094
    assert seqs(tx.tx_tlps) == [2, 4095, 0, 1, 2]          # the original 2 still on the link, then the replay
    assert all(t.is_replay for t in tx.tx_tlps[1:]) and not tx.tx_tlps[0].is_replay
    assert all(t.crc_ok for t in tx.retry_buffer)
    pass_tlps(tx, rx)                                      # 2 (future, discarded), then 4095 0 1 2 accepted
    assert rx.next_rcv_seq == 3 and not rx.nak_scheduled and seqs(rx.received_tlps) == [4094, 4095, 0, 1, 2]


def test_example_4_lost_ack_is_covered_by_the_next_one():
    tx, rx = Tx(10), Rx(10, random.Random(0))
    rx.ack_threshold = 99
    send(tx, 4)
    pass_tlps(tx, rx, 3)
    rx.flush_ack()
    ack = rx.tx_dllps.pop(0)
    assert (ack.kind, ack.seq) == (DllpKind.ACK, 12)
    ack.crc_ok = False
    tx.receive_dllp(ack)
    assert seqs(tx.retry_buffer) == [10, 11, 12, 13] and tx.ackd_seq == 9 and tx.bad_dllp_count == 1
    pass_tlps(tx, rx)
    rx.flush_ack()
    pass_dllps(tx, rx)
    assert tx.retry_buffer == [] and tx.ackd_seq == 13


def test_example_5_duplicate_tlp():
    tx, rx = Tx(10), Rx(10, random.Random(0))
    rx.ack_threshold = 99
    send(tx, 3)
    pass_tlps(tx, rx)
    assert rx.next_rcv_seq == 13
    rx.receive_tlp(Tlp(0x11, seq=11))
    assert seqs(rx.received_tlps) == [10, 11, 12] and rx.next_rcv_seq == 13
    assert dllps(rx) == [(DllpKind.ACK, 12)] and rx.duplicate_count == 1 and not rx.nak_scheduled


def test_transmitter_rejects_corrupt_and_illegal_dllps():
    tx = Tx(100)
    send(tx, 4)
    before = seqs(tx.retry_buffer)
    tx.receive_dllp(Dllp(DllpKind.NAK, 101, crc_ok=False))
    assert seqs(tx.retry_buffer) == before and tx.ackd_seq == 99 and tx.bad_dllp_count == 1 and tx.tx_tlps[4:] == []
    tx.receive_dllp(Dllp(DllpKind.ACK, 7))
    assert seqs(tx.retry_buffer) == before and tx.protocol_error_count == 1
    tx.receive_dllp(Dllp(DllpKind.ACK, 99))                # ACKD_SEQ itself: legal, no effect
    assert seqs(tx.retry_buffer) == before and tx.protocol_error_count == 1
    tx.receive_dllp(Dllp(DllpKind.NAK, 99))                # Nak for ACKD_SEQ: replay everything
    assert seqs(tx.tx_tlps[4:]) == [100, 101, 102, 103] and tx.replay_count == 1
    tx.receive_dllp(Dllp(DllpKind.NAK, 102))
    assert seqs(tx.retry_buffer) == [103] and tx.ackd_seq == 102 and seqs(tx.tx_tlps[8:]) == [103]


def test_plain_models_refuse_what_part_b_handles():
    tx, rx = PlainTx(), PlainRx(rng=random.Random(1))
    send(tx, 2)
    with pytest.raises(ValueError):
        tx.receive_dllp(Dllp(DllpKind.ACK, 7))
    with pytest.raises(ValueError):
        rx.receive_tlp(Tlp(1, seq=5))
    with pytest.raises(ValueError):
        rx.receive_tlp(Tlp(1, seq=0, crc_ok=False))
    pass_tlps(tx, rx)
    assert rx.next_rcv_seq == 2


def test_duplicate_window_covers_the_whole_sequence_space():
    rx = Rx(0)
    for expected in (0, 1, 2047, 2048, 2049, 4095, 1234):
        rx.next_rcv_seq = expected
        for received in range(SEQ_MOD):
            behind = (expected - received) % SEQ_MOD
            assert rx.is_duplicate(received) == (0 < behind <= 2048), (expected, received)


def test_retry_buffer_keeps_a_clean_copy():
    tx = Tx()
    tx.send_tlp(Tlp(0xAB))
    wire = tx.tx_tlps[0]
    wire.crc_ok, wire.seq, wire.payload = False, 77, 0
    assert tx.retry_buffer[0] == Tlp(0xAB, 0, True, False)
    tx.receive_dllp(Dllp(DllpKind.NAK, 4095))
    assert tx.tx_tlps[1] == Tlp(0xAB, 0, True, True)


def test_ack_thresholds_are_random_and_bounded():
    tx, rx = Tx(), Rx(rng=random.Random(3))
    sizes = []
    delivered_at_last_ack = 0
    for _ in range(300):
        send(tx, 1)
        pass_tlps(tx, rx)
        for d in rx.tx_dllps:
            sizes.append(len(rx.received_tlps) - delivered_at_last_ack)
            delivered_at_last_ack = len(rx.received_tlps)
        pass_dllps(tx, rx)
    assert set(sizes) == {1, 2, 3, 4} and sum(sizes) == 300 - rx.accepted_since_ack


# ------------------------------------------------------------------ random lossy traffic

class LossyLink:
    """In-order queues in both directions; the harness corrupts, drops or tampers with a
    packet when it takes it off the link, never with what the models keep."""

    def __init__(self, seed, start):
        self.rng = random.Random(seed)
        self.tx, self.rx = Tx(start), Rx(start, random.Random(seed + 1))
        self.sent = []                                     # payloads, in transmission order
        self.payload = 0
        self.stats = {"corrupt_tlp": 0, "drop_tlp": 0, "corrupt_dllp": 0, "drop_dllp": 0, "illegal": 0, "timeouts": 0}

    def check(self):
        tx, rx = self.tx, self.rx
        delivered = [t.payload for t in rx.received_tlps]
        assert delivered == self.sent[:len(delivered)], "delivered TLPs must be the sent ones, in order"
        assert all(t.crc_ok and not t.is_replay for t in tx.retry_buffer)
        assert seqs(tx.retry_buffer) == [(tx.ackd_seq + 1 + i) % SEQ_MOD for i in range(len(tx.retry_buffer))]
        assert len(tx.retry_buffer) == (tx.next_transmit_seq - tx.ackd_seq - 1) % SEQ_MOD
        assert rx.next_rcv_seq == (self.start + len(rx.received_tlps)) % SEQ_MOD

    def run(self, steps):
        tx, rx, rng = self.tx, self.rx, self.rng
        self.start = rx.next_rcv_seq
        for _ in range(steps):
            r = rng.random()
            if r < 0.35:
                if len(tx.retry_buffer) < 16:
                    tx.send_tlp(Tlp(self.payload))
                    self.sent.append(self.payload)
                    self.payload += 1
            elif r < 0.65:
                if tx.tx_tlps:
                    tlp = tx.tx_tlps.pop(0)
                    q = rng.random()
                    if q < 0.03:
                        tlp.crc_ok = False
                        self.stats["corrupt_tlp"] += 1
                    if 0.03 <= q < 0.05:
                        self.stats["drop_tlp"] += 1
                        continue
                    rx.receive_tlp(tlp)
            elif r < 0.85:
                if rx.tx_dllps:
                    dllp = rx.tx_dllps.pop(0)
                    q = rng.random()
                    if q < 0.03:
                        dllp.crc_ok = False
                        self.stats["corrupt_dllp"] += 1
                    elif q < 0.05:
                        self.stats["drop_dllp"] += 1
                        continue
                    elif q < 0.07:
                        dllp.seq = (tx.ackd_seq + 2048) % SEQ_MOD      # never outstanding: illegal
                        self.stats["illegal"] += 1
                    tx.receive_dllp(dllp)
            elif r < 0.92:
                rx.flush_ack()
            elif not tx.tx_tlps and not rx.tx_dllps and tx.retry_buffer:
                tx.on_replay_timeout()                     # the link is idle, something is owed
                self.stats["timeouts"] += 1
            self.check()
        for _ in range(200):                               # drain: deliver everything, time out as needed
            while tx.tx_tlps:
                rx.receive_tlp(tx.tx_tlps.pop(0))
            rx.flush_ack()
            while rx.tx_dllps:
                tx.receive_dllp(rx.tx_dllps.pop(0))
            self.check()
            if not tx.retry_buffer:
                break
            tx.on_replay_timeout()
        assert not tx.retry_buffer and [t.payload for t in rx.received_tlps] == self.sent
        return self


def test_random_lossy_traffic_delivers_everything_once_in_order():
    totals = {}
    delivered = 0
    for seed in range(6):
        link = LossyLink(seed, start=random.Random(seed).choice([0, 4000, 4090, 2047])).run(20000)
        delivered += len(link.sent)
        for k, v in link.stats.items():
            totals[k] = totals.get(k, 0) + v
        totals["replays"] = totals.get("replays", 0) + link.tx.replay_count
        totals["dups"] = totals.get("dups", 0) + link.rx.duplicate_count
        totals["proto"] = totals.get("proto", 0) + link.tx.protocol_error_count
        assert link.tx.protocol_error_count == link.stats["illegal"]
        assert link.tx.bad_dllp_count == link.stats["corrupt_dllp"]
    assert delivered > 8192, "several wraps of the 12-bit space"
    assert all(v > 20 for v in totals.values()), totals


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0025.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(25).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row


def test_explorer_matches_page_classes():
    """The Ack/Nak explorer: its engine against TransmitterWithReplay and ReceiverWithNak on
    300 random events (sends, deliveries, corruptions, losses, the two timers) with the
    same scripted Ack thresholds, state by state; and its two scripts end where the page
    tables end."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(25)
    events = []
    for _ in range(300):
        r = rng.random()
        if r < 0.3:
            events.append({"type": "send", "n": rng.randint(1, 3)})
        elif r < 0.6:
            events.append({"type": "tlp", "how": rng.choice(["ok", "ok", "ok", "bad", "lose"])})
        elif r < 0.85:
            events.append({"type": "dllp", "how": rng.choice(["ok", "ok", "ok", "bad", "lose"])})
        elif r < 0.93:
            events.append({"type": "flush"})
        else:
            events.append({"type": "timeout"})
    thresholds = [rng.randint(1, 4) for _ in range(2000)]
    got = node_json(f"""
      const m = {explorer_require()};
      const th = {json.dumps(thresholds)}, draw = () => th.shift();
      let s = m.anInit(4090, draw);
      const out = [];
      for (const ev of {json.dumps(events)}) {{
        s = m.anApply(s, ev, draw).state;
        out.push([s.nts, s.ackd, s.retry.map((t) => t.seq), s.link.map((t) => [t.seq, t.crcOk, t.replay]),
                  s.dllps.map((d) => [d.kind, d.seq, d.crcOk]), s.nrs, s.nak, s.pending, s.threshold, s.received,
                  s.badDllp, s.proto, s.replays, s.badTlp, s.dups]);
      }}
      const a = m.anRun(m.AN_SCRIPTS.a, () => 1).pop(), b = m.anRun(m.AN_SCRIPTS.b, () => 1).pop();
      console.log(JSON.stringify({{ out, a: [a.nts, a.ackd, a.nrs, a.retry.length], b: [b.nts, b.ackd, b.nrs, b.badDllp, b.proto, b.replays, b.badTlp, b.dups] }}));""")

    class Script:
        def __init__(self, values):
            self.values = list(values)

        def randint(self, a, b):
            v = self.values.pop(0)
            assert a <= v <= b
            return v

    rc, ep = Tx(4090), Rx(4090, Script(thresholds))
    payload = 0xA0
    for ev, g in zip(events, got["out"]):
        if ev["type"] == "send":
            for _ in range(ev["n"]):
                rc.send_tlp(Tlp(payload))
                payload += 1
        elif ev["type"] == "tlp":
            if rc.tx_tlps:
                t = rc.tx_tlps.pop(0)
                if ev["how"] != "lose":
                    if ev["how"] == "bad":
                        t.crc_ok = False
                    ep.receive_tlp(t)
        elif ev["type"] == "dllp":
            if ep.tx_dllps:
                d = ep.tx_dllps.pop(0)
                if ev["how"] != "lose":
                    if ev["how"] == "bad":
                        d.crc_ok = False
                    rc.receive_dllp(d)
        elif ev["type"] == "flush":
            ep.flush_ack()
        else:
            rc.on_replay_timeout()
        expected = [rc.next_transmit_seq, rc.ackd_seq, [t.seq for t in rc.retry_buffer],
                    [[t.seq, t.crc_ok, t.is_replay] for t in rc.tx_tlps],
                    [[d.kind.name, d.seq, d.crc_ok] for d in ep.tx_dllps],
                    ep.next_rcv_seq, ep.nak_scheduled, ep.accepted_since_ack, ep.ack_threshold,
                    [t.seq for t in ep.received_tlps],
                    rc.bad_dllp_count, rc.protocol_error_count, rc.replay_count, ep.bad_tlp_count, ep.duplicate_count]
        assert g == expected, ev
    assert got["a"] == [3, 2, 3, 0]                       # the part a table: NEXT_TRANSMIT_SEQ 3, ACKD_SEQ 2, NEXT_RCV_SEQ 3
    assert got["b"] == [2, 1, 2, 1, 1, 2, 3, 3]           # the part b table and its counters
