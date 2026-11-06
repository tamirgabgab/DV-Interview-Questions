# The page's functions: the simple algorithm, the exact worst case, the burnt pancakes
from solution import *  # noqa: F401,F403

s, flips = simple_sort([3, 1, 5, 4, 2])
print(s, len(flips))                                  # [1, 2, 3, 4, 5] 7
d = pancake_distances(5)
print(best_flips((3, 1, 5, 4, 2), d))                 # [2, 4, 2, 5, 2]
print([pancake_number(n) for n in range(1, 8)])       # [0, 1, 3, 4, 5, 7, 8]
print(burnt_simple([-1, -2, -3])[1])                  # [3, 1, 3, 2, 1, 2, 1]
print(max(burnt_distances(4).values()))               # 8
