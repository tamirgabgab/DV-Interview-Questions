# The best wand in each position, against the rivals of parts a to c (0.6, then 0.8)
from solution import *  # noqa: F401,F403

chance, wand = best_wand(1, [0.6, 0.8])
print("first:", round(chance, 4), "with a wand of", round(wand, 3))  # 0.6373 with a wand of 0.6
print("third:", round(best_wand(3, [0.6, 0.8])[0], 4))  # 0.651
chance, wand = best_wand(1, [0.8, 0.4])
print("first, rivals 0.8 and 0.4:", round(chance, 4), "with a wand of", round(wand, 3))  # 0.6 with a wand of 1.0
