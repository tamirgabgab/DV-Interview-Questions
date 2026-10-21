# The two 4-bit LFSRs of the page from 0001, and the period of every polynomial x^4 + ... + 1
from solution import *  # noqa: F401,F403

for name, mask in (("x^4 + x^3 + 1", 0b0011), ("x^4 + x^2 + 1", 0b0101)):
    s, seq = 1, []
    for _ in range(16):
        seq.append(f"{s:04b}")
        s = lfsr_next(s, mask, 4)
    print(name, "period", lfsr_period(mask, 4), ":", " ".join(seq))

print("all polynomials:", {f"{m:04b}": lfsr_period(m, 4) for m in range(1, 16, 2)})
