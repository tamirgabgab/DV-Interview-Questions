"""Question 0038: the page's reference model (check_handshake, as published) on the page
traces (one good transaction, three violations), on edge cases, and against a second,
independent formulation on random traffic."""

import random

from extract_code import load_python

check_handshake = load_python(38)["check_handshake"]


def wave(req: str, ack: str):
    return [int(c) for c in req], [int(c) for c in ack]


def only(fails, **expected):
    return {k: v for k, v in fails.items() if v} == expected


def test_page_traces():
    # cycle:                0 1 2 3 4 5 6 7
    assert only(check_handshake(*wave("01110000", "00010000")))                 # good
    assert only(check_handshake(*wave("01111100", "00000100")), late=[4])      # late ack (cycle 5)
    assert only(check_handshake(*wave("01100000", "00000000")), hold=[3], late=[4])   # req dropped
    assert only(check_handshake(*wave("00000000", "00100000")), orphan=[2])    # orphan ack
    assert only(check_handshake(*wave("01111100", "00010000")), drop=[4], hold=[6])   # req held after ack, then dropped without one


def test_window_and_edges():
    assert only(check_handshake(*wave("0110000", "0010000")))                   # ack after 1
    assert only(check_handshake(*wave("0111100", "0000100")))                   # ack after 3: still in time
    assert only(check_handshake(*wave("0111110", "0000010")), late=[4])        # ack after 4
    assert only(check_handshake(*wave("0111", "0000")))                         # window cut by the end: not counted
    assert only(check_handshake(*wave("1110", "0010")))                         # req high at cycle 0 is a rise
    assert only(check_handshake(*wave("011", "001"), max_wait=1))               # a shorter window
    assert only(check_handshake(*wave("0110", "0000"), max_wait=1), hold=[3], late=[2])


def independent(req, ack, max_wait=3):
    """A second formulation: walk the transactions as a state machine."""
    fails = {"hold": [], "late": [], "orphan": [], "drop": []}
    n = len(req)
    for t in range(n):
        if ack[t] and not req[t]:
            fails["orphan"].append(t)
        if t and ack[t - 1] and req[t]:
            fails["drop"].append(t)
        if t and req[t - 1] and not ack[t - 1] and not req[t]:
            fails["hold"].append(t)
        if req[t] and (t == 0 or not req[t - 1]) and t + max_wait < n and not any(ack[t + 1:t + 1 + max_wait]):
            fails["late"].append(t + max_wait)
    return fails


def test_random_against_independent_model():
    rng = random.Random(38)
    for _ in range(200):
        n = rng.randint(5, 40)
        req = [rng.random() < 0.6 for _ in range(n)]
        ack = [rng.random() < 0.3 for _ in range(n)]
        req, ack = [int(v) for v in req], [int(v) for v in ack]
        assert check_handshake(req, ack) == independent(req, ack)
