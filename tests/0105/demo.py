# The page's functions: the exact count, one register, HyperLogLog and the pipelined update
from solution import *  # noqa: F401,F403


def line(t):
    return 64 * ((t * 2654435761) % 2**26)      # distinct line addresses, the page's stream


def hll_of(addrs, p=10):
    h = HLL(p)
    for a in addrs:
        h.add(a)
    return h


print(hex(mix64(0)), rank(0, 64), rank(1, 64))  # 0xe220a8397b1dcdaf 65 64
print(distinct_exact([64, 128, 64, 192, 128]))  # 3
print([one_register([line(t) for t in range(1, n + 1)]) for n in (10, 100, 1000, 10000)])  # [5, 7, 10, 13]

h = hll_of([line(t) for t in range(1, 101)])
print(round(h.estimate(), 1), h.regs.count(0))  # 98.6 930
print(round(hll_of([line(t) for t in range(1, 100_001)]).estimate()))  # 106786

a = hll_of([line(t) for t in range(1, 60_001)])
b = hll_of([line(t) for t in range(30_001, 90_001)])
print(round(a.estimate()), round(b.estimate()))  # 62702 63234
a.merge(b)
print(round(a.estimate()))  # 96382

A, B, C = 1984, 1280, 1472                      # register 12 of 16, ranks 4, 1 and 2
print(pipeline([A, B, None, C], 4)[12])  # 4
print(pipeline([A, B, None, C], 4, forward=False)[12])  # 2  (B's write of 1 lost A's 4)
