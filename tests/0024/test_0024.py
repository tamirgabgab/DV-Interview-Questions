"""Question 0024: the USB4 Path credit reference model. The page's Python classes run
through the six numerical examples of the specification, an exhaustive check of the
transmit rule against the two-clause formula, the violations the model must report, and
random lossy traffic through an in-order link with an independent integer bookkeeping;
the SystemVerilog classes run the same way in tests/0024/tb.sv."""

import random
import re
import subprocess
import sys
from itertools import product

import pytest

from extract_code import ROOT, load_python, question_path

ns = load_python(24)
TunneledPacket, CreditGrant, CreditSync = ns["TunneledPacket"], ns["CreditGrant"], ns["CreditSync"]
Egress, Ingress = ns["EgressSyncModel"], ns["IngressSyncModel"]
forward_distance = ns["forward_distance"]
HOP = 3


def pair(credits):
    return Egress(HOP), Ingress(HOP, credits)


def grant(eg, ing):
    eg.consume_credit_grant(ing.build_credit_grant())


def send(eg, ing, accepted=True, packet_id=0):
    eg.on_packet_transmitted()
    ing.on_packet_received(TunneledPacket(HOP, packet_id), accepted)


def counters(eg, ing):
    """(PCC, PCL, PCR, PCA, occupancy)."""
    return eg.pcc, eg.pcl, ing.pcr, ing.pca, ing.rx_occupancy


def test_example_a_initial_grant_and_normal_traffic():
    eg, ing = pair(5)
    assert counters(eg, ing) == (0, 0, 0, 5, 0) and not eg.can_transmit()
    grant(eg, ing)
    assert counters(eg, ing) == (0, 5, 0, 5, 0)
    for n in (1, 2, 3):
        send(eg, ing, packet_id=n)
        assert counters(eg, ing) == (n, 5, n, 5, n)
    ing.on_packet_dequeued()
    assert counters(eg, ing) == (3, 5, 3, 6, 2)
    ing.on_packet_dequeued()
    assert counters(eg, ing) == (3, 5, 3, 7, 1)
    assert ing.build_credit_grant().credits == 7
    grant(eg, ing)
    assert counters(eg, ing) == (3, 7, 3, 7, 1) and forward_distance(eg.pcc, eg.pcl) == 4
    for _ in range(4):
        assert eg.can_transmit()
        send(eg, ing)
    assert counters(eg, ing) == (7, 7, 7, 7, 5) and not eg.can_transmit()


def test_example_b_dropped_packet_and_credit_sync():
    eg, ing = pair(5)
    grant(eg, ing)
    send(eg, ing, packet_id=1)
    assert counters(eg, ing) == (1, 5, 1, 5, 1)
    send(eg, ing, accepted=False, packet_id=2)           # transmitted, lost before the Ingress
    assert counters(eg, ing) == (2, 5, 1, 5, 1)
    send(eg, ing, packet_id=3)
    assert counters(eg, ing) == (3, 5, 2, 5, 2)
    sync = eg.build_credit_sync()
    assert sync.pcc == 3
    ing.consume_credit_sync(sync)
    assert counters(eg, ing) == (3, 5, 3, 6, 2)          # PCA repaired, occupancy untouched
    ing.on_packet_dequeued()
    ing.on_packet_dequeued()
    assert counters(eg, ing) == (3, 5, 3, 8, 0)
    assert ing.build_credit_grant().credits == 8
    grant(eg, ing)
    assert counters(eg, ing) == (3, 8, 3, 8, 0) and forward_distance(eg.pcc, eg.pcl) == 5


def test_example_c_credit_exhaustion():
    eg = Egress(HOP)
    eg.pcc, eg.pcl = 9, 10
    assert eg.can_transmit()
    eg.on_packet_transmitted()
    assert eg.pcc == 10 and not eg.can_transmit()
    eg.consume_credit_grant(CreditGrant(HOP, 13))
    assert (eg.pcc, eg.pcl) == (10, 13)
    for _ in range(3):
        assert eg.can_transmit()
        eg.on_packet_transmitted()
    assert not eg.can_transmit()


def test_example_d_wraparound_of_the_transmit_rule():
    eg = Egress(HOP)
    eg.pcc, eg.pcl = 251, 254
    seen = []
    while eg.can_transmit():
        eg.on_packet_transmitted()
        seen.append(eg.pcc)
    assert seen == [252, 253, 254]
    eg.consume_credit_grant(CreditGrant(HOP, 2))
    assert eg.pcl == 2 and eg.pcc == 254 and eg.can_transmit()
    seen = []
    while eg.can_transmit():
        eg.on_packet_transmitted()
        seen.append(eg.pcc)
    assert seen == [255, 0, 1, 2]


def test_example_e_sync_correction_across_the_wrap():
    ing = Ingress(HOP, 10)
    ing.pca, ing.pcr = 254, 253
    ing.consume_credit_sync(CreditSync(HOP, 1))
    assert (ing.pca, ing.pcr) == (2, 1)


def test_example_f_dequeue_does_not_change_pcr():
    ing = Ingress(HOP, 20)
    ing.pcr, ing.pca, ing.rx_occupancy = 12, 20, 3
    ing.on_packet_dequeued()
    assert (ing.pcr, ing.pca, ing.rx_occupancy) == (12, 21, 2)
    ing.on_packet_dequeued()
    ing.on_packet_dequeued()
    assert (ing.pcr, ing.pca, ing.rx_occupancy) == (12, 23, 0)
    assert ing.build_credit_grant() == CreditGrant(HOP, 23)


def test_transmit_rule_matches_the_two_clause_formula():
    eg = Egress(HOP)
    for pcc, pcl in product(range(256), repeat=2):
        eg.pcc, eg.pcl = pcc, pcl
        s = pcl - pcc
        spec = (0 < s < 128) or (s < 0 and pcc - pcl > 128)
        assert eg.can_transmit() == spec, (pcc, pcl)
        assert forward_distance(pcc, pcl) == (pcl - pcc) % 256


def test_grant_overwrites_and_carries_pca():
    eg, ing = pair(4)
    grant(eg, ing)
    grant(eg, ing)                                        # a repeated grant adds nothing
    assert eg.pcl == 4 and forward_distance(eg.pcc, eg.pcl) == 4
    send(eg, ing)
    ing.on_packet_dequeued()
    assert ing.build_credit_grant().credits == 5         # cumulative, not the 4 free slots
    eg.consume_credit_grant(CreditGrant(HOP, 2))          # a stale grant moves PCL back
    assert eg.pcl == 2


def test_more_than_127_credits_cannot_be_used():
    eg, ing = pair(200)
    grant(eg, ing)
    assert eg.pcl == 200 and not eg.can_transmit()       # 200 ahead reads as "behind"
    eg, ing = pair(127)
    grant(eg, ing)
    assert eg.can_transmit() and forward_distance(eg.pcc, eg.pcl) == 127


def test_violations_are_reported_and_change_nothing():
    for credits in (0, 256, 1000):
        with pytest.raises(ValueError):
            Ingress(HOP, credits)
    eg, ing = pair(2)
    with pytest.raises(ValueError):
        eg.on_packet_transmitted()                        # no credit yet
    with pytest.raises(ValueError):
        eg.consume_credit_grant(CreditGrant(HOP + 1, 9))  # another Path's grant
    with pytest.raises(ValueError):
        ing.on_packet_received(TunneledPacket(HOP + 1), True)
    with pytest.raises(ValueError):
        ing.consume_credit_sync(CreditSync(HOP + 1, 1))
    with pytest.raises(ValueError):
        ing.on_packet_dequeued()                          # empty buffer
    assert counters(eg, ing) == (0, 0, 0, 2, 0)
    grant(eg, ing)
    send(eg, ing)
    send(eg, ing)
    with pytest.raises(ValueError):
        eg.on_packet_transmitted()                        # credits exhausted
    with pytest.raises(ValueError):
        ing.on_packet_received(TunneledPacket(HOP), True)  # buffer full
    ing.on_packet_received(TunneledPacket(HOP), False)   # a corrupted packet is fine: no change
    assert counters(eg, ing) == (2, 2, 2, 2, 2)


class Bookkeeping:
    """Plain integers next to the modulo counters: transmitted, received, dequeued, lost,
    and how many of the losses a Credit Sync has already handed back."""

    def __init__(self, credits):
        self.credits = credits
        self.T = self.R = self.D = self.L = self.credited = 0

    def check(self, eg, ing):
        assert eg.pcc == self.T % 256
        assert ing.pcr == (self.R + self.credited) % 256
        assert ing.pca == (self.credits + self.D + self.credited) % 256
        assert ing.rx_occupancy == self.R - self.D <= self.credits


def drive(seed, credits, steps, loss):
    """Random traffic through an in-order link that may drop packets; grants and syncs
    travel on the same links. Returns the bookkeeping after a final sync-and-grant."""
    rng = random.Random(seed)
    eg, ing = pair(credits)
    book = Bookkeeping(credits)
    to_device, to_host = [], []                           # in-order links, one per direction

    def deliver_to_device():
        kind, item = to_device.pop(0)
        if kind == "sync":
            ing.consume_credit_sync(item)
            book.credited = book.L                        # every earlier packet arrived or was lost
        elif rng.random() < loss:
            book.L += 1
        else:
            ing.on_packet_received(item, True)
            book.R += 1

    for _ in range(steps):
        r = rng.random()                                  # one event kind per step; a kind
        if r < 0.30:                                      # that is not possible now is skipped
            if eg.can_transmit():
                eg.on_packet_transmitted()
                book.T += 1
                to_device.append(("pkt", TunneledPacket(HOP, book.T)))
        elif r < 0.65:
            if to_device:
                deliver_to_device()
        elif r < 0.80:
            if ing.rx_occupancy:
                ing.on_packet_dequeued()
                book.D += 1
        elif r < 0.87:
            to_host.append(ing.build_credit_grant())
        elif r < 0.95:
            if to_host:
                eg.consume_credit_grant(to_host.pop(0))
        else:
            to_device.append(("sync", eg.build_credit_sync()))
        book.check(eg, ing)
    while to_device:
        deliver_to_device()
    while ing.rx_occupancy:
        ing.on_packet_dequeued()
        book.D += 1
    to_device.append(("sync", eg.build_credit_sync()))
    deliver_to_device()
    eg.consume_credit_grant(ing.build_credit_grant())
    book.check(eg, ing)
    assert forward_distance(eg.pcc, eg.pcl) == credits   # repaired: credits = free slots
    return book


def test_random_lossy_traffic_never_overflows_and_syncs_repair():
    transmitted = lost = 0
    for seed in range(12):
        credits = random.Random(seed).choice([1, 2, 5, 16, 64, 127])
        book = drive(seed, credits, steps=6000, loss=0.06)
        transmitted += book.T
        lost += book.L
    assert transmitted > 4000 and lost > 100               # many wraps, many losses


def test_without_sync_losses_leak_credits_until_the_path_stalls():
    eg, ing = pair(3)
    grant(eg, ing)
    for n in range(3):
        send(eg, ing, accepted=False, packet_id=n)        # three losses
        ing.on_packet_dequeued() if ing.rx_occupancy else None
        grant(eg, ing)
    assert ing.rx_occupancy == 0 and not eg.can_transmit()   # empty buffer, no credits
    ing.consume_credit_sync(eg.build_credit_sync())
    grant(eg, ing)
    assert forward_distance(eg.pcc, eg.pcl) == 3


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0024.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(24).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="figure.*?</svg>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row
