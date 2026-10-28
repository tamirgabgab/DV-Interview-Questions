# A legal interleaving, then the same stream with two responses of ID 0 swapped
from solution import *  # noqa: F401,F403


def play(events, timeout=100):
    sb = OooScoreboard(timeout)
    for t, op, i, d in events:
        sb.check_timeouts(t)
        if op == "req":
            sb.on_request(i, d, t)
        elif op == "rsp":
            sb.on_response(i, d, t)
        elif op == "reset":
            sb.on_reset()
    sb.final_check()
    return sb.errors or ["no errors"]


legal = [(0, "req", 0, 10), (1, "req", 1, 20), (2, "req", 0, 11), (3, "rsp", 1, 20), (4, "rsp", 0, 10), (5, "rsp", 0, 11)]
swapped = legal[:4] + [(4, "rsp", 0, 11), (5, "rsp", 0, 10)]
print("legal:  ", play(legal))  # ['no errors']
print("swapped:", play(swapped))
