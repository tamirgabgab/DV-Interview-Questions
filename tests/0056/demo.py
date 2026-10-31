# The window of 3 bits both ways, and the general one: 4 decimal digits by 7
from solution import *  # noqa: F401,F403

print("LSB 1,1,0,1 (001, 011, 110, 101):", win3_lsb([1, 1, 0, 1], 3))  # [False, True, True, False]
print("MSB 1,0,1,1 (100, 010, 101, 110):", win3_msb([1, 0, 1, 1], 3))  # [False, False, False, True]
digits = [7, 0, 0, 7]                    # 1234 -> 2347, 3470, 4700, 7007 = 7 * 1001
print("window of 4 from 1234, by 7:", win_div(digits, 7, base=10, L=4, init=1234))  # [False, False, False, True]
