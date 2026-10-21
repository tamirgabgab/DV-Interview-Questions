# The page example: a burst of 120 words at 100 MHz, read at 80 MHz (part a) and with
# one read slot in four skipped (part b). Periods in steps of 0.05 ns.
from solution import *  # noqa: F401,F403

t_write, t_read = 200, 250
print("part a: formula", fifo_depth(120, 100, 80), "simulation", fifo_fill(120, t_write, t_read)[0])
print("part b: formula", fifo_depth(120, 100, 80, 0.75), "simulation", fifo_fill(120, t_write, t_read, 4)[0])

# Try your own numbers
print("burst 256 at 100 MHz, reader 50 MHz:", fifo_depth(256, 100, 50), fifo_fill(256, 200, 400)[0])
