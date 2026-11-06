# The page's functions: two coins by the formula, then any coins by the remainders and by the plain run
from solution import *  # noqa: F401,F403

print(two_coins(3, 5))                       # (7, 4)
print(two_coins(4, 6))                       # None
print(smallest_payable([6, 9, 20]))          # [0, 49, 20, 9, 40, 29]
print(frobenius([6, 9, 20]))                 # 43
print(frobenius_dp([6, 9, 20]))              # 43
print(can_pay(43, [6, 9, 20]))               # False
print(can_pay(44, [6, 9, 20]))               # True
print(frobenius([4, 6, 9, 20]))              # 11
