# The two machines of 3 on the bits of 6, and the general one: 7 in base 10, both ways
from solution import *  # noqa: F401,F403

print("MSB 1,1,0 (1, 3, 6):", div3_msb([1, 1, 0]))
print("LSB 0,1,1 (0, 2, 6):", div3_lsb([0, 1, 1]))
digits = [1, 4, 0]                       # 140 = 7 * 20, the highest digit first
print("140 by 7 from the MSB:", div_fsm(digits, 7, base=10))
print("140 by 7 from the LSB:", div_fsm(digits[::-1], 7, base=10, lsb=True))
