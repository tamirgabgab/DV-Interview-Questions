# The page's functions: the ways to climb n stairs with jumps from a set
from solution import *  # noqa: F401,F403

print(count_ways(10, [1, 2]))              # 89
print(count_ways(10, [1, 2, 3]))           # 274
print(list_ways(4, [1, 2]))                # [[1, 1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 2]]
print(count_ways_broken(10, [1, 2], [5]))  # 25
print(count_multisets(10, [1, 2]))         # 6
print(count_ways_exact(10, [1, 2], 7))     # 35
