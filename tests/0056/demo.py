# The page's six ants: when the last falls, how many collisions, and when each one falls
from solution import *  # noqa: F401,F403

pos, dirs = [10, 25, 40, 60, 75, 90], [1, -1, 1, -1, -1, 1]
print("last ant off after", last_fall(pos, dirs), "s")
print("collisions:", collisions(pos, dirs))
print("fall times, ants from the left:", fall_times(pos, dirs))
print("on a ring with four going right:", ring_after([1, 1, 1, -1, -1, 1]))
