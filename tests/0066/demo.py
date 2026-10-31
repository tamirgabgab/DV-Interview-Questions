# Merged intervals, the pieces of constant total height, the peak and the ranges over a threshold
from solution import *  # noqa: F401,F403

print("merged:", merge([(1, 3), (2, 6), (8, 10), (15, 18)]))  # [(1, 6), (8, 10), (15, 18)]
print("touching:", merge([(1, 4), (4, 5)]))  # [(1, 5)]
print("pieces:", skyline([(1, 7, 7), (2, 6, 4)]))  # [(1, 2, 7), (2, 6, 11), (6, 7, 7)]
print("one total:", skyline([(0, 2, 3), (2, 4, 3)]))  # [(0, 4, 3)]
pieces = skyline([(0, 4, 2), (1, 3, 3), (2, 6, 1), (5, 8, 4)])
print("peak:", peak(pieces))  # (6, [(2, 3)])
print("at least 4:", above(pieces, 4))  # [(1, 3), (5, 8)]
print("part a by part b:", above(skyline([(s, e, 1) for s, e in [(1, 3), (2, 6), (8, 10), (15, 18)]]), 1))  # [(1, 6), (8, 10), (15, 18)]
