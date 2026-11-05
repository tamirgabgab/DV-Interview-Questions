# The page's functions on the example: part a's dp, the LIS of part b, part c's count
from solution import *  # noqa: F401,F403

a = [10, 9, 2, 5, 3, 7, 101, 18]
n, dp, prev = lis_dp(a)
print(n, dp)                       # 4 [1, 1, 1, 2, 2, 3, 4, 4]
print(lis_from_dp(a, dp, prev))    # [2, 5, 7, 101]
print(lis(a))                      # [2, 3, 7, 18]
print(count_lis(a))                # 4
print(count_lis([1, 3, 5, 4, 7]))  # 2
print(lis([3, 4, 5, 1]))           # [3, 4, 5]
