# The weights of a load: on one pan (binary), on two pans (balanced ternary), with copies
from solution import *  # noqa: F401,F403

print("one pan, 40:", one_pan(40, 6))  # [0, 0, 0, 1, 0, 1]
print("two pans, 25:", two_pans(25, 4))  # [1, -1, 0, 1]
print("two pans, 40:", two_pans(40, 4))  # [1, 1, 1, 1]
print("two pans, 41:", two_pans(41, 4))  # None
print("two copies, 40:", placement(40, 3, 2))  # [0, -2, 2]
print("the check:", balances(40, 2, True, placement(40, 3, 2)))  # True
