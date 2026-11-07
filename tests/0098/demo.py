# Starting code of the run panel of question 0098: the page's Python code is loaded
# as solution.py; call its functions here.
from solution import *  # noqa: F401,F403

print(luhn_sum("4111 1111 1111 1111"), luhn_valid("4111 1111 1111 1111"))   # 30 True
print(luhn_valid("4111 1111 1111 1112"))                                     # False
print(check_digit("411111111111111"))                                         # 1
print(missed_swaps())                                                         # [(0, 9)]
print(israeli_id_valid("000000018"), isbn10_valid("0-306-40615-2"))           # True True
singles, swaps = misses(lambda d: d, lambda d: 3 * d)                        # EAN-13
print(len(singles), swaps)              # 0 [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
