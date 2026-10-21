# The four rules on the page traces: a good transaction and three violations
from solution import *  # noqa: F401,F403

def trace(req, ack):
    return [int(c) for c in req], [int(c) for c in ack]

print("good:        ", check_handshake(*trace("01110000", "00010000")))
print("late ack:    ", check_handshake(*trace("01111110", "00000100")))
print("req dropped: ", check_handshake(*trace("01100000", "00000000")))
print("orphan ack:  ", check_handshake(*trace("00000000", "00100000")))
