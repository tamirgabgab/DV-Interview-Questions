# The page's functions: the station from which a full lap never runs dry, and every such station
from solution import *  # noqa: F401,F403

gas, cost = [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]
print(start_naive(gas, cost))                                  # 3
print(start_one_pass(gas, cost))                               # 3
print(start_at_min(gas, cost))                                 # 3
print(start_one_pass([2, 3, 4], [3, 4, 3]))                    # -1
# sum 0: the good starts are the stations at the lowest level
print(good_starts([3, 1, 2, 1, 2, 2, 1], [1, 3, 1, 2, 2, 1, 2]))   # [0, 2, 4, 5]
# sum 3: more good starts than the lowest level
print(good_starts([1, 3, 2, 3, 4], [2, 1, 3, 2, 2]))           # [1, 3, 4]
