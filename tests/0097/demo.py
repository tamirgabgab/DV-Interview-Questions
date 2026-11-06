# The page's functions: the root bit by bit, the module's registers after each clock, the
# 16-bit corner inputs (every step edge, the powers of 2 and the ends), division, the cube root
from solution import *  # noqa: F401,F403

print(isqrt_bits(1000))                  # (31, 39)
print(isqrt_bits(65535))                 # (255, 510)
print(isqrt_bits(10**16 - 1, 54))        # (99999999, 199999998)
for regs in isqrt_seq_model(1000):       # (k, root, rem, busy, done) after each clock
    print(regs)
print(len(corner_inputs(16, 0)))         # 525
print(divide_bits(1000, 7))              # (142, 6)
print(icbrt_bits(1000))                  # (10, 0)
print(icbrt_bits(2**24 - 1))             # (255, 195840)
