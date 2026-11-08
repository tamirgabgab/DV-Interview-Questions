# The page's functions: the edit distance between an expected stream and an actual one
from solution import *  # noqa: F401,F403

print(edit_distance("ABCDEFGH", "ABDEYGHH"))           # 3
print(diff("ABCDEFGH", "ABDEYGHH"))                    # [('missing', 'C', None, 3, 2), ('changed', 'F', 'Y', 6, 5), ('extra', None, 'H', 7, 7)]
print(diff("ABCDEF", "ABDXEF", "changed"))             # [('changed', 'C', 'D', 3, 3), ('changed', 'D', 'X', 4, 4)]
print(edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 2))   # 2
print(edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 1))   # None
print(edit_distance_swaps("ABCDEFGH", "ABDCEFHG"))     # 2
