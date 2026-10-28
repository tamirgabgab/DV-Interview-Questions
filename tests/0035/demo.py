# The output of the divide-by-3 after every clock edge (rising, falling, rising, ...)
from solution import *  # noqa: F401,F403

wave = div3_50(24)
print("edges:   ", "".join("R" if i % 2 == 0 else "F" for i in range(len(wave))))  # RFRFRFRFRFRFRFRFRFRFRFRF
print("clk_out: ", "".join(str(v) for v in wave))  # 000011100011100011100011
steady = wave[6:]
print("period in half-cycles:", 6, " high:", sum(steady[:6]), "of 6")  # 6  high: 3 of 6

# part b: divide by 5, 2.5 cycles high and 2.5 low
wave5 = div_odd_50(5, 40)
print("N = 5:   ", "".join(str(v) for v in wave5))  # 0000001111100000111110000011111000001111
