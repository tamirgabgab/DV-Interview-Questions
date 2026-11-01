# Rotate 1..7 left by 3, both ways, and a full FIFO back to entry 0
from solution import *  # noqa: F401,F403

a = [1, 2, 3, 4, 5, 6, 7]
rotate_reversals(a, 3)
print(a)  # [4, 5, 6, 7, 1, 2, 3]
b = list(range(12))
rotate_cycles(b, 8)
print(b)  # [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]
ram = Ram(["e5", "e6", "e7", "e0", "e1", "e2", "e3", "e4"])
linearize(ram, 3)
print(ram.mem, "in", ram.cycles, "cycles")  # ['e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7'] in 16 cycles
