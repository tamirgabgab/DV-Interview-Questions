# Transpose an 8 x 8 bit matrix: the loop, the three delta swaps, and 32 x 32 in words
from solution import *  # noqa: F401,F403

x = 0x00000000000000FF                     # row 0 all ones
print(hex(transpose8_loop(x)), hex(transpose8(x)))  # 0x101010101010101 0x101010101010101
print(hex(transpose8(0x8040201008040201)))  # 0x8040201008040201
a = [0xFFFFFFFF] + [0] * 31                # row 0 all ones
transpose32(a)
print(set(a))  # {1}
