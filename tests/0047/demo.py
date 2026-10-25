# Starting code of the run panel of question 0047: the page's Python code is loaded
# as solution.py; call its functions here.
from solution import *  # noqa: F401,F403

print(trap([3, 0, 2, 0, 4]))                              # 7
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))         # 6

leak = [[3, 3, 3, 3, 3],
        [3, 1, 1, 1, 3],
        [3, 1, 5, 1, 3],
        [3, 1, 1, 1, 2],        # the water leaks out at the 2
        [3, 3, 3, 3, 3]]
print(trap_2d(leak))                                      # 8
