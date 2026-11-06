# The credit counter from 3 with N = 10: the formula in every part, and a simulation
from fractions import Fraction
from solution import *  # noqa: F401,F403

print("part a, fair:", walk_odds(3, 10, Fraction(1, 2), Fraction(1, 2)))
full, empty, cycles = walk_odds(3, 10, 0.6, 0.4)
print(f"part b, p = 0.6: full {float(full):.3f}, empty {float(empty):.3f}, cycles {float(cycles):.2f}")
full, empty, cycles = walk_odds(3, 10, 0.3, 0.2)
print(f"part c, p = 0.3, q = 0.2: full {float(full):.3f}, cycles {float(cycles):.2f}")
p, q = rates_to_steps(0.5, 0.25)
full, empty, cycles = walk_odds(3, 10, p, q)
print(f"part d, l1 = 0.5, l2 = 0.25: p = {p}, q = {q}, full {float(full):.3f}, cycles {float(cycles):.2f}")
print("simulated:", simulate(3, 10, 0.5, 0.25, 5000, seed=94))
