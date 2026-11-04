# Which pocket: point pockets (part b), from the corner (part c) and from anywhere (part d)
import math
from fractions import Fraction
from solution import *  # noqa: F401,F403

print(point_pocket(360, 180, Fraction(3, 4)))       # ((0, 180), 3)
print(point_pocket(360, 180, Fraction(180, 241)))   # ((360, 0), 599)
print(corner_shot(360, 180, 37, 9))                 # (4, 3, (0, 180))
print(corner_shot(360, 180, 37, 1))                 # (211, 159, (180.0, 180))
print(find_pocket(360, 180, 37, 9))                 # (0, 180)
centre = math.degrees(math.atan2(7, 6))
print(find_pocket(360, 180, centre, 9, 180, 90))    # (0, 0)
print(find_pocket(360, 180, 45, 9, 180, 45, max_k=10000))   # None
