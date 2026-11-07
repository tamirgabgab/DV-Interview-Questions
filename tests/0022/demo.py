# The page's functions: the number of paths in a grid, right and down or with up too
from solution import *  # noqa: F401,F403

grid = [[0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]]
print(paths_rd(3, 7), paths_rd_dp(3, 7))            # 28 28
print(paths_rd_mod(1000, 1000))                     # 965601742
print(paths_rd_blocked(grid))                       # 9
print(paths_rud(3, 7))                              # 729
print(paths_rud_blocked(grid))                      # 32
print(count_walks(grid, [(0, 1), (1, 0), (-1, 0)]))  # 32
