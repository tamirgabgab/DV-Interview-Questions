# The page's functions: the fewest meetings and the colour, the plan of the construction
from solution import *  # noqa: F401,F403

print(min_meetings((13, 15, 17)))               # None
print(min_meetings((13, 16, 17)))               # (16, 2)
print(meetings_to((13, 16, 17), 0))             # None
print(min_meetings((14, 15, 17)))               # (17, 1)
print(min_meetings((9, 0, 3)))                  # (3, 0)
print(len(meeting_plan((13, 16, 17), 2)))       # 16
print(meeting_plan((7, 1, 3), 2)[:3])           # [(0, 1), (0, 2), (0, 1)]
