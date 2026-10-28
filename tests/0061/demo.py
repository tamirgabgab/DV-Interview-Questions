# The longest run of ones with up to k zeros flipped, and the longest window of one value
from solution import *  # noqa: F401,F403

bits = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
print("k = 2:", longest_ones(bits, 2))  # 6
print("k = 0:", longest_ones(bits, 0))  # 4
print("k = 3:", longest_ones(bits, 3))  # 10
print("bus AAABBCBABA, k = 2:", longest_same("AAABBCBABA", 2))  # 6
print("bus ABAACAAB, k = 1:", longest_same("ABAACAAB", 1))  # 5
