# The page's functions: the fewest flips of k consecutive bits that make every bit 1
from solution import *  # noqa: F401,F403

print(min_flips([0, 0, 0, 1, 0, 1, 1, 0], 3))          # 3
print(min_flips([0, 1, 0], 1))                         # 2
print(min_flips([1, 1, 0], 2))                         # -1
print(min_flips_inplace([0, 0, 0, 1, 0, 1, 1, 0], 3))  # 3
# a grid with 2 x 2 squares, and the same grid with a 1 in the bottom right corner
grid = [[1, 0, 0, 1, 1], [1, 0, 1, 0, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0]]
print(min_flips_2d(grid, 2))                           # 4
grid[3][4] = 1
print(min_flips_2d(grid, 2))                           # -1
