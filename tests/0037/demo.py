# The page's functions: the edit distance between an expected stream and an actual one
from solution import *  # noqa: F401,F403

print(edit_distance("ABCDEFGH", "ABDEYGHH"))           # 3
print(diff("ABCDEFGH", "ABDEYGHH"))                    # [('missing', 'C', None), ('changed', 'F', 'Y'), ('extra', None, 'H')]
print(diff("ABCDEF", "ABDXEF", "changed"))             # [('changed', 'C', 'D'), ('changed', 'D', 'X')]
print(edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 2))   # 2
print(edit_distance_within("ABCDEFGHIJKL", "ABCEFGHIXJKL", 1))   # None
print(edit_distance_swaps("ABCDEFGH", "ABDCEFHG"))     # 2
