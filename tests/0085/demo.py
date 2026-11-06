# The page's functions: the number of base 10, the two of base 4, a guess that fails, the list of part c
from solution import *  # noqa: F401,F403

print(self_describing(10))                                  # [[6, 2, 1, 0, 0, 0, 1, 0, 0, 0]]
print(self_describing(4))                                   # [[1, 2, 1, 0], [2, 0, 2, 0]]
print(self_describing(6))                                   # []
print(is_self_describing([9, 0, 0, 0, 0, 0, 0, 0, 0, 0]))   # False
print(predicted(8))                                         # [[4, 2, 1, 0, 1, 0, 0, 0]]
print(differ(10))                                           # []
