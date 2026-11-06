# The page's functions: adding the chords one at a time, the formula, Euler, and the count
# from the angles of the points
from solution import *  # noqa: F401,F403

print([regions_by_chords(n) for n in range(1, 8)])   # [1, 2, 4, 8, 16, 31, 57]
print(regions(6), euler_regions(6))                  # 31 31
print(count_regions([85, 152, 203, 271, 324, 32]))   # 31
print(count_regions([90, 150, 210, 270, 330, 30]))   # 30
