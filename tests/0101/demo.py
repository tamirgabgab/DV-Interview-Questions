# The page's functions: dice whose sum is distributed as two standard dice
from solution import *  # noqa: F401,F403

print(same_sum((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)))   # True
print(same_sum((1, 1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6)))   # False
print(sum_counts((1, 2), (1, 1, 3)))                      # [0, 0, 2, 2, 1, 1]
print(dice_pairs(6))   # [((1, 2, 2, 3, 3, 4), (1, 3, 4, 5, 6, 8)), ((1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6))]
print(len(dice_pairs(6, low=0)))                          # 5
print(factor_pairs(4))                                    # [((1, 2, 2, 3), (1, 3, 3, 5)), ((1, 2, 3, 4), (1, 2, 3, 4))]
print(len(factor_pairs(8)))                               # 4
