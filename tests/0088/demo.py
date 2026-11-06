# The page's functions: one round, the rounds to all zeros, the power-of-2 test, the cycle
from solution import *  # noqa: F401,F403

print(ducci_step([2, 6, 11, 4]))                # [4, 5, 7, 2]
print(steps_to_zero([2, 6, 11, 4]))             # 6
print(steps_to_zero([0, 7, 20, 44]))            # 13
print([n for n in range(1, 20) if always_zero(n)])   # [1, 2, 4, 8, 16]
print(ducci_orbit((0, 0, 1)))                   # (1, 3)
print(ducci_orbit((1, 2, 3, 4, 5)))             # (2, 15)
