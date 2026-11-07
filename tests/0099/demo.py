# The page's functions: check an IBAN, compute its check digits, build an Israeli one
from solution import *  # noqa: F401,F403

print(to_digits("IL62 0108 0000 0009 9999 999"))      # 0108000000099999999182162
print(mod97(to_digits("IL62 0108 0000 0009 9999 999")))  # 1
print(is_valid("IL62 0108 0000 0009 9999 999"))       # True
print(is_valid("IL62 0108 0000 0009 9999 990"))       # False: one digit changed
print(is_valid("IL62 0108 0000 0009 9999 902"))       # True: two digits, 97 apart, slip through
print(check_digits("IL00 0108 0000 0009 9999 999"))   # 62
print(grouped(israeli_iban(12, 345, 6789012)))        # IL14 0123 4500 0000 6789 012
