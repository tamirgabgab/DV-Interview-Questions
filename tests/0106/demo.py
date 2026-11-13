# The page's functions: the number that appears once when every other appears twice, three times or k times
from solution import *  # noqa: F401,F403

print(single_twice([4, 1, 2, 1, 2]))                          # 4
print(single_thrice_count([2, 2, 3, 2]))                      # 3
print(single_thrice([0, 1, 0, 1, 0, 1, 99]))                  # 99
print(single_thrice([-2, -2, 1, 1, -3, 1, -3, -3, -4, -2]))   # -4
# one number twice among threes: it ends in twos
print(single_thrice_any([5, 5, 7, 7, 7]))                     # 5
# every number five times, 6 twice
print(single_mod_k([7, -1, 6, 7, -1, 7, 6, -1, 7, -1, 7, -1], 5))   # 6
