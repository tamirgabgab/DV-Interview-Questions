# The page's functions: the largest and the smallest number made by concatenating a list
from solution import *  # noqa: F401,F403

print(largest_number([3, 30, 34, 5, 9]))      # 9534330
print(largest_brute([3, 30, 34, 5, 9]))       # 9534330
print(largest_number([0, 0]))                 # 0
print(largest_number([12, 1212]))             # 121212
print(concat_order("3", "30"))                # -1
# part c: the smallest number with no leading zero
print(smallest_number([0, 1, 10]))            # 1001
print(smallest_number([3, 30, 34, 5, 9]))     # 3033459
print(smallest_number([0, 2, 21]))            # 2021
print(smallest_number([20, 1, 0]))            # 1020
