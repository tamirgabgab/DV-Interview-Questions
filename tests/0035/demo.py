# The output of the divide-by-3 after every clock edge (rising, falling, rising, ...)
from solution import *  # noqa: F401,F403

wave = div3_50(24)
print("edges:   ", "".join("R" if i % 2 == 0 else "F" for i in range(len(wave))))
print("clk_out: ", "".join(str(v) for v in wave))
steady = wave[6:]
print("period in half-cycles:", 6, " high:", sum(steady[:6]), "of 6")
