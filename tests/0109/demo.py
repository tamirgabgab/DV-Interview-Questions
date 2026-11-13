# The page's functions: how many fleets reach the target, and when every car hits the car ahead
from solution import *  # noqa: F401,F403

print(car_fleets(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))      # 3
# a meeting at time 1/2, and still one fleet arriving at 9
print(car_fleets(10, [0, 1], [3, 1]))                          # 1
# 10 / 3 and 9 / 3 are not equal: two fleets
print(car_fleets(10, [0, 1], [3, 3]))                          # 2
print([str(t) for t in collision_times([3, 5, 6, 9], [4, 4, 3, 1])])   # ['2', '1', '3/2', '-1']
print([float(t) for t in collision_times([1, 2, 4, 7], [2, 1, 3, 1])])   # [1.0, -1.0, 1.5, -1.0]
