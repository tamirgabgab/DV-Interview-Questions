# The page's functions: check an IBAN, the hardware checker clock by clock, its check digits
from solution import *  # noqa: F401,F403

print(to_digits("IL62 0108 0000 0009 9999 999"))      # 0108000000099999999182162
print(mod97(to_digits("IL62 0108 0000 0009 9999 999")))  # 1
print(is_valid("IL62 0108 0000 0009 9999 999"))       # True
print(is_valid("IL62 0108 0000 0009 9999 990"))       # False: one digit changed
print(is_valid("IL62 0108 0000 0009 9999 902"))       # True: two digits, 97 apart, slip through
print(check_stream(stream("IL62 0108 0000 0009 9999 999")))   # True
print(check_digits("IL00 0108 0000 0009 9999 999"))   # 62
