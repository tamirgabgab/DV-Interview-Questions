# The maximum of every window, the longest window with max - min <= limit, and the
# cycle model of the module
from solution import *  # noqa: F401,F403

print("k = 3:", window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
print("k = 1:", window_max([4, 2, 12], 1))  # [4, 2, 12]
print("limit 5:", longest_within([10, 1, 2, 4, 7, 2], 5))  # 4
print("limit 4:", longest_within([8, 2, 4, 7], 4))  # 2
print("limit 0:", longest_within([4, 2, 2, 2, 4, 4, 2, 2], 0))  # 3
print("module, K = 3:", win_max_run([9, 7, 5, 3, 6, 2, 8, 1], 3))  # [9, 9, 9, 7, 6, 6, 8, 8]
