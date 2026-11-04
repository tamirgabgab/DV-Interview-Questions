# The page's functions: the counts for N = 4 .. 10, the distinct solutions, and the construction
from solution import *  # noqa: F401,F403

for n in range(4, 11):
    print(n, count_queens(n), count_half(n), distinct(n))
print(next(solutions(8)))          # (0, 4, 7, 5, 2, 6, 1, 3): the first one the search finds
print(construct(8))                # [2, 4, 6, 8, 3, 1, 7, 5]
