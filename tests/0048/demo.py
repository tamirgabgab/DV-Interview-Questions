# The shortest path with the food line tilted by theta degrees (part c)
from solution import *  # noqa: F401,F403

z, food, water = tilted_path(7, 3, 1, 2, 15)
print("z:", round(z, 3))  # 10.456
print("food stop:", tuple(round(v, 2) for v in food))  # (0.8, 3.22)
print("water stop:", round(water[0], 2))  # 4.62
print("theta = 0, part a:", round(tilted_path(7, 3, 1, 2, 0)[0] ** 2, 6))  # 98.0
print("theta = 45, z^2:", round(tilted_path(7, 3, 1, 2, 45)[0] ** 2, 6))  # 106.0
